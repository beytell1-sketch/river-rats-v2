---
date: 2026-04-27
from: Architect (Phase 2.7)
to: gto-expert · ml-architect · QC stream · Lead-programmer · Owner
re: Scenario module expansion blueprint v3.5 — fill ~150-record gap across 8 modules
status: BLUEPRINT — for review chain
---

# Scenario Module Expansion Blueprint v3.5

## Allocator overlap correction (critical preamble)

The Phase 5 directive estimated ~80-120 new records via cross-module overlap. This estimate
assumed a record could fill multiple quota slots simultaneously. The F5 allocator does NOT
work that way: each record is assigned to **at most one category** (the highest-scarcity
eligible category at assignment time). `used_fps` prevents any record from counting toward
two quotas.

The genuine overlap mechanism is **overflow**: when a module produces more records than its
own quota gap, the excess — if they also match another category — get assigned to that
second category. Example: 52 new MAGG templates at spr_med-range pots (SPR 2-4):
- 40 records fill MAGG quota (10 existing + 30 new)
- 12 remaining new records are assigned to spr_med (magg full, next eligible = spr_med)

Beyond this one MAGG → spr_med overflow path, no other genuine dual-quota savings exist
under the current allocator. The honest minimum is **146 new records** across 8 modules.
This is documented transparently for the review chain.

---

## Scarcity order at current yields

Scarcity = PHASE_A_QUOTAS[cat] / max(1, current_yield). Higher = more urgent.

| Category   | Target | Current Yield | Scarcity |
|-----------|--------|--------------|---------|
| nfd_raise  | 20     | 4            | 5.00    |
| nfd_call   | 20     | 4            | 5.00    |
| magg       | 40     | 10           | 4.00    |
| bac        | 20     | 9            | 2.22    |
| spr_med    | 40     | 18           | 2.22    |
| pfa        | 80     | 46           | 1.74    |
| donk       | 25     | 15           | 1.67    |
| sb         | 20     | 13           | 1.54    |

Assignment rule: a record matching multiple categories is assigned to the
highest-scarcity category that still has quota remaining.

---

## SPR math reference

SPR = 100 / pot_bb (DEFAULT_EFFECTIVE_STACK = 100 BB).

- spr_med (2.0 ≤ SPR < 4.0): pot range **26 – 50 BB**
- spr_std (SPR ≥ 4.0): pot < 25 BB

All existing MAGG templates use pot 50–80 BB → SPR 1.25–2.0 (below spr_med).
All existing PFA flop templates use pot 14–16 BB → SPR 6.25–7.14 (spr_std).

---

## Module 1 — magg_scenarios.py

### Current state

10 records. All river decisions, villain=BB (preflop caller), hero=CO or BTN opener
(is_preflop_aggressor=1). Pot range 50–80 BB → SPR 1.25–2.0. All records match
{magg, pfa}. All assigned to magg (scarcity 4.0 > pfa 1.74).

Existing boards (5-card river boards):
Kd7s2c5hJd, Qs8h3cTd6s, JhTd4c8s2h, Ah9c4d2sKh, 9h6c2sTd5d,
8s5c2hJd4s, Kc9d3h7sQc, Ah8c4d6s2h, Ks8d3cJh9s, Qd7h2cTc5d

### Target expansion: +52 new records

- **30 records** at pot 50–80 BB (SPR < 2): fill magg quota gap (+30, from 10 to 40).
  These also satisfy {pfa} but get assigned to magg. Pot range deliberately ABOVE spr_med
  to keep all 30 cleanly assigned to magg without leaking to spr_med quota.
- **22 records** at pot 26–45 BB (SPR 2.22–3.85, spr_med range): once magg fills to 40/40,
  these 22 overflow records are assigned to spr_med (next highest scarcity at 2.22).
  Each also satisfies {pfa} but after magg fills, eligible = {spr_med, pfa}, and
  spr_med (2.22) > pfa (1.74) wins.

Net quota fill: magg +30, spr_med +22.

### Design rationale

Villain=BB (preflop caller) is mandatory per Bug 1: if villain is the preflop opener,
`villain_aggression_count` includes the preflop raise = 3 at river, not 2. All templates
follow the established MAGG-1/MAGG-2/MAGG-3 patterns:
- MAGG-A: villain bets flop + bets turn; hero calls both; hero at river check/bet decision
- MAGG-B: villain check-raises flop + bets turn; hero calls both; river decision
- MAGG-C: hero facing river bet after calling two streets of villain aggression

Board diversity: vary across draw-heavy, paired, broadway-heavy, low-connected textures
not already in existing 10 boards. Hero hand diversity: air, busted-draw, medium-made,
strong pair across new boards.

### New templates — MAGG Group A (pot 50–80 BB, fill magg quota)

MAGG-A-01 through MAGG-A-30: pot 50–75 BB, fills {magg, pfa}.

