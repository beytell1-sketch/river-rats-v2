"""
assemble_pilot_data.py — Pilot data assembly script.

Reads /tmp/pilot_situations.json and /tmp/pilot_v2_consensus.json,
merges with hardcoded ATTENTION_LEVELS and INTENTION_TAGS tables,
writes pilot_20_enriched.jsonl (canonical JSONL) and four CSV files,
and prints a verification summary.

Run from: repo root.
    python3 river-rats-core/assemble_pilot_data.py

Blueprint: BLUEPRINT_FEATURE_ATTENTION_TRAINING_2026-04-14.md
"""

import sys
import os
import json
import csv

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from gto_model import FEATURE_COLUMNS, ACTION_CLASSES

# ═══════════════════════════════════════════════════════════════════
# MODULE-LEVEL CONSTANTS
# ═══════════════════════════════════════════════════════════════════

PILOT_SITUATIONS_PATH  = '/tmp/pilot_situations.json'
PILOT_CONSENSUS_PATH   = '/tmp/pilot_v2_consensus.json'
TAG_VOCAB_PATH         = 'training-data/tag_vocabulary.json'
UNTAGGED_FEATURES_PATH = 'review/comms/PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt'
ENRICHED_JSONL_PATH    = 'training-data/pilot_20_enriched.jsonl'
BASE_CSV_PATH          = 'training-data/pilot_20_base.csv'
ATTENTION_CSV_PATH     = 'training-data/pilot_20_attention.csv'
LEVELS_CSV_PATH        = 'training-data/pilot_20_attention_levels.csv'
INTENTIONS_CSV_PATH    = 'training-data/pilot_20_intentions.csv'

LEVEL_WEIGHTS = {
    'PRIMARY':   1.0,
    'CONFIRMED': 0.7,
    'DISCOVERED': 0.5,
    'Untagged':  0.1,
}

# ═══════════════════════════════════════════════════════════════════
# ATTENTION_LEVELS
#
# Hardcoded from the pilot v2 run report.
# Keys: situation_id strings (all 20).
# Values: dict mapping feature_name -> level_string.
#
# Assignment hierarchy (blueprint Section 2a):
# - PRIMARY: primary decision drivers cited in pilot report reasoning
#   (equity_vs_range, villain composition pcts on BET/RAISE/CALL/FOLD hands)
# - CONFIRMED: mandatory composition features + bucket-specific features
#   (draw_outs, improvement_probability for drawing hands; is_made_hand etc.)
# - DISCOVERED: discovery team features
#   (villain_fold_equity_estimate, spr, villain_checked_back, connectivity_score,
#    is_preflop_aggressor, overcard_outs, flush_draw_rank, board_favour,
#    straight_danger, is_paired, flush_block_pct, flush_danger)
#
# CHECK hands NOT facing a bet: composition features (villain_*_pct) are untagged
# and must NOT appear in PRIMARY or CONFIRMED for those hands.
#
# Any feature in this dict for a hand must NOT appear in that hand's untagged list.
# ═══════════════════════════════════════════════════════════════════

