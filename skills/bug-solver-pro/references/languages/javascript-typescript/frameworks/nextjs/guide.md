# Next.js debugging

For a deeper boundary case, read [A hidden button still allows a server-side mutation](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [JavaScript / TypeScript guide](../../guide.md). Use this module when Next.js owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect resolved version, router type, rendering/runtime configuration, deployment mode, and React dependency. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Where does the incorrect value first appear: server render, client hydration, route handler, or later navigation? Which cache serves it?
- What is the scope of cached or shared state? Which invalidation and authorization paths execute for each user/navigation?

## Distinguishing experiment

Compare direct load and client navigation plus two relevant identities; record the value and cache provenance at each boundary.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
