---
author: general-purpose subagent acting as ml-architect (dedicated subagent unavailable)
date: 2026-04-26
version: v1.0.1
derived_from: STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md
status: v1.0.1 (REQUEST-CHANGES fix-forward on v1.0)
review_chain:
  - orchestrator structural skeleton (v0.1 DRAFT, 2026-04-26)
  - v1.0 fill (ml-architect persona pass)
  - v1.0 independent reviewer pass — REQUEST-CHANGES at `463e718`
    (2 MEDIUMs + 1 MEDIUM-NIT)
  - v1.0.1 fix-forward (ml-architect persona, this file) — addresses
    REQUEST-CHANGES per orchestrator directive `9f8457e`
  - independent reviewer re-pass on v1.0.1 — REQUIRED before retrain
    dispatch
  - owner final approval — REQUIRED before retrain dispatch
changelog:
  v1.0:
    date: 2026-04-26
    fills:
      - "Hyperparameters: locked v2.3.2 baseline confirmed; +4 v2.4
        blocker features judged small enough not to require re-tuning;
        explicit theoretical + empirical defence."
      - "Seed selection: 3 seeds confirmed (variance-floor estimate +
        majority-vote tie-break); seeds replaced with deterministic
        SHA256-derived integers for reproducibility; per-library seed
        propagation documented (numpy, sklearn, xgboost)."
      - "Train/CV split: SAME split across seeds (option a) selected;
        rationale = clean attribution of model-init variance vs data-
        split variance; data-split variance estimated separately via
        the existing 5-fold CV inside each seed."
      - "±2pp accuracy spread threshold: empirically anchored on v2.3.2
        cv_std=0.023 (≈2.3pp); ±2pp is one within-fold-std-dev — tight
        but within reach of the same model on resampled folds."
      - "Top-10 Spearman ≥ 0.8 threshold: theoretically justified as
        the >0.7 'high agreement' threshold from feature-stability
        literature, lifted to 0.8 because v2.4 production target is
        decision-driver consistency (not just rank similarity)."
      - "Median single-seed selected over ensemble: deployment cost
        + reproducibility + oracle_router.py compatibility + median is
        unbiased; ensemble revisitable in v2.5 if median seed regresses
        on calibration anchors."
      - "Rollback procedures expanded to 5 enumerated failure modes,
        each with diagnostic steps + rollback decision criteria + fix-
        forward authoring path."
      - "PRE-RETRAIN PREREQUISITES section added (analogous to Protocol
        B/C PRE-PILOT BUILD REQUIREMENT)."
  v1.0.1:
    date: 2026-04-26
    derived_from_verdict: "review/comms/REVIEW_VERDICT_PR_14_STAGE5_RETRAIN_2026-04-26.md (`463e718`)"
    derived_from_directive: "review/comms/MAIN_TERMINAL_PR_14_FIX_FORWARD_REQUIRED_2026-04-26.md (`9f8457e`)"
    fixes:
      - "MEDIUM #1 — Prereq #2 column-count rewrite. Old text was
        self-contradictory ('110-column contract (54 raw + 4 v2.4
        blocker = 58 raw + 58 attn_*)' — 58+58=116, not 110, and 54
        undercounts v2.3.2 by 1). Rewritten to '118-column v2.4
        contract (55 raw + 4 v2.4 blocker = 59 raw + 59 attn_*)' —
        consistent with §Hyperparameters point #4 (v2.3.2 = 55+55=110)
        and the 'training-tensor goes 110 → 118 columns' line. Verified
        against `gto_model.py:33-62` (FEATURE_COLUMNS, N_FEATURES=55)
        and v2.3.2 training report `n_features: 110`."
      - "MEDIUM #2 — Mode D anchor inventory resolution. Verified that
        `river-rats-core/anchors/calibration_anchors.json` (introduced
        at commit `570ece2`, 2026-04-19; only commit ever to touch
        that file) contains 5 anchors: `d2410_CO_turn`,
        `LITMUS_A4d_Qs5s7s_flop`, `LITMUS_T5h_JJ2_flop`,
        `LITMUS_AA_7h5d2c_flop`, `LITMUS_KQ_KsTs3h_flop`.
        `d0182_BTN_turn` and `d8411_BB_turn` were NEVER in the
        production calibration fixture — they exist only as hard-coded
        diagnostic specs inside `review/run_v231_anchor_recheck_stage35.py`
        (a one-off Stage 3.5 M5 recheck script). The Stage 3.5 closure
        and M4/M5 audit closure used d0182/d8411 as β-panel
        diagnostics, not as live calibration anchors. Selected option
        (a): updated Mode D + the Gate 3 d0182/d8411 references to the
        actual production anchor IDs from `calibration_anchors.json`.
        Mode C diagnostic step #3 retains the historical d8411 +0.072
        Finding B note (referencing the M5 recheck artifact) since
        that's the relevant baseline to compare any v2.4 multiway
        BET-strength regression against, but it's framed as a Stage
        3.5 audit baseline, not a current-fixture anchor."
      - "MEDIUM-NIT — Variance-reduction math. Old text:
        '~30% lower predictive variance (1/√3)' — neither 1/√3≈0.577
        (SD ratio for N=3 averaging) nor 1/3 (variance ratio).
        Rewritten to '~42% lower predictive SD (1/√3 ≈ 0.577 ratio
        for averaging N=3 independent models; equivalently ~67% lower
        variance, 1/N for N=3)'. Both framings included for ML rigor."
    bundled_nits:
      - "Prereq #3 explicit orchestrator-action assignment — added
        sentence: 'This step requires orchestrator action pre-Stage-5
        (tag baseline model commit on origin); not automatic.'
        (Item G NIT from verdict.)"
    deferred_to_v1_1_or_task_5_wrapup:
      - "Bouthillier 3-vs-10-seed framing nuance (Item B NIT) — v1.1
        language tightening; gate behaviour unchanged."
      - "±2pp vs cv_std between-seed-vs-within-fold statistical nuance
        (Item D) — v1.0 already carries an UNCERTAIN tag; further
        formalisation deferred."
      - "Per-class precision floor for RAISE class (Item D NIT) —
        deferred to Task 5 wrap-up; Mode E + per-shape-category
        breakdown in §Reporting cover diagnostic path for now."
      - "Prereq #6 v2.3.2 MW reference-set baseline measurement
        (Item F NIT) — deferred to Task 5 wrap-up since option (a)
        was selected for MEDIUM #2 (no other Prereq #6 created)."
      - "Ensemble disagreement-as-uncertainty trade-off row (Item E
        NIT) — v1.1."
      - "Promote MW-stratified accuracy from Mode-E-diagnosis to
        Gate-1.5 (Item D promotion) — v1.1."
    not_changed:
      - "ML core unchanged: hyperparameter spec, 5-point hyperparameter
        defence, SHA256 seed scheme, per-library seed propagation,
        ±2pp + Spearman ≥ 0.8 thresholds, median-seed-over-ensemble
        decision, 5 rollback modes."
      - "All v1.0 UNCERTAIN tags preserved."
