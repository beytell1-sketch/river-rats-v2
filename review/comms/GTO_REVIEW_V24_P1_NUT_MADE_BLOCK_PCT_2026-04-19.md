---
date: 2026-04-19
from: GTO Reviewer (subagent)
to: Builder / Main terminal / Owner
re: GTO review of v2.4 P1 plan #3 — `nut_made_block_pct`
status: REVIEW COMPLETE
verdict: APPROVED_WITH_MODIFICATIONS
related: BUILDER_V24_P1_PLAN_NUT_MADE_BLOCK_PCT_2026-04-19.md, TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md, knowledge/three_way_gto.md §1.7-§1.8, prompts/gto_labeller_v3.1.md
---

# GTO Review — `nut_made_block_pct` (Feature 3 of 3)

## Verdict

**APPROVED_WITH_MODIFICATIONS**

The feature is poker-sound, fills a real gap that `flush_block_pct` cannot
address (non-flush nut classes), and is coherent with the covering-triple
framing. It is not a strict superset of `flush_block_pct`, however — see
Retirement section. Modifications below are required before coding; all
are small scope changes and definitional tightening, not architectural.

## Summary (orchestrator cliff notes, <300 words)

The "nut-made" class — straight-flush, quads, full-house, nut flush, nut
straight, top-set — is the correct primitive. It is exactly villain's
"stack-off range" in the solver sense: combos that will never fold to any
bet/raise. Fraction-of-nut-made blocked is the cleanest possible signal
for bluff-catcher vs thin-value decisions on the defensive side, and
complements `nut_flush_block` (single-card aggressor trigger) and
`draw_block_pct` (bluff-removal, fold-lean) to form the covering triple
described in plan §"Interaction with plans 1 and 2".

**However, `nut_made_block_pct` does NOT strictly subsume
`flush_block_pct`.** `flush_block_pct` covers nut AND non-nut flush
combos; `nut_made_block_pct` only covers nut flush. A hero with Ks on a
monotone-spade board blocks villain's second-nut flush (Ks-flush)
combos — that signal is zero in `nut_made_block_pct` but positive in
`flush_block_pct`. This is a real gap on monotone / double-flush
textures. The fix is to add a small definitional tweak (include
**second-nut flush when A-of-suit is on the board**), which keeps the
feature nut-class strict on most boards but covers the one texture where
"second nut = effective nut".

The proposed A/B retirement comparison (v2.4 with vs without
`flush_block_pct`) is the correct test. Feature-importance alone is
insufficient because XGBoost gain on a correlated feature can collapse
toward zero while the feature still carries a unique signal on a narrow
texture subset. Recommendation: A/B comparison gated on both calibration
anchors AND a monotone-texture sanity sweep (see §Retirement below).

Grammar of covering-triple is sound: directional interpretation (positive
when defending for `nut_made_block_pct`, negative when defending for
`draw_block_pct`) matches solver intuition and KB §1.7-§1.8. Approved
with the four modifications below.

---

## Required modifications (before coding)

### M1. Add second-nut flush to the nut-made class ON BOARDS WHERE IT IS EFFECTIVELY NUT

**Why:** On a board with the Ace of the flush suit already on board
(e.g., A♠ K♠ 7♠), the second-nut flush (K-high) is the effective nut
because the A♠ cannot be in villain's hand. Without this carve-out,
`nut_made_block_pct` returns 0 when hero holds K♠ on A♠K♠7♠ — but
K♠-flush IS the stack-off class in that exact scenario. This is the most
common texture on which `flush_block_pct` carries non-trivial signal
that `nut_made_block_pct` would miss. Excluding it leaves the retirement
gate permanently failable on a narrow-but-real subset.

**Rule:**
```
"Effective nut flush" = highest flush possible given board cards.
  If A-of-suit is ON THE BOARD, then K-of-suit is effective nut.
  If A-of-suit AND K-of-suit on board, Q-of-suit is effective nut.
  (In practice, >2 high cards on board of same suit is very rare;
  clamp at second-nut.)
```

Include `strong_flush` in `_NUT_MADE_SUBCATS` **only when A-of-suit is
on the board**. On all other boards, `strong_flush` stays excluded.
Implementation-wise: check board for A-of-flush-suit before adding
`strong_flush` to the subcats set for that specific board.

