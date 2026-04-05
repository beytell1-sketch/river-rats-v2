"""
play.py — River Rats Interactive Poker Coach

Terminal-based poker coaching tester. Loads real hands from the test CSV,
shows the situation, asks what you would do, then reveals the GTO coaching.

Usage:
    python3 play.py
    python3 play.py --hands 30   (play 30 hands)
    python3 play.py --no-color   (disable ANSI color)

Controls:
    f / fold     → FOLD
    ch / check   → CHECK
    ca / call     → CALL
    b / bet       → BET
    r / raise     → RAISE
    a             → show ALL levels for this hand (after answering)
    L             → change level between hands
    q             → quit and see final summary
"""

import sys
import os
import csv
import random
import argparse
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# Ensure the coaching package is importable from cwd
sys.path.insert(0, '.')

from coaching.explain_hand import ExplainEngine
from coaching.levels import PlayerLevel
from coaching.hand_context import (
    build_hand_context, STREET_NAMES_CAP, CATEGORY_DESCRIPTIONS,
)
from coaching.gto_model import FEATURE_COLUMNS


# ═══════════════════════════════════════════════════════════════════
# ANSI COLOR SUPPORT
# ═══════════════════════════════════════════════════════════════════

def _supports_color() -> bool:
    """Check if the terminal likely supports ANSI color codes."""
    if not hasattr(sys.stdout, 'isatty'):
        return False
    if not sys.stdout.isatty():
        return False
    term = os.environ.get('TERM', '')
    if term == 'dumb':
        return False
    return True


class Colors:
    """ANSI color codes — degrade gracefully if not supported."""
    _enabled = True

    @classmethod
    def disable(cls):
        cls._enabled = False

    @classmethod
    def _c(cls, code: str, text: str) -> str:
        if cls._enabled:
            return f"\033[{code}m{text}\033[0m"
        return text

    @classmethod
    def green(cls, t): return cls._c("32", t)
    @classmethod
    def red(cls, t): return cls._c("31", t)
    @classmethod
    def yellow(cls, t): return cls._c("33", t)
    @classmethod
    def cyan(cls, t): return cls._c("36", t)
    @classmethod
    def bold(cls, t): return cls._c("1", t)
    @classmethod
    def dim(cls, t): return cls._c("2", t)


# ═══════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "training_data_37feat (Copy 1)", "test_action_37.csv"
)

