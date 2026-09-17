# Independent review — round 001

Decision: **revise**. Review date: 2026-09-16.

The mathematical construction and recovery argument are sound for the fixed
general operation model. The submitted executable fails on legal large integer
inputs, so the complete implemented rule cannot advance yet. This is a local
repair, not evidence against the construction or a reason to restart research.

## Correctness

I read README.md, the fixed question, contract.md, algorithm.py, proof.md,
preparation.md, verification.md, both round logs, both checkers, and the linked
screening record. No candidate implementation was imported. No shared experience
entry is used by the proof.

The earliest-departure recurrence is correct for the stated blocking convention.
For a fixed assignment, operations assigned to a machine form a contiguous
block. Removing internal idle time does not delay any release. The preceding
job's departure from a machine is its successor-machine start, except on M3,
where it is completion. These facts give the two max updates and final addition.
They also give lower bounds for every delayed schedule. Monotonicity proves
global earliest optimality, not merely feasibility of a particular schedule.
Simultaneous departure and arrival are permitted; no job skips a machine.

The four item modes in proof.md exactly match the operation lists in
algorithm.py. Mandatory visits make all four choices legal and exclude other
modes. The primer and suffix have no choices. For the forbidden mode (0,1),
the middle-machine increment exceeds the preceding M3 duration by at least
W+3. Telescoping the nonnegative increments retains that excess through all
later items. Adding the final item M3 duration and suffix M3 processing gives
a completion strictly above H. No assumption about the other choices is needed.

For the remaining modes, the induction is valid: the previous gap is at most
C-1, forcing the first max branch; the proposed next gap is at least L+1,
forcing the second branch even when the item middle time equals L+1. Partial
alpha and beta sums individually never exceed W, including duplicated weights
in mode (1,0). The suffix eliminates its middle redundant term and gives exactly
the stated constant plus max(A,B). Thus feasibility forces W even and excludes
every duplicated positive weight. Selecting operation 2 on M1 recovers a subset
of sum W/2. Conversely, any partition supplies legal complementary item modes
attaining H. These arguments cover arbitrary valid witnesses, rather than only
optimal assignments or witnesses found by one solver.

There are 5n+6 operations and all numbers have O(log(nW)) bits. The O(N²) output
bound and conservative O(N³) forward bound are valid for standard unbounded
integer arithmetic and decimal/binary conversion. Recovery is deterministic
linear scanning/indexing after parsing; the proposed quadratic conservative
bound is sufficient. No oracle or search occurs in either implemented map.
NP membership follows from assignment certificates and the recurrence.

### Required repair: integer transport is bounded in the executable

Current locations: algorithm.py:27 (`json.load`) and algorithm.py:34
(`json.dumps`), affecting forward and recovery; proof.md:111–119 claims
unbounded polynomial bit behavior without accounting for this transport limit.

On the installed Python 3.14.7, the default integer decimal conversion limit
is 4,300 digits. Both of these valid YES inputs fail:

* weights [10^4300, 10^4300]: parsing exits 1 before construction.
* weights [10^4300-1, 10^4300-1]: both weights parse, but the larger constructed
  durations fail during serialization, exit 1.

Recovery also exits 1 on the first source with the valid assignment consisting
of primer [1,2,3], selected item [1,1,2,2,3], unselected item [1,2,2,3,3], and
suffix [1,2,3]. The proof above establishes that witness's feasibility without
needing the broken forward serialization.

Minimal parsing reproducer, from this campaign directory:

```python
import subprocess, sys
number = '1' + '0' * 4300
source = '{"weights":[' + number + ',' + number + ']}'
subprocess.run([sys.executable, 'work/algorithm.py'], input=source, text=True)
```

Required correction: explicitly support unlimited integer decimal conversion
in both modes, and test parsing, output serialization, and witness recovery
above the default limit. A bounded-digit restriction would weaken the fixed
language and is not an acceptable repair. The verification tools must also
support large integers if they are used for this regression.

### Encoding totality clarification

contract.md's first paragraph says invalid source encodings map to a fixed NO
target, but its final sentence requires JSON syntax errors to exit nonzero.
algorithm.py:27 follows the latter operational rule; proof.md's totality
discussion does not delimit decoded JSON objects. This does not damage the
YES/NO argument on legal instances. For a total string-language Karp map,
state and implement the treatment of malformed serialized inputs explicitly,
or clearly distinguish the total abstract map from its valid-JSON transport.
Do not describe the current process as total on all strings. This clarification
is independent of the large-integer counterexample, which uses legal JSON.

