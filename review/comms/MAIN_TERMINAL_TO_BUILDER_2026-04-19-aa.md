---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.4 Stage 1 APPROVED — proceed to Stage 2 (KB §1.9 update)
status: DIRECTIVE — Stage 1 complete, Stage 2 GO
---

# v2.4 Stage 1 → APPROVED. Stage 2 GO.

## Stage 1 assessment

Clean execution across all Stage 1 criteria:

- 4 features implemented with 17/17 unit tests passing
- v2.3.1 anchor gate regression: 5/5 PASS — **backward compat
  preserved**. The feature-vector expansion didn't break
  existing models that use the 55-col schema (FEATURE_COLUMNS
  correctly held back until Stage 5 training, per discipline)
- Backfill audit: 579 rows, 0 sanity violations, healthy signal
  density (nut_flush_block 11.2% firing; defensive bucket 6.22%
  well above the 2% target)
- No scope creep — KB / prompt / training correctly deferred
  to Stages 2-5 per sequence

This is the execution pattern v2.4 needs. STOP-and-report
discipline held; stages stay isolated; audit produces evidence.

## I1 wording correction — good catch

Your flag on the I1 predicate (`flush_draw_rank==0` vs
`has_flush_draw==0`) is exactly right. The literal
`flush_draw_rank==0` predicate is empty-by-construction because
that field is only 0 when there's no flush possibility at all,
which contradicts `nut_flush_block=1` requiring flush
possibility.

You interpreted **reviewer intent over literal**, corrected to
the meaningful predicate, and flagged the discrepancy. That's
the discipline this project needs — don't execute a contradiction
silently. Log it in the spec doc's revision trail if not already
there.

## Stage 2 — KB §1.9 update

Per directive-z stage sequence:

### 2.1 — Identify KB §1.9 location

Find the labelling knowledge base in the v2 repo (likely
under `prompts/` or `knowledge/` — scan for v3.1 prompt's KB
reference to locate the section structure).

### 2.2 — Draft KB §1.9 additions

For each of the 4 new features, write knowledge-base language
covering:

- **Poker-theoretic meaning**: what the feature measures in
  poker terms (not math terms)
- **When it matters**: which decision contexts the feature
  should influence (e.g., facing-bet-on-flush-possible-board
  with weak-made for `flush_draw_block_pct`)
- **Directional interpretation**: when high values push action
  toward BET vs CHECK vs CALL. Remember: blockers cut both ways
  depending on hero's action context (owner's 2-flag insight).
  KB should describe this explicitly so labeller panels reason
  correctly per-hand rather than blindly counting combos.
- **Example cases**: one or two hand examples per feature where
  it should materially shift the panel's reasoning

Keep the language aligned with v3.1 prompt's existing knowledge
base tone — this is an additive, not a rewrite.

### 2.3 — GTO reviewer pass

Spawn GTO reviewer subagent on the KB §1.9 draft. Reviewer
checks:

- Does the poker-theoretic language describe what the feature
  actually measures?
- Are the "when it matters" criteria poker-sound?
- Directional interpretation matches the owner-flagged
  bluff-catch vs bluff-bet asymmetry?
- Are the example cases clean and illustrative?

Expected outcome: APPROVED or APPROVED_WITH_MODIFICATIONS. If
NEEDS_REWORK, revise and re-review (same discipline as Stage 1
plans).

### 2.4 — Commit + report

Commit KB diff + GTO review. Report back with:
- Line-level diff of what was added to KB §1.9
- GTO reviewer verdict
- Sanity check: does the KB language describe the same features
  your Stage 1 code implements? (Alignment audit)

## Stage 2 gate for Stage 3

Stage 3 (v3.2 prompt derivation) depends on:
- Stage 2 KB §1.9 language final + GTO-approved
- Clear naming of the 4 new features as they'll appear to
  labeller panels

Don't start Stage 3 until Stage 2 is landed + approved.

## Discipline reminders

- No training. Stage 5 work only.
- No feature changes. Stage 1 spec locked.
- No panel test runs. Stage 4 work only.
- KB is PROSE + EXAMPLES only. No code.

## Reporting cadence

Ping when KB diff drafted (before GTO review) if you want a
sanity check on tone/scope before reviewer burn. Ping when GTO
verdict lands. Ping when committed.

## Manifest update

I'll bump the manifest to reflect Stage 1 complete, Stage 2
underway. You don't need to touch the manifest — orchestrator
owns it.

Go.
