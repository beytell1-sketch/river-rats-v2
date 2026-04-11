# GTO Expert Assessment: PFA Range Advantage C-Bet Bluff
**Date:** 9 April 2026
**Question:** Do the 52 features capture the PFA c-bet bluff scenario, or is an explicit `is_preflop_aggressor` feature needed?
**Status:** COMPLETE — Owner decision required

---

## The Scenario

Hero is the preflop aggressor (PFA). Board is A/K/Q-high, favouring PFA's range. Hero missed the board but has outs. The bluff is credible because villain respects the range. Villain's range is weak on this texture.

Classic example: CO opens, BTN calls, BB folds. Flop comes Ah 7c 2d. CO missed with QJs (no pair, gutshot). CO c-bets as a bluff — the board hits CO's range (AK, AQ, AA, KK, QQ all in range), villain knows this, and villain's capped flat range (missing premium Ax) folds frequently.

---

## Step-by-Step Feature Audit

### Step 1: "Hero raised preflop"

The 52-feature vector has no `is_preflop_aggressor` field.

What exists instead:
- `hero_range_percentile` — hero's hand strength relative to the preflop range that opened from hero's position (`_opener_position` is a metadata field used in its computation)
- `is_3bet_pot` — flags whether the pot was 3-bet preflop
- `hero_position` / `villain_position` — positional encoding

The critical question is how `hero_range_percentile` is computed. The metadata field `_opener_position` is captured, which implies the pipeline knows who opened. But `hero_range_percentile` measures hand strength within range — it does NOT encode whether hero WAS the opener. A hand can have a high or low range percentile regardless of whether hero opened or called.

**Result: preflop aggressor identity is not directly in the 52 features.** The pipeline knows opener position as metadata but does not expose it as a model feature.

---

### Step 2: "Board favours our range (A/K/Q high)"

`board_favour` exists and is designed to capture exactly this. Per the knowledge base (Section 2, Factor 3): "positive = board favours hero's range."

However, the description in the KB says `board_favour` encodes "preflop construction → postflop range interaction." The sign convention matters: is it computed relative to hero's range or villain's range?

The feature reference in RAISE_DECISION_TREE_V2.md states: "board_favour: negative = villain's range is favoured." So positive board_favour = hero's range is favoured.

**On a board like Ah 7c 2d, board_favour should be positive** because the PFA's range (CO opens with AK, AQ, AA, KK, QQ) hits this board far more than the BTN flat range (condensed, capped, no premium Ax).

**Result: Step 2 is captured**, assuming board_favour is computed correctly for the PFA-vs-caller dynamic. The board favouring the PFA is reflected in positive board_favour.

---

### Step 3: "We don't hit"

`hand_category`, `is_made_hand`, `is_strong_made`, `is_monster` — all present.

QJs on Ah 7c 2d would show: hand_category = 0 or 1 (high card / one overcard), is_made_hand = 0, is_strong_made = 0, is_monster = 0. The model knows hero missed.

**Result: captured cleanly.**

---

### Step 4: "We have some outs"

`draw_outs`, `has_flush_draw`, `has_straight_draw`, `overcard_outs`, `improvement_probability` — all present.

QJs on Ah 7c 2d has a gutshot (draw_outs > 0) and overcard outs (overcard_outs captures Qx and Jx improvement). The model knows hero has partial equity.

**Result: captured cleanly.**

---

### Step 5: "Villain knows the flop hits our range, so the bluff is believable"

This is the mechanism that makes the bluff work. The key features:
- `villain_fold_equity_estimate` — estimated probability villain folds
- `board_favour` — board hits whose range
- `villain_range_capped` — villain's flat range excludes premiums
- `villain_air_pct` — fraction of villain's range that is air on this board
- `villain_top_pair_plus_pct` — fraction of villain's range that connected

