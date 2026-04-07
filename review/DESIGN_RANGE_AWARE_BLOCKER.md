# Design: Range-Aware Flush Blocker Feature

**Status:** Proposed — awaiting owner review before implementation  
**Date:** 2026-04-06  
**Author:** Architecture Expert

---

## 1. Problem Statement

The current feature pipeline has no flush blocker feature at all. This design proposes
`flush_block_pct`: the fraction of villain's flush combos that hero's hand blocks, computed
from villain's actual range rather than a generic probability.

---

## 2. Data Flow: What Is Available Where

All three required inputs are already computed earlier in the pipeline before `extract_range_composition` is called.

### 2a. Board — flush_suit and suit_counts

`analyze_board()` in `board_analyzer.py` returns a `BoardAnalysis` dataclass. The relevant fields:

- `flush_suit: Optional[str]` — the suit with 3+ cards on board, or `None`
- `suit_counts: Dict[str, int]` — count per suit (e.g. `{'s': 3, 'h': 1, 'd': 1}`)
- `max_suit_count: int` — highest suit count on board
- `is_monotone`, `is_two_tone` — suit texture flags

Board analysis is already computed in Step 2 of `extract_features_step1_through_5`. The
board analysis result is stored as `_board_analysis` in the feature dict (or equivalent).
**Key constraint:** `flush_suit` is only set when `max_suit_count >= 3`. Below 3 there is
no flush draw threat and the feature should return 0.0.

### 2b. Hero's Hand

Hero's two cards are parsed in `parse_hero_hand()` and stored as `_hero_cards: List[str]`
in the feature dict, e.g. `['As', 'Kd']`. Each card string is `<rank><suit>`.

The suit character is `hero_cards[i][1]` for each card `i`. This is already the format
used by `count_combos_with_blockers`, which expects blockers as `{(rank, suit), ...}`.

### 2c. Villain's Range

`get_villain_range(hero_pos, villain_pos, opener_pos)` is already called inside
`extract_range_composition`. It returns `Dict[str, float]` — hand notation to frequency.
This is the same range dict used for `villain_top_pair_plus_pct`.

`extract_range_composition` already has access to all three inputs. The new computation
slots in as an additional pass over `v_range`, alongside the existing classify_hand loop.

---

## 3. Exact Computation Steps

```
Input:
  v_range: Dict[str, float]        # villain's range (already fetched)
  hero_cards: List[str]            # ['As', 'Kd']
  flush_suit: Optional[str]        # 's', 'h', 'd', or 'c' — or None
  board_cards: List[str]           # to construct dead-card blockers

Step 1: Guard clause
  if flush_suit is None or max_suit_count < 3:
      return flush_block_pct = 0.0

Step 2: Build hero blocker set (same format as count_combos_with_blockers)
  hero_suit_set = {card[1] for card in hero_cards}
  hero_holds_flush_suit = flush_suit in hero_suit_set
  if not hero_holds_flush_suit:
      return flush_block_pct = 0.0  # fast exit, nothing to block

Step 3: Build full dead-card set for combo counting
  dead_cards = set of (rank, suit) for all hero_cards + board_cards
  (board cards are already dead from villain's perspective)

Step 4: For each hand in villain's range, determine flush combos

  A hand contributes to villain's flush draws / made flushes when it contains
  at least one card of flush_suit. For notation-level filtering:

  - Suited hands (e.g. 'AKs'): contributes only the one combo where
    both cards share flush_suit. 0 or 1 combos of flush_suit per suited hand.
  - Pair hands (e.g. 'AA'): contributes 1 combo per pair of flush_suit cards
    (C(flush_suit_available, 2) — usually 1 combo if flush_suit appears once).
  - Offsuit hands (e.g. 'AKo'): contributes combos where at least one card
    is flush_suit — i.e., offsuit combos involving the flush_suit.

  The implementation works at combo level, not notation level:

  For each (hand_notation, freq) in v_range where freq > 0:
    total_flush_combos_in_range += flush_combos_in_hand(hand_notation, flush_suit, dead_cards) * freq
    blocked_flush_combos += blocked_flush_combos_in_hand(hand_notation, flush_suit, dead_cards, hero_flush_cards) * freq

Step 5: Compute ratio
  if total_flush_combos_in_range == 0:
      flush_block_pct = 0.0
  else:
      flush_block_pct = blocked_flush_combos / total_flush_combos_in_range
```

