---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #261 + PR #263 merged (QC PASS; 30th solo cycle); variance-bound finding ratified at Lever A; dispatch 12.5K-B Lever B (hyperparameter sweep with CV-driven discipline)
status: DIRECTIVE — merges PR #261 + PR #263; fires LEAD-PROGRAMMER on 12.5K-B — fire now
---

# PR #261 + PR #263 merge + 12.5K-B Lever B (hyperparameter sweep) dispatch

QC verdict on PR #261 (`REVIEW_QC_PHASE125K_A_MORE_SEEDS_2026-05-06.md` on `qc/pr261-125ka-review-2026-05-06`, PR #263): **PASS**. 30th solo cycle expected.

**Empirical conclusion (Lever A complete):** 20-seed mean **33.10/40 ± 0.30 solver-corrected** vs baseline 34/40. Mean + 1-σ = 33.40 < 34 → not at-or-above baseline within 1-σ. Variance hypothesis ruled out. The model's true expected accuracy at 788-corpus 61-surface + existing config is ~33.10/40. **Per outcome matrix (Lever A § "Expected outcome (3 cases)"): variance-bound → proceed to Lever B.**

## LEAD-PROGRAMMER — Step: 12.5K-B Lever B (hyperparameter sweep) — fire on this comm merge

Per plan `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` §4 "Lever B — hyperparameter exploration".

Branch: `programmer/phase125k-b-hyperparameter-sweep-2026-05-06`. Base: master post-this-comm-merge.

### Scope — CV-driven hyperparameter sweep on 788-corpus 61-surface

#### Cross-validation discipline (binding per dispatch + plan §4)

The sweep uses **held-out cross-validation folds INTERNAL to the 788-corpus**, NOT the 40-hand reference set. Reference set is held out for final evaluation only. Per `feedback_solver_vs_expert_labels.md`: model performance is observed via reference set, NEVER trained against.

Suggested CV setup (builder discretion within these bounds):
- 5-fold stratified CV (stratified by action class) on 788-corpus
- Per fold: train on 4 folds (~630 hands) + evaluate on 1 fold (~158 hands)
- Per config: 5 folds × 1 seed = 5 measurements; aggregate mean + std
- Configs evaluated by mean fold accuracy (or weighted-confidence accuracy if more informative)

#### Hyperparameter grid (architect-hat builder selects within these axes)

Per plan §4 expected exploration axes:
- `n_estimators`: e.g., {400, 600, 800 [current], 1200, 1600}
- `max_depth`: e.g., {3, 4, 5 [current], 6, 7}
- `learning_rate`: e.g., {0.02, 0.03, 0.05 [current], 0.08, 0.10}
- `min_child_weight`: e.g., {3, 5 [current], 7, 10}
- `subsample`: e.g., {0.7, 0.8 [current], 0.9}
- `colsample_bytree`: e.g., {0.65, 0.75 [current], 0.85}
- `reg_alpha`: e.g., {0.05, 0.1 [current], 0.3}
- `reg_lambda`: e.g., {0.5, 1.0 [current], 2.0}

Full grid would be 5×5×5×4×3×3×3×3 = 16,200 configs — too large. Builder uses a **structured sweep** (e.g., random search 50-200 configs OR sequential one-axis-at-a-time with held-fixed defaults) per architect-hat judgment. Document the sweep strategy in builder report.

**Constraint**: warm-start anchor stays `gto_model_v9_3way_v2.2.json` (no pre-warm-start changes; testing post-warm-start config impact only).

#### Pilot-first 2-3 configs gate (binding per `feedback_pilot_first_for_long_jobs.md`)

Per plan §4 pilot-first scope. Run 2-3 representative configs from the planned sweep first to validate:

| Pilot gate criterion | Continue if... | Off-ramp if... |
|---|---|---|
| Sweep infrastructure works | All 2-3 pilot configs train + 5-fold CV evaluate without errors | Any pilot config crashes / schema mismatch / infrastructure failure → STOP, route to orchestrator |
| Per-config CV mean produces meaningful spread | At least 1 of the 2-3 pilot configs differs from baseline by >0.5 hand on CV mean | All 2-3 pilot configs show CV mean within 0.2 hand of baseline → REPORT (not STOP); orchestrator decides whether sweep is worth scaling (probably variance-bound at hyperparameter level too) |
| Resource utilization | Per-config wall clock <30 min (allows sweep to fit in budget) | Per-config wall clock >60 min → REPORT; orchestrator decides reduced grid |

If gate PASSES → scale to full sweep (e.g., 50-100 more configs).
If gate REPORTS but doesn't STOP → orchestrator escalation; potentially off-ramp Lever B early.

#### Best-config selection + reference-set evaluation

