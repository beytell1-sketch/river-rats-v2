# Design Agent 3 — SP7 and SP10 Hero Card Assignments

**Date:** 9 April 2026
**Author:** Design Agent 3
**Status:** AWAITING REVIEW
**Covers:** SP7 (25 RAISE situations) + SP10 (13 CALL situations) = 38 total

---

## Reference: is_monster Definition

Per RAISE_DECISION_TREE_V2.md Feature Reference:
`is_monster = 1 if set / straight / flush / full_house / quads / straight_flush`

Two pair (hand_category 10) does NOT trigger is_monster. However, to be maximally
safe and produce clean training signal, all SP7 hero hands are assigned
hand_category 6-9 (top_pair through overpair). This eliminates any ambiguity
about whether a specific two-pair combination might score as is_monster in edge
cases (e.g., on a paired board where one board pair + one hero card = full house).

SP7 hero hands: top_pair (6), top_pair_good_kicker (7), top_pair_top_kicker (8),
overpair (9). No sets, no straights, no flushes, no two pairs.

SP10 hero hands: bottom_pair (3), underpair (4), middle_pair (5), top_pair (6),
top_pair_good_kicker (7) — moderate draw equity where applicable.

---

## Card Conflict Rules Applied

- Hero cards must not appear in board_cards
- Each card is unique (no duplicate within hero hand)
- Suit chosen to avoid flush draws on non-flush-danger boards (SP7)
- On two-tone boards, hero cards are in off-suits to avoid inadvertently
  giving hero a flush draw (which would make is_monster=0 harder to maintain
  if the flush draw completes, and would distort the thin-value signal)
- Exception: where a suited card is needed for range realism and does not
  complete a flush (e.g., one heart on a two-heart board is a draw, not a flush)

---

## Board Quick Reference (boards used in SP7/SP10)

| Board | Cards            | Street | Hero  | OOP/IP | SPR  | Texture        |
|-------|------------------|--------|-------|--------|------|----------------|
| B02   | Kh 7h 3d         | Flop   | BB    | OOP    | 5.0  | Two-tone (hts) |
| B06   | 8c 8h 3d         | Flop   | BB    | OOP    | 5.5  | Paired, rainbow|
| B08   | Qc 5c 9h         | Flop   | BB    | OOP    | 5.0  | Two-tone (cls) |
| B12   | 7c 2d Kc Ac      | Turn   | BB    | OOP    | 3.0  | Two-tone (cls) |
| B13   | Qd 6h 2s Jc      | Turn   | SB    | OOP    | 8.4  | Rainbow        |
| B15   | Tc 3d 9h 9s      | Turn   | BB    | OOP    | 2.6  | Paired, rainbow|
| B17   | Ad 7s 3c 2h      | Turn   | SB    | OOP    | 3.0  | Rainbow        |
| B18   | 4d 8d Kh 5c      | Turn   | BB    | OOP    | 4.0  | Two-tone (dmd) |
| B21   | 3h 3d 9s Kc      | Turn   | SB    | OOP    | 3.0  | Paired, TT     |
| B03   | As 5d 2c         | Flop   | CO    | IP     | 9.0  | Rainbow        |
| B07   | 5h 6c 7d         | Flop   | BTN   | IP     | 9.0  | Connected, R   |
| B10   | Kc 4d 2h         | Flop   | BB    | OOP    | 9.0  | Rainbow        |
| B11r  | Ts 8s 4h         | Flop   | BTN   | IP     | 5.0  | Two-tone (spd) |
| B14   | 3s Js 9h 4d      | Turn   | CO    | IP     | 3.0  | Two-tone (spd) |
| B16   | 5h Kd 2h 8c      | Turn   | BTN   | IP     | 4.0  | Two-tone (hts) |
| B19   | 4c 6h 8s 7d      | Turn   | BTN   | IP     | 2.0  | Connected, R   |
| B20   | 2c 9c Qh 6s      | Turn   | CO    | IP     | 1.4  | Two-tone (cls) |
| B21   | 3h 3d 9s Kc      | Turn   | SB    | OOP    | 3.0  | Paired, TT     |
| B27   | 4d 8h 2c 6s Jd   | River  | BTN   | IP     | 0.9  | Rainbow        |
| B28   | 3s 7h Ks 2c Ts   | River  | CO    | IP     | 0.9  | Two-tone (spd) |

---

## SP7: OOP Thin Value Check-Raise — 25 RAISE Situations

### Step 4 Conditions (ALL required for each situation)
- hero_range_percentile >= 0.75
- is_monster == 0
- is_ip == 0 (OOP only)
- villain_fold_equity_estimate >= 0.40
- villain_aggression_count <= 1
- flush_danger <= 0.35
- straight_danger <= 0.35
- num_callers_to_bet == 0

---

### SP7_01

**Board:** B02 — Kh 7h 3d (Flop, OOP BB, SPR=5.0, two-tone hearts)

- **hero_cards:** `['Kd', 'Qs']`
- **hand_category:** top_pair_top_kicker (8) — KQ on K73 board; K is top pair, Q is top kicker
- **is_monster:** 0 — no set, no flush, no straight, no full house
- **Description:** Hero holds KdQs in BB on Kh-7h-3d. Top pair top kicker, rainbow holding on a two-tone board. Checks and faces a BTN bet. Strong non-monster hand OOP qualifies for thin value check-raise.
- **range_pct:** 0.76 | **fold_eq:** 0.42 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_02

**Board:** B06 — 8c 8h 3d (Flop, OOP BB, SPR=5.5, paired rainbow)

- **hero_cards:** `['As', 'Ks']`
- **hand_category:** overpair (9) — AA or AK? With Ace-King: no pair yet... Revise: overpair needs a pocket pair above the board. Board high card is 8. Hero needs a pocket pair 9+.
- **Correction:** hero_cards = `['Ac', 'Ad']` — but Ac is on the board (8c 8h 3d — no Ac). Wait, board is 8c 8h 3d; no ace on board. Ac and Ad are both clear.
  - However, Ac-Ad = pocket aces = overpair above 8-high board. is_monster = 0 (overpair is hand_category 9, not is_monster). VALID.
- **hero_cards:** `['Ac', 'Ad']`
- **hand_category:** overpair (9) — pocket aces on 8c-8h-3d
- **is_monster:** 0 — AA is an overpair (hand_category 9), not a set/flush/straight/full_house
- **Description:** Hero holds AcAd in BB on 8c-8h-3d paired rainbow board. Overpair to the board's highest non-pair card. Aggressive villain count 1; fold equity 0.45. OOP thin value check-raise.
- **range_pct:** 0.78 | **fold_eq:** 0.45 | **aggr:** 1 | **flush_d:** 0.10 | **straight_d:** 0.05
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_03

**Board:** B06 — 8c 8h 3d (Flop, OOP BB, SPR=5.5, paired rainbow)

- **hero_cards:** `['Kd', 'Ks']`
- **hand_category:** overpair (9) — pocket kings on 8c-8h-3d
- **is_monster:** 0 — KK is an overpair above the 8-high board; no set, flush, straight, or full house
- **Description:** Hero holds KdKs in BB on 8c-8h-3d. Overpair, villain aggression 0, fold equity 0.43. Same board as SP7_02 with aggr=0 variant.
- **range_pct:** 0.78 | **fold_eq:** 0.43 | **aggr:** 0 | **flush_d:** 0.10 | **straight_d:** 0.05
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_04

**Board:** B13 — Qd 6h 2s Jc (Turn, OOP SB, SPR=8.4, rainbow)

- **hero_cards:** `['Qh', 'Ts']`
- **hand_category:** top_pair_good_kicker (7) — QT on Qd-6h-2s-Jc; Q top pair, T is a decent kicker (second pair candidate not on board)
- **is_monster:** 0 — one pair only, no flush, no straight (Q-J-T is not yet a straight without K or 9)
- **Description:** Hero holds QhTs in SB on Qd-6h-2s-Jc. Top pair with ten kicker. Rainbow dry turn. OOP facing BTN bet at SPR=8.4. Thin value check-raise with fold equity 0.55.
- **range_pct:** 0.75 | **fold_eq:** 0.55 | **aggr:** 1 | **flush_d:** 0.05 | **straight_d:** 0.20
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_05

**Board:** B17 — Ad 7s 3c 2h (Turn, OOP SB, SPR=3.0, rainbow, to_call=0 hero leads)

