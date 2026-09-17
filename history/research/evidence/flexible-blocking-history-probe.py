"""Seek a suffix reversal after the same fixed final job in both histories."""

from itertools import product
import json
from pathlib import Path
from runpy import run_path

probe = run_path(str(Path(__file__).with_name("flexible-blocking-probe.py")))
departures, step, oracle_check = (probe[name] for name in ("departures", "step", "oracle_check"))


def modes(profile):
    a, x, y, b, c = profile
    return (a+x, b, c), (a, b+y, c)


def main():
    profiles = list(product(range(1, 3), repeat=5))
    prefixes = 0
    for first, second in product(profiles, repeat=2):
        for fixed in product(range(1, 4), repeat=3):
            prefixes += 1
            choices = list(product(modes(first), modes(second)))
            states = [departures([*jobs, fixed]) for jobs in choices]
            best = min(s[2] for s in states)
            for suffix in product(range(1, 5), repeat=3):
                restricted = min(step(s, suffix)[2] for s in states if s[2] == best)
                winner = min(range(4), key=lambda i: step(states[i], suffix)[2])
                optimal = step(states[winner], suffix)[2]
                if optimal < restricted:
                    for jobs in choices:
                        oracle_check([*jobs, fixed])
                        oracle_check([*jobs, fixed, suffix])
                    print(json.dumps({"prefixes_examined": prefixes,
                                      "profiles": [first,second], "fixed_last_job": fixed,
                                      "states": states, "choice_pairs": choices,
                                      "suffix": suffix, "restricted_finish": restricted,
                                      "optimal_finish": optimal, "winning_choice_index": winner,
                                      "oracle_instances": 8, "solver_queries": 16}, indent=2))
                    return
    print(json.dumps({"prefixes_examined": prefixes, "counterexample": None}))


if __name__ == "__main__":
    main()
