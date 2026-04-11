# Independent Review — Hero Hand Assignments, All Agents
**Date:** 9 April 2026
**Reviewer:** Independent reviewer (Creative Lead role)
**Files reviewed:**
- DESIGN_AGENT_1_SP5_SP6.md
- DESIGN_AGENT_2_SP1_SP2_SP3_SP4.md
- DESIGN_AGENT_3_SP7_SP10.md
- DESIGN_AGENT_4_SP8_SP9.md
- BOARD_ALLOCATION_V3_FINAL.md
- RAISE_DECISION_TREE_V2.md

**Verdict: ISSUES FOUND — conditional pass with four items requiring resolution before factory build**

---

## 1. Distribution Check

### Total situation count

| Sub-pattern | Type  | Count (allocation) | Agent count | Match |
|-------------|-------|--------------------|-------------|-------|
| SP1         | RAISE | 18                 | 18          | PASS  |
| SP2         | RAISE | 10                 | 10          | PASS  |
| SP3         | RAISE | 12                 | 12          | PASS  |
| SP4         | CALL  | 6                  | 6           | PASS  |
| SP5         | RAISE | 28                 | 28          | PASS  |
| SP6         | CALL  | 13                 | 13          | PASS  |
| SP7         | RAISE | 25                 | 25          | PASS  |
| SP8         | RAISE | 16                 | 16          | PASS  |
| SP9         | CALL  | 10                 | 10          | PASS  |
| SP10        | CALL  | 13                 | 13          | PASS  |
| **Total**   |       | **151**            | **151**     | PASS  |

Total count is correct at 151.

---

## 2. Card Conflict Check

### Methodology

For every situation I cross-checked hero_cards against board_cards at the same rank AND suit. A conflict exists only when the identical card (same rank and same suit) appears in both lists. I checked all 151 situations, using the board definitions in BOARD_ALLOCATION_V3_FINAL.md Section 1 as the authoritative board_cards source.

### Results by agent

**Agent 1 — SP5 (28 sits) + SP6 (13 sits) = 41 situations checked**

All 41 situations verified. No card appears in hero hand at the same rank+suit as a board card.

Notable near-misses verified clean:
- SP5_09 B08: board has Qc 5c 9h. Agent noted "Qc blocker" as placeholder and correctly substituted Ac (rank 14). Hero ['Ac', '8d'] — Ac not on B08. PASS.
- SP5_12 B09: board has Ah 4h 8c. Agent correctly identified Ah is on board, used Kh instead. Hero ['Kh', 'Jd'] — neither on B09. PASS.
- SP5_24/25 B05: board is monotone 6s 4s Qs. Hero holds As+7d and Ks+9d respectively. As, Ks not on B05. PASS.
- SP6_10 B11r: board has Ts 8s 4h. Agent noted Ts is on board; correctly used 9s instead of 10s. Hero ['9s', '7d'] — 9s not on B11r. PASS.
- SP6_11 B14: board has 3s Js 9h 4d. Agent noted Js is on board; correctly used Ts instead. Hero ['Ts', '6c'] — Ts not on B14. PASS.

**Agent 2 — SP1 (18 sits) + SP2 (10 sits) + SP3 (12 sits) + SP4 (6 sits) = 46 situations checked**

All 46 situations verified. Agent 2 produced a detailed set construction guide and correctly excluded board-suit cards in every case.

Notable verifications:
- SP1_13 B16: board ['5h', 'Kd', '2h', '8c']. Hero ['Kh', 'Kc']. Kd is on board; hero holds Kh and Kc (different suits). PASS.
- SP2_03 B17: board ['Ad', '7s', '3c', '2h']. Hero ['Ah', 'Ac']. Ad on board; hero holds Ah and Ac. PASS.
- SP3_03 B06: board ['8c', '8h', '3d']. Hero ['8d', '3h']. 8c and 8h on board; hero holds 8d. 3d on board; hero holds 3h. PASS.
- SP4_04 B26: board ['Kh', '5c', '2h', '9d', 'Qh']. Hero ['Ah', 'Th']. Board has Kh, 2h, Qh but not Ah or Th. PASS.
- SP4_02 B33: board ['Qh', 'Qd', '7h']. Hero ['Qc', '7c']. Qh and Qd on board; hero holds Qc. 7h on board; hero holds 7c. PASS.

