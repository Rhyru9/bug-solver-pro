# Laravel debugging

For a deeper boundary case, read [Adding an orWhere widens a tenant-scoped query](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [PHP guide](../../guide.md). Use this module when Laravel owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect installed framework version, service container bindings, effective cached configuration/routes, and queue worker setup. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which middleware, policies, validation, casts, observers, and model events execute on this path? Are raw or bulk operations different?
- Does job dispatch happen before the required data commits? Can retry or a reused worker duplicate effects or retain previous request state?

## Distinguishing experiment

Exercise the failing HTTP/job path with its configured driver; capture commit/dispatch order, retry effects, and fresh versus reused worker behavior.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
