---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Review of v2.3.1 train+eval — CONDITIONAL APPROVAL, one check before ship
status: DIRECTIVE — one additional validation step, then ship on teaching Layer 3 land
---

# Review — v2.3.1 Training + Evaluation

## Verdict

**CONDITIONAL APPROVAL.** Gates pass cleanly. Owner preference
is slow and quality-focused — before ship I want one additional
validation to confirm generalization (not narrow memorization),
plus three clarifications.

## What's strong

- **The money shot is real.** v2.3 → v2.3.1 on A4d/Qs5s7s flop:
  BET 98.6% → CHECK 93.5%. On T5h/JJ2 flop: BET 72% → CHECK 98.3%.
  Training had turn versions only; inference tested flop. The
  model generalized across `street` — Layer 1 + Layer 2 together
  produced the cross-street inoculation we hypothesized.
- Standard gates clear: FB-40 77.5% (+5.0 over floor), MW-50
  84.0% (at floor).
- Holdout 91.2%, CV 94.4%±1.6% — healthy, ~3pt train/holdout
  gap normal for 677 rows.
- Provenance manifest saved per §5.1.
- No override used. Clean honest data path.

## Additional validation required before ship

**Broader air-on-hostile-flop inference sweep.** 2 litmus cases
confirm the exact playtest spots fixed. What they don't confirm:
whether the fix *generalizes* to the broader class of "hero has
air on hostile checked-through flops," or whether it narrowly
memorized the Layer 2 pattern.

### What to run

Generate 15–20 flop inference cases — NOT in training set, NOT
the litmuses — varying across:

- Hero cards: mix of weak-ace (A4/A5/A7), low/mid broadway (T5,
  J4), baby disconnected (63, 42), suited-disconnected
- Flop textures: monotone (different suits than training seeds),
  paired (different pair ranks), rainbow-connected, two-tone-
  connected
- Positions: BTN vs blinds, CO vs BTN, MP vs blinds
- Villain counts: mix of HU and 3-way (HU is extra-informative
  since no HU examples in training)

### Predicate for candidates

Must match air-CHECK shape at inference:
- `facing_bet=0` (checked to hero)
- `is_made_hand=0`
- `draw_outs <= 2`
- `equity_vs_range < 0.35`

### What I want to see

- Expected pass rate: ≥ 85% CHECK across the sweep (14/16 or
  17/20). Small miss rate acceptable — unknown-unknowns exist.
- Report per-case: hero, board, street, action predicted, confidence
- Flag any BET predictions with feature dump so we see what
  pattern triggered

### Why this gate

If the sweep passes ≥ 85%: generalization confirmed, v2.3.1
ships on teaching Layer 3 land.

If the sweep fails (say <70% CHECK): Layer 2 memorized the narrow
pattern, doesn't generalize. v2.3.2 pass needed — broader
counter-example set across textures/positions. Not a disaster,
just more work, and better to catch now than after playtest.

## Clarifications needed

1. **RAISE recall 0.60 — was v2.2 the same?** You said "not a
   regression" — confirm with v2.2's RAISE recall number so
   we have the delta documented.

2. **Per-class holdout F1 / precision / recall for BET, CHECK,
   CALL, RAISE, FOLD.** "Strong" isn't specific. Want the
   numbers in the manifest or a separate metrics file.

3. **MW-50 tied at floor.** Exactly 84.0% is fine, but tied-at-
   floor means the three-layer fix didn't help the 3-way gate.
   Expected or surprising? Any intuition on why it didn't move?

Numbers in a short followup is fine — not asking for another
full doc.

## Ship sequence

Once the broader-inference sweep passes AND teaching Layer 3
lands:

1. Confirm both litmuses still hold (sanity recheck)
2. Copy `v2_3_1_model.json` + manifest to `river-rats-core/models/`
3. Notify game builder — adapter swap v2.2 → v2.3.1
4. Run self-play diagnostic (per `project_self_play_retest_v23.md`)
5. Tag release

## Not blocking ship

- Vocab gap (check_give_up) — forwarded to teaching
- Self-play diagnostic — scheduled post-ship per restart plan
- 28 solver-enqueued hands from Phase 4 — owner-paced
- HU counter-examples (`v23_air_check_hu.jsonl`) — v2.4 scope

## Why this additional gate

Two litmus cases fixing two playtest findings is great but
narrow. Owner style: catch problems now over shipping and
fixing later. A 15-hand sweep is a few minutes of your time
and a few seconds of inference — cheap insurance that the
three-layer fix is architectural, not patch-memorization.

If the sweep comes back 20/20 CHECK, I'll celebrate too.
Until then, one more check.

Go when ready.
