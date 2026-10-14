# 17. Structured diagnostic tooling

Use when searching unclear symptoms with the bundled catalog.

## Layers

| Layer | Resource | Responsibility |
|---|---|---|
| Workflow | `SKILL.md` | Decide investigation depth and interpret evidence |
| Catalog | `data/patterns.json` | Structured candidate mechanisms and discriminating checks |
| Open-world angles | `data/angles.json` | Trigger, question, observation and references independent of catalog fit |
| Retrieval | `scripts/core.py` | Schema validation and BM25 lexical ranking |
| CLI | `scripts/search.py` | Human-readable search or JSON; optional investigation plan |
| Framework context | `scripts/frameworks.py` | Discover local module folders and load explicitly selected working knowledge independently of ranking |
| Framework recipe data | `data/frameworks/<language>/<framework>/recipes.json` | Stable IDs, domains, keyword aliases and exact Markdown-section routes |
| Recipe retrieval | `scripts/recipe_index.py` | Validate owner/heading/completeness and retrieve source-owned working knowledge |
| Validator | `scripts/validate_data.py` | Reject incomplete records, incorrect labels and broken references |
| Detail | `references/*.md` | Read applicable reasoning guidance on demand |
| Working notes | `templates/*.md` | Optional records of the actual investigation |

The paths above are relative to the installed skill. Repository development tests live outside the skill in `tests/` and are not required to use it.

## Data contract

Schema version 1 has a `patterns` array. Each record has:

| Field | Meaning |
|---|---|
| `id`, `domain`, `title` | Stable identity, one of eleven declared domains, readable pattern name |
| `signals`, `keywords` | Observable symptoms and English lexical aliases |
| `mechanism` | Candidate failure mechanism requiring application evidence |
| `experiment` | Safe isolated discriminator to adapt to the actual system |
| `falsifies` | Observation that would contradict the candidate in the inspected boundary |
| `verification` | Post-fix checks for the candidate mechanism |
| `limits` | Conditions and alternative explanations restricting applicability |
| `references` | Provenance and detailed guidance inside the bundled references folder |
| `evidence_kind` | `heuristic` for all seed records; never a fabricated verified incident |

The catalog is an index into existing reasoning guidance, not a version-specific framework manual. The entries were curated from this skill's references; their completeness and causal effectiveness have not been established. Actual cases belong in [learned cases](learned-cases.md) only with traceable evidence and maintenance authorization. They are not automatically appended to this catalog.

Angle schema version 1 has an `axes` array. Each record contains a stable `id`, routed `domains`, an observable `trigger`, a diagnostic `question`, an `observation` to seek, and local `references`. Validation requires all eleven domains to be routed and rejects duplicate domains/references. The twenty angles include probe validity, multiplicity, composed guarantees, topology budgets, query semantics and population history. They are questions, not recorded incidents, mandatory tasks or a closed taxonomy of bugs.

## Per-framework data contract

Each index is `data/frameworks/<language>/<framework>/recipes.json`, schema version 1, with `language`, `framework`, and a nonempty `recipes` list. Every recipe contains exactly `id`, `domain`, `keywords`, `references`, `heading`, and `evidence_kind`. IDs are globally unique lowercase hyphenated identifiers; domains use the same eleven diagnostic domains; evidence remains `heuristic`. Keep IDs stable when editing wording and do not recycle them for a different mechanism.

`references` contains one owning framework `playbook.md` or `boundary-case.md`. `heading` is the exact ATX heading, including its Markdown prefix and any recipe number. The reader ignores headings inside fenced examples and rejects missing, ambiguous or empty sections. Every numbered playbook recipe and the optional boundary case must be indexed exactly once. Metadata must match the framework/language directories containing `recipes.json`, and indexed owners must match discovered framework modules. A new module therefore needs its data file before package validation succeeds.

Markdown owns title/content and supporting contracts. JSON owns retrieval metadata; it does not duplicate mechanisms/experiments/repairs. Current indexes route 88 techniques across 22 files. Strict JSON loading rejects duplicate object keys instead of silently replacing evidence. Local validation detects structural/source drift, not semantic truth, live URL reachability or empirical effectiveness. Findings and bounded runtime evidence are in the [data audit](coverage/data-audit.md).

## Query and output contract

Run the installed script using its absolute path from the project under investigation. Use `python3`, or the available equivalent (`python` / `py -3`) if it meets the version requirement. No network access or third-party libraries are needed.

```bash
python3 "<skill-root>/scripts/search.py" "payment committed timeout" --domain concurrency --plan
python3 "<skill-root>/scripts/search.py" "memory retained listeners" -n 2 --json
python3 "<skill-root>/scripts/search.py" "unrecorded boundary failure" --explore --json
python3 "<skill-root>/scripts/search.py" "transaction pool stall" --framework "Spring Boot" --plan --json
python3 "<skill-root>/scripts/validate_data.py"
```

