---
date: 2026-05-10
from: QC stream
to: Main terminal (orchestrator)
re: PR #370 — Phase 1.5-D.4 PR 1 SMOKE (vNext-HU 1-seed = 27/30 PASS, +9 above v8-HU baseline)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge milestone (smoke gate; ~15 min)
target_pr_head: ebb29723178a626d840e4bbceb9531df58b1d43f
master_at_audit: 4ed9542
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR370_SMOKE_2026-05-10.md
---

# QC verdict — PR #370 PASS (0/0/0)

53rd solo cycle. 8-item audit + 3-miss analysis VERIFIED. Smoke gate clearly PASS at 27/30 (+14 above ≥13/30 effective floor; +9 over v8-HU 18/30 baseline).

## 8-item summary

1. Trainer matches §4.5 spec — 59-feature assertion, from-scratch (no `xgb_model=`), v9_student-identical hyperparameters, 5-seed-ready, provenance docstring, no inline heredoc ✓
2. Corpus 746 — 50 pilot + 696 full; 59-feature feat_dict; 44 owner-arb-class rows (39 disagree + 5 2-2-1); confidence weights 1.0/0.8/0.6/0.4 ✓
3. Provenance docstring — links Phase 1.5-D.4 dispatch + AMENDMENT to model artifact filename ✓
4. Smoke model — gitignored per dispatch (deferred to 1.5-E force-add); not in PR diff (correct) ✓
5. Smoke score 27/30 — bit-exact: HU-1 4/5 · HU-2 5/5 · HU-3 4/5 · HU-4 5/5 · HU-5 5/5 · HU-6 4/5 ✓
6. Smoke gate — 27/30 vs floor ≥13/30 → PASS clearly ✓
7. Diff scope strict — 5 files; 0 changes to oracle_router.py / models/ / corpus inputs ✓
8. TC-X-DISPATCH-COMPLIANCE negative-scope — 6/6 items honored (no input mod / no solver-as-label / no swap / no model-add / no warm-start / no heredoc) ✓

## 3-miss analysis (special consideration)

| Miss | Direction | Conf | Hypothesis |
|------|-----------|------|------------|
| HU-1.4 turn | CALL→RAISE | 0.95 | Same-direction as v8-HU; possible labeller-pool RAISE-bleed despite owner-CALL adjudication; possible stay-wrong taxonomy |
| HU-3.3 turn | BET→CHECK | 0.50 | Tension: 7 in-corpus owner-CHECK on HU-3.3 lookalikes vs reference modal-consensus BET; borderline conf may flip with seed variance |
| HU-6.5 river | CALL→FOLD | 0.59 | Corpus-exclusion artifact (HU-6.5 excluded per PR #338); model never saw lookalikes; structural miss |

No class-collapse. 3 distinct directions. Builder's CLOSE-marker honesty is correct.

## Notable signal

**HU-2 +4 / HU-3 +3 deltas** (1/5 → 5/5 + 1/5 → 4/5) is the load-bearing signal: v8-HU's known under-aggression on draws/overcards (per `feedback_solver_findings.md`) is FIXED by 59-surface + corrected-corpus retrain. This validates the unified-59-surface workstream design intent.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims VERIFIED bit-exact:
- 27/30 ✓
- Per-axis HU-1 4/5 · HU-2 5/5 · HU-3 4/5 · HU-4 5/5 · HU-5 5/5 · HU-6 4/5 ✓
- HU-2 +4 / HU-3 +3 deltas vs v8-HU ✓
- 3 miss directions + confidence values ✓
- 50+696=746 corpus split ✓

## Smarter-over-time

- HU-6.5 corpus-exclusion = only structural miss; surfacing for post-1.5-D.4 design memo §4.4 amendment candidate (whether to include HU-6.5 owner-adjudicated lookalikes in retrain corpus).
- 27/30 smoke → 1 below ship gate (28/30): variance band makes 5-seed full result 25-29 plausible. CLOSE-marker hands HU-1.4/HU-3.3/HU-6.5 are the swing population.

## Gates

PR #370 cleared. Next: orchestrator merges → builder fires PR 2 (5-seed full); ship gate ≥28/30 (architect-committed). 27 or 26 → STOP/REPORT off-ramp.

## Cycle stats

53rd solo cycle. ~15 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
