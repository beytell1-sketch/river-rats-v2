---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.2 plan — value-BET counter-examples (Path C per directive-o)
status: PLAN — awaiting approval before building
related: MAIN_TERMINAL_DIRECTIVE_2026-04-18-o.md (6022bb5)
---

# Builder Plan — v2.3.2 Value-BET Counter-Examples

Plan before build per CLAUDE.md §1. Acknowledging the Path C
reasoning and the hard-rule memory overriding my Path A
recommendation — the counter-example-balance principle is the
right architectural call.

## Scope acknowledgement

- Mirror the Layer 2 generator. Flip hero-strength selector from
  AIR to VALUE.
- Generate ~40 value-BET counter-examples in the same
  `villain_checked_back=1 + checked-through + turn` shape as
  v2.3.1's air-CHECK rows. Both classes populated in the same
  feature subspace.
- Label with v3.1 (3-way set labelled; HU opportunistic per
  Decision-h Path B — consistent with v2.3.1 discipline).
- Retrain on v2.2 base + Section 1 + CALL + air-CHECK (40) +
  **value-BET (40 new)**. No sample_weight hacks.
- Full re-eval gates: standard + air litmus (protect Layer 2 fix)
  + value litmus (protect balance) + self-play (systemic).

## Generator design

**Location:** `review/generate_value_bet_v232.py` (mirrors
`review/generate_air_check_v231.py` commit `ad806ba`).

**Output:**
- `training-data/v23_2_value_bet_3way.jsonl` (labelling target)
- `training-data/v23_2_value_bet_hu.jsonl` (v2.4 prep, unlabelled)

**Predicate** (per directive-o):
```
facing_bet == 0
villain_checked_back == 1
num_opponents in {1, 2}
is_made_hand == 1                # flipped from air
equity_vs_range >= 0.55           # flipped from <0.35 air threshold
```

Note: directive-o's `draw_outs >= 0` is trivially always-true
(non-negative int). I read this as "don't filter on draws" — allow
both made-hand-with-draws and made-hand-no-draws. Will not add a
predicate check for draws.

**Hero selection:**
- `_is_value(hero, board)` accepts `evaluate_hand().category` in
  `VALUE_CATS`:
  ```
  VALUE_CATS = {
      # Monster
      'straight_flush', 'quads', 'full_house', 'flush', 'straight',
      'set', 'trips',
      # Strong made
      'two_pair', 'overpair',
      'top_pair_top_kicker', 'top_pair_good_kicker',
  }
  ```
