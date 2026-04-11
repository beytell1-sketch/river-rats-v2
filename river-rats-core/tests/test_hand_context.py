"""
Tests for HandContext — hand context and render context builder.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from coaching.hand_context import (
    HandContext, build_hand_context, build_render_context,
    CATEGORY_DESCRIPTIONS, POSITION_NAMES, STREET_NAMES,
    _category_to_description,
)


# ═══════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def strong_hand_features():
    """Top pair on the flop, IP, facing a bet."""
    return {
        "street": 0.0,
        "facing_bet": 1.0,
        "pot_size": 10.0,
        "to_call": 5.0,
        "pot_odds": 0.33,
        "bet_to_pot": 0.5,
        "hero_position": 3.0,   # BTN
        "villain_position": 5.0, # BB
        "is_ip": 1.0,
        "hand_category": 6.0,   # top_pair (integer encoding)
        "hand_rank": 5.0,
        "is_made_hand": 1.0,
        "is_strong_made": 0.0,
        "is_monster": 0.0,
        "has_flush_draw": 0.0,
        "has_straight_draw": 0.0,
        "draw_outs": 0.0,
        "is_monotone": 0.0,
        "is_two_tone": 1.0,
        "is_rainbow": 0.0,
        "is_paired": 0.0,
        "is_double_paired": 0.0,
        "connectivity_score": 0.4,
        "high_card_rank": 12.0,
        "danger_score": 0.55,
        "flush_danger": 0.3,
        "straight_danger": 0.25,
        "raw_equity": 0.62,
        "equity_vs_range": 0.65,
        "better_hand_pct": 0.30,
        "worse_hand_pct": 0.70,
        "equity_margin": 0.32,
        "spr": 8.0,
    }


@pytest.fixture
def weak_hand_features():
    """High card on the river, OOP, facing a bet."""
    return {
        "street": 2.0,
        "facing_bet": 1.0,
        "pot_size": 20.0,
        "to_call": 15.0,
        "pot_odds": 0.43,
        "bet_to_pot": 0.75,
        "hero_position": 4.0,   # SB
        "villain_position": 3.0, # BTN
        "is_ip": 0.0,
        "hand_category": 0.0,   # high_card (integer encoding)
        "hand_rank": 1.0,
        "is_made_hand": 0.0,
        "is_strong_made": 0.0,
        "is_monster": 0.0,
        "has_flush_draw": 0.0,
        "has_straight_draw": 0.0,
        "draw_outs": 0.0,
        "is_monotone": 0.0,
        "is_two_tone": 0.0,
        "is_rainbow": 1.0,
        "is_paired": 0.0,
        "is_double_paired": 0.0,
        "connectivity_score": 0.2,
        "high_card_rank": 10.0,
        "danger_score": 0.30,
        "flush_danger": 0.0,
        "straight_danger": 0.3,
        "raw_equity": 0.05,
        "equity_vs_range": 0.04,
        "better_hand_pct": 0.90,
        "worse_hand_pct": 0.10,
        "equity_margin": -0.39,
        "spr": 1.5,
    }


@pytest.fixture
def draw_hand_features():
    """Flush draw on the turn, IP, no bet."""
    return {
        "street": 1.0,
        "facing_bet": 0.0,
        "pot_size": 8.0,
        "to_call": 0.0,
        "pot_odds": 0.0,
        "bet_to_pot": 0.0,
        "hero_position": 2.0,   # CO
        "villain_position": 4.0, # SB
        "is_ip": 1.0,
        "hand_category": 0.0,   # high_card (made hand; draw tracked by has_flush_draw)
        "hand_rank": 2.0,
        "is_made_hand": 0.0,
        "is_strong_made": 0.0,
        "is_monster": 0.0,
        "has_flush_draw": 1.0,
        "has_straight_draw": 0.0,
        "draw_outs": 9.0,
        "is_monotone": 0.0,
        "is_two_tone": 1.0,
        "is_rainbow": 0.0,
        "is_paired": 0.0,
        "is_double_paired": 0.0,
        "connectivity_score": 0.3,
        "high_card_rank": 11.0,
        "danger_score": 0.60,
        "flush_danger": 0.6,
        "straight_danger": 0.0,
        "raw_equity": 0.35,
        "equity_vs_range": 0.38,
        "better_hand_pct": 0.55,
        "worse_hand_pct": 0.45,
        "equity_margin": 0.05,
        "spr": 12.0,
    }


# ═══════════════════════════════════════════════════════════════════
# MAPPING TABLES
# ═══════════════════════════════════════════════════════════════════

class TestCategoryDescriptions:
    """Test the category-to-description mapping."""
    
    def test_all_categories_have_descriptions(self):
        """Every category value maps to a non-empty string."""
        for val, desc in CATEGORY_DESCRIPTIONS.items():
            assert isinstance(desc, str)
            assert len(desc) > 0, f"Empty description for {val}"
    
    def test_descriptions_are_noun_phrases(self):
        """Descriptions should not start with 'Your' (avoid double possessive)."""
        for val, desc in CATEGORY_DESCRIPTIONS.items():
            assert not desc.startswith("Your "), f"Starts with 'Your': {desc}"
            assert not desc.startswith("your "), f"Starts with 'your': {desc}"
    
    def test_monster_hands_described(self):
        """Monster hands have appropriate descriptions."""
        assert "straight flush" in CATEGORY_DESCRIPTIONS[17.0]
        assert "quads" in CATEGORY_DESCRIPTIONS[16.0]
        assert "full house" in CATEGORY_DESCRIPTIONS[15.0]
    
    def test_common_hands_described(self):
        """Common hand categories have descriptions."""
        assert "top pair" in CATEGORY_DESCRIPTIONS[6.0]
        assert "high card" in CATEGORY_DESCRIPTIONS[0.0]
        assert "two pair" in CATEGORY_DESCRIPTIONS[10.0]
    
    def test_descriptions_work_after_your(self):
        """'Your ' + description should read naturally."""
        for val, desc in CATEGORY_DESCRIPTIONS.items():
            phrase = f"Your {desc}"
            # Should not produce "Your your hand" or "Your Your"
            assert "your your" not in phrase.lower(), f"Double possessive: {phrase}"
    
    def test_descriptions_work_after_you_have(self):
        """'you have ' + description should read naturally."""
        for val, desc in CATEGORY_DESCRIPTIONS.items():
            phrase = f"you have {desc}"
            assert len(phrase) > len("you have "), f"Empty desc: {phrase}"
    
    def test_nearest_match_handles_float_precision(self):
        """Slightly off float values should still match."""
        # 6.0 = top_pair, but might come as 5.9999999 or 6.0000001
        assert "top pair" in _category_to_description(6.0000001)
        assert "top pair" in _category_to_description(5.9999999)
    
    def test_unknown_category_returns_fallback(self):
        """Unknown values return 'your hand' fallback."""
        assert _category_to_description(99.0) == "your hand"
        assert _category_to_description(-1.0) == "your hand"
    
    def test_negative_returns_fallback(self):
        """Negative category returns fallback."""
        assert _category_to_description(-1) == "your hand"


class TestPositionNames:
    """Test position ordinal → name mapping."""
    
    def test_all_six_positions(self):
        """All 6 positions are mapped."""
        assert len(POSITION_NAMES) == 6
    
    def test_known_positions(self):
        assert POSITION_NAMES[0.0] == "UTG"
        assert POSITION_NAMES[3.0] == "BTN"
        assert POSITION_NAMES[4.0] == "SB"
        assert POSITION_NAMES[5.0] == "BB"
    
    def test_positions_are_strings(self):
        for val, name in POSITION_NAMES.items():
            assert isinstance(name, str)
            assert len(name) >= 2


class TestStreetNames:
    """Test street float → name mapping."""
    
    def test_three_streets(self):
        assert len(STREET_NAMES) == 3
    
    def test_known_streets(self):
        assert STREET_NAMES[0.0] == "flop"
        assert STREET_NAMES[1.0] == "turn"
        assert STREET_NAMES[2.0] == "river"


# ═══════════════════════════════════════════════════════════════════
# HAND CONTEXT FACTORY
# ═══════════════════════════════════════════════════════════════════

class TestBuildHandContext:
    """Test the HandContext factory function."""
    
    def test_basic_construction(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert isinstance(ctx, HandContext)
    
    def test_frozen(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        with pytest.raises(AttributeError):
            ctx.hero_cards = "changed"
    
    def test_position_names(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.hero_position_name == "BTN"
        assert ctx.villain_position_name == "BB"
    
    def test_street_name(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.street_name == "flop"
        assert ctx.street_name_cap == "Flop"
    
    def test_hand_description_top_pair(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.hand_description == "top pair"
        assert ctx.hand_description_cap == "Top pair"
    
    def test_hand_description_high_card(self, weak_hand_features):
        ctx = build_hand_context(weak_hand_features)
        assert ctx.hand_description == "high card"
    
    def test_hand_description_flush_draw(self, draw_hand_features):
        ctx = build_hand_context(draw_hand_features)
        assert ctx.hand_description == "a flush draw"
    
    def test_is_ip_true(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.is_ip is True
    
    def test_is_ip_false(self, weak_hand_features):
        ctx = build_hand_context(weak_hand_features)
        assert ctx.is_ip is False
    
    def test_is_initiative_facing_bet(self, strong_hand_features):
        """facing_bet=1.0 → is_initiative=False"""
        ctx = build_hand_context(strong_hand_features)
        assert ctx.is_initiative is False
    
    def test_is_initiative_no_bet(self, draw_hand_features):
        """facing_bet=0.0 → is_initiative=True"""
        ctx = build_hand_context(draw_hand_features)
        assert ctx.is_initiative is True
    
    def test_numeric_values_preserved(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.equity_vs_range == 0.65
        assert ctx.spr == 8.0
        assert ctx.draw_outs == 0.0
        assert ctx.danger_score == 0.55
    
    def test_optional_cards(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features, hero_cards="AcKs", board_cards="Ts9s4c")
        assert ctx.hero_cards == "AcKs"
        assert ctx.board_cards == "Ts9s4c"
    
    def test_default_empty_cards(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        assert ctx.hero_cards == ""
        assert ctx.board_cards == ""
    
    def test_unknown_position_fallback(self):
        """Unknown position ordinal gets a sensible fallback."""
        feat = {"hero_position": 99.0, "villain_position": -1.0}
        ctx = build_hand_context(feat)
        assert "99" in ctx.hero_position_name  # fallback includes the number


# ═══════════════════════════════════════════════════════════════════
# RENDER CONTEXT
# ═══════════════════════════════════════════════════════════════════

class TestBuildRenderContext:
    """Test the render context builder."""
    
    def test_returns_dict(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "CALL")
        assert isinstance(rc, dict)
    
    def test_hand_desc_is_noun_phrase(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        assert rc["hand_desc"] == "top pair"
        # Should NOT produce "Your your hand" in templates
        test_phrase = f"Your {rc['hand_desc']} is strong"
        assert "your your" not in test_phrase.lower()
    
    def test_capitalized_hand_desc(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        assert rc["Hand_desc"] == "Top pair"
    
    def test_equity_as_percentage(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "CALL")
        assert rc["equity_pct"] == pytest.approx(65.0, abs=0.1)
    
    def test_margin_as_percentage(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "CALL")
        assert rc["margin"] == pytest.approx(32.0, abs=0.1)
    
    def test_range_percentages(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "CALL")
        assert rc["top_range_pct"] == pytest.approx(70.0, abs=0.1)
        assert rc["bottom_range_pct"] == pytest.approx(30.0, abs=0.1)
    
    def test_pot_odds(self, weak_hand_features):
        ctx = build_hand_context(weak_hand_features)
        rc = build_render_context(ctx, "FOLD")
        assert rc["pot_odds_pct"] == pytest.approx(43.0, abs=0.1)
    
    def test_draw_outs(self, draw_hand_features):
        ctx = build_hand_context(draw_hand_features)
        rc = build_render_context(ctx, "CHECK")
        assert rc["outs"] == 9.0
        assert rc["draw_equity_outs_pct"] == pytest.approx(19.8, abs=0.1)
    
    def test_spr(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "CALL")
        assert rc["spr"] == 8.0
    
    def test_danger(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        assert rc["danger"] == pytest.approx(55.0, abs=0.1)
    
    def test_action_name(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "FOLD")
        assert rc["action"] == "fold"
    
    def test_action_default(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx)
        assert rc["action"] == "continue"
    
    def test_position_names_in_context(self, strong_hand_features):
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        assert rc["hero_pos"] == "BTN"
        assert rc["villain_pos"] == "BB"


# ═══════════════════════════════════════════════════════════════════
# TEMPLATE INTEGRATION — The "Your your hand" fix
# ═══════════════════════════════════════════════════════════════════

class TestTemplateIntegration:
    """
    Test that HandContext + templates produce correct English.
    This is the primary deliverable of Phase 3.
    """
    
    def test_your_hand_desc_no_double_possessive(self, strong_hand_features):
        """'Your {hand_desc}' must NOT produce 'Your your hand'."""
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        
        template = "Your {hand_desc} is strong on this board."
        rendered = template.format(**rc)
        assert rendered == "Your top pair is strong on this board."
        assert "your your" not in rendered.lower()
    
    def test_you_have_hand_desc(self, strong_hand_features):
        """'Even though you have {hand_desc}' reads naturally."""
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "FOLD")
        
        template = "Even though you have {hand_desc}, it doesn't hold up."
        rendered = template.format(**rc)
        assert rendered == "Even though you have top pair, it doesn't hold up."
    
    def test_hand_desc_at_sentence_start(self, strong_hand_features):
        """'{Hand_desc} is in the top...' capitalizes correctly."""
        ctx = build_hand_context(strong_hand_features)
        rc = build_render_context(ctx, "BET")
        
        template = "{Hand_desc} is in the top {top_range_pct:.0f}% of your range."
        rendered = template.format(**rc)
        assert rendered == "Top pair is in the top 70% of your range."
    
    def test_equity_in_template(self, weak_hand_features):
        """Equity renders correctly in L4-style templates."""
        ctx = build_hand_context(weak_hand_features)
        rc = build_render_context(ctx, "FOLD")
        
        template = "At {equity_pct:.0f}% equity, you're behind."
        rendered = template.format(**rc)
        assert rendered == "At 4% equity, you're behind."
    
    def test_margin_in_template(self, weak_hand_features):
        """Margin renders with sign."""
        ctx = build_hand_context(weak_hand_features)
        rc = build_render_context(ctx, "FOLD")
        
        template = "At {margin:+.0f}%, the math clearly says fold."
        rendered = template.format(**rc)
        assert rendered == "At -39%, the math clearly says fold."
    
    def test_draw_in_template(self, draw_hand_features):
        """Draw outs render correctly."""
        ctx = build_hand_context(draw_hand_features)
        rc = build_render_context(ctx, "BET")
        
        template = "Your draw has {outs:.0f} outs — roughly {draw_equity_outs_pct:.0f}% to improve."
        rendered = template.format(**rc)
        assert rendered == "Your draw has 9 outs — roughly 20% to improve."
    
    def test_article_hands_read_naturally(self, draw_hand_features):
        """Hands with articles ('a flush draw') work in context."""
        ctx = build_hand_context(draw_hand_features)
        rc = build_render_context(ctx, "BET")
        
        # "Your a flush draw" is awkward but acceptable for now
        # The resolver will handle article-stripping for "Your" prefix
        template = "You have {hand_desc} — you're drawing to a strong hand."
        rendered = template.format(**rc)
        assert "a flush draw" in rendered
    
    def test_set_description(self):
        """Set hands use 'a set' for natural English."""
        feat = {"hand_category": 12.0}
        ctx = build_hand_context(feat)
        assert ctx.hand_description == "a set"
        
        rc = build_render_context(ctx, "BET")
        template = "You have {hand_desc} — bet for value."
        rendered = template.format(**rc)
        assert rendered == "You have a set — bet for value."
    
    def test_overpair_description(self):
        """Overpair uses 'an overpair' for natural English."""
        feat = {"hand_category": 9.0}
        ctx = build_hand_context(feat)
        assert ctx.hand_description == "an overpair"


# ═══════════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases and boundary conditions."""
    
    def test_empty_feature_dict(self):
        """Empty dict produces sensible defaults."""
        ctx = build_hand_context({})
        assert ctx.street_name == "unknown"
        assert ctx.hand_description == "your hand"
        assert ctx.is_ip is False
        assert ctx.equity_vs_range == 0
    
    def test_missing_features_dont_crash(self):
        """Missing features default to 0, not KeyError."""
        ctx = build_hand_context({"street": 1.0})
        assert ctx.street_name == "turn"
        assert ctx.equity_vs_range == 0
        assert ctx.spr == 0
    
    def test_render_context_with_zero_equity(self):
        """Zero equity doesn't produce bad template output."""
        ctx = build_hand_context({"equity_vs_range": 0, "raw_equity": 0})
        rc = build_render_context(ctx, "FOLD")
        assert rc["equity_pct"] == 0
    
    def test_all_category_values_roundtrip(self):
        """Every category value in the map produces a valid HandContext."""
        for cat_val in CATEGORY_DESCRIPTIONS:
            ctx = build_hand_context({"hand_category": cat_val})
            assert ctx.hand_description != "your hand", f"Category {cat_val} fell through to fallback"
            assert len(ctx.hand_description) > 0