Retrieval searches titles, symptom signals, keywords and mechanisms. Generic terms such as `bug`, `error`, and `fix` are excluded; experiment boilerplate does not influence matching. Domain filtering never silently falls back to another domain. This is token-based retrieval, with no embeddings, automatic stack detection, full translation or arbitrary synonym understanding.

Every CLI query also searches the framework recipe indexes, returning a separate `framework_matches` result with its own `status`, `results`, lexical scores/coverage, source headings and content. Without a framework flag this spans all indexed modules and does not assert that the application uses a matched framework. `--framework` filters recipe leads before the result limit; term rarity remains based on the complete recipe index. Human output prints matched sections, while weak leads remain labeled source routes; JSON includes source-owned content with explicit match quality. Recipe leads never become shared-plan hypotheses automatically.

`--framework` also adds `framework_context` containing module identity, relative local resource paths, full playbook text and an optional deeper boundary case. Common display names such as `Next.js`, `NestJS`, `ASP.NET Core`, and `Spring Boot` have aliases. New canonical module folders take precedence over an older alias. Unknown/ambiguous names or invalid/missing data fail with exit 2 and no partial stdout. The option does not filter the shared catalog or change its status/hypotheses. A shared `no_match` can coexist with a `matched` recipe lead. Relative data paths/content are read from the installed skill, not the project cwd; no network is used.

`--plan` adds context to establish, candidate hypotheses marked `ASSUMED` for sufficiently matched results, discriminating experiments, falsifying observations, verification and a next step. Empty or weak retrieval instead adds observation angles without fabricated hypotheses. `--explore` always adds those angles and leaves the hypothesis list empty, even when the query matches familiar patterns. These modes write no investigation files, execute no experiments, and invent no observed results. Save output in authorized project working notes only if useful; do not write private incidents into a globally installed skill.

Shared JSON search and `framework_matches` each report their own `matched`, `weak_match` or `no_match` status, unmatched query terms and per-result `match_quality`. A single meaningful term or at most 50% token overlap marks a result weak; each search status follows its leading result. Even with a sufficiently matched shared result, weak secondary results remain leads and are excluded from the plan's hypotheses. Recipe matches are never automatically promoted. These conservative lexical rules are not a causal-confidence model. Valid weak/no-match queries exit 0; invalid input or malformed/missing data exits 2. Query coverage describes token overlap, not semantic fit. Reject irrelevant results and map the actual flow; do not present a leading result as an established cause.

## Catalog checks in the installed skill

`scripts/validate_data.py` rejects incomplete catalog records and broken local references. Adding patterns, retrieval tests, and repository checks is documented in the source [contributor guide](https://github.com/Rhyru9/bug-solver-pro/blob/main/.github/CONTRIBUTING.md). Those tests evaluate tooling behavior, not whether an agent diagnoses a real bug correctly.

## Gaps closed and remaining

| Previous gap | Implemented support | Remaining limit |
|---|---|---|
| Manual browsing only | Searchable structured catalog with reference routing | Small seed catalog; lexical matches can be incomplete or irrelevant |
| Symptom leads straight to a guessed fix | Experiment/falsifier per pattern; weak matches are not promoted automatically | Real source inspection and causal evidence still required |
| Bug is absent from the catalog | Twenty observation angles and `--explore` mode | Actual artifacts still decide relevant and previously unlisted questions |
| No composed investigation guidance | `--plan` output with explicit uncertainty | No automatic stack-specific runtime instrumentation |
| Data could silently drift | Strict schema and reference validation | Provenance checks are local, not independent empirical validation |
| Search relevance untested | Ranking, no-match, domain and copied-install tests | No realistic agent effectiveness benchmark yet |
| Agent-specific script path assumptions | Resolve data beside the installed script | Installed hosts still require their native discovery and permissions |
| Framework techniques absent from CLI output | Explicit `--framework` loads local playbook and boundary case separately from ranking | No automatic stack identification or recipe-level semantic retrieval |
| Passing untriggered probes treated as rejection | Plan context and causal-decision reference require applicable, activated, sensitive, comparable probes | Tool text cannot establish application-level evidence by itself |
| Missing timeout looked like no matches | Shell scan dependency/error failures are explicit | Shell helpers still require their documented tools |
| Hidden credential files entered scan output | Scan and usage search skip `.env`, `*.pem`, and `secret`/`credential` names | Other sensitive filenames can still match if they use ordinary names |

Expand stack-specific guidance for demonstrated gaps with authoritative contracts, version scope, concrete discriminators and repair tradeoffs. Keep techniques distinct from verified incident cases and route them through local modules. The [gap audit](coverage/gap-audit.md) tracks current evidence and remaining limits. For effectiveness testing, use raw held-out artifacts and independent correctness oracles, then measure diagnosis, regressions, scope and investigation cost.
