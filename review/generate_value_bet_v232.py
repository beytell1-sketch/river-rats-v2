"""generate_value_bet_v232.py — v2.3.2 Layer 2-mirror VALUE-BET counter-examples.

Mirror of review/generate_air_check_v231.py (ad806ba). Flips the hero-strength
selector from AIR to VALUE to add the balancing class per Path C directive
(MAIN_TERMINAL_DIRECTIVE_2026-04-18-o / 6022bb5) and answers
(MAIN_TERMINAL_TO_BUILDER_2026-04-18-p / 29dc412).

Predicate (flip of v2.3.1):
  facing_bet == 0
  villain_checked_back == 1
  num_opponents in {1, 2}
  is_made_hand == 1                # was 0 in v2.3.1
  equity_vs_range >= 0.55           # was <0.35 in v2.3.1

Litmus seeds (empirically probed for turn-card safety):
  AA on 7h5d2c + turn 3c   (eq=0.703, overpair preserved)
  KQ on KsTs3h + turn 2c   (eq=0.609, TPGK preserved)

Design identical to Layer 2: same board pool (monotone + paired + two-tone
+ dry), same archetypes, same turn-shift discipline (bridge vcb semantics
require prior-street checks), same output split (3-way labelled, HU for v2.4).

Outputs:
  training-data/v23_2_value_bet_3way.jsonl    (target 30-40 BP; labelling target)
  training-data/v23_2_value_bet_hu.jsonl      (opportunistic; v2.4 prep)

Run:
    python3 review/generate_value_bet_v232.py
"""
from __future__ import annotations

import sys
import os
import json
from typing import Callable, Dict, List, Tuple

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import (  # noqa: E402
    SituationSpec,
    build_situation,
    validate_situation,
    normalise_situation,
    _POSTFLOP_ORDER as _PFO,
)
from hand_evaluator import evaluate_hand  # noqa: E402


OUTPUT_DIR = os.path.join(_REPO, 'training-data')

STD_POT = 90.0
STD_STACK = 450.0


# =============================================================================
# Board templates — same pool as v2.3.1 (no narrowing; value hands anchor
# the boundary best with broad texture coverage per directive-o)
# =============================================================================
MONOTONE_BOARDS = [
    ['Qs', '5s', '7s'],
    ['Jh', '8h', '3h'],
    ['Kd', '9d', '4d'],
    ['Ac', '6c', '2c'],
]

PAIRED_BOARDS = [
    ['Jc', 'Jd', '2h'],
    ['9h', '9c', '4d'],
    ['Qs', 'Qd', '5c'],
    ['8c', '8d', '3s'],
    ['Kh', 'Ks', '7d'],
]

DRY_BOARDS = [
    ['Kh', '9d', '3c'],
    ['Kd', '7c', '2s'],
    ['Qh', '7d', '2c'],
    ['Qc', '8d', '3s'],
    ['Jd', '8c', '3s'],
    ['Jh', '7c', '2d'],
    ['Ah', '9d', '3c'],
    ['Ac', '7d', '2s'],
    ['Td', '6c', '2s'],
    ['9d', '5c', '2s'],
]

TWO_TONE_BOARDS = [
    ['Ts', '6s', '3d'],
    ['Qh', '8h', '4d'],
    ['Jc', '7c', '2d'],
    ['Kd', '8d', '4h'],
    ['Qs', '5d', '2h'],
]

# Round-robin textures for balanced coverage. Natural ordering (monotone
# first / dry first) creates asymmetric exhaustion of the `used` hero-card
# set — dry-board value hands are scarce (fewer category matches on
# K/Q/J-high rainbow), so visiting all dry first leaves no hero cards left
# for wet, and vice versa.
def _interleave(*lists):
    out = []
    longest = max(len(l) for l in lists)
    for i in range(longest):
        for lst in lists:
            if i < len(lst):
                out.append(lst[i])
    return out


FLOP_BOARDS_ALL = _interleave(
    DRY_BOARDS, PAIRED_BOARDS, MONOTONE_BOARDS, TWO_TONE_BOARDS,
)


# =============================================================================
# Hand category classification — VALUE class (flip of AIR)
# =============================================================================
# Matches generate_factory_batch6.py comment + directive-o scope:
#   monster      = straight_flush / quads / full_house / flush / straight /
#                  set / trips
#   strong_made  = two_pair / overpair / top_pair_top_kicker /
#                  top_pair_good_kicker
# Excludes: medium_made (top_pair weak kicker etc.) and weak_made — these
# often don't clear eq>=0.55 on paired/two-tone boards.
VALUE_CATS = {
    'straight_flush', 'quads', 'full_house', 'flush', 'straight',
    'set', 'trips',
    'two_pair', 'overpair',
    'top_pair_top_kicker', 'top_pair_good_kicker',
}


