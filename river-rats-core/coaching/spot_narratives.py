"""
Spot Narratives -- the catalog of action-coherent teaching narratives.

Each entry is keyed by (action, strategic_role, level) and contains
2-3 narrative functions that produce observation sentences.

Phase 2: 6 core spots x 5 levels = 30 catalog entries covering the
highest-frequency teaching spots.
"""
from dataclasses import dataclass, field
from typing import Callable, List, Optional


NarrativeFn = Callable  # (ctx, feat_dict, range_breakdown) -> Optional[str]


@dataclass
class SpotNarrative:
    """Teaching narrative for one (action, role, level) combination."""
    observations: List[NarrativeFn] = field(default_factory=list)


# =====================================================================
# HELPER: board texture description
# =====================================================================

def _board_texture_l1(ctx):
    """L1: Simple safe/dangerous board description."""
    danger = ctx.danger_score
    if danger < 0.30:
        return "The board is safe — few hands connect."
    elif danger > 0.60:
        return "The board is dangerous — many hands connect."
    return "The board has some draws possible."


def _board_texture_l2(ctx):
    """L2: Board texture with opponent phrase."""
    danger = ctx.danger_score
    if danger < 0.30:
        return (f"The board is dry and disconnected — few of "
                f"{ctx.opponent_phrase}'s hands connect.")
    elif danger > 0.60:
        return (f"The board is coordinated — but your hand is strong "
                f"enough to check and evaluate on later streets.")
    return (f"The board has moderate texture — checking controls "
            f"the pot size while maintaining your range balance.")


def _board_texture_l3(ctx):
    """L3: Board texture with danger percentage."""
    danger = ctx.danger_score
    danger_pct = danger * 100
    if danger < 0.30:
        return (f"Board danger is low ({danger_pct:.0f}%) — "
                f"few draws or connecting hands are present.")
    elif danger > 0.60:
        return (f"Board danger is elevated ({danger_pct:.0f}%) — "
                f"draws and connected hands are present, "
                f"but pot control preserves your equity.")
    return (f"Board danger is moderate ({danger_pct:.0f}%) — "
            f"enough texture to warrant caution.")


# =====================================================================
# SPOT 1: CHECK + pot_control (strong hand checking)
# =====================================================================

def _check_potcontrol_obs1_l1(ctx, feat_dict, rb):
    return "You have a strong hand with good showdown value."

def _check_potcontrol_obs2_l1(ctx, feat_dict, rb):
    return _board_texture_l1(ctx)


def _check_potcontrol_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} {ctx.hand_verb} ahead of most of "
            f"{ctx.opponent_phrase}'s range — checking here "
            f"preserves showdown value.")

def _check_potcontrol_obs2_l2(ctx, feat_dict, rb):
    return _board_texture_l2(ctx)


def _check_potcontrol_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range, "
            f"but betting targets only the slice that calls with worse.")

def _check_potcontrol_obs2_l3(ctx, feat_dict, rb):
    return _board_texture_l3(ctx)


def _check_potcontrol_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    better_pct = ctx.better_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of {ctx.opponent_phrase}'s range is worse, "
            f"{better_pct:.0f}% is better.")

def _check_potcontrol_obs2_l4(ctx, feat_dict, rb):
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    danger = ctx.danger_score
    threats = []
    if danger > 0.40:
        threats.append("draws present")
    if ctx.better_hand_pct > 0.15:
        threats.append(f"{ctx.better_hand_pct*100:.0f}% of range has you beat")
    threat_str = "; ".join(threats) if threats else "board is static"
    return (f"Threats: {threat_str}. "
            f"Betting targets thin value: only {value_target:.0f}% "
            f"would call with worse.")


def _check_potcontrol_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity "
            f"against {ctx.opponent_phrase}'s continuing range. "
            f"You beat {worse_pct:.0f}% overall but the calling range "
            f"is polarised toward better hands and draws.")

def _check_potcontrol_obs2_l5(ctx, feat_dict, rb):
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"Pot control spot. Thin value target insufficient for a bet — "
            f"only {value_target:.0f}% of the calling range is worse. "
            f"Checking preserves equity realisation and avoids "
            f"inflating the pot against a stronger range.")


# =====================================================================
# SPOT 2: BET + value_bet (strong hand betting for value)
# =====================================================================

def _bet_value_obs1_l1(ctx, feat_dict, rb):
    return "You have a strong hand — betting builds the pot."

def _bet_value_obs2_l1(ctx, feat_dict, rb):
    return _board_texture_l1(ctx)


def _bet_value_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} {ctx.hand_verb} ahead — "
            f"betting gets value from worse hands in "
            f"{ctx.opponent_phrase}'s range.")

def _bet_value_obs2_l2(ctx, feat_dict, rb):
    return _board_texture_l2(ctx)


def _bet_value_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range — "
            f"enough worse hands call to make betting profitable.")

def _bet_value_obs2_l3(ctx, feat_dict, rb):
    return _board_texture_l3(ctx)


def _bet_value_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of {ctx.opponent_phrase}'s range is worse. "
            f"Value target: {value_target:.0f}% of the calling range pays off.")

def _bet_value_obs2_l4(ctx, feat_dict, rb):
    danger = ctx.danger_score
    if danger > 0.50:
        return (f"Board danger is {danger*100:.0f}% — betting also denies "
                f"equity to draws that could overtake you.")
    return (f"Board danger is {danger*100:.0f}% — a stable board "
            f"means your value bet is straightforward.")


def _bet_value_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of the overall range is worse; "
            f"{value_target:.0f}% of the calling range pays off. "
            f"Clear value bet in your range construction.")

def _bet_value_obs2_l5(ctx, feat_dict, rb):
    return (f"This hand anchors the value portion of your betting range. "
            f"Balance requires mixing in bluffs at the appropriate frequency.")


