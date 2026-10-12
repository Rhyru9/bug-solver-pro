# 04. Prevent Fix Chains and Cascading Regressions (Analyze Mechanisms)

**A→B→C→D, A→E→B, and A↔B are only example shapes.** Real failures may branch, converge into diamonds, cycle, recur elsewhere, appear weeks later, or silently corrupt data without looking like a new bug. Analyze the **causal mechanism** rather than matching a shape.

Working definition: a *fix chain* occurs when a change **creates, exposes, moves, or revives** another defect, or fails to remove the original defect.

## 1. Basic model (applicable to any shape)

System = **elements** (functions, modules, tables, jobs, services, caches, configuration) + **coupling** between elements.

Coupling types (select relevant ones; do not search only for function calls):
- Shared data (tables, columns, caches, files, messages).
- Shared state (globals, singletons, sessions, process memory).
- Ordering/timing (execution order, timing, race windows).
- Contracts (request/response/event/schema shapes).
- Resources (connections, locks, threads, memory, quotas, rate limits).
- Configuration/flags/environment.
- Processes and people (deployment order, manual data edits, concurrent fixes by people/agents).

Defects propagate **through coupling**. A fix changes an element; outgoing couplings are possible paths for new bugs. Before editing, **enumerate coupling around changed elements** (`01-code-mapping.md`, `03-blast-radius.md`).

## 2. Mechanisms that make fixes cause problems (open catalog)

This is a **heuristic taxonomy assembled for this skill**, not a formal standard or research result. Names such as “defect conservation” and “compensating bug” are practical labels, not official terminology. Their value lies in the questions they prompt.

Use these as lenses. A case may involve multiple mechanisms. The catalog is **incomplete**; consult `13-research-adaptive.md` if no mechanism fits.

| # | Mechanism | Indicator | Example |
|---|---|---|---|
| 1 | **Hidden coupling** | A fix in A changes something implicitly used by B | A service date-format change breaks reports |
| 2 | **Unmasking** | The repaired bug previously hid another defect | An error previously stopped execution before the second bug |
| 3 | **Compensating bug** | Other code compensates for a bug; the fix breaks that compensation | A consumer subtracts 1 because the API always adds 1 |
| 4 | **Symptom displacement** | A symptom disappears but returns in another form | An exception becomes silently empty data; a bottleneck moves |
| 5 | **Conflicting requirements** | Two legitimate rules conflict | Fix A requires a value; fix B makes it optional |
| 6 | **Copy drift** | Logic exists in N places; only some are fixed | Create is fixed, update/import/bulk are not |
| 7 | **Partial coverage** | Only some execution paths are repaired | API works, job/admin paths remain broken |
| 8 | **Wrong layer** | Patches are applied to consumers rather than the source | Every controller adds a null check |
| 9 | **Timing/order shifts** | Changed timing opens a race | Speeding up a step exposes a race |
| 10 | **Data/code mismatch** | Code is correct but old data remains broken, or vice versa | New validation rejects legacy data |
| 11 | **Amplification** | A safeguard magnifies the problem | Retries cause load storms or duplicate effects |
| 12 | **Feedback loop** | A fix triggers events that trigger further fixes | An update invokes a listener that updates again |
| 13 | **Observer effect** | Logging/validation/instrumentation changes behavior | Logging forces lazy loading and changes results |
| 14 | **Defect conservation** | Errors persist while moving locations | A report discrepancy of 5 becomes a balance discrepancy of 5 |
| 15 | **Environment/configuration** | A fix works in one environment but fails in another | Different flags or library versions |
| 16 | **Test blind spots** | Correct neighboring behavior lacks protection | A regression appears only in production |
| 17 | **Lost fixes/recurrence** | Merge/rebase/hotfix loses a repair | A production hotfix never reaches the main branch |
| 18 | **Process/people** | Concurrent fixes overwrite each other | Two agents/people edit the same area |
| 19 | **Broken assumptions** | A fix changes consumers' implicit assumptions | Results become unordered but consumers rely on order |
| 20 | **Version dependencies** | Library/runtime versions change the fix's behavior | A minor upgrade changes a default |

Common shapes are descriptions, not mandatory classifications: chains, branches, diamonds, cycles, recurrence in related instances, delayed failures, and **silent** failures with incorrect data but no error.

## 3. Prevention before the first fix

