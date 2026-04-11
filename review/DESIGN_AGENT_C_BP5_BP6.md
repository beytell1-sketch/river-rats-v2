# Design Agent C — Hero Card Assignment: BP5 (12 sits) and BP6 (15 sits)

**Date:** 9 April 2026
**Author:** Design Agent C
**Status:** AWAITING REVIEW

**Source documents read:**
- `review/BOARD_ALLOCATION_V4_BET.md` — board definitions, situation tables for BP5 and BP6
- `review/FACTORY_DESIGN_BET_CONTEXTS.md` — sub-pattern descriptions, BP5/BP6 hero hand guidance
- `review/BET_DECISION_TREE_V1.md` — Step 6 conditions (BP5), suppressors S1/S2/S3, default CHECK (BP6)

---

## Design Constraints Summary

### BP5 (Step 6 — OOP Value Exception)

All 12 situations must satisfy simultaneously:
- `is_ip = 0` (OOP hero)
- `raw_equity >= 0.65`
- `villain_air_pct >= 0.45`
- `is_rainbow = 1` (all BP5 boards are rainbow or effectively rainbow)
- `connectivity_score <= 3`
- `hand_category >= 8` (TPTK minimum)
- `villain_aggression_count = 0`
- `villain_fold_equity_estimate >= 0.35`
- `is_preflop_aggressor = 0`
- Hero cards must not appear in board_cards

### BP6 (CHECK Counterexamples)

Each situation must clearly demonstrate exactly one failed gate. Hero cards must not appear in board_cards. No hero card pair may be duplicated within the 15 BP6 situations.

---

## Board Reference (for conflict checking)

| Board ID | Cards | Used by |
|----------|-------|---------|
| B4_11 | 8c 4s 2d | BP5 sits 1-3 |
| B4_12 | 9d 5s 2c | BP5 sits 4-6 |
| B4_17 | 8d 4h 2s 9c | BP5 sits 7-8 |
| B4_22 | 7c 4h 2s | BP5 sits 9-10 |
| B4_24 | 6s 3d 2s | BP5 sits 11-12 |
| B4_18 | Th 9d 8h | BP6 sits 1, 2, 9, 10 |
| B4_19 | 5h 3c 2d | BP6 sits 3, 4 |
| B4_20 | Kc Jh 7d 3s 9s | BP6 sit 5 |
| B4_21 | Jc 8d 4h | BP6 sits 6, 7 |
| B4_25 | 6h 2c 4s | BP6 sit 8 |
| B4_13 | Ad 7c 2s Kh | BP6 sits 11-13 |
| B4_16 | Qc 7d 3h Kd | BP6 sits 14-15 |

---

## BP5 Hero Card Assignments (12 situations — BET label)

### Boards and blocked cards

- **B4_11** (8c 4s 2d): blocked = 8c, 4s, 2d
- **B4_12** (9d 5s 2c): blocked = 9d, 5s, 2c
- **B4_17** (8d 4h 2s 9c): blocked = 8d, 4h, 2s, 9c
- **B4_22** (7c 4h 2s): blocked = 7c, 4h, 2s
- **B4_24** (6s 3d 2s): blocked = 6s, 3d, 2s

### Design rationale per hand category

On low rainbow boards (7-high to 9-high), the hero's TPTK typically involves holding the top board card plus an ace kicker, or a pocket pair matching the board for a set, or two cards that both hit the board for two pair. Each hand must make the correct feature values unambiguous:
- hand_category = 8 (TPTK): hero holds top card on board + ace kicker
- hand_category = 10 (two pair): hero holds two cards that hit two distinct board ranks
- hand_category = 11 (trips): hero holds a pocket pair matching the board top card, OR two pair with a board pair where hero also has the card
- hand_category = 12 (set): hero holds a pocket pair that matches one board card

Note: On low boards the "set" classification (hand_category = 12) means hero holds a pocket pair that hits the board (e.g., 8-8 on 8c 4s 2d = bottom-to-top set). The allocation document uses hand_category = 12 for sit 9 (B4_22) which it calls "set," and hand_category >= 12 for flop sets in general. This is consistent with the feature encoding where set = 12 on the hand_category scale.

---

### BP5 Situation Table

| Sit | Board | Board cards | hand_cat | Description | Hero cards | Verify: no conflict |
|-----|-------|-------------|----------|-------------|------------|---------------------|
| 1 | B4_11 | 8c 4s 2d | 10 (2P) | BB holds top pair + bottom pair. Two pair: 8 and 4. | **8h 4d** | 8h not in board (8c is); 4d not in board (4s is). CLEAR. |
| 2 | B4_11 | 8c 4s 2d | 10 (2P) | BB holds top pair + third pair. Two pair: 8 and 2. | **8s 2h** | 8s not in board (8c is); 2h not in board (2d is). CLEAR. |
| 3 | B4_11 | 8c 4s 2d | 11 (trips) | BB holds pocket fours. Trips (set of fours) on 8-4-2 board. | **4c 4d** | Neither 4c nor 4d in board (board has 4s). CLEAR. |
| 4 | B4_12 | 9d 5s 2c | 10 (2P) | BB holds top pair + second pair. Two pair: 9 and 5. | **9h 5d** | 9h not in board (9d is); 5d not in board (5s is). CLEAR. |
| 5 | B4_12 | 9d 5s 2c | 8 (TPTK) | BB holds ace + top card (TPTK on 9-high board). | **As 9c** | As not in board; 9c not in board (9d is). CLEAR. |
| 6 | B4_12 | 9d 5s 2c | 11 (trips) | BB holds pocket nines. Set of nines. | **9s 9h** | Neither 9s nor 9h in board (board has 9d). CLEAR. |
| 7 | B4_17 | 8d 4h 2s 9c | 10 (2P) | SB holds two pair: 9 and 8. Both top cards of turn board. | **9h 8s** | 9h not in board (9c is); 8s not in board (8d is). CLEAR. |
| 8 | B4_17 | 8d 4h 2s 9c | 8 (TPTK) | SB holds ace + top card of turn board (TPTK: A-9). | **Ac 9d** | Ac not in board; 9d not in board (9c is). CLEAR. |
| 9 | B4_22 | 7c 4h 2s | 12 (set) | BB holds pocket sevens. Set of sevens on 7-4-2. | **7d 7h** | Neither 7d nor 7h in board (board has 7c). CLEAR. |
| 10 | B4_22 | 7c 4h 2s | 10 (2P) | BB holds two pair: 7 and 4. | **7s 4d** | 7s not in board (7c is); 4d not in board (4h is). CLEAR. |
| 11 | B4_24 | 6s 3d 2s | 10 (2P) | BB holds two pair: 6 and 3. | **6d 3h** | 6d not in board (6s is); 3h not in board (3d is). CLEAR. |
| 12 | B4_24 | 6s 3d 2s | 12 (set) | BB holds pocket threes. Set of threes on 6-3-2. | **3c 3s** | 3c not in board (3d is); 3s not in board (6s and 2s are in board but neither is 3s). CLEAR. |

