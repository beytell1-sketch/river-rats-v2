# 3-Way Postflop GTO Knowledge Base

**Version:** 1.3
**Date:** 10 April 2026
**Purpose:** Reference document for the 3-way labelling agent.
Contains quantified facts (as reasoning inputs), a decision
framework, preflop range construction, board texture interactions,
and worked examples. NOT a set of threshold rules.
**Sources:** 80+ references across GTO Wizard (solver), Upswing,
Phil Galfond, Peter Clarke, MonkerSolver, PioSolver. Full source
index in research/ directory.

---

## 1. Reference Data

Quantified facts the agent uses as INPUTS to reasoning. These are
not decision rules. No single number determines the correct action.

### 1.1 Fold Equity

| Context | Fold equity to break even (pot-sized bet) | Source |
|---------|------------------------------------------|--------|
| HU | 50% (one opponent folds) | Math |
| 3-way | ~49% (need BOTH to fold: 0.70 x 0.70) | Math + GTO Wizard |

Each opponent only needs to defend ~30% (vs 50% HU). The defense
burden is shared. But it's asymmetric:
- Sandwich player (action behind): defends ~20%, folds ~80%
- Closing action player: defends ~40%, folds ~60%
- Combined: 0.80 x 0.60 = 0.48, meeting the ~50% MDF

**Implication for reasoning:** At 70% fold per opponent, fold equity
is 49% — still below the 50% breakeven for a pot-sized bluff. Pure
bluffs are unprofitable 3-way. Semi-bluffs require strong draws (nut flush draw,
combo draws). Gutshots and backdoor-only hands are check/folds.

### 1.2 Equity Dilution by Hand Class

| Hand class | Equity HU | Equity 3-way | Drop |
|-----------|-----------|-------------|------|
| AA | ~85% | ~73.5% | -11.5pp |
| AKo | ~65% | ~45-47% | -18 to -20pp |
| Overpairs (general) | ~60% | low-40s% | ~-18pp |
| TPTK | ~65% | ~50-55% | ~-12pp |
| Top pair weak kicker | ~55% | ~38-42% | ~-15pp |

Rough heuristic: premiums lose ~12% equity per additional opponent.

**Implication for reasoning:** Hands that are clear value bets HU
become marginal or even check-behind candidates 3-way. Top pair
weak kicker is a pot-control hand, not a value hand.

### 1.3 C-Bet Frequency (Solver)

| Metric | HU | 3-way | Change |
|--------|-----|-------|--------|
| Overall c-bet frequency | ~54% | ~43% | -11pp |
| Large (pot-sized) c-bet | ~18% | ~1.3% | virtually eliminated |
| Check frequency | ~46% | ~57% | +11pp |
| Default sizing when betting | Mixed (33-100%) | Small (25-33% pot) | Size down |

Range-betting is never correct 3-way. When betting, the range is
tighter and stronger than HU. Big bets (50%+ pot) are rare
exceptions on specific textures.

### 1.4 Bluff-to-Value Ratio

| Context | Ratio (pot-sized bet, river) | Source |
|---------|----------------------------|--------|
| HU | ~1:2 (33% bluffs) | GTO math |
| 3-way | ~1:4 or tighter (estimated) | Derived from solver principles |

The betting range is much more value-heavy 3-way. Pure bluffs are
nearly eliminated; only the strongest bluffs (nut blockers, strong
draws that missed) remain.

### 1.5 Equity Realization by Position

| Position | EQR range | Notes |
|----------|-----------|-------|
| IP (BTN/CO, closing action) | 105-120%+ | Over-realizes |
| OOP (BB, first to act) | 60-80% | Under-realizes |
| Sandwich (middle) | Worst seat | Must fold more, heuristics fail |

On 9s-3s-2d: IP realized 118.1% of equity, BB realized 79.1%
(PioSolver). Position is amplified 3-way because there's more
information to exploit and more opponents to act behind.

### 1.6 SPR Compression

A pot-sized flop bet 3-way leaves SPR ~1.5 on the turn (vs ~3-4
HU), which effectively commits stacks. The flop bet decision must
account for the full remaining tree at compressed SPR. Same numeric
SPR requires tighter stack-off thresholds multiway (more opponents
who could have you beat).

### 1.7 Semi-Bluff Conditions 3-Way (Solver-Verified)

Semi-bluffing 3-way is rarely profitable — but "rarely" is not
"never." GTO Wizard solves (April 2026) identify a narrow carve-out.

| Condition | Required? | Why |
|-----------|-----------|-----|
| Nut draw (nut flush draw, nut straight draw) | YES | Non-nut draws don't generate enough equity when called |
| Blocker to opponent's continuing range | YES | As on flush board blocks nut flush combos in villain's range, increasing fold equity |
| Side equity (overcards, gutshot, backdoor) | Strongly preferred | Nut draw alone is marginal; side outs push EV clearly positive |
| Position | Any (even OOP) | Blocker + draw equity compensate for positional disadvantage |

**Example:** AsQs on Ks Jd 5s facing bet — nut flush draw + As
blocker + two overcards + gutshot = ~44% equity + fold equity.
Solver: RAISE. (See Worked Example 9.)

**What does NOT qualify:**
- Non-nut flush draws (e.g., Ts9s on the same board) — call or fold
- Nut draw without blocker (e.g., 8s7s for nut flush) — call
- Gutshot-only or backdoor-only — check/fold
- Any draw on a paired board (set over set risk) — call at best

**Default for non-set made hands at mixed SPR:** When the solver
shows a hand mixing between raise and call (e.g., AT on A94 mixes
21-65% raise depending on suit), default to CALL in training labels.
The model cannot express mixed strategies. Only sets and the pure
nuts are labelled RAISE.

### 1.8 Blocker Effects on Action Selection (Solver-Verified)

Blockers have two distinct roles. They differ in multiway impact:

| Role | HU effect | 3-way effect | Example |
|------|-----------|-------------|---------|
| **Bluff selection** (which bluffs to choose) | Strong | Weaker (~40% less) | Choosing to bluff with Ah on heart board |
| **Action selection** (raise vs call with strong draw/made hand) | Strong | **Still strong** | AT with diamond raises 65%, AT without raises 21% |

The solver shows suit holdings swing raise frequency by 40+
percentage points for the SAME hand on the SAME board. This is not
a marginal effect — it's the primary driver of raise/call decisions
for non-set hands.

**Implication for labelling:** The labelling agent must consider
hero's specific suit holdings when deciding RAISE vs CALL. Using
worse_hand_pct (a suitless metric) as a raise signal is wrong.
Blockers and backdoor equity drive raise frequency, not raw hand
strength.

### 1.9 Preflop geometry vs postflop composition — do not collapse them

There are two distinct signals the labelling agent must not conflate:

**Preflop structural geometry.** A stable fact about villain's
preflop action sequence. Example: "villain cold-called a CO open in
a non-3-bet pot" implies villain's preflop range excludes AA / KK /
QQ / AKs by construction (those hands 3-bet preflop). This is a
statement about which hand combos were *allowed into the range in
the first place*, not about which combos remain after bets and
calls on the flop.

**Postflop composition.** The actual decomposition of villain's
*current continuing range* on the current street, measured by three
features from the 45-feature pipeline:

- `villain_top_pair_plus_pct` — fraction of villain's continuing
  range that is top pair or better (strength signal).
- `villain_draw_pct` — fraction that is draws without made-hand
  equity yet (equity-with-fold-potential signal).
- `villain_air_pct` — fraction that is air with no meaningful
  equity (fold-equity signal).

These three features sum to ≤ 1 (hands outside the three buckets
— e.g. low pocket pairs without draws on a high board — are
distributed across the remainder).