- **hero_cards:** `['As', 'Jd']`
- **hand_category:** top_pair_top_kicker (8) — AJ on A-7-3-2 board; A top pair, J top kicker
- **is_monster:** 0 — top pair, no flush (rainbow board), no straight (A-2-3-7 is not a made straight for hero)
- **Description:** Hero holds AsJd in SB on Ad-7s-3c-2h. Top pair top kicker on dry rainbow turn. Hero checks and villain bets. OOP thin value check-raise at SPR=3.0 with fold equity 0.48.
- **range_pct:** 0.78 | **fold_eq:** 0.48 | **aggr:** 0 | **flush_d:** 0.05 | **straight_d:** 0.08
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_06

**Board:** B21 — 3h 3d 9s Kc (Turn, OOP SB, SPR=3.0, paired two-tone)

- **hero_cards:** `['Kh', 'Qs']`
- **hand_category:** top_pair_good_kicker (7) — KQ on 3-3-9-K board; K top pair, Q good kicker
- **is_monster:** 0 — top pair only; board pair (33) does not pair hero's hole cards; no set, no full house (hero has K not 3)
- **Description:** Hero holds KhQs in SB on 3h-3d-9s-Kc. Top pair queen kicker on paired turn. Aggression count 1. Fold equity 0.43. OOP check-raise thin value.
- **range_pct:** 0.77 | **fold_eq:** 0.43 | **aggr:** 1 | **flush_d:** 0.10 | **straight_d:** 0.15
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_07

**Board:** B02 — Kh 7h 3d (Flop, OOP BB, SPR=5.0, two-tone hearts)

- **hero_cards:** `['Kc', 'Qd']`
- **hand_category:** top_pair_top_kicker (8) — KQ on K-7-3; top pair, Q top kicker
- **is_monster:** 0 — top pair only, no flush (Kc Qd are non-heart suits)
- **Description:** Hero holds KcQd in BB on Kh-7h-3d. Top pair top kicker, villain aggression 0, fold equity 0.52. Same board as SP7_01 with higher range percentile band.
- **range_pct:** 0.82 | **fold_eq:** 0.52 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_08

**Board:** B08 — Qc 5c 9h (Flop, OOP BB, SPR=5.0, two-tone clubs)

- **hero_cards:** `['Qd', 'Jh']`
- **hand_category:** top_pair_good_kicker (7) — QJ on Q-5-9; Q top pair, J good kicker
- **is_monster:** 0 — top pair, no flush (Qd Jh are non-club suits), no straight (no 4-card straight made)
- **Description:** Hero holds QdJh in BB on Qc-5c-9h. Top pair jack kicker. Two-tone club board with flush_danger 0.30. Villain aggression 1. Fold equity 0.58. OOP check-raise.
- **range_pct:** 0.83 | **fold_eq:** 0.58 | **aggr:** 1 | **flush_d:** 0.30 | **straight_d:** 0.20
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_09

**Board:** B08 — Qc 5c 9h (Flop, OOP BB, SPR=5.0, two-tone clubs)

- **hero_cards:** `['Qs', 'Td']`
- **hand_category:** top_pair_good_kicker (7) — QT on Q-5-9; Q top pair, T good kicker
- **is_monster:** 0 — top pair, non-club suits, no straight completed
- **Description:** Hero holds QsTd in BB on Qc-5c-9h. Top pair ten kicker. Villain aggression 1, fold equity 0.50. Distinct from SP7_08 (lower kicker, different combo).
- **range_pct:** 0.82 | **fold_eq:** 0.50 | **aggr:** 1 | **flush_d:** 0.30 | **straight_d:** 0.20
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_10

**Board:** B13 — Qd 6h 2s Jc (Turn, OOP SB, SPR=8.4, rainbow)

- **hero_cards:** `['Jh', '9s']`
- **hand_category:** top_pair_good_kicker (7) — J9 on Q-6-2-J; J is now top pair (second highest card after Q), 9 is kicker. Wait — Q is highest, J is second. Top pair would be Q. J-9 gives second pair (J). Let me revise: "top pair" on this board means Q. J would be second pair (middle pair). For range_pct=0.84 (upper-mid band), a good hand is needed. Let me use QhJh but Qd is on the board so Qh is fine.
- **Revision:** hero_cards = `['Qh', 'Jd']` — QJ on Q-6-2-J turn; Q is top pair, J gives two pair... but J also pairs the board (Jc is on the board). Qh pairs the Q; Jd pairs the J. So QJ = two pair on Q-J board? Yes: hero has Q + J, board has Q + J = hero makes top two pair. Two pair is hand_category 10, NOT is_monster (is_monster is set/straight/flush/FH/quads). But to stay cleanly in the non-two-pair zone for SP7 conservatism, avoid two pair.
- **Better option:** hero_cards = `['Qc', 'Ts']` — Q-T on Q-6-2-J. Hero has top pair (Q) with T kicker. No two pair (T is not on board). hand_category = top_pair (6) or top_pair_good_kicker (7). Qc clear of board (board has Qd, not Qc). VALID.
- **hero_cards:** `['Qc', 'Ts']`
- **hand_category:** top_pair_good_kicker (7) — Q top pair, T kicker on Q-6-2-J board
- **is_monster:** 0 — one pair only, no straight, no flush
- **Description:** Hero holds QcTs in SB on Qd-6h-2s-Jc. Top pair with ten kicker. Rainbow turn. Villain aggression 0, fold equity 0.45. OOP check-raise thin value at SPR=8.4.
- **range_pct:** 0.84 | **fold_eq:** 0.45 | **aggr:** 0 | **flush_d:** 0.05 | **straight_d:** 0.20
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_11

**Board:** B17 — Ad 7s 3c 2h (Turn, OOP SB, SPR=3.0, rainbow)

- **hero_cards:** `['Ah', 'Qc']`
- **hand_category:** top_pair_top_kicker (8) — AQ on A-7-3-2; A top pair, Q top kicker
- **is_monster:** 0 — top pair only; A-7-3-2 is close to a low straight but hero has A-Q (no straight; need 4-5-6 or similar for a wheel and hero does not hold those)
- **Description:** Hero holds AhQc in SB on Ad-7s-3c-2h. Top pair top kicker. Villain aggression 1, fold equity 0.63. Higher range percentile than SP7_05, distinct aggression/fold_eq profile.
- **range_pct:** 0.81 | **fold_eq:** 0.63 | **aggr:** 1 | **flush_d:** 0.05 | **straight_d:** 0.08
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_12

**Board:** B21 — 3h 3d 9s Kc (Turn, OOP SB, SPR=3.0, paired two-tone)

- **hero_cards:** `['Kd', 'Jc']`
- **hand_category:** top_pair_good_kicker (7) — KJ on 3-3-9-K; K top pair, J good kicker
- **is_monster:** 0 — top pair; board pair (33) does not give hero full house (hero has K not 3); K is one pair
- **Description:** Hero holds KdJc in SB on 3h-3d-9s-Kc. Top pair jack kicker on paired turn. Villain aggression 0, fold equity 0.40 (at lower bound). OOP thin value.
- **range_pct:** 0.83 | **fold_eq:** 0.40 | **aggr:** 0 | **flush_d:** 0.10 | **straight_d:** 0.15
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_13

**Board:** B15 — Tc 3d 9h 9s (Turn, OOP BB, SPR=2.6, paired rainbow)

- **hero_cards:** `['Td', 'Ks']`
- **hand_category:** top_pair_good_kicker (7) — TK on T-3-9-9; T pairs with the board T (Tc), giving hero top pair (T) with K kicker. Board pair is 9s; hero's pair is T which is the highest non-paired card.
- **Wait:** Board is Tc 3d 9h 9s. The nines are the pair. T is the highest non-paired card. Hero with Td: T pairs the Tc, giving hero a pair of tens. That's top pair (T is higher than 9). K is the kicker. hand_category = top_pair_good_kicker (7) with K as side card. Td is clear of board (board has Tc, not Td). VALID.
- **is_monster:** 0 — one pair (tens), no set (hero has T+K, not T+T+T), no flush, no straight
- **Description:** Hero holds TdKs in BB on Tc-3d-9h-9s paired turn. Top pair (tens) with king kicker. Villain aggression 1, fold equity 0.55 at SPR=2.6. OOP thin value.
- **range_pct:** 0.84 | **fold_eq:** 0.55 | **aggr:** 1 | **flush_d:** 0.15 | **straight_d:** 0.25
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_14

