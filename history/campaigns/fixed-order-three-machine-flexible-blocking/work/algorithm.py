"""Deterministic Partition reduction and witness recovery."""
import json
import sys

sys.set_int_max_str_digits(0)


def forward(source):
    weights = source.get('weights') if isinstance(source,dict) else None
    if not isinstance(weights,list) or not weights or any(type(w) is not int or w <= 0 for w in weights):
        return {'jobs':[[{'1':1},{'2':1},{'3':1}]],'bound':0}
    total = sum(weights)
    middle, base, gap = 4*total+4, 6*total+6, 5*total+5
    jobs = [[{'1':1},{'2':gap},{'3':base}]]
    for w in weights:
        jobs.append([{'1':base},{'1':w,'2':middle},{'2':1},
                     {'2':middle,'3':w},{'3':base}])
    jobs.append([{'1':gap+base-1},{'2':1},{'3':1}])
    return {'jobs':jobs,'bound':2+gap+(len(weights)+1)*base+total//2}


def recover(payload):
    n = len(payload['source']['weights'])
    rows = payload['target_solution']['assignment']
    return {'selected':[int(rows[i+1][1] == 1) for i in range(n)]}


if __name__ == '__main__':
    if sys.argv[1:] == ['--extract']:
        result = recover(json.load(sys.stdin))
    elif not sys.argv[1:]:
        try:
            data = json.load(sys.stdin)
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = None
        result = forward(data)
    else:
        raise ValueError('Expected no arguments or --extract')
    print(json.dumps(result))
