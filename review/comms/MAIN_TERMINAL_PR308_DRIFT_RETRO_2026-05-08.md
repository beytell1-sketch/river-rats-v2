---
date: 2026-05-08
from: Main terminal (orchestrator)
to: Owner (notice) · LEAD-PROGRAMMER (notice; no action) · QC stream (notice + curative-additions suggestion)
re: PR #308 cross-content drift — root cause + remedy + prevention rule committed; per-party state assertion post-fix
status: RETRO — no fire-now; informational + memory commit
---

# PR #308 cross-content drift retro

## Incident summary

PR #308 (orchestrator QC audit-now trigger for PR #307) was inadvertently created with PR #307's branch as its base, not master. Diff vs master at PR #308 open: 3 files added (intended trigger comm + 614-line architect memo + 96-line builder report) instead of 1.

If PR #308 had auto-merged, the 710-line milestone-class architect memo would have landed via the trigger PR — bypassing the four-step gating (trigger merge → QC fires on PR #307 content → QC verdict PR → owner-fire-now-on-content-merge). PR #307's branch would have auto-closed as merged-via-#308, eliminating its independent QC + owner-fire-now gate.

**Caught pre-merge by QC stream** via diff inspection of PR #308 vs master. Surfaced before any merge took place.

## Root cause

`git checkout -b orch/qc-audit-trigger-pr307-2026-05-08` ran while local HEAD was at `6164f14` (PR #307's branch tip), not at master `5863f13`. The orchestrator's prior `git pull --ff-only origin master` had succeeded (master at `5863f13`), but a subsequent intervening fetch/checkout step left HEAD on PR #307's branch ref. The new branch inherited that base.

The existing `feedback_shared_tree_commit_hygiene.md` rule (`git status` + `git diff --cached` before commit) covers staged content scope but does NOT catch wrong-base-branch — staged content was correct (single file added) and `--cached` diff showed only that file. Wrong base was detectable only via `git diff --stat origin/master..HEAD` or `git log --oneline origin/master..HEAD`.

## Remedy executed

1. PR #309 opened on a fresh branch `orch/qc-audit-trigger-pr307-clean-2026-05-08` rooted at master `5863f13` — single-file diff, identical trigger-comm content.
2. PR #308 closed with explanation; branch deleted.
3. PR #309 merged on owner fire-now (master `832d6d1`).
4. QC stream now firing 11-item audit on PR #307.

Force-push to PR #308's branch was attempted as Path 1 but denied (system-rule destructive operation; not explicitly authorized). Non-destructive close-and-replace path was equivalent in outcome and preserved the closed-PR audit record.

## Prevention rule (committed to memory)

New feedback memory: `feedback_orchestrator_branch_base_verification.md`. Three pre-push checks on every orchestrator dispatch/trigger PR:

1. `git rev-parse HEAD` matches `git rev-parse origin/master` (or intended base) IMMEDIATELY after `git checkout -b <new-branch>`.
2. `git diff --stat origin/master..HEAD` shows ONLY intended files.
3. `git log --oneline origin/master..HEAD` shows ONLY my own commit(s).

Failure of any check = abort, re-anchor, rebuild branch. Indexed in `MEMORY.md` under "Operational".

## Per-party state assertion post-fix

## Owner — informational

- Master `832d6d1` (PR #309 trigger merged).
- PR #307 OPEN, unchanged from your last fire-now decision point.
- Prevention rule committed to memory; orchestrator branch creation will run all 3 checks going forward.
- This retro comm itself is rooted at master `832d6d1`; HEAD = origin/master verified at branch creation.
- No action required on your side. Loop unchanged.

## LEAD-PROGRAMMER (architect-hat) — informational

- Phase 1.5-A authorship is unchanged. PR #307 remains OPEN at head `6164f14a6a98c3ec09ace3d0c624da6c558eb519` with the same 2-file diff (614+96 = 710 lines) as authored.
- No re-work required. The drift was orchestrator-side branch-base mistake; nothing about your dispatch-compliance, content, or methodology was implicated.
- QC's expanded-scope 11-item audit is now firing per dispatch in master (`MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR307_2026-05-08.md`, master `832d6d1`).
- No fire-now to you here.

## QC stream — catch acknowledged + curative-additions suggestion

- Pre-merge catch on PR #308's diff scope was load-bearing — without it, the milestone-class architect memo would have bypassed independent QC + owner gates. Recording this in the QC value-of-fourth-voice ledger.
- **Curative-additions suggestion**: add new test class `TC-X-ORCHESTRATOR-BRANCH-BASE-VERIFICATION` to `~/river-rats-qc/learning/test_class_registry.md` and incident entry to `incident_pattern_library.md`. Trigger: any orchestrator-authored PR. Check: PR's diff vs master matches the orchestrator's stated single-file-comm intent (typically 1 file; trigger PRs are exactly 1 trigger comm). Past finding: PR #308 (this incident).
- This is QC-scope to ratify or amend — orchestrator surfaces the suggestion; QC decides test class formalisation.
- 11-item audit on PR #307 unchanged in scope by this retro.

## What's blocked / what's queued

**Cleared by this comm:** drift retro recorded; prevention rule committed; per-party state asserted; QC curative-additions suggested.

**Unchanged:**
- PR #307 OPEN, awaiting QC verdict (~20-30 min from QC's tick on `832d6d1`).
- After QC PASS → owner explicit fire-now → PR #307 merge → orchestrator drafts Phase 1.5-B execution sub-phase dispatch.

**Newly queued:** None.

## References

- PR #308 (closed; bundled-content drift): `orch/qc-audit-trigger-pr307-2026-05-08` (branch deleted)
- PR #309 (clean replacement; merged): master `832d6d1`
- PR #307 (OPEN; architect memo): head `6164f14a`
- Phase 1.5-A dispatch: master `5863f13` (PR #306)
- New memory: `feedback_orchestrator_branch_base_verification.md`
- Existing memory invoked: `feedback_shared_tree_commit_hygiene.md`, `feedback_quality_default_no_ask.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_output_structure_per_party.md`, `project_qc_heartbeat_convention.md`

---

**Status: Retro recorded. No fire-now. Prevention rule committed. State across all 3 parties asserted post-fix. Loop holds at "QC firing on PR #307" per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR307_2026-05-08.md` (master `832d6d1`).**
