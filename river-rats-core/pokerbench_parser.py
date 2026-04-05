"""
PokerBench â†’ Gauntlet Format Converter
=======================================

Parses the PokerBench CSV format and converts hands into the gauntlet
JSON format expected by feature_extractor.extract_all_features().

Only extracts hands where the correct action includes sizing (Bet/Raise),
since we're building a sizing prediction pilot.

PokerBench line format (CSV, with quoted available actions):
  idx, preflop, flop_cards, turn_card, river_card, first_actor,
  action_history, street, "available_actions", pot, hero_position,
  hero_cards, correct_action

Gauntlet hand format expected by feature_extractor:
  {
    'pos': hero_position,
    'fb': facing_bet (0 or 1),
    'pot': pot_size,
    'tc': to_call,
    'st': street_code ('f', 't', 'r'),
    'h': hero_hand_string,
    'b': board_string,
    'exp': expected_action ('F', 'X', 'C', 'B', 'R'),
    'vp': villain_position,
  }
"""

import re
import sys
from typing import Dict, List, Optional, Tuple


# Postflop acting order (same as feature_extractor.py)
POSTFLOP_ORDER = {
    'SB': 0, 'BB': 1, 'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3, 'CO': 4, 'BTN': 5,
}

STREET_CODE = {'Flop': 'f', 'Turn': 't', 'River': 'r'}


def parse_preflop(preflop_str: str) -> Tuple[str, str]:
    """
    Extract the two positions from preflop action string.

    Examples:
      "HJ/2.0bb/BB/call" â†’ ("HJ", "BB")
      "UTG/2.0bb/CO/6.5bb/UTG/call" â†’ ("UTG", "CO")
      "SB/3.0bb/BB/10.0bb/SB/call" â†’ ("SB", "BB")
      "CO/2.3bb/BB/call" â†’ ("CO", "BB")

    Returns:
        (opener_position, caller_position)
    """
    parts = preflop_str.split('/')
    # First part is always the opener position
    opener = parts[0].upper()

    # Find the second position (the one that's not the opener)
    # Walk through parts to find position names
    positions_found = []
    for p in parts:
        p_upper = p.upper()
        if p_upper in POSTFLOP_ORDER and p_upper not in positions_found:
            positions_found.append(p_upper)

    if len(positions_found) >= 2:
        return positions_found[0], positions_found[1]
    elif len(positions_found) == 1:
        # Fallback: assume BB as second position
        return positions_found[0], 'BB'
    else:
        return 'BTN', 'BB'  # safe fallback


def determine_hero_villain(
    pos1: str, pos2: str, hero_ip_str: str
) -> Tuple[str, str]:
    """
    Determine which position is hero and which is villain.

    Args:
        pos1, pos2: The two positions from preflop
        hero_ip_str: "IP" or "OOP" indicating hero's postflop position

    Returns:
        (hero_position, villain_position)
    """
    order1 = POSTFLOP_ORDER.get(pos1, 2)
    order2 = POSTFLOP_ORDER.get(pos2, 2)

    # Higher order = IP (acts later postflop)
    if order1 > order2:
        ip_pos, oop_pos = pos1, pos2
    else:
        ip_pos, oop_pos = pos2, pos1

    if hero_ip_str.upper() == 'IP':
        return ip_pos, oop_pos
    else:
        return oop_pos, ip_pos


def parse_to_call_from_history(
    action_history: str,
    hero_is_ip: bool,
) -> float:
    """
    Parse the action history to determine to_call for the final decision.

    The last action before hero's decision point tells us:
    - If it's opponent's BET or RAISE â†’ hero faces a bet
    - We need the size of that bet/raise

    Args:
        action_history: e.g. "OOP_CHECK/IP_BET_1/OOP_CALL/..."
        hero_is_ip: Whether hero is IP

    Returns:
        to_call amount (0 if not facing a bet)
    """
    hero_tag = "IP" if hero_is_ip else "OOP"
    villain_tag = "OOP" if hero_is_ip else "IP"

    actions = action_history.split('/')

    # Walk backward from the end to find the last villain action
    # (the action hero is responding to)
    for action in reversed(actions):
        action = action.strip()

        # Skip dealcards
        if action.startswith('dealcards'):
            continue

        # If the last non-deal action is villain's bet/raise, that's what hero faces
        if action.startswith(f'{villain_tag}_BET_'):
            size = float(action.split('_')[-1])
            return size
        elif action.startswith(f'{villain_tag}_RAISE_'):
            # RAISE_X means raise TO X total
            # to_call depends on what hero already has in
            # For simplicity: the raise amount IS the to_call
            # (PokerBench seems to use total raise sizing)
            size = float(action.split('_')[-1])
            return size
        elif action.startswith(f'{villain_tag}_CHECK'):
            return 0.0
        elif action.startswith(f'{villain_tag}_CALL'):
            return 0.0
        elif action.startswith(f'{hero_tag}_'):
            # We hit a hero action before finding villain's last action
            # This means hero is opening the action (no bet to face)
            return 0.0

    return 0.0