**The trap.** Using preflop structural geometry as a postflop
strength proxy underestimates TP+ density in a cold-caller's
*actual continuing range* on boards that smash the caller's flats.
MW-30 is the canonical example: a BB hero holding KcTh on KdJc6s
facing CO bet + BTN cold-call. BTN's preflop range excludes
AA/KK/QQ/AKs by construction — but that is irrelevant to the
postflop strength question. What matters is what BTN's *continuing
range after calling CO's flop bet* actually contains. The real
feature row for this hand (source:
`review/all_557_situations.jsonl` line 120, CALL_Board5_KdJc6s_h5)
shows `villain_top_pair_plus_pct = 0.3174`,
`villain_draw_pct = 0.0878`, `villain_air_pct = 0.1856` — roughly
32% strong, 9% draws, 19% air, and ~40% weaker made hands and
pocket pairs in the remainder. The continuing range is not "all
better Kx"; it contains significant worse holdings that KcTh beats.
Hero's 43.2% raw equity vs 18.4% pot odds reflects that
composition. Reasoning from "BTN's preflop range is structurally
narrower than CO's" to "therefore KcTh is dominated" collapses the
two signals and produces the over-fold that the MW-30 solver
correction exposed (see feedback_solver_findings.md finding 6 and
Worked Example 3 below).

**Rule.** Reason postflop decisions from the composition triple as
the **primary** strength signal. Use preflop action sequence only
to inform what the preflop range looked like — never substitute it
for the current-street composition.

**Threshold buckets (provisional — adopted from teaching).** The
teaching-side L3 renderer
(`river-rats-teaching/interface/l3_renderer.py`,
`_villain_range_sentence` at line 317+) characterizes villain range
shape using these buckets:

| `villain_top_pair_plus_pct` | Shape |
|---|---|
| ≥ 60% | Heavy with strong hands |
| ≥ 40% | Meaningful value density |
| ≥ 20% | Some value but mostly weaker holdings |
| < 20% | Thin on value |

The KB adopts the same buckets so teaching and labelling share one
vocabulary. **Thresholds are provisional pending calibration
against solver data** — logged as TODO for the next
feature-importance audit (see `feedback_solver_findings.md`). If
calibration shifts the boundaries, both this section and
`l3_renderer.py` must be updated together.

**Cross-reference.** This section replaces the prior use of
`villain_range_capped` as a postflop strength indicator in the KB.
The feature remains in the pipeline for continuity with the
v9-3way-v2.2 model; no KB-level retraining decision is being made
in this revision. Whether to drop `villain_range_capped` from the
feature vector in a future training round is a model-training
decision, tracked against the next feature-importance audit in
`feedback_solver_findings.md`. The labelling agent must not treat
it as a postflop signal. See DO NOT Rule #8 for the operative
instruction.

### 1.10 Defensive Blocker Direction — the 4 new v2.4 features

§1.7 and §1.8 cover the **aggressor-side** use of blockers: holding
a card that removes villain's continuing range from a semi-bluff
raise line (As on a 2-flush board, supporting a flop raise). The
solver-verified carve-out in §1.7 is real and narrow.

This section covers the **defender-side** complement: what hero's
blocker does to villain's **betting** range when hero is facing a
bet and deciding whether to call / raise / fold. The v2.4 feature
vector adds four signals that let the labelling agent reason about
blocker direction per-decision rather than treating "blocker = good"
as context-free.

**Why a new section.** A known v2.3.2 regression (β-panel
re-label, 7 of 9 flipped hands) surfaced that the model — and the
panels — were missing the **densification effect**: hero holding a
non-nut blocker to villain's draw range REMOVES those draw combos
from villain's pre-bet range, so when villain bets, the betting
range is densified toward value. Hero's bluff-catch equity is
LOWER than `equity_vs_range` alone suggests. See
`feedback_concentration_effect.md`.

The features:

| # | Name | Direction for hero (high value) |
|---|---|---|
| 56 | `nut_flush_block` (0/1) | Aggressor: positive. Defender: slight positive (bluff-catch equity improves). |
| 57 | `flush_draw_block_pct` (0-1) | Aggressor: neutral. **Defender: negative** (densifies villain to value). |
| 58 | `straight_draw_block_pct` (0-1) | Aggressor: neutral. **Defender: negative** (same mechanism, straight class). |
| 59 | `nut_made_block_pct` (0-1) | Aggressor: positive (thin value blocked). **Defender: positive** (villain's value reduced → more bluff-catch equity). |

#### 1.10.1 `nut_flush_block` — the Ace-of-suit bit

**Poker meaning.** Hero holds the Ace of a flush-possible suit on
the board. The feature is 1 if board has 2+ of one suit (flop) or
3+ (turn/river) and hero holds A-of-that-suit, AND hero has not
already made a flush.

**When it matters.**
- Aggressor-side semi-bluff raise decisions (KB §1.7 canonical —
  AsQs on Ks·Jd·5s facing bet, raise is +EV specifically because
  As blocks nut-flush combos)
- Defender-side bluff-catch decisions on flush-possible boards —
  direction depends on whether the flush is currently possible
  or only future-possible

**Direction — texture-dependent, not uniform.**

Aggressor side (hero betting/raising): **positive**. Solver-verified
carve-out from §1.7. `nut_flush_block == 1` + side equity → RAISE
candidate.

Defender side (hero facing bet, CALL/FOLD/RAISE deciding):
**direction flips with street**.

- **2-flush flop** (board has 2 of suit; flush can COMPLETE on
  future streets). Hero's A-of-suit blocks villain's A-of-suit
  **semi-bluff** combos (Ax-of-suit as nut-flush-draw). Given
  villain bet, villain's betting range is densified toward MADE
  value (§1.10.2 mechanism applied to the ace specifically) →
  **defender-negative** (fold-lean), same direction as
  `flush_draw_block_pct`.
- **3+-flush board** (flush currently possible). Hero's A-of-suit
  blocks villain's **made** nut-flush combos. Given villain bet,
  villain's value fraction is reduced → **defender-positive**
  (call-lean), aligned with `nut_made_block_pct`.

The distinction matters: on a 2-flush flop, the blocker works AGAINST
hero's call; on a 3-flush turn, the same blocker works FOR hero's call.
Same card, same board-type suffix, opposite decision direction.

**Example (aggressor / KB §1.7).** Hero AsQs on Ks·Jd·5s facing
bet. Nut flush draw + overcard + gutshot + ace blocker = §1.7
RAISE. Solver-verified in Worked Example 9.

**Example (defender, 3-flush — CALL-lean).** Hero AhTd on
Kh-8h-3h-2c turn, facing villain's bet. Board is 3-flush hearts
and hero holds the Ah blocker. `nut_flush_block = 1`. Villain's
nut-flush combos (Ah-Xh) are impossible because hero holds Ah →
villain's value range on the turn bet is substantially reduced,
villain is bluffier. With TPGK (K-high pair) as showdown value,
this is a CLEAR CALL. Without Ah (e.g., KdTd in same spot), fold
is far closer.

**Example (defender, 2-flush — FOLD-lean).** Hero Ah9c on
Kh-8h-3d flop, facing villain's pot-sized bet. Board is 2-flush
(future flush possible on turn/river); hero's Ah blocks villain's
Ax-of-hearts semi-bluff combos. Villain's pre-bet semi-bluff
fraction shrinks; villain's betting range is more value-heavy.
Hero has ace-high (weak made) → hero's bluff-catch equity is LESS
than `equity_vs_range` alone suggests. FOLD despite the
"I have the blocker" instinct. Compare to a board where hero's
non-ace overcards provide similar equity without the
densification penalty.

#### 1.10.2 `flush_draw_block_pct` — blocking villain's flush semi-bluffs

**Poker meaning.** Fraction of villain's flush-draw combos
(`nut_flush_draw`, `flush_draw`, `combo_draw`) that hero's hole
cards remove from villain's range. Higher value = hero is blocking
more of villain's potential flush-draw semi-bluff candidates.

**When it matters.** Defender decisions on flush-possible boards
where hero holds partial flush-suit cards. The owner's Apr 18
example: hero has middle pair + J♠ on Q♠8♠4♥ facing a bet. The
J♠ blocks villain's spade-suited semi-bluff combos (Q♠J♠, J♠T♠,
K♠J♠). Given villain bet, villain's range is now more value-heavy
because the semi-bluff slice shrank relative to value.

