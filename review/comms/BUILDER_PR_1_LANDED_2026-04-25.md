---
date: 2026-04-25
from: Logic builder
to: Main terminal (orchestrator) · GTO reviewer · Owner
re: Stage 3.5 commit 13.2.6 PR opened — fix-forward for the APPROVE_WITH_FIXES verdict on 13.2.5
status: PR-OPEN — PR #1 on stage3.5/commit-13-2-6; awaits per-batch GTO review on PR thread + orchestrator approval; merge with --merge --delete-branch on greenlight
---

# Builder — PR #1 Open for 13.2.6

## PR

**URL:** https://github.com/beytell1-sketch/river-rats-v2/pull/1

**Title:** Stage 3.5 commit 13.2.6/16: APPROVE_WITH_FIXES on 13.2.5 — narrative cleanup + classifier tightening

**Branch:** `stage3.5/commit-13-2-6`

**Base:** `master`

**Single commit:** `78ca7ae` (3 files, +164 / -21).

This is the first PR opened under the standing pattern from
`MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md`. Per directive:
**merge with `--merge` (not `--squash`)** to preserve per-commit
SHAs in the audit trail.

## What's in the PR

Two fixes from the GTO verdict on 13.2.5
(`GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md`, `00099c6`):

1. **FIX #1 — SYN-T_B05 header narrative cleanup.** Replaced stale
   `narrow_by_action_history:814` line reference (actual is `:947`,
   but bare line numbers drift). Rephrased the ambiguous parenthetical
   that read as if turn:CHECK enters the chain when
   `decision_street='turn'` (per the prior-street-only rule it
   doesn't). Mirrors test-comment phrasing.

2. **FIX #2 — Position-aware classifier predicate.** Tightened
   `_classify_shape`'s `hu_donk_x_bet` flop-bet branch from
   `flop_bet_count >= 1` (position-agnostic) to `flop_has_villain_bet`
   (`e[1] == villain_pos`). Defensive against the 13.3 130-entry
   full lift mis-routing a hero-bets-flop + villain-led-river-bet
   pattern into `hu_donk_x_bet`. Threading: added
   `_REFERENCE_VILLAIN_POS: Dict[str, str]` to the reference
   sidecar as single source of truth; `_classify_shape` and
   `_stratify` signatures now require `villain_pos` /
   `villain_pos_map`.

Plus 2 new tests:

- `test_commit13_2_6_classifier_position_aware_donk` — verifies
  hero-as-flop-bettor + villain-river-bet does NOT route to
  `hu_donk_x_bet` post-fix; regression guards on SYN-F7 + SYN-T_J02.
- `test_commit13_2_6_villain_pos_map_covers_all_reference_entries`
  — cross-check that `_REFERENCE_VILLAIN_POS` covers every ref_id.

## Test results at PR-open time

| Suite | Result |
|---|---|
| `test_commit13_sidecar_dryrun.py` | **13/13 PASS** (was 11/11; +2 new) |
| All consumers of touched module (`_reference_action_history_sidecar`) | **24/24 PASS** |
| Adjacent commit-test files (commit10/11/8) | **21/21 PASS** |
| `tests/solver_verify_sidecars.py` end-to-end (stub mode) | **PASS** (7-entry stratified sample, all OK) |
| Full-suite collection | Hangs at extension-module segfault — pre-existing per 13.2.5 builder report; not introduced by 13.2.6 |

## Standing posture

1. ✅ Feature branch `stage3.5/commit-13-2-6` pushed
2. ✅ PR #1 opened with full body referencing GTO verdict, fix list,
   test results
3. ⏳ Per-batch GTO review on PR thread — builder will dispatch
   general-purpose subagent with gto-expert persona embedded
   (same provenance pattern as the 13.2.5 verdict; dedicated
   `gto-expert` subagent still unavailable in this builder session)
4. ⏳ Orchestrator + GTO APPROVE → `gh pr merge 1 --merge --delete-branch`
5. ⏳ Post-merge: orchestrator greenlights commit 13.3 authoring
   on a new `stage3.5/commit-13-3` feature branch

If GTO review on the PR returns APPROVE_WITH_FIXES or REWORK:
fix-forward to 13.2.7 on a new feature branch (PR pattern continues).

## Cross-stream impact

| Stream | Effect |
|---|---|
| Logic | 13.2.6 closes the APPROVE_WITH_FIXES audit-trail on 13.2.5; 13.3 unblocks on merge |
| Teaching HOLD #1 | Unchanged — still waits on commit 16 + M4/M5 |
| Teaching HOLD #3 / #5 | Unchanged — still waits on commit 14 (Finding B fold-in) |
| Teaching HOLD #4 | Unchanged — waits on #1 + #3 + #5 |

No teaching-side action triggered. Teaching stays at PRE-VERIFICATION
HOLD on its v4.1 SHIP REPORT.

## Reference

- PR: https://github.com/beytell1-sketch/river-rats-v2/pull/1
- GTO verdict that drove 13.2.6: `review/comms/GTO_REVIEW_VERDICT_13_2_5_2026-04-25.md` (`00099c6`)
- Push-policy parent directive: `review/comms/MAIN_TERMINAL_PUSH_POLICY_DECISION_2026-04-25.md` (`b6c1ade`) — PR pattern + `--merge` requirement
- Push-policy addendum: `review/comms/MAIN_TERMINAL_PUSH_POLICY_ADDENDUM_2026-04-25.md` (`0bb91ef`)
- GTO dispatch authority: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_AUTHORITY_2026-04-25.md` (`21f16e6`) — builder dispatches GTO
- Prior dispatch-block resolution: `review/comms/MAIN_TERMINAL_GTO_DISPATCH_BLOCK_RESOLUTION_2026-04-25.md` (`15f7b07`) — overridden in-session by owner; general-purpose-with-persona authorised
- 13.2.5 audit-trail: `review/comms/BUILDER_13_2_5_ON_ORIGIN_GTO_READY_2026-04-25.md` (`7bca96a`)

## Action

**Builder:** dispatching the per-batch GTO review on the PR next
(general-purpose with gto-expert persona, output to PR thread comment
+ verdict comms doc). After verdict: hold on 13.3 authoring until
orchestrator greenlight.

**Orchestrator:** read PR + GTO verdict; on APPROVE merge with
`gh pr merge 1 --merge --delete-branch`; post-merge greenlight 13.3.

**Owner:** no action; briefed via this doc and PR link.
