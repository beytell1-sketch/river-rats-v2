---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner · Teaching builder · Game builder
re: PR #9 merged — commit 16/16 (delayed_probe HU-only + PR #8 NITs) on master; ALL Stage 3.5 SUBSTANTIVE COMMITS DONE; only M4 + M5 audits remain before pre-Stage-6 gate fires
status: MILESTONE + GREENLIGHT — Stage 3.5 substantive cluster complete; M4 + M5 audits authorised; rollback tag stage3.5-pre-16-merge saved
---

# 🎯 Stage 3.5 Commits 1-16 ALL COMPLETE

## All 16 substantive Stage 3.5 commits are on master

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■■■■■        commits 13 / 13.2 / 13.2.5/6 / 13.3.1-5  ✅
■            commit 14 (Finding B fold-in)       ✅
■            commit 15 (folded_mw classifier split) ✅
■            commit 16 (delayed_probe HU-only + NITs) ✅ ← just merged
□            M4 audit                            🆕 authorised
□            M5 audit                            🆕 authorised (after M4)
```

After M4 + M5 clear: **pre-Stage-6 gate fires** (HOLD #4); Stage 3.5
declared closed; teaching unblock signals to merge v4.1; Stage 4
pilot can dispatch on owner's explicit greenlight.

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 9 |
| Title | Stage 3.5 commit 16/16: delayed_probe HU-only + PR #8 NITs |
| Merge commit | `cb4b827` on origin/master |
| Feature commit | `30dedc2` (preserved per `--merge`) |
| Verdict commit | `5eead6b` (preserved on master) |
| Feature branch | deleted from origin |
| Merge time | 2026-04-26T03:44:51Z (SAST 05:44) |
| Rollback tag | `stage3.5-pre-16-merge` at `2a54a7f` (origin) |
| Diff scope | 3 files, telemetry-only (per verdict) |

Pre-merge protocol-compliance checkpoint #4:
- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage3.5/commit-16`
- ✅ Title `Stage 3.5 commit 16/16:` (FINAL Stage 3.5 substantive commit)
- ✅ Verdict APPROVE 9/9 HIGH confidence
- ✅ Provenance line present
- ✅ "diff scope provably clean (3 files, telemetry-only)" — telemetry-only fix; no production code change in commit 16

## Commit 16 substance

Per the verdict: delayed_probe predicate tightened to HU-only
(previously misroute 4 multiway entries: MW-41, FB-18, FB-19,
SYN-F6_MW_all_live were all 3-way fixtures wrongly bucketed as
"HU delayed-probe large turn bet"). Plus PR #8 cosmetic NITs
fixed (stale doc comment + synthetic AH ordering bug).

This was a telemetry/classifier fix — labels for stratified
sampling in solver-verify stub. NOT a production code change to
chain narrowing or feature extraction.

## Greenlight: M4 + M5 audits

Builder may begin M4 audit and M5 audit per the original Stage 3.5
roadmap. These are the FINAL Stage 3.5 work items.

[**M4 / M5 SCOPE — TO BE SPECIFIED BY BUILDER:** the M4/M5 audits
are part of the original Stage 3.5 16-commit + audits roadmap.
Builder is the canonical authority on M4/M5 scope per
`BUILDER_V24_STAGE35_BLUEPRINT_V2_*.md` documents.

Likely M4/M5 shape (from `SESSION_STATE_2026-04-21.md` references):
- M4 audit: re-audit of Stage 3.5 work against MUST checklist; full
  validator + solver-verify stub run + corpus sanity + 81-case
  consumer test
- M5 audit: 3/3 anchors confirmation (calibration anchor + reference
  anchor + solver anchor)

Per orchestrator's autonomous-advance directive: builder authors
audits per blueprint. PR cycle if substantive code changes;
direct comms doc if audit-report-only with no code.]

## Cross-stream HOLD register update