### M2. Resolve "top set on paired board" explicitly via the taxonomy

Per the range_decomposition.py classifier (lines 254-273), `top_set`
already means "pocket pair matches TOP board rank". On 888, "top set"
would be quads (pocket 88 + trips on board). The classifier lands
those in `quads`, not `top_set`. So the plan's concern is already
handled by the classifier — but call this out explicitly in the
feature docstring to prevent future confusion:

```
# On boards where the top rank is already paired (e.g., 8h8c3d), hero's
# 88 classifies as 'quads', not 'top_set'. 'top_set' is therefore naturally
# restricted to unpaired top-rank boards. No special-case logic needed.
```

**Also add:** on doubly paired boards (e.g., 8h8c3c3d), top-set is
undefined; classifier routes to `full_house`. Again handled, but
document.

### M3. Restrict `nut_straight` to the highest-possible straight strictly

Per plan open question 3: the existing `_is_nut_straight` in
range_decomposition.py (line 383) already enforces "strictly highest
possible given board". Keep that. A "weak_straight" on JhTh9s (e.g.,
Q8 making 8-Q straight while KQ makes 9-K straight) should NOT count
as nut-made — it's vulnerable and will fold to a high-enough bet.
This is correct as-plannened.

**Edge case to handle:** on very connected boards (e.g., 9-T-J), both
7-8 and Q-K make straights. Classifier will call 7-8 `weak_straight`
and Q-K `nut_straight`. Good. But: on a board like 8-9-T, the nut
straight is Q-J (Q-high) AND J-7 is a weak straight. Solver treats
Q-J as stack-off; J-7 is a bluff-catcher that folds to turn action.
Correct to exclude J-7 from nut_made class.

### M4. Add `combo_draw` guard + verify subcategory string exactness

Plan's pseudocode uses `bucket.subcategory not in _NUT_MADE_SUBCATS`.
Verify the strings match exactly:

- `range_decomposition.py` line 82: `SUBCATEGORY_ORDER` contains
  `'straight_flush', 'quads', 'full_house', 'nut_flush', 'strong_flush',
  'weak_flush', 'nut_straight', 'weak_straight', 'top_set', ...`
