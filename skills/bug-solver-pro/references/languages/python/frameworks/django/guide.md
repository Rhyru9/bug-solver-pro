# Django debugging

For a deeper boundary case, read [get_or_create still inserts duplicates under concurrency](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [Python guide](../../guide.md). Use this module when Django owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect settings selected by the running process, URL/middleware setup, database aliases, and web/job worker mode. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- When is the queryset evaluated and against which connection? Do bulk/raw/job paths traverse the same validation and signals?
- Which effects occur before commit, on commit, or outside the transaction? Does the test runner hide the production boundary?

## Distinguishing experiment

Replay through the actual view/job path and configured database; capture query evaluation, signal execution, commit, and external effect order.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