**Direction — asymmetric by action context.**
- Aggressor (hero bet or raise): high value is **near-neutral**.
  Blocking villain's draws doesn't change their fold response to
  hero's aggression much — villain folds draws to a bet
  regardless of whether hero blocks specific combos.
- **Defender** (hero facing bet, CALL/FOLD deciding): high value
  is **negative** for hero's equity. Villain's betting range
  densifies toward value because the semi-bluff fraction is
  reduced. `equity_vs_range` overstates hero's true bluff-catch
  equity; lean toward FOLD/CHECK more than equity alone would
  suggest.

**Example.** Hero 8♠9h on Q♠8♥4♠ facing villain's 1.5×-pot bet.
Pot-odds break-even = 37.5%. `equity_vs_range = 0.38`,
`flush_draw_block_pct = 0.52` — hero holds one spade (8♠) that
blocks ~half of villain's flush-draw combos. Naive reading: "I
have middle pair + blocker; 0.38 clears 0.375 pot odds; call."
Correct reading: villain's betting range is densified by ~52%
removal of the semi-bluff slice; hero's true equity vs the
densified calling range drops below ~0.30, under the 0.375
break-even. FOLD. (Compare to the same hand without the spade
blocker — 8♥9h — where villain's semi-bluffs remain in range,
hero's true bluff-catch equity stays near 0.38, and CALL
becomes correct. Same hand shape, blocker direction flips the
decision.)

#### 1.10.3 `straight_draw_block_pct` — blocking villain's straight semi-bluffs

**Poker meaning.** Fraction of villain's straight-draw combos
(`oesd`, `gutshot`, `combo_draw`) hero's hole cards remove. Same
mechanic as `flush_draw_block_pct` applied to straight-draw class.

**When it matters.** Connected boards where hero holds a card in
the middle of the straight range but not a made straight. Example:
9h-8s-5c flop, hero holds Th (blocks ~half of villain's JT/T9 OESD
combos) + a marginal-made hand.

**Direction.** Same asymmetry as §1.10.2:
- Aggressor: near-neutral
- **Defender: negative** (densifies to value)

**Example.** Hero T♣7♣ on 9h-8s-5c facing a bet. Hero's T♣ blocks
JT/T9 OESD combos from villain's range; hero also has the pair of
7s (bottom pair) on the board. `straight_draw_block_pct ≈ 0.35`.
Villain's betting range is more value-weighted than range
composition suggests — the JT/T9 semi-bluff slice shrinks relative
to villain's made hands (8x, 9x, 55, 88). Combine with hero's weak
bottom-pair made hand → CHECK/FOLD is correct, not CALL despite
a naive 0.40 equity-vs-range reading.

#### 1.10.4 `nut_made_block_pct` — blocking villain's value

**Poker meaning.** Fraction of villain's nut-made combos —
straight-flush, quads, full-house, nut_flush, nut_straight, top_set
(and strong_flush when A-of-suit is on board as the effective nut)
— that hero's hole cards remove from villain's range.

**When it matters.** Any decision where villain's nut-made fraction
is a meaningful part of their range (flush-possible boards, paired
boards with full-house threats, etc.).

**Direction.**
- Aggressor **thin value bet / raise with medium-strong hand**:
  high value is **negative**. Hero's thin-value target is reduced
  because villain's top calling hands are blocked; villain calls
  less often with non-nut made hands. Does NOT apply to pure
  bluffs (blocking villain's value combos is irrelevant when hero
  is betting to fold villain out, not to extract from worse made
  hands).
- **Defender** (facing bet, bluff-catch deciding): high value is
  **positive**. Villain's stack-off range is reduced; villain's
  bets must contain relatively more bluffs. Hero's bluff-catch
  equity is HIGHER than `equity_vs_range` alone suggests. Lean
  CALL.

**Example (defender, aligned with d2410 calibration anchor
pattern).** Hero JcKs on Jd-9d-3h-6d turn, checked to at
compressed SPR. Paired-board nut-made class for villain is top_set
(JJ trips) + full_house candidates. Hero's Jc removes half of
villain's possible JJ combos (hero holds one of the four Jacks in
the deck; board holds one). `nut_made_block_pct` captures this
removal. With trips-of-jacks blocked from villain's range,
villain's betting range is less value-heavy → hero's TPGK
(K-kicker pair of Jacks) converts from thin call to strong value
bet. Matches the d2410 calibration-anchor reasoning.

### 1.11 Implication for labelling — the covering triple

These four features together encode blocker direction as a
**covering triple** in the feature subspace. The labelling agent
must use them TOGETHER, not in isolation:

1. **`nut_flush_block`** says "I have THE block" (binary, high signal;
   direction texture-dependent per §1.10.1)
2. **`flush_draw_block_pct` + `straight_draw_block_pct`** say "I'm
   blocking villain's semi-bluffs" (defender-negative, aggressor-neutral)
3. **`nut_made_block_pct`** says "I'm blocking villain's value
   combos" (defender-positive, aggressor-negative for thin-value)

When hero is defending with a marginal made hand on a draw-heavy
board, check whether `{flush,straight}_draw_block_pct` is high
(densification toward value → fold lean) or whether
`nut_made_block_pct` is high (villain value blocked → call lean).
Use `equity_vs_range` as the EQUITY baseline, then ADJUST by these
blocker features for the **directional** correction.

**Multi-signal resolution — what to do when signals co-fire.**
A defender may see BOTH `flush_draw_block_pct > 0.2` (fold-lean)
AND `nut_made_block_pct > 0.2` (call-lean) on the same decision.
The features pull in opposite directions. Rule:

- If `nut_made_block_pct − (flush_draw_block_pct + straight_draw_block_pct) / 2 > 0.15`,
  **net CALL lean** — villain's value blocked more than villain's
  draws. Call-bias wins.
- If `(flush_draw_block_pct + straight_draw_block_pct) / 2 − nut_made_block_pct > 0.15`,
  **net FOLD lean** — villain's draws blocked more than villain's
  value. Fold-bias wins.
- Smaller net differences (|delta| ≤ 0.15): blocker signals approximately
  cancel; decide on `equity_vs_range` + `villain_top_pair_plus_pct`
  alone. Do not tag blocker features as PRIMARY in this case.

This rule is a labelling heuristic for panel feature-attention
decisions, not a solver-verified threshold. Revisit when
Stage 5 training exposes the model's learned interaction.

**Combo-draw double-counting caveat.** A villain combo classified
as `combo_draw` (flush draw + straight draw simultaneously) is
counted in BOTH `flush_draw_block_pct` AND
`straight_draw_block_pct` when hero blocks it. This is intentional
— blocking a combo-draw removes a combo from each class's
denominator. But it means the two percentages can sum above 1.0
on connected-two-tone boards with meaningful combo-draw coverage.
Use each feature independently; do not add them.