- Plan's `_NUT_MADE_SUBCATS` uses: `'straight_flush', 'quads',
  'full_house', 'nut_flush', 'nut_straight', 'top_set'`

Strings match. Good. Add a unit test that asserts every string in
`_NUT_MADE_SUBCATS` appears in `SUBCATEGORY_ORDER` to guard against
taxonomy drift.

---

## Answers to the 5 open questions

### Q1. What counts as "nut made"? Include second nut flush / top-two-pair?

**Answer: Strict nut class PLUS "effective nut" carve-out (M1 above).**

- **Second nut flush:** Include ONLY when A-of-suit is on the board
  (see M1). Otherwise exclude. Rationale: the solver treats
  second-nut-flush as a value-but-callable hand HU, and a clear
  stack-off 3-way only when it IS the effective nut. Don't include
  K-high flush across the board — it dilutes the feature on boards
  where A♠ + K♠ in holes represents two completely different decisions.

- **Top-two-pair (e.g., AK on Ad Kd 7c):** EXCLUDE.
  - Top-two IS stack-off-class HU. But 3-way, top-two loses to sets,
    and the solver shows top-two checking back or pot-controlling on
    many dynamic boards (KB §1.2 — TPTK drops ~12pp 3-way; two-pair
    drops similarly). Solver stack-off frequency for top-two 3-way is
    70-85% depending on texture — not the near-100% of sets and
    straights.
  - Including it would dilute the feature: the nut-class is supposed
    to identify villain combos that NEVER fold. Top-two folds on
    enough boards (wet, multi-straight, multi-flush) to break that
    property.
  - Keep the feature tight. The model learns the top-two density via
    existing features (`hand_category`, `is_strong_made`).

- **Broader "could include" list (REJECTED):** overpairs, TPTK,
  second set. All of these are bluff-catchers or thin value 3-way
  per KB §1.2/§1.5, not stack-off class. Excluding is correct.

### Q2. Top-set on paired board

**Answer: Naturally excluded by the classifier — no special case needed.**

On 8h8c3d: hero with 88 already classifies as `quads` in
range_decomposition.py (line 216-218), not `top_set`. Plan's proposal
("`top_set` undefined on paired boards, only counts quads/full_house
there") is factually already the classifier's behavior. Adopt as
documentation only (see M2).

### Q3. Nut-straight ambiguity on connected boards

**Answer: Strictly highest. Plan's current position is correct.**

`_is_nut_straight` (range_decomposition.py line 383) already enforces
this. Solver treats non-nut straights as bluff-catchers or thin value
on connected boards because a higher straight is always live on
further streets. Any relaxation ("any high-made straight counts")
would (a) break the "nut class = stack-off" invariant and (b) create
a noisier signal on J-T-9 / 9-8-7 textures where 3-4 straights are
simultaneously possible. Keep strict.

### Q4. Multiway nut dilution — weight differently HU vs 3-way?

**Answer: No explicit reweighting. Use raw fraction as planned;
model learns weighting via `num_opponents` interaction.**

Reasoning:
- The feature is already implicitly dilution-aware because
  `range_breakdown.total_combos` is computed against the specific
  opponent's range. HU vs 3-way villain ranges differ in combo counts,
  and the fraction is self-normalizing.
- Absolute nut-made count IS lower 3-way (ranges are narrower), but
  that's a density question, not a directional question. The
  fraction-blocked interpretation is consistent in both cases: "I
  block X% of their nut-made combos" — same meaning, same positive-
  defending interpretation.
- Explicit reweighting (e.g., halving the feature value 3-way) would
  bake a heuristic into a feature that should remain a measurement.
  `num_opponents` is already in the feature vector; let XGBoost
  discover any interaction in training.

**Caveat:** For monitoring — after training, check feature_importance
partitioned by `num_opponents`. If the feature only fires HU, the
3-way signal is too sparse and a reweighted version should be tested
in v2.5+. Not a gate for v2.4.

### Q5. Retirement criteria for `flush_block_pct` — A/B test vs feature-importance threshold?

**Answer: A/B test on calibration anchors + self-play + a monotone-
texture sanity sweep. Feature-importance alone is insufficient.**

Reasoning:
- **Feature-importance threshold alone is NOT sufficient.** Two
  correlated features will share gain (tree either routes through
  one or the other). `flush_block_pct` could show <1% gain and still
  carry unique signal on a narrow subset (monotone flush boards with
  second-nut blocker — see M1). Dropping on importance alone risks
  losing that subset.
- **A/B on calibration anchors is necessary.** The v2.3 calibration
  anchors (MW-30, MW-33, MW-50, d8886, d2410, d8963, d3178) don't
  heavily load on flush blockers, so add a monotone-texture sanity
  pass: hand-pick 50-100 hands from the training set with hero on
  a 3+ flush board with a non-Ace flush card. Compare v2.4 and
  v2.4' (retired) action distributions on just those hands. If v2.4'
  regresses (e.g., over-calls on defending blocker spots),
  `flush_block_pct` stays. If distributions match, retire.
- **Sequencing gate:** Require BOTH calibration pass AND the
  monotone sanity pass before retirement. Either failing → retain
  `flush_block_pct`.

Plan's proposed sequence (train with both → compare with/without)
is correct. Add the monotone sanity sweep as the tie-breaker.

---

## Missing cases / additional checks

- **Straight-flush on paired board:** vanishingly rare but possible
  (e.g., 5h6h7h board, hero has 4h8h). The classifier returns
  `straight_flush`. Included in nut-made. Correct.

- **Quads on board (e.g., 7777x):** hero can't make quads, villain
  makes quads with any non-board card + a 7 (hero blocks nothing
  specific unless hero has the 7). `nut_combos = 0` → feature returns
  0.0 (plan handles via `if nut_combos == 0: return 0.0`). Good.

- **Double-paired boards (e.g., 7c7d3h3s):** nut-made is full house
  or quads. Classifier handles. Top-set is naturally undefined here
  per M2. Good.

- **Sub-case: hero has the nut-made hand himself.** E.g., hero has
  As-Ks on Qs-Js-Ts (hero has straight-flush, which IS nut-made).
  Plan's logic: hero blocks villain's AsKs combo... but hero IS
  AsKs, so villain cannot have it. This IS a blocker — hero removes
  100% of villain's straight-flush combos. Counter-intuitively
  useful: when hero has the absolute nuts, the feature reports 100%
  nut-blocked, which redundantly confirms "I have the nuts".
  Arguably fine — it's a correct measurement, and the model already
  has `is_monster` to avoid over-weighting. Not a blocker. Worth a
  unit test to verify expected 1.0 output on this case.

- **Runner-runner nut possibilities on flop:** on a 2-flush flop,
  villain's "nut flush" range is the Ace-of-suit with any other card
  in the flop's flush suit AND one additional suited card by river.
  Plan correctly applies the classifier at the CURRENT street —
  so on flop with 2-spade board, villain's Ace-of-spades hand is
  currently a `nut_flush_draw`, not `nut_flush`. Good. The feature
  accurately captures "made nut", not "potential nut". The
  draw-side blocking is the scope of plan #2 (`draw_block_pct`).

- **Direction sign sanity check:** The plan claims
  `nut_made_block_pct` is POSITIVE when defending (villain's value
  blocked → more bluff-catch equity). Verify: on a turn-bet facing
  spot, if hero blocks 40% of villain's nut-made, villain's betting
  range is less value-weighted → hero's bluff-catcher has better
  equity → CALL-lean. Yes, correct. This is the mirror of
  `draw_block_pct`'s fold-lean direction, forming the covering
  triple. Consistent with KB §1.7's "blocker to opponent's
  continuing range" framing, extended from nut-flush to all nut
  classes.

---

## Covering-triple coherence check

| Feature | Class | Defending interpretation | Aggressor interpretation |
|---|---|---|---|
| `nut_flush_block` (boolean) | Single most decisive blocker | Slight CALL-lean | Strong RAISE-lean (KB §1.7) |
| `draw_block_pct` (continuous) | Bluff-removal / densification | **FOLD-lean** | (Not primary; weaker effect) |
| `nut_made_block_pct` (continuous) | Value-removal / bluff-catch | **CALL-lean** | Thin RAISE-lean (extra value block) |

The three features give the model two orthogonal signals on defense
(CALL vs FOLD) and one strong signal on offense (RAISE). This is a
well-formed basis — no collinearity issues on the definitions.
`nut_flush_block` overlaps with `nut_made_block_pct` by 1 combo class
(nut flush) but is dominated by boolean specificity on the key
decision. Approved as a covering triple.

---

## Retirement verdict on `flush_block_pct`

**Conditional retirement.** After this feature lands:

1. Train v2.4 with all 4 features present (116 cols).
2. Run calibration anchors + monotone-texture sanity sweep.
3. If `flush_block_pct` feature_importance < 1% AND removing it
   does not regress calibration OR monotone sanity → retire.
4. If feature_importance < 1% but monotone sanity regresses → KEEP
   `flush_block_pct` (the signal is narrow but real).
5. If feature_importance >= 1% → KEEP regardless.

The plan's retirement sequence is sound with the monotone-sweep
addition.

---

## Summary

| Item | Verdict |
|---|---|
| Nut-made primitive (set of 6 subcats) | PASS (with M1 tweak for A-on-board second-nut) |
| Covers what `flush_block_pct` covers | PARTIAL — fix via M1 |
| Extends to non-flush classes | PASS — this is the load-bearing justification |
| Interaction with plans 1 & 2 (covering triple) | PASS |
| Paired board handling | PASS (already handled by classifier) |
| Connected board handling | PASS (strict highest-straight) |
| Retirement strategy | PASS with added monotone-sanity-sweep gate |

**Final: APPROVED_WITH_MODIFICATIONS.** Apply M1-M4, then proceed to
code. No need for a second GTO review pass on implementation unless
the modifications expand scope.

---

*Review complete. Reviewer: GTO-reviewer subagent. Reasoned from
solver theory (KB §1.7-1.8, Worked Example 9), existing taxonomy
(range_decomposition.py), and covering-triple framing with plans 1
and 2.*
