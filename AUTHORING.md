# Authoring a Skill — house style

This is the meta-skill. Read it before writing a new `SKILL.md`. It encodes the conventions every skill in this repo follows, so the collection reads as one voice rather than nine.

For the end-to-end PR walkthrough (commands, lint, index), see [CONTRIBUTING.md](./CONTRIBUTING.md). This file is about the *content*.

## Before you start

A skill is worth writing when **all three** of these hold:

1. **You've debugged it.** Not "I've read about it" — you've seen the failure pattern in production triage at least three times.
2. **The trigger is specific.** There's a recognisable user prompt or symptom that should fire it.
3. **It changes behaviour, not vocabulary.** Without the skill, the agent gives different (worse) advice.

If "the model just knows that", skip. If "it's just nice general advice", skip.

## The house style — eight conventions

### 1. One hard line per skill

Every skill closes its argument with one bolded sentence in **The hard line** that gates merge, deploy, or approval. Not advice — a rule. The hard line is the thing the agent should remember when the rest of the skill has fallen out of context.

Examples from this repo:

- *"If the schema needs a paragraph to explain when to call the tool, split the tool."*
- *"Every production call gets a trace. Otherwise, you're guessing."*
- *"Never auto-retry a non-idempotent write."*
- *"A judge that hasn't been meta-evaluated isn't a scorer; it's a vibes amplifier."*

If you can't write the hard line, you haven't found the thesis yet.

### 2. Anti-patterns are named, not hinted

Use the literal phrase **"Anti-patterns to flag immediately"** as a section. Each anti-pattern is one bolded name + one short explanation. The agent scans this list on every prompt that fires the skill.

```markdown
## Anti-patterns to flag immediately

- **Kitchen-sink tools.** The model has to guess `action`; your schema teaches it nothing.
- **Free-text payload parameters.** You've made the model serialise into a string. It will fail.
```

Avoid: "be careful with ...", "try to avoid ...", "consider whether ...". The voice is declarative.

### 3. Decision flow is numbered, top-down, and walked before recommending

Numbered list, ≤7 steps, each step is a question the agent answers before the next. The flow ends in a concrete pattern recommendation, not a "consider the trade-offs". This is how the skill resists generic answers.

```markdown
## Decision flow

1. **Is the task single-turn deterministic?** → no agent. Use a typed tool call.
2. **Is the path knowable up front?** → Plan-and-Execute.
3. **Is the path discoverable only by trying?** → ReAct.
```

### 4. Questions to ask the user

A numbered list the agent uses to elicit missing context before answering. ≤8 questions. Each question maps to a real decision; vague questions go in the trash.

If you can't generate 5 specific questions, the skill isn't ready.

### 5. Cross-link with `[[wiki-style]]` to related skills

Every skill ends with a `## Related skills` section linking by name. Use `[[skill-name]]` syntax. Skills point at the next decision along the path: architecture → cost → latency → eval → observability → guardrails → safety → memory → routing.

Cross-linking is not optional. It turns the collection from a list into a graph.

### 6. Terse declarative; one sentence per line where it earns it

- No hedging. "Consider possibly maybe" → cut.
- No "in general" / "it depends" without a follow-up rule.
- Bullets short. If a bullet needs three sentences, split.
- Italic emphasis sparingly. Bold for the *name* of an anti-pattern or rule.
- No emojis.

Read your draft out loud. If it sounds like a panel discussion, rewrite.

### 7. Schema and structure are fixed

Every `SKILL.md` has these sections, in this order:

```
---
name: ...
description: >- (verb + "Use when..." + trigger keywords + 2-3 user phrasings)
tags: (3-5, kebab-case, drawn from existing tag matrix where possible)
---

# Title

> One-line hook — the skill's thesis in a sentence.

Short opening paragraph (2-3 sentences) — frame the problem.

## When to use this skill
- 3-5 bullets, the situations where the skill should fire.

## Decision flow  OR  The N rules
- Numbered, top-down, walkable.

## (Optional) Patterns / mechanisms / one-liners
- One line each, scannable.

## Anti-patterns to flag immediately
- Bold name + short reason, ≥5 entries.

## Questions to ask the user
- Numbered, ≤8, specific.

## The hard line
- **One bolded sentence.**

## Why this exists
- 2-3 sentences. Links to the article or incident.

## References
- Pointer to `references/X.md` files for long material.

## Related skills
- [[wiki-links]] to adjacent skills.
```

