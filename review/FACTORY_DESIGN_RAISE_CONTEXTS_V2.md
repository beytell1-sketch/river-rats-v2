# Factory Design Brief: RAISE Context Situations — v2

**Date:** 9 April 2026
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Supersedes:** FACTORY_DESIGN_RAISE_CONTEXTS.md
**Purpose:** Fill the RAISE training gap (40 current → 150-160 needed)
**Tree version:** RAISE_DECISION_TREE_V2.md (approved)

---

## Changelog

All changes are driven by the four items flagged in the Factory Brief
Impact section of RAISE_DECISION_TREE_V2.md, plus the SP7 threshold
correction noted in the update brief.

**Item 13 — SP5 tightened to v2 Step 5 (RAISE count reduced 20 → 16):**
v1 SP5 had no nut-draw quality gate. v2 Step 5 requires BOTH
`flush_draw_rank >= 12` AND `flush_block_pct > 0`. SP5 RAISE count
is reduced from 20 to 16 to reflect the narrower qualifying set.
The description now explicitly states both conditions as requirements.
Four situations that would have qualified under v1 (nut draw, no
blocker OR non-nut draw with blocker) have been moved to SP6 as CALL
counterexamples (see Item 13 additions to SP6 below).

**Item 9 — SP6 gains nut-draw-without-blocker CALL example (+1 CALL):**
A new explicit CALL counterexample is added to SP6: flush_draw_rank
>= 12 (nut draw) AND flush_block_pct == 0 (no blocker) → CALL.
This is a defined branch in v2 Step 5 and needs a factory situation
to train it.

**Item 13 additions to SP6 (+4 CALL):**
Four situations displaced from SP5 (non-qualifying under v2 gate)
are re-homed in SP6 as CALL counterexamples: draws with nut rank but
no blocker, and draws with blocker but below nut threshold.

**SP6 total CALL count:** 8 (original) + 1 (Item 9) + 4 (Item 13) = 13.

**Item 10 — SP10 gains mid-draw zone CALL examples (+5 CALL):**
Five new CALL examples are added to SP10 for the mid-draw zone:
hero_range_percentile 0.70–0.80 with draw_outs 6–8. These hands
fail Step 3 (requires percentile >= 0.90) and fail Step 5 (requires
draw_outs >= 9). They are unambiguous CALL situations that the model
previously had no examples for in this specific zone.

**SP10 total CALL count:** 8 (original) + 5 (Item 10) = 13.

**SP7 fold_equity threshold corrected (0.30 → 0.40):**
v2 Step 4 raises the fold_equity threshold from >= 0.30 to >= 0.40.
SP7 description is updated accordingly. No count change — the 15
RAISE examples remain, but all situations must now use
villain_fold_equity_estimate >= 0.40 (not >= 0.30).

**v2.1 — Distribution rebalance (+30 RAISE to reach expert targets):**
Owner flagged that the v2 brief fell ~30 RAISE short of the 150-160
target and the distribution was skewed toward value. Analysis showed
self-play and existing labels contribute almost exclusively value RAISE,
leaving semi-bluff, thin value, and bluff under-represented. Added:
- +12 SP5 semi-bluff (16→28)
- +10 SP7 thin value (15→25)
- +8 SP8 bluff (8→16)
No value additions needed — value is already over-supplied from other
sources. Total factory RAISE: 79→109. Total new situations: 121→151.

**Item 8 — CALL count reconciliation (32 → 42):**
The v1 brief had 32 in the totals table and 43 in the summary line.
Neither was correct. The correct count is derived by summing CALL
examples across all sub-patterns after the above changes:
SP4 (6) + SP6 (13) + SP9 (10) + SP10 (13) = 42.
The summary line is updated to 42. The figure of 43 that appeared
in the handoff document was an approximation; 42 is the reconciled
count. See Totals table below.

---

## Summary

151 new situations needed across 10 sub-patterns.
~109 are RAISE labels, ~42 are CALL labels (counterexamples).

**Distribution target (expert-derived, 28-source research):**
40% value, 30% semi-bluff, 20% thin value, 10% bluff.
Factory RAISE counts are set to close the gap after accounting for
self-play (~37 RAISE, mostly value) and existing 406 relabelled
(~30-35 RAISE, mostly value). Semi-bluff, thin value, and bluff
are the categories that need factory volume most.

