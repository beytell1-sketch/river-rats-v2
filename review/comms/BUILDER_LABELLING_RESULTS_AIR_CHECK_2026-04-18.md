---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 Layer 2 — air-CHECK labelling results (post-labelling checkpoint)
status: READY FOR REVIEW — awaiting retrain go-ahead
---

# Labelling Results — Air-CHECK Counter-Examples

Per MAIN_TERMINAL_DECISION_2026-04-18-h and the REVIEW_YIELD_STATS
(c0276c9) post-labelling checkpoint. 40 hands dispatched to v3.1
labelling panels. All 40 returned clean.

## Dispatch configuration

- Prompt: `prompts/gto_labeller_v3.1.md` (override clause removed,
  per 4a2d28c)
- Input: `training-data/v23_air_check_3way_for_labelling.jsonl`
  (pre-processed from `v23_air_check_3way.jsonl` with decoded
  street/position and aliased board/action_history fields — the
  normalised integer schema doesn't render readably for
  panel agents)
- Batches: 4 × 10 hands, parallel dispatch
- Workspace: `review/label_batches_air_check/`
- Output: `training-data/v23_air_check_3way_labelled.jsonl`

## Results (reviewer's 3 checkpoint items)

### 1. Label distribution

```
CHECK:  40 / 40   (100%)
BET:     0 / 40
CALL:    0 / 40
RAISE:   0 / 40
FOLD:    0 / 40
```

Reviewer's flag threshold (`>5 BET labels → surface as red flag`)
**not tripped.** Zero BET labels.

Confidence distribution:
```
HIGH:   40 / 40
MEDIUM:  0 / 40
LOW:     0 / 40
```

Difficulty distribution:
```
1 (Clear):     36
2 (Standard):   4
3 (Boundary):   0
```

### 2. Panel vote splits

Single-panel run (one agent per batch, 4 agents total covering 40
hands). No vote splits to report by design. Given the unanimous
CHECK / HIGH confidence across the entire set, a second panel
pass is unlikely to surface different actions — but happy to run
one if reviewer wants the cross-check on the 4 difficulty-2
hands.

The 4 difficulty-2 hands are:
- `AIR_CHECK_3WAY_003` (monotone spade flop, hero holds no spade;
  highest villain_air_pct in set at 0.46)
- `AIR_CHECK_3WAY_022` (JcJd2h3c paired board, hero air, villain
  mix)
- `AIR_CHECK_3WAY_024` (JcJd2h3c paired, villain_air_pct=0.58)
- `AIR_CHECK_3WAY_028` (9h9c4d2h paired)

All 4 difficulty-2 hands had BET explicitly evaluated via fold-
equity math in `alternatives_considered` and rejected on KB
Section 1.1 (3-way pure bluffs unprofitable) plus DO NOT Rule 2
(no nut draw + blocker for semi-bluff carve-out).

### 3. Both litmus seeds labelled CHECK on poker merits

```
LITMUS_A4d_Qs5s7s_turn:  action=CHECK  conf=HIGH  difficulty=1
  reasoning: "This is an air hand — Ad4d on Qs5s7sKc has no pair,
  no flush draw (hero holds no spade on a three-spade board), and
  no straight draw; only a lone ace overcard. With 4.3% equity,
  75..."

LITMUS_T5h_JJ2_turn:     action=CHECK  conf=HIGH  difficulty=1
  reasoning: "This is an air hand — Th5h on JcJd2h3c has no pair
  and no live flush draw (three total hearts on a dead turn is
  backdoor-only, already dead at this point since only one card
  remain..."
```

Both labelled CHECK with HIGH confidence and difficulty 1 — i.e.,
the panels considered these clear calls, not boundary decisions.
No override clause was needed; v3.1's bucket-first protocol
reaches CHECK from first principles.

## Vocabulary gap flagged by panel (for awareness)

Batch-01 panel noted that the approved `street_plan` action-tag
vocabulary (`barrel_value`, `bet_protect_evaluate`, `check_trap`,
`check_pot_control`, `draw_continue`) has no clean fit for
"check air with intent to give up and realize equity cheaply on
the river." The agent used `check_pot_control` as the closest fit
and recorded `proposed_tags: [{name: "check_give_up"}]` on those
hands.

Not a blocker — the labels themselves are clean. Flagging for
vocab-registry reviewer to consider for v3.2 / future prompt
iteration. All existing fields in the output JSONL use approved
vocabulary.

## Integrity checks on output JSONL

Verified on `training-data/v23_air_check_3way_labelled.jsonl`:
- All 40 situations present (no collector dropouts)
- Every row has `expert_action`, `expert_confidence`,
  `expert_reasoning`, `difficulty` populated
- Every row preserves original 37-feature-plus-metadata schema
  from the input JSONL
- Both litmus seeds are in the output with CHECK action

No parse errors. Schema ready for downstream assembly.

## What's next

Per Decision-h checklist §9-10 (post-labelling):

**Ready to proceed on reviewer go-ahead:**
1. Re-extract all training data with the 110-feature vector
   (incorporates Layer 1's `board_adjusted_hrp`)
2. Assemble training CSV: v2.2 base + Section 1 + CALL supplement
   + **air-CHECK 3-way (40 labelled rows)**
3. Retrain → `v2_3_1_model.json`
4. Evaluate against standard gates + BOTH flop litmus tests:
   - A4d/Qs5s7s flop decision must predict CHECK at inference
   - T5h/JJ2 flop decision must predict CHECK at inference

(Layer 1 + Layer 2 together should carry both litmuses; Layer 1's
board_adjusted_hrp for the flop spots directly, Layer 2 for the
general air+vcb=1 pattern.)

## HU set status

`training-data/v23_air_check_hu.jsonl` (30 rows, unlabelled)
remains in place for v2.4 pickup. Not included in v2.3.1 retrain
per Decision-h Path B.

## Commits this cycle

- `training-data/v23_air_check_3way_labelled.jsonl` — 40 labelled
  rows ready for assembly
- `training-data/v23_air_check_3way_for_labelling.jsonl` — readable
  pre-labelling copy with decoded string fields
- `review/label_batches_air_check/` — panel workspace (context,
  batches, raw result files)
- `river-rats-core/labelling_agent.py` — additive changes:
  `--prompt` and `--batch-dir` CLI args, extended
  `_FLAT_METADATA_KEYS` to include `board` and `action_history`

Standing by for reviewer approval on retrain.
