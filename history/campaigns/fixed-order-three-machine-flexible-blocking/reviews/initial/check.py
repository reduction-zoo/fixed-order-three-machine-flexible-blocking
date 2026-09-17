"""Independent operation-start constraints and integer transport probes."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
from z3 import Int, Solver, sat, unsat

CANDIDATE = Path(__file__).resolve().parents[2] / 'work/algorithm.py'

def invoke(text, extract=False):
    return subprocess.run([sys.executable, str(CANDIDATE)] + (['--extract'] if extract else []),
                          input=text, text=True, capture_output=True)

def feasible(target, rows):
    solver = Solver()
    starts = [[Int(f's_{j}_{k}') for k in range(len(job))]
              for j, job in enumerate(target['jobs'])]
    for j, (job, row) in enumerate(zip(target['jobs'], rows)):
        for k, op in enumerate(job):
            solver.add(starts[j][k] >= 0)
            if k:
                solver.add(starts[j][k] >= starts[j][k-1] + job[k-1][str(row[k-1])])
        if j:
            previous = rows[j-1]
            for machine in (1, 2, 3):
                first = row.index(machine)
                last_previous = max(k for k, m in enumerate(previous) if m == machine)
                if machine < 3:
                    release = starts[j-1][last_previous+1]
                else:
                    release = starts[j-1][last_previous] + target['jobs'][j-1][last_previous]['3']
                solver.add(starts[j][first] >= release)
    solver.add(starts[-1][-1] + target['jobs'][-1][-1]['3'] <= target['bound'])
    status = solver.check()
    assert status in (sat, unsat)
    return status == sat

cases = [[1], [1, 1], [1, 2], [1, 2, 3], [1, 1, 1, 3],
         [2**100, 2**100 + 1], [2**100, 2**100, 1, 1]]
assignments = recovered = 0
for weights in cases:
    source = {'weights': weights}
    result = invoke(json.dumps(source))
    assert result.returncode == 0, result.stderr
    target = json.loads(result.stdout)
    found = False
    choices = [[r for r in itertools.product(*[list(map(int, op)) for op in job])
                if list(r) == sorted(r)] for job in target['jobs']]
    for rows in itertools.product(*choices):
        assignments += 1
        if not feasible(target, rows):
            continue
        found = True
        result = invoke(json.dumps({'source': source, 'target_solution': {'assignment': rows}}), True)
        assert result.returncode == 0, result.stderr
        bits = json.loads(result.stdout)['selected']
        assert len(bits) == len(weights) and all(type(b) is int and b in (0, 1) for b in bits)
        assert sum(w*b for w, b in zip(weights, bits))*2 == sum(weights)
        recovered += 1
    expected = any(sum(w*b for w, b in zip(weights, bits))*2 == sum(weights)
                   for bits in itertools.product((0, 1), repeat=len(weights)))
    assert found == expected, weights

probes = []
for label, number in [('parse', '1'+'0'*4300), ('serialize', '9'*4300)]:
    text = '{"weights":['+number+','+number+']}'
    result = invoke(text)
    probes.append({'stage': label, 'decimal_digits': len(number), 'exit': result.returncode,
                   'error': next((line for line in result.stderr.splitlines() if line.startswith('ValueError:')), '')})
number = '1'+'0'*4300
text = '{"source":{"weights":['+number+','+number+']},"target_solution":{"assignment":[[1,2,3],[1,1,2,2,3],[1,2,2,3,3],[1,2,3]]}}'
result = invoke(text, True)
probes.append({'stage': 'recovery_parse', 'decimal_digits': len(number), 'exit': result.returncode,
               'error': next((line for line in result.stderr.splitlines() if line.startswith('ValueError:')), '')})
print(json.dumps({'python': sys.version, 'sources': len(cases), 'assignments': assignments,
                  'recovered': recovered, 'integer_transport_probes': probes}, indent=2))
