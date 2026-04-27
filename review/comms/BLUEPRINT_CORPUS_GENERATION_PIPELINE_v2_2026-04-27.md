---
date: 2026-04-27
from: architect (Phase 2.5 update subagent)
to: orchestrator → reviewers (round 2: ml-architect + gto-expert + QC) → owner → lead-programmer
re: Updated corpus-generation pipeline blueprint v2 — incorporates synthesis decisions (Path A + 5 R-items + 2 scope additions)
supersedes: BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md (PR #53 closed)
status: BLUEPRINT v2 — pending reviews-2
---

# Architect Phase 2.5 — corpus-generation pipeline blueprint v2

## What changed in this update

This document supersedes the original blueprint from PR #53 (`e635d00`). The prior blueprint was ~90% correct; this update incorporates the five required fixes and two scope additions adopted by the synthesis at master `f5008b9`.

**Changes applied:**

| ID | Change | Section |
|----|--------|---------|
| Path A | Re-extract existing 100 hands (OQ-1 → resolved) | Q7, Implementation Handoff |
| R1 | `scripts/reextract_pilot_100_features.py` added to handoff | Q7, Implementation Handoff |
| R2 | Pre-training feature schema compatibility check added | Q6, Implementation Handoff |
| R3 | Module 4 (MAGG) action histories extended to river decision point | Q2, Q6 |
| R4 | Post-generation NFD boundary validation step added | Q4, Q6 |
| R5 | Rule 11 boundary pairs now vary across ≥3 board textures | Q2, Q6 |
| Scope+ | Module 8 (donk-bet defence) added | Q4, Q6 |
| Scope+ | Module 9 (SB-as-hero sandwich) added | Q4, Q6 |
| Nits | N1 (SPR regression assertion), N2 (pairwise correlation check), N3 (incremental forbidden fingerprints), +1-2 MAGG FOLD calibration hands | Q6, Q8 |
| OQ dispositions | Q1 RESOLVED, Q2 DEFERRED, Q3 RESOLVED | Q8 Open Questions |

The 90% of the blueprint that was correct is unchanged. Corrections are targeted.

---

## Sources read for this update

All source files read directly:

- `review/comms/MAIN_TERMINAL_BLUEPRINT_REVIEW_SYNTHESIS_2026-04-27.md` (master `f5008b9`)
- `review/comms/REVIEW_ML_ARCHITECT_BLUEPRINT_PR53_2026-04-27.md`
- `review/comms/REVIEW_GTO_EXPERT_BLUEPRINT_PR53_2026-04-27.md`
- `~/river-rats-qc/findings/2026-04-27-pr53-pre-merge-blueprint-corpus-generation.md`
- Original blueprint: `git show e635d00:review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md`

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

This bug has two compounding sources (ml-architect verification at Q2): (1) pool records never capture `game.opener_position` at generation time, and (2) Build C's `hand_dict` construction never passes `_opener_position` at assembly time. Both must be fixed in the new pipeline.

**Fix path**: The generation script must be modified to capture `opener_position` from the game context and include it in each situation record. Then corpus assembly must pass it as `_opener_position` to `extract_all_features`.

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

**Critically, this is not a code bug to fix in `feature_extractor.py` for self-play data.** The formula was designed for the gauntlet/PokerBench format where pots ARE already in BB units. For self-play data where pots are in chip units, the generation layer must convert pot to BB before passing it to feature extraction. Do NOT modify `feature_extractor.py`.

**The correct fix**: In the new generation script, convert the pot to BB units before populating the `pot` field in the hand dict passed to `extract_all_features`. Formula: `pot_bb = pot_chips / BB_CHIP_SIZE`. With `BB_CHIP_SIZE=10`, an 80-chip pot becomes 8bb, and SPR = 100bb/8bb = 12.5.

**Root cause 3: No `villain_aggression_count>=2` or `num_callers_to_bet>=1`**

These features ARE wired correctly through `game_state_bridge.py` (lines 112-134). They are populated from `game.street_actions`. The deficit is a natural consequence of the game dynamics, not a code bug.

A 3-way pot with oracle players tends to produce single-street aggression because the oracles' c-bet frequency is conservative (the multiway_adjuster suppresses c-bets OOP). Villains rarely bet two streets in a row against three oracle players because the second barrel is not reliably +EV for the oracle either.

The `num_callers_to_bet=0` is structural: in the self-play game, after a bet there are typically only two remaining players (hero + one villain), not three. Multi-way scenarios where villain bets and ANOTHER villain calls (creating a bet-and-call sandwich for hero) require specific preflop structure AND villain betting behaviour that the oracle does not naturally produce at high frequency.

**Fix path**: New scenario templates targeting multi-street aggression and bet-and-call situations, generated via `SituationFactory` (not self-play). This approach constructs hands with explicit action history rather than relying on the simulator to produce them organically.

**Root cause 4: No `facing_bet=1` without simultaneous `facing_raise=1`**

In the current pool, the 27 hands with `facing_bet=1` are all also `facing_raise=1`. The oracle's self-play dynamics produce check-raises (villain checks, hero bets, villain check-raises → hero faces a raise, not an initial bet). This means the pool is missing the most common facing-bet scenario: villain c-bets into hero (an initial bet, not a raise).

This structural gap requires generating hands where villain bets first on the street — achievable via `SituationFactory` with explicit `to_call > 0` and `action_history` showing only the bet (not a prior check then bet).

---

## Q2 — Modifications to the existing pipeline to produce missing patterns

### Gap 1: `is_preflop_aggressor=1` hands (Rule 4 / c-bet decisions)

**Required change**: The new generator must capture `game.opener_position` and include it in situation records. Then during corpus assembly, pass `_opener_position` into the hand dict for `extract_all_features`.

**Specific scenario templates** to add to `SituationFactory`-based generation:

- **Scenario PFA-1**: Hero is CO opener (opener_position='CO'), villains are BTN and BB. Flop SPR ~6-8 (pot in BB units). Range of hero hand classes (air through monster). Action history: preflop CO raises, BTN calls, BB calls. No postflop action yet (hero faces check-or-bet decision as PFA).
- **Scenario PFA-2**: Hero is BTN opener, villains are SB and BB. Flop SPR ~6-8.
- **Scenario PFA-3**: Hero is HJ opener, villains are CO and BB. Flop SPR ~6-8.
- **Scenario PFA-4 (turn c-bet)**: Same as PFA-1 but flop hero checks, villain checks, turn decision. SPR ~4-5. Cap at ≤10 hands — this is an uncommon action pattern (PFA checked flop, now leading turn; ~10% of flop-checked PFA decisions) and should not dominate the PFA stratum.

The key structural requirement: `opener_position == hero_position` so Feature 53 evaluates to 1.

### Gap 2: Varied SPR (standard: 2-4, deep: >=4)

**Root cause**: `DEFAULT_EFFECTIVE_STACK = 100.0` is in BB units but self-play pots are in chip units. The `SituationFactory`-based approach passes `pot` directly as a numeric value interpreted in the same unit system as `DEFAULT_EFFECTIVE_STACK`. Therefore, in `SituationFactory` specs, pot values should be in BB units (not chip units).

To produce **SPR = 4-8 (standard, early-street)**:
- Pot should be between 100/8 = 12.5bb and 100/4 = 25bb
- Use `SituationFactory` with `pot=12.5` to `pot=25.0` (in BB units).

To produce **SPR = 2-4 (medium, turn)**:
- Pot should be between 100/4 = 25bb and 100/2 = 50bb
- Use `SituationFactory` with `pot=25.0` to `pot=50.0`.

To produce **SPR < 2 (committed, late-street)**:
- Pot > 50bb
- River after multiple streets of betting: pot = 50-200bb.
- Use `SituationFactory` with `pot=50.0` to `pot=200.0`.

**The current 962-hand pool has pots of 80-855 chips. These are CHIP values, not BB values.** The fix is NOT to patch `feature_extractor.py`. The fix is to generate new hands using `SituationFactory` with correct BB-unit pot values, and to convert pot to BB units (`pot_bb = pot_chips / BB_CHIP_SIZE`) in the Mode A self-play path.

### Gap 3: `villain_aggression_count >= 2` (multi-street aggression)

**Required change**: New `SituationFactory` scenario templates with explicit `action_history` showing villain betting on two prior streets.

**CORRECTED action histories (R3 fix)**: The `villain_aggression_count` feature counts prior-street bets. To produce `villain_aggression_count=2`, the decision point must be on the **river**, after villain has bet both the flop and the turn. The blueprint's original action histories were truncated — they showed the second bet (putting hero on the turn with `villain_aggression_count=1`) rather than extending to the river (where `villain_aggression_count=2`).

**Corrected scenario templates**:

- **Scenario MAGG-1**: Villain bets flop, hero calls, villain bets turn, hero calls, hero faces river decision with `villain_aggression_count=2`.
  - Action history: `[('flop', 'CO', 'bet'), ('flop', 'BB', 'call'), ('turn', 'CO', 'bet'), ('turn', 'BB', 'call')]`
  - Decision point: river (hero is BB, decides check/call/fold facing potential river bet, or leading out)
  - Feature check: `villain_aggression_count=2` (two prior-street bets counted)

- **Scenario MAGG-2**: Villain bets flop, hero calls, villain bets turn, hero calls. Hero on river with `villain_aggression_count=2`.
  - Action history: `[('flop', 'CO', 'bet'), ('flop', 'BB', 'call'), ('turn', 'CO', 'bet'), ('turn', 'BB', 'call')]`
  - Same as MAGG-1; variant in board texture and hero hand class.

- **Scenario MAGG-3**: Villain check-raises flop (counts as aggression=1), villain bets turn (aggression=2). Hero calls both. River decision.
  - Action history: `[('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'raise'), ('flop', 'CO', 'call'), ('turn', 'BB', 'bet'), ('turn', 'CO', 'call')]`
  - Decision point: river (CO/hero faces or acts on river)
  - Feature check: `villain_aggression_count=2`

**Verification requirement**: For each MAGG scenario specification, confirm that `villain_aggression_count` reads as 2 at the river decision point (not 1 at a turn decision point). The programmer must NOT implement MAGG scenarios with truncated action histories.

**Concrete check**: After generating any MAGG batch, assert `all(r['feat_dict']['villain_aggression_count'] == 2 for r in magg_records)`. A count of 1 in any record means the action history is truncated at the turn.

### Gap 4: `num_callers_to_bet >= 1` (bet-and-call sandwich)

**Required change**: New `SituationFactory` scenario templates where one villain bets and a second villain calls before hero must act.

**Specific scenario templates**:

- **Scenario BAC-1**: BTN bets (c-bets), SB calls, hero (BB) faces a bet-and-call on the flop. Action history: `[('flop', 'BTN', 'bet'), ('flop', 'SB', 'call')]`. Hero's `num_callers_to_bet = 1`.
- **Scenario BAC-2**: Same structure on the turn.
- **Scenario BAC-3**: Same structure with villain_aggression_count >= 1 (villain bet a prior street too).

The `num_callers_to_bet` feature is computed in `game_state_bridge.py` (lines 127-134) by counting 'call' actions in `game.street_actions[current_street]`. The `SituationFactory`'s `_build_street_actions` populates this correctly.

**Critical**: In BAC scenarios, `to_call` in the `SituationFactory` spec must equal the bet amount (hero must call to continue), and `villain_positions` must include at least 2 opponents (the bettor and the caller).

### Gap 5: Nut FD facing initial bet (KB §1.7 patterns)

**Required change**: Targeted hand generation with specific hero cards (Ace of flush suit + flush draw card), board showing the flush draw, villain having bet.

**Specific scenario templates**:

- **Scenario NFD-RAISE**: Hero holds [Ah, Xh] on a board with 2+ hearts. Villain bets. `villain_air_pct >= 0.20`. Expected label: RAISE.
- **Scenario NFD-CALL**: Same hero hand and board. Villain bets. `villain_air_pct < 0.20` (villain_air_pct = 0.05-0.18). Expected label: CALL.
- **Boundary cases**: 5 hands with `villain_air_pct` spanning 0.15, 0.17, 0.20, 0.22, 0.25 to straddle the threshold.

**Board/position guidance for NFD-RAISE scenarios**: Prefer boards where villain's position naturally produces higher air fractions (e.g. villain is BB with wide range, or use lower-card boards like 7h-4h-2d where opener's range has more unconnected hands). This ensures `villain_air_pct >= 0.20` arises from realistic range dynamics, not forced feature injection.

