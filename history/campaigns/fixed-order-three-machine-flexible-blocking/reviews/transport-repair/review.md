# Focused independent review — transport repair

Decision: **advance**. Review date: 2026-09-16.

The two initial repair requirements are resolved. This decision incorporates
the mathematical, novelty and significance audit in
[the initial review](../initial/review.md), including its explicit coverage
limitations and general-model scope. It means eligible for expert review,
not publication acceptance.

## Correctness

I inspected the current algorithm, contract, verification report, updated
verification code, both post-repair logs, and the diff against the preserved
pre-repair algorithm. The forward arithmetic, operation construction, threshold,
and recovery logic are unchanged. The earlier general proof audit and 628
independent operation-assignment checks therefore remain applicable.

algorithm.py now calls `sys.set_int_max_str_digits(0)` before parsing or
serialization in either mode. Both previously failing large-integer paths
are fixed. Forward mode catches malformed JSON and invalid text decoding and
passes them to the existing fixed-NO construction; extraction retains explicit
failure for malformed payloads. contract.md now states these different mode
requirements consistently. No claim of successful recovery from an invalid
target witness is needed by the rule.

The integer conversion change removes a fixed representation ceiling; it does
not alter the algorithm's polynomial binary-size or runtime analysis. Decimal
and binary integer encodings have lengths within a constant factor. Construction
and recovery remain deterministic, without a solver or persistent state.

## Focused independent evidence

I wrote and executed [check.py](check.py), without importing the candidate or
either author-written checker. Output is preserved in
[check-result.json](check-result.json). From the campaign directory, reproduce
with `python3 reviews/transport-repair/check.py`.

The check passed:

* Exact forward outputs for equal-weight YES instances with weights 10^4300,
  10^4300-1, and 10^6000+17, covering input parsing and expanded output durations.
* Both complementary partition assignments for each source, with six successful
  fresh-process recoveries. Their feasibility follows from the unchanged general
  proof already audited; this focused check does not claim new scheduling coverage.
* Eight malformed source inputs mapping to the fixed legal NO target, including
  invalid UTF-8, invalid JSON, nested malformed input, a deeply nested decoded
  non-source value, null weights and Boolean weights.
* Three malformed extraction inputs and an invalid CLI option exiting nonzero.

The author-written post-repair logs report the prepared suite's 10 sources and
14 recoveries, and the separate suite's 39 sources, 1,884 assignments, 24
recoveries, six malformed decoded objects, three malformed JSON inputs and two
large-integer recoveries. I inspected and reused those results rather than
duplicating the full suites. Finite tests do not replace the general proof.

## Novelty and significance

Both judgments remain supported within the initial review's dated literature
coverage. The transport-only change creates no new theorem or model assumption.
The contribution remains weak NP-hardness of fixed-order three-machine flexible
blocking scheduling in the general model permitting varying operation patterns,
with polynomial recovery from every feasible target assignment. The stronger
identical-operation-pattern variant is not proved. Uninspected full literature
proofs, unindexed work and unpublished results remain explicit novelty limits.

No remaining correctness or implementation blocker was found in this focused
review. The unchanged construction may proceed to the research-write stage and
its required manuscript verification.
