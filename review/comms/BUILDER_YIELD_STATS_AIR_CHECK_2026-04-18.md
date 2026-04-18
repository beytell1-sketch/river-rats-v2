---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 Layer 2 — AIR-CHECK generator yield stats
status: READY FOR REVIEW — awaiting labelling go-ahead for 3-way set
---

# Builder Yield Stats — AIR-CHECK Counter-Examples

Per MAIN_TERMINAL_DECISION_2026-04-18-h (95e9221). Generator built,
10-spec yield probe done, full run complete. Incorporates both
blocker resolutions (Path B / turn-shifted litmus, Path B / HU
data prep unlabelled).

## Commits

- Generator: `review/generate_air_check_v231.py` (this commit)
- Output: `training-data/v23_air_check_3way.jsonl` (this commit)
- Output: `training-data/v23_air_check_hu.jsonl` (this commit)

## Run stats

```
[3-way]   generated=40  build_fail=0  pred_fail=0  valid_fail=0  clean=40
[HU]      generated=30  build_fail=0  pred_fail=0  valid_fail=0  clean=30
written 3-way: 40/40  predicate pass-through: 100%
written HU:    30/30  predicate pass-through: 100%
preflight schema: ALL PASS
litmus: BOTH PRESENT (LITMUS_A4d_Qs5s7s_turn, LITMUS_T5h_JJ2_turn)
```

## Predicate integrity — every row passes every condition

| Condition | 3-way | HU |
|---|---|---|
| `facing_bet=0` | 40/40 | 30/30 |
| `villain_checked_back=1` | 40/40 | 30/30 |
| `num_opponents` (2 / 1) | 40/40 | 30/30 |
| `is_made_hand=0` | 40/40 | 30/30 |
| `draw_outs <= 2` | 40/40 | 30/30 |
| `equity_vs_range < 0.35` | 40/40 | 30/30 |
| `has_errors=False` | 40/40 | 30/30 |

## Litmus seeds

Both build cleanly, pass predicate, present in final 3-way output.

```
LITMUS_A4d_Qs5s7s_turn:
  hero=Ad4d  board=Qs5s7sKc  street=turn
  fb=0  vcb=1  n_opp=2  is_made=0  outs=0
  equity_vs_range=0.036  hrp=0.957  board_adjusted_hrp=0.035

LITMUS_T5h_JJ2_turn:
  hero=Th5h  board=JcJd2h3c  street=turn
  fb=0  vcb=1  n_opp=2  is_made=0  outs=0
  equity_vs_range=0.068  hrp=0.143  board_adjusted_hrp=0.010
```

Note on turn card selection: initial Decision-h guidance suggested
"low non-spade" for A4d (2c/3d/4h). Probed — any low card opens a
wheel gutshot for A4 (needs a 3), so `draw_outs=4` would fail the
predicate. High non-spade works cleanly. Chose Kc (draw_outs=0,
eq=0.036, no board pair, no flush, no hero connection). T5h uses
3c per the original guidance (offsuit, no draws).

## Distribution

### 3-way (40 rows)
- Streets: turn-only 40 (flop can't satisfy vcb=1 per bridge)
- Hero positions: BTN 20, CO 10, BB 6, SB 4
- Unique boards used: 7 (from pool of 24)
- Flop textures: monotone 31, paired 9
- `equity_vs_range`: min=0.002, median=0.031, max=0.090
- `villain_air_pct`: min=0.00, median=0.29, max=0.58

### HU (30 rows) — v2.4 prep, unlabelled
- Streets: turn-only 30
- Hero positions: BTN 15, BB 6, HJ 4, CO 3, SB 2
- Unique boards used: 4
- Flop textures: monotone 30 (HU predicate self-selects here)
- `equity_vs_range`: min=0.066, median=0.088, max=0.153
- `villain_air_pct`: min=0.00, median=0.37, max=0.46

### Texture concentration — flagging for awareness

The predicate (`equity_vs_range<0.35 AND draw_outs<=2 AND is_made=0`)
self-selects to wet textures. On dry/two-tone boards, air hands
tend to retain >35% equity vs checked-through villain ranges
(high-card blocking + many times-it-goes-to-showdown). Dry-board
air isn't the class we're teaching — it's closer to "weak made
with showdown value" and should CHECK for a different reason.

The two playtest litmuses (A4d/Qs5s7s monotone and T5h/JJ2 paired)
ARE monotone+paired. This is the class the model over-bets. So
the concentration aligns with target signal, but worth noting if
you expected dry-board coverage.

## What's in the training-data files

Both JSONLs use the normalised schema (street/hero_position as ints
per ANOMALY-A guard). `bucket` field distinguishes `LITMUS` vs
`AIR_CHECK_3WAY` vs `AIR_CHECK_HU`. All fields match the existing
`v23_*.jsonl` convention.

## Generator design notes

- `_pick_air_hole_cards` iterates mid-rank-outward (T,9,8,J,7,Q,
  6,K,5,A,4,3,2) and filters hands via cheap `hand_evaluator`
  check (AIR_CATS + flush-suit + draw_outs<=2). This single-pass
  filter removed all the "ace-high has too much equity" and
  "low-connector has a straight draw" classes from the initial
  generator output (8/31 → 40/40 pass rate).
- Multi-pass board iteration (3 passes, rotating archetype order)
  to diversify board coverage within `max_per_archetype` bounds.
- Hard-fail litmus check runs BEFORE the main build loop — if
  seeds can't satisfy predicate, we stop and report rather than
  silently writing a broken training set.

## What's next

Per Decision-h proceed checklist:

**Done:**
- Generator built with all 3 review adjustments + 2 blocker fixes
- 10-spec yield probe identified 3 classes of bugs, all fixed
- Full run: 100% predicate conformance, both litmuses pass,
  schema preflight clean
- Output committed

**Next (awaiting reviewer go-ahead):**
- Labelling dispatch via `labelling_agent.py prepare` with v3.1
  prompt on `v23_air_check_3way.jsonl` (40 rows)
- HU set (`v23_air_check_hu.jsonl`, 30 rows) held for v2.4

**After labels land:**
- Re-extract all training data with 110-feature vector (Layer 1
  `board_adjusted_hrp` + existing features)
- Assemble: v2.2 base + Section 1 + CALL supplement + air-CHECK
  3-way + (existing labelled sources)
- Retrain → `v2_3_1_model.json`
- Evaluate: standard gates + BOTH litmus tests (A4d/Qs5s7s and
  T5/JJ2 FLOP decisions must predict CHECK at inference, per
  Decision-h closing note)

Standing by.
