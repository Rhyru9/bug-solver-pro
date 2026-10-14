# Django: get_or_create still inserts duplicates under concurrency

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Its atomicity relies on a database uniqueness constraint matching the lookup identity. An application-level existence check or model validation does not serialize two independent writers.

**Discriminating probe:** Inspect the deployed constraint, then barrier two separate connections before creation for the same identity. Record returned IDs and final row count. A matching enforced constraint with a genuine conflicting attempt rejects missing uniqueness; a sequential test or SQLite substitute is inconclusive about the production race.

**Repair, verification, and trap:** Define the correct unique identity at the database boundary, plan cleanup of existing duplicates before migration, and handle the conflict deliberately. Verify concurrent create, retry, distinct identities, and legacy rows. Do not introduce a broad process lock that leaves other workers unprotected. [Official contract](https://docs.djangoproject.com/en/5.2/ref/models/querysets/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