ATTENTION_LEVELS = {

    # ── d4534_BB_flop | CHECK | strong_made ─────────────────────────
    # Tagged (18): board_favour, danger_score, equity_vs_range, flush_danger,
    #   hero_range_percentile, improvement_probability, is_ip, is_preflop_aggressor,
    #   is_strong_made, is_two_tone, spr, villain_aggression_count,
    #   villain_air_pct, villain_draw_pct, villain_medium_made_pct,
    #   villain_position, villain_top_pair_plus_pct
    # CHECK hand not facing bet — composition pcts ARE tagged here (d4534 differs
    #   from other CHECK hands: villain already showed aggression, so teams looked
    #   at composition to determine why checking is right with a strong made hand)
    # villain_fold_equity_estimate is listed as untagged for this hand
    'villan_checked_back': 'DISCOVERED',  # placeholder — replaced per hand below
    'd4534_BB_flop': {
        'equity_vs_range':           'PRIMARY',
        'is_strong_made':            'PRIMARY',
        'villain_top_pair_plus_pct': 'PRIMARY',
        'villain_draw_pct':          'PRIMARY',
        'villain_air_pct':           'PRIMARY',
        'villain_medium_made_pct':   'CONFIRMED',
        'hero_range_percentile':     'CONFIRMED',
        'villain_aggression_count':  'CONFIRMED',
        'villain_position':          'CONFIRMED',
        'danger_score':              'DISCOVERED',
        'flush_danger':              'DISCOVERED',
        'is_ip':                     'DISCOVERED',
        'is_preflop_aggressor':      'DISCOVERED',
        'is_two_tone':               'DISCOVERED',
        'spr':                       'DISCOVERED',
        'board_favour':              'DISCOVERED',
        'improvement_probability':   'DISCOVERED',
        'has_showdown_value':        'CONFIRMED',
    },

    # ── d7760_BTN_flop | CHECK | air ────────────────────────────────
    # Tagged (18): board_favour, draw_outs, equity_vs_range, flush_danger,
    #   hero_range_percentile, improvement_probability, is_ip, is_made_hand,
    #   is_preflop_aggressor, num_opponents, overcard_outs,
    #   villain_air_pct, villain_draw_pct, villain_fold_equity_estimate,
    #   villain_medium_made_pct, villain_top_pair_plus_pct, worse_hand_pct
    # CHECK hand, air — composition pcts tagged because need to understand air % check
    'd7760_BTN_flop': {
        'equity_vs_range':              'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'is_made_hand':                 'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'draw_outs':                    'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'overcard_outs':                'DISCOVERED',
        'num_opponents':                'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
        'flush_danger':                 'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'villain_fold_equity_estimate': 'DISCOVERED',
    },

    # ── d6384_BTN_turn | CHECK | air ────────────────────────────────
    # Tagged (17): connectivity_score, danger_score, equity_vs_range,
    #   flush_block_pct, hero_range_percentile, improvement_probability,
    #   is_ip, overcard_outs, spr, straight_danger,
    #   villain_air_pct, villain_checked_back, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct, villain_top_pair_plus_pct
    # Note: computed tagged set had 17 items including all these
    'd6384_BTN_turn': {
        'equity_vs_range':              'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'overcard_outs':                'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'villain_checked_back':         'DISCOVERED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'flush_block_pct':              'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
    },

    # ── d6066_BB_flop | CHECK | monster ─────────────────────────────
    # Tagged (17): connectivity_score, danger_score, equity_vs_range,
    #   has_showdown_value, hero_range_percentile, improvement_probability,
    #   is_ip, is_monster, is_preflop_aggressor, spr, straight_danger,
    #   villain_aggression_count, villain_air_pct, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct, villain_top_pair_plus_pct
    'd6066_BB_flop': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'villain_aggression_count':     'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
    },

    # ── d5046_CO_flop | BET | monster ───────────────────────────────
    # Tagged (17): board_favour, danger_score, equity_vs_range,
    #   hero_range_percentile, is_ip, is_monster, is_paired, is_preflop_aggressor,
    #   overcard_outs, spr, villain_air_pct, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct, worse_hand_pct
    'd5046_CO_flop': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_paired':                    'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
    },

    # ── d6826_CO_turn | BET | monster ───────────────────────────────
    # Tagged (18): better_hand_pct, connectivity_score, equity_vs_range,
    #   hero_range_percentile, is_ip, is_monster, is_paired, is_preflop_aggressor,
    #   spr, straight_danger, villain_air_pct, villain_checked_back,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_range_capped, villain_top_pair_plus_pct, worse_hand_pct
    'd6826_CO_turn': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_range_capped':         'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_paired':                    'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
    },

    # ── d1971_HJ_river | BET | strong_made ──────────────────────────
    # Tagged (18): better_hand_pct, board_favour, danger_score, equity_vs_range,
    #   flush_danger, flush_draw_rank, hand_category, hero_range_percentile,
    #   is_ip, is_paired, villain_air_pct, villain_checked_back,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_range_capped, villain_top_pair_plus_pct, worse_hand_pct
    'd1971_HJ_river': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_range_capped':         'CONFIRMED',
        'hand_category':                'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'flush_draw_rank':              'DISCOVERED',
        'flush_danger':                 'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_paired':                    'DISCOVERED',
    },

    # ── d2285_BTN_river | FOLD | air ────────────────────────────────
    # Tagged (15): board_favour, equity_vs_range, facing_raise, has_showdown_value,
    #   hero_range_percentile, is_ip, is_paired, overcard_outs, pot_odds,
    #   villain_air_pct, villain_checked_back, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct, villain_top_pair_plus_pct
    'd2285_BTN_river': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'facing_raise':                 'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_paired':                    'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
    },

    # ── d6533_BTN_river | FOLD | weak_made ──────────────────────────
    # Tagged (15): better_hand_pct, equity_vs_range, facing_raise, flush_danger,
    #   flush_draw_rank, has_showdown_value, hero_range_percentile, is_ip,
    #   pot_odds, straight_danger, villain_air_pct, villain_checked_back,
    #   villain_draw_pct, villain_medium_made_pct, villain_top_pair_plus_pct
    'd6533_BTN_river': {
        'equity_vs_range':           'PRIMARY',
        'villain_top_pair_plus_pct': 'PRIMARY',
        'villain_draw_pct':          'PRIMARY',
        'villain_air_pct':           'PRIMARY',
        'villain_medium_made_pct':   'CONFIRMED',
        'hero_range_percentile':     'CONFIRMED',
        'has_showdown_value':        'CONFIRMED',
        'pot_odds':                  'CONFIRMED',
        'better_hand_pct':           'CONFIRMED',
        'villain_checked_back':      'DISCOVERED',
        'facing_raise':              'DISCOVERED',
        'flush_draw_rank':           'DISCOVERED',
        'flush_danger':              'DISCOVERED',
        'straight_danger':           'DISCOVERED',
        'is_ip':                     'DISCOVERED',
    },

    # ── d1200_HJ_turn | FOLD | air ───────────────────────────────────
    # Tagged (20): connectivity_score, danger_score, equity_vs_range, facing_raise,
    #   has_showdown_value, hero_range_percentile, improvement_probability,
    #   is_ip, is_preflop_aggressor, overcard_outs, pot_odds, straight_danger,
    #   villain_air_pct, villain_call_count, villain_checked_back,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_range_capped, villain_top_pair_plus_pct
    'd1200_HJ_turn': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'villain_range_capped':         'CONFIRMED',
        'villain_call_count':           'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'facing_raise':                 'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
    },

    # ── BP1_22 | CALL | drawing ─────────────────────────────────────
    # Tagged (19): draw_outs, equity_margin, equity_vs_range, flush_block_pct,
    #   flush_draw_rank, has_flush_draw, has_straight_draw, hero_range_percentile,
    #   improvement_probability, is_ip, overcard_outs, pot_odds, spr,
    #   villain_air_pct, villain_draw_pct, villain_fold_equity_estimate,
    #   villain_medium_made_pct, villain_range_capped, villain_top_pair_plus_pct
    'BP1_22': {
        'equity_vs_range':              'PRIMARY',
        'has_flush_draw':               'PRIMARY',
        'draw_outs':                    'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'improvement_probability':      'CONFIRMED',
        'equity_margin':                'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_straight_draw':            'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_range_capped':         'DISCOVERED',
        'spr':                          'DISCOVERED',
        'flush_draw_rank':              'DISCOVERED',
        'flush_block_pct':              'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
        'is_ip':                        'DISCOVERED',
    },

    # ── BP2_35 | RAISE | monster ─────────────────────────────────────
    # Tagged (19): better_hand_pct, connectivity_score, danger_score, equity_vs_range,
    #   facing_bet, hero_range_percentile, is_ip, is_monster, is_rainbow,
    #   num_callers_to_bet, pot_odds, spr, villain_air_pct, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct, villain_range_capped,
    #   villain_top_pair_plus_pct, worse_hand_pct
    'BP2_35': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'facing_bet':                   'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_range_capped':         'CONFIRMED',
        'num_callers_to_bet':           'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_rainbow':                   'DISCOVERED',
        'pot_odds':                     'DISCOVERED',
    },

    # ── BP3_03 | FOLD | air ──────────────────────────────────────────
    # Tagged (18): better_hand_pct, draw_outs, equity_vs_range, has_showdown_value,
    #   has_straight_draw, hero_range_percentile, improvement_probability, is_ip,
    #   is_preflop_aggressor, is_two_tone, overcard_outs, pot_odds,
    #   villain_air_pct, villain_draw_pct, villain_fold_equity_estimate,
    #   villain_medium_made_pct, villain_top_pair_plus_pct, worse_hand_pct
    'BP3_03': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'is_two_tone':                  'DISCOVERED',
        'draw_outs':                    'DISCOVERED',
        'has_straight_draw':            'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
    },

    # ── BP4_28 | BET | strong_made ───────────────────────────────────
    # Tagged (18): better_hand_pct, board_favour, connectivity_score, danger_score,
    #   equity_vs_range, hero_range_percentile, is_ip, is_preflop_aggressor,
    #   is_strong_made, spr, straight_danger, villain_air_pct, villain_checked_back,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct, worse_hand_pct
    'BP4_28': {
        'equity_vs_range':              'PRIMARY',
        'is_strong_made':               'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
    },

    # ── BP5_02 | CHECK | monster ─────────────────────────────────────
    # Tagged (17): board_favour, danger_score, equity_vs_range, flush_danger,
    #   hero_range_percentile, is_ip, is_monster, is_preflop_aggressor, spr,
    #   villain_aggression_count, villain_air_pct, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct, villain_range_capped,
    #   villain_top_pair_plus_pct
    # Note: 17 tagged. villain_air_pct etc. tagged because monster check — looking at
    #   composition to justify NOT betting (pot_control decision)
    'BP5_02': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'villain_aggression_count':     'CONFIRMED',
        'villain_range_capped':         'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'flush_danger':                 'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'has_showdown_value':           'CONFIRMED',
    },

    # ── BP6_01 | RAISE | drawing ─────────────────────────────────────
    # Tagged (18): board_favour, danger_score, draw_outs, equity_vs_range,
    #   flush_block_pct, flush_draw_rank, hero_range_percentile, improvement_probability,
    #   is_ip, is_monotone, overcard_outs, pot_odds, spr, villain_air_pct,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct
    'BP6_01': {
        'equity_vs_range':              'PRIMARY',
        'draw_outs':                    'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'improvement_probability':      'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'flush_draw_rank':              'DISCOVERED',
        'flush_block_pct':              'DISCOVERED',
        'spr':                          'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_monotone':                  'DISCOVERED',
    },

    # ── BP7_03 | CALL | drawing ──────────────────────────────────────
    # Tagged (17): draw_outs, equity_margin, equity_vs_range, flush_block_pct,
    #   flush_draw_rank, hero_range_percentile, improvement_probability, is_ip,
    #   overcard_outs, pot_odds, spr, villain_aggression_count, villain_air_pct,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct
    'BP7_03': {
        'equity_vs_range':              'PRIMARY',
        'draw_outs':                    'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'improvement_probability':      'CONFIRMED',
        'equity_margin':                'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_aggression_count':     'DISCOVERED',
        'spr':                          'DISCOVERED',
        'flush_draw_rank':              'DISCOVERED',
        'flush_block_pct':              'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
        'is_ip':                        'DISCOVERED',
    },

    # ── BP2_36 | RAISE | monster ─────────────────────────────────────
    # Tagged (19): better_hand_pct, board_favour, connectivity_score, danger_score,
    #   equity_vs_range, facing_bet, hero_range_percentile, is_ip, is_preflop_aggressor,
    #   pot_odds, spr, straight_danger, villain_aggression_count, villain_air_pct,
    #   villain_draw_pct, villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct, worse_hand_pct
    'BP2_36': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'facing_bet':                   'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_aggression_count':     'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'pot_odds':                     'DISCOVERED',
    },

    # ── BP2_42 | FOLD | air ──────────────────────────────────────────
    # Tagged (18): board_favour, connectivity_score, equity_vs_range, has_showdown_value,
    #   hero_range_percentile, high_card_rank, improvement_probability, is_ip,
    #   overcard_outs, pot_odds, straight_danger, villain_air_pct, villain_call_count,
    #   villain_checked_back, villain_draw_pct, villain_fold_equity_estimate,
    #   villain_medium_made_pct, villain_top_pair_plus_pct
    'BP2_42': {
        'equity_vs_range':              'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'has_showdown_value':           'CONFIRMED',
        'pot_odds':                     'CONFIRMED',
        'villain_call_count':           'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'villain_checked_back':         'DISCOVERED',
        'connectivity_score':           'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'straight_danger':              'DISCOVERED',
        'high_card_rank':               'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'improvement_probability':      'DISCOVERED',
        'overcard_outs':                'DISCOVERED',
    },

    # ── BP5_05 | BET | monster ───────────────────────────────────────
    # Tagged (17): better_hand_pct, board_favour, danger_score, equity_vs_range,
    #   flush_danger, hero_range_percentile, is_ip, is_monster, is_preflop_aggressor,
    #   is_two_tone, spr, villain_air_pct, villain_draw_pct,
    #   villain_fold_equity_estimate, villain_medium_made_pct,
    #   villain_top_pair_plus_pct, worse_hand_pct
    'BP5_05': {
        'equity_vs_range':              'PRIMARY',
        'is_monster':                   'PRIMARY',
        'villain_top_pair_plus_pct':    'PRIMARY',
        'villain_draw_pct':             'PRIMARY',
        'villain_air_pct':              'PRIMARY',
        'villain_medium_made_pct':      'CONFIRMED',
        'hero_range_percentile':        'CONFIRMED',
        'better_hand_pct':              'CONFIRMED',
        'worse_hand_pct':               'CONFIRMED',
        'villain_fold_equity_estimate': 'DISCOVERED',
        'flush_danger':                 'DISCOVERED',
        'board_favour':                 'DISCOVERED',
        'danger_score':                 'DISCOVERED',
        'spr':                          'DISCOVERED',
        'is_ip':                        'DISCOVERED',
        'is_preflop_aggressor':         'DISCOVERED',
        'is_two_tone':                  'DISCOVERED',
    },
}

