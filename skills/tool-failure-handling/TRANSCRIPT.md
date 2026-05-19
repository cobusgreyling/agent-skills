# Transcript — tool-failure-handling

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We added retries to all our tools. If the tool errors, we retry up to 3 times with exponential backoff. It's working — but we're seeing duplicate orders and our oncall is getting paged. What's wrong?"

---

## Without skill (typical baseline)

> The retry policy might be too aggressive. Try reducing max retries to 2 and increasing the base backoff. Make sure you're only retrying on 5xx errors, not 4xx. Add a check before placing an order to see if a recent order from the same customer already exists. Consider exponential backoff with jitter to avoid thundering herd.

Addresses symptoms. Doesn't reach the design failure: retry on non-idempotent writes.

---

## With skill (behavioural expectation)

> The retries aren't too aggressive — they're the wrong tool for this class of call. You're **auto-retrying non-idempotent writes**. Stop.
>
> Classify each tool before retrying anything:
>
> - **Read-safe.** No side effects. Retry freely.
> - **Idempotent write.** Same call, same effect. Retry safe.
> - **Non-idempotent write.** Each call is a new effect. Retry produces duplicates unless idempotency is enforced.
> - **Irreversible.** Cannot be undone. No auto-retry.
>
> Your `place_order` tool is non-idempotent — and probably irreversible — and you're retrying it three times. The duplicates aren't a bug in the retry library; they're the retry library doing its job on a tool that wasn't designed for it.
>
> Concrete fix, ordered:
>
> 1. **Idempotency key, end to end.** The agent generates (or your wrapper generates) `idempotency_key` per logical action. The downstream order service dedupes by key — same key, same result, no second order. This is the cleanest "exactly-once" you'll get. Most order systems either support it natively or expose it cheaply.
>
> 2. **Reconcile, don't retry, on timeout.** On a timeout, the call's outcome is *unknown* — not failed. Before retrying, *read* the order system by idempotency key. If the order exists → success, surface that to the agent. If not → safe to retry. Blind retry is the path to duplicates.
>
> 3. **Typed errors, not exceptions.** The tool returns `{status: "rate_limited", retry_after_ms: 1200}` or `{status: "invalid_argument", field: "amount"}` — never a stringified traceback. The agent can recover from typed errors; it can't from prose.
>
> 4. **Differentiate transient vs permanent.** Retry on 429, 503, timeouts. Don't retry on 400, 401, 422. The current "retry up to 3 times on any error" wastes budget on permanent failures and produces duplicates on transient ones.
>
> 5. **Per-call timeout, per-task retry budget.** Wall-clock cap per call (e.g. 5s); max retries per call (e.g. 2); max retries per task (e.g. 10). Both enforced. No "default to infinite".
>
> 6. **Circuit breaker on the tool.** N failures in a window → break for T seconds. Agent receives `tool_unavailable` and adapts (fallback, escalate, surface).
>
> 7. **Compensation, not silent rollback.** If you have a multi-step flow (reserve inventory → charge → confirm), each step has a typed compensation. Partial failure runs compensations in reverse, explicitly. Not `try/except: pass`.
>
> Anti-patterns I'm watching for in your stack:
>
> - **Blind retry on timeout.** Your immediate issue.
> - **Retry on 4xx.** Wastes budget; never fixes itself.
> - **Stringified errors to the agent.** Unreadable; model can't recover.
> - **No timeout.** Agent hangs forever on one slow tool.
> - **No retry budget.** Per-task max matters as much as per-call.
> - **Silent fallback** (empty results on error). Hides failure; downstream proceeds wrong.
>
> Seven questions:
>
> 1. What's the **classification** of each tool — read-safe, idempotent, non-idempotent, irreversible?
> 2. Does every non-read write have an **idempotency key**?
> 3. What's the **timeout** per call and per task?
> 4. What's the **retry budget** per call and per task?
> 5. How does the agent **distinguish transient vs permanent** errors?
> 6. What's the **compensation** strategy for multi-step writes?
> 7. Are failures **typed**, **traced**, and **fed back** into the eval?
>
> Realistic outcome on your workload: duplicates stop within a day of shipping the idempotency key + reconcile pattern. The oncall pages drop because the failure mode you were paging on was a self-inflicted retry storm.
>
> **Hard line:** never auto-retry a non-idempotent write. Reconcile, not retry. Duplicates are debugged at customer-support cost; the prevention is one server-side dedupe.

---

## The diff

What changed because the skill fired:

- **Classified the tool** (non-idempotent / irreversible) before recommending any retry change.
- **Replaced blind retry with reconcile-then-retry** keyed on idempotency.
- **Required typed errors** so the agent can recover deterministically.
- **Separated transient vs permanent** retry behaviour.
- **Imposed timeouts, retry budgets, circuit breaker** as standard scaffolding.
- **Treated compensation as an explicit typed step**, not a silent rollback.
- **Connected the incident** (oncall pages, duplicate orders) to the design failure (retry policy on non-idempotent write).

A naive answer tunes the retry knobs. A skilled answer classifies the tool, replaces retry with reconcile, types the errors, and turns failure handling into deterministic recovery.
