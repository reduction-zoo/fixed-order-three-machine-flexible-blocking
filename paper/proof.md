# Partition to fixed-order three-machine flexible blocking scheduling

## Statement and encodings

The languages and witnesses are fixed in contract.md. Positive-integer Partition
is NP-complete. The target is NP-complete, with hardness already for jobs having
at most five operations and at most one flexible operation per adjacent machine
pair. The complete rule received an independent advance review; novelty is supported
within the dated coverage in reviews/initial/review.md. Expert assessment remains
outstanding. It concerns weak NP-hardness, not strong NP-hardness.

## Earliest schedules

Fix all assignments and sum consecutive operations on each machine into a
processing triple (a,b,c). There is no advantage to internal idle time between
these operations. If the preceding job's machine departures are (d1,d2,d3),
the next departures are

    e1=max(d1+a,d2), e2=max(e1+b,d3), e3=e2+c.

The next job may begin on machine one at d1; it may transfer only when its own
processing and downstream occupancy permit. Induction gives the formula and
its feasibility. All three updates are monotone in previous departures, so no
later start can improve the final makespan. Start from (0,0,0). This also proves
NP membership: assignment lists are polynomial-size certificates and exact
integer evaluation takes polynomial bit complexity. Arbitrary legal schedules
with that assignment cannot beat the computed earliest schedule.

## Construction

For weights w1,...,wn>0 let W=sum(wi), L=4W+4, C=6W+6, G=5W+5. The job order is
one primer (1,G,C), then one item job for each weight in input order, then one
suffix (G+C-1,1,1). Primer and suffix operations are all mandatory. Each item has
five operations in this order:

1. M1 only, duration C.
2. M1 duration wi or M2 duration L.
3. M2 only, duration 1.
4. M2 duration L or M3 duration wi.
5. M3 only, duration C.

Let i=1 indicate operation 2 uses M1 and j=1 indicate operation 4 uses M2.
All four choices preserve operation order and yield:

| (i,j) | M1 | M2 | M3 |
|---|---|---|---|
| (0,0) | C | 1+L | C+wi |
| (0,1) | C | 1+2L | C |
| (1,0) | C+wi | 1 | C+wi |
| (1,1) | C+wi | 1+L | C |

Set H=2+G+(n+1)C+floor(W/2). The instance is legal for every source, including
NO instances. Invalid source encodings map to three unit mandatory operations
and bound zero, a fixed legal NO instance.

## Exclusion of mode (0,1)

Write x_t for the second-machine departure of item t, x_0=1+G for the primer,
and c_t for the third-machine duration of item t, with c_0=C. Always
x_t >= x_{t-1}+c_{t-1}. Define the nonnegative excess over this increment as
Delta_t. If item t uses (0,1), its first departure is at least x_{t-1}, so
x_t >= x_{t-1}+1+2L. Since c_{t-1} <= C+W,

    Delta_t >= 1+2L-(C+W)=W+3.

Thus the final item departs M3 at least 1+G+(n+1)C+W+3. The suffix takes at least
one more unit on M3, so the bound H cannot hold. This applies even if several
items use (0,1); all other excesses remain nonnegative.

## Exact two-sum identity for the remaining modes

For each item define alpha_t=wt if i=1, otherwise zero, and beta_t=wt if j=0,
otherwise zero. For modes (0,0),(1,0),(1,1), processing is
(C+alpha_t,b_t,C+beta_t), with b_t<=L+1. Let beta_0=0.

Inductively, immediately after item t,

    d1_t=1+tC+sum_{h<=t} alpha_h,
    d2_t=1+G+tC+sum_{h<t} beta_h.

At t=0 these expressions are the primer departures. The previous gap satisfies
G-W <= d2_{t-1}-d1_{t-1} <= G+W=C-1. Hence the first max chooses
 d1_t=d1_{t-1}+C+alpha_t.
The proposed d2_t=d2_{t-1}+C+beta_{t-1} has gap from d1_t equal to
G+sum_{h<t} beta_h-sum_{h<=t} alpha_h. Each sum lies in [0,W], so this gap
is at least G-W=L+1>=b_t. Therefore the second max chooses precisely the
proposed d2_t. This proves both formulas without assuming the max branches.

Let A=sum alpha_t and B=sum beta_t. After the final item,

    d1_n=1+nC+A, d3_n=1+G+(n+1)C+B.

For suffix duration a=G+C-1, b=c=1, its second departure is
max(d1_n+G+C,d2_n+1,d3_n). Since d3_n=d2_n+c_n and c_n>=1, the middle term is
redundant. Its final completion is exactly

    2+G+(n+1)C+max(A,B).

## Equivalence and arbitrary-witness recovery

A partition chooses mode (1,1) for selected weights and (0,0) for the others.
Then A=B=W/2 and the resulting schedule meets H.

Conversely, a feasible assignment contains no (0,1). For its remaining modes,
A+B=W plus the total weight of (1,0) items. Meeting H implies both A and B are
at most floor(W/2). For odd W this is impossible. For even W positivity of all
weights forces no (1,0), and A=B=W/2. The extractor reads whether operation 2
of each item uses M1. This selects exactly the (1,1) items, recovering a valid
partition from every feasible assignment, without requiring optimality or a
preferred solver output. The primer and suffix offer no choices.

## Bit bounds and totality

For source bit length N, n<=N and log(W+1)=O(N). All durations are O(W), H=O(nW),
and there are 5n+6 operations. Thus output length is O(N²). Schoolbook integer
arithmetic and output serialization give a conservative O(N³) forward bit-time
bound. Source validity checking is polynomial. Recovery reads n assignment
entries and returns n bits; parsing and indexing can be bounded by O((N+Y)²)
for encoded target-witness length Y. No solver, randomness, retained subprocess
state, or source search is used by either map.

## Novelty, significance, and limitations

Nicosia et al., Computers & Operations Research 184 (2025), 107219, Table 3 and
conclusion, explicitly leave three machines with fixed job order open:
https://doi.org/10.1016/j.cor.2025.107219 . Their two-machine algorithm has
matching nonpreemptive blocking semantics. Their Section 2 permits jobs with
varying operation counts and says the simplifying common-pattern assumption
is not required by their models or algorithms. Our target uses that general
model; no identical-operation-pattern theorem is claimed.

The screened queries and differing known hypotheses are recorded in question.md
and its linked evidence. No matching subsequent classification was found within
that coverage. This is not exhaustive novelty verification. Significance is
settling this specific named boundary. Independent expert assessment remains
necessary; no publication or acceptance is claimed.
