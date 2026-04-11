"""
Deterministic Labelling Script — River Rats v2
Applies RAISE, BET, and FOLD decision trees to all 563 factory situations.

Decision flow:
    if to_call == 0:
        run BET tree → BET or CHECK
    else:  # facing bet
        run RAISE tree → if RAISE fires, output RAISE
        else: run FOLD tree → FOLD or CALL

Sources:
    RAISE_DECISION_TREE_V2.md
    BET_DECISION_TREE_V1.md
    FOLD_DECISION_TREE_V1.md
    feature_keys.py (class F)
"""

import json
import os
from collections import Counter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def g(feat: dict, key: str, default=0):
    """Safe feature getter — returns default if key missing or None."""
    val = feat.get(key)
    if val is None:
        return default
    return val


def situation_id(record: dict, idx: int) -> str:
    """Return a stable situation ID from the record, falling back to index."""
    sid = record.get('_situation_id') or record.get('situation_id')
    if sid:
        return str(sid)
    return f"situation_{idx:04d}"


# ---------------------------------------------------------------------------
# RAISE tree  (RAISE_DECISION_TREE_V2.md)
# ---------------------------------------------------------------------------

def apply_raise_tree(feat: dict) -> dict:
    """
    Implements RAISE_DECISION_TREE_V2.md exactly.

    Returns dict:
        action      : 'RAISE' or None
        step_fired  : description string
        confidence  : 'HIGH' / 'MEDIUM' / 'LOW' / None
    """

    # ------------------------------------------------------------------
    # Step 1 — Flat Spot Check (force NOT-RAISE / pass to FOLD tree)
    # ------------------------------------------------------------------

    # Step 1A: Bet-and-call, non-monster = always CALL
    if g(feat, 'num_callers_to_bet') >= 1 and g(feat, 'is_monster') == 0:
        return {'action': None, 'step_fired': 'Step 1A flat spot (bet-and-call non-monster)', 'confidence': None}

    # Step 1B: Board heavily favours villain's uncapped range = CALL
    if g(feat, 'board_favour') <= -0.30 and g(feat, 'villain_range_capped') == 0:
        return {'action': None, 'step_fired': 'Step 1B flat spot (board favours villain uncapped)', 'confidence': None}

    # Step 1C: Multi-street aggressor, non-monster = CALL
    if g(feat, 'villain_aggression_count') >= 2 and g(feat, 'is_monster') == 0:
        return {'action': None, 'step_fired': 'Step 1C flat spot (multi-street aggressor non-monster)', 'confidence': None}

    # ------------------------------------------------------------------
    # Step 2 — Monster Value Raise
    # Condition: is_monster == 1
    # Suppressors S1-S5: any fires → CALL instead of RAISE
    # ------------------------------------------------------------------

    if g(feat, 'is_monster') == 1:
        # S1: flush-completing board threatens non-two-pair monsters
        # hand_category < 10 means below two_pair
        if g(feat, 'flush_danger') >= 0.60 and g(feat, 'hand_category') < 10:
            return {'action': None, 'step_fired': 'Step 2 suppressor S1 (flush danger + below two-pair)', 'confidence': None}

        # S2: flush on paired board = full-house danger
        if g(feat, 'flush_danger') >= 0.60 and g(feat, 'is_paired') == 1:
            return {'action': None, 'step_fired': 'Step 2 suppressor S2 (flush danger + paired board)', 'confidence': None}

        # S3: multi-street aggressor threatens monster
        if g(feat, 'villain_aggression_count') >= 2:
            return {'action': None, 'step_fired': 'Step 2 suppressor S3 (multi-street aggressor vs monster)', 'confidence': None}

        # S4: High SPR IP = pot control preferred (raised to 6.0 in v2)
        if g(feat, 'spr') >= 6.0 and g(feat, 'is_ip') == 1:
            return {'action': None, 'step_fired': 'Step 2 suppressor S4 (high SPR IP monster)', 'confidence': None}

        # S5: Bet-and-call, monster below top 8% of range
        if g(feat, 'num_callers_to_bet') >= 1 and g(feat, 'hero_range_percentile') < 0.92:
            return {'action': None, 'step_fired': 'Step 2 suppressor S5 (bet-and-call monster below 92nd pct)', 'confidence': None}

        # No suppressor fired → RAISE (Value)
        return {'action': 'RAISE', 'step_fired': 'Step 2 monster value raise', 'confidence': 'HIGH'}

    # ------------------------------------------------------------------
    # Step 3 — Low SPR Commit
    # Condition: spr <= 1.5 AND hero_range_percentile >= 0.90
    # (percentile raised from 0.80 to 0.90 in v2)
    # ------------------------------------------------------------------

    if g(feat, 'spr') <= 1.5 and g(feat, 'hero_range_percentile') >= 0.90:
        return {'action': 'RAISE', 'step_fired': 'Step 3 low SPR commit', 'confidence': 'HIGH'}

    # ------------------------------------------------------------------
    # Step 4 — Thin Value OOP Check-Raise
    # ALL 8 conditions required (fold_equity raised to 0.40 in v2)
    # ------------------------------------------------------------------

    if (
        g(feat, 'hero_range_percentile') >= 0.75
        and g(feat, 'is_monster') == 0
        and g(feat, 'is_ip') == 0                        # OOP only
        and g(feat, 'villain_fold_equity_estimate') >= 0.40
        and g(feat, 'villain_aggression_count') <= 1
        and g(feat, 'flush_danger') <= 0.35
        and g(feat, 'straight_danger') <= 0.35
        and g(feat, 'num_callers_to_bet') == 0
    ):
        return {'action': 'RAISE', 'step_fired': 'Step 4 thin value OOP check-raise', 'confidence': 'MEDIUM'}

    # ------------------------------------------------------------------
    # Step 5 — Semi-Bluff Raise
    # ALL 6 conditions required, including flush_draw_rank AND flush_block_pct (AND, not OR)
    # ------------------------------------------------------------------

    if (
        g(feat, 'draw_outs') >= 9
        and g(feat, 'flush_draw_rank') >= 12            # nut or near-nut draw (Q/K/A)
        and g(feat, 'flush_block_pct') > 0              # holds at least one blocker
        and g(feat, 'villain_fold_equity_estimate') >= 0.45
        and g(feat, 'villain_aggression_count') <= 1
        and g(feat, 'is_paired') == 0
    ):
        return {'action': 'RAISE', 'step_fired': 'Step 5 semi-bluff raise', 'confidence': 'MEDIUM'}

    # ------------------------------------------------------------------
    # Step 6 — Bluff Raise (river only, street >= 2)
    # ALL 6 conditions required (street gate added in v2)
    # ------------------------------------------------------------------

    if (
        g(feat, 'street') >= 2                          # river only (0=flop, 1=turn, 2=river)
        and g(feat, 'hero_range_percentile') <= 0.20
        and g(feat, 'villain_fold_equity_estimate') >= 0.50
        and g(feat, 'villain_top_pair_plus_pct') <= 0.35
        and g(feat, 'num_callers_to_bet') == 0
        and g(feat, 'villain_aggression_count') == 0
    ):
        return {'action': 'RAISE', 'step_fired': 'Step 6 bluff raise (river)', 'confidence': 'LOW'}

    # ------------------------------------------------------------------
    # Default — no RAISE step fired, pass to FOLD tree
    # ------------------------------------------------------------------
    return {'action': None, 'step_fired': 'RAISE default (no step fired)', 'confidence': None}


