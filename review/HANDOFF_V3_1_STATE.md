# Handoff: v3.1 Rebuild State

**Date:** 9 April 2026
**Session 2:** Decision tree fix, factory brief, diversity audit, board allocation
**Previous session:** Data integrity rebuild, feature upgrade, relabelling

---

## Current state

### What's DONE:
- Phase 0: RAISE validation (all 7 non-monster RAISEs NOT DEFENSIBLE from 48 features)
- Phase 1: Action sequence audit (24 CRITICAL, 10 MODERATE, 12 CLEAN)
- Phase 2: Reference set audit (39/40 correct, MW-42 fixed)
- Phase 3: Feature pipeline upgrade (48→52 features, flush_block_pct bug fixed, action validator added)
- Phase 4: Factory rebuild (46/46 boards CLEAN, both scripts regenerated)
- Phase 5: Labelling (406 situations labelled with simplified RAISE rule)
- Phase 5 review: 95.8% agreement, 5 corrections applied (3 over-fold, 2 RAISE violations)
- **RAISE research:** 28 sources (Research A) + 52-feature analysis (Research B) — complete
- **RAISE decision tree v2:** All 14 review findings addressed, independently reviewed, APPROVED
- **Self-play RAISE count:** 37/200 (18.5%) in selected subset, 37/962 (3.8%) in full set
- **Factory brief v2.1:** 151 situations (109 RAISE + 42 CALL), distribution targets met
- **Factory diversity audit:** 7 mandatory requirements (R1-R7), 14-point reviewer checklist
- **Fixed-stack research:** SPR variance in new batch supported by evidence; R3 stands
- **Board allocation FINAL:** 33 boards (B01-B33), 151 situations allocated to 10 sub-patterns
  - 3 review cycles: v1 (6 villain_positions errors + SP2 table), v2 (B22/SP7/B20 verifications), FINAL (B27 fix + B33 for S2)
  - All R1-R7 compliant (turn 45% vs 43% ceiling and 8.0+ SPR at 14% vs 15% floor documented as acceptable)
  - Factory brief v2.1 APPROVED by owner

### What's IN PROGRESS:
- BET-context factory batch 4 (~80-100 situations) needed before labelling

### What's DONE (this session continued):
- **Step 5 Phase B:** 4 design agents assigned hero hands (151 situations, 0 card conflicts)
- **Step 5 Phase C:** Review found 2 blockers (flush_block_pct redundancy, S4 boundary), both fixed
- **Step 6:** Factory generation — 151 rows in factory_batch3_situations.jsonl (150 clean, 1 SUSPICIOUS)
- **Finding:** flush_block_pct > 0 is structurally redundant when flush_draw_rank >= 12 (documented)
- **B23 correction:** SB folded on turn, villain_positions fixed to ['BB'] (same pattern as B25/B26/B27)
- **38 action history fixes** across 9 boards (missing player checks on postflop streets)
- **Calibration gate PASSED:** 24/24 (100%), all 3 reversals correct, MW-30 key updated to CALL
- **Feature 53 added:** is_preflop_aggressor (binary), all 3 batches regenerated with 53 features
- **Owner-identified gap:** PFA c-bet bluff scenario not distinguishable from defender bluff without feature 53
- **Labelling approach:** deterministic tree script + LLM reviewer sample (not 57 LLM agents)
- **C-bet research complete:** 5 research agents + 3 reviewers, all PASS
- **BET decision tree v1:** 7 steps, recalibrated thresholds (connectivity_score + high_card_rank)
- **FOLD decision tree v1:** 5 steps, reviewed PASS
- **Deterministic labelling script:** written, caught threshold mismatches, re-run confirmed
- **BET data gap found:** factory has 95% OOP in BET situations, 0 IP PFA. Need batch 4.
- **Owner decision:** Option A — design ~80-100 BET-context situations before labelling
- Step 6: Generate through factory with 52 features + action validator
- **Batch 4 factory brief** — design ~80-100 BET-context situations
  Categories: IP PFA value (30+), OOP PFA value (15+), PFA semi-bluff (20+),
  IP thin value non-PFA (15+), OOP value exception (10+), CHECK counterexamples (10+)
  Position: 55-65% IP. PFA: 65-75%. villain_aggr must include 0 values.
  See review/comms/BET_FACTORY_PLAN_2026-04-09.md for full spec.
