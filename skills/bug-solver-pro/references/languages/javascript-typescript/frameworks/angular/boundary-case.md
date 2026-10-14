# Angular: An interceptor changes the payload on a retried request

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** HttpRequest cloning/immutability does not deeply protect its body object. An interceptor that pushes into a nested array can modify the caller's DTO and accumulate changes if invoked again.

**Discriminating probe:** Snapshot a synthetic payload before each interceptor invocation; reproduce retry/re-entry and compare nested values plus object identity. Accumulation at this boundary supports mutation. Unchanged bodies with duplicate effects point instead to retry delivery; one invocation cannot test repeat safety.

**Repair, verification, and trap:** Construct the intended body without mutating caller-owned nested values, and make transformations safe for repeated invocation. Verify original DTO preservation, repeated invocation, and request retries. Separately require an appropriate idempotency contract before retrying mutations: body purity alone does not prevent duplicate effects. [Official contract](https://angular.dev/guide/http/interceptors).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
