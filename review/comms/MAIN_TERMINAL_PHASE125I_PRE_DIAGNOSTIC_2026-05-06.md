---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5I-pre — diagnostic investigation on 5 stay-wrong hands; per-hand E-FEATURE / E-DIST / isomorph classification; gates 12.5I (D) + 12.5J (C) parallel dispatch
status: TRIGGER — fire now
---

# Phase 12.5I-pre — diagnostic investigation

Owner picked **E → C + D parallel** at 12.5H-F gate. 12.5I-pre is the cheap diagnostic step that gates the 3-4 week parallel commit to 12.5I (corpus expansion) + 12.5J (feature engineering).

Goal: per-hand classification on MW-17/25/40/45/47 — for each, determine the dominant residual type (E-FEATURE primary / E-DIST underpowered / isomorph-mismatch / mixed). Output informs which 12.5I templates to expand and which 12.5J features to engineer.

Slow-quality scope: **diagnose before commit**. Cost ~$5 + 4-5 days; produces decision-ready evidence for the parallel directions to follow.

## LEAD-PROGRAMMER — what you do (architect + gto-expert hats combined)

Branch: `programmer/phase125i-pre-diagnostic-2026-05-XX` (XX = your start date)

### Per-hand diagnostic protocol (5 hands × the protocol below)

For each of MW-17, MW-25, MW-40, MW-45, MW-47:

#### Step 1: Read the reference spec

`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` and `BATCH2_8_RANGE_ANALYSIS.md` for the canonical hand definition + GTO reasoning.

#### Step 2: Catalog 12.5H corpus rows targeting this family

Identify which 12.5H templates were designed to teach this hand's pattern. Quote the labels (action + confidence) for each matching row. Flag patterns where corpus labels match the GTO-correct action AND patterns where they don't.

#### Step 3: Model inference walk-through

Load `gto_model_v9_3way_v2.2.json` (current canonical) and produce per-feature importance + activation on the reference hand. Specifically:
- Which features in the 59-surface have non-trivial values for this hand?
- Which top-15 importance features (per 12.5H-E Section C) are activated?
- For the booster's chosen-seed predictions on this hand: what's the confidence margin between the predicted action and the GTO-correct action? (close = tractable; far = structural gap)

#### Step 4: Counterfactual analysis

Construct 2-3 small perturbations of the hand (e.g., change one card; tweak villain range; remove blocker). Note which perturbations flip the prediction.

