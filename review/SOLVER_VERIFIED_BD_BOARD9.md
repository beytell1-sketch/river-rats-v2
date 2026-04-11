# Solver-Verified Hands: BD_Board9 (Qh 9h 4d Tc) — CORRECTED

**Date:** 7 April 2026
**Source:** GTO Wizard, exact line verified by owner
**Status:** VERIFIED — replaces original BD_Board9 (which had Th making all heart hands made flushes)

---

## Board correction

Original turn card: Th (3 hearts = all heart holdings were made flushes, useless for training draws)
Corrected turn card: **Tc** (2 hearts = heart holdings are flush DRAWS, which is the intended teaching)

---

## Setup (identical for all hands)

**Players:** CO (opener), BTN (cold-caller, bettor), SB (hero, defender, OOP sandwich)

**Preflop:** CO opens. BTN calls. SB defends. Pot: 90.

**Flop: Qh 9h 4d**
SB checks. CO checks. BTN checks. Pot: 90.

**Turn: Tc**
SB checks. CO checks. BTN bets 60 (66% pot) into 90.

**Hero's decision:** SB faces 60. Pot ~210 if calling. SPR ~0.56.

**Solver sizing:** 66% pot (BTN bet). Hero can call, raise, or fold.

---

## Solver results

| # | Hero Hand | Solver Action | Key Blocker/Draw Effect |
|---|-----------|--------------|------------------------|
| 1 | Kh 6h | **RAISE** | NFD (Kh) + blocker. Flush draw with high heart blocks villain's flush combos. Raise. |
| 2 | Ah 3h | **CALL** | NFD (Ah) + Ah blocker but low side equity (3h). Solver prefers call despite Ah. |
| 3 | 6h 7h | **FOLD** | Non-nut FD, low cards, no side equity, no blocker to value. Fold. |
| 4 | 8h 7h | **CALL** | Non-nut FD but with gutshot straight draw (7-8-9-T). Extra outs justify call. |
| 5 | 9s 9c | **CALL** | Set of 9s. No flush draw. Strong made hand but flush-heavy board. Call. |
| 6 | Kh Jh | **RAISE** | All KJ variants raise. NFD + straight draw (J-T-9 or K-Q-J-T). Combo draw + blocker. |
| 7 | Ks Jh | **RAISE** | KJ raises regardless of suits — the straight equity is the driver alongside flush draw. |
| 8 | Kc Jd | **RAISE** | Even offsuit KJ raises — the OESD (8-9-T-J or J-Q-K) + overcards is enough. |
| 9 | Kd Js | **RAISE** | Same — all KJ combos raise on this board/line. |

---

## Teaching points

1. **Ah blocker is NOT automatic raise:** Ah3h calls despite holding the nut flush draw + Ah blocker. The low side equity (3h contributes nothing) makes the raise marginal. This contradicts a naive reading of KB Section 1.7 which says "nut draw + blocker + side equity = RAISE." The solver shows side equity matters more than the rule suggests — Ah3h lacks it.

2. **Kh raises but Ah calls:** Kh6h raises while Ah3h calls. Counterintuitive — the nut flush draw (Ah) is "better" but the solver prefers raising with the second-nut (Kh). Likely because: (a) Kh6h has less showdown value than Ah3h so prefers aggression, and (b) the Ah in Ah3h blocks villain's folding range (busted Ah-high hands) — early echo of the Ace blocker paradox.

3. **KJ raises in ALL suits:** The straight draw equity (OESD to broadway) is so strong that even offsuit KJ without hearts raises. This is NOT a blocker-driven raise — it's a pure equity + fold equity raise from combo draw strength.

4. **6h7h folds, 8h7h calls:** One extra gutshot out (the 8 connecting to 7-8-9-T) flips fold to call. Marginal draws are extremely sensitive to side outs.

5. **Set of 9s calls:** Even a set doesn't raise here — the flush-heavy board means villain's raising range includes many flush draws that have decent equity against a set. Pot control with the set.

---

## Training labels

| # | Hero Hand | Training Label | Confidence |
|---|-----------|---------------|------------|
| 1 | Kh 6h | **RAISE** | HIGH |
| 2 | Ah 3h | **CALL** | HIGH |
| 3 | 6h 7h | **FOLD** | HIGH |
| 4 | 8h 7h | **CALL** | HIGH |
| 5 | 9s 9c | **CALL** | HIGH |
| 6 | Kh Jh | **RAISE** | HIGH |
| 7 | Ks Jh | **RAISE** | HIGH |
| 8 | Kc Jd | **RAISE** | HIGH |
| 9 | Kd Js | **RAISE** | HIGH |

---

## Action history for SituationFactory

All hands share this spec (NOTE: turn card changed to Tc):
```
board_cards: ['Qh', '9h', '4d', 'Tc']
hero_pos: 'SB'
villain_positions: ['CO', 'BTN']  # BTN is bettor (last)
pot: 150.0  # 90 preflop + 60 BTN bet
to_call: 60.0
street: 'turn'
action_history: [
    ('preflop', 'CO', 'raise'),
    ('preflop', 'BTN', 'call'),
    ('preflop', 'SB', 'call'),
    ('flop', 'SB', 'check'),
    ('flop', 'CO', 'check'),
    ('flop', 'BTN', 'check'),
    ('turn', 'SB', 'check'),
    ('turn', 'CO', 'check'),
    ('turn', 'BTN', 'bet'),
]
opener_position: 'CO'
effective_stack: 100.0
```

## Note on original BD_Board9 hands

The original 9 hands on Qh 9h 4d **Th** are INVALID — the 3-heart board made all heart holdings into made flushes. These 9 solver-verified hands on Qh 9h 4d **Tc** replace them entirely. Net change: 9 removed, 9 added = same count.
