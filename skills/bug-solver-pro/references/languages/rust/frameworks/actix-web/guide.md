# Actix Web debugging

For a deeper boundary case, read [Increasing HTTP workers exhausts database connections](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect actix-web/runtime versions, Cargo features, HttpServer application factory, Data registrations, and worker configuration. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which application/scope/resource middleware and extractor execute? Is state registered at the intended scope and with the expected type?
- Is state created per worker or shared across workers? Do blocking operations, locks, or detached tasks delay responses or outlive cancellation?

## Distinguishing experiment

Compare the failing route with matching and differing worker configurations; record application/state identity, extractor results, shared effects, and resource release.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
