# Corpus Label Distribution Audit — 4-way 700 corpus (350 consensus target, 337 actual)

Generated: 2026-05-13. Source: batch_00{1..7}_consensus.jsonl + context + raw labels.
Total consensus rows across 7 batches: **337**.

**Schema note:** batch_001_consensus.jsonl uses key `consensus_state`; batches 002-007 use `state`. Unified to `state` in loader.
**Sizing note:** consensus file has no `consensus_sizing_pct`; sizing analysis is over the 5×labeller `predicted_sizing_pct` raw labels (with action=RAISE/BET).

---

## 1. Action distribution — overall and per batch

**Overall:**

| Action | Count | % |
|---|---:|---:|
| BET | 113 | 33.5% |
| CALL | 69 | 20.5% |
| CHECK | 66 | 19.6% |
| RAISE | 58 | 17.2% |
| FOLD | 31 | 9.2% **<10% FLAG** |

**Per-batch action breakdown (counts):**

| Batch | BET | CALL | CHECK | FOLD | RAISE | Total |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 24 | 6 | 9 | 4 | 3 | 46 |
| 2 | 24 | 3 | 14 | 5 | 3 | 49 |
| 3 | 29 | 2 | 12 | 3 | 3 | 49 |
| 4 | 19 | 4 | 13 | 0 | 13 | 49 |
| 5 | 7 | 21 | 5 | 3 | 12 | 48 |
| 6 | 3 | 19 | 8 | 8 | 11 | 49 |
| 7 | 7 | 14 | 5 | 8 | 13 | 47 |

## 2. Action-context distribution

| Context | Count | % |
|---|---:|---:|
| opener | 179 | 53.1% |
| facing_bet | 158 | 46.9% |

**Action × context cross-tab:**

| Context | BET | CALL | CHECK | FOLD | RAISE |
|---|---:|---:|---:|---:|---:|
| facing_bet | 0 | 69 | 0 | 31 | 58 |
| opener | 113 | 0 | 66 | 0 | 0 |

## 3. Agreement distribution

| Pattern (sorted vote counts) | Interpretation | Count | % |
|---|---|---:|---:|
| 5 | unanimous 5/5 | 277 | 82.2% |
| 4-1 | 4/1 split | 46 | 13.6% |
| 3-2 | 3/2 split | 12 | 3.6% |
| 2-2-1 | 2-2-1 fractured | 1 | 0.3% |
| 3-1-1 | 3-way split | 1 | 0.3% |

**Non-unanimous total: 60/337 = 17.8%**

## 4. Sizing-bucket distribution for RAISE/BET (raw labels)

Total BET/RAISE labels with non-null sizing across all labellers: **844**

| Bucket | Count | % |
|---|---:|---:|
| ~66%-pot | 446 | 52.8% |
| raise-to-9bb? (semantic mismatch) | 119 | 14.1% |
| ~25%-pot | 114 | 13.5% |
| ~33%-pot | 67 | 7.9% |
| ~75%-pot | 62 | 7.3% |
| oversized-300% (likely bb-not-pct) | 21 | 2.5% |
| oversized-360% (likely bb-not-pct) | 7 | 0.8% |
| ~100%-pot | 3 | 0.4% |
| oversized-720% (likely bb-not-pct) | 2 | 0.2% |
| oversized-270% (likely bb-not-pct) | 1 | 0.1% |
| raise-to-10bb? (semantic mismatch) | 1 | 0.1% |
| raise-to-15bb? (semantic mismatch) | 1 | 0.1% |

**Outside solver-aligned pct-of-pot buckets (25/33/66/75/150):** 155/844 = 18.4%

**CRITICAL SCHEMA ISSUE — DUAL SEMANTICS in `predicted_sizing_pct`:**
Many RAISE labels carry values like 9, 18, 22, 27 (consistent with raise-to-bb, NOT pct-of-pot),
and values like 300, 360, 720 (consistent with raise-to-bb expressed as % of original bet, or raise-to-bb absolute).
Example: spot 4WF-MULTIWAY-147 has `to_call_bb=2.5, pot_bb=13.5`; a '9%' sizing is incoherent as %-of-pot
but coherent as raise-to-9bb (3.6× the 2.5bb bet). The 18/22/27 cluster matches typical 3-7× raise-to-bb amounts.
This means the labelling-prompt sizing field has been interpreted inconsistently across labellers and spots.
Action: v3.5 amendment must (a) split into `sizing_pct_of_pot` and `raise_to_bb` fields, OR (b) normalize
downstream during training-data export. Until normalized, the ~155/844 (18.4%) 'non-canonical' rate is
a measurement artifact, NOT a labeller drift signal.

Distribution by action:

**BET** (n=574):

