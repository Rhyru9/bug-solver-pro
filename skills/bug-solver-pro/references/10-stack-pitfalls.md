# 10. Translate Stack Pitfalls into Mechanisms

Challenge assumptions when moving between languages/frameworks/libraries. These are investigation questions, not universal product claims. Discover actual-version answers through [14-stack-semantics](14-stack-semantics.md) and [13-research-adaptive](13-research-adaptive.md).

Use the [language/framework index](languages/index.md) for stack-specific questions. This table retains mechanisms shared across stacks; put maintained language/framework details in their own module directories.

| Appearance | Assumption to test | Discriminating question |
|---|---|---|
| Null checks/defaults resolve errors | Missing values are legitimate | Optional, not loaded, parse failure, or fetch failure? |
| Objects change by themselves | Assignment creates a copy | Aliasing, shallow copies, reused buffers, lazy objects, or shared mutation? |
| Annotations/decorators do not work | All calls pass through the framework | Proxy/hook or direct call? Correct registration and scope? |
| Validation passes but data is wrong | Every path uses the same validator | Do imports, bulk operations, raw queries, jobs, or generated code bypass it? |
| Task returns but effects are missing | Return means all work finished | Lazy tasks, detached workers, streams, cancellation, or unobserved futures? |
| Catch does not handle failure | Errors are always synchronous exceptions | Result/status values, events, failed tasks, or delayed failures? |
| Transactions do not protect changes | Transaction APIs cover all effects | Same connection/session? Hooks/external effects outside the atomic boundary? |
| Tests pass but runtime fails | Tests match the real environment | Different providers/drivers, config, scopes, builds, schedulers, or dependencies? |
| Jobs read different records | Payloads are snapshots | Values, IDs, references, or serialized data fetched again? |
| Cancellation/timeout means total failure | Caller termination stops effects | Already committed? Task still running? Resources released? Retry duplicates? |
| New fields are compatible | Additions are always safe | Unknown fields rejected, exhaustive enums, schema validation, changed signatures? |
| Atomic means global | Guarantees span all participants | Per process, connection, key, partition, database, or across services? |
| Restart is a fix | Symptom disappearance proves the cause | What state/resources reset? Can the symptom return after time/load? |

If no row fits, map the failed invariant and boundaries directly. Missing examples do not justify forcing a diagnosis or researching a larger catalog.
