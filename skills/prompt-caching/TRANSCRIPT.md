# Transcript — prompt-caching

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We turned on prompt caching last week but our bill didn't go down much. What's wrong?"

---

## Without skill (typical baseline)

> Caching usually helps but it depends on your setup. Some things to check:
>
> - Make sure the cache is actually being read (check the response metadata for cached tokens).
> - Cache TTL might be too short for your call pattern.
> - Verify your prompt prefix is consistent across calls.
> - Some content can't be cached.
>
> Different providers cache differently — Anthropic uses explicit breakpoints, OpenAI auto-caches. What provider are you on?

Helpful but vague. No mental model, no diagnostic ladder.

---

## With skill (behavioural expectation)

> A bill that didn't move means **your cache hit rate is low or your cache reads aren't where you think they are**. Two questions answer this in five minutes:
>
> 1. **What is your current cache hit rate?** Pull `cache_read_input_tokens` (Anthropic) or `prompt_tokens_details.cached_tokens` (OpenAI) from your last 100 calls. Divide by total prompt tokens. If this is <20%, caching is misconfigured. If you can't pull it, that's task one — *if you can't measure it, you don't have caching*.
>
> 2. **What is above the cache boundary?** Walk me through your prompt order. The rule is: **static content above, dynamic below**. Tools → system prompt → long docs → conversation history → user turn. Any dynamic content (timestamp, request-id, per-call user data, reordered tool list) above the boundary destroys the cache. One character above the boundary is 0% hit rate.
>
> Most-common cache-killers I'm watching for:
>
> - **Dynamic timestamp in the system prompt** (`"Current time: 2026-05-19T11:34:12Z"`) — bypasses cache 100% of the time.
> - **Request-id or trace-id at the top** — same.
> - **Tool list reordered per call** — tool order is hashed.
> - **Per-user data interleaved with system prompt** instead of consolidated below.
> - **Anthropic ephemeral cache TTL is 5 minutes**; if your traffic has idle gaps >5 minutes, the cache is going cold between users.
>
> Provider-specific gotchas:
>
> - **Anthropic** — billing is asymmetric. Cache *writes* cost 125% of normal input tokens; *reads* cost 10%. A cache that misses costs you 25% more than no cache at all. Bill not moving means you're paying write premiums without read amortisation.
> - **OpenAI** — auto-cache requires ≥1024-token prefix and the prefix has to be stable to the token. No explicit knobs; if you're not seeing `cached_tokens`, your prefix isn't stable.
> - **Gemini** — implicit prefix caching + explicit `cachedContent` for long-lived caches. If you have a multi-hour stable doc, use explicit; you're missing free savings on implicit otherwise.
>
> **Hard line:** if you can't tell me your cache hit rate, you don't have caching — you have wishful thinking. Instrument first; tune second.

---

## The diff

What changed because the skill fired:

- **Demanded the hit-rate number** before suggesting a fix.
- **Reframed the problem** as cache-boundary placement, not "cache enabled/disabled".
- **Walked the prompt-order rule** (static above, dynamic below).
- **Listed common cache-killers** to scan their prompt for.
- **Surfaced the asymmetric billing trap** (cache miss costs *more* than no cache on Anthropic).
- **Provider-specific gotchas** instead of generic advice.
- **Invoked the hard line** on instrumentation before tuning.

A naive answer offers checks. A skilled answer makes the user measure first.
