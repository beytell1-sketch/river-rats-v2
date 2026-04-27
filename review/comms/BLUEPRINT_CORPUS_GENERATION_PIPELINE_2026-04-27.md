---
date: 2026-04-27
from: architect (Phase 2 design subagent)
to: orchestrator → lead-programmer (next phase)
re: Corpus-generation pipeline design for 400 new hands satisfying synthesis stratification targets
status: BLUEPRINT — not yet implemented; programmer phase next
---

# Architect Phase 2 — corpus-generation pipeline blueprint

## Sources read

All source files read directly before writing this blueprint:

- `review/comms/MAIN_TERMINAL_CORPUS_REVISION_SYNTHESIS_2026-04-27.md`
- `review/comms/AUDIT_ARCHITECT_CORPUS_DESIGN_2026-04-27.md`
- `review/comms/AUDIT_GTO_EXPERT_ACTION_DISTRIBUTION_2026-04-27.md`
- `review/comms/AUDIT_ML_ARCHITECT_CORPUS_SIZING_2026-04-27.md`
- `river-rats-core/generate_3way_situations.py`
- `river-rats-core/self_play.py`
- `river-rats-core/feature_extractor.py` (full, including SPR formula and `is_preflop_aggressor` at Feature 53)
- `river-rats-core/feature_keys.py`
- `river-rats-core/game_state_bridge.py`
- `river-rats-core/poker_game.py`
- `river-rats-core/situation_factory.py`
- `training-data/3way_situations_10k.jsonl` (schema inspection + statistical analysis)
- `data/pilot_corpus_100_hand_2026-04-26.jsonl` (schema inspection)
- `data/pilot_corpus_100_hand_2026-04-26.lock.json` (disjointness attestation)
- `scripts/build_pilot_corpus_100_hand.py` (full Build C v1.0.1 implementation)
- `review/generate_factory_situations.py` (SituationFactory usage pattern)

---

## Q1 — Existing pipeline documentation

### The two-layer architecture

The current corpus pipeline has two distinct layers:

**Layer 1: Source-pool generation** (`river-rats-core/generate_3way_situations.py`)

This script runs oracle-vs-oracle self-play using `SelfPlayRunner` with `log_all_multiway=True` and `single_position='UTG'`. For each deal, all six seats use oracle callbacks; decisions from all players (not just UTG) are captured. The output is a raw JSONL of 3-way postflop decision records.

Key parameters in the current generator call at line 85:
```python
runner = SelfPlayRunner([variant], num_deals=num_deals, seed=seed,
                        log_all_multiway=True, single_position='UTG')
```

Each record in the output pool (`training-data/3way_situations_10k.jsonl`) has this schema:
```
{situation_id, deal_id, hero_cards, board, street, hero_position,
 villain_positions, pot, to_call, facing_bet, num_opponents,
 prior_actions, feat_dict (45 features), oracle_action, adjusted_action, equity}
```

The pool contains 962 hands (not 10k as the filename implies — the file was named for the intended target but generation was halted before reaching that count).

**Layer 2: Stratified corpus sampling** (`scripts/build_pilot_corpus_100_hand.py`)

This script, Build C v1.0.1, samples 100 hands from the 962-hand pool using stratified round-robin across 5 dimensions: street × hero_position × opponent_count_bucket × board_texture × hero_range_placement.

It re-extracts all 59 features per record at sampling time (calling `feature_extractor.extract_all_features`) to upgrade from the pool's 45-feature schema to the v1.0.1 59-feature contract. The result is `data/pilot_corpus_100_hand_2026-04-26.jsonl` with a lock file at `data/pilot_corpus_100_hand_2026-04-26.lock.json`.

### Why the current pool has the structural deficits

**Root cause 1: `is_preflop_aggressor=0` for all 962 hands**

The feature is computed in `feature_extractor.py` Feature 53 (line 2499-2505):
```python
_opener_pos = hand.get('_opener_position', None)
_hero_pos = features.get('_hero_pos_raw', 'BTN')
features[F.IS_PREFLOP_AGGRESSOR] = int(
    _opener_pos is not None and _opener_pos.upper() == _hero_pos.upper()
)
```

In `game_state_bridge.py` (line 94), `opener_position` is read from `context.get('opener_position')`. The game correctly tracks `self.opener_position` in `poker_game.py` (set at lines 1161-1175 when the first preflop bet occurs). This propagates correctly through `game_state_bridge.py` line 176: `F.META_OPENER_POSITION: opener_position`.

However, the feature is correctly populated in self-play with the actual opener position. The source pool records store 45 features extracted at generation time. When Build C v1.0.1 re-extracts 59 features using `extract_all_features`, it passes `_opener_position` as a hand-dict field (line 438 of `build_pilot_corpus_100_hand.py`): `'_is_preflop_aggressor': src_feat.get('is_preflop_aggressor', 0)`.

**The problem**: the source pool's 45-feature `feat_dict` has `is_preflop_aggressor=None` for all records (confirmed by schema inspection). This is because the 45-feature extraction path used at pool-generation time did not populate this field (it was added as Feature 53 in a later step). So `src_feat.get('is_preflop_aggressor', 0)` defaults to 0, and the re-extraction in Build C inherits this zero.

More fundamentally: the generator's `_extract_3way_decisions` function (line 31-75 of `generate_3way_situations.py`) does not pass `_opener_position` into the situation record. The `feat_dict` is built from `dec.feat_dict` which is the 45-feature dict at game time — and the 45-feature path (FEATURE_COLUMNS subset) did not include `is_preflop_aggressor`. The `opener_position` is tracked in `game.opener_position` but never captured in the pool record.

**Fix path**: The generation script must be modified to capture `opener_position` from the game context and include it in each situation record. Then Build C must pass it as `_opener_position` to `extract_all_features`.

**Root cause 2: SPR=1.25 for 94% of hands**

The SPR formula in `feature_extractor.py` (line 1641-1643):
```python
pot = features['pot_size']
features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)
# DEFAULT_EFFECTIVE_STACK = 100.0
```

