---
date: 2026-05-11
from: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) · Owner (ratification) · QC stream
re: Phase 2 unified surface design — D5 blueprint refresh + 4-way feature gap analysis + new surface lock proposal + sub-phase decomposition + owner-scope items
status: DESIGN MEMO — DESIGN-ONLY per dispatch (PR #385); awaits owner ratification before Phase 2-B feature implementation pilot
---

# Phase 2 unified surface design

Per dispatch §"Scope of THIS dispatch (PR-A)" + owner direction (2026-05-11 02:30 SAST: "be careful on features and make sure we are truly ready for 4-way before building and training model"): comprehensive design memo combining D5 blueprint refresh + 4-way feature gap analysis + sub-phase plan + owner-scope items. NO build/train/corpus work in this PR.

Analog template: `PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (Phase 1.5 design memo).
Refresh source: `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (D5 blueprint per PR #302 sequencing).

## §1 — Current state attestation (post-Phase-1.5 ship)

Verified by source read (Phase 1.5 SHIP master `6961cca`):

### 1.1 Production oracle routing

`river-rats-core/oracle_router.py:34-38` `_MODEL_FILES`:

```python
_MODEL_FILES = {
    1: 'gto_model_vNext_hu_59feat.json',  # Phase 1.5-E PR-B swap
    2: 'gto_model_v9_3way.json',
    3: 'gto_model_v9_4way.json',
    4: 'gto_model_v9_5way.json',  # 5-way handles 4+ opponents
}
```

**Effective router state (verified by direct OracleRouter() instantiation):**

| Position | Filename | On disk? | n_features | n_classes | Loaded by router? |
|----------|----------|----------|------------|-----------|-------------------|
| 1 (HU) | `gto_model_vNext_hu_59feat.json` | YES (force-added 1.5-E PR-B; 2.0 MB) | 59 | 5 | ✓ LOADED |
| 2 (3-way) | `gto_model_v9_3way.json` | YES (45-feat; 3-class legacy) | 45 | 3 | ✗ silently skipped (5-class assertion fails) |
| 3 (4-way) | `gto_model_v9_4way.json` | NO (file missing) | n/a | n/a | ✗ skipped |
| 4 (5-way) | `gto_model_v9_5way.json` | NO (file missing) | n/a | n/a | ✗ skipped |

**State summary:** Only HU model is actively loaded. Per `OracleRouter._get_oracle` fallback logic, ALL multiway requests (num_opponents=2/3/4+) fall back to position 1 (vNext-HU-59). This is a substantive Phase 1.5 outcome documented in BUILDER_REPORT_PHASE15E_PR_B (§5): "fallback-to-HU path now uses vNext-HU-59 instead of v8-HU-38 (substantive quality improvement)" — but it also means **production has NO multiway specialist model in active use post-1.5-ship.**

**Architect-hat surface this as a Phase 2 starting condition:** the 4-way retrain is not "refreshing an active 4-way specialist" but "creating the first production-active 4-way specialist." Reframes scope.

### 1.2 Feature surface (post-Phase-1.5-B prune)

`river-rats-core/feature_extractor.py:1569` `FEATURE_COLUMNS` (59 entries):

- Step 1 (zero-compute, 9): street, facing_bet, pot_size, to_call, pot_odds, bet_to_pot, hero_position, villain_position, is_ip
- Step 2 (hand eval, 8): hand_category, hand_rank, is_made_hand, is_strong_made, is_monster, has_flush_draw, has_straight_draw, draw_outs
- Step 3 (board analysis, 9): is_monotone, is_two_tone, is_rainbow, is_paired, is_double_paired, connectivity_score, high_card_rank, danger_score, flush_danger
- Step 3 (cont.): straight_danger
- Step 4 (equity, 2): raw_equity, equity_vs_range
- Step 5 (range partition, 2): better_hand_pct, worse_hand_pct
- Step 6 (derived, 2): equity_margin, spr
- Step 7 (action history, 4): is_3bet_pot, villain_aggression_count, villain_checked_back, villain_call_count
- Step 8 (multiway, 1): num_opponents
- Step 10 (range-board, 5): villain_top_pair_plus_pct, villain_draw_pct, villain_air_pct, villain_range_capped, board_favour
- Step 11 (current-street action, 2): num_callers_to_bet, facing_raise
- Step 12 (46-48, 3): flush_block_pct, overcard_outs, improvement_probability
- Step 13 (49-52, 4): hero_range_percentile, has_showdown_value, villain_fold_equity_estimate, flush_draw_rank
- Step 14 (53): is_preflop_aggressor
- Step 15 (54): villain_medium_made_pct
- Step 16 (55): board_adjusted_hrp
- Step 17 (v2.4 P1 blockers, 56-59): nut_flush_block, flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct

**Total: 59 features** ✓ (matches `inference_path_59.N_FEATURES_59`).

### 1.3 Inference infrastructure

`river-rats-core/inference_path_59.py` (Phase 1.5-E PR-A; merged at master `6f61ba2`):
- Public `features_from_dict_59()` builds 59-array from feat_dict
- `oracle_router.predict()` dispatches via `oracle._n_features >= 59` → 59-path else 55-path (legacy `gto_model.FEATURE_COLUMNS`)
- Surface-size dispatch tested + backward-compat verified (23/23 tests PASS)

### 1.4 Solver-verification queue

**48 spots; HOLD-with-accepted-risk** per owner direction (2026-05-10 21:13 SAST per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`):
- 4 prior: HU-6.5 (CALL), HU-1.5-LK-10 (CALL), HU-1.4-LK-04 (CALL), HU-1.4-LK-05 (CALL)
- 44 new: from Phase 1.5-D.3 FULL labelling 44-arb adjudication (PR #362)

Recovery path: solver-verify-and-retrain-if-needed (post-ship). Not a pre-train gate.

### 1.5 12.5K experiment ceiling

Per `project_v9_3way_ceiling.md`:
- v9-3way-v2.2 = Phase 1 INTERIM ceiling (pre-1.5)
- Stay-wrong taxonomy: MW-17 pipeline-canonical mismatch; MW-40/45/47 model-stuck pipeline-aligned
- D5 deferred per blueprint memo
- Reference corrections per `reference_corrections.md`: MW-30 CALL, MW-46 CALL, MW-47 RAISE

### 1.6 4-way model history

v9-4way (45-feat) trained on PokerBench-derived data; **never refreshed since v9-3way work**; **file MISSING from `river-rats-core/models/`** at master `6961cca` (verified `ls`). Listed in `_MODEL_FILES` but unloaded — historical artifact reference only.

**Phase 2 4-way path is greenfield** for production model artifact (not a refresh).

### 1.7 Pre-Phase-2 incidentals (deferred from 1.5-E §"Post-ship items")

- Design memo §4.6 footnote (v8-HU baseline 18/30 vs projected 26-28/30) — minor doc edit
- HU-6.5 corpus-exclusion-gap (model-stuck on HU-6.5; no training lookalikes) — corpus design refinement

Architect proposes folding both into Phase 2 (see §6 owner-scope) rather than pre-Phase-2 small PRs (avoids context-switch).

## §2 — D5 blueprint refresh

Source: `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (master `a382fa2`). 11 candidates targeting MW-40 (3) + MW-45 (3) + MW-47 (3) + cross-axis (2).

### 2.1 Validity assessment (post-Phase-1.5 ship)

**Hypothesis still valid:** ✓
- Stay-wrong axes MW-40/45/47 unchanged in production (vNext-HU-59 didn't address these; HU vs multiway distinct)
- Lever C NULL evidence still load-bearing (PR #293)
- 12.5J-B 2-feature attempt evidence still relevant
- Blocker family precedent (4 features in v2.4 P1) still relevant

**Pilot gate still valid:** ≥1 of 3 candidates ≥2% importance + ≥1 stay-wrong graduation. No change recommended.

**Reference corrections applied:** per `reference_corrections.md` MW-30 CALL, MW-46 CALL, MW-47 RAISE — already baked into the 988-corpus + reference set; no D5 candidate change needed.

### 2.2 Candidate freshness check

Re-validating each of the 11 candidates:

| Axis | Candidate | Status | Notes |
|------|-----------|--------|-------|
| MW-40 | tpmk_position_with_kicker_strength | KEEP | Composite still relevant |
| MW-40 | multiway_checked_through_pot_aggression_score | KEEP | Composite still relevant |
| MW-40 | board_J_position_interaction | KEEP | One-hot still relevant |
| MW-45 | broadway_density_completed_on_turn | KEEP | Count of broadway cards on turn |
| MW-45 | draw_completion_indicator_on_turn | KEEP | Binary draw-completion signal |
| MW-45 | multiway_strong_hand_relative_to_completion | KEEP | Interaction; relevant |
| MW-47 | nut_fd_multiway_pressure_with_blocker | KEEP | Decomposition of 12.5J-B failed composite |
| MW-47 | nut_fd_villain_range_capped_signal | KEEP | Composite range-cap signal |
| MW-47 | multiway_oop_raise_target_pot_odds_inversion | KEEP | Continuous version of binary failure |
| Cross | villain_range_capped_pct_continuous | KEEP | Replace existing binary with continuous |
| Cross | hero_strength_relative_to_villain_capped_range | KEEP | Interaction with continuous range cap |

**No drops or modifications recommended.** All 11 candidates carry forward to Phase 2.

### 2.3 Pilot gate refresh

Per blueprint §4.2:

| Outcome | Action |
|---------|--------|
| ≥1 of 3 pilot candidates clocks importance ≥ 2% AND ≥1 of 3 stay-wrong (MW-40/45/47) graduates on chosen seed | PROCEED to full 11-candidate D5 |
| All 3 pilot candidates < 1% importance AND no stay-wrong graduates | HALT D5; escalate to D2 (transformer architecture) |
| Mixed signal | REPORT to orchestrator; orchestrator decides expand-vs-pivot |

**No change recommended.** Pilot gate is committed + binding.

### 2.4 Falsification criterion

Per blueprint §2: "If 5+ thoughtfully-engineered candidates targeting MW-40/45/47 each clock importance < 1% AND the model fails to graduate any of the 3 stay-wrong, the model architecture (XGBoost) itself may be the binding constraint, escalating to D2 (transformer architecture)."

**Still valid.** D2 escalation off-ramp per §6 of D5 blueprint.

## §3 — 4-way feature gap analysis

Owner-surfaced concern (2026-05-11 02:25 SAST): **"players left to act is a big driver"** in 4-way decisions.

### 3.1 Independent verification of orchestrator's first-pass gap analysis

Orchestrator (in dispatch §3) flagged:
- ❌ No explicit `players_to_act_after_hero`
- ❌ No `hero_action_index`
- ❌ No `live_aggressors_behind`

**Architect-hat verified (by FEATURE_COLUMNS read):** all 3 absent from current 59-surface. Confirmed gaps.

### 3.2 Extended architect+gto-expert-hat survey

Beyond "players left to act," surveying ANY 4-way-specific decision-class where GTO requirements diverge from HU/3-way:

#### 3.2.1 Range-cap dynamics (multiway range narrowing is harder)

In HU/3-way, `villain_range_capped` (binary) + `villain_top_pair_plus_pct` capture range structure adequately. In 4-way+, multiple villain ranges interact:
- Each callers' range narrows independently per their action history
- Behind villains have wider ranges (haven't acted) than already-called villains
- The aggregate "villain range" abstraction (used in `villain_top_pair_plus_pct` etc.) may collapse 4-way distinct-villain signal

**Candidate gap:** `range_dispersion_4way` — measure of how DIFFERENT the per-villain ranges are (4-way pots have higher range dispersion than HU/3-way; signals when range-aggregate features are unreliable).

#### 3.2.2 Pot equity vs equity-when-called (multiway changes the calculus)

In HU, `equity_vs_range` and `raw_equity` are roughly the same calculation. In 4-way:
- Pot equity (vs the field) can be high but equity-when-called (vs the range that would call a bet) can be much lower
- The model's `equity_vs_range` may be computed against a single-villain assumption that underestimates the 4-way "lots of fold equity if I bet small; lots of equity-collapse if anyone calls" dynamic

**Candidate gap:** `multiway_equity_realization_factor` — adjust raw_equity by num_opponents-derived realization factor (HU≈1.0; 4-way≈0.7-0.8); captures the well-known "equity is much harder to realize in multiway" effect.

#### 3.2.3 Position pressure asymmetry

In HU, `is_ip` captures position adequately. In 4-way:
- Hero EP (UTG, MP) faces 3 villains who ALL act after; CO faces 1 (BTN); BTN faces 0
- The asymmetry of "how much pressure can be applied behind hero" varies dramatically across position; current `is_ip` (binary) loses this signal

**Candidate gap:** Confirms orchestrator's `players_to_act_after_hero` is exactly this signal. KEEP.

#### 3.2.4 Bet-call chain dynamics

Current `villain_call_count` aggregates calls but doesn't distinguish:
- "1 villain bet, 2 villains called → 4-way pot to hero" (sticky range; calls are committal)
- "2 villains checked, 1 villain bet → hero faces 1-bet line" (different pressure)

In 4-way+ these are very different decisions; the aggregate count loses the structure.

**Candidate gap:** `bet_call_chain_signature` — categorical or one-hot of recent action sequence (e.g., "X-X-B"; "B-C-X"; "C-B-C"). May overlap with `bet_call_multiway_oop_raise_pressure_index` from D5 §3.3 but distinct in scope (general multiway vs specific MW-47 axis).

#### 3.2.5 Hero range ASYMMETRY (multiway changes hero's range too)

`hero_range_percentile` (feature 49) is correctly normalized but doesn't condition on num_opponents. In 4-way:
- A given hero hand has a different percentile in a 4-way OOP-defended preflop range than in a HU isolation-call range
- The model can implicitly learn this from the (hero_range_percentile, num_opponents) interaction — if it has the data — but XGBoost may need explicit interaction

**Candidate gap:** `hero_range_percentile_x_num_opponents` — explicit interaction (multiplication or one-hot bins). Low-cost addition.

### 3.3 Proposed 4-way candidates (final list)

Combining orchestrator's 3 + architect's 4-survey:

| # | Candidate | GTO theory | Falsification | Source |
|---|-----------|------------|---------------|--------|
| 1 | `players_to_act_after_hero` | EP > MP > LP pressure asymmetry; behind-villains can squeeze | If <2% importance + no 4-way close-hand graduation | Orchestrator first-pass + arch §3.2.3 |
| 2 | `hero_action_index` | Hero's ordinal in current street action sequence; captures "first-to-act in 4-way is hardest" | If <2% importance + no improvement on 4-way action-position-sensitive close hands | Orchestrator first-pass |
| 3 | `live_aggressors_behind` | Captures squeeze risk; behind-villains who haven't folded yet | If <2% importance + 4-way squeeze-position spots show no graduation | Orchestrator first-pass |
| 4 | `multiway_equity_realization_factor` | Adjust raw_equity for known multiway realization difficulty (HU≈1.0; 4-way≈0.7-0.8) | If <1% importance + 4-way thin-equity decisions show no graduation | Architect §3.2.2 |
| 5 | `range_dispersion_4way` | Measure of per-villain range divergence; signals when aggregate features fail | If <1% importance + 4-way decisions vs 3-way decisions show no differential improvement | Architect §3.2.1 |
| 6 | `bet_call_chain_signature` | Categorical action-sequence; distinguishes "X-X-B" vs "B-C-X" 4-way structures | If <1% importance + 4-way chain-sequence-sensitive close hands show no graduation | Architect §3.2.4 |
| 7 | `hero_range_percentile_x_num_opponents` | Explicit interaction for hero range conditioned on opponent count | If <0.5% importance + no improvement on hero-range-sensitive 4-way close hands | Architect §3.2.5 |

**Total 4-way candidates: 7** (analog to D5's 11 per-axis structure).

## §3.X — 4-way street distribution analysis (per AMENDMENT 1; PR #386)

Owner direction (2026-05-11 02:55 SAST): "a lot of 4 way action is bound to be preflop and flop. can the plan account for this?"

### 3.X.1 GTO + empirical fold-out evidence

Architect-hat + GTO-expert-hat assessment of street distribution of true-4-way decisions:

- **Preflop**: 4-way pots arise commonly via limped pots, multi-way iso/cold-call sequences, squeezes that don't take it down. Pot is genuinely 4-way at hero's preflop decision moment in a meaningful fraction of multiway scenarios.
- **Flop**: After preflop limp/iso/squeeze that goes 4-ways to the flop, hero's flop decision is genuinely 4-way until the first villain folds. Many spots collapse here (passive flops where 1-2 villains fold to small c-bets).
- **Turn**: By turn, most 4-way preflop pots have collapsed to 2-3-way. "True 4-way turn" requires all 4 players to have called all flop action — uncommon outside of low-stakes passive games, multi-way slowplays, or wet boards where multiple players have draws.
- **River**: Very rare — 4-way rivers are usually all-checked-down or all-allin scenarios; live decisions are minimal.

**Architect-committed estimate (no empirical study; theory-grounded; subject to refinement during 2-D reference-set design via PokerBench multiway data filtering):**

| Street | True-4-way decision fraction | Confidence |
|--------|------------------------------|------------|
| Preflop | ~30-35% | MEDIUM (depends heavily on game type/stakes; assumes typical online 100bb cash) |
| Flop | ~50-55% | HIGH (canonical heaviest concentration per multiway theory) |
| Turn | ~10-12% | MEDIUM (collapse rate varies) |
| River | ~3-5% | HIGH (rare by all sources) |

If empirical PokerBench filtering during 2-D shows materially different distribution, architect commits to refresh.

### 3.X.2 Implication for 4-way reference set design (2-D scope)

HU pattern was 30 hands × 6 axes evenly distributed across streets — appropriate for HU. **4-way SHOULD NOT mirror this evenly** (would over-sample turn/river decisions where 4-way is rare in practice, training/eval signal misaligned with production usage).

**Architect proposal for 4-way reference set distribution (35-hand reference; weighted per §3.X.1):**

| Street | Hand count | % | Notes |
|--------|-----------|---|-------|
| Flop | 18 | 51% | Heaviest concentration; covers c-bet defend, multi-way check-raise, donk-lead with draws, set vs multiway, etc. |
| Preflop | 11 | 31% | Limp/iso/cold-call/squeeze decision classes |
| Turn | 4 | 11% | When 4-way persists to turn (wet boards; slowplay) |
| River | 2 | 6% | Rare 4-way river scenarios (multi-way checked-down nut hand thin value, multi-way bluff-catch) |
| **Total** | **35** | **100%** | Slightly larger than HU 30 (more decision-classes per axis in multiway) |

### 3.X.3 Implication for 4-way lookalike corpus (2-E scope)

Lookalike generator (analog to `scripts/generate_hu_situations.py`) MUST:
- Filter for genuinely-4-way-at-decision spots (not 4-way preflop pots that collapsed)
- Weight per-axis lookalike generation toward preflop + flop (~35 + ~18 = 53 of 35 anchors are flop/preflop; ~530 + ~280 = ~810 lookalikes from those vs ~120 from turn + ~60 from river → ~970 total at 25× density; or refine per architect-call)

**True-4-way definition**: pot is genuinely 4-way at decision moment AND no players have folded between hero's decision and the prior bet/raise sequence. Disqualifies 4-way preflop pots that have folded to 2-way before flop.

If using existing PokerBench multiway data (4-way category): filter to actually-4-way-at-decision spots; document per-street volume after filtering. If volume insufficient (e.g., <50 4-way river decisions in PokerBench), architect surfaces for owner decision (own-data generation OR accept lower density on rare-street tail).

### 3.X.4 Implication for feature surface (§3 + §3.Y candidates)

Several candidates are essentially preflop/flop-only relevant:
- `players_to_act_after_hero` (§3.3 #1): differential 0-vs-3-behind largest preflop + flop
- `live_aggressors_behind` (§3.3 #3): mostly preflop + flop (turn/river unlikely to have 3 live aggressors behind)
- `live_raisers_behind` (§3.Y candidate): preflop + flop dominant
- `closing_action` (§3.Y candidate): every street, but most discriminating preflop where action sequence is longest
- `squeeze_risk_index` (§3.Y candidate): preflop + flop dominant

Architect surfaces this to ML-architect-hat for pilot evaluation: importance score is per-street-weighted; a feature scoring 1.5% globally but 4% on preflop+flop is more relevant than the global score suggests. Pilot report should break down per-street importance.

### 3.X.5 Implication for 4-way ship gate (§5 + §6.6)

35-hand reference scoring should weight per street distribution to match production usage. Three options:

**Option A:** Weighted total: each hand contributes its street-fraction to the score (preflop+flop hands ≈82% of weight; turn 11%; river 6%). Ship gate ≥ X/35 where X is calibrated against weighted total.

**Option B:** Per-street gates: flop ≥17/18, preflop ≥10/11, turn ≥3/4, river ≥1/2 (architect-illustrative). Stricter; explicit per-street.

**Option C:** Unweighted total (analog to HU 28/30): simplest; ignores street distribution at scoring time. Architect: NOT recommended; misaligned with production usage.

**Architect proposal:** Option A (weighted total) with per-street auxiliary reporting. Owner ratifies.

### 3.X.6 Implication for v9-4way model post-ship behavior

Model will see mostly preflop + flop 4-way at runtime. Training corpus + reference set + ship gate ALL must reflect this. The risk to mitigate: a 4-way model that optimizes for turn/river 4-way at expense of flop accuracy is wrong-loss-weighted. Architect's per-street weighted reference + per-street weighted ship gate captures this constraint structurally.

## §3.Y — Re-raise × players-left interaction analysis (per AMENDMENT 2; PR #387)

Owner direction (2026-05-11 02:58 SAST): "do we know when a pot is re raised? with players left to act?"

### 3.Y.1 GTO theory of squeeze-risk in 4-way

- **Facing re-raise with N players behind = squeeze potential.** Hero's calling range MUST tighten as N grows. Standard GTO: hero opens 25%, faces 3-bet → defends 50% HU; 35% in 4-way (not 50%) because the 2-3 players behind can squeeze with wide ranges, putting hero in spot-with-no-equity-to-call-twice.
- **Reverse-implied-odds**: calling a re-raise OOP with 2+ players behind = bad position post-flop + risk of being bet-into multiway. Need premium hands to call (vs HU where bluff-catching range is wider).
- **Closing-action flag**: hero last to act = no squeeze risk = decision tree is binary fold/call (or jam) without future-action complexity. The same hand that's a CALL when closing is a FOLD with players behind.
- **4-way is where this matters most**: HU has no "behind" players; 3-way is mild (1 behind); 4-way is severe (2-3 behind).

### 3.Y.2 Independent verification of orchestrator's gap analysis

Verified by source read (`feature_extractor.py` Step 7 + Step 11):

- ✓ `_num_raises` is METADATA-ONLY (not in FEATURE_COLUMNS); model cannot consume escalation level
- ✓ `is_3bet_pot` is preflop-only binary; no `is_4bet_or_higher`
- ✓ No `closing_action` flag
- ✓ No `squeeze_risk` / `live_raisers_behind` features
- ✓ `villain_aggression_count` (Step 7) is aggregate, not escalation-level

**Gap confirmed.** Orchestrator's first-pass identifies real architectural absence.

### 3.Y.3 Candidate features (architect proposal; collinearity-aware)

| # | Candidate | GTO theory | Falsification | Collinearity check |
|---|-----------|------------|---------------|---------------------|
| 8 | `street_raise_count` | Continuous escalation level (0/1/2/3+); replaces binary `facing_raise` | If <1% importance + close-hand on 4-bet pots show no graduation | Low; richer than existing binary |
| 9 | `is_4bet_or_higher_pot` | Preflop or current-street binary; complements `is_3bet_pot` | If <0.5% importance + 4-bet pot decisions show no graduation | Mid (overlaps with #8); architect picks one OR designs as interaction |
| 10 | `live_raisers_behind` | Behind-hero villains who could still raise | If <1% importance + squeeze-risk close hands show no graduation | HIGH with §3.3 #3 `live_aggressors_behind`; architect designs as MUTUALLY EXCLUSIVE pick (raisers OR aggressors; not both) |
| 11 | `closing_action` | Hero last to act this street; turns off squeeze risk | If <1% importance + closing-action vs early-action close-hand pairs show no differential | Low; orthogonal to other candidates |
| 12 | `squeeze_risk_index` | Composite: live_raisers_behind × pot-already-raised × pot/stack ratio | If <0.5% importance + squeeze-risk close hands show no graduation | HIGH with #10 (decomposed elements); architect picks composite OR atomic decomposition (not both) |
| 13 | `reverse_implied_odds_signal` | Composite: facing_raise × OOP × players_behind × pot_committed_pct | If <0.5% importance + RIO-class close hands show no graduation | Mid (composes existing + §3.3 features); pick if pilot evidence on simpler features marginal |

**Architect collinearity-resolution recommendation (for pilot 2-B):**
- Of {#10 `live_raisers_behind`, §3.3 #3 `live_aggressors_behind`}: pick **`live_raisers_behind`** (more discriminating per amendment GTO theory; aggressors-behind subsumes raisers-behind only if aggressor includes non-raiser callers, which is the wrong abstraction)
- Of {#12 `squeeze_risk_index` composite, #10 atomic decomposition}: pick **#10 atomic** for pilot — XGBoost can learn the interaction; if pilot shows the atomic isn't enough, escalate to composite in 2-C
- Of {#8 `street_raise_count`, #9 `is_4bet_or_higher_pot`}: pick **#8 continuous** — richer signal; XGBoost handles continuous well

**Net post-resolution: 4 of 6 candidates carry forward** (drop #9 + #12 in favor of #8 + #10 atomic; #11 + #13 carry independently).

### 3.Y.4 Pilot inclusion (Phase 2-B)

Per amendment §"Pilot inclusion": include AT LEAST ONE re-raise-interaction feature in the 6-candidate pilot.

**Updated pilot pick (revising §3.4 mandatory pick 3):**
- Mandatory pick 1: `players_to_act_after_hero` (§3.3 #1 — owner-direct)
- Mandatory pick 2: `multiway_equity_realization_factor` (§3.3 #4 — cleanest GTO theory)
- **Mandatory pick 3: `closing_action` (§3.Y #11 — re-raise × players-left interaction; orthogonal to #1/#2; binary cheap-to-implement)**

`live_aggressors_behind` (§3.3 #3) is moved to 2-C full-impl phase per collinearity-resolution.

### 3.Y.5 Implication for 4-way reference set (2-D)

Per amendment §"Implication for 4-way reference set design":

- Reference hands MUST include 4-way 3-bet pots + 4-way 4-bet pots (where re-raise level + players behind is MAXIMAL)
- Reference hands MUST include closing-action vs early-action variants of similar spots (model must differentiate)
- Per §3.X street weighting: 3-bet/4-bet pots are mostly preflop; aligns with the ~31% preflop allocation

Architect commits to including these axes in 2-D reference design.

### 3.Y.6 Implication for ship gate (§5)

Per amendment §"Implication for ship gate":

- Per-hand stay-wrong taxonomy in 2-G should classify misses by whether re-raise × players-left was the discriminating signal that the model failed to extract
- Architect proposes diagnostic categorization in 2-G builder report (analog to `project_v9_3way_ceiling.md` taxonomy: pipeline-canonical-mismatch vs model-stuck-pipeline-aligned)

### 3.Y.7 Total amendment-2 candidates added: 4 (post-collinearity-resolution)

(Started from 6 raw; dropped #9 + #12 per collinearity; net 4: #8, #10, #11, #13.)

## §X — 4-way labeller-prompt readiness (per AMENDMENT 3 item 1; PR #389)

Owner direction (2026-05-11 03:05 SAST): "does the plan include research session to make sure we can prompt labelers correctly on 4 way pots?"

### X.1 Background — HU labelling incident

Per `BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md` (PR #354): Phase 1.5 HU labelling experienced systemic methodology violations — FL4 wrote a Python rule-based scoring script; FL1/2/3/5 used template-based reasoning. Recovery (PR #357 AMENDMENT) required EXPLICIT anti-rule-based prompt boilerplate, validated by FL6+FL7-10 producing varied per-spot LLM reasoning at 696-spot scale.

**Memory rule from incident** (per `feedback_solver_vs_expert_labels.md` + `feedback_bucket_first_labelling.md`): labelling-pipeline subagent dispatches MUST include explicit "no Python scoring functions; per-spot LLM reasoning required" boilerplate. STANDING RULE for all future labelling.

### X.2 4-way labelling complexity vs HU

| Dimension | HU (1 villain) | 4-way (3 villains) | New brief content needed |
|-----------|----------------|---------------------|--------------------------|
| Range tracking | 1 villain range | 3 distinct narrowed-by-own-action ranges | Multiway range-chain reasoning |
| Players-left-to-act | N/A (closing always) | Variable per position (0-3 behind) | Per-spot enumeration of behind-villains + squeeze risk |
| Squeeze pressure | None | Active (re-raise × behind-villain) | Per-spot reasoning about squeeze potential |
| Closing-action vs early | Same hand always closes | Differential decision tree | Brief MUST distinguish closing/early action trees |
| Pot-cascade | Static (HU stays HU) | 4-way → 3-way → HU progression | Brief: reassess if villain folds |
| Range-chain narrowing | Single chain | Per-villain chains | Reference `range_narrowing.py` MULTIWAY path |

Naive HU brief reuse → labels miss multiway dimensions → bad model.

### X.3 4-way labeller brief design proposal

Extend HU brief with new sections:
1. **Multiway range-chain reasoning**: per-villain narrowing
2. **Players-left-to-act + squeeze-pressure prompt**: per-spot enumeration
3. **Closing-action vs early-action decision tree**: per-spot identification
4. **Anti-rule-based boilerplate** (MANDATORY per memory STANDING RULE)
5. **Bucket-first compliance** (per `feedback_bucket_first_labelling.md`)

### X.4 Calibration set design for 4-way

HU calibration was 28 hands. 4-way needs broader axis coverage:
- Preflop axis: limp/iso/cold-call/squeeze (~6 hands)
- Flop 4-way: c-bet defend / multi-way check-raise / donk-lead / set vs multiway (~8 hands)
- 3-bet pot 4-way (~4 hands)
- 4-bet pot 4-way (~2 hands)
- Closing-action variants (~4 hands)
- Turn 4-way (~3 hands)
- River 4-way (~2 hands)

**Architect proposal: 29-hand calibration set** (analog to HU 28; +1 for axis breadth). 5 reversal anchors must-pass-100% covering preflop squeeze, flop multi-way check-raise, closing-action river bluff-catch, 3-bet pot RAISE, 4-bet pot CALL — designed in 2-E.0.

### X.5 5-hand pilot validation (NEW sub-phase 2-E.0)

Per amendment + `feedback_pilot_first_for_long_jobs.md` STANDING RULE: 5-hand pilot before full pipeline (~$120-150 LLM + 25-40h).

**Sub-phase 2-E.0 — 4-way labeller readiness:**
- Deliverables: 4-way labeller brief + 29-hand calibration set + 5-hand pilot spots
- Run 1 fresh Sonnet labeller on 5 pilot spots (sample-check)
- **STOP-condition gate**: naive HU-style reasoning OR rule-based shortcuts OR template patterns → REPORT before scaling; re-design brief; re-pilot
- **PASS-condition gate**: 5/5 spots have varied per-spot multiway-aware reasoning (range-chain, squeeze, closing-action) → proceed to full 2-E

**2-E.0 inserts BEFORE 2-E in §5 sub-phase decomposition.**

### X.6 Cost-benefit

Pilot cost: <$5 + ~30min. Full pipeline cost: ~$120-150 + 25-40h. The Phase 1.5 FL4 incident demonstrated naive labelling at scale produces unrecoverable cost; 2-E.0 prevents recurrence at 4-way scale.

## §Y — 5-way scope decision (per AMENDMENT 3 item 2; PR #389)

Owner direction (2026-05-11 03:05 SAST): "is it worthwhile to consider covering 5 and 6 way models now or keep separate?"

### Y.1 State assessment

`oracle_router.py:34-38` `_MODEL_FILES` position 4 (`gto_model_v9_5way.json`) is the **catch-all for ALL pots with 4+ opponents** (5/6/7/8/9-way). Single model handles all >= 5-way.

**Verified file state**: `gto_model_v9_5way.json` is **MISSING** from disk at master `6961cca`:
- Listed in `_MODEL_FILES` but never present in `river-rats-core/models/`
- Per `oracle_router._load_models`: silently skipped
- Per `_get_oracle(num_opponents=4+)`: falls back to position 1 (vNext-HU-59 post-Phase-1.5-E)

**Effective state**: 5+way runtime requests fall back to vNext-HU-59. 5-way "specialist" never had a production artifact in current era.

### Y.2 Frequency in production

- PokerBench-derived multiway data: not surveyed (architect estimates 5+way < 10% of multiway data in typical online cash)
- Coaching/mobile-app usage: depends on game format. Architect estimates **<5% of production usage** for typical online cash app target.

### Y.3 Surface implication if 5-way included

- Same 74-80 feature surface (no fork; `inference_path_59` extends to surface-size dispatch per §4.3)
- `players_to_act_after_hero` cardinality goes 0-3 (4-way) → 0-8 (9-way); features scale
- 5+way reference set required (~20 hands; smaller than 4-way 35 due to lower coverage need)

### Y.4 Corpus implication

- 5+way fresh labelling: §X labeller-readiness applies at higher scale (probably 7-hand pilot)
- Cost: ~$200-300 LLM (analog scaling from 4-way's ~$120-150)
- Wall-clock: +~30-50h on top of Phase 2 4-way

### Y.5 Architect proposal

**Option A — Include 5-way in Phase 2:**
- Pros: full chain refresh; same surface; pipeline reuse; closes catch-all gap
- Cons: Phase 2 wall-clock expands ~30-50h; 5-way usage rare (~<5%); "be careful + truly ready" mandate strains across 4-way + 5-way concurrently

**Option B — Defer 5-way to Phase 3:**
- Pros: scope discipline; 4-way ships sooner; 5-way as smaller dedicated workstream when warranted
- Cons: 5-way stays on HU-fallback routing post-Phase-2-ship; eventual Phase 3 dispatch needed

**Architect picks Option B as default** per:
- `feedback_quality_default_no_ask.md` slow/quality path: better to do 4-way RIGHT than spread thin
- `feedback_pilot_first_for_long_jobs.md`: Phase 2 already 70-110h; +5-way pushes to 100-160h
- 5-way usage rarity (<5%) means deferral has low product impact
- 5-way Phase 3 can build on Phase 2 4-way evidence (proven labeller brief, incremental extension)

**Owner-gate decision (item 9):** ratify Option B (defer to Phase 3) or override to Option A (include in Phase 2).

### 3.4 Pilot gate strategy for 4-way candidates

Per dispatch §3 "Pilot gate strategy for 4-way candidates (analog to D5 §4)":

**Proposed:** 3-candidate pilot from above 7 (analog to D5's 3 from 11). Architect picks the 3 most-promising:
- **Mandatory pick 1:** `players_to_act_after_hero` (owner-surfaced; direct evidence-of-need)
- **Mandatory pick 2:** `multiway_equity_realization_factor` (cleanest GTO theory; orthogonal to existing features)
- **Architect pick 3:** `live_aggressors_behind` (squeeze-risk capture; behavioral-distinct from #1)

**Pilot gate (analog to D5 §4.2):**

| Outcome | Action |
|---------|--------|
| ≥1 of 3 4-way pilot candidates ≥2% importance AND ≥1 4-way close-hand graduates on 4-way reference set | PROCEED to full 7-candidate 4-way |
| All 3 candidates < 1% importance AND no 4-way close-hand graduates | HALT 4-way feature work; escalate to "is the issue elsewhere" investigation (corpus quality? game-state representation? 4-way-specific architecture?) |
| Mixed signal | REPORT to orchestrator |

### 3.5 Reframing per §1.6 "greenfield" finding

Per §1.6: **production has NO active 4-way specialist** post-Phase-1.5 ship. Phase 2 4-way path is creating the first production-active 4-way oracle since v8/v9-baseline era.

**Implication:** 4-way ship gate cannot be calibrated against an existing 4-way reference baseline (the v9-4way-45feat file is missing; no current production-comparison). Need a NEW 4-way reference set (per dispatch §5 sub-phase 2-D).

## §4 — Combined surface lock proposal

### 4.1 Candidate totals

- Existing 59-feature surface (lock; no removals proposed)
- D5 (§2): 11 candidates
- 4-way (§3): 7 candidates (- 1 = `live_aggressors_behind` superseded by §3.Y `live_raisers_behind` per collinearity → 6 net)
- Re-raise × players-left (§3.Y; per AMENDMENT 2): 4 candidates net (after collinearity-resolution: dropped #9 + #12)
- **Total net candidates: 11 + 6 + 4 = 21**
- Estimated drops during 2-C implementation: 4-6 (further redundancy surfaced during code review; some composites may collapse)
- **Final estimated surface: 74-80 features** (was dispatch §4 estimate 75-80; refined per architect drop estimate; AMENDMENT 2 adds back the re-raise dimension architect originally under-counted)

### 4.2 Surface lock rationale

- Per `feedback_pilot_first_for_long_jobs.md`: pilot gate (D5 3-candidate + 4-way 3-candidate = 6 candidates total) MUST clear before implementing full 18-candidate set
- Per `feedback_quality_default_no_ask.md`: slow/quality path = pilot first; full only on clearance

### 4.3 Backward compat implications

- Phase 1.5-E PR-A `inference_path_59.py` dispatch boundary at `oracle._n_features >= 59`
- Phase 2 SHIP changes that boundary to `>= 75` (or whatever final size lands)
- Need to either (a) update `inference_path_59` to a new module/threshold, or (b) keep 59-path intact as middle tier (legacy 38/55 → 55-path; intermediate 59 → 59-path; new 75 → 75-path)

**Architect recommendation:** Option (b) — preserve 59-path as middle tier; add NEW `inference_path_75.py` (or similar) for final size. Backward compat maximized; rollback cleaner.

## §5 — Sub-phase decomposition (proposed)

Per dispatch §5 suggested structure + architect refinement:

| Sub-phase | Subject | Pilot+full | Owner-gate fires |
|-----------|---------|------------|-------------------|
| **2-A** | Architectural design memo (THIS PR) | N/A | Owner ratifies feature lock + sub-phase structure |
| **2-B** | Feature implementation PILOT (6 candidates: 3 D5 + 2 4-way + 1 re-raise) | Pilot gate per §2.3 + §3.4 + §3.Y.4 | D5 importance ≥2% AND ≥1 stay-wrong graduation; 4-way importance ≥2% AND ≥1 4-way close-hand graduation; re-raise candidate ≥1% AND closing-action vs early-action differential captured |
| **2-C** | Full feature implementation (remaining ~12 candidates) | Per-feature unit-test gate | Each feature has unit test + non-NaN/Inf assertion |
| **2-D** | 4-way reference set design (35 hands street-weighted per §3.X.2; includes 3-bet/4-bet pots + closing-action variants per §3.Y.5) | Pilot=5 hands; full=30 hands | Pilot gate; full gate; per-street distribution verified |
| **2-E** | 4-way labelling + corpus assembly (analog to 1.5-D.2 + D.3; ~750 lookalikes) | Pilot per `feedback_pilot_first_for_long_jobs.md` + per-axis QC | Per-phase QC; owner-arb adjudication for 4-way owner-arbs |
| **2-F** | 3-way re-extract + retrain on new surface (D5 path; uses existing 988-corpus) | 5-seed | Ship gate ≥36/40 (D5 hypothesis target per §2 blueprint) |
| **2-G** | 4-way retrain on new surface + new 750-corpus | 1-seed smoke + 5-seed full | Ship gate TBD per §6 owner-scope |
| **2-H** | Production swap (force-add new 3-way + 4-way models + oracle_router updates + new inference path) | n/a | Phase 2 SHIP boundary |

### 5.1 Cross-cutting work

- **Inference path infrastructure** (§4.3 Option b): NEW `inference_path_75.py` (or final-size analog) added in 2-C; surface-size dispatch in oracle_router extended; tests added
- **Pre-Phase-2 incidentals** (§1.7): folded into 2-A as informational notes (this memo); no separate PRs needed

### 5.2 Estimated wall-clock per sub-phase

| Sub-phase | Estimate | Notes |
|-----------|----------|-------|
| 2-A (this) | ~4-8h architect | Memo only |
| 2-B | ~10-15h | 6-candidate impl + 1-seed pilot + report |
| 2-C | ~15-20h | 12-candidate impl + per-feature tests |
| 2-D | ~6-10h | 30 hand designs (multi-axis) |
| 2-E | ~25-40h | 750-hand labelling pipeline (analog to 1.5-D.3) |
| 2-F | ~3-5h | 5-seed retrain on existing 988-corpus |
| 2-G | ~3-5h | 1-seed + 5-seed |
| 2-H | ~2-4h | Force-add + router swap + tests |
| **Total** | **~70-110h** | Across 7-9 PRs |

### 5.3 Critical path

- 2-A → 2-B (gate) → 2-C → 2-F (3-way retrain on D5; can validate D5 hypothesis WITHOUT 4-way work)
- 2-D + 2-E (4-way reference + corpus) can start in parallel with 2-C if 2-B clears
- 2-G depends on 2-D + 2-E + 2-C
- 2-H depends on 2-F + 2-G

Critical path total: 2-A → 2-B → 2-C → 2-F → 2-G → 2-H ≈ 40-55h sequential.
Parallelizable: 2-D + 2-E ≈ 30-50h parallel with 2-C/2-F.

## §6 — Owner-scope items to surface (architect proposes; owner ratifies)

### 6.1 Feature lock

**Architect proposal:** ratify the combined 21 candidate set (D5 §2.2 11 + 4-way §3.3 6 net + re-raise §3.Y.3 4 net); architect drops to ~15-17 implemented during 2-C per §4.1 estimate; final surface 74-80 features.

**Owner-gate decision:** APPROVE the candidate list and surface size target (or override).

### 6.2 Surface size target

**Architect proposal:** ~74-80 features (D5 11 + 4-way 6 + re-raise 4 = 21 candidates; net post-implementation drops 15-17 features added to 59-baseline).

**Owner-gate decision:** confirm or override surface ceiling.

### 6.3 Corpus origin for 4-way

**Architect proposal:** **fresh expert-labelled ~750 lookalikes** (analog to HU pattern; per `feedback_solver_vs_expert_labels.md`). Reasons:
- HU pattern proved this delivers high-quality training signal (vNext-HU at 28/30 ship gate)
- Augmenting existing PokerBench-multiway data risks the same "rule-based heuristics pretending to be expert labels" failure mode (CLAUDE.md Anti-Patterns)
- 4-way axes are decision-class-distinct from 3-way; need axis-specific reference + lookalikes (analog to HU axes)

**Owner-gate decision:** approve fresh-corpus path or override (use augmented data; would change Phase 2 scope substantially).

### 6.4 Solver-verification queue posture

**Architect proposal:** continue HOLD-with-accepted-risk per current owner direction (`feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`). Solver-verify-and-retrain-if-needed remains post-ship recovery for Phase 2 + Phase 1.5 spots both.

**Owner-gate decision:** confirm continued HOLD or pivot to drain-queue-first.

### 6.5 3-way ship gate (Phase 2-F)

**Architect proposal:** ≥36/40 per D5 blueprint hypothesis target (committed in §2 blueprint). 988-corpus + new D5 features → 5-seed ≥36/40 = D5 hypothesis confirmed.

**Owner-gate decision:** ratify ≥36/40 (or revise; e.g., ≥35/40 or ≥37/40).

### 6.6 4-way ship gate (Phase 2-G)

**Architect proposal:** **NEW gate calibration required** because 4-way has no existing baseline (§1.6 greenfield) AND must be street-weighted per §3.X.5. Architect proposes:
- 35-hand reference set street-weighted per §3.X.2 (51% flop, 31% preflop, 11% turn, 6% river)
- Ship gate Option A (per §3.X.5): weighted total ≥ 28/35 (~80%; analog to HU 28/30 = 93.3%, lowered for multiway difficulty per `project_v9_3way_ceiling.md` evidence; per-street auxiliary reporting)
- Smoke gate: 5pts below v9-3way (45-feat; current multiway-fallback after Phase 1.5-E) baseline on the new 4-way reference; calibration spike in 2-D
- Per-hand stay-wrong taxonomy in 2-G classifies misses by re-raise × players-left signal per §3.Y.6 diagnostic categorization

**Owner-gate decision:** ratify Option A weighted-total approach + ≥28/35 threshold OR specify alternative weighting/threshold.

### 6.7 Pre-Phase-2 incidentals (per §1.7)

**Architect proposal:** fold both into Phase 2 (no separate small PRs):
- Design memo §4.6 footnote → addressed informationally in this memo (§1.6 4-way greenfield finding partially captures the historical context)
- HU-6.5 corpus-exclusion-gap → defer to post-Phase-2 corpus refresh (would require re-running 1.5-D.3 with HU-6.5 lookalikes; significant scope; not pre-Phase-2 cheap-win territory)

**Owner-gate decision:** approve fold-into-Phase-2 or pivot to small-PR ship.

### 6.8 4-way labeller-prompt readiness + 2-E.0 sub-phase (per AMENDMENT 3 item 1)

**Architect proposal:** insert NEW sub-phase 2-E.0 (4-way labeller readiness) before 2-E (full pipeline) per §X.5. Deliverables: 4-way labeller brief + 29-hand calibration set + 5-hand pilot validation. STOP-condition gate prevents naive HU-style reasoning from cascading to full pipeline.

**Owner-gate decision:** ratify 2-E.0 insertion + 5-hand pilot gate (or override calibration set size / pilot scope).

### 6.9 5-way scope decision (per AMENDMENT 3 item 2)

**Architect proposal:** **Option B — Defer 5-way to Phase 3** (per §Y.5 reasoning: Phase 2 already 70-110h; +5-way pushes to 100-160h; 5-way usage <5%; quality-default favors doing 4-way RIGHT first; Phase 3 5-way builds on proven 4-way labeller brief).

**Owner-gate decision:** ratify Option B (defer) or override to Option A (include in Phase 2).

## §7 — NO build, NO train, NO corpus work confirmation

Per dispatch §"NO build, NO train, NO corpus work":

This PR contains ONLY:
- ✓ This memo (`review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`)

This PR does NOT contain:
- ❌ Feature implementation in `feature_extractor.py`
- ❌ Corpus modifications
- ❌ Trainer changes
- ❌ Reference set design (4-way reference is 2-D scope)
- ❌ Model artifact production
- ❌ `oracle_router.py` changes
- ❌ Tests (no new feature tests; no new corpus tests)
- ❌ Documentation outside this memo

## §8 — TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

Architect-hat findings worth surfacing beyond the dispatch's request:

1. **§1.1 Production multiway specialist gap**: per direct verification, NO multiway specialist (3-way / 4-way / 5-way) is actively loaded in production OracleRouter post-Phase-1.5-ship. Multiway requests fall back to vNext-HU-59. This was a known design choice (per BUILDER_REPORT_PHASE15E_PR_B §5) but the architect-hat surfaces it explicitly because Phase 2 4-way work is "creating the first production multiway specialist" not "refreshing an existing one." Reframes scope.

2. **§3.5 4-way reference baseline missing**: ship-gate calibration for 2-G (4-way retrain) cannot anchor to existing v9-4way performance because that file is missing on disk. Calibration spike needed in 2-D (run v9-3way on the new 4-way reference set to establish baseline projection).

3. **§4.3 Inference path versioning**: extending to 75-feature surface needs a new `inference_path_75.py` (or rename + tier) to preserve backward compat with both legacy 55-path AND modern 59-path. Not a blocker; planning surface for 2-C/2-H.

4. **§6.7 HU-6.5 corpus gap deferral**: defer to post-Phase-2 corpus refresh rather than fold into Phase 2 — pragmatic scope discipline; HU-6.5 doesn't block Phase 2 work.

## §9 — QC stream — what you audit (PR-A this memo)

Per dispatch §"QC stream — what you audit (post-design-PR)" 8-item:

- [ ] Diff scope strict: 1 file (`review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`); NO source/data edits
- [ ] Memo coverage: §1-7 sections present + addressed per dispatch (§1 attestation; §2 D5 refresh; §3 4-way gap; §4 surface lock; §5 sub-phases; §6 owner-scope; §7 NO build confirmation)
- [ ] D5 blueprint refresh: candidates re-validated (no drops; pilot gate unchanged)
- [ ] 4-way gap analysis: independent verification + 4 new candidates beyond orchestrator's first-pass (total 7)
- [ ] Surface lock proposal: 18 candidates; ~70-75 final size estimate
- [ ] Sub-phase structure: 2-A through 2-H proposed; critical path documented
- [ ] Owner-scope items: 7 items surfaced (feature lock, surface size, 4-way corpus origin, solver-queue posture, 3-way gate, 4-way gate, pre-Phase-2 incidentals); architect proposes defaults
- [ ] TC-X-DISPATCH-COMPLIANCE: design-only scope honored

## §10 — What gates next

- Builder design memo PR → on QC PASS, orchestrator merges autonomously
- After merge → orchestrator surfaces 7 owner-scope items (§6) to owner → owner ratifies feature lock + sub-phase structure + ship gates + corpus origin
- After owner ratification → Phase 2-B (6-candidate feature implementation pilot) dispatched per `feedback_pilot_first_for_long_jobs.md` standing rule

## §11 — Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: branch base `596bb89`; current master `3763d8a` (AMENDMENT 3 merged after branch creation; this commit folds AMENDMENT 3 §X + §Y + §6.8/6.9 per dispatch §"Path A — Amend PR #388 directly")
- Diff vs master: 1 file (this memo)
- Log vs master: 1 commit

## §12 — References

- Phase 2 dispatch (this PR's trigger): master `16a5aab` (PR #385)
- Phase 2 design AMENDMENT 1 (street distribution; per owner): master `cee0705` (PR #386)
- Phase 2 design AMENDMENT 2 (re-raise × players-left; per owner): master `596bb89` (PR #387)
- Phase 2 design AMENDMENT 3 (labeller readiness + 5-way scope; per owner): master `3763d8a` (PR #389)
- Phase 1.5 SHIP boundary: master `6961cca` (PR #382 + QC PR #384 PASS)
- Phase 1.5-E PR-A inference path (cross-cutting infrastructure for §4.3): master `6f61ba2` (PR #379)
- Phase 1.5 unified surface design (analog template): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- D5 deferred blueprint (refresh source for §2): `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Stay-wrong taxonomy: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`
- Reference corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Feature extractor (FEATURE_COLUMNS read for §1.2): `river-rats-core/feature_extractor.py:1569`
- Production oracle router: `river-rats-core/oracle_router.py:34-38`
- Inference path 59: `river-rats-core/inference_path_59.py`
- Solver-verification queue protocol: `feedback_solver_verification_queue.md` + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_river_rats_team_structure.md`, `feedback_named_author_builds_not_polls.md`

**Status: Phase 2-A architect-hat design memo complete. 11 D5 candidates (refreshed; no drops) + 6 4-way candidates net + 4 re-raise × players-left candidates net = 21 candidates total; estimated 74-80 final surface. ALL 3 AMENDMENTS folded in: §3.X street distribution (AMENDMENT 1); §3.Y re-raise × players-left (AMENDMENT 2); §X 4-way labeller readiness + §Y 5-way scope (AMENDMENT 3). Sub-phases 2-A through 2-H proposed; NEW 2-E.0 (4-way labeller readiness) inserted before 2-E per §X.5; 4-way reference 35-hands street-weighted; ship-gate Option A weighted total ≥28/35. 9 owner-scope items surfaced for ratification (architect default Option B for 5-way: defer to Phase 3). NO build/train/corpus work in this PR. Awaits QC PASS + orchestrator merge → owner ratification → Phase 2-B pilot dispatch.**
