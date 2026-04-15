---
date: 2026-04-15
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Track 3.5 path forward — execute feature-importance cross-check next
status: DIRECTIVE
supersedes: decision-ask portion of MAIN_TERMINAL_UPDATE_2026-04-15-b.md
---

# Main Terminal Update — 2026-04-15 (c)

Decision on Track 3.5 is made. Execute in this order.

## 1. Track 2 — launch now (if not already running)

Per `MAIN_TERMINAL_UPDATE_2026-04-15-b.md`. Deliverable:
`review/comms/EVAL_RERUN_HARDENED_2026-04-15.md`.

Include the dtype-guard extension to the hardened harness
(catches string-where-numeric-expected at eval time).

## 2. Apply Fix 1 to BP generators

Per `MAIN_TERMINAL_UPDATE_2_2026-04-15.md`. Normalise `street`
and `hero_pos` at the serialisation boundary in all 5
`review/generate_factory_*.py`. Regenerate the affected
`training-data/factory_batch*_situations.jsonl`. Do NOT
regenerate `v2_2_training.csv`. Wire the schema test as a
pre-flight gate.

## 3. Track 3.5 follow-up — v2.2 feature-importance cross-check

This is the new item. It resolves the ANOMALY-A ambiguity as
cheaply as possible before we decide whether to recover the
v2.2 training script.

**What:** Read `river-rats-core/models/v2_2_training_report.json`
and/or load `v2_2_model.json` via XGBoost and compute:

- Per-feature gain (XGBoost `feature_importances_` or booster
  `get_score(importance_type='gain')`)
- Per-feature weight (split count)
- Rank of `street` and `hero_position` among all 108 features

Report:
- Absolute and relative importance of `street` and
  `hero_position`
- Rank among the 108 features (e.g. "street is rank 14 / 108
  by gain")
- What fraction of total gain they account for
- Whether the `attn_street` / `attn_hero_position` columns
  (attention mirrors) show any unusual pattern

**Deliverable:** `review/comms/V22_FEATURE_IMPORTANCE_XCHECK_2026-04-15.md`

**No code changes. Analysis only.**

## 4. Branching on the cross-check result

The cross-check outcome determines the next step. You do not
need to wait for main terminal on the branch — pick by the
thresholds below and proceed.

### Branch A — LOW-IMPACT (street + hero_position combined < 5% of total gain, AND neither in top 20)

- ANOMALY-A is bounded. Whatever loader path v2.2 took,
  these columns carry little weight.
- **Launch Track 4 (MW miss bias deep-dive).** The GTO
  analysis can proceed without trainer recovery.
- Note in the Track 4 brief that the analysis assumes
  low-impact ANOMALY-A per cross-check. No worst-case
  disclaimer forking.

### Branch B — NON-TRIVIAL (street or hero_position in top 20 by gain, OR combined > 5% of total gain)

- **Do NOT launch Track 4.** The bias diagnosis would be
  contaminated by potential street/position corruption.
- **Start trainer recovery** — check local machines, shell
  history, any notebooks that might have produced
  `v2_2_model.json`. If no recovery possible, rewrite the
  v2.2 trainer into `river-rats-core/train_model_v2_2.py`
  from the training report and CSV schema, then rerun and
  verify it reproduces CV 93.0% ± 3.5% / holdout 88.3%.
- Deliverable: `review/comms/V22_TRAINER_RECOVERY_2026-04-15.md`
  with recovered-or-rewritten script, reproduction numbers,
  and definitive answer on how the mixed encoding was handled.
- Then launch Track 4 with the ambiguity closed.

### Branch C — AMBIGUOUS (borderline — e.g. rank 15-25, or combined 3-5% gain)

- Default to Branch B. Quality-focused; we are not in a rush.

## 5. Track 6 — still held on Track 4

No change. Track 6 starts when Track 4 delivers.

## 6. Gate 7 — still held on owner solver

No change. Gate 7-independent work continues per above.

## 7. Order of execution

You can run Tracks 2 and Fix-1-generators in parallel (they
are independent). The feature-importance cross-check is a
single programmer call and should happen next. Then branch
on result.

Commit and push each step as you complete it. One commit per
deliverable.
