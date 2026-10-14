# Laravel: Adding an orWhere widens a tenant-scoped query

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** SQL boolean precedence and ungrouped OR clauses can change (tenant AND A) OR B into a wider predicate than tenant AND (A OR B), including interactions with scopes.

**Discriminating probe:** Inspect generated SQL and bindings with sanitized fixtures; create a second tenant row satisfying only B. Query the actual relation/scoped builder. If every branch remains restricted to the intended tenant, reject this grouping mechanism; a single-tenant dataset cannot expose it.

**Repair, verification, and trap:** Group alternatives inside a closure under the required identity/scope predicate and preserve authorization at the operation boundary. Verify cross-tenant, soft-deleted, no-match, and legitimate OR matches. Avoid removing a scope or filtering the already overbroad result in application memory. [Official contract](https://laravel.com/framework/docs/12.x/queries).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
