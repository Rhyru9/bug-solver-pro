# 15. Evidence, Experiments, and Difficult Cases

Read when multiple explanations fit, reproduction is unavailable, or bugs depend on timing, load, crashes, or environment.

For concrete tracing techniques when diagnosis stalls, read [16-hard-to-trace-debugging](16-hard-to-trace-debugging.md).

## Choose experiments that change decisions

For the leading hypothesis, record explained observations, unseen predictions, falsifying outcomes, and actions based on results. Choose the cheapest safe discriminator, not the greatest number of tests. Multiple hypotheses are useful when observations fit multiple mechanisms, not mandatory for every bug.

Example: stale values could come from a cache or an old artifact. Check artifact version and read source, then bypass the cache in isolation. Clearing all caches while redeploying changes two variables and does not establish the cause.

Reduce inputs while retaining the failing execution path. Compare failing and healthy cases by versions, data, configuration, ordering, and resources. If single-variable changes are not possible, record confounders and avoid claiming complete causal proof.

## Evidence types and limits

- **Observation:** tests/logs/queries show an event in a particular context. Record inputs, versions, conditions, results, and traceable artifacts.
- **Documented contract:** describes version-specific promises/behavior; does not establish that the application follows the relevant path/prerequisites.
- **Causal support:** controlled reproductions or isolated interventions change outcomes as predicted. Diagnosis may rely on combined traces/mechanism evidence without reproduction, with explicit limits.
- **Hypothesis:** consistent explanation not yet distinguished from alternatives.
- **Inconclusive:** tools/observations cannot distinguish explanations; this does not mean true or false.

Empty logs do not prove absence when sampling, buffering, crashes, or context propagation remain unchecked. Passing tests that never reach the failing path are not evidence of repair.

## When reproduction is unavailable

1. Preserve available incident evidence and sanitize sensitive data. Identify signatures, affected cohorts, and healthy comparison cases.
2. State missing inputs: payloads, order, versions, old state, topology, load, or visibility. Do not invent a reproduction.
3. Create replay/synthetic fixtures retaining trigger properties, or bounded instrumentation testing predictions. Do not enable broad/sensitive production logging without authorization.
4. If the mechanism is sufficiently supported, prepare/test a candidate patch locally; report that incident reproduction remains unconfirmed. Resolve unknown choices before applying patches that depend on them.
5. Authorized outage mitigation may precede final diagnosis; distinguish mitigation, cause repair, and data recovery.

## Timing, races, and partial failures

Use barriers/latches or test hooks to force suspected ordering; random repetition alone may miss races. Inspect results, effect counts, and final state. Fault injection at commit/publish/ack/reply boundaries reveals operations that succeed while callers time out.

Timeouts show the caller stopped waiting, not necessarily cancellation. Check cancellation ownership, committed effects, retries, and reconciliation. Do not promise exactly-once behavior solely from dedupe flags or after-commit hooks.

## Performance and resources

Define metrics, workload, and failure thresholds: latency distributions, throughput, errors, memory after steady state, queue depth, or resource exhaustion. Compare equivalent conditions using adequate observations; one stopwatch measurement does not prove stable improvement.

Separate CPU work, allocation, I/O, locks, queues, and external waits with appropriate profilers/traces/plans. Caching/pooling can reduce latency while increasing stale state or leaks. Verify correctness, success/error/cancel cleanup, bounded growth, and trade-offs.

## Crashes or build-dependent behavior

Preserve stacks/dumps/symbols and build identity. Trace resource ownership, bounds, lifetimes, races, and relevant compiler-mode/architecture differences. Use project-supported debuggers, sanitizers, race detectors, or runtime diagnostics. A crash disappearing in debug builds does not prove release safety.

## When to change approach

If iterations produce new patches without new evidence, summarize rejected explanations and remaining uncertainty. Change tools, observation boundaries, inputs, or the system model. Stop broad investigation once mechanism/impact adequately support a decision; expand again only when new evidence, failures, or unresolved risks require it.
