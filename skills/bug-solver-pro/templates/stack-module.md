# Stack module authoring template

Use this structure when adding a maintained module under [language modules](../references/languages/index.md). Replace the authoring prompts with concrete questions and experiments before linking a new module.

## Scope and parent

Name the language/framework and the boundary where this module applies. Link the parent language guide (for frameworks), module index (for languages), and shared stack-semantics workflow using paths relative to the new file.

## Establish the executing stack

List the manifests, resolved dependencies, runtime/build settings, configuration, and registrations that distinguish the executing path from source intent or a test double.

## Diagnostic questions

Describe stack-specific value, ownership, lifecycle, scheduling, persistence, or integration questions that change debugging decisions. Keep shared mechanisms in shared references. Avoid version-independent claims about configurable defaults.

## Local debugging playbook

Create `playbook.md` beside the guide. Include concrete framework-specific recipes: recognizable failure signature, causal mechanism with prerequisites/version scope, a local probe and expected observation, an observation rejecting the mechanism, repair options/tradeoffs, and regression verification. Add a small implementation pattern when it removes ambiguity. Link the supporting official contract at the recipe. Do not label an authored technique as a verified incident or require a fresh manual-reading step before applying every probe. A generic question list or documentation directory is insufficient.

Interpret falsifiers through the causal decision gates: applicability, actual trigger activation, observation sensitivity and comparable state. Include an inconclusive outcome when a probe cannot activate or observe the suspected mechanism. Use `boundary-case.md` for a deeper trap needing its own prerequisites, competing outcomes and unsafe-fix warning; link it from the playbook/guide. The framework CLI loads it automatically when present. Consult the coverage audit before duplicating an existing technique and record the evidence level of a claimed gap closure.

## Distinguishing experiment

Describe a safe experiment at the implicated real boundary, its predicted observation, and a result that rejects the candidate mechanism. Do not prescribe a fix before collecting evidence.

## Official documentation map

For a framework, create `docs.md` beside `guide.md` and `playbook.md` and cross-link them. Use docs to support the techniques and resolve unknown contracts/version changes, not as a substitute for the playbook. Include verified direct official website URLs, topic-selection guidance, version selection, and any official source alternative needed for access failures. Link the shared documentation access workflow. For a language, include its official language/runtime documentation in the guide. Verify URLs when authoring; local package checks do not check remote availability. Avoid assuming a `latest`, `current`, or `main` source matches the installed version.

## Verification and limits

Describe checks for the failing trigger, healthy behavior, and relevant partial failure or cleanup. Identify test-double/provider/build limitations. Record exact versions and authoritative evidence for retained semantic conclusions.

## Integrate the module

Link a language from the module index; link a framework from the language index, dedicated framework index, and its parent language guide. Run `scripts/check_package.py` from the repository root to check recursive links. Do not create empty directories for planned support.

Create `data/frameworks/<language>/<framework>/recipes.json` using the per-framework data contract in structured tooling. Index every numbered recipe and optional boundary-case title exactly once with stable IDs, the relevant diagnostic domain, useful symptom aliases, one owning reference and its exact heading. Do not duplicate the recipe text into JSON. Update the index when renaming source headings or adding/removing recipes; validators detect omissions and stale routes. Add representative retrieval queries and confusing/irrelevant controls when extending coverage. The CLI discovers the new data file without a hardcoded registry entry.
