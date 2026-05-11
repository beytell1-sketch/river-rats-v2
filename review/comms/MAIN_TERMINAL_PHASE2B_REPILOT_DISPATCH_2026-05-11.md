---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-direction)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: Phase 2-B RE-PILOT — keep 1 proven feature; re-engineer 3 failed encodings; drop 2 redundant; 4-candidate re-pilot per Option A (owner-ratified)
status: DISPATCH — fire now (Phase 2-B PILOT merged at master cfadc34; PR #393 + #395 PASS; owner ratified Option A re-engineer + re-pilot 2026-05-11 ~06:58 SAST)
---

# Phase 2-B RE-PILOT dispatch — 4-candidate re-engineered pilot

## Owner ratification record (2026-05-11 ~06:58 SAST)

Owner answered AskUserQuestion "Phase 2-B pilot: 1/6 features pass — how to proceed?" with:

**"A — Re-engineer + re-pilot (Recommended)"**

Locks the following direction:
- KEEP `players_to_act_after_hero` (proven novel signal at 3.58% importance, rank #10/65; AMENDMENT 1 validated)
- RE-ENGINEER 3 failed encodings with stronger formulations
- DROP 2 redundant (multiway_equity_realization_factor + closing_action; the model already constructs equivalent splits from baseline `num_opponents` + `is_ip`)
- Re-run 1-seed pilot → re-evaluate gates per design memo §3.4 + §3.Y.4

## Re-pilot candidate set (4 total)

### KEEP from PILOT v1 (1 feature; no implementation change)

| Feature | Status | Source | PILOT v1 result |
|---------|--------|--------|------------------|
| `players_to_act_after_hero` | KEEP unchanged | AMENDMENT 1 (PR #386) | 3.58% importance, rank #10/65 — gate PASS |

### RE-ENGINEER (3 features; new encodings)

#### Candidate 1 — TPMK kicker (re-engineered from `tpmk_position_with_kicker_strength`)

- **Original (PILOT v1)**: `hand_category × J-high × hand_rank/10`. Result: 0.00% importance, rank #62/65. Too narrow (only 5.4% nonzero; constrained to J-high).
- **Re-engineered**: use **absolute kicker rank** as a numeric feature, NOT Boolean × J-high. Architect picks specific encoding (e.g., `hand_category == TPMK ? kicker_rank : 0` where kicker_rank ∈ {2..14}).
- **Hypothesis**: numeric kicker carries more information than J-high-Boolean × hand_rank/10; reduces collinearity with hand_category + high_card_rank.

#### Candidate 2 — Broadway density composite (re-engineered from `broadway_density_completed_on_turn`)

- **Original (PILOT v1)**: `count(broadway cards on board) if turn else 0`. Result: 0.00% importance, rank #63/65. Redundant with high_card_rank + danger_score + is_paired.
- **Re-engineered**: compress to **composite at real decision boundary**: `broadway_turn × multiway × facing_bet` (binary or numeric composite). Concentrate signal where the spot type actually matters.
- **Hypothesis**: signal exists at the intersection (multiway turn flop with broadway texture + decision pressure), not at the marginal broadway-count level.

#### Candidate 3 — Nut FD MW blocker without facing_bet gate (re-engineered from `nut_fd_multiway_pressure_with_blocker`)

- **Original (PILOT v1)**: `has_FD × nut_block × multiway × facing_bet`. Result: 1.53% importance, rank #17/65 (near-miss; below 2% gate). The `facing_bet` gate collapses signal in CHECK spots where the same axis still matters.
- **Re-engineered**: drop the `facing_bet` gate → `has_FD × nut_block × multiway`. Let the model see signal in CHECK spots too; the model can re-combine with `facing_bet` if needed.
- **Hypothesis**: removing the facing_bet gate roughly doubles the nonzero rate + lets the signal show in the broader spot class; should push above 2%.

### DROP from PILOT v1 (2 features; will NOT be in re-pilot)

| Feature | Reason | PILOT v1 result |
|---------|--------|------------------|
| `multiway_equity_realization_factor` | Perfect collinearity with `num_opponents` (lookup table). Model already constructs equivalent splits. | 0.00% importance, rank #64/65 |
| `closing_action` | Near-perfect collinearity with `is_ip` (HU) + `is_ip × players_to_act_after_hero=0` (multiway). Model already constructs equivalent splits. | 0.00% importance, rank #65/65 |

These are NOT in re-pilot. Surface size returns to 59 + 4 = **63** post re-pilot (was 65 with the dropped 2).

## Implementation deliverables (per design memo §5.2; ~3-5h estimate per builder option A)

1. **Feature implementation** in `river-rats-core/feature_extractor.py`:
   - 3 re-engineered features (tpmk-kicker, broadway-composite, nut_fd-no-gate) replace the originals in Step 18
   - 2 dropped features removed from Step 18
   - `players_to_act_after_hero` UNCHANGED
   - `FEATURE_COLUMNS` shrinks 65 → 63 (rebuild canonical order; last 4 are pilot features in order)
2. **`river-rats-core/feature_keys.py`**:
   - 3 F-class constants updated to reflect new encodings (rename if semantically different)
   - 2 F-class constants removed (for dropped features)
   - 1 F-class constant unchanged (`players_to_act_after_hero`)
3. **`river-rats-core/inference_path_59.py`**:
   - canonical 59 frozen tuple UNCHANGED (first 59 entries are production surface; do NOT touch)
   - re-pilot extension to 63 does NOT change first-59
4. **`river-rats-core/train_model_v9_student.py`**:
   - UNCHANGED (already imports from inference_path_59.FEATURE_COLUMNS_59; trainer behavior preserved)
5. **Tests**:
   - Update `test_phase2b_pilot_features.py`: drop 2 tests for dropped features; rewrite 3 tests for re-engineered features; keep 1 test for `players_to_act_after_hero`
   - Surface-size sanity: `len(FEATURE_COLUMNS) == 63`; last 4 are re-pilot features
6. **Re-pilot trainer**: re-use `train_pilot_2b.py` if compatible; rename to `train_pilot_2b_v2.py` if needed
7. **Re-pilot importance JSON**: `review/comms/PILOT_2B_REPILOT_FEATURE_IMPORTANCE_2026-05-11.json`
8. **Re-pilot report**: `review/comms/BUILDER_REPORT_PHASE2B_REPILOT_2026-05-11.md`

## Re-pilot gate criteria (per design memo §3.4 + §3.Y.4)

For each re-engineered candidate, evaluate against the same gates:

| Feature | Gate | Pass condition |
|---------|------|----------------|
| `players_to_act_after_hero` | 4-way ≥2% | Already PASS; verify regression (re-pilot importance ≈ 3.58% ±1%) |
| Re-engineered tpmk-kicker | D5 ≥2% | New encoding clears 2% importance + ≥1 stay-wrong graduation on D5 reference |
| Re-engineered broadway-composite | D5 ≥2% | New encoding clears 2% + ≥1 stay-wrong graduation |
| Re-engineered nut_fd-no-gate | D5 ≥2% | New encoding clears 2% + ≥1 stay-wrong graduation |

### Re-pilot gate outcome dispatching

| Outcome | Action |
|---------|--------|
| 4/4 pass (3 re-engineered clear; `players_to_act` regression OK) | PROCEED to 2-C (full feature implementation; ~12 candidates remaining from §4 of design memo) |
| 3/4 pass (1 re-engineered still fails) | REPORT to orchestrator; orchestrator triages partial-proceed vs further iteration |
| 2/4 pass (2 re-engineered fail) | REPORT; likely further owner-direction needed (Option A2 = third iteration? OR Option B = partial-proceed-with-2?) |
| ≤1/4 pass (broad fail again) | HALT 2-C; escalate to "is the issue elsewhere" investigation per design memo §3.4 |

## What this re-pilot does NOT do

Per design memo §5 + §7 + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT implement remaining ~12 candidates from §4 (2-C scope; awaits re-pilot gate clear)
- ❌ Does NOT touch `oracle_router.py` (model swap is 2-H)
- ❌ Does NOT build the 4-way reference set (2-D scope)
- ❌ Does NOT generate or label corpus (2-E scope; 2-E.0 labeller readiness gate first)
- ❌ Does NOT retrain production models (2-F + 2-G)
- ❌ Does NOT modify `inference_path_59.py` canonical 59 tuple
- ❌ Does NOT drain solver-verification queue (HOLD per 6.4 ratified)

## STOP conditions (per CLAUDE.md §5)

- 3 re-engineered features can't be implemented per spec → STOP / REPORT (e.g., kicker rank semantics ambiguous)
- Re-pilot trainer fails (non-NaN/Inf assertion fails) → STOP / REPORT
- TC-23 EXISTENCE on new feature_extractor changes: every new feature must be git-tracked
- TC-X-OWNER-SCOPE-DISCIPLINE: NO deviation from owner-ratified Option A direction; deviation requires REPORT + new dispatch
- Wall-clock blows past ~7h (3-5h estimate + 40% buffer) → REPORT
- If `players_to_act_after_hero` importance regresses substantially (drops below 2.5% from prior 3.58%) → REPORT; may indicate corpus or trainer-config issue

## QC stream — what you audit (pre-merge milestone for Phase 2-B re-pilot PR)

Per `feedback_qc_required_before_approval.md`:

1. **Diff scope** (TC-23): feature_extractor.py + feature_keys.py + test_phase2b_pilot_features.py + train_pilot_2b{_v2}.py + JSON + report
   - NO oracle_router edits; NO data edits; NO trainer-arch changes; NO inference_path_59 canonical change; NO model files
2. **Surface size**: `len(FEATURE_COLUMNS) == 63`; first 59 unchanged; last 4 are re-pilot features
3. **Re-engineered candidate verification**: each re-engineered candidate IS semantically different from its PILOT v1 predecessor (architect picks encoding; verify it's not just a rename of the same logic)
4. **Per-feature unit tests**: 4/4 PASS (1 kept + 3 re-engineered)
5. **Non-NaN/Inf on 988-corpus**: 988/988 finite
6. **Re-pilot trainer report**:
   - All 4 features' importance values + ranks recorded
   - `players_to_act_after_hero` importance ≈ 3.58% ±1% (regression check)
   - Re-engineered candidate importance values numeric + non-NaN
   - Pilot gate evidence per Re-pilot gate table above
7. **TC-X-DISPATCH-COMPLIANCE**: all directives honored
8. **Honest reporting**: builder DOES NOT mis-report gate evidence

## What gates

- Builder Phase 2-B re-pilot PR → QC trigger when pushed
- On QC PASS + re-pilot gate clear (4/4 pass) → orchestrator merges + dispatches 2-C
- On 3/4 or 2/4 → orchestrator triages; may surface to owner
- On ≤1/4 → HALT; escalate to "is the issue elsewhere" investigation; may need replan dispatch
- STOP condition → REPORT; orchestrator triages

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `cfadc34` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-B PILOT v1 builder PR: master `fa0ea24` (PR #393)
- Phase 2-B PILOT v1 QC verdict PASS: master `cfadc34` (PR #395)
- Phase 2-B PILOT v1 dispatch: master `e69c724` (PR #392)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- Phase 2 design AMENDMENTS 1+2+3: masters `cee0705` / `596bb89` / `3763d8a`
- PILOT v1 builder report: `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md`
- PILOT v1 importance JSON: `review/comms/PILOT_2B_FEATURE_IMPORTANCE_2026-05-11.json`
- Design memo §3.4 pilot gate strategy: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` lines 495-510
- Stay-wrong taxonomy: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`
- Pilot-first standing rule: `~/.claude/projects/-home-rupertbeytell/memory/feedback_pilot_first_for_long_jobs.md`
- Quality default standing rule: `~/.claude/projects/-home-rupertbeytell/memory/feedback_quality_default_no_ask.md`
- Solver-queue posture: `~/.claude/projects/-home-rupertbeytell/memory/feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_attention_flags_when_features_change.md`, `feedback_bucket_first_labelling.md`

**Status: Phase 2-B RE-PILOT dispatch per owner-ratified Option A. 4-candidate re-pilot (1 kept + 3 re-engineered with stronger encodings; 2 dropped as collinearity-redundant). Surface 65→63. Re-engineered candidates target D5 ≥2% gate. Pilot+full split standing rule still applies (2-C blocked until re-pilot gate clears). Builder fires re-implementation + 1-seed re-pilot trainer + per-feature importance + gate evidence. NO 2-C work until gate clears.**
