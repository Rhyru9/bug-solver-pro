# Express: debugging playbook

Deeper case: [Webhook signature fails only through the full middleware stack](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Async rejection misses the error handler

**Mechanism:** Express 4 and Express 5 differ: v5 forwards rejected returned promises; v4 needs forwarding. Detached promises are outside either returned chain.

**Probe and falsifier:** Use a rejecting awaited dependency through the real router; record whether the four-argument error handler runs. If it runs exactly once, investigate elsewhere.

**Repair and verify:** Return/await the work; use a compatible catch(next) wrapper for v4, avoid forwarding twice, and return after responding. Verify one response and one error report. [Official contract](https://expressjs.com/en/guide/error-handling/).

## 2. Headers already sent hides the original exception

**Mechanism:** An earlier send, stream write, or missing return committed the response before a later error.

**Probe and falsifier:** Record headersSent and the first response write, then trigger the failure before and after that point. If no write preceded failure, this mechanism is rejected.

**Repair and verify:** Give one branch ownership of the response; delegate with next(err) when headers are already sent. Do not send a second JSON error. Verify early and streaming failures. [Official contract](https://expressjs.com/en/guide/error-handling/).

## 3. HTTPS cookies or client IP differ behind a proxy

**Mechanism:** req.protocol, req.secure, and req.ip depend on trust proxy and the actual forwarded-header chain.

**Probe and falsifier:** Compare direct and proxy requests with sanitized protocol/IP observations. If the proxy-derived values are correct, inspect cookie attributes/session storage instead.

**Repair and verify:** Configure only the actual trusted proxy path and ensure it overwrites forwarded headers. Do not enable trust proxy indiscriminately. Verify both legitimate forwarding and untrusted-header input. [Official contract](https://expressjs.com/en/guide/behind-proxies/).
