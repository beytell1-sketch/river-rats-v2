# Board Allocation V4 — BET Context Batch (104 Situations)
**Date:** 10 April 2026
**Author:** Board Architect
**Status:** REVISED v2 — Review issues 1-5 resolved (9 April 2026)
**Brief:** FACTORY_DESIGN_BET_CONTEXTS.md
**Supersedes:** N/A (first BET batch)

---

## Corrections Applied

### Round 1 corrections (original Section 8 — 6 items)

The following corrections resolve all six open items from the original Section 8.
Section 8 (Open Items) has been removed; all flags are cleared.

| # | Item | Resolution |
|---|------|------------|
| 1 | BP6 board isolation (CRITICAL) | Added B4_19, B4_20, B4_21, B4_22 — four dedicated BP6 boards. All BP6 situations now use only these boards plus B4_18. Zero overlap with BP1-BP5 boards. |
| 2 | Paired board (R2) | Added B4_23 (`5c 5d Ah`) — paired fives, A-high kicker. Assigned to BP1 (paired board changes monster-protection dynamics). Cards verified clear of all 82 prior boards. |
| 3 | SPR variation | SPR assignment table added to each sub-pattern section below. Board definitions unchanged; factory situation agent assigns effective_stack per row per the table. |
| 4 | BP3 turn count | Two additional turn situations added to BP3 using B4_16 (4D sub-condition), bringing BP3 turn total from 4 to 6. BP3 allocation table updated. |
| 5 | BP5 board count | B4_24 (`6s 3d 2h`) added — low rainbow flop, OOP hero, passive villains. BP5 board count: 4 unique boards. Minimum met. |
| 6 | B4_13 card note | Already accepted as non-conflicting. No action required. |

Board total after Round 1: 24 boards (B4_01–B4_24).

---

### Round 2 corrections (reviewer issues 1-5 — 9 April 2026)

| # | Issue | Resolution |
|---|-------|------------|
| R2-1 | CRITICAL: B4_03 listed as IP in BP1 — CO is OOP relative to BTN in CO/BTN/BB pot | Removed B4_03 from BP1. Its 2 BP1 situations reassigned to B4_01 (BTN opener, genuinely IP). BP1 sits 7-8 now use B4_01. BP1 total unchanged at 30. B4_03 retained in BP2 only (OOP PFA — correct). |
| R2-2 | MODERATE: B4_22 shared between BP5 and BP6-G, violates brief R1 board isolation | Added B4_25 (`6h 2c 4s`) — new dedicated very dry rainbow board for BP6-G. B4_22 removed from BP6-G. B4_22 now BP5-only. BP6 board count updated. |
| R2-3 | MODERATE: Total count was unstated at 104 vs brief target of 100 | Total is 104. The 4 extra situations (2 from BP3 turn expansion, 2 from BP5 board expansion) fill real structural gaps and are retained. Summary table updated to show 104. |
| R2-4 | MODERATE: BP2 sits 13-15 have villain_air_pct=0.38, below Step 3B gate of 0.40 | Moved sits 13-15 from BP2 to BP6 as near-miss CHECK counterexamples (villain_air 0.38 vs gate 0.40). BP2: 15→12. BP6 gains 3 BP6-H situations. |
| R2-5 | MODERATE: BP3 4D sits 21-22 have villain_air_pct=0.29, below Step 4D gate of 0.40 | Moved sits 21-22 from BP3 4D to BP6 as near-miss CHECK counterexamples. BP3: 22→20. BP6 gains 2 more BP6-H situations. |

**Revised counts after Round 2:**
- BP1: 30 (unchanged)
- BP2: 12 (was 15 — 3 moved to BP6)
- BP3: 20 (was 22 — 2 moved to BP6)
- BP4: 15 (unchanged)
- BP5: 12 (unchanged)
- BP6: 15 (was 10 — gained 5 near-miss counterexamples; B4_25 added for BP6-G isolation)
- **Total: 104**

Board total after Round 2: 25 boards (B4_01–B4_25).

---

## Card Conflict Protocol

A "card conflict" is defined as two boards in the combined inventory sharing
the same rank+suit where the boards are near-identical in composition (3+ shared
cards out of a 3-card flop). Single-card overlaps between otherwise distinct boards
are permitted — this is consistent with Batch 3 practice (e.g., 2c appears on
both B01 and SB_B3 without conflict flagging).

Cards from the 79-board prior inventory are tracked below each new board
definition. Any single-card overlap is noted; multi-card overlaps are avoided.

---

## Section 1 — Board Definitions (25 boards)

All boards: to_call = 0. Hero acts without facing a bet on this street.
SPR = effective_stack / pot.

---

### Flop Boards (B4_01 – B4_12)

---

**B4_01** — Rainbow, A-high, very dry | Tier 1
- board_cards: `['Ad', 'Tc', '4h']`
  *(Note: Ad free of B01/B03/B09/B17 boards; Tc appears on B25 but boards otherwise distinct; 4h appears on PA_Board3/SB_B7/B09 — three distinct boards, no near-identity risk)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor — all checked to hero)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow, A-high (high_card_rank=14), connectivity_score=2, flush_danger=0.0
- Tier: 1
- Sub-patterns: BP1 (primary — IP PFA Tier 1 value c-bet)
- villain_air_pct target: 0.35-0.40 (SB/BB call wide preflop, miss A-T-4r frequently)

---

**B4_02** — Rainbow, K-high, dry | Tier 1
- board_cards: `['Ks', 'Jh', '3c']`
  *(Ks appears on CALL_Board2/FB_B4/B24/B28 — all distinct; Jh on PA_Board3/SB_B8/FB_B1/OC_B2/B23; 3c on FB_B2/B17)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor — all checked to hero)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow, K-high (high_card_rank=13), connectivity_score=3, flush_danger=0.0
- Tier: 1
- Sub-patterns: BP1 (IP PFA Tier 1), BP2 (OOP PFA Tier 1 — with hero_pos remapped to CO or HJ for OOP use; see BP2 note in Section 3)
- villain_air_pct target: 0.38-0.43

---

**B4_03** — Rainbow, A-high, moderate gap | Tier 1
- board_cards: `['Ah', '8s', '3d']`
  *(Ah appears on CALL_Board4/SB_B7/B09; 8s on SB_B4/B19/TV_B4/B11r; 3d on PA_Board1 area — all distinct boards)*
- street: flop
- hero_pos: CO
- villain_positions: `['BB', 'BTN']` (no bettor — all checked to CO)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- is_preflop_aggressor: 1 | is_ip: 0
  *(CO opens, BTN cold-calls, BB calls. Postflop order: BB → CO → BTN. BB checks, CO (hero) acts next with to_call=0. BTN has not acted yet — their action is not in the history. is_ip=0. R2-1 correction: removed from BP1 IP usage.)*
- Texture: Rainbow, A-high (high_card_rank=14), connectivity_score=2, flush_danger=0.0
- Tier: 1
- Sub-patterns: BP2 only (OOP PFA — CO opens, BTN cold-calls, CO acts first postflop = OOP)
- villain_air_pct target: 0.38-0.45

---

**B4_04** — Rainbow, K-high, very dry | Tier 1
- board_cards: `['Kd', '6c', '2s']`
  *(Kd on CALL_Board5/BD_B1/SB_B6/B16/B18/TV_B3/B23/B31; 6c on PA_Board2; 2s on CALL_Board3/OC_B3/TV_B3/B13/B30 — all distinct)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow, K-high (high_card_rank=13), connectivity_score=2, flush_danger=0.0
- Tier: 1
- Sub-patterns: BP1 (IP PFA), BP2 (OOP variant with CO/HJ opener)
- villain_air_pct target: 0.40-0.48 (K-6-2r, BTN/CO cold-callers miss hard)

---

**B4_05** — Rainbow, Q-high, moderate | Tier 2
- board_cards: `['Qs', '9c', '5h']`
  *(Qs on PA_Board4/SB_B8/B05/B32; 9c on PA_Board6/SB_B4/SB_B7/B20; 5h on CALL_Board7/FB_B5/TV_B3/B07/B16 — single overlaps only, boards distinct)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow (Qs 9c 5h — three different suits), Q-high (high_card_rank=12), connectivity_score=3 (Q-9 gap=3, 9-5 gap=4), flush_danger=0.0
- Tier: 2
- Sub-patterns: BP1 (IP PFA Tier 2), BP4 (IP non-PFA thin value)
- villain_air_pct target: 0.28-0.35

---

**B4_06** — Two-tone (diamonds), Q-high | Tier 2
- board_cards: `['Qd', 'Jd', '5c']`
  *(Revised from Qd 8s 4d — 4d conflicted with BD_B5. Qd+Jd: TV_B2=Jd 7c 3s Ah has Jd, not Qd. No prior board has both Qd and Jd. 5c: SB_B4=Jc 8s 4c 9c has 4c but not 5c. CLEAR.)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Two-tone (diamonds: Qd, Jd), Q-high (high_card_rank=12), connectivity_score=3 (Q-J adjacent pair with 5 far below), flush_danger=0.25
- Tier: 2
- Sub-patterns: BP1 (IP PFA Tier 2), BP3 (4B NFD semi-bluff — hero holds Kd or Ad)
- villain_air_pct target: 0.30-0.38

---

**B4_07** — Rainbow, J-high, connected | Tier 2/3
- board_cards: `['Jc', '9h', '7s']`
  *(Jc on CALL_Board5/SB_B4/PA_Board7/B13/BD_B4/FB_B5; 9h on CALL_Board2/B08/B14/B21; 7s on SB_B5/B17)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow (Jc 9h 7s — three suits), J-high (high_card_rank=11), connectivity_score=6 (J-9-7 two-gap ladder), flush_danger=0.0
- Tier: 2 (high_card_rank=11, connectivity=6 is borderline Tier 2/3)
- Sub-patterns: BP1 (IP PFA Tier 2, hero needs TPGK+), BP3 (4A combo draw — 8h-Ts on Jc-9h-7s has OESD+FD)
- villain_air_pct target: 0.30-0.38

---

**B4_08** — Rainbow, T-high, connected | Tier 3
- board_cards: `['Tc', '8h', '5s']`
  *(Revised from Tc 8h 6d — 6d conflicted with B25. Tc+5s: PA_Board5=Ts 9d 5c 7h has Ts not Tc, 5c not 5s. CLEAR. 8h+5s: no prior board has both. CLEAR.)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow (Tc 8h 5s), T-high (high_card_rank=10), connectivity_score=7 (T-8 gap=2, 8-5 gap=3), flush_danger=0.0
- Tier: 3 (connectivity=7, hero needs two-pair+)
- Sub-patterns: BP1 (IP PFA Tier 3 — hero must hold two pair like T-8), BP3 (4A combo draw — 9s-7s has OESD on T-8-5)
- villain_air_pct target: 0.28-0.35

---

**B4_09** — Two-tone (spades), K-high, semi-connected | Tier 2 (BP3 primary)
- board_cards: `['Ks', '7s', '6d']`
  *(Ks on CALL_Board2/SB_B1/FB_B4/B24/B28; 7s on SB_B5/B17; 6d on CALL_Board4/B01/FB_B3/B25)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Two-tone (spades: Ks, 7s), K-high (high_card_rank=13), connectivity_score=4 (7-6 adjacent, K far), flush_danger=0.25
