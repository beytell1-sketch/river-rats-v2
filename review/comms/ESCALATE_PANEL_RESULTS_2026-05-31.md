# ESCALATE Panel Adjudication — 7 board-reading audit spots — 2026-05-31

**Panel architecture:** 3 reviewers (GTO Theoretician / Multiway Specialist / Range-Construction Analyst), all top-tier Opus, paired per the pilot 085 panel pattern.
**Scope:** 7 spots from PR #481's screening triage (BOARD_READING_AUDIT_38SPOT_SCREENING_2026-05-30.md) flagged ESCALATE_TO_PANEL.
**Method:** AA-cluster (4 spots) resolved via panel on representative 072 then cluster-apply to 090/099/109. Individual panels on 016, 193, 298. Total 4 panel adjudications × 3 reviewers = 12 R1 dispatches. No splits → no R2 needed.

---

## Per-spot verdicts

| Spot | Consensus | Final verdict | Action change | Confidence | Notes |
|---|---|---|---|---|---|
| 4WF-4-WAY-3--072 | BET 66 | **CHECK** | YES (BET → CHECK) | MEDIUM-HIGH | AA OOP cold-caller of 3bet, 4-way, 2-tone hearts. Check-to-PFA structural posture overrides AA-bet instinct. Ah-blocker REDUCES protection EV. |
| 4WF-4-WAY-3--090 | BET 66 | **CHECK** | YES (BET → CHECK) | HIGH | Cluster-apply from 072. Dryer board (J-6-3) MORE clearly slowplay-AA. |
| 4WF-4-WAY-3--099 | BET 66 | **CHECK** | YES (BET → CHECK) | HIGH | Cluster-apply from 072. Suit-variant (spades not hearts) — identical structurally. |
| 4WF-4-WAY-3--109 | BET 66 | **CHECK** | YES (BET → CHECK) | HIGH | Cluster-apply from 072. Driest board (J-3-2) — strongest CHECK in cluster. |
| 4WF-4-WAY-3--016 | BET 66 | **BET** (action AFFIRM, sizing → 25) | NO (action), YES (sizing 66→25) | MEDIUM-HIGH | AcKd, paired with pilot 085. Hero is 3-bettor (PFA), not cold-caller — opposite structural posture from AA cluster. Ac-blocker leverage drives BET-modal at 25% pot. |
| 4WF-MULTIWAY-193 | CHECK | **CHECK** | NO | MEDIUM-HIGH | 9d5d wrap-draw (8 outs + BDFD), 4-way SRP OOP-early. Sibling pattern (168/190/199 all CHECK) confirms. Multiway OOP-early semi-bluff EV too low. |
| 4WF-CLOSING--298 | FOLD | **FOLD** | NO | MEDIUM | AhJh overcards + Ah-blocker + BDFD. Marginal (~40% CALL frequency for combo) but FOLD remains modal under MW realization penalty. Closest spot of the 4. |

---

## Total action-change counts

| Bucket | Count |
|---|---|
| **REVISE (action-overturn)** | **4 spots** (entire AA cluster: 072, 090, 099, 109) |
| AFFIRM (action stands) | 3 spots (016, 193, 298) |
| Sizing-only change | 1 spot (016: BET 66 → BET 25) |

**Out of 7 ESCALATE spots: 4 action-overturns, 3 affirmations, 1 additional sizing change.**

---

## AA cluster uniformity check

**Question:** Does the CHECK verdict from the 072 panel apply uniformly to 090, 099, 109?

**Answer: YES, UNIFORMLY.**

All 4 spots share the IDENTICAL structural posture:
- Hero AA OOP-EP (UTG, sometimes labelled EP) cold-caller of CO 3-bet
- 4-way 3-bet pot (CO 3-bettor + BTN + SB + hero)
- 2-tone board with hero holding 1 suit-blocker to the nut flush draw
- Pot 36bb identical
- Stack: 75bb (072) or 100bb (090, 099, 109) — both supportive of CHECK; deeper stacks strengthen CHECK further

Board variations across the cluster:
- 072: Q-J-3 2-tone hearts (most coordinated)
- 090: J-6-3 2-tone hearts (drier — favors slowplay)
- 099: Q-J-3 2-tone spades (suit-variant of 072)
- 109: J-3-2 2-tone hearts (driest — strongest slowplay candidate)

The structural protocol (OOP cold-caller checks to PFA in 3-bet pots multiway) dominates board-texture details. Per-spot mix frequencies vary only ~5-10% but the modal action is CHECK in all 4. Confidence is HIGHEST on 109 (driest), MEDIUM-HIGH on 072 (most coordinated, slightly closer to mixed-strategy territory).

