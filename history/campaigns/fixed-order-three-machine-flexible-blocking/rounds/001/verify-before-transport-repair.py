"""Independent exhaustive operation-assignment and precedence-path check."""
import argparse
from itertools import product
import json
from pathlib import Path
import subprocess
import sys


def run(path,data,extract=False):
    result = subprocess.run([sys.executable,str(path)]+(['--extract'] if extract else []),input=json.dumps(data),text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def assignments(job):
    for values in product(*[tuple(map(int,op)) for op in job]):
        if all(a <= b for a,b in zip(values,values[1:])):
            yield values


def finish(jobs,choices):
    times = [[sum(op[str(m)] for op,k in zip(job,row) if k == m) for m in (1,2,3)] for job,row in zip(jobs,choices)]
    starts = [[0]*3 for _ in jobs]
    for j in range(len(jobs)):
        for k in range(3):
            lower = [0]
            if k:
                lower.append(starts[j][k-1]+times[j][k-1])
            if j:
                lower.append(starts[j-1][k]+times[j-1][k])
                if k < 2:
                    lower.append(starts[j-1][k+1])
            starts[j][k] = max(lower)
    return starts[-1][-1]+times[-1][-1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate',type=Path,required=True)
    path = parser.parse_args().candidate
    instances = examined = recovered = 0
    for n in range(1,4):
        for weights in product(range(1,4),repeat=n):
            source = {'weights':weights}
            target = run(path,source)
            assert type(target['bound']) is int and target['bound'] >= 0
            for job in target['jobs']:
                assert [next(iter(op)) for op in job if len(op)==1] == ['1','2','3']
                for op in job:
                    assert set(op) in ({'1'},{'2'},{'3'},{'1','2'},{'2','3'})
                    assert all(type(t) is int and t>0 for t in op.values())
            yes = False
            for rows in product(*[list(assignments(job)) for job in target['jobs']]):
                examined += 1
                if finish(target['jobs'],rows) > target['bound']:
                    continue
                yes = True
                answer = run(path,{'source':source,'target_solution':{'assignment':rows}},True)
                bits = answer['selected']
                assert len(bits)==n and all(type(b) is int and b in (0,1) for b in bits)
                assert sum(w*(2*b-1) for w,b in zip(weights,bits)) == 0
                recovered += 1
            source_yes = any(sum(w*s for w,s in zip(weights,signs))==0 for signs in product((-1,1),repeat=n))
            assert yes == source_yes, weights
            instances += 1
    for malformed in ({},{'weights':[]},{'weights':[0]},{'weights':[True]},{'weights':[-1]},[]):
        target = run(path,malformed)
        assert not any(finish(target['jobs'],rows)<=target['bound'] for rows in product(*[list(assignments(job)) for job in target['jobs']]))
    print(json.dumps({'instances':instances,'target_assignments':examined,'recovered':recovered,'malformed_source_cases':6}))


if __name__ == '__main__':
    main()