# =====================================================================
# SPOT 3: FOLD + equity_denial (weak hand folding)
# =====================================================================

def _fold_equity_obs1_l1(ctx, feat_dict, rb):
    return "Your hand is too weak to continue."

def _fold_equity_obs2_l1(ctx, feat_dict, rb):
    return "Folding saves chips for better opportunities."


def _fold_equity_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} {ctx.hand_verb} behind most of "
            f"what {ctx.opponent_phrase} can hold — folding cuts your losses.")

def _fold_equity_obs2_l2(ctx, feat_dict, rb):
    if ctx.danger_score > 0.50:
        return (f"The board is coordinated — even if you improve, "
                f"{ctx.opponent_phrase} likely has stronger draws or made hands.")
    return (f"Without enough equity to continue, folding is the "
            f"disciplined play.")


def _fold_equity_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    equity_pct = equity * 100
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"{ctx.hand_description_cap} with only {equity_pct:.0f}% equity. "
            f"You need {pot_odds_pct:.0f}% to call — the equity deficit "
            f"makes continuing unprofitable.")

def _fold_equity_obs2_l3(ctx, feat_dict, rb):
    better_pct = ctx.better_hand_pct * 100
    return (f"{better_pct:.0f}% of {ctx.opponent_phrase}'s range "
            f"has you beat — the price is wrong to continue.")


def _fold_equity_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    equity_pct = equity * 100
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    deficit = pot_odds_pct - equity_pct
    return (f"{ctx.hand_description_cap} — {equity_pct:.0f}% equity "
            f"vs {pot_odds_pct:.0f}% needed. "
            f"Equity deficit of {deficit:.0f}pp makes this a clear fold.")

def _fold_equity_obs2_l4(ctx, feat_dict, rb):
    worse_pct = ctx.worse_hand_pct * 100
    better_pct = ctx.better_hand_pct * 100
    return (f"Range position: only {worse_pct:.0f}% of "
            f"{ctx.opponent_phrase}'s range is worse, "
            f"{better_pct:.0f}% is better.")


def _fold_equity_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity "
            f"against {ctx.opponent_phrase}'s betting range. "
            f"Pot odds require {pot_odds_pct:.0f}% — this hand falls below "
            f"your minimum defence frequency.")

def _fold_equity_obs2_l5(ctx, feat_dict, rb):
    return (f"This hand belongs in the folding portion of your range. "
            f"Defending here would over-defend against "
            f"{ctx.opponent_phrase}'s value-heavy range.")


# =====================================================================
# SPOT 4: CALL + drawing_call (calling with a draw)
# =====================================================================

def _call_draw_obs1_l1(ctx, feat_dict, rb):
    return "You have a draw — your hand can improve to a very strong hand."

def _call_draw_obs2_l1(ctx, feat_dict, rb):
    return "The price is right to see another card."


def _call_draw_obs1_l2(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    return (f"Your {ctx.hand_description} has {outs} outs — "
            f"the price is right to continue.")

def _call_draw_obs2_l2(ctx, feat_dict, rb):
    return (f"Calling keeps you in the pot with a chance to make "
            f"a strong hand on a later street.")


def _call_draw_obs1_l3(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Drawing hand: {outs} outs (~{draw_equity_pct:.0f}% on next card). "
            f"Pot odds require {pot_odds_pct:.0f}% equity — "
            f"your draw {'meets' if draw_equity_pct >= pot_odds_pct else 'nearly meets'} "
            f"the threshold.")

def _call_draw_obs2_l3(ctx, feat_dict, rb):
    if ctx.spr > 3.0:
        return (f"With an SPR of {ctx.spr:.1f}, implied odds add significant "
                f"value when you hit.")
    return (f"SPR is {ctx.spr:.1f} — implied odds are limited, "
            f"but the direct price is sufficient.")


def _call_draw_obs1_l4(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Drawing call: {outs} outs, {draw_equity_pct:.0f}% draw equity, "
            f"{equity*100:.0f}% total equity vs range. "
            f"Need {pot_odds_pct:.0f}% — direct odds "
            f"{'plus implied odds justify' if draw_equity_pct < pot_odds_pct else 'justify'} "
            f"the call.")

def _call_draw_obs2_l4(ctx, feat_dict, rb):
    return (f"SPR {ctx.spr:.1f} — "
            f"{'deep stacks amplify implied odds when you hit' if ctx.spr > 3.0 else 'shallow stacks limit implied odds but direct odds compensate'}.")


def _call_draw_obs1_l5(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Range analysis: {ctx.hand_description} with {outs} outs "
            f"({draw_equity_pct:.0f}% improvement equity). "
            f"Total equity {equity*100:.0f}% vs {ctx.opponent_phrase}'s range. "
            f"Pot odds {pot_odds_pct:.0f}% — call is +EV with implied odds factored.")

def _call_draw_obs2_l5(ctx, feat_dict, rb):
    return (f"This draw anchors the calling portion of your range. "
            f"Folding here would make your calling range too "
            f"value-heavy and exploitable.")


# =====================================================================
# SPOT 5: BET + semi_bluff (betting with a draw)
# =====================================================================

def _bet_semibluff_obs1_l1(ctx, feat_dict, rb):
    return "You have a draw — betting gives you two ways to win."

def _bet_semibluff_obs2_l1(ctx, feat_dict, rb):
    return "You can win now if your opponent folds, or improve on a later card."


def _bet_semibluff_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} combines fold equity with "
            f"draw equity — betting is stronger than checking.")

def _bet_semibluff_obs2_l2(ctx, feat_dict, rb):
    return (f"If {ctx.opponent_phrase} folds, you win immediately. "
            f"If called, you still have outs to improve.")