These hands CANNOT be generated from self-play because the oracle will not naturally produce nut-FD hands facing bets with the correct villain air distribution.

### Gap 6: Monster facing initial bet (MW-33 RAISE pattern)

**Specific scenario templates**:

- **Scenario MONSTER-RAISE**: Hero holds a set or better (`is_monster=1`). Villain bets (first bet on the street, so `facing_raise=0`). Multiple board textures.
- The monster + facing initial bet combination must be explicitly constructed. Self-play oracles facing bets with strong hands will fold if the oracle is miscalibrated; factory construction ensures the desired feat_dict values.

### Gap 7: Rule 11 boundary scenarios (UPDATED — R5 texture variation)

**Target**: Paired/2-tone boards, OOP made hand, villain_top_pair_plus_pct crossing the 0.40 threshold (CHECK default vs BET override).

**CORRECTED spec (R5 fix)**: The original blueprint did not specify board texture variation across the 5 boundary pairs. Using the same board type for all 5 pairs risks the model learning a spurious board-texture confound (e.g. "2-tone K-high board → flip at 0.40" rather than "any paired/2-tone board → flip at 0.40").

**Required**: Use ≥3 different board textures across the 5 boundary pairs. Each texture must be GTO-meaningful for the rule's threshold (Rule 11 applies to paired/2-tone boards where villain's value-heavy vs. air composition determines whether hero's OOP medium-strong hand should bet or check for protection/value).

**Specified texture assignments for the 5 boundary pairs**:

| Pair # | Board texture | Example board | GTO rationale |
|--------|--------------|---------------|---------------|
| 1 | Dry paired | KcKd4s (rainbow) | Villain connects strongly to Kx combos; at TP+ >= 0.40, those Kx hands call bets; below 0.40, range is dominated by air that folds |
| 2 | 2-tone paired | KdTd4c | Villain has flush draw equity in addition to Kx combos; TP+ threshold still meaningful because bet for value vs Kx; below 0.40, flush draw calls but pair combos absent |
| 3 | Dynamic paired (connected) | 8h8d7c | Villain's range smashes connected boards with sets/straights but is rich in air on dry days; threshold separates "villain has made hands to bet into" from "villain range is draw-heavy and folds to bets" |
| 4 | Monotone | 9h6h3h | Villain's range dramatically split: flush combos (strong made) vs. offsuit holdings (air); TP+ composition shifts sharply; threshold still applies to OOP hero's BET vs CHECK |
| 5 | Draw-heavy paired | JsTd4d (two-tone, medium connected) | Villain has both pair combos and draw combos; TP+ boundary is most meaningful here as a separator between "enough made hands to extract from" and "draw-heavy range that bets out to protect" |

