# Blocker Feature Expansion — Research for v2.4+ Oracle

**Date:** 2026-04-18
**Scope:** Survey current blocker-adjacent features in `river-rats-core`, enumerate
blocker dimensions that matter in poker theory, and propose 2-3 consolidated signals
for the v2.4+ oracle. Teaching layer implications follow from what the oracle can
distinguish.

Owner's earlier insight (preserved): the directional sign of a blocker flips by role.
Holding the nut-flush blocker is **positive** for a bluff-bettor (removes villain's
continues) but **negative** for a bluff-catcher (removes villain's value combos and
raises the likelihood the remaining bet is a bluff hero is beating — i.e., wrong
direction if the signal is presented as "you block villain's strong hands").

---

## 1. Current Blocker / Blocker-Adjacent Features

| Feature (key in `feature_keys.py`) | What it computes | File:line | Gap |
|---|---|---|---|
| `flush_block_pct` | Fraction of villain's **flush combos** hero blocks, weighted by narrowed villain range. Returns 0.0 when hero has 2+ cards of the flush suit (hero is the draw, not a blocker). Monotone/2-tone only. | `feature_extractor.py:1240-1362` | Does not distinguish nut-flush blocker (Ah) from low-flush blocker (2h). Does not separate **made flush** blocking from **flush draw** blocking. |
| `flush_draw_rank` | Rank 2-14 of hero's highest card of the board's flush suit, or 0. | `feature_extractor.py:1450-1499` | Hero-side only — says nothing about what fraction of villain's range is affected. Oracle cannot tell "Ah blocks nut flush" from "Ah on two-tone where villain rarely has the flush." |
| `flush_danger` | Board-threat score `[0,1]` — function of board suit count and street. | `board_analyzer.py:1126-1172` | Hero-agnostic. Describes the board, not hero's blocker effect. |
| `straight_danger` | Board-threat score `[0,1]` from connectivity. | `board_analyzer.py:1178-1186` | Hero-agnostic. No feature anywhere tracks hero's rank-blockers of villain's straights. |
| `danger_score` | `max(flush_danger, straight_danger)` + bonuses for paired / trips / later streets. | `board_analyzer.py:1191-1207` | Aggregate board threat only. |
| `count_combos_with_blockers` (utility) | Removes board cards from the combo pool when counting a hand-notation's available combos. | `hand_categories.py:488-530` | Infrastructure only. Removes **board** cards from combos — does not remove **hero** cards unless the caller adds them to the blocker set. Not exposed as a feature. |
| `range_decomposition.py` (per-combo classifier) | Classifies each villain combo into `nut_flush / strong_flush / weak_flush / nut_straight / weak_straight / top_set / lower_set / top_two_pair / second_pair / bottom_pair / overpair / underpair / nut_flush_draw / flush_draw / oesd / gutshot / overcards / air`. | `range_decomposition.py:84-361` | Already per-combo-typed. Not currently consumed by any blocker feature. **This is the lever for range-aware blocker math.** |

**What's missing:** Everything except `flush_block_pct`. There is no straight blocker,
no nut/second-nut made-hand blocker, no paired-board trips blocker, no draw-vs-made
separation, no directional framing for bluff-catcher vs bluff-bettor.

The existing `flush_block_pct` is also **ambiguous** on blocker quality: holding the
2 of the flush suit and holding the Ace of the flush suit both show up as "blocks some
flush combos" when the true fold-equity impact is radically different. The research
doc `RESEARCH_CBET_R5_BLOCKERS.md` cites +8-15pp fold-equity from a nut-flush blocker
vs noise from a low-flush blocker — this distinction is currently invisible to the
oracle.

---

## 2. Blocker Dimensions That Matter (Poker Theory)

Each dimension is scored on (a) what it blocks, (b) which range component it hits,
(c) board-texture sensitivity, (d) directional sign by hero role.

