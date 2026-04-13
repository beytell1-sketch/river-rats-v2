---
date: 2026-04-13
from: Main terminal (orchestrator) + Plan agent
to: Owner (Rupert)
re: v9-3way-v2.2 retrain plan — full team design, data strategy, evaluation
status: FOR REVIEW — awaiting approval before execution
---

## 1. Why

v9-3way-v2.1 has a **63% passive bias** on 3-way check-to-hero spots.

| Axis | v2.1 baseline | Key weakness |
|---|---|---|
| Reference set (MW-11–50) | 82.5% (33/40) | MW-25/40 passive BET→CHECK |
| Facing-bet set (FB-01–40) | 65.0% (26/40) | CALL accuracy 44% |

The model needs more BET and CALL training examples in the 0.40–0.70
equity range. Training stays on 48 features (49-53 deferred to v2.3).

## 2. Data strategy

**Total training data: ~452 rows** (348 existing + ~104 new batch 4).

| Source | Rows | Content | Action |
|---|---|---|---|
| v2.1 existing | 348 | 199 self-play + 150 factory | Keep as-is (Option B) |
| Batch 4 factory | ~104 | BET/CHECK situations from BOARD_ALLOCATION_V4_BET.md | NEW — needs labelling |
| New self-play | 0 | Produces zero facing-bet situations | Not included |

Batch 4 breakdown: BP1 (30 IP PFA value bets), BP2 (12 OOP PFA value),
BP3 (20 semi-bluff BETs), BP4 (15 IP thin value), BP5 (12 OOP value
exceptions), BP6 (15 CHECK counterexamples). Expected: ~75 BET + ~29
CHECK. Roughly doubles BET examples from 100 to ~175.

Mix ratio: 77% old / 23% new. New data concentrated in BET/CHECK.

## 3. Labelling plan

### 3.1 Calibration exam (mandatory)

KB v1.3 was updated since last calibration. One agent takes the blind
exam. Gate: 20/24 minimum + all 3 GTO-reversal hands correct.

### 3.2 Labelling team

11 GTO Expert agents × ≤10 hands each. Assigned by batch pattern (BP1–BP6)
so each agent handles one tactical theme.

### 3.3 Independent reviewers

6 reviewer agents (≥ labeller count ÷ 2). Each reviews ~17–18 labels.
Check: card conflicts, KB v1.3 consistency, vocabulary (BET not RAISE
when facing_bet=0), solver findings cross-reference.

### 3.4 Solver verification

8–12 situations estimated. Triggers: BET with equity < 0.50 on non-monster,
CHECK with equity > 0.65 and villain_air > 0.45. Owner runs in GTO Wizard
with solver-aligned sizing (25%/66% flop, 33%/75% turn+river).

**Pre-flight mandatory:** All situations must pass hand_sequence_validator.py
AND use solver-aligned sizing before owner sees them.

## 4. Training plan (Process Guide Section 6)

| Step | Agent | Job | Gate |
|---|---|---|---|
| 1 | ML-architect | Design training config: from-scratch, XGBoost 800 rounds, max_depth=5, lr=0.05. BET class weight capped at 2.0 (new), RAISE at 3.0. 5-fold stratified CV, seed=42. Run villain_range_capped ablation. | Present to review/ |
| 2 | **Owner** | Approve training plan | Nothing proceeds |
| 3 | Architect | Blueprint: version bump, BET weight cap, CSV path update in train_model.py | Present to review/ |
| 4 | Programmer | Implement + run training. Merge batch 4 CSV with v2.1 data. Model → models/. Training report → review/. | CV scores + feature importance |
| 5 | Reviewer | Quality gates: feature importance (2.3), reference set eval (2.4), facing-bet eval, v2.1 vs v2.2 side-by-side | Report to review/ |
| 6 | **Owner** | Approve model for production | Ship or iterate |

**Decision: from-scratch** (not warm-start from v2.1). Feature
distributions shifted from Phase B range changes. From-scratch avoids
inheriting stale associations.

