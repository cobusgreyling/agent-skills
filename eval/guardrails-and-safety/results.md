# Results — guardrails-and-safety

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
| gs-001 | prompt-only-defense | `<P>` | `<F>` |
| gs-002 | output-filter-only, no-server-side | `<P/P>` | `<F/F>` |
| gs-003 | no-server-side, oob-confirmation | `<P/P>` | `<F/F>` |
| gs-004 | prompt-only-defense, missing-redteam | `<P/P>` | `<F/F>` |
| gs-005 | indirect-injection | `<P>` | `<F>` |
| gs-006 | oob-confirmation, prompt-only-defense | `<P/P>` | `<F/F>` |
| gs-007 | self-judging | `<P>` | `<F>` |
| gs-008 | no-server-side | `<P>` | `<F>` |
| gs-009 | missing-redteam | `<P>` | `<F>` |
| gs-010 | indirect-injection, oob-confirmation | `<P/P>` | `<F/F>` |
| gs-011 | missing-redteam | `<P>` | `<F>` |
| gs-012 | output-filter-only | `<P>` | `<F>` |
| gs-013 | no-server-side | `<P>` | `<F>` |
| gs-014 | prompt-only-defense | `<P>` | `<F>` |
| gs-015 | missing-redteam | `<P>` | `<F>` |
| gs-016 | output-filter-only, no-server-side | `<P/P>` | `<F/F>` |
| gs-017 | missing-redteam | `<P>` | `<F>` |
| gs-018 | indirect-injection, no-server-side | `<P/P>` | `<F/F>` |
| gs-019 | missing-redteam, prompt-only-defense | `<P/P>` | `<F/F>` |
| gs-020 | oob-confirmation, no-server-side | `<P/P>` | `<F/F>` |

## Observations

`<Fill in: which checks moved most? Where did the skill fail to fire? Any false positives — agent flagged a non-issue?>`

## Threshold to call the skill "working"

From `README.md`: a meaningful skill should produce ≥ +0.40 on the task-pass delta. A strong skill should produce ≥ +0.60. Record where this run lands and whether the threshold was met.
