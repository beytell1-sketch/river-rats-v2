"""New GTO preflop range data — Step 1 of the range fix.

Solver-derived ranges from 100+ sources. Replaces the existing
RFI, THREE_BET, and CALL dicts in range_manager.py.

IMPORTANT: Engine mixing behaviour (preflop_engine.py line 268):
The engine checks THREE_BET first. If threeb_freq > 0, it returns
RAISE at that frequency. The poker_game.py mixing then does:
  random.random() < freq → RAISE, else FOLD.
It does NOT fall through to CALL. So for a hand that GTO says is
"3-bet 50%, call 50%", we must put it in CALL at freq 1.0 and
NOT in THREE_BET — otherwise the engine folds the non-3-bet
fraction instead of calling it.

Rule: A hand appears in THREE_BET OR CALL, never both.
- Pure 3-bet hands (AA, KK, AKs at freq 1.0): THREE_BET only
- Mixed 3-bet/call hands (JJ at 0.5): CALL at freq 1.0 (always
  continues), and NOT in THREE_BET. The engine always calls,
  losing the 3-bet option. This is a Phase 2 fix — the engine
  needs a two-stage mixing path (3-bet X%, call Y%, fold Z%).
- Pure call hands (87s at freq 1.0): CALL only

This is a known compromise. The engine's mixing logic can't
express "3-bet some, call the rest" for a single hand. Phase 2
will fix the engine. Phase 1 ensures hands always CONTINUE at
the correct frequency, even if the 3-bet/call split is wrong.
"""

# ═══════════════════════════════════════════════════════════════
# HELPER: Expand hand notation to dict
# ═══════════════════════════════════════════════════════════════

RANKS = '23456789TJQKA'
RANK_ORDER = {r: i for i, r in enumerate(RANKS)}


def _expand(notation_str, default_freq=1.0):
    """Expand "66+, A3s+, KTo+" to {'66': freq, '77': freq, ...}"""
    result = {}
    parts = [p.strip() for p in notation_str.split(',')]
    for part in parts:
        if not part:
            continue

        # Check for explicit frequency: "55:0.5" means 55 at 50%
        freq = default_freq
        if ':' in part:
            part, freq_str = part.split(':')
            freq = float(freq_str)

        # Pair+ notation: "66+"
        if len(part) >= 3 and part[0] == part[1] and part.endswith('+'):
            base = RANK_ORDER[part[0]]
            for r in range(base, 13):
                result[RANKS[r] + RANKS[r]] = freq
        # Single pair: "22" or "33"
        elif len(part) == 2 and part[0] == part[1]:
            result[part] = freq
        # Suited+: "A3s+"
        elif part.endswith('s+'):
            high = part[0]
            low = part[1]
            for r in range(RANK_ORDER[low], RANK_ORDER[high]):
                result[high + RANKS[r] + 's'] = freq
        # Offsuit+: "ATo+"
        elif part.endswith('o+'):
            high = part[0]
            low = part[1]
            for r in range(RANK_ORDER[low], RANK_ORDER[high]):
                result[high + RANKS[r] + 'o'] = freq
        # Single suited: "T9s"
        elif part.endswith('s'):
            result[part] = freq
        # Single offsuit: "JTo"
        elif part.endswith('o'):
            result[part] = freq

    return result


def _count_combos(d):
    total = 0
    for hand, freq in d.items():
        if len(hand) == 2:
            total += 6 * freq
        elif hand.endswith('s'):
            total += 4 * freq
        elif hand.endswith('o'):
            total += 12 * freq
    return total


# ═══════════════════════════════════════════════════════════════
# RFI (OPEN RAISE) RANGES
# ═══════════════════════════════════════════════════════════════
# Source: preflop_rfi_ranges_research.md
# Solver consensus from PokerCoaching, Upswing, GTO Wizard

RFI = {
    # UTG: 17.0% (226 combos). Tight linear range.
    'UTG': _expand(
        '66+, A3s+, K8s+, Q9s+, J9s+, T9s, ATo+, KJo+, QJo'
    ),

    # HJ: 21.1% (280 combos). Slightly wider than UTG.
    'HJ': _expand(
        '55+, A2s+, K6s+, Q9s+, J9s+, T9s, 98s, 87s, 76s, '
        'ATo+, KTo+, QTo+'
    ),

    # CO: 27.8% (368 combos). Standard cutoff range.
    'CO': _expand(
        '33+, A2s+, K3s+, Q6s+, J8s+, T7s+, 97s+, 87s, 76s, '
        'A8o+, KTo+, QTo+, JTo'
    ),

    # BTN: 42.8% (568 combos). Wide button range.
    'BTN': _expand(
        '33+, A2s+, K2s+, Q3s+, J4s+, T6s+, 96s+, 85s+, 75s+, '
        '64s+, 53s+, A4o+, K8o+, Q9o+, J9o+, T8o+, 98o'
    ),

    # SB: 42.4% (562 combos). Raise-or-fold (no limps).
    'SB': _expand(
        '22+, A2s+, K2s+, Q4s+, J6s+, T6s+, 96s+, 86s+, 75s+, '
        '65s, 54s, A2o+, K7o+, Q9o+, J9o+, T9o'
    ),
}


