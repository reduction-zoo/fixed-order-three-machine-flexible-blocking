"""Bounded search with one flexible operation at each machine interface."""

from itertools import product
import json
from pathlib import Path
from runpy import run_path

probe = run_path(str(Path(__file__).with_name("flexible-blocking-probe.py")))
step, oracle_check = (probe[name] for name in ("step", "oracle_check"))


def main():
    largest_front = 0
    trials = 0
    example = None
    for profile in product((1, 2), repeat=7):
        a, x, y, b, u, v, c = profile
        modes = [(a+x*i, b+y*(1-i)+u*j, c+v*(1-j))
                 for i, j in product((0, 1), repeat=2)]
        states = {(0, 0, 0): ()}
        for length in range(1, 7):
            expanded = {step(s, p): path+(choice,) for s, path in states.items()
                        for choice, p in enumerate(modes)}
            states = {s: path for s, path in expanded.items()
                      if not any(t != s and all(a <= b for a, b in zip(t, s))
                                 for t in expanded)}
            largest_front = max(largest_front, len(states))
            if example is not None:
                continue
            for fixed in product(range(1, 5), repeat=3):
                after = {step(s, fixed): path for s, path in states.items()}
                best = min(s[2] for s in after)
                for suffix in product(range(1, 5), repeat=3):
                    trials += 1
                    restricted = min(step(s, suffix)[2] for s in after if s[2] == best)
                    winner = min(after, key=lambda s: step(s, suffix)[2])
                    if step(winner, suffix)[2] < restricted:
                        for path in after.values():
                            jobs = [modes[i] for i in path] + [fixed, suffix]
                            oracle_check(jobs)
                        example = {"profile": profile, "modes": modes, "length": length,
                                   "fixed": fixed, "states_and_paths": list(after.items()),
                                   "suffix": suffix, "winner": winner,
                                   "restricted_finish": restricted,
                                   "optimal_finish": step(winner, suffix)[2],
                                   "oracle_instances": len(after)}
                        break
                if example is not None:
                    break
    print(json.dumps({"profiles": 128, "lengths": [1,6],
                      "maximum_pareto_front": largest_front,
                      "suffix_trials": trials, "example": example}, indent=2))


if __name__ == "__main__":
    main()
