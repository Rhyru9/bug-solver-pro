# C# / .NET debugging

Official language/runtime documentation: [C# guide](https://learn.microsoft.com/en-us/dotnet/csharp/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the C# / .NET portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect project/solution files, global.json, resolved packages, target framework, and deployed runtime/configuration. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Are nullability assumptions, value/reference copies, equality, decimal conversions, or deferred enumeration changing the result?
- **Execution and lifecycle:** Who awaits each Task and owns its cancellation token? Does a service or database context outlive its scope or run concurrently?
- **Discriminator:** Replay using the same target/runtime and provider; observe enumeration time, service scope, task completion, and disposal.

## Framework modules

- [ASP.NET Core](frameworks/aspnet-core/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
