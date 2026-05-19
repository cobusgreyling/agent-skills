---
name: context-window-hygiene
description: >-
  Manage what enters and stays in the context window — pruning, compaction,
  summary fidelity, ordering — so the agent stays coherent on long runs
  without inflating cost. Use when the user is hitting context limits,
  running long agentic loops, paying for full-history replays, or asks
  "how do I keep context manageable?" / "the agent forgets things after
  N turns".
tags:
  - context-engineering
  - cost
  - latency
  - architecture
---

# Context Window Hygiene

A bigger context window is not a memory upgrade. It is a more expensive way to be wrong.

The model attends to the prompt it actually sees. Long contexts hide signal under noise — middle-of-context recall degrades, key facts get out-ranked by chatter, and cost scales linearly with every replayed turn. Hygiene is about removing what doesn't earn its place, not adding more.

## When to use this skill

- The user is running a long agentic loop (tool-use loop, multi-turn task).
- The user reports the agent "forgetting" mid-run, or contradicting earlier turns.
- The user is paying for context tokens that grow linearly with conversation length.
- The user is considering "just use a 1M-token window" as a solution to anything.

## What enters context — name the categories

Every token in the prompt is one of:

- **System prompt** — fixed instructions. Should be cache-aligned.
- **Skill / tool definitions** — fixed shapes. Cache-aligned.
- **Conversation history** — previous turns. Pruning candidates.
- **Tool results** — output of tool calls. Often the biggest growth vector.
- **Retrieved context** — RAG hits, memory recall. Bounded budget.
- **Current turn** — user input.

Distinguish them. They have different lifetimes, different cache behaviour, different prune rules.

## Decision flow

1. **Is context growth driven by tool results?** → yes (it usually is) → summarise large tool results before they enter history.
2. **Is context growth driven by long conversation?** → yes → compaction at turn N, not at the context limit.
3. **Are old turns still being read?** → no → drop them. The model can't read what isn't there, but it pays attention to what is.
4. **Is retrieved context unbounded?** → yes → set a recall budget (≤K items, ≤T tokens) — see [[memory-design]] and [[rag-vs-context-engineering]].
5. **Is the system prompt mutating per call?** → cache is dead. Stabilise the prefix.

## The hygiene rules

1. **Cache-aligned order.** Stable prefix first (system → tools → fixed examples), variable suffix last (history → current turn). Cache miss is paid per request; alignment turns long history from a cost into a free re-read.
2. **Summarise tool results that exceed a threshold.** Raw 50KB JSON in history poisons every subsequent turn. Summarise with a typed schema before storing in conversation.
3. **Compact at fixed boundaries, not at the cliff.** Compact at turn 10, 20, 30 — not when you hit the context limit. Predictable cost, predictable behaviour.
4. **Lossy compaction is fine; lying compaction is not.** Drop tool-result chatter; keep facts the agent decided on. Never invent context that wasn't there.
5. **Recency + saliency, not recency alone.** Drop the most-recent-but-irrelevant before the older-but-load-bearing. The model uses what's there, not what was there.

## Anti-patterns to flag immediately

- **"Just use a 1M-token window."** Solves cost-per-call by raising every-call's cost. Doesn't solve middle-of-context recall degradation. Doesn't solve attention drift.
- **Full-history replay with no pruning.** Cost grows quadratic-ish in real workloads (every call pays for every prior turn).
- **Tool results in history verbatim.** Raw HTML, full DB dumps, base64 — all attend, all confuse, all cost.
- **Mutating system prompt per call** ("Current time is X"). Kills cache; cost balloons; cache hit rate hides in the metrics.
- **Compacting at the cliff.** Hitting 95% context, panicking, summarising — produces lossy compaction at the worst moment.
- **Free-text summary memory.** Summaries written as paragraphs lose precision; key facts blur.
- **No measurement of attention.** "It feels like the agent forgot" with no diagnostic from the trace.
- **Confusing context window with memory.** See [[memory-design]] — they aren't the same.

## Diagnostic checklist when the agent "forgets"

1. Was the fact ever in the context window of the failing call? (Read the trace.)
2. Was it in the *first quarter* or the *middle* of the prompt? Middle-of-context recall degrades; surface it.
3. Was it surrounded by noisy tool output that out-competes for attention?
4. Did a compaction step drop or paraphrase it?
5. Is the fact in a documented format the model is following, or buried in prose?

## Questions to ask the user

1. What's in your **prompt prefix** vs **suffix** — is it cache-aligned?
2. How big is the average **tool result**? Are they **summarised** before re-entry?
3. What's the **compaction policy** — turn boundary, token threshold, or "when we hit the limit"?
4. What's the **recall budget** for memory / RAG hits in a single turn?
5. When the agent "forgets", can you trace **what was in context** at that call?
6. Is your system prompt **stable** across calls, or does it change per-request?

## The hard line

**Every token in context must be load-bearing on this turn's decision.** If a token isn't, it's noise — and noise costs you in money, latency, and quality.

## Why this exists

The "1M-token context" pitch made everyone forget that attention degrades with length, recall degrades in the middle of long contexts, and cost scales linearly with every token shipped. Hygiene — pruning, summarisation, cache alignment, compaction at boundaries — buys back the coherence that long contexts lose, at a fraction of the cost.

## References

- `references/prefix-order.md` — cache-aligned prompt order, system → tools → examples → history → turn.
- `references/compaction.md` — when, how, and what to drop; lossy vs lying; summarisation templates.
- `references/tool-result-summarisation.md` — schemas for compacting big tool outputs before they enter history.

## Related skills

- Hygiene is not memory — [[memory-design]].
- Hygiene is not retrieval — [[rag-vs-context-engineering]].
- Hygiene drives cache hit rate — [[prompt-caching]].
- Hygiene drives cost — [[agent-cost-modeling]].
- Hygiene drives latency — [[latency-budgeting]].
- Long runs need observability — [[agent-observability]].
- Tool result size is set in [[tool-use-schema-design]].
