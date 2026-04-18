---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.2 labelling complete — RED-FLAG tripped (4 CHECK > 3 threshold)
status: CHECKPOINT — surface before retraining; reviewer scope decision needed
---

# v2.3.2 Labelling Results — Red-Flag Checkpoint

Per directive-o red-flag protocol: ">3 of 40 labelled CHECK/CALL →
surface." **4 CHECK labels came back. Stopping to report before
retraining.**

## Dispatch configuration

- Prompt: `prompts/gto_labeller_v3.1.md` (same as v2.3.1)
- Input: `training-data/v23_2_value_bet_3way_for_labelling.jsonl`
  (39 rows: 2 litmus + 37 generated)
- Batches: 4 parallel subagents (10, 10, 10, 9)
- Workspace: `review/label_batches_value_bet/`
- Output: `training-data/v23_2_value_bet_3way_labelled.jsonl`

## Results

```
Total:         39 / 39
BET:           35 (89.7%)
CHECK:          4 (10.3%)   ← red-flag: >3 threshold tripped
CALL:           0
RAISE:          0
FOLD:           0

Confidence:   33 HIGH / 6 MEDIUM
Difficulty:   24 clear (1) / 15 standard (2) / 0 boundary (3)
```

### Litmus seeds — BOTH BET ✓

```
LITMUS_AA_7h5d2c_turn:   action=BET  conf=HIGH  diff=1
LITMUS_KQ_KsTs3h_turn:   action=BET  conf=HIGH  diff=2
```

The target class is protected: AA on dry overpair-value board and
KQ on TPGK two-tone board both BET on poker merits (v3.1 bucket-
first protocol).

## The 4 CHECK labels — all on ONE texture class

Every CHECK is `AhAd on Qs5s7s2h` (monotone spades, hero no spade
blocker) varied only by position/archetype:

| ID | Hero | Board | Pos | Villains |
|---|---|---|---|---|
| VALUE_BET_3WAY_011 | AhAd | Qs5s7s2h | BTN | HJ, BB |
| VALUE_BET_3WAY_012 | AhAd | Qs5s7s2h | CO  | SB, BB |
| VALUE_BET_3WAY_013 | AhAd | Qs5s7s2h | CO  | HJ, BB |
| VALUE_BET_3WAY_014 | AhAd | Qs5s7s2h | BTN | SB, BB |

Panel reasoning (consistent across all 4):
> "Three spades on the board, hero holds AhAd with no spade
> blocker. Any villain card that is a spade makes a flush.
> Equity only 0.56, danger 0.60, SPR 1.11 — a turn bet is
> stack-committing against a calling range heavily weighted to
> flushes. Bluff-catch line, not value."

## Panel disagreement on the exact same texture class

Interestingly, **batch 04 labelled one AhAd-on-monotone-no-
blocker hand as BET** (VALUE_BET_3WAY_038, SB position, MEDIUM
confidence):

> "Hero has no spade blocker on 3-flush board, but composition
> (17% TP+, 46% air, 88% worse) + villain checking back (flushes
> typically lead multiway) + compressed SPR still favor BET over
> CHECK."

**Different panels reached different conclusions on the same
texture class.** This is consistent with solver mixed-strategy
zones on monotone-no-blocker overpair spots. Both readings are
poker-defensible.

## Factory predicate gap (root-cause analysis)

The generator's predicate `is_made=1 AND eq>=0.55` captures hand
strength but not **texture-specific vulnerability**. AA on
Qs5s7s2h has is_made=1, eq=0.56, but:
- No spade blocker → villain's flush range plays freely
- SPR 1.11 → any bet commits stacks
- Villain range heavily polarized toward flushes after flop
  check-through

The eq threshold (≥0.55) is barely met on this spot (0.56-0.58),
which is precisely the "marginal value / bluff-catch" boundary in
solver theory. A tighter predicate like `eq>=0.60` OR explicit
texture-blocker check would have excluded these.

**This is a legitimate predicate gap, not a panel drift.** My
plan's monotone-inclusive board pool flowed through without a
texture-blocker guard.

## Four paths for reviewer

### Path A — Accept all 39 labels as-is (builder recommends)

Train on 35 BET + 4 CHECK. The 4 CHECK rows teach the model a
real poker truth: "value hands in checked-to spots do NOT
always BET — monotone-no-blocker textures flip to CHECK at
compressed SPR."

Pros:
- Honest signal (panels labelled on poker merits per v3.1)
- Counter-examples to BOTH sides of the value/check boundary
- Teaches texture-sensitivity the model currently lacks
- Protects litmus — AA/KQ on dry/two-tone still BET

Cons:
- Adds a "CHECK in value-looking shape" signal that partially
  offsets Path C's BET-rebalancing intent
- But: self-play will validate the net effect (systemic gate)

### Path B — Re-generate excluding monotone-no-blocker hands

Strengthen picker: when board is monotone, require hero to have
at least one card of the flush suit. Produces 35-40 cleaner
BET-correct rows. ~15 min re-run.

Pros:
- Cleaner BET-only rebalancing as originally intended
- Factory predicate learns from this iteration

Cons:
- Hides a real poker truth from the training distribution
- May cause the model to over-generalize "monotone + is_made =
  BET" in the exact spots v3.1 panels say CHECK

### Path C — Drop the 4 CHECK rows

Train on 35 BET only. Keeps counter-example rebalance; loses
texture-sensitivity signal. 1-line assembly change.

Pros:
- Simplest; 35 BET rows is still solid rebalancing vs v2.3.1's
  40 CHECK

Cons:
- Throws away honestly-labelled data
- Same over-generalization risk as Path B

### Path D — Replace the 4 CHECK rows with 4 new BET-correct specs

Factory re-run excluding monotone-no-blocker, append 4 more BET
rows to hit 39 BET total. ~10 min re-run.

Pros:
- Hits the original 40-ish BET target
- Still loses the texture signal

Cons:
- Same over-generalization risk as B/C

## Builder recommendation — Path A

Reasoning:

1. **The 4 CHECK labels are honestly poker-correct.** Modern
   solver theory on monotone-no-blocker overpair at SPR 1.11 is
   unambiguously bluff-catch-weighted. Rejecting these labels
   would be overriding the v3.1 prompt's output, which is
   explicitly prohibited by `feedback_no_manual_overrides_in_labelling.md`.

2. **Counter-example balance is BIDIRECTIONAL in the target
   subspace.** Path C's premise was "teach both sides of the
   boundary." If both sides genuinely exist in the feature
   subspace (they do, per empirical evidence), the training set
   should reflect that.

3. **Self-play is the systemic gate.** If Path A's net effect
   is wrong (e.g., model still over-CHECKs in dynamic play),
   self-play will catch it — same discipline that caught v2.3.1.
   We shouldn't pre-engineer the training data to a target we
   haven't validated.

4. **The litmus seeds protect the target class.** Both LITMUS_AA
   and LITMUS_KQ = BET in the labels. The Path C intent (value
   on safe textures → BET) is captured via the 35 BET rows.

## Ship-block status

v2.3.2 retraining is GATED on reviewer direction (A/B/C/D). All
prior artifacts are committed:

- Generator: `review/generate_value_bet_v232.py` (4630606)
- Input: `training-data/v23_2_value_bet_3way.jsonl`
- Labels: `training-data/v23_2_value_bet_3way_labelled.jsonl`
  (this commit)
- Workspace: `review/label_batches_value_bet/` (this commit)

Nothing goes into the retrain until reviewer decides scope.

## Cross-stream status (unchanged)

- Game: v2.2
- Teaching: Path B continues independent

Standing by for direction.
