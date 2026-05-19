# Rubric Anchors — anchored examples per check

For each check, one **pass**, one **partial**, one **fail** example. The scorer compares the response under test to these anchors before assigning a score. Anchors are written terse — match the shape, not the literal words.

## `flags-missing-cost-ceiling`

**Pass:**
> "Stop. Before any recommendation: what is the cost ceiling per task in dollars? Without that number, model choice and pattern choice are vibes. 'Keep costs under control' is a wish, not a ceiling. Push back on leadership for the figure; the architecture decision depends on it."

**Partial:**
> "It would be helpful to know your target cost per task. Here are some general approaches anyway..."

**Fail:**
> "To keep costs down, consider switching to a smaller model or reducing the number of tool calls per task."

---

## `flags-call-graph-missing`

**Pass:**
> "List prices won't tell you the answer. Sketch the call graph per task first: how many model calls, which tier, what's the prompt size at p50/p95, what tools are called, how many retries. Only with that can you price the workload. Comparing $/1M tokens is the wrong unit — the unit is cost-per-task."

**Partial:**
> "We'd need to know how many calls per task and how large each prompt is to give a real estimate. Roughly, model X costs Y."

**Fail:**
> "Sonnet is roughly $3/1M input tokens vs Opus at $15/1M. Five-fold savings if you switch."

---

## `flags-cache-savings-ignored`

**Pass:**
> "Caching is the first lever — before model swaps, before architecture, before pruning tools. What's your cache hit rate today, measured from `cache_read_input_tokens / total_input_tokens`? If it's <50% on a workload with a stable prefix, the issue is cache-key poisoning (timestamp, request id, mutating system prompt, reordered tools). Fix that first; you may not need any other change."

**Partial:**
> "Caching can help reduce cost. Make sure your prompts are cache-friendly."

**Fail:**
> "Switching to a cheaper model would cut your bill substantially. Consider Sonnet or Haiku."

---

## `flags-wrong-tier`

**Pass:**
> "Tier is per-step, not per-agent. Classification → Haiku. Planning → Opus or Sonnet, decided by eval. Tool execution → small. Summarisation → mid. Running the whole agent on Opus pays Opus prices on calls that don't need it. Cheapest model that passes the eval per step wins."

**Partial:**
> "You could use Sonnet instead of Opus for some steps to save money."

**Fail:**
> "If reliability is the priority, stick with Opus across the board. The reliability premium is worth the cost."

---

## `flags-unbounded-loop-cost`

**Pass:**
> "Step cap is not a cost cap. Add a per-task token (or dollar) budget check *inside* the loop — at the top of each iteration, sum tokens-so-far and break if you've exceeded budget. Controllers enforce; prompts advise. 'Be efficient' is not a defence."

**Partial:**
> "Lower the max_steps to something like 20. That should help bound the cost."

**Fail:**
> "Add a system prompt instruction telling the agent to be efficient and stop early when possible."

---

## `flags-non-model-costs`

**Pass:**
> "Model tokens are one line. Add: embeddings on every RAG indexed-doc and every query; vector-store read costs; tool execution (your APIs, infra); observability storage and retention; human-in-the-loop minutes if you have a HITL queue. Self-hosted moves variable cost to fixed (GPU lease, oncall) — break-even depends on volume."

**Partial:**
> "Don't forget about embedding costs too — those can add up."

**Fail:**
> "The main cost is the model itself. Optimising tokens-per-call is where the leverage is."

---

## `flags-cost-per-failed-task`

**Pass:**
> "$0.12 per call ≠ cost per task when 30% fail. Real cost-per-successful-task ≈ $0.12 / 0.7 + retry overhead ≈ $0.20+. The denominator is successful tasks; retries and abandoned runs ride in the numerator. The retry rate is a cost lever, not just a quality one."

**Partial:**
> "Account for retries in your cost calculation."

**Fail:**
> "$0.12/task is reasonable. If you want to drive it lower, look at prompt size."
