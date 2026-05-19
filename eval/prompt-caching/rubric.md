# Scoring Rubric — prompt-caching eval

The scorer reads one agent response and the task's `checks` list. For each check, it returns `pass`, `fail`, or `partial`.

## Per-check criteria

### `flags-dynamic-prefix`

The response should:

- Identify that a dynamic value (timestamp, request id, user id, A/B variant, anything that changes per call) above the cache boundary changes the cache key and forces a write on every call.
- Explain *why* this destroys hit rate: the cache hash is computed over the full prefix up to the breakpoint.
- Propose a concrete fix: move the dynamic value below the boundary, into the user turn, into request metadata, or accept a scoped cache key.

**Pass:** all three. **Partial:** names the issue but proposes only a vague fix ("avoid dynamic content"). **Fail:** does not connect the symptom to the dynamic prefix; suggests increasing the cache budget or switching providers.

### `flags-no-measurement`

The response should:

- Refuse to tune or diagnose without the cache hit rate metric.
- Name the concrete signal: `cache_read_input_tokens` / `cache_creation_input_tokens` (Anthropic), `usage.prompt_tokens_details.cached_tokens` (OpenAI), or the Gemini equivalent.
- Treat "I think it's caching" or "the bill looks the same" as not-a-metric.

**Pass:** all three. **Partial:** asks for metrics but does not name the specific field. **Fail:** offers tuning advice without first asking for the hit rate, or accepts vibes as evidence.

### `flags-cache-write-cost`

The response should:

- Name the write-cost premium: Anthropic charges ~125% for cache writes and ~10% for reads.
- Explain the break-even: caching pays off only when reads dominate writes (rule of thumb: ≥1.3× reads per write on Anthropic).
- Recommend caching only the *stable* prefix, not dynamic content or user turns, because writes on dynamic content earn no read benefit.

**Pass:** all three. **Partial:** names the write premium but does not connect it to the break-even or to the user's specific symptom. **Fail:** treats cache writes as free; recommends caching more without diagnosing.

### `flags-unstable-ordering`

The response should:

- Identify that tool list order, system prompt content order, and message order are all part of the cache key.
- Explain that any per-call reordering changes the hash and forces a write.
- Recommend a deterministic order; bias model behaviour with `tool_choice`, descriptions, or system-prompt instructions instead of physical reordering.

**Pass:** all three. **Partial:** names that order matters but does not propose the alternative. **Fail:** suggests the reordering is fine and the cache should still work.

### `flags-cross-user-cache`

The response should:

- Identify that putting per-user content above the cache boundary either (a) destroys shared-prefix caching or (b) raises a privacy concern if a shared cache key leaks across tenants.
- Distinguish the two cases: per-user content *below* the boundary is fine; per-user content *above* the boundary is the problem.
- Recommend per-user cache scoping or moving personalisation below the boundary.

**Pass:** all three. **Partial:** notes the issue but conflates the privacy and hit-rate problems. **Fail:** waves at "be careful with multi-tenant caching" without naming the boundary as the determinant.

### `recommends-explicit-breakpoints`

The response should:

- Name the provider-correct mechanism: `cache_control: ephemeral` for Anthropic, automatic prefix caching for OpenAI, `cachedContent` (explicit) or implicit prefix caching for Gemini.
- Place the breakpoint correctly: at the boundary between stable and dynamic content (typically end of tools or end of system, or end of a long stable user message).
- Cite the relevant constraint: Anthropic has ≤4 breakpoints and a ~1024-token minimum cacheable block; OpenAI has a ~1024-token minimum; Gemini explicit cache is for long-lived (hours-to-days) content.

**Pass:** all three. **Partial:** names the mechanism but places the breakpoint vaguely. **Fail:** confuses providers (e.g. tells an Anthropic user that caching is automatic) or omits the mechanism entirely.

### `flags-ttl-cold-start`

The response should:

- Name the relevant TTL: Anthropic ephemeral cache is 5 minutes; OpenAI's auto cache is longer but not infinite; Gemini implicit is session-scoped; Gemini explicit is hours-to-days.
- Explain that idle periods cause cold starts — the next call after TTL pays the write cost again.
- Recommend a fitting mitigation: keepalive only if traffic justifies, or switch to Anthropic's 1-hour beta cache, or use Gemini `cachedContent` for very long-lived workloads.

**Pass:** all three. **Partial:** names the TTL but does not propose a mitigation tied to the user's pattern. **Fail:** treats the cold-start cost as a bug or recommends caching harder.

## Overall task scoring

A task is **passed** if all its listed checks return `pass`. A task is **partial** if at least one returns `partial` and the rest are `pass` or `partial`. A task is **failed** if any check returns `fail`.

The delta the eval measures: **(passed-with-skill − passed-without-skill) / 20**. A meaningful skill should produce ≥ +0.40 on this delta; a strong skill should produce ≥ +0.60.

## Judging notes

- Use a different model than the one being evaluated. Same-model self-judging is co-conspirator territory.
- Run with `temperature=0` for both eval generation and scoring.
- Prompt-caching advice is more numerical than tool-use-schema advice (TTLs, percentages, token counts). The judge should accept any numerically-correct value within ±10% — providers occasionally tweak these and a strict-equality match will go stale.
- See `rubric_anchors.md` for one anchored pass / partial / fail example per check.
