# Spring: debugging playbook

Deeper case: [REQUIRES_NEW causes a stall only under load](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Internal Transactional call ignores the requested boundary

**Mechanism:** In proxy mode, this.inner() bypasses transaction advice. An outer transaction may still be active, while inner propagation such as REQUIRES_NEW is ignored.

**Probe and falsifier:** Compare transaction identity, propagation, and rollback through the self-call and an injected bean call. Merely seeing an active transaction is insufficient. Equivalent intended boundaries reject this explanation.

**Repair and verify:** Move the transactional operation to the appropriate injected bean or use a programmatic boundary. AspectJ has different semantics. Verify the production call path, not a directly constructed unit-test target. [Official contract](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html).

## 2. An exception is thrown but writes commit

**Mechanism:** Default rollback rules distinguish unchecked and checked exceptions; caught exceptions or configured rules can change the outcome.

**Probe and falsifier:** Throw the actual exception type after a sentinel write and check persisted state outside the transaction. Expected rollback rejects this cause.

**Repair and verify:** Set deliberate rollback rules at the owning boundary or propagate the intended failure. Inspect global rollback settings, including newer Spring options. Verify both expected commit and rollback cases. [Official contract](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html).

## 3. Advice applies to some methods but misses a final method

**Mechanism:** Subclass-based proxies cannot override final/private methods; JDK proxies expose interface calls instead.

**Probe and falsifier:** Inspect the actual proxy type and invocation target. Compare advice markers on the failing method and an interceptable entrypoint. Equal interception rejects this cause.

**Repair and verify:** Place the advised operation on a method compatible with the selected proxy strategy and call through the bean. Avoid blanket modifier changes. Verify proxy-level invocation. [Official contract](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html).
