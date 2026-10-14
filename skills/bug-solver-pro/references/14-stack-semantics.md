# 14. Discover the Semantics of the Actual Stack

Use when languages, frameworks, libraries, runtime modes, or versions are unfamiliar. Build enough of an execution model to diagnose the bug; a list of languages does not limit this skill's scope.

For maintained stack-specific questions, select a language and its framework modules from the [module index](languages/index.md). Read only modules implicated by the failing path. Use this workflow for shared semantic discovery and stacks without a module.

## Start with the actual system

Manifests express intent; lockfiles, installed packages, build artifacts, and running processes provide different evidence. Record relevant versions/features, build modes, OS/architecture where influential, effective configuration, and process topology. Ensure tests and incidents execute the code being compared. Consider code generation, transpilation, plugins, wrappers, vendor patches, and configuration changing defaults.

Do not install the newest version or switch toolchains merely to simplify diagnosis before understanding the environment being repaired. Use existing project runners and test patterns.

## Turn mechanisms into questions

Choose dimensions involved in the bug; not every dimension requires inspection.

| Dimension | Semantic questions | Evidence to seek |
|---|---|---|
| Values and representation | How are missing, null, empty, zero, and invalid distinguished? Coercion, overflow, precision, units, encoding? | Type/schema declarations plus values before/after conversion |
| Ownership and mutation | Copied or shared? Who may mutate? Is the reference still alive? | Aliasing/mutation paths, lifetime, ownership boundaries |
| Scope and lifecycle | Per operation, request, session, thread, or process? When reset/disposed? | Dependency registration, initialization, cleanup |
| Execution and scheduling | Eager/lazy? Blocking/nonblocking? When do tasks start, finish, or cancel? | Call graphs plus timelines/happens-before, not timestamps alone |
| Errors and cancellation | Thrown, returned, represented as values, or deferred? Who observes them? What does cancellation stop? | Function contracts plus failure/cleanup traces |
| Persistence and atomicity | Which operations share connections/transactions? Commit, acknowledgment, durability points? | Transaction/connection identity plus state at failures |
| Integration and formats | Serialization, validation, unknown-field, framing, pagination, and versioning defaults? | Actual boundary payloads plus producer/consumer contracts |
| Resources and backpressure | Who acquires/releases handles, buffers, locks, connections? Queue/concurrency limits? | Resource profiles, pools/queues/timeouts, failure cleanup |
| Metaprogramming and extensions | Where do hooks/proxies/decorators/reflection/generated code change flow? | Registration, resolved source, hook order |
| Build and configuration | Which semantics change with compiler modes, flags, dependency resolution, locale/config? | Artifacts and effective configuration, not source config alone |

## How to answer

1. State requirements neutrally, such as “each request has its own state” or “check and update must be atomic.”
2. Discover how the actual stack provides that guarantee and under which prerequisites. Similar API names do not imply equivalent semantics.
3. Inspect exact-version docs and the implementation path actually called. If unclear, run a small isolated experiment with matching versions/configuration.
4. Bring results back to application flow: proven library semantics do not automatically establish the application's bug cause.
5. Record unanswered assumptions and consequences. Do not fill irrelevant dimensions with guesses.

## Change tools without changing the objective

Text searches find candidates; language servers/call hierarchies assist static binding; debuggers/tracing reveal dynamic paths; schemas/registries reveal consumers outside code. Source maps/debug symbols connect artifacts with source. Choose available tools and state their blind spots.

During application debugging, do not add every newly encountered framework to the skill. When skill maintenance is authorized, extend the appropriate language/framework directory using the [module index](languages/index.md) and [module template](../templates/stack-module.md). Retain incident lessons as mechanism + prerequisites + evidence in authorized learned cases; keep reusable diagnostic questions in the stack module.
