---
date: 2026-04-19
from: GTO Reviewer (subagent)
to: Builder, Main terminal / Owner
re: GTO REVIEW — v2.4 P1 `draw_block_pct` plan
status: APPROVED_WITH_MODIFICATIONS
reviewing: BUILDER_V24_P1_PLAN_DRAW_BLOCK_PCT_2026-04-19.md
kb_refs: three_way_gto.md §1.1, §1.4, §1.7, §1.8, DO NOT Rule 6
ticket_ref: TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md
---

# GTO Review — `draw_block_pct` (Feature 2 of 3)

## Verdict

**APPROVED_WITH_MODIFICATIONS.** The feature correctly targets the
densification effect the owner's Apr 18 observation exposed and is
grounded in KB §1.1, §1.4, and §1.7. Two required modifications before
code: (1) an implementation-contract correction (`HandBucket.combos`
does not exist in `range_decomposition.py` as shipped), (2) a
granularity decision on combined-vs-split that the plan left open.
One strongly recommended optional: weight-by-outs semantics.

---

## 1. Poker correctness — does the feature capture the densification the owner flagged?

**Yes, directionally.** The owner's scenario (mid pair + one spade on
a two-spade board, villain bets) is the textbook densification /
unblocker effect. The solver math:

- Villain's pre-bet range contains some flush-draw semi-bluff combos.
  Per KB §1.1, 3-way fold equity at 0.70 x 0.70 ≈ 49% means **pure
  bluffs are unprofitable** and the only semi-bluffs that survive as
  bets 3-way are nut draws with blockers + side equity (KB §1.7). So
  villain's "bet with a draw" class is already thin.
- Given villain bet, the bluff-to-value ratio 3-way is already tight
  (KB §1.4: ~1:4 or tighter on river, tighter than HU). Hero's
  blocker removes a fraction of the already-thin semi-bluff component
  from the betting range. The remaining range densifies to value.
- Hero's bluff-catcher equity against the densified range is lower
  than `equity_vs_range` reports, because `equity_vs_range` is
  computed against villain's combined (pre-removal) betting range.
  `draw_block_pct` is the signal that quantifies the gap.

The direction in the plan (§"Expected model behavior") is correct:

- **Defender + marginal made + high `draw_block_pct`** → fold-lean.
  This is the target signal.
- **Aggressor bluffing** → near-neutral (villain folds draws either
  way). Correct.
- **Value betting** → mildly negative on thin value. Correct —
  blocking semi-bluff calls means villain's calling range is
  value-denser.

