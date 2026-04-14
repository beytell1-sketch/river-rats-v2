# Pass 1 Comparison Report — 2026-04-14

## Summary

- **Total hands**: 385 (200 reconstructed + 185 factory)
- **Labelling teams**: T1, T2, T3, T4 (Approach C amended, Exp 3 auxiliary flags)
- **Agent-calls**: 156 (39 batches × 4 teams)

## Action consensus (385 hands)

| Category | Count | % |
|---|---|---|
| UNANIMOUS | 332 | 86.2% |
| STRONG | 40 | 10.4% |
| MAJORITY | 13 | 3.4% |
| SPLIT | 0 | 0.0% |

## Difficulty consensus (385 hands)

| Category | Count | % |
|---|---|---|
| CLEAR | 143 | 37.1% |
| LIKELY_CLEAR | 57 | 14.8% |
| STANDARD | 161 | 41.8% |
| HARD | 20 | 5.2% |
| CONTESTED | 4 | 1.0% |

## Bucket agreement

| Category | Count | % |
|---|---|---|
| all4_same | 309 | 80.3% |
| 3-1 | 52 | 13.5% |
| 2-2 | 22 | 5.7% |
| split | 2 | 0.5% |

## Tag-agreement metrics

- Average intention Jaccard (pairwise across 4 teams): **0.850**
- Average feature-attention Jaccard: **0.846**

## CONFIDENT_SPLIT hands (D1 majority but action not unanimous): 1

| situation_id | T1 | T2 | T3 | T4 | consensus |
|---|---|---|---|---|---|
| BP5_01 | BET | BET | BET | CHECK | STRONG |

## MAJORITY-split hands (close spots, 13 hands)

These hands have a 2-2 or 2-1-1 action split — candidates for Pass 2 full panel + solver.

| situation_id | T1 | T2 | T3 | T4 | difficulty_consensus |
|---|---|---|---|---|---|
| BP4_19 | CHECK | BET | BET | CHECK | STANDARD |
| BP4_21 | BET | CHECK | CHECK | BET | HARD |
| BP5_12 | BET | BET | CHECK | CHECK | STANDARD |
| BP7_01 | RAISE | CALL | CALL | RAISE | HARD |
| d2788_UTG_flop | BET | BET | CHECK | CHECK | STANDARD |
| d4312_CO_turn | BET | CHECK | BET | CHECK | STANDARD |
| d5222_BTN_flop | CALL | CALL | FOLD | FOLD | STANDARD |
| d5620_CO_turn | CALL | FOLD | CALL | FOLD | HARD |
| d5749_HJ_turn | CALL | FOLD | FOLD | CALL | HARD |
| d8002_BTN_flop | FOLD | CALL | CALL | FOLD | STANDARD |
| d8886_BTN_flop | BET | CHECK | CHECK | BET | STANDARD |
| d8963_HJ_turn | BET | CHECK | BET | CHECK | STANDARD |
| d9556_BB_flop | CHECK | CHECK | BET | BET | STANDARD |

## STRONG (3/4) hands: 40

These need 1 expert reviewer per the Phase 3 Final Plan. Dissenting team flagged for reasoning review.

<details><summary>Expand full list (40)</summary>

