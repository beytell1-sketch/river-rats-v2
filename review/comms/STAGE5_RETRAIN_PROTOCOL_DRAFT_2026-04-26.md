---
date: 2026-04-26
from: Main terminal (orchestrator) — DRAFT
to: Owner · ML-architect (when commissioned) · Logic builder
re: Stage 5 multi-seed retrain protocol — concrete spec extending the locked Stage 4 plan
status: DRAFT v0.1 — orchestrator structural framework; awaits ML-architect + owner review for ML-specific judgment calls (hyperparameter selection, seed strategy, accuracy-spread thresholds)
---

# Stage 5 Multi-Seed Retrain Protocol — DRAFT v0.1

## Purpose

Stage 5 takes the Stage 4 relabelled corpus and trains v2.4. Per the
locked Stage 4 plan (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
commit `ee3d9f5`), Stage 5 uses **3-seed multi-seed training** with
agreement gates to distinguish "data noise" from "model capacity"
failure modes. This draft fleshes out the concrete protocol.

## Inputs from Stage 4

Pilot or full Stage 4 produces:

- **Final consensus labels** per hand from the 3-protocol × 5-agent
  cross-protocol process (15 labels per hand pre-adjudication; one
  consensus label post-adjudication, or DROP for ambiguous hands)
- **Final attention flag set** per hand (54 + 4 = 58 binary attn_*
  flags using v2.4 P1 + Exp 3 auxiliary protocol)
- **Hand metadata** per hand: features, situation, source (reference
  / calibration / pilot / generated), confidence band (HIGH /
  MEDIUM / LOW from adjudication)
- **Drop list** of hands marked AMBIGUOUS during Stage 4

Total expected corpus: ~600 hands minus DROPs. Estimated DROPs: 5-15%
of corpus per Pass 1 baseline.

## 3-seed retrain mechanics

### Hyperparameters (locked across seeds)

[**ML-ARCHITECT REVIEW NEEDED:** the locked v2.2 hyperparameters
should be the starting point; v2.4 may need tuning given +4 features.
ML-architect to confirm or propose revisions before pilot.]

Provisional locked hyperparameters (from v2.2 baseline, subject to
ML-architect review):

```python
{
  'objective': 'multi:softmax',
  'num_class': 5,                    # FOLD/CHECK/CALL/BET/RAISE
  'eta': 0.05,                       # learning rate
  'max_depth': 6,
  'min_child_weight': 5,
  'subsample': 0.8,
  'colsample_bytree': 0.8,
  'lambda': 1.0,                     # L2
  'alpha': 0.0,                      # L1
  'num_boost_round': 500,
  'early_stopping_rounds': 30,
  'eval_metric': ['mlogloss', 'merror']
}
```

### Seed selection

Three random seeds: `42`, `2026`, `1729`. Each seed produces an
independent model run.

[**ML-ARCHITECT REVIEW NEEDED:** seed selection rationale —
arbitrary numbers vs deliberately-chosen. Some practitioners pick
seeds spanning known-stable / known-unstable regimes. Owner /
ml-architect to decide.]

### Training data partitioning (identical across seeds)

- **Train set:** ~85% of corpus (Stage 4 consensus + HIGH/MEDIUM
  confidence)
- **CV set:** ~15% (held back from train for early stopping)
- **Reference set:** the existing 40-hand reference set, NOT in
  training data
- **Held-out test set:** new 50-hand held-out set per Stage 6 spec
  (`STAGE6_HOLDOUT_TESTSET_DRAFT_*` — to be authored), NOT in
  training data
- **Calibration set:** existing 24-hand calibration set, NOT in
  training data

Same train/CV split across all three seeds (same hands; different
seed only changes model initialisation + sampling).

[**ML-ARCHITECT REVIEW NEEDED:** alternative — DIFFERENT train/CV
splits per seed (each seed gets its own random partition). Trades
interpretability of seed-comparison vs robustness against split-
specific noise. Owner / ml-architect to decide.]

## Agreement gates

After 3 models trained (one per seed):

### Gate 1 — Reference-set accuracy spread ≤ ±2pp

Each model evaluated on the 40-hand reference set (solver-corrected
labels from `feedback_solver_findings.md` + `reference_corrections.md`).

Compute accuracy per seed: e.g. seed-42 = 84.5%, seed-2026 = 83.0%,
seed-1729 = 85.0%. Spread: 85.0 − 83.0 = 2.0pp.

| Spread | Verdict | Action |
|---|---|---|
| ≤ ±2pp | PASS | Proceed to Gate 2 |
| ±2.1pp – ±3.0pp | MARGINAL | Investigate seed-specific divergence; report findings; owner-gated decision |
| > ±3.0pp | FAIL | Data is noisy or model is unstable. Retrain blocked. Investigate before declaring v2.4. |

[**ML-ARCHITECT REVIEW NEEDED:** ±2pp threshold — empirically
calibrated against Pass 1 results? Or theoretically derived from
sample size? Owner / ml-architect to validate.]