1. **Model coupling:** record changed elements and their coupling. For each outgoing coupling, ask what the consumer assumes about the behavior being changed.
2. **Capture correct behavior before editing** (characterization/golden master): record outputs, statuses, data, events, and logs for representative neighboring scenarios as a comparison baseline.
3. **Compare before/after** (differential check): run the same input corpus on both versions; **every difference should be explained and intended**. Unexpected differences signal mechanisms above.
4. **Record system invariants** (balanced totals, no duplicates, valid statuses, incoming count = outgoing count) and check affected neighboring invariants as well as the original bug's invariant.
5. **Fix ledger** (`templates/fix-ledger.md`): changes, reasons, assumptions, impact; review before subsequent fixes.
6. **One source of truth:** identify the invariant's owner; consolidate only when required for the fix. Duplication does not automatically authorize a large refactor.
7. **Small, isolated, reversible steps:** one fix per step with passing tests between steps where applicable, making bisect easier. Separate behavior-preserving refactoring from behavioral changes.

## 4. Universal questions

Before, during, and after a fix, ask:
1. What **actually changes** in behavior? What must remain unchanged?
2. Who **depends on the old behavior**, intentionally or implicitly?
3. Is the defect **removed or displaced**? Check other locations reached by the same data.
4. Does the fix **explain all symptoms** and **why other cases do not fail**?
5. What previously **masked** another defect (error, guard, fallback, rounding, retry)?
6. What changes **beyond the edited code** (order, timing, data, size, defaults)?
7. If the fix is wrong, **how and how soon will that be detected**?
8. Do other paths (jobs, admin, imports, events, old versions) reach the same element?
9. Is another person/agent/process changing this area?
10. What remains **unknown**? Research or ask if necessary (`13-research-adaptive.md`).

## 5. Protocol for new or unusual symptoms (STOP)

Applies to **any shape**, including silent failures:

1. **Stop editing.** Do not patch a new symptom on top of an unexplained fix.
2. **Record** the last fix, new symptom, time, and evidence in working notes/ledger.
3. **Test causality:** compare baseline and patch in isolated workspaces/data. Do not revert/stash user changes or perform destructive bisect. Control relevant inputs/configuration/order; symptom disappearance supports causality within the experiment's limits, not every possible cause.
4. **Explain the mechanism** through a concrete data/state/order/contract path. If unable, remap (`01-code-mapping.md`) or research (`13`).
5. **Classify the mechanism** using the catalog (multiple matches or no match are acceptable).
6. **Reassess the cause:** do the original and new defects share a cause? Prove it rather than assume it.
7. **Design a solution around proven invariants:** combine patches when a shared cause is established; separate independent defects. If requirements conflict, state each rule and ask for a decision (`12-communication.md`).
8. **Expand protection:** add tests for new symptoms and extend relevant regression scenarios and invariants.
9. **Verify differentially** and check conservation: is the defect removed or merely moved?
10. **Update notes/ledger:** write learned cases only when skill maintenance is authorized.

## 6. Warning signs (independent of shape)

- New fixes touch the same lines/functions/rules as previous fixes.
- A fix cancels or weakens another fix's guard.
- Closed bugs return in the same or related location.
- Individual fixes seem locally correct while the system becomes less consistent.
- Totals/counts remain discrepant after the fix (defect conservation).
- One source change requires many small consumer patches.
- Failures appear only for specific data/tenants/versions/times after a fix.
- Symptoms become **quieter**: errors disappear but results remain wrong.
- The fix cannot be explained simply.

Signals to change approach:
- An unexplained new symptom: stop speculative patches and investigate.
- Repeated patches without new evidence, or a patch canceling a previous invariant: redraw coupling and check the oracle/semantics.
- Attempt counts do not prove misunderstanding. Clarify ambiguous product rules; research/experiment when semantics or mechanisms are unknown.

## 7. Break cycles and conflicts

Indicator: fix B removes/neutralizes fix A, or a bug shifts between two conditions.
1. Stop editing.
2. Express both desired behaviors as explicit rules (condition → correct result).
3. Check whether both can hold by distinguishing conditions, types, statuses, tenants, or versions.
4. If they cannot, this is a product/business decision; **ask the user**.
5. Implement a consistent rule at the appropriate owner and protect both cases with tests.

## 8. Structural reinforcement

Move enforcement from discipline to mechanisms: DB constraints, types/enums, state machines, atomic operations, boundary validation, shared calculation/format helpers, contract tests, invariant alerts. Repair **patterns**, not just instances: inspect related candidates and respect scope; use a shared mechanism only when invariants/prerequisites genuinely match.

## 9. Short illustration (not a template)

Symptom: incorrect order totals. Removing a discount call from a listener causes empty promotion reports; patching reports then makes report totals disagree with orders.
Mechanism: copy drift + wrong layer. Cause: no single owner of discount calculations.
Fix: `calculateOrderTotals()` becomes the source of truth for services, reports, and listeners; compare historical order inputs differentially; protect promotion + manual discount + tax combinations with tests.