def _category_of(hero_cards: List[str], board: List[str]) -> str:
    return evaluate_hand(hero_cards, board).category


def _is_value(hero_cards: List[str], board: List[str]) -> bool:
    return _category_of(hero_cards, board) in VALUE_CATS


# =============================================================================
# Card utilities
# =============================================================================
_RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
_SUITS = ['h', 'd', 'c', 's']


def _all_cards() -> List[str]:
    return [r + s for r in _RANKS for s in _SUITS]


def _has_flush_draw_with_board(hero_cards: List[str], board: List[str]) -> bool:
    """Any single suit appears 4+ times across hero+board."""
    from collections import Counter
    suits = [c[1] for c in hero_cards] + [c[1] for c in board]
    return max(Counter(suits).values()) >= 4


def _pick_value_hole_cards(
    board: List[str],
    max_hands: int,
    used: set,
) -> List[List[str]]:
    """Pick up to max_hands 2-card combos that evaluate as VALUE on board.

    Iterates high-ranks-first — value hands typically involve high cards
    (overpairs, top pair, broadway two-pair). Also avoids flush-draw
    exposure which hurts equity below 0.55 on wet boards.

    Predicate check `eq >= 0.55` happens at build time; this picker is
    the cheap pre-filter on category + flush-draw."""
    dead = set(board) | used
    rank_high_first = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    ordered_cards = [r + s for r in rank_high_first for s in _SUITS]
    available = [c for c in ordered_cards if c not in dead]
    found: List[List[str]] = []
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            cards = [available[i], available[j]]
            try:
                ev = evaluate_hand(cards, board)
                if ev.category not in VALUE_CATS:
                    continue
                # If hero exposes flush-draw that completes on turn, eq often
                # drops below 0.55 — predicate would reject; skip early.
                if _has_flush_draw_with_board(cards, board):
                    # allow only if hero's flush-draw doesn't dilute: unlikely
                    # on 3-card flop, skip defensively
                    continue
                found.append(cards)
                if len(found) >= max_hands:
                    return found
            except Exception:
                continue
    return found


# =============================================================================
# Turn card selection — avoid cards that break hero's made-hand state
# =============================================================================
def _safe_turn_card(board_flop: List[str], hero_cards: List[str]) -> str:
    """Prefer turn cards that don't add flush completions. For value hands,
    we want hero's equity to STAY above 0.55 — the probe showed any
    non-flush-completing offsuit card works in most cases."""
    dead = set(board_flop) | set(hero_cards)
    flop_suits = [c[1] for c in board_flop]
    hot_suits = {s for s in flop_suits if flop_suits.count(s) >= 2}
    pool = ['2h', '3c', '4d', '5s', '6h', '7c', '8d', '9s',
            'Tc', 'Jd', 'Qh', 'Kc', 'Ad']
    for c in pool:
        if c in dead:
            continue
        if c[1] in hot_suits:
            continue
        return c
    for c in pool:
        if c not in dead:
            return c
    for c in _all_cards():
        if c not in dead:
            return c
    raise RuntimeError("no turn card available")


# =============================================================================
# Preflop history
# =============================================================================
def _preflop_history(opener: str, callers: List[str]) -> List[Tuple[str, str, str]]:
    acts = [('preflop', opener, 'raise')]
    for c in callers:
        acts.append(('preflop', c, 'call'))
    return acts


# =============================================================================
# Archetypes — same as v2.3.1
# =============================================================================
ARCHETYPES_3WAY_IP = [
    ('BTN', ['SB', 'BB'], 'BTN'),
    ('BTN', ['HJ', 'BB'], 'BTN'),
    ('BTN', ['CO', 'SB'], 'CO'),
    ('CO',  ['SB', 'BB'], 'CO'),
    ('CO',  ['HJ', 'BB'], 'CO'),
]
ARCHETYPES_3WAY_IP = [
    (h, v, o) for (h, v, o) in ARCHETYPES_3WAY_IP
    if all(_PFO[h] > _PFO[vp] for vp in v)
]