**Agent 3 — SP7 (25 sits) + SP10 (13 sits) = 38 situations checked**

All 38 situations verified. Agent 3 included a detailed card conflict table in their document which I cross-checked against board definitions.

One item requiring special attention: Agent 3's own self-check at SP7_12 initially flagged a potential Jc conflict, then correctly resolved it — B21 is 3h 3d 9s Kc; hero holds Kd Jc; Jc is NOT in B21 (Kc is in B21, not Jc). Jc IS in B13 but SP7_12 uses B21. The resolution is correct. PASS.

**Agent 4 — SP8 (16 sits) + SP9 (10 sits) = 26 situations checked**

All 26 situations verified.

Notable:
- SP8_10 initial design ['Jc', 'Th'] on B26 ['Kh', '5c', '2h', '9d', 'Qh']: Agent caught that K-Q-J-T-9 = a made straight (not air). Correctly revised to ['Jc', '8d']. PASS.
- SP9_06 B26: hero ['Ks', '9s']. Board has Kh and 9d. Ks ≠ Kh, 9s ≠ 9d. PASS.
- SP9_09 B25: hero ['Ad', 'Th']. Board has As and Tc. Ad ≠ As, Th ≠ Tc. PASS.

### Card conflict summary

**Total situations checked: 151 / 151**
**Card conflicts found: 0**

---

## 3. Tree Condition Compliance — Spot Checks

### SP5: flush_draw_rank >= 12 across all 28 situations

Verified all 28 SP5 situations against the allocation table (Section 3, SP5 column "draw_rank"):

- Rank 14 (Ace): 12 situations — sits 1, 2, 4, 7, 9, 10, 12, 14, 17, 20, 22, 24
- Rank 13 (King): 9 situations — sits 3, 5, 8, 11, 13, 15, 18, 21, 25
- Rank 12 (Queen): 7 situations — sits 6, 16, 19, 23, 26, 27(note: sit 27 is rank 14 per Agent 1 text vs rank listed; see below), 28

Cross-check of hero cards against claimed rank:
- SP5_01 ['Ac', 'Kd'] → Ac = rank 14 clubs. Board B01 clubs suit. PASS.
- SP5_06 ['Qd', '7c'] → Qd = rank 12 diamonds. Board B04 diamonds suit. PASS (rank=12, minimum qualifying rank, correctly at boundary).
- SP5_26 ['Qc', 'Jd'] → Qc = rank 12 clubs. Board B01 clubs suit (Qc not on B01 which has 2c, Tc). PASS.
- SP5_28 ['Qs', 'Jh'] → Qs = rank 12 spades. Board B11r spades suit (Ts 8s 4h — Qs not on board). PASS.

**All 28 SP5 situations have flush_draw_rank >= 12. PASS.**

### SP5: flush_block_pct > 0 across all 28 situations

Agent 1 assigns block_pct values ranging 0.08-0.35. All are strictly positive. PASS.

### SP6: All 6 failure modes present with correct failing condition

Per allocation table (Section 3, SP6):

| Failure mode | Sits | Allocation count | Agent 1 count | PASS? |
|---|---|---|---|---|
| fold_equity < 0.45 | 1,2,3 | 3 | 3 | PASS |
| aggr_count >= 2 | 4,5 | 2 | 2 | PASS |
| is_paired == 1 | 6,7 | 2 | 2 | PASS |
| draw_outs < 9 | 8,9 | 2 | 2 | PASS |
| flush_draw_rank < 12 | 10,11 | 2 | 2 | PASS |
| flush_block_pct == 0 | 12,13 | 2 | 2 | PASS |

All 6 failure modes present. Minimum counts met. PASS.

### SP1: All hands are genuine monsters (set/two-pair/full-house)

