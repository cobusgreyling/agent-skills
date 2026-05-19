# Examples — agent-cost-modeling

---

## Example 1 — Price-list reasoning

**User prompt:**
> "Sonnet is $3/1M tokens, Haiku is $0.80. We'll save 75% by switching."

**Expected behaviour:** Reject the calculation. Cost per task depends on tokens × calls × cache hit rate × retry rate, not the list price. The smaller model that fails more often is often more expensive. Demand the cost-per-task equation be filled in with measured numbers.

---

## Example 2 — Cost spike with no breakdown

**User prompt:**
> "Our LLM bill tripled last month and we don't know why."

**Expected behaviour:** Diagnose the missing observability first. Without per-call token counts and per-pattern attribution, the answer is unfixable. Recommend instrumenting cost-per-task per task type as the first step.

---

## Example 3 — Pattern selection on cost

**User prompt:**
> "We're considering Reflexion (critic-actor) to improve quality. What's the cost impact?"

**Expected behaviour:** Apply the pattern-cost rule of thumb — Reflexion typically adds 2–4× per iteration. Ask: how many iterations are capped? Is the critic running every turn or only on uncertain ones? Recommend gating reflection on a confidence signal rather than running unconditionally.
