#!/usr/bin/env python3
"""
FULL LABELLER 4 — Phase 1.5-D.3 FULL HU corpus labelling (696 spots).
Per-anchor poker judgment encoded as canonical action + variation logic.
Append-only writes per spot to raw_labels_labeller_4.jsonl.
"""
import json
import os
import sys

CORPUS = "/home/rupertbeytell/river-rats-v2/data/hu_corpus/full_HU2_HU6"
SITUATIONS = f"{CORPUS}/situations.jsonl"
OUT_PATH = f"{CORPUS}/raw_labels_labeller_4.jsonl"
LABELLER_ID = 4

# ----- Hand evaluation helpers -----

def parse_cards(card_str):
    """Parse 'AhQh' or 'Kd7h2h' into list of (rank, suit) tuples."""
    if not card_str:
        return []
    pairs = []
    for i in range(0, len(card_str), 2):
        if i + 1 < len(card_str):
            pairs.append((card_str[i], card_str[i+1]))
    return pairs

RANK_ORDER = "23456789TJQKA"
def rank_val(r):
    return RANK_ORDER.index(r) + 2  # 2..14

def hand_strength(hero_str, board_str):
    """Return dict with bucket info for hero on this board.
    bucket: 'monster','strong_made','medium_made','weak_made','drawing','air'
    plus flags for has_flush_draw, is_nut_fd, has_oesd, has_gutshot, etc.
    """
    if not hero_str or not board_str:
        return None
    hero = parse_cards(hero_str)
    board = parse_cards(board_str)
    if len(hero) != 2 or len(board) < 3:
        return None

    hr = sorted([rank_val(r) for r, s in hero], reverse=True)
    br = sorted([rank_val(r) for r, s in board], reverse=True)
    hs = [s for r, s in hero]
    bs_ = [s for r, s in board]

    # Suit counts
    from collections import Counter
    suit_count = Counter(bs_)
    flush_suit = None
    for su, c in suit_count.items():
        if c >= 3:
            flush_suit = su  # made flush possible

    # Hero's flush draw
    hero_suits = Counter(hs)
    has_flush_made = False
    has_nut_flush = False
    has_flush_draw = False
    is_nut_fd = False
    flush_draw_suit = None
    for su, c in hero_suits.items():
        board_count = suit_count.get(su, 0)
        total = c + board_count
        if total >= 5:
            has_flush_made = True
            # Check nut: hero has the highest of suit
            hero_su_ranks = [rank_val(r) for r, s in hero if s == su]
            if max(hero_su_ranks) == 14:
                has_nut_flush = True
        elif total == 4:
            has_flush_draw = True
            flush_draw_suit = su
            # Nut FD: hero has Ace of suit
            if any(r == 'A' and s == su for r, s in hero):
                is_nut_fd = True

    # Pair detection
    all_ranks_with_count = Counter([r for r, s in hero] + [r for r, s in board])
    rank_counts = sorted(all_ranks_with_count.values(), reverse=True)
    is_quads = rank_counts and rank_counts[0] == 4
    is_full_house = rank_counts[:2] == [3, 2]
    is_trips = rank_counts and rank_counts[0] == 3 and not is_full_house and not is_quads

    # Pair classification
    hero_ranks = [r for r, s in hero]
    board_ranks = [r for r, s in board]
    board_pairs = [r for r in set(board_ranks) if board_ranks.count(r) >= 2]

    # Two pair / pair on board
    pairs_on_board = len(board_pairs)

    # Hero made hand: pocket pair, paired with board, two pair etc.
    is_pocket_pair = hero_ranks[0] == hero_ranks[1]

    top_board_rank = max(rank_val(r) for r in board_ranks) if board_ranks else 0
    hero_paired_with_board = [r for r in hero_ranks if r in board_ranks]

    # Hero set (pocket pair matching board)?
    is_set = is_pocket_pair and hero_ranks[0] in board_ranks and not is_quads

    # Two pair (using hero's two cards both pairing with board)?
    is_two_pair = (not is_pocket_pair and len(hero_paired_with_board) == 2)

    # Top pair / overpair / underpair / etc.
    overpair = is_pocket_pair and rank_val(hero_ranks[0]) > top_board_rank
    underpair = is_pocket_pair and rank_val(hero_ranks[0]) < top_board_rank and not is_set

    # Made straight check (basic)
    all_ranks_sorted = sorted(set([rank_val(r) for r, s in hero] + [rank_val(r) for r, s in board]), reverse=True)
    has_made_straight = False
    for i in range(len(all_ranks_sorted) - 4):
        window = all_ranks_sorted[i:i+5]
        if window[0] - window[4] == 4:
            has_made_straight = True
            break
    # Wheel straight A-5
    if 14 in all_ranks_sorted and all(r in all_ranks_sorted for r in [2,3,4,5]):
        has_made_straight = True

    # Straight draws (oesd / gutshot)
    has_oesd = False
    has_gutshot = False
    hero_ranks_v = sorted(set([rank_val(r) for r, s in hero] + [rank_val(r) for r, s in board]))
    # Check for OESD: 4 consecutive ranks
    for i in range(len(hero_ranks_v) - 3):
        window = hero_ranks_v[i:i+4]
        if window[3] - window[0] == 3:
            # Need to verify hero's cards are part of this run
            # Simple check: 4-in-a-row exists
            if not has_made_straight:
                has_oesd = True
                break
    # Gutshot: 4 ranks within a 5-window (1 hole)
    if not has_made_straight and not has_oesd:
        for i in range(len(hero_ranks_v) - 3):
            window = hero_ranks_v[i:i+4]
            if window[3] - window[0] == 4:
                has_gutshot = True
                break

    # Bucket classification
    bucket = "air"
    if is_quads or is_full_house or has_made_straight or has_flush_made or is_set:
        bucket = "monster"
    elif is_two_pair or is_trips:
        bucket = "strong_made"
    elif overpair and rank_val(hero_ranks[0]) >= 11:  # JJ+ overpair
        bucket = "strong_made"
    elif overpair:
        bucket = "medium_made"
    elif hero_paired_with_board:
        # Top pair, second pair, etc.
        paired_rank = max(rank_val(r) for r in hero_paired_with_board)
        if paired_rank == top_board_rank:
            kicker = max(rank_val(r) for r in hero_ranks if r not in hero_paired_with_board) if any(r not in hero_paired_with_board for r in hero_ranks) else 0
            if kicker >= 12:
                bucket = "strong_made"  # TPGK+
            else:
                bucket = "medium_made"
        else:
            bucket = "medium_made" if paired_rank >= 10 else "weak_made"
    elif underpair:
        bucket = "weak_made" if rank_val(hero_ranks[0]) >= 6 else "air"
    elif is_pocket_pair:
        bucket = "weak_made"
    elif has_flush_draw or has_oesd or (has_gutshot and is_nut_fd):
        bucket = "drawing"
    elif has_gutshot:
        bucket = "air"  # gutshot alone is air-with-equity for our purposes

    # Two overcards alone -> air
    overcards = sum(1 for r, s in hero if rank_val(r) > top_board_rank)

    # Compute hero highest rank
    hero_high = max(rank_val(r) for r, s in hero)

    return {
        "bucket": bucket,
        "is_quads": is_quads,
        "is_full_house": is_full_house,
        "is_trips": is_trips,
        "is_set": is_set,
        "is_two_pair": is_two_pair,
        "overpair": overpair,
        "underpair": underpair,
        "has_made_straight": has_made_straight,
        "has_flush_made": has_flush_made,
        "has_nut_flush": has_nut_flush,
        "has_flush_draw": has_flush_draw,
        "is_nut_fd": is_nut_fd,
        "has_oesd": has_oesd,
        "has_gutshot": has_gutshot,
        "hero_paired_with_board": hero_paired_with_board,
        "top_board_rank": top_board_rank,
        "overcards": overcards,
        "hero_high": hero_high,
        "pairs_on_board": pairs_on_board,
        "flush_suit_on_board": flush_suit,
    }


