# 09. Testing and Verification

Evidence must test requested behavior and changed mechanisms. Choose checks according to risk; tests mirroring implementation or counting patch lines do not help.

## Define the oracle

An oracle establishes correctness: requirements, specifications, an independent formula, an invariant, or consumer contracts. Do not derive expected values from the function under test. Snapshots can protect compatibility but must not canonize a bug as expected behavior.

If outputs contain timestamps, random IDs, or unspecified ordering, normalize only contractually irrelevant parts. Do not erase differences that constitute the symptom.

## Before/after evidence

1. Where possible, reproduce the failure on the baseline using relevant input/version/configuration. The test must fail because of the bug, not broken setup/dependencies.
2. Apply the fix; repeat the same check and observe results and effects.
3. Check neighbors reachable through coupling: callers, error paths, boundaries, legacy data, or concurrency according to the mechanism.
4. Run relevant project tests/checks. Broaden the suite for wide impact, required project checks, or new concerns. Do not repeat passing suites without changes or new reasons.

For simple low-risk repairs, direct checks or existing tests may suffice. For logic regressions, persistence, contracts, concurrency, or partial failures, automated invariant tests are usually valuable. Do not require a new test for every edit.

Without incident reproduction, use alternative evidence from `15`, verify the candidate patch, and report limits. Do not pretend every bug can be reproduced deterministically.

## Choose a level that observes the failure mode

| Mechanism | Relevant verification |
|---|---|
| Formulas, parsing, boundaries | Unit/property tests with independent oracles |
| ORM, constraints, isolation, queries | Integration with relevant engine/provider and configuration |
| Payloads, compatibility | Contract tests with old/new consumers and formats |
| Races, acknowledgments, retries, crash windows | Controlled interleaving/fault injection plus state invariants and effect counts |
| Legacy data/migrations | Old shapes, partial runs, resume, concurrent writers, recovery |
| Lifecycle/resources/performance | Comparable workload profiling plus success/error/cancel cleanup |
| Cross-component user flow | Replay/E2E at boundaries not covered by unit tests |

Mocks contain external effects and help test failure paths, but cannot establish transaction/driver semantics they replace. Test containers/alternative providers also require semantic equivalence checks.

Property/metamorphic tests help when there is no single expected result: supported serialization round-trips, input permutations where order is irrelevant, or idempotent replay. Relations must come from contracts, not assumptions that every operation is commutative/idempotent.

## Baselines, isolation, and failures

Use isolated workspaces/test data; do not overwrite user changes or trigger real effects for reproduction. Record commands, versions/conditions, exit status/results, and supporting evidence. Separate pre-existing failures from regressions; do not relax or skip tests to get green results. Proven incorrect tests may be updated based on the oracle.

## Final review and evidence limits

Review the diff: is each change needed? Debug code, scope creep, swallowed errors, weakened guards, or hidden environment assumptions? Check original data/logs/effects when available and authorized.

Report what ran, what passed/failed, and what remains untested with reasons. Documentation/local tests do not prove production resolution, compatibility with every consumer, or safety of every race schedule. Prepare monitoring and recovery indicators when needed without claiming deployment occurred.
