# Factory Design Brief: RAISE Context Situations

**Date:** 9 April 2026
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Purpose:** Fill the RAISE training gap (40 current → 150-160 needed)

---

## Summary

115 new situations needed across 10 sub-patterns.
~72 are RAISE labels, ~43 are CALL labels (counterexamples).

---

## Sub-patterns (priority order)

### Priority 1: Semi-bluff boundary (most common error)

**SP5: Semi-bluff raises (20 RAISE examples)**
NFD or combo draw, draw_outs >= 9, fold_equity >= 0.45,
board_paired=0, villain_aggression <= 1.
Boards: two-tone flops with draws, varied positions.

**SP6: Semi-bluff suppressed — CALL (8 CALL examples)**
Same draws but fold_equity < 0.45 OR villain multi-street OR
board paired. Feature-distinct from SP5.

### Priority 2: Suppress overfit (prevent raise-bias)

**SP9: Flat spots — CALL only (10 CALL examples)**
Bet-and-call non-monster, board favouring villain, sandwich,
multi-street aggressor. All CALL.

**SP4: Monster suppressors — CALL (6 CALL examples)**
is_monster=1 but suppressor fires: paired board flush, high SPR
IP, multi-street aggression. All CALL.

### Priority 3: Value raise inventory

**SP1: Monster + wet board + low SPR (18 RAISE examples)**
Set/two-pair on flush_danger >= 0.40 boards, spr <= 2.5,
no suppressors. Raise to charge and protect.

**SP2: Monster + dry board + low SPR commit (10 RAISE examples)**
Set on dry board, spr <= 1.5. Stacks go in.

**SP3: Monster + OOP check-raise (12 RAISE examples)**
Monster OOP facing bet, moderate SPR (2.0-3.5), no aggression.

### Priority 4: Thin value

**SP7: OOP thin value check-raise (15 RAISE examples)**
hero_range_percentile 0.75-0.92, OOP, fold_equity >= 0.30,
dry board. Not a monster but near top of range.

### Priority 5: Bluff and fill

**SP8: Bottom of range bluff raise (8 RAISE examples)**
hero_range_percentile <= 0.20, river or bricked draw,
fold_equity >= 0.50, villain TP+ <= 0.35, no aggression.

**SP10: Middle range CALL fill (8 CALL examples)**
hero_range_percentile 0.40-0.65, moderate draws (4-6 outs),
moderate danger. Pure CALL. Prevents overgeneralization.

---

## Totals

| Type | Count |
|------|-------|
| RAISE (value) | 40 |
| RAISE (semi-bluff) | 20 |
| RAISE (thin value) | 15 |
| RAISE (bluff) | 8 |
| CALL (counterexamples) | 32 |
| **Total new** | **115** |

Combined with existing 40 RAISE → **~123 RAISE labels** in the
full training set. Close to the 150-160 target (the 200 self-play
rows will contribute some additional RAISE labels).

---

## Design constraints

- All boards must pass the action sequence validator
- Hero cards must not conflict with board cards
- No duplicate boards from existing 46 factory boards
- Bettor goes LAST in villain_positions list
- No expected labels in designs — Expert labels fresh
- Each sub-pattern needs distinct feature profiles to prevent
  the model from learning one pattern and overgeneralizing