# Remove the stray placeholder key
del ATTENTION_LEVELS['villan_checked_back']

# ═══════════════════════════════════════════════════════════════════
# INTENTION_TAGS
#
# Hardcoded from pilot v2 report consensus reasoning.
# Keys: situation_id strings (all 20).
# Values: list of 1-3 tag strings from tag_vocabulary.json "intentions".
# ═══════════════════════════════════════════════════════════════════

INTENTION_TAGS = {
    'd4534_BB_flop':  ['pot_control'],
    'd7760_BTN_flop': ['pot_control'],
    'd6384_BTN_turn': ['pot_control'],
    'd6066_BB_flop':  ['pot_control'],
    'd5046_CO_flop':  ['value_extract', 'deny_equity'],
    'd6826_CO_turn':  ['value_extract'],
    'd1971_HJ_river': ['value_extract'],
    'd2285_BTN_river': ['range_fold_priced_out'],
    'd6533_BTN_river': ['range_fold_priced_out'],
    'd1200_HJ_turn':  ['range_fold_priced_out'],
    'BP1_22':  ['continue_draw'],
    'BP2_35':  ['value_extract', 'deny_equity'],
    'BP3_03':  ['range_fold_priced_out'],
    'BP4_28':  ['value_extract', 'deny_equity'],
    'BP5_02':  ['pot_control'],
    'BP6_01':  ['bluff_fold_better', 'continue_draw'],
    'BP7_03':  ['continue_draw'],
    'BP2_36':  ['value_extract'],
    'BP2_42':  ['range_fold_priced_out'],
    'BP5_05':  ['value_extract'],
}