| ID | hero_pos | villain_pos | board (5-card river) | hero_cards | pot | to_call | action pattern | categories |
|----|---------|-------------|---------------------|-----------|-----|---------|---------------|-----------|
| MAGG-A-01 | CO | BB | 7c 4h 2s 9d Jc | Ah Qd | 55.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-02 | BTN | BB | 6s 3d 2h 8s Kd | Jc Tc | 52.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-03 | CO | BB | Qc 5d 3h 7c 2s | Kd Jh | 58.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-04 | BTN | BB | Th 4d 2c 6h Ac | 9s 8d | 50.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-05 | CO | BB | Jd 8c 3s 5h 2d | Kh Qc | 60.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-06 | BTN | BB | 9c 6h 2d Ks Ts | Ad 7c | 55.0 | 18.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-07 | CO | BB | As 7d 3c Jh 5s | Qh Tc | 62.0 | 20.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-08 | BTN | BB | Kh 5c 2d 8h 4s | Jd 9s | 58.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa} |
| MAGG-A-09 | CO | BB | 8d 6s 3h Qc Th | Ah 7d | 65.0 | 22.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-10 | BTN | BB | Td 9c 5h 3s 7d | Ks Qh | 54.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-11 | CO | BB | Jh 6d 4c 2h 9s | Ac 8s | 60.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-12 | BTN | BB | Qh 4s 2d 6c Kh | Tc 8d | 57.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-13 | CO | BB | 7s 5h 2c Ah 3d | Kd Jc | 63.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-14 | BTN | BB | Kc 8h 4d 2s Qd | Jh 9s | 50.0 | 17.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-15 | CO | BB | Ac 6h 3s 9d 5h | Ks Qd | 68.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa} |
| MAGG-A-16 | BTN | BB | Js 9d 4c 2h 6s | Ah Kc | 55.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-17 | CO | BB | 5d 3h 2c Jc 8h | Qd Qh | 70.0 | 23.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-18 | BTN | BB | Th 7s 3d Qc 2h | Kd 9c | 52.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-19 | CO | BB | 9s 6d 2h 4c Ks | Jh Td | 60.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-20 | BTN | BB | As 3c 2d 7h Jd | 9h 8c | 53.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-21 | CO | BB | Qd 8h 5s 3d Ah | Kc Jd | 56.0 | 19.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-22 | BTN | BB | 6h 4d 3s Tc 9h | Ad Ks | 65.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa} |
| MAGG-A-23 | CO | BB | Kh 7c 4d 2s 8d | Qs Jh | 58.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-24 | BTN | BB | Jc 5h 2d 9s Kd | Ac Td | 55.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-25 | CO | BB | 8h 5d 3c 6s Qs | Ah 7s | 62.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-26 | BTN | BB | Qc 9h 6d 3s Td | Kh Jd | 50.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-27 | CO | BB | 7h 4s 2d 5c Jh | Kc Qs | 60.0 | 20.0 | BB bets flop+turn+river | {magg,pfa} |
| MAGG-A-28 | BTN | BB | Ah 8d 3s 6c 2h | Js 9d | 54.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-29 | CO | BB | Th 6c 3d 4h Qs | Kd Jh | 57.0 | 0.0 | BB bets flop+turn | {magg,pfa} |
| MAGG-A-30 | BTN | BB | 9d 5s 2c 8h Kc | Ah Qd | 63.0 | 21.0 | BB bets flop+turn+river | {magg,pfa} |

### New templates — MAGG Group B (pot 26–45 BB, overflow to spr_med)

MAGG-B-01 through MAGG-B-22: pot 26–45 BB → SPR 2.22–3.85 (spr_med). Once magg fills
(40/40), these 22 records are assigned to spr_med.

| ID | hero_pos | villain_pos | board (5-card river) | hero_cards | pot | to_call | action pattern | categories |
|----|---------|-------------|---------------------|-----------|-----|---------|---------------|-----------|
| MAGG-B-01 | CO | BB | 7d 3h 2c 5s Tc | Ah Kd | 32.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-02 | BTN | BB | 6c 4s 2d 8h Js | Kd Qh | 28.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-03 | CO | BB | Jd 7c 3s 5h Ah | Qs Td | 35.0 | 12.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |
| MAGG-B-04 | BTN | BB | Tc 8s 2h 4d 6c | Kh Jd | 30.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-05 | CO | BB | 9s 5d 2c 7h Kd | Ac Jh | 40.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-06 | BTN | BB | Qs 6h 3d 2c 8s | Th 9c | 33.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa,spr_med} |
| MAGG-B-07 | CO | BB | 8c 4h 2s 6d Jc | Kd Qs | 27.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-08 | BTN | BB | Kd 5s 3h 9c 2d | Ah Jc | 38.0 | 13.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |
| MAGG-B-09 | CO | BB | Ts 7h 4c 2d 8s | Qd Jh | 32.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-10 | BTN | BB | 5c 3s 2h 9d Ks | Ad Tc | 45.0 | 15.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |
| MAGG-B-11 | CO | BB | Jh 8d 5s 3c Qs | Kc 9h | 30.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-12 | BTN | BB | Ac 7s 4h 2d 6c | Kd Jh | 35.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa,spr_med} |
| MAGG-B-13 | CO | BB | 9h 6c 3d 5s Td | Qs Jc | 28.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-14 | BTN | BB | Kh 4d 2c 7s Jh | Ah Qc | 40.0 | 14.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |
| MAGG-B-15 | CO | BB | 7s 5c 2h 4d Qs | Kh Jd | 32.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-16 | BTN | BB | Qd 8c 3s 6h 2d | Ac Td | 27.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-17 | CO | BB | 8s 6d 3h 5c Kc | Jd 9h | 36.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-18 | BTN | BB | As 5h 3d 7c 2s | Ks Jd | 42.0 | 14.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |
| MAGG-B-19 | CO | BB | Jc 7d 4s 2h Qs | Kh Td | 30.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-20 | BTN | BB | 9c 4h 2s 6d Ah | Ks Qd | 34.0 | 0.0 | BB check-raises flop+bets turn | {magg,pfa,spr_med} |
| MAGG-B-21 | CO | BB | Th 8s 3c 5d Kd | Ac Jh | 38.0 | 0.0 | BB bets flop+turn | {magg,pfa,spr_med} |
| MAGG-B-22 | BTN | BB | Qs 6s 4d 2c 7h | Kd Jc | 44.0 | 15.0 | BB bets flop+turn+river | {magg,pfa,spr_med} |

### Action history spec for each pattern

All templates hero is PFA opener (opener_position = hero_pos).

**MAGG-A pattern (BB bets flop + bets turn, hero checks river):**
```python
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'), ('flop', hero_pos, 'call'),
    ('turn', 'BB', 'bet'), ('turn', hero_pos, 'call'),
]
# pot and to_call=0 → hero acts first on river
```

**MAGG-B pattern (BB bets flop + turn + river, hero faces bet):**
```python
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'), ('flop', hero_pos, 'call'),
    ('turn', 'BB', 'bet'), ('turn', hero_pos, 'call'),
    ('river', 'BB', 'bet'),
]
# to_call > 0 → hero faces river bet
```

**MAGG-C pattern (BB check-raises flop, bets turn, hero at river):**
```python
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'check'), ('flop', hero_pos, 'bet'),
    ('flop', 'BB', 'raise'), ('flop', hero_pos, 'call'),
    ('turn', 'BB', 'bet'), ('turn', hero_pos, 'call'),
]
# villain_aggression_count = 2 (check-raise counts as 1 bet-action + turn bet = 2)
```

Note: In MAGG-C, the bridge computes villain_aggression_count from prior-street
bet/raise actions by the primary villain (last in villain_positions for faced-bet
scenarios, or first otherwise). Check-raise = 1 aggression event; turn bet = 1
aggression event → total = 2 at river.

