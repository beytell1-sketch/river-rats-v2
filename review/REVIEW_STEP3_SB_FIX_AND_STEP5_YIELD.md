# Review: Step 3 (SB Cold-Call Fix) + Step 5 (3-Way Yield Check)

**Date:** 6 April 2026
**Status:** REVIEW — awaiting owner decision on next steps

---

## Step 3: SB Cold-Call Fix — APPLIED

### What changed

Two one-line edits in `river-rats-core/preflop_engine.py`:

**Line 284** (`_decide_defend_call`):
```python
# Before:
elif _implied_odds_override(hand, opener_pos):

# After:
elif hero_pos.upper() != 'SB' and _implied_odds_override(hand, opener_pos):
```

**Line 383** (`_decide_squeeze`):
```python
# Before:
elif _implied_odds_override(hand, opener_pos):

# After:
elif hero_pos.upper() != 'SB' and _implied_odds_override(hand, opener_pos):
```

### Why

The CALL dict correctly returns `{}` for SB (line 1600 of
`range_manager.py`), but the implied odds override bypassed
this and could still produce CALL for SB with small pairs
(22-55) and suited connectors (54s-98s) vs non-tight openers.
GTO says SB is strictly 3-bet-or-fold.

### Risk

Low. Only affects SB facing opens with 10 specific hands.
These hands either appear in SB's THREE_BET dict (and get
3-bet) or fold. Both are correct GTO outcomes.

---

## Step 5: 3-Way Yield Check — GATE FAILED

### Run parameters

- Deals: 500
- Seed: 200
- All 6 seats use oracle callbacks
- Output: `/tmp/yield_check_3way.jsonl`

### Raw results

| Metric | Value |
|--------|-------|
| Deals | 500 |
| Games (6 rotations/deal) | 3,000 |
| 3-way postflop decisions | 36 |
| **Yield** | **1.20%** |
| Previous yield (pre-range-fix) | 0.51% |
| Improvement | 2.4x |
| Target | >= 3% |
| **Gate** | **FAILED** |

### Distribution

| Dimension | Breakdown | Concern? |
|-----------|-----------|----------|
| Street | flop 12, turn 12, river 12 | Even — good |
| Position | OOP 24, IP 12 | 2:1 OOP-heavy — acceptable |
| Facing bet | 1 facing, 35 not facing | BAD — 97% uncontested |
| Oracle action | CHECK 34, RAISE 1, FOLD 1 | BAD — no call/fold/raise signal |

### What this means for training

Even with brute-force volume (~17,000 deals for ~200 situations),
94% would be CHECK decisions. A model trained on that won't learn
when to bet, call, or fold in 3-way pots.

---

## Range Data Verification — RANGES ARE CORRECT

This is a key finding. The original diagnostic flagged BTN opening
at 20% vs 43% target, which looked like tight ranges. I verified
the actual range sizes:

| Position | Hands in RFI dict | % of 169 combos | Target | Status |
|----------|-------------------|-----------------|--------|--------|
| UTG | 38 | 22.5% | 17.6% | Wider than target |
| HJ | 47 | 27.8% | 21.4% | Wider than target |
| CO | 62 | 36.7% | 27.8% | Wider than target |
| BTN | 90 | 53.3% | 43.5% | Wider than target |
| SB | 86 | 50.9% | ~43% | Wider than target |

**All positions are wider than GTO targets.** The observed 20%
open rate for BTN is expected because BTN can only RFI when
UTG, HJ, and CO all fold first. With earlier positions opening
~22-37% each, BTN gets an RFI opportunity only ~35% of the time.

The "BTN at 20% vs 43%" flag was a false alarm — 43% is the
range width, not the expected open rate at a table where 3
players act before BTN.

**Preflop ranges do not need further widening.**

### Defend ranges

| Matchup | Call hands | 3-bet hands |
|---------|-----------|-------------|
| BB vs UTG | 35 | 4 |
| BB vs HJ | 44 | 8 |
| BB vs CO | 62 | 9 |
| BB vs BTN | 77 | 11 |
| BB vs SB | 70 | 19 |
| SB vs UTG | 0 (correct) | 8 |
| SB vs HJ | 0 (correct) | 11 |
| SB vs CO | 0 (correct) | 16 |
| SB vs BTN | 0 (correct) | 27 |
| BTN vs UTG | 17 | 3 |
| BTN vs HJ | 25 | 6 |
| BTN vs CO | 31 | 6 |

SB has zero call hands everywhere — confirms 3-bet-or-fold is
correctly implemented in the data.

---

## Where the yield is leaking

The preflop diagnostic showed 6.3% of deals go multiway.
But only 1.2% of games produce a 3-way postflop decision.

**Layer 1 — Preflop (working):** Ranges are correct, multiway
pots form at 6.3%.

**Layer 2 — Postflop collapse (the leak):** ~80% of multiway
pots lose a player before a hero 3-way decision is recorded.
The oracle folds one opponent quickly on the flop.

**Layer 3 — Action quality (secondary):** Of 36 surviving
situations, 35 are "checked to hero" with no bet to face.
The oracle checks most multiway flops (correct GTO tendency
but limits training signal).

---

## Options

**A. Brute-force volume (~17,000 deals)**
Gets ~200 situations but 94% CHECK. Training data quality
is poor. Not recommended.

**B. Investigate postflop collapse (recommended)**
Why does the oracle fold one player so quickly in multiway
pots? Possible causes:
- Multiway adjuster too aggressive with fold recommendations
- Oracle model (v8/v9) trained on HU data, over-folds multiway
- Equity calculations in multiway spots pushing toward fold
This directly addresses the 6.3% -> 1.2% leak.

**C. Investigate action distribution**
Why are 94% of surviving 3-way decisions CHECK? Possible:
- Oracle is check-heavy in multiway (GTO-correct but limiting)
- facing_bet detection issue in the callback
Lower priority than B.

**D. Combine B + C**
Fix the postflop collapse first, then assess if action
distribution improves naturally.

---

## My Recommendation

**Option B first.** The 6.3% -> 1.2% collapse is the biggest
leak. If we can retain even 50% of multiway pots through the
flop (instead of 20%), yield jumps to ~3% and the action
distribution likely improves too (more opponents = more bets).

Start by examining what the multiway adjuster does with
fold recommendations in 3-way pots.

---

## Files changed this session

| File | Change |
|------|--------|
| `river-rats-core/preflop_engine.py:284` | SB excluded from implied odds override in defend_call |
| `river-rats-core/preflop_engine.py:383` | SB excluded from implied odds override in squeeze |