# ═══════════════════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def load_pilot_sources() -> tuple:
    """
    Reads pilot_situations.json and pilot_v2_consensus.json.
    Returns (situations_list, consensus_dict).
    Raises FileNotFoundError, ValueError on missing or invalid data.
    """
    if not os.path.exists(PILOT_SITUATIONS_PATH):
        raise FileNotFoundError(f"Missing: {PILOT_SITUATIONS_PATH}")
    if not os.path.exists(PILOT_CONSENSUS_PATH):
        raise FileNotFoundError(f"Missing: {PILOT_CONSENSUS_PATH}")

    with open(PILOT_SITUATIONS_PATH) as f:
        situations = json.load(f)
    with open(PILOT_CONSENSUS_PATH) as f:
        consensus = json.load(f)

    if len(situations) != 20:
        raise ValueError(f"Expected 20 situations, got {len(situations)}")

    action_set = set(ACTION_CLASSES)
    for s in situations:
        sid = s['situation_id']
        if sid not in consensus:
            raise ValueError(f"situation_id '{sid}' not found in consensus dict")
        if consensus[sid] not in action_set:
            raise ValueError(f"Invalid consensus action '{consensus[sid]}' for '{sid}'")

    return situations, consensus


def parse_untagged_features_file(path: str) -> dict:
    """
    Parses PILOT_V2_UNTAGGED_FEATURES_2026-04-14.txt.
    Returns dict mapping situation_id -> set of untagged feature names.

    File format: lines starting with "--- HAND_ID |" begin a new block.
    Within each block, lines with "  FEATURE_NAME  =  VALUE" are feature lines.

    Raises ValueError if dict does not contain exactly 20 keys, or if any
    parsed feature name is not in FEATURE_COLUMNS.
    """
    fc_set = set(FEATURE_COLUMNS)
    result = {}
    current_hand = None

    # Hero/villain position display names are not feature names; the file
    # shows hero_position and villain_position with display values but
    # those ARE feature names in FEATURE_COLUMNS. We parse the key (left side).
    # However "hero_position" and "villain_position" ARE in FEATURE_COLUMNS.
    # The blueprint note says these have "display values" in the file but the
    # feature names (keys) do match FEATURE_COLUMNS. So include them.

    with open(path) as f:
        for line in f:
            # Detect hand block header
            stripped = line.strip()
            if stripped.startswith('---') and '|' in stripped:
                # Format: "--- HAND_ID | ..."
                parts = stripped.lstrip('- ').split('|')
                current_hand = parts[0].strip()
                result[current_hand] = set()
                continue

            # Detect feature lines: start with spaces then FEATURE_NAME = VALUE
            if current_hand is not None and line.startswith('  ') and '=' in line:
                # Extract feature name: everything before the first whitespace group
                content = line.lstrip()
                feat_name = content.split()[0]
                # Only include if it's a valid feature column
                if feat_name in fc_set:
                    result[current_hand].add(feat_name)

    if len(result) != 20:
        raise ValueError(f"Expected 20 hand blocks, parsed {len(result)}")

    # Validate all parsed names
    for hand_id, feat_set in result.items():
        for fname in feat_set:
            if fname not in fc_set:
                raise ValueError(f"Unknown feature '{fname}' in hand '{hand_id}'")

    return result


