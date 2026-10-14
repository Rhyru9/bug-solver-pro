# Go debugging

Official language/runtime documentation: [Go documentation](https://go.dev/doc/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the Go portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect go.mod, go.sum, toolchain/build flags, executable, and service launch environment. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Are interface values hiding nil, slices sharing storage, map entries missing, or value copies sharing pointers? Where is state owned?
- **Execution and lifecycle:** Which goroutine closes each channel and observes each error? Do cancellation and return release goroutines, response bodies, rows, and locks?
- **Discriminator:** Minimize the failing operation and track goroutine/resource ownership; use the project's race-enabled checks when shared-memory evidence warrants them.

## Framework modules

- [Echo](frameworks/echo/guide.md): use when this framework owns the failing boundary.

- [Gin](frameworks/gin/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
