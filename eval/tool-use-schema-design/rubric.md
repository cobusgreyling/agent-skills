# Scoring Rubric — tool-use-schema-design eval

The scorer reads one agent response and the task's `checks` list. For each check, it returns `pass`, `fail`, or `partial`.

## Per-check criteria

### `flags-kitchen-sink`

The response should:

- Name the pattern explicitly (kitchen-sink, do-everything, universal-entry-point, "tool that needs 'or' to describe").
- Propose splitting into ≥2 purpose-built tools with `verb_noun` names.
- Optionally cite the rule "if the description needs the word 'or', split the tool".

**Pass:** all three. **Partial:** names the pattern and proposes a split but with vague names. **Fail:** implements what was asked; does not flag the design.

### `flags-free-text-payload`

The response should:

- Name `payload: object` / `payload: string` / `data: object` as an anti-pattern.
- Explain *why*: the model is forced to serialise into an unstructured shape; it will fail.
- Replace with typed per-tool parameters.

**Pass:** all three. **Partial:** names it but does not replace. **Fail:** accepts the free-text payload.

### `flags-missing-idempotency`

The response should:

- Identify the action as destructive / irreversible / high-impact.
- Require either an `idempotency_key` parameter **or** a propose/commit split (`propose_X` + `commit_X`).
- Optionally call out the need for out-of-band confirmation for high-impact cases.

**Pass:** both first points. **Partial:** flags the risk but doesn't propose a concrete mechanism. **Fail:** wraps the action with no safety scaffolding.

### `flags-untyped-enum`

The response should:

- Identify a closed-set parameter masquerading as a string.
- Require an `enum` type (or equivalent typed constraint).
- Optionally cite: "string with 'must be one of X,Y,Z' in the description leaks".

**Pass:** all three. **Partial:** names the issue but suggests only "make the description clearer". **Fail:** accepts the untyped string.

### `flags-overlapping-tools`

The response should:

- Identify the overlap and the cost (model alternates, confuses itself).
- Recommend either consolidation (one tool, typed mode parameter) or full separation (clearly distinct names, descriptions, parameters).

**Pass:** both. **Partial:** names the problem but doesn't recommend a structural fix. **Fail:** suggests "better descriptions" as the fix.

### `flags-silent-failure`

The response should:

- Identify that the tool's failure mode (empty result, 200-with-error-body, HTML output) hides errors from the model.
- Require a typed error shape: status code or discriminated union, with reason codes.
- Reject "tell the model better" as a fix — the schema is the contract.

**Pass:** all three. **Partial:** names the issue but recommends a prompt-side workaround. **Fail:** accepts the silent failure.

### `flags-magic-sentinel`

The response should:

- Identify the sentinel (`-1`, `"all"`, empty value with overloaded meaning).
- Require a separate boolean / different tool / pagination instead.
- Optionally explain: sentinels are bug factories because the model conflates them with real values.

**Pass:** all three. **Partial:** suggests adding documentation. **Fail:** accepts the sentinel.

## Overall task scoring

A task is **passed** if all its listed checks return `pass`. A task is **partial** if at least one returns `partial` and the rest are `pass` or `partial`. A task is **failed** if any check returns `fail`.

The delta the eval measures: **(passed-with-skill − passed-without-skill) / 20**. A meaningful skill should produce ≥ +0.40 on this delta; a strong skill should produce ≥ +0.60.

## Judging notes

- Use a different model than the one being evaluated. Same-model self-judging is co-conspirator territory.
- Run with `temperature=0` for both eval generation and scoring.
- See `rubric_anchors.md` for 2-3 anchored examples per check level.
