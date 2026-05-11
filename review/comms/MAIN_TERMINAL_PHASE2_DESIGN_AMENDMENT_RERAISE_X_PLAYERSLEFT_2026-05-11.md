---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-direction)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: AMENDMENT 2 to Phase 2 design dispatch (PR #385) — fold owner's "do we know when a pot is re-raised? with players left to act?" insight into design memo (re-raise × players-left interaction = squeeze-risk + closing-action signal)
status: DISPATCH AMENDMENT — fire now (folds new constraint into in-progress design memo; same deliverable file)
---

# Phase 2 design AMENDMENT 2 — re-raise × players-left interaction

Owner direction (2026-05-11 02:58 SAST): "do we know when a pot is re raised? with players left to act?"

**Architectural insight:** Owner identifies a SECOND 4-way decision-class gap complementary to AMENDMENT 1's "players left to act" gap: **the interaction between re-raise level and players-still-behind**. In 4-way: facing a 3-bet with 2 players behind ≠ facing the same 3-bet with 0 behind (closing action). This drives squeeze-risk + reverse-implied-odds + range polarization decisions.

## Current state attestation (orchestrator first-pass; architect verifies)

**What's in the 59-feat surface NOW (re-raise / aggression):**
- `is_3bet_pot` (binary; PREFLOP ONLY) — was preflop a 3-bet?
- `facing_raise` (binary; current street) — is hero facing a raise this street? Loses info on 4-bet vs simple 2nd raise
- `villain_aggression_count` (int) — count of villain aggression actions across history
- `_num_raises` (METADATA only — NOT in FEATURE_COLUMNS)

**Identified gaps:**
- ❌ No `is_4bet_pot` or escalation-level signal beyond binary 3-bet
- ❌ No `street_aggression_level` as a model feature (`_num_raises` is metadata; not fed to model)
- ❌ No interaction `facing_raise × players_to_act_after_hero` (squeeze-pressure signal)
- ❌ No `closing_action` flag (hero last-to-act = decision tree dramatically different)
- ❌ No `live_raisers_behind` (count of behind-hero villains who could still raise; combines with re-raise-level to flag squeeze risk)

## What this amendment changes (folds into the in-progress design memo)

Architect adds a new section to `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`:

### §3.Y Re-raise × players-left interaction analysis (NEW; required)

Architect-hat + GTO-expert-hat addresses:

1. **GTO theory of squeeze-risk in 4-way**:
   - Facing a re-raise (3-bet, 4-bet) with N players behind = squeeze potential from those N players. Hero's calling range MUST tighten as N grows.
   - Reverse-implied-odds: calling a re-raise OOP with 2+ players behind = bad position post-flop + risk of being bet-into multiway = need premium hands.
   - Closing-action flag: hero is last to act = no squeeze risk = decision tree is binary fold/call (or jam) without future-action complexity.
   - 4-way is where this matters most; HU has no "behind" players; 3-way is mild.

2. **Independent verification of orchestrator gap analysis**:
   - Read `feature_extractor.py` Step 7 + Step 11 sections
   - Confirm `_num_raises` is metadata-only (not in FEATURE_COLUMNS)
   - Confirm `is_3bet_pot` is preflop-only binary (not multi-street, not multi-level)
   - Confirm no existing `closing_action` / `squeeze_risk` / `live_raisers_behind` features
   - Surface ANY other re-raise × position interactions present that orchestrator missed

3. **Candidate features to add** (architect-hat proposes; some may overlap with AMENDMENT 1's "players left to act" candidates):
   - `street_raise_count` — int (0/1/2/3+) raises this street; replaces binary `facing_raise` with continuous escalation-level
   - `is_4bet_or_higher_pot` — binary; preflop or current-street; complements `is_3bet_pot`
   - `live_raisers_behind` — count of behind-hero villains who haven't folded yet AND have stack to raise
   - `closing_action` — binary; hero is last to act this street; turns off squeeze-risk
   - `squeeze_risk_index` — composite: live_raisers_behind × pot-already-raised × pot_size_relative_to_stacks; captures "expensive to call here, more expensive if squeezed"
   - `reverse_implied_odds_signal` — composite: facing_raise × OOP × players_behind × pot_committed_pct; captures the post-flop multiway disadvantage

   Some of these may compose with AMENDMENT 1's `players_to_act_after_hero` family — architect designs to AVOID feature collinearity (e.g., don't ship both `players_to_act_after_hero` AND `live_raisers_behind` if they're 90% correlated; choose the more discriminating one OR design as an interaction product).

4. **Pilot inclusion**:
   - Per Phase 2-B pilot scope (3 candidates), include AT LEAST ONE re-raise-interaction feature (e.g., `closing_action` or `squeeze_risk_index`) alongside D5 candidate + 4-way `players_to_act` candidate
   - Pilot gate evidence threshold per AMENDMENT 1 unchanged

5. **Implication for 4-way reference set design (2-D)**:
   - Reference hands MUST include 4-way 3-bet pots + 4-way 4-bet pots (where re-raise level + players behind matters most)
   - Reference hands MUST include closing-action vs early-action variants of similar spots (to test the model differentiates)
   - Per AMENDMENT 1's preflop+flop concentration: 3-bet/4-bet pots are mostly preflop; this aligns with the street weighting

6. **Implication for ship gate (§5)**:
   - Per-hand stay-wrong taxonomy should classify misses by whether re-raise × players-left was the discriminating signal that the model failed to extract
   - Architect proposes diagnostic categorization

## What this amendment does NOT change

- Phase 2 design-only scope (still NO build/train/corpus work)
- Same target deliverable file: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md`
- D5 blueprint refresh + 4-way feature gap analysis + sub-phase decomposition + owner-scope items + AMENDMENT 1 street-distribution analysis — all still in scope
- Pilot-first standing rule still applies
- Owner-gate ratification before build/train still required
- Solver-queue HOLD-with-accepted-risk posture unchanged

## STOP conditions (per CLAUDE.md §5)

- Architect finds existing features for re-raise × players-left interaction that orchestrator missed → REPORT in design memo (not blocking; just informs candidate proposals)
- Candidate features show severe collinearity with AMENDMENT 1 candidates that can't be resolved → STOP / REPORT; orchestrator + owner reconcile
- Re-raise × players-left signal is purely preflop (no flop+ relevance) → confirm + scope to preflop-only feature subset (not blocking; tightens design)

## Negative scope

- ❌ Does NOT change the design-only scope of Phase 2-A
- ❌ Does NOT pre-commit to specific feature definitions (architect proposes; owner ratifies)
- ❌ Does NOT change the owner-ratification gate before 2-B fires
- ❌ Does NOT supersede AMENDMENT 1; both apply

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `cee0705` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2 design dispatch: master `16a5aab` (PR #385)
- AMENDMENT 1 (street distribution): master `cee0705` (PR #386)
- D5 blueprint: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Phase 1.5 unified surface design (analog template): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_pilot_first_for_long_jobs.md`

**Status: AMENDMENT 2 folds owner's "re-raise × players-left interaction" insight into in-progress Phase 2 design memo. Architect adds §3.Y addressing GTO theory + gap verification + candidate features (`street_raise_count`, `is_4bet_or_higher_pot`, `live_raisers_behind`, `closing_action`, `squeeze_risk_index`, `reverse_implied_odds_signal`) + pilot inclusion + reference set + ship-gate implications. Same deliverable; design-only scope unchanged. Both AMENDMENT 1 + AMENDMENT 2 apply.**
