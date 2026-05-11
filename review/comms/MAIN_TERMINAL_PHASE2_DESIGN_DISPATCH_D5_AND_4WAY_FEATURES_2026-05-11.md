---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: Phase 2 ARCHITECTURAL DESIGN dispatch — comprehensive feature design memo combining D5 (3-way ceiling lift; deferred blueprint) + 4-way readiness (owner: "players left to act is a big driver"); design-first per owner direction "be careful on features and make sure we are truly ready for 4-way before building and training model"
status: DISPATCH — fire now (DESIGN-ONLY; NO model build, NO corpus changes, NO feature implementation; just the architectural memo)
---

# Phase 2 ARCHITECTURAL DESIGN dispatch

Phase 1.5 SHIPPED at master `6961cca` (vNext-HU-59 production HU oracle; 3-way + multiway routing unchanged). Owner direction (2026-05-11 02:30 SAST):
- "yes please [combined D5 + 4-way]"
- "we need to be careful on features and make sure we are truly ready for 4-way before building and training model"

Per owner direction + `feedback_quality_default_no_ask.md` + `feedback_pilot_first_for_long_jobs.md` + `feedback_orchestrator_decides_not_recommends.md`: Phase 2 starts with a **DESIGN-ONLY architectural dispatch** (builder-architect produces comprehensive memo). Owner ratifies the feature lock BEFORE any build/train work fires.

## Scope of THIS dispatch (PR-A: design memo)

