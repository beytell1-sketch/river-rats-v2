---
date: 2026-05-10
from: LEAD-PROGRAMMER (builder; architect-hat for trainer adaptation)
to: Main terminal (orchestrator) · QC stream · Owner (informational)
re: Phase 1.5-D.4 PR 1 (smoke) — 1-seed vNext-HU-59 trainer + 746-corpus + smoke score 27/30 (PASS); ready for 5-seed full
status: DELIVERY — smoke PASS; orchestrator authorizes PR 2 (5-seed full)
---

# Phase 1.5-D.4 PR 1 — Smoke delivery

## Summary

Per 1.5-D.4 dispatch (PR #364) §"Builder deliverables PR 1 (smoke)" + AMENDMENT (PR #366) gating on PR 0 + QC PASS:

- **Trainer**: `river-rats-core/train_model_vNext_hu.py` (305 lines; from-scratch HU adaptation of `train_model_v9_student.py`)
- **Corpus**: `data/corpus_hu_746_2026-05-10.jsonl` (746 rows; 50 from pilot_50_v2 + 696 from full_HU2_HU6)
- **Assembly script**: `scripts/assemble_hu_corpus_746.py`
- **Smoke model**: `models/gto_model_vNext_hu_59feat_seed42_smoke.json` (5-class XGBoost; 59 features; seed=42)
- **Smoke training report**: `models/gto_model_vNext_hu_59feat_seed42_smoke_report.json`
- **Smoke 30-hand HU reference eval**: `data/hu_reference_smoke_seed42_2026-05-10.jsonl`
- **This report**

**SMOKE GATE: PASS** — score 27/30 (90.0%) vs v8-HU baseline 18/30 (60.0%). Delta = **+9 absolute points above baseline** (gate was "≤5 pts below" → ≥13/30 floor; smoke at 27 is +14 above floor).

## §1 — Trainer adaptation

`river-rats-core/train_model_vNext_hu.py` (305 lines, NEW). Adapted from `train_model_v9_student.py` with HU-specific deviations per dispatch §"Trainer":

| Aspect | v9_student (3-way warm-start) | vNext-HU (this trainer) |
|--------|-------------------------------|-------------------------|
| Surface | 59 features | 59 features (identical) |
| Classes | 5 (FOLD/CHECK/CALL/BET/RAISE) | 5 (identical) |
| Warm-start | `xgb_model=padded_v9_3way_v2.2` | NONE (from-scratch per dispatch) |
| Hyperparameters | n_estimators=800, max_depth=5, lr=0.05, ESR=50, etc. | IDENTICAL |
| Confidence weight | `consensus_confidence` (1.0/0.8/0.6/0.4) | Derived from `consensus_kind`: 5-of-5=1.0, 4-of-5=0.8, 3-2-tier-up-agree=0.6, owner-arb-3-2/2-2-1=0.4 |
| Class weight cap | 3.0 | 3.0 (identical) |
| Train/test split | 0.2 stratified | 0.2 stratified (identical) |
| Corpus join key | pilot_hand_id | spot_id |

Provenance docstring present (per `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1 amendment).

## §2 — Corpus assembly

`scripts/assemble_hu_corpus_746.py` + `data/corpus_hu_746_2026-05-10.jsonl`.

**Inputs:**
- `data/hu_corpus/pilot_50_v2/{situations,consensus}.jsonl` (50 HU-1 lookalikes)
- `data/hu_corpus/full_HU2_HU6/{situations,consensus}.jsonl` (696 HU-2..HU-6 lookalikes)

**Process:**
- Merge by spot_id (746 = 746 ∩ 746)
- Build hand_dict (HU `num_opponents=1`; empty `_action_history`)
- Extract feat_dict via `feature_extractor.extract_all_features` (59 features per row)
- Filter feat_dict to 59 FEATURE_COLUMNS; assert all numeric

**Output schema:** `{spot_id, anchor_id, feat_dict (59 keys), consensus_action, consensus_kind, confidence, owner_arb}`

**Action distribution (746 samples):**

| Action | Count | % |
|--------|-------|---|
| BET | 333 | 44.6% |
| CALL | 175 | 23.5% |
| CHECK | 103 | 13.8% |
| FOLD | 100 | 13.4% |
| RAISE | 35 | 4.7% |

RAISE is rare (~5%); class-weight-cap 3.0 handles this per v9_student precedent.

## §3 — Smoke training (1-seed)

`models/gto_model_vNext_hu_59feat_seed42_smoke.json`.

- Seed: 42 (project convention smoke seed)
- Train/test split: 80/20 stratified by action (596 train / 150 test)
- From-scratch (no warm-start)
- Boosted rounds: 530 (early-stopped at ESR=50 from n_estimators=800 nominal)

**Held-out metrics:**
- Accuracy: 90.0%
- Weighted accuracy: 92.8%

## §4 — 30-hand HU reference eval

`data/hu_reference_smoke_seed42_2026-05-10.jsonl`.

**Score: 27/30 (90.0%)**

### Per-axis breakdown (vs v8-HU baseline)

| Axis | Smoke (vNext-HU) | v8-HU baseline | Delta |
|------|------------------|----------------|-------|
| HU-1 | 4/5 (80%) | 3/5 (60%) | +1 |
| HU-2 | 5/5 (100%) | 1/5 (20%) | +4 |
| HU-3 | 4/5 (80%) | 1/5 (20%) | +3 |
| HU-4 | 5/5 (100%) | 4/5 (80%) | +1 |
| HU-5 | 5/5 (100%) | 4/5 (80%) | +1 |
| HU-6 | 4/5 (80%) | 5/5 (100%) | -1 |
| **Total** | **27/30 (90%)** | **18/30 (60%)** | **+9** |

**Massive improvement on draws (HU-2 +4) and air/bluffs (HU-3 +3)** — exactly the under-aggression failure mode noted in PR0 v8-HU baseline analysis.

### Misses (3/30)

| Spot | Marker | Street | Expected | Predicted | Confidence | Notes |
|------|--------|--------|----------|-----------|------------|-------|
| HU-1.4 | CLOSE | turn | CALL | RAISE | 0.95 | Over-aggressive on set vs IP probe; same direction as v8-HU miss |
| HU-3.3 | CLOSE | turn | BET | CHECK | 0.50 | Borderline (low confidence 0.50); model split close to BET/CHECK; expected BET (delayed-stab on overcards) |
| HU-6.5 | CLOSE | river | CALL | FOLD | 0.59 | Folds nut straight facing 150% overbet; model didn't capture nut-confidence on this anchor (HU-6.5 has no lookalikes in training corpus) |

**Failure-direction taxonomy (informational):**
- 1 over-aggressive (HU-1.4 RAISE vs CALL)
- 1 under-aggressive (HU-3.3 CHECK vs BET; low conf 0.50 = borderline)
- 1 over-folding (HU-6.5 FOLD vs CALL)

No class-collapse pattern (each miss is a distinct direction). Same axes hit by both v8-HU and vNext-HU on HU-1.4 + HU-3.3, suggesting these are genuinely difficult close spots; HU-6.5 is unique to vNext-HU (no training lookalikes for this anchor).

### HU-6.5 specific note

HU-6.5 is the ONLY 30-hand reference anchor with **NO lookalikes in the training corpus** (excluded from generation per `scripts/hu_anchors_axes_2_6.py` because pre-adjudicated). The vNext-HU model has never seen this exact anchor's variations during training. Its FOLD prediction here is unsurprising — without training signal on this specific anchor, the model defaults to broad bluff-catch caution. v8-HU coincidentally got this one CORRECT (CALL) but its 18/30 overall is much weaker. For 5-seed full + ship gate consideration: HU-6.5 may remain a miss unless additional adjudication or solver-verification surfaces.

## §5 — Smoke gate analysis

Per dispatch §"Smoke gate": "smoke score on 30-hand HU reference set must NOT be > 5 pts below v8-HU baseline".

- v8-HU baseline: 18/30
- 5pts-below threshold: ≥ 13/30
- Smoke score: **27/30**
- Delta vs floor: **+14 points above floor** (or equivalently +9 above v8-HU baseline)

**Gate: PASS** with massive margin. Recommend orchestrator authorizes PR 2 (5-seed full) per original dispatch §"If smoke clears: proceed to full 5-seed run".

## §6 — Ship-gate trajectory (informational)

Per dispatch §"Ship gate": ≥ 28/30 (≥ 93.3%).

- Smoke (1-seed) at 27/30 (90.0%) is **1 hand below ship gate**.
- 5-seed full will produce 5 candidate models; canonical artifact is median seed.
- Probability of 5-seed median ≥ 28/30 depends on seed variance:
  - If all 5 seeds at 27±1, median may be 26-28 (gate borderline)
  - If smoke seed=42 is representative, expect median similar to smoke ~27/30 (1 below gate)
- **Risk acknowledgment**: ship gate is achievable but NOT guaranteed at first 5-seed run. Per dispatch §"5-seed full produces 26 or 27 of 30: STOP / REPORT. Do NOT auto-promote." If 5-seed median = 26 or 27, builder STOPs + reports.

The 3 smoke-miss hands (HU-1.4, HU-3.3, HU-6.5) are all CLOSE-marker hands with documented poker difficulty; expecting all 3 to flip with seed variance alone is optimistic. Per `feedback_quality_default_no_ask.md`: surface this honestly so orchestrator can pre-plan off-ramps.

## §7 — TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **Single-file corpus (vs v9_student's 2-file corpus+labels split)**: builder-architect choice for cleaner HU pipeline. Trainer reads `--corpus` only; consensus_action + confidence are inline per-row. Acceptable simplification; no functional risk.
2. **Confidence derivation from consensus_kind (vs explicit consensus_confidence)**: consensus.jsonl rows don't have `consensus_confidence` field; derived from `consensus_kind` per dispatch §"§(c) Confidence weighting" implicit (mapped 5-of-5=1.0/4-of-5=0.8/3-2-tier-up-agree=0.6/owner-arb=0.4). Acceptable; documented in trainer module + this report.
3. **HU-6.5 has no training lookalikes**: structural absence in corpus (HU-6.5 excluded from generation per `scripts/hu_anchors_axes_2_6.py` line 4 comment). Model can't learn from variations. Smoke miss on HU-6.5 expected; flagged for orchestrator (may need post-1.5-D.4 corpus expansion if persistent).

## §8 — QC stream — what you audit (PR 1)

Per dispatch §"QC stream — what you audit (PR 1 smoke)" 8-item:

- [ ] Trainer matches §4.5 spec (surface 59, from-scratch, hyperparameters identical to v9_student, 5-seed-ready)
- [ ] Corpus 746 entries (50 from pilot_50_v2 + 696 from full_HU2_HU6); per-row schema valid
- [ ] Provenance docstring present in trainer
- [ ] Smoke model artifact produced; size + format valid
- [ ] Smoke score on 30-hand HU reference 27/30 documented; v8-HU-38 baseline 18/30 on same 30 hands; delta +9 documented
- [ ] Smoke gate result correctly applied: PASS (27/30 vs ≥13/30 floor)
- [ ] Diff scope strict: NEW trainer + NEW corpus + NEW assembly script + NEW smoke artifact + NEW report; NO production swap; NO router edits; NO model file force-added
- [ ] TC-X-DISPATCH-COMPLIANCE per AMENDMENT (PR #366) + original dispatch (PR #364)

## Files in this PR

- `river-rats-core/train_model_vNext_hu.py` (305 lines; NEW)
- `scripts/assemble_hu_corpus_746.py` (172 lines; NEW)
- `data/corpus_hu_746_2026-05-10.jsonl` (746 rows; NEW)
- `models/gto_model_vNext_hu_59feat_seed42_smoke.json` (XGBoost JSON model; NEW)
- `models/gto_model_vNext_hu_59feat_seed42_smoke_report.json` (training metrics; NEW)
- `data/hu_reference_smoke_seed42_2026-05-10.jsonl` (30 per-hand smoke eval results; NEW)
- `review/comms/BUILDER_REPORT_PHASE15D4_SMOKE_2026-05-10.md` (this report)

## What gates next

Per dispatch §"If PASS: builder fires 5-seed full in PR 2":
- Orchestrator merges PR 1 + QC PASS → builder fires PR 2 (5-seed full)
- 5 seeds {0, 1, 2, 3, 4}; median selection for canonical artifact
- Per-hand stay-wrong taxonomy across 5 seeds (analog to `project_v9_3way_ceiling.md`)
- Ship gate ≥ 28/30 evaluated on canonical median artifact

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3fcf7f1` ✓ (PR #367 + #369 merged)
- Diff vs master: 7 files (4 NEW data/model files + 1 trainer + 1 assembly script + 1 report)
- Log vs master: 1 commit

## References

- AMENDMENT (PR #366; Option B): master `3d5572b`
- 1.5-D.4 dispatch (PR #364): master `178fdaf`
- PR 0 eval infra (PR #367): master `38b1149`
- PR 0 QC verdict (PR #369): master `3fcf7f1`
- Architect's design memo §4.5 + §4.6: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- v9_student trainer (reference adaptation source): `river-rats-core/train_model_v9_student.py`
- HU eval infrastructure (PR0): `river-rats-core/hu_reference_evaluator.py` + `design/hu_reference_set/hu_30_hand_reference.jsonl`
- v8-HU baseline (PR0): `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (18/30)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_named_author_builds_not_polls.md`, `feedback_orchestrator_decides_not_recommends.md`, `project_v9_3way_ceiling.md`

**Status: Phase 1.5-D.4 PR 1 (smoke) complete. Smoke PASS at 27/30 (+9 above v8-HU baseline; +14 above 13/30 floor). 1 below ship gate ≥28/30 — 5-seed full may close gap or surface need for off-ramp. Awaits QC + orchestrator merge → PR 2 (5-seed full) authorized per dispatch §"If PASS".**
