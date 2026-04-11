# Review: BOARD_ALLOCATION_V4_BET.md

**Date:** 9 April 2026
**Reviewer:** Independent Reviewer
**Files read:**
- `review/BOARD_ALLOCATION_V4_BET.md` (primary)
- `review/FACTORY_DESIGN_BET_CONTEXTS.md` (brief)
- `review/BET_DECISION_TREE_V1.md` (tree reference)

**Verdict: ISSUES FOUND**

---

## Checklist Results

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | All boards have to_call = 0 | PASS | All 24 board definitions show to_call=0; action histories confirm hero is never facing a live bet |
| 2 | PFA boards: hero_pos == opener_position | PASS | BP1/BP2/BP3 boards consistently have hero as the preflop raiser |
| 3 | Non-PFA boards: hero_pos != opener_position | PASS | BP4/BP5 heroes are cold-callers or defenders throughout |
| 4 | Action histories valid | FAIL | B4_03 has an incorrect action order — see Issue 1 |
| 5 | No Section 8 open items | PASS | Section 8 removed; 6 corrections documented and applied |
| 6 | Card conflicts checked | PASS | Full conflict table for all 24 boards; 5 boards revised; new boards B4_19-B4_24 verified |
| 7 | BP6 isolated from BP1-BP5 | SOFT FAIL | B4_22 shared between BP6-G and BP5 — see Issue 2 |
| 8 | At least 1 paired board | PASS | B4_23 (5c 5d Ah) |
| 9 | SPR variation documented per sub-pattern | PASS | SPR assignment table in Section 3; 5 distinct SPR values across batch |
| 10 | Position distribution ~55-65% IP | PASS | ~63 IP sits of ~104 total = ~61% |
| 11 | Texture tiers: at least 3 boards per tier | PASS | Tier 1: 6+, Tier 2: 9, Tier 3: 2 explicit boards (B4_08, B4_10) — marginal but 6 Tier 3 situations covered |
| 12 | Total situation count matches brief (~100) | FAIL | Actual total is 104 — see Issue 3 |

---

## Issues Found

### Issue 1 — CRITICAL: B4_03 Action History Has Incorrect Postflop Order

**Board:** B4_03 (`Ah 8s 3d`), hero_pos=CO, villain_positions=[BB, BTN]

**Observed action history:**
```
(preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
(flop, BB, check), (flop, BTN, check)
```

**Problem:** In a 3-way pot with CO, BTN, and BB, standard postflop action order is BB → CO → BTN (earliest position acts first; BTN acts last as dealer). The action history shows BTN checking before CO acts, which means CO is listed as acting after BTN. This is non-standard and implies BTN has no further action on the street after CO — which is incorrect. CO should act second, BTN last.

**Correct action history should be:**
```
(preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
(flop, BB, check), (flop, CO, check or bet) → then BTN acts
```

For BP1 use (IP PFA c-bet), CO as the PFA acts second (between BB and BTN) — CO is OOP relative to BTN, not IP last to act. The board's own note acknowledges this: "CO is IP relative to BB; BTN checked before hero acts — CO is between BB and BTN positionally." This note is self-contradictory. If BTN checked before hero acts, then BTN acts before CO, which reverses the standard order.

**Impact:** The board is described as IP for BP1 purposes, but the positional logic is confused. CO is NOT the last to act in this configuration — BTN is. The BP2 usage of this board (CO as OOP PFA) is correctly described. The BP1 usage claiming CO is "IP last to act" is wrong.

**Required fix:** Either (a) change the BP1 hero position for B4_03 to BTN (BTN opens, CO calls, BB calls — BTN is then correctly IP and last to act), or (b) retain CO as hero but correctly label this as an OOP scenario and remove from BP1 (IP) usage. The action history for B4_03 as written cannot produce an IP CO hero in a standard dealt hand.

---

### Issue 2 — MODERATE: B4_22 Shared Between BP6-G and BP5 Violates Brief Requirement

