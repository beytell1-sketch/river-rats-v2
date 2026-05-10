---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (builder; architect-hat for trainer adaptation)
re: Phase 1.5-D.4 — HU model retrain on 59-surface, from-scratch, 5-seed (1-seed smoke + full 5-seed) per design memo §4.5 + §4.6
status: DISPATCH — fire now
---

# Phase 1.5-D.4 — HU model retrain dispatch

Phase 1.5-D.3 complete: pilot_50_v2 (50 HU-1 hands; all owner-arbs adjudicated PR #349) + full_HU2_HU6 (696 HU-2..HU-6 hands; all 44 owner-arbs adjudicated PR #363) = **746 HU-labelled situations** (architect committed ~750). Phase 1.5-D.4 (HU model retrain on 59-surface, from-scratch) AUTHORIZED to proceed.

Solver-verification queue: 48 spots (4 prior + 44 new); HOLD-with-accepted-risk per owner direction (2026-05-10 21:13 SAST: "we can verify with solver later and retrain if necessary"). Solver-verify-and-retrain-delta is the recovery path; not a pre-train gate.

## Scope (per design memo §4.5)

### Trainer

**Build NEW trainer:** `river-rats-core/train_model_vNext_hu.py` (HU-specific variant of `river-rats-core/train_model_v9_student.py`).

Differences from 3-way student per §4.5:
- **Surface size assertion 59** (not 61)
- **No `num_opponents`-conditioned features** need attention; HU has constant `num_opponents=1`; 59-surface includes `num_opponents` as a feature → model learns it as constant on HU corpus (no surgery needed)
- **From-scratch** (no `xgb_model=` warm-start arg)
- **Hyperparameters identical to 3-way student** (justified: same model family; same regularization regime suitable for ~750-corpus 5-class XGBoost)
- **5-seed standard run**

Provenance docstring required per §4.5 amendment: every model-producing script lives in `river-rats-core/` with a docstring linking its commit → model artifact (per `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1). Inline `python3 <<'EOF'` heredoc training is PROHIBITED.

### Corpus assembly

Combine HU labelled situations into a single corpus file:
- **Inputs:**
  - `data/hu_corpus/pilot_50_v2/consensus.jsonl` (50 entries; HU-1 axis)
  - `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696 entries; HU-2..HU-6 axes)
  - **Total:** 746 HU-labelled situations
- **Output:** `data/corpus_hu_746_2026-05-10.jsonl` (filename pattern per design memo §4.4: `data/corpus_hu_<size>_<date>.jsonl`)

Combine consensus_action + spot context for each row; convert to feature-extraction-input format compatible with the trainer. Pipeline analog: `scripts/assemble_corpus_v9_3way.py` (or equivalent existing script). Builder-architect picks tooling.

### Pilot+full split (per §4.7 + `feedback_pilot_first_for_long_jobs.md`)

**1.5-D.4 pilot = 1-seed smoke run.** Run trainer once with seed=0 (or `seed=42` per project convention); produce `models/gto_model_vNext_hu_59feat_seed{N}_smoke.json`.

**Smoke gate:** smoke score on 30-hand HU reference set must NOT be > 5 pts below v8-HU baseline. Specific threshold:
- v8-HU-38 reference: 88.1% PokerBench (cross-evaluation; not directly applicable)
- HU 30-hand reference equivalent: TBD by builder during smoke (compare smoke 30-hand score vs v8-HU-38 evaluated on same 30 hands; if smoke score > 5 pts below v8-HU 30-hand score → HALT)
- Per design memo §4.7 + dispatch §"HALT" below

If smoke clears: proceed to full 5-seed run.

**1.5-D.4 full = 5-seed full run.** Run trainer 5 times with seeds {0,1,2,3,4} (or project convention); aggregate produce `models/gto_model_vNext_hu_59feat.json` (canonical 5-seed model artifact).

### Ship gate (per §4.6; committed)

**Architect-committed ship gate: aggregate accuracy on 30-hand HU reference set ≥ 28/30 (≥ 93.3%).**

- 28/30 chosen specifically: lets one CLOSE hand miss per typical axis without tripping; 27/30 (-3) would allow class-collapse pattern to slip through
- This threshold is committed; if 1.5-D.4 produces 26 or 27 of 30, that's STOP/REPORT (not auto-promote)

**Per-hand stay-wrong tracking required** (per §4.5):
- Builder report MUST include §3.4 failure-direction format (under-aggressive / over-aggressive / class-collapse)
- Per-hand stay-wrong taxonomy across 5 seeds (analog to `project_v9_3way_ceiling.md` taxonomy: pipeline-canonical mismatch vs model-stuck pipeline-aligned)

**Fallback verification (NOT a gate):** PokerBench 88.1% parity reported as SECONDARY metric for provenance.

### STOP / HALT conditions (per CLAUDE.md §5 + design memo §"HALT")

- **Smoke score > 5 pts below v8-HU on 30-hand reference:** STOP / REPORT. Do NOT fire 5-seed full. Off-ramps documented in design memo §"1.5-D.4 HALT" (expand corpus 750 → 1500; revert HU to v8-HU-38 + ship 3-way-only Phase 1.5; re-investigate HU surface choice).
- **5-seed full produces 26 or 27 of 30:** STOP / REPORT. Do NOT auto-promote.
- **Trainer fails (XGBoost crash, surface assertion mismatch, etc.):** STOP / REPORT. Do NOT improvise.
- **Corpus assembly produces unexpected size (≠ 746):** STOP / REPORT. Investigate before training.
- **Per-hand stay-wrong taxonomy reveals class-collapse:** STOP / REPORT. Class-collapse means model defaults to majority class; corpus or trainer issue.

### Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT modify pilot_50_v2/ or full_HU2_HU6/ corpus inputs (those are merged + locked)
- ❌ Does NOT use solver output as training label (solver verification is post-train per §(c) above)
- ❌ Does NOT swap production HU oracle (`oracle_router.py:34`); architect commits this happens in **1.5-E** sub-phase, NOT 1.5-D.4 (per §4.6 amendment)
- ❌ Does NOT git-add the new model file in 1.5-D.4 PR; force-add happens in 1.5-E per §4.6 amendment (avoid recreating v8-HU-38 git-tracking gap)
- ❌ Does NOT use warm-start (architect-committed from-scratch per §4.5)
- ❌ Does NOT run inline heredoc training (provenance docstring requirement per §4.5)
- ❌ Does NOT improvise on STOP/HALT conditions

## Builder deliverables

**PR 1 (smoke):**
- `river-rats-core/train_model_vNext_hu.py` (NEW; provenance docstring; from-scratch HU trainer)
- `data/corpus_hu_746_2026-05-10.jsonl` (assembled corpus)
- `models/gto_model_vNext_hu_59feat_seed{N}_smoke.json` (1-seed smoke model; in `.gitignore`-respecting location per project convention)
- `review/comms/BUILDER_REPORT_PHASE15D4_SMOKE_2026-05-10.md`:
  - Trainer adaptation summary (diffs vs train_model_v9_student.py)
  - Corpus assembly summary (746 entries verified)
  - Smoke score on 30-hand HU reference vs v8-HU-38 baseline on same 30 hands
  - Smoke gate result (PASS / HALT)
  - If HALT: STOP per §"HALT" off-ramps; do NOT fire 5-seed
  - If PASS: builder fires 5-seed full in PR 2

**PR 2 (5-seed full; only if smoke clears):**
- `models/gto_model_vNext_hu_59feat.json` (canonical 5-seed model artifact)
- `models/gto_model_vNext_hu_59feat_seed{0..4}.json` (per-seed artifacts)
- `review/comms/BUILDER_REPORT_PHASE15D4_FULL_2026-05-10.md`:
  - 5-seed mean + per-seed scores on 30-hand HU reference
  - Per-hand stay-wrong taxonomy (§3.4 format) across 5 seeds
  - Ship-gate result (PASS ≥ 28/30, STOP/REPORT 26-27/30, HALT < 26/30)
  - PokerBench 88.1% parity (SECONDARY metric)
  - If PASS: orchestrator authorizes 1.5-E (router/coaching alignment + production swap per §4.6 ship-action)

QC stream audits each PR per `feedback_qc_required_before_approval.md` (1.5-D.4 produces production-class model artifact — milestone-class).

## QC stream — what you audit

**For PR 1 (smoke):** ~15-20 min audit
1. Trainer matches §4.5 spec (surface 59, from-scratch, hyperparameters identical to v9_student, 5-seed-ready)
2. Corpus 746 entries (50 from pilot_50_v2 + 696 from full_HU2_HU6); per-row schema valid
3. Provenance docstring present in trainer
4. Smoke model artifact produced; size + format valid
5. Smoke score on 30-hand HU reference computed; v8-HU-38 baseline computed on same 30 hands; delta documented
6. Smoke gate result correctly applied (PASS / HALT decision matches dispatch §"HALT")
7. Diff scope strict (no production swap; no router edits; no model file force-added in this PR)
8. TC-X-DISPATCH-COMPLIANCE per this comm

**For PR 2 (5-seed full; only if smoke PASS):** ~20-25 min audit
1. 5-seed model artifacts present + per-seed scores documented
2. 5-seed mean on 30-hand HU reference computed
3. Per-hand stay-wrong taxonomy applied (§3.4 format; under/over/collapse classification)
4. Ship-gate result correctly applied (PASS ≥ 28/30, STOP/REPORT 26-27/30, HALT < 26/30)
5. PokerBench 88.1% parity reported as SECONDARY (not gate)
6. Diff scope strict (no production swap; no `oracle_router.py:34` edit; no force-add of new model file)
7. TC-X-DISPATCH-COMPLIANCE per this comm

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

## Owner — informational

- 1.5-D.4 fires per design memo §4.5 + §4.6; smoke + 5-seed full split per `feedback_pilot_first_for_long_jobs.md`
- Ship gate ≥28/30 committed per `feedback_quality_default_no_ask.md`
- Solver-verification queue (48 spots) HOLD-with-accepted-risk per your direction; verify-and-retrain-if-needed is recovery (not pre-train gate)
- After 1.5-D.4 PASS → orchestrator authorizes 1.5-E (router/coaching alignment + production swap; oracle_router.py:34 filename pointer change + force-add new model file)
- After 1.5-E → Phase 1.5 SHIP boundary (full Phase 1.5 milestone)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a3fb9f3` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 44 owner-arbs adjudication dispatch: master `ca1f7b0` (PR #362)
- 44 owner-arbs data-layer fix merged: master `a3fb9f3` (PR #363)
- 1.5-D.3 FULL labelling SCALE merged: master `a3fb9f3` (predecessors PR #359 + PR #361 QC PASS · 0/0/0)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict: master `b790524` (PR #346)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- Architect's design memo §4.4 (corpus) + §4.5 (retrain) + §4.6 (ship-gate) + §4.7 (sub-phase decomposition): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Trainer reference: `river-rats-core/train_model_v9_student.py`
- Stay-wrong taxonomy reference: `project_v9_3way_ceiling.md` memory + design memo §3.4
- Production-runtime-anchor (Path β) per `oracle_router.py:34` reference: design memo §4.6 amendment
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `project_v9_3way_ceiling.md`

**Status: Phase 1.5-D.4 fires LEAD-PROGRAMMER. Smoke first (1-seed); STOP/HALT on smoke <5pts-below-v8-HU; 5-seed full on smoke PASS; ship gate ≥28/30 on 30-hand HU reference. Per-hand stay-wrong taxonomy required. Solver-verification queue (48 spots) HOLD-with-accepted-risk; verify-and-retrain-if-needed is recovery. After PASS → 1.5-E (router/coaching alignment + production swap).**