- **Batch 4 board allocation + hero hands + generation**
- ~~Phase B: C-bet research~~ DONE (5 research agents + 3 reviewers)
  Per §1.1: 1 topic per research agent. 5 subtopics:
    Agent R1: 3-way c-bet frequency (PFA vs defender, by position)
    Agent R2: Board texture effects on c-betting (dry/wet/paired/connected)
    Agent R3: Multiway c-bet sizing and SPR interaction
    Agent R4: When to check back (PFA give-up conditions, trap lines)
    Agent R5: Blocker effects on c-bet profitability (flush/straight blockers)
  3 reviewers (§1.2: reviewer count ≥ researcher count ÷ 2 = 2.5, round up to 3)
  Owner's starting observations: PFA on dry board can bluff; PFA on wet
  board vs 2 opponents without outs/blockers can't; with outs or blocker
  can. These are starting points for research, not directives.
- **Phase C: BET decision tree** (like RAISE tree but for BET/CHECK)
  Must use feature 53. GTO Expert synthesises, independent review, owner
  approval.
- **Phase D: Updated calibration** (53-feature situations, KB c-bet section)
- **Step 7: Label ALL 563 situations** with deterministic script applying
  BOTH trees (RAISE tree for facing-bet, BET tree for not-facing-bet).
  LLM reviewer sample (~60 situations) checks both applications.
  MW-30 key already updated to CALL. Calibration already passed 24/24.
- Step 8: Review labels (≥21 reviewers, bias briefing included)
- Step 9: Combine with 200 self-play → ~757 total training rows
- Step 10: Leakage check (Gate 2.2) against corrected reference set
- Step 11: Train v3.1 (from-scratch, 52 features, cap 3.0)
- Step 12: Gate 2.3 (feature importance) + Gate 2.4 (reference eval)
- Step 13: Post-hoc bluff rule implementation + testing
- KB v1.3 update

### Training-time note for ML architect:
Existing Batch 1 has SPR=1.11 on 53% of situations (pot=90, effective_stack=100).
New batch will span SPR 1.0-10.0+ per R3. This creates a bimodal SPR distribution.
ML architect must address this explicitly in v3.1 training config (class-weight
correction, normalization, or feature-range handling). See review/RESEARCH_FIXED_STACK_TRAINING.md.

---

## Key files

| File | Status |
|------|--------|
| knowledge/three_way_gto.md | v1.2 — needs v1.3 update (15 changes identified) |
| river-rats-core/feature_extractor.py | 52 features, flush_block_pct fixed, validator added |
| river-rats-core/feature_keys.py | 52 feature keys |
| river-rats-core/gto_model.py | 52 FEATURE_COLUMNS |
| river-rats-core/situation_factory.py | Action sequence validator added |
| river-rats-core/reference_evaluator.py | MW-42 fixed (agg count 2→1) |
| river-rats-core/train_model.py | v3 training config (needs update for v3.1) |
| review/generate_factory_situations.py | Fixed action sequences, 151 situations |
| review/generate_factory_batch2.py | Fixed action sequences, 261 situations |
| training-data/factory_situations.jsonl | Regenerated with 52 features, clean |
| training-data/factory_batch2_situations.jsonl | Regenerated with 52 features, clean |
| review/label_batches_v3/all_labels_v3.json | 406 labels, 5 corrections applied |

---

## Corrected reference scores (MW-42 fixed)

| Model | Raw | With MW-46 CALL |
|-------|-----|----------------|
| v8 | 23/40 (57.5%) | 24/40 (60.0%) |
| v2.2 | 33/40 (82.5%) | 34/40 (85.0%) |
| v3 (discarded) | 31/40 (77.5%) | 32/40 (80.0%) |

Gate: v3.1 must tie or beat v2.2's 33/40 raw.

---

## Critical constraints

1. **No artificial deadlines.** Quality over speed. (memory/feedback_no_deadlines.md)
2. **Solver labels are verification/research only.** Never training labels. (FEEDBACK_SOLVER_LABELS_DANGER.md)
3. **Labels must be feature-visible.** If the reasoning requires info not in the 52 features, the label is wrong.
4. **Process Guide §3** applies: research before design, ≥8 sources, independent review.
5. **Don't present options menus.** Recommend, don't ask.
6. **Present for review — always.** Don't ask whether to review; present and move on.