# ---------------------------------------------------------------------------
# BET tree  (BET_DECISION_TREE_V1.md)
# ---------------------------------------------------------------------------

def apply_bet_tree(feat: dict) -> dict:
    """
    Implements BET_DECISION_TREE_V1.md exactly.
    Only called when to_call == 0.

    Returns dict:
        action      : 'BET' or 'CHECK'
        step_fired  : description string
        confidence  : 'HIGH' / 'MEDIUM' / 'MEDIUM-LOW' / None
    """

    def _check(step_name):
        return {'action': 'CHECK', 'step_fired': step_name, 'confidence': None}

    def _bet(step_name, confidence='HIGH'):
        return {'action': 'BET', 'step_fired': step_name, 'confidence': confidence}

    # ------------------------------------------------------------------
    # Step 1 — Global Suppressors
    # S1 and S3 apply to ALL subsequent steps.
    # S2 applies to Steps 3A, 4, and 5 (Steps 2, 3B, 6 override it).
    # ------------------------------------------------------------------

    # S1: Wet board bluff suppressor
    # (flush_danger >= 0.60 OR straight_danger >= 0.50) AND is_made_hand == 0 AND draw_outs < 12
    s1_fires = (
        (g(feat, 'flush_danger') >= 0.60 or g(feat, 'straight_danger') >= 0.50)
        and g(feat, 'is_made_hand') == 0
        and g(feat, 'draw_outs') < 12
    )

    # S2: OOP suppressor (non-monster, non-exception)
    # is_ip == 0 AND is_monster == 0 AND hero_range_percentile < 0.72 AND raw_equity < 0.60
    s2_fires = (
        g(feat, 'is_ip') == 0
        and g(feat, 'is_monster') == 0
        and g(feat, 'hero_range_percentile') < 0.72
        and g(feat, 'raw_equity') < 0.60
    )

    # S3: Multi-street villain aggressor suppressor
    # villain_aggression_count >= 2 AND hero_range_percentile < 0.85
    s3_fires = (
        g(feat, 'villain_aggression_count') >= 2
        and g(feat, 'hero_range_percentile') < 0.85
    )

    if s1_fires:
        return _check('S1 wet board bluff suppressor')

    if s3_fires:
        return _check('S3 multi-street aggressor suppressor')

    # ------------------------------------------------------------------
    # Step 2 — Monster Protection Bet (Dynamic Board)
    # OOP override: this step explicitly allows OOP bets (overrides S2).
    # ALL required:
    #   is_monster == 1
    #   danger_score >= 0.45 OR flush_danger >= 0.45 OR straight_danger >= 0.40
    #   is_preflop_aggressor == 1 OR raw_equity >= 0.70
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_monster') == 1
        and (
            g(feat, 'danger_score') >= 0.45
            or g(feat, 'flush_danger') >= 0.45
            or g(feat, 'straight_danger') >= 0.40
        )
        and (
            g(feat, 'is_preflop_aggressor') == 1
            or g(feat, 'raw_equity') >= 0.70
        )
    ):
        return _bet('Step 2 monster protection bet', 'HIGH')

    # ------------------------------------------------------------------
    # Step 3A — IP PFA Value C-Bet
    # ALL required:
    #   is_preflop_aggressor == 1
    #   is_made_hand == 1
    #   high_card_rank >= 12  (recalibrated from board_favour >= 0.20; Q+ = PFA range advantage)
    #   is_ip == 1
    #   hand_category >= 7
    #   Texture gate passes (Tier 1/2/3; Tier 4 skips)
    # S2 applies to this step.
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_preflop_aggressor') == 1
        and g(feat, 'is_made_hand') == 1
        and g(feat, 'high_card_rank') >= 12             # Q+ board favors PFA's range
        and g(feat, 'is_ip') == 1
        and g(feat, 'hand_category') >= 7               # TPGK minimum initial gate
        and not s2_fires                                 # S2 does not apply (is_ip==1 so s2_fires==False anyway)
    ):
        # Determine board texture tier (evaluate in order, first match applies)
        hcr = g(feat, 'high_card_rank')
        fd = g(feat, 'flush_danger')
        cs = g(feat, 'connectivity_score')
        hcat = g(feat, 'hand_category')

        # Gate 3A-2: flush danger acceptable only with nut flush draw
        gate_3a2 = (fd <= 0.50) or (fd > 0.50 and g(feat, 'flush_draw_rank') >= 12)

        if not gate_3a2:
            pass  # tier check below will still be evaluated; gate_3a2 failure blocks BET
        else:
            # Tier 1: K or A high, flush_danger <= 0.20, connectivity_score <= 3
            if hcr >= 13 and fd <= 0.20 and cs <= 3:
                # Gate 3A-1 for Tier 1: connectivity_score <= 6 OR high_card_rank >= 12
                gate_3a1 = cs <= 6 or hcr >= 12
                # Gate 3A-3 Tier 1: hand_category >= 6
                if gate_3a1 and hcat >= 6:
                    return _bet('Step 3A Tier 1 IP PFA value c-bet', 'HIGH')

            # Tier 2: J+ high, flush_danger <= 0.35, connectivity_score <= 5
            elif hcr >= 11 and fd <= 0.35 and cs <= 5:
                gate_3a1 = cs <= 6 or hcr >= 12
                # Gate 3A-3 Tier 2: hand_category >= 7
                if gate_3a1 and hcat >= 7:
                    return _bet('Step 3A Tier 2 IP PFA value c-bet', 'MEDIUM')

            # Tier 3: flush_danger <= 0.50, connectivity_score <= 7
            elif fd <= 0.50 and cs <= 7:
                gate_3a1 = cs <= 6 or hcr >= 12
                # Gate 3A-3 Tier 3: hand_category >= 10 (two_pair+)
                if gate_3a1 and hcat >= 10:
                    return _bet('Step 3A Tier 3 IP PFA value c-bet', 'MEDIUM-LOW')

            # Tier 4: everything else → skip Step 3A (go to later steps)
            # Step 3A does NOT fire on Tier 4

    # ------------------------------------------------------------------
    # Step 3B — OOP PFA Value Bet (Exception — overrides S2)
    # ALL required:
    #   is_preflop_aggressor == 1
    #   is_made_hand == 1
    #   high_card_rank >= 12  (outer Step 3 gate: recalibrated from board_favour >= 0.20)
    #   is_ip == 0
    #   hand_category >= 7
    #   high_card_rank >= 13  (stricter OOP gate: K or A high; recalibrated from board_favour >= 0.35)
    #   villain_air_pct >= 0.40
    #   is_rainbow == 1 OR flush_danger <= 0.20
    #   villain_aggression_count == 0
    #   hero_range_percentile >= 0.72
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_preflop_aggressor') == 1
        and g(feat, 'is_made_hand') == 1
        and g(feat, 'high_card_rank') >= 12             # outer Step 3 gate: Q+ board
        and g(feat, 'is_ip') == 0
        and g(feat, 'hand_category') >= 7
        and g(feat, 'high_card_rank') >= 13             # stricter OOP requirement: K or A high only
        and g(feat, 'villain_air_pct') >= 0.40
        and (g(feat, 'is_rainbow') == 1 or g(feat, 'flush_danger') <= 0.20)
        and g(feat, 'villain_aggression_count') == 0
        and g(feat, 'hero_range_percentile') >= 0.72
    ):
        return _bet('Step 3B OOP PFA value exception', 'MEDIUM')

    # ------------------------------------------------------------------
    # Step 4 — PFA Bluff C-Bet (Semi-Bluff with Equity)
    # Outer gate — ALL required:
    #   is_preflop_aggressor == 1
    #   is_made_hand == 0
    #   high_card_rank >= 12  (recalibrated from board_favour >= 0.20; Q+ = range credibility)
    # S1 and S3 already checked above.
    # S2 applies to this step (OOP: only sub-4A applies).
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_preflop_aggressor') == 1
        and g(feat, 'is_made_hand') == 0
        and g(feat, 'high_card_rank') >= 12             # Q+ board: range credibility for PFA semi-bluff
    ):
        is_ip = g(feat, 'is_ip') == 1
        fd = g(feat, 'flush_danger')
        draw_outs = g(feat, 'draw_outs')
        fdr = g(feat, 'flush_draw_rank')
        fbp = g(feat, 'flush_block_pct')

        # Sub-condition 4A: Combo draw (12+ outs) — fires for both IP and OOP
        if draw_outs >= 12:
            # Position gate: 4A applies to both IP and OOP
            # S2 check for OOP: 4A is the only OOP-viable sub-condition,
            # but the tree says "OOP: sub-condition 4A only" as a grant,
            # meaning it fires even if S2 would otherwise block.
            # Re-checking S2 here: the tree's position gate overrides S2 for 4A OOP.
            return _bet('Step 4A PFA bluff c-bet (combo draw 12+ outs)', 'MEDIUM')

        # For 4B, 4C, 4D: OOP is blocked
        if not is_ip:
            # OOP gets only 4A — which didn't fire — so skip rest of Step 4
            pass
        else:
            # IP: evaluate 4B, 4C, 4D

            # Sub-condition 4B: near-nut flush draw with blocker
            # draw_outs >= 9 AND flush_draw_rank >= 12 AND flush_block_pct > 0
            # Wet board suppressor: if flush_danger >= 0.60 → CHECK (4B)
            if (
                draw_outs >= 9
                and fdr >= 12
                and fbp > 0
                and not (fd >= 0.60)                   # wet board suppressor for 4B
            ):
                return _bet('Step 4B PFA bluff c-bet (nut FD + blocker)', 'MEDIUM')

            # Sub-condition 4C: nut draw K/A + favorable board, IP only, no blocker req
            # draw_outs >= 9 AND flush_draw_rank >= 13 AND board_favour >= 0.30 AND is_ip == 1
            if (
                draw_outs >= 9
                and fdr >= 13
                and g(feat, 'board_favour') >= 0.30
            ):
                return _bet('Step 4C PFA bluff c-bet (nut FD K/A IP)', 'MEDIUM-LOW')

            # Sub-condition 4D: blocker + weak draw (gutshot min), IP, K/A high, rainbow
            # flush_block_pct > 0 AND draw_outs >= 4 AND villain_air_pct >= 0.40
            # AND is_ip == 1 AND high_card_rank >= 13 AND is_rainbow == 1
            # Wet board suppressor also applies to 4D: if flush_danger >= 0.60 → CHECK
            if (
                fbp > 0
                and draw_outs >= 4
                and g(feat, 'villain_air_pct') >= 0.40
                and g(feat, 'high_card_rank') >= 13
                and g(feat, 'is_rainbow') == 1
                and not (fd >= 0.60)                   # wet board suppressor for 4D
            ):
                return _bet('Step 4D PFA bluff c-bet (blocker + weak draw IP)', 'MEDIUM-LOW')

    # ------------------------------------------------------------------
    # Step 5 — Thin Value IP Non-PFA
    # S2 applies (is_ip==1 so s2_fires==False for IP anyway).
    # ALL required:
    #   is_ip == 1
    #   is_made_hand == 1
    #   hand_category >= 7
    #   villain_range_capped == 1
    #   villain_top_pair_plus_pct <= 0.35
    #   danger_score <= 0.35
    #   villain_aggression_count <= 1
    #   is_preflop_aggressor == 0
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_ip') == 1
        and g(feat, 'is_made_hand') == 1
        and g(feat, 'hand_category') >= 7
        and g(feat, 'villain_range_capped') == 1
        and g(feat, 'villain_top_pair_plus_pct') <= 0.35
        and g(feat, 'danger_score') <= 0.35
        and g(feat, 'villain_aggression_count') <= 1
        and g(feat, 'is_preflop_aggressor') == 0
    ):
        return _bet('Step 5 thin value IP non-PFA', 'MEDIUM-LOW')

    # ------------------------------------------------------------------
    # Step 6 — OOP Value Bet Exception (KB Example 6 Pattern)
    # Overrides S2 (stronger requirements than S2 thresholds).
    # ALL required:
    #   is_ip == 0
    #   raw_equity >= 0.65
    #   villain_air_pct >= 0.45
    #   is_rainbow == 1
    #   connectivity_score <= 3  (recalibrated from 0.25; integer scale, dry-board gate)
    #   hand_category >= 8
    #   villain_aggression_count == 0
    #   villain_fold_equity_estimate >= 0.35
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_ip') == 0
        and g(feat, 'raw_equity') >= 0.65
        and g(feat, 'villain_air_pct') >= 0.45
        and g(feat, 'is_rainbow') == 1
        and g(feat, 'connectivity_score') <= 3
        and g(feat, 'hand_category') >= 8
        and g(feat, 'villain_aggression_count') == 0
        and g(feat, 'villain_fold_equity_estimate') >= 0.35
    ):
        return _bet('Step 6 OOP value exception', 'MEDIUM-LOW')

    # ------------------------------------------------------------------
    # Step 7 — Default: CHECK
    # ------------------------------------------------------------------

    # If S2 fired and no OOP override step fired, CHECK
    if s2_fires:
        return _check('S2 OOP suppressor (no override step fired)')

    return _check('Step 7 default CHECK')


