# Svelte debugging

For a deeper boundary case, read [An effect ignores a value read after await](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Svelte/compiler versions, legacy versus runes syntax, build plugins, component tree, and state/store ownership. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Where do derived values, props, bindings, or store updates stop reflecting the intended state? Is compiler transformation or runtime identity involved?
- Which effect or subscription owns cleanup? Can delayed work update state after a newer interaction or component teardown?

## Distinguishing experiment

Replay the original interaction while observing input, derived state, DOM updates, and subscription cleanup; compare the actual compiled build mode.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
