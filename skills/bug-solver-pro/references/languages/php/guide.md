# PHP debugging

Official language/runtime documentation: [PHP manual](https://www.php.net/manual/en/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the PHP portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect composer.json, composer.lock, PHP runtime/extensions, and web/queue worker startup configuration. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Are array keys, null/missing values, numeric strings, or loose comparisons changing the branch? Where are references or serialized values reused?
- **Execution and lifecycle:** Is state scoped to a request or a long-running worker? When are transactions committed and jobs dispatched? Which errors reach the configured handler?
- **Discriminator:** Replay the boundary payload with its original types, then compare a fresh worker with repeated operations in one worker.

## Framework modules

- [Symfony](frameworks/symfony/guide.md): use when this framework owns the failing boundary.

- [Laravel](frameworks/laravel/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
