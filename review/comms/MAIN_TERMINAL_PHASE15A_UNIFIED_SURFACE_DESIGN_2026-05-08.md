---
date: 2026-05-08
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (architect-hat) · QC stream (FYI; standalone audit on PR open) · Owner (notice; ratifies sub-phase execution dispatches)
re: Phase 1.5-A — unified-59-surface workstream DESIGN dispatch (architect-hat memo; design only, no execution)
status: DIRECTIVE — fires LEAD-PROGRAMMER architect-hat — fire now
---

# Phase 1.5-A — unified-59-surface design dispatch

## Context (state at this dispatch)

PR #303 (12.5L-SHIP-A) merged at master `dceb265`. PR #305 (QC PASS verdict) merged at master `e66e2e6`. Phase 1 INTERIM v9-3way-v2.2 production lock recorded. 12.5K experiment closed at 3-lever ceiling 33.00/40 ± 0.00 on 988-corpus / 61-surface. D5 blueprint (`PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`) deferred to Phase 2 — fires post Phase 1.5 ship.

Phase 1.5 was queued at PR #302 (`MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md`, master `a382fa2`) per owner directive surfaced in PR #300 (`BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md`, master `48297e4`). Owner-scope decisions made at PR #302:

1. Single committed path: unified-59-surface workstream IS the next-phase commitment (not a menu against D5; D5 stays Phase 2 deferred).
2. Surface canonical: 59 features = current 61-experimental MINUS 2 J-B features (`nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`). Both 12.5J-B feature additions targeted MW-17 / MW-47 axes; both remained on stay-wrong list through 12.5K; importance below 1% drop threshold on chosen seed.
3. Retrain-ordering pre-commitment: HU first → 3-way verification → router/coaching alignment.
4. Coaching-pipeline rationale: feature-grounded narrative consistency requires ONE feature surface across HU + 3-way + (future) 4-way + 5-way.

This dispatch fires Phase 1.5-A as the FIRST sub-phase of the workstream: an architect-hat DESIGN memo only. Execution sub-phases (Phase 1.5-B/C/D/...) will be dispatched separately AFTER this design ships and owner ratifies.

## LEAD-PROGRAMMER (architect-hat) — fire now

You are authorized to fire Phase 1.5-A as a single DESIGN PR. No source/data/model/prompt edits in this branch — design memo only. ~$0 LLM spend; ~60-90 min wall-clock estimate to PR open. Architect-hat persona dispatches per the project's standard pattern (gto-expert + ml-architect + architect agents per `docs/PROCESS_GUIDE.md` §1.1; orchestrator-scope reminder, not a menu).

### Single deliverable (one file in PR diff)

`review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` — architect-hat design memo.

(Plus the matching `review/comms/BUILDER_REPORT_PHASE15A_2026-05-08.md` builder-report comm. 2 files total in PR; no other changes.)

### Memo scope (5 design areas; ALL must be covered as committed paths, not menus)

Per the queued spec at PR #302 §"After SHIP-A merge → Phase 1.5-A dispatch fires", expanded with binding constraints below:

**1. 59-surface canonical**
- Enumerate the 59 features: name + computation pointer (file:function) + axis-of-targeting (HU / 3-way / 4-way / shared) + chosen-seed importance from PR #293 §"Section C — Gate 2.3".
- Confirm `nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index` are the 2 dropped (per `BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md`); cite line refs in `feature_extractor.py` + `feature_keys.py` for what's removed.
- Per `feedback_attention_flags_when_features_change.md`: list the matching attention-vocab + prompt-rules + capture + trainer touch-points that the execution sub-phase MUST update in lock-step. Architect names every file path (no hand-waving).
- TC-23 EXISTENCE pre-commitment: every cited path must exist at master HEAD `e66e2e6`. Architect verifies before PR.

