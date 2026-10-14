# Vue: debugging playbook

Deeper case: [Reading a computed sort changes another component's list](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Destructured primitive stops changing

**Mechanism:** In Vue 3 Composition API, destructuring a primitive property from reactive() copies its current value rather than preserving a reactive property access.

**Probe and falsifier:** Compare state.count with the destructured count after mutation. If both stay current, inspect the actual source type and compiler transform.

**Repair and verify:** Keep property access or use toRef/toRefs for an ordinary reactive object. Vue 3.5 reactive props destructuring is a separate compiler feature. Verify rerender without remounting. [Official contract](https://vuejs.org/guide/essentials/reactivity-fundamentals.html).

## 2. State is correct but immediate DOM measurement is stale

**Mechanism:** Vue batches DOM updates, so a measurement immediately after mutation can read the prior DOM.

**Probe and falsifier:** Measure before and after await nextTick() for the same state change. If both are stale, inspect refs, visibility, or transition timing.

**Repair and verify:** Use nextTick for post-update measurements; a watcher reading updated owner DOM may need flush: 'post'. Verify rapid changes and hidden-to-visible transitions rather than adding arbitrary timeouts. [Official contract](https://vuejs.org/guide/essentials/reactivity-fundamentals.html).

## 3. Watcher applies an old fetch after the user changes selection

**Mechanism:** Async watcher work can finish after its watched source has changed.

**Probe and falsifier:** Force request A to resolve after B and attach the source key to each result. If obsolete A cannot commit, investigate a different writer.

**Repair and verify:** Register cancellation/ignore cleanup with the watcher. onWatcherCleanup requires Vue 3.5+ and synchronous registration before await; use the supported cleanup callback otherwise. Verify reversal and component unmount. [Official contract](https://vuejs.org/guide/essentials/watchers.html).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```js
const state = reactive({ count: 0 });
const count = toRef(state, 'count'); // stays linked to state.count
state.count++;
await nextTick(); // only needed when observing the updated DOM
```
