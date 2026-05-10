---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #373 — Phase 1.5-D.4 PR 2 (5-seed full; SHIP GATE PASS — mean 28.2/30, canonical 28/30; ALL 5 seeds ≥28/30; +10 absolute over v8-HU 18/30) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #373 (1.5-D.4 PR 2 5-SEED FULL)

PR #373: `builder-phase15d4-pr2-5seed-full-2026-05-10`. Head `4a1600ca907652cf90b48fe73eb40eb729541a85`. Title: "Builder Phase 1.5-D.4 PR 2 (5-seed full): SHIP GATE PASS — mean 28.2/30, canonical 28/30".

Builder fired 5-seed full per 1.5-D.4 dispatch (PR #364) §"Builder deliverables PR 2" + smoke PASS gate (PR #370 + QC PR #372 PASS).

## SHIP GATE: PASS

- **Canonical (median seed=3):** 28/30 (93.3%) — exactly at architect-committed gate
- **5-seed mean:** 28.2/30 (94.0%)
- **ALL 5 seeds ≥28/30** (no seed below ship gate)
- **vs v8-HU baseline:** 18/30 (60%) → 28/30 (+10 absolute pts)

## 5-seed reference-eval results

| Seed | Held-out | Ref-eval (30) |
|------|----------|---------------|
| 0 | 0.933 | 28/30 (93.3%) |
| 1 | 0.960 | **29/30 (96.7%) ← best** |
| 2 | 0.967 | 28/30 (93.3%) |
| 3 | 0.960 | **28/30 (93.3%) ← MEDIAN canonical** |
| 4 | 0.967 | 28/30 (93.3%) |
| **Mean** | **0.957** | **28.2/30 (94.0%)** |

## Per-axis (canonical seed=3) vs v8-HU

| Axis | Canonical | v8-HU | Delta |
|------|-----------|-------|-------|
| HU-1 | 4/5 | 3/5 | +1 |
| HU-2 | 5/5 | 1/5 | **+4** |
| HU-3 | 5/5 | 1/5 | **+4** |
| HU-4 | 5/5 | 4/5 | +1 |
| HU-5 | 5/5 | 4/5 | +1 |
| HU-6 | 4/5 | 5/5 | -1 |
| **Total** | **28/30** | **18/30** | **+10** |

## Stay-wrong taxonomy (per design memo §3.4 + `project_v9_3way_ceiling.md` analog)

- **HU-1.4 (CALL→RAISE):** stuck 5/5 seeds = **model-stuck pipeline-aligned**. Lookalike consensus split CALL:5/RAISE:5; class-weight-cap pressure → RAISE; in solver-verification queue (HU-1.4-LK-04 + HU-1.4-LK-05 from PR #348).
- **HU-6.5 (CALL→FOLD):** stuck 4/5 seeds = **pipeline-canonical mismatch**. No training lookalikes (HU-6.5 anchor + lookalikes excluded by design); model defaults to fold; in solver-verification queue (HU-6.5 from PR #338).
- **HU-3.3 (BET→CHECK; smoke-seed-42 only):** 5-seed CLEAR — pure variance.
- **No class-collapse pattern.**

Both stuck-wrong hands already in solver-verification queue; verify-and-retrain-if-needed is recovery per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`.

**Diff summary** (per `gh pr view 373`): 6 files / +317:
- 5 per-seed reference eval JSONL: `data/hu_reference_5seed_seed{0..4}_2026-05-10.jsonl` (+30 each)
- `review/comms/BUILDER_REPORT_PHASE15D4_FULL_2026-05-10.md` (+167) — full delivery report

Model artifacts gitignored per dispatch §"Does NOT git-add the new model file in 1.5-D.4 PR; force-add happens in 1.5-E".

## Audit scope (~20-25 min)

Per 1.5-D.4 dispatch (PR #364) §"QC stream — what you audit (For PR 2 5-seed full)":

1. **5-seed model artifacts present + per-seed scores documented:** verify all 5 per-seed JSONL files (seed{0..4}); each has 30 per-hand entries; per-seed scores match builder claim (28, 29, 28, 28, 28). Model artifacts (gitignored) verified present locally per builder report.

2. **5-seed mean on 30-hand HU reference 28.2/30:** independent computation (sum 28+29+28+28+28 = 141 / 5 = 28.2 ✓). Verify mean rounding to 28.2 not 28.0/28.4.

3. **Per-hand stay-wrong taxonomy applied (§3.4 format):**
   - **HU-1.4** classification = "model-stuck pipeline-aligned": verify all 5 seeds predict RAISE on HU-1.4 reference hand; verify lookalike consensus split (CALL:5/RAISE:5 in pilot_50_v2/consensus.jsonl HU-1.4 anchors)
   - **HU-6.5** classification = "pipeline-canonical mismatch": verify 4/5 seeds predict FOLD; verify no HU-6.5 lookalikes in corpus_hu_746_2026-05-10.jsonl
   - **HU-3.3** classification = "pure variance": verify smoke-seed-42 missed but 5-seed all correct on HU-3.3
   - **No class-collapse:** sample-check that each seed's predictions span all 5 classes (not stuck on majority class)

4. **Ship-gate result correctly applied:** PASS (28/30 canonical; mean 28.2/30; ALL 5 ≥28/30). Verify dispatch §"5-seed full produces 26 or 27 of 30: STOP/REPORT" did NOT fire.

5. **PokerBench 88.1% parity reported as SECONDARY:** check builder report mentions PokerBench parity; not gate-blocking. Likely deferred per dispatch §"Fallback verification: PokerBench 88.1% parity reported as SECONDARY metric for provenance; not a gate."

6. **Diff scope strict:** 6 PR files (5 per-seed eval JSONLs + builder report). NO `oracle_router.py:34` edit; NO model file force-added; NO production swap; NO trainer/corpus/eval-infra modifications (those merged in PR 0/1).

7. **TC-X-DISPATCH-COMPLIANCE per dispatch + AMENDMENT:** dispatch §"Negative scope" all honored; AMENDMENT §"Phase 1.5-D.4 PR 0/1/2 sequence preserved" verified.

8. **TC-X-OPERATIONAL-DEVIATION-ASSESSMENT:** any deviations from dispatch spec documented + acceptable.

## Special audit consideration: ship gate at exactly 28/30 (no margin)

Architect committed ≥28/30 specifically because "30 - 2 = 28 lets one CLOSE hand miss per typical axis without tripping the gate, while 27/30 (-3) would allow a class-collapse pattern to slip through" (design memo §4.6). Canonical at exactly 28/30 = 2 misses (HU-1.4 + HU-6.5) = 1 per typical axis — within the architect's tolerance.

Both misses are CLOSE-marker hands documented as "expected difficulty" + already in solver-verification queue. No class-collapse pattern. Per architect commitment, this PASSES the ship gate.

QC may flag for orchestrator awareness: 28/30 is at-gate (not above), so any future regression (e.g., new evaluation reveals additional miss) would trip the gate. Surface for monitoring, not blocking.

## Special audit consideration: HU-6.5 corpus-exclusion gap

HU-6.5 was excluded from full_HU2_HU6 corpus by design (PR #338 owner adjudication preserved as anchor, not relabelled as lookalike). Result: model never saw HU-6.5 spots in training; predictable miss on HU-6.5 reference hand. Surface for post-1.5-D.4 design memo amendment consideration:
- Option A: include HU-6.5 lookalikes in retrain corpus to close gap (would require new labelling round)
- Option B: accept HU-6.5 as known-miss documented in stay-wrong taxonomy; ship as-is
- Out-of-scope for this audit; surfaces for orchestrator/architect post-1.5-D.4 review.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-25 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr373-phase15d4-pr2-5seed-full.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D4_PR2_5SEED_FULL_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #373 merge → on QC PASS, orchestrator merges autonomously
- After merge → orchestrator authorizes Phase 1.5-E (router/coaching alignment + production swap) per dispatch §"After PASS: orchestrator authorizes 1.5-E"
- 1.5-E action per design memo §4.6: `git add -f` new HU model file + change `oracle_router.py:34` filename pointer + run coaching-pipeline tests + commit + open 1.5-E PR
- After 1.5-E + ship → Phase 1.5 SHIP boundary

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `77bbefb` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.4 PR 1 SMOKE merged: master `77bbefb` (PR #370 + QC PR #372 PASS · 0/0/0; 27/30 PASS)
- 1.5-D.4 PR 0 EVAL INFRA merged: master `3fcf7f1` (PR #367 + QC PR #369 PASS · 0/0/0; 18/30 v8-HU baseline)
- 1.5-D.4 AMENDMENT Option B: master `3d5572b` (PR #366)
- 1.5-D.4 original dispatch: master `178fdaf` (PR #364)
- Builder PR #373 head: `4a1600c`
- Architect's design memo §4.5 (retrain) + §4.6 (ship-gate ≥28/30; production swap deferred to 1.5-E): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Stay-wrong taxonomy reference: `project_v9_3way_ceiling.md` + design memo §3.4
- HU reference set: `design/hu_reference_set/hu_30_hand_reference.jsonl`
- v8-HU-38 baseline: `data/hu_reference_v8_hu_baseline_2026-05-10.jsonl` (18/30)
- Solver-verification queue: 48 spots; HU-1.4 (4 spots: LK-04, LK-05) + HU-6.5 (1 anchor) both in queue
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_pilot_first_for_long_jobs.md`, `project_v9_3way_ceiling.md`

**Status: QC stream — fire audit now on PR #373 PR 2 5-SEED FULL. ~20-25 min wall-clock. 8-item audit + at-gate margin assessment + HU-6.5 corpus-exclusion-gap assessment. Orchestrator merges PR #373 + verdict autonomously on PASS. After merge → orchestrator authorizes Phase 1.5-E (router/coaching + production swap; force-add new model file + oracle_router.py:34 filename pointer change).**
