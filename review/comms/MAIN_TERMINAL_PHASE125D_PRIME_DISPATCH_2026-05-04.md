---
date: 2026-05-04
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · ML-ARCHITECT (advisory) · GTO-EXPERT (review)
re: Phase 12.5D' — hybrid weighting + invariant test + blueprint pre-flight protocol amendment per owner C' decision
status: DIRECTIVE — owner picked C'; LEAD-PROGRAMMER named author
---

# Phase 12.5D' — hybrid weighting (Path C')

Owner picked **C'** at the 12.5D synthesis owner gate (`MAIN_TERMINAL_PHASE125D_SYNTHESIS_OWNER_GATE_2026-05-04.md`, master `d6dd36d`). Master HEAD now `af6b82c` includes the merged 12.5D BLOCKED baseline (PR #126), the synthesis (PR #128), and the QC convergence record (PR #129).

Dispatch designed against the converged expert findings:
- gto-expert root cause: class-prior collapse on aggressive labels
- ml-architect quantification: 3.9× passive bias under pure confidence weighting
- Same mitigation: hybrid weighting (confidence × inverse-class-frequency, capped)

## LEAD-PROGRAMMER

Branch: `programmer/phase125d-prime-hybrid-weighting-2026-05-XX` (XX = your start date)

### Authority chain (highest to lowest precedence)

