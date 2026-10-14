# Rails debugging

For a deeper boundary case, read [A stale edit silently replaces a newer one](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Ruby guide](../../guide.md). Use this module when Rails owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect resolved Rails/components, environment configuration, middleware, Active Record adapter, and job backend. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which callbacks, validations, scopes, serializers, and controller filters execute? Do bulk updates or jobs take another path?
- When do lazy relations execute and jobs see committed data? Does request/job reuse retain tenant, locale, or other operation-specific state?

## Distinguishing experiment

Replay the failing controller/job with the configured database/backend; capture SQL, callbacks, commit/enqueue order, retries, and repeated-operation isolation.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
