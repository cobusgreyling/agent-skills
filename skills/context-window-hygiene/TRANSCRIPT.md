# Transcript — context-window-hygiene

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "Our coding agent runs a tool-use loop for ~30 turns per task. Cost per task has 3× over the last month even though the task hasn't changed. We're considering switching to a model with a bigger context window. Smart move?"

---

## Without skill (typical baseline)

> A larger context window might help if you're truncating history — but it'll also cost more per call. Better short-term move: enable prompt caching on your system prompt and tools, that should cut input cost by ~70% on cached portions. Also consider summarising older turns into a brief recap to reduce prompt size.

Names a few correct moves. Doesn't diagnose the growth vector or impose hygiene as a discipline.

---

## With skill (behavioural expectation)

> Bigger context is the wrong lever. Your cost-per-task tripled on the same workload, which means tokens-per-call grew. Find the growth vector first; the answer is almost never "we need more window".
>
> Categorise what's in your prompt every turn:
>
> - **System prompt** (fixed) — should be cached.
> - **Tool definitions** (fixed) — should be cached.
> - **Conversation history** (grows) — pruning candidate.
> - **Tool results** (grows fast) — usually the biggest culprit.
> - **Retrieved context** (RAG / memory hits) — bound by recall budget.
> - **Current turn** (fixed-ish).
>
> Hygiene rules, in order of leverage:
>
> 1. **Cache-align the prefix.** System → tools → fixed examples → history → current turn. Stable first, variable last. If your tool definitions or system prompt are after a variable section, the cache breaks every turn. Confirm cache hit rate in your traces.
>
> 2. **Find and fix the tool-result growth.** In a 30-turn loop, raw tool outputs are usually the dominant cost. Each tool result entering history is paid for on every subsequent call. Fix: summarise tool results before they go into history. Each result becomes `{result_id, kind, key_fields, summary}`; raw payload stored externally; re-fetched only if the agent decides it's needed (which is rare in practice).
>
> 3. **Compact at fixed turn boundaries.** Compact at turn 10, 20, 30 — not when you hit the cliff. Predictable behaviour, predictable cost. Compaction preserves *facts the agent decided* verbatim and drops tool-result chatter. Lossy is fine; lying is not.
>
> 4. **Bound retrieval recall per turn.** ≤K items, ≤T tokens. Vector-store hits that don't make it into a recall budget become noise.
>
> 5. **Promote durable constraints to the system prompt.** Anything that must hold across all 30 turns belongs in the stable prefix, not buried in turn-1 chat. Middle-of-context recall is unreliable on long prompts.
>
> 6. **Don't mutate the system prompt per call.** "Current time is X" in the system breaks cache. If you need time, put it in user-turn metadata.
>
> Why bigger context isn't the answer:
>
> - **Cost scales linearly with tokens shipped.** A 1M model on 30-turn tasks pays for every prior turn on every call. Worse than your current cost, not better, unless you also fix the growth.
> - **Middle-of-context recall degrades.** The agent already isn't reading the middle of the long context reliably. More window doesn't fix that.
> - **Cache savings are paid on the prefix, not the bloat.** Bigger window doesn't make tool-result bloat cheaper.
>
> Anti-patterns I'm watching for:
>
> - **Full-history replay** with no pruning.
> - **Tool results in history verbatim** (raw HTML, big JSON, base64).
> - **Mutating system prompt per call** (kills cache silently).
> - **Compaction at the cliff** (panic summarisation at 95% context).
> - **Free-text summary memory** that paraphrases facts into vagueness.
> - **"Just use a bigger window"** as the fix.
> - **No measurement of attention** — "the agent forgot" with no trace diagnostic.
>
> Diagnostic checklist when the agent forgets something:
>
> 1. Was the fact actually in context at the failing call? (Read the trace.)
> 2. Was it in the first quarter, middle, or last quarter?
> 3. Was it out-competed by noisy tool output?
> 4. Did compaction drop or paraphrase it?
> 5. Is it in a clean documented format or buried in prose?
>
> Six questions:
>
> 1. Is your prompt **cache-aligned**?
> 2. How big are tool results, and are they **summarised** before re-entry?
> 3. What's your **compaction policy** — turn boundary, token threshold, or cliff?
> 4. What's the **recall budget** per turn?
> 5. Can you **read what was in context** at the failing call?
> 6. Is your system prompt **stable** across calls?
>
> Likely outcome: tool-result summarisation alone cuts cost-per-task 40–70% on a typical 30-turn agentic loop. Cache alignment cuts another 20–40% if you weren't aligned. Bigger context window: unnecessary, more expensive.
>
> **Hard line:** every token in context must be load-bearing on this turn's decision. If a token isn't, it's noise — and noise costs you in money, latency, and quality.

---

## The diff

What changed because the skill fired:

- **Refused the bigger-window framing.** Diagnosed the growth vector first.
- **Categorised prompt contents** and named the dominant cost (tool results).
- **Required cache alignment** of the prefix.
- **Imposed tool-result summarisation, fixed-boundary compaction, recall budget.**
- **Surfaced middle-of-context recall degradation** as a reason bigger windows don't fix forgetting.
- **Provided a forget-the-fact diagnostic** the user can run on traces.
- **Refused mutating system prompts** as a silent cache killer.

A naive answer reaches for a bigger window or "enable caching". A skilled answer diagnoses the growth, sets hygiene rules, and treats the context window as a scarce resource that needs active curation.