def _bet_semibluff_obs1_l3(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    return (f"Semi-bluff: {outs} outs (~{draw_equity_pct:.0f}% on next card). "
            f"Fold equity plus improvement makes this profitable.")

def _bet_semibluff_obs2_l3(ctx, feat_dict, rb):
    danger = ctx.danger_score
    if danger > 0.50:
        return (f"The board is coordinated (danger {danger*100:.0f}%) — "
                f"your draw has credibility as a bluff on this texture.")
    return (f"Board danger is {danger*100:.0f}% — your bet represents "
            f"a wide range that includes strong made hands.")


def _bet_semibluff_obs1_l4(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    return (f"Semi-bluff with {outs} outs ({draw_equity_pct:.0f}% draw equity, "
            f"{equity*100:.0f}% total equity). "
            f"Combined fold equity and draw equity make betting +EV "
            f"compared to checking.")

def _bet_semibluff_obs2_l4(ctx, feat_dict, rb):
    villain_air_pct = ctx.villain_air_pct * 100
    return (f"{ctx.opponent_phrase.capitalize()}'s range includes "
            f"~{villain_air_pct:.0f}% air — fold equity is real. "
            f"When called, your draw provides backup equity.")


def _bet_semibluff_obs1_l5(ctx, feat_dict, rb):
    outs = int(ctx.draw_outs)
    draw_equity_pct = ctx.draw_equity * 100 if ctx.draw_equity > 0 else outs * 2.2
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    return (f"Range construction: {ctx.hand_description} with {outs} outs "
            f"({draw_equity_pct:.0f}% draw equity, {equity*100:.0f}% total). "
            f"This hand is an ideal semi-bluff candidate — it balances "
            f"the value hands in your betting range.")

def _bet_semibluff_obs2_l5(ctx, feat_dict, rb):
    return (f"Betting with draws maintains an aggressive, balanced range. "
            f"Checking here would leave your betting range too "
            f"value-heavy and predictable.")


# =====================================================================
# SPOT 6: CHECK + showdown_value (medium hand checking)
# =====================================================================

def _check_showdown_obs1_l1(ctx, feat_dict, rb):
    return "You have a decent hand."

def _check_showdown_obs2_l1(ctx, feat_dict, rb):
    return "Checking keeps the pot small with a hand that can win at showdown."


def _check_showdown_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} has some showdown value — "
            f"checking avoids bloating the pot.")

def _check_showdown_obs2_l2(ctx, feat_dict, rb):
    if ctx.is_ip:
        return ("You are in position — you can control the pot size "
                "and see a free card if needed.")
    return ("Out of position, checking avoids building a pot "
            "where you may face difficult decisions.")


def _check_showdown_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range — "
            f"enough to win at showdown but not enough to bet for value.")

def _check_showdown_obs2_l3(ctx, feat_dict, rb):
    return _board_texture_l3(ctx)


def _check_showdown_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    better_pct = ctx.better_hand_pct * 100
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"Range position: {worse_pct:.0f}% worse, {better_pct:.0f}% better. "
            f"Betting would fold out worse hands and get called by better.")

def _check_showdown_obs2_l4(ctx, feat_dict, rb):
    danger = ctx.danger_score
    return (f"Board danger {danger*100:.0f}% — checking preserves "
            f"showdown equity without inflating the pot.")


def _check_showdown_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity. "
            f"This hand sits in the middle of your range — "
            f"too strong to bluff, too weak to value bet.")

def _check_showdown_obs2_l5(ctx, feat_dict, rb):
    return (f"Showdown value hand. In range construction, these hands "
            f"anchor your checking range, providing protection against "
            f"opponents who probe aggressively.")


# =====================================================================
# CATALOG REGISTRATION
# =====================================================================

SPOT_CATALOG: dict = {}

# -- Spot 1: CHECK + pot_control --
SPOT_CATALOG[('CHECK', 'pot_control', 'L1')] = SpotNarrative(
    observations=[_check_potcontrol_obs1_l1, _check_potcontrol_obs2_l1])
SPOT_CATALOG[('CHECK', 'pot_control', 'L2')] = SpotNarrative(
    observations=[_check_potcontrol_obs1_l2, _check_potcontrol_obs2_l2])
SPOT_CATALOG[('CHECK', 'pot_control', 'L3')] = SpotNarrative(
    observations=[_check_potcontrol_obs1_l3, _check_potcontrol_obs2_l3])
SPOT_CATALOG[('CHECK', 'pot_control', 'L4')] = SpotNarrative(
    observations=[_check_potcontrol_obs1_l4, _check_potcontrol_obs2_l4])
SPOT_CATALOG[('CHECK', 'pot_control', 'L5')] = SpotNarrative(
    observations=[_check_potcontrol_obs1_l5, _check_potcontrol_obs2_l5])

# -- Spot 2: BET + value_bet --
SPOT_CATALOG[('BET', 'value_bet', 'L1')] = SpotNarrative(
    observations=[_bet_value_obs1_l1, _bet_value_obs2_l1])
SPOT_CATALOG[('BET', 'value_bet', 'L2')] = SpotNarrative(
    observations=[_bet_value_obs1_l2, _bet_value_obs2_l2])
SPOT_CATALOG[('BET', 'value_bet', 'L3')] = SpotNarrative(
    observations=[_bet_value_obs1_l3, _bet_value_obs2_l3])
SPOT_CATALOG[('BET', 'value_bet', 'L4')] = SpotNarrative(
    observations=[_bet_value_obs1_l4, _bet_value_obs2_l4])
SPOT_CATALOG[('BET', 'value_bet', 'L5')] = SpotNarrative(
    observations=[_bet_value_obs1_l5, _bet_value_obs2_l5])