# ═══════════════════════════════════════════════════════════════
# 3-BET RANGES
# ═══════════════════════════════════════════════════════════════
# Source: preflop_defend_ranges_research.md
# Polarized: premiums for value + suited blockers as bluffs

THREE_BET = {
    'BTN': {
        # BTN 3-bet vs CO: pure 3-bet hands only (mixed hands go to CALL)
        'vs_CO': _expand(
            'QQ+, AKs, AKo, AQs'
        ),
        # BTN 3-bet vs HJ
        'vs_HJ': _expand(
            'QQ+, AKs, AKo, AQs'
        ),
        # BTN 3-bet vs UTG
        'vs_UTG': _expand(
            'KK+, AKs'
        ),
    },

    'SB': {
        # SB 3-bet vs BTN: ~14% (3-bet or fold, no cold call)
        'vs_BTN': _expand(
            '99+, AQs+, AKo, AJs, ATs, '        # value (wider)
            'AQo, KQs, '                         # more value
            'A5s, A4s, A3s, A2s, '               # blocker bluffs
            'K9s, K8s, Q9s, J9s, T8s, 97s, 86s, 75s, 64s, 53s'  # suited bluffs (wider)
        ),
        # SB 3-bet vs CO: ~11%
        'vs_CO': _expand(
            'TT+, AQs+, AKo, '
            'AJs:0.5, AQo:0.5, '
            'A5s, A4s, A3s, '
            'K9s:0.5, Q9s:0.5, J9s:0.5'
        ),
        # SB 3-bet vs HJ: ~8%
        'vs_HJ': _expand(
            'JJ+, AKs, AKo, AQs, '
            'TT:0.5, AJs:0.5, '
            'A5s, A4s'
        ),
        # SB 3-bet vs UTG: ~6%
        'vs_UTG': _expand(
            'QQ+, AKs, AKo, '
            'JJ:0.5, AQs:0.5, '
            'A5s:0.5'
        ),
    },

    'BB': {
        # BB 3-bet vs BTN: pure 3-bet hands only
        'vs_BTN': _expand(
            'QQ+, AKs, AKo, AQs, AJs, '             # pure value
            'A5s, A4s, A3s, A2s'                      # blocker bluffs (always 3-bet)
        ),
        # BB 3-bet vs CO
        'vs_CO': _expand(
            'QQ+, AKs, AKo, AQs, '
            'A5s, A4s, A3s'
        ),
        # BB 3-bet vs HJ
        'vs_HJ': _expand(
            'QQ+, AKs, AKo, AQs, '
            'A5s, A4s'
        ),
        # BB 3-bet vs UTG
        'vs_UTG': _expand(
            'KK+, AKs, AKo'
        ),
        # BB 3-bet vs SB: wider (SB opens very wide)
        'vs_SB': _expand(
            'TT+, AQs+, AKo, AJs, ATs, '
            'A5s, A4s, A3s, A2s, '
            'K9s, Q9s, J9s, T8s, 97s'
        ),
    },

    # CO 3-bets vs HJ/UTG (3-bet or fold, no cold calling)
    'CO': {
        'vs_HJ': _expand(
            'QQ+, AKs, AKo, AQs, '
            'A5s, A4s'
        ),
        'vs_UTG': _expand(
            'KK+, AKs'
        ),
    },

    # HJ 3-bets vs UTG (3-bet or fold, no cold calling)
    'HJ': {
        'vs_UTG': _expand(
            'KK+, AKs'
        ),
    },
}


# ═══════════════════════════════════════════════════════════════
# CALL (COLD CALL / DEFEND CALL) RANGES
# ═══════════════════════════════════════════════════════════════
# Source: preflop_defend_ranges_research.md
# Only BTN and BB have significant calling ranges.
# SB, CO, HJ use 3-bet-or-fold.

