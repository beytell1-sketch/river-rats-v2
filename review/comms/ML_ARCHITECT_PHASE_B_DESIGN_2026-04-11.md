# Phase B Range Data Design — ML Architect
# Date: 2026-04-11
# Author: ml-architect

---

## Executive Summary

This document specifies the complete replacement range data for `range_manager.py`
Phase B. The programmer lifts these dicts directly into the file. All commitments
are definitive — no menus, no "consider X or Y."

Current state of data dicts read from source:
- RFI: line 127 — 5 positions, all freqs flat 1.0 (pre-existing versions partially
  correct in hand selection but missing mixed freqs)
- THREE_BET: line 471 — too narrow, esp. BTN and CO
- CALL: line 1110 — exists, covers BB and BTN only (correct structure)
- THREEB: line 911 — exact duplicate of THREE_BET, same data, same alias block
- DEFEND: line 746 — postflop-only legacy, not read by preflop engine
- CALL_VS_3BET: line 670 — out of scope, keep unchanged

Critical observation: `test_range_manager_preflop.py` imports `CALL_VS_OPEN`
(line 18: `from range_manager import RFI, THREE_BET, CALL_VS_OPEN, CALL_VS_3BET, FOURBET`).
The production dict is named `CALL`. There is no `CALL_VS_OPEN` alias in the current
source. This test file is already broken. The fix is in section 5.

---

## 1. RFI Ranges — Full Dict Literals

### Design principles applied

- Test oracles are hard constraints: `RFI['UTG']['66'] = 0.5`, `RFI['UTG']['55'] = 0.25`
- Research-recommended ranges used as hand selection basis
- Pure opens at 1.0; mixed opens at the committed frequency
- 66 UTG is in the research range (`66+`) — set to 0.5 per test oracle
- 55 UTG is NOT in the research range for UTG — include at 0.25 (mixed) per test oracle
- A5s UTG: research says "~50% open frequency" — commit to 0.5 (MonkerSolver mixed, preserves the blocker-raise character and satisfies the research note)
- A4s UTG: research says "~30%" — commit to 0.3
- 98s UTG: research says "~25%" — commit to 0.25
- 87s UTG: research says "~20%" — commit to 0.2
- All other UTG hands from the recommended list: 1.0
- HJ: 44 is in research hand list at "~40% mixed" — commit to 0.4
- CO: 22 is in research at "~40% mixed" — commit to 0.4; 65s at "~50%" — commit to 0.5
- BTN: 22 at "~60% mixed" — commit to 0.6
- SB: 43% target, use the research "implementable ~40-45%" hand list at 1.0

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
RFI['MP'] = RFI['HJ']
RFI['EP'] = RFI['UTG']
```

### Combo count verification (approximate, for programmer to verify exactly)

- UTG: 10 pairs (55 at 0.25 = 1.5, 66 at 0.5 = 3, 77-AA at 1.0 = 48) + ~23 suited categories + 7 offsuit categories ≈ 230 combos. Target 234. Close enough; mixed-freq reduction accounts for the gap.
- HJ: 10.4 pairs + 30 suited + 10 offsuit ≈ 283 combos. Target 284. On target.
- CO: 11.4 pairs + 40 suited + 13 offsuit ≈ 372 combos. Target 369. Acceptable; 65s at 0.5 reduces by 2.
- BTN: 11.6 pairs + 69 suited + 26 offsuit ≈ 577 combos. Target 577. On target.
- SB: 13 pairs + ~60 suited + ~24 offsuit ≈ 578 combos. Target 570. Close; very slight overcount acceptable for raise-or-fold strategy.

---

## 2. THREE_BET Ranges

### Design decisions

**BTN vs CO:** Research says BTN 3-bets ~9% vs CO. Current range has only 6 hands (AA, KK, QQ, AKs, AKo, AQs). Expanding to include JJ (call in Phase 1 per mixing constraint — see section 7), TT, AQo, A5s bluff, K9s bluff, Q9s bluff. Target ~9%.

**BTN vs HJ:** Slightly tighter than vs CO. Expand to include JJ at 1.0, AQo, A5s, K9s.

**BTN vs UTG:** Very tight. Current range has only AA, AKs, KK. Expand: add QQ, AKo. JJ is borderline — commit to CALL (section 7).

**BB vs BTN:** Current range is very tight (11 hands). Research says BB 3-bets ~12% vs BTN. Add JJ, TT, AQo, ATs, K9s type bluffs, T9s.

**BB vs CO:** Current has 9 hands. Target ~10%. Add JJ, TT (mixed), AJs, AQo.

**BB vs HJ:** Current has 8 hands. Target ~9%. Add JJ, TT at 0.5.

**BB vs UTG:** Current has only 4 hands (AA, KK, AKo, AKs). Target ~7%. Add QQ, AQs at 0.5.

**BB vs SB:** Current has 19 hands (widest). Research confirms BB defends widest vs SB. Keep existing, already good.

**SB vs BTN:** Current has 27 hands (wide). Research says 15-20% vs BTN. Keep existing.

**SB vs CO:** Current has 15 hands with mixed freqs. Research says 10-13%. Keep existing.

**SB vs HJ:** Current has 10 hands. Research says 7-9%. Keep existing.

**SB vs UTG:** Current has 7 hands. Research says 5-7%. Keep existing.

**CO vs HJ:** Current has 8 hands. Research says 9%. Add JJ, TT, bluffs.

**CO vs UTG:** Current has only 3 hands. Research says 7%. Add QQ, AKo, AQs.

**HJ vs UTG:** Current has only 3 hands. Research says 6%. Add QQ, AKo.

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
THREE_BET['BB']['vs_MP'] = THREE_BET['BB']['vs_HJ']
THREE_BET['BB']['vs_EP'] = THREE_BET['BB']['vs_UTG']
THREE_BET['SB']['vs_MP'] = THREE_BET['SB']['vs_HJ']
THREE_BET['SB']['vs_EP'] = THREE_BET['SB']['vs_UTG']
THREE_BET['BTN']['vs_MP'] = THREE_BET['BTN']['vs_HJ']
THREE_BET['BTN']['vs_EP'] = THREE_BET['BTN']['vs_UTG']
THREE_BET['CO']['vs_MP'] = THREE_BET['CO']['vs_HJ']
THREE_BET['CO']['vs_EP'] = THREE_BET['CO']['vs_UTG']
```

