---
date: 2026-05-10
from: Main terminal (orchestrator; owner-adjudication relay + generator-fix dispatch)
to: LEAD-PROGRAMMER (architect-hat lead for generator fix; programmer-hat for `scripts/generate_hu_situations.py` patch) · QC stream · Owner (ratification record)
re: (a) HU-1.5-LK-10 owner adjudication = CALL with solver-verification flag pending; (b) Phase 1.5-D.3 generator-fix dispatch (board-field propagation bug — BLOCKS full batch per QC PR #342 SHOULD_FIX); (c) solver-verification queue update
status: ADJUDICATION + DIRECTIVE — fire LEAD-PROGRAMMER on generator fix — fire now
---

# (a) HU-1.5-LK-10 owner adjudication

## Spot

Phase 1.5-D.3 PILOT (PR #339 merged at master `a2b97e2`) routed HU-1.5-LK-10 to owner-arbitration:
- **Sonnet 5-labeller majority (3-2): CALL**
- **Opus tier-up: FOLD**
- Same hero/board as 1.5-D.2 HU-6.5 owner-adjudicated spot (CALL); LK-10 differs by villain-bet-sizing (~112% pot overbet vs anchor's 75% pot bet)

## Spot detail (full hand)

- **Hero**: Qd9h (BTN, 100bb effective)
- **Board**: 7h 6c 5s 2d 8d (river)
- **Action**: BTN opens 2.5bb → BB calls. Flop 7h6c5s: BB checks → BTN bets 1.4bb (25%) → BB calls. Turn 2d: BB checks → BTN bets 2.7bb (33%) → BB calls. **River 8d: BB leads 56.25bb (~112% pot overbet)** (vs anchor's 75% pot bet at 20.6bb).
- **Pot odds**: ~35% required to call (vs anchor's 30%)
- **Hero's hand**: nut straight 5-6-7-8-9 on flush-completing runout. Qd is a weak diamond blocker.

## Online research (no live solver; solver currently offline)

Owner directed online research per "can this hand be researched online? perhaps there some online expert opinions on similar situations":

Key findings from GTO Wizard / poker theory ([Principles of River Play](https://blog.gtowizard.com/principles-of-river-play/), [Art of Bluff Catching](https://blog.gtowizard.com/the-art-of-bluff-catching/), [Why You're Bluffing the River Wrong](https://blog.gtowizard.com/why_youre_bluffing_the_river_wrong_with_bricked_flush_draws_in_cash_games/)):

1. "A well-constructed polarized betting range should make you roughly indifferent to calling with medium-strength hands... against an optimal betting range, you'll have roughly the same EV whether call or fold." → confirms HU-1.5-class spots are genuinely close at the optimum.
2. "Overbets exceeding pot size appear when ranges polarize heavily toward nuts or air... draws are complete enabling aggressive polarization."
3. 75% vs 112% sizing comparison: 75% requires 30% caller equity (~30% bluff freq); 112% requires 35% caller equity (~35% bluff freq).
4. Population-wise, "missed flush draws" overbluffing is well-documented on flush-completing rivers (per the Upswing/GTO Wizard analyses).

## Owner decision

**Final label: CALL.** Reason (per owner): "flag this hand and other hand to check on solver. mark as call for now."

Solver-verification flag: solver currently offline; **flag this spot for solver review when available** alongside HU-6.5.

## Effect on consensus.jsonl

The data already records consensus_action = null on HU-1.5-LK-10 (per builder routing to owner-arb). This comm ratifies the consensus_action = CALL with a SOLVER-VERIFICATION-PENDING annotation. Builder updates consensus.jsonl in the generator-fix re-pilot PR (next workstream) to reflect CALL for HU-1.5-LK-10.

---

# (b) Phase 1.5-D.3 generator-fix dispatch

## Context

QC PR #342 (master `2f04f34`): PASS-WITH-FINDINGS · 0/1/0 SHOULD_FIX. The SHOULD_FIX is the generator bug surfaced by the builder report:

**The bug (per builder report)**: `scripts/generate_hu_situations.py` produces 50 lookalike rows where `variation_param` field describes board-runout / SPR / villain-action mutations in prose (e.g., "replaced last-street brick with 4d", "effective_stack_bb=60") but the actual `board_flop` / `board_turn` / `board_river` fields in each row are unchanged from the anchor. Effective_stack_bb and to_call_bb fields ARE updated; only the board fields are not.

**Why this BLOCKS full batch:**
- The 50 lookalikes effectively re-label the anchor (with prose annotations) rather than producing diverse lookalikes
- 96% pilot gate PASS partly reflects anchor-stability rather than lookalike-discrimination
- Full 700 would replicate the bug at 14× scale
- Per CLAUDE.md §5 STOP > improvise: builder correctly flagged rather than fix-forward
- Per `feedback_pilot_first_for_long_jobs.md`: full holds until pilot's actual signal validates the pipeline

**Owner decision**: "Fix generator before FULL (orchestrator dispatches generator-fix sub-PR, then re-pilot, then full)" — quality default per `feedback_quality_default_no_ask.md`.

## LEAD-PROGRAMMER — fire now

You are authorized to fire the generator-fix patch + re-pilot per the binding spec below.

### Binding spec

1. **Patch `scripts/generate_hu_situations.py`** to actually mutate the board fields per `variation_param` semantics. Specifically:
   - When `variation_param` is "replaced last-street brick with <card>": update `board_river` (or whichever street is the brick) to the new card. Verify card uniqueness (no duplicate with hero/board).
   - When `variation_param` is "effective_stack_bb=N": update `effective_stack_bb` field (already working).
   - When `variation_param` is a board-texture mutation: actually mutate `board_flop` / `board_turn` / `board_river` fields, not just describe in prose.
   - Add a unit test or assertion in the generator: for each output row, assert that EITHER (a) `variation_param` describes a non-board mutation (e.g., stack/sizing) AND board fields equal anchor, OR (b) `variation_param` describes a board mutation AND at least one board field differs from anchor.
2. **Re-run pilot 50** with the fixed generator. Same anchor (HU-1 axis), same labeller protocol, same Opus tier-up.
3. **Re-validate pilot gate**: ≥80% labeller-consensus rate on the diverse-lookalike output (should be lower than 96% if diversity works correctly — anchor-stability artificially inflated the prior pilot).
4. **HU-1.5-LK-10 propagation**: in the re-pilot, the LK-10 lookalike (~112% overbet) is owner-adjudicated CALL per (a) above. Builder marks consensus_action = CALL with solver-verification-pending flag.

### Output (in PR diff — generator-fix re-pilot PR)

1. `scripts/generate_hu_situations.py` — patched generator (with board-field mutation + assertion)
2. `scripts/test_generate_hu_situations.py` (new) — unit test asserting board-mutation correctness across all output rows
3. `data/hu_corpus/pilot_50_v2/situations.jsonl` — 50 generated lookalikes (DIVERSE this time)
4. `data/hu_corpus/pilot_50_v2/raw_labels.jsonl` — 5 labellers × 50 = 250 outputs
5. `data/hu_corpus/pilot_50_v2/consensus.jsonl` — 50 hands consensus (HU-1.5-LK-10 = CALL per owner adjudication)
6. `data/hu_corpus/pilot_50_v2/calibration_results.jsonl`
7. `data/hu_corpus/pilot_50_v2/opus_tier_up.jsonl`
8. `data/hu_corpus/pilot_50_v2/similarity_distance_audit.jsonl` — re-validate similarity-band assignment with diverse lookalikes
9. `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_V2_2026-05-10.md` — execution log + bug-fix verification + gate result + new owner-arbs (if any)

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus
- **Pilot-first** per `feedback_pilot_first_for_long_jobs.md`: re-pilot is binding gate
- **No deadlines** per `feedback_no_deadlines.md`
- **STOP conditions**: if generator fix can't reproduce the variation_param semantics deterministically OR if re-pilot consensus rate < 80% → STOP and surface to orchestrator
- **HU-1.5-LK-10 propagation rule**: builder MAY observe the v2 lookalike has different actual board (per fixed generator) — in that case, re-evaluate the spot independently and the owner-CALL adjudication does NOT propagate (it only applies to the original LK-10 spot with the actual board overbet sequence). Document either way.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT execute the FULL 700-batch (separate PR after re-pilot gate clears)
- ❌ Does NOT modify any source files outside `scripts/generate_hu_situations.py` + `scripts/test_*` + `data/hu_corpus/`
- ❌ Does NOT use solver output as training label
- ❌ Does NOT relax pilot gate
- ❌ Does NOT improvise on STOP conditions

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

10-item audit:

1. Diff scope strict per dispatch
2. Generator fix verification: read patched `generate_hu_situations.py` + assert the bug condition no longer present
3. Unit test passes: `pytest scripts/test_generate_hu_situations.py` (or equivalent invocation per `docs/PROCESS_GUIDE.md`)
4. Re-pilot 50 lookalikes show actual board diversity (sample 10 spots; verify board fields differ from anchor where variation_param describes board mutation)
5. 5 labellers per spot + calibration ≥20/24 + 3 GTO-reversal correct
6. Bucket-first + solver-vs-labels separation
7. Consensus rule applied
8. Pilot gate verification: ≥80% (anchor-stability inflation should be gone; expect 80-90% range, not 96%)
9. HU-1.5-LK-10 propagation: per (a) — CALL with solver-verification-pending; OR if v2 board differs, re-evaluated independently
10. TC-X-DISPATCH-COMPLIANCE per this comm

## Owner — informational

- Standing directive: orchestrator merges this dispatch + builder fix-PR + QC verdict autonomously per quality default
- After fix-pilot + verdict merge → orchestrator authorizes Phase 1.5-D.3-FULL dispatch (700 lookalikes from HU-2..HU-6 anchors)
- Solver-verification queue tracked under (c) below

---

# (c) Solver-verification queue (recurring annotation pattern)

Per `feedback_solver_verification_queue.md` (memory rule): owner-arbitrated spots flagged "check solver later" accumulate here. Queue MUST drain before Phase 1.5-D.4 (HU model retrain) ships.

**Current queue:**

| spot_id | source PR | hero / board / action | owner adjudication | timestamp |
|---|---|---|---|---|
| HU-6.5 | PR #338 | Qd9h on 7h6c5s2d8d; BB 150% overbet (20.6bb into 13.7bb); pot odds 37.5% | CALL | 2026-05-10 |
| HU-1.5-LK-10 | PR #338 (this PR) | Qd9h on 7h6c5s2d8d (same as HU-6.5); BB ~112% overbet (56.25bb into 50bb); pot odds ~35% | CALL | 2026-05-10 |

**Drain protocol** (per memory rule):
1. Confirm solver online
2. Run each queued spot through solver verification
3. Document agree/disagree per spot
4. If solver disagrees with owner adjudication on any spot: surface to owner for re-judgment BEFORE retrain corpus is finalized
5. Document outcome in `SOLVER_VERIFICATION_QUEUE_DRAINED_<date>.md` comm

**Trigger:** Before authoring the Phase 1.5-D.4 dispatch comm, orchestrator MUST check solver-status:
- Solver still offline: HOLD 1.5-D.4 with explicit owner-gate ask
- Solver online: DRAIN queue first (per protocol above) BEFORE 1.5-D.4 dispatch

This rule persists across orchestrator sessions via memory file `feedback_solver_verification_queue.md`.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `9a7b1eb` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.3 PILOT merged: master `a2b97e2` (PR #339)
- QC verdict PASS-WITH-FINDINGS: master `2f04f34` (PR #342)
- Builder observation merged: master `9a7b1eb` (PR #341)
- HU-6.5 owner-adjudication: master `c54eab1` (PR #338)
- 1.5-D.3 dispatch + design memo §4.4: same as above
- Generator file (to fix): `scripts/generate_hu_situations.py`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md` (NEW), `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: HU-1.5-LK-10 adjudicated CALL with solver-verification flag pending. Generator-fix dispatch fires LEAD-PROGRAMMER. Solver-verification queue tracked for pre-1.5-D.4 drain. Loop CONTINUES through generator-fix re-pilot → QC → 1.5-D.3-FULL dispatch → 1.5-D.4 dispatch (post solver-queue drain).**
