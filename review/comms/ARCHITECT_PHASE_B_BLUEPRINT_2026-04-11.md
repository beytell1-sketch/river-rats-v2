# Phase B Range Fix — Implementation Blueprint
# Date: 2026-04-11
# Author: architect

---

## 1. Pre-Implementation Check Results

### 1.1 Line number verification

All cited line numbers in the design document were verified against the current source.
Results:

| Dict / Location | Design says | Actual line | Match? |
|---|---|---|---|
| RFI dict open brace | 127 | 127 | YES |
| THREE_BET dict open brace | 471 | 471 | YES |
| CALL_VS_3BET dict open brace | 670 | 670 | YES |
| FOURBET dict open brace | 727 | 727 | YES |
| DEFEND dict open brace | 746 | 746 | YES |
| THREEB dict open brace | 911 | 911 | YES |
| THREEB alias block end | 1107 | 1107 | YES |
| CALL dict open brace | 1110 | 1110 | YES |
| CALL alias block end | 1499 | 1499 | YES |

### 1.2 Duplicate get_3bet_range() confirmed

There are two definitions of `get_3bet_range()` inside class `RangeManager`:

- **Line 1539**: reads from `THREEB` (stale — reads dead dict)
- **Line 1617**: reads from `THREE_BET` (live — this is the keeper)

The stale definition at line 1539 must be deleted along with the THREEB dict.

### 1.3 get_call_range() reads from CALL, not THREEB

`get_call_range()` at line 1578 reads from `CALL`. Unaffected by THREEB removal.

`get_defend_range()` at line 1522 calls `self.get_3bet_range()` + `self.get_call_range()`.
After the stale `get_3bet_range()` at 1539 is removed, Python will resolve
`self.get_3bet_range()` to the live definition at line 1617 (renumbered after earlier edits).
This is correct.

### 1.4 THREEB import check — no test file imports THREEB

- `test_preflop_engine.py`: no import of THREEB (docstring references only — safe to delete)
- `test_range_manager_preflop.py`: no import of THREEB — safe to delete

### 1.5 RFI structure compatibility

`get_rfi_range()` at line 1513 does `RFI.get(pos, RFI['HJ']).copy()`.
New RFI dict has the same top-level position keys (UTG, HJ, CO, BTN, SB) and the same
hand→float structure. Compatible.

### 1.6 THREE_BET structure compatibility

`get_3bet_range()` (live, line 1617) does `THREE_BET[hero][vs_key].copy()`.
New THREE_BET dict has the same hero → vs_position → hand→float structure. Compatible.

### 1.7 Feature 49 (hero_range_percentile) downstream note

`feature_extractor.py` feature 49 reads hero range via `get_rfi_range()` or
`get_postflop_range()`. New RFI values introduce mixed frequencies (e.g. UTG 66→0.5,
55→0.25). This will shift hero_range_percentile for hands in those positions. Any
`reference_evaluator.py` assertions tied to specific hero_range_percentile thresholds
for UTG 66/55/A4s/A5s/98s/87s will shift. No test in the suite currently hard-codes
those exact values, so no additional changes needed. Flag for monitoring.

---

## 2. Sequenced Edit List

Execute edits in this exact order. Do not reorder.

---

