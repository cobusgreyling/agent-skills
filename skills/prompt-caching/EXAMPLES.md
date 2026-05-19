# Examples — prompt-caching

---

## Example 1 — Dynamic timestamp killing the cache

**User prompt:**
> "I enabled prompt caching but my hit rate is 0%. The prompt is mostly stable."

**Expected behaviour:** Walk the prompt top-down looking for dynamic content above the cache boundary — timestamps, request IDs, formatted "current user" blocks. Move them below the boundary. Re-measure.

---

## Example 2 — "Should I cache?"

**User prompt:**
> "My system prompt is 800 tokens, called 5 times a minute. Worth caching?"

**Expected behaviour:** Apply the decision flow: 800 tokens is below most providers' threshold (~1024 for OpenAI auto-cache, fine for Anthropic explicit). Recommend either growing the cacheable surface (move tool definitions, few-shots above the boundary) or skipping caching and focusing elsewhere.

---

## Example 3 — Cache without measurement

**User prompt:**
> "We turned on caching last week. Pretty sure it's working."

**Expected behaviour:** Ask for the actual hit rate from `usage.cached_tokens` (OpenAI) or `cache_read_input_tokens` (Anthropic). If no dashboard exists, that's the first task before any tuning.