**Justification per texture**: Each texture is GTO-meaningful for Rule 11 because Rule 11's 0.40 threshold governs whether hero's OOP strong-made hand can bet for value (villain range has enough TP+ to call) vs. check to protect (villain range is too air-heavy and folds to bets, leaving hero value-cutting). The threshold operates on the composition of villain's range — a variable that genuinely differs across board textures. Five different textures produce five different contexts where the same threshold applies for distinct poker-theoretic reasons.

**Note**: The 0.40 threshold is provisional per gto-expert review (not solver-exact); it reflects the empirical failure cases d3688 and d9556. The model should learn the boundary in context across varied textures, not a crisp single-board cutoff.

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

**Pool decomposition** (9 scenario families, up from 7):

| Generation source | Target pool hands | Expected yield for corpus |
|---|---|---|
| Self-play (opener decisions, with SPR fix and PFA capture) | 1000 | ~200 checker/bettor hands for CHECK/BET stratum |
| SituationFactory - PFA c-bet scenarios | 300 | ~100 PFA hands (Rule 4 stratum) |
| SituationFactory - facing initial bet (CALL/RAISE/FOLD) | 400 | ~150 facing-bet hands |
| SituationFactory - bet-and-call (BAC) scenarios | 200 | ~50 BAC hands |
| SituationFactory - multi-street aggression (MAGG) | 200 | ~50 MAGG hands |
| SituationFactory - nut-FD facing bet (NFD) | 100 | ~25 NFD hands (boundary coverage) |
| SituationFactory - monster facing bet | 100 | ~25 monster-facing-bet hands |
| SituationFactory - donk-bet defence (Module 8, new) | 80 | ~25-30 donk-defence hands |
| SituationFactory - SB-as-hero sandwich (Module 9, new) | 70 | ~20-25 SB-hero hands |
| **Total pool** | **~2450** | **~645 candidates for 500 selection** |

The 645-candidate post-filter pool provides adequate oversampling ratio for the 400-hand selection step. Adding 2 modules increases pool size by ~150 hands, well within the same compute envelope.

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
| Multi-street aggression fold (villain_aggression >= 2, river decision) | 20 | MAGG factory scenarios |
| Standard SPR (4-8) hands | 50 | Self-play (SPR fixed) + factory |
| Medium SPR (2-4) hands | 40 | Self-play (SPR fixed) + factory |
| Boundary cases: Rule 11 threshold (villain_tp_pct 0.35-0.45) | 10 | Rule 11 boundary scenarios (≥3 textures) |
| Donk-bet defence hands (Module 8) | 25 | Donk-bet defence scenarios |
| SB-as-hero sandwich hands (Module 9) | 20 | SB-hero scenarios |
| **Phase A total** | **355** | — |

*Note: Phase A total increases from 310 to 355 due to Modules 8 and 9. Phase B stratified fill adjusts from 90 to 45 hands. Total new hands remains 400.*

**Phase B: Stratified fill (remaining 45 hands)**

The remaining 45 hands are drawn from the general pool using the 8-dimension stratified sampler:

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

### Post-generation validation of NFD boundary hands (R4)

**New step added between pool generation and corpus assembly.**

After generating the NFD boundary hands (villain_air_pct targets: 0.15, 0.17, 0.20, 0.22, 0.25), validate the **actual computed** `villain_air_pct` from `feature_extractor` against the target values.

**Validation rule**: For each NFD boundary hand, the actual `feat_dict['villain_air_pct']` must satisfy:
```
|actual_villain_air_pct - target_villain_air_pct| <= 0.03
```

**Failure action**: Any hand where the actual value drifts from the target by more than 0.03 must be filtered out and replaced before corpus assembly. The boundary coverage requires exactly 5 hands straddling the threshold; hands that miss the target range by more than ±0.03 land in the wrong bucket (e.g. a hand targeted at villain_air=0.20 but computing as 0.25 is effectively a RAISE case, not a boundary case).

This validation runs in the corpus assembly script as a mandatory pre-labelling gate, before any NFD boundary hands enter the Phase A quota.

**Where it runs**: `scripts/build_corpus_revision_500_hand.py` — in the Phase A quota allocation loop, after NFD hands are pulled from the pool but before they are written to the candidate set. Failed hands are flagged to stderr; the script must regenerate replacements or fail with an informative error message.

### Handling rare-class imbalance

The synthesis target action distribution (CHECK 30% / BET 27% / CALL 17% / RAISE 14% / FOLD 12%) requires deliberate oversampling of RAISE and FOLD relative to their natural frequency.

Natural frequency in 3-way play: CHECK ~45% / BET ~30% / CALL ~10% / RAISE ~5% / FOLD ~8%.
Target vs natural: RAISE is oversampled ~3x; FOLD is oversampled ~1.5x; CHECK is undersampled.

**Handling approach**: Phase A's mandatory quotas inject the rare-class hands first. Phase B's stratified fill uses action context (opener/facing_bet/facing_raise) as the primary stratification dimension, ensuring that the pool of facing-bet hands is sampled proportionally to yield the target CALL/RAISE/FOLD distribution.

Specifically: among the 45 Phase B hands, target:
- ~10 checker/bettor hands (CHECK/BET outcomes from opener decisions)
- ~20 facing-initial-bet hands (CALL/RAISE/FOLD outcomes)
- ~15 facing-raise hands (CALL/FOLD outcomes)

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
donk_bet_defence_count >= 25    # Module 8 Phase A quota met
sb_hero_count >= 20             # Module 9 Phase A quota met
magg_villain_aggression_2_count >= 20  # MAGG hands at river decision point
```

Note: action distribution cannot be verified before labelling, since labels are assigned by labellers post-corpus-build. The structural checks (facing_bet, pfa, spr, oop/ip) CAN be verified pre-labelling from feat_dict values. The action distribution check is estimated from the expected labels given the hand structures.

---

## Q5 — Disjointness preservation

### Existing disjointness mechanism

The Build C v1.0.1 script (`scripts/build_pilot_corpus_100_hand.py`) implements fingerprint-based deduplication. The fingerprint is `(sorted(hero_cards), sorted(board_cards))` — a card-equivalence-class check.

Fingerprint sets currently locked:
- **Stage 6 holdout**: 49 fingerprints, anchored at SHA256 `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- **v2.3 calibration (24-hand legacy)**: 21 fingerprints
- **v2.3 anchor (9-hand extension)**: 9 fingerprints
- **Tier 1 (existing 33)**: 33 fingerprints from `review/calibration_grading_key.json`
- **Tier 2 (existing 100)**: 100 fingerprints from `data/pilot_corpus_100_hand_2026-04-26.jsonl`
- **Total forbidden**: 79 fingerprints (deduplicated)

### Disjointness protocol for the 400 new hands

The new corpus-builder script must:

1. Load all existing forbidden fingerprint sets (holdout, v2.3 calibration, v2.3 anchors, Tier 1, Tier 2 existing 100).

2. Before selecting any candidate hand, check its fingerprint against ALL forbidden sets.

