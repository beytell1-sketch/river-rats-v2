---
date: 2026-05-10
from: Main terminal (orchestrator; owner re-engaged)
to: LEAD-PROGRAMMER (architect-hat with ml-architect-hat consult; gto-expert-hat for solver-aligned bet sizing) — third fire-now re-poke + STOP-surfacing demand
status: TRIGGER + STOP-SURFACING DEMAND — fire NOW or surface BLOCKED diagnostic within 2h
---

# LEAD-PROGRAMMER — third fire-now re-poke + STOP-surfacing demand: Phase 1.5-D.1

This is the **third explicit fire-now directive** for Phase 1.5-D.1 (HU reference set design). Prior actions:
- **Dispatch**: PR #325 merged at master `fab6c4c` ~12.5h ago (2026-05-09 11:30 SAST) — `MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md`
- **Re-poke #1**: PR #326 merged at master `bdfe381` ~11h ago (2026-05-09 13:05 SAST) — `MAIN_TERMINAL_BUILDER_FIRE_NOW_REPOKE_PHASE15D1_2026-05-09.md`
- **Re-poke #2 (this comm)**: requires either firing OR diagnostic comm within 2h

State observed at master `bdfe381`:
- No `programmer/phase15d1-*` branch on origin
- No diagnostic comm in `review/comms/`
- No commits since `bdfe381` (re-poke merge)

Per CLAUDE.md §5 ("Stop Conditions — NEVER Improvise"): if builder cannot proceed, **STOP and write a diagnostic comm**. Silence is not acceptable when explicitly addressed by orchestrator directive (per `feedback_explicit_action_trigger.md`, `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`).

Owner has re-engaged after autonomous overnight period. Builder silence past two prior fire-nows must resolve to one of two states within **2h wall-clock from this comm's merge**:

## Required outcome (one of two)

### Option A — Fire NOW

Author Phase 1.5-D.1 per the binding spec already in master:

- **Dispatch comm**: `review/comms/MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md`
- **Architect's design memo §4.2**: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- **Branch**: `programmer/phase15d1-hu-reference-set-design-2026-05-10` rooted at current master
- **Scope**: 30 spots × 6 axes; 3 close + 2 canonical per axis; solver-aligned bet sizes; close-hand-anchor `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (α=β decided)
- **Team**: 6 design agents in parallel + 1 reviewer
- **Methodology rules** (memory): `feedback_close_hand_selection.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_pilot_first_for_long_jobs.md`

### Option B — Surface BLOCKED diagnostic comm

If you cannot fire (environment issue, tool failure, unclear spec, missing dependency, anything), write a diagnostic comm in `review/comms/` titled `BUILDER_DIAGNOSTIC_PHASE15D1_BLOCKED_2026-05-10.md` containing:

1. **Concrete blocker**: what specifically prevents firing (error messages, missing files, tool failures, ambiguous spec lines — with file:line citations)
2. **Verification trail**: what you ran (`git log`, `git ls-files`, `python -c '...'`, etc.) + actual output
3. **Spec confusion (if any)**: which design memo §4.2 line is ambiguous; what interpretations are possible
4. **Environment snapshot**: `which python`, `python --version`, `git --version`, working directory
5. **Asks of orchestrator**: what would unblock you (clarification, scope expansion authorization, environment fix)

## What "silent for 2 more hours" means

If neither A nor B occurs within 2h of this comm's merge, the operational interpretation is: **builder Claude session is non-functional** (hung, closed, or unable to read master). Owner has been informed and will manually restart the builder terminal.

This is NOT an authorization for orchestrator to take over building (per owner's prior instruction "the solution is not to take over building"). It is an operational acknowledgment that further re-pokes from orchestrator are pure process drift, and the unblock is owner-action (terminal restart), not directive content.

## Loop owner — informational

Owner has re-engaged. Standing directive remains: orchestrator decides; quality default; merge orchestrator dispatch + QC PASS PRs autonomously. After 1.5-D.1 PR opens (Option A), orchestrator fires QC trigger autonomously; on QC PASS, orchestrator merges PR + verdict autonomously; then dispatches Phase 1.5-D.2 (HU labelling pipeline; pilot 5 → Sonnet→Opus tier-up gate → full 25) per design memo §4.3.

If Option B occurs, orchestrator triages the diagnostic + surfaces synthesis to owner.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at branch creation: MATCH `bdfe381` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.1 dispatch: `MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md` (master `fab6c4c`, PR #325)
- Re-poke #1: `MAIN_TERMINAL_BUILDER_FIRE_NOW_REPOKE_PHASE15D1_2026-05-09.md` (master `bdfe381`, PR #326)
- 1.5-A architect design memo §4.2 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- 1.5-C merged: master `d3c3da0` (PR #322); QC verdict: `b4caf38` (PR #324; PASS · 0/0/0)
- 988-on-59 corpus: `data/corpus_combined_988_on_59_2026-05-09.jsonl` + labels
- Canonical close-hand-anchor: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`
- 1.5-C re-poke precedent: PR #321 → PR #322 successful pickup in <2h
- Memory: CLAUDE.md §5 (STOP conditions), `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`

---

**Status: LEAD-PROGRAMMER — third fire-now + STOP-surfacing demand. 2h budget from this comm's merge: Option A (fire) OR Option B (BLOCKED diagnostic comm). Silence past 2h = operational session-down; owner restarts builder terminal manually.**