def validate_attention_levels(untagged_map: dict) -> None:
    """
    Cross-validates the hardcoded ATTENTION_LEVELS against the parsed untagged map.
    Raises ValueError with descriptive message on first violation found.
    Prints success message on pass.
    """
    fc_set = set(FEATURE_COLUMNS)
    valid_levels = {'PRIMARY', 'CONFIRMED', 'DISCOVERED'}
    n_validated = 0

    for situation_id, feat_level_map in ATTENTION_LEVELS.items():
        hand_untagged = untagged_map.get(situation_id, set())
        for feat_name, level in feat_level_map.items():
            if feat_name not in fc_set:
                raise ValueError(
                    f"ATTENTION_LEVELS[{situation_id!r}][{feat_name!r}]: "
                    f"feature not in FEATURE_COLUMNS"
                )
            if feat_name in hand_untagged:
                raise ValueError(
                    f"ATTENTION_LEVELS[{situation_id!r}][{feat_name!r}]: "
                    f"feature is tagged PRIMARY/CONFIRMED/DISCOVERED but also "
                    f"appears in untagged_map (conflict)"
                )
            if level not in valid_levels:
                raise ValueError(
                    f"ATTENTION_LEVELS[{situation_id!r}][{feat_name!r}]: "
                    f"invalid level '{level}' (must be PRIMARY/CONFIRMED/DISCOVERED)"
                )
            n_validated += 1

    print(f"ATTENTION_LEVELS: OK — {n_validated} feature-level assignments validated")