# ---------------------------------------------------------------------------
# FOLD tree  (FOLD_DECISION_TREE_V1.md)
# ---------------------------------------------------------------------------

def apply_fold_tree(feat: dict) -> dict:
    """
    Implements FOLD_DECISION_TREE_V1.md exactly.
    Only called when facing bet AND RAISE tree returned None.

    Returns dict:
        action      : 'FOLD' or 'CALL'
        step_fired  : description string
        confidence  : 'HIGH' / 'MEDIUM-HIGH' / 'MEDIUM' / None
    """

    def _fold(step_name, confidence='HIGH'):
        return {'action': 'FOLD', 'step_fired': step_name, 'confidence': confidence}

    def _call(step_name):
        return {'action': 'CALL', 'step_fired': step_name, 'confidence': None}

    # ------------------------------------------------------------------
    # Global Pre-Check C: is_monster == 1 → always CALL
    # ------------------------------------------------------------------
    if g(feat, 'is_monster') == 1:
        return _call('FOLD pre-check C: monster always calls')

    # ------------------------------------------------------------------
    # Step 1 — Equity Below Pot Odds (Pure Math Fold)
    # ALL required:
    #   raw_equity < pot_odds
    #   draw_outs < 6
    #   overcard_outs < 4
    #   is_monster == 0
    # ------------------------------------------------------------------

    if (
        g(feat, 'raw_equity') < g(feat, 'pot_odds')
        and g(feat, 'draw_outs') < 6
        and g(feat, 'overcard_outs') < 4
        and g(feat, 'is_monster') == 0
    ):
        return _fold('Step 1 equity below pot odds (pure math fold)', 'HIGH')

    # ------------------------------------------------------------------
    # Step 2 — Pure Air: No Made Hand, No Draw, No Showdown Value
    # ALL required:
    #   is_made_hand == 0
    #   draw_outs == 0
    #   has_showdown_value == 0
    #   overcard_outs < 4
    #   is_monster == 0
    # ------------------------------------------------------------------

    if (
        g(feat, 'is_made_hand') == 0
        and g(feat, 'draw_outs') == 0
        and g(feat, 'has_showdown_value') == 0
        and g(feat, 'overcard_outs') < 4
        and g(feat, 'is_monster') == 0
    ):
        return _fold('Step 2 pure air (no made hand, no draw, no SDV)', 'HIGH')

    # ------------------------------------------------------------------
    # Step 3 — Thin Equity + Multi-Street Aggression (MW-50 pattern)
    # ALL required:
    #   equity_margin < 0.05
    #   villain_aggression_count >= 2
    #   is_monster == 0
    #   draw_outs < 8
    #   has_showdown_value == 0 OR villain_top_pair_plus_pct >= 0.55
    # ------------------------------------------------------------------

    if (
        g(feat, 'equity_margin') < 0.05
        and g(feat, 'villain_aggression_count') >= 2
        and g(feat, 'is_monster') == 0
        and g(feat, 'draw_outs') < 8
        and (
            g(feat, 'has_showdown_value') == 0
            or g(feat, 'villain_top_pair_plus_pct') >= 0.55
        )
    ):
        return _fold('Step 3 thin equity + multi-street aggression (MW-50)', 'HIGH')

    # ------------------------------------------------------------------
    # Step 4 — Bet-and-Call Signal with Dominated Non-Premium
    # ALL required:
    #   num_callers_to_bet >= 1
    #   hero_range_percentile < 0.40
    #   equity_margin < 0.10
    #   is_monster == 0
    #   is_made_hand == 1
    #   draw_outs < 6
    # ------------------------------------------------------------------

    if (
        g(feat, 'num_callers_to_bet') >= 1
        and g(feat, 'hero_range_percentile') < 0.40
        and g(feat, 'equity_margin') < 0.10
        and g(feat, 'is_monster') == 0
        and g(feat, 'is_made_hand') == 1
        and g(feat, 'draw_outs') < 6
    ):
        return _fold('Step 4 bet-and-call dominated non-premium', 'MEDIUM-HIGH')

    # ------------------------------------------------------------------
    # Step 5 — Board Heavily Favours Villain, Uncapped Range, Thin Equity
    # ALL required:
    #   board_favour <= -0.30
    #   villain_range_capped == 0
    #   equity_margin < 0.10
    #   is_monster == 0
    #   draw_outs < 6
    #   villain_aggression_count >= 1
    # ------------------------------------------------------------------

    if (
        g(feat, 'board_favour') <= -0.30
        and g(feat, 'villain_range_capped') == 0
        and g(feat, 'equity_margin') < 0.10
        and g(feat, 'is_monster') == 0
        and g(feat, 'draw_outs') < 6
        and g(feat, 'villain_aggression_count') >= 1
    ):
        return _fold('Step 5 board favours villain uncapped + thin equity', 'MEDIUM')

    # ------------------------------------------------------------------
    # Default — CALL
    # ------------------------------------------------------------------
    return _call('FOLD default CALL (no fold step fired)')


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def label_situation(feat: dict) -> dict:
    """
    Orchestrates the three-tree decision flow:
        if to_call == 0 → BET tree
        else → RAISE tree; if no RAISE → FOLD tree

    Returns:
        action      : BET / CHECK / RAISE / CALL / FOLD
        tree_used   : 'bet_tree' / 'raise_tree' / 'fold_tree'
        step_fired  : which step determined the label
        confidence  : from the firing tree
    """
    to_call = g(feat, 'to_call', 0)

    if to_call == 0:
        # Not facing a bet — run BET tree
        result = apply_bet_tree(feat)
        return {
            'action': result['action'],
            'tree_used': 'bet_tree',
            'step_fired': result['step_fired'],
            'confidence': result['confidence'],
        }
    else:
        # Facing a bet — run RAISE tree first
        raise_result = apply_raise_tree(feat)
        if raise_result['action'] == 'RAISE':
            return {
                'action': 'RAISE',
                'tree_used': 'raise_tree',
                'step_fired': raise_result['step_fired'],
                'confidence': raise_result['confidence'],
            }
        else:
            # RAISE tree did not fire — run FOLD tree
            fold_result = apply_fold_tree(feat)
            return {
                'action': fold_result['action'],
                'tree_used': 'fold_tree',
                'step_fired': fold_result['step_fired'],
                'confidence': fold_result['confidence'],
            }