### Gate 2 — Top-10 feature-importance Spearman ≥ 0.8 across seeds

Each model produces a feature-importance ranking (XGBoost gain or
shap-mean per feature). Compute pairwise Spearman correlation on the
top-10 features across the 3 seeds: seed-42 vs seed-2026, seed-2026
vs seed-1729, seed-42 vs seed-1729.

| All 3 pairwise Spearman | Verdict | Action |
|---|---|---|
| All ≥ 0.8 | PASS | Proceed to Gate 3 |
| 1+ pairwise ∈ [0.6, 0.8) | MARGINAL | Investigate which features differ; owner-gated decision |
| 1+ pairwise < 0.6 | FAIL | Data is structurally noisy on which features matter. Flag for v2.5 feature engineering before retraining. |

[**ML-ARCHITECT REVIEW NEEDED:** Spearman ≥ 0.8 threshold +
justification. Top-10 vs top-20 — owner / ml-architect to decide.]

### Gate 3 — Calibration exam pass

Each model takes the 24-hand calibration exam (independent grading
against answer key). Required: 20/24 + all 3 GTO-reversal hands
(MW-30, MW-33, MW-50 at solver-corrected labels) correct.

| All 3 seeds pass | Verdict |
|---|---|
| YES | PASS — proceed to seed selection |
| Some seeds pass | MARGINAL — investigate; owner-gated decision |
| No seeds pass | FAIL — Stage 4 labelling regression; rollback to Stage 4 |

## Seed selection (post-gates)

If Gates 1-3 all PASS: pick the **median seed** by reference-set
accuracy. NOT the best.

**Why median, not best:** "best of 3 seeds" is selection bias on the
same data — picks the seed that happens to fit reference-set noise
the closest. Median is the unbiased estimator.

[**ML-ARCHITECT REVIEW NEEDED:** alternative — average ensemble of
all 3 seeds. Trade-off: ensemble is harder to interpret + harder to
deploy + slower inference. Median single-seed is simpler. Owner /
ml-architect to decide if ensemble is worth the complexity.]

The chosen seed is **v2.4 candidate**. Submit to Stage 6 ship gate.

## Reporting

Stage 5 produces `STAGE5_RETRAIN_REPORT_<date>.md` with:

- All 3 seeds' hyperparameters (locked, identical)
- All 3 seeds' training curves (train/CV loss + accuracy)
- All 3 seeds' final reference-set accuracy + per-shape-category
  breakdown
- Top-10 feature importance ranking per seed + pairwise Spearman
- Calibration exam result per seed (24-hand grades)
- Gate 1/2/3 outcomes
- Median-seed selection rationale
- v2.4 candidate model artifact pointer

Provenance discipline: report records its authoring agent (whoever
ran the training script) + reviewer agent (independent ML-architect
or general-purpose-with-persona-fallback) + the Stage 4 corpus SHA
the retrain was done against.

## Rollback

If Gate 1, 2, or 3 FAIL:

- **Gate 1 FAIL** (accuracy spread > ±3pp): rollback target =
  Stage 4 consensus labels. Investigate which hands drive the
  spread (probably high-DROP-rate or LOW-confidence hands inflating
  noise). Re-pilot on those if necessary.
- **Gate 2 FAIL** (feature importance Spearman < 0.6): rollback
  target = v2.4 P1 feature set. Investigate whether new blocker
  features destabilise the importance ranking. Drop unstable
  features if they don't add accuracy.
- **Gate 3 FAIL** (calibration regression): rollback target =
  Stage 4 labelling. Investigate whether Stage 4 introduced
  systematic GTO-reversal bias (the 3 reversal hands were the most
  carefully-curated; failing them means labellers diverged from
  solver truth).

Rollback rules per `feedback_quality_default_no_ask.md`: take the
slow/quality path. Don't ship v2.4 with marginal gates.

[**ML-ARCHITECT REVIEW NEEDED:** rollback investigation procedures
need ml-architect rigour. Owner / ml-architect to refine.]

## Author note

This draft is the STRUCTURAL FRAMEWORK for Stage 5. ML-judgment
specifics (hyperparameters, seed selection, threshold values,
ensemble vs median, rollback investigation) are flagged for
ML-architect review.

DRAFT v0.1. Production: `STAGE5_RETRAIN_PROTOCOL_v1.0.md` after
ML-architect content fill + reviewer pass + owner approval.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — locked
  Stage 4 plan; multi-seed retrain spec is §6 of the locked plan
- `feedback_solver_findings.md` — solver-corrected reference labels
  (MW-30 CALL, MW-46 CALL, MW-47 RAISE)
- `reference_corrections.md` — 3 verified + 2 likely corrections
- `feedback_attention_flags_when_features_change.md` — v2.4 P1
  features + Exp 3 auxiliary attention flags (108-column training)
- `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` — Exp 3
  background (Spearman 0.912 vs baseline; production approach)
- `LABELLING_PIPELINE.md` — calibration exam infrastructure