1. This dispatch directive (operational scope, sequencing, stop conditions, gate threshold)
2. ml-architect 12.5D findings (`/tmp/ml_architect_125d_findings.md` summary in synthesis comm; ml-architect's Q3 hybrid spec is the verbatim implementation target for the weighting line)
3. gto-expert 12.5D findings (synthesis comm §"Finding 2") — informs gate-failure interpretation if hybrid weighting still falls short
4. Approved blueprint PR #122 §2-§8 (module skeleton, signatures unchanged; only the `sample_weight` computation and one new test change)
5. CLAUDE.md §6 (sacred core) + §6 addendum (training provenance)

### Deliverable — exactly 4 files in the diff

Per Path Y discipline (still binds):

1. **`river-rats-core/train_model_v9_student.py`** — UPDATE (existing file; ~5-line diff for hybrid weighting at the `sample_weight` computation)
2. **`river-rats-core/tests/test_train_model_v9_student.py`** — UPDATE (add 1 invariant test per ml-architect Option α)
3. **`river-rats-core/models/gto_model_v9_student.json`** — NEW (produced model artifact, ONLY if gate passes per stop condition #4)
4. **`review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-XX.md`** — NEW (Section A-D per blueprint §2.4 + Section E "12.5D vs 12.5D' delta")

`git diff --stat` against master must show exactly these 4 files. Any edit to existing source surfaces other than `train_model_v9_student.py` and its test → **STOP**.

### The hybrid weighting change (ml-architect Q3 spec, verbatim)

In `train_one_seed`, replace the existing `sample_weight = confidence` (or equivalent confidence-only line) with:

```python
# Hybrid weighting per ml-architect 12.5D Q3 (closes class-prior collapse).
# Cap = 3.0 ported from train_model.py:252-257 prior art (empirically
# calibrated for v9-3way-v2.2 to balance aggressive classes without
# inverting discipline). On the 5-class corpus, ~3.0× boost on RAISE,
# ~1.4× on BET, ~1.6× on CALL, ~1.0× on CHECK/FOLD.
class_counts = np.bincount(y_train, minlength=N_CLASSES)
mean_class_count = class_counts.mean()
class_weights = {c: min(3.0, mean_class_count / max(class_counts[c], 1))
                 for c in range(N_CLASSES)}
sample_weight = confidence_train * np.array([class_weights[c] for c in y_train])
```

Same change to the `sample_weight_eval_set` computation for held-out evaluation. **Do not** improvise the cap or the formula — if anything is unclear, STOP and request ml-architect clarification rather than guess.

### The invariant test (ml-architect Option α, verbatim)

Add to `river-rats-core/tests/test_train_model_v9_student.py`:

```python
def test_student_inference_mirror_invariant_on_baseline():
    """Behavioural-equivalence test: student inference on 45-feat baseline
    must match canonical reference_evaluator._evaluate_one_hand on all 40
    MW reference hands. If reference_evaluator changes shape and the
    in-module mirror doesn't, this test flips at least one hand."""
    from train_model_v9_student import (
        _StudentInference, _evaluate_student_one_hand,
        STUDENT_FEATURE_COLUMNS_V9,
    )
    from gto_model import GtoOracle
    from reference_evaluator import _evaluate_one_hand, parse_reference_hands

    baseline_path = "river-rats-core/models/gto_model_v9_3way_v2.2.json"
    canonical_oracle = GtoOracle(baseline_path)
    student_45_shim = _StudentInference(
        baseline_path, feature_columns=list(STUDENT_FEATURE_COLUMNS_V9[:45])
    )

    designs = "design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md"
    analysis = "design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md"
    hands = parse_reference_hands(designs_path=designs, analysis_path=analysis)
    assert len(hands) == 40

    for hand in hands:
        canonical = _evaluate_one_hand(canonical_oracle, hand)
        student = _evaluate_student_one_hand(student_45_shim, hand)
        assert canonical.adjusted_action == student.adjusted_action, (
            f"Mirror drift on {hand.ref_id}: "
            f"canonical={canonical.adjusted_action} "
            f"student={student.adjusted_action}"
        )
        assert canonical.correct == student.correct
        assert canonical.was_adjusted == student.was_adjusted
```

If `_StudentInference.__init__` signature doesn't currently accept `feature_columns`, that's an in-module change ONLY (extends the existing class to take an optional `feature_columns` kwarg defaulting to the full 59 surface). Adding the kwarg is allowed under Path Y because `_StudentInference` is in-module to the trainer — no edits to `gto_model.py` or `reference_evaluator.py`.

### Blueprint pre-flight protocol amendment (ml-architect Q1, in-effect immediately)

This dispatch establishes a new mandatory pre-flight rule for all future blueprint authors. Lead-programmer (when wearing architect hat for future blueprints), QC, and orchestrator all enforce:

> **Blueprint pre-flight rule (effective 2026-05-04):** Any blueprint citing a join key between two data files must (a) verify the join key on at least 5 sample rows spanning the file (e.g., row 1, 100, 200, 400, last), AND (b) compute and report the empirical join cardinality. If the cardinality ratio is < 0.99, the join key is a STOP-class question, NOT a verified premise. Blueprint authors record the verification commands + outputs inline.

This rule lives in dispatch directives until ml-architect formalizes it in `docs/PROCESS_GUIDE.md` (separate workstream, not gating 12.5D').

### Sequencing — mandatory order

1. **Pre-flight (5 min):** verify trainer module + tests pass on master HEAD `af6b82c` before changes (sanity check); confirm no source-surface drift since 12.5D merge
2. **Implement** the hybrid weighting + invariant test. Run pytest; all 17 tests (16 existing + 1 new invariant) must pass before any training run
3. **R-1 dry-run gate (mandatory):** `python3 river-rats-core/train_model_v9_student.py --no-write-model` per blueprint §8.3. Verifies hybrid weighting shape + capture+check that pre-pad still works. Captures xgboost trace for diff vs 12.5D
4. **5-seed training run:** seeds 0-4 (same as 12.5D for direct delta comparison). Hyperparameters per blueprint §2.6 unchanged. Choose seed by median solver-corrected litmus
5. **Reference-evaluator gate:** `gate_24_reference_evaluation` with baselines `[gto_model_v9_3way_v2.2.json]`. (v8-38feat still untracked per #PSH-01; canonicality guard drops it as before.) Apply solver-correction overlay (MW-30/46/47); NOT MW-31/50
6. **Promotion decision:** if median seed solver-corrected ≥ 33 → promote (write `gto_model_v9_student.json`). If < 33 → STOP, do NOT promote, report
7. **Write trainer report** per blueprint §2.4 + Section E "12.5D vs 12.5D' delta" comparing per-class metrics, per-hand outcomes (which of MW-17/24/25/40/42/45/47 flipped to correct), and the P1 blocker importances pre/post hybrid weighting
8. **Open 12.5D' PR** with the 4 files (or 3 if model not promoted); PR title `Builder Phase 12.5D': v9 student trainer hybrid weighting (C')`

### Gate threshold (NEW — clarified vs 12.5D)

| Median seed solver-corrected | Outcome |
|---|---|
| ≥ 33 (clears v9-3way-v2.2 baseline) | PROMOTE to `gto_model_v9_student.json` |
| 31-32 (no improvement or marginal) | STOP, do NOT promote, report — owner gate on "ship a tie? new direction?" |
| < 31 (regression vs 12.5D) | STOP, do NOT promote, report — hybrid weighting hurt; ml-architect Q3 reasoning needs revision |

Per-seed variance is OK; only median gates. Report all 5 seed scores.

### Stop conditions

- Trainer module + tests don't pass on master HEAD `af6b82c` before changes → STOP (something drifted since 12.5D merge)
- Hybrid weighting computation fails at runtime (e.g., `class_counts` has zero-count class) → STOP, do not silently mask with `max(..., 1)` beyond the pattern shown
- Invariant test fails (mirror drift between `_evaluate_one_hand` and `_evaluate_student_one_hand` on 45-feat shim) → STOP, report (this means the mirror was already drifted on master; not a 12.5D' regression)
- Pre-pad metadata-only path fails → fall back to curriculum 45→59 per blueprint §4.4 (R-1) — this is the ONLY sanctioned alternative; don't improvise a third
- Median seed solver-corrected < 33 → STOP, do NOT promote (per gate threshold table)
- Median seed solver-corrected < 31 → STOP, do NOT promote, **and** flag this as evidence ml-architect Q3 reasoning was wrong (hybrid weighting made things worse)
- >4 files in diff → STOP, revert extras

### What you do NOT do

- Do NOT touch `gto_model.FEATURE_COLUMNS` or any other existing source surface (Path Y still binds)
- Do NOT change the cap from 3.0 to anything else without ml-architect approval (the 3.0 was empirically calibrated; tuning is a separate workstream if this run overshoots)
- Do NOT add a per-class boost beyond the formula given (the formula handles all 5 classes uniformly via inverse-class-frequency)
- Do NOT extend `reference_evaluator.evaluate_variants` (still forbidden per Path Y)
- Do NOT auto-promote on score ≥ 31 if < 33 (the 31 threshold is the regression-flag, not the promote threshold)

## QC

**QC pre-merge audit FIRES on the 12.5D' PR.** Standalone QC stream is the primary channel per `feedback_qc_routing_when_standalone_active.md` (saved 2026-05-04 from the 12.5D NIT-1 incident). Orchestrator will NOT spawn parallel general-purpose subagent for the same audit.

QC stream audits:

1. **Diff scope** — exactly 4 files (or 3 if model not promoted); verify the trainer module diff is ONLY the hybrid weighting block + Path Y `_StudentInference` kwarg extension
2. **Citation existence** — every file:line citation in trainer module + tests + report exists at master HEAD at audit time
3. **Provenance** — trainer docstring updated to reflect 12.5D' run; report Section D hashes match
4. **NEW: Hybrid weighting verbatim check** — the `sample_weight` computation matches the directive's verbatim spec (cap 3.0, multiplicative on confidence, applied to both train + eval_set weights). NIT-class deviations OK; substantive deviations = HOLD
5. **NEW: Invariant test verification** — the test actually runs and passes (not just defined); covers all 40 MW hands; tests three fields (adjusted_action, correct, was_adjusted)

Post `REVIEW_QC_PHASE125D_PRIME_TRAINER_*.md`.

## ML-ARCHITECT (advisory)

The 12.5D' PR will surface:
- Per-class metrics post-hybrid (does CHECK degrade meaningfully? does RAISE recall hit ≥ 0.7?)
- Per-hand outcomes vs 12.5D (which of MW-17/24/25/40/42/45/47 flipped?)
- 5-seed variance under hybrid weighting (does the cap of 3.0 stabilize across seeds?)

If hybrid weighting overshoots (e.g., student scores 36+/40 but RAISE precision drops below 0.5 = false-positive RAISE-bias), recommend cap tuning (2.0 or 2.5) for 12.5D''.

If 12.5D' falls in 31-32 range despite hybrid weighting, your Q3 recommendation needs revision — the 7-of-7 shared-cause hypothesis was wrong. Re-engage with revised diagnosis.

No gate vote required at 12.5D' PR. 12.5F owner ship gate is your next decision point.

## GTO-EXPERT (review)

12.5D' PR review chain:
- Per-class action distribution in 12.5D' student vs 12.5D student vs v9-3way-v2.2 baseline
- Solver-correction overlay arithmetic unchanged
- **NEW:** verify the per-hand flip pattern matches the predicted shared-cause vs distinct-cause split. Specifically: of MW-17/24/25/40/42/45/47 (your "shared cause" 7), how many flipped to correct under hybrid weighting? Of MW-31/46 (your "distinct cause" 2), how many remained wrong (predicted: both)? If the flip pattern doesn't match the prediction, your Q1 root-cause analysis needs revision

## After 12.5D' PR opens

1. QC pre-merge audit (standalone stream)
2. ml-architect + gto-expert reviews land
3. If all clear AND model promoted (median seed ≥ 33): orchestrator presents to owner for **12.5F ship gate**
4. If gate failed (31-32) OR hybrid overshoots (precision regression): orchestrator synthesizes for owner gate on next direction
5. On owner ship-gate APPROVE: v9 student model promoted to canonical; router updated per ml-architect §10 rollout

## What this directive supersedes

Nothing. Pivot directive PR #119 + nudge PR #121 + blueprint PR #122 + dispatch PR #125 + synthesis PR #128 + this dispatch are the active authority chain for 12.5D'.

## References

- 12.5D synthesis: `review/comms/MAIN_TERMINAL_PHASE125D_SYNTHESIS_OWNER_GATE_2026-05-04.md` (master `d6dd36d`, PR #128)
- QC convergence record: `review/comms/QC_FINDING_2026-05-04_PR126_PHASE_12_5D.md` (master `af6b82c`, PR #129)
- 12.5D BLOCKED baseline (now on master): trainer + tests + report + BLOCKED comm (master `d7d2cdd`, PR #126)
- Dispatch directive 12.5D: PR #125 (master `e3c0dfc`)
- Approved blueprint: PR #122 (master `1e4e47e`)
- Pivot directive: PR #119 (master `770b897`)
- ml-architect spec: PR #110 (master `291af80`); §11 R-2 risk register (now reversed by ml-architect Q3 empirical refutation)
- ml-architect 12.5D findings: `/tmp/ml_architect_125d_findings.md` (raw, on orchestrator host)
- gto-expert 12.5D findings: `/tmp/gto_expert_125d_findings.md` (raw, on orchestrator host)
- Memory: `feedback_qc_routing_when_standalone_active.md` (NEW 2026-05-04), `feedback_orchestrator_decides_not_recommends.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`

**Status: 12.5D' DISPATCHED. LEAD-PROGRAMMER named author. Branch `programmer/phase125d-prime-hybrid-weighting-2026-05-XX`. Path Y discipline: 4 files exactly (3 if no promotion). Gate: median seed solver-corrected ≥ 33 to promote. Owner ship gate at 12.5F.**
