---
date: 2026-05-11
from: BUILDER (lead-programmer + architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-B RE-PILOT report — 4-candidate re-engineered (Option A); 1-seed importance evidence
status: RE-PILOT GATE PARTIAL-PASS (2/4 features clear; 1 near-miss; 1 absorbed) — orchestrator-owner decision required
---

# Phase 2-B RE-PILOT report — 4-candidate re-engineered features

## TL;DR

Per dispatch PR #396 (owner-ratified Option A): re-engineered 3 failed PILOT v1 encodings, kept the 1 proven feature, dropped 2 redundant. Surface 65→63. Re-pilot evidence: **2/4 features clear the ≥2% gate; 1 near-miss (1.87%); 1 still absorbed**. The re-engineering produced one major win (**tpmk_kicker_rank: 0% → 9.18%, rank #2 overall**) and one modest improvement, with one feature still showing collinearity with baseline.

**Orchestrator-owner decision required**: third iteration on the 2 sub-threshold features, partial-proceed with the 2 winners, or take the 2 winners as the final 2-B addition and advance to 2-C.

## Re-pilot training results — 988-corpus, seed=42

### Distribution + sanity

- **988 rows joined** (same as PILOT v1)
- **Actions**: CHECK 326 / RAISE 246 / BET 219 / CALL 100 / FOLD 97
- **All 63 features finite**, no NaN/Inf
- **Train accuracy 100%** (overfit baseline — same regularization regime as v1; comparable signal)

### Feature value distributions (sanity)

| Feature | Nonzero | Mean | Min/Max |
|---------|---------|------|---------|
| players_to_act_after_hero | 584/988 (59.1%) | 1.17 | 0 / 3 |
| tpmk_kicker_rank | 175/988 (17.7%) | 1.84 | 0 / 14 |
| broadway_pressure_multiway_facing | 131/988 (13.3%) | 0.29 | 0 / 3 |
| nut_fd_blocker_multiway | 152/988 (15.4%) | 0.15 | 0 / 1 |

### Feature importance — top 20

```
facing_bet                                  15.41%
tpmk_kicker_rank                             9.18% ← RE-PILOT
pot_odds                                     7.06%
villain_range_capped                         6.92%
equity_margin                                6.34%
worse_hand_pct                               5.53%
hand_rank                                    5.50%
villain_draw_pct                             4.71%
hand_category                                3.72%
players_to_act_after_hero                    3.36% ← RE-PILOT
flush_draw_block_pct                         3.21%
to_call                                      2.92%
is_ip                                        2.32%
board_adjusted_hrp                           2.30%
nut_made_block_pct                           2.21%
nut_fd_blocker_multiway                      1.87% ← RE-PILOT
is_strong_made                               1.67%
flush_block_pct                              1.39%
better_hand_pct                              1.11%
hero_range_percentile                        1.01%
```

### Per-feature gate evidence

| Feature | v1 importance | v2 importance | Δ | Rank | Gate (≥2%) | Verdict |
|---------|---------------|---------------|---|------|-----------|---------|
| `players_to_act_after_hero` (KEEP) | 3.58% | **3.36%** | -0.22% | #10/63 | regression check ±1% | **PASS** |
| `tpmk_kicker_rank` (RE-ENG) | 0.00% (v1: tpmk_position_with_kicker_strength) | **9.18%** | +9.18% | **#2/63** | ≥2% | **PASS** |
| `nut_fd_blocker_multiway` (RE-ENG) | 1.53% (v1: nut_fd_multiway_pressure_with_blocker) | 1.87% | +0.34% | #16/63 | ≥2% | **FAIL (narrowly; +22% relative)** |
| `broadway_pressure_multiway_facing` (RE-ENG) | 0.00% (v1: broadway_density_completed_on_turn) | 0.26% | +0.26% | #41/63 | ≥2% | **FAIL** |

**Overall: 2/4 features pass (50%). Dispatch §"Re-pilot gate outcome": 2/4 → REPORT for orchestrator triage.**

## Interpretation (gto-expert + ml-architect)

### Wins

1. **`tpmk_kicker_rank` is a major win — 0% → 9.18%, rank #2 overall.** It beats pot_odds, equity_margin, worse_hand_pct, hand_rank, even hand_category itself. The numeric kicker continuum carries strong, novel signal that the J-high × hand_category × hand_rank composite buried. Validates architect hypothesis: "numeric kicker carries more information than J-high-Boolean × hand_rank/10".

2. **`players_to_act_after_hero` regression-checked clean.** v1: 3.58% → v2: 3.36% (within ±1% gate). AMENDMENT 1 owner-direct feature confirmed stable across pilot runs.

### Near-misses + failures

3. **`nut_fd_blocker_multiway` (1.87%) is a near-miss with directional confirmation.** Dropping the `facing_bet` gate raised importance from 1.53% to 1.87% (+22% relative). The signal is real but the model still absorbs most of it through `nut_made_block_pct` (2.21%) + `flush_draw_block_pct` (3.21%). Could potentially clear 2% with a *third* iteration:
   - Try `has_FD × nut_block` (drop multiway too — let model combine with `num_opponents`)
   - Try interaction with `villain_air_pct` (the "do they fold?" component, not "is hero IP?")
   - Try unconditional nut-FD-with-blocker (without `has_flush_draw` gate)

4. **`broadway_pressure_multiway_facing` (0.26%) improved but remains absorbed.** The composite at the decision boundary helped (0% → 0.26%) but baseline `high_card_rank` + `danger_score` + `is_paired` continue to absorb the variance. Possible third iteration:
   - Try Q+J+T-specific indicator (the actual problematic turn type from MW-45)
   - Try interaction with `villain_top_pair_plus_pct` (range pressure axis)
   - Architect now suspects broadway is genuinely baseline-absorbed; this axis may need a *different feature* not a different encoding

### What we now know

- **D5 axis encoding matters more than D5 axis selection.** MW-40 (TPMK) went from 0% to 9.18% with the same underlying axis — just a different encoding. This is the single biggest learning.
- **MW-47 (nut FD with blocker) is real but narrow.** Architect underestimated baseline absorption.
- **MW-45 (broadway pressure) is likely baseline-absorbed at any encoding short of a fundamentally different axis.** Pilot evidence supports dropping MW-45 from 2-B scope entirely.

## What this evidence supports

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: REPORT, don't improvise next direction.

### Options for orchestrator-owner decision

**Option A2 — Third iteration on the 2 sub-threshold features** (~3-5h)
- `nut_fd_blocker_multiway` → try alternate encodings (drop multiway gate; try nut_block × villain_air_pct interaction)
- `broadway_pressure_multiway_facing` → either swap to QJT-specific indicator OR accept that MW-45 is baseline-absorbed and drop entirely
- Re-pilot 4 features again
- **Recommended for nut_fd (real signal, +22% trajectory).** Not recommended for broadway (likely fundamental absorption).

**Option B — Partial-proceed with 2 confirmed winners** (recommended per quality default + scope discipline)
- Promote `players_to_act_after_hero` + `tpmk_kicker_rank` to 2-C/D refresh
- Drop `nut_fd_blocker_multiway` (1.87% real but absorbed by baseline blocker features)
- Drop `broadway_pressure_multiway_facing` (0.26% baseline-absorbed)
- Surface lands at 61 (59 baseline + 2 confirmed)
- **Saves ~3-5h of re-pilot iteration; uses the strongest empirical evidence available**

**Option C — Mixed: ship 2 winners + iterate 1** (compromise)
- Promote `players_to_act_after_hero` + `tpmk_kicker_rank` to 2-C/D
- Third iteration ONLY on `nut_fd_blocker_multiway` (single-feature pilot, ~1-2h)
- Drop `broadway_pressure_multiway_facing` permanently
- Surface lands at 62 or 63 depending on third-iteration outcome

**My architect-hat lean: Option B.** The 2 winners (one PASS, one breakthrough 9.18%) are a clear ship-net positive. The `nut_fd` near-miss is real but absorbed; chasing 0.13% more importance through a third iteration is unlikely to clear the gate. The `broadway_pressure` feature is fundamentally absorbed — drop it. Phase 2-C/D delivers concrete value with these 2 features, and the orchestrator can revisit the failed axes in a future phase if new evidence demands it. This aligns with `feedback_quality_default_no_ask.md` (no half-finished implementations) + `feedback_pilot_first_for_long_jobs.md` (don't iterate past diminishing returns).

## Risks + caveats

- **1-seed result**: importance scores can shift ±0.5–1% across seeds. The 9.18% / 3.36% / 1.87% / 0.26% spread is large enough that seed variance won't flip the gate verdicts on the 2 winners or the 2 failures, but could push nut_fd above/below 2% gate. Multi-seed would harden the evidence if owner wants higher confidence.
- **HU-heavy corpus**: 988-corpus is ~75% HU. The 4-way / D5 features have fewer training examples; importance may be under-counted in this corpus. The 9.18% tpmk_kicker_rank result is even more impressive in this light — it's already winning despite being multiway-relevant in a HU-heavy corpus.
- **Train accuracy 100% on 988 rows**: overfit; same caveat as v1. Real signal validation requires CV / held-out eval (2-C scope).

## Compliance with dispatch (TC-X-DISPATCH-COMPLIANCE checklist)

- ✅ Owner-ratified Option A — re-engineered 3 failed encodings (no deviation)
- ✅ Kept `players_to_act_after_hero` unchanged (PILOT v1)
- ✅ Dropped `multiway_equity_realization_factor` + `closing_action`
- ✅ Each re-engineered candidate is semantically different from PILOT v1 predecessor (architect-attested + Step 18 docstring records the v1→v2 delta)
- ✅ `FEATURE_COLUMNS` shrinks 65 → 63; last 4 are re-pilot features
- ✅ First 59 unchanged; production-surface integrity preserved (`test_first_59_match_canonical` PASS)
- ✅ `inference_path_59.py` canonical 59 tuple UNCHANGED
- ✅ `train_model_v9_student.py` UNCHANGED (already on canonical import)
- ✅ NO oracle_router edits; NO data/corpus edits; NO model artifact production; NO solver-queue drain
- ✅ 17/17 unit tests on re-pilot features PASS
- ✅ Non-NaN/Inf on 988/988 corpus rows
- ✅ Importance values numeric + recorded per-feature
- ✅ Honest reporting of 2/4 gate verdict (no mis-report)
- ✅ STOP-condition compliance: hit 2/4 → did NOT improvise third iteration; surfacing for owner direction

## Files in this PR

- `river-rats-core/feature_extractor.py` — Step 18 replaced (4 features instead of 6)
- `river-rats-core/feature_keys.py` — 4 F constants instead of 6
- `river-rats-core/tests/test_phase2b_pilot_features.py` — rewritten (17 tests; 4 feature classes + surface-aggregate class)
- `river-rats-core/train_pilot_2b.py` — rewritten for 63-feature surface + 4-feature gates
- `review/comms/PILOT_2B_REPILOT_FEATURE_IMPORTANCE_2026-05-11.json` — full importance dump
- `review/comms/BUILDER_REPORT_PHASE2B_REPILOT_2026-05-11.md` — this report

## Pre-push checks

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a668002` ✓
- Diff scope: 6 files (matches builder report)
- All 17 new tests pass on `tests/test_phase2b_pilot_features.py`
- Production surface integrity preserved (`test_first_59_match_canonical`)

## STOP / awaiting

Per dispatch §STOP-conditions + §"Re-pilot gate outcome dispatching" 2/4 row: REPORT to orchestrator. Not improvising Option A2 third iteration without explicit direction.

## References

- Dispatch (Option A re-pilot): `MAIN_TERMINAL_PHASE2B_REPILOT_DISPATCH_2026-05-11.md` (master `a668002`, PR #396)
- PILOT v1 builder PR: master `fa0ea24` (PR #393)
- PILOT v1 QC verdict PASS: master `cfadc34` (PR #395)
- PILOT v1 builder report: `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md`
- Design memo: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` (PR #388)
- AMENDMENTS 1+2+3 folded
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_branch_base_verification.md`
