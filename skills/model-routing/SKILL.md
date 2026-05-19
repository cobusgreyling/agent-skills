---
name: model-routing
description: >-
  Pick the right model per call, not per project — route Opus/Sonnet/Haiku,
  GPT-5/4o/mini, Gemini Pro/Flash by task, and cut cost without losing
  quality. Use when the user is choosing model tiers, building a router,
  or debating Opus-only vs mixed-tier deployments and mentions model
  selection, model router, cascade, fallback, cheap-first, draft-then-verify,
  or asks "which model should I use?" / "do I need Opus for this?".
tags:
  - cost
  - latency
  - architecture
  - model-selection
---

# Model Routing

Pick the model per call, not per project.

A single-tier deployment is either overpaying for easy turns or underdelivering on hard ones. The lever is matching model capability to *the specific decision* the call is making — and only escalating when the cheaper model demonstrably fails.

## When to use this skill

- The user is choosing a model for a new agent.
- The user is on the most expensive tier for everything and the bill is climbing.
- The user is on the cheapest tier and quality is borderline.
- The user is building or evaluating a router / cascade / draft-then-verify pipeline.
- The user mentions Opus, Sonnet, Haiku, GPT-5, GPT-4o-mini, Gemini Pro/Flash, model fallback, or hybrid inference.

## Decision flow

1. **Is the task single-shot, easily-verified, and bounded?** → cheapest tier. Don't romanticise quality where it doesn't move the needle.
2. **Is the task agentic (multi-step tool use, planning)?** → the *planner* needs the strongest model; the *executor* can be smaller.
3. **Is the task latency-critical (TTFT-sensitive UX)?** → cheapest fast model that clears the quality bar. Cascade if quality wobbles.
4. **Is the task safety-critical (real-world side-effects, irreversible actions)?** → strongest model on the *decision*, with a verification pass.
5. **Is the task variance-sensitive (you need consistent output)?** → strongest model + `temperature=0` + structured output schema. Don't try to fix variance with a router.
6. **Do you have an eval that shows which tier passes?** → no? Build one before routing. Routing without measurement is folklore.

## Routing patterns that work

- **Cheap-first + escalate.** Run the cheap model; verify (rule, regex, classifier, second model); escalate on fail. Saves cost when the cheap model is right most of the time.
- **Draft → verify.** Cheap model drafts; strong model checks. Only escalate the *output*, not the input.
- **Capability gate.** Classifier picks model from task type: extraction → cheap; reasoning → strong; tool-use → strong-with-tools.
- **Cascade with confidence.** Cheap model returns a confidence score; route to strong below threshold. Calibrate the threshold against your eval.
- **Mixed-tier agent.** Planner = strong; tool-executor = small; summariser = small. Single conversation, multiple tiers.

## Anti-patterns to flag immediately

- **Opus / GPT-5 / Pro everywhere.** Defaulting to the most expensive tier is laziness with a budget impact.
- **Haiku / mini everywhere.** Defaulting to the cheapest tier is laziness with a quality impact.
- **Routing by "which model is cool right now".** The eval picks the model. Trends don't.
- **No eval before routing.** You will route based on vibes; vibes regress quietly.
- **Hard-coded model names in business code.** Wrap behind a `route(task) -> model` boundary. Models change quarterly.
- **Cascade without confidence signal.** "Re-run on the bigger model if the answer looks bad" is a vibe, not a router.
- **Same temperature, same top-p across tiers.** Tier swap is a behaviour change; re-tune sampling.
- **Routing across providers without normalising tool-use semantics.** Anthropic's tools and OpenAI's tools don't behave identically.

## The cost lever

Order of magnitude per million tokens (illustrative — get current numbers; they move):

- Frontier (Opus / GPT-5 / Pro): ~10×–20× cheapest.
- Mid (Sonnet / GPT-4o / Pro): ~3×–6× cheapest.
- Small (Haiku / mini / Flash): baseline.

A 30/70 strong/cheap mix on a workload that's 90% easy can cut spend 5× with no measurable quality loss — if you measured.

## Questions to ask the user

1. What is each **call doing** — extraction, classification, reasoning, tool-use, summarisation?
2. What's the **acceptance criterion** per call — exact match, semantic match, structural validity, human grade?
3. What's the **failure cost** — wrong answer free, expensive, or unrecoverable?
4. Is there an **eval** that distinguishes tier quality on your workload? If not, build it before routing.
5. What's the **latency budget** per call — TTFT and total?
6. Does the router itself need to be cheap and fast? Yes — make it a classifier, not an LLM call.

## The hard line

**No routing decision without an eval. No tier choice without a per-call cost target.** Folklore is expensive in both directions.

## Why this exists

Every agent deployment ends up paying for too-strong or too-weak. The discipline of asking "which decision is this call making, and what's the cheapest model that passes the eval for that decision?" cuts cost 3×–10× on real workloads without quality loss. The router is the architecture decision most teams skip; it's the highest-ROI one.

## References

- `references/per-task-tiering.md` — extraction / classification / reasoning / tool-use / summarisation — recommended tier per task type, with caveats.
- `references/cascade-patterns.md` — cheap-first + verify, draft → verify, confidence-based routing — code sketches.
- `references/cross-provider.md` — switching between Anthropic, OpenAI, Google, Bedrock — what stays the same, what doesn't.

## Related skills

- Routing is a [[agent-cost-modeling]] decision; model the unit economics before wiring it.
- Routing shapes [[latency-budgeting]] — small models hit TTFT targets cheap models don't.
- Routing decisions need [[agent-evaluation-harness]] coverage per tier.
- Cache hit rates differ by model — [[prompt-caching]].
- Wrap the router as a tool, not an inline call — [[tool-use-schema-design]].
- Multi-tier agents are an [[agent-architecture-patterns]] choice.
