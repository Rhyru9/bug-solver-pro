# Vue debugging

For a deeper boundary case, read [Reading a computed sort changes another component's list](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect resolved Vue version, compiler/build setup, component tree, and state/store ownership. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Where does the changed value lose reactivity or become stale? Do destructuring, object identity, keys, or computed dependencies explain the first incorrect render?
- Which watcher or lifecycle hook starts asynchronous work, and how is stale work or an unmounted subscription cleaned up?

## Distinguishing experiment

Replay the interaction with a delayed older response; compare source state, computed values, and rendered output before and after component teardown.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
