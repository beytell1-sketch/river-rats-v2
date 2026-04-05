"""
LevelRenderer -- renders SpotObservation at Beginner, Intermediate, or Advanced.

All three levels read the SAME SpotObservation. They cannot contradict
because they share the same data. They differ only in:
1. Which fields they render (observation selection)
2. What vocabulary they use (vocabulary rendering)

Design principles:
- Beginner: no jargon, action-supportive framing, max 2 observations
- Intermediate: poker vocabulary, qualitative reasoning, qualifier required
  when counterintuitive, max 2-3 observations
- Advanced: full numbers, range decomposition, blockers, max 2-3 observations
"""
from typing import List, Optional, Tuple

from coaching.spot_observation import SpotObservation


# =====================================================================
# STANCE GATING — filter teaching sentences by oracle action alignment
# =====================================================================
# Each sentence is tagged with a stance:
#   AGGRESSIVE: fires when action is BET, RAISE, or CALL
#   DEFENSIVE:  fires when action is CHECK or FOLD
#   NEUTRAL:    fires regardless of action
#
# This prevents teaching text from contradicting the oracle's action.
# Example: "supports a continuation bet" (AGGRESSIVE) is suppressed
# when the oracle says CHECK.

AGGRESSIVE = "aggressive"
DEFENSIVE = "defensive"
NEUTRAL = "neutral"

_AGGRESSIVE_ACTIONS = {"BET", "RAISE", "CALL"}
_DEFENSIVE_ACTIONS = {"CHECK", "FOLD"}


def _possessive(phrase: str) -> str:
    """Return the possessive form: 'opponent' -> \"opponent's\", 'opponents' -> \"opponents'\"."""
    if phrase.endswith("s"):
        return f"{phrase}'"
    return f"{phrase}'s"


def _stance_ok(stance: str, action: str) -> bool:
    """Check if a sentence's stance is compatible with the oracle action."""
    if stance == NEUTRAL:
        return True
    if stance == AGGRESSIVE:
        return action in _AGGRESSIVE_ACTIONS
    if stance == DEFENSIVE:
        return action in _DEFENSIVE_ACTIONS
    return True


def _filter_by_stance(candidates: List[Tuple[str, str]], action: str) -> List[str]:
    """Filter (stance, sentence) tuples, returning only stance-compatible sentences."""
    return [s for stance, s in candidates if s and _stance_ok(stance, action)]


# =====================================================================
# GTO OPENING RANGE PERCENTAGES (6-max 100bb cash)
# Source: standard GTO solver outputs for 6-max cash game.
# Used at Intermediate and Advanced to name the position's range width.
# =====================================================================

GTO_OPEN_PCT = {
    'UTG': 13,
    'HJ':  18,
    'CO':  26,
    'BTN': 44,
    'SB':  52,
    'BB':  100,  # BB sees all hands (option/squeeze/defend)
}


# =====================================================================
# BEGINNER VOCABULARY MAPS
# =====================================================================

_BUCKET_TO_BEGINNER = {
    "monster":     "strong hand",
    "strong_made": "strong hand",
    "medium_made": "decent hand",
    "weak_made":   "weak hand",
    "drawing":     "draw",
    "air":         "weak hand",
}

_BOARD_BEGINNER = {
    "dry":       "safe board",
    "moderate":  "safe board",
    "dangerous": "dangerous board",
}

_BOARD_INTERMEDIATE = {
    "dry":       "dry and disconnected",
    "moderate":  "coordinated",
    "dangerous": "draw-heavy",
}


# =====================================================================
# DRAW TIER CLASSIFICATION
# =====================================================================

def _draw_tier(draw_outs: int) -> str:
    """
    Classify draw strength by out count.

    Returns one of: "gutshot", "standard", "combo", or "" (not a draw).

    Tiers (B2 fix -- boundary at 5 was wrong):
      gutshot  = exactly 4 outs
      standard = 5-9 outs
      combo    = 10+ outs
    """
    if draw_outs < 4:
        return ""           # not a meaningful draw
    if draw_outs == 4:
        return "gutshot"
    if draw_outs <= 9:
        return "standard"
    return "combo"


# =====================================================================
# SENTENCE SLOT PRIORITY (B6 / OQ-5 fix)
# =====================================================================

def _apply_sentence_priority(
    hand_assessment: str,
    tier2_candidates: list,   # draw price, equity, fold justification
    tier3_candidates: list,   # board texture, range state, villain behaviour
    tier4_candidates: list,   # tightness qualifiers
    cap: int = 3,
) -> list:
    """
    Enforce sentence slot priority at Intermediate (B6 / OQ-5 fix).

    Always includes hand_assessment in slot 0.
    Fills remaining slots with tier2 first, then tier3, then tier4.
    Never exceeds cap.

    Args:
        hand_assessment: The mandatory first sentence (never dropped).
        tier2_candidates: List of strings for priority 2 slot(s).
        tier3_candidates: List of strings for priority 3 slot(s).
        tier4_candidates: List of strings for priority 4 slot(s).
        cap: Maximum sentences to return (default 3).

    Returns:
        List of sentences, length <= cap.
    """
    result = [hand_assessment]
    remaining = cap - 1

    for candidate_list in (tier2_candidates, tier3_candidates, tier4_candidates):
        for sentence in candidate_list:
            if remaining <= 0:
                break
            if sentence:
                result.append(sentence)
                remaining -= 1
        if remaining <= 0:
            break

    return result


# =====================================================================
# CONFIDENCE HEDGE HELPER (A-8, S-7 fix)
# =====================================================================

def _confidence_hedge(obs: SpotObservation, level: str) -> str:
    """
    Confidence-driven hedging sentence (A-8).

    level: "beginner", "intermediate", "advanced"

    Confidence thresholds:
      >= 0.70  -- no hedge (return "")
      0.45-0.69 -- acknowledge alternative action by name (S-7 fix)
      < 0.45   -- frame as genuine close decision

    Returns empty string when:
      - confidence is 0.0 (not set by caller)
      - tightness is TOSS_UP or CLOSE (existing system already covers it)
      - confidence >= 0.70

    Never duplicates the tightness qualifier sentence.
    """
    # If tightness system already fires, do not also fire confidence hedge
    if obs.tightness in ("TOSS_UP", "CLOSE"):
        return ""

    conf = obs.confidence

    # confidence not populated
    if conf <= 0.0:
        return ""

    # High confidence -- no hedge needed
    if conf >= 0.70:
        return ""

    # Determine the alternative action name
    action = obs.action
    _ALTERNATIVES = {
        "BET":   "check",
        "CHECK": "bet",
        "RAISE": "call",
        "CALL":  "fold",
        "FOLD":  "call",
    }
    alt = _ALTERNATIVES.get(action, "the other action")

    if level == "beginner":
        # S-7 fix: name both actions at Beginner, not just "close decision"
        if conf < 0.45:
            return f"This is a close decision — {action.lower()} or {alt} are both reasonable."
        else:  # 0.45-0.69
            return f"{action.capitalize()} is the better choice, though {alt} is also fine."

    elif level == "intermediate":
        if conf < 0.45:
            return f"This is a close spot — {action.lower()} and {alt} are both reasonable here."
        else:  # 0.45-0.69
            return f"{action.capitalize()} is preferred here, but {alt} is also a reasonable option."

    else:  # advanced
        if conf < 0.45:
            return (
                f"Mixed spot: confidence {conf:.0%}. "
                f"GTO mixes between {action.lower()} and {alt} — both actions are near-EV-neutral."
            )
        else:  # 0.45-0.69
            return (
                f"Close decision: confidence {conf:.0%}. "
                f"{action.capitalize()} is preferred; {alt} is also defensible."
            )


