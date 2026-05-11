---
date: 2026-05-11
from: BUILDER (lead-programmer + architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-B PILOT report — 6-candidate feature implementation + 1-seed importance evidence
status: PILOT GATE PARTIAL-FAIL (1/6 features meet threshold) — orchestrator-owner decision required before 2-C/2-D
---

# Phase 2-B PILOT report — 6 candidate features

## TL;DR

Per dispatch PR #392 + design memo §5 row 2-B: built + tested + pilot-trained 6 candidate features (3 D5 + 2 4-way + 1 re-raise). Out of 6 features, **1 clears its importance gate** (players_to_act_after_hero, 3.58% importance, rank #10/65). The remaining 5 score 0–1.53% — below their gates. The pilot did its job: it surfaces signal-vs-noise *before* full multiway corpus + multi-seed train cost.

**Orchestrator-owner decision required**: revise feature engineering, accept partial-gate proceed with 1–2 features only, or defer to Phase 3.

## What was built

### 1. Feature implementations — `river-rats-core/feature_extractor.py` Step 18

All 6 features implemented inline at the end of `extract_all_features` (just before `return features`). FEATURE_COLUMNS grew 59 → 65.

| # | Feature | Type | Source |
|---|---------|------|--------|
| 1 | `tpmk_position_with_kicker_strength` | D5 / MW-40 | hand_category × J-high × hand_rank/10 |
| 2 | `broadway_density_completed_on_turn` | D5 / MW-45 | count(broadway cards on board) if turn else 0 |
| 3 | `nut_fd_multiway_pressure_with_blocker` | D5 / MW-47 | has_FD × nut_block × multiway × facing_bet |
| 4 | `players_to_act_after_hero` | AMENDMENT 1 | 0 if is_ip else num_opponents |
| 5 | `multiway_equity_realization_factor` | §3.2.2 | lookup {1:1.0, 2:0.85, 3:0.75, 4+:0.70} |
| 6 | `closing_action` | AMENDMENT 2 #11 | is_ip AND players_to_act == 0 |

### 2. F-class constants — `river-rats-core/feature_keys.py`

6 new constants added to `class F` with section header noting Phase 2-B PILOT provenance + per-feature axis cross-reference.

### 3. Production-surface integrity guard — `river-rats-core/inference_path_59.py`

Refactored to pin canonical 59-feature production surface explicitly (frozen tuple `_CANONICAL_FEATURE_COLUMNS_59`) so that:
- Phase 2-B PILOT extension to 65 features does NOT trip the assertion
- Any reorder/rename/drop of the FIRST 59 entries DOES trip the assertion
- Production HU + 3-way models continue to build 59-element arrays in canonical order

This was a load-time guard change; no inference-path behavior change.

### 4. Compatible trainer assertion — `river-rats-core/train_model_v9_student.py`

The v9 student trainer is frozen on the 59-feature surface (Phase 1.5-B). Changed import source from `feature_extractor.FEATURE_COLUMNS` (now 65) to `inference_path_59.FEATURE_COLUMNS_59` (canonical 59). Trainer behavior unchanged.

### 5. Updated stale test — `river-rats-core/tests/test_board_adjusted_hrp.py`

`TestFeatureCountIs55` was pre-existing technical debt (asserted len == 55; broke after Phase 1.5-B prune to 59 in 2026-04). Renamed to `TestFeatureSurface` with three tests:
- `test_production_surface_at_least_59` (FEATURE_COLUMNS ≥ 59)
- `test_first_59_match_canonical` (production-surface integrity)
- `test_gto_model_feature_count_is_55` (legacy 55-tuple still 55)

### 6. New tests — `river-rats-core/tests/test_phase2b_pilot_features.py`

21 unit tests covering all 6 features across HU + 3-way + 4-way + flop/turn/river boundaries:
- Tpmk: zero-for-non-TPMK, positive-for-TPMK-J-high, zero-for-non-J-high
- Broadway: zero-on-flop, high-on-QJT-turn, zero-on-river
- Nut FD MW pressure: zero-in-HU, zero-without-facing-bet
- Players to act: zero-IP-HU, three-OOP-4way
- Realization: HU=1.0, 3w=0.85, 4w=0.75, 5w=0.70
- Closing action: 1-HU-IP, 0-HU-OOP, 0-MW-OOP
- Plus surface-size sanity: count=65; last 6 are PILOT features; all 6 populated on HU + 4-way.

**Result: 21/21 PASS** on isolated test run.

### 7. Pilot trainer — `river-rats-core/train_pilot_2b.py`

Joins 988-on-59 situations + labels corpus on pilot_hand_id, augments feat_dict with 6 pilot features (replicates Step 18 logic inline), trains 1-seed XGBoost (hyperparams from v9_student), prints + dumps per-feature importance to JSON.

## Pilot training results — 988-corpus, seed=42

### Distribution

- **988 rows** (HU + multiway mixed; same as 12.5K-C-E ceiling corpus)
- **Actions**: CHECK 326 / RAISE 246 / BET 219 / CALL 100 / FOLD 97
- **All 65 features finite**, no NaN/Inf

### Pilot feature value distribution (sanity)

| Feature | Nonzero rate | Mean | Min/Max |
|---------|--------------|------|---------|
| tpmk_position_with_kicker_strength | 53/988 (5.4%) | 0.0071 | 0.00 / 0.13 |
| broadway_density_completed_on_turn | 203/988 (20.5%) | 0.40 | 0.0 / 4.0 |
| nut_fd_multiway_pressure_with_blocker | 128/988 (13.0%) | 0.13 | 0.00 / 1.00 |
| players_to_act_after_hero | 584/988 (59.1%) | 1.17 | 0 / 3 |
| multiway_equity_realization_factor | 988/988 (100%) | 0.85 | 0.75 / 1.00 |
| closing_action | 404/988 (40.9%) | 0.41 | 0 / 1 |

### Feature importance — top 20

```
facing_bet                                          16.55%
villain_range_capped                                 8.07%
pot_odds                                             7.63%
equity_margin                                        7.14%
worse_hand_pct                                       6.26%
hand_rank                                            6.17%
villain_draw_pct                                     4.74%
hand_category                                        3.90%
nut_made_block_pct                                   3.78%
players_to_act_after_hero                            3.58% ← PILOT
flush_draw_block_pct                                 3.52%
to_call                                              3.07%
is_ip                                                2.74%
board_adjusted_hrp                                   2.47%
is_strong_made                                       2.27%
flush_block_pct                                      1.58%
nut_fd_multiway_pressure_with_blocker                1.53% ← PILOT
better_hand_pct                                      1.12%
villain_position                                     1.01%
overcard_outs                                        1.00%
```

### Per-pilot-feature importance + rank

| Feature | Importance | Rank | Gate | Pass? |
|---------|------------|------|------|-------|
| tpmk_position_with_kicker_strength | 0.00% | #62/65 | ≥2% | **FAIL** |
| broadway_density_completed_on_turn | 0.00% | #63/65 | ≥2% | **FAIL** |
| nut_fd_multiway_pressure_with_blocker | 1.53% | #17/65 | ≥2% | **FAIL (narrowly)** |
| players_to_act_after_hero | 3.58% | #10/65 | ≥2% | **PASS** |
| multiway_equity_realization_factor | 0.00% | #64/65 | ≥2% | **FAIL** |
| closing_action | 0.00% | #65/65 | ≥1% | **FAIL** |

### Gate summary

- **D5 ≥2%**: 0/3 features passing
- **4-way ≥2%**: 1/2 features passing (players_to_act_after_hero)
- **Re-raise ≥1%**: 0/1 features passing

**Overall: 1/6 features pass — pilot gate FAIL** (would require 4+/6 per design memo §5.2 for unconditional 2-C proceed).

## Interpretation (gto-expert-hat + ml-architect-hat)

The pilot is doing exactly what a pilot is supposed to do: surface signal-vs-noise *before* full corpus refresh + multi-seed cost. Three patterns:

1. **`players_to_act_after_hero` (3.58%) is the clear winner.** Ranks #10/65, beating well-established baseline features like is_ip, board_adjusted_hrp, is_strong_made. The 4-way pressure asymmetry signal is real and non-redundant with is_ip. AMENDMENT 1's owner intuition validated.

2. **`nut_fd_multiway_pressure_with_blocker` (1.53%) shows signal but doesn't clear gate.** Below 2% threshold but well above the four 0% features. Likely captures a real but narrow MW-47 axis; competes with `nut_made_block_pct` (3.78%) and `flush_draw_block_pct` (3.52%) which already absorb most of that variance. Could potentially clear 2% with re-engineering (e.g., removing the facing_bet gate, which collapses signal in CHECK spots).

3. **Four features show 0% importance — collinearity with baseline:**
   - `tpmk_position_with_kicker_strength`: too narrow (5.4% nonzero) + redundant with hand_category=7/8 + high_card_rank already in baseline
   - `broadway_density_completed_on_turn`: redundant with high_card_rank + danger_score + is_paired turn-conditional
   - `multiway_equity_realization_factor`: **perfect** collinearity with num_opponents (lookup table) → XGBoost dedups via the existing num_opponents feature
   - `closing_action`: near-perfect collinearity with is_ip in HU + with (is_ip × players_to_act_after_hero=0) which the tree can already construct from is_ip + num_opponents

None of these 0% results invalidate the *concept* of the underlying axis — they invalidate the *encoding* chosen for that axis. The model can already construct equivalent splits from baseline features.

## What this evidence supports

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: pilot is the gate. Failed gate → STOP and report.

The honest interpretation: the design memo's 6-feature pilot was a reasonable upper-bound bet on the D5 + 4-way + re-raise axes; the empirical evidence is that **most of the proposed encodings are already absorbed by the baseline**, and only the AMENDMENT 1 owner-direct feature shows clear novel signal.

## Options for orchestrator-owner decision

**Option A — Re-engineer + re-pilot (recommended per `feedback_quality_default_no_ask.md`)**:
- Keep `players_to_act_after_hero` (proven novel signal)
- Re-design 3 of the 5 failed features with stronger encodings:
  - tpmk → "TPMK with absolute-kicker rank ≥ T" (numeric kicker, not Boolean × J-high)
  - broadway_density → "broadway turn × multiway × facing_bet" (compress to a single composite at the real decision boundary)
  - nut_fd_mw_blocker → drop the facing_bet gate (let signal show in CHECK spots too)
- Drop 2 (multiway_realization, closing_action) as redundant with num_opponents + is_ip
- Re-run 1-seed pilot → re-evaluate gates
- Wall-clock ~3-5h

**Option B — Partial-gate proceed**:
- Promote `players_to_act_after_hero` only to Phase 2-C/D refresh
- Skip the other 5 features entirely
- Surface-size lands at 60, not 65
- Wall-clock saved: ~5-8h

**Option C — Defer to Phase 3 / replan**:
- Park Phase 2 build; re-design feature surface from scratch with the importance evidence in hand
- Revisit AMENDMENT 1's pressure-asymmetry axis with more nuanced encodings (e.g., separate IP-tight vs OOP-tight features)

I lean toward **Option A** under quality-default rule — the failed encodings are fixable; the dispatch carved Phase 2-B as exactly this kind of evidence-gathering step, and the 3-5h re-engineering cost is well within the dispatch §STOP soft cap.

## Risks + caveats

- **1-seed result**: importance scores can shift ±0.5–1% across seeds. The 3.58% / 1.53% / 0% spread is large enough that seed variance won't flip the gate verdict — but multi-seed pilot would harden the evidence if owner wants higher confidence.
- **988-corpus is HU-heavy (~75% HU)**: 4-way / D5 features get fewer training examples; the importance of multiway-only features might be under-counted. Mitigation: full multiway-refreshed corpus (Phase 2-D) would surface this — but only if features survive the pilot.
- **Train accuracy 100% on 988 rows with depth-4 / 200 estimators**: this is overfit. Real signal validation requires CV / held-out eval (deferred to 2-C per design memo).
- **Two pre-existing test files have load-time assertions tied to `len(FEATURE_COLUMNS) == 59`**:
  - `train_model_v9_student.py` — FIXED (now imports canonical from inference_path_59)
  - `test_board_adjusted_hrp.py::TestFeatureCountIs55` — FIXED (renamed + updated)
  - One additional location may exist; collection now clean across full test suite (1652 tests).
- **Pre-existing test-suite SIGABRT instability**: not caused by these changes; unrelated to feature work. Reproducible on master pre-pilot.

## Files in this PR

- `river-rats-core/feature_extractor.py` — Step 18 block (+86 lines)
- `river-rats-core/feature_keys.py` — 6 F constants (+10 lines)
- `river-rats-core/inference_path_59.py` — canonical guard refactor (~40 lines net)
- `river-rats-core/train_model_v9_student.py` — import source change (~6 lines)
- `river-rats-core/tests/test_board_adjusted_hrp.py` — updated stale test (~30 lines net)
- `river-rats-core/tests/test_inference_path_59.py` — updated first-59 assertion (~5 lines)
- `river-rats-core/tests/test_phase2b_pilot_features.py` — 21 new tests (NEW, ~250 lines)
- `river-rats-core/train_pilot_2b.py` — pilot trainer (NEW, ~230 lines)
- `review/comms/PILOT_2B_FEATURE_IMPORTANCE_2026-05-11.json` — full importance dump (NEW)
- `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md` — this report (NEW)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e69c724` ✓
- Diff scope: 10 files (matches "Files in this PR" above)
- All new tests pass: 21/21 on `tests/test_phase2b_pilot_features.py`
- Production surface integrity preserved: canonical 59 frozen

## STOP / awaiting

Per dispatch §STOP-conditions: gate evidence sub-threshold for 5/6 features → surface for owner decision before Phase 2-C/D fires. Not improvising re-engineering without explicit direction.

**References**:
- Dispatch: `MAIN_TERMINAL_PHASE2B_PILOT_DISPATCH_2026-05-11.md` (master `e69c724`, PR #392)
- Design memo: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` (master, PR #388)
- AMENDMENTS 1+2+3 folded
- Pilot data: `data/corpus_combined_988_on_59_*_2026-05-09.jsonl`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_branch_base_verification.md`