All 18 SP1 hands verified:
- Sets (hand_category 12+): SP1_01(QQ set), 03(66 set), 04(TT set), 06(KK set), 08(QQ set), 09(KK set), 11(JJ set), 13(KK set), 15(QQ set), 17(TT set) = 10 sets
- Two pair (hand_category 10): SP1_02(Q+6), 05(T+8), 07(K+7), 10(K+7), 12(J+4), 14(K+8), 16(Q+9), 18(Q+5) = 8 two-pairs

All 18 have is_monster == 1. PASS.

### SP3: All 12 hands are OOP check-raises with monsters

All 12 SP3 hands verified as is_monster == 1 (sets, full houses) on boards with to_call > 0.

One structural flag (noted by Agent 2, confirmed here): SP3 sit#10 uses B17 which has to_call = 0 (hero leads). This is a leading action, not a check-raise. The allocation table describes this as "Set OOP, dry turn" but the SP3 pattern is defined as "Monster + OOP check-raise." Agent 2 flagged this and interpreted it as a monster OOP lead, which still fires Step 2 value raise. The label RAISE is correct under the tree regardless of action structure (Step 2 fires when is_monster == 1 and no suppressor fires). However, this situation technically does not demonstrate a check-raise structure, which is the SP3 pedagogical intent. This is an allocation-level design issue, not a labelling error. **Flagged as Issue #1 below.**

### SP4: All 6 suppressors correctly identified and monster is present

All 6 SP4 situations verified:
- SP4_01/02 B33: S2 fires (flush_danger=0.65 >= 0.60 AND is_paired=1). PASS.
- SP4_03 B12: S3 fires (villain_aggression_count=2). PASS.
- SP4_04 B26: S3 fires (villain_aggression_count=2). PASS. Hero ['Ah', 'Th'] = ace-high flush on 3-heart board = is_monster=1 (flush). PASS.
- SP4_05 B09: S4 fires (SPR=8.0 >= 6.0 AND is_ip=1). PASS.
- SP4_06 B20: S5 fires (num_callers=1 AND range_pct=0.88 < 0.92). PASS.

All 5 suppressors (S2, S3, S3, S4, S5) represented. Note: S1 is NOT represented in SP4 — the allocation only requires S2-S5 coverage. S1 is "flush_danger >= 0.60 AND hand_category < 10" which is not in the 6-sit SP4 allocation. This gap is in the original allocation design, not introduced by Agent 2.

### SP7: is_monster == 0 for all 25 situations

Agent 3 explicitly chose hand_category 7-9 (top_pair_good_kicker, top_pair_top_kicker, overpair) for all SP7 hands. None are sets, straights, flushes, full houses, or quads.

Spot checks:
- SP7_02 ['Ac', 'Ad']: overpair (9) on 8c-8h-3d. Board pair is 88; hero has AA = overpair. is_monster = 0 (AA is hand_category 9, not a set). PASS.
- SP7_15 ['Qs', 'Qd']: overpair (9) on 8c-8h-3d. QQ above the 88 board. is_monster = 0. PASS.
- SP7_22 B12 ['Ah', 'Jd']: board 7c-2d-Kc-Ac. Ah pairs Ac for top pair of aces. One pair only; no set (hero has only one Ace). is_monster = 0. PASS.

**All 25 SP7 situations: is_monster == 0. PASS.**

### SP8: All 16 situations at range_pct <= 0.20 and river only

Verified all 16 SP8 range percentiles: 0.02 (SP8_16) to 0.19 (SP8_09). All strictly at or below 0.20. PASS.

All 16 are on river boards (B23-B29). PASS.

villain_aggression_count == 0 for all 16. PASS.

num_callers_to_bet == 0 for all 16. PASS.

### SP9: All 10 situations CALL with correct flat-spot trigger

