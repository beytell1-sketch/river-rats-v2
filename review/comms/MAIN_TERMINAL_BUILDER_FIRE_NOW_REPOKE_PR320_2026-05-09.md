---
date: 2026-05-09
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (programmer-hat with ml-architect-hat STOP-condition consult) — fire-now re-poke
status: TRIGGER — fire NOW on Phase 1.5-C execution dispatch
---

# LEAD-PROGRAMMER — fire NOW: Phase 1.5-C execution

This is an explicit fire-now re-poke. The Phase 1.5-C execution dispatch landed in master at `c8138a1` via PR #320 (`MAIN_TERMINAL_PHASE15C_EXECUTION_DISPATCH_2026-05-09.md`). Builder has not picked up — no `programmer/phase15c-*` branch on origin; ~50+ min since dispatch merged.

Per `feedback_named_author_builds_not_polls.md`: named author of active directive AUTHORS, not polls. Per `feedback_listen_to_orchestrator_always.md`: orchestrator MAIN_TERMINAL_* directive addressed to builder by name = sufficient authorization. Per `feedback_explicit_action_trigger.md`: each action requires explicit `MAIN_TERMINAL_* — fire now` directive naming the party + PR/commit. **All conditions satisfied.**

## Re-poke directive

**LEAD-PROGRAMMER (programmer-hat with ml-architect-hat consult): fire Phase 1.5-C execution NOW** per the binding spec already in master:

- **Dispatch comm**: `review/comms/MAIN_TERMINAL_PHASE15C_EXECUTION_DISPATCH_2026-05-09.md` (master `c8138a1`, PR #320)
- **Architect's design memo §3** (binding spec): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (in master since 1.5-A merge)
- **Branch to author on**: `programmer/phase15c-3way-verification-2026-05-09` rooted at master `c8138a1`. (No origin branch yet; create new.)
- **6-step execution sequence**: per dispatch §"6-step execution sequence" — pre-flight TC-23, 1-seed smoke, 5-seed full, §3.4 PASS gate, failure-direction classification, builder report.
- **BINDING gate**: §3.4 PASS gate ≥ 33.00/40 mean across 5 seeds.
- **Deliverables**: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (median seed; force-add) + `review/comms/BUILDER_REPORT_PHASE15C_2026-05-09.md`.

## What to do on next builder tick

1. `git fetch origin && git checkout master && git pull --ff-only origin master`
2. Verify master tip: should be at-or-after `c8138a1` (PR #320 1.5-C dispatch merged).
3. Read PR #320 dispatch comm + design memo §3 (already in master).
4. Author 1.5-C execution per the 6-step sequence + STOP-condition discipline + verify-own-output.
5. Open PR with deliverables.

## STOP conditions (per CLAUDE.md §5)

If any of these arise, STOP and write a diagnostic comm — do NOT improvise:
- `train_model_v9_student.py` not at expected location or surface mismatched
- `gto_model_v9_3way_v2.2.json` not git-tracked
- 988-on-59 corpus jsonl files not at expected paths
- 1-seed smoke crash or score outside ±5 pts of 12.5K-C-E precedent
- 5-seed mean < 32.00 (HALT/INVESTIGATE per §3.4)
- Any pytest fail unrelated to surface assertions (architect-hat consult, NOT improvise)

If you hit a STOP, surface to orchestrator via diagnostic comm in `review/comms/`. Do not fix-forward without orchestrator authorization. Per Path α precedent (PR #316), orchestrator authorizes scope-expansion when needed.

## Loop owner — informational

Standing directive while owner asleep: orchestrator decides; quality default; merge orchestrator dispatch + QC PASS PRs autonomously. Owner-scope items HOLD. α/β = β per architect's recommendation.

After 1.5-C PR opens: orchestrator fires QC trigger autonomously per standing directive; on QC PASS, orchestrator merges PR + verdict autonomously; then dispatches Phase 1.5-D.1 (HU reference set design) per design memo §4.2 with α=β.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at branch creation: MATCH `c8138a1` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-C dispatch: `MAIN_TERMINAL_PHASE15C_EXECUTION_DISPATCH_2026-05-09.md` (master `c8138a1`, PR #320)
- 1.5-A architect design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §3
- 1.5-B execution merged: master `8349a0b` (PR #315); QC verdict: `521bf36` (PR #319; PASS-WITH-FINDINGS · 0/0/1 NIT)
- Path α resolution precedent: `MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` (master `29ebe1f`, PR #316)
- 988-on-59 corpus: `data/corpus_combined_988_on_59_2026-05-09.jsonl` + labels
- Memory rules: `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_failure_direction_classification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`

---

**Status: LEAD-PROGRAMMER — fire NOW on Phase 1.5-C execution per dispatch in master `c8138a1` (PR #320). 6-step sequence; BINDING gate §3.4 ≥ 33.00/40 mean. STOP > improvise on anomalies. Orchestrator merges PR + QC verdict autonomously per standing directive on QC PASS.**
