# Axum: Adding authentication changes unknown URLs from 404 to 401

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Router layer and route_layer have different routing/fallback scope. An authentication layer covering fallback can reject before the intended not-found behavior.

**Discriminating probe:** Exercise existing, absent, and method-mismatched routes with allowed/denied fixtures; trace route selection and layer entry. Auth on unmatched fallback supports scope mismatch. A request already matching an explicit catch-all rejects the assumed not-found path.

**Repair, verification, and trap:** Select layer placement from the intended route/fallback contract; route_layer can apply checks to matched routes without rewriting ordinary unmatched-route behavior. Preserve protection of every real endpoint. Verify nested routers and fallback deliberately; do not use 404 as evidence that a protected resource operation cannot execute. [Official contract](https://docs.rs/axum/latest/axum/struct.Router.html).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
