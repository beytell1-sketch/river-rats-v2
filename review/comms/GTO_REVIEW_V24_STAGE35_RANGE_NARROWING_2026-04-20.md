---
date: 2026-04-20
from: GTO Reviewer
to: Builder, Owner
re: Stage 3.5 range-narrowing refactor — poker-correctness review
status: APPROVED_WITH_MODIFICATIONS — Option A (with a tighter derivation), same-street NO (exclude), two non-trivial frequency-table flags, plus four risk mitigations owed before code lands.
reviewed:
  - BUILDER_V24_RANGE_NARROWING_EXPERT_REVIEW_2026-04-20.md
  - BUILDER_V24_RANGE_NARROWING_WALKTHROUGH_2026-04-20.md
  - BUILDER_V24_RANGE_NARROWING_ADDENDUM_PRIOR_REVIEWS_2026-04-20.md
  - river-rats-core/range_narrowing.py (frequency tables + narrow_to_betting/checking_range)
  - river-rats-core/feature_extractor.py (classify_villain_range gate, line ~1143)
  - prompts/gto_labeller_v3.1.md §1.3, §1.4, §1.7, §1.8
  - knowledge/three_way_gto.md §1.3, §1.4, §1.7, §1.8, §1.9, §1.10-§1.12
---

# Stage 3.5 — GTO Reviewer Verdict

## Verdict: APPROVED_WITH_MODIFICATIONS

The core thesis — that villain's current range is the **intersection of
per-street continue filters** rather than a single-street filter applied
to the raw preflop range — is poker-correct. The walkthrough's "SHOULD"
column is solver-aligned and the `narrow_by_action_history` chain is the
right shape. It ships subject to the five modifications below.

Changes required before code lands:
1. CALL-narrow: Option **A**, but with a tighter derivation than the
   spec proposes (details in Q1).
2. Same-street pre-hero actions: **NO** — exclude (details in Q2).
3. Update two RIVER frequency-table entries that currently bias the
   chain on value-heavy rivers (Flag A).
4. Add three safety-rails for the composition pipeline (Flag B:
   empty range, minimum total_weight, weight floor collision with the
   0.001 filter).
5. Decouple bet-size / facing-raise context from `CALL`-continue
   frequency at the spec level; ship a single uniform table for v2.4
   with a documented bias band (Flag C).

Scope call: Stage 3.5 as proposed is the correct placement — must land
before Stage 4 re-label.

---

## Question 1 — CALL-narrowing path

### Verdict: **Option A, but refined**

Option **B (pass-through)** is not poker-acceptable. A cold-called /
bet-and-called line on a prior street is one of the **strongest**
available narrowings — it removes both the "would raise" top of the
range AND the "would fold" bottom of the range. Passing it through as
a no-op systematically **overstates air and understates TP+** on
exactly the hands Stage 3.5 is being built to fix. Pass-through
reintroduces the MW-30-style error that §1.9 of `three_way_gto.md`
calls out by name: "Using preflop structural geometry as a postflop
strength proxy underestimates TP+ density in a cold-caller's actual
continuing range." The d2410 / d0182 / d8411 anchors are turn
decisions whose FLOP action was a villain **check** (not a call), so
they survive pass-through, but `H_8dfb6ef8` does not — it has a
villain FLOP-BET then TURN-CHECK then TURN-CALL then RIVER-BET, and
pass-through on the turn-call would leave hero composing a river range
from a post-turn-check range that still contains the pre-flop-bet
weights. Directionally wrong and empirically load-bearing.

Option **C (solver-derive)** is the right long-term answer but
correctly out of v2.4 scope per the builder's §4.1.C.

Option **A** is acceptable **if the heuristic is derived correctly.**

### Refinement: the spec's derivation is wrong

The builder proposes:
> `narrow_to_continuing_range(range) ≈ range minus hands that would
> fold AND minus hands that would raise`
> i.e. `call_freq ≈ 1 - fold_freq - raise_freq`

This is directionally right but the specific derivation is wrong in
two places:

