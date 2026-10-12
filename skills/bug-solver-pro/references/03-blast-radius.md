# 03. Blast Radius: Assess Impact Before Changing

Every change has a blast radius. Identify it **before** implementing a fix rather than discovering it through new bugs.

## Questions for affected boundaries

### A. Code consumers
- Who calls/imports/inherits/configures the changed component? (`scripts/find-usages.sh`)
- Are there indirect usages: reflection, strings, event names, DI bindings, route names, templates, serializers, raw queries, YAML/JSON configuration?
- Are there consumers outside the repository: services, frontend, mobile, SDKs, BI reports, ETL, third-party integrations?

### B. Contracts
- Do signatures, types, nullability, defaults, or parameter order change?
- Do response shapes, field names/types, error codes, HTTP statuses, array order, or date/number formats change?
- Do event/webhook/message payloads change?
- Does the DB schema change (columns, types, constraints, indexes, defaults)?

### C. Behavior others may depend on
- Does anyone rely on the old behavior, including behavior considered a bug? Consumers may have adapted to longstanding bugs.
- Does execution order, timing, or a side effect change?

### D. Data
- How do new rules treat **existing data**? Are migration, backfill, or legacy handling needed?
- Could data become invalid, unreadable, or duplicated?
- Do caches, search indexes, read models, or other copies need invalidation/rebuilding?
- Can queued messages created in the old format still be processed?

### E. Side effects
- Could email, notifications, payments, outgoing webhooks, jobs, audit logs, or metrics occur twice, disappear, or change timing?
- Does the change affect transaction scope, commit order, or rollback?

### F. Operations
- Is a specific deployment order required (migration before code, or the reverse)?
- Is it safe during rolling deployment with old and new code coexisting?
- Are feature flags, staged rollout, or rollback paths needed?
- Are long-running jobs still executing old logic?

### G. Security and access
- Does the change affect authorization, tenant scoping, input validation, or sensitive data?

## How to answer

1. Search for consumers/coupling with available tools; usage/history helpers are optional.
2. Record relevant impacts; `templates/impact-analysis.md` is optional for complex changes.
3. Produce a **regression list**: concrete scenarios that must keep working, each with a check (existing test, new test, or manual verification).
4. Classify each impact as low/medium/high risk and select mitigations (tests, flags, staged migrations, team communication).

## Signals of broad impact (pause and reconsider)
- Functions/fields used across many modules.
- Changes to stored or externally transmitted formats.
- Changes to default behavior.
- Code involving money, authorization, permissions, customer data, or deletion.
- Fixes requiring changes across multiple services.

Increase evidence, reduce scope where appropriate, or prepare a staged fix. Clarify only decisions not already given; authorization follows the session (`12-communication.md`).

## Principles
- Test compatibility against actual consumers; even additive changes can break strict schemas, exhaustive enums, or default semantics. Choose transitions according to the contract.
- **Centralize changes** at the correct owner rather than distributing patches across consumers.
- **Do not assume** consumers are absent because a search found none; inspect access logs, metrics, and ask when needed.
