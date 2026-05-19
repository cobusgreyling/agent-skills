# Results — agent-architecture-patterns

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
| aap-001 | no-agent-needed | `<P>` | `<F>` |
| aap-002 | multi-for-parallelism, freeform-chat, pattern-by-shape | `<P/P/P>` | `<F/F/F>` |
| aap-003 | unbounded-loop | `<P>` | `<F>` |
| aap-004 | multi-for-parallelism | `<P>` | `<F>` |
| aap-005 | shared-mutable-memory | `<P>` | `<F>` |
| aap-006 | pattern-by-shape, multi-for-parallelism | `<P/P>` | `<F/F>` |
| aap-007 | freeform-chat, unbounded-loop | `<P/P>` | `<F/F>` |
| aap-008 | pattern-by-shape, demands-eval | `<P/P>` | `<F/F>` |
| aap-009 | pattern-by-shape | `<P>` | `<F>` |
| aap-010 | pattern-by-shape, freeform-chat | `<P/P>` | `<F/F>` |
| aap-011 | pattern-by-shape | `<P>` | `<F>` |
| aap-012 | pattern-by-shape | `<P>` | `<F>` |
| aap-013 | demands-eval | `<P>` | `<F>` |
| aap-014 | pattern-by-shape, multi-for-parallelism | `<P/P>` | `<F/F>` |
| aap-015 | multi-for-parallelism, freeform-chat, pattern-by-shape | `<P/P/P>` | `<F/F/F>` |
| aap-016 | unbounded-loop, pattern-by-shape | `<P/P>` | `<F/F>` |
| aap-017 | shared-mutable-memory | `<P>` | `<F>` |
| aap-018 | multi-for-parallelism, pattern-by-shape | `<P/P>` | `<F/F>` |
| aap-019 | pattern-by-shape | `<P>` | `<F>` |
| aap-020 | unbounded-loop, pattern-by-shape, demands-eval | `<P/P/P>` | `<F/F/F>` |

## Observations

`<Fill in: which checks moved most? Where did the skill fail to fire? Any false positives — agent flagged a non-issue?>`

## Threshold to call the skill "working"

From `README.md`: a meaningful skill should produce ≥ +0.40 on the task-pass delta. A strong skill should produce ≥ +0.60. Record where this run lands and whether the threshold was met.