`DEFAULT_EFFECTIVE_STACK = 100.0` is a hardcoded constant documented as "100bb" (line 1565-1566). The `pot` field comes from the game in chip units (not BB units). The game has `starting_stack=1000` chips with BB=10 chips, so the game operates at effective depth of 100bb.

A typical 3-way raised pot (UTG raises to 3×BB, CO calls, BB calls) yields a flop pot of approximately 80 chips = 8bb. The formula computes `100.0 / 80 = 1.25`.

This is a unit mismatch: `DEFAULT_EFFECTIVE_STACK` is in BB (100bb), but `pot` is in chips (80 chips at BB=10). The correct SPR should be `effective_stack_chips / pot_chips = (1000 - invested) / 80 ≈ 12.5` (standard flop SPR).

**Critically, this is not a code bug to fix in `feature_extractor.py` for self-play data.** The formula was designed for the gauntlet/PokerBench format where pots ARE already in BB units. For self-play data where pots are in chip units, the generation layer must convert pot to BB before passing it to feature extraction, OR the corpus-builder must override the `spr` field post-extraction.

**The correct fix**: In the new generation script, convert the pot to BB units before populating the `pot` field in the hand dict passed to `extract_all_features`. Formula: `pot_bb = pot_chips / BB_chip_size`. With BB=10, a 80-chip pot becomes 8bb, and SPR = 100bb/8bb = 12.5.

**Root cause 3: No `villain_aggression_count>=2` or `num_callers_to_bet>=1`**

These features ARE wired correctly through `game_state_bridge.py` (lines 112-134). They are populated from `game.street_actions`. The deficit is a natural consequence of the game dynamics, not a code bug.

A 3-way pot with oracle players tends to produce single-street aggression because the oracles' c-bet frequency is conservative (the multiway_adjuster suppresses c-bets OOP). Villains rarely bet two streets in a row against three oracle players because the second barrel is not reliably +EV for the oracle either.

The `num_callers_to_bet=0` is structural: in the self-play game, after a bet there are typically only two remaining players (hero + one villain), not three. Multi-way scenarios where villain bets and ANOTHER villain calls (creating a bet-and-call sandwich for hero) require specific preflop structure (three players reaching postflop with specific positions) AND villain betting behaviour that the oracle does not naturally produce at high frequency.

**Fix path**: New scenario templates targeting multi-street aggression and bet-and-call situations, generated via `SituationFactory` (not self-play). This approach constructs hands with explicit action history rather than relying on the simulator to produce them organically.

**Root cause 4: No `facing_bet=1` without simultaneous `facing_raise=1`**

In the current pool, the 27 hands with `facing_bet=1` are all also `facing_raise=1`. In self-play, when a villain bets and hero faces that bet, the game's `num_raises_this_street` counter is already at 1 (the initial bet counts as a raise in `poker_game.py` line 1148: `if self.street == 'preflop' and self.opener_position and added > 0`). Wait — let me clarify: postflop, the first aggressive action is a "bet" not a "raise" in poker terminology, but the game's raise counter may be tracking differently.

Inspecting `game_state_bridge.py` line 138: `facing_raise = int(facing_bet and num_raises > 0)`. And `num_raises = context.get('num_raises_this_street', getattr(game, 'raises_this_street', 0))`. The `raises_this_street` counter in `poker_game.py` counts raise-over-raise actions, not the initial bet. So an initial postflop bet should produce `facing_bet=True, facing_raise=False`.

The reason ALL facing_bet hands in the pool also have facing_raise is likely that the oracle's self-play dynamics produce check-raises (villain checks, hero bets, villain check-raises → hero faces a raise, not an initial bet). This means the pool is missing the most common facing-bet scenario: villain c-bets into hero (an initial bet, not a raise).

This structural gap requires generating hands where villain bets first on the street — achievable via `SituationFactory` with explicit `to_call > 0` and `action_history` showing only the bet (not a prior check then bet).

---

## Q2 — Modifications to the existing pipeline to produce missing patterns

### Gap 1: `is_preflop_aggressor=1` hands (Rule 4 / c-bet decisions)

**Required change**: The new generator must capture `game.opener_position` and include it in situation records. Then during corpus assembly, pass `_opener_position` into the hand dict for `extract_all_features`.

**Specific scenario templates** to add to `SituationFactory`-based generation:

- **Scenario PFA-1**: Hero is CO opener (opener_position='CO'), villains are BTN and BB. Flop SPR ~6-8 (pot in BB units). Range of hero hand classes (air through monster). Action history: preflop CO raises, BTN calls, BB calls. No postflop action yet (hero faces check-or-bet decision as PFA).
- **Scenario PFA-2**: Hero is BTN opener, villains are SB and BB. Flop SPR ~6-8.
- **Scenario PFA-3**: Hero is HJ opener, villains are CO and BB. Flop SPR ~6-8.
- **Scenario PFA-4 (turn c-bet)**: Same as PFA-1 but flop hero checks, villain checks, turn decision. SPR ~4-5.

The key structural requirement: `opener_position == hero_position` so Feature 53 evaluates to 1.

### Gap 2: Varied SPR (standard: 2-4, deep: >=4)

**Root cause**: `DEFAULT_EFFECTIVE_STACK = 100.0` is in BB units but self-play pots are in chip units. The `SituationFactory`-based approach passes `pot` directly as a numeric value interpreted in the same unit system as `DEFAULT_EFFECTIVE_STACK`. Therefore, in `SituationFactory` specs, pot values should be in BB units (not chip units).

To produce **SPR = 4-8 (standard, early-street)**:
- Pot should be between 100/8 = 12.5bb and 100/4 = 25bb
- Canonical flop scenarios: UTG opens 3bb, BTN/BB call → pot = 9-10bb (SPR ≈ 10); adjust pot to 13-20bb for SPR 5-8.
- Use `SituationFactory` with `pot=12.5` to `pot=25.0` (in BB units).

