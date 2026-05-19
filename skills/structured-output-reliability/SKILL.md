---
name: structured-output-reliability
description: >-
  Get reliable structured output (JSON, typed objects) out of an LLM without
  regex repair, retry loops, or silent corruption. Use when the user is
  parsing model output, fighting malformed JSON, comparing JSON mode vs
  function calling vs structured outputs, or asks "why does the model keep
  breaking my schema?" / "how do I force valid JSON?".
tags:
  - structured-output
  - reliability
  - tool-use
  - production
---

# Structured Output Reliability

If you're repairing model output with regex, your schema is the problem.

The model will produce malformed structured output. The question is whether your system fails closed (loud rejection) or open (silent corruption). The default of "parse and hope" produces the second.

## When to use this skill

- The user is parsing JSON or typed objects out of a model and reports breakage.
- The user is regex-fixing model output (trailing commas, smart quotes, unescaped newlines).
- The user is comparing "JSON mode" / "structured outputs" / "function calling" / "tool use" for the same job.
- The user is building a pipeline where structured output feeds a downstream system.

## The three mechanisms — pick by job

- **Function calling / tool use.** The model emits a structured argument to a tool. *The provider enforces the schema.* Strongest guarantees. Use when the structured output represents an *action*.
- **Structured outputs / JSON schema mode.** The provider constrains generation to your schema. Use when the structured output represents *data* — extraction, transformation, classification.
- **Free-form JSON in text.** Model emits JSON-like text inside a string response. Weakest guarantees. Use only when the above aren't available.

Picking the wrong mechanism is the most common root cause of "the model breaks my schema".

## Decision flow

1. **Is this output an action or data?** → action → tool use / function calling. Data → structured outputs / JSON schema mode.
2. **Does the provider enforce schemas natively?** → yes → use it. (Anthropic tool use, OpenAI structured outputs, Gemini controlled generation.) Don't roll your own.
3. **Is the schema reachable in <100 tokens of output?** → yes → simpler schemas pass; nested schemas degrade fast. Flatten where possible.
4. **Is the schema closed (enums, fixed shape) or open (free-text fields)?** → closed wins. Use enums, not strings-with-constraints.
5. **Does the downstream system tolerate partial output?** → no → validate strictly, reject loudly; do not "fix" output silently.

## The five rules

1. **Schema is part of the prompt.** It's not a post-hoc validator; it's a behaviour driver. Place it before the task, with one concrete example.
2. **One concrete example beats five sentences of description.** Always include an exemplar.
3. **Enums for closed sets.** `priority: "high"|"medium"|"low"` not `priority: string`.
4. **Reject loudly on schema-violation.** Pydantic / zod / JSON-schema strict validation. No repair. No `try/except: pass`. Failure goes to retry or human.
5. **Retries with feedback.** On schema violation, retry *once* with the parser error as a corrective message. Never silently swallow.

## Anti-patterns to flag immediately

- **Regex-repairing model output.** Trailing commas, smart quotes, missing close-brackets — every "fix" hides a class of bugs. The schema enforcement layer is doing the model's job *and* doing it wrong.
- **`response.choices[0].message.content` parsed as JSON with no validation.** You'll discover the failure when downstream breaks.
- **Free-text fields where enums belong.** Strings with "must be one of X, Y, Z" in the description leak.
- **Deeply nested schemas (>3 levels).** Flatten or split into multiple calls.
- **Description-only constraints** ("the date must be in YYYY-MM-DD format"). Constrain via type / regex / format in the schema.
- **No exemplar in the prompt.** One worked example halves error rate.
- **Provider's native schema mode unused** because "we're already parsing JSON". Switch immediately.
- **Mixing free text and structured fields in one response.** Either return JSON-only, or use tool-use to separate the action from the explanation.

## Questions to ask the user

1. Is this output an **action** or **data**?
2. Does your **provider** support native schema enforcement? Are you using it?
3. What does **validation failure** do — repair, retry, reject, alert, human?
4. How is your **schema reaching the model** — system prompt, function definition, both?
5. Do you have **one concrete example** of valid output in the prompt?
6. Are enums actually **enums**, or strings with constraint descriptions?
7. What's the **failure rate** on a held-out set? If you don't know, you don't have a structured-output pipeline; you have hope.

## The hard line

**Validate strictly. Reject loudly. Never repair silently.** If the schema isn't worth enforcing, it isn't a schema — it's a hint.

## Why this exists

Every team building structured-output pipelines starts by writing a JSON repair function. Six months later it's 200 lines of regex masking the failure modes that proper schema enforcement would have surfaced and fixed. The native schema mechanisms — function calling, structured outputs, controlled generation — exist; using them is the right answer, and most teams skip past them in a hurry.

## References

- `references/mechanism-comparison.md` — function calling vs structured outputs vs tool use, per provider, with capability deltas.
- `references/schema-design.md` — flat vs nested, enums vs strings, exemplar placement, failure-rate impact.
- `references/retry-patterns.md` — single-shot retry with parser-error feedback, when to escalate, when to fail.

## Related skills

- Structured *actions* are tool calls — [[tool-use-schema-design]].
- Structured-output failures look like tool failures at runtime — [[tool-failure-handling]].
- A retry policy is part of the [[agent-evaluation-harness]] surface.
- Cost climbs on retries — [[agent-cost-modeling]].
- Tier swap changes structured-output reliability — [[model-routing]].
- Schema-validation failures are first-class trace events — [[agent-observability]].