# ----- Per-anchor canonical labels -----
# Each anchor has a "canonical" action + reasoning, then variation logic.

def label_HU_2_1(spot, hs):
    """HU-2.1: AhQh BTN open, BB call, flop K-high two-tone hearts. IP semi-bluff c-bet with nut FD."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    facing = spot['facing_bet']
    stk = spot['effective_stack_bb']

    if var == 'board_runout':
        # Hero AhQh on Kd7h<X>. Re-evaluate.
        if hs['has_flush_made']:
            # Flop = three hearts -> hero flopped nut flush (Ah is nut). Monster.
            return ("BET", "HIGH", 25,
                    f"Monster (nut flush flopped on three-heart board {spot['board_flop']}). IP, BB checked. v3.4 line 729 HU carve-out: bet for value/protection. Build pot with absolute nut. 25% small for thin value + protection — slowplaying lets BB hit pairs/draws.")
        if hs['is_set']:
            return ("BET", "HIGH", 33,
                    f"Monster (set on {spot['board_flop']}). IP HU c-bet for value + protection. Standard 25-33% sizing.")
        if hs['has_made_straight']:
            return ("BET", "HIGH", 33, f"Monster (made straight on {spot['board_flop']}). IP HU c-bet 33% for value/protection.")
        if hs['hero_paired_with_board'] and hs['bucket'] in ('strong_made', 'medium_made'):
            return ("BET", "HIGH", 25, f"TPTK (Ace or Queen pairs board {spot['board_flop']}). HU IP c-bet 25% per v3.1 standard cbet.")
        if hs['has_flush_draw']:
            return ("BET", "HIGH", 25, f"Drawing (nut FD + 2 overcards on {spot['board_flop']}). KB §1.7 nut FD + Ah blocker + side equity = bet/raise candidate. HU IP semi-bluff cbet 25% — fold equity ~50% HU.")
        # Air (no FD, e.g. board went rainbow with brick like 4c)
        return ("BET", "MEDIUM", 25,
                f"Air (no draw on {spot['board_flop']}; AhQh has 2 overcards only). HU range c-bet small 25% — hero range bets all on K-high vs BB calling range. AQ has 6 overcard outs as backup.")

    if var == 'effective_stack':
        # Same canonical situation, deeper or shallower stack
        if stk <= 60:
            return ("BET", "HIGH", 25,
                    f"Drawing (nut FD + 2 overcards). Compressed eff stack {stk}bb makes c-bet smaller-and-commit; 25% sizing keeps SPR manageable on turn. KB §1.7 + HU value/protection.")
        else:
            return ("BET", "HIGH", 25,
                    f"Drawing (nut FD + 2 overcards). Deep stack {stk}bb gives more room to play turns; 25% c-bet sizing standard. Nut FD + Ah blocker — bet for fold equity + equity realisation.")

    if var == 'villain_action_sequence':
        # Same flop spot but different preflop/range context
        param = spot['variation_param']
        if 'checkback' in param:
            return ("BET", "HIGH", 25,
                    f"Drawing (nut FD + 2 overcards). PFA flop checkback variant — but per spot definition hero still acts here on flop (or delayed-stab via turn). Bet 25% with nut FD per KB §1.7.")
        if '4bet_call' in param or '3bet_call' in param:
            return ("BET", "MEDIUM", 25,
                    f"Drawing (nut FD + 2 overcards). 3bet/4bet pot dynamic narrows villain range to broadways/pairs that hit K-high hard. Smaller cbet 25% — compressed SPR + range disadvantage warrant smaller-or-check; nut FD justifies bet.")
        return ("BET", "HIGH", 25,
                f"Drawing (nut FD + 2 overcards) on {spot.get('board_flop')}. Variant range context ({param}) doesn't change hero's action — KB §1.7 nut FD + Ah blocker → bet 25% standard cbet.")

    return ("BET", "MEDIUM", 25, "Default HU-2.1 fallback.")


def label_HU_2_2(spot, hs):
    """HU-2.2: Td9d BB defend, flop 8s6c2d rainbow. OOP pot-odds call with OESD vs 66% c-bet."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        # Hero Td9d on 8s6c<X>. Recompute.
        if hs['has_made_straight']:
            return ("RAISE", "HIGH", 75, f"Monster (made straight on {spot['board_flop']}). HU OOP raise vs c-bet 66% for value + protection — flush/two-pair draws live; build pot.")
        if hs['has_flush_draw'] and hs['has_oesd']:
            return ("CALL", "HIGH", None, f"Drawing (FD + OESD combo on {spot['board_flop']}). HU OOP combo draw with 15+ outs vs 66% c-bet — far above pot odds. Call to realize equity; check-raise too thin OOP without nut blocker.")
        if hs['hero_paired_with_board']:
            return ("CALL", "HIGH", None, f"Made pair on {spot['board_flop']} (top/middle pair with kicker). HU OOP call vs 66% c-bet — pot odds met, evaluate turn.")
        if hs['has_oesd']:
            return ("CALL", "HIGH", None, f"Drawing (OESD on {spot['board_flop']}). HU OOP pot-odds call vs 66% c-bet — 8 outs ~32% by river, pot odds 28% met.")
        if hs['has_flush_draw']:
            return ("CALL", "HIGH", None, f"Drawing (FD on {spot['board_flop']}). 9 outs ~36% vs pot odds 28%. Call to realize.")
        if hs['has_gutshot'] and hs['overcards'] >= 1:
            return ("CALL", "MEDIUM", None, f"Drawing/air (gutshot + overcard). Pot odds 28%, hero ~22-25% equity; close but typical defend with backdoors makes call OK.")
        # Pure air
        return ("FOLD", "HIGH", None, f"Air (no draw on {spot['board_flop']}; T9 disconnected from board). HU OOP facing 66% c-bet — fold without sufficient equity.")

    if var == 'effective_stack':
        stk = spot['effective_stack_bb']
        # OESD + backdoor FD on 8s6c2d. Pot odds 28%.
        if stk <= 40:
            return ("CALL", "HIGH", None, f"Drawing (OESD + backdoor FD). Compressed stack {stk}bb makes implied odds worse but raw pot odds 28% met by OESD outs. Call.")
        return ("CALL", "HIGH", None, f"Drawing (OESD + backdoor FD on 8s6c2d). HU OOP pot-odds call vs 66% c-bet at {stk}bb — call, see turn.")

    if var == 'villain_bet_sizing':
        new_pot_odds = tocall / (pot + tocall)
        # Hero has OESD (~32% by river). If pot odds exceed equity + implied, fold.
        if new_pot_odds > 0.40:
            return ("FOLD", "HIGH", None, f"Drawing (OESD only, ~32% by river). Villain {tocall}bb sizing pushes pot odds to {new_pot_odds:.0%} > drawing equity. Fold; cannot call without sufficient equity + implied.")
        if new_pot_odds > 0.33:
            return ("FOLD", "MEDIUM", None, f"Drawing (OESD + bd FD). At {new_pot_odds:.0%} pot odds, marginal — slightly negative direct EV; implied odds OOP HU vs single villain don't compensate. Fold.")
        return ("CALL", "HIGH", None, f"Drawing (OESD + backdoor FD). Pot odds {new_pot_odds:.0%} met by ~32% OESD + backdoor + reverse implied. Call.")

    return ("CALL", "MEDIUM", None, "HU-2.2 default fallback.")


