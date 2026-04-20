---
date: 2026-04-20
from: GTO Reviewer (subagent)
to: Builder / Main terminal / Owner
re: GTO review of v2.4 Stage 2 KB addition — §1.10-§1.12 Defensive Blocker Direction
status: REVIEW COMPLETE
verdict: APPROVED_WITH_MODIFICATIONS
related: knowledge/three_way_gto.md §1.7, §1.8, §1.10-§1.12, Worked Example 9, DO NOT Rule #6; feedback_concentration_effect.md; GTO_REVIEW_V24_P1_NUT_FLUSH_BLOCK_2026-04-19.md, GTO_REVIEW_V24_P1_DRAW_BLOCK_PCT_2026-04-19.md, GTO_REVIEW_V24_P1_NUT_MADE_BLOCK_PCT_2026-04-19.md
---

# GTO Review — v2.4 Stage 2 KB Addition (§1.10 Defensive Blocker Direction)

## Verdict

**APPROVED_WITH_MODIFICATIONS**

The draft is poker-theoretically sound, correctly encodes the aggressor/defender
asymmetry the v2.3.2 β-panel regression exposed, and restores the covering-triple
framing agreed in the three P1 feature reviews. The densification-effect
mechanism is correctly stated and will ship to the labelling panel as intended.

Modifications below are scoped to (a) one directional edge-case on
`nut_flush_block`, (b) one example that understates the densification math,
(c) tightening the `nut_made_block_pct` aggressor-side claim so it does not
over-generalise, and (d) a cross-reference hygiene pass. None are architectural.

## Summary (orchestrator, <400 words)

§1.10 does what it needs to do. It names the exact failure mode (densification)
that flipped 7 of 9 β-panel hands, attaches it to a specific feature
(`flush_draw_block_pct`), gives the defender-side sign, and explicitly lists
this as the CALL-lean trap to avoid. The owner's Apr 18 J♠ example is
reproduced verbatim in §1.10.2 line 316-322 with the correct
equity-adjustment direction (0.38 → ~0.28 after densification). A labeller
reading this in production will not make the historic error. That is the
bar and it is met.

The aggressor-vs-defender asymmetry table at line 256-261 is correct for
all four features and matches the three feature-level GTO reviews already
signed off (NUT_FLUSH_BLOCK, DRAW_BLOCK_PCT, NUT_MADE_BLOCK_PCT). The
covering-triple articulation in §1.11 (lines 373-390) is clean and gives
the panel a three-step reasoning sequence: (1) THE block, (2) villain
semi-bluffs blocked, (3) villain value blocked. That is the right mental
model.

Required modifications:

1. **`nut_flush_block` defender direction is overstated as "positive."**
   On a 2-flush flop the feature is positive when villain's betting range
   is flush-draw-heavy (hero's Ah removes Ah-Xs *semi-bluffs*, densifying
   villain to value — this is the SAME densification as §1.10.2). The
   feature is positive for defense only on boards where villain's betting
   range is already *made-flush heavy* (turned/rivered 3-flush). The draft
   collapses this into "slight positive." Fix below.

2. **§1.10.2 example needs the pot-odds floor.** The hero 8♠9h example
   correctly adjusts equity 0.38 → 0.28, but does not state the required
   equity. At pot-sized bet, pot odds = 25%. 0.28 > 0.25 is still a call.
   The "Fold-lean" closing is directionally right but the worked math
   argues the opposite. Either raise the densification shift or reduce
   pot-odds by making it a 1.5x pot bet.

3. **§1.10.4 aggressor-side claim is too broad.** "Thin value blocked →
   negative" is correct for *combining* nut-made-block with a thin-value
   bet; it is NOT negative for a pure-bluff bet (no value hand to block).
   The NUT_MADE_BLOCK_PCT feature review (2026-04-19) already caveated
   this. Mirror that caveat here.

4. **Cross-reference hygiene.** Lines 160 and 447 still refer to the
   "45-feature pipeline." v2.4 ships 59 features (55→59). §1.10 correctly
   numbers new features 56-59. Leave those alone in this PR, but log
   a TODO on the two legacy mentions for a follow-up pass so the KB stops
   contradicting itself on pipeline size.

## Per-subsection review

### §1.10 intro (lines 231-254) — PASS

- Aggressor/defender framing clean. Correctly credits §1.7/§1.8 for
  aggressor-side coverage and positions §1.10 as the defender-side
  complement.