All 10 SP9 triggers verified:
- Board_favour trigger (sits 1-4, 10): B07 x2 (-0.45, -0.50), B19 (-0.55), B23 (-0.35), B17 (-0.32). All <= -0.30. PASS.
- Aggression trigger (sits 5-7): B12 (aggr=2), B26 (aggr=2), B29 (aggr=3). All >= 2. PASS.
- Num_callers trigger (sits 8-9): B24 (callers=1), B25 (callers=1). PASS.

All 10 SP9 hands have is_monster == 0. PASS.

---

## 4. Known Flag Assessments

### Flag 1: SP6_12 flush_block_pct == 0 interpretation

**Agent 1 finding:** Agent 1 devoted extensive analysis to this flag, working through multiple interpretations of how flush_block_pct can be zero when hero holds a high-rank suit card.

**Reviewer assessment:** Agent 1's final resolution for SP6_12 uses ['Ac', '9h'] on B01 (clubs board 2c Tc 6d), arguing that Ac gives flush_draw_rank=14 but flush_block_pct=0 because Ac only blocks villain's Ac-x combos while villain's actual flush range (Kc-x, Qc-x, Jc-x) is entirely unblocked. This is a workable interpretation if the feature extractor implements flush_block_pct as "fraction of villain's flush draw combos blocked," not "fraction of nut-flush combos blocked." The distinction matters and is feature-implementation-dependent.

**Issue:** The interpretation is internally consistent but depends on a specific implementation choice in the feature extractor that is not documented in the 52-feature reference. Before factory build, the feature extractor's exact definition of flush_block_pct should be confirmed. If flush_block_pct is implemented as "fraction of villain's flush combos that hero's cards remove from the deck" (i.e., any suit card reduces the denominator), then Ac on a clubs board would produce a positive block_pct, making SP6_12's design invalid.

SP6_13 ['8s', '7d'] on B04 (diamond board) is cleaner: hero holds no diamonds, so flush_block_pct = 0 unambiguously. However the agent notes this also fails flush_draw_rank (7d gives rank=7 < 12) and draw_outs (gutshot = 4 outs). The primary failure is documented as flush_block_pct=0 but multiple gates fail simultaneously. This is acceptable for CALL labelling but produces a situation where the failure mode is not cleanly isolated to block_pct alone.

**Verdict:** SP6_12 is the more problematic of the two. Recommend confirming flush_block_pct implementation before build. If the extractor produces a positive value for Ac on a clubs board, SP6_12 needs a redesign. SP6_13 is acceptable as is, with the caveat that it demonstrates multiple simultaneous failures. **Issue #2 — requires feature extractor confirmation before factory build.**

### Flag 2: SP1 B05 SPR=6.0 — does S4 fire at exactly 6.0?

**Agent 2 finding:** Agent 2 identified this conflict directly and flags it clearly. B05 has SPR=6.0 and hero is IP (BTN). S4 fires when "spr >= 6.0 AND is_ip == 1." The tree condition uses >= 6.0, which means SPR=6.0 exactly satisfies S4, making these three SP1 situations (sits 1-3 on B05) CALL, not RAISE.

**Reviewer assessment:** This is a genuine labelling conflict. The allocation table assigns B05 sits 1-3 as SP1 RAISE. The decision tree S4 suppressor fires at spr >= 6.0. The tree rationale note says "at SPR 4-6 IP monsters still raise for value; only at SPR 6+ does pot control clearly dominate" — using "6+" language that implies strictly greater than 6.0 in the English description, contradicting the formal "spr >= 6.0" threshold.

If the factory uses the formal threshold (>= 6.0), SP1_01, SP1_02, and SP1_03 will be labelled CALL, not RAISE. That reduces SP1 RAISE count from 18 to 15 and adds 3 unintended CALLs to the dataset. If the factory uses strict inequality (> 6.0), the three B05 situations correctly label as RAISE.

**This is an unresolved ambiguity in the tree itself.** The tree must be clarified: is S4 threshold "spr > 6.0" or "spr >= 6.0"? Agent 2 deferred to the allocation table's RAISE intent, which is reasonable, but the factory labeller will apply the formal condition. **Issue #3 — tree ambiguity must be resolved before factory build. Recommend changing S4 to "spr > 6.0" to match the stated rationale, or explicitly accepting that B05 situations label CALL.**

