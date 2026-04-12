#!/usr/bin/env python3
"""Hand sequence validator — enforces correct poker action ordering.

Validates that postflop action sequences follow Texas Hold'em rules:
1. Initiative round: players act in position order (SB→BB→...→BTN)
2. After a bet/raise: responses proceed clockwise from bettor
3. FOLD is only legal when facing a bet
4. CHECK is only legal when NOT facing a bet
5. Every active player must act — no skipping
6. Bet-and-call: hero can only see a prior call if the caller acts
   before hero in the clockwise-from-bettor order

Usage:
    from hand_sequence_validator import validate_hand, HandSpec, Action

    spec = HandSpec(
        positions=['BB', 'CO', 'BTN'],
        opener='CO',
        streets=[
            StreetSpec(
                name='flop',
                cards=['Ah', '6d', '2c'],
                actions=[
                    Action('BB', 'check'),
                    Action('CO', 'bet', 45),
                    Action('BTN', 'call', 45),
                    Action('BB', 'fold'),
                ],
                hero_pos='BB',
                hero_action_index=3,
            ),
        ],
    )
    errors = validate_hand(spec)
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
    else:
        print("VALID")
"""
from dataclasses import dataclass, field
from typing import List, Optional

# Fixed postflop position order (left of dealer first)
POSTFLOP_ORDER = {
    'SB': 0, 'BB': 1, 'UTG': 2, 'EP': 2,
    'HJ': 3, 'MP': 3, 'CO': 4, 'BTN': 5,
}


@dataclass
class Action:
    position: str
    action: str  # 'check', 'bet', 'call', 'raise', 'fold'
    amount: float = 0.0

    def is_aggressive(self):
        return self.action.lower() in ('bet', 'raise')

    def requires_bet(self):
        return self.action.lower() in ('call', 'raise', 'fold')

    def requires_no_bet(self):
        return self.action.lower() in ('check', 'bet')


@dataclass
class StreetSpec:
    name: str  # 'flop', 'turn', 'river'
    cards: List[str]
    actions: List[Action]
    hero_pos: str
    hero_action_index: int  # index into actions[] where hero decides


@dataclass
class HandSpec:
    positions: List[str]  # active positions in the pot
    opener: str  # preflop opener position
    hero_cards: List[str] = field(default_factory=list)
    streets: List[StreetSpec] = field(default_factory=list)


def _clockwise_order(active_positions: List[str]) -> List[str]:
    """Sort positions in postflop order (SB first, BTN last)."""
    return sorted(active_positions, key=lambda p: POSTFLOP_ORDER.get(p.upper(), 99))


def _next_clockwise_from(bettor: str, active_positions: List[str]) -> List[str]:
    """Return active positions in clockwise order starting AFTER the bettor.

    Uses the table position numbers (POSTFLOP_ORDER) to determine
    clockwise order. The bettor need not be in active_positions.
    """
    bettor_order = POSTFLOP_ORDER.get(bettor.upper(), 99)
    positions_with_order = [
        (POSTFLOP_ORDER.get(p.upper(), 99), p)
        for p in active_positions
        if p.upper() != bettor.upper()
    ]

    # Split into positions AFTER bettor (higher order) and BEFORE (lower
    # order, wrapping around). Clockwise from bettor means: first the
    # seats with higher position numbers, then wrap to lower numbers.
    after = sorted([(o, p) for o, p in positions_with_order if o > bettor_order])
    before = sorted([(o, p) for o, p in positions_with_order if o <= bettor_order])

    return [p for _, p in after] + [p for _, p in before]


