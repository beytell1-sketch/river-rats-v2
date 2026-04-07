"""
Single source of truth for feature dictionary key names.

All modules that read or write feature dicts should import from here.
This prevents silent mismatches where one module writes '_num_raises_this_street'
and another reads 'num_raises_this_street'.

Convention:
- Model features (in FEATURE_COLUMNS): no underscore prefix
- Metadata fields (not in model): underscore prefix
- Internal game state: underscore prefix
"""


class F:
    """Feature dictionary key constants."""

    # Model features (38 features in FEATURE_COLUMNS)
    STREET = 'street'
    FACING_BET = 'facing_bet'
    POT_SIZE = 'pot_size'
    TO_CALL = 'to_call'
    POT_ODDS = 'pot_odds'
    BET_TO_POT = 'bet_to_pot'
    HERO_POSITION = 'hero_position'
    VILLAIN_POSITION = 'villain_position'
    IS_IP = 'is_ip'
    HAND_CATEGORY = 'hand_category'
    HAND_RANK = 'hand_rank'
    IS_MADE_HAND = 'is_made_hand'
    IS_STRONG_MADE = 'is_strong_made'
    IS_MONSTER = 'is_monster'
    HAS_FLUSH_DRAW = 'has_flush_draw'
    HAS_STRAIGHT_DRAW = 'has_straight_draw'
    DRAW_OUTS = 'draw_outs'
    IS_MONOTONE = 'is_monotone'
    IS_TWO_TONE = 'is_two_tone'
    IS_RAINBOW = 'is_rainbow'
    IS_PAIRED = 'is_paired'
    IS_DOUBLE_PAIRED = 'is_double_paired'
    CONNECTIVITY_SCORE = 'connectivity_score'
    HIGH_CARD_RANK = 'high_card_rank'
    DANGER_SCORE = 'danger_score'
    FLUSH_DANGER = 'flush_danger'
    STRAIGHT_DANGER = 'straight_danger'
    RAW_EQUITY = 'raw_equity'
    EQUITY_VS_RANGE = 'equity_vs_range'
    BETTER_HAND_PCT = 'better_hand_pct'
    WORSE_HAND_PCT = 'worse_hand_pct'
    EQUITY_MARGIN = 'equity_margin'
    SPR = 'spr'
    IS_3BET_POT = 'is_3bet_pot'
    VILLAIN_AGGRESSION_COUNT = 'villain_aggression_count'
    VILLAIN_CHECKED_BACK = 'villain_checked_back'
    VILLAIN_CALL_COUNT = 'villain_call_count'
    NUM_OPPONENTS = 'num_opponents'
    VILLAIN_TOP_PAIR_PLUS_PCT = 'villain_top_pair_plus_pct'
    VILLAIN_DRAW_PCT = 'villain_draw_pct'
    VILLAIN_AIR_PCT = 'villain_air_pct'
    VILLAIN_RANGE_CAPPED = 'villain_range_capped'
    BOARD_FAVOUR = 'board_favour'
    NUM_CALLERS_TO_BET = 'num_callers_to_bet'
    FACING_RAISE = 'facing_raise'
    # had_preflop_open: removed — oracle always plays opened pots,
    # limped pots are out of scope. Feature would be constant=1.

    # Step 12: new features 46-48
    FLUSH_BLOCK_PCT = 'flush_block_pct'
    OVERCARD_OUTS = 'overcard_outs'
    IMPROVEMENT_PROBABILITY = 'improvement_probability'

    # Metadata fields (underscore prefix, not in model)
    META_NUM_OPPONENTS = '_num_opponents'
    META_NUM_RAISES = '_num_raises_this_street'
    META_HERO_CARDS = '_hero_cards'
    META_BOARD_CARDS = '_board_cards'
    META_HERO_POS_RAW = '_hero_pos_raw'
    META_VILLAIN_POS_RAW = '_villain_pos_raw'
    META_STREET_RAW = '_street_raw'
    META_VILLAIN_TP_PLUS_PCT = '_villain_top_pair_plus_pct'
    META_VILLAIN_DRAW_PCT = '_villain_draw_pct'
    META_VILLAIN_AIR_PCT = '_villain_air_pct'
    META_VILLAIN_RANGE_CAPPED = '_villain_range_capped'
    META_OPENER_POSITION = '_opener_position'
    META_BETTOR_POSITION = '_bettor_position'
