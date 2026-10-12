# Learned Cases (Growing Knowledge Base)

This file holds only actual cases reproduced during authorized skill maintenance. Tooling cases below are not claims of production incidents or general agent effectiveness. No synthetic catalog seed is promoted into verified knowledge.

Entry rules:
- Include traceable causal evidence/context. If only a documented contract is verified, say so; do not present it as a proven incident case.
- Describe **abstract patterns**, not project stories. Exclude customer data, secrets, internal names, and confidential code.
- Include versions/dates for version-dependent behavior.
- One entry per pattern. Update similar entries rather than duplicating them.
- Do not record memories or guesses without evidence.
- Write only when skill maintenance is authorized, not merely because files are writable. For project-fix tasks, relevant lessons may remain in working notes/reports.

## Entry format (copy into Entries below)

```
### <Short pattern title>
- Recorded date / relevant versions:
- Symptom (observed behavior):
- Context (stack, trigger conditions):
- Cause / mechanism:
- Category (such as inconsistent state, concurrency, contracts, fix-chain: <mechanism>):
- Evidence and context (tests/logs/data; distinguish documented contracts from application causality):
- Generalization limits / conditions where the solution does not apply:
- General fix / solution pattern:
- Post-fix checks:
- Sources (title + URL), if any:
```

## Entries

### Search failure misreported as absence

- Recorded date / relevant versions: 2026-10-13; Bash 3.2.57 on macOS; usage-search helper with `rg` available.
- Symptom: searching a nonexistent directory completed with exit 0 and printed `(none)`.
- Context: an isolated fixture passed a missing child directory to `find-usages.sh`.
- Cause / mechanism: `SEARCH ... || echo "(none)"` treated all nonzero statuses as an ordinary no-match outcome and replaced the failure status with successful output.
- Category: observation/error-propagation boundary.
- Evidence and context: repository test `UsageTests.test_missing_directory_is_failure_not_no_matches` failed before the change (exit 0) and passed afterward (nonzero failure, no fabricated empty-result claim). `test_real_no_match_is_success` separately confirms an actual no-match remains successful.
- Generalization limits: observed for this helper and fixture; tool exit-code contracts must be inspected before applying the pattern elsewhere.
- General fix: validate the directory and preserve search status, accepting only the documented no-match status as absence. Do not suppress diagnostic errors.
- Post-fix checks: valid empty directory, invalid directory, literal symbol and relevant fixture match; all passed.
- Sources: local helper implementation and repository fixture tests; no external source or production incident.

### Regex interpretation of a literal identifier

- Recorded date / relevant versions: 2026-10-13; Bash 3.2.57, local `rg` search.
- Symptom: searching `a.b` returned both `a.b` and `aXb`.
- Context: an isolated text fixture contained distinguishable markers on the two lines.
- Cause / mechanism: the user-supplied identifier entered a regex search, where its dot matched any character.
- Category: representation/interpretation boundary.
- Evidence and context: `UsageTests.test_symbol_is_literal_not_regular_expression` failed before the change because the unrelated line appeared; it passed after fixed-string search was used.
- Generalization limits: the helper promises symbol lookup; a tool explicitly offering regular expressions should preserve regex semantics instead.
- General fix: use fixed-string matching at a literal-search boundary and pass operands after `--`.
- Post-fix checks: exact identifier matches, no unrelated wildcard match, genuine no-match and missing-directory behavior; all passed.
- Sources: local helper implementation and repository fixture tests.

### EOF termination and valid empty history

- Recorded date / relevant versions: 2026-10-13; Bash 3.2.57 and Git 2.50.0.
- Symptom: co-change inspection on a one-commit fixture produced no peer file and exited 1; a commit touching only the target also exited 1.
- Context: disposable Git repositories, including a peer filename containing spaces. No external repository or user Git history was changed.
- Cause / mechanism: `git log --pretty=format:'%H'` could omit the final newline, while a plain `while read` skipped the last unterminated line. A filtering pipeline also treated valid empty output as a failure under `pipefail`.
- Category: framing/termination plus empty-result semantics.
- Evidence and context: `CoChangeTests.test_single_commit_is_not_dropped_at_eof` and `test_no_cochanges_is_valid_empty_result` failed before the patch with exit 1. Both passed after terminated commit output and explicit empty-result handling. These changes were verified together, not as an independent ablation experiment.
- Generalization limits: this line-based helper still needs manual review for unusual Git path quoting and names before renames; co-change is not proof of causal coupling.
- General fix: use a terminated record format for line readers, preserve command failures, and distinguish an empty data set from a failed pipeline.
- Post-fix checks: one commit with a peer path containing spaces, no peer changes and invalid history limit; all passed.
- Sources: helper source and local Git fixture tests.
