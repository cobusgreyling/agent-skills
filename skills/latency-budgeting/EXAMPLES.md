# Examples — latency-budgeting

---

## Example 1 — Sequential tool loop

**User prompt:**
> "My agent calls four APIs sequentially and the whole thing takes 9 seconds. Can I speed it up?"

**Expected behaviour:** Ask which of the four calls have data dependencies on each other. If two or more are independent, parallelise. Measure the new p95 before chasing further optimisations.

---

## Example 2 — No latency target

**User prompt:**
> "My agent is slow. How do I make it faster?"

**Expected behaviour:** Refuse to optimise without a target. Ask for p50 and p95 budgets in milliseconds. Then trace the existing pipeline to identify which stage dominates.

---

## Example 3 — One model for everything

**User prompt:**
> "I'm using the biggest model for every step — routing, retrieval, synthesis, formatting. Quality is great but it's slow and expensive."

**Expected behaviour:** Identify which step actually needs the big model (typically synthesis or reasoning). Recommend a small/fast tier for routing, classification, and formatting; keep the big model only on the step that needs it.