On Ah 7c 2d versus a BTN flat:
- `villain_range_capped` = 1 (BTN flat is capped — no AA, KK, QQ, AKs)
- `villain_air_pct` will be high (BTN's suited connectors and medium pairs whiffed)
- `villain_top_pair_plus_pct` will be low (BTN rarely has Ax)
- `board_favour` will be positive
- `villain_fold_equity_estimate` should be elevated

**These features collectively encode the result of villain respecting PFA range.** But they encode the result, not the cause. The model sees "villain is likely to fold on this board with this range composition" — it does NOT see "villain folds because hero's range is threatening."

This distinction matters for generalisation. The model learns a correlation (positive board_favour + villain_range_capped + high villain_air_pct → high fold equity) without understanding the mechanism. In most training cases, this correlation holds because the PFA is the one with the threatening range. But if a defender hero happened to face the same board composition features, the model cannot tell the scenarios apart from the feature vector alone.

**Result: the outcome is partially captured, the mechanism is not.**

---

### Step 6: "Does not connect with villain's range"

`villain_top_pair_plus_pct`, `villain_air_pct`, `villain_draw_pct` — all present.

A BTN flat on Ah 7c 2d will show low villain_top_pair_plus_pct and high villain_air_pct. The model sees villain missed.

**Result: captured cleanly.**

---

## The Critical Question: Can the Model Conflate PFA with Defender?

The scenario that exposes the gap:

- `board_favour` positive (board favours hero's range)
- `villain_fold_equity_estimate` high (villain likely folds)
- `hero_range_percentile` low (hero missed)
- `draw_outs` > 0 (hero has some outs)

Can the same feature values appear when hero is the DEFENDER (BB, who called preflop) instead of the PFA?

**Yes, they can.** Consider: BB defends vs CO open. BTN also calls. Flop is Kh 4d 2c. If the pipeline computes board_favour from BB's perspective (which appears to be the case), then a board that hits BB's defending range (BB has many K-x hands, small pairs, suited connectors) would show positive board_favour for hero. If villain_fold_equity_estimate is high for other reasons (villain_aggression_count is low, villain_range_capped = 1), and hero missed with a hand that has some outs, the feature vector can look nearly identical to the PFA bluff scenario.

The difference in real poker is enormous:
- **PFA bluffing on Ah 7c 2d:** credible. CO's range is full of Ax. Villain knows this.
- **BB defender bluffing on Kh 4d 2c:** harder to claim. CO's range has more premiums and more Kx than BB's range on this board. BB's bluff range is less believable.

But from the feature vector, if board_favour happens to be positive for BB on that board (because BB's range does have some Kx and suited connectors), villain_fold_equity_estimate is elevated, and hero missed — **the model cannot separate the two scenarios without knowing who raised preflop.**

---

## How Bad Is the Gap in Practice?

The severity depends on two questions:

**Q1: Does `board_favour` systematically encode PFA vs defender correctly?**

If board_favour is computed specifically as "how much does THIS board hit the preflop opener's range relative to the caller/defender," then positive board_favour already implies "board favours the PFA" — which means the gap partially closes. The model can infer PFA scenario from high board_favour if the feature is computed in a PFA-centric way.

But the feature reference says "positive = board favours hero's range." If hero is the BB defender and the board happens to favour BB's range, board_favour will also be positive — for the wrong reason.

**Q2: Does villain_fold_equity_estimate already incorporate PFA identity?**

If villain_fold_equity_estimate is computed using board_favour, villain_range_capped, and villain_air_pct together, then it is capturing a downstream consequence of PFA range advantage. The model would learn: when board_favour is positive AND villain_range_capped AND villain_air_pct is high → villain folds. In most training data, this configuration will be dominated by PFA-bluff scenarios, because PFA boards are the ones where villain is most often capped and airiest.

The question is whether the training data has enough defender-hero cases where these same features fire without PFA identity — and whether those cases get different labels (CALL instead of RAISE). If they do, the model learns the distinction statistically. If they do not exist in training data, the model cannot learn the distinction at all.

---

## Verdict

**The owner has identified a real gap, but its severity is conditional.**

The 52 features capture all the downstream consequences of PFA range advantage: board_favour, villain_fold_equity_estimate, villain_range_capped, villain_air_pct. What they do not capture is the upstream cause — who created the range pressure by raising preflop.

**The gap is real under two conditions:**

1. The pipeline does not compute board_favour in a strictly PFA-centric way (i.e., board_favour can be positive for defender-hero on the right board), AND

2. The training data does not have enough labelled examples that cleanly separate "defender-hero with positive board_favour bluffs" (CALL) from "PFA-hero with positive board_favour bluffs" (RAISE).

If either of those conditions is false, the gap is minor and the model learns the distinction statistically. If both are true, the model will overfit to the bluff signal in feature space and incorrectly label defender-hero bluffs as RAISE.

**The clean solution is a binary `is_preflop_aggressor` feature.**

This is a single bit. The pipeline already tracks `_opener_position` as metadata. Exposing it as a binary feature (hero_position == opener_position → is_preflop_aggressor = 1) would directly capture the mechanism the owner identified. It would allow the model to learn: PFA + positive board_favour + missed + outs = bluff candidate. Defender + same board = default to CALL.

---

## What Is NOT Needed

The gap does not require a full preflop action sequence, a new range model, or any complex computation. It requires one binary: did hero make the last preflop raise? The metadata to compute it already exists in `_opener_position`.

The decision tree currently has no branch for "PFA c-bet bluff with outs" — this scenario falls through to default CALL. Adding `is_preflop_aggressor` would enable a new tree branch:

- is_preflop_aggressor == 1
- board_favour >= threshold (e.g., 0.20)
- is_made_hand == 0
- draw_outs >= minimum (e.g., 4, gutshot or better)
- villain_fold_equity_estimate >= threshold (e.g., 0.40)
- villain_range_capped == 1

This maps precisely to the owner's described scenario and is fully computable from the feature vector if `is_preflop_aggressor` is added.

---

## Recommendation

**Add `is_preflop_aggressor` as feature 53.** One binary. Low implementation cost. The pipeline already has the data (`_opener_position` metadata). The poker logic improvement is significant.

Without it, the model conflates PFA bluffs (credible, profitable) with defender bluffs (less credible, often incorrect) in a feature region where the correct labels diverge. This is the definition of a feature gap — the information needed to distinguish two different correct actions is not in the vector.

The owner found a real one.

---

*Written by: GTO Expert*
*For: Owner review*
*Next step: If owner agrees, raise with Architecture Expert and Lead Programmer to add feature 53 and a new decision tree step.*