| situation_id | T1 | T2 | T3 | T4 | majority | difficulty |
|---|---|---|---|---|---|---|
| BP1_01 | RAISE | RAISE | CALL | RAISE | RAISE | STANDARD |
| BP1_05 | RAISE | RAISE | RAISE | CALL | RAISE | HARD |
| BP1_07 | RAISE | CALL | RAISE | RAISE | RAISE | STANDARD |
| BP1_08 | RAISE | CALL | RAISE | RAISE | RAISE | HARD |
| BP1_19 | RAISE | RAISE | CALL | RAISE | RAISE | STANDARD |
| BP1_25 | FOLD | CALL | FOLD | FOLD | FOLD | STANDARD |
| BP2_16 | FOLD | CALL | CALL | CALL | CALL | STANDARD |
| BP2_18 | CALL | FOLD | CALL | CALL | CALL | HARD |
| BP2_31 | CALL | RAISE | RAISE | RAISE | RAISE | STANDARD |
| BP2_33 | CALL | RAISE | CALL | CALL | CALL | STANDARD |
| BP3_02 | FOLD | CALL | FOLD | FOLD | FOLD | CONTESTED |
| BP4_12 | BET | CHECK | BET | BET | BET | STANDARD |
| BP4_20 | BET | CHECK | CHECK | CHECK | CHECK | HARD |
| BP4_24 | BET | BET | CHECK | BET | BET | STANDARD |
| BP4_35 | CHECK | CHECK | BET | CHECK | CHECK | HARD |
| BP5_01 | BET | BET | BET | CHECK | BET | LIKELY_CLEAR |
| BP5_10 | CHECK | CHECK | BET | CHECK | CHECK | HARD |
| BP6_04 | CALL | RAISE | RAISE | RAISE | RAISE | HARD |
| BP7_12 | FOLD | FOLD | CALL | FOLD | FOLD | STANDARD |
| d0244_CO_river | CALL | FOLD | CALL | CALL | CALL | HARD |
| d1764_BTN_flop | BET | CHECK | CHECK | CHECK | CHECK | STANDARD |
| d1971_HJ_river | BET | CHECK | BET | BET | BET | STANDARD |
| d2511_CO_river | CALL | CALL | CALL | RAISE | CALL | HARD |
| d3409_HJ_river | FOLD | CALL | CALL | CALL | CALL | STANDARD |
| d3687_HJ_turn | CHECK | CHECK | CHECK | BET | CHECK | STANDARD |
| d4211_HJ_turn | FOLD | CALL | CALL | CALL | CALL | STANDARD |
| d4472_BTN_turn | BET | CHECK | CHECK | CHECK | CHECK | CONTESTED |
| d5066_BTN_river | CALL | CALL | FOLD | CALL | CALL | HARD |
| d6508_BB_flop | CHECK | CHECK | BET | CHECK | CHECK | STANDARD |
| d6709_BTN_flop | CHECK | CHECK | BET | CHECK | CHECK | STANDARD |
| d6826_BTN_turn | FOLD | FOLD | CALL | FOLD | FOLD | STANDARD |
| d6869_CO_turn | CHECK | CHECK | CHECK | BET | CHECK | STANDARD |
| d7296_BB_flop | CHECK | CHECK | BET | CHECK | CHECK | STANDARD |
| d7760_BTN_flop | CHECK | BET | CHECK | CHECK | CHECK | STANDARD |
| d7760_BTN_river | FOLD | CALL | CALL | CALL | CALL | HARD |
| d8427_CO_river | CALL | CALL | FOLD | CALL | CALL | HARD |
| d8453_BTN_turn | BET | CHECK | BET | BET | BET | STANDARD |
| d9208_BB_turn | BET | CHECK | BET | BET | BET | STANDARD |
| d9556_BB_turn | BET | BET | CHECK | BET | BET | STANDARD |
| d9989_BB_flop | CHECK | BET | CHECK | CHECK | CHECK | STANDARD |

</details>

## 200 Reconstructed hands — old vs new consensus

- Agree: **83/200 (41.5%)**
- Disagree: **117/200 (58.5%)**

### Transition breakdown (old -> new consensus)

| Transition | Count | Interpretation |
|---|---|---|
| FOLD->CHECK | 39 | Old heuristic mis-labelled check-nodes as fold (no bet to face) — corrected |
| RAISE->BET | 35 | Old used RAISE for unraised-pot aggression — new uses BET (convention change) |
| CHECK->BET | 31 | New teams see value/protection where old gave up — review for over-aggression |
| FOLD->CALL | 10 | New teams defend lighter — review for over-calling |
| CALL->FOLD | 1 | New teams fold tighter — check equity_vs_range |
| RAISE->CHECK | 1 | Old raised where new checks — unusual |

### Key finding

- **Convention/labelling shifts**: 74/200 (37.0%) — FOLD->CHECK and RAISE->BET reclassifications, not GTO disagreements.
- **Genuine GTO-direction shifts**: 43/200 (21.5%).
- **CALL<->RAISE swaps requiring solver**: 0
- **CALL->FOLD with equity_vs_range > 0.30 (solver mandatory)**: 0
- Once convention shifts are excluded, genuine disagreement is **21.5%** — within the Phase 3 Final Plan acceptable band.

## Pass 2 candidate triage (per Phase 3 Final Plan)

| Category | Count | Treatment |
|---|---|---|
| UNANIMOUS + CLEAR | 143 | Done — no Pass 2 |
| UNANIMOUS + LIKELY_CLEAR | 56 | Done — no Pass 2 |
| UNANIMOUS + STANDARD | 127 | 1 challenger |
| STRONG (3/4) | 40 | 1 expert reviewer |
| MAJORITY (split) | 13 | Full panel + solver |
| HARD or CONTESTED difficulty | 24 | Full panel regardless of action |
| CONFIDENT_SPLIT | 1 | Panel + solver mandatory |

## Artefacts

- Per-team JSONL: `training-data/pass1_T{1-4}_labels.jsonl` (385 records each)
- Machine-readable per-hand comparison: `training-data/pass1_comparison.jsonl`
- Reconstructed old-vs-new comparison: `training-data/pass1_recon_comparison.jsonl`

## Next steps

1. **Pass 1 gate** — owner review of this report
2. After approval: T5-T6 discovery teams (78 agents) to find features T1-T4 missed
3. Pass 2 targeted review per category breakdown above
4. Solver verification on escalated hands
