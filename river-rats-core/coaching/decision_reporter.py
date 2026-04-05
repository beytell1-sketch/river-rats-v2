"""
DecisionReporter — states what GTO does and how confident the decision is.

Computes the top-two-gap tightness signal and optionally provides a causal
bridge for structurally clear spots at L3+.

Architecture:
    OraclePrediction + HandContext + PlayerLevel
        → DecisionReport (action_statement, tightness, causal_bridge, ...)

Layer: Teaching (sits above Oracle, reads HandContext from foundation layer).
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from coaching.levels import PlayerLevel, level_gte
from coaching.hand_context import HandContext

if TYPE_CHECKING:
    # Avoid circular import at runtime; OraclePrediction is duck-typed at call site.
    from coaching.gto_model import OraclePrediction


# ═══════════════════════════════════════════════════════════════════
# TIGHTNESS CONSTANTS
# ═══════════════════════════════════════════════════════════════════

_TOSS_UP_THRESHOLD = 0.20   # gap < this → TOSS_UP
_CLOSE_THRESHOLD   = 0.35   # gap < this → CLOSE  (else → SILENCE)


# ═══════════════════════════════════════════════════════════════════
# OUTPUT DATACLASS
# ═══════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class DecisionReport:
    """
    Complete decision report for one hand at one player level.

    action_statement:   "GTO bets here." — level-gated phrasing.
    tightness:          "TOSS_UP", "CLOSE", or "SILENCE".
    tightness_sentence: None for SILENCE; short human phrase otherwise.
    causal_bridge:      Structural one-liner, fires only at L3+ / SILENCE / condition met.
    is_mixed:           True when gap < 0.20 (TOSS-UP territory).
    gap:                Probability gap between the top two actions (0.0-1.0).
    """
    action_statement: str
    tightness: str
    tightness_sentence: Optional[str]
    causal_bridge: Optional[str]
    is_mixed: bool
    gap: float


# ═══════════════════════════════════════════════════════════════════
# REPORTER
# ═══════════════════════════════════════════════════════════════════

class DecisionReporter:
    """
    Produces a DecisionReport from an oracle prediction, feature dict,
    hand context, and player level.

    No state; safe for reuse across hands.
    """

    def report(
        self,
        pred: "OraclePrediction",
        feat_dict: dict,
        ctx: HandContext,
        level: PlayerLevel,
        effective_action: Optional[str] = None,
    ) -> DecisionReport:
        """
        Build a DecisionReport for a single decision point.

        Args:
            pred:             OraclePrediction from GtoOracle (action, confidence, probs).
            feat_dict:        Raw feature dict — passed through; not reused internally.
            ctx:              HandContext for this hand (built from feat_dict upstream).
            level:            Player level gate for statement verbosity and bridge eligibility.
            effective_action: Final action after multiway adjustment (overrides pred.action
                              for the headline when the adjuster changed the action).

        Returns:
            Frozen DecisionReport.
        """
        gap = _compute_gap(pred)
        tightness, is_mixed = _classify_tightness(gap)
        action_statement = _build_action_statement(pred, level, tightness,
                                                   effective_action=effective_action)
        tightness_sentence = _build_tightness_sentence(tightness)
        causal_bridge = _build_causal_bridge(pred, ctx, level, gap, tightness)

        return DecisionReport(
            action_statement=action_statement,
            tightness=tightness,
            tightness_sentence=tightness_sentence,
            causal_bridge=causal_bridge,
            is_mixed=is_mixed,
            gap=gap,
        )


# ═══════════════════════════════════════════════════════════════════
# GAP COMPUTATION
# ═══════════════════════════════════════════════════════════════════

def _compute_gap(pred: "OraclePrediction") -> float:
    """
    Top-two-gap: difference between the highest and second-highest action probabilities.

    With five action classes, there will always be at least two values.
    """
    sorted_probs = sorted(pred.probs.values(), reverse=True)
    return sorted_probs[0] - sorted_probs[1]


# ═══════════════════════════════════════════════════════════════════
# TIGHTNESS CLASSIFICATION
# ═══════════════════════════════════════════════════════════════════

def _classify_tightness(gap: float) -> tuple:
    """
    Return (tightness_string, is_mixed) for the given gap value.

    Bands:
        gap < 0.20  → TOSS_UP, mixed=True
        0.20-0.49   → CLOSE,   mixed=False
        >= 0.50     → SILENCE, mixed=False
    """
    if gap < _TOSS_UP_THRESHOLD:
        return "TOSS_UP", True
    if gap < _CLOSE_THRESHOLD:
        return "CLOSE", False
    return "SILENCE", False


# ═══════════════════════════════════════════════════════════════════
# ACTION STATEMENT
# ═══════════════════════════════════════════════════════════════════

def _build_action_statement(
    pred: "OraclePrediction",
    level: PlayerLevel,
    tightness: str,
    effective_action: Optional[str] = None,
) -> str:
    """
    Produce the level-gated action statement.

    Templates by level:
        L1-L2:  "GTO {action}s here."
        L3:     "GTO {action}s here -- this is the higher-frequency action."
                  → TOSS-UP override: "GTO {action}s here -- both actions are in the mix."
        L4:     "GTO {action}s here -- {confidence_pct}% confidence."
                  → TOSS-UP override: same mix suffix
        L5:     "GTO {action}s at {confidence_pct}% frequency in this construction."
                  → TOSS-UP override: same mix suffix

    Note on grammar: we conjugate action verbs in third-person singular ("checks",
    "bets", etc.). "fold" → "folds", "raise" → "raises", "call" → "calls".
    All standard English -s suffix rules apply.

    Args:
        effective_action: When provided (e.g. after multiway adjustment), the headline
                          uses this action string rather than pred.action. Confidence
                          figures still come from the oracle prediction.
    """
    # Use effective_action for the headline verb when the adjuster changed the action.
    action = (effective_action if effective_action is not None else pred.action).lower()
    confidence_pct = round(pred.confidence * 100)

    # L3+ TOSS-UP override suffix
    mix_suffix = "-- both actions are in the mix."
    is_toss_up = tightness == "TOSS_UP"
    at_l3_plus = level_gte(level, PlayerLevel.L3_ARCHITECTURE)

    if level in (PlayerLevel.L1_PERCEPTION, PlayerLevel.L2_CAUSE_EFFECT):
        return f"GTO {action}s here."

    if level == PlayerLevel.L3_ARCHITECTURE:
        if is_toss_up:
            return f"GTO {action}s here {mix_suffix}"
        return f"GTO {action}s here -- this is the higher-frequency action."

    if level == PlayerLevel.L4_MEASUREMENT:
        if is_toss_up:
            return f"GTO {action}s here {mix_suffix}"
        return f"GTO {action}s here -- {confidence_pct}% confidence."

    # L5_SYSTEMS
    if is_toss_up:
        return f"GTO {action}s here {mix_suffix}"
    return f"GTO {action}s at {confidence_pct}% frequency in this construction."


# ═══════════════════════════════════════════════════════════════════
# TIGHTNESS SENTENCE
# ═══════════════════════════════════════════════════════════════════

def _build_tightness_sentence(tightness: str) -> Optional[str]:
    """
    Short qualitative sentence describing decision tightness.

    SILENCE returns None — no sentence needed when the decision is clear.
    """
    if tightness == "TOSS_UP":
        return "Both actions are reasonable here."
    if tightness == "CLOSE":
        return "The other action is also reasonable here."
    return None  # SILENCE


# ═══════════════════════════════════════════════════════════════════
# CAUSAL BRIDGE
# ═══════════════════════════════════════════════════════════════════

def _build_causal_bridge(
    pred: "OraclePrediction",
    ctx: HandContext,
    level: PlayerLevel,
    gap: float,
    tightness: str,
) -> Optional[str]:
    """
    Optional one-liner explaining WHY the decision is structurally clear.

    Gate conditions (ALL three must hold):
        1. gap >= 0.50  (SILENCE band — decision is unambiguous)
        2. level >= L3  (player can handle structural reasoning)
        3. At least one structural condition is met (checked in priority order)

    Structural conditions (priority order, first match wins):
        1. Pot odds mismatch    — equity vs. correct pot odds diverges by >10 pp
        2. SPR extreme          — SPR < 2.5 (commitment) or > 12.0 (deep)
        3. Draw quality         — meaningful draw equity present

    Returns None if no condition fires.
    """
    # Gate 1: only fires in the SILENCE band
    if tightness != "SILENCE":
        return None

    # Gate 2: level must be L3+
    if not level_gte(level, PlayerLevel.L3_ARCHITECTURE):
        return None

    # Gate 3: check structural conditions in priority order

    # --- Value targeting bridge (L5, requires range_breakdown) ---
    # Only fire value targeting when action is BET, RAISE, or CALL — not FOLD/CHECK
    action = pred.action.upper() if hasattr(pred, 'action') else ''
    if level_gte(level, PlayerLevel.L5_SYSTEMS) and action in ('BET', 'RAISE', 'CALL'):
        rb = getattr(ctx, 'range_breakdown', None)
        if rb and rb.calling_range_pct > 0:
            if rb.hero_equity_vs_callers < 0.40:
                return "Raising targets thin value -- you're likely behind the calling range."
            elif rb.value_target_pct > 0.20:
                return f"{rb.value_target_pct*100:.0f}% of villain's range is worse and would call."

    # --- Pot odds ---
    if ctx.to_call_amount > 0:
        # pot_size is BEFORE bet; to_call IS the bet. Total = pot + bet + call.
        total = ctx.pot_size + 2 * ctx.to_call_amount
        if total > 0:
            correct_pot_odds = ctx.to_call_amount / total
            equity = ctx.equity_vs_range if ctx.equity_vs_range else ctx.raw_equity

            if abs(equity - correct_pot_odds) > 0.10:
                pct = round(correct_pot_odds * 100)
                eq_pct = round(equity * 100)
                if equity > correct_pot_odds + 0.10:
                    return (
                        f"The pot asks for {pct}% equity. "
                        f"Your hand has {eq_pct}%."
                    )
                else:
                    return (
                        f"The pot asks for {pct}% equity. "
                        f"Your hand has only {eq_pct}%."
                    )

    # --- SPR ---
    spr = ctx.spr
    if spr < 2.5:
        return f"With SPR {spr:.1f}, stack commitment shapes this decision."
    if spr > 12.0:
        return f"With SPR {spr:.1f}, deep stacks favor positional play."

    # --- Draw quality ---
    draw_outs = ctx.draw_outs
    if draw_outs > 0:
        # Prefer ctx.draw_equity if populated; fall back to rule-of-2 approximation
        draw_equity = ctx.draw_equity if ctx.draw_equity else draw_outs * 0.022
        if draw_equity >= 0.35:
            return (
                f"You have {draw_outs:.0f} outs to improve "
                f"-- substantial draw equity."
            )

    return None
