# Examples — llm-as-judge

---

## Example 1 — "Our model scored higher"

**User prompt:**
> "We compared v2 vs v1 of our agent. Used GPT-4 as the judge. v2 scored 4.6/5, v1 scored 4.2/5. Ship v2?"

**Expected behaviour:** Not yet. Six missing pieces: (1) judge model same family as candidate? (self-preference risk); (2) pairwise or pointwise? (pointwise on a 5-scale without anchors is noisy); (3) position randomised? (position bias mimics quality); (4) was length normalised, or is v2 just longer? (length bias); (5) what's judge-human agreement on this task? (without it, the score is a vibes amplifier); (6) confidence interval on the 0.4 delta? With N=50 noisy judgments, 0.4 is well inside the noise floor.

---

## Example 2 — "Why is the judge inconsistent?"

**User prompt:**
> "Same task, same outputs, the judge gives different scores on re-run. Sometimes 3, sometimes 4. Help?"

**Expected behaviour:** Expected, and a sign the design needs tightening: (1) drop to pairwise (more stable than absolute scores); (2) add anchored examples per score level so the judge anchors instead of guessing; (3) run with `temperature=0`; (4) average N≥3 runs and report median; (5) if pointwise is required, score one dimension per call rather than "overall". The score is a measurement; it has variance — design around the variance.

---

## Example 3 — Code review judge

**User prompt:**
> "We're using an LLM to judge code reviews — does the suggested fix solve the bug? Judge is GPT-4, candidate is GPT-4. Scores look fine; humans disagree with the judge ~30% of the time on a sample."

**Expected behaviour:** 70% agreement (≈ kappa < 0.5 on a binary task) is below trust threshold. Three changes: (1) different judge family (Claude or Gemini as judge against GPT candidate); (2) pairwise where possible — "is fix A or fix B better?" stabilises faster than absolute; (3) before any production decision, raise judge-human agreement above 0.8 on 50+ labelled examples or report uncertainty bounds on every downstream metric. Until then, treat judge scores as suggestive, not authoritative.
