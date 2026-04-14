# Pass 2 Review Report — 2026-04-14

## Summary

- **68 hands reviewed** across 5 tiers by 13 reviewer agents
- **Pass 1 labels stand**: 58/68 (85.3%)
- **Pass 1 labels overridden**: 10/68 (14.7%)
- **CHECK→BET transitions**: 8/9 validated (bucket-first method confirmed), 1/9 flagged for over-aggression

## Per-tier breakdown

| Tier | Category | Hands | Stands | Overridden |
|---|---|---|---|---|
| 1 | CONFIDENT_SPLIT | 1 | 1 | 0 |
| 2 | MAJORITY split | 13 | 5 | 8 |
| 3 | HARD/CONTESTED | 20 | 19 | 1 |
| 4 | STRONG 3/4 | 25 | 25 | 0 |
| 5 | CHECK→BET challenger | 9 | 8 | 1 |

## Pass 2 overrides (Pass 1 labels flipped)

| Situation | Tier | Pass 1 (T1-T4) | Pass 2 Consensus | Reviewer votes |
|---|---|---|---|---|
| BP4_21 | 2 | BET (BET/CHECK/CHECK/BET) | **CHECK** | CHECK/CHECK/CHECK |
| BP7_01 | 2 | RAISE (RAISE/CALL/CALL/RAISE) | **CALL** | CALL/RAISE/CALL |
| d5222_BTN_flop | 2 | CALL (CALL/CALL/FOLD/FOLD) | **FOLD** | FOLD/FOLD/CALL |
| d5620_CO_turn | 2 | CALL (CALL/FOLD/CALL/FOLD) | **FOLD** | FOLD/FOLD/FOLD |
| d5749_HJ_turn | 2 | CALL (CALL/FOLD/FOLD/CALL) | **FOLD** | FOLD/FOLD/FOLD |
| d8002_BTN_flop | 2 | FOLD (FOLD/CALL/CALL/FOLD) | **CALL** | FOLD/CALL/CALL |
| d8886_BTN_flop | 2 | BET (BET/CHECK/CHECK/BET) | **CHECK** | CHECK/BET/CHECK |
| d8963_HJ_turn | 2 | BET (BET/CHECK/BET/CHECK) | **CHECK** | CHECK/CHECK/CHECK |
| BP1_08 | 3 | RAISE (RAISE/CALL/RAISE/RAISE) | **CALL** | CALL/CALL/CALL |
| d1983_BTN_turn | 5 | BET (BET/BET/BET/BET) | **CHECK** | CHECK |

## Tier 5 CHECK→BET challenge (the key validation)

The bucket-first method's biggest behavioural shift from the old sequential tree was converting CHECK labels to BET for value/protection spots. Pass 2 challenger validated **8/9** — the method is confirmed. One over-aggression flagged:

- **d1983_BTN_turn** (Ad4d on Jd7dKh2c): nut flush draw, 28.8% equity, 19.6% improvement, SPR 1.25. All 4 new teams applied KB 1.7 semi-bluff despite poor equity-when-called. Challenger: CHECK preserves free river realization. **Flagged for solver.**

Challenger proposed a KB guard: at SPR<2, semi-bluff requires improvement_probability>30% OR equity_vs_range>35%. Consider adding to the prompt before v2.3.

## Solver verification list

| Category | Count | Priority |
|---|---|---|
| Mandatory (Tier 1+2) | 14 | HIGH — action splits |
| Tier 5 over-aggression | 1 | HIGH — method validation |
| Tier 3 panel-majority flagged | 10 | MEDIUM |
| Tier 4 expert-flagged | 25 | LOW (spot-check) |
| **Total** | **50** | |

## Key judgement themes from reviewers

- **MW-30 vs MW-50 boundary**: multiple Tier 3 river TPTK/two-pair spots facing bet+raise (d0244, d5066, d7760, d8427) hit the equity-surplus vs facing_raise=near-nuts boundary. Reviewers consistently chose CALL when equity_margin >+15pp.
- **Tier 2 MW-50 FOLD corrections**: 3 Pass 1 CALLs flipped to FOLD (d5222, d5620, d5749) — bet+raise or raise-into-two on paired/straight-heavy boards = near-nuts signal per KB DO-NOT #3.
- **BP1_08 RAISE→CALL (Tier 3)**: All 3 panelists agreed KB 1.7 RAISE threshold not met (FE 36% below 40%, weak 6% blocker, SPR 1.11 commits badly). Clean Pass 1 correction.
- **Bucket misclassification** caught on BP5_01 (Tier 1): T4 mis-read bottom two pair as a set. Panel corrected to BET (2/3).
- **25/25 Tier 4 STRONG**: all majorities validated; 4 dissenters flagged as genuinely close (line defensible but majority better).

## Artefacts

- Per-hand reviewer summary: `training-data/pass2_summary.jsonl`
- Solver verification list: `training-data/pass2_solver_list.json`
- Raw reviewer outputs: `/tmp/pass2_results/*.json` (13 files)

## Updated Pass 1 labels (after Pass 2 overrides)

Apply these 10 changes to the production label set before training:

| situation_id | new_label |
|---|---|
| BP1_08 | CALL |
| BP4_21 | CHECK |
| BP7_01 | CALL |
| d1983_BTN_turn | CHECK |
| d5222_BTN_flop | FOLD |
| d5620_CO_turn | FOLD |
| d5749_HJ_turn | FOLD |
| d8002_BTN_flop | CALL |
| d8886_BTN_flop | CHECK |
| d8963_HJ_turn | CHECK |

## Next steps

1. **Pass 2 gate**: owner review this report
2. Solver verification on 15 high-priority hands (user runs GTO Wizard; pre-flight sizes per KB)
3. Apply any solver-driven label corrections
4. Vocabulary review (merge proposed_tags synonyms)
5. Apply attn_* binary flags via T1-T6 union → 108 training columns
6. Train v2.2 model
