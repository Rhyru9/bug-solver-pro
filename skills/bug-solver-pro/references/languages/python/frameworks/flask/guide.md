# Flask debugging

For a deeper boundary case, read [Two successful requests lose one session update](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Python guide](../../guide.md). Use this module when Flask owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect application factory, blueprint registration, effective configuration, WSGI worker mode, and extensions. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Is the expected application/request context active? Which extension instance and configuration does the failing path use?
- Does background work reference a request context after its lifetime? Is per-request data held by a reused process object?

## Distinguishing experiment

Compare a real request with the failing command/job path; track context, extension/session ownership, teardown, and repeated-request state.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