| Bucket | Count | % |
|---|---:|---:|
| ~66%-pot | 443 | 77.2% |
| ~25%-pot | 74 | 12.9% |
| ~33%-pot | 57 | 9.9% |

**RAISE** (n=270):

| Bucket | Count | % |
|---|---:|---:|
| raise-to-9bb? (semantic mismatch) | 119 | 44.1% |
| ~75%-pot | 62 | 23.0% |
| ~25%-pot | 40 | 14.8% |
| oversized-300% (likely bb-not-pct) | 21 | 7.8% |
| ~33%-pot | 10 | 3.7% |
| oversized-360% (likely bb-not-pct) | 7 | 2.6% |
| ~66%-pot | 3 | 1.1% |
| ~100%-pot | 3 | 1.1% |
| oversized-720% (likely bb-not-pct) | 2 | 0.7% |
| oversized-270% (likely bb-not-pct) | 1 | 0.4% |
| raise-to-10bb? (semantic mismatch) | 1 | 0.4% |
| raise-to-15bb? (semantic mismatch) | 1 | 0.4% |

## 5. Hero position distribution

| Position | Count | % |
|---|---:|---:|
| BTN | 90 | 26.7% |
| CO | 74 | 22.0% |
| SB | 43 | 12.8% |
| MP | 39 | 11.6% |
| BB | 32 | 9.5% **<10% FLAG** |
| UTG | 26 | 7.7% **<10% FLAG** |
| HJ | 20 | 5.9% **<10% FLAG** |
| EP | 13 | 3.9% **<10% FLAG** |

**Position × action cross-tab:**

| Position | BET | CALL | CHECK | FOLD | RAISE | Total |
|---|---:|---:|---:|---:|---:|---:|
| BB | 0 | 20 | 0 | 0 | 12 | 32 |
| BTN | 18 | 39 | 7 | 18 | 8 | 90 |
| CO | 36 | 4 | 14 | 2 | 18 | 74 |
| EP | 11 | 0 | 2 | 0 | 0 | 13 |
| HJ | 5 | 0 | 11 | 3 | 1 | 20 |
| MP | 10 | 4 | 13 | 7 | 5 | 39 |
| SB | 21 | 2 | 5 | 1 | 14 | 43 |
| UTG | 12 | 0 | 14 | 0 | 0 | 26 |

## 6. Board texture distribution

| Texture | Count | % of corpus |
|---|---:|---:|
| rainbow_dry | 104 | 30.9% |
| two_tone | 103 | 30.6% |
| preflop_or_no_board | 72 | 21.4% |
| rainbow | 30 | 8.9% |
| paired | 22 | 6.5% |
| monotone | 6 | 1.8% |

**Postflop subset n=265 (excluding 72 preflop spots):**

| Texture | Count | % of postflop |
|---|---:|---:|
| rainbow_dry | 104 | 39.2% |
| two_tone | 103 | 38.9% |
| rainbow | 30 | 11.3% |
| paired | 22 | 8.3% **<10% FLAG** |
| monotone | 6 | 2.3% **<10% FLAG** |

**Board × action:**

| Texture | BET | CALL | CHECK | FOLD | RAISE | Total |
|---|---:|---:|---:|---:|---:|---:|
| monotone | 0 | 1 | 0 | 0 | 5 | 6 |
| paired | 9 | 1 | 7 | 1 | 4 | 22 |
| preflop_or_no_board | 9 | 45 | 0 | 11 | 7 | 72 |
| rainbow | 15 | 4 | 7 | 3 | 1 | 30 |
| rainbow_dry | 31 | 8 | 31 | 8 | 26 | 104 |
| two_tone | 49 | 10 | 21 | 8 | 15 | 103 |

## 7. Per-batch heterogeneity

**Action-mix variation per batch (percentage points from corpus mean):**

| Batch | n | ΔBET | ΔCHECK | ΔFOLD | ΔRAISE | ΔCALL | max|Δ| |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 46 | +18.6 | -0.0 | -0.5 | -10.7 | -7.4 | 18.6 **>10pp FLAG** |
| 2 | 49 | +15.4 | +9.0 | +1.0 | -11.1 | -14.4 | 15.4 **>10pp FLAG** |
| 3 | 49 | +25.7 | +4.9 | -3.1 | -11.1 | -16.4 | 25.7 **>10pp FLAG** |
| 4 | 49 | +5.2 | +6.9 | -9.2 | +9.3 | -12.3 | 12.3 **>10pp FLAG** |
| 5 | 48 | -18.9 | -9.2 | -2.9 | +7.8 | +23.3 | 23.3 **>10pp FLAG** |
| 6 | 49 | -27.4 | -3.3 | +7.1 | +5.2 | +18.3 | 27.4 **>10pp FLAG** |
| 7 | 47 | -18.6 | -8.9 | +7.8 | +10.4 | +9.3 | 18.6 **>10pp FLAG** |