def extract_action_history_features(
    preflop: str,
    action_history: str,
    hero_is_ip: bool,
) -> Dict:
    """
    Derive structured features from preflop tree and action history.

    These features capture information that the original gauntlet format
    discards: pot type (single-raised vs 3-bet), and villain's multi-street
    aggression pattern.

    Args:
        preflop: Preflop action string, e.g. "HJ/2.0bb/BB/call"
                 or "CO/2.3bb/BTN/7.5bb/CO/call"
        action_history: Postflop history, e.g.
                 "OOP_CHECK/IP_BET_1/OOP_CALL/dealcards/5d/OOP_BET_9"
        hero_is_ip: Whether hero is the IP player

    Returns:
        Dict with:
            _is_3bet_pot: 1 if preflop 3-bet occurred, 0 otherwise
            _villain_aggression_count: int 0-3, streets villain bet or raised
            _villain_checked_back: 1 if villain checked any prior street, 0 otherwise
            _villain_call_count: int 0-3, streets villain flat-called
    """
    # â”€â”€ 3-bet detection â”€â”€
    # Count sizing actions (e.g. "2.0bb", "7.5bb") in preflop string.
    # Single-raised: 1 sizing ("HJ/2.0bb/BB/call")
    # 3-bet pot: 2+ sizings ("CO/2.3bb/BTN/7.5bb/CO/call")
    pf_parts = preflop.split('/')
    sizing_count = sum(
        1 for p in pf_parts if re.match(r'^\d+\.?\d*bb$', p)
    )
    is_3bet_pot = 1 if sizing_count >= 2 else 0

    # â”€â”€ Villain action history features â”€â”€
    villain_tag = "OOP" if hero_is_ip else "IP"

    actions = action_history.split('/')

    # Track per-street villain actions
    # Streets are delimited by "dealcards" entries
    current_street_v_bet = False
    current_street_v_check = False
    current_street_v_call = False

    streets_v_bet = 0       # streets where villain bet or raised
    streets_v_check = 0     # streets where villain checked
    streets_v_call = 0      # streets where villain flat-called

    for action in actions:
        action = action.strip()

        if action.startswith('dealcards'):
            # New street boundary â€” commit current street tallies
            if current_street_v_bet:
                streets_v_bet += 1
            if current_street_v_check:
                streets_v_check += 1
            if current_street_v_call:
                streets_v_call += 1
            # Reset for next street
            current_street_v_bet = False
            current_street_v_check = False
            current_street_v_call = False
            continue

        if not action.startswith(f'{villain_tag}_'):
            continue

        if '_BET_' in action or '_RAISE_' in action:
            current_street_v_bet = True
        elif action.endswith('_CHECK'):
            current_street_v_check = True
        elif action.endswith('_CALL'):
            current_street_v_call = True

    # Don't commit current street â€” that's the decision point street,
    # which is the action hero is responding to (already captured by facing_bet).
    # We only want PRIOR street behavior.

    return {
        '_is_3bet_pot': is_3bet_pot,
        '_villain_aggression_count': streets_v_bet,
        '_villain_checked_back': 1 if streets_v_check > 0 else 0,
        '_villain_call_count': streets_v_call,
    }


def build_board_string(
    flop_str: str, turn_str: str, river_str: str, street: str
) -> str:
    """Build board string appropriate for the current street."""
    if street == 'Flop':
        return flop_str
    elif street == 'Turn':
        return flop_str + turn_str
    elif street == 'River':
        return flop_str + turn_str + river_str
    return flop_str


