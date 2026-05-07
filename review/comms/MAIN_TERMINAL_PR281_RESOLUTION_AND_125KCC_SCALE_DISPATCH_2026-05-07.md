---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #281 + PR #283 merged (QC PASS; 35th solo cycle); ratify Path A (re-tag MW-17 hands as RAISE; treat as unified suited-nut-FD-RAISE axis with MW-47); dispatch 12.5K-C-C-SCALE (full 200-hand 4-axis labelling)
status: DIRECTIVE — merges PR #281 + PR #283; fires LEAD-PROGRAMMER on 12.5K-C-C-SCALE — fire now
---

# PR #281 + PR #283 merge + 12.5K-C-C-SCALE dispatch

QC verdict on PR #281: **PASS — diagnosis VERIFIED**. 35th solo cycle. MW-17 axis-target shift confirmed: redesigned hands have "suited nut FD" structure that routes to RAISE per labelling pipeline (KB §1.7). This is a labelling-pipeline-canonical mismatch parallel to MW-40 graduation-fail.

## Path A ratified

**Decision: Path A.** Per `feedback_quality_default_no_ask.md` — empirically faithful labelling > forcing a structural argument that contradicts ground truth.

- **Path A (selected)**: re-tag MW-17 redesigned hands as `design_action=RAISE`; treat as unified "suited nut FD on 2-FD-suit board → RAISE" axis combined with MW-47. 100 hands of correctly-labelled RAISE training data.
- Path B (re-redesign for off-suit + low pot odds): would produce FOLD labels; doesn't help (canonical CALL is unattainable via labelling pipeline).
- Path C (drop MW-17): compromises on scale.

**Empirical convergence on stay-wrong axes:**
- **MW-40**: graduation-fail (PR #245); model layer can't be taught canonical via labelling pipeline
- **MW-17**: axis-target shift (PR #281); model layer can't be taught canonical via labelling pipeline
- **MW-45 + MW-47**: pipeline aligns with canonical RAISE; model can be taught
- Lever C augmented data: **valid 200-hand corpus expansion** with empirical labels from labelling pipeline; model trained on these will learn the pipeline's view (which differs from canonical for MW-17 + MW-40)

## LEAD-PROGRAMMER — Step: 12.5K-C-C-SCALE (fire on this comm merge)

Branch: `programmer/phase125k-c-c-scale-2026-05-07`. Base: master post-this-comm-merge.

### Scope — full-scale labelling for all 4 axes

Per design plan §5 + Path A ratification:

| Axis | Source | Pilot status | Scale-to-full count | design_action |
|---|---|---|---|---|
| MW-40 | PR #277 50 situations (preserved unchanged) | 5/5 BET | 45 more hands × 5 labellers = 225 labels | BET |
| MW-45 | PR #277 50 situations (preserved unchanged) | 5/5 RAISE | 45 more hands × 5 labellers = 225 labels | RAISE |
| MW-47 | PR #281 50 redesigned situations | 5/5 RAISE | 45 more hands × 5 labellers = 225 labels | RAISE |
| MW-17-as-RAISE | PR #281 50 redesigned situations (re-tagged Path A) | 5/5 RAISE (axis-target shifted) | 45 more hands × 5 labellers = 225 labels | RAISE (re-tagged) |

**Total full-scale: 180 more hands × 5 labellers = 900 labels. Plus existing 50 pilot labels (10 per axis × 5 labellers + 5×5 axis B pilot) = ~150 pilot labels. Final total: ~1050 labels for 200 unique hands.**

Cost: ~$45-50 LLM (900 × ~$0.05); ~30-45 min wall clock.

### What you do NOT do

- Do NOT modify MW-40 + MW-45 situations (preserved from PR #277)
- Do NOT modify MW-47 redesigned situations (PR #281)
- Do NOT change the design_action re-tagging for MW-17 from RAISE back to CALL (Path A is binding; re-tagging is the empirical truth)
- Do NOT modify v3.x prompts
- Do NOT skip per-axis convergent-reasoning verification
- Do NOT make the -E promote/no-promote call (orchestrator-scope)

### Deliverable scope

1. `data/corpus_lever_c_labels_full_2026-05-07.jsonl` (1000-1050 raw labels OR 200 consensus rows; format consistent with prior labelling outputs)
2. `data/corpus_lever_c_situations_v2_2026-05-07.jsonl` (200 situations with MW-17 design_action re-tagged to RAISE; could be in-place edit of v2 OR new v3)
3. `scripts/run_lever_c_full_labelling.py`
4. `review/comms/BUILDER_REPORT_PHASE125K_C_C_SCALE_2026-05-07.md`

## QC stream — what you audit (when -SCALE PR opens)

Standalone audit, ~15-20 min, 8-item full-scale labelling format.

QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_SCALE_2026-05-07.md`.

## Sequencing

After -SCALE merges:
- 12.5K-C-D Opus tier-up (5 canonical hands × 4 axes = 20 Opus calls)
- 12.5K-C-E corpus integration + 5-seed re-train (788 → 988 corpus)
- 12.5L gate eval

## What's blocked / what's queued

**Cleared**: PR #281 + #283 + 12.5K-C-C-SCALE dispatch.

**Queued**: 12.5K-C-D / -E + 12.5L.

**Memory candidates**: MW-17 + MW-40 are LABELLING-PIPELINE-CANONICAL MISMATCHES — augmented training data via labelling pipeline can't teach canonical action; structural argument empirically too narrow. Future verification rounds for stay-wrong axes should pre-test labelling pipeline alignment with canonical BEFORE designing data. Owner-scope to ratify.

**Status: PR #281 + #283 cleared. LEAD-PROGRAMMER fires 12.5K-C-C-SCALE (full 4-axis 200-hand labelling) on this comm merge. ~$45-50; ~30-45 min wall clock.**
