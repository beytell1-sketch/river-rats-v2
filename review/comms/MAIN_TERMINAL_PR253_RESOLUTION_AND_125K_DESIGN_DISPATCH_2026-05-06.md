---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #253 + PR #255 merged (QC PASS; 28th solo cycle); accept builder no-promote call (12.5J-E mean 33.20/40 ± 0.40 vs baseline 34/40); 12.5J-F synthesis (rolled in); dispatch 12.5K combined re-train DESIGN phase (architect-hat)
status: DIRECTIVE — merges PR #253 + PR #255; rolls in 12.5J-F synthesis; fires LEAD-PROGRAMMER on 12.5K design — fire now
---

# PR #253 + PR #255 merge + 12.5J-F synthesis + 12.5K design dispatch

QC verdict on PR #253 (`REVIEW_QC_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` on `qc/pr253-125je-retrain-review-2026-05-06`, PR #255): **PASS**. 28th solo cycle expected. 8-item training-output audit cleared (provenance + pilot-first + 5-seed aggregation + ref-set spot-check + schema + owner-scope + dispatch compliance).

## Builder no-promote call ACCEPTED

**Empirical finding (5 seeds × 788-corpus 61-surface, mean 33.20/40 ± 0.40 solver-corrected):**

| Seed | Raw | Solver-corrected |
|---|---|---|
| 0 | 34/40 | 33/40 |
| 1 | 35/40 | 34/40 (= baseline) |
| 2 | 34/40 | 33/40 (median) |
| 3 | 34/40 | 33/40 |
| 4 | 34/40 | 33/40 |
| **mean** | — | **33.20/40 ± 0.40** |

vs v9-3way-v2.2 baseline: 34/40 raw / **34/40 solver-corrected**.

**Per quality-default (`feedback_quality_default_no_ask.md`):** don't ship a regression. 12.5J-E's 5-seed mean is -0.80 below baseline on solver-corrected. Even seed 1 (the single seed at baseline) is at parity, not an improvement. **Builder's call to NOT promote is the correct slow-quality choice.** Orchestrator accepts.

## 12.5J-F synthesis (rolled into this comm per `feedback_orchestration_efficiency_rules.md`)

Per plan `PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md` table row "12.5J-F | MAIN_TERMINAL_PHASE125J_F_SYNTHESIS | gate evaluation; integration with 12.5I at 12.5K | owner WHAT". The user's direction "continue without asking for confirmation on anything" + `feedback_orchestrator_decides_not_recommends.md` authorizes me to perform the synthesis decision under decision authority.

### 12.5J synthesis decision

**12.5J workstream outcome: NEUTRAL.** Net effect on the 40-hand reference set: 0 to -1 hand vs v9-3way-v2.2 baseline.

