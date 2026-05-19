# Results — tool-use-schema-design

> **Status: awaiting first run.** This file is a template. Replace the placeholder rows after running `score.py` and commit your numbers.

## Setup used

| Field | Value |
|---|---|
| Eval revision (commit SHA) | `<fill in>` |
| Agent under test | `<e.g. Claude Code with claude-opus-4-7>` |
| Judge model | `claude-sonnet-4-6` (or other; must differ from agent under test) |
| Temperature | `0` |
| Runs averaged | `1` (single-pass) |
| Date | `<YYYY-MM-DD>` |

## Headline

| Metric | With skill | Without skill | Delta |
|---|---|---|---|
| Tasks passed (all checks PASS) | `<x>/20` | `<y>/20` | `<+/-z%>` |
| Tasks partial-or-pass | `<x>/20` | `<y>/20` | `<+/-z%>` |
| Total checks passed | `<x>/<N>` | `<y>/<N>` | `<+/-z%>` |

## Per-task breakdown

| Task | Checks | With skill | Without skill |
|---|---|---|---|
| tusd-001 | kitchen-sink, free-text-payload, missing-idempotency | `<P/P/P>` | `<F/F/F>` |
| tusd-002 | kitchen-sink, free-text-payload | `<P/P>` | `<F/F>` |
| tusd-003 | missing-idempotency | `<P>` | `<F>` |
| tusd-004 | untyped-enum | `<P>` | `<F>` |
| tusd-005 | overlapping-tools | `<P>` | `<F>` |
| tusd-006 | silent-failure | `<P>` | `<F>` |
| tusd-007 | magic-sentinel, untyped-enum | `<P/P>` | `<F/F>` |
| tusd-008 | untyped-enum | `<P>` | `<F>` |
| tusd-009 | kitchen-sink | `<P>` | `<F>` |
| tusd-010 | silent-failure | `<P>` | `<F>` |
| tusd-011 | missing-idempotency | `<P>` | `<F>` |
| tusd-012 | silent-failure | `<P>` | `<F>` |
| tusd-013 | kitchen-sink, free-text-payload | `<P/P>` | `<F/F>` |
| tusd-014 | silent-failure | `<P>` | `<F>` |
| tusd-015 | kitchen-sink, missing-idempotency | `<P/P>` | `<F/F>` |
| tusd-016 | magic-sentinel | `<P>` | `<F>` |
| tusd-017 | missing-idempotency | `<P>` | `<F>` |
| tusd-018 | untyped-enum, overlapping-tools | `<P/P>` | `<F/F>` |
| tusd-019 | kitchen-sink | `<P>` | `<F>` |
| tusd-020 | overlapping-tools | `<P>` | `<F>` |

## Observations

`<Fill in: which checks moved most? Where did the skill fail to fire? Any false positives — agent flagged a non-issue?>`

## Threshold to call the skill "working"

From `README.md`: a meaningful skill should produce ≥ +0.40 on the task-pass delta. A strong skill should produce ≥ +0.60. Record where this run lands and whether the threshold was met.