`flush_block_pct` (feature 46) remains in the feature vector
pending the Stage 5 retirement A/B test. It is superseded on
aggressor-side reasoning by `nut_flush_block` (specific-blocker
case) and on defender-side by the split-direction features above.
Until retirement is decided, treat `flush_block_pct` as a generic
aggregate signal and prefer the more specific features for action
decisions.

### 1.12 DO NOT Rule 6 update — expanded

DO NOT Rule 6 (blocker over-weighting) was written when the only
blocker signal was `flush_block_pct` (aggregate). With the four
new features, the operative instruction becomes:

- **DO NOT** treat `flush_block_pct` as a defensive CALL signal.
  It aggregates nut-flush and flush-draw blocking into one scalar
  that has opposite defender-side directions.
- **DO** use `nut_made_block_pct` as a defender CALL signal
  (villain's nut range shrinks → more bluff-catch equity).
- **DO** use `flush_draw_block_pct` and `straight_draw_block_pct`
  as defender FOLD signals when hero has a marginal made hand
  (densification effect).
- **DO** use `nut_flush_block` as a semi-bluff RAISE trigger per
  §1.7 (aggressor) OR as a defender signal subject to the
  texture-flip rule in §1.10.1 (2-flush flop = negative,
  3-flush = positive).

The forward-pointer in Rule 6 itself (§5, DO NOT Rules) references
this sub-section by number.

---

## 2. Decision Framework

Every 3-way postflop decision depends on the interaction of 5
factors. No single factor is decisive. The correct action emerges
from weighing all five.

### Factor 1: Equity Position

Raw equity relative to pot odds. Reference data (Section 1.2)
provides the baseline, but equity alone does not determine the
action. A hand with 45% equity may be a BET (if other factors
align) or a CHECK (if they don't).

### Factor 2: Position

- **IP (closing action):** Can bet thinner for value, can bluff
  more effectively (one fewer player to act behind), realizes
  more equity. But 3-way IP c-bet frequency is still only 30-45%,
  not 65%+.
- **OOP (first to act):** Under-realizes equity. Must play tighter
  ranges. Pot control is more important. Checking strong hands is
  common (even AA checks ~80% OOP on dry boards in 3-bet pots).
- **Sandwich:** Worst position. Must worry about players on both
  sides. Tighten continuing range 15-20% vs HU cutoffs.

### Factor 3: Range Composition

Postflop strength is measured directly from the composition triple,
NOT from preflop structural labels. The 45-feature pipeline
provides:

- `villain_top_pair_plus_pct` — fraction of villain's continuing
  range that is top pair or better. **Primary postflop strength
  signal.** Bucket thresholds in Section 1.9 (≥60 / ≥40 / ≥20 / <20).
- `villain_draw_pct` — fraction that is draws without made-hand
  equity yet. Signals equity-with-fold-potential in villain's range.
- `villain_air_pct` — fraction that is air with no meaningful
  equity. High air supports thin value bets.
- `board_favour` — positive when board favours hero's range,
  negative when it favours villain's.

**How to use the triple.** Read `villain_top_pair_plus_pct` first
against the Section 1.9 buckets. A range with ≥40% TP+ has
meaningful value density regardless of preflop structural labels.
A range with <20% TP+ is thin on value and supports thin value
betting. High `villain_air_pct` (≥30%) adds fold-equity support
for thin value and for nut-draw semi-bluffs with blockers (see
Section 1.7). High `villain_draw_pct` means many of villain's
continuing combos still need to improve, which supports protection
betting with vulnerable made hands.

**Feature `villain_range_capped` — present in the pipeline but not
a postflop signal.** The pipeline also exposes
`villain_range_capped` (see
`river-rats-core/feature_extractor.py:1195-1197`). It is computed
as `int(not is_3bet_pot and villain_is_defender)` — a pure
preflop-action-geometry bit that flags whether villain was the
preflop caller in a non-3-bet pot. It encodes "which hands were
structurally *allowed into* the preflop range", not "which hands
are *currently in* the continuing range after flop/turn/river
action". Do not use it as a postflop strength signal. If the
composition triple and `villain_range_capped` appear to
contradict each other, **the composition triple is authoritative**
— it is a direct measurement of the current range; the binary is
a preflop structural label. See Section 1.9 and DO NOT Rule #8.

**The two opponents are NOT symmetric — expressed compositionally.**
The cold-caller (BTN flat) and the blind defender (BB) have
different preflop range constructions:

- **Cold-caller (BTN flat vs CO open):** Preflop range excludes
  AA / KK / QQ / AKs by construction (those 3-bet). Still contains
  22-TT for set-mining, suited broadway (KTs/QJs/JTs), suited
  connectors (76s-T9s), and suited aces (A2s-A5s). On boards that
  smash these holdings (connected middling, two-tone middling),
  the postflop composition can still be heavy with TP+ and draws
  even without any premium overpairs.
- **Blind defender (BB vs CO+1 caller):** Preflop range is wider
  (speculative suited/connected, small pairs, some broadway) and
  includes some premium combos at low frequency (BB mixes flats
  and squeezes with AA/KK). Very wide flop range, high air
  fraction, but carries strong combos on connecting boards.

When reasoning about which opponent is dominating which part of
the action, reason from their *actual composition triple*, not
from the preflop construction. The preflop construction tells you
how the composition triple was generated; it does not substitute
for it. See Section 1.9.

### Factor 4: Board Texture

From the pipeline: `danger_score`, `flush_danger`,
`straight_danger`, `connectivity_score`, `is_monotone`, etc.

**Boards that favour the preflop raiser (CO/HJ):**
- Ace-high dry/rainbow (A72r, AK5r): raiser has more Ax, AK
- King-high paired (KK5r): raiser has all premium pairs
- Static, disconnected: equity doesn't shift across streets

**Boards that favour the cold-caller (BTN):**
- Connected middling (764r, T86): BTN flat range is dense with
  suited connectors that smash these
- Two-tone middling: BTN has flush draws + pair+draw combos

**Boards that favour the BB defender:**
- Low, connected (532, 643): BB's speculative overcalling range
  hits hard — small pairs for sets, suited connectors for straights
- Monotone low: BB's suited hands connect disproportionately

### Factor 5: Action History

- `facing_bet`: someone has bet this street
- `facing_raise`: someone raised (not just bet) — strong signal
- `num_callers_to_bet`: bet-and-call = confirming signal from
  second opponent. Two ranges are condensed.
- `villain_aggression_count`: multi-street betting = strong range
- `villain_checked_back`: villain showed weakness on a prior street

**The bet-and-call signal (MW-30 pattern):** When one opponent bets
and another calls in a 3-way pot, both ranges have narrowed. The
bettor is representing strength. The caller is confirming with a
hand strong enough to continue against the bet AND the remaining
player.

**IMPORTANT CORRECTION (solver-verified, April 2026):** The
bet-and-call signal narrows ranges but does NOT automatically mean
fold. The fold applies ONLY when BOTH conditions are met:
1. Hero's equity against the narrowed ranges is close to break-even
   (within ~5pp of pot odds), AND
2. Hero's specific holding is dominated by the calling range (e.g.,
   weak kicker on a paired board where better kickers abound).

When hero has equity well above pot odds (e.g., 40% vs 18% pot
odds) AND holds a made hand (not just overcards), the correct
action is CALL even facing bet-and-call. The MW-30 solver
verification showed KT top pair on KJ6 is a pure CALL despite
bet-and-call — 40% equity vs 18% pot odds, and KT still beats
significant portions of both opponents' continuing ranges. See
corrected Example 3.

**The check-raise signal (MW-31 pattern):** A check-raise into
two opponents in a 3-way pot is almost exclusively the nuts or
near-nuts. The raiser must beat not only the bettor's range but
also the third player's calling range. Even top pair top kicker
folds to a 3-way check-raise.

**Exception (solver-verified):** Trips or better facing a river
check-raise is still a CALL. The solver shows opponents include
enough bluffs and thin value that trips is never a fold unless the
board makes a higher full house virtually certain AND hero has no
blocker. (MW-46: K7 trips on 775-9-J, solver says 100% CALL even
with worse trips.)

---

## 3. Preflop Construction → Postflop Ranges

Preflop action sequence determines which combos were structurally
allowed into each player's range. That is a *generator* for the
postflop composition triple (Section 1.9, Factor 3) — it is not a
substitute for it. This section describes the generators; the
labelling agent still reasons postflop decisions from the actual
composition triple.

### CO open / BTN flat / BB defend (most common 3-way)

- **CO opens ~27-28%:** Linear range. Includes all premiums
  (AA-QQ, AKs/AKo), strong broadways, suited connectors, suited
  aces, medium pairs. On any flop, CO's continuing range will
  *contain* some AA/KK/AK combos — those don't have to be
  inferred from the action.
- **BTN flats ~5%:** Condensed range. Excludes AA / KK / QQ / AKs
  by construction (those 3-bet). Contains 22-TT, suited connectors
  (76s-JTs), suited aces (A2s-A5s), some KTs/QJs. On connecting
  middling boards, the postflop composition can still show
  meaningful TP+ density even though the preflop range contained
  no premium overpairs — middle pairs, top-pair-with-kicker, and
  sets fill in. On dry high-card boards, the composition is air-
  and draw-heavy.
- **BB overcalls wide:** Speculative suited/connected hands, small
  pairs, some broadway. Needs ~19% equity to defend. Premium
  hands (AA/KK/AKs) squeeze rather than flat, so the BB flat
  range excludes them at high frequency (BB mixes a squeeze-flat
  fraction but the headline construction is still "wide without
  premiums"). OOP reduces EQR, so BB is selective despite good
  odds. Very high preflop air, strong composition on low
  connecting boards, thin composition on high dry boards.

### HJ open / CO flat / BB defend

- **HJ opens tighter (~22-24%):** Stronger range than CO — more
  overpairs, more AK/AQ, fewer speculative suited connectors.
- **CO flats ~4-6%:** Excludes AA / KK / QQ / AKs / AQs and most
  broadway combos that would 3-bet over HJ. Very condensed. Even
  narrower than BTN vs CO. Postflop composition is similarly
  pair-and-draw-driven on connecting boards.
- **BB:** Similar to above but facing a stronger open — tighter
  defend range, lower preflop air.

### Key insight for labelling

The opener's preflop range width drives the postflop composition
triple, particularly `villain_air_pct`. A CO opener's continuing
range has more air than an HJ opener's on the same flop, because
the CO preflop range was wider to begin with. The cold-caller's
preflop range always excludes the premium 3-bet holdings by
construction, but its postflop continuing range can still be
dense with value on boards that smash the caller's flats (middle
pairs, connected suited combos). The BB's preflop range is
always wide and carries the highest baseline air fraction. When
the features show high `villain_air_pct`, it reflects the combined
effect of a wide opening/defend range and a board that missed it
— read the composition triple directly rather than inferring
strength from the preflop role.

---

## 4. Worked Examples

Each example shows the full reasoning chain: factors identified →
weighed → conflicts resolved → action chosen.

### Example 1: Strong hand OOP — check for pot control

**Setup:** Hero holds KcQc on Kh 8d 3s. BB (OOP), 2 opponents
(CO opened, BTN called). Pot 90, checked to hero (first to act).

**Factors:**
1. Equity: ~52% (marginal 3-way for top pair second kicker)
2. Position: OOP — hero acts first, worst position
3. Range composition: villain_air_pct ~0.25 (moderate), BTN flat
   range excludes AA/KK/QQ/AKs, but CO open range still
   contains AK and KK
4. Board: dry, rainbow, low danger — favours raiser (CO)
5. Action: no prior aggression this street

**Factor interaction:** Equity suggests possible thin value. But
OOP + board favouring CO + CO's open range containing AK / KK (which
dominate KQ) = too much risk. Betting folds out worse (BTN's
middle pairs) and gets called/raised by better (CO's AK, KK).

**Action:** CHECK
**Confidence:** HIGH
**Alternative:** BET small (33%) — rejected because OOP, and the
hands that call are mostly better. Showdown value is high enough
to check-call if CO bets.

### Example 2: Thin value bet IP with air-heavy villain range

**Setup:** Hero holds Jh9h on Jc 7d 2s. BTN (IP), 2 opponents
(CO opened, BB defended). Pot 100, both check to hero.

**Factors:**
1. Equity: ~54% (top pair decent kicker, marginal 3-way)
2. Position: IP with closing action — strong positive
3. Range composition: villain_air_pct ~0.32 (high air — CO checked
   back on a board that favours their range, BB checked)
4. Board: dry, rainbow — low danger
5. Action: both opponents checked — showing weakness

**Factor interaction:** Equity is marginal by reference data. But
IP + high villain air (0.32) + dry board + both opponents showed
weakness = strong factor combination for thin value. Hero's bet
folds out villain's air (which has some equity) and gets called
by worse pairs (77, 88, Jx worse kicker).

**Action:** BET (small, ~33% pot)
**Confidence:** MEDIUM
**Alternative:** CHECK — reasonable for pot control, but leaving
value against two wide, weak ranges.

### Example 3: Fold to bet-and-call despite decent equity

**Setup:** Hero holds Kd Th on Ks Jc 6h. BB, 2 opponents. Pot 155.
CO bet 35, BTN called. Hero faces 35 to call (pot odds ~18.4%).

**Factors:**
1. Equity: ~39.9% (well above pot odds of 18.4%)
2. Position: last to act this street
3. Range composition: CO's bet into 3-way = strong. BTN's cold-call
   of CO's bet = credibly Kx+ or better. Combined range is strong.
4. Board: dry — but irrelevant when both opponents show strength
5. Action: bet-and-call — the strongest signal in multiway poker

**Factor interaction:** Raw equity (39.9%) massively exceeds pot odds
(18.4%), which naively suggests CALL. But the bet-and-call sequence
narrows both opponents' ranges to hands that crush KT. BTN's call
specifically represents KJ, KQ, AK, or better — all dominating
hero's kicker. The raw equity is computed against full preflop ranges,
not the narrowed post-action ranges. This is where action history
overrides equity.

**Original action (pre-solver):** FOLD
**Original confidence:** HIGH
**Original reasoning:** CALL rejected — equity against the
ACTION-IMPLIED ranges (not the preflop ranges) is much lower than
39.9%. Hero is dominated by better Kx and crushed by sets/two-pair.

**⚠ SOLVER CORRECTION (April 2026):** GTO Wizard shows KT on KJ6
facing bet-and-call is a **pure CALL** for all KT combos. Only
KcTs raises (66%). The "action narrows ranges → fold despite
equity" reasoning was over-applied here. While bet-and-call does
narrow ranges, KT still has 40% equity vs 18% pot odds — the
equity surplus is too large for folding to be correct. KT beats
significant portions of both opponents' continuing ranges (worse
Kx, middle pairs, draws).

