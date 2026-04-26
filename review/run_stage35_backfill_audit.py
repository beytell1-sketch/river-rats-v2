#!/usr/bin/env python3
"""Stage 3.5 M4 — distribution-shift audit on existing training rows.

Re-extracts villain composition features on training rows that carry
action_history (or can synthesize one). Compares pre-Stage-3.5 stored
values against post-Stage-3.5 re-extracted values. Expected:
  - Flop-only hands (no prior postflop action): near-zero shift
  - Multi-street hands: shifts expected, any direction

Reports:
  - Per-feature distribution shift (mean, median, max absolute delta)
  - Per-street breakdown (flop vs turn vs river decisions)
  - Isolation check: flop-only hands show ≤ 0.01 absolute delta on
    villain_top_pair_plus_pct / _medium_made_pct / _draw_pct / _air_pct

Phase 1 HIGH fix (Task 4.5): default output path is now timestamped
(`review/comms/RERUN_run_stage35_backfill_audit_<UTC-iso>.md`)
so re-running the script does NOT overwrite the committed 2026-04-20
baseline. Pass `--out <path>` to choose an explicit destination.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import statistics
import sys
from collections import defaultdict

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CORE = os.path.join(_REPO, 'river-rats-core')
if _CORE not in sys.path:
    sys.path.insert(0, _CORE)
os.chdir(_CORE)

from situation_factory import SituationSpec, build_situation  # noqa: E402


VILLAIN_COMP_FEATURES = [
    'villain_top_pair_plus_pct',
    'villain_medium_made_pct',
    'villain_draw_pct',
    'villain_air_pct',
    'villain_range_capped',
    'board_favour',
]

STREET_MAP = {0: 'flop', 1: 'turn', 2: 'river'}
POS_MAP = {0: 'UTG', 1: 'HJ', 2: 'CO', 3: 'BTN', 4: 'SB', 5: 'BB'}


def _parse_cards(s):
    if isinstance(s, list):
        return list(s)
    if isinstance(s, str) and s:
        return [s[i:i + 2] for i in range(0, len(s), 2)]
    return []


def _decode_street(v):
    if isinstance(v, str):
        m = v.lower()
        if m in ('f', 'flop'):
            return 'flop'
        if m in ('t', 'turn'):
            return 'turn'
        if m in ('r', 'river'):
            return 'river'
    if isinstance(v, (int, float)):
        return STREET_MAP.get(int(v), 'flop')
    return 'flop'


def _decode_pos(v):
    if isinstance(v, str):
        return v.upper()
    if isinstance(v, (int, float)):
        return POS_MAP.get(int(v), 'BTN')
    return 'BTN'


def _load_rows():
    """Load training rows with enough info to re-extract."""
    sources = [
        'training-data/pass1_final_labels_v23.jsonl',
        'training-data/v23_air_check_3way_labelled.jsonl',
        'training-data/v23_2_value_bet_3way_labelled.jsonl',
        'training-data/pass1_final_labels_v23_call.jsonl',
        'training-data/v23_pilot_labelled.jsonl',
    ]
    rows = []
    for src in sources:
        full_path = os.path.join(_REPO, src)
        if not os.path.exists(full_path):
            continue
        with open(full_path) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                hero = r.get('hero_cards') or r.get('_hero_cards')
                board = r.get('board_cards') or r.get('_board_cards')
                if isinstance(hero, list):
                    hero_cards = hero
                elif isinstance(hero, str):
                    hero_cards = _parse_cards(hero)
                else:
                    continue
                if isinstance(board, list):
                    board_cards = board
                elif isinstance(board, str):
                    board_cards = _parse_cards(board)
                else:
                    continue
                if len(hero_cards) != 2 or len(board_cards) < 3:
                    continue

                # Action history: prefer action_string (parseable); fallback
                # to prior_actions list if present. If neither usable, skip.
                action_history = r.get('_action_history')
                action_string = r.get('action_string', '')
                prior_actions = r.get('prior_actions', [])

                hero_pos = _decode_pos(
                    r.get('_hero_pos_raw') or r.get('hero_position')
                )
                villain_positions = r.get('villain_positions', [])
                if isinstance(villain_positions, str):
                    villain_positions = [villain_positions]
                if not villain_positions:
                    villain_positions = [
                        _decode_pos(r.get('_villain_pos_raw') or r.get('villain_position'))
                    ]

                # Skip rows where stored composition is None — those
                # files don't carry real pre-Stage-3.5 values and would
                # produce spurious "shifts" when compared against zeros.
                stored_tp = r.get('villain_top_pair_plus_pct')
                if stored_tp is None:
                    continue
                rows.append({
                    'source': os.path.basename(src),
                    'situation_id': r.get('situation_id', '?'),
                    'hero_cards': hero_cards,
                    'board_cards': board_cards,
                    'street': _decode_street(r.get('_street_raw') or r.get('street')),
                    'hero_pos': hero_pos,
                    'villain_positions': villain_positions,
                    'action_history': action_history,
                    'prior_actions': prior_actions,
                    'action_string': action_string,
                    'stored_tp_plus': stored_tp,
                    'stored_medium': r.get('villain_medium_made_pct', 0.0) or 0.0,
                    'stored_draw': r.get('villain_draw_pct', 0.0) or 0.0,
                    'stored_air': r.get('villain_air_pct', 0.0) or 0.0,
                    'stored_capped': r.get('villain_range_capped', 0) or 0,
                    'stored_board_favour': r.get('board_favour', 0.0) or 0.0,
                    'facing_bet': r.get('facing_bet', 0),
                    'raw': r,
                })
    return rows


def _synthesize_action_history(row):
    """Best-effort reconstruction of action_history.

    Two schemas supported:
    1. `prior_actions` list (test_set_50_labelled schema)
    2. Factory-generated rows (v23 buckets, air_check, value_bet) — these
       come from checked-through preflop+postflop sequences per the
       factory script. For decision on street N, reconstruct:
         preflop: opener raise + others call
         flop/turn (if before decision): all-check through
    """
    # Try schema 1 first
    prior = row.get('prior_actions', []) or []
    action_history = []
    for entry in prior:
        if not isinstance(entry, str) or ':' not in entry:
            continue
        street_part, action_part = entry.split(':', 1)
        tokens = action_part.strip().split()
        if len(tokens) >= 2:
            pos, act = tokens[0], tokens[1]
            action_history.append({
                'street': street_part.strip().lower(),
                'position': pos.upper(),
                'action': act.upper(),
            })
    if action_history:
        return action_history

    # Schema 2: factory-generated rows. Reconstruct implied history.
    # Heuristic: preflop opener raised, others called; all prior postflop
    # streets were checked-through (the v2.3.x air-CHECK / value-BET
    # factories use this pattern exclusively).
    hero_pos = row.get('hero_pos', 'BTN')
    villain_positions = row.get('villain_positions', [])
    decision_street = row.get('street', 'flop')

    # Opener is whoever would raise preflop — use hero_position as the
    # opener by default (matches factory convention); fall back to CO.
    opener = hero_pos if hero_pos in ('CO', 'BTN', 'HJ', 'UTG') else 'CO'
    active = list(villain_positions) + [hero_pos]

    action_history.append({
        'street': 'preflop', 'position': opener, 'action': 'RAISE',
    })
    for p in active:
        if p != opener:
            action_history.append({
                'street': 'preflop', 'position': p, 'action': 'CALL',
            })

    # Postflop all-check through prior streets (per factory convention)
    street_order = ['flop', 'turn', 'river']
    decision_idx = street_order.index(decision_street) if decision_street in street_order else 0
    for street in street_order[:decision_idx]:
        # All active players check in postflop order (lowest _PFO first)
        for p in active:
            action_history.append({
                'street': street, 'position': p, 'action': 'CHECK',
            })

    return action_history


def _rerun_feature_extraction(row):
    """Re-extract villain composition using SituationFactory path."""
    action_history = row.get('action_history') or _synthesize_action_history(row)

    # Compute opener from action_history (first RAISE in preflop)
    opener = None
    for a in action_history:
        if a.get('street') == 'preflop' and a.get('action') == 'RAISE':
            opener = a['position']
            break

    spec = SituationSpec(
        hero_cards=list(row['hero_cards']),
        board_cards=list(row['board_cards']),
        hero_pos=row['hero_pos'],
        villain_positions=list(row['villain_positions']),
        pot=90.0,  # placeholder; doesn't affect villain range
        to_call=0.0 if not row['facing_bet'] else 30.0,
        street=row['street'],
        action_history=[
            (a['street'], a['position'], a['action']) for a in action_history
        ],
        opener_position=opener,
        effective_stack=450.0,
        current_bet=0.0,
        num_opponents=len(row['villain_positions']),
    )
    try:
        feat_dict = build_situation(spec)
    except Exception as exc:
        return None, str(exc), action_history
    return feat_dict, None, action_history


def _default_report_path():
    """Phase 1 HIGH fix (Task 4.5): timestamped default so re-runs
    don't overwrite the immutable 2026-04-20 baseline."""
    ts = _dt.datetime.now(_dt.timezone.utc).strftime('%Y-%m-%dT%H-%M-%SZ')
    return os.path.join(
        _REPO, 'review', 'comms',
        f'RERUN_run_stage35_backfill_audit_{ts}.md',
    )


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description='Stage 3.5 M4 distribution-shift audit.',
    )
    parser.add_argument(
        '--out',
        default=None,
        help=(
            'Output report path. Defaults to a timestamped path under '
            'review/comms/ so re-runs preserve prior outputs (Phase 1 '
            'HIGH fix; the original 2026-04-20 file is no longer '
            'overwritten by default).'
        ),
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    report_path = args.out or _default_report_path()

    print('=' * 72)
    print('Stage 3.5 M4 — distribution-shift audit')
    print('=' * 72)

    rows = _load_rows()
    print(f'Loaded {len(rows)} training rows')

    per_row_deltas = []
    per_street_deltas = defaultdict(list)
    no_prior = 0  # rows without prior-postflop action (flop decisions)
    multi_street = 0
    build_failures = 0

    for r in rows:
        feat_dict, err, action_history = _rerun_feature_extraction(r)
        if err:
            build_failures += 1
            continue

        # Did this row have any prior-postflop action in history?
        has_prior_postflop = any(
            a.get('street') in ('flop', 'turn') and r['street'] != a.get('street')
            for a in action_history
        )
        if not has_prior_postflop and r['street'] == 'flop':
            no_prior += 1
        else:
            multi_street += 1

        def d(k_new, k_stored):
            new_val = float(feat_dict.get(k_new, 0.0) or 0.0)
            stored_val = float(r.get(k_stored, 0.0) or 0.0)
            return new_val - stored_val

        row_deltas = {
            'tp_plus': d('villain_top_pair_plus_pct', 'stored_tp_plus'),
            'medium':  d('villain_medium_made_pct', 'stored_medium'),
            'draw':    d('villain_draw_pct', 'stored_draw'),
            'air':     d('villain_air_pct', 'stored_air'),
        }
        per_row_deltas.append({
            'sid': r['situation_id'],
            'street': r['street'],
            'has_prior_postflop': has_prior_postflop,
            **row_deltas,
            'chain_steps': feat_dict.get('_villain_range_chain_steps', []),
        })
        per_street_deltas[r['street']].append(row_deltas)

    print(f'Build failures: {build_failures}')
    print(f'Flop-only rows (no prior postflop): {no_prior}')
    print(f'Multi-street rows: {multi_street}')
    print()

    def _stats(values):
        if not values:
            return None
        abs_v = [abs(v) for v in values]
        return {
            'n': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'max_abs': max(abs_v),
            'over_0_05': sum(1 for v in abs_v if v > 0.05),
        }

    # Report per-feature per-street
    print(f'{"feature":<10} {"street":<10} {"n":>5} {"mean_delta":>12} {"median_delta":>14} {"max_abs":>9} {"|d|>0.05":>9}')
    for feat in ('tp_plus', 'medium', 'draw', 'air'):
        for st in ('flop', 'turn', 'river'):
            vals = [row[feat] for row in per_street_deltas[st]]
            s = _stats(vals)
            if s:
                print(f'{feat:<10} {st:<10} {s["n"]:>5} {s["mean"]:>12.4f} '
                      f'{s["median"]:>14.4f} {s["max_abs"]:>9.4f} {s["over_0_05"]:>9}')

    print()

    # Isolation check: flop-only rows should show near-zero shift
    flop_only = [row for row in per_row_deltas
                 if row['street'] == 'flop' and not row['has_prior_postflop']]
    isolation_violations = []
    for row in flop_only:
        for feat in ('tp_plus', 'medium', 'draw', 'air'):
            if abs(row[feat]) > 0.01:
                isolation_violations.append({
                    'sid': row['sid'], 'feat': feat, 'delta': row[feat],
                })

    print(f'Isolation check — flop-only rows (n={len(flop_only)}):')
    print(f'  Violations (|delta| > 0.01 on any composition feature): '
          f'{len(isolation_violations)}')
    if isolation_violations[:5]:
        for v in isolation_violations[:5]:
            print(f'    [{v["sid"]}] {v["feat"]}: delta {v["delta"]:+.4f}')

    # Multi-street rows should generally show SOME chain_steps activity
    multi_with_chain = sum(
        1 for row in per_row_deltas
        if row['has_prior_postflop'] and row['chain_steps']
    )
    print()
    print(f'Multi-street rows with chain_steps > 0: {multi_with_chain}')
    print(f'Multi-street rows total: {multi_street}')
    print()

    # Write report
    # Phase 1 HIGH fix (Task 4.5): `report_path` from `--out` flag with
    # timestamped default; original 04-20 baseline preserved on disk.
    with open(report_path, 'w') as f:
        f.write(f"""---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 3.5 M4 — distribution-shift audit on existing training rows
status: AUDIT COMPLETE
---

# Stage 3.5 M4 — Distribution-Shift Audit

Re-extracted villain composition features on existing training rows
using the new action-aware chained narrowing. Compared against
stored pre-Stage-3.5 values.

## Coverage

```
Total training rows loaded: {len(rows)}
Build failures:             {build_failures}
Flop-only rows:             {no_prior}
Multi-street rows:          {multi_street}
```

## Per-feature distribution shift

| feature | street | n | mean_delta | median_delta | max_abs | |delta| > 0.05 |
|---|---|---|---|---|---|---|
""")
        for feat in ('tp_plus', 'medium', 'draw', 'air'):
            for st in ('flop', 'turn', 'river'):
                vals = [row[feat] for row in per_street_deltas[st]]
                s = _stats(vals)
                if s:
                    f.write(
                        f'| {feat} | {st} | {s["n"]} | {s["mean"]:+.4f} | '
                        f'{s["median"]:+.4f} | {s["max_abs"]:.4f} | {s["over_0_05"]} |\n'
                    )

        f.write(f"""

## Isolation check (flop-only rows should not shift)

Flop-only rows (n={len(flop_only)}) — should have ≤ 0.01 absolute
delta on composition features per GTO review Q2 (same-street
actions excluded from chain).

Isolation violations (|delta| > 0.01 on any composition feature):
{len(isolation_violations)} / {len(flop_only)} rows

""")
        if isolation_violations:
            f.write('First 10 violations:\n\n')
            for v in isolation_violations[:10]:
                f.write(f'- `{v["sid"]}` on `{v["feat"]}`: delta {v["delta"]:+.4f}\n')
        else:
            f.write('**CLEAN** — zero violations. Same-street exclusion '
                   'working as specified.\n')

        f.write(f"""

## Chain activity verification

Multi-street rows with non-empty `chain_steps`:
{multi_with_chain} / {multi_street}

If this ratio is high (>80%), chain is firing as designed on
multi-street hands. If low, action_history plumbing isn't reaching
these rows — investigate.

## Acceptable shift thresholds

Per spec lock (a4cab83):
- Flop-only rows: near-zero (< 0.01 absolute) — PASS IFF violations == 0
- Multi-street rows: any direction acceptable, any magnitude
""")

    print(f'Report written: {report_path}')
    print()
    print('=' * 72)
    pass_isolation = len(isolation_violations) == 0
    print(f'Stage 3.5 M4 audit: '
          f'{"PASS" if pass_isolation else "FAIL — isolation violations found"}')
    return 0 if pass_isolation else 1


if __name__ == '__main__':
    raise SystemExit(main())
