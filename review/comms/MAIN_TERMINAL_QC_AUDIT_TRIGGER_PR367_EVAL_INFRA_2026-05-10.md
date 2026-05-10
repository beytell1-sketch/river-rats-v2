---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #367 — Phase 1.5-D.4 PR 0 (eval infrastructure: 30-hand HU reference JSONL + reference_evaluator + v8-HU baseline 18/30) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #367 (1.5-D.4 PR 0 EVAL INFRA)

PR #367: `builder-phase15d4-pr0-eval-infra-2026-05-10`. Head `25bf75b00cbb844b6af62069840b082e2a7ac6e4`. Title: "Builder Phase 1.5-D.4 PR 0: eval infra (30-hand HU reference + evaluator + v8-HU baseline 18/30)".

Builder built eval infrastructure per AMENDMENT (PR #366) Option B. Delivered ahead of smoke (PR 1) + 5-seed full (PR 2).

**Diff summary** (per `gh pr view 367`): 4 files / +559:
- `design/hu_reference_set/hu_30_hand_reference.jsonl` (+30) — 30 anchor rows; expected_action sourced from modal lookalike consensus + owner adjudications (PR #338, #343, #348, #362)
- `river-rats-core/hu_reference_evaluator.py` (+270) — parse + evaluate + CLI; v8-HU-38 + vNext-HU-59 compatible
- `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (+30) — per-hand v8-HU-38 results
- `review/comms/BUILDER_REPORT_PHASE15D4_PR0_EVAL_INFRA_2026-05-10.md` (+229) — full delivery report

## NOTABLE FINDING: v8-HU-38 baseline 18/30 (60%)

Architect projected ~26-28/30 (PokerBench 88.1% → 30-hand reference per design memo §4.6 reasoning). Actual = 18/30. Builder flags as significant signal:
- Failure mode: under-aggression on draws/overcards (5/12 misses; "expected BET, predicted CHECK" pattern)
- Per-axis: HU-1 3/5 · HU-2 1/5 · HU-3 1/5 · HU-4 4/5 · HU-5 4/5 · HU-6 5/5 (HU-2/HU-3 dominantly miss)

**Orchestrator decision on gates (NOT revised):**
- **Smoke gate** ("≤5pts below v8-HU" → effective floor ≥13/30): unchanged. Smoke is sanity-check ("model totally broken"). With v8-HU = 18/30, ≥13/30 catches class-collapse + critical bugs. Builder recommended keeping; orchestrator concurs.
- **Ship gate ≥28/30**: unchanged (architect-committed per `feedback_quality_default_no_ask.md`). +10/30 absolute improvement over v8-HU baseline is the load-bearing quality bar; this is what the 746-corpus + 59-surface retrain is supposed to produce.
- **Design memo §4.6 projection footnote**: needs post-1.5-D.4 amendment to acknowledge actual v8-HU baseline (18/30 vs projected 26-28/30); deferred — not blocking 1.5-D.4 sequence.

## Audit scope (~15-20 min)

Per AMENDMENT (PR #366) §"QC stream — what you audit (PR 0)":

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 4 PR files. NO production-swap edits; NO `oracle_router.py:34` change; NO model force-add; NO 1.5-D.4 dispatch edits.

2. **30 reference rows in JSONL**: `design/hu_reference_set/hu_30_hand_reference.jsonl` has exactly 30 entries. All 6 axes covered (HU-1, HU-2, HU-3, HU-4, HU-5, HU-6); per-axis count = 5 each.

3. **expected_action per row** — spot-check 5 hands:
   - Read each spot's row in JSONL: `{hero_cards, board, action_summary, expected_action}`
   - Cross-reference with design markdown (`HU_AXIS_{N}.md`) narrative
   - Assert expected_action matches the canonical answer per design markdown
   - Special verification: at least 1 owner-adjudicated spot (HU-6.5 → CALL, HU-1.5-LK-10 → CALL, HU-1.4-LK-04/05 → CALL, OR any of the 44 from PR #362)
   - Methodology assessment: "modal lookalike consensus + owner adjudications" is a derived expected_action methodology — verify this matches anchor's expected action where lookalike consensus is unanimous; flag if there's signal vs design markdown drift

4. **Parser produces consistent predictions** — sample-check 3 hands:
   - Run `python3 river-rats-core/hu_reference_evaluator.py` (or equivalent CLI invocation per docs) on the same model artifact twice
   - Assert same per-hand predictions both runs (determinism)
   - Assert model artifact format compatibility (v8-HU-38 loadable per existing artifact + vNext-HU-59 format-compatible per provenance docstring)

5. **v8-HU-38 baseline 18/30** — independent verification:
   - Load `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl`
   - Count correct/total → 18/30 expected
   - Sample-check 3 per-hand predictions vs running parser independently against v8-HU-38 artifact
   - Per-axis breakdown matches builder report (HU-1 3/5 · HU-2 1/5 · HU-3 1/5 · HU-4 4/5 · HU-5 4/5 · HU-6 5/5)
   - Builder claim "failure mode dominated by under-aggression on draws/overcards" — sample-check by inspecting 3 of the 12 missed hands

6. **Ambiguities flagged correctly**: builder report claims "0 unflagged ambiguities" — verify. Each row's expected_action should be traceable to a single source (design markdown OR owner adjudication). If QC finds any row where expected_action is ambiguous AND not surfaced in builder report → SHOULD_FIX.

7. **Expected_action distribution sanity**: 14 BET / 10 CALL / 3 CHECK / 2 FOLD / 1 RAISE = 30 ✓. Per-axis distribution shouldn't be wildly skewed; if any axis has 5 of same action, flag for design review.

8. **TC-X-DISPATCH-COMPLIANCE**: per AMENDMENT (PR #366); per-deliverable verification.

## Special audit consideration: 18/30 baseline impact assessment

Builder flagged this for orchestrator decision. Orchestrator has decided gates UNCHANGED. QC may corroborate or push back if QC finds methodology issue with baseline computation that would suggest the 18/30 number is artifact (e.g., parser bug, prediction-format mismatch, expected_action methodology mismatch). If QC finds methodology issue → SHOULD_FIX (orchestrator re-amends gate decision).

If baseline is genuine: 18/30 is a meaningful data point about v8-HU-38's actual weakness on HU close spots. QC may surface for post-1.5-D.4 design memo §4.6 amendment but NOT as blocking on this PR.

## Special audit consideration: expected_action sourcing methodology

Builder used "modal lookalike consensus + owner adjudications" for expected_action. This is a DERIVED ground-truth methodology because design markdown didn't have explicit action keys per anchor. QC assesses:
- Is this methodology defensible as a 30-hand reference? Alternatives: (a) extract from anchor design markdown explicitly; (b) modal lookalike consensus (chosen); (c) owner per-anchor adjudication (would require new owner gate).
- For the 4 owner-adjudicated <50% confidence anchors: which 4? Are these the prior owner-arb adjudications (HU-6.5 CALL, HU-1.5-LK-10 CALL, HU-1.4-LK-04/05 CALL) or new ones from the 44-spot batch (PR #362)?
- Solver verification queue (48 spots) implications: if 4 of the 30 reference anchors have expected_action sourced from orchestrator-adjudicated picks (PR #362), then those 4 are part of the verification queue. If solver later disagrees on any of these 4 → both reference set AND smoke/ship gate scoring affected. Acceptable risk per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` (retrain-if-needed is recovery).

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr367-phase15d4-pr0-eval-infra.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D4_PR0_EVAL_INFRA_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #367 merge → on QC PASS, orchestrator merges autonomously
- After merge → builder fires PR 1 (smoke) per original 1.5-D.4 dispatch (master `178fdaf`, PR #364)
- Smoke gate ≥13/30 effective (catches "model totally broken")
- After smoke + QC PASS → builder fires PR 2 (5-seed full); ship gate ≥28/30 (architect-committed)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3d5572b` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 AMENDMENT Option B: master `3d5572b` (PR #366)
- 1.5-D.4 original dispatch: master `178fdaf` (PR #364)
- Builder PR #367 head: `25bf75b`
- 44 owner-arbs data-layer fix merged: master `a3fb9f3` (PR #363)
- 44 owner-arbs adjudication dispatch: master `ca1f7b0` (PR #362)
- Architect's design memo §4.5 + §4.6: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Multiway parser reference (analog): `river-rats-core/reference_evaluator.py:parse_reference_hands`
- HU reference design source: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + `HU_AXIS_{1..6}.md`
- Production HU oracle reference: `oracle_router.py:34` → `models/gto_model_v8_hu.json`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`

**Status: QC stream — fire audit now on PR #367 PR 0 EVAL INFRA. ~15-20 min wall-clock. 8-item audit + baseline-impact assessment + expected_action methodology assessment. Orchestrator merges PR #367 + verdict autonomously on PASS. After merge → builder fires PR 1 smoke per 1.5-D.4 dispatch (smoke gate ≥13/30 effective). Ship gate ≥28/30 unchanged.**