### Expected feat_dict values

All 52 templates:
- `villain_aggression_count`: 2 (checked by generate_scenarios assertion)
- `street`: 'river'
- `is_preflop_aggressor`: 1 (hero is opener)

MAGG Group B only:
- `spr`: 2.22 – 3.85 (pot 26–45 BB, formula = 100/pot)

### Bug-awareness checklist for programmer

- Bug 1: villain MUST be BB (preflop CALLER). Do NOT use CO/BTN as villain — their
  preflop raise adds to villain_aggression_count making it 3 not 2.
- All hero_cards must be 2 distinct cards not appearing on the board.
- villain_positions = ['BB'] for all 52 templates (HU scenario).

---

## Module 2 — pfa_scenarios.py

### Current state

22 records. Mix of CO/BTN/HJ openers, flop and turn decisions. Pot 14–22 BB → SPR
4.5–7.1 (all spr_std). Boards used: see fingerprint list in source file.

### Target expansion: +34 new records

All 34 at pot 14–24 BB (spr_std). These match {pfa, spr_std} but spr_std is already
met (target 50, currently above threshold). Eligible category = {pfa}. Assigned to pfa.

Fills: pfa +34 (from 46 to 80 — target exactly met).

### Design rationale

Expand position and board-texture coverage not in existing 22 templates:
- Existing templates: CO opener (7), BTN opener (5+5 turn), HJ opener (5). No SB or UTG.
  Add HJ opener on new board textures, and CO/BTN on more dynamic boards.
- Existing boards: all dry/rainbow or two-tone. Add: paired boards, monotone flops,
  3-connected flops, high-connected boards (broadway-heavy).
- Hero hand diversity: existing templates concentrate on air/overcards/overpairs.
  Add: second pair, weak flush draw, trips, bottom pair.

Sub-groups:
- PFA-5: HJ opener, CO+BB callers, new boards (8 records)
- PFA-6: CO opener, BTN+BB callers, dynamic boards (10 records)
- PFA-7: BTN opener, CO+SB callers (BB folds), spr_std range (8 records)
- PFA-8: Turn c-bet continuation (delayed c-bet), new positions (8 records)

### New template list — PFA Group (pot 14–24 BB, spr_std)

| ID | hero_pos | villain_pos | board | hero_cards | pot | to_call | street | categories |
|----|---------|-------------|-------|-----------|-----|---------|--------|-----------|
| PFA-5a | HJ | CO,BB | Ac 9s 4d | Kh Qd | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5b | HJ | CO,BB | Ks 8c 3h | Jc Jd | 14.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5c | HJ | CO,BB | Qc 6d 2s | Ah Kd | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5d | HJ | CO,BB | Jd 9s 5c | Ks Qh | 14.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5e | HJ | CO,BB | Tc 4d 2h | Ad Qc | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5f | HJ | CO,BB | 8s 8d 3c | Ah Kc | 14.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5g | HJ | CO,BB | Kd 6c 6s | Qs Jd | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-5h | HJ | CO,BB | 5h 5d 2c | Kc Kd | 14.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6a | CO | BTN,BB | Ad 6s 3d | Kh Jd | 16.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6b | CO | BTN,BB | Jc 7s 4h | Ac 9c | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6c | CO | BTN,BB | Qs 9d 8c | Kh Kd | 16.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6d | CO | BTN,BB | Tc 9s 8d | Jd 7c | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6e | CO | BTN,BB | Ah 7c 4s | Qd Qs | 16.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6f | CO | BTN,BB | Kc 5s 3h | Ac Jc | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6g | CO | BTN,BB | 9h 9c 2d | Kd Kh | 16.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6h | CO | BTN,BB | Qd Jh 5c | As Kh | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6i | CO | BTN,BB | 8h 6c 4d | Kc Qd | 16.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-6j | CO | BTN,BB | 5c 5s 3d | Ah Qs | 15.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7a | BTN | CO,SB | Kd 8s 2h | Ah Jd | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7b | BTN | CO,SB | Qh 7d 4c | Kc Ks | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7c | BTN | CO,SB | Jd 6s 3c | Ac Qd | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7d | BTN | CO,SB | Th 5d 2s | Kh Jc | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7e | BTN | CO,SB | Ah 4c 2d | 9h 9d | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7f | BTN | CO,SB | 7s 6d 3h | Ks Qc | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7g | BTN | CO,SB | Qs 5h 2c | Ac Kd | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-7h | BTN | CO,SB | 9c 8s 4h | Jh Jd | 20.0 | 0.0 | flop | {pfa,spr_std} |
| PFA-8a | CO | BTN,BB | Ks 7d 2c Qh | Ah Kd | 22.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8b | CO | BTN,BB | Jc 6h 2d Tc | As Js | 24.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8c | HJ | CO,BB | Qd 5s 3h 8d | Kh Kd | 22.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8d | BTN | SB,BB | Ah 5c 2d 9s | Kh Qd | 23.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8e | CO | BTN,BB | 9h 8c 4d Jh | Kd Qs | 22.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8f | BTN | SB,BB | Td 6s 2c Ks | Jh Jd | 24.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8g | HJ | CO,BB | 8d 5s 2h As | Kc Qh | 22.0 | 0.0 | turn | {pfa,spr_std} |
| PFA-8h | CO | BTN,BB | Qh 7c 3s 5d | Ah 9h | 23.0 | 0.0 | turn | {pfa,spr_std} |

### Action history spec

Flop templates (PFA-5, PFA-6, PFA-7):
```python
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', vill1, 'call'), ('preflop', vill2, 'call'),
]
# to_call=0, hero acts first on flop
```

Turn templates (PFA-8): hero checks flop, all check, hero faces turn decision:
```python
# For BTN openers (acts last postflop):
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', vill1, 'call'), ('preflop', vill2, 'call'),
    ('flop', vill1, 'check'), ('flop', vill2, 'check'), ('flop', hero_pos, 'check'),
]
# For CO/HJ openers (acts before BTN/SB postflop):
action_history = [
    ('preflop', hero_pos, 'raise'), ('preflop', vill1, 'call'), ('preflop', vill2, 'call'),
    ('flop', hero_pos, 'check'), ('flop', vill1, 'check'), ('flop', vill2, 'check'),
]
```

