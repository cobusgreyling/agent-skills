---
name: agent-cost-modeling
description: >-
  Model the cost of an LLM agent before it ships, and after. Use when the
  user is planning a deployment, comparing patterns, choosing a model tier,
  or justifying a budget and mentions tokens per task, cost per task, unit
  economics, cost ceiling, cache hit rate, ReAct cost, multi-agent cost,
  or asks "how much will this cost?" / "is this economical at scale?".
tags:
  - cost
  - production
  - architecture
  - economics
---

# Agent Cost Modeling

Token math beats price-list math. Model your cost per task, not per call.

A model that costs $3/1M tokens is cheap until your agent burns 80k tokens per task at 5 calls per task with a 0% cache hit rate. The interesting unit is the task, and the interesting equation has six terms, not two.

## When to use this skill

- The user is planning a deployment and needs a unit-economics number.
- The user is comparing patterns (ReAct vs. Plan-and-Execute vs. Router) on cost.
- The user is comparing model tiers and only has price-list intuition.
- The user is debugging a cost spike and has no per-task breakdown.

## The cost-per-task equation

```
cost_per_task = Σ (calls_per_task × tokens_per_call × price_per_token)
              + retrieval_cost
              + tool_cost
              - cache_savings
```

Six terms. Skipping any of them is how forecasts miss by 5×.

## Decision flow

1. **What is the cost ceiling per task?** Number in dollars. Without it, you cannot pick a pattern or a model.
2. **What does the task **actually decompose into** — how many model calls, how many tool calls?** Sketch the call graph before pricing.
3. **What is the **prompt prefix** that repeats across calls? → that's your caching surface.** See `[[prompt-caching]]`.
4. **Which step needs the **biggest model**, and can the others use a smaller tier?** See `[[latency-budgeting]]` for the same principle on latency.
5. **What is the **failure-and-retry** rate? Retries are real cost.**

## Pattern-level cost overhead (rules of thumb)

- **Single-shot tool call** — baseline (1.0×).
- **ReAct loop** — 2–5× baseline depending on step count; dominated by repeated context resending.
- **Plan-and-Execute** — 1.5–2× baseline; plan reused across steps so the prefix caches well.
- **Reflexion / critic** — 2–4× baseline per iteration. Cap iterations hard or this number explodes.
- **Supervisor + N workers** — N+1× baseline best case; can be 2N+1× if workers re-pull the full context.
- **Hierarchical** — uncapped without explicit budget enforcement. Treat as a fire hazard.

Numbers approximate; the *ratios* are stable across providers. Use them to sanity-check architecture choices.

## The five rules

1. **Measure tokens per stage in dev.** Token counts on every span (see `[[agent-observability]]`).
2. **Caching is the first lever, not the last.** A well-laid-out prompt can halve the cost line without touching the model.
3. **The smallest model that passes the eval wins.** Default to "smaller until quality regresses", not "biggest because it's safer."
4. **Cap loops at the controller, not the prompt.** "Try up to 5 times" must be code, not vibes.
5. **Cost is per *successful* task.** Include retries, failed runs, and abandoned sessions in the denominator. Otherwise the number lies.

## Anti-patterns to flag immediately

- **Pricing the cheapest model with no quality eval.** The cheapest model that fails 30% of tasks is the most expensive.
- **Ignoring the cache.** A 60% cache hit rate routinely halves cost; not measuring it leaves money on the table.
- **Counting only model cost.** Retrieval, embedding, tool, observability all show up on the bill.
- **One agent, one price.** Cost is per task type — debugging an agent that handles three task shapes with one cost number is impossible.
- **No cost dashboard per release.** Cost drift is a regression; treat it like a perf regression.

## Questions to ask the user

1. What is the **cost ceiling per task** in dollars?
2. What is the **call graph** — how many model calls and tool calls per task, today?
3. What is the **token count per call** at p50 and p95?
4. What is the **cache hit rate**, and where is it measured?
5. What is the **retry rate**, and is it included in cost-per-task?
6. What is the **traffic shape** — is this 100 tasks/day or 100k/hour?

If the user can't answer (1), unit economics will be debated forever. Pin that first.

## The hard line

**No cost-per-task number, no production approval.** A cost ceiling without measurement is a wish.

## Why this exists

Cost surprises in production agents are almost always architectural, not pricing — wrong pattern, wrong model on the wrong step, no caching, runaway loops. The unit economics fall out of the architecture; arguing about list price is the wrong fight. See [link to article on agent unit economics].

## References

- `references/cost-equation.md` — the six terms worked through with examples.
- `references/pattern-cost-table.md` — per-pattern token overhead with sketches.
- `references/cost-dashboards.md` — what to put on the per-release cost dashboard.

## Related skills

- Cost falls out of architecture — start with [[agent-architecture-patterns]] if you have not.
- Caching is the first lever — [[prompt-caching]].
- Latency and cost trade against each other — [[latency-budgeting]].
- Measure tokens per stage from traces — [[agent-observability]].
- Cheapest model that passes the eval wins — [[agent-evaluation-harness]].
