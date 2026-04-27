---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Builder · QC stream · Reviewer streams · Owner
re: ORCHESTRATION STATE — single source of truth; current next-action per role; updated each major state change
status: LIVE — re-read this comm on every /loop tick before deciding anything else
---

# Orchestration state — single source of truth

**Last updated:** 2026-04-27 ~12:51 SAST
**Master HEAD:** `b39126b` (build-execute directive merged)
**Open PRs in v2:** none

## Active workstream

**Corpus revision pipeline execution.** Phase 2 implementation merged. Pipeline scripts ready to run on live data. Mass labelling kickoff blocked on the data PR landing + Tier 1 manifest expansion.

Phase B pilot (Protocol B/C labelling) is **INDEFINITELY HELD** per Tick 84 — do NOT watch Phase B file paths; that workstream is paused.

## Per-role next action (READ THIS FIRST when your /loop fires)

### BUILDER — your next action is AUTHORING, not polling

If you are the lead-programmer / builder terminal: your next action is authoring per the build-execute directive at `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` (master `b39126b`).

Per memory `feedback_named_author_builds_not_polls.md`: when /loop reads a comm naming YOU as the author of an active build directive, next tick is **AUTHORING**, not polling.

**Sequence:**
1. `cd ~/river-rats-v2 && git pull --ff-only origin master`
2. Read `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md` in full
3. Run E1 → verify gate → E2-B → verify gate → E2-A → verify gate → E3 → verify gate → C2 → final attestation
4. Open data-only PR on branch `programmer/corpus-revision-execution-2026-04-27` with the new files + your report at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md`
5. STOP and report BLOCKED on any verification gate failure. Do NOT improvise.

**Known watchout from your Phase 2 Q3:** Mode A self-play with `single_position='UTG'` yields 0 records (UTG folds preflop). Use CO/BTN/BB. If the script has no `--positions` flag, write a small driver in `scripts/` for that — but flag it for orchestrator review before merging.

### QC STREAM — your next action depends on builder activity

When the builder opens the data PR (branch `programmer/corpus-revision-execution-2026-04-27`):
- Run paired V-Implementation-Spec-Match (TC-24) + V-Integration-Trace (TC-26) on the data PR
- V-Implementation-Spec-Match: lock file fields populated correctly; structural gates fired correctly
- V-Integration-Trace: re-run a sample from the pool through `extract_all_features` and confirm output matches stored `feat_dict` bit-for-bit (this is exactly the failure mode TC-26 was added to catch)
- Write findings to `~/river-rats-qc/findings/2026-04-27-data-pr-pre-merge-corpus-revision-500-hand.md`
- Mirror to `review/comms/QC_*.md` per Path B pattern; open PR

Until builder produces output: continue post-merge audit-trail integrity sweeps on master `b39126b`. Master delta since your last sweep includes 5 PRs: #65, #64, #66, #60, #67. TC-25 audit-trail-integrity check on each merge is appropriate background work.

### REVIEWER STREAMS (gto-expert + ml-architect) — wait for orchestrator dispatch

Per orchestrator role separation: reviewer dispatch is orchestrator-initiated when the data PR opens. Don't pre-emptively review.

### ORCHESTRATOR (this terminal) — coordinate + dispatch

- /loop tick cadence: 180s (3 min) for active orchestration
- On builder data PR open: immediately dispatch gto-expert + ml-architect round 3 reviews
- On QC data PR audit landing: synthesize all 3 reviews → merge gate (per `feedback_qc_required_before_approval.md`, QC must be in the synthesis)
- On synthesis converge APPROVE: merge data PR, then write mass-labelling kickoff directive
- On any CHANGES_REQUESTED: write Phase 3 directive to builder

## What is NOT in scope right now

- Phase B Protocol B/C labelling (HELD)
- New scenario modules (deferred to v2.3+)
- Bare-except cleanup, conftest.py path, T5 alternative spec (NIT backlog)

## Structural escalation to owner

Builder terminal /loop input is stale (Phase B watch checklist). The watch criteria do not include `MAIN_TERMINAL_*.md` directives, so the build-execute directive will not be discovered by the builder /loop's automated checks. The builder will only see this directive if their /loop's `ls -lt review/comms/QC_*.md` happens to surface comms that name them — and even then, their decision rules don't action on it.

**Recommended fix when owner returns:** Replace builder /loop input with corpus-revision watch:
```
/loop Check ~/river-rats-v2 master for orchestrator directives at review/comms/MAIN_TERMINAL_*.md and BUILDER_*.md naming the lead-programmer; on directive present and not yet executed, AUTHOR per directive instructions; on data PR open by you, hold until orchestrator dispatches round 3 reviews; per `feedback_named_author_builds_not_polls.md` next tick is authoring not polling. 5 min cadence. STOP on anomaly.
```

## References

- Build-execute directive: `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_DIRECTIVE_2026-04-27.md`
- Round 2 synthesis: `review/comms/MAIN_TERMINAL_PR60_PHASE2_SYNTHESIS_2026-04-27.md`
- Reviews: `REVIEW_GTO_EXPERT_PR60_PHASE2_*.md`, `REVIEW_ML_ARCHITECT_PR60_PHASE2_*.md`, `QC_ROUND2_AUDIT_PR60_PHASE2_*.md`
- Builder Phase 2 report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- Memory: `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_qc_required_before_approval.md`

**Status: ORCHESTRATION STATE LIVE. Builder primary blocker = /loop input stale (owner-fix on return). All other roles aligned + ready.**
