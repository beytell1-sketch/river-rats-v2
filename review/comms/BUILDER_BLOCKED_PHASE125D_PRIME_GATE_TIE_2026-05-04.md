---
date: 2026-05-04
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · Owner · ML-ARCHITECT (advisory) · GTO-EXPERT (review) · QC stream
re: Phase 12.5D' — BUILDER BLOCKED on dispatch gate threshold; median 31/40 ties 12.5D, model NOT promoted; gto-expert prediction structurally refuted
status: BUILDER BLOCKED — 12.5D' run complete; landed in dispatch's "31-32 owner-tie-gate" band
---

# Phase 12.5D' — BUILDER BLOCKED on owner-tie-gate threshold

Per dispatch (PR #130, master `1b95648`) §"Gate threshold":

> | Median seed solver-corrected | Outcome |
> |---|---|
> | ≥ 33 (clears v9-3way-v2.2 baseline) | PROMOTE |
> | 31-32 (no improvement or marginal) | STOP, do NOT promote, report — owner gate on "ship a tie? new direction?" |
> | < 31 (regression vs 12.5D) | STOP, report — hybrid weighting hurt; ml-architect Q3 reasoning needs revision |

12.5D' median solver-corrected = **31/40**. Same as 12.5D (also 31/40). Per-seed scores **identical** under reproducible runs: [31, 30, 30, 31, 31] both phases. Falls in the "31-32 owner-tie-gate" band. Model NOT promoted. Trainer report: `review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` (Section E quantifies the delta).

## Headline numbers (full diagnostic in trainer report)

| Quantity | 12.5D | 12.5D' | Δ |
|---|---|---|---|
| Per-seed solver-corrected | [31, 30, 30, 31, 31] | [31, 30, 30, 31, 31] | 0 across all seeds |
| Median solver-corrected | 31/40 | 31/40 | 0 |
| Chosen seed | 4 | 4 | — |
| Hybrid weighting active | NO (pure confidence) | YES (cap 3.0) | active per ml-architect Q3 |
| Held-out BET recall | 0.824 | **1.000** | **+0.176** |
| Held-out RAISE recall | 0.500 | **0.667** | **+0.167** |
| Held-out CHECK recall | 0.939 | 0.918 | -0.021 |
| Held-out FOLD recall | 1.000 | 1.000 | 0 |
| Held-out CALL recall | 0.833 | 0.833 | 0 |
| `nut_flush_block` importance | 0.0000 | 0.0000 | 0 (still never split on) |
| Pre-pad metadata-only | succeeded | succeeded | R-1 fallback NOT triggered |

## What hybrid weighting did and did not do

**It did fix held-out class collapse exactly as ml-architect Q3 predicted:**
- BET recall went from 0.824 → 1.000 (perfect on the held-out test fold)
- RAISE recall went from 0.500 → 0.667
- The corpus's passive-skew gradient bias is reversed under cap-3.0 hybrid weighting

**It did not move the gate score on the MW-11..MW-50 reference set.** Of the 7 gto-expert "shared cause" failures predicted to flip:

| hand | 12.5D student | 12.5D' student | corrected expert | outcome |
|---|---|---|---|---|
| MW-17 | FOLD | FOLD | CALL | STAYED-WRONG |
| MW-24 | CHECK | **BET** | BET | **FLIPPED-CORRECT** ✓ |
| MW-25 | CHECK | CHECK | BET | STAYED-WRONG |
| MW-40 | CHECK | CHECK | BET | STAYED-WRONG |
| MW-42 | CHECK | CHECK | BET | STAYED-WRONG |
| MW-45 | CALL | CALL | RAISE | STAYED-WRONG |
| MW-47 | CALL | CALL | RAISE | STAYED-WRONG |

**1 of 7 flipped, 6 stayed wrong.** gto-expert's prediction (7-of-7 shared-cause flip → student score 36-38/40) is empirically refuted at this cap level. MW-31 + MW-46 distinct-cause failures both stayed wrong as predicted.

## Why the held-out gain doesn't transfer to the reference set

The held-out test set draws from the same 494-hand corpus distribution as training; hybrid weighting fixes collapse on those in-distribution BET/RAISE situations. The MW-11..MW-50 reference set is structurally OUT of that distribution — the failure spots require GTO reasoning (e.g., MW-45 set on rainbow board, MW-47 nut-flush-draw with fold equity) that the corpus doesn't contain enough examples of. The model now has the calibration to predict BET/RAISE on familiar patterns, but the canonical reference-set failures aren't familiar patterns.

This converges with gto-expert Finding 3 H2 from 12.5D synthesis: **the corpus + 4 P1 blocker features do not deliver decisive signal on the canonical reference-set failure spots.** The migration's premise is empirically not supported on this evaluation set with this corpus, regardless of weighting scheme.

## Cross-reference: ml-architect Q3 reasoning audit

Per dispatch §"What you do NOT do" + §"Stop conditions": "Median seed solver-corrected < 31 → STOP, do NOT promote, **and** flag this as evidence ml-architect Q3 reasoning was wrong (hybrid weighting made things worse)."

12.5D' is 31, NOT < 31. Hybrid weighting did NOT make things worse — it FIXED held-out class collapse cleanly. The Q3 mechanism is sound at the loss-function level.

What's empirically refuted is the **gto-expert prediction** that fixing held-out class collapse would translate to 7-of-7 reference-set flips. Only 1 of 7 flipped. The transfer-from-held-out-to-reference-set assumption is the falsified link, not Q3's loss-function math.

## Three findings flagged for orchestrator + experts

### Finding 1 — Hybrid weighting works on held-out, doesn't transfer to reference set

The held-out class metrics show large positive gains under hybrid weighting (BET recall +0.176, RAISE recall +0.167). The reference set median is unchanged (31 → 31). Conclusion: held-out gates and reference-set gates measure different things on this corpus. Held-out passes; reference set fails. ml-architect's premise that fixing class collapse closes the reference-set gap is not borne out — but the held-out improvement is real and could matter for production inference distributions that more closely resemble the corpus.

### Finding 2 — Per-seed reproducibility limited by xgboost BLAS non-determinism

Repeated runs of the same 5-seed sweep produce per-seed scores that vary by ±1 hand on borderline argmax cases (e.g., MW-33 BET≈0.276 vs RAISE≈0.300, the kind of ±0.03 gap where multi-threaded reduction order flips the prediction). **Median is stable at 31** across all observed runs. Per-seed exact reproducibility requires `OMP_NUM_THREADS=1` at the trainer process level (the invariant test sets this for itself; production inference does not). Documented in trainer report Section A.

### Finding 3 — `nut_flush_block` importance still 0.0 under hybrid weighting

The most poker-theoretically significant blocker (direct nut-blocker for canonical RAISE/bluff spots like MW-47) has importance 0.0000 under both 12.5D and 12.5D'. Hybrid weighting did not change this. Other blockers shifted slightly: `flush_draw_block_pct` 0.0107 → 0.0040, `straight_draw_block_pct` 0.0071 → 0.0086, `nut_made_block_pct` 0.0056 → 0.0095. None cross the 1% drop threshold. The migration's "blocker features are load-bearing" premise remains empirically unsupported on this corpus.

## What the orchestrator + owner decide (per dispatch §"Gate threshold")

The dispatch lays out the next steps for each gate-band outcome. Median 31 → "31-32 owner-tie-gate." Plausible directions (no recommendation per `feedback_orchestrator_decides_not_recommends.md`):

- **Ship the tie**: promote v9-student at 31/40 (regression vs 33/40 baseline) on the strength of the held-out improvements. Held-out gain is real if production data resembles the corpus more than the reference set.
- **Cap retuning**: try cap=2.0 or 2.5 (ml-architect Q3 said the 3.0 cap was a starting point). Could over-correct or undershoot; informative either way.
- **Abandon migration**: gto-expert Finding 3 H2 + 12.5D' empirical refutation of the gto-expert flip prediction together suggest the 4 P1 blocker features do not deliver value on this reference set. The migration could be retired and the v9-3way-v2.2 baseline kept canonical.
- **Data-side fix**: add reference-set-style RAISE/bluff situations to the next labelling round (gto-expert Finding 3 H1, originally rejected). Larger workstream; would reframe the problem from "gate v9-student" to "rebuild the corpus."

## What the BLOCKED PR ships

Three deliverable files (NOT four — no model artifact per gate threshold) + 1 BLOCKED comm:

1. `river-rats-core/train_model_v9_student.py` — UPDATE (~5-line hybrid-weighting block + `_StudentInference` `feature_columns` kwarg + Section E in report writer + minor `12.5D` → `12.5D'` framing updates + fixed 12.5D wording-cleanup item from QC review)
2. `river-rats-core/tests/test_train_model_v9_student.py` — UPDATE (added `test_student_inference_mirror_invariant_on_baseline` per ml-architect Option α; 17 tests passing)
3. `review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` — NEW (Section A-D per blueprint + Section E delta)
4. `review/comms/BUILDER_BLOCKED_PHASE125D_PRIME_GATE_TIE_2026-05-04.md` — NEW (this comm)

## Process compliance

| Check | Status |
|---|---|
| Worked in isolated worktree (`/tmp/builder-12.5D-prime-wt`) | ✅ |
| Pre-flight on master HEAD `1b95648` (16/16 tests pass before changes) | ✅ no source-surface drift since 12.5D merge |
| Hybrid weighting computation = ml-architect Q3 verbatim (cap 3.0, multiplicative on confidence, applied to both train + eval_set weights) | ✅ |
| Invariant test added per ml-architect Option α (covers all 40 MW hands; tests 3 fields) | ✅ — passes with `OMP_NUM_THREADS=1` |
| 17 tests pass (16 existing + 1 new invariant) | ✅ |
| R-1 dry-run before 5-seed sweep | ✅ pre-pad metadata-only succeeded |
| 5-seed sweep ran to completion | ✅ |
| `git diff --stat` exactly 4 files (no model, no out-of-scope edits) | ✅ |
| Did NOT touch `gto_model.FEATURE_COLUMNS` or any other existing source surface | ✅ |
| Did NOT change cap from 3.0 to anything else | ✅ |
| Did NOT add per-class boost beyond formula given | ✅ |
| Did NOT extend `reference_evaluator.evaluate_variants` | ✅ |
| Did NOT auto-promote model on 31/40 tie | ✅ stop condition fired correctly |
| Did NOT improvise a third pre-pad realization | ✅ R-1 fallback NOT needed |

## References

- 12.5D' dispatch: `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md` (PR #130, master `1b95648`)
- 12.5D synthesis: `review/comms/MAIN_TERMINAL_PHASE125D_SYNTHESIS_OWNER_GATE_2026-05-04.md` (PR #128, master `d6dd36d`)
- 12.5D BLOCKED baseline (now on master): trainer + tests + report + BLOCKED comm (PR #126, master `d7d2cdd`)
- Approved blueprint: PR #122 (master `1e4e47e`)
- ml-architect spec: PR #110 (master `291af80`); §11 R-2 RAISE-collapse risk + Q3 hybrid weighting recommendation
- Solver corrections memory: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- BLOCKED branch: `programmer/phase125d-prime-hybrid-weighting-2026-05-04`

**Status: BUILDER BLOCKED at owner-tie-gate (median 31/40). Hybrid weighting fixed held-out class collapse cleanly but did not transfer to reference-set gate. gto-expert flip prediction empirically refuted (1/7 vs predicted 7/7). 3-deliverable-file PR open + this BLOCKED comm. Awaiting orchestrator decision per dispatch §"After 12.5D' PR opens".**
