---
date: 2026-05-07
from: LEAD-PROGRAMMER (architect-hat / ml-architect-hat)
to: Future LEAD-PROGRAMMER (Phase 3 D5 execution) · Owner (DEFERRED-PARK) · Main terminal (orchestrator)
re: D5 deferred blueprint — 75+ feature surface targeting model-stuck pipeline-aligned stay-wrong (MW-40/45/47); commited-but-not-executed per Hybrid A→D5-deferred decision
status: BLUEPRINT-MEMO — parked for Phase 3 re-open; no execution this PR
---

# Phase 3 D5 deferred blueprint

## §1 Purpose

Per dispatch `MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md` (master `62eae79`, PR #301), Hybrid A→D5-deferred path commits to D5 (75+ feature surface) as the next-lever WITH BLUEPRINT, executed in a future Phase 3 dispatch when production-readiness deliverables (coaching pipeline, mobile app) progress past the user-value threshold.

This memo provides the architect-hat-ready specification for that future dispatch. It is NOT executed here. When owner directs Phase 3 D5 execution, this memo is the design starting point.

## §2 Hypothesis

**Expanding the feature surface from the unified 59-surface (Phase 1.5 base) to 75+ features targeting the structural patterns of MW-40, MW-45, MW-47 will lift the model's solver-corrected accuracy from the 33-34/40 ceiling to ≥36-37/40 by enabling the model layer to extract discriminating signal currently absent at 59-feature scale.**

**Sequencing update per `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (PR #302)**: D5 is no longer the immediate next-phase. Phase 1.5 unified-59-surface workstream comes first (drop the 2 J-B features and unify HU + 3way + experimental on a single 59-feature surface). D5 is re-sequenced as Phase 2, building on top of the unified-59 base — NOT on top of the current fragmented 38/45/61 surfaces. The 11 candidate features below target a 59 → 75+ transition (not 61 → 75+).

### Pre-experiment evidence supporting the hypothesis

1. **Stay-wrong taxonomy** (per `project_v9_3way_ceiling.md`): 3 of 4 stay-wrong (MW-40, MW-45, MW-47) are model-stuck pipeline-aligned. Pipeline labels match canonical; the model layer cannot extract the discriminating signal. This is a feature-surface-bound failure, not a labelling failure.
2. **Lever C NULL on 988-corpus** (PR #293): adding 200 hands of high-quality (20/20 Opus-validated) labelled training data targeting these axes did NOT lift mean. The signal is not in the labels — adding more labelled data on the same surface cannot teach what the surface cannot represent.
3. **12.5J-B 2-feature attempt evidence** (chosen Seed 2 of 988-corpus model): both targeted features (`nut_blocker_overcard_count` for MW-17; `bet_call_multiway_oop_raise_pressure_index` for MW-47) clocked importance < 1% (0.0091, 0.0076 respectively). The features didn't fail because feature engineering can't help; they failed because the specific 2 features chosen were under-specified composites of existing fields. A larger, structurally-targeted feature family is the natural next step.
4. **Blocker family precedent**: the v2.4 P1 blocker migration (4 features added in earlier work) produced 3 features in the chosen-seed top-5 (`nut_flush_block` 0.0527, `flush_block_pct` 0.0504, `flush_draw_block_pct` 0.0499). Targeted feature families CAN move the model when designed against the right structural axes.

### What would falsify the hypothesis

If 5+ thoughtfully-engineered candidates targeting MW-40/45/47 each clock importance < 1% AND the model fails to graduate any of the 3 stay-wrong, the model architecture (XGBoost) itself may be the binding constraint, escalating to D2 (transformer architecture) as next-lever.

## §3 Candidate features (3-7 specific candidates per axis)

ml-architect-hat suggested set; refine in Phase 3 with fresh poker-judgment review.

### §3.1 MW-40 axis (J-on-board TPMK 4-way checked-through pipeline-CHECK→canonical-BET)

The structural pattern: hero holds top-pair-medium-kicker on a J-high board in a 4-way pot with a checked-through line; canonical action is a thin value bet. Pipeline labels BET; model predicts CHECK because the feature surface doesn't represent why this specific TPMK shape merits a thin bet vs other TPMK shapes that should check.

**Candidate features**:
- `tpmk_position_with_kicker_strength` — composite: hero top-pair × kicker rank percentile (0.0-1.0) given the board high-card. Discriminates TPMK with T+ kicker (good for thin value) from TPMK with low kicker (CHECK).
- `multiway_checked_through_pot_aggression_score` — composite: pot-passed-through-N-streets × num_opponents × villain-stack-depth. Captures the "everyone passed; small thin bet wins close to N×bet equity" pattern.
- `board_J_position_interaction` — board high-card × villain-position interaction one-hot (J + UTG / J + MP / J + LP, etc.). Captures the position-specific routing for J-high boards in checked-through 4-way.

### §3.2 MW-45 axis (broadway-completed-turn multiway under-RAISE)

The structural pattern: broadway-completing turn card in a multiway pot; hero holds a strong hand that should RAISE. Model predicts CALL because the feature surface doesn't capture the broadway-completion turn dynamic vs other turn dynamics.

**Candidate features**:
- `broadway_density_completed_on_turn` — count of broadway cards on the board AFTER turn completion (0/1/2/3). Discriminates the "Q + J + T" turn (high broadway density; multiway pressure) from non-completing turns.
- `draw_completion_indicator_on_turn` — binary or 0-1 score: did the turn complete a major draw type (straight / flush / 2-pair structures) for villain ranges? Pairs with broadway density.
- `multiway_strong_hand_relative_to_completion` — interaction: hero hand strength × broadway completion. Captures the "I have a strong hand AND the board got dangerous" signal that should drive RAISE not CALL.

### §3.3 MW-47 axis (nut FD blocker on multiway should RAISE)

The structural pattern: hero holds a nut flush draw with the blocker on a 2-FD-suit board in a multiway pot facing a bet+call line; canonical RAISE. Model predicts CALL. The 12.5J-B `bet_call_multiway_oop_raise_pressure_index` was a partial attempt at this; expanding the family is the right move.

**Candidate features** (expand the `bet_call_multiway_oop_raise_pressure_index` family):
- `nut_fd_multiway_pressure_with_blocker` — separate from the original combined index: split into NFD strength × multiway pressure × hero-position one-hot. The original combined the components into a single scalar; separating lets XGBoost learn non-linear interactions.
- `nut_fd_villain_range_capped_signal` — composite: hero has nut FD + blocker × estimated villain range cap. Captures why a nut FD with a key blocker on a bet-call line should raise: villain range is capped; nut FD has fold equity + equity-when-called.
- `multiway_oop_raise_target_pot_odds_inversion` — composite: pot odds × oop position × multiway. The original `bet_call_multiway_oop_raise_pressure_index` returned 0 unless ALL gating conditions held; this version is continuous and decomposes the signal.

### §3.4 Cross-axis general candidates

- `villain_range_capped_pct_continuous` — replace the binary `villain_range_capped` (importance 0.0070 in chosen Seed 2; below 1% drop) with a continuous estimate of how capped the villain range is. The binary loses signal; the continuous version may activate.
- `hero_strength_relative_to_villain_capped_range` — interaction: hero hand strength percentile × villain-range-cap-continuous. The "I'm strong and they're capped" signal for thin value bets and raises.

**Total candidates**: 3 (MW-40) + 3 (MW-45) + 3 (MW-47) + 2 (cross-axis) = 11 candidates. Some will be redundant with existing features and dropped during implementation review (analogous to 12.5J-A's 3-candidate → 2-feature reduction).

## §4 Pre-experiment hypothesis test (gate before full investment)

Before implementing all 11 candidates and running a full multi-seed re-train, run a minimal pilot to validate D5 has signal:

### §4.1 Pilot scope

- Implement 3 candidates total: 1 from each of the 3 stay-wrong axes (the most promising per ml-architect-hat / gto-expert-hat review).
- Re-extract the 988-corpus to 64 features (61 + 3 pilot candidates).
- Train 1-seed pilot model on 988-corpus 64-features with same hyperparameters as v9-3way-v2.2.
- Evaluate on 40-hand reference set; compute per-hand solver-corrected score; check Section C feature importance for the 3 pilot candidates.

### §4.2 Pilot gate

| Outcome | Action |
|---|---|
| ≥1 of 3 pilot candidates clocks importance ≥ 2% AND ≥1 of 3 stay-wrong (MW-40/45/47) graduates on chosen seed | PROCEED to full 11-candidate D5 |
| All 3 pilot candidates < 1% importance AND no stay-wrong graduates | HALT D5; escalate to D2 (transformer architecture) consideration |
| Mixed signal (1 of 3 candidates 1-2% importance; no stay-wrong graduates) | REPORT to orchestrator; orchestrator decides expand-vs-pivot |

### §4.3 Why this pilot gate matters

The 12.5J-B 2-feature attempt failed silently — both features below 1% importance and no stay-wrong graduated. The "hypothesis test" was implicit in the full 988-corpus re-train, which was expensive ($60-70 LLM + 15h). Phase 3 D5 should NOT make that mistake. A 1-seed 3-feature pilot costs ~$0 and ~30 min; it provides the gate signal before full investment.

## §5 Cost / time forecast

### Pilot phase (Phase 3-A)
- Feature implementation: ~4-6h (3 candidates with re-extraction)
- 1-seed pilot train + reference eval: ~30 min
- Pilot report + gate decision: ~1h
- **Total**: ~$0; ~6-8h wall clock

### Full D5 phase (Phase 3-B; gated on Phase 3-A PASS)
- Implement remaining 8 candidates: ~12-16h
- 988-corpus re-extraction to 75-feature surface: ~2h
- 5-seed re-train + reference eval: ~3-4h
- Hyperparameter re-baseline (analogous to Lever B but on new surface): ~6-8h optional
- Full D5 report: ~2h
- **Total**: ~$0; ~25-30h wall clock

### Total Phase 3 D5 commitment (if pilot passes)
- ~$0 LLM (no labelling required; existing 988-corpus reused)
- ~30-40h builder wall clock
- ~3-5 PRs through the pipeline

## §6 Stop conditions and off-ramp

### Stop conditions during Phase 3-A pilot

- Trainer crashes on 64-feature surface → STOP; root-cause; halt-and-route to orchestrator.
- 988-corpus re-extraction produces NaN/Inf in any of the 3 new features → STOP; root-cause feature implementation; do NOT proceed to training until fixed.
- Reference set evaluation produces predictions for < 40 hands → STOP; pipeline integrity failure; halt-and-route.

### Stop conditions during Phase 3-B full D5

- 5-seed mean stays in the 33.0-34.0 range with no stay-wrong graduating (analogous Lever C NULL) → ESCALATE to D2 architecture consideration; D5 was the structurally-correct lever and has been falsified.
- One or more stay-wrong (MW-40/45/47) graduates BUT mean does not lift past 35/40 → REPORT; orchestrator + owner decide partial-lift acceptance vs further engineering.
- Mean lifts past 36/40 with stay-wrong graduations → PROMOTE to v9-3way-v3 production candidate; advance to next phase (gate evaluation analogous to 12.5L).

### Off-ramp

If Phase 3-A pilot HALTS with all candidates below 1% importance, the off-ramp is **D2 (transformer architecture)** as the next-lever, NOT continued tuning of D5 candidates. The pilot's purpose is precisely to make this gate empirical — if D5 has no signal at the 3-candidate scale, scaling to 11 candidates is wasted effort.

## §7 What this memo does NOT do

- ❌ Does NOT execute D5 — memo only.
- ❌ Does NOT modify v3.x prompts.
- ❌ Does NOT modify river-rats-core/ source.
- ❌ Does NOT modify BATCH2 reference labels.
- ❌ Does NOT modify the 988-corpus or any prior-phase corpus.
- ❌ Does NOT modify the v9-3way-v2.2 production model file.
- ❌ Does NOT auto-decide Phase 3 trigger timing — owner-scope per Hybrid A→D5-deferred ("when production-readiness deliverables progress past user-value threshold").

## §8 Re-open trigger

Owner directive: "execute D5 now" (or equivalent) post-coaching/mobile MVP. Phase 3 dispatch will reference this blueprint by file path. The orchestrator at re-open time will review this memo for staleness (the candidate list and feature taxonomy assumes 2026-05-07 understanding; if the model architecture, corpus, or stay-wrong taxonomy changes between now and re-open, the candidates may need refresh) and either dispatch as-is or commission a refresh.

## §9 References

- 12.5L synthesis: `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297)
- SHIP-A dispatch: `review/comms/MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md` (master `62eae79`, PR #301)
- **SHIP-A fire authorization + Phase 1.5 queue**: `review/comms/MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302) — D5 re-sequenced as Phase 2 post Phase 1.5 unified-59 ship.
- **Builder directive-receipt** (HU + unified surface + drop 2 J-B): `review/comms/BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md` (master `48297e4`, PR #300) — origin of the unified-59-surface direction.
- Stay-wrong taxonomy: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md` (this PR; owner-scope to ratify)
- Lever C NULL evidence: `review/comms/BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (PR #293)
- 12.5J-B partial-attempt evidence: `review/comms/BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md` (PR #198 era)
- v2.4 P1 blocker family precedent: `river-rats-core/feature_extractor.py` `compute_*_block*` functions
- Memory: `feedback_solver_vs_expert_labels.md` (D1 forbidden), `feedback_quality_default_no_ask.md` (committed single path; pilot-first), `feedback_pilot_first_for_long_jobs.md` (Phase 3-A pilot gate is BINDING)

---

**Status: D5 BLUEPRINT MEMO — committed-but-deferred. Phase ordering: Phase 1 SHIP-A (this PR) → Phase 1.5 unified-59-surface workstream (queued post-SHIP-A merge per PR #302) → Phase 2 D5 (this blueprint; fires post-Phase-1.5-ship). Pilot gate is BINDING; do NOT skip pilot when re-opening.**
