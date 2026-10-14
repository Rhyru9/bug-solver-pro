# Rails: A stale edit silently replaces a newer one

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** A read-modify-save flow can lose a concurrent update unless the operation uses a suitable conditional/atomic update or optimistic locking. Optimistic locking depends on the configured locking column and the actual write API.

**Discriminating probe:** Load two instances of the same fixture before either save; commit the first, then attempt the stale second edit. Record locking-column values, affected rows, and StaleObjectError. Rejection of the stale write refutes missing conflict detection on that path; sequential reloads are not a conflicting test.

**Repair, verification, and trap:** Use the appropriate locking/version contract or atomic update for the invariant; handle conflicts with a deliberate user-visible retry/merge decision. Verify stale, fresh, and bulk/raw paths. Blindly rescuing and resaving can merely overwrite the newer state again. [Official contract](https://api.rubyonrails.org/classes/ActiveRecord/Locking/Optimistic.html).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