def validate_intention_tags(vocab: dict) -> None:
    """
    Validates the hardcoded INTENTION_TAGS table against the tag vocabulary.
    vocab: the "intentions" sub-dict from tag_vocabulary.json.
    Raises ValueError if any tag is unknown or tag count is outside 1-3.
    Raises ValueError if INTENTION_TAGS does not have exactly 20 keys.
    Prints success message on pass.
    """
    if len(INTENTION_TAGS) != 20:
        raise ValueError(
            f"INTENTION_TAGS must have 20 entries, has {len(INTENTION_TAGS)}"
        )

    n_validated = 0
    for situation_id, tags in INTENTION_TAGS.items():
        if not (1 <= len(tags) <= 3):
            raise ValueError(
                f"INTENTION_TAGS[{situation_id!r}]: "
                f"must have 1-3 tags, has {len(tags)}"
            )
        for tag in tags:
            if tag not in vocab:
                raise ValueError(
                    f"INTENTION_TAGS[{situation_id!r}]: "
                    f"tag '{tag}' not in vocabulary (valid: {sorted(vocab.keys())})"
                )
            n_validated += 1

    print(f"INTENTION_TAGS: OK — {n_validated} tag assignments validated")


def build_enriched_record(
    situation: dict,
    label: str,
    untagged_features: set,
) -> dict:
    """
    Builds one enriched record for the canonical JSONL.
    situation: one item from pilot_situations.json.
    label: consensus action string for this hand.
    untagged_features: set of feature names that are untagged for this hand.

    Returns dict with: situation_id, label, feat_dict, attention_flags,
    attention_levels, intention_tags, n_tagged.
    Raises ValueError if situation['feat_dict'] is missing any key in FEATURE_COLUMNS.
    """
    # String-to-numeric maps for features that may have string values in the BP* hands
    STREET_MAP = {'flop': 0, 'turn': 1, 'river': 2}
    POSITION_MAP = {'UTG': 0, 'HJ': 1, 'CO': 2, 'BTN': 3, 'SB': 4, 'BB': 5}

    situation_id = situation['situation_id']
    feat_dict_raw = situation['feat_dict']

    # Verify all 54 features present
    for fc in FEATURE_COLUMNS:
        if fc not in feat_dict_raw:
            raise ValueError(
                f"situation '{situation_id}': feat_dict missing feature '{fc}'"
            )

    def to_float(key, val):
        """Convert value to float, handling known string encodings."""
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            if key == 'street':
                if val in STREET_MAP:
                    return float(STREET_MAP[val])
                raise ValueError(f"Unknown street string '{val}' for '{situation_id}'")
            if key in ('hero_position', 'villain_position'):
                if val in POSITION_MAP:
                    return float(POSITION_MAP[val])
                # Try numeric parse
                try:
                    return float(val)
                except ValueError:
                    raise ValueError(
                        f"Unknown position string '{val}' for feature '{key}' in '{situation_id}'"
                    )
            try:
                return float(val)
            except ValueError:
                raise ValueError(
                    f"Cannot convert '{val}' to float for feature '{key}' in '{situation_id}'"
                )
        return float(val)

    # Build clean feat_dict in FEATURE_COLUMNS order
    feat_dict = {fc: to_float(fc, feat_dict_raw[fc]) for fc in FEATURE_COLUMNS}

    # Build attention_flags: 1 if tagged (not in untagged_features), else 0
    attention_flags = {
        fc: (0 if fc in untagged_features else 1)
        for fc in FEATURE_COLUMNS
    }
    n_tagged = sum(attention_flags.values())

    # Build attention_levels: look up in ATTENTION_LEVELS[situation_id]
    hand_levels = ATTENTION_LEVELS.get(situation_id, {})
    attention_levels = {}
    for fc in FEATURE_COLUMNS:
        if fc in untagged_features:
            # Untagged always gets 0.1 regardless of ATTENTION_LEVELS
            attention_levels[fc] = LEVEL_WEIGHTS['Untagged']
        elif fc in hand_levels:
            attention_levels[fc] = LEVEL_WEIGHTS[hand_levels[fc]]
        else:
            # Tagged but not assigned a level — treat as Untagged weight
            # (should not happen for the 20 pilot hands if ATTENTION_LEVELS is complete)
            attention_levels[fc] = LEVEL_WEIGHTS['Untagged']

    # Intention tags
    intention_tags = INTENTION_TAGS.get(situation_id, [])

    return {
        'situation_id':    situation_id,
        'label':           label,
        'feat_dict':       feat_dict,
        'attention_flags': attention_flags,
        'attention_levels': attention_levels,
        'intention_tags':  intention_tags,
        'n_tagged':        n_tagged,
    }


