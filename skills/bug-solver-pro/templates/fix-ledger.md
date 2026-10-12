# Fix Ledger

Optional for long investigations: record behavioral changes and key decisions. Before adding a patch, check whether it cancels, repeats, or conflicts with earlier assumptions.

| # | Time | Bug addressed | Changed file/function | Change | Rationale (cause) | Assumptions | Impact checked | Verification result | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | active / reverted / replaced by #n |
| 2 | | | | | | | | | |

## New bugs after a fix (STOP protocol)

| After fix # | New bug | Causal mechanism (concrete path) | Shared cause with original bug? | Decision |
|---|---|---|---|---|
| | | | | |

## Protected rules (detect conflicts/cycles)

| # | Correct behavioral rule | From fix # | Protected by test |
|---|---|---|---|
| 1 | | | |

## Warnings

- [ ] Repeated patches without new evidence? → Review the model and choose a discriminating experiment.
- [ ] New fix cancels an earlier invariant? → Check the oracle; ask if product rules are ambiguous.
- [ ] Old bug returns? → Check causes and related bugs.
