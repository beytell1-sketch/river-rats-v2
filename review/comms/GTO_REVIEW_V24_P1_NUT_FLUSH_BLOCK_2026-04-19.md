---
date: 2026-04-19
from: GTO Reviewer subagent
to: Builder / Main terminal / Owner
re: v2.4 P1 GTO review — `nut_flush_block` (feature 1 of 3)
status: APPROVED_WITH_MODIFICATIONS
reviews: BUILDER_V24_P1_PLAN_NUT_FLUSH_BLOCK_2026-04-19.md
---

# GTO Review — `nut_flush_block` (P1)

## Verdict

**APPROVED_WITH_MODIFICATIONS**

The feature is poker-correct in its core primitive, sits in the right
place in the feature set (orthogonal to `flush_block_pct`,
`flush_draw_rank`, `has_flush_draw`), and targets the single most
solver-validated blocker signal in the KB (§1.7, §1.8, Worked Example
9, DO NOT Rule #6). Ship, but with the modifications below — three
are required for poker correctness, one is strongly recommended.

## Required modifications (must land before code)

### M1 — Tighten the flop-two-tone trigger to preserve reachability

Plan defines a 2+ suited board as sufficient on the flop. That is
poker-correct for the semi-bluff-raise spot the feature is built to
capture (KB §1.7: "AsQs on KsJd5s" — the canonical trigger is a
two-tone flop, not a three-tone flop). **Keep the 2+ trigger on the
flop.** However, on turn and river the threshold must be 3+, not 2+,
because a two-tone turn or river with no flush yet has only one or
zero streets left to complete — the As no longer blocks a *completable*
nut flush in villain's turn/river *continuing* range in the way §1.7
describes.

Revise the boolean to:

```
flop:    nut_flush_block == 1 iff board has 2+ of a suit AND hero has A of that suit
turn:    nut_flush_block == 1 iff board has 3+ of a suit AND hero has A of that suit
         (a 2-tone turn with 1 street left is NOT a blocker-drives-action situation)
river:   nut_flush_block == 1 iff board has 3+ of a suit AND hero has A of that suit
         (no runner-runner possible; 2-tone river is never in scope)
```

This mirrors the "nut flush matters this street" intent in the plan
text but the current pseudocode applies the 2+ threshold to all three
streets, which over-triggers on turn/river and adds noise.

**Why this matters for the model:** on a 2-tone river, hero's As is
not blocking a flush combo — villain cannot have a flush. Labelling
the same bit `1` there as on a two-tone flop where AsQs is a
solver-raise collapses two distinct poker situations into one feature
value. Tree splits lose resolution.

### M2 — Gate on paired-board correctly (answer to open question 4)

On paired flush-possible boards (e.g., 7h7d5h, Qs7s7d), villain's
betting range shifts decisively toward trips / full-house combos;
flush-combo density inside villain's *continuing* range drops by
roughly the paired-board densification factor. The As blocker still
removes AsXs combos, but those combos are a smaller slice of villain's
bet-this-board range, so the action-selection signal weakens
substantially.

**Recommendation:** do NOT gate the feature to zero on paired boards
— the signal is still non-zero and the model can learn the
interaction from `is_paired`. But the plan should document that the
model is expected to down-weight `nut_flush_block` when `is_paired == 1`,
and the v3.2 prompt guidance (below) should tell the labelling panel
not to tag `nut_flush_block` as PRIMARY on paired boards.

This answers open question 4: **keep the feature 1 on paired boards,
but mark paired-board activation as SECONDARY not PRIMARY in the
prompt's feature-attention guidance.**

### M3 — Hero's-own-made-flush handling: current plan is correct, make it explicit in code

The plan's text says "hero has the nut flush already → feature = 0"
(correct — this is not a blocker situation, it is a made-hand
situation handled by `is_made_hand` / hand-category features). But
the pseudocode does not implement that carve-out. Add:

```python
# Exclusion: hero already has a made flush using this suit
hero_same_suit_count = sum(1 for c in hole_cards if c[1].lower() == fs)
board_same_suit_count = suit_counts[fs]
if hero_same_suit_count + board_same_suit_count >= 5:
    # Hero has a made flush in this suit — not a blocker spot
    continue   # don't set to 1 for this suit
```

This answers open question 3: **feature = 0 when hero already holds
the made flush. Correct in intent, currently missing in code.** The
plan's §1.7 worked example is explicitly about a *draw* with the
blocker, not a made flush; keeping the bit at 0 when hero is already
made preserves semantic cleanliness.

## Strongly recommended modification

### M4 — Do not add `near_nut_flush_block` (companion K-blocker)

Open question 2 asks whether a companion K-of-suit bit should exist.
**Recommendation: no, and `draw_block_pct` (P2) is the right home
for it.** Reasoning:

1. The solver evidence in §1.7 and §1.8 anchors specifically on the
   *nut* blocker. The Kc blocker on a three-club board is still a
   meaningful blocker but its action-swing magnitude (per GTO Wizard
   suit-isomorphism data in the KB narrative) is closer to the
   generic suit-holding effect than to the ace-specific effect.
2. Adding a second boolean for K increases feature count without a
   solver-verified categorical break. A continuous bluff-blocker
   signal (`draw_block_pct`) captures K, Q, and the long tail in one
   scalar — which is exactly the P2 scope.
3. Introducing `near_nut_flush_block` now would mean the Q-of-suit
   and J-of-suit cases have nowhere to live until P2, creating an
   unprincipled gap.

Keep P1 scoped to the ace. Let P2 carry the non-nut blockers as
continuous signal.

## Answers to the 4 open questions

### Q1 — "2+ on flop, becomes 3+ later" framing

**Partial agreement. Adopt M1's split: 2+ on flop, 3+ on turn and
river.** The plan's instinct to activate on the flop two-tone is
correct and is exactly the KB §1.7 / Worked Example 9 trigger. The
plan's instinct to carry 2+ through turn and river is wrong — on
turn a 2-tone board has one street left to complete and the solver
does not treat that as a nut-blocker-drives-action situation. On
river a 2-tone is impossible to complete. Reducing the threshold to
3+ on turn/river keeps the feature activated only where the KB
evidence supports it.

### Q2 — Companion `near_nut_flush_block` for K-of-suit?

**No. Defer to `draw_block_pct` in P2.** See M4. The solver evidence
cited in the KB is ace-specific; the K case is weaker and better
represented as one sample in a continuous bluff-blocker distribution.
Adding a second boolean without solver anchoring would be feature
bloat.

### Q3 — Hero's own flush: feature = 0?

**Yes, 0 is correct — but implement it explicitly (M3).** KB §1.7
and Worked Example 9 are about a *draw with a blocker* (AsQs on
KsJd5s — As is the draw's high card, not a made flush). When hero
has the made flush, `is_made_hand` + nut-flush signal through
existing features (e.g., `flush_draw_rank == 14` combined with
`has_flush_draw == 1` and board suit count) already captures hand
strength. `nut_flush_block` is a *draw-and-bluff-catcher* blocker
signal; firing it on a made hand confuses the semantic.

### Q4 — Paired-board gating

**Do not gate the feature to 0 (keep computation as-is). Instead,
mark paired-board activations as SECONDARY in v3.2 prompt
feature-attention guidance.** See M2. Hard-gating would lose the
non-zero signal; leaving `is_paired` as a separate feature lets the
tree model learn the interaction. What needs fixing is the
*labelling* signal, not the feature definition.

## Issues the plan missed

### I1 — Interaction with `flush_draw_rank == 14`

Plan notes `flush_draw_rank` "activates only when hero has a flush
draw" (currently only when hero holds 2+ cards of the suit). The new
`nut_flush_block == 1` with `flush_draw_rank == 0` is exactly the
"hero holds A-of-suit but has NO flush draw" case — the ticket's
defensive-blocker scenario. Confirm in backfill that this
combination is well-represented in the training data. If
`flush_draw_rank > 0` AND `nut_flush_block == 1` dominates the
population, the feature's defensive-blocker signal will be swamped
by the aggressor-side (AsXs) signal and the ticket's original gap
will persist.

**Concrete action for backfill audit (already in plan step 3):**
report the joint distribution:
```
nut_flush_block=1 & flush_draw_rank == 14  (hero has nut flush DRAW)
nut_flush_block=1 & flush_draw_rank == 0   (hero has As but no flush draw — DEFENSIVE)
nut_flush_block=0                           (everything else)
```
If the defensive bucket is < 2% of total training rows, flag for
synthetic augmentation before retraining.

### I2 — Position interaction not encoded (by design, but noteworthy)

§1.8 shows the ace-blocker swings raise frequency by 40+ points
*regardless* of position ("AT with diamond raises 65%, AT without
raises 21%" is OOP-dominant data). The boolean stays
position-agnostic — correct, since `is_ip` is its own feature and the
tree model should learn the interaction. No change needed. Flag for
awareness: training distribution should include both IP and OOP
activations or the model will spuriously correlate the boolean with
whichever position dominates the training set.

### I3 — "Blocker direction" from the original ticket is only partially addressed

The defensive-blocker ticket (2026-04-18) specifically identifies the
*non-nut* defensive blocker (hero has J♠ on a two-spade board) as
the densification case. `nut_flush_block` does not touch that case
directly — that is the *nut* blocker, which per KB §1.8 is
*call-lean* when defending (villain's bets are more bluff-weighted
when hero blocks the nuts). The original ticket's fold-lean case
(hero blocks villain's *draws*, making villain's bet more
value-weighted) is P2 territory (`draw_block_pct`). This is
consistent with the plan's sequencing — just confirm in the P1
approval note that P1 alone does NOT close the ticket; all three
features are needed.

## Scope note — v3.2 prompt `feature_attention` guidance

Not implementing here; flagging for the prompt-update work item.

Recommended guidance for v3.2 prompt when `nut_flush_block == 1`:

- **Action = BET or RAISE, hero aggressing, facing_bet in {0, 1}, 3-way:**
  tag `nut_flush_block` as PRIMARY. KB §1.7 and Worked Example 9 are
  the direct reference. This is the semi-bluff-raise case where the
  blocker is the action-selection driver.
- **Action = CALL, hero facing bet, `is_made_hand == 1`, villain bet
  sized consistently with value-heavy range:**
  tag `nut_flush_block` as CONFIRMED (not PRIMARY) with framing
  "blocks villain nut flush → villain's bet is bluffier → bluff-catch
  leans call." KB §1.8 role 1.
- **`is_paired == 1`:** downgrade tag from PRIMARY to SECONDARY
  regardless of action — paired board densification reduces
  flush-combo weight in villain's range (see M2).
- **Action = FOLD:** do NOT tag `nut_flush_block` as PRIMARY. If
  the panel is folding despite hero holding the nut-flush blocker,
  either equity/pot-odds dominate (tag those instead) or the panel
  is making an error the feature should help correct.
- **`has_flush_draw == 1 AND flush_draw_rank == 14`:** tag
  `nut_flush_block` as PRIMARY — this is the literal Worked Example 9
  hand.

## Ship conditions

Approved to code after:
1. M1 implemented (2+ on flop, 3+ on turn/river)
2. M2 documented (no code gate; prompt guidance reflects paired-board
   downgrade — scope note for P1, actual prompt change in v3.2 work)
3. M3 implemented (made-flush exclusion in the Python helper)
4. M4 confirmed (no `near_nut_flush_block` in P1 scope)
5. Backfill distribution audit reports the joint stratification in I1
   before training is triggered

Nothing here blocks writing the P2 (`draw_block_pct`) and P3
(`nut_made_block_pct`) plans in parallel — those can proceed now.

## Summary line

Poker-correct primitive targeted at the one blocker signal the KB
explicitly validates for action selection. Three required code/scope
adjustments (turn/river threshold, made-flush exclusion, no K
companion) keep the feature semantically clean. Paired-board case
stays in the feature but is handled via prompt-level attention
downgrade, not a code gate. Proceed to implementation once M1–M4 are
folded into the plan.