def write_enriched_jsonl(records: list, path: str) -> None:
    """
    Writes one JSON-serialized record per line to path.
    Raises IOError if file cannot be written.
    """
    try:
        with open(path, 'w') as f:
            for rec in records:
                f.write(json.dumps(rec) + '\n')
    except OSError as e:
        raise IOError(f"Cannot write enriched JSONL to {path}: {e}")
    print(f"Wrote {len(records)} records to {path}")


def write_base_csv(records: list, path: str) -> None:
    """
    Writes pilot_20_base.csv.
    Columns: 54 FEATURE_COLUMNS (in order) + label.
    Raises ValueError if records list is not length 20.
    """
    if len(records) != 20:
        raise ValueError(f"write_base_csv: expected 20 records, got {len(records)}")

    columns = list(FEATURE_COLUMNS) + ['label']
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for rec in records:
            row = dict(rec['feat_dict'])
            row['label'] = rec['label']
            writer.writerow(row)


def write_attention_csv(records: list, path: str) -> None:
    """
    Writes pilot_20_attention.csv.
    Columns: 54 FEATURE_COLUMNS + 54 attn_{feature} cols + label. Total: 109 cols.
    """
    attn_cols = ['attn_' + fc for fc in FEATURE_COLUMNS]
    columns = list(FEATURE_COLUMNS) + attn_cols + ['label']
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for rec in records:
            row = dict(rec['feat_dict'])
            for fc in FEATURE_COLUMNS:
                row['attn_' + fc] = rec['attention_flags'][fc]
            row['label'] = rec['label']
            writer.writerow(row)


def write_levels_csv(records: list, path: str) -> None:
    """
    Writes pilot_20_attention_levels.csv.
    Columns: 54 FEATURE_COLUMNS + 54 level_{feature} cols + label. Total: 109 cols.
    """
    level_cols = ['level_' + fc for fc in FEATURE_COLUMNS]
    columns = list(FEATURE_COLUMNS) + level_cols + ['label']
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for rec in records:
            row = dict(rec['feat_dict'])
            for fc in FEATURE_COLUMNS:
                row['level_' + fc] = rec['attention_levels'][fc]
            row['label'] = rec['label']
            writer.writerow(row)


def write_intentions_csv(records: list, path: str) -> None:
    """
    Writes pilot_20_intentions.csv.
    Columns: 54 FEATURE_COLUMNS + one intent_{tag} column per unique tag (sorted).
    No label column.
    """
    # Collect all unique tags across all records
    all_tags = sorted(set(
        tag
        for rec in records
        for tag in rec['intention_tags']
    ))
    intent_cols = ['intent_' + tag for tag in all_tags]

    # Print distribution before writing
    tag_counts = {tag: 0 for tag in all_tags}
    for rec in records:
        for tag in rec['intention_tags']:
            tag_counts[tag] += 1
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"  intent_{tag}: {count}/20 hands")

    columns = list(FEATURE_COLUMNS) + intent_cols
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for rec in records:
            row = dict(rec['feat_dict'])
            for tag in all_tags:
                row['intent_' + tag] = (1 if tag in rec['intention_tags'] else 0)
            writer.writerow(row)


def print_verification_summary(records: list) -> None:
    """
    Prints verification summary to stdout.
    """
    from collections import Counter

    print("\n" + "=" * 60)
    print("ASSEMBLY VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total records: {len(records)}")
    print(f"Feature column count: {len(FEATURE_COLUMNS)}")

    # Label distribution
    label_dist = Counter(rec['label'] for rec in records)
    dist_str = ', '.join(f"{a}: {label_dist.get(a, 0)}" for a in ACTION_CLASSES)
    print(f"Label distribution: {{{dist_str}}}")

    # Attention coverage
    tagged_counts = [rec['n_tagged'] for rec in records]
    avg_tagged = sum(tagged_counts) / len(tagged_counts)
    print(f"Attention coverage: avg tagged per hand = {avg_tagged:.1f}, "
          f"min = {min(tagged_counts)}, max = {max(tagged_counts)}")

    # Intention tag distribution
    all_tags = sorted(set(
        tag for rec in records for tag in rec['intention_tags']
    ))
    tag_counts = {tag: 0 for tag in all_tags}
    for rec in records:
        for tag in rec['intention_tags']:
            tag_counts[tag] += 1

    print("Intention tag distribution:")
    for tag, count in sorted(tag_counts.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count}/20 hands")

    # Find smallest N such that top-N tags cover >= 90% of hands
    # "cover" = sum of top-N tag counts / 20 >= 0.9 (treating overlaps liberally)
    sorted_tags_by_count = sorted(tag_counts.items(), key=lambda x: -x[1])
    threshold = 20 * 0.9
    cumulative = 0
    n_cover = 0
    for tag, cnt in sorted_tags_by_count:
        cumulative += cnt
        n_cover += 1
        if cumulative >= threshold:
            break
    pct_covered = min(100.0, cumulative / 20 * 100)
    print(f"Top {n_cover} tags cover {pct_covered:.0f}% of hands (tag-assignment coverage)")

    # Files written
    print("Files written:")
    for path in [ENRICHED_JSONL_PATH, BASE_CSV_PATH, ATTENTION_CSV_PATH,
                 LEVELS_CSV_PATH, INTENTIONS_CSV_PATH]:
        print(f"  {path}")
    print("=" * 60)


def main() -> None:
    """
    Orchestrates assembly in the exact order specified by the blueprint.
    """
    try:
        # 1. Load tag vocabulary
        with open(TAG_VOCAB_PATH) as f:
            vocab = json.load(f)

        # 2. Load pilot sources
        situations, consensus = load_pilot_sources()

        # 3. Parse untagged features file
        untagged_map = parse_untagged_features_file(UNTAGGED_FEATURES_PATH)

        # 4. Validate ATTENTION_LEVELS
        validate_attention_levels(untagged_map)

        # 5. Validate INTENTION_TAGS
        validate_intention_tags(vocab['intentions'])

        # 6. Build enriched records
        records = [
            build_enriched_record(
                s,
                consensus[s['situation_id']],
                untagged_map[s['situation_id']],
            )
            for s in situations
        ]

        # 7. Write enriched JSONL
        write_enriched_jsonl(records, ENRICHED_JSONL_PATH)

        # 8. Write base CSV
        write_base_csv(records, BASE_CSV_PATH)

        # 9. Write attention CSV
        write_attention_csv(records, ATTENTION_CSV_PATH)

        # 10. Write levels CSV
        write_levels_csv(records, LEVELS_CSV_PATH)

        # 11. Write intentions CSV
        write_intentions_csv(records, INTENTIONS_CSV_PATH)

        # 12. Print verification summary
        print_verification_summary(records)

        # 13. Done
        print("ASSEMBLY COMPLETE — proceed to experiments")

    except Exception as e:
        print(f"ASSEMBLY FAILED: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
