# Agent Skills

Personal collection of [Agent Skills](https://agentskills.io/home) — Markdown-based instructions that give AI coding agents (Claude Code, Gemini CLI, Cursor, Codex, etc.) domain expertise without re-prompting every session.

## Installation

```bash
npx skills add cobusgreyling/agent-skills
```

The installer detects your agent and symlinks the selected skills into the right place (e.g. `~/.claude/skills/` for Claude Code).

## Available Skills

- [**example-skill**](./skills/example-skill) — Starter template demonstrating the SKILL.md structure. Replace or delete before publishing real skills.

## Layout

```
skills/
  <skill-name>/
    SKILL.md          # frontmatter + master prompt
    references/       # optional sub-docs the agent loads on demand
```

Each `SKILL.md` begins with YAML frontmatter:

```yaml
---
name: skill-name
description: >-
  One- or two-sentence trigger description. The agent reads this to decide
  whether the skill is relevant. Be specific about WHEN to use it.
---
```

The body is a normal Markdown prompt: prerequisites, commands, gotchas, examples.

## License

Apache 2.0 — see [LICENSE](./LICENSE).
