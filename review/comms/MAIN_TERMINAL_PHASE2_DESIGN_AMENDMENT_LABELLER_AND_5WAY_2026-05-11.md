---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-direction)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: AMENDMENT 3 to Phase 2 design dispatch (PR #385) — fold owner's 2 new questions into design memo: (a) 4-way labeller-prompt readiness sub-phase; (b) 5-way (catch-all 5..9 way) scope decision (include in Phase 2 OR defer)
status: DISPATCH AMENDMENT — fire now (folds new constraints into the in-progress / just-PR'd design memo; builder amends PR #388 OR opens follow-up PR)
---

# Phase 2 design AMENDMENT 3 — labeller readiness + 5-way scope

Owner direction (2026-05-11 03:05 SAST):
1. "does the plan include research session to make sure we can prompt labelers correctly on 4 way pots?"
2. "is it worthwhile to consider covering 5 and 6 way models now or keep separate?"

Both are architectural readiness/scope questions that the current design memo (PR #388) does not explicitly address. Builder must amend PR #388 OR open follow-up PR to address before QC + ratification.

## Item 1 — 4-way labeller-prompt readiness (NEW required section: §X "Labeller readiness for 4-way")

### Background

Phase 1.5 HU labelling experienced severe methodology violations (`BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`): FL4 wrote a Python rule-based scoring script; FL1/2/3/5 used template-based reasoning. Recovery required EXPLICIT anti-rule-based prompt boilerplate (validated by FL6+FL7-10).

**4-way labelling complexity is higher than HU.** Reasons:
- Multiple villain ranges to track (3 villains vs 1 in HU)
- Players-left-to-act logic (per AMENDMENT 1)
- Squeeze-pressure analysis (per AMENDMENT 2)
- Closing-action vs early-action differential
- Pot-cascade dynamics (4-way → 3-way → HU progression within a hand)
- Range-chain narrowing across multiple villains (per `range_narrowing.py` multiway path)

Naive re-use of HU labeller brief will likely produce labels that miss these multiway dimensions.

### Architect required deliverables (in design memo §X — new section)

1. **Survey HU labeller brief** (`data/hu_corpus/full_HU2_HU6/labeller_brief.md` or equivalent) + identify what extends naturally to 4-way vs what needs new design.
2. **Propose 4-way labeller brief design**:
   - Multiway range-chain reasoning (per villain's range, narrowed independently)
   - Players-left-to-act + squeeze-pressure prompting
   - Closing-action vs early-action explicit decision trees
   - Anti-rule-based boilerplate (mandatory per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + FL6 evidence)
   - Bucket-first compliance preserved (per `feedback_bucket_first_labelling.md`)
3. **Calibration set design** for 4-way:
   - HU calibration was 24-28 hands; 4-way may need more breadth (preflop + flop + 3-bet + 4-bet + closing-action variants)
   - Propose calibration anchor count + axis coverage
4. **5-hand pilot validation**:
   - Before firing full 4-way labelling pipeline (~750 lookalikes × 5 labellers), run a 5-hand pilot
   - Sample-check labeller reasoning for multiway-specific signal (not just HU-style reasoning applied to 4-way spots)
   - STOP-condition gate: if pilot shows naive HU-style reasoning OR rule-based shortcuts, REPORT before scaling
5. **New sub-phase 2-E.0** inserted before 2-E (labelling pipeline):
   - 2-E.0 = "4-way labeller readiness" = brief design + calibration set + 5-hand pilot validation
   - Gate: pilot validation passes (varied per-spot multiway-aware reasoning; no template/script)
   - Failure: re-design brief; do NOT proceed to full pipeline

### Why this matters

Naive labelling pipeline applied to 4-way spots produces HU-quality labels at 4-way scale → model trained on misaligned labels → bad model. The Phase 1.5 FL4 incident demonstrated that labelling discipline is fragile + must be explicit. 4-way adds dimensions that must be in the brief.

## Item 2 — 5-way scope decision (NEW required section: §Y "5-way scope")

### Background

`oracle_router.py:34-38` `_MODEL_FILES` routing:
- 1 → vNext-HU-59 (HU; refreshed Phase 1.5)
- 2 → v9-3way (3-way; D5 lift in Phase 2)
- 3 → v9-4way 45-feat (4-way; refresh in Phase 2)
- 4 → v9-5way (catch-all: ALL 4+ opponent pots, i.e., 5/6/7/8/9-way)

**v9-5way is the CATCH-ALL for any pot with 4+ opponents.** It has not been refreshed in the progressive chain since v9-3way work. No separate 6-way model exists.

### Architect required deliverables (in design memo §Y — new section)

1. **State assessment**: When does production HU/3-way/4-way oracle route to 5-way?
   - Only when `num_opponents ≥ 4` (5+ players in pot)
   - Frequency in PokerBench-derived multiway data: architect estimates
   - Frequency in typical coaching/mobile-app usage: architect estimates (likely low)

2. **Surface-size implication**: If 5-way refresh is included in Phase 2:
   - Same 75+ feature surface applies (inference path 59 already extended to surface-size dispatch)
   - Some features may be 5+way-specific or differently relevant (e.g., `players_to_act_after_hero` differentially relevant by table size)
   - Reference set must include 5+way scenarios (analog to 4-way 35-hand reference; might be 25-30 hands at higher cardinality)

3. **Corpus implication**:
   - 5-way labelling: even more multiway dimensions; same labeller-readiness concerns from Item 1 apply at higher scale
   - Existing PokerBench-multiway data: does it contain 5+way spots in sufficient volume to filter without re-labelling?
   - Cost trade-off: full 5-way fresh corpus ~$200-300 LLM (analog scaling from 4-way's ~$120)

4. **Architect proposal** (per `feedback_quality_default_no_ask.md`):
   - **Option A — Include 5-way in Phase 2**: same workstream; refresh 5-way alongside 3-way + 4-way; full progressive chain closure
   - **Option B — Defer 5-way to Phase 3**: scope Phase 2 to 3-way (D5) + 4-way only; keep 5-way as separate workstream
   - Architect picks default per quality + scope-discipline; surfaces as owner-scope item #10

5. **Quality-default trade-offs**:
   - Option A pros: full chain refresh; same surface; same labeller pipeline reuse; closes 5-way catch-all gap
   - Option A cons: Phase 2 wall-clock expands (~30-50h more); 5-way usage in production is rare; "be careful + truly ready" mandate strains
   - Option B pros: scope discipline; 4-way ships sooner; 5-way can be smaller dedicated workstream
   - Option B cons: 5-way stays on outdated 45-feat surface; eventual Phase 3 dispatch needed

## Item 3 — Updated owner-scope items count

Architect's existing 7 owner-scope items in PR #388 §6 expand to **9-10**:
- 8: 4-way labeller readiness + 2-E.0 sub-phase (Item 1 above)
- 9: 5-way scope (Option A include in Phase 2 / Option B defer; architect default per Item 2 above)
- (10: if Item 2 surfaces additional dependent decision)

## What this amendment does NOT change

- Phase 2 design-only scope (still NO build/train/corpus work)
- Same target deliverable file: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- AMENDMENT 1 (street distribution) + AMENDMENT 2 (re-raise × players-left) — both still apply
- Pilot-first standing rule still applies
- Owner-gate ratification before build/train still required
- Solver-queue HOLD-with-accepted-risk posture unchanged

## How to incorporate (architect's choice)

Builder-architect has two paths:
- **Path A (preferred)**: Amend PR #388 directly — add §X (labeller readiness) + §Y (5-way scope) + expand §6 owner-scope items
- **Path B (acceptable)**: Open a follow-up PR with the addition; QC audits the combined memo state

Either path: design memo must address both items BEFORE QC PASS gates ratification.

## STOP conditions (per CLAUDE.md §5)

- Architect cannot scope 4-way labeller readiness without spike work (e.g., 5-hand pilot is needed BEFORE architect can propose calibration set) → REPORT; orchestrator may amend with spike scope
- 5-way Phase 2 inclusion turns out to require fundamental architecture change (e.g., variable-cardinality model architecture) → REPORT; orchestrator + owner reconsider
- Item 1 + Item 2 require >2x the design wall-clock estimate → REPORT; orchestrator surfaces revised timeline

## Negative scope

- ❌ Does NOT change the design-only scope of Phase 2-A
- ❌ Does NOT pre-commit to specific labeller brief content or 5-way inclusion
- ❌ Does NOT change the owner-ratification gate before 2-B fires
- ❌ Does NOT supersede AMENDMENT 1 or AMENDMENT 2; all 3 apply

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `596bb89` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2 design dispatch: master `16a5aab` (PR #385)
- AMENDMENT 1 (street distribution): master `cee0705` (PR #386)
- AMENDMENT 2 (re-raise × players-left): master `596bb89` (PR #387)
- Phase 2-A design memo (currently in PR #388 open): head `cd5cc4f`
- HU labelling incident (FL4/FL1-5 methodology violation): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Recovery dispatch + AMENDMENT (Option A explicit-prompt): master `bdd1960` (PR #357)
- Production routing: `river-rats-core/oracle_router.py:34-38` `_MODEL_FILES`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_pilot_first_for_long_jobs.md`

**Status: AMENDMENT 3 folds 2 new owner concerns into design memo: (a) 4-way labeller-prompt readiness (new §X + sub-phase 2-E.0); (b) 5-way scope decision (new §Y + new owner-scope item #9). Builder-architect amends PR #388 (preferred) or opens follow-up PR. QC + ratification gate hold until both items in memo. Design-only scope unchanged. All 3 AMENDMENTS apply.**
