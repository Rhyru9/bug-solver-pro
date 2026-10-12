# 05. Investigating Inconsistent State

Many bugs involve two representations that disagree rather than an obviously incorrect line of code. Use these lenses during investigation. Ask: **what relationship is promised, when must it hold, and what maintains it?**

## 1. Data and schema
- DB versus ORM/model versus DTO versus response versus OpenAPI/docs versus frontend: field names, types, nullability, defaults, enums, lengths, precision.
- Migrations missing, different across environments, or partially applied manually.
- Legacy data violating new rules (nulls, empty strings, old enum values/formats).
- DB constraints (unique, FK, check, not null) disagreeing with application validation.
- Soft-deleted/`deleted_at`/archived records not filtered in every query, including joins, counts, aggregates, and exports.
- Denormalized/derived fields (counters, totals, last_activity) not updated on all write paths.
- Pagination without deterministic ordering/tie-breakers causing duplicate or missing rows across pages.
- Collation/case sensitivity differing across DB, application, and indexes.

## 2. Caches, replicas, and copies
- Missing invalidation on write paths (API, job, admin, import, script).
- Cache keys omitting distinguishing dimensions (tenant, user, role, locale, version, filter).
- Unsuitable TTLs, stampedes, cached errors/empty results.
- Reads after writes hitting a replica that has not caught up.
- Search indexes/read models/data warehouses lagging behind authoritative state.
- Instance-local versus centralized caches producing different views.
- Memoization/static/singleton state persisting across requests or tenants.

## 3. Concurrency and transactions
- Check-then-act/read-modify-write without locks, atomic updates, or optimistic versions.
- Transactions too narrow (partial state visible) or too broad (long locks, deadlocks).
- External effects (email, webhooks, jobs) occurring before commit or not occurring after rollback.
- Isolation levels mismatched to requirements (non-repeatable reads, phantoms).
- Deadlocks from inconsistent lock ordering across paths.
- Details: `06-concurrency-transactions.md`.

## 4. Time
- Time zones: UTC versus local, server versus DB versus client, DST; whose definition of a day?
- Dates versus datetimes; inclusive/exclusive ranges; month ends; leap years.
- Clock differences across instances; assuming timestamp order across machines.
- Tokens/TTLs/expiration compared against different clocks.
- Cron running on multiple instances or missing execution during deployment.
- Date formats/parsing differing across layers.

## 5. Contracts and integrations
- Producer/consumer expectations diverging (new required fields, removed fields, changed types).
- Old frontend/mobile versions receiving new responses.
- Rolling deployment with old/new code and different schemas/formats coexisting.
- Old queued messages processed by new code, and vice versa.
- Third parties: timeouts, rate limits, partial responses, retries duplicating effects, unannounced API changes.
- Webhooks: unspecified order, duplicates, signatures/verification, replay.

## 6. Types and logic
- null versus undefined versus empty versus 0 versus false; truthiness; automatic coercion.
- String versus numeric IDs; UUID case; integer overflow; precision loss involving large integers and JSON/JS.
- Money: float versus decimal, rounding, units (cents versus rupiah), currency.
- Enums/constants/statuses defined in multiple places; unvalidated transitions.
- Off-by-one; string/numeric/version comparisons; lexicographic versus numeric sorting.
- Duplicated logic: one copy fixed while others remain unchanged.
- Default arguments, shared mutable objects, input mutation, shallow copies.
- Errors swallowed, wrapped, or replaced, losing the original cause.
- Partial failures stopping multi-step operations without rollback/compensation.

## 7. Access, tenants, and identity
- Tenant/organization/user scoping missing in a query or execution path.
- Permission checks present on one path (API) but absent elsewhere (job, admin, GraphQL, export, WebSocket).
- Middleware/guard order changed or missing on specific routes.
- Identity differences across systems (internal/external IDs, changed emails, merged accounts).

## 8. Configuration and environment
- Environment variables, flags, configuration differing across dev/staging/prod; hidden defaults.
- Incorrect secrets/regions/endpoints; silent default fallbacks.
- Runtime/library/lockfile differences; defaults changing across versions.
- Locale, encoding, Unicode normalization, line endings, trailing slashes, filesystem case sensitivity.
- Resource limits (memory, timeouts, body size, connection counts) differing across environments.

## 9. Processes and people
- Incorrect deployment order (code before migration, or vice versa).
- Manual DB/admin changes bypassing application rules.
- Seeders/fixtures not representing production data.
- Production hotfixes missing from the main branch, causing branch drift.
- Documentation/OpenAPI/comments disagreeing with code.

## 10. Tests and observability
- Excessive mocks hiding bugs; tests pass because of fixtures rather than correctness.
- Missing coverage for errors, boundaries, empty/large data, concurrency, and legacy data.
- Logs lacking correlation IDs/context for tracing across services.
- Metrics/alerts missing silent failures (jobs succeed but results are empty).

## Consistency does not always mean equal values right now

Define the invariant: equality, projection/aggregation, ordering, read-your-writes, or permitted lag. Specify identity/version, observation time, freshness budget, and convergence/recovery. Replica lag within budget is not automatically a bug; equal values do not prove copies represent the same version.

## Usage

For unusual or intermittent bugs:
1. Identify the pair expected to stay consistent: `X (source) ↔ Y (copy)`.
2. Record the maintaining **mechanism** (constraint, transaction, event, invalidation, job).
3. Find **write paths** bypassing that mechanism.
4. Compare X and Y using evidence from the failing case.
5. Repair the synchronization mechanism rather than only one side.
