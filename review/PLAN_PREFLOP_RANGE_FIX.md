# Plan: Preflop Range Fix

**Date:** 6 April 2026
**Status:** PLAN — awaiting review before any building
**Blocking:** 3-way training data generation (Phase A)
**Also fixes:** Phase B preflop accuracy (independent value)

---

## 1. Findings

### The Problem

The preflop engine's range tables are ~50% too tight at every
position. This is the root cause of the 0.51% three-way yield
in data generation, and it's also wrong for production play.

### Diagnostic Data (200-deal sample, all-oracle seats)

| Position | Current open% | GTO target | Gap |
|----------|--------------|------------|-----|
| UTG | 8% | 17.6% | 2.2x too tight |
| HJ | 9% | 21.4% | 2.4x too tight |
| CO | 21% | 27.8% | 1.3x too tight |
| BTN | 23% | 43.5% | 1.9x too tight |
| SB | 7% | 40-50% | 6x too tight |

| Position | Current defend% | GTO target | Gap |
|----------|----------------|------------|-----|
| BTN call vs CO | 4% | ~15% | 3.75x too tight |
| BB defend vs CO | 5% | ~38% | 7.6x too tight |
| BB defend vs BTN | ~5% | ~47% | 9.4x too tight |

### Architecture Audit (from code analysis)

The preflop engine has the RIGHT structure:
- `RFI` dict: per-position opening ranges with per-hand frequencies
- `THREE_BET` dict: per-matchup 3-bet ranges (hero_pos × opener_pos)
- `CALL` dict: per-matchup calling ranges
- `detect_scenario()`: 5 scenarios (rfi, bb_option, defend_call,
  squeeze, defend_3bet)
- GTO mixing: `random.random() < range_frequency` per hand

The structure is sound. The DATA is wrong — the range tables are
too tight. This is a data fix, not an architecture rewrite.

### Key Structural Issues (beyond data)

1. **Squeeze uses same ranges as defend_call.** No adjustment for
   extra dead money from callers. Should widen 3-bet and narrow call.
2. **BB overcall not implemented.** BB defends tighter with callers
   (not wider), but the engine doesn't adjust at all.
3. **SB cold-calls when it shouldn't.** GTO says SB is 3-bet-or-fold
   vs opens, never cold-call. Engine allows SB cold-calling.
4. **BB option uses BTN RFI as proxy.** Should have its own
   isolation range.

### Research Sources

4 research files with 100+ solver-backed sources:
- `research/preflop_rfi_ranges_research.md` — exact hand lists
- `research/preflop_defend_ranges_research.md` — call + 3-bet per matchup
- `research/preflop_overcalling_research.md` — BB tighter with callers
- `research/preflop_sb_strategy_research.md` — SB open/defend strategy

---

## 2. Scope Decision

### What to fix now (unblocks training data generation)

**Phase 1: Replace range table data.**
Update the `RFI`, `THREE_BET`, and `CALL` dicts in `range_manager.py`
with solver-derived hand lists and frequencies from the research.
No structural changes to the engine — just new data in the same
data structures.

This is the minimum viable fix:
- Correct opening frequencies at all positions
- Correct defend frequencies for common matchups
- BB defend scales with opener position (~25% vs UTG → ~47% vs BTN)
- SB 3-bet-or-fold vs opens (remove SB CALL entries)

**Expected impact on 3-way yield:** With BTN opening 43% instead
of 23%, and BB defending 38% instead of 5%, multiway pots should
occur 5-10x more often. The 0.51% yield should become 3-5%.

### What to fix later (Phase B, not blocking)

**Phase 2: Structural improvements.**
- Squeeze range adjustment for caller count
- BB overcalling (tighter with callers, -5 to -8pp)
- BB option isolation range (replace BTN RFI proxy)
- Stack-depth adaptation (currently 100bb only)

These improve accuracy but don't block data generation. The Phase 1
data fix gets ranges "close enough" for realistic multiway pots.

---

## 3. Plan: Phase 1 (Range Table Data Fix)

### Step 1: Write new range tables

Update the 3 dicts in `range_manager.py`:

**RFI (5 positions):**
- UTG 17.6%: `66+, A3s+, K8s+, Q9s+, J9s+, T9s, ATo+, KJo+, QJo`
- HJ 21.4%: `55+, A2s+, K6s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, ATo+, KTo+, QTo+`
- CO 27.8%: `33+, A2s+, K3s+, Q6s+, J8s+, T7s+, 97s+, 87s, 76s, A8o+, KTo+, QTo+, JTo`
- BTN 43.5%: `33+, A2s+, K2s+, Q3s+, J4s+, T6s+, 96s+, 85s+, 75s+, 64s+, 53s+, A4o+, K8o+, Q9o+, J9o+, T8o+, 98o`
- SB ~43%: `22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 96s+, 86s+, 75s+, 65s, 54s, A2o+, K7o+, Q9o+, J9o+, T9o`