### EDIT 1 — range_manager.py: Replace RFI dict (lines 127–468)

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/range_manager.py`

**Lines to replace:** 127–468 (the full RFI dict literal from `RFI = {` through the closing `}` before the alias lines)

**Old content (lines 127–466):**
```
RFI = {
    'UTG': {
        "66": 1.0,
        ...
    },
    ...
    'SB': {
        ...
        "TT": 1.0,
    },

}
```
(The entire block from line 127 to line 466 inclusive, ending with the lone `}`)

**New content — exact replacement:**

```python
RFI = {
    'UTG': {
        # Pairs: 66+ pure; 55 mixed per test oracle; no 22-44
        '55': 0.25,
        '66': 0.5,
        '77': 1.0,
        '88': 1.0,
        '99': 1.0,
        'TT': 1.0,
        'JJ': 1.0,
        'QQ': 1.0,
        'KK': 1.0,
        'AA': 1.0,
        # Suited Aces: A3s+ pure; A5s and A4s mixed (blocker hands)
        'A3s': 1.0,
        'A4s': 0.3,
        'A5s': 0.5,
        'A6s': 1.0,
        'A7s': 1.0,
        'A8s': 1.0,
        'A9s': 1.0,
        'ATs': 1.0,
        'AJs': 1.0,
        'AQs': 1.0,
        'AKs': 1.0,
        # Suited Kings: K8s+
        'K8s': 1.0,
        'K9s': 1.0,
        'KTs': 1.0,
        'KJs': 1.0,
        'KQs': 1.0,
        # Suited Queens: Q9s+
        'Q9s': 1.0,
        'QTs': 1.0,
        'QJs': 1.0,
        # Suited Jacks: J9s+
        'J9s': 1.0,
        'JTs': 1.0,
        # Suited connectors: T9s pure; 98s and 87s mixed
        'T9s': 1.0,
        '98s': 0.25,
        '87s': 0.2,
        # Offsuit Aces: ATo+
        'ATo': 1.0,
        'AJo': 1.0,
        'AQo': 1.0,
        'AKo': 1.0,
        # Offsuit Kings: KJo+
        'KJo': 1.0,
        'KQo': 1.0,
        # Offsuit Queens: QJo
        'QJo': 1.0,
    },

    'HJ': {
        # Pairs: 55+ pure; 44 mixed
        '44': 0.4,
        '55': 1.0,
        '66': 1.0,
        '77': 1.0,
        '88': 1.0,
        '99': 1.0,
        'TT': 1.0,
        'JJ': 1.0,
        'QQ': 1.0,
        'KK': 1.0,
        'AA': 1.0,
        # Suited Aces: A2s+
        'A2s': 1.0,
        'A3s': 1.0,
        'A4s': 1.0,
        'A5s': 1.0,
        'A6s': 1.0,
        'A7s': 1.0,
        'A8s': 1.0,
        'A9s': 1.0,
        'ATs': 1.0,
        'AJs': 1.0,
        'AQs': 1.0,
        'AKs': 1.0,
        # Suited Kings: K6s+
        'K6s': 1.0,
        'K7s': 1.0,
        'K8s': 1.0,
        'K9s': 1.0,
        'KTs': 1.0,
        'KJs': 1.0,
        'KQs': 1.0,
        # Suited Queens: Q9s+
        'Q9s': 1.0,
        'QTs': 1.0,
        'QJs': 1.0,
        # Suited Jacks: J9s+
        'J9s': 1.0,
        'JTs': 1.0,
        # Suited connectors: T9s, 98s, 87s, 76s
        'T9s': 1.0,
        '98s': 1.0,
        '87s': 1.0,
        '76s': 1.0,
        # Offsuit Aces: ATo+
        'ATo': 1.0,
        'AJo': 1.0,
        'AQo': 1.0,
        'AKo': 1.0,
        # Offsuit Kings: KTo+
        'KTo': 1.0,
        'KJo': 1.0,
        'KQo': 1.0,
        # Offsuit Queens: QTo+
        'QTo': 1.0,
        'QJo': 1.0,
    },

    'CO': {
        # Pairs: 33+ pure; 22 mixed
        '22': 0.4,
        '33': 1.0,
        '44': 1.0,
        '55': 1.0,
        '66': 1.0,
        '77': 1.0,
        '88': 1.0,
        '99': 1.0,
        'TT': 1.0,
        'JJ': 1.0,
        'QQ': 1.0,
        'KK': 1.0,
        'AA': 1.0,
        # Suited Aces: A2s+
        'A2s': 1.0,
        'A3s': 1.0,
        'A4s': 1.0,
        'A5s': 1.0,
        'A6s': 1.0,
        'A7s': 1.0,
        'A8s': 1.0,
        'A9s': 1.0,
        'ATs': 1.0,
        'AJs': 1.0,
        'AQs': 1.0,
        'AKs': 1.0,
        # Suited Kings: K3s+
        'K3s': 1.0,
        'K4s': 1.0,
        'K5s': 1.0,
        'K6s': 1.0,
        'K7s': 1.0,
        'K8s': 1.0,
        'K9s': 1.0,
        'KTs': 1.0,
        'KJs': 1.0,
        'KQs': 1.0,
        # Suited Queens: Q6s+
        'Q6s': 1.0,
        'Q7s': 1.0,
        'Q8s': 1.0,
        'Q9s': 1.0,
        'QTs': 1.0,
        'QJs': 1.0,
        # Suited Jacks: J8s+
        'J8s': 1.0,
        'J9s': 1.0,
        'JTs': 1.0,
        # Suited Tens: T7s+
        'T7s': 1.0,
        'T8s': 1.0,
        'T9s': 1.0,
        # Suited nines: 97s+
        '97s': 1.0,
        '98s': 1.0,
        # Other suited connectors
        '87s': 1.0,
        '76s': 1.0,
        '65s': 0.5,
        # Offsuit Aces: A8o+
        'A8o': 1.0,
        'A9o': 1.0,
        'ATo': 1.0,
        'AJo': 1.0,
        'AQo': 1.0,
        'AKo': 1.0,
        # Offsuit Kings: KTo+
        'KTo': 1.0,
        'KJo': 1.0,
        'KQo': 1.0,
        # Offsuit Queens: QTo+
        'QTo': 1.0,
        'QJo': 1.0,
        # Offsuit Jacks: JTo
        'JTo': 1.0,
    },

    'BTN': {
        # Pairs: 33+ pure; 22 mixed
        '22': 0.6,
        '33': 1.0,
        '44': 1.0,
        '55': 1.0,
        '66': 1.0,
        '77': 1.0,
        '88': 1.0,
        '99': 1.0,
        'TT': 1.0,
        'JJ': 1.0,
        'QQ': 1.0,
        'KK': 1.0,
        'AA': 1.0,
        # Suited Aces: A2s+
        'A2s': 1.0,
        'A3s': 1.0,
        'A4s': 1.0,
        'A5s': 1.0,
        'A6s': 1.0,
        'A7s': 1.0,
        'A8s': 1.0,
        'A9s': 1.0,
        'ATs': 1.0,
        'AJs': 1.0,
        'AQs': 1.0,
        'AKs': 1.0,
        # Suited Kings: K2s+
        'K2s': 1.0,
        'K3s': 1.0,
        'K4s': 1.0,
        'K5s': 1.0,
        'K6s': 1.0,
        'K7s': 1.0,
        'K8s': 1.0,
        'K9s': 1.0,
        'KTs': 1.0,
        'KJs': 1.0,
        'KQs': 1.0,
        # Suited Queens: Q3s+
        'Q3s': 1.0,
        'Q4s': 1.0,
        'Q5s': 1.0,
        'Q6s': 1.0,
        'Q7s': 1.0,
        'Q8s': 1.0,
        'Q9s': 1.0,
        'QTs': 1.0,
        'QJs': 1.0,
        # Suited Jacks: J4s+
        'J4s': 1.0,
        'J5s': 1.0,
        'J6s': 1.0,
        'J7s': 1.0,
        'J8s': 1.0,
        'J9s': 1.0,
        'JTs': 1.0,
        # Suited Tens: T6s+
        'T6s': 1.0,
        'T7s': 1.0,
        'T8s': 1.0,
        'T9s': 1.0,
        # Suited nines: 96s+
        '96s': 1.0,
        '97s': 1.0,
        '98s': 1.0,
        # Suited eights: 85s+
        '85s': 1.0,
        '86s': 1.0,
        '87s': 1.0,
        # Suited sevens: 75s+
        '75s': 1.0,
        '76s': 1.0,
        # Suited sixes: 64s+
        '64s': 1.0,
        '65s': 1.0,
        # Suited fives: 53s+
        '53s': 1.0,
        '54s': 1.0,
        # Offsuit Aces: A4o+
        'A4o': 1.0,
        'A5o': 1.0,
        'A6o': 1.0,
        'A7o': 1.0,
        'A8o': 1.0,
        'A9o': 1.0,
        'ATo': 1.0,
        'AJo': 1.0,
        'AQo': 1.0,
        'AKo': 1.0,
        # Offsuit Kings: K8o+
        'K8o': 1.0,
        'K9o': 1.0,
        'KTo': 1.0,
        'KJo': 1.0,
        'KQo': 1.0,
        # Offsuit Queens: Q9o+
        'Q9o': 1.0,
        'QTo': 1.0,
        'QJo': 1.0,
        # Offsuit Jacks: J9o+
        'J9o': 1.0,
        'JTo': 1.0,
        # Offsuit Tens: T8o+
        'T8o': 1.0,
        'T9o': 1.0,
        # Offsuit nines: 98o
        '98o': 1.0,
    },

    'SB': {
        # All pairs (22+)
        '22': 1.0,
        '33': 1.0,
        '44': 1.0,
        '55': 1.0,
        '66': 1.0,
        '77': 1.0,
        '88': 1.0,
        '99': 1.0,
        'TT': 1.0,
        'JJ': 1.0,
        'QQ': 1.0,
        'KK': 1.0,
        'AA': 1.0,
        # Suited Aces: A2s+
        'A2s': 1.0,
        'A3s': 1.0,
        'A4s': 1.0,
        'A5s': 1.0,
        'A6s': 1.0,
        'A7s': 1.0,
        'A8s': 1.0,
        'A9s': 1.0,
        'ATs': 1.0,
        'AJs': 1.0,
        'AQs': 1.0,
        'AKs': 1.0,
        # Suited Kings: K2s+
        'K2s': 1.0,
        'K3s': 1.0,
        'K4s': 1.0,
        'K5s': 1.0,
        'K6s': 1.0,
        'K7s': 1.0,
        'K8s': 1.0,
        'K9s': 1.0,
        'KTs': 1.0,
        'KJs': 1.0,
        'KQs': 1.0,
        # Suited Queens: Q4s+
        'Q4s': 1.0,
        'Q5s': 1.0,
        'Q6s': 1.0,
        'Q7s': 1.0,
        'Q8s': 1.0,
        'Q9s': 1.0,
        'QTs': 1.0,
        'QJs': 1.0,
        # Suited Jacks: J6s+
        'J6s': 1.0,
        'J7s': 1.0,
        'J8s': 1.0,
        'J9s': 1.0,
        'JTs': 1.0,
        # Suited Tens: T6s+
        'T6s': 1.0,
        'T7s': 1.0,
        'T8s': 1.0,
        'T9s': 1.0,
        # Suited nines: 96s+
        '96s': 1.0,
        '97s': 1.0,
        '98s': 1.0,
        # Suited eights: 86s+
        '86s': 1.0,
        '87s': 1.0,
        # Suited sevens: 75s+
        '75s': 1.0,
        '76s': 1.0,
        # Suited connectors: 65s, 54s
        '65s': 1.0,
        '54s': 1.0,
        # Offsuit Aces: A2o+
        'A2o': 1.0,
        'A3o': 1.0,
        'A4o': 1.0,
        'A5o': 1.0,
        'A6o': 1.0,
        'A7o': 1.0,
        'A8o': 1.0,
        'A9o': 1.0,
        'ATo': 1.0,
        'AJo': 1.0,
        'AQo': 1.0,
        'AKo': 1.0,
        # Offsuit Kings: K7o+
        'K7o': 1.0,
        'K8o': 1.0,
        'K9o': 1.0,
        'KTo': 1.0,
        'KJo': 1.0,
        'KQo': 1.0,
        # Offsuit Queens: Q9o+
        'Q9o': 1.0,
        'QTo': 1.0,
        'QJo': 1.0,
        # Offsuit Jacks: J9o+
        'J9o': 1.0,
        'JTo': 1.0,
        # Offsuit Tens: T9o
        'T9o': 1.0,
    },

}
```

**Verification grep (run after edit):**
```
grep -c "'66': 0.5" river-rats-core/range_manager.py
```
Expected: 1

```
grep -c "'55': 0.25" river-rats-core/range_manager.py
```
Expected: 1

```
grep -c "'A4s': 0.3" river-rats-core/range_manager.py
```
Expected: 1

```
grep -c "'22': 0.4" river-rats-core/range_manager.py
```
Expected: 1 (CO entry)

Note: the alias lines `RFI['MP'] = RFI['HJ']` and `RFI['EP'] = RFI['UTG']` at lines 467–468
are NOT part of the replaced block. They remain as-is after the closing `}` of the new dict.

---

### EDIT 2 — range_manager.py: Replace THREE_BET dict (lines 471–668)

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/range_manager.py`