# -- Spot 3: FOLD + equity_denial --
SPOT_CATALOG[('FOLD', 'equity_denial', 'L1')] = SpotNarrative(
    observations=[_fold_equity_obs1_l1, _fold_equity_obs2_l1])
SPOT_CATALOG[('FOLD', 'equity_denial', 'L2')] = SpotNarrative(
    observations=[_fold_equity_obs1_l2, _fold_equity_obs2_l2])
SPOT_CATALOG[('FOLD', 'equity_denial', 'L3')] = SpotNarrative(
    observations=[_fold_equity_obs1_l3, _fold_equity_obs2_l3])
SPOT_CATALOG[('FOLD', 'equity_denial', 'L4')] = SpotNarrative(
    observations=[_fold_equity_obs1_l4, _fold_equity_obs2_l4])
SPOT_CATALOG[('FOLD', 'equity_denial', 'L5')] = SpotNarrative(
    observations=[_fold_equity_obs1_l5, _fold_equity_obs2_l5])

# -- Spot 4: CALL + drawing_call --
SPOT_CATALOG[('CALL', 'drawing_call', 'L1')] = SpotNarrative(
    observations=[_call_draw_obs1_l1, _call_draw_obs2_l1])
SPOT_CATALOG[('CALL', 'drawing_call', 'L2')] = SpotNarrative(
    observations=[_call_draw_obs1_l2, _call_draw_obs2_l2])
SPOT_CATALOG[('CALL', 'drawing_call', 'L3')] = SpotNarrative(
    observations=[_call_draw_obs1_l3, _call_draw_obs2_l3])
SPOT_CATALOG[('CALL', 'drawing_call', 'L4')] = SpotNarrative(
    observations=[_call_draw_obs1_l4, _call_draw_obs2_l4])
SPOT_CATALOG[('CALL', 'drawing_call', 'L5')] = SpotNarrative(
    observations=[_call_draw_obs1_l5, _call_draw_obs2_l5])

# -- Spot 5: BET + semi_bluff --
SPOT_CATALOG[('BET', 'semi_bluff', 'L1')] = SpotNarrative(
    observations=[_bet_semibluff_obs1_l1, _bet_semibluff_obs2_l1])
SPOT_CATALOG[('BET', 'semi_bluff', 'L2')] = SpotNarrative(
    observations=[_bet_semibluff_obs1_l2, _bet_semibluff_obs2_l2])
SPOT_CATALOG[('BET', 'semi_bluff', 'L3')] = SpotNarrative(
    observations=[_bet_semibluff_obs1_l3, _bet_semibluff_obs2_l3])
SPOT_CATALOG[('BET', 'semi_bluff', 'L4')] = SpotNarrative(
    observations=[_bet_semibluff_obs1_l4, _bet_semibluff_obs2_l4])
SPOT_CATALOG[('BET', 'semi_bluff', 'L5')] = SpotNarrative(
    observations=[_bet_semibluff_obs1_l5, _bet_semibluff_obs2_l5])

# -- Spot 6: CHECK + showdown_value --
SPOT_CATALOG[('CHECK', 'showdown_value', 'L1')] = SpotNarrative(
    observations=[_check_showdown_obs1_l1, _check_showdown_obs2_l1])
SPOT_CATALOG[('CHECK', 'showdown_value', 'L2')] = SpotNarrative(
    observations=[_check_showdown_obs1_l2, _check_showdown_obs2_l2])
SPOT_CATALOG[('CHECK', 'showdown_value', 'L3')] = SpotNarrative(
    observations=[_check_showdown_obs1_l3, _check_showdown_obs2_l3])
SPOT_CATALOG[('CHECK', 'showdown_value', 'L4')] = SpotNarrative(
    observations=[_check_showdown_obs1_l4, _check_showdown_obs2_l4])
SPOT_CATALOG[('CHECK', 'showdown_value', 'L5')] = SpotNarrative(
    observations=[_check_showdown_obs1_l5, _check_showdown_obs2_l5])


# ═══════════════════════════════════════════════════════════════════
# SPOT 7: CHECK + trap (monster hand checking — equity > 0.80)
# ═══════════════════════════════════════════════════════════════════

def _check_trap_obs1_l1(ctx, feat_dict, rb):
    return "You have a very strong hand. There is no rush to build the pot."

def _check_trap_obs2_l1(ctx, feat_dict, rb):
    return "Checking keeps your opponent in the hand."

def _check_trap_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} is very strong — "
            f"checking here keeps {ctx.opponent_phrase} in the hand "
            f"and lets them put more money in on later streets.")

def _check_trap_obs2_l2(ctx, feat_dict, rb):
    danger = ctx.danger_score
    if danger < 0.30:
        return "The board is safe — your hand is not in danger of being outdrawn."
    return "The board has some draws — but your hand is strong enough to let them develop."

def _check_trap_obs1_l3(ctx, feat_dict, rb):
    eq = ctx.equity_vs_range * 100
    worse = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {eq:.0f}% equity. "
            f"You beat {worse:.0f}% of {ctx.opponent_phrase}'s range — "
            f"checking lets weaker hands catch up or bluff.")

def _check_trap_obs2_l3(ctx, feat_dict, rb):
    return "GTO checks its strongest hands at a frequency to protect the checking range."

def _check_trap_obs1_l4(ctx, feat_dict, rb):
    if rb:
        threats = [b for b in rb.buckets if b.beats_hero > 0 and b.pct_of_range > 0.01][:2]
        threat_str = ""
        if threats:
            parts = [f"{t.subcategory.replace('_',' ')} ({t.pct_of_range*100:.1f}%)" for t in threats]
            threat_str = f" Threats: {', '.join(parts)}."
        return (f"{rb.hero_label}. {ctx.equity_vs_range*100:.0f}% equity. "
                f"Very few hands beat you.{threat_str}")
    return (f"{ctx.hand_description_cap}: {ctx.equity_vs_range*100:.0f}% equity. "
            f"Premium hand — checking controls the action.")

