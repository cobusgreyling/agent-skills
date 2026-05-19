# Results — prompt-caching

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
| pcache-001 | dynamic-prefix | `<P>` | `<F>` |
| pcache-002 | explicit-breakpoints, no-measurement | `<P/P>` | `<F/F>` |
| pcache-003 | no-measurement | `<P>` | `<F>` |
| pcache-004 | cache-write-cost | `<P>` | `<F>` |
| pcache-005 | cross-user-cache, dynamic-prefix | `<P/P>` | `<F/F>` |
| pcache-006 | ttl-cold-start | `<P>` | `<F>` |
| pcache-007 | unstable-ordering | `<P>` | `<F>` |
| pcache-008 | cache-write-cost | `<P>` | `<F>` |
| pcache-009 | explicit-breakpoints, cache-write-cost | `<P/P>` | `<F/F>` |
| pcache-010 | explicit-breakpoints | `<P>` | `<F>` |
| pcache-011 | dynamic-prefix | `<P>` | `<F>` |
| pcache-012 | explicit-breakpoints | `<P>` | `<F>` |
| pcache-013 | dynamic-prefix, no-measurement | `<P/P>` | `<F/F>` |
| pcache-014 | dynamic-prefix | `<P>` | `<F>` |
| pcache-015 | dynamic-prefix | `<P>` | `<F>` |
| pcache-016 | explicit-breakpoints | `<P>` | `<F>` |
| pcache-017 | cache-write-cost, no-measurement | `<P/P>` | `<F/F>` |
| pcache-018 | explicit-breakpoints | `<P>` | `<F>` |
| pcache-019 | cross-user-cache, explicit-breakpoints | `<P/P>` | `<F/F>` |
| pcache-020 | explicit-breakpoints | `<P>` | `<F>` |

## Observations

`<Fill in: which checks moved most? Where did the skill fail to fire? Any false positives — agent flagged a non-issue?>`

## Threshold to call the skill "working"

From `README.md`: a meaningful skill should produce ≥ +0.40 on the task-pass delta. A strong skill should produce ≥ +0.60. Record where this run lands and whether the threshold was met.
