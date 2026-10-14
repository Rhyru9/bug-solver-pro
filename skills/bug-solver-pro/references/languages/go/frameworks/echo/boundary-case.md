# Echo: Client disconnects but downstream calls keep consuming resources

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Request-scoped cancellation reaches downstream code only when the request context is propagated and observed. A background context or a non-context-aware API can sever that link; cancellation does not undo committed effects.

**Discriminating probe:** Use an isolated slow downstream, cancel the caller, and trace request context completion versus downstream termination and effect state. A severed context chain supports propagation failure. Prompt downstream cancellation with already committed effects rejects a resource-leak diagnosis; no client disconnect means the probe was not activated.

**Repair, verification, and trap:** Pass the incoming request's context to supported downstream operations, give detached jobs their own explicit lifetime, and release resources on every exit. Verify cancellation before and after commit and bounded pool recovery. Do not treat timeout/cancel as permission to retry a non-idempotent effect. [Official contract](https://pkg.go.dev/net/http#Request.Context).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
