# FastAPI debugging

For a deeper boundary case, read [A supposedly filtered response exposes extra fields on one route](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Python guide](../../guide.md). Use this module when FastAPI owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect application construction, router/dependency registration, ASGI server configuration, and resolved validation-library versions. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which dependency instance and validated representation reach the endpoint? Do omitted, null, defaulted, and coerced fields remain distinguishable?
- Who owns each database session and dependency cleanup? Does background or blocking work outlive the response or occupy the event loop?

## Distinguishing experiment

Exercise the actual ASGI dependency path with success and failure payloads; record session lifetime, task completion, cleanup, and stored values.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
