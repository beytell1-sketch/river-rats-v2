#!/usr/bin/env python3
"""v2.3.2 self-play diagnostic — adapted from run_v231_selfplay_diagnostic.py.

Only difference from v2.3.1: MODEL_PATH + output filename. Same 110-feature
schema. Same anomaly watches + stop conditions per directive-o.
"""
import sys, os
# Reuse the v2.3.1 script's machinery by importing + patching
CORE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'river-rats-core')
sys.path.insert(0, CORE_DIR)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run_v231_selfplay_diagnostic as base

# Override paths for v2.3.2
base.MODEL_PATH = os.path.join(CORE_DIR, 'models', 'v2_3_1_model.json')

# Monkey-patch `main` to use v2.3.2 model and different output
_original_main = base.main

def main():
    # Swap model + output file names just by patching the names used inside
    base.MODEL_PATH = os.path.join(CORE_DIR, 'models', 'v2_3_2_model.json')
    # The raw_json path is constructed inline in base.main() — monkey-patch via
    # replacing the path right before base.main() writes. Simplest: rerun base.main
    # then rename the raw json file.
    rc = _original_main()

    # Rename output
    src = os.path.join(CORE_DIR, '..', 'review', 'v231_selfplay_raw.json')
    dst = os.path.join(CORE_DIR, '..', 'review', 'v232_selfplay_raw.json')
    if os.path.exists(src):
        os.rename(src, dst)
        print(f'Renamed {src} -> {dst}')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
