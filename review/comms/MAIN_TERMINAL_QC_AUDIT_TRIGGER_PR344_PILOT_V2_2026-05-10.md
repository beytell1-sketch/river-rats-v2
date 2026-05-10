---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #344 — Phase 1.5-D.3 PILOT V2 (generator-fix re-pilot, 50 HU lookalikes from HU-1 axis × 5 labellers + Opus tier-up; gate PASS 96% honest; 3 owner-arbs surfaced) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #344 (PILOT V2)

PR #344: `programmer/phase15d3-pilot-v2-generator-fix-2026-05-10`. Head `29de5daae720a46b7203eda1cbfa635b1904972a`. Title: "Builder Phase 1.5-D.3 PILOT V2: generator-fix re-pilot 50 HU lookalikes (board-mutation bug fix; gate PASS 96% honest; 2 new owner-arbs HU-1.4-LK-04/05)".

Builder fired re-pilot per generator-fix dispatch `MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md` (master `60bb850`, PR #343). Fixes QC PR #342 SHOULD_FIX-1 (board-mutation bug in `scripts/generate_hu_situations.py`).

**Diff summary** (per `gh pr view 344`): 20 files / +1465:
- `scripts/generate_hu_situations.py` (+185/-67) — patched generator (board fields now mutate per `variation_param`)
- `scripts/test_generate_hu_situations.py` (+197) — NEW: 8 unit tests for per-anchor flop/turn/river uniqueness
- `data/hu_corpus/pilot_50_v2/situations.jsonl` — 50 generated lookalikes
- `data/hu_corpus/pilot_50_v2/raw_labels.jsonl` + 5 per-labeller raw files — 5 × 50 = 250 outputs
- `data/hu_corpus/pilot_50_v2/consensus.jsonl` — 50 hands consensus + confidence
- `data/hu_corpus/pilot_50_v2/calibration_results.jsonl` + 5 per-labeller calibration files
- `data/hu_corpus/pilot_50_v2/opus_tier_up.jsonl` — 11 tier-up entries (10 non-unanimous spots + 1 audit)
- `data/hu_corpus/pilot_50_v2/similarity_distance_audit.jsonl` — per-spot similarity assignment
- `data/hu_corpus/pilot_50_v2/labeller_brief.md` — labeller brief used
- `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_V2_2026-05-10.md` — execution log + flagged issues

**Title claim**: 96% gate PASS (39 unanimous + 2 majority + 7 with Opus agreeing → 48/50 effective consensus); 3 owner-arbs (HU-1.5-LK-10 re-confirm + HU-1.4-LK-04 + HU-1.4-LK-05). v2 96% gate is structurally honest vs v1's 96% (v1 inflated by 25 anchor-identical lookalikes; v2 has truly diverse boards).

Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.3 v2 produces fix-pilot data feeding 1.5-D.3 FULL → 1.5-D.4 retrain — milestone-class).

## Audit scope (~15-20 min; 10-item per generator-fix dispatch §"QC stream — what you audit")