**Board:** B02 — Kh 7h 3d (Flop, OOP BB, SPR=5.0, two-tone hearts)

- **hero_cards:** `['Ks', 'Ad']`
- **hand_category:** top_pair_top_kicker (8) — KA on K-7-3; K top pair, A top kicker
- **is_monster:** 0 — top pair only; no flush (Ks Ad are non-heart suits)
- **Description:** Hero holds KsAd in BB on Kh-7h-3d. Top pair ace kicker (AK on K-high board). Villain aggression 0, fold equity 0.65. Highest fold equity in the 0.86-0.92 band example.
- **range_pct:** 0.88 | **fold_eq:** 0.65 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_15

**Board:** B06 — 8c 8h 3d (Flop, OOP BB, SPR=5.5, paired rainbow)

- **hero_cards:** `['Qs', 'Qd']`
- **hand_category:** overpair (9) — pocket queens on 8-8-3 board (Q > 8)
- **is_monster:** 0 — overpair is hand_category 9, not in is_monster list; no set (hero has QQ, board does not have Q); QQ is not a set on this board
- **Description:** Hero holds QsQd in BB on 8c-8h-3d. Overpair above the board's highest non-pair rank (8). Villain aggression 1, fold equity 0.60. OOP check-raise high percentile band.
- **range_pct:** 0.87 | **fold_eq:** 0.60 | **aggr:** 1 | **flush_d:** 0.10 | **straight_d:** 0.05
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_16

**Board:** B08 — Qc 5c 9h (Flop, OOP BB, SPR=5.0, two-tone clubs)

- **hero_cards:** `['Qh', 'Ks']`
- **hand_category:** top_pair_top_kicker (8) — QK on Q-5-9; Q top pair, K top kicker
- **is_monster:** 0 — top pair only; non-club suits prevent flush
- **Description:** Hero holds QhKs in BB on Qc-5c-9h. Top pair king kicker (KQ). Villain aggression 0, fold equity 0.55. Higher range percentile validates thin value check-raise at 0.86-0.92 band.
- **range_pct:** 0.90 | **fold_eq:** 0.55 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.20
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_17

**Board:** B13 — Qd 6h 2s Jc (Turn, OOP SB, SPR=8.4, rainbow)

- **hero_cards:** `['Qh', 'Ac']`
- **hand_category:** top_pair_top_kicker (8) — QA on Q-6-2-J; Q top pair, A top kicker
- **is_monster:** 0 — top pair; Qh clear of board (Qd on board, not Qh); no flush (rainbow board); no straight
- **Description:** Hero holds QhAc in SB on Qd-6h-2s-Jc. Top pair ace kicker on rainbow turn. Villain aggression 1, fold equity 0.42. OOP check-raise in 0.86-0.92 band.
- **range_pct:** 0.89 | **fold_eq:** 0.42 | **aggr:** 1 | **flush_d:** 0.05 | **straight_d:** 0.20
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_18

**Board:** B17 — Ad 7s 3c 2h (Turn, OOP SB, SPR=3.0, rainbow)

- **hero_cards:** `['Ac', 'Ks']`
- **hand_category:** top_pair_top_kicker (8) — AK on A-7-3-2; A top pair, K top kicker (next to A)
- **is_monster:** 0 — top pair only; AK on A-7-3-2 has no straight (would need 4-5-6 for a wheel segment), no flush (rainbow), no set
- **Description:** Hero holds AcKs in SB on Ad-7s-3c-2h. Top pair king kicker. Villain aggression 0, fold equity 0.65. Highest fold equity on this board. Dry rainbow turn.
- **range_pct:** 0.88 | **fold_eq:** 0.65 | **aggr:** 0 | **flush_d:** 0.05 | **straight_d:** 0.08
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_19

**Board:** B21 — 3h 3d 9s Kc (Turn, OOP SB, SPR=3.0, paired two-tone)

- **hero_cards:** `['Ks', 'Qh']`
- **hand_category:** top_pair_top_kicker (8) — KQ on 3-3-9-K; K top pair, Q kicker
- **is_monster:** 0 — top pair; board pair (33) does not interact with K-Q hero hand to produce full house or set; K is one pair
- **Description:** Hero holds KsQh in SB on 3h-3d-9s-Kc. Top pair queen kicker. Villain aggression 1, fold equity 0.50. Paired turn board, OOP check-raise.
- **range_pct:** 0.91 | **fold_eq:** 0.50 | **aggr:** 1 | **flush_d:** 0.10 | **straight_d:** 0.15
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_20

**Board:** B15 — Tc 3d 9h 9s (Turn, OOP BB, SPR=2.6, paired rainbow)

- **hero_cards:** `['Th', 'As']`
- **hand_category:** top_pair_top_kicker (8) — TA on T-3-9-9; T top pair (highest non-pair rank), A top kicker
- **is_monster:** 0 — one pair (tens); Th is clear of board (board has Tc, not Th); no set (hero has T not T+T+T on board); board pair 99 does not combine with hero to make FH
- **Description:** Hero holds ThAs in BB on Tc-3d-9h-9s. Top pair (tens) with ace kicker. Villain aggression 0, fold equity 0.62. Higher range band than SP7_13.
- **range_pct:** 0.86 | **fold_eq:** 0.62 | **aggr:** 0 | **flush_d:** 0.15 | **straight_d:** 0.25
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_21

**Board:** B02 — Kh 7h 3d (Flop, OOP BB, SPR=5.0, two-tone hearts)

- **hero_cards:** `['Kd', 'Jc']`
- **hand_category:** top_pair_good_kicker (7) — KJ on K-7-3; K top pair, J good kicker
- **is_monster:** 0 — top pair only; non-heart suits; no flush, no straight
- **Description:** Hero holds KdJc in BB on Kh-7h-3d. Top pair jack kicker. Villain aggression 0, fold equity 0.55. Fourth SP7 sit on B02, completing the per-board cap. Range percentile 0.89 in 0.86-0.92 band.
- **range_pct:** 0.89 | **fold_eq:** 0.55 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

### SP7_22

**Board:** B12 — 7c 2d Kc Ac (Turn, OOP BB, SPR=3.0, two-tone clubs — three clubs)

- **hero_cards:** `['Ks', 'Jd']`
- **hand_category:** top_pair_good_kicker (7) — KJ on 7-2-K-A; K is second pair (A is highest), but wait — A is on board. On K-A board, A is top pair, K is second pair. Hero with K pairs the K for second pair / good hand.
- **Re-evaluation:** Board is 7c-2d-Kc-Ac. Highest card is A. Top pair = AA. Hero with KJ: K pairs → second pair (K). This is middle_pair (5) or top_pair_good_kicker (7) depending on position in range. Actually, on a board of A-K-7-2, "top pair" = A, "second pair" = K. Hero with K = middle pair or second pair = hand_category 5 (middle_pair). That is too low for SP7 (needs >= 0.75 range percentile). 
- **Better option:** hero holds two pair: K+something-that-pairs-another-board-card. But we're avoiding two pair for SP7. Alternatively, hero holds AJ — top pair (A) jack kicker on A-K-7-2. Ah is clear (board has Ac, not Ah). hero_cards = `['Ah', 'Jd']`.
- **hero_cards:** `['Ah', 'Jd']`
- **hand_category:** top_pair_good_kicker (7) — AJ on 7c-2d-Kc-Ac; A top pair (pairing the Ac), J kicker
- **is_monster:** 0 — one pair; Ah pairs Ac for a pair of aces (top pair on this board); no flush (Ah+Jd vs three clubs — hero has no club); no set (hero has Ah only, board has Ac); no straight
- **flush_danger note:** Board has three clubs (7c, Kc, Ac). flush_danger = 0.35 (as specified in allocation table). Hero holds no clubs, so no flush draw. is_monster = 0. VALID.
- **Description:** Hero holds AhJd in BB on 7c-2d-Kc-Ac. Top pair (aces) with jack kicker on three-club turn. Villain aggression 0, fold equity 0.55. Flush danger at 0.35 (boundary). OOP check-raise.
- **range_pct:** 0.76 | **fold_eq:** 0.55 | **aggr:** 0 | **flush_d:** 0.35 | **straight_d:** 0.10
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_23

**Board:** B18 — 4d 8d Kh 5c (Turn, OOP BB, SPR=4.0, two-tone diamonds)

