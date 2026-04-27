---
date: 2026-04-27
from: ml-architect (independent reviewer)
to: orchestrator → owner
re: Re-review of corpus-generation pipeline blueprint at PR #53
verdict: APPROVE-WITH-NITS
---

# ml-architect re-review of corpus-generation blueprint

## Source files read for this review

- `review/comms/AUDIT_ML_ARCHITECT_CORPUS_SIZING_2026-04-27.md` (my prior audit)
- `review/comms/MAIN_TERMINAL_CORPUS_REVISION_SYNTHESIS_2026-04-27.md`
- `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md` (under review)
- `review/comms/AUDIT_ARCHITECT_CORPUS_DESIGN_2026-04-27.md`
- `review/comms/AUDIT_GTO_EXPERT_ACTION_DISTRIBUTION_2026-04-27.md`
- `river-rats-core/feature_extractor.py` (lines 1555-1650, 2490-2545)
- `river-rats-core/generate_3way_situations.py` (full)
- `river-rats-core/game_state_bridge.py` (lines 80-188)
- `river-rats-core/feature_keys.py` (full)
- `scripts/build_pilot_corpus_100_hand.py` (lines 400-475)

---

## Q1: Does the blueprint hit my audit's stratification targets?

### Action distribution

My audit specified: CHECK 25% / BET 25% / CALL 20% / RAISE 15% / FOLD 15%.
The synthesis reconciled this to: CHECK 30% / BET 27% / CALL 17% / RAISE 14% / FOLD 12%.
The blueprint adopts the synthesis targets (Section Q4, verification gate).

**Assessment: PASS.** The synthesis reconciliation is reasonable. The 2pp difference in FOLD target (15% → 12%) and CALL target (20% → 17%) is within acceptable tolerance given the warm-start setting. The blueprint's mandatory Phase A quota (310 of 400 hands) directly enforces coverage of RAISE (56 hands), CALL (40 hands from BAC + NFD-CALL + MW-30), and FOLD (68 hands from MW-50 + MAGG + multi-street fold). The 90-hand Phase B stratified fill addresses the remainder.

**One tension to flag:** The blueprint's pool decomposition table (Section Q3) shows CHECK and BET dominated by self-play (200 opener-decision hands expected from 1000-deal self-play). If the self-play yield is lower than predicted (the current pool yields 962 hands from what was presumably thousands of deals, suggesting ~0.3 situations/deal at 3-way, not ~1.5), the CHECK/BET stratum could be underfilled. The blueprint's 1.5:1 oversampling ratio (600 candidates → 400 selected) provides some buffer, but a self-play shortfall would consume that buffer entirely. This is a calibration risk, not a design flaw.

### SPR bucket targets

My audit did not specify numeric SPR targets explicitly (I flagged SPR uniformity as the most severe structural limitation). The synthesis and blueprint specify:
- SPR >= 4: >= 25% of 500 hands (125 hands)
- SPR 2-4: >= 20% of 500 hands (100 hands)
- SPR < 2: <= 55% of 500 hands (275 hands)

The blueprint achieves this by generating SituationFactory hands with BB-unit pot values. The mechanism is correct: `pot=12.5` to `pot=25.0` for SPR 4-8; `pot=25.0` to `pot=50.0` for SPR 2-4 (Section Q2, Gap 2). **PASS.**

### OOP/IP balance

My audit specified 55-65% OOP / 35-45% IP. Blueprint adopts this verbatim in the verification gate. **PASS.**

### Class minimums

My audit specified minimum 50 per class (targeting 100+ for CALL and RAISE). The blueprint targets 56 RAISE and 68 CALL (from Phase A alone, before Phase B adds more). This meets the spirit of my floor. **PASS.**

### Rule-trigger coverage