def parse_pokerbench_line(line: str) -> Optional[Dict]:
    """
    Parse a single PokerBench line into a dict with all needed fields.

    Returns None if the line can't be parsed or correct action has no sizing.
    Returns dict with gauntlet-format fields plus sizing metadata.
    """
    line = line.strip()
    if not line:
        return None

    # Split carefully: available actions field is quoted and contains commas
    match = re.search(r'"(\[.*?\])"', line)
    if not match:
        return None

    # Everything before the quoted section
    before_quote = line[:match.start()].rstrip(',')
    # Everything after the quoted section
    after_quote = line[match.end():].lstrip(',').strip()

    before_parts = before_quote.split(',')
    after_parts = after_quote.split(',')

    if len(before_parts) < 8 or len(after_parts) < 4:
        return None

    try:
        idx = int(before_parts[0])
        preflop = before_parts[1]
        flop_cards = before_parts[2]
        turn_card = before_parts[3]
        river_card = before_parts[4]
        first_actor = before_parts[5]  # OOP or IP
        action_history = before_parts[6]
        street = before_parts[7]

        pot = float(after_parts[0])
        hero_ip_str = after_parts[1].strip()
        hero_cards = after_parts[2].strip()
        correct_action = after_parts[3].strip()

        # Parse available actions
        avail_str = match.group(1)
        avail_actions = re.findall(r"'([^']*)'", avail_str)

    except (ValueError, IndexError):
        return None

    # Parse correct action for sizing
    size_match = re.match(r'(Bet|Raise)\s+(\d+)', correct_action)
    if not size_match:
        # Not a sized action â€” we only want bet/raise for sizing pilot
        # But we'll return basic info for CHECK/CALL/FOLD too if needed
        action_type = correct_action  # "Check", "Call", "Fold"
        action_size = 0
    else:
        action_type = size_match.group(1)  # "Bet" or "Raise"
        action_size = float(size_match.group(2))

    # Determine positions
    pos1, pos2 = parse_preflop(preflop)
    hero_pos, villain_pos = determine_hero_villain(pos1, pos2, hero_ip_str)
    hero_is_ip = (hero_ip_str.upper() == 'IP')

    # Build board
    board_str = build_board_string(flop_cards, turn_card, river_card, street)

    # Determine facing_bet and to_call
    to_call = parse_to_call_from_history(action_history, hero_is_ip)
    facing_bet = 1 if to_call > 0 else 0

    # Map to gauntlet action code
    action_map = {
        'Fold': 'F', 'Check': 'X', 'Call': 'C',
        'Bet': 'B', 'Raise': 'R',
    }
    exp_code = action_map.get(action_type, 'X')

    # Street code
    st_code = STREET_CODE.get(street, 'f')

    # Pot ratio for sizing
    pot_ratio = action_size / pot if pot > 0 and action_size > 0 else 0.0

    # Count available sizing options
    n_sizing_options = 0
    for a in avail_actions:
        if re.match(r'(Bet|Raise)\s+\d+', a):
            n_sizing_options += 1

    # Extract action history features (is_3bet, villain aggression, etc.)
    history_features = extract_action_history_features(
        preflop, action_history, hero_is_ip,
    )

    return {
        # Gauntlet format fields
        'pos': hero_pos,
        'fb': facing_bet,
        'pot': pot,
        'tc': to_call,
        'st': st_code,
        'h': hero_cards,
        'b': board_str,
        'exp': exp_code,
        'vp': villain_pos,

        # Sizing metadata (not used by feature_extractor)
        '_pb_idx': idx,
        '_action_type': action_type,
        '_action_size': action_size,
        '_pot_ratio': round(pot_ratio, 4),
        '_street_name': street,
        '_hero_ip': hero_is_ip,
        '_n_sizing_options': n_sizing_options,
        '_avail_actions': avail_actions,
        '_correct_action_raw': correct_action,

        # Action history features (consumed by feature_extractor Phase 2)
        **history_features,
    }


def load_raise_hands(
    chunk_files: List[str],
    max_hands: int = None,
) -> List[Dict]:
    """
    Load and filter to RAISE hands from PokerBench chunks.

    Args:
        chunk_files: List of PokerBench chunk file paths
        max_hands: Optional cap on total hands returned

    Returns:
        List of parsed hand dicts (gauntlet format + sizing metadata)
    """
    raise_hands = []
    total_parsed = 0
    total_errors = 0

    for fpath in chunk_files:
        with open(fpath) as f:
            for line in f:
                result = parse_pokerbench_line(line)
                if result is None:
                    total_errors += 1
                    continue

                total_parsed += 1

                if result['_action_type'] == 'Raise':
                    raise_hands.append(result)

                if max_hands and len(raise_hands) >= max_hands:
                    break

        if max_hands and len(raise_hands) >= max_hands:
            break

    print(f"  Parsed {total_parsed} hands, {total_errors} errors")
    print(f"  Found {len(raise_hands)} RAISE hands")
    return raise_hands