**THREE_BET (per matchup):** From defend research.
- SB vs BTN: ~15-20%
- SB vs CO: ~10-13%
- BB vs BTN: ~12%
- BB vs CO: ~9%
- BTN vs CO: ~9%

**CALL (per matchup):** From defend research.
- BTN vs CO: ~15%
- BB vs BTN: ~35%
- BB vs CO: ~29%
- BB vs HJ: ~23%
- BB vs UTG: ~16%
- SB vs any: 0% (3-bet or fold only)

### Step 2: Convert hand lists to dict format

The research gives hand lists like "66+, A3s+, K8s+". These need
to be converted to the `{'AKs': 1.0, 'AQs': 1.0, ...}` format
the range manager expects. This is mechanical — expand notation
to individual hands with frequencies.

### Step 3: Update range_manager.py

Replace the existing `RFI`, `THREE_BET`, and `CALL` dicts with
the new data. Keep the same dict structure and API — `get_rfi_range()`,
`get_3bet_range()`, `get_call_range()` all work unchanged.

Also:
- Remove SB entries from `CALL` dict (SB never cold-calls)
- Add BB defend scaling: separate entries for BB vs each opener
  position (vs_UTG, vs_HJ, vs_CO, vs_BTN, vs_SB)

### Step 4: Update DEFEND dict

The legacy `DEFEND` dict (combined call + 3-bet) needs updating
to match the new `THREE_BET` + `CALL` data, or be removed if
nothing depends on it.

### Step 5: Test

- Run the preflop frequency diagnostic again (200 deals)
- Verify: UTG opens ~17%, CO opens ~28%, BTN opens ~43%, BB
  defends ~35-40% vs CO
- Run 3-way yield check: should see 3-5% of games going 3-way
- Run existing preflop tests to check for regressions

### Step 6: Regenerate training data

With correct ranges, run generation again (~2000 deals should
produce ~200 three-way situations).

---

## 4. Files to Change

| File | Change | Risk |
|------|--------|------|
| `range_manager.py` | Replace RFI, THREE_BET, CALL dicts with solver data | Medium — this is the core data, affects everything |
| `preflop_engine.py` | Remove SB cold-call path in `_decide_defend_call()` | Low — SB should 3-bet-or-fold |
| `range_manager.py` | Update or remove legacy DEFEND dict | Low — verify nothing depends on it |

**Files NOT changed:**
- `preflop_engine.py` scenario detection (correct)
- `preflop_engine.py` mixing logic (correct)
- `poker_game.py` callback integration (correct)
- `feature_extractor.py` range composition (uses range_manager API)

---

## 5. Risks

**Range accuracy.** The research gives approximate hand lists, not
exact solver grids. Mixed-frequency hands (e.g., "55 opens 60%
from UTG") are estimated. The hand lists are close enough for
realistic play but not solver-perfect. Good enough for production
and data generation.

**Downstream impact.** The feature extractor's range composition
features (villain_top_pair_plus_pct, villain_air_pct, etc.) are
computed from the range tables. Changing the ranges changes these
features for every hand. This is CORRECT — the old features were
based on wrong ranges. But it means the 40-hand reference evaluation
scores may shift (the oracle's predictions won't change, but the
features it sees will).

**Test regression.** Some preflop tests may be calibrated to the
old ranges. These tests are testing the wrong ranges and should
be updated, not preserved.

---

## 6. Sequence

```
1. Write new range data (hand lists → dict format)
   → PRESENT for review

2. Update range_manager.py
   → PRESENT for review (diff against old)

3. Fix SB cold-call in preflop_engine.py
   → PRESENT for review

4. Run diagnostic (200-deal frequency check)
   → PRESENT results for review

5. Run 3-way yield check (~500 deals)
   → PRESENT yield stats for review

6. Update tests
   → Run full test suite, PRESENT results

7. Regenerate training data (~2000 deals)
   → PRESENT output stats for review
```

Each step requires review approval before proceeding.

---

## 7. What This Does NOT Cover

- Squeeze range adjustment for caller count (Phase 2)
- BB overcalling adjustment (Phase 2)
- BB option isolation range (Phase 2)
- Stack-depth adaptation (Phase 2)
- Postflop range composition recalibration (handled automatically
  by the feature extractor reading the updated range tables)
