---
status: ready-for-attempt
openness: supported-within-coverage
difficulty: moderate
importance: moderate
tags: [scheduling, blocking, fixed-order, partition, karp]
last-literature-check: 2026-09-16
---

# Fixed-order three-machine flexible blocking scheduling

Prove NP-hardness by a deterministic Karp reduction from positive-integer
Partition, with polynomial recovery of a partition from every feasible target
assignment. Target instances specify three ordered machines, a fixed job order,
positive integer operation durations, and an integer makespan bound. Each job
visits every machine through a mandatory operation and may have flexible
operations between consecutive machines. Assignments preserve operation order;
there is no preemption, overtaking, or intermediate storage. The output must
have polynomial binary encoding size. A negative or partial result is useful
evidence but does not fulfill the requested positive reduction.

Nicosia et al., [Computers & Operations Research 184 (2025), 107219](https://doi.org/10.1016/j.cor.2025.107219),
Table 3 and the conclusion, explicitly leave this fixed-order three-machine case
open. The two-machine fixed-order version is polynomial; variable-order blocking
hardness and preemptive flexibility hardness have different premises.
The [screening record](../../research/evidence/fixed-order-three-machine-flexible-blocking.md)
contains exact definitions, source locations, dated queries, failed restricted
families, the candidate proof, and executable evidence. The 2026-09-16 follow-up
queries were `"fixed" "three" "blocking" "inter-stage" complexity Partition`,
`"FIXB" "Partition"`, and `"fixed sequence" "blocking" "flexibility" NP-hard three machines`.
They identified no matching later resolution; unpublished or overlooked work
remains outside the coverage. No claim of exhaustive novelty is made.

The candidate uses one primer, one five-operation job per weight, and one suffix.
A large middle-machine cost excludes one of four assignment modes. The suffix
then bounds both accumulated groups, excluding the mode that counts a weight
twice. Assignment bits directly recover the partition. The proof and 69,904
finite assignment checks support further work; formal operation-level tests and
independent review remain necessary.

| Gate | Decision | Evidence |
|---|---|---|
| Precise question | Pass | Fixed integer languages, threshold, finite assignment witnesses and explicit decoding route |
| Applicable results | Pass | Fixed-order, nonpreemptive, three-machine premises differ from the inspected known hardness cases |
| Supported openness | Pass | Explicit 2025 table and conclusion; bounded follow-up searches above |
| Significance | Pass | Settles a named fixed-order assignment complexity boundary |
| Proof route | Pass | Explicit forward construction, all-mode soundness argument and direct recovery |
| Initial investigation | Pass | 340 source instances, 69,904 target assignments, 36 independent-model checks; evidence linked above |

Difficulty is moderate: the arithmetic mechanism is now explicit, but subtle
blocking semantics and arbitrary-witness soundness require auditing. Importance
is moderate: this resolves a specific published boundary, not general scheduling
complexity. Both assessments are provisional and may change after review.

Campaign: `campaigns/fixed-order-three-machine-flexible-blocking`, with the active
40-round authorization. Screening probes are not retroactively counted as rounds.
The first formal round will implement and audit the screened construction after
preparation. No production integration or publication is authorized by this card.