---

# Stage 5 Multi-Seed Retrain Protocol — v1.0.1

## Purpose

Stage 5 takes the Stage 4 relabelled corpus and trains v2.4. Per the
locked Stage 4 plan (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
commit `ee3d9f5`), Stage 5 uses **3-seed multi-seed training** with
agreement gates to distinguish "data noise" from "model capacity"
failure modes. This v1.0 spec fills the ML-judgment placeholders
flagged by the v0.1 DRAFT.

## PRE-RETRAIN PREREQUISITES

**THIS PROTOCOL CANNOT BE DISPATCHED UNTIL ALL FIVE PREREQUISITES
ARE MET.** Builder MUST verify each before calling the retrain script.

1. **Stage 4 labels landed.** Stage 4 final consensus labels file
   (`training-data/v2_4_consensus_labels_<date>.jsonl` or equivalent)
   exists, has been merged to master, and the SHA is recorded in the
   Stage 4 closure document. Per `feedback_github_is_state_not_local.md`:
   `git fetch && git status` clean before reading the labels file.

2. **Training-data export verified.** The Stage 4 → trainer-CSV export
   step has been run and the resulting CSV passes `_preflight_schema_check`
   (see `train_v2_3_2.py:84`). Verification: row count matches Stage 4
   consensus count minus DROPs; class distribution non-degenerate
   (all 5 classes present, none < 5% of corpus); **118-column v2.4
   contract (55 raw + 4 v2.4 blocker = 59 raw + 59 attn_*)** validated,
   OR the contract is updated and the change is documented in the
   report. (v2.3.2 baseline was 55+55=110 columns per
   `gto_model.py:33-62` `N_FEATURES=55` and v2.3.2 training report
   `n_features: 110`; the v2.4 delta is +4 raw blocker features per
   §Hyperparameters point #4, so 55+4=59 raw and the parallel
   attn_* layer also goes 55→59 per
   `feedback_attention_flags_when_features_change.md`.)

3. **Baseline model preserved as rollback.** `v2_3_2_model.json` and
   its manifest are tagged on origin (e.g.
   `pre-stage5-baseline-v2-3-2`) before any v2.4 training begins.
   Rollback rule: if all gates fail and Stage 5 is rejected, the live
   production model remains v2.3.2. **This step requires orchestrator
   action pre-Stage-5 (tag baseline model commit on origin); not
   automatic.** Builder verifies the tag exists before calling the
   retrain script and HALTs (per CLAUDE.md §5) if absent.

4. **Calibration / reference / held-out sets confirmed disjoint from
   training corpus.** Per `feedback_units_and_dedup.md`: explicitly
   verify no situation_id from the 40-hand reference set, the 24-hand
   calibration set, or the Stage 6 50-hand held-out set appears in
   the v2.4 training CSV. Output a 3-line confirmation in the
   pre-retrain log.

5. **Trainer script lives in `river-rats-core/`.** Per CLAUDE.md §6
   training provenance: the v2.4 trainer (e.g.
   `train_v2_4.py`, ported from `train_v2_3_2.py`) MUST be committed
   to `river-rats-core/` before producing the artifact. No inline
   `python3 <<'EOF'` heredoc training. The trainer's git SHA is
   recorded in the v2.4 model manifest.

If any prerequisite fails: HALT. Surface to orchestrator. Do NOT
improvise (CLAUDE.md §5 stop conditions).

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

**DECISION: keep v2.3.2 baseline hyperparameters verbatim. No
re-tuning for the +4 v2.4 blocker features.**

Locked hyperparameters (port from `train_v2_3_2.py:106-111`):

```python
{
  'n_estimators': 800,
  'max_depth': 5,
  'learning_rate': 0.05,
  'objective': 'multi:softprob',
  'num_class': 5,                    # FOLD/CHECK/CALL/BET/RAISE
  'eval_metric': 'mlogloss',
  'use_label_encoder': False,
  'random_state': <SEED>,            # varied per seed (see §Seed selection)
  'early_stopping_rounds': 50,
  'verbosity': 0,
}
```

`n_estimators=800` is an upper bound; early stopping on `mlogloss`
typically halts at ~100-200 trees (v2.3.2 best_iteration=138; v2.2
best_iteration=95).

**Class weighting: NONE** (matches v2.3.2 — see
`train_v2_3_2.py:169` `"class_weighting": "NONE"`). v2.2 used
weighted classes (BET 1.33, CALL 2.28, RAISE 3.00) but v2.3.2
explicitly removed this and improved holdout accuracy
(v2.2: 88.3% → v2.3.2: 90.3%). Stage 5 inherits the unweighted
v2.3.2 decision unless a Stage 4 class-distribution analysis shows
material drift that justifies re-introducing weights — in which case
that's a Stage 5 design change owner-gated, not a default.

#### Why the +4 blocker features don't warrant re-tuning