---

## The RAISE question — RESOLVED

Research complete (Research A: 28 poker sources, Research B: 52-feature
analysis). Decision tree v2 approved. Factory brief v2.1 approved with
diversity requirements.

**Next steps (in order):**
1. ~~Fix the decision tree~~ → DONE (v2 approved)
2. ~~Verify self-play RAISE yield~~ → DONE (37/200 = 18.5%)
3. ~~Update factory brief~~ → DONE (v2.1 with diversity requirements)
4. ~~Get owner approval~~ → DONE (tree + brief approved)
5. Design 151 new factory situations per brief v2.1 + diversity R1-R7
6. Generate through factory with 52 features + action validator
7. Relabel ALL ~557 situations (406 existing + 151 new) with v2 tree
8. Review labels (≥21 reviewers, bias briefing included)
9. Combine with 200 self-play → ~757 total training rows
10. Leakage check (Gate 2.2) against corrected reference set
11. Train v3.1 (from-scratch, 52 features, cap 3.0)
12. Gate 2.3 (feature importance) + Gate 2.4 (reference eval)
13. Post-hoc bluff rule implementation + testing

**Sample size target:** 150-160 RAISE labels total. Distribution:
40% value, 30% semi-bluff, 20% thin value, 10% bluff. Plus 42
CALL counterexamples in RAISE-context situations. Projected total
RAISE ~176-181 (provides buffer for labelling yield).

## Current label state

406 factory situations labelled with simplified is_monster-only rule.
5 corrections applied (3 over-fold, 2 RAISE violations).
38 RAISE labels, all is_monster.
These will be RELABELLED with v2 tree once new factory situations exist.

---

## Review docs — reading order for next session

| File | What | Priority |
|------|------|----------|
| review/BOARD_ALLOCATION_V3_FINAL.md | Board allocation (33 boards, 151 situations) | READ FIRST |
| review/comms/BET_FACTORY_PLAN_2026-04-09.md | Batch 4 factory plan (BET contexts) | READ SECOND |
| review/BET_DECISION_TREE_V1.md | BET tree (recalibrated, reviewed) | READ THIRD |
| review/FOLD_DECISION_TREE_V1.md | FOLD tree (reviewed) | Reference |
| review/RAISE_DECISION_TREE_V2.md | RAISE tree (approved) | Reference |
| review/FACTORY_DIVERSITY_AUDIT.md | Diversity R1-R7 framework (adapt for batch 4) | Reference |
| review/deterministic_labeller.py | Labelling script (update after batch 4) | Reference |

## Superseded docs (do not use for building)

| File | Superseded by |
|------|--------------|
| review/RAISE_DECISION_TREE_V1.md | RAISE_DECISION_TREE_V2.md |
| review/FACTORY_DESIGN_RAISE_CONTEXTS.md | FACTORY_DESIGN_RAISE_CONTEXTS_V2.md |
| review/REVIEW_RAISE_DECISION_TREE_V1.md | REVIEW_RAISE_DECISION_TREE_V2.md (all findings addressed) |
| review/BOARD_ALLOCATION_V3_BATCH.md | BOARD_ALLOCATION_V3_FINAL.md |
| review/BOARD_ALLOCATION_V3_BATCH_V2.md | BOARD_ALLOCATION_V3_FINAL.md |

## Plans and reviews on disk

| File | What |
|------|------|
| review/PLAN_V3_COMPLETE.md | The approved master plan |
| review/CALIBRATION_GRADING_V3.md | Calibration grading with bias profile |
| review/PROPOSAL_BLUFF_FEATURES.md | Bluff feature research and proposal |
| review/KB_V1.3_REQUIREMENTS.md | 15 KB changes from solver session |
| review/FEEDBACK_SOLVER_LABELS_DANGER.md | Critical constraint on solver labels |
| review/SOLVER_SESSION_NOTES.md | Aggression tracking insight |
| review/SOLVER_ANALYSIS_SUMMARY.md | 24 solver hands analyzed |
| review/BLUEPRINT_FEATURES_V3.1.md | Feature pipeline blueprint (implemented) |
| review/BLUEPRINT_TRAIN_V3.md | Training blueprint (needs update for v3.1) |
