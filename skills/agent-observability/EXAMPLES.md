# Examples — agent-observability

---

## Example 1 — Opaque failure

**User prompt:**
> "The agent gave a weird answer to a user yesterday. I can't reproduce it. Help."

**Expected behaviour:** Diagnose the missing observability before debugging the agent. Was the request traced? Are inputs captured verbatim? Are tool calls in the trace? Without those, the failure isn't fixable — the first task is to instrument, then wait for the next occurrence.

---

## Example 2 — Logging the wrong things

**User prompt:**
> "We log model responses to a file. Is that enough?"

**Expected behaviour:** No. A response without the input, the tool calls that produced it, the model version, and the timing is half a story. Walk the user through the minimum span shape and recommend an OpenTelemetry-compatible tracer.

---

## Example 3 — Sampling errors

**User prompt:**
> "We sample 1% of traces to keep costs down."

**Expected behaviour:** Sampling successes is fine; sampling errors is not. Errors should be 100% traced. If cost is the issue, sample successes more aggressively and keep error-trace coverage at 100%.
