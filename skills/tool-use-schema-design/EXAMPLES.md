# Examples — tool-use-schema-design

---

## Example 1 — Kitchen-sink tool

**User prompt:**
> "I have a `do_customer_action(action, payload)` tool — the model picks the action and serialises arguments into payload. Why is it unreliable?"

**Expected behaviour:** Diagnose immediately: the schema teaches the model nothing about what `action` or `payload` should contain. Recommend splitting into per-action tools (`create_customer`, `update_customer_email`, `cancel_customer_subscription`) with typed parameters.

---

## Example 2 — Optional parameters everywhere

**User prompt:**
> "My tool has 8 optional parameters and the model hallucinates values for them."

**Expected behaviour:** Map out which parameters are required for which use cases. Split the tool into 2–3 use-case-specific tools where the required set is unambiguous, or use a discriminated union pattern.

---

## Example 3 — Irreversible action

**User prompt:**
> "The model called `delete_user` on the wrong user. How do I prevent this?"

**Expected behaviour:** Treat the schema as the issue. Recommend splitting into `propose_user_deletion` (returns a token) + `commit_user_deletion(token)`, server-side validation of the token, and a human confirmation gate.
