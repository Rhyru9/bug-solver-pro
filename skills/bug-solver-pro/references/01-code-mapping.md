# 01. Map the Code Before Editing

Goal: before changing a line, explain **how the feature works from trigger to final effect across relevant boundaries**, and **who will be affected by the change**.

## Steps

### 0. Confirm the map represents the actual system
Match source, runtime artifacts, dependency versions, effective configuration, and environment. For unfamiliar stacks or execution modes, read `14-stack-semantics.md`. Map paths that affect diagnosis; expand when new evidence appears.

### 1. Identify entry points
- HTTP: route → middleware/guard/interceptor → controller/handler → validator.
- Job/queue: producer → broker → consumer/worker → handler.
- Cron/scheduler: schedule definition → command → service.
- Event/webhook: event source → listener/subscriber → handler.
- CLI/script/migration, callback, stream, plugin, native/FFI boundary, or public library function, according to the system.

Record middleware and hook **ordering**; ordering can cause bugs.

### 2. Trace the complete path
Follow a request through completion without skipping steps:

```
entry → validation → authorization → service/use case → domain logic
      → repository/ORM → DB / cache / queue / external API
      → response mapping / event / side effects
```

At each step, record inputs, outputs, possible failures, and who handles them.

### 3. Callers and callees
- **Callers:** find usages of the functions/classes/fields being changed (code, tests, scripts, cron, migrations, seeders, frontend, other services, API documentation). Use available text and symbol/runtime tools; `scripts/find-usages.sh <symbol>` is optional.
- **Callees:** understand each called function's contract: guarantees, assumptions, and errors it throws.
- Include **indirect** usages: reflection, method-name strings, event names, configuration, DI containers, dynamic imports, ORM relationships, serializers, templates, and raw queries.

### 4. Data shapes across layers
Create a small table:

| Layer | Field name | Type | Nullable | Default | Notes |
|---|---|---|---|---|---|
| Request DTO | | | | | |
| Model/Entity | | | | | |
| DB table | | | | | |
| Cache | | | | | |
| Response/Event | | | | | |

Mark where names, types, or meanings change. Shape transformations can be sources of synchronization bugs.

### 5. Invariants
Write conditions that **must always hold**, for example:
- Emails are unique per tenant.
- `total = sum(item.subtotal) - discount + tax`.
- Status transitions are limited to `draft → submitted → approved/rejected`.
- Stock is never negative.
- Each order has exactly one successful payment.
- Records with `deleted_at` are hidden except from administrators.

For each invariant, find where it is **enforced** (validator, service, DB constraint, trigger) and whether enforcement covers **all paths** (API, job, import, admin, script).

### 6. Source of truth
For each important value, identify where authoritative state lives and where copies/derivatives live (cache, denormalized data, search indexes, read models, reports). Copies need clear synchronization rules.

### 7. Project conventions
Learn and follow error handling, error formats, transactions, logging, naming, layering, DI, testing, and migration conventions. Fixes that ignore conventions can introduce bugs and maintenance costs.

### 8. History and intent
- Use `git log -p -- <file>`, `git blame`, commit messages, PRs, and tickets to learn why code was written this way.
- Unusual code may address a real case (Chesterton's fence). Understand the reason before removing it.

### 9. Tests as specifications
Read existing tests: guarantees, fixtures, and mocks. Tests reveal guarantees and blind spots; compare expected behavior with requirements/contracts because tests can be wrong too.

## Useful notes (select according to the problem)

- Short text flow diagram from entry to final effect.
- Key files.
- Important callers and callees.
- Data-shape table.
- Invariants and enforcement locations.
- Suspicious boundaries and reasons.

## Common mistakes
- Reading only the file named in the stack trace.
- Assuming a function has only one caller without searching.
- Ignoring jobs/cron/scripts/migrations as consumers.
- Ignoring configuration and feature flags that change execution paths.
- Assuming DB field names match API field names.
