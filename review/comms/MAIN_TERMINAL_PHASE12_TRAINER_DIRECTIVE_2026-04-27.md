---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · ml-architect · QC stream · gto-expert (eval-only) · Owner
re: Phase 12 trainer pipeline — XGBoost v9 student warm-start on 494-hand corpus + 2470 labels
status: DIRECTIVE — milestone PR; full review chain; cost minimal (XGBoost CPU, no API)
---

# Phase 12 trainer directive

## Context

Master `78bad39`: 494-hand corpus + 2470 v3.2 labels merged. v9 baseline at `models/gto_model_v9_baseline_45feat.json` (per Phase 2 R2 schema verify). Pipeline ready for student warm-start training.

## Authorization

Per `feedback_listen_to_orchestrator_always.md`: orchestrator-named-author = sufficient. Cost ~$0 (XGBoost CPU; no API calls); quality-first default per `feedback_quality_default_no_ask.md`.

## Scope

Train **v9 student model** (59-feature XGBoost multi:softprob 5-class) warm-started from v9 baseline (45-feature) on the 494-hand corpus + 2470 consensus labels.

## Inputs

- **Corpus**: `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records, 59-feature schema)
- **Labels**: `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (consensus_action keyed by ref_id, 2470 individual labels preserved)
- **Baseline**: `river-rats-core/models/gto_model_v9_baseline_45feat.json` (warm-start init)
- **Feature schema**: 59 features per `feature_extractor.py` FEATURE_COLUMNS (45 base + 14 v2.4 P1 blockers)

## Operational sequence

### Step 1 — feature delta resolution (R2 verification carryforward)

Per Phase 2 directive R2: confirm 14 new features (59-45=14) are appended to existing 45 base — no schema reordering. Use `scripts/verify_feature_schema_compatibility.py` (already on master) to validate the corpus contract.

### Step 2 — label join

Join corpus + labels on `ref_id`. Output flat training matrix:
- X: 494 × 59 feature matrix
- y: 494 × 1 consensus_action labels (5 classes: CHECK / BET / FOLD / CALL / RAISE)
- metadata: `consensus_confidence` per row (for sample weighting in step 3)

Verify 100% join (no orphans).

### Step 3 — train

Train script: `river-rats-core/train_model.py` (already in core). Invocation:
```
python3 river-rats-core/train_model.py \
  --corpus data/corpus_revision_500_hand_2026-04-27.jsonl \
  --labels data/corpus_revision_500_hand_labels_2026-04-27.jsonl \
  --warm-start river-rats-core/models/gto_model_v9_baseline_45feat.json \
  --output river-rats-core/models/gto_model_v9_3way_59feat_2026-04-27.json \
  --seeds 0,1,2,3,4 \
  --confidence-weighting 1
```

(Verify exact arg names against `train_model.py` argparse before running. If absent, do NOT improvise — report BLOCKED and surface what the script actually accepts.)

**Hyperparameters**: use existing v9 baseline hyperparameters as defaults; warm-start preserves tree structure. If train_model.py doesn't support warm-start at this 45→59 boundary, builder reports BLOCKED — Phase 12.5 directive will resolve.

**Multi-seed**: 5 seeds (0-4) for variance estimation. Output: 5 model files; trainer report computes per-seed accuracy + std-dev.

**Confidence weighting**: per-sample weight = `consensus_confidence` (so unanimous labels weighted higher than 3/5 plurality). Optional flag; if absent in train_model.py, default to uniform weighting.

### Step 4 — held-out evaluation

Per ship-gate plan (CLAUDE.md): 5 litmus tests + held-out + multi-seed validation.

- **Litmus tests**: use existing reference set at `training-data/3way_reference_40hand.jsonl` (or whatever the canonical reference set is — verify path before running)
- **Held-out**: split 80/20 train/eval at training time (stratified by category to avoid concentrating minority cats in eval — per ml-architect round 7 recommendation)
- **Multi-seed**: report mean ± std accuracy across seeds 0-4

### Step 5 — final report

`review/comms/PROGRAMMER_REPORT_PHASE12_TRAINER_2026-04-27.md`. Cover:
- Train accuracy (per seed + mean ± std)
- Held-out accuracy (per seed + mean ± std)
- 5 litmus test pass/fail
- Per-class precision/recall (esp. RAISE — it's the rarest class at 5.9%)
- Feature importance from one model (top 20)
- Comparison to v9 baseline 45-feat on the same held-out (warm-start gain measurement)

## Round 12 review chain (milestone)

Per memory `feedback_qc_required_before_approval.md` milestone scope:
- **ml-architect**: training methodology, hyperparameters, warm-start correctness, eval methodology (stratified split, multi-seed variance)
- **gto-expert**: spot-check 10 model predictions on held-out hands for poker realism (does the model produce sensible actions?)
- **QC**: paired V-Implementation-Spec-Match (training pipeline matches directive) + V-Integration-Trace (model loads + inferences cleanly via existing `gto_model.py` infrastructure)

## PR

- Branch: `programmer/v9-3way-59feat-trainer-2026-04-27`
- Files: trained model artefacts (5 seeds) + final report + any new training script changes
- Title: `Builder Phase 12: v9 student warm-start trainer (59-feat, 5 seeds, 494 hands)`

## Failure handling

- train_model.py CLI mismatch / missing warm-start support: STOP, report BLOCKED — orchestrator dispatches small Phase 12.5 fix
- Held-out accuracy < v9 baseline (warm-start regression): STOP, report; orchestrator decides accept-or-iterate
- Litmus test fail: STOP, report which test; orchestrator + gto-expert evaluate

## What this directive does NOT cover

- Tier 1 calibration manifest 33→45 (parallel separate workstream)
- Held-out testset v1.0 expansion (separate workstream)
- Model deployment / shipping (post-Phase-12 ship gate)

## References

- Master HEAD: `78bad39`
- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl`
- Labels: `data/corpus_revision_500_hand_labels_2026-04-27.jsonl`
- v9 baseline: `river-rats-core/models/gto_model_v9_baseline_45feat.json`
- Round 7 ml-architect on stratified split: `review/comms/REVIEW_ML_ARCHITECT_PR80_PHASE6_2026-04-27.md`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_verify_source_not_plan.md` (verify train_model.py CLI before running)

**Status: PHASE 12 DIRECTIVE OPEN. Builder authors training run + report; round 12 review chain (ml + gto + QC); merge → ship-gate evaluation.**