3. After selection, perform post-hoc verification:
   - No overlap with Stage 6 holdout
   - No overlap with Tier 1 calibration (expanded to 45 hands)
   - No overlap with existing 100 Tier 2 hands (after re-extraction, same fingerprints)
   - No within-batch duplicates

4. Produce a new lock file `data/pilot_corpus_500_hand_2026-04-27.lock.json` recording counts and all-zero overlap attestations.

**Re-attestation after re-extraction (Path A)**: After re-extracting the 100 existing hands (R1), verify that fingerprints are unchanged (hero_cards and board_cards are not modified by re-extraction — only feat_dict is updated). Update the lock file SHA256 for the 100-hand JSONL. The disjointness attestation remains valid.

### Factory-generated hands and disjointness

Hands generated via `SituationFactory` have explicitly specified `hero_cards` and `board_cards`. Disjointness check must be applied at scenario-spec generation time (before any labelling), not only at corpus sampling time.

**Required (ml-architect N3)**: The scenario-spec generator must accept a `forbidden_fingerprints: set` parameter and update it **incrementally** across all 9 scenario families. When scenario family N runs, `forbidden_fingerprints` should already include all fingerprints from families 1 through N-1 (plus the external forbidden sets). This prevents inter-scenario-family fingerprint collisions (e.g. an NFD hand and a monster-facing-bet hand independently specifying the same hero cards on the same board).

**Implementation**: The `generate_scenarios()` dispatcher function in `generate_corpus_revision_pool.py` calls scenario families in sequence, threading the updated `forbidden_fingerprints` set through each call:

```python
fp_set = load_all_forbidden_fingerprints()  # external forbidden sets
for generator_fn in [
    generate_pfa_scenarios,
    generate_facing_initial_bet_scenarios,
    generate_bac_scenarios,
    generate_magg_scenarios,
    generate_nfd_scenarios,
    generate_monster_facing_bet_scenarios,
    generate_rule11_boundary_scenarios,
    generate_donk_bet_defence_scenarios,  # Module 8
    generate_sb_hero_scenarios,           # Module 9
]:
    new_records = generator_fn(forbidden_fingerprints=fp_set)
    fp_set.update(fingerprint(r) for r in new_records)
    all_records.extend(new_records)
```

### Lock file structure (new 400-hand batch)

```json
{
  "corpus_revision_version": "v2.0",
  "new_hand_count": 400,
  "combined_corpus_count": 500,
  "sha256_new_400": "<hash of 400-hand JSONL>",
  "sha256_combined_500": "<hash of 500-hand JSONL>",
  "sha256_reextracted_100": "<hash of re-extracted 100-hand JSONL>",
  "byte_size_combined": "...",
  "build_seed": 20260427,
  "generation_sources": {
    "self_play_with_spr_fix": {"pool_size": "...", "selected": "..."},
    "factory_pfa_scenarios": {"pool_size": "...", "selected": "..."},
    "factory_facing_bet": {"pool_size": "...", "selected": "..."},
    "factory_bac": {"pool_size": "...", "selected": "..."},
    "factory_magg": {"pool_size": "...", "selected": "..."},
    "factory_nfd": {"pool_size": "...", "selected": "..."},
    "factory_monster_facing_bet": {"pool_size": "...", "selected": "..."},
    "factory_donk_bet_defence": {"pool_size": "...", "selected": "..."},
    "factory_sb_hero": {"pool_size": "...", "selected": "..."}
  },
  "disjointness": {
    "stage6_holdout_fingerprints": 49,
    "tier1_calibration_fingerprints": 45,
    "tier2_existing_100_fingerprints": 100,
    "v23_calibration_fingerprints": 21,
    "v23_anchor_fingerprints": 9,
    "total_forbidden_fingerprints_deduplicated": "...",
    "post_sample_overlap_holdout": 0,
    "post_sample_overlap_tier1": 0,
    "post_sample_overlap_existing_100": 0,
    "post_sample_overlap_within_new_400": 0
  },
  "structural_verification": {
    "facing_bet_count": "...",
    "pfa_count": "...",
    "spr_ge_4_count": "...",
    "spr_2_to_4_count": "...",
    "oop_count": "...",
    "ip_count": "...",
    "magg_villain_aggression_2_count": "...",
    "donk_bet_defence_count": "...",
    "sb_hero_count": "...",
    "zero_instance_rules_coverage": {"...": "..."},
    "poker_pattern_coverage": {"...": "..."}
  },
  "reextraction": {
    "script": "scripts/reextract_pilot_100_features.py",
    "original_sha256": "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40",
    "reextracted_sha256": "<updated hash>",
    "labels_unchanged": true,
    "fingerprints_unchanged": true
  },
  "predecessor_corpus_hash": "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40"
}
```

---

## Q6 — Pipeline interface

### Files to create

**1. `river-rats-core/generate_corpus_revision_pool.py`** — new source-pool generation script

This script generates the ~2450-hand candidate pool for the 400 new hands. It has two generation modes:

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

Uses `SituationFactory.build_situation()` to generate hands from explicit scenario specs. Nine scenario families (7 original + 2 new):

- `generate_pfa_scenarios()` — PFA c-bet decisions (Rule 4 pattern)
- `generate_facing_initial_bet_scenarios()` — initial-bet response decisions (CALL/RAISE/FOLD)
- `generate_bac_scenarios()` — bet-and-call sandwich (MW-30 pattern)
- `generate_magg_scenarios()` — multi-street aggression response (MW-50 pattern; river decision point, villain_aggression_count=2)
- `generate_nfd_scenarios()` — nut-FD facing bet (KB §1.7 pattern; with post-generation validation)
- `generate_monster_facing_bet_scenarios()` — set/monster facing initial bet (MW-33 pattern)
- `generate_rule11_boundary_scenarios()` — Rule 11 threshold boundary pairs (≥3 board textures)
- `generate_donk_bet_defence_scenarios()` — donk-bet defence scenarios (Module 8, new)
- `generate_sb_hero_scenarios()` — SB-as-hero sandwich scenarios (Module 9, new)

Each scenario function signature: `generate_scenarios(forbidden_fingerprints: set) -> list[dict]`. The forbidden_fingerprints set is threaded incrementally through all 9 families (see Q5).

**Module 8: Donk-bet defence scenarios**

Hero is IP (BTN or CO), facing an OOP donk lead on the flop from the BB (non-PFA).

- **Hero position**: BTN or CO (in-position, not the PFA)
- **Villain (donk bettor)**: BB (OOP, not PFA) — leads into the CO and BTN
- **Action history template**: `[('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'), ('flop', 'BB', 'bet')]`
  - Preflop: PFA is CO, BTN flats, BB calls (3-way)
  - Flop: BB leads into CO and BTN (donk bet from OOP non-PFA)
  - Hero (BTN or CO) faces the donk bet
