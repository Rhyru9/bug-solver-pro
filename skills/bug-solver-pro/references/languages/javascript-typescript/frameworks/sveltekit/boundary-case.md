# SvelteKit: Enhanced form succeeds but the page does not update

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Returning a custom use:enhance result callback replaces default post-submission behavior. Ignoring its update helper can omit the expected reset/invalidation/form-state handling.

**Discriminating probe:** Compare native submission, uncustomized enhancement, and the actual callback with the same local action result. Then invoke the supported update path without changing the action. Restored behavior supports a client post-processing gap. Stale server output across all three rejects that explanation.

**Repair, verification, and trap:** Call update with intentional options when retaining defaults, or deliberately implement the required applyAction/invalidation behavior; understand their different scope. Verify success, validation failure, redirect, and double-click state. Do not resubmit a successful mutation merely to refresh the UI. [Official contract](https://svelte.dev/docs/kit/form-actions).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
