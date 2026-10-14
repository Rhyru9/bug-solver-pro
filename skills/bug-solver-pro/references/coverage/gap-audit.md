# Skill coverage audit

Audit scope: the current skill, its 22 framework modules, local retrieval, and reasoning instructions. This is a maintained gap record, not a claim to cover every language, provider, version, or bug. Update a row when new evidence changes the assessment; do not convert recipe counts into effectiveness scores.

The follow-up [data/retrieval audit](data-audit.md) inspects shared catalogs, per-framework indexes, source completeness, corruption handling and bounded SQL fixtures. Use it alongside this framework/reasoning review.

## Evidence vocabulary

- **Implemented:** the local instruction or tool path exists.
- **Tool-tested:** repository tests execute that tool behavior with independent output expectations.
- **Contract-backed:** official documentation/source supports the described framework mechanism; it does not prove a real incident or a matching project version.
- **Runtime-unvalidated:** no matching application/runtime reproduction was executed in this audit.
- **Synthetic-runtime-checked:** a bounded local fixture exercised the specified runtime/contract; this is narrower than incident reproduction or deployment validation.

Authored examples and probes remain heuristics. Synthetic interaction cases are explicitly labeled. Package tests do not establish that an agent will diagnose an unseen production bug correctly.

## Findings and closure

