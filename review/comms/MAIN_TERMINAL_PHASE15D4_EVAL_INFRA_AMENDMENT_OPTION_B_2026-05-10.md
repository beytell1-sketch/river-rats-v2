---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous on quality-default)
to: LEAD-PROGRAMMER (builder; architect-hat for eval infrastructure design)
re: AMENDMENT to Phase 1.5-D.4 dispatch (PR #364) — Option B selected per `feedback_quality_default_no_ask.md`: builder builds 30-hand HU reference eval infrastructure FIRST as PR 0, then smoke (PR 1) + 5-seed (PR 2) per original dispatch
status: DISPATCH AMENDMENT — fire now (adds PR 0 prefix; original PR 1/2 sequence preserved)
---

# Phase 1.5-D.4 — Eval infrastructure AMENDMENT

Builder PR #365 observation surfaced infrastructure gap: 30-hand HU reference eval (the LOAD-BEARING signal for ship gate ≥28/30) does NOT exist on master. Building proxy eval (Option C) ships a model on weak signal; inline-extraction (Option A) risks ground-truth quality. **Option B (architect-dispatch eval infrastructure first)** is the quality-default path per `feedback_quality_default_no_ask.md`.

## Orchestrator decision

**Option B selected.** Adds a PR 0 (eval infrastructure) before the original PR 1 (smoke) + PR 2 (5-seed full) sequence. Original §"Smoke gate" + §"Ship gate" thresholds remain unchanged; only the eval infrastructure that COMPUTES those scores is being built first.

## Phase 1.5-D.4 PR 0 — Eval infrastructure (NEW; precedes smoke)

### Scope

Build the HU equivalent of multiway `reference_evaluator.parse_reference_hands` so any HU model artifact can be scored against the 30-hand HU reference set and produce `<correct>/30` aggregate accuracy.

### Sub-deliverables

1. **Structured 30-hand HU reference set:**
   - Convert `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + `HU_AXIS_{1..6}.md` markdown narrative into structured JSONL: `design/hu_reference_set/hu_30_hand_reference.jsonl`
   - Each row: `{spot_id, axis, hero_cards, board_flop, board_turn?, board_river?, street, hero_pos, villain_pos, pot_bb, to_call_bb, effective_stack_bb, facing_bet, opener, bettor?, action_summary, expected_action}`
   - `expected_action` = canonical answer for each of the 30 hands (extracted from architect's design markdown; if any are ambiguous in the markdown, builder flags + orchestrator surfaces to owner)
   - Schema parity with multiway 40-hand reference for tooling reuse where possible

2. **HU reference parser + evaluator:**
   - Extend `river-rats-core/reference_evaluator.py` with `parse_hu_reference_hands()` + `evaluate_hu_reference()` functions (or NEW HU-specific module if cleaner separation; builder-architect picks)
   - Loads `design/hu_reference_set/hu_30_hand_reference.jsonl` + a model artifact path → returns `{correct: int, total: 30, per_hand: [{spot_id, expected, predicted, correct: bool}]}`
   - Compatible with vNext-HU-59 model artifact format + (importantly) v8-HU-38 artifact format so baseline comparison works

3. **v8-HU-38 baseline computation:**
   - Run `evaluate_hu_reference()` against current production HU oracle (`models/gto_model_v8_hu.json` per `oracle_router.py:34`)
   - Output: `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (per-hand v8-HU-38 prediction + correctness)
   - Aggregate v8-HU-38 score = `{correct}/30`. This becomes the smoke-gate baseline for "smoke score must NOT be > 5 pts below v8-HU".

4. **Builder report:** `review/comms/BUILDER_REPORT_PHASE15D4_PR0_EVAL_INFRA_2026-05-10.md`
   - Markdown→JSONL extraction summary (per-axis spot count + any flagged ambiguities)
   - Parser/evaluator design summary
   - v8-HU-38 baseline score on 30-hand reference (`{correct}/30`)
   - Confirmation that infrastructure can score vNext-HU-59 once smoke artifact exists

### Verification gate (PR 0)

- 30 reference rows in JSONL (count exact)
- All 6 axes covered (HU-1..HU-6); per-axis spot count matches design memo
- Parser smoke-test on at least 1 hand (manual spot-check expected_action matches design markdown)
- v8-HU-38 baseline score computed + documented in builder report
- No unflagged ambiguities (any ambiguous hands surfaced for orchestrator/owner adjudication)

### STOP conditions for PR 0

- More than ~3 hands ambiguous in design markdown → STOP + report; orchestrator surfaces to owner before infrastructure ships
- v8-HU-38 model artifact NOT loadable / format incompatible → STOP + report; investigate (Path β reframing per design memo §4.6 amendment may need a precursor step)
- Parser produces nonsensical predictions on smoke-test hand → STOP + report

## Original Phase 1.5-D.4 PR 1 (smoke) + PR 2 (5-seed full) — UNCHANGED scope

After PR 0 ships + QC PASS:

**PR 1 (smoke; per original dispatch):** trainer + corpus_hu_746 + 1-seed model + builder report. Smoke-gate score now COMPUTABLE via `evaluate_hu_reference()` on the smoke model + comparison to v8-HU-38 baseline (delta ≤ 5 pts → PASS; delta > 5 pts → HALT).

**PR 2 (5-seed full; per original dispatch):** 5-seed model + builder report. Ship-gate score = aggregate accuracy on 30-hand HU reference ≥ 28/30 (≥ 93.3%) per design memo §4.6.

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE; PR 0 specific)

