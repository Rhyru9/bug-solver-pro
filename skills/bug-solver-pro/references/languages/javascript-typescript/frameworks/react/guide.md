# React debugging

For a deeper boundary case, read [Editing the second row changes the first row's draft](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [JavaScript / TypeScript guide](../../guide.md). Use this module when React owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect resolved React/renderer versions, root setup, build mode, and state ownership. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which render supplied the captured values? Are identity, keys, stale closures, or out-of-order responses changing the displayed state?
- Which effect setup owns cleanup? Can a prior request, subscription, or optimistic update overwrite newer state?

## Distinguishing experiment

Replay the actual interaction and an adverse response order; observe render inputs, commits, effect cleanup, and final UI state.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
