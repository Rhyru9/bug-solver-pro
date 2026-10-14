# 19. Make the next debugging decision from evidence

Use when a familiar recipe fits too easily, a probe passes without explaining the incident, or several plausible causes remain. This adds decision gates to [root-cause analysis](02-root-cause-analysis.md) and [tracing techniques](16-hard-to-trace-debugging.md); it is not a checklist for every small bug.

## 1. State a claim at the right granularity

Replace “the cache is broken” with “request R reads projection P, keyed by K, whose version predates write W.” Record the entity/actor, source version, intended effect, and last-correct/first-incorrect transition. A familiar exception or technology name is not a mechanism.

Separate necessary prerequisites from the predicted consequence. Example: a missing await matters only if that particular task owns a required effect and the caller can finish before it. Finding any unawaited promise elsewhere does not explain this report.

## 2. Check whether a probe can distinguish anything

Before interpreting a pass/fail, establish:

| Gate | Evidence needed | If missing |
|---|---|---|
| Applicable | Actual version/mode, path, identity, state and boundary match the hypothesis | Recipe is a lead, not an applicable explanation |
| Activated | The suspected branch, overlap, retry, cleanup or reuse actually occurred | Non-failure is inconclusive |
| Sensitive | The observation can detect the predicted violation; a safe known-bad control triggers it where feasible | Missing evidence may be a blind observer |
| Comparable | Baseline/intervention use equivalent initial state, workload and artifact | Changed results may be confounded |

These are gates for interpreting evidence, not a demand for production fault injection. Use local test hooks, independent queries, or recorded traces at authorized boundaries. If a gate cannot be checked, retain that limit.

“No duplicate in 100 requests” is not a falsifier when none overlapped. “One shared state pointer” does not establish cross-process sharing. “SQL is correct” does not establish the ORM's final graph. “Callback ran” does not establish commit or durable delivery.

## 3. Predict competing observations before changing code

When alternatives remain, use a small decision table:

| Candidate | Distinguishing prediction | Next observation | Result that changes the decision |
|---|---|---|---|
| Stale cache | Authoritative read is current; named projection is old for the same identity | Compare versions and keys without redeploying | Both sources current: inspect downstream presentation |
| Old artifact | Failing execution identifies a different build/path | Trace artifact identity at the implicated operation | Same artifact through the failure: inspect state/history |
| ORM reuse/fixup | SQL membership is correct; managed graph contains previous entities | Compare fresh and reused contexts with identical rows | Wrong rows already in SQL: inspect predicate first |

Prefer a cheap observation whose possible outcomes lead to different actions. Another log that both explanations predict adds little. Inspect a prerequisite rather than rerunning an experiment when the prerequisite itself is uncertain.

## 4. Use hidden dimensions deliberately

- **Identity as a tuple:** trace business ID, tenant/actor, operation ID, attempt ID, state version, worker/process and build. Equal business IDs do not prove equal operations, instances or versions. Compare only fields relevant to the suspected boundary.
- **Count transformations:** count one user action → submissions → attempts → handler starts → commits → external effects. The first increase localizes multiplicity. Several logs from one retry attempt are not necessarily several effects; one request log can also hide downstream retries.
- **Read through an independent path:** compare original bytes, query rows, managed objects and wire output. Reusing the same identity map/cache/serializer in the oracle can confirm the same error twice.
- **Probe order as well as content:** run A→B and B→A, then B in fresh state. Dependence on prior operations points to reuse, lifecycle, identity or initialization; it does not identify which one without another discriminator.
- **Use metamorphic relations:** when exact expected output is expensive, test a justified invariant such as isolation between tenants, replay having one effect, or permitted reordering preserving totals. State why that relation is promised; order can legitimately change pagination or last-writer semantics.
- **Separate time from work:** vary elapsed time, operation count, concurrency and input size independently where feasible. Do not explain a pool stall from CPU samples alone; follow the resource holder and wait chain.

## 5. Update status precisely

- A reliably observed contradiction with applicable prerequisites can reject the specific claim tested. It does not eliminate every related mechanism or every schedule.
- A predicted change after an intervention supports causality only to the extent that competing changes were controlled. Replacing a database driver, restarting workers and clearing caches together proves little about which change mattered.
- An untriggered, insensitive or confounded probe is **INCONCLUSIVE**, even if it passed.
- Direct evidence may support a cause without reproducing the incident. State what is observed versus inferred and which missing condition matters.

Report an externally checkable reasoning summary: observed facts → candidate mechanism/prerequisites → chosen discriminator → result → decision and remaining limit. Do not invent a detailed thought transcript or fill a template with unsupported claims.

## 6. After the patch, try to break the explanation

Replay the original trigger and a nearby negative control. Exercise the relevant error/cancel/retry boundary. Where safe, confirm that removing only the fix restores the same failure in an isolated copy; do not erase user work. If the symptom disappears but the alleged invariant still fails, the patch may only mask it.

Use [composed failures](20-composed-failures.md) for interacting causes, and [coverage audit](coverage/gap-audit.md) for maintained skill gaps. Stop expanding once the requested mechanism and impact are adequately supported; unresolved unrelated categories are not mandatory work.