Builder-architect produces ONE comprehensive memo: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` (analog to PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md).

### §1 Current state attestation (analog to 1.5-A §1)

Survey + attest current production state post-1.5 ship:
- Production oracle routing (`oracle_router.py:34-38` `_MODEL_FILES`) — vNext-HU-59 + v9-3way + v9-4way (45-feat) + v9-5way
- Current 59-feature surface (FEATURE_COLUMNS in `feature_extractor.py`)
- Inference path infrastructure (`inference_path_59.py` from PR-A 1.5-E)
- Solver-verification queue: 48 spots HOLD-with-accepted-risk per owner; verify-and-retrain-if-needed is recovery (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)
- 12.5K experiment ceiling per `project_v9_3way_ceiling.md` (v9-3way-v2.2 = Phase 1 INTERIM; D5 deferred)
- 4-way model status: v9-4way at 45-feat surface; trained on PokerBench-derived data; never refreshed since v9-3way work

### §2 D5 blueprint refresh (build on PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md)

Existing blueprint (master `a382fa2` per PR #302 sequencing) covers:
- 11 candidate features targeting MW-40/45/47 stay-wrong axes
- 3-feature pilot gate (≥1 of 3 candidates ≥2% importance + ≥1 stay-wrong graduates)
- Full D5 cost: ~$0 LLM + ~30-40h builder (corpus reused)

**Architect-hat refresh required:**
- Are the 11 candidates still valid given current state? (post-1.5 ship; vNext-HU-59 production; possibly different feature interactions)
- Any candidate to drop / modify / add given new evidence?
- Does the pilot gate threshold need adjustment?
- Are the stay-wrong axes (MW-40/45/47) still the right targets? Re-verify per current solver-corrected reference labels (`reference_corrections.md` memory: MW-30 CALL, MW-46 CALL, MW-47 RAISE)
- Stale-check the candidate list staleness clause per blueprint §8

### §3 4-way feature gap analysis (NEW; owner-driven)

**Owner-surfaced concern (2026-05-11 02:25 SAST):** "players left to act is a big driver" in 4-way decisions.

**Architect + GTO-expert hat survey** (extending the prior orchestrator-level analysis):

Current 59-feat surface contains:
- `num_opponents` (1/2/3/4): total live villains
- `num_callers_to_bet`: aggregated callers BEFORE hero this street
- `hero_position`, `villain_position`, `is_ip`: seat-based positioning
- Metadata only (NOT model features): `_opener_position`, `_bettor_position`

Identified 4-way gaps (orchestrator first-pass):
- ❌ No explicit `players_to_act_after_hero` (count of villains still to act post-hero in current street)
- ❌ No `hero_action_index` (hero's ordinal position in current street's action sequence)
- ❌ No `live_aggressors_behind` (count of behind-hero villains who haven't folded yet — captures squeeze risk)

**Architect deliverable for §3:**
- Independently verify the gap analysis (read feature_extractor.py + game_state code paths)
- Survey ANY OTHER 4-way-specific features missing (not just "players left to act" — any decision-class where 4-way GTO requirements diverge from HU/3-way)
- Propose 3-7 candidate 4-way features (analog to D5 11-candidate structure)
- Evidence why each candidate matters (GTO theory + observable failure mode in v9-4way 45-feat current production)
- Falsification criterion per candidate (analog to D5 §2 "what would falsify")
- Pilot gate strategy for 4-way candidates (analog to D5 §4)

### §4 Combined surface lock proposal

After §2 + §3 candidate sets are finalized:

- Total candidate features: D5 (11) + 4-way (3-7) = ~14-18 candidates
- Implementation will likely DROP some as redundant/under-specified (D5 blueprint §3 anticipated 11→fewer; same applies here)
- Final target surface size estimate: 75-80 features (current 59 + ~15-20 net additions)
- **PROPOSAL ONLY — NOT FINAL.** Owner-gate ratification required (per next §6).

### §5 Sub-phase decomposition (post-design-ratification)

Builder-architect proposes the execution sub-phases in the design memo. Suggested structure:

| Sub-phase | Subject | Pilot+full | Owner-gate fires |
|---|---|---|---|
| 2-A | Architectural design memo (THIS dispatch's deliverable) | N/A | Owner ratifies feature lock + sub-phase structure |
| 2-B | Feature implementation PILOT (3 candidates: 1 D5 axis representative + 1 4-way axis representative + 1 cross-axis) | Pilot gate | Importance + stay-wrong graduation gate |
| 2-C | Full feature implementation (remaining 11-15 candidates) | n/a | Per-feature unit-test gate |
| 2-D | 4-way reference set design (analog to 1.5-D.1 HU reference) | Pilot=5 hands; full=25-35 hands | Pilot+full gate |
| 2-E | 4-way labelling + corpus assembly (analog to 1.5-D.2 + D.3; ~750 lookalikes) | Pilot+full per `feedback_pilot_first_for_long_jobs.md` | Per-phase QC |
| 2-F | 3-way re-extract + retrain on new surface (D5 path; uses existing 988-corpus) | 5-seed | Ship gate ≥36/40 (D5 hypothesis target) |
| 2-G | 4-way retrain on new surface + new corpus | 1-seed smoke + 5-seed full | Ship gate TBD per design memo |
| 2-H | Production swap (force-add new 3-way + 4-way models + oracle_router updates) | n/a | Phase 2 SHIP boundary |

Builder-architect refines + commits in the design memo.

### §6 Owner-scope items to surface (architect lists; owner ratifies)

Architect surfaces all owner-WHAT decisions for owner ratification BEFORE 2-B fires:

- **Feature lock**: ratify the candidate list (D5 + 4-way, total)
- **Surface size target** (75? 80? other?)
- **Corpus origin for 4-way** (fresh expert-labelled ~750 OR augment existing PokerBench-multiway data; HU pattern was fresh)
- **Solver-verification queue posture** (still accepted-risk per HU pattern, OR drain queue first?)
- **3-way ship gate** (D5 hypothesis target ≥36/40 as committed in blueprint, or revise?)
- **4-way ship gate** (multiway-analog ≥35/40 or different?)
- **Pre-Phase-2 incidental items**: design memo §4.6 footnote amendment; HU-6.5 corpus-exclusion-gap refinement — fold into Phase 2 OR ship as separate small-PR pre-Phase-2?

Architect proposes default per quality-default; owner can override.

### §7 NO build, NO train, NO corpus work

This dispatch is **DESIGN-ONLY**. Builder-architect produces the memo. NO:
- ❌ Feature implementation in `feature_extractor.py`
- ❌ Corpus modifications
- ❌ Trainer changes
- ❌ Reference set design (4-way reference is 2-D scope, not 2-A)
- ❌ Model artifact production
- ❌ oracle_router.py changes

**Memo + commit + open PR is the ONLY deliverable.**

## STOP conditions (per CLAUDE.md §5)

- Architect-hat finds D5 blueprint stale beyond simple refresh (e.g., MW axes have shifted; 988-corpus deprecated; etc.) → STOP / REPORT; orchestrator surfaces to owner before architect commits to refresh scope
- 4-way gap analysis surfaces concerns beyond "players left to act" that change Phase 2 fundamentally (e.g., game-state representation gaps; multiway range chain limitations) → STOP / REPORT; orchestrator surfaces to owner
- Architect cannot satisfy "be careful on features" with a single-memo deliverable (e.g., needs spike work to validate hypothesis) → STOP / REPORT; orchestrator may amend dispatch with spike scope

## Negative scope (TC-X-OWNER-SCOPE-DISCIPLINE)

- ❌ Does NOT execute any D5 or 4-way build work
- ❌ Does NOT modify any model artifacts
- ❌ Does NOT modify production routing
- ❌ Does NOT touch existing corpora (988-corpus, hu_corpus, etc.)
- ❌ Does NOT change ship gates without owner ratification
- ❌ Does NOT solver-verify queue spots (HOLD-with-accepted-risk per owner; folds into Phase 2 as design item if needed)
- ❌ Does NOT skip pilot+full split per `feedback_pilot_first_for_long_jobs.md` standing rule

## QC stream — what you audit (post-design-PR)

When builder PR opens (design memo only):

1. Diff scope strict: 1 file (`review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`); NO source/data edits
2. Memo coverage: §1-7 sections present + addressed per this dispatch
3. D5 blueprint refresh: candidates re-validated against current state; staleness assessed
4. 4-way gap analysis: independent verification + new candidates with GTO-evidence
5. Surface lock proposal: candidate list complete + size target
6. Sub-phase structure proposed
7. Owner-scope items surfaced (architect proposes defaults; owner-gate items clearly marked)
8. TC-X-DISPATCH-COMPLIANCE: design-only scope honored

QC routing per `feedback_qc_routing_when_standalone_active.md`. ~20-25 min audit (memo-heavy; cross-references to existing memos required).

## What gates next

- Builder design memo PR → on QC PASS, orchestrator merges autonomously
- After merge → orchestrator surfaces architect's owner-scope items to owner (per §6) → owner ratifies feature lock
- After owner ratification → Phase 2-B (feature implementation pilot) dispatched

## Owner — informational

- Phase 2 starts with comprehensive design (D5 blueprint refresh + 4-way gap analysis + new surface lock + sub-phase plan)
- NO build/train work fires until you ratify the feature lock
- Solver-queue (48 spots) HOLD-with-accepted-risk per your direction; design memo addresses how queue affects 4-way reference design
- Estimated design-memo wall-clock: ~4-8h architect work (analog to PHASE15A complexity; covers D5 + 4-way both)
- After your ratification, execution begins per pilot-first standing rule

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `6961cca` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 1.5 SHIPPED: master `6961cca` (PR #382 + QC PR #384 PASS)
- D5 deferred blueprint (refresh starting point): `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (master `a382fa2` per PR #302 sequencing)
- Phase 1.5 unified surface design (analog template): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Stay-wrong taxonomy + Phase 1 INTERIM ceiling: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`
- Reference corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Feature extractor: `river-rats-core/feature_extractor.py` (FEATURE_COLUMNS at line 1569)
- Inference path 59: `river-rats-core/inference_path_59.py` (merged 1.5-E PR-A)
- Production oracle router: `river-rats-core/oracle_router.py` (`_MODEL_FILES` lines 33-39)
- Solver-verification queue protocol: `~/.claude/projects/-home-rupertbeytell/memory/feedback_solver_verification_queue.md` + `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_qc_required_before_approval.md`, `feedback_river_rats_team_structure.md` (builder wears architect-hat + gto-expert-hat — single party)

**Status: Phase 2 DESIGN-ONLY dispatch fires LEAD-PROGRAMMER (architect+ml-architect+gto-expert hats). Comprehensive memo combining D5 blueprint refresh + 4-way feature gap analysis + new surface lock proposal + sub-phase plan + owner-scope items. NO build/train work. After QC PASS + merge → orchestrator surfaces owner-scope items → owner ratifies feature lock → Phase 2-B pilot dispatched.**
