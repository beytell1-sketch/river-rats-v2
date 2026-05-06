---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5J-B — feature implementation per 12.5J-A design (3 features: implied_outs_overcard + nut_blocker_overcard_count for MW-17; bet_call_multiway_oop_raise_pressure_index for MW-47); parallel with 12.5I-B
status: TRIGGER — fire now
---

# Phase 12.5J-B — feature implementation

12.5J-A merged at master `6e6d9d8`. Builder implements 3 new features per design. Direction-X-retro scope; cascade through `feature_extractor.py` + `feature_keys.py` + attention vocab + capture + trainer per `feedback_attention_flags_when_features_change.md`.

12.5J-B parallel with 12.5I-B (situation generation; separate dispatch).

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125j-b-feature-implementation-2026-05-XX`

### Cascade scope (per `feedback_attention_flags_when_features_change.md`)

Per 12.5J-A design §4:

1. **Raw feature** in `river-rats-core/feature_extractor.py` + `feature_keys.py`:
   - `implied_outs_overcard` (MW-17 axis): per design spec
   - `nut_blocker_overcard_count` (MW-17 axis): per design spec
   - `bet_call_multiway_oop_raise_pressure_index` (MW-47 axis): per design spec

2. **`FEATURE_COLUMNS` extension**: 59 → 62 features. Path Y boundary INTENTIONALLY relaxed for 12.5J (Direction-X-retro per 12.5H-F gate).

3. **Attention vocabulary** in `assemble_pilot_data.py` + related: 3 new attention flags

4. **Prompt rules** in `prompts/gto_labeller_v3.4.md` (or v3.5 if amendment needed): only if features should appear in labeller bucket reasoning. Per 12.5J-A design §4: probably NOT (features are model-side discriminators, not labeller-side rules). Confirm at design-walk before implementing.

5. **Capture pipeline**: re-extract feat_dict for existing 694-hand corpus (12.5H combined) to add new feature values. 12.5I corpus (when 12.5I-B merges) also needs re-extraction.

6. **Trainer**: `train_model_v9_student.py` `_StudentInference` mirror updated for 62-feature surface. `_StudentInferenceLike45` invariant test re-baselined.

### Phased B-implementation breakdown

12.5J-B itself splits into sub-phases per pilot-first rule:

- **12.5J-B-1**: feature implementation in `feature_extractor.py` + `feature_keys.py` + unit tests; verify on small set before re-extraction
- **12.5J-B-2**: re-extraction of existing 694 corpus + integration test
- **12.5J-B-3**: trainer mirror update + invariant test re-baseline + small-sample dry-run (1-seed; 10-15 hands cross-section)

### Pilot gate (12.5J-B-3 dry-run)

Before committing to full re-extraction + trainer integration:
- Run 1-seed dry-run with new 62-feature surface on small cross-section (5 reference hands × 5 random parametrics)
- Verify: trainer loads 62-feature surface; pre-pad mechanism works (new metadata bump 59 → 62); held-out classification reasonable (no NaN; all 5 classes present)
- Stop conditions: pre-pad fails → STOP, fallback to feature-by-feature integration; trainer crash → STOP, debug; held-out class collapse → STOP, investigate

### Deliverable scope (8-12 files; Direction-X-retro is broader than Path Y phases)

1. `river-rats-core/feature_extractor.py` — UPDATE (add 3 features)
2. `river-rats-core/feature_keys.py` — UPDATE (3 new feature constants)
3. `river-rats-core/assemble_pilot_data.py` — UPDATE (3 new attention vocab entries)
4. Tests for new features (e.g., `tests/test_features_125j.py`) — NEW
5. Re-extracted corpus (combined 694) — NEW or UPDATE
6. `river-rats-core/train_model_v9_student.py` — UPDATE (62-feature surface; `_StudentInference` mirror)
7. `tests/test_train_model_v9_student.py` — UPDATE (`_StudentInferenceLike45` invariant test re-baseline)
8. `review/comms/BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-XX.md` — NEW: report

### Stop conditions

- Cascade scope misses any of 5 cascade points → STOP
- Pre-pad fails on 62-feature surface → STOP, document for trainer-side mitigation (curriculum 59→62 path or similar)
- Re-extraction produces feat_dict shape ≠ 62 → STOP
- Invariant test fails after re-baseline → STOP, mirror drift in `_StudentInference`
- Solver call appears → STOP

## QC stream — what you audit

When 12.5J-B PR opens, audits per dispatch + cascade-scope verification + Path Y boundary relaxation acknowledgment in builder report.

## Sequencing

12.5J-B → 12.5J-C corpus integration → 12.5J-D corpus QC → 12.5J-E trainer integration test (parallel with 12.5I phases). Combined re-train at 12.5K when both 12.5I-E and 12.5J-E ship.

## What's blocked / what's queued

**Blocked:**
- 12.5J-B PR opens → on builder cascade implementation + report
- Subsequent 12.5J-X → on prior phase merge
- 12.5K combined re-train → on both 12.5I-E AND 12.5J-E ship

## References

- 12.5J-A merged: master `6e6d9d8` (PR #198)
- 12.5J-A QC APPROVE: master `73963b4` (PR #200)
- 12.5J dispatch: master `c536c30` (PR #196)
- 12.5C blueprint trainer module (`_StudentInference` pattern): master `1e4e47e` (PR #122)
- 12.5G trainer parameterization (cap CLI flag): master `2135fc8` (PR #157)
- Memory: `feedback_attention_flags_when_features_change.md` (cascade scope), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`

**Status: 12.5J-B TRIGGER posted. LEAD-PROGRAMMER (architect + default hats) implements 3 new features through 5 cascade points.**