| ID | Evidence of the gap | Implemented correction | Evidence and residual limit |
|---|---|---|---|
| G01: false rejection | Several recipes used a non-failure as a falsifier without requiring overlap, actual branch execution, or a sensitive observer | [Causal decision gates](../19-causal-decision-procedure.md), plan context, entrypoint principle, and a stricter Symfony redelivery probe | Implemented; a gate still requires application evidence, not a ticked checklist |
| G02: isolated-component bias | Base playbooks mostly considered one mechanism; proxy/transaction fixes, cache/authority, and cleanup/task interactions could remain unexplained | [Composed-failure guide](../20-composed-failures.md), controlled interaction matrix, five worked synthetic cases | Implemented; examples are not runtime reproductions or an exhaustive interaction catalog |
| G03: knowledge not surfaced by tooling | Original search ranked only `data/patterns.json`; framework recipes/cases were absent from output | Explicit context plus per-framework indexes retrieve exact source sections separately from shared ranking | Tool-tested for aliases, lexical recipe ranking/filtering, copied installs, corruption, no-match/explore behavior and extracted ZIPs; no automatic stack detection or semantic understanding |
| G04: shallow framework coverage | Three base recipes per framework omitted specific high-impact boundary traps | Twenty-two [boundary cases](#framework-boundary-review) with applicability, discriminators, repair tradeoffs and contracts | Contract-backed and routed locally; one FastAPI output case has a synthetic runtime probe, other framework cases remain runtime-unvalidated |
| G05: independent-oracle gap | Correct SQL, managed objects, responses and durable commits could be treated as interchangeable evidence | EF/Doctrine cases and causal guide require comparison at the first divergent representation and an independent read path | Implemented; oracle choice still depends on the application's consistency/transaction contract |
| G06: deployment/topology budget | Per-request/per-process sharing and pool limits did not establish cross-worker/replica behavior | Spring nested-transaction and Actix worker-pool cases plus identity/work-count techniques | Contract-backed; no production capacity or performance baseline claimed |
| G07: fragile extension | Link checks alone could accept a new docs-only framework module or omit it from retrieval | Package checks require working resources plus matching complete data indexes and source headings | Tool-tested structural/source integrity; these checks do not assess semantic quality |
| G08: validation overstated by counts | Prior test counts described packaging/retrieval, not framework bug-solving effectiveness | Evidence vocabulary here and explicit distinction in skill/README/reporting guidance | Closed as a reporting correction; independent agent/runtime effectiveness evaluation remains open |

## Framework boundary review

Each row identifies a concrete omission in the base playbook and the new local case that addresses it. Read only rows relevant to the failing path; none is a mandatory whole-project audit.

| Framework/library | Previously missing boundary case | Evidence |
|---|---|---|
| Express | [Webhook signature fails only through the full middleware stack](../languages/javascript-typescript/frameworks/express/boundary-case.md) | Contract-backed; runtime-unvalidated |
| NestJS | [ValidationPipe is installed but malformed DTOs still pass](../languages/javascript-typescript/frameworks/nest/boundary-case.md) | Contract-backed; runtime-unvalidated |
| React | [Editing the second row changes the first row's draft](../languages/javascript-typescript/frameworks/react/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Next.js | [A hidden button still allows a server-side mutation](../languages/javascript-typescript/frameworks/nextjs/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Django | [get_or_create still inserts duplicates under concurrency](../languages/python/frameworks/django/boundary-case.md) | Contract-backed; runtime-unvalidated |
| FastAPI | [A supposedly filtered response exposes extra fields on one route](../languages/python/frameworks/fastapi/boundary-case.md) | Contract-backed; synthetic-runtime-checked for the versions below |
| Flask | [Two successful requests lose one session update](../languages/python/frameworks/flask/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Laravel | [Adding an orWhere widens a tenant-scoped query](../languages/php/frameworks/laravel/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Spring | [REQUIRES_NEW causes a stall only under load](../languages/java/frameworks/spring/boundary-case.md) | Contract-backed; runtime-unvalidated |
| ASP.NET Core | [Filtered Include returns entities outside the filter](../languages/csharp/frameworks/aspnet-core/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Gin | [A second binder sees EOF although the request body was valid](../languages/go/frameworks/gin/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Rails | [A stale edit silently replaces a newer one](../languages/ruby/frameworks/rails/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Vue | [Reading a computed sort changes another component's list](../languages/javascript-typescript/frameworks/vue/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Nuxt | [Authenticated API works in the browser but fails during SSR](../languages/javascript-typescript/frameworks/nuxt/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Svelte | [An effect ignores a value read after await](../languages/javascript-typescript/frameworks/svelte/boundary-case.md) | Contract-backed; runtime-unvalidated |
| SvelteKit | [Enhanced form succeeds but the page does not update](../languages/javascript-typescript/frameworks/sveltekit/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Angular | [An interceptor changes the payload on a retried request](../languages/javascript-typescript/frameworks/angular/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Hono | [Validator works but a later raw Request read fails](../languages/javascript-typescript/frameworks/hono/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Symfony | [Repository read appears to prove a write that never reached the database](../languages/php/frameworks/symfony/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Echo | [Client disconnects but downstream calls keep consuming resources](../languages/go/frameworks/echo/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Axum | [Adding authentication changes unknown URLs from 404 to 401](../languages/rust/frameworks/axum/boundary-case.md) | Contract-backed; runtime-unvalidated |
| Actix Web | [Increasing HTTP workers exhausts database connections](../languages/rust/frameworks/actix-web/boundary-case.md) | Contract-backed; runtime-unvalidated |

## Bounded runtime evidence

Executed [FastAPI ASGI probe](../../scripts/probes/fastapi_response_filter.py): Python 3.14.7, FastAPI 0.135.3, Pydantic 2.12.5, Starlette 1.0.0. Normal output filtering removed a synthetic extra field; a direct JSONResponse retained it; the explicit output-DTO repair removed it. All three HTTP statuses were 200. This demonstrates why status-only assertions miss the contract violation. The probe has a negative control and repair comparison, is reproducible with existing dependencies, and uses no server/network or production inputs. An optional repository test executes it when FastAPI is installed and otherwise skips without installing dependencies.

No runtime result is claimed for the other framework cases, all original base recipes, unseen agent reasoning, middleware/network deployment, or other package versions. Optional framework checks and standard-library tooling checks are distinct validation layers.

## Remaining gaps and how to handle them

| Remaining gap | Current fallback | Evidence needed to extend coverage |
|---|---|---|
| Exact-version/provider/runtime reproductions across frameworks | Check actual versions/providers, inspect the cited contract and local implementation, run a bounded matching probe | Failing-before/passing-after behavior, activated trigger and independent healthy/error controls |
| Unlisted frameworks and languages, native/runtime internals | [Stack semantics](../14-stack-semantics.md), [open-world investigation](../18-coverage-and-unknowns.md) | A consequential repeated gap or concrete workflow need, with a useful discriminating technique |
| Third-party integrations such as ORM adapters, queues and auth providers | Follow the actual integration path and owning contract; do not infer from framework name | Provider/version/configuration, real boundary behavior, and fault/cleanup observations |
| Unseen agent effectiveness and investigation cost | Review evidence quality and scope on actual tasks; do not infer from tool tests | Raw held-out artifacts, independent oracle, observed diagnosis/fix/regression outcomes and cost |
| External URL drift and official documentation defaults | Follow version selection/local sources via the [docs workflow](../framework-documentation.md) | Recheck the changed page/tag; repository package checks validate local resources only |
| Lexical synonym/language limitations and recipe discovery | Curated keyword indexes, explicit framework aliases, recipe content and full module context; manually reject unrelated leads | Representative queries and negative controls before adding semantic ranking/automatic detection |

A remaining broad category is not automatically a blocking defect in a particular bug fix. Expand when an actual artifact exposes a decision-changing uncertainty. Preserve existing working techniques; reject speculative additions that merely rename a shared question.
