# Angular: debugging playbook

Deeper case: [An interceptor changes the payload on a retried request](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. One UI event makes two HTTP calls

**Mechanism:** HttpClient observables are cold: separate subscriptions, including manual subscription plus async pipe, issue separate requests.

**Probe and falsifier:** Count subscriptions and network attempts for one interaction. One subscription with two attempts points instead to retry/interceptors or another caller.

**Repair and verify:** Give the read one intended subscription owner or share it with explicit lifetime/cache semantics. Verify teardown and later subscribers. Do not casually share a mutation observable to hide duplicate submissions. [Official contract](https://angular.dev/guide/http/making-requests).

## 2. Signal data changes internally without notifying consumers

**Mechanism:** Mutating an object in place and setting the same reference can be suppressed by the signal equality check.

**Probe and falsifier:** Compare in-place mutation with an immutable update and observe the computed value/template. Equal notifications reject reference identity as the cause.

**Repair and verify:** Return a new object/array from update when changing value semantics. Inspect custom equality functions. Verify downstream computations and OnPush rendering without forced change detection. [Official contract](https://angular.dev/guide/signals).

## 3. Computed signal stops reacting to one input

**Mechanism:** Computed dependencies are dynamic: only signals actually read in the latest derivation are tracked.

**Probe and falsifier:** Toggle the branch that controls the read, then mutate each source independently. If the supposedly absent source is tracked, inspect scheduling or equality.

**Repair and verify:** Make dependencies reflect intended semantics; do not assume a skipped branch registered its reads. Verify both branch transitions and input updates. [Official contract](https://angular.dev/guide/signals).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```ts
// Preserve value-change notification for an object signal.
profile.update(previous => ({ ...previous, name: nextName }));
// Mutating previous.name and returning previous can retain the same identity.
```