- Iterate rank-order mid-first (same diversification heuristic as
  Layer 2's `_pick_air_hole_cards`) but accept hands matching
  `is_made=1 AND eq>=0.55` — predicate filter at build time drops
  weak-TP or medium-made that don't clear the equity bar.
- Reject flush-suit-dilution where hero holds 1+ suit but board
  has 3+ same-suit (→ hero has flush-draw vulnerability even with
  top pair — eq often falls below 0.55). Predicate will drop most
  of these anyway; the filter is cheap.

**Action history:** turn-shifted with flop check-through, identical
to v2.3.1's `_checked_through_history` — preserved bridge
semantics means `vcb=1` only on turn+.

**Board pool:** same as Layer 2 (`MONOTONE_BOARDS` +
`PAIRED_BOARDS` + `DRY_BOARDS` + `TWO_TONE_BOARDS`). Directive-o
emphasized breadth: "Don't narrow to only hostile textures —
value hands want broad texture coverage to anchor the boundary."

## Litmus seeds — value class

Two must-pass seeds, turn-shifted from directive-o flop form
(bridge vcb semantics as before):

1. **AA on 7h5d2c + turn 3c** (overpair dry board → BET)
   - Empirical probe: eq=0.703, is_made=1, vcb=1, cat=9 (overpair),
     hrp=0.93, bah=0.653
   - Turn 3c was chosen because: offsuit clubs, doesn't pair board,
     doesn't complete flush, no meaningful straight connection for
     villain range. Keeps hero's overpair status intact.

2. **KQ on KsTs3h + turn 2c** (TPGK two-tone → BET)
   - Empirical probe: eq=0.609, is_made=1, vcb=1, cat=7
     (top_pair_good_kicker), hrp=0.90, bah=0.551
   - Turn 2c was chosen because: clubs (not spades — avoids
     completing flush), low-rank (doesn't boost villain range),
     doesn't help hero's equity beyond flop state. Avoided Jd
     (eq drops to 0.487 — completes villain straights) and Ad (eq
     drops to 0.369 — gives villain Ax advantage).

**Hard-fail discipline** (symmetric with Layer 2's air litmus):
both value litmus seeds must pass predicate AND the eventual model
must predict BET at inference on the ORIGINAL flop positions
(mirror of Layer 2's "training has turn, inference tests flop").

## Expected yield

- OS target: ~50 candidates
- BP target: ≥ 30 passing predicate (30–40 clean rows per
  directive)
- Split: ~20 HU + ~20 3-way (matches v2.3.1 pattern; 3-way is the
  labelling target; HU held for v2.4)
- Predicate pass-through: higher than air-CHECK's 38% → 100%
  because made-hand + eq≥0.55 is a cleaner filter than air +
  eq<0.35 (fewer accidental classifications). Anticipate ≥60%
  predicate pass, 40+ clean.

## Labelling

- v3.1 prompt via `labelling_agent.py prepare` (now supports
  `--prompt` and `--batch-dir` from v2.3.1 additive changes)
- 4 batches × ~10 hands, parallel subagent dispatch
- Workspace: `review/label_batches_value_bet/`
- Collection: `training-data/v23_2_value_bet_3way_labelled.jsonl`

**Red-flag threshold** (directive-o): >3 of 40 labelled
CHECK/CALL/FOLD. Expected: ~35 BET + ~5 RAISE. If the red flag
trips → surface immediately (either the hands aren't as strong as
designed OR v3.1 has a BET-suppression drift I need to understand
before retraining).

## Training assembly

Script: `assemble_v23_2.py` (extends `assemble_v23_1.py` with
`load_value_bet_labels()`).

Sources:
```
v2.2 base                        385
Phase 4 labels (no UMBRELLA)     207
Pilot labels                      16
CALL supplement                   32
air-CHECK 3-way (v2.3.1)          40   ← unchanged, not re-labelled
value-BET 3-way (v2.3.2, NEW)    ~40
─────────────────────────────────────
Total                           ~720
```

All rows `label_source` tagged; CSV column schema same 55 raw +
55 attn = 110. `board_adjusted_hrp` already present on new rows
via the factory.

## Training

Script: `river-rats-core/train_v2_3_2.py` (per §5.1 — mirrors
`train_v2_3_1.py`, inherits hyperparameters):
- n_estimators=800, max_depth=5, lr=0.05
- No class weighting
- Same 80/20 stratified holdout, 5-fold CV
- Output: `river-rats-core/models/v2_3_2_model.json`
- Report + manifest in same directory

Manifest will include provenance link back to v2.3.1's manifest
(inherit audit trail).

## Evaluation gates — all four tiers

### Tier 1 — Standard (reference floors)
- FB-40 ≥ 72.5% (v2.2 floor)
- MW-50 ≥ 84.0% (v2.2 floor)
- Holdout + 5-fold CV — no degradation vs v2.3.1 baselines
  (v2.3.1: holdout 0.9118, CV 0.9439±0.0158)

### Tier 2 — Air-class litmus (protect Layer 2 fix)
- A4d/Qs5s7s flop → CHECK (the v2.3 → v2.3.1 win)
- T5h/JJ2 flop → CHECK (same)
- Broader-inference sweep: ≥ 85% CHECK (v2.3.1 had 94.7% — should
  stay high post-rebalance; mild decrease acceptable if value
  litmus/self-play pass)

### Tier 3 — Value-class litmus (protect Layer 2 balance; NEW)
- AA on 7h5d2c flop checked-to → BET
- KQ on KsTs3h flop checked-to → BET
- Value-in-checked-through sweep (15-hand analog of the air
  sweep): ≥ 85% BET. Will design this sweep in the build step —
  mirror of `eval_flop_generalization_sweep.py` with value hands.

### Tier 4 — Self-play (systemic balance; the gate that caught v2.3.1)
- Facing-bet 3-way+ count ≥ 888 (restored toward v2.3's 1269)
- Check-to-hero BET prob < 0.05 ≤ 5% (passive loop stays broken)
- Postflop CHECK share ≤ 25% (over-correction resolved)
- 2000 deals, same seed (42), use adapted
  `review/run_v231_selfplay_diagnostic.py` — will inline a
  `MODEL_PATH` override or fork to a v232 variant (keeping v2.3.1
  artifact for comparison).

**All four tiers must pass. Any STOP → report, don't paper over.**

## Open questions for reviewer

1. **HU/3-way balance in v2.3.2 output.**
   Directive-o specified "50/50 HU vs 3-way" for generation. My
   v2.3.1 yield was 40 3-way + 30 HU. For v2.3.2, I'll target
   ~20 HU + ~20 3-way for the generator but label only the 20
   3-way per Decision-h Path B (HU still opportunistic / unlabelled
   for v2.4). Confirming this matches intent.

2. **Tier 3 "value-in-checked-through sweep" sizing.**
   Layer 2's sweep was 20 cases. Mirror for value class is ~15
   per directive. OK to stay at 15, or expand to 20 for symmetry?

3. **`train_v2_3_1.py` vs a new `train_v2_3_2.py`.**
   Training logic is identical (just a different CSV path and
   output artifact). Two options:
   (a) New file `train_v2_3_2.py` that's a near-copy — preserves
       the v2.3.1 provenance artifact but adds another file with
       same hyperparams.
   (b) Parameterize the existing `train_v2_3_1.py` with `--version`
       flag — reduces drift, more elegant, but changes a committed
       artifact.
   
   Preferred (a) per CLAUDE.md §5.1 "training script's commit is
   provenance record" — keeping v2.3.1 script intact preserves the
   audit trail for the v2.3.1 model. Confirming.

## Timeline

- Plan approval: waiting
- Generator + 10-spec probe: ~30 min
- Full generation: ~5 min
- Labelling (4 parallel agents): ~15 min wall
- Assembly + train: ~5 min
- Standard eval: ~1 min
- Value sweep: ~2 min
- Self-play diagnostic: ~30-60 min (the slow gate)

**Total builder time: ~2-3 hours active, plus ~1 hour for agents
and self-play.** Within directive's 1-2 day window.

## What's NOT in this plan

- No sample_weight, class-weight, or pruning (ruled out by
  directive + memory)
- No hyperparameter tuning to compensate for anything
- No revert of Layer 1 board_adjusted_hrp (clean, not the
  culprit — v2.3.1 self-play confirmed the feature distribution
  healthy)
- No re-labelling of existing air-CHECK rows (labels are correct;
  just under-balanced — adding the balancing class fixes that)
- No touching `hand_evaluator.py` straight-draw bug (v2.3.2/v2.4
  ticket stands — independent scope)

Ready to build on your go-ahead. Three questions above to confirm.
