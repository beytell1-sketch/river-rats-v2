---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #236 — 12.5I-MW40-VERIFICATION-B situation generation (Path γ' amended; 30 J-on-board variants; pre-flight 4-check PASS) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #236

PR #236: `programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06` (head `58ac0d6`). Builder report: `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` (in branch). Includes the original HALT query comm (`BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md`) as part of the squash-merge audit trail.

Per dispatch `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235) AS AMENDED BY `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` (master `42460ae`, PR #237). Path γ' is the active spec.

## Audit scope (8 items per amended dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (squash-merge contribution against `master = 42460ae`):
   - `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (30 situations; 61-surface feat_dict)
   - `scripts/generate_125i_mw40_verif_situations.py` (factory script)
   - `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` (builder report)
   - `review/comms/BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md` (HALT query record; carry-forward audit trail)
   
   Verify NOT touched: v3.x prompts (`prompts/`), BATCH2 reference (`design/multiway_reference_set/BATCH2_*`), `river-rats-core/` source, training-data, existing 788-corpus or any prior-phase corpus files, memory files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Pre-flight 4-check correctness (Hybrid pilot-first per PR #228 SHOULD_FIX-1 Path 3)** — verify builder ran the 4 pre-flight checks on first 5 emitted situations BEFORE emitting the remaining 25. Builder report must explicitly show pre-flight result per check:
   - Schema parity (61-surface; 0 NaN/Inf/missing)
   - Step-18 feature plausibility (both ≈ 0 across J-on-board variants)
   - ref_id namespace integrity (`PILOT_MW40_VERIF_001..005` disjoint)
   - Top-level structural fields match plan §3 constraint table

   PR title says "pre-flight 4-check PASS" — verify this claim against the report's actual pre-flight section.

3. **Row count integrity** — 30 / 30 emitted; ref_id namespace `PILOT_MW40_VERIF_001..030` exact; 0 collisions with existing 788-corpus or prior 12.5I ref_ids (specifically vs 694 + 94-revision corpus from PR #213 + PR #222).

4. **Sub-axis distribution (AMENDED to 15/0/15 per Path γ')** — sub-axis A = 15 exact; sub-axis B = 0 (dropped); sub-axis C = 15 exact. **Blocker split = 30/0 (uniform with-J-blocker; no STOP per amendment) — REPORT only, not BLOCKER.**

5. **Schema integrity** — 61-surface uniform across all 30; 0 NaN/Inf in 30 × 61 = 1830 values.

6. **Step-18 activation pattern** — verify both Step-18 features ≈ 0 across all 30 variants (hero IP + no nut-FD blocker semantics on J-on-board); flag any non-zero pattern as informational (not a finding).

7. **TC-X-DISPATCH-COMPLIANCE (3rd formal exercise)** — cross-check builder's implementation against amended dispatch:
   - Did builder run all 4 pre-flight checks on first 5 emitted?
   - Did builder emit only 15/0/15 sub-axis distribution per Path γ' (not 10/10/10 from original)?
   - Did builder leave PR #228's NIT-1/NIT-2 alone (no auto-fix to plan)?
   - Did builder NOT modify the merged plan (`PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`)?
   - Did builder pin T-kicker (no adjacent-kicker control variants)?
   - Any unilateral deviation → SHOULD_FIX (mirror PR #228 SHOULD_FIX-1 pattern).

8. **Path γ' compliance (NEW; per amendment)** — verify:
   - Builder selected 5 additional boards per sub-axis A and C (matching plan §3 constraint table)
   - All 30 boards match plan §3 constraint table (BTN, IP, non-PFA, num_opponents=3, FLOP SoD, villain_check_through_count=3, effective_stack=200bb, hand_category=6, kicker_class=T-kicker, is_rainbow=1, pot_odds=0.0)
   - Sub-axis A: 15 J-high-flop boards (J as highest card; non-paired)
   - Sub-axis C: 15 J-medium-flop boards (J as middle card; ≤2 paired-J variants total in C)
   - Builder report includes §"Board list (PR #236-amended)" section documenting the 5 additional boards per sub-axis
   - Hero TJ uniform across all 30 (no TT or T9 in any variant)

## QC routing

Standalone stream (`~/river-rats-qc/`) per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit (mini-phase situation-generation milestone). Expected duration: ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` on `qc/pr236-mw40-verification-b-review-2026-05-06`. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #236 merge → on QC PASS (no Opus tier-up needed; deterministic factory; no labelling outputs)
- 12.5I-MW40-VERIFICATION-C labelling round dispatch → on PR #236 merge (5 Sonnet × 30; pilot-first 5-hand gate per `feedback_pilot_first_for_long_jobs.md`; ~$5-10 LLM cost)
- 12.5J-C trainer integration test on 61-surface → on PR #236 merge (parallel queue with -C in builder serial)

## What you do NOT do

- Do NOT make GTO judgments on whether CHECK is the right design_action (verification target; Sonnet+Opus consensus during -C/-D will produce empirical answer)
- Do NOT modify any file (review-only)
- Do NOT recommend further blocker-effect work (deferred to follow-up phase post-graduation per PR #237 amendment)
- Do NOT recommend reverting Path γ' (orchestrator-decision per `feedback_orchestrator_decides_not_recommends.md`)
- Do NOT run training or inference

## References

- 12.5I-MW40-VERIFICATION-B amended dispatch (Path γ'): `MAIN_TERMINAL_PR236_MW40B_RESOLUTION_2026-05-06.md` (master `42460ae`, PR #237)
- Original -B dispatch (superseded by Path γ' amendment): `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235)
- HALT query (audit trail): `BUILDER_QUERY_PHASE125I_MW40_VERIFICATION_B_BLOCKER_DEFINITION_2026-05-06.md` (PR #236 first commit `bfdda9f`)
- PR #228 (Plan with §4 contradiction; merged): master `e0e0304`
- PR #231 (Path 3 Hybrid pilot-first resolution): master `e44ed59`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md` (Hybrid pre-flight), `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_solver_findings.md` finding 2 (blocker-effect deferral)

**Status: QC stream — fire now on PR #236. Standalone audit, pre-merge, 8-item amended scope (Path γ' compliance new). ~10-15 min.**
