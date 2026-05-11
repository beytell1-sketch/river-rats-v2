---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat + gto-expert-hat + ml-architect-hat)
re: Phase 2-E.0 — 4-way labeller readiness (labeller brief design + 29-hand calibration set + 5-hand pilot validation per AMENDMENT 3 owner-ratified §6.8); blocks 2-E full labelling pipeline
status: DISPATCH — fire now (Phase 2-D-FULL merged at master a44780f; PR #409 + #411 PASS; 35-hand 4-way reference set complete)
---

# Phase 2-E.0 dispatch — 4-way labeller readiness

## Context

Per AMENDMENT 3 (PR #389) Item 1 + design memo §X + owner-ratified §6.8: the 4-way labelling pipeline must NOT fire until labeller readiness is validated via:
1. 4-way labeller brief design (extends HU brief; adds multiway dimensions)
2. 29-hand calibration set (vs HU's 24-28 hands; +1 axis breadth for 4-way)
3. 5-hand pilot validation with STOP-condition gate
4. Cost-of-failure prevention per FL4 incident lessons (rule-based labelling)

The 35-hand 4-way reference set (PR #409 just merged) is the EVALUATION anchor for the 4-way model post-retrain. The 29-hand calibration set is what LABELLERS USE during the labelling pipeline to anchor their reasoning. They are different.

## Why 2-E.0 exists (FL4 incident background)

Phase 1.5-D.3 HU labelling experienced severe methodology violations:
- FL4 wrote a Python rule-based scoring script (5/5 labels rule-based)
- FL1/2/3/5 used template-based reasoning
- Recovery required explicit anti-rule-based prompt boilerplate (validated by FL6/FL7-10)

**4-way labelling complexity is HIGHER than HU.** Reasons:
- Multiple villain ranges to track (3 villains vs 1 in HU)
- Players-left-to-act logic (per AMENDMENT 1)
- Squeeze-pressure analysis (per AMENDMENT 2)
- Closing-action vs early-action differential
- Pot-cascade dynamics (4-way → 3-way → HU progression within a hand)
- Range-chain narrowing across multiple villains (per `range_narrowing.py` multiway path)

Naive re-use of HU labeller brief will likely produce labels that miss these multiway dimensions. 2-E.0 prevents that BEFORE the full ~750-hand labelling pipeline fires.

## Owner-ratified 2-E.0 scope (per §6.8)

- Insert NEW sub-phase 2-E.0 before 2-E (full pipeline) per design memo §X.5
- Deliverables: 4-way labeller brief + 29-hand calibration set + 5-hand pilot validation
- STOP-condition gate prevents naive HU-style reasoning from cascading to full pipeline

## What Phase 2-E.0 builds

### Task 1 — 4-way labeller brief design

`review/comms/PHASE2E0_4WAY_LABELLER_BRIEF_2026-05-11.md` (or NEW `data/4way_labeller_brief.md` if architect prefers data/ for runtime use):

- Multiway range-chain reasoning: per-villain range narrowing across action history
- Players-left-to-act + squeeze-pressure prompting (AMENDMENT 1 + AMENDMENT 2)
- Closing-action vs early-action decision trees
- **Mandatory anti-rule-based boilerplate** (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + FL6 evidence). Explicit prohibition: NO if/elif rule chains; NO threshold-based ("if hand_rank > X") logic; NO template repetition; NO Python-script-style reasoning. Every label must derive from per-hand poker theory.
- Bucket-first compliance (per `feedback_bucket_first_labelling.md`): bucket assignment FIRST, then action label; NO equity thresholds in labelling prompt (thresholds live in spot_classifier.py)
- Per-hand structure required: pre-flop action context → per-villain range chains → equity/range tensions at decision → action selection + rationale (~250-400 words per hand)
- Solver-aligned bet sizing guidance (per `feedback_solver_aligned_sizing.md`): flop 25%/66%, turn 33%/75%, river 33%/75%/150%
- Terminology compliance (per `feedback_terminology_raise_vs_bet.md`)

### Task 2 — 29-hand calibration set

`data/4way_calibration_29hand_2026-05-11.jsonl` (machine-readable) + `review/comms/PHASE2E0_4WAY_CALIBRATION_SET_2026-05-11.md` (human-readable rationale):

- 29 calibration hands across the 4-way axes (per design memo §X.4 architect-chosen breadth)
- Suggested coverage (architect adjusts):
  - 4-way 3-bet/4-bet pots: ~6 hands
  - Multiway-cooler: ~3 hands
  - Closing-action vs early-action variants: ~5 hands
  - Range-asymmetry: ~5 hands
  - MW-40/45/47 axis representation: ~4 hands (3 axes × 1-2 hands)
  - Standard 4-way SRP IP/OOP: ~6 hands
- These are NOT the same as 35-hand reference set (which is for model evaluation); these are anchors LABELLERS use to ground their reasoning when labelling lookalikes
- Each calibration hand has full GTO label + rationale (250-400 words; same standard as reference set hands)
- Calibration hands should COVER axis space; reference set hands EVALUATE model

### Task 3 — 5-hand pilot validation

Run the proposed labeller brief on 5 sample lookalike hands (NOT the calibration set; NOT the reference set). 5-labeller consensus pattern per design memo §4.3 (if multi-labeller infrastructure already exists) OR single-labeller-with-explicit-anti-rule-prompt for this 2-E.0 pilot validation.

Validation criteria (the GATE):
- All 5 labels produced via gto-expert reasoning (NOT rule-based / threshold / template)
- Per-label rationale ~250-400 words; multiway dimensions explicit (range chains, players-left, squeeze-pressure where relevant)
- Per `feedback_bucket_first_labelling.md`: bucket-first compliance
- No labeller falls back to HU-style reasoning that misses multiway considerations

### Task 4 — Pilot validation report + STOP-condition gate

`review/comms/BUILDER_REPORT_PHASE2E0_LABELLER_PILOT_2026-05-11.md` covering:
- Labeller brief evolution from HU to 4-way (delta documentation)
- 29-hand calibration set summary (axis breakdown)
- 5-hand pilot results: each label + reasoning quality assessment
- Gate verdict:

| Outcome | Action |
|---------|--------|
| 5/5 hands clear (anti-rule-based + multiway-aware) | PROCEED to 2-E full labelling pipeline |
| 3-4/5 clear (mixed signal) | REPORT; orchestrator triages (brief revision vs proceed-with-caution) |
| <3/5 clear (broad fail; naive HU-style or rule-based drift) | HALT 2-E; REPORT; brief design needs deeper iteration |

## What Phase 2-E.0 does NOT do

Per design memo §X.5 + §7 + AMENDMENT 3 + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT execute the full ~750-hand labelling pipeline (that's 2-E scope; gates on 2-E.0 PASS)
- ❌ Does NOT touch `feature_extractor.py` (surface 61 frozen)
- ❌ Does NOT touch `oracle_router.py` (2-H scope)
- ❌ Does NOT generate lookalikes (2-E corpus scope)
- ❌ Does NOT retrain (2-F / 2-G)
- ❌ Does NOT touch model artifacts
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4)
- ❌ Does NOT change the 35-hand reference set (frozen from PR #409 merge)

## STOP conditions (per CLAUDE.md §5)

- 4-way labeller brief design requires spike (e.g., new infrastructure for multiway range-chain capture) → STOP / REPORT
- 29 calibration hands can't be sourced (e.g., 4-way 4-bet pots too rare) → REPORT; orchestrator may amend with reduced count
- 5-hand pilot validation shows ALL 5 labels rule-based/template (mirrors FL4 incident) → STOP; brief design has fundamental gap
- ≥3 of 5 pilot labels need owner-arb adjudication → SURFACE batch comm; do not unilaterally pick
- Wall-clock blows past ~12h (memo estimate 6-10h × 30% buffer) → REPORT
- TC-23 EXISTENCE: labeller brief + calibration JSONL + pilot report git-tracked

## QC stream — what you audit (pre-merge milestone)

Per `feedback_qc_required_before_approval.md`:

1. **Diff scope**: labeller brief + calibration JSONL + calibration rationale + pilot report; NO river-rats-core/ / oracle_router / model / lookalike corpus generation edits
2. **Labeller brief content**: multiway range-chain reasoning explicit; players-left + squeeze-pressure prompts present; anti-rule-based boilerplate explicit; bucket-first compliance preserved; terminology + bet sizing solver-aligned
3. **Calibration set**: 29 hands; axis coverage spans 4-way 3-bet/4-bet + multiway-cooler + closing-action + range-asymmetry + MW-40/45/47 + SRP; per-hand 250-400 word rationale; non-overlapping with 35-hand reference set
4. **Pilot validation**: 5 hands with full labels; gto-expert reasoning chains visible; NO rule-based/template/threshold patterns
5. **STOP-condition gate evidence**: 5/5 pass evidence (or partial/fail with explicit categorization)
6. **TC-X-DISPATCH-COMPLIANCE**: all 4 task deliverables present; no scope leak
7. **FL4-incident comparison**: pilot labels DON'T resemble FL4's rule-based pattern; explicit anti-rule-based attestation

QC routing: standalone per `feedback_qc_routing_when_standalone_active.md`. Output:
- `~/river-rats-qc/findings/2026-05-11-pr<N>-phase2e0.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2E0_LABELLER_READINESS_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- Builder Phase 2-E.0 PR → QC trigger when pushed
- On QC PASS + 5/5 pilot gate cleared → orchestrator merges + dispatches 2-E (full ~750-hand labelling pipeline)
- On QC PASS + 3-4/5 partial → orchestrator triages; may surface to owner
- On QC PASS + <3/5 fail → HALT 2-E; REPORT for brief revision
- On QC SHOULD_FIX-substantive → amend + re-fire
- On QC BLOCKER → hold + redo
- STOP condition → REPORT; orchestrator triages

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a44780f` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-D-FULL builder PR: master `b669541` (PR #409)
- Phase 2-D-FULL QC PASS: master `a44780f` (PR #411)
- Phase 2-D pilot builder: master `3509679` (PR #405) + QC PASS `e518028` (PR #407)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- AMENDMENT 3 (labeller readiness + 5-way scope): master `3763d8a` (PR #389)
- Design memo §X (labeller readiness): `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` lines 384-443
- Design memo §6.8 (owner-ratified labeller readiness scope): lines 640-644
- HU labelling FL4 incident: `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- HU labeller brief (analog template): `data/hu_corpus/full_HU2_HU6/labeller_brief.md` (or equivalent; architect locates)
- 35-hand 4-way reference set (evaluation anchor): `data/4way_reference_35hand_2026-05-11.jsonl`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_qc_required_before_approval.md`, `feedback_attention_flags_when_features_change.md`

**Status: Phase 2-E.0 dispatch — 4-way labeller readiness per AMENDMENT 3 owner-ratified §6.8. Builds 4-way labeller brief + 29-hand calibration set + 5-hand pilot validation. STOP-condition gate prevents naive HU-style reasoning cascading to full ~750-hand pipeline. FL4-incident lessons explicit. Architect estimate ~6-10h. After 2-E.0 QC PASS + 5/5 gate clear → 2-E full labelling pipeline dispatch.**
