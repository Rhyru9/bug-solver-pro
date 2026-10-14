# Ruby debugging

Official language/runtime documentation: [Ruby documentation](https://www.ruby-lang.org/en/documentation/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the Ruby portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect Gemfile, Gemfile.lock, Ruby implementation/version, and web/job worker startup configuration. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Are mutable constants, shared class state, string/symbol keys, truthiness, or implicit conversions selecting the wrong path?
- **Execution and lifecycle:** When are lazy queries evaluated? Which callbacks and exceptions alter control flow? Is state isolated between reused workers and concurrent requests?
- **Discriminator:** Replay with matching worker mode and dependencies; compare fresh/reused objects and record query, callback, and commit order.

## Framework modules

- [Rails](frameworks/rails/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
