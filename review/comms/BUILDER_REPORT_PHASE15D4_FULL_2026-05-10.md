---
date: 2026-05-10
from: LEAD-PROGRAMMER (builder; architect-hat for trainer adaptation)
to: Main terminal (orchestrator) · QC stream · Owner (informational)
re: Phase 1.5-D.4 PR 2 (5-seed full) — vNext-HU-59 5-seed mean 28.2/30; median (canonical) 28/30 — SHIP GATE PASS
status: DELIVERY — ship gate PASS at 28/30 exactly; orchestrator authorizes 1.5-E
---

# Phase 1.5-D.4 PR 2 — 5-seed full delivery

## Summary

Per 1.5-D.4 dispatch (PR #364) §"Builder deliverables PR 2 (5-seed full; only if smoke clears)" + smoke PASS authorization (PR #370 + QC PASS PR #372).

- **Trainer**: `river-rats-core/train_model_vNext_hu.py` (unchanged from PR #370)
- **Corpus**: `data/corpus_hu_746_2026-05-10.jsonl` (unchanged from PR #370)
- **5-seed models**: `models/gto_model_vNext_hu_59feat_seed{0,1,2,3,4}.json`
- **Canonical artifact (median)**: `models/gto_model_vNext_hu_59feat.json` (= seed=3 by held-out accuracy median)
- **5-seed training report**: `models/gto_model_vNext_hu_59feat_5seed_report.json`
- **5-seed reference eval**: `data/hu_reference_5seed_seed{0,1,2,3,4}_2026-05-10.jsonl`
- **This report**

**SHIP GATE: PASS** — canonical (median) artifact scores 28/30 (93.3%) on 30-hand HU reference, AT the ≥28/30 architect-committed ship gate. 5-seed mean 28.2/30; 4 of 5 seeds at gate; 1 seed (seed=1) above at 29/30.

## §1 — 5-seed training results

| Seed | Held-out acc | Held-out weighted | Boosted rounds | 30-hand ref score |
|------|--------------|-------------------|----------------|-------------------|
| 0 | 0.933 | 0.943 | 743 | **28/30** |
| 1 | 0.960 | 0.957 | 325 | **29/30** ← BEST |
| 2 | 0.967 | 0.969 | 800 | **28/30** |
| 3 | 0.960 | 0.976 | 800 | **28/30** ← MEDIAN (canonical) |
| 4 | 0.967 | 0.968 | 719 | **28/30** |
| **Mean** | **0.957** | **0.963** | **677** | **28.2/30** |

**Canonical artifact selection**: median seed by held-out accuracy = seed 3 (acc 0.960). Held-out median is the standard v9_student selection criterion; avoids cherry-picking on reference-eval (gaming the ship-gate). Canonical artifact 30-hand-ref score = 28/30 = AT SHIP GATE.

## §2 — 30-hand HU reference eval (5-seed canonical = 28/30)

### Per-axis breakdown (canonical median seed=3 vs v8-HU baseline)

| Axis | Canonical (seed=3) | v8-HU baseline | Delta |
|------|---------------------|----------------|-------|
| HU-1 | 4/5 (80%) | 3/5 (60%) | +1 |
| HU-2 | 5/5 (100%) | 1/5 (20%) | **+4** |
| HU-3 | 5/5 (100%) | 1/5 (20%) | **+4** |
| HU-4 | 5/5 (100%) | 4/5 (80%) | +1 |
| HU-5 | 5/5 (100%) | 4/5 (80%) | +1 |
| HU-6 | 4/5 (80%) | 5/5 (100%) | -1 |
| **Total** | **28/30 (93.3%)** | **18/30 (60.0%)** | **+10** |

Smoke (seed=42) was 27/30 with HU-3.3 also miss; 5-seed all CLEAR HU-3.3 — pure seed variance.

### Per-axis 5-seed dispersion (informational)

| Axis | Min | Max | Range |
|------|-----|-----|-------|
| HU-1 | 4/5 | 4/5 | 0 |
| HU-2 | 5/5 | 5/5 | 0 |
| HU-3 | 5/5 | 5/5 | 0 |
| HU-4 | 5/5 | 5/5 | 0 |
| HU-5 | 5/5 | 5/5 | 0 |
| HU-6 | 4/5 | 5/5 | 1 |
| **Total** | **28** | **29** | **1** |

Tight per-axis dispersion (range = 0 on 5 of 6 axes). Variance concentrated on HU-6 axis (HU-6.5 specifically — see §3).

## §3 — Per-hand stay-wrong taxonomy (across 5 seeds + smoke)

Per dispatch §"Per-hand stay-wrong tracking required (per §3.4)" + `project_v9_3way_ceiling.md` taxonomy.

### Stuck-wrong hands (miss in ≥3/5 seeds)

| Spot | Marker | Street | Expected | 5-seed predictions | Smoke | Direction | Taxonomy |
|------|--------|--------|----------|---------------------|-------|-----------|----------|
| HU-1.4 | CLOSE | turn | CALL | 5/5 RAISE | RAISE | Over-aggressive | **model-stuck pipeline-aligned**: model consistently picks RAISE; lookalike consensus split (CALL:5/RAISE:5) means training data itself is mixed; model defaults to RAISE under class-weight-cap pressure. Pipeline-aligned because predictions match a coherent (if wrong) GTO line. |
| HU-6.5 | CLOSE | river | CALL | 4/5 FOLD (1/5 CALL via seed=1) | FOLD | Over-folding | **pipeline-canonical mismatch**: HU-6.5 is the ONLY 30-hand reference anchor with NO lookalikes in training corpus (excluded from generation per `scripts/hu_anchors_axes_2_6.py`); model never trained on this anchor's variations. Mostly defaults to FOLD vs 150% overbet. Seed=1 happens to predict CALL — variance, not stable signal. |

### Variance hands (miss in only 1-2 seeds)

| Spot | Marker | Street | Expected | 5-seed predictions | Smoke | Direction | Taxonomy |
|------|--------|--------|----------|---------------------|-------|-----------|----------|
| HU-3.3 | CLOSE | turn | BET | 5/5 BET (✓) | CHECK (conf 0.50) | Under-aggressive (smoke only) | **seed variance**: 5-seed clears; smoke seed=42 borderline (conf 0.50 = uncertain split). Not a model-stuck issue; resolved by seed selection. |

### Class-collapse check

No class-collapse pattern. Misses are split between over-aggressive (HU-1.4) and over-folding (HU-6.5); the model uses all 5 actions (FOLD/CHECK/CALL/BET/RAISE) appropriately.

### TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **HU-1.4 5/5 stuck-RAISE = model-stuck pipeline-aligned**: per `project_v9_3way_ceiling.md` taxonomy, this is a corpus-quality signal, not a model defect. Lookalike consensus is RAISE:5/CALL:5 (5/10 each); owner adjudicated CALL on LK-04/05 (per PR #348). Model trained on the unreduced lookalike set sees 50/50 split → defaults to RAISE under class-weight-cap. Solver verification (HU-1.4 in queue) will resolve; if solver confirms CALL, retrain with corrected lookalike labels per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` recovery path.
2. **HU-6.5 4/5 stuck-FOLD = pipeline-canonical mismatch**: HU-6.5 has NO training lookalikes (structural absence in corpus per generation script). Model can't learn this anchor's variations. Solver verification (HU-6.5 in queue) will resolve; if solver confirms CALL, post-1.5-D.4 corpus expansion to include HU-6.5 lookalikes recommended.

Both stuck-wrong hands are in the solver-verification queue (per PR #362 §(c) + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`). Verification + retrain-if-needed is the recovery path; ship gate clears at 28/30 with these acknowledged misses.

## §4 — PokerBench parity (SECONDARY metric)

Per dispatch §"Fallback verification (NOT a gate)": PokerBench 88.1% parity reported as SECONDARY metric for provenance.

**NOT MEASURED in this PR.** PokerBench evaluation requires a separate eval harness (different from 30-hand HU reference). The architect-committed ship gate is the 30-hand reference (per design memo §4.6); PokerBench parity was framed as fallback. Builder defers PokerBench eval to a future post-ship measurement if orchestrator/architect requests it.

## §5 — Ship gate analysis

Per dispatch §"Ship gate (per §4.6; committed)": aggregate accuracy on 30-hand HU reference set ≥ 28/30 (≥ 93.3%).

- Canonical (median seed=3): **28/30 = 93.3%** ✓ AT GATE
- 5-seed mean: **28.2/30 = 94.0%** ✓ ABOVE GATE
- Best (seed=1): 29/30 = 96.7% ✓
- Worst (seeds 0/2/3/4): 28/30 = 93.3% ✓
- Spread: ALL 5 seeds at-or-above gate

**Gate: PASS** — canonical artifact at exactly the gate threshold; mean +0.7%; no seed below gate. Per dispatch §"5-seed full produces 26 or 27 of 30: STOP / REPORT" — this scenario does NOT trigger; all 5 seeds clear ≥28/30.

## §6 — Files in this PR

- `data/hu_reference_5seed_seed0_2026-05-10.jsonl` (per-hand seed-0 results)
- `data/hu_reference_5seed_seed1_2026-05-10.jsonl`
- `data/hu_reference_5seed_seed2_2026-05-10.jsonl`
- `data/hu_reference_5seed_seed3_2026-05-10.jsonl`
- `data/hu_reference_5seed_seed4_2026-05-10.jsonl`
- `review/comms/BUILDER_REPORT_PHASE15D4_FULL_2026-05-10.md` (this report)

Model artifacts (`models/gto_model_vNext_hu_59feat*.json`) gitignored per dispatch §"Does NOT git-add the new model file in 1.5-D.4 PR; force-add happens in 1.5-E per §4.6 amendment".

Trainer + corpus + assembly script unchanged from PR #370 (no diff).

## §7 — QC stream — what you audit (PR 2)

Per dispatch §"QC stream — what you audit (PR 2 5-seed full)" 7-item:

- [ ] 5-seed model artifacts present + per-seed scores documented
- [ ] 5-seed mean on 30-hand HU reference computed (28.2/30 ✓)
- [ ] Per-hand stay-wrong taxonomy applied (§3.4 format; under/over/collapse classification ✓)
- [ ] Ship-gate result correctly applied (PASS at 28/30 canonical; mean 28.2/30 ✓)
- [ ] PokerBench 88.1% parity reported as SECONDARY (not gate); deferred to post-ship measurement
- [ ] Diff scope strict (no production swap; no oracle_router.py:34 edit; no force-add of new model file)
- [ ] TC-X-DISPATCH-COMPLIANCE per dispatch (PR #364) + AMENDMENT (PR #366)

## §8 — What gates next

Per dispatch §"After 1.5-D.4 PASS → orchestrator authorizes 1.5-E":
- 1.5-E (router/coaching alignment + production swap): swap `oracle_router.py:34` filename pointer from `gto_model_v8_hu.json` to `gto_model_vNext_hu_59feat.json`; force-add new model file to git; coaching pipeline tests pass with NO test-suite changes per design memo §4.6 P7.
- After 1.5-E: Phase 1.5 SHIP boundary.
- Solver-verification queue (48 spots) HOLD-with-accepted-risk per owner direction; verify-and-retrain-if-needed is recovery (post-ship).

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `77bbefb` ✓ (PR #370 + #372 merged)
- Diff vs master: 6 files (5 per-seed reference eval JSONL + 1 builder report)
- Log vs master: 1 commit

## References

- 1.5-D.4 dispatch (PR #364): master `178fdaf`
- AMENDMENT (PR #366; Option B): master `3d5572b`
- PR 0 eval infra (PR #367): master `38b1149`
- PR 0 QC verdict (PR #369): master `3fcf7f1`
- PR 1 smoke (PR #370): master `e4a3650`
- PR 1 QC verdict (PR #372): master `77bbefb`
- Architect's design memo §4.5 + §4.6 + §4.7: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- v9_student trainer (reference adaptation source): `river-rats-core/train_model_v9_student.py`
- Stay-wrong taxonomy reference: `project_v9_3way_ceiling.md` memory + design memo §3.4
- Solver-verification queue (48 spots; HU-1.4 + HU-6.5 in queue): per `feedback_solver_verification_queue.md` + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`
- v8-HU baseline (PR0): 18/30 in `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_named_author_builds_not_polls.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `project_v9_3way_ceiling.md`

**Status: Phase 1.5-D.4 PR 2 (5-seed full) complete. SHIP GATE PASS at 28/30 (canonical median) / 28.2/30 (mean) on 30-hand HU reference. 2 stuck-wrong hands documented (HU-1.4 model-stuck pipeline-aligned, HU-6.5 pipeline-canonical mismatch — both in solver queue). Awaits QC + orchestrator merge → 1.5-E (router + production swap) authorized per dispatch §"After 1.5-D.4 PASS".**