# =====================================================================
# DRAW PRICE SENTENCE HELPER (A-4, with A-9 RIO for flush draws)
# =====================================================================

def _draw_price_sentence(obs: SpotObservation, level: str) -> str:
    """
    Draw price framing for draw + facing_bet situations (A-4).

    Called from render_intermediate() and render_advanced() when:
      is_multiway AND has_draw AND facing_bet are all True.

    Also appends reverse implied odds qualifier for flush draws (A-9, B4 fix).

    level: "intermediate" or "advanced"

    Returns a single string. For Advanced, the string may contain
    two sentences joined with a space (price sentence + RIO qualifier).

    B4 fix: reverse implied odds fires for flush draw ONLY (not straight draw).
    B5 fix: level gate -- only fires at intermediate or advanced.

    Equity is authoritative (v7 model, true N-opponent Monte Carlo).
    No caveats, no "(approximate)" -- display numbers clean.
    """
    if level not in ("intermediate", "advanced"):
        return ""

    draw_desc = obs.draw_description or "draw"
    draw_outs = obs.draw_outs
    draw_eq = obs.draw_equity * 100
    pot_odds = obs.pot_odds_pct
    margin = obs.equity_margin

    # --- Intermediate ---
    if level == "intermediate":
        if margin > 0:
            price_sentence = (
                f"Your {draw_desc} is getting the right price to call — "
                f"{draw_outs} outs gives you enough equity at this bet size."
            )
        elif margin > -10:
            price_sentence = (
                f"Your draw needs a better price — the bet is too large "
                f"for the number of outs you have."
            )
        else:
            price_sentence = (
                f"The bet is too large for your draw — fold and wait for "
                f"a better price."
            )

        # WI-16: Non-nut draw distinction (C2/C3 companion pair)
        # When is_nut_draw is False and multiway, add nut-awareness qualifier
        nut_warning = ""
        if (
            obs.is_multiway
            and not obs.is_nut_draw
            and draw_desc == "flush draw"
        ):
            if margin > 0:
                # C2 path: price is right but draw is not to the nuts
                nut_warning = (
                    "Your flush draw is not to the nuts — be aware that a higher "
                    "flush is possible, which limits how aggressively you should "
                    "play if you hit."
                )
            elif obs.action == "FOLD":
                # C3 path: too expensive AND not the nuts
                nut_warning = (
                    "Your draw is not to the nuts, and the bet is too large — "
                    "the risk of completing your draw and losing to a better "
                    "hand makes this a clear fold."
                )

        # A-9: reverse implied odds qualifier for non-nut flush draws only (B4 fix)
        # Suppressed when: combo draw, nut draw (is_nut_draw or hero_label),
        # a-high flush, margin <= 0, or WI-16 nut_warning already fires
        rio = ""
        if (
            not nut_warning
            and not obs.is_nut_draw
            and margin > 0
            and obs.is_multiway
            and draw_desc == "flush draw"
            and _draw_tier(draw_outs) != "combo"
            and "nut" not in obs.hero_label.lower()
            and "a-high" not in obs.hero_label.lower()
        ):
            rio = (
                "Be aware that completing your draw does not guarantee winning the "
                "pot — with multiple opponents, a higher flush is possible, "
                "and the pot will be larger when it happens."
            )

        suffix = nut_warning or rio
        return (price_sentence + " " + suffix).strip() if suffix else price_sentence

    # --- Advanced ---
    # Equity is correct (v7 model). Display numbers as authoritative.
    if margin > 0:
        price_sentence = (
            f"{draw_desc.capitalize()} with {draw_outs} outs "
            f"({draw_eq:.0f}% equity vs {pot_odds:.0f}% pot odds needed) — "
            f"call is profitable by {margin:.0f} points."
        )
    elif margin > -10:
        price_sentence = (
            f"{draw_desc.capitalize()} with {draw_outs} outs but equity "
            f"({draw_eq:.0f}%) falls short of the {pot_odds:.0f}% pot odds threshold."
        )
    else:
        price_sentence = (
            f"Equity deficit makes this draw a clear fold at this sizing."
        )

    # WI-16 Advanced: Non-nut draw distinction
    nut_warning = ""
    if (
        obs.is_multiway
        and not obs.is_nut_draw
        and draw_desc == "flush draw"
    ):
        if margin > 0:
            nut_warning = (
                f"Draw is not to the nuts — a higher flush is possible against "
                f"{obs.num_opponents} opponents, limiting post-completion value."
            )
        elif obs.action == "FOLD":
            nut_warning = (
                f"Non-nut draw at an insufficient price — completing and losing "
                f"to a higher flush is a significant multiway risk."
            )

    # A-9 Advanced: RIO qualifier (B4 fix -- flush draw only, not combo or nut)
    # Suppressed when WI-16 nut_warning fires
    rio = ""
    if (
        not nut_warning
        and margin > 0
        and obs.is_multiway
        and draw_desc == "flush draw"
        and _draw_tier(draw_outs) != "combo"
        and "nut" not in obs.hero_label.lower()
        and "a-high" not in obs.hero_label.lower()
    ):
        rio = (
            f"Reverse implied odds are elevated multiway: completing a non-nut "
            f"{draw_desc} against {obs.num_opponents} opponents risks losing a "
            f"large pot to a dominating hand."
        )

    suffix = nut_warning or rio
    return (price_sentence + " " + suffix).strip() if suffix else price_sentence


# =====================================================================
# BOARD TEXTURE INTERMEDIATE HELPER (A-6, S-2, S-9 fixes)
# =====================================================================

def _board_texture_intermediate(obs: SpotObservation) -> str:
    """
    Board texture sentence for Intermediate level (A-6).

    S-2 fix: dry board now includes action implication, not just description.
    S-9 fix: "few hands connect with this board" (not "here" which was ambiguous).
    """
    board_desc = _BOARD_INTERMEDIATE.get(obs.board_texture_label, "")
    if not board_desc:
        return ""

    if obs.is_multiway:
        if obs.board_texture_label in ("dangerous", "moderate"):
            return (
                f"The board is {board_desc} — with {obs.num_opponents} opponents, "
                f"at least one is likely to have connected."
            )
        else:  # dry
            return (
                f"The board is {board_desc} — even with multiple opponents, "
                f"few hands connect with this board, which supports a continuation bet."
            )
    else:
        return (
            f"The board is {board_desc} — "
            f"{_possessive(obs.opponent_phrase)} range connects accordingly."
        )


# =====================================================================
# SHARED BURDEN OF DEFENSE HELPER (A-10, S-4, S-8, B5 fixes)
# =====================================================================

