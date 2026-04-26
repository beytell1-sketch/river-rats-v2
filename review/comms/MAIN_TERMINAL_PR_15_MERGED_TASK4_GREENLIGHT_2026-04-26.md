---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #15 merged (with PR #14 auto-resolved as ancestor) — Stage 5 retrain protocol v1.0.1 sealed; Task 3 complete; Task 4 (Stage 6 held-out test set) greenlit; rollback tag stage4-prep-pre-task3-merge saved
status: CONFIRMATION + GREENLIGHT — Stage 4 prep 3/5 tasks done; builder may begin Task 4 (Stage 6 held-out v1.0)
---

# PR #15 Merged — Task 3 (Stage 5 retrain v1.0.1) Sealed

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 15 (with #14 auto-resolved) |
| Title | Stage 4 prep Task 3.1: Stage 5 retrain v1.0.1 (REQUEST-CHANGES fix-forward) |
| Merge commit | `b639776` on origin/master |
| Feature commits | `9e6213f` (v1.0.1) + `a7a62fa` (v1.0) — both preserved per `--merge` |
| Verdict commit | `ce73f22` (preserved on master) |
| Feature branches | both deleted from origin |
| Merge time | 2026-04-26T07:47:51Z (SAST 09:47) |
| Rollback tag | `stage4-prep-pre-task3-merge` at `9f8457e` (origin) |
| Final artifact | `review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md` (914 lines) |

Pre-merge protocol-compliance checkpoint #4:

- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN (after compute settle)
- ✅ Branch `stage4-prep/stage5-retrain-fill-3-1`
- ✅ Title cites REQUEST-CHANGES fix-forward
- ✅ Verdict APPROVE on PR #15 (`ce73f22`)
- ✅ Provenance line present (independent reviewer)
- ✅ All 3 MEDIUM findings (column-count, anchor inventory,
  variance math) cleanly addressed
- ✅ No new MEDIUMs introduced
- ✅ ML core preserved verbatim

## Stage 4 prep progress

```
Task 1 (Protocol B v1.0.1)               ✅ sealed at dc6fa1f
Task 2 (Protocol C v1.0.1)               ✅ sealed at 435757f
Task 3 (Stage 5 retrain v1.0.1)          ✅ sealed at b639776 ← just merged
Task 4 (Stage 6 held-out v1.0)           🆕 greenlit — NEXT
Task 5 (Pilot orchestration v1.0)        ⏳
```

## Greenlight: Task 4 (Stage 6 held-out test set v1.0)

Builder may begin **Task 4** per their sequential plan.

**Source:** `review/comms/STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md`
**Branch:** `stage4-prep/stage6-holdout-fill`
**Target artifact:** `review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md`

Task 4 is the longest of the 5 — it includes authoring 50 hands
(per the locked Stage 4 plan §D3: independent GTO expert pool
authoring + non-overlap with reference / calibration / pilot /
training corpora + SHA256 hash-locked).

Same workflow as Tasks 1-3:
1. Author dispatch (independent GTO expert pool)
2. Reviewer dispatch (different gto-expert)
3. PR (per standing per-batch protocol)
4. Orchestrator merge on APPROVE
5. Fix-forward if APPROVE-WITH-NITS / REQUEST-CHANGES

Task 4 specifics flagged in the draft:
- 50-hand authoring (the actual hands, not just the protocol)
- Action distribution targets (FOLD/CHECK/CALL/BET/RAISE)
- Confidence band targets (60% HIGH / 30% MEDIUM / 10% LOW)
- Solver verification on 10-hand sample
- SHA256 hash + lock for permanent test-set immutability
- Non-overlap verification against:
  - 40-hand reference set
  - 24-hand calibration set
  - 100-hand Stage 4 pilot corpus (when authored)
  - v2.x training corpora

## Task 4 estimated effort

Per the locked Stage 4 plan §"Estimated effort":

> "Task 4 (Stage 6 held-out fill): ~2-3 h"

Longest task in the prep arc because of the 50-hand authoring +
non-overlap verification.

## Carry-forward (post-Task-3)

Same carry-forward list (Anti-pattern #11, 4B-rate floor, MW-30
restatement, EV-cost boundary, κ trail-grading) folds into Task 5
wrap-up commit / pilot calibration phase.

Task 3-specific NITs:
- Bouthillier 2021 oversells "3 seeds for variance estimation"
  (Item B) — fold into Task 5 wrap or v1.1 calibration material
- ±2pp vs cv_std statistical nuance (Item D) — UNCERTAIN tag
  acknowledges; acceptable
- Prereq #3 auto-rollback tagging (Item G) — could explicitly
  assign to orchestrator-pre-Stage-5 step
- Mode E MW baseline number gap (Item F) — could be addressed by
  Prereq #6 OR cite specific MW-accuracy number

## Cross-stream + QC — unchanged

Teaching at `0b6d4d3` (held). Game at `021b302`. QC stream
activated 2026-04-26 (per `MAIN_TERMINAL_QC_STREAM_LIVE_2026-04-26.md`
at `ed0fc4b`) — QC ready for Phase 0 comms ingestion when owner
launches the QC terminal.

QC's first-run priority will be audit-trail integrity sweep on
PRs #5–#9 (overnight Stage 3.5). It can also retrospectively audit
PRs #11/#13/#15 (Stage 4 prep merges) when active.

## Action

**Builder:**
1. Begin Task 4 (Stage 6 held-out test set v1.0 author dispatch) on
   `stage4-prep/stage6-holdout-fill`
2. Apply Task 1-3 lessons:
   - Worked content self-consistency (Task 1 lesson)
   - Memory alignment for sizings (Task 2 lesson)
   - Cross-check referenced resources against current code/data
     (Task 3 lessons: column counts, anchor IDs)
   - Numerical/statistical rigour (Task 3 MEDIUM-NIT lesson)
3. Standing PR pattern + 4-checkpoint protocol
4. Multi-expert author dispatch encouraged for the 50-hand authoring
   (independent agents reduce systematic-bias risk per Stage 4 plan
   protocol-diversity principle)

**Orchestrator (me):**
1. PR #15 merged (this confirmation)
2. Loop continues at 15-min cadence
3. Watch for PR #16 (Task 4) opening + verdict

**Owner:**
- 3 of 5 Stage 4 prep tasks complete
- v1.0.1 of all 3 protocol/spec docs production-ready
- Pilot dispatch still owner gate (unchanged)
- QC stream ready for Phase 0 activation when you launch the QC
  terminal

## References

- `MAIN_TERMINAL_PR_14_FIX_FORWARD_REQUIRED_2026-04-26.md` (`9f8457e`)
  — fix-forward directive
- `MAIN_TERMINAL_PR_13_MERGED_TASK3_GREENLIGHT_2026-04-26.md` (`0d9bdfb`)
  — Task 2 closure pattern
- `BUILDER_STAGE4_PREP_SCOPE_2026-04-26.md` (`1c63d93`) — builder
  execution plan
- `MAIN_TERMINAL_QC_STREAM_LIVE_2026-04-26.md` (`ed0fc4b`) — QC
  stream announcement
