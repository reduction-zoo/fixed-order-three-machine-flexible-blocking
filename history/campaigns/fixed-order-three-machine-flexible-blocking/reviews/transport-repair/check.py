"""Focused independent check of transport repairs; no candidate imports."""
import json
from pathlib import Path
import subprocess
import sys

sys.set_int_max_str_digits(0)
candidate = Path(__file__).resolve().parents[2] / 'work/algorithm.py'

def run(raw, extract=False):
    return subprocess.run([sys.executable, str(candidate)] + (['--extract'] if extract else []),
                          input=raw, capture_output=True)

def decode(result):
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)

large = []
for w in (10**4300, 10**4300-1, 10**6000+17):
    source = {'weights': [w, w]}
    target = decode(run(json.dumps(source).encode()))
    W = 2*w
    L, C, G = 4*W+4, 6*W+6, 5*W+5
    assert target == {'jobs': [[{'1':1},{'2':G},{'3':C}],
                              [{'1':C},{'1':w,'2':L},{'2':1},{'2':L,'3':w},{'3':C}],
                              [{'1':C},{'1':w,'2':L},{'2':1},{'2':L,'3':w},{'3':C}],
                              [{'1':G+C-1},{'2':1},{'3':1}]],
                      'bound': 2+G+3*C+w}
    for selected in (0, 1):
        chosen, other = [1,1,2,2,3], [1,2,2,3,3]
        rows = [[1,2,3], chosen if selected else other,
                other if selected else chosen, [1,2,3]]
        payload = {'source':source, 'target_solution':{'assignment':rows}}
        answer = decode(run(json.dumps(payload).encode(), True))
        assert answer == {'selected':[selected,1-selected]}
    large.append({'digits':len(str(w)), 'recovered':2})

malformed = [b'', b'{', b'{"weights":[1,]}', b'\xff', b'['*2000,
             b'['*2000+b'0'+b']'*2000, b'{"weights":[null]}', b'{"weights":[true]}']
for raw in malformed:
    assert decode(run(raw)) == {'jobs':[[{'1':1},{'2':1},{'3':1}]],'bound':0}
for raw in (b'', b'{', b'\xff'):
    assert run(raw, True).returncode != 0
assert subprocess.run([sys.executable,str(candidate),'--unknown'],input=b'{}',capture_output=True).returncode != 0
print(json.dumps({'large_integer_cases':large,'recoveries':6,
                  'malformed_forward_cases':len(malformed),
                  'malformed_extraction_failures':3,'invalid_cli_failure':True},indent=2))
