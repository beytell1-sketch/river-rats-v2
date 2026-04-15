---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Trainer + 108-feature eval rewrite — proceed now
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-15 (d)

Round 2 deliverables accepted. See
`REVIEW_ROUND2_2026-04-15.md`. Start trainer/eval rewrite
immediately.

## 1. Rewrite, not wait-for-recovery

The owner-side local-machine check can happen in parallel.
You do not wait for it. Reasoning:

- The trainer script needs to live in `river-rats-core/`
  regardless. That's CLAUDE.md §6 (sacred-folder rule). Even
  if owner finds the original, a cleaned-up version gets
  checked in.
- If owner finds the original, it becomes your **validation
  reference** — your rewrite must reproduce the same numbers.
  That upgrades verification strength.
- If owner cannot find it, your rewrite is the definitive
  artifact.
- Either way, the rewrite happens.

## 2. Scope

Produce:

### 2.1 `river-rats-core/train_model_v2_2.py`

Trainer that:
- Loads `training-data/v2_2_training.csv` (108 features:
  54 raw + 54 `attn_*`, label column `label`, metadata
  `situation_id` + `label_source`)
- Invokes `_preflight_schema_check()` from `train_model.py`
  before fitting — if `v2_2_training.csv` still has mixed
  encoding, the trainer must fail fast (per Fix 1 gate).
  This means you will not be able to actually fit v2.2 until
  after regeneration — see §4.
- Handles the mixed-encoding `street` / `hero_position`
  columns via explicit mapping-with-fallback (path 3 from
  ANOMALY_A report §2) — NOT `errors='coerce'` → NaN
  (path 2) and NOT silent-zero (path 5). Explicit mapping
  is the clean choice and what we want v2.2+ to use going
  forward.
- XGBoost config per `v2_2_training_report.json`:
  max_depth=5, lr=0.05, 800 rounds cap with early-stopping,
  class weights capped (BET ≤ 2.0, RAISE ≤ 3.0, others ≤ 4.0),
  stratified 80/20, 5-fold CV. best_iteration=95 on the
  original run.
- Saves to `river-rats-core/models/v2_2_model.json`
  (but to a different path during rewrite verification — do
  NOT overwrite the current file until we have reproduction
  confirmed; use `v2_2_model_rewrite.json`).
- Emits a training report comparable in shape to
  `v2_2_training_report.json`.

### 2.2 108-feature eval path

Add to `river-rats-core/reference_evaluator.py` (or a new
`evaluate_v2_2.py` — your call, prefer the shared module if
the shape extension is clean):
- 108-feature inference: extract 54 raw via
  `extract_all_features` → concat 54 `attn_*=1` → predict
- Legal-action masking: `facing_bet=False` → {CHECK, BET};
  `facing_bet=True` → {CALL, RAISE, FOLD}
- Reuse Track 1 dtype guard + completeness guard

### 2.3 Verification

Run FB-40 and MW-50 through the new eval path using the
**existing** `v2_2_model.json` (not your rewrite). Report
accuracy. Targets:
- FB-40: 72.5% (29/40) per PHASE_4_TRAINING_REPORT
- MW-50: 80.0% (40/50) with d2920-in / d4534-out swap per
  HRP re-extraction

If your rebuilt eval path matches both numbers, the 108-feature
reconstruction is validated. If either differs, that itself is
a finding — stop and report before doing anything else.

Only **after** 2.3 passes, proceed to retraining (§4).

## 3. Deliverables

- `review/comms/V22_TRAINER_RECOVERY_2026-04-15.md` — the
  report. Sections: recovery attempt outcome (see §5), eval
  path reconstruction, reproduction numbers (FB-40 / MW-50 on
  current model), training rerun numbers (CV / holdout) if §4
  runs, how mixed encoding was handled, verdict on ANOMALY-A
  loader path (is it discoverable from the model behaviour?).
- Code: `train_model_v2_2.py`, eval extension.
- Commit per deliverable. Push immediately.

## 4. Retraining — gated on CSV regeneration

The rewritten trainer will **not run** on the current
`v2_2_training.csv` (pre-flight gate will reject it). To
actually exercise §2.1 end-to-end you need a cleaned CSV.

Path forward (do NOT execute without further direction after
§2.3 lands):
- Regenerate `v2_2_training.csv` from the clean BP JSONLs
  (now numeric after Fix 1) plus the d-series JSONLs. This
  needs the assembly script that produced `9dd1a68`. If that
  is also missing, rewrite it — it's a concat + dedup on
  `situation_id`.
- Fit the rewrite model.
- Compare: CV should be 93.0% ± 3.5%, holdout 88.3%, FB-40
  72.5%, MW-50 80.0%. If the retrain matches, ANOMALY-A
  loader-path question is moot (the clean data reproduces
  the original numbers — path doesn't matter).
- If the retrain diverges notably (e.g. CV > 95% or MW-50
  improves materially), ANOMALY-A was impactful and the
  original v2.2 training was corrupted. That's a finding.
  Stop and report before overwriting anything.

Get §2.3 (eval path validation) complete and reviewed before
touching §4.

## 5. Owner-side local check — parallel, non-blocking

I will ask owner separately to check their local machines /
shell history for the original scripts. If found, they get
posted to `review/comms/V22_TRAINER_ORIGINAL_*.py` (or
similar). Treat those as **validation references only** —
compare your rewrite against them, do not blindly substitute.

If owner's check comes back empty, no change to your plan.

## 6. Tracks still held

- Track 4 (MW bias deep-dive): held until §2.3 eval
  reconstruction validates (unblocks Track 2) AND §4 retrain
  resolves ANOMALY-A loader-path question.
- Track 6 (scope corrections): held until Track 4.

Track 2 eval partial delivery (dtype guard) already
accepted — no further Track 2 deliverable needed beyond §2.3
validation numbers.

## 7. Protocols reminder

- Test-first on the trainer and eval module.
- Do NOT overwrite `v2_2_model.json` until reproduction
  confirmed.
- Commit and push each artifact separately.
- If anything diverges from expected numbers, stop and report.
