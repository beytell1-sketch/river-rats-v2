---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #289 + PR #291 merged (QC PASS; 37th solo cycle; 20/20 Sonnet-Opus match across 4 axes); ratify Lever C corpus expansion; dispatch 12.5K-C-E corpus integration + 5-seed re-train (788 → 988-corpus)
status: DIRECTIVE — merges PR #289 + PR #291; fires LEAD-PROGRAMMER on 12.5K-C-E — fire now
---

# PR #289 + PR #291 merge + 12.5K-C-E (corpus integration + 5-seed re-train) dispatch

QC verdict on PR #289: **PASS**. 37th solo cycle. Opus tier-up validated Path A — 20/20 Sonnet-Opus match across 4 axes (100%). Strongest possible empirical signal that the 200-hand augmented corpus has high label quality.

## LEAD-PROGRAMMER — Step: 12.5K-C-E (fire on this comm merge)

Per merged plan `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` §5 + dispatch §"Phase 5: Corpus integration + re-train".

Branch: `programmer/phase125k-c-e-corpus-and-retrain-2026-05-07`. Base: master post-this-comm-merge.

### Scope — corpus integration + 5-seed re-train + reference-set evaluation

#### Phase 1: Corpus integration (788 → 988)

Merge the 200 Lever C hands (with Sonnet consensus labels + Path A re-tagging applied) into the 788-row canonical corpus. Output: `data/corpus_combined_988_2026-05-07.jsonl` + `data/corpus_combined_988_labels_2026-05-07.jsonl` (61-surface uniform; 988 rows × 61 features).

**Constraints**:
- ref_id namespace disjoint (788-corpus + 200 Lever C with `PILOT_LEVER_C_<AXIS>_*`)
- 61-surface schema clean (mirror PR #222 12.5I-D pattern)
- Distribution sanity: report per-action breakdown across 988 (BET / CHECK / CALL / FOLD / RAISE)

#### Phase 2: 5-seed re-train

Same trainer + hyperparameters + warm-start as PR #253 / PR #261 (variance characterization). 5 seeds (Seeds 0-4 on 988-corpus).

**Pilot-first 1-seed gate**: 1-seed pilot first; verify trainer ingests 988 cleanly; gate on schema integrity + reference-set inference success. Then scale to remaining 4 seeds.

#### Phase 3: Reference set spot-check + comparison

For each of the 5 seeds:
- 40-hand reference set inference
- Per-stay-wrong subset detail (MW-17, MW-40, MW-45, MW-47)
- Solver-corrected per-hand comparison

Aggregate 5-seed mean / median / std comparison vs:
- v9-3way-v2.2 baseline: 34/40 raw / 34/40 solver-corrected
- PR #261 20-seed mean: 33.10/40 ± 0.30 (788-corpus)

**Outcome matrix**:
| 988-corpus 5-seed mean | Action |
|---|---|
| Mean ≥ 34.5/40 within 1-σ | PROMOTE; Lever C succeeded; off-ramp 12.5K-D and ship |
| Mean in [34.0, 34.5) (parity or slight improvement) | REPORT; orchestrator decides ship-or-defer |
| Mean in [33.10, 34.0) (improvement vs PR #261 but below baseline) | REPORT; orchestrator decides whether augmented data is partial-lift-worth-shipping |
| Mean ≈ 33.10/40 ± 0.30 (no improvement vs PR #261) | NULL result; document; consider follow-up Lever D or accept ceiling |
| Mean < 33.0/40 (regression) | NEGATIVE; surface for orchestrator |

### Cost / time

- Phase 1 corpus integration: ~$0; ~10-15 min (mechanical assembly script)
- Phase 2 5-seed re-train: ~$0; ~30-90 min (5 seeds × ~6-15 min each)
- Phase 3 reference-set + report: ~$0; ~15-20 min
- Total: ~$0; ~1-2 hours wall clock

### What you do NOT do

- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source EXCEPT new corpus assembly script if needed (per CLAUDE.md provenance)
- Do NOT modify BATCH2 reference
- Do NOT modify the 788-corpus or 200 Lever C labels (read-only training inputs)
- Do NOT skip the 1-seed pilot gate
- Do NOT auto-promote (orchestrator-scope decision per outcome matrix)

### Deliverable scope

1. `data/corpus_combined_988_2026-05-07.jsonl` (988 rows; 61-surface)
2. `data/corpus_combined_988_labels_2026-05-07.jsonl` (988 rows)
3. `scripts/assemble_125k_c_e_988.py` (corpus integration script)
4. `river-rats-core/models/v9_3way_125k_c_e_seed_0..4.json` (5 model artifacts)
5. `data/inference_125k_c_e_reference_predictions_2026-05-07.jsonl` (200 predictions)
6. `review/comms/BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md`

## QC stream — what you audit (when -E PR opens)

Standalone audit, ~15-20 min, 9-item corpus-integration-and-retrain format. Focus on:
- Corpus 988-row integrity (788 + 200; ref_id namespace disjoint; 61-surface uniform)
- 5-seed aggregation correctness
- Reference set spot-check completeness
- Outcome interpretation matches the matrix per dispatch
- TC-X-DISPATCH-COMPLIANCE 17th formal exercise

QC writes `review/comms/REVIEW_QC_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md`.

## Sequencing

After -E merges + outcome interpretation:
- PROMOTE / improvement → 12.5L gate evaluation dispatch (PROMOTE-and-ship pattern)
- NULL / negative → orchestrator decides next step (Lever D? Accept ceiling? Re-design Lever C?)

**Status: PR #289 + #291 cleared. LEAD-PROGRAMMER fires 12.5K-C-E (corpus integration + 5-seed re-train; pilot-first 1-seed gate) on this comm merge. ~$0; ~1-2h wall clock.**
