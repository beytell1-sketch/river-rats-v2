---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (builder; architect-hat for §(c.2) implementation)
re: Phase 1.5-D.3 FULL LABELLING-EXECUTION dispatch — implement §(c.2) throttle-aware batching DESIGN + run 3480-LLM-call labelling pipeline (5 Sonnet labellers × 696 situations + Opus tier-up + consensus + builder report)
status: DISPATCH — fire now (next builder session resumption)
---

# Phase 1.5-D.3 FULL LABELLING-EXECUTION — dispatch

INFRA-PREP cleared (PR #350 merged at master `6274fce`; QC PR #352 PASS · 0/0/0). LABELLING-EXECUTION authorized to fire.

## Scope

Run the 3480-LLM-call labelling pipeline on `data/hu_corpus/full_HU2_HU6/situations.jsonl` (696 situations from 24 anchors HU-2..HU-6, HU-6.5 excluded) using the §4.3 5-labeller + Opus tier-up + consensus architecture, with §(c.2) throttle-aware batching IMPLEMENTED per the QC-approved DESIGN.

**Implementation sequence:**

1. **Implement §(c.2) throttle-aware batching** per QC-approved DESIGN in `BUILDER_REPORT_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md` (per-labeller serial + parallel agents + backpressure + retry + append-only durability). Builder-architect-hat finalizes implementation details:
   - Concurrency limit (e.g., max-N-concurrent-labellers, token-bucket per minute)
   - Backoff (exponential + jittered + retry-after-header-aware)
   - Append-only durability: each labeller writes to its own per-spot append-only output file; resumption test passes (kill mid-batch, resume, no duplicate or missing entries)
   - Wall-clock budget estimate documented in BUILDER_REPORT before labelling fires

2. **Recovery-resumption test** (per dispatch §(c.2) verification gate): kill mid-batch + resume + assert (a) no duplicate (labeller_id, spot_id) tuples, (b) no missing tuples, (c) no corrupt/partial entries. Document in BUILDER_REPORT.

3. **5 fresh Sonnet labellers** (NEW pool; not L1..L5 from PILOT V2). Each passes calibration ≥20/24 (or ≥20/28 per current scheme) + GTO-reversal anchors all correct. Failed labellers NOT in raw_labels.

4. **3480 LLM calls** (5 × 696). Output: `data/hu_corpus/full_HU2_HU6/raw_labels.jsonl` + 5 per-labeller raw_labels files + per-labeller calibration_results files.

5. **Opus tier-up sample** for non-unanimous Sonnet hands per §4.3 tier-up rule. Output: `data/hu_corpus/full_HU2_HU6/opus_tier_up.jsonl`.

6. **Consensus assembly** per §4.3 consensus rule:
   - ≥4-of-5 → consensus
   - 3-2 with Opus agree → consensus = majority
   - 3-2 with Opus disagree → owner-arb required (consensus_action = null)
   - 2-2-1+ → owner-arb required (consensus_action = null)
   Output: `data/hu_corpus/full_HU2_HU6/consensus.jsonl` (696 entries).

7. **Builder report** `review/comms/BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md`:
   - §(c.2) implementation summary + concurrency/backoff/durability params
   - Recovery-resumption test result
   - Labeller pool composition (5 Sonnet IDs + Opus ID; calibration scores)
   - Per-axis confidence summary (HU-2 / HU-3 / HU-4 / HU-5 / HU-6)
   - Gate verification: ≥4-of-5 base rate; tier-up resolution; effective consensus rate
   - Owner-arb surface (count + spot_ids + per-spot RAISE/CALL/etc. distribution + Opus position)
   - Any HU-6.5-propagation lookalikes (per §(b) item from FULL dispatch §(b) "Pilot V2 owner-adjudications baked in")
   - Any unexpected behaviors flagged for orchestrator decision (TC-X-OPERATIONAL-DEVIATION-ASSESSMENT pattern)

## Gate

- Base ≥4-of-5 labeller-consensus rate ≥80% (matches pilot V2's 82%)
- Effective consensus rate after Opus tier-up ~95% (matches pilot V2's 96%)
- Owner-arbs surface as PR-level artifacts; orchestrator surfaces to owner BEFORE merging FULL LABELLING PR

## STOP conditions (per CLAUDE.md §5)

- §(c.2) implementation diverges from QC-approved DESIGN → flag as architect-hat consult; orchestrator decides whether to amend dispatch or proceed
- Recovery-resumption test FAILS → STOP and report; do NOT fire 3480 LLM calls until durability is proven
- Calibration contamination resurfaces (despite §(c.1) sanitization) → STOP and report; investigate root cause
- API rate-limit cascade triggers DESIGN-not-handled fall-back path → STOP and report; do NOT improvise recovery
- Per-axis gate <80% → STOP and report; QC may re-pilot or owner may adjudicate

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT modify the merged INFRA-PREP files (`scripts/generate_hu_situations.py`, `scripts/hu_anchors_axes_2_6.py`, `scripts/sanitize_calibration_extracts.py`, `data/hu_corpus/full_HU2_HU6/situations.jsonl`, `similarity_distance_audit.jsonl`, `labeller_brief.md`, sanitized calibration_sources/) — those are the prepared inputs
- ❌ Does NOT modify §4.3 labelling-pipeline architecture or §4.4 corpus-assembly architecture
- ❌ Does NOT include any HU-1 axis lookalikes (those are in pilot_50_v2/)
- ❌ Does NOT relabel HU-6.5 anchor (already adjudicated; in solver queue)
- ❌ Does NOT use solver output as training label
- ❌ Does NOT fire labelling before §(c.2) recovery-resumption test passes
- ❌ Does NOT improvise on STOP conditions

## Pilot V2 owner-adjudication propagation (§(b) item from FULL dispatch)

If any HU-2..HU-6 lookalike's variation_axis is `villain_bet_sizing` AND anchor board is unchanged AND anchor itself was owner-adjudicated (HU-6.5 → CALL): inherit the owner-adjudication. Apply to consensus.jsonl row with explicit notes citing PR #338. Builder identifies these spots during consensus assembly + flags in BUILDER_REPORT.

## QC stream — what you audit (post-PR; standalone, ~25-30 min)

10-item audit:

1. Diff scope strict per dispatch (raw_labels + consensus + opus_tier_up + per-labeller calibration files + builder report; NO source/INFRA-PREP-file edits beyond §(c.2) implementation in dedicated module if any)
2. §(c.2) implementation matches DESIGN per QC-approved INFRA-PREP review; recovery-resumption test result documented + assessed
3. 696 spots × 5 labellers = 3480 raw_labels entries; per-labeller counts 696 each; per-spot counts 5 each
4. Calibration: all 5 labellers PASS ≥20/24 (or ≥20/28) + GTO-reversal correct; failed labellers NOT in raw_labels
5. Bucket-first compliance + solver-vs-labels separation in raw_labels reasoning (sample-check 10 spots)
6. Opus tier-up: non-unanimous Sonnet hands sampled; tier-up rule applied (Opus agree → consensus; Opus disagree → owner-arb)
7. Consensus rule applied per §4.3: ≥4-of-5 → consensus; 3-2 → tier-up + majority/owner-arb; 2-2-1+ → owner-arb
8. Per-axis confidence summary (HU-2..HU-6) in builder report; gate ≥80% base ≥4-of-5 rate
9. Pilot V2 owner-adjudication propagation correctness (any HU-6.5-similar spots inherit owner-CALL)
10. TC-X-DISPATCH-COMPLIANCE per this comm

QC routing per `feedback_qc_routing_when_standalone_active.md`. Heartbeat + cross-post per protocol.

## Owner — informational

- Standing directive: orchestrator merges this dispatch + builder LABELLING PR + QC verdict autonomously per quality default (post-owner-adjudication on any new owner-arbs that surface in FULL labelling)
- After FULL LABELLING PR + verdict merge → orchestrator authorizes Phase 1.5-D.4 (HU model retrain on 59-surface, from-scratch per §4.5) AFTER solver-queue drain (4 spots: HU-6.5 + HU-1.5-LK-10 + HU-1.4-LK-04 + HU-1.4-LK-05; all CALL)
- Loop CONTINUES through 1.5-D.4 → 1.5-E (router/coaching) → Phase 2 D5 (deferred per blueprint)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `6274fce` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.3 FULL INFRA-PREP merged: master `6274fce` (PR #350 + QC PR #352 PASS)
- 1.5-D.3 FULL dispatch: master `bfebd13` (PR #348)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict: master `b790524` (PR #346; PASS · 0/0/0)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- Architect's design memo §4.3 + §4.4 + §4.5: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Generator file (V3 with main_full): `scripts/generate_hu_situations.py`
- Anchor data: `scripts/hu_anchors_axes_2_6.py`
- Sanitization: `scripts/sanitize_calibration_extracts.py`
- INFRA-PREP situations: `data/hu_corpus/full_HU2_HU6/situations.jsonl`
- INFRA-PREP labeller brief: `data/hu_corpus/full_HU2_HU6/labeller_brief.md`
- INFRA-PREP sanitized calibration sources: `data/hu_corpus/full_HU2_HU6/calibration_sources/`
- INFRA-PREP builder report (with §(c.2) DESIGN + §(c.3) path-(b) justification): `review/comms/BUILDER_REPORT_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md`
- INFRA-PREP QC verdict: `review/comms/REVIEW_QC_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_verification_queue.md`, `feedback_bucket_first_labelling.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_river_rats_team_structure.md`, `project_qc_heartbeat_convention.md`

**Status: Phase 1.5-D.3 FULL LABELLING-EXECUTION fires LEAD-PROGRAMMER. Implement §(c.2) throttle-aware batching per QC-approved DESIGN; run recovery-resumption test FIRST; on PASS, fire 3480-LLM-call labelling pipeline; assemble consensus; surface any owner-arbs in BUILDER_REPORT. Solver-verification queue (4 spots; all CALL) tracked for pre-1.5-D.4 drain. Loop CONTINUES through LABELLING → QC → owner-arbs → solver-queue drain → 1.5-D.4 dispatch.**