My audit flagged zero-instance rules but did not specify per-trigger minimums (that was the architect audit's domain). The blueprint adopts the architect's 20-instances-per-rule minimum and builds Phase A mandatory quotas to enforce it. **PASS.**

---

## Q2: Are the root-cause bugs actually correct?

### Root Cause 1: `is_preflop_aggressor=0` due to metadata gap

**Blueprint claim (Section Q1):** The 45-feature pool has `is_preflop_aggressor=None` for all records because Feature 53 was added after pool generation. When `build_pilot_corpus_100_hand.py` re-extracts features, it calls `src_feat.get('is_preflop_aggressor', 0)` which defaults to 0. Additionally, the pool records never captured `opener_position` from the game, so even with a fix to the Build C script, the source data lacks the field.

**Verification against source:**

`feature_extractor.py` lines 2499-2505:
```python
_opener_pos = hand.get('_opener_position', None)
_hero_pos = features.get('_hero_pos_raw', 'BTN')
features[F.IS_PREFLOP_AGGRESSOR] = int(
    _opener_pos is not None and _opener_pos.upper() == _hero_pos.upper()
)
```

`build_pilot_corpus_100_hand.py` lines 421-440: The `hand_dict` passed to `extract_all_features` contains `_villain_aggression_count`, `_villain_checked_back`, `_villain_call_count`, `_num_callers_to_bet`, `_facing_raise`, `_is_3bet_pot` — but **NOT `_opener_position`**. This is confirmed in the source. The `hand.get('_opener_position', None)` call in `feature_extractor.py` therefore returns `None` for every record built via `build_pilot_corpus_100_hand.py`.

`generate_3way_situations.py` lines 52-74: The situation record stored in the pool includes `hero_position`, `villain_positions`, `pot`, `to_call`, `facing_bet`, `prior_actions`, and `feat_dict` — but **NOT `opener_position`**. The game's `opener_position` is never captured in the pool record.

`game_state_bridge.py` line 94: `opener_position = context.get('opener_position') or getattr(game, 'opener_position', '') or None`. The live self-play path correctly passes `opener_position` to `extract_all_features` via `F.META_OPENER_POSITION` (line 176). But this path is only used during live game inference, not during pool-record generation.

**Verdict: Root Cause 1 is correctly diagnosed.** The bug has two compounding sources:
1. Pool records never capture `game.opener_position` (generation-layer omission)
2. Build C's `hand_dict` construction never passes `_opener_position` (assembly-layer omission)

Both must be fixed in the new pipeline, and the blueprint correctly identifies both fix paths (Section Q2, Gap 1). The blueprint's description of this bug is accurate and complete.

**Implication for existing 100 hands:** All 100 existing hands have `is_preflop_aggressor=0` in their `feat_dict`. This is a systematic error. These hands will be used as the opener-decision stratum in the combined 500-hand corpus. Training the model on 100 hands with `is_preflop_aggressor=0` that are actually a mix of PFA and non-PFA decisions will teach the model that the non-aggressor structure applies to opener decisions generally — a systematic bias. This matters less than it appears because the blueprint generates 80 explicit PFA hands (Phase A mandatory quota) with correct `is_preflop_aggressor=1`, providing the positive class signal. But the 100 existing hands remain noisy for this feature.

---

### Root Cause 2: SPR=1.25 due to unit mismatch

**Blueprint claim (Section Q1):** `DEFAULT_EFFECTIVE_STACK=100.0` is in BB units, but self-play pots are in chip units. A typical 3-way raised pot of 80 chips / BB=10 produces SPR = 100.0 / 80 = 1.25 (wrong). The correct SPR would be stack_chips / pot_chips = ~920 / 80 = 11.5.

**Verification against source:**

`feature_extractor.py` lines 1565-1566 and 1641-1643:
```python
DEFAULT_EFFECTIVE_STACK = 100.0
# ...
pot = features['pot_size']
features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)
```

The docstring at line 1627-1629 confirms: "We use a default 100bb effective stack since gauntlet data doesn't include stack sizes." This is the design intent — the formula was built for PokerBench/gauntlet data where `pot` is already expressed in BB units.

In the self-play pipeline, `generate_3way_situations.py` line 58: `'pot': dec.pot` — this is the raw chip-unit pot from the game object. The game runs with `starting_stack=1000` chips and `BIG_BLIND=10` chips (confirmed from `game_state_bridge.py` context). An 80-chip pot = 8bb. SPR formula computes 100.0/80 = 1.25, not 100.0/8.0 = 12.5.

**Verdict: Root Cause 2 is correctly diagnosed.** The unit mismatch is real and the fix path (convert pot to BB units before passing to `extract_all_features` in the new generator, OR pass pot in BB units from `SituationFactory` specs) is correct. The blueprint's guidance NOT to modify `feature_extractor.py` is also correct — the formula is right for its original use case and changing it would break the PokerBench training path.

**One nuance the blueprint handles correctly but could make more explicit:** The blueprint correctly notes (Section Q7, OQ-1) that the existing 100 hands have SPR=1.25 throughout, and recommends accepting this as the "committed SPR bucket" for the combined corpus. This is workable because (a) the 100 hands will always be labelled examples where the game was effectively committed-stack, and (b) the model can learn SPR as a meaningful feature if the new 400 hands span the SPR range correctly.

---

## Q3: Does the SPR unit-inconsistency affect the warm-start delta?

This is the most important ML risk in the blueprint and it is under-addressed. Let me be specific.

**The confound:** The existing 100 hands all have `spr=1.25` (wrong units; true SPR was ~12.5). The new 400 hands will have `spr` spanning 1.0-12.0+ (correct units, correct values). When the combined 500-hand corpus is used for warm-start training:

- A model seeing `spr=1.25` will be presented with two completely different decision contexts:
  - From the existing 100 hands: "I have 1.25bb stack-to-pot, I am committed" (wrong interpretation of what the feature value means)
  - From the new 400 hands: "I actually have SPR=1.25, which is a genuinely committed river or multi-street-barrel situation"

This creates a spurious correlation between `spr=1.25` and the existing 100 hands' opener-decision label distribution (heavy CHECK/BET). The new 400 hands will likely have `spr` values above 2.0 for the non-committed scenarios, so `spr=1.25` will become a proxy for "this is from the old corpus" rather than a poker-meaningful feature.

**How severe is this?** The severity depends on how many new hands land at SPR near 1.25. If the new factory generates river/late-street scenarios with committed stacks, some will genuinely be SPR 1.0-1.5. The model may partially recover from the confound because there will be some legitimate `spr=1.25` examples in the new batch. But the 100 existing hands' use of `spr=1.25` to represent SPR=12.5 decisions remains a contamination signal.

**My recommendation vs blueprint's recommendation:**

The blueprint (Section Q7, OQ-1) recommends **accepting the mixed SPR distribution** because:
- The existing labels are still valid for committed-SPR decisions
- Relabelling costs additional dev time
- The stratification target (SPR<2: ≤55%) is nominally satisfied

I disagree with this framing. The blueprint treats the 100 existing hands as "committed SPR decisions" — but they are NOT. They are standard-SPR decisions (true SPR ~12.5) that have a corrupted SPR feature. The labels are correct (labellers labelled the actual hand, not the feature value), but the SPR feature is wrong. Training the model on a hand where the true game SPR was 12.5 but the feature reads 1.25, with a CHECK label, teaches the model: "when SPR=1.25, CHECK is often correct." This is correct for genuinely committed pots but wrong for the 100 hands where the game was actually at standard SPR.

**Concrete impact:** The XGBoost warm-start trees will see `spr` as a noisy feature with a split at ~2.0 separating "old corpus" (spr=1.25) from "new corpus" (spr>2.0). Feature importance for `spr` will be artificially elevated, and the model may use `spr` to distinguish between the two corpus sources rather than to distinguish poker decisions. This is a training-data quality issue that warm-start cannot compensate for.

**Cost-quality tradeoff:**

| Option | Cost | Quality impact |
|---|---|---|
| Accept mixed corpus (blueprint recommendation) | Zero additional cost | SPR confound; model may learn SPR as a corpus-source indicator; estimated 3-5% accuracy degradation on SPR-sensitive decisions |
| Re-extract features on existing 100 hands with corrected SPR formula | ~2-4 hours dev time; no relabelling needed | Eliminates the confound; full SPR signal quality across all 500 hands |
| Discard existing 100 hands; rebuild fully | ~$15-25 relabelling cost for 100 hands (500 labels) | Maximum signal quality; loses the existing investment |

**My specific recommendation: Re-extract features on the existing 100 hands** (Option 2). This is low-cost (no relabelling needed — labels are preserved), corrects the systematic error, and takes 2-4 hours of dev work. The process: read `data/pilot_corpus_100_hand_2026-04-26.jsonl`, reconstruct the hand dict with `pot_bb = pot_chips / 10.0` substituted for the raw chip-unit pot before calling `extract_all_features`, and write a `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` with corrected feature dicts. The lock file SHA256 needs updating but the labels are unchanged.

**The blueprint flags this as OQ-1 without making a strong recommendation**, instead defaulting to "accept the mixed distribution." This is the one place where the blueprint's risk assessment is too sanguine. The confound is real and the fix is cheap.

**Bottom line for Q3:** The warm-start delta is materially affected by the SPR confound. Re-extraction of the 100 existing hands is the correct call. Cost: ~2-4 dev hours. Benefit: eliminates the most significant feature-quality issue in the combined corpus. I recommend adding this as a required step before corpus assembly, not an optional follow-up.

---

## Q4: Are the proposed feature additions addressed?

My prior audit recommended (as optional, not required):
1. `hero_range_is_capped` (Feature 60)
2. `villain_checked_back_turn` (decompose existing `villain_checked_back` by street)

**Blueprint handling (Section Q8, Risk 6):**

The blueprint explicitly addresses both features:
> "Do NOT add any new features before corpus generation is complete. Feature additions, if approved, should be a post-labelling change that triggers a corpus rebuild only if the reference gate fails."

This is correct. My audit marked both as optional and non-blocking. The blueprint's policy — freeze features before corpus generation, add after if the model fails the reference gate — is the right sequencing.

**Extendability question:** Can the blueprint's pipeline be extended for future feature additions without rewriting?

Yes, with one caveat. The blueprint's `generate_corpus_revision_pool.py` (Mode A) passes `_opener_position` into the hand dict for `extract_all_features`. This is the right pattern. If a new feature requires a new metadata field, the same pattern applies: add the field to the hand dict construction in both Mode A (self-play) and Mode B (factory scenarios), add it to `extract_all_features`, add to `FEATURE_COLUMNS`, and regenerate the corpus with the new feature. The modular structure of the scenario files (7 separate modules) makes this tractable.

The one-time rebuild cost if `hero_range_is_capped` is added would be a full corpus regeneration (the 400 new hands would need re-extraction; the 100 existing hands also). Given that this is why the feature was marked optional and post-launch, the blueprint's sequencing is correct.

**Assessment: PASS.** The blueprint correctly defers feature additions, maintains extendability via the modular scenario architecture, and does not contradict my audit's recommendation on these features.

---

## Q5: Does the scenario-module approach produce realistic ML training distributions?

The blueprint uses 7 explicit SituationFactory scenario families to generate facing-bet and PFA hands that self-play cannot organically produce. The poker realism of these factory-generated hands is the key risk.

**What the blueprint claims:** Factory hands have explicitly specified `pot`, `to_call`, and `action_history`. Villain range composition features (`villain_top_pair_plus_pct`, `villain_air_pct`, etc.) are computed by `feature_extractor` using the preflop range model. The blueprint acknowledges Risk 3: "factory-generated hands have different feature distributions than self-play hands" and recommends GTO-expert review of 20-30 factory-generated hands before mass generation.

**The joint-distribution problem:**

In real play, `villain_air_pct` is not independently drawn — it is a function of the board texture, street, and villain's preflop range. For example:
- On A-high boards, BTN opener's range is heavy in Ace-x combos → `villain_air_pct` is naturally low
- On low connected boards, BTN opener has many air combos (overcards without connection) → `villain_air_pct` naturally higher

If `SituationFactory` constructs NFD scenarios by specifying arbitrary `villain_air_pct` values (e.g. "5 hands with villain_air_pct=0.20" and "5 hands with villain_air_pct=0.15"), but these values don't emerge from the preflop range model applied to the actual board and positions specified in the scenario, then the joint distribution of (`villain_air_pct`, `board_texture`, `villain_position`) will be unrealistic.

**Is this actually a problem with the blueprint's approach?**

The blueprint does NOT specify that factory scenarios hard-code `villain_air_pct`. Section Q2, Gap 5 (NFD scenarios) says:
> "Villain bets. `villain_air_pct >= 0.20`. Expected label: RAISE."

This reads as a constraint on what the feature value should be, not a directly injected value. The feature is computed by `feature_extractor` from the specified hero cards, board, and villain position. So the question is: can the scenario designer reliably choose `hero_cards`, `board`, and positions such that the resulting computed `villain_air_pct` lands in the desired range?

**Answer: Yes, but it requires poker-expert iteration.** If the GTO expert designs the NFD scenario as "AhXh on a 2-heart board where villain is BTN and board is 8h5d2c," the preflop range model will compute villain's air percentage based on BTN's range on that board. Whether that produces `villain_air_pct >= 0.20` or not depends on the specific range model and board. The blueprint's Risk 3 mitigation (GTO-expert review of 20-30 factory hands) is the correct safeguard.

**The correlation preservation question:**

In real play, `villain_top_pair_plus_pct` and `villain_aggression_count` are naturally correlated — aggressive villains tend to have more value-heavy continuing ranges (they bet their good hands; their checking range is weaker). If all 20 Phase A MAGG scenarios are constructed with villain_aggression_count=2 AND villain_top_pair_plus_pct at some fixed level, this correlation may not be preserved.

This is a genuine risk. The blueprint does not explicitly address whether the factory scenarios preserve realistic joint distributions among villain range features. Risk 3's mitigation (GTO-expert review) is necessary but may not be sufficient for detecting joint-distribution issues — a reviewer looking at 30 hands individually may not notice if `villain_aggression_count` and `villain_top_pair_plus_pct` are systematically uncorrelated across those 30 hands.

**Recommendation (NIT):** Before mass generation, run a brief distribution check on the factory pool: compute the pairwise correlation between `villain_air_pct`, `villain_top_pair_plus_pct`, `villain_draw_pct`, and `villain_aggression_count` across the factory-generated hands. Compare to the same correlations in the self-play pool (962 hands). Large correlation differences are a signal that factory hands are unrealistic. This is a 30-minute analysis step, not a full review.

**Overall assessment:** The 7-scenario approach is sound for covering rule-trigger patterns that self-play cannot produce. The joint-distribution realism risk is real but manageable with the GTO-expert review gate and the correlation check I recommend above. The blueprint's Risk 3 acknowledgment is honest and the mitigation is correct in spirit; the above adds a quantitative safeguard.

---

## Q6: Pipeline testability

The blueprint proposes a 4-step test plan (Section Q6, Q8):

1. Smoke test the pool generator (20 deals, assert 8 structural checks)
2. Validate factory scenario outputs (spot-check 5 per scenario family)
3. Run corpus assembler on smoke test pool (10 new hands, assert lock file)
4. Full generation

**Assessment of testability:**

**Smoke test (Step 1):** The 8 structural assertions (`is_preflop_aggressor=1` in ≥5 records, `spr >= 4.0` in ≥5 records, etc.) directly test whether the root-cause bugs are fixed. This is well-designed — it tests what matters rather than what's easy. The assertion `zero records with is_preflop_aggressor=None` would catch any regression in the `_opener_position` propagation.

**Factory scenario validation (Step 2):** Spot-checking 5 hands per scenario family is the minimum useful unit test. The assertions are specific: `is_preflop_aggressor=1` for PFA scenarios, `num_callers_to_bet >= 1` for BAC scenarios, etc. These directly verify the scenario-generation logic.

**Corpus assembler smoke test (Step 3):** Testing with `--target-new 10` is correct — it exercises the disjointness check, stratified sampling, and lock file generation without the full compute cost.

**Gaps in the test plan:**

- No test for SPR correctness specifically. The smoke test checks `spr >= 4.0` in ≥5 records, but does not verify that `spr=1.25` from the old self-play path is not re-introduced. A specific assertion: "no record from Mode A self-play should have `spr < 2.0` when `pot_chips` is in the 60-120 range" would catch the unit-mismatch regression.

- No test for feature consistency between Mode A (self-play) and Mode B (factory) hands. The combined corpus should have the same feature schema for both sources. A validation: "the distribution of `is_preflop_aggressor` across Mode A hands should match the distribution of preflop-opener hands in the source pool based on `hero_position`" would catch silent generation errors.

- No test for action distribution. The blueprint correctly notes (Section Q4): "action distribution cannot be verified before labelling." However, the expected action distribution can be estimated from the structural features before labelling: PFA hands with `facing_bet=0` should predominantly produce BET/CHECK labels; NFD RAISE scenario hands should produce RAISE. Adding a pre-labelling action-distribution estimate to the lock file (as the blueprint already specifies in the verification gate section) partially addresses this.

**Will the smoke test surface real issues?** Yes, for the root-cause bugs. The 8 structural checks directly test whether `is_preflop_aggressor`, `spr`, `facing_bet`, `num_callers_to_bet`, and `villain_aggression_count` are populated correctly. A smoke test failure on any of these is a real bug, not a false alarm.

**Overall assessment: The test plan is solid for the specific root causes being fixed.** The two gaps I flagged (no SPR regression test, no cross-mode feature consistency test) are minor additions. The fundamental smoke-test design is correct.

---

## Q7: What's missing from an ML perspective?

### 7.1 Validation/holdout split strategy — PARTIALLY ADDRESSED

The blueprint does not specify the train/val split strategy for the combined 500-hand corpus. My prior audit recommended: use the 24 three-way reference hands as the validation set for early stopping (rather than a random 20% split). The blueprint does not address this. The synthesis mentions it (Section "Architecture changes": "Validation: gate against the 24 three-way reference hands directly, not random 20% split") but the blueprint as a corpus-generation document doesn't need to resolve training configuration. This belongs in the training plan, not the corpus-generation blueprint.

**Not a gap in the blueprint. It is the correct scope boundary for this document.** However, the orchestrator should ensure this is carried into the training plan when that phase is dispatched.

### 7.2 Sample-weight handling — NOT ADDRESSED

The blueprint does not address whether the existing 100 hands and the new 400 hands should receive the same sample weight during training. This matters because:

- The 100 existing hands are all opener-decisions at (incorrectly) compressed SPR. If accepted as-is (with the SPR confound), they represent a systematically different distribution from the new 400.
- Even if SPR is corrected (my Q3 recommendation), the existing 100 hands cover a much narrower range of action contexts than the new 400.

**Recommendation:** In the training script, the combined 500-hand corpus should be shuffled and trained with standard inverse-frequency class weighting. Do NOT apply additional corpus-source weighting (do not downweight the 100 old hands relative to the 400 new hands). The class weighting is sufficient to handle the action-class imbalance. Additional source weighting would be premature; assess whether it's needed after seeing the reference-gate results.

This is a training-phase concern, not a corpus-generation concern. **Not a gap in the blueprint.**

### 7.3 Feature normalization / preprocessing — NOT ADDRESSED

XGBoost does not require feature normalization (tree-based models are scale-invariant). No normalization changes are needed. **Not a gap in the blueprint.**

### 7.4 Compatibility with existing model.json artifact — NOT EXPLICITLY ADDRESSED

The blueprint does not mention whether the new 59-feature corpus is compatible with the existing `model.json` artifact for warm-start. The warm-start mechanism requires that the new corpus use the same feature schema as the base model.

This is a concern that needs verification before the training phase. If the base model (v9-baseline trained on PokerBench) uses a different feature subset than the 59-feature contract, the warm-start will fail silently or visibly. The blueprint's "no modify to feature_extractor.py" instruction preserves this compatibility for the feature pipeline, but the training script needs to verify that `FEATURE_COLUMNS` in `train_model.py` matches the feature contract of both the existing model artifact and the new corpus.

**This is a gap.** The blueprint should flag this as a pre-training verification step: before warm-start training, verify that the base model's feature schema matches `FEATURE_COLUMNS` exactly (same columns, same order). This is a 5-minute check but has historically caused silent errors in this project. **NIT: add this as a pre-training verification to the implementation handoff section.**

### 7.5 Early stopping on imbalanced corpus — NOT ADDRESSED

The blueprint does not specify how early stopping should behave on the combined 500-hand corpus. With my prior audit's recommendation to use the 24 reference hands for early stopping (rather than a random 20% split), the imbalanced action distribution in the training corpus becomes less of a concern for the validation metric — the reference hands have roughly balanced class coverage. However, if the programmer uses a random 20% split for early stopping instead, the validation set will inherit the same action-class imbalance as the training set, and early stopping may optimize for CHECK/BET accuracy at the expense of CALL/RAISE.

**This is a training-phase concern.** The blueprint correctly leaves training configuration to the training phase. **Not a gap in the corpus-generation blueprint.**

### 7.6 Missing: explicit disjointness verification for factory-generated hands at scenario spec time

The blueprint recommends (Section Q5): "The scenario-spec generator should accept a `forbidden_fingerprints: set` parameter and skip any spec whose fingerprint is already forbidden." This is correct. However, `SituationFactory`-generated hands have programmer-specified `hero_cards` and `board_cards`. The fingerprint `(sorted(hero_cards), sorted(board_cards))` for a factory hand is deterministic given the spec. If two scenario families generate specs with the same card combination (e.g. both the NFD scenario and the monster-facing-bet scenario specify AhKh on Kh8h3d), the disjointness check must catch this WITHIN the factory pool, not just against the external forbidden sets.

**The blueprint mentions within-batch duplicate detection** (Section Q5, OQ-1 lock file: "post_sample_overlap_within_new_400: 0") but does not explicitly call out the risk of inter-scenario-family fingerprint collisions during spec generation. This is a minor gap in the spec-generation layer.

**NIT: Add an explicit note that the `forbidden_fingerprints` set passed to each scenario generator should be updated incrementally as each scenario family runs, so that cards chosen by NFD scenarios are excluded from consideration by monster-facing-bet scenarios.**

---

## Q8: Final verdict

**Verdict: APPROVE-WITH-NITS**

The blueprint is fundamentally sound. The root-cause diagnoses are correct, the generation strategy addresses the structural gaps, the 7-scenario modular approach is implementable, the test plan is adequate, and the implementation handoff (file list, CLI interface, lock file schema) is complete.

**The changes needed before programmer dispatch:**

### Required changes (must be addressed before programmer starts):

**R1: SPR confound — re-extraction of existing 100 hands is required, not optional.**

The blueprint's OQ-1 presents re-extraction as optional and defaults to accepting the mixed SPR distribution. This is incorrect. The 100 existing hands have `is_preflop_aggressor=0` (wrong) and `spr=1.25` (wrong units). Both are systematic errors in the feature contract, not just distributional imbalances. Re-extraction fixes both: the new generator will pass `_opener_position` correctly, and pot values will be in BB units. This requires building a one-off re-extraction script for the existing 100 hands: read their raw pool records (the source JSONL from which they were sampled), rebuild `hand_dict` with `pot_bb = pot_chips / BB_CHIP_SIZE`, and call `extract_all_features`. Cost: 2-4 hours dev time. Benefit: eliminates the most significant feature-quality issue in the combined corpus.

**Action:** Add a `scripts/reextract_pilot_100_features.py` step to the implementation handoff table, with the instruction to run it BEFORE corpus assembly and update the lock file with the corrected SHA256.

**R2: Pre-training feature schema compatibility check — add to implementation handoff.**

Before warm-start training, verify that the base model's feature schema (from `model.json` or the training artifact's `FEATURE_COLUMNS`) matches the 59-feature contract of the new corpus exactly. Add this as a verification step in the implementation handoff section. It is not a code change but a mandatory pre-training gate.

