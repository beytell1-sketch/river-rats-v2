# V23 Curated-Draw Candidate Filter — Phase 1.4 Rows 6–7

**Date:** 2026-04-16
**Track:** D — curated-bucket sourcing (semi-bluff draws)
**Scope:** Analysis + data extraction only. No labelling, no generation, no pool mutation.
**Build plan ref:** `review/comms/V23_HAND_GENERATION_PLAN_2026-04-16.md` §1.4, scope row 6 (flop draws) + row 7 (turn draws).

---

## Filter Criteria

```
is_made_hand == 0
AND (has_flush_draw == 1 OR has_straight_draw == 1)
AND draw_outs >= 8
AND facing_bet == 0
AND num_opponents == 2       # i.e. 3-way pot (hero + 2 villains)
```

## Pool Inputs

| Pool | Path | N inspected | M matched |
|------|------|-------------|-----------|
| P1 | `training-data/3way_combined_350.jsonl` | 350 | 9 |
| P2 | `training-data/factory_batch5_situations.jsonl` | 185 | 7 |
| **Total** | — | **535** | **16** |

## Status: BLOCKED (stop condition tripped)

Per build plan stop condition: "If the filter returns < 20 candidates total — STOP, report (may mean the pool is too narrow for rows 6-7 targets of 25 hands combined; scope implication needs owner review before Phase 1 proceeds on these rows)."

**Matched: 16 candidates** (target ~30, floor 20). Filter surface is narrower than the row 6+7 target of ~25 curated hands.

### Why the pool is thin
- The 3-way pot precondition (num_opponents == 2) naturally shrinks hit-rate — most pool hands are HU.
- `facing_bet == 0` (hero is the first aggressor to act) further restricts to check-to-hero spots; most flops in the pool have someone already betting.
- Several rows with draws in the pool have `is_made_hand == 1` (e.g. pair + draw) so they filter out despite carrying draw equity.

### Recommended owner decisions
1. **Accept thinner rows** — approve ~12–15 of the 16 candidates below for Phase 4 Pass 1/2, and scale row 6+7 target to match.
2. **Widen the filter** — e.g. permit `is_made_hand=1` if hero holds weak pair + strong draw (common semi-bluff shape); or drop `facing_bet=0` and allow facing-small-bet semi-bluff-raise spots.
3. **Source more** — stand up a supplementary 3-way pool query on PokerBench targeted at the missing shape (2-way check-check-to-hero with 9+ out draws).

## Distribution Summary

| Slice | Count |
|-------|-------|
| Flop (row 6) | 10 |
| Turn (row 7) | 6 |
| Flush-only draws | 9 |
| Straight-only draws | 4 |
| Combo (flush + straight) draws | 3 |
| Nut-blocker YES | 3 |
| Nut-blocker LIKELY | 1 |
| Nut-blocker NO | 12 |

Nut-blocker YES/LIKELY total: **4 of 16 (25%)** — below the "at least half" target for the curated-draw bucket. Owner may wish to down-select heavily toward the YES/LIKELY rows and widen the sourcing for additional nut-blocker shapes.

---

## Summary Table

| # | Source | situation_id | Hero | Board | Street (Row) | Draw type / outs | Nut-blocker | Existing label |
|---|--------|--------------|------|-------|--------------|------------------|-------------|----------------|
| 1 | 3way_350 | `d3036_BTN_flop` | KdQd | JhJd9d | row 6 (flop) | combo/13 | **NO** | labelled_3way=RAISE; oracle=RAISE; adjusted=CHECK; expert=CHECK |
| 2 | 3way_350 | `d5620_BTN_flop` | QsAd | JsKsKd | row 6 (flop) | straight/8 | **LIKELY** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 3 | 3way_350 | `d6522_HJ_flop` | AhJc | 5cKc6c | row 6 (flop) | flush/9 | **NO** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 4 | 3way_350 | `d1764_BB_flop` | 7sKs | 9s4s9d | row 6 (flop) | flush/9 | **NO** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 5 | 3way_350 | `d4472_BTN_turn` | 5d4d | Qs2d3s9h | row 7 (turn) | straight/8 | **NO** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 6 | 3way_350 | `d1983_BTN_turn` | Ad4d | Jd7dKh2c | row 7 (turn) | flush/9 | **YES** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 7 | 3way_350 | `d1168_CO_turn` | KdTd | Js5d2s7d | row 7 (turn) | flush/9 | **NO** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 8 | 3way_350 | `d1903_BB_turn` | QcKs | 6c5h9c8c | row 7 (turn) | combo/13 | **NO** | labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK |
| 9 | 3way_350 | `PA_Board3_Jh8h4h_h6` | Ah3c | Jh8h4h | row 6 (flop) | flush/9 | **YES** | oracle=PENDING; expert=CHECK |
| 10 | bp_batch5 | `BP4_19` | 8s6s | As7s3d | row 6 (flop) | flush/9 | **NO** | action=CALL |
| 11 | bp_batch5 | `BP4_20` | Jh9h | Th7h3s | row 6 (flop) | combo/13 | **NO** | action=CALL |
| 12 | bp_batch5 | `BP4_22` | 8d7h | Jd6s2d9c | row 7 (turn) | straight/8 | **NO** | action=CALL |
| 13 | bp_batch5 | `BP4_30` | 8s7d | Jh9c6d | row 6 (flop) | straight/8 | **NO** | action=CALL |
| 14 | bp_batch5 | `BP6_05` | Js5d | AsTs4s | row 6 (flop) | flush/9 | **NO** | action=CALL |
| 15 | bp_batch5 | `BP6_10` | KdQh | Th6h2h | row 6 (flop) | flush/9 | **NO** | action=CALL |
| 16 | bp_batch5 | `BP7_06` | AhJh | Qh9d5h7c | row 7 (turn) | flush/9 | **YES** | action=CALL |

