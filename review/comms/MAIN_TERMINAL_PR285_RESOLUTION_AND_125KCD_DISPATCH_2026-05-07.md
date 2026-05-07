---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #285 + PR #287 merged (QC PASS; 36th solo cycle); ratify Lever C 700-label corpus expansion; dispatch 12.5K-C-D Opus tier-up (20 Opus × 4 axes × 5 canonical)
status: DIRECTIVE — merges PR #285 + PR #287; fires LEAD-PROGRAMMER on 12.5K-C-D — fire now
---

# PR #285 + PR #287 merge + 12.5K-C-D Opus tier-up dispatch

QC verdict on PR #285: **PASS**. 36th solo cycle. Lever C SCALE ratified — 700 labels on 200-hand corpus expansion across 4 stay-wrong axes; Path A applied (MW-17 re-tagged as RAISE).

## LEAD-PROGRAMMER — Step: 12.5K-C-D Opus tier-up (fire on this comm merge)

Per merged plan `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` §5 + dispatch §"Phase 4: Opus tier-up". Mirror MW-40-VERIFICATION-D Opus tier-up pattern.

Branch: `programmer/phase125k-c-d-opus-tierup-2026-05-07`. Base: master post-this-comm-merge.

### Scope — 20 Opus 4.7 calls (5 canonical hands per axis × 4 axes)

Select 5 canonical hands per axis from the merged 200-hand corpus. Run Opus 4.7 with v3.4 prompt; compare with Sonnet labels (per `feedback_pilot_first_for_long_jobs.md` sub-rule for training-data outputs).

| Axis | Sonnet target | Opus tier-up calls |
|---|---|---|
| MW-40 (BET) | 5/5 BET pilot; full PASS | 5 Opus calls; expect BET consensus |
| MW-45 (RAISE) | 5/5 RAISE pilot; full PASS | 5 Opus calls; expect RAISE consensus |
| MW-47 (RAISE) | 5/5 RAISE pilot; full PASS | 5 Opus calls; expect RAISE consensus |
| MW-17-as-RAISE (Path A) | 5/5 RAISE pilot; full sub-axis-variable | 5 Opus calls; verify whether RAISE re-tag is empirically robust at Opus tier |

### Outcome interpretation

For each axis: Opus consensus aligns with Sonnet consensus → CONFIRMED training-data quality for that axis. Disagrees → flag for orchestrator (possibly indicates Sonnet+Opus disagreement on that axis; may need to re-label or drop axis).

### Cost / time

~$15-20 Opus (20 × ~$0.75-1); ~30 min wall clock.

### What you do NOT do

- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/
- Do NOT modify BATCH2
- Do NOT modify situations or Sonnet labels
- Do NOT scale Opus beyond 20 calls (5 per axis)
- Do NOT make the -E corpus integration decision (orchestrator-scope)

### Deliverable scope

1. `data/corpus_lever_c_opus_tierup_labels_2026-05-07.jsonl` (20 Opus labels)
2. `scripts/run_lever_c_opus_tierup.py`
3. `review/comms/BUILDER_REPORT_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md`

## QC stream — what you audit (when -D PR opens)

Standalone audit, ~10-15 min, 7-item Opus tier-up format:

1. Diff scope strict
2. Opus 4.7 model id correctness (`claude-opus-4-7`)
3. Same v3.4 prompt
4. 5 canonical hands per axis (= 20 hands matched from Sonnet-labelled corpus)
5. No solver-as-labels
6. Sonnet-Opus comparison correctness per axis
7. TC-X-DISPATCH-COMPLIANCE 16th formal exercise

## Sequencing

After -D: 12.5K-C-E corpus integration + 5-seed re-train (788 → 988 corpus) → 12.5L gate eval.

**Status: PR #285 + #287 cleared. LEAD-PROGRAMMER fires 12.5K-C-D Opus tier-up on this comm merge. ~$15-20; ~30 min.**