- ❌ Does NOT modify the 30-hand HU reference DESIGN (markdown is canonical; structured JSONL is derived only)
- ❌ Does NOT change ship-gate threshold (still ≥28/30 per design memo §4.6)
- ❌ Does NOT preempt original PR 1 (smoke) or PR 2 (5-seed) deliverables
- ❌ Does NOT touch `oracle_router.py:34` filename pointer (production swap still 1.5-E)

## QC stream — what you audit (PR 0)

~15-20 min audit:

1. Diff scope strict: new JSONL + extended evaluator module + baseline output + builder report; NO production-swap edits
2. 30 reference rows in JSONL; all 6 axes covered; per-axis count matches design memo
3. expected_action per row: spot-check 5 hands by reading both design markdown narrative + JSONL row; assert match
4. Parser produces consistent predictions (sample-check 3 hands; assert determinism)
5. v8-HU-38 baseline `{correct}/30` documented + reasonable (expect ~26-28/30 per architect's PokerBench 88.1% projection)
6. Ambiguities flagged correctly (if any)
7. TC-X-DISPATCH-COMPLIANCE per this comm

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

## Owner — informational

- Quality-default path per `feedback_quality_default_no_ask.md`: build proper eval infrastructure before smoke (vs proxy eval risk on ship-gate signal)
- Adds ~2-4 hr to 1.5-D.4 timeline; preserves quality of smoke + ship gate decisions
- All other 1.5-D.4 commitments unchanged: corpus 746, trainer from-scratch, 1-seed smoke + 5-seed full, ship gate ≥28/30, per-hand stay-wrong taxonomy, production swap deferred to 1.5-E
- Solver-verification queue (48 spots) HOLD-with-accepted-risk per your direction; verify-and-retrain-if-needed is recovery

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `b49f73a` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 dispatch: master `178fdaf` (PR #364)
- Builder PR 0 observation: master `b49f73a` (PR #365)
- Architect's design memo §4.5 (retrain) + §4.6 (ship-gate): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- HU reference design: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + `HU_AXIS_{1..6}.md`
- Multiway parser reference (analog): `river-rats-core/reference_evaluator.py:parse_reference_hands`
- Production HU oracle reference: `oracle_router.py:34` → `models/gto_model_v8_hu.json`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`

**Status: Phase 1.5-D.4 amended — Option B selected. Builder fires PR 0 (eval infrastructure) FIRST. PR 1 (smoke) + PR 2 (5-seed full) proceed per original dispatch after PR 0 ships + QC PASS. Ship gate ≥28/30 unchanged.**