def load_bet_hands(
    chunk_files: List[str],
    max_hands: int = None,
) -> List[Dict]:
    """Load and filter to BET hands."""
    bet_hands = []
    total_parsed = 0

    for fpath in chunk_files:
        with open(fpath) as f:
            for line in f:
                result = parse_pokerbench_line(line)
                if result is None:
                    continue
                total_parsed += 1
                if result['_action_type'] == 'Bet':
                    bet_hands.append(result)
                if max_hands and len(bet_hands) >= max_hands:
                    break
        if max_hands and len(bet_hands) >= max_hands:
            break

    print(f"  Parsed {total_parsed} hands, found {len(bet_hands)} BET hands")
    return bet_hands


def assign_raise_bucket(pot_ratio: float) -> str:
    """
    Assign a raise to SMALL / MEDIUM / STANDARD bucket.

    Boundaries (from data analysis):
      SMALL:    pot_ratio < 1.00  (~31% of raises)
      MEDIUM:   1.00 <= ratio < 1.40  (~47% of raises)
      STANDARD: ratio >= 1.40  (~21% â€” but 71% when solver has 2 options)
    """
    if pot_ratio < 1.00:
        return "SMALL"
    elif pot_ratio < 1.40:
        return "MEDIUM"
    else:
        return "STANDARD"


def assign_bet_bucket(pot_ratio: float) -> str:
    """
    Assign a bet to SMALL / STANDARD bucket.

    Boundaries (from data analysis):
      SMALL:    pot_ratio < 0.60  (~11% of bets)
      STANDARD: ratio >= 0.60  (~89%)
    """
    if pot_ratio < 0.60:
        return "SMALL"
    else:
        return "STANDARD"


if __name__ == '__main__':
    # Quick self-test
    test_line = '0,HJ/2.0bb/BB/call,JcJh4s,4d,As,OOP,OOP_CHECK/IP_BET_1/OOP_CALL/dealcards/4d/OOP_CHECK/IP_BET_8/OOP_CALL/dealcards/As/OOP_CHECK,River,"[\'Check\', \'Bet 17\']",21,IP,AhKd,Check'

    result = parse_pokerbench_line(test_line)
    if result:
        print("Parse test PASSED:")
        for k, v in result.items():
            if not k.startswith('_'):
                print(f"  {k}: {v}")
        print(f"  _action_type: {result['_action_type']}")
        print(f"  _pot_ratio: {result['_pot_ratio']}")
        print(f"  _is_3bet_pot: {result['_is_3bet_pot']}")
        print(f"  _villain_aggression_count: {result['_villain_aggression_count']}")
        print(f"  _villain_checked_back: {result['_villain_checked_back']}")
        print(f"  _villain_call_count: {result['_villain_call_count']}")
    else:
        print("Parse test FAILED")

    # Test a raise line (3-bet pot, villain double-barrel)
    test_raise = '15,CO/2.3bb/BB/call,Th3s2d,5d,Ks,OOP,OOP_CHECK/IP_CHECK/dealcards/5d/OOP_CHECK/IP_BET_6/OOP_CALL/dealcards/Ks/OOP_BET_9/IP_RAISE_32,River,"[\'Fold\', \'Call\', \'Raise 91\']",58,OOP,3h3c,Raise 91'

    result2 = parse_pokerbench_line(test_raise)
    if result2:
        print("\nRaise parse test:")
        print(f"  hero_pos: {result2['pos']}, villain_pos: {result2['vp']}")
        print(f"  facing_bet: {result2['fb']}, to_call: {result2['tc']}")
        print(f"  pot: {result2['pot']}, board: {result2['b']}")
        print(f"  hero_cards: {result2['h']}")
        print(f"  action: {result2['_action_type']} {result2['_action_size']}")
        print(f"  pot_ratio: {result2['_pot_ratio']}")
        print(f"  bucket: {assign_raise_bucket(result2['_pot_ratio'])}")
        print(f"  _is_3bet_pot: {result2['_is_3bet_pot']}")
        print(f"  _villain_aggression_count: {result2['_villain_aggression_count']}")
        print(f"  _villain_checked_back: {result2['_villain_checked_back']}")
        print(f"  _villain_call_count: {result2['_villain_call_count']}")

    # Test 3-bet pot detection
    test_3bet = '99,CO/2.3bb/BTN/7.5bb/CO/call,As8d2c,,,OOP,OOP_BET_5,Flop,"[\'Fold\', \'Call\', \'Raise 15\']",20,IP,KsQd,Call'
    result3 = parse_pokerbench_line(test_3bet)
    if result3:
        print(f"\n3-bet pot test: is_3bet={result3['_is_3bet_pot']} (expected 1)")
        assert result3['_is_3bet_pot'] == 1, "3-bet detection FAILED"
        print("  3-bet detection PASSED")

    # Test action history features
    print("\n--- Action history feature tests ---")

    # Test 1: Single-raised, villain checks flop then bets turn
    ah1 = extract_action_history_features(
        "HJ/2.0bb/BB/call",
        "OOP_CHECK/IP_CHECK/dealcards/5d/OOP_BET_6",
        hero_is_ip=True,
    )
    assert ah1['_is_3bet_pot'] == 0, f"Expected 0, got {ah1['_is_3bet_pot']}"
    assert ah1['_villain_aggression_count'] == 0, f"Expected 0 (flop only, villain checked), got {ah1['_villain_aggression_count']}"
    assert ah1['_villain_checked_back'] == 1, f"Expected 1 (villain checked flop), got {ah1['_villain_checked_back']}"
    assert ah1['_villain_call_count'] == 0
    print("  Test 1 (check-back detection) PASSED")

    # Test 2: 3-bet pot, villain double-barrels
    ah2 = extract_action_history_features(
        "CO/2.3bb/BTN/7.5bb/CO/call",
        "OOP_BET_5/IP_CALL/dealcards/6d/OOP_BET_12/IP_CALL/dealcards/Ks/OOP_BET_25",
        hero_is_ip=True,
    )
    assert ah2['_is_3bet_pot'] == 1
    assert ah2['_villain_aggression_count'] == 2, f"Expected 2 (villain bet flop+turn), got {ah2['_villain_aggression_count']}"
    assert ah2['_villain_checked_back'] == 0
    assert ah2['_villain_call_count'] == 0
    print("  Test 2 (3-bet + double-barrel) PASSED")

    # Test 3: Villain bets flop, checks turn, hero faces river decision
    ah3 = extract_action_history_features(
        "HJ/2.0bb/BB/call",
        "OOP_BET_3/IP_CALL/dealcards/7d/OOP_CHECK/IP_CHECK/dealcards/As/OOP_BET_10",
        hero_is_ip=True,
    )
    assert ah3['_villain_aggression_count'] == 1, f"Expected 1 (villain bet flop only), got {ah3['_villain_aggression_count']}"
    assert ah3['_villain_checked_back'] == 1, f"Expected 1 (villain checked turn)"
    assert ah3['_villain_call_count'] == 0
    print("  Test 3 (bet-then-check pattern) PASSED")

    # Test 4: Flop decision â€” no prior streets
    ah4 = extract_action_history_features(
        "SB/3.0bb/BB/call",
        "OOP_BET_4",
        hero_is_ip=True,
    )
    assert ah4['_villain_aggression_count'] == 0, "Flop decision should have 0 prior aggression"
    assert ah4['_villain_checked_back'] == 0
    assert ah4['_villain_call_count'] == 0
    print("  Test 4 (flop decision, no prior streets) PASSED")

    # Test 5: Villain calls on multiple streets (OOP checks then calls)
    ah5 = extract_action_history_features(
        "HJ/2.0bb/BB/call",
        "OOP_CHECK/IP_BET_3/OOP_CALL/dealcards/5d/OOP_CHECK/IP_BET_8/OOP_CALL/dealcards/As/OOP_CHECK",
        hero_is_ip=True,
    )
    assert ah5['_villain_aggression_count'] == 0, "Villain (OOP) never bet"
    assert ah5['_villain_checked_back'] == 1, "Villain checked on flop + turn (prior streets)"
    assert ah5['_villain_call_count'] == 2, f"Expected 2 (called flop + turn), got {ah5['_villain_call_count']}"
    print("  Test 5 (villain check-call pattern) PASSED")

    print("\nAll action history tests PASSED")
