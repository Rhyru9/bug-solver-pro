# Axum debugging

For a deeper boundary case, read [Adding authentication changes unknown URLs from 404 to 401](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect axum/tower/tokio versions, Cargo features, Router composition, state types, and server startup. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which layer or extractor rejects the request? Does body consumption or state routing differ from the assumed handler path?
- Which cloned state shares mutable resources? Where do lock guards, blocking work, cancellation, and spawned tasks cross await boundaries?

## Distinguishing experiment

Send the failing request through the actual Router and layers; record extractor/rejection order, shared state identity, task completion, and cleanup.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
