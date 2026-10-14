# Laravel: debugging playbook

Deeper case: [Adding an orWhere widens a tenant-scoped query](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Queue job cannot see a just-created record

**Mechanism:** A real queue worker can consume a job before its dispatching database transaction commits; a synchronous test backend can hide this.

**Probe and falsifier:** Hold the transaction open while an isolated worker consumes; compare immediate dispatch with after-commit dispatch. Visibility before commit rejects this race for that setup.

**Repair and verify:** Use afterCommit()/configured after_commit when appropriate. For durable publish guarantees, assess an outbox: after-commit dispatch alone still has a crash gap. Verify rollback and worker visibility. [Official contract](https://laravel.com/framework/docs/12.x/queues).

## 2. Queued model contains later values, not dispatch-time values

**Mechanism:** Queued Eloquent models are typically serialized by identifier and reloaded; loaded relationship constraints are not a reliable snapshot.

**Probe and falsifier:** Change the row after enqueue but before consumption; inspect job input and relation results. An explicit serialized value payload rejects this mechanism.

**Repair and verify:** Choose explicitly between IDs plus current reads and immutable scalar snapshots with a version. Avoid serializing unnecessary relationships. Verify delayed and retried execution. [Official contract](https://laravel.com/framework/docs/12.x/queues).

## 3. Mass update changes rows without running observers

**Mechanism:** Eloquent mass updates do not retrieve each model, so corresponding per-model update events are not emitted.

**Probe and falsifier:** Compare an instance save with the actual query update while recording observer calls and affected rows. Matching observer activity rejects this path assumption.

**Repair and verify:** Move required bulk invariants into the owning operation or deliberately use per-model persistence with a cost budget. Verify effects exactly once; do not disable observers globally. [Official contract](https://laravel.com/framework/docs/12.x/eloquent).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```php
// When the job requires the enclosing transaction's committed records:
ProcessOrder::dispatch($order->id)->afterCommit();
// This orders dispatch after commit; it does not close the commit/publish crash gap.
```
