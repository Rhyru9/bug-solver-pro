# Java debugging

Official language/runtime documentation: [Java learning and API navigation](https://dev.java/learn/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the Java portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect pom.xml or Gradle configuration, resolved dependencies, JDK, build artifact, and JVM launch options. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Are boxed/null values, equality/hash behavior, decimal scale, or mutable keys involved? Which object owns shared state?
- **Execution and lifecycle:** Which executor/thread and transaction context execute the effect? Are futures observed and resources closed on error or cancellation?
- **Discriminator:** Use the executing artifact and matching JDK; record thread, object, connection, and transaction identity across the failing path.

## Framework modules

- [Spring](frameworks/spring/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
