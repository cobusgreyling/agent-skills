# Agent Skills

A curated collection of [Agent Skills](https://agentskills.io/home) — Markdown-based instructions that give AI coding agents (Claude Code, Gemini CLI, Cursor, Codex, etc.) durable domain expertise instead of one-shot prompting.

Opinionated, written from production triage of real agent failures. Each skill is a short, declarative brief: when to use it, the decision flow, the anti-patterns, the hard line that gates merge.

## Installation

### Option A — installer (recommended)

```bash
npx skills add cobusgreyling/agent-skills
```

The installer detects your agent and symlinks the selected skills into the right place (e.g. `~/.claude/skills/` for Claude Code).

> The `skills` CLI is a third-party installer; see its repo for status. If it does not work for your setup, use the manual path below.

### Option B — manual symlink

Clone the repo, then symlink the skill(s) you want into your agent's skills directory:

```bash
git clone https://github.com/cobusgreyling/agent-skills.git
cd agent-skills

# Claude Code
mkdir -p ~/.claude/skills
ln -sf "$PWD/skills/agent-architecture-patterns" ~/.claude/skills/

# Gemini CLI, Cursor, Codex: symlink into the equivalent directory for your agent.
```

Restart your agent. The skill should appear in the available-skills list and fire on matching prompts.

## Available Skills

<!-- BEGIN: auto-generated skill index -->
- [**agent-architecture-patterns**](./skills/agent-architecture-patterns) — Choose the right architecture for an LLM agent or multi-agent system. Use when the user is designing, comparing, or debugging agentic workflows and mentions ReAct, Reflexion, Plan-and-Execute, Router, Supervisor, Hierarchical, multi-agent, tool-use loop, agent graph, LangGraph, AutoGen, CrewAI, or asks "which agent pattern should I use" / "how should this agent be structured".  
  _tags:_ `architecture`, `patterns`, `multi-agent`, `design`
- [**agent-cost-modeling**](./skills/agent-cost-modeling) — Model the cost of an LLM agent before it ships, and after. Use when the user is planning a deployment, comparing patterns, choosing a model tier, or justifying a budget and mentions tokens per task, cost per task, unit economics, cost ceiling, cache hit rate, ReAct cost, multi-agent cost, or asks "how much will this cost?" / "is this economical at scale?".  
  _tags:_ `cost`, `production`, `architecture`, `economics`
- [**agent-evaluation-harness**](./skills/agent-evaluation-harness) — Design an evaluation harness for an LLM agent before shipping it. Use when the user is building or rewriting an agent, deciding ship/no-ship, debugging regressions, or mentions golden sets, eval suites, regression tests, trace-level evals, LLM-as-judge, scoring rubrics, or asks "how do I test this agent?" / "how do I know if my agent got better?".  
  _tags:_ `evaluation`, `production`, `regression`, `quality`
- [**agent-observability**](./skills/agent-observability) — Instrument an LLM agent so failures are diagnosable, traces are replayable, and evals can run against production data. Use when the user is moving an agent past prototype and mentions tracing, spans, OpenTelemetry, LangSmith, Langfuse, Arize, OpenLLMetry, structured logs, GenAI semantic conventions, or asks "how do I debug this agent in production?" / "what should I log?".  
  _tags:_ `observability`, `tracing`, `production`, `opentelemetry`
- [**guardrails-and-safety**](./skills/guardrails-and-safety) — Design guardrails for an LLM agent that handles user input, calls real tools, or operates in a regulated domain. Use when the user is building a user-facing agent and mentions guardrails, jailbreaks, prompt injection, content moderation, PII redaction, output validation, red-teaming, safety filters, or asks "how do I keep this agent from doing X?" / "how do I make this production-safe?".  
  _tags:_ `safety`, `guardrails`, `red-teaming`, `production`
- [**latency-budgeting**](./skills/latency-budgeting) — Budget and engineer latency for an LLM agent — TTFT, tokens-per-second, tool round-trips, parallelism, streaming. Use when the user is building a user-facing or real-time agent and mentions latency, p50, p95, p99, TTFT, streaming, throughput, time-to-first-token, slow agent, or asks "why is my agent slow?" / "how do I hit a 2-second latency target?".  
  _tags:_ `latency`, `production`, `performance`, `user-experience`
- [**prompt-caching**](./skills/prompt-caching) — Use prompt caching correctly across Anthropic, OpenAI, Bedrock, and Gemini to cut cost and latency on hot paths. Use when the user is building a production LLM app and mentions prompt caching, cache hits, cache key, cache TTL, ephemeral cache, system-prompt caching, or asks "why is my cache hit rate low?" / "should I cache this?".  
  _tags:_ `caching`, `cost`, `latency`, `production`, `claude`
- [**rag-vs-context-engineering**](./skills/rag-vs-context-engineering) — Decide between RAG, long-context, structured tool retrieval, and prompt-only approaches for grounding an LLM in private or fresh data. Use when the user is designing a knowledge-grounded agent or chatbot and mentions RAG, vector search, embeddings, retrieval, chunking, long context, context window, tool retrieval, hybrid search, rerank, or asks "do I need RAG?" / "should I just use a big context window?".  
  _tags:_ `rag`, `retrieval`, `context-engineering`, `architecture`
- [**tool-use-schema-design**](./skills/tool-use-schema-design) — Design tool schemas (function-calling definitions) that LLMs can use reliably. Use when the user is defining tools for Claude, GPT, Gemini, or any function-calling agent and mentions tool definitions, function calling, JSON schema, tool descriptions, parameters, structured outputs, MCP tools, or asks "why is the model calling my tool wrong?" / "how should I design this tool?".  
  _tags:_ `tool-use`, `function-calling`, `mcp`, `architecture`
<!-- END: auto-generated skill index -->

> Regenerated by `python scripts/build_index.py`. CI fails if this section drifts.

## Skills by tag

<!-- BEGIN: auto-generated tag matrix -->
| Tag | Skills |
| --- | --- |
| `architecture` | [agent-architecture-patterns](./skills/agent-architecture-patterns), [agent-cost-modeling](./skills/agent-cost-modeling), [rag-vs-context-engineering](./skills/rag-vs-context-engineering), [tool-use-schema-design](./skills/tool-use-schema-design) |
| `caching` | [prompt-caching](./skills/prompt-caching) |
| `claude` | [prompt-caching](./skills/prompt-caching) |
| `context-engineering` | [rag-vs-context-engineering](./skills/rag-vs-context-engineering) |
| `cost` | [agent-cost-modeling](./skills/agent-cost-modeling), [prompt-caching](./skills/prompt-caching) |
| `design` | [agent-architecture-patterns](./skills/agent-architecture-patterns) |
| `economics` | [agent-cost-modeling](./skills/agent-cost-modeling) |
| `evaluation` | [agent-evaluation-harness](./skills/agent-evaluation-harness) |
| `function-calling` | [tool-use-schema-design](./skills/tool-use-schema-design) |
| `guardrails` | [guardrails-and-safety](./skills/guardrails-and-safety) |
| `latency` | [latency-budgeting](./skills/latency-budgeting), [prompt-caching](./skills/prompt-caching) |
| `mcp` | [tool-use-schema-design](./skills/tool-use-schema-design) |
| `multi-agent` | [agent-architecture-patterns](./skills/agent-architecture-patterns) |
| `observability` | [agent-observability](./skills/agent-observability) |
| `opentelemetry` | [agent-observability](./skills/agent-observability) |
| `patterns` | [agent-architecture-patterns](./skills/agent-architecture-patterns) |
| `performance` | [latency-budgeting](./skills/latency-budgeting) |
| `production` | [agent-cost-modeling](./skills/agent-cost-modeling), [agent-evaluation-harness](./skills/agent-evaluation-harness), [agent-observability](./skills/agent-observability), [guardrails-and-safety](./skills/guardrails-and-safety), [latency-budgeting](./skills/latency-budgeting), [prompt-caching](./skills/prompt-caching) |
| `quality` | [agent-evaluation-harness](./skills/agent-evaluation-harness) |
| `rag` | [rag-vs-context-engineering](./skills/rag-vs-context-engineering) |
| `red-teaming` | [guardrails-and-safety](./skills/guardrails-and-safety) |
| `regression` | [agent-evaluation-harness](./skills/agent-evaluation-harness) |
| `retrieval` | [rag-vs-context-engineering](./skills/rag-vs-context-engineering) |
| `safety` | [guardrails-and-safety](./skills/guardrails-and-safety) |
| `tool-use` | [tool-use-schema-design](./skills/tool-use-schema-design) |
| `tracing` | [agent-observability](./skills/agent-observability) |
| `user-experience` | [latency-budgeting](./skills/latency-budgeting) |
<!-- END: auto-generated tag matrix -->

## Contributing a skill

1. Create `skills/<your-skill>/SKILL.md` with the frontmatter shown below.
2. Write a `description:` that names the **products, verbs, and keywords** that should fire the skill. Vague descriptions don't trigger.
3. Add `tags:` — kebab-case, max 8, drawn from the existing tag matrix where possible.
4. Add an `EXAMPLES.md` with 2–3 prompt/expected-behaviour pairs that demonstrate the skill firing correctly.
5. Put long material (CLI tables, deep-dives) under `references/` so the agent loads it on demand.
6. Run `python scripts/lint_skills.py` and `python scripts/build_index.py` before opening a PR.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the end-to-end walkthrough.

## Layout

```
skills/
  <skill-name>/
    SKILL.md          # frontmatter + master prompt
    EXAMPLES.md       # 2–3 prompt/behaviour pairs
    references/       # optional sub-docs the agent loads on demand
```

Each `SKILL.md` begins with YAML frontmatter:

```yaml
---
name: skill-name
description: >-
  One- or two-sentence trigger description. The agent reads this to decide
  whether the skill is relevant. Be specific about WHEN to use it.
tags:
  - kebab-case
  - up-to-eight
---
```

The body is a normal Markdown prompt: prerequisites, commands, gotchas, examples. Each skill ends with a short **Why this exists** section linking to the original article or incident that motivated it.

## License

Apache 2.0 — see [LICENSE](./LICENSE).
