---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #269 + PR #271 merged (QC PASS; 32nd solo cycle); ratify 12.5K-C-A Lever C design; dispatch 12.5K-C-B situation generation (4-axis × ~50 hands = ~200 new corpus rows; per-axis pre-flight + ref_id namespaces)
status: DIRECTIVE — merges PR #269 + PR #271; fires LEAD-PROGRAMMER on 12.5K-C-B — fire now
---

# PR #269 + PR #271 merge + 12.5K-C-B situation generation dispatch

QC verdict on PR #269 (`REVIEW_QC_PHASE125K_C_A_LEVER_C_DESIGN_2026-05-07.md` on `qc/pr269-125kca-design-review-2026-05-07`, PR #271): **PASS**. 32nd solo cycle expected. All 7 design-phase items cleared. Lever C design ratified.

## LEAD-PROGRAMMER — Step: 12.5K-C-B situation generation (fire on this comm merge)

Per merged plan `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`. Mirror MW-40-VERIFICATION-B factory pattern, scaled to 4 axes.

Branch: `programmer/phase125k-c-b-situation-gen-2026-05-07`. Base: master post-this-comm-merge.

### Scope — 200 situations across 4 stay-wrong axes

**Per-axis target: ~50 hands.** Total: ~200 new corpus rows.

| Axis | Target action | ref_id namespace | Approximate count |
|---|---|---|---|
| MW-17 | CALL | `PILOT_LEVER_C_MW17_001..050` | 50 |
| MW-40 | BET | `PILOT_LEVER_C_MW40_001..050` | 50 |
| MW-45 | RAISE | `PILOT_LEVER_C_MW45_001..050` | 50 |
| MW-47 | RAISE | `PILOT_LEVER_C_MW47_001..050` | 50 |

Builder consults the merged plan for per-axis structural specs (constraint tables, sub-axis variants, blocker variation per `feedback_solver_findings.md` finding 2).

### Per-axis pre-flight 4-check (Hybrid pilot-first; binding per `feedback_pilot_first_for_long_jobs.md`)

Mirror MW-40-VERIFICATION-B Path 3 Hybrid pre-flight: emit FIRST 5 of each axis (5 × 4 = 20 total pre-flight situations), then run 4-check validation:

1. **Schema parity** — 61-surface; 0 NaN/Inf/missing keys
2. **Step-18 feature plausibility** — both ≈ 0 across most variants (per axis structural pattern; document predicted activation rates per axis in builder report)
3. **ref_id namespace integrity** — disjoint vs 788-corpus + prior 12.5I namespaces + cross-axis disjoint
4. **Top-level structural fields** — match plan §3 constraint tables PER AXIS

If ALL 4 checks pass on 20 pre-flight situations → emit remaining 30 per axis (180 more). If ANY check fails → STOP and report.

### Stop conditions

- Pre-flight fails any 4 checks → STOP
- ref_id collision → STOP
- ≥1% NaN/Inf across 200 × 61 = 12200 values → STOP
- Per-axis count not exactly 50 → STOP
- design_action ≠ axis target on any emitted situation → STOP

### What you do NOT do

- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source (read-only import)
- Do NOT modify BATCH2 reference
- Do NOT touch existing 788-corpus or labels
- Do NOT label hands (12.5K-C-C scope; separate dispatch)
- Do NOT skip the 4-check pre-flight (binding)

### Cost / time

~$0 (factory script; no LLM). ~20-30 min wall clock for 200 situations + report.

### Deliverable scope

1. `data/corpus_lever_c_situations_2026-05-07.jsonl` (200 situations; 61-surface)
2. `scripts/generate_lever_c_situations.py` (factory script per CLAUDE.md provenance)
3. `review/comms/BUILDER_REPORT_PHASE125K_C_B_SITUATION_GEN_2026-05-07.md`

## QC stream — what you audit (when -B PR opens)

Standalone audit, ~10-15 min, 7-item scope:

1. Diff scope strict — exactly the 3 files (+ optional script) per dispatch
2. Pre-flight 4-check executed on 20 pre-flight situations (5 × 4 axes) BEFORE remaining emit
3. 200 situations / 50 per axis exact; ref_id namespaces disjoint
4. Schema 61-surface uniform; 0 NaN/Inf
5. Step-18 activation pattern matches plan predictions per axis
6. TC-X-OWNER-SCOPE-DISCIPLINE
7. TC-X-DISPATCH-COMPLIANCE 12th formal exercise

QC writes `review/comms/REVIEW_QC_PHASE125K_C_B_SITUATION_GEN_2026-05-07.md`.

## Sequencing — what fires after 12.5K-C-B merges

1. 12.5K-C-C labelling round (5 Sonnet × 200 hands; per-axis pilot-first 5-hand gate; ~$50-80; ~2-3h)
2. 12.5K-C-D Opus tier-up (20 Opus calls × 4 axes × 5 canonical; ~$15-20)
3. 12.5K-C-E corpus integration + re-train (788 → 988 corpus; 5-seed re-train; reference set spot-check)
4. 12.5L gate evaluation

## What's blocked / what's queued

**Cleared**: PR #269 + #271 merge + 12.5K-C-B fires.

**Queued**: 12.5K-C-C / -D / -E + 12.5L.

## References

- 12.5K-C-A merged plan: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`
- 12.5I-MW40-VERIFICATION-B precedent: `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_findings.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: PR #269 + #271 cleared for merge. LEAD-PROGRAMMER fires 12.5K-C-B (200 situations × 4 axes; per-axis pre-flight 4-check) on this comm merge. ~$0; ~20-30 min wall clock.**
