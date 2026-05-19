# Transcript — memory-design

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We want our support agent to 'remember' things about each customer. Plan: dump every conversation into a vector DB, retrieve top-k each turn, prepend to the prompt. Sound right?"

---

## Without skill (typical baseline)

> Yes, that's a common pattern. Use a vector DB like Pinecone or Weaviate. Embed each turn, store with the customer ID as metadata, retrieve top-5 most similar turns each new request, prepend to the system prompt. Tune chunk size and top-k as you go.
>
> A few tips: chunk conversations into ~300-token windows, add a recency boost to the similarity score, and filter by `customer_id` at query time so you don't leak across users.

Implements what was asked. Does not name the design failure.

---

## With skill (behavioural expectation)

> Stop. What you've described is a **conversation-chunks-in-a-vector-store** pipeline, and it's the worst long-term store. It will produce confidently wrong recall within weeks.
>
> The error is conflating four different memory types into one store:
>
> - **Working** — current turn. Lives in the prompt.
> - **Episodic** — what happened in this session. Recalled by recency.
> - **Semantic** — durable facts ("customer's plan tier", "preferred contact channel", "outstanding ticket #4421"). Recalled by entity lookup.
> - **Procedural** — how to handle classes of issue. This is a skill, not a memory write.
>
> Your vector dump turns all four into approximate-nearest-neighbour soup. Symptoms you'll see: stale preferences override new ones; episodic chatter buries hard facts; recall returns *something* even when the right answer is "I don't know"; cost grows; recall quality degrades.
>
> Refactor:
>
> 1. **Working** — keep nothing. Cleared at end of request.
> 2. **Episodic** — per-session, time-keyed, in-memory or short-TTL store. Cleared at session end (configurable; days at most).
> 3. **Semantic** — typed entity store. Schema like:
>
>    ```
>    {customer_id, kind: 'preference'|'fact'|'status', key, value, written_at, source, confidence, ttl}
>    ```
>    Write at episode boundaries (end of conversation), summarising what's *new and durable*. Recall by entity + key. Latest-write-wins on contradictory keys; surface conflicts when recency-bias is dangerous.
> 4. **Procedural** — agent prompts and skills, not memory.
>
> Five rules I'd want in your design:
>
> - **Recall budget per turn:** ≤5 episodic, ≤10 semantic. More is noise.
> - **Filter before rank:** customer_id → time window → relevance. Vector-only ranking returns nostalgia.
> - **TTLs are mandatory:** preferences months, status weeks, transient state hours.
> - **Show provenance:** `(source, written_at, confidence)` reach the model so it can reason about staleness.
> - **Negative recall is valid:** "no preference recorded" beats "best guess from old chunk".
>
> Anti-patterns I'm watching for:
>
> - One vector store as "the memory".
> - Writing every turn (signal-to-noise collapses).
> - No forgetting (cost climbs, recall degrades).
> - Confusing the context window with memory (stuffing the prompt is expensive amnesia).
> - Picking a vendor (mem0, Letta, Zep) before designing the four types.
>
> Eval before you ship: can the agent reach the same task success on a held-out set *with* memory loaded vs *without*? If memory doesn't move the needle, delete it.
>
> **Hard line:** if memory makes the agent slower or wronger on a held-out task, delete the memory. Default to no memory until evidence forces it.

---

## The diff

What changed because the skill fired:

- **Refused the vector-dump design.** Named the failure mode and its symptoms.
- **Decomposed memory into four types**, each with its own store, write rule, recall mechanism.
- **Added typed semantic schema** with TTL, provenance, conflict resolution.
- **Imposed recall budget and filter-before-rank.**
- **Surfaced negative recall** as a first-class result.
- **Demanded an eval gate** before shipping the memory feature.
- **Refused vendor-first reasoning.**

A naive answer wires the pipeline. A skilled answer rejects the design, decomposes the problem, and ties memory to a measurable task outcome.
