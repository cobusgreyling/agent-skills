# Rubric Anchors — anchored examples per check

For each of the seven checks, one **pass**, one **partial**, one **fail** example. The scorer compares the response under test to these anchors before assigning a score. Anchors are written terse — match the shape, not the literal words.

## `flags-dynamic-prefix`

**Pass:**
> "`Today is {iso_timestamp}` at the top of the system prompt rewrites the cache key on every call. The hash is computed over the prefix up to your cache breakpoint, so one character changing = full write, zero reads. Two fixes: (1) move the timestamp into the user turn (below the boundary), or (2) drop it entirely and let the model ask if it needs the date. Tracing headers also belong outside the model-visible prompt."

**Partial:**
> "Yeah, dynamic content can hurt caching. Try to avoid putting changing values at the top."

**Fail:**
> "Anthropic's cache TTL is only 5 minutes — maybe your traffic isn't hot enough. Try sending more requests."

---

## `flags-no-measurement`

**Pass:**
> "Before we tune anything, what does `cache_read_input_tokens` vs `cache_creation_input_tokens` look like on a typical request? Those come back in the Anthropic `usage` object. 'The bill looks the same' isn't a metric — we need the read/write ratio per call to know whether the cache is hitting, not hitting, or hitting on the wrong block."

**Partial:**
> "Let's check whether the cache is actually firing. Can you share your usage metrics?"

**Fail:**
> "Try moving the system prompt earlier and adding another breakpoint. That usually helps."

---

## `flags-cache-write-cost`

**Pass:**
> "Anthropic prices cache writes at 125% of input and reads at 10%. You added `cache_control` to every message, so every turn pays a write premium and almost nothing reads — net cost goes up. Caching pays off only when reads are ≥ ~1.3× writes. Move the breakpoint to the last *stable* message (typically end of system / end of tool list); leave dynamic turns uncached."

**Partial:**
> "Cache writes cost more than regular tokens, so don't cache everything."

**Fail:**
> "Costs went up because you probably need more cache breakpoints. Try adding them at every assistant turn too."

---

## `flags-unstable-ordering`

**Pass:**
> "Tool list order is part of the cache key. Reordering by relevance score per call = 100% writes, 0% reads. Fix: keep a deterministic tool order and steer the model with `tool_choice`, with descriptions that make the right tool obviously correct, or with a one-line hint in the system prompt. Physical reordering buys you nothing the model can't get from words."

**Partial:**
> "Reordering tools might affect caching. Consider keeping them in a fixed order."

**Fail:**
> "Caching should still work as long as the tools themselves haven't changed."

---

## `flags-cross-user-cache`

**Pass:**
> "Two cases to separate: (1) per-user data *below* the cache boundary is fine — shared prefix caches once across tenants, user-specific tail is uncached, you get the read benefit. (2) Per-user data *above* the boundary means each tenant has its own cache key — no sharing, and a privacy hazard if you ever rebalance keys. Put personalisation in the user turn, breakpoint at the end of the shared system prompt."

**Partial:**
> "Be careful — multi-tenant caching can leak data or hurt hit rates."

**Fail:**
> "Just give each tenant their own API key and the caches will stay separate."

---

## `recommends-explicit-breakpoints`

**Pass:**
> "Anthropic requires explicit `cache_control: {type: 'ephemeral'}` on the block you want cached — it isn't automatic the way OpenAI is. Put it on the tools array and on the last system block; that gives you one warm-up call, then 10%-cost reads for the next 5 minutes. You get up to 4 breakpoints — save the others for conversation-history rotation. Note the ~1024-token minimum cacheable block."

**Partial:**
> "Add a `cache_control` field to your prompt and Anthropic will cache it."

**Fail:**
> "Anthropic auto-caches anything over 1k tokens, same as OpenAI. You don't need to do anything."

---

## `flags-ttl-cold-start`

**Pass:**
> "Anthropic's ephemeral cache TTL is 5 minutes from last read. Ten minutes idle = cold start; the next call pays the write premium again. Three options: (1) accept it if traffic is bursty and amortise across the hot window, (2) keepalive ping every ~4 minutes if traffic justifies it, (3) move to the 1-hour beta cache if your read pattern is hourly rather than per-minute. Not a bug."

**Partial:**
> "The cache only lasts a few minutes, so this is expected."

**Fail:**
> "Sounds like a regression — file a support ticket with Anthropic."