**Lines to replace:** 471–659 (the full THREE_BET dict literal, from `THREE_BET = {` through
the lone closing `}` on line 659, before the alias block at lines 660–667)

**New content — exact replacement:**

```python
THREE_BET = {
    'BB': {
        'vs_BTN': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 1.0,
            'TT': 0.5,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AJs': 1.0,
            'ATs': 0.5,
            'AQo': 0.5,
            # Bluffs (suited blockers)
            'A5s': 1.0,
            'A4s': 1.0,
            'A3s': 1.0,
            'A2s': 1.0,
            'K9s': 0.5,
            'Q9s': 0.5,
            'J9s': 0.5,
            'T8s': 0.5,
            '97s': 0.5,
        },
        'vs_CO': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 0.7,
            'TT': 0.3,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AJs': 0.5,
            'AQo': 0.3,
            # Bluffs
            'A5s': 1.0,
            'A4s': 1.0,
            'A3s': 1.0,
            'K9s': 0.3,
        },
        'vs_HJ': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 0.5,
            'TT': 0.25,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            # Bluffs
            'A5s': 1.0,
            'A4s': 1.0,
        },
        'vs_UTG': {
            # Value only — UTG range is strong
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 0.5,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 0.5,
        },
        'vs_SB': {
            # BB vs SB: widest defend. Keep existing (already well-calibrated).
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 1.0,
            'TT': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AJs': 1.0,
            'ATs': 1.0,
            'AQo': 0.5,
            'A5s': 1.0,
            'A4s': 1.0,
            'A3s': 1.0,
            'A2s': 1.0,
            'K9s': 1.0,
            'Q9s': 1.0,
            'J9s': 1.0,
            'T8s': 1.0,
            '97s': 1.0,
        },
    },

    'BTN': {
        'vs_CO': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 0.5,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AQo': 0.5,
            # Bluffs
            'A5s': 0.5,
            'A4s': 0.5,
            'K9s': 0.5,
            'Q9s': 0.3,
        },
        'vs_HJ': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 0.5,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AQo': 0.3,
            # Bluffs
            'A5s': 0.5,
            'K9s': 0.3,
        },
        'vs_UTG': {
            # Value only — UTG is tight
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            # Bluff at low freq
            'A5s': 0.3,
        },
    },

    'CO': {
        'vs_HJ': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 0.5,
            'TT': 0.3,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            # Bluffs
            'A5s': 1.0,
            'A4s': 1.0,
        },
        'vs_UTG': {
            # Value
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 0.5,
            # Bluff
            'A5s': 0.5,
        },
    },

    'HJ': {
        'vs_UTG': {
            # Value only — UTG vs HJ is very tight
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
        },
    },

    'SB': {
        # SB ranges: keep existing data (well-calibrated in current source)
        'vs_BTN': {
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 1.0,
            'TT': 1.0,
            '99': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'AQo': 1.0,
            'AJs': 1.0,
            'ATs': 1.0,
            'A5s': 1.0,
            'A4s': 1.0,
            'A3s': 1.0,
            'A2s': 1.0,
            'KQs': 1.0,
            'K9s': 1.0,
            'K8s': 1.0,
            'Q9s': 1.0,
            'J9s': 1.0,
            'T8s': 1.0,
            '97s': 1.0,
            '86s': 1.0,
            '75s': 1.0,
            '64s': 1.0,
            '53s': 1.0,
        },
        'vs_CO': {
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 1.0,
            'TT': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'A5s': 1.0,
            'A4s': 1.0,
            'A3s': 1.0,
            'AJs': 0.5,
            'AQo': 0.5,
            'K9s': 0.5,
            'Q9s': 0.5,
            'J9s': 0.5,
        },
        'vs_HJ': {
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'JJ': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 1.0,
            'A5s': 1.0,
            'A4s': 1.0,
            'AJs': 0.5,
            'TT': 0.5,
        },
        'vs_UTG': {
            'AA': 1.0,
            'KK': 1.0,
            'QQ': 1.0,
            'AKs': 1.0,
            'AKo': 1.0,
            'AQs': 0.5,
            'JJ': 0.5,
            'A5s': 0.5,
        },
    },

}
```