# Simpler hand category names for display (the spec uses a simplified 0-8 mapping
# but the CSV uses the richer 17-category system from hand_context.py)
SIMPLE_HAND_NAMES = {
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

STREET_DISPLAY = {0.0: "Flop", 1.0: "Turn", 2.0: "River"}

BOARD_TEXTURE_NAMES = {
    "is_monotone": "monotone (all one suit)",
    "is_paired":   "paired board",
}

# Rank names for card display — high_card_rank is stored as 2-14 in the CSV
RANK_NAMES = {
    14: 'Ace', 13: 'King', 12: 'Queen', 11: 'Jack', 10: 'Ten',
    9: 'Nine', 8: 'Eight', 7: 'Seven', 6: 'Six', 5: 'Five',
    4: 'Four', 3: 'Three', 2: 'Two',
}

# Position seat names
POS_NAMES = {0: 'UTG', 1: 'HJ', 2: 'CO', 3: 'BTN', 4: 'SB', 5: 'BB'}


def _describe_hero_hand(feat_dict: Dict[str, float]) -> str:
    """
    Build a human-readable hero hand description from numeric features.

    hand_category uses the 17-level system (SIMPLE_HAND_NAMES above).
    hand_rank is a continuous value; for pairs (cat 3-9) it encodes
    pair quality as ~1.0 (bottom) through ~2.9 (top pair top kicker).
    """
    cat = feat_dict.get('hand_category', 0.0)
    hand_rank = feat_dict.get('hand_rank', 0.0)
    high = int(feat_dict.get('high_card_rank', 0))
    high_name = RANK_NAMES.get(high, str(high) if high else '?')

    has_fd = feat_dict.get('has_flush_draw', 0) > 0.5
    has_sd = feat_dict.get('has_straight_draw', 0) > 0.5
    outs = int(feat_dict.get('draw_outs', 0))

    # Derive base hand name from the 17-category system
    # For pair hands (cat 3-9) we can add more colour using hand_rank
    if cat >= 17:
        hand = "a straight flush"
    elif cat >= 16:
        hand = f"quad {high_name}s"
    elif cat >= 15:
        hand = "a full house"
    elif cat >= 14:
        hand = f"{high_name}-high flush"
    elif cat >= 13:
        hand = f"{high_name}-high straight"
    elif cat >= 12:
        hand = "a set"
    elif cat >= 11:
        hand = "trips"
    elif cat >= 10:
        hand = "two pair"
    elif cat >= 9:
        hand = "an overpair"
    elif cat >= 8:
        hand = f"top pair, top kicker ({high_name}s)"
    elif cat >= 7:
        hand = f"top pair, good kicker ({high_name}s)"
    elif cat >= 6:
        hand = f"top pair ({high_name}s)"
    elif cat >= 5:
        hand = "middle pair"
    elif cat >= 4:
        hand = "an underpair"
    elif cat >= 3:
        hand = "bottom pair"
    elif cat >= 2:
        hand = f"{high_name}-high (two overcards)"
    elif cat >= 1:
        hand = f"{high_name}-high (one overcard)"
    else:
        hand = f"{high_name} high"

    # Draw suffix
    draw = ""
    if has_fd and has_sd:
        draw = f" + combo draw ({outs} outs)"
    elif has_fd:
        draw = f" + flush draw ({outs} outs)"
    elif has_sd:
        draw = f" + straight draw ({outs} outs)"
    elif outs > 0:
        draw = f" + {outs} outs to improve"

    return hand + draw


def _describe_board(feat_dict: Dict[str, float]) -> str:
    """Build a human-readable board texture description from numeric features."""
    high = int(feat_dict.get('high_card_rank', 0))
    high_name = RANK_NAMES.get(high, str(high) if high else '?')
    danger = feat_dict.get('danger_score', 0.0)
    connectivity = feat_dict.get('connectivity_score', 0.0)
    is_mono = feat_dict.get('is_monotone', 0) > 0.5
    is_two_tone = feat_dict.get('is_two_tone', 0) > 0.5
    is_paired = feat_dict.get('is_paired', 0) > 0.5

    parts = [f"{high_name}-high"]

    # Suit texture
    if is_mono:
        parts.append("monotone")
    elif is_two_tone:
        parts.append("two-suited")
    else:
        parts.append("rainbow")

    # Pairing
    if is_paired:
        parts.append("paired")

    # Connectivity
    if connectivity > 1.5:
        parts.append("very connected")
    elif connectivity > 0.6:
        parts.append("connected")
    elif connectivity < 0.2:
        parts.append("dry")

    # Overall danger
    if danger > 0.7:
        parts.append(Colors.red("(dangerous)"))
    elif danger < 0.25:
        parts.append(Colors.dim("(safe)"))

    return ", ".join(parts)


def load_hands(csv_path: str, n: int = 200, seed: int = 42) -> List[Dict[str, float]]:
    """
    Load up to n random hands from the CSV.

    Handles both 'action_label' and 'action' column names.
    Returns list of feat_dicts with 'gto_label' key added.
    """
    rows = []
    abs_path = os.path.realpath(csv_path)

    try:
        with open(abs_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"ERROR: CSV not found at {abs_path}")
        sys.exit(1)

    if not rows:
        print("ERROR: CSV is empty.")
        sys.exit(1)

    # Reproducible shuffle then sample
    rng = random.Random(seed)
    rng.shuffle(rows)
    selected = rows[:n]

    hands = []
    for row in selected:
        # Determine label column
        if 'action_label' in row:
            label = row['action_label'].strip().upper()
        elif 'action' in row:
            label = row['action'].strip().upper()
        else:
            label = 'UNKNOWN'

        feat_dict: Dict[str, float] = {}
        for col in FEATURE_COLUMNS:
            try:
                feat_dict[col] = float(row[col])
            except (KeyError, ValueError):
                feat_dict[col] = 0.0

        feat_dict['_gto_label'] = label
        hands.append(feat_dict)

    return hands


# ═══════════════════════════════════════════════════════════════════
# HAND DISPLAY
# ═══════════════════════════════════════════════════════════════════

def describe_hand(feat_dict: Dict[str, float], level: int) -> str:
    """
    Build a poker-narrative description of the hand situation.
    Tells a story a player would recognize at the table.
    Equity is hidden for L1-L3, shown for L4-L5 per spec.
    """
    lines = []

    # --- Extract all features ---
    street_val = feat_dict.get('street', 0.0)
    street_name = STREET_DISPLAY.get(street_val, "Flop")
    is_ip = feat_dict.get('is_ip', 0) > 0.5
    spr = feat_dict.get('spr', 0.0)
    pot = feat_dict.get('pot_size', 0.0)
    to_call = feat_dict.get('to_call', 0.0)
    facing_bet = feat_dict.get('facing_bet', 0) > 0.5
    is_3bet = feat_dict.get('is_3bet_pot', 0) > 0.5
    hand_cat = feat_dict.get('hand_category', 0.0)
    hand_rank = feat_dict.get('hand_rank', 0.0)
    is_made = feat_dict.get('is_made_hand', 0) > 0.5
    is_strong = feat_dict.get('is_strong_made', 0) > 0.5
    is_monster = feat_dict.get('is_monster', 0) > 0.5
    has_fd = feat_dict.get('has_flush_draw', 0) > 0.5
    has_sd = feat_dict.get('has_straight_draw', 0) > 0.5
    draw_outs = feat_dict.get('draw_outs', 0.0)
    danger = feat_dict.get('danger_score', 0.0)
    is_mono = feat_dict.get('is_monotone', 0) > 0.5
    is_paired = feat_dict.get('is_paired', 0) > 0.5
    connectivity = feat_dict.get('connectivity_score', 0.0)
    v_agg = feat_dict.get('villain_aggression_count', 0)
    v_check = feat_dict.get('villain_checked_back', 0) > 0.5
    v_calls = feat_dict.get('villain_call_count', 0)

    # --- Build the story ---
    # Pot type
    pot_type = "3-bet pot" if is_3bet else "single-raised pot"

    # Hero hand and board — human-readable from numeric features
    hero_desc = _describe_hero_hand(feat_dict)
    board_desc = _describe_board(feat_dict)

    # Add strength qualifier to hero hand
    if is_monster:
        hero_desc = Colors.green(hero_desc + " (monster!)")
    elif is_strong:
        hero_desc = Colors.green(hero_desc + " (strong)")

    # Villain story
    villain_desc = ""
    if v_agg >= 2:
        villain_desc = "  Villain has been " + Colors.red("aggressive on multiple streets") + "."
    elif v_check:
        villain_desc = "  Villain checked on a previous street (showed weakness)."
    elif v_calls >= 2:
        villain_desc = "  Villain has been calling passively on multiple streets."

    # Stack depth description
    if spr < 2:
        stack_desc = Colors.red(f"shallow (SPR {spr:.1f} -- near commitment)")
    elif spr < 6:
        stack_desc = f"moderate (SPR {spr:.1f})"
    else:
        stack_desc = f"deep (SPR {spr:.1f})"

    # Position description with seat names
    hero_pos = POS_NAMES.get(int(feat_dict.get('hero_position', 0)), '?')
    villain_pos = POS_NAMES.get(int(feat_dict.get('villain_position', 0)), '?')
    pos_str = (
        f"You ({hero_pos}) vs Villain ({villain_pos}) — "
        f"{'you act last' if is_ip else 'you act first'}"
    )

    # --- Compose output ---
    lines.append("")
    lines.append(f"  {Colors.bold(street_name)} | {pot_type} | Stacks: {stack_desc}")
    lines.append(f"  Position: {pos_str}")
    lines.append(f"  Pot: {pot:.0f} chips")
    lines.append("")
    lines.append(f"  You hold: {Colors.bold(hero_desc)}")
    lines.append(f"  Board:    {board_desc}")

    if facing_bet:
        pot_odds = feat_dict.get('pot_odds', 0.0)
        lines.append("")
        lines.append(f"  >> Villain bets {to_call:.0f} into a {pot:.0f} chip pot (you need {pot_odds*100:.0f}% equity to call)")
    else:
        lines.append("")
        lines.append("  Action is on you. No bet to face.")

    if villain_desc:
        lines.append(villain_desc)

    # Equity -- only at L4+
    if level >= 4:
        equity = feat_dict.get('equity_vs_range', feat_dict.get('raw_equity', 0.0))
        margin = feat_dict.get('equity_margin', 0.0)
        lines.append(f"  {Colors.cyan(f'Your equity: {equity*100:.0f}%')} (margin: {margin*100:+.0f}%)")

    lines.append("")
    return "\n".join(lines)


def _nearest_hand_name(cat_val: float) -> str:
    """Return hand name for nearest category key."""
    if cat_val in SIMPLE_HAND_NAMES:
        return SIMPLE_HAND_NAMES[cat_val]
    best_key = min(SIMPLE_HAND_NAMES.keys(), key=lambda k: abs(k - cat_val))
    if abs(best_key - cat_val) < 0.6:
        return SIMPLE_HAND_NAMES[best_key]
    return "your hand"


# ═══════════════════════════════════════════════════════════════════
# INPUT HANDLING
# ═══════════════════════════════════════════════════════════════════

ACTION_INPUT_MAP = {
    'f':    'FOLD',
    'fold': 'FOLD',
    'ch':   'CHECK',
    'check':'CHECK',
    'ca':   'CALL',
    'call': 'CALL',
    'b':    'BET',
    'bet':  'BET',
    'r':    'RAISE',
    'raise':'RAISE',
}

LEVEL_TO_ENUM = {
    1: PlayerLevel.L1_PERCEPTION,
    2: PlayerLevel.L2_CAUSE_EFFECT,
    3: PlayerLevel.L3_ARCHITECTURE,
    4: PlayerLevel.L4_MEASUREMENT,
    5: PlayerLevel.L5_SYSTEMS,
}

LEVEL_NAMES = {
    1: "L1 — Perception (beginner)",
    2: "L2 — Cause & Effect",
    3: "L3 — Architecture",
    4: "L4 — Measurement",
    5: "L5 — Systems (advanced)",
}


def prompt_level() -> int:
    """Prompt user to choose a coaching level (1-5). Returns int."""
    print()
    print(Colors.bold("Coaching levels:"))
    for n, name in LEVEL_NAMES.items():
        print(f"  {n}: {name}")
    print()
    while True:
        raw = input(Colors.bold("Choose your level (1-5): ")).strip()
        if raw in ('q', 'quit'):
            return -1
        try:
            level = int(raw)
            if 1 <= level <= 5:
                return level
        except ValueError:
            pass
        print("  Please enter a number between 1 and 5.")


def prompt_action(facing_bet: bool) -> str:
    """
    Prompt for action. Returns action string, 'q', 'L', or 'skip'.
    """
    if facing_bet:
        options = "(f)old / (ca)ll / (r)aise"
    else:
        options = "(f)old / (ch)eck / (b)et"

    while True:
        raw = input(f"\n  What do you do? {options} : ").strip().lower()
        if raw == 'q':
            return 'q'
        if raw == 'l':
            return 'L'
        if raw in ACTION_INPUT_MAP:
            action = ACTION_INPUT_MAP[raw]
            # Basic sanity: if facing bet, can't check/bet; if not, can't call/raise
            # (We allow it but it will just be counted as wrong vs GTO)
            return action
        print("  Unrecognised input. Try: f, ch, ca, b, r — or q to quit, L to change level.")


def prompt_continue() -> str:
    """Prompt between hands. Returns 'next', 'q', 'L', or 'all'."""
    raw = input(
        Colors.dim("\n[Enter] next hand  |  q = quit  |  L = change level  |  a = all levels: ")
    ).strip().lower()
    if raw == 'q':
        return 'q'
    if raw == 'l':
        return 'L'
    if raw == 'a':
        return 'all'
    return 'next'


# ═══════════════════════════════════════════════════════════════════
# COACHING DISPLAY
# ═══════════════════════════════════════════════════════════════════

def display_explanation(explanation, action: str, confidence: float, label_prefix: str = ""):
    """Print a formatted coaching explanation."""
    conf_pct = f"{confidence*100:.0f}%"
    action_str = Colors.bold(Colors.cyan(action))
    print(f"\n  {label_prefix}GTO says: {action_str}  ({conf_pct} confidence)")

    if hasattr(explanation, 'headline') and explanation.headline:
        print(f"  \"{explanation.headline}\"")
    if hasattr(explanation, 'supporting') and explanation.supporting:
        for line in explanation.supporting:
            if line:
                print(f"  \"{line}\"")
    if hasattr(explanation, 'qualifier') and explanation.qualifier:
        print(f"  {Colors.dim('Note: ' + explanation.qualifier)}")


def display_all_levels(engine: ExplainEngine, feat_dict: Dict[str, float]):
    """Show explanations for all 5 levels for the current hand."""
    print(f"\n  {Colors.bold('--- All Levels ---')}")
    try:
        all_exp = engine.explain_from_features_all_levels(feat_dict)
        for level_key in ('L1', 'L2', 'L3', 'L4', 'L5'):
            exp = all_exp.get(level_key)
            if exp is None:
                continue
            level_num = int(level_key[1])
            level_name = LEVEL_NAMES.get(level_num, level_key)
            print(f"\n  {Colors.bold(Colors.yellow(level_name))}")
            if hasattr(exp, 'headline') and exp.headline:
                print(f"    \"{exp.headline}\"")
            if hasattr(exp, 'supporting') and exp.supporting:
                for line in exp.supporting:
                    if line:
                        print(f"    \"{line}\"")
    except Exception as e:
        print(f"  (Could not generate all-levels view: {e})")


# ═══════════════════════════════════════════════════════════════════
# SCORING & SUMMARY
# ═══════════════════════════════════════════════════════════════════

class ScoreTracker:
    """Tracks session score and mistake patterns."""

    def __init__(self):
        self.total = 0
        self.correct = 0
        # mistakes[gto_action][user_action] = count
        self.mistakes: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.level_correct: Dict[int, int] = defaultdict(int)
        self.level_total: Dict[int, int] = defaultdict(int)

    def record(self, gto_action: str, user_action: str, level: int):
        agreed = gto_action == user_action
        self.total += 1
        self.level_total[level] += 1
        if agreed:
            self.correct += 1
            self.level_correct[level] += 1
        else:
            self.mistakes[gto_action][user_action] += 1
        return agreed

    @property
    def accuracy(self) -> float:
        return self.correct / self.total if self.total > 0 else 0.0

    def score_line(self) -> str:
        pct = f"{self.accuracy*100:.0f}%"
        color = Colors.green if self.accuracy >= 0.6 else Colors.yellow if self.accuracy >= 0.4 else Colors.red
        return f"Score: {self.correct}/{self.total}  ({color(pct)})"

    def summary(self):
        print()
        print(Colors.bold("=" * 50))
        print(Colors.bold("  FINAL SUMMARY"))
        print(Colors.bold("=" * 50))
        print(f"  Hands played : {self.total}")
        print(f"  Correct      : {self.correct}")
        acc_str = f"{self.accuracy*100:.1f}%"
        color_fn = Colors.green if self.accuracy >= 0.6 else Colors.yellow if self.accuracy >= 0.4 else Colors.red
        print(f"  Accuracy     : {color_fn(Colors.bold(acc_str))}")

        if self.level_total:
            print()
            print("  By level:")
            for lvl in sorted(self.level_total.keys()):
                tot = self.level_total[lvl]
                cor = self.level_correct[lvl]
                pct = cor / tot if tot > 0 else 0
                bar = "#" * int(pct * 10) + "-" * (10 - int(pct * 10))
                print(f"    L{lvl}: {cor}/{tot}  [{bar}]  {pct*100:.0f}%")

        if self.mistakes:
            print()
            print("  Most common mistakes:")
            # Flatten and sort by count
            all_mistakes = []
            for gto, user_map in self.mistakes.items():
                for user, count in user_map.items():
                    all_mistakes.append((count, gto, user))
            all_mistakes.sort(reverse=True)
            for count, gto, user in all_mistakes[:5]:
                print(f"    GTO said {Colors.cyan(gto)}, you said {Colors.red(user)}: {count}x")

        print()
        if self.accuracy >= 0.7:
            print(Colors.green("  Great session! Your instincts are aligning with GTO."))
        elif self.accuracy >= 0.5:
            print(Colors.yellow("  Solid work. Keep studying the spots you missed."))
        else:
            print(Colors.red("  Keep at it — review the coaching for missed spots."))
        print()


# ═══════════════════════════════════════════════════════════════════
# MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════════

def run(num_hands: int = 20, use_color: bool = True):
    """Main entry point for the coaching session."""

    if not use_color or not _supports_color():
        Colors.disable()

    print()
    print(Colors.bold(Colors.cyan("=" * 50)))
    print(Colors.bold(Colors.cyan("     RIVER RATS POKER COACH")))
    print(Colors.bold(Colors.cyan("=" * 50)))
    print()
    print("  Loading hands and models...")

    # Load model engine
    model_path = os.path.join(os.path.dirname(__file__), "gto_model_v3.json")
    sizing_path = os.path.join(os.path.dirname(__file__), "raise_sizing_model.json")

    try:
        engine = ExplainEngine(
            model_path=model_path,
            sizing_model_path=sizing_path if os.path.exists(sizing_path) else None,
        )
    except Exception as e:
        print(f"ERROR loading model: {e}")
        sys.exit(1)

    # Load hands
    hands = load_hands(CSV_PATH, n=200)
    if not hands:
        print("No hands loaded. Exiting.")
        sys.exit(1)

    print(f"  Loaded {len(hands)} hands from test set.")
    print()

    # Get initial level
    level = prompt_level()
    if level == -1:
        print("Goodbye.")
        return

    score = ScoreTracker()
    hand_idx = 0
    total_hands = min(num_hands, len(hands))

    while hand_idx < total_hands:
        feat_dict = hands[hand_idx]
        gto_label = feat_dict.get('_gto_label', 'UNKNOWN')

        print()
        print(Colors.bold(f"--- Hand {hand_idx + 1} of {total_hands} ---"))

        # Describe situation
        print(describe_hand(feat_dict, level))

        # Get oracle prediction (this is what we coach toward)
        try:
            player_level_enum = LEVEL_TO_ENUM[level]
            explanation = engine.explain_from_features(feat_dict, player_level_enum)
            gto_action = explanation.action
            gto_confidence = explanation.confidence
        except Exception as e:
            print(f"  (Engine error for this hand: {e})")
            hand_idx += 1
            continue

        # Get user action
        facing_bet = feat_dict.get('facing_bet', 0) > 0.5
        user_input = prompt_action(facing_bet)

        if user_input == 'q':
            break
        if user_input == 'L':
            new_level = prompt_level()
            if new_level == -1:
                break
            level = new_level
            # Re-do the same hand with new level
            continue

        user_action = user_input

        # Record score
        agreed = score.record(gto_action, user_action, level)

        # Show coaching
        display_explanation(explanation, gto_action, gto_confidence)

        # Agreement feedback
        print()
        if agreed:
            print(Colors.bold(Colors.green(f"  You agreed with GTO! ({user_action})")))
        else:
            print(Colors.bold(Colors.red(f"  You said {user_action}, GTO says {gto_action}.")))

        # CSV label note (informational — the CSV label may differ from oracle in edge cases)
        if gto_label != 'UNKNOWN' and gto_label != gto_action:
            print(Colors.dim(f"  (Historical label from dataset: {gto_label})"))

        print(f"\n  {score.score_line()}")

        # Between-hand navigation
        nav = prompt_continue()
        if nav == 'q':
            break
        if nav == 'L':
            new_level = prompt_level()
            if new_level == -1:
                break
            level = new_level
        elif nav == 'all':
            display_all_levels(engine, feat_dict)

        hand_idx += 1

    score.summary()


def main():
    parser = argparse.ArgumentParser(
        description="River Rats Interactive Poker Coach"
    )
    parser.add_argument(
        '--hands', type=int, default=20,
        help="Number of hands to play (default: 20)"
    )
    parser.add_argument(
        '--no-color', action='store_true',
        help="Disable ANSI color output"
    )
    args = parser.parse_args()

    run(num_hands=args.hands, use_color=not args.no_color)


if __name__ == '__main__':
    main()
