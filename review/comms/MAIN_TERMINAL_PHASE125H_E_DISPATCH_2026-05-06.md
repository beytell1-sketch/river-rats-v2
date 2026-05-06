---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-E — re-train v9 student on 694-hand corpus + queued cleanup; pilot 1-seed before 5-seed full
status: TRIGGER — fire now
---

# Phase 12.5H-E — re-train on 694-hand corpus

12.5H-D APPROVED at master `a554d71`. Combined 694-hand corpus is QC-cleared (G1-G4 + G5 cap-binding pre-flight + design_action verification all PASS). Builder re-runs trainer on combined corpus + labels.

Hyperparameters identical to 12.5E-E (cap=3.0 hybrid, pre-pad metadata-only, 5 seeds 0-4). No trainer code changes beyond paths + queued NIT cleanup.

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125h-e-retrain-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (default — implementation)

#### Step 1: merge corpus + labels at file level

```
data/corpus_combined_694_2026-05-XX.jsonl    = data/corpus_combined_604_2026-05-05.jsonl
                                              + data/corpus_revision_125h_situations_2026-05-06.jsonl
                                              + data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl

data/corpus_combined_694_labels_2026-05-XX.jsonl = data/corpus_combined_604_labels_2026-05-05.jsonl
                                                  + data/corpus_revision_125h_labels_2026-05-06.jsonl
```

Verify post-merge: 694 rows each; pilot_hand_id cardinality 694/694; join works.

#### Step 2: PILOT — 1-seed dry-run BEFORE 5-seed full (per `feedback_pilot_first_for_long_jobs.md`)

```
python3 river-rats-core/train_model_v9_student.py \
  --corpus data/corpus_combined_694_2026-05-XX.jsonl \
  --labels data/corpus_combined_694_labels_2026-05-XX.jsonl \
  --no-write-model \
  --seeds 0
```

Pilot gate criteria (all must hold):
- Trainer loads combined 694 corpus + labels without errors
- Pre-pad metadata-only mechanism succeeds (no R-1 fallback needed)
- Held-out classification report produced (5 classes, sane support)
- Reference-evaluator gate runs and produces solver-corrected score
- `_StudentInferenceLike45` invariant test passes

#### Step 3: FULL — 5-seed run (only on pilot APPROVE)

5 seeds 0-4, write-model. Produces `river-rats-core/models/gto_model_v9_student.json` if median ≥ 33; else artifact NOT promoted.

**Hyperparameters identical to 12.5E-E:**
- cap=3.0 hybrid weighting
- Pre-pad metadata-only (warm-start anchor `gto_model_v9_3way_v2.2.json`)
- 5 seeds; 80/20 stratified split; multi:softprob 5-class

#### Step 4: cleanup (3 queued NITs)

| Item | File | Fix |
|---|---|---|
| NIT-1 from PR #139 | `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | §3.T8 wording: clarify 36→22+14 history (post-12.5H, ride-along clarification — minor) |
| PILOT_595 cosmetic | `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (~line 315) | "TPTK + nut blocker" → "top-two-pair + nut blocker" |
| NIT-1 from PR #148 | `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (line 151) | Stale `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH` filename → `BUILDER_REPORT_PHASE125E_C_RESOLVED` |

#### Step 5: trainer report

Produce `review/comms/PROGRAMMER_REPORT_PHASE125H_E_TRAINER_2026-05-06.md` per blueprint §2.4 + Section F "12.5E vs 12.5H delta":

- Section A: training metadata (corpus 694; hyperparams unchanged)
- Section B: reference-evaluator results (5-seed litmus, chosen seed)
- Section C: Gate 2.3 feature importance — **NEW: cross-seed reporting required** per TC-X-CROSS-SEED-IMPORTANCE (median + std + min/max + % above 0.02 floor for `nut_flush_block`)
- Section D: provenance hashes
- Section F (NEW): 12.5E vs 12.5H delta — per-seed scores; per-class metrics; per-hand outcomes on the 5 stay-wrong hands (MW-17/25/40/45/47); newly-correct vs newly-broken count

