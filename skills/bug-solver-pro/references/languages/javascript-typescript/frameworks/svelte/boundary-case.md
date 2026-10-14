# Svelte: An effect ignores a value read after await

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** In Svelte 5, effect dependency tracking follows synchronous reactive reads. A read performed later in an async callback is not automatically a dependency of the original effect.

**Discriminating probe:** Mutate the late-read source without changing other sources; trace effect starts and compare with a version that captures it synchronously. Reruns only after synchronous capture support missing tracking. A tracked read already occurring before the async boundary refutes this cause; no executed effect is inconclusive.

**Repair, verification, and trap:** Capture intended dependencies synchronously, pass the snapshot to async work, and add cancellation/obsolete-result guards with synchronous cleanup registration. Verify each source independently, reverse completion order, and unmount. Do not make the effect callback async and assume its Promise supplies cleanup. [Official contract](https://svelte.dev/docs/svelte/$effect).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
