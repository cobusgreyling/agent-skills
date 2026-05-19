---
name: latency-budgeting
description: >-
  Budget and engineer latency for an LLM agent — TTFT, tokens-per-second,
  tool round-trips, parallelism, streaming. Use when the user is building a
  user-facing or real-time agent and mentions latency, p50, p95, p99, TTFT,
  streaming, throughput, time-to-first-token, slow agent, or asks "why is my
  agent slow?" / "how do I hit a 2-second latency target?".
tags:
  - latency
  - production
  - performance
  - user-experience
---

# Latency Budgeting

Latency is a feature; budget it before you build.

Agents fail user-acceptance tests on latency more often than on quality. A great answer at 12 seconds is worse, in product terms, than a B+ answer at 2 seconds for most interactive use cases. Latency must be engineered, not measured after.

## When to use this skill

- The user is building a user-facing chat, voice, or agentic UI.
- The user reports an agent that "works but is slow."
- The user is choosing a model tier and is about to default to the biggest one.
- The user is adding a sub-agent, a reflection step, or a guardrail and asks how to keep it snappy.

## Where time actually goes

In order of typical magnitude for an LLM agent call:

1. **Tool round-trips.** Network + backend; serial loops dominate. Often 50–80% of wall-clock.
2. **Time to first token (TTFT).** Model-dependent and load-dependent.
3. **Token generation.** Output tokens × tokens-per-second.
4. **Pre-flight overhead.** Auth, embedding lookups, cache reads.
5. **Client render.** Often overlooked; streaming hides it.

If you don't know which of these dominates, you cannot optimise. Trace it.

## Decision flow

1. **What is the latency target?** Pin a p50 *and* a p95 budget. No target = no design.
2. **Is this user-facing and interactive?** → stream by default. TTFT is the perceived latency.
3. **Are tool calls in the loop independent?** → parallelise them. Sequential is the default mistake.
4. **Is the model tier appropriate for the task?** → the smaller model is almost always fast enough for routing, classification, formatting.
5. **Is there a re-plan or reflection step?** → cap iterations; show progress streaming if it can't be removed.
6. **Are you doing RAG at query time?** → measure retrieval latency separately. It is often the silent killer.

## The five rules

1. **Budget per stage.** If a pipeline has five stages, each gets a written budget that sums to the total. No stage gets a blank cheque.
2. **Parallelise by default.** Sequential tool calls only when there's a real data dependency.
3. **Stream output.** TTFT matters more than total time for almost every interactive UX.
4. **Right-size the model.** Use the biggest model on the step that actually needs it (reasoning, synthesis), the smallest on the rest (routing, formatting).
5. **Cache the static prefix.** See `[[prompt-caching]]` — cache hits often halve TTFT.

## Anti-patterns to flag immediately

- **Sequential by default.** Two tool calls in series when the inputs don't depend on each other.
- **One model for everything.** Premium model for routing decisions a Haiku-tier model handles fine.
- **Unstreamed UX.** User stares at a spinner for 8 seconds while the answer is ready in chunks.
- **No traceable latency.** A p95 number with no per-stage breakdown is not actionable.
- **Reflection in the hot path.** Quality wrapper that triples latency without an A/B showing users care.
- **Long context window on hot paths.** TTFT scales with input length; trim aggressively.

## Streaming notes

- Stream as soon as the model emits tokens; do not buffer to "clean up" the output.
- If post-processing is required, stream a placeholder + replace, or stream into a structured UI that tolerates updates.
- Tool calls in the middle of a stream interrupt TTFT — design for it.

## Questions to ask the user

1. What is the **p50 / p95 target** in milliseconds? If "fast" is the answer, ask again.
2. What does the user **see** while waiting? Is anything streamed today?
3. Which steps are **independent** and could run in parallel today?
4. What **model tier** is each step using, and why?
5. What is the **latency of the slowest tool**, measured at p95?
6. Is the agent's latency **bimodal** (fast path + slow path)? Are users surfacing the bimodality?

## The hard line

**If a step has no latency budget, it has no budget.** Total p95 is a result, not a target — the targets live on the stages.

## Why this exists

Latency complaints in production almost always trace back to architectural decisions made without a budget — a sequential loop where parallel would do, a premium model where a small one would do, an unstreamed pipeline where streaming was free. Budgeting per stage forces the decisions to be made deliberately. See [link to article on agent latency].

## References

- `references/streaming.md` — UX patterns for streaming, partial outputs, mid-stream tool calls.
- `references/model-routing.md` — model-tier selection per step.
- `references/parallel-tools.md` — how to express parallel tool calls in major frameworks.
