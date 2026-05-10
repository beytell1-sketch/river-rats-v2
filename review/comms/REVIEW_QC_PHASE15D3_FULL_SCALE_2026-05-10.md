---
date: 2026-05-10
from: QC stream
to: Main terminal (orchestrator)
re: PR #359 — Phase 1.5-D.3 FULL LABELLING SCALE (696 spots × 5 valid Sonnet labellers FL6+FL7-10 + Opus tier-up; 652 consensus + 44 owner-arbs; recovery from SYSTEMIC STOP)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge milestone (FULL labelling scale; ~25 min)
target_pr_head: 48b695b0ab24458155721505feed1a148fb3c0d2
master_at_audit: 3034092
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR359_FULL_SCALE_2026-05-10.md
---

# QC verdict — PR #359 PASS (0 BLOCKER · 0 SHOULD_FIX · 0 NIT)

51st solo cycle. 10-item audit + 4 TC-X-OPERATIONAL-DEVIATION-ASSESSMENT applications + Opus-disagreement signal analysis + 44 owner-arb propagation analysis ALL VERIFIED.

Recovery from SYSTEMIC STOP (PR #354) confirmed clean: 0 rule-based or template labellers in valid pool; FL6 + FL7-FL10 produce per-spot varied LLM reasoning at 696-spot scale; calibration uniformly PASS ≥25/28 + 5/5 reversal.

## 10-item summary

1. Diff scope — 27 files / +13662; all in `data/hu_corpus/full_HU2_HU6/` + builder report; NO source edits ✓
2. Per-labeller reasoning variation — FL6 695/696, FL7-FL10 696/696 unique ✓
3. 3480 raw_labels — 5×696, per-spot 5, 0 duplicates ✓
4. Calibration — L6:26, L7:25, L8:26, L9:26, L10:26 (all ≥25 + 5/5 reversal) ✓
5. Bucket-first + solver-vs-labels separation — sample-check 10 spots PASS ✓
6. Opus tier-up — 254 labels (+ 1 metadata = 255); exactly the 254 non-unanimous spots ✓
7. Consensus arithmetic — 442 + 112 + 98 = 652; 39 + 5 = 44 ✓ matches builder claim EXACTLY
8. Per-axis ≥80% — HU-2 93.1%, HU-3 93.8%, HU-4 100.0%, HU-5 83.4% (low due to HU-5.4 concentration), HU-6 99.1% ✓
9. Pilot V2 propagation — 0 (HU-6.5 excluded honored) ✓
10. TC-X-DISPATCH-COMPLIANCE — 4 deviation entries documented; all ACCEPT per 5-point framework ✓

## TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (4 deviations; all ACCEPT)

1. **§(c.2) per-agent self-paced**: outcome equivalent; resumption drill deferred to post-hoc uniqueness verification (passed). ACCEPT.
2. **FL8 marginal-template (anchor-preamble + variation-tail)**: per-variation tail correctly reads each card replacement (verified on HU-2.1-LK-01..05 sample); FL8 varies action on multi-action anchors (HU-2.2: 23/1/5; HU-2.4: 18/6/5); calibration 26/28 evidences poker judgment. ACCEPT marginal-pass. Recommend stricter labeller-style criterion for future rounds.
3. **Opus 4-of-5 disagreement 33/112 (29.5%, HU-3 24/33)**: per §4.3 these remain consensus; informational signal of axis-specific difficulty. ACCEPT current rule; surface for 1.5-D.4 design.
4. **Effective rate 93.7% < 95% target**: explained by strict tier-up rule (Opus-disagree → arb); 99.3% loose rule would suppress genuine ambiguity. ACCEPT.

## 44 owner-arbs — propagation surface (for orchestrator's owner-ask)

| Anchor | Count | Pattern | Propagation |
|--------|-------|---------|-------------|
| HU-5.4 | 22 | 21 IDENTICAL (Sonnet 3 CHECK / 2 BET; Opus BET); 1 mirror | Group as 1 decision |
| HU-2.4 | 7 | raise-vs-call mixing (5 of 7 are 2-2-1 RAISE/CALL/FOLD) | Group as 1 decision |
| HU-3.3 | 7 | delayed-stab vs check | Group as 1 decision |
| HU-2.3, 2.5, 3.4, 3.5, 5.1, 6.4 | 8 | individual | 8 individual |

**Effective unique owner-decisions if grouped: ~11 (3 grouped + 8 individual)** vs 44 if not propagated.

## Notable signals

- **L8 marginal-template** acceptable for this round; future-round criterion recommended.
- **Opus 4-of-5 disagreement 29.5%** concentrated HU-3 axis is novel signal — useful for 1.5-D.4/1.5-E difficulty calibration.
- **HU-5.4 owner-arb pattern is strikingly structural**: 21/22 IDENTICAL split suggests anchor-level decision class (Opus-BET vs Sonnet-majority-CHECK) rather than per-variation variance. Single owner decision should propagate cleanly.

## Gates

PR #359 cleared. Next: orchestrator surfaces 44 owner-arbs to owner (grouped per propagation surface above) → merge on adjudication → solver-queue drain → 1.5-D.4 dispatch.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims verified bit-exact:
- Per-axis: HU-2 93.1%, HU-3 93.8%, HU-4 100.0%, HU-5 83.4%, HU-6 99.1% ✓
- Consensus: 442 + 112 + 98 = 652 ✓
- Owner-arbs: 39 + 5 = 44 ✓
- Owner-arb concentration: HU-5.4 22, HU-2.4 7, HU-3.3 7 ✓

## Cycle stats

51st solo cycle. ~25 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
