# Flask: Two successful requests lose one session update

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Concurrent requests can read the same session state and save competing versions without a guaranteed save order. A session dictionary mutation is not an atomic multi-request operation.

**Discriminating probe:** Start two requests from the same initial test session, barrier after their reads, then observe response cookies or backing-store versions and the next read. A reproduced overwrite supports the race. Serialized/version-checked storage rejects this particular cause; nonoverlapping requests prove little.

**Repair, verification, and trap:** Keep correctness-critical counters/workflow state in an authoritative atomic store; use deliberate versioning/merge rules for session updates where needed. Verify reversed completion order and both requests' effects. Server-side session storage alone does not guarantee concurrency control. [Official contract](https://flask.palletsprojects.com/en/stable/api/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
