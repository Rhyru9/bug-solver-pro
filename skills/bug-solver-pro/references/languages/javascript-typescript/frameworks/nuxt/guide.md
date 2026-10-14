# Nuxt debugging

For a deeper boundary case, read [Authenticated API works in the browser but fails during SSR](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

## Establish configuration and entrypoints

Inspect Nuxt version, nuxt.config, Nitro/server deployment, module registrations, and Vue version. Match the executing artifact and entrypoint with the reproduction/test environment.

## Boundary and lifecycle questions

- Does divergence begin in server rendering, payload transfer, hydration, or client navigation? Which data key, cache, or runtime configuration is read?
- Is state or a composable scoped to the request or shared on the server? Can a stale async response or plugin override newer state?

## Distinguishing experiment

Compare server load and client navigation with equivalent inputs and distinct identities; trace state provenance, payload serialization, and repeated requests.

Before the experiment, state the predicted observation and a result that rejects the candidate mechanism. Keep effects isolated from production systems.

## Verification and limits

Verify the original trigger, healthy neighboring behavior, and implicated error/cleanup paths through the real framework boundary. Use matching providers, features, and worker/build modes where they affect the mechanism. Passing a direct function test does not verify framework wiring. Record evidence and untested boundaries; these questions do not establish a diagnosis.
