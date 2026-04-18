---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Review of air-CHECK labels — APPROVED, proceed to retrain
status: DIRECTIVE — go on retrain; vocab gap forwarded to teaching
---

# Review — Air-CHECK Labels

## Verdict

**APPROVED.** Proceed: 110-feature re-extract → assemble →
retrain → evaluate.

## Results summary

- 40/40 CHECK · 0 BET · 0 CALL · 0 RAISE · 0 FOLD
- Unanimous HIGH confidence across 4 panels
- Both litmus seeds: CHECK HIGH diff=1
- 36 clear / 4 standard / 0 boundary
- BET red-flag threshold (>5): NOT tripped (0 BET)

## Why 100% CHECK is good, not suspicious

The hard-rule override check asks: "Does it apply uniformly
across a shape without per-hand reasoning?" This looks superficially
like a yes — all 40 uniform CHECK. But the test is whether the
labels came from per-hand reasoning or from an imposed rule.

**Evidence they came from reasoning:**
- 4 agents reasoned independently, no splits
- 4 hands flagged as standard-difficulty had BET explicitly
  evaluated via 3-way fold-equity math (KB §1.1 + DO NOT Rule 2)
  and rejected — that's per-hand analysis, not rule application
- No override clause in v3.1 prompt

**Why uniform CHECK is the correct answer here:**
The predicate (`air + vcb=1 + checked-through + eq<0.35`) *is*
the definition of a shape where CHECK is correct on poker merits.
We deliberately filtered to this shape to produce the missing
counter-examples. Unanimous CHECK validates the predicate is
well-defined — not that a rule was imposed.

**Balanced learning doesn't come from this set alone.** It
comes from the combined training data: v2.2 base + Section 1 +
CALL supp has plenty of BET examples in the "hero has value"
shapes. The air-CHECK 40 adds CHECK examples in the "hero has
air" shape. Model learns the boundary from the combined set.

This is the right distribution for Layer 2's job.

## Vocab gap — forwarded to teaching terminal

Panel 01 proposed `check_give_up` tag: "check air intending to
realize equity cheaply on river." Used `check_pot_control` as
closest approved vocab fit.

The concept is real and distinct:
- `pot_control` = "I have something to protect; keep pot small"
- Proposed `give_up` / "cheap showdown" = "I have nothing; see
  river cheaply to realize whatever equity remains"

Semantic gap is genuine. **Not a v2.3.1 blocker** (builder used
closest approved vocab, Oracle's Read is unaffected). Forwarding
to teaching terminal for vocab-registry review during their
Phase 3 L2/L1 work or sooner if Layer 3 guard surfaces the same
gap.

## Retrain checklist — proceed

1. Re-extract ALL training data with 110-feature vector (Layer 1
   `board_adjusted_hrp` included)
2. Assemble: v2.2 base + Section 1 + CALL supp + air-CHECK 3way (40)
3. Train → `v2_3_1_model.json`
4. Save training manifest (per §5.1 provenance requirement):
   - Base data sources + row counts
   - Feature vector spec (110-col)
   - Training script commit SHA
   - Hyperparameters
   - Output artifact path

## Evaluation gates — v2.3.1 ships when ALL pass

**Standard gates:**
- HU / 3-way reference accuracy: no regression vs v2.2
  (72.5% / 84.0% floor)
- Holdout set: no regression
- Class distribution sanity: no new bias modes

**Litmus gates (both REQUIRED):**
- A4d/Qs5s7s (FLOP decision, not turn) → predict CHECK
- T5h/JJ2 (FLOP decision) → predict CHECK

**These test inference on the ORIGINAL flop playtest spots.**
Training set has turn versions; litmus tests flop versions.
If either flop inference fails:
- Layer 1 board_adjusted_hrp alone wasn't enough
- Revisit: add flop memorization specs (Path A from Decision-h)
  as v2.3.2 pass
- Do NOT paper over with an override

If both flop litmuses pass on v2.3.1, ship.

## Parallel status

- Teaching Layer 3 (value_extract air guard) — separate terminal,
  tracked independently
- Game — on v2.2 until v2.3.1 ships

Go.
