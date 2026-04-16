---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder (architect)
re: Final housekeeping before v2.3 scope approval — close three stale open questions
status: DIRECTIVE — small cleanup, then scope is approved
---

# Main Terminal Update — 2026-04-16 (a)

Round 4 accepted. Substance of Track 6 amendments + Stream C
verdict + forensic = all correct. One small housekeeping
pass before v2.3 scope is formally approved.

## The only task

Edit `review/comms/PLAN_V23_SCOPE_2026-04-15.md` "Open
Questions for Owner Review" section. All three questions are
stale and should be removed (or answered-in-place) because
they have been resolved since the initial draft:

### Open Question 1 — Track B fallback

> "The 206-hand allocation assumes the BP generator fix (Track
> B) is complete before supplement generation starts. If Track
> B slips, the factory-sourced cohort (approx 166 hands) cannot
> be generated reliably. Is there a fallback if Track B is
> delayed?"

**Remove.** Track B (referred to elsewhere as Track 5) is
complete as of commit `b69e668`. Fix 1 applied to all 5
generators, factory_batch5 JSONL regenerated, pre-flight schema
gate wired. No fallback needed because no slip occurred.

### Open Question 2 — 23/27 vs 23/28 calibration threshold

> "Proposed pass threshold for v2.3 is 23/27 or 23/28 (82-85%).
> Owner to confirm whether 82% or 85% is acceptable given the 4
> new hard anchors raise the bar."

**Remove.** Resolved — the gate section (Section 5, line 486)
already states 23/28 authoritatively. Directive-f §2.3
specified 23/28 (scaled from v2.2's 20/24). There is no open
question; the document contradicts itself only because the
Open Questions section wasn't updated.

### Open Question 3 — hero_range_percentile artifact

> "Section 2 notes that all 10 MW misses show ~~hero_range_percentile
> = 0.00 with visibly strong~~ holdings…"

**Remove.** ANOMALY-A resolved via Track 3.5 (HRP investigation
→ test-harness silent-default bug) and Stream A recovery (loader
path 3 confirmed). The hrp=0.00 claim itself is already struck
through in the body. The Open Question is redundant.

## Optional housekeeping (include if the diff is already open)

Line 567: "Analyzing the 10 MW misses and d-series spots." The
live model has 8 MW misses, not 10. Stream B.2 analysed the
original 10-hand set (pre-correction); the 10-hand analysis
drove the signature and is not wrong to cite historically.
Either leave as-is or change to "Analyzing the MW miss set."
Your call — this is not blocking.

## Commit message

```
Track 6 housekeeping: close three stale open questions in v2.3 scope

- Q1 (Track B fallback): Track 5 complete, question dead
- Q2 (23/27 vs 23/28): gate section authoritative at 23/28, remove
- Q3 (hero_range_percentile artifact): ANOMALY-A resolved, remove
```

## After this commit

Scope is approved. Builder can begin v2.3 hand generation once
owner signs off on the scope in its final form. No further
review cycles.

## What remains with owner

- Solver on remaining MW misses (non-gating, whenever)
- Gate 7 ship/iterate qualitative call (numeric case passes)
- Final v2.3 scope approval after this cleanup commit lands
