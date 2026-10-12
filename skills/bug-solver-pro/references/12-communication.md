# 12. Communication and Scope

## Clarification and authorization are different

Ask about correct behavior when requirements are ambiguous, business rules genuinely conflict, or fix options have different consequences that cannot be resolved from the repository/session. Provide findings, options, a recommendation, and the specific decision needed. Continue independent investigation that does not depend on the answer.

Use existing authorization. A fix request includes necessary investigation, local patches, checks, and reviewable migration/recovery designs. Contracts, money, authorization, or multiple modules require stronger analysis and evidence, not automatic reauthorization.

Production actions, real-data backfills, destructive operations, messaging, publishing, and deployment follow actual session/environment permissions. If new authorization is necessary, first complete available artifacts and checks; seek approval for a concrete action rather than an unprepared plan.

## Scope

Repair the requested bug's mechanism. Related findings may be included when necessary for the invariant and within the task; report them. Keep independent findings, cosmetic refactoring, mass renaming, unnecessary upgrades, and architectural rewrites separate.

Templates are optional. Small bugs need brief notes/reports; long investigations benefit from ledgers preserving evidence and decisions. Do not ask users for information discoverable through code, tests, configuration, or history.

## Reporting

Lead with the result, then cause/evidence, changes, verification, and material limits/risks. Distinguish verified patches, candidate fixes, mitigation, data recovery, and deployment status. `[VERIFIED]` requires evidence context; `[ASSUMED]` is not evidence. When wrong, explain the updated understanding and correct it using new evidence.

Use relevant sections of `templates/final-report.md`; small fixes do not need the entire structure.