**Corrected action:** CALL
**Confidence:** HIGH (solver-verified)

**Teaching point:** This example demonstrates a dangerous reasoning
trap. The bet-and-call signal FEELS like it should override equity,
and the logic is internally consistent. But the solver shows that
when equity exceeds pot odds by 20+ percentage points with a made
hand, the action-implied range narrowing is insufficient to flip the
decision from CALL to FOLD. Reserve the "bet-and-call = fold" pattern
for hands where equity is genuinely close to break-even AND hero's
specific holding is dominated (e.g., bottom pair, no draw).

**Composition addendum (v1.3, real feature row):** The feature row
for KcTh on KdJc6s BB vs CO bet + BTN call
(`review/all_557_situations.jsonl` line 120,
`_situation_id = CALL_Board5_KdJc6s_h5`) shows the continuing-range
composition the old "capped + bet+call → fold" reasoning collapsed:

- `villain_top_pair_plus_pct` = **0.3174** (≥20% bucket per
  Section 1.9 — "some value but mostly weaker holdings"; nowhere
  near the ≥60% "heavy with strong hands" threshold)
- `villain_draw_pct` = **0.0878**
- `villain_air_pct` = **0.1856**
- `worse_hand_pct` = **0.8043** (KcTh beats roughly 80% of the
  partition sample)
