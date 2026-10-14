# Express: Webhook signature fails only through the full middleware stack

Read with the [playbook](playbook.md). This closes a specific boundary gap identified in the [coverage audit](../../../../coverage/gap-audit.md); it is an authored technique, not an observed incident.

**Mechanism and prerequisites:** Signature verification may need the provider-defined byte representation, while an earlier JSON parser has consumed and transformed the stream. JSON.stringify(req.body) cannot reconstruct whitespace or original encoding.

**Discriminating probe:** Use a local signed fixture with intentionally varied JSON whitespace. Compare byte length/digest at ingress and at verification, without logging secrets/body contents. Divergence on the failing path supports transformation. Exact agreement with a failing signature rejects this candidate; a fresh unsigned payload is an invalid control.

**Repair, verification, and trap:** Mount a bounded raw-body route before competing parsers, or preserve bytes in the parser's verify hook if appropriate. Confirm what decompression stage the provider signs. Verify valid, altered, malformed, and oversized fixtures; never bypass signature verification. [Official contract](https://expressjs.com/en/5x/api/express/).

**Evidence discipline:** A non-failing probe rejects this mechanism only if its prerequisites were active, the real boundary executed, and the observation could detect the predicted failure. Otherwise mark it inconclusive. See [causal decision procedure](../../../../19-causal-decision-procedure.md).