- **Range dynamics**: BB's donk-betting range is polarised — either strong (sets, two-pair, top pair on specific boards) or air (low equity hands leading to deny equity). Hero's IP uncapped range can respond with CALL / RAISE / FOLD depending on hero hand strength and villain's donk range composition.
- **Decision tree**: Hero faces donk → CALL (good but not raiseable hand), RAISE (monster or semi-bluff with equity), or FOLD (air/weak hand with no equity vs. donk range).
- **Spec target**: ~25-30 hands across the 9-module corpus (Phase A: 25 mandatory slots).
- **Key structural differences from Module 2 (facing_initial_bet)**: The bettor is OOP (BB), not IP (opener's continuation bet). The bettor is the non-PFA. Villain's range is more polarised than a c-bet range.

**Module 9: SB-as-hero sandwich scenarios**

Hero is the SB, sandwiched between an earlier-position aggressor and a later-position caller. Real role-asymmetry currently at ~3% of the existing corpus.

- **Hero position**: SB (OOP to the BTN and CO, IP to the BB — sandwich position)
- **Villain aggressor**: BTN or CO (opened preflop, potentially betting postflop)
- **Villain caller**: BB or a separate caller behind
- **Action history template**: `[('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'), ('flop', 'CO', 'bet')]`
  - Preflop: CO opens, BTN calls, SB calls, BB folds (3-way to flop with SB as hero)
  - Flop: CO bets into SB (hero) and BTN
  - Hero (SB) faces the c-bet with BTN behind
- **Role asymmetry captured**: SB is OOP to both CO and BTN. Hero's continuing standard is tighter than BB because the BTN may yet raise. SB MDF (~20%) is tighter than BB MDF (~33%). This produces systematically higher FOLD rates from SB than BB in similar structural spots.
- **Spec target**: ~20-25 hands across the 9-module corpus (Phase A: 20 mandatory slots).
- **Variants**: Include hands where BTN has acted (folded or called) before hero's decision, and hands where BTN is yet to act (pure sandwich). Also include SB-as-hero facing a BTN c-bet (preflop opener was UTG/HJ/CO; BTN calls preflop; SB calls preflop; BTN bets flop with UTG/HJ/CO behind).

**Pre-training feature schema compatibility check (R2)**

Added to the pipeline as a mandatory gate before warm-start training kickoff (not before corpus generation — this is a training-phase gate specified here for completeness).

**`scripts/verify_feature_schema_compatibility.py`** — standalone verification script:

- Load the warm-start base model artifact (v8 oracle model from `river-rats-core/models/`)
- Extract the model's feature column list (from `model.json` or the training artifact's `FEATURE_COLUMNS` metadata)
- Compare against the 59-feature corpus contract (`FEATURE_COLUMNS` in `river-rats-core/feature_keys.py`)
- **Pass condition**: Exact match — same columns, same count, same order (XGBoost warm-start requires identical feature schemas)
- **Fail condition**: Any mismatch. Script must exit with non-zero status and print specific column diffs (missing columns, extra columns, order differences)

**Usage**:
```bash
python3 scripts/verify_feature_schema_compatibility.py \
  --model river-rats-core/models/v8_oracle.json \
  --feature-keys river-rats-core/feature_keys.py
# Exit 0: PASS — feature schemas match
# Exit 1: FAIL — diff printed to stderr
```

This is a gate before `scripts/train_warm_start.py` runs. If it fails, the programmer must STOP and report BLOCKED; do not attempt warm-start training with mismatched feature schemas.

---

**2. `scripts/reextract_pilot_100_features.py`** — re-extraction of existing 100 hands (Path A, R1)

This script re-extracts the 59 feature dict for each of the 100 existing pilot hands using corrected inputs, without modifying labels.

**Algorithm**:

1. Load `data/pilot_corpus_100_hand_2026-04-26.jsonl` (100 hands, 59 features each — currently with `is_preflop_aggressor=0` for all and `spr=1.25` for 94%).

2. For each hand, reconstruct `_opener_position` from the hand's `prior_actions` (action history). The opener is the first player who made a preflop bet (raise). If `prior_actions` does not contain preflop action, `_opener_position` remains None (the feature defaults to 0, which is correct for non-PFA decisions).

3. Recompute `pot_size` in BB units: `pot_bb = pot_chips / BB_CHIP_SIZE` where `BB_CHIP_SIZE=10`. The raw chip-unit pot is stored in the existing record's `pot` field.

4. Call `feature_extractor.extract_all_features(hand_dict)` with:
   - `_opener_position`: reconstructed from step 2
   - `pot`: `pot_bb` from step 3 (BB units, not chip units)
   - All other hand fields unchanged from the original record

5. Write the updated 100-hand JSONL to `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` — same structure as the original, with `feat_dict` replaced by the corrected 59-feature dict.

**Invariants to preserve**:
- Labels: do NOT re-run labelling. If the original record has a `label` field (or the labels are stored in a separate file keyed by `pilot_hand_id`), labels remain untouched. Labels were assigned based on the poker situation, not the feature values.
- Fingerprints: hero_cards and board_cards are not modified. Disjointness attestation remains valid.
- pilot_hand_id: unchanged (PILOT_001 through PILOT_100).

**Verification**:
- Assert: after re-extraction, at least 30 of 100 hands have `is_preflop_aggressor=1` (the existing pool should have ~30% opener decisions; if all remain 0, the opener reconstruction failed).
- Assert: `mean(spr)` across 100 re-extracted hands is between 5.0 and 15.0 (was 1.25; should be ~8-12 for standard flop situations).
- Assert: fingerprints of all 100 re-extracted hands match the fingerprints in the original lock file (SHA256 of fingerprint set unchanged).

**Update the lock file**: After re-extraction, update `data/pilot_corpus_100_hand_2026-04-26.lock.json` with the new SHA256 of the re-extracted JSONL, noting `reextracted_from: original_sha256` for provenance.

**Disjointness re-attestation**: After re-extraction, re-run the disjointness check (fingerprint-only, since fingerprints are unchanged). This is a quick verification step before combining with the 400 new hands.

**CLI**:
```bash
python3 scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --bb-chip-size 10 \
  --verify
```

---

**3. `scripts/build_corpus_revision_500_hand.py`** — new corpus assembly script

This script assembles the combined 500-hand corpus from:
- The 100 re-extracted existing hands (`data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`)
- 400 new hands sampled from `training-data/corpus_revision_pool_2026-04-27.jsonl`

It follows the same structure as `scripts/build_pilot_corpus_100_hand.py` but with:
- 8-dimension stratification instead of 5-dimension
- Phase A mandatory quota allocation (355 hands) before Phase B stratified fill (45 hands)
- Additional disjointness checks (including against existing 100 hands)
- NFD boundary validation gate (R4) in Phase A allocation
- Structural verification gate
- Unified output with consistent `pilot_hand_id` numbering

**CLI entry point**:
```bash
python3 scripts/build_corpus_revision_500_hand.py \
  --pool training-data/corpus_revision_pool_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 \
  --seed 20260427 \
  --output data/pilot_corpus_500_hand_2026-04-27.jsonl \
  --lock-output data/pilot_corpus_500_hand_2026-04-27.lock.json
```

**Output artifacts**:
- `data/pilot_corpus_500_hand_2026-04-27.jsonl` — combined 500-hand corpus (100 re-extracted + 400 new)
- `data/pilot_corpus_500_hand_2026-04-27.lock.json` — lock file with disjointness attestation, structural verification, and SHA256

---

**4. Scenario spec files** — in `river-rats-core/corpus_revision_scenarios/`

Each scenario family lives in a separate Python module for readability (9 modules total):
- `corpus_revision_scenarios/pfa_scenarios.py`
- `corpus_revision_scenarios/facing_initial_bet_scenarios.py`
- `corpus_revision_scenarios/bac_scenarios.py`
- `corpus_revision_scenarios/magg_scenarios.py` — CORRECTED: extends action histories to river
- `corpus_revision_scenarios/nfd_scenarios.py`
- `corpus_revision_scenarios/monster_facing_bet_scenarios.py`
- `corpus_revision_scenarios/rule11_boundary_scenarios.py` — UPDATED: ≥3 board textures
- `corpus_revision_scenarios/donk_bet_defence_scenarios.py` — NEW (Module 8)
- `corpus_revision_scenarios/sb_hero_scenarios.py` — NEW (Module 9)

