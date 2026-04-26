---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner · Teaching builder · Game builder
re: Pre-Stage-6 gate FIRED + CLEARED — Stage 3.5 declared CLOSED — teaching v4.1 merge authorised post-C5.2/C7 — Stage 4 design review authorised — pilot dispatch remains owner gate
status: MILESTONE — major project transition; HOLD #1 + #4 both clear; teaching unblock signal upgraded from "pending C5.2 confirmation" to "merge-greenlightable when C5.2/C7 + V3 reviews done"
---

# 🎯 Pre-Stage-6 Gate CLEARED — Stage 3.5 CLOSED

## What just happened

Builder posted `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md` at
`33272ff`: M4 + M5 audits BOTH PASS on post-Stage-3.5 master HEAD
`59c3fd9`. Canonical Stage 3.5 test suite 50/50 PASS. Solver-verify
stratification PASS. d8411 multiway anchor STRENGTHENED from
commit 14 Finding B promotion.

This clears HOLD #1. Pre-Stage-6 gate (HOLD #4) is the
orchestrator's responsibility per the locked roadmap; running it
now.

## Pre-Stage-6 gate — orchestrator's protocol-compliance check

| Gate item | Status | Evidence |
|---|---|---|
| Stage 3.5 commits 1-16 on master | ✅ PASS | `git log origin/master` includes commits 1-12 + 13/13.2/13.2.5/6 + 13.3.1-5 + 14 + 15 + 16 |
| All per-batch GTO reviews APPROVE | ✅ PASS | Verdicts on master at `5eead6b`, `488310f`, `36e18be`, `bf6be6e`, `5e3b75f`, `00099c6`, `2fc545c`, etc. |
| All PRs merged via `--merge --delete-branch` (preserved per-commit SHAs) | ✅ PASS | Merge commits at `8480b56`, `5007a41`, `b0ef6c5`, `a9b6301`, `cb4b827` |
| Rollback tags saved on origin | ✅ PASS | `stage3.5-pre-13-3-4-merge`, `stage3.5-pre-13-3-5-merge`, `stage3.5-pre-14-merge`, `stage3.5-pre-15-merge`, `stage3.5-pre-16-merge` (5 tags) |
| M4 distribution-shift audit | ✅ PASS | 0/124 isolation violations; 455/455 multi-street chain-active; identical to 04-20 baseline |
| M5 3-anchor model recheck | ✅ PASS | 3/3 anchors predict BET; d8411 STRENGTHENED +0.072 p(BET) from Finding B; HU anchors identical (semantics unchanged) |
| Canonical test suite | ✅ PASS | 50/50 |
| Solver-verify stratification | ✅ PASS | Commit 16 verification clean |
| No regressions | ✅ PASS | Distribution numbers identical to 04-20 baseline; HU/multiway semantics intact |
| Cross-stream contracts | ✅ READY | Commit 14 Finding B fields propagate to teaching/game adapter consumers |
| Provenance discipline | ✅ PASS | All verdicts honestly recorded as general-purpose + gto-expert persona (owner-authorised fallback) |
| Carry-forward items | ✅ TRACKED | folded_mw split (commit 15), delayed_probe HU-only (commit 16), MW-50 RAISE→BET deferred to v2.5, 1 cosmetic NIT from PR #9 (non-blocker) |

**All 12 gate items PASS. Pre-Stage-6 gate CLEARED.**

## Stage 3.5 declared CLOSED

```
■■■■■■■■■■■■  commits 1-12 (foundation)         ✅
■■■■■        commits 13 / 13.2 / 13.2.5/6 / 13.3.1-5  ✅
■            commit 14 (Finding B fold-in)       ✅
■            commit 15 (folded_mw classifier split) ✅
■            commit 16 (delayed_probe HU-only + NITs) ✅
■            M4 distribution-shift audit         ✅ PASS
■            M5 3-anchor recheck                 ✅ PASS

🎯 STAGE 3.5 CLOSED at master `59c3fd9` (audits clean on this SHA)
```

**Effect on dependent streams:**

- v2.4 ship sequence: Stage 3.5 → **Stage 4 (relabel)** → Stage 5
  (retrain) → Stage 6 (ship gate)
- Stage 4 is the next phase. Pilot dispatch remains owner gate per
  locked Stage 4 plan at `ee3d9f5`.

## Cross-stream HOLD register — final update

| # | Item | Status |
|---|---|---|
| 1 | Stage 3.5 commit 16 + M4/M5 clean | ✅ CLEARED 04-26 |
| 2 | nut_flush_block hero-side | ✅ CLEARED 04-24 |
| 3 | C5 fixture swap real rows F3/F4 | 🟡 unblocked-pending-teaching-execution (3-gate rule still applies) |
| 4 | Orchestrator pre-Stage-6 gate | ✅ CLEARED 04-26 (this doc) |
| 5 | Commit 14 multiway field promotion | ✅ CLEARED 04-26 |
| 6 | Teaching Path B (range_position_desc) | ⏳ pending (separate trigger, not gating Stage 3.5 closure) |

