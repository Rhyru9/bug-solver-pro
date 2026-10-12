# 11. Symptoms → Possible Causes

Quick investigation prompts. Each row is a **hypothesis to test**, not a conclusion.

| Symptom | Possible causes | Quick check |
|---|---|---|
| Intermittent success/failure | Races, stale caches, async order, particular data, retries/duplicates, instance differences | Compare successful/failing requests (data, time, instance); repeat parallel runs |
| Works locally, fails in production | Config/env/flag differences, dependencies, legacy data, volume/concurrency, time zones, permissions | Compare config/versions; use authorized isolated fixtures/data copies |
| Appears after deployment | Code/migration/config changes, deployment order, old cache formats, rolling deployment | Compare healthy/failing deployments; inspect migration order |
| Duplicate data | Missing unique constraints, check-then-act, retries without idempotency, duplicate jobs/submissions | Find duplicates and associated request/job traces |
| Missing/invisible data | Soft-delete/tenant/status filters, rollback, lagging replicas, caches, silent job failures, unstable pagination | Compare primary sources and filters using test data/authorized access; inspect job logs |
| Incorrect numbers/totals | Double calculation, float/rounding, joins multiplying rows, units, operation order, legacy data | Calculate independently from raw data; inspect joins |
| Unexpected nulls | Optional fields, DTO/entity mapping, left joins, legacy data, serialization, missing defaults | Find where values first become null |
| Stuck statuses | Unvalidated transitions, uncompensated job failures, partial failures, lost events | Inspect status history and job logs |
| User A's data visible to user B | Missing tenant scope, cache keys lacking user/tenant, global/singleton state | Inspect queries/cache keys; reproduce with two tenants |
| Duplicate/missing email or notifications | Dispatch inside transactions, retries, duplicate listeners, rollback, inactive queues | Trace triggers and queue logs |
| Dates shift by a day / incorrect time | Time zones, DST, dates versus datetimes, parsing | Inspect UTC/local values across layers |
| Frontend fails after backend changes | Changed fields/types/error codes/order | Compare old/new responses |
| Tests pass but real bugs remain | Excessive mocks, unrealistic fixtures, untested failure paths | Test the relevant path without replacing the failing boundary with mocks |
| Flaky tests | Time, order, shared test state, races, residual data | Repeat, randomize order, isolate data |
| Sudden slowness | N+1, missing/unused indexes, locks, data growth, mass cache misses, retry storms | Inspect query plans and query counts |
| Memory keeps growing | Unbounded caches, retained listeners, leaked goroutines/promises, open connections | Profile heap; count connections/handles |
| DB deadlocks/timeouts | Inconsistent lock order, long transactions, bulk updates | Inspect wait/lock graphs, transaction scope, lock order |
| Fix A introduces bug B | Hidden coupling, incorrect diagnosis, conflicting rules | Follow `04-anti-fix-chain.md` |
| Fixed bug returns | Symptom-only fix, missed related bugs, branch drift, corrupted legacy data | Search related patterns; inspect data/branches |
| Different endpoints disagree | Duplicate logic, different filters/caches/data sources | Compare code paths and queries |
| Webhook/job executes twice | At-least-once delivery, retries, cron on multiple instances, missing dedupe | Inspect IDs/dedupe keys, schedules, instance counts |
| **No matching row** | Incomplete catalog | Map invariants/boundaries; discover semantics in `14`, experiments in `15`, research in `13` as needed |

## Usage

1. Choose matching rows; multiple matches are possible.
2. Turn proposed causes into hypotheses using `02-root-cause-analysis.md`.
3. Run discriminating checks; reject a prediction contradicted by sufficiently reliable observations. Missing/ambiguous evidence → INCONCLUSIVE, not automatically REJECTED.
4. Do not stop at the first plausible row.
