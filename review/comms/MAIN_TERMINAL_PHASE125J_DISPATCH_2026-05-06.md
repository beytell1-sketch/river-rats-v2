---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5J — feature engineering for MW-17/47 (E-FEATURE primary); parallel with 12.5I (separate dispatch); Direction X retro scope
status: TRIGGER — fire now
---

# Phase 12.5J — feature engineering (C path; addresses 2 of 5 stay-wrong)

12.5I-pre diagnostic merged at master `54e2943`. Per-hand verdicts assigned 2 hands to 12.5J (feature engineering path C):

- **MW-17** (E-FEATURE primary, no secondary): need features for implied-odds + nut-blocker-with-overcards reasoning. Margin to expert: +0.843 (very far).
- **MW-47** (E-FEATURE primary, mixed with raw-vs-corrected expert disagreement): SUITED-NFD-with-blocker-bet+call-multiway. v3.4 Fix 2.1.1 corpus teaches the right RAISE, but model fails to transfer. Margin: +0.910 (model agrees with RAW expert CALL).

12.5J runs in **parallel with 12.5I** (corpus expansion for MW-25/40/45; separate dispatch comm `MAIN_TERMINAL_PHASE125I_DISPATCH_2026-05-06.md`). Non-overlapping targets; no coordination overhead until 12.5K integration.

## Direction X retro scope warning

Per `feedback_attention_flags_when_features_change.md`: feature changes REQUIRE matching attention vocabulary + prompt rules + capture + trainer changes. 12.5J is explicitly Direction-X-retro scope (Path Y boundary issue per 12.5E-F decision matrix). Cascade through:

1. **Raw feature** (`feature_extractor.py` + `feature_keys.py`): new feature(s) added to 59-surface
2. **Attention vocabulary** (`assemble_pilot_data.py` + related): new attention flag(s) for the new feature(s)
3. **Prompt rules** (`prompts/gto_labeller_v3.X.md`): if feature is part of labeller bucket reasoning, prompt may need amendment
4. **Capture pipeline**: existing labels need re-extraction with the new feature
5. **Trainer**: `train_model_v9_student.py` + Path Y `_StudentInference` mirror updated for the new feature(s)

This is a 3-4 week workstream, not a 1-day edit. Owner approved this scope at 12.5H-F gate (E → C+D parallel compound). Slow-quality default applies throughout.

## LEAD-PROGRAMMER — what you do (architect hat for design)

This is a multi-phase workstream. 12.5J-A (design) → 12.5J-B (feature implementation) → 12.5J-C (corpus re-extraction) → 12.5J-D (QC) → 12.5J-E (trainer integration test). Final integration with 12.5I at 12.5K.

### 12.5J-A — Feature design comm

Author `review/comms/PLAN_PHASE125J_FEATURE_ENGINEERING_2026-05-XX.md`.

Required content:

#### §1 Authority chain

