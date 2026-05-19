---
name: prompt-caching
description: >-
  Use prompt caching correctly across Anthropic, OpenAI, Bedrock, and Gemini
  to cut cost and latency on hot paths. Use when the user is building a
  production LLM app and mentions prompt caching, cache hits, cache key, cache
  TTL, ephemeral cache, system-prompt caching, or asks "why is my cache hit
  rate low?" / "should I cache this?".
tags:
  - caching
  - cost
  - latency
  - production
  - claude
---

# Prompt Caching

Prompt caching is the easiest 5× cost win in production. Most teams botch the key design and never see the hit rate they were promised.

The model providers do the heavy lifting — your job is to put the right content above the cache boundary and to measure whether the cache is actually hitting.

## When to use this skill

- The user has a stable system prompt or tool list ≥1k tokens on a hot path.
- The user reports cost or latency problems on repeated calls.
- The user is comparing Anthropic, OpenAI, Bedrock, or Gemini for an agent.
- The user mentions "cache hit rate" but cannot quote theirs.

## Decision flow

1. **Is there a stable prefix ≥1k tokens that repeats across calls?** → cache it.
2. **Does the cached content change less often than every 5 minutes?** → cache it.
3. **Is the hot-path call volume ≥10/min from the same prefix?** → cache it.
4. **Is the content user-specific but stable for that user's session?** → per-user cache with a session-scoped key.
5. **Is the content fully dynamic per call?** → no cache. Compress the prompt instead.

## The five rules

1. **Static content above, dynamic below.** Tools, system prompt, large docs at the top. User turn at the bottom. Any dynamic injection above the cache boundary destroys the cache.
2. **Cache boundaries are explicit.** Anthropic uses `cache_control: ephemeral` breakpoints; OpenAI auto-caches with hashing. Know which knobs your provider gives you.
3. **TTL is short.** 5 minutes typical (Anthropic ephemeral). Plan for cold starts after idle periods, not just initial requests.
4. **Measure hit rate.** Every provider returns cache-read and cache-write token counts. Log them. Dashboard them.
5. **Cache-aware prompt layout costs nothing.** Refactor the prompt order *before* enabling caching.

## What to cache, in priority order

- **Tool/function definitions.** Long, stable, expensive on every call.
- **System prompt.** Especially when it includes few-shot examples or rubrics.
- **Long documents** (RAG context, schemas, transcripts) that repeat across turns of one conversation.
- **Conversation history** above the latest turn — for multi-turn agents.

## Anti-patterns to flag immediately

- **Dynamic timestamp or request-id in the system prompt.** Single character above the boundary = 0% hit rate.
- **Reordering tools per call.** Tool list order matters for the hash; keep it deterministic.
- **Caching everything.** Cache writes cost more than reads; cache the *stable* part only.
- **No cache-hit dashboard.** "I think it's caching" is not a metric.
- **Caching across users where prompts include other users' data.** Privacy bug *and* low hit rate.
- **Assuming the cache survives idle periods.** Anthropic ephemeral cache is 5 minutes; OpenAI's is longer but not infinite.

## Provider notes (one-liners)

- **Anthropic (Claude).** Explicit `cache_control` breakpoints on system/messages/tools. Up to 4 breakpoints. 5-minute TTL. Read tokens billed at 10%; write tokens at 125%.
- **OpenAI.** Automatic prefix caching for ≥1024-token prompts. No explicit breakpoints. Hit reported in `usage.prompt_tokens_details.cached_tokens`.
- **Google (Gemini).** Both implicit prefix caching and explicit `cachedContent` for long-lived caches (hours-to-days). Use explicit cache for large stable docs.
- **AWS Bedrock.** Inherits per-provider semantics; verify the model + region supports caching before designing around it.

## Questions to ask the user

1. What is the **prefix length** and **call rate** for the hot path?
2. What is the **current hit rate**? If unknown, that's task one.
3. Which **dynamic value** is highest in the prompt today, and can it move below the boundary?
4. Is the workload **interactive** (cache survives between user turns) or **batch** (caches go cold between requests)?
5. What is the **cost target** per task, and what fraction of that is prompt tokens?

## The hard line

**If you can't tell me your cache hit rate, you don't have caching — you have wishful thinking.** Instrument first; tune second.

## Why this exists

Caching is the single biggest lever on production cost for any agent with a non-trivial system prompt or tool list, yet most teams either skip it or implement it in a way that quietly fails. A 10-minute prompt-layout refactor often beats weeks of model-swapping. See [link to article on prompt caching].

## References

- `references/anthropic-caching.md` — breakpoint placement, billing math, gotchas.
- `references/openai-caching.md` — what auto-caches, what doesn't, how to read `cached_tokens`.
- `references/gemini-caching.md` — implicit vs explicit cache, when to use which.
- `references/cost-math.md` — when caching breaks even.

## Related skills

- Caching is the first cost lever — [[agent-cost-modeling]].
- Cache hits cut TTFT, not just cost — [[latency-budgeting]].
- Prefix layout depends on architecture — [[agent-architecture-patterns]].
- Tool definitions cache (or quietly don't) — [[tool-use-schema-design]].
