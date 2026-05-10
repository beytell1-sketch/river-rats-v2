---
date: 2026-05-10
from: QC stream
to: Main terminal (orchestrator)
re: PR #367 — Phase 1.5-D.4 PR 0 (eval-infra: 30-hand HU reference + evaluator + v8-HU baseline 18/30)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge milestone (eval-infra prerequisite for D.4 smoke + 5-seed; ~15 min)
target_pr_head: 25bf75b00cbb844b6af62069840b082e2a7ac6e4
master_at_audit: fdd3084
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR367_EVAL_INFRA_2026-05-10.md
---

# QC verdict — PR #367 PASS (0/0/0)

52nd solo cycle. 8-item audit + 2 special considerations VERIFIED.

## 8-item summary

1. Diff scope — 4 files / +559; NO production-swap / NO oracle_router edit / NO model force-add ✓
2. 30 reference rows — 5 per axis (HU-1..HU-6); 12 CANONICAL + 18 CLOSE ✓
3. expected_action sourcing — 26 modal-lookalike-consensus + 4 owner-adjudicated; all traceable via `expected_source` field ✓
4. Parser determinism — script logic review (no random/seed/sample); XGBoost predict deterministic; action normalization pure function ✓
5. v8-HU baseline 18/30 — bit-exact: per-axis 3/5/1/5/1/5/4/5/4/5/5/5; miss 12 (5 BET→CHECK + 4 CALL→FOLD + 2 CALL→RAISE + 1 CHECK→BET) ✓
6. Ambiguities — 0 unflagged; every row has `expected_source` ✓
7. Action distribution — 14 BET / 10 CALL / 3 CHECK / 2 FOLD / 1 RAISE = 30 ✓
8. TC-X-DISPATCH-COMPLIANCE per AMENDMENT (PR #366) — 4 deliverables present; negative-scope honored ✓

## Special considerations

**18/30 baseline impact assessment**: GENUINE, not artifact. Per-axis distribution + miss patterns + sample HU-2.1/2.5/3.1 hands all consistent with v8-HU's known under-aggression bias on draws/overcards. PokerBench 88.1% does NOT linearly project to 30-hand HU close-set because close spots dominantly miss. Orchestrator's gate decisions (smoke ≥13/30 effective; ship ≥28/30 unchanged) ACCEPT.

**expected_action sourcing methodology**: DEFENSIBLE. Modal-lookalike-consensus is reproducible + auditable. 1 of 30 rows (HU-6.4-LK-24, CALL) from PR #362 orchestrator-adjudicated 44-batch is in solver-queue; if solver later disagrees, 1 reference row affected — acceptable risk per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims VERIFIED bit-exact:
- 18/30 baseline ✓
- Per-axis HU-1 3/5 · HU-2 1/5 · HU-3 1/5 · HU-4 4/5 · HU-5 4/5 · HU-6 5/5 ✓
- 5/12 under-aggression BET→CHECK pattern ✓
- 14 BET / 10 CALL / 3 CHECK / 2 FOLD / 1 RAISE ✓
- 0 unflagged ambiguities ✓

## Smarter-over-time

- Eval-infra-first pattern (PR0 before smoke) is good Option B precedent: surfaces baseline + parser-determinism + ref-set audit BEFORE 5-seed compute commitment. Recommend as standing pattern for retrain phases.
- 18/30 baseline = novel design-memo §4.6 input. Document for post-1.5-D.4 amendment.

## Gates

PR #367 cleared. Next: orchestrator merges → builder fires PR 1 (smoke 1-seed) per 1.5-D.4 dispatch. Smoke gate ≥13/30 effective; ship gate ≥28/30 unchanged.

## Cycle stats

52nd solo cycle. ~15 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
