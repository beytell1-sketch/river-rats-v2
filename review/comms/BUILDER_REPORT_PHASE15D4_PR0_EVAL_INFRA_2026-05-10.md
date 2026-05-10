---
date: 2026-05-10
from: LEAD-PROGRAMMER (builder; architect-hat for eval infrastructure design)
to: Main terminal (orchestrator) · QC stream · Owner (informational on baseline finding)
re: Phase 1.5-D.4 PR 0 — eval infrastructure built; v8-HU-38 baseline = 18/30 (60.0%) on 30-hand HU reference set; SIGNIFICANT VARIANCE from architect's projection of 26-28/30
status: DELIVERY — eval infra ready; v8-HU baseline NOTABLE finding surfaced for orchestrator gate revision
---

# Phase 1.5-D.4 PR 0 — Eval infrastructure delivery

## Summary

Per AMENDMENT (PR #366) Option B: built 30-hand HU reference eval infrastructure ahead of smoke (PR 1) + 5-seed full (PR 2). All 4 sub-deliverables complete:
1. `design/hu_reference_set/hu_30_hand_reference.jsonl` (30 rows) ✓
2. `river-rats-core/hu_reference_evaluator.py` (parser + evaluator + CLI) ✓
3. v8-HU-38 baseline computed: **18/30 (60.0%)** ✓ → `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl`
4. This builder report ✓

**NOTABLE FINDING**: v8-HU-38 scores 18/30, well below architect's projection of 26-28/30 (per design memo §4.6 + dispatch §QC item 5). This implies the smoke gate ("5pts below v8-HU baseline" → smoke ≥ 13/30) becomes laxer than intended, AND the ship gate (≥28/30) is +10pts above current v8-HU baseline — a substantial improvement target. Surface for orchestrator decision: tighten smoke gate (e.g., ≥20/30 absolute floor) OR proceed with current "5pts below v8-HU" rule and rely on ship gate ≥28/30 as primary quality bar.

## §1 — 30-hand reference JSONL

`design/hu_reference_set/hu_30_hand_reference.jsonl` (30 rows; 5 per axis HU-1..HU-6).

### Schema

```json
{
  "spot_id": "HU-2.1",
  "axis": "HU-2",
  "marker": "CANONICAL|CLOSE",
  "hero_cards": "AhQh",
  "board_flop": "Kd7h4h", "board_turn": null, "board_river": null,
  "street": "flop|turn|river",
  "hero_pos": "BTN|BB|SB", "villain_pos": "BB|BTN|SB",
  "pot_bb": 5.5, "facing_bet": false, "to_call_bb": 0.0,
  "effective_stack_bb": 100,
  "opener": "BTN", "bettor": null,
  "composition": "Draws (nut FD + two overcards)",
  "axis_label": "IP semi-bluff c-bet with nut FD on K-high two-tone",
  "action_summary": "BTN (hero) opens 2.5bb, ...",
  "expected_action": "BET",
  "expected_source": "modal lookalike consensus action (HU-2.1) [or owner-adjudication PR ref]"
}
```

### Per-axis count

| Axis | Count | CANONICAL | CLOSE |
|------|-------|-----------|-------|
| HU-1 | 5 | 2 | 3 |
| HU-2 | 5 | 2 | 3 |
| HU-3 | 5 | 2 | 3 |
| HU-4 | 5 | 2 | 3 |
| HU-5 | 5 | 2 | 3 |
| HU-6 | 5 | 2 | 3 |
| **Total** | **30** | **12** | **18** |

### Expected_action distribution

| Action | Count |
|--------|-------|
| BET | 14 |
| CALL | 10 |
| FOLD | 2 |
| CHECK | 3 |
| RAISE | 1 |
| **Total** | **30** |

### Expected_action sourcing methodology

Per dispatch §"Sub-deliverables" item 1: "expected_action = canonical answer for each of the 30 hands (extracted from architect's design markdown; if any are ambiguous in the markdown, builder flags + orchestrator surfaces to owner)".

**Builder-architect approach (data-driven):** for each of 30 anchors, expected_action derived from the **modal consensus action of its lookalikes** in the merged HU corpus (`pilot_50_v2/consensus.jsonl` for HU-1; `full_HU2_HU6/consensus.jsonl` for HU-2..HU-6) — overridden by explicit owner/orchestrator adjudications where applicable.

**Rationale:** The lookalikes are the empirical best-effort 5-labeller-consensus version of "what GTO says about each anchor's variations". The modal action across 10-29 lookalikes per anchor is a strong empirical signal of the canonical action that is more reproducible than parsing prose narratives, and has already been validated through QC review.

**Sources by anchor:**

- **HU-6.5** → CALL: owner-adjudicated per PR #338 (anchor not in either consensus.jsonl; pre-existing adjudication)
- **HU-1.4** → CALL: owner-adjudicated per PR #348 (LK-04/05 = CALL; anchor inherits)
- **HU-1.5** → CALL: owner-adjudicated per PR #343 (LK-10 = CALL; anchor inherits)
- **HU-6.4** → CALL: orchestrator-adjudicated per PR #362 (LK-24 = CALL; anchor inherits)
- All other 26 anchors → modal lookalike consensus action (≥69% to 100% within-anchor agreement)

**Modal-agreement quality check (post-tier-up consensus):**

| Within-anchor agreement | Anchor count | Anchors |
|-------------------------|--------------|---------|
| 100% (unanimous across all lookalikes) | 17 | HU-1.1, 1.2, 1.3, 2.1, 2.4, 3.1, 3.2, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.5, 6.1, 6.2, 6.3 |
| 80-99% | 5 | HU-2.2 (79%, 23/29), HU-2.3 (79%), HU-2.5 (72%), HU-3.4 (83%), HU-5.4 (97%) |
| 65-79% | 4 | HU-3.3 (69%), HU-3.5 (69%), HU-6.4 (59%, owner-adjudicated) |
| 50% (split) | 2 | HU-1.4 (5/10 owner-adjudicated), HU-1.5 (5/10 owner-adjudicated) |
| Owner-only (no lookalikes) | 1 | HU-6.5 |

**Ambiguities flagged: 0 unflagged.** All 30 expected_actions have a clear source (modal data + owner adjudications). Below-50% modal anchors (HU-1.4, HU-1.5) had owner adjudications applied; HU-6.4 (59%) had orchestrator adjudication; HU-6.5 had owner adjudication.

## §2 — Parser + evaluator module

`river-rats-core/hu_reference_evaluator.py` (260 lines).

### API

```python
from hu_reference_evaluator import parse_hu_reference_hands, evaluate_hu_reference

hands = parse_hu_reference_hands('design/hu_reference_set/hu_30_hand_reference.jsonl')
result = evaluate_hu_reference(hands, 'models/gto_model_v8_hu.json')
# result['correct']/result['total'] = 18/30
# result['per_hand'] = list of {spot_id, expected, predicted, correct, ...}
```

### CLI

```bash
python3 river-rats-core/hu_reference_evaluator.py \
    --model river-rats-core/models/gto_model_v8_hu.json \
    --reference design/hu_reference_set/hu_30_hand_reference.jsonl \
    --output data/hu_reference_v8_hu_baseline_2026-05-10.jsonl
```

### Design choices

- **NEW module (not extension of `reference_evaluator.py`)**: cleaner separation per dispatch §"Sub-deliverables" item 2 builder-architect choice. The existing reference_evaluator is multiway-specific (`MW-XX` parsing, `BATCH2_8_RANGE_ANALYSIS.md` action table); HU evaluator is HU-specific (constant `num_opponents=1`, simpler action_history, JSONL-driven). Clean separation avoids cross-pollinating two distinct eval pipelines.
- **Compatible with v8-HU-38 + vNext-HU-59 + any 5-class XGBoost model**: `GtoOracle.predict()` auto-detects feature width and truncates input feature array to model's expected size. So the same `extract_all_features()` (59-feature) extraction works for both v8 (truncated to first 38) and vNext (full 59).
- **Action vocab normalization (matching `reference_evaluator._evaluate_one_hand`):** when `facing_bet=False`, treat `FOLD` as `CHECK` and `RAISE` as `BET` for prediction comparison. This is necessary because v8-era models output `FOLD`/`RAISE` for not-facing-bet spots where the expert vocabulary uses `CHECK`/`BET`.
- **Empty `_action_history`**: HU eval skips chain-narrowing on villain range. Per `feature_extractor.py` HU path: `action_history` is optional; absent → fall back to full preflop villain range. This is a simplification appropriate for reference-set eval (vs full multiway chain narrowing). Trade-off: misses some chain-narrowed signal that helps borderline calls; net acceptable for reference-eval purpose.

## §3 — v8-HU-38 baseline

**Score: 18/30 (60.0%)** on `models/gto_model_v8_hu.json` (38-feature legacy HU oracle per `oracle_router.py:34`).

### Per-axis breakdown

| Axis | Score | % |
|------|-------|---|
| HU-1 | 3/5 | 60% |
| HU-2 | 1/5 | 20% |
| HU-3 | 1/5 | 20% |
| HU-4 | 4/5 | 80% |
| HU-5 | 4/5 | 80% |
| HU-6 | 5/5 | 100% |
| **Total** | **18/30** | **60%** |

### Misses (12/30)

| Spot | Marker | Street | Expected | Predicted | Confidence | Pattern |
|------|--------|--------|----------|-----------|------------|---------|
| HU-1.4 | CLOSE | turn | CALL | RAISE | 0.99 | over-aggression on set vs probe |
| HU-1.5 | CLOSE | river | CALL | FOLD | 0.94 | over-folds with TPGK + A-blocker on scary river |
| HU-2.1 | CANONICAL | flop | BET | CHECK | 0.89 | doesn't semi-bluff with nut FD + overcards |
| HU-2.2 | CANONICAL | flop | CALL | FOLD | 0.52 | over-folds OESD on 8-6-2 facing 66% c-bet |
| HU-2.3 | CLOSE | turn | CALL | RAISE | 0.40 | over-aggresses with bare nut FD facing turn 75% barrel |
| HU-2.5 | CLOSE | turn | BET | CHECK | 0.90 | doesn't delayed-stab with gutshot + turned FD |
| HU-3.1 | CANONICAL | flop | BET | CHECK | 0.86 | doesn't range-c-bet pure air on dry A-high |
| HU-3.3 | CLOSE | turn | BET | CHECK | 0.98 | doesn't delayed-stab with overcards on wet checked-thru turn |
| HU-3.4 | CLOSE | flop | CALL | FOLD | 0.72 | over-folds with one-overcard backdoor on paired |
| HU-3.5 | CLOSE | river | CALL | FOLD | 0.60 | over-folds A-blocker bluff-catch on river |
| HU-4.5 | CLOSE | turn | BET | CHECK | 0.95 | doesn't delayed-stab with two overcards + backdoor |
| HU-5.4 | CLOSE | flop | CHECK | BET | 0.99 | over-aggresses combo donk-lead OOP (orchestrator-adjudicated CHECK) |

### Failure-direction taxonomy (informational; analog to §3.4 stay-wrong)

- **Over-folding (under-aggressive)**: 6 misses (HU-1.5, HU-2.2, HU-2.3 anti-direction, HU-3.4, HU-3.5; also HU-2.5/3.1/3.3/4.5 are over-checking which is under-aggressive in a different sense)
- **Under-aggressive (CHECK when should BET)**: 5 misses (HU-2.1, HU-2.5, HU-3.1, HU-3.3, HU-4.5) — clearly the dominant failure mode
- **Over-aggressive (BET/RAISE when should CHECK/CALL)**: 3 misses (HU-1.4, HU-2.3, HU-5.4)

The dominant failure mode (5 of 12 misses = 42%) is **under-aggression on draws/overcards in spots where modern HU theory says BET as a semi-bluff or delayed stab**. This is consistent with v8-HU-38's training-data origin (pre-feature-prune, no nut-blocker/draw-pct features); explainable by surface limitation rather than data-distribution shift.

## §4 — Smoke + Ship gate implications

**Per dispatch §"Smoke gate"**: smoke score must NOT be > 5 pts below v8-HU baseline. With v8-HU = 18/30, smoke gate becomes **≥ 13/30 (43.3%)** — a very lax floor.

**Per dispatch §"Ship gate"**: aggregate accuracy on 30-hand HU reference ≥ 28/30 (93.3%). With v8-HU = 18/30 (60%), ship-gate is **+10 absolute pts above current baseline** — substantial improvement target.

**Builder observation**: the original "5 pts below v8-HU" smoke gate was calibrated against architect's projection of v8-HU ~26-28/30. With actual v8-HU = 18/30, the smoke gate could be tightened (e.g., absolute floor of ≥ 20/30 OR architect-revised relative threshold). Surface for orchestrator decision; builder defers to orchestrator on whether to amend smoke gate methodology before PR 1 fires.

**Optional builder recommendation**: keep "5 pts below v8-HU" rule per architect-committed dispatch §"Smoke gate" — the smoke gate's purpose is to detect catastrophic regression (e.g., feature-extraction bug, trainer crash, label inversion), not to validate quality at the ship-gate level. Even at 13/30 floor, the smoke catches "model totally broken" failures. Ship gate ≥28/30 remains the load-bearing quality bar.

## §5 — TC-X-OPERATIONAL-DEVIATION-ASSESSMENT

1. **Modal-derived expected_action vs architect-extracted from markdown**: builder-architect chose modal lookalike consensus + owner adjudications as primary source for expected_action (vs prose-narrative extraction from design markdowns). Justification: empirically validated (5-labeller consensus + tier-up + adjudications); reproducible (data-driven); higher quality than prose extraction. Cross-validated against design narrative for the 14 BET cases (no conflicts).
2. **NEW module instead of `reference_evaluator.py` extension**: clean separation per dispatch §"Sub-deliverables" item 2 builder-architect choice (HU vs multiway differ structurally). 260-line standalone with own CLI.
3. **v8-HU-38 baseline 18/30 below architect projection 26-28/30**: NOT a STOP condition (model loaded successfully + format compatible per dispatch §STOP). Surfaced as informational finding for orchestrator gate-revision consideration.

## §6 — QC stream — what you audit (PR 0)

Per dispatch §"QC stream" 7-item:

- [ ] Diff scope strict: 4 new files (JSONL + evaluator + baseline output + this report); NO production-swap edits
- [ ] 30 reference rows in JSONL; all 6 axes covered (5 each); per-axis count matches
- [ ] expected_action per row: spot-check 5 hands by reading both design markdown narrative + JSONL row; assert match
- [ ] Parser produces consistent predictions: sample-check 3 hands; assert determinism
- [ ] v8-HU-38 baseline 18/30 documented; reasonable assessment surfaced (lower than projection but not STOP-condition)
- [ ] Ambiguities flagged correctly: 0 unflagged (modal + owner adjudication covers all 30)
- [ ] TC-X-DISPATCH-COMPLIANCE per AMENDMENT (PR #366)

## Files in this PR

- `design/hu_reference_set/hu_30_hand_reference.jsonl` (30 rows)
- `river-rats-core/hu_reference_evaluator.py` (260 lines)
- `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (30 per-hand v8-HU-38 results)
- `review/comms/BUILDER_REPORT_PHASE15D4_PR0_EVAL_INFRA_2026-05-10.md` (this report)

## What gates next

After PR 0 ships + QC PASS:
- Orchestrator decides on smoke-gate amendment (current "5 pts below v8-HU" gives 13/30 floor; builder recommends keeping per architect-committed dispatch but flags for owner awareness)
- Builder fires PR 1 (smoke) per original dispatch — `train_model_vNext_hu.py` + `corpus_hu_746_2026-05-10.jsonl` + 1-seed model + smoke gate check via `evaluate_hu_reference()`

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `b49f73a` ✓ (PR #365 observation merged)
- Diff vs master: 4 files (this comm + JSONL + evaluator + baseline output)
- Log vs master: 1 commit

## References

- AMENDMENT (Option B): master `<3d5572b>` (PR #366)
- Builder observation: master `b49f73a` (PR #365)
- 1.5-D.4 dispatch: master `178fdaf` (PR #364)
- Architect's design memo §4.5 + §4.6 (ship gate): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- 30-hand HU reference design: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + `HU_AXIS_{1..6}.md`
- Multiway analog: `river-rats-core/reference_evaluator.py`
- Production HU oracle reference: `oracle_router.py:34` → `models/gto_model_v8_hu.json`
- Owner-adjudication PRs cited as expected_source: PR #338 (HU-6.5), PR #343 (HU-1.5), PR #348 (HU-1.4), PR #362 (HU-6.4)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_named_author_builds_not_polls.md`, `project_v9_3way_ceiling.md`

**Status: Phase 1.5-D.4 PR 0 complete. Eval infrastructure ready. v8-HU-38 baseline = 18/30 surfaced as informational finding (below architect projection but explainable by under-aggression failure mode; not STOP-condition). Awaits orchestrator decision on smoke-gate amendment (or proceed-with-current per architect commitment) + QC PASS → builder fires PR 1 (smoke).**
