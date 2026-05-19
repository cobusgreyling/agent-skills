# Examples — tool-failure-handling

---

## Example 1 — Duplicate payments

**User prompt:**
> "Our agent calls `charge_card(amount, customer_id)`. Sometimes the tool times out and we retry. Some customers are being charged twice. How do we fix?"

**Expected behaviour:** Classify: this is a **non-idempotent write** on an **irreversible** action. Auto-retry is wrong. Fix: server-side idempotency key (agent provides `idempotency_key`; the payment processor dedupes by key — most PSPs already support this, e.g. Stripe). On timeout, the agent must *reconcile* (read state by idempotency key) before retry. Better still: propose/commit split where `commit_charge(token)` is naturally idempotent on the token. Never blind-retry a charge.

---

## Example 2 — Agent hangs on flaky tool

**User prompt:**
> "One of our tools occasionally hangs for 60+ seconds. The agent waits, blocks the whole run, sometimes times out the user request."

**Expected behaviour:** Two missing things: (1) per-call timeout (e.g. 5s wall-clock), enforced at the wrapper; (2) typed error back to the agent on timeout (`{status: "timeout", elapsed_ms: 5000}`) so the model can adapt — try again, try a fallback tool, or surface to the user. Optionally add a circuit breaker so repeated timeouts pause that tool for the rest of the session.

---

## Example 3 — Multi-step partial failure

**User prompt:**
> "Our agent does (1) reserve inventory, (2) charge card, (3) send confirmation email. Step 3 failed for a customer. They were charged but never notified. What's the right pattern?"

**Expected behaviour:** Saga / compensation. Each step has a defined compensation: step 3 compensation = retry email with backoff, then enqueue for manual follow-up; step 2 compensation = refund; step 1 compensation = release inventory. On step 3 fail, *do not* compensate steps 1–2 silently — the order has shipped. The compensation for "delivery failed" is retry-then-manual, not refund. Treat compensation as an explicit, typed step, never `try/except: pass`.
