# Review: All-Player Multiway Decision Logging

**Date:** 6 April 2026
**Status:** REVIEW — yield gate check

---

## What Changed

### Removed: sticky callback (dead code)

`_make_sticky_callback()` removed from `self_play.py`. It was
correctly built but had zero effect — opponents never fold
postflop in multiway pots. The spec is preserved in
`review/SPEC_STICKY_OPPONENTS.md` if ever needed.

### Added: all-player multiway decision logging

When `log_all_multiway=True`, opponent seats also get a
`decision_log` passed to their oracle callbacks. Their multiway
postflop decisions (with full feat_dict from their perspective)
are captured in `GameResult.all_player_decisions`.

The GTO Expert labels situations based on board/ranges/position/pot,
not on what the oracle chose. Every player's perspective is equally
valid training data.

### Changes to `generate_3way_situations.py`

- Extracts 3-way decisions from both `hero_decisions` and
  `all_player_decisions`
- Deduplicates by situation_id
- Removed sticky/equity-floor CLI flags
- Default deals changed from 5400 to 3000

## Files Changed

| File | Change |
|------|--------|
| `self_play.py` | Removed `_make_sticky_callback()`, removed `sticky_opponents`/`equity_floor` params, added `log_all_multiway` param + `all_player_decisions` field on GameResult |
| `generate_3way_situations.py` | Rewritten to extract from all players, removed sticky flags |

## Test Results

864 passed, 7 failed (all pre-existing from range data change),
45 skipped. Zero new failures.

## Yield Results

| Metric | Hero-only (before) | All-player (after) |
|--------|-------------------|-------------------|
| Deals | 500 | 500 |
| Games | 3,000 | 3,000 |
| 3-way decisions | 36 | 216 |
| **Yield** | **1.20%** | **7.20%** |
| **Multiplier** | — | **6x** |

### Distribution (all-player)

| Dimension | Breakdown |
|-----------|-----------|
| Street | flop 72, turn 72, river 72 (even) |
| Position | OOP 144, IP 72 |
| Facing bet | 6 facing, 210 not facing |
| Oracle action | CHECK 204, RAISE 6, FOLD 6 |

### Primary Gate: yield >= 3%

**PASSED.** 7.20% yield means ~3,000 deals produces ~1,300
situations. More than enough to select 200 stratified examples
for labelling.

### Secondary Gate: action distribution

3% non-CHECK (6 RAISE + 6 FOLD out of 216). Still CHECK-heavy,
but with ~1,300 situations from 3,000 deals, we'll have ~40
non-CHECK situations to include in stratified selection. And per
earlier review guidance: CHECK-heavy first iteration is acceptable.

## Volume Estimate

At 7.20% yield:
- 3,000 deals = 18,000 games = ~1,300 3-way situations
- Select best ~200 stratified for GTO Expert labelling
- Runtime: ~6 minutes for 3,000 deals

## Card Dealer Verification

The deal generator (`deal_generator.py`) uses Python's
`random.Random(seed)` — Mersenne Twister with Fisher-Yates
shuffle. Standard for poker simulations. Not cryptographically
secure (not needed — this is offline training data, not real
money). Uniform distribution, no bias.

## Next Steps (pending approval)

1. Run full 3,000-deal generation
2. Stratify selection: balance by street, position, facing_bet
3. Send ~200 situations to GTO Expert labelling pipeline
4. Export CSV, train v9-3way, gate check
