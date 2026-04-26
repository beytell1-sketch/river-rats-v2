---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #18 merged at afc815c — Task 4 (Stage 6 held-out v1.0.1) sealed as canonical; PR #16 auto-resolved; Task 4.2 v1.0.2 micro-correction directive (single-line H025 + hash re-lock + closure tally) before pilot use; Task 5 still queued post-Task-4.2
status: CONFIRMATION + DIRECTIVE — fix-forward Task 4.2 follows standing pattern; non-blocking on Task 5 prep but pilot use gates on v1.0.2
---

# PR #18 Merged — Task 4 v1.0.1 Sealed

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 18 (with #16 auto-resolved) |
| Title | Stage 4 prep Task 4.1: Stage 6 held-out v1.0.1 (APPROVE-WITH-NITS fix-forward) |
| Merge commit | `afc815c` on origin/master |
| Feature commit | `3bbef9e` (v1.0.1) preserved per `--merge` |
| Verdict commit | `cc247ac` (preserved on master) |
| Feature branch | `stage4-prep/stage6-holdout-fill-4-1` deleted from origin |
| Merge time | 2026-04-26 ~11:18 SAST |
| Rollback tag | `pre-pr18-merge-2026-04-26` at `cc247ac` (origin) |
| Final artifact (this seal) | `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` (v1.0.1 content, hash-locked) |

Pre-merge protocol-compliance checkpoint #4:
- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage4-prep/stage6-holdout-fill-4-1`
- ✅ Title cites APPROVE-WITH-NITS fix-forward
- ✅ Reviewer verdict APPROVE-WITH-NITS at `cc247ac` — all 7 prior items
  (2 HIGH + 4 MEDIUM + 1 LOW-MEDIUM) cleanly addressed empirically
- ✅ Independent reviewer dispatch (general-purpose with persona,
  different agent than v1.0 reviewer at `9758a99` and v1.0.1 author)
- ✅ Empirical verification: hash recompute (b775df2a... matches over
  47653 bytes), grep markers exactly 1 each, calibration manifest
  non-overlap re-run (21 fingerprints, 0 matches), 50 hands × 1 Board
- ✅ ML core preserved verbatim

PR #16 disposition: auto-resolved by PR #18 merge (different branch but
GitHub closed automatically per merge precedence — verified open list
post-merge shows only PR #19).

## Stage 4 prep progress

```
Task 1 (Protocol B v1.0.1)               ✅ sealed at dc6fa1f
Task 2 (Protocol C v1.0.1)               ✅ sealed at 435757f
Task 3 (Stage 5 retrain v1.0.1)          ✅ sealed at b639776
Task 4 (Stage 6 held-out v1.0.1)         ✅ sealed at afc815c ← just merged
Task 4.2 (Stage 6 held-out v1.0.2)       🆕 micro-correction — directive below
Task 5 (Pilot orchestration v1.0)        ⏳ queued — after Task 4.2
```

## Task 4.2 — v1.0.2 micro-correction directive

Per reviewer recommendation in `cc247ac`:

> "v1.0.2 micro-correction (single-line H025 header fix + hash re-lock
> + closure tally cleanup) before pilot evaluation use."

**Branch:** `stage4-prep/stage6-holdout-fill-4-2`
**Source:** v1.0.1 sealed content (now on master at `afc815c`)
**Target artifact:** `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md` (hash re-locked)

### Scope (3 items)

1. **H025 header pot-at-decision correction** — the inline body reframe
   says `pot now = 94.2`; pot odds 29.3% validates with `94.2`; FOLD
   conclusion unaffected. The header value `Pot at decision: 105.2bb`
   is inconsistent. Single-line fix: change `105.2` → `94.2` in the
   H025 header.

2. **Hash re-lock** — H025 header sits inside the hashed block, so the
   v1.0.1 hash `b775df2a...` invalidates after the H025 edit.
   Re-compute SHA256 over the modified test-set block; update the
   hash declaration line in the artifact.

3. **Closure section tally cleanup** — solver-sample tally drift in the
   closure section per reviewer NIT. Audit the closure prose; reconcile
   with the corrected header values.

### Optional (4 NITs from reviewer; address if cycle permits, otherwise
defer to v1.1 calibration material)

- H001 minor poker overstatement
- H027 inline self-correction artifact
- Solver sample FOLD swap is LOW-band (HIGH-band would be cleaner)
- (One more NIT enumerated in `cc247ac` verdict body)

### Lessons from Tasks 1-4 (apply to Task 4.2)

- Task 1 lesson: worked content self-consistency
- Task 2 lesson: memory references aligned to standing spec
- Task 3 lesson: cross-check referenced infrastructure against current
  state
- Task 3 numerical-rigour lesson: statistical claims need actual
  computation (1/√3 = SD ratio not variance ratio)
- **Task 4 lesson (new):** hashed-block edits require hash re-lock as
  a first-class step in the fix-forward checklist. The H025 issue
  exists because v1.0.1 header drifted from body; v1.0.2 must close
  that loop AND prove the hash is fresh.

### Acceptance criteria

1. H025 header reads `Pot at decision: 94.2bb`
2. Hash declaration line on the artifact matches a fresh SHA256
   recompute over the (now-corrected) test-set block
3. Closure section tally numbers reconcile with the corrected hands
4. Pre-flight: solver-sample diversity + non-overlap claims still hold
5. PR title cites `APPROVE-WITH-NITS micro-correction (v1.0.2)`

### Reviewer dispatch

Independent gto-expert reviewer, different general-purpose subagent
than v1.0.1 reviewer at `cc247ac`. Standing per-batch per-checkpoint
protocol applies.

### Estimated effort

~30-60 min (single-line edit + hash recompute + closure tally pass +
PR cycle).

### Sequencing

Task 4.2 is the immediate next task. **Task 5 (Pilot orchestration
v1.0) does NOT begin until Task 4.2 is sealed** — the held-out test
set is referenced by the pilot orchestration spec's evaluation
protocol, and we want the canonical v1.0.2 artifact pinned before
authoring evaluation prose.

## Cross-stream context — QC HIGH finding (separate doc)

Concurrent with PR #18 verdict, QC stream completed Phase 2 cross-
stream contract drift sweep on commit 14. **TWO HIGH-severity findings
surfaced on the commit 14 Finding B promotion path** — both pre-existing
(predate Stage 3.5 closure), neither warrants rollback (model behavior
unchanged, M4/M5 audits valid), but both block downstream stream work:

- **HIGH-1:** `_per_villain_composition` inner-key drift (producer
  emits `{tp_plus, medium, draw, air}` vs CONTENT_API documents
  `{tp_pct, medium_made_pct, draw_pct, air_pct}`)
- **HIGH-2:** Game adapter strips all underscore-prefixed keys
  (`real_teaching.py:48`) → multiway pathway dormant in live game flow

See companion doc `MAIN_TERMINAL_QC_HIGH_FINDING_ACK_CASCADE_2026-04-26.md`
for full ACK + directive cascade. **Builder is NOT directly affected
by HIGH-1 or HIGH-2** — those are cross-stream / consumer-side fixes
on teaching + game. The MEDIUM finding (aggregate flag derivation)
*is* logic-side; directive folded into Task 4.2 scope notes (see
companion doc).

## Action

**Builder:**
1. Begin Task 4.2 (Stage 6 held-out v1.0.2) on
   `stage4-prep/stage6-holdout-fill-4-2`
2. Apply Task 1-4 lessons (especially the new hash re-lock discipline)
3. Standing PR + 4-checkpoint protocol
4. Surface in comms when PR #20 opens
5. **Optional fold**: if desired, fold the QC MEDIUM aggregate-flag
   fix (`feature_extractor.py` post-line-2303 `_villain_chain_overflowed`
   aggregate derivation per `any(_per_villain_overflowed.values())`)
   into a separate small commit on the same branch — keeps it bundled
   with the Task 4.2 PR but on a separate commit for clean history.
   Reviewer can verify both. Otherwise queue for post-Task-5
   housekeeping. Builder's call.

**Orchestrator (me):**
1. PR #18 merged (this confirmation)
2. PR #16 auto-resolved (verified)
3. PR #19 disposition pending (separate doc)
4. QC HIGH cascade dispatched (separate doc + cross-stream comms)
5. Loop continues at 15-20 min cadence
6. Watch for PR #20 (Task 4.2) opening + verdict

**Owner:**
- 4 of 5 Stage 4 prep tasks sealed (Task 4 = canonical v1.0.1 NOW)
- Task 4.2 v1.0.2 micro-correction in flight (~30-60 min)
- Task 5 queued post-4.2
- Pilot dispatch still owner gate (pre-pilot QC sweep + all 5
  prep tasks sealed)
- QC stream now has 2 sweep cycles (Phase 1 ✅, Phase 2 ✅);
  Phase 3 (architecture stress) next per QC's standing protocol

## References

- PR #18 verdict (`cc247ac`): `GTO_REVIEW_VERDICT_PR_18_STAGE6_HOLDOUT_V1_0_1_2026-04-26.md`
- PR #16 fix-forward directive (`006a13e`): `MAIN_TERMINAL_PR_16_FIX_FORWARD_REQUIRED_2026-04-26.md`
- PR #15 closure (`b639776`): `MAIN_TERMINAL_PR_15_MERGED_TASK4_GREENLIGHT_2026-04-26.md`
- Stage 4 plan (`ee3d9f5`): `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`
- QC HIGH ACK (companion): `MAIN_TERMINAL_QC_HIGH_FINDING_ACK_CASCADE_2026-04-26.md`

**Status: PR #18 merged. Task 4 v1.0.1 sealed as canonical. Task 4.2
v1.0.2 directive issued. Task 5 queued. Builder begins Task 4.2 now.**
