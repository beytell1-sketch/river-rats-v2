---
date: 2026-05-08
from: Main terminal (orchestrator)
to: QC stream
re: PR #307 — Phase 1.5-A architect-hat unified-59-surface workstream design memo — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #307

PR #307: `programmer/phase15a-unified-surface-design-2026-05-08`. Head `6164f14a6a98c3ec09ace3d0c624da6c558eb519`. Builder fired Phase 1.5-A per dispatch `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306).

Milestone-class PR (architect-hat design memo for the entire unified-59 workstream — design lock that constrains Phase 1.5-B/C/D/E execution sub-phases) → pre-merge QC required per `feedback_qc_required_before_approval.md`.

## Audit scope (expanded; ~20-30 min wall-clock — NOT 10-15)

QC heads-up on PR #307 received: this audit is bigger than the SHIP-A 7-item template because the dispatch self-bound the memo to 5 design areas + falsifiable predictions + binding TC-23 EXISTENCE on every cited file:function. Trigger ratifies the expanded scope.

### Items 1-7 (per dispatch §"QC stream — what you audit")

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 2 PR files (`PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` + `BUILDER_REPORT_PHASE15A_2026-05-08.md`); no source/prompt/data/model edits.
2. **All 5 design areas covered as committed paths** (NO open technical questions): 59-surface canonical / drop-2-J-B-features migration / 3-way verification at 59 / HU re-train cascade / cost-time forecast. If any design area contains "open question of technical type" — FLAG SHOULD_FIX.
3. **TC-23 EXISTENCE grep-loop on every cited file:function**: forward-binding to current master `5863f13` (dispatch said `e66e2e6`; master has advanced by PR #306 merge — same content for all source paths; QC verifies at current tip). Every cited path / function / file referenced by the memo must exist at master `5863f13`.
4. **Pilot-first binding gates** per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: every long batch in the design has a pilot+full split with explicit binding gate. Specifically check: HU reference set design + HU labelling + 3-way 59-surface retrain + HU 59-surface retrain. Sub-rule: training-data outputs require Sonnet → Opus tier-up cross-check.
5. **Methodology rule cross-check**: each rule explicitly addressed in the memo's HU section + relevant design areas:
   - `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150)
   - `feedback_solver_vs_expert_labels.md` (solver verifies/researches only; never labels)
   - `feedback_bucket_first_labelling.md` (no equity thresholds in labelling prompt; thresholds in coaching/spot_classifier.py)
   - `feedback_terminology_raise_vs_bet.md` (raise = raise of existing bet; bet = first postflop bet; open = preflop opener)
   - `feedback_attention_flags_when_features_change.md` (feature changes REQUIRE attention vocab + prompt rules + capture + trainer touch-points named)
   - `feedback_failure_direction_classification.md` (per-hand miss classification: under-aggress / over-aggress / class-collapse)
   - `feedback_preflop_geometry_vs_postflop_composition.md` (postflop strength from TP+/draws/air composition triple)
   - `feedback_close_hand_selection.md` (close spots = model uncertainty + poker difficulty)
6. **TC-X-DISPATCH-PREDICTION-VERIFICATION**: ≥ 3 falsifiable predictions present (heads-up says memo has 7 — verify each is actually falsifiable, i.e., specifies a concrete observable outcome that could be empirically invalidated, not a tautology or untestable claim).
7. **TC-X-OWNER-SCOPE-DISCIPLINE** (21st formal use; durable): 6 mandatory negative-scope items held (no source/data/model/prompt edits; no D5 execution; no `project_v9_3way_ceiling.md` pre-emption; no open technical questions). 3 owner-scope items per heads-up should be flagged AS owner-scope and NOT silently committed.

### Additional items (per QC heads-up; expanded scope)

8. **Per-design-area dispatch-compliance**: each of the 5 areas matches the dispatch's per-area requirements (architect named every file path for area 1; determinism verification command for area 2; warm-start strategy committed for area 3; HU-on-59 ship-gate parity metric committed for area 4; Phase 1.5-B/C/D/E sub-phase decomposition for area 5).
9. **Single-committed-path verification**: scan for "Option A vs Option B", "either … or …", "TBD", "open question" patterns. Architect commits → singular, with reasoning. (Genuine owner-scope trade-offs flagged AS owner-scope are exempt.)
10. **3-owner-scope-item separation check** (per QC heads-up): the 3 owner-scope items present in the memo are genuinely owner-scope (not technical choices the architect punted) and are clearly separated from the architect's committed decisions.
11. **Per-prediction falsifiability check** (per QC heads-up): each of the 7 predictions specifies an observable that could fail (e.g., "3-way at 59 will hold ≥ 33.00 mean" is falsifiable; "the workstream will succeed" is not).

## Critical audit emphasis

This is the FIRST design lock for the Phase 1.5 workstream. Every Phase 1.5-B/C/D/E execution sub-phase will reference back to this memo. QC verifies:

- **Single committed path is intact** — execution sub-phases must be unambiguously navigable from this memo without architect having to revisit decisions
- **TC-23 EXISTENCE strict** — if architect cites a file:function path that doesn't exist, downstream sub-phases will TC-23-FAIL on the cascade
- **Pilot-first BINDING** — HU labelling is the largest pilot-first gate in the workstream; if binding language is loose, pilot will run as full-scale by accident
- **Methodology rules carried forward** — solver-aligned sizing, terminology, bucket-first, attention-on-feature-change must all be present; their absence at design lock = absence at execution

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-30 min (per QC heads-up). QC writes:
- `~/river-rats-qc/findings/2026-05-08-pr307-phase15a-design.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15A_DESIGN_2026-05-08.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` per `project_qc_heartbeat_convention.md`

## What gates

- PR #307 merge → on QC PASS + owner explicit `fire now` per going-forward rule (orchestrator does not merge milestone PRs without owner authorization, even on QC PASS)
- After PR #307 + QC verdict comm merge → orchestrator dispatches Phase 1.5-B execution sub-phase per architect's chosen first execution step (drafted on receipt of architect's design)
- LOOP CONTINUES through 1.5-A merge → 1.5-B execution dispatch

## References

- Phase 1.5-A dispatch: `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306)
- Phase 1.5 queue + retrain-ordering pre-commitment: `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302)
- 12.5L SHIP-A: master `dceb265` (PR #303); QC PASS at master `e66e2e6` (PR #305)
- D5 deferred blueprint: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (in master via PR #303)
- Project memory (owner-ratified): `project_v9_3way_ceiling.md`
- Memory rules: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `project_qc_heartbeat_convention.md`, all methodology rules cited under item 5.

**Status: QC stream — fire now on PR #307. ~20-30 min (expanded scope per QC heads-up). Pre-merge QC for milestone-class design lock. Heartbeat sync to current master `5863f13` at end of tick.**
