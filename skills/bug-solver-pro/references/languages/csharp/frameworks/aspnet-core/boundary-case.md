# ASP.NET Core: Filtered Include returns entities outside the filter

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** With EF Core tracking, navigation fixup can attach already tracked related entities even when they fail the current filtered Include. SQL results and the final in-memory graph need not have identical membership.

**Discriminating probe:** Run the failing sequence in one context, then compare with a fresh context/no-tracking query while keeping database rows identical. Record tracked entity IDs and raw query membership. Divergence after fixup supports this cause. Out-of-filter rows already in SQL reject fixup as the first violation.

**Repair, verification, and trap:** Use a projection or suitable no-tracking/fresh-context read when that matches the operation's semantics; keep write/identity requirements explicit. Verify prior-query order and concurrent updates. Do not blindly clear tracking mid-unit-of-work and discard pending changes. [Official contract](https://learn.microsoft.com/en-us/ef/core/querying/related-data/eager).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