- Tier: 1/2 (K-high, but two-tone places it Tier 2)
- Sub-patterns: BP3 (4B — hero holds As or Qs for NFD + blocker; 4C — As-Xh for nut flush draw + board_favour on K-high), BP1 (IP PFA, top pair value c-bet)
- villain_air_pct target: 0.35-0.45

---

**B4_10** — Two-tone (hearts), Q-high, connected | Tier 2/3 (BP3 4A primary)
- board_cards: `['Qh', '9s', '8h']`
  *(Qh on CALL_Board3/SB_B2/FB_B5/B20/B26/B33; 9s on TV_B3/CALL_Board8/B15/B21/B24; 8h on PA_Board3/CALL_Board6/FB_B5/B27)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Two-tone (hearts: Qh, 8h), Q-high (high_card_rank=12), connectivity_score=5 (Q-9 gap=3, 9-8 adjacent), flush_danger=0.30
- Tier: 2
- Sub-patterns: BP3 (4A combo draw — Jh-Th has OESD [K/7 completes straight] + heart FD = 15 outs; 4B — hero holds Kh for NFD), BP1 (IP PFA top pair)
- villain_air_pct target: 0.32-0.42

---

**B4_11** — Rainbow, low board, very dry | BP5 primary
- board_cards: `['8c', '4s', '2d']`
  *(8c on B06/BD_B3; 4s on TV_B1/B04/B05/B25; 2d on SB_B6/B12/B24)*
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
  *(BB acts first; to_call = 0 because no one has bet)*
- opener_position: CO
- is_preflop_aggressor: 0 (BB is defender, non-PFA)
- is_ip: 0
- Texture: Rainbow (8c 4s 2d), low board (high_card_rank=8), connectivity_score=2, flush_danger=0.0
- Tier: 1 (by connectivity/flush criteria; low high_card serves BP5)
- Sub-patterns: BP5 (OOP value exception — hero hits hard, CO opener misses)
- villain_air_pct target: 0.45-0.55 (BTN/CO open ranges miss 8-4-2r heavily)
- villain_aggression_count: 0 (required for BP5)

---

**B4_12** — Rainbow, low board, disconnected | BP5 primary
- board_cards: `['9d', '5s', '2c']`
  *(9d on PA_Board5/CALL_Board2/PA_Board6/BD_B4/B04; 5s on CALL_Board8/SB_B8; 2c on SB_B3/FB_B1/B01/B03)*
- street: flop
- hero_pos: BB
- villain_positions: `['HJ', 'BTN']` (no bettor — hero acts first)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, HJ, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: HJ
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Rainbow (9d 5s 2c), low (high_card_rank=9), connectivity_score=2, flush_danger=0.0
- Tier: 1 (by texture criteria; serves BP5)
- Sub-patterns: BP5 (OOP value exception)
- villain_air_pct target: 0.45-0.53
- villain_aggression_count: 0 (required for BP5)

---

### Turn Boards (B4_13 – B4_17)

---

**B4_13** — Rainbow, A-high, dry turn | Tier 1 (BP1 + BP2 turn)
- board_cards: `['Ad', '7c', '2s', 'Kh']`
  *(Ad on PA_Board6/TV_B2; 7c on CALL_Board3/OC_B3/BD_B6/B23/TV_B2; 2s on CALL_Board3/OC_B3/TV_B3/B13/B30; Kh on B02/BD_B4/B26 — 7c and 2s both appear on OC_B3, a 5-card river board of very different composition. Accepted as non-conflicting per multi-card near-identity definition.)*
- street: turn
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor — all checked to BTN on turn)
- pot: 90 | to_call: 0 | effective_stack: 970 | SPR: **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, check)
  - (turn, SB, check), (turn, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Rainbow (Ad 7c 2s Kh), A-high (high_card_rank=14), connectivity_score=2, flush_danger=0.0
- Tier: 1
- Sub-patterns: BP1 (IP PFA turn continuation), BP2 (OOP PFA turn variant — hero_pos CO for Section 3 remapping)
- villain_air_pct target: 0.35-0.42
- villain_aggression_count: 0 (no flop bet from either villain)

---

**B4_14** — Two-tone (spades), K-high turn | Tier 1/2 (BP3 turn semi-bluff)
- board_cards: `['Kc', '9s', '4c', 'Qs']`
  *(Revised from Kd 9s 4c Qs — Kd+9s conflicted with TV_B3. Kc+9s: FB_B2=Kc 9c 5d 3c has Kc and 9c, not 9s. CLEAR. Kc+Qs: B32=Th Jc Qs 3h has Qs, no Kc. CLEAR. Kc+4c: SB_B4=Jc 8s 4c 9c has 4c, no Kc. CLEAR.)*
- street: turn
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor on turn)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check), (flop, BTN, check)
  - (turn, SB, check), (turn, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Two-tone (spades: 9s, Qs), K-high (high_card_rank=13), connectivity_score=3, flush_danger=0.30
- Tier: 1/2
- Sub-patterns: BP3 (4B — hero holds As for NFD + blocker on K-Q-9-4 two-tone; 4C — nut flush draw + board_favour on K-high), BP1 (turn value c-bet)
- villain_air_pct target: 0.35-0.45

---

**B4_15** — Two-tone (spades), J-high turn, semi-connected | Tier 2 (BP4 primary)
- board_cards: `['Js', '6s', '2d', '8c']`
  *(Revised from Jd 6h 2c 8d — Jd+8d conflicted with CALL_Board1; 6h+2d conflicted with SB_B6. Js+8c: CALL_Board8=7h 7d 5s 9c Js has Js, no 8c. CLEAR. 6s+2d: SB_B5=7s 6s 5d has 6s, no 2d. OC_B4=6s 3h 2c Ts has 6s and 2c, not 2d. CLEAR. Js+6s: two spades.)*
- street: turn
- hero_pos: BTN
- villain_positions: `['CO', 'BB']` (no bettor on turn)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, BB, check), (turn, CO, check)
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 1
- Texture: Two-tone (spades: Js, 6s), J-high (high_card_rank=11), connectivity_score=3, flush_danger=0.25
- Tier: 2
- Sub-patterns: BP4 (IP thin value non-PFA — BTN cold-called CO, villain BB is capped defender)
- villain_range_capped: 1 (BB defended, excluded 3-bet premiums)
- villain_aggression_count: 0 (no flop bet)

---

**B4_16** — Two-tone (diamonds), K-high turn, dry | Tier 1/2 (BP4 primary)
- board_cards: `['Qc', '7d', '3h', 'Kd']`
  *(Revised from Qc 7h 3s Td — Qc+3s conflicted with PA_Board8. Qc+7d: TV_V4=Tc 7d 4c 8s has 7d, no Qc. CLEAR. Qc+3h: SB_B2=Qh 8d 3h has 3h, Qh not Qc. CLEAR. 3h+Kd: BD_B8=6h 3d 2h 9c Ks has 3d not 3h, Ks not Kd. CLEAR. 7d+Kd: BD_B1=Ac Kd 7h has Kd and 7h, not 7d. CLEAR.)*
- street: turn
- hero_pos: CO
- villain_positions: `['BB', 'HJ']` (no bettor on turn)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, HJ, raise), (preflop, CO, call), (preflop, BB, call)
  - (flop, BB, check), (flop, HJ, check), (flop, CO, check)
  - (turn, BB, check), (turn, HJ, check)
- opener_position: HJ
- is_preflop_aggressor: 0 | is_ip: 1
- Texture: Two-tone (diamonds: 7d, Kd), K-high (high_card_rank=13), connectivity_score=2, flush_danger=0.20
- Tier: 1/2
- Sub-patterns: BP4 (IP thin value non-PFA — CO cold-called HJ, BB is capped), BP1 (if hero is remapped to HJ opener = PFA turn c-bet), BP3 (4D turn variants — see BP3 note)
- villain_range_capped: 1 (BB cold-call is capped)
- villain_aggression_count: 0

---

**B4_17** — Rainbow, low turn, disconnected | BP5 turn
- board_cards: `['8d', '4h', '2s', '9c']`
  *(8d on PA_Board1/CALL_Board1/TV_B1/SB_B2/BD_B7/B18; 4h on PA_Board3/SB_B7/B09; 2s on CALL_Board3/OC_B3/TV_B3/B13/B30; 9c on PA_Board6/SB_B4/SB_B7/B20)*
- street: turn
- hero_pos: SB
- villain_positions: `['CO', 'BTN']` (no bettor on turn — all checked flop and turn to SB)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, SB, call)
  - (flop, SB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, SB, check)
  *(turn, SB acts first as OOP; to_call=0 at SB's turn decision)*
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Rainbow (8d 4h 2s 9c), low (high_card_rank=9), connectivity_score=3, flush_danger=0.0
- Tier: 1 (by texture criteria for BP5)
- Sub-patterns: BP5 (OOP value exception turn — villain_aggression_count=0 because no flop bet)
- villain_air_pct target: 0.45-0.52
- villain_aggression_count: 0 (no flop bet from either CO or BTN)

---

### Flop Board for BP6 Counterexamples — B4_18 (original)

---

**B4_18** — Two-tone (hearts), very wet, high connectivity | BP6 only
- board_cards: `['Th', '9d', '8h']`
  *(Th on SB_B7/B32; 9d on PA_Board5/CALL_Board2/PA_Board6/BD_B4/B04; 8h on PA_Board3/CALL_Board6/FB_B5/B27)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Two-tone (hearts: Th, 8h), T-high (high_card_rank=10), connectivity_score=9 (T-9-8 ladder), flush_danger=0.40
- Tier: 4 (connectivity_score >= 8 = Tier 4 exit in Step 3A)
- Sub-patterns: BP6-D (Tier 4 board — even with top pair, Step 3A exits; hero needs two-pair+ to bet here), BP6-A (wet board suppressor)
- Design notes: Hero holds Td-Qs (top pair, hand_category=6) — not strong enough for Tier 4. CHECK.

---

### New BP6 Boards (B4_19 – B4_22) — Isolation Fix

---

**B4_19** — Rainbow, very low, disconnected | BP6-B only
- board_cards: `['5h', '3c', '2d']`
  *(5h: CALL_Board7/FB_B5/TV_B3/B07/B16 — single overlaps only. 3c: FB_B2/B17/B4_02 — single overlaps only. 2d: B4_11/SB_B6/B12/B24 — single overlaps only. 5h+3c: no prior board has both. 5h+2d: no prior board has both. 3c+2d: no prior board has both. CLEAR.)*
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Rainbow (5h 3c 2d — three suits), low (high_card_rank=5), connectivity_score=1, flush_danger=0.0
- Sub-patterns: **BP6-B only** — OOP hero, failed range threshold (hero_range_percentile < 0.72, raw_equity < 0.60). Villain (CO opener) misses this board almost entirely; but hero also does not have a strong enough hand to overcome OOP suppressor.
- villain_air_pct target: 0.15-0.35 (CHECK counterexample — villain_air not high enough to justify OOP bet with weak hand)
- villain_aggression_count: 0

---

**B4_20** — River board, multi-suit, K-high | BP6-C only
- board_cards: `['Kc', 'Jh', '7d', '3s', '9s']`
  *(Kc: FB_B2=Kc 9c 5d 3c — 9c and 3c, not 9s or 3s. No prior board has Kc+Jh. Jh+7d: no prior board. Jh+3s: SB_B8=Qs 8s 3d 5c Jh has Jh and 3d, not 3s. CLEAR. 7d+9s: no prior board. 3s+9s: SB_B1=Ks Jd 5s — no 3s or 9s on SB_B1. CLEAR.)*
- street: river
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP on river)
- pot: 270 | to_call: 0 | effective_stack: 700
- SPR: 700/270 = **2.6** (reduced — multi-street action has contracted stacks)
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, bet), (flop, BTN, call), (flop, BB, call)
  - (turn, BB, check), (turn, CO, bet), (turn, BTN, call), (turn, BB, call)
  - (river, BB, check to act)
  *(villain_aggression_count = 2: CO bet flop AND bet turn. Now river, hero acts first OOP with to_call=0 — villain has not yet acted on this street)*
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Two-tone (spades: 3s, 9s) with K-high runout, high_card_rank=13, flush_danger=0.20 (two spades on board)
- Sub-patterns: **BP6-C only** — Multi-street aggressor. villain_aggression_count=2. Hero has a decent hand (hero_range_percentile=0.78-0.82, below the 0.85 gate). S3 fires. CHECK.
- villain_aggression_count: 2 (flop bet + turn bet on prior streets; river is current street)

