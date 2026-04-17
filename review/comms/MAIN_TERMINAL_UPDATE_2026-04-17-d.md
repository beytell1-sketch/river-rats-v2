---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Phase 7 STOP — Option 3 (UMBRELLA pruning) + retrain
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-17 (d)

Root cause is self-evident from the numbers: 62.8% BET in
training vs 25.7% in v2.2 flipped the model from CHECK-biased
to BET-biased. No diagnostic retrain needed to confirm.

## Fix: Option 3 — prune UMBRELLA, retrain, re-evaluate

### Step 1 — Prune UMBRELLA from 268 to ~80

Keep the most predicate-concentrated hands (those closest to
the bias-signature center: highest worse_hand_pct, highest
villain_checked_back × villain_range_capped co-occurrence,
SPR closest to 1.25). Discard the periphery.

Pruning criteria (rank + cut):
- Score each UMBRELLA hand by distance to the bias-signature
  centroid (the feature medians from Stream C §5: HRP 0.884,
  equity_vs_range 0.875, worse_hand_pct 0.946, SPR 1.25)
- Keep the 80 closest; discard the rest
- If the 80 are still >90% BET-labelled (likely), that's fine
  — the volume reduction is what matters, not the label ratio
  within the UMBRELLA subset

Rows 1-12 (~130 hands) stay untouched. They carry the
specific sub-pattern signal the v2.3 scope designed.

Pilot hands (16) stay.

Curated hands (3) stay.

### Step 2 — Rebuild v2_3_training.csv

New total: 385 (v2.2 base) + ~130 (rows 1-12) + 80 (pruned
UMBRELLA) + 16 (pilot) + 3 (curated) = ~614 rows.

Expected BET distribution: ~99 (v2.2) + ~130 (rows 1-12,
mostly BET) + ~72 (UMBRELLA 80 × 90%) + ~15 (pilot BET) +
~3 (curated BET) = ~319 BET / ~614 total = **~52% BET**.

This is above v2.2's 25.7% but well below 62.8%. The bias-fix
signal is preserved; CHECK discrimination has room to survive.

Preflight must pass clean (no --allow-mixed-encoding).

### Step 3 — Retrain (Phase 6 re-run)

Same XGBoost config as v2.3-iter-1:
- max_depth=5, lr=0.05, 800 rounds + early stopping
- Same class weight caps (BET ≤ 2.0, RAISE ≤ 3.0, others ≤ 4.0)
- Save as `v2_3_model_iter2.json` — do NOT overwrite iter1

### Step 4 — Re-evaluate (Phase 7 re-run)

Targets (same as before):
- FB-40 ≥ 70.0% (29/40 or better)
- MW-50 ≥ 82.5% (42/50 or better, using the 84% live-model
  canonical baseline)
- Group D regression ≤ 1 hand vs v2.2
- Groups A+B absolute ≥ 70%

Report per-hand comparison: v2.2 vs v2.3-iter1 vs v2.3-iter2
on both FB-40 and MW-50. Show specifically:
- Which BET-miss hands from v2.2 are now correct (the
  bias-fix wins)
- Which CHECK hands that v2.3-iter1 broke are now restored
  (the balance restoration)
- Any NEW misses that neither v2.2 nor v2.3-iter1 had

### Step 5 — Stop conditions

- If FB-40 or MW-50 still below gate: STOP and report. We
  may need to prune further or adjust class weights on top.
- If Group D regresses > 1 hand: STOP. The fix is still
  too BET-aggressive.
- If BET-miss correction disappears (the original 8 MW
  misses revert to CHECK): STOP. We pruned too aggressively
  and lost the fix signal.

## Why not the other options

- **Option 1 (add CHECK hands):** weeks of labelling for
  data we don't need. v2.2 already has 131 CHECK hands —
  they're drowned, not absent. Fix is removing excess.
- **Option 2 alone (class weighting):** global weights can't
  fix a local feature-space imbalance — 5 CHECK hands vs 435
  BET hands in the bias-signature bucket means weighting
  alone can't teach the discrimination boundary.
- **Option 4 (diagnostic retrain):** root cause is diagnosed.
  62.8% BET speaks for itself.

## Deliverables

- Pruned `training-data/v2_3_training_iter2.csv` (keep iter1
  CSV for comparison)
- `river-rats-core/models/v2_3_model_iter2.json`
- `review/comms/PHASE_7_ITER2_REPORT_2026-04-17.md` with
  the 3-way per-hand comparison table
- Updated phase grid

Commit per step. Push immediately.

## Timeline

Steps 1-4 are mechanical: ~1-2 hours total. This is NOT
another labelling cycle — it's data selection + retrain +
eval. Same agent, same session.
