#!/usr/bin/env python3
"""Evaluate oracle variants against the 50-hand expert reference set.

Usage:
    python3 run_eval.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from reference_evaluator import evaluate_variants, format_eval_report
from self_play import Variant
from multiway_adjuster import get_default_params


def main():
    base_params = get_default_params()

    variants = [
        Variant(
            name="baseline",
            params=base_params,
            rationale="Current calibration — the control",
        ),
        Variant(
            name="baseline_draw_fix",
            params={**base_params,
                    'rule1_draw_bypass': 5,
                    'draw_outs_ip_base': 6,
                    'rule5_draw_bypass': 5},
            rationale="Baseline + draw bypass 5/6/5 only",
        ),
        Variant(
            name="loose_draws_oop",
            params={**base_params,
                    'rule1_draw_bypass': 5,
                    'draw_outs_ip_base': 6,
                    'rule5_draw_bypass': 5,
                    'equity_realization_oop': 0.75},
            rationale="Draw fix + OOP discount 0.75",
        ),
    ]

    print("Evaluating 3 variants against 40 expert-labelled hands...\n")

    report = evaluate_variants(variants)
    print(format_eval_report(report))


if __name__ == '__main__':
    main()
