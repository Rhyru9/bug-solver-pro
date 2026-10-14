# Actix Web: debugging playbook

Deeper case: [Increasing HTTP workers exhausts database connections](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Counter or cache changes depending on worker

**Mechanism:** HttpServer's application factory runs per worker; constructing mutable state inside it creates separate worker-local state.

**Probe and falsifier:** Compare one-worker and multiple-worker local runs, logging state pointer identity and values. One shared state identity rejects this mechanism.

**Repair and verify:** Construct web::Data outside the factory and clone it into each App when process-wide sharing is intended. Verify concurrency; this still does not share state across separate processes. [Official contract](https://actix.rs/docs/application/).

## 2. Data extractor cannot find state that appears registered

**Mechanism:** Data<T> extraction depends on the exact type and scoped registration; nested scope data can shadow outer data.

**Probe and falsifier:** Compare the handler's concrete T with each app_data registration, then invoke root and nested routes. Matching type/scope rejects this cause.

**Repair and verify:** Register the exact Data<T> at the intended scope and remove accidental shadowing. Verify both scopes; avoid adding unwraps or global fallback state. [Official contract](https://actix.rs/docs/extractors/).

## 3. Adding a second extractor breaks body parsing

**Mechanism:** Only one ordinary extractor can consume the request body; separate Json and body consumers compete for the same stream.

**Probe and falsifier:** Minimize the route to one body extractor, then inspect what the earlier extractor consumed. Persistent failure with one reader rejects this explanation.

**Repair and verify:** Parse once and derive other values from the parsed body, or use an explicit supported fallback extractor. Verify malformed JSON and size/content-type limits. [Official contract](https://actix.rs/docs/extractors/).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```rust
let state = web::Data::new(AppState::new()); // outside worker factory
HttpServer::new(move || {
    App::new().app_data(state.clone()).configure(routes)
}) // then bind/run using the project's existing server setup
```