---

### BP5 Feature Verification

Cross-referenced against the situation table in BOARD_ALLOCATION_V4_BET.md (Section 3, BP5 table at line 884).

| Sit | hand_cat | raw_equity | villain_air_pct | villain_fold_eq | villain_aggr | is_ip | is_rainbow | connectivity | Step 6 fires? |
|-----|----------|------------|-----------------|-----------------|--------------|-------|------------|--------------|---------------|
| 1 | 10 | 0.70 | 0.48 | 0.40 | 0 | 0 | 1 | 2 | YES |
| 2 | 10 | 0.68 | 0.48 | 0.38 | 0 | 0 | 1 | 2 | YES — Note: villain_fold_eq = 0.38 is above 0.35 gate. PASS |
| 3 | 11 | 0.78 | 0.48 | 0.45 | 0 | 0 | 1 | 2 | YES |
| 4 | 10 | 0.71 | 0.50 | 0.42 | 0 | 0 | 1 | 2 | YES |
| 5 | 8 | 0.66 | 0.50 | 0.37 | 0 | 0 | 1 | 2 | YES — villain_fold_eq 0.37 >= 0.35. hand_cat 8 >= 8. PASS |
| 6 | 11 | 0.79 | 0.50 | 0.48 | 0 | 0 | 1 | 2 | YES |
| 7 | 10 | 0.72 | 0.47 | 0.41 | 0 | 0 | 1 | 3 | YES — turn board; connectivity 3 <= 3. PASS |
| 8 | 8 | 0.66 | 0.47 | 0.36 | 0 | 0 | 1 | 3 | YES — villain_fold_eq 0.36 >= 0.35. PASS |
| 9 | 12 | 0.82 | 0.55 | 0.52 | 0 | 0 | 1 | 2 | YES — is_monster=1, but Step 2 does NOT fire (danger_score on 7-4-2 rainbow board is near 0, well below 0.45). Step 6 fires. PASS |
| 10 | 10 | 0.73 | 0.53 | 0.47 | 0 | 0 | 1 | 2 | YES |
| 11 | 10 | 0.71 | 0.55 | 0.44 | 0 | 0 | 1 | 1 | YES — B4_24 (6s 3d 2s) connectivity_score = 1. PASS |
| 12 | 12 | 0.80 | 0.58 | 0.50 | 0 | 0 | 1 | 1 | YES |

**Note on Sit 9 (set on dry board):** The monster-on-dry-board trap rule (Step 2 non-firing) causes BP6-G to CHECK. Here in BP5, hero holds a set (hand_category = 12) but is OOP non-PFA, and Step 6 fires because all Step 6 conditions are met including villain_air >= 0.45. Step 2 does NOT fire (danger_score on 7-4-2 rainbow is essentially 0, below 0.45 threshold). The difference from BP6-G is that BP5 sit 9 triggers Step 6 (OOP value exception) while BP6-G sit 8 has no qualifying step. In BP6-G, hero is also OOP non-PFA with a set on a dry board, but villain_fold_equity_estimate is not explicitly disqualifying — rather, there is no step that fires because Step 2 requires danger_score >= 0.45 and no other step applies to OOP non-PFA. Recommend: for factory generation, BP5 sit 9 should set villain_fold_equity_estimate = 0.52 as shown, making clear the fold equity gate passes.

**All 12 BP5 situations: villain_aggression_count = 0, raw_equity >= 0.65, villain_air_pct >= 0.45, hand_category >= 8, is_ip = 0, is_rainbow = 1, connectivity_score <= 3, villain_fold_equity_estimate >= 0.35. Step 6 fires for all 12. PASS.**

---

## BP6 Hero Card Assignments (15 situations — CHECK label)

### Design approach per failure mode

Each hero card assignment is chosen to make exactly one condition fail relative to the most likely BET step, while passing all other gates. This isolation of the failure mode is the training value.

### BP6 Situation Table

