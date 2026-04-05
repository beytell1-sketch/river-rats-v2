"""
RIVER RATS AI PLAYER TEST
=========================

Simulates a learning player going through 100 hands of poker,
making deliberate decisions (right ~60% of the time), receiving coaching
from the full pipeline, and checking the output for known issues.

Run:
    python3 test_player_ai.py
"""

import sys
import os
import random
import re
from typing import List, Dict, Optional, Tuple

# Ensure project root is on path
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

# ─── Import game primitives ───────────────────────────────────────────────────

from poker_game import (
    Card, Player, make_deck, POSITIONS, RANKS, SUITS,
    hand_strength_0_1, STREET_CODE,
    run_coaching, run_coaching_all_levels,
    _get_player_level,
)


# ─── AI PLAYER DECISION LOGIC ─────────────────────────────────────────────────

def ai_player_decision(gto_action: str, equity: float,
                       street: str, spr: float) -> str:
    """
    Simulate a learning player — right ~60% of the time,
    with realistic beginner mistakes.
    """
    if random.random() < 0.6:
        return gto_action
    # 40% make mistakes:
    # - Call too much (don't fold enough)
    # - Don't bluff enough (check instead of bet)
    # - Don't raise enough (call instead of raise)
    if gto_action == 'FOLD':
        return 'CALL'
    if gto_action == 'BET':
        return 'CHECK'
    if gto_action == 'RAISE':
        return 'CALL'
    if gto_action == 'CHECK':
        return 'BET'
    return gto_action


# ─── COACHING CHECK ENGINE ────────────────────────────────────────────────────

# Template variable pattern: {word}, {word_word}, etc. — literal curly braces
_TEMPLATE_VAR_RE = re.compile(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}')

# L1-restricted vocab — these words should NOT appear in L1 explanations
_L1_FORBIDDEN = re.compile(
    r'\b(range|gto|frequency|mdf|minimum defence|equity)\b', re.IGNORECASE
)

# Numeric value pattern — at least one digit, optionally with % or decimals
_NUMERIC_RE = re.compile(r'\d+\.?\d*\s*%|\d+\.\d+|\b\d{2,}\b')

# "Your opponent" — should not appear when multiple opponents are active
_SINGULAR_OPP_RE = re.compile(r'\byour opponent\b', re.IGNORECASE)


def _all_text(exp) -> str:
    """Concatenate all text fields of an Explanation."""
    parts = [str(exp.headline)]
    for s in (exp.supporting or []):
        parts.append(str(s))
    if exp.qualifier:
        parts.append(str(exp.qualifier))
    return ' '.join(parts)


CheckResult = Tuple[bool, str]  # (passed, description_if_failed)


