# Phase 1 Redesign — 5 Facing-Bet Situations
**Date:** 2026-04-13
**Author:** Architecture Expert
**Task:** Redesign FB-23, FB-32, FB-33, FB-34, FB-37 per definitive audit findings
**Source A:** `review/comms/DEFINITIVE_ACTION_ORDER_AUDIT_2026-04-12.md`
**Source B:** `review/comms/ML_ARCHITECT_FACING_BET_TEST_SET_2026-04-12.md`

---

### FB-23

**Original error:** BTN folds on the turn without any bet being live — illegal action.

**Fix approach:** BTN checks on the turn (legal — no bet live), then folds to CO's river bet before hero acts. The intended game state (BTN out before river hero decision) is preserved. River bet sizing changed from 60 (50% of 120 pot — not on approved list) to 90 (75% pot), which also improves axis coverage for the "large bet" sizing axis.

**Board:** Ad 9c 3h 2s Kd
**Street:** River
**Hero position:** BB — CLOSING
**Bettor:** CO (river bet after passive multi-street line)
**Third player:** BTN (folds to CO's river bet before hero acts)
**Bet sizing:** 75% pot (90 into 120)

**Corrected action sequence:**
```
Preflop: CO opens, BTN calls, BB (hero) calls.
Flop Ad 9c 3h: BB checks, CO checks, BTN checks.
Turn 2s: BB checks, CO checks, BTN checks.
River Kd: BB checks, CO bet 90, BTN fold, BB ???
```

**Validator output (turn street):**
```
VALID
```
**Validator output (river street):**
```
VALID
```

**Pot / Bet / To call:** 120 / 90 / 90
**Pot odds:** 90 / (120 + 90 + 90) = 90 / 300 = 30%

**Axis coverage preserved?** River, OOP hero, closes action, large sizing (75% now replaces 50%), dry two-tone runout, IP bettor, passive multi-street line. All original axes retained; large-bet sizing axis now correctly filled.

---

### FB-32

**Original error:** BTN hero faces CO bet with BB called — impossible because BTN is first clockwise from CO (BTN must respond before BB can act on CO's bet).

**Fix approach:** Change hero position from BTN to BB. After CO bets, the clockwise response order is BTN(5) first, then BB(1) wraps. BTN calls first, then BB (hero) faces the bet-and-call. This is the structurally valid bet-and-call pattern for this pot: CO bet → BTN call → BB hero last. Bet sizing changed from 30 (33% — not on approved list) to 60 (66% pot), preserving the connected board texture and making the bet-and-call more pedagogically interesting.

**Board:** Jd 8s 6h
**Street:** Flop
**Hero position:** BB — CLOSING
**Bettor:** CO (c-bet on connected rainbow)
**Third player:** BTN (already called — bet-and-call)
**Bet sizing:** 66% pot (60 into 90)

**Corrected action sequence:**
```
Preflop: CO opens, BTN calls, BB (hero) calls.
Flop Jd 8s 6h: BB check, CO bet 60, BTN call 60, BB ???
```

**Validator output:**
```
VALID
```

**Pot / Bet / To call:** 90 / 60 / 60
**Pot after BTN call:** 210
**Pot odds (hero's call):** 60 / (210 + 60) = 60 / 270 = 22%

**Axis coverage preserved?** Flop, bet-and-call, connected rainbow, range compression, large sizing (upgraded from small). Hero moves from BTN to BB — OOP hero axis now served instead of IP hero. FB-31 already covers BTN/IP/closing on this same board (Jd 8s 6h), so using BB here avoids redundancy. Net axis change: IP → OOP for this bet-and-call situation.

---

### FB-33

**Original error:** BB hero faces BTN bet with CO called — impossible because BB is first clockwise from BTN (BB must respond before CO can act on BTN's bet).

**Fix approach:** Change hero position from BB to CO. After BTN bets, clockwise response order is BB(1) first, then CO(4). BB calls first, then CO (hero) faces the bet-and-call. This is structurally valid: BTN bet → BB call → CO hero last. Bet sizing changed from 45 (50% — not on approved list) to 60 (66% pot), preserving the paired board texture. Preflop structure unchanged: BTN opens, CO calls, BB calls.

**Board:** Th Td 7c
**Street:** Flop
**Hero position:** CO — CLOSING
**Bettor:** BTN (IP c-bet on paired board)
**Third player:** BB (already called — bet-and-call)
**Bet sizing:** 66% pot (60 into 90)

**Corrected action sequence:**
```
Preflop: BTN opens, CO (hero) calls, BB calls.
Flop Th Td 7c: BB check, CO check, BTN bet 60, BB call 60, CO ???
```

**Validator output:**
```
VALID
```

**Pot / Bet / To call:** 90 / 60 / 60
**Pot after BB call:** 210
**Pot odds (hero's call):** 60 / (210 + 60) = 60 / 270 = 22%

**Axis coverage preserved?** Flop, bet-and-call, paired board, range compression, standard-to-large sizing. Hero moves from BB (OOP-first-responder) to CO (OOP but closing after BB call). The bet-and-call with CO hero still tests cold-call range compression from the CO perspective — BB's call of a paired-board bet is highly polarising (full house, set, or pure float). Core pedagogical axis (range compression on paired board) fully preserved.

---

### FB-34

**Original error:** BB hero faces BTN bet with CO called — impossible because BB is first clockwise from BTN (same structural error as FB-33).

**Fix approach:** Change hero position from BB to CO. After BTN bets, clockwise response order is BB(1) first, then CO(4). BB calls first, then CO (hero) faces the bet-and-call. Preflop: CO opens, BTN calls, BB calls (CO is the preflop aggressor — maintained). Bet sizing changed from 30 (33% — not on approved list) to 25% pot (22 into 90) to use the approved small-bet sizing. This distinguishes FB-34 from FB-33 on the sizing axis (small bet vs large bet), even though both are bet-and-call situations.

**Board:** As 9s 4s
**Street:** Flop
**Hero position:** CO — CLOSING
**Bettor:** BTN (IP c-bet on monotone board)
**Third player:** BB (already called — bet-and-call on monotone)
**Bet sizing:** 25% pot (22 into 90)

**Corrected action sequence:**
```
Preflop: CO opens, BTN calls, BB calls.
Flop As 9s 4s: BB check, CO check, BTN bet 22, BB call 22, CO ???
```

**Validator output:**
```
VALID
```

**Pot / Bet / To call:** 90 / 22 / 22
**Pot after BB call:** 134
**Pot odds (hero's call):** 22 / (134 + 22) = 22 / 156 = 14%

**Axis coverage preserved?** Flop, bet-and-call, monotone board, range compression, small sizing. Hero moves from BB (OOP-first-responder) to CO (OOP but closing). CO is now the preflop aggressor facing a bet on their own opened board — a distinct and pedagogically valid scenario. The monotone + small-bet + bet-and-call combination is unique in the test set, and CO-as-PFA-facing-a-bet adds the "PFA loses initiative" dimension.

---

### FB-37

**Original error:** CO's initiative-round check omitted before BTN bets on the turn — in a BB/CO/BTN pot, initiative order is BB → CO → BTN, so CO must check before BTN can bet. Additionally, after BTN bets, BB (who checked in the initiative round) must still respond to the bet in the clockwise-from-BTN order (BB first, then CO) — this response was also absent.

**Fix approach:** Add (1) CO's initiative check, and (2) BB's fold response to BTN's bet before CO acts. The full sequence is now: BB check → CO check → BTN bet → BB fold → CO faces. Bet sizing changed from 60 (67% — not on approved list) to 68 (75% pot, rounded), preserving the "large bet" axis the original intended. BB folding to the bet reduces it to heads-up for CO.

**Board:** Ac Jh 5d Ks
**Street:** Turn
**Hero position:** CO — CLOSING
**Bettor:** BTN (delayed c-bet on turn after all-check flop)
**Third player:** BB (folds to BTN's bet before hero acts)
**Bet sizing:** 75% pot (68 into 90)

**Corrected action sequence:**
```
Preflop: BTN opens, CO (hero) calls, BB calls.
Flop Ac Jh 5d: BB checks, CO checks, BTN checks.
Turn Ks: BB check, CO check, BTN bet 68, BB fold, CO ???
```

**Validator output (turn):**
```
VALID
```

**Pot / Bet / To call:** 90 / 68 / 68
**Pot odds:** 68 / (90 + 68 + 68) = 68 / 226 = 30%

**Axis coverage preserved?** Turn, OOP hero (closes action), large sizing (75% replaces 67%), dry rainbow, IP bettor (delayed c-bet). All original axes retained. BB now explicitly folds to the bet rather than being implicitly absent, making the sequence fully legal and unambiguous.

---

## Summary Table

| ID    | Original Error                        | Fix                                       | Hero Pos | Street | Sizing      | Classification |
|-------|---------------------------------------|-------------------------------------------|----------|--------|-------------|----------------|
| FB-23 | BTN folds turn without facing a bet   | BTN checks turn, folds to river bet       | BB       | River  | 75% pot     | CLOSING        |
| FB-32 | BB can't call CO's bet before BTN     | Hero → BB; BTN calls first, BB last       | BB       | Flop   | 66% pot     | CLOSING        |
| FB-33 | CO can't call BTN's bet before BB     | Hero → CO; BB calls first, CO last        | CO       | Flop   | 66% pot     | CLOSING        |
| FB-34 | CO can't call BTN's bet before BB     | Hero → CO; BB calls first, CO last        | CO       | Flop   | 25% pot     | CLOSING        |
| FB-37 | CO check + BB response both missing   | Add CO check and BB fold in correct order | CO       | Turn   | 75% pot     | CLOSING        |

## Axis Distribution Impact

All five corrected situations remain CLOSING-classification. The original spec intended FB-33 and FB-34 to be OOP-first-responder situations (BB facing a bet with CO/BTN behind) — the fixes convert both to CLOSING (CO hero, last to act after BB's call). This is a necessary structural consequence of the bet-and-call mechanic: the player who faces both the bet AND a prior call must be last in the clockwise-from-bettor order, which means CLOSING is the only valid classification for this sub-axis.

Net axis change from the original 40-situation design:
- CLOSING count: +2 (FB-33 and FB-34 change from intended FIRST-RESPONDER to CLOSING)
- FIRST-RESPONDER count: -2
- All other axes (board texture, street, sizing tiers, bet-and-call sub-axis) preserved or improved.

If the FIRST-RESPONDER count must be maintained, the shortfall can be recovered by adding two new simple-facing-bet situations (no bet-and-call, OOP hero with players behind) — but this is a design decision for the Creative Lead / ML Architect, not a structural requirement of these five fixes.
