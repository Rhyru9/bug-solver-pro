---
name: bug-solver-pro
license: MIT
description: Investigate and fix backend or application logic bugs across languages, frameworks, and libraries through flow mapping, testable hypotheses, impact analysis, and regression verification. Use for errors, incorrect results, inconsistent state, races, dependency failures, or performance problems requiring diagnosis. Not for new feature development or cosmetic refactoring without a bug.
---

# Bug Solver Pro

Purpose: produce fixes that explain the failure mechanism, preserve behavior that is still correct, and provide evidence proportional to risk. This skill is a reasoning framework; catalogs prompt questions rather than provide an exhaustive list of causes or a guarantee against regressions.

## Searchable diagnostic guidance

For unclear symptoms, the bundled catalog offers candidate mechanisms and discriminating experiments in eleven domains: `concurrency`, `state`, `contracts`, `performance`, `testing`, `diagnosis`, `representation`, `lifecycle`, `control-flow`, `integration`, and `security`. It is optional for a local bug whose mechanism is already clear. Security angles apply to the reported bug and its relevant impact; they do not expand the request into a broad security audit.

Resolve `<skill-root>` to the folder containing this installed `SKILL.md`; do not assume the user's project contains the scripts or a particular agent environment variable exists. Requires Python 3.9+ with no external packages:

```bash
python3 "<skill-root>/scripts/search.py" "duplicate webhook retry" --domain concurrency
python3 "<skill-root>/scripts/search.py" "stale cache after write" --plan --json
python3 "<skill-root>/scripts/search.py" "unexplained boundary failure" --explore
```

Use 2–5 sanitized English symptom/mechanism terms; translate a report into keywords without inventing facts. Domain filters are explicit; omit `--domain` when the boundary is uncertain. Inspect matched terms and applicability before using a result; the score is lexical relevance, not confidence in a cause. Every seed is a heuristic sourced from bundled references, not a verified incident. Turn applicable results into hypotheses and select an experiment based on actual code and evidence. Do not apply a listed mechanism as an automatic fix or require every returned hypothesis to be investigated.

If results are absent, weak, unrelated or contradicted, state the retrieval limit and use [coverage and unknowns](references/18-coverage-and-unknowns.md) to map the first incorrect boundary, test hidden assumptions and form a new falsifiable mechanism. `--explore` prints fourteen observation angles independently of catalog fit; `--plan` includes exploration for absent or weak matches. The angles guide investigation and are not an exhaustive list of possible bugs. Python is optional for the reasoning workflow. Read [structured tooling](references/17-structured-tooling.md) for the schema, query contract, validation, and remaining gaps.

## Choose depth according to the problem

- **Local and clear:** read the relevant path, identify the violated invariant, fix it, and verify the failing case and neighboring behavior. Brief notes are enough.
- **Cross-boundary or unclear:** map data flow, lifecycle, versions, and coupling; use competing hypotheses and experiments before editing.
- **Persistent state, concurrency, money/access, performance, or production:** add analysis of partial failures, existing data, compatibility, recovery, and evidence at the relevant real boundaries.

Increase depth when evidence conflicts, scope grows, or a patch exposes another symptom. You do not need to read every reference, fill every template, invent multiple hypotheses for a proven typo, or run the entire suite without a reason. Templates may be used in working notes; do not add repository files merely to satisfy a process.

## Decision principles

1. **Understand before changing.** Explain trigger → flow → first invariant violation → symptom. Map the boundaries that affect the decision, then expand when evidence requires it.
2. **Establish correct behavior from authoritative sources.** Requirements, contracts, specifications, and tests may conflict. Existing tests and behavior are not automatically correct; resolve ambiguities that change the fix.
3. **Look for mechanisms, not technology names.** Discover the semantics of the version actually running: lifetime, mutation, errors, transactions, serialization, scheduling, and resources. Do not transfer solutions between stacks without checking assumptions.
4. **Separate evidence from assumptions.** `[VERIFIED]` identifies the observation, artifact/command, and context. Documentation establishes a documented contract; it does not establish the cause of an incident. Use `[ASSUMED]`, `[REJECTED]`, or `[INCONCLUSIVE]` as appropriate.
5. **Test hypotheses before stacking patches.** Choose experiments that distinguish explanations and change decisions. If results disagree, revise the model instead of protecting a hypothesis with more patches.
6. **Fix at the invariant's owner.** Choose the smallest change in behavior and impact, not simply the fewest lines. Guards, retries, fallbacks, or validation can be valid fixes when justified by the contract and failure mode; silently swallowing failures is insufficient.
7. **Preserve scope and safeguards.** Do not weaken authorization, constraints, validation, or tests to pass a patch. If a rule/test is wrong, show evidence and update it deliberately. Avoid unnecessary refactoring or upgrades.
8. **Respect existing authorization.** Continue investigation, local patches, tests, and migration design within the task. Ask only for decisions not already provided; production, destructive, or external actions follow session and environment permissions. Touching a contract or authorization does not automatically require asking again.
9. **State the limits of evidence.** Passing tests does not prove every interleaving, environment, consumer, or delayed effect is safe. Do not promise zero regressions.

