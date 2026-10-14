# Data, retrieval and validation audit

This follow-up inspects the data layer and its consumers, rather than counting documentation modules. It extends the [skill gap audit](gap-audit.md). Results below concern specific repository behavior and bounded fixtures; they do not establish general diagnostic effectiveness.

## Demonstrated gaps and implemented corrections

| Finding | Before | Correction and current check |
|---|---|---|
| Framework knowledge missing from searchable data | 88 local techniques existed only as Markdown; explicit `--framework` dumped a module but did not retrieve recipes | 22 JSON indexes under `data/frameworks/<language>/<framework>/recipes.json` route all 88 techniques to exact local sections; CLI searches them with or without a declared framework |
| New reasoning absent from data references | None of 48 shared patterns referenced causal decision gates or composed-failure guidance | Existing records now route to causal gates and relevant composition guidance; six specific shared mechanisms add dedicated discriminators |
| Observation axes lagged behind workflow | 14 angles did not explicitly address probe validity, multiplicity, composed guarantees, topology budgets, query semantics or data population history | Six added axes and references produce 20 angles; domain-filtered exploration remains questions-only |
| JSON could silently overwrite evidence | Default JSON loading accepted duplicate object keys | Shared strict loader rejects duplicate keys, including nested objects, for catalogs, indexes and package manifests |
| Weak integrity checks | Duplicate references/domains, renamed headings, cross-framework targets and omitted recipes could escape detection | Validators reject these, owner/path mismatches, duplicate recipe IDs/sections, ambiguous/empty sections and unsupported evidence labels |
| Passing retrieval tests covered mostly nearby wording | Existing generic tests did not exercise unreachable framework symptoms or realistic weak controls | Regression queries cover the demonstrated misses; broad/unrelated queries remain weak/no-match and are not converted into hypotheses |
| Data correctness tested only as text | No executed fixture distinguished joined rows from entity grain or explicit null policy | In-memory SQLite probe demonstrates fan-out, a wrong DISTINCT repair, null-containing exclusion and an empty-set control |

## Before/after retrieval evidence

Before changes, shared search returned `no_match` for `body signature whitespace` and `filtered include navigation fixup`, and weak unrelated leads for the other two queries below. Current CLI reports shared-catalog status separately from local recipe matches.

| Query | Current leading local technique | Source of truth |
|---|---|---|
| `body signature whitespace` | `express-boundary` | [Express bytes/parser case](../languages/javascript-typescript/frameworks/express/boundary-case.md) |
| `component key reorder draft` | `react-boundary` | [React identity case](../languages/javascript-typescript/frameworks/react/boundary-case.md) |
| `filtered include navigation fixup` | `aspnet-core-boundary` | [EF Core graph case](../languages/csharp/frameworks/aspnet-core/boundary-case.md) |
| `runtime dto metadata validation` | `nest-boundary` | [Nest runtime DTO case](../languages/javascript-typescript/frameworks/nest/boundary-case.md) |

These are curated regression queries, not held-out benchmarks. For `body signature whitespace`, shared status can remain `no_match` while recipe status is `matched`; `--plan` and `--explore` still invent no shared hypothesis. A recipe match is a lexical lead requiring actual applicability checks.

## Data ownership and drift controls

Markdown owns mechanisms, experiments, repair tradeoffs and supporting contracts. JSON owns stable recipe IDs, diagnostic domain, keyword aliases and an exact source heading. Titles/content are read from that source; the index does not duplicate the full recipe. For examples, inspect [Express data](../../data/frameworks/javascript-typescript/express/recipes.json) and [Django data](../../data/frameworks/python/django/recipes.json).

Every numbered playbook recipe and optional boundary case must be indexed exactly once. Metadata owner must match the file path and reference owner. Adding a module without its index, removing a source heading, or omitting one recipe fails validation rather than silently reducing retrieval coverage. Code-fenced example headings cannot become retrieval boundaries. Source/structure validity still does not prove semantic quality.

## Executed data-semantics fixture

The standard-library [SQL probe](../../scripts/probes/sql_query_semantics.py) used in-memory SQLite 3.53.4. Three orders have amounts 100, 100 and 30; joined IDs are 1, 1, 1, 2, 3. The naive joined sum is 430, SUM(DISTINCT amount) is 130, and the correct one-row-per-order sum is 230. This exposes both the original fan-out and a tempting incorrect repair.

NOT IN against a set containing 2 and null selects no candidate IDs; removing null selects ID 1. An empty exclusion set admits all candidates, including the null candidate in this fixture. An explicit non-null identity policy selects ID 1 for the original exclusion data. These observations support the bounded SQL cases; they do not establish production isolation, provider/ORM behavior, or a universal null policy.

## Remaining limits

Retrieval is lexical: no embeddings, full translation, natural-language negation understanding or automatic stack detection. Scores and query coverage are not causal confidence. Candidate domains are curated and may need revision when actual tasks expose a routing mistake. New generic mechanisms and most framework techniques are not runtime-validated here; the SQL and previously recorded FastAPI probes are narrow synthetic checks. Remote contract/version drift and independent agent effectiveness remain separately tracked.
