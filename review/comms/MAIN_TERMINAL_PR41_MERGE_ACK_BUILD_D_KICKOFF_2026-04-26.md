---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (NOW Builder persona for Build D) · Owner (briefed) · QC stream
re: PR #41 (Build C v1.0.1) merging after triple-reviewer convergent APPROVE; PRE-DISPATCH rows #2/#3 RED → GREEN; PR #39 closed superseded; Build D kickoff signal (directive at fa280d6 active)
status: MERGE ACK + BUILD D KICKOFF SIGNAL — Build C v1.0.1 ships clean; 59-feature contract embedded in pilot corpus; pilot dispatch resume contingent on Build D + Phase A.5 spec edit
---

# PR #41 Merge ACK + Build D Kickoff Signal

## Triple-reviewer convergence — APPROVE clean

| Pipeline | Verdict | Key checks |
|----------|---------|------------|
| Builder's reviewer (240ae88) | APPROVE | V-C13 closed; reviewer verified 59-feature contract |
| QC pre-merge audit (PR #42) | APPROVE clean | V-C13 fully closed |
| Orchestrator ml-architect (REVIEWER_ML_ARCHITECT_PR41) | APPROVE clean | 59-feature contract enforced (module-load + per-record); SHA256 c93a41c4... matches; determinism preserved (same situation_ids); disjointness 0/0/0 overlaps; feature_extractor.py call correct (no silent fallback) |

**Convergent verdict.** All three pipelines independently confirm:
- Pilot corpus `feat_dict` has exactly 59 keys per record (not 45)
- All 4 v2.4 P1 blockers present (`nut_flush_block`,
  `flush_draw_block_pct`, `straight_draw_block_pct`,
  `nut_made_block_pct`)
- All v3.1 features that should be present are present
  (`villain_medium_made_pct`, `villain_range_capped`,
  `flush_draw_rank`, `is_preflop_aggressor`, `board_adjusted_hrp`)
- Determinism preserved (same SEED=20260426 → same 100-hand selection;
  identical situation_id list as v1.0)
- Disjointness preserved (0 overlaps with Stage 6 holdout, v2.3
  calibration, v2.3 anchor)
- Within-pilot uniqueness preserved (100 unique fingerprints)

## Merge decision

**MERGE PR #41.** No NITs. Same-velocity ship as Build B (clean
APPROVE).

**Post-merge state:**
- Master advances 240ae88 → <merge SHA>
- PRE-DISPATCH PREREQUISITES gate: rows #2/#3 RED → GREEN
- **PR #39 closes as superseded** (don't merge v1.0; v1.0.1 is
  canonical)
- Remaining gaps for pilot dispatch: Build D (V-X2) +
  Phase A.5 spec edit
- Both can run in parallel:
  - Build D: builder-owned (directive at fa280d6 ACTIVE)
  - Phase A.5 spec edit: orchestrator-owned (post-Build-D for
    fixture path reference)

## Build D kickoff signal

Build C v1.0.1 sealing unblocks Build D per directive
`MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`
(master `fa280d6`). Key reminders (full directive in the comm):

- **File:** `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl`
- **Branch:** `stage4-pre-dispatch/phase-a5-partial-fold-fixtures`
- **5 hands**, each with explicit `<position>: fold` in `prior_actions`
  + `villain_positions` lists LIVE villains only
- **Diversity:** mix of street/folded-position/live-composition
  (per directive guidance)
- **Disjointness verification** + **hash-lock** per Build C pattern
- **Reviewer flavour:** gto-expert OR ml-architect for corpus
  structure + diversity + per-fixture validity
- **TC-15 multi-expert recommended** per QC's standing offer

**Estimated effort:** ~30-45 min build + ~30-45 min review = ~1-1.5h
total

## Build velocity recap (Stage 4 prep)

| Build | Authoring | Review cycle | Total |
|-------|-----------|--------------|-------|
| Build A (Protocol B pilot) | ~30 min | ~45 min | ~1h15min |
| Build B (Protocol C pilot) | ~15 min | ~25 min | ~40 min (33% faster) |
| Build C v1.0 (corpus, superseded) | ~10 min | ~10 min before MEDIUMs | ~20 min |
| Build C v1.0.1 (V-C13 fix) | ~8 min | ~18 min | ~26 min |
| Build D (estimated) | ~30-45 min | ~30-45 min | ~1-1.5h |