### Nits (small additions, do not block programmer):

**N1: SPR regression test in smoke test.**

Add to the smoke test assertions: "no Mode A (self-play) record has `spr < 2.0` AND `pot_chips > 60`" — this catches the unit-mismatch regression if the new generator makes an error in the BB conversion. Estimated cost: 5 lines added to the smoke test.

**N2: Joint-distribution correlation check for factory pool.**

Before mass generation, run a pairwise correlation check between `villain_air_pct`, `villain_top_pair_plus_pct`, `villain_draw_pct`, and `villain_aggression_count` across the factory pool. Compare to the same correlations in the self-play pool. Flag if any correlation differs by > 0.3. This is a 30-minute analysis step, not a code change.

**N3: Incremental `forbidden_fingerprints` update within scenario spec generation.**

When generating scenario specs across 7 scenario families, update the `forbidden_fingerprints` set incrementally after each family runs, so that inter-family fingerprint collisions are caught at spec-generation time (not only at corpus-assembly time). Add this to the `generate_scenarios()` interface documentation in Section Q6.

---

## Summary table

| Item | Audit target | Blueprint coverage | Assessment |
|---|---|---|---|
| Action distribution targets | CHECK 25 / BET 25 / CALL 20 / RAISE 15 / FOLD 15 | CHECK 30 / BET 27 / CALL 17 / RAISE 14 / FOLD 12 (synthesis) | PASS — synthesis reconciliation is sound |
| SPR coverage | Varied SPR as primary blocker | SPR 4-8 (>= 25%), SPR 2-4 (>= 20%), SPR<2 (<= 55%) | PASS — BB-unit fix is correct |
| OOP/IP balance | 55-65% OOP / 35-45% IP | Verbatim from synthesis | PASS |
| Class minimums | 50+ per class (100+ for CALL, RAISE) | CALL 68+, RAISE 56+ from Phase A alone | PASS |
| Rule-trigger coverage | All 9 zero-instance rules covered | Phase A mandatory quotas for all 9 | PASS |
| Root cause 1 diagnosis | — | `is_preflop_aggressor` missing due to generation + assembly gap | CORRECT |
| Root cause 2 diagnosis | — | SPR unit mismatch: chip-unit pots against BB-unit stack constant | CORRECT |
| SPR confound in warm-start | Flagged in Q3 (my audit: Low risk annotation) | Noted as OQ-1, defaults to "accept" | INSUFFICIENT — re-extraction required (R1) |
| Feature additions deferred | Optional, non-blocking | Explicitly deferred post-labelling | PASS |
| Scenario realism | — | GTO-expert review gate for 20-30 factory hands | ADEQUATE + NIT (N2 correlation check) |
| Testability | — | 4-step test plan with 8 structural assertions | PASS + NIT (N1 SPR regression test) |
| Validation split | Use 24 reference hands for early stopping | Not addressed (correct scope boundary) | NOT A GAP — training plan handles |
| Sample weighting | Standard inverse-frequency | Not addressed (correct scope boundary) | NOT A GAP — training plan handles |
| Feature schema compatibility | — | Not mentioned | MISSING — required pre-training gate (R2) |

**Required changes before programmer dispatch: R1 (re-extract existing 100 hands) and R2 (add feature schema check to handoff).**

**Blueprint is otherwise ready for programmer.** The architect has done solid work: root causes correctly identified, fix paths correctly specified, scenario design comprehensive, test plan adequate, and implementation handoff complete.

---

*Review complete. No files modified except this document. No code written.*
