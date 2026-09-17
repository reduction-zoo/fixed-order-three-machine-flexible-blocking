# Manuscript content audit

Date: 2026-09-16. The advance decision remains applicable to the unchanged
mathematical construction. I inspected work/manuscript.typ and
work/figures/item.typ, comparing their statements with the reviewed proof,
construction, contract and saved verification counts. Visual PDF inspection
is assigned to the main researcher and is not claimed here. No suite rerun was
necessary.

## Content findings

The abstract, introduction and scope section consistently restrict the result
to the general model allowing different operation patterns. The manuscript
explicitly identifies the five-operation items and three-operation boundary
jobs and does not claim a common-pattern theorem or strong NP-hardness.

Theorem 1 states the correct decision language, positive integer encoding,
operation bound and arbitrary-witness recovery. The all-mode table is correct.
Lemma 3 excludes (0,1) without assumptions about other choices, and Lemmas 4
and 5 establish the two cumulative sums and suffix readout for every remaining
mode. The final converse excludes (1,0) using positivity and handles odd total
weight. The recovery implication applies to every feasible assignment, without
requiring an optimal schedule or a particular solver's witness. The earliest
schedule lemma supports this universal implication.

The figure's five operation labels, allowed machines and processing times
match the candidate. Its two illustrated paired choices correctly add the
weight to opposite sums. The caption says the two other modes are excluded
by the proof, rather than pretending they are illegal local choices.

The operation count 5n+6, binary output bound O(N²), forward bit bound O(N³),
and conservative extraction bound agree with the reviewed proof. The appendix
accurately reports 10/14 prepared sources/recoveries; 39 sources, 1,884
assignments and 24 recoveries for exhaustive verification; six malformed
decoded inputs, three malformed JSON strings and two large-integer regressions;
628 assignments and ten recoveries across seven independent sources; and six
focused large-integer recoveries plus eight malformed forward checks. Its
warning that these scopes overlap is correct. Z3 5.1.0 matches the saved
preparation self-test. The displayed extraction example returns [1,0].

## Small precision edits recommended

At the inspected manuscript.typ:162, Lemma 5 says "the final makespan is
exactly" the readout. State "the minimum makespan for the assignment is
exactly", because arbitrary added idle time can increase a schedule's makespan.
At the start of Correctness, explicitly say that departure variables refer to
the earliest schedule of Lemma 2. This also makes Lemma 4's equalities
unambiguous. The underlying proof already uses that schedule correctly.

At manuscript.typ:131, "Every third-machine duration is at least C" should
read "Every primer/item third-machine duration is at least C". The telescoping
sum contains only those jobs; the suffix has third-machine duration 1 and is
added separately in the next sentence. This is a quantifier clarification,
not a gap in the telescoping argument.

These local wording improvements need no change to the algorithm, theorem,
finite checks or earlier novelty assessment. Literature priority remains
subject to the bounded coverage and expert assessment already recorded.

## Confirmation after manuscript edits

I checked the current manuscript after the main researcher applied the three
clarifications. Correctness now explicitly uses the earliest schedule; the
duration lower bound is limited to primer and item jobs; and Lemma 5 states
the minimum makespan for the assignment. All three wording findings are
resolved. No remaining content issue was found in this audit. The advance
decision stands, subject to the main researcher's separate visual PDF QA.