The alias block (lines 660–667) remains unchanged:
```python
THREE_BET['BB']['vs_MP'] = THREE_BET['BB']['vs_HJ']
THREE_BET['BB']['vs_EP'] = THREE_BET['BB']['vs_UTG']
THREE_BET['SB']['vs_MP'] = THREE_BET['SB']['vs_HJ']
THREE_BET['SB']['vs_EP'] = THREE_BET['SB']['vs_UTG']
THREE_BET['BTN']['vs_MP'] = THREE_BET['BTN']['vs_HJ']
THREE_BET['BTN']['vs_EP'] = THREE_BET['BTN']['vs_UTG']
THREE_BET['CO']['vs_MP'] = THREE_BET['CO']['vs_HJ']
THREE_BET['CO']['vs_EP'] = THREE_BET['CO']['vs_UTG']
```

**Verification grep:**
```
grep -c "'JJ': 1.0" river-rats-core/range_manager.py
```
Expected: count includes the new BB vs_BTN and vs_SB entries. At least 6 occurrences total across the file.

```
grep -c "'TT': 0.5" river-rats-core/range_manager.py
```
Expected: 2 (BB vs_BTN and BB vs_SB entries in THREE_BET)

```
grep -c "'QQ': 0.5" river-rats-core/range_manager.py
```
Expected: 2 (BB vs_UTG and CO vs_UTG entries)