**Per-hand failure direction classification** per `feedback_failure_direction_classification.md`.

### Stop conditions

- Combined corpus row count ≠ 694 → STOP
- pilot_hand_id cardinality ≠ 694 → STOP
- Pilot 1-seed gate fails → STOP per Step 2
- 5-seed median < 32 (regression vs 12.5E-E) → STOP, do NOT promote, route to orchestrator
- Cross-seed `nut_flush_block` median < 0.02 → STOP (H-FEAT validation regressed; route to orchestrator)
- `_StudentInferenceLike45` invariant test fails → STOP (mirror drift)
- >8 files in diff → STOP

### Deliverable scope (PR diff)

8 files maximum (or 7 if no model promotion):
1. `data/corpus_combined_694_*.jsonl` — NEW
2. `data/corpus_combined_694_labels_*.jsonl` — NEW
3. `river-rats-core/models/gto_model_v9_student.json` — NEW or UPDATE if median ≥ 33
4. `review/comms/PROGRAMMER_REPORT_PHASE125H_E_TRAINER_*.md` — NEW
5-7. 3 NIT cleanups (likely 1-2 file touches per NIT)
8. (room for one additional cleanup if needed)

If gate < 33 → 7 files (no model artifact); trainer report documents BLOCKED state.

### What you do NOT do

- Do NOT touch existing 604-row corpus or 90-row 12.5H corpus (locked)
- Do NOT change trainer hyperparameters (cap=3.0; 5 seeds; pre-pad metadata-only; warm-start anchor)
- Do NOT modify v3.x prompts
- Do NOT promote model unless median ≥ 33 (12.5H-F gate decides)
- Do NOT improvise R-2 mitigations

## QC stream — what you audit (when 12.5H-E PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

5 audits:
1. Diff scope — exactly 7-8 files
2. Citation existence
3. Combined corpus integrity (694 rows + cardinality)
4. NEW: Trainer hyperparameter immutability — only NIT cleanup diffs allowed
5. NEW: Cleanup completeness — verify all 3 NITs applied per dispatch §"Step 4 cleanup"

Post `REVIEW_QC_PHASE125H_E_RETRAIN_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER pre-flight + Step 1 merge corpus + labels
2. Step 2 pilot 1-seed dry-run → gate
3. Step 3 5-seed full run
4. Step 4 cleanup
5. Step 5 trainer report (with cross-seed importance)
6. PR opens
7. Orchestrator posts QC audit-now trigger
8. Standalone QC audit
9. On QC APPROVE: orchestrator merges; dispatches 12.5H-F gate evaluation

## What's blocked / what's queued

**Blocked:**
- 12.5H-E PR opens → on builder pilot APPROVE + 5-seed run + report + cleanup
- 12.5H-F dispatch → on 12.5H-E PR merge

**Queued:**
- All items per prior queues
- 12.5G' or feature-engineering escalation (only if 12.5H-F gate fails on MW-17 / E-FEATURE residuals)

## References

- 12.5H-D APPROVE: master `a554d71` (PR #186)
- 12.5H-C LABELS FINAL: master `690ca8f` (PR #184)
- 12.5H-C labelling round merged: master `90e17dc` (PR #181)
- 12.5C blueprint (trainer module): master `1e4e47e` (PR #122)
- 12.5E-E precedent: master `b51e525` (PR #152)
- ml-architect 12.5D' Q4 H-FEAT prediction: `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_pilot_first_for_long_jobs.md` (1-seed pilot + tier-up sub-rule), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_failure_direction_classification.md`

**Status: 12.5H-E TRIGGER posted. LEAD-PROGRAMMER pilot 1-seed → 5-seed full → cleanup → report → PR. Median ≥ 33 = success path; < 33 = STOP, route to orchestrator.**