PFA-7 note: BB folded preflop. Action history uses ('preflop', 'BB', 'fold') to remove BB
from active positions. villain_positions = [CO, SB] (no BB).

PFA-8d/8f note: BB did not fold in these templates (SB+BB are villains). Use standard
3-way preflop action.

### Expected feat_dict values

All 34 templates:
- `is_preflop_aggressor`: 1
- `spr`: 4.17–7.14 (pot 14–24 BB)
- `street`: 'flop' or 'turn'
- `to_call`: 0.0

---

## Module 3 — nfd_scenarios.py

### Current state

11 records: 4 RAISE-eligible (villain_air_pct ≥ 0.20), 4 CALL-eligible (< 0.20),
4 boundary (pass R4 filter), 1 boundary (fail R4 = filtered). Net: 4 nfd_raise,
4 nfd_call, 4 nfd_boundary (nfd_boundary already at target 6/10 acceptable per gto-expert).

Existing boards: 7h4h2d, 6d3d2c, 8h5h2s, 9c5c2h (RAISE), Kh Qh4c, JcTc5d, JhTh6d (CALL),
Tc4c2d8c, 7c4c2h-Kc, 7c4c2d9c, 6s3s2c9s, 6c3c2h9c (boundary).

### Target expansion: +32 new records

- +16 nfd_raise templates (villain_air_pct ≥ 0.20, non-boundary)
- +16 nfd_call templates (villain_air_pct < 0.20, non-boundary)

No new boundary templates needed (nfd_boundary target already met at 6/10).

### Design rationale

**NFD RAISE** templates: villain_air_pct ≥ 0.20 arises when villain is a wide-range
caller (BB) on low/unconnected boards where their range has many unconnected broadways.
Use: villain=BB, hero=BB (calling BB vs BTN/CO raise), board ranks 2–9, rainbow or
two-tone (not monotone). Vary flush suits across hearts, diamonds, clubs, spades.
New hero card pairs: Ah+Th, Ad+9d, As+5s, Ac+7c, Ah+6h, As+8s (suit+blocker diversity).

**NFD CALL** templates: villain_air_pct < 0.20 arises when villain is a BTN/CO PFA on
high/connected boards (K/A/Q-high, J-T-high) where their continuation range is value-heavy.
Use: villain=CO or BTN (tighter range), board with broadway cards, hero=BB.

**Bug 2**: hero MUST hold 2 cards of the flush suit. Board must have exactly 2 cards of
that suit (flop templates). Total = 4 of same suit = flush draw. Do NOT use 1-suit hero
card + 2-suit board unless using TURN boundary pattern (3-flush-board).

### New template list — NFD RAISE (villain_air_pct ≥ 0.20)

All: hero=BB, 2-player, villain=BTN or CO (PFA), BB defends. Flop decision.
hero_cards: both of flush suit. board: 2 cards of flush suit + 1 offsuit.

| ID | villain_pos | board | hero_cards | pot | to_call | flush_suit | notes |
|----|------------|-------|-----------|-----|---------|-----------|-------|
| NFD-R-01 | BTN | 6h 3h 2s | Ah Th | 12.0 | 4.0 | hearts | low board |
| NFD-R-02 | BTN | 5d 3d 2c | Ad 9d | 12.0 | 4.0 | diamonds | very low |
| NFD-R-03 | CO | 7s 4s 2h | As 8s | 12.0 | 4.0 | spades | low |
| NFD-R-04 | CO | 8c 4c 3d | Ac 7c | 12.0 | 4.0 | clubs | low |
| NFD-R-05 | BTN | 6s 3s 2d | As 5s | 12.0 | 4.0 | spades | very low |
| NFD-R-06 | CO | 7h 5h 3c | Ah 6h | 12.0 | 4.0 | hearts | low mid |
| NFD-R-07 | BTN | 9d 4d 2c | Ad Jd | 12.0 | 4.0 | diamonds | low w high FD |
| NFD-R-08 | CO | 8s 5s 3h | As Qs | 12.0 | 4.0 | spades | low w high FD |
| NFD-R-09 | BTN | 7c 3c 2s | Ac 8c | 12.0 | 4.0 | clubs | low |
| NFD-R-10 | CO | 6d 4d 2h | Ad Kd | 12.0 | 4.0 | diamonds | low K-kicker FD |
| NFD-R-11 | BTN | 5h 3h 2d | Ah 9h | 12.0 | 4.0 | hearts | very low |
| NFD-R-12 | CO | 9s 6s 2c | As Ts | 12.0 | 4.0 | spades | mid low |
| NFD-R-13 | BTN | 8h 4h 3s | Ah Qh | 12.0 | 4.0 | hearts | low w Q-kicker FD |
| NFD-R-14 | CO | 7d 4d 3h | Ad 8d | 12.0 | 4.0 | diamonds | low |
| NFD-R-15 | BTN | 6c 5c 2d | Ac Jc | 12.0 | 4.0 | clubs | connected low |
| NFD-R-16 | CO | 9h 5h 2s | Ah Kh | 12.0 | 4.0 | hearts | low w K-kicker FD |

### New template list — NFD CALL (villain_air_pct < 0.20)

All: hero=BB, villain=BTN or CO (PFA), BB defends. Flop decision.
High/connected boards → villain's range is value-heavy → low air fraction.

| ID | villain_pos | board | hero_cards | pot | to_call | flush_suit | notes |
|----|------------|-------|-----------|-----|---------|-----------|-------|
| NFD-C-01 | BTN | Qh 9h 5c | Ah Jh | 13.0 | 4.0 | hearts | Q-high board |
| NFD-C-02 | CO | Kd 8d 4s | Ad Td | 13.0 | 4.0 | diamonds | K-high |
| NFD-C-03 | BTN | As 7s 3d | Ks 9s | 13.0 | 4.0 | spades | A-high, hero K-blocker |
| NFD-C-04 | CO | Kc 9c 6h | Ac Qc | 13.0 | 4.0 | clubs | K-high |
| NFD-C-05 | BTN | Qd Jd 4c | Ad Kd | 13.0 | 4.0 | diamonds | Q-J connected |
| NFD-C-06 | CO | Jh 9h 7c | Ah Kh | 13.0 | 4.0 | hearts | J-high connected |
| NFD-C-07 | BTN | Ks Ts 4d | As Qs | 13.0 | 4.0 | spades | K-T connected |
| NFD-C-08 | CO | Qc 8c 5h | Ac Kc | 13.0 | 4.0 | clubs | Q-high |
| NFD-C-09 | BTN | Ah Th 3d | Kh Jh | 13.0 | 4.0 | hearts | A-T connected |
| NFD-C-10 | CO | Kd Qd 5c | Ad Jd | 13.0 | 4.0 | diamonds | K-Q connected |
| NFD-C-11 | BTN | Js Ts 7h | As 9s | 13.0 | 4.0 | spades | J-T connected |
| NFD-C-12 | CO | Qh 8h 6d | Ah Th | 13.0 | 4.0 | hearts | Q-high |
| NFD-C-13 | BTN | Kc 7c 3h | Ac Tc | 13.0 | 4.0 | clubs | K-high |
| NFD-C-14 | CO | Ad 9d 4s | Kd Qd | 13.0 | 4.0 | diamonds | A-high, K blocker |
| NFD-C-15 | BTN | Js 8s 4d | As Ks | 13.0 | 4.0 | spades | J-high connected |
| NFD-C-16 | CO | Qc 7c 2h | Ac 8c | 13.0 | 4.0 | clubs | Q-high low |

