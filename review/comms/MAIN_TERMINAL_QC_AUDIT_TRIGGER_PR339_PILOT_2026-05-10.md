---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #339 — Phase 1.5-D.3 PILOT (50 HU lookalikes from HU-1 axis × 5 labellers + Opus tier-up; gate PASS 96%; 1 owner-arb HU-1.5-LK-10; 1 generator bug flagged) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #339 (PILOT)

PR #339: `programmer/phase15d3-pilot-2026-05-10`. Head `7470147385ad22c23dfa4a6bfc61714cb1dfbd66`. Title: "Builder Phase 1.5-D.3 PILOT: 50 HU lookalikes (HU-1 axis) × 5 labellers + Opus tier-up — pilot gate PASS at 96%; 1 owner-arb (HU-1.5-LK-10) + 1 generator bug flagged for FULL fix".

**Diff summary** (per `gh pr view 339`): 9 files / +963:
- `scripts/generate_hu_situations.py` — generator script (276 lines)
- `data/hu_corpus/pilot_50/situations.jsonl` — 50 generated lookalikes
- `data/hu_corpus/pilot_50/raw_labels.jsonl` — 5 labellers × 50 = 250 outputs
- `data/hu_corpus/pilot_50/consensus.jsonl` — 50 hands consensus
- `data/hu_corpus/pilot_50/calibration_results.jsonl` — 5 labellers calibration
- `data/hu_corpus/pilot_50/opus_tier_up.jsonl` — 7 non-unanimous (1 disagreement → owner-arb HU-1.5-LK-10)
- `data/hu_corpus/pilot_50/similarity_distance_audit.jsonl` — per-spot similarity assignment
- `data/hu_corpus/pilot_50/labeller_brief.md` — labeller brief used
- `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_2026-05-10.md` — execution log + flagged issues

**Title claim**: 96% gate PASS (49/50 ≥4-of-5; 49 consensus + 1 owner-arb). 1 generator bug surfaced for FULL phase fix.

## Audit scope (~15-20 min; 10-item per dispatch)

Per dispatch `MAIN_TERMINAL_HU65_OWNER_ADJUDICATION_AND_PHASE15D3_DISPATCH_2026-05-10.md` §"QC stream — what you audit":

1. **Diff scope strict** (TC-23): 9 PR files in scripts/ + data/hu_corpus/pilot_50/ + review/comms/. NO unauthorized source/prompt/model edits.
2. **Generation script quality**: `generate_hu_situations.py` reads from `design/hu_reference_set/` + outputs valid jsonl. **Verify the generator-bug claim independently** (board_flop/board_turn/board_river fields unchanged from anchor while variation_param prose describes board mutations). Flag severity for FULL phase.
3. **Pool size**: ~3000 generated; 50 filtered for pilot.
4. **Similarity-band threshold**: similarity_distance_audit.jsonl shows per-spot assignment within architect-committed threshold; rationale documented.
5. **5 labellers per spot + calibration**: 5 IDs × 50 spots = 250 entries in raw_labels; calibration ≥20/24 + 3 GTO-reversal correct for all 5.
6. **Bucket-first compliance** + solver-vs-labels separation.
7. **Consensus rule applied**: ≥4-of-5 → consensus; 3-2 → solver verification + majority; 2-2-1 → owner-arbitrated. HU-1.5-LK-10 routed correctly per 3-2-with-Opus-disagreement → owner-arb (consensus_action = null).
8. **Pilot gate verification**: ≥80% labeller-consensus rate cleared at 96%; documented.
9. **HU-6.5 owner-adjudication propagation check**: pilot is HU-1 axis only; HU-6.5 lookalikes appear in FULL phase — N/A here. But verify HU-1.5 anchor consensus action (CALL from 1.5-D.2 PILOT) is reflected in HU-1.5-LK consensus where applicable.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.4 spec + pilot+full split + solver-pending gating + negative scope items honored. Generator-bug surface is genuine (per CLAUDE.md §5 STOP > improvise — builder correctly flagged rather than fixed-forward).

## Special audit consideration: generator bug severity

QC should assess whether the generator bug invalidates pilot gate clearance:
- **If pilot consensus is partly anchor-stability** (5 lookalikes × 1 actual board variation), the 96% PASS reflects labeller agreement on the *anchor*, not on diverse lookalikes
- This is genuinely "STOP > improvise" territory per CLAUDE.md §5 — builder did the right thing flagging
- QC verdict should explicitly recommend: PASS-WITH-FINDINGS (data is committable; FULL phase BLOCKED on generator fix) OR REJECT (re-run pilot after generator fix)

## Owner-arbitration surface (HU-1.5-LK-10)

Orchestrator surfaces HU-1.5-LK-10 to owner separately: same hero/board as 1.5-D.2 HU-6.5-equivalent spot but ~112% overbet (vs anchor's 75% pot bet). Pot odds threshold shifts 30% → 35%. Owner-judgment whether previous CALL adjudication propagates at the larger size.

## QC routing + Output

Standalone stream. ~15-20 min. QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr339-phase15d3-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D3_PILOT_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- PR #339 merge → on QC PASS or PASS-WITH-FINDINGS, orchestrator merges autonomously; data is captured + flagged
- HU-1.5-LK-10 owner-arbitration → orchestrator surfaces to owner for adjudication
- Generator bug → orchestrator HOLDs FULL batch dispatch until generator fix lands (per dispatch STOP-condition discipline; FULL would replicate the bug at 14x scale)
- After QC verdict + owner adjudication on HU-1.5-LK-10 + generator-fix dispatch + builder generator-fix PR + QC PASS on fix → orchestrator authorizes FULL batch dispatch

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `c54eab1` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.3 dispatch + HU-6.5 adjudication: master `c54eab1` (PR #338)
- Builder PR #339 head: `7470147`
- HU-1.5 axis spec: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`
- 1.5-D.2 HU-1 PILOT (HU-1.5 anchor 5/5 unanimous): master `bed7368` (PR #332)
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #339 PILOT. ~15-20 min wall-clock. 10-item audit + special generator-bug severity assessment. Heartbeat sync at end. Orchestrator merges PR #339 + verdict autonomously on PASS. HU-1.5-LK-10 owner-arbitration surfaced separately. FULL batch dispatch HOLDs on generator fix.**
