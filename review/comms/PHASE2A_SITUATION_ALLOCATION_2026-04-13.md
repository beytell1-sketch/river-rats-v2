---
date: 2026-04-13
from: Builder team (GTO Expert + ML Architect)
to: Owner (Rupert)
re: Phase 2A — new situation allocation to reach ~400-470 total
status: FOR OWNER REVIEW (Gate 4)
---

# Phase 2A: Situation Allocation Design

## 1. What the surviving 200 look like

### Action distribution

| Action | Count | % | Target for v2.2 |
|--------|-------|---|------------------|
| CHECK | 100 | 50.0% | ≤35% |
| BET | 73 | 36.5% | ~25-30% |
| FOLD | 14 | 7.0% | ~15-20% |
| CALL | 13 | 6.5% | ~15-20% |
| RAISE | 0 | 0.0% | ~5-10% |

**Critical gaps:**
- **RAISE: 0 situations.** The model has never seen a RAISE in
  self-play training data. This is the single biggest gap.
- **CALL: 13 (6.5%).** Severely under-represented for a 5-class
  classifier. The facing-bet test set has 17/40 CALL — the model
  must learn this action well.
- **FOLD: 14 (7.0%).** Same problem.
- **CHECK: 100 (50%).** Over-represented. The sequential bias
  shows here — CHECK was the default for not-facing-bet.
- **BET: 73 (36.5%).** Reasonable but the model needs to see
  diverse BET contexts, not just self-play PFA c-bets.

### Facing-bet split

| | Not facing (173) | Facing (27) |
|---|---|---|
| BET | 73 | — |
| CHECK | 100 | — |
| CALL | — | 13 |
| FOLD | — | 14 |
| RAISE | — | 0 |

**Only 27/200 (13.5%) are facing-bet.** But facing-bet situations
are where the oracle struggles most (65% accuracy vs 82.5% on
check-to-hero). We need substantially more facing-bet data.

### Street distribution

| Street | Count | % |
|--------|-------|---|
| Flop | 67 | 33.5% |
| Turn | 67 | 33.5% |
| River | 66 | 33.0% |

Balanced. No gap here.

### Hero position

| Position | Count | % |
|----------|-------|---|
| BTN | 75 | 37.5% |
| BB | 56 | 28.0% |
| CO | 38 | 19.0% |
| HJ | 23 | 11.5% |
| UTG | 8 | 4.0% |

Reasonable distribution. BTN is over-weighted but BTN is the most
common IP position in 3-way — this is natural.

### Board texture

| Texture | Count |
|---------|-------|
| Rainbow | 97 |
| Two-tone | 89 |
| Monotone | 3 |
| Paired | 69 |

**Monotone: only 3 situations.** Monotone boards produce flush
draws and flush-blocking dynamics — exactly where the NULL
features matter most. Need more.

### Hand strength

| Category | Count |
|----------|-------|
| Monster | 42 |
| Strong made | 70 |
| Made (any) | 116 |
| Drawing (4+ outs) | 35 |
| Air | 49 |

Reasonable mix. Drawing hands are under-represented relative to
their importance for RAISE decisions (semi-bluff raises need
drawing hands with blockers).

## 2. Gaps to fill

| Gap | Severity | Situations needed |
|-----|----------|-------------------|
| **RAISE (any)** | CRITICAL | 25-30 |
| **CALL facing bet** | HIGH | 40-50 |
| **FOLD facing bet** | HIGH | 25-35 |
| **BET diverse contexts** | MEDIUM | 30-40 |
| **CHECK counterexamples** | LOW | 15-20 |
| **Monotone boards** | MEDIUM | 10-15 |
| **Drawing hands** | MEDIUM | 15-20 |

## 3. Allocation table

**Target: ~250 new situations** (200 surviving + 250 new = 450 total)

### BP1: Non-Monster RAISE (25-30 situations)

The highest-priority gap. Per retirement doc and KB v1.3:

| Sub-pattern | Count | Expected label | Hand type |
|-------------|-------|---------------|-----------|
| BP1a: Nut flush draw + blocker | 6-8 | RAISE (semi-bluff) | Drawing |
| BP1b: Combo draw (flush + straight) | 6-8 | RAISE (semi-bluff) | Drawing |
| BP1c: Strong two pair facing bet | 4-5 | RAISE (value) | Strong made |
| BP1d: RAISE counterexamples | 8-10 | CALL | Drawing without blocker, non-nut draws |

BP1d is critical — the model needs the RAISE/CALL boundary, not
just RAISE examples. Per KB Section 1.7: nut draw + blocker = RAISE;
anything less = CALL.

All BP1 situations are facing_bet=1.

### BP2: CALL facing bet (40-50 situations)

The model's weakest axis (44% accuracy on facing-bet CALL).

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP2a: Drawing hands with correct price | 10-12 | Pot odds > equity needed to continue |
| BP2b: Made hands in bet-and-call | 8-10 | Both opponents showed strength, hero calls |
| BP2c: Medium made hands closing action | 8-10 | Hero last to act, marginal but correct call |
| BP2d: Strong made hands (not raising) | 6-8 | Strong hand but raise not correct (flat board, no blockers) |
| BP2e: CALL counterexamples → FOLD | 8-10 | Similar spots where FOLD is correct (equity below pot odds) |

