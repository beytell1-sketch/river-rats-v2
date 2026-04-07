# Restart Prompt — v9-3way Continuation

**Date:** 7 April 2026
**Session:** v9-3way shipped, solver verification complete

---

## Where We Are

v9-3way-v2.1 is shipped as the 3-way specialist. Solver-corrected
reference score: 33/40 (82.5%). Independent test: 41/50 (82%).

## What Was Done (6-7 April, in order)

1. **Preflop range fix** — SB cold-call blocked, ranges verified
   correct (all positions wider than GTO targets)
2. **3-way yield problem** — diagnosed as circular (HU oracle
   folds multiway), solved with all-player logging + single
   position runner
3. **10,000 deals generated** — 962 situations, 125 unique boards
4. **200 stratified selection** — labelled by calibrated GTO Expert
   (24/24 blind exam verified)
5. **v9-3way-v1** — first attempt, 50% gate (from-scratch 3-class).
   Failed due to CALL starvation + lost base knowledge
6. **Warm-start experiment** — v1 warm-start scored 60% (24/40),
   preserved SPR/nut_potential. Established warm-start as regime.
7. **SituationFactory built** — ~100 lines, board-anchored hand
   sweeps, validated with smoke test
8. **151 factory situations** — position-amplification (79) + CALL
   (72) sweeps, structurally reviewed, labelled
9. **v9-3way-v2** — warm-start, 67.5%. facing_bet dominated at 62%.
   Solver verified 3 RAISE labels were wrong → fixed to CALL
10. **v9-3way-v2.1** — FROM-SCRATCH on corrected 348 labels. 80%
    reference (32/40). facing_bet dropped to 10%. Healthy features.
11. **Leakage check** — 1 direct leak found (PA_Board2_h8 = MW-28),
    removed. Score held at 32/40.
12. **Independent test** — 50 unseen self-play hands, 82% accuracy.
    +8pp over v8.
13. **Solver verification** — 3 solves used:
    - MW-30 (KT top pair): expert FOLD wrong, solver says CALL
    - MW-46 (K7 trips): expert FOLD wrong, solver says CALL
    - MW-47 (AQs nut flush draw): expert+model CALL wrong, solver
      says RAISE (shared blind spot)
14. **Corrected score: 33/40 (82.5%)**

## Key Architectural Decisions

- **From-scratch for specialists** when base domain differs.
  Warm-start hurts (HU→3way). Retest at 3way→4way.
- **SituationFactory** over self-play for targeted data generation.
  Axis coverage matters more than volume.
- **Solver verification mandatory** on RAISE/CALL boundaries and
  any expert FOLD with equity well above pot odds.
- **Leakage check mandatory** before every gate.
- **Limped pots excluded** from scope.

## Solver-Verified Rules for Labelling

1. Non-set hands at mixed SPR: default CALL (solver mixes, model
   can't express mixed strategies)
2. Blockers swing raise frequency by 40pp — labelling agent ignores
   this entirely
3. Bottom pair with equity 5+pp above pot odds: CALL even facing
   bet+call
4. River check-raise ≠ nuts only. Trips is never a fold.
5. Nut flush draw + blocker + overcards: RAISE even OOP 3-way
   (fold equity + draw equity > flat call)
6. Expert over-folds with "action narrows ranges" heuristic.
   Verify with solver when model disagrees.

## 7 True Remaining Failures (solver-corrected)

| Hand | Expert | Model | Status |
|------|--------|-------|--------|
| MW-17 | CALL | FOLD | Model wrong — under-calling |
| MW-25 | BET | CHECK | Model wrong — residual passive |
| MW-31 | FOLD | CALL | Unverified — likely model correct |
| MW-40 | BET | CHECK | Model wrong — residual passive |
| MW-45 | RAISE | CALL | Model wrong — under-raising |
| MW-47 | RAISE* | CALL | Both wrong — shared blind spot |
| MW-50 | FOLD | CALL | Unverified — likely model correct |

*MW-47 expert was CALL, solver says RAISE

## Key Files

| File | Description |
|------|-------------|
| models/gto_model_v9_3way_v2.1.json | Production 3-way model |
| training-data/train_3way_v2.1_clean.csv | Training data (348 rows) |
| training-data/test_set_50_labelled.jsonl | Independent test set |
| training-data/3way_combined_350.jsonl | Combined labelled data |
| river-rats-core/situation_factory.py | Factory for generation |
| river-rats-core/generate_factory_situations.py | Factory runner |
| docs/POKER_TERMINOLOGY.md | Bet vs raise reference |
| review/REVIEW_V9_3WAY_V2.1_FINAL.md | Full review |

## Next Session Priorities

1. **Knowledge base update** — add solver rules (especially nut
   draw + blocker = RAISE, and over-fold bias correction) to
   three_way_gto.md before next labelling round
2. **Verify MW-31 and MW-50** — likely model correct (same pattern
   as MW-30/46). Use solver when available.
3. **Failure analysis** — group 7 ref failures + 9 test failures.
   Target types appearing in both sets.
4. **Facing-bet test set** — current independent test only covers
   CHECK/BET decisions. Need 30-50 facing-bet test hands.
5. **Blocker feature** — solver showed 40pp swing. Spec and add.
6. **Iterate v9-3way to ceiling** before starting v9-4way.

## CLAUDE.md Protocol Reminders

- Plan before build, present for review
- Leakage check before every gate
- Solver verify RAISE/CALL boundaries and expert FOLDs with
  high equity
- From-scratch is the regime for 3-way (retest at 4-way)
- Calibration exam (blind, graded) before each labelling round