Deviations need a reason.

### 8. Description that actually triggers

The `description:` frontmatter is the skill's resume — agents read it to decide whether to fire. Make it specific:

- Start with a verb of the form "Do X for / when …".
- Include the **products, tools, keywords** the user will mention ("Anthropic / OpenAI / Gemini", "tool definitions / JSON schema / MCP").
- Include 2-3 example user phrasings ('asks "why is X slow?" / "should I cache this?"').
- 100-300 words. Vague descriptions don't trigger.

## Proof — every skill ships a TRANSCRIPT.md

`TRANSCRIPT.md` is non-negotiable for new skills. Structure:

```markdown
# Transcript — <skill-name>

> Side-by-side behavioural exemplar. Composite responses, not a single literal run.

## Prompt
> A realistic user prompt that should trigger this skill.

## Without skill (typical baseline)
> What a competent generic coding agent says without the skill loaded.

(One-line summary of what this answer misses.)

## With skill (behavioural expectation)
> What the agent says with this skill loaded — refuses what should be refused, names anti-patterns, walks the decision flow, ends with the hard line.

## The diff
- Bulleted list of what changed because the skill fired.

A naive answer X. A skilled answer Y.
```

This is the artefact that makes "the skill changes behaviour" auditable. If you can't write the side-by-side, the skill isn't worth shipping.

## Eval — recommended for high-claim skills

If your skill makes ≥5 distinct claims about agent behaviour, write a 20-task eval under `eval/<skill-name>/`. See `eval/tool-use-schema-design/` for the canonical example. Each eval needs:

- `tasks.jsonl` — 20 prompts with per-task `checks` (claim IDs).
- `rubric.md` — per-check pass/partial/fail criteria.
- `rubric_anchors.md` — one anchored pass/partial/fail example per check.
- `run_eval.py` — runs prompts against an agent with/without the skill loaded.
- `score.py` — applies the rubric via a different-family judge model.
- `results.md` — template for the user to fill in.
- `README.md` — methodology + how to run.

Evals are the receipts. They take a weekend; they're worth it.

## Model-version pin (optional, recommended)

If your TRANSCRIPT.md or eval ran against a specific model version, note it in the frontmatter:

```yaml
tested_against:
  - claude-opus-4-7
  - gpt-5
  - gemini-2.5-pro
last_tested: 2026-05-19
```

Models change quarterly; without a pin, readers can't tell what's stale. The `scripts/transcript_regression.py` tool re-runs transcripts against current models to catch drift.

## What NOT to write

- **A skill about your favourite framework.** Patterns travel; frameworks don't. The skill is the pattern.
- **A skill that's a tutorial.** "Here's how to use LangChain" is documentation. A skill is a *behavioural directive*.
- **A skill without a hard line.** Means you have advice, not a rule. Rewrite or skip.
- **A skill that's actually two skills.** If the description needs "and" twice, split.
- **A skill the model already does well.** Run a TRANSCRIPT first; if the without-skill answer is already correct, you haven't found a gap.

## Style sanity check before opening a PR

- Hard line present, bolded, gates merge/deploy/approval.
- ≥5 named anti-patterns.
- Decision flow numbered, top-down, ≤7 steps.
- ≥5 specific questions in "Questions to ask the user".
- TRANSCRIPT.md side-by-side with annotated diff.
- Cross-links to ≥3 related skills.
- `python scripts/lint_skills.py` clean.
- `python scripts/build_index.py` regenerated README and skills.json.
- No emojis. No filler. No hedging.

## License

By contributing you agree your contribution is licensed under Apache 2.0 to match the repo.
