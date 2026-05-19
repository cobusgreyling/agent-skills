# Transcript — agent-observability

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "Our agent is randomly failing in production. We log the final model response and the user input. What else should we add?"

---

## Without skill (typical baseline)

> Good question — adding more logging will help. Some things you might want to capture:
>
> - Tool call inputs and outputs
> - Latency per step
> - Error messages
> - Maybe the system prompt version
>
> You could also consider using a tracing library like LangSmith, Langfuse, or OpenTelemetry. They give you nice dashboards and let you replay traces. Try one and see if it fits your workflow.

A laundry list. No structure, no priorities, no replay contract.

---

## With skill (behavioural expectation)

> Logging the final response and user input is not observability — it's a story missing the middle. You can't replay it, can't diagnose it, can't feed it into an eval. Three things have to be true before "we have observability" is a real claim:
>
> 1. **One trace per user request.** Sub-agents, retries, tool calls are nested **spans** inside it. Not separate log lines you have to join by timestamp.
>
> 2. **Inputs and outputs verbatim, on every span.** Truncated logs hide bugs. If size is a concern, use a long-content store; never trim by default.
>
> 3. **Standardised span names + attributes.** Use the OpenTelemetry GenAI conventions if your stack supports them — `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, etc. Future-proofs vendor swaps.
>
> Six questions:
>
> 1. What's the **first thing you look at** when an agent fails today? If it's logs, what's in them?
> 2. Can you **replay a single failed request** without modifying code? (If no, that's task one.)
> 3. Are **tool calls** traced with the same fidelity as model calls?
> 4. Is there **cost-per-request** attribution, or only monthly totals?
> 5. When a new model version ships, can you **diff behaviour on real traffic**?
> 6. Who owns the **dashboard**, and what's on it?
>
> Anti-patterns I'm watching for in your current setup:
>
> - **Print-debugging only** — works in dev, useless under prod concurrency.
> - **No input capture** — "the model said this" without "given what input" is a story, not a trace.
> - **One span per agent run** — collapses loops into an opaque blob.
> - **Sampling errors out** — always trace 100% of errors; sample successes.
>
> **Hard line:** every production call gets a trace. Otherwise you're guessing.

---

## The diff

What changed because the skill fired:

- **Reframed "logging" as "trace + spans"** — a structural claim, not a checklist.
- **Listed three load-bearing properties** (one-trace, verbatim, standardised) before suggesting tools.
- **Asked diagnostic questions** about the user's actual debugging workflow.
- **Named four anti-patterns** to watch for in their current setup.
- **Pushed OpenTelemetry GenAI conventions** instead of vendor lock-in.
- **Invoked the hard line** on full-error trace coverage.

A naive answer adds log lines. A skilled answer demands replay, eval-ready shape, and one trace per request.
