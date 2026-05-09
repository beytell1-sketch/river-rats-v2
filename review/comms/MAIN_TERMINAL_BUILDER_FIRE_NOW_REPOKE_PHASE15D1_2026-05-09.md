---
date: 2026-05-09
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat with ml-architect-hat consult; gto-expert-hat for solver-aligned bet sizing) — fire-now re-poke
status: TRIGGER — fire NOW on Phase 1.5-D.1 (HU reference set design)
---

# LEAD-PROGRAMMER — fire NOW: Phase 1.5-D.1 (HU reference set design)

This is an explicit fire-now re-poke. The Phase 1.5-D.1 dispatch landed in master at `fab6c4c` via PR #325 (`MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md`) ~93 min ago. Original architect-hat estimate was 60-90 min wall-clock. No `programmer/phase15d1-*` branch on origin; no diagnostic comm. Builder past upper bound of expected ETA.

Per `feedback_named_author_builds_not_polls.md`: named author of active directive AUTHORS, not polls. Per `feedback_listen_to_orchestrator_always.md`: orchestrator MAIN_TERMINAL_* directive addressed to builder by name = sufficient authorization. Per `feedback_explicit_action_trigger.md`: each action requires explicit `MAIN_TERMINAL_* — fire now` directive naming the party + PR/commit. **All conditions satisfied.** Per PR #321 precedent (1.5-C re-poke, which preceded successful builder pickup → PR #322 PASS in <2h).

## Re-poke directive

**LEAD-PROGRAMMER (architect-hat with ml-architect-hat consult; gto-expert-hat for solver-aligned sizing): fire Phase 1.5-D.1 NOW** per the binding spec already in master:

- **Dispatch comm**: `review/comms/MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md` (master `fab6c4c`, PR #325)
- **Architect's design memo §4.2** (binding spec for HU reference set): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (in master since 1.5-A merge)
- **Branch to author on**: `programmer/phase15d1-hu-reference-set-design-2026-05-09` rooted at master `fab6c4c`. (No origin branch yet; create new.)
- **α=β resolution applied**: close-hand-anchor on `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (canonical 1.5-C output, force-added per `feedback_tc23_existence_must_be_git_tracked.md`).
- **Scope**: 30 spots × 6 axes (HU-1 through HU-6); 3 close + 2 canonical per axis; solver-aligned bet sizes per `feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river 33%/75%/150%).
- **Team**: 6 design agents in parallel + 1 reviewer.
- **Methodology**: per `feedback_close_hand_selection.md` (close = model uncertainty + poker difficulty, not feature stats); per `feedback_preflop_geometry_vs_postflop_composition.md` (postflop strength from TP+/draws/air composition triple); per `feedback_terminology_raise_vs_bet.md`; per `feedback_solver_vs_expert_labels.md` (solver verifies/researches only; NEVER training labels).

## What to do on next builder tick

1. `git fetch origin && git checkout master && git pull --ff-only origin master`
2. Verify master tip: should be at-or-after `fab6c4c` (PR #325 1.5-D.1 dispatch merged + this re-poke if it lands first).
3. Read PR #325 dispatch comm + design memo §4.2 (already in master).
4. Author 1.5-D.1 per dispatch §"6 design agents + 1 reviewer" sequence + STOP-condition discipline + verify-own-output.
5. Open PR with deliverables (HU reference set spec + per-spot rationale + solver-verification table per design memo §4.2).

## STOP conditions (per CLAUDE.md §5)

If any of these arise, STOP and write a diagnostic comm — do NOT improvise:
- `v9_3way_v22_on_59.json` not git-tracked (verify per `feedback_tc23_existence_must_be_git_tracked.md`: `git ls-files river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` returns non-empty)
- 988-on-59 corpus jsonl files not at expected paths
- Solver output cannot reproduce sizing axes (NOT improvise; consult gto-expert-hat)
- Design agent disagreement on close-hand selection >50% (architect-hat reviewer adjudicates, NOT improvise)
- Any condition not covered by the dispatch + design memo

If you hit a STOP, surface to orchestrator via diagnostic comm in `review/comms/`. Do not fix-forward without orchestrator authorization. Per Path α precedent (PR #316), orchestrator authorizes scope-expansion when needed.

## Loop owner — informational

Standing directive while owner asleep: orchestrator decides; quality default; no rush; merge orchestrator dispatch + QC PASS PRs autonomously. Owner-scope items HOLD. α/β = β.

After 1.5-D.1 PR opens: orchestrator fires QC trigger autonomously per standing directive; on QC PASS, orchestrator merges PR + verdict autonomously; then dispatches Phase 1.5-D.2 (HU labelling pipeline; pilot 5 → Sonnet→Opus tier-up gate per `feedback_pilot_first_for_long_jobs.md` → full 25) per design memo §4.3.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at branch creation: MATCH `fab6c4c` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.1 dispatch: `MAIN_TERMINAL_PHASE15D1_HU_REFERENCE_SET_DESIGN_DISPATCH_2026-05-09.md` (master `fab6c4c`, PR #325)
- 1.5-A architect design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.2
- 1.5-C merged: master `d3c3da0` (PR #322); QC verdict: `b4caf38` (PR #324; PASS · 0/0/0)
- 1.5-B execution merged: master `8349a0b` (PR #315); QC verdict: `521bf36` (PR #319)
- Path α resolution precedent: `MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` (master `29ebe1f`, PR #316)
- 988-on-59 corpus: `data/corpus_combined_988_on_59_2026-05-09.jsonl` + labels
- Canonical close-hand-anchor: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`
- 1.5-C re-poke precedent: master `aa26ae4` (PR #321) — successful pattern; PR #322 followed in <2h
- Memory rules: `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_close_hand_selection.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_solver_aligned_sizing.md`, `feedback_solver_vs_expert_labels.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`

---

**Status: LEAD-PROGRAMMER — fire NOW on Phase 1.5-D.1 per dispatch in master `fab6c4c` (PR #325). 30 spots × 6 axes; 3 close + 2 canonical per axis; solver-aligned bet sizes; close-hand-anchor `v9_3way_v22_on_59.json`. STOP > improvise on anomalies. Orchestrator fires QC trigger + merges PR + QC verdict autonomously per standing directive on QC PASS.**