---

## Sub-patterns (priority order)

### Priority 1: Semi-bluff boundary (most common error)

**SP5: Semi-bluff raises (28 RAISE examples)**

Qualifying conditions (ALL required — v2 Step 5):
- draw_outs >= 9
- flush_draw_rank >= 12 (nut or near-nut: Q/K/A of flush suit)
- flush_block_pct > 0 (hero holds at least one blocker to villain's flush)
- villain_fold_equity_estimate >= 0.45
- villain_aggression_count <= 1
- is_paired == 0

Boards: two-tone flops and turns with nut flush draws, varied positions.
Hero must hold a card >= Q in the flush suit AND have flush_block_pct > 0.
Example qualifying holding: AsQs on a Ks-Jd-5s board (nut draw + blocker).
Example non-qualifying: 8s7s on same board (nut draw, no blocker → SP6 CALL).
Example non-qualifying: As-9h on Ks-Jd-5s (blocker but non-nut draw → SP6 CALL).

Note on count change from v1: The v1 brief allocated 20 RAISE examples
to SP5. Four of those would have been non-qualifying under the v2 nut-draw
gate (situations with flush_draw_rank < 12 OR flush_block_pct == 0). Those
four have been moved to SP6 as CALL counterexamples per Item 13. Twelve
additional situations added (v2.1) to close the semi-bluff gap: self-play
and existing factory contribute almost no semi-bluff RAISE, so factory
must carry this category. 28 total ensures varied board textures (two-tone
flops, two-tone turns, mono flops) with distinct feature profiles across
all qualifying situations.

**SP6: Semi-bluff suppressed — CALL (13 CALL examples)**

Original 8 CALL examples (fold_equity or aggression-based suppressors):
- Same nut-draw + blocker setup as SP5 but fold_equity < 0.45 → CALL
- villain_aggression_count >= 2 with draw → CALL
- is_paired == 1 with draw → CALL
- draw_outs < 9 (gutshot only) → CALL

Item 9 addition (1 new CALL example — nut-draw-without-blocker):
- flush_draw_rank >= 12 (nut draw, e.g. 8s7s on spade board)
- flush_block_pct == 0 (no blocker to villain's flush)
- draw_outs >= 9, villain_fold_equity_estimate >= 0.45 (all other
  SP5 conditions met — only the blocker gate fails)
- Label: CALL
- Training purpose: teaches the model that a nut draw alone does not
  justify a semi-bluff raise when hero cannot reduce villain's
  continuing range.

Item 13 additions (4 new CALL examples — v1 situations displaced by v2 gate):
- 2 situations: flush_draw_rank >= 12, flush_block_pct == 0,
  draw_outs >= 9 (nut draw, no blocker — same class as Item 9 but
  with varied board textures)
- 2 situations: flush_draw_rank 9–11 (below nut threshold), flush_block_pct
  > 0, draw_outs >= 9 (blocker present but non-nut draw)
- All other SP5 conditions met; only the v2 nut-draw gate fails
- Label: CALL
- Training purpose: shows the model the full boundary of the v2 gate —
  both failure modes (no blocker, non-nut draw) produce CALL.

Total SP6: 13 CALL examples. Feature profiles must be distinct across
all 13 to prevent the model collapsing them to a single pattern.

### Priority 2: Suppress overfit (prevent raise-bias)

**SP9: Flat spots — CALL only (10 CALL examples)**

Bet-and-call non-monster (num_callers_to_bet >= 1, is_monster == 0),
board heavily favouring villain (board_favour <= -0.30,
villain_range_capped == 0), multi-street aggressor non-monster
(villain_aggression_count >= 2, is_monster == 0). All CALL.

No change from v1.

**SP4: Monster suppressors — CALL (6 CALL examples)**

is_monster == 1 but a Step 2 suppressor fires:
- S2: paired board with flush danger (flush_danger >= 0.60, is_paired == 1)
- S3: multi-street aggressor (villain_aggression_count >= 2)
- S4: high SPR IP (spr >= 6.0, is_ip == 1) — threshold is 6.0 per v2 S4,
  not the v1 value of 4.0. Any SP4 situations using spr 4.0–5.9 must be
  revised to spr >= 6.0 to match the tree.
- S5: bet-and-call monster below top 8% of range
  (num_callers_to_bet >= 1, hero_range_percentile < 0.92)

All CALL. No count change from v1. Verify that all 6 situations use
spr >= 6.0 for the high-SPR-IP suppressor (not the old 4.0 threshold).

### Priority 3: Value raise inventory

**SP1: Monster + wet board + low SPR (18 RAISE examples)**

Set or two-pair on flush_danger >= 0.40 boards, spr <= 2.5,
no Step 2 suppressors firing. Raise to charge draws and protect.
hand_category >= 10 (two_pair or better — per v2 S1 encoding).

No change from v1 count. Note that v2 S1 uses hand_category >= 10
(not the informal "two-pair+" phrasing). All 18 situations must use
hand_category >= 10 to be consistent.

**SP2: Monster + dry board + low SPR commit (10 RAISE examples)**

Set on dry board (flush_danger <= 0.20, straight_danger <= 0.20),
spr <= 1.5. Step 3 fires (stack-off). hero_range_percentile >= 0.90
required (raised from v1's 0.80 per v2 Step 3).

Note: Any v1 SP2 situations that used hero_range_percentile 0.80–0.89
are now sub-threshold for Step 3. Those situations should use
hero_range_percentile >= 0.90 in the v2 factory build.

No count change from v1.

**SP3: Monster + OOP check-raise (12 RAISE examples)**

Monster OOP facing bet, moderate SPR (2.0–3.5), no suppressors.
villain_aggression_count <= 1, is_ip == 0.

No change from v1.

### Priority 4: Thin value

**SP7: OOP thin value check-raise (25 RAISE examples)**

ALL of the following required (v2 Step 4):
- hero_range_percentile >= 0.75
- is_monster == 0
- is_ip == 0 (OOP only)
- villain_fold_equity_estimate >= 0.40 (UPDATED from v1's 0.30)
- villain_aggression_count <= 1
- flush_danger <= 0.35
- straight_danger <= 0.35
- num_callers_to_bet == 0

OOP check-raise, near-top-of-range non-monster hand. Boards should
be dry (low danger scores). Count raised from 15 to 25 (v2.1):
self-play and existing factory contribute almost no thin value RAISE,
so factory must carry this category toward the 20% distribution target.
Additional 10 situations should vary: street (flop vs turn), SPR
(2.0-3.5), hero_range_percentile (0.75-0.90), and board texture.

Critical update: the fold_equity floor is now 0.40, not 0.30. Any
situation designed with villain_fold_equity_estimate 0.30–0.39 does
NOT qualify as a v2 SP7 RAISE. If such situations appear in the build,
they should be labelled CALL (they fall below Step 4's threshold and no
other step fires for a non-monster OOP hand in this range percentile).
Do not use the 0.30 threshold.

Note: IP thin value at this percentile (is_ip == 1, is_monster == 0,
hero_range_percentile >= 0.75) = CALL (explicitly stated in v2 Step 4).
SP7 must be OOP only.

### Priority 5: Bluff and fill

**SP8: Bottom of range bluff raise (16 RAISE examples)**

ALL of the following required (v2 Step 6):
- street >= 2 (river only — v2 added this gate; flop/turn bluff
  raises do NOT qualify)
- hero_range_percentile <= 0.20
- villain_fold_equity_estimate >= 0.50
- villain_top_pair_plus_pct <= 0.35
- num_callers_to_bet == 0
- villain_aggression_count == 0

River-only bluff raises. Hero holds bricked draw or air.
Count raised from 8 to 16 (v2.1): self-play contributes zero bluff
RAISE (conservative oracle), so factory must carry the full 10%
distribution target. Additional 8 situations should vary:
villain_fold_equity_estimate (0.50-0.70), villain_top_pair_plus_pct
(0.15-0.35), hero hand type (bricked flush draw, bricked straight
draw, complete air). Critical: all 16 situations must be river
(street == 2). Any situation set on flop or turn does not qualify
under v2.

**SP10: Middle range CALL fill (13 CALL examples)**

Original 8 CALL examples:
hero_range_percentile 0.40–0.65, moderate draws (4–6 outs), moderate
danger. Pure CALL. Prevents model overgeneralizing to mid-range hands.

Item 10 additions (5 new CALL examples — mid-draw zone):
- hero_range_percentile 0.70–0.80 (above the original SP10 range
  but below Step 3's 0.90 threshold)
- draw_outs 6–8 (below Step 5's 9-out threshold)
- flush_danger and straight_danger varied (0.20–0.50)
- villain_fold_equity_estimate varied (0.30–0.55, straddling SP7's
  threshold to make these clearly non-SP7 as well — is_monster == 0,
  spr > 1.5 so Step 3 does not fire)
- Label: CALL
- Training purpose: these hands occupy a gap that previously had no
  examples — they look like potential raises (decent percentile, some
  draw equity) but fail every RAISE gate in the tree. The model needs
  to see them labelled CALL.

Total SP10: 13 CALL examples.

---

## Totals

| Type | Count | % of factory RAISE |
|------|-------|--------------------|
| RAISE (value: SP1 + SP2 + SP3) | 40 | 37% |
| RAISE (semi-bluff: SP5) | 28 | 26% |
| RAISE (thin value: SP7) | 25 | 23% |
| RAISE (bluff: SP8) | 16 | 15% |
| CALL (SP4 monster suppressors) | 6 | — |
| CALL (SP6 semi-bluff suppressed) | 13 | — |
| CALL (SP9 flat spots) | 10 | — |
| CALL (SP10 middle range fill) | 13 | — |
| **Total new** | **151** | |

RAISE total: 40 + 28 + 25 + 16 = **109 factory RAISE**.
CALL total: 6 + 13 + 10 + 13 = **42 CALL counterexamples**.

**Projected total RAISE across full training set:**
- Existing 406 relabelled with v2 tree: ~30-35 (mostly value)
- New factory: 109
- Self-play (200 rows): ~37 (mostly value)
- **Total: ~176-181 RAISE**

This exceeds the 150-160 target, which provides buffer for labelling
yield (not every designed-RAISE situation will be labelled RAISE by
the expert — some will be called CALL after full-context evaluation).

**Projected distribution (factory + self-play + existing):**

| Category | Target % | Factory | Other sources | Projected total | Projected % |
|----------|----------|---------|---------------|----------------|-------------|
| Value | 40% | 40 | ~65 | ~105 | ~58% |
| Semi-bluff | 30% | 28 | ~7 | ~35 | ~19% |
| Thin value | 20% | 25 | ~2 | ~27 | ~15% |
| Bluff | 10% | 16 | ~0 | ~16 | ~9% |

Value is over-represented due to self-play and existing labels, which
are overwhelmingly value RAISE. This is a known structural bias in the
data sources. The factory deliberately over-weights semi-bluff, thin
value, and bluff relative to value to compensate. The model's class
weighting (RAISE cap 3.0) will further address any residual imbalance.

If actual labelling yield is closer to target (some projected value
RAISEs may be relabelled CALL by v2 suppressors), the distribution
will improve. Assess after relabelling in Step 7.

---

## Design constraints — correctness

- All boards must pass the action sequence validator
- Hero cards must not conflict with board cards
- No duplicate boards from existing 46 factory boards
- Bettor goes LAST in villain_positions list
- No expected labels in designs — Expert labels fresh
- SP5: every situation must have flush_draw_rank >= 12 AND
  flush_block_pct > 0 (both conditions, not one)
- SP7: every situation must have villain_fold_equity_estimate >= 0.40
- SP8: every situation must have street == 2 (river)
- SP4: every high-SPR-IP situation must have spr >= 6.0 (not 4.0)
- SP2: every situation must have hero_range_percentile >= 0.90 (not 0.80)
- hand_category references must use numeric encoding (>= 10 for two_pair+)
  not informal labels

---

## Diversity requirements (from FACTORY_DIVERSITY_AUDIT.md)

These requirements are mandatory. They address structural problems
found in existing batches: SPR=1.11 uniformity (53% of Batch 1),
65% OOP bias, villain-feature clustering within board groups, and
paired-board under-representation. Full audit and rationale in
review/FACTORY_DIVERSITY_AUDIT.md.

### R1. Board uniqueness
- Minimum **25 unique boards** across all 151 situations
- Maximum **8 situations per board** (prefer 6)
- **No board reuse** from existing 46 factory boards

### R2. Board texture distribution (of 25+ boards)
| Texture | Min boards | Max boards | % range |
|---------|-----------|-----------|---------|
| Rainbow | 6 | 8 | 24–32% |
| Two-tone | 11 | 13 | 44–52% |
| Monotone (flop) | 1 | 2 | 4–8% |
| Paired | 2 | 3 | 8–12% |
| Connected (straight_danger >= 0.40) | 3 | 4 | 12–16% |
| River runouts with flush completion | 2 | 3 | — |

### R3. SPR distribution (of 151 situations)
| SPR tier | Min % | Max % |
|----------|-------|-------|
| 1.0–2.0 | — | 25% |
| 2.0–4.0 | 30% | — |
| 4.0–8.0 | 25% | — |
| 8.0+ | 15% | — |

No more than 20% of situations may share the same SPR value
(within +/- 0.15 tolerance). This directly counters the Batch 1
SPR=1.11 uniformity problem. Use effective_stack proportional to
pot to achieve realistic SPR values (e.g., pot=90, effective_stack=900
gives SPR=10).

### R4. Street distribution (of 151 situations)
| Street | Min | Max |
|--------|-----|-----|
| Flop | 40 (27%) | 55 (36%) |
| Turn | 50 (33%) | 65 (43%) |
| River | 35 (23%) | 50 (33%) |

River increased relative to existing batches because SP8 (16
situations) requires street=2.

### R5. Position distribution (of 151 situations)
| Position | Min | Max |
|----------|-----|-----|
| OOP (BB, SB) | 55 (36%) | 70 (46%) |
| IP (BTN, CO, HJ) | 80 (53%) | 95 (63%) |

Corrects existing 65% OOP bias.

### R6. Boards per sub-pattern
| Sub-pattern | Size | Min unique boards | Max situations/board |
|-------------|------|-------------------|---------------------|
| SP1 | 18 | 6 | 3 |
| SP2 | 10 | 4 | 3 |
| SP3 | 12 | 5 | 3 |
| SP5 | 28 | 7 | 4 |
| SP7 | 25 | 7 | 4 |
| SP8 | 16 | 5 | 3 |
| SP4 | 6 | 4 | 2 |
| SP6 | 13 | 5 | 3 |
| SP9 | 10 | 4 | 3 |
| SP10 | 13 | 5 | 3 |

### R7. Villain-feature variance within sub-patterns (size >= 8)
For each sub-pattern with 8+ situations, measure (max - min)
across all situations in that sub-pattern:
| Feature | Min range |
|---------|-----------|
| villain_fold_equity_estimate | >= 0.20 |
| villain_top_pair_plus_pct | >= 0.10 |
| board_favour | >= 0.15 |
| flush_danger | >= 0.10 (where flush-relevant) |

---

## Per-sub-pattern variation requirements

### SP1 (18 RAISE): Monster + wet board + low SPR
- flush_danger: span 0.40–0.75
- SPR: span 1.0–2.5 (min 3 at SPR <= 1.5, min 3 at SPR 2.0–2.5)
- hand_category: include both two_pair (10-11) and set (12+)
- Street: mix flop and turn
- Min 6 unique boards

### SP2 (10 RAISE): Monster + dry board + low SPR commit
- hero_range_percentile: span 0.90–0.98 (not all at 0.90)
- SPR: span 0.8–1.5
- hand_category: min 3 two_pair, min 5 set
- villain_fold_equity_estimate: vary (teaches model SP2 doesn't require fold equity)
- Min 4 unique boards (2 flop, 2 turn)

### SP3 (12 RAISE): Monster + OOP check-raise
- SPR: span 2.0–3.5, min 3 distinct values
- Street: mix flop and turn
- Board texture: min 2 rainbow, 2 two-tone, 1 paired
- hero_range_percentile: span 0.90–0.99
- Min 5 unique boards

### SP5 (28 RAISE): Semi-bluff raises
- flush_danger: span 0.20–0.60
- flush_draw_rank: min 8 at rank 14, min 8 at rank 13, min 6 at rank 12
- flush_block_pct: span 0.05–0.35
- villain_fold_equity_estimate: span 0.45–0.70
- villain_aggression_count: include both 0 and 1
- Street: min 10 turn, min 14 flop
- Position: min 10 OOP, min 10 IP
- Min 7 unique boards

### SP6 (13 CALL): Semi-bluff suppressed
- All 6 failure modes must appear:
  1. fold_equity < 0.45 (min 2 situations)
  2. villain_aggression_count >= 2 (min 2)
  3. is_paired == 1 (min 2)
  4. draw_outs < 9 (min 2)
  5. flush_draw_rank < 12 (min 1)
  6. flush_block_pct == 0 (min 2)
- Min 5 unique boards (min 3 for fold-equity mode)
- No duplicate hero_cards within sub-pattern on same board

### SP7 (25 RAISE): OOP thin value check-raise
- hero_range_percentile: span 0.75–0.92 (min 6 per band: 0.75–0.80, 0.80–0.86, 0.86–0.92)
- villain_fold_equity_estimate: span 0.40–0.65 (min 5 at 0.40–0.50, min 5 at 0.55–0.65)
- flush_danger: span 0.05–0.35
- straight_danger: span 0.05–0.35
- SPR: span 2.0–3.5
- Street: target 10 flop, 15 turn
- villain_aggression_count: include both 0 and 1
- Min 7 unique boards

### SP8 (16 RAISE): Bottom of range bluff raise
- hero_range_percentile: span 0.02–0.20 (min 4 at 0.02–0.08, min 4 at 0.12–0.20)
- villain_fold_equity_estimate: span 0.50–0.72
- villain_top_pair_plus_pct: span 0.10–0.35
- Hero hand types: min 4 bricked flush draw, min 4 bricked straight draw, min 4 pure air
- Board texture: min 2 flush-possible runouts, min 2 rainbow runouts
- All 16 must be river (street == 2)
- Min 5 unique boards, max 3 per board

### SP4 (6 CALL): Monster suppressors
- All 4 suppressors (S2, S3, S4, S5) must appear at least once
- S4 situations must use spr >= 6.0
- Recommend 2 each for S3 and S4, 1 each for S2 and S5

### SP9 (10 CALL): Flat spots
- All 3 triggers must appear (min 3 each)
- board_favour: span -0.30 to -0.60
- villain_aggression_count: use both 2 and 3

### SP10 (13 CALL): Middle range fill
- hero_range_percentile: span 0.40–0.80 in 4 bands (min 3 per band)
- draw_outs: span 0–8 (include 0, 4–6, 6–8)
- Min 3 situations with is_ip == 1 AND hero_range_percentile >= 0.75
  (teaches IP thin value = CALL, contrasting with SP7 OOP = RAISE)
- Min 3 boards with flush_danger 0.20–0.50

---

## Reviewer checklist (diversity gate)

The reviewer must document all 14 checks before the batch is approved:

1. Count unique boards >= 25; none in existing 46-board list
2. Max situations per board <= 8
3. Monotone flop boards <= 2
4. SPR distribution across 4 tiers; no tier > 25%
5. OOP situations <= 70
6. River situations >= 35
7. SP5 unique boards >= 7
8. SP5 flush_draw_rank, flush_block_pct, fold_equity ranges meet minimums
9. SP7 hero_range_percentile, fold_equity ranges meet minimums
10. SP8 unique river boards >= 5; all situations at street == 2
11. SP4 S4 situations have spr >= 6.0
12. SP10 has >= 3 situations with is_ip == 1 AND percentile >= 0.75
13. Every sub-pattern (size >= 8): fold_equity range >= 0.20
14. No duplicate hero_cards within sub-pattern on same board

---

## Tree version alignment check

| Tree step | Key threshold | Brief sub-patterns affected | Status |
|-----------|--------------|----------------------------|--------|
| Step 2 S1 | hand_category >= 10 | SP1, SP4 | Updated (encoding note added) |
| Step 2 S4 | spr >= 6.0 | SP4 | Updated (was 4.0 in v1) |
| Step 3 | hero_range_percentile >= 0.90 | SP2 | Updated (was 0.80 in v1) |
| Step 4 | fold_equity >= 0.40 | SP7 | Updated (was 0.30 in v1) |
| Step 5 | flush_draw_rank >= 12 AND flush_block_pct > 0 | SP5, SP6 | Updated |
| Step 6 | street >= 2 | SP8 | Updated (gate added) |
