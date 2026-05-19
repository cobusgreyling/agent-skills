---
name: memory-design
description: >-
  Design memory for an LLM agent — what to keep, where to keep it, and when
  memory hurts more than it helps. Use when the user is adding memory to an
  agent and mentions short-term memory, long-term memory, episodic, semantic,
  conversation history, summary memory, vector memory, memory store, mem0,
  Letta, MemGPT, or asks "should this agent remember?" / "why is the agent
  recalling the wrong thing?".
tags:
  - memory
  - architecture
  - context-engineering
  - production
---

# Memory Design

Memory is the most over-built and under-designed part of an agent.

The default question is "what should the agent remember?" The better question is "what *must* the agent forget so the next turn works?" Memory that doesn't earn its place poisons recall, inflates cost, and produces confidently wrong answers.

## When to use this skill

- The user is adding "memory" to a chatbot, copilot, or task agent.
- The user reports the agent recalling stale, wrong, or irrelevant facts.
- The user is choosing between full-history, summary, vector store, or a memory framework (mem0, Letta, MemGPT, Zep).
- The user is conflating "context window" with "memory" — they are not the same.

## The four memory types

Distinguish before designing. Mixing them is the root cause of most "memory bugs".

- **Working** — current turn's context. Lives in the prompt. Cleared at end of request.
- **Episodic** — what happened in this session / thread. Indexed by time; recalled by recency or relevance.
- **Semantic** — durable facts about the user, project, world. Indexed by entity; recalled by lookup.
- **Procedural** — how to do things (skills, tool-use patterns, workflows). Indexed by task type; recalled by trigger.

Each has a different write rule, retention policy, and recall mechanism. If your design has one memory store, you have a bug waiting.

## Decision flow

Walk this before adding any memory.

1. **Does the task need information beyond the current turn?** → no? Use no memory. Stateless wins on debuggability.
2. **Is the information lifecycle bounded by the session?** → episodic only. Don't persist past session end.
3. **Is the information a stable fact about the user or world?** → semantic. Write through a typed entity store, not a vector dump.
4. **Is the information a learned pattern of how to act?** → procedural. This is a skill or prompt update, not a memory write.
5. **Does recall ever return contradictory items?** → memory needs conflict resolution, not more recall.
6. **Can the agent operate correctly if memory is empty?** → yes? Memory is an enhancement. No? You've designed a brittle dependency.

## Write rules

- **Write at episode boundaries, not turn boundaries.** Per-turn writes flood the store with low-signal noise.
- **Summarise before writing semantic memory.** Raw conversation chunks make the worst long-term store.
- **Type every memory.** `{kind: 'preference', entity: 'user', key: 'tone', value: 'terse'}` beats a free-text blob.
- **Set a TTL.** No memory is forever. Preferences last months; project state lasts weeks; session state lasts hours.
- **Idempotency on write.** "User prefers terse responses" should not appear 40 times in semantic memory.

## Recall rules

- **Filter before ranking.** Entity match, then time window, then relevance. Vector-only recall returns nostalgia.
- **Recall budget per turn.** ≤5 episodic items, ≤10 semantic items. More is noise.
- **Show provenance.** Every recalled item carries `(source, written_at, confidence)`. The agent reasons about staleness.
- **Conflict resolution is part of recall.** When two facts contradict, latest-write wins by default; surface the conflict for high-stakes decisions.
- **Negative recall matters.** "I checked and found nothing about X" is a valid result. Silent empty recall is a bug.

## Anti-patterns to flag immediately

- **One vector store as "the memory".** Different memory types have different shapes; one store flattens them and ruins recall.
- **Dumping conversation history into RAG.** You get the worst of both: stale chunks, no entity grounding, retrieval drift.
- **Writing every turn.** Signal-to-noise collapses; old facts get buried under restatements.
- **Recalling without filtering by user/session.** Cross-tenant leakage; cross-session confusion.
- **No forgetting.** Memory grows; recall degrades; cost climbs. TTL is not optional.
- **Memory framework as architecture.** "We use mem0" is not a memory design; it's a vendor choice.
- **Confusing context window with memory.** Stuffing the prompt is not memory — it's expensive amnesia.

## Questions to ask the user

1. What **decision** does memory enable that's impossible without it? If you can't name one, you don't need memory.
2. Which memory **type** is each piece — working, episodic, semantic, procedural?
3. What's the **write trigger** — every turn, end of session, explicit save, agent-initiated?
4. What's the **recall budget** per turn — count and tokens?
5. What's the **TTL** per memory type?
6. How does the agent **detect** and **resolve** contradictory memories?
7. What's the **eval** for memory — does loading it improve task success, or just inflate latency?

## The hard line

**If memory makes the agent slower or wronger on a held-out task, delete the memory.** Memory is a load-bearing feature; treat it like one. Default to no memory until evidence forces it.

## Why this exists

Most agent "memory" deployments are vector-store retrieval pipelines re-skinned as memory. They retrieve confidently wrong items, contaminate recall, and degrade with use. Designing for the four memory types separately — with explicit write rules, recall budgets, and TTLs — converts memory from a liability into a feature.

## References

- `references/types.md` — working / episodic / semantic / procedural — what each looks like in storage.
- `references/write-and-recall.md` — patterns for write triggers, recall filters, and conflict resolution.
- `references/frameworks.md` — mem0, Letta, MemGPT, Zep — what each does well, where each leaks.

## Related skills

- Memory is not the same as retrieval — [[rag-vs-context-engineering]].
- Memory contents end up in the prompt — [[context-window-hygiene]].
- Memory writes/reads are spans in the trace — [[agent-observability]].
- Memory shape is set by the architecture — [[agent-architecture-patterns]].
- Memory load is part of cost per task — [[agent-cost-modeling]].