def _check_trap_obs2_l4(ctx, feat_dict, rb):
    if rb and rb.value_target_pct > 0:
        return (f"Betting targets only {rb.value_target_pct*100:.0f}% of villain's range "
                f"that is worse and would call — thin target for a monster hand.")
    return "Checking at a frequency with strong hands keeps your overall range balanced."

def _check_trap_obs1_l5(ctx, feat_dict, rb):
    if rb:
        better = rb.better_pct * 100
        worse = rb.worse_pct * 100
        return (f"{rb.hero_label}. Villain: {better:.0f}% beats you, "
                f"you beat {worse:.0f}%. Near-nuts.")
    return f"{ctx.hand_description_cap}. Near-nuts. GTO mixes check/bet at this equity level."

def _check_trap_obs2_l5(ctx, feat_dict, rb):
    return ("Pot control node. GTO checks strong hands at a frequency "
            "to prevent checking range from becoming exploitably weak.")

for lvl, o1, o2 in [
    ('L1', _check_trap_obs1_l1, _check_trap_obs2_l1),
    ('L2', _check_trap_obs1_l2, _check_trap_obs2_l2),
    ('L3', _check_trap_obs1_l3, _check_trap_obs2_l3),
    ('L4', _check_trap_obs1_l4, _check_trap_obs2_l4),
    ('L5', _check_trap_obs1_l5, _check_trap_obs2_l5),
]:
    SPOT_CATALOG[('CHECK', 'trap', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# PREFLOP NARRATIVES
# ═══════════════════════════════════════════════════════════════════

# -- FOLD + preflop_open --
def _fold_preflop_open_l1(ctx, feat_dict, rb):
    return "This hand is not strong enough to open from this position."

def _fold_preflop_open_l2(ctx, feat_dict, rb):
    return (f"From {ctx.position}, your opening range is tight "
            f"— this hand doesn't qualify.")

SPOT_CATALOG[('FOLD', 'preflop_open', 'L1')] = SpotNarrative(
    observations=[_fold_preflop_open_l1])
SPOT_CATALOG[('FOLD', 'preflop_open', 'L2')] = SpotNarrative(
    observations=[_fold_preflop_open_l2])


# -- FOLD + preflop_defend --
def _fold_preflop_defend_l1(ctx, feat_dict, rb):
    return "This hand is not strong enough to defend against this raise."

def _fold_preflop_defend_l2(ctx, feat_dict, rb):
    villain_pos = feat_dict.get('_villain_position', 'opponent')
    return (f"Facing a raise from {villain_pos}, your defending range is "
            f"tighter than your opening range — this hand should fold.")

SPOT_CATALOG[('FOLD', 'preflop_defend', 'L1')] = SpotNarrative(
    observations=[_fold_preflop_defend_l1])
SPOT_CATALOG[('FOLD', 'preflop_defend', 'L2')] = SpotNarrative(
    observations=[_fold_preflop_defend_l2])


# -- CALL + preflop_defend --
def _call_preflop_defend_l1(ctx, feat_dict, rb):
    return "This hand is in your defending range — calling is correct."

def _call_preflop_defend_l2(ctx, feat_dict, rb):
    return (f"Your hand is strong enough to call {ctx.opponent_phrase}'s "
            f"raise from {ctx.position} — you are in the defending range "
            f"for this matchup.")

SPOT_CATALOG[('CALL', 'preflop_defend', 'L1')] = SpotNarrative(
    observations=[_call_preflop_defend_l1])
SPOT_CATALOG[('CALL', 'preflop_defend', 'L2')] = SpotNarrative(
    observations=[_call_preflop_defend_l2])


# -- RAISE + preflop_open --
def _raise_preflop_open_l1(ctx, feat_dict, rb):
    return "This is a standard opening hand from this position."

def _raise_preflop_open_l2(ctx, feat_dict, rb):
    return (f"From {ctx.position}, this hand is in your opening range "
            f"— raising is the standard play.")

SPOT_CATALOG[('RAISE', 'preflop_open', 'L1')] = SpotNarrative(
    observations=[_raise_preflop_open_l1])
SPOT_CATALOG[('RAISE', 'preflop_open', 'L2')] = SpotNarrative(
    observations=[_raise_preflop_open_l2])


# -- RAISE + preflop_3bet --
def _raise_preflop_3bet_l1(ctx, feat_dict, rb):
    return "This hand is strong enough to re-raise here."

def _raise_preflop_3bet_l2(ctx, feat_dict, rb):
    return (f"Against {ctx.opponent_phrase}'s open, your hand is in the "
            f"3-bet range — re-raising builds the pot with a strong holding.")

SPOT_CATALOG[('RAISE', 'preflop_3bet', 'L1')] = SpotNarrative(
    observations=[_raise_preflop_3bet_l1])
SPOT_CATALOG[('RAISE', 'preflop_3bet', 'L2')] = SpotNarrative(
    observations=[_raise_preflop_3bet_l2])


# -- CALL + preflop_open (limping/overlimping — rare) --
def _call_preflop_open_l1(ctx, feat_dict, rb):
    return "Calling is fine at this price."

def _call_preflop_open_l2(ctx, feat_dict, rb):
    return "The price is right to see a flop with this hand."

SPOT_CATALOG[('CALL', 'preflop_open', 'L1')] = SpotNarrative(
    observations=[_call_preflop_open_l1])
SPOT_CATALOG[('CALL', 'preflop_open', 'L2')] = SpotNarrative(
    observations=[_call_preflop_open_l2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 8: FOLD + range_fold (decent hand folding to aggression)
# ═══════════════════════════════════════════════════════════════════

def _fold_rangefold_obs1_l1(ctx, feat_dict, rb):
    return "Your hand looks decent but is not strong enough to continue here."

def _fold_rangefold_obs2_l1(ctx, feat_dict, rb):
    return "Folding saves chips when facing strength."


def _fold_rangefold_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} is a reasonable hand, but when "
            f"{ctx.opponent_phrase} raises, their range is much stronger "
            f"than average — most of it has you beat.")

def _fold_rangefold_obs2_l2(ctx, feat_dict, rb):
    return (f"Against a wider range you could continue, but "
            f"{ctx.opponent_phrase}'s aggression signals real strength.")


def _fold_rangefold_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity "
            f"vs the raising range. You need {pot_odds_pct:.0f}% to call — "
            f"the equity gap makes continuing unprofitable.")

def _fold_rangefold_obs2_l3(ctx, feat_dict, rb):
    better_pct = ctx.better_hand_pct * 100
    return (f"{better_pct:.0f}% of {ctx.opponent_phrase}'s raising range "
            f"has you beat — your decent hand is not decent enough.")


def _fold_rangefold_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    better_pct = ctx.better_hand_pct * 100
    worse_pct = ctx.worse_hand_pct * 100
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"Range decomposition: {better_pct:.0f}% beats you, "
            f"{worse_pct:.0f}% is worse. Need {pot_odds_pct:.0f}% to call.")

