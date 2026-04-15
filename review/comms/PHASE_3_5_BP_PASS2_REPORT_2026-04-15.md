---
date: 2026-04-15
from: Builder
to: Owner
re: BP Pass 2 review — final BP label decisions
---

# BP Phase 3.5 Pass 2 — Final Decisions

## Summary

- 4 reviewers (1 STRONG expert + 3 MAJORITY panelists) covered 11 of the 15 BP-relabel flips
- 4 UNANIMOUS-relabel flips (BP4_20/22/24, BP5_12) needed no review
- **9 of 11 reviewed flips confirmed by Pass 2**; 3 reverted to original labels (relabel was wrong)
- **Final: 12 BP overrides apply** (vs. 15 from relabel)

## STRONG-tier outcomes (1 expert, 6 hands)

| ID | Old | Relabel | Expert | Decision |
|---|---|---|---|---|
| BP1_03 | CALL | RAISE | CALL | **revert to CALL** ⚠ solver-flag |
| BP1_08 | RAISE | CALL | CALL | confirm CALL |
| BP4_11 | BET | CHECK | CHECK | confirm CHECK |
| BP5_10 | CHECK | BET | BET | confirm BET |
| BP6_04 | RAISE | CALL | CALL | confirm CALL |
| BP7_01 | RAISE | CALL | CALL | confirm CALL |

## MAJORITY-tier outcomes (3 panelists, 5 hands)

| ID | Old | Relabel | Panel votes | Final |
|---|---|---|---|---|
| BP2_28 | CALL | FOLD | FOLD/CALL/FOLD | **FOLD** (confirm relabel) |
| BP4_19 | CHECK | BET | BET/BET/BET | **BET** (confirm relabel — unanimous panel) |
| BP4_30 | BET | CHECK | CHECK/CHECK/BET | **CHECK** (confirm relabel) |
| BP5_17 | CHECK | BET | CHECK/BET/CHECK | **revert to CHECK** (panel agrees CHECK) |
| BP7_11 | RAISE | CALL | RAISE/RAISE/RAISE | **revert to RAISE** (unanimous panel — MW-33 pattern) |

## UNANIMOUS-relabel flips (no Pass 2, applied as-is)

| ID | Old | New |
|---|---|---|
| BP4_20 | CHECK | BET |
| BP4_22 | BET | CHECK |
| BP4_24 | BET | CHECK |
| BP5_12 | BET | CHECK |

## Final BP override list (12 hands)

| ID | Old → New |
|---|---|
| BP1_08 | RAISE → CALL |
| BP4_11 | BET → CHECK |
| BP5_10 | CHECK → BET |
| BP6_04 | RAISE → CALL |
| BP7_01 | RAISE → CALL |
| BP2_28 | CALL → FOLD |
| BP4_19 | CHECK → BET |
| BP4_30 | BET → CHECK |
| BP4_20 | CHECK → BET |
| BP4_22 | BET → CHECK |
| BP4_24 | BET → CHECK |
| BP5_12 | BET → CHECK |

## Pass 2-reverted hands (3) — Pass 2 said relabel was wrong, original label stands

| ID | Original | Relabel proposed | Pass 2 verdict |
|---|---|---|---|
| BP1_03 | CALL | RAISE | CALL — FE 21% below KB 1.7 raise bar; T1's call was correct (solver-flag added) |
| BP5_17 | CHECK | BET | CHECK — bottom of BTN range on connected board, panel agrees no c-bet |
| BP7_11 | RAISE | CALL | RAISE — top two at SPR 0.56 is MW-33 commit pattern; panel unanimous |

## New solver flags from Pass 2 (6 hands)

- BP1_03 — STRONG expert flagged; close FE call vs raise spot
- BP2_28, BP4_19, BP4_30, BP5_17, BP7_11 — all MAJORITY panel hands tagged solver_recommended

These add to the d-series HIGH solver list. Owner can include in current GTO Wizard session or defer.

## Inline feature-attention additions

Reviewers flagged these as load-bearing in the corrected-villain context but missing from discovery union:

- `spr` (BP2_28, BP7_11) — commit geometry decisive
- `is_preflop_aggressor` (BP4_19, BP4_30, BP5_17) — gates c-bet logic
- `board_favour`, `connectivity_score` (BP4_30, BP5_17) — connected-middling boards favour BB not PFA
- `flush_danger`, `is_strong_made` (BP7_11) — protection urgency on live FD board
- `flush_draw_rank`, `flush_block_pct` (BP1_03) — KB 1.7 raise inputs
- `equity_margin`, `num_callers_to_bet` (BP2_28) — sandwich-defender math
- `high_card_rank` (BP4_19, BP5_17) — board-strength signal

These will be added to the union when building the 54 attn_* binary columns for training.

## Grand total label changes for final assembly

- d-series Pass 2 overrides (previously approved): **10**
- BP relabel + Pass 2 overrides: **12**
- **Total: 22 label changes** (+ pending solver-driven corrections from owner's d-series HIGH session)

## Next: Phase 3.5H Final Assembly

1. Apply 22 label overrides to production set (`pass1_final_labels.jsonl` already has 10 d-series; add 12 BP)
2. Apply any solver-driven corrections from owner's verification session
3. Build T1-T6 union feature_attention with the 7 new feature additions above
4. Generate 108-column training CSV (54 features + 54 attn_* binary flags)
5. Vocabulary review
6. Present for Gate 6