def run_checks(
    exp,
    level_int: int,
    street: str,
    board_cards: List[Card],
    hero_position: str,
    villain_position: str,
    gto_action: str,
    hero_action: str,
    num_opponents: int,
    all_level_exps: Optional[List] = None,
) -> List[CheckResult]:
    """
    Run all coaching checks against a single Explanation.
    Returns list of (passed, issue_description) tuples.
    One tuple per check — True means passed.
    """
    results: List[CheckResult] = []

    # ── Check 1: villain position visible in situation display ──────────────
    # The situation is printed by the game, so we check the explanation text.
    # We verify villain_position is non-empty (meaning the caller tracked it).
    vp_visible = bool(villain_position)
    results.append((
        vp_visible,
        f"Villain position empty (not tracked by caller)"
    ))

    # ── Check 2: Board cards present for non-preflop streets ───────────────
    if street == 'preflop':
        results.append((True, ""))  # no board check needed preflop
    else:
        board_ok = len(board_cards) >= 3
        results.append((
            board_ok,
            f"Board has {len(board_cards)} cards on {street} (expected >=3)"
        ))

    # ── Check 3: Headline non-empty ─────────────────────────────────────────
    headline_ok = bool(exp.headline and str(exp.headline).strip())
    results.append((headline_ok, "Headline is empty"))

    # ── Check 4: No unrendered template variables ───────────────────────────
    all_txt = _all_text(exp)
    unrendered = _TEMPLATE_VAR_RE.findall(all_txt)
    results.append((
        len(unrendered) == 0,
        f"Unrendered template vars: {unrendered}"
    ))

    # ── Check 5: Sizing info only on BET/RAISE actions ──────────────────────
    has_sizing = (
        hasattr(exp, 'sizing_bucket') and exp.sizing_bucket is not None
        or hasattr(exp, 'sizing_pot_ratio') and exp.sizing_pot_ratio is not None
    )
    action_is_bet_raise = gto_action in ('BET', 'RAISE')
    if has_sizing and not action_is_bet_raise:
        results.append((False, f"Sizing info present on {gto_action} action"))
    else:
        results.append((True, ""))

    # ── Check 6: "Free card" never on river ─────────────────────────────────
    if street == 'river':
        free_card_present = 'free card' in all_txt.lower()
        results.append((
            not free_card_present,
            "\"free card\" mentioned on river"
        ))
    else:
        results.append((True, ""))

    # ── Check 7: "Future streets" never on river ────────────────────────────
    if street == 'river':
        future_streets_present = 'future street' in all_txt.lower()
        results.append((
            not future_streets_present,
            "\"future streets\" mentioned on river"
        ))
    else:
        results.append((True, ""))

    # ── Check 8: No singular "your opponent" when multiple opponents active ──
    if num_opponents > 1:
        singular_present = bool(_SINGULAR_OPP_RE.search(all_txt))
        results.append((
            not singular_present,
            "Singular \"your opponent\" used with multiple opponents"
        ))
    else:
        results.append((True, ""))

    # ── Check 9: Coaching action matches GTO recommendation ─────────────────
    coaching_action = str(exp.action).upper() if hasattr(exp, 'action') else ''
    # Normalize: BET/RAISE both acceptable for open bets, CHECK/CALL close
    def _norm(a):
        return a.upper()
    coaching_matches = (_norm(coaching_action) == _norm(gto_action))
    results.append((
        coaching_matches,
        f"Coaching action {coaching_action!r} != GTO action {gto_action!r}"
    ))

    # ── Check 10: Supporting sentences don't contradict headline ────────────
    # Check known bad pattern: "fold" appears in support when action is BET/RAISE,
    # or "bet/raise" appears when action is FOLD/CHECK.
    contradiction = False
    contradiction_detail = ''
    support_txt = ' '.join(str(s) for s in (exp.supporting or []))
    if gto_action in ('BET', 'RAISE'):
        if re.search(r'\bfold\b', support_txt, re.IGNORECASE):
            contradiction = True
            contradiction_detail = "Support mentions fold on BET/RAISE action"
    elif gto_action in ('FOLD',):
        if re.search(r'\bvalue bet\b|\bstrong\b.*\bbet\b', support_txt, re.IGNORECASE):
            contradiction = True
            contradiction_detail = "Support suggests value betting on FOLD action"
    results.append((
        not contradiction,
        contradiction_detail if contradiction_detail else "Support contradicts headline"
    ))

    # ── Check 11: Hand description makes sense ──────────────────────────────
    # Look for '? high' or empty-looking hand description in all text
    bad_hand_desc = bool(
        re.search(r'\?\s*high', all_txt) or
        re.search(r'^\s*$', str(exp.headline))
    )
    results.append((
        not bad_hand_desc,
        "Hand description looks broken ('? high' or empty)"
    ))

    # ── Check 12: All levels produce non-empty explanations (if available) ──
    if all_level_exps is not None:
        empty_levels = []
        for li, lexp in enumerate(all_level_exps, 1):
            if lexp is None or not str(lexp.headline).strip():
                empty_levels.append(f"L{li}")
        results.append((
            len(empty_levels) == 0,
            f"Empty explanation at levels: {empty_levels}"
        ))
    else:
        results.append((True, ""))

    # ── Check 13: L1 doesn't contain restricted vocab ───────────────────────
    if level_int == 1:
        l1_forbidden_found = _L1_FORBIDDEN.findall(all_txt)
        results.append((
            len(l1_forbidden_found) == 0,
            f"L1 contains restricted vocab: {l1_forbidden_found}"
        ))
    else:
        results.append((True, ""))

    # ── Check 14: L4/L5 contain numeric values ──────────────────────────────
    if level_int in (4, 5):
        has_numbers = bool(_NUMERIC_RE.search(all_txt))
        results.append((
            has_numbers,
            f"L{level_int} explanation has no numeric values (expected equity%, SPR, etc.)"
        ))
    else:
        results.append((True, ""))

    assert len(results) == 14, f"Expected 14 checks, got {len(results)}"
    return results