def _fold_rangefold_obs2_l4(ctx, feat_dict, rb):
    threats = []
    if ctx.better_hand_pct > 0.30:
        threats.append(f"over-pairs and better kickers ({ctx.better_hand_pct*100:.0f}%)")
    if ctx.danger_score > 0.40:
        threats.append(f"board danger {ctx.danger_score*100:.0f}%")
    threat_str = "; ".join(threats) if threats else "raising range is value-heavy"
    return f"Threats: {threat_str}. Folding is correct despite hand strength."


def _fold_rangefold_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity "
            f"against {ctx.opponent_phrase}'s raising range. "
            f"Villain's raising range is heavily weighted toward value — "
            f"pot odds require {pot_odds_pct:.0f}% but you fall short.")

def _fold_rangefold_obs2_l5(ctx, feat_dict, rb):
    return (f"MDF analysis: even accounting for minimum defence frequency, "
            f"this hand falls below the threshold against a value-heavy "
            f"raising range. Folding preserves range integrity.")


for lvl, o1, o2 in [
    ('L1', _fold_rangefold_obs1_l1, _fold_rangefold_obs2_l1),
    ('L2', _fold_rangefold_obs1_l2, _fold_rangefold_obs2_l2),
    ('L3', _fold_rangefold_obs1_l3, _fold_rangefold_obs2_l3),
    ('L4', _fold_rangefold_obs1_l4, _fold_rangefold_obs2_l4),
    ('L5', _fold_rangefold_obs1_l5, _fold_rangefold_obs2_l5),
]:
    SPOT_CATALOG[('FOLD', 'range_fold', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 9: BET + thin_value (betting for thin value)
# ═══════════════════════════════════════════════════════════════════

def _bet_thinvalue_obs1_l1(ctx, feat_dict, rb):
    return "You have a decent hand — betting gets some value from weaker hands."

def _bet_thinvalue_obs2_l1(ctx, feat_dict, rb):
    return _board_texture_l1(ctx)


def _bet_thinvalue_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} is ahead, but not by much — "
            f"a small bet extracts value without overcommitting.")

def _bet_thinvalue_obs2_l2(ctx, feat_dict, rb):
    return (f"Against {ctx.opponent_phrase}, a thin value bet targets "
            f"the weaker portion of their range that may still call.")


def _bet_thinvalue_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range — "
            f"enough for a thin value bet, but sizing should stay small.")

def _bet_thinvalue_obs2_l3(ctx, feat_dict, rb):
    return _board_texture_l3(ctx)


def _bet_thinvalue_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of {ctx.opponent_phrase}'s range is worse. "
            f"Thin value target: {value_target*100:.0f}% of the calling "
            f"range is worse — just enough to justify a small bet.")

def _bet_thinvalue_obs2_l4(ctx, feat_dict, rb):
    better_pct = ctx.better_hand_pct * 100
    return (f"Risk: {better_pct:.0f}% of the range beats you. "
            f"A raise from {ctx.opponent_phrase} would be a clear fold — "
            f"bet small to control exposure.")


def _bet_thinvalue_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity. "
            f"Value target is thin — {value_target*100:.0f}% of the calling range "
            f"is worse. This hand sits at the bottom of the value betting range.")

def _bet_thinvalue_obs2_l5(ctx, feat_dict, rb):
    return (f"Thin value bet in range construction. These marginal value bets "
            f"increase EV by extracting from worse hands while keeping the "
            f"betting range appropriately wide.")


for lvl, o1, o2 in [
    ('L1', _bet_thinvalue_obs1_l1, _bet_thinvalue_obs2_l1),
    ('L2', _bet_thinvalue_obs1_l2, _bet_thinvalue_obs2_l2),
    ('L3', _bet_thinvalue_obs1_l3, _bet_thinvalue_obs2_l3),
    ('L4', _bet_thinvalue_obs1_l4, _bet_thinvalue_obs2_l4),
    ('L5', _bet_thinvalue_obs1_l5, _bet_thinvalue_obs2_l5),
]:
    SPOT_CATALOG[('BET', 'thin_value', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 10: BET + protection (betting to protect against draws)
# ═══════════════════════════════════════════════════════════════════

def _bet_protection_obs1_l1(ctx, feat_dict, rb):
    return "You have a made hand on a dangerous board — betting charges draws to continue."

def _bet_protection_obs2_l1(ctx, feat_dict, rb):
    return "Betting now prevents opponents from seeing free cards."


def _bet_protection_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} is ahead now, but the board is "
            f"dangerous — betting denies free cards to opponents with draws.")

