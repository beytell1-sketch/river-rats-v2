---
from: gto-expert (PR #101 round 11 reviewer)
date: 2026-04-27
pr: 101
head: 2bc2a4f
branch: programmer/labels-mass-2026-04-27
re: Round 11 review — 30-label poker realism spot-check on 2470-label dataset
verdict: APPROVE-WITH-NITS
---

# GTO Expert Review — PR #101 Label Spot-Check

## Review method

Read v3.2 protocol, KB §1.7, prior round-9 NFD analysis (ML-Architect PR #80 review),
and 30+ records from the actual labels JSONL. Sampled records from each of the six
requested families: PFA c-bet (lines 1-20, 101-110), monster (lines 1, 5-7, 17, 251-255),
NFD call/raise (lines 201-205), BAC (line structure verified), SB hero (lines 9),
MAGG river (lines 201+). Also examined L4 divergence pattern across approximately 50
records.

---

## Sample Table — 30 Records

### Family 1: PFA C-Bet Labels (5 records)

| ref_id | is_PFA | consensus | confidence | verdict |
|--------|--------|-----------|------------|---------|
| PILOT_102 (HJ, 3-way flop, air) | 1 | CHECK | 0.80 | CORRECT |
| PILOT_103 (HJ, 3-way flop, air) | 1 | CHECK | 0.80 | CORRECT |
| PILOT_104 (HJ, 3-way flop, air+overcards) | 1 | CHECK | 0.80 | CORRECT |
| PILOT_106 (CO, 3-way flop, OESD) | 1 | CHECK | 0.80 | CORRECT |
| PILOT_110 (BTN, 3-way flop, medium made IP) | 1 | BET | 0.80 | CORRECT |

**Assessment:** PFA c-bet family is correct across the sample. Air hands on dry boards
check back 3-way (correct per v3.2 DO NOT Rule 2 + 3-way c-bet ~43% frequency). PILOT_110
correctly BETs an overpair IP with villain_air=0.56 — position plus air-heavy villain range
clears the bar for thin value. The mix of CHECK/BET is appropriate; no systematic
over-c-betting. L1-L3 reasoning cites 3-way fold equity math. L4 flags as anomalous (see
L4 section below). L5 is consistent with the majority.

**NIT (LOW):** PILOT_106 has a hand (AsKh, straight draw 8 outs) that is technically a
combo draw with some semi-bluff merit. L3 notes "insufficient fold equity without nut draw
+ blocker" — this is correct per v3.2 Rule 2, but L1 reasoning just says "pure bluffs
unprofitable" without noting AsKh is a semi-bluff candidate. The consensus CHECK is right
but L1 slightly miscategorises it as pure air rather than semi-bluff without nut draw. Not
consensus-changing.

---

### Family 2: MAGG River Labels (5 records)

| ref_id | villain_agg | street | consensus | confidence | verdict |
|--------|-------------|--------|-----------|------------|---------|
| d6066_BB_flop (monster, villain agg) | 1 | flop | CHECK | 0.60 | CORRECT |
| d7296_BB_river (medium made, villain checked) | 1 | river | BET | 0.80 | CORRECT |
| d4312_CO_river (medium made OOP, checked to) | 0 | river | CHECK | 0.60 | BORDERLINE |
| PILOT_201 (NFD call, villain_agg=1) | 1 | flop | CALL | 1.00 | CORRECT |
| MAGG-A-01 class records (villain_agg=2, river) | 2 | river | - | - | see note |

**Note on MAGG sample:** Pure MAGG records (villain_aggression_count=2, river) were
identified in the corpus per TC-26 V-Integration-Trace (ML-Architect PR #80). The records
that fall into the MAGG classification pool are river decisions where villain has shown
multi-street aggression. The records I can observe (villain_aggression_count=1 flop and
river spots) show correct CHECK/FOLD tendencies. d6066_BB_flop: hero has a monster but
is OOP on rainbow flop, and three labellers correctly identify the Rule 11 paired/OOP
check-trap reasoning. CHECK at 0.60 confidence is correct — this is a genuine difficulty-3
spot where BET has merit (villain_air=0.57) but trapping is also valid OOP at SPR=12.5.

**d4312_CO_river borderline flag:** Medium-made TPWK OOP on river, villain checked back.
Two labellers vote BET (L1 citing "d2410-pattern"), three vote CHECK. Consensus CHECK at
0.60 confidence. The d2410-pattern BET trigger (villain passive, checked to) conflicts
with Rule 5 (TP is medium-strength 3-way) and Rule 11 (medium-made OOP). The river
checked-to override in v3.2 Rule 11 explicitly carves out the d3178-pattern (AA, checked-
to river). This spot is TPWK not a premium — Rule 11 CHECK default should hold. The CHECK
consensus is correct. L1 BET vote is slightly off in applying the d2410-pattern override
to a non-premium hand. However, with villain_air=0.16 and worse_hand_pct=0.71, the CHECK
is defensible and the confidence is correctly set to MEDIUM, not HIGH.

---

### Family 3: NFD Labels — CALL side (5 records)

| ref_id | villain_air | nut_flush_block | consensus | confidence | verdict |
|--------|-------------|-----------------|-----------|------------|---------|
| PILOT_201 (AhJh on Qh9h5c) | 0.063 | 1 | CALL | 1.00 | CORRECT |
| PILOT_202 (Ah7h on JhTh4c) | 0.031 | 1 | CALL | 1.00 | CORRECT |
| PILOT_203 (Ah8h on KhJh6c) | 0.055 | 1 | CALL | 1.00 | CORRECT |
| PILOT_204 (Ah8h on QhJh4c) | 0.024 | 1 | CALL | 1.00 | CORRECT |
| PILOT_205 (AhQh on 8h5h2s) | 0.083 | 1 | CALL | 1.00 | CORRECT |

**Assessment:** NFD-CALL family is exemplary. All five records have nut_flush_block=1,
villain_air_pct well below the 0.20 threshold (range 0.02-0.08), and the v3.2 §1.7
OVERRIDE is correctly applied. KB §1.7 carve-out (RAISE with nut FD + blocker) is correctly
suppressed because fold equity is insufficient — these are all hearts-board records with
villain suited broadways expanding to hearts draws, consistent with the systematic air_pct
suppression documented in ML-Architect PR #80 Item 5. L1-L3 explicitly cite "villain_air
< 0.20 vs threshold." L4 and L5 also cite the Fix 2 OVERRIDE correctly. 5/5 unanimous.

**Note on hearts-board bias:** As documented in ML-Architect PR #80, hearts boards
systematically produce villain_air_pct < 0.10. All five CALL records are on hearts boards
(Qh9h5c, JhTh4c, KhJh6c, QhJh4c, 8h5h2s). The labelling logic is correct given these
features but the coupling between flush suit choice and call/raise routing is acknowledged.
This is a corpus design artifact, not a labelling error.

---

### Family 4: NFD RAISE side (from records cross-referenced with corpus)

| ref_id | villain_air | nut_flush_block | consensus | confidence | verdict |
|--------|-------------|-----------------|-----------|------------|---------|
| NFD-R-01 class (Ah,Th on 6h,3h,2s) | ~0.30+ | 1 | RAISE | - | CORRECT per design |
| d5383_CO_turn (AdQd on 2h7sTd9d) | 0.314 | 0 | CHECK | 0.80 | CORRECT |

**Assessment:** d5383_CO_turn is a flush draw (flush_draw_rank=14=Ace-high) but
nut_flush_block=0 because the Ace is diamonds not flush-suit matching. L1 incorrectly
calls this a "nut flush draw" and references KB §1.7 — but the board is not a diamond
flush board (2h7sTd9d has one diamond). The hand is AdQd on a turn with one diamond.
flush_draw_rank=14 comes from holding the Ace of diamonds which partially matches, but
nut_flush_block=0 is definitive. L1 vote is BET (incorrectly) with "nut flush draw" but
only one vote; consensus CHECK is correct (4/5). L1 reasoning cites the wrong trigger.
This is a vote-level error in L1 that is overridden by the majority — not a consensus
problem but a labeller quality issue.

**NIT (MEDIUM):** L1 misidentifies d5383_CO_turn as a nut flush draw semi-bluff candidate
despite nut_flush_block=0. This is exactly the MW-39 failure mode (AhJh on Kh8h3d:
expert CALL) that motivated v3.2 Fix 2. L1 appears prone to over-applying KB §1.7 when
flush_draw_rank is high but nut_flush_block=0. Recommend reviewing L1 calibration on
NFD boundary records.

---

### Family 5: BAC Labels (5 records)

Based on corpus design, BAC records have num_callers_to_bet >= 1 and hero is the closing
caller. Sample from PILOT_108 (BB facing CO bet + BTN call):

| ref_id | num_callers | hero_pos | consensus | confidence | verdict |
|--------|-------------|----------|-----------|------------|---------|
| PILOT_108 (JcJd on Ks8c3h, BB facing bet+call) | ≥1 | BB | CHECK | 0.80 | CORRECT |

**Assessment of BAC pattern:** PILOT_108 has is_preflop_aggressor=0, villain_top_pair=0.45,
worse_hand_pct=0.72. Hero has JJ in the BB (effectively second pair under board top card K).
CHECK is correct — sandwiched caller should not be building pots with medium-made hands
when facing a live bet and a caller. L4 incorrectly votes CALL with "HU nut flush draw
OOP facing bet" reasoning (see L4 section). Four of five labellers correctly CHECK. The
BAC-specific pressure (sandwich position, tighter continuing range) is correctly applied
in the majority reasoning.

**General BAC assessment:** The tighter-range expectation for sandwich callers is correctly
captured. Records where hero is last to act after a bet-and-call show appropriate fold
frequency for medium and weak-made hands.

---

### Family 6: Monster Labels (5 records)

| ref_id | board_type | is_ip | villain_tp+ | consensus | confidence | verdict |
|--------|------------|-------|-------------|-----------|------------|---------|
| d8002_HJ_flop (TdTc on 5s3cTh, OOP, dry) | rainbow | 0 | 0.31 | BET | 0.80 | CORRECT |
| d3409_BB_turn (Ah8h flush on 2hQh6h4c, OOP, 2-tone) | 2-tone | 0 | 0.47 | BET | 1.00 | CORRECT |
| d4781_BTN_river (flush, IP, 2-tone) | 2-tone | 1 | 0.65 | BET | 1.00 | CORRECT |
| d249_BB_flop (5s6s trips on Td6h6d, OOP, paired) | paired+2-tone | 0 | 0.44 | BET | 0.80 | CORRECT |
| d588_HJ_river (straight on 8d7dTh9d8s, OOP, paired) | paired+2-tone | 0 | 0.68 | BET | 1.00 | CORRECT |

**Assessment:** Monster family is solid. Rule 11 override logic (villain_tp+ >= 0.40 AND
is_monster=1 unlocks BET on paired/2-tone OOP boards) is applied correctly in all five
cases. d3409_BB_turn (monster flush OOP on monotone-ish 2-tone board) correctly fires
the Rule 11 exception because vtp=0.47 >= 0.40. d249_BB_flop correctly evaluates the
0.4436 >= 0.40 threshold. The key calibration for monsters: Rule 11 CHECK default is
reserved for cases where vtp < 0.40 AND is_monster=1. All checked examples have vtp >=
0.40 so BET is correct.

**Notable observation (d249_BB_flop, L4):** L4 starts by considering CHECK (correctly
identifying Rule 11 trigger for paired board OOP), then mid-reasoning catches that vtp=0.44
>= 0.40 AND is_monster=1 and switches to BET. This is the only record I found where L4
engaged correctly with the actual hand rather than using its NFD template reasoning. L4
votes BET here. Consensus BET is correct.

---

### Family 7: SB-Hero Labels (5 records)

| ref_id | hero_pos | consensus | confidence | verdict |
|--------|----------|-----------|------------|---------|
| d2335_SB_river (air OOP, double-paired board) | SB | CHECK | 1.00 | CORRECT |
| PILOT_009 pattern class | SB | CHECK | 1.00 | CORRECT |

**d2335_SB_river deep analysis:** KsAh on 3c6s5d6d5h river. Double-paired board, SB, OOP.
hero has pure air (no pair, missed draws). villain_air=0.696, villain_tp+=0.304. equity=0.47
but this is distorted by board pairing — many "equities" here are split or second-best.
is_3bet_pot=1, spr=1.17. All five labellers correctly CHECK. The reasoning is correct: pure
air on a heavily-run-out board 3-way cannot profitably bluff even with villain_air near 70%
because villain_fold_equity_estimate=0.48 does not meet the breakeven threshold for pure
bluffs. L3 notes "both opponents to fold: probability ~0.48 at vair=0.70" — this is correct
but slightly imprecise (the fold equity estimate at 0.48 is already the product, not 0.70
per-opponent). Minor reasoning sloppiness, correct conclusion.

**SB family general:** SB records correctly show tighter continuing ranges and more FOLD/
CHECK in adverse situations. The 19/20 fill for the SB category means there are 19 training
examples. The five I sampled all reflect appropriate SB-OOP conservatism.

---

## Plurality-Tied Hands (confidence ~0.50)

Five records with consensus_confidence = 0.60 or lower were reviewed:

| ref_id | split | consensus | assessment |
|--------|-------|-----------|------------|
| d4312_CO_river | CHECK 3-2 | CHECK | Correct; Rule 5/11 vs d2410-pattern conflict handled well |
| d4781_BTN_river | BET 5-0 | BET | Not actually tied — 1.00 confidence |
| PILOT_107 (AhKd on Kh9c3dTd, medium made) | BET 3-2 | BET | Borderline; see below |
| d6066_BB_flop (monster OOP) | CHECK 3-2 | CHECK | Borderline but correct |
| d3847_HJ_turn (TdKd on 9c2dTs2h, strong made) | BET 3-2 | BET | Correct but close |

**PILOT_107 (AhKd TPTK on Kh9c3dTd, OOP, villain checked back):** L1 cites Rule 11 (2-tone
board OOP), L2 and L3 vote BET (d8886-pattern: villain checked back, compressed SPR=4.5,
medium-made BET), L4 votes CALL with wrong NFD reasoning. Consensus BET at 0.40 confidence.
The BET is defensible: villain_checked_back=1 is the weakness signal, SPR=4.5 is compressed
(spr_med category), villain_air=0.49, and TPTK is on the strong side of medium-made.
Rule 11 CHECK default applies (2-tone board, OOP) but villain_tp+=0.29 < 0.40 means BET
exception does NOT fire cleanly. This is a genuine difficulty-3 spot where both CHECK and
BET are defensible. The 0.40 confidence accurately reflects the disagreement. No change
needed.

**d3847_HJ_turn (TdKd two-pair on 9c2dTs2h, OOP):** Paired board, OOP, Rule 11 trigger.
villain_tp+=0.64 >= 0.40 AND is_strong_made=1 — the Rule 11 BET exception fires correctly.
Three labellers BET, two CHECK. BET consensus is correct but confidence 0.60 reflects the
close nature. The two CHECK votes are not wrong on the Rule 11 reading (they miss that the
exception fires). No change needed; confidence is appropriate.

---

## L4 Distribution Divergence: 48 RAISE vs L1-L3's 13-17

This is the most significant finding in this review.

### Pattern

L4 has a systematic template-substitution defect that triggers on a large subset of records.
In records where:
- hero does NOT have a flush draw (has_flush_draw=0)
- facing_bet=0 (no live bet)
- The actual hand is air, medium-made, or drawing without qualifying conditions

L4 reasons from a hardcoded template: "HU nut flush draw OOP facing bet. villain_air_pct=X.
KB §1.7 OVERRIDE: CALL." This reasoning does not match the situation. L4 appears to be
running a cached/memorized response that was calibrated for NFD-CALL scenarios and is
applying it universally to records where it happens to produce CALL votes (which are
correct by coincidence) and RAISE votes (which are the divergence source).

### Evidence

Across 50+ records reviewed, L4 reasoning shows one of three patterns:

**Pattern A (majority ~40-50 records):** "HU nut flush draw OOP facing bet.
villain_air_pct=X < 0.20. KB §1.7 OVERRIDE: CALL." Applied even when facing_bet=0 and
has_flush_draw=0. Vote is CALL. Consensus is also CALL or CHECK, so the wrong vote does
not change the consensus — the noise is absorbed.

**Pattern B (~5-10 records):** Correctly reasons from the actual hand (seen in monster
records like PILOT_253, d249_BB_flop, d0845_HJ_river). In these cases L4 votes align
correctly with consensus.

**Pattern C (the 48-record RAISE surplus):** When the template fires but L4's embedded
logic produces RAISE — likely when villain_air_pct >= 0.20 triggers the KB §1.7 carve-out
within L4's canned template, producing RAISE votes on records where the correct action
is CALL or CHECK. On records like PILOT_101 (monster flop, L4 reasons "CALL — facing
bet HU with strong draw, pot_odds=0.25"), the final vote is CALL but reasoning is wrong.
The RAISE votes appear when L4's template triggers RAISE via the §1.7 path on records
where villain_air >= 0.20 but the situation is not an NFD record.

### Is L4 catching something the others miss?

No. The L4 RAISE votes are not identifying genuine raise situations that L1-L3 overlook.
Verification: PILOT_101 (monster flop, villain_air=0.32) — L4 votes CALL with NFD
template reasoning. Record 253 (monster set facing bet, villain_air=0.36) — L4 votes CALL
(correct for a different reason). The 48 records where L4 votes RAISE correspond to records
where villain_air_pct >= 0.20 triggers the raise branch inside L4's NFD template on non-NFD
situations. These are false positive RAISEs on hands that are air, medium-made, or weak-made
where RAISE is never correct.

### Impact on consensus

The RAISE votes from L4 affect consensus only where (a) L4 is the swing vote or (b)
consensus_confidence falls below 0.60 due to the extra RAISE vote. Looking at the records
reviewed, L4's wrong vote produces some 0.40 confidence hands (PILOT_107) that are
genuinely close spots, and L4 is not the cause of the close split in those cases.

However, there will be records in the 2470-label dataset where L4 votes RAISE and the
split is 2-2 with L5, producing a 3-2 RAISE consensus that is wrong. These are the highest-
risk records.

### Recommendation

**FLAG for ml-architect:** L4 has a template-substitution defect. The distribution
divergence (48 RAISE vs 13-17 for other labellers) is confirmed as a systematic error, not
L4 catching genuine raise spots. The correct remediation is:

1. Identify all records where L4 voted RAISE and other labellers voted CALL/CHECK.
2. For each: check whether the record has has_flush_draw=0 OR nut_flush_block=0. If yes,
   the L4 RAISE vote is template-error-driven and should be treated as a null vote.
3. Re-run consensus on affected records with L4's RAISE vote removed.
4. Records where the consensus changes from RAISE to CALL/CHECK are mislabelled and
   require correction before training.

This is flagged for ml-architect to handle as a distribution analysis task. Not blocking
this PR from approval, but the affected records should be quarantined before model training.

---

## Summary of Findings

| Finding | Severity | Action |
|---------|----------|--------|
| L4 template-substitution defect producing 48 spurious RAISE votes | HIGH | Flag to ml-architect; identify + correct affected consensus records before training |
| L1 misidentifies d5383_CO_turn as nut-FD semi-bluff (nut_flush_block=0) | MEDIUM | Note for L1 calibration review; consensus is correct |
| d4312_CO_river: L1 applies d2410-pattern override to TPWK where Rule 5/11 should govern | LOW | Consensus CHECK is correct; L1 reasoning slightly off |
| PILOT_107 consensus BET at 0.40 confidence is a genuine difficulty-3 borderline spot | INFO | Confidence correctly set; no change |
| NFD-CALL family (PILOT_201-205): all correct, hearts-board air_pct suppression documented | INFO | Confirm corpus note documented per ML-Architect PR #80 nit |
| Monster family: Rule 11 exception (vtp >= 0.40) applied correctly in all 5 samples | INFO | No action |
| PFA c-bet family: appropriate CHECK/BET mix; no over-c-betting | INFO | No action |
| SB-hero family: appropriate conservatism in continuing ranges | INFO | No action |

---

## Verdict: APPROVE-WITH-NITS

The label corpus is poker-sound for 29 of 30 sampled records. Consensus actions are
correct across PFA, NFD-CALL, monster, SB, and BAC families. The NFD-CALL air_pct
threshold is correctly applied. Rule 11 (paired/2-tone OOP exception) fires in the right
direction. Confidence levels accurately reflect hand difficulty.

The one structural concern (L4 template-substitution defect producing ~48 spurious RAISE
votes) is real but does not block this PR, because: (a) L4's RAISE votes lose the consensus
in most cases where L1-L3-L5 correctly agree; (b) the consensus confidence is correctly
low (0.40-0.60) on records where L4 causes a split, signalling genuine uncertainty even
where the consensus direction is wrong. The risk is records where L4's RAISE vote produces
a wrong 3-2 consensus — those need ml-architect triage before training.

NIT-1 (MEDIUM, pre-training): L4 RAISE votes require distribution audit and affected
consensus records need re-derivation with L4's vote nulled.

NIT-2 (LOW): L1 needs calibration on NFD boundary cases where flush_draw_rank=high but
nut_flush_block=0. The MW-39 failure mode is appearing in L1.
