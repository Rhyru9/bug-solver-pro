# SvelteKit debugging

For a deeper boundary case, read [Enhanced form succeeds but the page does not update](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect SvelteKit/Svelte versions, adapter, route tree, hooks, and prerender/SSR configuration. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Does the wrong value originate in a server load, universal load, action, endpoint, or hydration? Which invalidation path re-runs it?
- Is user state scoped to a request? Are cookies, redirects, failures, and serialized data handled consistently between direct and client navigation?

## Distinguishing experiment

Compare direct load, client navigation, and action submission; trace server/client load inputs, response payloads, invalidation, and per-user isolation.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