### Action history spec (all 32 NFD templates)

```python
action_history = [
    ('preflop', villain_pos, 'raise'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'check'), ('flop', villain_pos, 'bet'),
]
# hero_pos='BB', opener_position=villain_pos, to_call=4.0
```

### Expected feat_dict values

All 32:
- `has_flush_draw`: 1 (2 hero cards + 2 board cards of same suit = 4 total)
- `nut_flush_block`: 1 (hero holds Ace of flush suit)

NFD-RAISE group (R-01 through R-16):
- `villain_air_pct`: ≥ 0.20 (target range 0.22–0.28 for low boards vs BTN/CO)

NFD-CALL group (C-01 through C-16):
- `villain_air_pct`: < 0.20 (target range 0.08–0.16 for high/connected boards)

### Card conflict checks

For each template, verify:
- hero_cards[0] and hero_cards[1] not on board
- hero_cards[0] ≠ hero_cards[1]
- No board card appears in hero_cards

Example: NFD-R-01: hero [Ah, Th], board [6h, 3h, 2s] — Ah and Th not on board. ✓
Example: NFD-C-09: hero [Kh, Jh], board [Ah, Th, 3d] — Kh and Jh not on board. ✓

---

## Module 4 — bac_scenarios.py

### Current state

9 records. All hero=BB, villain=SB+BTN or BTN+SB (CO bets case). Pot 20–46 BB.
Three sub-patterns: flop (4 records), turn (4 records), 1 CO-bets-BTN-calls.

Existing boards: Ks7d2c, Jh8c3d, 9h8c4d, As6c2d (flop), Kd7s2hTc, Ah9c3d8s, Jc8h3dKs,
Qh7c2s5d (turn), Td6h2c (SB/CO pattern).

### Target expansion: +11 new records

All 11 at pot 14–24 BB (spr_std range, SPR ≥ 4.0). This keeps BAC records cleanly
separate from spr_med (which is filled by MAGG overflow), avoiding tie-break uncertainty.
spr_std is already at target but these records are eligible only for {bac} since spr_std
is full → cleanly assigned to bac.

Fills: bac +11 (from 9 to 20).

### Design rationale

Expand villain position coverage:
- Existing: BTN bets, SB calls, BB hero (most templates). One CO-bets, BTN-calls, SB hero.
- New: CO bets, BTN calls, BB hero (BAC-4: adds CO as bettor against BB)
- New: HJ bets, CO calls, BTN hero (BAC-5: positional diversity)
- New: Turn decision with CO/BTN structure (BAC-6)

Hero hand diversity: existing covers air, OESD, top-pair-weak-kicker, gutshot.
New: flush draw facing BAC, two pair, medium pair.

### New template list

| ID | hero_pos | bettor_pos | caller_pos | board | hero_cards | pot | to_call | street | categories |
|----|---------|-----------|-----------|-------|-----------|-----|---------|--------|-----------|
| BAC-4a | BB | CO | BTN | 7d 4h 2c | Qh Jd | 18.0 | 5.0 | flop | {bac,spr_std} |
| BAC-4b | BB | CO | BTN | 9s 5d 3c | Kc Qh | 18.0 | 5.0 | flop | {bac,spr_std} |
| BAC-4c | BB | CO | BTN | Ah 8s 3d | Tc 9h | 18.0 | 5.0 | flop | {bac,spr_std} |
| BAC-4d | BB | CO | BTN | Jd 5h 2s | Ac 7d | 18.0 | 5.0 | flop | {bac,spr_std} |
| BAC-5a | BTN | HJ | CO | Kh 6s 3d | Jc Jh | 16.0 | 5.0 | flop | {bac,spr_std} |
| BAC-5b | BTN | HJ | CO | Qd 8c 2h | Kh Jd | 16.0 | 5.0 | flop | {bac,spr_std} |
| BAC-5c | BTN | HJ | CO | Th 7s 4d | As Kc | 16.0 | 5.0 | flop | {bac,spr_std} |
| BAC-6a | SB | BTN | CO | Ks 9h 3d 7c | Jd Td | 22.0 | 7.0 | turn | {bac,spr_std} |
| BAC-6b | BB | BTN | SB | Ah 7c 4d 2s | Qd Js | 24.0 | 7.0 | turn | {bac,spr_std} |
| BAC-6c | BB | CO | BTN | Qh 5s 3d 9c | Kd Th | 22.0 | 7.0 | turn | {bac,spr_std} |
| BAC-6d | SB | CO | BTN | Jc 8h 4s 6d | Tc 9s | 24.0 | 7.0 | turn | {bac,spr_std} |

### Action history spec

BAC-4 (CO bets, BTN calls, BB hero faces):
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
    ('flop', 'SB', 'check'),    # SB checked/folded (BB goes after SB; SB acts first)
    ('flop', 'BB', 'check'),
    ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
]
# villain_positions=['BTN', 'CO'] — CO is last (bettor); BTN is caller
# num_callers_to_bet = 1 (BTN called)
```

Wait — if SB is not in the hand, do not include SB action. If SB folded preflop:
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
    ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'check'),
    ('flop', 'CO', 'bet'), ('flop', 'BTN', 'call'),
]
# villain_positions=['BTN', 'CO']
```

