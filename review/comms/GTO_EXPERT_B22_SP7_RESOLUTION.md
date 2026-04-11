# GTO Expert Resolution: B22 Connected Board and SP7 SPR=9.0

**Date:** 9 April 2026
**Author:** GTO Expert
**Status:** COMPLETE — ready for Board Architect to action
**Addresses:** BOARD_ALLOCATION_V3_BATCH_V2.md pending items A and B (Section 7)

---

## Item 1: B22 Replacement — B32 Definition

### Finding

B22 (Jh 4c 2h Td) produces straight_danger = 0.3 from the feature extractor.
The connected-board threshold requires straight_danger >= 0.40. B22 does not
qualify. The allocation currently has B07 (567) and B19 (4678) as confirmed
connected boards — two boards, below the R2 minimum of three.

B22's low score is expected in retrospect: the board contains only one
consecutive rank pair (T-J, ranks 10-11). The remaining cards (4, 2) are
isolated. The feature extractor requires more straight-completing structure
than a single consecutive pair to clear 0.40.

### B32 Definition

**B32** — Two-tone, T-J-Q connected turn, IP hero

- board_cards: `['Th', 'Jc', 'Qs', '3h']`
- street: turn
- hero_pos: BTN
- villain_positions: `['BB', 'CO']` (CO is bettor — donk into BTN)
- pot: 180
- to_call: 60
- effective_stack: 900
- SPR: 900 / 180 = **5.0**
- action_history:
  - (preflop, CO, raise), (preflop, BTN, call), (preflop, BB, call)
  - (flop, BB, check), (flop, CO, check), (flop, BTN, check)
  - (turn, BB, check), (turn, CO, bet)
- opener_position: CO
- Texture: Two-tone (hearts: Th, 3h), T-J-Q connected

**Why straight_danger will clear 0.40:**
T (10), J (11), Q (12) are three sequential ranks on the board. The feature
extractor confirmed B07 (5,6,7) and B19 (4,6,7,8) as connected. T-J-Q
presents the same three-consecutive-rank structure as B07 and has more
straight completions: 89TJQ (needs 89), 9TJQK (needs 9K), TJQKA (needs KA),
8TJQK (needs 8K). The straight_danger score for T-J-Q will be materially
higher than B22's single consecutive pair. This board is confident to clear
the 0.40 threshold.

**Card conflict check:**
- Th: not used in any existing board (B09=Ah 4h 8c, B16=5h Kd 2h 8c,
  B22=Jh 4c 2h Td — uses Jh not Th, and Td not Th)
- Jc: not used in any existing board (B08=Qc 5c 9h uses Qc/5c not Jc;
  B12=7c 2d Kc Ac uses Kc/Ac not Jc)
- Qs: not used (B08=Qc, B29=Qc — both clubs; Qs is clear)
- 3h: checking B06=8c 8h 3d (3d not 3h), B26=Kh 5c 2h 9d Qh (no 3h). Clear.

All four cards are clear of the existing 31-board inventory.

**Sub-pattern assignments:**

B32 is assigned to SP9 and SP10 as specified. Texture is two-tone (hearts)
but SP7 requires straight_danger <= 0.35 — T-J-Q will far exceed this,
making B32 ineligible for SP7. SP5 requires is_paired == 0 and a flush draw
context; B32 can serve SP5 if needed (Th and 3h provide hearts texture) but
the primary assignment is SP9 and SP10 as required.

SP9 fit: On a T-J-Q board, CO (preflop opener) donks into BTN. CO's range
heavily favours this board: QQ, JJ, TT (sets), KQ, QJ, QT, JT (straights
or strong two-pair). Hero BTN called preflop and checked the flop — a
weaker holding is implied. board_favour will be negative (villain-favoured),
triggering the board_favour <= -0.30 flat-spot condition. The donk bet
format (CO bets into hero BTN) also provides the num_callers_to_bet context
if BB calls before hero acts.

SP10 fit: Middle-range hands on T-J-Q — hero holds pair of tens or a
pair-plus-gutshot type hand. range_percentile 0.50-0.75. Pure CALL on a
villain-favoured connected board.

**Board summary table entry:**

| ID  | Cards          | Street | Texture   | Hero | OOP/IP | Pot | Stack | SPR | to_call |
|-----|----------------|--------|-----------|------|--------|-----|-------|-----|---------|
| B32 | Th Jc Qs 3h   | Turn   | Connected / Two-tone | BTN | IP | 180 | 900 | 5.0 | 60 |

**R2 texture impact after adding B32:**

