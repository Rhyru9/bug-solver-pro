# Symfony: debugging playbook

Deeper case: [Repository read appears to prove a write that never reached the database](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Autowiring injects a valid but wrong implementation

**Mechanism:** Multiple services can satisfy an interface; aliases and named bindings determine the chosen dependency.

**Probe and falsifier:** Inspect php bin/console debug:autowiring and debug:container for the implicated type/service under the actual environment. Correct resolution rejects this candidate.

**Repair and verify:** Set the intended alias/binding at the owner rather than changing arbitrary constructors. Verify both HTTP and command consumers resolve the right implementation. [Official contract](https://symfony.com/doc/current/service_container.html).

## 2. Message effects repeat even though the handler succeeded

**Mechanism:** Messenger transport redelivery can occur after effects but before acknowledgement; a successful prior attempt does not imply exactly-once processing.

**Probe and falsifier:** In an isolated transport, fail after the effect and before acknowledgement, then redeliver the same operation. Confirm multiple handler executions for that operation. One atomically deduplicated effect across those executions rejects missing idempotency on that path; redelivery not reaching the handler is inconclusive.

**Repair and verify:** Enforce idempotency at the effect owner with a stable operation key and atomic state transition where possible. Verify crash/retry and normal repeated distinct messages. [Official contract](https://symfony.com/doc/current/messenger.html).

## 3. Second message inherits state from the first

**Mechanism:** Long-running workers reuse services; operation state can survive if it is not reset between messages.

**Probe and falsifier:** Process A and B in one worker, then B in a fresh worker; compare synthetic tenant/state markers. Identical clean behavior rejects retained state.

**Repair and verify:** Prefer operation-local state; for stateful services implement supported reset behavior and inspect worker reset configuration/version. Verify retries and sequential messages without relying on worker restarts. [Official contract](https://symfony.com/doc/current/messenger.html).