**Wrong 1 — the check table does not give you fold_freq.** The
current code treats a street-CHECK and a street-FOLD as disjoint
categories. But the `*_CHECKING_FREQUENCIES` table is the prob that
villain would **CHECK** with a hand when given the option to
open-bet — that is not the same as "hands that would CALL a bet."
Villain's weak-made that checks 80% when first-to-act will FOLD most
of the time when faced with a bet, not CALL. Deriving call-continue
as `(1 - bet_freq - check_freq)` collapses check and call into the
same bucket and **massively overstates** the continuing range (since
check_freq is near-zero when facing a bet).

**Wrong 2 — the bet table does not give you raise_freq.** Villain's
first-in bet frequency is not the same as villain's raise-when-
facing-a-bet frequency. Nut and strong-value hands raise facing a
bet at much higher rates than they open-bet (because the pot is
larger, equity is realised, and value goes up). Using bet_freq as a
raise-freq proxy understates how much of the top of the range is
excised by "villain just called." That matters: a "call" is
informative precisely because villain had a raise option and did not
take it.

### Refined heuristic for `narrow_to_continuing_range`

Use a **per-category call-continue multiplier** directly, grounded in
solver intuition from §1.3-§1.4 and §1.7-§1.8. Recommended table for
v2.4 MVP (document as "heuristic, not solver-run"):

```python
# CALL-continue frequencies: fraction of each category that calls a
# standard-sized bet on that street, given villain had bet/fold/raise
# available. Derived from solver intuition (§1.3, §1.4, §1.8), not
# direct solver data. Polarisation increases through streets.
FLOP_CALL_FREQUENCIES = {
    'nuts':          0.15,  # mostly raises; only slow-plays call
    'strong_value':  0.35,  # mixes raise / call; more call on wet
    'good_value':    0.75,  # TPTK/overpair-type calls standardly
    'draw':          0.70,  # calls with pot odds + implied odds
    'medium_made':   0.55,  # calls with showdown; floats some
    'weak_made':     0.30,  # calls small bets, folds big
    'bluff':         0.15,  # rare float with blockers
    'air':           0.05,  # overwhelmingly folds
}
TURN_CALL_FREQUENCIES = {
    'nuts':          0.15,
    'strong_value':  0.30,  # raises more as pot grows
    'good_value':    0.70,  # TPTK continues
    'draw':          0.55,  # pot odds tighter; some give up
    'medium_made':   0.50,  # bluff-catcher band
    'weak_made':     0.15,  # mostly folds by turn
    'bluff':         0.10,
    'air':           0.03,
}
RIVER_CALL_FREQUENCIES = {
    'nuts':          0.20,  # mostly raises
    'strong_value':  0.40,  # thin raise vs polarised bet
    'good_value':    0.65,  # standard bluff-catch
    'draw':          0.00,  # missed = air; already handled
    'medium_made':   0.55,  # primary bluff-catch band
    'weak_made':     0.20,  # folds most
    'bluff':         0.05,
    'air':           0.02,
}
```

These numbers are NOT claimed to be solver-exact. They are defensible
approximations for v2.4 with two poker properties the spec's derived
formula does not have:

1. `medium_made` stays **elevated** in the CALL-continue range at
   each street — this is exactly the "showdown value / bluff-catch"
   category and it MUST survive a call. The spec's derived formula
   (using `1 - check_freq` for medium_made flop would give
   `1 - 0.55 = 0.45`, roughly OK) accidentally lands near these
   numbers for medium_made specifically but for wrong reasons.
2. `nuts` / `strong_value` get **suppressed** in the CALL-continue
   range (since they would usually raise) — the spec's derived
   formula doesn't capture this because bet_freq is not raise-vs-bet
   freq.

Either ship the table above, or ship the builder's simpler
`1 - fold_freq - raise_freq` formula but **source fold_freq and
raise_freq from dedicated tables, not by aliasing the existing
bet/check tables.** The alias is the actual bug risk.

### Anchor domination

On the three target anchors (d2410, d0182, d8411 — all TPTK turn
decisions where villain **checked the flop**, not called), the CALL
path is **not** on the chain. The chain for these is just:
preflop ∩ flop-CHECK ∩ (no turn action yet because hero is deciding
the turn). **Option A vs B vs C makes zero difference on the three
target anchors** — the CALL-continue question is orthogonal to
whether d2410 restores to BET. That outcome is driven by the
flop-CHECK filter entering the chain, not by the CALL filter. (The
addendum makes this same point in §Category 1.)

