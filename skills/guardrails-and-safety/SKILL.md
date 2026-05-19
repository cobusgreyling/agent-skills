---
name: guardrails-and-safety
description: >-
  Design guardrails for an LLM agent that handles user input, calls real tools,
  or operates in a regulated domain. Use when the user is building a
  user-facing agent and mentions guardrails, jailbreaks, prompt injection,
  content moderation, PII redaction, output validation, red-teaming, safety
  filters, or asks "how do I keep this agent from doing X?" / "how do I make
  this production-safe?".
tags:
  - safety
  - guardrails
  - red-teaming
  - production
---

# Guardrails and Safety

Safety isn't a wrapper, it's an architecture decision.

A "be safe" line in the system prompt is not a guardrail. A single output filter is not a guardrail. Safety in production is layered, observable, and tested against an explicit adversarial set — same rigour as functional evaluation.

## When to use this skill

- The user is building an agent that takes free-form user input.
- The user is exposing tools with real side-effects (writes, payments, messages).
- The user operates in a regulated domain (finance, health, legal, education).
- The user reports a jailbreak, prompt-injection, or unintended action incident.

## The five layers

Treat these as a stack. Skipping a layer is a deliberate choice with a cost.

1. **Input layer.** Schema validation, PII detection, prompt-injection detection, rate-limiting per user.
2. **Routing layer.** Classify the request; refuse out-of-scope traffic before it hits the agent.
3. **Model layer.** System prompt with explicit refusal contract, response-format constraints, tool subset by user role.
4. **Tool layer.** Server-side authorisation on every tool call. Allowlists, idempotency keys, side-effect confirmations.
5. **Output layer.** Schema validation, PII redaction, content moderation, optional second-pass review.

Two layers minimum for any user-facing agent. All five for anything writing to production systems.

## Decision flow

1. **Is the input from a human, an upstream LLM, or a document?** → all three need injection-resistant handling, not just the human case. Documents are the most under-defended vector today.
2. **Does the agent ever take an action with money, identity, or external messaging?** → require explicit per-action authorisation and a human-confirmation step for high-impact actions.
3. **Can a single bad output cause downstream harm?** → second-pass review or deterministic validator before the action commits.
4. **Is the domain regulated?** → guardrails are evidence, not just behaviour. Log everything.

## Anti-patterns to flag immediately

- **"Be safe" in the system prompt as the entire defence.** Adversarial input ignores polite requests.
- **Post-hoc output filter only.** Blocks the obvious, misses everything subtle, and stops nothing the model has already done via tools.
- **Trusting LLM-generated tool arguments without server-side validation.** The model is an untrusted client. Always.
- **Treating prompt injection as a model problem.** It's a context-source problem. Untrusted text needs explicit framing in the prompt and explicit constraints on tool calls.
- **No red-team set.** "We haven't seen any abuse" is not a defence.
- **Same model evaluating its own output.** Co-conspirator, not auditor. Use a different model or a deterministic checker.
- **Logging the prompt but not the tool calls.** Half a trace is no trace.

## Prompt-injection: the short version

- Untrusted content (user uploads, retrieved docs, tool outputs) must be **clearly delimited** in the prompt with explicit "treat as data, not instructions" framing.
- The model **will** follow embedded instructions in retrieved documents. Assume it. Test it.
- High-impact tools must require **out-of-band confirmation** that doesn't pass through the model — e.g. a user-facing button, not "type yes".

## Questions to ask the user

1. What is the **worst-case action** the agent can take in one call?
2. What is the **worst-case action** it can take in a sequence of calls?
3. Who is the **adversary** — random user, motivated abuser, regulator audit?
4. What signals indicate **abuse in progress** — and is anyone watching them?
5. What is the **rollback** if a guardrail fails?
6. Where will the **red-team set** live, and who owns it?

## What to log

- Every input verbatim (with PII redacted at log-write time, not after).
- Every tool call with arguments and outcome.
- Every refusal, with the rule that triggered it.
- Every classifier score above the noise floor — for tuning thresholds.

## The hard line

**No red-team set, no deploy.** Functional evals tell you the agent does the right thing; the red-team set tells you it won't do the wrong thing. Both gate merge.

## Why this exists

Most agent safety incidents in the wild are not novel attacks — they are the same handful of patterns (prompt injection via retrieved docs, tool-arg injection, role escalation, side-effect spam) and the same handful of missing layers. Naming the layers makes the missing one obvious. See [link to article on agent safety].

## References

- `references/prompt-injection.md` — vectors, framing patterns, test cases.
- `references/red-team-set.md` — how to build and maintain an adversarial set.
- `references/output-validation.md` — schema, PII, content moderation pipelines.

## Related skills

- Output validation depends on typed tool schemas — [[tool-use-schema-design]].
- Adversarial set runs through the eval harness — [[agent-evaluation-harness]].
- Safety incidents are diagnosed from traces — [[agent-observability]].
- Retrieved-doc injection is a retrieval problem — [[rag-vs-context-engineering]].
