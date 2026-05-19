# Transcript — structured-output-reliability

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We ask Claude to extract structured info from invoices. Prompt says 'return JSON with these fields'. About 8% of the time the JSON is malformed — trailing commas, missing quotes, sometimes wrapped in ```json fences. We wrote a regex repair function. It works most of the time, but bugs slip through. What should we do?"

---

## Without skill (typical baseline)

> Improve the prompt: be more explicit that the output must be pure JSON, no fences, no commentary. Add an example of valid output. Strengthen the repair function — there are libraries like `json5` or `dirtyjson` that handle common LLM quirks. Consider setting a stop sequence to prevent trailing commentary. You could also retry on parse failure.

Goes along with the repair-function premise. Doesn't reach for the right mechanism.

---

## With skill (behavioural expectation)

> Delete the regex repair function. The 8% failure rate is the model telling you you're using the wrong mechanism.
>
> Pick the right mechanism first. Your output is **data** (extraction), not an action. The right tool is **Anthropic's tool use** (declare a tool whose `input_schema` matches your extraction shape; the model emits a tool call with schema-validated arguments) or, equivalently in other providers, **structured outputs** / **controlled generation**. The provider enforces the schema; you parse the structured argument, not the text.
>
> Five concrete changes:
>
> 1. **Use tool-use, not text-with-JSON.** Define `extract_invoice` as a tool with a JSON-schema'd `input_schema`. Force the model to call it (`tool_choice: {"type": "tool", "name": "extract_invoice"}`). The model's output is now a structured argument, not a string containing JSON.
>
> 2. **Schema is part of the prompt — make it tight.**
>    - **Enums for closed sets.** `currency: ["USD", "EUR", "GBP", ...]` not `currency: string`.
>    - **Format constraints in the schema.** `invoice_date: {type: "string", format: "date"}` not "in YYYY-MM-DD format" in description.
>    - **Required vs optional explicit.** Don't lean on "usually filled in".
>
> 3. **One concrete example in the prompt.** A single worked example halves error rate. Put it before the task.
>
> 4. **Flatten the schema if it's nested.** Failure rate climbs with depth. If you're at >3 levels, restructure or split into multiple calls.
>
> 5. **Validate strictly, reject loudly, retry once.** Pydantic / zod / JSON-schema strict. No silent repair. On failure, retry *once* with the parser error in the message: "Your previous output failed validation: `<error>`. Return only the corrected structure." If retry fails, surface to logs and (depending on stakes) a human.
>
> Anti-patterns I'm watching for elsewhere in your pipeline:
>
> - **Regex-repairing output** (your current state).
> - **`response.content` parsed with `json.loads()`** and no validation. You'll find the failure downstream.
> - **Free-text fields where enums belong.** Strings with "must be one of X" in the description leak.
> - **Mixed free-text + structured output** in one response. Tool-use cleanly separates the action from any explanation.
> - **Provider native schema mode unused.** "We're already parsing JSON" is not a reason to skip enforcement.
> - **No measurement.** What is your validation-pass rate on a held-out set?
>
> Seven questions:
>
> 1. Is the output an **action** or **data**?
> 2. Are you using the **provider's native schema mechanism**?
> 3. Where do enums live — as types or as descriptions?
> 4. Is the schema **flat enough** to reach in <100 tokens?
> 5. What does validation failure **do** — repair, retry, reject, alert?
> 6. Is there an **exemplar in the prompt**?
> 7. What's the **failure rate** on a held-out set? If unknown, build the eval first.
>
> Expected outcome on your workload: 8% malformed → <0.5% with tool-use + strict validation + one-shot retry. The remaining 0.5% becomes a tracked failure mode, not a silent corruption.
>
> **Hard line:** validate strictly, reject loudly, never repair silently. If the schema isn't worth enforcing, it isn't a schema — it's a hint.

---

## The diff

What changed because the skill fired:

- **Refused the repair-function premise.** Named the wrong-mechanism root cause.
- **Switched to tool-use / structured outputs** as the primary fix.
- **Tightened the schema** with enums, format constraints, required/optional explicit.
- **Required one concrete example in the prompt.**
- **Imposed strict validation, loud rejection, one-shot retry with parser feedback.**
- **Surfaced measurement gap** — failure rate on a held-out set must exist.
- **Listed adjacent anti-patterns** likely present elsewhere in the pipeline.

A naive answer iterates the repair function. A skilled answer deletes it, switches mechanism, and turns the failure mode into a tracked event instead of a silent corruption.
