"""Exhaustive finite check of the two-interface Partition construction."""

from itertools import product
import json
from pathlib import Path
from runpy import run_path

probe = run_path(str(Path(__file__).with_name("flexible-blocking-probe.py")))
departures, oracle_check = (probe[name] for name in ("departures", "oracle_check"))


def construction(weights):
    total = sum(weights)
    middle = 4*total+4
    base = 6*total+6
    gap = 5*total+5
    first = (1, gap, base)
    last = (gap+base-1, 1, 1)
    modes = [[(base, 1+middle, base+w),
              (base, 1+2*middle, base),
              (base+w, 1, base+w),
              (base+w, 1+middle, base)] for w in weights]
    bound = 2+gap+(len(weights)+1)*base+total//2
    return first, modes, last, bound


def main():
    instances = assignments = recovered = 0
    for n in range(1, 5):
        for weights in product(range(1, 5), repeat=n):
            first, modes, last, bound = construction(weights)
            source_yes = any(2*sum(w for w,s in zip(weights,bits) if s) == sum(weights)
                             for bits in product((0,1), repeat=n))
            target_yes = False
            for choices in product(range(4), repeat=n):
                jobs = [first] + [modes[i][c] for i,c in enumerate(choices)] + [last]
                feasible = departures(jobs)[2] <= bound
                if 1 not in choices:
                    left = sum(w for w,c in zip(weights,choices) if c in (2,3))
                    right = sum(w for w,c in zip(weights,choices) if c in (0,2))
                    constant = bound - sum(weights)//2
                    assert departures(jobs)[2] == constant + max(left,right)
                else:
                    assert not feasible
                if feasible:
                    assert set(choices) <= {0,3}
                    assert 2*sum(w for w,c in zip(weights,choices) if c == 3) == sum(weights)
                    target_yes = True
                    recovered += 1
                assignments += 1
            assert source_yes == target_yes
            instances += 1
    oracle_instances = 0
    for weights in ((1,), (1,1), (1,2)):
        first, modes, last, bound = construction(weights)
        for choices in product(range(4), repeat=len(weights)):
            oracle_check([first] + [modes[i][c] for i,c in enumerate(choices)] + [last])
            oracle_instances += 1
    print(json.dumps({"source_instances": instances, "target_assignments": assignments,
                      "recovered_witnesses": recovered, "oracle_instances": oracle_instances,
                      "solver_queries": 2*oracle_instances}, indent=2))


if __name__ == "__main__":
    main()
