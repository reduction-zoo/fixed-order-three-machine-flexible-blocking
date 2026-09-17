# Encodings and executable contract

Source: `{"weights":[w1,...,wn]}`, a nonempty list of positive integers. The
language is YES exactly when a subset sums to half the total. Source witnesses
are `{"selected":[b1,...,bn]}` with integer bits selecting that subset. Invalid
source encodings map to a fixed legal NO target.

Target: `{"jobs":[job1,...,jobN],"bound":H}`. A job is a nonempty operation
list; each operation is an object mapping allowed machine numbers (strings
"1", "2", "3") to positive integer times. Allowed sets are singletons or
{1,2}/{2,3}. Each job has exactly one mandatory operation on each machine,
in order. It may have intervening flexible operations. A legal assignment
chooses an allowed machine per operation and is nondecreasing within every job.
The supplied job order applies to every machine. There is no preemption or
buffer; a job holds its current machine until starting on the next. H is a
nonnegative integer. Target witnesses are `{"assignment":[[machine,...],...]}`.
They are valid when some feasible schedule for that assignment finishes by H.
The earliest schedule is sufficient to check this predicate.

`python3 algorithm.py` reads one source JSON object and returns a target JSON
object. `python3 algorithm.py --extract` reads `{"source":...,"target_solution":...}`
and returns a source witness. Each invocation is a fresh process. Extraction
is required only for valid target witnesses of forward outputs; invalid witness
behavior is not part of the mathematical recovery contract. In forward mode,
malformed JSON maps to the same fixed NO target as malformed decoded objects.
In extraction mode, malformed JSON and execution failures exit nonzero.
Integer decimal conversion is unlimited in both modes; integers are not
restricted by Python's default transport digit limit.
