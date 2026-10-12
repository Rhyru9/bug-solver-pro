# 07. Data, Migrations, Backfills, and Caches

A correct code fix can still fail if **existing data** is not addressed.

## Before changing schemas or data rules

1. **Inventory affected data:** row counts, tables, tenants, time ranges.
2. **Measure actual conditions** with queries (nulls, duplicates, invalid enum values/formats). Do not infer production data from fixtures.
3. Choose a legacy strategy: reject, normalize, migrate, or temporarily support both formats.

## Safe migration pattern: expand → migrate → contract

1. **Expand:** add backward-compatible columns/tables/fields (nullable or with appropriate defaults). Old code continues to work.
2. **Deploy compatible code** for the transition. If using dual writes, explain atomicity, ordering, partial failures, retries, and reconciliation; two separate writes are not automatically safe. Fallbacks must distinguish missing values from valid but empty new data.
3. **Backfill** incrementally, idempotently/with guards, and resumably. Prevent old snapshots from overwriting active writers through versions/conditional writes or appropriate coordination.
4. **Verify** old/new consistency using comparison queries.
5. **Switch reads** to the new format.
6. **Contract:** remove old columns/code in a separate release after stability is established.

Do not combine incompatible schema changes and code deployment in one step on a running system.

## Migration rules
- Migrations must be **idempotent** or protected against duplicate execution.
- Avoid long locks on large tables; batch data changes. Check online/concurrent DDL semantics for the actual engine/version: locks, transactions, validation, failure state, and resume/recovery. “Online” does not guarantee no locking.
- Provide **down/rollback** or recovery plans; identify irreversible actions (dropped columns, lossy type changes).
- Change column types carefully: conversions can truncate or round data.
- Before adding `NOT NULL`/unique constraints to old data, repair that data.
- Test migrations on realistic copies, including scale and dirty data.
- Keep migrations, models/ORM, seeders, fixtures, and documentation **aligned**.

## Backfills
- Use small batches and progress markers; support stopping and resuming.
- Make reruns safe and idempotent.
- Respect application rules; avoid unintentionally triggering mass notifications/emails.
- Record before/after counts and checksums as evidence.
- Consider DB load and peak hours.

## Dirty and legacy data
- Temporarily tolerate old shapes during transition; remove compatibility code after backfill completes.
- Do not manually “clean” production data without backups and authorization.
- Record anomalies; they can reveal the bug's cause.

## Caches

Questions for every involved cache:
- What is its **source of truth**? Who writes it?
- When is it **invalidated**, and do all write paths trigger invalidation (API, job, admin, import, script, migration)?
- Does the **key** include all dimensions (tenant, user/role, locale, version, query parameters)?
- What happens when the cache is **empty, expired, or unavailable** (stampede, fallback)?
- Are **errors/empty results** cached and then treated as valid?
- After a data-shape change, can new code read old cache entries? Consider versioned keys or a planned flush.
- Are multiple layers (application, Redis, CDN, browser, ORM) independently stale?

Choose a strategy according to freshness/consistency budgets. Check races where an old reader repopulates the cache after writer invalidation; centralized invalidation, versioned keys, or TTL alone do not automatically preserve invariants. TTL can be valid when bounded staleness is allowed.

## Replicas and consistency
- Read from the primary after writing when current data is required (read-your-writes).
- Do not rely on replicas for logic requiring strong consistency.

## Required evidence
- Before/after queries (row counts, aggregates, samples).
- Backfill verification showing no remaining old-format rows.
- Written rollback plans for high-risk changes.