---

### EDIT 3 — range_manager.py: Delete THREEB dict and stale get_3bet_range() (lines 903–1107 + lines 1539–1576)

This edit has two sub-parts. Execute in order.

#### EDIT 3a — Delete THREEB dict including its aliases

**Lines to delete:** 903–1107

This is the entire block from the comment header:
```
# =============================================================================
# 3BET RANGES (Preflop Re-raise)
# =============================================================================
```
through the final alias line:
```
THREEB['CO']['vs_EP'] = THREEB['CO']['vs_UTG']
```

Replace the entire block with a single comment line:

```python
# THREEB dict removed — was an exact duplicate of THREE_BET. See THREE_BET above.
```

**Verification grep:**
```
grep -c "^THREEB" river-rats-core/range_manager.py
```
Expected: 0

```
grep -c "THREEB\[" river-rats-core/range_manager.py
```
Expected: 0

#### EDIT 3b — Delete stale get_3bet_range() definition (reads from THREEB)

After EDIT 3a, re-read the file to get fresh line numbers.

Find the first `def get_3bet_range` inside class `RangeManager`. This is the stale one that
read from `THREEB`. It begins with:

```python
    def get_3bet_range(self, hero_pos: str, vs_position: str) -> Dict[str, float]:
        """
        Get 3bet range for hero position vs opener.
        
        Args:
            hero_pos: Hero's position (BB, SB, BTN, CO, HJ)
            vs_position: Opener's position (UTG, HJ, CO, BTN)
        
        Returns:
            Dict of {hand: frequency}
        """
        hero = hero_pos.upper()
        vs = vs_position.upper()
        
        # Normalize position names
        if vs == 'MP':
            vs = 'HJ'
        elif vs == 'EP':
            vs = 'UTG'
        
        # Get range
        if hero not in THREEB:
            return THREEB['BB']['vs_BTN'].copy()
        
        vs_key = f"vs_{vs}"
        if vs_key not in THREEB[hero]:
            # Find closest match
            if vs in ('UTG', 'EP'):
                vs_key = 'vs_UTG' if 'vs_UTG' in THREEB[hero] else list(THREEB[hero].keys())[0]
            elif vs in ('HJ', 'MP'):
                vs_key = 'vs_HJ' if 'vs_HJ' in THREEB[hero] else 'vs_CO'
            else:
                vs_key = 'vs_BTN' if 'vs_BTN' in THREEB[hero] else list(THREEB[hero].keys())[-1]
        
        if vs_key in THREEB[hero]:
            return THREEB[hero][vs_key].copy()
        
        return THREEB['BB']['vs_BTN'].copy()
```

Delete this entire method definition. Do not delete `get_call_range()` immediately following it.

**Verification grep (after both 3a and 3b):**
```
grep -c "def get_3bet_range" river-rats-core/range_manager.py
```
Expected: 1 (only the keeper, which reads from THREE_BET)

```
grep -c "THREEB" river-rats-core/range_manager.py
```
Expected: 1 (only the replacement comment line added in 3a)

---