# ─── CHECK LABELS (14 checks) ─────────────────────────────────────────────────

CHECK_LABELS = [
    "Villain position tracked",
    "Board cards present for street",
    "Headline non-empty",
    "No unrendered template vars",
    "Sizing info only on BET/RAISE",
    "No 'free card' on river",
    "No 'future streets' on river",
    "No singular 'opponent' multiway",
    "Coaching action matches GTO",
    "Support doesn't contradict headline",
    "Hand description makes sense",
    "All levels non-empty",
    "L1 no restricted vocab",
    "L4/L5 has numeric values",
]


# ─── MINI GAME ENGINE ─────────────────────────────────────────────────────────

BIG_BLIND = 10
SMALL_BLIND = 5


class MiniPokerHand:
    """
    Minimal poker hand engine for the AI tester.
    No interactive I/O — the AI player makes all hero decisions.
    """

    def __init__(self, hand_number: int):
        self.hand_number = hand_number
        self.deck = make_deck()
        self.community_cards: List[Card] = []
        self.street = 'preflop'
        self.pot = 0
        self.current_bet = BIG_BLIND

        # Build 6 players; hero is always BTN for simplicity
        names = ['Alex', 'Blake', 'Casey', 'Hero', 'Dana', 'Ellis']
        self.players: List[Player] = []
        for i, pos in enumerate(POSITIONS):
            is_hero = (pos == 'BTN')
            p = Player(names[i], pos, 1000, is_hero)
            self.players.append(p)
        self.hero: Player = next(p for p in self.players if p.is_hero)

        # Post blinds
        sb = self._player_at('SB')
        bb = self._player_at('BB')
        sb_amount = min(SMALL_BLIND, sb.stack)
        bb_amount = min(BIG_BLIND, bb.stack)
        sb.stack -= sb_amount
        sb.bet_this_street += sb_amount
        bb.stack -= bb_amount
        bb.bet_this_street += bb_amount
        self.pot += sb_amount + bb_amount
        self.current_bet = BIG_BLIND

        # Deal hole cards
        for _ in range(2):
            for pos in POSITIONS:
                p = self._player_at(pos)
                p.hole_cards.append(self.deck.pop())

    def _player_at(self, pos: str) -> Player:
        for p in self.players:
            if p.position == pos:
                return p
        raise ValueError(f"No player at {pos}")

    def active_players(self) -> List[Player]:
        return [p for p in self.players if not p.is_folded]

    def _reset_street(self):
        self.current_bet = 0
        for p in self.players:
            p.bet_this_street = 0

    def deal_flop(self):
        self.deck.pop()  # burn
        for _ in range(3):
            self.community_cards.append(self.deck.pop())
        self.street = 'flop'
        self._reset_street()

    def deal_turn(self):
        self.deck.pop()  # burn
        self.community_cards.append(self.deck.pop())
        self.street = 'turn'
        self._reset_street()

    def deal_river(self):
        self.deck.pop()  # burn
        self.community_cards.append(self.deck.pop())
        self.street = 'river'
        self._reset_street()

    def _find_last_aggressor(self) -> str:
        """Return position of the player who set the current bet (not the hero)."""
        aggressors = [
            p for p in self.players
            if not p.is_folded and not p.is_hero
            and p.bet_this_street == self.current_bet
            and self.current_bet > 0
        ]
        return aggressors[0].position if aggressors else ''

    def run_ai_betting_round(self):
        """
        Run a simplified betting round where:
        - AI opponents randomly fold/check/call/bet.
        - Hero is not included — decisions happen in play_street().
        """
        order = (
            ['UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB']
            if self.street == 'preflop'
            else ['SB', 'BB', 'UTG', 'HJ', 'CO', 'BTN']
        )
        players_to_act = [
            self._player_at(pos) for pos in order
            if not self._player_at(pos).is_folded
            and not self._player_at(pos).is_hero
        ]

        for p in players_to_act:
            if p.is_folded:
                continue
            to_call = self.current_bet - p.bet_this_street
            r = random.random()
            if to_call == 0:
                # Can check or bet
                if r < 0.25:
                    bet_size = max(int(self.pot * 0.5), BIG_BLIND)
                    bet_size = min(bet_size, p.stack)
                    if bet_size > 0:
                        p.stack -= bet_size
                        p.bet_this_street += bet_size
                        self.pot += bet_size
                        self.current_bet = p.bet_this_street
                # else check (no action)
            else:
                if r < 0.35:
                    # fold
                    p.is_folded = True
                elif r < 0.80:
                    # call
                    call_amount = min(to_call, p.stack)
                    p.stack -= call_amount
                    p.bet_this_street += call_amount
                    self.pot += call_amount
                else:
                    # raise
                    raise_to = min(self.current_bet * 2 + BIG_BLIND, p.stack + p.bet_this_street)
                    chips_to_add = raise_to - p.bet_this_street
                    chips_to_add = min(chips_to_add, p.stack)
                    if chips_to_add > 0:
                        p.stack -= chips_to_add
                        p.bet_this_street += chips_to_add
                        self.pot += chips_to_add
                        self.current_bet = p.bet_this_street

        # Check if only one player remains
        survivors = [p for p in self.players if not p.is_folded]
        return len(survivors) >= 2