Each module exports: `generate_scenarios(forbidden_fingerprints: set) -> list[dict]`.

**Important**: Do not modify `generate_3way_situations.py` (preserve existing pool generator). The new generator is a parallel script.

---

### Configuration / parameter files

No separate config file is required. All parameters are CLI arguments with documented defaults. The seed (20260427) is the only parameter that must be kept stable across reruns for reproducibility.

The `BB_CHIP_SIZE = 10` constant (used in the pot-to-BB conversion for self-play) should be defined at the top of `generate_corpus_revision_pool.py` as a named constant, matching `poker_game.py`'s `PokerGame.BIG_BLIND = 10`. This same constant is used in `reextract_pilot_100_features.py`.

---

## Q7 — Integration with existing 100 hands

### Path A adopted: re-extract existing 100 hands

**Decision (locked per synthesis, three-way convergence: ml-architect + QC + gto-expert)**: Re-extract the 100 existing pilot hands with corrected `_opener_position` and BB-unit pot values before assembling the combined 500-hand corpus.

**Why this is required**:

The 100 existing hands have two systematic feature errors:
1. `is_preflop_aggressor=0` for all 100 hands, including hands that are actually opener decisions. This is a generation-layer omission (pool records never captured `game.opener_position`).
2. `spr=1.25` for 94/100 hands due to the chip/BB unit mismatch. The true game SPR was ~12.5 for these standard-depth decisions.

