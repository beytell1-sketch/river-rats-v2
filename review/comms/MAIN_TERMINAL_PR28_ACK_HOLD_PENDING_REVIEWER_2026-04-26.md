---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner (briefed)
re: PR #28 Task 5 v1.0.1 pre-dispatch fix-forward ACK at d1b8323 — clean 5-fix surgical patch (M-1 + L-1/L-8/L-11/L-12); HIGH-4 cross-stream prereq correctly removed; holding merge pending reviewer
status: ACK + HOLD — PR #28 acknowledged; merge awaits reviewer APPROVE; standing per-batch protocol
---

# PR #28 Task 5 v1.0.1 — ACK

## Headline

PR #28 opened at `d1b8323` per directive `309ad35`. 1 file, +95/-11
lines. All 5 directive items addressed cleanly:
- M-1 (MEDIUM) — Stage 5 contract terminology line 586 fix
- L-1 — Cross-protocol output-path firewall in Labeller briefs
- L-8 — Tool restrictions across all 6 phase agent briefs (Task 4.5 whitelist-or-raise discipline)
- L-11 — API-tier + model-selection promoted to PRE-DISPATCH PREREQUISITES rows #14 + #15
- L-12 — `docs/LABELLING_PIPELINE.md` path correction at 4 references

Frontmatter bumped to v1.0.1 with full changelog block. **HARD
branch check verified pre-commit.** Mergeable CLEAN. Holding pending
reviewer per standing per-batch protocol.

## What's strong about this PR

1. **Cross-stream awareness:** HIGH-4 cross-stream prereq from
   v1.0 reviewer NITs correctly REMOVED — HIGH-4 SEALED via PR #26
   `d3fcd02` so it's no longer a gate. Builder integrated the merge
   state cleanly.

2. **5 v1.0 NITs from PR #24 verdict folded into changelog:**
   - Phase B band-tightness — defer v1.1 (preflight 5-call gate
     mitigates)
   - HIGH-4 cross-stream prereq — REMOVED (no longer needed)
   - Adjudicator role 1+3 dispatch-ID — partially addressed via
     tool restrictions
   - LABELLING_PIPELINE.md path — ADDRESSED (L-12)
   - Cost telemetry as new infrastructure ask — deferred to
     orchestrator commission-time

   Honest disposition; deferrals justified.

3. **PRE-DISPATCH PREREQUISITES grew from 13 → 15 rows** with
   API-tier + model-selection promotion (L-11). Pilot Orchestrator
   brief read-list updated correspondingly: "ALL 13 prereqs" → "ALL
   15 prereqs" — cross-reference discipline preserved.

4. **Tool restrictions consistent** across all 6 brief types
   (Labeller A canonical + B/C inherit + Highlighter H1/H2 +
   Reviewer + Adjudicator per-role 1/2/3). Whitelist-or-raise
   discipline propagated from Task 4.5 across the pilot
   orchestration spec.

## What's pending

1. **Independent reviewer dispatch by builder** — recommended:
   ml-architect or orchestration-engineering persona; verify the 5
   directive items + check no new MEDIUM/HIGH introduced
2. **Reviewer verdict on master** (verdict commit precedes merge)
3. **Orchestrator merge on APPROVE** via atomic bash flow with
   rollback tag
4. If APPROVE-WITH-NITS / REQUEST-CHANGES: fix-forward via v1.0.2
   per quality default

## Pilot-dispatch gate progress (after PR #28 → 9/9 SEALED minus QC sweep)

```
✅ Phase 2 HIGH-2 (game adapter passlist):           SEALED
✅ Phase 3 HIGH-1/2/3 + Phase 1 HIGH (Task 4.5):     SEALED
✅ Task 4.3 v1.0.3 NITs:                             SEALED
✅ Task 5 (Pilot orchestration v1.0):                SEALED
✅ HIGH-4 (cross-stream aggregate semantics):        SEALED
🟡 Task 5 v1.0.1 pre-dispatch fixes:                 ON PR #28 — pending reviewer
⏳ Phase 2 HIGH-1 (teaching renderer translation):    pending teaching
⏳ HOLD #21 / #24 (post-pilot):                       deferred
⏳ QC pre-pilot sweep clean (Phase 5):                framework published; awaits HIGH-1 + v1.0.1 land
```

After PR #28 merges:
- Pilot-dispatch gate at 9/9 SEALED on logic side
- Only teaching HIGH-1 + QC Phase 5 sweep remain before owner
  pilot-dispatch authorization

## HOLD register update

| # | Item | Status | Owner |
|---|---|---|---|
| 26 | Task 5 v1.0.1 pre-dispatch fix-forward | 🟡 ON PR #28 — pending reviewer | Logic builder |

## Cross-stream context

- **Teaching at `b75d867`** — held; HIGH-1 directive shipped;
  awaiting renderer translation fix (last cross-stream HIGH)
- **Game at `e7ebc4c`** — Phase B integration ACK'd; multiway
  playtest queued
- **QC stream Phase 4 dynamic /loop** — 6 TC-15 demonstrations
  consistent; expected pre-merge audit on PR #28 next

## Action

**Builder:**
1. Dispatch reviewer on PR #28 per standing pattern
2. Surface verdict in `review/comms/` when it lands
3. **After PR #28 sealed:** all logic-side pilot-dispatch gates
   clear (only teaching HIGH-1 + QC Phase 5 + owner remaining)
4. Optional: HOLD #27 (monotone-True doc v1.1 NIT) +
   HOLD #21 FEATURE_COLUMNS investigation (post-pilot housekeeping)

**Orchestrator (me):**
1. PR #28 ACK shipped (this commit)
2. Hold PR #28 merge pending reviewer verdict
3. On reviewer APPROVE → tag rollback + merge via atomic bash flow
4. Watch for incoming teaching HIGH-1 fix + game multiway playtest
   signal + QC pre-merge audit on PR #28
5. **Queue: orchestrator-side note for owner** that pilot-dispatch
   gate at 9/9 logic + 1 cross-stream + 1 QC remaining = 3 items
   to clear before owner authorization

**Owner:**
- Builder maintaining excellent cadence (Task 5 v1.0.1 ~30 min
  from directive to PR — surgical scope met estimate)
- After PR #28 sealed → only teaching HIGH-1 + QC Phase 5 sweep
  + your pilot-dispatch authorization

## References

- Task 5 v1.0.1 directive: `309ad35`
  (`MAIN_TERMINAL_PR24_MERGED_TASK5_V1_0_1_DIRECTIVE_2026-04-26.md`)
- PR #28 commit: `d1b8323`
- HIGH-4 SEALED reference: `d3fcd02`
- Pilot orchestration spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md`

**Status: PR #28 ACK'd; held pending reviewer verdict.**
