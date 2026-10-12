# 06. Concurrency, Transactions, Retries, and Partial Failures

Start with the invariant, participants that can change state, and guarantee boundaries. Names such as “lock,” “transaction,” or “dedupe” do not establish whether guarantees apply per process, key, connection, database, or across services.

## Races and atomicity

For check-then-act/read-modify-write, draw an interleaving that violates the invariant. Choose constraints, conditional atomic updates, optimistic versions, or locks according to store semantics and all write paths. Handle conflicts and use the correct scope/connection. Distributed locks require lifetime, ownership, and rules for workers still running after lease expiration; do not assume permanent ownership.

Distinguish **safety** (bad outcomes do not occur) from **liveness** (work can eventually complete). A lock that prevents duplicates but hangs forever is insufficient. Evaluate contention, fairness where relevant, lock ordering, timeouts, and error/cancellation cleanup.

## Transactions and external effects

Map the atomic unit, commit/durability points, rollback, nested transactions/savepoints, and effects outside the store. Reduce external work holding locks; define a protocol when cross-service coordination is needed.

After-commit hooks can prevent effects before commit, but crashes between commit and delivery still require analysis. Outboxes can persist delivery intent with state, but publishers/consumers still need failure and redelivery handling. Choose according to permitted loss/duplication, not because a pattern sounds safe.

Compensation is not atomic rollback across services; it can fail or remain incomplete. Explain intermediate state, recovery, and invariants that must continue to hold.

## Unknown outcomes

Timeouts/cancellation/lost replies do not establish whether an operation committed. Distinguish not started, failed before commit, successful, and unknown outcomes. For unknown outcomes, reconcile using operation identity or status queries before retrying effects that may duplicate.

## Retries and idempotency

- Retry only appropriate failures; the retry scope must preserve required snapshots/transactions and avoid repeating successful effects without protection.
- Define deadlines/attempt limits/budgets, backoff/jitter where appropriate, and retry ownership; layered retries can amplify load.
- Dedupe requires key scope (such as tenant + operation), payload equivalence, expiration/retention, and behavior for simultaneous requests.
- A “processed” marker and its effect must not introduce unexplained loss/duplication windows. Recording the marker before the effect alone can make a retry assume success when the effect never occurred.
- Idempotency means repeated operations have effects consistent with the contract; not every operation should become an upsert or absolute assignment. Increments are valid when each business event is applied under the required guarantees.

## Tasks, queues, and schedulers

Determine who observes errors, who owns tasks, when they finish/cancel, and how resources are released. Intentional detached work needs clear ownership and failure handling.

Discover actual broker guarantees: ordering scope/partition, redelivery, visibility timeouts, acknowledgments, and dead letters. Determine whether payloads are snapshots or IDs fetched again. Check crashes before/after effects and acknowledgments, old pending messages, cron overlap, worker restart, and resume.

## Evidence

Use barriers/hooks for controlled interleavings and fault injection at commit/publish/ack boundaries in tests. Assert final state, effect counts, conflict outcomes, progress, and cleanup, not merely absence of errors. Repeated parallel runs help, but passing some runs does not prove every schedule is safe. See `15-evidence-and-experiments.md`.