To produce **SPR = 2-4 (medium, turn)**:
- Pot should be between 100/4 = 25bb and 100/2 = 50bb
- Canonical turn scenarios: after a flop bet and call in a 12bb pot, turn pot = ~30bb (SPR ≈ 3.3).
- Use `SituationFactory` with `pot=25.0` to `pot=50.0`.

To produce **SPR < 1 (committed, river)**:
- Pot > 100bb (SPR < 1.0)
- River after multiple streets of betting: pot = 100-200bb.
- Use `SituationFactory` with `pot=100.0` to `pot=200.0`.

**The current 962-hand pool has pots of 80-855 chips. These are CHIP values, not BB values.** When passed to `extract_all_features` they produce SPR = 100/80 = 1.25. The fix is NOT to patch `feature_extractor.py` (which would break the PokerBench training path). The fix is to generate new hands using `SituationFactory` with correct BB-unit pot values.

### Gap 3: `villain_aggression_count >= 2` (multi-street aggression)

**Required change**: New `SituationFactory` scenario templates with explicit `action_history` showing villain betting on two prior streets.

**Specific scenario templates**:

- **Scenario MAGG-1**: Villain bets flop AND turn, hero faces river decision. Action history: `[('flop', 'CO', 'bet'), ('flop', 'BB', 'call'), ('turn', 'CO', 'bet')]`. Hero faces a check-or-call/fold decision with `villain_aggression_count=2`.
- **Scenario MAGG-2**: Villain bets flop, hero calls, villain bets turn. Hero on turn faces `villain_aggression_count=1` (flop bet already counted); hero on river faces `villain_aggression_count=2`.
- **Scenario MAGG-3**: Check-raise flop (counts as 1 aggression), bet turn (counts as 2nd aggression). Hero faces river.

The feature is computed in `game_state_bridge.py` by counting prior-street bets/raises in `game.street_actions`. `SituationFactory` populates `game.street_actions` from `action_history` via `_build_street_actions()`. This path is already implemented and correct.

### Gap 4: `num_callers_to_bet >= 1` (bet-and-call sandwich)

**Required change**: New `SituationFactory` scenario templates where one villain bets and a second villain calls before hero must act.

**Specific scenario templates**:

- **Scenario BAC-1**: BTN bets (c-bets), SB calls, hero (BB) faces a bet-and-call on the flop. Action history: `[('flop', 'BTN', 'bet'), ('flop', 'SB', 'call')]`. Hero's `num_callers_to_bet = 1`.
- **Scenario BAC-2**: Same structure on the turn.
- **Scenario BAC-3**: Same structure with villain_aggression_count >= 1 (villain bet a prior street too).

The `num_callers_to_bet` feature is computed in `game_state_bridge.py` (lines 127-134) by counting 'call' actions in `game.street_actions[current_street]`. The `SituationFactory`'s `_build_street_actions` populates this correctly. This path is confirmed working.

**Critical**: In BAC scenarios, `to_call` in the `SituationFactory` spec must equal the bet amount (hero must call to continue), and `villain_positions` must include at least 2 opponents (the bettor and the caller).

### Gap 5: Nut FD facing initial bet (KB §1.7 patterns)

**Required change**: Targeted hand generation with specific hero cards (Ace of flush suit + flush draw card), board showing the flush draw, villain having bet.

**Specific scenario templates**:

- **Scenario NFD-RAISE**: Hero holds [Ah, Xh] on a board with 2+ hearts. Villain bets. `villain_air_pct >= 0.20`. Expected label: RAISE.
- **Scenario NFD-CALL**: Same hero hand and board. Villain bets. `villain_air_pct < 0.20` (villain_air_pct = 0.05-0.18). Expected label: CALL.
- **Boundary cases**: 5 hands with `villain_air_pct` spanning 0.15, 0.17, 0.20, 0.22, 0.25 to straddle the threshold.

These hands CANNOT be generated from self-play because the oracle will not naturally produce nut-FD hands facing bets with the correct villain air distribution. They must be explicitly constructed using `SituationFactory` with specified hero cards and board.

### Gap 6: Monster facing initial bet (MW-33 RAISE pattern)

**Specific scenario templates**:

- **Scenario MONSTER-RAISE**: Hero holds a set or better (`is_monster=1`). Villain bets (first bet on the street, so `facing_raise=0`). Multiple board textures.
- The monster + facing initial bet combination must be explicitly constructed. Self-play oracles facing bets with strong hands will fold if the oracle is miscalibrated; factory construction ensures the desired feat_dict values.

---

## Q3 — New source-pool size target

### Revised generation target: ~2500 candidate hands

The synthesis specifies "~2000+ candidate hands" but a more precise analysis follows.

**Action class yield analysis**:

The final 400 new hands require:
- CHECK: ~120 (30% of 400)
- BET: ~108 (27% of 400)
- CALL: ~68 (17% of 400)
- RAISE: ~56 (14% of 400)
- FOLD: ~48 (12% of 400)

The rare action classes drive the pool size requirement:

For RAISE (target 56 hands): RAISE is the rarest naturally-occurring action. In factory-constructed facing-bet hands, RAISE occurs when: (a) hero has nut FD + blocker + villain_air >= 0.20, or (b) hero has a monster. Even with deliberate targeting, expect ~30-40% of facing-bet hands to produce RAISE labels. To yield 56 RAISE hands, need approximately 140-190 facing-bet hands that are RAISE-eligible. Adding safety margin: 250 facing-bet hands with deliberate RAISE structure.

For structured scenarios (NFD, BAC, MAGG, PFA): these have high per-hand hit rates because they are explicitly constructed to trigger the target patterns. A 3:1 overgenerate-to-select ratio is sufficient.

**Pool decomposition**:

| Generation source | Target pool hands | Expected yield for corpus |
|---|---|---|
| Self-play (opener decisions, with SPR fix and PFA capture) | 1000 | ~200 checker/bettor hands for CHECK/BET stratum |
| SituationFactory - PFA c-bet scenarios | 300 | ~100 PFA hands (Rule 4 stratum) |
| SituationFactory - facing initial bet (CALL/RAISE/FOLD) | 400 | ~150 facing-bet hands |
| SituationFactory - bet-and-call (BAC) scenarios | 200 | ~50 BAC hands |
| SituationFactory - multi-street aggression (MAGG) | 200 | ~50 MAGG hands |
| SituationFactory - nut-FD facing bet (NFD) | 100 | ~25 NFD hands (boundary coverage) |
| SituationFactory - monster facing bet | 100 | ~25 monster-facing-bet hands |
| **Total pool** | **~2300** | **~600 candidates for 400 selection** |

