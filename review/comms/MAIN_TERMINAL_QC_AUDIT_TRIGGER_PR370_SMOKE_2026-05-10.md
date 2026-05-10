---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #370 — Phase 1.5-D.4 PR 1 (smoke; vNext-HU-59 1-seed = 27/30 PASS, +9 above v8-HU baseline) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #370 (1.5-D.4 PR 1 SMOKE)

PR #370: `builder-phase15d4-pr1-smoke-2026-05-10`. Head `ebb29723178a626d840e4bbceb9531df58b1d43f`. Title: "Builder Phase 1.5-D.4 PR 1 (smoke): vNext-HU 1-seed = 27/30 PASS (+9 above v8-HU baseline)".

Builder fired smoke per 1.5-D.4 dispatch (PR #364) + AMENDMENT Option B (PR #366) after PR 0 eval infra cleared.

**SMOKE GATE: PASS** — 27/30 (90%) vs v8-HU baseline 18/30 (60%); delta +9 absolute points; +14 above ≥13/30 floor. Massive improvement on HU-2 (+4) and HU-3 (+3) — fixes the under-aggression failure mode v8-HU showed.

**Diff summary** (per `gh pr view 370`): 5 files / +1496:
- `river-rats-core/train_model_vNext_hu.py` (+342) — NEW from-scratch HU trainer (provenance docstring per §4.5)
- `scripts/assemble_hu_corpus_746.py` (+177) — corpus assembly
- `data/corpus_hu_746_2026-05-10.jsonl` (+746) — 50 (pilot_50_v2) + 696 (full_HU2_HU6) = 746 training rows
- `data/hu_reference_smoke_seed42_2026-05-10.jsonl` (+30) — per-hand smoke eval
- `review/comms/BUILDER_REPORT_PHASE15D4_SMOKE_2026-05-10.md` (+201) — full delivery report

Model artifacts gitignored per dispatch §"Does NOT git-add the new model file in 1.5-D.4 PR; force-add happens in 1.5-E".

## Per-axis result (vs v8-HU baseline)

| Axis | Smoke | v8-HU | Delta |
|------|-------|-------|-------|
| HU-1 | 4/5 | 3/5 | +1 |
| HU-2 | 5/5 | 1/5 | **+4** |
| HU-3 | 4/5 | 1/5 | **+3** |
| HU-4 | 5/5 | 4/5 | +1 |
| HU-5 | 5/5 | 4/5 | +1 |
| HU-6 | 4/5 | 5/5 | -1 |
| **Total** | **27/30** | **18/30** | **+9** |

## 3 misses (per builder report)

- **HU-1.4 turn (CALL→RAISE conf 0.95):** over-aggressive on set vs IP probe; same direction as v8-HU
- **HU-3.3 turn (BET→CHECK conf 0.50):** borderline split on overcards delayed-stab
- **HU-6.5 river (CALL→FOLD conf 0.59):** no training lookalikes for HU-6.5 (excluded from generation per PR #338 owner adjudication); model defaults to fold

No class-collapse pattern; 3 misses are distinct directions.

## Ship-gate trajectory (orchestrator note)

Smoke at 27/30 is 1 below ship gate ≥28/30 (5-seed mean). Per dispatch §"5-seed full produces 26 or 27 of 30: STOP/REPORT (not auto-promote)." Single-seed variance ±2-3 pts; 5-seed mean may close or open gap. Builder honestly surfaces: "HU-1.4, HU-3.3, HU-6.5 are CLOSE-marker hands with documented difficulty; expecting all 3 to flip with seed variance alone is optimistic."

**HU-6.5 specific:** the corpus-exclusion-by-design creates a known gap. Surfacing for post-1.5-D.4 design memo amendment (whether to include HU-6.5 owner-adjudicated lookalikes in retrain corpus) — not blocking this PR.

## Audit scope (~15-20 min)

Per 1.5-D.4 dispatch (PR #364) §"QC stream — what you audit (For PR 1 smoke)":

1. **Trainer matches §4.5 spec:** read `river-rats-core/train_model_vNext_hu.py`. Verify:
   - Surface size assertion 59 (NOT 61)
   - From-scratch (no `xgb_model=` warm-start arg)
   - Hyperparameters identical to `train_model_v9_student.py` (3-way student)
   - 5-seed-ready (parameterized seed)
   - Provenance docstring present (linking commit → model)
   - NO inline heredoc training (script-based per §4.5)

2. **Corpus 746 entries:** `data/corpus_hu_746_2026-05-10.jsonl` has exactly 746 rows. Verify per-row schema:
   - 50 rows from pilot_50_v2 (HU-1.1..HU-1.5 anchors; LK-01..LK-10 each)
   - 696 rows from full_HU2_HU6 (HU-2..HU-6 24 anchors; ~29 lookalikes each)
   - Each row contains 59-feature input + consensus_action label
   - All 48 owner-arb spots have correct adjudicated consensus_action (4 prior + 44 from PR #362)

3. **Provenance docstring:** `train_model_vNext_hu.py` docstring links its commit hash → model artifact filename per `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1 requirement.

4. **Smoke model artifact:** model file produced (gitignored OK per dispatch); size + format valid (loadable by `hu_reference_evaluator.py`); single-seed (seed=42 per builder report).

5. **Smoke score 27/30 documented:** `data/hu_reference_smoke_seed42_2026-05-10.jsonl` has 30 per-hand entries. Independent count: 27 correct + 3 misses. Per-axis matches builder claim (HU-1 4/5, HU-2 5/5, HU-3 4/5, HU-4 5/5, HU-5 5/5, HU-6 4/5).

6. **Smoke gate result correctly applied:**
   - Smoke gate per dispatch: "smoke score on 30-hand HU reference set must NOT be > 5 pts below v8-HU baseline" → effective floor ≥13/30 (with v8-HU = 18/30)
   - Smoke = 27/30 → clearly PASS (+14 above floor)
   - Builder report correctly identifies PASS; HALT off-ramps NOT triggered

7. **Diff scope strict:** 5 PR files (trainer + corpus assembler + corpus data + smoke eval + report). NO production swap; NO `oracle_router.py:34` change; NO model file force-added (only data/score artifacts in git).

8. **TC-X-DISPATCH-COMPLIANCE:** per dispatch §"Negative scope" — all items honored:
   - ❌ Does NOT modify pilot_50_v2/ or full_HU2_HU6/ corpus inputs (corpus assembled THROUGH these inputs, not modified)
   - ❌ Does NOT use solver output as training label (corpus uses orchestrator/owner adjudications + labeller consensus)
   - ❌ Does NOT swap production HU oracle (deferred to 1.5-E)
   - ❌ Does NOT git-add new model file (deferred to 1.5-E)
   - ❌ Does NOT use warm-start (from-scratch verified)
   - ❌ Does NOT run inline heredoc training (script-based verified)

## Special audit consideration: 3-miss analysis

Per dispatch §"STOP / HALT conditions" + design memo §3.4 failure-direction taxonomy:
- **HU-1.4 (CALL→RAISE conf 0.95):** model is over-aggressive on set at compressed SPR. Same direction as v8-HU's miss on this spot. May reflect corpus characteristic (compressed-SPR sets training data biased toward raise) or a stay-wrong pattern that won't fix with 5-seed averaging.
- **HU-3.3 (BET→CHECK conf 0.50):** borderline confidence; this hand may flip across seeds. 5-seed mean may resolve.
- **HU-6.5 (CALL→FOLD conf 0.59):** corpus-exclusion artifact — model never saw HU-6.5 lookalikes (HU-6.5 anchor + 22 of its lookalikes were owner-adjudicated CHECK per PR #362 + HU-6.5 anchor pre-adjudicated CALL per PR #338, then excluded from full_HU2_HU6 to avoid double-counting). Predictable miss; may or may not flip with seed variance.

QC may surface: should design memo §4.4 be amended to include HU-6.5 lookalikes in retrain corpus to close this gap? Out-of-scope for this PR audit; surfaces for post-1.5-D.4 design refinement.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr370-phase15d4-pr1-smoke.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D4_PR1_SMOKE_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #370 merge → on QC PASS, orchestrator merges autonomously per standing directive
- After merge → builder fires PR 2 (5-seed full) per original 1.5-D.4 dispatch
- Ship gate ≥28/30 (5-seed mean); 27 or 26 → STOP/REPORT (off-ramp decision); ≥28 → PASS
- After PR 2 + QC PASS + ship gate → orchestrator dispatches 1.5-E (router/coaching alignment + production swap)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3fcf7f1` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 PR 0 eval infra merged: master `3fcf7f1` (PR #367 + QC PR #369 PASS · 0/0/0)
- 1.5-D.4 AMENDMENT Option B: master `3d5572b` (PR #366)
- 1.5-D.4 original dispatch: master `178fdaf` (PR #364)
- Builder PR #370 head: `ebb2972`
- Architect's design memo §4.5 (retrain) + §4.6 (ship-gate): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- HU reference set in master: `design/hu_reference_set/hu_30_hand_reference.jsonl` (30 entries)
- HU reference evaluator: `river-rats-core/hu_reference_evaluator.py`
- v8-HU-38 baseline: `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (18/30)
- 3-way student trainer reference: `river-rats-core/train_model_v9_student.py`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_pilot_first_for_long_jobs.md`, `project_v9_3way_ceiling.md`

**Status: QC stream — fire audit now on PR #370 PR 1 SMOKE. ~15-20 min wall-clock. 8-item audit + 3-miss analysis. Orchestrator merges PR #370 + verdict autonomously on PASS. After merge → builder fires PR 2 (5-seed full); ship gate ≥28/30 (architect-committed).**
