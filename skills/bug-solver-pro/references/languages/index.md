# Language and framework modules

For concrete framework debugging techniques, use the [framework playbook index](../frameworks/index.md). Each framework has `playbook.md` with mechanisms, discriminators, and repair/verification patterns; `guide.md` maps wider boundaries and `docs.md` supports unresolved contracts and version differences.

Select modules from the system actually executing, not only file extensions. Confirm runtime, resolved dependencies, build mode, and worker topology using [stack semantics](../14-stack-semantics.md).

1. Read the relevant language guide below.
2. If the failing path uses a listed framework, open its local playbook from the framework index or guide, and select a recipe matching actual evidence. Combine relevant modules for mixed stacks (for example, Next.js and React), reading only implicated boundaries.
3. Use the shared diagnosis references for causal reasoning, impact, and verification. These modules supply stack-specific questions, not established causes.
4. For an unlisted stack or version, continue with [stack semantics](../14-stack-semantics.md) and [adaptive research](../13-research-adaptive.md). Missing coverage never blocks diagnosis or warrants silently substituting another framework.

| Language | Framework modules |
|---|---|
| [JavaScript / TypeScript](javascript-typescript/guide.md) | [Express](javascript-typescript/frameworks/express/guide.md), [NestJS](javascript-typescript/frameworks/nest/guide.md), [React](javascript-typescript/frameworks/react/guide.md), [Next.js](javascript-typescript/frameworks/nextjs/guide.md), [Vue](javascript-typescript/frameworks/vue/guide.md), [Nuxt](javascript-typescript/frameworks/nuxt/guide.md), [Svelte](javascript-typescript/frameworks/svelte/guide.md), [SvelteKit](javascript-typescript/frameworks/sveltekit/guide.md), [Angular](javascript-typescript/frameworks/angular/guide.md), [Hono](javascript-typescript/frameworks/hono/guide.md) |
| [Python](python/guide.md) | [Django](python/frameworks/django/guide.md), [FastAPI](python/frameworks/fastapi/guide.md), [Flask](python/frameworks/flask/guide.md) |
| [PHP](php/guide.md) | [Laravel](php/frameworks/laravel/guide.md), [Symfony](php/frameworks/symfony/guide.md) |
| [Java](java/guide.md) | [Spring](java/frameworks/spring/guide.md) |
| [C# / .NET](csharp/guide.md) | [ASP.NET Core](csharp/frameworks/aspnet-core/guide.md) |
| [Go](go/guide.md) | [Gin](go/frameworks/gin/guide.md), [Echo](go/frameworks/echo/guide.md) |
| [Rust](rust/guide.md) | [Axum](rust/frameworks/axum/guide.md), [Actix Web](rust/frameworks/actix-web/guide.md) |
| [Ruby](ruby/guide.md) | [Rails](ruby/frameworks/rails/guide.md) |

## Ownership and extension

Keep runtime/value/ownership questions in `<language>/guide.md`. Keep framework registration, lifecycle, hooks, and integration questions in `<language>/frameworks/<framework>/guide.md`. Shared mechanisms belong in the numbered references one directory above. JavaScript and TypeScript share a module because emitted JavaScript and runtime boundaries must be investigated together; identify compiler-specific assumptions explicitly.

To extend coverage, start from the [module template](../../templates/stack-module.md), add a populated language/framework directory, and link it here and from its parent language guide. A framework needs concrete local recipes in `playbook.md`, supporting URLs in `docs.md`, and a row in the framework index. Use lowercase hyphenated directory names. Framework variants with materially different execution models can have separate guides within their framework directory, linked from its guide.

Keep each module focused on concrete debugging mechanisms, discovery evidence, distinguishing experiments, repair patterns, verification, and limits. A playbook must add usable framework-specific techniques; a list of questions and documentation URLs is insufficient. Do not copy manuals or put unrelated stacks in one file. Version-dependent answers require exact-version official documentation, resolved source, or a matching experiment; record versions and evidence for retained conclusions. A new module does not require a new search domain or pattern; add catalog entries only for distinct reusable mechanisms with experiments and falsifiers.

Run the repository package check after changes; it checks local Markdown links recursively, including these nested modules.