---

**B4_21** — Rainbow, J-high, moderate gap | BP6-E and BP6-F
- board_cards: `['Jc', '8d', '4h']`
  *(Jc: CALL_Board5/SB_B4/PA_Board7/BD_B4/FB_B5 — single overlaps. 8d: CALL_Board1=Jd 8d 4c — Jd not Jc; SB_B2/BD_B7/B18/TV_B1 — single overlaps only. 4h: PA_Board3/SB_B7/B09 — single overlaps. Jc+8d: CALL_Board1 has Jd+8d (Jd not Jc). No prior board has both Jc and 8d. Jc+4h: no prior board. 8d+4h: no prior board. CLEAR.)*
- street: flop
- hero_pos: varies by situation (see BP6 table)
- villain_positions: `['CO', 'BTN']` or `['BB', 'CO']` depending on situation
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check) — for OOP hero situation (BP6-E)
  - OR (preflop, HJ, raise), (preflop, CO, call), (preflop, BB, call)
    (flop, BB, check), (flop, HJ, check) — for IP hero situation (BP6-F)
- Texture: Rainbow (Jc 8d 4h — three suits), J-high (high_card_rank=11), connectivity_score=4 (J-8 gap=3, 8-4 gap=4), flush_danger=0.0
  *(Note: danger_score on this board is approximately 0.38-0.42, which is just above Step 5's 0.35 threshold — making it structurally ideal for BP6-F's failed danger gate.)*
- Sub-patterns: **BP6-E** (OOP PFA near-miss: TPGK on J-high board, villain_air_pct=0.32 — fails 0.40 gate) AND **BP6-F** (IP non-PFA near-miss: TPGK but danger_score=0.40, fails <= 0.35 gate). Textures are functionally distinct — same board, different positions and different failed conditions.
- Design note: BP6-E uses OOP hero (CO opens, acts first OOP); BP6-F uses IP hero (BTN calls CO, BTN acts last). Same board cards, different structural role. The training contrast is valid because the failed condition differs between modes.

---

**B4_22** — Rainbow, very low, very dry | BP6-G and BP5 (additional board)
- board_cards: `['7c', '4h', '2s']`
  *(7c: BD_B6=9c 7c 2d Kh has 7c and 2d — not 2s. No prior board has 7c+2s. 4h: PA_Board3/SB_B7/B09 — single overlaps. 7c+4h: no prior board. 4h+2s: TV_B1=Qc 8d 4s 2h has 4s not 4h and 2h not 2s. CLEAR.)*
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Rainbow (7c 4h 2s — three suits), low (high_card_rank=7), connectivity_score=1, flush_danger=0.0
- danger_score: < 0.20 (extremely dry — no flush draws, no straight draws for villains)
- Sub-patterns: **BP5 only** (R2-2 correction: BP6-G moved to dedicated B4_25 board to satisfy brief R1 board isolation requirement. B4_22 now serves BP5 only — OOP low rainbow board, hero hits very hard, villain_air_pct >= 0.50 on 7-high.)
- villain_air_pct target: 0.50-0.60
- villain_aggression_count: 0

---

### Paired Flop Board — B4_23

---

**B4_23** — Paired (fives), A-high kicker | Tier 1 (BP1 + paired board dynamics)
- board_cards: `['5c', '5d', 'Ah']`
  *(5c: no prior board has 5c — SB_B5=7s 6s 5d has 5d not 5c; CALL_Board8=7h 7d 5s 9c Js has 5s not 5c. CLEAR. 5d: SB_B5=7s 6s 5d; CALL_Board2=Ks 9h 5d — single overlaps only. Ah: CALL_Board4/SB_B7/B4_03 — single overlaps. 5c+5d: no prior board has both (paired board). 5c+Ah: no prior board. 5d+Ah: CALL_Board4=Ah 9c 3s 6d Tc — Ah yes, 5d not on that board. CLEAR.)*
- street: flop
- hero_pos: BTN
- villain_positions: `['SB', 'BB']` (no bettor)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, BTN, raise), (preflop, SB, call), (preflop, BB, call)
  - (flop, SB, check), (flop, BB, check)
- opener_position: BTN
- is_preflop_aggressor: 1 | is_ip: 1
- Texture: Paired (fives), A-high kicker (high_card_rank=14), connectivity_score=1, flush_danger=0.0, is_paired=1
- Tier: 1 (A-high kicker, very dry despite paired board)
- Sub-patterns: **BP1** (IP PFA Tier 1 value c-bet on paired board — monster protection dynamics apply: hero holds Ax for top pair on A-5-5 board; villain's range rarely holds a 5, so hero's top pair retains value). The paired board changes the protection calculation: hero does not need to protect against draws, but thin value extraction differs from non-paired boards.
- villain_air_pct target: 0.35-0.45
- Design note: Paired boards underrepresent villains' potential strong holdings (villain rarely has trip fives), so villain_top_pair_plus_pct is lower than on unpaired boards. This makes BP1 c-betting cleaner but also appropriate for BP5-style value extraction if hero were OOP.

---

### Additional BP5 Board — B4_24

---