def _shared_burden_sentence(obs: SpotObservation, level: str) -> str:
    """
    Shared burden of defense sentence for marginal FOLD/CALL decisions (A-10).

    B5 fix: explicit level gate -- fires at intermediate and advanced ONLY.
    S-4 fix: window narrowed from [-15, +5].
    S-8 fix: CALL template leads with "price makes this a call."

    Equity is authoritative (v7 model). Window is the original [-8, +5].
    No inflation compensation needed -- equity values are correct.

    Trigger conditions:
      is_multiway AND facing_bet AND action in (FOLD, CALL)
      AND equity_margin between -8 and +5 (marginal spot)

    Suppression (do NOT fire):
      - level == "beginner"
      - action is BET, RAISE, or CHECK
      - equity_margin > +5.0 (clear call)
      - equity_margin < -8.0 (clear fold)
      - is_multiway is False
    """
    if level == "beginner":
        return ""

    if not obs.is_multiway:
        return ""

    if not obs.facing_bet:
        return ""

    if obs.action not in ("FOLD", "CALL"):
        return ""

    # Original [-8, +5] window -- equity is correct, no inflation compensation
    if obs.equity_margin > 5.0 or obs.equity_margin < -8.0:
        return ""

    n_plus_one = obs.num_opponents + 1  # total players in pot

    if level == "intermediate":
        if obs.action == "FOLD":
            return (
                f"In a {n_plus_one}-way pot, you can fold more hands without "
                f"being exploited — {obs.opponent_phrase} share the defensive "
                f"responsibility."
            )
        else:  # CALL
            # S-8 fix: lead with "price makes this a call"
            return (
                "The price makes this a call, but notice that defending standards "
                "are tighter with multiple opponents."
            )

    else:  # advanced
        # Equity is correct -- display clean numbers, no caveats
        eq_pct = obs.equity * 100
        if obs.action == "FOLD":
            return (
                f"Shared burden of defense: with {obs.num_opponents} opponents, "
                f"each defender needs to continue less often to prevent profitable "
                f"bluffs. Your equity ({eq_pct:.0f}%) falls below the multiway "
                f"defending threshold."
            )
        else:  # CALL
            return (
                f"Price makes this a call ({eq_pct:.0f}% equity vs "
                f"{obs.pot_odds_pct:.0f}% needed), but multiway defense standards "
                f"are tighter — each defender continues less often when the burden "
                f"is shared."
            )


# =====================================================================
# VILLAIN RANGE STATE HELPER (A-11, S-5 fix)
# =====================================================================

def _villain_range_sentence_intermediate(obs: SpotObservation) -> str:
    """
    Villain range state sentence for Intermediate (A-11 + existing logic).

    A-11: When villain_range_state is CAPPED and is_multiway, add shared-burden
    qualifier. S-5 fix: specify "other opponents" rather than vague "others."

    For non-CAPPED states or heads-up, falls back to existing INTERMEDIATE_DESCRIPTIONS.
    """
    if not obs.villain_range_state or obs.villain_range_state == "unknown":
        return ""

    try:
        from testing.range_state import RangeState, INTERMEDIATE_DESCRIPTIONS
        rs = RangeState(obs.villain_range_state)

        # A-11: CAPPED + multiway + confident classifier
        if (
            obs.is_multiway
            and rs == RangeState.CAPPED
            and obs.villain_range_confidence > 0.5
        ):
            # S-5 fix: specify "one opponent" vs "other opponents"
            return (
                "Your opponent's range appears capped — they likely don't have the "
                "strongest hands. However, in a multiway pot, a capped range is harder "
                "to attack because one or more other opponents may still hold "
                "strong hands."
            )

        # All other states: use existing description (heads-up calibrated)
        desc = INTERMEDIATE_DESCRIPTIONS.get(rs)
        return desc or ""

    except (ValueError, KeyError):
        return ""


# =====================================================================
# BET-AND-CALL SIGNAL (WI-14)
# =====================================================================

def _bet_and_call_sentence(obs: SpotObservation, level: str) -> str:
    """
    Signal when hero faces both a bet and a call in a multiway pot (WI-14).

    Fires when facing_bet_and_call AND is_multiway.
    Level-gated: different language per level.
    """
    if not obs.facing_bet_and_call or not obs.is_multiway:
        return ""

    if level == "beginner":
        return (
            "Two opponents are showing interest — one bet and one "
            "called. Your hand is not strong enough against both."
        )
    elif level == "intermediate":
        return (
            "A bet and a call in a multiway pot means both opponents "
            "have connected — your hand cannot beat two screened ranges."
        )
    elif level == "advanced":
        return (
            "The bet-call sequence is among the strongest multiway "
            "signals: the caller has already filtered for hands "
            "beating the bettor."
        )
    return ""


# =====================================================================
# RAISE FOLD SIGNAL (WI-10)
# =====================================================================

def _raise_fold_sentence(obs: SpotObservation, level: str) -> str:
    """
    Signal when hero faces a raise in a multiway pot and folds (WI-10).

    Uses 'raised' not 'check-raised' because facing_check_raise is a
    heuristic that may fire on bet-raise sequences.

    Fires when facing_check_raise AND is_multiway AND action == 'FOLD'.
    """
    if not obs.facing_check_raise or not obs.is_multiway or obs.action != "FOLD":
        return ""

    if level == "beginner":
        return (
            "When your opponent raises, they almost always have you "
            "beaten — especially with more players watching."
        )
    elif level == "intermediate":
        return (
            "A raise in a multiway pot is one of the strongest signals "
            "in poker — your opponent is raising despite knowing other "
            "players may still be in the hand."
        )
    elif level == "advanced":
        return (
            "The raising range in multiway pots is polarised toward "
            "very strong hands — bluffs are nearly absent because the "
            "raiser must beat both the bettor and potential callers."
        )
    return ""


# =====================================================================
# MULTI-STREET AGGRESSION SIGNAL (WI-15)
# =====================================================================

def _multi_street_aggression_sentence(obs: SpotObservation, level: str) -> str:
    """
    Signal when villain has bet on multiple streets in a multiway pot (WI-15).

    Fires when villain_aggression_streets >= 2 AND is_multiway.
    Beginner: suppressed per Q3.
    """
    if obs.villain_aggression_streets < 2 or not obs.is_multiway:
        return ""

    if level == "beginner":
        return ""  # Suppressed per Q3

    if level == "intermediate":
        return (
            "Your opponent has bet on multiple streets against multiple "
            "players — their range is very narrow and strong."
        )
    elif level == "advanced":
        return (
            "Villain's multi-street aggression into a multiway pot signals "
            "a range weighted toward top pair with a strong kicker, two "
            "pair, and sets — dominated kickers cannot continue."
        )
    return ""


# =====================================================================
# MISSED-DRAW RIVER TEACHING (D2)
# =====================================================================

def _missed_draw_river_sentence(obs: SpotObservation, level: str) -> str:
    """
    Teaching for river hands where hero was drawing on a previous street
    and the draw missed (D2).

    Trigger: was_drawing_previous_street AND action == CHECK AND is_multiway.
    """
    if not obs.was_drawing_previous_street or obs.action != "CHECK" or not obs.is_multiway:
        return ""

    if level == "beginner":
        hand_label = _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")
        return (
            f"Your draw missed — you have only a {hand_label} now. "
            f"Checking is the right move."
        )

    if level == "intermediate":
        return (
            "A missed draw on the river in a multiway pot is almost "
            "always a check — you need all opponents to fold for a "
            "bluff to work."
        )

    if level == "advanced":
        n = obs.num_opponents
        if n > 0:
            combined = (0.40 ** n) * 100
            return (
                f"Missed draw on the river. Bluffing requires all {n} "
                f"opponents to fold — at a typical sizing, combined fold "
                f"probability is ~{combined:.0f}%, making a bluff "
                f"unprofitable. Check and concede."
            )
        return "Missed draw on the river. Check."

    return ""


# =====================================================================
# PROTECT CHECKING RANGE (WI-17)
# =====================================================================

