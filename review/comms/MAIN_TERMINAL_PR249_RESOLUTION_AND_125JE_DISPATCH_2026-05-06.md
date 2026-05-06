---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #249 + PR #251 merged (QC PASS clean; MW-40 verification round closed; 27th solo cycle); reconcile 12.5J phase numbering; dispatch 12.5J-E small-sample re-train + reference set spot-check (pilot-first 1-seed gate)
status: DIRECTIVE — merges PR #249 + PR #251; fires LEAD-PROGRAMMER on 12.5J-E — fire now
---

# PR #249 + PR #251 merge + 12.5J-E small-sample re-train dispatch

QC verdict on PR #249 (`REVIEW_QC_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` on `qc/pr249-mw40-verification-e-review-2026-05-06`, PR #251): **PASS — closes MW-40 verification round (A→B→C→D→E).** 27th solo cycle expected. MW-40 verification mini-phase fully documented. Stay-wrong list count: **4** (MW-17, MW-40, MW-45, MW-47). BATCH2 MW-40 reference: **BET MEDIUM** (unchanged).

## 12.5J phase reconciliation

Per `MAIN_TERMINAL_PHASE125J_DISPATCH_2026-05-06.md` original definition:
- 12.5J-A: feature design ✅ shipped
- 12.5J-B: feature implementation in `feature_extractor.py` ✅ PR #205 (master `0b77bdd`)
- 12.5J-C: corpus re-extraction (existing 694 + 12.5I) ✅ effectively shipped via PR #205 (694 re-extracted to 61-surface) + PR #222 (94-revision Step-18 backfill; 788-corpus uniformly 61-surface)
- 12.5J-D: QC sweep on 61-surface integrity ✅ effectively shipped via PR #224 (QC PASS clean on PR #222 corpus)
- 12.5J-D-pre: test-guard deflake (Option b Δ-tolerance) ✅ PR #232 (master `cd06c02`)
- 12.5J-E: small-sample re-train + reference set spot-check on MW-17 + MW-47 — **CURRENT (this dispatch)**
- 12.5J-F: synthesis / gate evaluation — pending -E outcome
- 12.5K: combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)

12.5J-C and 12.5J-D were rolled up into 12.5I-D's deliverable (PR #222 produces a 788-corpus that is BOTH the 12.5I corpus expansion AND the 12.5J-C re-extracted-to-61-surface corpus). QC PASS on PR #222 (PR #224) provides the 12.5J-D integrity sweep evidence. **Per `feedback_orchestration_efficiency_rules.md`**: this rollup is correct (avoids duplicate work); not a process violation.

## LEAD-PROGRAMMER — Step: 12.5J-E small-sample re-train (fire on this comm merge)

Per `PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md` table row "12.5J-E | PROGRAMMER_REPORT_PHASE125J_E | small-sample re-train (5 seeds × 694-hand corpus or 794 if 12.5I shipped) + reference set spot-check on MW-17 + MW-47 | QC APPROVE; partial PROMOTE on flip".

Branch: `programmer/phase125j-e-small-sample-retrain-2026-05-06`. Base: master post-this-comm-merge.

### Scope — 5 seeds × 788-hand corpus + reference set spot-check (pilot-first 1-seed gate)