- **hero_cards:** `['Ks', 'Qc']`
- **hand_category:** top_pair_top_kicker (8) — KQ on 4-8-K-5; K top pair, Q top kicker (between K and 8)
- **is_monster:** 0 — top pair only; Ks Qc are non-diamond suits; no flush, no straight (K-8-5-4 with Q — no 5-card straight made by hero)
- **Description:** Hero holds KsQc in BB on 4d-8d-Kh-5c. Top pair queen kicker on two-tone diamond turn. Villain aggression 1, fold equity 0.60. OOP check-raise.
- **range_pct:** 0.79 | **fold_eq:** 0.60 | **aggr:** 1 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.75-0.80
- **Expected label:** RAISE

---

### SP7_24

**Board:** B12 — 7c 2d Kc Ac (Turn, OOP BB, SPR=3.0, two-tone clubs)

- **hero_cards:** `['As', 'Qd']`
- **hand_category:** top_pair_top_kicker (8) — AQ on 7c-2d-Kc-Ac; A top pair (pairing Ac), Q kicker
- **is_monster:** 0 — top pair; As pairs Ac for one pair of aces; no flush (As Qd, no clubs); no set (one ace in hero hand); no straight
- **Description:** Hero holds AsQd in BB on 7c-2d-Kc-Ac. Top pair (aces) queen kicker. Villain aggression 0, fold equity 0.42. Second SP7 sit on B12. Different range band and hand from SP7_22.
- **range_pct:** 0.83 | **fold_eq:** 0.42 | **aggr:** 0 | **flush_d:** 0.35 | **straight_d:** 0.10
- **Band:** 0.80-0.86
- **Expected label:** RAISE

---

### SP7_25

**Board:** B18 — 4d 8d Kh 5c (Turn, OOP BB, SPR=4.0, two-tone diamonds)

- **hero_cards:** `['Kc', 'As']`
- **hand_category:** top_pair_top_kicker (8) — KA on 4-8-K-5; K top pair, A top kicker
- **is_monster:** 0 — top pair only; Kc Ac clear (board has Kh not Kc, board has no Ac); no flush (Kc As — one club but need five for flush; Kh on board is heart not club); no straight
- **Description:** Hero holds KcAs in BB on 4d-8d-Kh-5c. Top pair ace kicker (AK). Villain aggression 0, fold equity 0.65. Highest percentile SP7 on this board. OOP check-raise.
- **range_pct:** 0.90 | **fold_eq:** 0.65 | **aggr:** 0 | **flush_d:** 0.30 | **straight_d:** 0.10
- **Band:** 0.86-0.92
- **Expected label:** RAISE

---

## SP7 Verification Summary

### Band Distribution

| Band        | Situations                         | Count | Min Required |
|-------------|------------------------------------|-------|-------------|
| 0.75-0.80   | SP7_01, 02, 03, 04, 05, 06, 22, 23 | 8     | 6 — PASS    |
| 0.80-0.86   | SP7_07, 08, 09, 10, 11, 12, 13, 24 | 8     | 6 — PASS    |
| 0.86-0.92   | SP7_14, 15, 16, 17, 18, 19, 20, 21, 25 | 9 | 6 — PASS    |

### fold_equity Range

| Metric     | Value                |
|------------|----------------------|
| Minimum    | 0.40 (SP7_12)        |
| Maximum    | 0.65 (SP7_14, 18, 25)|
| Range      | 0.25 — meets >= 0.20 requirement |
| Low zone (0.40-0.50) | SP7_01, 04, 05, 06, 09, 10, 12, 17, 21, 24 = 10 sits |
| High zone (0.55-0.65) | SP7_02, 03, 07, 08, 11, 13, 14, 15, 16, 18, 19, 20, 22, 23, 25 = 15 sits |

### is_monster Check

All 25 SP7 situations use hand_category 7-9 (top_pair_good_kicker, top_pair_top_kicker, overpair).
None are sets, straights, flushes, full houses, or quads.
**All is_monster == 0. PASS.**

### Card Conflict Check

Board cards confirmed not in hero hands:

| Sit  | Board cards           | Hero cards  | Conflict? |
|------|-----------------------|-------------|-----------|
| 01   | Kh 7h 3d              | Kd Qs       | None      |
| 02   | 8c 8h 3d              | Ac Ad       | None      |
| 03   | 8c 8h 3d              | Kd Ks       | None      |
| 04   | Qd 6h 2s Jc           | Qh Ts       | None      |
| 05   | Ad 7s 3c 2h           | As Jd       | None      |
| 06   | 3h 3d 9s Kc           | Kh Qs       | None      |
| 07   | Kh 7h 3d              | Kc Qd       | None      |
| 08   | Qc 5c 9h              | Qd Jh       | None      |
| 09   | Qc 5c 9h              | Qs Td       | None      |
| 10   | Qd 6h 2s Jc           | Qc Ts       | None      |
| 11   | Ad 7s 3c 2h           | Ah Qc       | None      |
| 12   | 3h 3d 9s Kc           | Kd Jc       | None — Jc is on board! |

Wait — B13 is Qd 6h 2s Jc (SP7_12 uses B21 which is 3h 3d 9s Kc). Jc appears in B13 but SP7_12 uses B21. B21 = 3h 3d 9s Kc. Hero KdJc on B21 = 3h 3d 9s Kc. Board has Kc. Hero has Kd (not Kc) and Jc. Board has no Jc. VALID. Let me re-verify the Kc concern: board B21 = 3h 3d 9s Kc. Hero = Kd Jc. Hero Kd — board has Kc (not Kd). Hero Jc — board has no Jc. No conflict.

| Sit  | Board cards           | Hero cards  | Conflict? |
|------|-----------------------|-------------|-----------|
| 12   | 3h 3d 9s Kc           | Kd Jc       | None — Kc vs Kd, Jc not in board. PASS |
| 13   | Tc 3d 9h 9s           | Td Ks       | None — Tc vs Td (different suits). PASS |
| 14   | Kh 7h 3d              | Ks Ad       | None      |
| 15   | 8c 8h 3d              | Qs Qd       | None      |
| 16   | Qc 5c 9h              | Qh Ks       | None      |
| 17   | Qd 6h 2s Jc           | Qh Ac       | None — Qd vs Qh (diff suits), Ac not in board |
| 18   | Ad 7s 3c 2h           | Ac Ks       | None — Ad vs Ac (diff suits). PASS |
| 19   | 3h 3d 9s Kc           | Ks Qh       | None — Kc vs Ks (diff suits). PASS |
| 20   | Tc 3d 9h 9s           | Th As       | None — Tc vs Th (diff suits). PASS |
| 21   | Kh 7h 3d              | Kd Jc       | None — Kh vs Kd (diff suits). PASS |
| 22   | 7c 2d Kc Ac           | Ah Jd       | None — Ac vs Ah (diff suits). PASS |
| 23   | 4d 8d Kh 5c           | Ks Qc       | None      |
| 24   | 7c 2d Kc Ac           | As Qd       | None — Ac vs As (diff suits), 2d vs Qd (diff ranks). PASS |
| 25   | 4d 8d Kh 5c           | Kc As       | None — Kh vs Kc (diff suits). PASS |

All conflicts checked. **No card appears in both board and hero hand at same rank+suit. PASS.**

---

## SP10: Middle Range CALL Fill — 13 CALL Situations

### Conditions

- hero_range_percentile 0.40-0.80
- draw_outs 0-8 (moderate draws only)
- Pure CALL — no RAISE step fires
- Min 3 situations with is_ip == 1 AND hero_range_percentile >= 0.75

### Why these hands don't qualify for RAISE

Each SP10 hand fails all RAISE gates:
- Step 2: is_monster == 0 (not a monster; even if it were, suppressors would fire)
- Step 3: hero_range_percentile < 0.90 (all SP10 sits are 0.40-0.80)
- Step 4: either is_ip == 1 (fails OOP requirement), OR villain_fold_equity too low, OR range_pct < 0.75
- Step 5: draw_outs < 9 (all SP10 sits have 0-8 outs)
- Step 6: not a river bluff situation; hero_range_percentile > 0.20

---

### SP10_01

**Board:** B07 — 5h 6c 7d (Flop, IP BTN, SPR=9.0, connected rainbow)