def _protect_checking_range_sentence(obs: SpotObservation, level: str) -> str:
    """
    Explain why GTO checks some strong hands OOP to protect the checking
    range (WI-17).

    Trigger: is_multiway AND NOT is_ip AND hand_bucket in (strong_made, monster)
    AND tightness in (CLOSE, TOSS_UP) AND action == BET.

    Beginner: suppressed (concept too abstract).
    """
    if not obs.is_multiway:
        return ""
    if obs.is_ip:
        return ""
    if obs.hand_bucket not in ("strong_made", "monster"):
        return ""
    if obs.tightness not in ("CLOSE", "TOSS_UP"):
        return ""
    if obs.action != "BET":
        return ""

    if level == "beginner":
        return ""

    if level == "intermediate":
        # GTO review: drops "protect the checking range" (L4 vocabulary),
        # uses outcome-based language, frames BET as correct action
        return (
            "The bet here is correct, but this is a close spot — GTO also "
            "checks some strong hands in this position. If you always bet "
            "your best hands when out of position in multiway pots, your "
            "checks signal weakness and opponents will attack them."
        )

    if level == "advanced":
        # GTO review: completes exploit path, ties multiway to the reason
        return (
            "BET is the recommended line, but this is genuinely close. "
            "Retaining strong hands in your checking range OOP is a GTO "
            "requirement: if you pure-bet all value, your check range "
            "becomes capped to medium-strength hands. In multiway pots "
            "this is especially costly — the aggregate range across "
            "multiple opponents increases the probability someone can "
            "punish a capped check range."
        )

    return ""


# =====================================================================
# BEGINNER MULTIWAY QUALIFIER HELPER (A-1, S-6 fix)
# =====================================================================

def _beginner_multiway_qualifier(obs: SpotObservation) -> str:
    """
    Return a multiway qualifier sentence for Beginner level (A-1).

    Returns empty string when:
      - is_multiway is False
      - action is BET or RAISE with confidence >= 0.70 (confident positive actions
        don't need a multiway caveat)

    S-6 fix: do not use the word "still" in the low-confidence qualifier.
    """
    if not obs.is_multiway:
        return ""

    action = obs.action
    hand_label = _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")

    # Positive action, high confidence: suppress qualifier
    if action in ("BET", "RAISE") and obs.confidence >= 0.70:
        return ""

    # Positive action, low confidence: supportive but hedged (S-6: no "still")
    if action in ("BET", "RAISE") and obs.confidence < 0.70:
        return "With more players in the hand, betting here is the right move."

    # Facing a bet and weak: show that multiple opponents increases the threat
    if obs.facing_bet:
        return (
            f"With multiple players showing strength, your {hand_label} "
            f"is not strong enough to continue."
        )

    # CHECK or FOLD with multiway context
    return (
        f"With multiple opponents, your {hand_label} is not strong enough "
        f"to lead out here."
    )


# =====================================================================
# BEGINNER RENDERER
# =====================================================================

def render_beginner(obs: SpotObservation) -> List[str]:
    """
    Render at Beginner level: max 2 observations, no jargon.

    No percentages, no "range", no "equity", no "MDF".
    Action-supportive framing when counterintuitive.
    """
    # -- Preflop --
    if obs.is_preflop and obs.preflop_scenario is not None:
        return _render_beginner_preflop(obs)

    sentences = []

    if obs.is_counterintuitive:
        sentences.append(_beginner_counterintuitive(obs))
    else:
        sentences.append(_beginner_standard(obs))

    # Slot 2: specific signals > generic qualifier > board texture
    # All candidates are (stance, sentence) tuples, filtered by action alignment.
    action = obs.action
    slot2_candidates = []

    # D2: missed-draw river teaching — DEFENSIVE
    missed_draw = _missed_draw_river_sentence(obs, "beginner")
    if missed_draw:
        slot2_candidates.append((DEFENSIVE, missed_draw))

    # WI-14: bet-and-call signal — DEFENSIVE
    bet_call = _bet_and_call_sentence(obs, "beginner")
    if bet_call:
        slot2_candidates.append((DEFENSIVE, bet_call))

    # WI-10: raise fold signal — DEFENSIVE
    raise_fold = _raise_fold_sentence(obs, "beginner")
    if raise_fold:
        slot2_candidates.append((DEFENSIVE, raise_fold))

    # Multiway qualifier — stance depends on content
    mw_qualifier = _beginner_multiway_qualifier(obs)
    if mw_qualifier:
        if "right move" in mw_qualifier or "betting" in mw_qualifier.lower():
            slot2_candidates.append((AGGRESSIVE, mw_qualifier))
        elif "not strong enough" in mw_qualifier:
            slot2_candidates.append((DEFENSIVE, mw_qualifier))
        else:
            slot2_candidates.append((NEUTRAL, mw_qualifier))

    # Board texture — NEUTRAL (always in pool as fallback; stance filter
    # will select it when higher-priority candidates are filtered out)
    board = _BOARD_BEGINNER.get(obs.board_texture_label, "")
    if board:
        if board == "safe board":
            slot2_candidates.append((NEUTRAL, "The board is safe — few hands connect here."))
        else:
            slot2_candidates.append((NEUTRAL, "The board is dangerous — many hands connect."))

    # Filter by stance and take the first compatible sentence
    compatible = _filter_by_stance(slot2_candidates, action)
    if compatible:
        sentences.append(compatible[0])

    # A-8: confidence-driven hedging
    hedge = _confidence_hedge(obs, "beginner")
    if hedge:
        sentences.append(hedge)

    # A-2 defence-in-depth: strip bluff vocabulary at Beginner
    sentences = [s for s in sentences if "bluff" not in s.lower()]
    return sentences[:2]


def _beginner_standard(obs: SpotObservation) -> str:
    """Standard (non-counterintuitive) beginner framing."""
    action = obs.action
    bucket_label = _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")

    if action == "BET" or action == "RAISE":
        if obs.hand_bucket in ("monster", "strong_made"):
            return f"You have a {bucket_label} — betting builds the pot."
        if obs.hand_bucket == "drawing":
            return "You have a draw — the price is right to continue."
        return f"You have a {bucket_label} — betting builds the pot."

    if action == "FOLD":
        return "Your hand is too weak to continue."

    if action == "CALL":
        if obs.has_draw:
            return "You have a draw — the price is right to continue."
        return f"You have a {bucket_label} — the price is right to continue."

    # CHECK
    if obs.hand_bucket in ("monster", "strong_made"):
        return f"You have a {bucket_label} with good showdown value."
    return f"You have a {bucket_label}."


def _beginner_counterintuitive(obs: SpotObservation) -> str:
    """Action-supportive framing for counterintuitive spots."""
    action = obs.action

    if action == "CHECK":
        # CHECK + strong/monster
        return "You have a strong hand. Checking is the right play here."

    if action == "BET" or action == "RAISE":
        if obs.hand_bucket in ("weak_made", "air"):
            return "Your hand is weak, but betting can still win the pot."
        if obs.hand_bucket == "drawing":
            return "You have a draw — betting gives you two ways to win."
        return "Betting can still win the pot."

    if action == "FOLD":
        if obs.counterintuitive_reason == "multiway_fold_discipline":
            hand_label = _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")
            return (
                f"With multiple players showing strength, your {hand_label} "
                f"is not strong enough to continue."
            )
        return "Your hand looks decent but is not strong enough here."

    if action == "CALL":
        if obs.has_draw:
            return "You have a draw — your hand can improve."
        return "You have a draw — your hand can improve."

    return f"You have a {_BUCKET_TO_BEGINNER.get(obs.hand_bucket, 'hand')}."


