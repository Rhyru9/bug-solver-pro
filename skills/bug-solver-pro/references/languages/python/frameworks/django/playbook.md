# Django: debugging playbook

Deeper case: [get_or_create still inserts duplicates under concurrency](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Bulk updates silently omit business effects

**Mechanism:** QuerySet.update() bypasses model save() and pre_save/post_save signals; bulk_create also has lifecycle limitations.

**Probe and falsifier:** Compare one instance.save() with the actual bulk path using a signal recorder and persisted rows. Equal lifecycle effects reject this explanation.

**Repair and verify:** Make required bulk-path invariants explicit or use the instance path when appropriate. Do not blindly replace bulk work with an N+1 loop. Verify data and required effects. [Official contract](https://docs.djangoproject.com/en/5.2/ref/models/querysets/).

## 2. on_commit never runs in a passing test

**Mechanism:** Django TestCase wraps work in a transaction that rolls back; ordinary test completion does not exercise a real commit.

**Probe and falsifier:** Capture callbacks with captureOnCommitCallbacks(execute=True), or use TransactionTestCase for actual transaction behavior. An absent registration rejects the test-wrapper explanation.

**Repair and verify:** Test callback registration separately from real commit/rollback ordering. Use transaction-aware tests for locking and visibility; verify rollback emits no committed-effect notification. [Official contract](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).

## 3. Catching a database error causes later transaction failures

**Mechanism:** An IntegrityError caught inside atomic can leave that transaction broken until its rollback boundary.

**Probe and falsifier:** Trigger a duplicate constraint, then query inside the same block versus after leaving it. If both succeed, inspect the actual exception and connection state.

**Repair and verify:** Catch around an inner atomic savepoint, outside that inner block, or let the owning transaction roll back. Verify valid writes remain possible after recovery and partial writes do not escape. [Official contract](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```python
# In Django TestCase: check registration and deliberately execute callbacks.
with self.captureOnCommitCallbacks(execute=True) as callbacks:
    perform_operation()
self.assertEqual(len(callbacks), 1)
# This does not simulate independent connections or a real durable commit.
```