- Densification motivation explicit with the v2.3.2 β-panel reference.
- Feature table at lines 256-261 is directionally correct for all four
  rows as written, with one caveat on row 56 (see §1.10.1).

### §1.10.1 `nut_flush_block` (lines 263-288) — FLAG

**Aggressor direction: PASS.** Matches §1.7 and Worked Example 9. The
AsQs on Ks-Jd-5s raise is correctly cited as the canonical case.

**Defender direction: FLAG — too simple.** The draft says defender is
"slight positive (villain can't have nut flush)." That is correct ONLY on
textures where villain's betting range contains made nut flushes — i.e.
turn/river after a third flush card, or a rivered flush. On a 2-flush
flop, villain can't yet HAVE the nut flush; villain's Ah combos in the
betting range are *Ah-with-a-draw semi-bluffs*. Hero blocking Ah on a
flop **removes villain's semi-bluffs**, which is the SAME densification
mechanism §1.10.2 correctly flags as fold-lean. The draft's current
wording would incorrectly tell a panel that holding Ah on a 2-flush flop
facing a bet is a call-trigger.

**Concrete fix:** on line 282-284, change:

> `nut_flush_block == 1` + hero has bluff-catcher + facing bet →
>   slight CALL lean (villain can't have nut flush)

to:

> `nut_flush_block == 1` + hero has bluff-catcher + facing bet:
>   - **On made-flush boards (3+ of suit on board):** slight CALL lean
>     (villain's nut-flush combos are blocked, villain is relatively bluffier).
>   - **On 2-flush boards (flop only):** **negative for defense** — hero's
>     Ah blocks villain's Ah-Xs semi-bluff raises, densifying villain's
>     betting range toward value. Same mechanism as §1.10.2.

The example at lines 285-288 (AhTh on Kh-8h-3d facing flop bet) is a
2-flush flop, so it illustrates the aggressor raise case, not the defender
call case. Either move the example up to the aggressor bullet, or add a
second example for a 3-flush defender case (e.g., hero Ah-Kd on
Qh-8h-3h-2h river facing bet: `nut_flush_block = 1`, defender CALL-lean
because villain's nut-flush made combos are blocked).

### §1.10.2 `flush_draw_block_pct` (lines 290-322) — FLAG

**Mechanism explanation (lines 290-314): PASS.** Densification correctly
identified. Aggressor near-neutral / Defender negative is correct per the
2026-04-19 DRAW_BLOCK_PCT review. Owner's J♠ example at line 299-302
carried through verbatim — good.

**Example math (lines 316-322): FLAG — numerics under-argue the conclusion.**

The example: 8♠9h on Q♠8♥4♠, pot-sized bet, `equity_vs_range = 0.38`,
`flush_draw_block_pct = 0.52`, "equity after densification ~0.28."

Pot odds on a pot-sized bet = `to_call / (pot + 2·to_call)` = 100 / 300
= 33%. Hero's adjusted equity 0.28 < 0.33 is a correct fold. Good.

BUT the stated 0.38 → 0.28 drop is too large relative to the 0.52
block-pct. A rough sanity check: if villain's betting range is, say, 40%
value / 40% flush-draw / 20% other at baseline, blocking 52% of the
flush-draw slice pushes ratios to ~40% value / ~19% flush-draw / 20%
other (remainder rebalances), so value fraction of the *continuing*
betting range rises from ~40/80 = 50% to ~40/60 = 67% — maybe a 0.38 →
~0.32 equity shift, not 0.28. The qualitative direction is right; the
magnitude is aggressive.

**Concrete fix:** replace the numerics with something that holds up to a
labeller re-deriving them. Either:

(a) State the example at **1.5× pot** bet, where pot odds = 37.5% and
0.38 clearly calls before densification (trap), 0.32 clearly folds after
(correct). OR

(b) Use a higher block-pct (0.75 — hero holds both a spade and a
specific semi-bluff combo blocker) to justify the 0.38 → 0.28 drop. OR

(c) Soften to "closer to ~0.32" and restate: "fold-lean only if villain's
sizing implies ≥33% equity needed — check sizing before over-folding."

Option (a) is cleanest and matches the KB's existing style of giving
labellers an unambiguous pot-odds check.

### §1.10.3 `straight_draw_block_pct` (lines 324-343) — PASS

Mechanism mirrors §1.10.2. Aggressor near-neutral / Defender negative is
correct. Example (T♣7♣ on 9h-8s-5c) cleanly illustrates middle-card
blockers removing JT/T9 OESDs. 0.35 block-pct → "check/fold is correct,
not call despite 0.40 equity" is directionally correct and — unlike
§1.10.2 — does not commit to a specific adjusted-equity number, which is
honest given the uncertainty.

Minor nit: line 339 says "Hero T♣7♣" but the worked setup in line 342
says "weak bottom-pair made hand (7s)". Hero is T♣7♣ holding bottom pair
with the 7; the 7s reference is a typo (should be "7c" or "hero's 7").
Fix: line 342, change `(7s)` to `(pair of 7s)` for clarity.

### §1.10.4 `nut_made_block_pct` (lines 345-371) — FLAG

**Mechanism and directional interpretation: PASS** on defender side,
matches the 2026-04-19 NUT_MADE_BLOCK_PCT feature review verdict.

**Aggressor-side claim (lines 357-360): FLAG — too broad.**

> Aggressor (thin value bet, raise with medium-strong hand): high value
> is **negative**. Hero's thin-value target is reduced because villain's
> top calling hands are blocked

This is correct for THIN VALUE bets. It is **not** applicable to pure
bluff bets — a bluff has no value hand to block, so
`nut_made_block_pct` is near-neutral to mildly positive for aggressor
bluffs (blocking villain's stack-off range marginally improves fold
equity). The 2026-04-19 review flagged exactly this and the draft has
not picked up the fix.

**Concrete fix:** lines 357-360, change:

> Aggressor (thin value bet, raise with medium-strong hand): high value
> is **negative**. Hero's thin-value target is reduced because villain's
> top calling hands are blocked; villain calls less often with non-nut
> made hands.

to:

> Aggressor direction is **context-dependent**:
> - **Thin value bet / raise with medium-strong hand:** negative. Hero's
>   thin-value target is reduced; villain calls less often with non-nut
>   made hands.
> - **Pure bluff bet:** near-neutral to slightly positive. No value
>   target to block; blocking villain's stack-off combos marginally
>   raises fold equity.

**Example (lines 366-371): FLAG — poker inaccuracy.**

"Hero AcKs on Ks-Qs-7s-2h ... Hero's Ks + As (if held) would block
villain's nut-flush combos on the spade board. `nut_made_block_pct =
0.40` (if As held; 0.0 if not)."

Hero is **AcKs**, not AsKs. Hero does NOT hold the As in this setup. The
parenthetical "(if As held; 0.0 if not)" then says the feature is 0.0 for
the stated hero. This is confusing — the worked example is setting up a
counterfactual but presenting it as the active case. A labelling panel
will read this and be unsure whether the feature fires.

Also: Ks does NOT block nut-flush combos. Nut-flush on a spade board is
AsXs combos. Ks blocks second-nut (Ks-flush), which is only the
effective nut on a **monotone** board where no higher card of suit is in
hero's hand or already on board. The board here is Ks-Qs-7s-2h (3
spades on board, hero has Ks which IS on board — wait: hero has Ks and
the board also contains Ks — that's impossible, one Ks. So hero holds
the only Ks.)

Given the only Ks is in hero's hand, and hero does NOT hold As:
- Nut flush (As-flush) is NOT blocked by hero.
- Second-nut flush (Ks-flush) IS held by hero — villain cannot have it.

The effective-nut-flush qualifier from the NUT_MADE_BLOCK_PCT feature
spec (the "second-nut-when-A-of-suit-on-board" carve-out) does not apply
here because the As is NOT on the board. So the example is actually the
wrong case to illustrate `nut_made_block_pct` at all.

**Concrete fix:** replace lines 366-371 entirely with a clean example.
Suggested:

> **Example.** Hero AsKh on As-Ts-6s-2c (turn). Board is 3-flush; As is
> on board, making Ks-flush the **effective nut flush**. Villain's
> nut-made combos on this texture include set of tens, set of sixes,
> and Ks-flush. Hero does not hold Ks, so does not block Ks-flush. But
> replace with Hero AsKs on As-Ts-6s-2c: hero holds As (on board, so
> irrelevant for blocking) and Ks, which blocks Ks-flush combos from
> villain's range. `nut_made_block_pct ≈ 0.25` (Ks-flush is ~25% of
> villain's nut-made slice on this texture). Defender-side facing a
> river bet: villain's stack-off range is materially reduced, bluff-catch
> equity boosted. Calling with just top-pair-top-kicker becomes correct.

(Reviewer will defer exact block-pct number to the feature extractor
team, but the mechanism is unambiguous.)

### §1.11 Covering triple (lines 373-398) — PASS with one nit

The three-step reasoning sequence (THE block / semi-bluff blocks / value
blocks) is clean. `equity_vs_range` as baseline + blocker features as
directional correction is the right framing and matches the P1 plan.

Lines 392-398 correctly position `flush_block_pct` as legacy pending
Stage 5 retirement test. Language is appropriately cautious.

Nit: line 379 says "`nut_flush_block` ... says 'I have THE block'" —
given the §1.10.1 flag above, this should be qualified: "says 'I have
THE block' on a made-flush board; says 'I block villain's nut-flush
semi-bluffs' on a 2-flush flop." Since §1.11 is the summary, it is the
right place to telegraph that `nut_flush_block` has two mechanisms.

### §1.12 DO NOT Rule 6 update (lines 400-415) — PASS

Original Rule 6 (lines 1069-1075) intent preserved: blockers for bluff
SELECTION still matter less 3-way; blockers for ACTION selection still
matter. The expansion correctly maps each of the four new features to
the operative lean:

- FOLD signals: `flush_draw_block_pct`, `straight_draw_block_pct` (for
  defender with marginal made hand) — CORRECT, matches §1.10.2/.3.
- CALL signal: `nut_made_block_pct` — CORRECT, matches §1.10.4 defender.
- RAISE trigger: `nut_flush_block` — CORRECT per §1.7.
- Anti-signal: `flush_block_pct` as defensive CALL signal — CORRECT.
  This is the exact trap that caused the v2.3.2 β-panel regression.

Recommend a small addition: the Rule 6 body at line 1069 should get a
one-line forward-pointer ("See §1.12 for the expanded feature-level
decomposition"), so a labeller reading the DO NOT Rules in isolation is
routed to the new section.

## Example adequacy

| Example | Location | Clear? | Unambiguous? |
|---|---|---|---|
| AhTh / Th9h contrast | §1.10.1 (line 285-288) | Yes | Illustrates aggressor, not defender — misplaced. FIX per §1.10.1 flag. |
| 8♠9h on Q♠8♥4♠ | §1.10.2 (line 316-322) | Yes | Math is aggressive. FIX per §1.10.2 flag. |
| T♣7♣ on 9h-8s-5c | §1.10.3 (line 339-343) | Yes | Clean. Typo nit only. |
| AcKs on Ks-Qs-7s-2h | §1.10.4 (line 366-371) | No | Wrong suit attribution and conflates Ks-block with As-block. FIX per §1.10.4 flag (replace entirely). |

Three of four examples need work. None are fatal; all are fixable with
targeted edits.

## Missing cases the KB should cover

1. **Turn/river-specific blocker mechanics.** §1.10 treats block-pct as
   street-agnostic, but the densification effect operates differently
   on each street. On the flop, hero blocks semi-bluff candidates; on
   the turn with a third flush card, hero blocks made-flush combos.
   The KB should add a single sentence in §1.10 intro noting that the
   feature's direction flips streets in predictable ways and that the
   panel should read `board` alongside the feature.

2. **Combo draws (flush + straight simultaneously).** Neither
   `flush_draw_block_pct` nor `straight_draw_block_pct` alone covers
   combo draws on texture like 987 two-tone. The feature-level spec
   says combo_draw is counted in BOTH `flush_draw_block_pct` and
   `straight_draw_block_pct`, so a panel could double-count the
   densification effect. §1.11 should flag this to prevent additive
   over-application.

3. **Nothing says what happens when MULTIPLE block features fire for
   the same hand.** If hero defends with a hand that has
   `flush_draw_block_pct = 0.5` AND `nut_made_block_pct = 0.4`, the
   two pull in opposite directions. §1.11 says "use them together"
   but does not give a resolution rule. Suggest a one-paragraph addition
   to §1.11: "When defender-negative and defender-positive blocker
   signals co-fire, the primary driver is the *larger of the
   bluff-slice vs value-slice* in villain's betting range. If villain's
   range is >50% bluffs, `nut_made_block_pct` dominates (call lean).
   If villain's range is <30% bluffs, `flush_draw_block_pct` dominates
   (fold lean). In the middle zone, hold back — these are the
   genuinely close decisions where model mixed-strategy bias shows up."

## Poker-theoretic accuracy — overall

- Densification effect (§1.10.2, §1.10.3): **CORRECT.** Matches solver
  behavior. A bet by an opponent whose range composition has had the
  bluff-slice fractionally removed is, by conditional probability, a
  more value-weighted bet.
- Aggressor/defender asymmetry: **CORRECT** for 3 of 4 features as
  written; `nut_flush_block` defender direction needs the 2-flush vs
  3-flush split (§1.10.1 flag).
- Covering-triple framing (§1.11): **CORRECT.** This is the right
  conceptual structure for the panel to apply.
- Rule 6 expansion (§1.12): **CORRECT.** Preserves intent, adds the
  feature-level instruction map.

## Labelling pitfalls — specific checks

| Pitfall | Does KB guard against it? |
|---|---|
| Treating `flush_draw_block_pct` as defender CALL signal (historic β-panel error) | YES — §1.10.2 explicit, §1.12 Rule 6 bullet 3 explicit |
| Confusing `nut_flush_block` RAISE trigger with defender CALL trigger | PARTIAL — draft treats both as positive; FLAG on 2-flush boards where defender direction should be negative |
| Densification mechanism unclear for unseen hands | PASS — mechanism stated in plain terms, two workable examples (after fixes) |
| `nut_made_block_pct` direction flip aggressor vs defender | PASS on defender, FLAG on aggressor (too-broad "negative" claim) |

## Internal consistency

- §1.10 vs §1.7: Compatible. §1.10 explicitly positions as the
  defender-side complement; §1.7 remains the aggressor-side carve-out.
  The AsQs raise pattern is referenced correctly.
- §1.10 vs §1.8: Compatible. §1.8's raise-frequency swing claim
  (40-pp for suit holdings) is aggressor-side action selection; §1.10
  adds defender-side reasoning to the same family of features.
- §1.10 vs Worked Example 9: Consistent. Example 9 is aggressor. §1.10
  does not re-tread it; it adds the complementary case.
- §1.10 vs DO NOT Rule 6: Consistent. Rule 6 update at §1.12 is the
  operationalisation of the §1.10 direction table.
- §1.10 vs §1.9: No conflict. §1.9's postflop-composition-triple
  framing is orthogonal to §1.10's blocker-direction framing; both
  feed into the Factor 3 range composition reasoning.

## Action items for Builder

Before this KB section ships to the production labelling prompt:

1. **§1.10.1** — split defender direction by 2-flush vs 3-flush board.
   Move AhTh example to aggressor bullet or add a 3-flush defender
   example. (~8 lines added.)
2. **§1.10.2** — fix example math. Pick option (a), (b), or (c) from
   the flag above. (~3 line edit.)
3. **§1.10.3** — typo fix on line 342: `(7s)` → `(pair of 7s)` or
   similar disambiguation. (1-word edit.)
4. **§1.10.4** — (a) split aggressor direction into thin-value vs bluff
   cases (~4 lines added); (b) replace the AcKs example entirely with
   a clean nut-made-blocking example (~6-line rewrite).
5. **§1.11** — add multi-signal resolution rule (~1 paragraph added);
   add combo-draw double-counting caveat (~1 sentence added); qualify
   the `nut_flush_block` line 379 summary (~1 phrase added).
6. **§1.12** — optional forward-pointer in the original Rule 6 body at
   line 1069. (1-line edit.)
7. **Cross-ref hygiene** — log a follow-up TODO to fix "45-feature
   pipeline" references at lines 160 and 447 (outside Stage 2 scope;
   do NOT touch in this PR).

Estimated edit size: ~40 line changes total, all within §1.10-§1.12.
No changes required to §1.7, §1.8, Worked Example 9, or Rule 6 body.

## Final verdict

**APPROVED_WITH_MODIFICATIONS.** The section is doing the right work
and will — once the six fixes above land — give the labelling panel
the vocabulary it needs to avoid the v2.3.2 densification trap and to
correctly weigh the four new v2.4 blocker features. The mechanism is
explained, the directions are (mostly) right, and the covering-triple
framing will generalise to hands the panel has not seen before.

Return to Builder with the modification list above. No second-round
review needed after these are applied; spot-check only.

---
*GTO Reviewer (subagent), 2026-04-20*