def _render_beginner_preflop(obs: SpotObservation) -> List[str]:
    """
    Beginner preflop rendering.

    Rules:
    - No percentages, no pot odds, no "range" or "equity" vocabulary.
    - Action-supportive framing: tell them WHAT to do and a simple WHY.
    - Mixed spots (tightness == TOSS_UP) append "This is a close decision."
    """
    scenario = obs.preflop_scenario
    action = obs.action
    pos = obs.hero_position or "this position"

    sentences: List[str] = []

    # --- RFI (Raise First In / open) ---
    if scenario == "rfi":
        if action == "RAISE":
            sentences.append(f"This hand is strong enough to open from {pos}.")
        else:  # FOLD
            sentences.append("This hand is too weak to open from here.")

    # --- DEFEND_CALL (facing one open, deciding to call/3bet/fold) ---
    elif scenario == "defend_call":
        if action == "CALL":
            sentences.append(
                "This hand is good enough to call here. You're getting a fair price."
            )
        elif action == "RAISE":
            sentences.append("This hand is strong enough to re-raise.")
        else:  # FOLD
            sentences.append(
                "This hand is not worth calling — it will lose too often."
            )

    # --- DEFEND_3BET (hero raised, now facing a re-raise) ---
    elif scenario == "defend_3bet":
        if action == "FOLD":
            sentences.append(
                "Facing a re-raise, most hands should fold. This one is too weak."
            )
        elif action == "RAISE":
            sentences.append("This hand is strong enough to re-raise.")
        else:  # CALL
            sentences.append(
                "This hand is worth continuing against the re-raise."
            )

    # --- BB_OPTION (unraised pot, BB to act) ---
    elif scenario == "bb_option":
        if action == "CHECK":
            sentences.append("You get to see the flop for free — check.")
        else:  # RAISE
            sentences.append("This hand is strong enough to raise here.")

    # --- SQUEEZE (open + caller(s), hero 3-bets) ---
    elif scenario == "squeeze":
        if action == "RAISE":
            sentences.append(
                "With a raiser and callers, this hand is strong enough to squeeze."
            )
        else:  # FOLD
            sentences.append("Not strong enough to squeeze here — fold.")

    else:
        # Fallback for any unrecognised scenario
        bucket_label = _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")
        sentences.append(f"You have a {bucket_label}.")

    # Mixed-spot qualifier (no percentages — just signal closeness)
    if obs.tightness == "TOSS_UP":
        sentences.append("This is a close decision.")

    return sentences


# =====================================================================
# INTERMEDIATE RENDERER
# =====================================================================

def render_intermediate(obs: SpotObservation) -> List[str]:
    """
    Render at Intermediate level: max 2-3 observations, poker vocabulary.

    Qualitative numbers. MUST include qualifier when counterintuitive.
    """
    # -- Preflop --
    if obs.is_preflop and obs.preflop_scenario is not None:
        return _render_intermediate_preflop(obs)

    sentences = []

    if obs.is_counterintuitive:
        sentences.append(_intermediate_counterintuitive(obs))
    else:
        sentences.append(_intermediate_standard(obs))

    # A-3: Multiplicative fold equity framing for bluffs (B1 fix)
    if obs.is_multiway and obs.strategic_role in ("pure_bluff", "semi_bluff"):
        if obs.strategic_role == "pure_bluff":
            sentences.append(
                (
                    f"Bluffing into {obs.num_opponents} opponents requires all of them "
                    f"to fold — fold equity is not just reduced, it is multiplicative: "
                    f"if each opponent folds 40% of the time at a typical sizing, "
                    f"the combined fold rate is 40% \u00d7 40% = 16%."
                )
                if obs.num_opponents == 2 else
                (
                    f"Bluffing into {obs.num_opponents} opponents requires all of them "
                    f"to fold — combined fold probability drops multiplicatively with "
                    f"each additional player, making pure bluffs unprofitable here."
                )
            )
        else:  # semi_bluff
            sentences.append(
                f"Your draw gives you a chance to improve, but with "
                f"{obs.num_opponents} opponents, fold equity is multiplicative — "
                f"each additional player who must fold dramatically reduces the "
                f"bluff component's profitability."
            )
    else:
        # --- Sentence candidates for slots 2 and 3 ---
        # Priority ordering per B6 / OQ-5:
        #   tier2: draw price, equity, fold justification
        #   tier3: board texture, villain range state
        #   tier4: tightness qualifier / confidence hedge
        #
        # Each candidate is a (stance, sentence) tuple.
        # Stance filtering removes sentences that contradict the oracle action.

        tier2_raw = []
        tier3_raw = []
        tier4_raw = []

        # D2: missed-draw river teaching — DEFENSIVE (only fires on CHECK)
        missed_draw = _missed_draw_river_sentence(obs, "intermediate")
        if missed_draw:
            tier2_raw.append((DEFENSIVE, missed_draw))

        # A-4: draw price framing — stance depends on content
        if obs.is_multiway and obs.has_draw and obs.facing_bet:
            draw_price = _draw_price_sentence(obs, "intermediate")
            if draw_price:
                # "right price to call" is AGGRESSIVE; "too large / fold" is DEFENSIVE
                dp_stance = AGGRESSIVE if obs.equity_margin > 0 else DEFENSIVE
                tier2_raw.append((dp_stance, draw_price))

        # A-10: shared burden of defense — stance matches its own action gate
        shared_burden = _shared_burden_sentence(obs, "intermediate")
        if shared_burden:
            # A-10 already gates on FOLD/CALL; FOLD text is DEFENSIVE, CALL text is AGGRESSIVE
            sb_stance = DEFENSIVE if obs.action == "FOLD" else AGGRESSIVE
            tier2_raw.append((sb_stance, shared_burden))

        # WI-17: protect checking range — NEUTRAL (explains why decision is close)
        protect_range = _protect_checking_range_sentence(obs, "intermediate")
        if protect_range:
            tier2_raw.append((NEUTRAL, protect_range))

        # WI-14: bet-and-call signal — DEFENSIVE (supports fold)
        bet_call = _bet_and_call_sentence(obs, "intermediate")
        if bet_call:
            tier2_raw.append((DEFENSIVE, bet_call))

        # WI-10: raise fold signal — DEFENSIVE (supports fold)
        raise_fold = _raise_fold_sentence(obs, "intermediate")
        if raise_fold:
            tier2_raw.append((DEFENSIVE, raise_fold))

        # WI-15: multi-street aggression — NEUTRAL (describes villain, not hero action)
        aggression = _multi_street_aggression_sentence(obs, "intermediate")
        if aggression:
            tier2_raw.append((NEUTRAL, aggression))

        # A-6: board texture multiway interaction — stance depends on content
        board_sentence = _board_texture_intermediate(obs)
        if board_sentence:
            # "supports a continuation bet" is AGGRESSIVE; "likely connected" is NEUTRAL
            bt_stance = AGGRESSIVE if "supports" in board_sentence.lower() else NEUTRAL
            tier3_raw.append((bt_stance, board_sentence))

        # A-11: capped range state — NEUTRAL (describes villain)
        range_sentence = _villain_range_sentence_intermediate(obs)
        if range_sentence:
            tier3_raw.append((NEUTRAL, range_sentence))

        # A-8: confidence hedge — NEUTRAL
        hedge = _confidence_hedge(obs, "intermediate")
        if hedge:
            tier4_raw.append((NEUTRAL, hedge))

        # Tightness qualifier — NEUTRAL
        if obs.tightness == "TOSS_UP":
            tier4_raw.append((NEUTRAL, "Both actions are reasonable here."))
        elif obs.tightness == "CLOSE":
            tier4_raw.append((NEUTRAL, "The other action is also reasonable here."))

        # Apply stance filter
        action = obs.action
        tier2 = _filter_by_stance(tier2_raw, action)
        tier3 = _filter_by_stance(tier3_raw, action)
        tier4 = _filter_by_stance(tier4_raw, action)

        # Apply priority ordering
        hand_assessment = sentences[0]  # already appended above
        remaining = _apply_sentence_priority(
            hand_assessment, tier2, tier3, tier4, cap=3
        )
        # remaining[0] is hand_assessment, which we already have
        sentences = remaining

    return sentences[:3]