### EDIT 4 — range_manager.py: Replace CALL['BTN'] sub-dicts (lines 1412–1492)

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/range_manager.py`

The BB sub-dicts in CALL (vs_BTN, vs_CO, vs_HJ, vs_SB, vs_UTG) are left unchanged per design.
Only the `'BTN'` entry changes.

**Lines to replace:** 1412–1492 (from `    'BTN': {` through the closing `    },` that ends the BTN block,
before the closing `}` of the CALL dict at line 1494)

**Old content (lines 1412–1492):**
The existing BTN sub-dict with vs_CO (30 hands), vs_HJ (24 hands), vs_UTG (17 hands).

**New content:**
```python
    'BTN': {
        'vs_CO': {
            # Pairs: 22-TT (JJ+ 3-bet)
            '22': 1.0,
            '33': 1.0,
            '44': 1.0,
            '55': 1.0,
            '66': 1.0,
            '77': 1.0,
            '88': 1.0,
            '99': 1.0,
            'TT': 0.5,   # mixed call/3bet
            # Suited Aces: A2s-A5s (A6s+ 3bet or RFI)
            'A2s': 1.0,
            'A3s': 1.0,
            'A4s': 0.5,  # partial 3bet
            'A5s': 0.5,  # partial 3bet
            # Suited Kings
            'KTs': 1.0,
            'KJs': 1.0,
            'KQs': 0.5,  # KQs mixed call/3bet
            # Suited Queens
            'QTs': 1.0,
            'QJs': 1.0,
            # Suited Jacks
            'JTs': 1.0,
            # Suited connectors
            'T9s': 1.0,
            '98s': 1.0,
            '87s': 1.0,
            '76s': 1.0,
            '65s': 0.5,
            # Offsuit broadways
            'AJo': 0.5,  # mixed call/3bet
            'AQo': 0.5,  # partial 3bet
            'KQo': 0.5,  # mixed call/fold
            'ATs': 1.0,
            'AJs': 0.5,
        },
        'vs_HJ': {
            # Pairs: 33-TT
            '33': 1.0,
            '44': 1.0,
            '55': 1.0,
            '66': 1.0,
            '77': 1.0,
            '88': 1.0,
            '99': 1.0,
            'TT': 0.5,
            # Suited Aces
            'A2s': 1.0,
            'A3s': 1.0,
            'A4s': 0.5,
            'A5s': 0.5,
            # Suited broadways
            'KTs': 1.0,
            'KJs': 1.0,
            'KQs': 0.5,
            'QTs': 1.0,
            'QJs': 1.0,
            'JTs': 1.0,
            'ATs': 1.0,
            'AJs': 0.5,
            # Suited connectors
            'T9s': 1.0,
            '98s': 1.0,
            '87s': 1.0,
            '76s': 0.5,
            '65s': 0.3,
            # Offsuit
            'AQo': 0.3,
            'KQo': 0.3,
        },
        'vs_UTG': {
            # Pairs: 44-TT (33 is borderline; set to 0.5)
            '33': 0.5,
            '44': 1.0,
            '55': 1.0,
            '66': 1.0,
            '77': 1.0,
            '88': 1.0,
            '99': 1.0,
            # Suited Aces
            'A2s': 0.5,
            'A3s': 1.0,
            'A4s': 1.0,
            'A5s': 0.5,
            # Suited broadways
            'KTs': 0.5,
            'KJs': 1.0,
            'KQs': 1.0,
            'QTs': 0.5,
            'QJs': 1.0,
            'JTs': 1.0,
            'ATs': 1.0,
            'AJs': 1.0,
            # Suited connectors
            'T9s': 1.0,
            '98s': 1.0,
            '87s': 1.0,
            '76s': 0.5,
            # Offsuit
            'AQo': 0.5,
        },
    },
```

The CALL alias block (the 4 lines after the dict closing `}`) remains unchanged:
```python
CALL['BB']['vs_MP'] = CALL['BB']['vs_HJ']
CALL['BB']['vs_EP'] = CALL['BB']['vs_UTG']
CALL['BTN']['vs_MP'] = CALL['BTN']['vs_HJ']
CALL['BTN']['vs_EP'] = CALL['BTN']['vs_UTG']
# SB, CO, HJ: 3-bet-or-fold. No CALL entries.
```

**Verification grep:**
```
grep -c "'76s': 1.0" river-rats-core/range_manager.py
```
Expected: at least 1 in the CALL BTN vs_CO block

```
grep -c "'TT': 0.5" river-rats-core/range_manager.py
```
Expected: count includes the new CALL['BTN']['vs_CO'] and CALL['BTN']['vs_HJ'] entries

---

### EDIT 5 — range_manager.py: Add legacy dead-code comment above DEFEND

**Lines:** Find the DEFEND section header comment block beginning at line 741.

After `DEFEND['CO']['vs_EP'] = DEFEND['CO']['vs_UTG']` (current line 900), or alternatively
at the top of the DEFEND section comment block, add:

```python
# NOTE: DEFEND is legacy dead code. get_defend_range() builds its result dynamically
# from get_3bet_range() + get_call_range() and never reads this dict. Do not remove
# yet (unknown external consumers). Scheduled for cleanup in a separate task.
```

Insert this comment directly before the line:
```python
# =============================================================================
# DEFEND RANGES (vs Open) - Legacy Combined Ranges
# =============================================================================
```

**Verification grep:**
```
grep -c "legacy dead code" river-rats-core/range_manager.py
```
Expected: 1

---

### EDIT 6 — tests/test_preflop_engine.py: Replace 3 SB squeeze CALL tests

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_preflop_engine.py`

