# SvelteKit: debugging playbook

Deeper case: [Enhanced form succeeds but the page does not update](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Server-side store leaks data between users

**Mechanism:** A module variable/store mutated by server load can be shared across requests.

**Probe and falsifier:** Interleave two authenticated synthetic requests in one process; inspect state identities. Request-local identity and no cross-write reject this cause.

**Repair and verify:** Return request-specific load data and use scoped context where needed. Avoid a server-global writable for current user. Verify SSR and client navigation with both identities. [Official contract](https://svelte.dev/docs/kit/state-management).

## 2. Child route waits for unrelated parent work

**Mechanism:** An early await parent() can serialize otherwise independent loading.

**Probe and falsifier:** Measure starts/finishes of parent and child fetches; move independent child work before awaiting parent in a reproduction. No overlap improvement rejects this waterfall explanation.

**Repair and verify:** Start independent work before awaiting parent; retain ordering for genuine dependencies. Verify errors, cancellation, returned data, and total latency. [Official contract](https://svelte.dev/docs/kit/load).

## 3. Navigation leaves load data stale although the URL changed

**Mechanism:** Load reruns depend on tracked inputs; reading a parameter outside the tracked execution or using an untracked custom dependency can hide the change.

**Probe and falsifier:** Change only the relevant route/query input and record whether load executes and which input it reads. A rerun with correct data rejects tracking as the cause.

**Repair and verify:** Read dependencies inside load; use depends/invalidate for custom invalidation where appropriate. Verify relevant changes rerun and unrelated changes do not unnecessarily refetch. [Official contract](https://svelte.dev/docs/kit/load).