- `raw_equity` = **0.4323**, `pot_odds` = **0.1842**,
  `equity_margin` = **+0.2480** (equity surplus of ~25 percentage
  points over pot odds)
- `villain_range_capped` = **0** (note: the pipeline's
  `range_capped` bit is 0 here because the *villain*
  captured by the features is CO — the bettor/opener — not the
  BTN cold-caller. This is a structural quirk of the single-villain
  feature extraction, and it is a further reason not to treat the
  bit as a postflop strength signal: it depends on *which*
  opponent the feature pipeline happened to index, not on the
  overall range the hero is facing.)

Reading from the composition triple: the continuing range after
bet+call is ~32% top pair or better, ~9% draws, ~19% air, with
~40% of the range in weaker made hands and pocket pairs across
the remainder. It is **not** "100% better Kx". KcTh dominates a
large portion of the remainder (middle pairs, weaker Kx that BTN
flats preflop, some pocket pairs, missed broadways). Hero's 43%
raw equity against a combined-villain sample reflects exactly
this composition. The "~40% weaker made hands and pocket pairs"
characterisation follows directly from `extract_range_composition`
in `river-rats-core/feature_extractor.py`: the function classifies
each combo via `classify_hand` and sums only the `nuts`,
`strong_value`, `good_value` (TP+), `draw`, `air`, and `bluff`
buckets — `medium_made` and `weak_made` fall through into the
unclassified remainder (see `feature_extractor.py` line 1173 and
the `_TOP_PAIR_PLUS` / `_DRAW_CATEGORIES` / `_AIR_CATEGORIES`
constants at lines 1088-1092). `medium_made` and `weak_made`
correspond exactly to top-pair-weak-kicker, second/middle pair,
underpairs (pocket pairs below the top board card), and bottom
pair (see `range_narrowing.py` lines 213-240), which is the
"weaker made hands and pocket pairs" bucket.

The prior v1.2 reasoning — "capped BTN flat + bet+call → KT is
dominated" — substituted a preflop structural label
("capped") for the actual postflop composition. The composition
triple shows villain's *continuing* range is in the ≥20% TP+
bucket, not the ≥60% bucket the old reasoning implicitly assumed.
The solver correction (MW-30 = pure CALL for all KT combos; see
`feedback_solver_findings.md` finding 6 and
`reference_corrections.md`) is exactly what the composition
triple would predict if read correctly.

**Generalisation.** When facing bet+call with a made hand that
has equity well above pot odds (≥20pp margin), read the
composition triple before folding. If `villain_top_pair_plus_pct`
is in the <40% buckets (i.e. NOT "heavy with strong hands") and
hero's hand dominates some portion of the continuing range, the
bet+call signal alone is insufficient to flip the decision to
fold. Reserve "bet+call = fold" for composition-supported cases:
top pair weak kicker against a ≥60% TP+ continuing range on a
board where hero's kicker is outkicked in the remainder.

### Example 4: Must bet monster — don't slowplay 3-way

**Setup:** Hero holds 8c 8h on Jd 8s 5c. BTN (IP), 2 opponents.
Pot 120. Both check to hero.

**Factors:**
1. Equity: ~82% (middle set, near-nut hand)
2. Position: IP — ideal for building pot
3. Range composition: both opponents checked on a board with
   straight draws and flush draws possible on future streets
4. Board: semi-connected, two-tone possible on turn — danger of
   free cards
5. Action: both checked — giving free cards is dangerous with draws

**Factor interaction:** Monster equity + IP + two opponents who
could have draws = must bet. 3-way, the probability of being
outdrawn on free cards is dramatically higher than HU (two opponents
drawing). Sets MUST bet multiway — slowplaying risks letting
draws get there for free.

**Action:** BET (50-66% pot)
**Confidence:** HIGH
**Alternative:** CHECK (slowplay) — rejected. Multiple opponents =
too many draws in the combined range. Protection is critical.

### Example 5: Draw OOP — check, don't semi-bluff

**Setup:** Hero holds Td 9d on Qd 7h 3d. BB (OOP), 2 opponents.
Pot 90. First to act.

**Factors:**
1. Equity: ~36% (flush draw + gutshot = 12 outs)
2. Position: OOP — worst position for semi-bluffing
3. Range composition: CO's open range contains premiums (AA-QQ, AK),
   BTN's cold-call range excludes those premiums by construction
   but connected range hits middle boards
4. Board: two-tone — flush draw is visible to opponents
5. Action: hero is first to act

**Factor interaction:** Decent draw equity, but OOP + two opponents
= fold equity is ~36% (0.6 x 0.6). Semi-bluff needs fold equity to
be profitable. With two opponents who see the flush draw on board,
even fewer will fold. Check and realize equity cheaply — if someone
bets, calling has correct odds with 12 outs.

**Action:** CHECK
**Confidence:** HIGH
**Alternative:** BET (semi-bluff) — rejected. OOP semi-bluffs into
two opponents have ~36% fold equity at best. With a visible flush
draw on board, actual fold equity is even lower. Check-call is the
line.

### Example 6: OOP value bet — high equity overrides position default

**Setup:** Hero holds Qs Jd on Qc 8d 3s. SB (OOP, first to act),
2 opponents (BTN opened, BB called). Pot 90, not facing bet.