BAC-5 (HJ bets, CO calls, BTN hero faces):
```python
action_history = [
    ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BTN', 'call'),
    ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'fold'),
    ('flop', 'HJ', 'bet'), ('flop', 'CO', 'call'),
]
# villain_positions=['CO', 'HJ'] — HJ is last (bettor); CO is caller
# hero faces bet-and-call as BTN (last to act)
```

BAC-6 turn templates: include flop check-around before turn action:
```python
action_history = [
    ('preflop', opener, 'raise'), ...callers...,
    ('flop', ...all check...),
    ('turn', bettor, 'bet'), ('turn', caller, 'call'),
]
```

### Expected feat_dict values

All 11 templates:
- `num_callers_to_bet`: ≥ 1
- `spr`: 4.17–7.14 (pot 14–24 BB)

---

## Module 5 — donk_bet_defence_scenarios.py

### Current state

15 records across sub-scenarios 8a–8e + Pattern D (5 flush-blocker hands). Existing boards:
Kc7h2d, 9d6c2h (8a), Jh8d3s, Ks5c2d (8b_co_calls), Td6h2c (8b_co_folds), 8s5d2c, Qd7s3h
(8c), Jc8h3d, 9s6c2h (8d), Tc7d4s (8e), and 5 Pattern-D boards.

### Target expansion: +10 new records

Split: 5 new sub-scenario 8c/8d templates (hero=PFA), 5 new sub-scenario 8a/8b templates.
Mix ensures donk category fills without relying on pfa overlap (donk < pfa in scarcity).

Fills: donk +10 (from 15 to 25).

### Design rationale

- Hero hand diversity: existing 8c/8d templates are top-pair/overcards-heavy.
  New: bottom-two-pair, gutshot, flush-draw-blocker on new boards.
- Board diversity: existing templates are dry low-boards and Q-J-high boards.
  New: add T-high two-tone, K-mid-low, A-high paired boards.
- Bug 5 awareness: if CO folded preflop, omit CO from action_history postflop.
  Bug-Dc awareness: hero_cards must be 2 distinct cards.

### New template list

| ID | sub_sc | hero_pos | villain_pos | board | hero_cards | pot | to_call | street | categories |
|----|--------|---------|-------------|-------|-----------|-----|---------|--------|-----------|
| DK-N-01 | 8c | CO | BB,BTN | Kd 5d 2h | Ac Kh | 18.0 | 6.0 | flop | {donk,pfa} |
| DK-N-02 | 8c | CO | BB,BTN | 7h 5s 3d | Kh Kd | 18.0 | 6.0 | flop | {donk,pfa} |
| DK-N-03 | 8d | BTN | BB | Ah 6c 3s | Kd Kh | 15.0 | 5.0 | flop | {donk,pfa} |
| DK-N-04 | 8d | BTN | BB | Qs 4h 2d | Jd Jh | 15.0 | 5.0 | flop | {donk,pfa} |
| DK-N-05 | 8c | CO | BB,BTN | Jd 4s 2c | Ah Qd | 18.0 | 6.0 | flop | {donk,pfa} |
| DK-N-06 | 8a | CO | BB,BTN | Th 8s 5d | Kc Qs | 18.0 | 6.0 | flop | {donk} |
| DK-N-07 | 8a | CO | BB,BTN | 6d 4c 2h | Ac 8d | 18.0 | 6.0 | flop | {donk} |
| DK-N-08 | 8b_co_calls | BTN | BB,CO | Ks 7d 3h | Qd Jc | 30.0 | 6.0 | flop | {donk} |
| DK-N-09 | 8b_co_calls | BTN | BB,CO | Ah 5c 4d | Tc 8s | 30.0 | 6.0 | flop | {donk} |
| DK-N-10 | 8e | CO | BB,BTN | Jh 7c 4d | Ac Qh | 18.0 | 6.0 | flop | {donk,pfa} |

Note: DK-N-01 through DK-N-05 and DK-N-10 are sub-scenarios 8c/8d (hero=PFA). These
records satisfy {donk, pfa} but are assigned to pfa (scarcity 1.74 > donk 1.67) until
pfa fills. Once pfa quota fills (80/80), remaining donk+pfa records overflow to donk.
Since donk needs exactly +10, and pfa also needs +34, the assignment path matters:

- If pfa fills BEFORE these donk+pfa records are processed: assigned to donk.
- If pfa not yet full: assigned to pfa, donk remains unfilled.

**Risk**: the 6 donk+pfa templates (DK-N-01 to -05, -10) may all go to pfa, leaving donk
with only +4 (DK-N-06 to -09). This is insufficient (+4 instead of +10 for donk gap).

**Mitigation**: Design all 10 new donk templates, including 6 that also hit pfa. The
net result depends on pool ordering, but the pool will have enough records to fill both
donk(+10) and pfa(+34) when ALL new records across all modules are combined. The 34 pure
PFA records in Module 2 (pfa_scenarios.py) fill pfa without needing donk-pfa records.
Once pfa fills from pure PFA records, these 6 donk-pfa templates serve donk.

**Builder note**: ensure pfa-only templates (Module 2) are generated BEFORE donk templates
in the pool. The allocator shuffles the pool, but the pure PFA records (34 new + 46 existing
= 80) should provide enough pfa-eligible records that donk-pfa records flow to donk.

### Action history spec

