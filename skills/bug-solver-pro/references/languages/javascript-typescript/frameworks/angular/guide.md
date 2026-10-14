# Angular debugging

For a deeper boundary case, read [An interceptor changes the payload on a retried request](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Angular/build versions, bootstrap mode, providers, component change detection, and zone configuration. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Which provider instance and reactive value reach the component? Does the form/router/HTTP path preserve the intended value and validation state?
- Who owns an observable subscription, signal effect, or pending HTTP request? Can injector scope, change detection, or response ordering cause stale UI?

## Distinguishing experiment

Replay the actual routed component flow with controlled response ordering; observe provider identity, state updates, rendered state, and destruction cleanup.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
