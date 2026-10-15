"""Definition-based Z3 oracle and fresh-process reduction checks."""
import argparse
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
from z3 import Int, If, Or, Solver, Sum, sat, unsat, get_version_string


def source_yes(source):
    w = source['weights']
    return any(2*sum(a for a,b in zip(w,bits) if b) == sum(w)
               for bits in product((0,1), repeat=len(w)))


def source_witness(source, witness):
    bits = witness['selected']
    return len(bits) == len(source['weights']) and all(type(b) is int and b in (0,1) for b in bits) and 2*sum(w*b for w,b in zip(source['weights'],bits)) == sum(source['weights'])


def legal(target):
    assert type(target['bound']) is int and target['bound'] >= 0
    assert target['jobs']
    for job in target['jobs']:
        assert job
        mandatory = []
        for op in job:
            assert set(op) in ({'1'},{'2'},{'3'},{'1','2'},{'2','3'})
            assert all(type(t) is int and t > 0 for t in op.values())
            if len(op) == 1:
                mandatory.append(int(next(iter(op))))
        assert mandatory == [1,2,3]


def valid_witness(target, witness):
    rows = witness['assignment']
    if len(rows) != len(target['jobs']):
        return False
    departures = [0,0,0]
    for ops, assignment in zip(target['jobs'], rows):
        if len(ops) != len(assignment) or any(type(k) is not int for k in assignment):
            return False
        if assignment != sorted(assignment) or any(str(k) not in op for op,k in zip(ops,assignment)):
            return False
        times = [sum(op[str(k)] for op,k in zip(ops,assignment) if k == m) for m in (1,2,3)]
        first = max(departures[0]+times[0],departures[1])
        second = max(first+times[1],departures[2])
        departures = [first,second,second+times[2]]
    return departures[2] <= target['bound']


def solve(target, limit):
    legal(target)
    solver = Solver()
    choices, starts, times = [], [], []
    for j,job in enumerate(target['jobs']):
        row = [Int(f'a{j}_{i}') for i in range(len(job))]
        for i,op in enumerate(job):
            solver.add(Or(*[row[i] == int(k) for k in op]))
            if i:
                solver.add(row[i-1] <= row[i])
        choices.append(row)
        starts.append([Int(f's{j}_{k}') for k in range(3)])
        times.append([Sum([If(row[i] == k,op[str(k)],0) for i,op in enumerate(job) if str(k) in op]) for k in (1,2,3)])
    for j in range(len(starts)):
        for k in range(3):
            solver.add(starts[j][k] >= 0)
            if k:
                solver.add(starts[j][k] >= starts[j][k-1]+times[j][k-1])
            if j:
                solver.add(starts[j][k] >= starts[j-1][k]+times[j-1][k])
                if k < 2:
                    solver.add(starts[j][k] >= starts[j-1][k+1])
    solver.add(starts[-1][2]+times[-1][2] <= target['bound'])
    found = []
    while len(found) < limit:
        result = solver.check()
        assert result in (sat,unsat), str(result)
        if result == unsat:
            return found, True
        model = solver.model()
        values = [[model.eval(a).as_long() for a in row] for row in choices]
        witness = {'assignment':values}
        assert valid_witness(target,witness)
        found.append(witness)
        solver.add(Or(*[a != v for row,vals in zip(choices,values) for a,v in zip(row,vals)]))
    return found, False


def invoke(candidate, payload, extract=False):
    result = subprocess.run([sys.executable,str(candidate)]+(['--extract'] if extract else []), input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def self_test(cases):
    fixture = {'jobs':[[{'1':1},{'2':1},{'3':1}]],'bound':3}
    witnesses, complete = solve(fixture,2)
    assert len(witnesses) == 1 and complete
    assert not valid_witness(fixture,{'assignment':[[1,1,3]]})
    fixture['bound'] = 2
    assert solve(fixture,2) == ([],True)
    assert source_yes({'weights':[1,1]}) and not source_yes({'weights':[1,2]})
    assert not source_witness({'weights':[1,1]},{'selected':[0,0]})
    try:
        legal({'jobs':[[{'1':0},{'2':1},{'3':1}]],'bound':3})
    except AssertionError:
        pass
    else:
        raise AssertionError('Malformed target accepted')
    # Deliberately wrong target decision for a YES source is detected.
    assert bool(solve(fixture,2)[0]) != source_yes({'weights':[1,1]})
    for case in cases:
        assert source_yes(case['source']) == case['yes']
    print(json.dumps({'self_test':'pass','cases':len(cases),'z3':get_version_string()}))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate',type=Path)
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    if args.self_test:
        self_test(cases)
    if args.candidate:
        recovered = 0
        exhaustive = 0
        for case in cases:
            source = case['source']
            target = invoke(args.candidate,source)
            witnesses, complete = solve(target,32)
            assert bool(witnesses) == source_yes(source), (source,target)
            exhaustive += complete
            for witness in witnesses:
                answer = invoke(args.candidate,{'source':source,'target_solution':witness},True)
                assert source_witness(source,answer), (source,witness,answer)
                recovered += 1
        print(json.dumps({'instances':len(cases),'recovered':recovered,'assignment_enumerations_complete':exhaustive}))


if __name__ == '__main__':
    main()
