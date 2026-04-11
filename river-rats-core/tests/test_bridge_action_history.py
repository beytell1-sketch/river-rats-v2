"""
Verify that action-history features in the self-play JSONL are internally
consistent with each situation's own metadata.

Run with:
    python3 /home/rupertbeytell/river-rats-v2/river-rats-core/tests/test_bridge_action_history.py

Pass criteria (printed to stdout):
- Each facing_bet=True situation's facing_raise value is plausible.
- villain_aggression_count matches what the prior_actions list implies.
- villain_checked_back / villain_call_count are consistent.

Known limitations of this cross-check:
- prior_actions in the JSONL is assembled from the *hero* player's
  own action log (generate_3way_situations._extract_3way_decisions),
  NOT from game.street_actions.  So prior_actions captures hero moves,
  not villain moves.  We cannot reconstruct villain history from it.
- Instead we validate internal numeric consistency (facing_raise implies
  facing_bet; aggression_count <= max possible prior streets; etc.)
"""
from __future__ import annotations

import json
import os
import sys

# Make river-rats-core importable
CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if CORE not in sys.path:
    sys.path.insert(0, CORE)

JSONL = os.path.join(
    CORE, '..', 'training-data', '3way_selected_200.jsonl'
)


def load_situations(path: str) -> list:
    with open(os.path.normpath(path)) as f:
        return [json.loads(line) for line in f if line.strip()]


def max_prior_streets(street: str) -> int:
    order = ['preflop', 'flop', 'turn', 'river']
    idx = order.index(street) if street in order else 1
    # Prior postflop streets only (preflop is excluded from aggression count
    # because the feature tracks postflop villain bets).
    # Actually the bridge counts ALL prior streets including preflop for
    # villain_aggression_count, but preflop villain aggression is uncommon
    # in the hero-opened pots that dominate self-play.
    return idx  # maximum streets before this one


PASS = 0
FAIL = 0
WARNINGS = 0


def ok(msg: str):
    global PASS
    PASS += 1
    print(f"  PASS  {msg}")


def fail(msg: str):
    global FAIL
    FAIL += 1
    print(f"  FAIL  {msg}")


def warn(msg: str):
    global WARNINGS
    WARNINGS += 1
    print(f"  WARN  {msg}")


def check_situation(sit: dict, idx: int):
    sid = sit.get('situation_id', f'row_{idx}')
    fd = sit.get('feat_dict', {})
    street = sit.get('street', 'flop')
    facing_bet = bool(sit.get('facing_bet', False))
    to_call = sit.get('to_call', 0)

    # ---- 1. facing_bet vs to_call consistency ----
    if facing_bet and to_call <= 0:
        fail(f"{sid}: facing_bet=True but to_call={to_call}")
    elif not facing_bet and to_call > 0:
        fail(f"{sid}: facing_bet=False but to_call={to_call}")

    # ---- 2. feat_dict facing_bet must match top-level flag ----
    fd_fb = fd.get('facing_bet', -1)
    if fd_fb != int(facing_bet):
        fail(f"{sid}: feat_dict.facing_bet={fd_fb} != top-level facing_bet={int(facing_bet)}")
    else:
        ok(f"{sid}: facing_bet consistent ({fd_fb})")

    # ---- 3. facing_raise only allowed when facing_bet=True ----
    facing_raise = fd.get('facing_raise', 0)
    if facing_raise and not facing_bet:
        fail(f"{sid}: facing_raise=1 but facing_bet=False")

    # ---- 4. villain_aggression_count bounded by number of prior streets ----
    max_streets = max_prior_streets(street)
    v_agg = fd.get('villain_aggression_count', 0)
    if v_agg < 0:
        fail(f"{sid}: villain_aggression_count={v_agg} is negative")
    elif v_agg > max_streets:
        fail(
            f"{sid}: villain_aggression_count={v_agg} exceeds "
            f"max possible prior streets={max_streets} (street={street})"
        )
    else:
        ok(f"{sid}: villain_aggression_count={v_agg} in range [0,{max_streets}]")

    # ---- 5. villain_checked_back is binary ----
    vcb = fd.get('villain_checked_back', 0)
    if vcb not in (0, 1):
        fail(f"{sid}: villain_checked_back={vcb} is not 0 or 1")

    # ---- 6. villain_call_count bounded by prior streets ----
    vcc = fd.get('villain_call_count', 0)
    if vcc < 0 or vcc > max_streets:
        fail(
            f"{sid}: villain_call_count={vcc} out of range [0,{max_streets}]"
        )

    # ---- 7. num_callers_to_bet only non-zero when facing_bet ----
    ncb = fd.get('num_callers_to_bet', 0)
    if ncb > 0 and not facing_bet:
        fail(f"{sid}: num_callers_to_bet={ncb} but facing_bet=False")

    # ---- 8. Spot-check: villain position is set when facing_bet ----
    vp = fd.get('villain_position', None)
    hero_pos = fd.get('hero_position', None)
    if facing_bet and vp is None:
        warn(f"{sid}: facing_bet=True but villain_position not in feat_dict")
    if facing_bet and vp == hero_pos:
        fail(f"{sid}: villain_position == hero_position ({vp}) — wrong villain selected")