## 2. Draw-subcategory primitive — is `_DRAWS = {combo_draw,
nut_flush_draw, flush_draw, oesd, gutshot}` the right set?

**Mostly yes, with one flag.** The set covers the combos that
`villain_draw_pct` already treats as "draws" and that KB §1.7 names
as semi-bluff candidates. One caveat:

- **`gutshot` is too wide.** Per KB §1.7 and DO NOT Rule 2, gutshots
  do NOT qualify as semi-bluffs 3-way — "Gutshot-only or
  backdoor-only — check/fold." Villain is not betting naked gutshots
  3-way in any GTO frequency worth tracking. Including gutshots in
  the denominator will dilute the feature: hero's blocker pct will
  look smaller than the actual effect on *bet-frequency-weighted*
  draws.
- `combo_draw` (flush draw + straight draw = 15+ outs) and
  `nut_flush_draw` are the primary solver-verified semi-bluff
  combos. `flush_draw` (non-nut) bets occasionally at mixed
  frequency. `oesd` bets at some frequency on specific textures.
- **Recommendation (optional but strong):** either weight by
  solver-appropriate semi-bluff frequency, or drop `gutshot` from
  the `_DRAWS` set. Simplest correct version: keep the set as-is
  for v2.4 P1 (matches `villain_draw_pct`'s scope) and flag
  "bet-frequency weighting" as a v2.5 refinement.

## 3. Directional interpretation audit

Plan's directional claim matches solver theory. Adding one nuance
the plan didn't surface:

- **Defender + marginal made + HIGH `draw_block_pct`** is fold-lean
  ONLY when villain's betting range still contains *some* draw
  combos pre-removal (i.e. the feature is measured against a
  non-degenerate denominator). On truly dry rainbow boards where
  villain has ~0 draw combos, the feature is irrelevant — there
  is no draw-class to remove. The model should learn this
  interaction with `villain_draw_pct` (see Q4 below).
- **IP value bet with high `draw_block_pct`** is slightly worse
  than the plan suggests. Removing villain's semi-bluff *calls*
  means the worse-hand portion of the calling range shrinks, so
  thin value gets called fairly and rarely by worse. The plan
  flags this correctly; I confirm.

## 4. Interaction with `villain_draw_pct`

**Both are needed.** `villain_draw_pct` is the SIZE of the draw
bucket in villain's pre-bet range; `draw_block_pct` is the
FRACTION of that bucket hero removes. Low `villain_draw_pct` x
high `draw_block_pct` = hero blocks most of a small draw portion
— net impact on bet densification is small. High x high = hero
blocks most of a large draw portion — big densification. Tree
splits on `villain_draw_pct` first, then `draw_block_pct` within
each bin, are the natural way for XGBoost to learn the product.
See Q4 answer below for whether to expose a derived product.

## 5. Connected boards — combined vs split

The plan's main open question. On 9h8s5c with hero Th (gutshot +
one spade), hero blocks some OESD combos (JT, 76 combos
containing Th) *and* potentially some flush-draw combos on a
future turn. The combined `draw_block_pct` collapses these.
Splitting into `flush_draw_block_pct` and `straight_draw_block_pct`
gives the model two orthogonal signals. See Q1 answer below.

---

## 6. Implementation-contract bug (MUST FIX before code)

The plan's pseudocode does:

```python
for bucket in range_breakdown.buckets:
    ...
    for combo in bucket.combos:  # <-- bucket.combos DOES NOT EXIST
