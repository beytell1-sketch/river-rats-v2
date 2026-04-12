#!/usr/bin/env python3
"""Generate solver verification PDFs for the facing-bet test set.

Each page presents one hand in the format the owner needs to input
into GTO Wizard:
  1. Positions involved
  2. Flop cards (colored)
  3. Flop action sequence (OOP first, IP last, no skips)
  4. Turn card (if applicable)
  5. Turn action sequence
  6. River card (if applicable)
  7. River action sequence
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import (
    HexColor, black, white, red
)
from reportlab.pdfgen import canvas

WIDTH, HEIGHT = A4

# Card colors
SUIT_COLORS = {
    's': black,            # spades
    'c': HexColor('#228B22'),  # clubs (green)
    'd': HexColor('#0066CC'),  # diamonds (blue)
    'h': red,              # hearts
}

SUIT_SYMBOLS = {
    's': '\u2660',  # ♠
    'c': '\u2663',  # ♣
    'd': '\u2666',  # ♦
    'h': '\u2665',  # ♥
}

RANK_DISPLAY = {
    'A': 'A', 'K': 'K', 'Q': 'Q', 'J': 'J', 'T': '10',
    '9': '9', '8': '8', '7': '7', '6': '6', '5': '5',
    '4': '4', '3': '3', '2': '2',
}

# Postflop position order (OOP → IP)
POSITION_ORDER = {'SB': 0, 'BB': 1, 'UTG': 2, 'HJ': 3, 'CO': 4, 'BTN': 5}


def draw_card(c, x, y, card_str, size=28):
    """Draw a single colored card at (x, y)."""
    rank = card_str[0]
    suit = card_str[1].lower()

    rank_text = RANK_DISPLAY.get(rank, rank)
    suit_sym = SUIT_SYMBOLS.get(suit, '?')
    color = SUIT_COLORS.get(suit, black)

    card_w = size * 1.6
    card_h = size * 2.2

    # Card background
    c.setFillColor(white)
    c.setStrokeColor(HexColor('#888888'))
    c.setLineWidth(1.5)
    c.roundRect(x, y, card_w, card_h, 4, fill=1, stroke=1)

    # Rank
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(x + card_w / 2, y + card_h * 0.55, rank_text)

    # Suit
    c.setFont("Helvetica", size * 0.75)
    c.drawCentredString(x + card_w / 2, y + card_h * 0.15, suit_sym)


def draw_card_row(c, x, y, cards, size=28, gap=8):
    """Draw a row of cards. Returns the x after the last card."""
    card_w = size * 1.6
    for i, card in enumerate(cards):
        draw_card(c, x + i * (card_w + gap), y, card, size)
    return x + len(cards) * (card_w + gap)


def draw_action_sequence(c, x, y, actions, font_size=12):
    """Draw action sequence as colored text lines.

    actions: list of (position, action_text) tuples, already in
    postflop order (OOP first).
    """
    c.setFont("Helvetica", font_size)
    line_height = font_size * 1.6
    for i, (pos, action) in enumerate(actions):
        # Position label
        c.setFillColor(HexColor('#555555'))
        c.drawString(x, y - i * line_height, f"{pos}:")

        # Action (colored by type)
        action_upper = action.upper()
        if 'BET' in action_upper or 'RAISE' in action_upper:
            c.setFillColor(HexColor('#CC0000'))
        elif 'CALL' in action_upper:
            c.setFillColor(HexColor('#006600'))
        elif 'CHECK' in action_upper:
            c.setFillColor(HexColor('#666666'))
        elif 'FOLD' in action_upper:
            c.setFillColor(HexColor('#999999'))
        else:
            c.setFillColor(black)
        c.drawString(x + 40, y - i * line_height, action)

    return y - len(actions) * line_height


def sort_positions(positions):
    """Sort positions in postflop order (OOP first)."""
    return sorted(positions, key=lambda p: POSITION_ORDER.get(p, 99))


def generate_hand_page(c, hand):
    """Generate one page for a single hand verification."""
    c.showPage()

    margin_left = 25 * mm
    y = HEIGHT - 25 * mm

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(black)
    c.drawString(margin_left, y, f"Solver Verification — {hand['id']}")
    y -= 8 * mm

    # Hero info line (text only, no cards inline)
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#333333'))
    c.drawString(margin_left, y, f"Hero: {hand['hero_pos']}  |  Label: {hand['label']}  |  Confidence: {hand['confidence']}")
    y -= 10 * mm

    # Hero cards on their own line
    c.setFont("Helvetica", 11)
    c.setFillColor(HexColor('#555555'))
    c.drawString(margin_left, y, "Hero cards:")
    y -= 5 * mm
    draw_card_row(c, margin_left + 10, y - 48, hand['hero_cards'], size=22)
    y -= 58 * mm

    # Separator
    c.setStrokeColor(HexColor('#CCCCCC'))
    c.setLineWidth(0.5)
    c.line(margin_left, y, WIDTH - margin_left, y)
    y -= 8 * mm

    # 1. Positions
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(black)
    c.drawString(margin_left, y, "1. Positions")
    y -= 6 * mm
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor('#333333'))
    positions_sorted = sort_positions(hand['positions'])
    c.drawString(margin_left + 10, y, "  \u2192  ".join(positions_sorted) + "   (OOP \u2192 IP)")
    y -= 6 * mm

    # Preflop action
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#777777'))
    c.drawString(margin_left + 10, y, f"Preflop: {hand['preflop']}")
    y -= 10 * mm

    # Process each street
    for street_num, street_info in enumerate(hand['streets']):
        street_name = street_info['name']
        cards = street_info['cards']
        actions = street_info['actions']

        # Street header
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(black)
        step = 2 + street_num * 2
        c.drawString(margin_left, y, f"{step}. {street_name} cards")
        y -= 5 * mm

        # Cards — draw below current y with proper clearance
        card_h = 26 * 2.2  # card height at size=26
        draw_card_row(c, margin_left + 10, y - card_h, cards, size=26)
        y -= card_h + 10 * mm

        # Action sequence header
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(black)
        c.drawString(margin_left, y, f"{step + 1}. {street_name} action sequence")
        y -= 6 * mm

        # Actions
        y = draw_action_sequence(c, margin_left + 10, y, actions, font_size=12)
        y -= 10 * mm

    # Decision point
    c.setStrokeColor(HexColor('#CC0000'))
    c.setLineWidth(1.5)
    c.line(margin_left, y, WIDTH - margin_left, y)
    y -= 7 * mm
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(HexColor('#CC0000'))
    c.drawString(margin_left, y, f"DECISION: Hero ({hand['hero_pos']}) to act")
    y -= 6 * mm
    c.setFont("Helvetica", 12)
    c.setFillColor(black)
    c.drawString(margin_left + 10, y, f"Pot: {hand['pot']}  |  Facing bet: {hand['bet']}  |  To call: {hand['to_call']}")
    y -= 5 * mm
    c.drawString(margin_left + 10, y, f"Pot odds: {hand['pot_odds']}")
    y -= 7 * mm

    # Expert label
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(HexColor('#006600'))
    c.drawString(margin_left, y, f"Expert label: {hand['label']} ({hand['confidence']})")
    y -= 5 * mm
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor('#555555'))

    # Wrap the verification question
    c.drawString(margin_left + 10, y, f"Verify: {hand['verify_question']}")


def main():
    # Sample: FB-34
    fb34 = {
        'id': 'FB-34',
        'hero_pos': 'BB',
        'hero_cards': ['Ks', '6s'],
        'label': 'RAISE',
        'confidence': 'MEDIUM',
        'positions': ['BB', 'CO', 'BTN'],
        'preflop': 'CO opens 2.5bb, BTN calls, BB calls',
        'streets': [
            {
                'name': 'FLOP',
                'cards': ['As', '9s', '4s'],
                'actions': [
                    ('BB', 'Check'),
                    ('CO', 'Check'),
                    ('BTN', 'Bet 30 into 90'),
                    ('CO', 'Call 30'),
                    ('BB', '??? (HERO DECISION)'),
                ],
            },
        ],
        'pot': '120 (after CO call)',
        'bet': '30',
        'to_call': '30',
        'pot_odds': '30 / (120 + 30 + 30) = 16.7%',
        'verify_question': 'Does solver RAISE or CALL with Ks6s (nut flush) on As9s4s monotone facing small bet + call?',
    }

    output_path = os.path.join(
        os.path.dirname(__file__),
        'SOLVER_VERIFY_SAMPLE_FB34.pdf'
    )

    pdf = canvas.Canvas(output_path, pagesize=A4)
    pdf.setTitle("Solver Verification — FB-34 Sample")
    generate_hand_page(pdf, fb34)
    pdf.save()
    print(f"Written to: {output_path}")


if __name__ == '__main__':
    main()
