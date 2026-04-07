# Restart Prompt — v9-3way Continuation

**Date:** 7 April 2026 (end of session)
**Session:** v9-3way-v2.2 shipped, features built, ready for next factory batch

---

## Where We Are

**v9-3way-v2.2 is the production 3-way specialist.**
- Reference: 32/40 (80% raw), **33/40 (82.5%) solver-corrected**
- Independent test: 41/50 (82%) on unseen self-play hands
- v8 baseline: 23/40 (57.5%). Improvement: +10 hands.
- Trained from-scratch on 348 situations, 45 features
- 3 new features built (48 total) but need 600+ samples to activate

## What Was Done (6-7 April, in order)

1. **Preflop range fix** — SB cold-call blocked, ranges verified
   correct (all positions wider than GTO targets)
2. **3-way yield problem** — diagnosed as circular (HU oracle
   folds multiway), solved with all-player logging + single
   position runner (6x speedup)
3. **10,000 deals generated** — 962 situations, 125 unique boards
4. **200 stratified selection** — labelled by calibrated GTO Expert
   (24/24 blind exam verified, graded against answer key)
5. **v9-3way-v1** — from-scratch 3-class, 50% gate. Failed: CALL
   starvation + lost base knowledge
6. **Warm-start experiment** — 60% (24/40). Preserved SPR but
   facing_bet dominated at 63%. Established that warm-start from
   HU base hurts.
7. **SituationFactory built** — ~100 lines, board-anchored sweeps
8. **151 factory situations** — position-amplification (79) + CALL
   (72), structurally reviewed, 3 fixes applied, labelled
9. **Solver verification (3 solves used):**
   - MW-30 KT top pair: expert FOLD wrong → CALL (model correct)
   - MW-46 K7 trips: expert FOLD wrong → CALL (model correct)
   - MW-47 AQs nut flush draw: both CALL wrong → RAISE (shared blind spot)
10. **Label corrections:** 3 RAISE→CALL (solver: non-sets mix at
    SPR), 1 FOLD revert (6c5c bottom pair — expert reasoning valid)
11. **v9-3way-v2 warm-start** — 67.5%, facing_bet at 62%. Broken.
12. **v9-3way-v2.1 from-scratch** — 80% (32/40). facing_bet 12%.
    Leakage check: 1 leak found (PA_Board2_h8), removed, score held.
13. **v9-3way-v2.2** — facing_raise bug fixed (100 situations
    corrected), retrained, 80% confirmed. Production model.
14. **3 new features built** (45→48):
    - `flush_block_pct`: range-aware flush combo blocking (0.0-1.0)
    - `overcard_outs`: hero overcards × 3 (0/3/6)
    - `improvement_probability`: fraction of cards improving to 2pair+
    - At 349 samples: only improvement_probability shows signal (1.1%)
    - flush_block_pct and overcard_outs need 600+ samples
15. **v3 tested with 48 features** — no improvement over v2.2.
    Data ceiling, not feature ceiling. v2.2 stays production.

## Key Architectural Decisions

- **From-scratch for specialists** when base domain differs (HU→3way).
  Warm-start hurts. Retest at 3way→4way.
- **SituationFactory** over self-play for targeted data.
  Axis coverage > volume.
- **Solver verification mandatory** on RAISE/CALL and expert FOLDs
  with high equity.
- **Leakage check mandatory** before every gate.
- **Limped pots excluded.** Oracle always plays opened pots.
- **Blind calibration exam** (graded against answer key, no access
  to answers) before each labelling round.
- **Don't patch individual failures.** Add features or training
  volume that teach general principles.

## Solver-Corrected Reference Labels

See `memory/reference_corrections.md` for full details.

| Hand | Original | Solver | Impact |
|------|----------|--------|--------|
| MW-30 | FOLD | **CALL** | Model was right |
| MW-46 | FOLD | **CALL** | Model was right |
| MW-47 | CALL | **RAISE** | Both wrong — shared blind spot |
| MW-31 | FOLD | likely CALL | Unverified, same pattern |
| MW-50 | FOLD | likely CALL | Unverified, same pattern |

