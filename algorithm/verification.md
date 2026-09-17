# Verification coverage

Both suites execute the actual algorithm.py in fresh processes. check.py uses
Z3 choices on the operation lists and start-time inequalities; verify.py enumerates
all legal operation assignments and computes earliest starts from the precedence
and occupancy constraints. Neither imports algorithm.py; verify.py also does
not import check.py. This is program separation, not independent authorship.

Prepared command: `python3 work/check.py --candidate work/algorithm.py`.
Separate command: `python3 work/verify.py --candidate work/algorithm.py`.
Current logs: [prepared](../history/campaigns/fixed-order-three-machine-flexible-blocking/rounds/001/prepared-check-after-repair.json),
[verification](../history/campaigns/fixed-order-three-machine-flexible-blocking/rounds/001/verification-check-after-repair.json).

The prepared suite covers ten sources including 100-bit weights and multiple
partition witnesses. The separate suite exhausts positive weights 1..3 and
lengths 1..3, all legal target assignments, and every feasible extractor input.
Six malformed decoded objects and three malformed JSON strings map to NO.
Two large-integer regressions cover 4,300- and 4,301-digit source weights,
larger constructed durations, and successful witness recovery. The original
review failures and pre-repair files remain in the initial review and round.
No runtime timeout is
used. Finite evidence cannot prove the general theorem; proof.md supplies the
argument to be reviewed.
