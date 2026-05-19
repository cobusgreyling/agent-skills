# Examples — model-routing

---

## Example 1 — "We use Opus for everything"

**User prompt:**
> "We're on Claude Opus for everything. Bill's $40k/month and climbing. Should we move to Sonnet to save money?"

**Expected behaviour:** Reject the all-or-nothing framing. Decompose calls by task: classification → Haiku; tool execution → Sonnet; planning / hard reasoning → Opus. Demand the eval before changing tiers — without it, the savings come with silent quality regression. Cheap-first + escalate is usually the right pattern on this profile; expected savings 3×–10× on a workload where most calls are "easy".

---

## Example 2 — "Build a router"

**User prompt:**
> "I want a router that picks Opus vs Sonnet vs Haiku per call. How?"

**Expected behaviour:** Two patterns, depending on signal. (1) **Capability gate** — a small fast classifier (regex or a Haiku call) maps task type → tier. (2) **Cheap-first + escalate** — run Haiku; verify via rule or second-model check; escalate to Sonnet/Opus on fail. The router itself must be cheap and fast (≤ one Haiku call or zero LLM calls). Demand: per-tier eval, calibrated escalation threshold, traces that show route decisions.

---

## Example 3 — "Quality regressed after switching"

**User prompt:**
> "We moved from GPT-4o to GPT-4o-mini for our extraction step. Saved 80% on cost. But our downstream metrics dropped. Roll back?"

**Expected behaviour:** Don't roll back blindly — instrument. Was the regression on *all* inputs or a subset? If subset, the right move is a router: 4o-mini for the easy 80%, 4o for the hard 20%, gated by an extractable feature (input length, document type, confidence). Likely net result: 60–70% of the original savings with no quality regression. Roll back only if the regression is uniform and the router can't distinguish the failing subset.
