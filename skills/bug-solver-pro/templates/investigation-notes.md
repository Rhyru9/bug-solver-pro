# Investigation Notes (Optional)

Choose sections that support decisions; omit others. Working notes do not have to become repository files.

## Problem and oracle
- Bug/ticket, scope:
- Expected behavior, requirement/contract basis:
- Actual behavior, triggers, healthy comparison case:
- Reproduction / incident evidence / unavailable information:

## Actual system and map
- Source/artifact, runtime/dependency/provider versions, effective configuration:
- Trigger → data/control/state/resources → final effect:
- Files, callers/callees, dynamic usages, external boundaries:
- Invariants, owners, enforcement/bypass paths:
- Stack semantics relevant to the bug and their evidence/prerequisites:
- Source of truth, projections/copies, freshness budget:

## Hypotheses and experiments
| Hypothesis | Prediction / falsifying result | Experiment and context | Result / artifact | Status and limits |
|---|---|---|---|---|
| | | | | |

Status: VERIFIED (what/context/evidence), ASSUMED, REJECTED, INCONCLUSIVE. Distinguish documented contracts from evidence of application causality.

## Causal explanation
- First invariant violation and mechanism:
- Triggers/contributing factors:
- Detection gaps (not automatically technical causes):
- Why failing and healthy cases differ:
- Related bugs / remaining symptoms / uncertainty:

## Plan and task boundaries
- Relevant options, choice, rationale:
- Affected consumers/data/effects/resources; regression list:
- Mitigation, code fix, data recovery, deployment status:
- Required evidence / project checks:
- Unknown user decisions, if any:
- Already-authorized actions versus actions requiring new authorization:
