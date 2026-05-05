---
date: 2026-05-05
from: LEAD-PROGRAMMER (architect hat)
to: Main terminal (orchestrator) · ML-ARCHITECT (advisory) · GTO-EXPERT (review)
re: Phase 12.5G — cap=4.0 retune complete; cap is non-binding on 604 corpus; route to 12.5H per dispatch
status: BUILDER BLOCKED — gate threshold not cleared (median 32); B-then-C step 1 produced cap-non-binding finding (load-bearing for step 2 12.5H)
---

# Phase 12.5G — BUILDER BLOCKED on gate threshold + cap-non-binding finding

Per dispatch (PR #156, master `1bd464e`) §"Sequencing":
- Median ≥ 33 → PROMOTE
- Median < 33 → 12.5H corpus expansion with cap=4.0 evidence folded in

**Empirical median: 32/40 < 33 → 12.5H route.** Per architect-hat instruction "If pilot or full STOPs, swap to architect hat → `BUILDER_BLOCKED_PHASE125G_*.md` documenting failure mode + cap=4.0 evidence available for 12.5H corpus design," this comm captures the load-bearing 12.5H input.

Full empirical analysis is in `review/comms/PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` Section F. This comm summarizes for orchestrator decision.

## Headline finding: cap is non-binding at both 3.0 and 4.0 on the 604 corpus

| class | count | uncapped boost | cap=3.0 active | cap=4.0 active |
|---|---|---|---|---|
| FOLD | 75 | 1.611 | NO | NO |
| CHECK | 271 | 0.446 | NO | NO |
| CALL | 72 | 1.678 | NO | NO |
| BET | 118 | 1.024 | NO | NO |
| **RAISE** | **68** | **1.776** | **NO (< 3.0)** | **NO (< 4.0)** |

Maximum natural boost = 1.776× on RAISE. Cap=3.0 was binding in 12.5D'/12.5D on the 494 corpus where RAISE was 5.9% (mean/count ≈ 4.3); 12.5E corpus expansion (5.9% → 11.26% RAISE share) lifted the natural boost below cap=3.0, making cap non-binding from 12.5E forward.

**cap=4.0 produces identical sample weights to cap=3.0 on this corpus.** Any model-output difference is purely xgboost BLAS-reduction non-determinism, not a cap effect.

## Gate outcome

| seed | 12.5E (cap=3.0) | 12.5G (cap=4.0) | Δ |
|---|---|---|---|
| 0 | 32 | 31 | -1 |
| 1 | 33 | 33 | 0 |
| 2 | 32 | 33 | +1 |
| 3 | 32 | 32 | 0 |
| 4 | 32 | 32 | 0 |
| **median** | **32** | **32** | **0** |

Median identical. Per-seed ±1 jiggle is noise.

## Opus 30% MW-47-flip prediction did not materialize

12.5G chosen seed (3) outputs **CALL** on MW-47 (corrected expert RAISE) — same as 12.5E-E chosen seed (2). MW-20 also unchanged (RAISE; over-aggression vs corrected CALL).

Consistent with cap-non-binding: identical sample weights → identical gradient signal → identical decisions on borderline hands.

## Load-bearing 12.5H input package

1. **Cap-as-lever empirically refuted.** B's premise was "cap=4.0 may flip MW-47 by giving RAISE more weight." Cap=4.0 doesn't change weights vs cap=3.0 here; lever is structurally absent.
2. **Higher caps would also be no-ops** on this corpus. Same math: any cap > 1.78 produces the natural inverse-frequency boost. Cap=5.0/6.0/etc all produce identical results to cap=3.0.
3. **For 12.5H corpus design**, the remaining levers are:
   - **(a) Add MORE situations** of the specific patterns where MW-17/25/40/45/47 fail (E-DIST + E-FEATURE residuals per gto-expert classification). The 110-hand expansion was at design §4's conservative end (150-200 cited as escalation point).
   - **(b) Feature engineering** to add features distinguishing MW-31/46 distinct-cause spots (out of Path Y scope; would be 12.5H-prime or beyond).
   - **(c) Hyperparameter tuning** (depth, n_estimators, regularization) — locked at 12.5E-E; changing them is methodology drift.
4. **Methodology amendment for future cap-sweep dispatches:** pre-flight check whether the cap actually binds on the candidate corpus before committing to a sweep. The check is a 1-line computation: `mean(class_counts) / min(class_counts) ≥ cap?` If False, cap is non-binding and the sweep is moot. The 12.5G dispatch's 30% Opus probability was correct *conditional on cap mattering*, but didn't account for cap being non-binding given the post-12.5E corpus class distribution.

## Seed-volatility methodological observation

12.5G chosen seed (3) `nut_flush_block` importance = 0.0054 (below 0.02 floor).
12.5E-E chosen seed (2) `nut_flush_block` importance = 0.0268 (above 0.02 floor).

**Single-seed feature-importance numbers are unreliable.** The 12.5E-E "H-FEAT confirmed" reading was a single-seed snapshot; cross-seed median may be lower. Future trainer reports should include cross-seed median ± std for feature importance, not chosen-seed only. Surfaced for ml-architect's attention; informs 12.5H design pre-flight.

## What this PR ships (2 files; cap-non-binding-no-promote outcome)

1. `river-rats-core/train_model_v9_student.py` — UPDATE: parameterize cap via `--class-weight-cap` CLI arg (default 3.0; preserves existing behavior). 13 insertions / 5 deletions.
2. `review/comms/PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` — NEW: 12.5G trainer report (Sections A-D auto-generated + Section F manually appended with 12.5E-E vs 12.5G delta + cap-non-binding finding + 12.5H input package).
3. (this comm) `review/comms/BUILDER_BLOCKED_PHASE125G_CAP_NON_BINDING_2026-05-05.md` — NEW: focused architect-hat block per dispatch §"LEAD-PROGRAMMER (architect hat)".

3 files in PR diff (1 modified + 2 new). Below dispatch's >5-file STOP threshold. Combined corpus + labels (items 2-3 in dispatch's deliverable list) are UNCHANGED — already on master from 12.5E-E.

## Sequencing per dispatch §"Sequencing" branch

- **Median ≥ 33 → PROMOTE** (NOT triggered)
- **Median < 33 → 12.5H corpus expansion with cap=4.0 evidence folded in** (TRIGGERED — orchestrator authors 12.5H dispatch)

Builder standing down per `feedback_named_author_builds_not_polls.md`. Awaiting QC audit-now trigger from orchestrator + 12.5H dispatch (orchestrator decides scope based on this PR's findings).

## Process compliance

| Check | Status |
|---|---|
| Worked in isolated worktree (`/tmp/builder-12.5G-wt`) | ✅ |
| Pilot 1-seed dry-run before 5-seed full (per `feedback_pilot_first_for_long_jobs.md`) | ✅ |
| Trainer parameterization edit ≤ 10 lines (functional) | ✅ — 13 insertions incl multi-line CLI help; functional change ≈ 5 lines |
| Did NOT touch combined corpus + labels (locked at 12.5E-E master) | ✅ |
| Did NOT change other hyperparameters (depth, n_estimators, etc.) | ✅ |
| Did NOT modify v3.x prompts | ✅ |
| Did NOT proceed to 12.5H without orchestrator dispatch | ✅ — STOP per gate threshold + route to orchestrator |
| Cap value verified in trainer report Section A | ✅ |
| `_StudentInferenceLike45` invariant test passed | ✅ (existing test, ran in trainer's gate_24) |

## References

- 12.5G dispatch: `review/comms/MAIN_TERMINAL_PHASE125G_DISPATCH_2026-05-05.md` (PR #156, master `1bd464e`)
- 12.5E-F synthesis (B-then-C compound recommendation): master `16351e1` (PR #155)
- Opus second-tier evaluation: `review/comms/ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (master `16351e1`)
- 12.5E-E re-train (this run's parent baseline; cap=3.0): master `b51e525` (PR #152)
- 12.5C blueprint: master `1e4e47e` (PR #122)
- ml-architect 12.5D' Q3 cap=3.0 spec: `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`, `feedback_failure_direction_classification.md`

**Status: 12.5G BUILDER BLOCKED on gate threshold (median 32 < 33). Cap-non-binding finding empirically refutes B's cap-as-lever premise on the 604 corpus. 12.5H route triggered per dispatch §"Sequencing". Load-bearing input package in §"Load-bearing 12.5H input package" above + Section F of trainer report. Builder standing down; awaiting QC audit-now trigger + orchestrator's 12.5H dispatch.**