### Sub-step: flush_combos_in_hand (notation level)

This is the critical helper that does not yet exist. It enumerates combos of a hand that
include at least one card of `flush_suit`, accounting for dead cards.

```python
SUITS = ['c', 'd', 'h', 's']

def flush_combos_in_hand(notation: str, flush_suit: str, dead: set) -> Tuple[int, int]:
    """
    Returns (total_flush_combos, hero_blocked_flush_combos).
    
    total_flush_combos: combos of this hand containing >= 1 card of flush_suit,
                        after removing dead cards (board + hero cards).
    hero_blocked_flush_combos: subset of total_flush_combos that include a
                               specific card hero holds (hero's flush_suit card).
    
    hero_flush_card: the (rank, suit) of hero's card that is flush_suit, or None.
    """
    h = normalize_hand(notation)
    r1, r2 = h[0].upper(), h[1].upper()
    is_pair = (r1 == r2)
    is_suited = h.endswith('s') and not is_pair

    total = 0
    blocked = 0

    if is_pair:
        # Pair: combos are (r1_suit_a, r1_suit_b) pairs
        available = [(r1, s) for s in SUITS if (r1, s) not in dead]
        for i, c1 in enumerate(available):
            for c2 in available[i+1:]:
                if c1[1] == flush_suit or c2[1] == flush_suit:
                    total += 1
                    if c1 == hero_flush_card or c2 == hero_flush_card:
                        blocked += 1

    elif is_suited:
        # Suited: exactly one combo per suit (both cards same suit)
        s = flush_suit  # only the flush_suit combo matters
        c1 = (r1, s)
        c2 = (r2, s)
        if c1 not in dead and c2 not in dead:
            total += 1
            if c1 == hero_flush_card or c2 == hero_flush_card:
                blocked += 1

    else:
        # Offsuit: combos (r1_suit_a, r2_suit_b) where suits differ
        r1_avail = [(r1, s) for s in SUITS if (r1, s) not in dead]
        r2_avail = [(r2, s) for s in SUITS if (r2, s) not in dead]
        for c1 in r1_avail:
            for c2 in r2_avail:
                if c1[1] == c2[1]:
                    continue  # same suit = invalid offsuit combo
                if c1[1] == flush_suit or c2[1] == flush_suit:
                    total += 1
                    if c1 == hero_flush_card or c2 == hero_flush_card:
                        blocked += 1

    return total, blocked
```

Note: `hero_flush_card` is the specific `(rank, suit)` tuple for hero's card that matches
`flush_suit`. If hero holds two cards of `flush_suit` (rare but possible if board has 3 of
a suit and hero has 2 more of the same), both count. The blocked count increments if either
hero card appears in the villain combo.

---

## 4. Performance Estimate

The existing `extract_range_composition` already iterates every hand in `v_range` once
(the `classify_hand` loop). The flush blocker pass is a second loop over the same dict.

Range sizes by position (approximate combo counts before weighting):
- CO RFI: ~50-65 hand notations in the dict
- BTN RFI: ~90-110 hand notations
- Average across all positions: ~70 notations

For each notation, the flush combo enumeration is:
- Suited hand: O(1) — one suit check, at most 1 combo
- Pair: O(C(4,2)) = 6 iterations max
- Offsuit: O(4x4) = 16 iterations max, filtered by suit

Worst case per call: 110 hands x 16 iterations = 1,760 simple tuple comparisons.

This is negligibly fast. The equity Monte Carlo is the bottleneck by several orders of
magnitude (it runs thousands of board runouts). The flush blocker pass adds no meaningful
latency.

No caching is needed. The range dict is already instantiated in `get_villain_range`;
the blocker pass runs directly over it.

---

## 5. Relationship to the Simple Binary

There is currently no flush blocker feature of any kind in the 45-feature pipeline.
This feature would be new, not a replacement.

If a simple binary were added first, it would answer: "does hero hold any card of the
flush suit?" That is a coarse signal — it treats `As` on a 3-spade board the same as `2s`,
ignoring that `As` blocks far more of villain's flush range than `2s` does.

`flush_block_pct` is strictly more informative and is only marginally more expensive to
compute. The recommendation is to implement `flush_block_pct` directly without an
intermediate binary, since both are new and `flush_block_pct` subsumes the binary (a value
near 0.0 = no blocking, near 1.0 = heavy blocking).

