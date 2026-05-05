---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-pre — cross-seed nut_flush_block importance analysis on existing 12.5E-E + 12.5G runs; settle H-FEAT validation question before 12.5H-A design
status: TRIGGER — fire now
---

# Phase 12.5H-pre — cross-seed importance analysis

QC's institutional memory addition (TC-X-CROSS-SEED-IMPORTANCE) and 12.5G chosen-seed `nut_flush_block` = 0.0054 (vs 12.5E-E chosen seed = 0.0268) raises a load-bearing question: **was the 12.5E-E H-FEAT validation real, or single-seed noise?**

This question must resolve BEFORE 12.5H-A design fires. If H-FEAT was genuinely validated (cross-seed median ≥ 0.02), 12.5H scope = corpus expansion targeting E-DIST stay-wrong patterns. If H-FEAT was single-seed noise (cross-seed median << 0.02), 12.5H scope must broaden — feature engineering or recharacterization of migration premise.

This is a small analysis (no new training); ~1-2 hour task; ≤ $0 (no API spend).

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125h-pre-crossseed-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (default — implementation)

#### Step 1: extract per-seed nut_flush_block importance from existing trainer artifacts

The 12.5E-E run (master `b51e525`) and 12.5G run (master `2135fc8`) each ran 5 seeds (0-4) on the same 604-hand corpus. Trainer module `train_model_v9_student.py` may have logged per-seed feature_importances_ during training (check trainer code at lines covering `train_one_seed` + report-write phase).

Two paths:
- **Path 1 (preferred):** if per-seed importances are in trainer report Section A's "Per-seed training summary" or similar, extract directly. Should cover all 5 seeds × 2 runs = 10 data points.
- **Path 2 (fallback):** if per-seed importances aren't reported, write a small analysis script `scripts/extract_cross_seed_importance.py` that:
  - Reads existing seed-specific model artifacts (if persisted) OR re-runs trainer with `--no-write-model` for each of seeds 0-4 on combined corpus + cap=3.0 (12.5E-E config)
  - Prints `feature_importances_` for `nut_flush_block` index per seed
  - Costs ~5-10 min runtime; no API calls

Path 1 takes precedence if data is available. Path 2 only fires if data is not on disk.

#### Step 2: produce cross-seed importance report

Output: `review/comms/BUILDER_REPORT_PHASE125H_PRE_CROSSSEED_2026-05-XX.md`. Format:

```markdown
# Cross-seed nut_flush_block importance analysis

## 12.5E-E run (cap=3.0, master b51e525)

| Seed | nut_flush_block importance |
|---|---|
| 0 | X.XXXX |
| 1 | X.XXXX |
| 2 | 0.0268 (chosen seed; from 12.5E-E report) |
| 3 | X.XXXX |
| 4 | X.XXXX |
| **Median** | **X.XXXX** |
| **Mean ± Std** | **X.XXXX ± X.XXXX** |

## 12.5G run (cap=4.0, master 2135fc8) — should be ≡ 12.5E-E since cap non-binding

| Seed | nut_flush_block importance |
|---|---|
| 0 | X.XXXX |
| 1 | X.XXXX |
| 2 | X.XXXX |
| 3 | 0.0054 (chosen seed; from 12.5G report) |
| 4 | X.XXXX |
| **Median** | **X.XXXX** |
| **Mean ± Std** | **X.XXXX ± X.XXXX** |

## Combined cross-seed (10 seeds)

| Statistic | Value |
|---|---|
| Median | X.XXXX |
| Mean ± Std | X.XXXX ± X.XXXX |
| Min | X.XXXX |
| Max | X.XXXX |
| % seeds ≥ 0.02 (ml-architect Q4 floor) | X% |

## Verdict on H-FEAT validation

- If median ≥ 0.02 (above ml-architect Q4 floor) → H-FEAT genuinely validated; 12.5H scope = E-DIST corpus expansion
- If median < 0.02 but max ≥ 0.02 → H-FEAT MARGINAL; some seeds activate the feature; 12.5H scope = E-DIST + investigate seed sensitivity
- If max < 0.02 → H-FEAT NOT validated; 12.5H scope must broaden to feature engineering or migration recharacterization

## Other P1 blocker importances (sanity check)

Same per-seed table for `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`. Note: ml-architect predicted 0.02-0.05 across blockers; was that prediction validated cross-seed for ANY blocker?
```

#### Stop conditions