Source corpus: `data/corpus_combined_788_2026-05-06.jsonl` (PR #222 merged; 61-surface uniform). Trainer: `river-rats-core/train_model.py` (per CLAUDE.md "Training provenance" addendum 2026-04-15: every model-producing script must live in river-rats-core/ with provenance docstring linking commit to artifact).

### Pilot-first 1-seed gate (binding per `feedback_pilot_first_for_long_jobs.md`)

Training jobs ARE long batches. Per the standing rule, split:

1. **Pilot batch (Seed 1 only)**: train 1 model on 788-hand corpus 61-surface. Evaluate on reference set. ~15-30 min wall clock.
2. **Pilot gate**: examine pilot output before scaling:
   - Trainer ingests 788-corpus without errors (61-surface schema clean) → PASS gate
   - Reference set inference produces predictions for all 40 reference hands → PASS gate
   - Stay-wrong subset (MW-17, MW-40, MW-45, MW-47) gets predictions; report per-hand action vs canonical label
   - If trainer crashes, schema mismatch, or systematic prediction failures (e.g., all predictions = same class) → STOP and report to orchestrator
3. **Full run (Seeds 2-5; after pilot gate clear)**: train 4 more models with different seeds. Aggregate predictions across 5 seeds. ~60-120 min wall clock total for seeds 2-5.

### Reference set spot-check focus

Per plan §"12.5J-E" original spec: spot-check focuses on **MW-17 + MW-47** (the original 12.5J target hands; the structural feature-engineering work was designed for those). Per current state, expand to include **all 4 stay-wrong** (MW-17, MW-40, MW-45, MW-47) for completeness.

For each stay-wrong hand, report:
- Canonical (BATCH2 reference) action
- Per-seed prediction (5 seeds: action + probability)
- Aggregate (5-seed majority vote + average probability per action class)
- Match/Diverge vs canonical
- Δ-comparison vs prior model (v9-3way-v2.2 baseline at 32/40 = 80% raw / 82.5% solver-corrected on the 40-hand reference set per CLAUDE.md project state)

### Training config (per existing `train_model.py` defaults)

- XGBoost (per existing trainer)
- 5 seeds (1 pilot + 4 full)
- Sample weights: consensus_confidence (per 12.5I-D corpus assemble report; 0.4-1.0 weights are the down-weighted to high-signal training rows)
- Train/test split: per existing trainer default; document in builder report
- Hyperparameters: per existing trainer default; document any deviation in builder report
- Model output paths: `river-rats-core/models/v9_3way_125j_e_seed_N.joblib` (or whatever the existing convention is)
- Provenance: per CLAUDE.md addendum, docstring linking the commit hash producing each model artifact

### Stop conditions

- Trainer crash on 788-corpus 61-surface ingestion → STOP (route to orchestrator)
- Schema mismatch between trainer expectations and corpus → STOP
- Reference-set inference fails on any of the 40 hands → STOP (model output integrity)
- Pilot seed produces all-same-class predictions on reference set → STOP (degenerate model; orchestrator decides retry vs investigate)
- 5-seed aggregate predictions diverge wildly across seeds (>30% disagreement on stay-wrong hands) → REPORT (high training variance flag; orchestrator decides whether to extend to more seeds)
- Solver-as-labels appears in any reasoning or training-data citation → STOP

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source EXCEPT for the new training script if needed (per CLAUDE.md "Training provenance" — script must live in river-rats-core/)
- Do NOT modify BATCH2 reference (orchestrator-scope; locked unless graduation outcome dispatched)
- Do NOT modify the 788-corpus or any prior-phase corpus
- Do NOT update reference labels based on model predictions (model performance is observed, not used to update ground truth)
- Do NOT skip the pilot-first 1-seed gate (binding per `feedback_pilot_first_for_long_jobs.md`)
- Do NOT auto-fix degenerate pilot model (route to orchestrator)
- Do NOT trigger 12.5K combined re-train (that's a separate dispatch on 12.5J-E QC PASS)

### Cost / time

~$0 (no LLM calls; pure XGBoost training + Python inference). ~2-3 hours wall clock total (pilot 15-30 min + full 60-120 min + report 15-30 min).

### Deliverable scope

Expected files in PR diff:
1. `river-rats-core/train_125j_e_small_sample.py` (new training script per CLAUDE.md "Training provenance"; OR if existing `train_model.py` is reusable as-is, that's also acceptable — builder discretion within the provenance discipline)
2. `river-rats-core/models/v9_3way_125j_e_seed_1.joblib` through `seed_5.joblib` (5 model artifacts)
3. `data/inference_125j_e_reference_predictions_2026-05-06.jsonl` (40 reference hands × 5 seeds = 200 predictions; OR 40 rows × 5 prediction columns; format consistent with prior inference outputs)
4. `review/comms/BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` (the report)

### Builder report sections (mandatory)

- §"Pilot 1-seed gate" — pilot results + gate decision
- §"Full 5-seed training" — per-seed metadata + aggregate
- §"Reference set spot-check" — 40-hand predictions table + stay-wrong subset analysis
- §"Stay-wrong subset detail" — per-hand 5-seed breakdown + comparison vs canonical for MW-17 / MW-40 / MW-45 / MW-47
- §"Comparison vs v9-3way-v2.2 baseline" — Δ on aggregate accuracy + Δ on per-stay-wrong predictions
- §"Provenance" — per CLAUDE.md addendum: which commit hash produced which model artifact
- §"Stop conditions" — full record (which triggered, which didn't)
- §"What's blocked / what's queued" — 12.5J-F (synthesis); 12.5K (combined re-train; gates on -E + 12.5I-MW40-VERIFICATION-E both shipped)
- §"References"

## QC stream — what you audit (when 12.5J-E PR opens)

Standalone audit, ~15-20 min, 8-item scope (training-output format):

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (training script + 5 models + inference output + report). Verify no v3.x prompts / BATCH2 / training-data corpus / unrelated river-rats-core/ touched.
2. **Provenance integrity** — verify training script docstring links the commit hash to each model artifact (per CLAUDE.md addendum). Critical for reproducibility.
3. **Pilot-first gate executed** — builder report shows pilot 1-seed result + gate decision before full run.
4. **5-seed aggregation correctness** — verify aggregation math (majority vote / average probability) computed correctly from per-seed outputs.
5. **Reference set spot-check completeness** — all 40 reference hands have predictions; all 4 stay-wrong hands have detailed per-seed breakdowns.
6. **Schema integrity** — inference output schema consistent with prior inference outputs; 61-feature surface used uniformly.
7. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm BATCH2 reference unchanged; reference labels NOT updated based on model predictions; v3.x prompts UNCHANGED.
8. **TC-X-DISPATCH-COMPLIANCE (7th formal exercise)** — pilot-first executed; 5 seeds (no fewer; not skipped); reference set spot-check focuses on stay-wrong (MW-17/40/45/47); aggregate comparison vs v9-3way-v2.2 baseline reported.

QC writes `review/comms/REVIEW_QC_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` on `qc/pr<N>-125je-retrain-review-2026-05-06`.

## Why no Opus tier-up on 12.5J-E

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs (LLM judgments). 12.5J-E is mechanical training + inference (no LLM in the loop). Pilot-first 1-seed gate is the appropriate quality discipline at this scope. Standard QC PASS suffices.

## Sequencing — what fires after 12.5J-E merges

1. **12.5J-F synthesis** (gate evaluation; orchestrator-scope per plan; small-form decision comm summarizing 12.5J outcomes)
2. **12.5K combined re-train design** — gates on 12.5J-E ship AND 12.5I-MW40-VERIFICATION-E ship (the latter shipped this session; the former pending). Architect-hat phase.
3. **12.5L gate evaluation** — gates on 12.5K.

12.5K is the next big milestone. Per project state in CLAUDE.md, current model is **v9-3way-v2.2 at 82.5% solver-corrected accuracy on 40-hand reference set**. 12.5K's goal is to push toward the ceiling using the 788-corpus 61-surface + 12.5J feature engineering.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #249 merge (Builder -E memo)
- PR #251 merge (QC verdict record)
- 12.5J-E small-sample re-train dispatch fires
- MW-40 verification mini-phase fully closed (A→B→C→D→E shipped)
- 12.5J-C / 12.5J-D phase numbering reconciled (rolled up into PR #205 + PR #222 + PR #224)

**Newly queued (after 12.5J-E merges):**
- 12.5J-F synthesis (small comm)
- 12.5K combined re-train design

**Still queued (later):**
- 12.5K combined re-train execution
- 12.5L gate evaluation

**Owner-scope items pending (informational, non-blocking):**
- TC-X-INTRA-PLAN-CONSISTENCY ratification (curative entry #13)
- TC-X-DISPATCH-COMPLIANCE ratification (5+ exercises now)
- Memory note refresh for "composition quad" vs "composition triple" terminology (NIT-1 carried; surfaced in -E memo)
- "Structural arguments must cross-check against v3.4 DO NOT rules" — process-improvement standing-rule candidate (surfaced from -C HALT empirical finding)

## References

- PR #249 (Builder -E graduation-fail memo): branch `programmer/phase125i-mw40-verification-e-memo-2026-05-06`
- PR #251 (QC PASS verdict closing MW-40 verification round): branch `qc/pr249-mw40-verification-e-review-2026-05-06`
- PR #248 (orchestrator -E dispatch): master `92e2d85`
- PR #205 (12.5J-B feature impl 59→61): master `0b77bdd`
- PR #222 (12.5I-D corpus assemble; 788-corpus 61-surface): master `48084c3`
- PR #224 (QC PASS on PR #222; provides 12.5J-D integrity evidence rollup): master `4d8fcf8`
- PR #232 (12.5J-D-pre test-guard deflake; Option b Δ-tolerance): master `cd06c02`
- 12.5J master plan: `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md`
- CLAUDE.md "Training provenance" addendum (2026-04-15): `review/comms/PLAN_CONSOLIDATED_2026-04-15.md` §5.1
- v9-3way-v2.2 baseline: 32/40 = 80% raw / 82.5% solver-corrected (CLAUDE.md project state)
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestration_efficiency_rules.md` (rollup of 12.5J-C/D into PR #222), `feedback_pilot_first_for_long_jobs.md` (1-seed gate; binding), `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`

**Status: PR #249 + PR #251 cleared for merge. MW-40 verification mini-phase closed. LEAD-PROGRAMMER fires 12.5J-E small-sample re-train (5 seeds × 788-hand corpus 61-surface; reference set spot-check on stay-wrong) on this comm merge. ~2-3 hours wall clock to PR open (pilot ~15-30 min + full ~60-120 min + report).**
