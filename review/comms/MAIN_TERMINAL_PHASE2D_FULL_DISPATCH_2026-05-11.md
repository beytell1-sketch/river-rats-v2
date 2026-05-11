---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat + gto-expert-hat)
re: Phase 2-D-FULL — 30 additional 4-way reference hands (pilot+full second half); brings reference set to 35-hand total per AMENDMENT 1 street distribution + AMENDMENT 2 closing-action variants
status: DISPATCH — fire now (Phase 2-D pilot merged at master e518028; PR #405 + #407 PASS 0/0/0)
---

# Phase 2-D-FULL dispatch — 30 additional 4-way reference hands

## Context

Phase 2-D PILOT (PR #405) cleared 5/5 gate with QC PASS (PR #407, 0/0/0). The 5 pilot hands cover: closing-action (PILOT-1), MW-40 TPGK (PILOT-2), MW-47 nut FD blocker (PILOT-3), range-asymmetry MP (PILOT-4), MW-45 broadway turn (PILOT-5). Spec framework `PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md` (PR #405) establishes the per-hand format + axis allocation.

Phase 2-D-FULL builds the remaining 30 hands to complete the 35-hand 4-way reference set that gates Phase 2-G retrain.

## Target full-set distribution (35-hand total per AMENDMENT 1)

Street distribution per AMENDMENT 1 (§3.X.2) 51/31/11/6:

| Street | Target % | Target count | Pilot | Full needed |
|--------|----------|--------------|-------|-------------|
| flop | 51% | 17-18 | 3 | **15** |
| preflop | 31% | 10-11 | 1 | **10** |
| turn | 11% | 3-4 | 1 | **3** |
| river | 6% | 2 | 0 | **2** |
| **Total** | 100% | **35** | **5** | **30** |

## Axis coverage (full-set guidance)

Per pilot builder report §"Axes deferred to full 30-hand":

- **4-way 3-bet pots (squeeze cold-call)** — at least 2-3 hands; one of these the 4-way preflop squeeze scenario
- **4-way 4-bet pots (rare)** — ~1-2 hands (architect's call on whether to include given rarity)
- **Multiway-cooler spots** — 2-3 hands covering sets vs straights / two-pair vs flushes / top-set vs nut flush
- **River decisions** — 2 hands (6% of 35); both river-jam-fold or river-thin-value-bet axes
- **BET decisions** — at least 3-4 hands (donk-leads OOP value, OOP block-bets, IP value-bets after villain checks)
- **FOLD decisions** — at least 2-3 hands (fold-to-3-bet preflop, fold-to-river-jam, fold-to-multiway-aggression)
- **Range-asymmetry continuations** — extend pilot's PILOT-4 MP axis; cover BTN-vs-MP, EP-vs-everyone, SB-vs-BTN asymmetries

Architect picks final distribution within these axis families; goal is COVERAGE not exhaustiveness.

## Decision class diversity target

Pilot had: CALL × 2, CHECK × 2, RAISE × 1, BET × 0, FOLD × 0 (3 of 5 classes).

Full-set should achieve 5-of-5 class diversity:
- BET (3-4 hands)
- FOLD (2-3 hands)
- CHECK (~8-10 hands continuing pilot coverage)
- CALL (~7-9 hands continuing pilot coverage)
- RAISE (~3-5 hands continuing pilot coverage)

Numbers approximate; architect adjusts within axis-coverage constraint.

## Implementation deliverables (per builder pilot pattern)

1. **30 hands appended to spec framework**:
   - Update `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md` OR create new `PHASE2D_4WAY_REFERENCE_FULL_DESIGN_2026-05-11.md` covering hands #6-#35
   - Each hand specified per pilot format: pre-flop action history, board, hero hole cards, opponent count, expected action, primary axis
   - Architect picks (cleaner: single combined doc)

2. **Per-hand gto-expert rationale**:
   - `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md` (or append to pilot rationale doc)
   - ~250-400 words per hand × 30 hands ≈ 7500-12000 words total
   - NO rule-based shortcuts (per FL4 incident + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)
   - Range composition / equity realization / blocker effects / pot geometry reasoning
   - Terminology compliance (raise vs bet) + solver-aligned bet sizing

3. **Machine-readable artifact**:
   - `data/4way_reference_35hand_2026-05-11.jsonl` (or `.json`) — full 35-hand set including 5 pilot + 30 new
   - Each line has required fields (architect's pilot JSONL schema preserved)
   - Validation: 35 valid JSON lines; no NaN; all required fields present

4. **Owner-arb adjudication** for ambiguous spots:
   - If any of the 30 hands has architect uncertainty (e.g., 50/50 GTO call vs raise; closing-action edge cases), flag for owner review BEFORE submitting
   - Adjudication request via `review/comms/OWNER_ARB_PHASE2D_FULL_<DATE>.md` if needed
   - Per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`: if owner deferring, orchestrator picks per quality/GTO + queues for solver verify later

5. **Builder report**:
   - `review/comms/BUILDER_REPORT_PHASE2D_FULL_4WAY_REFERENCE_2026-05-11.md` covering:
     - 30 hands delivered + axis coverage breakdown
     - Street distribution actual vs target (should match 18/11/4/2)
     - Decision class diversity (5-of-5)
     - Compliance with pilot gate criteria (rationale quality, no rule-based, terminology, solver-aligned)
     - Owner-arb items (if any)
     - STOP-condition status

## What Phase 2-D-FULL does NOT do

Per design memo §5 + §7 + `feedback_pilot_first_for_long_jobs.md` (already-cleared pilot):

- ❌ Does NOT touch `feature_extractor.py` (surface 61 frozen)
- ❌ Does NOT touch `oracle_router.py` (2-H scope)
- ❌ Does NOT generate or label lookalike corpus (2-E scope; 2-E.0 labeller readiness gate first)
- ❌ Does NOT retrain production models (2-F / 2-G)
- ❌ Does NOT touch model artifacts
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4)
- ❌ Does NOT design 4-way labeller brief (that's 2-E.0 scope; AMENDMENT 3 owner-ratified §6.8)

## STOP conditions (per CLAUDE.md §5)

- 4-way 4-bet pots can't be sourced (rare spot type) → REPORT; orchestrator may amend with reduced 4-bet coverage
- Per-hand rationale slides into rule-based shortcuts → STOP; require explicit anti-rule-based pattern (mirrors FL4 incident lessons)
- River decision spots can't reasonably be sourced (river is rare in 4-way) → REPORT; orchestrator may amend; OR architect makes judgment call (e.g., 1 river instead of 2; document deviation)
- ≥3 hands require owner-arb adjudication → SURFACE all in one batch comm; do not improvise picks unilaterally
- Wall-clock blows past ~12h (memo estimate 6-10h × 30% buffer for 30-hand subset) → REPORT
- TC-23 EXISTENCE: JSONL artifact + rationale doc + builder report must be git-tracked

## QC stream — what you audit (pre-merge milestone)

Per `feedback_qc_required_before_approval.md`:

1. **Diff scope**: 30 new hands + rationale + JSONL + report; NO river-rats-core/ / oracle_router / model edits
2. **Hand count**: 30 new hands (35 total with pilot's 5)
3. **Per-hand rationale quality**: gto-expert reasoning chain; NOT rule-based / threshold-based
4. **Street distribution** (35-total): 17-18 flop / 10-11 preflop / 3-4 turn / 2 river (within ±2 of target)
5. **Axis coverage**: 4-way 3-bet + 4-way 4-bet (≥1) + multiway-cooler + river + BET + FOLD + range-asymmetry all represented
6. **Decision class diversity**: 5-of-5 classes (BET, FOLD, CHECK, CALL, RAISE) present
7. **True 4-way attestation**: each of 30 new hands verified 4-way at decision moment
8. **Terminology compliance** (raise vs bet) + bet sizing solver-aligned
9. **TC-X-DISPATCH-COMPLIANCE**: all deliverables present; no scope leak; owner-arb items surfaced if any
10. **JSONL validity**: 35 lines parseable; required fields present

QC routing: standalone per `feedback_qc_routing_when_standalone_active.md`. Output:
- `~/river-rats-qc/findings/2026-05-11-pr<N>-phase2d-full.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2D_FULL_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- Builder Phase 2-D-FULL PR → QC trigger when pushed
- On QC PASS (no owner-arb pending) → orchestrator merges + dispatches 2-E.0 (4-way labeller readiness per AMENDMENT 3)
- On QC PASS + owner-arb items pending → orchestrator surfaces arb decisions to owner BEFORE 2-E.0 dispatch (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`: owner-arbitrated spots may be solver-queued + retrain-recovery)
- On QC SHOULD_FIX → amend + re-fire
- On QC BLOCKER → hold + redo
- STOP condition → REPORT; orchestrator triages

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e518028` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-D pilot builder PR: master `3509679` (PR #405)
- Phase 2-D pilot QC PASS: master `e518028` (PR #407)
- Phase 2-D pilot dispatch (5+30 split): master `e2efc93` (PR #404)
- Phase 2-D pilot builder report: `review/comms/BUILDER_REPORT_PHASE2D_PILOT_4WAY_REFERENCE_2026-05-11.md`
- Phase 2-D pilot rationale: `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md`
- Phase 2-D spec framework: `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md`
- Phase 2-D pilot JSONL: `data/4way_reference_pilot_5hand_2026-05-11.jsonl`
- Design memo §3.X.2 (AMENDMENT 1 street distribution): `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` lines 260-273
- Design memo §3.Y.5 (AMENDMENT 2 reference set requirements): lines 363-372
- Design memo §6.6 (owner-ratified ship gate ≥28/35 weighted-total): lines 622-631
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_bucket_first_labelling.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`

**Status: Phase 2-D-FULL dispatch — 30 additional 4-way reference hands to complete 35-hand set. Distribution target 15 flop / 10 preflop / 3 turn / 2 river (per AMENDMENT 1 51/31/11/6 minus pilot's 5). Axis coverage: 4-way 3-bet/4-bet + multiway-cooler + river + BET + FOLD + range-asymmetry. Decision class diversity: 5-of-5. Architect estimate ~6-8h for 30 hands. Owner-arb adjudication batched if ≥3 ambiguous spots. Pilot-first standing rule already cleared (this is the full half). After 2-D-FULL QC PASS + merge → 2-E.0 dispatch (4-way labeller readiness per AMENDMENT 3 owner-ratified §6.8).**