If small perturbations flip the prediction → **E-DIST underpowered** (model HAS the relevant features but doesn't generalize from training distribution to this specific spec)

If no perturbations flip but a feature ablation (zeroing out a feature like `nut_flush_block`) significantly changes prediction confidence → **E-FEATURE primary** (the relevant feature exists in the surface but isn't strong enough OR a needed feature is missing)

If neither applies → **isomorph-mismatch** (the corpus templates aren't structurally close enough to this reference hand; design defect)

#### Step 5: Classify and record

Per-hand verdict: E-FEATURE / E-DIST / isomorph-mismatch / mixed (state primary + secondary). Recommend specific 12.5I or 12.5J actions:
- E-FEATURE primary → 12.5J feature: which new feature(s) would address this; rough scope estimate
- E-DIST underpowered → 12.5I corpus: which template family to expand from N hands to ~30-40; specific spec changes if needed
- isomorph-mismatch → 12.5I' redesign: specific template restructure
- mixed → both 12.5I + 12.5J actions

### Deliverable scope (PR diff)

Exactly **2 files**:

1. `review/comms/BUILDER_REPORT_PHASE125I_PRE_DIAGNOSTIC_2026-05-XX.md` — diagnostic report with per-hand verdicts + 12.5I + 12.5J recommendations
2. (Optional) `scripts/diagnostic_125i_pre.py` — analysis script if Step 3/4 require code (not required if doable in-comm)

No changes to `river-rats-core/`. No new training runs (use existing v9-3way-v2.2 model artifact). No corpus or label changes.

### Stop conditions

- Diagnostic ambiguous on >1 hand (i.e., can't classify dominant residual) → STOP, route to orchestrator
- Counterfactual analysis requires re-training (Step 4 should NOT need it) → STOP
- Diff scope > 2 files → STOP
- Solver call appears anywhere → STOP per `feedback_solver_vs_expert_labels.md`

### What you do NOT do

- Do NOT run trainer (existing model artifact is sufficient for inference)
- Do NOT modify corpus, labels, or prompts
- Do NOT make recommendations beyond the 5 hands' classification + 12.5I/12.5J spec hints
- Do NOT decide whether owner picks 12.5I or 12.5J (orchestrator will dispatch parallel after diagnostic)

## QC stream — what you audit (when 12.5I-pre PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

When triggered (3 audits — analysis-only):

1. **Diff scope** — exactly 1-2 files; analysis-only; no `river-rats-core/` touches
2. **Citation existence** — every file:line in diagnostic report exists at master HEAD
3. **NEW: Per-hand verdict completeness** — verify all 5 hands classified with primary residual type + supporting evidence (Step 3 importance + Step 4 counterfactual at minimum)

Post `REVIEW_QC_PHASE125I_PRE_DIAGNOSTIC_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER (architect + gto-expert hats) runs per-hand diagnostic protocol
2. Step 1-5 per hand × 5 hands
3. Authoring builder report with per-hand verdicts + 12.5I + 12.5J spec hints
4. PR opens
5. Orchestrator posts QC audit-now trigger
6. Standalone QC audit
7. **On QC APPROVE: orchestrator dispatches 12.5I (corpus expansion) + 12.5J (feature engineering) IN PARALLEL** based on diagnostic verdicts:
   - Hands diagnosed E-DIST underpowered → 12.5I template expansion
   - Hands diagnosed E-FEATURE primary → 12.5J feature engineering
   - Hands diagnosed isomorph-mismatch → 12.5I' template redesign (sub-direction of D)
   - Hands diagnosed mixed → both parallel dispatches address the hand

## What's blocked / what's queued

**Blocked:**
- 12.5I-pre PR opens → on builder diagnostic + report
- 12.5I-pre QC trigger → on PR open
- 12.5I-pre merge → on QC APPROVE
- **12.5I (D) + 12.5J (C) parallel dispatch → on 12.5I-pre merge**

**Queued (post-12.5I-pre):**
- 12.5I corpus expansion: target N hands per template per E-DIST diagnosed hands
- 12.5J feature engineering: new features beyond 59-surface per E-FEATURE diagnosed hands; cascade through `feedback_attention_flags_when_features_change.md` (raw + attention vocab + prompt + capture + trainer)
- Both 12.5I and 12.5J ship into a combined 12.5K (final re-train) when both deliver
- 12.5K gate evaluation: median ≥33 = PROMOTE

## Methodology lesson

This is the FIRST time the project explicitly diagnoses before committing 2-3 weeks of work. Prior cycles (12.5C-D-D'/E/G/H) repeatedly committed to corpus expansion or hyperparameter tuning based on prior-cycle predictions that under-delivered. 12.5I-pre breaks that pattern: $5 + 4-5 days of analysis informs the 6-7 weeks of D + C parallel work. If diagnostic surprises owner (e.g., reveals MW-25/40/45 are also E-FEATURE not E-DIST, or that all 5 are isomorph-mismatch), owner can pivot before committing.

This pattern is the per-hand version of the pilot-first rule (`feedback_pilot_first_for_long_jobs.md`). The diagnostic IS the pilot for the C+D parallel commit.

## References

- 12.5H-F synthesis: master `ea642ed` (PR #191)
- 12.5H-E re-train: master `283af91` (PR #188)
- Reference set: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- Current canonical model: `river-rats-core/models/gto_model_v9_3way_v2.2.json`
- 12.5C blueprint trainer module: `river-rats-core/train_model_v9_student.py` (master `f5472bc` post-12.5G parameterization)
- Memory: `feedback_pilot_first_for_long_jobs.md` (12.5I-pre IS the pilot for D+C), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md` (slow-quality default), `feedback_orchestrator_decides_not_recommends.md`, `feedback_river_rats_team_structure.md` (analyst hat = builder), `feedback_solver_vs_expert_labels.md`

**Status: 12.5I-pre TRIGGER posted. LEAD-PROGRAMMER analyst hat runs per-hand diagnostic. After QC APPROVE: 12.5I (D) + 12.5J (C) parallel dispatch.**