After full sweep:
1. Select top 3-5 configs by CV mean (with std as tiebreaker; prefer lower std)
2. Train each top config with 5 seeds (mirrors PR #253 + PR #261 protocol)
3. Evaluate each top config × 5 seeds on reference set
4. Build comparison: best-config 5-seed mean vs Lever A 20-seed mean (33.10/40 ± 0.30) vs baseline (34/40)

#### Outcome matrix (Lever B)

| Best-config 5-seed mean | Action |
|---|---|
| **Mean ≥ 34.0/40 within 1-σ** | PROMOTE; Lever B succeeds; off-ramp Lever C; dispatch 12.5L gate eval |
| **Mean in [33.20, 34.0) (improvement but not above baseline)** | REPORT; orchestrator decides: ship as best-effort improvement OR proceed to Lever C for further lift |
| **Mean ≈ 33.10/40 ± 0.30 (no improvement vs Lever A)** | Hyperparameter-bound finding; conclude existing config near-optimal at 788-corpus 61-surface; proceed to Lever C (augmented data) |
| **Mean < 33.0/40 (worse than Lever A)** | Negative; surface for orchestrator; possible bug or sweep error |

### What you do NOT do

- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source EXCEPT trainer hyperparameters/sweep infrastructure (per CLAUDE.md provenance: any new sweep script lives in `river-rats-core/`)
- Do NOT modify BATCH2 reference
- Do NOT modify the 788-corpus or labels
- Do NOT change warm-start anchor
- Do NOT train against reference set (CV folds are INTERNAL to 788-corpus; reference set is final evaluation only)
- Do NOT skip the 2-3 config pilot gate (binding)
- Do NOT auto-promote; orchestrator-scope decision per outcome matrix
- Do NOT use solver-as-labels for any sweep evaluation

### Cost / time

~$0 LLM; ~10-20 hours wall clock total per plan §4. Pilot 2-3 configs: ~30-90 min. Full sweep: ~5-15 hours depending on grid size. Best-config 5-seed evaluation: ~30 min.

If wall clock will exceed 30 hours → STOP per dispatch §"Stop conditions" budget cap; route to orchestrator.

### Deliverable scope

Expected files in PR diff:
1. `river-rats-core/sweep_125k_b_hyperparameter.py` (new sweep orchestration script with provenance docstring)
2. `data/sweep_125k_b_results_2026-05-06.jsonl` (per-config CV results across the full sweep)
3. `river-rats-core/models/125k_b/best_config_*.json` (top 3-5 configs × 5 seeds = 15-25 model artifacts)
4. `data/inference_125k_b_reference_predictions_2026-05-06.jsonl` (reference-set evaluation of top configs)
5. `review/comms/BUILDER_REPORT_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md`

### Builder report sections (mandatory)

- §"Sweep strategy" — random search / sequential / etc.; grid size + axes
- §"Pilot 2-3 config gate" — per-pilot CV mean + gate decision
- §"Full sweep results" — per-config CV mean / std / wall clock
- §"Top configs selected" — top 3-5 by CV mean with selection rationale
- §"Reference-set evaluation of top configs" — per-config 5-seed × 40-hand predictions
- §"Best-config aggregate" — best-config 5-seed mean / std vs Lever A 20-seed mean vs baseline
- §"Per-stay-wrong subset detail" — does best config flip any stay-wrong?
- §"Outcome matrix conclusion" — which case from §"Outcome matrix" above; orchestrator-scope decision route
- §"Provenance" — top configs' commit-hash links
- §"Stop conditions" — full record

## QC stream — what you audit (when 12.5K-B PR opens)

Standalone audit, ~20-30 min, 9-item training-output sweep scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — sweep script + sweep results + top configs + ref-set eval + report. NO touch to v3.x / BATCH2 / corpora / unrelated source.
2. **Provenance integrity** — top configs each have commit-hash docstring link.
3. **Pilot 2-3 config gate executed** — gate decision before full sweep scaling.
4. **CV discipline correct** — 5-fold stratified on 788-corpus; reference set NOT used in CV.
5. **No reference-set training** — verify no training cycles target reference set; reference set is held out for final eval.
6. **No solver-as-labels** — sweep doesn't cite solver outputs as label authority.
7. **Best-config selection correct** — top-N selection by CV mean with std tiebreaker.
8. **TC-X-OWNER-SCOPE-DISCIPLINE** — BATCH2 unchanged; warm-start anchor unchanged; corpus unchanged.
9. **TC-X-DISPATCH-COMPLIANCE (10th formal exercise)** — pilot-first; structured sweep (not exhaustive); orchestrator-scope outcome decision preserved.

## Sequencing — what fires after 12.5K-B merges (per outcome)

Per Lever B outcome matrix:
1. **PROMOTE outcome (≥34.0 in 1-σ)** → 12.5L gate eval dispatch (Lever C off-ramped)
2. **Improvement but not promote (33.20-34.0)** → orchestrator escalation; ship best-effort or proceed to Lever C
3. **No improvement / hyperparameter-bound** → 12.5K-C Lever C (augmented data) dispatch
4. **Negative** → orchestrator escalation; possible bug

## What's blocked / what's queued

**Cleared by this comm:**
- PR #261 merge (Builder Lever A 20-seed; variance-bound)
- PR #263 merge (QC verdict record)
- 12.5K-B Lever B dispatch fires
- Variance hypothesis ruled out at Lever A

**Newly queued (after 12.5K-B merges, conditional on outcome):**
- PROMOTE → 12.5L gate eval
- Improvement → orchestrator escalation
- Hyperparameter-bound → 12.5K-C Lever C
- Negative → orchestrator escalation

**Still queued (later):**
- 12.5K-C (if reached)
- 12.5L gate evaluation

## References

- PR #261 (Builder Lever A; 20-seed 33.10/40 ± 0.30): branch `programmer/phase125k-a-more-seeds-2026-05-06`
- PR #263 (QC PASS verdict): branch `qc/pr261-125ka-review-2026-05-06`
- PR #262 (QC trigger): master `8906d99`
- PR #260 (orchestrator: 12.5K-A dispatch): master `44089bb`
- 12.5K master plan §4 (Lever B spec + outcome matrix): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- v9-3way-v2.2 baseline: 34/40 solver-corrected
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md` (2-3 config pilot gate at Lever B), `feedback_solver_vs_expert_labels.md` (no reference-set training; CV folds INTERNAL only)

**Status: PR #261 + PR #263 cleared for merge. Variance hypothesis ruled out. LEAD-PROGRAMMER fires 12.5K-B Lever B (hyperparameter sweep with CV-driven discipline; 2-3 config pilot gate) on this comm merge. ~$0 LLM; ~10-20h wall clock to PR open.**
