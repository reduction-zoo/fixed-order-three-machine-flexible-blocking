# Reading two cumulative loads in a blocking flow shop

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
[proof](../../campaigns/fixed-order-three-machine-flexible-blocking/work/proof.md), with positive mathematical assessment in the
[initial independent review](../../campaigns/fixed-order-three-machine-flexible-blocking/reviews/initial/review.md). Executable
transport repair received an independent advance review. Finite tests supplement the proof.

**Consequence for search.** When a scheduling reduction needs equality of two
chosen loads, track both in an exact recurrence and construct a suffix that
bounds their maximum. Check every local assignment mode; duplicated weights
can be ruled out by positivity only after proving both bounds. Merely tuning
large penalties does not establish either property.

**Use history.** No subsequent campaign use. Extracted 2026-09-16 from this
round; transferred after campaign closure on 2026-09-16 under the ongoing research authorization.

