# v9-3way-v2.1 — Final Review

**Date:** 7 April 2026
**Status:** SHIPPED as 3-way specialist

---

## Results

| Model | Reference (40) | Independent Test (50) |
|-------|---------------|----------------------|
| v8 baseline | 23/40 (57.5%) | 37/50 (74.0%) |
| **v9-3way-v2.1** | **32/40 (80.0%)** | **41/50 (82.0%)** |

## Training

- **Regime:** From-scratch (warm-start hurts at this transition)
- **Data:** 348 situations (199 self-play + 150 factory, 1 leak removed)
- **Labels:** GTO Expert agent, 3 solver-verified corrections
- **Features:** 45 columns, balanced importance (top: bet_to_pot 10.7%)

## Verification

- Baselines confirmed in single evaluator session
- 1 direct leak found and removed (PA_Board2_h8 = MW-28)
- 3 other board overlaps verified clean (distances >0.068)
- Score held at 32/40 after leak removal
- Independent 50-hand test on unseen self-play data: 82%
- Test set validates CHECK/BET boundary only (all not-facing-bet)

## Axis Performance

| Axis | v8 | v2.1 |
|------|-----|------|
| position_amplification | 17% | **83%** |
| spr_interaction | 83% | **83%** |
| nut_potential | 67% | **83%** |
| bluff_compression | 100% | **100%** |
| combined | 50% | **75%** |
| aggression_respect | 33% | **67%** |
| range_narrowing | 50% | **67%** |

## 8 Remaining Failures

| Pattern | Count | Hands |
|---------|-------|-------|
| Over-calling (expert=FOLD, model=CALL) | 4 | MW-30, MW-31, MW-46, MW-50 |
| Residual passive (expert=BET, model=CHECK) | 2 | MW-25, MW-40 |
| Under-calling (expert=CALL, model=FOLD) | 1 | MW-17 |
| Under-raising (expert=RAISE, model=CALL) | 1 | MW-45 |

## Key Findings This Session

1. **From-scratch beats warm-start** when base model domain
   differs from specialist (HU→3way). Retest at 3way→4way.
2. **Axis coverage matters more than training regime.** Factory
   situations with deliberate SPR/position/equity variety let
   from-scratch learn what self-play alone couldn't teach.
3. **Solver verification caught 3 mislabels** (RAISE→CALL for
   non-set hands). Fixing 4 labels improved gate by +5 hands.
4. **Leakage check is mandatory.** Factory designers draw from
   the reference set unconsciously. One leak found and removed.
5. **Labelling agent has ~15% error rate** on borderline spots.
   Solver verification on RAISE/CALL boundaries is non-negotiable.

## Next Iteration Targets

1. Over-calling (4 failures) — solver-verify MW-30/31/46/50
2. Residual passive (2 failures) — more OOP thin-value-bet data
3. Facing-bet test set — validate CALL/FOLD/RAISE decisions
4. Blocker feature (bookmarked) — solver showed 40pp swing

## Files

| File | Description |
|------|-------------|
| models/gto_model_v9_3way_v2.1.json | Production model |
| training-data/train_3way_v2.1_clean.csv | Training CSV (348 rows) |
| training-data/test_set_50_labelled.jsonl | Independent test set |
| docs/POKER_TERMINOLOGY.md | Terminology reference |
