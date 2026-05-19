---
name: tool-use-schema-design
description: >-
  Design tool schemas (function-calling definitions) that LLMs can use
  reliably. Use when the user is defining tools for Claude, GPT, Gemini, or
  any function-calling agent and mentions tool definitions, function calling,
  JSON schema, tool descriptions, parameters, structured outputs, MCP tools,
  or asks "why is the model calling my tool wrong?" / "how should I design
  this tool?".
tags:
  - tool-use
  - function-calling
  - mcp
  - architecture
---

# Tool-Use Schema Design

Tool schemas are prompts. Bad schemas drive bad calls more than bad prompts do.

The model sees your tool definitions as part of its context. A confusing name, an under-described parameter, or an overloaded tool will make the most carefully-prompted agent unreliable.

## When to use this skill

- The user is defining tools for a function-calling agent (Claude, GPT, Gemini, Bedrock, MCP server).
- The user reports the model calling tools with wrong arguments, in the wrong order, or not at all.
- The user is exposing an internal API to an LLM and copying the existing signatures.
- The user is adding a new tool to a working agent and the agent regresses.

## The five rules

1. **One tool, one job.** If the description needs the word "or", split the tool.
2. **Names are the strongest signal.** `get_customer_by_id` is unambiguous; `fetch` is not. Verbs + nouns + scope.
3. **Every parameter has a description, an example, and a constraint.** The model reads all three.
4. **Return shapes are part of the schema.** Documented, typed, and stable. Models reason about returns when planning next calls.
5. **Errors are first-class.** Define what failure looks like — typed error codes, not freeform strings — so the model can recover deterministically.

## Decision flow when designing a new tool

1. **Can a single existing tool already do this?** → extend its description, don't add a new tool. Tool-list bloat hurts every call.
2. **Is the action reversible?** → no? Require an explicit confirmation argument or split into `propose_X` + `commit_X`.
3. **Does the tool have ≥4 parameters, or any optional ones?** → consider splitting by use-case. Optional parameters are where models hallucinate.
4. **Does the tool return >1 page of data?** → add pagination *and* a summary mode. Models drown in raw lists.
5. **Could the tool be called in a loop?** → add a hard limit in the description and enforce it server-side.

## Naming patterns that work

- `verb_noun` for actions: `create_invoice`, `cancel_order`.
- `get_noun_by_key` for lookups: `get_user_by_email`, `get_doc_by_id`.
- `list_noun` for collections (with pagination): `list_open_tickets`.
- `search_noun` for fuzzy queries: `search_products`.

Avoid `do_thing`, `helper`, `util`, `process`, `handle` — every one of these is a smell.

## Parameter design rules

- **Types are load-bearing.** Use enums for closed sets; the model will follow them. String parameters with "must be one of X, Y, Z" in the description leak.
- **IDs over names where ambiguity matters.** `customer_id` not `customer_name`. The model will happily invent a name.
- **Dates are ISO 8601, in UTC.** Every other choice causes silent bugs.
- **No "magic" sentinel values.** `-1` for "all" is a bug factory. Use a separate boolean or a different tool.
- **Required vs optional matters.** If a parameter is "usually filled in", make it required and document the default explicitly.

## Anti-patterns to flag immediately

- **Kitchen-sink tools** (`do_anything(action, payload)`). The model has to guess `action`, and your schema teaches it nothing.
- **Free-text payload parameters** (`payload: string`). You've made the model serialise into a string. It will fail.
- **Two tools that overlap by 80%.** Pick one; the model alternates and confuses itself.
- **Returning HTML or markup** instead of structured data. The model now has to parse strings to plan.
- **Silent failure** (returning empty results on error). The model thinks success and proceeds.
- **No examples in descriptions.** One concrete example doubles reliability for the cost of one sentence.

## Questions to ask the user

1. What does the tool **do in one verb**? If you need two, split it.
2. What is the **smallest set of parameters** that fully specify the action?
3. What does the tool return on **success, partial success, and failure**?
4. Is the action **idempotent**? If not, who owns retry safety?
5. What's the **rate or call-budget** the agent must respect?
6. How will you **observe** every call (input, output, latency, error)?

## The hard line

**If the schema needs a paragraph to explain when to call the tool, split the tool.** The schema is the contract; if humans can't read it, the model can't either.

## Why this exists

In production triage of agent failures, "the model called the tool wrong" is almost always "the tool didn't tell the model how to call it right." Tool design is the highest-leverage, lowest-effort lever on agent reliability — and the most ignored. See [link to article on tool design].

## References

- `references/parameter-patterns.md` — enums, IDs, dates, pagination, idempotency keys.
- `references/error-shapes.md` — typed error codes the model can recover from.
- `references/mcp-notes.md` — MCP-specific schema conventions and gotchas.
