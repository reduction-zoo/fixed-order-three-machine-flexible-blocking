# Fixed-order three-machine flexible blocking flow shop

Screened 2026-09-16. Hold pending a bounded construction investigation; no
campaign admitted and no formal rounds used.

## Precise prospective target

Input: three ordered machines, an ordered list of jobs, a positive integer
processing time for every allowed operation-machine assignment, and an integer
makespan bound H, all numbers binary encoded. Each job has a listed operation
sequence with one mandatory operation on each machine, in machine order.
Operations between consecutive mandatory operations can use either of those
two machines. Assignment indices must be nondecreasing within a job. Operations
are nonpreemptive. Every machine processes jobs in the supplied order. There
is no buffer: a completed job occupies its machine until it starts on the next.
Ask whether assignments and a feasible schedule finish by H.

An assignment list is a finite witness: its earliest schedule can be computed
exactly, so a schedule need not be supplied separately. The contemplated source
is binary Partition. Its witness is a sign for each input integer. A proposed
construction must encode those choices in operation assignments, prove both
directions, and recover signs from every feasible target assignment. No such
construction is claimed here. Restricting times to integers avoids witness
representation issues; the hardness and novelty implications of this restriction
still need to be checked against the primary model.

## Primary source and exact gap

Nicosia, Pacifici, Pferschy, Russo Russo and Salvatore,
[Flow shop scheduling with inter-stage flexibility and blocking constraints](https://doi.org/10.1016/j.cor.2025.107219),
Computers & Operations Research 184 (2025), 107219, Table 3, lists the fixed-order
three-machine case as open. Its two-machine fixed-order case is polynomial.
The [2024 preprint](https://arxiv.org/html/2411.18381v1), Section 2 and Table 1,
states the operation model and the same gap. Section 3.2, Lemma 1 and Theorem 2,
uses a two-machine no-wait transformation and a shortest-path construction;
the text explicitly explains why that transformation fails for three machines.

The known hardness of three-machine blocking with a variable job order does
not resolve fixed-order assignment. Preemptive two-machine hardness also has
different hypotheses. These are not contradictory classifications of one model.
The original preemptive-paper DOI could not be opened in this check; no transfer
from that proof is assumed.

Queries used: `scheduling "complexity remains open" "2025" two machines`,
`"Flow shop scheduling with inter-stage flexibility and blocking constraints" pdf`,
`"FIXB" "three" "complexity"`,
`"blocking" "fixed sequence" "flexibility" "2026"`, and
`"Flow shop" "inter-stage flexibility" "NP-hard" "three"`.
No matching later classification was identified in this bounded search. This
does not establish exhaustive coverage or prove current openness.

## Initial algebraic route

For a chosen assignment, aggregate each job's processing into a triple
(a,b,c). If the preceding job departs the machines at (d1,d2,d3), the next
job's earliest departures are

    e1 = max(d1+a, d2),
    e2 = max(e1+b, d3),
    e3 = e2+c.

Initialize departures to (0,0,0). To justify earliest optimality, the next job
can start on machine one at d1. Its transfer to machine two needs both its own
processing completion and the previous job's departure from machine two; the
same reasoning applies at the next transfer. Delaying any start cannot improve
these monotone bounds. Consecutive operations on one machine need no internal
idle time, so aggregation is legitimate for a fixed assignment.

There are polynomially many assignment modes per job for three machines: choose
one split position in each of the two flexible operation blocks. An exact
pseudo-polynomial algorithm propagates all departure triples up to H, rejecting
states with final departure greater than H. If Q is the total number of listed
operations, the simple bound O(n Q² (H+1)³) suffices for state transitions,
apart from polynomial-bit arithmetic. This is not polynomial in binary input
size and does not decide the desired hardness question. It does constrain a
prospective proof: unary bounded-horizon instances cannot support strong
NP-hardness unless P=NP.

The candidate mechanism is to encode Partition through nondominated departure
times, then add fixed suffix jobs to test a balance threshold. Its main gap is
whether the max operations retain the required accumulated choices instead of
erasing them. A valid mapping must output real operation lists, not arbitrary
unrelated triples presented as assignment modes.

## Next bounded task

### Two-interface construction found (2026-09-16)

The [two-interface probe](flexible-blocking-two-interface-probe.py) examines
128 five-operation profiles with all seven machine-specific durations in {1,2},
repeated for lengths one through six. Its [output](flexible-blocking-two-interface-probe.json)
records a largest Pareto set of four and a history reversal after a common
fixed job. With modes (1,2,3), (1,3,1), (2,1,3), (2,2,1), appending (1,1,1)
leaves relevant states (3,6,7) and (4,5,6). Appending (3,1,1) finishes at eight
and nine respectively. Both histories passed the start-time oracle. The search
stopped looking for reversals after this example (49,185 suffix trials), while
finishing the declared Pareto-size enumeration.

This led to the following complete candidate construction, not yet independently
reviewed or admitted as a finished research result. Let the positive Partition
weights be w_1,...,w_n, with W their sum. Set

    L = 4W+4, C = 6W+6, G = 5W+5.

Use a fixed primer job (1,G,C), followed by n item jobs in input order, then a
fixed suffix job (G+C-1,1,1). Each item has five ordered operations: mandatory
M1 duration C; a flexible M1/M2 operation with durations w_i and L; mandatory
M2 duration 1; a flexible M2/M3 operation with durations L and w_i; mandatory
M3 duration C. Its four modes are

    00: (C,     1+L,  C+w_i),
    01: (C,     1+2L, C),
    10: (C+w_i, 1,    C+w_i),
    11: (C+w_i, 1+L,  C).

Set the makespan bound to 2+G+(n+1)C+floor(W/2). All times are positive integers,
the output contains 5n+6 operations, and its binary size is polynomial in the
binary source size. The primer and suffix have no flexible operations, as
permitted by the stated target domain.

**Candidate soundness argument.** In every schedule, d2 increases by at least
the previous job's third-machine processing time. A mode 01 item increases
d2 by at least 1+2L, since its first-machine departure cannot precede the previous
second-machine departure. Every preceding third-machine duration is at most
C+W. Thus a mode 01 causes an excess of at least 1+2L-(C+W)=W+3 over the baseline
increment. Later increments cannot erase it. Including the suffix, completion
is then at least 2+G+(n+1)C+W+3, above the bound. This reasoning covers every
assignment containing mode 01, including multiple such modes.

For assignments using only 00,10,11, let A be the sum of weights assigned to
10 or 11, and B the sum assigned to 00 or 10. Inductively the gap d2-d1 remains
between G-W=L+1 and G+W=C-1 throughout the item sequence. Consequently every
first-machine update is d1'=d1+a, and every second-machine update is d2'=d2+c_prev.
To check the induction without assuming the conclusion, at item i the proposed
new gap is G plus the third-machine weight increments through item i-1 minus
the first-machine weight increments through item i. Each partial sum is between
zero and W; the proposed gap therefore has the stated bounds and is at least
the item's middle duration (either 1 or L+1). Both max branches are justified.

After all items, d1=1+nC+A and d3=1+G+(n+1)C+B. The suffix yields exactly

    C_max = 2+G+(n+1)C+max(A,B).

Since A+B=W plus the total weight of mode 10 items, the bound forces W even,
no mode 10, and A=B=W/2. Reading mode 11 as membership in the first part recovers
a valid source witness from every feasible assignment. Conversely any partition
chooses mode 11 for one part and 00 for the other and attains the bound. Delayed
schedules cannot improve the earliest schedule, so the argument covers them too.

The [Partition probe](flexible-blocking-partition-probe.py) checks every positive
weight sequence of lengths one through four with weights at most four: 340 source
instances and all 69,904 target assignments. It checks the exact formula for
every assignment without mode 01, rejects every assignment with mode 01, and
recovers 340 feasible target witnesses. Another 36 constructed fixed-assignment
schedules passed the separately formulated Z3 oracle (72 queries), including
both YES and NO source instances. See the [output](flexible-blocking-partition-probe.json).
These finite checks support the candidate; they are not a proof or an independent
author review. The probe currently operates on derived processing triples;
formal preparation must check the actual five-operation encoding independently.

The next action is to finish the novelty and model-equivalence audit, then admit
a campaign with a fixed question and build operation-level construction and
recovery programs. Do not describe this candidate as a resolved open problem
before that audit, independent review, and manuscript work. Experience extraction
is deferred until the candidate argument has been checked; none is counted as saved.

### Executed checks (2026-09-16)

The [recurrence probe](flexible-blocking-probe.py) compares its output with a
separately formulated Z3 integer model using operation start times, precedence,
machine occupancy, and blocking inequalities. For every sequence of one through
three jobs with each aggregated processing time in {1,2}, it checks feasibility
at the predicted makespan and infeasibility below it. All 584 instances passed
both checks (1,168 solver queries). This is independent modeling by one author,
not independent review; it validates fixed assignments, not a reduction.
Run `python3 research/evidence/flexible-blocking-probe.py` from the repository;
the saved [output](flexible-blocking-probe.json) also records the construction probe.

The construction family uses four operations per job: mandatory M1 time a,
one flexible M1/M2 operation taking x or y, mandatory M2 time b, and mandatory
M3 time c. Its actual assignment triples are (a+x,b,c) and (a,b+y,c).
All 243 profiles with a,x,y,b,c in {1,2,3} were repeated for prefix lengths
one through six. Componentwise dominated departure states were discarded,
which is sound because every subsequent transition is monotone. The largest
observed Pareto set had only two states. A suffix reversal was found for the
profile (1,1,2,1,1): its states (2,3,4) and (1,4,5), followed by the fixed job
(3,1,1), finish at 7 and 6 respectively. Thus retaining only the current smallest
makespan is invalid. This phenomenon alone does not distinguish the three-machine
problem from the already tractable two-machine case.

The [history probe](flexible-blocking-history-probe.py) tests the stronger claim
that history matters after a common final assignment. It exhausts 32² ordered
pairs of four-operation profiles with parameters in {1,2}, each followed by
one of 27 fixed jobs with processing times in {1,2,3}. For each of these 27,648
prefixes, it considers all four assignment histories and all 64 fixed suffix
triples with entries in {1,2,3,4}. No suffix achieved a better makespan by using
a state discarded by minimum prefix makespan after the common fixed job.
This is a finite absence of a counterexample, not a proof of dominance or a
polynomial algorithm. The [output](flexible-blocking-history-probe.json) records
the exhausted prefix count. Run the script directly to reproduce it.

No target instance from a Partition input has been constructed. The tested
family provides no evidence of persistent accumulation of independent choices.
The original four-operation route is therefore not sufficient for admission.
A materially different next check would permit flexibility between M2 and M3
as well, so that the last-machine processing time can depend on the choice.
It must still arise from valid operation lists; arbitrary pairs of triples
are not interchangeable with such lists.

Experience extraction: none. The small greedy failure is already explained
by the general state recurrence, and the stronger negative search has no
established general cause. Keep the exact finite scope here rather than
promoting it to a reusable impossibility statement.

The recurrence checks and restricted-family probes above are complete. Test
both flexible interfaces before investing in a Partition construction; reject
a family without persistent tradeoffs rather than interpreting state count
as hardness evidence. Gate 6 is not passed. Difficulty remains uncertain; the potential
significance is settling the precise classification gap above, not a claim of
a publishable result. No experience extracted from this source-and-model check.
