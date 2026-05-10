---
date: 2026-05-10
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #350 — Phase 1.5-D.3 FULL INFRA-PREP (HU-2..HU-6 generator extension + sanitization + 696 situations + §(c.1)+§(c.3) decisions; §(c.2) DESIGN-ONLY; labelling deferred to next session) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #350 (FULL INFRA-PREP)

PR #350: `programmer/phase15d3-full-infra-prep-2026-05-10`. Head `aab92ec9fdede58f4d32f501fdff9680de58ea6d`. Title: "Builder Phase 1.5-D.3 FULL INFRA-PREP: HU-2..HU-6 generator + sanitization + 696 situations + architect decisions §(c.1)+§(c.3) (labelling deferred to next session per context budget)".

Builder fired infrastructure-prep portion of Phase 1.5-D.3 FULL dispatch (`MAIN_TERMINAL_HU14_ADJUDICATION_AND_PHASE15D3_FULL_DISPATCH_2026-05-10.md`, master `e58ed94` after PR #349 data-fix landing on `bfebd13` dispatch merge). Builder applied `feedback_pilot_first_for_long_jobs.md` STANDING RULE + CLAUDE.md §5 STOP > improvise to split INFRA-PREP from LABELLING (deferring 3480 LLM calls + Opus tier-up + consensus + report to next session).

**Orchestrator-decision on the split:** ACCEPTED. Reasons:
1. Quality-default per owner: avoiding mid-batch context-budget exhaustion (which would force improvised recovery)
2. Pilot+full standing rule applies to ANY long batch, not just the original spec's pilot+full split
3. Builder's split allows orchestrator + QC pre-merge audit of infrastructure BEFORE 3480-LLM-call commitment
4. CLAUDE.md §5 STOP > improvise is correctly invoked

**Diff summary** (per `gh pr view 350`): 10 files / +3700 / -23:
- `scripts/generate_hu_situations.py` (+148/-23) — extended with main_full() for HU-2..HU-6 generation
- `scripts/hu_anchors_axes_2_6.py` (+468) — NEW: anchor data for HU-2..HU-6 (24 anchors; HU-6.5 excluded per PR #338)
- `scripts/sanitize_calibration_extracts.py` (+216) — NEW: §(c.1) sanitization implementation
- `data/hu_corpus/full_HU2_HU6/calibration_sources/3way_combined_350_SANITIZED.jsonl` (+351) — sanitized calibration extract
- `data/hu_corpus/full_HU2_HU6/calibration_sources/BATCH2_8_HAND_DESIGNS_SANITIZED.md` (+870) — sanitized hand-designs source
- `data/hu_corpus/full_HU2_HU6/calibration_sources/test_set_50_labelled_SANITIZED.jsonl` (+50) — sanitized test-set extract
- `data/hu_corpus/full_HU2_HU6/situations.jsonl` (+696) — 24 anchors × 29 lookalikes = 696 situations
- `data/hu_corpus/full_HU2_HU6/similarity_distance_audit.jsonl` (+696) — per-spot similarity assignment
- `data/hu_corpus/full_HU2_HU6/labeller_brief.md` (+75) — labeller brief used
- `review/comms/BUILDER_REPORT_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md` (+130) — execution log + architect decisions + deferral rationale

**Title claim**:
- §(c.1) sanitized JSONL extracts IMPLEMENTED + verified zero-match grep
- §(c.2) throttle-aware batching DESIGNED (implementation in next session alongside labelling)
- §(c.3) stale composition Path (b) chosen + documented per pilot V2 evidence
- 696 situations across 24 anchors × 29 lookalikes (vs dispatch spec ~700; close enough — similarity-band filter trim)

Pre-merge QC required per `feedback_qc_required_before_approval.md` (1.5-D.3 FULL infrastructure feeds 700-spot labelling → 1.5-D.4 retrain — milestone-class).

## Audit scope (~20-25 min; expanded for §(c) decisions)

10-item audit:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 10 PR files. Generator extension + new anchor module + sanitization script + sanitized calibration files + situations + similarity audit + labeller_brief + builder report. NO unauthorized source/prompt/model edits beyond named files. Verify NO labelling outputs (raw_labels.jsonl / consensus.jsonl) — split was deliberate; their absence is a positive signal.

2. **§(c.1) Sanitization verification — INDEPENDENT GREP**:
   - Read patched `scripts/sanitize_calibration_extracts.py`; understand sanitization logic.
   - Run `grep -E "expert_action|expert_reasoning|oracle_action" data/hu_corpus/full_HU2_HU6/calibration_sources/*.jsonl data/hu_corpus/full_HU2_HU6/calibration_sources/*.md` → assert ZERO matches.
   - QC may extend to grep for any other forward-leaking field discovered (e.g., `expected_action`, `correct_action`, `solver_action`).
   - Builder report mentions "13 forbidden fields" — verify the list is sufficient (QC's call on completeness).

3. **Generator extension verification**:
   - `scripts/generate_hu_situations.py` extended to `main_full()`; verify: no breakage of `main_pilot()` (which produced PILOT V2 50 hands); main_full produces 696 situations from 24 anchors × 29 each.
   - 8/8 unit tests still PASS (re-run `python3 scripts/test_generate_hu_situations.py`).
   - Per-anchor board diversity preserved on decision-street (consistent with PILOT V2 6/anchor pattern but scaled).

4. **Anchor coverage**: `scripts/hu_anchors_axes_2_6.py` defines 24 anchors. Verify:
   - 24 ≠ 25 (HU-6.5 excluded per PR #338 owner adjudication; verify exclusion is explicit)
   - HU-2.1..HU-2.5, HU-3.1..HU-3.5, HU-4.1..HU-4.5, HU-5.1..HU-5.5, HU-6.1..HU-6.4, HU-6.6 (or whatever the architecture is) covered
   - Anchor data matches `design/hu_reference_set/HU_AXIS_*.md` specs

5. **696 situations**: situations.jsonl has 696 entries; per-anchor count = 29 each (24 × 29 = 696). similarity_distance_audit.jsonl has matching 696 entries. variation_axes are correctly distributed per anchor (5 board_runout + 5 effective_stack + 5 villain_action + 5 villain_bet_sizing + 9 axis-specific = 29; or whatever spec).

6. **§(c.2) DESIGN assessment**: builder ships DESIGN, not implementation. Per builder report:
   - per-labeller serial + parallel agents + backpressure + retry + append-only durability
   - QC assesses: is this design sufficient for 14x scale (3480 calls)?
   - Specifically: does append-only durability handle resumption-after-crash without double-counting? Does backpressure handle rate-limit headers correctly? Concurrency limit specified?
   - If design insufficient: SHOULD_FIX (amend before next-session labelling fires).

7. **§(c.3) path-(b) justification assessment**: builder chose path (b) "accept stale composition with justification". Per builder report:
   - Pilot V2 evidence (5/5 labellers correctly read board fields and ignored stale composition prose)
   - QC assesses: does the prose-decoration claim hold at FULL scale (3480 outputs vs PILOT's 250)? Are there counter-examples (e.g., spots where prose contradicts board in ways labellers might not catch)?
   - If insufficient: SHOULD_FIX (require path-(a) generator fix before labelling).

8. **labeller_brief**: bucket-first compliance + solver-vs-labels separation + sanitized-extract guidance.

9. **Pilot V2 vs FULL alignment**: similarity-band threshold same as PILOT V2 (architect committed in 1.5-D.3 PILOT V2; same threshold applies). Per-anchor lookalike count 29 vs PILOT V2's 10 — verify reasoning (FULL needs higher density; 24 anchors × 29 = 696, vs HU-1's 5 × 10 = 50).

10. **TC-X-DISPATCH-COMPLIANCE**: dispatch §(b) scope + §(c) decisions + negative-scope items honored. Builder split decision documented + justified.

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~20-25 min wall-clock (larger than usual due to sanitization grep + §(c) design assessment). QC writes:
- `~/river-rats-qc/findings/2026-05-10-pr350-phase15d3-full-infra-prep.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE15D3_FULL_INFRA_PREP_2026-05-10.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master

## What gates

- PR #350 merge → on QC PASS, orchestrator merges autonomously per standing directive (split is accepted)
- §(c.2) DESIGN sufficiency → if QC SHOULD_FIX: orchestrator amends-and-re-fires (builder updates design before labelling fires)
- §(c.3) path-(b) justification → if QC SHOULD_FIX: orchestrator amends-and-re-fires
- After QC PASS + merge → orchestrator authorizes Phase 1.5-D.3 FULL LABELLING-EXECUTION dispatch (next session resumption with builder firing 3480 LLM calls + Opus tier-up + consensus + builder report)
- After FULL LABELLING PR + QC + owner-arb adjudications (if any) + solver-queue drain → orchestrator authorizes 1.5-D.4

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e58ed94` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-D.3 FULL dispatch: master `bfebd13` (PR #348)
- HU-1.4 data-layer-fix merged: master `e58ed94` (PR #349)
- 1.5-D.3 PILOT V2 merged: master `4432f68` (PR #344); v2 QC verdict: master `b790524` (PR #346; PASS · 0/0/0)
- Builder PR #350 head: `aab92ec`
- Architect's design memo §4.3 + §4.4 + §4.5: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Generator file (V3 with main_full): `scripts/generate_hu_situations.py`
- Generator unit tests: `scripts/test_generate_hu_situations.py`
- Anchor data NEW: `scripts/hu_anchors_axes_2_6.py`
- Sanitization NEW: `scripts/sanitize_calibration_extracts.py`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_verification_queue.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_optional_is_not_authorized.md`, `project_qc_heartbeat_convention.md`

**Status: QC stream — fire audit now on PR #350 FULL INFRA-PREP. ~20-25 min wall-clock. 10-item audit + sanitization grep verification + §(c.2) DESIGN sufficiency assessment + §(c.3) path-(b) justification assessment. Heartbeat sync to current master at end of tick. Orchestrator merges PR #350 + verdict autonomously on PASS. Then authorizes next-session FULL LABELLING-EXECUTION dispatch (3480 LLM calls + Opus tier-up + consensus + report).**
