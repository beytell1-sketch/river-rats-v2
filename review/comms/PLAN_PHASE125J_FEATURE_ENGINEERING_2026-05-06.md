---
date: 2026-05-06
from: LEAD-PROGRAMMER (architect hat)
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5J-A — feature engineering design (3 candidate features: 2 for MW-17 axis, 1 for MW-47 axis); Direction-X-retro scope; 5-point cascade per feedback_attention_flags_when_features_change.md
status: DESIGN — PR open, ready for QC trigger
branch: programmer/phase125j-a-design-2026-05-06
base: master `c536c30`
---

# 12.5J-A — feature engineering design (C path)

## §1 Authority chain

- 12.5H-F synthesis owner gate (PR #191): owner picked **E** → **C+D parallel** compound
- 12.5I-pre diagnostic (PR #193) per-hand verdicts assigned 2 hands to C path:
  - **MW-17**: E-FEATURE primary; margin +0.843 (FOLD vs CALL); v9-3way-v2.2 has NO `nut_flush_block` in top-15; counterfactual ablation shows no realistic perturbation flips toward CALL; needs encoded features for implied-odds + nut-blocker-with-overcards-on-zero-FD-outs reasoning
  - **MW-47**: E-FEATURE primary; margin +0.910 to corrected RAISE (model agrees with raw expert CALL); v3.4 Fix 2.1.1 protocol-level carve-out works at labeller layer but doesn't transfer to model; needs feature-layer equivalent of clause-e (bet+call-multiway-with-NFD+blocker-OOP raise pressure)
- 12.5J dispatch (PR #196): per-axis feature design (recommend ≥2 candidates with trade-offs); 3-4 week multi-phase workstream; Direction-X-retro scope (Path Y intentionally relaxed; owner approved at 12.5H-F)

## §2 Direction-X-retro scope warning

Per `feedback_attention_flags_when_features_change.md`, feature changes REQUIRE matching cascade through 5 surfaces:

1. **Raw feature**: `feature_extractor.py` + `feature_keys.py` — new feature(s) added to 59-surface
2. **Attention vocabulary**: `assemble_pilot_data.py` (and any related attention-flag scripts) — new attention vocab entries
3. **Prompt rules**: `prompts/gto_labeller_v3.X.md` — IF new features should appear in labeller bucket reasoning (per §5 below, my recommendation is NO — features are model-side discriminators, not labeller-side rules)
4. **Capture pipeline**: existing 694-hand corpus + 12.5I corpus when it ships — re-extract with new feature values (no re-labelling; only feat_dict augmentation)
5. **Trainer**: `train_model_v9_student.py` + Path Y `_StudentInference` mirror updated for new feature count (60+ if 1 feature added; 62 if 3 features); `_StudentInferenceLike45` invariant test re-baselined

**This is multi-week scope.** Owner approved at 12.5H-F. Slow-quality default applies throughout. Rough timeline: design (this comm) → implementation 1 week → re-extraction + invariant tests 3-4 days → integration test 3-4 days = ~3 weeks excluding 12.5K combined re-train.

## §3 Feature design — MW-17 axis (implied-odds + nut-blocker on zero-FD-outs hands)

### MW-17 failure mechanism (per 12.5I-pre diagnostic)

Hero AdKs on Jd8d4c facing CO bet 5bb HU after BTN folds. Key features in v9-3way-v2.2 inference:
- `raw_equity=0.234` (model sees low equity)
- `pot_odds≈0.367` (high — to_call 33 / pot 90)
- `equity_margin=-0.13` (negative; hero behind pot odds)
- `better_hand_pct=0.597` (model sees hero behind 60%)
- `to_call=33` weighted very high in v9-3way-v2.2 (importance 0.091)

Model predicts FOLD with 0.889 confidence. To shift to CALL the model needs encoded features that capture:
- **Implied odds**: hero's overcards (A, K) provide future-card outs to TPTK/TPGK. Backdoor diamonds (Ad + 2 board diamonds = 3 of suit; runner-runner FD has small probability). Combined ≥6 overcard outs + ~2 backdoor outs = ~15 future-card outs.
- **Nut blocker**: Ad blocks villain's strongest continuing range (any nut-FD villain hand contains Ad; removing Ad from villain's range narrows their value-bet frequency).
- **3-way reduced to HU after BTN fold**: BTN's preflop call narrows CO's CB range (CO now CBs into 1 caller, range less wide than pure 3-way assumption).

### Candidate feature 1: `implied_outs_overcard`

**Definition:** count of hole-card overcards that improve to TPTK/TPGK on a future card. For AdKs on Jd8d4c: A is overcard (improves to TPTK on A turn = 3 outs); K is overcard (improves to TPGK on K turn = 3 outs); total = 6 overcard outs.

**Computation:**
```python
def implied_outs_overcard(hero_cards, board):
    board_high = max(rank(c) for c in board_cards(board))
    overcard_count = sum(1 for c in hero_cards_list if rank(c) > board_high)
    # 3 outs per overcard (one of remaining 3 unpaired)
    return overcard_count * 3
```

**Discriminative on MW-17:** Ad and Ks both overcards above J → 6 implied outs.

**Trade-off:** simpler than `effective_pot_odds_with_blocker_premium` (candidate 3 below); doesn't capture backdoor draws (those are weaker signal anyway).

### Candidate feature 2: `nut_blocker_overcard_count`

**Definition:** count of overcards × is_nut_blocker bit. Specifically: hero's overcards × `nut_flush_block`.

**Computation:**
```python
def nut_blocker_overcard_count(hero_cards, board, nut_flush_block):
    return implied_outs_overcard(hero_cards, board) // 3 * nut_flush_block
```

**Discriminative on MW-17:** AdKs on Jd8d4c → 2 overcards × `nut_flush_block=1` (Ad on diamond board) = 2.

**Trade-off:** combines two signals into one feature; cleaner discrimination but loses the standalone "implied outs" signal.

### Candidate feature 3: `effective_pot_odds_with_blocker_premium`

**Definition:** pot odds adjusted by implied-odds factor when hero has nut blocker. The actual pot odds formula reduced by `(1 + nut_blocker_overcard_count × 0.05)` premium factor.

**Computation:**
```python
def effective_pot_odds_with_blocker_premium(pot, to_call, hero_cards, board, nut_flush_block):
    raw_pot_odds = to_call / (pot + to_call)
    blocker_overcard = nut_blocker_overcard_count(hero_cards, board, nut_flush_block)
    premium = 0.05 * blocker_overcard
    return raw_pot_odds / (1 + premium)
```

**Discriminative on MW-17:** raw_pot_odds=0.367; blocker_overcard=2; premium=0.10; effective_pot_odds=0.334 (lowered from 0.367).

**Trade-off:** more aggressive feature engineering (encoded EV adjustment); risks over-fitting to MW-17-like spots; harder for QC to review for soundness.

### Recommended for MW-17 axis: **Candidates 1 + 2** (2 features)

- `implied_outs_overcard` — clean, generalizable, simple
- `nut_blocker_overcard_count` — combines two existing signals; ablation-testable

**Why not candidate 3:** EV-adjustment-encoded-as-feature contradicts `feedback_bucket_first_labelling.md` philosophy (no equity thresholds). Candidates 1 + 2 are clean discrimination signals; let the booster learn the EV math via training.

## §4 Feature design — MW-47 axis (bet+call-multiway-OOP raise pressure)

### MW-47 failure mechanism (per 12.5I-pre diagnostic)

Hero AsQs on KsJd5s, SB OOP, facing CO bet 40 + BTN call (bet+call multiway). Key features:
- `raw_equity=0.458` (NFD + gutshot ≈ 50% equity)
- `pot_odds=0.167` (cheap to call into 4-way pot)
- `nut_flush_block=1` (As on spade board)
- `villain_aggression_count=1`, `villain_call_count=1`, `num_callers_to_bet=1`
- `num_opponents=3` (4-way preflop)
- Hero OOP

Model predicts CALL with 0.920 confidence. v3.4 Fix 2.1.1 corpus teaches RAISE for this pattern (clauses a-e all satisfied at labeller layer). Model fails to transfer.

### Candidate feature: `bet_call_multiway_oop_raise_pressure_index`

**Definition:** combines villain bet+call signals + hero OOP + hero NFD+blocker + raw_equity ≥ 35% into a single discriminator that the booster can use for RAISE bucket reasoning.

**Computation:**
```python
def bet_call_multiway_oop_raise_pressure_index(features):
    if not (features['facing_bet'] == 1 and 
            features['num_callers_to_bet'] >= 1 and
            features['num_opponents'] >= 2 and
            features['is_ip'] == 0 and
            features['nut_flush_block'] == 1 and
            features['has_flush_draw'] == 1 and
            features['raw_equity'] >= 0.35):
        return 0.0
    # Composite signal: NFD strength + multiway pressure - OOP penalty
    nfd_strength = 1.0  # has_flush_draw=1 + nut_flush_block=1 → max
    multiway_pressure = features['num_callers_to_bet'] * 0.3
    oop_penalty = 0.2 if features['is_ip'] == 0 else 0.0
    return nfd_strength + multiway_pressure - oop_penalty
```

**Discriminative on MW-47:** All conditions satisfied → returns 1.0 + 0.3 - 0.2 = 1.1.

**Discriminative on negatives:** Hero with similar feature profile but no NFD (has_flush_draw=0) → returns 0. Hero IP → no OOP penalty → returns 1.3 (slightly higher; preserves IP-vs-OOP discrimination). Hero NOT facing bet+call → returns 0.

**Trade-off:** boolean-gated index returns 0 most of the time, then jumps to ~1.0+; the booster will likely weight this as a high-importance feature for RAISE-bucket discrimination. Risk: feature is so MW-47-specific it doesn't generalize. Mitigation: cross-seed importance reporting at 12.5J-E will show whether the feature is load-bearing across multiple seeds.

### Recommended for MW-47 axis: **Candidate above** (1 feature)

`bet_call_multiway_oop_raise_pressure_index` — single composite feature that captures the v3.4 Fix 2.1.1 clause-e equivalent at the model layer.

**Alternative considered + rejected:** decompose into 3 separate features (`is_bet_call_multiway`, `is_oop_with_nfd_blocker`, `raise_pressure_eligible`). Rejected because:
- Adds 3 features instead of 1 (overscope per stop condition "Feature design proposes >5 new features → STOP")
- Booster would need to learn the AND-conjunction across 3 binary features; single composite is cleaner
- Cross-seed importance is interpretable on 1 feature; less so on 3 correlated features

## §5 Cascade scope (per `feedback_attention_flags_when_features_change.md`)

For each of the 3 new features (`implied_outs_overcard`, `nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index`):

### Surface 1: Raw feature (`feature_extractor.py` + `feature_keys.py`)

Add 3 new feature key constants in `feature_keys.py`. Implement extraction in `feature_extractor.py` per definitions in §3-§4. Update `FEATURE_COLUMNS` tuple to include the new 3 → length 62 (was 59).

**Test:** `tests/test_feature_extractor.py` add unit tests with MW-17 + MW-47 + 2-3 negative-case hands; verify expected feature values.

### Surface 2: Attention vocabulary (`assemble_pilot_data.py` + related)

Add 3 new attention vocab entries with descriptions. Per `feedback_attention_flags_when_features_change.md`: "Feature changes REQUIRE matching attention vocab + prompt rules + capture + trainer."

The attention vocab entries describe the new features for downstream pipeline visibility.

### Surface 3: Prompt rules (`prompts/gto_labeller_v3.X.md`)

**Recommendation: NO PROMPT CHANGE.** The 3 new features are MODEL-side discriminators, not labeller-side bucket-reasoning rules. v3.4 already has the labelling logic (Fix 2.1.1 for MW-47 axis; bucket-first reasoning for MW-17). New features encode that logic at the model layer for transfer.

If owner / orchestrator decides labeller should ALSO see the new features (e.g., to align labels with the encoded features), that's a v3.5 prompt amendment scope outside 12.5J-A.

### Surface 4: Capture pipeline (corpus re-extraction)

After 12.5J-B (feature implementation), the 694-hand corpus + 12.5I corpus when it ships need re-extraction:
- Read existing JSONL rows
- Re-run `extract_all_features(hand_dict)` with new 62-feature surface
- Write back same JSONL with augmented `feat_dict`
- Per-row: pilot_hand_id unchanged; only `feat_dict` adds 3 new keys

This is the BIGGEST cost in the cascade (re-extraction across the entire 694+ corpus). Approximately 1-2 hours of runtime + verification.

### Surface 5: Trainer integration

`train_model_v9_student.py` updated:
- `STUDENT_FEATURE_COLUMNS_V9` extended from 59 → 62
- Pre-pad mechanism updated: warm-start `gto_model_v9_3way_v2.2.json` (45 features) needs metadata-only bump to 62 (current bumps to 59)
- `_StudentInference` mirror updated for 62-feature path
- `_StudentInferenceLike45` invariant test: re-baseline expected outputs (this WILL change for any hand where the new 3 features have non-zero values)

**Test:** `tests/test_student_inference_invariant.py` re-baseline + add MW-17 + MW-47 explicit assertions (predicted action should now flip to CALL/RAISE respectively after the new features become load-bearing).

## §6 Predicted impact (per per-hand counterfactual)

Per 12.5I-pre diagnostic counterfactual: feature ablation on existing 45-feature surface shifts X.XXX toward expert action. Adding new features changes the SHAPE of the booster's prediction surface, so simple ablation comparison is not directly informative. The empirical test is a small-sample re-train + reference set spot-check at 12.5J-E.

**Plausible outcomes at 12.5J-E:**
- **Best case:** MW-17 flips to CALL; MW-47 flips to RAISE; gate score jumps from 32 to 33-34. Median ≥33 → PROMOTE eligible if combined 12.5K with 12.5I confirms.
- **Mid case:** MW-17 prediction probability shifts from 0.046 (CALL) to 0.20-0.40 (CALL) — closer to flipping but not yet majority. MW-47 similar partial movement. Gate stays at 32 but margins meaningfully reduced. 12.5J-F decision: re-iterate with refined feature design OR accept partial gain + ship combined 12.5K.
- **Worst case:** new features have <0.02 cross-seed median importance (the H-FEAT primary watchpoint threshold) → features are not load-bearing → MW-17 + MW-47 unchanged. STOP and route to orchestrator: feature design needs revision OR E-FEATURE-primary diagnosis itself is wrong (booster can't represent the relevant logic regardless of feature surface).

## §7 Quantity discipline

3 new features total (2 for MW-17 axis, 1 for MW-47 axis). Per dispatch stop condition: "Feature design proposes >5 new features → STOP". 3 features is well within budget.

Per dispatch: "1-3 features per axis" — MW-17 axis at 2; MW-47 axis at 1. Compliant.

## §8 Methodology rules (per 12.5H-A §10 — adapted for 12.5J)

1. **Cross-seed importance reporting** at 12.5J-E (TC-X-CROSS-SEED-IMPORTANCE) for all 3 new features; expectation: at least 1 of 3 ≥0.02 floor cross-seed median to validate
2. **Cap-binding pre-flight** at 12.5J-E (TC-X-CAP-BINDING-PRE-CHECK)
3. **Pilot-first applies at 12.5J-E** (small-sample re-train before full integration test); same as 12.5H-E pattern
4. **Tier-up verification** orchestrator-side at 12.5J-E (Opus single-pass spot-check on MW-17 + MW-47 specifically)
5. **Solver-as-labels prohibited** per `feedback_solver_vs_expert_labels.md`
6. **TC-X-DISPATCH-PREDICTION-VERIFICATION** (formalized at 12.5H-C): predicted impact in §6 is LP-side estimate; orchestrator may amend; 12.5J-E small-sample re-train is the truth signal
7. **Path Y INTENTIONALLY relaxed** for 12.5J (Direction-X-retro scope per dispatch §"Direction X retro scope warning")

## §9 Sequencing — multi-phase 12.5J workstream

Per 12.5H-A precedent + 12.5J dispatch §"Sequencing":

| Phase | Comm pattern | Deliverable | Gate |
|---|---|---|---|
| 12.5J-A (this comm) | PLAN_PHASE125J_FEATURE_ENGINEERING | design (1 file) | QC APPROVE |
| 12.5J-B | BUILDER_REPORT_PHASE125J_B | feature implementation in `feature_extractor.py` + `feature_keys.py` + tests (~5 files) | QC APPROVE |
| 12.5J-C | BUILDER_REPORT_PHASE125J_C | corpus re-extraction (existing 694 + 12.5I if shipped) + JSONL writes + verification | QC APPROVE |
| 12.5J-D | REVIEW_QC_PHASE125J_D | QC sweep on 62-feature surface integrity | QC APPROVE |
| 12.5J-E | PROGRAMMER_REPORT_PHASE125J_E | small-sample re-train (5 seeds × 694-hand corpus or 794 if 12.5I shipped) + reference set spot-check on MW-17 + MW-47 | QC APPROVE; partial PROMOTE on flip |
| 12.5J-F | MAIN_TERMINAL_PHASE125J_F_SYNTHESIS | gate evaluation; integration with 12.5I at 12.5K | owner WHAT |

12.5K = combined re-train integrating 12.5I + 12.5J results. Fires AFTER both 12.5I-E and 12.5J-E ship.

## §10 Risks + open questions for orchestrator

### Risk 1: feature engineering may not transfer (E-FEATURE-primary deeper than feature surface)

If 12.5J-E small-sample re-train shows MW-17 + MW-47 still don't flip with the new features, that's evidence E-FEATURE primary is structurally deeper (booster can't represent the relevant multi-step reasoning). Mitigation: feature design is RE-VALIDATABLE empirically at 12.5J-E; if features don't load-bear, route back to architect for re-design BEFORE 12.5K combined re-train.

### Risk 2: prompt vs feature divergence

If 12.5J ships 3 new features but v3.4 prompt is unchanged (per §5 surface-3 recommendation), the labeller-side reasoning and the model-side reasoning diverge. Future re-labelling at 12.5K (if needed) might produce labels that don't exercise the new features. Mitigation: 12.5J-E small-sample re-train uses EXISTING labels (no re-label); only the model layer changes.

### Risk 3: cascade scope 5-point review

Per `feedback_attention_flags_when_features_change.md`: missing any cascade point (raw + attention + prompt + capture + trainer) creates a stale state. §5 above explicitly addresses all 5; 12.5J-B through 12.5J-E phases enforce per-surface delivery.

### Open question to orchestrator

Per 12.5I-pre diagnostic §"Cross-hand patterns": **MW-47 raw expert (CALL) and solver-corrected expert (RAISE) disagree.** Model agrees with raw expert. v3.4 Fix 2.1.1 + 12.5H corpus agree with solver-corrected expert.

If MW-47 RAW expert is GTO-correct (i.e., solver-correction is wrong), then `bet_call_multiway_oop_raise_pressure_index` feature is engineering AGAINST the GTO-correct answer. MW-47 graduates from stay-wrong list at zero feature-engineering cost.

**Recommendation:** orchestrator commission gto-expert-hat reference re-evaluation on MW-47 (similar to MW-25 question raised in 12.5I-A §9) BEFORE 12.5J-B feature implementation begins. If gto-expert confirms RAISE is GTO-correct, proceed; if CALL, drop the MW-47 feature from 12.5J scope (only `implied_outs_overcard` + `nut_blocker_overcard_count` for MW-17 ship).

This reduces risk of engineering effort against an incorrect target. Cost: 1-2 hours gto-expert review; saves 1-2 weeks of feature engineering if MW-47 is graduated.

## §11 References

- 12.5J dispatch: master `c536c30` (PR #196)
- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- 12.5H-F synthesis: master `ea642ed` (PR #191)
- 12.5I dispatch (parallel): master `c536c30` (PR #196)
- 12.5H-E re-train (cross-seed importance template): master `283af91` (PR #188)
- BATCH2 reference set: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- ml-architect 12.5D' Q4 (H-FEAT prediction validated at feature layer; didn't transfer): `/tmp/ml_architect_125d_prime_findings.md`
- gto-expert 12.5D' (E-FEATURE primary on MW-17/47): `/tmp/gto_expert_125d_prime_findings.md`
- v3.4 protocol (Fix 2.1.1 clause-e at line 880): `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_attention_flags_when_features_change.md` (cascade scope), `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_explicit_action_trigger.md`, `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`

**Status: 12.5J-A DESIGN COMPLETE. PR opening; awaiting QC trigger. After QC APPROVE: 12.5J-B (feature implementation in feature_extractor.py + feature_keys.py + tests) dispatches. Open question to orchestrator on MW-47 reference re-evaluation surfaced in §10.**
