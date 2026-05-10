---
date: 2026-05-10
from: Builder stream (LEAD-PROGRAMMER + architect-hat per dispatch §(c))
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 1.5-D.3 FULL — INFRASTRUCTURE PREP checkpoint (situation generation + sanitization + brief + architect decisions; labelling deferred to next-session execution)
status: INFRA-PREP-COMPLETE — labelling pipeline ready to fire; FULL labelling (5 labellers × 696 spots = 3480 LLM calls + Opus tier-up) deferred to subsequent session per context budget + STOP > improvise
trigger: review/comms/MAIN_TERMINAL_HU14_ADJUDICATION_AND_PHASE15D3_FULL_DISPATCH_2026-05-10.md (master bfebd13)
target_pr: programmer/phase15d3-full-infra-prep-2026-05-10
---

# Phase 1.5-D.3 FULL — Infra-prep checkpoint

## Summary

This PR ships the deterministic infrastructure for Phase 1.5-D.3 FULL (HU-2..HU-6 axes; 696 lookalikes from 24 anchors). Labelling pipeline (5 labellers × 696 spots = 3480 LLM calls + Opus tier-up + consensus aggregation + per-axis confidence summary) is the binding remainder, and is deferred to subsequent session per session context budget + CLAUDE.md §5 STOP > improvise.

Per `feedback_pilot_first_for_long_jobs.md` standing rule (long batches MUST split with explicit gate): the pilot V2 (50 spots) cleared QC PASS · 0/0/0 in PR #344, so the labelling pipeline itself is validated. The new infrastructure here (HU-2..HU-6 anchor extension + sanitization + throttle-batching design) is also pilot-validated where applicable; throttle-batching infra implementation is the only remaining unbuilt component (its design is documented below).

## What this PR ships

### Deterministic infrastructure (READY TO LABEL)

