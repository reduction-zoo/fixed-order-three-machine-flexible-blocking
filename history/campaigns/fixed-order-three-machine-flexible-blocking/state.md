# Campaign state

Status: **ready_for_expert_review** (2026-09-16).

Result: a deterministic Partition Karp reduction proves NP-completeness of
fixed-order three-machine flexible blocking makespan feasibility in the general
model allowing varying operation patterns. Both the forward map and recovery
from every feasible target assignment are implemented and proved. No claim of
strong NP-hardness, identical operation patterns, or publication acceptance.

Budget: original allocation 40; started 1, completed 1, unused 39. The latest
20-round continuation completed the already-active round without opening a new
construction route. Completion was reached before exhausting either allowance.
Screening probes are not retroactively labeled as formal rounds.

| Round | Result | Evidence |
|---|---|---|
| [001](rounds/001/round.md) | Complete, one construction route | General proof, operation tests, transport repair, independent review, inspected paper |

Current artifacts: [algorithm](work/algorithm.py), [proof](work/proof.md),
[contract](work/contract.md), [Typst manuscript](work/manuscript.typ),
[five-page paper](work/manuscript.pdf).

Checks, run from this campaign directory:
- `python3 work/check.py --candidate work/algorithm.py`: 10 sources, 14 recoveries;
  [current output](rounds/001/prepared-check-after-repair.json).
- `python3 work/verify.py --candidate work/algorithm.py`: 39 sources, 1,884
  assignments, 24 recoveries, six malformed decoded inputs, three malformed JSON
  strings, two large-integer recoveries;
  [current output](rounds/001/verification-check-after-repair.json).
- [Initial independent review](reviews/initial/review.md): general mathematics
  supported; 628 assignment checks and ten recoveries; integer-transport defect
  found and preserved.
- [Focused review](reviews/transport-repair/review.md): advance after repair;
  six large-integer recoveries and eight malformed-input checks.
- [Manuscript addendum](reviews/transport-repair/manuscript-addendum.md): advance
  maintained. `typst compile work/manuscript.typ work/manuscript.pdf` passed;
  all five final page renders in `work/evidence/manuscript/final-page-*.png`
  were visually inspected. [Compilation log](work/evidence/manuscript/compile.log).

No algorithm or mathematical change followed the advance review. Manuscript
wording and layout were corrected and recompiled; these did not require rerunning
unchanged algorithm suites. Test domains overlap and counts are not additive.

Novelty and significance are supported within the dated primary-literature
coverage in the initial review, not guaranteed exhaustively. Human expert
assessment remains the next result-level step. The fixed campaign has no open
construction or verification obligation.

Experience: 0 shared files created, 0 updated, 1 pending. The proposed
blocking-two-load-suffix entry is recorded in [round 001](rounds/001/round.md)
with premises and evidence. Transfer to `research/experience/` is pending because
this active campaign restricts writes to its own directory. No shared update
or board update is falsely claimed.

Post-campaign selection update (2026-09-16): the ongoing multi-topic authorization
now permits board and shared-experience maintenance outside the closed campaign.
The proposed entry was transferred to
[blocking-two-load-suffix](../../research/experience/blocking-two-load-suffix.md),
and the problem card/board were synchronized. Closeout counts are now one shared
entry created, zero updated, zero pending; the earlier pending statement records
the campaign-time write boundary.
