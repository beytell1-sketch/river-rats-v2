"""
SituationDescriber — generates 2-3 situation observation sentences per hand.

Observations are ordered by SHAP magnitude so the most model-important feature
cluster surfaces first. Tightness preview (if it fires) is always appended last
and is excluded from the SHAP sort.

Design:
  - 8 observation types, each with: eligibility condition, first_visible level,
    and a set of associated SHAP features used for sorting.
  - Top 2 eligible observations (SHAP-ordered) are selected; tightness appended.
  - Vocabulary is level-gated L1–L5 — never leak higher-level terms downward.
  - Pot odds formula: to_call / (pot_size + 2*to_call) — NOT the feature value.
"""

from typing import List, Dict, Tuple

from feature_keys import F
from coaching.levels import PlayerLevel, level_index, level_gte
from coaching.hand_context import HandContext


# ═══════════════════════════════════════════════════════════════════
# TIGHTNESS CONSTANTS
# ═══════════════════════════════════════════════════════════════════

_TOSS_UP_GAP = 0.20   # gap < 0.20 → "Both actions are reasonable here."
_CLOSE_GAP   = 0.35   # gap < 0.35 → "The other action is also reasonable here."


# ═══════════════════════════════════════════════════════════════════
# SHAP FEATURE GROUPS
# (used purely for sorting — higher max-abs-SHAP fires first)
# ═══════════════════════════════════════════════════════════════════

_SHAP_GROUPS: Dict[str, Tuple[str, ...]] = {
    "hand_strength":    ("equity_vs_range", "raw_equity", "hand_rank",
                         "worse_hand_pct", "better_hand_pct"),
    "draw_quality":     ("draw_outs", "has_flush_draw", "has_straight_draw"),
    "pot_odds":         ("pot_odds", "equity_margin", "to_call"),
    "board_texture":    ("danger_score", "connectivity_score",
                         "flush_danger", "straight_danger"),
    "range_advantage":  ("hero_position", "villain_position"),
    "spr_geometry":     ("spr",),
    "position_context": ("is_ip", "hero_position"),
    "blocker_analysis":  ("better_hand_pct", "worse_hand_pct", "hero_position"),
    "action_sequence":   ("facing_bet", "to_call"),
    # tightness_preview excluded — always last
}


# ═══════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════

def _shap_score(obs_name: str, shap_dict: Dict[str, float]) -> float:
    """Max absolute SHAP value across associated features for an observation."""
    features = _SHAP_GROUPS.get(obs_name, ())
    return max((abs(shap_dict.get(f, 0.0)) for f in features), default=0.0)


def _gap(pred) -> float:
    """Top-two probability gap from OraclePrediction."""
    sorted_probs = sorted(pred.probs.values(), reverse=True)
    if len(sorted_probs) < 2:
        return 1.0
    return sorted_probs[0] - sorted_probs[1]


def _correct_pot_odds_pct(feat_dict: Dict[str, float]) -> float:
    """
    Correct pot odds formula: to_call / (pot_size + 2 * to_call).

    In PokerBench data, pot_size is BEFORE villain's bet, and to_call IS
    the bet. Total pot after hero calls = pot_size + bet + call = pot_size + 2*to_call.
    Required equity = to_call / total.
    Returns percentage (0-100).
    """
    to_call = feat_dict.get("to_call", 0.0)
    pot_size = feat_dict.get("pot_size", 0.0)
    total = pot_size + 2 * to_call
    if total <= 0 or to_call <= 0:
        return 0.0
    return (to_call / total) * 100.0


# ═══════════════════════════════════════════════════════════════════
# VOCABULARY BUILDERS
# Each returns a single sentence string or None if it shouldn't fire
# for this level (level-gated observations return None below threshold).
# ═══════════════════════════════════════════════════════════════════