If accepted without re-extraction (the original blueprint's OQ-1 "accept mixed" recommendation), training on the combined corpus creates a spurious correlation: `spr=1.25` marks the 100 old hands as a distinct regime from the new 400 hands. The model may use `spr` to distinguish between corpus-source batches rather than to model poker-meaningful committed-stack decisions. The ml-architect verified this as a training-quality issue, not merely a distributional imbalance.

Re-extraction is low-cost (2-4 dev hours), requires no relabelling (labels are tied to game state, not feature vectors), and preserves all 100 valid poker situations and their $15-25 worth of labels.

**Labels are NOT re-run**: The 500 labels from Phase B Protocol A (master `4bce49f`) remain exactly as produced. Only the `feat_dict` is updated. The re-extracted JSONL (`data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`) contains corrected feature dicts with unchanged labels.

### Schema compatibility

The re-extracted 100 hands use the same 59-feature contract schema as the 400 new hands. Both sources produce the same top-level structure:

```
{pilot_hand_id, source_situation_id, deal_id, hero_cards, board, street,
 hero_position, villain_positions, pot, to_call, facing_bet, num_opponents,
 prior_actions, feat_dict (59 features, correct SPR, correct is_preflop_aggressor)}
```

### Unified pilot_hand_id numbering

The 100 existing hands are `PILOT_001` through `PILOT_100`. The 400 new hands are `PILOT_101` through `PILOT_500`. The combined file lists re-extracted hands first (in their original order), followed by new hands ordered by generation source.

### Unified lock file

The combined lock file documents both source provenances, including re-extraction provenance:

```json
{
  "stratum_0_reextracted_100": {
    "source": "data/pilot_corpus_100_hand_2026-04-26_v2.jsonl",
    "original_source": "data/pilot_corpus_100_hand_2026-04-26.jsonl",
    "original_sha256": "c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40",
    "reextracted_sha256": "<updated hash>",
    "labels_unchanged": true,
    "reextraction_script": "scripts/reextract_pilot_100_features.py",
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
- Tier 3 holdout (49 fingerprints): re-verified across all 500 hands
- Tier 1 calibration (45 fingerprints after expansion): re-verified across all 500 hands

The lock file must record all 500 hands' fingerprint set and confirm zero overlap with Tier 1 and Tier 3. Since re-extraction does not change hero_cards or board_cards, fingerprints are unchanged and this re-verification is expected to pass trivially — but must be run and recorded.

---

## Q8 — Risks and dependencies

### Risk 1: v3.2 rule gaps surfaced by new patterns (HIGH)

**Risk**: When the factory scenarios generate hands for multi-street aggression, bet-and-call, PFA c-bets, donk-bet defence, and SB-as-hero, the v3.2 protocol may not have explicit rules for some configurations. Labellers will encounter spots where v3.2's rules produce an ambiguous or incorrect recommendation.

**Specific flagged patterns**:

- **PFA c-bet on monotone board as aggressor, range advantage**: v3.2's Rule 4 says "don't auto-c-bet IP" but does not specify frequency targets by board texture as PFA.
- **Multi-street aggression fold on the river**: v3.2 has MW-50 (medium_made facing raise + aggression) but the boundary between CALL and FOLD on the river after villain bet two streets is not explicitly calibrated.
- **Bet-and-call on a draw-heavy board (hero has draw)**: KB §1.7 says RAISE is correct ONLY with nut FD + blocker. Non-nut-FD draws in a sandwich should CALL or FOLD. The CALL vs FOLD boundary for non-nut draws in BAC situations is not explicitly covered by v3.2.
- **Donk-bet defence**: v3.2 has no explicit rule for responding to OOP donk bets. The range dynamics (donker is polarised) require inference from first principles.
- **SB-as-hero**: v3.2's continuing standards are documented for BB more than SB. The SB's tighter MDF (~20% vs BB's ~33%) may not be explicitly encoded.

**Mitigation**: Per synthesis (Q2 disposition): **defer v3.3 decision until Build E sample inspection.** Run GTO-expert review on 30 factory-generated hands (including sample hands from Modules 8 and 9) before mass labelling. If labeller disagreement exceeds 2 of 5 on any spot type, dispatch protocol revision before labelling the full 400-hand batch. Do not speculate on v3.3 need; let the corpus tell us.

### Risk 2: SPR calibration set inconsistency (MEDIUM)

**Status**: Substantially mitigated by Path A (re-extraction). After re-extraction, the 100 existing hands will have corrected SPR values (~8-12 for standard-SPR flop decisions). The Tier 1 expansion (33→45) should still include ≥5 hands with SPR >= 4.0 to calibrate labellers on the full SPR range they will encounter in the 400 new hands.

### Risk 3: Factory-generated hands have different feature distributions than self-play hands (MEDIUM)

**Risk**: `SituationFactory` hands have explicitly specified pot, to_call, and action_history. Villain range composition features may be plausible in isolation but not jointly realistic (e.g. high `villain_air_pct` on a board where villain's position smashes the texture).

**Mitigation**: GTO-expert must review 20-30 factory-generated hands across all 9 modules before mass generation. This is mandatory, not optional (blueprint Risk 3 mitigation). Specifically verify for Modules 8 and 9:
- Module 8 (donk-bet defence): villain's donk-betting range is plausibly polarised; `villain_top_pair_plus_pct` is higher than a standard c-bet range (donkers lead with strong hands more than air in balanced strategies)
- Module 9 (SB-hero): hero's SPR and position reflect a realistic SB-vs-CO 3-way scenario; hero's `is_preflop_aggressor=0` (hero called preflop) is correctly populated

Additionally (ml-architect N2, nit): before mass generation, run a pairwise correlation check between `villain_air_pct`, `villain_top_pair_plus_pct`, `villain_draw_pct`, and `villain_aggression_count` across the factory pool. Compare to the same correlations in the self-play pool. Flag if any pairwise correlation differs by > 0.3. This is a 30-minute analysis step, not a code change, but it catches joint-distribution issues that individual hand review may miss.

### Risk 4: Compute time for pool generation (LOW)

**Estimate**: 1000 self-play deals + 1450 factory scenario hands ≈ 30-70 minutes total (same estimate as original blueprint plus ~10-15 min for 2 additional modules). Acceptable.

**Mitigation**: Run self-play component first with `--mode self_play` to get the self-play pool early. Factory scenarios can run in parallel if needed.

### Risk 5: Solver bandwidth for Tier 1 expansion (EXTERNAL DEPENDENCY)

**Status per synthesis (Q3 disposition)**: Tier 1 expansion is **informational, not a strict gate**. Tier 1 runs in parallel with Tier 2 labelling. If Tier 1 expansion surfaces v3.3-required gaps mid-way through Tier 2 labelling, we can pause Tier 2 at that point. This is preferable to blocking the critical path on the calibration set.

**Recommendation to Tier 1 architect (from gto-expert, noted for handoff)**: Add 1-2 calibration hands for the MAGG FOLD pattern (villain_aggression_count=2, hero medium made, FOLD on river) as part of the Tier 1 expansion. Labellers encountering 20+ MAGG scenarios in the main corpus without calibration exposure to this pattern may produce inconsistent labels.

### Risk 6: Feature additions dependency (LOW)

**Risk**: ml-architect recommended two optional feature additions (`hero_range_is_capped`, `villain_checked_back_turn`). If added between now and mass-labelling, corpus rebuild would be needed.

**Mitigation**: Do NOT add any new features before corpus generation is complete. Feature additions, if approved, should be a post-labelling change that triggers a corpus rebuild only if the reference gate fails.

### Risk 7: Model training warm-start with combined corpus (LOW)

**Status**: Substantially mitigated by Path A. After re-extraction, the combined 500-hand corpus has consistent SPR values across both the 100 re-extracted and 400 new hands. The spurious SPR-as-corpus-source-indicator risk is eliminated.

**Remaining mitigation**: The combined 500-hand corpus should still be shuffled before training (not batched with existing-100 first, new-400 second). Class weighting via standard inverse-frequency weighting. No additional source weighting.

---

## Implementation handoff

### Files to create or modify

| Action | File | Description |
|---|---|---|
| CREATE | `river-rats-core/generate_corpus_revision_pool.py` | New pool generator (Mode A: self-play with SPR fix; Mode B: 9 factory scenario families) |
| CREATE | `river-rats-core/corpus_revision_scenarios/__init__.py` | Package init |
| CREATE | `river-rats-core/corpus_revision_scenarios/pfa_scenarios.py` | PFA c-bet scenario specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/facing_initial_bet_scenarios.py` | Initial-bet response specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/bac_scenarios.py` | Bet-and-call sandwich specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/magg_scenarios.py` | Multi-street aggression specs (CORRECTED: river decision point, villain_aggression_count=2) |
| CREATE | `river-rats-core/corpus_revision_scenarios/nfd_scenarios.py` | Nut-FD facing-bet specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/monster_facing_bet_scenarios.py` | Monster facing bet specs |
| CREATE | `river-rats-core/corpus_revision_scenarios/rule11_boundary_scenarios.py` | Rule 11 threshold boundary pairs (UPDATED: ≥3 board textures per Q2 spec) |
| CREATE | `river-rats-core/corpus_revision_scenarios/donk_bet_defence_scenarios.py` | Module 8: donk-bet defence scenarios (new) |
| CREATE | `river-rats-core/corpus_revision_scenarios/sb_hero_scenarios.py` | Module 9: SB-as-hero sandwich scenarios (new) |
| CREATE | `scripts/reextract_pilot_100_features.py` | Re-extract existing 100 hands with corrected SPR + opener_position (Path A) |
| CREATE | `scripts/build_corpus_revision_500_hand.py` | Corpus assembly script (includes NFD boundary validation gate) |
| CREATE | `scripts/verify_feature_schema_compatibility.py` | Pre-training feature schema compatibility check (R2) |
| NO MODIFY | `river-rats-core/generate_3way_situations.py` | Preserve existing pool generator |
| NO MODIFY | `river-rats-core/feature_extractor.py` | Do NOT change DEFAULT_EFFECTIVE_STACK or SPR formula |
| NO MODIFY | `scripts/build_pilot_corpus_100_hand.py` | Preserve Build C v1.0.1 exactly |
| NO MODIFY | Labels at master `4bce49f` | Labels are preserved; only feat_dicts updated by re-extraction |

### Execution order

The scripts must run in this order:

1. **`scripts/reextract_pilot_100_features.py`** — re-extract the 100 existing hands first. Output: `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl`. Verify assertions (≥30 hands with `is_preflop_aggressor=1`, mean SPR in [5.0, 15.0], fingerprints unchanged).

2. **`river-rats-core/generate_corpus_revision_pool.py`** — generate the ~2450-hand candidate pool. Run smoke test first (Step 1 below), then full generation.

3. **GTO-expert review of 30 factory hands** — mandatory before mass generation (all 9 modules represented). Flag any range-composition issues. If Module 8 or 9 hands have implausible features, revise scenario specs before full pool run.

4. **`scripts/build_corpus_revision_500_hand.py`** — assemble combined 500-hand corpus. NFD boundary validation gate runs internally in Phase A quota allocation. Output: `data/pilot_corpus_500_hand_2026-04-27.jsonl` + lock file.

5. **`scripts/verify_feature_schema_compatibility.py`** — run before warm-start training kickoff (separate timing from corpus build; this is a training-phase gate). Must pass before any training script is run.

### Test plan

**Step 1: Smoke test the pool generator**
```bash
python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all --self-play-deals 20 --seed 20260427 \
  --output /tmp/smoke_test_pool.jsonl --stats-output /tmp/smoke_stats.json
```
Assert:
- Output pool >= 50 records
- At least 5 records with `is_preflop_aggressor=1`
- At least 5 records with `spr >= 4.0`
- At least 5 records with `facing_bet=1` and `facing_raise=0`
- At least 1 record with `num_callers_to_bet >= 1`
- At least 1 record with `villain_aggression_count >= 2`
- Zero records with `is_preflop_aggressor=None`
- **N1 (nit): Zero Mode A records with `spr < 2.0` AND `pot_chips > 60`** — regression test for unit-mismatch bug
- At least 1 record from `generation_source == "donk_bet_defence"` with OOP bettor
- At least 1 record from `generation_source == "sb_hero"` with `hero_position == "SB"`
- All MAGG records have `villain_aggression_count == 2` at decision point (not 1)

**Step 2: Smoke test re-extraction**
```bash
python3 scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output /tmp/smoke_reextracted.jsonl \
  --bb-chip-size 10 --verify
```
Assert: at least 30/100 hands have `is_preflop_aggressor=1`; mean SPR in [5.0, 15.0]; fingerprints unchanged.

**Step 3: Validate factory scenario outputs**
For each scenario family, spot-check 5 generated hands:
- PFA scenarios: `is_preflop_aggressor == 1`
- BAC scenarios: `num_callers_to_bet >= 1`
- MAGG scenarios: `villain_aggression_count == 2` (verify river decision point, NOT turn)
- NFD scenarios: `nut_flush_block == 1` and `has_flush_draw == 1`
- Monster-facing-bet scenarios: `is_monster == 1`
- Facing-initial-bet scenarios: `facing_bet == 1` and `facing_raise == 0`
- Rule 11 boundary scenarios: confirm ≥3 distinct board textures across the 5 boundary pairs
- Module 8 (donk): verify bettor is OOP (BB), hero is IP (BTN or CO), `facing_bet == 1`, `facing_raise == 0`
- Module 9 (SB-hero): verify `hero_position == "SB"`, hero is not PFA, villain is IP relative to hero

**Step 4: Run the corpus assembler on the smoke test pool**
```bash
python3 scripts/build_corpus_revision_500_hand.py \
  --pool /tmp/smoke_test_pool.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 10 \
  --seed 20260427 \
  --output /tmp/smoke_corpus.jsonl \
  --lock-output /tmp/smoke_lock.json
```
Assert: lock file shows 0 disjointness overlaps; structural verification passes; NFD boundary validation gate runs (may trivially pass at target-new=10 if no NFD boundary hands sampled, which is acceptable for smoke test).

**Step 5: Feature schema compatibility check**
```bash
python3 scripts/verify_feature_schema_compatibility.py \
  --model river-rats-core/models/v8_oracle.json \
  --feature-keys river-rats-core/feature_keys.py
```
Assert: exit 0 (PASS). If exit 1, do NOT proceed to warm-start training.

**Step 6: Full generation**
```bash
python3 scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --bb-chip-size 10 --verify

python3 river-rats-core/generate_corpus_revision_pool.py \
  --mode all --self-play-deals 1000 --seed 20260427 \
  --output training-data/corpus_revision_pool_2026-04-27.jsonl

python3 scripts/build_corpus_revision_500_hand.py \
  --pool training-data/corpus_revision_pool_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 --seed 20260427 \
  --output data/pilot_corpus_500_hand_2026-04-27.jsonl \
  --lock-output data/pilot_corpus_500_hand_2026-04-27.lock.json
```

**Step 7: Structural verification (before PR)**
Assert that lock file structural_verification section shows all targets met (see Q4 verification gate).

---

## Open questions for owner / orchestrator

### OQ-1: SPR unit consistency — RESOLVED

**Adopted decision**: Path A — re-extract the 100 existing pilot hands with corrected BB-unit pot conversion and `_opener_position` reconstruction. Three-way convergent recommendation: ml-architect (required fix), QC (Path A or C preferable over Path B), gto-expert (100+400 mix manageable with correction). Labels at master `4bce49f` are preserved. No relabelling needed. Implementation: `scripts/reextract_pilot_100_features.py` (new script, Implementation Handoff above).

### OQ-2: v3.3 protocol revision timing — DEFERRED PER QC

**Adopted decision**: Defer v3.3 decision until Build E source-pool generation + sample inspection. Do not speculate on whether v3.3 is needed before the corpus exists. If Build E sample inspection (GTO-expert review of 30 factory hands) surfaces patterns not covered by v3.2, surface as a protocol revision proposal at that point. This is the quality-first default: let the data tell us what the protocol needs, not our a priori predictions.

This disposition supersedes the original OQ-2 recommendation (option a: pre-labelling GTO-expert review, which was partially correct — the review still happens, but the v3.3 decision is explicitly deferred rather than treated as a likely outcome).

### OQ-3: Tier 1 expansion as labelling gate — RESOLVED (informational, not strict gate)

**Adopted decision**: Tier 1 expansion (33→45) runs in parallel with Tier 2 mass labelling, not as a strict prerequisite. Tier 1 is the QC harness for the labelling protocol; Tier 2 is the training corpus. They are independent artifacts. If Tier 1 expansion surfaces v3.3-required gaps mid-way through Tier 2 labelling, Tier 2 can pause and address. Blocking Tier 2 on Tier 1 would put Tier 1 on the critical path unnecessarily.

**For Tier 1 architect (handoff note)**: Include at least 5 hands with SPR >= 4.0 in the 12 new calibration additions (Risk 2 mitigation). Include 1-2 MAGG FOLD calibration hands before labellers encounter the multi-street aggression river fold in the main corpus (gto-expert recommendation, not this blueprint's scope to fully spec).

### New open questions surfaced by this update

**OQ-4**: Does `_opener_position` reconstruction from `prior_actions` (step 2 of re-extraction algorithm) produce correct results for all 100 existing hands? The `prior_actions` field stores action history as a list; the preflop opener is the player who first made a preflop bet. If `prior_actions` stores only postflop actions (the preflop action is not recorded), reconstruction will fail and all re-extracted hands will still have `is_preflop_aggressor=0`.

**Before programming**: The programmer must verify that `prior_actions` in the existing 100-hand JSONL includes preflop actions, OR confirm that the original pool records have a separate `opener_position` field that can be used directly. If neither is available, the re-extraction will correctly produce `is_preflop_aggressor=0` for all 100 hands (since `_opener_position` remains None), and the IS_PFA correction will come entirely from the 400 new hands. This would still be an improvement over the corrupt SPR values, and the ml-architect's primary concern about the SPR confound would be resolved even if IS_PFA remains 0 for the old hands.

**OQ-5**: The Phase A mandatory quota has increased from 310 to 355 hands (adding Modules 8 and 9). Phase B fill correspondingly drops from 90 to 45 hands. Does the reduced Phase B fill (45 vs 90) still provide adequate coverage of the 8-dimension stratification space? The 45 hands are distributed across 3 action contexts × 3 streets × 2 positions × 3 SPR buckets × 6 hand classes × 4 board textures (2592 cells), making most cells unreachable from 45 hands. Phase B's purpose is distributional fill, not exhaustive coverage — the 45 hands provide a distribution-broadening sample. If the orchestrator determines 45 hands is insufficient for distributional fill, two options: (a) reduce Phase A quotas slightly (e.g. drop Modules 8/9 mandatory quotas by 5 each), or (b) accept Phase B at 45 hands and note this in the lock file's structural_verification section. Quality-first default: proceed with 355/45 split and flag if structural verification gate fails.

---

## Nits folded into programmer phase (do not block)

These are small additions identified in the reviews; they do not block blueprint approval or programmer dispatch:

- **N1 (ml-architect)**: SPR regression assertion in smoke test — Zero Mode A records with `spr < 2.0` AND `pot_chips > 60`. Catches unit-mismatch regression if the new generator miscalculates the BB conversion. 5 lines added to smoke test. *(Already incorporated into Step 1 test plan above.)*

- **N2 (ml-architect)**: Pairwise correlation check between `villain_air_pct`, `villain_top_pair_plus_pct`, `villain_draw_pct`, and `villain_aggression_count` across factory pool vs. self-play pool. Flag if any pairwise correlation differs by > 0.3. Run before mass generation — a 30-minute analysis step. *(Incorporated into Risk 3 mitigation.)*

- **N3 (ml-architect)**: Incremental `forbidden_fingerprints` update during scenario spec generation — thread the `fp_set` through all 9 scenario families sequentially. *(Incorporated into Q5 disjointness protocol and the `generate_corpus_revision_pool.py` interface.)*

- **gto-expert recommendation**: +1-2 MAGG FOLD calibration hands as part of Tier 1 expansion. This is a recommendation to the Tier 1 architect, not a change to this corpus-generation blueprint. *(Noted in OQ-3 handoff.)*

---

*Blueprint v2 complete. No code written, no files modified except this document.*
*Next step: orchestrator dispatches round-2 reviewers (ml-architect + gto-expert + QC) with this updated blueprint. On reviews-2 convergence, lead-programmer dispatches.*