All BP2 facing_bet=1. Mixed streets (flop/turn/river).

### BP3: FOLD facing bet (25-35 situations)

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP3a: Air facing bet | 8-10 | No equity, clear fold |
| BP3b: Medium made vs multi-street aggression | 6-8 | Top pair but villain range above hero |
| BP3c: Drawing hands priced out | 6-8 | Draw outs insufficient for the price |
| BP3d: Bet-and-call range fold | 5-8 | Both opponents showed strength, hero behind |

All BP3 facing_bet=1.

### BP4: BET diverse contexts (30-40 situations)

The surviving 200 have 73 BETs, mostly from self-play PFA c-bets.
Need more diversity.

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP4a: IP value bets (non-PFA) | 8-10 | Hero IP, strong hand, villain checked |
| BP4b: OOP value bets | 6-8 | Hero OOP, strong enough to lead |
| BP4c: Semi-bluff bets (draws) | 6-8 | Hero has draw, villain checked, betting for fold equity |
| BP4d: Protection bets | 5-6 | Made hand on dynamic board, betting to deny equity |
| BP4e: BET counterexamples → CHECK | 8-10 | Similar spots where CHECK is correct |

All BP4 facing_bet=0.

### BP5: CHECK counterexamples (15-20 situations)

The surviving 200 have 100 CHECKs (50%). The model might over-CHECK.
Need situations where CHECK looks tempting but BET is correct.

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP5a: Trap with monster | 5-6 | Monster checks for deception → actually should bet for value 3-way |
| BP5b: Pot control that should be thin value | 5-6 | Medium-strong hand checking → should bet thin |
| BP5c: Air checking → should bluff | 5-6 | Hero has fold equity, board favours hero range → bet |

All BP5 facing_bet=0.

### BP6: Monotone board situations (10-15 situations)

Only 3 monotone boards in the surviving 200. Need flush dynamics.

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP6a: Hero has flush draw on monotone | 4-5 | Key for flush_block_pct and flush_draw_rank features |
| BP6b: Hero has made flush on monotone | 3-4 | Value betting with a made flush |
| BP6c: Hero has no flush card on monotone | 3-4 | Air/weak on monotone → fold or check |

Mixed facing_bet. Mixed streets.

### BP7: Drawing hand RAISE diversity (15-20 situations)

Supplements BP1. Focused on the RAISE/CALL boundary with draws.

| Sub-pattern | Count | Context |
|-------------|-------|---------|
| BP7a: Turn semi-bluff raises | 5-6 | Draws on turn with fold equity |
| BP7b: River bluff raises | 3-4 | Missed draws on river → raise as bluff (rare, strong conditions) |
| BP7c: Draws that should CALL not RAISE | 5-6 | Non-nut draws, no blocker, 3-way → CALL |
| BP7d: Draws that should FOLD not CALL | 3-4 | Priced out draws, bad implied odds |

## 4. Totals

| Batch | Situations | Primary action | facing_bet? |
|-------|-----------|---------------|-------------|
| BP1 | 25-30 | RAISE + CALL | Yes |
| BP2 | 40-50 | CALL + FOLD | Yes |
| BP3 | 25-35 | FOLD | Yes |
| BP4 | 30-40 | BET + CHECK | No |
| BP5 | 15-20 | BET + CHECK | No |
| BP6 | 10-15 | Mixed | Mixed |
| BP7 | 15-20 | RAISE + CALL + FOLD | Yes |
| **Total new** | **160-210** | | |

**Combined with 200 surviving: 360-410 total.**

This is slightly below the ~400-470 target. If the owner wants
to hit 450+, expand BP2 (CALL) and BP4 (BET) by 20 each.

## 5. Projected action distribution (combined)

| Action | Surviving 200 | New (~185 mid) | Total (~385) | % |
|--------|---------------|----------------|-------------|---|
| CHECK | 100 | ~30 | ~130 | 34% |
| BET | 73 | ~45 | ~118 | 31% |
| CALL | 13 | ~60 | ~73 | 19% |
| FOLD | 14 | ~30 | ~44 | 11% |
| RAISE | 0 | ~20 | ~20 | 5% |

No single action exceeds 35% (plan constraint). CALL and FOLD
are now meaningful minorities. RAISE has enough examples for the
model to learn the pattern (20 situations with counterexamples).

## 6. Sizing requirements

All new situations MUST use solver-aligned sizing:
- Flop bets: 25% or 66% pot
- Turn bets: 33% or 75% pot
- River bets: 33% or 75% pot
- Raises: 33% or 66% pot

The surviving 200 keep their original sizing (Option B from
earlier plans — old data retains old sizing).

## 7. Generation requirements

All new situations through the hardened pipeline:
- `situation_factory.py` with `action_string` gate
- `hand_sequence_validator` validates every sequence
- Full 48-feature extraction (zero NULLs)
- 3-way only (BB/CO/BTN or equivalent)
- Stratified by street (roughly 1/3 each)
- Stratified by hero position (mix of IP/OOP/sandwich)

## 8. For owner

**Questions:**
1. Is ~385 total sufficient, or do you want to expand to 450+?
2. BP1 (RAISE) allocation — is 25-30 enough, or more?
3. Should any batch pattern be removed or consolidated?

---

**Awaiting approval. On "go" the programmer generates through
the hardened factory.**
