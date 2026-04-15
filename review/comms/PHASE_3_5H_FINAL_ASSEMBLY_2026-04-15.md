---
date: 2026-04-15
from: Builder
to: Owner
re: Phase 3.5H — Final assembly complete, ready for Gate 6
status: AWAITING APPROVAL
---

# v2.2 Final Assembly — Gate 6 Submission

## TL;DR

- **385 hands**, 22 net label changes vs original Pass 1
- 108-column training CSV ready at `training-data/v2_2_training.csv`
- T1-T6 union feature_attention applied (avg 22.4 features tagged per hand)
- Vocabulary review complete: 6 intention tags, 10 street_plan tags, 2 proposed-new tags
- 13 hands solver-verified — see `training-data/solver_verification_log.jsonl`

## Final action distribution (385 hands)

| Action | Original Pass 1 | Final | Δ |
|---|---|---|---|
| BET | 105 | 99 | -6 |
| CHECK | 125 | 131 | +6 |
| CALL | 59 | 57 | -2 |
| RAISE | 25 | 23 | -2 |
| FOLD | 71 | 75 | +4 |

## 22 label changes

| ID | Old | New | Source |
|---|---|---|---|
| `BP1_03` | CALL | **RAISE** | Pass1+relabel consensus |
| `BP2_28` | CALL | **FOLD** | Pass1+relabel consensus |
| `BP4_11` | BET | **CHECK** | Pass1+relabel consensus |
| `BP4_19` | CHECK | **BET** | Pass1+relabel consensus |
| `BP4_20` | CHECK | **BET** | Pass1+relabel consensus |
| `BP4_21` | BET | **CHECK** | Pass 2 — solver said BET 25%, but owner keeps CHECK in mixed zone |
| `BP4_22` | BET | **CHECK** | Pass1+relabel consensus |
| `BP4_24` | BET | **CHECK** | Pass1+relabel consensus |
| `BP4_30` | BET | **CHECK** | Pass1+relabel consensus |
| `BP5_01` | BET | **CHECK** | Pass 2 + SOLVER override (was Pass 2 BET, solver said CHECK) |
| `BP5_10` | CHECK | **BET** | Pass1+relabel consensus |
| `BP5_12` | BET | **CHECK** | Pass1+relabel consensus |
| `BP5_17` | CHECK | **BET** | Pass1+relabel consensus |
| `BP6_04` | RAISE | **CALL** | Pass1+relabel consensus |
| `BP7_01` | RAISE | **CALL** | Pass 2 — no solver, Pass 2 CALL stands |
| `BP7_11` | RAISE | **CALL** | Pass1+relabel consensus |
| `d4312_CO_turn` | BET | **CHECK** | Pass 2 + SOLVER override (was Pass 2 BET, solver said CHECK) |
| `d5222_BTN_flop` | CALL | **FOLD** | Pass 2 — solver confirms FOLD (close) |
| `d5620_CO_turn` | CALL | **FOLD** | Pass 2 — solver confirms FOLD |
| `d5749_HJ_turn` | CALL | **FOLD** | Pass 2 — solver confirms FOLD |
| `d8886_BTN_flop` | BET | **CHECK** | Pass 2 — solver mixed (BET combo) but owner keeps CHECK |
| `d8963_HJ_turn` | BET | **CHECK** | Pass 2 — solver mixed (BET combo) but owner keeps CHECK |

## Solver verification — 13 hands

- 5 confirms / 8 overrides (62%, but most are mixed-strategy zone — see v2.3 backlog item 7)
- 2 clean reverts to Pass 1 (d1983 BET, BP1_08 RAISE)
- See `training-data/solver_verification_log.jsonl` for full per-hand record

## Training CSV

- File: `training-data/v2_2_training.csv`
- 385 rows × 111 columns:
  - 1 situation_id
  - 54 raw feature values
  - 54 attn_* binary flags (T1-T6 union + Pass 2 additions)
  - label, label_source
- Avg attn coverage per hand: 22.4 / 54 (41%)
- 8 reserved features always tagged (equity_vs_range, villain composition quad, is_ip, hero_range_percentile, pot_odds)

## Vocabulary review

**Intentions (6 unique):**
- value_extract (761 uses), pot_control (587), range_fold_priced_out (524), deny_equity (457), continue_draw (409), bluff_fold_better (20)
- Clean, no synonyms, all retained.

**Street plan tags (10 unique):** retained as-is

**Proposed new tags (2):** `give_up_no_equity` (2 uses), `give_up` (1 use). **Recommendation: merge both into existing `pot_control`** (semantic overlap, low frequency). No vocabulary expansion needed for v2.2.

## Phase 3.5 summary (BP relabel + Pass 2 + solver)

| Phase | Outcome |
|---|---|
| 3.5A villain inference | 148 HIGH-conf + 28 LOW-conf, 9 already clean |
| 3.5B regenerate situations | 185 BP situations rewritten with complete villain lists |
| 3.5C BP Pass 1 relabel | 76 agents, 15 BP hands flipped (8.1%) |
| 3.5D BP T5-T6 discovery | SKIPPED per owner — discovery union stable |
| 3.5E damage measurement | 0 solver-mandatory escalations from BP transitions |
| 3.5F BP Pass 2 | 4 reviewers, 12 BP overrides (3 reverted to Pass 1) |
| 3.5G d-series + BP solver | 13 hands verified, 8 overrides, 2 reverts to Pass 1 |
| 3.5H final assembly | **22 net label changes**, 108-column CSV ready |

## Gate 6 ask

Approve the v2.2 label set + 108-column training CSV for Phase 4 (model training).

**Artefacts:**
- `training-data/v2_2_training.csv` — production training input
- `training-data/pass1_final_labels.jsonl` — full label record with sources
- `training-data/v2_2_vocab_audit.json` — vocabulary breakdown
- `training-data/solver_verification_log.jsonl` — solver decision record
- `training-data/bp_relabel_comparison.jsonl` — BP relabel deltas

## Known issues logged for v2.3

- Item 5 (BLOCKER): villain seat data integrity — add validator to factory
- Item 6 (struck): SPR<2 semi-bluff guard — invalidated, do not apply
- Item 7: bucket-first CHECK bias in solver-mixed spots — calibration check needed
- Item 8: Pass 2 override discipline — solver-confirmation required for overriding Pass 1 unanimous
