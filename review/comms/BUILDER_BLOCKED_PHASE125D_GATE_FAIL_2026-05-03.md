---
date: 2026-05-03
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5D — BUILDER BLOCKED on dispatch stop condition #3 (gate failure); model NOT promoted
status: BUILDER BLOCKED — 5-seed run complete, gate FAILED, awaiting orchestrator decision
---

# Phase 12.5D — BUILDER BLOCKED on gate failure

Per dispatch directive (PR #125, master `e3c0dfc`) §"Stop conditions":

> 5-seed training emits any seed that fails reference-evaluator gate
> (`gate_24_reference_evaluation` returns < ml-architect §10 threshold for
> v9-3way-v2.2 baseline) → STOP, do NOT promote, report

Median solver-corrected litmus on the chosen seed (seed 4) is **31/40**; the v9-3way-v2.2 baseline scored **33/40** in the same run. The median student is short by 2 hands. **Model NOT promoted** to `river-rats-core/models/gto_model_v9_student.json`. Trainer report written to `review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-03.md`.

## Headline numbers (full report has the rest)

| Quantity | Value |
|---|---|
| Joined corpus rows | 494 / 494 (correct join key required schema discovery — see below) |
| Held-out accuracy (5-seed mean ± std) | 0.903 ± 0.014 |
| Held-out weighted accuracy (5-seed mean ± std) | 0.921 ± 0.009 |
| Pre-pad mechanism | metadata-only `num_feature` JSON bump succeeded; R-1 fallback NOT triggered |
| Per-seed solver-corrected litmus | 31, 30, 30, 31, 31 → mean 30.6/40 (std 0.49) |
| Chosen seed (median solver-corrected) | seed 4 — score 31/40 |
| v9-3way-v2.2 baseline (same run, same overlay) | 33/40 |
| Gate verdict | FAIL (31 < 33) |
| v8-38feat baseline | NOT EVALUATED — `gto_model_v8_38feat.json` is not git-tracked at master HEAD (#PSH-01); canonicality guard dropped it from litmus |

## Three findings flagged for review

### 1. Schema discoveries (Path Y boundary surprises)

a. **Join key**: blueprint §6 + ml-architect §12 cited `corpus.source_situation_id == labels.ref_id`, verified on row 1. That holds only for the first 100 rows. Cohort 2 (rows 100-493) uses `situation_id` instead, and labels.ref_id is heterogeneous (`d####_POS_street` vs `PILOT_###`). Empirical join cardinality at HEAD `e3c0dfc`: source_situation_id ∩ ref_id = 100/494; pilot_hand_id ∩ pilot_hand_id = **494/494**. Trainer joins on `pilot_hand_id` to honor the spec INTENT (494-hand training).

b. **Inference boundary**: `reference_evaluator.evaluate_variants` builds inference arrays via `gto_model.GtoOracle.features_from_dict` which iterates `gto_model.FEATURE_COLUMNS` (length 55). Student model expects 59 features. Path Y forbids extending `gto_model.FEATURE_COLUMNS`. Trainer module owns a `_StudentInference` + `_evaluate_student_one_hand` 59-feature inference helper that mirrors `reference_evaluator._evaluate_one_hand` line-for-line. Baselines (38/45) continue to flow through `evaluate_variants` since gto_model's 55-feature pipeline accommodates them via the predict-time slice.

Both surfaced empirically during 12.5D execution; both addressed in-module per Path Y discipline (zero edits to existing surfaces). Report Section A "Schema discoveries" documents both.

### 2. RAISE class collapsed (ml-architect R-2 confirmed)

Chosen seed (seed 4) per-class held-out test metrics:

| class | precision | recall | f1 | support |
|---|---|---|---|---|
| FOLD | 0.938 | 1.000 | 0.968 | 15 |
| CHECK | 0.939 | 0.939 | 0.939 | 49 |
| CALL | 0.769 | 0.833 | 0.800 | 12 |
| BET | 0.824 | 0.824 | 0.824 | 17 |
| **RAISE** | **0.750** | **0.500** | **0.600** | **6** |

Reference-set student RAISE count: **2** (vs the chosen seed's expected RAISE distribution from ~6-9 RAISE situations including MW-45 and MW-47 corrected). Per ml-architect R-2, this is the predicted failure mode under pure confidence weighting on 29 RAISE training rows. The per-hand failure list (Section B) shows MW-45 student=CALL (expert=RAISE) and MW-47 student=CALL (corrected expert=RAISE) — the canonical RAISE-bias hands both fail.

### 3. Three of four v2.4 P1 blockers below the 1% drop threshold

The migration's load-bearing features did not earn importance during continued training:

| feature | importance | on PROCESS_GUIDE §2.3 drop list? |
|---|---|---|
| `nut_flush_block` | 0.0000 | YES — flagged |
| `flush_draw_block_pct` | 0.0107 | no (just above 1%) |
| `straight_draw_block_pct` | 0.0071 | YES — flagged |
| `nut_made_block_pct` | 0.0056 | YES — flagged |

Per blueprint §6 — "the entire migration's value rides on these features being load-bearing." Three of four are not. `nut_flush_block` (the most poker-theoretically significant — direct nut-blocker for the canonical RAISE/bluff spot) is at 0.0 importance; the model literally never split on it.

Likely cause hypothesis (gto-expert review territory): the 494-hand corpus has too few situations where blocker effects discriminate between expert actions for the booster's importance gain to register them. Continued training adds only ~140-435 trees on top of the 129-tree warm-start anchor; the anchor never saw blockers, and the new training rounds preferentially split on already-strong features (equity_margin, raw_equity, facing_bet — top 5).

## What the orchestrator decides

The dispatch directive says: "5-seed training emits any seed that fails reference-evaluator gate ... → STOP, do NOT promote, report." Done. The decision is now what to do about the gate failure. Several plausible directions, listed without recommendation per `feedback_orchestrator_decides_not_recommends.md`:

- **A**: accept the gate failure as data; do NOT ship v9-student; close 12.5D as "ran cleanly, model fell short, design surface needs revision." Possible 12.5+1 work: ml-architect re-design with hyperparameter changes (RAISE-class oversampling? curriculum 45→59 instead of single-shot pre-pad?) or data-level fix (more RAISE situations in next labelling round per ml-architect §11 R-2 mitigation B).
- **B**: re-evaluate the gate threshold. v9-3way-v2.2's 33/40 was scored on its own training distribution; v9-student is being judged out-of-distribution on the MW-11..MW-50 set without solver-aligned labels. Maybe 31/40 is acceptable at 12.5F owner ship gate.
- **C**: schedule a follow-up 12.5D' run with a different RAISE handling (hybrid weighting per ml-architect §11 R-2 option C — requires a new ml-architect design pass).
- **D**: defer — investigate RAISE failure at gto-expert review first; come back to dispatch decisions after the diagnosis lands.

These are observations only; orchestrator chooses.

## What the BLOCKED PR ships

Three files (NOT four — no model artifact per stop condition):
1. `river-rats-core/train_model_v9_student.py` (full implementation)
2. `river-rats-core/tests/test_train_model_v9_student.py` (16 tests passing)
3. `review/comms/PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-03.md` (Section A/B/C/D per dispatch)

Plus this BUILDER_BLOCKED comm, separately.

The trainer is fully reproducible: re-running yields identical median 31/40. R-1 dry-run mode (`--no-write-model`) is functional for ml-architect/QC inspection of the pre-pad trace without re-running the full 5-seed sweep.

## Process compliance

| Check | Status |
|---|---|
| Worked in isolated worktree (`/tmp/builder-12.5D-wt`) | ✅ |
| Pre-flight on §6 citations at master HEAD `e3c0dfc` (vs blueprint pin `1fb0dea`) | ✅ no source-surface drift |
| Test suite (16 tests) passes | ✅ |
| R-1 dry-run before 5-seed sweep | ✅ metadata-only pre-pad succeeded |
| 5-seed sweep ran to completion | ✅ |
| `git diff --stat` exactly the 3 files (no model, no out-of-scope edits) | ✅ |
| Did NOT extend `reference_evaluator.evaluate_variants` | ✅ in-module `_StudentInference` instead |
| Did NOT mutate `BATCH2_8_HAND_DESIGNS.md` | ✅ solver overlay is in-module |
| Did NOT add stub trees to warm-start anchor | ✅ metadata-only realization per blueprint §4.1 |
| Did NOT auto-promote model | ✅ stop condition #3 fired; model NOT written |
| STOP'd on first gate-fail signal; did not improvise hyperparameter changes | ✅ |

## References

- Dispatch directive: `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` (PR #125, master `e3c0dfc`)
- Approved blueprint: `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` (PR #122, master `1e4e47e`)
- ml-architect spec: PR #110 (master `291af80`) — §11 R-2 RAISE-collapse risk
- Solver corrections memory: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- BLOCKED branch: `programmer/phase125d-trainer-impl-2026-05-03`

**Status: BUILDER BLOCKED on dispatch stop condition #3 (gate FAIL). 3-file PR open; awaiting orchestrator decision per the four directions above (or any other).**
