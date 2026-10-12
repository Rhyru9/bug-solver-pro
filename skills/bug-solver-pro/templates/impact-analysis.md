# Impact Analysis (Optional; Use Relevant Sections)

Planned change: ____

## Changed elements

| Item (function/field/endpoint/table/event) | Change type | Contract changed? |
|---|---|---|
| | | yes / no |

## Consumers

| Consumer (code/test/job/service/frontend/third party) | Usage | Affected? | Mitigation |
|---|---|---|---|
| | | | |

Discovery sources: grep/find-usages, access logs, metrics, owners: ____

## Data

- Existing data affected? (counts, tables, tenants):
- Migration/backfill needed? Strategy:
- Caches/indexes/read models requiring invalidation/rebuilding:
- Queued messages using old formats:
- Active writers, partial failures, dual-write/backfill atomicity:

## Side effects

| Effect (email, notification, payment, webhook, job, audit, metric) | How it changes | Risk |
|---|---|---|
| | | |

## Operations

- Deployment order:
- Safe rolling deployment with old/new code coexisting?
- Feature flags / staged rollout:
- Rollback/recovery plan, including irreversible effects/data:

## Risks

| Risk | Level (low/medium/high) | Mitigation |
|---|---|---|
| | | |

## Regression list (must keep working)

| # | Scenario | Check (existing test / new test / manual) | Status |
|---|---|---|---|
| R1 | | | |
| R2 | | | |
| R3 | | | |
