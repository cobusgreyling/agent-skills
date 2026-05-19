# Contributing a Skill

This guide walks you end-to-end through adding a new skill. Goal: a PR that lints cleanly, builds a fresh README index, and is mergeable on first review.

## Before you start

A skill is worth writing when **all three** of these are true:

1. The advice is **non-obvious** — you've debugged it in production, or you've seen others get it wrong repeatedly.
2. The trigger is **specific** — there's a recognisable user prompt or symptom that should fire it.
3. The skill changes **behaviour**, not just vocabulary — without it, the agent gives different (worse) advice.

If a skill could be replaced by "the model just knows that", skip it.

## End-to-end walkthrough

We'll add a fictional skill `example-skill` to show the full flow.

### 1. Create the directory

```bash
mkdir -p skills/example-skill
```

### 2. Write `SKILL.md`

Start with frontmatter:

```yaml
---
name: example-skill
description: >-
  One- or two-sentence trigger description. Name the **products, verbs, and
  keywords** that should fire the skill. Include 2–3 example user phrasings
  ("how do I X" / "why is Y slow").
tags:
  - kebab-case
  - max-eight
---
```

Body conventions (match the existing skills):

- **Opening line:** one strong declarative sentence that frames the skill's thesis.
- **`When to use this skill`** — bullet list of triggering situations.
- **Decision flow** — numbered, top-down. Walked before recommending anything.
- **Anti-patterns to flag immediately** — bullet list, one line each. This is what the agent watches for.
- **Questions to ask the user** — numbered. If the user can't answer them, the skill says so.
- **The hard line** — one sentence that gates merge / deploy / approval.
- **Why this exists** — 2–3 lines explaining the motivation; link to the article or incident.
- **References** — sub-docs under `references/` that load on demand.

Keep the body under 10 kB. Long material (tables, deep-dives) goes in `references/`.

### 3. Add `EXAMPLES.md`

Two to three prompt/expected-behaviour pairs. Each demonstrates the skill firing on a realistic user prompt and *changing* the agent's response. See any existing skill's `EXAMPLES.md` for the format.

### 4. Add `references/` (optional)

```
skills/example-skill/
  SKILL.md
  EXAMPLES.md
  references/
    deep-dive.md
```

Reference `references/deep-dive.md` from `SKILL.md` so the agent loads it on demand.

### 5. Lint and rebuild the index

```bash
pip install pyyaml
python scripts/lint_skills.py
python scripts/build_index.py
```

The first command validates frontmatter (name, description, tags, body size). The second regenerates the "Available Skills" section and the tag matrix in `README.md`.

Commit the README change with your skill.

### 6. Paste the lint output into your PR

The PR template asks for the `lint_skills.py` output. Paste it. PRs that don't pass lint are not merged.

## Tagging guidance

- Draw from existing tags where possible (see the tag matrix in `README.md`).
- Don't invent a tag that only one skill will use — tags are for navigation, not metadata.
- Maximum 8 tags per skill. Aim for 3–5.

## Style

- Terse, declarative, opinionated.
- One sentence per line for emphasis where it earns it.
- Hard lines and anti-patterns over hedged advice.
- No emoji.

## License

By contributing you agree your contribution is licensed under Apache 2.0 to match the repo.
