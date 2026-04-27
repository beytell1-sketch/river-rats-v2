"""Rule 11 boundary scenario specs.

Paired/2-tone boards, OOP made hand, villain_top_pair_plus_pct crossing 0.40.
5 boundary pairs with >= 3 distinct board textures per R5 correction.

Corrected per C1 (Pair 5: JsJd9c, not JsTd4d) and C2 (Pair 4: 9d6d3s, not 9h6h3h).

Blueprint Q2 Gap 7 / Q6 Rule 11 boundary scenarios.
"""
from __future__ import annotations

import sys
import os
from typing import List, Set, Tuple

_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)

from situation_factory import SituationSpec
from corpus_revision_scenarios._scenario_utils import (
    build_record_from_spec,
    fingerprint,
)

# Rule 11 boundary pairs per blueprint v3 Q2 table.
# Each pair has two variants: villain_top_pair_plus_pct above and below 0.40.
# We generate the OOP position (BB) with a medium-strong made hand.
#
# Board specs (C1 + C2 corrections applied):
#   Pair 1: KcKd4s (dry paired)
#   Pair 2: KdTd4c (2-tone paired)
#   Pair 3: 8h8d7c (dynamic paired, connected)
#   Pair 4: 9d6d3s (2-tone-flush, corrected per C2 — replaces 9h6h3h monotone)
#   Pair 5: JsJd9c (draw-heavy paired, corrected per C1 — replaces JsTd4d unpaired)

# For each boundary pair, we generate 2 records:
# - Below threshold (villain_tp+ = 0.30-0.38): CHECK expected (villain too air-heavy)
# - Above threshold (villain_tp+ = 0.42-0.50): BET expected (villain has enough value)
#
# We construct hero hands that are "medium-strong OOP" (top pair strong kicker, two pair)
# to make the threshold decision meaningful.

_RULE11_PAIRS: List[dict] = [
    # ─── Pair 1: Dry paired (KcKd4s) ───
    {
        'pair_id': 1,
        'board': ['Kc', 'Kd', '4s'],
        'texture': 'dry_paired',
        'hero_cards_below': ['Ah', '4d'],  # two pair (A kicker, no K)
        'hero_cards_above': ['Qh', 'Qs'],  # strong pair (QQ vs K-K board)
        'hero_pos': 'BB',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'pot': 18.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
        ],
    },

    # ─── Pair 2: 2-tone paired (KdTd4c) ───
    {
        'pair_id': 2,
        'board': ['Kd', 'Td', '4c'],
        'texture': 'two_tone_paired',
        'hero_cards_below': ['Th', '9s'],  # middle pair + kicker
        'hero_cards_above': ['Kh', 'Jc'],  # top pair strong kicker
        'hero_pos': 'BB',
        'villain_positions': ['BTN'],
        'opener_position': 'BTN',
        'pot': 17.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
        ],
    },

    # ─── Pair 3: Dynamic paired (8h8d7c) ───
    {
        'pair_id': 3,
        'board': ['8h', '8d', '7c'],
        'texture': 'dynamic_paired',
        'hero_cards_below': ['Jh', '7d'],  # bottom pair + J kicker
        'hero_cards_above': ['As', '8s'],  # trips (A kicker)
        'hero_pos': 'BB',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'pot': 17.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
        ],
    },

    # ─── Pair 4: 2-tone-flush (9d6d3s) — C2 correction ───
    {
        'pair_id': 4,
        'board': ['9d', '6d', '3s'],
        'texture': 'two_tone_flush',
        'hero_cards_below': ['Tc', '9s'],  # top pair (mediocre kicker)
        'hero_cards_above': ['9h', 'Ac'],  # top pair (A kicker)
        'hero_pos': 'BB',
        'villain_positions': ['BTN'],
        'opener_position': 'BTN',
        'pot': 17.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'BTN', 'raise'), ('preflop', 'BB', 'call'),
        ],
    },

    # ─── Pair 5: Draw-heavy paired (JsJd9c) — C1 correction ───
    {
        'pair_id': 5,
        'board': ['Js', 'Jd', '9c'],
        'texture': 'draw_heavy_paired',
        'hero_cards_below': ['Qh', '9h'],  # second pair (9)
        'hero_cards_above': ['Ah', 'Jh'],  # trips (A kicker)
        'hero_pos': 'BB',
        'villain_positions': ['CO'],
        'opener_position': 'CO',
        'pot': 17.0,
        'to_call': 0.0,
        'street': 'flop',
        'action_history': [
            ('preflop', 'CO', 'raise'), ('preflop', 'BB', 'call'),
        ],
    },
]


def generate_scenarios(forbidden_fingerprints: Set[Tuple[str, str]]) -> List[dict]:
    """Generate Rule 11 boundary scenario records.

    Produces 2 records per pair (below and above threshold), totaling 10 records
    across 5 board textures. Minimum 5 records (one per pair) if some are skipped.
    """
    records = []

    for pair in _RULE11_PAIRS:
        board = pair['board']
        board_str = ''.join(board)

        for variant, hero_cards in [
            ('below', pair['hero_cards_below']),
            ('above', pair['hero_cards_above']),
        ]:
            hero_cards_str = ''.join(hero_cards)

            fp = fingerprint(hero_cards_str, board_str)
            if fp in forbidden_fingerprints:
                continue

            spec = SituationSpec(
                hero_cards=hero_cards,
                board_cards=board,
                hero_pos=pair['hero_pos'],
                villain_positions=pair['villain_positions'],
                pot=pair['pot'],
                to_call=pair['to_call'],
                street=pair['street'],
                action_history=pair['action_history'],
                opener_position=pair.get('opener_position'),
            )

            sit_id = f"rule11_pair{pair['pair_id']}_{variant}"
            record = build_record_from_spec(spec, sit_id, 'rule11_boundary_scenarios')
            if record is None:
                continue

            records.append(record)
            forbidden_fingerprints.add(fp)

    return records
