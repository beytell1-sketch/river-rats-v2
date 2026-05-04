---
date: 2026-05-04
from: Main terminal (orchestrator)
to: Owner · QC stream · GTO-EXPERT · ML-ARCHITECT · LEAD-PROGRAMMER
re: Phase 12.5D gate FAIL — orchestrator decision (Direction D); expert dispatches in parallel; owner WHAT decision deferred until findings land
status: DECISION + DISPATCHES
---

# Phase 12.5D — orchestrator decision on the gate FAIL

LEAD-PROGRAMMER PR #126 BLOCKED on dispatch stop condition #3 (gate FAIL: median seed 31/40 < v9-3way-v2.2 baseline 33/40 in same run). Builder stood down correctly. Trainer ran cleanly, all 16 tests pass, Path Y discipline preserved (4 files, zero source-surface edits), no model artifact promoted.

## Orchestrator independent verification

I read the BLOCKED comm (`BUILDER_BLOCKED_PHASE125D_GATE_FAIL_2026-05-03.md`) and trainer report Section A-D. Three claims I verified specifically:

| Claim | Verification |
|---|---|
| 4-file diff exactly | ✅ PR #126: trainer + tests + report + BLOCKED comm; no model file |
| Path Y discipline (no source edits) | ✅ files list contains zero existing source paths |
| Stop condition #3 reading | ✅ correctly invoked: 31 < 33, model not written |
| Per-hand failure pattern | ⚠️ **NOT just RAISE collapse**: student under-bets MW-17/24/25/40/42 (CALL/CHECK where expert BET), over-aggresses MW-31/46, collapses RAISE on MW-45/47. Mixed-direction miscalibration. |

The mixed-direction failure pattern matters: a RAISE-class fix alone (Direction C — hybrid weighting per ml-architect §11 R-2 option C) won't close the 31→33 gap. The 5 under-betting failures are independent of RAISE collapse.

