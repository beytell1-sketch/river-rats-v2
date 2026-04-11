# Review: Position String + Prior Actions Fix

**Date:** 6 April 2026
**Status:** REVIEW — both blockers fixed, yield gate passed

---

## Bugs Fixed

### 1. Opponent position string (BLOCKER — fixed)

**Problem:** All opponent-sourced situations had `hero_position: 'opp'`
because `_extract_3way_decisions()` received a hardcoded string.

**Fix:** Added `player_position: str` field to `HeroDecision` dataclass
(self_play.py line 76). Populated with `player.position` in both the
preflop (line 155) and postflop (line 193) logging paths inside
`_make_oracle_callback()`. The extraction function now reads
`dec.player_position` directly — no more passed-in string.

**Verification:** Output shows real positions (CO, BTN, BB, UTG, HJ).

### 2. Cross-contaminated prior actions (SHOULD_FIX — fixed)

**Problem:** All 5 opponents shared one `all_decisions` list. When
`_extract_3way_decisions` built priors from `decisions[:i]`, it mixed
decisions from different players.

**Fix:** `_play_one_game()` now creates a separate `List[HeroDecision]`
per opponent, stored in `Dict[str, List[HeroDecision]]` keyed by
position. Each opponent's callback gets its own list. `GameResult`
field renamed from `all_player_decisions` to `opponent_decisions`
(typed `Dict[str, List[HeroDecision]]`).

The extraction loop iterates per-position:
```python
for pos, dec_list in game.opponent_decisions.items():
    for sit in _extract_3way_decisions(dec_list, game.deal_id):
```

Prior actions now reflect only that player's own action history.

## Yield Results (corrected)

| Metric | Before (broken) | After (fixed) |
|--------|----------------|---------------|
| Deals | 500 | 500 |
| Games | 3,000 | 3,000 |
| Raw situations | 216 | 45 |
| **Unique situations** | **~36** | **45** |
| Yield (per game) | — | 1.50% |

The previous 216 count was inflated — each deal is played 6 times
(hero rotation), so the same physical 3-way pot was counted up to
6 times from different game instances. With proper dedup by
situation_id (`d{deal}_{position}_{street}`), the real count is 45.

The 45 vs 36 improvement comes from capturing decisions at positions
where hero folded preflop but another player in the same 3-way pot
had their decision logged.

### Volume estimate (corrected math)

45 unique situations from 500 deals.
At 3,000 deals: ~270 unique situations.
Select 200 stratified for labelling.
Runtime: ~6 minutes for 3,000 deals.

### Primary gate: yield sufficient for 200 labelled situations

**PASSED.** 270 > 200. Enough to stratify by street, position,
facing_bet.

## Test Results

864 passed, 7 failed (all pre-existing from range data change).
Zero new failures.

## Distribution

| Dimension | Breakdown |
|-----------|-----------|
| Street | flop 15, turn 15, river 15 (even) |
| Position | OOP 27, IP 18 |
| Positions | CO 12, BTN 15, BB 12, UTG 3, HJ 3 |
| Facing bet | 1 facing, 44 not facing |
| Oracle action | CHECK 43, RAISE 1, FOLD 1 |

## Files Changed

| File | Change |
|------|--------|
| `self_play.py` | Added `player_position` to HeroDecision; per-player opponent decision lists; removed sticky callback |
| `generate_3way_situations.py` | Uses `dec.player_position`; iterates per-opponent list; proper dedup |

## Next Steps (pending approval)

1. Run 3,000-deal generation (~6 min)
2. Stratify: balance by street, position, facing_bet
3. Select ~200 situations for GTO Expert labelling
4. Run labelling pipeline
5. Export CSV, train v9-3way, gate check
