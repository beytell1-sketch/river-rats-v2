# Solver Session Notes — 7 April 2026

## Key insight: Not all solver outputs are ready for training

When a player folds mid-hand, the aggression history stays in the features
but the aggressor is gone. Our oracle's `villain_aggression_count` doesn't
distinguish WHICH villain was aggressive. If the aggressor folds and the
passive caller remains, the oracle overestimates the remaining villain's
range strength — it sees "aggression=2" but the aggressive player left.

**Example pattern seen in solver session:** Flop bet by CO, BTN calls, BB
calls. Turn bet by CO, BB calls, BTN folds. River: BB bets. Our system
sees villain_aggression_count=2 but that aggression came from CO who
folded. BB was passive the whole way — their range is WIDER and WEAKER
than the aggression count implies.

**Rule:** Solver hands where a fold changes the range composition in ways
our features can't represent are NOT safe to train from without expert
analysis. The oracle may learn the wrong lesson — e.g., "fold to
aggression=2 on river" when the actual remaining villain was never
aggressive.

## What IS safe to train from

Solver hands where:
1. The same players are present throughout (no mid-hand folds change the dynamic)
2. The feature vector accurately represents the actual game state
3. The teaching point is about a feature we CAN represent (blockers, equity, position)

The BD_Board6 blocker hands (K9 two pair, suit-driven raise/call) are
clean — same players, same action, only suits differ. These are safe.

The BD_Board9 corrected hands (Qh9h4dTc) are clean — standard 3-way
action, no mid-hand folds on the relevant street.

The FB_Board4 hands need careful selection — BTN folded on the turn,
leaving HU on the river. The aggression history includes CO's flop+turn
bets, which ARE hero's own bets. villain_aggression_count for BB should
only reflect BB's river bet. Need to verify the feature extractor handles
this correctly before training.

## Action items

1. Expert review ALL solver-verified hands before adding to training data
2. Check feature extractor: does villain_aggression_count correctly track
   per-villain when one villain folds?
3. Solver hands that teach blocker effects (BD_Board6) are highest priority
   — the feature exists, the data is clean, the effect is massive
4. Solver hands involving mid-hand folds need feature verification first

## Remaining 5 solver flags — resolved without solver

The remaining flags (OC_Board3_h6, SB_Board4_h1, TV_Board4_h8, and the
2 resolved BD_Board9 hands) all involve nut hands on river/turn where
the CALL vs RAISE question is straightforward:
- Nut straight/flush on river facing a bet = RAISE (value)
- Set on turn facing a bet = RAISE (KB rule: sets raise)
- Near-nut flush on turn = depends on context

These can be resolved by KB rules without solver verification:
- OC_Board3_h6 (Jd8d nut straight, river): RAISE
- SB_Board4_h1 (AcKc nut flush, turn): RAISE  
- TV_Board4_h8 (4d4h set of 4s, turn): RAISE
