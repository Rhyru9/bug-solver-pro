# React: Editing the second row changes the first row's draft

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Component state follows position/type/key identity, not the business entity described by props. Index keys can preserve the wrong local draft after reorder; nested component definitions can instead cause unexpected resets.

**Discriminating probe:** Edit one row, reorder/filter the collection, and trace stable record ID, key, and component mount identity. A draft following position supports wrong identity. Stable entity keys and unchanged intended mounts reject this explanation for the observed transition; initial render alone is inconclusive.

**Repair, verification, and trap:** Use stable entity keys where state belongs to entities; use a changed key only when resetting is intended. Move nested component definitions out when remounting is accidental. Verify reorder, delete, insert, and entity switching; do not mirror props into effects merely to conceal identity errors. [Official contract](https://react.dev/learn/preserving-and-resetting-state).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
