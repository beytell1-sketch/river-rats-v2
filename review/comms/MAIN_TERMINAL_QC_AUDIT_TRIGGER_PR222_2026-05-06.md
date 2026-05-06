---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #222 — 12.5I-D corpus assemble (694 + 94 = 788; 61-surface uniform) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #222

PR #222: `programmer/phase125i-d-corpus-assemble-2026-05-06`. Builder report at `review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md` (in branch). Corpus output: `data/corpus_combined_788_2026-05-06.jsonl` + labels variant. Per dispatch `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` (master `680f51d`, PR #221).

## Audit scope (7 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 3 files (+ optional script):
   - `data/corpus_combined_788_2026-05-06.jsonl` (788 rows)
   - `data/corpus_combined_788_labels_2026-05-06.jsonl` (788 rows; consensus action + confidence)
   - `review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md`
   - Optionally a small `scripts/assemble_*.py` if needed (per `assemble_v23_*.py` precedent)
   
   Verify NOT touched: v3.x prompts, BATCH2 reference files, river-rats-core/ source, training-data files outside the new combined corpus.

2. **Row count integrity** — 694 + 94 = 788 exact; verify no duplicate ref_ids between sources; confirm preservation of 694 ordering followed by 94 in PILOT_695..PILOT_788 order.

3. **Schema match** — column names + dtypes consistent across 694-source rows and 94-revision rows. Per `feedback_attention_flags_when_features_change.md`: 61-surface uniform across all 788 rows.

4. **Feature backfill correctness** — spot-check 5 random pre-existing 694-corpus rows: do the 2 new Step-18 features (`nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`) compute correctly from `feat_dict` + board state? (Compare against `feature_extractor.compute_step18_features()` if such a helper exists; otherwise check value plausibility against expected ranges.)

5. **Distribution table correctness** — match builder report's per-template + per-action distribution table against actual jsonl distributions (sampling-spot-check sufficient).

6. **Reference correctness (post-PR #218)** — verify MW-25 in `BATCH2_8_RANGE_ANALYSIS.md` still reads CHECK HIGH (no regression from PR #218 effect).

7. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x prompts, no BATCH2 edits, no river-rats-core/ source touched in this PR. Reference-set + memory + prompts untouched.

## QC routing

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit. Expected duration: ~10-15 min (medium scope; spot-check feature backfill is the longest item).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md` on `qc/pr222-corpus-assemble-review-2026-05-06`. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #222 merge → on QC PASS (no Opus tier-up needed; mechanical corpus assemble, not labelling)
- 12.5I-MW40-VERIFICATION-A design dispatch → on PR #222 merge
- 12.5J-D-pre test-guard deflake dispatch → on PR #222 merge (sequential after MW-40-A)
- 12.5K combined re-train design → on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship

## What you do NOT do

- Do NOT make GTO judgments on corpus labels (that was PR #213 audit + Opus tier-up scope)
- Do NOT modify any file (review-only)
- Do NOT recommend reference-set changes (orchestrator-scope)
- Do NOT run training or inference

## Apology for delayed dispatch

PR #222 opened at 19:18 SAST; this trigger fires at 19:23 SAST = 5 min idle gap. Cause: orchestrator self-paced wakeup was scheduled for 19:37 SAST (25-min cadence for "12.5I-D ~25-30 min builder time"); builder finished in ~10 min (faster than estimated). Tightening pacing on subsequent dispatches; considering Monitor on PR-open as a wake signal in addition to ScheduleWakeup.

## References

- 12.5I-D dispatch: `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` (master `680f51d`, PR #221)
- PR #213 (12.5I-C source 94-row labels): master `994ae67`
- 12.5H-D corpus assemble precedent: `data/corpus_combined_604_*` → `data/corpus_combined_694_*`
- BATCH2 MW-25 (post-graduation, CHECK HIGH active): master `e01b296` (PR #218)
- Memory: `feedback_attention_flags_when_features_change.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_explicit_action_trigger.md`

**Status: QC stream — fire now on PR #222. Standalone audit, pre-merge, 7-item scope. ~10-15 min.**