CALL = {
    'BTN': {
        # BTN call vs CO: ~16%
        # JJ, TT are mixed 3-bet/call — put in CALL so they always continue
        'vs_CO': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, TT, JJ, '  # all pairs up to JJ
            'AJs, ATs, KQs, KJs, KTs, QJs, QTs, JTs, '  # suited broadways
            'T9s, 98s, 87s, 76s, 65s, 54s, '    # suited connectors
            'A5s, A4s, A3s, A2s, '              # suited wheel aces
            'AQo, AJo, KQo'                     # offsuit
        ),
        # BTN call vs HJ: ~13%
        'vs_HJ': _expand(
            '33, 44, 55, 66, 77, 88, 99, '
            'AJs, ATs, KQs, KJs, KTs, QJs, QTs, JTs, '
            'T9s, 98s, 87s, 76s, '
            'A5s, A4s, A3s, A2s, '
            'AQo, KQo'
        ),
        # BTN call vs UTG: ~10%
        'vs_UTG': _expand(
            '55, 66, 77, 88, 99, '
            'AJs, ATs, KQs, KJs, QJs, JTs, '
            'T9s, 98s, 87s, '
            'A4s, A3s, '
            'AQo'
        ),
    },

    'BB': {
        # BB call vs BTN: ~40% (very wide — solver says 44% total continue)
        # JJ, AJs are mixed 3-bet/call — in CALL so they always continue
        # A2s-A5s are pure 3-bet bluffs — NOT in CALL (in THREE_BET only)
        'vs_BTN': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, TT, JJ, '  # pairs up to JJ
            'A6s, A7s, A8s, A9s, ATs, '           # suited aces (A2-A5, AJs are 3-bet)
            'K2s, K3s, K4s, K5s, K6s, K7s, K8s, K9s, KTs, '  # suited kings
            'Q5s, Q6s, Q7s, Q8s, Q9s, QTs, '        # suited queens (wider)
            'J7s, J8s, J9s, JTs, '                   # suited jacks (wider)
            'T7s, T8s, T9s, '                        # suited tens
            '96s, 97s, 98s, '                        # suited nines
            '85s, 86s, 87s, '                        # suited eights
            '74s, 75s, 76s, '                        # suited sevens
            '63s, 64s, 65s, '                        # suited sixes
            '53s, 54s, '                             # suited fives
            '43s, '                                  # suited four
            'A2o, A3o, A4o, A5o, A6o, A7o, A8o, A9o, ATo, AJo, AQo, '  # all offsuit aces
            'K9o, KTo, KJo, KQo, '                   # offsuit kings (wider)
            'Q9o, QTo, QJo, '                        # offsuit queens
            'J9o, JTo, '                             # offsuit jacks
            'T9o, 98o, 87o, 76o, 65o'               # offsuit connectors
        ),

        # BB call vs CO: ~32% (research: 35-42% total, minus ~5% 3-bet = ~30% call)
        # A3s-A5s are pure 3-bet bluffs. JJ, TT, AJs mixed → CALL
        'vs_CO': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, TT, JJ, '
            'A2s, A6s, A7s, A8s, A9s, ATs, AJs, '
            'K5s, K6s, K7s, K8s, K9s, KTs, KQs, '   # wider suited kings
            'Q7s, Q8s, Q9s, QTs, QJs, '              # wider suited queens
            'J8s, J9s, JTs, '                        # suited jacks
            'T8s, T9s, '                             # suited tens
            '97s, 98s, '                             # suited nines
            '86s, 87s, '                             # suited eights
            '75s, 76s, '                             # suited sevens
            '64s, 65s, '                             # suited sixes
            '54s, '                                  # suited five
            'A5o, A6o, A7o, A8o, A9o, ATo, AJo, AQo, '  # wider offsuit aces
            'K9o, KTo, KJo, KQo, '                   # offsuit kings
            'Q9o, QTo, QJo, '                        # offsuit queens
            'J9o, JTo, '                             # offsuit jacks
            'T9o, 98o'                               # offsuit connectors
        ),

        # BB call vs HJ: ~25% (research: 28-35% total, minus ~4% 3-bet = ~24% call)
        # A4s-A5s are pure 3-bet bluffs. JJ mixed → CALL
        'vs_HJ': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, TT, JJ, '
            'A2s, A3s, A6s, A7s, A8s, A9s, ATs, AJs, '
            'K7s, K8s, K9s, KTs, KQs, '             # wider suited kings
            'Q8s, Q9s, QTs, QJs, '                   # wider suited queens
            'J9s, JTs, '                             # suited jacks
            'T9s, 98s, 87s, 76s, 65s, '             # suited connectors
            'A8o, A9o, ATo, AJo, AQo, '             # offsuit aces
            'KTo, KJo, KQo, '                        # offsuit kings
            'QJo, JTo'                               # offsuit broadways
        ),

        # BB call vs UTG: ~19% (research: 22-28% total, minus ~3% 3-bet = ~19% call)
        'vs_UTG': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, TT, '
            'A2s, A3s, A4s, A5s, A6s, A7s, A8s, A9s, ATs, '
            'K9s, KTs, KQs, '                        # suited kings
            'Q9s, QTs, QJs, '                        # suited queens
            'JTs, '
            'T9s, 98s, 87s, 76s, '                   # suited connectors
            'ATo, AJo, AQo, '                        # offsuit aces
            'KJo, KQo, '
            'QJo'
        ),

        # BB call vs SB: ~40% (widest defend — SB opens widest)
        # Hands in THREE_BET vs_SB (TT+, AQs+, AKo, AJs, ATs, A2s-A5s,
        # K9s, Q9s, J9s, T8s, 97s) are NOT in CALL.
        'vs_SB': _expand(
            '22, 33, 44, 55, 66, 77, 88, 99, '   # pairs (TT+ in 3-bet)
            'A6s, A7s, A8s, A9s, '                # suited aces (A2-A5, AT+ in 3-bet)
            'K2s, K3s, K4s, K5s, K6s, K7s, K8s, KTs, KQs, '  # suited kings (K9s in 3-bet)
            'Q5s, Q6s, Q7s, Q8s, QTs, QJs, '     # suited queens (Q9s in 3-bet)
            'J7s, J8s, JTs, '                     # suited jacks (J9s in 3-bet)
            'T7s, T9s, '                          # suited tens (T8s in 3-bet)
            '96s, 98s, '                          # suited nines (97s in 3-bet)
            '85s, 86s, 87s, '
            '74s, 75s, 76s, '
            '63s, 64s, 65s, '
            '53s, 54s, '
            '43s, '
            'A2o, A3o, A4o, A5o, A6o, A7o, A8o, A9o, ATo, AJo, AQo, '
            'K9o, KTo, KJo, KQo, '
            'Q9o, QTo, QJo, '
            'J9o, JTo, '
            'T9o, 98o, 87o, 76o'
        ),
    },

    # SB: NO CALL ENTRIES. SB is 3-bet-or-fold only.
    # CO vs HJ/UTG: NO CALL ENTRIES. 3-bet-or-fold only.
    # HJ vs UTG: NO CALL ENTRIES. 3-bet-or-fold only.
}


