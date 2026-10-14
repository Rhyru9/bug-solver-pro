# ASP.NET Core debugging

For a deeper boundary case, read [Filtered Include returns entities outside the filter](boundary-case.md).

Start with the [debugging playbook](playbook.md) for concrete failure signatures, probes, and repair patterns. Use the [official documentation map](docs.md) when a contract, version difference, or configuration remains unresolved.

Read with the [C# / .NET guide](../../guide.md). Use this module when ASP.NET Core owns a boundary involved in the reported bug; keep the shared [stack-semantics workflow](../../../../14-stack-semantics.md) for unknown semantics.

## Establish configuration and entrypoints

Inspect host setup, middleware order, endpoint mappings, DI registrations, and data provider. Identify the entrypoint that actually fails and the equivalent path used by tests.

## Boundary and lifecycle questions

- Which middleware, binding, filters, and authorization path reaches the endpoint? Does the input retain the expected null/default distinctions?
- Does a singleton/background task retain scoped dependencies? Is a database context shared across concurrent tasks or disposed before completion?

## Distinguishing experiment

Exercise the real host pipeline and provider; record service scope, task lifetime, database calls, response, and disposal under success and failure.

State the predicted observation and its falsifier before changing behavior. A direct function test is insufficient when framework registration or lifecycle is the suspected mechanism.

## Verification and limits

Verify the reported failure and healthy neighboring behavior through the framework boundary. Cover the relevant failure, cleanup, retry, or concurrency case when implicated. Use the project's existing test setup and matching dependencies/providers. Treat these questions as heuristics; confirm exact-version behavior from official documentation, resolved implementation, or a matching experiment. Neither the framework name nor a passing isolated test establishes the incident's cause.