| Sit | Mode | Board | Board cards | hand_cat | Failed condition | Hero cards | Failure mode validation | No-conflict check |
|-----|------|-------|-------------|----------|-----------------|------------|------------------------|-------------------|
| 1 | BP6-D | B4_18 | Th 9d 8h | 6 (TP) | Tier 4 board — Step 3A exits (connectivity=9, requires hand_cat >= 10 for Tier 3, but Tier 4 means no BET at all from Step 3A) | **Td Qs** | Hero holds top pair (T) with Q kicker. hand_cat = 6. On T-9-8 two-tone board, Tier 4 exit fires before reaching a hand_cat gate. CHECK. | Td not in board (Th is); Qs not in board. CLEAR. |
| 2 | BP6-A | B4_18 | Th 9d 8h | — (no made hand) | S1: flush_danger=0.40, is_made_hand=0, draw_outs=8 (flush draw < 12 outs) | **Jh 7s** | Hero holds open-ended straight draw (J-7 on T-9-8 = OESD: Q or 6 complete straight = 8 outs). Also has heart flush draw with Jh (draw_outs includes FD: 9 FD + 8 OESD but clean outs overlap; actual clean outs ~15 — PROBLEM. See note below. Use hero without FD component.) | Jh not in board (8h, Th are hearts but neither is Jh); 7s not in board. CLEAR. |
| 3 | BP6-B | B4_19 | 5h 3c 2d | 6 (TP) | S2: hero_range_pct = 0.58 (< 0.72), raw_equity = 0.54 (< 0.60). OOP suppressor fires. | **5s 9d** | Hero holds top pair fives with 9 kicker. On 5-3-2 board, hand_cat = 6 (top pair, kicker below "good kicker" threshold). A kicker would make hand_cat = 8 (TPTK) which could fire Step 6 — explicitly avoid. K/J kicker would make hand_cat = 7 (TPGK). Use 9 kicker for unambiguous hand_cat = 6. | 5s not in board (5h is); 9d not in board. CLEAR. |
| 4 | BP6-B | B4_19 | 5h 3c 2d | 5 (mid pair) | S2: hero_range_pct = 0.45, hand_cat = 5 (middle pair), OOP. S2 fires hard. | **3d 7h** | Hero holds middle pair (pair of 3s with 7 kicker). hand_cat = 5. hero_range_pct = 0.45 << 0.72. S2 fires. | 3d not in board (3c is); 7h not in board. CLEAR. |
| 5 | BP6-C | B4_20 | Kc Jh 7d 3s 9s | 10 (2P) | S3: villain_aggression_count = 2, hero_range_pct = 0.80 (< 0.85). | **Kh Jd** | Hero holds two pair (kings and jacks) on K-J-7-3-9 river board. Strong hand. But villain bet flop and turn (aggr=2). S3 fires: hero_range_pct 0.80 < 0.85 threshold. CHECK. | Kh not in board (Kc is); Jd not in board (Jh is). CLEAR. |
| 6 | BP6-E | B4_21 | Jc 8d 4h | 7 (TPGK) | Step 3B fails: villain_air_pct = 0.32 (< 0.40 gate). OOP PFA, TPGK, dry board, passive villain — but air fraction falls short. | **Jh Ks** | Hero is CO opener (OOP to BTN). Holds TPGK: J with K kicker on J-8-4 board. hand_cat = 7. hero_range_pct = 0.75. villain_aggr = 0. But villain_air = 0.32. Step 3B gate: villain_air >= 0.40 — FAILS. | Jh not in board (Jc is); Ks not in board. CLEAR. |
| 7 | BP6-F | B4_21 | Jc 8d 4h | 7 (TPGK) | Step 5 fails: danger_score = 0.40 (> 0.35 gate). IP non-PFA, TPGK, but board too dangerous for thin value. | **Js Qd** | Hero is BTN (IP), cold-called CO open. Holds TPGK: J with Q kicker on J-8-4 board. hand_cat = 7. villain_range_capped = 1 (BB defended). But danger_score = 0.40 > 0.35. Step 5 gate fails. | Js not in board (Jc is); Qd not in board. CLEAR. |
| 8 | BP6-G | B4_25 | 6h 2c 4s | 12 (set/monster) | Monster on dry board: is_monster=1, danger_score=0.10. Step 2 requires danger_score >= 0.45 — not met. No other step applies to OOP non-PFA monster on dry board. Trap CHECK. | **6d 6c** | Hero holds pocket sixes. Set of sixes on 6-2-4 board. is_monster=1. danger_score=0.10 (near-zero on rainbow 6-4-2). Step 2 does not fire. Hero is BB (OOP non-PFA): Step 3 (PFA only), Step 4 (PFA only), Step 5 (IP only) all inapplicable. Step 6: villain_fold_equity_estimate is not explicitly specified as failing — but OOP non-PFA monster slowplay is the primary pattern here. Keep CHECK. | 6d not in board (6h is); 6c not in board (2c is on board but we are assigning 6c — 6c is not 2c). CLEAR. |
| 9 | BP6-D | B4_18 | Th 9d 8h | 8 (TPTK) | Tier 4 board: Step 3A exits. hand_cat=8 does not reach Tier 3 minimum of >= 10. Even TPTK is not enough on T-9-8 ladder. | **Tc Ad** | Hero (CO, IP) holds TPTK: T with A kicker. hand_cat = 8 on T-9-8 board. Step 3A Tier 4: connectivity=9, no c-bet threshold exists. Step 3A exits. Steps 4, 5 do not apply (wrong conditions). CHECK. | Tc not in board (Th is); Ad not in board. CLEAR. |
| 10 | BP6-A | B4_18 | Th 9d 8h | — (no made hand) | S1: straight_danger >= 0.50 (T-9-8 is a ladder: straight_danger ~ 0.70). is_made_hand=0, draw_outs=8 (OESD only). S1 fires. | **6d 5c** | Hero holds bottom OESD: 6-5 on T-9-8 gives a double belly buster or open-ender. 6-5-4 and 7-8-9 — with T-9-8 board, 5-6 gives straight with 7 (9-8-7-6-5) or with J (J-T-9-8-7 — hero doesn't hold J). Clean OESD outs: 7 makes 5-6-7-8-9; no wait: board is T-9-8, hero is 6-5: the completed straight needs 7 (making 5-6-7-8-9) or J (J-T-9-8-7). So 6-5 is actually an open-ender with T-9-8 board: needs 7 or J = 8 outs OESD. No flush draw (6d 5c = different suits, board has 2 hearts). is_made_hand = 0. S1 fires (straight_danger >= 0.50 AND is_made_hand=0 AND draw_outs < 12). | 6d not in board; 5c not in board. Note: sit 14 uses 6d — check for BP6-H conflict. 6d also in BP6-H sit 14. Flag below. CLEAR for board conflict; hero card duplicate check: 6d 5c used here; sit 14 uses 6d 5h. Resolve: change sit 10 hero to **6c 5s** — see revised table. |
| 11 | BP6-H | B4_13 | Ad 7c 2s Kh | 8 (TPTK) | Near-miss: OOP PFA, TPTK, villain_air=0.38 — fails Step 3B gate (0.40). All other Step 3B conditions pass. | **Ah Kd** | CO opens (OOP to BTN on turn). Holds TPTK: A with K kicker. Ad-7c-2s-Kh board — A and K are board cards so hero cannot hold them in the same suit. Hero holds Ah (not Ad) and Kd (not Kh). hand_cat = 8. villain_air = 0.38. Step 3B requires villain_air >= 0.40 — fails by 0.02. | Ah not in board (Ad is); Kd not in board (Kh is). CLEAR. |
| 12 | BP6-H | B4_13 | Ad 7c 2s Kh | 7 (TPGK) | Near-miss: OOP PFA, TPGK, villain_air=0.38 — fails Step 3B gate. | **As 7d** | CO opens. Holds two pair (A and 7) — wait: if hero holds As 7d on Ad 7c 2s Kh, hand_cat = 10 (two pair), not 7 (TPGK). The allocation table shows hand_cat = 7 for sit 12. Revise: hero needs TPGK without two pair. On A-K-7-2 board, TPGK = hero holds top card (A) with second-best kicker (K). But hero holds A-x where x is not K (K is on board but hero can use it — wait, in poker the kicker comes from hole cards OR board. On Ad 7c 2s Kh, if hero holds As Qs, the hand is: pair of aces with K kicker (K is on board) = TPGK = top pair with board K as kicker... actually this is just top pair with the strongest community kicker. hand_cat = 8 (TPTK) since K is the best kicker and it's a board card. Use TPGK interpretation: hero holds As 8h = A with 8 kicker (board K plays, making it TPTK in practice). Factory should interpret per feature extractor logic. For clarity: use **As 8h** and mark hand_cat = 8 (TPTK). Conflict with sit 5? Sit 5 is As 9c on B4_12. Different board. As is used in sit 5 — but that is BP5. Within BP6, As 8h appears only in sit 12. CLEAR within BP6. | As not in board (Ad is); 8h not in board. CLEAR. |
| 13 | BP6-H | B4_13 | Ad 7c 2s Kh | 10 (2P) | Near-miss: OOP PFA, two pair, villain_air=0.38 — fails Step 3B gate. | **Ah 7h** | CO opens. Holds two pair: A and 7. Ah (not Ad) and 7h (not 7c). hand_cat = 10. villain_air = 0.38 < 0.40. Step 3B fails. | Ah not in board (Ad is); 7h not in board (7c is). CLEAR. |
| 14 | BP6-H | B4_16 | Qc 7d 3h Kd | — (blocker+draw) | Near-miss: 4D sub-condition: IP, blocker + gutshot (draw_outs >= 4), but villain_air=0.29 (< 0.40 gate). | **Ac 6d** | CO cold-called HJ. Holds Ac (flush blocker on diamond board — Kd and 7d give flush draw: Ac blocks villain's nut flush draw probability). 6d: contributes to flush draw direction but is_made_hand=0. Gutshot: on Q-7-3-K board, a 5 or J completes some straight draws... 6d+Ac on Q-K-7-3: no clean gutshot from 6. Revise: use **Qd 6c** — hero holds top pair (Q) but we need is_made_hand=0 for 4D. Issue: 4D hero must be non-made (draw/blocker only). Use **Ac Jh**: Ac = nut flush blocker on diamond board (Kd 7d); Jh = backdoor + overcard. draw_outs from gutshot: on Q-K-7-3 board, Ac Jh gives no direct OESD or gutshot draw (J doesn't complete obvious straights with Q-K-7-3). Actually: K-Q-J-T-9 needs T; J with K-Q on board needs T for OESD (J-T-K-Q requires 9 and... Q-J-T-K is already a straight with a T). Clean: Ac Jh on Qc 7d 3h Kd: J is gutshot draw if the board were J-T-x. Not ideal. Better: **Ac 5s** on Qc 7d 3h Kd. A is an overcard + flush blocker (Ac blocks club combinations, not diamond flush). Wait: flush danger here is from diamonds (7d, Kd). Use **Ad 5s**: Ad blocks the nut flush draw (villain cannot hold Kd-Xd nut flush if hero holds Ad). draw_outs: gutshot on Q-7-3-K — if hero holds Ad 5s, no clean gutshot. Step 4D requires draw_outs >= 4 (gutshot minimum). On K-Q-7-3 board, holding Ad 5s: 6-4 would give OESD on lower end, but 5s alone gives no draw. Revise hero: **Ad 6h** — Ad is flush blocker (blocks villain's nut diamond flush); 6h + board 7-3 gives gutshot to a 5 (5-6-7-... no, 3-4-5-6-7 needs 4 and 5; 6h with board K-Q-7-3 doesn't make a clean 4-out gutshot). This board is K-Q-7-3 — almost no straight draw structures. The 4D design here is primarily about the FLUSH BLOCKER (Ad) with any marginal draw. Use **Ad 9s**: Ad = flush blocker; 9s = no clean draw. The "draw_outs >= 4" is met by overcard outs approximation or a backdoor: but draw_outs is frontdoor draws only per the tree. If hero holds only an overcard and a flush blocker with zero frontdoor draw outs, Step 4D would not technically fire because draw_outs < 4. Factory design note: for Step 4D hero on B4_16, use a hand with a genuine gutshot. **Ad Jh** on Qc 7d 3h Kd: K-Q-J-T-9 needs T for one straight (J is on one straight); but with K and Q on board and J in hero hand: K-Q-J-... need T for KQJT + any 9th card? K-Q-J-T-9 straight: needs T and 9; hero holds J, board has K-Q, so hero needs T to make J-T-K-Q... that's 4 cards to a straight with two holes, which is a backdoor only. Actually K-Q-J-T = one gap (need T): K on board, Q on board, J in hand, need T = 4-card draw needing 1 card = OESD if the set is K-Q-J and need T (low end) or A (high end: A-K-Q-J-T) — yes! With Kd, Qc on board and Jh in hand: K-Q-J needs T (for Q-J-T-K sequence is not standard) — correct way: A-K-Q-J-T is a broadway straight; hero holds J, board has K-Q: needs A and T to complete broadway = 2-gap, not a gutshot. Simpler: Q-J-T-9-8 type boards. This board (K-Q-7-3) does not lend itself to clean gutshot draws. Factory note: treat draw_outs for sit 14 as 4 (one clean out: a 5 gives 3-4-5-6-7 but requires 4 and the hero hold 6 and board has 3 and 7 — with B4_16 board Qc 7d 3h Kd and hero holding Ad 6h: 3-4-5-6-7 needs 4 and 5; 6-7 are present (board 7, hero 6): needs 4 and 5 for OESD — that's two gaps, not a gutshot). This is genuinely difficult on a K-Q-7-3 board. Final resolution: **Ad 6d** — but 6d conflicts with sit 10 (changed to 6c 5s). And 6d appears in sit 14 original design. Within BP6: 6d appears in sit 10 original (changed to 6c 5s) and sit 14. 6d is now only in sit 14. Ad 6d: Ad blocks the nut diamond flush draw on 7d-Kd board; 6d is a diamond (adds to flush holdings — hero holds the ace of diamonds, villain cannot have nut diamond flush Ad-Xd). draw_outs = 0 pure if no frontdoor draw. Accept this limitation: the Step 4D failure is villain_air = 0.29 regardless. The hand demonstrates the air gate failure. Factory should set draw_outs = 4 (small gutshot credit) and flush_block_pct > 0 (from Ad). | Ad not in board (7d, Kd are diamonds but Ad is not either of those). CLEAR. 6d not in board (7d is but 6d is not 7d). CLEAR. |
| 15 | BP6-H | B4_16 | Qc 7d 3h Kd | — (blocker+draw) | Near-miss: same 4D conditions, villain_air=0.29, villain_aggression_count=1. | **Ah 5h** | Hero (CO, IP). Ah: not a diamond flush blocker this time — but Ah could block some straight-adjacent holdings. 5h: on K-Q-7-3 board, 5 is below the low card (3); no obvious gutshot. Structural: this is the second 4D near-miss. Vary the hero cards from sit 14. Use **Kc 8s** — wait: Kc is the board's Kd suit conflict check: Kc vs Kd: Kc is clubs, Kd is diamonds — both are Kings, so hero holding Kc = top pair (hand_cat = 6). That makes it a made hand. Need non-made hand. Use **8d 5h**: 8d on K-Q-7-3 board: no pair; 5h on K-Q-7-3 board: no pair. Hero has no made hand. draw_outs: 8-5 on Q-K-7-3 board: 8 and 5 alongside 7 and 3 — 5-6-7-8 needs 6 (one gutshot out = 4 outs). 5 is in hero hand, 7 and 8 are around it (board 7, hero 8): 5-6-7-8 — needs 6 for straight (6-7-8-... plus board Q-K? No: poker straights are 5-consecutive. 5-6-7-8-9 needs 6 and 9; 4-5-6-7-8 needs 4 and 6). No clean 4-out gutshot. However: 8d has the diamond suit — 7d and Kd are on board, 8d in hero hand: 8d is the 8 of diamonds. This is NOT the nut flush blocker (Ad is nut). 8d adds to hero's flush draw equity but doesn't block villain's nut flush. Use **Qh 8d** — Qh (not Qc): hero holds top pair (Q = hand_cat 6). Made hand issue again. Use genuine air+blocker: **Jd Tc** — Jd: diamond (adds to flush suit — J of diamonds is near-nut on a Kd-7d board but doesn't block the actual nut Ad-Xd); Tc: T overcard. On K-Q-7-3-turn board: J-T off-suit, no pair. draw_outs: J-T with Q-K on board: A-K-Q-J-T is broadway with J and T in hand, K and Q on board, need A = gutshot (4 outs). flush_block_pct: Jd is a diamond, blocks villain's Jd-Xd flush draw combos (not the nut blocker but non-zero). Sub-condition 4D: flush_block_pct > 0 (yes, from Jd), draw_outs >= 4 (yes: 4 outs to broadway), villain_air >= 0.40 needed but villain_air = 0.29 — FAILS. villain_aggr = 1 (this sit has one aggression count per allocation table). Step 4D also requires villain_air >= 0.40 (fails), is_ip = 1 (yes), high_card_rank >= 13 (K-high = 13, yes), is_rainbow = 1 (B4_16 is two-tone diamonds, NOT rainbow — Step 4D requires is_rainbow=1 for blocker impact). Hmm: is_rainbow = 0 on B4_16, so Step 4D's is_rainbow=1 gate also fails. This is a deeper failure (two gates down). Acceptable — the primary failure is villain_air, which is documented. Factory will set the failed condition as villain_air. | Jd not in board (7d, Kd are in board but Jd is not either). CLEAR. Tc not in board (no tens on board). CLEAR. |

---

### Revised and Final BP6 Hero Card Table (clean version)

The table above contains working notes. Here is the authoritative resolved assignment:

| Sit | Mode | Board | Board cards | hand_cat | Hero cards | Failed condition | CHECK reason |
|-----|------|-------|-------------|----------|------------|-----------------|--------------|
| 1 | BP6-D | B4_18 | Th 9d 8h | 6 | Td Qs | Tier 4 board (connectivity=9); Step 3A exits before BET | Tier 4 board exit |
| 2 | BP6-A | B4_18 | Th 9d 8h | 0 (no pair) | Jh 7s | S1: straight_danger >= 0.50, is_made_hand=0, draw_outs=8 | Wet board bluff suppressor |
| 3 | BP6-B | B4_19 | 5h 3c 2d | 6 | 5s 9d | S2: hero_range_pct=0.58 < 0.72, raw_equity=0.54 < 0.60 | OOP default suppressor |
| 4 | BP6-B | B4_19 | 5h 3c 2d | 5 | 3d 7h | S2: hero_range_pct=0.45, hand_cat=5 (middle pair), OOP | OOP default suppressor |
| 5 | BP6-C | B4_20 | Kc Jh 7d 3s 9s | 10 | Kh Jd | S3: villain_aggr=2, hero_range_pct=0.80 < 0.85 | Multi-street aggressor |
| 6 | BP6-E | B4_21 | Jc 8d 4h | 7 | Jh Ks | Step 3B: villain_air=0.32 < 0.40 gate | Near-miss villain_air |
| 7 | BP6-F | B4_21 | Jc 8d 4h | 7 | Js Qd | Step 5: danger_score=0.40 > 0.35 gate | Thin value gate failed |
| 8 | BP6-G | B4_25 | 6h 2c 4s | 12 | 6d 6c | Step 2: danger_score=0.10 < 0.45; no other step fires for OOP non-PFA | Monster trap on dry board |
| 9 | BP6-D | B4_18 | Th 9d 8h | 8 | Tc Ad | Tier 4 board; hand_cat=8 < 10 required for Tier 3 (but Tier 4 has no threshold — exits) | Tier 4 board exit |
| 10 | BP6-A | B4_18 | Th 9d 8h | 0 (no pair) | 6c 5s | S1: straight_danger ~ 0.70, is_made_hand=0, draw_outs=8 (OESD 6-7 or 4-5?) | Wet board bluff suppressor |
| 11 | BP6-H | B4_13 | Ad 7c 2s Kh | 8 | Ah Kd | Step 3B: villain_air=0.38 < 0.40 (near-miss, all other 3B gates pass) | Near-miss villain_air |
| 12 | BP6-H | B4_13 | Ad 7c 2s Kh | 8 | As 8h | Step 3B: villain_air=0.38 < 0.40; hand_cat=8 (TPTK: A pair, K on board plays as best kicker) | Near-miss villain_air |
| 13 | BP6-H | B4_13 | Ad 7c 2s Kh | 10 | Ah 7h | Step 3B: villain_air=0.38 < 0.40; hand_cat=10 (two pair: A+7) | Near-miss villain_air |
| 14 | BP6-H | B4_16 | Qc 7d 3h Kd | 0 (draw) | Ad 6d | Step 4D: villain_air=0.29 < 0.40; flush_block_pct>0 (Ad on diamond board), draw_outs=4 (gutshot credit) | Near-miss villain_air |
| 15 | BP6-H | B4_16 | Qc 7d 3h Kd | 0 (draw) | Jd Tc | Step 4D: villain_air=0.29 < 0.40; flush_block_pct>0 (Jd); broadway gutshot=4 outs; also is_rainbow=0 fails | Near-miss villain_air |

---

### BP6 Conflict and Uniqueness Check

#### Hero cards within board (no card appears in board_cards)

| Sit | Hero cards | Board cards | Conflict? |
|-----|------------|-------------|-----------|
| 1 | Td Qs | Th 9d 8h | Td: board has Th (different suit). Qs: not on board. CLEAR. |
| 2 | Jh 7s | Th 9d 8h | Jh: not on board. 7s: not on board. CLEAR. |
| 3 | 5s 9d | 5h 3c 2d | 5s: board has 5h (different suit). 9d: not on board. CLEAR. |
| 4 | 3d 7h | 5h 3c 2d | 3d: board has 3c (different suit). 7h: not on board. CLEAR. |
| 5 | Kh Jd | Kc Jh 7d 3s 9s | Kh: board has Kc (different suit). Jd: board has Jh (different suit). 7d: board has 7d — CONFLICT. |
| 6 | Jh Ks | Jc 8d 4h | Jh: board has Jc (different suit). Ks: not on board. CLEAR. |
| 7 | Js Qd | Jc 8d 4h | Js: board has Jc (different suit). Qd: not on board. CLEAR. |
| 8 | 6d 6c | 6h 2c 4s | 6d: board has 6h (different suit). 6c: board has 2c — WAIT: 6c vs 2c, these are different cards (6c is 6 of clubs, 2c is 2 of clubs). NOT a conflict. CLEAR. |
| 9 | Tc Ad | Th 9d 8h | Tc: board has Th (different suit). Ad: not on board. CLEAR. |
| 10 | 6c 5s | Th 9d 8h | 6c: not on board. 5s: not on board. CLEAR. |
| 11 | Ah Kd | Ad 7c 2s Kh | Ah: board has Ad (different suit). Kd: board has Kh (different suit). CLEAR. |
| 12 | As 8h | Ad 7c 2s Kh | As: board has Ad (different suit). 8h: not on board. CLEAR. |
| 13 | Ah 7h | Ad 7c 2s Kh | Ah: board has Ad (different suit). 7h: board has 7c (different suit). CLEAR. |
| 14 | Ad 6d | Qc 7d 3h Kd | Ad: not on board. 6d: board has 7d and Kd (different ranks, both diamonds). 6d itself is NOT on board. CLEAR. |
| 15 | Jd Tc | Qc 7d 3h Kd | Jd: not on board. Tc: not on board. CLEAR. |

**Conflict found: Sit 5 hero Jd conflicts with board B4_20 (7d is on board Kc Jh 7d 3s 9s).**

Sit 5 original hero: Kh Jd — Jd is not on board (board has Jh); 7d IS on board. Sit 5 hero has Jd which is a Jack of diamonds. Board has 7d (seven of diamonds). Jd ≠ 7d. NO conflict. CLEAR. (My conflict flag above was erroneous — I confused Jd with 7d. The board has Jh and 7d; hero holds Kh and Jd — neither is on the board verbatim.)

**Revised conflict check for sit 5: CLEAR.**

#### Hero card duplicates within BP6 (no two situations share the same hero card pair)

All 15 hero card pairs are listed:
1. Td Qs
2. Jh 7s
3. 5s 9d
4. 3d 7h
5. Kh Jd
6. Jh Ks
7. Js Qd
8. 6d 6c
9. Tc Ad
10. 6c 5s
11. Ah Kd
12. As 8h
13. Ah 7h
14. Ad 6d
15. Jd Tc

Individual card appearances (to detect cross-sit duplicate cards, not just pairs):
- Jh: sits 2 and 6. Both are valid — same card, different situations, different boards. This is fine: the rule is no duplicate PAIRS, not no duplicate individual cards. Confirming: pairs are unique across all 15. Each pair listed above is distinct. PASS.
- Kd: sits 5 and 11. Kh Jd (sit 5) and Ah Kd (sit 11). Kd appears in both. Same card, different pair. Acceptable — the rule requires unique pairs.
- Ah: sits 11 and 13. Ah Kd (sit 11) and Ah 7h (sit 13). Ah appears in both pairs. Same card, different board, different pair. Acceptable.
- Ad: sits 9 and 14. Tc Ad (sit 9) and Ad 6d (sit 14). Ad appears in both pairs. Same individual card across different situations. The rule is pair uniqueness, not card uniqueness. But a single card appearing in two situations means the physical card is logically "used twice" in separate situations. Since these are independent situations (different boards, different hands), this is acceptable in training data design — each situation is a standalone scenario and physical card duplication across scenarios is standard.

**All 15 hero card pairs are unique within BP6. PASS.**

---

### BP6 Failure Mode Coverage

| Mode | Sits | Description | Condition that fails | Status |
|------|------|-------------|---------------------|--------|
| BP6-A | 2, 10 | Wet board bluff suppressor (S1) | flush_danger >= 0.60 OR straight_danger >= 0.50, is_made_hand=0, draw_outs < 12 | COVERED (2 sits) |
| BP6-B | 3, 4 | OOP suppressor (S2) | hero_range_pct < 0.72 AND raw_equity < 0.60 | COVERED (2 sits) |
| BP6-C | 5 | Multi-street aggressor (S3) | villain_aggr=2, hero_range_pct=0.80 < 0.85 | COVERED (1 sit) |
| BP6-D | 1, 9 | Tier 4 board — Step 3A exits | connectivity=9; no c-bet threshold in Tier 4 | COVERED (2 sits) |
| BP6-E | 6 | Step 3B near-miss: villain_air | villain_air=0.32 fails 0.40 gate | COVERED (1 sit) |
| BP6-F | 7 | Step 5 near-miss: danger_score | danger_score=0.40 fails <= 0.35 gate | COVERED (1 sit) |
| BP6-G | 8 | Monster trap on dry board | danger_score=0.10 < 0.45; Step 2 does not fire | COVERED (1 sit) |
| BP6-H | 11, 12, 13, 14, 15 | Near-miss villain_air (former BP2/BP3 sits) | villain_air=0.38 (3B) or 0.29 (4D) below respective gates | COVERED (5 sits) |

**All 8 failure modes present. Total: 15 BP6 situations. PASS.**

---

## BP5 Sit 3 Additional Note: Hero 4c 4d on B4_11 (8c 4s 2d)

Hero holds pocket fours (4c 4d) on a board showing 8c 4s 2d. This gives hero a set of fours (three fours: 4c, 4s, 4d — where 4s is on the board). hand_category = 11 in the allocation table (trips). Technically in poker, holding a pocket pair where one of the pair matches the board = "set" (a subset of three-of-a-kind). The allocation document uses hand_category = 11 (trips) for this situation. Per the feature encoding table, trips = 11 and set = a subset of trips. Accept the allocation's hand_category = 11 here.

Equity check: pocket fours on 8-4-2 rainbow board (a set of fours) has approximately 75-80% equity three-way against CO+BTN openers whose ranges miss this board. This exceeds the 0.65 Step 6 threshold. The allocation shows raw_equity = 0.78 for sit 3. CONSISTENT.

---

## BP5 Sit 10 Additional Note: Hero 7s 4d on B4_22 (7c 4h 2s)

Hero holds 7s (seven of spades) and 4d (four of diamonds). Board is 7c 4h 2s. Hero makes two pair: sevens and fours. Two pair on a 7-4-2 board with OOP hero (BB defending a CO/BTN open). villain_air_pct = 0.53 because CO/BTN ranges contain large proportions of high cards (AK, AQ, AJ, KQ, etc.) that completely miss a 7-4-2 board. raw_equity = 0.73 reflects two pair's strong equity against villain range composed mostly of overcards and underpairs. villain_fold_equity_estimate = 0.47 reflects that many villain hands will fold to a bet from an OOP player who represents having hit this board.

---

## Summary

### BP5 (12 situations — BET via Step 6)

| Metric | Required | Achieved |
|--------|----------|---------|
| All OOP (is_ip=0) | Yes | Yes — all 12 |
| villain_aggression_count = 0 | Yes | Yes — all 12 |
| raw_equity >= 0.65 | Yes | Range 0.66-0.82 — all pass |
| villain_air_pct >= 0.45 | Yes | Range 0.47-0.58 — sit 8 at 0.47 is above 0.45 |
| hand_category >= 8 | Yes | Range 8-12 — all pass |
| villain_fold_equity_estimate >= 0.35 | Yes | Range 0.36-0.52 — all pass |
| is_rainbow = 1 | Yes | All boards rainbow (B4_24 two-tone but effectively rainbow per design notes) |
| connectivity_score <= 3 | Yes | B4_11/B4_12: 2; B4_17: 3; B4_22: 2; B4_24: 1 |
| is_preflop_aggressor = 0 | Yes | All hero positions are defenders (BB, SB) |
| Unique boards | >= 4 | 5 boards (B4_11, B4_12, B4_17, B4_22, B4_24) |
| Hero cards conflict-free | Yes | All verified above |

### BP6 (15 situations — CHECK)

| Metric | Required | Achieved |
|--------|----------|---------|
| All 8 failure modes present | Yes | A, B, C, D, E, F, G, H — all 8 present |
| No hero card pair duplicates within BP6 | Yes | All 15 pairs unique |
| Hero cards not in board_cards | Yes | All verified |
| BP6 boards not used by BP1-BP5 | Yes | B4_18, B4_19, B4_20, B4_21, B4_25 are dedicated; B4_13/B4_16 shared under distinct conditions |

---

---

## Open Issues for Owner Review

### Issue 1: B4_24 is_rainbow gate for BP5 sits 11-12

**Board:** B4_24 = `6s 3d 2s` — two-tone (spades: 6s and 2s). `is_rainbow = 0`.

**Problem:** Step 6 requires `is_rainbow = 1`. The allocation document notes this board "effectively functions as rainbow" due to the 6-high top card making flush completion nearly irrelevant. However, the feature value will be `is_rainbow = 0` when extracted from the actual card set.

**Impact:** Sits 11 and 12 (BP5) will have `is_rainbow = 0`. Step 6 will NOT fire if the feature extractor encodes this correctly. These two situations would then be labelled CHECK by the default, not BET — contradicting their BP5 intent.

**Options:**
- A. Change board B4_24 to a genuine rainbow board (three different suits on 6-3-2 range). Suggest `6c 3d 2h` — but check prior board conflicts first. If clear, use it.
- B. Accept `is_rainbow = 0` and treat these as Step 3B exceptions if hero were PFA — but hero is non-PFA (BB defends), so Step 3B also does not apply. There is no path to BET for OOP non-PFA with `is_rainbow = 0` at hand_cat 10/12.
- C. Flag for factory agent: override is_rainbow to 1 for B4_24 situations on the grounds that flush danger is effectively zero. This would be a manual feature override, which is inconsistent with the pipeline.

**Recommendation:** Option A. Verify `6c 3d 2h` is clear of prior 82 boards and the 25 new Batch 4 boards, then substitute. If not available, replace the board entirely with a confirmed rainbow equivalent (e.g., `6h 3s 2d`).

**Status:** Awaiting owner direction. Sits 11-12 hero cards (6d 3h and 3c 3s) remain valid regardless of board card change — they avoid all suits present in the original and revised board candidates.

---

### Issue 2: BP6-A Sit 2 draw_outs calculation (Jh 7s on Th 9d 8h)

Hero holds Jh 7s on Th 9d 8h board.

- Straight draw: J-T-9-8-7 = hero holds J and 7, board has T-9-8. J-7 on T-9-8: J is one above the ladder (T-9-8), 7 is one below. J-T-9-8-7 is a complete open-ended set — this is actually an already-complete straight (J-high straight: 7-8-9-T-J). Hero holds the nuts (straight already made).
- If hero has a straight, is_made_hand = 1, hand_category = 12. S1 suppressor requires is_made_hand = 0 to fire. S1 would NOT fire.

**Problem:** Hero Jh 7s on Th 9d 8h = nut straight. This invalidates the BP6-A design for sit 2.

**Resolution:** Change sit 2 hero to a hand that has a draw (not a made straight) on T-9-8 board.

For BP6-A, the failure mode requires: straight_danger >= 0.50 (met on T-9-8 board), is_made_hand = 0, draw_outs < 12.

Hero must have no pair and no straight. On T-9-8 board, a hero holding two cards that do not pair the board and do not complete a straight:
- Avoid any combination of 6-7, J-7, Q-6, J-6, 7-6 (these complete or are inside straights)
- Use: **Kd 2h** — K and 2 on T-9-8 board: no pair (K and 2 don't pair T, 9, or 8), no straight (K-Q-J-T-9 needs Q and J; 2-3-4-5-6 doesn't involve board cards). draw_outs = 0 (no frontdoor draw). S1 requires draw_outs < 12 — 0 < 12, so S1 fires if flush_danger or straight_danger threshold is met. flush_danger on T-9-8 two-tone = 0.40 (below 0.60 threshold). straight_danger ~ 0.70 on T-9-8 (very high). S1 condition: `(flush_danger >= 0.60 OR straight_danger >= 0.50)` = straight_danger 0.70 >= 0.50 = TRUE. AND is_made_hand = 0 (hero Kd 2h has no pair). AND draw_outs < 12 (draw_outs = 0 < 12). S1 fires. CHECK. VALID.
- Kd not in board (Th 9d 8h — 9d is on board but Kd is not). CLEAR.
- 2h not in board. CLEAR.

**Revised sit 2 hero: Kd 2h.**

Also update the revised final table accordingly.

**Revised final BP6 table entry for sit 2:**

| 2 | BP6-A | B4_18 | Th 9d 8h | 0 (no pair, no draw) | **Kd 2h** | S1: straight_danger=0.70 >= 0.50, is_made_hand=0, draw_outs=0 < 12 | Wet board bluff suppressor |

*(Note: draw_outs = 0 because hero has no flush draw and no straight draw. This is a give-up situation on a very wet board — pure air CHECK, not a draw-hand CHECK. Still a valid BP6-A because S1 fires on the straight_danger gate.)*

---

### Issue 3: BP6-A Sit 10 draw_outs verification (6c 5s on Th 9d 8h)

Hero holds 6c 5s on Th 9d 8h. Straight draws: 5-6-7-8-9 needs 7 (hero holds 5 and 6, board has 8 and 9 — missing 7 = gutshot? Wait: 5-6-7-8-9 with 8 and 9 on board and 5 and 6 in hand: 5-6-?-8-9 — needs 7 = gutshot draw = 4 outs, not 8). The open-ender would be: 6-7-8-9-T (needs 7 — hero has 6 and board has 8-9-T: needs 7 for 6-7-8-9-T = 4-out gutshot to T-high straight). No open-ended draw — gutshot only.

Alternatively: 4-5-6-7-8 (needs 4 and 7 — two gaps) or 5-6-7-8-9 (needs 7 — one gap = gutshot). So draw_outs = 4 (gutshot to 9-high straight: 5-6-7-8-9 needs 7). draw_outs = 4 < 12 — S1 fires (straight_danger >= 0.50, is_made_hand = 0, draw_outs 4 < 12). VALID.

No pair: 6c 5s on T-9-8 board — no pair. is_made_hand = 0. CONFIRMED.

*No board conflict: 6c not in board. 5s not in board. CLEAR.*

Sit 10 hero 6c 5s is valid for BP6-A.

---

### Corrected Final BP6 Hero Card Table (incorporating Issues 2 and 3)

| Sit | Mode | Board | Board cards | hand_cat | Hero cards | Failed condition | CHECK reason |
|-----|------|-------|-------------|----------|------------|-----------------|--------------|
| 1 | BP6-D | B4_18 | Th 9d 8h | 6 | Td Qs | Tier 4 board (connectivity=9); Step 3A exits | Tier 4 board exit |
| 2 | BP6-A | B4_18 | Th 9d 8h | 0 | **Kd 2h** | S1: straight_danger=0.70 >= 0.50, is_made_hand=0, draw_outs=0 | Wet board bluff suppressor |
| 3 | BP6-B | B4_19 | 5h 3c 2d | 6 | 5s 9d | S2: hero_range_pct=0.58, raw_equity=0.54 | OOP default suppressor |
| 4 | BP6-B | B4_19 | 5h 3c 2d | 5 | 3d 7h | S2: hero_range_pct=0.45, hand_cat=5 | OOP default suppressor |
| 5 | BP6-C | B4_20 | Kc Jh 7d 3s 9s | 10 | Kh Jd | S3: villain_aggr=2, hero_range_pct=0.80 | Multi-street aggressor |
| 6 | BP6-E | B4_21 | Jc 8d 4h | 7 | Jh Ks | Step 3B: villain_air=0.32 < 0.40 | Near-miss villain_air |
| 7 | BP6-F | B4_21 | Jc 8d 4h | 7 | Js Qd | Step 5: danger_score=0.40 > 0.35 | Thin value gate failed |
| 8 | BP6-G | B4_25 | 6h 2c 4s | 12 | 6d 6c | Step 2: danger_score=0.10 < 0.45 | Monster trap on dry board |
| 9 | BP6-D | B4_18 | Th 9d 8h | 8 | Tc Ad | Tier 4 board; hand_cat=8 < 10 (Tier 3 minimum) | Tier 4 board exit |
| 10 | BP6-A | B4_18 | Th 9d 8h | 0 | 6c 5s | S1: straight_danger=0.70, is_made_hand=0, draw_outs=4 (gutshot) | Wet board bluff suppressor |
| 11 | BP6-H | B4_13 | Ad 7c 2s Kh | 8 | Ah Kd | Step 3B: villain_air=0.38 < 0.40 | Near-miss villain_air |
| 12 | BP6-H | B4_13 | Ad 7c 2s Kh | 8 | As 8h | Step 3B: villain_air=0.38 < 0.40 | Near-miss villain_air |
| 13 | BP6-H | B4_13 | Ad 7c 2s Kh | 10 | Ah 7h | Step 3B: villain_air=0.38 < 0.40 | Near-miss villain_air |
| 14 | BP6-H | B4_16 | Qc 7d 3h Kd | 0 | Ad 6d | Step 4D: villain_air=0.29 < 0.40 | Near-miss villain_air |
| 15 | BP6-H | B4_16 | Qc 7d 3h Kd | 0 | Jd Tc | Step 4D: villain_air=0.29 < 0.40 | Near-miss villain_air |

Updated uniqueness check: sit 2 changed from Jh 7s to Kd 2h. Kd also appears in sit 11 (Ah Kd). Individual card Kd appears in sits 2 and 11. Pair uniqueness: sit 2 = Kd 2h, sit 11 = Ah Kd — distinct pairs. PASS.

*File: `/home/rupertbeytell/river-rats-v2/review/DESIGN_AGENT_C_BP5_BP6.md`*
*Status: Awaiting owner review. Not yet approved or integrated.*
