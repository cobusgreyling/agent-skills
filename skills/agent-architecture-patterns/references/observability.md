# Observability — what to log, span shape, eval scaffolding

You cannot fix an agent you cannot see. Instrument before you scale.

## Minimum log shape per step

Every agent step emits one structured record:

```json
{
  "trace_id": "uuid",
  "step_id": 7,
  "agent": "executor",
  "input": { "messages": [...], "state_hash": "abc123" },
  "model": "claude-opus-4-7",
  "tool_calls": [{ "name": "search", "args": {...}, "latency_ms": 412 }],
  "output": { "text": "...", "tokens_in": 1240, "tokens_out": 318 },
  "cost_usd": 0.0094,
  "wallclock_ms": 1880,
  "terminated": false
}
```

Non-negotiable fields: `trace_id`, `step_id`, `tokens_in/out`, `cost_usd`. Without these you cannot debug cost regressions.

## Span hierarchy

Treat each agent invocation as a trace; each step as a span; each tool call as a child span. OpenTelemetry semantics work — `gen_ai.*` attributes are the emerging convention.

- Trace: full task, end-to-end.
- Span: one model call (one ReAct step, one planner call, one critic call).
- Child span: one tool execution.

If you use LangSmith, Phoenix (Arize), Braintrust, or Langfuse, they emit this shape natively. Pick one and stay.

## Eval harness

Three layers, build in this order:

1. **Smoke tests.** ~20 hand-picked inputs covering common shapes. Run on every commit. Fail loudly on schema breaks.
2. **Golden set.** ~100 inputs with expected outputs or rubric checks. Run nightly. Track pass-rate over time.
3. **Production replay.** Sample real traces, replay against the candidate graph, diff outputs. Run before any prompt or graph change ships.

Common mistake: skipping (1) and jumping to LLM-as-judge. Judges have their own biases; calibrate them against (2) before you trust them.

## Cost and latency budgets

Each agent gets a hard budget per task:

- `max_tokens_total`
- `max_wallclock_ms`
- `max_steps`

Enforce inside the loop, not only at the edge. Log the breach reason so you can distinguish "hit step cap" from "hit token cap".

## Red flags in traces

- **Step count climbing** week over week on the same task class → drift in tool reliability or prompt.
- **Tokens-per-step climbing** → state object growing unbounded.
- **Same tool called >3 times per task** → missing memoization or a broken observation parse.
- **Critic-actor ratio approaching 1:1** → critic isn't rejecting anything; the rubric is too loose.
