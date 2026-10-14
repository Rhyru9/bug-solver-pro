# NestJS debugging

For a deeper boundary case, read [ValidationPipe is installed but malformed DTOs still pass](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [JavaScript / TypeScript guide](../../guide.md). Use this module when NestJS owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect bootstrap, module graph, provider registrations/scopes, transport, and build output. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Does the failing call traverse the expected guard, pipe, interceptor, and exception filter for this transport?
- Which instance owns mutable state? Do direct service calls and background jobs use the same validation and lifecycle as requests?

## Distinguishing experiment

Compare the failing transport path with a direct service call; record provider identity and the order of validation, effects, and exception handling.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
