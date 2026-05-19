# Examples — structured-output-reliability

---

## Example 1 — The repair function

**User prompt:**
> "We ask GPT for JSON and the model returns trailing commas, single quotes, sometimes a markdown code fence. We wrote a 300-line repair function. It mostly works."

**Expected behaviour:** Diagnose: wrong mechanism. The 300-line repair function is doing the schema-enforcement layer's job, badly. Switch to OpenAI's structured outputs (or function calling if the output represents an action). Drop the repair function. Validate strictly with a schema library; reject loudly on the rare failure; retry once with the parser error as feedback. Expected failure rate drops by 1–2 orders of magnitude.

---

## Example 2 — Enum vs string

**User prompt:**
> "We have a `category` field. Description says 'must be one of: billing, technical, account, other'. The model sometimes returns 'tech' or 'general'."

**Expected behaviour:** Promote to enum. `category: Literal['billing', 'technical', 'account', 'other']` in the schema, enforced at the provider level (structured outputs / function calling). String-with-constraint-in-description leaks. The model follows types; descriptions are a softer signal.

---

## Example 3 — Deeply nested schema

**User prompt:**
> "Our extraction schema has 6 levels of nesting and the model breaks it more often than not. The schema mirrors our DB model exactly."

**Expected behaviour:** Schema follows the model's output capability, not your DB. Flatten to ≤3 levels for the extraction step; transform to your DB shape in code afterward. If the schema is genuinely irreducible, split into multiple calls (extract chunk-by-chunk, assemble in code) or escalate to a stronger model. Don't fight nested-schema failure mode at the prompt layer.