**Agreement rate per batch:**

| Batch | mean agreement | unanimous % |
|---|---:|---:|
| 1 | 0.974 | 91.3% |
| 2 | 0.959 | 83.7% |
| 3 | 0.959 | 85.7% |
| 4 | 0.927 | 69.4% |
| 5 | 0.946 | 79.2% |
| 6 | 0.980 | 89.8% |
| 7 | 0.945 | 76.6% |

## 8. Confidence distribution (from raw labels)

| Confidence | Count | % |
|---|---:|---:|
| HIGH | 1580 | 90.3% |
| MEDIUM | 170 | 9.7% |

## 9. Bucket-type distribution (from raw labels — modal bucket per spot)

Distinct modal buckets: 330. Showing top 20:

| Bucket | Count | % |
|---|---:|---:|
| 4-way-3-bet-pot-AK-OOP-cbet-Q-high | 2 | 0.6% |
| preflop-closing-BTN-suited-connector-3way | 2 | 0.6% |
| BB-defend-closing-broadway-MW-5way | 2 | 0.6% |
| OOP-overpair-MW-protection | 2 | 0.6% |
| UTG-checks-twice-MW-mid-pair-turn | 2 | 0.6% |
| preflop-closing-suited-connector-3way | 2 | 0.6% |
| AA-IP-middle-K-board-call | 2 | 0.6% |
| 4-way-3-bet-pot-AA-IP-cbet | 1 | 0.3% |
| 3-bet-pot-cold-caller-underpair-missed-flop | 1 | 0.3% |
| 3-bet-pot-cold-caller-bluffcatch-OOP-middle | 1 | 0.3% |
| 3-bet-pot-cold-caller-underpair-vs-Q-board | 1 | 0.3% |
| preflop-cold-call-3-bet-trash-IP | 1 | 0.3% |
| preflop-cold-call-3-bet-dominated-broadway | 1 | 0.3% |
| 4-bet-pot-HU-cbet-dry-board | 1 | 0.3% |
| preflop-squeeze-AA-value-multiway | 1 | 0.3% |
| 3-bet-pot-OOP-top-pair-coordinated-board | 1 | 0.3% |
| 3-bet-pot-OOP-overpair-value-protection | 1 | 0.3% |
| 4-way-3-bet-pot-cold-caller-complete-air-IP | 1 | 0.3% |
| preflop-3-bet-IP-creates-4-way-cbet-follow-through | 1 | 0.3% |
| 4-way-3-bet-pot-cbet-OOP-bluff-overpair-miss | 1 | 0.3% |

**Primary axis distribution:**

| Primary axis | Count | % |
|---|---:|---:|
| wrap-draw-MW-OOP | 16 | 4.7% |
| TPTK-MP-early-action-MW | 15 | 4.5% |
| UTG-checks-twice-MW-mid-pair | 14 | 4.2% |
| top-set-multiway-cooler | 13 | 3.9% |
| set-vs-flush-turn-MW | 13 | 3.9% |
| OOP-overpair-MW-protection | 13 | 3.9% |
| TPTK-OOP-early-action | 13 | 3.9% |
| 3-bet-pot-cold-caller-bluffcatch | 12 | 3.6% |
| 4-way-3-bet-pot-flop-3bettor-checks | 12 | 3.6% |
| 4-bet-pot-rare | 11 | 3.3% |
| 4-way-3-bet-pot-AK-OOP-cbet | 11 | 3.3% |
| top-set-FD-board-OOP-MW | 11 | 3.3% |
| AA-IP-middle-MW-vs-K | 10 | 3.0% |
| set-IP-middle-MW | 10 | 3.0% |
| 3-bet-pot-cold-caller-underpair-vs-Q | 9 | 2.7% |
| preflop-3-bet-iso-creates-4-way | 9 | 2.7% |
| 4-way-3-bet-pot-cbet-IP-overpair | 9 | 2.7% |
| 4-way-3-bet-pot-AA-IP-cbet | 8 | 2.4% |
| 3-bet-pot-OOP-overpair | 8 | 2.4% |
| closing-action | 8 | 2.4% |
| BB-defend-closing | 8 | 2.4% |
| 3-bet-pot-cold-caller-coordinated | 7 | 2.1% |
| straight-coordinated-MW | 7 | 2.1% |
| straight-OESD-flush-draw-cooler | 7 | 2.1% |
| 4-way-3-bet-pot-set-mine-flop | 6 | 1.8% |
| 4-way-3-bet-pot-cold-caller-bluff-catch | 6 | 1.8% |
| BB-defend-closing-5way | 6 | 1.8% |
| preflop-closing-suited-A-peel | 6 | 1.8% |
| closing-action-preflop-BTN | 6 | 1.8% |
| 4-bet-for-value | 5 | 1.5% |
| 4-way-3-bet-pot-flop | 5 | 1.5% |
| preflop-closing-suited-connector | 5 | 1.5% |
| BB-defend-5way-suited | 5 | 1.5% |
| cold-call-3-bet-IP | 4 | 1.2% |
| 4-way-3-bet-pot-squeeze | 4 | 1.2% |
| 4-way-3-bet-pot-creation | 3 | 0.9% |
| 4-way-3-bet-pot | 3 | 0.9% |
| TPTK-BTN-vs-MP-3way | 2 | 0.6% |
| middle-pair-draw-IP-MW | 2 | 0.6% |
| FD-OESD-CO-3way | 2 | 0.6% |
| TPGK-BTN-3way-vs-MP-flat | 2 | 0.6% |
| Ace-high-MP-fold-MW | 2 | 0.6% |
| range-asymmetry-SB-vs-BTN | 2 | 0.6% |
| AK-overcards-CO-MW-fold | 1 | 0.3% |
| range-asymmetry-MP | 1 | 0.3% |
| range-asymmetry-MP-vs-UTG | 1 | 0.3% |
| range-asymmetry-EP-vs-BTN | 1 | 0.3% |
| TPMK-MP-MW | 1 | 0.3% |
| range-asymmetry-CO-vs-UTG | 1 | 0.3% |
| range-asymmetry-BTN-vs-MP-coordinated | 1 | 0.3% |

