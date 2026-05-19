---
name: agent-observability
description: >-
  Instrument an LLM agent so failures are diagnosable, traces are replayable,
  and evals can run against production data. Use when the user is moving an
  agent past prototype and mentions tracing, spans, OpenTelemetry, LangSmith,
  Langfuse, Arize, OpenLLMetry, structured logs, GenAI semantic conventions,
  or asks "how do I debug this agent in production?" / "what should I log?".
tags:
  - observability
  - tracing
  - production
  - opentelemetry
---

# Agent Observability

If you can't replay a failed trace, you can't fix the agent.

Logging "model returned X" is not observability. An agent has structure — graphs, loops, tool calls, retries, sub-agents — and the trace has to reflect that structure or the failure is opaque.

## When to use this skill

- The user is moving an agent from notebook to service.
- The user reports flaky or intermittent failures with no reproducer.
- The user is adopting OpenTelemetry, LangSmith, Langfuse, Arize, or similar.
- The user wants to run evals against real production traffic, not just a fixed set.

## What a complete trace looks like

A single user-facing request produces one trace, with nested spans for every step. Each span has:

- **Name** — `agent.plan`, `agent.tool_call.search_docs`, `agent.model_call`, `agent.reflect`.
- **Inputs and outputs** — verbatim, with PII redacted at write-time.
- **Attributes** — model name, model version, prompt version, token counts (prompt, completion, cached), latency, cost.
- **Status** — OK, error, fallback-taken.
- **Trace + span IDs** linking sub-agent calls back to the parent trace.

If any one of those is missing, the failure mode "the agent did something weird" is unfixable.

## Decision flow

1. **Are you past prototype?** → instrument. Now, not after the first incident.
2. **Does your framework emit OpenTelemetry-compatible spans?** → use them. The GenAI semantic conventions are stabilising; align early.
3. **Do you need replay** (deterministic re-run from a captured trace)? → log inputs + every random seed, temperature, model version, and tool response verbatim.
4. **Do you need production-eval** (sample real traces, score offline)? → ensure inputs and ground truth (or proxy labels) are captured.
5. **Do you need cost attribution?** → token counts on every span, rolled up to trace.

## The five rules

1. **One trace per user request.** Sub-agents and retries are spans inside it.
2. **Inputs and outputs verbatim.** Truncation hides bugs. Use a separate "long-content" store if needed.
3. **Standardise span names.** `<component>.<action>` — searchable, dashboardable.
4. **Token + cost on every model call.** Aggregating cost without per-span detail is reverse-engineering.
5. **Errors are typed.** `error.kind = tool_timeout`, not "tool failed".

## OpenTelemetry GenAI conventions (one-liner each)

- `gen_ai.system` — provider (`anthropic`, `openai`, `bedrock`, `vertex`).
- `gen_ai.request.model` — requested model.
- `gen_ai.response.model` — actually-used model (may differ).
- `gen_ai.usage.input_tokens` / `output_tokens` / `cached_tokens`.
- `gen_ai.operation.name` — `chat`, `embeddings`, `tool_call`.

Use them. Your future self with a different vendor will thank you.

## Anti-patterns to flag immediately

- **Print-debugging only.** Works in dev, useless in prod under concurrency.
- **No input capture.** "The model said this" without "given what input" is a story, not a trace.
- **One span per agent run.** Loops and tool calls collapse into a single opaque blob.
- **Sampling errors out.** Always trace 100% of errors; sample successes if cost demands.
- **Trace data with no eval-friendly schema.** If you can't replay a trace into the eval harness, it's write-only telemetry.
- **No cardinality discipline.** Per-user IDs as span names will blow up the backend.

## Questions to ask the user

1. What's the **first thing you look at** when an agent fails today? If the answer is "the logs", ask what's in them.
2. Can you **replay** a single failed request without modifying code?
3. Are **tool calls** traced with the same fidelity as model calls?
4. Is there **cost per request** attribution, or only monthly totals?
5. When a new model version ships, can you **diff** behaviour on real traffic?
6. Who owns the **dashboard**, and what's on it?

## The hard line

**Every production call gets a trace. Otherwise, you're guessing.** Sampling is fine for cost; zero coverage on errors is not.

## Why this exists

Most production-agent incidents are diagnosed by reading a trace, not by reading code. Agents that can't be traced can't be debugged, can't be evaluated against real traffic, and can't be improved with confidence. Observability is not a phase-2 concern. See [link to article on agent observability].

## References

- `references/span-shape.md` — span naming, attributes, error model.
- `references/otel-genai.md` — OpenTelemetry GenAI semantic conventions, current state.
- `references/eval-from-traces.md` — sampling real traces into an offline eval pipeline.