def _bet_protection_obs2_l2(ctx, feat_dict, rb):
    return (f"If you check, {ctx.opponent_phrase} gets a free card that "
            f"could complete a draw and overtake you.")


def _bet_protection_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    danger = ctx.danger_score * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity on a "
            f"board with {danger:.0f}% danger. Betting denies equity to the "
            f"drawing portion of {ctx.opponent_phrase}'s range.")

def _bet_protection_obs2_l3(ctx, feat_dict, rb):
    return (f"Equity denial is key here — every free card risks giving "
            f"opponents the 4-8% they need to outdraw you.")


def _bet_protection_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    danger = ctx.danger_score * 100
    villain_draw_pct = ctx.villain_air_pct * 100
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"Board danger {danger:.0f}%. Approximately {villain_draw_pct:.0f}% "
            f"of {ctx.opponent_phrase}'s range includes draws or air that "
            f"benefit from free cards.")

def _bet_protection_obs2_l4(ctx, feat_dict, rb):
    return (f"Protection bet: charges draws the wrong price to continue. "
            f"Even when called, you maintain equity advantage "
            f"against the calling range.")


def _bet_protection_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    danger = ctx.danger_score * 100
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity "
            f"on a {danger:.0f}% danger board. Betting serves dual purpose — "
            f"value from worse made hands and equity denial against draws.")

def _bet_protection_obs2_l5(ctx, feat_dict, rb):
    return (f"Protection in range construction. On draw-heavy boards, "
            f"GTO bets more frequently with made hands to deny free equity "
            f"realisation. Checking here would allow too many draws to "
            f"realise their equity for free.")


for lvl, o1, o2 in [
    ('L1', _bet_protection_obs1_l1, _bet_protection_obs2_l1),
    ('L2', _bet_protection_obs1_l2, _bet_protection_obs2_l2),
    ('L3', _bet_protection_obs1_l3, _bet_protection_obs2_l3),
    ('L4', _bet_protection_obs1_l4, _bet_protection_obs2_l4),
    ('L5', _bet_protection_obs1_l5, _bet_protection_obs2_l5),
]:
    SPOT_CATALOG[('BET', 'protection', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 11: BET + pure_bluff (betting with air)
# ═══════════════════════════════════════════════════════════════════

def _bet_purebluff_obs1_l1(ctx, feat_dict, rb):
    return "Your hand is weak, but betting can still win the pot."

def _bet_purebluff_obs2_l1(ctx, feat_dict, rb):
    return "If your opponent folds, you take the pot without a showdown."


def _bet_purebluff_obs1_l2(ctx, feat_dict, rb):
    return (f"Your hand cannot win at showdown — betting gives fold equity "
            f"as your only path to winning.")

def _bet_purebluff_obs2_l2(ctx, feat_dict, rb):
    return (f"If {ctx.opponent_phrase} folds, you win immediately. "
            f"This is a bluff — no need for a strong hand.")


def _bet_purebluff_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    return (f"No showdown value — {equity*100:.0f}% equity. "
            f"GTO includes bluffs on this board to keep opponents honest "
            f"and prevent them from over-folding.")

def _bet_purebluff_obs2_l3(ctx, feat_dict, rb):
    danger = ctx.danger_score
    if danger > 0.50:
        return (f"Board danger is {danger*100:.0f}% — the coordinated texture "
                f"gives your bluff credibility.")
    return (f"Board danger is {danger*100:.0f}% — your bluff represents "
            f"a strong made hand on this board.")


def _bet_purebluff_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    villain_air_pct = ctx.villain_air_pct * 100
    return (f"Pure bluff: {equity*100:.0f}% equity — no showdown value. "
            f"{ctx.opponent_phrase.capitalize()}'s range includes "
            f"~{villain_air_pct:.0f}% weak hands that will fold to a bet.")

def _bet_purebluff_obs2_l4(ctx, feat_dict, rb):
    return (f"Bluff profitability: if {ctx.opponent_phrase} folds more than "
            f"half the time, this bluff is automatically profitable "
            f"regardless of your hand strength.")


def _bet_purebluff_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    return (f"Range construction: {ctx.hand_description} at {equity*100:.0f}% "
            f"equity — this hand is a pure bluff candidate. GTO needs bluffs "
            f"in the betting range to prevent opponents from profitably "
            f"calling with their entire range.")

def _bet_purebluff_obs2_l5(ctx, feat_dict, rb):
    return (f"Auto-profit threshold: bet / (pot + bet) determines the fold "
            f"frequency needed for break-even. This hand has zero showdown "
            f"value, making it an ideal bluff — nothing is lost by betting.")


for lvl, o1, o2 in [
    ('L1', _bet_purebluff_obs1_l1, _bet_purebluff_obs2_l1),
    ('L2', _bet_purebluff_obs1_l2, _bet_purebluff_obs2_l2),
    ('L3', _bet_purebluff_obs1_l3, _bet_purebluff_obs2_l3),
    ('L4', _bet_purebluff_obs1_l4, _bet_purebluff_obs2_l4),
    ('L5', _bet_purebluff_obs1_l5, _bet_purebluff_obs2_l5),
]:
    SPOT_CATALOG[('BET', 'pure_bluff', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 12: CALL + mandatory_defend (calling with a made hand)
# ═══════════════════════════════════════════════════════════════════

def _call_mandatory_obs1_l1(ctx, feat_dict, rb):
    return "You have a decent hand — the price is right to continue."

def _call_mandatory_obs2_l1(ctx, feat_dict, rb):
    return "Calling keeps you in the pot with a hand that can still win."


def _call_mandatory_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} may not be the best hand, but the "
            f"pot is offering enough to justify calling.")

def _call_mandatory_obs2_l2(ctx, feat_dict, rb):
    return (f"Folding here would give up too much equity — "
            f"{ctx.opponent_phrase} could be betting with a wide range.")


def _call_mandatory_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"Pot odds require {pot_odds_pct:.0f}% — your equity "
            f"{'exceeds' if equity*100 >= pot_odds_pct else 'meets'} "
            f"the threshold, making calling profitable.")

def _call_mandatory_obs2_l3(ctx, feat_dict, rb):
    worse_pct = ctx.worse_hand_pct * 100
    return (f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range — "
            f"folding would surrender too much equity.")


def _call_mandatory_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    better_pct = ctx.better_hand_pct * 100
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"Pot odds: {pot_odds_pct:.0f}%. Range position: {worse_pct:.0f}% "
            f"worse, {better_pct:.0f}% better. Equity exceeds the price.")