def validate_street(street: StreetSpec, active_positions: List[str]) -> List[str]:
    """Validate one street's action sequence. Returns list of errors."""
    errors = []
    street_name = street.name.upper()
    actions = street.actions
    hero_pos = street.hero_pos.upper()

    initiative_order = _clockwise_order(active_positions)
    active_set = set(p.upper() for p in active_positions)
    folded = set()

    bet_live = False
    current_bet_amount = 0.0
    bettor = None
    responded_to_bet = set()

    # Track who has acted in the initiative round (before any bet)
    initiative_acted = []

    # Expected position pointer for initiative round
    init_ptr = 0

    for i, act in enumerate(actions):
        pos = act.position.upper()
        action_lower = act.action.lower()

        # Check player is active and hasn't folded
        if pos not in active_set:
            errors.append(
                f"[{street_name}] Action {i+1}: {pos} is not in the pot "
                f"(active: {sorted(active_set)})"
            )
            continue

        if pos in folded:
            errors.append(
                f"[{street_name}] Action {i+1}: {pos} already folded but acts again"
            )
            continue

        if not bet_live:
            # Initiative round — must act in position order
            if init_ptr < len(initiative_order):
                expected_pos = initiative_order[init_ptr].upper()
                if pos != expected_pos:
                    # Check if expected player has already been skipped
                    errors.append(
                        f"[{street_name}] Action {i+1}: {pos} acts but "
                        f"{expected_pos} should act first (initiative order: "
                        f"{' → '.join(initiative_order)}). "
                        f"Every active player must act — no skipping."
                    )

            # Validate action type
            if action_lower in ('call', 'raise', 'fold'):
                errors.append(
                    f"[{street_name}] Action {i+1}: {pos} {action_lower}s "
                    f"but no bet is live. Legal actions: CHECK or BET only."
                )

            if action_lower == 'check':
                initiative_acted.append(pos)
                # Advance pointer past this position
                while init_ptr < len(initiative_order) and \
                      initiative_order[init_ptr].upper() in [p.upper() for p in initiative_acted]:
                    init_ptr += 1

            elif action_lower == 'bet':
                bet_live = True
                current_bet_amount = act.amount
                bettor = pos
                initiative_acted.append(pos)

        else:
            # Bet is live — must respond in clockwise-from-bettor order
            response_order = _next_clockwise_from(bettor,
                [p for p in active_positions if p.upper() not in folded
                 and p.upper() != bettor.upper()])

            # Check this player is next in response order
            expected_responders = [p for p in response_order
                                   if p.upper() not in responded_to_bet
                                   and p.upper() not in folded]
            if expected_responders:
                expected_next = expected_responders[0].upper()
                if pos != expected_next:
                    errors.append(
                        f"[{street_name}] Action {i+1}: {pos} responds to bet "
                        f"but {expected_next} should respond first (clockwise "
                        f"from {bettor}: {' → '.join(response_order)}). "
                        f"Already responded: {sorted(responded_to_bet)}."
                    )

            # Validate action type
            if action_lower in ('check', 'bet'):
                errors.append(
                    f"[{street_name}] Action {i+1}: {pos} {action_lower}s "
                    f"but a bet is live ({bettor} bet {current_bet_amount}). "
                    f"Legal actions: CALL, RAISE, or FOLD only."
                )

            if action_lower == 'fold':
                folded.add(pos)
            elif action_lower == 'raise':
                # Raise resets — new bettor, everyone must respond again
                responded_to_bet = {pos}
                bettor = pos
                current_bet_amount = act.amount
            else:
                responded_to_bet.add(pos)

    # Check hero's position in the sequence
    hero_idx = street.hero_action_index
    if hero_idx < len(actions):
        hero_act = actions[hero_idx]
        if hero_act.position.upper() != hero_pos:
            errors.append(
                f"[{street_name}] Hero action index {hero_idx} points to "
                f"{hero_act.position}, not hero ({hero_pos})"
            )

        # Check if hero is facing a bet
        if not bet_live and hero_idx > 0:
            # Check if any prior action was a bet
            prior_bet = any(a.is_aggressive() for a in actions[:hero_idx])
            if not prior_bet and hero_act.requires_bet():
                errors.append(
                    f"[{street_name}] Hero ({hero_pos}) {hero_act.action}s "
                    f"but no bet is live. Cannot fold/call/raise without a bet."
                )

    # Return remaining active positions (for next street)
    return errors


def validate_hand(spec: HandSpec) -> List[str]:
    """Validate an entire hand specification. Returns list of errors."""
    all_errors = []
    active = [p.upper() for p in spec.positions]

    # Check hero cards don't conflict with board
    hero_cards_upper = [c.lower() for c in spec.hero_cards]
    for street in spec.streets:
        board_cards = [c.lower() for c in street.cards]
        for hc in hero_cards_upper:
            if hc in board_cards:
                all_errors.append(
                    f"CARD CONFLICT: Hero card {hc} appears on "
                    f"{street.name} board {board_cards}"
                )

    for street in spec.streets:
        errors = validate_street(street, active)
        all_errors.extend(errors)

        # Remove folded players for next street
        for act in street.actions:
            if act.action.lower() == 'fold':
                pos = act.position.upper()
                if pos in active:
                    active.remove(pos)

    return all_errors


def validate_action_string(
    positions: List[str],
    street_name: str,
    action_string: str,
    hero_pos: str,
) -> List[str]:
    """Convenience: validate from a simple action string.

    action_string format: "BB check, CO bet 45, BTN call 45, BB fold"
    """
    actions = []
    hero_idx = None
    parts = [p.strip() for p in action_string.split(',')]

    for i, part in enumerate(parts):
        tokens = part.split()
        if len(tokens) < 2:
            return [f"Cannot parse action part: '{part}'"]

        pos = tokens[0].upper()
        act = tokens[1].lower()
        amount = float(tokens[2]) if len(tokens) > 2 else 0.0

        if '???' in part or 'HERO' in part.upper():
            hero_idx = i
            continue

        actions.append(Action(pos, act, amount))

    if hero_idx is None:
        hero_idx = len(actions)

    street = StreetSpec(
        name=street_name,
        cards=[],
        actions=actions,
        hero_pos=hero_pos,
        hero_action_index=hero_idx,
    )

    return validate_street(street, positions)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("=== Test 1: Valid sequence (BB checks, CO bets, BTN calls, BB folds) ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'flop',
        'BB check, CO bet 45, BTN call 45, BB fold',
        'BB'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 2: Invalid — BB folds without bet ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'turn',
        'BB fold, CO bet 60',
        'BTN'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 3: Invalid — BTN acts before CO after BB bets ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'flop',
        'BB bet 30, BTN call 30, CO fold',
        'CO'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 4: Invalid — CO skipped in initiative round ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'turn',
        'BB check, BTN bet 60',
        'BB'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 5: Valid bet-and-call (CO bets, BTN calls, BB last) ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'flop',
        'BB check, CO bet 30, BTN call 30, BB ???',
        'BB'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 6: Invalid bet-and-call (BTN bets, CO calls before BB) ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'flop',
        'BB check, CO check, BTN bet 30, CO call 30, BB ???',
        'BB'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")

    print("\n=== Test 7: Valid — BTN bets, BB responds first (sandwiched), CO last ===")
    errs = validate_action_string(
        ['BB', 'CO', 'BTN'], 'flop',
        'BB check, CO check, BTN bet 30, BB call 30, CO ???',
        'CO'
    )
    print(f"  Errors: {errs}" if errs else "  VALID")
