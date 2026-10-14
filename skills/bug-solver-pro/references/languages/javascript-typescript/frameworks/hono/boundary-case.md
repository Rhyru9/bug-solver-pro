# Hono: Validator works but a later raw Request read fails

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** HonoRequest body helpers and the underlying raw Request have different body-cache/access paths. Mixing cached helper reads with direct consumption can leave the raw stream already used.

**Discriminating probe:** Use the same bounded fixture through helper-only and mixed helper/raw paths; record bodyUsed and the first reader. A failed second raw read after successful consumption supports this cause. Failure with an untouched stream refutes exhaustion; replacing middleware wholesale introduces confounders.

**Repair, verification, and trap:** Choose one parsing owner; share its validated result through request context. If a real raw clone is needed, use a supported cloneRawRequest helper when available, or clone before consumption with explicit memory limits. Verify middleware order, content type, and size limits; do not assume every installed Hono release has the same helper. [Official contract](https://hono.dev/docs/api/request).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
