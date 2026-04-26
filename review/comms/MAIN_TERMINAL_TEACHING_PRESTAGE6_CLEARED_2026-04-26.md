---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Teaching builder · Owner
re: Pre-Stage-6 gate CLEARED at orchestrator side; teaching v4.1 merge to teaching/master is now AUTHORISED post C5.2/C7 + V3 reviews; C5.2 START rule unchanged (3-gate user confirmation)
status: CROSS-STREAM UPGRADE — teaching's upstream block is fully lifted; merge authorisation now in place, waiting only on teaching's own internal C5.2/C7 + V3 review chain
---

# Teaching — Pre-Stage-6 Gate Cleared (Merge Authorised)

## What changed

Pre-Stage-6 gate (HOLD #4) cleared 2026-04-26 (this morning) per
`MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md`.
Stage 3.5 declared CLOSED at master `59c3fd9` post M4 + M5 audits
both PASS.

Teaching's upstream block is now fully lifted:

- **HOLD #1** (Stage 3.5 closure) ✅ CLEARED
- **HOLD #4** (orchestrator pre-Stage-6 gate) ✅ CLEARED
- **HOLD #5** (commit 14 multiway field promotion) ✅ CLEARED
- **HOLD #2** (nut_flush_block) ✅ CLEARED (long ago)

Net: teaching is **merge-authorised** for v4.1 — pending only
teaching's own internal completion of C5.2 + C7 + V3 reviews +
SHIP REPORT update.

## What this changes for teaching's flow

**Before:** even if teaching completed C5.2 + C7 + V3 reviews,
teaching still had to wait for orchestrator's pre-Stage-6 gate
before merge.

**Now:** teaching can proceed through its sequence and merge as
soon as the internal sequence completes:

```
[teaching's current state: held at 0b6d4d3, awaiting user
 confirmation per 3-gate rule for C5.2 START]
  → C5.2 (real-row F3/F4 fixture swap)
  → V3 per-commit review on C5.2 = APPROVE
  → C7 (hero_range_percentile wording cleanup, doc-only)
  → V3 per-commit review on C7 = APPROVE
  → SHIP REPORT update (drop PRE-VERIFICATION marker on §5.3)
  → Open PR teaching/v4-1-nan-render → master
  → Merge teaching v4.1 ship
```

Note: the C5.2 START still requires the 3-gate rule:

1. ✅ Commit 14 on v2 master (long since cleared)
2. ✅ Orchestrator cross-stream notification (this doc + earlier
   `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md`)
3. ⏳ **Explicit user confirmation** — teaching loop should surface
   "begin C5.2?" to owner; await go-ahead

**The merge authorisation upgrade does NOT bypass the 3-gate
START rule.** C5.2 still starts only on user confirmation.

## What this means for HOLD #6 (Path B)

HOLD #6 (Teaching Path B / range_position_desc rename) is INDEPENDENT
of pre-Stage-6 gate. Path B has its own trigger and is not gated by
Stage 3.5 closure. Continue to treat Path B as a separate workstream
post-v4.1-ship.

## Cross-stream contract from commit 14 + commit 16 (telemetry split)

Reminder of upstream contract teaching depends on:

- `_per_villain_folded` — Dict[str, bool] (commit 14)
- `_per_villain_composition` — Dict[str, Dict[str, float]] (commit 14)
- `_per_villain_overflowed` — Dict[str, bool] (commit 14)

Plus (for telemetry / classifier consumers — not directly read by
teaching's renderer):

- `delayed_probe` predicate now HU-only (commit 16) — teaching does
  not consume this directly; mention only for awareness

Teaching's renderer reads only the three commit-14 fields. C5.2
fixture swap pulls real commit-14-era rows from
`extract_all_features` into F3/F4 sentinel fixtures.

Cross-stream verification recommended before C5.2 (already in
prior notification): run `extract_all_features` on a 3-way multiway
fixture, assert all three keys present, then proceed.

## Action

**Teaching builder (when /loop surfaces or owner directs):**

1. Read this doc + prior notification at `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md`
2. Confirm session launched from `~/river-rats-teaching/` (V3
   reviewer subagent available)
3. ASK user "begin C5.2 fixture swap?" — wait for explicit go
4. On user go: cross-stream contract verification → C5.2 fixture
   swap → V3 review → C7 wording → V3 review → SHIP REPORT update
5. Open PR teaching/v4-1-nan-render → master; merge per teaching's
   own discipline (no orchestrator gate now)

**Owner (when ready):**
- Confirm or hold on C5.2 START
- Teaching's sequence is bounded (C5.2 data-only + C7 doc-only) so
  total time is small once started

**Orchestrator (me):**
- Pre-Stage-6 gate cleared (parent doc)
- Loop cadence dropped to 15-20 min per owner directive (faster
  feedback)
- When teaching ships v4.1: write `MAIN_TERMINAL_TO_GAME_*` for
  Phase B trigger
- Awaits owner direction on Stage 4 pilot dispatch authorisation

## References

- `MAIN_TERMINAL_PRE_STAGE6_GATE_CLEARED_STAGE35_CLOSED_2026-04-26.md` —
  parent gate-clearance doc
- `MAIN_TERMINAL_TEACHING_COMMIT14_LANDED_2026-04-26.md` — initial
  cross-stream unblock signal
- `MAIN_TERMINAL_TEACHING_C7_HOLD_2026-04-25.md` — defines C5.2 →
  C7 → SHIP REPORT sequence
- `MAIN_TERMINAL_TEACHING_LOOP_SETUP_2026-04-25.md` — 3-gate START
  rule
- `BUILDER_M4_M5_AUDIT_CLOSURE_2026-04-26.md` — Stage 3.5 closure
  audit evidence
