# Vue: Reading a computed sort changes another component's list

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** A computed getter that calls sort/reverse on the source array mutates shared reactive state while ostensibly deriving a value. The observer becomes a writer.

**Discriminating probe:** Snapshot ordered entity IDs before the getter's first actual evaluation, then read its value with other writers controlled. Source reordering at evaluation supports this cause. No source mutation during an executed getter rejects it; a cached getter that never runs makes the probe inconclusive.

**Repair, verification, and trap:** Derive from a copy or supported nonmutating array API, keeping getter evaluation pure. Verify source order, sorted view, and other consumers across dependency updates. Shallow copying suffices for array ordering, but does not isolate mutations of nested elements. [Official contract](https://vuejs.org/guide/essentials/computed.html).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