```

`HandBucket` in `river-rats-core/range_decomposition.py` lines 42-51
has fields: `category, subcategory, total_combos, beats_hero,
loses_to_hero, pct_of_range`. No `combos` list. The per-combo
iteration happens inside `decompose_range` (lines 708-731) and is
aggregated away before `HandBucket` is built.

**Options:**

1. **Recommended:** mirror `decompose_range`'s inner loop inside a
   new `_draw_block_pct` function in `feature_extractor.py`: iterate
   `villain_range` → `get_valid_combos(hand_str, used_cards)` → for
   each combo, classify via `_classify_combo_subcategory` → if
   subcategory in `_DRAWS`, increment denominator; check hero-card
   overlap on the combo for numerator. This avoids touching
   `range_decomposition.py` and keeps the feature computable without
   running the full 285-combo eval7 pass on every hand.
2. **Alternative:** extend `HandBucket` to carry a `combos:
   List[Tuple[str, str]]` field for the `_DRAWS` subcategories only
   (keep memory tight). Then Builder's pseudocode works. But this
   re-enables every downstream consumer of `decompose_range` and may
   regress the <20ms performance target.

Option 1 is cheaper and isolates the change.

---

## 7. Answers to the 5 open questions

### Q1. Combined `draw_block_pct` vs split flush/straight?

**Split them.** Reasoning:

- The owner's flagged scenario is flush-specific (two-spade board,
  hero holds J♠). Flush-draw blocking and straight-draw blocking
  have different board-texture prerequisites: a monotone / two-tone
  board has flush-draw combos but not necessarily straight-draw
  combos, and vice versa on a 9-high connected board.
- The combined metric creates a floor-ceiling artifact: on a
  monotone board hero might have `draw_block_pct` ≈ 0.4 (blocking
  all flush draws he can), while on a connected rainbow board the
  same 0.4 would reflect blocking straight draws but no flush draws.
  The model cannot distinguish these, yet they have different
  downstream implications (flush draws → single-card out class on
  one street; straight draws → two directional classes, unblockers
  matter — see Q3).
- Splitting produces **two sparse features** (lots of zeros on
  boards without that draw class), which XGBoost handles cleanly.
- **Concrete example (KB §1.7):** On Ks Jd 5s (two spades), AsQs
  is the solver's canonical semi-bluff RAISE. The As blocker is
  specifically flush-related. Splitting lets the model learn
  "flush-draw blocking on wet-spade board signals defensive fold-
  lean" independent of any straight-draw signal that wouldn't
  apply on Ks Jd 5s anyway.

**Recommended feature split:** `flush_draw_block_pct` (combo_draw +
nut_flush_draw + flush_draw) and `straight_draw_block_pct` (combo_draw
+ oesd + [gutshot optional — see §2]). Note `combo_draw` appears in
both because hero can block a combo-draw combo via either its flush
suit or a straight-completing rank. This is correct (not double-
counting — the combo is one combo with two removal vectors; which
feature catches it depends on *which* of hero's cards overlapped).

### Q2. Weight by outs?

**Strongly recommended as optional follow-up; not required for P1.**

Solver-theoretic reasoning:

- A 15-out combo-draw has ~54% equity vs a made hand by the river
  from the flop; a 9-out flush draw ~35%; an 8-out OESD ~32%; a
  4-out gutshot ~17% (per standard Rule of 4 approximations). The
  *fold equity contribution* villain expects when betting a draw
  scales roughly with the hand's when-called equity — more equity
  = villain bets more often. So blocking a combo-draw combo
  removes more "bettor mass" than blocking a gutshot combo.
- Unweighted `draw_block_pct` treats 1 combo-draw combo = 1 gutshot
  combo, which is a 3x overcount of gutshot impact on bet density.
- The weighted variant `sum(blocked * outs) / sum(all_draws * outs)`
  (plan's proposal) is the right shape. I would use equity-at-next-
  street rather than raw outs (gutshot outs often have dirty outs;
  combo draws have redraws), but outs is a cheap proxy that
  captures 80% of the effect.

**Recommendation:** ship unweighted in P1 to validate the signal is
learnable at all. Add `draw_block_pct_weighted` as a v2.5 feature
if feature-importance audit shows the unweighted version is
marginal but directional. Documenting this as a known refinement
in the plan is sufficient for P1.

### Q3. Suit/rank awareness for straight-draw unblockers?

**Not at feature level for P1; handled implicitly.** Reasoning:

- The plan's per-combo iteration checks "does villain combo contain
  a hero card?" which is inherently rank-aware for straight draws:
  hero's Th on 9h8s5c blocks JTs/JTo straight-draw combos
  containing a T but not 76 straight-draw combos. That asymmetry
  is captured by counting actual combo overlaps, not by abstract
  "straight-draw class" presence.
- However, the feature does NOT distinguish "hero blocks a
  nut-straight-draw-completer" (JT on 9h8s5c — JT makes nut
  straight) from "hero blocks a weak-straight-draw-completer"
  (76 on 9h8s5c — makes one-liner straight). For P1, treating all
  straight-draw combos equally is acceptable since the bet-
  frequency difference between nut vs weak straight draws 3-way is
  small (both are mixed-strategy at best per KB §1.7).
- **What the feature WILL miss:** unblocker effects. On 9h8s5c, if
  hero holds Kh (irrelevant rank) he doesn't block ANY straight
  draws but he *also doesn't help villain's straight-draw range*.
  That's fine — no signal needed. If hero holds Th (blocks JT),
  the feature correctly reports a non-zero block pct. What it
  *doesn't* say is "hero unblocks 76 because hero has no 6 or 7"
  — but that's the default state (hero has 2 cards, most hands
  are unblocked). The feature is one-sided by design: only blocked
  combos count; unblocked are the denominator.
- **Recommendation:** acceptable as-is for P1. Rank-aware variants
  (weight blocked combos by their equity share within the draw
  class) are a v2.5+ question.

### Q4. Derived `effective_draw_block = villain_draw_pct * draw_block_pct`?

**Do NOT expose as a separate feature. Let the model learn the
interaction via tree splits.** Reasoning:

- XGBoost naturally learns multiplicative interactions through
  sequential splits. A split on `villain_draw_pct >= 0.10`
  followed by a split on `draw_block_pct >= 0.30` within the
  high-draw-pct branch is equivalent to a threshold on the
  product, and the tree can also learn asymmetric thresholds that
  a scalar product cannot.
- Adding a derived product feature risks **feature collinearity**:
  the product is a deterministic function of the two inputs. This
  doesn't hurt XGBoost (unlike linear models) but it inflates the
  SHAP attribution budget — the product feature will absorb
  attribution that should go to the two primitives. In a pipeline
  where we care about SHAP ordering for teaching (per River Rats
  v3 design), this matters.
- **Exception:** if empirical validation on the training set shows
  XGBoost cannot split cleanly on the two features in interaction
  (e.g. tree depth too shallow), the derived product becomes
  useful. Defer to post-training feature-importance audit.

### Q5. Numerical stability when villain has no draw combos

**Return 0.0 (current plan) is correct. Do NOT use NaN.** Reasoning:

- 0.0 has the correct semantic: "hero's blocker removes 0 fraction
  of villain's draw range" — which is trivially true when there
  is no draw range to remove. The model can learn the interaction
  with `villain_draw_pct = 0` cleanly: "when draw_pct is 0,
  draw_block_pct is also 0 and carries no information; ignore this
  split."
- NaN breaks XGBoost's missing-value handling semantics here: NaN
  would tell the model "this feature is missing / unknown," but
  the actual semantic is "this feature is known to be
  inapplicable." These are different. XGBoost would route NaN
  rows down a default branch that was learned from rows where the
  feature *was* applicable but unmeasured — wrong distribution.
- The combination `villain_draw_pct == 0 AND draw_block_pct == 0`
  is a clean signature of "draw-block signal is inapplicable" that
  tree splits can exploit. Prefer this to a sentinel.

---

## 8. Missing cases / additional concerns

1. **Pair-blocking interaction with made-hand blocking.** The
   feature targets draws only, which is correct scope for this
   plan. But the owner's "mid pair + one spade" scenario also
   blocks villain's *overpair* combos (JJ, if hero has a J) at
   low frequency. `nut_made_block_pct` (plan 3) is meant to cover
   this. Confirm plan 3 denominator includes made-hand classes
   that hero's pair-card blocks, otherwise a gap persists.
2. **River behavior.** On the river, draws are dead (per
   `extract_range_composition` line 1177-1179 which reclassifies
   river draws as air). `draw_block_pct` on river should be 0.0
   because the `_DRAWS` subcategory set is empty in villain's
   river range. Verify `_draw_block_pct` uses the same street-
   aware range narrowing `narrow_to_betting_range` produces, so
   river draw_block_pct is naturally 0.
3. **Multiway (3-way) specificity.** All KB reasoning above is
   3-way. In HU spots (if the pipeline ever extends to HU), the
   densification effect is weaker because bluff frequency is
   higher (KB §1.4: ~1:2 HU vs ~1:4 3-way). The feature is still
   directionally correct in HU but with smaller magnitude. No
   action needed for v2.4 (pipeline is 3-way-only per directive).
4. **Counter-example balance.** Per `feedback_counter_example_
   balance.md` (referenced in directive-x line 88): if/when
   counter-examples are generated to teach the defensive blocker
   signal, they must include BOTH directions (hero blocks a lot /
   hero blocks little on same board texture) to avoid
   single-direction overfitting. This is a training-set concern,
   not a feature-engineering concern, but flagging here because
   this feature's value is ZERO without paired counter-examples —
   the feature is what *lets* such counter-examples teach.

---

## 9. v3.2 prompt guidance — scope note only

Per plan §"Feature attention guidance (for v3.2 prompt)", the
intent is:

- PRIMARY for Medium-made / Weak-made + facing_bet=1
- CONFIRMED for Drawing / Air + bluff aggressor
- Default for Strong-made / Monster + facing_bet=0

**Scope note for v3.2 authoring (not this review's deliverable):**
the prompt must instruct panels to tag `draw_block_pct` (or the
split features if Q1 adopted) with **directional reasoning**: "Hero
blocks X% of villain's draw combos, which **densifies** villain's
bet range toward value — this is a FOLD-lean signal for marginal
made hands." The word "densifies" should appear in the KB §1.9 (new
subsection — the TICKET proposes §1.9 or extended §1.8). Panels
cannot use this feature correctly without the causal mechanism
being explicit in the KB. If Builder ships the feature before the
KB/prompt updates land, the training signal remains zero — the
feature exists but labels won't tag it. Sequencing: KB §1.9 first,
v3.2 prompt second, re-label of affected hands third, then retrain.
Feature can ship earlier (additive, no schema break).

---

## 10. Required modifications before code

1. **MUST: fix implementation contract.** `HandBucket.combos` does
   not exist. Reimplement per §6 Option 1 (inline combo iteration
   in `feature_extractor.py`, not via `range_breakdown.buckets`).
2. **MUST: decide Q1 (combined vs split).** My recommendation is
   SPLIT into `flush_draw_block_pct` and `straight_draw_block_pct`.
   If Builder disagrees, document the counter-reason and the v2.5
   path for adding the split later.
3. **SHOULD: gutshot treatment (§2).** Keep gutshot in the `_DRAWS`
   set for v2.4 to match `villain_draw_pct` scope, but document the
   dilution risk and defer "bet-frequency weighting" to v2.5.
4. **SHOULD: distribution audit scope.** Plan §"Validation plan"
   step 3 covers median check. Add: per-street breakdown (flop /
   turn / river), verify river `draw_block_pct` ≈ 0 everywhere
   (§8.2 missing case).

Items 1 and 2 are blocking. Items 3 and 4 are strong
recommendations the reviewer will re-audit if re-submitted.

---

## Summary (for orchestrator)

APPROVED_WITH_MODIFICATIONS. The feature is solver-grounded and
correctly targets the densification effect the v2.3.2 training
signal is missing. Two required fixes before code: (1) the pseudocode
accesses `HandBucket.combos` which does not exist — reimplement via
inline combo iteration in `feature_extractor.py`; (2) split the
feature into `flush_draw_block_pct` and `straight_draw_block_pct`
— the owner's scenario is flush-specific, combined metric creates
floor-ceiling artifacts across board textures, and XGBoost handles
sparse features cleanly. Gutshot inclusion is a documented dilution
risk (KB §1.7 says gutshots don't semi-bluff 3-way); acceptable for
v2.4, defer bet-frequency weighting to v2.5. Keep 0.0 default
(NOT NaN) for empty-draw-range spots — 0.0 has the correct
"inapplicable" semantic while NaN triggers XGBoost's missing-value
routing. Do NOT expose `effective_draw_block` product — XGBoost
learns the interaction via tree splits and adding the product
inflates SHAP attribution. Scope note: the feature produces zero
training signal until KB §1.9 + v3.2 prompt land, because panels
won't tag an undocumented feature — sequence is KB, prompt,
re-label, retrain. Feature can ship earlier (additive, no schema
break). Refs: KB §1.1 (3-way fold equity), §1.4 (3-way bluff:value),
§1.7 (semi-bluff conditions), §1.8 (blocker action selection),
DO NOT Rule 6 (blockers for action selection still critical
3-way).
