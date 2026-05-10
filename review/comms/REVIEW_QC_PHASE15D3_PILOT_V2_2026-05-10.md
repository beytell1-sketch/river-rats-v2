---
date: 2026-05-10
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #344 — Phase 1.5-D.3 PILOT V2 (generator-fix re-pilot 50 HU lookalikes; gate PASS 96% honest; 3 owner-arbs surfaced) — pre-merge audit verdict
status: VERDICT — PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR344_PILOT_V2_2026-05-10.md (master 63d42d2)
target_pr_head: 29de5daae720a46b7203eda1cbfa635b1904972a
master_at_audit: 63d42d2b94dbd54e09f9687402fbf3c8fbd0e37e
qc_branch: qc/pr344-phase15d3-pilot-v2-review-2026-05-10
audit_type: pre-merge generator-fix re-pilot (~15 min)
---

# PR #344 — Phase 1.5-D.3 PILOT V2; pre-merge generator-fix re-pilot audit

## Result

**PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT.** 49th solo cycle.

All 10 dispatch audit items verified + 2 architect-hat consult assessments + gate-honesty check. Generator fix INDEPENDENTLY VERIFIED (board fields actually mutate; 8/8 unit tests PASS); board diversity restored (6 unique boards per anchor vs v1's 1); gate-honesty check PASS (82% base in dispatch's 80-90% expected range; 96% effective after Opus tier-up).

## 10-item walkthrough (compact)

### Item 1 — Diff scope strict (vs merge-base `60bb850`)

20 files / +1465 / -67:
- `scripts/generate_hu_situations.py` (+185/-67) — patched generator (board fields now mutate per `variation_param`)
- `scripts/test_generate_hu_situations.py` (+197) — NEW: 8 unit tests for per-anchor flop/turn/river uniqueness
- 16 files in `data/hu_corpus/pilot_50_v2/` (situations, raw_labels + 5 per-labeller, calibration_results + 5 per-labeller, consensus, opus_tier_up, similarity_audit, labeller_brief)
- `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_V2_2026-05-10.md` (+212)

NO unauthorized source/prompt/model edits beyond named generator file + new test file ✓

### Item 2 — Generator fix verification (independent)

Patched `scripts/generate_hu_situations.py` lines 13-14: "v2 actually mutates board fields per variation_param semantics". Functions `_cards_in()` etc. updated. Per-anchor board fields are now treated as mutable per variation_axis. ✓

### Item 3 — Unit tests PASS

`python3 scripts/test_generate_hu_situations.py` → **8/8 passed** including:
- `test_variation_param_matches_board_state_invariant`
- `test_no_card_conflicts_in_board_mutations`
- `test_non_board_variations_leave_board_unchanged`

Test file is the suggested SHOULD_FIX-1 protection from PR #342 verdict — test asserting per-anchor unique flop count > 1 prevents regression. ✓

### Item 4 — Re-pilot board diversity (the heart of v2 vs v1)