### Flag 3: SP3 sit#10 (B17) is a lead board, not check-raise

**Agent 2 finding:** B17 has to_call=0 (hero leads; no bet to check-raise against). SP3 is defined as "Monster + OOP check-raise" requiring to_call > 0.

**Reviewer assessment:** This conflict was already identified in the original flags list. Agent 2 flagged it correctly. The label remains RAISE (Step 2 fires regardless of to_call when is_monster=1 and no suppressor fires), but the pedagogical purpose of SP3 is to demonstrate OOP check-raise structure. A leading action on B17 does not teach check-raise. This is a design inconsistency, not a labelling error. The factory will produce a correct RAISE label, but the training example will not demonstrate the intended SP3 structure.

**Verdict:** Labelling is correct (RAISE). Design is inconsistent with SP3 purpose. This is an allocation-level issue (B17 should not be in SP3 since to_call=0). If this matters for pedagogical integrity, SP3 sit#10 should be replaced with a board that has to_call > 0. If only the label matters for model training, accept it as is. **Issue #1 — design inconsistency, labelling correct. Owner decision: accept or replace.**

### Flag 4: SP10 IP thin value CALL count — 2 confirmed, not 3

**Agent 3 finding:** The brief requires minimum 3 situations with is_ip == 1 AND hero_range_percentile >= 0.75 in SP10. The allocation provides only 2 qualifying situations: SP10_10 (B03, range_pct=0.75, is_ip=1) and SP10_11 (B11r, range_pct=0.78, is_ip=1). The third candidate, SP10_09 (B28, range_pct=0.72, is_ip=1), falls below the 0.75 threshold by 0.03.

**Reviewer assessment:** Agent 3 correctly identified and flagged this. The allocation table's sit#9 is set at range_pct=0.72 by the board architect. Raising it to 0.76 fixes the IP contrast count but drops the 0.65-0.75 band to 2 situations (below the minimum of 3 for that band). The two constraints are in conflict: either the IP thin value count is 2 (below minimum), or the 0.65-0.75 band count is 2 (below minimum).

The allocation table as designed cannot simultaneously satisfy both constraints. This is an allocation-level error, not a design agent error.

**Options:**
a. Accept 2 IP thin value CALLs (instead of 3) — shortfall of 1 in the IP contrast set.
b. Accept the 0.65-0.75 band having 2 situations (instead of 3) by raising SP10_09 to 0.76.
c. Add a new SP10 situation on an IP board at range_pct 0.75-0.80 — but that would bring SP10 to 14 situations, breaking the total of 151.

There is no clean resolution within the current 151-situation framework. **Issue #4 — allocation-level constraint conflict. Requires owner decision. Reviewer recommends option (a): accept 2 IP thin value CALLs, as the downstream impact on model training is marginal at -1 situation from a 13-sit pool, and the 0.65-0.75 band minimum of 3 is a harder constraint.**

### Flag 5: B12 flush_danger boundary at 0.35

**Agent 3 finding (SP7_22, SP7_24 on B12):** B12 is a three-club turn (7c 2d Kc Ac). flush_danger is specified at 0.35 in the SP7 allocation table. The Step 4 condition requires flush_danger <= 0.35. These two situations are exactly at the boundary.

**Reviewer assessment:** 0.35 satisfies "flush_danger <= 0.35" exactly. The hands are RAISE at the boundary. No compliance failure. However, this is the tightest possible flush_danger value for SP7, and the board has three clubs — a significantly flushed texture. The GTO soundness of a thin-value OOP check-raise at flush_danger=0.35 on a three-club board is worth noting. The Step 4 condition formally passes. Flagged for awareness only; no action required.

---

## 5. Additional Issues Identified

### Issue A: SP1_10 and SP1_09 — same hero cards on B12

SP1_09: B12, hero ['Kh', 'Kd'] — set of kings (RAISE)
SP4_03: B12, hero ['Kh', 'Kd'] — set of kings (CALL, S3 suppressor)
SP3_07: B12, hero ['Kh', 'Kd'] — set of kings (RAISE)

