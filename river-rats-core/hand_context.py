"""
HandContext — Human-readable hand context for the teaching pipeline.

Converts numeric feature values into the strings that templates need.
Pure data module: no model access, no SHAP, no side effects.

Two key outputs:
  1. HandContext dataclass — human-readable fields for the hand
  2. build_render_context() — dict of all template variables

Architecture:
  Feature array → HandContext → RenderContext dict → Template engine
  
  HandContext is built ONCE per hand, before the pipeline runs.
  RenderContext is passed to every template render call.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════
# REVERSE MAPPINGS (numeric feature value → human-readable string)
# ═══════════════════════════════════════════════════════════════════

# hand_category integer → noun phrase for templates
# Source: HAND_CATEGORY_ENCODING in feature_extractor.py
# Key = integer value from feature vector, Value = display string
CATEGORY_DESCRIPTIONS: Dict[float, str] = {
    0.0:  "high card",
    1.0:  "one overcard",
    2.0:  "overcards",
    3.0:  "bottom pair",
    4.0:  "an underpair",
    5.0:  "middle pair",
    6.0:  "top pair",
    7.0:  "top pair, good kicker",
    8.0:  "top pair, top kicker",
    9.0:  "an overpair",
    10.0: "two pair",
    11.0: "trips",
    12.0: "a set",
    13.0: "a straight",
    14.0: "a flush",
    15.0: "a full house",
    16.0: "quads",
    17.0: "a straight flush",
}

# hero_position / villain_position float → position name
# Source: POSITION_ORDINAL in feature_extractor.py (reversed)
POSITION_NAMES: Dict[float, str] = {
    0.0: "UTG",
    1.0: "HJ",
    2.0: "CO",
    3.0: "BTN",
    4.0: "SB",
    5.0: "BB",
}

# street float → display name
STREET_NAMES: Dict[float, str] = {
    0.0: "flop",
    1.0: "turn",
    2.0: "river",
}

STREET_NAMES_CAP: Dict[float, str] = {
    0.0: "Flop",
    1.0: "Turn",
    2.0: "River",
}


# ═══════════════════════════════════════════════════════════════════
# HAND CONTEXT DATACLASS
# ═══════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class HandContext:
    """
    Human-readable context for a single hand decision point.
    
    Built from numeric features. Passed through the entire pipeline.
    All fields are display-ready strings or simple values.
    """
    # Card strings (optional — not available in features-only mode)
    hero_cards: str               # "AcKs" or "" if unavailable
    board_cards: str              # "9s7s4c6s" or "" if unavailable
    
    # Human-readable names
    hero_position_name: str       # "BTN", "SB", etc.
    villain_position_name: str    # "BB", "UTG", etc.
    street_name: str              # "flop", "turn", "river"
    street_name_cap: str          # "Flop", "Turn", "River"
    hand_description: str         # "top pair", "a flush draw", "high card"
    hand_description_cap: str     # "Top pair", "A flush draw", "High card"
    hand_description_bare: str    # "top pair", "flush draw", "high card" (no article)
    hand_verb: str                # "is" or "are" (for plural agreement)
    hand_verb_neg: str            # "isn't" or "aren't"
    hand_does_neg: str            # "doesn't" or "don't"
    
    # Key context flags
    is_ip: bool                   # True = in position
    is_initiative: bool           # True = not facing a bet
    
    # Raw numeric values (kept for render context)
    equity_vs_range: float
    raw_equity: float
    equity_margin: float
    pot_odds: float
    bet_to_pot: float
    spr: float
    danger_score: float
    draw_outs: float
    better_hand_pct: float
    worse_hand_pct: float
    hand_category: float
    hand_rank: float

    # Action history context (from PokerBench; 0 for gauntlet hands)
    is_3bet_pot: bool               # True = preflop 3-bet occurred
    villain_aggression_count: int   # 0-3, streets villain bet/raised
    villain_checked_back: bool      # True = villain checked any prior street
    villain_call_count: int         # 0-3, streets villain flat-called

    # Multiway seed — defaults to HU, ready for multiway when wired
    num_opponents: int              # 1 = heads-up (default), 2+ = multiway
    opponent_phrase: str            # "your opponent" (HU) or "your opponents" (MW)

    # V3 enrichment fields (from foundation layer, not model features)
    pfr_advantage: float = 0.5         # 0-1, how much board favors PFR
    board_type: str = "unknown"        # texture classification
    draw_equity: float = 0.0           # 0-0.45, estimated draw equity
    needs_protection: bool = False     # one-pair hands need protection bet
    pot_size: float = 0.0              # raw pot size for correct pot odds
    to_call_amount: float = 0.0        # raw call amount for correct pot odds

    # Range-board teaching features (Phase 4B — from classify loop)
    villain_top_pair_plus_pct: float = 0.0   # 0-1, % of villain range TP+
    villain_draw_pct: float = 0.0            # 0-1, % with strong draws
    villain_air_pct: float = 0.0             # 0-1, % with nothing
    villain_range_capped: bool = False       # True = no 3-bet premiums
    board_favour: float = 0.0               # positive = favours hero

    # Range decomposition (Phase 2 — L4+ only, populated by explain_hand)
    range_breakdown: object = None           # Optional RangeBreakdown, L4+ only


# Descriptions that need "are" instead of "is"
_PLURAL_DESCRIPTIONS = {"overcards"}


def _strip_leading_article(desc: str) -> str:
    """Strip leading 'a ' or 'an ' from a hand description."""
    if desc.startswith("a "):
        return desc[2:]
    if desc.startswith("an "):
        return desc[3:]
    return desc


# ═══════════════════════════════════════════════════════════════════
# FACTORY
# ═══════════════════════════════════════════════════════════════════

def build_hand_context(
    feat_dict: Dict[str, float],
    hero_cards: str = "",
    board_cards: str = "",
    num_opponents: int = 1,
) -> HandContext:
    """
    Build HandContext from a feature dictionary.
    
    Args:
        feat_dict: {feature_name: value} from the feature vector
        hero_cards: Optional card string like "AcKs"
        board_cards: Optional board string like "9s7s4c6s"
        num_opponents: Number of opponents (1 = heads-up, 2+ = multiway)
    
    Returns:
        Frozen HandContext ready for the pipeline.
    """
    # Position names
    hero_pos = feat_dict.get("hero_position", -1)
    villain_pos = feat_dict.get("villain_position", -1)
    hero_pos_name = POSITION_NAMES.get(hero_pos, f"Pos{hero_pos:.0f}")
    villain_pos_name = POSITION_NAMES.get(villain_pos, f"Pos{villain_pos:.0f}")
    
    # Street
    street_val = feat_dict.get("street", -1)
    street_name = STREET_NAMES.get(street_val, "unknown")
    street_name_cap = STREET_NAMES_CAP.get(street_val, "Unknown")
    
    # Hand description from category + draw info
    # Suppress draw flags on river — draws are dead, feature values are artifacts
    cat_val = feat_dict.get("hand_category", -1)
    is_river = feat_dict.get("street", -1) == 2.0
    has_fd = feat_dict.get("has_flush_draw", 0) > 0.5 and not is_river
    has_sd = feat_dict.get("has_straight_draw", 0) > 0.5 and not is_river
    hand_desc = _build_hand_description(cat_val, has_fd, has_sd)
    hand_desc_cap = hand_desc[0].upper() + hand_desc[1:] if hand_desc else "Your hand"
    hand_desc_bare = _strip_leading_article(hand_desc)
    is_plural = hand_desc_bare in _PLURAL_DESCRIPTIONS
    hand_verb = "are" if is_plural else "is"
    hand_verb_neg = "aren't" if is_plural else "isn't"
    hand_does_neg = "don't" if is_plural else "doesn't"
    
    # Flags
    is_ip = feat_dict.get("is_ip", 0) > 0.5
    is_initiative = feat_dict.get("facing_bet", 0) == 0
    
    return HandContext(
        hero_cards=hero_cards,
        board_cards=board_cards,
        hero_position_name=hero_pos_name,
        villain_position_name=villain_pos_name,
        street_name=street_name,
        street_name_cap=street_name_cap,
        hand_description=hand_desc,
        hand_description_cap=hand_desc_cap,
        hand_description_bare=hand_desc_bare,
        hand_verb=hand_verb,
        hand_verb_neg=hand_verb_neg,
        hand_does_neg=hand_does_neg,
        is_ip=is_ip,
        is_initiative=is_initiative,
        equity_vs_range=feat_dict.get("equity_vs_range", 0),
        raw_equity=feat_dict.get("raw_equity", 0),
        equity_margin=feat_dict.get("equity_margin", 0),
        pot_odds=feat_dict.get("pot_odds", 0),
        bet_to_pot=feat_dict.get("bet_to_pot", 0),
        spr=feat_dict.get("spr", 0),
        danger_score=feat_dict.get("danger_score", 0),
        draw_outs=feat_dict.get("draw_outs", 0),
        better_hand_pct=feat_dict.get("better_hand_pct", 0),
        worse_hand_pct=feat_dict.get("worse_hand_pct", 0),
        hand_category=feat_dict.get("hand_category", 0),
        hand_rank=feat_dict.get("hand_rank", 0),
        is_3bet_pot=feat_dict.get("is_3bet_pot", 0) > 0.5,
        villain_aggression_count=int(feat_dict.get("villain_aggression_count", 0)),
        villain_checked_back=feat_dict.get("villain_checked_back", 0) > 0.5,
        villain_call_count=int(feat_dict.get("villain_call_count", 0)),
        num_opponents=num_opponents,
        opponent_phrase="your opponents" if num_opponents > 1 else "your opponent",
        pfr_advantage=feat_dict.get('_pfr_advantage', 0.5),
        board_type=feat_dict.get('_board_type', 'unknown'),
        draw_equity=feat_dict.get('_draw_equity', 0.0),
        needs_protection=feat_dict.get('_needs_protection', 0) > 0.5,
        pot_size=feat_dict.get('pot_size', 0.0),
        to_call_amount=feat_dict.get('to_call', 0.0),
        villain_top_pair_plus_pct=feat_dict.get('_villain_top_pair_plus_pct', 0.0),
        villain_draw_pct=feat_dict.get('_villain_draw_pct', 0.0),
        villain_air_pct=feat_dict.get('_villain_air_pct', 0.0),
        villain_range_capped=feat_dict.get('_villain_range_capped', 0) > 0.5,
        board_favour=feat_dict.get('_board_favour', 0.0),
    )


def _build_hand_description(
    cat_val: float,
    has_flush_draw: bool,
    has_straight_draw: bool,
) -> str:
    """
    Build a natural hand description combining made hand and draws.
    
    Logic:
      - Weak made hand (cat <= 2: high card, overcards) + draw → describe as draw
      - Strong made hand + draw → "top pair with a flush draw"
      - No draw → just the made hand
    """
    made_desc = _category_to_description(cat_val)
    
    # Determine draw description
    draw_desc = None
    if has_flush_draw and has_straight_draw:
        draw_desc = "a combo draw"
    elif has_flush_draw:
        draw_desc = "a flush draw"
    elif has_straight_draw:
        draw_desc = "a straight draw"
    
    if draw_desc is None:
        return made_desc
    
    # Weak made hands (high card, one overcard, overcards) → lead with draw
    if cat_val <= 2.0:
        return draw_desc
    
    # Strong made hand + draw → combine
    return f"{made_desc} with {draw_desc}"


def _category_to_description(cat_val: float) -> str:
    """
    Convert numeric hand_category to a noun phrase.
    
    Uses nearest-match lookup because floating point values
    from the feature vector may have precision artifacts.
    """
    if cat_val < 0:
        return "your hand"  # fallback
    
    # Try exact match first
    if cat_val in CATEGORY_DESCRIPTIONS:
        return CATEGORY_DESCRIPTIONS[cat_val]
    
    # Nearest match (within 0.06 tolerance for float precision)
    best_key = None
    best_dist = float("inf")
    for key in CATEGORY_DESCRIPTIONS:
        dist = abs(key - cat_val)
        if dist < best_dist:
            best_dist = dist
            best_key = key
    
    if best_dist < 0.1:
        return CATEGORY_DESCRIPTIONS[best_key]
    
    return "your hand"  # unknown category


# ═══════════════════════════════════════════════════════════════════
# RENDER CONTEXT BUILDER
# ═══════════════════════════════════════════════════════════════════

def _correct_pot_odds_pct(ctx: HandContext) -> float:
    """Correct pot odds: to_call / (pot_size + 2 * to_call).

    In PokerBench data, pot_size is the pot BEFORE villain's bet,
    and to_call IS the bet amount (which equals the call amount).
    Total pot after hero calls = pot_size + bet + call = pot_size + 2 * to_call.
    Required equity = risk / total = to_call / (pot_size + 2 * to_call).
    """
    if ctx.to_call_amount <= 0:
        return 0.0
    total = ctx.pot_size + 2 * ctx.to_call_amount
    if total <= 0:
        return 0.0
    return (ctx.to_call_amount / total) * 100


def _correct_margin_pct(ctx: HandContext) -> float:
    """Correct equity margin using correct pot odds."""
    pot_odds_pct = _correct_pot_odds_pct(ctx)
    equity_pct = (ctx.equity_vs_range or ctx.raw_equity) * 100
    return equity_pct - pot_odds_pct


def build_render_context(
    ctx: HandContext,
    action_name: str = "",
) -> Dict[str, object]:
    """
    Build the template variable dict from HandContext.
    
    This is the single source of truth for all template variables.
    Every vocab template's {placeholder} maps to a key here.
    
    Args:
        ctx: HandContext for this hand
        action_name: "FOLD", "CHECK", "CALL", "BET", "RAISE"
    
    Returns:
        Dict ready for str.format(**render_ctx)
    """
    equity_pct = (ctx.equity_vs_range or ctx.raw_equity) * 100
    
    return {
        # Hand description (noun phrase, no possessive)
        "hand_desc": ctx.hand_description,
        "Hand_desc": ctx.hand_description_cap,
        "hand_desc_bare": ctx.hand_description_bare,
        "hand_verb": ctx.hand_verb,
        "hand_verb_neg": ctx.hand_verb_neg,
        "hand_does_neg": ctx.hand_does_neg,
        
        # Position & street
        "hero_pos": ctx.hero_position_name,
        "villain_pos": ctx.villain_position_name,
        "street": ctx.street_name,
        "Street": ctx.street_name_cap,
        
        # Equity & margin (as percentages)
        "equity_pct": equity_pct,
        "margin": ctx.equity_margin * 100,
        
        # Range position (as percentages)
        "top_range_pct": ctx.worse_hand_pct * 100,      # % of range you BEAT
        "bottom_range_pct": ctx.better_hand_pct * 100,   # % of range BETTER than you
        "range_pct": ctx.worse_hand_pct * 100,           # legacy compat
        
        # Price & structure
        "pot_odds_pct": ctx.pot_odds * 100,
        "spr": ctx.spr,
        "mdf_pct": 65,  # placeholder — proper MDF calc in resolver
        
        # Draw info
        "outs": ctx.draw_outs,
        "draw_equity_outs_pct": ctx.draw_outs * 2.2,  # rule of 2 approximation (outs-based)
        
        # Board
        "danger": ctx.danger_score * 100,
        
        # Action (for templates that reference {action})
        "action": action_name.lower() if action_name else "continue",

        # Action history context (available for future templates)
        "is_3bet_pot": ctx.is_3bet_pot,
        "v_aggression": ctx.villain_aggression_count,
        "v_checked_back": ctx.villain_checked_back,
        "v_call_count": ctx.villain_call_count,

        # Multiway seed — use {opponent_phrase} in templates instead of "your opponent"
        "opponent_phrase": ctx.opponent_phrase,
        "num_opponents": ctx.num_opponents,

        # V3 enrichment
        "pfr_advantage": ctx.pfr_advantage,
        "board_type": ctx.board_type,
        "draw_equity": ctx.draw_equity,
        "draw_equity_pct": ctx.draw_equity * 100,
        "needs_protection": ctx.needs_protection,
        "pot_size": ctx.pot_size,
        "to_call_amount": ctx.to_call_amount,

        # Corrected pot odds (feature value uses wrong formula)
        "correct_pot_odds_pct": _correct_pot_odds_pct(ctx),
        "correct_margin_pct": _correct_margin_pct(ctx),

        # Board details
        "danger_raw": round(ctx.danger_score, 2),
        "hand_cat": int(ctx.hand_category),

        # Range-board teaching features (Phase 4B)
        "villain_tp_pct": round(ctx.villain_top_pair_plus_pct * 100, 1),
        "villain_draw_pct": round(ctx.villain_draw_pct * 100, 1),
        "villain_air_pct": round(ctx.villain_air_pct * 100, 1),
        "range_capped": ctx.villain_range_capped,
        "board_favour_desc": (
            "favours your range" if ctx.board_favour > 0.05
            else "favours your opponent's range" if ctx.board_favour < -0.05
            else "roughly neutral"
        ),
    }
