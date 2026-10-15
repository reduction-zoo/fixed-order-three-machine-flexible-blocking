"""Finite oracle comparison and valid-operation timing-tradeoff search."""

from itertools import product
import json
from z3 import Int, Solver, sat, unsat


def step(state, processing):
    d1, d2, d3 = state
    a, b, c = processing
    e1 = max(d1 + a, d2)
    e2 = max(e1 + b, d3)
    return e1, e2, e2 + c


def departures(jobs):
    state = (0, 0, 0)
    for job in jobs:
        state = step(state, job)
    return state


def oracle_check(jobs):
    starts = [[Int(f"s_{j}_{k}") for k in range(3)] for j in range(len(jobs))]
    solver = Solver()
    for j, times in enumerate(jobs):
        for k in range(3):
            solver.add(starts[j][k] >= 0)
            if k:
                solver.add(starts[j][k] >= starts[j][k-1] + times[k-1])
            if j:
                solver.add(starts[j][k] >= starts[j-1][k] + jobs[j-1][k])
                if k < 2:
                    solver.add(starts[j][k] >= starts[j-1][k+1])
    finish = starts[-1][2] + jobs[-1][2]
    expected = departures(jobs)[2]
    solver.push()
    solver.add(finish <= expected)
    assert solver.check() == sat
    solver.pop()
    solver.add(finish < expected)
    assert solver.check() == unsat


def main():
    triples = list(product((1, 2), repeat=3))
    checks = 0
    for length in range(1, 4):
        for jobs in product(triples, repeat=length):
            oracle_check(jobs)
            checks += 1

    largest_front = 0
    suffix_example = None
    for a, x, y, b, c in product(range(1, 4), repeat=5):
        # Four operations: mandatory M1, flexible M1/M2, mandatory M2, mandatory M3.
        modes = ((a+x, b, c), (a, b+y, c))
        states = {(0, 0, 0): ()}
        for length in range(1, 7):
            expanded = {step(s, p): path + (choice,)
                        for s, path in states.items() for choice, p in enumerate(modes)}
            states = {s: path for s, path in expanded.items()
                      if not any(t != s and all(u <= v for u, v in zip(t, s))
                                 for t in expanded)}
            largest_front = max(largest_front, len(states))
            best = min(s[2] for s in states)
            prefix_best = [s for s in states if s[2] == best]
            if suffix_example is None:
                for suffix in product(range(1, 5), repeat=3):
                    restricted = min(step(s, suffix)[2] for s in prefix_best)
                    winner = min(states, key=lambda s: step(s, suffix)[2])
                    optimum = step(winner, suffix)[2]
                    if optimum < restricted:
                        suffix_example = {"operation_times": [a,x,y,b,c], "modes": modes,
                                          "prefix_length": length, "prefix_best": prefix_best,
                                          "other_state": winner, "other_choices": states[winner],
                                          "suffix": suffix, "restricted_finish": restricted,
                                          "optimal_finish": optimum}
                        break
    print(json.dumps({"oracle_instances": checks, "solver_queries": 2*checks,
                      "flexible_profiles": 243, "prefix_lengths": [1,6],
                      "maximum_pareto_front": largest_front,
                      "suffix_counterexample": suffix_example}, indent=2))


if __name__ == "__main__":
    main()