Three situations share the same board (B12) and the same hero cards (['Kh', 'Kd']). The labels differ (RAISE for SP1 and SP3, CALL for SP4) because the villain aggression count differs between the sub-patterns. The factory should produce three distinct situation rows, which is correct if each row carries distinct feature values (aggr_count). However, having identical hero_cards on the same board across three different sub-patterns could confuse a model that does not attend carefully to aggr_count. This is a design concern, not a conflict. **Flagged for awareness: the factory brief should ensure these three rows have explicitly distinct aggr_count values.**

### Issue B: SP2_09/SP1_15/SP4_06 — same hero cards on B20

SP1_15: B20, hero ['Qc', 'Qd'] — RAISE (SP1 monster wet board)
SP2_09: B20, hero ['Qc', 'Qd'] — RAISE (SP2 low SPR commit)
SP4_06: B20, hero ['Qc', 'Qd'] — CALL (S5 suppressor fires)

Same hero cards, same board, different labels (two RAISE, one CALL). Again, label differs only because of context features (num_callers_to_bet, SPR as treated by different steps). Same concern as Issue A. **Flagged for awareness only — the factory must supply distinct context features for each row.**

### Issue C: SP8_10 initial hand correction

Agent 4 caught mid-document that their initial SP8_10 hero hand ['Jc', 'Th'] on B26 created a straight (K-Q-J-T-9 using board cards). The agent correctly revised to ['Jc', '8d']. The final submitted hand is correct. No conflict. Mentioned here to confirm the correction was applied.

---

## 6. Summary of Required Actions Before Factory Build

| # | Issue | Severity | Action required |
|---|-------|----------|-----------------|
| 1 | SP3 sit#10 B17 is a lead not check-raise | DESIGN | Owner decision: accept label-correct-but-structure-inconsistent, or replace with a board that has to_call > 0 |
| 2 | SP6_12 flush_block_pct=0 interpretation depends on feature extractor implementation | BLOCKER | Confirm flush_block_pct definition in feature_extractor.py before build. If Ac on clubs board produces block_pct > 0, redesign SP6_12 |
| 3 | S4 threshold ambiguity: "spr >= 6.0" vs "spr > 6.0" — affects SP1 sits 1-3 on B05 | BLOCKER | GTO Expert or owner must decide: is threshold inclusive (>= 6.0) or exclusive (> 6.0)? Update RAISE_DECISION_TREE_V2.md before build |
| 4 | SP10 IP thin value CALL count = 2, brief requires 3 | DESIGN | Owner decision: accept shortfall of 1, or restructure SP10 allocation (impacts total count) |

Issues #2 and #3 are blockers — they will produce incorrect labels if unresolved. Issues #1 and #4 are design quality concerns with correct labels.

---

## 7. What Passed Without Issues

- All 151 card conflicts: zero conflicts found across all agents
- SP5 flush_draw_rank >= 12: all 28 situations confirmed
- SP5 flush_block_pct > 0: all 28 situations confirmed
- SP6 failure modes: all 6 modes present, minimum counts met
- SP7 is_monster == 0: all 25 situations confirmed
- SP8 river-only (street == 2): all 16 confirmed
- SP8 range_pct <= 0.20: all 16 confirmed
- SP9 flat-spot triggers: all 10 triggers correctly applied
- SP1/SP2/SP3/SP4 monster quality: all hands are genuine is_monster == 1 hands
- Distribution: 151 total, correct per-sub-pattern counts
- Band distributions (SP7, SP8, SP10): all bands meet minimum counts (except SP10 IP thin value shortfall noted)
- fold_equity ranges for SP5 (0.45-0.70), SP7 (0.40-0.65), SP8 (0.50-0.72): all within spec

---

**Review complete.** Two blockers (Issues #2 and #3) must be resolved before factory generation begins. The card-conflict gate, which is the primary risk identified in the review brief, is fully clear across all 151 situations.
