# Symfony: Repository read appears to prove a write that never reached the database

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** With Doctrine ORM, the identity map can return the same managed object after an in-memory mutation. persist schedules management; flush synchronizes pending changes, and an enclosing transaction may still roll back.

**Discriminating probe:** Record SQL/transaction boundaries, then compare the managed-object read with an independent connection after the owning commit. A changed object but unchanged committed row supports an unflushed/uncommitted write. A committed independent row rejects it; another repository read in the same EntityManager is not an independent oracle.

**Repair, verification, and trap:** Place flush and commit at the intended unit-of-work boundary and handle failures there. Verify fresh-reader visibility, rollback, and pending unrelated changes. Do not scatter flush calls: one flush can synchronize more managed changes than the local method suggests. [Official contract](https://www.doctrine-project.org/projects/doctrine-orm/en/3.6/reference/working-with-objects.html).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