def _intermediate_standard(obs: SpotObservation) -> str:
    """Standard intermediate framing."""
    action = obs.action
    hand_desc = obs.hand_description or _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")
    hand_cap = obs.hand_description_cap or hand_desc.capitalize()

    if action == "BET" or action == "RAISE":
        if obs.hand_bucket in ("monster", "strong_made"):
            return (
                f"Your {hand_desc} is ahead of most of {_possessive(obs.opponent_phrase)} "
                f"range — betting gets value from worse hands."
            )
        if obs.hand_bucket == "drawing":
            outs_part = f" with {obs.draw_outs} outs" if obs.draw_outs > 0 else ""
            return (
                f"Your {obs.draw_description or 'draw'}{outs_part} gives you a chance "
                f"to improve — betting adds fold equity."
            )
        # thin value / medium
        return (
            f"Your {hand_desc} can get value from some worse hands in "
            f"{_possessive(obs.opponent_phrase)} range."
        )

    if action == "FOLD":
        if obs.hand_bucket == "medium_made":
            return (
                f"Your {hand_desc} is behind most of what {obs.opponent_phrase} "
                f"can hold here — the price is too high to continue."
            )
        return (
            f"Your {hand_desc} is too weak against {_possessive(obs.opponent_phrase)} "
            f"range here."
        )

    if action == "CALL":
        if obs.has_draw:
            outs_part = f" with {obs.draw_outs} outs" if obs.draw_outs > 0 else ""
            return (
                f"Your {obs.draw_description or 'draw'}{outs_part} — "
                f"the price is right to continue."
            )
        return (
            f"Your {hand_desc} has enough equity against {_possessive(obs.opponent_phrase)} "
            f"range to continue."
        )

    # CHECK
    if obs.hand_bucket in ("monster", "strong_made"):
        return (
            f"Your {hand_desc} is ahead of most of {_possessive(obs.opponent_phrase)} "
            f"range — checking preserves showdown value."
        )
    return f"Your {hand_desc} has showdown value — checking is reasonable."


def _intermediate_counterintuitive(obs: SpotObservation) -> str:
    """Intermediate framing with required qualifier for counterintuitive spots."""
    action = obs.action
    hand_desc = obs.hand_description or _BUCKET_TO_BEGINNER.get(obs.hand_bucket, "hand")

    if action == "CHECK":
        # CHECK + strong/monster
        return (
            f"Your {hand_desc} is ahead — but few worse hands would call a bet, "
            f"so checking preserves value."
        )

    if action == "BET" or action == "RAISE":
        if obs.hand_bucket == "drawing":
            draw_name = obs.draw_description or "draw"
            return (
                f"Your {draw_name} combines fold equity with draw equity — "
                f"betting is stronger than checking."
            )
        # weak/air betting (pure bluff)
        return (
            f"Your {hand_desc} is weak, but betting applies pressure and can "
            f"win the pot without a showdown."
        )

    if action == "FOLD":
        if obs.counterintuitive_reason == "multiway_fold_discipline":
            return (
                f"Folding a made hand in a multiway pot is discipline, not "
                f"weakness — the combined opponent ranges beat your "
                f"{obs.hand_description or 'hand'} here."
            )
        return (
            f"Your {hand_desc} is reasonable, but {_possessive(obs.opponent_phrase)} range "
            f"is much stronger here."
        )

    if action == "CALL":
        if obs.has_draw:
            return (
                f"You're behind now, but your draw gives you the right price "
                f"to continue."
            )
        return (
            f"You're behind now, but your draw gives you the right price "
            f"to continue."
        )

    return f"Your {hand_desc}."


def _render_intermediate_preflop(obs: SpotObservation) -> List[str]:
    """
    Intermediate preflop rendering.

    Rules:
    - Poker vocabulary: position names, "opening range", "defending range", "pot odds".
    - Include range percentage for RFI and pot odds for calling scenarios.
    - Mixed spots: "GTO mixes between {action1} and {action2}."
    - Pot odds shown here (not at Beginner).
    """
    scenario = obs.preflop_scenario
    action = obs.action
    pos = obs.hero_position or "your position"
    opener_pos = obs.preflop_opener_position or "the opener"

    # Range percentage for this position (GTO opening ranges by position)
    range_pct = GTO_OPEN_PCT.get(pos, 0)

    sentences: List[str] = []

    # --- RFI ---
    if scenario == "rfi":
        if action == "RAISE":
            sentences.append(
                f"From {pos}, your opening range is ~{range_pct}% of hands — "
                f"this hand qualifies."
            )
        else:  # FOLD
            sentences.append(
                f"From {pos}, you open ~{range_pct}% of hands. "
                f"This hand is outside that range."
            )

    # --- DEFEND_CALL ---
    elif scenario == "defend_call":
        pot_odds = obs.pot_odds_pct
        if action == "CALL":
            sentences.append(
                f"Facing a raise from {opener_pos}, your defending range includes "
                f"this hand. You need ~{pot_odds:.0f}% equity — this hand exceeds that."
            )
        elif action == "RAISE":
            sentences.append(
                f"This hand is strong enough to re-raise from {pos}. "
                f"A 3-bet applies pressure and builds value."
            )
        else:  # FOLD
            sentences.append(
                f"Against a raise from {opener_pos}, your defending range is tight. "
                f"This hand doesn't have enough equity to justify the "
                f"{pot_odds:.0f}% you're putting in."
            )

    # --- DEFEND_3BET ---
    elif scenario == "defend_3bet":
        pot_odds = obs.pot_odds_pct
        if action == "FOLD":
            sentences.append(
                f"Facing a re-raise, most hands should fold. "
                f"You'd need ~{pot_odds:.0f}% equity — this hand doesn't meet that bar."
            )
        elif action == "RAISE":
            sentences.append(
                f"This hand is strong enough to 4-bet from {pos}. "
                f"Re-raising puts maximum pressure on the 3-bettor."
            )
        else:  # CALL
            sentences.append(
                f"This hand has enough equity to continue against the re-raise. "
                f"You need ~{pot_odds:.0f}% — this hand qualifies."
            )

    # --- BB_OPTION ---
    elif scenario == "bb_option":
        if action == "CHECK":
            sentences.append(
                "You're in the big blind with a free play — "
                "no reason to raise with this hand."
            )
        else:  # RAISE
            sentences.append(
                "You can isolate here. This hand plays better heads-up."
            )

    # --- SQUEEZE ---
    elif scenario == "squeeze":
        pot_odds = obs.pot_odds_pct
        if action == "RAISE":
            sentences.append(
                f"With {opener_pos}'s open and callers, you have extra fold equity. "
                f"This hand is strong enough to squeeze."
            )
        else:  # FOLD
            sentences.append(
                f"Squeezing requires a strong hand — this one doesn't have enough "
                f"equity against multiple players."
            )

    else:
        hand_desc = obs.hand_description or "hand"
        sentences.append(f"Your {hand_desc}.")

    # Mixed-spot qualifier using the two most likely actions
    if obs.tightness == "TOSS_UP":
        alt_action = "call" if action == "FOLD" else "fold"
        sentences.append(
            f"This is a borderline spot — GTO mixes between "
            f"{action.lower()} and {alt_action}."
        )
    elif obs.tightness == "CLOSE":
        sentences.append("The other action is also reasonable here.")

    return sentences