**Brief requirement (R1, Board Uniqueness):**
> "BP6 boards must not overlap with BP1-BP5 boards (purpose: prevents model from seeing the same board produce both BET and CHECK, which could create position-correlated confusion)"

**B4_22 usage:**
- BP5 sit 9: BB bets two pair or better (BET intent)
- BP5 sit 10: BB bets two pair (BET intent)
- BP6-G sit 8: BB traps with a set (CHECK intent)

The allocation justifies this on the grounds that the hand strength differs (set traps CHECK; two pair bets BET). The training contrast is described as "intentional." However, the brief's prohibition is not conditioned on hand strength — it is a blanket board-level isolation requirement. The same board appearing with the same OOP BB position in both BET and CHECK situations is exactly the pattern the brief is designed to prevent: the model sees B4_22 OOP and must infer from hand strength whether to bet or check, which is a harder learning signal than having distinct boards for each label class.

**Severity:** Moderate. The allocation's justification is reasonable from a GTO standpoint (set traps on dry boards is correct) but it does not satisfy the brief's isolation requirement. If the factory situation agent assigns sufficiently different hand features, the model may still learn correctly — but the risk of positional confusion is real.

**Required action:** Either (a) replace BP6-G with a new dedicated board (B4_25 with a different low rainbow layout), or (b) escalate to owner for explicit exception approval with acknowledgment that the brief's R1 isolation requirement is not met.

---

### Issue 3 — MODERATE: Total Situation Count is 104, Not 100

**Brief target:** 100 situations.

**Actual allocation:**
- BP1: 30
- BP2: 15
- BP3: 22 (expanded from 20 — BP3 turn fix added 2 sits)
- BP4: 15
- BP5: 12 (expanded from 10 — B4_22 and B4_24 added 2 sits)
- BP6: 10
- **Total: 104**

The allocation document acknowledges BP3 at 22 and BP5 at 12 in the section summaries but never updates the batch total or flags the discrepancy from the 100-situation brief target. The opening summary table still shows 100.

**Impact:** Minor on data quality (4 extra situations is not harmful), but the allocation does not acknowledge or justify the overrun. The factory situation agent will generate 104 rows. Any downstream count checks expecting 100 will fail.

**Required action:** Either trim 4 situations from BP3 or BP5 to return to 100, or document the overrun explicitly and confirm owner acceptance of 104.

---

### Issue 4 — MODERATE: BP2 Sits 13-15 Have villain_air_pct = 0.38, Below the Step 3B Gate of 0.40

**BP2 sits 13-15** use board B4_13 (turn, Ad 7c 2s Kh) with villain_air_pct=0.38.

**Step 3B requires:** villain_air_pct >= 0.40 (ALL conditions required — this is explicit in both the tree and the brief).

**The allocation self-notes this:** "villain_air_pct: 0.38-0.50 (all >= 0.40 except B4_13 at 0.38 — B4_13 is A-K-7-2 turn, villain_air is slightly lower on turn after range narrowing)" and concludes PASS.

**This conclusion is incorrect.** 0.38 < 0.40. Step 3B will not fire for sits 13-15. These 3 situations are designed as BET-intent (BP2) but will label CHECK because the critical gate fails. The allocation's self-declared PASS is wrong.

**Impact:** 3 of 15 BP2 situations (20%) will not fire BET. The labelling yield from BP2 drops from the expected ~13-14 BET labels to ~10-11. This is within acceptable yield range but the situations are mislabelled in intent.

**Required fix:** Raise villain_air_pct to >= 0.40 for B4_13 BP2 situations. On a turn board of Ad 7c 2s Kh after a checked flop, a BTN cold-caller's air fraction narrows somewhat but A-K-7-2r still misses a high fraction of BTN's range (QJo, QTo, JTo, 98s have no pair here). 0.40 is achievable — the 0.38 estimate is conservative and could be revised to 0.40-0.42 with justification.

