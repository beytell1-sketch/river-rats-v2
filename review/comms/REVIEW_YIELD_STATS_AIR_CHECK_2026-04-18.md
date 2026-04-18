---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Review of BUILDER_YIELD_STATS_AIR_CHECK — APPROVED, proceed to labelling
status: DIRECTIVE — go on 3-way labelling
---

# Review — Air-CHECK Yield Stats

## Verdict

**APPROVED.** Proceed to labelling dispatch on the 3-way set.

## What's right

- 100% predicate pass-through on both streams (40/40, 30/30)
- Both litmus seeds present, pass predicate, feature values
  confirm air state (eq=0.036 / 0.068; board_adjusted_hrp=0.035
  / 0.010)
- Schema preflight clean (ANOMALY-A guard intact)
- Hard-fail litmus runs before main loop — good discipline
- 10-spec probe caught 3 bug classes before full-run burn —
  exactly the "validate assumptions first" pattern from
  CLAUDE.md §2
- Honest surface of the Kc turn-card deviation from my
  guidance: wheel gutshot on low turns was a real constraint
  I missed. Your empirical probe found the right card. Fine.

## Texture concentration — accepted with monitoring flag

You flagged it; I'm accepting the reasoning:

- The predicate (`eq<0.35 AND outs<=2 AND is_made=0`) *is* the
  hostile-texture selector. Dry-board air retains >35% equity
  against checked-through villain ranges, so it doesn't belong
  in the "hero has nothing on a dangerous board" class.
- The playtest findings (A4d monotone, T5h paired) live in
  exactly this concentration. Targeting here is correct.
- Layer 1 `board_adjusted_hrp` carries the broader "hero is
  weak" signal across all textures. Combined fix generalises;
  Layer 2 inoculates the specific pattern.

**Monitoring note for post-retrain eval:** if the retrained
model generalises poorly to dry-board weak-showdown spots
(separate class from air), we add dry-board counter-examples
in a v2.3.2 pass. Not a v2.3.1 blocker.

## Board diversity — 7 unique 3-way boards

40 rows across 7 boards = ~5-6 rows per board on average. You
verified all 40 rows are unique 4-tuples (hero × board × pos ×
street). That's the correct integrity check — the model sees
varied (hero, archetype) combinations on each board, not duplicate
situations.

The multi-pass + rotated-archetype generator design is sound.
Accept as-is.

## Labelling dispatch — GO

Proceed with:
- `labelling_agent.py prepare` on `v23_air_check_3way.jsonl`
- v3.1 prompt (calibrated on 3-way exam — fit for purpose)
- Panels reason on poker merits per hand (no override clause)
- HU set stays unlabelled for v2.4

Expected panel behaviour per update-g Layer 2:
> "Label with v3.1 prompt (no override). Panels should produce
> CHECK on poker merits — these are genuinely CHECK-correct
> spots."

If panels label >5 of the 40 as BET, that's a red flag worth
surfacing — either the hands aren't as air as we think, or the
panels are drifting. Report label distribution when done.

## Post-labelling checkpoint

After labels land, BEFORE retraining, I want to see:
1. Label distribution (BET / CHECK / CALL / RAISE / FOLD counts)
2. Any panel disagreement / vote splits on individual hands
3. Confirmation that both litmus seeds labelled CHECK (they
   must, on poker merits)

Then proceed per Decision-h checklist:
- Re-extract all training data with 110-feature vector
- Assemble: v2.2 base + Section 1 + CALL supp + air-CHECK 3way
- Retrain → `v2_3_1_model.json`
- Evaluate: standard gates + BOTH **flop** litmus tests must
  predict CHECK at inference

## Parallel reminder

Teaching terminal has Layer 3 (value_extract air guard) open
in parallel. Not your dependency; flagging for orchestration
awareness. Both must land before v2.3.1 ships.

Go.