# ═══════════════════════════════════════════════════════════════════
# ACTION HISTORY FIELDS (new in 38-feature expansion)
# ═══════════════════════════════════════════════════════════════════

class TestActionHistoryFields:
    """Test 4 new action history features and multiway seeds."""

    def test_3bet_pot_true(self):
        ctx = build_hand_context({"is_3bet_pot": 1.0})
        assert ctx.is_3bet_pot is True

    def test_3bet_pot_false_default(self):
        ctx = build_hand_context({})
        assert ctx.is_3bet_pot is False

    def test_villain_aggression_count(self):
        ctx = build_hand_context({"villain_aggression_count": 2.0})
        assert ctx.villain_aggression_count == 2
        assert isinstance(ctx.villain_aggression_count, int)

    def test_villain_checked_back(self):
        ctx = build_hand_context({"villain_checked_back": 1.0})
        assert ctx.villain_checked_back is True

    def test_villain_call_count(self):
        ctx = build_hand_context({"villain_call_count": 3.0})
        assert ctx.villain_call_count == 3
        assert isinstance(ctx.villain_call_count, int)

    def test_all_default_to_zero(self):
        ctx = build_hand_context({"street": 1.0})
        assert ctx.is_3bet_pot is False
        assert ctx.villain_aggression_count == 0
        assert ctx.villain_checked_back is False
        assert ctx.villain_call_count == 0