Where A vs B matters empirically is `H_8dfb6ef8` (turn-CALL in the
chain) and the ~550 remaining multi-street training rows.

---

## Question 2 — Same-street pre-hero action chaining

### Verdict: **NO — exclude same-street pre-hero actions**

Poker rationale (not just the pragmatic control-anchor argument):

**A. Villain's same-street check carries almost no orthogonal
information at the flop.** On a decision where hero is IP and
villains checked to hero on the flop, the primary signal ("nobody
led") is already encoded in the feature vector elsewhere: `facing_bet
= 0`, plus any checked-to feature if the pipeline has one. Applying
`narrow_to_checking_range` on top of that reads the same signal
twice — the composition shift you'd get is double-counting the check
because the downstream consumer (hero's decision) already knows it's
a check-to situation via `facing_bet`.

**B. Flop checks-to-IP are weakly informative on range, strongly
informative on strategy.** In a multiway flop, §1.3 gives villain a
~57% overall check frequency (vs ~46% HU). When flop-check frequency
is that high, the check is close to uninformative about villain's
category distribution — every category checks substantial fractions
of the time. The solver-correct read is "villains are capped-ish on
any sufficiently-dry board" — which is a **position-level** statement
already handled by `get_villain_range` and by the uncapped-vs-capped
features in the vector. Re-applying `narrow_to_checking_range` to
shift categories at the 5-10% range is noise, not signal.

**C. "Historical" should mean "prior decision point."** The chain's
mental model is: villain made a decision, observed the result, then
made another decision. A same-street pre-hero check is villain's
first decision on the street; hero's decision follows without an
intervening villain decision on a new decision point. The chain's
intersection logic is about composing decision points, not about
stacking filters within a single street's decision.

**D. Turn check-through (the motivating case) is correctly captured
under NO.** On a river decision after check-through turn, villain's
turn-check is a **prior-street** action (turn ended with a pass-
through, river begins with villain's new decision). That is in the
chain under the NO rule. The owner's motivating scenario is fixed
either way.

**E. Flop-calibration-anchor preservation is a real constraint.**
The addendum §Category 2 identifies that 4 of 5 anchors (A4d, T5h,
AA, KQ flops) are checked-to-IP flops. Under YES, `narrow_by_action_
history` fires on those anchors and shifts feature values. Under NO,
they stay as ZERO-impact controls. Losing the 4 flop controls means
you cannot cleanly distinguish "Stage 3.5 fixed d2410" from "Stage
3.5 also moved unrelated flop anchors." That is diagnostic loss,
not just convenience.

### Expected impact on the 4 flop anchors under NO

Unchanged. Feature values identical to pre-Stage-3.5. They remain
clean controls; any regression on A4d/T5h/AA/KQ after Stage 3.5
indicates a bug in the chain implementation unrelated to poker
theory, and builder should STOP.

### Under YES (rejected path), what would change

- A4d / Qs5s7s: `narrow_to_checking_range(flop)` on the preflop
  range. Medium-made density rises (CHECKING_FREQUENCIES['medium_
  made'] = 0.55 at flop → medium hands retained at 55% of original
  weight vs 45% for bet). TP+ density drops because
  `good_value` checks at 30% while `medium_made` checks at 55%. Net:
  villain looks "softer" than today. This directionally flips in the
  wrong direction on A-high dry boards where solver theory
  specifically calls out that checked-to-IP villains are weighted
  toward air and weak-made — the chain would overstate medium_made.
- T5h / JJ2, AA / 7h5d2c, KQ / KsTs3h: similar direction. Not
  catastrophic but definitely not "zero impact."

This is additional evidence for NO.

---

## Additional Concerns / Flags

### Flag A — Two RIVER frequency entries are stale; update BEFORE Stage 3.5

The current tables were written for a single-street filter applied
to the raw preflop range. When the chain is composed, two entries
compound in a way the original tables did not anticipate:

**A.1 `RIVER_BETTING_FREQUENCIES['bluff'] = 0.35`.** This value
reflects HU river bluff frequency. §1.4 of both the prompt and
`three_way_gto.md` explicitly flag the 3-way river ratio as
`~1:4 or tighter` — i.e. ~20% bluffs, not 33%. In the current
single-street world the over-broad preflop starting set masked this.
Post-Stage-3.5, the river-bet filter runs on an already-narrowed
range, and over-stating bluff density will **directly inflate air
and underestimate TP+** on river decisions in 3-way hands. Update:

```python
# v2.4 Stage 3.5: tightened for multiway application
RIVER_BETTING_FREQUENCIES['bluff'] = 0.20  # was 0.35
```

Add inline doc: "3-way-aware; will run over post-chain ranges where
preflop structural geometry has already been filtered."

**A.2 `RIVER_BETTING_FREQUENCIES['air'] = 0.20`.** Same problem —
§1.4 + §1.7 say pure bluffs are "nearly eliminated" 3-way. 20%
air-betting on the river is HU-correct but over-states 3-way. Soft
update recommended:

```python
RIVER_BETTING_FREQUENCIES['air'] = 0.10  # was 0.20
```

Tighter bluff/air on river cascades correctly: the narrower bluff
class raises the TP+ fraction, which is exactly the signal the model
needs to see on value-heavy rivers.

**A.3 No change recommended to FLOP or TURN entries.** Those numbers
are solver-consistent with §1.3 HU figures and the composition chain
doesn't compound errors on those streets the way it does on the
river.

### Flag B — Three composition-pipeline safety rails

The chain as spec'd has three failure modes the builder should
test for and guard against:

**B.1 Empty range.** Two paths to empty: (i) villain action is FOLD
(correctly returns `{}`); (ii) chain of filters drives every hand's
weight below the `> 0.001` floor in `narrow_to_betting_range`. Path
(ii) is new: three-street chain (flop-bet × turn-bet × river-bet) on
a `medium_made` hand = 0.45 × 0.30 × 0.08 = 0.0108 of original,
still above 0.001 — survives. But `air`: 0.20 × 0.15 × 0.20 = 0.006,
barely survives. `weak_made`: 0.35 × 0.20 × 0.05 = 0.0035, survives.
In a 4-action chain like `H_8dfb6ef8` (flop-bet × turn-check ×
turn-call × river-bet), the compound for `weak_made` is
0.35 × 0.80 × 0.30 × 0.05 = 0.0042 which survives, but any hand
weighted < 1.0 in the preflop range can be filtered out. Guard:
after each `narrow_*` call in the chain, if `total_weight == 0`,
return the previous step's range with a logged warning — do NOT
return `{}` to `classify_villain_range` (which would produce
all-zero composition features and silently look like a bug).

**B.2 Weight floor collision.** The existing
`narrow_to_betting_range` filters hands at `new_freq > 0.001`. When
three or four narrowings compound, a hand with initial weight 0.5
(e.g. a frequency-weighted combo in a mixed range) times a product
of 0.5 × 0.5 × 0.1 ≈ 0.025 is fine, but 0.5 × 0.3 × 0.08 = 0.012 is
close. Recommendation: the chain should track a **minimum total
weight threshold** (say 5% of original range total) and if the
chain drops below it, either short-circuit with a warning or reset
to the last valid intermediate.

**B.3 Normalisation cascade.** Each `narrow_to_*` call re-normalises
to probability-sum-1. When chained, the normalisation in step N+1
hides how much absolute weight was stripped in step N. This means
`villain_air_pct` post-chain is "fraction of surviving range that is
air," not "fraction of original range that is air." Downstream
consumers (blocker features, board_favour) that interpret the
composition as a prior may want either representation — verify
current consumers are OK with normalised fractions or expose the
surviving-weight total as a separate `_villain_range_surviving_
weight` metadata field.

### Flag C — Decouple CALL-continue from bet-sizing at the spec level

The builder notes in §4.2 that "if villain CALLED hero's raise, vs.
CALLED hero's initial bet, those are different ranges." This is
correct but the proposed fix — a second check on the preceding
action — adds complexity without much v2.4 payoff. Recommended
simplification:

- v2.4: ship ONE call-continue table per street, applied uniformly
  regardless of facing-bet vs facing-raise. Document bias band
  (raise-calls will be over-wide by ~30% of range; bet-calls will
  be approximately correct).
- v2.5+: if playtest shows the bias materially affects decisions,
  add raise-aware variants.

This is what the builder recommended in §4.2 and I concur.

### Flag D — `H_8dfb6ef8` chain composition correctness check

The builder's hand exercises `bet → check → call → bet` across
flop-turn-river. Walking through on the proposed chain:

1. Flop: BB bet → `narrow_to_betting_range(preflop, flop, 'flop')`.
   `good_value` retained at 0.70 of preflop weight.
2. Turn: BB check → `narrow_to_checking_range(step_1, turn,
   'turn')`. `good_value` retained at 0.40 of step 1, so 0.28 of
   preflop.
3. Turn: BB call → `narrow_to_continuing_range(step_2, turn,
   'turn')`. Using refined table: `good_value` retained at 0.70,
   so 0.196 of preflop.
4. River: BB bet → `narrow_to_betting_range(step_3, river,
   'river')`. `good_value` retained at 0.55, so 0.108 of preflop.

Compound weight for `good_value` across the chain: 10.8% of its
preflop presence survives to the river-bet range. For `medium_
made` same chain: 0.45 × 0.70 × 0.50 × 0.08 = 0.0126 (1.3%
surviving). That's the correct solver intuition: villain who bet-
check-called-bet on a bet-check-call-bet line is value-heavy on
the river, bluff-light, medium-made almost extinct. Chain composes
correctly and does NOT double-count coverage. **PASS.**

The one edge: `narrow_to_betting_range` on step 1 and step 4 uses
the same bet table. That's correct because the **street** is
different (flop vs river) so the correct frequencies are selected
per-street. The compound is multiplicative over independent
per-street decisions, which is the right mental model.

### Flag E — d2410 expected direction

**Expected: BET confidence UP after Stage 3.5** (with Option A
refined table + NO on same-street).

Reasoning. d2410 is TPGK (JcKs) on Jd-9d-3h turn after a flop
check. Stage 3.5 adds `narrow_to_checking_range(preflop, flop,
'flop')` to the chain before the turn decision (which has
`facing_bet = 1` and therefore also applies turn-bet narrowing).

Effect on villain's turn-betting range:
- **Before Stage 3.5**: villain turn-bet range computed from raw
  preflop BB-defend range. `TURN_BETTING_FREQUENCIES` strips
  mediums to 30% and strong_value to 80%. TP+ density is inflated
  because the preflop range still contains premium pockets that
  would have bet the flop (AA, KK, QQ-type hands).
- **After Stage 3.5**: the flop-CHECK filter drops those premium
  pockets first (`FLOP_CHECKING_FREQUENCIES['strong_value'] = 0.25`,
  `'nuts' = 0.15`). The post-check range is **condensed, capped**
  (§1.3 language). Applying the turn-bet filter to a capped range
  gives higher medium-made / bluff density and lower TP+ density.
  Villain's turn-bet range now looks like "hands that checked flop
  and are now betting turn" — the natural read is "polarised toward
  draws-that-improved + mediums turning into value + some air."
- Net: hero's TPGK is now ahead of a larger fraction of villain's
  actual turn-betting range. Value-bet EV goes up. **Model should
  restore BET.**

This is the load-bearing expectation. If the model does NOT flip
back to BET after Stage 3.5, the diagnosis is **not** feature
correctness — it is Stage 4 re-label (training data class balance)
per the addendum's alternative-path language.

### Flag F — Risk unknowns / catastrophic failure modes

The builder should test for:

1. **Range collapsing to empty** after a deep chain (4+ actions).
   Failure mode: `narrow_to_continuing_range` on an already-narrow
   range produces `{}`. Test: construct a synthetic hand with
   `flop-bet-turn-bet-turn-call-river-bet-river-raise` (5 filters)
   and verify non-empty output.
2. **NaN weights.** If the normaliser sees `total_weight == 0` it
   divides by zero. Current code has `if total_weight > 0` guard
   which is correct; the chain must not bypass that guard.
3. **Compute cost explosion.** Builder estimates 3x (60ms), which
   is fine. But `classify_hand` is O(N_hands_in_range). If the
   preflop range has 200 combos and chain runs 4 steps, you do
   800 classifications per decision. For the ~700-row training
   regen this is ~560k classifications — minutes, not hours, but
   not trivial. Consider caching classification-per-board-per-hand
   within a single extraction run.
4. **Action-history schema mismatch.** Builder assumes every action
   entry has `{'street', 'position', 'action'}`. If any hand
   source uses `'pos'` vs `'position'`, the loop silently skips
   every action. Add an assertion on the first action entry's
   schema inside `narrow_by_action_history`.

---

## What would change my mind

- **Reject Option A and go to B**: If playtest reveals the heuristic
  CALL table above is materially biasing composition on >10% of
  hands vs a solver ground truth. No such evidence today.
- **Accept same-street inclusion (YES)**: If the 4 flop calibration
  anchors are deliberately retired as controls AND the sweep
  regenerates with new anchors pre-Stage-3.5. Not recommended for
  v2.4 — retain control discipline.
- **Defer the frequency-table updates (Flag A)**: If empirical
  retro-audit on the 700-row regen shows river composition shifts
  are within tolerance (say ±3pp on bluff density). Recommend
  running the audit BEFORE deciding.

---

## Recommendations before builder starts coding

In priority order:

1. **Lock the CALL-continue table.** Either adopt the refined per-
   category table in Q1 or explicitly commit to the `1 - fold -
   raise` formula with dedicated fold/raise tables (not alias of
   bet/check). My preference: ship the refined table. Document
   "heuristic, v2.4 MVP" in code comment + KB §1.3 footnote.
2. **Update RIVER_BETTING_FREQUENCIES bluff (0.35→0.20) and air
   (0.20→0.10).** Add inline doc tagging 3-way-aware.
3. **Lock same-street scope: NO.** `narrow_by_action_history` only
   chains actions from streets STRICTLY PRIOR to the decision
   street. On-street pre-hero actions enter a future extension.
   Add unit test asserting flop-only decisions with villains-
   checked-to-hero return identical composition to pre-Stage-3.5.
4. **Add the three safety rails from Flag B** (empty-chain
   fallback, weight-floor threshold, surviving-weight metadata).
5. **Extend the unit-test plan in §5 Part 5 item 5.** Must include:
   - `H_8dfb6ef8` chain (bet-check-call-bet) as canonical test.
   - Turn-check-through → river-bet (owner's scenario, clean).
   - Flop-check → turn-decision (d2410 shape).
   - Deep chain (4+ actions) for empty-range guard.
   - Schema-mismatch guard (wrong key in action entry).
6. **Retroactive audit on ~700 training rows**: before Stage 4
   trains, produce a distribution-shift report on the 10 villain-
   composition features. Acceptable shift: any direction on hands
   with multi-street action; near-zero on flop-only hands.
7. **d2410 / d0182 / d8411 model re-inference, pre-retrain.** Run
   the v2.3.1 model with the new feature values. Expected: BET
   restored on d2410. If BET restored → Stage 3.5 alone fixed it,
   Stage 4 re-label is additive insurance. If still CHECK →
   diagnose whether Stage 4 will close the gap (class imbalance)
   or whether we need to escalate.

---

## Summary

The refactor is poker-correct in its core mechanism. The three
non-trivial changes before code lands are: (1) use a direct per-
category CALL-continue table, not an alias of bet/check tables;
(2) exclude same-street pre-hero actions from the chain to preserve
the 4 flop anchors as clean controls and avoid double-counting
the check signal; (3) update two river bluff/air entries that were
written for HU-single-street application and will bias the chained
range. With those three plus the safety rails, Stage 3.5 is APPROVED
to proceed to implementation. Dispatch Gauntlet after code + audit +
d2410 re-inference land; my verdict on the implementation is
contingent on those artefacts.
