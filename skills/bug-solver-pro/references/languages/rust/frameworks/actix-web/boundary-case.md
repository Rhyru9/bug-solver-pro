# Actix Web: Increasing HTTP workers exhausts database connections

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Each worker builds an App. A separately created connection pool inside the factory multiplies the pool budget across workers and process replicas; a pool limit is not necessarily a service-wide limit.

**Discriminating probe:** With a bounded local configuration, count pool instances, allowed connections, workers, and process replicas; change only worker count. Proportional new pool instances support multiplication. One shared pool per process rejects worker-local pool duplication; it does not establish a cluster-wide budget.

**Repair, verification, and trap:** Share a pool outside the worker factory when the client supports that ownership model, or explicitly budget separate pools against database capacity. Verify concurrency, recovery, and graceful shutdown. Do not assume cloning every client shares its pool: inspect that client's clone semantics and actual instances. [Official contract](https://actix.rs/docs/server/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
