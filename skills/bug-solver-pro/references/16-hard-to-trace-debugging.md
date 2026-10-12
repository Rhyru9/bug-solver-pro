# 16. Debugging Techniques for Hard-to-Trace Bugs

Use when traces point too late, failures are intermittent, replay is insufficient, or diagnosis circles. These are experiment-selection heuristics; choose a technique addressing current uncertainty rather than applying the entire list. Evidence fundamentals and limits are in [15-evidence-and-experiments](15-evidence-and-experiments.md).

## Four questions when stuck

1. Which observations are trustworthy, and does the tool observe what you think it does?
2. Where was state last known correct and first known incorrect?
3. What is the smallest difference between comparable failing and healthy cases?
4. Which experiment would force the current diagnosis to change?

If answers remain speculative, choose an observation point/experiment before patching. Keep brief notes on rejected and inconclusive hypotheses to avoid repeating experiments without reason.

## Choose techniques by obstacle

| Obstacle | Starting technique | Evidence sought |
|---|---|---|
| Symptoms appear far from their source | Last-correct / first-incorrect boundaries | First flow segment violating an invariant |
| Only some inputs fail | Healthy comparison plus minimization | Trigger properties, not just an example payload |
| Values change unexpectedly | Provenance plus watchpoints | Writer, version, transformation changing the value |
| Identical inputs produce different results | Reconstruct history and state | Ordering, lifecycle, or hidden-input differences |
| Failures are rare | Cohorts, denominators, controlled schedules | Failure conditions and relevant interleavings |
| Logging/debugging makes failures disappear | Observer effects | Behavior changed by observation |
| Errors shift across layers | Cross-boundary causal chains | Original errors versus wrappers, retries, downstream effects |
| Fails only after prolonged operation | Lifecycle/resource experiments | Accumulating state or resources |
| Every explanation sounds plausible | Counterfactual experiments | Predictions distinguishing explanations |

## 1. Find last-correct / first-incorrect boundaries

State invariants at selected flow boundaries and observe inputs/outputs there. Example: values are correct on entry, correct after validation, and incorrect after mapping; focus on mapping and intervening effects.

On stable paths, observe the middle of a segment to narrow the search. In asynchronous/branching graphs, follow data identity and operation dependencies; file boundaries or log timestamps do not automatically divide causal chains. Sparse checkpoints may miss an initial violation when state is corrupted and then repaired.

Observe meaning: not merely “object is non-null,” but relevant values, versions, units, tenant, and invariants. Place temporary assertions near suspected transitions; avoid production-path changes without justification and authorization.

## 2. Compare equivalent healthy cases

Choose healthy cases with similar paths, versions, load, and conditions. Compare structured inputs, initial state, effective configuration, dependencies, and order before diffing thousands of log lines.

Differences are candidates, not causes. If all failures involve one tenant, inspect its features, data, routes, and workload before blaming tenant identity. Swap a factor in tests when possible. For suspected interactions, use small combinations with relevant controls; record changes rather than varying many factors blindly.

## 3. Minimize triggers while preserving the failure signature

Remove unnecessary fields, records, events, steps, modules, or dependencies. After reduction, verify the **same kind of failure** remains, not broken setup or a new error. Record removed parts and results.

Halving and testing can help, but failure need not be monotonic: two parts may be required together, or removal may change timing. If a subset passes, test relevant complements/combinations and keep equivalent state resets. Minimal means small enough to explain the mechanism, not proof that no smaller trigger exists.

For version bisect, ensure versions build and the oracle is reliable. Unassessable runs are inconclusive; one non-failing run does not automatically establish a healthy version.

## 4. Trace value provenance and every writer

For incorrect values, ask who created them, which source supplied them, where transformations occurred, which version/units apply, and who overwrote them. Inspect setters, raw queries, callbacks, event handlers, triggers, generated code, and relevant mutable aliases; function-name searches alone are insufficient.

Use watchpoints/data breakpoints where supported, or bounded observations at mutations. Capture necessary scalar snapshots **at event time**; live objects inspected later may already have changed. Avoid logging entire payloads, forcing lazy loads, or reading unsafe state solely for instrumentation.

