# Results — agent-cost-modeling

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
| acm-001 | missing-ceiling, call-graph, wrong-tier | `<P/P/P>` | `<F/F/F>` |
| acm-002 | call-graph, cache-ignored | `<P/P>` | `<F/F>` |
| acm-003 | unbounded-loop-cost | `<P>` | `<F>` |
| acm-004 | cache-ignored | `<P>` | `<F>` |
| acm-005 | cache-ignored, non-model-costs, failed-task | `<P/P/P>` | `<F/F/F>` |
| acm-006 | non-model-costs, cache-ignored, failed-task | `<P/P/P>` | `<F/F/F>` |
| acm-007 | wrong-tier | `<P>` | `<F>` |
| acm-008 | call-graph | `<P>` | `<F>` |
| acm-009 | failed-task | `<P>` | `<F>` |
| acm-010 | non-model-costs | `<P>` | `<F>` |
| acm-011 | call-graph, cache-ignored, wrong-tier | `<P/P/P>` | `<F/F/F>` |
| acm-012 | missing-ceiling | `<P>` | `<F>` |
| acm-013 | wrong-tier, failed-task | `<P/P>` | `<F/F>` |
| acm-014 | cache-ignored | `<P>` | `<F>` |
| acm-015 | cache-ignored, non-model-costs | `<P/P>` | `<F/F>` |
| acm-016 | non-model-costs | `<P>` | `<F>` |
| acm-017 | call-graph, failed-task | `<P/P>` | `<F/F>` |
| acm-018 | call-graph, failed-task | `<P/P>` | `<F/F>` |
| acm-019 | call-graph | `<P>` | `<F>` |
| acm-020 | cache-ignored, call-graph, wrong-tier | `<P/P/P>` | `<F/F/F>` |

## Observations

`<Fill in: which checks moved most? Where did the skill fail to fire? Any false positives — agent flagged a non-issue?>`

## Threshold to call the skill "working"

From `README.md`: a meaningful skill should produce ≥ +0.40 on the task-pass delta. A strong skill should produce ≥ +0.60. Record where this run lands and whether the threshold was met.