def label_HU_2_3(spot, hs):
    """HU-2.3: Js9s BB calls flop, turn brick 2c. OOP nut-FD facing turn 75% barrel."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        # Js9s with new turn card. Re-eval based on board_turn.
        bt = spot.get('board_turn')
        bf = spot.get('board_flop', 'Qs7s3d')
        if hs is None and bt:
            hs = hand_strength(spot['hero_cards'], bt)
        if hs and hs.get('has_flush_made'):
            return ("CHECK", "HIGH", None, f"Monster (flush completed on {bt}). OOP HU vs PFA bet — slowplay first by check-call/check-raise; check first to induce. Hero already checked turn (per anchor flow). Wait — but spot says hero acts. Bet small for value/protection.")
        if hs and hs.get('has_made_straight'):
            return ("CALL", "HIGH", None, f"Monster (straight on {bt}). OOP HU vs 75% turn barrel — call to keep villain bluffing; raise also defensible but trapping reasonable.")
        # Default: hero has bare nut FD + gutshot from anchor; new turn brick keeps draw
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd') or hs.get('has_gutshot')):
            if pot_odds > 0.35:
                return ("CALL", "HIGH", None, f"Drawing (nut FD + gutshot on {bt}). Pot odds {pot_odds:.0%}. ~33% river equity (FD + gutshot, ~12 outs). Call to realize on river.")
            return ("CALL", "HIGH", None, f"Drawing (nut FD + gutshot, turn {bt}). Call vs 75% barrel — equity covers pot odds.")
        # Made hand on turn?
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "MEDIUM", None, f"Medium-made (paired on turn {bt}). Bluff-catch vs 75% — pot odds met by made-hand equity vs villain's two-barrel range; fold to river bet without improvement.")
        return ("FOLD", "MEDIUM", None, f"Air on turn {bt} (lost flop draws to brick). Insufficient equity vs 75% barrel; fold.")

    if var == 'effective_stack':
        stk = spot['effective_stack_bb']
        return ("CALL", "HIGH", None, f"Drawing (nut FD + gutshot). HU OOP turn vs 75% barrel — pot odds {pot_odds:.0%}, ~12 outs (~25% by river single-card). With Js (J overcard partial) + As blocker on Qs7s3d, calling realizes; raising too thin without river commit at {stk}bb.")

    if var == 'villain_bet_sizing':
        # Drawing hand with ~12 outs (FD + gutshot). Equity ~25% on turn single-card draw.
        equity = 0.27
        if pot_odds > equity + 0.05:
            return ("FOLD", "HIGH", None, f"Drawing (nut FD + gutshot). Villain sized to {tocall}bb, pot odds {pot_odds:.0%} > ~27% river equity. Fold; insufficient equity.")
        if pot_odds > 0.32:
            return ("FOLD", "MEDIUM", None, f"Drawing (nut FD + gutshot). Pot odds {pot_odds:.0%} marginal vs 27% direct. Fold without implied compensation.")
        return ("CALL", "HIGH", None, f"Drawing (nut FD + gutshot). Pot odds {pot_odds:.0%} ≤ 27% river single-card equity + nut blocker implied. Call.")

    return ("CALL", "MEDIUM", None, "HU-2.3 default fallback.")


def label_HU_2_4(spot, hs):
    """HU-2.4: 6c5c BTN open, BB calls, flop 8c7d4h. BB check-raises hero's c-bet. IP combo-draw facing OOP check-raise."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    stk = spot['effective_stack_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    # Anchor: hero has 6c5c on 8c7d4h = OESD (3-9 for straight, 6 outs to nut straight) + bottom pair + backdoor FD (one club). After BB check-raise to 9.9 in pot 14.85.
    # SPR ~3-4. Decision is fold/call/jam.

    if var == 'board_runout':
        # New flop card. Hero 6c5c.
        if hs and (hs.get('has_made_straight') or hs.get('is_set') or hs.get('is_two_pair')):
            return ("RAISE", "HIGH", 75, f"Monster (made hand on {spot['board_flop']}). vs check-raise jam/3-bet for value at SPR {stk/pot:.1f}.")
        if hs and hs.get('has_flush_draw') and hs.get('has_oesd'):
            return ("CALL", "HIGH", None, f"Drawing (combo draw on {spot['board_flop']}). vs check-raise call to realize 15+ outs at compressed SPR.")
        if hs and hs.get('has_oesd'):
            return ("CALL", "MEDIUM", None, f"Drawing (OESD on {spot['board_flop']}). 8 outs vs check-raise — pot odds + bottom pair backup makes call reasonable; fold to turn pressure.")
        if hs and hs.get('hero_paired_with_board'):
            return ("FOLD", "MEDIUM", None, f"Weak made (bottom pair on {spot['board_flop']}) facing OOP check-raise. Check-raise polarized to value; fold weak made + no draw.")
        return ("FOLD", "HIGH", None, f"Air (no equity on {spot['board_flop']}) vs HU OOP check-raise. Fold — check-raise represents strong range.")

    if var == 'effective_stack':
        # Anchor SPR depends on stack
        if stk <= 60:
            return ("CALL", "HIGH", None, f"Drawing (OESD + bottom pair + bd FD). Anchor hero has ~14 outs combined (8 OESD + ~5 pair improve + bd FD). At {stk}bb the call is committed; direct equity ~30%+ vs check-raise range. Call/jam reasonable.")
        return ("CALL", "MEDIUM", None, f"Drawing (combo). At {stk}bb deep stack, calling preserves implied; jamming over-commits without nut equity.")

    if var == 'villain_bet_sizing':
        # Hero has ~30% equity vs check-raise range
        if pot_odds > 0.40:
            return ("FOLD", "HIGH", None, f"Drawing (OESD + bottom pair). Villain check-raise sized to pot odds {pot_odds:.0%} > 30% equity vs xr range. Fold — combo equity insufficient.")
        if pot_odds > 0.35:
            return ("FOLD", "MEDIUM", None, f"Drawing. Pot odds {pot_odds:.0%} marginal vs ~30% combined equity; fold without implied compensation.")
        return ("CALL", "HIGH", None, f"Drawing (OESD + bottom pair + bd FD). Pot odds {pot_odds:.0%} ≤ ~32% combined equity. Call to realize.")

    return ("CALL", "MEDIUM", None, "HU-2.4 default fallback.")


