# JavaScript / TypeScript debugging

Official language/runtime documentation: [Node.js runtime API](https://nodejs.org/api/); [TypeScript compiler and language](https://www.typescriptlang.org/docs/). Match the executing version using the [documentation access workflow](../../framework-documentation.md).

Use for the JavaScript / TypeScript portion of the failing path. Start with [module selection](../index.md); apply the shared [stack-semantics workflow](../../14-stack-semantics.md) to versions or dependencies not covered here.

## Establish the executing stack

Inspect package.json, the active lockfile, tsconfig files, runtime launch flags, and emitted JavaScript/source maps. Compare the failing process with the test process before interpreting different outcomes.

## Questions that change the investigation

- **Values and ownership:** Is the failure in source or emitted code? Are values coerced, missing, null, or precision-sensitive? Which objects are shared across requests?
- **Execution and lifecycle:** Which promises are awaited or detached? Where are rejections observed? Does cancellation stop the work or only the caller?
- **Discriminator:** Replay the same input through the built entrypoint; capture value types and a task timeline around the first incorrect boundary.

## Framework modules

- [Vue](frameworks/vue/guide.md): use when this framework owns the failing boundary.
- [Nuxt](frameworks/nuxt/guide.md): use when this framework owns the failing boundary.
- [Svelte](frameworks/svelte/guide.md): use when this framework owns the failing boundary.
- [SvelteKit](frameworks/sveltekit/guide.md): use when this framework owns the failing boundary.
- [Angular](frameworks/angular/guide.md): use when this framework owns the failing boundary.
- [Hono](frameworks/hono/guide.md): use when this framework owns the failing boundary.

- [Express](frameworks/express/guide.md): use when this framework owns the failing boundary.
- [NestJS](frameworks/nest/guide.md): use when this framework owns the failing boundary.
- [React](frameworks/react/guide.md): use when this framework owns the failing boundary.
- [Next.js](frameworks/nextjs/guide.md): use when this framework owns the failing boundary.

## Verification and limits

Use the project's existing runner. Verify the original trigger, a healthy neighboring case, and the error/cleanup path implicated by the mechanism. Include matching build/worker modes when they affect the failure. These are investigation questions; establish version-specific behavior from resolved source, exact-version official documentation, or an isolated matching experiment before applying a fix.
