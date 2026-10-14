# Hono debugging

For a deeper boundary case, read [Validator works but a later raw Request read fails](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Hono version, runtime/adapter, route/middleware construction, and deployment bindings. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which route, middleware, and error handler run in the failing runtime? When is the response created, replaced, or finalized?
- Are request context values or runtime bindings reused across operations? What work is awaited or scheduled after the response?

## Distinguishing experiment

Exercise the actual adapter path with success, throw, cancellation, and repeated-request cases implicated by the bug; trace context and response ownership.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