def _render_advanced_preflop(obs: SpotObservation) -> List[str]:
    """
    Advanced preflop rendering.

    Rules:
    - Full numbers: range frequency as percentage, pot odds, position.
    - GTO frequency from obs.preflop_range_frequency (0-1, multiply by 100 to display).
    - Pot odds shown for all calling/defending scenarios.
    - Mixed spots: "Mixed strategy: GTO frequency {freq:.0%}."
    """
    scenario = obs.preflop_scenario
    action = obs.action
    pos = obs.hero_position or "your position"
    opener_pos = obs.preflop_opener_position or "the opener"
    range_pct = GTO_OPEN_PCT.get(pos, 0)

    # Raw GTO frequency for this specific hand (0-1 → display as %)
    freq = obs.preflop_range_frequency
    freq_pct = freq * 100  # for display in f-strings using .0f

    pot_odds = obs.pot_odds_pct

    sentences: List[str] = []

    # --- RFI ---
    if scenario == "rfi":
        if action == "RAISE":
            sentences.append(
                f"This hand from {pos}: GTO opens this {freq_pct:.0f}% of the time. "
                f"Opening range is ~{range_pct}% of hands."
            )
        else:  # FOLD
            sentences.append(
                f"This hand from {pos}: GTO opens this {freq_pct:.0f}% — "
                f"outside the {range_pct}% opening range for this position."
            )

    # --- DEFEND_CALL ---
    elif scenario == "defend_call":
        if action == "CALL":
            sentences.append(
                f"Pot odds: {pot_odds:.0f}% equity needed. "
                f"This hand vs {opener_pos} range: in calling range at {freq_pct:.0f}% frequency."
            )
        elif action == "RAISE":
            sentences.append(
                f"This hand is in 3-bet range vs {opener_pos} at {freq_pct:.0f}%. "
                f"Polarized 3-bet: value + blocker logic."
            )
        else:  # FOLD
            sentences.append(
                f"Pot odds: {pot_odds:.0f}% needed. "
                f"This hand is not in calling or 3-bet range vs {opener_pos} — fold."
            )

    # --- DEFEND_3BET ---
    elif scenario == "defend_3bet":
        if action == "FOLD":
            sentences.append(
                f"Facing a 3-bet: pot odds {pot_odds:.0f}%. "
                f"This hand is not in 4-bet or call-3bet range — fold."
            )
        elif action == "RAISE":
            sentences.append(
                f"This hand is in 4-bet range at {freq_pct:.0f}%. "
                f"Pot odds {pot_odds:.0f}% — re-raise dominates."
            )
        else:  # CALL
            sentences.append(
                f"Pot odds: {pot_odds:.0f}% needed. "
                f"This hand is in call-3bet range at {freq_pct:.0f}% frequency."
            )

    # --- BB_OPTION ---
    elif scenario == "bb_option":
        if action == "CHECK":
            sentences.append(
                f"BB option in unraised pot. "
                f"This hand ({freq_pct:.0f}% isolation raise frequency) — check and take free play."
            )
        else:  # RAISE
            sentences.append(
                f"BB isolation raise: this hand qualifies at {freq_pct:.0f}% frequency. "
                f"Opening range ~{range_pct}% from BB."
            )

    # --- SQUEEZE ---
    elif scenario == "squeeze":
        if action == "RAISE":
            sentences.append(
                f"Squeeze vs {opener_pos} + callers at {freq_pct:.0f}% frequency. "
                f"Added fold equity from dead money in pot."
            )
        else:  # FOLD
            sentences.append(
                f"Pot odds: {pot_odds:.0f}% needed. "
                f"This hand is not in squeeze range vs {opener_pos} — fold."
            )

    else:
        hand_desc = obs.hand_description or "hand"
        sentences.append(f"Your {hand_desc}.")

    # Mixed-spot qualifier with full frequency
    if obs.tightness == "TOSS_UP":
        sentences.append(
            f"Mixed strategy: GTO frequency {freq:.0%}. "
            f"Both actions are near-EV-neutral."
        )
    elif obs.tightness == "CLOSE":
        sentences.append(
            f"Close decision: range frequency {freq:.0%}."
        )

    return sentences


# =====================================================================
# ADVANCED RENDERER
# =====================================================================

def render_advanced(obs: SpotObservation) -> List[str]:
    """
    Render at Advanced level: max 2-3 observations, full numbers.

    Range decomposition, blockers, equity percentages, strategic role naming.
    """
    # -- Preflop: use dedicated Advanced preflop renderer --
    if obs.is_preflop and obs.preflop_scenario is not None:
        return _render_advanced_preflop(obs)

    sentences = []

    # Observation 1: quantitative hand assessment
    sentences.append(_advanced_hand_assessment(obs))

    # A-7: geometric fold equity with opponent-count math (S-1, S-3 fixes)
    if obs.is_multiway and obs.strategic_role in ("pure_bluff", "semi_bluff"):
        n = obs.num_opponents
        if obs.strategic_role == "pure_bluff" and n > 0:
            # S-1 fix: use (0.40 ** n) * 100 for readability
            # S-3 fix: "at a typical sizing" qualifier on the 40% assumption
            per_opp_fold_rate = 0.40
            combined = (per_opp_fold_rate ** n) * 100
            sentences.append(
                f"Pure bluff into {n} opponents: at a typical sizing, assume each "
                f"opponent folds approximately 40% of the time — combined probability "
                f"all {n} fold is ({per_opp_fold_rate:.2f} ** {n}) * 100 "
                f"= ~{combined:.0f}%, insufficient for a profitable bluff."
            )
        elif obs.strategic_role == "semi_bluff" and n > 0:
            combined = (0.40 ** n) * 100
            draw_eq = obs.draw_equity * 100 if obs.draw_equity > 0 else 0
            sentences.append(
                f"Semi-bluff into {n} opponents: combined fold probability "
                f"~{combined:.0f}% at a typical sizing. "
                f"Draw equity ({draw_eq:.0f}%) carries more weight than fold equity here."
            )
        else:
            sentences.append(
                f"Multiway bluff: fold equity is sharply reduced with {n} opponents."
            )
    else:
        # Observation 2: draw price framing (A-4) takes priority over strategic frame
        # when is_multiway AND has_draw AND facing_bet
        # Stance-gate: draw price can be AGGRESSIVE ("call is profitable") or DEFENSIVE
        if obs.is_multiway and obs.has_draw and obs.facing_bet:
            draw_price = _draw_price_sentence(obs, "advanced")
            dp_stance = AGGRESSIVE if obs.equity_margin > 0 else DEFENSIVE
            if draw_price and _stance_ok(dp_stance, obs.action):
                sentences.append(draw_price)
            else:
                sentences.append(_advanced_strategic_frame(obs))
        else:
            sentences.append(_advanced_strategic_frame(obs))

    # D2 Advanced: missed-draw river teaching — DEFENSIVE
    missed_draw = _missed_draw_river_sentence(obs, "advanced")
    if missed_draw and _stance_ok(DEFENSIVE, obs.action):
        sentences.append(missed_draw)

    # WI-17 Advanced: protect checking range — NEUTRAL (explains close decision)
    protect_range = _protect_checking_range_sentence(obs, "advanced")
    if protect_range:
        sentences.append(protect_range)

    # A-10 Advanced: shared burden of defense — stance matches action
    shared = _shared_burden_sentence(obs, "advanced")
    if shared:
        sb_stance = DEFENSIVE if obs.action == "FOLD" else AGGRESSIVE
        if _stance_ok(sb_stance, obs.action):
            sentences.append(shared)

    # WI-14 Advanced: bet-and-call signal — DEFENSIVE
    bet_call = _bet_and_call_sentence(obs, "advanced")
    if bet_call and _stance_ok(DEFENSIVE, obs.action):
        sentences.append(bet_call)

    # WI-10 Advanced: raise fold signal — DEFENSIVE
    raise_fold = _raise_fold_sentence(obs, "advanced")
    if raise_fold and _stance_ok(DEFENSIVE, obs.action):
        sentences.append(raise_fold)

    # WI-15 Advanced: multi-street aggression — replaces generic strategic
    # frame when it fires (more informative than "pot control spot")
    aggression = _multi_street_aggression_sentence(obs, "advanced")
    if aggression:
        # Replace the strategic frame (sentence[1]) if it's generic
        if len(sentences) >= 2 and "pot control" in sentences[1].lower():
            sentences[1] = aggression
        else:
            sentences.append(aggression)

    # A-11 Advanced: capped range multiway qualification
    if (
        obs.villain_range_state == "capped"
        and obs.is_multiway
        and obs.villain_range_confidence > 0.5
    ):
        n_plus_one = obs.num_opponents + 1
        conf_pct = obs.villain_range_confidence
        sentences.append(
            f"Villain's range is capped (confidence: {conf_pct:.0%}). "
            f"In a {n_plus_one}-way pot, this is less exploitable than heads-up — "
            f"the remaining opponents share defensive burden, making aggressive "
            f"exploitation of the capped range risky."
        )

    # Villain composition (when meaningful data exists)
    if obs.villain_tp_plus_pct > 0 or obs.villain_draw_pct > 0 or obs.villain_air_pct > 0:
        tp = obs.villain_tp_plus_pct * 100
        draw = obs.villain_draw_pct * 100
        air = obs.villain_air_pct * 100
        if tp > 0 or draw > 0 or air > 0:
            sentences.append(
                f"Villain range: ~{tp:.0f}% value (TP+), ~{draw:.0f}% draws, "
                f"~{air:.0f}% air."
            )

    # A-8: confidence hedge (fires when tightness SILENCE but confidence is medium)
    # _confidence_hedge() suppresses itself when tightness is TOSS_UP or CLOSE,
    # so the existing tightness block and the hedge are mutually exclusive.
    hedge = _confidence_hedge(obs, "advanced")
    if hedge:
        sentences.append(hedge)

    # Tightness with gap numbers
    if obs.tightness == "TOSS_UP":
        sentences.append(
            f"Mixed spot: confidence {obs.confidence:.0%}. "
            f"Both actions are close to equilibrium."
        )
    elif obs.tightness == "CLOSE":
        sentences.append(
            f"Close decision: confidence {obs.confidence:.0%}. "
            f"The alternative action is also defensible."
        )

    return sentences[:3]


