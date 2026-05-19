# Transcript — llm-as-judge

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We tuned our summarisation prompt. New version scored 4.5/5 on our LLM-judge eval; old version scored 4.1/5. Judge is GPT-4o, same model that generates the summaries. 100 prompts, single-pass each. We're going to ship the new prompt. Reasonable?"

---

## Without skill (typical baseline)

> A 0.4 improvement on a 5-point scale with N=100 is a meaningful gain. Ship it. Optionally re-run once to confirm the result is stable, but the delta looks real.

Treats the score as a measurement. Doesn't audit the measurement system.

---

## With skill (behavioural expectation)

> Don't ship yet. The number isn't the question; the measurement system is. Audit the judge before trusting it.
>
> Six issues with this design, ordered by severity:
>
> 1. **Same model as candidate and judge.** Self-preference is real and well-documented — GPT-4o systematically prefers GPT-4o output, especially when the candidate output uses similar style/length. The delta you're seeing might be entirely "the new prompt produces output that's more GPT-4o-ish". Use a different family as judge — Claude or Gemini — and re-run. If the delta survives, it's signal. If it collapses, your real improvement is near zero.
>
> 2. **Pointwise on a 5-scale, single-pass.** Pointwise scoring is noisy without anchors. "4.1 vs 4.5" assumes the scale is calibrated; without anchored examples per score level, the model is improvising. Switch to **pairwise** ("is A or B a better summary, or tie") — most signal, most stable.
>
> 3. **Position bias not measured.** If you're pairwise, you must randomise A/B order per call. If you're pointwise scoring two prompts separately, the prompt ordering in your study could be doing work you're attributing to the prompt change.
>
> 4. **Length bias not normalised.** Longer answers score higher on most judges. Is your new prompt producing longer summaries? If yes, control for length (truncate to same length, or normalise score by length percentile).
>
> 5. **No judge-human agreement number.** You don't know if your judge is measuring quality at all. Label 50 examples by hand; compute % agreement or kappa. Below 0.6 the judge is noise; below 0.8 use with explicit uncertainty.
>
> 6. **No confidence interval.** N=100 with a noisy classifier — the 95% CI on a 0.4 delta is probably ±0.3 or more. The delta might not be distinguishable from zero.
>
> What I'd want before shipping:
>
> - **Different-family judge** (Claude as judge of GPT candidates).
> - **Pairwise comparison** with **randomised position** and **ties allowed**.
> - **Anchored examples per score level** if pointwise is non-negotiable.
> - **Length normalisation** or per-length-bucket reporting.
> - **N≥3 judge runs per example**, report median + IQR.
> - **Meta-eval:** 50 hand-labelled examples; judge-human agreement reported alongside any judge-driven decision.
> - **Bias probes:** re-run with positions swapped, output reformatted, length controlled — see how much the score moves.
>
> Anti-patterns I'm watching for in your eval pipeline:
>
> - **Same-model self-judging.** (Your current state.)
> - **No randomised position** in pairwise.
> - **Unanchored rubric.**
> - **"Overall" score** — decompose into named dimensions (faithfulness, completeness, concision) and score each separately.
> - **Free-text justification trusted as scoring signal.** Justifications are post-hoc; the score is the score.
> - **Judge sees the candidate's prompt or system instructions.** Leaks criteria into judging.
>
> Eight questions:
>
> 1. Could this be **deterministic** (ROUGE, faithfulness extraction)?
> 2. Is the judge a **different family** from the candidate?
> 3. **Pairwise or pointwise** — and why?
> 4. Is position **randomised**? Ties **allowed**?
> 5. Are there **anchored examples** per score level?
> 6. What's the **judge-human agreement** on your task?
> 7. What's the **bias probe** result?
> 8. Are you reporting **confidence intervals**?
>
> Likely outcome on your workload: after switching to a different-family judge and pairwise comparison, your real delta lands somewhere between "negligible" and "real but smaller". Either way, you'll know — which beats shipping a regression with a 4.5/5 sticker on it.
>
> **Hard line:** a judge that hasn't been meta-evaluated isn't a scorer; it's a vibes amplifier. Validate against humans on ≥50 examples before any production decision rests on its scores.

---

## The diff

What changed because the skill fired:

- **Refused to ship on the score alone.** Audited the measurement system.
- **Named six bias / calibration failures**, ordered by severity.
- **Replaced same-family judging with cross-family judging.**
- **Switched pointwise to pairwise** as the higher-signal protocol.
- **Required position randomisation, anchored rubric, length normalisation.**
- **Demanded meta-eval** (judge-human agreement) before any decision.
- **Required confidence intervals** on the reported delta.

A naive answer reads the score and ships. A skilled answer audits the judge first and treats the score as evidence only after the measurement system passes its own eval.