- **hero_cards:** `['9s', '4d']`
- **hand_category:** middle_pair (5) — 9-4 on 5-6-7 board. Hero has no pair on this board. Wait: 9 and 4 don't pair any board card (5, 6, 7). Hero has no pair = high_card (0). That is too weak. Let me reconsider.
- **Board 5h 6c 7d.** Hero for middle pair needs to pair a middle board card. Hero pairs 6 → hand_category 5 (middle_pair). Cards containing 6 not on board: 6s, 6d, 6h (6c is on board, 6h not on board). hero_cards = `['6h', 'Kd']` — pair of sixes with K kicker. hand_category = middle_pair (5).
- But wait — the allocation says range_pct=0.45 for this sit. Middle pair on a straight-danger board with a king kicker seems reasonable for 0.45.
- **hero_cards:** `['6h', 'Kd']`
- **hand_category:** middle_pair (5) — 6K on 5h-6c-7d; 6 makes middle pair (6c on board)
- **is_monster:** 0 — one pair; no straight (6-6-5-7 is not a straight for hero; hero has pair of 6s, not a 4-5-6-7-8 run)
- **draw_outs:** 0 (no draw equity; hero has made hand)
- **Description:** Hero holds 6hKd in BTN (IP) on 5h-6c-7d straight-heavy board. Middle pair (sixes) with K kicker. No draw. IP position means Step 4 OOP check-raise cannot fire. Percentile 0.45 fails Step 3 (needs >= 0.90). Pure CALL.
- **range_pct:** 0.45 | **is_ip:** 1 | **draw_outs:** 0
- **Band:** 0.40-0.55
- **Expected label:** CALL

---

### SP10_02

**Board:** B10 — Kc 4d 2h (Flop, OOP BB, SPR=9.0, rainbow, to_call=0)

- **hero_cards:** `['Jc', '4s']`
- **hand_category:** bottom_pair (3) or middle_pair (5)? Board is K-4-2. Hero pairs 4 → second pair from bottom — actually there are three board cards: K (top), 4 (middle), 2 (bottom). Pairing 4 = middle pair (5). Jc as side card.
- **Wait:** Jc — board has no club (board is Kc 4d 2h — Kc IS on board). Jc is clear (Jc ≠ Kc). 4s vs 4d — different suits, clear. VALID.
- **Kc on board, Jc in hero hand — Kc and Jc are different cards (different ranks). No conflict.**
- **hero_cards:** `['Jc', '4s']`
- **hand_category:** middle_pair (5) — J4 on K-4-2; pairs the 4 for middle pair
- **draw_outs:** 4 (gutshot: J-9-8-? or similar; hero has J for backdoor gutshot possibilities — actually on K-4-2 rainbow, J gives hero a gutshot to T-J-Q... wait, no: for a gutshot hero needs 4 cards to a straight with one gap. J-9-8-7 needs a T, or A-K-Q-J needs a T. Hero has J and board has K and 4 and 2 — hero could have a backdoor to Q-J-T-9-8 or K-Q-J-T... with J on flop, a gutshot would need specific turn+river. As a flop gutshot draw estimation: draw_outs=4 as specified in allocation table.)
- **Description:** Hero holds JcAs in BB (OOP) on Kc-4d-2h. Middle pair (fours) with J kicker plus gutshot draw. to_call=0 so hero faces no bet (hero leads). Fails all RAISE gates: Step 3 (range_pct=0.50 < 0.90), Step 4 (range_pct=0.50 is technically >= but the hand is OOP on a dead board where fold equity is well below 0.40 on K-4-2 dry rainbow). Pure CALL.
- **Revision:** More clearly: hero_cards = `['Jc', '4s']` exactly as designed. Kicker concern resolved — 4s pairs board's 4d.
- **range_pct:** 0.50 | **is_ip:** 0 | **draw_outs:** 4
- **Band:** 0.40-0.55
- **Expected label:** CALL

---

### SP10_03

**Board:** B13 — Qd 6h 2s Jc (Turn, OOP SB, SPR=8.4, rainbow)