Sub-scenario 8c (hero=CO PFA, BTN behind):
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'),
]
# villain_positions=['BB', 'BTN'], opener_position='CO'
# hero=CO faces BB donk first; BTN still behind
```

Sub-scenario 8d (hero=BTN PFA, HU vs BB after SB fold):
```python
action_history = [
    ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'fold'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'),
]
# villain_positions=['BB'], opener_position='BTN'
```

Sub-scenario 8a (hero=CO, opener=HJ):
```python
action_history = [
    ('preflop', 'HJ', 'raise'), ('preflop', 'CO', 'call'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'),
]
# villain_positions=['BB', 'BTN'], opener_position='HJ'
```

Sub-scenario 8b_co_calls (BTN faces BB donk + CO call):
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'), ('flop', 'CO', 'call'),
]
# villain_positions=['BB', 'CO'], opener_position='CO'
```

Sub-scenario 8e (hero=CO, PFA, BTN behind):
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'),
    ('flop', 'BB', 'bet'),
]
# identical structure to 8c; sub_scenario label differentiates
```

### Expected feat_dict values

All 10:
- `generation_source`: 'donk_bet_defence_scenarios' → `_is_donk_hand` = True
- `facing_bet`: 1 (hero faces BB donk)
- hero_position: 'CO' or 'BTN'

DK-N-01 to -05, DK-N-10 (hero=PFA):
- `is_preflop_aggressor`: 1

---

## Module 6 — sb_hero_scenarios.py

### Current state

12 records. Hero=SB, facing CO or BTN c-bets, with or without BTN-behind-sandwich.
Pot 15–35 BB. Existing boards: Kh7d2s, Jc8h3d, Ah5c2d, 9s8d3h (3-way sandwich),
Qs7h2c, Tc6d2s (BTN-called), Kc9h4d, 8s5d2h (BTN 2-way), Js7c2d, Td8h3s (medium-made),
Ks7d2c9h, Ah8c3dKs (turn).

### Target expansion: +7 new records

Fills: sb +7 (from 13 to 20).

### Design rationale

Expand: (a) river decisions for SB (currently 0 river records); (b) 3-bet pot scenarios
where SB 3-bets and faces 4-bet or calls and faces c-bet; (c) SPR medium range for SB.
Keep hero=SB for `_is_sb_hero_hand` filter. BB folded preflop in all scenarios → BB NOT
in villain_positions (Bug 3 awareness).

### New template list

| ID | hero_pos | villain_pos | board | hero_cards | pot | to_call | street | categories |
|----|---------|-------------|-------|-----------|-----|---------|--------|-----------|
| SB-N-01 | SB | CO,BTN | 6d 4s 2h | Kh Qc | 20.0 | 6.0 | flop | {sb} |
| SB-N-02 | SB | CO,BTN | Qd 5h 3s | Jd Tc | 20.0 | 6.0 | flop | {sb} |
| SB-N-03 | SB | BTN | 9h 6d 3c | Ah 8d | 18.0 | 6.0 | flop | {sb} |
| SB-N-04 | SB | CO,BTN | Kc 8d 4h | Qd Jh | 20.0 | 6.0 | flop | {sb} |
| SB-N-05 | SB | CO | Th 7c 2s 6d | Kd Qh | 34.0 | 10.0 | turn | {sb,spr_med} |
| SB-N-06 | SB | CO | As 4d 2c 8h | Jh Td | 36.0 | 12.0 | turn | {sb,spr_med} |
| SB-N-07 | SB | BTN | Jd 9s 5h 3c | Kc Qd | 32.0 | 10.0 | turn | {sb,spr_med} |

SB-N-05/06/07: pot 32–36 BB → SPR 2.78–3.13 (spr_med). Once spr_med fills (from MAGG
overflow), these are assigned to sb.

### Action history spec

Flop templates (SB-N-01 to -04):
```python
# SB-N-01: CO+BTN villains, BB folded preflop
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
    ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
    ('flop', 'SB', 'check'), ('flop', 'CO', 'bet'),
]
# villain_positions=['CO', 'BTN']
```

```python
# SB-N-03: BTN villain only, BB folded preflop
action_history = [
    ('preflop', 'BTN', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
    ('flop', 'SB', 'check'), ('flop', 'BTN', 'bet'),
]
# villain_positions=['BTN']
```

Turn templates (SB-N-05 to -07):
```python
action_history = [
    ('preflop', 'CO', 'raise'), ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
    ('flop', 'SB', 'check'), ('flop', 'CO', 'check'),
    ('turn', 'SB', 'check'), ('turn', 'CO', 'bet'),
]
# villain_positions=['CO'] — 2-way after BB folds
```

### Expected feat_dict values

All 7:
- `hero_position`: 'SB' → `_is_sb_hero_hand` = True (also satisfied by generation_source)
- `generation_source`: 'sb_hero_scenarios'

SB-N-05/06/07:
- `spr`: 2.78–3.13 (spr_med)

---

## Cross-module overlap table

| Record group | Categories satisfied | Assigned to | Notes |
|-------------|---------------------|-------------|-------|
| MAGG-A (30 records, pot 50–75 BB) | {magg, pfa} | magg | All 30 fill magg quota |
| MAGG-B (22 records, pot 26–45 BB) | {magg, pfa, spr_med} | spr_med | After magg full (40/40); spr_med wins over pfa (2.22 > 1.74) |
| PFA new (34 records, pot 14–24 BB) | {pfa, spr_std} | pfa | spr_std full → eligible = pfa only |
| BAC new (11 records, pot 14–24 BB) | {bac, spr_std} | bac | spr_std full → eligible = bac only |
| NFD-RAISE (16 records) | {nfd_raise} | nfd_raise | Pure nfd_raise (scarcity 5.0) |
| NFD-CALL (16 records) | {nfd_call} | nfd_call | Pure nfd_call (scarcity 5.0) |
| DONK 8c/8d new (6 records) | {donk, pfa} | pfa (while pfa open), then donk | pfa scarcity 1.74 > donk 1.67 |
| DONK 8a/8b new (4 records) | {donk} | donk | Pure donk |
| SB flop new (4 records) | {sb} | sb | Pure sb |
| SB turn new (3 records) | {sb, spr_med} | sb (spr_med already full) | After MAGG fills spr_med |

**Genuine dual-quota filling**: Only MAGG-B templates achieve true dual-quota fill
(magg + spr_med) via the overflow mechanism. All other records fill exactly one quota.

---

## Total summary

### New record count by module

| Module | New templates | Primary quota fill | Secondary quota fill |
|--------|-------------|-------------------|---------------------|
| magg_scenarios.py | 52 | magg +30 | spr_med +22 (overflow) |
| pfa_scenarios.py | 34 | pfa +34 | — |
| nfd_scenarios.py | 32 | nfd_raise +16, nfd_call +16 | — |
| bac_scenarios.py | 11 | bac +11 | — |
| donk_bet_defence_scenarios.py | 10 | donk +10 | — |
| sb_hero_scenarios.py | 7 | sb +7 | — |
| **TOTAL** | **146** | | |

### Category fill matrix

| Category | Current yield | New records filling this category | Post-expansion yield | Target | Status |
|----------|-------------|----------------------------------|---------------------|--------|--------|
| pfa | 46 | +34 (from pfa_scenarios.py) | 80 | 80 | FULL |
| magg | 10 | +30 (from magg-A group) | 40 | 40 | FULL |
| spr_med | 18 | +22 (from magg-B overflow) | 40 | 40 | FULL |
| nfd_raise | 4 | +16 (from nfd_scenarios.py) | 20 | 20 | FULL |
| nfd_call | 4 | +16 (from nfd_scenarios.py) | 20 | 20 | FULL |
| bac | 9 | +11 (from bac_scenarios.py) | 20 | 20 | FULL |
| donk | 15 | +10 (from donk_scenarios.py) | 25 | 25 | FULL |
| sb | 13 | +7 (from sb_hero_scenarios.py) | 20 | 20 | FULL |

### Overlap factor

146 new records fills 150 quota slots (8 gaps summing to 30+22+34+16+16+11+10+7 = 146).
Overlap factor: 150/146 = 1.03. The MAGG-B overflow mechanism fills spr_med (+22) without
requiring a separate spr_med module expansion, saving 22 dedicated records. No other genuine
dual-quota savings exist under the F5 allocator's one-record-one-category constraint.

The directive's estimate of ~80–120 records was based on multi-quota assignment, which the
F5 allocator does not support. The actual minimum is 146 net new records.

---

## Verification spec

### Per-module assertions (programmer must confirm before committing)

**MAGG (52 new)**
- A-01 to A-30: assert `villain_aggression_count == 2` for every generated record
- B-01 to B-22: assert `villain_aggression_count == 2` AND `2.0 <= spr < 4.0`
- All 52: assert `is_preflop_aggressor == 1`
- All 52: assert hero_cards ∩ board == ∅ (no card conflicts)
- All 52: villain_positions == ['BB'] (villain is preflop caller, not raiser)
- Fingerprint check: no (hero_cards_str, board_str) pair duplicates any of the 10 existing
  MAGG records or any other new MAGG record in this batch

**PFA (34 new)**
- All 34: assert `is_preflop_aggressor == 1`
- All 34: assert `spr >= 4.0` (pot 14–24 BB)
- PFA-8 turn records: assert `street == 'turn'`
- Fingerprint check: no duplicates within PFA-5/6/7/8 batch or vs existing 22 PFA records

**NFD-RAISE (16 new)**
- All 16: assert `has_flush_draw == 1` AND `nut_flush_block == 1`
- All 16: assert `villain_air_pct >= 0.20`
- All 16: assert none pass `_validate_nfd_boundary` (not boundary cases)
- Card conflict: hero holds 2 cards of flush suit; board holds 2 cards of same suit; all 4 distinct

**NFD-CALL (16 new)**
- All 16: assert `has_flush_draw == 1` AND `nut_flush_block == 1`
- All 16: assert `villain_air_pct < 0.20`
- All 16: assert none pass `_validate_nfd_boundary`
- Card conflict: same as NFD-RAISE

**BAC (11 new)**
- All 11: assert `num_callers_to_bet >= 1`
- All 11: assert `spr >= 4.0`
- BAC-4: villain_positions[-1] = 'CO' (last = bettor); BTN is caller
- BAC-5: villain_positions[-1] = 'HJ'; CO is caller
- Fingerprint check: no duplicates vs existing 9 BAC records

**DONK (10 new)**
- All 10: assert `generation_source == 'donk_bet_defence_scenarios'`
- All 10: assert `facing_bet == 1`
- All 10: assert hero_position in ('CO', 'BTN')
- All 10: hero_cards are 2 distinct cards (Bug Dc check)
- DK-N-01 to -05, DK-N-10: assert `is_preflop_aggressor == 1`
- Fingerprint check: no duplicates vs existing 15 DONK records

**SB (7 new)**
- All 7: assert `hero_position == 'SB'`
- SB-N-05/06/07: assert `2.0 <= spr < 4.0` (spr_med range, pot 32–36 BB)
- Bug 3 check: BB NOT in villain_positions for any template (BB folded preflop)
- Fingerprint check: no duplicates vs existing 12 SB records

### Cross-module fingerprint disjointness

No new template shares (hero_cards_str, board_str) fingerprint with any existing template
across ALL modules. The builder must run fingerprint collision check across the combined pool
after generation (Mode B pool produces all scenario records before fingerprint check).

### Pool size target after expansion

Current Mode B pool: 115 records.
After expansion: 115 + 146 = 261 records in Mode B pool.

E2-B smoke test: assert Mode B pool ≥ 250 records.
Phase A allocator re-run: assert all 8 categories show FULL (not UNDER).

---

## Notes for builder (Phase 6 implementation)

1. Add new templates as additional list entries in `_MAGG_TEMPLATES`, `_PFA_TEMPLATES`,
   `_NFD_TEMPLATES`, `_BAC_TEMPLATES`, `_DONK_TEMPLATES`, `_SB_HERO_TEMPLATES`. Do NOT
   create new modules or modify generate_scenarios() function signatures.

2. For MAGG templates, the generate_scenarios() function already asserts
   `villain_aggression_count == 2`. New templates must satisfy this. The action_history
   patterns above are designed to produce exactly count=2.

3. NFD villain_air_pct targets: the feature extractor computes this from the villain's
   range composition. Low boards (2–9 rank) with BB caller → higher air. The existing
   NFD templates at boards 7h4h2d and 6d3d2c confirmed ≥ 0.22 for BTN opener vs BB.
   New low boards (5-rank and below) at 12 BB pot should produce similar results. Builder
   must run extraction on each new NFD template and confirm before committing.

4. BAC villain_positions ordering: the bridge uses the LAST entry in villain_positions as
   the bettor (Bug 4). For BAC-4: villain_positions=['BTN', 'CO'] — CO (last) is bettor,
   BTN is caller. For BAC-5: villain_positions=['CO', 'HJ'] — HJ (last) is bettor, CO is caller.

5. PFA-7 templates (BTN opener, CO+SB callers, BB folds): use
   `('preflop', 'BB', 'fold')` in action_history. BB is NOT in villain_positions.

6. Donk DK-N-08 and DK-N-09 (8b_co_calls): villain_positions=['BB', 'CO'].
   CO is last (bettor via BAC bridge logic); BB called the CO bet.

7. After all 8 modules expanded, run E2-B to regenerate Mode B pool. Then re-run C2
   (with working Mode A pool) to produce full 500-hand corpus. Per Phase 5 directive,
   this is Phase 6 scope.
