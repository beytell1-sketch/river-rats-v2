---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #257 + PR #259 merged (QC PASS+0/0/1NIT; 29th solo cycle); ratify 12.5K design + sequence A→B→C; dispatch 12.5K-A execution (Lever A: 15 additional seeds; 2-seed pilot gate)
status: DIRECTIVE — merges PR #257 + PR #259; fires LEAD-PROGRAMMER on 12.5K-A — fire now
---

# PR #257 + PR #259 merge + 12.5K design ratification + 12.5K-A Lever A dispatch

QC verdict on PR #257 (`REVIEW_QC_PHASE125K_COMBINED_RETRAIN_DESIGN_2026-05-06.md` on `qc/pr257-125k-design-review-2026-05-06`, PR #259): **PASS — 0 BLOCKER, 0 SHOULD_FIX, 1 NIT (cost-budget arithmetic).** 29th solo cycle expected. All 7 design-phase audit items PASS. Plan structure sound (3 levers analyzed; sequenced recommendation; pilot-first gates per lever; cost/time budget under cap; owner-scope perimeter held; dispatch-compliance verified).

NIT-1 (cost-budget arithmetic) is advisory — minor calculation issue in plan §7 cost summary (per-lever sub-totals don't precisely add to the headline ~$85; minor rounding-or-summary issue, not structural). Carry-forward as a footnote-correction in the next 12.5K-related comm or 12.5L gate eval; non-blocking.

## 12.5K design ratification

Builder's plan analyzed 3 levers comprehensively:
- **Lever A** (more seeds): 15 additional seeds (Seeds 5-19) on existing 788-corpus 61-surface config; 2-seed pilot (Seeds 5-6) gate; ~$0 / ~90 min wall clock
- **Lever B** (hyperparameter sweep): CV-driven on 788-corpus 61-surface; ~$0 / ~10-20 hours
- **Lever C** (augmented data): targeted labelling round on stay-wrong axes; ~$50-200 / ~2-5 hours

Sequenced recommendation: **A → B → C** with off-ramps at each gate. Total budget ~$85 / ~9.5 hours (well under $300/30h cap).

**Decision: Path A→B→C ratified.** This is the slow-quality default sequence (cheapest+most-informative-first; ruling out variance hypothesis before investing in B/C). Lever A's 15 additional seeds also serve as variance characterization for ANY future re-train (whether Lever B or C subsequently lifts the mean).

### Outcome interpretation matrix (orchestrator decisions on Lever A pilot gate)

Per plan §3:

| Lever A 7-seed aggregate | Action |
|---|---|
| **Mean ≥ 34.0/40 within 1-σ** (e.g., observed mean 33.7 ± 0.5) | PROMOTE; Lever A succeeds; off-ramp Lever B and C; dispatch 12.5L gate eval |
| **Mean ≈ 33.20/40 ± 0.40 (replicates existing 5-seed)** | Variance-bound finding confirmed; conclude 12.5J adds no measurable lift; proceed to Lever B with this finding documented |
| **Mean < 33.0/40 (worse than existing)** | Negative; surface for orchestrator (possibly indicates training instability; Lever B may be premature — could indicate a bug or warm-start issue) |

The 2-seed pilot (Seeds 5+6 only) at Lever A's pilot-first gate fires the same outcome interpretation but at 7-seed total (5 existing + 2 pilot). On pilot PASS → scale to full 15 (Seeds 5-19). On pilot FAIL → orchestrator decides retry or escalate.

## LEAD-PROGRAMMER — Step: 12.5K-A Lever A execution (fire on this comm merge)

Per plan `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` §3 "Lever A — more seeds" + §3 "Pilot-first gate".

Branch: `programmer/phase125k-a-more-seeds-2026-05-06`. Base: master post-this-comm-merge.

### Scope — Seeds 5-19 (15 new seeds) on existing config; 2-seed pilot first

#### Pilot batch (Seeds 5 + 6 only)

Train 2 models with seeds 5 and 6 using the SAME config as PR #253:
- Corpus: `data/corpus_combined_788_2026-05-06.jsonl`
- Labels: `data/corpus_combined_788_labels_2026-05-06.jsonl`
- Trainer: `river-rats-core/train_model_v9_student.py` (existing; reuse)
- Hyperparameters: per PR #253 (n_estimators=800, max_depth=5, learning_rate=0.05, etc. — verbatim from plan §3)
- Warm-start: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (same anchor)
- Confidence weighting: `pure` (per PR #253)
- Class-weight cap (hybrid): `3.0` (per PR #253)
- Test size: 0.2 (per PR #253)
- Reference set: `mw_11_50` (40 hands; per PR #253)
- Output paths: `river-rats-core/models/125k_a/v9_3way_125k_a_seed_5.json` and `..._seed_6.json` (or naming consistent with prior PR #253 convention)

Cost: ~$0 LLM; ~12-15 min wall clock for 2 seeds. Provenance per CLAUDE.md addendum (commit hash → model artifact docstring link).

#### Pilot gate (after 2-seed pilot completes)

Build 7-seed aggregate (5 existing seeds 0-4 from PR #253 + 2 pilot seeds 5-6 from this PR):

| Gate criterion | Continue (scale to Seeds 7-19) if... | Off-ramp (route to orchestrator) if... |
|---|---|---|
| Per-seed solver-corrected scores | Both pilot seeds (5+6) in [32, 35] range | Either pilot seed < 30 OR all-same-class predictions on reference set → STOP |
| Schema integrity | 788/788 join clean; 61-surface uniform; 40-hand reference eval produces predictions | Schema mismatch on either pilot seed → STOP |
| Aggregate over 7 seeds | Mean ≥ 33.0/40 AND std ≤ 1.0 | Mean < 32.5/40 OR std > 1.0 → STOP (variance won't converge) |

If ALL gate criteria PASS → continue to full run (Seeds 7-19).

#### Full run (Seeds 7-19; 13 additional seeds; on pilot gate PASS)

Train 13 more seeds. Total 20-seed aggregate (Seeds 0-19) becomes the empirical record.

Cost: ~$0 LLM; ~78-100 min wall clock (~6-7.5 min/seed × 13).

### Reference set spot-check (full run)

For each of the 20 seeds, run the 40-hand reference set inference. Aggregate per-seed predictions per PR #253 pattern. Builder report sections (mandatory):

- §"Pilot 2-seed gate" — pilot 7-seed aggregate + gate decision
- §"Full 13-seed sweep" — Seeds 7-19 individual + aggregate
- §"20-seed aggregate" — final mean, median, std on solver-corrected; comparison vs baseline 34/40
- §"Per-stay-wrong subset detail" — MW-17 / MW-40 / MW-45 / MW-47 across 20 seeds (does any single seed flip any stay-wrong?)
- §"Variance characterization conclusion" — interpret the result per the 3-case matrix above (PROMOTE / variance-bound / negative)
- §"Provenance" — 15 new model artifacts × commit hash links

### Stop conditions

- Pilot gate fails (per matrix above) → STOP
- Trainer crash on any seed → STOP (route to orchestrator)
- Schema mismatch → STOP
- Reference set inference fails on any 40-hand pass → STOP
- Solver-as-labels appears → STOP
- 20-seed aggregate variance > 1.5 std (high training instability) → REPORT (not STOP); orchestrator decides

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source EXCEPT the trainer (read-only reuse; no source edits to trainer logic; only output paths if needed)
- Do NOT modify BATCH2 reference
- Do NOT modify the 788-corpus or labels
- Do NOT change hyperparameters (this lever is variance characterization; same config as PR #253)
- Do NOT change warm-start anchor (same v9-3way-v2.2)
- Do NOT skip the 2-seed pilot gate (binding per `feedback_pilot_first_for_long_jobs.md`)
- Do NOT make the PROMOTE decision (orchestrator-scope per `feedback_orchestrator_decides_not_recommends.md`)

### Cost / time

~$0 LLM; ~90 min wall clock (15 seeds × ~6 min each). Pilot 2-seed: ~12-15 min. Full 13-seed: ~78-100 min.

### Deliverable scope

Expected files in PR diff:
1. `river-rats-core/models/125k_a/v9_3way_125k_a_seed_5.json` ... `_seed_19.json` (15 new model artifacts)
2. `data/inference_125k_a_reference_predictions_2026-05-06.jsonl` (or 20-seed-aggregate inference output; format consistent with PR #253)
3. `review/comms/BUILDER_REPORT_PHASE125K_A_MORE_SEEDS_2026-05-06.md` (the report)
4. Optionally a small training-orchestration script in `river-rats-core/` if needed (per CLAUDE.md provenance discipline; reuse existing `train_model_v9_student.py` is preferred)

## QC stream — what you audit (when 12.5K-A PR opens)

Standalone audit, ~15-20 min, 8-item training-output scope (mirror PR #253 audit but on 15-seed scale):

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly 15 model artifacts + inference output + builder report. Verify NO touch to v3.x prompts / BATCH2 / training-data corpora / unrelated `river-rats-core/` / plan / memory.
2. **Provenance integrity** — 15 model artifacts each have commit-hash-to-artifact docstring link.
3. **Pilot 2-seed gate executed** — builder report shows 2-seed pilot result + gate decision before scaling to remaining 13.
4. **20-seed aggregation correctness** — math correct (mean / median / std on solver-corrected); claim "20-seed mean = X.YZ ± W.AB" verifies against per-seed values.
5. **Reference set spot-check completeness** — all 40 hands × 20 seeds = 800 predictions. All 4 stay-wrong hands have detailed per-seed breakdowns.
6. **Variance characterization conclusion** — builder report's Section "Variance characterization conclusion" matches the 3-case matrix (PROMOTE / variance-bound / negative); orchestrator decides; builder doesn't auto-promote.
7. **TC-X-OWNER-SCOPE-DISCIPLINE** — BATCH2 unchanged; reference labels NOT updated; hyperparameters / warm-start NOT changed (this lever is pure variance characterization).
8. **TC-X-DISPATCH-COMPLIANCE (9th formal exercise)** — pilot-first gate executed; 15 new seeds (no fewer; not skipped); same config as PR #253 (no hyperparameter drift); 20-seed aggregate vs baseline reported.

QC writes `review/comms/REVIEW_QC_PHASE125K_A_MORE_SEEDS_2026-05-06.md` on `qc/pr<N>-125ka-review-2026-05-06`.

## Sequencing — what fires after 12.5K-A merges (per outcome)

Per plan §3 outcome matrix + this dispatch's sequencing:

1. **Mean ≥ 34.0/40 within 1-σ** → 12.5L gate eval dispatch (PROMOTE; off-ramp Lever B+C)
2. **Mean ≈ 33.20/40 ± 0.40 (variance-bound)** → 12.5K-B Lever B (hyperparameter sweep) dispatch
3. **Mean < 33.0/40 (negative)** → orchestrator escalation; Lever B may be premature

## What's blocked / what's queued

**Cleared by this comm:**
- PR #257 merge (Builder 12.5K design)
- PR #259 merge (QC verdict record)
- 12.5K-A Lever A execution dispatch fires
- 12.5K design ratified A → B → C sequence
- NIT-1 (cost-budget arithmetic) recorded as carry-forward

**Newly queued (after 12.5K-A merges, conditional on outcome):**
- PROMOTE outcome → 12.5L gate eval
- Variance-bound outcome → 12.5K-B Lever B (hyperparameter sweep)
- Negative outcome → orchestrator escalation

**Still queued (later):**
- 12.5K-C Lever C (augmented data; gates on Lever B outcome)
- 12.5L gate evaluation (gates on full 12.5K complete OR PROMOTE-on-A)

**Owner-scope items pending (informational, non-blocking):**
- TC-X-INTRA-PLAN-CONSISTENCY ratification
- TC-X-DISPATCH-COMPLIANCE ratification (now 8+ exercises)
- Memory note refresh for "composition quad" vs "composition triple" terminology
- "Structural arguments must cross-check against v3.4 DO NOT rules" standing-rule candidate
- "12.5J-E neutral result" memory candidate

## References

- PR #257 (Builder 12.5K design): branch `programmer/phase125k-combined-retrain-design-2026-05-06`
- PR #259 (QC PASS+1NIT verdict): branch `qc/pr257-125k-design-review-2026-05-06`
- PR #258 (QC trigger): master `2021444`
- PR #256 (orchestrator: 12.5K design dispatch): master `4e55ff4`
- PR #253 (12.5J-E source data; baseline for variance characterization): master `2b6aa02`
- 12.5K master plan (with §3 Lever A spec): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- v9-3way-v2.2 baseline: 34/40 solver-corrected (CLAUDE.md project state)
- Memory: `feedback_quality_default_no_ask.md` (A→B→C sequence per slow-quality default), `feedback_orchestrator_decides_not_recommends.md` (orchestrator dispatches each lever), `feedback_pilot_first_for_long_jobs.md` (2-seed pilot gate at Lever A), `feedback_orchestration_efficiency_rules.md` (single comm: ratification + dispatch)

**Status: PR #257 + PR #259 cleared for merge. 12.5K design A→B→C sequence ratified. LEAD-PROGRAMMER fires 12.5K-A Lever A (15 additional seeds; 2-seed pilot first) on this comm merge. ~$0 LLM; ~90 min wall clock to PR open.**
