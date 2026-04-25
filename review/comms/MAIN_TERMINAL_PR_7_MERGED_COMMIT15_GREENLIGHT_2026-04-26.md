---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner · Teaching builder · Game builder
re: PR #7 merged — commit 14 (Finding B fold-in) on master; teaching HOLD #5 + game per-villain range bars now UNBLOCKED upstream-side; commit 15 greenlit; rollback tag stage3.5-pre-14-merge saved
status: CONFIRMATION + GREENLIGHT + CROSS-STREAM UNBLOCK — commit 14 landed; teaching may begin C5.2 fixture swap on signal; game may begin per-villain range bar work; commit 15 may begin on stage3.5/commit-15
---

# PR #7 Merged — Commit 14 Landed — Cross-Stream Unblock Fired

## Major milestone: Finding B is on master

Per `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`,
commit 14 promotes the multiway per-villain fields from
`chain_meta` onto the features dict. This is the upstream change
that unblocks teaching's HOLD #5 / #3 and game's per-villain range
bars + (separately) range_position_desc rename.

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■            commit 13 (1st dry-run)             ✅
■            commit 13.2 (2nd dry-run)           ✅
■■           commits 13.2.5 + 13.2.6 (fixes)     ✅
■■■■■        commits 13.3.1..5 (full lift)       ✅
■            commit 14 (Finding B fold-in)       ✅ ← just merged 🎯
□            commit 15                           🆕 greenlit — NEXT
□            commit 16                           ⏳
□            M4 + M5 audits                      ⏳
```

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 7 |
| Title | Stage 3.5 commit 14/16: Finding B fold-in — multiway per-villain field promotion |
| Merge commit | `b0ef6c5` on origin/master |
| Feature commit | `134be52` (preserved per `--merge`) |
| Verdict commit | `36e18be` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-25T23:34:45Z (SAST 01:34) |
| Rollback tag | `stage3.5-pre-14-merge` at `a20ff23` (origin) |
| Code change | +85 lines `feature_extractor.py` + new `test_commit14_finding_b.py` |

Pre-merge protocol-compliance checkpoint #4:

- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage3.5/commit-14`
- ✅ Title cites Finding B
- ✅ Verdict APPROVE 7/7 HIGH confidence — verdict status line:
  *"cross-stream contract READY for teaching HOLD #5 + game
  per-villain range bars; orchestrator can merge"*
- ✅ Provenance line present

## Cross-stream notifications fired

Two cross-stream comms docs being written in parallel with this
confirmation:

1. `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md` —
   teaching unblock signal; activates teaching's path through
   C5.2 fixture swap → V3 review → C7 wording → V3 review → SHIP
   REPORT update → pre-Stage-6 gate
2. `MAIN_TERMINAL_TO_GAME_2026-04-26-a.md` — game unblock for
   per-villain range bars (separately from
   range_position_desc rename which still waits on teaching Path B)

## Greenlight: commit 15

Builder may begin **commit 15** on `stage3.5/commit-15`.

[**COMMIT 15 SCOPE — TO BE SPECIFIED:** I do not have an explicit
commit 15 spec in the comms history accessible to this session.
Per the Stage 3.5 16-commit roadmap (`SESSION_STATE_2026-04-21.md`
+ blueprint docs), commits 14, 15, 16 are the final cluster before
M4 + M5 audits.

Builder is the canonical authority on commit 15 scope per
`BUILDER_V24_STAGE35_BLUEPRINT_V2_*.md` documents. If builder has
the commit 15 spec in their own scratch / blueprint:

- Author per the blueprint
- PR #8 follows standing per-batch protocol (branch
  `stage3.5/commit-15`, GTO review, verdict, merge with --merge
  --delete-branch)

If commit 15 spec is unclear / depends on commit 14 outcomes
(e.g. integration tests against the new per-villain fields):

- Builder writes a brief `BUILDER_COMMIT15_SCOPE_<date>.md` to
  comms, surfaces to orchestrator, owner reviews on wake before
  authoring begins

Per `feedback_quality_default_no_ask.md`: when scope is unclear,
the slow/quality option is the brief surface to orchestrator
rather than authoring something speculative. Builder discretion.]

