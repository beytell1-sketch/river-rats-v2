---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #359 — Phase 1.5-D.3 FULL LABELLING SCALE (696 lookalikes labelled by FL6+FL7-10 with explicit-anti-rule prompt; 652/696 = 93.7% consensus; 44 owner-arbs surfaced; 0 rule-based or template labellers in valid pool) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #359 (FULL LABELLING SCALE)

PR #359: `builder-phase15d3-full-labelling-2026-05-10`. Head `48b695b0ab24458155721505feed1a148fb3c0d2`. Title: "Builder Phase 1.5-D.3 FULL labelling: 696 lookalikes, 652 consensus + 44 owner-arbs".

Builder fired Phase 1.5-D.3 FULL labelling per AMENDMENT (`MAIN_TERMINAL_PHASE15D3_RECOVERY_AMENDMENT_EXPLICIT_PROMPT_2026-05-10.md`, master `bdd1960`, PR #357) + re-poke (master `dd3b0f4`, PR #358). Successfully recovered from SYSTEMIC STOP (PR #354) via Phase 1 Option A explicit-anti-rule prompt + 4 FL6-style replacements (FL7, FL8, FL9, FL10).

**Recovery success signal:** 0 rule-based or template-based labellers in valid pool. FL6 + FL7-10 all produced varied per-spot LLM reasoning per FL6 evidence pattern. Quarantined evidence (FL1-FL5) preserved in `_invalidated_*/` subdirs.

**Diff summary** (per `gh pr view 359`): 27 files / +13662:
- `data/hu_corpus/full_HU2_HU6/raw_labels.jsonl` (3480) + 5 per-labeller files (FL6/7/8/9/10 × 696 each)
- `data/hu_corpus/full_HU2_HU6/calibration_results.jsonl` + 5 per-labeller files
- `data/hu_corpus/full_HU2_HU6/opus_tier_up.jsonl` (255 = 1 metadata + 254 labels)
- `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696)
- `data/hu_corpus/full_HU2_HU6/_invalidated_fl{1,2,3,4,5}_*/` (quarantined evidence preserved)
- `review/comms/BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md` (199 lines)

**Title claim**:
- 5 fresh Sonnet labellers (FL6 + FL7-10) all PASS calibration (≥25/28 + 5/5 reversal)
- Per-axis ≥80% gate met on all axes: HU-2 93.1%, HU-3 93.8%, HU-4 100.0%, HU-5 83.4%, HU-6 99.1%
- 696 spots / 652 consensus / 44 owner-arbs (3-2 with Opus disagree OR 2-2-1+)
- 0 rule-based or template labellers in valid pool

**Owner-arb concentration (per builder report):**
- HU-5.4 combo-draw donk-or-check: **22 spots** (Sonnet 3 CHECK / 2 BET; Opus BET on 21 of 22)
- HU-2.4 raise-vs-call mixing: 7 spots
- HU-3.3 delayed-stab vs check: 7 spots
- Other (HU-2.5, HU-5.1, HU-2.3, HU-3.4, HU-3.5, HU-6.4): 8 spots

**Notable signal (informational):** Opus disagrees with Sonnet 4-of-5 majority on 33/112 (29.5%) 4-of-5 spots. Per §4.3 these remain consensus. Concentrated in HU-3 axis (24/33). Surfaced for QC consideration of stricter rule for future training rounds.

Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.3 FULL labelling produces corpus directly feeding 1.5-D.4 retrain — milestone-class).

## Audit scope (~25-30 min; standard FULL post-PR + recovery validation)

Per AMENDMENT dispatch §"QC stream — what you audit" 10-item:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 27 PR files. raw_labels + consensus + opus_tier_up + per-labeller calibration + builder report + 5 quarantined evidence dirs. NO source/INFRA-PREP-file edits beyond what was in PR #350.

2. **Per-labeller validation: 5 labellers (FL6 + FL7-10) all show varied per-spot LLM reasoning**:
   - Sample 5 spots × 3+ distinct boards each labeller; verify (a) varied reasoning citing specific bricks, (b) no identical-text-across-spots, (c) no Python script outputs in raw_labels.
   - Builder note: "FL8 marginal-template note in builder report" — assess severity; if FL8 borderline, decide whether to invalidate or accept.
   - Calibration: all 5 PASS ≥25/28 + 5/5 reversal (claim).

3. **3480 raw_labels entries**: per-labeller counts 696 each; per-spot counts 5 each; no duplicates / no missing tuples.

4. **Calibration compliance**: per-labeller files (calibration_results_labeller_{6,7,8,9,10}.jsonl) all show ≥20/28 + 5/5 reversal correct; failed labellers NOT in raw_labels.

5. **Bucket-first compliance + solver-vs-labels separation** in raw_labels reasoning (sample-check 10 spots).

6. **Opus tier-up applied per §4.3 rule**: opus_tier_up.jsonl 255 entries (1 metadata + 254 labels). Verify:
   - Non-unanimous Sonnet hands (3-2 splits + 4-of-5 splits where Opus tier-up applies) sampled
   - 3-2 with Opus agree → consensus = majority
   - 3-2 with Opus disagree → owner-arb (consensus_action = null)

7. **Consensus rule applied**: builder claim "442 unanimous + 112 4-of-5 + 98 tier-up-agree = 652 consensus; 39 + 5 = 44 owner-arbs" — verify arithmetic + per-spot application across 696 hands.

8. **Per-axis confidence ≥80% all axes**: HU-2 93.1%, HU-3 93.8%, HU-4 100.0%, HU-5 83.4%, HU-6 99.1%. Verify per-axis split + arithmetic. HU-5 is lowest (83.4%) — assess whether marginal pass risks corpus quality or is acceptable per dispatch gate.

9. **Pilot V2 owner-adjudication propagation**: 0 propagations (HU-6.5 excluded; no HU-2..HU-6 anchor pre-adjudicated). Verify exclusion is honored.

10. **TC-X-DISPATCH-COMPLIANCE per AMENDMENT**: 4 deviation-assessment entries per builder report. Verify each is documented + acceptable per amendment scope.

## Special audit consideration: Opus 4-of-5 disagreement signal

Builder surfaces: "Opus disagrees with Sonnet 4-of-5 majority on 33/112 (29.5%) 4-of-5 spots ... concentrated in HU-3 axis (24/33)."

Per current §4.3 rule, 4-of-5 → consensus regardless of Opus position. But 29.5% Opus-Sonnet disagreement on 4-of-5 is a non-trivial signal: either (a) Opus has a different prior than Sonnet pool, OR (b) HU-3 axis spots are systematically harder than HU-2/4/5/6 axis spots.

QC assessment: is the 24/33 HU-3 concentration a labelling-axis-specific issue (e.g., HU-3 axis composition makes Opus diverge) OR a generator-axis-specific issue (e.g., HU-3 lookalike spots are genuinely harder)? Surface for orchestrator + Phase 1.5-D.4 design consideration; not blocking on this PR.

## Special audit consideration: 44 owner-arbs surface

Heavy concentration on HU-5.4 (22 spots = 50% of all owner-arbs). Verify:
- HU-5.4 spec is correctly designed (or whether the variation_axis was too aggressive on a difficult anchor)
- Sonnet 3-CHECK / 2-BET pattern + Opus BET on 21 of 22 is consistent across the 22 spots (or shows variance)
- Whether a single owner adjudication on HU-5.4 anchor can propagate to all 22 lookalikes (per §(b) item 4 propagation rule)

If propagatable: owner-arb count effectively reduces to ~22 unique decisions. If not: each requires individual adjudication.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~25-30 min wall-clock (larger due to 3480 raw_labels + 44 owner-arb surface assessment + Opus-disagreement-signal assessment). QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr359-phase15d3-full-scale.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D3_FULL_SCALE_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #359 merge → on QC PASS, orchestrator surfaces 44 owner-arbs to owner BEFORE merging FULL + verdict per AMENDMENT §"What gates" + recovery dispatch §"Phase 3 SCALE"
- 44 owner-arbs → orchestrator groups by anchor + character + presents to owner (HU-5.4 22 spots likely as 1 grouped decision; HU-2.4/3.3 7-spot batches likely as grouped decisions; other 8 individual or grouped)
- After QC PASS + owner adjudications + propagation → orchestrator merges PR #359 + verdict + owner-adjudication comm autonomously
- After FULL LABELLING merge → solver-verification queue drain BEFORE 1.5-D.4 dispatch (queue: HU-6.5 + HU-1.5-LK-10 + HU-1.4-LK-04 + HU-1.4-LK-05 + any new spots flagged from 44 owner-arbs)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `dd3b0f4` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- AMENDMENT dispatch: master `bdd1960` (PR #357)
- Re-poke: master `dd3b0f4` (PR #358)
- Phase 0 outcome (FL6 evidence): master `c591570` (PR #356)
- SYSTEMIC STOP observation: master `4c4c946` (PR #354)
- 1.5-D.3 FULL INFRA-PREP merged: master `6274fce` (PR #350 + QC PR #352 PASS)
- 1.5-D.3 FULL dispatch: master `bfebd13` (PR #348)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict PASS · 0/0/0: master `b790524` (PR #346)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- Builder PR #359 head: `48b695b`
- Architect's design memo §4.3 + §4.4: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #359 FULL LABELLING SCALE. ~25-30 min wall-clock. 10-item audit + Opus-disagreement-signal assessment + 44 owner-arb surface assessment. Heartbeat sync to current master at end of tick. Orchestrator surfaces 44 owner-arbs to owner BEFORE merging FULL + verdict (likely grouped decisions per anchor/character to keep owner-ask manageable). After PASS + owner adjudications + solver-queue drain → 1.5-D.4 dispatch.**
