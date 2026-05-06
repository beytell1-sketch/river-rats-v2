---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #261 — Phase 12.5K-A Lever A more-seeds (20-seed mean 33.10/40 ± 0.30; variance-bound finding) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR261_2026-05-06.md (master `8906d99`, PR #262)
pr_branch: programmer/phase125k-a-more-seeds-2026-05-06 (head `d0e3216`)
qc_branch: qc/pr261-125ka-review-2026-05-06
---

# PR #261 — pre-merge QC verdict: PASS (0/0/0)

30th solo cycle. **Lever A more-seeds completion; variance-bound finding empirically confirmed.** All 8 audit items PASS. 20-seed math verified independently; provenance preserved; pilot 2-seed gate correctly executed; reference set spot-check complete; owner-scope perimeter held; dispatch compliance complete (9th formal exercise).

**Empirical conclusion:** mean 33.10/40 with pop std 0.30 → mean+1σ = 33.40 < baseline 34. Variance-bound (not PROMOTE; not negative). Builder's call is correct; orchestrator can confidently proceed to Lever B (hyperparameter sweep).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. **Provenance integrity** [critical] | ✅ PASS |
| 3. **Pilot 2-seed gate executed** | ✅ PASS |
| 4. **20-seed aggregation correctness** [critical] | ✅ PASS |
| 5. Reference set spot-check completeness | ✅ PASS |
| 6. **Variance characterization conclusion** [critical] | ✅ PASS |
| 7. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 8. TC-X-DISPATCH-COMPLIANCE (9th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge.** Lever A confirms variance-bound finding; orchestrator dispatches Lever B next.

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125k-a-more-seeds-2026-05-06` (three-dot):

```
 review/comms/BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md | 533 +++++
 review/comms/PILOT_REPORT_PHASE125K_A_2026-05-06.md             | 307 +++++
 river-rats-core/models/125k_a/v9_3way_125k_a_full.json          |   1 +
 3 files changed, 841 insertions(+)
```

3 files. Per dispatch expectation:
- ✅ Builder report present (533L)
- ✅ Pilot report present (307L)
- ✅ Model artifact present — but only 1 (`125k_a/v9_3way_125k_a_full.json`), not the 15 per-seed artifacts the dispatch expected. **This is the per-seed × stay-wrong artifact limitation surfaced in PR #253 audit:** trainer only saves median-chosen seed model on promotion-PASS; when promotion refuses (33.10 < 34), per-seed artifacts unavailable. Builder report documents this consistently with PR #253's same observation. Process-improvement candidate (non-blocking) — already tracked from PR #253.
- ✅ No inference output jsonl (trainer's auto-report Section B contains per-seed predictions inline; no separate jsonl)
- ✅ No new training-orchestration script (existing trainer reused per dispatch builder-discretion)

Verified NOT touched:
- `prompts/` (v3.x prompts) — 0 changes
- `design/multiway_reference_set/BATCH2_*` — 0 changes
- `data/corpus_*.jsonl` (READ-only training inputs) — 0 changes
- `training-data/`, plan-comm files, memory files — 0 changes
- Existing model artifacts (warm-start anchor, prior trainer outputs) — 0 changes

Owner-scope perimeter held. **PASS.**

## §2 — Provenance integrity

Per CLAUDE.md "Training provenance" addendum:

| Provenance check | Result |
|---|---|
| Trainer module lives in `river-rats-core/` | ✅ `train_model_v9_student.py` (verified existing in PR #253 audit) |
| Trainer is git-tracked, not heredoc | ✅ tracked file (per curative entry #5) |
| Pilot report cites master HEAD at run time | ✅ `44089bb` (verified in pilot report Section A) |
| Pilot report cites run timestamp | ✅ documented |
| Warm-start anchor cited + verified tracked | ✅ `gto_model_v9_3way_v2.2.json` (unchanged from PR #253) |
| Hyperparameters documented | ✅ same as PR #253 (no drift; n_estimators=800, max_depth=5, lr=0.05, ESR=50, subsample=0.8) |
| Model artifact in PR for promotion-PASS case | N/A — promotion refused (33.10 < 34); only chosen-median saved; consistent with PR #253 trainer design |
| Negative-result trail documented | ✅ Section D provenance hashes section + per-seed table of run states |

**PASS.**

## §3 — Pilot 2-seed gate executed

Per `feedback_pilot_first_for_long_jobs.md` and dispatch §"Pilot batch":

| Pilot-first check | Result |
|---|---|
| Pilot 2-seed (Seeds 5+6) authored FIRST | ✅ `PILOT_REPORT_PHASE125K_A_2026-05-06.md` 307 lines |
| Pilot trainer invocation in separate run | ✅ pilot fired BEFORE full 13-seed run per builder report §"Pilot 2-seed gate" |
| Per-seed scores cited | ✅ Seeds 5=33; Seed 6=33 |
| Pilot gate criteria evaluated | ✅ all 3 criteria PASS (per-seed in [32,35] both 33; schema integrity; 7-seed mean ≥33.0 std ≤1.0 → 33.14/0.35) |
| Pilot gate decision documented | ✅ "Pilot gate CLEAR. Proceeded to full run (Seeds 7-19; 13 additional seeds)." |

Sequence: pilot 2-seed → gate decision → full 13-seed run. Sequence verified by report structure. **PASS.**

## §4 — 20-seed aggregation correctness (CRITICAL)

QC independently re-verified 20-seed table (consolidating PR #253 seeds 0-4 + this PR's pilot seeds 5-6 + full seeds 7-19):

| Seed source | Count | Solver-corrected scores | Sum |
|---|---|---|---|
| PR #253 seeds 0-4 | 5 | 33, 34, 33, 33, 33 | 166 |
| PR #261 pilot seeds 5-6 | 2 | 33, 33 | 66 |
| PR #261 full seeds 7-19 | 13 | 33×12 + 34 (seed 17) = 430 | 430 |
| **Total** | **20** | (18 × 33) + (2 × 34) = 594 + 68 | **662** |

| Statistic | Builder claim | QC verification |
|---|---|---|
| Mean | 33.10/40 | ✅ 662 / 20 = **33.10** |
| Population std | 0.30 | ✅ var = (18 × (33-33.10)² + 2 × (34-33.10)²) / 20 = (18 × 0.01 + 2 × 0.81) / 20 = 1.80 / 20 = 0.09; sqrt(0.09) = **0.30** |
| Sample std (alternative) | — | sqrt(1.80 / 19) = sqrt(0.0947) ≈ 0.308 ≈ 0.30 |

Both population std (0.30) and sample std (0.31) round to 0.30. Math is correct. **PASS.**

Distribution: 2 seeds at 34/40 (seeds 1 and 17); 18 seeds at 33/40. **No seed exceeds baseline 34/40; only 2/20 = 10% at baseline.** Variance bound is tight (std 0.30 vs 0.40 from 5-seed PR #253 — std tightened with N as expected).

## §5 — Reference set spot-check completeness

All 4 stay-wrong hands tabulated at chosen seed 12 (per builder report Section B lines 156-163):

| ref_id | Expert (raw) | Expert (solver-corrected) | Student (chosen seed 12) | Match |
|---|---|---|---|---|
| MW-17 | CALL | CALL | FOLD | ❌ DIVERGE |
| MW-40 | BET | BET | CHECK | ❌ DIVERGE |
| MW-45 | RAISE | RAISE | CALL | ❌ DIVERGE |
| MW-47 | CALL | RAISE (corrected) | CALL | ❌ DIVERGE (matches raw, not solver-corrected) |

Solver-corrected reference labels applied per memory (MW-30, MW-46, MW-47). Builder report Section B explicitly cites: "Solver-correction overlay: applied to ['MW-30', 'MW-46', 'MW-47'] per `memory/reference_corrections.md`. MW-31, MW-50 NOT applied (unverified per blueprint §5.3)."

Section E delta vs PR #253 chosen seed (lines 305-311) confirms: all 4 stay-wrong are STAYED-WRONG across all 20 seeds. Stay-wrong list of 4 unchanged at the model layer.

**Note on MW-40 (informational):** chosen-seed model still predicts CHECK on MW-40, consistent with PR #253 finding (labelling-pipeline-vs-trained-model layer divergence). 12.5K-B and 12.5K-C may correct this — Lever B's hyperparameter sweep could shift the decision boundary; Lever C's augmented data (excluding MW-40 by §5 explicit exclusion) won't directly affect MW-40's training signal.

**PASS.**

## §6 — Variance characterization conclusion (CRITICAL)

Per dispatch outcome matrix (plan §3 Lever A; expected-outcome cases):

| Outcome case | Threshold | Observed | Match |
|---|---|---|---|
| Mean ≥ 34.0/40 within 1-σ → PROMOTE | 33.10 + 0.30 = 33.40 < 34 → NOT within 1-σ | ❌ Not PROMOTE |
| Mean ≈ 33.20/40 ± 0.40 → variance-bound | 33.10 ± 0.30 (within 1-σ of 33.20) → matches | ✅ Variance-bound |
| Mean < 33.0/40 → negative | 33.10 ≥ 33.0 → not negative | ❌ Not negative |

**Conclusion: variance-bound** (mean stays at the 5-seed estimate ± 0.30 with tighter envelope; variance-bound finding confirmed). Builder's call is **correct**.

Implication for Lever B/C dispatch: per dispatch §"Sequencing", on variance-bound → orchestrator proceeds to Lever B (hyperparameter sweep) next. **PASS.**

## §7 — TC-X-OWNER-SCOPE-DISCIPLINE

(Verified in §1 above; restating for completeness.)

- BATCH2 reference UNCHANGED ✓
- Reference labels NOT updated based on model predictions ✓
- v3.x prompts UNCHANGED ✓
- Hyperparameters unchanged from PR #253 ✓
- Warm-start anchor unchanged (`gto_model_v9_3way_v2.2.json`) ✓
- 788-corpus + label files UNCHANGED (training inputs; READ-only) ✓
- Memory edits 0 ✓

**PASS.**

## §8 — TC-X-DISPATCH-COMPLIANCE (9th formal exercise)

| Compliance check | Spec | Observation | Match |
|---|---|---|---|
| Pilot 2-seed gate executed | dispatch §"Pilot batch" | Pilot fired separately (Seeds 5+6) before full run | ✅ |
| 15 new seeds (no fewer; not skipped) | dispatch §"Full run" | 15 new seeds: 2 pilot (5-6) + 13 full (7-19) | ✅ |
| Same config as PR #253 (no hyperparameter drift) | dispatch §"What you do NOT do" | Section A confirms identical hyperparameters | ✅ |
| Warm-start anchor unchanged | dispatch §"What you do NOT do" | Same `gto_model_v9_3way_v2.2.json` | ✅ |
| 20-seed aggregate vs baseline reported | dispatch §"Aggregate verification" | 33.10 ± 0.30 vs 34 baseline; explicit comparison | ✅ |
| Variance-bound call documented | dispatch §"Outcome matrix" | Builder's conclusion mapped to 3-case matrix | ✅ |
| Builder did NOT auto-promote | dispatch §"What you do NOT do" | Promotion gate refused (33.10 < 34); chosen-seed saved but model NOT promoted to baseline | ✅ |

Per `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`: builder discipline matches dispatch authoritative wording. **PASS.**

TC-X-DISPATCH-COMPLIANCE class continues to validate as durable on 9th formal exercise.

## §"Stop conditions" — all clear

Per dispatch §"Stop conditions":
- ❌ Pilot scores diverge wildly (>1 hand spread on 2-seed pilot) → both at 33; spread = 0
- ❌ Schema integrity break → 788/788 join; 61-surface; 40-hand reference eval all clean
- ❌ 20-seed aggregate diverges from 5-seed pilot direction → tightens (std 0.40 → 0.30); same mean direction
- ❌ Provenance gap → none (consistent with PR #253 negative-result trail pattern)

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-23-CANONICAL-STATE sub-vector (curative entry #5; gitignored .json handling — only 1 model artifact in PR consistent with trainer design)
- TC-X-OWNER-SCOPE-DISCIPLINE (11th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (9th formal exercise; clean PASS)** — class durable
- TC-X-METHODOLOGY-RULE-CROSSCHECK (sub-class; pilot-first cell-by-cell against `feedback_pilot_first_for_long_jobs.md`)
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; outcome matrix interpretation cell-by-cell against plan §3)

## Smarter-over-time observations

**Lever A confirms variance bound; QC class system continues to scale to multi-PR cycles:**

- 12.5K-A is the 2nd training-output PR (after PR #253) audited under the curative class system
- TC-X-DISPATCH-COMPLIANCE 9th formal exercise: durable
- Per-seed × stay-wrong artifact limitation surfaced at PR #253 manifested as expected at PR #261; trainer design unchanged; non-blocking
- Math verification (item 4) is a critical audit for training-output PRs; both 33.10 mean and 0.30 std verified independently

**Lever progression:** with Lever A confirming variance-bound, the next dispatch is Lever B (hyperparameter sweep). Per the plan §4, Lever B's pilot is 12 configs × 5 seeds = 60 trainer runs at ~6 hours wall clock. The audit trail for Lever B will follow the same training-output PR pattern (provenance + pilot-first + per-seed math + reference spot-check + dispatch compliance).

## Audit cost / time

- Wall clock: ~14 min (per-seed math verification + provenance check + pilot-first sequence + dispatch cross-check + verdict authoring). Within 15-20 min estimate.
- LLM cost: $0 (mechanical inspection + git operations).

## Gates

PR #261 cleared from QC side. Per dispatch §"What gates on this audit":

- **PR #261 merge:** clear from QC; orchestrator confirms variance-bound outcome
- **12.5K-B Lever B (hyperparameter sweep) dispatch:** gates on PR #261 merge AND variance-bound outcome confirmed (both met by this audit)

No QC-side blocker.

## References

- 12.5K-A dispatch: `MAIN_TERMINAL_PR257_RESOLUTION_AND_125KA_DISPATCH_2026-05-06.md` (master `44089bb`, PR #260)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR261_2026-05-06.md` (master `8906d99`, PR #262)
- Builder report: `BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md` (in PR #261; 533L)
- Pilot report: `PILOT_REPORT_PHASE125K_A_2026-05-06.md` (in PR #261; 307L)
- 12.5J-E source (5-seed prior): PR #253 (master `2b6aa02`)
- Trainer module: `river-rats-core/train_model_v9_student.py` (existing; reused)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (unchanged)
- 12.5K plan §3 outcome matrix: `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (master `9798007`)
- CLAUDE.md "Training provenance" addendum: `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entry #5 (TC-23-CANONICAL-STATE; gitignored .json)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: VERDICT = PASS. PR #261 cleared for merge from QC side. Variance-bound finding empirically confirmed (mean 33.10 ± 0.30; not at-or-above baseline within 1-σ). Builder's variance-bound call is correct. 30th solo QC cycle. TC-X-DISPATCH-COMPLIANCE 9th formal exercise (durable). Orchestrator proceeds to Lever B dispatch on PR #261 merge.**
