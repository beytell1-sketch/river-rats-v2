---
date: 2026-05-03
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · ML-ARCHITECT (advisory)
re: Phase 12.5 — pivot to Path Y; 12.5-prep CANCELED; dispatch 12.5C blueprint
status: DIRECTIVE — supersedes PRs #112, #113, #115, #117 (all 12.5-prep variants)
---

# Phase 12.5 pivot — Path Y; 12.5C blueprint dispatch

## Decision

**12.5-prep is CANCELED.** No `FEATURE_COLUMNS` migration. Pivot to Path Y per ml-architect's PR #110 §5 alternative.

**Why:** Three BLOCKED iterations (PRs #114, #116, #118) grew scope from 4 → 5 → 7 source surfaces. Path X's "single source of truth" premise is empirically false — `gto_model.py` is one of 7+ `FEATURE_COLUMNS` tuples with cross-equality assertions enforcing identity. The "dual-schema risk" Path Y was supposed to prevent already exists. `feature_extractor.py:FEATURE_COLUMNS` is already at 59 (Step 17 P1 blockers committed previously). The corpus is extracted at 59 features. The trainer can read 59 features without touching any other source surface.

This pivot reverses ml-architect's Item 4 Path X choice given new empirical evidence the builder surfaced. Methodology re-decision is between two options ml-architect already explicitly considered (PR #110 §5).

## What stays from ml-architect's design (PR #110)

Unchanged: Items 1, 2, 3, 5, 6 + Hyperparameters (§8) + CLI surface (§9) + Gate hooks (§10) + Risk register (§11). Item 4 reverses to Path Y.

## 12.5C — LEAD-PROGRAMMER (architect hat)

Branch: `programmer/phase125c-trainer-blueprint-2026-05-03`

Author `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md`. Blueprint only — **no code changes**.

### Required content

1. **New module skeleton** — `river-rats-core/train_model_v9_student.py`
   - Provenance docstring (per CLAUDE.md §6 addendum)
   - Imports list with line-by-line reasoning (must include `from feature_extractor import FEATURE_COLUMNS as STUDENT_FEATURE_COLUMNS_V9` — single source of truth from the extraction layer)
   - Module-load assertion: `assert len(STUDENT_FEATURE_COLUMNS_V9) == 59` and the 4 v2.4 P1 blocker names are present
   - Function signatures (load_corpus, load_labels, join_on_ref_id, prepad_baseline_booster, train_one_seed, evaluate_held_out, gate_23_feature_importance_check, gate_24_reference_evaluation, write_report, main)
   - argparse contract per ml-architect §9 (verbatim)
   - Hyperparameter dict per ml-architect §8 (verbatim)

2. **Pre-pad mechanism specifics** (ml-architect Item 2)
   - Exact xgboost API calls: `xgb.Booster(model_file=...)`, `feature_names` mutation, `xgb_model=` to `fit()`
   - Failure mode if API rejects: log + fall back to curriculum 45→59 (per R-1 mitigation)

3. **No `gto_model.py` / `coaching/gto_model.py` / `sizing_oracle.py` / `train_model.py` / `train_sizing_model.py` changes**
   - Path Y leaves all existing 55-feature surfaces untouched
   - Inference of the new 59-feature student model uses `gto_model.py:104-107` `n_features_in_` auto-detect (already in master)

4. **Reference evaluator integration** (ml-architect Item 5)
   - Calls `reference_evaluator.evaluate_variants(...)` with v8 + v9-3way-v2.2 + new student
   - Solver corrections per `memory/reference_corrections.md`

5. **Cite line numbers for every external reference** (`feature_extractor.py:1569`, `gto_model.py:104-107`, etc.) — verify against master HEAD before writing

### Stop conditions

- Any cited line number doesn't exist on master HEAD → STOP
- Any function signature requires changes to existing modules outside the new file → STOP
- Pre-pad mechanism's xgboost API path is unclear after reading xgboost docs → STOP, request ml-architect clarification

PR title: `Builder Phase 12.5C: v9 student trainer blueprint`

PR body: blueprint summary (≤10 lines); link to ml-architect PR #110.

## QC

**No pre-merge audit on the 12.5C blueprint PR.** Blueprints are design comms; QC fires at 12.5D implementation PR.

## After 12.5C merges

Owner gates 12.5C blueprint review. On approval, orchestrator dispatches 12.5D (LEAD-PROGRAMMER implements + runs from blueprint).

## What this directive supersedes

- PR #112 (verbose prep directive)
- PR #113 (tight prep directive)
- PR #115 (R-A amended scope)
- PR #117 (R-A2 scope)

All four are now historical. Lead-programmer's prep branch (`programmer/phase125-prep-r-a2-2026-05-03`) is abandoned.

## References

- PR #118 (R-A2 BLOCKED, empirical Path X refutation) — master `76bf256`
- PR #116 (R-A BLOCKED) — master `ddfc6a2`
- PR #114 (PR #113 BLOCKED) — master `9f5c22a`
- PR #110 (ml-architect spec, §5 Path Y as alternative) — master `291af80`
- PR #111 (orchestrator review + owner approval) — master `88e5b38`

**Status: 12.5-PREP CANCELED. 12.5C BLUEPRINT DISPATCHED. LEAD-PROGRAMMER named author.**
