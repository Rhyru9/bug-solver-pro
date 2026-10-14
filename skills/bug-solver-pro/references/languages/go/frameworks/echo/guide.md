# Echo debugging

For a deeper boundary case, read [Client disconnects but downstream calls keep consuming resources](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Echo version/module import, router and middleware registration, binder/validator, and server settings. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which middleware or error handler writes the response? Are route/body/query fields bound and validated in the intended order?
- Does asynchronous work retain a context or buffer beyond its owner? Does downstream work receive request cancellation and release resources?

## Distinguishing experiment

Exercise the actual handler chain with a malformed input and cancellation when relevant; trace binding values, context lifetime, response writes, and cleanup.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