## Reasoning workflow

1. **Define the failure and oracle.** Expected versus actual behavior, the basis for the expectation, triggers, a healthy comparison case, and how correctness is detected. Reproduce when possible; otherwise retain incident evidence and state its limits.
2. **Identify the system actually executing.** Match source to artifacts, runtime, installed dependencies, configuration, and environment. Follow data/control/state/resources across relevant boundaries; check direct and indirect callers. For unfamiliar stacks, read `14`.
3. **Build a causal explanation.** Record hypotheses, predictions, falsifying evidence, and experiment results. Find the first invariant violation; distinguish technical causes, triggers, and detection gaps. For intermittent failures or missing reproductions, read `15`.
4. **Assess impact and options.** What changes, who depends on it, what data/effects have already occurred, what can partially fail, and what must remain correct? Code repair, data recovery, and incident mitigation are separate work.
5. **Implement a targeted fix.** Obtain failing-before/passing-after evidence where possible; choose tests or checks suited to the failure mode. Follow project conventions. Structural changes are justified only when necessary to enforce the invariant.
6. **Verify according to risk.** Check the original scenario, neighboring behavior, error paths, side effects, and relevant real boundaries. Run appropriate project checks; report pre-existing failures separately. Review the diff and remove temporary instrumentation.
7. **Report results and limits.** Cause and evidence, changes and rationale, checks and results, remaining risks, and deployment/recovery actions not yet performed. Record lessons in the skill only when skill maintenance is authorized.

## When a bug is hard to trace

Ask: what was actually observed; where was state last correct and first incorrect; how do failing and healthy cases differ; and what result would reject the current hypothesis? Choose one discriminating experiment before adding a patch. For value provenance, trigger minimization, history replay, observer effects, negative controls, and failures after prolonged operation, read [16-hard-to-trace-debugging](references/16-hard-to-trace-debugging.md).

## When a patch introduces another symptom

Stop adding speculative patches; continue investigation. Compare before/after in isolation without deleting user work. Distinguish a new regression, a previously unreachable defect, and environmental coincidence. Reassess invariants and coupling; combine fixes only when a shared mechanism is proven. Repeated patches without new evidence signal a need to update the model, not a magic numerical threshold or automatic proof of misunderstanding.

## References: read according to the question

| Question | Reference |
|---|---|
| Flow, callers, data, invariants, ownership | [01-code-mapping](references/01-code-mapping.md) |
| Hypotheses and causal diagnosis | [02-root-cause-analysis](references/02-root-cause-analysis.md) |
| Consumers and change impact | [03-blast-radius](references/03-blast-radius.md) |
| Conflicting patches or shifting symptoms | [04-anti-fix-chain](references/04-anti-fix-chain.md) |
| Different representations of state disagree | [05-desync-angles](references/05-desync-angles.md) |
| Races, transactions, retries, acknowledgments | [06-concurrency-transactions](references/06-concurrency-transactions.md) |
| Existing data, migrations, caches | [07-data-migrations-cache](references/07-data-migrations-cache.md) |
| Contracts and coexisting versions | [08-contracts-and-deploy](references/08-contracts-and-deploy.md) |
| Tests, oracles, evidence, verification limits | [09-testing-verification](references/09-testing-verification.md) |
| Translate stack pitfalls into questions | [10-stack-pitfalls](references/10-stack-pitfalls.md) |
| Symptoms that prompt hypotheses | [11-symptom-to-cause](references/11-symptom-to-cause.md) |
| Ambiguity, authorization, reporting | [12-communication](references/12-communication.md) |
| Unknown semantics or versions | [13-research-adaptive](references/13-research-adaptive.md) |
| Adapt to unfamiliar languages/frameworks/libraries | [14-stack-semantics](references/14-stack-semantics.md) |
| Choose experiments; intermittent failures, crashes, performance | [15-evidence-and-experiments](references/15-evidence-and-experiments.md) |
| Misleading traces, hidden state, rare bugs, stalled diagnosis | [16-hard-to-trace-debugging](references/16-hard-to-trace-debugging.md) |
| Unrecorded mechanisms, partial matches, conflicting evidence, coverage gaps | [18-coverage-and-unknowns](references/18-coverage-and-unknowns.md) |

[Templates](templates/investigation-notes.md) are optional aids; use only relevant sections. [Learned cases](references/learned-cases.md) retain cases with evidence and context.

The `scripts/*.sh` helpers are optional tools for usage/history searches; read their usage before running. Search results are candidates, not proof that no consumers exist. Without shell/Git/rg, use IDE search, a language server, debugger, or equivalent environment tools.

## Completion criteria

- Correct behavior and fix scope are clear; the mechanism is explained with evidence and confidence level.
- The patch enforces the invariant; relevant impact and compatibility are checked.
- Available verification is complete; results, baseline failures, and untested boundaries are reported.
- No speculative patches, weakened safeguards, or unrelated changes remain.
- If the cause or runtime behavior is unconfirmed, describe the result as a candidate fix / mitigation with limits, rather than a proven resolution. Unauthorized production actions remain unperformed.
