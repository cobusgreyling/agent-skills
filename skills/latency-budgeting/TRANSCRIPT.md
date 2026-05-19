# Transcript — latency-budgeting

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "My agent takes 12 seconds end-to-end. Users complain it's slow. How do I make it faster?"

---

## Without skill (typical baseline)

> Twelve seconds is slow for an interactive UX. A few things to try:
>
> - Use a smaller model — Haiku or GPT-4o-mini are much faster.
> - Add streaming so users see output as it's generated.
> - Cache the system prompt if it's long.
> - Profile to see where time is going.
>
> Streaming usually has the biggest perceived-latency impact. Try that first.

Reasonable suggestions, presented as a menu. No budget, no diagnosis, no stage breakdown.

---

## With skill (behavioural expectation)

> Twelve seconds is a result, not a target. I cannot recommend a fix until you have:
>
> 1. **A p50 and a p95 budget**, in milliseconds. "Fast" is not a target. "<2.5s p95 TTFT, <8s p95 total" is a target.
> 2. **A per-stage latency breakdown**. Twelve seconds where? If you don't know, that's the first task.
>
> In order of where time usually goes for an LLM agent:
>
> 1. **Tool round-trips** (50–80% of wall-clock typically). Sequential loops dominate.
> 2. **TTFT** (model-dependent, load-dependent).
> 3. **Token generation** (output tokens × tokens-per-second).
> 4. **Pre-flight overhead** (auth, embedding lookups, cache reads).
> 5. **Client render**.
>
> Six diagnostic questions:
>
> 1. **p50/p95 target?** If "fast", ask again with numbers.
> 2. **What does the user see while waiting?** Anything streamed today?
> 3. **Which steps are independent** and could run in parallel today?
> 4. **What model tier is each step using, and why?**
> 5. **What is the latency of the slowest tool**, p95?
> 6. **Is latency bimodal?** A fast path + slow path is usually masked by the average.
>
> What I am *not* going to do before that breakdown:
>
> - Swap the model. Premium model on a routing step is wasteful; swapping doesn't fix that.
> - Turn on streaming as a blanket fix. Streaming hides latency; it doesn't reduce it.
> - Add caching without measuring whether the prefix is stable.
>
> Anti-patterns I'm watching for once we have the breakdown:
>
> - **Sequential tool calls** with no data dependency. Default mistake.
> - **One model for everything.** Premium tier on classification.
> - **Reflection in the hot path** with no A/B showing users care.
> - **Long context on every call**. TTFT scales with input length.
>
> **Hard line:** if a step has no latency budget, it has no budget. Total p95 is a result; the targets live on the stages.

---

## The diff

What changed because the skill fired:

- **Refused to recommend fixes** without a per-stage breakdown.
- **Demanded p50 + p95 budgets**, not "faster".
- **Named the typical time-distribution** so the user knows where to look.
- **Listed what the agent refuses to do** before measurement (model swap, blanket streaming, blind caching).
- **Surfaced bimodal latency** as a likely hidden problem.
- **Invoked the hard line** on per-stage budgets.

A naive answer offers fixes. A skilled answer refuses to fix what hasn't been measured.
