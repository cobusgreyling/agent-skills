# Transcript — agent-evaluation-harness

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "I tweaked the system prompt and the agent feels better. Should I ship it?"

---

## Without skill (typical baseline)

> If it works in your testing, sure — go ahead and ship. You can always roll back if you see issues in production. Good practice would be to monitor closely for the first few days. Some things you might do:
>
> - Add some example inputs to a test file
> - Compare a few responses before/after
> - Check that the same edge cases still work
>
> But if your manual testing looks better, "feels better" is often a real signal.

Permissive. Treats a vibe check as signal.

---

## With skill (behavioural expectation)

> No. "Feels better" is not a signal — it's a memory of two responses you happened to read.
>
> The pattern that produces this question is the pattern that produces silent regressions in production. Before this change ships, I need three things:
>
> 1. **A frozen input set** — ≥20 representative prompts covering the long tail of your real traffic, not the average. Curated, not sampled.
> 2. **A scoring function** — deterministic if possible (regex, JSON-schema, tool-call match). LLM-as-judge only with a rubric + 3–5 anchored examples per score level. Never "rate 1–10" freeform.
> 3. **A regression gate** — score the new prompt vs the last known-good score. If it's down on any task, the merge blocks until you understand why.
>
> Two specific questions:
>
> - **Multi-step agent?** Then score the trace, not just the final answer. A right answer via a wrong tool sequence is a future regression.
> - **Tweaked against a specific failing input?** Don't ship a fix to one input — add it to the set, run the *whole* set. Single-example tweaks always overfit.
>
> What I am refusing to do:
>
> - Tell you "it looks better in spot-checks". I don't trust spot-checks.
> - Use the same model to judge its own output. That's a co-conspirator, not an auditor.
> - Let an LLM-as-judge run without rubric anchors. A judge that has never seen what a "5" looks like is a random number generator.
>
> **Hard line:** no golden set, no merge. No exceptions for "small" prompt changes — small changes are exactly where regressions hide.

---

## The diff

What changed because the skill fired:

- **Refused to greenlight a vibe-check ship.** Named the failure mode this question hides.
- **Demanded the three pieces** (frozen set, scorer, regression gate) before approval.
- **Asked about the agent's structure** (multi-step → score trace, not answer).
- **Flagged the single-example trap** (the source of the original "tweak").
- **Listed what the agent refuses to do** — vibe checks, self-judging, unanchored LLM-as-judge.
- **Invoked the hard line** on "no golden set, no merge".

A naive answer ships. A skilled answer blocks until the measurement exists.
