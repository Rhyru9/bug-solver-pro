# Rails: debugging playbook

Deeper case: [A stale edit silently replaces a newer one](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Bulk maintenance bypasses callbacks or validations

**Mechanism:** update_all writes through the relation without instantiating models and does not run the normal model callback/validation path.

**Probe and falsifier:** Compare one update! with the maintenance relation update_all and record required callbacks. Equal lifecycle effects reject this assumption.

**Repair and verify:** Enforce required bulk invariants explicitly or use deliberate per-record operations with a query budget. Verify persisted rows and effects, not only the affected count. [Official contract](https://guides.rubyonrails.org/active_record_querying.html).

## 2. Notification is sent for a transaction that later rolls back

**Mechanism:** after_save executes before the enclosing transaction has committed; external effects cannot be rolled back with the row.

**Probe and falsifier:** Force rollback after save and record notification attempts. No effect before commit rejects this cause.

**Repair and verify:** Use after_commit or an owning transactional publication design for effects requiring committed data. Handle callback failure and durable delivery separately. Verify rollback, commit, and retry. [Official contract](https://guides.rubyonrails.org/active_record_callbacks.html).

## 3. Eager loading is present but query count still grows per row

**Mechanism:** Accessing unpreloaded associations or building new scoped relations can bypass the preloaded association result.

**Probe and falsifier:** Count SQL for a small and larger result set; identify the association expression creating per-row queries. A flat count rejects this N+1 explanation.

**Repair and verify:** Preload the association actually read or shape the query explicitly. Verify returned semantics as well as query scaling; fewer queries alone is insufficient. [Official contract](https://guides.rubyonrails.org/active_record_querying.html).