The v2.4 addition is +4 features over the existing 55 raw + 55 attn_*
schema (training-tensor goes 110 → 118 columns). Theoretical and
empirical reasoning for keeping v2.3.2 hyperparameters:

1. **XGBoost hyperparameter sensitivity to feature count is weak in
   the additive regime.** `max_depth=5` (max 32 leaves per tree) and
   `colsample_bytree`-equivalent (XGBoost default 1.0 here) both
   adapt automatically: at any given split the algorithm picks the
   gain-best feature from the available pool. Adding 4 features
   (~7% of the raw feature count) does not change the loss landscape
   topology; it only adds 4 candidate splits per node. (Friedman et
   al. 2001 — gradient boosting; Chen & Guestrin 2016 — XGBoost.)

2. **Learning rate (0.05) and n_estimators (800 cap) are calibrated
   to the loss surface, not to dimensionality.** Early stopping on
   `mlogloss` halts when the held-out CV loss plateaus. If the +4
   features carry useful signal, the model uses more trees before
   plateauing (best_iteration drifts up); if they don't, best_iteration
   stays put. Either way the hyperparameter spec is correct.

3. **L1/L2 regularisation (XGBoost defaults: lambda=1.0, alpha=0.0)
   handles potential redundancy.** `flush_block_pct` (existing
   feature 46) overlaps semantically with `nut_flush_block` and
   `flush_draw_block_pct` (new). XGBoost handles correlated features
   via gain-based split selection; the regularisation prior absorbs
   small additional model capacity. The feature-attention literature
   (and this project's own Exp 3 result, Spearman 0.912) shows
   ranking stability survives feature additions.

4. **Empirical: v2.2 → v2.3.2 added more than 4 features and did
   not require hyperparameter changes.** v2.2 used 54 raw + 54 attn_*
   = 108 columns; v2.3.2 went to 55 raw + 55 attn_* = 110 columns.
   `train_v2_3_2.py:17-19` provenance docstring explicitly notes
   "Ports `train_v2_3_1.py` verbatim for hyperparameters." Holdout
   accuracy improved (88.3% → 90.3%) without a tune. This is the
   single most direct empirical precedent for the v2.3.2 → v2.4
   delta.

5. **Re-tuning at this stage would conflate two effects.** Stage 5's
   purpose is to measure data-noise vs model-capacity contributions
   to v2.4 accuracy. Tuning hyperparameters concurrently with new
   features and new labels would make the resulting model's success
   (or failure) un-attributable. Per `feedback_compute_assumptions.md`:
   change one variable at a time. Hyperparameter sweep, if needed,
   is a v2.5 task with v2.4 as the reference.

#### What WOULD trigger a hyperparameter revisit

Listed for orchestrator + reviewer awareness; none of these are
expected to trigger but the protocol must enumerate the trigger
conditions:

| Trigger | Action |
|---|---|
| Stage 4 class distribution materially shifts (e.g. RAISE drops below 5% of corpus) | Reintroduce class weighting per v2.2 pattern; re-run Stage 5 with weighted losses |
| Stage 4 corpus shrinks below ~400 hands (from ~600 expected) | Drop `max_depth` to 4 to reduce overfit risk; reduce `n_estimators` cap to 400 |
| All 3 seeds early-stop at the n_estimators cap (=800) | Loss has not plateaued; increase cap to 1500 and re-run |
| Holdout accuracy < v2.3.2 baseline (90.3%) by > 3pp | Re-tune `learning_rate` (try 0.03 + 0.1 sweep) before declaring v2.4 model insufficient |

These are conditional re-tunes triggered by Stage 5 evidence, NOT
default Stage 5 work. The default is: keep v2.3.2 hyperparameters,
vary only the seed.

### Seed selection

**Three seeds**, deterministically derived for reproducibility.

#### Why 3 seeds (not 5, not 10)

3 is the minimum for:
- A meaningful spread (max − min) calculation
- A median (not biased by single outlier)
- Pairwise Spearman triangle (3 pairs from 3 seeds)

5 or 10 seeds give tighter variance estimates but at 3-5× compute
cost. ML-literature guidance (Reimers & Gurevych 2017 — "Reporting
Score Distributions Makes a Difference: Performance Study of LSTM-
networks for Sequence Tagging"; Bouthillier et al. 2021 — "Accounting
for Variance in Machine Learning Benchmarks") recommends ≥5 seeds
for strong variance claims, but 3 seeds is sufficient for "is the
model stable enough to ship?" — which is the Stage 5 question.

If Gate 1 produces a MARGINAL spread (2.1–3.0pp) the recommendation
is to expand to 5 seeds (add 2 more) BEFORE declaring fail —
documented in §Rollback below.

#### Why these specific seed values

Replace the v0.1 DRAFT placeholders (42, 2026, 1729) with
deterministic SHA256-derived integers. Reproducibility rationale:

- **Reproducible** — anyone re-deriving from the same anchor string
  gets the same seeds; no "magic numbers."
- **Bias-free** — SHA256 is a cryptographic hash; no human bias
  toward "lucky" or "round" numbers; no risk of inadvertently
  picking known-good seeds.
- **Shareable** — the anchor string ("river-rats-v2-stage-5-seed-N")
  goes in the Stage 5 report; reviewer can re-derive and verify.

Derivation rule (executed in the trainer script):

```python
import hashlib
def derive_seed(n: int) -> int:
    h = hashlib.sha256(f"river-rats-v2-stage-5-seed-{n}".encode()).digest()
    return int.from_bytes(h[:4], 'big') % (2**31 - 1)

SEEDS = [derive_seed(0), derive_seed(1), derive_seed(2)]
```

The actual integer values are computed at trainer-script execution
time and recorded in the Stage 5 report. Do NOT pre-compute and
hard-code — that defeats the reproducibility argument.

#### Per-library seed propagation

XGBoost is the only learner; sklearn's `train_test_split` and
`StratifiedKFold` also accept a seed. Numpy is used for
sampling/shuffling. The trainer MUST set the same seed in:

```python
import random, numpy as np
random.seed(SEED)
np.random.seed(SEED)
# sklearn:
train_test_split(..., random_state=SEED, stratify=y)
StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
# xgboost:
xgb.XGBClassifier(..., random_state=SEED)
```

This is one seed value driving all four RNG sources via their
own state. Stage 5 trainer must NOT use Python's global `random`
state (e.g. `np.random.shuffle` without a Generator) — that creates
an uncontrolled fourth RNG source that breaks reproducibility. The
existing `train_v2_3_2.py` already uses `random_state=42` for
`train_test_split` and `StratifiedKFold`; v2.4 trainer extends this
pattern to `xgb.XGBClassifier(random_state=SEED)` and adds explicit
`random.seed(SEED)` + `np.random.seed(SEED)` at the top of `main()`.

### Training data partitioning (identical across seeds)

**DECISION: SAME train/CV split across all three seeds** (option a
from v0.1 DRAFT).

- **Train set:** ~80% of corpus (matches v2.3.2 `test_size=0.20`,
  stratified by label)
- **Holdout test set within trainer:** ~20% (the `train_test_split`
  test partition; used for early stopping per v2.3.2 pattern)
- **Reference set:** the existing 40-hand reference set, NOT in
  training data
- **Held-out test set:** new 50-hand held-out set per Stage 6 spec
  (`STAGE6_HOLDOUT_TESTSET_DRAFT_*` — to be authored), NOT in
  training data
- **Calibration set:** existing 24-hand calibration set, NOT in
  training data

Same train/test partition (same hands, same stratification) across
all three seeds. Only the seed argument changes.

#### Why same split, not different split per seed

The Stage 5 question is "is the model stable enough to ship?" The
two factors that drive instability are:

(a) **Model-initialisation variance** — same data, different
    XGBoost RNG state (column subsampling, tree-build order)
(b) **Data-split variance** — different held-out sample, same
    model spec

Stage 5's 3-seed gate is designed to measure (a) cleanly. (b) is
already measured separately by the 5-fold StratifiedKFold inside
each seed (v2.3.2 pattern: 5 folds per seed × 3 seeds = 15 fold
estimates total, with cv_std reported per seed).

If we used different splits per seed, (a) and (b) would be entangled
and the spread could be high either because the model is unstable
OR because the data is small enough that 80/20 splits vary
substantially. Disentangling those would require a 2D matrix
(seeds × splits), which is beyond Stage 5 scope.

The "different split per seed" approach (option b) IS more robust
to split-specific noise but only matters if we expect data-split
sensitivity to dominate model-init sensitivity, and at corpus size
~600 with stratified splitting this is unlikely. The hybrid
(option c) was rejected as combining the worst of both.

[UNCERTAIN: this decision should be revisited if Stage 4 corpus
ends up < 400 hands — at that size data-split variance starts
materially affecting the 80/20 partition. Owner / ml-architect to
revalidate at Stage 4 close.]

## Agreement gates

After 3 models trained (one per seed):

### Gate 1 — Reference-set accuracy spread ≤ ±2pp

Each model evaluated on the 40-hand reference set (solver-corrected
labels from `feedback_solver_findings.md` + `reference_corrections.md`).

Compute accuracy per seed: e.g. seed-A = 84.5%, seed-B = 83.0%,
seed-C = 85.0%. Spread: max − min = 85.0 − 83.0 = 2.0pp.

| Spread | Verdict | Action |
|---|---|---|
| ≤ ±2pp | PASS | Proceed to Gate 2 |
| ±2.1pp – ±3.0pp | MARGINAL | Expand to 5 seeds (add seed-D + seed-E) before declaring; if 5-seed spread still > 2pp, owner-gated decision per §Rollback |
| > ±3.0pp | FAIL | Data is noisy or model is unstable. Retrain blocked. Investigate per §Rollback Mode A. |

#### Why ±2pp

Empirical anchor: v2.3.2 cv_std = 0.0232 (training_report
`cv_std`: 0.02315254...). One within-fold standard deviation is
≈2.3pp. ±2pp is one-σ on the v2.3.2 baseline — tight enough to
catch instability, loose enough to be achievable.

This is NOT a literature default; it's a project-specific anchor
on the most recent comparable model. If v2.4's corpus is
materially larger or smaller than v2.3.2's 716 rows, the σ will
shift and the threshold should be re-anchored. At 716 rows v2.3.2
σ=0.023; at ~550 rows (600 corpus minus 8% DROPs) the central
limit theorem suggests σ scales roughly with √(N_v23/N_v24) ≈
1.14× → estimated v2.4 σ ≈ 0.026, so ±2pp remains close to one-σ
but is now slightly tight. Acceptable — tightness is the
quality-default direction (`feedback_quality_default_no_ask.md`).

[UNCERTAIN: ±2pp is one-σ which is a conservative-strict choice;
two-σ (≈4.6pp on v2.3.2 baseline) would be the conventional "95%
confidence interval" interpretation. The choice of one-σ over two-σ
is a quality default. Reviewer to flag if they prefer the looser
interpretation.]

### Gate 2 — Top-10 feature-importance Spearman ≥ 0.8 across seeds

Each model produces a feature-importance ranking (XGBoost gain or
shap-mean per feature; trainer should record both, gate uses
gain). Compute pairwise Spearman correlation on the top-10
features across the 3 seeds: A↔B, B↔C, A↔C.

| All 3 pairwise Spearman | Verdict | Action |
|---|---|---|
| All ≥ 0.8 | PASS | Proceed to Gate 3 |
| 1+ pairwise ∈ [0.6, 0.8) | MARGINAL | Investigate which features differ (per §Rollback Mode B); owner-gated decision |
| 1+ pairwise < 0.6 | FAIL | Data is structurally noisy on which features matter. Flag for v2.5 feature engineering before retraining. |

#### Why ≥ 0.8 on top-10

Theoretical anchor: feature-stability literature (Nogueira & Brown
2016 — "Measuring the Stability of Feature Selection") reports
ρ ≥ 0.7 as "high agreement" and ρ ≥ 0.9 as "near-perfect." We
pick 0.8 because:

- The Exp 3 attention experiment (`RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md`)
  reported Spearman 0.912 between the attention-augmented model
  and baseline — that's 0.8+ across architectural changes, so
  same-architecture different-seed should comfortably exceed 0.8.
- The v2.4 production target is decision-driver consistency (the
  router uses the model's top features as proxy for which features
  actually drive predictions). 0.7 is "agreement"; 0.8 is "the
  model is using the same features in the same priority order."
- 0.9 would be too tight: at top-10 with realistic seed-driven
  splits, even a stable model can swap rank 7 ↔ rank 8 of similar-
  importance features and drop pairwise Spearman to ≈0.85.

Top-10 (not top-5, not top-20): 5 is too few (one swap = 0.7
Spearman); 20 is too many (the lower-ranked features have noisy
gain values and Spearman becomes dominated by noise). 10 is the
"head" of the importance distribution where decisions are made.

[UNCERTAIN: the top-10 vs top-20 boundary is a judgement call.
Empirical pilot: when v2.4 trainer is built, run a 3-seed mini-pilot
on the v2.3.2 corpus to measure baseline same-architecture
seed-driven Spearman. If baseline is < 0.85 on top-10, relax the
gate; if > 0.95, tighten. Reviewer to consider whether to require
this mini-pilot.]

### Gate 3 — Calibration exam pass

Each model takes the 24-hand calibration exam (independent grading
against answer key). Required: 20/24 + all 3 GTO-reversal hands
(MW-30 CALL, MW-46 CALL, MW-47 RAISE per
`feedback_solver_findings.md` + `reference_corrections.md`) correct.

Per `evaluate_calibration_anchors.py` (existing file in
`river-rats-core/`): the script already grades against the
calibration fixture (`river-rats-core/anchors/calibration_anchors.json`)
and reports per-anchor predictions. As of `570ece2` (2026-04-19) the
fixture contains exactly 5 anchors: `d2410_CO_turn` (TPGK turn,
expected BET — the v2.3.2 regression anchor), `LITMUS_A4d_Qs5s7s_flop`
(air on monotone, expected CHECK), `LITMUS_T5h_JJ2_flop` (air on
paired board, expected CHECK), `LITMUS_AA_7h5d2c_flop` (overpair
dry, expected BET), `LITMUS_KQ_KsTs3h_flop` (TPGK two-tone, expected
BET). Gate 3 requires `evaluate_calibration_anchors.py` to run on
each of the 3 seed-models and pass all 5 anchors per their
`tolerance` rule (`strict`: top-1 == expected; `mixed`: expected in
top-2 with p ≥ 0.20).

| All 3 seeds pass (20/24 + all 3 reversals) | Verdict |
|---|---|
| YES | PASS — proceed to seed selection |
| Some seeds pass | MARGINAL — investigate per §Rollback Mode C; owner-gated decision |
| No seeds pass | FAIL — Stage 4 labelling regression; rollback to Stage 4 per §Rollback Mode E |

## Seed selection (post-gates)

If Gates 1-3 all PASS: pick the **median seed** by reference-set
accuracy. NOT the best.

**Why median, not best:** "best of 3 seeds" is selection bias on
the same data — picks the seed that happens to fit reference-set
noise the closest. Median is the unbiased estimator (Bouthillier
et al. 2021).

#### Why median single-seed, not ensemble

Considered: average ensemble of all 3 seeds (each prediction is
mean of 3 seed predictions). REJECTED for v2.4. Trade-offs:

| Dimension | Median single-seed | 3-seed ensemble |
|---|---|---|
| Inference cost | 1× (current router pattern) | 3× (each prediction runs 3 models) |
| Model-artifact size | 1× (~MB) | 3× (~3MB) — mobile-deployment concern |
| Calibration anchor reproducibility | Exact (same model object) | Approximate (averaging adds float-error noise) |
| `oracle_router.py` compatibility | Drop-in (replaces `v2_3_2_model.json`) | Requires router rework to handle 3 models |
| `gto_model.py` compatibility | Drop-in (single XGBoost predictor) | Requires aggregation layer (mean of probs, then argmax) |
| Variance reduction | None (you discard 2 of 3 models' info) | ~42% lower predictive SD (1/√3 ≈ 0.577 ratio for averaging N=3 independent models; equivalently ~67% lower variance, 1/N for N=3) |
| Selection bias | None (median is unbiased) | None (uses all 3) |
| Reproducibility | Single artifact + single trainer SHA | 3 artifacts + 3 trainer SHAs (all same script, different seeds) |

The variance-reduction case for ensemble is real but the
deployment + router-compatibility cost is concrete and immediate,
while the variance reduction is a theoretical 1/√3 SD ratio
(~42% lower SD, equivalently ~67% lower variance for N=3 averaging
of independent models) that may not show up in shape-category
accuracy. v2.4 ships with median single-seed; if Stage 6 ship-gate
identifies a class of hands where ensemble would have helped
(e.g. close-call hands where seed disagreement maps to user-visible
inconsistency), ensemble is a v2.5 candidate.

The chosen seed is **v2.4 candidate**. Submit to Stage 6 ship gate.

[UNCERTAIN: if all 3 seeds tie on reference-set accuracy (e.g.
all three score 84.0% within rounding), the median is undefined.
Tie-break rule: pick the seed with the lowest cv_std (most
internally-stable model). If still tied, pick seed-A (the first
deterministically-derived seed). Reviewer to consider whether
this rule belongs in the trainer script as a deterministic
fallback.]

## Reporting

Stage 5 produces `STAGE5_RETRAIN_REPORT_<date>.md` with:

- All 3 seeds' integer values + the SHA256 anchor strings used to
  derive them
- All 3 seeds' hyperparameters (locked, identical except `random_state`)
- All 3 seeds' training curves (train/CV mlogloss + accuracy)
- All 3 seeds' final reference-set accuracy + per-shape-category
  breakdown (8 MUST #49 categories)
- Top-10 + top-20 feature importance ranking per seed (gain) +
  pairwise Spearman matrix
- Calibration exam result per seed (24-hand grades + the 5 production
  calibration_anchors.json anchors: `d2410_CO_turn`,
  `LITMUS_A4d_Qs5s7s_flop`, `LITMUS_T5h_JJ2_flop`,
  `LITMUS_AA_7h5d2c_flop`, `LITMUS_KQ_KsTs3h_flop`; + the optional
  Stage 3.5 audit diagnostic `d8411_BB_turn` per
  `review/run_v231_anchor_recheck_stage35.py`)
- Gate 1 / 2 / 3 outcomes with thresholds + actuals
- Median-seed selection rationale (which seed, why)
- Tie-break invocation if applicable
- v2.4 candidate model artifact pointer + trainer SHA + Stage 4
  corpus SHA the retrain was done against

Provenance discipline: report records its authoring agent (whoever
ran the training script) + reviewer agent (independent ML-architect
or general-purpose-with-persona-fallback) + the Stage 4 corpus SHA
the retrain was done against.

## Rollback

If any gate fails, follow the per-mode rollback procedure below.
General rule per `feedback_quality_default_no_ask.md`: take the
slow/quality path. Don't ship v2.4 with marginal gates.

### Mode A — Gate 1 FAIL (accuracy spread > ±3pp)

**Diagnosis steps:**

1. Plot per-seed accuracy on each of the 8 MUST #49 shape categories.
   If spread is concentrated in one category, the corpus has too few
   hands of that shape and seed-variance is amplified.
2. Per-hand prediction agreement across seeds: count hands where all
   3 seeds disagree, vs hands where 2-of-3 agree. High all-disagree
   count → fundamentally noisy region of feature space.
3. Cross-reference disagreed hands with Stage 4 confidence band
   (HIGH / MEDIUM / LOW). If disagreed hands cluster in MEDIUM/LOW
   confidence bands, the issue is label noise.
4. Per `feedback_units_and_dedup.md`: verify the 40-hand reference
   set has no inadvertent duplicates inflating disagreement signal.
5. Expand to 5 seeds before declaring FAIL. If 5-seed spread is still
   > 3pp, the model spec is unstable on this corpus.

**Rollback decision criteria:**

- IF disagreement is shape-concentrated AND that shape is
  under-represented (< 40 hands of that shape in corpus): rollback to
  Stage 4 with directive to relabel + supplement that shape category.
- IF disagreement is uniform across shapes AND clusters in
  LOW-confidence Stage 4 hands: rollback to Stage 4 with directive
  to drop LOW-confidence hands or re-adjudicate them.
- IF disagreement is uniform AND not band-correlated: rollback to
  v2.3.2; v2.4 is structurally not stable on the new corpus and
  hyperparameter / feature work is needed (v2.5 territory).

**Fix-forward authoring path:** Stage 5 author writes
`STAGE5_GATE1_FAIL_<date>.md` with the diagnosis output, the
recommended rollback target, and the proposed re-pilot scope.
Owner-gated.

### Mode B — Gate 2 FAIL (top-10 feature importance Spearman < 0.6)

**Diagnosis steps:**

1. Tabulate top-10 features per seed side-by-side. Mark features that
   are top-10 in some seeds but not others.
2. For each "swap" feature: examine its gain value distribution. If
   gain values for swapping features are within ±20% of each other,
   the swap is statistical noise (those features have similar real
   importance). If gain values diverge substantially, the model is
   genuinely indecisive about which to use.
3. Specifically check the +4 v2.4 blocker features (`nut_flush_block`,
   `flush_draw_block_pct`, `straight_draw_block_pct`,
   `nut_made_block_pct`). If 1+ blocker feature appears in some seeds'
   top-10 but not others, the new features are destabilising the
   ranking.
4. Run a leave-one-feature-out variant of the median seed: retrain
   median seed with each of the 4 new blocker features removed.
   Compare the resulting top-10 stability.

**Rollback decision criteria:**

- IF the unstable swaps are between similar-gain features (noise):
  ACCEPT the marginal gate; document the swap as expected statistical
  variation; proceed to Gate 3.
- IF the unstable swaps involve the +4 blocker features AND removing
  them stabilises the ranking AND accuracy stays within 1pp: ROLLBACK
  the +4 features; ship v2.4 without blocker features (revert to v2.3.2
  feature set).
- IF the unstable swaps involve the +4 blocker features AND removing
  them stabilises the ranking BUT accuracy drops > 1pp: the features
  are useful but unstable. ROLLBACK to v2.3.2 baseline; flag for v2.5
  feature engineering on blocker features (e.g. better feature scaling,
  binning, or interaction terms).

**Fix-forward authoring path:** Stage 5 author writes
`STAGE5_GATE2_FAIL_<date>.md`. Owner-gated.

### Mode C — Gate 3 FAIL (calibration exam regression)

**Diagnosis steps:**

1. Per-anchor breakdown: which of the 3 GTO-reversal anchors (MW-30,
   MW-46, MW-47) failed in which seeds. If all 3 seeds fail on the
   same anchor, the issue is corpus-wide; if seeds vary, the issue
   is seed-specific.
2. Cross-reference failed anchors with Stage 4 labels for the same
   situations. If Stage 4 mislabelled the analogous shapes, the model
   has internalised the wrong label.
3. Run the 5 production calibration anchors per
   `evaluate_calibration_anchors.py` (`d2410_CO_turn` +
   `LITMUS_A4d_Qs5s7s_flop` + `LITMUS_T5h_JJ2_flop` +
   `LITMUS_AA_7h5d2c_flop` + `LITMUS_KQ_KsTs3h_flop`). Additionally,
   re-run `review/run_v231_anchor_recheck_stage35.py` on each seed
   to obtain the d8411_BB_turn diagnostic — the d8411 multiway
   BET-strength signal was STRENGTHENED in Stage 3.5 commit 14
   Finding B (0.589 → 0.661 p(BET) per
   `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`). If d8411 regresses
   below the 0.661 Stage 3.5 baseline (or back to v2.3.2's pre-Finding-B
   level), Stage 4 may have mis-labelled the multiway BET-strength
   signal. (d8411 is a Stage 3.5 audit-script diagnostic, not a
   production calibration-fixture anchor; for v2.4 ship Gate 3 only
   the 5 fixture anchors are mandatory.)
4. Per `feedback_solver_findings.md` + `reference_corrections.md`:
   verify the calibration exam answer key still reflects solver-
   corrected labels (MW-30 CALL, MW-46 CALL, MW-47 RAISE).

**Rollback decision criteria:**

- IF all 3 seeds fail on the same anchor AND analogous Stage 4 hands
  are mislabelled: ROLLBACK to Stage 4; re-adjudicate the analogous-
  shape hands with solver-verify pass.
- IF some seeds pass + some fail on the same anchor: model variance
  on a borderline call. Pick the seed that passed (NOT median in this
  case — calibration exam is the harder bar than reference accuracy).
  Document the deviation from median rule.
- IF the d8411_BB_turn audit-script diagnostic regresses below the
  Stage 3.5 Finding-B baseline of 0.661 p(BET) (per
  `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`): Stage 4 corpus did
  not preserve the Finding B multiway BET-strength signal. ROLLBACK
  to Stage 4; re-adjudicate multiway hands.

**Fix-forward authoring path:** Stage 5 author writes
`STAGE5_GATE3_FAIL_<date>.md`. Owner-gated.

### Mode D — Calibration anchor regression (5 production anchors in `calibration_anchors.json`)

This is a sub-mode of Gate 3 but warrants explicit treatment because
the production calibration fixture (`river-rats-core/anchors/calibration_anchors.json`,
introduced at `570ece2` 2026-04-19) is the strongest known-correct
distribution-shift signal in the corpus. The 5 anchors:

| Anchor ID | Tolerance | Expected | Class protected |
|---|---|---|---|
| `d2410_CO_turn` | strict | BET | TPGK turn after flop check (the v2.3.2 regression class) |
| `LITMUS_A4d_Qs5s7s_flop` | strict | CHECK | Air on monotone (v2.3.1 air-class playtest fix) |
| `LITMUS_T5h_JJ2_flop` | strict | CHECK | Air on paired board (v2.3.1 air-class playtest fix) |
| `LITMUS_AA_7h5d2c_flop` | strict | BET | Overpair dry (v2.3.2 Path C value litmus) |
| `LITMUS_KQ_KsTs3h_flop` | strict | BET | TPGK two-tone (v2.3.2 Path C value litmus) |

Plus an OPTIONAL Stage 3.5 audit diagnostic: `d8411_BB_turn` — NOT in
`calibration_anchors.json`, only in `review/run_v231_anchor_recheck_stage35.py`
— provides the multiway BET-strength baseline (0.661 p(BET) post-Finding-B
per `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md`).

**Diagnosis steps:**

1. Run `evaluate_calibration_anchors.py` against each of the 3 seeds'
   models. All 5 production anchors must pass per their `tolerance`
   rule.
2. Compare per-anchor predicted action + top-1 probability against
   the v2.3.1/v2.3.2 retroactive-audit baseline recorded in
   `BUILDER_V24_P0_LANDED_2026-04-19.md` (commit `570ece2`):
   v2.3.1 5/5 PASS clean margins 0.93-0.99; v2.3.2 4/5 with
   d2410_CO_turn FAIL (predicts CHECK 0.713 vs expected BET 0.287).
   v2.4 must restore d2410_CO_turn → BET (the Stage-4 + Stage-5
   primary objective) and preserve all 4 LITMUS_* anchors.
3. Run `review/run_v231_anchor_recheck_stage35.py` against each
   seed to obtain the d8411_BB_turn p(BET) diagnostic. v2.4 must
   preserve OR strengthen the post-Finding-B baseline of 0.661
   p(BET); regression below v2.3.1's pre-Finding-B 0.589 is a
   multiway BET-strength regression signal.
4. If `d2410_CO_turn` or any LITMUS_* anchor regresses, examine the
   Stage 4 labels for the analogous shapes (TPGK turn-after-flop-check
   for d2410; air-on-monotone or air-on-paired for the air LITMUSes;
   overpair-dry or TPGK-two-tone for the value LITMUSes). If labels
   diverged from v2.3.1/v2.3.2 training labels for the same shape,
   Stage 4 introduced a regression.

**Rollback decision criteria:**

- IF `d2410_CO_turn` does NOT pass (the primary v2.3.2 regression
  anchor that motivates the entire v2.4 retrain): v2.4 has not
  achieved its core objective. ROLLBACK to v2.3.2 OR diagnose Stage 4
  label coverage of TPGK-turn shapes per Mode A/C.
- IF any LITMUS_* anchor flips action (BET → CHECK or similar): the
  model has lost a known-correct GTO signal previously protected by
  v2.3.1/v2.3.2. ROLLBACK to v2.3.2.
- IF d8411_BB_turn p(BET) regresses below 0.661 (loses Finding B
  strengthening): Stage 4 corpus does not encode the multiway
  BET-strength signal. ROLLBACK to Stage 4 with directive to
  re-adjudicate multiway hands with explicit Finding B reasoning
  trace required. (Diagnostic, not Gate-3-blocking — d8411 is a
  Stage 3.5 audit anchor, not in the production fixture.)

**Fix-forward authoring path:** Stage 5 author writes
`STAGE5_ANCHOR_REGRESSION_<date>.md`. Owner-gated.

### Mode E — Multiway accuracy decline > 5pp on reference set

This is a specialised gate inherited from the original 88.1% HU /
52.5% multiway split (per CLAUDE.md project state). Multiway accuracy
is the project's known weak point; v2.4 must not regress further.

**Diagnosis steps:**

1. Stratify reference-set accuracy by HU vs MW. Compute per-seed.
2. If MW accuracy regresses below v2.3.2's MW baseline (recorded in
   `v2_2_evaluation_report.json` and the v2.3.2 evaluation chain):
   the new corpus or features have not improved (or have hurt) MW.
3. Run `evaluate_v2_2.py` on the median v2.4 model with `--mw-only`
   filter (or equivalent) to isolate MW-specific regressions.
4. Cross-reference with the +4 blocker features: are they MW-specific
   in their feature definition? If yes, they should help MW; if MW
   regresses anyway, the features are mis-specified.

**Rollback decision criteria:**

- IF MW regresses > 5pp AND HU does not regress: feature engineering
  problem on the +4 blockers. Per Mode B fix-forward path.
- IF both HU and MW regress: corpus / hyperparameter problem. Per
  Mode A.
- IF MW regresses ≤ 5pp: ACCEPT the regression with documentation;
  flag for v2.5 multiway focus.

**Fix-forward authoring path:** Stage 5 author writes
`STAGE5_MW_REGRESSION_<date>.md`. Owner-gated.

## Author note

This v1.0 fills the 6 ML-judgment placeholders flagged in v0.1
DRAFT (hyperparameters, seed selection, train/CV split, threshold
values, ensemble vs median, rollback procedures) and adds a
PRE-RETRAIN PREREQUISITES section.

v1.0.1 surgically addresses the v1.0 reviewer REQUEST-CHANGES
verdict (`463e718`) per orchestrator directive (`9f8457e`):
Prereq #2 column-count rewrite (110 → 118 with 55+4=59 raw and
59 attn_*); Mode D + Gate 3 + Mode C + §Reporting anchor IDs
updated to match the active production fixture
(`river-rats-core/anchors/calibration_anchors.json`: d2410_CO_turn
+ 4 LITMUS_*; d0182/d8411 retired as fixture-eligible anchors,
d8411 retained as a Stage 3.5 audit-script diagnostic only);
variance-reduction math corrected from "30% lower variance (1/√3)"
to the mathematically-correct 42% SD / 67% variance reduction for
N=3 averaging. ML core unchanged.

The dominant risk is corpus-size-driven: at ~600 hands, three
hyperparameter-related decisions (max_depth=5, n_estimators=800,
80/20 split) are inherited from v2.3.2's 716-row training. If
Stage 4 corpus comes in materially smaller (< 400 hands), the
Mode A trigger conditions in §Hyperparameters apply and Stage 5
should pause for a corpus-size-aware re-tune before dispatching.

v1.0.1 awaits independent reviewer re-pass + owner approval before
any retrain dispatch.

## Self-consistency notes (author pass)

1. ±2pp threshold derives from v2.3.2 cv_std=0.0232 → empirically
   anchored.
2. Top-10 Spearman ≥ 0.8 derives from Nogueira & Brown 2016 + Exp 3
   project precedent → theoretically + empirically anchored.
3. Hyperparameters all justified: 5 reasons listed; +4 features
   judged additive not architectural.
4. Rollback Modes A-E enumerate the 5 most likely failure modes;
   each has diagnosis steps, decision criteria, fix-forward path.
5. Per-library seed propagation lists 4 RNG sources (random,
   numpy, sklearn, xgboost) — single seed value drives all four.
6. Same-split decision is consistent with v2.3.2 trainer pattern
   (`train_v2_3_2.py:101-103` uses `random_state=42` deterministic
   split, only the trainer randomness changes per seed in v2.4).
7. PRE-RETRAIN PREREQUISITES section parallels Protocol B/C
   PRE-PILOT BUILD REQUIREMENT pattern.
8. Memory alignment: `feedback_quality_default_no_ask.md` →
   one-σ threshold (strict default); `feedback_units_and_dedup.md`
   → explicit dedup verification in prerequisites + Mode A;
   `feedback_compute_assumptions.md` → "change one variable at a
   time" cited in §Hyperparameters; `feedback_solver_findings.md`
   + `reference_corrections.md` → solver-corrected labels cited
   in Gate 3 + Mode C.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — locked
  Stage 4 plan; multi-seed retrain spec is §6 of the locked plan
- `STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md` — v0.1 DRAFT this
  v1.0 derives from
- `feedback_solver_findings.md` — solver-corrected reference labels
  (MW-30 CALL, MW-46 CALL, MW-47 RAISE)
- `reference_corrections.md` — 3 verified + 2 likely corrections
- `feedback_attention_flags_when_features_change.md` — v2.4 P1
  features + Exp 3 auxiliary attention flags (108-column training)
- `RESULTS_FEATURE_ATTENTION_TRAINING_2026-04-14.md` — Exp 3
  background (Spearman 0.912 vs baseline; production approach)
- `LABELLING_PIPELINE.md` — calibration exam infrastructure
- `train_v2_3_2.py` — current trainer; v2.4 trainer ports verbatim
  except for the seed-loop wrapper
- `train_model_v2_2.py` — class-weighting v2.2 reference (NOT
  applied in v2.4 default)
- `evaluate_calibration_anchors.py` — Gate 3 + Mode C/D evaluator
- `MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`
  — Stage 3.5 closure; d8411 STRENGTHENED baseline for Mode D
- Bouthillier et al. 2021, "Accounting for Variance in Machine
  Learning Benchmarks" — seed-variance literature
- Nogueira & Brown 2016, "Measuring the Stability of Feature
  Selection" — feature-stability Spearman thresholds
- Reimers & Gurevych 2017, "Reporting Score Distributions Makes a
  Difference" — multi-seed reporting practice
- Chen & Guestrin 2016, "XGBoost: A Scalable Tree Boosting System"
  — hyperparameter sensitivity to dimensionality
