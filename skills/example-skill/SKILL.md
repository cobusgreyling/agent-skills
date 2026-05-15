---
name: example-skill
description: >-
  Starter template demonstrating the SKILL.md structure. Replace this description
  with a specific trigger so the agent knows WHEN to load the skill — e.g. tools
  it operates on, tasks it handles, keywords that should fire it.
---

# Example Skill

Replace this file with your own skill. The agent reads the frontmatter `description`
to decide whether to load this skill, so make it concrete: name the product,
the verbs, and the keywords that should trigger it.

## When to use

List the conditions under which this skill should activate. Be specific.

- The user mentions <product / tool / framework>
- The user asks to <task>
- A file matching <pattern> is in scope

## Prerequisites

- CLI / SDK / credential requirements
- IAM / permissions
- Environment variables

## Core workflow

Step-by-step instructions the agent should follow. Use concrete commands
rather than prose.

```bash
# example: replace with your real command
your-cli do-thing --flag value
```

## Gotchas

- Things that look right but break
- Defaults that differ from common assumptions
- Region / version / quota traps

## References

Sub-docs in `./references/` are loaded on demand. Use them for long material
the agent doesn't always need:

- `references/cli.md` — full CLI flag reference
- `references/iam.md` — least-privilege roles
- `references/examples.md` — worked examples
