# Spring: REQUIRES_NEW causes a stall only under load

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** The outer transaction retains its connection while a proxied REQUIRES_NEW operation acquires another. Enough simultaneous outer holders can exhaust the pool and wait for inner acquisitions.

**Discriminating probe:** In an isolated bounded test, record transaction depth, held connections, pool waiters, and acquisition timeouts; synchronize outer transactions before inner calls. Outer-held/inner-waiting cycles support this cause. Free capacity with a different wait owner refutes it; raising a timeout and seeing recovery is inconclusive.

**Repair, verification, and trap:** Reconsider the independent-transaction requirement and resource budget, then bound admission or size the pool for the proven topology. Verify outer rollback versus inner commit behavior. Do not remove transaction boundaries or blindly enlarge pools: database capacity and other clients still constrain them. [Official contract](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-propagation.html).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