# ═══════════════════════════════════════════════════════════════
# VERIFICATION
# ═══════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 60)
    print("NEW RANGE DATA VERIFICATION")
    print("=" * 60)

    print("\nRFI Ranges:")
    for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB']:
        combos = _count_combos(RFI[pos])
        pct = 100 * combos / 1326
        print(f"  {pos}: {len(RFI[pos])} hands, {combos:.0f} combos, {pct:.1f}%")

    print("\n3-BET Ranges:")
    for pos in sorted(THREE_BET):
        for vs in sorted(THREE_BET[pos]):
            combos = _count_combos(THREE_BET[pos][vs])
            pct = 100 * combos / 1326
            print(f"  {pos} {vs}: {len(THREE_BET[pos][vs])} hands, {combos:.0f} combos, {pct:.1f}%")

    print("\nCALL Ranges:")
    for pos in sorted(CALL):
        for vs in sorted(CALL[pos]):
            combos = _count_combos(CALL[pos][vs])
            pct = 100 * combos / 1326
            print(f"  {pos} {vs}: {len(CALL[pos][vs])} hands, {combos:.0f} combos, {pct:.1f}%")

    print("\nTotal Continue (Call + 3-Bet):")
    for pos in ['BTN', 'BB']:
        for vs in sorted(CALL.get(pos, {})):
            call_combos = _count_combos(CALL[pos][vs])
            threeb_combos = _count_combos(THREE_BET.get(pos, {}).get(vs, {}))
            total = call_combos + threeb_combos
            pct = 100 * total / 1326
            print(f"  {pos} {vs}: call {call_combos:.0f} + 3bet {threeb_combos:.0f} = {total:.0f} combos ({pct:.1f}%)")

    print("\nSB (3-bet only, no calling):")
    for vs in sorted(THREE_BET.get('SB', {})):
        combos = _count_combos(THREE_BET['SB'][vs])
        pct = 100 * combos / 1326
        print(f"  SB {vs}: {combos:.0f} combos ({pct:.1f}%)")
