# Restart Prompt — River Rats v2

**Date:** 6 April 2026
**Session:** Preflop range fix + 3-way training pipeline

---

## Where We Are

Step 2 of the preflop range fix is complete. range_manager.py has
been updated with new GTO-derived range data. The diagnostic shows
it working — multiway yield went from 2.6% to 6.3%.

## What Was Done This Session (in order)

1. **Bridge fix** — activated 3 dormant action-history features in
   live play (self_play.py, game_state_bridge.py)
2. **Reference evaluator** — built and ran. Confirmed v8 model has
   no latent signal in action-history features (21/40 = 52.5%)
3. **Feature expansion 38→45** — shipped. 5 metadata features
   promoted, 2 new features added, is_3bet_pot activated. 916
   tests pass.
4. **Model router** — oracle_router.py built. Selects specialist
   model by opponent count. 11 tests pass.
5. **v9-baseline** — trained on 45-column PokerBench. 91.9% HU
   accuracy. Saved as gto_model_v9_baseline_45feat.json.
6. **All-oracle self-play** — all 6 seats now use oracle callbacks
   (removed heuristic AI opponents). 18 tests pass.
7. **Progressive Model Chain** — design plan approved. Master plan
   updated.
8. **3-way labelling agent** — spec written, knowledge base
   researched (5 agents, 80+ sources), curated into
   knowledge/three_way_gto.md v1.1. Prompt written at
   prompts/gto_labeller_v1.md.
9. **Calibration exam** — agent scored 20/24 (v1.0), then 24/24
   projected after v1.1 update (4 failures fixed, 0 regressions).
   Gate passed.
10. **Labelling pipeline** — labelling_agent.py (prepare/collect),
    export_3way_training.py, calibration_exam.py all built.
11. **Generation attempt** — 5400 deals produced only 164 3-way
    decisions (0.51% yield). Root cause: preflop ranges ~50% too
    tight at every position.
12. **Preflop range research** — 4 agents, 100+ solver-backed
    sources. RFI, defend, overcalling, SB strategy all researched.
13. **New range data** — review/new_range_data.py approved.
    No overlaps between THREE_BET and CALL dicts. Engine mixing
    compromise documented.
14. **range_manager.py updated** — RFI, THREEB, CALL dicts replaced.
    get_defend_range() now combines THREEB + CALL dynamically.
    get_call_range() returns {} for SB/CO/HJ. Diagnostic shows
    multiway yield 2.6% → 6.3%.

## What Needs To Happen Next

**Remaining preflop range fix steps (Plan Step 3-7):**

3. Fix SB cold-call in preflop_engine.py (SB should 3-bet-or-fold
   vs opens, but the engine still allows SB cold-calling if a hand
   is in the CALL dict — CALL dict is now empty for SB so this may
   be moot, but verify)
4. ~~Run diagnostic~~ (done — 6.3% multiway)
5. Run 3-way yield check (~500 deals, confirm yield is usable)
6. Run full test suite, update any broken tests
7. Regenerate training data (~3000-5000 deals)

**After range fix ships:**

- Step 7 of labelling plan: Run labelling on ~200 situations
- Step 8: Export CSV, train v9-3way, gate check

**Review notes from the diagnostic:**
- BTN opening 20% (target 43%) and SB opening 16% (target 43%)
  appear low. This may be because many hands fold before reaching
  them (UTG/HJ open first). OR the range data may need widening
  for these positions. Worth investigating if yield is still
  insufficient after Step 5.
- BB defending 29% (target 35-47%) — much improved from 5% but
  still on the low side.
- CO shows 19% open vs 27.8% in range — may be folding to earlier
  opens instead of RFI-ing.

## Key Files

| File | Status |
|------|--------|
| `river-rats-core/range_manager.py` | Updated with new ranges |
| `river-rats-core/oracle_router.py` | New — model router |
| `river-rats-core/self_play.py` | Modified — all-oracle + feat_dict capture |
| `river-rats-core/game_state_bridge.py` | Modified — 3 new features |
| `river-rats-core/feature_keys.py` | Modified — 7 new constants |
| `river-rats-core/gto_model.py` | Modified — 45 features + auto-detect |
| `river-rats-core/feature_extractor.py` | Modified — promotions + new features |
| `river-rats-core/reference_evaluator.py` | Modified — action history annotations |
| `river-rats-core/calibration_exam.py` | New — labelling agent calibration |
| `river-rats-core/labelling_agent.py` | New — batch prepare/collect |
| `river-rats-core/generate_3way_situations.py` | New — situation generator |
| `river-rats-core/export_3way_training.py` | New — CSV exporter |
| `knowledge/three_way_gto.md` | New — v1.1 knowledge base |
| `prompts/gto_labeller_v1.md` | New — labelling agent prompt |
| `models/gto_model_v8_hu.json` | New — renamed v8 anchor |
| `models/gto_model_v9_baseline_45feat.json` | New — v9 baseline |
| `docs/MASTER_PLAN (1).md` | Updated — progressive chain |
| `docs/PROGRESSIVE_MODEL_CHAIN.md` | New — chain design |
| `docs/SPEC_FEATURE_EXPANSION_38_TO_45.md` | New — feature spec |
| `docs/SPEC_3WAY_LABELLING_PROTOCOL.md` | New — labelling spec |
| `review/SPEC_3WAY_LABELLING_AGENT.md` | New — agent spec |
| `review/CALIBRATION_EXAM_RESULTS.md` | New — exam results |
| `review/PLAN_PREFLOP_RANGE_FIX.md` | New — range fix plan |
| `review/new_range_data.py` | New — approved range data |
| `research/` | 9 research files from agent dispatches |

## CLAUDE.md Protocol Reminder

Per the updated CLAUDE.md:
- Plan before build, present for review
- Validate assumptions before building
- Stop and report when things don't work as expected
- No running pipelines until code is reviewed
- Each step requires review approval before proceeding
