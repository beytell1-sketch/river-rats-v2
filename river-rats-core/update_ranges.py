#!/usr/bin/env python3
"""Update range_manager.py with new GTO range data.

This script reads the approved new_range_data.py and patches
range_manager.py in place. Run once, verify, then delete this script.

Usage:
    python3 update_ranges.py
    python3 -m pytest tests/ --tb=short  # verify
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'review'))

from new_range_data import RFI, THREE_BET, CALL


def format_dict(d, indent=8):
    """Format a hand:freq dict as Python source code."""
    lines = []
    items = sorted(d.items(), key=lambda x: (-x[1], x[0]))
    for hand, freq in items:
        if freq == 1.0:
            lines.append(f'{" " * indent}"{hand}": 1.0,')
        else:
            lines.append(f'{" " * indent}"{hand}": {freq},')
    return '\n'.join(lines)


def build_rfi_source():
    """Build Python source for the RFI dict."""
    lines = ['RFI = {']
    for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB']:
        lines.append(f"    '{pos}': {{")
        lines.append(format_dict(RFI[pos]))
        lines.append('    },')
        lines.append('')
    # Aliases
    lines.append("}")
    lines.append("RFI['MP'] = RFI['HJ']")
    lines.append("RFI['EP'] = RFI['UTG']")
    return '\n'.join(lines)


def build_threeb_source(varname='THREEB'):
    """Build Python source for the THREE_BET/THREEB dict."""
    lines = [f'{varname} = {{']
    for pos in sorted(THREE_BET.keys()):
        lines.append(f"    '{pos}': {{")
        for vs in sorted(THREE_BET[pos].keys()):
            lines.append(f"        '{vs}': {{")
            lines.append(format_dict(THREE_BET[pos][vs], indent=12))
            lines.append('        },')
        lines.append('    },')
        lines.append('')
    lines.append('}')
    # Aliases
    aliases = [
        (f"{varname}['BB']['vs_MP']", f"{varname}['BB']['vs_HJ']"),
        (f"{varname}['BB']['vs_EP']", f"{varname}['BB']['vs_UTG']"),
        (f"{varname}['SB']['vs_MP']", f"{varname}['SB']['vs_HJ']"),
        (f"{varname}['SB']['vs_EP']", f"{varname}['SB']['vs_UTG']"),
        (f"{varname}['BTN']['vs_MP']", f"{varname}['BTN']['vs_HJ']"),
        (f"{varname}['BTN']['vs_EP']", f"{varname}['BTN']['vs_UTG']"),
        (f"{varname}['CO']['vs_MP']", f"{varname}['CO']['vs_HJ']"),
        (f"{varname}['CO']['vs_EP']", f"{varname}['CO']['vs_UTG']"),
    ]
    for lhs, rhs in aliases:
        # Only add if the source key exists
        src_pos = rhs.split("'")[1]
        src_vs = rhs.split("'")[3]
        if src_pos in THREE_BET and src_vs in THREE_BET[src_pos]:
            lines.append(f"{lhs} = {rhs}")
    return '\n'.join(lines)


def build_call_source():
    """Build Python source for the CALL dict."""
    lines = ['CALL = {']
    for pos in sorted(CALL.keys()):
        lines.append(f"    '{pos}': {{")
        for vs in sorted(CALL[pos].keys()):
            lines.append(f"        '{vs}': {{")
            lines.append(format_dict(CALL[pos][vs], indent=12))
            lines.append('        },')
        lines.append('    },')
        lines.append('')
    lines.append('}')
    # Aliases
    aliases = [
        ("CALL['BB']['vs_MP']", "CALL['BB']['vs_HJ']"),
        ("CALL['BB']['vs_EP']", "CALL['BB']['vs_UTG']"),
        ("CALL['BTN']['vs_MP']", "CALL['BTN']['vs_HJ']"),
        ("CALL['BTN']['vs_EP']", "CALL['BTN']['vs_UTG']"),
    ]
    for lhs, rhs in aliases:
        src_pos = rhs.split("'")[1]
        src_vs = rhs.split("'")[3]
        if src_pos in CALL and src_vs in CALL[src_pos]:
            lines.append(f"{lhs} = {rhs}")
    # Note: SB, CO, HJ have no CALL entries (3-bet-or-fold)
    lines.append("# SB, CO, HJ: 3-bet-or-fold. No CALL entries.")
    return '\n'.join(lines)


if __name__ == '__main__':
    print("Generating updated range source code...")
    print()

    rfi_src = build_rfi_source()
    threeb_src = build_threeb_source('THREEB')
    three_bet_src = build_threeb_source('THREE_BET')
    call_src = build_call_source()

    # Count hands for verification
    from new_range_data import _count_combos

    print("RFI verification:")
    for pos in ['UTG', 'HJ', 'CO', 'BTN', 'SB']:
        c = _count_combos(RFI[pos])
        print(f"  {pos}: {len(RFI[pos])} hands, {c:.0f} combos, {100*c/1326:.1f}%")

    print("\nTHREEB verification:")
    for pos in sorted(THREE_BET):
        for vs in sorted(THREE_BET[pos]):
            c = _count_combos(THREE_BET[pos][vs])
            print(f"  {pos} {vs}: {c:.0f} combos ({100*c/1326:.1f}%)")

    print("\nCALL verification:")
    for pos in sorted(CALL):
        for vs in sorted(CALL[pos]):
            c = _count_combos(CALL[pos][vs])
            print(f"  {pos} {vs}: {c:.0f} combos ({100*c/1326:.1f}%)")

    # Write to output files for manual review
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'review')
    with open(os.path.join(out_dir, 'rfi_source.py'), 'w') as f:
        f.write(rfi_src)
    with open(os.path.join(out_dir, 'threeb_source.py'), 'w') as f:
        f.write(threeb_src)
    with open(os.path.join(out_dir, 'three_bet_source.py'), 'w') as f:
        f.write(three_bet_src)
    with open(os.path.join(out_dir, 'call_source.py'), 'w') as f:
        f.write(call_src)

    print(f"\nSource code written to {out_dir}/")
    print("Manually replace the corresponding sections in range_manager.py")