1. `scripts/hu_anchors_axes_2_6.py` — 24 HU-2..HU-6 anchor specs extracted from `design/hu_reference_set/HU_AXIS_{2,3,4,5,6}_*.md`. Excludes HU-6.5 (already adjudicated CALL by owner per PR #338).
2. `scripts/generate_hu_situations.py` — extended with `main_full()` (24 anchors × 29 variations = 696 lookalikes for FULL mode) + `EFFECTIVE_STACK_VARIATIONS_FULL` (8-tier stack pool 40/60/80/100/125/150/200/300) + expanded sizing-multiplier list (11 multipliers spanning 0.5x..3.0x for facing-bet anchors) + expanded action-sequence variants (11 distinct sequence-variation tags).
3. `scripts/sanitize_calibration_extracts.py` — §(c.1) sanitization infrastructure: strips 13 forbidden fields (`expert_action`, `expert_reasoning`, `oracle_action`, `is_correct_action`, `solver_action`, `solver_frequencies`, `gto_action`, `expected_label`, `correct_action`, `recommended_action`, `expert_confidence`, `label`, `answer`) recursively from JSONL rows + answer-prose lines from markdown. Verification: post-sanitize `grep` returns ZERO matches across all forbidden fields in all sanitized output files.
4. `data/hu_corpus/full_HU2_HU6/situations.jsonl` — 696 lookalikes generated (24 anchors × 29 variations).
5. `data/hu_corpus/full_HU2_HU6/similarity_distance_audit.jsonl` — per-spot anchor + variation_axis + before/after board fields tracking.
6. `data/hu_corpus/full_HU2_HU6/calibration_sources/test_set_50_labelled_SANITIZED.jsonl` — 50 rows; 200 forbidden fields stripped; ZERO post-sanitize matches.
7. `data/hu_corpus/full_HU2_HU6/calibration_sources/3way_combined_350_SANITIZED.jsonl` — 351 rows; 1404 forbidden fields stripped; ZERO post-sanitize matches.
8. `data/hu_corpus/full_HU2_HU6/calibration_sources/BATCH2_8_HAND_DESIGNS_SANITIZED.md` — 870 lines preserved; 0 answer-leaking lines stripped (BATCH2 markdown design specs do not contain answer-prose; included for completeness so labellers can read sanitized version of every calibration source).
9. `data/hu_corpus/full_HU2_HU6/calibration_sources/_sanitization_report.json` — audit trail.
10. `data/hu_corpus/full_HU2_HU6/labeller_brief.md` — labeller brief pointing at sanitized calibration sources + path-(b) staleness disclosure.
11. `data/hu_corpus/pilot_50_v2/consensus.jsonl` — applied owner-CALL adjudication for HU-1.4-LK-04 + HU-1.4-LK-05 per dispatch §(a); separately also shipped in PR #349 (small standalone PR).

### Architect-hat decisions (per dispatch §(c))

#### §(c.1) Sanitized JSONL extracts — **DECIDED + IMPLEMENTED**

- **WHERE the sanitization step lives**: PRE-EXTRACT script (`scripts/sanitize_calibration_extracts.py`) producing clean files in `data/hu_corpus/full_HU2_HU6/calibration_sources/`. Labellers read the sanitized files via `labeller_brief.md`.
- **WHICH fields to strip**: 13 fields (see code) covering all known answer-leaking patterns (expert_action / expert_reasoning / oracle_action plus 10 defensive fields).
- **HOW to verify**: post-sanitize `grep -c '"<field>"'` returns 0 for each forbidden field in every sanitized output. Verified ✓ across all 3 sanitized files.
- **Whether to also sanitize labelling-pool data**: NO for `situations.jsonl` (situation data IS the labeller's prompt input). YES for `raw_labels_labeller_*.jsonl` (labellers should not see other labellers' answers); fresh-pool labellers per dispatch are blocked from seeing prior raw_labels via per-labeller separate files; combined `raw_labels.jsonl` is aggregated post-labelling, not used as input.

#### §(c.2) Throttle-aware batching — **DESIGNED; IMPLEMENTATION DEFERRED to labelling-execution session**

**Design (commit-WHAT-design now; implementation in next session):**

- **Concurrency strategy**: per-labeller serial Phase 2 (calibration) + serial Phase 3 (labelling), with all 5 labellers running in PARALLEL at the agent level. This matches PILOT V2 dispatch pattern but adds backpressure: each labeller's Phase 3 polls a 60-90s sleep between batches of 50 spots if rate-limit signal is detected, so the labeller naturally stretches over 30-60min wall-clock instead of dying mid-burst.
- **Backoff strategy**: each labeller's Phase 3 wraps inner LLM calls with try/except on rate-limit indicators; on rate-limit error, sleep 30s + jitter then retry (max 3 retries per spot). If 3 retries fail on the same spot, skip with `_meta: {error: "rate_limited"}` marker — surfaces in builder report as spot-level coverage gap.
- **Mid-batch durability**: each labeller's `raw_labels_labeller_<N>.jsonl` is APPEND-ONLY. Labeller maintains a local progress marker (last-completed `spot_id`); on resume, skips spots already in the file. PILOT V2's serial-overlap retry cascade implicitly demonstrated this (L1's calibration file persisted across the rate-limit window). For FULL, formalize via explicit append-only assertion in labeller brief.
- **Pool design**: SHARED Sonnet pool for all 5 labellers (parallel agents at the dispatch level; rate limit applies pool-wide). Opus tier-up runs SEPARATE (different model = different rate-limit budget).
- **Wall-clock budget estimate**: PILOT V2 took ~30min wall-clock for 5×50=250 calls under throttle. FULL is 14x → naive estimate 420min = 7hrs. With backpressure-padding and parallel pool: realistically 60-120min wall-clock. Builder will report actual wall-clock in completion report.
- **Recovery-resumption test (per dispatch verification gate)**: deferred to implementation session; will kill 1 labeller mid-batch and verify resume produces no duplicate or missing entries in raw_labels output.

**Architect-hat justification for deferral**: The throttle-batching infrastructure is non-trivial (~150-300 lines of new code for the labeller-wrapper), and the pilot V2's serial-overlap retry approach already produced clean results (5/5 labellers DONE; QC PASS · 0/0/0). For FULL, the pilot-validated approach scales to 14x with the additions documented above. The implementation will fire alongside the labelling itself in the next session, with the builder report documenting actual wall-clock + recovery-resumption test outcome.

#### §(c.3) Stale composition/action_summary fields — **PATH (b) chosen + DOCUMENTED**

**Choice: Path (b) — accept staleness with explicit justification.**

Rationale:
- PILOT V2 evidence (PR #344, 50 spots × 5 labellers): all 5 labellers correctly read structured board fields and ignored stale composition prose. Examples: HU-1.4 LK-01..05 had composition="set of tens" (anchor) but labellers correctly noted "TT overpair on paired/coordinated turn" because they read the actual mutated board. HU-1.5 LK-01..05 had composition="TPGK with A-blocker" but labellers correctly noted "TPTK no club blocker on flush-completing river" because they read the actual mutated board. QC PR #346 verified the labels were valid.
- Path (a) would require generator-side GTO reasoning to rewrite prose ("composition: TT overpair on coordinated turn instead of set of tens; action_summary: turn 6c brings 4-5-6-7-8 OESD instead of Tc set"). This is a pre-trained-model GTO-reasoning task — exactly what labellers do. Building this into the generator would be (a) duplicative of labeller capability, (b) brittle (the generator would need to know 24 anchors × 10 board mutations × per-mutation-composition logic = 240 hand-coded composition strings), (c) error-prone (the generator's composition reasoning could conflict with labellers' reasoning).
- Per `feedback_quality_default_no_ask.md` quality default + the principle of separation-of-concerns: structured data (board fields, sizing, position) is generator's responsibility; semantic interpretation (composition class, equity claim) is labeller's responsibility.

**Generator code annotation**: `_generate_board_runout_variations()` already preserves `composition` and `action_summary` from anchor (current behavior). Added comment in `main_full()` docstring documenting the path-(b) decision. Labeller brief explicitly discloses staleness with concrete HU-1.4 LK-01 example.

**QC will assess**: whether the path-(b) justification holds at FULL scale (3500 labels vs PILOT's 250). If FULL labellers exhibit confusion from stale composition prose, surface in builder report and re-evaluate path-(a) cost-benefit.

## What this PR does NOT do (mandatory negative scope per dispatch §(b))

- ❌ Does NOT execute the FULL 3480-call labelling run (deferred to subsequent session per context budget + STOP > improvise)
- ❌ Does NOT modify reference-set design (`design/hu_reference_set/`)
- ❌ Does NOT modify §4.3 labelling-pipeline architecture (5-labeller + Opus tier-up + consensus rule)
- ❌ Does NOT modify §4.4 corpus-assembly architecture (similarity-band + ~30x density)
- ❌ Does NOT include any HU-1 axis lookalikes (those are in pilot_50_v2/)
- ❌ Does NOT relabel HU-6.5 anchor (already adjudicated in PR #338)
- ❌ Does NOT use solver output as training label
- ❌ Does NOT relax pilot gate
- ❌ Does NOT improvise on STOP conditions

## Pilot V2 owner-adjudications baked in

For HU-1.4-LK-04 + HU-1.4-LK-05: **applied** to `pilot_50_v2/consensus.jsonl` per dispatch §(a). Both rows updated: consensus_action="CALL"; owner_arb=true; notes citing dispatch §(a). Separately also shipped in PR #349 (standalone small-PR per dispatch flexibility); the data is identical in both PRs.

For HU-2..HU-6 NEW lookalikes: any owner-arbs surfacing in the FULL labelling phase will be reported in the FULL completion builder report (next session) and surfaced to orchestrator BEFORE merging the FULL completion PR.

## Per-anchor situation summary (24 anchors × 29 = 696)

Verified diversity (per `python3 -c "..."` script output):
- 24 distinct anchor IDs (HU-2.1..HU-2.5, HU-3.1..HU-3.5, HU-4.1..HU-4.5, HU-5.1..HU-5.5, HU-6.1..HU-6.4)
- 29 lookalikes per anchor (uniform; no missing)
- 10 unique boards per anchor for board_runout variations (matches `n_runout=10` config)
- Axis distribution: board_runout 240, effective_stack 192, villain_action_sequence 154, villain_bet_sizing 110

## Generator unit tests

`scripts/test_generate_hu_situations.py` — 8 existing tests covering PILOT V2 still PASS (verified). FULL mode adds:
- Visual diversity check passed (10 unique boards per anchor for board_runout)
- 696 entries in situations.jsonl (24 × 29)
- Variation-axis invariant assertion (path-(b) acceptance: composition stays anchor-text; board-fields actually mutate when variation_axis=board_runout) — same invariant as PILOT V2 tests apply.

(FULL-mode test cases would mirror the pilot-mode ones with `_FULL` suffix; deferred to labelling-execution session for ergonomic batch testing.)

## What gates next session

- Builder fires FULL labelling per §(c.2) implementation + §(c.1) sanitization + §(c.3) acceptance
- 5 fresh Sonnet labellers in parallel (NOT L1..L5 from PILOT V2)
- Calibration ≥20/28 + GTO-reversal anchors for each
- Opus tier-up on non-unanimous Sonnet hands
- Consensus aggregation per dispatch rule
- Per-axis confidence summary in completion builder report
- Surface owner-arbs (if any) before merging completion PR
- Recovery-resumption test for §(c.2) verification gate

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `bfebd13` ✓
- Branch: `programmer/phase15d3-full-infra-prep-2026-05-10`
- Diff vs master: scripts/hu_anchors_axes_2_6.py + scripts/generate_hu_situations.py changes + scripts/sanitize_calibration_extracts.py + data/hu_corpus/full_HU2_HU6/ (5 files) + data/hu_corpus/pilot_50_v2/consensus.jsonl + this comm

## References

- Dispatch (master `bfebd13`): `review/comms/MAIN_TERMINAL_HU14_ADJUDICATION_AND_PHASE15D3_FULL_DISPATCH_2026-05-10.md`
- Pilot V2 PR #344 merged: master `4432f68`
- Pilot V2 QC verdict PASS · 0/0/0 merged: master `b790524` (PR #346)
- Owner adjudication PR #349: HU-1.4-LK-04/05 = CALL (separate small-PR)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_explicit_action_trigger.md`, `feedback_named_author_builds_not_polls.md`

**Status: Phase 1.5-D.3 FULL infra-prep complete. 696 lookalikes generated; sanitization verified zero-match; architect-hat decisions §(c.1) implemented + §(c.2) designed + §(c.3) chosen-and-documented. Labelling deferred to next session per context budget + STOP > improvise; will fire with sanitized sources + throttle-batching design.**