| Dimension | Blocks | Range component | Board sensitivity | Directional sign |
|---|---|---|---|---|
| **Nut-flush blocker** (Ax of flush suit) | Villain's nut-flush combos on mono / 2-tone boards | Value | High on mono, moderate on 2-tone, zero on rainbow | +bluff-bettor, −bluff-catcher |
| **Generic flush blocker** (any non-Ax of flush suit) | Fraction of villain's flush combos | Value + some draws | Moderate — weakens fast as rank drops | Weak +bluff-bettor |
| **Nut-straight blocker** (the rank that completes villain's straight) | Villain's straight combos on connected boards | Value | High on connected / 1-gappers, zero on dry | +bluff-bettor, −bluff-catcher |
| **Overpair / set blocker** (pocket pair rank matching board) | Villain's sets and overpairs via card-removal on pairs | Value-nuts | High on dry A-high, K-high, Q-high boards | +bluff-bettor (removes AA on A-high), −bluff-catcher |
| **Top-pair blocker** (ace on A-high, king on K-high) | Villain's top-pair combos | Value-mid | Very high on paired-top textures | +bluff-bettor, ambiguous for bluff-catcher |
| **Paired-board trips blocker** (hero holds the paired rank) | Villain's trips + full-house combos | Value-nuts | High only when board is paired | +bluff-bettor |
| **Draw blocker** (hero holds cards in villain's draw-completion set) | Villain's draws (not made hands) | Bluffs / semi-bluffs | Highest on wet-drawy boards | −bluff-bettor (fewer semi-bluffs), +bluff-catcher (villain's bets are more value-weighted) — **sign flip** from made-hand blockers |
| **Bluff-combo blocker** (removes villain's natural bluff candidates, e.g. Ax-suited) | Villain's bluffs | Bluffs | Board-specific | −value-bettor (villain folds fewer bluff-catchers to a raise), irrelevant for most bluffing |

Two axes emerge: **what it blocks** (made hands vs draws vs bluff combos) and
**directional impact** (bluff-bettor vs bluff-catcher). The owner's insight —
"weak-made facing a bet" — falls into the **bluff-catcher with made-hand blocker =
bad news** cell: removing villain's value combos shifts villain's remaining bet
toward bluffs, which is actually fine for the call, but if the feature is named
"you block the nuts" a learner will misread it as a reason to fold.

---

## 3. Proposed New Features for v2.4+ Oracle

Three features, chosen to be **orthogonal to** `flush_block_pct` and to capture
distinct range components. All are single floats/ints, extractable from
`(hero_cards, board, narrowed_villain_range)`. Computation infrastructure already
exists — `range_decomposition.classify_combo()` produces per-combo subcategories,
and `count_combos_with_blockers` handles combo removal.

### Proposed Feature A: `nut_made_block_pct` — *made-hand-nuts blocker, range-weighted*

**What:** Fraction of villain's **nut-category made-hand combos** (nut_flush +
nut_straight + top_set + top_two_pair + overpair + full_house + trips) that hero
blocks via card-removal. Range-weighted like `flush_block_pct`. Reuses
`range_decomposition.classify_combo` to filter the "nut" subset, then applies the
`count_combos_with_blockers` math with `hero_cards + board` as the blocker set.

**High value means:** Hero's card-removal meaningfully shrinks villain's
nut-range. Signals are consistent whether hero is bluff-bettor (+fold equity) or
bluff-catcher (villain's remaining bets are less value-heavy → call more).

**Why it's distinct from `flush_block_pct`:** Aggregates across **all** nut
made-hand categories (set, two-pair, straight, flush), not just flush. Works on
dry boards and paired boards where flush is irrelevant. Subsumes nut-flush-blocker
as one input.

**Complexity: Moderate.** Per-combo classification is already in
`range_decomposition.py`. Need to (a) wire the classifier through the villain
range, (b) filter to a "nut" subcategory set, (c) count blocked vs total. The
fairness of blocker-counting already exists in `count_combos_with_blockers`.
Estimated 80-150 lines in `feature_extractor.py`.

### Proposed Feature B: `draw_block_pct` — *villain-draw-range blocker, range-weighted*

**What:** Fraction of villain's **draw-category combos** (nut_flush_draw +
flush_draw + oesd + gutshot) that hero blocks via card-removal. Range-weighted.

**High value means:** Hero's cards remove villain's semi-bluff / draw combos.
**This is the directional counterweight to made-hand blockers** — it is
*negative* for a bluff-bettor (villain has fewer draws = fewer folds on turn/river
barrels) but *positive* for a bluff-catcher (villain's remaining bets are less
likely to be semi-bluffs, but also less likely to be pure bluffs — net
informative).

**Why it's distinct:** `flush_block_pct` conflates blocking **made flushes** with
blocking **flush draws** — both produce a non-zero value. Separating made-hand
blocks from draw blocks is what lets the oracle represent the owner's
"weak-made facing a bet" insight as a learned weight rather than a hardcoded rule.

**Complexity: Moderate.** Same infrastructure as Feature A, filtered to the draw
subcategory set. 60-100 lines.

### Proposed Feature C: `nut_flush_block` — *binary + rank-weighted ace-of-suit flag*

**What:** `flush_draw_rank == 14 and board has flush suit`. Emit as a single
`[0, 1]` float: `1.0` if hero holds the ace of the board's flush suit (and a
flush threat exists), `0.0` otherwise. Optional finer grading: return
`(flush_draw_rank - 10) / 4` clipped to `[0, 1]` — K=0.75, Q=0.5, J=0.25, T=0,
and 1.0 for the ace.

**High value means:** Hero holds the single most impactful blocker card in
poker. Research doc `RESEARCH_CBET_R5_BLOCKERS.md` quantifies +8-15pp fold-equity
for this specific signal in 3-way c-bet spots.

**Why it's distinct from `flush_draw_rank` (feature 52):** `flush_draw_rank` is a
raw 0-14 integer; the oracle has to learn the nonlinear step-function from scratch
(ace vs king vs queen is not a smooth ramp). Emitting the blocker-strength
directly saves training-data and makes the signal explicit. Also, it is a
function of `(hero_cards, board)` only — no range narrowing needed — so it is
trivial to compute and zero-cost to add.

**Complexity: Trivial.** ~10 lines; derived from `flush_draw_rank` and
`board_suit_counts`.

---

## 4. Recommended Priority for v2.4+

1. **`nut_flush_block`** — cheapest win. Trivial complexity, directly addresses the
   owner-flagged case (nut-flush blocker sign-flip). Worth adding even before any
   retraining so the oracle gets a clean binary on the highest-leverage blocker.
2. **`draw_block_pct`** — the **directional counterweight** that enables the oracle
   to reason about bluff-catcher vs bluff-bettor asymmetry without hardcoded
   rules. Directly addresses the "weak-made facing a bet" misread risk.
3. **`nut_made_block_pct`** — generalizes `flush_block_pct` to all made-hand
   categories. Replaces `flush_block_pct` long-term, or runs alongside it during a
   transition period to validate.

All three should be added **additively** for v2.4 training data. `flush_block_pct`
stays in place until validation proves the new features dominate, to preserve the
oracle's current calibration.

---

## 5. Teaching Implications

Once these features exist and the oracle assigns them non-trivial SHAP weight,
the teaching layer can surface **three distinct blocker observations** that today
collapse into one:

- **"You hold the nut-flush blocker"** (L3+) — fired when `nut_flush_block == 1.0`
  and the oracle's SHAP weight on it is high. Framing varies by action:
  *bluff-bet* → "removes villain's strongest continues"; *bluff-catch* → "villain
  is less likely to hold the nut flush, but this doesn't change your call math
  directly." This resolves the owner's sign-flip concern by letting the template
  branch on `decision_reporter.action`.
- **"You block villain's draws"** (L3+) — fired when `draw_block_pct` is high.
  Framing: *bluff-bet* → "villain has fewer semi-bluffs to continue with — be
  cautious about barreling"; *bluff-catch* → "villain's betting range is more
  polarised than usual." This is a **new observation type** with no current
  analog in `situation_describer.py`.
- **"You block villain's value range"** (L4+) — fired when `nut_made_block_pct`
  is high. Numeric framing at L4: "You remove ~X% of villain's nut combos from
  their range." This makes the SHAP ordering signal teach range-removal logic
  rather than just card-counting.

No level-gating surprises: all three observations are L3+ and use vocabulary
(`nut`, `blocker`, `draw`) that is already in the L3 vocabulary set.

---

## Appendix: File / Line Index

- `feature_extractor.py:1012-1050` — FEATURE_COLUMNS canonical order
- `feature_extractor.py:1240-1362` — `compute_flush_block_pct` (current sole blocker feature)
- `feature_extractor.py:1450-1499` — `compute_flush_draw_rank` (hero-only, not range-weighted)
- `feature_extractor.py:1606-1643` — Step 12 wiring (where new blocker features would integrate)
- `feature_keys.py:44,68,76` — key constants for FLUSH_DANGER, FLUSH_BLOCK_PCT, FLUSH_DRAW_RANK
- `board_analyzer.py:1126-1229` — `flush_danger` / `straight_danger` / `danger_score` (hero-agnostic, for contrast)
- `hand_categories.py:488-530` — `count_combos_with_blockers` (reusable infrastructure)
- `range_decomposition.py:84-361` — per-combo subcategory classifier (the unused lever for Features A and B)
- `range_manager.py:1631-1712` — `get_hand_percentile` / `get_range_size` with `blocker_aware=True` (pattern for range-weighted blocker math)