- Per-seed importances unavailable on disk AND trainer doesn't expose them in current dispatch → STOP, route to architect hat to add per-seed-importance logging in next trainer touch (12.5H-E)
- Cross-seed median nut_flush_block < 0.005 → STOP, alert orchestrator (H-FEAT premise empirically refuted; 12.5H scope shifts dramatically)
- Path 2 re-run produces results inconsistent with chosen-seed values from 12.5E-E (0.0268) or 12.5G (0.0054) → STOP, debug (data integrity issue)

#### Deliverable scope

**Exactly 1 file** (or 2 if Path 2 fires):

1. `review/comms/BUILDER_REPORT_PHASE125H_PRE_CROSSSEED_2026-05-XX.md` — NEW (the analysis report)
2. `scripts/extract_cross_seed_importance.py` — NEW only if Path 2 used; UPDATE only if extending an existing analysis script

No code in `river-rats-core/`. No model artifacts. No corpus changes. No prompt changes. Pure analysis.

### LEAD-PROGRAMMER (gto-expert hat — interpretation)

After cross-seed numbers land, interpret:
- Is H-FEAT validation real, marginal, or refuted?
- What does this mean for the migration's premise?
- Does it change the 12.5H-A design priority (corpus expansion vs feature engineering vs migration recharacterization)?

Document in §"gto-expert-hat interpretation" section of the report.

### What you do NOT do

- Do NOT modify `river-rats-core/` files (this is analysis, not training)
- Do NOT touch corpus, labels, or prompts
- Do NOT re-train (Path 2 dry-run is OK; producing a model artifact is not)
- Do NOT propose 12.5H-A design (that's the next dispatch; this analysis informs but doesn't preempt it)

## QC stream — what you audit (when 12.5H-pre PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` comm pointing at the 12.5H-pre PR commit hash when builder force-pushes.

When triggered (4 audits — smaller scope; analysis-only):

1. **Diff scope** — exactly 1 file (or 2); analysis-only; no `river-rats-core/` touches
2. **Citation existence** — every file:line in report exists at master HEAD
3. **NEW: Cross-seed methodology TC-X-CROSS-SEED-IMPORTANCE applied** — verify per-seed numbers reported; verify median + std + min/max; verify chosen-seed values from 12.5E-E (0.0268) and 12.5G (0.0054) match the per-seed table entries
4. **NEW: Reproducibility** — if Path 2 was used, verify the analysis script is runnable AND deterministic (same `--seeds 0-4` produces same importances on re-run)

Post `REVIEW_QC_PHASE125H_PRE_CROSSSEED_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER step 1: extract cross-seed importances (Path 1 preferred; Path 2 fallback)
2. LEAD-PROGRAMMER step 2: write report with verdict
3. gto-expert-hat interpretation
4. PR opens
5. Orchestrator posts QC audit-now trigger
6. Standalone QC audit
7. On QC APPROVE: orchestrator merges; **branches:**
   - H-FEAT validated (median ≥0.02) → 12.5H-A design with E-DIST corpus expansion focus
   - H-FEAT marginal (median <0.02, max ≥0.02) → 12.5H-A design with E-DIST + seed-sensitivity investigation
   - H-FEAT refuted (max <0.02) → 12.5H-A design recharacterizes migration; possibly Path C (feature engineering) revisited

## What's blocked / what's queued

**Blocked:**
- 12.5H-pre PR opens → on builder analysis + report
- 12.5H-A design dispatch → on 12.5H-pre PR merge AND H-FEAT verdict
- 12.5H-B/C/D/E/F → all downstream of 12.5H-A

**Queued:**
- Per-seed importance logging in trainer module (so future runs report this directly without post-hoc extraction) → at 12.5H-E or whenever trainer is next touched
- Cap-binding pre-flight check (TC-X-CAP-BINDING-PRE-CHECK) → applies to any future cap-tuning dispatch
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete) → builder formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5G outcome: master `2135fc8` (PR #157) — cap non-binding refuted
- 12.5E-E re-train: master `b51e525` (PR #152) — chosen seed 0.0268
- 12.5G QC verdict: master `fcb88d6` (PR #159) — TC-X queued
- 12.5E-F synthesis: master `16351e1` (PR #155)
- ml-architect 12.5D' Q4 prediction (≥0.02): `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_pilot_first_for_long_jobs.md` (analysis-before-commit), `feedback_quality_default_no_ask.md` (resolve question before scaling), `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5H-pre TRIGGER posted. Cross-seed importance analysis settles H-FEAT validation question. 12.5H-A design scope branches on verdict.**