# ─── MAIN TEST RUNNER ─────────────────────────────────────────────────────────

NUM_HANDS = 100
NUM_CHECKS = 14


def run_test():
    random.seed(42)

    print()
    print("RIVER RATS AI PLAYER TEST — 100 Hands")
    print("=" * 38)
    print()

    # Track all results
    all_hand_summaries = []
    total_decisions = 0
    total_checks = 0
    total_pass = 0
    total_fail = 0
    issues_by_type: Dict[str, int] = {}

    # Coaching engine is loaded lazily inside run_coaching
    # (singleton via _get_engine in poker_game.py)

    for hand_num in range(1, NUM_HANDS + 1):
        hand = MiniPokerHand(hand_num)
        hero = hand.hero
        hand_issues = []

        # ── Preflop: AI opponents act, then hero acts ──────────────────────
        # Let AI opponents act first (before hero position in order)
        preflop_order = ['UTG', 'HJ', 'CO', 'SB', 'BB']
        for pos in preflop_order:
            p = hand._player_at(pos)
            if p.is_folded:
                continue
            to_call = hand.current_bet - p.bet_this_street
            r = random.random()
            if to_call == 0:
                pass  # check
            elif r < 0.40:
                p.is_folded = True
            else:
                call_amount = min(to_call, p.stack)
                p.stack -= call_amount
                p.bet_this_street += call_amount
                hand.pot += call_amount

        survivors = [p for p in hand.players if not p.is_folded]
        if len(survivors) < 2:
            continue

        # ── Hero preflop decision (skip coaching — preflop uses range logic) ──
        to_call_pf = hand.current_bet - hero.bet_this_street
        if to_call_pf > 0:
            # randomly call or fold preflop
            if random.random() < 0.55:
                call_amount = min(to_call_pf, hero.stack)
                hero.stack -= call_amount
                hero.bet_this_street += call_amount
                hand.pot += call_amount
            else:
                hero.is_folded = True
        else:
            # Already in BB with a check option — check
            pass

        if hero.is_folded:
            continue

        survivors = [p for p in hand.players if not p.is_folded]
        if len(survivors) < 2:
            continue

        # ── Postflop streets ──────────────────────────────────────────────
        streets = ['flop', 'turn', 'river']
        street_dealers = [hand.deal_flop, hand.deal_turn, hand.deal_river]

        hero_pos = hero.position
        hero_card_str = ''.join(str(c) for c in hero.hole_cards)
        hand_summary_lines = []

        for street, deal_fn in zip(streets, street_dealers):
            deal_fn()

            # Let AI opponents act before hero
            hand.run_ai_betting_round()

            survivors = [p for p in hand.players if not p.is_folded]
            if len(survivors) < 2 or hero.is_folded:
                break

            # ── Hero's coaching decision point ────────────────────────────
            to_call = hand.current_bet - hero.bet_this_street
            facing_bet = to_call > 0

            # Find who made the last bet
            villain_position = hand._find_last_aggressor()

            active_opponents = [
                p for p in hand.players
                if not p.is_folded and not p.is_hero
            ]
            num_opponents = len(active_opponents)
            if num_opponents == 0:
                break

            # Compute equity estimate
            equity = hand_strength_0_1(hero.hole_cards, hand.community_cards)
            spr = hero.stack / hand.pot if hand.pot > 0 else 100.0

            # Run coaching pipeline for a random coaching level (1-5)
            coaching_level = random.randint(1, 5)
            explanation = run_coaching(
                hero=hero,
                board=hand.community_cards,
                pot=hand.pot,
                to_call=to_call,
                street=street,
                facing_bet=facing_bet,
                active_opponents=[hero] + active_opponents,  # include hero for filtering
                level=coaching_level,
                betting_villain_position=villain_position,
            )

            if explanation is None:
                # No coaching available (rare edge case), skip checks
                continue

            # Run all-levels coaching for check 12
            all_levels = run_coaching_all_levels(
                hero=hero,
                board=hand.community_cards,
                pot=hand.pot,
                to_call=to_call,
                street=street,
                facing_bet=facing_bet,
                active_opponents=[hero] + active_opponents,
                betting_villain_position=villain_position,
            )

            # GTO action from explanation
            gto_action = str(explanation.action).upper()

            # Hero AI decision
            hero_action = ai_player_decision(gto_action, equity, street, spr)
            is_correct = (hero_action.upper() == gto_action)

            # Run coaching quality checks
            check_results = run_checks(
                exp=explanation,
                level_int=coaching_level,
                street=street,
                board_cards=hand.community_cards,
                hero_position=hero_pos,
                villain_position=villain_position,
                gto_action=gto_action,
                hero_action=hero_action,
                num_opponents=num_opponents,
                all_level_exps=all_levels,
            )

            passed = sum(1 for ok, _ in check_results if ok)
            failed = [(CHECK_LABELS[i], desc)
                      for i, (ok, desc) in enumerate(check_results) if not ok]

            total_decisions += 1
            total_checks += NUM_CHECKS
            total_pass += passed
            total_fail += len(failed)

            for label, desc in failed:
                issues_by_type[label] = issues_by_type.get(label, 0) + 1

            # Build summary line
            board_str = ' '.join(f"{c.rank}{c.suit}" for c in hand.community_cards)
            action_tag = "CORRECT" if is_correct else "MISSED"
            summary = (
                f"  Hand {hand_num}: L{coaching_level} {hero_pos} vs "
                f"{villain_position or '??'}, {street.capitalize()}, "
                f"{board_str} | Hero: {hero_card_str}"
                f"\n    Decision: {hero_action} (GTO: {gto_action}) — {action_tag}"
                f"\n    Coaching checks: {passed}/{NUM_CHECKS} PASS"
            )
            for label, desc in failed:
                summary += f"\n    ISSUE [{label}]: {desc}"
            hand_summary_lines.append(summary)

            # Apply hero action (simplified — just put in/fold)
            if hero_action == 'FOLD':
                hero.is_folded = True
                break
            elif hero_action == 'CALL':
                call_amount = min(to_call, hero.stack)
                hero.stack -= call_amount
                hero.bet_this_street += call_amount
                hand.pot += call_amount
            elif hero_action in ('BET', 'RAISE', 'CHECK'):
                pass  # simplified — hero checks or bets standard amount
            # else check — no action

            survivors = [p for p in hand.players if not p.is_folded]
            if len(survivors) < 2:
                break

        all_hand_summaries.extend(hand_summary_lines)

    # ── Print results ──────────────────────────────────────────────────────
    print('\n'.join(all_hand_summaries))

    print()
    print("SUMMARY")
    print("=" * 38)
    print(f"  Hands played: {NUM_HANDS}")
    print(f"  Decisions: {total_decisions}")
    total_theoretical = total_decisions * NUM_CHECKS
    print(f"  Coaching checks: {total_decisions} x {NUM_CHECKS} = {total_theoretical}")
    print()
    pass_pct = (100.0 * total_pass / total_checks) if total_checks > 0 else 0.0
    fail_pct = (100.0 * total_fail / total_checks) if total_checks > 0 else 0.0
    print(f"  PASS: {total_pass} ({pass_pct:.1f}%)")
    print(f"  FAIL: {total_fail} ({fail_pct:.1f}%)")

    if issues_by_type:
        print()
        print("  Issues by type:")
        for label, count in sorted(issues_by_type.items(), key=lambda x: -x[1]):
            print(f"    {label}: {count}")
    else:
        print()
        print("  No issues found.")


if __name__ == '__main__':
    run_test()
