# GTO Labelling — Calibration Batch 3 Answers

**Date:** 2026-04-09
**Agent:** GTO Labeller v1 (knowledge base v1.2)
**Reference material:** prompts/gto_labeller_v1.md + knowledge/three_way_gto.md

---

```
REF_ID: MW-37
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds top pair decent kicker (QJ on Q72r) IP with 54.2% equity vs 25% pot odds — a large surplus. The board is dry and rainbow (danger 0.0), villain's air pct is 0.333, and only 9.6% of CO's range currently beats hero, meaning worse_hand_pct is 88.8%. A single CO bet into a 3-way pot on a dry board represents a wide range including many Qx worse kickers and air; facing one bet with no callers confirming strength, CALL is correct. RAISE is rejected because CO is uncapped (has AK, AA, KK) and top pair does not clear the two pair+ threshold required to build a large pot 3-way.
```

```
REF_ID: MW-38
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds the nut flush draw (AhJh on Kh8h3d) with 44.4% equity against 33.3% pot odds — a clear call on equity alone. The Ah blocker is present, which in a different configuration could support a raise, but BB's donk-lead into a 3-way pot represents a strong, narrow range (villain_air_pct only 9.2%, villain_tp_plus 20.3%) — the fold equity from a raise is drastically reduced. Calling cleanly realizes the 9-out draw at a price well below its equity value; raising into a strong donk range with CO still potentially live creates unnecessary risk.
```

```
REF_ID: MW-39
ACTION: CALL
CONFIDENCE: MEDIUM
REASONING: Hero holds the nut flush draw (AhJh) with Ah blocker on Kh8h3d, facing a CO c-bet with 44.75% equity vs 26.83% pot odds. The Ah blocker satisfies one condition for the Section 1.7 raise carve-out, but villain_air_pct is only 5.4% — CO's betting range is extremely value-heavy on this king-high board, severely limiting fold equity from a raise. SPR is 1.11 (extremely compressed), so a raise approaches commitment; calling still gives 44.75% equity well above pot odds and realizes the draw at a fair price. The semi-bluff raise is rejected because insufficient fold equity against a strong, uncapped CO range negates the blocker advantage.
```

```
REF_ID: MW-41
ACTION: CALL
CONFIDENCE: HIGH
REASONING: This is the Worked Example 8 pattern: hero holds second pair (QhTc on KsQd7cJh) plus an 8-out open-ended straight draw (any 9 or A makes broadway) with 34.07% equity vs 23.08% pot odds and IP position. While CO's double-barrel signals a strong, narrow range (villain_aggression_count=2, villain_tp_plus 49.3%, villain_air_pct only 3.9%), the 8 draw outs survive range narrowing — hitting the straight beats CO's entire continuing range. The key distinction from a pure fold situation: hero is not dominated with no outs, but rather has significant equity improvement paths. IP position further supports calling over folding.
```

```
REF_ID: MW-44
ACTION: CALL
CONFIDENCE: HIGH
REASONING: Hero holds top pair with straight draw (Th8h on Ts9h4d7c) with 42.85% equity vs 28.0% pot odds — a 14.8pp surplus — plus 8 outs to the straight (any 6 or J). Villain is a capped BB (villain_range_capped=1, no premiums) whose donk-lead range is strong but bounded; worse_hand_pct is 63.4%, confirming the majority of BB's range is weaker than hero's holding. SPR is 0.56 (near commitment), equity is well above pot odds, hero is IP, and 8 clean outs exist when called. Folding would be a significant over-fold given the equity surplus and draw equity.
```

```
REF_ID: MW-48
ACTION: CHECK
CONFIDENCE: HIGH
REASONING: Hero holds a gutshot straight draw only (AhTc on QdJc4s, any K makes broadway) OOP in a 3-way pot with 28.73% equity and no facing bet. The knowledge base explicitly classifies gutshot-only hands as check/folds 3-way: fold equity is ~36% (0.6 x 0.6) and a gutshot has only 4 outs per street, making a semi-bluff unprofitable OOP against two opponents. Despite villain_air_pct being relatively high (42.2%), the OOP position and draw weakness override thin value or semi-bluff considerations. Checking allows hero to realize hidden overcard equity (the Ah may pair on later streets) without inflating the pot from a losing position.
```

```
REF_ID: MW-49
ACTION: BET
CONFIDENCE: HIGH
REASONING: Hero holds TPTK (AdKd on As9c5dTc) IP with 55.37% equity, both opponents checked to hero, worse_hand_pct is 84.4%, villain_range_capped=1 (capped flat-caller range), and SPR is 0.47 — near commitment. With the vast majority of two opponents' ranges weaker than TPTK, no aggression signal to respect, and a shallow SPR that makes pot-building essential, betting for value is mandatory. Checking back would give two opponents a free card and forfeit significant value against 84% weaker holdings; at SPR 0.47 any bet is near-commitment, so hero must get the money in while ahead.
```

```
REF_ID: MW-50
ACTION: FOLD
CONFIDENCE: HIGH
REASONING: This is the named calibration case: BTN raised CO's flop bet in a 3-way pot (a near-nuts signal in 3-way play), then fires a turn barrel with villain_tp_plus at 60.3% — BTN's action-implied range is dominated by sets and strong two-pair that crush hero's JcTc (top pair poor kicker, no draw). Equity is 30.98% vs 29.03% pot odds — only 1.95pp above break-even — and this equity is computed against full preflop ranges, not BTN's narrowed post-raise range. OOP position, zero draw outs, board_favour of -0.303, and a range-narrowing flop raise followed by a turn barrel all combine to make this a fold despite technically positive pot odds.
```
