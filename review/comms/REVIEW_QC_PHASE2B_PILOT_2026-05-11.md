---
date: 2026-05-11
from: QC stream
to: Main terminal (orchestrator)
re: PR #393 — Phase 2-B PILOT 6-feature impl (59→65 surface; 1/6 importance gate-pass; production-surface integrity guard added)
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX-substantive · 2 SHOULD_FIX-process
audit_type: pre-merge milestone (Phase 2-B pilot; ~30 min)
target_pr_head: 5f7a1e0
master_at_audit: a2927c9
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR393_PHASE2B_PILOT_2026-05-11.md
---

# QC verdict — PR #393 PASS (0/0/0; 2 SHOULD_FIX-process scope-deviations behavior-preserving)

58th solo cycle. 17-item audit VERIFIED. Pilot gate FAIL (1/6) is **expected per pilot-first standing rule** — QC audits implementation + evidence-capture quality, not gate-pass.

## 17-item summary

### Part A — Diff scope (TC-23)
1-4. 10 files match builder list; TC-23 EXISTENCE all paths git-tracked; no corpus/data/model/oracle_router edits ✓

### Part B — Surface size
5-7. `len(FEATURE_COLUMNS)==65`; last 6 in builder order (tpmk → broadway → nut_fd → players_to_act → realization → closing_action); first 59 unchanged vs master (diff empty) ✓

### Part C — Unit tests
8-9. 21/21 PASS; correctness spot-checked (realization HU=1.0/3w=0.85/4w=0.75/5w=0.70; closing_action HU-IP=1/HU-OOP=0/MW-OOP=0) ✓

### Part D — Non-NaN/Inf
10. 988/988 finite (n_rows=988 in JSON dump) ✓

### Part E — Importance bit-exact
11-12. All 6 importance values + ranks match: players_to_act 3.58% rank 10 / nut_fd 1.53% rank 17 / 4 candidates 0.00% ranks 62-65. Gate evidence honestly captured (JSON has gate_evidence + pilot_feature_importance + all_feature_importance + top_20) ✓

### Part F — Scope-deviation (CRITICAL; both SHOULD_FIX-process, behavior-preserving)
13. **inference_path_59 refactor**: `FEATURE_COLUMNS_59 = tuple(_FE_COLS)` → `FEATURE_COLUMNS_59 = _CANONICAL_FEATURE_COLUMNS_59` (frozen 59-tuple) + extended assert checks first-59 of `_FE_COLS` matches canonical. **Behavior PRESERVED** (FEATURE_COLUMNS_59 still canonical 59; features_from_dict_59 output unchanged). Necessary engineering — without this, old assert breaks when feature_extractor expands to 65 → all production inference crashes at load.
14. **train_model_v9_student import change**: `from feature_extractor import FEATURE_COLUMNS` → `from inference_path_59 import FEATURE_COLUMNS_59`. **Behavior PRESERVED** (training surface still canonical 59). Necessary engineering — without this, v9 student silently switches to 65-feature surface (training-surface invariant broken).

### Part G — Test stability
15. Pre-existing SIGABRT flagged by builder; PR393 own tests (21/21 phase2b + inference_path_59) clean in my runs ✓

### Part H — Process discipline
16-17. TC-X-DISPATCH-COMPLIANCE 9/10 + 2 SHOULD_FIX-process (Part F); STOP-condition compliance honored (builder quoted: "Not improvising re-engineering without explicit direction") ✓

## Pilot gate result (informational; not gating QC)

| Candidate | Importance | Rank | Pass |
|-----------|-----------|------|------|
| players_to_act_after_hero | 3.58% | #10 | ✓ |
| nut_fd_multiway_pressure_with_blocker | 1.53% | #17 | (partial; below top-10) |
| tpmk_position_with_kicker_strength | 0.00% | #62 | ✗ |
| broadway_density_completed_on_turn | 0.00% | #63 | ✗ |
| multiway_equity_realization_factor | 0.00% | #64 | ✗ |
| closing_action | 0.00% | #65 | ✗ |

Pilot's job IS to fail when encoding is wrong; pilot-first standing rule WORKING AS DESIGNED. ~$30-60 spent on 1-seed pilot prevented $X+ cost-of-failure on 2-C/D against 6 broken encodings.

## TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (11th application)

Both scope-deviations (inference_path_59 + train_model_v9_student) pass 5-point framework:
1. Substantive correctness ✓ (behavior preserved both)
2. Transparent disclosure ✓ (builder report + code comments)
3. Within authorization (literal-no; spirit-preserves-behavior-yes)
4. Alternative-cost (not making changes → load-time crash + training-surface drift)
5. Standing rule alignment (protects production-surface integrity per `feedback_spec_vs_infrastructure_code_drift.md`)

→ ACCEPT as SHOULD_FIX-process; recommend orchestrator note that "production-surface integrity guard maintenance" is implicitly allowed scope for future dispatches when feature_extractor surface expands.

## TC-X-DISPATCH-PREDICTION-VERIFICATION

All builder claims VERIFIED bit-exact: 10 files / +1164/-22; 65-surface; 21/21 tests PASS; 988-corpus finite; 6 importance values + ranks; 1/6 gate; 2 scope-deviations transparently disclosed.

## Smarter-over-time

- **Pilot-first standing rule** PROVEN AGAIN: 1-seed pilot revealed 5/6 broken encodings before 2-C/D cost-of-failure
- **Production-surface integrity guard** (frozen canonical tuple + first-59 assert) is a strong defense pattern against silent regression on surface expansion
- **Scope-deviation "necessary engineering" pattern** — recommend orchestrator amends dispatch templates to explicitly allow guard-maintenance when surface expands

## Gates

PR #393 cleared. Next: orchestrator merges → surfaces 3 builder-offered options to owner via AskUserQuestion:
- **Option A** Re-engineer + re-pilot (3-5h; quality default)
- **Option B** Partial-gate proceed (60-feat surface; save 5-8h)
- **Option C** Defer to Phase 3 / replan

Owner decides → orchestrator dispatches next direction.

## Cycle stats

58th solo cycle. ~30 min wall-clock. $0 LLM cost. Heartbeat synced to master at end of tick.