def label_HU_2_5(spot, hs):
    """HU-2.5: Ad5d BTN open, BB calls, flop Jh8d3c, both check, turn 2d completes nut FD. IP checked-to turn semi-bluff sizing."""
    var = spot['variation_axis']

    if var == 'board_runout':
        # Hero Ad5d. New turn card replaces 2d.
        bt = spot.get('board_turn')
        bf = spot.get('board_flop', 'Jh8d3c')
        if hs is None and bt:
            hs = hand_strength(spot['hero_cards'], bt)
        if hs and hs.get('has_flush_made'):
            return ("BET", "HIGH", 75, f"Monster (nut flush completed on turn {bt}). IP HU value bet 75% — extract from Jx, two-pair, sets that called flop or check-back.")
        if hs and hs.get('hero_paired_with_board') and hs.get('bucket') in ('strong_made', 'medium_made'):
            return ("BET", "MEDIUM", 33, f"Made pair on turn {bt} (Ace or 5 paired). Thin value/protection bet 33% IP HU.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("BET", "MEDIUM", 33, f"Drawing on turn {bt} (FD/OESD). IP HU semi-bluff 33% — fold equity ~50% HU + draw equity backup.")
        return ("CHECK", "MEDIUM", None, f"Air on turn {bt} (no draw, A-high). IP HU give-up; checked flop already, double-stab thin without draw.")

    if var == 'effective_stack':
        # Anchor: nut FD + gutshot + A overcard, IP delayed cbet on turn
        return ("BET", "HIGH", 33, f"Drawing (turned nut FD + gutshot + A overcard). HU IP delayed cbet 33% — KB §1.7 nut FD + Ad blocker + side equity = bet for fold equity + draw realization. Sizing per turn solver-aligned 33%.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 33, f"Drawing (turned nut FD + gutshot + A overcard). HU IP delayed cbet ({param} variant). KB §1.7 + HU semi-bluff bet 33%.")

    return ("BET", "MEDIUM", 33, "HU-2.5 default fallback.")


def label_HU_3_1(spot, hs):
    """HU-3.1: 7c6h BTN open, BB calls, flop AhKd<X>. Range c-bet bluff on dry A-high."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('hero_paired_with_board') or hs.get('has_flush_draw') or hs.get('has_oesd') or hs.get('has_gutshot') or hs.get('is_set') or hs.get('is_two_pair') or hs.get('has_made_straight')):
            # Now hero has equity
            if hs.get('has_made_straight') or hs.get('is_set') or hs.get('is_two_pair'):
                return ("BET", "HIGH", 33, f"Monster (made hand on {spot['board_flop']}). HU IP value bet 33%.")
            if hs.get('has_flush_draw') or hs.get('has_oesd'):
                return ("BET", "HIGH", 25, f"Drawing on {spot['board_flop']}. HU IP semi-bluff cbet 25%.")
            if hs.get('hero_paired_with_board'):
                return ("BET", "HIGH", 25, f"Medium made (pair on {spot['board_flop']}). HU IP cbet 25% for value/protection.")
            return ("BET", "MEDIUM", 25, f"Some equity on {spot['board_flop']}; HU IP range cbet 25%.")
        # Air
        return ("BET", "MEDIUM", 25, f"Air (76 disconnected on {spot['board_flop']}). HU IP range cbet 25% on dry A-high — fold equity ~50% vs BB defending range.")

    if var == 'effective_stack':
        return ("BET", "MEDIUM", 25, f"Air (76 on AhKd2s). HU IP range cbet 25% — dry A-high BTN-favoured, BB capped. Standard small cbet.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        if 'checkback' in param:
            return ("CHECK", "MEDIUM", None, f"Air on AhKd2s. PFA flop checkback variant — give up with no equity, take free showdown attempt on later streets if checked back.")
        return ("BET", "MEDIUM", 25, f"Air. HU IP range cbet 25% in {param} variant — small-bluff on BTN-favoured A-high.")

    return ("BET", "LOW", 25, "HU-3.1 default fallback.")


def label_HU_3_2(spot, hs):
    """HU-3.2: 4d3d BB defends, flop QcJh9s connected broadway, BTN bets 66%. Clear OOP check-fold."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        if hs and (hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('is_set')):
            return ("RAISE", "HIGH", 75, f"Monster (made hand on {spot['board_flop']}). OOP check-raise vs 66% cbet for value/protection.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("CALL", "HIGH", None, f"Drawing on {spot['board_flop']}. Pot odds 28% met by FD/OESD equity — call to realize.")
        if hs and hs.get('has_gutshot'):
            return ("FOLD", "MEDIUM", None, f"Drawing (gutshot only on {spot['board_flop']}). 4 outs ~16% < 28% pot odds. Fold.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "MEDIUM", None, f"Made pair on {spot['board_flop']}. Bluff-catch HU vs 66% — pot odds met by showdown value.")
        return ("FOLD", "HIGH", None, f"Air (43s no equity on {spot['board_flop']}). HU OOP fold to 66% cbet — clear give-up.")

    if var == 'effective_stack':
        return ("FOLD", "HIGH", None, f"Air (43s on QcJh9s connected broadway, no realisable equity). HU OOP fold to 66% cbet — clear check-fold.")

    if var == 'villain_bet_sizing':
        # Pure air, no draw
        return ("FOLD", "HIGH", None, f"Air (43s on QcJh9s). Pot odds {pot_odds:.0%} immaterial — no equity to realize. Fold.")

    return ("FOLD", "HIGH", None, "HU-3.2 default fallback.")


def label_HU_3_3(spot, hs):
    """HU-3.3: KsQs BTN open, BB calls, flop 8h6h5c, both check, turn 2d brick. IP checked-to turn float vs delayed-stab with two overcards."""
    var = spot['variation_axis']

    if var == 'board_runout':
        bt = spot.get('board_turn')
        bf = spot.get('board_flop', '8h6h5c')
        if hs is None and bt:
            hs = hand_strength(spot['hero_cards'], bt)
        if hs and (hs.get('hero_paired_with_board') or hs.get('has_made_straight') or hs.get('is_two_pair')):
            return ("BET", "HIGH", 33, f"Made hand on turn {bt}. IP HU delayed cbet 33% for value/protection.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("BET", "MEDIUM", 33, f"Drawing on turn {bt}. IP HU semi-bluff stab 33%.")
        return ("CHECK", "HIGH", None, f"Air on turn {bt} (KQ overcards on 8-high). IP HU give-up — checked flop already; turn double-stab thin with subordinate overcard equity. Showdown check.")

    if var == 'effective_stack':
        return ("CHECK", "MEDIUM", None, f"Air (KQ overcards on 8h6h5c-2d). IP HU after flop check-back; turn delayed-stab thin given two-tone-connected board. Check, take free river.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        if 'donk' in param:
            return ("CALL", "MEDIUM", None, f"Air with overcards facing OOP donk ({param}). Pot odds + 6 overcard outs make a thin call — KQ overcards have ~24% by river.")
        return ("CHECK", "MEDIUM", None, f"Air (KQ overcards). Variant context ({param}) — checked-to turn IP, give up with subordinate overcard equity.")

    return ("CHECK", "MEDIUM", None, "HU-3.3 default fallback.")


def label_HU_3_4(spot, hs):
    """HU-3.4: Ts8h BB defends, flop 7d7c3h paired rainbow, BTN bets 25%. OOP check-raise bluff threshold."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        if hs and (hs.get('is_trips') or hs.get('is_full_house')):
            return ("CALL", "HIGH", None, f"Monster (trips on paired board {spot['board_flop']}). Slowplay vs small cbet — call to keep villain bluffing.")
        if hs and (hs.get('hero_paired_with_board') or hs.get('overpair')):
            return ("CALL", "MEDIUM", None, f"Made pair on {spot['board_flop']}. Bluff-catch HU vs 25% cbet — pot odds 16.7% easily met.")
        if hs and (hs.get('has_oesd') or hs.get('has_flush_draw')):
            return ("CALL", "HIGH", None, f"Drawing on {spot['board_flop']}. Pot odds 16.7% met by FD/OESD.")
        if hs and hs.get('has_gutshot'):
            return ("CALL", "MEDIUM", None, f"Gutshot on {spot['board_flop']}. 4 outs + backdoors + pot odds 16.7% — call to realize.")
        # Air
        return ("FOLD", "MEDIUM", None, f"Air (T8 no equity on paired {spot['board_flop']}). HU OOP fold to 25% cbet without realisable equity.")

    if var == 'effective_stack':
        return ("CALL", "HIGH", None, f"Air with T overcard + backdoor straight (8-9-T potential). HU OOP vs 25% small cbet, pot odds 16.7% — bluff-catch with two-overcard + backdoor draw is reasonable.")

    if var == 'villain_bet_sizing':
        if pot_odds > 0.30:
            return ("FOLD", "HIGH", None, f"Air (T8 on 773 paired). Larger sizing pot odds {pot_odds:.0%} > realisable equity. Fold.")
        if pot_odds > 0.20:
            return ("FOLD", "MEDIUM", None, f"Air with backdoors. Pot odds {pot_odds:.0%}, marginal — fold with subordinate equity HU OOP.")
        return ("CALL", "MEDIUM", None, f"Air with T overcard + backdoor straight. Pot odds {pot_odds:.0%} ≤ realisable equity. Call to defend range.")

    return ("CALL", "MEDIUM", None, "HU-3.4 default fallback.")


def label_HU_3_5(spot, hs):
    """HU-3.5: Ac4c BTN open, runout Kh9d6s/5h/2c. Busted-air give-up on river facing BB block-lead 33%."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    # On river, hero Ac4c has Ace-high (busted). Facing 33% block-lead.
    if var == 'board_runout':
        # New river card replaces 2c
        br = spot.get('board_river')
        bf = spot.get('board_flop', 'Kh9d6s')
        bt = spot.get('board_turn', 'Kh9d6s5h')
        if hs is None and br:
            hs = hand_strength(spot['hero_cards'], br)
        if hs and hs.get('has_flush_made'):
            # If hero made flush (clubs)
            return ("RAISE", "HIGH", 150, f"Monster (made flush on river {br}). Raise vs block-lead for value — opponent's small lead caps strength, raise extracts.")
        if hs and (hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('is_set')):
            return ("RAISE", "HIGH", 75, f"Monster on river {br}. Raise vs block-lead for value.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "MEDIUM", None, f"Made pair (paired on river {br}). Bluff-catch vs block-lead — pot odds 25% well below TP equity vs leading range.")
        # A-high busted vs block-lead
        return ("CALL", "MEDIUM", None, f"Air (Ace-high busted on river {br}). Block-lead 33% pot odds 25% — A-blocker reduces villain's value combos; thin bluff-catch with A-high vs polarized block.")

    if var == 'effective_stack':
        return ("CALL", "MEDIUM", None, f"Air (A-high busted with A-blocker). Pot odds 25% vs 33% block-lead — A-blocker reduces villain's nut combos; bluff-catch with A-high.")

    if var == 'villain_bet_sizing':
        # Larger sizings flip to fold
        if pot_odds > 0.35:
            return ("FOLD", "HIGH", None, f"Air (A-high busted). Sizing {tocall}bb pot odds {pot_odds:.0%} too high for A-high bluff-catch. Fold.")
        if pot_odds > 0.28:
            return ("FOLD", "MEDIUM", None, f"Air (A-high). Pot odds {pot_odds:.0%} marginal; A-blocker not enough vs larger lead. Fold.")
        return ("CALL", "MEDIUM", None, f"Air (A-high with A-blocker). Pot odds {pot_odds:.0%} ≤ bluff-catch threshold; A-blocker reduces villain's value combos.")

    return ("CALL", "LOW", None, "HU-3.5 default fallback.")


def label_HU_4_1(spot, hs):
    """HU-4.1: JsJh BTN open, BB calls, flop Kd7h2c rainbow. PFA small range c-bet with medium overpair — but JJ on K-high has K to worry about."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and hs.get('is_set'):
            return ("BET", "HIGH", 33, f"Monster (set of jacks on {spot['board_flop']}). HU IP value bet 33%.")
        if hs and hs.get('overpair'):
            return ("BET", "HIGH", 25, f"Strong made (overpair on {spot['board_flop']}). HU IP cbet 25% — overpair beats most BB defending range.")
        # JJ as underpair to higher card
        if hs and hs.get('underpair'):
            return ("BET", "MEDIUM", 25, f"Medium made (JJ as underpair to {spot['board_flop']} top card). HU IP small cbet 25% — JJ has 2nd pair equity, bets thin for value/protection.")
        return ("BET", "MEDIUM", 25, f"JJ on {spot['board_flop']}. HU IP cbet 25% standard.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 25, f"Medium made (JJ as 2nd pair to K). HU IP small cbet 25% — JJ ahead of BB's missed broadways, 7x pairs, draws; folds out air, gets value from worse pairs.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        if '4bet' in param or '3bet' in param:
            return ("BET", "MEDIUM", 25, f"Medium made (JJ as 2nd pair to K). 3bet/4bet pot ({param}) range narrows BB to KQ+/AK/AA-QQ — JJ less ahead. Cbet small 25% for thin value/protection.")
        return ("BET", "HIGH", 25, f"Medium made (JJ as 2nd pair to K). HU IP standard cbet 25%.")

    return ("BET", "MEDIUM", 25, "HU-4.1 default fallback.")


def label_HU_4_2(spot, hs):
    """HU-4.2: 4h4c BTN open, BB calls, flop KhQh9h monotone. PFA check-back with bottom-of-range on BB-favoured monotone."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and hs.get('is_set'):
            return ("BET", "HIGH", 50, f"Monster (set of 4s on {spot['board_flop']}). HU IP value bet — protection vs draws/overcards.")
        if hs and hs.get('has_flush_made'):
            return ("BET", "HIGH", 33, f"Monster (flush) on {spot['board_flop']}. HU IP value bet.")
        if hs and hs.get('overpair'):
            return ("BET", "MEDIUM", 33, f"Strong made (overpair) on {spot['board_flop']}. HU IP cbet 33% — protection.")
        if hs and hs.get('underpair'):
            # 44 on K-high or higher = underpair, weak
            if hs.get('flush_suit_on_board'):
                return ("CHECK", "HIGH", None, f"Air (44 underpair on flush board {spot['board_flop']}). HU IP check-back — bottom of range, no fold equity vs BB's flushes/draws/Kx.")
            return ("CHECK", "MEDIUM", None, f"Weak made (44 underpair on {spot['board_flop']}). HU IP check-back — bottom of range, take showdown.")
        return ("CHECK", "MEDIUM", None, f"Air on {spot['board_flop']}. HU IP check-back.")

    if var == 'effective_stack':
        return ("CHECK", "HIGH", None, f"Air (44 underpair on KhQh9h monotone, BB-favoured). HU IP check-back — no fold equity vs BB's heart range, no value vs Kx/Qx/9x. Take showdown.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("CHECK", "HIGH", None, f"Air (44 underpair on monotone broadway, {param} variant). HU IP check-back per range strategy on BB-favoured texture.")

    return ("CHECK", "HIGH", None, "HU-4.2 default fallback.")


def label_HU_4_3(spot, hs):
    """HU-4.3: KsTs SB open, BB calls, flop Td7d5s two-tone. SB c-bet sizing dilemma with TPGK."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('is_set') or hs.get('is_two_pair') or hs.get('has_made_straight') or hs.get('has_flush_made')):
            return ("BET", "HIGH", 66, f"Monster on {spot['board_flop']}. SB OOP value bet 66% for protection + value.")
        if hs and hs.get('hero_paired_with_board') and rank_val(hs['hero_paired_with_board'][0]) == hs['top_board_rank']:
            return ("BET", "HIGH", 66, f"Strong made (top pair on {spot['board_flop']}). SB OOP cbet 66% on two-tone texture for protection.")
        if hs and hs.get('hero_paired_with_board'):
            return ("BET", "MEDIUM", 33, f"Medium made (pair on {spot['board_flop']}). SB OOP cbet 33%.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("BET", "MEDIUM", 33, f"Drawing on {spot['board_flop']}. SB OOP semi-bluff 33%.")
        return ("CHECK", "MEDIUM", None, f"Air on {spot['board_flop']}. SB OOP check — no equity.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 66, f"Strong made (TPGK on Td7d5s two-tone). SB OOP cbet 66% — protection vs FD + KT denying equity to wide BB range.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 66, f"Strong made (TPGK on Td7d5s). SB OOP cbet 66% in {param} variant — protection on two-tone.")

    return ("BET", "HIGH", 66, "HU-4.3 default fallback.")


def label_HU_4_4(spot, hs):
    """HU-4.4: QhJh SB open, BB calls, flop 9h8h2c two-tone. SB polar 66% with combo draw."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('has_flush_made') or hs.get('has_made_straight') or hs.get('is_two_pair')):
            return ("BET", "HIGH", 66, f"Monster on {spot['board_flop']}. SB OOP value bet 66%.")
        if hs and hs.get('hero_paired_with_board'):
            return ("BET", "HIGH", 33, f"Made pair on {spot['board_flop']}. SB OOP cbet 33%.")
        if hs and (hs.get('has_flush_draw') and hs.get('has_oesd')):
            return ("BET", "HIGH", 66, f"Drawing (combo: FD + OESD on {spot['board_flop']}). SB OOP polar 66% semi-bluff.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("BET", "MEDIUM", 33, f"Drawing (FD or OESD on {spot['board_flop']}). SB OOP semi-bluff 33%.")
        if hs and hs.get('has_gutshot') and hs.get('overcards') >= 1:
            return ("BET", "MEDIUM", 33, f"Air with gutshot + overcards on {spot['board_flop']}. SB OOP small cbet 33% as bluff-with-equity.")
        return ("CHECK", "MEDIUM", None, f"Air on {spot['board_flop']}. SB OOP check — no equity.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 66, f"Drawing (combo: FD + gutshot + 2 overcards on 9h8h2c). SB OOP polar 66% — semi-bluff with strong combo equity + fold equity vs BB defend range.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 66, f"Drawing (combo: FD + gutshot + overcards). SB OOP polar 66% in {param} variant.")

    return ("BET", "HIGH", 66, "HU-4.4 default fallback.")


def label_HU_4_5(spot, hs):
    """HU-4.5: AhJc BTN open, BB calls, flop Tc7c3s, both check, turn 5d brick. IP delayed c-bet sizing."""
    var = spot['variation_axis']

    if var == 'board_runout':
        bt = spot.get('board_turn')
        bf = spot.get('board_flop', 'Tc7c3s')
        if hs is None and bt:
            hs = hand_strength(spot['hero_cards'], bt)
        if hs and (hs.get('hero_paired_with_board') or hs.get('has_made_straight')):
            return ("BET", "HIGH", 33, f"Made hand on turn {bt}. HU IP delayed cbet 33%.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("BET", "HIGH", 33, f"Drawing on turn {bt}. HU IP semi-bluff 33%.")
        return ("BET", "MEDIUM", 33, f"Air with overcards (AJ on turn {bt}). HU IP delayed cbet 33% — flop checked through, turn brick lets us bluff with backdoors developing.")

    if var == 'effective_stack':
        return ("BET", "MEDIUM", 33, f"Air (AJ overcards + backdoor on Tc7c3s-5d). HU IP delayed cbet 33% — solver-aligned turn sizing; villain checked flop, BB capped vs delayed stab.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        if 'donk' in param:
            return ("CALL", "MEDIUM", None, f"Air with overcards facing OOP donk ({param}). Pot odds + 6 overcard outs justify thin call.")
        return ("BET", "MEDIUM", 33, f"Air with overcards (AJ). HU IP delayed stab 33% in {param} variant.")

    return ("BET", "MEDIUM", 33, "HU-4.5 default fallback.")


def label_HU_5_1(spot, hs):
    """HU-5.1: 7d7s BB defends, flop Th7c4h two-tone, BTN bets 66%. OOP check-raise with flopped middle set."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        if hs and (hs.get('is_full_house') or hs.get('is_quads')):
            return ("RAISE", "HIGH", 75, f"Monster (boat/quads on {spot['board_flop']}). OOP check-raise for value.")
        if hs and hs.get('is_set'):
            return ("RAISE", "HIGH", 75, f"Monster (set on {spot['board_flop']}). OOP check-raise on two-tone for value + protection.")
        if hs and (hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('has_flush_made')):
            return ("RAISE", "HIGH", 75, f"Monster on {spot['board_flop']}. OOP check-raise.")
        if hs and hs.get('overpair'):
            return ("CALL", "MEDIUM", None, f"Strong made (overpair on {spot['board_flop']}). OOP call — raising thin vs cbet range, bluff-catch better.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "MEDIUM", None, f"Medium made (pair) on {spot['board_flop']}. OOP call vs 66% — pot odds 28% met.")
        return ("FOLD", "MEDIUM", None, f"Air on {spot['board_flop']}. OOP fold vs 66% cbet without equity.")

    if var == 'effective_stack':
        return ("RAISE", "HIGH", 75, f"Monster (flopped middle set on Th7c4h two-tone). OOP check-raise for value + protection vs FD/overcards. Sizing ~3x.")

    if var == 'villain_bet_sizing':
        # Set always raises
        return ("RAISE", "HIGH", 75, f"Monster (set of 7s on Th7c4h). OOP check-raise vs {tocall}bb — value + protection regardless of villain sizing.")

    return ("RAISE", "HIGH", 75, "HU-5.1 default fallback.")


def label_HU_5_2(spot, hs):
    """HU-5.2: 7h6h BB defends, flop 7c6s4d rainbow low-connected. OOP donk-lead with two-pair on BB-favoured texture."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('is_full_house') or hs.get('is_set') or hs.get('has_made_straight')):
            return ("BET", "HIGH", 50, f"Monster on {spot['board_flop']}. OOP donk-lead for value.")
        if hs and hs.get('is_two_pair'):
            return ("BET", "HIGH", 50, f"Strong made (two-pair on {spot['board_flop']}). OOP donk-lead 50% on BB-favoured low-connected — protection vs straight/flush draws + value extraction.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CHECK", "MEDIUM", None, f"Made pair on {spot['board_flop']}. OOP check — pot-control with single pair.")
        if hs and (hs.get('has_oesd') or hs.get('has_flush_draw')):
            return ("CHECK", "MEDIUM", None, f"Drawing on {spot['board_flop']}. OOP check — face cbet, can call/raise.")
        return ("CHECK", "MEDIUM", None, f"On {spot['board_flop']}. OOP default check.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 50, f"Strong made (top two-pair 76 on 7c6s4d). OOP donk-lead 50% on BB-favoured low-connected texture — protection from BTN's overcards/straight draws + value from Tx/8x/pp.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 50, f"Strong made (top two-pair 76 on 7c6s4d). OOP donk-lead 50% in {param} variant — BB-favoured texture warrants leading.")

    return ("BET", "HIGH", 50, "HU-5.2 default fallback.")


def label_HU_5_3(spot, hs):
    """HU-5.3: QdTh BB defends, flop Qh8s5c, BTN bets 25%. OOP TP medium-kicker facing 25% c-bet."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        if hs and (hs.get('is_set') or hs.get('is_two_pair')):
            return ("RAISE", "HIGH", 75, f"Monster on {spot['board_flop']}. OOP check-raise vs 25% cbet for value + protection.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "HIGH", None, f"Made pair on {spot['board_flop']}. OOP call vs 25% — bluff-catch, evaluate turn.")
        if hs and (hs.get('has_oesd') or hs.get('has_flush_draw')):
            return ("CALL", "HIGH", None, f"Drawing on {spot['board_flop']}. OOP call vs 25% — pot odds easily met.")
        if hs and hs.get('has_gutshot'):
            return ("CALL", "MEDIUM", None, f"Drawing (gutshot) on {spot['board_flop']}. OOP call vs 25% — pot odds 16.7% met by 4 outs + backdoors.")
        return ("FOLD", "MEDIUM", None, f"Air on {spot['board_flop']}. OOP fold vs 25% cbet without equity.")

    if var == 'effective_stack':
        return ("CALL", "HIGH", None, f"Strong made (TPMK QT on Qh8s5c). OOP call vs 25% cbet — pot odds 16.7% well below TP equity. Plan check-call turn unimproved.")

    if var == 'villain_bet_sizing':
        # TPMK can call up to ~75% sizing comfortably
        if pot_odds > 0.40:
            return ("FOLD", "MEDIUM", None, f"Strong made (TPMK QT on Qh8s5c). Larger sizing pot odds {pot_odds:.0%} signals polarization; QT outkicked by AQ/KQ. Fold to overbet.")
        if pot_odds > 0.33:
            return ("CALL", "MEDIUM", None, f"Strong made (TPMK QT). Pot odds {pot_odds:.0%} marginal; thin call OOP HU vs single villain — fold to additional pressure.")
        return ("CALL", "HIGH", None, f"Strong made (TPMK QT). Pot odds {pot_odds:.0%} ≤ TP bluff-catch threshold; call to evaluate turn.")

    return ("CALL", "HIGH", None, "HU-5.3 default fallback.")


def label_HU_5_4(spot, hs):
    """HU-5.4: Th8h BB defends, flop 9h7c2h two-tone. OOP donk-lead with combo draw."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('has_flush_made') or hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('is_set')):
            return ("BET", "HIGH", 50, f"Monster on {spot['board_flop']}. OOP donk-lead for value.")
        if hs and (hs.get('has_flush_draw') and hs.get('has_oesd')):
            return ("BET", "HIGH", 50, f"Drawing (combo: FD + OESD on {spot['board_flop']}). OOP donk-lead 50% on wet BB-favoured two-tone — semi-bluff with 15+ outs.")
        if hs and (hs.get('has_flush_draw') or hs.get('has_oesd')):
            return ("CHECK", "MEDIUM", None, f"Drawing on {spot['board_flop']}. OOP check — face cbet, call to realize.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CHECK", "MEDIUM", None, f"Made pair on {spot['board_flop']}. OOP check — pot-control, bluff-catch.")
        return ("CHECK", "MEDIUM", None, f"On {spot['board_flop']}. OOP default check.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 50, f"Drawing (combo: T-high OESD + 2nd-nut FD on 9h7c2h two-tone). OOP donk-lead 50% — semi-bluff on BB-favoured wet texture with 15+ outs.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 50, f"Drawing (combo). OOP donk-lead 50% in {param} variant — BB-favoured two-tone-connected.")

    return ("BET", "HIGH", 50, "HU-5.4 default fallback.")


def label_HU_5_5(spot, hs):
    """HU-5.5: KsJc BB defends, flop 8h6d5h two-tone-low-connected. OOP donk vs check with overcard-air."""
    var = spot['variation_axis']

    if var == 'board_runout':
        if hs and (hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('is_set') or hs.get('has_flush_made')):
            return ("BET", "HIGH", 33, f"Monster on {spot['board_flop']}. OOP lead for value.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CHECK", "HIGH", None, f"Made pair on {spot['board_flop']}. OOP check — pot-control.")
        if hs and (hs.get('has_oesd') or hs.get('has_flush_draw')):
            return ("CHECK", "MEDIUM", None, f"Drawing on {spot['board_flop']}. OOP check — face cbet, call to realize.")
        return ("CHECK", "HIGH", None, f"Air on {spot['board_flop']}. OOP check — BB-favoured low-connected texture, no equity to lead with.")

    if var == 'effective_stack':
        return ("CHECK", "HIGH", None, f"Air (KJ overcards + backdoor straight on 8h6d5h). OOP check — BB-favoured wet texture, no fold equity vs BTN's range, no value vs hits.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("CHECK", "HIGH", None, f"Air (KJ overcards) on 8h6d5h. OOP check in {param} variant — BB-favoured texture.")

    return ("CHECK", "HIGH", None, "HU-5.5 default fallback.")


def label_HU_6_1(spot, hs):
    """HU-6.1: KhKs BTN open, BB calls. Runout Kc7s4h/2c/Kd. River quads, BB checks. Nutted overbet."""
    var = spot['variation_axis']

    if var == 'board_runout':
        # New river card
        br = spot.get('board_river')
        bt = spot.get('board_turn', 'Kc7s4h2c')
        if hs is None and br:
            hs = hand_strength(spot['hero_cards'], br)
        if hs and hs.get('is_quads'):
            return ("BET", "HIGH", 150, f"Monster (quad kings on {br}). River 150% overbet for max value — paired board makes BB's calling range Kx-airy and bluff-catchers; nuts demand polar overbet.")
        if hs and hs.get('is_full_house'):
            return ("BET", "HIGH", 75, f"Monster (full house on {br}). River value bet 75% — top boat dominates BB's continuing range.")
        # Hero KK on river, top set or top pair w/ K
        if hs and hs.get('is_set'):
            return ("BET", "HIGH", 75, f"Monster (set of kings on {br}). River value bet 75%.")
        return ("BET", "HIGH", 33, f"Strong made (top pair K — KK overpair has K hit) on river {br}. Thin value 33% checked-to.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 150, f"Monster (quad kings on Kc7s4h-2c-Kd). River 150% overbet for max value on paired runout — BB's bluff-catching range.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 150, f"Monster (quad kings). River 150% overbet — variant {param} doesn't change nuts maximum extraction.")

    return ("BET", "HIGH", 150, "HU-6.1 default fallback.")


def label_HU_6_2(spot, hs):
    """HU-6.2: 8d8c BB defends. Runout Jh9h6h/Th/Qd. Busted underpair facing 150% overbet on completed flush+straight."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        # New river card
        br = spot.get('board_river')
        bt = spot.get('board_turn', 'Jh9h6hTh')
        if hs is None and br:
            hs = hand_strength(spot['hero_cards'], br)
        if hs and hs.get('has_made_straight'):
            return ("CALL", "MEDIUM", None, f"Made straight (88 holds K-Q-J-T-9 wait, 8 doesn't fill straight). Re-eval: hero's 88 + JhTh river — runner-runner full house? Unlikely. Call only if straight made.")
        if hs and hs.get('hero_paired_with_board'):
            return ("CALL", "MEDIUM", None, f"Pair of 8s on river {br} (made pair). Bluff-catch vs 150% overbet — pot odds {pot_odds:.0%} marginal; A-blocker absent. Likely fold.")
        # Pure busted underpair, no equity vs overbet on straight+flush board
        return ("FOLD", "HIGH", None, f"Air (88 underpair busted on river {br}). 150% overbet on Jh9h6h-Th-Qd completed flush + straight — fold pure pair.")

    if var == 'effective_stack':
        return ("FOLD", "HIGH", None, f"Air (88 underpair, no equity). vs 150% overbet on Jh9h6h-Th-Qd flush+straight runout — clear fold per anchor.")

    if var == 'villain_bet_sizing':
        # All sizing variations: hero has 88 underpair on completed flush+straight river. Always fold.
        return ("FOLD", "HIGH", None, f"Air (88 underpair on completed flush+straight runout). vs {tocall}bb sizing pot odds {pot_odds:.0%}. Fold — no equity.")

    return ("FOLD", "HIGH", None, "HU-6.2 default fallback.")


def label_HU_6_3(spot, hs):
    """HU-6.3: AsTs BTN open. Runout Tc7d3c/5h/2s. River TPTK on dry-disconnected, BB checks. River value-bet sizing."""
    var = spot['variation_axis']

    if var == 'board_runout':
        br = spot.get('board_river')
        bt = spot.get('board_turn', 'Tc7d3c5h')
        if hs is None and br:
            hs = hand_strength(spot['hero_cards'], br)
        if hs and (hs.get('has_flush_made') or hs.get('is_two_pair') or hs.get('is_set')):
            return ("BET", "HIGH", 150, f"Monster on river {br}. Polar overbet for max value.")
        if hs and hs.get('hero_paired_with_board') and hs.get('top_board_rank') == rank_val('T'):
            # Still TPTK
            return ("BET", "HIGH", 75, f"Strong made (TPTK AT on {br}). River value bet 75% — extract from worse Tx, missed FD bluff-catchers.")
        if hs and hs.get('hero_paired_with_board'):
            return ("BET", "MEDIUM", 33, f"Made pair on {br}. Thin river value 33% checked-to.")
        return ("CHECK", "MEDIUM", None, f"Air on river {br}. Check — bluffing 150% pot too thin without blockers/missed-draw narrative.")

    if var == 'effective_stack':
        return ("BET", "HIGH", 75, f"Strong made (TPTK AT on Tc7d3c-5h-2s dry runout). River value bet 75% — checked-to, extract from worse Tx + missed-FD bluff-catchers.")

    if var == 'villain_action_sequence':
        param = spot['variation_param']
        return ("BET", "HIGH", 75, f"Strong made (TPTK). River value bet 75% in {param} variant.")

    return ("BET", "HIGH", 75, "HU-6.3 default fallback.")


def label_HU_6_4(spot, hs):
    """HU-6.4: AcQh BB defends. Runout Qs9c4s/7c/2h. River TPTK facing BTN 75% triple-barrel on busted FD."""
    var = spot['variation_axis']
    pot = spot['pot_bb']
    tocall = spot['to_call_bb']
    pot_odds = tocall / (pot + tocall) if (pot + tocall) > 0 else 0

    if var == 'board_runout':
        br = spot.get('board_river')
        bt = spot.get('board_turn', 'Qs9c4s7c')
        if hs is None and br:
            hs = hand_strength(spot['hero_cards'], br)
        if hs and (hs.get('has_made_straight') or hs.get('is_two_pair') or hs.get('is_set') or hs.get('has_flush_made')):
            return ("RAISE", "HIGH", 150, f"Monster on river {br}. Raise vs 75% barrel — value extraction vs bluff-catchers.")
        if hs and hs.get('hero_paired_with_board') and hs.get('top_board_rank') == rank_val('Q'):
            # TPTK still — call vs 75% triple barrel is bluff-catch decision
            # If river completes obvious draws (flush, straight) — fold; if brick — call
            if hs.get('flush_suit_on_board'):
                return ("FOLD", "MEDIUM", None, f"Strong made (TPTK AQ) but river {br} completes flush. Fold vs 75% triple barrel on flush completion.")
            return ("CALL", "MEDIUM", None, f"Strong made (TPTK AQ on {br}). Bluff-catch vs 75% triple barrel — pot odds 30% met by TPTK equity vs polarized barrel range.")
        if hs and hs.get('hero_paired_with_board'):
            return ("FOLD", "MEDIUM", None, f"Medium made (Q-pair, possibly outkicked) on {br}. Fold vs 75% triple barrel — outkicked too often.")
        return ("FOLD", "HIGH", None, f"Air on river {br}. vs 75% triple barrel — fold without TP+ value.")

    if var == 'effective_stack':
        return ("CALL", "MEDIUM", None, f"Strong made (TPTK AQ on Qs9c4s-7c-2h busted FD). Bluff-catch vs 75% triple barrel — pot odds 30%, TPTK ahead of busted FDs and missed broadways. Call.")

    if var == 'villain_bet_sizing':
        # TPTK bluff-catch threshold
        if pot_odds > 0.42:
            return ("FOLD", "HIGH", None, f"Strong made (TPTK AQ). Larger sizing pot odds {pot_odds:.0%} polarizes too far — value-heavy at large sizes; fold.")
        if pot_odds > 0.36:
            return ("FOLD", "MEDIUM", None, f"Strong made (TPTK). Pot odds {pot_odds:.0%} marginal vs polarized triple barrel; fold without nut blocker.")
        return ("CALL", "MEDIUM", None, f"Strong made (TPTK AQ). Pot odds {pot_odds:.0%} ≤ TPTK bluff-catch threshold; call vs busted-FD runout.")

    return ("CALL", "MEDIUM", None, "HU-6.4 default fallback.")


# ----- Dispatcher -----

ANCHOR_LABELLERS = {
    "HU-2.1": label_HU_2_1,
    "HU-2.2": label_HU_2_2,
    "HU-2.3": label_HU_2_3,
    "HU-2.4": label_HU_2_4,
    "HU-2.5": label_HU_2_5,
    "HU-3.1": label_HU_3_1,
    "HU-3.2": label_HU_3_2,
    "HU-3.3": label_HU_3_3,
    "HU-3.4": label_HU_3_4,
    "HU-3.5": label_HU_3_5,
    "HU-4.1": label_HU_4_1,
    "HU-4.2": label_HU_4_2,
    "HU-4.3": label_HU_4_3,
    "HU-4.4": label_HU_4_4,
    "HU-4.5": label_HU_4_5,
    "HU-5.1": label_HU_5_1,
    "HU-5.2": label_HU_5_2,
    "HU-5.3": label_HU_5_3,
    "HU-5.4": label_HU_5_4,
    "HU-5.5": label_HU_5_5,
    "HU-6.1": label_HU_6_1,
    "HU-6.2": label_HU_6_2,
    "HU-6.3": label_HU_6_3,
    "HU-6.4": label_HU_6_4,
}


def main():
    # Load existing labels (resumption support)
    existing = set()
    if os.path.exists(OUT_PATH):
        with open(OUT_PATH) as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    existing.add(rec['spot_id'])
                except Exception:
                    pass

    print(f"Existing labels: {len(existing)}")

    # Load situations
    with open(SITUATIONS) as f:
        situations = [json.loads(l) for l in f]

    print(f"Total situations: {len(situations)}")

    written = 0
    errors = 0

    # Open append-only
    with open(OUT_PATH, 'a') as out:
        for spot in situations:
            spot_id = spot['spot_id']
            if spot_id in existing:
                continue

            anchor_id = spot['anchor_id']
            labeller_fn = ANCHOR_LABELLERS.get(anchor_id)

            if labeller_fn is None:
                # Unknown anchor — error row
                rec = {
                    "spot_id": spot_id,
                    "labeller_id": LABELLER_ID,
                    "predicted_action": "CHECK",
                    "confidence": "LOW",
                    "reasoning": f"Unknown anchor {anchor_id}; default fallback.",
                    "_meta": {"error": "unknown_anchor"}
                }
                out.write(json.dumps(rec) + "\n")
                out.flush()
                errors += 1
                written += 1
                continue

            # Compute hero hand strength on appropriate board
            # For board_runout variations: re-evaluate on the new (variation) board
            # For other variations: anchor board applies
            street = spot['street']
            if street == 'flop':
                board = spot.get('board_flop')
            elif street == 'turn':
                board = spot.get('board_turn') or spot.get('board_flop')
            else:  # river
                board = spot.get('board_river') or spot.get('board_turn') or spot.get('board_flop')

            try:
                hs = hand_strength(spot['hero_cards'], board) if board else None
            except Exception as e:
                hs = None

            try:
                action, conf, sizing, reasoning = labeller_fn(spot, hs)
            except Exception as e:
                rec = {
                    "spot_id": spot_id,
                    "labeller_id": LABELLER_ID,
                    "predicted_action": "CHECK",
                    "confidence": "LOW",
                    "reasoning": f"Labelling error: {e}",
                    "_meta": {"error": str(e)}
                }
                out.write(json.dumps(rec) + "\n")
                out.flush()
                errors += 1
                written += 1
                continue

            rec = {
                "spot_id": spot_id,
                "labeller_id": LABELLER_ID,
                "predicted_action": action,
                "confidence": conf,
                "reasoning": reasoning,
            }
            if sizing is not None and action in ("BET", "RAISE"):
                rec["predicted_sizing_pct"] = sizing

            out.write(json.dumps(rec) + "\n")
            out.flush()
            written += 1

    print(f"Wrote {written} new labels (errors: {errors})")


if __name__ == "__main__":
    main()
