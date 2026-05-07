---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #273 + PR #275 merged (QC PASS; 33rd solo cycle); ratify 12.5K-C-B situation gen; dispatch 12.5K-C-C Lever C labelling round (5 Sonnet × 200 hands; per-axis pilot-first 5-hand gate)
status: DIRECTIVE — merges PR #273 + PR #275; fires LEAD-PROGRAMMER on 12.5K-C-C — fire now
---

# PR #273 + PR #275 merge + 12.5K-C-C labelling round dispatch

QC verdict on PR #273: **PASS**. 33rd solo cycle. Lever C situation gen ratified — 200 situations × 4 stay-wrong axes (50 each), per-axis 4-check pre-flight PASS, ref_id namespaces disjoint.

## LEAD-PROGRAMMER — Step: 12.5K-C-C labelling round (fire on this comm merge)

Per merged plan `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`. Mirror MW-40-VERIFICATION-C labelling pattern (5 Sonnet × N hands; pilot-first per-axis gate).

Branch: `programmer/phase125k-c-c-labelling-2026-05-07`. Base: master post-this-comm-merge.

### Scope — 5 Sonnet labellers × 200 hands; per-axis pilot-first 5-hand gate

Source corpus: `data/corpus_lever_c_situations_2026-05-07.jsonl` (PR #273 merged; 200 situations; 61-surface). v3.4 prompt (`prompts/gto_labeller_v3.4.md`; locked).

### Per-axis pilot-first 5-hand gate (binding per `feedback_pilot_first_for_long_jobs.md`)

Per axis: emit 5 hands × 5 Sonnet labellers = 25 labels (~$1-2 cost; ~5 min wall clock). Examine pilot consensus per axis BEFORE scaling that axis to remaining 45 hands.

| Per-axis pilot gate | Continue if... | Off-ramp if... |
|---|---|---|
| ≥4/5 hands consensus on axis target action | Scale axis to full 50 | <4/5 consensus → REPORT to orchestrator (parallel of MW-40-VERIFICATION-C HALT pattern); surface for orchestrator decision per axis |
| Sonnet API errors | <5% on pilot | >5% → STOP infrastructure |
| Reasoning convergence | Convergent reasoning | Mode-collapse → STOP |

Per-axis off-ramp: failed axis dropped from -E corpus integration; orchestrator decides whether to re-design that axis.

### Cost / time

- Per-axis pilot: ~$1-2; ~5-10 min × 4 axes = ~$5-8; ~20-40 min total pilot
- Full run (axes that pass pilot): ~$8-10 per axis × up to 4 axes = ~$32-40
- Total: ~$40-50 LLM; ~2-3 hours wall clock
- Within ~$300/30h budget cap

### What you do NOT do

- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/
- Do NOT modify BATCH2 / 788-corpus / corpus_lever_c situations
- Do NOT skip per-axis pilot gates (binding)
- Do NOT auto-decide off-ramp; route to orchestrator
- Do NOT use solver-as-labels
- Do NOT make the -E promote/no-promote call (orchestrator-scope after -D + -E)

### Deliverable scope

1. `data/corpus_lever_c_labels_2026-05-07.jsonl` (consensus labels per hand; or raw labels per labeller-hand)
2. `scripts/run_lever_c_labelling.py`
3. `review/comms/BUILDER_REPORT_PHASE125K_C_C_LABELLING_2026-05-07.md`

## QC stream — what you audit (when -C PR opens)

Standalone audit, ~15-20 min, 8-item scope (training-data labelling format):

1. Diff scope strict
2. Pilot-first gate executed per-axis
3. Row count integrity (200 hands × 5 labellers = 1000 labels; or 200 consensus rows)
4. Reasoning convergence per axis
5. No solver-as-labels
6. Schema integrity
7. TC-X-OWNER-SCOPE-DISCIPLINE
8. TC-X-DISPATCH-COMPLIANCE 13th formal exercise

QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_LABELLING_2026-05-07.md`.

## Sequencing

After -C: 12.5K-C-D Opus tier-up (20 Opus × 4 axes × 5 canonical) → -E corpus integration + 5-seed re-train → 12.5L gate eval.

**Status: PR #273 + #275 cleared. LEAD-PROGRAMMER fires 12.5K-C-C labelling on this comm merge. ~$40-50 / ~2-3h.**