ARCHETYPES_3WAY_OOP = [
    ('SB', ['CO', 'BTN'], 'CO'),
    ('BB', ['HJ', 'BTN'], 'HJ'),
    ('BB', ['CO', 'BTN'], 'CO'),
]

ARCHETYPES_HU_IP = [
    ('BTN', ['BB'], 'BTN'),
    ('BTN', ['SB'], 'BTN'),
    ('CO',  ['BB'], 'CO'),
    ('HJ',  ['BB'], 'HJ'),
    ('BTN', ['CO'], 'CO'),
    ('BTN', ['HJ'], 'HJ'),
]
ARCHETYPES_HU_IP = [
    (h, v, o) for (h, v, o) in ARCHETYPES_HU_IP
    if _PFO[h] > _PFO[v[0]]
]

ARCHETYPES_HU_OOP = [
    ('SB', ['BTN'], 'BTN'),
    ('BB', ['BTN'], 'BTN'),
    ('BB', ['CO'],  'CO'),
    ('BB', ['HJ'],  'HJ'),
    ('SB', ['CO'],  'CO'),
]


# =============================================================================
# Spec construction
# =============================================================================
def _make_spec(
    hero_cards: List[str],
    board: List[str],
    hero_pos: str,
    villain_positions: List[str],
    street: str,
    action_history: List[Tuple[str, str, str]],
    opener_position: str,
    num_opponents: int,
) -> SituationSpec:
    return SituationSpec(
        hero_cards=hero_cards,
        board_cards=board,
        hero_pos=hero_pos,
        villain_positions=villain_positions,
        pot=STD_POT,
        to_call=0.0,
        street=street,
        action_history=action_history,
        opener_position=opener_position,
        effective_stack=STD_STACK,
        current_bet=0.0,
        num_opponents=num_opponents,
    )


def _checked_through_history(
    street: str,
    hero_pos: str,
    villain_positions: List[str],
    opener: str,
) -> List[Tuple[str, str, str]]:
    """Turn-shifted check-through: flop all-check, on turn villains-before-
    hero check. Matches v2.3.1 pattern."""
    active = villain_positions + [hero_pos]
    order = sorted(active, key=lambda p: _PFO[p])
    hero_order = _PFO[hero_pos]
    pre = _preflop_history(opener, [p for p in active if p != opener])
    if street == 'turn':
        flop_acts = [('flop', p, 'check') for p in order]
        turn_acts = [('turn', p, 'check') for p in order if _PFO[p] < hero_order]
        return pre + flop_acts + turn_acts
    if street == 'flop':
        acts = [('flop', p, 'check') for p in order if _PFO[p] < hero_order]
        return pre + acts
    # river — not generated in this factory
    flop_acts = [('flop', p, 'check') for p in order]
    turn_acts = [('turn', p, 'check') for p in order]
    river_acts = [('river', p, 'check') for p in order if _PFO[p] < hero_order]
    return pre + flop_acts + turn_acts + river_acts


# =============================================================================
# Litmus seeds — value class (HARD FAIL if either misses predicate)
# =============================================================================
LITMUS_SEEDS: List[Tuple[str, SituationSpec]] = []

_LITMUS_TURN_AA = '3c'  # AA+7h5d2c probe: eq=0.703, cat=9 overpair
_LITMUS_TURN_KQ = '2c'  # KQ+KsTs3h probe: eq=0.609, cat=7 TPGK


def _build_litmus_seeds() -> None:
    LITMUS_SEEDS.clear()

    # AA on 7h5d2c, turn 3c — BTN hero, SB+BB villains, flop check-through.
    flop_a = ['7h', '5d', '2c']
    board_a = flop_a + [_LITMUS_TURN_AA]
    hist_a = _checked_through_history('turn', 'BTN', ['SB', 'BB'], 'BTN')
    spec_a = _make_spec(
        hero_cards=['Ah', 'As'],
        board=board_a,
        hero_pos='BTN',
        villain_positions=['SB', 'BB'],
        street='turn',
        action_history=hist_a,
        opener_position='BTN',
        num_opponents=2,
    )
    LITMUS_SEEDS.append(('LITMUS_AA_7h5d2c_turn', spec_a))

    # KQ on KsTs3h, turn 2c — BTN hero, SB+BB villains.
    flop_b = ['Ks', 'Ts', '3h']
    board_b = flop_b + [_LITMUS_TURN_KQ]
    hist_b = _checked_through_history('turn', 'BTN', ['SB', 'BB'], 'BTN')
    spec_b = _make_spec(
        hero_cards=['Kh', 'Qd'],
        board=board_b,
        hero_pos='BTN',
        villain_positions=['SB', 'BB'],
        street='turn',
        action_history=hist_b,
        opener_position='BTN',
        num_opponents=2,
    )
    LITMUS_SEEDS.append(('LITMUS_KQ_KsTs3h_turn', spec_b))