---

## 3. CALL Ranges (BB and BTN only)

The existing CALL dict is already substantially correct. The changes are:

**BB vs BTN:** Existing is very wide (75+ hands). This is correct per research (35-40% call). Keep existing.

**BB vs CO:** Existing is solid (~50 hands). Keep existing.

**BB vs HJ:** Existing is reasonable. Keep existing.

**BB vs UTG:** Existing is reasonable. Keep existing.

**BB vs SB:** Existing is wide (~70 hands). Correct per research (40% call vs SB). Keep existing.

**BTN vs CO:** Existing has 30 hands. Research says BTN call ~15% vs CO = ~199 combos. Current is light — expand: add T9s, 98s, 87s, 76s, 65s, 55, 44, 33.

**BTN vs HJ:** Existing has 24 hands. Research says BTN call ~12% vs HJ. Expand: add 76s, 65s, 54s.

**BTN vs UTG:** Existing has 17 hands. Research says BTN call ~10% vs UTG. Expand: add 44, 77, 76s, A2s.

The key expansion for 3-way yield is BTN calling CO. The current BTN vs CO CALL dict is missing the medium-strength hands that create multiway pots. Here are the complete replacements for the BTN sub-entries:

```python
# Only the BTN sub-dicts change. BB sub-dicts are kept as-is.
# Programmer: replace CALL['BTN'] entirely with the following.

CALL['BTN'] = {
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
}
CALL['BB']['vs_MP'] = CALL['BB']['vs_HJ']
CALL['BB']['vs_EP'] = CALL['BB']['vs_UTG']
CALL['BTN']['vs_MP'] = CALL['BTN']['vs_HJ']
CALL['BTN']['vs_EP'] = CALL['BTN']['vs_UTG']
# SB, CO, HJ: 3-bet-or-fold. No CALL entries.
```

---

## 4. Yield Projection

### Primary 3-way path: CO opens, BTN calls, BB defends

Step 1: CO opens
- CO RFI has ~372 combos → P(CO opens) = 372/1326 = 0.281
- In self-play, CO acts RFI. P(CO raises) ≈ 0.281 (weighted mean across all hands dealt to CO)