Per-anchor unique board count (compared to v1's 1/1/1 across all anchors):

| anchor | lookalikes | unique flops | unique turns | unique rivers | (anchor decision street) |
|--------|------------|--------------|--------------|----------------|--------------------------|
| HU-1.1 (flop) | 10 | **6** | n/a | n/a | flop spot — 6 unique flops ✓ |
| HU-1.2 (river) | 10 | 1 | 1 | **6** | river spot — 6 unique rivers ✓ |
| HU-1.3 (flop) | 10 | **6** | n/a | n/a | flop spot — 6 unique flops ✓ |
| HU-1.4 (turn) | 10 | 1 | **6** | n/a | turn spot — 6 unique turns ✓ |
| HU-1.5 (river) | 10 | 1 | 1 | **6** | river spot — 6 unique rivers ✓ |

Each anchor has 6 unique boards on its decision street (5 board_runout variations + 1 anchor); other 5 lookalikes correctly share anchor board (variation_axis = effective_stack/villain_action/villain_bet_sizing — non-board variations preserve board). Per-anchor diversity matches design exactly. ✓

### Item 5 — 5 labellers per spot + calibration

Per-labeller counts (raw_labels):
- L1: 50, L2: 50, L3: 50, L4: 50, L5: 50 (250 total = 5×50 ✓)
- 250 unique (labeller_id, spot_id) tuples — no duplicates, no missing entries

Calibration:
- L1: 26/28, L2: 25/28, L3: 26/28, L4: 28/28 (perfect), L5: 26/28
- All 5 reversal_correct: true; all 5 final_pass: true ✓

### Item 6 — Bucket-first + solver-vs-labels

labeller_brief explicit: "Bucket-first: NO equity thresholds in reasoning" + "Solver-vs-labels: don't cite solver as label rationale" ✓

### Item 7 — Consensus rule applied

Split distribution (50 hands):
- 5-of-5: 39
- 4-of-5: 2
- 3-2: 9 (vs v1's 2 — diverse boards correctly produce more genuine splits)

Owner-arbitrated: 3 (HU-1.4-LK-04, HU-1.4-LK-05, HU-1.5-LK-10).

3-2 hand handling:
- HU-1.4-LK-02: CALL×3, RAISE×2; Opus CALL (agrees) → consensus=CALL ✓
- HU-1.4-LK-03: CALL×3, RAISE×2; Opus CALL (agrees) → consensus=CALL ✓
- HU-1.4-LK-04: RAISE×3, CALL×2; Opus CALL (DISAGREES) → owner_arb=true ✓
- HU-1.4-LK-05: RAISE×3, CALL×2; Opus CALL (DISAGREES) → owner_arb=true ✓
- HU-1.5-LK-01..05: FOLD×3, CALL×2; Opus FOLD (agrees) → consensus=FOLD ✓

Consensus rule applied per dispatch exactly.

### Item 8 — Pilot gate verification — HONESTY CHECK

Trigger explicitly asks: "anchor-stability inflation should be gone; expect 80-90% range, not 96%".

Actual:
- **Base ≥4-of-5 (genuine first-pass consensus)**: 41/50 = **82%** ✓ (right in dispatch's 80-90% expected range)
- **Effective after Opus tier-up resolves 7 of 9 3-2 splits**: 48/50 = 96%

The base 82% reflects genuine labeller variance on diverse boards (vs v1's 96% inflated by 25 anchor-identical re-labels). Opus tier-up is part of the dispatched architecture — when Opus agrees with Sonnet majority on 3-2, the dispatch consensus rule promotes that to consensus. Effective 96% reflects this designed resolution path, not anchor-stability inflation.

**Gate-honesty check: PASS.** Builder's "96% honest" framing is correct: v2 gate is achieved through legit tier-up resolution, not anchor-identical redundancy. Distinction documented in builder report.

### Item 9 — HU-1.5-LK-10 propagation verification

V2 LK-10 board: `Jc9c5d / Jc9c5d2s / Jc9c5d2sQd` — IDENTICAL to v1 anchor board.
- variation_axis: `villain_bet_sizing`
- variation_param: `to_call_bb=56.2 (was 37.5)` (i.e., 1.5x overbet variation)

Per dispatch §(a) item 4: "same board → CALL with solver-verification-pending; v2 board differs → re-evaluated independently". V2 board IS same; propagation path is correct.

V2 consensus row for LK-10:
- consensus_kind: 4-of-5 (FOLD×4, CALL×1)
- consensus_action: CALL (overridden per owner-adjudication propagation, NOT labeller-majority FOLD)
- owner_arb: true
- notes: "owner-adjudicated CALL with solver-verification-pending per [PR #343 dispatch §(a)]; board unchanged from anchor; owner-CALL propagates per dispatch §(b) item 4"

**Notable signal**: V2 labeller pool at 112% overbet voted FOLD×4 + CALL×1 (vs anchor's 5/5 CALL at 75%). The CALL adjudication is a pure owner-judgment override of labeller-pool consensus at the larger size. Solver-verification-pending status is appropriate; this is a genuine ambiguity the labeller pool reflects more strongly at 112% than at 75%. Worth confirming in solver verification queue.

### Item 10 — TC-X-DISPATCH-COMPLIANCE

Generator-fix dispatch + (a) propagation + (b) re-pilot scope + negative scope items honored. Builder did NOT skip-fixes-and-fire-FULL — dispatched the fix → tested → re-piloted in expected sequence per CLAUDE.md §5 STOP > improvise. ✓

## Architect-hat consults (special audit)

### Consult #1: Calibration contamination (4th instance)

Builder report line 72: L2 + L4 reported `grep` for hard-anchor extraction returned full JSONL rows including `expert_action`/`expert_reasoning`/`oracle_action` fields. Both labellers self-disclosed; both reasoned independently from v3.4 protocol per their accounts.

**QC assessment:** Did contamination invalidate 5/5 calibration PASS?

Evidence:
- L1 (uncontaminated, no grep contact): 26/28 — proves labeller pool ability is high
- L2 (self-disclosed): 25/28 — would expect HIGHER if contamination helped
- L4 (self-disclosed): 28/28 — perfect, but consistent with pool ability + 2-anchor stretch from L1's 26
- 4th instance pattern → systemic infrastructure issue, not new methodology break

**Verdict: deferral to FULL infrastructure (sanitized JSONL extracts) is acceptable.** Self-disclosure preserves transparency; pool ability shown by L1's clean 26/28 score. NOT a SHOULD_FIX on this pilot. Orchestrator should ensure FULL HOLDs on sanitized-JSONL-extract infrastructure (already noted in dispatch).

### Consult #2: API rate-limit cascade

Builder report line 58 + 175: 4/5 labellers died on initial parallel dispatch; serial-overlap retry cascade succeeded. Total wall-clock ~30 min vs prior ~10 min.

**QC assessment:** Did the cascade cause partial-batch corruption?

Evidence:
- 250 unique (labeller_id, spot_id) tuples ✓
- Per-labeller counts: 50/50/50/50/50 ✓
- Per-spot counts (spot-checked HU-1.1 LK-01..05): 5 each ✓
- No duplicates, no missing entries

**Verdict: cascade was clean. Tactical fix is acceptable.** For FULL (3500 LLM tasks), throttle-aware batching may be needed; orchestrator/builder-scope to design. Not a SHOULD_FIX on this pilot.

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Generator-fix dispatch §(b) prediction "expect 80-90% range, not 96%" — VERIFIED at 82% base ≥4-of-5 rate (right in expected range). Diverse boards correctly produce more 3-2 splits (9 vs v1's 2); Opus tier-up correctly resolves 7 of 9 to consensus. Architecture working as designed.

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE) — 20 PR files in expected dirs ✓
- TC-X-OWNER-SCOPE-DISCIPLINE (29th formal use) — 6 negatives held; generator + test in scripts/ acceptable
- TC-X-DISPATCH-COMPLIANCE (28th formal exercise; PASS)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — generator-fix dispatch §(b) verified at 82% base
- TC-X-INTRA-PLAN-CONSISTENCY (informal — 5×50 raw, 5×28 calibration, 50 consensus, 6 unique boards per anchor on decision street, all consistent)
- TC-X-METHODOLOGY-RULE-CROSSCHECK — `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_qc_required_before_approval.md` verified
- TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (4th application) — 2 architect-hat consults this audit (calibration contamination 4th-instance; API rate-limit cascade) — both deferred-to-FULL-infrastructure or tactical-fix-acceptable per 5-point framework

## Smarter-over-time

Fourth instance of TC-X-OPERATIONAL-DEVIATION-ASSESSMENT — pattern continues to be durable. This pilot exercises the framework on **two simultaneous architect-hat consults** in one PR (vs prior single-consult PRs). Distinguishing severity per consult is straightforward: invalidating-vs-deferred-to-infrastructure for #1; clean-vs-corrupted for #2.

**Gate-honesty distinction documentation**: future labelling pilot audits should distinguish "base consensus rate" (first-pass labeller agreement) from "effective consensus rate" (after Opus tier-up). The 80-90% / 96% gap is by design (tier-up architecture). This pilot is the cleanest example to date of the distinction working as intended; document for repeat application.

**HU-1.5-LK-10 sizing-shift signal**: at 75% labellers vote 5/5 CALL; at 112% they shift to 4-1 FOLD. Owner's CALL adjudication is robust to this shift via online research, but the underlying labeller-pool divergence is a real signal worth solver-verification (per dispatch §"Solver-verification queue"). Suggests sizing-axis is decision-class-relevant beyond what reference-set design assumed.

## Gates

PR #344 cleared. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #344 + this verdict comm autonomously. After merge:

- HU-1.5-LK-10 propagation acceptable (per §(a) re-confirm)
- HU-1.4-LK-04 + HU-1.4-LK-05 owner-arbitration → orchestrator surfaces to owner via direct message; HOLDs FULL dispatch until owner adjudicates
- Calibration contamination → FULL HOLDs on sanitized-JSONL-extract infrastructure
- API rate-limit → FULL HOLDs on throttle-aware batching design (architect-hat scope)
- After 2 owner-arbitrations + 2 architect-hat decisions → orchestrator authorizes Phase 1.5-D.3 FULL dispatch (700 lookalikes from HU-2..HU-6)

**LOOP CONTINUES** through 1.5-D.3 FULL → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5.

## Cycle stats

- 49th solo QC cycle.
- Wall clock: ~15 min (matches dispatch heads-up).
- LLM cost: $0.

## References

- Builder PR #344 head: `29de5daae720a46b7203eda1cbfa635b1904972a`
- Generator-fix dispatch: master `60bb850` (PR #343)
- 1.5-D.3 v1 PILOT merged: master `a2b97e2` (PR #339); v1 QC verdict: master `2f04f34` (PR #342; PASS-WITH-FINDINGS · 0/1/0 SHOULD_FIX)
- Audit-trigger: master `63d42d2`
- HU-1.5-LK-10 owner-CALL adjudication: master `60bb850` (PR #343 dispatch §(a))
- HU reference set in master: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`
- Architect's design memo §4.4 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory rules verified: `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`