Pattern improvement is real. Build A established the recipe; Builds B/C/v1.0.1 all benefited.

## Pilot dispatch resume — updated dependency list

1. ✅ Build A — SEALED at 2ea67d0
2. ✅ Build B — SEALED at 3241413
3. ✅ Build C v1.0.1 — SEALING (this commit); **PRE-DISPATCH rows #2/#3 GREEN**
4. ⏸️ PR #39 (Build C v1.0) — closing as superseded
5. 🔥 Build D — ACTIVE per directive fa280d6 (~1-1.5h)
6. 🔥 Phase A.5 spec edit — orchestrator-owned, post-Build-D
   (~5-10 min)
7. PRE-DISPATCH gate re-check
8. Phase A.1-A7 preflight begins

**Total ETA to pilot dispatch resume:** ~1.5-2h from now (~19:00 SAST → ~20:30-21:00 SAST).

## QC PR #42 — Path B bundle in this commit

QC's audit comm (`QC_PRE_MERGE_AUDIT_PR41_2026-04-26.md`) bundled
into orch commit per Path B. Closing PR #42 as no-op after this
commit lands.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 35 | Build A | ✅ SEALED | Logic builder |
| 36 | Build B | ✅ SEALED | Logic builder |
| 37 | Build C v1.0 (PR #39) | ✅ CLOSED — superseded | Logic builder |
| 40 | Build C v1.0.1 (PR #41) | ✅ SEALING — this commit | Logic builder |
| 41 | V-X2 spec edit (Phase A.5) | 🔥 QUEUED post-Build-D | Orchestrator |
| 42 | Build D — 5-hand partial-fold MW fixtures | 🔥 ACTIVE — directive at fa280d6 | Logic builder |

## Action

**Logic builder:**
1. Build C v1.0.1 SEALED clean
2. Pick up Build D per directive `fa280d6` immediately
3. Standing per-batch protocol (PR + dual/triple-reviewer + merge)
4. Surface `BUILDER_BUILDS_ABCD_COMPLETE_2026-04-26.md` after Build D
   ships (final builder signal before pilot dispatch resumes)

**Orchestrator (me):**
1. PR #41 merge + close PR #39 + close PR #42 + this ack shipped
   (this commit)
2. Watch for Build D PR drop (~30-45 min ETA)
3. Dispatch gto-expert OR ml-architect reviewer at Build D PR open
4. After Build D merges: write Phase A.5 spec edit + push
5. Re-issue pilot dispatch directive (Phase A.1-A7 preflight resumes)

**QC stream:**
- Continue Layer 1+2 mode for Build D PR audit
- V-D1...V-D3 vectors; per-fixture validity + diversity + disjointness
- TC-15 multi-expert offer standing (recommended per Build D directive)
- Same Path B bundle pattern

**Owner:**
- Build C v1.0.1 SHIPPED clean (triple-reviewer convergent APPROVE)
- 59-feature contract now embedded in pilot corpus
- Build D + Phase A.5 spec edit ≈ 1.5-2h to pilot dispatch resume
- All 4 builds + spec edit unblock the pilot

## References

- PR #41: `https://github.com/beytell1-sketch/river-rats-v2/pull/41`
- PR #42 (QC audit, Path B bundled): `review/comms/QC_PRE_MERGE_AUDIT_PR41_2026-04-26.md`
- Builder's reviewer: master `240ae88`
- ml-architect verdict: `review/comms/REVIEWER_ML_ARCHITECT_PR41_2026-04-26.md`
- Build D directive: `fa280d6` (`MAIN_TERMINAL_BUILD_D_DIRECTIVE_PARTIAL_FOLD_FIXTURES_2026-04-26.md`)
- V-X2 lookup: `review/comms/V_X2_PARTIAL_FOLD_LOOKUP_2026-04-26.md`
- New corpus SHA: `c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40` (was `492154...ef4b`)
- New corpus bytes: 173,079 (was 131,835; +41,244 from 14×100 expansion)

**Status: PR #41 MERGING. PRE-DISPATCH rows #2/#3 GREEN. PR #39
closing as superseded. Build D begins NOW per directive fa280d6.**