def _hand_strength(ctx: HandContext, feat_dict: Dict[str, float],
                   level: PlayerLevel) -> str:
    equity    = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    equity_pct = equity * 100.0
    worse_pct  = ctx.worse_hand_pct * 100.0
    better_pct = ctx.better_hand_pct * 100.0
    idx = level_index(level)

    if idx == 0:  # L1
        if equity > 0.60:
            return "You have a strong hand."
        if equity > 0.40:
            return "You have a decent hand."
        # Draw-aware: don't say "weak" if hero has a meaningful draw
        draw_outs = feat_dict.get("draw_outs", 0.0)
        if draw_outs >= 8 and ctx.better_hand_pct > 0.60:
            return "You have a draw -- your hand can improve to a very strong hand."
        if ctx.better_hand_pct > 0.60:
            return ("You have a weak hand -- you are behind most of what "
                    "your opponent could have.")
        if equity <= 0.20:
            return "You have a weak hand -- you cannot win at showdown."
        return "You have a decent hand."

    if idx == 1:  # L2
        draw_outs = feat_dict.get("draw_outs", 0.0)
        if ctx.worse_hand_pct > 0.70:
            return (f"You have {ctx.hand_description} -- your hand is ahead of "
                    f"most of {ctx.opponent_phrase}'s range.")
        if 0.40 <= ctx.worse_hand_pct <= 0.70:
            return (f"You have {ctx.hand_description} -- a solid but not "
                    f"dominant hand.")
        # Draw-aware reframe
        if draw_outs >= 8 and ctx.better_hand_pct > 0.60:
            return (f"You have {ctx.hand_description} -- not the best hand right "
                    f"now, but with strong drawing potential.")
        if draw_outs >= 4 and ctx.better_hand_pct > 0.60:
            return (f"You have {ctx.hand_description} -- behind for now, "
                    f"but with some outs to improve.")
        if ctx.better_hand_pct > 0.60:
            return (f"You have {ctx.hand_description} -- your hand is behind "
                    f"most of what {ctx.opponent_phrase} can hold.")
        if equity < 0.05:
            return (f"You have {ctx.hand_description} -- you have zero "
                    f"showdown value.")
        return f"You have {ctx.hand_description}."

    if idx == 2:  # L3
        return (f"{ctx.hand_description_cap} with {equity_pct:.0f}% equity. "
                f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range.")

    if idx == 3:  # L4
        rb = getattr(ctx, 'range_breakdown', None)
        if rb:
            threats = [b for b in rb.buckets if b.beats_hero > 0 and b.pct_of_range > 0.01][:3]
            threat_str = ""
            if threats:
                threat_parts = [f"{t.subcategory.replace('_', ' ')} ({t.pct_of_range*100:.1f}%)" for t in threats]
                threat_str = f" Threats: {', '.join(threat_parts)}."
            return (f"{rb.hero_label}. {equity_pct:.0f}% equity. "
                    f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range.{threat_str}")
        # Fallback to existing L4 text
        return (f"{ctx.hand_description_cap}: {equity_pct:.0f}% equity. "
                f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range, "
                f"{better_pct:.0f}% has you beat.")

    # L5 with range breakdown — tiered summary instead of flat subcategory list
    rb = getattr(ctx, 'range_breakdown', None)
    if rb:
        threats = [b for b in rb.buckets if b.beats_hero > 0 and b.pct_of_range > 0.01]
        threat_str = ""
        if threats:
            top_threats = threats[:3]
            threat_parts = [f"{t.subcategory.replace('_', ' ')} {t.pct_of_range*100:.0f}%" for t in top_threats]
            threat_str = f" Main threats: {', '.join(threat_parts)}."

        return (f"{rb.hero_label}. "
                f"Villain: {rb.better_pct*100:.0f}% beats you, "
                f"you beat {rb.worse_pct*100:.0f}%.{threat_str}")
    # Fallback
    return (f"{ctx.hand_description_cap} (cat {int(ctx.hand_category)}). "
            f"{equity_pct:.0f}% equity, {worse_pct:.0f}% worse_hand_pct.")


def _draw_quality(ctx: HandContext, feat_dict: Dict[str, float],
                  level: PlayerLevel) -> str:
    outs = ctx.draw_outs
    idx  = level_index(level)

    draw_eq = ctx.draw_equity if ctx.draw_equity > 0 else outs * 2.2
    draw_eq_pct = draw_eq * 100.0 if ctx.draw_equity > 0 else draw_eq

    if idx == 0:  # L1
        return "You have a draw -- your hand can improve to a very strong hand."

    if idx == 1:  # L2
        if outs >= 8:
            return (f"You have {ctx.hand_description} -- {outs:.0f} outs to "
                    f"make a powerful hand.")
        if outs >= 4:
            return (f"You have {ctx.hand_description} -- limited outs, but "
                    f"your hand has some potential.")
        return f"You have {ctx.hand_description} -- a small number of outs."

    if idx == 2:  # L3
        return (f"You have {ctx.hand_description} with {outs:.0f} outs.")

    if idx == 3:  # L4
        return (f"{ctx.hand_description_cap}: {outs:.0f} outs, approximately "
                f"{draw_eq_pct:.0f}% draw equity.")

    # L5
    return (f"{ctx.hand_description_cap} ({outs:.0f} outs, "
            f"{draw_eq_pct:.0f}% draw equity).")


def _pot_odds(ctx: HandContext, feat_dict: Dict[str, float],
              level: PlayerLevel) -> str:
    """L3+ only — caller guarantees level >= L3 before calling."""
    pot_odds_pct = _correct_pot_odds_pct(feat_dict)
    equity       = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    equity_pct   = equity * 100.0
    margin       = equity_pct - pot_odds_pct
    idx          = level_index(level)

    if idx == 2:  # L3
        return (f"The price requires {pot_odds_pct:.0f}% equity to continue. "
                f"Your hand has {equity_pct:.0f}%.")

    if idx == 3:  # L4
        return (f"Pot odds require {pot_odds_pct:.1f}% equity. "
                f"At {equity_pct:.1f}%, your equity margin is {margin:+.1f} points.")

    # L5
    return (f"Pot odds {pot_odds_pct:.1f}% vs {equity_pct:.1f}% equity. "
            f"Margin {margin:+.1f}%.")


def _board_texture(ctx: HandContext, feat_dict: Dict[str, float],
                   level: PlayerLevel) -> str:
    danger       = feat_dict.get("danger_score", 0.0)
    connectivity = feat_dict.get("connectivity_score", 0.0)
    is_rainbow   = feat_dict.get("is_rainbow", 0) > 0.5
    is_two_tone  = feat_dict.get("is_two_tone", 0) > 0.5
    is_monotone  = feat_dict.get("is_monotone", 0) > 0.5
    is_river     = feat_dict.get("street", 0) == 2.0
    idx          = level_index(level)

    # Range composition from HandContext (Phase 4B features)
    tp_pct  = ctx.villain_top_pair_plus_pct
    draw_pct = ctx.villain_draw_pct
    air_pct  = ctx.villain_air_pct
    capped   = ctx.villain_range_capped

    if idx == 0:  # L1 — simple, specific
        if danger < 0.30:
            if capped:
                return "The board is safe and your opponent's range is limited."
            return "The board is safe -- few hands connect here."
        # Use range composition for specificity
        if tp_pct > 0.30:
            return ("This board hits your opponent's range hard -- "
                    "many of their hands connect.")
        if is_monotone:
            return "The board is all one suit -- flushes are a real threat."
        if draw_pct > 0.20 and not is_river:
            return "The board is draw-heavy -- your opponent may be drawing."
        if connectivity >= 8:
            return "The board is very connected -- straights and strong hands are possible."
        if air_pct > 0.50:
            return "The board misses most of your opponent's range."
        return "The board has some danger -- be cautious."

    if idx == 1:  # L2 — cause-effect, range-aware
        if danger < 0.30:
            if is_rainbow and connectivity < 4:
                if capped:
                    return ("The board is dry and disconnected -- your opponent's "
                            "range is capped with few strong holdings here.")
                return ("The board is dry and disconnected -- very few of "
                        f"{ctx.opponent_phrase}'s hands connect.")
            return f"The board is relatively safe for your hand."

        if is_monotone:
            if is_river:
                return "The board is all one suit -- flushes are possible."
            return "The board is all one suit -- flush draws dominate this texture."
        if tp_pct > 0.30:
            return (f"This board connects well with {ctx.opponent_phrase}'s range "
                    "-- many of their hands have a pair or better.")
        if draw_pct > 0.20 and not is_river:
            return (f"This board creates drawing opportunities for "
                    f"{ctx.opponent_phrase} -- flush and straight draws are in play.")
        if air_pct > 0.50:
            return (f"This board misses most of {ctx.opponent_phrase}'s range "
                    "-- they have many weak holdings here.")
        if connectivity >= 8:
            return "The board is very connected -- straights and two pairs are possible."
        return f"The board has moderate texture -- some of {ctx.opponent_phrase}'s range connects."

    # L3+: include numbers and range composition
    parts = []

    # Texture descriptor
    if danger < 0.30:
        parts.append(f"The board is safe (danger {danger:.2f}, connectivity {connectivity:.0f})")
    elif danger <= 0.60:
        parts.append(f"The board is moderately textured (danger {danger:.2f}, connectivity {connectivity:.0f})")
    else:
        parts.append(f"The board is dangerous (danger {danger:.2f}, connectivity {connectivity:.0f})")

    # Range composition (the specific part)
    if idx >= 3:  # L4+ gets percentages
        if tp_pct > 0.05:
            parts.append(f"{tp_pct*100:.0f}% of {ctx.opponent_phrase}'s range is top pair or better")
        if draw_pct > 0.05 and not is_river:
            parts.append(f"{draw_pct*100:.0f}% is drawing")
        if air_pct > 0.20:
            parts.append(f"{air_pct*100:.0f}% is air")
    else:  # L3 gets qualitative
        if tp_pct > 0.30:
            parts.append(f"{ctx.opponent_phrase}'s range hits this board hard")
        elif tp_pct < 0.10:
            parts.append(f"few hands in {ctx.opponent_phrase}'s range connect")
        if draw_pct > 0.20 and not is_river:
            parts.append("draws are significant on this texture")
        if capped:
            parts.append(f"{ctx.opponent_phrase}'s range is capped")

    return " -- ".join(parts) + "."


def _range_advantage(ctx: HandContext, feat_dict: Dict[str, float],
                     level: PlayerLevel) -> str:
    """L3+ only — caller guarantees level >= L3 before calling."""
    pfr     = ctx.pfr_advantage
    pfr_pct = pfr * 100.0
    idx     = level_index(level)

    if idx == 2:  # L3
        if pfr > 0.55:
            return (f"As {ctx.hero_position_name}, your range connects better "
                    f"with this board.")
        return "This board connects better with your opponent's range than yours."

    if idx == 3:  # L4
        return (f"Range advantage: ~{pfr_pct:.0f}% as "
                f"{ctx.hero_position_name} on this texture.")

    # L5
    return (f"{ctx.hero_position_name} has ~{pfr_pct:.0f}% range advantage. "
            f"Range dynamics shape frequency splits.")


def _spr_geometry(ctx: HandContext, feat_dict: Dict[str, float],
                  level: PlayerLevel) -> str:
    """L3+ only — caller guarantees level >= L3 before calling."""
    spr = ctx.spr
    idx = level_index(level)

    # Build context phrase used at L4/L5
    if spr < 1.5:
        context_phrase = "You are in stack-commitment territory."
    elif spr <= 4.0:
        context_phrase = "A single bet can commit meaningful stack depth."
    else:  # spr > 10 (eligibility guard ensures this)
        context_phrase = "Deep stacks favor positional play."

    if idx == 2:  # L3
        if spr < 1.5:
            return f"With SPR {spr:.1f}, you are in stack-commitment territory."
        if spr <= 4.0:
            return (f"With SPR {spr:.1f}, a single bet can commit meaningful "
                    f"stack depth.")
        return f"With SPR {spr:.1f}, deep stacks favor positional play."

    if idx == 3:  # L4
        return f"SPR {spr:.1f}. {context_phrase}"

    # L5
    return (f"SPR {spr:.1f}. {context_phrase} "
            f"Stack geometry is a primary constraint.")


def _position_context(ctx: HandContext, feat_dict: Dict[str, float],
                      level: PlayerLevel) -> str:
    idx = level_index(level)

    if idx == 0:  # L1
        if ctx.is_ip:
            return "You are in position -- you act last, which is an advantage."
        return "You are out of position -- your opponent acts last."

    if idx == 1:  # L2
        if ctx.is_ip:
            return (f"You have position on {ctx.opponent_phrase} -- you see "
                    f"how they act first.")
        return (f"You are out of position against {ctx.opponent_phrase} -- "
                f"you must act first.")

    if idx in (2, 3):  # L3, L4
        if ctx.is_ip:
            return (f"You are {ctx.hero_position_name}, acting last on the "
                    f"{ctx.street_name}.")
        return (f"You are {ctx.hero_position_name} out of position on the "
                f"{ctx.street_name}.")

    # L5
    ip_str = "IP" if ctx.is_ip else "OOP"
    return (f"Position: {ctx.hero_position_name} vs "
            f"{ctx.villain_position_name}, {ip_str}.")


def _blocker_analysis(ctx: HandContext, feat_dict: Dict[str, float],
                      level: PlayerLevel) -> str:
    """L5 only: blocker analysis with strategic implications."""
    rb = getattr(ctx, 'range_breakdown', None)
    if rb is None:
        return None
    bi = rb.blocker_info
    if bi.total_blocked == 0:
        return None

    # Strategic implication, not raw numbers
    if bi.blocks_value:
        return ("Your cards block villain's value hands — "
                "they are less likely to have the nuts here.")
    if bi.blocks_bluffs:
        return ("Your cards block villain's bluffing hands — "
                "their bets are more likely to be real.")
    # Fallback with count
    if bi.total_blocked > 10:
        return f"Your cards remove {bi.total_blocked} combos from villain's range."
    return None


def _action_sequence(ctx: HandContext, feat_dict: Dict[str, float],
                     level: PlayerLevel) -> str:
    """Note when facing a raise (not just a bet)."""
    num_raises = feat_dict.get(F.META_NUM_RAISES, 0)
    if num_raises == 0:
        return None

    idx = level_index(level)
    if idx <= 1:  # L1-L2
        if num_raises == 1:
            return "You are facing a raise -- this represents significant strength."
        return "You are facing a re-raise -- this represents very strong hands."
    # L3+
    if num_raises == 1:
        return ("Facing a raise over a bet -- villain's range is much "
                "stronger than a single bettor's range.")
    return ("Facing a re-raise -- villain's range is heavily "
            "polarized toward premium hands and strong draws.")


def _soften_for_check(ctx: HandContext, feat_dict: Dict[str, float],
                      level: PlayerLevel) -> str:
    """Reframe hand_strength when GTO checks a strong hand (L1-L2)."""
    idx = level_index(level)
    if idx == 0:  # L1
        return "You have a strong hand with good showdown value."
    # L2
    return (f"You have {ctx.hand_description} -- a strong hand "
            f"that does not need to build the pot right now.")


def _type2_bridge(action: str, ctx: HandContext,
                  feat_dict: Dict[str, float]) -> str:
    """
    Type 2 behavioral bridging statement — factual observation about solver
    patterns, NOT a causal claim. Only fires at L2 when contradiction detected.
    """
    draw_outs = feat_dict.get("draw_outs", 0.0)
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity

    # CHECK + strong hand
    if action == 'CHECK' and equity > 0.55:
        return "GTO sometimes checks strong hands in this position."

    # BET/RAISE + weak hand (semi-bluff)
    if action in ('BET', 'RAISE') and draw_outs >= 4 and ctx.better_hand_pct > 0.50:
        return "Betting with draws is a common pattern in this spot."

    # BET + weak hand (pure bluff on dry board)
    if action in ('BET', 'RAISE') and draw_outs < 4 and ctx.better_hand_pct > 0.60:
        return "GTO includes some bets with weaker hands on this board."

    # CALL + behind with draws
    if action == 'CALL' and draw_outs >= 8 and ctx.better_hand_pct > 0.50:
        return "Draws with this many outs regularly call at this price."

    return None  # No bridge needed


def _tightness_preview(pred, gap_value: float) -> str | None:
    """Returns the tightness sentence, or None if SILENCE (gap >= 0.35)."""
    if gap_value < _TOSS_UP_GAP:
        return "Both actions are reasonable here."
    if gap_value < _CLOSE_GAP:
        return "The other action is also reasonable here."
    return None


# ═══════════════════════════════════════════════════════════════════
# MAIN CLASS
# ═══════════════════════════════════════════════════════════════════

class SituationDescriber:
    """
    Generates 2-3 situation observation sentences for a single hand.

    Observations are selected by:
      1. Eligibility (feature condition + level gate)
      2. SHAP ordering (highest max-abs-SHAP among associated features)
      3. Selection cap (top 2 non-tightness + tightness preview if it fires)
    """

    def describe(
        self,
        ctx: HandContext,
        feat_dict: Dict[str, float],
        shap_dict: Dict[str, float],
        pred,
        level: PlayerLevel,
    ) -> List[str]:
        """
        Produce 2-3 situation observation sentences.

        Args:
            ctx:       HandContext for this hand
            feat_dict: dict of 37 feature name → float
            shap_dict: dict of feature_name → shap_value
            pred:      OraclePrediction (used for gap computation)
            level:     PlayerLevel controlling vocabulary gate

        Returns:
            List[str] of 2-3 sentences.
        """
        eligible = self._collect_eligible(ctx, feat_dict, shap_dict, level)

        # Separate hand_strength (guaranteed first) and action_sequence
        # (forced slot 2 when it fires) from SHAP-sorted rest
        hand_strength_obs = None
        action_sequence_obs = None
        rest = []
        for name, score, sentence in eligible:
            if name == "hand_strength":
                hand_strength_obs = sentence
            elif name == "action_sequence":
                action_sequence_obs = sentence
            elif name != "tightness_preview":
                rest.append((name, score, sentence))

        # SHAP-sort the rest for slot 2
        rest.sort(key=lambda x: x[1], reverse=True)

        # Get action from oracle prediction
        idx = level_index(level)
        action = pred.action.upper() if hasattr(pred, 'action') else ''

        # --- L1-L2: Action-coherence reordering ---
        if idx <= 1 and hand_strength_obs:
            obs_lower = hand_strength_obs.lower()
            is_strong = any(w in obs_lower for w in
                           ['ahead', 'strong hand', 'showdown value',
                            'strong drawing'])
            is_weak = any(w in obs_lower for w in
                         ['behind', 'weak hand'])

            action_is_passive = action in ('CHECK', 'FOLD')
            action_is_aggressive = action in ('BET', 'RAISE')

            contradiction = ((is_strong and action_is_passive) or
                             (is_weak and action_is_aggressive))

            if contradiction and rest:
                # Action-aligned obs first, hand strength second
                second_obs = rest[0][2]

                # Fix 3: Suppress "capped" on FOLD
                if action == 'FOLD' and (
                    'capped' in second_obs.lower()
                    or 'range is limited' in second_obs.lower()
                ):
                    if feat_dict.get('facing_bet', 0):
                        second_obs = (f"When {ctx.opponent_phrase} bets, "
                                      "they usually have a strong range.")
                    else:
                        second_obs = ("Your hand does not have enough "
                                      "value to continue.")

                selected = [second_obs, hand_strength_obs]
            else:
                selected = []
                if hand_strength_obs:
                    selected.append(hand_strength_obs)
                if rest:
                    selected.append(rest[0][2])
        else:
            # L3+: Original behavior (hand_strength first, SHAP-sorted second)
            selected = []
            if hand_strength_obs:
                selected.append(hand_strength_obs)
            if rest:
                selected.append(rest[0][2])

        # Action sequence observation: force into slot 2 when facing a raise
        if action_sequence_obs is not None:
            if len(selected) >= 2:
                selected[1] = action_sequence_obs
            else:
                selected.append(action_sequence_obs)

        # Fix 3 continued: suppress "capped" on FOLD even without contradiction
        if idx <= 1 and action == 'FOLD':
            for i, obs in enumerate(selected):
                if ('capped' in obs.lower()
                        or 'range is limited' in obs.lower()):
                    if feat_dict.get('facing_bet', 0):
                        selected[i] = (f"When {ctx.opponent_phrase} bets, "
                                       "they usually have a strong range.")
                    else:
                        selected[i] = ("Your hand does not have enough "
                                       "value to continue.")

        # L5 aggression teaching: when GTO bets/raises with a weak hand
        if idx >= 4 and action in ('BET', 'RAISE'):
            rb = getattr(ctx, 'range_breakdown', None)
            if rb and rb.better_pct > 0.50:
                # Replace hand_strength obs with aggression-framing obs
                draw_outs = feat_dict.get('draw_outs', 0)
                if draw_outs >= 8:
                    aggression_obs = (f"{rb.hero_label}. Semi-bluff: "
                                     f"not the best hand, but {int(draw_outs)} outs "
                                     f"plus fold equity make this a profitable bet.")
                else:
                    aggression_obs = (f"{rb.hero_label}. Range construction bluff: "
                                     f"this hand needs to be in your betting range "
                                     f"to keep villain from overly exploiting your checks.")
                # Replace the first observation
                if selected:
                    selected[0] = aggression_obs

        # Append tightness preview if it fires
        gap_value = _gap(pred)
        tightness = _tightness_preview(pred, gap_value)

        # Type 2 bridging at L3+ ONLY (data shows it hurts at L2)
        if idx >= 2:  # L3+
            bridge = _type2_bridge(action, ctx, feat_dict)
            if bridge:
                selected.append(bridge)
            elif tightness is not None:
                selected.append(tightness)
        elif tightness is not None:
            # L1-L2: still append tightness (but NO bridging)
            selected.append(tightness)

        return selected

    def _collect_eligible(
        self,
        ctx: HandContext,
        feat_dict: Dict[str, float],
        shap_dict: Dict[str, float],
        level: PlayerLevel,
    ) -> List[Tuple[str, float, str]]:
        """
        Return list of (obs_name, shap_score, sentence) for every
        observation that passes its eligibility gate.
        """
        results = []

        # --- 1. hand_strength (always fires, L1+) ---
        sentence = _hand_strength(ctx, feat_dict, level)
        results.append(("hand_strength", 0.0, sentence))

        # --- 1b. action_sequence (num_raises >= 1, all levels) ---
        num_raises = feat_dict.get(F.META_NUM_RAISES, 0)
        if num_raises >= 1:
            sentence = _action_sequence(ctx, feat_dict, level)
            if sentence is not None:
                # High forced score so it surfaces as slot 2 (after hand_strength)
                results.append(("action_sequence", 0.0, sentence))

        # --- 2. draw_quality (draw_outs > 0 AND street != river) ---
        draw_outs = feat_dict.get("draw_outs", 0.0)
        street    = feat_dict.get("street", 0.0)
        if draw_outs > 0 and street != 2:
            sentence = _draw_quality(ctx, feat_dict, level)
            results.append(("draw_quality", 0.0, sentence))

        # --- 3. pot_odds (facing_bet == 1 AND level >= L3) ---
        facing_bet = feat_dict.get("facing_bet", 0)
        if facing_bet == 1 and level_gte(level, PlayerLevel.L3_ARCHITECTURE):
            sentence = _pot_odds(ctx, feat_dict, level)
            results.append(("pot_odds", 0.0, sentence))

        # --- 4. board_texture (always fires, L1+) ---
        sentence = _board_texture(ctx, feat_dict, level)
        results.append(("board_texture", 0.0, sentence))

        # --- 5. range_advantage (L3+ AND pfr_advantage deviates from 0.5) ---
        pfr = ctx.pfr_advantage
        if level_gte(level, PlayerLevel.L3_ARCHITECTURE) and (pfr > 0.55 or pfr < 0.45):
            sentence = _range_advantage(ctx, feat_dict, level)
            results.append(("range_advantage", 0.0, sentence))

        # --- 6. spr_geometry (L3+ AND spr < 4 or spr > 10) ---
        spr = ctx.spr
        if level_gte(level, PlayerLevel.L3_ARCHITECTURE) and (spr < 4.0 or spr > 10.0):
            sentence = _spr_geometry(ctx, feat_dict, level)
            results.append(("spr_geometry", 0.0, sentence))

        # --- 7. position_context (always fires, L1+) ---
        sentence = _position_context(ctx, feat_dict, level)
        results.append(("position_context", 0.0, sentence))

        # --- 8. blocker_analysis (L5 only, needs range_breakdown) ---
        if level_gte(level, PlayerLevel.L5_SYSTEMS):
            rb = getattr(ctx, 'range_breakdown', None)
            if rb and rb.blocker_info.total_blocked > 0:
                sentence = _blocker_analysis(ctx, feat_dict, level)
                if sentence:
                    results.append(("blocker_analysis", 0.0, sentence))

        # Now apply real SHAP scores using the shap_dict
        scored = []
        for name, _, sentence in results:
            score = _shap_score(name, shap_dict)
            scored.append((name, score, sentence))

        return scored