---

## Candidate Detail Blocks

### 1. `d3036_BTN_flop` — KdQd on JhJd9d — row 6 (flop semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BTN, villains=['UTG', 'BB']; pot=80, to_call=0
- **Draw:** combo (flush+straight), 13 outs (has_flush_draw=1, has_straight_draw=1)
- **Board texture:** two_tone=1, monotone=0, paired=1, high_card_rank=11, connectivity=2
- **Action history:** preflop: BTN call
- **Nut-blocker flag: NO** — K-high flush draw (not nut); straight draw with high card (rank 13)
- **Existing label:** labelled_3way=RAISE; oracle=RAISE; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has KdQd on JhJd9d — a flush draw plus gutshot (13 outs) but no made hand, with 46.5% equity. Despite being IP with closing action, villain_top_pair_plus_pct is 55% (UTG opened, strong uncapped range likely holding Jx, overpairs). Board favour is negative (-0.25). Semi-bluffing into two opponents with only 36% fol…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 2. `d5620_BTN_flop` — QsAd on JsKsKd — row 6 (flop semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BTN, villains=['CO', 'BB']; pot=80, to_call=0
- **Draw:** straight draw, 8 outs (has_flush_draw=0, has_straight_draw=1)
- **Board texture:** two_tone=1, monotone=0, paired=1, high_card_rank=13, connectivity=2
- **Action history:** preflop: BTN call
- **Nut-blocker flag: LIKELY** — straight draw with high card (rank 14)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** QsAd on JsKsKd from BTN (IP) with a straight draw (8 outs, need a T for broadway) and 32.7% equity. However, the paired K board massively favours the CO opener's uncapped range — villain_tp_plus is 56.5% and board_favour is -0.26. CO has KK, AK, KQ, KJ all in range. Despite IP position and a decent draw, DO NOT rule #2…

### 3. `d6522_HJ_flop` — AhJc on 5cKc6c — row 6 (flop semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=HJ, villains=['BTN', 'BB']; pot=80, to_call=0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=1, paired=0, high_card_rank=13, connectivity=4
- **Action history:** preflop: HJ raise
- **Nut-blocker flag: NO** — J-c on monotone board (non-nut blocker)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has AhJc (nut flush draw with Ah on 5cKc6c monotone board) but is OOP as HJ with BTN and BB behind. Despite 9 flush outs and 31% equity, DO NOT rule #2 applies: do not barrel draws into 2 opponents. OOP semi-bluffs have ~36% fold equity at best, and on a monotone board opponents are less likely to fold flush draws…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 4. `d1764_BB_flop` — 7sKs on 9s4s9d — row 6 (flop semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BB, villains=['HJ', 'BTN']; pot=80, to_call=0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=1, monotone=0, paired=1, high_card_rank=9, connectivity=2
- **Action history:** preflop: BB call
- **Nut-blocker flag: NO** — K-high flush draw (not nut)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has Ks7s (flush draw) on 9s4s9d — paired board with a flush draw. OOP in BB with 40.5% equity and 9 flush outs. Despite reasonable equity, DO NOT rule #2 applies: do not semi-bluff draws into two opponents OOP. Fold equity is ~36% which is insufficient. The paired board also means opponents with trips or full hous…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 5. `d4472_BTN_turn` — 5d4d on Qs2d3s9h — row 7 (turn semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BTN, villains=['CO', 'BB']; pot=80, to_call=0
- **Draw:** straight draw, 8 outs (has_flush_draw=0, has_straight_draw=1)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=12, connectivity=4
- **Action history:** preflop: BTN call | flop: BTN check
- **Nut-blocker flag: NO** — low-end straight draw (top rank 5)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has 54 with an open-ended straight draw (needs an A or 6 for a straight) on Qs2d3s9h, IP on the turn. With 18.6% equity, 8 draw outs, and 99.4% better hands currently, this is a pure draw with no made hand. Despite being IP with high villain air (40.3%) and both opponents checking, semi-bluffing into two opponents…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 6. `d1983_BTN_turn` — Ad4d on Jd7dKh2c — row 7 (turn semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BTN, villains=['HJ', 'BB']; pot=80, to_call=0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=13, connectivity=2
- **Action history:** preflop: BTN call | flop: BTN check
- **Nut-blocker flag: YES** — nut flush draw: hero Ace-d on two-tone d
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has Ad4d (nut flush draw, 9 outs) on Jd7dKh2c. IP on BTN with 27.5% equity. Both opponents checked (villain_checked_back=1). Despite having the nut flush draw and IP position, DO NOT rule #2 applies: barrelling draws into 2 opponents has only ~36% fold equity. At SPR 1.25, a bet here nearly commits stacks. The nut…

### 7. `d1168_CO_turn` — KdTd on Js5d2s7d — row 7 (turn semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=CO, villains=['BTN', 'BB']; pot=80, to_call=0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=11, connectivity=2
- **Action history:** preflop: CO raise | flop: CO check
- **Nut-blocker flag: NO** — K-high flush draw (not nut)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has KdTd (flush draw, 9 outs) on Js5d2s7d. OOP as CO with 24.8% equity. Despite having a flush draw, hero is OOP and the DO NOT rules clearly prohibit barrelling draws into 2 opponents — fold equity is ~36% which is insufficient. OOP makes it even worse as hero acts first with BTN still behind. Check and realize e…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 8. `d1903_BB_turn` — QcKs on 6c5h9c8c — row 7 (turn semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BB, villains=['UTG', 'BTN']; pot=80, to_call=0
- **Draw:** combo (flush+straight), 13 outs (has_flush_draw=1, has_straight_draw=1)
- **Board texture:** two_tone=1, monotone=0, paired=0, high_card_rank=9, connectivity=7
- **Action history:** preflop: BB call | flop: BB check
- **Nut-blocker flag: NO** — Q-c on monotone board (non-nut blocker); straight draw with high card (rank 13)
- **Existing label:** labelled_3way=CHECK; oracle=CHECK; adjusted=CHECK; expert=CHECK
- **Expert reasoning (pool):** Hero has QcKs on 6c5h9c8c — no made hand but a monster combo draw with 13 outs (flush draw + straight draw via 7 or T). OOP in BB with 22.4% equity. Despite the strong draw, hero is OOP against two opponents on a very dangerous board (0.75 danger). DO NOT rule #2: don't barrel draws into 2 opponents. The 13 outs give e…
- **Flags:** non-nut-blocker; owner may exclude unless diversity-filler

### 9. `PA_Board3_Jh8h4h_h6` — Ah3c on Jh8h4h — row 6 (flop semi-bluff)

- **Source:** 3way_combined_350
- **Position:** hero=BB, villains=['CO']; pot=90.0, to_call=0.0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=1, paired=0, high_card_rank=11, connectivity=2
- **Action history:** (none)
- **Nut-blocker flag: YES** — Ace-h nut blocker on monotone h board (1-card fd)
- **Existing label:** oracle=PENDING; expert=CHECK
- **Expert reasoning (pool):** Ah3c holds the nut flush draw (Ah blocker) with 42.4% equity but no made hand. OOP with 9 flush outs. On a monotone board 3-way OOP, semi-bluffing has low fold equity (~36%) and opponents with made flushes or their own draws will not fold. The Ah is a valuable blocker but blockers matter 40% less 3-way per the DO NOT r…

### 10. `BP4_19` — 8s6s on As7s3d — row 6 (flop semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=3, villains=['SB', 'BB']; pot=90.0, to_call=0.0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=1, monotone=0, paired=0, high_card_rank=14, connectivity=2
- **Action history:** SB check, BB check, BTN ???
- **Nut-blocker flag: NO** — 8-high flush draw (not nut)
- **Existing label:** action=CALL
- **Description:** BP4_19: 8s6s on As-7s-4d. Flush draw (spades) + gutshot. Hero BTN IP, all checked to BTN — semi-bluff bet.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 11. `BP4_20` — Jh9h on Th7h3s — row 6 (flop semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=3, villains=['SB', 'BB']; pot=90.0, to_call=0.0
- **Draw:** combo (flush+straight), 13 outs (has_flush_draw=1, has_straight_draw=1)
- **Board texture:** two_tone=1, monotone=0, paired=0, high_card_rank=10, connectivity=2
- **Action history:** SB check, BB check, BTN ???
- **Nut-blocker flag: NO** — J-high flush draw (not nut); straight draw with high card (rank 11)
- **Existing label:** action=CALL
- **Description:** BP4_20: Jh9h on Th-7h-3s. Flush draw + OESD (J-T-9-8 or T-9-8-7). Hero BTN IP, all checked to BTN — semi-bluff bet.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 12. `BP4_22` — 8d7h on Jd6s2d9c — row 7 (turn semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=2, villains=['BB', 'BTN']; pot=90.0, to_call=0.0
- **Draw:** straight draw, 8 outs (has_flush_draw=0, has_straight_draw=1)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=11, connectivity=2
- **Action history:** BB check, CO check, CO ???
- **Nut-blocker flag: NO** — low-end straight draw (top rank 8)
- **Existing label:** action=CALL
- **Description:** BP4_22: 8d7h on Jd-6s-2d-9c. Flush draw (diamonds) + OESD (8-7-6 needs 5 or T). Hero CO on turn — semi-bluff bet.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 13. `BP4_30` — 8s7d on Jh9c6d — row 6 (flop semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=3, villains=['SB', 'BB']; pot=90.0, to_call=0.0
- **Draw:** straight draw, 8 outs (has_flush_draw=0, has_straight_draw=1)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=11, connectivity=2
- **Action history:** SB check, BB check, BTN ???
- **Nut-blocker flag: NO** — low-end straight draw (top rank 8)
- **Existing label:** action=CALL
- **Description:** BP4_30: 8s7d on Jh-9c-6d. Middle pair eights on connected board. Hero BTN. Bet looks natural but CHECK preferred — range advantage unclear on J-9-6.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 14. `BP6_05` — Js5d on AsTs4s — row 6 (flop semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=3, villains=['SB', 'BB']; pot=90.0, to_call=0.0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=1, paired=0, high_card_rank=14, connectivity=2
- **Action history:** SB check, BB check, BTN ???
- **Nut-blocker flag: NO** — J-s on monotone board (non-nut blocker)
- **Existing label:** action=CALL
- **Description:** BP6_05: Js5d on As-Ts-4s monotone. Non-nut flush draw (Js). Hero BTN IP, not-facing-bet. Flush draw consideration on monotone.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 15. `BP6_10` — KdQh on Th6h2h — row 6 (flop semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=5, villains=['CO', 'BTN']; pot=90.0, to_call=0.0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=1, paired=0, high_card_rank=10, connectivity=2
- **Action history:** BB check, BB ???
- **Nut-blocker flag: NO** — Q-h on monotone board (non-nut blocker)
- **Existing label:** action=CALL
- **Description:** BP6_11: KdQh on Th-6h-2h monotone. Two overcards, no heart. Hero BB OOP, not-facing-bet. Air on monotone — check.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled; non-nut-blocker; owner may exclude unless diversity-filler

### 16. `BP7_06` — AhJh on Qh9d5h7c — row 7 (turn semi-bluff)

- **Source:** factory_batch5
- **Position:** hero=2, villains=['BB', 'BTN']; pot=90.0, to_call=0.0
- **Draw:** flush draw, 9 outs (has_flush_draw=1, has_straight_draw=0)
- **Board texture:** two_tone=0, monotone=0, paired=0, high_card_rank=12, connectivity=2
- **Action history:** BB check, CO check, CO ???
- **Nut-blocker flag: YES** — nut flush draw: hero Ace-h on two-tone h
- **Existing label:** action=CALL
- **Description:** BP7_06: AhJh on Qh-9d-5h-7c. Nut flush draw + overcard on turn. Hero CO OOP not-facing-bet — semi-bluff lead.
- **Flags:** BP-factory label `CALL` is suspect — to_call=0; treat as unlabelled

---

## Owner Spot-Check Instructions

1. **Confirm blocker status** on the 4 YES/LIKELY candidates (#2, #6, #9, #16). Downgrade any that fail manual review.
2. **Triage the NO rows** — decide whether any are worth keeping for diversity (e.g. 8-high flush draw against a capped range may still be a semi-bluff spot) or whether to exclude all and widen sourcing.
3. **Decide scope** — approve up to ~25 candidates for the row 6+7 curated bucket. If approved set < 20, pick one of the three options in the `BLOCKED` section above (accept thinner rows / widen filter / source more).
4. **Note on existing labels** — these candidates carry pre-existing labels (see Existing label column). **Do NOT treat those as authoritative for the curated bucket.** Approved candidates run through **Pass 1 / Pass 2 labelling in Phase 4, NOT pre-labelled.** The existing labels are informational only (for sanity-checking that approved candidates weren't already flagged as clear CHECK spots by prior labellers).
5. **Deliverable back to Programmer:** approved sid list + scope decision (accept 16-only / widen / source-more).

**Do not label these hands in this document.** Labelling happens in Phase 4.