**2. Drop-2-J-B-features migration (988-corpus re-extract to 59)**
- Re-extraction protocol: which composite ops on `assemble_v23.py` / `extract_features_parallel.py` carry through; which require code change vs schema change vs both.
- Determinism guarantee: re-extracted 59-surface 988-corpus must bit-equal a re-extraction of 988-corpus then column-drop, modulo the 2 dropped columns. Architect specifies the verification command.
- Invariant tests re-baseline: which tests in `check_leakage.py` + `train_v2_3_clean.py` need surface-size update.
- Output: a `corpus-988-on-59-surface` artifact path + size + checksum spec. Single committed path: re-extract from raw situations (NOT column-drop), per `feedback_solver_findings.md` quality discipline.

**3. 3-way verification at 59-surface**
- Re-train v9-3way analog on 988-on-59-surface; pre-commitment: PASS gate is mean ≥ 33.00/40 across N seeds (architect picks N with reasoning; default to 5-seed per PR #293 precedent).
- Hyperparameters: warm-start strategy (warm-start from v9-3way-v2.2 weights at 45-feat is dimension-mismatched → architect commits to from-scratch OR a specified projection scheme with reasoning, NOT a menu).
- Failure modes: if 3-way at 59 < 33.00/40 mean, what does that prove? Architect specifies HALT/PROCEED/REPORT decision matrix per `feedback_pilot_first_for_long_jobs.md`.
- Per `feedback_orchestrator_decides_not_recommends.md`: this is HOW (architect-scope), not WHETHER (owner-scope).

**4. HU re-train cascade (v8 38-feat → vNext-HU 59-feat)**
- HU reference set design: ~30-40 HU postflop spots per the multiway BATCH2 design pattern (`design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`); ≥ 2 design agents + 1 reviewer per `docs/PROCESS_GUIDE.md` §1.2.
- HU labelling protocol: 5-labeller v3.4 consensus per the locked Stage 4 plan; PROCESS_GUIDE §2.1 calibration discipline (BLIND exam, ≥ 20/24 + 3 GTO-reversal hands correct, agent must NOT have access to `calibration_exam.py` or any answer key).
- HU corpus assembly: analogous to 988-corpus pipeline (situation gen → labelling → consensus → solver verification on disagreements). Pilot+full split MANDATORY per `feedback_pilot_first_for_long_jobs.md` STANDING RULE — pilot is binding gate for full corpus dispatch.
- Solver-aligned bet sizes per `feedback_solver_aligned_sizing.md`: flop 25%/66%, turn 33%/75%, river 33%/75%/150%. Architect explicitly notes adoption.
- Terminology compliance per `feedback_terminology_raise_vs_bet.md`: raise = raise of existing bet; bet = first postflop bet; open = preflop opener. Architect spot-checks HU spot specs.
- Solver vs labels per `feedback_solver_vs_expert_labels.md`: solver verifies/researches only, NEVER as training labels.
- Bucket-first per `feedback_bucket_first_labelling.md`: no equity thresholds in labelling prompt; thresholds in `spot_classifier.py`.
- HU model retrain: warm-start strategy from v8-HU-38-feat OR from-scratch OR projection (architect commits to ONE with reasoning); ≥ 5-seed; per-hand stay-wrong tracking analogous to 3-way.
- Pre-commitment: ship gate is HU-on-59-surface ≥ v8-HU-on-38-surface aggregate parity (architect specifies the parity metric — PokerBench 88.1% baseline OR per-hand canonical match rate, with reasoning for which one is load-bearing).

**5. Cost/time forecast for the full unified-59 workstream**
- Decompose into Phase 1.5-B/C/D/E sub-phases (architect commits to specific decomposition).
- Per sub-phase: $$, wall-clock, dependencies, BINDING pilot gates per `feedback_pilot_first_for_long_jobs.md`, HALT conditions, off-ramps.
- Aggregate: total $$ + total wall-clock + critical path.
- Sequencing pre-commitment from PR #302 (HU first → 3-way verification → router/coaching alignment) constrains design — architect designs WITHIN this ordering, not outside it.

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: every technical choice is a commitment with reasoning, NOT a menu of options for owner. "Open questions" of technical type in this memo = architect failed; will be sent back. (Genuine owner-scope trade-offs — e.g., "expand HU corpus to 200 hands vs 300 hands" — ARE acceptable as owner-decisions and may be flagged AS owner-scope.)
- **Pilot-first** per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: every long batch in the workstream has a pilot+full split with explicit binding gate. Sub-rule: training-data outputs require Sonnet → Opus tier-up cross-check.
- **No deadlines** per `feedback_no_deadlines.md`: forecasts are estimates; quality path beats schedule.
- **Spec vs infrastructure** per `feedback_spec_vs_infrastructure_code_drift.md`: every cited code path / file / function MUST exist at master HEAD `e66e2e6`. TC-23 CONTENT + EXISTENCE will be QC'd.
- **TC-X-DISPATCH-PREDICTION-VERIFICATION** pre-commitment: architect lists ≥ 3 falsifiable predictions about what will / will not happen in execution sub-phases (e.g., "3-way at 59 will hold ≥ 33.00 mean"; "v8-HU-on-38 will not match HU-on-59 on > 5/30 reference hands"; etc.). Used by QC to retrospectively verify dispatch-compliance.
- **Failure-direction classification** per `feedback_failure_direction_classification.md`: HU and 3-way verification reports MUST classify per-hand misses by direction (under-aggress / over-aggress / class-collapse). Architect specifies the report format.
- **Postflop strength composition** per `feedback_preflop_geometry_vs_postflop_composition.md`: HU postflop spot strength derives from TP+/draws/air composition triple, not preflop range labels. Architect honors when designing HU spots.
- **Close-hand selection** per `feedback_close_hand_selection.md`: HU reference set close spots = model uncertainty + poker difficulty, not feature stats.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT execute any feature drop, corpus re-extract, retrain, or HU labelling — DESIGN ONLY.
- ❌ Does NOT modify `feature_extractor.py` / `feature_keys.py` / any river-rats-core source — design memo cites paths but does not edit.
- ❌ Does NOT modify v3.x prompts / BATCH2 / 988-corpus / model files / 40-hand reference set.
- ❌ Does NOT execute D5 (deferred to Phase 2; blueprint exists at `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`).
- ❌ Does NOT pre-empt owner ratification of `project_v9_3way_ceiling.md` memory entries (independent owner-gate; not blocking this design).
- ❌ Does NOT include "open technical questions" — architect commits to recommendations per `feedback_quality_default_no_ask.md`.

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

Routing per `feedback_qc_routing_when_standalone_active.md`: QC stream (~/river-rats-qc/) handles audit; do NOT spawn parallel subagent.

Pre-merge QC required per `feedback_qc_required_before_approval.md` (Phase 1.5-A is the design lock for the entire 1.5 workstream — milestone-class).

7-item audit:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 2 PR files; no source/prompt/data/model edits.
2. **5 design areas all covered as committed paths**: 59-surface canonical / drop-2-J-B migration / 3-way verification / HU re-train cascade / cost-time forecast — NO open technical questions; if found, FLAG SHOULD_FIX.
3. **TC-23 EXISTENCE on every cited path**: every file/function/path referenced by the memo exists at master `e66e2e6`.
4. **Pilot-first binding gates** per `feedback_pilot_first_for_long_jobs.md`: every long batch in the design has a pilot+full split with explicit binding gate. Specifically: HU reference set, HU labelling, 3-way 59 retrain, HU 59 retrain.
5. **Methodology rule cross-check** per `feedback_solver_aligned_sizing.md` + `feedback_solver_vs_expert_labels.md` + `feedback_bucket_first_labelling.md` + `feedback_terminology_raise_vs_bet.md` + `feedback_attention_flags_when_features_change.md`: each rule explicitly addressed in HU section.
6. **TC-X-DISPATCH-PREDICTION-VERIFICATION**: ≥ 3 falsifiable predictions present in memo (per dispatch above).
7. **TC-X-OWNER-SCOPE-DISCIPLINE** (21st formal use): all 6 negative-scope items (above) held; owner-scope flags only on genuine owner trade-offs.

QC writes finding to `~/river-rats-qc/findings/2026-05-08-pr<n>-phase15a-design.md` + cross-posts `review/comms/REVIEW_QC_PHASE15A_DESIGN_2026-05-08.md`. Updates heartbeat `~/river-rats-qc/.last_seen_master_sha` per `project_qc_heartbeat_convention.md`.

## Owner — what you gate

Two independent gates surfaced now, neither blocks Phase 1.5-A authorship:

1. **Phase 1.5-A merge gate** (after QC PASS) — owner approves merge with explicit `fire now` per `feedback_explicit_action_trigger.md`. Orchestrator does NOT merge milestone PRs without explicit owner authorization.
2. **`project_v9_3way_ceiling.md` memory ratification** — SHIP-A Deliverable 2; owner-scope per `feedback_orchestrator_decides_not_recommends.md`. Owner ratifies entries (or amends). Independent of Phase 1.5-A; can happen in parallel.

After Phase 1.5-A merges, Phase 1.5-B execution sub-phase dispatch fires (architect's chosen first execution step — likely either "feature-prune mechanical" or "HU reference set design" depending on the architect's committed sequencing within the PR #302 retrain-ordering). Owner gates each execution sub-phase fire.

## Loop status

Loop CONTINUES through Phase 1.5-A authorship + QC + merge + Phase 1.5-B dispatch. Loop HOLDS only on owner gates (Phase 1.5-A merge; sub-phase fires; memory ratification).

If owner directs different sequencing on session resume, orchestrator pivots.

## What's blocked / what's queued

**Cleared by this dispatch:**
- LEAD-PROGRAMMER architect-hat fires Phase 1.5-A (was queued; now firing).

**Newly queued (post Phase 1.5-A merge):**
- Phase 1.5-B execution sub-phase dispatch (architect's chosen first execution step; orchestrator drafts on receipt of architect's design).

**Held independently (not blocking Phase 1.5-A):**
- `project_v9_3way_ceiling.md` ratification (owner-scope).

**Re-queued (post Phase 1.5 ship):**
- Phase 2 D5 (blueprint at `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`); fires post Phase 1.5 ship; D5 builds on unified-59 base per PR #302 amendment.

## References

- Phase 1.5 queue + retrain-ordering pre-commitment: `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302).
- Builder directive-receipt (owner's verbatim directive + builder's parsed reading): `BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md` (master `48297e4`, PR #300).
- 12.5L SHIP-A: master `dceb265` (PR #303); QC PASS at master `e66e2e6` (PR #305).
- 12.5L synthesis (3-lever ceiling): `PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297).
- D5 blueprint (deferred Phase 2): `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (in master via PR #303).
- Project memory: `project_v9_3way_ceiling.md` (owner-scope ratification pending).
- 12.5J-B feature implementation (the 2 features being dropped): `BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md`.
- 12.5K-C-E corpus + 5-seed: `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (master `62814a3`, PR #293).
- PROCESS_GUIDE: `docs/PROCESS_GUIDE.md` (calibration discipline §2.1; agent batch sizes §1.1; minimum agent counts §1.2; experts-recommend-owner-decides-scope §1.4).
- Memory feedback rules cited above: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_attention_flags_when_features_change.md`, `feedback_solver_aligned_sizing.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_failure_direction_classification.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_close_hand_selection.md`, `feedback_solver_findings.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `project_qc_heartbeat_convention.md`.

---

**Status: LEAD-PROGRAMMER (architect-hat) fires Phase 1.5-A on this comm merge. DESIGN ONLY; ~$0; ~60-90 min wall-clock to PR open. QC standalone audit on PR open. Owner gates Phase 1.5-A merge with explicit `fire now`. Loop CONTINUES through 1.5-A → 1.5-B execution dispatch (drafted by orchestrator on receipt of architect's design).**
