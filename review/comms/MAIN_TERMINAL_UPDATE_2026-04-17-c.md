---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Phase 4 accepted; launch Phase 5 assembly now with provisional labels
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-17 (c)

Phase 4 accepted. 470 hands labelled, all stop conditions
clear, override clause behaviour correct (S4.3 re-scope noted
as doc fix, not defect).

## 1. Launch Phase 5 assembly now

Do not wait for the 28 solver-enqueued hands or the row-11
solver-sourced cohort. Assemble now with provisional labels.

### Assembly inputs

| Source | Hands | Label status |
|---|---|---|
| v2.2 base | 385 | final |
| Phase 4 production | 470 | 442 final (4/4 or 3/1) + 28 provisional |
| Phase 3.5 pilot | 16 | final |
| Row-11 solver-sourced | 0 (pending owner) | — |
| **Total** | **871** | 842 final + 28 provisional + ~10-20 solver TBD |

### Provisional label handling

For the 28 solver-enqueued hands:

- **26 hands (2/2 Pass 1 splits):** use Pass 2's resolution
  as the provisional label. Pass 2 saw the full panel traces
  and made a call — that's the best available signal.
- **2 hands (Pass 2 overrides):** use Pass 2's override
  action as the provisional label (it was the considered
  decision).
- Mark all 28 as `label_source=PROVISIONAL_AWAITING_SOLVER`
  in the CSV so they're trivially filterable.

### Schema and preflight

- Output: `training-data/v2_3_training.csv`
- Must pass `_preflight_schema_check()` **without**
  `--allow-mixed-encoding` (all inputs are post-Fix-1 clean
  BP JSONLs + d-series numeric + pilot numeric).
- If preflight fails, STOP — that's a Fix 1 regression.
- The v2.2 base rows in `v2_2_training.csv` still have mixed
  encoding. Assembly script must re-encode them through
  CAT_MAPS at merge time (same encoding as the ported trainer
  uses). Do NOT copy mixed-encoded rows verbatim into the
  v2.3 CSV.

### Solver correction protocol (post-assembly)

When solver results land on any of the 28 hands:
1. Patch `label` in `v2_3_training.csv` for affected rows
2. Update `label_source` from `PROVISIONAL_AWAITING_SOLVER`
   to `SOLVER_CONFIRMED` or `SOLVER_OVERRIDE_<old>_TO_<new>`
3. If ≤3 labels flip: targeted retrain, compare metrics
4. If >5 labels flip: investigate before retraining — that
   volume of overrides suggests a systematic prompt/panel
   issue
5. Row-11 solver-sourced cohort (10-20 hands): append when
   available, same protocol

## 2. S4.3 re-scope — doc fix

The override clause firing on non-UMBRELLA MM/SM buckets is
correct behaviour (those hands satisfy all 7 preconditions
by construction). Update the build plan §8 S4.3 from:

> "Override clause fires on >10% of non-UMBRELLA hands"

to:

> "Override clause fires on hands where <7 of the 7
> preconditions hold"

This converts the metric from a bucket-taxonomy check to a
precondition-compliance check. Commit as a one-line doc
fix alongside Phase 5 assembly.

## 3. Sequencing through Phase 7

| Phase | Status | Gates on |
|---|---|---|
| 5 Assembly | 🟢 launch now | — |
| 6 Training | ⏸️ | Phase 5 + preflight pass |
| 7 Validation | ⏸️ | Phase 6 |
| Ship | ⏸️ | Phase 7 all 5 criteria + solver 7.3 |

Phase 5 → 6 → 7.1/7.2 can run end-to-end without pause.
Phase 7.3 (solver validation on 8 MW misses) is the only
owner-dependent step before ship.

## 4. Deliverables

- `training-data/v2_3_training.csv` (871 rows × 111 columns)
- `review/comms/PHASE_5_ASSEMBLY_2026-04-17.md` with: row
  counts by source, class distribution, preflight pass/fail,
  schema comparison vs v2.2, provisional-label count
- S4.3 doc fix in the build plan

Commit per deliverable. Push immediately.
