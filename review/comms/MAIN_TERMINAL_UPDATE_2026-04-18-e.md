---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: AMEND prior directive — targeted cleanup, not full re-label
status: DIRECTIVE — supersedes the re-label scope in update-d §3
---

# Amended Fix: Targeted Label Cleanup

Owner correctly flagged: we don't need to re-label all 215
hands. The oracle has no hard rules — it learned from the
labels. Find the contaminated labels and clean just those.

## Step 1 — Query the labelled data (30 min)

From `training-data/v23_pilot_labelled.jsonl` and the
Phase 4 labels: extract every hand where
`override_clause_fired = true`.

For each, report:
- situation_id
- consensus_action (should be BET if override fired)
- is_made_hand
- has_flush_draw / has_straight_draw / draw_outs
- equity_vs_range
- worse_hand_pct
- hand_bucket
- hero_range_percentile
- is_monotone / danger_score
- Pass 1 vote split (4/4? 3/1? 2/2?)

Deliverable:
`review/comms/OVERRIDE_AUDIT_2026-04-18.md`

## Step 2 — Classify each override-fired hand

Three buckets:

**CLEAN** — override fired but the poker case for BET is
strong independently:
- is_made_hand=1 OR has_flush_draw=1 OR draw_outs >= 4
- equity_vs_range >= 0.40
- worse_hand_pct >= 0.55
- Panel would have said BET without the override

These labels stay. The override didn't change the outcome.

**SUSPECT** — override fired but BET case is weak:
- is_made_hand=0 AND draw_outs < 4
- equity_vs_range < 0.35 OR worse_hand_pct < 0.50
- OR is_monotone=1 with hero holding wrong suit
- OR hand_bucket = air

These labels need re-examination. The override may have
pushed a natural CHECK to BET.

**BORDERLINE** — override fired, features are in between:
- Everything not clearly CLEAN or SUSPECT

Flag these for manual review but don't auto-reclassify.

## Step 3 — Re-label only SUSPECT hands

Create v3.1 prompt per update-d §1 (strip override).
Re-label ONLY the SUSPECT hands with v3.1 (panels reason
on poker merits). This might be 20-40 hands, not 215.

If a SUSPECT hand flips from BET to CHECK under v3.1:
the override was the only reason it was BET. Keep the
CHECK label — it's honest.

If a SUSPECT hand stays BET under v3.1: the override
wasn't needed for this hand. Keep BET.

## Step 4 — Retrain on cleaned data

Replace the SUSPECT labels in the training CSV with the
v3.1-relabelled versions. Keep everything else unchanged.
Retrain. Evaluate.

## Why this is better than full re-label

- ~20-40 hands re-labelled vs ~215
- CLEAN labels preserved (genuine poker reasoning, override
  was redundant on these)
- Only the contaminated labels get fixed
- Faster (~2-3 hours total vs ~half a day)
- Less risk of introducing new noise from re-labelling
  hands that were correctly labelled the first time

## What still holds from update-d

- Game builder reverts to v2.2 for playtest (already
  directed)
- v3.1 prompt creation (strip override clause)
- The lesson: no override clauses in future prompts

## What's superseded from update-d

- Full re-label of all Section 1 hands (§3) — replaced
  by targeted cleanup of SUSPECT hands only
- Phase 3.5 pilot on v3.1 — not needed for a targeted
  re-label of ~20-40 hands
- Calibration gate on v3.1 — still run, but as validation
  not as a gate (v3.1 is simpler than v3, lower risk)