12.5H-F synthesis (PR #191) + 12.5I-pre diagnostic (PR #193) + ml-architect 12.5D' Q4 H-FEAT prediction (validated at feature layer, didn't transfer).

#### §2 Feature design — MW-17 axis

Engineer feature(s) that capture implied-odds + nut-blocker-with-overcards on draws where draw_outs=0 but blockers + overcards make calling profitable. Candidate features (recommend at least 2 candidates with trade-offs):
- `implied_odds_with_nut_blocker` (pot_odds reduced by implied-odds factor when hero has nut blocker)
- `nut_blocker_overcard_count` (count of overcards × nut_blocker bit)
- `effective_pot_odds_with_blocker_premium` (combined adjustment)

For each candidate: define computation; identify which existing features it depends on; estimate how it would discriminate MW-17 (CALL) from non-MW-17 weak-air-folds.

#### §3 Feature design — MW-47 axis

Engineer feature(s) that capture SUITED-NFD-with-nut-blocker-bet+call-multiway raise pressure. The v3.4 Fix 2.1.1 protocol clause-e equivalent at the FEATURE layer rather than the LABELLER layer. Candidate:
- `bet_call_multiway_oop_raise_pressure_index` (combines villain_call_count, villain_aggression_count, hero position OOP, hero NFD+blocker, raw_equity ≥35%)

This feature, if load-bearing, lets the booster RAISE on bet+call-multiway hands (matching MW-47 + the T-RAISE-stabilize labels) WITHOUT relying on the labeller-level v3.4 carve-out.

#### §4 Cascade scope

Per `feedback_attention_flags_when_features_change.md`:
- New raw features in `feature_extractor.py` + `feature_keys.py`
- New attention vocab entries in `assemble_pilot_data.py`
- v3.4 → v3.5 prompt amendment IF features should appear in labeller bucket reasoning (probably not — features are model-side discriminators, not labeller-side rules)
- Re-extraction of existing 694-hand corpus to add new feature values (no re-labelling needed; only feat_dict augmentation)
- Trainer `_StudentInference` mirror updated for new feature count (60+, not 59)
- `_StudentInferenceLike45` invariant test re-baselined

#### §5 Predicted impact

Per per-hand counterfactual at 12.5I-pre diagnostic: feature ablation shifts X.XXX toward expert action. Verify the new feature design empirically at 12.5J-E (small-sample re-train + reference set spot-check).

If 12.5J-E shows MW-17 + MW-47 still don't flip with the new feature, that's evidence E-FEATURE primary is structurally deeper than feature-surface (e.g., requires multi-step reasoning the booster can't represent). At that point, owner WHAT decision would re-engage.

### 12.5J-B/C/D/E — phases after design

- 12.5J-B: feature implementation in `feature_extractor.py` + `feature_keys.py`
- 12.5J-C: corpus re-extraction (existing 694 corpus + 12.5I corpus when 12.5I-B merges)
- 12.5J-D: QC (CONTENT drift on feature contract; 60-feature surface verification)
- 12.5J-E: integration test (small-sample re-train; reference set spot-check on MW-17 + MW-47)

Each phase fires on prior phase merge + explicit MAIN_TERMINAL_*_TRIGGER comm.

### Scope discipline

- Path Y is INTENTIONALLY relaxed for 12.5J (Direction X retro scope per 12.5E-F decision matrix; owner approved)
- Trainer module + `_StudentInference` updated for 60-feature surface
- Existing 694 corpus + 12.5I corpus + new 12.5J feature → fed to combined trainer at 12.5K
- Cross-seed importance reporting still required (TC-X-CROSS-SEED-IMPORTANCE)

### Stop conditions

- Feature design proposes >5 new features → STOP, route to orchestrator (overscope; 1-3 features per axis)
- Cascade scope misses any of the 5 cascade points (raw + attention + prompt + capture + trainer) → STOP, fix design
- Solver-as-labels appears → STOP

## QC stream — what you audit (per phase)

Same audit pattern as 12.5H. 12.5J-A is design-only (3 audits: diff scope, citations, methodology). 12.5J-B onwards add CONTENT drift audits + invariant test verification.

## Sequencing

1. LEAD-PROGRAMMER (architect hat) authors 12.5J-A design comm
2. 12.5J-A PR opens
3. QC audit
4. On QC APPROVE: 12.5J-B (feature implementation) dispatched; subsequent phases follow

## What's blocked / what's queued

**Blocked:**
- 12.5J-A PR opens → on builder design comm
- Each subsequent 12.5J-X → on prior phase merge

**Parallel (independent of 12.5J):**
- 12.5I workstream (corpus expansion for MW-25/40/45) — separate dispatch comm
- 12.5K combined re-train — fires AFTER both 12.5I-E and 12.5J-E ship

## References

- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- 12.5I dispatch (parallel): `MAIN_TERMINAL_PHASE125I_DISPATCH_2026-05-06.md` (in this PR cycle)
- 12.5H-F synthesis: master `ea642ed` (PR #191)
- ml-architect 12.5D' Q4 (H-FEAT prediction): `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_attention_flags_when_features_change.md` (cascade scope), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`

**Status: 12.5J TRIGGER posted. LEAD-PROGRAMMER (architect hat) authors 12.5J-A feature design comm. Parallel with 12.5I. Combined re-train at 12.5K.**
