---
date: 2026-04-27
from: gto-expert (audit subagent)
to: orchestrator
re: Action-distribution + range-pattern coverage audit
corpus: data/pilot_corpus_100_hand_2026-04-26.jsonl (100 hands, 63 unique deals)
labels_sample: review/pilot_run_2026-04-26/phase_b/labels_protocol_A_labeller_3.json (100 labels)
---

# GTO-expert audit: Action-distribution and range-pattern coverage

---

## Q1 answer — Action-vocabulary coverage

### Structural context (what's legal in each hand)

The 100-hand corpus has a single, overwhelming structural constraint:

| Context | Count | % of corpus |
|---------|-------|-------------|
| Not facing any bet or raise | 97 | 97% |
| facing_bet = 1 or facing_raise = 1 | 3 | 3% |

RAISE, CALL, and FOLD are only structurally possible in 3 hands. RAISE requires facing a bet or raise. CALL requires facing a bet. FOLD requires facing a bet or raise. All three legal constraints collapse to the same 3 situations.

Those 3 hands are: PILOT_021 (facing raise, turn), PILOT_029 (facing raise, river), PILOT_094 (facing raise, river). None are on the flop. Zero RAISE labels resulted — the 3 eligible hands resolved 2×FOLD, 1×CALL.

For the 97 checker/bettor hands, the legal menu is CHECK or BET only.

### Action likelihood under v3.2 (what the protocol produces)

Labeller 3 (richest output, 100 labels):

| Action | Count | % |
|--------|-------|---|
| CHECK | 57 | 57% |
| BET | 40 | 40% |
| FOLD | 2 | 2% |
| CALL | 1 | 1% |
| RAISE | 0 | 0% |

Across all 5 labellers, the distribution is 57-63 CHECK / 34-40 BET / 2-3 FOLD / 0-1 CALL / 0 RAISE, totalling approximately 300 CHECK / 185 BET / 13 FOLD / 3 CALL / 0 RAISE across 500 labels.

### What's structurally underrepresented by design

Three action classes are structurally blocked by corpus construction, not by the v3.2 protocol:

**RAISE (100% underrepresented — 0 labels):** Requires facing_bet = 1. Only 3 hands allow it. None produced a RAISE label because two were clear folds (air facing check-raise, near-zero equity) and one was a CALL (equity surplus over pot odds). The corpus has no hands that combine facing_bet=1 with the conditions KB §1.7 requires for semi-bluff RAISE (nut FD + blocker + villain_air_pct >= 0.20) or for value RAISE (monster facing bet). Zero RAISE labels is a corpus design problem, not a labeller failure.

**CALL (97% underrepresented — 1 label, 0.2% of 500):** Same structural cause. Only 3 hands allow it. One produced a CALL (PILOT_094: TPTK facing raise, equity surplus). A model trained on this corpus cannot learn when to CALL.

**FOLD (97% underrepresented — 13 labels total, 2.6%):** Only 3 hands create facing-bet contexts. 2 of 3 produce FOLD (correct). As a fraction of total labels, FOLD is near-statistical-noise territory for tree-based ML.

**The verdict:** The action-class imbalance is not a labeller reasoning problem — it is a corpus structural problem. 97% of hands do not allow three of the five action classes to appear.

---

## Q2 answer — Hand-class × board-texture × position × range-positioning matrix

### Hand class × board texture (counts from corpus)

|             | paired | 2-tone | dynamic | dry | mono |
|-------------|--------|--------|---------|-----|------|
| monster     |   6    |   5    |    1    |  4  |  1   |
| strong_made |  13    |   1    |    2    |  2  |  0   |
| made        |   0    |   7    |    0    |  10 |  2   |
| draw        |  10    |   3    |    1    |  7  |  2   |
| air         |  11    |   2    |    3    |  7  |  0   |

Note: "dynamic" here = connectivity_score >= 6 AND two-tone AND unpaired. "dry" = rainbow AND unpaired AND danger < 0.6. Cells do not add to 100 because texture categories overlap (a hand can be both paired and two-tone).

