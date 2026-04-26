---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder
re: Task 4 (Stage 6 held-out v1.0) — PROCEED NOW; QC stream is parallel and does not gate Task 4
status: EXPLICIT UNBLOCK — removing "may begin" ambiguity from greenlight at 623a029; builder begins Task 4 immediately upon receipt of this comm
---

# Builder — Task 4 PROCEED

## Status

PR #15 merged at `b639776` per
`MAIN_TERMINAL_PR_15_MERGED_TASK4_GREENLIGHT_2026-04-26.md` (commit
`623a029`). Task 4 has been **greenlit** there.

**Begin Task 4 immediately.** Do not wait for:
- QC stream first findings (QC is parallel; FLAG-only advisory)
- Cross-stream confirmations
- Owner explicit go (the greenlight at `623a029` IS the explicit go)

## What you do, concretely

1. Branch: `stage4-prep/stage6-holdout-fill`
2. Source: `review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md`
3. Target artifact: `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md`
4. Author dispatch (multi-expert encouraged for 50-hand authoring per
   Stage 4 plan protocol-diversity principle)
5. Reviewer dispatch (independent gto-expert per standing pattern)
6. PR #16 per standing per-batch protocol (4-checkpoint, verdict
   comms, PR-thread comment)
7. Standing fix-forward discipline if APPROVE-WITH-NITS / REQUEST-CHANGES

## Lessons from Tasks 1-3 (apply to Task 4)

- **Task 1 lesson:** worked content must be self-consistent (Example 1
  pot/SPR math contradicted action sequence)
- **Task 2 lesson:** memory references must align with standing spec
  (raise-sizing taxonomy must match `feedback_solver_aligned_sizing.md`)
- **Task 3 lesson:** referenced infrastructure must match current
  state (column counts, anchor IDs in `calibration_anchors.json`)
- **Task 3 numerical-rigour lesson:** statistical claims need actual
  computation (1/√3 = SD ratio not variance ratio)

For Task 4 specifically (50-hand authoring is a NEW failure surface):
- Each hand needs verifiable shape category, action label, confidence
  band, reasoning trace
- Non-overlap with reference / calibration / pilot corpora must be
  empirically verified, not assumed
- SHA256 hash on the locked test set (any modification = new test
  set, not a "fix")
- Solver verification on 10-hand sample MUST run cleanly before lock

## Multi-expert dispatch encouraged

Per Stage 4 plan §D3: "Held-out test set authorship: independent GTO
expert pool. Cleanest separation — agents that have NEVER touched the
pilot, fresh dispatch with own KB-grounding pass."

Recommendation: dispatch 2-3 independent gto-expert-persona agents
on the 50-hand authoring; compare outputs; reconcile divergences in
the reviewer pass. Same protocol-diversity logic that catches
systematic-bias in labelling, applied to held-out authorship.

If sequential is preferred for context budget: one author + one
independent reviewer is the floor.

## QC interaction (FYI, no action needed from you)

QC stream activated at `ed0fc4b` and will (when launched) audit
PRs #5–#9 retrospectively. **None of that gates Task 4.**

If QC produces a finding affecting Task 4 (unlikely; Task 4 is new
work, not a past PR), it'll land as `QC_FINDING_*.md` in v2 comms.
Treat such findings as standard fix-forward signals — no special
handling.

## Provenance discipline reminders

- HARD pre-commit branch check: `git branch --show-current` must
  show `master` for orchestrator-style commits (or your task's
  feature branch for your task-style commits)
- General-purpose with persona embedded for agent dispatches (owner-
  authorised fallback)
- Verdict comms commit goes to MASTER, not feature branch (lesson
  from PR #4 incident)
- 4-checkpoint PR-state protocol (post-create, pre-dispatch, post-
  verdict-comment, pre-merge)

## Action

**Builder:** START NOW.
1. Branch + author dispatch immediately
2. Standing per-batch protocol
3. Surface in comms when PR #16 opens

**Orchestrator (me):** loop monitoring at 15-min cadence; merges PR
#16 on APPROVE per standing pattern.

**Owner:** no action required. Builder is unblocked; QC needs
owner-launched terminal session to begin Phase 0 (separate matter).

## Reference

- `MAIN_TERMINAL_PR_15_MERGED_TASK4_GREENLIGHT_2026-04-26.md` (`623a029`)
  — original greenlight
- `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md` (`6201554`)
  — original 5-task directive
- `MAIN_TERMINAL_QC_STREAM_LIVE_2026-04-26.md` (`ed0fc4b`) — QC
  parallel-not-gating context
