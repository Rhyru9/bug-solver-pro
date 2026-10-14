# Python debugging

Official language/runtime documentation: [Python language and standard library](https://docs.python.org/3/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the Python portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect pyproject.toml or requirements files, lockfiles, interpreter/virtual environment, and worker launch configuration. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Do mutable defaults, shared class attributes, aliases, or late-bound closures retain state between calls? Is a returned iterator consumed?
- **Execution and lifecycle:** Which calls block the executing worker? Which coroutine/task is actually awaited, cancelled, or observed? Where is a session acquired and released?
- **Discriminator:** Run the failing input in the same interpreter and worker mode; compare fresh versus reused state and record task/session ownership.

## Framework modules

- [Django](frameworks/django/guide.md): use when this framework owns the failing boundary.
- [FastAPI](frameworks/fastapi/guide.md): use when this framework owns the failing boundary.
- [Flask](frameworks/flask/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