**Lines to delete:**
- `test_jts_sb_calls_squeeze_vs_co`: lines 255–260
- `test_small_pair_calls_via_implied_odds`: lines 267–271
- `test_kts_sb_calls_squeeze_vs_co`: lines 278–281

These three tests sit inside the `TestSqueeze` class. The surrounding tests that must be
kept are:
- Line 249: `test_aks_sb_squeezes_vs_co` — keep
- Line 262: `test_72o_sb_folds_squeeze` — keep
- Line 273: `test_98s_bb_calls_squeeze_vs_co` — keep
- Line 283: `test_small_pair_folds_vs_tight_opener` — keep

**Replacement:** Delete the three tests and add a new class `TestSBIs3BetOrFold` after the
`TestSqueeze` class ends (after line 287 in the current file, before the `TestBBOption` class
at line 291).

Add the following new class in that gap:

```python
# ---------------------------------------------------------------------------
# 4b. SB 3-bet-or-fold policy
# ---------------------------------------------------------------------------

class TestSBIs3BetOrFold:
    def test_jts_sb_folds_vs_co_open(self, rm):
        """
        JTs from SB facing CO open — SB has no CALL range.
        JTs is not in THREE_BET['SB']['vs_CO'] at any meaningful freq.
        Expect FOLD.
        """
        d = decide_preflop('JTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'
        assert d.scenario == 'squeeze'

    def test_kts_sb_folds_vs_co_open(self, rm):
        """
        KTs from SB facing CO open — not in SB 3-bet range, should FOLD.
        """
        d = decide_preflop('KTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'

    def test_small_pair_btn_calls_via_implied_odds_vs_utg(self, rm):
        """
        44 from BTN vs UTG open — BTN has a CALL range.
        44 is in CALL['BTN']['vs_UTG'] at 1.0.
        Implied odds path in engine also fires for BTN (non-SB, non-tight opener check differs).
        Expect CALL.
        (Replaces test_small_pair_calls_via_implied_odds which wrongly used SB hero.)
        """
        d = decide_preflop('44', 'BTN', 'defend_call', 'UTG', 4.0, 1.5, rm)
        assert d.action == 'CALL'
        assert d.scenario == 'defend_call'
```

**Precise surgery on TestSqueeze class:** Replace the three target test methods in-place,
leaving the surrounding methods intact. The cleanest approach:

Replace this block (lines 255–281, three methods):

```python
    def test_jts_sb_calls_squeeze_vs_co(self, rm):
        """JTs from SB vs CO open — in CALL['SB']['vs_CO'] at 0.5, should CALL."""
        d = decide_preflop('JTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'CALL'
        assert 0 < d.range_frequency <= 1.0
        assert d.scenario == 'squeeze'

    def test_72o_sb_folds_squeeze(self, rm):
        """72o from SB — not in any range, folds."""
        d = decide_preflop('72o', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'

    def test_small_pair_calls_via_implied_odds(self, rm):
        """44 from SB vs BTN open — not in CALL/THREEB but implied odds override fires."""
        d = decide_preflop('44', 'SB', 'squeeze', 'BTN', 75.0, 25.0, rm)
        assert d.action == 'CALL'
        assert d.range_frequency == 0.45  # Fixed implied-odds confidence

    def test_98s_bb_calls_squeeze_vs_co(self, rm):
        """98s from BB vs CO open with caller — in CALL['BB']['vs_CO'], should CALL."""
        d = decide_preflop('98s', 'BB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'CALL'

    def test_kts_sb_calls_squeeze_vs_co(self, rm):
        """KTs from SB vs CO — in CALL['SB']['vs_CO'] at 0.5."""
        d = decide_preflop('KTs', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'CALL'
```

With this block (removes the 3 SB CALL tests, keeps the 2 correct ones):

```python
    def test_72o_sb_folds_squeeze(self, rm):
        """72o from SB — not in any range, folds."""
        d = decide_preflop('72o', 'SB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'FOLD'

    def test_98s_bb_calls_squeeze_vs_co(self, rm):
        """98s from BB vs CO open with caller — in CALL['BB']['vs_CO'], should CALL."""
        d = decide_preflop('98s', 'BB', 'squeeze', 'CO', 75.0, 25.0, rm)
        assert d.action == 'CALL'
```

**Verification grep:**
```
grep -c "test_jts_sb_calls_squeeze_vs_co" river-rats-core/tests/test_preflop_engine.py
```
Expected: 0

```
grep -c "test_kts_sb_calls_squeeze_vs_co" river-rats-core/tests/test_preflop_engine.py
```
Expected: 0

```
grep -c "test_small_pair_calls_via_implied_odds" river-rats-core/tests/test_preflop_engine.py
```
Expected: 0

```
grep -c "test_jts_sb_folds_vs_co_open" river-rats-core/tests/test_preflop_engine.py
```
Expected: 1

```
grep -c "test_small_pair_btn_calls_via_implied_odds_vs_utg" river-rats-core/tests/test_preflop_engine.py
```
Expected: 1

---

### EDIT 7 — tests/test_range_manager_preflop.py: Fix CALL_VS_OPEN import and usages