def _advanced_hand_assessment(obs: SpotObservation) -> str:
    """Observation 1 at Advanced: quantitative hand + equity position."""
    hand_cap = obs.hand_description_cap or obs.hand_description or "Hand"
    eq_pct = obs.equity * 100
    worse_pct = obs.worse_hand_pct * 100

    # Use hero_label from range decomposition when available
    label = obs.hero_label if obs.hero_label else hand_cap

    if obs.is_counterintuitive:
        return _advanced_counterintuitive(obs, label, eq_pct, worse_pct)

    if obs.has_draw and obs.hand_bucket == "drawing":
        draw_eq = obs.draw_equity * 100
        return (
            f"{label} with {obs.draw_outs} outs "
            f"({draw_eq:.0f}% draw equity, {eq_pct:.0f}% total equity)."
        )

    return f"{label} with {eq_pct:.0f}% equity. You beat {worse_pct:.0f}% of {_possessive(obs.opponent_phrase)} range."


def _advanced_counterintuitive(obs: SpotObservation, label: str,
                                eq_pct: float, worse_pct: float) -> str:
    """Advanced counterintuitive: explain with range data."""
    action = obs.action

    if action == "CHECK":
        vt = obs.value_target_pct * 100
        return (
            f"{label}. You beat {worse_pct:.0f}% but only {vt:.0f}% of "
            f"calling hands are worse. Thin value target."
        )

    if action in ("BET", "RAISE") and obs.hand_bucket == "drawing":
        draw_eq = obs.draw_equity * 100
        return (
            f"{obs.draw_description or 'Draw'} with {obs.draw_outs} outs "
            f"({draw_eq:.0f}% equity). Semi-bluff: fold equity + improvement."
        )

    if action in ("BET", "RAISE"):
        # Pure bluff with range data
        return (
            f"{label} with {eq_pct:.0f}% equity. "
            f"Range construction bluff — fold equity drives profitability."
        )

    if action == "FOLD":
        pot_odds = obs.pot_odds_pct
        if obs.counterintuitive_reason == "multiway_fold_discipline":
            return (
                f"{label} with {eq_pct:.0f}% equity, facing multiway pressure. "
                f"Combined opponent ranges make this a discipline fold — "
                f"the individual equity number is misleading when opponents' "
                f"ranges are both weighted toward strength."
            )
        # equity > pot_odds = surplus (still folding for range/multiway reasons)
        # equity < pot_odds = deficit (not getting the right price)
        if eq_pct > pot_odds:
            equity_label = "equity surplus"
            rationale = "range considerations make folding correct."
        else:
            equity_label = "equity deficit"
            rationale = "folding is correct."
        return (
            f"{label} with {eq_pct:.0f}% equity vs {pot_odds:.0f}% pot odds needed. "
            f"{equity_label.capitalize()} — {rationale}"
        )

    if action == "CALL":
        if obs.has_draw:
            draw_eq = obs.draw_equity * 100
            return (
                f"{label} — behind now but {obs.draw_outs} outs "
                f"({draw_eq:.0f}% draw equity) justify the call."
            )
        pot_odds = obs.pot_odds_pct
        return (
            f"{label} with {eq_pct:.0f}% equity vs {pot_odds:.0f}% pot odds. "
            f"Priced in to continue."
        )

    return f"{label} with {eq_pct:.0f}% equity."


def _advanced_strategic_frame(obs: SpotObservation) -> str:
    """Observation 2 at Advanced: strategic role + board/range context."""
    # Name the strategic role
    role_names = {
        "value_bet":        "Value bet spot",
        "thin_value":       "Thin value spot",
        "semi_bluff":       "Semi-bluff",
        "pure_bluff":       "Range construction bluff",
        "pot_control":      "Pot control spot",
        "showdown_value":   "Showdown value",
        "protection":       "Protection bet",
        "trap":             "Trapping spot",
        "mandatory_defend": "Mandatory defend",
        "priced_in":        "Priced in",
        "equity_denial":    "Equity denial fold",
        "range_fold":       "Range fold",
        "drawing_call":     "Drawing call",
    }
    role_name = role_names.get(obs.strategic_role, obs.strategic_role.replace("_", " ").title())

    # Board danger
    danger_pct = obs.danger_score * 100

    # Threats
    threats_part = ""
    if obs.top_threats:
        threats_part = f" Threats: {obs.top_threats}."

    # Blockers
    blocker_part = ""
    if obs.blocker_description:
        blocker_part = f" {obs.blocker_description}."

    return (
        f"{role_name}. Board danger {danger_pct:.0f}%.{threats_part}{blocker_part}"
    )


# =====================================================================
# DISPATCH (public API)
# =====================================================================

def render(obs: SpotObservation, level_index: int) -> List[str]:
    """
    Render a SpotObservation at the given teaching level.

    Args:
        obs: SpotObservation (frozen dataclass, single source of truth).
        level_index: 0=Beginner, 1=Intermediate, 2+=Advanced.

    Returns:
        List of 2-3 coaching sentences.
    """
    if level_index == 0:
        return render_beginner(obs)
    elif level_index == 1:
        return render_intermediate(obs)
    else:
        return render_advanced(obs)