| Component | Result | Status |
|---|---|---|
| 12.5J-A: feature design | 2 new features designed for MW-17 + MW-47 axes | ✅ shipped (PR #198) |
| 12.5J-B: feature implementation (59→61) | 2 new features implemented in `feature_extractor.py` | ✅ shipped (PR #205) |
| 12.5J-C/D: corpus re-extraction + integrity sweep | 788-corpus 61-surface canonical | ✅ effectively rolled into PR #205 + PR #222 + PR #224 (no separate PR needed; rollup per `feedback_orchestration_efficiency_rules.md`) |
| 12.5J-D-pre: test-guard deflake | tier-2 invariant Δ-tolerance 0.05 (Option b) | ✅ shipped (PR #232) |
| 12.5J-E: small-sample re-train | 5 seeds; mean 33.20/40 ± 0.40; **no-promote** | ✅ shipped (PR #253; this resolution) |

### Empirical finding (synthesis)

The 2 new Step-18 features (`nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index`) **did NOT move the needle on aggregate reference-set accuracy**:
- Both show low feature importance (`nut_blocker_overcard_count` = 0.1026 chosen seed = 1st place; `bet_call_multiway_oop_raise_pressure_index` = 0.0000 last; mixed signal)
- Per-hand outcome on stay-wrong subset:
  - **MW-17** (stay-wrong; 12.5J target axis): student FOLD vs canonical CALL → still wrong
  - **MW-47** (stay-wrong; 12.5J target axis; solver-corrected RAISE): student CALL → still wrong
  - **MW-40** (stay-wrong; just confirmed graduation-fail): student CHECK vs BATCH2 BET → still wrong (consistent with -C empirical refutation)
  - **MW-45** (stay-wrong): student CALL vs canonical RAISE → still wrong

**Net interpretation:** the 12.5J feature-engineering work added structural information that the model can use, but the existing 788-row corpus + standard hyperparameters + 5 seeds × warm-start config does NOT realize a measurable accuracy gain. This is a NULL result on the aggregate reference set — neither catastrophic nor confirming.

### 12.5J-E observation worth carrying forward to 12.5K

Seed 1 hit baseline (34/40); seeds 0/2/3/4 sat 1 below (33/40). With std=0.40, the effect is small but present. Possible interpretations:
- **Variance-bound regression** (single hand of the 7 difference-hands flipped between seeds) — the 5-seed sample isn't enough to characterize the model's true expected accuracy. **More seeds (10-20) would tighten this.**
- **True regression** (the new features added bias on average) — would require investigating WHICH hands are flipping between seeds.
- **Hyperparameter mismatch** (existing hypers tuned for 59-surface; 61-surface may benefit from re-tune) — explore in 12.5K.

12.5K design phase should consider all three.

## LEAD-PROGRAMMER — Step: 12.5K combined re-train DESIGN (architect-hat) — fire on this comm merge

Per plan `PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md` table mention "12.5K = combined re-train integrating 12.5I + 12.5J results. Fires AFTER both 12.5I-E and 12.5J-E ship." Both have shipped (12.5I-MW40-VERIFICATION-E + 12.5J-E in this PR resolution). 12.5K is now CLEARED to fire.

Branch: `programmer/phase125k-combined-retrain-design-2026-05-06`. Base: master post-this-comm-merge.

### Scope — design plan comm only (architect-hat; design phase)

This is a DESIGN phase, NOT execution. Mirror 12.5I-A pattern (PLAN_PHASE125I_CORPUS_EXPANSION) and 12.5I-MW40-VERIFICATION-A pattern (PLAN_PHASE125I_MW40_VERIFICATION). Output is a single plan comm; execution is separate -B/-C/-D dispatches.

### What 12.5K design must address (quality-default; slow-steady)

The 12.5J-E empirical finding (mean 33.20/40 ± 0.40 vs baseline 34/40 on solver-corrected) defines 12.5K's challenge: **what's the highest-quality lever to push past baseline?**

Builder authors `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` analyzing all 3 levers:

#### Lever A — More seeds (variance characterization)

- Hypothesis: 5 seeds is too small; true mean may be at-or-above baseline within 1-σ
- Action: 10-20 seed sweep on existing 788-corpus 61-surface + same hypers + same warm-start
- Cost: ~$0; ~30 min wall clock per seed × 10-20 = ~5-10 hours wall clock total
- Pilot-first: 2-seed pilot pass, then scale to remaining
- Expected outcome: tighter mean ± std; if mean ≥ 34/40 within 1-σ, promote; if stays at 33.20 ± 0.40, conclude variance-bound finding
- **Slow-quality reading:** valuable IF cheap; doesn't rule out other levers

#### Lever B — Hyperparameter exploration (CV-driven sweep)

- Hypothesis: existing hyperparameters tuned for 59-surface; 61-surface benefits from re-tune
- Action: structured hyperparameter sweep (n_estimators, max_depth, learning_rate, regularization) on 788-corpus 61-surface; cross-validated on held-out folds (NOT on reference set; reference set is held out for final evaluation)
- Cost: ~$0; ~30 min × dozens of configs × 5 seeds each = ~10-20 hours wall clock
- Pilot-first: 2-3 configs first to validate sweep infrastructure, then full grid
- Expected outcome: best-config training run that's then evaluated on reference set
- Risk: overfitting to held-out folds; reference-set evaluation is the only real signal
- **Slow-quality reading:** valuable IF the sweep includes proper cross-validation discipline; risks over-engineering

#### Lever C — Augmented training data (further labelling rounds)

- Hypothesis: 788-row corpus is undersized for the 5-class 61-feature problem (especially for the rare classes FOLD/CALL = 81 each = 10% of corpus)
- Action: design a NEW labelling round targeting the 4 stay-wrong axes (MW-17, MW-40, MW-45, MW-47) — similar to MW-40-VERIFICATION but for the OTHER stay-wrong hands; or a broader expansion targeting under-represented classes
- Cost: $50-200 LLM (5 sonnet × 50-200 hands); ~2-5 hours wall clock for labelling + Opus tier-up
- Pilot-first: 5-hand pilot per stay-wrong axis, then scale on graduation pattern
- Expected outcome: 850-950 row corpus that has stronger signal on the failing axes
- Risk: if the 4 stay-wrong axes are model-class-blind (like MW-40 turned out to be — broader pattern is BET), more data won't move the needle
- **Slow-quality reading:** valuable IF the empirical evidence shows it CAN move the needle; cost is non-trivial

#### Recommendation framework (architect-hat decides; orchestrator approves on PR review)

Builder's design plan should:
1. Analyze each lever's expected outcome + cost/risk
2. **Recommend a sequenced approach**: which lever first; what gates to next lever; what's the off-ramp if no improvement
3. Cite memory feedback (`feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_findings.md`, etc.)
4. Specify per-lever pilot-first gate threshold + abort condition
5. Estimate total cost + time budget for the lever sequence
6. Acknowledge: 12.5K may produce another null result; the slow-quality default is to TEST levers methodically, not to force a positive outcome

### Methodology rules (standing per 12.5I-A precedent)

- design_action per T-CONTROL not applicable (12.5K is not a labelling phase; no per-hand predictions)
- Cross-seed importance reporting (for any retrain runs, report importance across seeds)
- Cap-binding pre-flight (ref_id namespace if any new corpus rows added)
- Tier-up verification (Sonnet → Opus on any new labelling output per `feedback_pilot_first_for_long_jobs.md` sub-rule)
- Pilot-first (binding for ALL long batches in 12.5K)
- Hero-only convention (if labelling is involved)
- Pre-flight join-cardinality (if new corpus rows added)

### Stop conditions

- Plan diverges from quality-default sequencing (e.g., recommends Lever C BEFORE evaluating Lever A's variance characterization) → STOP, route to orchestrator
- Plan does NOT include pilot-first gates per lever → STOP
- Plan recommends bypassing reference-set held-out evaluation → STOP per `feedback_solver_vs_expert_labels.md` (model performance is observed via reference set, never trained against it)
- Plan recommends solver-as-labels for any new labelling round → STOP
- Plan total budget exceeds ~$300 LLM OR ~30 hours wall clock without explicit orchestrator approval → REPORT (not STOP); surface for orchestrator decision

### What you do NOT do

- Do NOT execute any retrain in this PR (this is design only)
- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source (read-only reference)
- Do NOT modify BATCH2 reference
- Do NOT touch existing 788-corpus or label files
- Do NOT auto-fix the 12.5J-E result (treat as input data; orchestrator-scope to interpret)
- Do NOT recommend a single-lever-only plan (must analyze all 3 levers; can sequence them with gates)

### Cost / time

~$0 (design only; no LLM, no inference). ~45-60 min builder wall clock for the design plan.

### Deliverable scope

1 file in PR diff: `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`

(Optionally a small supporting analysis file in `review/comms/` if Lever B's hyperparameter grid space benefits from a separate breakdown table.)

### Builder report sections (mandatory; in the plan)

- §1 — Recap: 12.5I-MW40-VERIFICATION graduation-fail + 12.5J-E no-promote
- §2 — 12.5K Goal: push past v9-3way-v2.2 baseline (34/40 solver-corrected) to ceiling
- §3 — Lever A analysis (more seeds; variance characterization)
- §4 — Lever B analysis (hyperparameter sweep with CV)
- §5 — Lever C analysis (augmented training data; further labelling)
- §6 — Sequenced recommendation (which lever first; gates; off-ramps)
- §7 — Cost + time budget + pilot-first gates per lever
- §8 — Stop conditions (per dispatch)
- §9 — What this PR does NOT do (per dispatch)
- §10 — Risks + open questions for orchestrator (per `feedback_orchestrator_decides_not_recommends.md`)
- §11 — References

## QC stream — what you audit (when 12.5K design PR opens)

Standalone audit, ~10-15 min, 7-item scope (design-phase format):

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 1 file (+ optional analysis); no drift outside `review/comms/`. Verify NOT touched: v3.x prompts, BATCH2, river-rats-core/, training-data, existing corpora, models.
2. **All 3 levers analyzed** — Lever A (more seeds) + Lever B (hyperparameters) + Lever C (augmented data) each have dedicated analysis section. Single-lever plan = SHOULD_FIX.
3. **Sequenced recommendation present** — plan §6 explicitly sequences levers with gates between them. Single-lever-only or no-sequencing plan = SHOULD_FIX.
4. **Pilot-first gates per lever** — each lever has explicit pilot-first scope (e.g., "2 seeds first, gate, then scale to remaining"). Missing = SHOULD_FIX.
5. **Cost + time budget realistic** — totals match the per-lever sub-totals; budget ≤$300 LLM or surfaces for orchestrator approval.
6. **TC-X-OWNER-SCOPE-DISCIPLINE + solver-as-labels prohibition** — plan does NOT recommend training against reference set, does NOT propose solver-as-labels, does NOT propose BATCH2/v3.x edits.
7. **TC-X-DISPATCH-COMPLIANCE (8th formal exercise)** — design-only (no execution); 1 file; methodology rules cited.

## Why no Opus tier-up on 12.5K design

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs. 12.5K design is architecture / planning. Standard QC PASS suffices.

## Sequencing — what fires after 12.5K design merges

1. **12.5K-A execution dispatch** (specific lever per design plan; orchestrator dispatches based on builder's recommended Lever-A-first sequence) — fires on 12.5K design merge
2. **12.5K-B / -C / -D / -E** (subsequent levers per design plan; each fires on prior lever gate)
3. **12.5L gate evaluation** — fires on 12.5K full sweep complete (all levers tested or off-ramped)

## What's blocked / what's queued

**Cleared by this comm:**
- PR #253 merge (Builder 12.5J-E)
- PR #255 merge (QC verdict record)
- 12.5J-F synthesis rolled in (this comm IS the synthesis comm)
- 12.5K design dispatch fires
- 12.5J workstream effectively closed (all phases shipped or rolled up)

**Newly queued (after 12.5K design merges):**
- 12.5K-A execution (specific lever per design plan)

**Still queued (later):**
- 12.5K-B / -C / -D / -E execution (multi-lever sequence per design)
- 12.5L gate evaluation

**Owner-scope items pending (informational, non-blocking):**
- TC-X-INTRA-PLAN-CONSISTENCY ratification (curative entry #13; class proven via PR #236)
- TC-X-DISPATCH-COMPLIANCE ratification (now 7+ exercises)
- Memory note refresh for "composition quad" vs "composition triple" terminology (NIT-1 carry-forward; surfaced in -E memo)
- "Structural arguments must cross-check against v3.4 DO NOT rules before submission to verification rounds" — process-improvement standing-rule candidate (surfaced from MW-40 -C HALT)
- The 12.5J-E "neutral" result is itself worth memory: feature-engineering work added structural information without measurable accuracy gain at this corpus scale; future feature work should be co-designed with corpus expansion to test signal at sufficient scale

## References

- PR #253 (Builder 12.5J-E small-sample re-train; mean 33.20/40 ± 0.40): branch `programmer/phase125j-e-small-sample-retrain-2026-05-06`
- PR #255 (QC PASS verdict): branch `qc/pr253-125je-retrain-review-2026-05-06`
- PR #254 (QC trigger): master `4e9e5e7`
- PR #252 (orchestrator: 12.5J-E dispatch + 12.5J reconciliation): master `ba678a5`
- PR #248 (orchestrator: -E memo dispatch): master `92e2d85`
- 12.5J master plan: `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-06.md`
- 12.5I master plan: `review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md`
- 12.5I-A design precedent: `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- v9-3way-v2.2 baseline (34/40 solver-corrected): CLAUDE.md project state
- 788-corpus 61-surface (training input): `data/corpus_combined_788_2026-05-06.jsonl` (PR #222 master `48084c3`)
- Memory: `feedback_orchestrator_decides_not_recommends.md` (orchestrator decides under owner direction), `feedback_orchestration_efficiency_rules.md` (synthesis rolled into resolution comm), `feedback_quality_default_no_ask.md` (no-promote acceptance + design phase mandates pilot-first per lever), `feedback_pilot_first_for_long_jobs.md` (binding for all 12.5K execution), `feedback_solver_vs_expert_labels.md` (no solver-as-labels in any 12.5K lever), `feedback_solver_findings.md` (blocker effects sensitivity)

**Status: PR #253 + PR #255 cleared for merge. 12.5J-F synthesis rolled in. LEAD-PROGRAMMER fires 12.5K combined re-train DESIGN (architect-hat) on this comm merge. ~45-60 min wall clock to PR open.**