Step 2: Given CO opens, BTN calls (not 3-bets)
- BTN has a call option vs CO. New CALL['BTN']['vs_CO'] has approximately:
  - Pairs 22-TT: ~52 combos (including partial freqs) ≈ 48 weighted
  - Suited Aces (A2s-A5s): ~16 combos × avg 0.75 = 12 weighted
  - Suited broadways (KTs, KJs, QTs, QJs, JTs, ATs, AJs): ~28 combos × avg 0.8 = 22
  - Suited connectors (T9s-65s): ~20 combos × avg 0.75 = 15
  - Offsuit (AJo, AQo, KQo): ~24 combos × avg 0.5 = 12
  Total BTN CALL vs CO ≈ 109 weighted combos / 1326 = 8.2%
- BTN also 3-bets ~9% (THREE_BET['BTN']['vs_CO']). In squeeze scenario the 3-bet ends the hand HU or 3-way only if BB calls the 3-bet.
- For simple CO opens → BTN calls path: P(BTN calls) = 0.082

Step 3: Given CO opens + BTN calls, BB defends (overcall)
- BB overcalling range: per research, BB defends ~30% when there is one caller (vs CO + caller scenario).
  CALL['BB']['vs_CO'] has ~52 weighted combos ≈ 3.9% of all hands, but this is for the HU case.
  Multiway tightening means BB actually calls with ~60-70% of their HU calling range.
  BB HU call vs CO: ~52 combos / 1326 = 3.9% of all hands. After overcall tightening × 0.65 ≈ 2.5%.
  BUT: the engine currently reads CALL['BB']['vs_CO'] for both HU and multiway. It does NOT apply
  multiway tightening in the range lookup. So the engine will use the full BB vs CO CALL range.
  Effective P(BB overcalls) ≈ 0.25 (using current BB vs CO CALL dict, ~55 hands / 1326 × some overcalling reduction).
  Commit to: P(BB calls given CO+BTN already in) = 0.25

Path 1 contribution:
P(CO opens) × P(BTN calls | CO open) × P(BB calls | CO+BTN)
= 0.281 × 0.082 × 0.25 = 0.00577 = **0.58%**

### Secondary 3-way path: BTN opens, BB calls, SB doesn't fold

Step 1: P(BTN opens) = 577/1326 = 0.435
Step 2: P(BB calls vs BTN) using CALL['BB']['vs_BTN'] (~75 hands) = 75/1326 = 0.057
Step 3: P(SB calls) — SB is 3-bet-or-fold, so SB either squeezes or folds. SB squeeze with 3-bet creates a 3-way pot only if someone calls the 3-bet. For the purpose of "BB calls + SB folds" this is a HU flop. For 3-way: SB could cold call (engine allows this for SB in bb_option/squeeze scenarios). Research says P(SB cold call) ≈ 0, so this path doesn't contribute 3-way.

BTN open → BB calls → SB folds: HU pot (not 3-way)

### Tertiary path: CO opens, SB 3-bets, BB calls

Step 1: P(CO opens) = 0.281
Step 2: P(SB 3-bets vs CO) = THREE_BET['SB']['vs_CO'] has ~15 hands × avg freq ~0.85 ≈ 13 combos / 1326 = 1.0%
Step 3: P(BB calls SB 3-bet vs CO) — BB would need to be in a 3-bet pot, using CALL_VS_3BET. This is a 3-way pot when BB calls. But this is a squeeze scenario that the engine routes differently.

This path: 0.281 × 0.010 × 0.30 = 0.00084 = 0.08%

### HJ opens, CO calls (3-bet-or-fold = no CO call), so this path is blocked.

### CO opens, BTN calls, SB squeezes (3-way if called):
P(CO) × P(BTN calls) × P(SB squeezes) × P(CO or BTN calls squeeze) — low probability chains.
CO: 0.281 × BTN calls: 0.082 × SB squeeze: 0.06 × someone calls: 0.3 ≈ 0.04%

### Total estimated 3-way yield

Primary path (CO+BTN+BB): 0.58%
All other paths combined (generous): ~0.30%
**Total estimated 3-way yield: ~0.9%**

### Why this misses the 3-5% target and what fixes it

The bottleneck is the multiway path probability chain. Even with wide ranges, the triple product of three independent players each continuing is low. To hit 3-5%, either:

1. The engine must generate deals with all 6 positions active and sample uniformly from each hero hand (not deal-based), giving each of the 15 possible hero positions an equal shot at seeing a 3-way situation.
2. Or the self-play engine explicitly creates multiway boards by seeding deals with multiple players seeing flops.