Per dispatch `MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md` §"QC stream — what you audit":

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 20 PR files in scripts/ + data/hu_corpus/pilot_50_v2/ + review/comms/. NO unauthorized source/prompt/model edits beyond the named generator file + new test file.
2. **Generator fix verification**: read patched `scripts/generate_hu_situations.py` + assert the bug condition no longer present (board_flop / board_turn / board_river fields actually mutate per `variation_param` instead of being copied from anchor).
3. **Unit tests pass**: invoke `python3 scripts/test_generate_hu_situations.py` (or pytest equivalent per `docs/PROCESS_GUIDE.md`). Title claims 8/8 PASS — verify count + content (per-anchor flop/turn/river uniqueness).
4. **Re-pilot board diversity** (the heart of v2 vs v1): sample 10 spots from `data/hu_corpus/pilot_50_v2/situations.jsonl`; verify board fields differ from anchor where `variation_param` describes board mutation. Per anchor (5 lookalikes per anchor × 10 anchors), verify ≥4 of 5 lookalikes show distinct boards.
5. **5 labellers per spot + calibration**: 5 distinct labeller IDs × 50 spots = 250 entries in raw_labels; calibration ≥20/24 (or ≥20/28 per builder's L4-perfect claim) + GTO-reversal anchors all correct. Per-labeller calibration files present.
6. **Bucket-first compliance** per `feedback_bucket_first_labelling.md`: labelling prompt does NOT contain equity thresholds.
7. **Consensus rule applied**: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 → owner-arbitrated. Tier-up rule: non-unanimous Sonnet → Opus; Opus disagrees → owner-arb. Verify 39 unanimous + 2 majority + 7 with Opus agreeing + 2 NEW owner-arbs (HU-1.4-LK-04/05) + 1 propagated owner-arb (HU-1.5-LK-10) = 50.
8. **Pilot gate verification — HONESTY CHECK**: dispatch §(b) item 8 explicitly notes "anchor-stability inflation should be gone; expect 80-90% range, not 96%". Builder reports 96% on TRULY DIVERSE boards. QC must independently verify the 96% is HONEST (not residual anchor-stability inflation). Sample-check: do similar-anchor lookalikes get HIGH agreement (true label consistency) or do diverse-anchor lookalikes get HIGH agreement (suspicious — would suggest collapsed labelling)?
9. **HU-1.5-LK-10 propagation**: dispatch §(a) item 4 — propagation logic is "same board → CALL with solver-verification-pending; v2 board differs → re-evaluated independently". Verify which path the v2 spot took. Builder claims §(a) "same board, bet-sizing variation only" → CALL re-confirmed. QC verifies v2 board IS the same as v1.
10. **TC-X-DISPATCH-COMPLIANCE**: generator-fix dispatch + (a) propagation + (b) re-pilot scope + negative scope items honored. Builder did NOT skip-fixes-and-fire-FULL (would have been STOP > improvise violation).

## Special audit consideration: architect-hat consults flagged

Builder report flags 2 architect-hat consults in PR body:

1. **Calibration contamination (4th instance)** — `grep` reveals expert_action on hard anchors; sanitized JSONL extracts deferred to FULL infrastructure. QC assesses: did contamination invalidate the 5/5 calibration PASS (e.g., labellers may have used contaminated info)? OR did labellers ignore it (calibration scores still reflect true ability)? If invalidating: BLOCKER for FULL; if not: deferral to FULL infrastructure is acceptable.
2. **API rate-limit during parallel labeller dispatch** — required serial-overlap retry cascade. QC verifies the cascade did NOT cause partial-batch corruption (any labeller missing entries / out-of-order labels / duplicate calls). If clean: tactical fix is acceptable.

These are HOW questions for orchestrator decision. QC reports findings + severity; orchestrator decides whether they block FULL dispatch or are deferred to FULL infrastructure work.

## Owner-arbitration surface (3 spots)

Orchestrator surfaces to owner separately AFTER QC verdict (HOLDs FULL dispatch until owner adjudicates):

1. **HU-1.5-LK-10** (re-confirmation): builder claims §(a) propagation — same board as v1 owner-CALL, only bet-sizing variation. Owner already adjudicated CALL on 2026-05-10 (queued for solver verification). Re-confirm acceptable per dispatch §(a) item 4.
2. **HU-1.4-LK-04** (NEW): Sonnet 3-2 RAISE majority; Opus disagrees with CALL. Small-probe RAISE-vs-CALL on TT overpair. Owner-judgment required.
3. **HU-1.4-LK-05** (NEW): same shape as HU-1.4-LK-04 (Sonnet 3-2 RAISE; Opus CALL; TT overpair small-probe). Owner-judgment required.

NEW spots will be added to solver-verification queue per `feedback_solver_verification_queue.md` if owner flags for solver check.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~15-20 min wall-clock. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr344-phase15d3-pilot-v2.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D3_PILOT_V2_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #344 merge → on QC PASS (or PASS-WITH-FINDINGS where findings are deferred-to-FULL-infrastructure), orchestrator merges autonomously per standing directive
- 3 owner-arbs (HU-1.5-LK-10 re-confirm + HU-1.4-LK-04 + HU-1.4-LK-05) → orchestrator surfaces to owner; HOLDs FULL dispatch until owner adjudicates
- Architect-hat consults (calibration contamination, rate-limit) → orchestrator decides per QC findings + dispatch
- After QC verdict + owner adjudications + architect decisions → orchestrator authorizes Phase 1.5-D.3-FULL dispatch (700 lookalikes from HU-2..HU-6 anchors)
- Solver-verification queue (HU-6.5 + HU-1.5-LK-10 + any new flagged spots from this PR) MUST drain before 1.5-D.4 retrain ships per `feedback_solver_verification_queue.md`

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `60bb850` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Generator-fix dispatch: master `60bb850` (PR #343)
- 1.5-D.3 v1 PILOT merged: master `a2b97e2` (PR #339)
- v1 QC verdict PASS-WITH-FINDINGS: master `2f04f34` (PR #342)
- Builder PR #344 head: `29de5da`
- HU-1.5-LK-10 owner-CALL adjudication: master `60bb850` (PR #343 dispatch §(a))
- HU-1.5 axis spec: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`
- HU-1.4 axis spec: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md` (HU-1.4 entries)
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_solver_verification_queue.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #344 PILOT V2. ~15-20 min wall-clock. 10-item audit + 2 architect-hat consult assessments + gate-honesty check (96% claimed on diverse boards, vs dispatch's 80-90% expectation). Heartbeat sync to current master at end of tick. Orchestrator merges PR #344 + verdict autonomously on PASS. 3 owner-arbs surfaced separately. FULL dispatch HOLDs on owner adjudications + architect decisions.**