**File:** `/home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_range_manager_preflop.py`

#### Step 7a — Replace the import line (line 18)

**Old content:**
```python
from range_manager import (
    RFI, THREE_BET, CALL_VS_OPEN, CALL_VS_3BET, FOURBET,
    RangeManager,
)
```

**New content:**
```python
from range_manager import (
    RFI, THREE_BET, CALL, CALL_VS_3BET, FOURBET,
    RangeManager,
)
CALL_VS_OPEN = CALL  # backward-compat alias for test assertions
```

#### Step 7b — Global replace of remaining CALL_VS_OPEN references in test bodies

There are 13 remaining occurrences of `CALL_VS_OPEN` in the test file (after the import line)
at lines 77, 81, 82, 85, 89, 91, 95, 102, 103, 111, 318, and the docstring lines 6 and 67.

The alias `CALL_VS_OPEN = CALL` added in step 7a means all runtime references will resolve
correctly without any further changes to test bodies. The docstring references on lines 6 and 67
are comments — no runtime impact. No further edits required beyond step 7a.

If the programmer prefers a clean file with no alias, they may optionally do a global
find-replace of `CALL_VS_OPEN` → `CALL` throughout the file and remove the alias line.
This is cleaner but not required for the tests to pass.

**Verification grep:**
```
python3 -c "from range_manager import RFI, THREE_BET, CALL, CALL_VS_3BET, FOURBET, RangeManager; print('import ok')"
```
Expected: "import ok" (run from `river-rats-core/` directory)

```
python3 -m pytest river-rats-core/tests/test_range_manager_preflop.py --collect-only -q 2>&1 | head -5
```
Expected: no `ImportError` on collection

---

## 3. Test Plan

### Step 1 — test_preflop_engine.py in isolation
```
python3 -m pytest river-rats-core/tests/test_preflop_engine.py -q
```
Expected: all green. The 3 deleted SB CALL tests are gone; the 3 new tests pass.
Tests that now pass that previously failed: `test_66_utg_is_mixed`, `test_55_utg_low_freq_raises_mixed`
(both depend on new RFI mixed frequencies).

### Step 2 — test_range_manager_preflop.py collection
```
python3 -m pytest river-rats-core/tests/test_range_manager_preflop.py -q
```
Expected: no `ImportError` on collection. The file previously failed at collection due to
`ImportError: cannot import name 'CALL_VS_OPEN'`. That error is resolved by Edit 7.
Some tests in this file may still fail for pre-existing reasons unrelated to Phase B — that
is acceptable.

### Step 3 — Full suite minus known-broken files
```
python3 -m pytest river-rats-core/tests/ \
  --ignore=river-rats-core/tests/test_explain_hand.py \
  --ignore=river-rats-core/tests/test_oracle_shap.py \
  -q
```
Expected delta: 8 fewer failures vs pre-Phase-B baseline.
- 3 deleted SB CALL tests (previously failing): removed
- 2 previously failing UTG mixed-freq tests: now passing
- 1 collection error in test_range_manager_preflop.py: resolved
- 1 `test_broadway_board_has_high_tp_plus`: passes (wider ranges → higher TP+ composition)
- 1 stale `get_3bet_range` shadowing `get_defend_range` path: resolved by removing duplicate

### Step 4 — Targeted composition test
```
python3 -m pytest river-rats-core/tests/test_range_features.py::test_broadway_board_has_high_tp_plus -v
```
Expected: PASS

### Step 5 — Multiway features test (monitor only)
```
python3 -m pytest river-rats-core/tests/test_multiway_features.py::test_hu_with_opener_pos_unchanged -v
```
Expected: uncertain. Pass/fail depends on whether the range delta flows into composition
features in a way that shifts HU vs multiway distinguishability. Flag result either way —
do not treat a failure here as a blocker for Phase B.

---

## 4. Rollback Plan

Before starting any edits, capture the current HEAD:
```
git -C /home/rupertbeytell/river-rats-v2 rev-parse HEAD
```
Save that hash. If any edit produces an unexpected result and the programmer cannot
diagnose within 10 minutes, run:
```
git -C /home/rupertbeytell/river-rats-v2 checkout -- river-rats-core/range_manager.py
git -C /home/rupertbeytell/river-rats-v2 checkout -- river-rats-core/tests/test_preflop_engine.py
git -C /home/rupertbeytell/river-rats-v2 checkout -- river-rats-core/tests/test_range_manager_preflop.py
```
This restores all three files to the last committed state without disturbing anything else.

If edits were committed incrementally, use:
```
git -C /home/rupertbeytell/river-rats-v2 reset --hard <saved-hash>
```

---

## 5. Stop Conditions

Per PROCESS_GUIDE.md protocol, the programmer STOPS and reports BLOCKED if:

- Any grep verification check returns the wrong count
- `def get_3bet_range` appears more than once after Edit 3b
- `THREEB[` appears anywhere after Edit 3a
- The import in test_range_manager_preflop.py still raises ImportError after Edit 7
- `test_preflop_engine.py` produces any new failure (not a pre-existing one)
- Line numbers differ from those specified here when the programmer opens the file
  (indicates an intermediate edit was applied; re-read the file and adjust)
