# Examples — agent-evaluation-harness

---

## Example 1 — Vibe-check shipping

**User prompt:**
> "I tweaked the system prompt and it feels better on my test cases. Can I ship?"

**Expected behaviour:** Block on the question. Ask for the golden set, the regression score, and the per-criterion breakdown. Refuse to call "feels better" a signal. Offer the smallest possible harness (20 inputs, deterministic scorer where possible) if none exists.

---

## Example 2 — LLM-as-judge with no anchors

**User prompt:**
> "I'm using GPT-4 as a judge to rate my agent's responses 1–10. Why are the scores so noisy?"

**Expected behaviour:** Diagnose the missing rubric and anchors. Offer a concrete rubric template: define each score level with 1–2 anchored examples; reduce to a 3- or 5-point scale; never raw "1–10".

---

## Example 3 — Overfitting on one failing case

**User prompt:**
> "This one user query keeps failing. I'll add a few lines to the prompt to handle it."

**Expected behaviour:** Warn that single-case tweaks overfit. Add the failing case to the golden set, then run the *whole* set after the tweak to check for regressions before merging.