## Cross-stream HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 1 | Stage 3.5 commit 16 + M4/M5 clean | ⏳ pending (commit 15 + 16 + audits remain) | Logic builder |
| 2 | nut_flush_block hero-side | ✅ CLEARED 2026-04-24 | — |
| 3 | C5 fixture swap real rows F3/F4 | 🆕 NOW UNBLOCKED — teaching may execute on cross-stream-notification receipt | Teaching |
| 4 | Orchestrator pre-Stage-6 gate | ⏳ pending (waits for #1) | Orchestrator |
| 5 | Commit 14 multiway field promotion | ✅ CLEARED 2026-04-26 (this PR) | — |
| 6 | Teaching Path B (range_position_desc) | ⏳ pending (separate from commit 14) | Teaching |

Net: HOLDs #5 cleared; HOLD #3 unblocked-pending-teaching-execution.
HOLD #1, #4, #6 remain.

## Carry-forward items (post-commit-14)

| Item | Source | Disposition |
|---|---|---|
| `folded_mw` classifier promiscuity (32+ entries) | PRs #2-#6 | Defer to commit 14.x cleanup. **Now commit 14 has landed; the cleanup window is open.** Builder discretion on whether to fold into commit 15 or a separate 14.1 commit. |
| `mw_per_villain` distribution growth | PRs #4-#6 | Same family as folded_mw; same disposition. |
| MW-50 RAISE→BET normalisation | PR #5 | Deferred to v2.5 (pre-existing, owner-authorised). |
| Dedicated `gto-expert` dispatch | dispatch resolution | Owner-authorised general-purpose + persona fallback continues; no change. |

## Stage 4 design DRAFTs status

5 drafts on origin/master (`4d939f1` + `362e70b`) — unchanged this
tick. Awaits owner review on wake + domain-expert content fill.
Pilot dispatch is owner gate.

## Action

**Builder:**
1. Begin commit 15 on `stage3.5/commit-15` (or surface scope
   question via `BUILDER_COMMIT15_SCOPE_<date>.md` if unclear)
2. Apply HARD pre-commit branch check
3. PR #8 per standing pattern

**Teaching builder:**
1. Read `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md`
   (cross-stream notification)
2. Per overnight discipline: surface "ready to begin C5.2 fixture
   swap?" to user — DO NOT auto-start (3-gate rule from
   `MAIN_TERMINAL_TEACHING_LOOP_SETUP_2026-04-25.md`)
3. On user explicit confirmation: foreground C5.2 fixture swap
   (real F3/F4 rows from commit-14-era extract_all_features) →
   V3 review → C7 wording → V3 review → SHIP REPORT update

**Game builder:**
1. Read `MAIN_TERMINAL_TO_GAME_2026-04-26-a.md`
2. Per-villain range bars now feasible. Review + plan execution.
3. range_position_desc rename remains blocked (separate trigger:
   teaching Path B).

**Orchestrator (me):**
1. PR #7 merged + cross-stream notifications fired (this commit
   batch)
2. Loop continues at 60-min cadence (post-merge, awaiting cross-
   stream responses + builder's commit 15 PR)
3. When commit 15 PR opens: standing pre-merge checklist + merge
   on APPROVE
4. Continue to commit 16 + M4 + M5 audits sequence
5. Pre-Stage-6 gate runs after commit 16 + M4/M5 clean

**Owner:** sleep / wake to read overnight progress + Stage 4 drafts
+ this commit-14-merge confirmation + cross-stream notifications.
No emergency.

## References

- `MAIN_TERMINAL_PR_6_MERGED_COMMIT14_GREENLIGHT_2026-04-26.md` —
  commit 14 spec + cross-stream pre-notification
- `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md` —
  Finding B resolution doc; commit 14 fulfils §3-Q1 promotion
- `MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md` — defines teaching
  unblock sequence triggered by commit 14 landing
- `MAIN_TERMINAL_TO_GAME_2026-04-25-a.md` — defines game's deferred
  items + cross-stream linkage
- `feedback_quality_default_no_ask.md`, `feedback_no_deadlines.md`,
  `feedback_orchestrator_controls_parallel_timing.md`