---

### Issue 5 — MODERATE: BP3 4D Sits 21-22 Have villain_air_pct = 0.29, Below the Step 4D Gate of 0.40

**BP3 4D sits 21-22** use board B4_16 (turn, Qc 7d 3h Kd) with villain_air_pct=0.29.

**Step 4D requires:** villain_air_pct >= 0.40 (explicit condition in sub-condition 4D).

**The allocation shows 0.29 for both sits 21 and 22.** No flag is raised in the allocation document.

**Impact:** Step 4D will not fire for sits 21-22. These situations will label CHECK, not BET. Two of the 5 BP3 4D situations (40%) will produce wrong-direction labels for their designed intent.

**Required fix:** Raise villain_air_pct to >= 0.40 for sits 21-22, or replace B4_16 for 4D use with a board where villain_air is achievably >= 0.40. B4_16 is a K-high turn (Qc 7d 3h Kd) — a CO/HJ opener's range on K-high hits fairly well (K-x combos pair, A-high has overcards). villain_air_pct of 0.29 is plausible for this board. A different board (e.g., a K-high rainbow with wider villain misses) may be needed.

---

## Spot-Check Action History Summary

| Board | Check | Result |
|-------|-------|--------|
| B4_01 | BTN raises, SB/BB call, SB/BB check flop → BTN acts | VALID |
| B4_03 | CO raises, BTN/BB call, BB/BTN check flop → CO acts | INVALID — BTN acts after CO in standard order, not before |
| B4_13 | BTN raises, SB/BB call, all check flop, SB/BB check turn → BTN acts | VALID |
| B4_15 | CO raises, BTN/BB call, all check flop, BB/CO check turn → BTN acts | VALID |
| B4_17 | CO raises, BTN/SB call, all check flop, SB acts first on turn | VALID |
| B4_20 | CO raises, BTN/BB call; CO bets flop + turn (villain_aggr=2); BB acts first on river | VALID |

---

## Items That Are Correct and Need No Action

- All 24 boards have to_call=0.
- PFA/non-PFA structural assignment is correct across all sub-patterns.
- Card conflict checking is thorough and all revisions are correct.
- Section 8 is cleared — all 6 original open items resolved.
- Paired board requirement met (B4_23).
- SPR variation is documented and substantially improved over prior batches.
- BP6 failure modes: all 7 modes (A through G) are present and the failed conditions are correctly identified.
- BP2 villain_aggression_count=0 enforced for all 15 situations.
- BP5 villain_aggression_count=0 enforced for all 12 situations.
- Rainbow board overage (13 vs max 8) is design-driven and documented with justification — acceptable.
- River board shortfall (1 situation vs 5-10 brief target) is documented and accepted — river c-bets are correctly described as rare.

---

## Summary of Required Actions

| Priority | Issue | Action |
|----------|-------|--------|
| CRITICAL | B4_03 action history / IP claim wrong | Fix BP1 positional structure for B4_03: use BTN as hero (BTN opens, CO calls, BB calls) OR remove B4_03 from BP1 IP usage |
| MODERATE | BP2 sits 13-15 villain_air_pct = 0.38 (below 0.40 gate) | Revise to 0.40-0.42; document reasoning |
| MODERATE | BP3 4D sits 21-22 villain_air_pct = 0.29 (below 0.40 gate) | Revise to >= 0.40 or replace B4_16 for 4D situations |
| MODERATE | Total count is 104, brief target is 100 | Trim 4 sits or document overrun with owner acknowledgment |
| MODERATE | B4_22 shared between BP5 and BP6-G (violates brief R1 isolation) | Add B4_25 for BP6-G or escalate for owner exception approval |

The allocation is substantially correct and represents careful work. Issues 1, 4, and 5 are the most likely to cause downstream labelling errors. Issues 3 and 2 are documentation/policy items.

**Board Architect should revise and resubmit before factory situation generation begins.**
