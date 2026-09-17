# Round 001 — Operation-level two-interface construction

## Plan

Implement the screened Partition construction and its extractor under the
prepared JSON contract. This is the first formal round, not a retrospective
renumbering of screening. Budget: 40 rounds. Preserve the two-counter timing
invariant and exclude all unintended assignment modes.

Scope: prepared ten source cases with up to 32 independently generated target
assignments per case, then a separately implemented finite checker for all
positive weight lists of length at most three and weights at most three.
Check actual subprocess outputs, legal operation lists, YES/NO equivalence,
and recovery from every enumerated feasible assignment. Completion requires
passing checks and a general proof suitable for independent review.

The prior screening supplies the mechanism and exact finite evidence. No shared
experience entry matched the blocking-timing construction in the repository
search; unrelated matrix Schur-complement entries are inapplicable.

## Evidence and diagnosis

One mathematical construction was implemented; no new mathematical route or
coefficient family was introduced during verification. Preparation passed
before implementing the operation-level candidate. The prepared suite covered
10 sources and recovered 14 witnesses. Separate verification covered 39 sources,
1,884 assignments, and 24 recoveries. See [prepared-check.json](prepared-check.json)
and [verification-check.json](verification-check.json).

The [initial independent review](../../reviews/initial/review.md) found the
mathematical proof sound for varying operation patterns and confirmed the
bounded novelty/significance assessment. Its operation-start Z3 model checked
628 assignments from seven sources and recovered ten witnesses. These counts
are separate from author-side tests and must not be summed as disjoint instances.

The reviewer reproduced three legal-input failures caused by Python's default
integer conversion limit, not by a scheduling counterexample. The implementation
now explicitly permits unbounded integer conversion in both directions.
Forward malformed JSON is mapped to the fixed NO target; the contract now
states this behavior. Original implementation, contract, checker and failure
logs are preserved. Both required suites passed after repair, with additional
malformed-JSON and large-integer recovery regressions. See
[prepared-check-after-repair.json](prepared-check-after-repair.json) and
[verification-check-after-repair.json](verification-check-after-repair.json).
The [focused review](../../reviews/transport-repair/review.md) returned advance.
It checked six large-integer recoveries and eight malformed forward inputs.
Runtime repairs are not new research rounds.

The mathematical consequence is an exact two-load identity, not an empirical
fit: excluding the costly middle mode leaves completion equal to a constant
plus the larger of two cumulative weights. Positivity and the total budget
then exclude duplicated weights and force a partition. The arbitrary-witness
argument is in [proof.md](../../work/proof.md). The theorem does not establish
strong hardness or the common-operation-pattern restriction.

Experience extraction: one proposed finding is recorded below, pending transfer
to `research/experience/blocking-two-load-suffix.md`. The active campaign permits
writes only inside this campaign, so no shared entry has been created or updated.
A closure search found no duplicate; the older `one-sided-partition-capacity.md`
concerns a different scheduling model. That entry was inspected retrospectively,
not used to discover this construction. No measured discovery benefit is claimed.

### Proposed reusable finding: blocking two-load suffix

Tags: scheduling, blocking, partition, max-plus, witness-soundness.

**Claim and applicability.** For the three-machine blocking recurrence in
proof.md, a primer with gap G and item durations (C+alpha,b,C+beta) preserves
two partial sums when their total magnitudes are at most W,
G+W<C, and b<=G-W. A suffix (G+C-1,1,1) reads out a constant plus
max(sum alpha,sum beta). In the present construction, L=4W+4, G=5W+5,
C=6W+6; the remaining four-mode obstacle is excluded by an irreversible
middle-machine increment of at least W+3. These premises are essential;
this is not a claim about arbitrary blocking systems or arbitrary flexible jobs.

**Evidence and status.** General lemmas and exact construction in
[proof.md](../../work/proof.md), with positive mathematical assessment in the
[initial independent review](../../reviews/initial/review.md). Executable
transport repair received an independent advance review. Finite tests supplement the proof.

**Consequence for search.** When a scheduling reduction needs equality of two
chosen loads, track both in an exact recurrence and construct a suffix that
bounds their maximum. Check every local assignment mode; duplicated weights
can be ruled out by positivity only after proving both bounds. Merely tuning
large penalties does not establish either property.

**Use history.** No subsequent campaign use. Extracted 2026-09-16 from this
round; shared destination remains pending under the write boundary.

## Next action

Round complete: ready_for_expert_review. The unchanged mathematical construction
has passing author-side suites, an independent advance review, and a manuscript
content audit in [the addendum](../../reviews/transport-repair/manuscript-addendum.md).
The five-page native Typst manuscript includes an exact vector operation diagram,
complete proof, both algorithms, bit bounds, and reproduction instructions.
The final PDF was inspected on every page; equations and their setup paragraphs
remain together, all labels are legible, and no clipping was found. The writing
skill's final language pass preserved the reviewed quantifiers and model limits.

One formal round and one construction route were completed. The latest 20-round
continuation was not exhausted because the current target reached the defined
completion status. No further construction is needed on this fixed question.
The earlier high short-term-prospects judgment was followed by completion of
review and writing; it was not a calibrated probability. Expert novelty and
correctness assessment remain outstanding. Per-round time/token measurements
are unavailable; no synthetic measurements are reported.

Experience closeout: 0 shared entries created, 0 updated, 1 pending under the
campaign-only write boundary, with its complete proposed content above.