The 600-candidate post-filter pool provides a 1.5:1 oversampling ratio for the 400-hand selection step. This is sufficient for stratified sampling with stratification slack.

**Rare cell analysis (worst case)**:

The rarest stratum cell is: nut-FD + facing initial bet + villain_air=0.18-0.22 (boundary) + SPR 4-8 + OOP. To get 5 boundary cases of this pattern, the NFD pool needs 15-20 hands in this cell. At 100 NFD pool hands, this is achievable.

---

## Q4 — Sampling strategy

### Two-phase stratification

The 400 new hands are drawn using a two-phase stratified sampling approach.

**Phase A: Mandatory quota allocation (fills structural gaps first)**

Reserve slots for hands that MUST appear regardless of natural distribution:

| Mandatory quota | Count | Source |
|---|---|---|
| Rule 4 PFA c-bet hands | 80 | PFA factory scenarios |
| KB §1.7 RAISE (nut FD facing bet, air >= 0.20) | 20 | NFD factory scenarios |
| KB §1.7 OVERRIDE→CALL (nut FD facing bet, air < 0.20) | 20 | NFD factory scenarios |
| Boundary cases: KB §1.7 threshold (air = 0.15-0.25) | 10 | NFD factory scenarios |
| MW-30 CALL pattern (facing bet + callers >= 1) | 20 | BAC factory scenarios |
| MW-33 RAISE pattern (monster facing initial bet) | 20 | Monster-facing-bet scenarios |
| MW-50 FOLD pattern (medium_made facing raise + aggression >= 1) | 20 | MAGG factory scenarios |
| Multi-street aggression fold (villain_aggression >= 2) | 20 | MAGG factory scenarios |
| Standard SPR (4-8) hands | 50 | Self-play (SPR fixed) + factory |
| Medium SPR (2-4) hands | 40 | Self-play (SPR fixed) + factory |
| Boundary cases: Rule 11 threshold (villain_tp_pct 0.35-0.45) | 10 | Targeted factory |
| **Phase A total** | **310** | — |

**Phase B: Stratified fill (remaining 90 hands)**

The remaining 90 hands are drawn from the general pool using the 8-dimension stratified sampler:

Dimensions:
1. Action context: opener / facing_initial_bet / facing_raise
2. Street: flop / turn / river
3. Position: OOP / IP
4. SPR bucket: committed (<2) / medium (2-4) / standard (4-8)
5. Hand class: air / draw / weak_made / medium_made / strong_made / monster
6. Board texture: rainbow_dry / two_tone / paired / monotone
7. Aggressor type: PFA (is_preflop_aggressor=1) / caller
8. Villain aggression: none / single-street / multi-street

