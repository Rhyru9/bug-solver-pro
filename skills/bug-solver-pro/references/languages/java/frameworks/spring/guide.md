# Spring debugging

For a deeper boundary case, read [REQUIRES_NEW causes a stall only under load](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Java guide](../../guide.md). Use this module when Spring owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect application context, component scanning, proxy configuration, active profiles, and resolved Spring modules. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Does the invocation cross the configured proxy, or call the target directly? Which transaction, validation, caching, and async advice actually executes?
- Which bean scope and thread own the state? Does async execution or an event listener leave the transaction/context that the caller assumes?

## Distinguishing experiment

Compare entry through the real bean/proxy with the failing invocation; record advice execution, thread, connection, rollback, and external effect order.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
