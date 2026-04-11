# Delivery Note: BET_DECISION_TREE_V1.md

**From:** GTO Expert
**Date:** 9 April 2026
**File delivered:** `review/BET_DECISION_TREE_V1.md`
**Status:** AWAITING OWNER REVIEW

---

## What Was Delivered

A complete BET decision tree for labelling situations where `to_call == 0`
(hero is not facing a bet). The tree outputs BET or CHECK — never a frequency.

Seven sequential steps:
- Step 1: Global suppressors (S1 wet bluff, S2 OOP default, S3 aggressor)
- Step 2: Monster protection bet (dynamic boards)
- Step 3: PFA value c-bet (3A IP, 3B OOP exception)
- Step 4: PFA bluff c-bet (sub-conditions 4A combo draw, 4B NFD+blocker,
  4C nut draw IP, 4D blocker+gutshot edge case)
- Step 5: Thin value IP bet (non-PFA, capped opponent)
- Step 6: OOP value exception (KB Example 6 pattern)
- Step 7: Default CHECK

---

## Sources Synthesised

All 5 research papers read in full:
- R1 (Frequency): position-split c-bet rates, board texture modifier table
- R2 (Texture): 4-tier texture classification system (primary structure of Step 3A)
- R3 (Sizing/SPR): SPR zone framework; confirmed high SPR is the flop default
- R4 (Check-back): 4 check types; protection vs trap rule; danger_score threshold
- R5 (Blockers): flush blocker direction (bluff = positive, thin value = neutral/negative); combo draw threshold

All 3 cross-reviews incorporated:
- REVIEW_CBET_R1_R2: Position-split refinement; Issue 2 (middle connected board disagreement resolved)
- REVIEW_CBET_R3_R4: SPR zone correction (standard flop is high SPR); MDF math framing noted
- REVIEW_CBET_R5_AND_CROSS: Issue 4 (R2 tables are IP figures, OOP thresholds tightened); 5-gate composite framework confirmed coherent

---

## Key Design Choices

1. R2's 4-tier texture classification gates Step 3A. Tier determines the
   hand_category threshold required to BET: Tier 1 (A/K-high dry) requires
   top_pair (>= 6); Tier 2 (Q/J-high) requires TPGK (>= 7); Tier 3
   (moderate danger) requires two_pair (>= 10); Tier 4 produces no BET from Step 3.

2. OOP is substantially tighter throughout. S2 suppresses OOP bets below
   top 28% of range and 60% raw equity. Step 3B (OOP PFA value) and Step 6
   (OOP non-PFA value) have harder conditions than their IP equivalents.

3. Step 4 requires equity for all semi-bluff c-bets. Pure air never bets (R4
   Finding 2, R5 Finding 5). The minimum is draw_outs >= 4 with blocker + dry
   board + IP (4D, restricted). Combo draws (12+ outs) need no blocker (4A).

4. Monster protection (Step 2) uses danger_score >= 0.45 as the trigger.
   Below 0.45 the monster checks to trap (Default 7). This implements R4's
   "Bet monsters on dynamic boards, slowplay on dry boards" rule cleanly.

5. Frequency-to-threshold mapping table is included showing exactly how each
   research frequency (e.g., "OOP PFA 22-30%") informed each threshold
   (e.g., hero_range_percentile >= 0.72 = top 28%).

---

## Known Issues and Gaps (inherited from research)

- OOP texture-specific frequencies are not precisely quantified (Gap 1)
- Backdoor flush equity not captured in draw_outs (Gap 2)
- Made-hand nut blocker not in flush_block_pct (Gap 3)
- Middle connected board frequency disagreement R1 vs R2 resolved conservatively (Gap 4)
- 3-bet pot SPR profile differs from SRP — tree may over-produce BET in 3BP (Gap 5)

None of these are blocking. All are documented in the tree's Known Limitations section.

---

## Questions for Owner Review

1. Step 3A uses board_favour >= 0.20 as the range credibility gate. The feature
   encodes how much the board favors the PFA's range. Is 0.20 the right floor,
   or should this be higher (e.g., 0.30) to further suppress marginal c-bets?

2. Step 4D (blocker + gutshot edge case) is flagged MEDIUM-LOW confidence and
   heavily restricted (IP only, A/K high board, rainbow, villain_air >= 0.40).
   The reviewer noted this is a "marginal edge case" from R5. Should it be
   removed entirely to simplify the tree?

3. Tier 3 threshold (hand_category >= 10, two_pair required on moderately
   connected boards) is conservative. R2 allows up to 40% on Tier 3 textures,
   which might admit TPGK in some spots. Should Tier 3 allow TPGK (>= 7) with
   additional conditions, or keep two_pair as the floor?

---

*Delivered to review/comms/ per protocol. GTO Expert confirms delivery.*