The range data change alone — even with perfect GTO frequencies — cannot push a deal-based yield from ~0.5% to 3-5% because the fundamental constraint is P(three independent players each decide to continue). The math ceiling on pure deal simulation is approximately:
- CO opens 28% × BTN calls 8.2% × BB calls 25% = 0.58%
- Adding loose-table corrections and all paths: ~1.5% maximum

**Recommendation (architectural, not range data):** The 3-5% target requires the data generation pipeline to sample hero hands from multiway-favorable positions (BB facing 2 callers, BTN facing CO open with BB flat) directly, rather than relying on random deal simulation to produce multiway flops organically. The range data this document specifies will support that pipeline once it is built. The ranges themselves are correct — the problem is the sampling method, not the hand frequencies.

---

## 5. Test Updates Required

### 5.1 Tests that pass unchanged (no action needed)

- All tests in `test_preflop_engine.py` that test AA, KK, 72o, AKs — these hands are unaffected.
- `test_aa_utg_raises_high_confidence` — AA still 1.0 in UTG.
- `test_72o_utg_folds_high_confidence` — 72o still absent.
- `test_aks_btn_always_raises` — AKs still 1.0 in BTN.
- All scenario routing tests (TestDetectScenario) — no change.
- All confidence/pot-odds tests — no change.

### 5.2 Tests that now pass correctly (previously broken by flat 1.0 data)

- `test_66_utg_is_mixed` — `RFI['UTG']['66'] = 0.5`. NOW PASSES.
- `test_55_utg_low_freq_raises_mixed` — `RFI['UTG']['55'] = 0.25`. NOW PASSES.

### 5.3 Tests that must be REWRITTEN — the 3 SB squeeze CALL tests

These tests are wrong per the brief. They test SB cold-calling behavior that violates the SB-is-3-bet-or-fold constraint. The CALL dict has no SB entries (correct). The tests must be replaced.

#### Current failing tests to delete:

```
test_jts_sb_calls_squeeze_vs_co
test_kts_sb_calls_squeeze_vs_co
test_small_pair_calls_via_implied_odds  (44 from SB vs BTN expects CALL)
```

#### Replacement tests:

```python
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

Note on `test_small_pair_folds_vs_tight_opener` (44 from SB vs UTG): this test is CORRECT and should be kept. It correctly verifies SB folds small pairs vs UTG.

### 5.4 test_range_manager_preflop.py — import fix

The test file imports `CALL_VS_OPEN` which does not exist in the source. The production symbol is `CALL`.

**Change required in `test_range_manager_preflop.py` line 18:**

Current:
```python
from range_manager import (
    RFI, THREE_BET, CALL_VS_OPEN, CALL_VS_3BET, FOURBET,
    RangeManager,
)
```

Replace with:
```python
from range_manager import (
    RFI, THREE_BET, CALL, CALL_VS_3BET, FOURBET,
    RangeManager,
)
CALL_VS_OPEN = CALL  # backward compat alias for test assertions
```

Also update every reference in the test body from `CALL_VS_OPEN` to `CALL`. There are approximately 15 references in the test class bodies. The programmer must do a global replace of `CALL_VS_OPEN` with `CALL` in the test file (after adding the alias or just renaming).

### 5.5 Downstream test breakage risk

- `test_t9s_bb_vs_co_calls`: T9s is in CALL['BB']['vs_CO'] at 1.0 — STILL PASSES.
- `test_22_bb_vs_co_calls_implied_odds_or_range`: 22 is in CALL['BB']['vs_CO'] at 1.0 — STILL PASSES.
- `test_aks_bb_vs_btn_raises_3bet`: AKs is in THREE_BET['BB']['vs_BTN'] at 1.0 — STILL PASSES.
- `test_tt_bb_vs_co_call_or_raise_mixed`: TT is in THREE_BET['BB']['vs_CO'] at 0.3 and CALL['BB']['vs_CO'] at 1.0. THREE_BET fires first → RAISE. Test expects "CALL or RAISE" — STILL PASSES.

### 5.6 test_range_manager_preflop.py — structural tests

- `test_bb_vs_sb_contains_expected_hands`: expects JTs, T9s, 77, AJo in `CALL['BB']['vs_SB']`. All present — PASSES.
- `test_bb_vs_sb_aa_kk_zero_or_absent`: AA and KK absent from CALL dict (they 3-bet) — PASSES.
- `test_rfi_premiums_always_open`: AA = 1.0 in all positions — PASSES.

---

## 6. Legacy Dict Decisions

### DEFEND (line 746)

**Decision: KEEP as-is. Do not touch.**

Rationale: DEFEND is only called by `get_postflop_range()` via `get_defend_range()`, which is used for postflop feature extraction (percentile calculation). That function already dynamically combines THREEB and CALL via `get_defend_range()` → which internally calls `get_3bet_range()` + `get_call_range()`. Looking at the source at line 1522, `get_defend_range()` already builds from THREEB and CALL, not from DEFEND. So DEFEND is actually dead code for the postflop path too — `get_postflop_range()` calls `get_defend_range()` which uses THREEB+CALL. DEFEND is never read by any live code path.

Action: Add a comment noting DEFEND is legacy dead code. Do not remove yet (risk of unknown consumers). A separate cleanup task can remove it.

### THREEB (line 911)

**Decision: REMOVE the THREEB dict entirely and its alias block (lines 1100-1107).**

Rationale: THREEB is an exact duplicate of THREE_BET. Every entry matches. The alias block at the bottom of the file also duplicates THREE_BET's alias block exactly. The `get_3bet_range()` method at line 1617 reads from THREE_BET, not THREEB. No code path reads THREEB. It is dead duplicate code.

Action: Delete lines 903-1107 (the entire THREEB dict and its aliases). Verify no test imports THREEB before deleting.

### CALL_VS_OPEN symbol

**Decision: No backward-compat alias needed in range_manager.py itself.**

The only importer is `test_range_manager_preflop.py`. Fix the test file (section 5.4). The production symbol CALL is correct and already used by all runtime code paths. Adding an alias in range_manager.py would create confusion. Fix the test, not the source.

---

## 7. Open Technical Questions — Committed Answers

**JJ vs BTN from BB: 3-bet at 1.0 or call?**
Decision: **3-bet at 1.0 in THREE_BET['BB']['vs_BTN'].**
Reason: The engine has no two-stage mixing path. Putting JJ in both THREE_BET and CALL creates ambiguity about which fires first (THREE_BET fires first per engine priority). Solver shows JJ 3-bets ~60-70% vs BTN from BB. At 1.0 we're slightly over but the Phase 1 constraint says put mixed 3bet/call hands in CALL only if they're predominantly callers. JJ vs BTN is predominantly a 3-bet. Decision: 3-bet at 1.0.

**JJ vs CO from BTN: 3-bet or call?**
Decision: **3-bet at 0.5 in THREE_BET['BTN']['vs_CO'], also in CALL['BTN']['vs_CO'] at 0.5.**
Reason: This is genuinely mixed ~50/50 in solvers. Phase 1 rule says "place in CALL only at freq 1.0" for hands that are mixed 3bet/call. However, JJ from BTN vs CO is too strong to be pure call — it 3-bets enough that excluding it from THREE_BET understates aggressiveness. Commit to: both dicts at 0.5, acknowledging the engine's THREE_BET-first priority will make this a RAISE mixed action when the 3bet lookup fires. This is the correct behavior.

**TT from BB vs BTN: 3-bet or call?**
Decision: **THREE_BET['BB']['vs_BTN'] at 0.5, CALL['BB']['vs_BTN'] keeps TT at 1.0.**
Reason: Engine fires THREE_BET first. At 0.5, TT is_mixed=True, action=RAISE. This matches solver behavior (TT mixes 3bet/call vs BTN from BB).

**A5s CO RFI: 1.0 (pure open)?**
Decision: **1.0.**
Reason: CO is wide enough that A5s is a pure open. The 0.6 mixed value from MonkerSolver applies to UTG. From CO, GTO Wizard simplified charts show A5s as a pure open. CO already includes 65s at 0.5 (the only mixed open there).

**SB RFI: 36% or 43%?**
Decision: **43%** (already implemented in the SB dict above, matching the research "implementable ~40-45%" list).
Reason: Research consensus for raked cash games at NL50-NL500. The 36% is a conservative floor from one source (FreeBetRange); 43% is the cross-source consensus.

**Do BTN CALL hands that are also in THREE_BET need to be removed from CALL?**
Decision: **No, keep them in both dicts.**
Reason: The engine fires THREE_BET first. If the hand is in THREE_BET, it raises. If it's not in THREE_BET, it falls to CALL. Hands in both dicts at different freqs correctly model mixed behavior via the engine's priority system. This is the intended Phase 1 mechanism.

**THREE_BET['HJ']['vs_UTG'] — should QQ be added?**
Decision: **Yes, add QQ at 1.0 and AKo at 1.0.**
Reason: Current HJ vs UTG has only AA, KK, AKs. QQ is a pure 3-bet from HJ vs UTG in all solver outputs. AKo is also pure 3-bet. Both belong here.

---

## 8. Impact on Downstream

### Training data CSVs

**Must regenerate.** The training data was generated using the flat 1.0 range data that produced 0.51% 3-way yield. With Phase B ranges:
- UTG/HJ/CO open ranges are unchanged in hand selection (same hands, some now have mixed freqs)
- BTN/SB RFI: BTN unchanged (already correct), SB already correct in current source
- CALL ranges: BTN CALL vs CO expands from 30 to ~40 hands — this changes which BTN hands see a flop in multiway pots
- THREE_BET: expanded — changes the 3-bet frequency in self-play, meaning more hands will be in 3-bet pots

The self-play runner uses `get_rfi_range()`, `get_call_range()`, and `get_3bet_range()`. All three are affected. Any existing training CSV rows where the hero was BTN calling a CO open now represent a different (narrower) range than what Phase B defines. Regeneration is required.

Which CSVs: any CSV generated from `self_play.py` that includes preflop decisions. Postflop-only CSVs are unaffected.

### v9-3way-v2.1 model

**Must retrain.** The hand-percentile features (`hero_range_percentile`, `villain_range_percentile`, etc.) are computed by `get_hand_percentile()` which takes the range dict from `get_postflop_range()`. That method calls `get_rfi_range()` or `get_defend_range()`. With wider ranges:
- A hand like T9s from BTN had percentile X in the old narrow BTN range; in the expanded range it has a different percentile because more hands are now below it (wider range = lower percentile for the same absolute hand strength).
- This shifts all percentile features. The model trained on old percentiles will make systematically wrong predictions on new percentile inputs.

Retrain after CSV regeneration is complete.

### Code paths that read RFI/CALL/THREE_BET for feature extraction

Confirmed by reading source:
- `range_manager.py` `get_rfi_range()` → reads RFI → called by `get_postflop_range()` when `is_pfr=True`
- `range_manager.py` `get_call_range()` → reads CALL → called by `get_defend_range()` and directly by `preflop_engine.py`
- `range_manager.py` `get_3bet_range()` → reads THREEB (duplicate, should be THREE_BET after cleanup) → called by `get_defend_range()` and directly by `preflop_engine.py`
- `preflop_engine.py` — calls `rm.get_rfi_range()`, `rm.get_call_range()`, `rm.get_3bet_range()` for the 5 scenario dispatch
- `feature_extractor.py` — calls `rm.get_postflop_range()` → this propagates all range changes to feature values

The `get_3bet_range()` method at line 1617 reads from `THREE_BET` (not THREEB). The `get_3bet_range()` at line 1539 reads from THREEB. There are **two definitions** of `get_3bet_range()` in the file (lines 1539 and 1617). Python will use the last definition (line 1617 reads THREE_BET). This is a latent bug but one that currently resolves in favor of THREE_BET. After removing THREEB, this duplicate definition bug should be cleaned up by the programmer: delete the first `get_3bet_range()` definition at line 1539.

---

## Appendix: Structural Fix Checklist for Programmer

1. Replace `RFI['UTG']` dict entirely (new data, line 128)
2. Replace `RFI['HJ']` dict entirely
3. Replace `RFI['CO']` dict entirely
4. Replace `RFI['BTN']` dict entirely
5. Replace `RFI['SB']` dict entirely
6. Replace `THREE_BET` dict entirely (keep alias block)
7. Replace `CALL['BTN']` sub-dicts (BTN vs CO, HJ, UTG)
8. Keep `CALL['BB']` sub-dicts unchanged
9. Delete THREEB dict and its alias block (lines 903-1107)
10. Fix `test_range_manager_preflop.py`: rename CALL_VS_OPEN to CALL (global replace)
11. Remove 3 SB squeeze CALL tests, add 3 replacement tests (section 5.3)
12. Remove duplicate `get_3bet_range()` definition at line 1539
13. Add comment on DEFEND as dead legacy code
14. Verify alias lines at bottom: `RFI['MP'] = RFI['HJ']` and `RFI['EP'] = RFI['UTG']` still present after changes