The binary can be derived trivially from `flush_block_pct > 0.0` downstream if ever needed
for teaching output.

---

## 6. Integration Point in feature_extractor.py

The new computation belongs inside `extract_range_composition`. It has direct access to
`v_range`, `hero_cards`, and `board_cards` at that call site. The board analysis
(`flush_suit`, `max_suit_count`) must be passed in as parameters, matching how
`extract_range_composition` already receives `board_cards`.

### Signature change

Current:
```python
def extract_range_composition(
    board_cards: List[str],
    hero_pos: str,
    villain_pos: str,
    facing_bet: bool,
    street_raw: str,
    is_3bet_pot: int,
    opener_pos: str = None,
) -> Dict:
```

Proposed addition (two new parameters):
```python
def extract_range_composition(
    board_cards: List[str],
    hero_pos: str,
    villain_pos: str,
    facing_bet: bool,
    street_raw: str,
    is_3bet_pot: int,
    opener_pos: str = None,
    hero_cards: List[str] = None,       # NEW
    flush_suit: Optional[str] = None,   # NEW
) -> Dict:
```

Caller in `extract_all_features` already has both pieces available via
`features.get('_hero_cards', [])` and the board analysis result.

### Return dict addition

The function already returns a dict of `_`-prefixed fields. Add:
```python
'_flush_block_pct': flush_block_pct,  # float [0.0, 1.0]
```

### Feature promotion (Step 10)

Following the same pattern as `villain_top_pair_plus_pct`:
```python
features['flush_block_pct'] = features.get('_flush_block_pct', 0.0)
```

This also requires adding `'flush_block_pct'` to `FEATURE_KEYS` in `feature_keys.py`.

---

## 7. Edge Cases

| Case | Handling |
|---|---|
| No flush draw on board (`max_suit_count < 3`) | Return 0.0 immediately |
| Hero holds no card of `flush_suit` | Return 0.0 after suit check |
| Villain range empty or all-zero frequency | Return 0.0 (divide-by-zero guard) |
| Hero holds two cards of `flush_suit` | Both hero cards checked; a villain combo is blocked if it includes either |
| Monotone board (all 5 cards one suit) | `flush_suit` is set; logic proceeds normally; villain needs only 1 of that suit |
| Villain range narrowed (facing bet) | `v_range` is already narrowed by `narrow_to_betting_range` before this function runs — blocker applies to narrowed range automatically |
| Suited hand where flush_suit combo is dead (e.g. board has As, hero has Xs of flush suit) | Dead-card check removes the combo correctly |

---

## 8. Open Questions for Owner

1. **Model feature or metadata-only?** The design proposes promoting `flush_block_pct` to
   a model feature (Step 10). This adds a 46th feature to the pipeline and requires
   retraining v9-baseline. Alternative: keep it metadata-only for teaching output only,
   similar to how `_villain_top_pair_plus_pct` coexists with its promoted version. Owner
   decides based on whether retraining cost is justified.

2. **Range narrowing before blocker computation?** Currently, when hero is facing a bet,
   `v_range` is narrowed to villain's betting range before classification. The blocker
   computation inherits this narrowing automatically. Is that correct? On a 3-spade board,
   villain's betting range may be weighted toward flushes, making the blocker signal sharper.
   This is likely the right behavior but worth confirming.

3. **Weighted by frequency or unweighted combos?** The design weights by `freq` (villain's
   GTO mixing frequency). A hand villain plays at 0.5 frequency contributes half as much
   to the denominator and numerator. This mirrors how `villain_top_pair_plus_pct` is
   computed. Alternative: weight all hands equally (ignore frequency). Frequency-weighted
   is more theoretically correct.

---

## 9. Files Affected

| File | Change |
|---|---|
| `river-rats-core/feature_extractor.py` | Add helper function; extend `extract_range_composition` signature and return dict; promote feature in Step 10 |
| `river-rats-core/feature_keys.py` | Add `FLUSH_BLOCK_PCT = 'flush_block_pct'` constant |
| `river-rats-core/hand_categories.py` | No change — existing `count_combos_with_blockers` and `SUITS` constant are already sufficient |
| `river-rats-core/board_analyzer.py` | No change — `flush_suit` already computed |

No new imports required. All dependencies are already present.