5 of 6 HOLDs cleared. HOLD #3 awaits teaching execution; HOLD #6
is independent.

## Teaching v4.1 merge authorisation

Teaching is hereby **authorised** to merge `teaching/v4-1-nan-render`
into teaching's master once:

1. C5.2 fixture swap (F3/F4 real-row swap) lands on the held branch
2. V3 per-commit review on C5.2 = APPROVE
3. C7 wording cleanup lands
4. V3 per-commit review on C7 = APPROVE
5. SHIP REPORT updated to drop PRE-VERIFICATION marker on §5.3

The pre-Stage-6 gate clearance lifts the upstream block. Teaching's
3-gate execution rule for C5.2 START is unchanged (still requires
user explicit confirmation). The merge AUTHORIZATION is the part
that pre-Stage-6 was holding back.

Cross-stream notification sent separately: `MAIN_TERMINAL_TEACHING_PRESTAGE6_CLEARED_2026-04-26.md`.

## Game per-villain range bars — status update

Game's Phase A (mockup + UX design against synthetic per-villain
fixture) was unblocked at commit 14. Phase B (integration against
real teaching CONTENT_API per-villain composition) becomes feasible
when teaching ships v4.1.

No cross-stream notification needed for game right now — they're
already operating per `MAIN_TERMINAL_TO_GAME_2026-04-26-a.md`. They
don't gate on pre-Stage-6 gate clearance directly.

## Stage 4 transition — what's authorised vs what isn't

**Authorised now:**
- Owner review of 5 Stage 4/5/6 design DRAFTs at `4d939f1` + `362e70b`
- Commissioning of gto-expert + ml-architect agents to fill in
  poker/ML-judgment specifics on the DRAFTs (per locked Stage 4
  plan §11)
- Drafting Protocol B + C fully-filled prompts with reviewer pass
  + calibration exam construction
- Drafting Stage 5 retrain protocol fully-filled
- Drafting Stage 6 held-out test set fully-filled
- Drafting Pilot orchestration script fully-filled

**NOT authorised (still owner gate per locked plan):**
- Pilot dispatch (the 33-agent pilot run on 100 hands)
- Any actual labelling / training / model production
- Any cross-stream stream-changing-protocol directives

Owner can review on wake and authorise pilot dispatch when ready.

## Builder — what's next

Per the standing roadmap, after Stage 3.5 closure, the logic stream
has a few options:

1. **WAIT** — wait for owner direction on Stage 4 commissioning
2. **PRE-AUTHOR** — pre-fill some of the Stage 4 DRAFT specifics
   that benefit from logic-domain knowledge (e.g. integration test
   specs for the new commit 14 fields)
3. **OPPORTUNISTIC** — pick up any v2.5 backlog items that don't
   gate on Stage 4 (per `project_river_rats_v23_backlog.md`)

[**BUILDER DISCRETION:** orchestrator does not direct further; per
autonomous-advance directive, builder picks the highest-value
next move. Surface scope-doc if non-trivial.]

## Action

**Builder:**
1. M4 + M5 audit closure read by orchestrator (this doc) — Stage 3.5
   declared closed
2. Builder discretion on next move (see above)
3. Standing pattern continues for any new PR

**Orchestrator (me):**
1. Pre-Stage-6 gate cleared (this doc)
2. Cross-stream notification to teaching (separate doc)
3. Loop cadence dropped to 15-20 min per owner directive
4. When teaching ships C5.2 + C7 → notify game for Phase B
5. When owner authorises Stage 4 pilot: orchestrate pilot dispatch

**Teaching:** authorised to merge v4.1 once C5.2 + C7 + V3 reviews
all clear. C5.2 START still requires user confirmation per 3-gate
rule.

**Game:** Phase A continues at owner-paced UX iteration; Phase B
viable post teaching v4.1 ship.

**Owner:** the project transitioned overnight. Stage 3.5 is CLOSED.
All gates passed. Teaching merge authorised when their work
completes. Stage 4 ready for review. No emergency. Major milestone.

## References

- `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md` (`33272ff`) —
  audit-closure source
- `MAIN_TERMINAL_PR_9_MERGED_STAGE35_COMMITS_COMPLETE_2026-04-26.md`
  (`59c3fd9`) — prior milestone (commits done; audits next)
- `MAIN_TERMINAL_WAKE_STATUS_2026-04-26.md` — wake-up navigational
- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`)
  — locked Stage 4 plan; pilot dispatch is owner gate
- 5 Stage 4/5/6 design DRAFTs at `4d939f1` + `362e70b`
- 5 rollback tags on origin
