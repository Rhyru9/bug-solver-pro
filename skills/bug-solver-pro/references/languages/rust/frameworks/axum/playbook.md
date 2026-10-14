# Axum: debugging playbook

Deeper case: [Adding authentication changes unknown URLs from 404 to 401](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Handler signature fails or body is unexpectedly unavailable

**Mechanism:** The body is a consumable stream; body-consuming extractors belong last and cannot independently consume it twice.

**Probe and falsifier:** Minimize to parts extractors plus one final Json<T>; inspect middleware for prior body consumption. Failure before any body read rejects the double-consumption explanation.

**Repair and verify:** Extract parts first, consume once, and derive multiple views from the parsed body. Buffer only with a justified size limit. Verify malformed input and body-limit rejection. [Official contract](https://docs.rs/axum/latest/axum/extract/index.html).

## 2. New routes silently miss an existing middleware layer

**Mechanism:** Router.layer applies to routes already registered at that point; building additional routes later can leave them outside the layer.

**Probe and falsifier:** Exercise one route registered before and one after layer application, with a middleware sentinel. Equal coverage rejects registration order.

**Repair and verify:** Compose the complete intended router then apply the layer, or attach route layers explicitly. Verify allowed and rejected requests for every affected route; do not infer coverage from one endpoint. [Official contract](https://docs.rs/axum/latest/axum/struct.Router.html).

## 3. Invalid input bypasses the handler's custom error response

**Mechanism:** Extractor rejection occurs before handler body execution; converting only handler errors cannot customize that rejection.

**Probe and falsifier:** Send malformed JSON and set a handler-entry sentinel. If entry occurs, the failure originates later.

**Repair and verify:** Accept Result<Json<T>, JsonRejection> or implement a deliberate custom extractor when the API needs custom formatting. Preserve rejection status/details safely. Verify malformed syntax, type errors, and valid JSON. [Official contract](https://docs.rs/axum/latest/axum/extract/index.html).
