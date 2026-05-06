---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #188 (12.5H-E re-train; median 32/40 unchanged; H-FEAT primary +85%; model NOT promoted) at commit 5d9c258 — audit-now trigger
status: TRIGGER — fire now
---

# QC pre-merge audit on PR #188 — fire now

LEAD-PROGRAMMER opened PR #188 at commit `5d9c258` (12.5H-E re-train deliverable). 5 files: combined 694-hand corpus + labels + trainer report + 2 NIT cleanups (no model artifact per median <33; trainer module untouched).

Headline (from PR title):
- Median 32/40 unchanged from 12.5E-E (corpus expansion +90 hands didn't move gate)
- H-FEAT primary +85% (presumably `nut_flush_block` cross-seed importance jumped — design's secondary gate ≥0.04 likely cleared)
- Model NOT promoted

**Audit scope:** 5 audits per `MAIN_TERMINAL_PHASE125H_E_DISPATCH_2026-05-06.md` (master `bacce1d`, PR #187) §"QC stream — what you audit":

1. **Diff scope** — exactly 5-7 files; no model artifact (correctly absent per median <33); only NIT-cleanup edits to existing review/comms files
2. **Citation existence** — every file:line in trainer report exists at master HEAD
3. **Combined corpus integrity** — 694 rows; `pilot_hand_id` cardinality 694/694
4. **NEW: Trainer hyperparameter immutability** — `train_model_v9_student.py` byte-identical to master HEAD `a554d71` (only NIT cleanup diffs allowed; if any code change beyond NIT, HOLD)
5. **NEW: Cleanup completeness** — verify all 3 NITs applied per dispatch §"Step 4 cleanup" (PLAN §3.T8 wording, PILOT_595 cosmetic, BUILDER_REPORT stale filename)

**Bonus:** verify cross-seed `nut_flush_block` reporting per TC-X-CROSS-SEED-IMPORTANCE (median + std + min/max + % above 0.02 floor) — required by 12.5H-E dispatch §"Section C".

**Audit subject:** PR #188, branch `programmer/phase125h-e-retrain-2026-05-06`, commit `5d9c258`.

Post `REVIEW_QC_PHASE125H_E_RETRAIN_*.md`. APPROVE or HOLD.

## Sequencing on QC verdict

- APPROVE → orchestrator merges; **dispatches 12.5H-F gate evaluation** (synthesis + owner WHAT decision; secondary gate cross-seed `nut_flush_block` ≥0.04 status will inform)
- HOLD → route to LEAD-PROGRAMMER for amendment

## Note on outcome

Median 32 unchanged is structurally significant: B-then-C compound's step 2 (corpus expansion) didn't close the gap to ≥33 either. H-FEAT +85% confirms the feature is becoming load-bearing but didn't translate to gate-score improvement. 12.5H-F synthesis will surface owner WHAT decision (promote / abandon / feature engineering escalation per Path C of original 12.5E-F decision matrix).

## What's blocked / what's queued

**Blocked:**
- PR #188 merge → on QC APPROVE
- 12.5H-F dispatch → on PR #188 merge

**Queued:** all items per prior queues

## References

- 12.5H-E dispatch: master `bacce1d` (PR #187)
- 12.5H-D APPROVE: master `a554d71` (PR #186)
- 12.5H-C LABELS FINAL: master `690ca8f` (PR #184)
- 12.5E-E precedent (12.5E delta target): master `b51e525` (PR #152)
- Memory: `feedback_explicit_action_trigger.md`

**Status: QC trigger posted. PR #188 ready for 5-audit sweep.**