def verify_one_facing_bet_situation(situations: list):
    """Detailed printout for first facing_bet=True situation."""
    fb_sits = [s for s in situations if s.get('facing_bet')]
    if not fb_sits:
        print("\nNo facing_bet=True situations found — cannot do detailed spot-check.")
        return

    sit = fb_sits[0]
    fd = sit['feat_dict']
    print("\n--- Detailed spot-check: first facing_bet=True situation ---")
    print(f"  situation_id : {sit['situation_id']}")
    print(f"  street       : {sit['street']}")
    print(f"  hero_cards   : {sit['hero_cards']}")
    print(f"  board        : {sit['board']}")
    print(f"  hero_pos     : {sit['hero_position']}")
    print(f"  villain_pos  : {sit['villain_positions']}")
    print(f"  pot          : {sit['pot']}  to_call: {sit['to_call']}")
    print(f"  prior_actions: {sit.get('prior_actions', [])}")
    print()
    print(f"  facing_bet              : {fd.get('facing_bet')}")
    print(f"  facing_raise            : {fd.get('facing_raise')}")
    print(f"  villain_aggression_count: {fd.get('villain_aggression_count')}")
    print(f"  villain_checked_back    : {fd.get('villain_checked_back')}")
    print(f"  villain_call_count      : {fd.get('villain_call_count')}")
    print(f"  num_callers_to_bet      : {fd.get('num_callers_to_bet')}")
    print(f"  villain_position (code) : {fd.get('villain_position')}  "
          f"hero_position (code): {fd.get('hero_position')}")
    print(f"  oracle_action           : {sit.get('oracle_action')}")
    print(f"  adjusted_action         : {sit.get('adjusted_action')}")

    # Sanity: on the river, villain_aggression_count=0 yet checked_back=1 means
    # villain passive on prior streets — consistent with prior_actions showing
    # hero checked twice.
    v_agg = fd.get('villain_aggression_count', 0)
    vcb = fd.get('villain_checked_back', 0)
    if v_agg == 0 and vcb == 1:
        print("\n  INTERPRETATION: villain_aggression_count=0, villain_checked_back=1")
        print("  => Villain was passive on prior streets (checked at least once).")
        print("  => Current bet is villain's first aggression — facing_raise may be")
        print("     1 if raises_this_street > 0, else 0.")


def main():
    if not os.path.exists(os.path.normpath(JSONL)):
        print(f"ERROR: file not found: {JSONL}")
        sys.exit(1)

    situations = load_situations(JSONL)
    print(f"Loaded {len(situations)} situations from 3way_selected_200.jsonl\n")

    # Stats
    streets = {}
    fb_count = 0
    for s in situations:
        streets[s.get('street', '?')] = streets.get(s.get('street', '?'), 0) + 1
        if s.get('facing_bet'):
            fb_count += 1

    print(f"Distribution by street: {streets}")
    print(f"facing_bet=True: {fb_count} / {len(situations)}")
    print()

    # Run checks on all situations
    print("Running per-situation checks...")
    for i, sit in enumerate(situations):
        check_situation(sit, i)

    print()
    print(f"Results: {PASS} passed, {FAIL} failed, {WARNINGS} warnings")

    # Detailed spot-check
    verify_one_facing_bet_situation(situations)

    print()
    if FAIL == 0:
        print("ALL CHECKS PASSED — action history features look internally consistent.")
    else:
        print(f"FAILURES FOUND: {FAIL} checks failed. See FAIL lines above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
