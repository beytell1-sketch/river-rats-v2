---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-direction)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: AMENDMENT to Phase 2 design dispatch (PR #385) — fold owner's "4-way action concentrates preflop + flop" insight into design memo before architect produces it
status: DISPATCH AMENDMENT — fire now (folds new constraint into in-progress design memo; same deliverable file)
---

# Phase 2 design AMENDMENT — 4-way street distribution

Owner direction (2026-05-11 02:55 SAST): "a lot of 4 way action is bound to be preflop and flop. can the plan account for this?"

**Architectural insight:** By turn/river, most 4-way pots have collapsed to 2-3-way (≥1 player folds by flop). "True 4-way" decisions concentrate at preflop + flop, with diminishing fraction on turn/river. This is a corpus-design + reference-design + feature-design constraint that must be in the architect's memo from the start (not bolted on after).

## What this amendment changes (folds into the in-progress design memo)

Architect adds a new section to `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`:

### §3.X 4-way street distribution analysis (NEW; required)

Architect-hat + GTO-expert-hat addresses:

1. **Empirical/theoretical street distribution of 4-way decisions**:
   - Estimate fraction of "true 4-way" decisions per street (preflop, flop, turn, river)
   - Sources: PokerBench multiway data distribution, GTO Wizard frequency tables, theoretical fold-out rate per street, or evidence from existing v9-4way training data
   - Expected shape: heavy preflop + flop; light turn; very light river (most multiway pots have collapsed by then)

2. **Implication for 4-way reference set design (2-D scope)**:
   - HU pattern was 30 hands × 6 axes evenly distributed across streets. 4-way SHOULD NOT mirror this evenly — would over-sample turn/river decisions where 4-way is rare in practice.
   - Architect proposes 4-way reference distribution (e.g., 60% flop, 25% preflop, 10% turn, 5% river — these are illustrative; architect commits per evidence-based estimate)
   - Total 4-way reference hand count: architect proposes (analog to HU 30; could be 30-40 weighted; architect-call)

3. **Implication for 4-way lookalike corpus (2-E scope)**:
   - Lookalike generator weights spots toward preflop + flop
   - "True 4-way" definition: pot is genuinely 4-way at decision moment (not 4-way preflop pot that's 2-way by river)
   - If using existing PokerBench multiway data: filter to actually-4-way-at-decision spots; document the per-street volume after filtering

4. **Implication for feature surface (§3 in design dispatch)**:
   - "players_to_act_after_hero" matters MOST preflop + flop where differential 0-vs-3-behind is largest
   - Other features may be street-conditional (e.g., `live_aggressors_behind` mostly relevant preflop + flop)
   - Architect surfaces ANY features in candidate set that are essentially preflop/flop-only — important for ML-architect to know during pilot evaluation (pilot importance score is per-street weighted)

5. **Implication for 4-way ship gate (§5 in design dispatch)**:
   - 30-hand reference scoring should weight by street distribution to match production usage
   - OR: ship gate is per-street (e.g., flop ≥X/N_flop, preflop ≥Y/N_preflop, etc.)
   - Architect proposes weighting/aggregation; owner ratifies

6. **Implication for v9-4way model behavior post-ship**:
   - Model will see mostly preflop + flop 4-way at runtime; turn/river 4-way is rare
   - Training data should reflect this distribution
   - Model SHOULD NOT optimize for turn/river 4-way at the expense of flop 4-way accuracy (that would be the wrong loss-weighting)

## What this amendment does NOT change

- Phase 2 design-only scope (still NO build/train/corpus work)
- Same target deliverable file: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- D5 blueprint refresh + 4-way feature gap analysis + sub-phase decomposition + owner-scope items — all still in scope
- Pilot-first standing rule still applies
- Owner-gate ratification before build/train still required
- Solver-queue HOLD-with-accepted-risk posture unchanged

## STOP conditions (per CLAUDE.md §5)

- Architect cannot find empirical/theoretical evidence for street distribution → STOP / REPORT; orchestrator surfaces to owner (may need a small spike to extract from existing data)
- Distribution evidence shows 4-way is much less concentrated than expected (e.g., 40% turn) → architect surfaces; orchestrator + owner reconsider weighting
- Existing PokerBench multiway data is insufficient to filter to "true 4-way" — STOP / REPORT; corpus-source decision needs revisiting

## Negative scope

- ❌ Does NOT change the design-only scope of Phase 2-A
- ❌ Does NOT pre-commit to specific street weighting (architect proposes; owner ratifies)
- ❌ Does NOT change the owner-ratification gate before 2-B fires

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `16a5aab` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2 design dispatch (this amends): master `16a5aab` (PR #385)
- D5 blueprint: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Phase 1.5 unified surface design (analog template): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_pilot_first_for_long_jobs.md`

**Status: AMENDMENT folds owner's "4-way concentrates preflop + flop" street-distribution insight into in-progress Phase 2 design memo. Architect adds §3.X to PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md addressing distribution evidence + reference set weighting + lookalike weighting + feature street-conditional surface + ship-gate implications + post-ship behavior. Same deliverable; design-only scope unchanged.**