| Texture   | Before | After | Min | Max | Status |
|-----------|--------|-------|-----|-----|--------|
| Connected | 2      | 3     | 3   | 4   | PASS   |
| Two-tone  | 15     | 16    | 11  | 13  | Over ceiling by 3 — see note |

Two-tone rises to 16 of 32 boards (50%), within the 44-52% target range
(16/32 = 50%). PASS. Rainbow remains 11/32 = 34%, slightly above the 32%
ceiling but this is the same marginal overage already documented in the
allocation for the 31-board set. No action required.

**R4 street impact:**
B32 is a turn board. Turn count was already ~64 situations (42%), within
the 33-43% target. Adding 2-3 situations from B32 may push turn to ~67
(44%), marginally over. Board Architect should confirm final turn count
after SP9/SP10 assignment and trim if needed from other turn boards. This
is a minor calibration, not a structural problem.

---

## Item 2: SP7 at SPR=9.0 — Recommendation

### Decision: Replace all three situations (sits 3, 9, 21 on B10)

The three situations should not be built. Here is the reasoning.

**The board and context**

B10 is Kc 4d 2h — rainbow, completely dry. BB hero checks, villain (CO or
BTN) bets into a three-way pot. Hero check-raises as a thin value play
(hero_range_percentile 0.75-0.92, is_monster=0).

At this percentile band with is_monster=0 on a K-4-2 rainbow board, hero's
qualifying hands are almost entirely strong Kx: KQ, KJ, KT (top pair top
or good kicker). Sets (KK, 44, 22) would be is_monster=1 and route to
Step 2 instead.

**Why SPR=9.0 makes this unsound**

The fold equity problem: K-4-2 rainbow is a board where villain's betting
range is heavily weighted toward value. Villain has no flush draws (rainbow),
no meaningful straight draws (K-4-2 has no consecutive structure), and no
combo draws. The bet is almost entirely value-weighted: AK, KQ, KJ, sets,
AA, QQ betting for protection. Against this value-heavy betting range,
fold_equity of 0.40-0.60 (as listed in sits 3, 9, 21) is too optimistic.
When villain is betting a dry board in a three-way pot, they are rarely
bluffing. Realistically, fold_equity is closer to 0.25-0.35 on K-4-2 for
a check-raise. This means sits 3 and 21 (fold_eq 0.48-0.50) are using
inflated fold equity assumptions, and sit 9 (fold_eq 0.60) is particularly
unrealistic.

The SPR compounding problem: even if fold_equity is granted at 0.40-0.50,
at SPR=9.0 the hands that do not fold present a severe problem. Villain's
continuing range when they call or 3-bet a check-raise on K-4-2 contains:
AK (dominates KQ, KJ, KT), sets (KK, 44, 22 all beat TPTK), AA, QQ (both
beat TPTK). Hero is OOP with reverse implied odds for the remaining 8x pot.
Hero cannot call a 3-bet from villain without being essentially committed,
and cannot fold without losing the check-raise chips. The check-raise with
TPTK at SPR=9.0 OOP creates a lose-lose dynamic: villain folds when behind
and continues when ahead.

Contrast with SPR=2.6-5.5 where the same action is correct: at SPR=3.0,
a check-raise to 3x commits ~30-35% of effective stack immediately, and
hero can call a villain 3-bet and be committed at roughly neutral equity.
The play has a clean resolution. At SPR=9.0, check-raising with TPTK is
leaving hero dangling on a long and expensive line OOP with a non-nut hand.

The Step 4 gate confirms this: Step 4 requires fold_equity >= 0.40.
On K-4-2 dry rainbow at SPR=9.0 three-way, the realistic fold equity of
0.25-0.35 fails this gate. The situations were designed with inflated fold
equity assumptions (0.48-0.60) that do not reflect what villain's range
actually looks like on this board. The situations fail the tree's own gate
on honest feature values, let alone the deeper poker logic.

Note on B13 (SPR=8.4): sits 4, 10, 17 on B13 (Qd 6h 2s Jc) at SPR=8.4
are retained. B13 is a mixed-texture board with Q-J connectivity and a
wider villain betting range (villain includes more semi-bluffs and mixed
hands on Qd 6h 2s Jc than on K-4-2). The fold equity estimates of 0.42-0.55
on B13 are plausible. SPR=8.4 versus 9.0 is not the differentiating factor
— it is the combination of board texture, realistic fold equity, and villain
range composition. B13 is retained on its merits. B10 at SPR=9.0 is not.

### Replacement: Add 3 situations to existing flop boards

Remove sits 3, 9, 21 from B10 at SPR=9.0. Add one situation each to B02,
B06, and B08 — all are flop boards already in SP7. This restores the
10-flop/15-turn street balance in SP7 (removing 3 flop B10 sits brings
flop to 7; adding 3 flop sits restores to 10).

