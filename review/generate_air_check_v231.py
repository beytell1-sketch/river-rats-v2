"""generate_air_check_v231.py — v2.3.1 Layer 2 AIR-CHECK counter-example generator.

Produces the missing counter-example class per MAIN_TERMINAL_UPDATE_2026-04-18-g
§Layer 2, with adjustments from REVIEW_BUILDER_AIR_CHECK_PLAN (0a2467e) and
resolutions from MAIN_TERMINAL_DECISION_2026-04-18-h (95e9221):

  - Two output streams: 3-way (labelled for v2.3.1) and HU (v2.4 prep, unlabelled)
  - Litmus seeds shifted to TURN with flop check-through (Path B, Blocker 2):
    bridge computes villain_checked_back from prior streets only, so the
    predicate only fires on turn+. Layer 1 (board_adjusted_hrp) handles the
    literal flop playtest spots at inference; Layer 2 teaches the broader
    air+vcb=1+checked-through pattern on turn+.
  - Hard-fail on 3-way litmus miss (both litmus specs must pass predicate);
    HU is opportunistic with no litmus requirement.
  - Expanded monotone board pool (4 boards across suits)

Outputs:
  training-data/v23_air_check_3way.jsonl   (target 30-40 BP; labelled for v2.3.1)
  training-data/v23_air_check_hu.jsonl     (opportunistic; v2.4 prep, unlabelled)

Predicate (per update-g §Layer 2):
  facing_bet=0, villain_checked_back=1, is_made_hand=0,
  draw_outs <= 2, equity_vs_range < 0.35, num_opponents in {1, 2}

Preflop convention: standard raise-call (not 3-bet). is_3bet_pot=0.
Pot=90, effective_stack=450 (batch6 convention, SPR ~ 1.11).

Run:
  python3 review/generate_air_check_v231.py
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
os.chdir(_CORE)  # ensures range data + model assets resolve

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
# Board templates
# =============================================================================
# Monotone boards — core coverage for the A4d-on-Qs5s7s class (hero has no suit,
# zero outs, hostile texture). Per REVIEW adjustment #3.
MONOTONE_BOARDS = [
    ['Qs', '5s', '7s'],  # A4d litmus board
    ['Jh', '8h', '3h'],
    ['Kd', '9d', '4d'],
    ['Ac', '6c', '2c'],
]

# Paired boards — T5/JJ2 litmus class (small hand on paired board, overbet-
# shaped villain range with lots of air).
PAIRED_BOARDS = [
    ['Jc', 'Jd', '2h'],  # T5h litmus board (with Jd as second J)
    ['9h', '9c', '4d'],
    ['Qs', 'Qd', '5c'],
    ['8c', '8d', '3s'],
    ['Kh', 'Ks', '7d'],
]

# Dry rainbow boards — classic "checked-through" contexts where villain range
# is capped but hero has nothing either.
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

# Two-tone dry-ish boards — broader texture coverage.
TWO_TONE_BOARDS = [
    ['Ts', '6s', '3d'],
    ['Qh', '8h', '4d'],
    ['Jc', '7c', '2d'],
    ['Kd', '8d', '4h'],
    ['Qs', '5d', '2h'],
]

FLOP_BOARDS_ALL = MONOTONE_BOARDS + PAIRED_BOARDS + DRY_BOARDS + TWO_TONE_BOARDS


# =============================================================================
# Hand category classification
# =============================================================================
# AIR_CATS matches the comment block in generate_factory_batch6.py:
#   air = high_card / overcards / one_overcard / nothing
AIR_CATS = {'high_card', 'overcards', 'one_overcard', 'nothing'}


def _category_of(hero_cards: List[str], board: List[str]) -> str:
    return evaluate_hand(hero_cards, board).category


def _is_air(hero_cards: List[str], board: List[str]) -> bool:
    return _category_of(hero_cards, board) in AIR_CATS


# =============================================================================
# Card utilities
# =============================================================================
_RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
_SUITS = ['h', 'd', 'c', 's']


def _all_cards() -> List[str]:
    return [r + s for r in _RANKS for s in _SUITS]


def _has_flush_draw_with_board(hero_cards: List[str], board: List[str]) -> bool:
    """Cheap flush-draw check: any single suit appears 4+ times across hero+board."""
    from collections import Counter
    suits = [c[1] for c in hero_cards] + [c[1] for c in board]
    return max(Counter(suits).values()) >= 4


def _pick_air_hole_cards(
    board: List[str],
    max_hands: int,
    used: set,
) -> List[List[str]]:
    """Pick up to max_hands 2-card combos that evaluate as AIR on board
    AND have draw_outs<=2 (cheap check via hand_evaluator). Iterates
    ranks from middle outward to prefer disconnected-from-board hands
    (helps predicate equity_vs_range<0.35 without dragging in straight
    connectors at either rank extreme)."""
    dead = set(board) | used
    # Mid-rank outward ordering: T, 9, 8, J, 7, Q, 6, K, 5, A, 4, 3, 2.
    # This prefers mid-rank offsuit hands which tend to be disconnected
    # from most board textures (avoids the A-high "too much equity"
    # class AND the low-connector "straight draw" class).
    rank_order = ['T', '9', '8', 'J', '7', 'Q', '6', 'K', '5', 'A', '4', '3', '2']
    ordered_cards = [r + s for r in rank_order for s in _SUITS]
    available = [c for c in ordered_cards if c not in dead]
    found: List[List[str]] = []
    for i in range(len(available)):
        for j in range(i + 1, len(available)):
            cards = [available[i], available[j]]
            try:
                ev = evaluate_hand(cards, board)
                if ev.category not in AIR_CATS:
                    continue
                if ev.draw_outs > 2:
                    continue
                if _has_flush_draw_with_board(cards, board):
                    continue
                found.append(cards)
                if len(found) >= max_hands:
                    return found
            except Exception:
                continue
    return found


# =============================================================================
# Turn card selection
# =============================================================================
# Prefer turn cards that DON'T complete obvious draws — we want the AIR-on-
# checked-through signal clean. Avoid cards of same suit as a 2+ suited flop.
def _safe_turn_card(board_flop: List[str], hero_cards: List[str]) -> str:
    dead = set(board_flop) | set(hero_cards)
    # Suits already present 2+ times on flop → avoid completing flush draws.
    flop_suits = [c[1] for c in board_flop]
    hot_suits = {s for s in flop_suits if flop_suits.count(s) >= 2}
    # Cards by preference: offsuit blank mid-low ranks first.
    pool = ['2h', '3c', '4d', '5s', '6h', '7c', '8d', '9s',
            'Tc', 'Jd', 'Qh', 'Kc', 'Ad']
    for c in pool:
        if c in dead:
            continue
        if c[1] in hot_suits:
            continue
        return c
    # Fallback: allow any unused card
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
# Archetypes
# =============================================================================
# 3-way: hero IP on flop / IP or OOP on turn (OOP turn works because flop
# check-through sets villain_checked_back=1). Bridge primary villain must have
# a check recorded somewhere prior.
ARCHETYPES_3WAY_IP = [
    ('BTN', ['SB', 'BB'], 'BTN'),   # flop order: SB → BB → BTN
    ('BTN', ['HJ', 'BB'], 'BTN'),
    ('BTN', ['CO', 'SB'], 'CO'),
    ('CO',  ['SB', 'BB'], 'CO'),
    ('CO',  ['HJ', 'BB'], 'CO'),
]

# Validate IP ordering
ARCHETYPES_3WAY_IP = [
    (h, v, o) for (h, v, o) in ARCHETYPES_3WAY_IP
    if all(_PFO[h] > _PFO[vp] for vp in v)
]

ARCHETYPES_3WAY_OOP = [
    ('SB', ['CO', 'BTN'], 'CO'),
    ('BB', ['HJ', 'BTN'], 'HJ'),
    ('BB', ['CO', 'BTN'], 'CO'),
]

# HU: hero IP on flop (villain OOP must have checked first). Turn allows either
# position provided flop check-through.
ARCHETYPES_HU_IP = [
    ('BTN', ['BB'], 'BTN'),
    ('BTN', ['SB'], 'BTN'),
    ('CO',  ['BB'], 'CO'),
    ('HJ',  ['BB'], 'HJ'),
    ('BTN', ['CO'], 'CO'),  # BTN defend vs CO open
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
    """Build preflop + checked-through postflop action history up to hero's turn.

    Semantics:
      - Flop, hero IP: villains check in postflop order before hero acts.
      - Turn: flop all-check through; on turn, villains ahead of hero check.
      - River: flop + turn all-check; river villains ahead of hero check.

    All histories end without hero's current-street action; factory will
    treat hero as acting next.
    """
    active = villain_positions + [hero_pos]
    order = sorted(active, key=lambda p: _PFO[p])
    hero_order = _PFO[hero_pos]

    pre = _preflop_history(
        opener,
        [p for p in active if p != opener],
    )

    if street == 'flop':
        # Villains acting before hero check; hero is about to act.
        acts = [('flop', p, 'check') for p in order if _PFO[p] < hero_order]
        return pre + acts

    if street == 'turn':
        flop_acts = [('flop', p, 'check') for p in order]
        turn_acts = [('turn', p, 'check') for p in order if _PFO[p] < hero_order]
        return pre + flop_acts + turn_acts

    # river (not used by the main generator paths, but kept for completeness)
    flop_acts = [('flop', p, 'check') for p in order]
    turn_acts = [('turn', p, 'check') for p in order]
    river_acts = [('river', p, 'check') for p in order if _PFO[p] < hero_order]
    return pre + flop_acts + turn_acts + river_acts


# =============================================================================
# Litmus seeds — HARD FAIL if either misses predicate (REVIEW adjustment #2)
# Shifted to TURN per Decision-h Blocker 2: bridge computes vcb from prior
# streets only. Same hero + flop + villain weakness context, one street later.
# =============================================================================
LITMUS_SEEDS: List[Tuple[str, SituationSpec]] = []

# Safe turn cards per Decision-h §Blocker 2 guidance. NOTE: initial
# guidance suggested "low non-spade" (2c/3d/4h) but those cards open a
# gutshot straight for A4d (4-5-7-low → A2345 wheel needs a 3, giving
# draw_outs=4 and failing the predicate). Any low card 2-8 opens some
# wheel/connector for A4. High non-spade picks preserve air cleanly.
# Probed empirically: Kc gives draw_outs=0, equity_vs_range=0.038 (air).
_LITMUS_TURN_A = 'Kc'  # A4d air-preserving: no flush, no pair, no straight
_LITMUS_TURN_B = '3c'  # T5h air-preserving: offsuit, doesn't pair JJ2, no draws


def _build_litmus_seeds() -> None:
    LITMUS_SEEDS.clear()

    # A4d on Qs5s7s, turn 2c — BTN hero, SB+BB villains, flop check-through.
    flop_a = ['Qs', '5s', '7s']
    board_a = flop_a + [_LITMUS_TURN_A]
    hist_a = _checked_through_history('turn', 'BTN', ['SB', 'BB'], 'BTN')
    spec_a = _make_spec(
        hero_cards=['Ad', '4d'],
        board=board_a,
        hero_pos='BTN',
        villain_positions=['SB', 'BB'],
        street='turn',
        action_history=hist_a,
        opener_position='BTN',
        num_opponents=2,
    )
    LITMUS_SEEDS.append(('LITMUS_A4d_Qs5s7s_turn', spec_a))

    # T5h on JJ2, turn 3c — BTN hero, SB+BB villains, flop check-through.
    flop_b = ['Jc', 'Jd', '2h']
    board_b = flop_b + [_LITMUS_TURN_B]
    hist_b = _checked_through_history('turn', 'BTN', ['SB', 'BB'], 'BTN')
    spec_b = _make_spec(
        hero_cards=['Th', '5h'],
        board=board_b,
        hero_pos='BTN',
        villain_positions=['SB', 'BB'],
        street='turn',
        action_history=hist_b,
        opener_position='BTN',
        num_opponents=2,
    )
    LITMUS_SEEDS.append(('LITMUS_T5h_JJ2_turn', spec_b))


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
    """Walk (board × archetype × street) combinations (board outermost for
    diversity), pick one AIR hero hand per cell, build checked-through specs.
    Stops at target count."""
    specs: List[Tuple[SituationSpec, str]] = []
    used: set = set()
    picks_per_archetype: Dict[str, int] = {}

    # Multi-pass over boards to stay within max_per_archetype while still
    # distributing across the pool. Each pass adds at most one hand per
    # (archetype × street) cell.
    for pass_idx in range(3):
        for flop_idx, flop in enumerate(board_pool):
            if len(specs) >= target:
                return specs
            # Rotate archetype order per board to avoid always using the
            # same archetype-first ordering.
            rotated = archetypes[flop_idx % len(archetypes):] + archetypes[:flop_idx % len(archetypes)]
            for hero_pos, villain_positions, opener in rotated:
                if len(specs) >= target:
                    return specs
                key = f'{hero_pos}_{tuple(villain_positions)}'
                if picks_per_archetype.get(key, 0) >= max_per_archetype:
                    continue
                # Pick the pass_idx'th street choice (cycles through streets).
                street = streets[(pass_idx + flop_idx) % len(streets)]

                # Build board by street
                if street == 'turn':
                    turn = _safe_turn_card(flop, [])
                    board = flop + [turn]
                elif street == 'flop':
                    # Hero must be last to act on flop for villains to have checked.
                    if _PFO[hero_pos] <= max(_PFO[v] for v in villain_positions):
                        continue
                    board = list(flop)
                else:
                    continue  # river not generated

                hist = _checked_through_history(street, hero_pos, villain_positions, opener)
                heroes = _pick_air_hole_cards(board, max_hands=1, used=used)
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
                    f'air-CHECK (opp={num_opponents}): hero {hero_pos} '
                    f'({_category_of(hero, board)}) on {"-".join(board)}; '
                    f'street={street}, checked-through.'
                )
                specs.append((spec, desc))
                used.add(tuple(sorted(hero)))
                picks_per_archetype[key] = picks_per_archetype.get(key, 0) + 1
    return specs


def build_3way_specs(target: int = 40) -> List[Tuple[SituationSpec, str]]:
    """3-way AIR-CHECK, turn-only (vcb=1 requires prior-street checks)."""
    ip = _build_checked_through_specs(
        ARCHETYPES_3WAY_IP,
        streets=['turn'],
        num_opponents=2,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=6,
        target=target - 10,
    )
    remaining = target - len(ip)
    oop = _build_checked_through_specs(
        ARCHETYPES_3WAY_OOP,
        streets=['turn'],
        num_opponents=2,
        board_pool=FLOP_BOARDS_ALL,
        max_per_archetype=4,
        target=remaining,
    )
    return ip + oop


def build_hu_specs(target: int = 30) -> List[Tuple[SituationSpec, str]]:
    """HU AIR-CHECK, turn-only. Opportunistic yield (v2.4 prep)."""
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
    """Per update-g §Layer 2. Returns (ok, list_of_failed_conditions)."""
    fails = []
    if feat_dict.get('facing_bet', 0) != 0:
        fails.append(f"facing_bet={feat_dict.get('facing_bet')} (expected 0)")
    if feat_dict.get('villain_checked_back', 0) != 1:
        fails.append(
            f"villain_checked_back={feat_dict.get('villain_checked_back')} (expected 1)"
        )
    n_opp = feat_dict.get('num_opponents', 0)
    if n_opp not in (1, 2):
        fails.append(f"num_opponents={n_opp} (expected in {{1,2}})")
    if feat_dict.get('is_made_hand', 0) != 0:
        fails.append(f"is_made_hand={feat_dict.get('is_made_hand')} (expected 0)")
    if feat_dict.get('draw_outs', 99) > 2:
        fails.append(f"draw_outs={feat_dict.get('draw_outs')} (expected <=2)")
    if feat_dict.get('equity_vs_range', 1.0) >= 0.35:
        fails.append(
            f"equity_vs_range={feat_dict.get('equity_vs_range'):.3f} (expected <0.35)"
        )
    return (len(fails) == 0, fails)


def _build_record(
    spec: SituationSpec,
    description: str,
    sit_id: str,
    bucket: str,
) -> Tuple[dict, List[str], List[str]]:
    """Returns (record, validation_errors, predicate_fails).

    Record is None if build_situation raised."""
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


# =============================================================================
# Orchestrator
# =============================================================================
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
    """HARD requirement: both litmus seeds must appear as clean passes in the
    3-way output. Returns list of failure messages; empty = pass."""
    failures = []
    litmus_ids = {sid for sid, _ in LITMUS_SEEDS}
    seen_ok = set()
    for r in records_3way:
        if r.get('situation_id') in litmus_ids:
            if r.get('_skip_reason'):
                failures.append(
                    f'{r["situation_id"]}: BUILD_EXCEPTION '
                    f'({r.get("_skip_reason")})'
                )
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
    target_3way: int = 38,  # +2 litmus seeds = 40 total (upper bound of 30-40)
    target_hu: int = 30,
) -> bool:
    print('=' * 72)
    print('v2.3.1 Layer 2 — AIR-CHECK counter-example generator')
    print('=' * 72)

    _build_litmus_seeds()

    # ---- Litmus seeds first (3-way only, per update-g framing) ----
    litmus_records: List[dict] = []
    for sid, spec in LITMUS_SEEDS:
        rec, verrs, pfails = _build_record(
            spec,
            description=f'{sid}: hand=[{"".join(spec.hero_cards)}] '
                        f'on {"".join(spec.board_cards)}; litmus seed.',
            sit_id=sid,
            bucket='LITMUS',
        )
        litmus_records.append(rec)

    # HARD-FAIL check on litmus BEFORE building the rest
    litmus_failures = _verify_litmus(litmus_records)
    if litmus_failures:
        print('\n**LITMUS HARD-FAIL** — generator cannot produce seeded playtest spots:')
        for f in litmus_failures:
            print(f'  - {f}')
        print('\nThis is a generator bug. See REVIEW adjustment #2. Aborting.')
        # Still write what we have for post-mortem inspection
        _write_jsonl(litmus_records, os.path.join(OUTPUT_DIR, 'v23_air_check_litmus_debug.jsonl'))
        return False
    print(f'\nLITMUS seeds OK: {[sid for sid, _ in LITMUS_SEEDS]}')

    # ---- 3-way spec generation ----
    print(f'\n[3-way] target={target_3way}')
    specs_3way = build_3way_specs(target=target_3way)
    print(f'  built {len(specs_3way)} specs')

    records_3way: List[dict] = list(litmus_records)
    used_ids = set()
    for idx, (spec, desc) in enumerate(specs_3way):
        sit_id = f'AIR_CHECK_3WAY_{idx + 1:03d}'
        rec, _, _ = _build_record(spec, desc, sit_id, 'AIR_CHECK_3WAY')
        records_3way.append(rec)
        used_ids.add(sit_id)

    # ---- HU spec generation ----
    print(f'\n[HU] target={target_hu}')
    specs_hu = build_hu_specs(target=target_hu)
    print(f'  built {len(specs_hu)} specs')

    records_hu: List[dict] = []
    for idx, (spec, desc) in enumerate(specs_hu):
        sit_id = f'AIR_CHECK_HU_{idx + 1:03d}'
        rec, _, _ = _build_record(spec, desc, sit_id, 'AIR_CHECK_HU')
        records_hu.append(rec)

    # ---- Write JSONLs ----
    out_3way = os.path.join(OUTPUT_DIR, 'v23_air_check_3way.jsonl')
    out_hu = os.path.join(OUTPUT_DIR, 'v23_air_check_hu.jsonl')
    written_3way = _write_jsonl(records_3way, out_3way)
    written_hu = _write_jsonl(records_hu, out_hu)

    # ---- Stats ----
    def _stats(records: List[dict], label: str):
        generated = len(records)
        build_failures = sum(1 for r in records if r.get('_skip_reason'))
        predicate_failures = sum(1 for r in records if r.get('_predicate_fails'))
        validation_failures = sum(
            1 for r in records
            if r.get('has_errors')
            and not r.get('_skip_reason')
            and not r.get('_predicate_fails')
        )
        clean = generated - build_failures - predicate_failures - validation_failures
        print(f'  [{label}] generated={generated} '
              f'build_fail={build_failures} pred_fail={predicate_failures} '
              f'valid_fail={validation_failures} clean={clean}')
        return (generated, build_failures, predicate_failures, validation_failures, clean)

    print('\n' + '=' * 72)
    print('STATS')
    print('=' * 72)
    s3 = _stats(records_3way, '3-way')
    sh = _stats(records_hu, 'HU')

    print(f'\n  written 3-way: {written_3way} → {out_3way}')
    print(f'  written HU:    {written_hu} → {out_hu}')

    # ---- Preflight ----
    pf_errors_3way = _preflight_schema_check(out_3way)
    pf_errors_hu = _preflight_schema_check(out_hu)
    if pf_errors_3way or pf_errors_hu:
        print('\n**PREFLIGHT SCHEMA CHECK FAILED**')
        for e in (pf_errors_3way + pf_errors_hu)[:10]:
            print(f'  {e}')
        return False
    print('\n  preflight schema: ALL PASS')

    # ---- Stop conditions ----
    # Build failure rate > 25% per bucket → abort
    for label, (gen, bf, _, _, _) in [('3-way', s3), ('HU', sh)]:
        if gen > 0 and bf / gen > 0.25:
            print(f'\n**STOP CONDITION**: {label} build failure rate = {bf/gen:.1%} > 25%')
            return False

    # Predicate pass-through rate informational only
    print()
    print(f'  3-way predicate pass-through: '
          f'{s3[4]}/{s3[0]} = {s3[4]/max(1,s3[0]):.0%}')
    print(f'  HU predicate pass-through:    '
          f'{sh[4]}/{sh[0]} = {sh[4]/max(1,sh[0]):.0%}')

    # Litmus reverify on final written 3-way file (HU not required)
    with open(out_3way) as f:
        written_ids = {json.loads(l).get('situation_id') for l in f if l.strip()}
    missing_litmus = [sid for sid, _ in LITMUS_SEEDS if sid not in written_ids]
    if missing_litmus:
        print(f'\n**LITMUS FINAL CHECK FAILED** — missing from 3-way output: {missing_litmus}')
        return False
    print(f'\n  litmus final: BOTH PRESENT in {out_3way}')

    # ---- 3-way yield gate (target 30-40 BP) ----
    if written_3way < 30:
        print(f'\n**YIELD GATE**: 3-way written={written_3way} < 30 (target 30-40)')
        return False
    if written_3way > 50:
        print(f'\n  [warn] 3-way written={written_3way} exceeds upper target 50; trim?')

    return True


if __name__ == '__main__':
    ok = main()
    sys.exit(0 if ok else 1)