### Independent targeted evidence

Run `python3 reviews/initial/check.py` from the campaign directory.
Saved output: [check-result.json](check-result.json).

The independently written checker has one start variable per operation,
operation precedence, and machine release constraints tied directly to the
next operation's start. It does not aggregate processing triples or use the
candidate recurrence. It asks Z3 about each fixed assignment at the actual
constructed bound and executes the extractor for every feasible assignment.
Seven selected sources produced 628 assignments and 10 recovered witnesses,
all with matching independent subset decisions. Cases include odd totals,
singletons, skewed weights, multiple partitions, 100-bit magnitudes, and four
items. Three separate large-integer transport probes fail as described above.
The script records those failures rather than asserting the submitted program
works. Finite results supplement the general proof; they do not establish it.

The existing logs report 10 prepared sources/14 recovered witnesses and
39 exhaustive sources/1,884 assignments/24 recovered witnesses, plus six
malformed decoded objects. I inspected their implementations and reused that
evidence rather than rerunning those suites.

## Novelty

Judgment: supported within the following bounded literature coverage, with no
matching known result identified. This is not an exhaustive novelty guarantee.

[Nicosia et al., COR 184 (2025), 107219](https://doi.org/10.1016/j.cor.2025.107219),
Section 2, Table 3 and Section 7, explicitly identify the fixed-order
three-machine blocking-flexibility case as open. Section 3.2 treats two
machines. Section 2 defines variable operation counts, then adopts a common
operation pattern for presentation while stating its models and algorithms
do not require it. The candidate fits the general definition; it does not
prove hardness for identical operation patterns. The primer and suffix are
precisely where the patterns differ. The published table therefore supports
the general-model motivation, but a claim settling its common-pattern
restriction would require an additional argument. The
[2024 preprint](https://arxiv.org/html/2411.18381v1), Section 2, Table 1 and
Section 3.2, supplies the same model distinction. The published primary text
was available through indexed publisher search excerpts; direct opening failed.

[Lin, Hwang and Gupta](https://link.springer.com/article/10.1007/s10951-016-0493-x),
publisher abstract (2017 volume, online 2016), proves hardness for the
fixed-sequence two-machine flexible-operation problem. The inspected abstract
does not provide its complete proof. Nicosia's Table 3 and Section 3.2 identify
that case as without blocking. Adding blocking changes feasibility, so it
does not immediately establish the submitted theorem.

[Shop scheduling problems with pliable jobs](https://link.springer.com/article/10.1007/s10951-019-00607-9),
Sections 2 and 6.1, distinguishes discrete flexible operations from divisible
processing and shows polynomial fixed-order optimization for its pliable model.
Its Partition construction uses the position of a separator job in a variable
sequence. Neither the divisible model nor that sequencing choice is available
here; the result does not subsume this construction.

The known preemptive two-machine paper is
[Khorasanian and Moslehi, DOI 10.1016/j.cor.2016.09.023](https://doi.org/10.1016/j.cor.2016.09.023).
Its full theorem proof was not inspected; the candidate cannot claim a complete
comparison with it. The 2025 primary account distinguishes its preemption and
variable-order premises. Hardness with choices of order or preemption does
not by itself imply hardness when those choices are removed.

Dated queries on 2026-09-16 included the exact 2025 DOI and title, `"fixed"
"blocking" "inter-stage flexibility" "NP-hard"`, `"three machines" "fixed"
"FIXB"`, `"fixed sequence" "flexible flow shop" "Partition" blocking`,
`"fixed" "blocking" "operation assignment" "NP-hard" three`,
`"blocking" "fixed sequence" "three" "flexibility" 2026`, and
`"FIXB" "Partition"`. No later resolution or equivalent discrete construction
was identified. Unindexed papers, unpublished work, and uninspected full proofs
remain coverage limitations, not evidence of novelty.

## Significance

Judgment: meets the fixed campaign's significance criterion for the general
model, conditional on repairing the executable. It establishes weak NP-hardness
through a deterministic Karp map and arbitrary-witness recovery for the
three-machine fixed-order decision problem. The useful mathematical mechanism
is retaining two cumulative loads despite blocking, using a middle-time penalty
to exclude one local mode and a suffix to detect both totals. This is more than
an implementation of the two-machine algorithm. It neither establishes strong
NP-hardness nor resolves the stricter common-pattern variant.

After the transport repair and aligned totality wording, rerun the required
candidate checks and the targeted regressions, then request focused follow-up
review. The mathematical and literature findings above can be reused if the
construction is unchanged. No publication acceptance is implied.
