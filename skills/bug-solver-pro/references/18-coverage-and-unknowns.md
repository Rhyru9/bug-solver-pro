# 18. Coverage and bugs outside the catalog

Use when a query has no applicable result, evidence contradicts a familiar pattern, a repair leaves unexplained behavior, or several interacting mechanisms may be involved. The catalog is open-ended; an unrecorded bug is not an exceptional case requiring a guessed match.

## Mechanism coverage

The following are candidate angles, not confirmed causes or a requirement to inspect every row. New seed records in `data/patterns.json` are curated from these questions and references `14` and `15`. They are reasoning heuristics, not independently established framework facts or observed incidents.

| Domain | Angles represented | Distinguishing evidence |
|---|---|---|
| Representation | Missing/null/empty/zero, encoding/normalization, numeric bounds; existing numeric/date guidance | Original bytes/types and intermediate values versus an independent contract |
| Lifecycle | Aliasing, use after release, reused sessions, initialization order, cleanup masking failure | Ownership, identities, acquire/release events and prerequisite readiness |
| Control flow | Unawaited work, dropped errors, invalid transitions, pagination, range bounds, nontermination | Required completion/error paths, state transitions and progress measures |
| Concurrency | Duplicate delivery, check-then-act, ambiguous commit, commit/publish gap, lost updates, deadlocks, stale completion | Versions, operation IDs, real atomic boundaries and controlled happens-before order |
| State | Cache/replica disagreement, tenant state, legacy shapes, partial batches, durability | Authoritative state and projections, initial data, commit/recovery boundaries |
| Contracts | Producer/consumer drift, date/instant interpretation | Actual payloads, declared expectations and both consumer versions |
| Integration | Stream framing, short writes, external retry semantics, native ABI boundaries | Bytes, completion counts, provider responses and actual layouts/ownership |
| Security | Wrong resource/actor decision, validation/use representation gap, credential lifecycle | Isolated authorized/denied fixtures and effective identities before effects |
| Performance | Query amplification, retention, pool exhaustion, scheduling starvation, input growth | Comparable workload, wait ownership, operation counts and profiles |
| Testing | Shared state, incorrect oracle, mocked-boundary gap | Independent expected behavior and the actual failing boundary |
| Diagnosis | Environment/artifact drift, patch chains, observer effects, source-map mismatch | Executing artifact identity, equivalent controls and original uninstrumented behavior |

## Open-world investigation

1. **Preserve the observation.** Write expected/actual behavior, the independent oracle, the failure signature and its context. If reproduction is missing, preserve available evidence and identify which observation would change the decision.
2. **Locate the first violation.** Map the actual path from trigger through values, control, state and resources. Find last-correct and first-incorrect boundaries. Include prior history, late writers, generated code and external consumers when evidence points there.
3. **Question the model.** At an implicated boundary ask what assumptions about representation, ownership, lifetime, ordering, atomicity, authority, delivery, resources or observation must be true. Which prerequisites are known, assumed or contradicted?
4. **Compare controls.** Use a comparable healthy case, boundary input, fresh/reused state or a controlled schedule. Preserve the original failure signature when minimizing. For interacting factors, compare small combinations instead of changing many variables together.
5. **Choose one discriminator.** State candidate mechanism → new prediction → falsifying observation → safe experiment. The mechanism may be absent from the catalog. Pick the experiment that most cheaply resolves a consequential uncertainty, then update the explanation from its result.
6. **Repair and verify the owner.** After enough causal evidence, fix the invariant at its owner and check original behavior, coupled callers, error/cancel paths and persisted effects. Separate code repair, recovery and mitigation. Reopen diagnosis when observations remain unexplained.

Use `scripts/search.py "<sanitized symptom>" --explore` to print the structured angle prompts from `data/angles.json`, independently of catalog fit. Ordinary `--plan` output includes exploration when retrieval is empty or weak. Angle prompts ask where to observe; they do not invent hypotheses or establish a diagnosis. Select relevant angles using the actual artifact, rather than treating this list as a ceiling.

## Match handling

- A strong lexical match still requires actual applicability and causal evidence.
- A partial or weak match is a lead to inspect, not a ready investigation diagnosis. The plan does not promote weak matches into hypotheses automatically.
- A no-match result is a retrieval outcome, not proof the system has an unfamiliar bug or that all known mechanisms were excluded.
- A plausible mechanism contradicted by reliable evidence is rejected. Unavailable or ambiguous evidence is inconclusive.
- A catalog result explaining one symptom does not explain every symptom. Trace whether two failures share an invariant, are independent, or are artifacts of observation.

Do not attach undocumented runtime semantics to a language name. Discover the executing versions and actual behavior using [14](14-stack-semantics.md). Use [15](15-evidence-and-experiments.md) and [16](16-hard-to-trace-debugging.md) for experiment selection and misleading traces.

## Recording genuine lessons

A newly encountered mechanism need not be added to the installed skill to fix the current project. Keep project evidence in authorized working notes, with inputs/conditions, commands/artifacts, results, falsifying controls, impact and generalization limits. Do not include credentials, customer data or confidential source in shared skill resources.

When skill maintenance is authorized, record a verified case using [learned cases](learned-cases.md), including exact versions if relevant. For the search catalog, add an abstract **heuristic** with an applicable experiment, falsifier, verification, limits and traceable local reference. Add positive paraphrases and confusing or unrelated negative queries to the tests. Do not promote a synthetic example, documented contract or passing tool test into an empirically verified incident.

## What all-angle coverage can establish

Coverage helps expose missing questions. It does not establish every bug class, every interaction, every stack or every race schedule. Stop when the mechanism and relevant impact are adequately supported, while retaining explicit untested boundaries. Expand again when the current artifact exposes a blind spot, not to satisfy an arbitrary category count.
