# Gin: debugging playbook

Deeper case: [A second binder sees EOF although the request body was valid](boundary-case.md).

Use the [causal decision procedure](../../../../19-causal-decision-procedure.md) to check probe sensitivity and the [composed-failure guide](../../../../20-composed-failures.md) when one recipe leaves another symptom unexplained.

Start with the matching symptom below and inspect the actual code. Each recipe gives a concrete candidate mechanism, a discriminating probe, and a repair/verification path. These are reusable techniques, not recorded incidents or automatic fixes. Reject a recipe when its probe contradicts it; use the [guide](guide.md) for other boundaries.

Version scope matters: examples describe the APIs/modes named in each recipe. Identify the installed version and effective configuration before applying them. The linked official sources support the API mechanisms; the probes are investigation techniques. Use the [docs map](docs.md) only for an unresolved contract, changed version, or configuration difference.

## 1. Background logging shows another request's context

**Mechanism:** Gin contexts are reused; retaining *gin.Context after the handler returns can expose changed data.

**Probe and falsifier:** Block the goroutine until the handler returns, then send another request and compare synthetic markers. If the actual worker retains only independent values and no context pointer, reject this cause; one run without observed reuse is inconclusive.

**Repair and verify:** Prefer copied immutable inputs; c.Copy() supports read-only context access but does not extend response-writer lifetime or guarantee successful downstream work. Verify overlapping requests and cancellation requirements. [Official contract](https://gin-gonic.com/en/docs/middleware/goroutines-inside-a-middleware/).

## 2. Custom validation response still has status 400 or duplicate writes

**Mechanism:** Bind/MustBind can abort and write on binding failure; ShouldBind returns the error for caller-controlled formatting.

**Probe and falsifier:** Send malformed JSON through each binding path and inspect status before custom rendering. An uncommitted response rejects auto-write as the cause.

**Repair and verify:** Use ShouldBind when the handler owns the error response, return after handling it, and keep one writer. Verify malformed and valid inputs. [Official contract](https://gin-gonic.com/en/docs/binding/binding-and-validation/).

## 3. Unauthorized request still executes code after Abort

**Mechanism:** Abort stops pending handlers, not the remainder of the current Go function.

**Probe and falsifier:** Place a sentinel directly after AbortWithStatusJSON and invoke the rejecting branch. If unreachable already, inspect another handler or goroutine.

**Repair and verify:** Return immediately after the abort in the denying branch. Verify the sensitive side effect is absent and an authorized request still reaches it. [Official contract](https://pkg.go.dev/github.com/gin-gonic/gin#Context.Abort).

## Small implementation pattern

Adapt identifiers and imports to the existing project. This illustrates the relevant boundary; it is not a standalone application or an incident reproduction.

```go
if !allowed {
    c.AbortWithStatusJSON(403, gin.H{"error": "forbidden"})
    return // Abort does not return from this function.
}
```
