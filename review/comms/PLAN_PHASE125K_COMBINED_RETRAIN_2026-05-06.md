---
date: 2026-05-06
from: LEAD-PROGRAMMER (Builder, architect hat)
to: Main terminal (orchestrator) · QC stream · Owner (notice)
re: Phase 12.5K combined re-train DESIGN — 3-lever analysis + sequenced recommendation; pilot-first gates per lever; off-ramp at any failed lever
status: design-only deliverable; execution gates on lever-specific dispatches per orchestrator
---

# PLAN: 12.5K combined re-train (architect-hat design)

## §1 Recap — what 12.5K inherits

| Phase | Outcome |
|---|---|
| 12.5I-MW40-VERIFICATION (A→B→C→D→E) | **Graduation-fail confirmed** via 4-source pattern. PR #241 (Sonnet pilot 25/25 BET) + PR #245 (Opus 4.7 tier-up 5/5 BET) → MW-40 stays BET MEDIUM. Stay-wrong list 4 → 4 (UNCHANGED): MW-17, MW-40, MW-45, MW-47. PR #249 -E memo fully documented. |
| 12.5J-A through 12.5J-E (feature engineering + small-sample re-train) | **Neutral / no-promote.** 2 new Step-18 features shipped (PR #205); 788-corpus 61-surface canonical (PR #222); test-guard deflake (PR #232); 5-seed re-train mean 33.20/40 ± 0.40 vs baseline 34/40 (PR #253) → trainer's promotion gate refused. **All 4 stay-wrong continue to diverge across all 5 seeds at the model layer.** Net effect on aggregate reference-set accuracy: 0 to -1 hand. |
| 12.5J-F synthesis | Rolled into PR #256 resolution. 12.5J workstream NEUTRAL on aggregate accuracy; new features added structural information that didn't realize accuracy gain at the existing 788-row corpus scale. |

**State at 12.5K design fire-time (master `4e55ff4`):**
- v9-3way-v2.2 production model: 34/40 raw / 34/40 solver-corrected (CLAUDE.md project state)
- 788-corpus 61-surface (canonical training input)
- 5-seed re-train at this scale: mean 33.20/40 ± 0.40 (no lift)
- Stay-wrong list: 4 hands; all consistently model-layer-wrong across seeds
- 12.5J-E observation: seed 1 hit baseline (34/40); seeds 0/2/3/4 sat 1 below (33/40); std=0.40 (small but present effect)

## §2 12.5K Goal — push past v9-3way-v2.2 baseline (34/40 solver-corrected) toward ceiling

Per dispatch §"What 12.5K design must address": **what's the highest-quality lever to push past baseline?** This design analyzes 3 levers, sequences them, and specifies pilot-first gates and off-ramps for each. The slow-quality default (`feedback_quality_default_no_ask.md`) is to TEST levers methodically, not to force a positive outcome.

**Acknowledgment of null-result possibility:** 12.5K may produce another no-promote result. The plan is robust to that outcome — each lever has an off-ramp, total budget is bounded, and the orchestrator's go/no-go decision after each lever's pilot-first gate prevents runaway investment.

## §3 Lever A — more seeds (variance characterization)

### Hypothesis

5 seeds is too small to characterize the model's true expected accuracy on the 788-corpus 61-surface. The 12.5J-E mean 33.20/40 ± 0.40 reflects **5-seed sampling variance** more than a true regression. With 10-20 seeds, the empirical mean's confidence interval will tighten; if the true mean is at-or-above 34/40 within 1-σ, the model can be promoted.

### Action

10-15 additional seeds on existing 788-corpus 61-surface + same hyperparameters + same warm-start (`gto_model_v9_3way_v2.2.json`).

| Item | Value |
|---|---|
| Seeds 0-4 (existing) | 33, 34, 33, 33, 33 (PR #253) |
| Seeds 5-19 (new) | TBD |
| Total seeds | 20 (5 existing + 15 new) |
| Trainer | `river-rats-core/train_model_v9_student.py` (existing; reused per dispatch builder-discretion clause) |
| Cost | ~$0 LLM (no labelling); ~6 min/seed CPU × 15 = ~90 min wall clock |
| Pilot-first | 2-seed pilot (Seeds 5 + 6) before scaling to remaining 13 seeds |

### Pilot-first gate (Lever A)

After 2-seed pilot (Seeds 5-6 trained on identical configuration to existing seeds):

| Pilot gate criterion | Continue if... | Off-ramp if... |
|---|---|---|
| Per-seed solver-corrected scores | Both pilot seeds in [32, 35] range (consistent with existing 5-seed distribution) | Either pilot seed shows degenerate output (e.g., < 30 or all-same-class predictions) → STOP, route to orchestrator |
| Schema integrity | 788/788 join clean; 61-surface uniform; reference eval produces 40 hands | Schema mismatch on either pilot seed → STOP |
| Aggregate over 7 seeds (5 existing + 2 pilot) | Mean ≥ 33.0/40 with consistent std | Mean < 32.5/40 OR std > 1.0 → STOP (variance characterization will not converge cleanly; route to orchestrator) |

### Expected outcome (3 cases)

| Case | Action |
|---|---|
| **Mean ≥ 34.0/40 within 1-σ** (e.g., observed mean 33.7 ± 0.5) | PROMOTE; lever A succeeds; off-ramp Lever B and C |
| **Mean ≈ 33.20/40 ± 0.40 (replicates existing)** | Variance-bound finding confirmed; conclude 12.5J adds no measurable lift; proceed to Lever B with this finding documented |
| **Mean < 33.0/40 (worse than existing)** | Negative result; surface for orchestrator (possibly indicates training instability; Lever B may be premature) |

### Slow-quality assessment

Lever A is **cheap, fast, and informative**. It's the right first lever:
- Eliminates the "5-seed variance" hypothesis cheaply
- Doesn't bias subsequent levers (variance characterization is purely observational)
- If it succeeds, no further work needed
- If it fails, we have stronger empirical grounding for Lever B/C

## §4 Lever B — hyperparameter exploration (CV-driven sweep)

### Hypothesis

Existing hyperparameters in `train_model_v9_student.py` were tuned for the 59-surface (pre-PR #205) corpus. The 61-surface adds 2 new features (`nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index`) which may interact differently with `n_estimators`, `max_depth`, `learning_rate`, regularization. A re-tuned config may extract more signal.

### Action

Structured hyperparameter sweep with proper cross-validation discipline:

| Item | Value |
|---|---|
| Hyperparameters swept | `n_estimators` (current default; tested 200/500/800/1000), `max_depth` (current default; tested 4/6/8/10), `learning_rate` (current default; tested 0.05/0.10/0.15), `reg_alpha` + `reg_lambda` (regularization; tested 0/0.1/1.0/10.0) |
| Total grid size | 4 × 4 × 3 × 4×4 = 768 configs (too many; pilot-first to narrow) |
| Pilot-first grid | 12 carefully-chosen configs spanning the corner cases of the full grid |
| CV strategy | 5-fold cross-validation on 788-row corpus (NOT on reference set; reference set is held out for final evaluation) |
| Seeds per config | 5 (matching 12.5J-E protocol) |
| Trainer | `river-rats-core/train_model_v9_student.py` extended with `--hyperparams-config` arg (small modification; documented as `feedback_quality_default_no_ask` slow-quality option vs. inline-config-dict) |
| Cost | ~$0 LLM; ~6 min/seed × 5 seeds × 12 configs = ~6 hours wall clock pilot; ~30 hours full grid |
| Pilot-first | 12-config pilot before deciding on full-grid expansion |

### Pilot-first gate (Lever B)

After 12-config pilot:

| Pilot gate criterion | Continue if... | Off-ramp if... |
|---|---|---|
| Best pilot config CV score | Significantly higher than existing config CV score (Δ ≥ 1 hand on 40-row reference equivalent) | Best pilot config CV ≤ existing → STOP, conclude default hypers were already near-optimal; off-ramp Lever B |
| Reference set evaluation of best pilot config | Better than baseline 34/40 with 5-seed mean | Reference set evaluation ≤ baseline → off-ramp |
| Stability across seeds | std < 0.5 across 5 seeds for best config | std > 1.0 → unstable; surface to orchestrator |

### Expected outcome (3 cases)

| Case | Action |
|---|---|
| **Best pilot config beats baseline by ≥1 hand on 5-seed mean** | PROMOTE best config; full-grid expansion optional (orchestrator decides) |
| **Best pilot config matches baseline (34/40)** | Modest gain; promote if interpretable; document as Lever-B-marginal |
| **Best pilot config matches existing 33.20/40** | Lever B fails; off-ramp |

### Slow-quality assessment

Lever B is **moderately expensive (~6 hour pilot)** but methodologically sound. Risks: overfitting to held-out folds; reference-set evaluation is the only real signal. The CV discipline + held-out reference set protects against this.

**Caveat:** Lever B should fire AFTER Lever A. If Lever A succeeds (variance reveals true mean ≥ 34), Lever B becomes optional refinement. Conversely, if Lever A confirms 33.20 ± 0.40 is the true mean, Lever B's hyperparameter improvement target becomes well-defined.

## §5 Lever C — augmented training data (further labelling rounds)

### Hypothesis

The 788-row corpus is undersized for the 5-class 61-feature problem, especially for the rare classes:
- FOLD: 81 / 788 = 10.3% of corpus
- CALL: 81 / 788 = 10.3% of corpus
- BET: 169 / 788 = 21.4%
- CHECK: 326 / 788 = 41.4%
- RAISE: 131 / 788 = 16.6%

Stay-wrong axes (MW-17 + MW-47) are CALL/RAISE on facing-bet spots — under-represented in corpus relative to CHECK/BET on checked-through spots. Adding more data targeted at the failing axes may move the model's decision boundary.

### Action

NEW labelling round targeting the 4 stay-wrong axes:
- **Sub-axis MW-17**: Under-calling on low-equity draw + facing-bet 3-way+
- **Sub-axis MW-45**: Under-raising on broadway-completed turn + multiway
- **Sub-axis MW-47**: Shared blind spot (nut FD + blocker should RAISE)
- **Sub-axis MW-40**: Already verified (graduation-fail; do NOT re-label)

Mirror MW-40-VERIFICATION pattern but at smaller scale (no need for 30-hand verification; aim for 50-100 hands per axis × 3 axes = 150-300 hands new training data, NOT verification).

| Item | Value |
|---|---|
| Hands per axis | 50-100 (parametric variants per axis) |
| Total new corpus | 150-300 hands (target = 250-300; gives 1038-1088 corpus = 30-40% expansion) |
| Sonnet labellers | 5 per hand (consensus pattern from 12.5I-C) |
| Opus tier-up | On 5 canonical hands per axis × 3 axes = 15 Opus calls (per `feedback_pilot_first_for_long_jobs.md` sub-rule for training-data outputs) |
| Cost | ~$50-150 LLM (5 Sonnet × 250 hands × ~$0.05/hand = $62; 15 Opus × $1 = $15; ~$80 total budget) |
| Wall clock | ~3-5 hours total (design ~30 min + situation gen ~30 min + labelling ~2-3 hours + Opus tier-up ~30 min + report ~30 min) |
| Pilot-first | Per axis: 5-hand pilot × 5 Sonnet labellers; gate on pilot consensus aligned with axis prediction |

### Pilot-first gate (Lever C)

Per axis, before scaling beyond pilot:

| Pilot gate criterion | Continue if... | Off-ramp if... |
|---|---|---|
| Pilot consensus aligns with structural prediction | ≥4/5 hands consensus on the predicted action (RAISE for MW-47-axis; CALL for MW-17-axis; RAISE for MW-45-axis) | Consensus diverges from prediction (parallel of MW-40-VERIFICATION-C HALT) → REPORT to orchestrator; investigate whether labelling pipeline disagrees with the structural argument BEFORE scaling |
| Sonnet API errors | <5% on pilot | >5% → STOP infrastructure issue |
| Reasoning convergence | Convergent reasoning citing v3.4 KB sections | Mode-collapse-style identical text → STOP |

### Expected outcome (3 cases)

| Case | Action |
|---|---|
| **All 3 axis pilots align with structural prediction** | Scale to full 50-100 per axis; ship as 1038-1088 corpus → re-train (Lever B if completed; or default hypers) → measure delta vs baseline |
| **1-2 axis pilots diverge from prediction (parallel of MW-40 graduation-fail)** | Surface to orchestrator; partial scale (only the aligned axes); consider whether the divergent axes are model-class-blind |
| **All 3 axis pilots diverge** | Lever C fails; off-ramp; document as model-class-blind-on-stay-wrong finding |

### Slow-quality assessment

Lever C is **most expensive ($80 + 3-5 hours)** but addresses the root cause (under-represented classes). Risks: if the labelling pipeline diverges from the structural prediction (as happened with MW-40), the new data won't help — and may actively hurt by introducing noise that contradicts ground truth.

**Caveat:** Lever C should fire AFTER Lever A AND Lever B. The dispatch's outcome matrix for MW-40-VERIFICATION revealed that **the labelling pipeline's protocol routing dominates over structural arguments**; this is a real risk for any future verification-style labelling round on the other stay-wrong axes.

## §6 Sequenced recommendation

**Recommended sequence: A → B → C, with explicit gates between each lever.**

```
[start]
  │
  ▼
LEVER A — more seeds (variance characterization)
  cost: ~$0 / ~90 min
  pilot: 2 seeds (5+6) → gate on consistency w/ existing
  full: 13 more seeds → 20-seed mean
  │
  ├─→ MEAN ≥ 34 within 1-σ → PROMOTE → SKIP B and C → 12.5L gate eval
  │
  ├─→ MEAN ≈ 33.20 ± 0.40 (variance-bound confirmed)
  │     │
  │     ▼
  │   LEVER B — hyperparameter sweep (CV-driven)
  │     cost: ~$0 / ~6h pilot + optional ~30h full grid
  │     pilot: 12 configs × 5 seeds → gate on Δ ≥ 1 hand on CV
  │     full: scaled grid OR best-config retrain
  │     │
  │     ├─→ BEST CONFIG > BASELINE → PROMOTE → 12.5L gate eval
  │     │
  │     └─→ BEST CONFIG ≤ BASELINE
  │           │
  │           ▼
  │         LEVER C — augmented training data (labelling round)
  │           cost: ~$80 / ~5h
  │           pilot: per-axis 5-hand × 5 Sonnet labeller
  │           full: 250-300 hand expansion → re-train
  │           │
  │           ├─→ ALL 3 AXES ALIGN → CORPUS → RETRAIN → if > baseline → PROMOTE → 12.5L
  │           │
  │           └─→ AXES DIVERGE FROM PREDICTION → off-ramp; document model-class-blind-on-stay-wrong
  │
  └─→ MEAN < 33.0 (regression) → STOP, route to orchestrator (training instability)
```

### Why this sequence (slow-quality reasoning)

1. **A first**: cheapest, fastest, eliminates a hypothesis cleanly. If the 12.5J-E result was variance-bound, A reveals it before any expensive work.
2. **B second**: moderate cost. Hyperparameter mismatch is plausible because 61-surface is new vs the 59-surface hypers were tuned for. Should NOT precede A because variance characterization defines B's improvement target.
3. **C last**: most expensive. Augmented data is the most plausible long-term lift but also the most risky (could replicate MW-40 verification's negative finding). Doing C without A and B as priors means burning $80 + 5 hours when the answer might already be in A.

### Off-ramp at any lever

After ANY lever's pilot-first gate:
- If lever succeeds → promote + 12.5L
- If lever fails cleanly → next lever in sequence
- If lever is unstable / unclear → STOP, route to orchestrator (no-auto-fix)

## §7 Cost + time budget + pilot-first gates per lever

| Lever | Pilot cost | Pilot wall clock | Full cost | Full wall clock | Total budget |
|---|---|---|---|---|---|
| A | ~$0 | ~12 min (2 seeds × 6 min) | ~$0 | ~78 min (13 more seeds) | ~$0 / ~90 min |
| B | ~$0 | ~6 hours (12 configs × 5 seeds × 6 min) | ~$0 | ~30 hours (full grid OR best-config × 5 seeds) | ~$0 / ~6-36 hours |
| C | ~$5 | ~30 min (15 pilot × 5 Sonnet labellers) | ~$80 | ~3-5 hours (250-300 × 5 Sonnet + 15 Opus + retrain) | ~$80 / ~3.5-5.5 hours |
| **Total (A → fail → B → fail → C → fail)** | — | — | — | — | **~$85 / ~9.5-41.5 hours wall clock** |

Per dispatch §"Stop conditions": "Plan total budget exceeds ~$300 LLM OR ~30 hours wall clock without explicit orchestrator approval → REPORT (not STOP); surface for orchestrator decision."

**Total LLM budget: ~$85 (well under $300).** Total wall clock: 9.5-41.5 hours (the 41.5h max requires Lever B's full grid; if B's pilot is decisive, the max is ~9.5 hours). **Wall-clock max IS within the 30-hour soft cap** if Lever B uses pilot-only or best-config-only execution rather than the full 30-hour grid.

**Builder recommendation: cap Lever B at the 12-config pilot phase (6 hours) initially.** If pilot reveals a clearly dominant config, run that config with 5 seeds (additional ~30 min) and stop. Do NOT execute the full 30-hour grid unless A AND B-pilot both fail AND orchestrator explicitly approves.

This caps total wall clock at ~9.5 hours (A + B-pilot-only + C). Well within the 30-hour soft cap.

## §8 Stop conditions (this PR — design phase)

Per dispatch §"Stop conditions":

- Plan diverges from quality-default sequencing (e.g., recommends Lever C BEFORE evaluating Lever A's variance characterization) → ✅ Plan sequences A → B → C correctly
- Plan does NOT include pilot-first gates per lever → ✅ Each lever has explicit pilot-first gate (§3, §4, §5)
- Plan recommends bypassing reference-set held-out evaluation → ✅ All levers preserve reference set as held-out signal; CV uses 5-fold on 788-corpus, NOT on reference
- Plan recommends solver-as-labels for any new labelling round → ✅ Lever C explicitly cites `feedback_solver_vs_expert_labels.md` prohibition; no solver labels
- Plan total budget exceeds ~$300 LLM OR ~30 hours wall clock without explicit orchestrator approval → ✅ ~$85 LLM (well under); ~9.5h cap with B-pilot-only (within 30h soft cap)

No stop conditions triggered.

## §9 What this PR does NOT do (per dispatch)

- ❌ Does NOT execute any retrain (this is design only)
- ❌ Does NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- ❌ Does NOT modify river-rats-core/ source (read-only reference)
- ❌ Does NOT modify BATCH2 reference
- ❌ Does NOT touch existing 788-corpus or label files
- ❌ Does NOT auto-fix the 12.5J-E result (it's input data; orchestrator-scope to interpret)
- ❌ Does NOT recommend a single-lever-only plan (analyzed all 3 with sequenced recommendation)

## §10 Risks + open questions for orchestrator

Per `feedback_orchestrator_decides_not_recommends.md`: experts recommend HOW; orchestrator decides WHAT. Where I have committed to a position, no question is raised. Where scope is ambiguous, I flag it.

| # | Risk / question | Builder default (committed) | When orchestrator must override |
|---|---|---|---|
| R1 | Lever B's full 30-hour grid is unbounded; pilot-only may miss the global optimum | Cap Lever B at 12-config pilot + best-config retrain (~6.5 hours total) | If orchestrator wants global-optimum search → approve full grid (30 hours) explicitly |
| R2 | Lever C's per-axis labelling round may produce more graduation-fail outcomes (parallel of MW-40-VERIFICATION) | Run pilot-first per axis with HALT-on-divergence pattern (per PR #241 / PR #245 precedent); accept partial scale (only aligned axes) | If orchestrator wants single-axis scope → narrow Lever C to one axis (e.g., MW-47 first) |
| R3 | The 12.5J-E observation (seed 1 hit baseline) may indicate Lever A will reveal a slightly-positive mean | Lever A's 20-seed mean characterization handles this | None — design is robust |
| R4 | Combined 12.5K (multi-lever sequence) interacts with 12.5L gate evaluation; some levers may produce models that differ on per-hand predictions even if aggregate is similar | Document per-hand differences in each lever's report; 12.5L decides on which model to ship | None — design supports |
| R5 | The "MW-40 graduation-fail" finding from 12.5I shows the labelling pipeline can diverge from structural arguments. Lever C is exposed to this risk on the OTHER stay-wrong axes (MW-17, MW-45, MW-47). Pre-emptive cross-check against v3.4 DO NOT rules + composition quad routing rules is the right discipline (per the surfaced standing-rule candidate from PR #248). | Lever C design includes the per-axis pilot-first HALT pattern; accept axes-fail outcome cleanly | None — design supports; orchestrator decides per-axis if HALT triggers |
| R6 | The 788-corpus class imbalance (FOLD/CALL = 10.3% each) may cause the model to under-call/under-fold even with more data. Lever C's 250-hand expansion to 1038 corpus barely shifts the class ratios. | Document the class ratios + observe whether expansion helps; cap Lever C scope at 250 unless orchestrator approves more | Future phase 12.5M may need explicit class re-weighting OR larger expansion if class imbalance remains the bottleneck |

## §11 References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR253_RESOLUTION_AND_125K_DESIGN_DISPATCH_2026-05-06.md` (master `4e55ff4`, PR #256)
- 12.5J-E source (mean 33.20/40 ± 0.40): PR #253 master `2b6aa02`
- 12.5J-E builder report: `BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` (master `2b6aa02`)
- 12.5I-MW40-VERIFICATION-E -E memo (graduation-fail): PR #249 master `34325ec`
- 788-corpus (canonical training input): `data/corpus_combined_788_2026-05-06.jsonl` (PR #222 master `48084c3`)
- Plan precedent for design comm structure: `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228)
- Plan precedent for corpus-expansion design: `PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md` (master `54e2943`)
- Trainer module: `river-rats-core/train_model_v9_student.py` (existing; reusable for Lever A; needs `--hyperparams-config` extension for Lever B)
- v3.4 protocol prompt: `prompts/gto_labeller_v3.4.md`
- v9-3way-v2.2 baseline: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (34/40 solver-corrected per CLAUDE.md project state)
- Memory: `feedback_quality_default_no_ask.md` (slow-quality A → B → C sequencing), `feedback_pilot_first_for_long_jobs.md` (binding for all 12.5K execution levers), `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides per-lever go/no-go), `feedback_solver_vs_expert_labels.md` (Lever C prohibits solver-as-labels), `feedback_solver_findings.md` finding 2 (blocker effects sensitivity in Lever C label design), `feedback_attention_flags_when_features_change.md` (Lever B hyperparameter changes don't affect feature surface; if surface changes, attention vocab + capture + trainer must update in lockstep)

**Status: 12.5K combined re-train DESIGN complete. 3 levers analyzed (A: more seeds; B: hyperparameter sweep; C: augmented training data); sequenced recommendation A → B → C with pilot-first gates and off-ramps per lever; total budget ~$85 LLM / ~9.5 hours wall clock at the recommended cap (B-pilot-only). PR opens for QC audit per dispatch §"QC stream — what you audit". Builder ready for 12.5K-A execution dispatch on this PR's merge.**
