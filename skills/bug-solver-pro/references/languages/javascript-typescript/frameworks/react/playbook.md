# React: debugging playbook

Deeper case: [Editing the second row changes the first row's draft](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Repeated increments lose updates

**Mechanism:** Multiple setCount(count + 1) calls in one event read the same render snapshot; they are replacements rather than cumulative operations.

**Probe and falsifier:** Invoke two increments in one event and compare with two functional updates. If both produce the intended delta, find a different state owner.

**Repair and verify:** Use setCount(previous => previous + 1) when deriving from prior state. Keep updaters pure. Verify batched and independent interactions. [Official contract](https://react.dev/learn/queueing-a-series-of-state-updates).

## 2. Old request overwrites a newer selection

**Mechanism:** An effect's async response can arrive after a later effect has begun.

**Probe and falsifier:** Force A to finish after B; inspect the selected key versus the key attached to the committed response. If A cannot commit, this cause is rejected.

**Repair and verify:** Abort supported requests and/or ignore results from obsolete effect instances using cleanup. Verify reverse completion order and unmount; do not remove dependency entries to silence reruns. [Official contract](https://react.dev/reference/react/useEffect).

## 3. Development sends twice; disabling Strict Mode hides it

**Mechanism:** Strict Mode deliberately exercises an extra development setup/cleanup cycle; missing cleanup exposes subscriptions or effects that cannot restart safely.

**Probe and falsifier:** Count setup, cleanup, and live subscriptions across mount/unmount. If live resources return to baseline, duplicated logging alone does not prove a resource leak.

**Repair and verify:** Make setup reversible and cleanup symmetrical. Place user-triggered mutations in the appropriate event flow. Verify remount and production behavior; a run-once ref is not cleanup. [Official contract](https://react.dev/reference/react/useEffect).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```js
// Derive from the queued value, not the render's captured count.
setCount(previous => previous + 1);
setCount(previous => previous + 1);
```
