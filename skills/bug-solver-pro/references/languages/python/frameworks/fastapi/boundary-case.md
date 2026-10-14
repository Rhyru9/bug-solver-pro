# FastAPI: A supposedly filtered response exposes extra fields on one route

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** response_model handles filtering/validation on the normal return path; returning a Response subclass directly bypasses that conversion. A DTO annotation is not a universal output firewall.

**Discriminating probe:** Return the same synthetic object through the normal path and the actual direct-Response path, comparing raw response keys/status. Extra fields only in the direct path support bypass. Matching filtered wire payloads reject it; inspecting Python return values without serialization is inconclusive.

**Repair, verification, and trap:** Construct the approved output DTO explicitly before a deliberate direct response, or use the normal response-model path. Keep streaming and error responses in the audit. Verify sensitive extras are excluded and malformed output is surfaced appropriately; do not remove response validation to silence errors. [Official contract](https://fastapi.tiangolo.com/advanced/response-directly/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).

## Reproducible synthetic runtime evidence

The bundled [ASGI probe](../../../../../scripts/probes/fastapi_response_filter.py) runs without a network server or external effects using an interpreter where FastAPI is already installed:

```bash
python3 "<skill-root>/scripts/probes/fastapi_response_filter.py"
```

Observed in this audit: Python 3.14.7, FastAPI 0.135.3, Pydantic 2.12.5, Starlette 1.0.0. The normal response path returned only `id`; direct `JSONResponse` also returned the synthetic extra field; explicitly constructing the public DTO before the direct response excluded it. All three statuses were 200, separating successful delivery from correct output filtering.

This is an executed local synthetic contract probe, not a reproduced production incident. It does not establish streaming, middleware, network deployment, provider, or other-version behavior. Missing FastAPI causes an explicit dependency error; the probe does not install packages.