Round-robin across the 8D cell space (same algorithm as Build C's `_stratified_sample`, extended to 8 dimensions).

### Handling rare-class imbalance

The synthesis target action distribution (CHECK 30% / BET 27% / CALL 17% / RAISE 14% / FOLD 12%) requires deliberate oversampling of RAISE and FOLD relative to their natural frequency.

Natural frequency in 3-way play: CHECK ~45% / BET ~30% / CALL ~10% / RAISE ~5% / FOLD ~8%.
Target vs natural: RAISE is oversampled ~3x; FOLD is oversampled ~1.5x; CHECK is undersampled.

**Handling approach**: Phase A's mandatory quotas inject the rare-class hands first. Phase B's stratified fill uses action context (opener/facing_bet/facing_raise) as the primary stratification dimension, ensuring that the pool of facing-bet hands is sampled proportionally to yield the target CALL/RAISE/FOLD distribution.

Specifically: among the 90 Phase B hands, target:
- ~25 checker/bettor hands (CHECK/BET outcomes from opener decisions)
- ~40 facing-initial-bet hands (CALL/RAISE/FOLD outcomes)
- ~25 facing-raise hands (CALL/FOLD outcomes)

Within each group, hand-class and board-texture stratification controls the sub-distribution.

### Verification gate (pre-merge)

Before the 400 new hands enter the corpus, the corpus-builder script must compute and assert:

```
facing_bet_count >= 125         # >= 25% of 500 total
pfa_count >= 150                # >= 30% of 500 total (including existing 100 hands)
spr_ge_4_count >= 125           # >= 25% of 500 total
spr_2_to_4_count >= 100         # >= 20% of 500 total
oop_pct in [0.55, 0.65]         # OOP balance check
ip_pct in [0.35, 0.45]          # IP balance check
action_dist: CHECK in [0.27, 0.33]  # ±3pp tolerance
action_dist: BET in [0.24, 0.30]
action_dist: CALL in [0.14, 0.20]
action_dist: RAISE in [0.11, 0.17]
action_dist: FOLD in [0.09, 0.15]
zero_instance_rules: each of 9 rules has >= 20 instances in combined 500
zero_coverage_patterns: each of 4 poker patterns has >= 15 instances
```

Note: action distribution cannot be verified before labelling, since labels are assigned by labellers post-corpus-build. The structural checks (facing_bet, pfa, spr, oop/ip) CAN be verified pre-labelling from feat_dict values. The action distribution check is estimated from the expected labels given the hand structures (e.g. all Phase A KB §1.7 RAISE hands are expected to produce RAISE labels).

The script should output a pre-labelling structural report and a post-labelling distribution estimate.

---

## Q5 — Disjointness preservation

### Existing disjointness mechanism

The Build C v1.0.1 script (`scripts/build_pilot_corpus_100_hand.py`) implements fingerprint-based deduplication. The fingerprint is `(sorted(hero_cards), sorted(board_cards))` — a card-equivalence-class check (two hands with the same cards in different order count as the same "spot").

Fingerprint sets currently locked:
- **Stage 6 holdout**: 49 fingerprints, anchored at SHA256 `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- **v2.3 calibration (24-hand legacy)**: 21 fingerprints
- **v2.3 anchor (9-hand extension)**: 9 fingerprints
- **Tier 1 (existing 33)**: 33 fingerprints from `review/calibration_grading_key.json`
- **Tier 2 (existing 100)**: 100 fingerprints from `data/pilot_corpus_100_hand_2026-04-26.jsonl`
- **Total forbidden**: 79 fingerprints (deduplicated)

### Disjointness protocol for the 400 new hands

The new corpus-builder script (`scripts/build_corpus_revision_500_hand.py`, see Q6) must:

1. Load all existing forbidden fingerprint sets:
   - Stage 6 holdout (parse from `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md`)
   - v2.3 calibration (parse from `review/calibration_situations.json` and mirrors)
   - v2.3 anchors (parse from pool by `situation_id`)
   - Tier 1 calibration (parse from `review/calibration_grading_key.json` + any new Tier 1 additions)
   - **New**: The 100 existing Tier 2 hands (parse from `data/pilot_corpus_100_hand_2026-04-26.jsonl`)

2. Before selecting any candidate hand, check its fingerprint against ALL forbidden sets.

3. After selection, perform post-hoc verification:
   - No overlap with Stage 6 holdout
   - No overlap with Tier 1 calibration (expanded to 45 hands)
   - No overlap with existing 100 Tier 2 hands
   - No within-batch duplicates

4. Produce a new lock file `data/pilot_corpus_500_hand_2026-04-27.lock.json` recording:
   - Fingerprint counts for each forbidden set
   - Post-sample overlap counts (all must be 0)
   - SHA256 of the combined 500-hand JSONL

### Factory-generated hands and disjointness

Hands generated via `SituationFactory` have explicitly specified `hero_cards` and `board_cards`. Their fingerprints are computed the same way. Disjointness check must be applied at scenario-spec generation time (before any labelling), not only at corpus sampling time.

**Recommended**: The scenario-spec generator should accept a `forbidden_fingerprints: set` parameter and skip any spec whose fingerprint is already forbidden. This prevents wasted labelling effort on scenarios that would be filtered out later.

### Lock file structure (new 400-hand batch)

```json
{
  "corpus_revision_version": "v2.0",
  "new_hand_count": 400,
  "combined_corpus_count": 500,
  "sha256_new_400": "<hash of 400-hand JSONL>",
  "sha256_combined_500": "<hash of 500-hand JSONL>",
  "byte_size_combined": ...,
  "build_seed": 20260427,
  "generation_sources": {
    "self_play_with_spr_fix": {"pool_size": ..., "selected": ...},
    "factory_pfa_scenarios": {"pool_size": ..., "selected": ...},
    "factory_facing_bet": {"pool_size": ..., "selected": ...},
    "factory_bac": {"pool_size": ..., "selected": ...},
    "factory_magg": {"pool_size": ..., "selected": ...},
    "factory_nfd": {"pool_size": ..., "selected": ...},
    "factory_monster_facing_bet": {"pool_size": ..., "selected": ...}
  },
  "disjointness": {
    "stage6_holdout_fingerprints": 49,
    "tier1_calibration_fingerprints": 45,
    "tier2_existing_100_fingerprints": 100,
    "v23_calibration_fingerprints": 21,
    "v23_anchor_fingerprints": 9,
    "total_forbidden_fingerprints_deduplicated": ...,
    "post_sample_overlap_holdout": 0,
    "post_sample_overlap_tier1": 0,
    "post_sample_overlap_existing_100": 0,
    "post_sample_overlap_within_new_400": 0
  },
  "structural_verification": {
    "facing_bet_count": ...,
    "pfa_count": ...,
    "spr_ge_4_count": ...,
    "spr_2_to_4_count": ...,
    "oop_count": ...,
    "ip_count": ...,
    "zero_instance_rules_coverage": {...},
    "poker_pattern_coverage": {...}
  },
  "predecessor_corpus_hash": "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40"
}
```

---

## Q6 — Pipeline interface

### Files to create

**1. `river-rats-core/generate_corpus_revision_pool.py`** — new source-pool generation script

This script generates the ~2300-hand candidate pool for the 400 new hands. It has two generation modes:

**Mode A: Self-play with SPR fix and PFA capture**

Runs `SelfPlayRunner` with modified parameters to capture `opener_position` and convert pot to BB units. The key change from `generate_3way_situations.py` is:

- Capture `game.opener_position` per situation record
- Store `pot_bb = pot_chips / BB_CHIP_SIZE` (BB_CHIP_SIZE = 10) as the pot field
- Include `_opener_position` in the situation record's metadata

The output pool records for Mode A should include:
```
{situation_id, deal_id, hero_cards, board, street, hero_position,
 villain_positions, pot (in BB units), to_call (in BB units),
 facing_bet, num_opponents, prior_actions,
 feat_dict (59 features with correct SPR and is_preflop_aggressor),
 oracle_action, adjusted_action, equity,
 generation_source: "self_play_v2",
 opener_position: <position string>}
```

**Mode B: SituationFactory scenario expansion**

Uses `SituationFactory.build_situation()` to generate hands from explicit scenario specs. Seven scenario families:

- `generate_pfa_scenarios()` — PFA c-bet decisions (Rule 4 pattern)
- `generate_facing_initial_bet_scenarios()` — initial-bet response decisions (CALL/RAISE/FOLD)
- `generate_bac_scenarios()` — bet-and-call sandwich (MW-30 pattern)
- `generate_magg_scenarios()` — multi-street aggression response (MW-50 pattern)
- `generate_nfd_scenarios()` — nut-FD facing bet (KB §1.7 pattern)
- `generate_monster_facing_bet_scenarios()` — set/monster facing initial bet (MW-33 pattern)
- `generate_rule11_boundary_scenarios()` — Rule 11 threshold boundary pairs

Each scenario function returns a list of dicts in the same schema as Mode A records, with `generation_source` set to the scenario family name.

**CLI entry point**:
```bash
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all \            # or "self_play" | "factory"
  --self-play-deals 1000 \
  --seed 20260427 \
  --output training-data/corpus_revision_pool_2026-04-27.jsonl \
  --stats-output training-data/corpus_revision_pool_stats.json
```

**Smoke test** (small-N run before full generation):
```bash
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all \
  --self-play-deals 20 \
  --seed 20260427 \
  --output /tmp/smoke_test_pool.jsonl
```

Smoke test assertions:
- Output pool >= 50 records
- At least 5 records with `is_preflop_aggressor=1`
- At least 5 records with `spr >= 4.0`
- At least 5 records with `facing_bet=1` and `facing_raise=0`
- At least 1 record with `num_callers_to_bet >= 1`
- At least 1 record with `villain_aggression_count >= 2`
- Zero records with `is_preflop_aggressor=None`

---

**2. `scripts/build_corpus_revision_500_hand.py`** — new corpus assembly script

This script assembles the combined 500-hand corpus from:
- The 100 existing hands (`data/pilot_corpus_100_hand_2026-04-26.jsonl`)
- 400 new hands sampled from `training-data/corpus_revision_pool_2026-04-27.jsonl`

It follows the same structure as `scripts/build_pilot_corpus_100_hand.py` but with:
- 8-dimension stratification instead of 5-dimension
- Phase A mandatory quota allocation before Phase B stratified fill
- Additional disjointness checks (including against existing 100 hands)
- Structural verification gate
- Unified output with consistent `pilot_hand_id` numbering

**CLI entry point**:
```bash
python3 scripts/build_corpus_revision_500_hand.py \
  --pool training-data/corpus_revision_pool_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --target-new 400 \
  --seed 20260427 \
  --output data/pilot_corpus_500_hand_2026-04-27.jsonl \
  --lock-output data/pilot_corpus_500_hand_2026-04-27.lock.json
```

**Output artifacts**:
- `data/pilot_corpus_500_hand_2026-04-27.jsonl` — combined 500-hand corpus (100 existing + 400 new)
- `data/pilot_corpus_500_hand_2026-04-27.lock.json` — lock file with disjointness attestation, structural verification, and SHA256

---

**3. Scenario spec files** — in `river-rats-core/corpus_revision_scenarios/`

Each scenario family lives in a separate Python module for readability:
- `corpus_revision_scenarios/pfa_scenarios.py`
- `corpus_revision_scenarios/facing_initial_bet_scenarios.py`
- `corpus_revision_scenarios/bac_scenarios.py`
- `corpus_revision_scenarios/magg_scenarios.py`
- `corpus_revision_scenarios/nfd_scenarios.py`
- `corpus_revision_scenarios/monster_facing_bet_scenarios.py`
- `corpus_revision_scenarios/rule11_boundary_scenarios.py`

Each module exports a `generate_scenarios(forbidden_fingerprints: set) -> list[dict]` function.

**Important**: These are NEW files. Do not modify `generate_3way_situations.py` (keep it intact as the source of the existing 962-hand pool). The new generator is a parallel script.

---

### Configuration / parameter files

No separate config file is required. All parameters are CLI arguments with documented defaults. The seed (20260427) is the only parameter that must be kept stable across reruns for reproducibility.

The `BB_CHIP_SIZE = 10` constant (used in the pot-to-BB conversion for self-play) should be defined at the top of `generate_corpus_revision_pool.py` as a named constant, matching `poker_game.py`'s `PokerGame.BIG_BLIND = 10`.

---

## Q7 — Integration with existing 100 hands

### Schema compatibility

The existing 100 hands (`data/pilot_corpus_100_hand_2026-04-26.jsonl`) have this top-level schema:
```
{pilot_hand_id, source_situation_id, deal_id, hero_cards, board, street,
 hero_position, villain_positions, pot, to_call, facing_bet, num_opponents,
 prior_actions, feat_dict (59 features)}
```

The new 400 hands must use the same schema. The `source_situation_id` field should distinguish generation source:
- Self-play hands: `d{deal_id:04d}_{pos}_{street}` (same format as the existing pool)
- Factory hands: `factory_{scenario_family}_{sequence_id}` (new format)

The `generation_source` metadata field (not in feat_dict, just in the top-level record) allows post-hoc filtering by generation method for diagnostics.

### Unified pilot_hand_id numbering

The 100 existing hands are `PILOT_001` through `PILOT_100`. The 400 new hands should be `PILOT_101` through `PILOT_500`. The combined file lists existing hands first (in their original order), followed by new hands ordered by generation source.

### Unified output schema

The combined 500-hand corpus:
```jsonl
# Records PILOT_001 through PILOT_100: unchanged from existing file
# Records PILOT_101 through PILOT_500: new hands, same schema
```

The combined file is produced by `build_corpus_revision_500_hand.py` reading both sources and writing them in the unified format. The existing 100 hands are NOT re-extracted (their 59-feature feat_dict is correct per v1.0.1). The new 400 hands ARE extracted at build time using `feature_extractor.extract_all_features` (same as v1.0.1's approach).

### Unified lock file

The combined lock file documents both source provenances:

```json
{
  "stratum_0_existing_100": {
    "source": "data/pilot_corpus_100_hand_2026-04-26.jsonl",
    "sha256": "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40",
    "hand_ids": "PILOT_001 through PILOT_100"
  },
  "stratum_1_new_400": {
    "source": "training-data/corpus_revision_pool_2026-04-27.jsonl",
    "sha256": "<pool sha256>",
    "hand_ids": "PILOT_101 through PILOT_500"
  }
}
```

### Re-validation against Tier 1 and Tier 3

After the 500-hand corpus is assembled, the lock file's disjointness verification covers:
- Tier 3 holdout (49 fingerprints): re-verified across all 500 hands (not just the 400 new ones)
- Tier 1 calibration (45 fingerprints after expansion): re-verified across all 500 hands

The lock file must record all 500 hands' fingerprint set and confirm zero overlap with Tier 1 and Tier 3.

---

## Q8 — Risks and dependencies

### Risk 1: v3.2 rule gaps surfaced by new patterns (HIGH)

**Risk**: When the factory scenarios generate hands for multi-street aggression, bet-and-call, and PFA c-bets, the v3.2 protocol may not have explicit rules for some configurations. Labellers will encounter spots where v3.2's rules produce an ambiguous or incorrect recommendation.

**Specific flagged patterns**:

- **PFA c-bet on monotone board as aggressor, range advantage**: v3.2's Rule 4 says "don't auto-c-bet IP" but does not specify frequency targets by board texture as PFA. Labellers may inconsistently apply BET vs CHECK on connected boards when hero is PFA with range advantage.
- **Multi-street aggression fold on the river**: v3.2 has MW-50 (medium_made facing raise + aggression) but the boundary between CALL and FOLD on the river after villain bet turn AND bet river is not explicitly calibrated. Labellers may disagree at this boundary.
- **Bet-and-call on a draw-heavy board (hero has draw)**: If hero has a flush draw and faces a bet-and-call, KB §1.7 says RAISE is correct ONLY with nut FD + blocker. Non-nut-FD draws in a sandwich should CALL or FOLD. The CALL vs FOLD boundary for non-nut draws in BAC situations is not explicitly covered by v3.2.

**Mitigation**: Flag these patterns to the orchestrator before mass labelling. If labeller disagreement exceeds 2 of 5 on these spot types, dispatch a GTO-expert review for v3.3 additions BEFORE labelling the full 400-hand batch.

### Risk 2: SPR fix introduces a calibration set inconsistency (MEDIUM)

**Risk**: The existing 33-hand Tier 1 calibration set was built from the same source pool (SPR=1.25 universe). If the new 400 hands have SPR 2-8 and the existing Tier 1 hands have SPR 1.25, labellers will be calibrated on a different SPR distribution than they will label.

**Mitigation**: When expanding Tier 1 from 33 to 45 hands (Synthesis Step 4), include at least 5 hands with SPR >= 4.0 in the calibration additions. This ensures labellers are calibrated on the SPR range they will encounter in the new corpus.

### Risk 3: Factory-generated hands have different feature distributions than self-play hands (MEDIUM)

**Risk**: `SituationFactory` hands have explicitly specified pot, to_call, and action_history. The villain range composition features (villain_top_pair_plus_pct, villain_air_pct, etc.) are computed by `feature_extractor` using the preflop range model. These may produce feature values that are plausible in isolation but do not occur together in real play (e.g. a very high villain_air_pct on a board that should smash villain's range given the position).

**Mitigation**: The GTO-expert should review a sample of 20-30 factory-generated hands before mass generation, confirming that the feature values are poker-realistic. Specifically verify that `villain_air_pct`, `villain_top_pair_plus_pct`, and `villain_draw_pct` are internally consistent with the specified board and positions.

### Risk 4: Compute time for 1000-deal self-play with all-player logging (LOW)

**Risk**: The existing `generate_3way_situations.py` with 3000 deals took significant wall time. The new generator with 1000 deals + all-player logging should be faster, but the per-record feature extraction now includes the 59-feature pipeline (slower than the 45-feature path).

**Estimate**: 1000 deals × 6 positions × ~0.5 situations/game × (extract time per record) ≈ 3000 records. At ~0.5-1 seconds per record for `extract_all_features`, this is 25-50 minutes for the self-play component. The factory scenarios (2300 - 1000 = 1300 records) are pure computation with no game simulation: estimate 0.2-0.3 seconds each = 4-7 minutes. Total: ~30-60 minutes for full pool generation.

**Mitigation**: Run self-play component first with `--mode self_play` to get the self-play pool early. Factory scenarios can run in parallel if needed.

### Risk 5: Solver bandwidth for Tier 1 expansion (EXTERNAL DEPENDENCY)

**Risk**: Tier 1 expansion (33 → 45 hands) requires solver verification on the 12 new calibration hands. This is a manual, time-consuming process (GTO Wizard per hand). The corpus revision plan lists this as a parallel step, but if solver bandwidth is unavailable, the Tier 1 expansion will block mass labelling.

**Mitigation**: The 400 new Tier 2 hands can be built and labelled using the existing 33-hand Tier 1 calibration gate, accepting slightly lower quality assurance on the new calibration patterns. The Tier 1 expansion is RECOMMENDED but not BLOCKING for the Phase B labelling step per the synthesis.

### Risk 6: Feature additions dependency (LOW)

**Risk**: The ml-architect audit recommended two optional feature additions: `hero_range_is_capped` and `villain_checked_back_turn`. Per the synthesis, these are NOT required for v3.0 launch. However, if added between now and the mass-labelling phase, the corpus would need to be rebuilt with the new 61-feature schema.

**Mitigation**: Do NOT add any new features before corpus generation is complete. Feature additions, if approved, should be a post-labelling change that triggers a corpus rebuild only if the reference gate fails.

### Risk 7: Model training warm-start with mixed-SPR corpus (LOW)

**Risk**: The existing 100 hands are all SPR=1.25. The new 400 hands span SPR 1-12. If the XGBoost warm-start learns SPR as a spurious separator between the "old" and "new" corpus subsets, the model may overfit to SPR as a feature that separates training batches rather than a game-theoretically meaningful feature.

**Mitigation**: The combined 500-hand corpus should be shuffled before training. The existing 100 hands should be mixed with the new 400 hands in the training input, not treated as a separate batch. The 80/20 train/val split should be stratified by action class and SPR bucket to ensure both SPR ranges appear in both splits.

---

## Implementation handoff

### Files to create or modify

| Action | File | Description |
|---|---|---|
| CREATE | `river-rats-core/generate_corpus_revision_pool.py` | New pool generator (Mode A: self-play with SPR fix; Mode B: factory scenarios) |
| CREATE | `river-rats-core/corpus_revision_scenarios/__init__.py` | Package init |
| CREATE | `river-rats-core/corpus_revision_scenarios/pfa_scenarios.py` | PFA c-bet scenario specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/facing_initial_bet_scenarios.py` | Initial-bet response specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/bac_scenarios.py` | Bet-and-call sandwich specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/magg_scenarios.py` | Multi-street aggression specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/nfd_scenarios.py` | Nut-FD facing-bet specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/monster_facing_bet_scenarios.py` | Monster facing bet specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/rule11_boundary_scenarios.py` | Rule 11 threshold boundary pairs |
| CREATE | `scripts/build_corpus_revision_500_hand.py` | Corpus assembly script |
| NO MODIFY | `river-rats-core/generate_3way_situations.py` | Preserve existing pool generator |
| NO MODIFY | `river-rats-core/feature_extractor.py` | Do NOT change DEFAULT_EFFECTIVE_STACK or SPR formula |
| NO MODIFY | `scripts/build_pilot_corpus_100_hand.py` | Preserve Build C v1.0.1 exactly |

### Test plan

**Step 1: Smoke test the pool generator**
```bash
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all --self-play-deals 20 --seed 20260427 \
  --output /tmp/smoke_test_pool.jsonl --stats-output /tmp/smoke_stats.json
```
Assert: all 8 structural checks pass (see Q6 smoke test assertions).

**Step 2: Validate factory scenario outputs**
For each scenario family, spot-check 5 generated hands:
- Verify `is_preflop_aggressor` is correct for PFA scenarios (must be 1)
- Verify `spr` is in the target range for SPR-targeted scenarios
- Verify `num_callers_to_bet >= 1` for BAC scenarios
- Verify `villain_aggression_count >= 2` for MAGG scenarios
- Verify `nut_flush_block = 1` and `has_flush_draw = 1` for NFD scenarios
- Verify `is_monster = 1` for monster-facing-bet scenarios
- Verify `facing_bet = 1` and `facing_raise = 0` for initial-bet scenarios

**Step 3: Run the corpus assembler on the smoke test pool**
```bash
python3 scripts/build_corpus_revision_500_hand.py \
  --pool /tmp/smoke_test_pool.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --target-new 10 \  # small target for smoke test
  --seed 20260427 \
  --output /tmp/smoke_corpus.jsonl \
  --lock-output /tmp/smoke_lock.json
```
Assert: lock file shows 0 disjointness overlaps, structural verification passes.

**Step 4: Full generation**
```bash
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all --self-play-deals 1000 --seed 20260427 \
  --output training-data/corpus_revision_pool_2026-04-27.jsonl

python3 scripts/build_corpus_revision_500_hand.py \
  --pool training-data/corpus_revision_pool_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --target-new 400 --seed 20260427 \
  --output data/pilot_corpus_500_hand_2026-04-27.jsonl \
  --lock-output data/pilot_corpus_500_hand_2026-04-27.lock.json
```

**Step 5: Structural verification (before PR)**
Assert that lock file structural_verification section shows all targets met.

---

## Open questions for owner

### OQ-1: SPR formula fix scope

The SPR bug (`DEFAULT_EFFECTIVE_STACK=100.0` treated as BB-units against chip-unit pots) means the existing 100 pilot hands have SPR=1.25 even though the true game SPR was ~12.5. This is a systematic mismatch in the existing corpus.

**Question**: Should the 500-hand combined corpus have consistent SPR units (all pot values converted to BB units, including the 100 existing hands which would need re-extraction)? Or is it acceptable to have the 100 existing hands with SPR=1.25 (compressed) and the 400 new hands with real SPR values (2-12)?

**Recommended**: Accept the mixed SPR distribution. The existing 100 hands' SPR=1.25 labelling is still valid label signal for committed-SPR decisions; the model can learn this as the "committed" bucket. The new 400 hands at higher SPR fill the missing range. The stratification target (SPR<2: ≤55%) is met because the 100 existing hands all fall into the committed bucket and constitute exactly 20% of the 500-hand corpus. No re-extraction of existing hands is needed.

If the owner disagrees and wants uniform SPR across all 500 hands, the 100 existing hands must be re-extracted with the corrected SPR formula. This means Build C v1.0.2 (a new build of the existing hands), which costs additional development time but does not change the labels (labels are assigned after corpus build).

### OQ-2: v3.3 protocol decision point

As noted in Risk 1, the new corpus patterns (PFA c-bet, multi-street aggression fold, BAC CALL/FOLD) may surface rule gaps in v3.2. The decision point is:

a. Run GTO-expert review on 30 factory-generated hands BEFORE mass labelling. If gaps are found, dispatch v3.3 protocol revision first.
b. Proceed with mass labelling using v3.2, accept inter-labeller disagreement on gap spots as noise, and revise to v3.3 only if the trained model fails the reference gate.

**Recommended**: Option (a). The prior audit showed that range-logic gaps are best fixed before labelling rather than after. A GTO-expert review costs ~$5-10 and 1-2 hours; discovering and fixing protocol gaps post-labelling costs far more (re-labelling 400 hands at 5x = 2000 labels).

### OQ-3: Tier 1 expansion timing relative to corpus build

The synthesis lists Tier 1 expansion (Step 4) as parallel to corpus build (Step 3). However, mass labelling (Step 5) is gated on Tier 1 expansion (labellers must pass calibration before labelling corpus). If Tier 1 expansion is bottlenecked on solver bandwidth, it could delay mass labelling by days.

**Question**: Is the Tier 1 expansion gate waivable for the 400 new hands if the new hands' patterns are not represented in the calibration set? Or must Tier 1 be updated before ANY mass labelling proceeds?

**Recommended**: Update Tier 1 before mass labelling, even if this adds wall-time. The calibration gate's purpose is to catch labeller protocol errors on the hardest patterns. If the new corpus contains patterns the calibration set doesn't test, labellers may apply v3.2 incorrectly on precisely those patterns. The Tier 1 expansion is a blocker, not optional.

---

*Blueprint complete. No code written, no files modified except this document.*
*Next step: orchestrator dispatches lead-programmer with this blueprint.*
