# 21. Data and query failures hidden by valid schemas

Use when values look individually valid but the selected population, row multiplicity, history, or concurrent decisions violate the contract. These six heuristics are indexed in `data/patterns.json`; framework-specific techniques are indexed separately under `data/frameworks/`. Apply [probe validity](19-causal-decision-procedure.md) and distinguish source rows, query results, managed graphs and wire output.

## Shared-predicate write skew

Different transactions can change different rows based on compatible-looking snapshots while breaking a shared rule. Synchronize the relevant reads, then inspect the invariant across committed results. A per-row version check is not automatically a cross-row invariant. Choose constraints, serialization or explicit coordination from the actual provider contract; handle transaction aborts and external effects deliberately. [PostgreSQL isolation semantics](https://www.postgresql.org/docs/current/transaction-iso.html).

## Stale cache refill after invalidation

An older in-flight read may populate a cache after a newer write invalidates it. Hold that read, perform the write/invalidation, then release the fill and compare versions. Repeated deletion or longer TTLs do not establish ordering. Evaluate version-aware publication or another consistency design against the required freshness and failure behavior. The race is an authored composition scenario; cache-aside alone promises no global consistency. [Cache-aside consistency limits](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).

## Expired lease holder and missing fencing

A former owner can resume after lease expiry. Trace owner epochs at the protected effect boundary, rather than only the lock service. A newer lock token has no protective effect if the resource accepts stale writes. Rejecting stale epochs must be an enforced contract; lock release correctness and fencing are distinct concerns. [Redis distributed-lock guidance](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/).

## Nested retry multiplication

Independent retry layers can multiply work and exceed an outer deadline. Count attempts per operation at each layer while the local dependency fails deterministically. Set budgets and retry ownership deliberately; backoff/jitter does not substitute for a cap or idempotency. Compare error classes and the combined path, rather than optimizing each layer in isolation. [AWS retry and overload guidance](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/).

## Join cardinality and filter placement

Establish the intended grain before computing totals: one row per order, line, event, or other entity. Use zero/one/many related rows and preserve identities through joins. Outer-join filters can alter membership; a DISTINCT on amounts can discard legitimate equal amounts. Fix query shape/aggregation at the intended grain, then check arithmetic. [PostgreSQL table expressions](https://www.postgresql.org/docs/current/queries-table-expressions.html).

## Null-sensitive exclusion

Null in a NOT IN list/subquery can produce unknown rather than true, changing WHERE membership. Compare nullable left values, nullable right sets and empty sets explicitly. NOT EXISTS may encode a different intended null policy; it is not a mechanical replacement. Observe predicate outcomes and selected IDs before changing application defaults. [PostgreSQL subquery/null semantics](https://www.postgresql.org/docs/current/functions-subquery.html).

## Population history is an input

A current schema does not show whether a row came from an old writer, partial backfill, default, tombstone, retry or repair. Compare cohorts under the same artifact and query. Keep migration progress and active writers visible. Code fixes and recovery of previously incorrect data need separate verification; use [data/migrations/cache](07-data-migrations-cache.md) and [coexisting contracts](08-contracts-and-deploy.md).

Official links support the mechanisms, not a claim that an application or every database uses the same semantics. Select matching versions/providers and test the implicated boundary. Lack of a row in this list does not rule out an unrecorded data bug.

## Bounded executable controls

The [in-memory SQL probe](../scripts/probes/sql_query_semantics.py) uses only Python's standard library. It compares joined sums, an incorrect DISTINCT-on-amounts repair, and one-row-per-order aggregation. It also compares null-containing/non-null/empty exclusion sets against an explicit non-null identity policy. Run with `python3 "<skill-root>/scripts/probes/sql_query_semantics.py"`. Executed versions, results and limits are recorded in the [data audit](coverage/data-audit.md); this is not a production migration or a concurrency/isolation test.