class TestMultiwaySeeds:
    """Test num_opponents and opponent_phrase."""

    def test_default_hu(self):
        ctx = build_hand_context({})
        assert ctx.num_opponents == 1
        assert ctx.opponent_phrase == "your opponent"

    def test_multiway(self):
        ctx = build_hand_context({}, num_opponents=3)
        assert ctx.num_opponents == 3
        assert ctx.opponent_phrase == "your opponents"

    def test_render_context_hu(self):
        ctx = build_hand_context({})
        rc = build_render_context(ctx, "BET")
        assert rc["opponent_phrase"] == "your opponent"
        assert rc["num_opponents"] == 1

    def test_render_context_mw(self):
        ctx = build_hand_context({}, num_opponents=2)
        rc = build_render_context(ctx, "BET")
        assert rc["opponent_phrase"] == "your opponents"
        assert rc["num_opponents"] == 2

    def test_render_context_action_history(self):
        ctx = build_hand_context({
            "is_3bet_pot": 1.0,
            "villain_aggression_count": 2.0,
            "villain_checked_back": 1.0,
            "villain_call_count": 1.0,
        })
        rc = build_render_context(ctx, "RAISE")
        assert rc["is_3bet_pot"] is True
        assert rc["v_aggression"] == 2
        assert rc["v_checked_back"] is True
        assert rc["v_call_count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