# =============================================================================
# Bucket builders
# =============================================================================
def _build_checked_through_specs(
    archetypes: List[Tuple[str, List[str], str]],
    streets: List[str],
    num_opponents: int,
    board_pool: List[List[str]],
    max_per_archetype: int = 5,
    target: int = 25,
) -> List[Tuple[SituationSpec, str]]:
    """Board-outermost, archetype-rotated iteration (diversity). Mirror of
    v2.3.1 loop."""
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    picks_per_archetype: Dict[str, int] = {}

    for pass_idx in range(3):
        for flop_idx, flop in enumerate(board_pool):
            if len(specs) >= target:
                return specs
            rotated = (archetypes[flop_idx % len(archetypes):]
                       + archetypes[:flop_idx % len(archetypes)])
            for hero_pos, villain_positions, opener in rotated:
                if len(specs) >= target:
                    return specs
                key = f'{hero_pos}_{tuple(villain_positions)}'
                if picks_per_archetype.get(key, 0) >= max_per_archetype:
                    continue
                street = streets[(pass_idx + flop_idx) % len(streets)]
                if street == 'turn':
                    turn = _safe_turn_card(flop, [])
                    board = flop + [turn]
                elif street == 'flop':
                    # value hands on flop IP checked-to are valid shape but
                    # bridge vcb=0; skip to keep predicate clean
                    continue
                else:
                    continue

                hist = _checked_through_history(
                    street, hero_pos, villain_positions, opener,
                )
                heroes = _pick_value_hole_cards(board, max_hands=1, used=used)
                if not heroes:
                    continue
                hero = heroes[0]
                spec = _make_spec(
                    hero_cards=hero,
                    board=board,
                    hero_pos=hero_pos,
                    villain_positions=villain_positions,
                    street=street,
                    action_history=hist,
                    opener_position=opener,
                    num_opponents=num_opponents,
                )
                desc = (
                    f'value-BET (opp={num_opponents}): hero {hero_pos} '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'street={street}, checked-through.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
                picks_per_archetype[key] = picks_per_archetype.get(key, 0) + 1
    return specs


def build_3way_specs(target: int = 38) -> List[Tuple[SituationSpec, str]]:
    """3-way value-BET, turn-only."""
    ip = _build_checked_through_specs(
        ARCHETYPES_3WAY_IP,
        streets=['turn'],
        num_opponents=2,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=10,
        target=target - 10,
    )
    remaining = target - len(ip)
    oop = _build_checked_through_specs(
        ARCHETYPES_3WAY_OOP,
        streets=['turn'],
        num_opponents=2,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=8,
        target=remaining,
    )
    return ip + oop


def build_hu_specs(target: int = 30) -> List[Tuple[SituationSpec, str]]:
    """HU value-BET, turn-only. Opportunistic yield (v2.4 prep)."""
    ip = _build_checked_through_specs(
        ARCHETYPES_HU_IP,
        streets=['turn'],
        num_opponents=1,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=5,
        target=target - 8,
    )
    remaining = target - len(ip)
    oop = _build_checked_through_specs(
        ARCHETYPES_HU_OOP,
        streets=['turn'],
        num_opponents=1,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=4,
        target=remaining,
    )
    return ip + oop


# =============================================================================
# Predicate + build + filter
# =============================================================================
def _predicate_passes(feat_dict: dict) -> Tuple[bool, List[str]]:
    """Value-BET predicate per directive-o §Generation."""
    fails = []
    if feat_dict.get('facing_bet', 0) != 0:
        fails.append(f"facing_bet={feat_dict.get('facing_bet')} (expected 0)")
    if feat_dict.get('villain_checked_back', 0) != 1:
        fails.append(
            f"villain_checked_back={feat_dict.get('villain_checked_back')} "
            f"(expected 1)"
        )
    n_opp = feat_dict.get('num_opponents', 0)
    if n_opp not in (1, 2):
        fails.append(f"num_opponents={n_opp} (expected in {{1,2}})")
    if feat_dict.get('is_made_hand', 0) != 1:
        fails.append(f"is_made_hand={feat_dict.get('is_made_hand')} (expected 1)")
    if feat_dict.get('equity_vs_range', 0.0) < 0.55:
        fails.append(
            f"equity_vs_range={feat_dict.get('equity_vs_range'):.3f} "
            f"(expected >=0.55)"
        )
    return (len(fails) == 0, fails)


def _build_record(
    spec: SituationSpec,
    description: str,
    sit_id: str,
    bucket: str,
) -> Tuple[dict, List[str], List[str]]:
    try:
        feat_dict = build_situation(spec)
    except Exception as exc:
        return (
            {
                '_skip_reason': f'BUILD_EXCEPTION: {exc}',
                'situation_id': sit_id,
                'bucket': bucket,
                'has_errors': True,
                'validation_errors': [str(exc)],
                'villain_positions': list(spec.villain_positions),
                'hero_position': spec.hero_pos,
                'action_string': spec.action_string or '',
                'street': spec.street,
            },
            [str(exc)],
            [],
        )

    validation_errors = validate_situation(spec, feat_dict) or []
    ok, pred_fails = _predicate_passes(feat_dict)

    feat_dict['situation_id'] = sit_id
    feat_dict['bucket'] = bucket
    feat_dict['sub_pattern'] = bucket
    feat_dict['hero_cards'] = ''.join(spec.hero_cards)
    feat_dict['board_cards'] = ''.join(spec.board_cards)
    feat_dict['description'] = description
    feat_dict['action_string'] = spec.action_string
    feat_dict['hero_position'] = spec.hero_pos
    feat_dict['villain_positions'] = list(spec.villain_positions)
    feat_dict['street'] = spec.street
    feat_dict['has_errors'] = bool(validation_errors) or not ok
    if validation_errors:
        feat_dict['validation_errors'] = validation_errors
    if not ok:
        feat_dict['_predicate_fails'] = pred_fails

    return feat_dict, validation_errors, pred_fails


def _write_jsonl(records: List[dict], path: str) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_rows = [
        r for r in records
        if not r.get('_skip_reason')
        and not r.get('_predicate_fails')
        and not r.get('has_errors')
    ]
    with open(path, 'w') as f:
        for r in write_rows:
            f.write(json.dumps(normalise_situation(r)) + '\n')
    return len(write_rows)


def _preflight_schema_check(path: str) -> List[str]:
    errors = []
    if not os.path.exists(path):
        return [f'{path}: MISSING']
    with open(path) as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            for col in ('street', 'hero_position'):
                v = rec.get(col)
                if v is None:
                    continue
                if not isinstance(v, (int, float)) or isinstance(v, bool):
                    errors.append(f'{path}:{col} line {i} = {v!r} (non-numeric)')
                    break
    return errors


def _verify_litmus(records_3way: List[dict]) -> List[str]:
    failures = []
    litmus_ids = {sid for sid, _ in LITMUS_SEEDS}
    seen_ok = set()
    for r in records_3way:
        if r.get('situation_id') in litmus_ids:
            if r.get('_skip_reason'):
                failures.append(f'{r["situation_id"]}: BUILD_EXCEPTION')
            elif r.get('_predicate_fails'):
                failures.append(
                    f'{r["situation_id"]}: predicate fail — '
                    f'{"; ".join(r["_predicate_fails"])}'
                )
            elif r.get('has_errors'):
                failures.append(
                    f'{r["situation_id"]}: validation errors — '
                    f'{r.get("validation_errors")}'
                )
            else:
                seen_ok.add(r['situation_id'])
    missing = litmus_ids - seen_ok - {m.split(":")[0] for m in failures}
    for m in missing:
        failures.append(f'{m}: not present in output')
    return failures


def main(
    target_3way: int = 40,  # 38 clean + 2 litmus = 40, matches v2.3.1's 40 CHECK
    target_hu: int = 30,
) -> bool:
    print('=' * 72)
    print('v2.3.2 Layer 2-mirror — VALUE-BET counter-example generator')
    print('=' * 72)

    _build_litmus_seeds()

    # Litmus-first hard-fail
    litmus_records: List[dict] = []
    for sid, spec in LITMUS_SEEDS:
        rec, _, _ = _build_record(
            spec,
            description=(
                f'{sid}: hand=[{"".join(spec.hero_cards)}] '
                f'on {"".join(spec.board_cards)}; value litmus seed.'
            ),
            sit_id=sid,
            bucket='LITMUS_VALUE',
        )
        litmus_records.append(rec)

    litmus_failures = _verify_litmus(litmus_records)
    if litmus_failures:
        print('\n**LITMUS HARD-FAIL** — generator cannot produce seeded litmus:')
        for f in litmus_failures:
            print(f'  - {f}')
        _write_jsonl(
            litmus_records,
            os.path.join(OUTPUT_DIR, 'v23_2_value_bet_litmus_debug.jsonl'),
        )
        return False
    print(f'\nLITMUS seeds OK: {[sid for sid, _ in LITMUS_SEEDS]}')

    # 3-way
    print(f'\n[3-way] target={target_3way}')
    specs_3way = build_3way_specs(target=target_3way)
    print(f'  built {len(specs_3way)} specs')
    records_3way: List[dict] = list(litmus_records)
    for idx, (spec, desc) in enumerate(specs_3way):
        sit_id = f'VALUE_BET_3WAY_{idx + 1:03d}'
        rec, _, _ = _build_record(spec, desc, sit_id, 'VALUE_BET_3WAY')
        records_3way.append(rec)

    # HU
    print(f'\n[HU] target={target_hu}')
    specs_hu = build_hu_specs(target=target_hu)
    print(f'  built {len(specs_hu)} specs')
    records_hu: List[dict] = []
    for idx, (spec, desc) in enumerate(specs_hu):
        sit_id = f'VALUE_BET_HU_{idx + 1:03d}'
        rec, _, _ = _build_record(spec, desc, sit_id, 'VALUE_BET_HU')
        records_hu.append(rec)

    # Write
    out_3way = os.path.join(OUTPUT_DIR, 'v23_2_value_bet_3way.jsonl')
    out_hu = os.path.join(OUTPUT_DIR, 'v23_2_value_bet_hu.jsonl')
    written_3way = _write_jsonl(records_3way, out_3way)
    written_hu = _write_jsonl(records_hu, out_hu)

    def _stats(records, label):
        generated = len(records)
        build_failures = sum(1 for r in records if r.get('_skip_reason'))
        predicate_failures = sum(
            1 for r in records if r.get('_predicate_fails')
        )
        validation_failures = sum(
            1 for r in records
            if r.get('has_errors')
            and not r.get('_skip_reason')
            and not r.get('_predicate_fails')
        )
        clean = (generated - build_failures - predicate_failures
                 - validation_failures)
        print(f'  [{label}] generated={generated} build_fail={build_failures} '
              f'pred_fail={predicate_failures} '
              f'valid_fail={validation_failures} clean={clean}')
        return (generated, build_failures, predicate_failures,
                validation_failures, clean)

    print('\n' + '=' * 72)
    print('STATS')
    print('=' * 72)
    s3 = _stats(records_3way, '3-way')
    sh = _stats(records_hu, 'HU')
    print(f'\n  written 3-way: {written_3way} → {out_3way}')
    print(f'  written HU:    {written_hu} → {out_hu}')

    pf_errors_3way = _preflight_schema_check(out_3way)
    pf_errors_hu = _preflight_schema_check(out_hu)
    if pf_errors_3way or pf_errors_hu:
        print('\n**PREFLIGHT SCHEMA CHECK FAILED**')
        for e in (pf_errors_3way + pf_errors_hu)[:10]:
            print(f'  {e}')
        return False
    print('\n  preflight schema: ALL PASS')

    for label, (gen, bf, _, _, _) in [('3-way', s3), ('HU', sh)]:
        if gen > 0 and bf / gen > 0.25:
            print(f'\n**STOP**: {label} build failure rate = {bf/gen:.1%} > 25%')
            return False

    print(f'\n  3-way predicate pass-through: '
          f'{s3[4]}/{s3[0]} = {s3[4]/max(1,s3[0]):.0%}')
    print(f'  HU predicate pass-through:    '
          f'{sh[4]}/{sh[0]} = {sh[4]/max(1,sh[0]):.0%}')

    with open(out_3way) as f:
        written_ids = {
            json.loads(l).get('situation_id') for l in f if l.strip()
        }
    missing_litmus = [sid for sid, _ in LITMUS_SEEDS if sid not in written_ids]
    if missing_litmus:
        print(f'\n**LITMUS FINAL CHECK FAILED** — missing: {missing_litmus}')
        return False
    print(f'\n  litmus final: BOTH PRESENT in {out_3way}')

    if written_3way < 30:
        print(f'\n**YIELD GATE**: 3-way written={written_3way} < 30 (target 30-40)')
        return False

    return True


if __name__ == '__main__':
    raise SystemExit(0 if main() else 1)
