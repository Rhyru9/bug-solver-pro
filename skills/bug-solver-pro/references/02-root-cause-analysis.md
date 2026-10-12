# 02. Root Cause Analysis

The visible error may occur after the first invariant violation. Explain the chain trigger → mechanism → consequence, including why healthy cases still work.

## Establish correct behavior

Find relevant requirements, contracts, specifications, tests, and history. Distinguish promised behavior from current implementation habits. If legitimate rules conflict and the choice changes the fix, ask for a specific decision after completing independent investigation.

## Localization

Collect errors/traces, inputs, state, versions/configuration, and cohort patterns. Compare failing and healthy cases. Narrow through flow boundaries (is data correct before or after this point?), minimal input, version/build, environment, or operation order. Use bisect only when the baseline and failure indicator are sufficiently reliable.

## Falsifiable hypotheses

For each hypothesis that affects the decision:

```
Hypothesis / mechanism:
Observations explained:
New prediction if true:
Falsifying result / alternatives to distinguish:
Experiment (input, version, conditions):
Result and artifacts:
Status: VERIFIED / ASSUMED / REJECTED / INCONCLUSIVE
Limits of the conclusion:
```

There is no minimum hypothesis count. For a simple mechanism already directly proven, proceed to the fix. If evidence fits multiple explanations, choose a discriminating experiment from [15-evidence-and-experiments](15-evidence-and-experiments.md). Verify unfamiliar semantics through `13` and `14`.

## Separate three questions

- **Technical cause:** what mechanism violates the invariant? Example: two paths debit the balance for the same event.
- **Triggers and contributing factors:** when do duplicate delivery, ordering, legacy data, load, or configuration enable the mechanism?
- **Detection/prevention gap:** why did tests, monitoring, or design fail to catch it?

“Missing tests” explains why a bug escaped, not necessarily its technical cause. Five Whys can help, but need not contain exactly five steps and does not automatically justify architectural refactoring. Fix at a boundary sufficient to enforce the invariant; report process/design improvements outside scope separately.

## Test the explanation's sufficiency

- Does it explain reported symptoms and cases that do not fail?
- Does it identify prerequisites that actually exist in the application?
- Is there failing-before/passing-after evidence, or other causal evidence with explicit limits?
- Do remaining symptoms arise from the same mechanism, already corrupted data/effects, or separate problems?

Search for related bugs through paths reaching the same invariant, copied code, or other callers. Fix only those within scope; search results are candidates requiring inspection.

## Anti-patterns

Stacking patches without experiments; blaming a library/layer without evidence; treating flakiness as randomness; treating missing logs as proof of absence; inferring cause solely from deployment correlation; defending a hypothesis contradicted by evidence; replacing technical diagnosis with “bad design.”
