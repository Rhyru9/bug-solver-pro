# Gin debugging

For a deeper boundary case, read [A second binder sees EOF although the request body was valid](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Go guide](../../guide.md). Use this module when Gin owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect engine/router construction, middleware order, bindings, server configuration, and dependency versions. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which handler/middleware writes or aborts the response? Does binding preserve the expected missing/zero/invalid distinction?
- Does spawned work retain request context or mutable buffers beyond their owner? Which cancellation signal reaches downstream calls?

## Distinguishing experiment

Replay the actual router path and a cancelled request; trace handler order, response writes, downstream cancellation, and background resource cleanup.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