## 5. Evaluation plan

Two-axis, both mandatory:

| Axis | v2.1 baseline | v2.2 target | Regression floor |
|---|---|---|---|
| Reference (MW-11–50) | 82.5% (33/40) | 85%+ (34/40) | 82.5% (no regression) |
| Facing-bet (FB-01–40) | 65.0% (26/40) | 70%+ (28/40) | 62.5% |

Per-class facing-bet targets:

| Class | v2.1 | v2.2 target |
|---|---|---|
| CALL (16) | 44% | 55%+ |
| FOLD (15) | 93% | maintain 75%+ |
| RAISE (9) | 56% | maintain 75%+ |

The 5 residual reference failures (MW-17, MW-25, MW-40, MW-45, MW-47)
tracked individually. Fixing MW-25/MW-40 (passive BET→CHECK) is the
primary reference improvement target.

## 6. Leakage check plan

Mandatory before training. Extend check_leakage.py to cover BOTH
test sets:
- vs reference set (MW-11–50): exact match, board overlap, feature NN
- vs facing-bet set (FB-01–40): same three checks (NEW)
- Internal deduplication within combined 452 rows

Any exact match against either test set: remove from training data.

## 7. Risk register

| Risk | Mitigation |
|---|---|
| Batch 4 labels shift too many to CHECK (>35%) | BP1–BP5 designed for BET; escalate if CHECK rate > 35% |
| Reference set regression from BET-heavy data | Regression gate at 82.5%; diagnose and adjust weights |
| Leakage between batch 4 and FB test set boards | Different boards by design; verify anyway |
| Labelling agent reverts to pre-v1.3 KB biases | Calibration gate + solver findings memo to every agent |
| Feature distribution shift from Phase B ranges | Monitor board_favour and range composition importance |

## 8. Resource summary

| Phase | Agents | Parallel? |
|---|---|---|
| Calibration | 2 (examiner + grader) | Sequential |
| Labelling | 11 GTO Experts | All parallel |
| Review | 6 reviewers | All parallel |
| Solver verification | Owner | Sequential |
| Leakage check | 1 programmer | Sequential |
| ML-architect | 1 | Sequential |
| Architect blueprint | 1 | Sequential |
| Programmer train | 1 | Sequential |
| Reviewer gate | 1 | Sequential |
| **Total** | **23 agents + 2 owner checkpoints + 1 solver session** |

Estimated: 3 sessions.

## 9. Success criteria

v2.2 ships if ALL of:
1. Reference set ≥ 82.5% (no regression)
2. Facing-bet set ≥ 70.0% overall
3. Facing-bet CALL accuracy ≥ 55%
4. 5-fold CV accuracy: no drop > 3pp from v2.1
5. No feature above 30% importance
6. Leakage check: zero exact matches against either test set
7. All quality gates (2.1–2.4) passed with evidence

If #1 fails: do NOT ship. Diagnose and adjust.
If #2–3 fail but #1 passes: do NOT ship. Diagnose whether batch 4
data addressed the passive bias. If CALL accuracy improved but didn't
hit 55%, add more CALL-targeted factory data and retrain as v2.2.1
before shipping. No half-fixes reach production.

## Notes

**Facing-bet baseline (65.0%)** is against FINAL labels in the
shipped production file `training-data/facing_bet_test_set_40.jsonl`
(task #4 completed, commit 22b02e9). Targets do not need recalibration.

**Reference set** runs against the corrected version with MW-31 and
MW-34 sequence fixes applied (task #10, commit 6379761). Both labels
unchanged (MW-31 FOLD, MW-34 BET).

## 10. Not in scope

- Features 49–53 (deferred to v2.3)
- Phase B-2 multiway-biased sampling (downgraded)
- Teaching system updates (gated on v2.2 ship)
- New self-play data (zero facing-bet yield)
- Sizing oracle retraining (separate model)
- v9-4way specialist (gated on v9-3way ceiling)

---

**Awaiting approval. On "go" I execute calibration immediately.**