# ---------------------------------------------------------------------------
# Load and label all situations
# ---------------------------------------------------------------------------

def load_situations() -> list:
    """Load all 563 situations from the three batch files."""
    base = '/home/rupertbeytell/river-rats-v2/training-data'
    files = [
        os.path.join(base, 'factory_situations.jsonl'),
        os.path.join(base, 'factory_batch2_situations.jsonl'),
        os.path.join(base, 'factory_batch3_situations.jsonl'),
    ]
    records = []
    for fpath in files:
        with open(fpath) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
    return records


def main():
    print('Loading situations...')
    records = load_situations()
    print(f'Loaded {len(records)} situations.')

    labelled = []
    for idx, record in enumerate(records):
        sid = situation_id(record, idx)
        result = label_situation(record)

        # Build output: original record fields first, then deterministic labels on top.
        # Deterministic fields MUST come after the record spread to avoid being overwritten
        # by original 'action' (which is CALL placeholder in all factory files).
        output = {
            **{k: v for k, v in record.items()},
            # Deterministic label fields — override any same-named original fields
            'situation_id': sid,
            'action': result['action'],
            'original_action': record.get('action'),  # preserve source label for audit
            'tree_used': result['tree_used'],
            'step_fired': result['step_fired'],
            'confidence': result['confidence'],
        }
        labelled.append(output)

    # Write output
    out_path = '/home/rupertbeytell/river-rats-v2/review/deterministic_labels.json'
    with open(out_path, 'w') as fh:
        json.dump(labelled, fh, indent=2)
    print(f'\nWrote {len(labelled)} labelled situations to:\n  {out_path}')

    # ------------------------------------------------------------------
    # Summary report
    # ------------------------------------------------------------------
    action_dist = Counter(r['action'] for r in labelled)
    tree_dist = Counter(r['tree_used'] for r in labelled)
    step_dist = Counter(r['step_fired'] for r in labelled)

    print('\n=== ACTION DISTRIBUTION ===')
    for action, count in sorted(action_dist.items()):
        pct = 100.0 * count / len(labelled)
        print(f'  {action:<8} {count:>4}  ({pct:5.1f}%)')

    print('\n=== TREE USAGE ===')
    for tree, count in sorted(tree_dist.items()):
        pct = 100.0 * count / len(labelled)
        print(f'  {tree:<20} {count:>4}  ({pct:5.1f}%)')

    print('\n=== STEP FREQUENCY (all steps) ===')
    for step, count in step_dist.most_common():
        pct = 100.0 * count / len(labelled)
        print(f'  {count:>4}  ({pct:5.1f}%)  {step}')

    # Note: the factory situation files store 'action: CALL' as a placeholder.
    # The 'action' field in source records is NOT a validated expert label —
    # the deterministic tree output IS the label this script produces.
    # No agreement check against source is meaningful.

    # Sanity check: every situation must have a valid action
    valid_actions = {'BET', 'CHECK', 'RAISE', 'CALL', 'FOLD'}
    invalid = [r for r in labelled if r['action'] not in valid_actions]
    if invalid:
        print(f'\nWARNING: {len(invalid)} situations with invalid action:')
        for r in invalid[:5]:
            print(f'  {r["situation_id"]}: action={r["action"]}')
    else:
        print(f'\nSanity check PASSED: all {len(labelled)} situations have valid actions.')

    # Sanity check: BET tree should only produce BET or CHECK
    bet_tree_bad = [r for r in labelled if r['tree_used'] == 'bet_tree' and r['action'] not in ('BET', 'CHECK')]
    # Raise tree should only produce RAISE (None cases never reach output)
    raise_tree_bad = [r for r in labelled if r['tree_used'] == 'raise_tree' and r['action'] != 'RAISE']
    # Fold tree should only produce FOLD or CALL
    fold_tree_bad = [r for r in labelled if r['tree_used'] == 'fold_tree' and r['action'] not in ('FOLD', 'CALL')]
    if bet_tree_bad or raise_tree_bad or fold_tree_bad:
        print(f'WARNING: Tree/action mismatches — bet:{len(bet_tree_bad)} raise:{len(raise_tree_bad)} fold:{len(fold_tree_bad)}')
    else:
        print('Sanity check PASSED: tree/action consistency correct.')


if __name__ == '__main__':
    main()
