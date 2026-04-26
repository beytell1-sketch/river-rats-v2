---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder · Owner
re: PR #13 merged (with PR #12 auto-resolved as ancestor) — Protocol C v1.0.1 sealed; Task 2 complete; Task 3 (Stage 5 retrain protocol) greenlit; rollback tag stage4-prep-pre-task2-merge saved
status: CONFIRMATION + GREENLIGHT — Stage 4 prep Task 2 sealed; both labelling protocols (B + C) at v1.0.1 production-ready; builder may begin Task 3 (Stage 5 retrain v1.0)
---

# PR #13 Merged — Task 2 (Protocol C v1.0.1) Sealed

## Merge confirmation

| Field | Value |
|---|---|
| PR # | 13 (with #12 auto-resolved) |
| Title | Stage 4 prep Task 2.1: Protocol C v1.0.1 (APPROVE-WITH-NITS fix-forward) |
| Merge commit | `435757f` on origin/master |
| Feature commits | `2cd46aa` (v1.0.1) + `d77a95e` (v1.0) — both preserved per `--merge` |
| Verdict commit | `2738fcc` (preserved on master) |
| Feature branches | both deleted from origin |
| Merge time | 2026-04-26T06:44:50Z (SAST 08:44) |
| Rollback tag | `stage4-prep-pre-task2-merge` at `31aa43c` (origin) |
| Final artifact | `prompts/protocol_c_adversarial_elimination_v1_0.md` |

PR #12 auto-resolved as merged per the same GitHub ancestor-merge
pattern as Task 1's PR #10 → PR #11.

Pre-merge protocol-compliance checkpoint #4:

- ✅ HARD branch check passed (`master`)
- ✅ PR state OPEN / MERGEABLE / CLEAN
- ✅ Branch `stage4-prep/protocol-c-fill-2-1`
- ✅ Title cites APPROVE-WITH-NITS fix-forward
- ✅ Verdict APPROVE on PR #13
- ✅ Provenance line present (independent reviewer ≠ v1.0 author / reviewer)
- ✅ MEDIUM #1 (raise-sizing taxonomy) cleanly resolved
- ✅ 2 UNCERTAIN tag downgrades bundled per PR #12 reviewer recommendations
- ✅ No new MEDIUMs introduced
- ✅ Cross-protocol consistency verified

## Task 2 final disposition

✅ **Task 2 (Protocol C fill) COMPLETE** at v1.0.1.

Production artifact: `prompts/protocol_c_adversarial_elimination_v1_0.md`.

Both labelling protocols now at v1.0.1 production-ready:
- Protocol B (composition-first): `prompts/protocol_b_composition_first_v1_0.md`
- Protocol C (adversarial-elimination): `prompts/protocol_c_adversarial_elimination_v1_0.md`

Plus Protocol A baseline (`prompts/gto_labeller_v3.1.md`) which is
unchanged.

The 3-protocol matrix for the Stage 4 pilot is now fully drafted.

## Greenlight: Task 3 (Stage 5 retrain protocol v1.0)

Builder may begin **Task 3** per their sequential plan.

**Source:** `review/comms/STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md`
**Branch:** `stage4-prep/stage5-retrain-fill`
**Target artifact:** `review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md`
(or similar finalised path)

Same workflow as Tasks 1 + 2:
1. Author dispatch (general-purpose + ml-architect persona)
2. Reviewer dispatch (independent ml-architect)
3. PR (per standing per-batch protocol)
4. Orchestrator merge on APPROVE
5. Fix-forward if APPROVE-WITH-NITS

Lessons from Tasks 1 + 2 (apply to Task 3):
- Worked content must be self-consistent (Protocol B mathematical
  consistency lesson)
- Threshold values + memory references must align with standing
  spec (Protocol C raise-sizing lesson)
- Author should run a self-consistency pass before publishing PR
- Reviewer flags MEDIUM-severity → fix-forward, not defer

Task 3 specifics flagged in the draft:
- Hyperparameters review (locked v2.2 baseline; verify or revise
  for v2.4 +4 features)
- Seed selection rationale (currently 42/2026/1729 placeholders)
- Train/CV split strategy (same vs different per seed)
- Threshold values: ±2pp accuracy spread, top-10 Spearman ≥ 0.8 —
  validate empirically vs theoretically
- Ensemble vs median single-seed decision
- Rollback investigation procedures per gate failure mode

## Stage 4 prep progress

```
Task 1 (Protocol B v1.0.1)        ✅ sealed at dc6fa1f
Task 2 (Protocol C v1.0.1)        ✅ sealed at 435757f ← just merged
Task 3 (Stage 5 retrain v1.0)     🆕 greenlit — NEXT
Task 4 (Stage 6 held-out v1.0)    ⏳
Task 5 (Pilot orchestration v1.0) ⏳
```

2 of 5 Stage 4 prep tasks done. 3 remaining.

## Carry-forward (post-Task-2)

| Item | Source | Disposition |
|---|---|---|
| Protocol B Anti-pattern #11 (per-villain vs merged composition naming) | PR #10 NIT | Task 5 wrap-up commit |
| Protocol B 4B-rate floor | PR #10 NIT | Task 5 wrap-up (pilot orchestration design parameter) |
| Protocol B MW-30 rule restatement (LOW) | PR #11 verdict | Wrap-up |
| Protocol C WEAK-tier "<5% EV cost" boundary fuzziness (LOW) | PR #12 verdict | v1.1 calibration material |
| Protocol C κ ≥ 0.65 trail-grading target (LOW) | PR #12 verdict | Pilot calibration: measure + report, no go/no-go gate at v1.0 |

These are LOW/NIT — Task 5 wrap-up commit is the right home for
them, not blockers on Tasks 3 + 4.

## Cross-stream — unchanged

Teaching at `0b6d4d3` (held). Game at `021b302`. No cross-stream
impact from Stage 4 prep tasks.

## Action

**Builder:**
1. Begin Task 3 (Stage 5 retrain protocol v1.0 author dispatch) on
   `stage4-prep/stage5-retrain-fill`
2. Apply Task 1 + 2 lessons (self-consistency, memory alignment)
3. Standing PR pattern + 4-checkpoint protocol

**Orchestrator (me):**
1. PR #13 merged (this confirmation)
2. Loop continues at 15-min cadence
3. Watch for PR #14 (Task 3) opening + verdict

**Owner:**
- 2 of 5 Stage 4 prep tasks complete
- v1.0.1 of both labelling protocols production-ready for owner review at convenience
- Pilot dispatch still owner gate (unchanged)

## References

- `MAIN_TERMINAL_PR_12_FIX_FORWARD_REQUIRED_2026-04-26.md` (`31aa43c`)
  — fix-forward directive
- `MAIN_TERMINAL_PR_11_MERGED_TASK2_GREENLIGHT_2026-04-26.md` (`dbcbf0c`)
  — Task 1 closure pattern
- `BUILDER_STAGE4_PREP_SCOPE_2026-04-26.md` (`1c63d93`) — builder
  execution plan
- 6 rollback tags on origin (5 Stage 3.5 + 2 Stage 4 prep — minor
  count discrepancy from including pre-13-3-4 + pre-13-3-5)