| # | Item | Status |
|---|---|---|
| 1 | Stage 3.5 commit 16 + M4/M5 clean | 🟡 commit 16 ✅ done; M4 + M5 still pending |
| 2 | nut_flush_block hero-side | ✅ CLEARED 04-24 |
| 3 | C5 fixture swap real rows F3/F4 | 🟡 unblocked-pending-teaching-execution (3-gate rule) |
| 4 | Orchestrator pre-Stage-6 gate | ⏳ pending — fires when #1 fully clears (M4 + M5 done) |
| 5 | Commit 14 multiway field promotion | ✅ CLEARED 04-26 |
| 6 | Teaching Path B (range_position_desc) | ⏳ pending (separate trigger) |

Net since prior register: HOLD #1 went from "pending" to "🟡 partial"
— commit 16 done, M4/M5 to go.

## Pre-Stage-6 gate (HOLD #4) — what orchestrator runs at Stage 3.5 closure

Per the standing roadmap, when M4 + M5 audits clear, orchestrator
runs the pre-Stage-6 gate. This is the orchestrator's job, NOT a
builder task. Scope:

1. **Verify Stage 3.5 audits clean** — M4 + M5 reports show no
   blockers; builder confirms via comms
2. **Cross-stream verification** — teaching v4.1 SHIP REPORT can
   drop PRE-VERIFICATION marker post-C5.2 + C7 + V3 reviews;
   game's deferred items still owner-paced
3. **Authorise transition to Stage 4** — relabel pilot dispatch
   becomes owner-greenlightable (still owner's gate)
4. **Authorise teaching v4.1 merge** — teaching can open PR
   `teaching/v4-1-nan-render` → master with formal pre-Stage-6
   greenlight comms

A pre-Stage-6 gate plan was NOT pre-drafted overnight (avoiding
scope creep). Will be authored when M4 + M5 land.

## Stage 4 design DRAFTs status (unchanged this cycle)

5 drafts remain on origin/master, awaits owner review on wake.
Pilot dispatch is owner gate.

## Action

**Builder:**
1. Begin M4 audit per blueprint (or surface scope question)
2. After M4 clean: M5 audit
3. Surface audit reports via comms doc(s) when complete
4. After both clear: orchestrator runs pre-Stage-6 gate; builder
   stands by

**Orchestrator (me):**
1. PR #9 merged + this milestone confirmation pushed
2. Loop continues at 60-min cadence
3. When M4 + M5 audit reports land: surface to owner on wake
4. Pre-Stage-6 gate runs after M4 + M5 clear; will draft gate plan
   at that point
5. Cross-stream notifications fire on pre-Stage-6 gate clearance

**Teaching:** still held; awaits user confirmation per 3-gate rule
for C5.2 fixture swap. Cross-stream contract from commit 14 +
commit 16 (telemetry split) is intact.

**Game:** Phase A workstream owner-paced; commit 14 + 16 don't
change game-side disposition.

**Owner:** Stage 3.5 commits done while you slept. Wake to:
- Master at `cb4b827` with all 16 commits + audits queued
- 5 Stage 4 design DRAFTs ready for review
- Cross-stream unblock signals fired
- Wake-status navigational doc at `2a54a7f` (lists tier-1/2/3 reads)
- Builder ready for M4 audit on your nudge / their /loop pickup
- No emergency

## References

- `MAIN_TERMINAL_WAKE_STATUS_2026-04-26.md` — single-page
  orientation
- `MAIN_TERMINAL_OVERNIGHT_PROGRESS_2026-04-26.md` — 02:00 snapshot
- `MAIN_TERMINAL_PR_8_MERGED_COMMIT16_GREENLIGHT_2026-04-26.md` —
  parent doc that greenlit commit 16
- `BUILDER_COMMIT16_SCOPE_2026-04-26.md` — builder's scope reasoning
- 4 rollback tags on origin: `stage3.5-pre-13-3-4-merge`,
  `stage3.5-pre-13-3-5-merge`, `stage3.5-pre-14-merge`,
  `stage3.5-pre-15-merge`, `stage3.5-pre-16-merge`
