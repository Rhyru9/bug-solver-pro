# Svelte: debugging playbook

Deeper case: [An effect ignores a value read after await](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. A variable copied out of $state stops tracking updates

**Mechanism:** In Svelte 5 runes mode, destructuring a $state proxy reads the values at that moment; it is not a live binding.

**Probe and falsifier:** Mutate the original proxy and compare direct property access with the copied primitive. If both update, inspect a compiler-supported special case.

**Repair and verify:** Use direct access or a suitable $derived expression for the live projection. Verify a later mutation, not just initial rendering. Do not apply runes syntax to an older compiler. [Official contract](https://svelte.dev/docs/svelte/$state).

## 2. A computed label updates only once

**Mechanism:** A plain initialization from reactive state is a snapshot; derived state needs an actual reactive dependency.

**Probe and falsifier:** Change the input twice and compare the label with a $derived version. If the original follows both changes, find another stale writer.

**Repair and verify:** Represent the calculation with $derived/$derived.by in runes mode and keep derivation free of effects. Verify all dependency branches. [Official contract](https://svelte.dev/docs/svelte/$derived).

## 3. SSR output lacks data populated by $effect

**Mechanism:** $effect runs in the browser, so data required for server rendering cannot depend on it.

**Probe and falsifier:** Compare raw server HTML with hydrated output. If server data is already present, the discrepancy has another cause.

**Repair and verify:** Use derived state for pure calculations and the app's server/load data path for SSR requirements. Reserve effects for external synchronization and return cleanup for subscriptions. Verify SSR and remount. [Official contract](https://svelte.dev/docs/svelte/$effect).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```js
// Svelte 5 runes mode
let item = $state({ price: 10, quantity: 2 });
let total = $derived(item.price * item.quantity);
// Plain `let total = item.price * item.quantity` is only initialization.
```