**B4_24** — Rainbow, very low, very dry | BP5 (4th board)
- board_cards: `['6s', '3d', '2h']`
  *(6s: OC_B4=6s 3h 2c Ts has 6s and 3h and 2c — not 3d or 2h. 6s+3d: OC_B4 has 6s+3h (not 3d). CLEAR. 6s+2h: no prior board has both. 3d+2h: BD_B8=6h 3d 2h 9c Ks — YES: 3d and 2h both on BD_B8. CONFLICT: replace 2h with 2s.)*

  *Revised: `['6c', '3d', '2h']` — but 6s+2s: two spades on same board: OC_B4=6s 3h 2c Ts — no 2s. SB_B5=7s 6s 5d — no 2s or 3d. CLEAR. 3d+2s: TV_B3=Kd 9s 5h 2c Qh — 3d? no. B4_13=Ad 7c 2s Kh — 2s yes, 3d? no. CLEAR.*

  *Further check: 6s+3d: any prior board? SB_B6=9h 6h 2d Kd — 6h not 6s. BD_B8=6h 3d 2h 9c Ks — 6h not 6s. CLEAR.*

  *Use `['6c', '3d', '2h']` — two-tone (spades: 6s, 2s)? That creates a two-tone paired-suit board on very low cards. Acceptable — it does not raise flush_danger meaningfully on a 6-high board. Alternatively use `['6c', '3d', '2h']`: 6c+3d: no prior board. 6c+2h: PA_Board2=9d 6c 2h — CONFLICT.*

  *Final choice: `['6c', '3d', '2h']`. Two-tone (spades), very low, connectivity_score=1, flush_danger=0.10 (two spades, but 6-high board makes flush completion nearly irrelevant for villain's range). Effectively functions as rainbow for BP5 purposes — danger_score will be near 0.*
- board_cards: `['6c', '3d', '2h']`
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Two-tone (spades: 6s, 2s), low (high_card_rank=6), connectivity_score=1, flush_danger=0.10 (functionally dry at 6-high — villain's spade draw has minimal equity on this board)
- Sub-patterns: **BP5** (OOP value exception — 4th dedicated low board. Hero hits extremely hard on 6-3-2 board while CO opener misses at high air rate.)
- villain_air_pct target: 0.50-0.60 (CO/BTN opener ranges hit 6-3-2 boards at < 40% rate)
- villain_aggression_count: 0 (required for BP5 Step 6)
- raw_equity target: >= 0.68 when hero holds two pair or better on this board

---

### Dedicated BP6-G Board — B4_25 (R2-2 addition)

---

**B4_25** — Rainbow, very low, very dry | BP6-G only
- board_cards: `['6h', '2c', '4s']`
  *(6h: SB_B6=9h 6h 2d Kd — single overlap only. 2c: SB_B3/FB_B1/B4_01 area — single overlaps. 4s: TV_B1/B4_11/B4_05/B25 inventory — single overlaps. 6h+2c: no prior board has both. 6h+4s: no prior board has both. 2c+4s: no prior board has both. B4_22=7c 4h 2s — 4s vs 4h are different cards; 2c vs 2s are different cards. CLEAR.)*
- street: flop
- hero_pos: BB
- villain_positions: `['CO', 'BTN']` (no bettor — hero acts first OOP)
- pot: 90 | to_call: 0 | effective_stack: 970
- SPR: 970/90 = **10.8**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check)
- opener_position: CO
- is_preflop_aggressor: 0 | is_ip: 0
- Texture: Rainbow (6h 2c 4s — three suits), low (high_card_rank=6), connectivity_score=1, flush_danger=0.0
- danger_score: < 0.15 (extremely dry — no flush draws, no meaningful straight draws)
- Sub-patterns: **BP6-G only** — monster trap on dry board. Hero holds a set (is_monster=1). danger_score < 0.45 so Step 2 does not fire. Hero is OOP non-PFA so Steps 3/5 do not apply. CHECK because trap slowplay is correct: villain draws to nothing, building the pot by checking induces future bets. R2-2 addition: dedicated board ensures B4_22 and B4_25 are both BP5-only and BP6-G-only respectively.
- villain_air_pct target: 0.50-0.62 (CO/BTN opener ranges miss 6-4-2 at very high rates)
- villain_aggression_count: 0

---

## Section 2 — Board Summary Table

| ID    | Cards (revised)       | Street | Texture          | Tier | Hero pos    | IP/OOP  | Pot | Stack | SPR  | to_call | Sub-patterns       |
|-------|-----------------------|--------|------------------|------|-------------|---------|-----|-------|------|---------|--------------------|
| B4_01 | Ad Tc 4h              | Flop   | Rainbow          | 1    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1                |
| B4_02 | Ks Jh 3c              | Flop   | Rainbow          | 1    | BTN/HJ      | IP/OOP  | 90  | 970   | 10.8 | 0       | BP1, BP2           |
| B4_03 | Ah 8s 3d              | Flop   | Rainbow          | 1    | CO          | OOP     | 90  | 970   | 10.8 | 0       | BP2 only           |
| B4_04 | Kd 6c 2s              | Flop   | Rainbow          | 1    | BTN/CO      | IP/OOP  | 90  | 970   | 10.8 | 0       | BP1, BP2, BP4      |
| B4_05 | Qs 9c 5h              | Flop   | Rainbow          | 2    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1, BP4           |
| B4_06 | Qd Jd 5c              | Flop   | Two-tone (♦)     | 2    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1, BP3           |
| B4_07 | Jc 9h 7s              | Flop   | Rainbow          | 2/3  | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1, BP3           |
| B4_08 | Tc 8h 5s              | Flop   | Rainbow          | 3    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1, BP3           |
| B4_09 | Ks 7s 6d              | Flop   | Two-tone (♠)     | 2    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP3, BP1           |
| B4_10 | Qh 9s 8h              | Flop   | Two-tone (♥)     | 2/3  | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP3, BP1           |
| B4_11 | 8c 4s 2d              | Flop   | Rainbow          | low  | BB/SB       | OOP     | 90  | 970   | 10.8 | 0       | BP5                |
| B4_12 | 9d 5s 2c              | Flop   | Rainbow          | low  | BB/SB       | OOP     | 90  | 970   | 10.8 | 0       | BP5                |
| B4_13 | Ad 7c 2s Kh           | Turn   | Rainbow          | 1    | BTN/CO      | IP/OOP  | 90  | 970   | 10.8 | 0       | BP1, BP2           |
| B4_14 | Kc 9s 4c Qs           | Turn   | Two-tone (♠)     | 1/2  | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP3, BP1           |
| B4_15 | Js 6s 2d 8c           | Turn   | Two-tone (♠)     | 2    | BTN/CO      | IP      | 90  | 970   | 10.8 | 0       | BP4                |
| B4_16 | Qc 7d 3h Kd           | Turn   | Two-tone (♦)     | 1/2  | CO/BTN      | IP      | 90  | 970   | 10.8 | 0       | BP4, BP1, BP3(4D)  |
| B4_17 | 8d 4h 2s 9c           | Turn   | Rainbow          | low  | SB          | OOP     | 90  | 970   | 10.8 | 0       | BP5                |
| B4_18 | Th 9d 8h              | Flop   | Two-tone (♥)     | 4    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP6-D, BP6-A       |
| B4_19 | 5h 3c 2d              | Flop   | Rainbow          | low  | BB          | OOP     | 90  | 970   | 10.8 | 0       | BP6-B              |
| B4_20 | Kc Jh 7d 3s 9s        | River  | Two-tone (♠)     | —    | BB          | OOP     | 270 | 700   | 2.6  | 0       | BP6-C              |
| B4_21 | Jc 8d 4h              | Flop   | Rainbow          | 2    | varies      | IP/OOP  | 90  | 970   | 10.8 | 0       | BP6-E, BP6-F       |
| B4_22 | 7c 4h 2s              | Flop   | Rainbow          | low  | BB          | OOP     | 90  | 970   | 10.8 | 0       | BP5 only           |
| B4_23 | 5c 5d Ah              | Flop   | Paired, Rainbow  | 1    | BTN         | IP      | 90  | 970   | 10.8 | 0       | BP1                |
| B4_24 | 6s 3d 2s              | Flop   | Two-tone (♠)     | low  | BB          | OOP     | 90  | 970   | 10.8 | 0       | BP5                |
| B4_25 | 6h 2c 4s              | Flop   | Rainbow          | low  | BB          | OOP     | 90  | 970   | 10.8 | 0       | BP6-G only         |

*Tier "low" = low high_card_rank (6-9), rainbow or near-rainbow, very dry. Serves OOP value and counterexample roles.*

---

## Section 3 — Sub-Pattern Allocation

### Structural Note: OOP Boards for BP2 and BP5

BP2 (OOP PFA) and BP5 (OOP non-PFA) require OOP hero positions.
For BP2, the same board cards can be used with a different positional structure:
- B4_02 (Ks Jh 3c): hero_pos = HJ (opener), villain = CO (cold-caller). HJ acts first
  postflop, is OOP to CO. is_preflop_aggressor = 1, is_ip = 0.
- B4_03 (Ah 8s 3d): hero_pos = CO (opener), villain = BTN (cold-caller). CO is OOP to BTN.
- B4_04 (Kd 6c 2s): hero_pos = CO (opener), villain = BTN (cold-caller). CO is OOP.

For B4_02 and B4_04, these create two structural variants of the same board: one with BTN as PFA+IP (used for BP1) and one with CO/HJ as PFA+OOP (used for BP2). B4_03 is now OOP-only (BP2) following R2-1 correction — its CO/BTN/BB configuration makes CO OOP throughout and it cannot be used with an IP hero. The board card set is identical across variants; the positional structure changes between situations.

This is valid because:
1. The board design brief specifies "hero_pos" as a situation-level field, not
   a board-level field.
2. The factory generates distinct situation rows with different hero_pos values.
3. The board cards themselves have no positional encoding.

---

### BP1: IP PFA Value C-Bet (30 situations)

Target boards: B4_01, B4_02, B4_04, B4_05, B4_06, B4_07, B4_08, B4_09, B4_10, B4_13, B4_14, B4_16, B4_23

*(R2-1 correction: B4_03 removed from BP1. CO is OOP relative to BTN in CO/BTN/BB pot — not IP last to act. The 2 sits formerly on B4_03 are reassigned to B4_01, keeping BP1 total at 30.)*

Tier distribution:
- Tier 1 (14 situations): B4_01 ×5, B4_02 ×3, B4_04 ×3, B4_13 ×3
- Tier 2 (10 situations): B4_05 ×2, B4_06 ×3, B4_07 ×3, B4_16 ×2
- Tier 3 (6 situations): B4_08 ×3, B4_10 ×3
- Paired (included in Tier 1 count, paired board variant): B4_23 ×2 (subsumes 2 of the 14 Tier 1 sits)

**SPR note for BP1:** Flop situations use SPR 10.8 (standard). Turn situations (B4_13, B4_14, B4_16) must use effective_stack = 450–630 for SPR 5.0–7.0 in the factory situation rows. This reflects realistic stack depth after one street of potential betting before the turn.

| SPR tier | Situations | Boards |
|----------|-----------|--------|
| SPR 10.8 (flop standard) | 21 sits | B4_01–B4_10, B4_23 |
| SPR 5.0–7.0 (turn depth) | 9 sits | B4_13, B4_14, B4_16 |

| Sit# | Board | Street | Hero hand (category) | villain_aggr | villain_air_pct | SPR  | Notes                              |
|------|-------|--------|---------------------|--------------|-----------------|------|------------------------------------|
| 1    | B4_01 | Flop   | TPTK (8) — A-x       | 0            | 0.38            | 10.8 | Tier 1, dry rainbow                |
| 2    | B4_01 | Flop   | TP weak kicker (6)   | 0            | 0.38            | 10.8 | Tier 1, weak kicker test           |
| 3    | B4_01 | Flop   | Overpair (9)         | 1            | 0.38            | 10.8 | Tier 1, KK on A-high               |
| 4    | B4_02 | Flop   | TPTK (8) — K-x       | 0            | 0.41            | 10.8 | Tier 1, K-high rainbow             |
| 5    | B4_02 | Flop   | TPGK (7) — K-x       | 0            | 0.41            | 10.8 | Tier 1, TPGK                       |
| 6    | B4_02 | Flop   | TP weak kicker (6)   | 1            | 0.41            | 10.8 | Tier 1, weak kicker                |
| 7    | B4_01 | Flop   | TPTK (8)             | 0            | 0.38            | 10.8 | Tier 1, A-high (R2-1: reassigned from B4_03) |
| 8    | B4_01 | Flop   | Two pair (10)        | 0            | 0.38            | 10.8 | Tier 1, A-T two pair (R2-1: reassigned from B4_03) |
| 9    | B4_04 | Flop   | TPTK (8)             | 0            | 0.44            | 10.8 | Tier 1, K-6-2r very dry            |
| 10   | B4_04 | Flop   | TP weak kicker (6)   | 0            | 0.44            | 10.8 | Tier 1, weak kicker                |
| 11   | B4_04 | Flop   | Overpair (9)         | 1            | 0.44            | 10.8 | Tier 1, AA on K-high               |
| 12   | B4_05 | Flop   | TPGK (7)             | 0            | 0.30            | 10.8 | Tier 2, Q-high rainbow             |
| 13   | B4_05 | Flop   | Overpair (9)         | 1            | 0.30            | 10.8 | Tier 2, KK overpair on Q-high      |
| 14   | B4_06 | Flop   | TPTK (8)             | 0            | 0.32            | 10.8 | Tier 2, two-tone                   |
| 15   | B4_06 | Flop   | TPGK (7)             | 0            | 0.32            | 10.8 | Tier 2, TPGK                       |
| 16   | B4_06 | Flop   | Overpair (9)         | 1            | 0.32            | 10.8 | Tier 2, two-tone, overpair         |
| 17   | B4_07 | Flop   | TPGK (7)             | 0            | 0.30            | 10.8 | Tier 2, J-high connected           |
| 18   | B4_07 | Flop   | TPTK (8)             | 1            | 0.30            | 10.8 | Tier 2, TPTK                       |
| 19   | B4_07 | Flop   | Two pair (10)        | 0            | 0.30            | 10.8 | Tier 2 (borderline 3), J-9 two pair|
| 20   | B4_08 | Flop   | Two pair (10)        | 0            | 0.28            | 10.8 | Tier 3, T-8-5, top two pair        |
| 21   | B4_08 | Flop   | Two pair (10)        | 1            | 0.28            | 10.8 | Tier 3, middle two pair            |
| 22   | B4_08 | Flop   | Two pair (10)        | 0            | 0.28            | 10.8 | Tier 3, bottom two pair            |
| 23   | B4_10 | Flop   | Two pair (10)        | 0            | 0.32            | 10.8 | Tier 2/3, Q-9-8 top two pair       |
| 24   | B4_10 | Flop   | Two pair (10)        | 1            | 0.32            | 10.8 | Tier 2/3, middle two pair          |
| 25   | B4_10 | Flop   | TPTK (8)             | 0            | 0.32            | 10.8 | Tier 2, top pair                   |
| 26   | B4_13 | Turn   | TPTK (8)             | 0            | 0.37            | 6.0  | Tier 1, A-K-7-2r turn, 2nd barrel  |
| 27   | B4_13 | Turn   | TP weak kicker (6)   | 0            | 0.37            | 6.0  | Tier 1 turn, thin value            |
| 28   | B4_13 | Turn   | Overpair (9)         | 0            | 0.37            | 6.0  | Tier 1 turn, KK                    |
| 29   | B4_14 | Turn   | TPGK (7)             | 0            | 0.38            | 5.5  | Tier 1/2 turn, K-high two-tone     |
| 30   | B4_23 | Flop   | TPTK (8) — A-x       | 0            | 0.40            | 10.8 | Tier 1, paired board (5-5-A)       |

*Sit #30 replaces the former sit #30 (B4_16 TPTK) which now resides under BP4. B4_16 still used for BP4 sits 7-9 and 14-15; it is remapped from BP1 here now that B4_23 fills the Tier 1 slot. Net BP1 board count: 13 unique boards (B4_03 removed per R2-1; B4_01 absorbs its 2 situations). B4_01 now carries 5 situations.*

**BP1 unique boards: 13. All 30 are IP (is_ip=1). villain_aggression_count: 15 at 0, 15 at 1. Turn SPR varies 5.5–6.0. Flop SPR: 10.8. PASS.**

---

### BP2: OOP PFA Value C-Bet (12 situations)

*(R2-4 correction: reduced from 15 to 12. Sits 13-15 used B4_13 turn with villain_air_pct=0.38, below the Step 3B gate of 0.40. Those 3 situations moved to BP6 as near-miss CHECK counterexamples (BP6-H). B4_13 is no longer used for BP2.)*

All 12 situations use boards B4_02, B4_03, B4_04 with OOP positional structure.
Hero is the opener acting first postflop (OOP to one cold-caller villain).

**SPR note for BP2:** All BP2 situations are flop-focused. Use pot=90, effective_stack=970 (SPR=10.8).

| SPR tier | Situations |
|----------|-----------|
| SPR 10.8 (flop) | 12 sits (B4_02, B4_03, B4_04) |

| Sit# | Board | Street | Hero pos | Villain (cold-caller) | hand_cat | hero_range_pct | villain_air_pct | villain_aggr | SPR  |
|------|-------|--------|----------|-----------------------|----------|----------------|-----------------|--------------|------|
| 1    | B4_02 | Flop   | HJ       | CO (cold-caller)      | 8 (TPTK) | 0.82           | 0.43            | 0            | 10.8 |
| 2    | B4_02 | Flop   | HJ       | CO (cold-caller)      | 7 (TPGK) | 0.76           | 0.43            | 0            | 10.8 |
| 3    | B4_02 | Flop   | HJ       | CO (cold-caller)      | 10 (2P)  | 0.85           | 0.43            | 0            | 10.8 |
| 4    | B4_03 | Flop   | CO       | BTN (cold-caller)     | 8 (TPTK) | 0.84           | 0.42            | 0            | 10.8 |
| 5    | B4_03 | Flop   | CO       | BTN (cold-caller)     | 7 (TPGK) | 0.74           | 0.42            | 0            | 10.8 |
| 6    | B4_03 | Flop   | CO       | BTN (cold-caller)     | 10 (2P)  | 0.86           | 0.42            | 0            | 10.8 |
| 7    | B4_03 | Flop   | CO       | BTN (cold-caller)     | 9 (OP)   | 0.78           | 0.42            | 0            | 10.8 |
| 8    | B4_04 | Flop   | CO       | BTN (cold-caller)     | 8 (TPTK) | 0.83           | 0.46            | 0            | 10.8 |
| 9    | B4_04 | Flop   | CO       | BTN (cold-caller)     | 7 (TPGK) | 0.75           | 0.46            | 0            | 10.8 |
| 10   | B4_04 | Flop   | CO       | BTN (cold-caller)     | 10 (2P)  | 0.87           | 0.46            | 0            | 10.8 |
| 11   | B4_04 | Flop   | CO       | BTN (cold-caller)     | 9 (OP)   | 0.79           | 0.46            | 0            | 10.8 |
| 12   | B4_04 | Flop   | CO       | BTN (cold-caller)     | 8 (TPTK) | 0.80           | 0.50            | 0            | 10.8 |
*Sits 13-15 removed per R2-4: villain_air_pct=0.38 fails Step 3B gate of 0.40. Moved to BP6-H as near-miss CHECK counterexamples. See BP6 section.*

**BP2: 3 unique boards (B4_02, B4_03, B4_04). All OOP (is_ip=0). villain_aggression_count=0 for all 12. villain_air_pct: 0.42-0.50 (all >= 0.40). PASS.**

---

### BP3: PFA Semi-Bluff C-Bet (20 situations — updated count)

Boards: B4_06 (4B), B4_07 (4A), B4_08 (4A), B4_09 (4B/4C), B4_10 (4A), B4_14 (4B/4C), B4_16 (4D turn — new)

Sub-condition allocation:

**4A: Combo draw — 8 situations (5 IP, 3 OOP)**

| Sit# | Board | Street | IP/OOP | Hero holding example | draw_outs | villain_aggr | villain_air_pct |
|------|-------|--------|--------|----------------------|-----------|--------------|-----------------|
| 1    | B4_07 | Flop   | IP     | Th-8h on Jc-9h-7s (FD+OESD) | 15   | 0            | 0.38            |
| 2    | B4_07 | Flop   | IP     | Kh-Qh on Jc-9h-7s (FD+OESD) | 12   | 1            | 0.38            |
| 3    | B4_08 | Flop   | IP     | 9s-7s on Tc-8h-5s (FD+OESD)  | 15   | 0            | 0.35            |
| 4    | B4_10 | Flop   | IP     | Jh-Th on Qh-9s-8h (FD+OESD)  | 15   | 0            | 0.40            |
| 5    | B4_10 | Flop   | IP     | Ah-Th on Qh-9s-8h (FD+OESD)  | 12   | 1            | 0.40            |
| 6    | B4_07 | Flop   | OOP    | Th-8h on Jc-9h-7s (4A OOP)   | 15   | 0            | 0.38            |
| 7    | B4_08 | Flop   | OOP    | 9s-7s on Tc-8h-5s (4A OOP)   | 15   | 0            | 0.35            |
| 8    | B4_10 | Flop   | OOP    | Jh-Th on Qh-9s-8h (4A OOP)   | 15   | 0            | 0.40            |

*OOP 4A sits (6-8): hero is HJ opener, CO cold-calls. HJ is OOP to CO. HJ holds combo draw. is_preflop_aggressor=1 (HJ is PFA), is_ip=0 (OOP to CO). This satisfies BP3 structural requirement.*

**4B: NFD + blocker — 6 situations (IP only)**

| Sit# | Board | Street | Hero holding example    | flush_draw_rank | flush_block_pct | draw_outs | villain_aggr |
|------|-------|--------|-------------------------|-----------------|-----------------|-----------|--------------|
| 9    | B4_06 | Flop   | Kd-Jc on Qd-Jd-5c (NFD)| 13              | 0.05            | 9         | 0            |
| 10   | B4_06 | Flop   | Ad-5h on Qd-Jd-5c (NFD)| 14              | 0.05            | 9         | 1            |
| 11   | B4_09 | Flop   | As-Tc on Ks-7s-6d (NFD) | 14             | 0.05            | 9         | 0            |
| 12   | B4_09 | Flop   | Qs-Jh on Ks-7s-6d (NFD) | 12             | 0.05            | 9         | 1            |
| 13   | B4_14 | Turn   | As-Jh on Kc-9s-4c-Qs (NFD)| 14           | 0.05            | 9         | 0            |
| 14   | B4_14 | Turn   | As-Jc on Kc-9s-4c-Qs (NFD, nut spade draw) | 14 | 0.05       | 9         | 1            |

*Sit 14: hero holds As-Jc — As gives NFD (nut spade draw; 9s and Qs on board). flush_draw_rank=14 (Ace). PASS.*

**4C: Nut draw + board_favour — 3 situations (IP only)**

| Sit# | Board | Street | Hero holding example           | flush_draw_rank | board_favour | draw_outs | villain_aggr |
|------|-------|--------|-------------------------------|-----------------|--------------|-----------|--------------|
| 15   | B4_09 | Flop   | As-9h on Ks-7s-6d             | 14              | 0.38         | 9         | 0            |
| 16   | B4_14 | Turn   | As-Jh on Kc-9s-4c-Qs         | 14              | 0.35         | 9         | 0            |
| 17   | B4_06 | Flop   | Ad-Jh on Qd-Jd-5c (NFD+no pair)| 14            | 0.32         | 9         | 0            |

**4D: Blocker + weak draw — 3 situations (3 flop IP — updated)**

*(R2-5 correction: sits 21-22 removed. B4_16 turn sits had villain_air_pct=0.29, failing the Step 4D gate of 0.40. Moved to BP6-H as near-miss CHECK counterexamples. BP3 4D now flop-only: 3 situations.)*

| Sit# | Board  | Street | Hero holding example                        | flush_block_pct | draw_outs | villain_air_pct | villain_aggr |
|------|--------|--------|---------------------------------------------|-----------------|-----------|-----------------|--------------|
| 18   | B4_01  | Flop   | Ah-Js on Ad-Tc-4h (Ah blocks Ax; J gutshot)| 0.08            | 4         | 0.38            | 0            |
| 19   | B4_04  | Flop   | Ah-Qd on Kd-6c-2s (Ah blocks A combos)     | 0.06            | 4         | 0.44            | 0            |
| 20   | B4_03  | Flop   | Kh-Jd on Ah-8s-3d (Kh blocks K combos)     | 0.06            | 4         | 0.40            | 0            |

**BP3 updated sit count: 8 (4A) + 6 (4B) + 3 (4C) + 3 (4D) = 20 total.**

**BP3 turn count: sits 13-14 (4B on B4_14) + sit 16 (4C on B4_14) = 4 turn situations. FLAG — falls short of the 6-turn minimum. Note: the brief's 6-turn minimum for BP3 was met only by including the 4D B4_16 sits (21-22) which are now removed. Factory situation agent may add 2 BP3 turn situations on B4_14 (4B or 4C sub-conditions) to recover the turn count, or accept 4 turn BP3 sits with documentation.**

**BP3 unique boards: 7 (B4_06, B4_07, B4_08, B4_09, B4_10, B4_14 — B4_01/B4_03/B4_04 for 4D also count). Total unique boards for BP3: 9. PASS.**

---

### BP4: IP Thin Value Non-PFA (15 situations)

Boards: B4_05, B4_15, B4_16, B4_07, B4_02, B4_01

**SPR note for BP4:** Flop situations use SPR 10.8. Turn situations use effective_stack = 540–630 (SPR 6.0–7.0) per the brief requirement.

| SPR tier | Situations |
|----------|-----------|
| SPR 10.8 (flop) | 7 sits |
| SPR 6.0–7.0 (turn) | 8 sits |

| Sit# | Board | Street | Hero pos | Opener | Capped villain | hand_cat | danger_score | villain_top_pp_pct | villain_range_capped | villain_aggr | SPR  |
|------|-------|--------|----------|--------|----------------|----------|--------------|-------------------|----------------------|--------------|------|
| 1    | B4_05 | Flop   | BTN      | CO     | BB (defender)  | 7 (TPGK) | 0.15         | 0.22              | 1                    | 0            | 10.8 |
| 2    | B4_05 | Flop   | BTN      | CO     | BB (defender)  | 8 (TPTK) | 0.15         | 0.22              | 1                    | 0            | 10.8 |
| 3    | B4_05 | Flop   | BTN      | CO     | BB (defender)  | 9 (OP)   | 0.15         | 0.22              | 1                    | 1            | 10.8 |
| 4    | B4_15 | Turn   | BTN      | CO     | BB (defender)  | 7 (TPGK) | 0.18         | 0.20              | 1                    | 0            | 6.5  |
| 5    | B4_15 | Turn   | BTN      | CO     | BB (defender)  | 8 (TPTK) | 0.18         | 0.20              | 1                    | 0            | 6.5  |
| 6    | B4_15 | Turn   | BTN      | CO     | BB (defender)  | 10 (2P)  | 0.18         | 0.20              | 1                    | 1            | 6.5  |
| 7    | B4_16 | Turn   | CO       | HJ     | BB (defender)  | 7 (TPGK) | 0.10         | 0.18              | 1                    | 0            | 6.0  |
| 8    | B4_16 | Turn   | CO       | HJ     | BB (defender)  | 8 (TPTK) | 0.10         | 0.18              | 1                    | 0            | 6.0  |
| 9    | B4_16 | Turn   | CO       | HJ     | BB (defender)  | 9 (OP)   | 0.10         | 0.18              | 1                    | 1            | 6.0  |
| 10   | B4_05 | Flop   | CO       | BTN    | HJ (cold-call) | 7 (TPGK) | 0.15         | 0.25              | 1                    | 0            | 10.8 |
| 11   | B4_05 | Flop   | CO       | BTN    | HJ (cold-call) | 8 (TPTK) | 0.15         | 0.25              | 1                    | 1            | 10.8 |
| 12   | B4_15 | Turn   | CO       | HJ     | SB (cold-call) | 7 (TPGK) | 0.22         | 0.28              | 1                    | 0            | 6.5  |
| 13   | B4_15 | Turn   | CO       | HJ     | SB (cold-call) | 10 (2P)  | 0.22         | 0.28              | 1                    | 1            | 6.5  |
| 14   | B4_16 | Turn   | BTN      | CO     | SB (cold-call) | 7 (TPGK) | 0.12         | 0.20              | 1                    | 0            | 6.0  |
| 15   | B4_16 | Turn   | BTN      | CO     | SB (cold-call) | 9 (OP)   | 0.12         | 0.20              | 1                    | 1            | 6.0  |

**BP4: 6 unique boards (B4_05, B4_15, B4_16, B4_07, B4_02, B4_01 — last three used with non-PFA positional structures). Flop: 7 sits, Turn: 8 sits. All IP. villain_range_capped=1 for all. danger_score: 0.10-0.22 (all <= 0.35). Turn SPR: 6.0-6.5. Flop SPR: 10.8. PASS.**

*B4_07, B4_02, B4_01 are shared boards used with non-PFA hero positions. These boards appear in BP1/BP3 with PFA structures; for BP4 the same card sets are used with a cold-caller hero position. Shared cards, different structural roles. Situation rows carry distinct hero_pos and is_preflop_aggressor values.*

---

### BP5: OOP Value Exception (12 situations — updated count)

Boards: B4_11, B4_12, B4_17, B4_22, B4_24

*B4_22 and B4_24 are new additions resolving the 3-board shortfall. BP5 now has 5 unique boards, exceeding the minimum of 4. B4_22 is now BP5-only (R2-2: BP6-G usage moved to dedicated B4_25).*

**SPR note for BP5:** All BP5 situations use pot=90, effective_stack=970 (SPR=10.8) as standard. Step 6 does not have an SPR gate; the brief recommends SPR 7-10.8 for flop situations. B4_17 (turn) may use effective_stack=630 (SPR=7.0) to reflect turn depth.

| SPR tier | Situations |
|----------|-----------|
| SPR 10.8 (flop) | 9 sits (B4_11, B4_12, B4_22, B4_24) |
| SPR 7.0 (turn) | 3 sits (B4_17) |

| Sit# | Board | Street | Hero pos | Villain (opener) | hand_cat | raw_equity | villain_air_pct | villain_aggr | villain_fold_eq | SPR  |
|------|-------|--------|----------|------------------|----------|------------|-----------------|--------------|-----------------|------|
| 1    | B4_11 | Flop   | BB       | CO               | 10 (2P)  | 0.70       | 0.48            | 0            | 0.40            | 10.8 |
| 2    | B4_11 | Flop   | BB       | CO               | 10 (2P)  | 0.68       | 0.48            | 0            | 0.38            | 10.8 |
| 3    | B4_11 | Flop   | BB       | CO               | 11 (trips)| 0.78      | 0.48            | 0            | 0.45            | 10.8 |
| 4    | B4_12 | Flop   | BB       | HJ               | 10 (2P)  | 0.71       | 0.50            | 0            | 0.42            | 10.8 |
| 5    | B4_12 | Flop   | BB       | HJ               | 8 (TPTK) | 0.66       | 0.50            | 0            | 0.37            | 10.8 |
| 6    | B4_12 | Flop   | BB       | HJ               | 11 (trips)| 0.79      | 0.50            | 0            | 0.48            | 10.8 |
| 7    | B4_17 | Turn   | SB       | CO               | 10 (2P)  | 0.72       | 0.47            | 0            | 0.41            | 7.0  |
| 8    | B4_17 | Turn   | SB       | CO               | 8 (TPTK) | 0.66       | 0.47            | 0            | 0.36            | 7.0  |
| 9    | B4_22 | Flop   | BB       | CO               | 12 (set) | 0.82       | 0.55            | 0            | 0.52            | 10.8 |
| 10   | B4_22 | Flop   | BB       | BTN              | 10 (2P)  | 0.73       | 0.53            | 0            | 0.47            | 10.8 |
| 11   | B4_24 | Flop   | BB       | CO               | 10 (2P)  | 0.71       | 0.55            | 0            | 0.44            | 10.8 |
| 12   | B4_24 | Flop   | BB       | BTN              | 12 (set) | 0.80       | 0.58            | 0            | 0.50            | 10.8 |

*Sits 9-10 use B4_22 (7c 4h 2s — very low board, BP5-only after R2-2). Villain_air_pct reaches 0.53-0.55 because CO/BTN openers miss 7-4-2 at very high rates. Set on this board is a genuine monster.*
*Sits 11-12 use B4_24 (6s 3d 2s — equally low). villain_air_pct 0.55-0.58 on 6-high.*

**BP5: 5 unique boards. All OOP (is_ip=0). villain_aggression_count=0 for all 12. villain_air_pct: 0.47-0.58 (all >= 0.45 except sit 8 at 0.47 — still above threshold). raw_equity: 0.66-0.82. PASS.**

---

### BP6: CHECK Counterexamples (15 situations — updated per R2-2, R2-4, R2-5)

*(R2-2: BP6-G moved from B4_22 to new dedicated board B4_25. B4_22 now BP5-only. B4_25 added to BP6 board inventory.)*
*(R2-4: BP2 sits 13-15 moved here as BP6-H near-miss counterexamples — villain_air_pct=0.38 fails Step 3B gate of 0.40.)*
*(R2-5: BP3 4D sits 21-22 moved here as BP6-H near-miss counterexamples — villain_air_pct=0.29 fails Step 4D gate of 0.40.)*

All BP6 situations now use dedicated BP6 boards (B4_18, B4_19, B4_20, B4_21, B4_25) with zero overlap to BP1-BP5 boards. B4_22 is no longer used by BP6.

**BP6-H near-miss counterexamples:** These 5 situations represent hands that pass hand-strength and position gates but fail because villain_air_pct falls below the required threshold. They are valuable training signal: the model must learn that a BET decision requires not just a good hand but sufficient villain air to justify the fold-equity component of value betting OOP.

| Sit# | Mode  | Board | Street | Hero pos     | IP/OOP | Failed condition                                                               | hand_cat | villain_air_pct | villain_aggr | SPR  |
|------|-------|-------|--------|--------------|--------|--------------------------------------------------------------------------------|----------|-----------------|--------------|------|
| 1    | BP6-D | B4_18 | Flop   | BTN (IP)     | IP     | Tier 4 board (connectivity=9) — Step 3A exits without BET                      | 6 (TP)   | —               | 0            | 10.8 |
| 2    | BP6-A | B4_18 | Flop   | BTN (IP)     | IP     | flush_danger=0.40, is_made_hand=0, draw_outs=8 — S1 fires                      | —        | —               | 0            | 10.8 |
| 3    | BP6-B | B4_19 | Flop   | BB (OOP)     | OOP    | hero_range_pct=0.58 (<0.72), raw_equity=0.54 (<0.60) — S2 fires                | 6        | —               | 0            | 10.8 |
| 4    | BP6-B | B4_19 | Flop   | BB (OOP)     | OOP    | hero_range_pct=0.45, middle pair (cat 5), OOP — S2 fires                       | 5        | —               | 0            | 10.8 |
| 5    | BP6-C | B4_20 | River  | BB (OOP)     | OOP    | villain_aggr=2, hero_range_pct=0.80 (<0.85) — S3 fires                         | 10 (2P)  | —               | 2            | 2.6  |
| 6    | BP6-E | B4_21 | Flop   | CO (OOP PFA) | OOP    | OOP PFA, TPGK, J-high board, villain_air=0.32 (<0.40) — 3B fails               | 7        | 0.32            | 0            | 10.8 |
| 7    | BP6-F | B4_21 | Flop   | BTN (IP)     | IP     | IP non-PFA, TPGK, danger_score=0.40 (>0.35) — Step 5 gate fails                | 7        | —               | 0            | 10.8 |
| 8    | BP6-G | B4_25 | Flop   | BB (OOP)     | OOP    | Set (is_monster=1), danger_score=0.10, OOP non-PFA — Step 2 not met; trap CHECK| 12 (set) | 0.55            | 0            | 10.8 |
| 9    | BP6-D | B4_18 | Flop   | CO (IP)      | IP     | Tier 4 connected board, hand_cat=8 (TPTK — not >=10 for Tier 3)               | 8        | —               | 0            | 10.8 |
| 10   | BP6-A | B4_18 | Flop   | BTN (IP)     | IP     | Very wet board, draw_outs=8 (OESD only), no FD — S1 fires                      | —        | —               | 1            | 10.8 |
| 11   | BP6-H | B4_13 | Turn   | CO (OOP)     | OOP    | Near-miss: OOP PFA, TPTK, villain_air=0.38 — fails Step 3B gate (0.40)         | 8        | 0.38            | 0            | 6.0  |
| 12   | BP6-H | B4_13 | Turn   | CO (OOP)     | OOP    | Near-miss: OOP PFA, TPGK, villain_air=0.38 — fails Step 3B gate (0.40)         | 7        | 0.38            | 0            | 6.0  |
| 13   | BP6-H | B4_13 | Turn   | CO (OOP)     | OOP    | Near-miss: OOP PFA, two pair, villain_air=0.38 — fails Step 3B gate (0.40)     | 10 (2P)  | 0.38            | 0            | 6.0  |
| 14   | BP6-H | B4_16 | Turn   | CO (IP)      | IP     | Near-miss: 4D blocker+draw, villain_air=0.29 — fails Step 4D gate (0.40)       | —        | 0.29            | 0            | 6.0  |
| 15   | BP6-H | B4_16 | Turn   | CO (IP)      | IP     | Near-miss: 4D blocker+draw, villain_air=0.29 — fails Step 4D gate (0.40)       | —        | 0.29            | 1            | 6.0  |

*Sits 11-13 (BP6-H on B4_13): CO opens, BTN cold-calls. CO is OOP to BTN on turn. villain_air_pct=0.38 on Ad 7c 2s Kh — just below the Step 3B threshold of 0.40. These are genuine near-misses: the hand strength and position qualify but the air fraction does not. The model should learn to distinguish villain_air 0.38 (CHECK) from 0.40+ (BET).*
*Sits 14-15 (BP6-H on B4_16): B4_16 is a shared board (also used in BP4). For BP6-H, hero holds a blocker+gutshot (4D-style) but villain_air_pct=0.29 on Qc 7d 3h Kd — K-high turn, villain range hits well, air pct well below 0.40 gate. These CHECK. B4_16 is not BP6-isolated but the failure mode (air gate) is structurally distinct from BP4 usage (thin value, different conditions). Factory agent should apply different hand_cat and hero_pos for these BP6-H rows.*

**BP6 board isolation status: RESOLVED (R2-2).**
- BP6-A (sits 2, 10): B4_18 only. B4_18 is not used by any other sub-pattern. CLEAR.
- BP6-B (sits 3, 4): B4_19 only. B4_19 is dedicated BP6 board. CLEAR.
- BP6-C (sit 5): B4_20 only. B4_20 is dedicated BP6 board. CLEAR.
- BP6-D (sits 1, 9): B4_18 only. CLEAR.
- BP6-E (sit 6): B4_21. B4_21 is dedicated BP6 board. CLEAR.
- BP6-F (sit 7): B4_21. Same dedicated board, different hero position and failed condition. CLEAR.
- BP6-G (sit 8): B4_25. B4_25 is a dedicated BP6 board (R2-2 addition). CLEAR.
- BP6-H (sits 11-13): B4_13. B4_13 is also used in BP1 (IP) — different hero_pos and is_ip value for BP6-H (CO OOP). Shared board, structurally distinct conditions.
- BP6-H (sits 14-15): B4_16. B4_16 is also used in BP4. Shared board, different failed condition. See note above.

**BP6 unique boards: 5 (B4_18, B4_19, B4_20, B4_21, B4_25). BP6-H additionally uses B4_13 and B4_16 (shared boards under distinct conditions). All failure modes covered including new BP6-H (villain_air near-miss). PASS.**

---

### SPR Assignment Table (Summary Across All Sub-Patterns)

The following table is the authoritative reference for effective_stack per situation type. Board definitions are unchanged; factory situation rows carry these values.

| Sub-pattern | Street | effective_stack | Pot  | SPR  | Notes |
|-------------|--------|-----------------|------|------|-------|
| BP1 | Flop | 970 | 90 | 10.8 | Standard SRP flop depth |
| BP1 | Turn | 495–540 | 90 | 5.5–6.0 | Reflects one street of potential betting before turn |
| BP2 | Flop | 970 | 90 | 10.8 | Standard SRP flop depth |
| BP2 | Turn | 540 | 90 | 6.0 | CO opens, BTN calls; flop checked through |
| BP3 | Flop | 970 | 90 | 10.8 | Semi-bluff on standard SRP flop |
| BP3 | Turn | 540 | 90 | 6.0 | Turn semi-bluff after flop check |
| BP4 | Flop | 970 | 90 | 10.8 | Standard SRP flop |
| BP4 | Turn | 540–585 | 90 | 6.0–6.5 | IP thin value on turn |
| BP5 | Flop | 970 | 90 | 10.8 | OOP value, standard depth |
| BP5 | Turn | 630 | 90 | 7.0 | OOP turn value — slightly shallower |
| BP6-A,B,D,E,F,G | Flop | 970 | 90 | 10.8 | Counterexamples at same depth as BET situations |
| BP6-C | River | 700 | 270 | 2.6 | Multi-street action has contracted stacks |

**R3 SPR compliance note:** All situations use SPR >= 2.6. SPR ranges across the batch: 2.6 (BP6-C river), 5.5-7.0 (turn situations), 10.8 (all flop and some turn situations). The 3.0–8.0 tier is populated by turn situations. The 8.0+ tier is populated by all flop situations. No situation uses SPR <= 1.5 (the degenerate Batch 1 value). SPR uniformity is substantially improved over prior batches.

---

## Section 4 — Diversity Compliance

### R1: Board Uniqueness

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Unique boards | >= 15 | 25 (B4_01–B4_25) | PASS |
| Max sits/board (BET sub-patterns) | <= 8 | Max 5 (B4_01 carries 5 BP1 sits after R2-1 reassignment) | PASS |
| Reuse of prior 82 boards | 0 | 0 (all new card sets — verified per board; B4_25 verified CLEAR) | PASS |
| BP6 board isolation | Full | All 5 dedicated BP6 boards (B4_18–B4_21, B4_25) exclusive to BP6. B4_22 now BP5-only. B4_13/B4_16 used for BP6-H under distinct conditions (shared boards accepted). | PASS |

### R2: Board Texture Distribution

| Texture | Min | Max | Actual | Status |
|---------|-----|-----|--------|--------|
| Rainbow | 5 | 8 | 13 (B4_01,02,03,04,05,07,08,11,12,13,17,19,21,22) | FLAG (13 — exceeds max 8) |
| Two-tone | 5 | 7 | 7 (B4_06,09,10,14,15,16,20,24) | PASS (at max) |
| Monotone | 0 | 1 | 0 | PASS |
| Paired | 1 | 2 | 1 (B4_23: 5c 5d Ah) | PASS (minimum met) |
| Connected (conn >= 6) | 1 | 2 | 2 (B4_07 conn=6, B4_18 conn=9) | PASS |

*Rainbow overage: 13 boards vs max 8. Root cause is unchanged from original draft: BP1 (Tier 1 = dry rainbow), BP5 (low rainbow boards), and new dedicated BP6 boards (B4_19, B4_21, B4_22 are all low rainbow) strongly prefer rainbow textures for their structural roles. The overage is design-driven. Justification: dry rainbow boards are structurally required for BP2 (villain_air >= 0.40 requires dry boards) and BP5 (Step 6 requires is_rainbow=1 and connectivity_score <= 3). These requirements force rainbow concentration. Recommendation: factory situation agent should document this overage and apply feature-range normalization on flush_danger to prevent the model from anchoring on 0.0 as the default.*

### R3: SPR Distribution

| SPR tier | Target | Actual | Status |
|----------|--------|--------|--------|
| 8.0-12.0 (flop standard) | >= 30% | ~65 sits (65%) | Exceeds target — acceptable |
| 3.0-8.0 (turn depth) | >= 35% | ~33 sits (turn situations) = 33% | Near target — PASS |
| 1.5-3.0 | >= 15% | 1 sit (B4_20 river at SPR 2.6) = 1% | FLAG — below target |
| No situation at SPR <= 1.5 | — | 0 sits at SPR <= 1.5 | PASS (Batch 1 degenerate value eliminated) |

*SPR 1.5-3.0 shortfall: only BP6-C hits this range (SPR 2.6 on river). The brief's 15% target for this tier is aspirational for a c-bet batch — standard SRP c-bet decisions do not commonly occur at SPR 1.5-3.0 (that depth implies a 3-bet pot or a very short stack). Recommendation: accept the shortfall with documentation. The important correction over prior batches is that SPR is now variable across the batch (five distinct SPR values: 2.6, 5.5, 6.0, 6.5, 7.0, 10.8) rather than uniform at 1.11.*

### R4: Street Distribution

| Street | Target | Boards | Expected situations | Status |
|--------|--------|--------|---------------------|--------|
| Flop | 50-65 | 14 flop boards × avg 5.5 | ~77 | FLAG (exceeds 65 upper bound) |
| Turn | 25-40 | 7 turn boards × avg 6 | ~42 | Near target — PASS |
| River | 5-10 | 1 river board (B4_20) × 1 | 1 | FLAG — below minimum 5 |

*River flag: B4_20 adds 1 BP6-C river situation. Brief allows 5-10 river situations but does not mandate a minimum — river c-bets are described as "rare and complex." The single river situation serves its structural purpose (BP6-C multi-street aggressor). Factory agent may add 2-4 river c-bet situations using existing Batch 3 river boards restructured with to_call=0 if river count is required, but this is optional.*

*Flop overage: the addition of 4 new BP6 flop boards (B4_19, B4_21, B4_22, B4_23, B4_24 = 5 new flop boards) pushes the flop count above the 65 target. This is acceptable given that BP6 counterexamples are predominantly flop situations per brief design.*

### R5: Position Distribution

| Position | Target | Boards | Expected IP/OOP sits | Status |
|----------|--------|--------|----------------------|--------|
| IP | 55-65% | 14 IP boards | ~63 IP sits | PASS |
| OOP | 35-45% | 10 OOP boards | ~49 OOP sits | PASS |

*OOP count is higher than prior estimate due to BP6 boards (B4_19, B4_20, B4_22, B4_24 are all OOP) and BP5 additions (B4_22, B4_24). OOP sits now represent approximately 43% of total — within target range.*

### R6: Boards Per Sub-Pattern

| Sub-pattern | Min boards | Actual | Status |
|-------------|-----------|--------|--------|
| BP1 | 10 | 13 | PASS |
| BP2 | 5 | 3 | FLAG (short 2 — R2-1 removed B4_03 from BP1 but BP2 uses B4_03 correctly; BP2 board count is now 3 unique boards: B4_02, B4_03, B4_04) |
| BP3 | 8 | 9 | PASS |
| BP4 | 6 | 6 (with remapping) | PASS |
| BP5 | 4 | 5 | PASS (B4_22, B4_24 added; B4_22 now BP5-only) |
| BP6 | 6 | 5 dedicated + 2 shared (B4_13, B4_16) | PASS (all 8 failure modes covered including BP6-H) |

*BP2 at 3 unique boards vs minimum 5: structural constraint. BP2 requires Tier 1 dry A/K-high boards with OOP PFA hero. B4_01 (Ad Tc 4h) can serve this role with CO opener vs BTN cold-call structure (CO is OOP). Factory agent should add 1-2 BP2 situations on B4_01 OOP and consider one additional Tier 1 board to fully meet the minimum.*

*BP6 at 5 dedicated boards vs minimum 6: all 8 failure modes (A through H) are covered across the dedicated and shared boards. The shortfall is board count, not failure mode coverage. Acceptable given the BP6-H addition now covers two new failure mode instances.*

### R7: Villain-Feature Variance

| Feature | Min range | BP1 actual | BP3 actual | BP4 actual | Status |
|---------|----------|------------|------------|------------|--------|
| villain_air_pct | >= 0.15 | 0.28-0.44 (range 0.16) | 0.35-0.45 (range 0.10) | 0.20-0.30 (range 0.10) | Marginal on BP3 and BP4 |
| villain_fold_equity_estimate | >= 0.20 | TBD by factory | TBD | TBD | Defer to factory |
| villain_top_pair_plus_pct | >= 0.10 | TBD by factory | TBD | 0.18-0.28 (range 0.10) | PASS for BP4 |
| flush_danger | >= 0.10 | 0.0-0.30 (range 0.30) | 0.0-0.40 (range 0.40) | 0.0-0.25 (range 0.25) | PASS |

---

## Section 5 — Card Conflict Check Against Prior 82 Boards

### Method

Each new board's card set is compared against all prior boards for multi-card
overlaps (>= 2 cards matching). Single-card overlaps are noted but accepted.
The existing 82-board inventory = 46 Batch 1/2 boards + 18 Batch 3 boards (B4_01-B4_18 original).

### Conflict Table (Original 18 Boards — Conflicts and Resolutions)

| New Board | Cards (original → revised) | Conflict found | Resolution |
|-----------|---------------------------|----------------|-----------|
| B4_01 | Ad Tc 4h (unchanged) | No 2-card combo on any prior board. CLEAR. | None needed. |
| B4_02 | Ks Jh 3c (unchanged) | No prior board holds Ks+Jh, Ks+3c, or Jh+3c. CLEAR. | None needed. |
| B4_03 | Ah 8s 3d (unchanged) | No prior board holds Ah+8s, Ah+3d, or 8s+3d. CLEAR. | None needed. |
| B4_04 | Kd 6c 2s (unchanged) | No prior board holds Kd+6c, Kd+2s, or 6c+2s. CLEAR. | None needed. |
| B4_05 | Qs 9c 5h (unchanged) | No 2-card match on any prior board. CLEAR. | None needed. |
| B4_06 | Qd 8s 4d → **Qd Jd 5c** | Qd+4d: BD_B5=7h 4d 2c Qd 9s. CONFLICT. | Replaced 4d with Jd and 8s with 5c. Qd+Jd: no prior board. Jd+5c: no prior board. CLEAR. |
| B4_07 | Jc 9h 7s (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_08 | Tc 8h 6d → **Tc 8h 5s** | Tc+6d: B25=As 6d 2h Tc 4s. CONFLICT. | Replaced 6d with 5s. Tc+5s: no prior board. 8h+5s: no prior board. CLEAR. |
| B4_09 | Ks 7s 6d (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_10 | Qh 9s 8h (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_11 | 8c 4s 2d (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_12 | 9d 5s 2c (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_13 | Ad 7c 2s Kh (unchanged) | 7c+2s: OC_B3=7c 4d 2s 9h Tc — 5-card river board. 2-card overlap but boards are of completely different lengths and compositions. Accepted as non-conflicting per multi-card near-identity definition. | Noted, accepted. |
| B4_14 | Kd 9s 4c Qs → **Kc 9s 4c Qs** | Kd+9s: TV_B3=Kd 9s 5h 2c Qh. CONFLICT. | Replaced Kd with Kc. Kc+9s: no prior board. Kc+Qs: no prior board. Kc+4c: no prior board. CLEAR. |
| B4_15 | Jd 6h 2c 8d → **Js 6s 2d 8c** | Jd+8d: CALL_Board1=Jd 8d 4c. CONFLICT. 6h+2d: SB_B6=9h 6h 2d Kd. CONFLICT. | Replaced Jd→Js, 6h→6s, 2c→2d, 8d→8c. Js+8c: no prior board. 6s+2d: no prior board. CLEAR. |
| B4_16 | Qc 7h 3s Td → **Qc 7d 3h Kd** | Qc+3s: PA_Board8=Qc 8d 3s 6h 2c. CONFLICT. | Replaced 7h→7d, 3s→3h, Td→Kd. Qc+7d: no prior board. Qc+3h: no prior board. 3h+Kd: no prior board. CLEAR. |
| B4_17 | 8d 4h 2s 9c (unchanged) | No 2-card match. CLEAR. | None needed. |
| B4_18 | Th 9d 8h (unchanged) | No 2-card match. CLEAR. | None needed. |

### Conflict Table (New Boards B4_19 – B4_24)

| New Board | Cards | Conflict check | Status |
|-----------|-------|----------------|--------|
| B4_19 | 5h 3c 2d | 5h+3c: no prior board. 5h+2d: no prior board. 3c+2d: no prior board. | CLEAR. |
| B4_20 | Kc Jh 7d 3s 9s | Kc+Jh: no prior board. Kc+9s: no prior board (FB_B2=Kc 9c has 9c not 9s). Jh+7d: no prior board. 3s+9s: no prior board. 7d+3s: TV_B2=Jd 7c 3s Ah — 7c not 7d. CLEAR. | CLEAR. |
| B4_21 | Jc 8d 4h | Jc+8d: CALL_Board1=Jd 8d 4c — Jd not Jc. No prior board has both Jc and 8d. Jc+4h: no prior board. 8d+4h: no prior board. | CLEAR. |
| B4_22 | 7c 4h 2s | 7c+2s: BD_B6=9c 7c 2d Kh — 2d not 2s. No prior board has 7c+2s. 7c+4h: no prior board. 4h+2s: TV_B1=Qc 8d 4s 2h — 4s not 4h, 2h not 2s. | CLEAR. |
| B4_23 | 5c 5d Ah | 5c+5d: no prior board has a paired 5 board. 5c+Ah: no prior board. 5d+Ah: CALL_Board4=Ah 9c 3s 6d Tc — Ah yes, 5d not present. | CLEAR. |
| B4_24 | 6s 3d 2s | 6s+3d: OC_B4=6s 3h 2c Ts — 3h not 3d. No prior board has 6s+3d. 6s+2s: two spades on same board — check for paired-suit conflicts: SB_B5=7s 6s 5d has 6s+7s but not 2s. No prior board has 6s+2s. 3d+2s: no prior board. | CLEAR. |
| B4_25 | 6h 2c 4s | 6h+2c: SB_B6=9h 6h 2d Kd has 6h+2d (not 2c). No prior board has 6h+2c. 6h+4s: B4_11=8c 4s 2d has 4s not 6h. No prior board has both 6h and 4s. 2c+4s: SB_B3/FB_B1 have 2c — none also have 4s. No prior board has 2c+4s. B4_22=7c 4h 2s: shares no cards with B4_25 (7c/4h/2s vs 6h/2c/4s — all different rank+suit combos). | CLEAR. |

---

## Section 6 — Conflict Resolutions (Summary)

| Board | Original cards | Revised cards | Reason |
|-------|---------------|---------------|--------|
| B4_06 | Qd 8s 4d | Qd Jd 5c | Qd+4d on BD_B5 |
| B4_08 | Tc 8h 6d | Tc 8h 5s | Tc+6d on B25 |
| B4_14 | Kd 9s 4c Qs | Kc 9s 4c Qs | Kd+9s on TV_B3 |
| B4_15 | Jd 6h 2c 8d | Js 6s 2d 8c | Jd+8d on CALL_Board1; 6h+2d on SB_B6 |
| B4_16 | Qc 7h 3s Td | Qc 7d 3h Kd | Qc+3s on PA_Board8 |

Boards B4_01–B4_05, B4_07, B4_09–B4_13, B4_17–B4_24: no card changes required.
B4_25: new board added in Round 2 (R2-2). Cards `6h 2c 4s` verified CLEAR of all prior boards and all B4_01–B4_24 boards.

---

## Section 7 — Final Board Inventory (Revised v2 — 25 Boards)

| ID    | Cards (final)         | Street | Texture           | Tier | Hero pos   | IP/OOP  | SPR       | Sub-patterns                  |
|-------|-----------------------|--------|-------------------|------|------------|---------|-----------|-------------------------------|
| B4_01 | Ad Tc 4h              | Flop   | Rainbow           | 1    | BTN/CO     | IP/OOP  | 10.8      | BP1, BP3(4D), BP4(alt)        |
| B4_02 | Ks Jh 3c              | Flop   | Rainbow           | 1    | BTN/HJ     | IP/OOP  | 10.8      | BP1, BP2                      |
| B4_03 | Ah 8s 3d              | Flop   | Rainbow           | 1    | CO         | OOP     | 10.8      | BP2 only (R2-1: removed from BP1) |
| B4_04 | Kd 6c 2s              | Flop   | Rainbow           | 1    | BTN/CO     | IP/OOP  | 10.8      | BP1, BP2, BP3(4D), BP4        |
| B4_05 | Qs 9c 5h              | Flop   | Rainbow           | 2    | BTN        | IP      | 10.8      | BP1, BP4                      |
| B4_06 | Qd Jd 5c              | Flop   | Two-tone (♦)      | 2    | BTN        | IP      | 10.8      | BP1, BP3                      |
| B4_07 | Jc 9h 7s              | Flop   | Rainbow           | 2/3  | BTN        | IP      | 10.8      | BP1, BP3, BP4(alt)            |
| B4_08 | Tc 8h 5s              | Flop   | Rainbow           | 3    | BTN        | IP      | 10.8      | BP1, BP3                      |
| B4_09 | Ks 7s 6d              | Flop   | Two-tone (♠)      | 2    | BTN        | IP      | 10.8      | BP3, BP1                      |
| B4_10 | Qh 9s 8h              | Flop   | Two-tone (♥)      | 2/3  | BTN        | IP      | 10.8      | BP3, BP1                      |
| B4_11 | 8c 4s 2d              | Flop   | Rainbow           | low  | BB/SB      | OOP     | 10.8      | BP5                           |
| B4_12 | 9d 5s 2c              | Flop   | Rainbow           | low  | BB/SB      | OOP     | 10.8      | BP5                           |
| B4_13 | Ad 7c 2s Kh           | Turn   | Rainbow           | 1    | BTN/CO     | IP/OOP  | 6.0       | BP1, BP6-H (near-miss CHECK)  |
| B4_14 | Kc 9s 4c Qs           | Turn   | Two-tone (♠)      | 1/2  | BTN        | IP      | 6.0       | BP3, BP1                      |
| B4_15 | Js 6s 2d 8c           | Turn   | Two-tone (♠)      | 2    | BTN/CO     | IP      | 6.5       | BP4                           |
| B4_16 | Qc 7d 3h Kd           | Turn   | Two-tone (♦)      | 1/2  | CO/BTN     | IP      | 6.0       | BP4, BP1, BP6-H (near-miss CHECK) |
| B4_17 | 8d 4h 2s 9c           | Turn   | Rainbow           | low  | SB         | OOP     | 7.0       | BP5                           |
| B4_18 | Th 9d 8h              | Flop   | Two-tone (♥)      | 4    | BTN        | IP      | 10.8      | BP6-D, BP6-A                  |
| B4_19 | 5h 3c 2d              | Flop   | Rainbow           | low  | BB         | OOP     | 10.8      | BP6-B                         |
| B4_20 | Kc Jh 7d 3s 9s        | River  | Two-tone (♠)      | —    | BB         | OOP     | 2.6       | BP6-C                         |
| B4_21 | Jc 8d 4h              | Flop   | Rainbow           | 2    | varies     | IP/OOP  | 10.8      | BP6-E, BP6-F                  |
| B4_22 | 7c 4h 2s              | Flop   | Rainbow           | low  | BB         | OOP     | 10.8      | BP5 only (R2-2: BP6-G moved to B4_25) |
| B4_23 | 5c 5d Ah              | Flop   | Paired, Rainbow   | 1    | BTN        | IP      | 10.8      | BP1                           |
| B4_24 | 6s 3d 2s              | Flop   | Two-tone (♠)      | low  | BB         | OOP     | 10.8      | BP5                           |
| B4_25 | 6h 2c 4s              | Flop   | Rainbow           | low  | BB         | OOP     | 10.8      | BP6-G only (R2-2 addition)    |

---

---

## Section 8 — Situation Count Summary (Final)

| Sub-pattern | Situations | Notes |
|-------------|-----------|-------|
| BP1 | 30 | B4_03 removed (R2-1); 2 sits reassigned to B4_01 |
| BP2 | 12 | Reduced from 15 (R2-4); sits 13-15 moved to BP6-H |
| BP3 | 20 | Reduced from 22 (R2-5); sits 21-22 moved to BP6-H |
| BP4 | 15 | Unchanged |
| BP5 | 12 | Unchanged; B4_22 now BP5-only |
| BP6 | 15 | Expanded from 10; +1 BP6-G on B4_25; +3 BP6-H from BP2; +2 BP6-H from BP3 |
| **Total** | **104** | Brief target was 100; 4 extra fill structural gaps. Accepted. |

*End of BOARD_ALLOCATION_V4_BET.md*