## Orchestrator decision: Direction D (defer; expert findings first)

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator decides sequencing/team allocation; **owner decides WHAT/WHETHER** between Directions A (accept gate fail; close 12.5D), B (re-evaluate gate threshold), C (12.5D' with hybrid RAISE weighting). All three need informed inputs first.

**Direction D (orchestrator scope — sequencing decision):** dispatch gto-expert + ml-architect + QC in parallel; owner reviews their findings + this synthesis before making the A/B/C call. ETA to owner gate: as fast as the slowest expert.

This is not "recommend D" — it's the orchestrator deciding the next sequencing step. Owner's WHAT decision (A/B/C) is preserved and informed when it happens.

## Three parallel dispatches

### QC pre-merge audit on PR #126

Per dispatch directive PR #125 §"QC": pre-merge audit fires on the 12.5D PR. TC-23 sub-vector applies.

QC, run the three audits on PR #126:

1. **Diff scope** — exactly 4 files (the model artifact is correctly absent per stop condition); no edits to existing source surfaces
2. **Citation existence** — every file:line citation in `train_model_v9_student.py` + tests + trainer report exists at master HEAD `e3c0dfc` (CONTENT drift + EXISTENCE drift sub-vectors per TC-23)
3. **Provenance** — `train_model_v9_student.py` provenance docstring matches the trainer report Section D hashes (CLAUDE.md §6 addendum); model artifact absence is consistent with stop condition #3

Note: this is a BLOCKED PR. QC's job is to confirm the BLOCKED state is faithfully reported and the code that landed is mergeable as a re-runnable trainer baseline (even though no model artifact ships). HOLD on any audit failure; APPROVE if all three audits pass.

Post `REVIEW_QC_PHASE125D_TRAINER_2026-05-04.md`.

### GTO-EXPERT — per-hand failure analysis (Findings 2 + 3)

Read trainer report Section B "Solver-corrected per-hand comparison" (10-row table) and Section C P1-blocker importance (row 165-172). Specifically diagnose:

**a. Mixed-direction miscalibration root cause.** The student fails on 9 hands (3 over-aggressive: MW-31, MW-46, MW-46-RAISE-where-CALL; 5 under-aggressive: MW-17 FOLD, MW-24/25/40/42 CHECK; 2 RAISE-collapse: MW-45, MW-47). Is this one root cause (e.g., conservative bias from confidence weighting) or several? Specifically: could the under-betting failures (MW-24/25/40/42) and the RAISE collapse (MW-45/47) share a common feature-level cause, or are they independent failures requiring separate mitigations?

**b. P1 blockers' poker-theoretic relevance to the 40-hand reference set.** The migration's premise is that nut/flush/straight-blocker features matter for canonical RAISE/bluff spots. Empirically the booster never split on `nut_flush_block` (0.0000 importance) and `straight_draw_block_pct`/`nut_made_block_pct` are below 1%. Two competing hypotheses:
   - H1: The features genuinely matter, but the 494-hand training corpus has too few situations where blockers discriminate between expert actions for importance gain to register them. → mitigation is data-side (more blocker-decisive situations in next labelling round).
   - H2: The features are poker-theoretically real but the reference set's RAISE/bluff hands (MW-45, MW-46, MW-47, etc.) are decided by other features (equity, position, opponent type) and blockers are second-order. → mitigation is to revisit whether the migration is worth shipping at all.

   Per `feedback_preflop_geometry_vs_postflop_composition.md`: reason from TP+/draws/air composition. Look at MW-45 + MW-47 specifically — would correctly weighting `nut_flush_block` change the predicted action? Or are these decided by composition-level features that are present in the 55-feature surface anyway?

Post `REVIEW_GTO_EXPERT_PHASE125D_2026-05-04.md`. Recommend HOW between H1/H2 and identify whether RAISE-collapse + under-betting share a cause.

### ML-ARCHITECT — design-level recommendations (Findings 1 + 2)

**a. Blueprint join-key defect post-mortem (Finding 1a).** Builder discovered that blueprint §6's `corpus.source_situation_id == labels.ref_id` join key was verified on row 1 only and breaks on rows 100-493 (cohort 2 uses `situation_id`; ref_id is heterogeneous). Empirical correct key is `pilot_hand_id == pilot_hand_id` (494/494). What was the root cause of the blueprint defect — bad spec inheritance from PR #110, insufficient pre-flight on the corpus by the blueprint author, or a real schema change since the corpus was generated? Recommend the blueprint pre-flight protocol amendment that prevents recurrence.

**b. In-module schema handling (Finding 1b).** Builder added `_StudentInference` + `_evaluate_student_one_hand` as in-module 59-feature mirrors of `reference_evaluator._evaluate_one_hand` because Path Y forbids extending `gto_model.FEATURE_COLUMNS`. Is this in-module mirror methodologically sound, or does it create a hidden divergence risk where the student inference path drifts from the canonical 55-feature path during future maintenance? If unsound, what's the alternative under Path Y constraints?

**c. R-2 mitigation recommendation (Finding 2).** Empirical RAISE collapse confirmed as predicted in your §11 R-2. Of the three §11 R-2 options (A: more RAISE training data; B: oversampling; C: hybrid weighting), which do you recommend now that we have empirical numbers? Is a single mitigation sufficient, or are findings 2 + the under-betting half of finding 1 likely to need a combined approach?

Post `REVIEW_ML_ARCHITECT_PHASE125D_2026-05-04.md`. Per `feedback_orchestrator_decides_not_recommends.md`: HOW recommendations only; do not pre-empt owner's A/B/C WHAT decision.

## What LEAD-PROGRAMMER does

Stand down per `feedback_named_author_builds_not_polls.md`. PR #126 is open and BLOCKED; no action until owner decides Direction A/B/C and orchestrator dispatches the next round. Do not speculatively start re-runs, hyperparameter sweeps, or design alternatives.

## What the owner decides (when expert findings land)

Owner picks among:

- **A** — accept gate fail; close 12.5D as ran-cleanly-fell-short; iterate via 12.5+1 (informed by ml-architect R-2 mitigation choice + gto-expert H1/H2 verdict)
- **B** — re-evaluate gate threshold; potentially ship 31/40 as "good enough" if expert findings show the gap is structural (e.g., student is solver-correct on hands the baseline gets wrong by a different mechanism)
- **C** — 12.5D' run with the specific R-2 mitigation ml-architect recommends + any data-side fix gto-expert recommends
- (Any other direction the experts surface that orchestrator and builder didn't list)

## What does NOT happen at this gate

- **PR #126 does NOT merge until QC APPROVE lands** (per dispatch directive QC pre-merge audit gating)
- **No 12.5+1 dispatch** until owner picks A/B/C
- **No source surface edits** under any direction without a fresh ml-architect design pass + owner gate (Path Y discipline still binds)
- **No model promotion** under any direction without a passing reference-evaluator gate

## Sequencing

1. **Now (parallel):** QC pre-merge audit on PR #126; gto-expert per-hand analysis; ml-architect design recommendations
2. **As findings land:** orchestrator synthesizes into a single owner-gate-prep doc
3. **Owner WHAT decision (A/B/C/other):** informed by all three expert outputs + this synthesis
4. **On owner decision:** orchestrator dispatches the chosen path

## References

- BLOCKED PR #126 (open, branch `programmer/phase125d-trainer-impl-2026-05-03`)
- Dispatch directive PR #125 (master `e3c0dfc`)
- Approved blueprint PR #122 (master `1e4e47e`)
- Pivot directive PR #119 (master `770b897`)
- ml-architect spec PR #110 (master `291af80`) — §11 R-2 RAISE-collapse risk register
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_named_author_builds_not_polls.md`, `feedback_check_comms_before_wait.md`

**Status: ORCHESTRATOR DECISION = DIRECTION D. Three parallel dispatches issued (QC + gto-expert + ml-architect). PR #126 holds open. Owner WHAT decision deferred to post-findings synthesis.**