**Zero-coverage cells:**
- made × paired: 0 hands — medium-made hands on paired boards OOP (the canonical Rule 11 context for TPWK/second-pair) are absent as a standalone cell
- made × dynamic: 0 hands — TPWK/second pair on the most dangerous boards (connected + 2-tone, unpaired) absent
- strong × mono: 0 hands — strong made on monotone boards absent
- air × mono: 0 hands — bluff-catcher decisions on monotone boards absent

**Thin-coverage cells (1 hand each):**
- monster × dynamic: 1 hand
- monster × mono: 1 hand
- strong × 2-tone: 1 hand
- draw × dynamic: 1 hand

### Position distribution

| Position | OOP | IP | Total |
|----------|-----|----|-------|
| monster | 12 | 5 | 17 |
| strong | 14 | 4 | 18 |
| made | 15 | 4 | 19 |
| draw | 18 | 5 | 23 |
| air | 17 | 6 | 23 |
| **Total** | **76** | **24** | **100** |

IP hands are 24% of the corpus. Real-play IP-to-OOP ratios for 3-way postflop are closer to 40-50% IP for the closing-action player and 33-40% for the middle player. The corpus is heavily OOP-skewed, and this is likely a systematic bias from the deal-generation process — the BB defending position is over-represented (25 hands), while BTN (24), HJ (22), CO (16) are roughly reasonable, but SB (3) is severely underrepresented.

Critically: is_preflop_aggressor = 0 for ALL 100 hands. The preflop aggressor (the player who opened the pot) is never hero. This eliminates the c-bet decision class entirely — all "BET" labels in the corpus are donk bets, delayed leads, or river thin-value bets after checking through, not continuation bets by the aggressor. This is a severe gap.

### Range positioning distribution

| board_favour range | Count |
|-------------------|-------|
| > 0.2 (clear hero advantage) | 0 |
| 0.1 to 0.2 (slight advantage) | 3 |
| -0.1 to 0.1 (neutral) | 47 |
| -0.1 to -0.2 (slight disadvantage) | 21 |
| < -0.2 (clear disadvantage) | 29 |

The corpus has zero hands where the board clearly favours the hero's range. Hero is range-advantaged zero times. The model cannot learn what to do when it has a range advantage (which should support thinner value betting and higher c-bet frequency). The bias toward range-disadvantaged spots makes sense given BB-heavy composition (BB is often defending into the raiser's range advantage) but produces a one-sided training signal.

### SPR: a catastrophic uniformity problem

94% of all hands have SPR = exactly 1.25. The remaining 6 hands have SPR in the range 0.117 to 0.752. **Zero hands have SPR >= 2.0.** This means the corpus represents only one stage of the pot-tree: the compressed late-street decision after stack-to-pot has been compressed to near-commitment. The model cannot learn:

- Flop c-bet decisions at standard SPR (4-8)
- Turn barrel decisions at SPR 2-4
- Early-street fold decisions where pot is still small relative to stacks
- Any SPR-sensitive protection bet reasoning

This is the single most structurally severe limitation in the corpus.

---

## Q3 answer — Range-pattern coverage from poker theory perspective

### Pattern 1: Range advantage / disadvantage

**Corpus coverage: 0 hands with clear range advantage (board_favour > 0.2); 29 with clear disadvantage.**