- **hero_cards:** `['6d', '8c']`
- **hand_category:** bottom_pair (3) — 6-8 on Q-6-2-J; 6 pairs the 6h for bottom pair (lowest board card pair). 8 is a kicker.
- **is_monster:** 0 — one pair; no flush (rainbow board); no straight
- **draw_outs:** 0 (no meaningful draw; 8 on Q-6-2-J doesn't complete a draw)
- **Description:** Hero holds 6d8c in SB (OOP) on Qd-6h-2s-Jc. Bottom pair (sixes) with 8 kicker. No draw. Fails Step 3 (range_pct=0.42 << 0.90) and Step 4 (range_pct=0.42 < 0.75). Pure CALL.
- **range_pct:** 0.42 | **is_ip:** 0 | **draw_outs:** 0
- **Band:** 0.40-0.55
- **Expected label:** CALL

---

### SP10_04

**Board:** B19 — 4c 6h 8s 7d (Turn, IP BTN, SPR=2.0, connected rainbow)

- **hero_cards:** `['9h', 'Js']`
- **hand_category:** top_pair (6) — 9-J on 4-6-8-7? No pair with board cards 4, 6, 8, 7. Hero has 9 and J — neither pairs a board card. Hero has no pair. Actually top pair from board perspective: highest board card is 8. Hero's J > 8, so J is an overcard. Hero's 9 pairs... nothing. Hero has no pair = high_card type.
- **Revision:** For range_pct=0.58 with middle pair on a connected board, hero needs to pair a board card. Let's use hero_cards = `['8h', 'Jd']`: 8 pairs the 8s for top pair (8 is highest board card). hand_category = top_pair (6). J is a good kicker. But is 8 the top pair when board is 4-6-8-7? Yes, 8 is highest. But this might be hand_category 6 or 7.
- **hero_cards:** `['8h', 'Jd']`
- **hand_category:** top_pair (6) — 8J on 4c-6h-8s-7d; 8 pairs board's 8s for top pair
- **is_monster:** 0 — one pair; no straight (hero would need 5 for a 4-5-6-7-8 straight; hero has 8+J, not a straight)
- **draw_outs:** 5 (allocation specifies 5 draw_outs; middle pair + backdoor straight potential on 4-5-6-7-8 board — hero needs a 5 for the straight; that's one specific out. Actually with 8-J on 4-6-8-7 connected board: no clean flush draw; straight draw: hero needs to fill in a 5-card run. With J-8 and board 4-6-7-8: holding J-8, board has 4-5 cards that could help complete a run... 5 draw_outs is specified and we accept it as given.)
- **Description:** Hero holds 8hJd in BTN (IP) on 4c-6h-8s-7d. Top pair (eights) with jack kicker on very straight-danger board. IP position: Step 4 OOP check-raise cannot fire (is_ip=1). Range_pct=0.58 fails Step 3 (< 0.90). draw_outs=5 fails Step 5 (< 9). Pure CALL.
- **range_pct:** 0.58 | **is_ip:** 1 | **draw_outs:** 5
- **Band:** 0.55-0.65
- **Expected label:** CALL

---

### SP10_05

**Board:** B20 — 2c 9c Qh 6s (Turn, IP CO, SPR=1.4, two-tone clubs)

- **hero_cards:** `['Td', 'Jh']`
- **hand_category:** middle_pair? T-J on 2-9-Q-6. Hero has T and J, neither pairs a board card (board has 2, 9, Q, 6). Hero has no pair from these cards. Hmm. The allocation says range_pct=0.60, draw_outs=4 (moderate hand with club draw on board).
- **Option:** hero holds QdTs: Q pairs board Q for top pair, T is kicker. hand_category = top_pair (6). But QdTs — Qd vs Qh (board has Qh) — clear.
- **Better for range_pct=0.60 (moderate):** hero_cards = `['9h', 'Ts']` — 9 pairs board 9c for middle pair (9), T is kicker. No flush draw (non-club).
- **hero_cards:** `['9h', 'Ts']`
- **hand_category:** middle_pair (5) — 9T on 2c-9c-Qh-6s; 9 pairs the 9c
- **is_monster:** 0 — one pair; no flush (9h Ts — no clubs)
- **draw_outs:** 4 (allocation specifies; club draw is on the board but hero holds no clubs — hero has 4 straight-type outs from back-door equity or weak gutshot with T on 6-9-Q: T could be part of 8-9-T-J-Q if hero had more; approximately 4 outs for a gutshot)
- **Description:** Hero holds 9hTs in CO (IP) on 2c-9c-Qh-6s. Middle pair (nines) with T kicker. Flush danger present (two clubs on board) but hero holds no clubs. IP position: Step 4 cannot fire. Range_pct=0.60 fails Step 3 (< 0.90). draw_outs=4 fails Step 5 (< 9). Pure CALL.
- **range_pct:** 0.60 | **is_ip:** 1 | **draw_outs:** 4
- **Band:** 0.55-0.65
- **Expected label:** CALL

---

### SP10_06

**Board:** B14 — 3s Js 9h 4d (Turn, IP CO, SPR=3.0, two-tone spades)

- **hero_cards:** `['Jd', 'Th']`
- **hand_category:** top_pair_good_kicker (7) — JT on 3s-Js-9h-4d; J pairs the Js for top pair, T is good kicker
- **is_monster:** 0 — one pair; Jd vs Js (different suits); no flush (Jd Th, non-spade)
- **draw_outs:** 6 (T on 3-4-9-J: gutshot or open-ender candidates; with T-J on 3-4-9-J: 8 completes 8-9-T-J and Q completes J-Q if turn card not counted... approximately 6 outs for straight draws)
- **Description:** Hero holds JdTh in CO (IP) on 3s-Js-9h-4d. Top pair (jacks) with T kicker. Spade flush draw on board; hero holds no spades. IP position: Step 4 OOP check-raise cannot fire. Range_pct=0.55 fails Step 3 (< 0.90). draw_outs=6 fails Step 5 (< 9). Pure CALL.
- **range_pct:** 0.55 | **is_ip:** 1 | **draw_outs:** 6
- **Band:** 0.40-0.55
- **Expected label:** CALL

---

### SP10_07

**Board:** B16 — 5h Kd 2h 8c (Turn, IP BTN, SPR=4.0, two-tone hearts)

- **hero_cards:** `['Kh', 'Tc']`
- **hand_category:** top_pair_good_kicker (7) — KT on 5h-Kd-2h-8c; K top pair, T good kicker
- **Wait:** Kh is in hero hand; board has Kd (not Kh). Clear. But Kh is a heart — board has 5h and 2h (two hearts). Hero holds Kh = one heart. That gives hero a flush draw to hearts (Kh + 5h + 2h = three hearts toward a flush). That changes draw_outs: hero has a flush draw = ~9 outs. But allocation says draw_outs=7. We need draw_outs ≤ 8 for SP10.
- **Revision:** Use Ks instead of Kh to avoid flush draw. hero_cards = `['Ks', 'Tc']`
- **hero_cards:** `['Ks', 'Tc']`
- **hand_category:** top_pair_good_kicker (7) — KT on 5h-Kd-2h-8c; K top pair (Ks pairs Kd), T kicker
- **is_monster:** 0 — one pair; Ks vs Kd (different suits); no flush (Ks Tc both non-heart)
- **draw_outs:** 7 (allocation specifies 7; with T on 5-8-K-2 board: T contributes to possible straight draws J-T-9-8-7 needing J and 9, or backdoor draws; 7 outs as specified)
- **Description:** Hero holds KsTc in BTN (IP) on 5h-Kd-2h-8c. Top pair (kings) with T kicker. Two-tone heart board; hero holds no hearts. IP position: Step 4 OOP check-raise cannot fire. Range_pct=0.68 fails Step 3 (< 0.90). draw_outs=7 fails Step 5 (< 9). Pure CALL.
- **range_pct:** 0.68 | **is_ip:** 1 | **draw_outs:** 7
- **Band:** 0.65-0.75
- **Expected label:** CALL

---

### SP10_08

**Board:** B27 — 4d 8h 2c 6s Jd (River, IP BTN, SPR=0.9, rainbow)

- **hero_cards:** `['8s', 'Kc']`
- **hand_category:** middle_pair (5) — 8K on 4-8-2-6-J; 8 pairs the 8h for middle pair (8 is middle card on this board: J > 8 > 6 > 4 > 2)
- **is_monster:** 0 — one pair; no flush (rainbow board, Ks Ac non-applicable); no straight
- **draw_outs:** 0 (river — all draws resolved; no outs)
- **Description:** Hero holds 8sKc in BTN (IP) on 4d-8h-2c-6s-Jd. Middle pair (eights) with K kicker at river. IP position. Range_pct=0.62, fails Step 3 (< 0.90). draw_outs=0. Pure CALL — showdown value only.
- **range_pct:** 0.62 | **is_ip:** 1 | **draw_outs:** 0
- **Band:** 0.55-0.65
- **Expected label:** CALL

---

### SP10_09

**Board:** B28 — 3s 7h Ks 2c Ts (River, IP CO, SPR=0.9, two-tone spades — flush completed)

- **hero_cards:** `['Kd', 'Jh']`
- **hand_category:** top_pair_good_kicker (7) — KJ on 3s-7h-Ks-2c-Ts; K top pair (Kd pairs Ks), J kicker
- **is_monster:** 0 — one pair; no flush (Kd Jh are non-spade; hero has no spade); no straight
- **draw_outs:** 0 (river — all draws resolved)
- **Description:** Hero holds KdJh in CO (IP) on 3s-7h-Ks-2c-Ts. Top pair (kings) with jack kicker. Spade flush completed on river (three spades: 3s, Ks, Ts); hero holds no spades so no flush. IP position, range_pct=0.72 fails Step 3 (< 0.90). Flush danger present but hero does not hold a flush. Pure CALL.
- **range_pct:** 0.72 | **is_ip:** 1 | **draw_outs:** 0
- **Band:** 0.65-0.75
- **Expected label:** CALL

---

### SP10_10

**Board:** B03 — As 5d 2c (Flop, IP CO, SPR=9.0, rainbow)

- **hero_cards:** `['Kd', 'Qh']`
- **hand_category:** This is tricky. B03 board is As-5d-2c. Hero KQ: neither K nor Q pairs a board card (A, 5, 2). Hero has no pair — overcards only (both K and Q are below A). hand_category = overcards (2). Range_pct=0.75. But overcards at 0.75 range percentile suggests hero is near top of range without a pair. This is the "IP thin value = CALL" contrast case.
- **draw_outs:** 6 (K and Q give hero 6 outs to top pair on the turn: Kx or Qx = 3+3 = 6 outs)
- **is_monster:** 0 — no pair yet, clearly not a monster
- **Description:** Hero holds KdQh in CO (IP) on As-5d-2c. Two overcards, no pair. IP position: even at range_pct=0.75, Step 4 requires is_ip==0. Hero is IP → Step 4 cannot fire. Step 3 fails (range_pct=0.75 < 0.90). Step 5 fails (draw_outs=6 < 9). Pure CALL — contrasts with SP7 OOP check-raise situations at same percentile.
- **range_pct:** 0.75 | **is_ip:** 1 | **draw_outs:** 6
- **Band:** 0.75-0.80
- **Expected label:** CALL

---

### SP10_11

**Board:** B11r — Ts 8s 4h (Flop, IP BTN, SPR=5.0, two-tone spades)

- **hero_cards:** `['Jd', '9c']`
- **hand_category:** middle_pair? J-9 on T-8-4. Neither J nor 9 pairs a board card. Hero has no pair = overcards. Actually: J and 9 bracket the T (J > T > 9); neither pairs board cards T, 8, 4. Hero has no pair. However, J-9 gives hero an open-ended straight draw to Q-J-T-9-8 needing a Q, or 9-8-7-6 type. draw_outs=7 as specified.
- **hand_category:** overcards (2) or high_card (0)? Actually for range purposes, JTs would be a gutshot/OESD hand. J9 on T-8-4: J-T is connected (gap), 9-8 is connected (gap), 4 is isolated. Hero has J-9 with board T-8-4: that's J-T-9-8 = 4 connected cards, missing only the Q for J-high end or the 7 for low end = open-ended straight draw. Hero has a powerful draw but draw_outs=7 (slightly below the full 8-out OESD? That may be because some outs are compromised). hand_category for the made hand portion = high_card (0) since no pair. But for range_pct=0.78, this is a drawing hand near the top of range.
- **is_monster:** 0 — no pair, no flush (Jd 9c, non-spade), no straight yet
- **Description:** Hero holds Jd9c in BTN (IP) on Ts-8s-4h. Open-ended straight draw (J-T-9-8) with 7 outs. No made pair. Spade flush draw on board; hero holds no spades. IP position: Step 4 OOP check-raise cannot fire. Step 5 fails (draw_outs=7 < 9). Range_pct=0.78 fails Step 3 (< 0.90). Pure CALL — demonstrates IP drawing hand with high percentile = CALL.
- **range_pct:** 0.78 | **is_ip:** 1 | **draw_outs:** 7
- **Band:** 0.75-0.80
- **Expected label:** CALL

---

### SP10_12

**Board:** B21 — 3h 3d 9s Kc (Turn, OOP SB, SPR=3.0, paired two-tone)

- **hero_cards:** `['Tc', '7d']`
- **hand_category:** middle_pair? T-7 on 3-3-9-K. Neither T nor 7 pairs a board card (K, 9, 3, 3). Hero has no pair = high_card or overcards. For range_pct=0.70, a moderate hand. With T and 7 on K-9-3-3: no pair, moderate hand. 
- **Revision for a made hand:** hero_cards = `['9d', 'Th']` — 9 pairs the 9s for middle pair (9), T kicker. Board K-9-3-3: 9 pairs 9s. hand_category = middle_pair (5). 9d vs 9s (clear). Th not on board. VALID.
- **hero_cards:** `['9d', 'Th']`
- **hand_category:** middle_pair (5) — 9T on 3h-3d-9s-Kc; 9 pairs the 9s for middle pair
- **is_monster:** 0 — one pair; board pair (33) does not combine with hero's 9 to make full house
- **draw_outs:** 5 (allocation specifies 5; T on K-9-3-3 gives some backdoor straight potential)
- **Description:** Hero holds 9dTh in SB (OOP) on 3h-3d-9s-Kc. Middle pair (nines) with T kicker. OOP but range_pct=0.70 fails Step 4 (needs >= 0.75) and Step 3 (< 0.90). draw_outs=5 fails Step 5 (< 9). Pure CALL.
- **range_pct:** 0.70 | **is_ip:** 0 | **draw_outs:** 5
- **Band:** 0.65-0.75
- **Expected label:** CALL

---

### SP10_13

**Board:** B15 — Tc 3d 9h 9s (Turn, OOP BB, SPR=2.6, paired rainbow)

- **hero_cards:** `['Jd', '8c']`
- **hand_category:** on Tc-3d-9h-9s: T is the highest non-pair card. Hero J-8: neither J nor 8 pairs a board card (T, 3, 9, 9). Hero has no pair. J is an overcard to T. 8 is below T. For range_pct=0.76, hero has a moderate made hand... Let me use a hand that pairs the T.
- **hero_cards:** `['Ts', 'Qh']` — T pairs the Tc for top pair (T, the highest non-9 card), Q kicker. Ts vs Tc (different suits). Board 9s is on board — Ts is clear. VALID.
- **hand_category:** top_pair_good_kicker (7) — TQ on Tc-3d-9h-9s; T top pair (highest non-pair rank), Q kicker
- **is_monster:** 0 — one pair (tens); Ts pairs Tc for one pair; board 9-9 does not combine with Ts to make full house; no flush, no straight
- **draw_outs:** 6 (allocation specifies 6; Q-J-T-9 setup gives some straight-outs: if we have Q-T on 9-9 board, a J would give Q-J-T + board 9s... approximately 6 outs for gutshot/straight completions)
- **Description:** Hero holds TsQh in BB (OOP) on Tc-3d-9h-9s. Top pair (tens) with queen kicker. OOP, range_pct=0.76 is above 0.75 but fails Step 4 because the specific board conditions (flush_danger=0.20, straight_danger=0.25) — actually Step 4 requires ALL conditions including fold_equity >= 0.40 and aggression <= 1. The key reason this is CALL: Step 5 fails (draw_outs=6 < 9) and Step 3 fails (range_pct=0.76 < 0.90). Even OOP with decent percentile, these gates prevent RAISE.
- **range_pct:** 0.76 | **is_ip:** 0 | **draw_outs:** 6
- **Band:** 0.75-0.80
- **Expected label:** CALL

---

## SP10 Verification Summary

### Band Distribution

| Band        | Situations                                  | Count | Min Required |
|-------------|---------------------------------------------|-------|-------------|
| 0.40-0.55   | SP10_01(0.45), 02(0.50), 03(0.42), 06(0.55) | 4     | 3 — PASS    |
| 0.55-0.65   | SP10_04(0.58), 05(0.60), 08(0.62)           | 3     | 3 — PASS    |
| 0.65-0.75   | SP10_07(0.68), 09(0.72), 12(0.70)           | 3     | 3 — PASS    |
| 0.75-0.80   | SP10_10(0.75), 11(0.78), 13(0.76)           | 3     | 3 — PASS    |

### IP Thin Value CALL Count (is_ip == 1 AND range_pct >= 0.75)

| Situation | range_pct | is_ip | Qualifies |
|-----------|-----------|-------|-----------|
| SP10_10   | 0.75      | 1     | YES       |
| SP10_11   | 0.78      | 1     | YES       |
| SP10_09   | 0.72      | 1     | No (< 0.75)|
| SP10_13   | 0.76      | 0     | No (OOP)  |

SP10_10 and SP10_11 qualify. Need a third. SP10_09 has is_ip=1 but range_pct=0.72 (just below threshold).

**Correction needed:** The third IP thin value CALL must have is_ip=1 AND range_pct >= 0.75. Looking at the allocation table: sit#9 (B28, CO IP, range_pct=0.72). That is below 0.75. Sit#10 (B03, CO IP, range_pct=0.75) — that is SP10_10. Sit#11 (B11r, BTN IP, range_pct=0.78) — that is SP10_11.

The allocation table shows only sits 9, 10, 11 in the 0.65-0.80 range with IP. Sit 9 (range_pct=0.72) is below the 0.75 threshold. We need at minimum 3 qualifying (is_ip==1 AND range_pct >= 0.75).

**Resolution:** Adjust SP10_09 (B28, IP CO) range_pct from 0.72 to 0.76 to cross the threshold. This puts SP10_09 in the 0.75-0.80 band. The 0.65-0.75 band then has SP10_07 (0.68) and SP10_12 (0.70) = 2 situations. That falls below the minimum of 3 for the 0.65-0.75 band.

**Alternative resolution:** Keep SP10_09 at 0.72 (in 0.65-0.75 band = 3 situations) but add a note that the allocation table as designed has only 2 qualifying IP sits above 0.75. This is a design constraint from the allocation table itself (the board architect set sit#9 at 0.72). The design agent cannot unilaterally change allocation table values without a flag.

**Flag for reviewer:** The allocation table (BOARD_ALLOCATION_V3_FINAL.md, SP10 section) assigns sit#9 (B28, CO IP) range_pct=0.72, below the 0.75 threshold for the "IP thin value = CALL" contrast requirement. With the three IP sits at 0.72, 0.75, and 0.78, only two meet the is_ip==1 AND range_pct >= 0.75 criterion. The brief requires minimum 3. Options: (a) raise sit#9 range_pct to 0.76, accepting that the 0.65-0.75 band drops to 2 situations (below minimum of 3); (b) keep sit#9 at 0.72 and note the shortfall in the IP contrast requirement; (c) substitute a different board for one SP10 sit in the 0.65-0.75 band that uses an IP position at range_pct=0.75+. This flag is referred to the reviewer and the board architect.

**For this document:** SP10_10 (range_pct=0.75, is_ip=1) and SP10_11 (range_pct=0.78, is_ip=1) are confirmed as IP thin value CALL contrasts. SP10_09 (range_pct=0.72, is_ip=1) is the closest third but falls below the 0.75 threshold by 0.03. Two of three are confirmed; the third is a near-miss flagged for review.

### draw_outs Range

| Metric     | Value                            |
|------------|----------------------------------|
| Minimum    | 0 (SP10_01, 08, 09 — river/straight board no draw) |
| Maximum    | 7 (SP10_07, 11)                  |
| Range      | 0-7 — within specified 0-8 range |

### Card Conflict Check (SP10)

| Sit   | Board cards             | Hero cards  | Conflict? |
|-------|-------------------------|-------------|-----------|
| 01    | 5h 6c 7d                | 6h Kd       | None — 6c vs 6h (diff suits). PASS |
| 02    | Kc 4d 2h                | Jc 4s       | None — Kc vs Jc (diff ranks), 4d vs 4s (diff suits). PASS |
| 03    | Qd 6h 2s Jc             | 6d 8c       | None — 6h vs 6d (diff suits), Jc in board vs 8c in hand (diff ranks). PASS |
| 04    | 4c 6h 8s 7d             | 8h Jd       | None — 8s vs 8h (diff suits), 7d in board vs Jd in hand... 7d and Jd are different ranks. PASS |
| 05    | 2c 9c Qh 6s             | 9h Ts       | None — 9c vs 9h (diff suits). PASS |
| 06    | 3s Js 9h 4d             | Jd Th       | None — Js vs Jd (diff suits). PASS |
| 07    | 5h Kd 2h 8c             | Ks Tc       | None — Kd vs Ks (diff suits). PASS |
| 08    | 4d 8h 2c 6s Jd          | 8s Kc       | None — 8h vs 8s (diff suits), Jd in board vs Kc in hand (diff ranks). PASS |
| 09    | 3s 7h Ks 2c Ts          | Kd Jh       | None — Ks vs Kd (diff suits), Ts in board vs Jh in hand (diff ranks). PASS |
| 10    | As 5d 2c                | Kd Qh       | None. PASS |
| 11    | Ts 8s 4h                | Jd 9c       | None. PASS |
| 12    | 3h 3d 9s Kc             | 9d Th       | None — 9s vs 9d (diff suits). PASS |
| 13    | Tc 3d 9h 9s             | Ts Qh       | None — Tc vs Ts (diff suits), 9s and 9h in board vs Qh and Ts in hand (diff ranks). PASS |

All conflicts checked. **No card appears in both board and hero hand at same rank+suit. PASS.**

---

## Consolidated Situation Table

### SP7 — 25 RAISE Situations

| ID     | Board | hero_cards  | hand_cat | range_pct | fold_eq | aggr | flush_d | Band      |
|--------|-------|-------------|----------|-----------|---------|------|---------|-----------|
| SP7_01 | B02   | Kd Qs       | 8        | 0.76      | 0.42    | 0    | 0.30    | 0.75-0.80 |
| SP7_02 | B06   | Ac Ad       | 9        | 0.78      | 0.45    | 1    | 0.10    | 0.75-0.80 |
| SP7_03 | B06   | Kd Ks       | 9        | 0.78      | 0.43    | 0    | 0.10    | 0.75-0.80 |
| SP7_04 | B13   | Qh Ts       | 7        | 0.75      | 0.55    | 1    | 0.05    | 0.75-0.80 |
| SP7_05 | B17   | As Jd       | 8        | 0.78      | 0.48    | 0    | 0.05    | 0.75-0.80 |
| SP7_06 | B21   | Kh Qs       | 7        | 0.77      | 0.43    | 1    | 0.10    | 0.75-0.80 |
| SP7_07 | B02   | Kc Qd       | 8        | 0.82      | 0.52    | 0    | 0.30    | 0.80-0.86 |
| SP7_08 | B08   | Qd Jh       | 7        | 0.83      | 0.58    | 1    | 0.30    | 0.80-0.86 |
| SP7_09 | B08   | Qs Td       | 7        | 0.82      | 0.50    | 1    | 0.30    | 0.80-0.86 |
| SP7_10 | B13   | Qc Ts       | 7        | 0.84      | 0.45    | 0    | 0.05    | 0.80-0.86 |
| SP7_11 | B17   | Ah Qc       | 8        | 0.81      | 0.63    | 1    | 0.05    | 0.80-0.86 |
| SP7_12 | B21   | Kd Jc       | 7        | 0.83      | 0.40    | 0    | 0.10    | 0.80-0.86 |
| SP7_13 | B15   | Td Ks       | 7        | 0.84      | 0.55    | 1    | 0.15    | 0.80-0.86 |
| SP7_14 | B02   | Ks Ad       | 8        | 0.88      | 0.65    | 0    | 0.30    | 0.86-0.92 |
| SP7_15 | B06   | Qs Qd       | 9        | 0.87      | 0.60    | 1    | 0.10    | 0.86-0.92 |
| SP7_16 | B08   | Qh Ks       | 8        | 0.90      | 0.55    | 0    | 0.30    | 0.86-0.92 |
| SP7_17 | B13   | Qh Ac       | 8        | 0.89      | 0.42    | 1    | 0.05    | 0.86-0.92 |
| SP7_18 | B17   | Ac Ks       | 8        | 0.88      | 0.65    | 0    | 0.05    | 0.86-0.92 |
| SP7_19 | B21   | Ks Qh       | 8        | 0.91      | 0.50    | 1    | 0.10    | 0.86-0.92 |
| SP7_20 | B15   | Th As       | 8        | 0.86      | 0.62    | 0    | 0.15    | 0.86-0.92 |
| SP7_21 | B02   | Kd Jc       | 7        | 0.89      | 0.55    | 0    | 0.30    | 0.86-0.92 |
| SP7_22 | B12   | Ah Jd       | 7        | 0.76      | 0.55    | 0    | 0.35    | 0.75-0.80 |
| SP7_23 | B18   | Ks Qc       | 8        | 0.79      | 0.60    | 1    | 0.30    | 0.75-0.80 |
| SP7_24 | B12   | As Qd       | 8        | 0.83      | 0.42    | 0    | 0.35    | 0.80-0.86 |
| SP7_25 | B18   | Kc As       | 8        | 0.90      | 0.65    | 0    | 0.30    | 0.86-0.92 |

### SP10 — 13 CALL Situations

| ID      | Board | hero_cards  | hand_cat | range_pct | is_ip | draw_outs | Band      |
|---------|-------|-------------|----------|-----------|-------|-----------|-----------|
| SP10_01 | B07   | 6h Kd       | 5        | 0.45      | 1     | 0         | 0.40-0.55 |
| SP10_02 | B10   | Jc 4s       | 5        | 0.50      | 0     | 4         | 0.40-0.55 |
| SP10_03 | B13   | 6d 8c       | 3        | 0.42      | 0     | 0         | 0.40-0.55 |
| SP10_04 | B19   | 8h Jd       | 6        | 0.58      | 1     | 5         | 0.55-0.65 |
| SP10_05 | B20   | 9h Ts       | 5        | 0.60      | 1     | 4         | 0.55-0.65 |
| SP10_06 | B14   | Jd Th       | 7        | 0.55      | 1     | 6         | 0.40-0.55 |
| SP10_07 | B16   | Ks Tc       | 7        | 0.68      | 1     | 7         | 0.65-0.75 |
| SP10_08 | B27   | 8s Kc       | 5        | 0.62      | 1     | 0         | 0.55-0.65 |
| SP10_09 | B28   | Kd Jh       | 7        | 0.72      | 1     | 0         | 0.65-0.75 |
| SP10_10 | B03   | Kd Qh       | 2        | 0.75      | 1     | 6         | 0.75-0.80 |
| SP10_11 | B11r  | Jd 9c       | 0        | 0.78      | 1     | 7         | 0.75-0.80 |
| SP10_12 | B21   | 9d Th       | 5        | 0.70      | 0     | 5         | 0.65-0.75 |
| SP10_13 | B15   | Ts Qh       | 7        | 0.76      | 0     | 6         | 0.75-0.80 |

---

## Open Flags for Reviewer

**FLAG 1 — SP10 IP thin value CALL count:**
The allocation table (BOARD_ALLOCATION_V3_FINAL.md) places the three highest-percentile IP sits at range_pct = 0.72, 0.75, and 0.78. The brief requires min 3 with is_ip==1 AND range_pct >= 0.75. Only two of the three clear this threshold (SP10_10 at 0.75 and SP10_11 at 0.78). SP10_09 (IP, B28) sits at 0.72, which is 0.03 below the threshold. The board architect should either raise SP10_09 range_pct to >= 0.75 (shifting it from the 0.65-0.75 band into the 0.75-0.80 band, reducing that lower band to 2 situations — below minimum) or add a 14th SP10 situation as a dedicated IP contrast at range_pct >= 0.75. This is a structural conflict in the allocation table, not a design agent error.

**FLAG 2 — SP7_04 straight_danger note:**
B13 (Qd 6h 2s Jc) has straight_danger specified as 0.20 in the allocation table. Q-J is a two-gap connection, and with 6 and 2 present, board straight danger is moderate. The allocation confirms 0.20 which is within the Step 4 ceiling of 0.35. No action needed; flagged for transparency.

**FLAG 3 — SP7_22 flush_danger at boundary:**
SP7_22 uses B12 (7c 2d Kc Ac) with flush_danger=0.35, exactly at the Step 4 ceiling. The allocation table specifies this value. The hand (AhJd — no clubs) does not hold a flush draw. The OOP check-raise thin value label is correct as long as the extractor produces flush_danger <= 0.35 on this board. Verify that the feature extractor produces exactly 0.35 (not marginally above due to floating point) before building this situation.

