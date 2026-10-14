# Gin: A second binder sees EOF although the request body was valid

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Ordinary body binding consumes the request stream. Middleware or a first binder can leave no bytes for a later independent parse; this differs from malformed JSON.

**Discriminating probe:** Observe which component first reads the body and compare one binder versus the actual two-reader sequence using the same fixture. EOF only after consumption supports ownership failure. Failure on the first untouched read refutes second-reader exhaustion; skipping middleware also changes the path and needs a control.

**Repair, verification, and trap:** Parse once into the input contract, or use a compatible ShouldBindBodyWith variant when multiple bounded views are genuinely needed. Verify content types and size limits. Buffering every request or ignoring the second error can hide the problem and increase memory cost. [Official contract](https://gin-gonic.com/en/docs/binding/bind-body-into-different-structs/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
