# Testing foundation

The prepared checker reads operation-level inputs. It uses Z3 integer assignment
variables, monotone within-job machine choices, and start-time inequalities for
precedence, machine processing, and blocking. Positive operation times and a
mandatory visit to every machine justify aggregating consecutive operations
assigned to one machine. Integer start times suffice because, for fixed choices,
the earliest feasible starts are longest-path sums of integer durations.

The oracle enumerates distinct assignment lists, not schedules, by blocking
only assignment variables. SAT witnesses are separately validated using an
exact earliest-departure recurrence. UNSAT is accepted only from Z3's conclusive
status; unknown and execution errors fail. This is separate modeling by the
main author, not independent review.

The source oracle exhausts all subsets. Cases include odd totals, equal and
unequal weights, multiple partitions, and 100-bit magnitudes. Self-tests cover
hand-checkable feasible/infeasible targets, an invalid assignment, malformed
positive-duration data, wrong recovery, and a deliberately mismatched target
decision. They do not claim an end-to-end faulty subprocess fixture test.

Command: `python3 work/check.py --self-test` from the campaign directory.
Result: [self-test.json](evidence/preparation/self-test.json). The unchanged
screening evidence remains linked from the question; it is not a substitute
for checking the actual candidate output.
