# Rust debugging

Official language/runtime documentation: [Rust documentation](https://doc.rust-lang.org/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the Rust portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect Cargo.toml, Cargo.lock, toolchain, feature flags, target, and deployed binary. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Do clone, shared ownership, interior mutation, numeric conversion, or serialization change the invariant? Does the issue cross an unsafe or FFI boundary?
- **Execution and lifecycle:** Which executor polls each future? Who observes task results and owns cancellation, locks, and cleanup across await points?
- **Discriminator:** Reproduce with matching features/profile; trace ownership and completion around the boundary, including drop and external effects.

## Framework modules

- [Axum](frameworks/axum/guide.md): use when this framework owns the failing boundary.
- [Actix Web](frameworks/actix-web/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