For persistent state, separate past corruption from current reads. Reader patches can hide symptoms without stopping corrupting writers.

## 5. Replay history, not only the last request

Hidden inputs include prior operations, retries, warm caches, session/connection reuse, ordering, clocks, flags, dependency state, and residual test data. Record relevant initial state and sequence; random seeds alone do not capture all nondeterminism.

Compare fresh versus long-running processes, clean versus reused state, and single operations versus trigger sequences in tests. If only reuse fails, investigate ownership/reset/cleanup; symptom disappearance after restarting is not a final diagnosis. Reset fixtures between experiments so early trials do not change later outcomes.

Isolate replayed external effects or use appropriate stubs/test endpoints. Do not replay real payments, emails, or webhooks just to obtain traces.

## 6. Rare bugs: count failure opportunities and control ordering

Record failures **and relevant operation counts**, not errors alone. Define signatures/cohorts: builds, paths, data shapes, state, instances, time/load. Sampling differences or falling traffic may falsely suggest disappearance.

Use bounded sampling/instrumentation capturing triggers and comparison context; size-limited ring buffers or selective traces can help where supported. Missing evidence after sampling does not establish absence.

For races, build timelines using operation identity, versions/sequences, and commit/send/receive/ack relations. Cross-machine timestamps do not guarantee causal ordering. Force interleavings with barriers/test hooks; delays/random repeats may provoke symptoms but are not fixes or proof every schedule is safe.

## 7. When observation hides bugs, inspect observer effects

Debuggers, logs, pretty printers, getters, and extra queries may change timing, force lazy evaluation, extend reference lifetimes, or acquire locks. Compare equivalent conditions with/without observation; do not immediately conclude logging repaired the bug.

Start with small observations: scalar values, identities/versions, counters, or bounded events. Choose diagnostics matching the hypothesis; measure overhead when timing matters. Changed outcomes are experiment clues, not justification to ship logging as the repair.

## 8. Follow errors back to the originating mechanism

Distinguish where errors are created, caught, wrapped, converted, retried, and displayed. Preserve original causes/statuses and operation identity in sanitized notes. “500,” “timeout,” or “null” alone may have lost important distinctions.

Across asynchronous work/processes, reconstruct parent/child relations or message IDs; do not assume the final logged error is the initial cause. Check whether secondary errors arise from cleanup, compensation, rollback, or failing observability. For timeouts, inspect effect state before retrying (`06-concurrency-transactions.md`).

## 9. Use counterfactuals and negative controls

State: “if mechanism M is correct, changing X under condition C should change Y while Z stays the same.” Test controllable boundaries. Examples: suspected aliasing → isolated copies in tests; suspected cache → vary read sources while preserving artifact/input. Changed results support hypotheses but require checking other intervention effects.

Add a negative control that **should not** trigger the bug: nearly identical payloads across a boundary, operations without retries, or paths without shared state, according to the hypothesis. If controls also fail, the diagnosis is too broad, setup is wrong, or the mechanism remains unclear.

Bypass/disable only in isolated experiments; do not weaken authorization, validation, or constraints in patches. Disappearance when a component is disabled localizes a relationship without proving the component is defective.

## 10. Long-running failures: separate elapsed time, work count, and reuse

In tests, vary one dimension: many operations in little time, long idle periods with little work, data size, or concurrency. Choose realistic workloads and observable resource limits. This distinguishes accumulation from expiration, clocks, or load; it is not an automatic diagnosis table.

Inspect acquire/release ownership and success/error/cancel cleanup. Measure live resources after relevant steady state/cleanup, not only peak memory or total allocations. Bounded cache retention and leaks need different lifecycle explanations. For stalls, inspect who waits for whom and queue/pool/lock progress, not only functions with the longest total duration.

## When to update the model

If repeated interventions add no evidence, restate facts without naming the favored cause. Check strong assumptions: correct artifact? Correct oracle? State really reset? All writers visible? Instrumentation observing events or later state?

Choose the next experiment by decision-changing uncertainty, cost, and effects. Replace unavailable techniques with equivalent observations while stating blind spots. Not every technique is required; stop searching once mechanism and impact are sufficiently tested for the requested fix.