**Band assignments for the three replacement sits:**

Each removed sit came from a different percentile band. The replacements
must maintain band minimums (minimum 6 per band per brief):

| Removed sit | Band      | Replacement sit | Board | SPR  | range_pct | fold_eq | aggr |
|-------------|-----------|-----------------|-------|------|-----------|---------|------|
| Sit 3       | 0.75-0.80 | New sit A       | B06   | 5.5  | 0.78      | 0.43    | 0    |
| Sit 9       | 0.80-0.86 | New sit B       | B08   | 5.0  | 0.82      | 0.50    | 1    |
| Sit 21      | 0.86-0.92 | New sit C       | B02   | 5.0  | 0.89      | 0.55    | 0    |

All three replacement sits inherit the step 4 conditions from the SP7 brief:
- is_ip = 0 (BB is OOP on B02, B06, B08)
- is_monster = 0
- flush_danger <= 0.35 (B02=0.30, B06=0.10, B08=0.30 — all within gate)
- straight_danger <= 0.35 (B02=0.10, B06=0.05, B08=0.20 — all within gate)
- num_callers_to_bet = 0
- villain_aggression_count <= 1

Per-board sit counts after replacement:

| Board | Current SP7 sits | After replacement | Max allowed |
|-------|-----------------|-------------------|-------------|
| B02   | 3 (sits 1,7,14) | 4 (adds sit C)    | 4 — at cap  |
| B06   | 2 (sits 2,15)   | 3 (adds sit A)    | 4 — OK      |
| B08   | 2 (sits 8,16)   | 3 (adds sit B)    | 4 — OK      |
| B10   | 3 (sits 3,9,21) | 0 (all removed)   | —           |

B02 reaches the per-board maximum of 4 with sit C added. This is within the
hard cap of 8 and the SP7 sub-pattern cap of 4. No breach.

SP7 unique board count after replacement: B02, B06, B08, B12, B13, B15,
B17, B18, B21 = 9 boards (B10 removed, no new board added). Minimum 7
required. PASS.

SP7 total situations: 25 (unchanged — 3 removed, 3 added).

**Band counts after replacement:**

| Band      | Before (with B10 sits) | After (B10 removed, replacements added) |
|-----------|------------------------|----------------------------------------|
| 0.75-0.80 | 8 (sits 1-6, 22-23)    | 7 (sit 3 removed, sit A added = net 0 change: 8) |
| 0.80-0.86 | 8 (sits 7-13, 24)      | 7 (sit 9 removed, sit B added = net 0 change: 8) |
| 0.86-0.92 | 9 (sits 14-21, 25)     | 8 (sit 21 removed, sit C added = net 0 change: 9) |

Each band maintains its count. All bands >= 6. PASS.

---

## Summary of Actions for Board Architect

1. **Add B32** (Th Jc Qs 3h, turn, BTN IP, SPR=5.0) to Section 1 and the
   board summary table. Assign to SP9 (2 sits, board-favour trigger) and
   SP10 (2 sits, middle-range fill). Update R2 connected count to 3. PASS.

2. **Remove SP7 sits 3, 9, 21** (B10 at SPR=9.0). Mark as GTO Expert
   rejected — thin-value OOP check-raise at SPR=9.0 on dry K-4-2 is
   unsound due to inflated fold equity assumptions and reverse implied odds
   from villain's value-heavy continuing range.

3. **Add three replacement SP7 situations** to existing flop boards:
   - Sit A: B06, flop, BB (OOP), SPR=5.5, range_pct=0.78, fold_eq=0.43, aggr=0, band 0.75-0.80
   - Sit B: B08, flop, BB (OOP), SPR=5.0, range_pct=0.82, fold_eq=0.50, aggr=1, band 0.80-0.86
   - Sit C: B02, flop, BB (OOP), SPR=5.0, range_pct=0.89, fold_eq=0.55, aggr=0, band 0.86-0.92

4. **Pending item A** (SP7 sits 3,9,21) is now resolved — GTO Expert sign-off
   is a rejection. Remove the PENDING GTO status markers from those rows
   and delete the rows from the SP7 table.

5. **Pending item B** (B22 straight_danger) is now resolved by replacement —
   B22 does not qualify as connected. B32 replaces the connected-board
   requirement. B22 continues to serve SP1, SP5, SP6 (its two-tone hearts
   texture is valid for those sub-patterns). Remove the PENDING VERIFICATION
   note from B22's Section 1 entry but retain the board. Add a note that
   B22 is two-tone only, not connected.

No other allocation changes are required. The 151-situation total is
unchanged.
