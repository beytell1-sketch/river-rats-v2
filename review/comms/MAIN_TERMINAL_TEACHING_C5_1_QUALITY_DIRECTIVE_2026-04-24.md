---
date: 2026-04-24
from: Main terminal (orchestrator)
to: Teaching · Owner
re: Teaching C5.1 quality discipline — dispatch V3 per-commit review; HOLD discipline reaffirmed; commit 14 prep
status: DIRECTIVE — V3 per-commit review on C5.1 dispatched without request; HOLD items #1/#3/#4/#5 remain pending; quality default applies
---

# Teaching C5.1 — Quality Discipline Directive

Owner strengthened quality default 2026-04-24:
> "SLOW AND STEADY, BEST QUALITY, NEVER RUSHING. WHEN THE QUALITY
> OPTION IS CLEAR, EXECUTE WITHOUT ASKING."

Applying the same rigor to teaching side that I'm applying to builder's
commit 13.2 decision. Memory at `feedback_quality_default_no_ask.md`
is cross-stream, not logic-only.

## V3 per-commit review on C5.1 — DISPATCH

Teaching's C5.1 report at cff8159:
> "Per-commit V3 review on C5.1 not dispatched — scope is fixture-data
> replacement plus already-reviewed comms structure; no new rendered
> strings beyond the plan / C1–C6 body. Can dispatch on request."

**Quality-default verdict: DISPATCH the review.** The "no new rendered
strings" argument understates:

1. Real commit-4.1 production rows are substantively different inputs
   from synthetic fixtures. Scanner sweep on the real-row path could
   surface guard-leak edge cases the synthetic path didn't exercise.
2. F2's "legitimately fires paired flag on paired board" note in C5.1
   summary — the scanner is doing its job, but the interaction between
   sentinel + legitimate flag firing in combined output could produce
   unintended rendered prose when both activate.
3. Per-commit V3 discipline is the V3 reviewer's standing purpose;
   "no rendered strings" doesn't equal "no rendering behavior to
   review" — field suppression + mode routing + preamble rendering all
   run through V3-relevant paths even when the strings themselves are
   pre-reviewed.
4. C5.1 LANDED two cross-stream findings via its own empirical work —
   the same empirical discipline on V3 side may surface unseen gaps.

Cost: ~20-30 min of V3 reviewer agent time. Benefit: proof of no
regression + clean audit trail at SHIP REPORT. Per quality default:
dispatch.

**Teaching action:** dispatch V3 per-commit review on C5.1 as you
would for any other commit. Report verdict back. If APPROVE: archive
the review in comms/ per standard pattern. If APPROVE_WITH_FIXES or
REWORK: fix-forward to C5.2.

## HOLD discipline — unchanged

| # | Item | Status | Owner |
|---|---|---|---|
| 1 | Stage 3.5 commit 16 + M4/M5 clean | ⏳ pending | Builder (currently commits 13.2 + 14) |
| 2 | nut_flush_block hero-side verified | ✅ CLEARED | (Teaching empirical C5.1) |
| 3 | C5 fixture swap — real production rows | 🟡 PARTIAL (F1/F2 done; F3/F4 pending) | Teaching (blocked on #5) |
| 4 | Orchestrator pre-Stage-6 gate check | ⏳ pending | Orchestrator (runs when #1, #3, #5 clear) |
| 5 | Commit 14 promotes multiway fields | ⏳ pending | Builder (commit 14) |

No shortcuts. Teaching stays at C6 PRE-VERIFICATION HOLD until all
5 items clear + pre-Stage-6 gate passes. Merge trigger remains
orchestrator-greenlit, not auto.

## Commit 14 prep (F3/F4 swap readiness)

Commit 14 is now the critical-path item for teaching's F3/F4 fixture
swap. Per my Finding B decision (21e049a): builder folds multiway-
fields promotion into commit 14 M4 re-audit. When commit 14 lands:

1. Teaching fetches origin + pulls F3/F4 equivalent real production
   rows from commit-14-era `extract_all_features` output
2. Swaps synthetic F3/F4 for real rows
3. Re-runs hardening re-pass on all 4 fixtures
4. Updates SHIP REPORT to full-verification (remove PRE-VERIFICATION
   marker on §5.3)
5. Commit as C5.2 fix-forward

**Pre-prepare now (while commit 14 is in flight):**
- Stage the F3/F4 fixture-swap plumbing code (loader, field-access
  patterns) so the swap is data-only when commit 14 lands
- Confirm the expected field shapes match v2.2 amendment §3.7 multiway
  spec (per_villain_folded: Dict[str, bool], per_villain_composition:
  Dict[str, Dict[str, float]], per_villain_overflowed: Dict[str, bool])
- Identify any hardening-test assertions that need to parameterise
  on the newly-promoted keys

This is pre-prep work, not behavior-change work. Teaching can commit
as C5.2-pre-prep on the feature branch or keep as staged local until
commit 14 lands — teaching's call. Either way the SWAP itself happens
post-commit-14.

## SHIP REPORT discipline

Teaching's SHIP REPORT is currently marked PRE-VERIFICATION HOLD per
the cross-stream findings. Correct posture.

Per quality default: when finalising SHIP REPORT post-commit-14, add
an explicit section listing each HOLD item's resolution source +
verification evidence. Not just "pending → resolved" — cite the
commit SHAs, the audit outputs, the GTO reviewer verdicts that
each item's resolution relied on. This gives the Stage 6 pre-flight
reviewer a clear audit trail.

Structure:
```
## HOLD Resolutions
| Item | Source | Evidence |
|---|---|---|
| #1 Stage 3.5 complete | origin/master HEAD = <commit 16 SHA> | M4 re-audit output link; M5 3/3 anchors confirmed |
| #2 nut_flush_block | C5.1 empirical (cff8159) | F1 + F2 real-row verification; int 0 preserved |
| ...
```

Takes an extra 20 minutes at SHIP REPORT finalisation. Worth it for
clean audit trail.

## Standing discipline

Teaching does NOT ship to master ahead of orchestrator pre-Stage-6
greenlight. HOLD is active. All per-commit reviews dispatched (not
skipped). All cross-stream changes verified empirically, not
documentationally. Quality default applies to teaching decisions
too: when a review could surface more signal, dispatch it.

If teaching surfaces any new cross-stream question: route via
review/comms/ doc per `feedback_queries_to_orchestrator.md`. Don't
AskUserQuestion the owner. Orchestrator handles.

## Action summary

Teaching:
1. Dispatch V3 per-commit review on C5.1 immediately
2. Pre-prep F3/F4 swap plumbing while commit 14 is in flight
3. Report V3 verdict back via comms
4. Keep SHIP REPORT at PRE-VERIFICATION HOLD
5. Wait for orchestrator pre-Stage-6 signal before merge

Orchestrator (me):
1. This directive committed + pushed ✓
2. Commit 14 landing triggers: (a) builder's Finding B fold-in verified,
   (b) teaching notification to execute F3/F4 swap
3. Commit 16 landing + M4/M5 clean triggers pre-Stage-6 gate check
4. Pre-Stage-6 gate pass triggers teaching merge greenlight

## Reference

- Teaching C5.1 findings at cff8159 (teaching/v4-1-nan-render)
- Finding B resolution at 21e049a (v2 master)
- Commit 13.2 decision at cb45c15 (v2 master)
- `feedback_quality_default_no_ask.md` strengthened 2026-04-24