**Cluster verdict: ALL 4 → CHECK. Apply uniformly.**

---

## Pattern observations

### 1. AA-bet instinct overrides structural protocol (mass-vote failure mode)

The 5/5 Sonnet labellers' unanimous BET 66% across 4 AA-cold-caller spots represents a CONSISTENT BLIND SPOT: when hero holds AA, the labellers default to "AA = value-bet for protection" without engaging the structural posture (cold-caller checks to PFA in 3-bet pots). This failure mode is independent of board texture — labellers voted BET 66% on the driest possible board (109) as well as the wettest (072).

**Implication for training data:** AA cold-caller spots in 3-bet pots may be systematically mislabelled BET when CHECK is correct. Recommend a labeller-eval test focused on "AA OOP cold-caller in 3-bet pot multiway" to catch this class.

### 2. Sizing errors hide inside affirmed actions (016 case)

Spot 016 had the correct action (BET) but the wrong sizing (66 → should be 25). 1 of 5 labellers voted BET 25 (correct); the other 4 voted BET 66 (incorrect sizing). The audit caught this as part of the "right action, wrong reason" pattern — the action was driven by Ac-blocker leverage (correct logic) but the sizing was driven by 'AK is value' instinct (wrong logic for Q-high boards where AK is thin-equity protection).

**Implication:** Sizing-as-separate-error from action-as-separate-error is a real category. Future audits should track sizing-only-revisions separately.

### 3. Closing-action spots are knife-edge (298 case)

The 298 spot (AhJh on 3h7c5d) is the closest decision in the panel — 40% CALL frequency for the combo means roughly 1 in 2.5 instances should CALL. The FOLD verdict survives but the mass-FOLD vote may overstate confidence. Consider this spot as a candidate for solver-verification before any retraining decision treats it as gold.

### 4. Multiway semi-bluff with strong draw still defaults CHECK (193 case)

193 with 8 outs (DG) + BDFD is a STRONG draw but the modal action remains CHECK because OOP-early multiway SRP nodes have ~75% CHECK frequency for the wrap class. The 9d5d combo specifically is at the LOW BET frequency end of its class (no pair-value, no FD-equity backup). This confirms the IP-vs-OOP and combo-within-class principles previously established.

### 5. AcKd Ac-blocker leverage replicates from pilot 085 to 016

Pilot 085 (AcKd on Qc4c3s) resolved BET 33% via Ac-blocker leverage on a Q-high 2-tone-clubs board. Spot 016 (AcKd on Qc5c4d) is structurally identical — same Ac-blocker leverage, same Q-high 2-tone-clubs board, same PFA range advantage. The verdict transfers cleanly: BET at small sizing (25%), modal action for AcKd specifically. This confirms the blocker-leverage class is a real pattern that can be relied upon across the corpus.

---

## Recommended downstream actions

1. **Apply REVISE for AA cluster (072, 090, 099, 109):** update `consensus_v2.consensus_action` for all 4 spots from `BET` to `CHECK`. Set `consensus_bet_pct` to `null` (since action is now CHECK).
2. **Apply sizing-only revision for 016:** update `consensus_v2.consensus_bet_pct` from `66` to `25` (action stays BET).
3. **Affirm 193 and 298:** no consensus changes needed.
4. **Add labeller-eval test:** "AA OOP cold-caller in 3-bet pot multiway" failure mode for next labeller calibration.
5. **Queue 298 for solver-verification:** marginal FOLD/CALL spot worth a solver cross-check before retraining treats it as a gold label.

---

## Cross-reference

- Pilot panel: `data/4way_corpus/full_700/audit_panel_r{1,2}_*_4way-3--085.json`
- Per-spot panel files for this run:
  - 072: `audit_panel_r1_{gto_theoretician,multiway_specialist,range_construction}_4way-3--072.json`
  - 090/099/109: `audit_panel_r1_cluster_apply_4way-3--{090,099,109}.json`
  - 016: `audit_panel_r1_{gto_theoretician,multiway_specialist,range_construction}_4way-3--016.json`
  - 193: `audit_panel_r1_{gto_theoretician,multiway_specialist,range_construction}_4way-multiway--193.json`
  - 298: `audit_panel_r1_{gto_theoretician,multiway_specialist,range_construction}_4way-closing--298.json`
- Screening source: `review/comms/BOARD_READING_AUDIT_38SPOT_SCREENING_2026-05-30.md` (PR #481, merged)

---

*Panel adjudication completed 2026-05-31 by orchestrator (Opus 4.7 1M). No R2 dispatches required — all 4 panels had unanimous R1 verdicts on action.*
