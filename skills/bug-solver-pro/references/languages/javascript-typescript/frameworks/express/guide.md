# Express debugging

For a deeper boundary case, read [Webhook signature fails only through the full middleware stack](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [JavaScript / TypeScript guide](../../guide.md). Use this module when Express owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect package resolution, app/router construction, middleware registration order, and error handling. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Does the request reach the expected router and middleware? Which layer terminates the response or forwards the error?
- Are request-specific values stored in shared objects? Does work continue after the response or disconnect?

## Distinguishing experiment

Exercise the actual middleware chain with a failing request, a healthy neighbor, and an error path; record response completion and remaining effects.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