The pattern is one-sided. A teaching corpus needs both sides to teach the concept: what do you do when the board smashes your range (A-high dry on a CO open) versus when it runs against you (low connected board where BB's speculative flats connect). The corpus has 29 disadvantaged spots but literally zero advantaged ones. This means the model sees no examples of the "I'm range-advantaged — bet tighter for value, check more draws" dynamic.

Boundary case risk: some hands in the corpus have neutral board_favour (-0.1 to 0.1) but are assigned CHECK due to Rule 11 (OOP paired/2-tone). These are not range-disadvantage checks — they are range-structure checks. The corpus does not distinguish these at the label level, which may cause the model to generalise "neutral board = check" incorrectly.

### Pattern 2: Polarised vs condensed range shapes

**Corpus coverage: 11 paired-board BB hands (polarised BB range context), roughly appropriate.**

Paired-low boards with BB as hero appear 11 times. This is meaningful coverage for the polarisation concept. However, the labeller (and the protocol) does not explicitly label these as "polarised-range" spots — the Rule 11 paired-board exception fires mechanically, and the reasoning cites Rule 11's predicate conditions rather than the underlying "BB's range is polarised between trips+ and air; betting intermediate hands is range-tipping" logic.

The boundary case that MUST be in the corpus: medium-made hand on a paired-low board where villain_top_pair_plus >= 0.40 (BET override fires) adjacent to an identical hand where villain_top_pair_plus = 0.35 (override doesn't fire, CHECK). These two spots teach the boundary of the polarisation protection rule. The corpus has 9 Rule-11-default-CHECK hands and 19 Rule-11-BET-override hands, but they are not systematically paired to teach the boundary — they are drawn from different deals with different board textures.

### Pattern 3: Capped ranges

**Corpus coverage: 48 hands where villain_range_capped = 1 (preflop-structural capped), 1 facing a bet from that capped range.**

The concept is present structurally (half the hands have a preflop-capped villain), but the labelling does not exercise it meaningfully. The v3.2 protocol (correctly) instructs agents to use the composition quad rather than the capped flag — but this means there are no labels explicitly testing the capped-range × aggressive action combination. The single facing-bet from a capped range (PILOT_094: TPTK facing raise from a capped villain) produces CALL due to equity, not due to range-cap reasoning. The model cannot learn that a capped villain's river check-raise is essentially impossible with value (not just "rare") — a nuance that affects CALL/FOLD frequency at these decision points.

### Pattern 4: Dominated kicker (TPWK on K/A-high boards)

**Corpus coverage: ~6 hands classifiable as TPWK-like (made, not strong, hero_range_percentile < 0.6).**

These 6 hands are the core of Rule 11's second clause: TPWK OOP on 2-tone boards where the BET override requires is_strong_made = 1 but hero is only is_made_hand = 1. PILOT_012, PILOT_036, PILOT_075, PILOT_083, PILOT_100 are examples. All correctly produce CHECK via Rule 11. But the corpus lacks the boundary case: TPWK on a dry rainbow board OOP where Rule 11 doesn't fire and BET is correct for thin value. Without this contrast, the model may over-generalise "TPWK = CHECK" beyond the Rule 11 scope.

Specific missing spot: TPWK on K72r rainbow unpaired (CO-favoured board) where hero is the preflop aggressor and villain_air_pct > 0.35. This should be a BET. Zero examples of this exist.

### Pattern 5: Nut-blocker semi-bluff

**Corpus coverage: 1 hand (PILOT_060), NOT facing a bet.**

PILOT_060 has nut_flush_block = 1 and has_flush_draw = 1, but facing_bet = 0. It is a BET label (hero leads as a semi-bluff). This teaches the donk semi-bluff with nut FD, but not the KB §1.7 RAISE pattern that v3.2 specifically codified. The paradigm case for KB §1.7 is: hero faces a villain bet, holds nut FD + nut blocker, villain_air_pct >= 0.20, and the correct action is RAISE (not call or check). Zero examples of this exist. The v3.2 OVERRIDE (villain_air_pct < 0.20 → CALL even with nut FD) also has zero examples.

The research phase showed labellers fail this pattern at 50% even with scaffolding. A corpus with zero examples of the RAISE case provides no training signal at all.

### Pattern 6: River-checked-to (CO range-cap protection)

**Corpus coverage: 32 hands on river where villain_checked_back = 1.**

This is the best-represented pattern. 32 of 34 river hands have villain_checked_back = 1 — essentially ALL river hands are checked-to situations. The labeller correctly applies the d3178 anchor in many cases: monsters and strong-made hands that pass the Rule 11 BET override on checked-to rivers get BET (14 hands); medium and weak hands that still fail the Rule 11 threshold get CHECK (18 hands).

However: the boundary is overfit. There are ZERO river hands where the villain did NOT check back. This means the model cannot learn the contrast between "river checked to → BET" and "river with prior villain aggression → CHECK/CALL/FOLD". The river-checked-to pattern is 100% represented without its complement.

### Pattern 7: Multi-street equity realization OOP (BB trapping with monsters)

**Corpus coverage: 12 OOP monsters, producing 3 CHECK and 9 BET labels.**

The 3 CHECK cases are on paired/2-tone boards where Rule 11's default-CHECK fires (villain_top_pair_plus_pct < 0.40). These correctly teach the trap-by-checking pattern. But they are mechanically Rule-11 driven, not trap-driven: the reasoning cites Rule 11's predicate rather than "I check this monster to induce bluffs across multiple streets." The multi-street equity realisation concept — where OOP players check monsters on the flop to induce bets on turn and river — has zero representation as a distinct pattern. All corpus spots are single-decision snapshots; there are no multi-street-linked hands where the flop check leads to a turn or river value bet.

### Pattern 8: Bet-and-call sequences (3-way fold-pressure dynamics)

**Corpus coverage: 0 hands with num_callers_to_bet >= 1.**

Complete absence. The bet-and-call pattern (one villain bets, a second calls, hero must act third) is one of the most important 3-way-specific patterns. It narrows both villain ranges simultaneously and typically forces hero to a much tighter continuing standard. The MW-30 calibration anchor (CALL despite bet-and-call because of equity surplus) is the solver-verified exception case. Neither the standard case nor the MW-30 exception is teachable from this corpus. A model trained here will have no learned response to num_callers_to_bet >= 1.

### Pattern 9: Free-card protection on dynamic boards

**Corpus coverage: 0 hands where is_monster = 1 AND danger_score >= 0.6 AND villain_draw_pct >= 0.2.**

Exact zero. Sets and straights on dynamic boards (T86 two-tone, 765 connected, 9-8-7 with two flush suits) are the canonical spot where protection betting is mandatory — not because of thin value, but because giving free cards to villain's flush/straight draws costs too much equity. This decision structure (bet for protection, not value) is completely absent from the corpus. The related labelling vocabulary tag `deny_equity` is presumably triggered occasionally, but always in lower-danger contexts.

### Pattern 10: Range-tipping protection (paired-low BB checks whole range)

**Corpus coverage: 7 paired-low OOP hands (high_card_rank <= 9 AND is_paired AND is_ip = 0).**

Some coverage, but the range-tipping logic is not surfaced in labels. The pattern is: BB must check the entire range on paired-low boards (not just the specific made hand) to avoid revealing hand strength through action. Labeller 3's reasoning for these spots cites Rule 11's predicate conditions — it does not cite "range-tipping protection." The concept is encoded in the rule but not surfaced in the label reasoning. Teaching downstream models to understand why the rule exists (range balance, not just board texture) requires explicit range-tipping examples in the reasoning text.

---

## Q4 answer — Boundary-case sampling within rule triggers

### Rule 11: Paired/2-tone OOP made-hand CHECK exception

Inside-trigger count: 28 hands
- BET override fires: 19 hands
- Default CHECK: 9 hands

Just-outside trigger (dry board OOP made): 12 hands — all produce BET
Just-outside trigger (IP made hand, rule exempt): 13 hands

**Evaluation:** The 9 default-CHECK cases adequately anchor the rule's CHECK outcome. The 12 dry-board OOP BET cases anchor the just-outside boundary (rule doesn't fire because no pair or 2-tone structure). This is one of the better-covered rules.

**Gap:** The boundary between BET override (villain_top_pair_plus >= 0.40) and default CHECK (villain_top_pair_plus = 0.35-0.39) is not explicitly paired. The corpus has examples of both outcomes but not adjacent examples that differ only in villain_top_pair_plus crossing the 0.40 threshold. This creates a fuzzy boundary in the training signal. Recommendation: 3-4 pairs of hands where only villain_top_pair_plus differs across the 0.40 threshold, holding all other features roughly constant.

**Recommended ratio:** Inside (all sub-cases) : Outside = roughly 28:25 in the current corpus — close to 1:1, which is good. The absolute counts are the problem: 9 default-CHECK cases and 12 dry-OOP-BET cases are adequate individually but may blur when the model must learn villain_top_pair_plus as the deciding feature within the rule-fire zone.

### KB §1.7 OVERRIDE: villain_air_pct >= 0.20 threshold

Inside-trigger (nut FD + facing bet + villain_air >= 0.20): 0 hands
Just-outside (nut FD + facing bet + villain_air < 0.20 → CALL): 0 hands
Non-nut FD (CHECK preferred): 9 hands (correct, teaches the base case)

**Evaluation:** Complete failure. The rule's trigger condition (nut FD + facing bet + villain_air threshold) has zero examples on either side of the boundary. The 9 non-nut FD hands teach the base case (non-nut → CHECK) correctly, but without any nut FD + facing bet examples, the override rule is entirely unteachable.

**Recommended ratio:** 5 inside-trigger RAISE cases (nut FD + facing bet + air >= 0.20) : 5 just-outside CALL cases (nut FD + facing bet + air < 0.20) : 9 non-nut-FD CHECK cases = 5:5:9. Total: ~19 hands covering the rule's full boundary.

**Recommended sample size:** Minimum 10 facing-bet hands with flush draws. Currently 0.

### River-checked-to override: villain_checked_back = 1 on river

Inside-trigger (villain checked back on river): 32 hands
Outside-trigger (river with prior villain aggression, not checked to): 0 hands

**Evaluation:** The inside case is over-represented (32 hands, 32% of corpus). The outside case is absent. This creates a severe class-imbalance in the rule's boundary: the model will see "river" almost always paired with "villain_checked_back = 1" and may not correctly learn that villain aggression changes the river decision structure entirely.

**Recommended fix:** Add 10-15 river hands where villain_aggression_count >= 1 AND villain_checked_back = 0 (villain bet a prior street and hero is first to act on the river with initiative). These should produce CHECK-or-BET depending on range strength, not default-BET from the checked-to override. Target ratio: 32 inside : 12-15 outside = roughly 2:1, not current 32:0.

---

## Q5 answer — Action class imbalance: minimum representation for ML

### Minimum N for each class

Based on tabular ML learning requirements (XGBoost / gradient boosting, which is the stated architecture for River Rats):

| Action | Current (500 labels) | Minimum for learning | Notes |
|--------|---------------------|---------------------|-------|
| CHECK | ~300 (60%) | ~200 | Dominant class; over-represented relative to model needs |
| BET | ~185 (37%) | ~150 | Adequate if balanced well |
| FOLD | ~13 (2.6%) | ~100 | Severely under minimum; XGBoost with class_weight adjustments needs ~50+ examples |
| CALL | ~3 (0.6%) | ~80 | Far below minimum; model will essentially never predict CALL |
| RAISE | 0 (0%) | ~60 | Zero; model literally cannot learn this class |

**Why these minimums:** For a 54-feature tabular XGBoost classifier, the minority class needs enough examples to find the relevant feature boundaries. With 5 classes, the model needs to learn a different boundary surface for each class. Fewer than 50 examples for a minority class with 54 features produces unstable, high-variance splits that don't generalise.

### The RAISE problem specifically

In real 3-way postflop play, RAISE occurs in approximately 3-8% of decisions (solver data). The corpus has 3% facing-bet hands, which is realistic, but none produce RAISE. In a Tier 2 corpus of 500 hands, expecting 3-8% RAISE = 15-40 RAISE labels — achievable only if facing-bet hands are oversampled to 20-25% of the corpus and include the KB §1.7 semi-bluff + monster-value-raise scenarios.

### Proportions sustainable given real-play rates

For a model that must generalise to real play (not just match the training distribution), the recommended corpus distribution is:

| Action | Real-play approximate rate | Recommended corpus rate |
|--------|--------------------------|------------------------|
| CHECK | ~45-50% | 35-40% (reduce slightly) |
| BET | ~30-35% | 30-35% |
| CALL | ~8-12% | 12-15% (oversample) |
| FOLD | ~5-8% | 8-10% (oversample) |
| RAISE | ~3-6% | 8-10% (oversample) |

**Oversampling rare classes is necessary and appropriate.** The model will need class_weight adjustments during training anyway. Better to have 60-80 RAISE examples with known oversampling bias than 0 RAISE examples and a model that never predicts RAISE.

---

## Q6 answer — Spot types a competent expert would expect in a teaching corpus

Independent of v3.2 protocol, from pure poker GTO expertise, the following spot types are MANDATORY in a comprehensive 3-way postflop corpus:

### 1. C-bet decision spots (hero is preflop aggressor) — ABSENT

is_preflop_aggressor = 0 for 100% of corpus hands. The most common postflop decision in real play is the preflop aggressor deciding whether to continue betting on the flop. In a 3-way pot this is 30-45% c-bet frequency vs 65%+ HU. The corpus teaches nothing about when to fire a continuation bet. This is not a minor gap — it is probably the most frequently recurring postflop decision type.

A competent player MUST learn: which boards to c-bet as the aggressor (dry K-high, A-high) vs which to check (connected two-tone, BB-smashing low boards), and how to range-balance the c-bet vs check-behind ranges.

### 2. Standard and deep SPR decisions — ABSENT

SPR >= 2.0: zero hands in corpus. All 100 hands are at compressed SPR (1.25 or lower). Standard 3-way flop decisions occur at SPR 4-8. Turn decisions at SPR 2-4. The entire early-street decision structure is absent. A model trained here will have no learned response to standard SPR contexts.

This correlates with the c-bet gap: early-street decisions at natural SPR are precisely the spots where hero is often the preflop aggressor making c-bet decisions.

### 3. Bet-and-call (3-way fold-pressure sandwich) — ABSENT

num_callers_to_bet = 0 for 100% of corpus. The bet-and-call structure is uniquely 3-way — it cannot occur HU. It is one of the two most important distinctions between 3-way and HU play (the other being fold equity math). A model that cannot respond to num_callers_to_bet >= 1 is fundamentally incomplete as a 3-way oracle.

### 4. Multi-street aggression sequences — ABSENT

villain_aggression_count >= 2: 0 hands. Real play frequently involves villains who bet flop and continue betting turn (double-barrel), or check-raise and then bet river. Hero's response changes dramatically between "villain bet once" and "villain has now bet twice." This feature is in the 54-feature vector precisely because it matters, but the corpus provides no training signal for it.

### 5. Facing-bet flop decisions — ABSENT

0 flop hands with facing_bet = 1. The majority of FOLD, CALL, and RAISE decisions in real play occur on the flop (when pot is smallest, SPR is highest, and villain betting range is widest). River-heavy facing-bet decisions (2 of 3) produce a systematically different signal: on the river, villain's range is narrower, pot odds are clearer, and "just fold" is more often correct. Flop facing-bet decisions require nuanced range-shape reasoning that the corpus cannot teach.

### 6. SB / sandwich position decisions — SEVERELY UNDERREPRESENTED

SB: 3 hands (3%). In real 3-way play, the SB is the sandwich player — worst position, first-or-second to act on later streets depending on sequence, must account for both a bettor and a caller. The sandbox position dynamics (20% MDF, much tighter continuing range) are completely different from OOP-blind or IP-button. With 3 hands, the model cannot distinguish SB dynamics from BB dynamics.

### 7. Facing raises (check-raise by villain) — SEVERELY UNDERREPRESENTED

facing_raise = 1: 3 hands, all of which resolve to FOLD or CALL. The check-raise in a 3-way pot is "almost exclusively the nuts" per KB §2 Factor 5. But the solver exception (trips+ facing river check-raise is still CALL per MW-46) is important and untaught. A corpus needs ~10-15 facing-raise hands to teach: when to fold (air/weak made), when to call (trips+, equity surplus), and never to re-raise without the nuts.

### 8. IP thin-value and c-bet decisions — UNDERREPRESENTED

IP hands: 24%. Real-play IP frequency in 3-way pots is ~35-45% for the button/closing-position player. The model sees mostly OOP decisions. IP-specific reasoning (ability to check behind for pot control, 105-120% EQR, thinner value extraction, secondary position advantage) is learned from 24 examples — insufficient given the material differences between IP and OOP play.

### 9. 3-bet pot dynamics — SEVERELY UNDERREPRESENTED

is_3bet_pot = 1: 3 hands (3%). In real play, 3-bet pots occur 8-15% of 3-way situations. 3-bet pots have dramatically different stack depths, range constructions, and SPR profiles (often 2-4 on the flop rather than 6-10). A model that sees only 3 hands from 3-bet pots cannot learn the distinctive dynamics: narrower ranges, stronger compositions, higher c-bet frequency, different pot-size decisions.

### 10. Villain draw-heavy ranges — UNDERREPRESENTED

villain_draw_pct >= 0.3: 5 hands (5%). In real play, flop villain draw percentages of 20-40% are common on textured boards. The model has almost no examples of "charge the draws" reasoning — the fundamental motivation for protection betting with made hands on dynamic boards.

---

## Q7 answer — Corpus revision recommendation

### Verdict: Rebuild, do not supplement

The current 100-hand corpus has systemic structural deficits that supplement hands cannot fix:

1. **is_preflop_aggressor = 0 for 100% of hands** — the c-bet class is structurally absent.
2. **SPR = 1.25 for 94% of hands** — all decisions are compressed; no standard-SPR coverage.
3. **facing_bet = 0 for 97% of hands** — RAISE, CALL, FOLD are untrained.
4. **villain_aggression_count = 0 or 1 only** — multi-street sequences absent.
5. **BB over-represented (25%), SB severely underrepresented (3%)**.
6. **villain_draw_pct is low (< 0.15) for 92% of hands** — protection bet reasoning absent.
7. **board_favour > 0.2 for 0% of hands** — range-advantage situations absent.

These are not individual bad hands — they are systematic generation artifacts. Supplementing with facing-bet hands and c-bet hands added to an otherwise SPR-1.25 corpus produces a bimodal distribution that confounds the model rather than teaching it.

### Minimum spot-type coverage requirements for Tier 2

| Dimension | Requirement |
|-----------|-------------|
| Action class | CHECK >= 35%, BET >= 30%, CALL >= 10%, FOLD >= 8%, RAISE >= 7% |
| facing_bet = 1 | >= 25% of corpus |
| is_preflop_aggressor = 1 | >= 30% of corpus |
| SPR >= 4 (deep, early street) | >= 25% of corpus |
| SPR 2-4 (standard, turn) | >= 20% of corpus |
| SPR < 2 (compressed) | <= 55% of corpus |
| OOP / IP balance | OOP 55-65%, IP 35-45% |
| BB / SB / BTN / CO / HJ / UTG | BB <= 25%, SB >= 10% |
| villain_aggression_count >= 2 | >= 10% of corpus |
| num_callers_to_bet >= 1 | >= 10% of corpus |
| is_3bet_pot = 1 | >= 10% of corpus |
| villain_draw_pct >= 0.2 | >= 20% of corpus |
| board_favour > 0.15 | >= 10% of corpus |
| board_favour < -0.15 | 25-40% of corpus |

### Recommended Tier 2 size

Minimum: **400 hands** to provide adequate class coverage at the required ratios. Optimal: **600-800 hands** to cover the boundary-case sampling requirements per Q4 without crowding any single rule-trigger cell.

Rationale per class:

| Action | Target % | Hands at 500 total | Notes |
|--------|---------|-------------------|-------|
| CHECK | 35% | 175 | Reduce from current 60% |
| BET | 30% | 150 | Maintain |
| CALL | 12% | 60 | Requires 120+ facing-bet hands |
| FOLD | 10% | 50 | Requires facing-bet hands across streets |
| RAISE | 13% | 65 | Requires ~250 facing-bet hands with §1.7 + monster setups |

Note: at 500 hands, achieving 13% RAISE requires that a significant fraction of facing-bet hands produce RAISE labels. At ~25% facing-bet rate, 125 facing-bet hands. Of those, RAISE-eligible ones need: nut FD + blocker + villain_air >= 0.20, or monster facing bet, or set facing bet. Expect 30-40% of well-designed facing-bet hands to produce RAISE = 40-50 RAISE labels at 500 total hands. To reach 65, increase facing-bet rate to 30%.

### Spot patterns that MUST be added as design targets

**Tier-A (must-have, corpus cannot teach without these):**

1. **C-bet spots**: is_preflop_aggressor = 1, flop/turn, SPR 3-8, villain_aggression_count = 0. Produce BET (value or bluff) or CHECK (pot-control). Target: 30% of corpus.

2. **Facing-bet flop decisions**: facing_bet = 1, flop, SPR 3-8. Villain c-bet into hero. Hero must decide CALL/RAISE/FOLD. This is the only way to get meaningful RAISE and CALL labels at natural SPR. Target: 15% of corpus.

3. **Bet-and-call sandwich spots**: num_callers_to_bet >= 1, hero last to act behind a bet-and-call. Produce FOLD (usually), CALL (equity surplus, MW-30 pattern), or RAISE (monster, essentially never). Target: 8-10% of corpus.

4. **Multi-street aggression responses**: villain_aggression_count = 2, hero facing a second street of betting. Produce CALL (if continuing), FOLD (if behind), occasionally RAISE (trips+ facing river barrel). Target: 8-10% of corpus.

5. **Standard SPR early-street decisions**: SPR 4-8, flop. All hand classes, multiple board textures. Target: 20-25% of corpus.

**Tier-B (important for specific rule coverage):**

6. **KB §1.7 RAISE examples**: nut_flush_block = 1, has_flush_draw = 1, facing_bet = 1, villain_air_pct >= 0.20. Must produce RAISE. Minimum: 10 examples. Include 5 contrast cases where villain_air_pct < 0.20 → CALL.

7. **Check-raise facing situations**: facing_raise = 1. Produce FOLD (air/medium), CALL (trips+, equity surplus), never RAISE. Minimum: 12 examples across strength classes.

8. **Range-advantage c-bet spots**: board_favour > 0.15, is_preflop_aggressor = 1, hero has medium-strong made hand. BET as thin value on favoured board. Minimum: 10-15 examples.

9. **Protection bet on dynamic boards**: villain_draw_pct >= 0.25, danger_score >= 0.5, is_made_hand = 1 (any strength). BET for deny_equity. Minimum: 15-20 examples.

10. **SB sandwich decisions**: hero_position = SB, villain_aggression_count >= 1. Teach 20% MDF, tighter continuing standard. Minimum: 15-20 examples.

**Tier-C (rule-boundary coverage):**

11. **Rule 11 boundary pairs**: villain_top_pair_plus_pct = 0.35-0.39 (CHECK) vs 0.40-0.45 (BET override) on paired/2-tone OOP boards, all else equal. Minimum: 4-6 pairs.

12. **River-without-checked-back contrast**: villain_aggression_count = 1, villain_checked_back = 0, river (villain bet earlier but checked river). Hero CHECK/CALL/FOLD rather than default-BET. Minimum: 10-15 examples.

13. **3-bet pot dynamics**: is_3bet_pot = 1, SPR 2-4 on flop, narrower ranges. All action classes. Minimum: 15-20 examples.

14. **Dominated kicker on dry boards**: TPWK on K72r or A-high dry rainbow with is_preflop_aggressor = 0, villain_air_pct >= 0.30. BET as thin value (do not apply Rule 11 because board is dry). Minimum: 5-8 examples (this is the just-outside Rule 11 boundary for TPWK specifically).

---

## Recommendation

The pilot corpus is adequate for testing labelling consistency on a narrow opener-decision distribution at compressed SPR — which is what it was originally designed for. It is not adequate as a training corpus for a 3-way postflop GTO model.

**The action-class imbalance is structural, not labeller-caused.** The labellers perform correctly given the hands they receive. The hands simply do not provide the contexts for RAISE, CALL, meaningful FOLD, or c-bet decisions to occur.

**The range-logic patterns the owner identified as missing are genuinely absent.** Range-advantage, bet-and-call, multi-street aggression, KB §1.7 RAISE conditions, and protection betting are untaught because the corpus doesn't contain the situation types that exercise them. Adding 50-100 supplement hands on top of a structural mismatch cannot fix these gaps.

**Recommendation: Design a 500-600 hand Tier 2 corpus from scratch** with explicit allocation targets per the Tier-A/B/C lists above. The corpus design should be the next blocker — before any mass labelling resumes — and should be reviewed by both gto-expert and ml-architect before generation begins. The current 100-hand corpus remains available as a calibration-only reference set (it exercises Rule 11 and the river-checked-to override adequately) but should not be the primary training data.

**Immediate data collection note:** The 5 facing-bet hands (PILOT_021, PILOT_029, PILOT_094, plus the 1 turn facing-bet) and the 9 non-nut FD check hands contain real data and should be preserved as anchors in any revised corpus, since they represent the rare facing-bet contexts that are most valuable.