## Labelling Agent Known Biases

1. **Over-folds** with "action narrows ranges" heuristic
2. **Ignores blockers** — solver shows 40pp swing from suit holdings
3. **Over-applies "don't semi-bluff 3-way"** — nut draws with
   blockers should RAISE even 3-way OOP
4. **Uses worse_hand_pct as raise signal** — wrong, blockers drive it
5. **Knowledge base needs updating** with solver rules before next
   labelling round (especially semi-bluff carve-out)

## 5 True Remaining Failures (solver-corrected)

| Hand | Pattern |
|------|---------|
| MW-17 | Under-calling (low equity draw) |
| MW-25 | Residual passive (thin value bet) |
| MW-40 | Residual passive (very thin value bet) |
| MW-45 | Under-raising |
| MW-47 | Shared blind spot (nut draw should raise) |

Plus MW-31, MW-50 (unverified, likely model correct).

## Next Session Priorities

1. **Update knowledge base** — add solver rules to three_way_gto.md:
   - Nut draw + blocker = RAISE even 3-way OOP
   - Non-set hands MIX raise/call (default CALL)
   - Over-fold bias correction
   - Semi-bluff conditions in multiway

2. **Research semi-bluff situations** — what boards/hands/conditions
   make semi-bluffing profitable 3-way. Design factory situations
   that include semi-bluff opportunities.

3. **Design next factory batch** — 250-300 situations targeting:
   - Broad distribution (not patch fixes)
   - Semi-bluff spots (test if expert identifies them)
   - Flush-blocking situations (activate the feature)
   - Overcard situations (activate the feature)
   - Diverse boards, positions, streets

4. **Solver verify** borderline semi-bluff labels before training

5. **Retrain v9-3way-v3** on ~600 situations with 48 features
   - Expect flush_block_pct and overcard_outs to activate
   - Gate: >= 32/40 reference, feature importance check

6. **Iterate to ceiling** before starting v9-4way

## Phase Sequence

- Phase A: v9-3way **SHIPPED (82.5%)** — iterate to ceiling
- Phase B: Preflop range fix — steps 5-7 pending
- Phase C: Teaching system — GATED on 80%+ (**GATE MET**)
- Phase D: Human testing

## Key Files

| File | Description |
|------|-------------|
| models/gto_model_v9_3way_v2.2.json | Production 3-way model (45 feat) |
| training-data/train_3way_v2.2.csv | Training data (348 rows, 45 feat) |
| training-data/train_3way_v3_48.csv | Training data (349 rows, 48 feat) |
| training-data/3way_combined_350.jsonl | Combined labelled data |
| training-data/test_set_50_labelled.jsonl | Independent test set |
| training-data/3way_situations_10k.jsonl | 962 self-play pool |
| river-rats-core/situation_factory.py | Factory for generation |
| river-rats-core/feature_extractor.py | 48-feature pipeline |
| river-rats-core/gto_model.py | 48 FEATURE_COLUMNS |
| docs/POKER_TERMINOLOGY.md | Bet/raise/post reference |
| knowledge/three_way_gto.md | v1.1 — NEEDS UPDATING with solver rules |
| prompts/gto_labeller_v1.md | Labelling prompt |
| review/PLAN_FEATURES_45_TO_48.md | Feature plan |

## Memory Files (auto-loaded in new sessions)

| File | What it contains |
|------|-----------------|
| memory/project_river_rats_v2.md | Full project state |
| memory/feedback_solver_findings.md | 9 solver findings with rules |
| memory/reference_corrections.md | 3 verified + 2 likely label corrections |
| memory/feedback_close_hand_selection.md | Use model uncertainty, not feature stats |
| memory/feedback_compute_assumptions.md | Check for redundant compute |
| memory/feedback_units_and_dedup.md | Verify units, check inflation |

## CLAUDE.md Protocol Reminders

- Plan before build, present for review
- Leakage check before every gate
- Solver verify RAISE/CALL boundaries
- Blind calibration exam before labelling rounds
- From-scratch is the regime for 3-way
- Don't target individual failures — train general principles
- Multiple experts review, then independent final review