**Factors:**
1. Equity: ~60% (top pair second kicker — strong for 3-way)
2. Position: OOP — normally argues for pot control
3. Range composition: `villain_air_pct` = **0.5222** (very high —
   BTN's CO-open range is heavily skewed toward unpaired broadways
   and suited connectors that miss a Q-8-3 rainbow flop),
   `villain_top_pair_plus_pct` = **0.1222** (<20% bucket per
   Section 1.9 — "thin on value"),
   `villain_draw_pct` = **0.0000** (rainbow, disconnected — no
   flush draws, one gutshot-only range fraction absorbed into air),
   `worse_hand_pct` = **0.9164** (hero's QJ is above ~92% of
   villain's continuing combos), `board_favour` = **+0.1778**
   (positive — board favours hero's range)
4. Board: dry, rainbow, danger 0.00 — static, equity stable
5. Action: hero is first to act, no aggression to respect

**Factor interaction:** OOP position normally defaults to CHECK for
pot control. But this hand has ~66% raw equity with ~92% of
villain's continuing range worse, on a dry rainbow board — far
above the typical OOP pot-control threshold. The key distinction:
"AA checks 80% OOP on dry board" applies to 3-bet pots with deep
SPR where the opponent's composition is in the ≥60% TP+ bucket
and contains AA/KK/AK. Here, in a single-raised pot, the
composition triple shows villain is compositionally thin on value
(`villain_top_pair_plus_pct = 0.1222` — the <20% "thin on value"
bucket; `villain_air_pct = 0.5222` — over half the range is air)
and hero's TPSK is near the top of hero's own range
(`hero_range_percentile = 0.7164`). When `raw_equity` is ~65%+,
`worse_hand_pct` is ≥90%, `villain_top_pair_plus_pct` is in the
<20% bucket, and the board is dry and static (`danger_score =
0.0`), the OOP penalty is insufficient to override the value from
betting. A small bet (25-33% pot) gets called by worse Qx, Jx,
pocket pairs, and the few draws in the air fraction.

**Action:** BET
**Confidence:** HIGH
**Alternative:** CHECK — defensible as pure pot control, but leaves
significant value against two wide, weak ranges. With 88% worse
hands and a dry board, hero's equity is stable enough that OOP
risk is minimal.

**When does OOP default to CHECK instead?** When equity is marginal
(< 50%), `villain_top_pair_plus_pct` is in the ≥40% or ≥60% bucket
(meaningful value density or heavier), or the board is dynamic.
The AA-checks-80% reference data applies to 3-bet pots where the
opponent's continuing range contains AA / KK / AK at high frequency
(a ≥60% TP+ composition) — not to single-raised pots where the
composition triple shows a high-air, low-TP+ range like Example 6.

### Example 7: Overcard equity — AK on a missed board

**Setup:** Hero holds Ad Ks on Jd 8d 4c. BB (OOP), 2 opponents.
Pot 90. CO bets 33 (pot odds 26.8%). draw_outs = 0 in the feature
vector.

**Factors:**
1. Equity: ~25% (no pair, no flush/straight draw per pipeline)
2. Position: OOP — unfavourable
3. Range composition: CO's open range contains premiums (AA/KK/AK),
   villain_top_pair_plus_pct ~0.47 (strong — ≥40% bucket per Section 1.9)
4. Board: semi-wet (two diamonds), danger 0.25
5. Action: facing a standard c-bet from CO

**Factor interaction:** The pipeline reports draw_outs = 0 because
it counts flush draws and straight draws, NOT overcards. But AK
has 6 overcard outs (3 aces + 3 kings) worth ~24% to improve to
top pair by the river. These are "hidden outs" not captured in the
feature vector. When hero hits an ace or king, the hand is likely
best (TPTK). Additionally, AK has backdoor flush draw potential
with Ad. The true equity (~25%) is close to pot odds (26.8%), but
accounting for overcard improvement and implied odds when hero hits,
this becomes a profitable call.

**Action:** CALL
**Confidence:** MEDIUM
**Alternative:** FOLD — defensible if equity is exactly at pot odds
with no improvement path. But AK's overcards provide hidden equity
the feature vector understates. The hand has showdown potential if
checked through on turn, and significant value when it improves.

**Key lesson:** When draw_outs = 0 but hero holds unpaired high
cards (AK, AQ) on a low/medium board, consider overcard outs as
hidden equity not captured in the features. 6 overcards ≈ 24%
improvement probability.

### Example 8: Draw equity survives multi-street aggression

**Setup:** Hero holds Qh Tc on Ks Qd 7c Jh. BTN (IP), 2 opponents.
Turn. Pot 200. CO fires 60 (second barrel). villain_aggression=2.

**Factors:**
1. Equity: ~27% (second pair + open-ended straight draw, 8 outs)
2. Position: IP — favourable for equity realization
3. Range composition: villain_tp_plus 63%, villain_air 4% — very
   strong, value-heavy betting range
4. Board: danger 0.88 (very high), many straights possible
5. Action: CO double-barrel into two opponents — strong signal

**Factor interaction:** Multi-street aggression (villain_aggression=2)
signals a strong, narrow range. The knowledge base teaches that
action history overrides equity for dominated hands without outs
(the MW-30 pattern). But this hand is NOT dominated without outs —
hero has second pair (showdown value) PLUS 8 straight outs (any T
or A makes a straight). The distinction is critical:

- MW-30 pattern (FOLD): top pair weak kicker, no draws, facing
  bet-and-call. Hero is dominated with zero improvement path.
- THIS pattern (CALL): second pair with 8 draw outs, IP, pot odds
  nearly met. Hero has a significant improvement path.

The aggression signal narrows villain's range, reducing hero's
made-hand equity. But the 8 draw outs survive range narrowing —
when hero makes the straight, it beats villain's entire range.
Combined with IP position and nearly correct pot odds, the draw
equity tips the decision from FOLD to CALL.

**Action:** CALL
**Confidence:** MEDIUM
**Alternative:** FOLD — defensible given the multi-street aggression
and 63% TP+ in villain's range. But hero's 8 clean outs to a
straight (~16% per street, ~32% by river) combined with IP position
and current pot odds make calling marginally profitable even against
the narrowed range.

**Key lesson:** "Action history overrides equity" applies to
dominated hands with no outs. When hero has significant draw equity
(8+ outs to a strong hand), the draw equity survives range
narrowing. Don't conflate "villain is strong" with "always fold."

### Example 9: Nut draw with blocker — RAISE, not call (Solver-verified)

**Setup:** Hero holds As Qs on Ks Jd 5s. SB (OOP), 3-way pot
(CO opened, BTN called). Flop. Pot 90. CO bets 30. Hero faces 30.

**Factors:**
1. Equity: ~44% (nut flush draw + two overcards + gutshot to broadway)
2. Position: OOP (SB) — normally argues against semi-bluffing
3. Range composition: CO betting into 3-way = strong range, BTN
   behind still to act
4. Board: Ks Jd 5s — two spades, high cards favour raiser's range
5. Action: facing a single bet from CO, BTN still to act

**Factor interaction:** The default heuristic says "don't semi-bluff
3-way OOP" (DO NOT Rule #2). That rule applies to MOST draws. But
this hand has ALL four conditions from Section 1.7:
- ✅ Nut draw (nut flush draw)
- ✅ Blocker (As blocks villain's nut flush combos, reducing their
  continuing range when facing a raise)
- ✅ Side equity (two overcards = 6 outs to TPTK, gutshot to
  broadway straight)
- Combined: ~44% raw equity + fold equity from the semi-bluff

The As blocker is critical. It removes AsXs combos from villain's
range, meaning when hero raises, villain is less likely to hold a
hand that can continue profitably. Without the As (e.g., 8s7s for
nut flush draw), the raise becomes unprofitable because villain's
continuing range includes the nut flush draw.

**Action:** RAISE
**Confidence:** HIGH (solver-verified — GTO Wizard shows even single
spade holdings raise here)
**Alternative:** CALL — the pre-correction default. Calling is not
terrible (hero has odds), but it wastes the fold equity component.
With the As blocker, raising is clearly +EV vs calling.

**Key lesson:** "Don't semi-bluff 3-way" is a default, not an
absolute. The solver carves out nut draws with blockers + side
equity. The blocker is the key differentiator — without it, the
same draw should call. With it, raise. This is the MW-47 pattern
that was a shared blind spot between the expert and model.

---

## 5. DO NOT Rules

Each rule explains WHY the naive reasoning fails so the agent can
generalise, not memorise.

**1. DO NOT decide based on equity alone.** 3-way decisions depend
on the interaction of all 5 factors. 55% equity is a BET when IP +
air-heavy villain + dry board, but a CHECK when OOP + strong villain
range + wet board. Equity is an input, not a threshold.

**2. DO NOT barrel draws into 2 opponents hoping for folds — UNLESS
you hold the nut draw with a blocker.** 3-way fold equity is ~36%
(0.6 x 0.6). A flush draw semi-bluff that prints money HU (60%
fold equity) loses money 3-way. Check and realize equity for most
draws. **Exception (solver-verified):** Nut draws (nut flush draw,
nut straight draw) with a blocker to villain's continuing range
AND side equity (overcards, gutshot) should RAISE. The blocker
increases fold equity above the 3-way threshold, and the combined
draw + side equity provides enough value when called. See Section
1.7 and Worked Example 9 for the full conditions.

**3. DO NOT assume the checking player has nothing.** 3-way, players
trap more because a third opponent may bet for them. A check-raise
into two opponents is almost exclusively the nuts.

**4. DO NOT auto-c-bet IP just because you have position.** IP
c-bet frequency 3-way is 30-45%, not 65%+. Two opponents = two
chances to run into strength. Board texture and range composition
determine whether to bet.

**5. DO NOT treat top pair as a strong hand.** Top pair is medium-
strength 3-way. The threshold for "strong enough to build a pot"
shifts up by roughly one hand class: two pair+ to bet big, vs TP+
in HU. Top pair good kicker is a pot-control hand.

**6. DO NOT overweight blockers for bluff selection — but DO use
them for action selection.** Blockers for choosing WHICH bluffs to
run matter ~40% less 3-way (need to block both opponents). But
blockers for deciding RAISE vs CALL with a strong draw or made hand
are still critical — solver shows suit holdings swing raise
frequency by 40+ percentage points for the same hand. See Section
1.8. **Defender-side blocker direction (v2.4):** see §1.10-§1.12
for the four blocker-direction features
(`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`,
`nut_made_block_pct`) that encode when a blocker works FOR hero's
CALL (nut-made blocked → more bluff-catch) vs AGAINST hero's CALL
(draws blocked → densification toward value).

**7. DO NOT analyze streets in isolation.** A pot-sized flop bet
3-way leaves SPR ~1.5 on the turn. The flop decision must account
for the full remaining tree at compressed SPR.

**8. DO NOT assume both opponents have equivalent ranges, and DO
NOT use `villain_range_capped` as a postflop strength signal.**
The two opponents in a 3-way pot have different preflop range
constructions, and those constructions must be read through the
postflop composition triple — not via a binary preflop label.

- **Cold-caller (BTN flat vs CO open):** Preflop range excludes
  AA / KK / QQ / AKs by construction (those hands 3-bet preflop).
  Contains 22-TT, suited broadway, suited connectors, suited aces.
  On connected / middling / two-tone boards the cold-caller's
  postflop composition can still be heavy with TP+ and draws —
  check the composition triple, not the preflop construction.
- **Blind defender (BB):** Preflop range is wider (speculative
  suited/connected, small pairs, some broadway) and includes some
  premium combos at squeeze frequency. High preflop air, but low
  connected boards can invert the composition toward strong
  holdings and sets.

The operative asymmetry for postflop labelling is: the cold-caller
folds strong draws less often (sticky continuing range, low air
on connecting boards), the blind defender folds air more often
(wide construction leaves more combos that miss any given flop).
But this is a *generalisation about what the composition triple
will typically look like*, not a substitute for reading it.

**Do NOT use `villain_range_capped` as a postflop strength signal.**
The pipeline exposes this feature (see
`river-rats-core/feature_extractor.py:1195-1197`), but it encodes
preflop action geometry only — it is `int(not is_3bet_pot and
villain_is_defender)`, a pure flag for "villain was the preflop
caller in a non-3-bet pot". It says nothing about the current
continuing range's TP+ / draw / air split. Postflop strength is
measured by `villain_top_pair_plus_pct`,
`villain_draw_pct`, and `villain_air_pct` — read those against
the Section 1.9 buckets and use the preflop action sequence only
to inform *how* the preflop range was constructed. If the binary
and the composition triple appear to conflict, the composition
triple is authoritative. See Section 1.9.

---

## 6. Sources

**Solver-based (highest authority):**
- GTO Wizard blog (10+ articles on multiway strategy)
- PioSolver equity realization studies
- MonkerSolver multiway benchmarks

**Expert with solver support:**
- Phil Galfond (philgalfond.com) — multiway pot framework
- Peter Clarke — multiway postflop principles
- PokerCoaching.com — multiway modules
- Run It Once — multiway strategy content

**Theoretical:**
- MDF/Alpha math (universally accepted)
- Equity dilution calculations

**Full source index:** See `research/` directory for 80+ cited URLs
with per-source classification.

## 7. Ignore List

- Pre-2018 poker forum advice (outdated, pre-solver era)
- HU-focused content applied to multiway without adjustment
- Exploitative "read-based" frameworks (not GTO)
- Any source that uses HU c-bet frequencies in multiway spots
- Doug Polk / Upswing HU-specific content repurposed for multiway

---

## Version History

- **v1.3 (10 Apr 2026):** Vocabulary purge and postflop composition
  reframing. Removed the words "capped" and "uncapped" from the KB
  body entirely (19 occurrences across Section 1 Factor 3, Section 3
  preflop construction, Examples 1 / 5 / 6 / 7, and DO NOT Rule #8),
  replacing them with compositional / "range excludes X by
  construction" language. Added Section 1.9 (Preflop geometry vs
  postflop composition) as the load-bearing principle — preflop
  structural facts are a *generator* for the postflop composition
  triple (`villain_top_pair_plus_pct` / `villain_draw_pct` /
  `villain_air_pct`), not a substitute for it. Rewrote Factor 3 to
  demote `villain_range_capped` out of the postflop signal list
  (it encodes preflop action geometry; the feature stays in the
  pipeline but must not be used as a postflop strength signal).
  Rewrote Example 3 (MW-30) and Example 6 with real feature values
  from `review/all_557_situations.jsonl` and live
  `feature_extractor.py` extraction. Rewrote DO NOT Rule #8 to
  preserve the BTN-vs-BB asymmetry compositionally and to instruct
  the labelling agent explicitly not to use `villain_range_capped`
  as a postflop signal. Adopted teaching's TP+ buckets (≥60 / ≥40
  / ≥20 / <20) as shared vocabulary with
  `river-rats-teaching/interface/l3_renderer.py` — provisional
  pending calibration, TODO logged for the next feature-importance
  audit. Rationale: the binary "capped/uncapped" framing was too
  fixed, lacked nuance, and was being used by the labelling agent
  as a postflop shortcut that contributed to the MW-30 / MW-46 /
  MW-50 over-fold pattern. See `review/comms/KB_V1.3_EDIT_PLAN.md`
  and `review/comms/REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md`.
- **v1.2 (7 Apr 2026):** Solver-verified corrections from 3 GTO
  Wizard solves. Added: Section 1.7 (semi-bluff conditions), Section
  1.8 (blocker action selection), Worked Example 9 (nut draw raise).
  Corrected: Example 3 (MW-30 FOLD→CALL with teaching note), DO NOT
  Rule #2 (semi-bluff carve-out for nut draws with blockers), DO NOT
  Rule #6 (blockers still critical for action selection). Updated
  Factor 5 (bet-and-call signal qualifier, check-raise exception for
  trips+). 4 solver rules integrated, 5 labelling biases addressed.
- **v1.1 (6 Apr 2026):** Added 3 worked examples from calibration
  exam failures. Fixes: OOP value betting exception (Example 6),
  overcard hidden equity (Example 7), draw equity surviving
  aggression (Example 8). Now 8 examples total. Calibration:
  v1.0 scored 20/24, v1.1 targets fixing MW-17/24/28/41.
- **v1.0 (6 Apr 2026):** Initial knowledge base. 5 worked examples,
  8 DO NOT rules, quantified reference data from 80+ sources.
  Research files in `research/` directory.

After each training gate, failures are analyzed and new worked
examples are added. Principles stay stable. Examples accumulate.
