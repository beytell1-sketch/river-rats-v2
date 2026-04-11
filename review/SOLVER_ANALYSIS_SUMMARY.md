# Solver Hand Analysis — Full Summary

**Date:** 7 April 2026
**Status:** Analysis complete, awaiting review agents

---

## All 24 solver hands — verdict

### BD_Board6 (9c 7c 2d Kh) — K9 two pair suit variants

| # | Hand | Label | Safe? | Reason |
|---|------|-------|-------|--------|
| 1 | Kh 9d | CALL | YES | flush_block_pct=0, no club blocker, clean |
| 2 | Kd 9h | RAISE | **NO** | Identical vector to Hand 1, opposite label. Secondary heart blocker not captured. |
| 3 | Ks 9h | CALL | YES | Same vector as Hand 1, same label. Harmless. |
| 4 | Kc 9d | RAISE | YES | flush_block_pct positive (Kc blocks clubs). Clean signal. |
| 5 | Kd 9c | N/A | **NO** | INVALID — 9c is on the board. Card conflict. |

### BD_Board9 (Qh 9h 4d Tc) — corrected board, flush draws + combo draws

| # | Hand | Label | Safe? | Reason |
|---|------|-------|-------|--------|
| 1 | Kh 6h | RAISE | **NO** | Near-identical vector to Ah3h, opposite label. No flush_draw_rank feature. |
| 2 | Ah 3h | CALL | **NO** | Near-identical vector to Kh6h, opposite label. |
| 3 | 6h 7h | FOLD | YES | Differentiated by overcard_outs=0, no straight draw. |
| 4 | 8h 7h | CALL | YES | Combo draw (OESD+FD) correctly detected, draw_outs=17. |
| 5 | 9s 9c | CALL | CONDITIONAL | Set calling on flush board may conflict with set=raise elsewhere. |
| 6 | Kh Jh | RAISE | YES | Combo draw, overcard_outs=3 separates from 8h7h. |
| 7 | Ks Jh | RAISE | YES | OESD alone sufficient. draw_outs=8, no flush. |
| 8 | Kc Jd | RAISE | YES | Identical to Hand 7. Volume not information. |
| 9 | Kd Js | RAISE | YES | Identical to Hand 7. Volume not information. |

### FB_Board4 (As 7s 3c Ks 9d) — river value/bluff raising

| # | Hand | Label | Safe? | Reason |
|---|------|-------|-------|--------|
| 1 | Ts 9s | RAISE | YES | hand_category=flush cleanly separates. |
| 2 | Ts 8s | RAISE | YES | Same as above. Original hand confirmed. |
| 3 | 8s 6s | RAISE | YES | Low flush still raises. hand_rank slightly lower. |
| 4 | 6s 5s | RAISE | YES | Lowest flush still raises. |
| 5 | 5s 4s | RAISE | YES | Absolute minimum flush. Same clean signal. |
| 6 | Ac 8s | RAISE | CONDITIONAL | Bluff-raise. flush_block_pct nonzero (8s). Ace blocker not captured. Partial signal. |
| 7 | Ad 8c | RAISE | **NO** | No feature encodes ace-blocker motivation. Looks like a fold candidate. Corrupts river raise signal. |
| 8 | Ad 9c | CALL | YES | Two pair, showdown value. Clean. |
| 9 | Ac 9s | CALL | YES | Two pair + spade blocker. Clean. |
| 10 | K7 (all) | CALL | YES | Two pair on 4-flush board. Clean. |

---

## Scorecard

| Verdict | Count | Hands |
|---------|-------|-------|
| **YES — safe to train** | 15 | BD6: 1,3,4. BD9: 3,4,6,7,8,9. FB4: 1,2,3,4,5,8,9 |
| **CONDITIONAL** | 3 | BD9: 5 (set calls). FB4: 6 (Ac8s bluff). FB4: 10 (K7) |
| **NO — hold** | 4 | BD6: 2 (Kd9h). BD9: 1,2 (Kh6h/Ah3h). FB4: 7 (Ad8c) |
| **INVALID** | 1 | BD6: 5 (Kd9c card conflict) |
| **Deduced** | 1 | BD9: AhKh = RAISE (stronger than Kh6h which raises) |

---

## Missing features identified

1. **flush_draw_rank** — rank of hero's highest flush-suit card when holding a flush draw. Solves Kh6h vs Ah3h contradiction. Low effort.
2. **Secondary-suit blocker** — flush_block_pct only tracks dominant suit. Heart blocking on a club-draw board is invisible. Solves Kd9h vs Kh9d.
3. **Ace-rank blocker** — no feature captures "hero's Ace blocks villain's Ax value range." Needed for river bluff-raise teaching (Ad8c).

---

## villain_aggression_count: CONFIRMED CORRECT

All code paths (pokerbench_parser + game_state_bridge) correctly attribute aggression to the primary villain only. CO's bets as hero are never counted. BB's passive history correctly shows aggression=0. No fix needed for any batch.

---

## Constraint for FB_Board4 hands

Leave `_villain_aggression_count` UNSET in factory specs (defaults to 0). This is correct — BB never bet on prior streets. Do NOT manually calculate from action_history.