def _call_mandatory_obs2_l4(ctx, feat_dict, rb):
    return (f"Mandatory defence: folding this hand would make your "
            f"defending range too tight, allowing {ctx.opponent_phrase} "
            f"to exploit you with bluffs.")


def _call_mandatory_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    pot_odds_pct = 0.0
    if ctx.to_call_amount > 0:
        total = ctx.pot_size + 2 * ctx.to_call_amount
        pot_odds_pct = (ctx.to_call_amount / total) * 100 if total > 0 else 0
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity "
            f"against {ctx.opponent_phrase}'s betting range. "
            f"Pot odds {pot_odds_pct:.0f}% — this hand is a mandatory defend "
            f"to maintain correct defence frequency.")

def _call_mandatory_obs2_l5(ctx, feat_dict, rb):
    return (f"Defence frequency: folding here drops below MDF, "
            f"making your range exploitable. This hand anchors the "
            f"calling range with sufficient equity to profit long-term.")


for lvl, o1, o2 in [
    ('L1', _call_mandatory_obs1_l1, _call_mandatory_obs2_l1),
    ('L2', _call_mandatory_obs1_l2, _call_mandatory_obs2_l2),
    ('L3', _call_mandatory_obs1_l3, _call_mandatory_obs2_l3),
    ('L4', _call_mandatory_obs1_l4, _call_mandatory_obs2_l4),
    ('L5', _call_mandatory_obs1_l5, _call_mandatory_obs2_l5),
]:
    SPOT_CATALOG[('CALL', 'mandatory_defend', lvl)] = SpotNarrative(observations=[o1, o2])


# ═══════════════════════════════════════════════════════════════════
# SPOT 13: RAISE + value_bet (raising for value with a strong hand)
# ═══════════════════════════════════════════════════════════════════

def _raise_value_obs1_l1(ctx, feat_dict, rb):
    return "You have a strong hand — raising builds a bigger pot."

def _raise_value_obs2_l1(ctx, feat_dict, rb):
    return "Your opponent has shown interest — make them pay more."


def _raise_value_obs1_l2(ctx, feat_dict, rb):
    return (f"Your {ctx.hand_description} is well ahead — raising extracts "
            f"maximum value from {ctx.opponent_phrase}.")

def _raise_value_obs2_l2(ctx, feat_dict, rb):
    return (f"{ctx.opponent_phrase.capitalize()} has already put money in — "
            f"raising builds the pot while you have the advantage.")


def _raise_value_obs1_l3(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    return (f"{ctx.hand_description_cap} with {equity*100:.0f}% equity. "
            f"You beat {worse_pct:.0f}% of {ctx.opponent_phrase}'s range — "
            f"raising for value is clearly profitable.")

def _raise_value_obs2_l3(ctx, feat_dict, rb):
    return _board_texture_l3(ctx)


def _raise_value_obs1_l4(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"{ctx.hand_description_cap} — {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of {ctx.opponent_phrase}'s range is worse. "
            f"Value target: {value_target*100:.0f}% of the calling range "
            f"pays off a raise.")

def _raise_value_obs2_l4(ctx, feat_dict, rb):
    danger = ctx.danger_score
    if danger > 0.50:
        return (f"Board danger {danger*100:.0f}% — raising also denies equity "
                f"to draws and builds the pot before scare cards arrive.")
    return (f"Board danger {danger*100:.0f}% — a stable board means "
            f"your raise is purely for value extraction.")


def _raise_value_obs1_l5(ctx, feat_dict, rb):
    equity = ctx.equity_vs_range if ctx.equity_vs_range > 0 else ctx.raw_equity
    worse_pct = ctx.worse_hand_pct * 100
    value_target = 0.0
    if rb is not None:
        value_target = getattr(rb, 'value_target_pct', 0.0)
    return (f"Range analysis: {ctx.hand_description} at {equity*100:.0f}% equity. "
            f"{worse_pct:.0f}% of the overall range is worse; "
            f"{value_target*100:.0f}% of the calling range pays off. "
            f"Clear value raise in your range construction.")

def _raise_value_obs2_l5(ctx, feat_dict, rb):
    return (f"This hand anchors the value portion of your raising range. "
            f"Balance requires mixing in bluff-raises at the appropriate "
            f"frequency to prevent {ctx.opponent_phrase} from over-folding.")


for lvl, o1, o2 in [
    ('L1', _raise_value_obs1_l1, _raise_value_obs2_l1),
    ('L2', _raise_value_obs1_l2, _raise_value_obs2_l2),
    ('L3', _raise_value_obs1_l3, _raise_value_obs2_l3),
    ('L4', _raise_value_obs1_l4, _raise_value_obs2_l4),
    ('L5', _raise_value_obs1_l5, _raise_value_obs2_l5),
]:
    SPOT_CATALOG[('RAISE', 'value_bet', lvl)] = SpotNarrative(observations=[o1, o2])