## 10. Cross-tabulations: agreement × position, agreement × action

**Mean agreement rate by hero position:**

| Position | n | mean agreement | unanimous % |
|---|---:|---:|---:|
| BTN | 90 | 0.960 | 84.4% |
| CO | 74 | 0.943 | 77.0% |
| HJ | 20 | 0.950 | 85.0% |
| SB | 43 | 0.972 | 88.4% |
| UTG | 26 | 0.962 | 84.6% |
| MP | 39 | 0.954 | 82.1% |
| EP | 13 | 1.000 | 100.0% |
| BB | 32 | 0.931 | 68.8% |

**Mean agreement rate by consensus action:**

| Action | n | mean agreement | unanimous % |
|---|---:|---:|---:|
| BET | 113 | 0.981 | 91.2% |
| CHECK | 66 | 0.955 | 86.4% |
| FOLD | 31 | 0.968 | 90.3% |
| RAISE | 58 | 0.907 | 56.9% |
| CALL | 69 | 0.951 | 81.2% |

**Position × action: cells with mean agreement < 0.80 (chronic-disagreement combos, n≥5):**

| Position | Action | n | mean agreement | unanimous % |
|---|---|---:|---:|---:|
| _(none with n≥5 and mean<0.80)_ | | | | |

## 11. Top 10 lowest-agreement hands (most likely to drift on re-label)

| spot_id | consensus_action | sonnet_votes | hero_pos | agreement_rate | primary_axis |
|---|---|---|---|---:|---|
| 4WF-4-WAY-3--026 | CHECK | BET,BET,CHECK,CHECK,CALL | CO | 0.40 | 3-bet-pot-cold-caller-underpair-vs-Q |
| 4WF-4-WAY-3--063 | CHECK | CHECK,CHECK,BET,BET,CHECK | HJ | 0.60 | 3-bet-pot-cold-caller-bluffcatch |
| 4WF-4-WAY-3--066 | CHECK | CHECK,BET,CHECK,BET,CHECK | UTG | 0.60 | 4-way-3-bet-pot-flop-3bettor-checks |
| 4WF-4-WAY-3--110 | BET | CHECK,BET,BET,BET,CHECK | CO | 0.60 | 4-way-3-bet-pot-cbet-IP-overpair |
| 4WF-4-WAY-3--114 | CHECK | CHECK,CHECK,CHECK,BET,BET | HJ | 0.60 | 3-bet-pot-cold-caller-bluffcatch |
| 4WF-4-WAY-3--115 | CHECK | BET,CHECK,CHECK,BET,CHECK | CO | 0.60 | 3-bet-pot-cold-caller-underpair-vs-Q |
| 4WF-CLOSING--214 | CALL | CALL,CALL,RAISE,CALL,FOLD | SB | 0.60 | TPTK-OOP-early-action |
| 4WF-CLOSING--216 | CALL | RAISE,CALL,RAISE,CALL,CALL | MP | 0.60 | TPTK-MP-early-action-MW |
| 4WF-CLOSING--240 | FOLD | CALL,CALL,FOLD,FOLD,FOLD | MP | 0.60 | TPTK-MP-early-action-MW |
| 4WF-MULTIWAY-162 | CALL | CALL,CALL,FOLD,FOLD,CALL | BB | 0.60 | set-vs-flush-turn-MW |

---

**Total report rows analyzed: 337**.
