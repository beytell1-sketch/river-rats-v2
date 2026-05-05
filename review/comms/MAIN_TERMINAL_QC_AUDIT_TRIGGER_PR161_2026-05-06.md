---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #161 (12.5H-pre cross-seed analysis; H-FEAT median validated but volatile 60/40 bimodal) at commit e064edd — audit-now trigger
status: TRIGGER — fire now
---

# QC pre-merge audit on PR #161 — fire now

LEAD-PROGRAMMER opened PR #161 at commit `e064edd` (12.5H-pre cross-seed nut_flush_block importance analysis). 2 files: builder report + Path 2 fallback analysis script.

Headline empirical: H-FEAT VALIDATED at median (0.0268) but VOLATILE (60/40 bimodal across seeds); cap-non-binding byte-confirmed (12.5E-E ≡ 12.5G seed weights).

**Audit scope:** 4 audits per `MAIN_TERMINAL_PHASE125H_PRE_CROSSSEED_2026-05-05.md` (master `2c52e6b`, PR #160) §"QC stream — what you audit":

1. **Diff scope** — exactly 1-2 files (analysis-only); no `river-rats-core/` touches; no corpus/labels/prompt edits
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **Cross-seed methodology TC-X-CROSS-SEED-IMPORTANCE applied** — verify per-seed numbers reported across all 5 seeds for both 12.5E-E and 12.5G runs; verify median + std + min/max + chosen-seed values match expected (12.5E-E chosen=0.0268; 12.5G chosen=0.0054)
4. **Reproducibility** — if Path 2 used (extract_cross_seed_importance.py), verify deterministic re-run produces same importances

Post `REVIEW_QC_PHASE125H_PRE_CROSSSEED_*.md`. APPROVE or HOLD.

**Audit subject:** PR #161, branch `programmer/phase125h-pre-crossseed-2026-05-05`, commit `e064edd`.

## Sequencing on QC verdict

- APPROVE → orchestrator merges; dispatches 12.5H-A design (corpus expansion focus on E-DIST patterns, with seed-volatility caveat documented)
- HOLD → orchestrator routes findings to LEAD-PROGRAMMER for amendment

## What's blocked / what's queued

**Blocked:**
- PR #161 merge → on QC APPROVE
- 12.5H-A design → on PR #161 merge

**Queued:** all items from prior phases plus:
- Seed-volatility methodology investigation (60/40 bimodal): may want to fold into 12.5H-A design — N-seed-sweep-for-confidence requirement on future trainer runs

## References

- 12.5H-pre dispatch: master `2c52e6b` (PR #160)
- 12.5G: master `2135fc8` (PR #157)
- 12.5E-E: master `b51e525` (PR #152)
- Memory: `feedback_explicit_action_trigger.md` (this comm IS the trigger)

**Status: QC trigger posted. PR #161 ready for 4-audit sweep.**
