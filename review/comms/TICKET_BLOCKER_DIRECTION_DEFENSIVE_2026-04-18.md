---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: TICKET — blocker-direction gap on defensive holdings (KB + prompt + feature)
status: FILED — scope v2.4 (not a v2.3.2 blocker)
related_directive: Owner-flagged during v2.3.2 retrain
---

# TICKET — Blocker Direction on Defensive Holdings

## Summary

The v3.1 labelling prompt, knowledge base, and resulting training
data treat blockers as a uniformly positive signal ("I have the
blocker"), framed almost entirely around aggressor-side usage
(semi-bluff RAISE with nut-flush blocker per KB §1.7-1.8).

**What's missing:** the defensive case where hero holds a
non-nut blocker to villain's draw range. When hero is bet into
with a marginal made hand + one suit card (e.g., middle pair
holding J♠ on a two-spade board):

- The J♠ **removes** villain's flush-draw combos from range
- Given villain bet, villain's betting range is now **more
  weighted to value** (fewer semi-bluffs remain in the range)
- Hero's middle-pair equity vs villain's betting range **drops**
- The blocker is a **fold-lean** signal, not a call-lean signal

This is a standard solver result (densification / unblocker
effect) absent from the pipeline.

## Empirical evidence — labels don't capture it

Scanned all 470 Pass 1 labels for `flush_block_pct` in
`feature_attention`:

- PRIMARY attention: **0 hands**
- CONFIRMED attention: **1 hand** (a CHECK action, not a
  defensive CALL/FOLD)
- Defensive contexts (CALL/FOLD facing bet) tagging
  `flush_block_pct`: **0 hands**

Experts don't surface this feature in their reasoning because
the prompt doesn't prompt them to. The training signal on
blocker direction — especially defensive direction — is
effectively absent from the v2.2 base, Phase 4, pilot, and
both v2.3.x counter-example sets.

## Root cause — three structural gaps

### 1. KB gap

v1.2 of `knowledge/three_way_gto.md` covers blockers in three
places:

| Reference | Scope | Covers defensive blocker? |
|---|---|---|
| KB §1.7 | Nut-draw semi-bluff RAISE | No — hero as aggressor |
| KB §1.8 | Blocker action selection ("RAISE vs CALL with strong draw/made hand") | No — aggressor-side framing |
| DO NOT Rule 6 | "Overweight blockers" 40%-less-multiway warning | No — generic caveat |

No section covers: "when defending with a marginal made hand
against a bet, your non-nut blocker to villain's draw range
is a **fold-lean** signal because it removes villain's
semi-bluffs from range."

### 2. Prompt gap

`prompts/gto_labeller_v3.1.md` line 402 mandates `flush_block_pct`
as a feature-attention tag ONLY for the DRAWING bucket. Made-hand
buckets (strong_made, medium_made, weak_made) have no mandatory
blocker-attention requirement — so defensive bluff-catching
decisions with partial blockers never tag the feature.

### 3. Feature granularity gap

`flush_block_pct` is a single scalar — "% of villain's flush
range hero blocks" — that conflates:

- "Hero blocks nut flush" (good when aggressing; neutral when
  defending)
- "Hero blocks non-nut flush draws" (mildly good when
  aggressing; **bad when defending** — the user's scenario)

The model cannot learn directional effects from a feature that
collapses both into one number. Even if panels tagged it
correctly, the feature's information content is too coarse.

## Proposed fix — three-layer

### Layer A — KB update
Add section (e.g. §1.9 or extend §1.8) titled *"Blocker direction
on defensive holdings"*. Content:

```
When hero is facing a bet with a marginal made hand and holds a
non-nut blocker to villain's draw range, the blocker works AGAINST
hero:

  - Villain's pre-bet range had some flush-draw semi-bluff combos
  - Hero's blocker removes those combos from the range
  - Given villain bet, villain's betting range is now MORE weighted
    to value (the bluff portion shrank relative to value)
  - Hero's bluff-catching equity is LOWER than equity_vs_range
    suggests

This is the densification / unblocker effect. Rule:
  - NON-NUT blocker + DEFENDING (facing bet) with MARGINAL made hand
    → FOLD-LEAN signal
  - NUT blocker + DEFENDING with bluff-catcher → CALL-LEAN (villain
    bets are bluffier because nut value combos are blocked)
```

Add worked example: "Jc9c on Ks8s4d, villain bets. Hero has second
pair + J♠? No — hero has no spade. Re-work: hero JsTs on Ks8s4d
(no pair, gutshot, one spade). Actually the cleanest illustration:
hero 8h9h on Ks8s4d (middle pair, no spade) vs hero 8h9s on same
board (middle pair, one spade). Compare equities vs villain's
checked-to-hero range → hero's equity is higher with NO spade
because villain's betting range contains more bluffs."

### Layer B — Prompt update
In the v3.1/v3.2 prompt's "Reasoning Protocol" Step 2 (READ THE
SITUATION) and the action-dependent feature-attention defaults:

- Add a bucket-specific tag for Medium-made and Weak-made
  buckets when `has_flush_draw == 0` AND hero has at least one
  card of a board-flush-suit AND villain has bet: tag
  `flush_block_pct` as PRIMARY with defensive direction.
- Add guidance in the bucket-first protocol that "on wet
  boards with partial blocker holdings, consider villain's
  range densification before tagging call."

### Layer C — Feature split (optional; v2.4 assessment)

Split `flush_block_pct` into:
- `nut_flush_block_pct` — hero blocks villain's A-high flush combos
  (computable from `flush_draw_rank == 14` AND suit on board)
- `partial_flush_block_pct` — hero blocks non-nut flush combos

OR add a derived signal:
- `blocks_villain_bluffs` — indicator that hero's holdings
  specifically remove villain's semi-bluff class

Layer C requires `feature_extractor.py` change + re-extraction
of all training rows + schema bump.

## Repro / user-observed scenario

Owner described:

> "Villain bets, we have mid pair, two spades on the board and we
> hold one — lets say a jack vs the cut off. Now we block the flush.
> Actually the blocker makes it more likely he is betting with a
> made hand — as we block the flush, weakening our mid pair."

Correct. Modern solver output for this class (e.g., 87 on Ks8s4d
vs 8♠7♠ on same board) shows raise/call frequencies shifting
substantially based on whether hero holds a spade. The pipeline
currently has no way to represent this.

## Scope + sequencing

Per owner: **v2.4 scope, not a v2.3.2 blocker.** Recommended
sequence when picked up:

1. **Audit existing labels** for hands where hero has partial
   flush blocker + faces bet + is middle-or-weak made → estimate
   how many labels should arguably flip CALL→FOLD (or LOW-conf
   CALL → HIGH-conf FOLD) under the corrected framing.
2. **KB + prompt update** (Layer A + B) — low-cost,
   immediately improves panel reasoning for future labelling.
3. **Re-label audit-flagged hands** with v3.2 prompt
   incorporating defensive-blocker guidance.
4. **Feature split** (Layer C) — assess cost/benefit after A+B.
   If A+B alone produce enough directional signal via
   feature_attention, skip C. If the model still can't learn
   the pattern, add C.
5. **Retrain + re-evaluate** all gate tiers.

## Not blocking v2.3.2

Reasons this doesn't hold v2.3.2 ship:

- The Path C retrain is already scoped to the air-CHECK / value-BET
  rebalance. This is a different scope (defensive blockers).
- v2.3.2's standard-gate regression (FB-40 70%, MW-50 78%) is a
  separate investigation — unlikely to be caused by this gap since
  the flagged hands in FB-40/MW-50 are mostly not blocker-partial
  defensive spots (can verify with per-hand diff if reviewer wants).
- Teaching terminal's coherence guards handle output-level
  misframing independently.

## Cross-ref

- Labelling prompt: `prompts/gto_labeller_v3.1.md` — feature 46
  `flush_block_pct`
- KB: `knowledge/three_way_gto.md` §1.7, §1.8, DO NOT Rule 6
- Feature source: `river-rats-core/feature_extractor.py`
  (`flush_block_pct` derivation)
- Related ticket: `TICKET_HAND_EVALUATOR_DRAW_SEMANTICS_2026-04-18.md`
  (similar shape — KB/feature gap, v2.3.2/v2.4 scope)

## Action requested

Log this ticket. No immediate action — will revisit in v2.4
scope, likely alongside HU counter-example work and the
`hand_evaluator` straight-draw fix.
