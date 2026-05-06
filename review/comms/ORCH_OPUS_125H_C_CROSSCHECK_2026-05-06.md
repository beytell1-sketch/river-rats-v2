# Opus tier-up cross-check on 20 hands (12.5H-C labelling round)

## Per-hand verdict

### PILOT_689 (manuals) — Sonnet: CHECK (1.0)
- Hero: Ks7h on As9s5s monotone, BTN, 4-way, checked to BTN, no bet yet.
- Composition: villain_air 0.34, TP+ 0.19, draws 0.00; raw_equity 0.351; better_hand_pct 0.83; non-nut FD (no nut blocker); 7 kicker is dominated.
- DO NOT Rule 2 fires hard: 3+ opponents on monotone board + non-nut FD + dominated kicker. With 83% of villain combos better and 4-way pot, betting is punished by both made hands and other flush draws.
- Opus verdict: CHECK
- Match: Y

### PILOT_690 (manuals) — Sonnet: CHECK (0.6)
- Hero: AsKh on Js9s3s monotone, BTN, 4-way, checked to BTN.
- Composition: villain_air 0.44, TP+ 0.25, draws 0.04; raw_equity 0.378; nut_flush_block=1 (As); 4-way monotone.
- Hero has nut blocker but is a one-card NFD only (As alone, Kh offsuit). Equity is realised by check (free turn for flush). DO NOT Rule 2: monotone, 3 opponents — leading is poor even with nut blocker because (a) hero only has one-card NFD, not a 5-card flush draw, (b) 4-way folds out the air without value from worse made hands, (c) NFD blocker carve-out applies to facing aggression scenarios, not unprovoked flop bets into 3 opponents.
- Opus verdict: CHECK
- Match: Y

### PILOT_691 (manuals) — Sonnet: BET (0.8)
- Hero: AhTs on AcJc5d, BTN, 4-way, checked to BTN.
- Composition: air 0.27, TP+ 0.21, draws 0.04; raw_equity 0.181 — but better_hand_pct 0.136 (most of villain range is below TP).
- Hero has top-pair-decent-kicker on dry-ish two-tone board. raw_equity looks low because removed villain combos that beat hero are concentrated (AK/AQ/AJ/sets). better_hand_pct 0.136 means 86% of range is below TPTK. Small bet for protection vs 3 backdoor draws + thin value from worse Ax/J-x/5x is standard.
- Opus verdict: BET
- Match: Y

### PILOT_692 (manuals) — Sonnet: RAISE (1.0)
- Hero: 6d6c on AcKd6hQs (turn), BB, 4-way, BB check, faces bet+call.
- Composition: air 0.07, TP+ 0.48, draws 0.025; raw_equity 0.501; is_monster=1 (set on dynamic turn); pot_odds 0.255; danger_score 0.88.
- Bottom set on AKQ6 turn — extremely vulnerable to JT (made straight) which is in TP+ range, plus tons of TP/TT pair+draw. Flatting is dominated by pot-control logic for non-nut sets, but with one already called and another behind, raise to charge AK/AQ/KQ two-pair + protect vs straight draws is correct. Bet+call indicates wide value, raising for protection on vulnerable set is standard line.
- Opus verdict: RAISE
- Match: Y

### PILOT_693 (manuals) — Sonnet: RAISE (1.0)
- Hero: AdKd on Jd8d4c, BB, 3-way, BB check, faces bet (no call yet).
- Composition: air 0.31, TP+ 0.39, draws 0.023; raw_equity 0.463; nut_flush_block=1; bet only (num_callers_to_bet=0). Two opponents.
- v3.4 carve-out check (bet+call multi-way): num_callers_to_bet=0 → NOT bet+call multi-way. So default v3.2 KB §1.7 applies. NFD + nut blocker, villain_air_pct=0.31 ≥ 0.20 → RAISE per v3.2 default. Air is well above 0.20 threshold; nut blocker; OOP; 35%+ raw equity. Standard raise.
- Opus verdict: RAISE
- Match: Y

### PILOT_694 (manuals) — Sonnet: RAISE (0.8)
- Hero: AsQs on KsJd5s, BB, 4-way, BB check, faces bet+call.
- Composition: air 0.17, TP+ 0.36, draws 0.11; raw_equity 0.405; nut_flush_block=1; flush_draw_block_pct 0.80; has_straight_draw=1; bet+call (num_callers_to_bet=1).
- v3.4 Fix 2.1 multi-way bet+call carve-out: (a) NFD + nut blocker ✓, (b) OOP ✓, (c) bet+call no raise ✓, (d) raw_equity 0.405 ≥ 0.35 ✓, (e) air 0.17 ≥ 0.05 ✓. Carve-out triggers. Combined nut FD + open-ended (BDSD broadway gutter) gives massive equity, blocker effect on AK/AQ/AJ huge. RAISE.
- Opus verdict: RAISE
- Match: Y

### PILOT_647 (T7-ext_CALL) — Sonnet: CALL (1.0)
- Hero: AhKh on Jh9h3c, BB, 2-way, faces bet.
- Composition: villain_air 0.0469 (below 0.05 floor), TP+ 0.29, draws 0.47; raw_equity 0.478; nut_flush_block=1; bet only (no call); OOP.
- v3.4 Fix 2.1.1 floor: villain_air 0.0469 < 0.05 → carve-out does NOT trigger. v3.2 default KB §1.7 applies: villain_air < 0.20 → CALL preferred even with nut blocker. Air-starved range (huge draw% means villain has it most of the time), raising folds out the only worse hands and gets called by everything that beats us.
- Opus verdict: CALL
- Match: Y

### PILOT_648 (T7-ext_CALL) — Sonnet: CALL (1.0)
- Hero: AhQh on Jh9h3c, BB, 2-way, faces bet.
- Composition: air 0.0469 (<0.05), TP+ 0.29, draws 0.47; raw_equity 0.454; nut_flush_block=1.
- Identical structure to PILOT_647. Floor fails (air 0.0469 < 0.05) → v3.2 default → CALL. Q kicker slightly worse than K but same logic.
- Opus verdict: CALL
- Match: Y

### PILOT_649 (T7-ext_CALL) — Sonnet: CALL (1.0)
- Hero: AhKh on Th7h3c, BB, 2-way, faces bet.
- Composition: air 0.0614 (just above 0.05 floor), TP+ 0.31, draws 0.44; raw_equity 0.503; nut_flush_block=1.
- Floor (e) passes barely. But v3.4 carve-out (Fix 2.1) requires bet+call multi-way (num_callers_to_bet ≥ 1). Here num_callers_to_bet=0 (bet only, no caller yet). So carve-out does NOT trigger; we evaluate under v3.2 default KB §1.7. With villain_air 0.0614 < 0.20 → CALL preferred. Sonnet correct.
- Opus verdict: CALL
- Match: Y

### PILOT_650 (T7-ext_CALL) — Sonnet: CALL (1.0)
- Hero: AhQh on Th9h3c, BB, 2-way, faces bet.
- Composition: air 0.0466 (<0.05 floor), TP+ 0.31, draws 0.45; raw_equity 0.450; nut_flush_block=1.
- Floor fails (0.0466 < 0.05) → carve-out off → v3.2 default → CALL.
- Opus verdict: CALL
- Match: Y

### PILOT_651 (T7-ext_RAISE) — Sonnet: RAISE (1.0)
- Hero: AdKd on Jd9d3c, BB, 2-way, faces bet (no call).
- Composition: air 0.282, TP+ 0.38, draws 0.067; raw_equity 0.458; nut_flush_block=1; num_callers_to_bet=0.
- Bet only (no caller) → not in carve-out scope. v3.2 default KB §1.7: villain_air 0.282 ≥ 0.20 → RAISE. Standard NFD + nut blocker raise into single bettor with sufficient air.
- Opus verdict: RAISE
- Match: Y

### PILOT_654 (T7-ext_RAISE) — Sonnet: RAISE (1.0)
- Hero: AsKs on Js9s3c, BB, 2-way, faces bet.
- Composition: air 0.282, TP+ 0.38, draws 0.067; raw_equity 0.467; nut_flush_block=1.
- Same structure as PILOT_651, different suit. air 0.282 ≥ 0.20, nut FD + nut blocker → RAISE.
- Opus verdict: RAISE
- Match: Y

### PILOT_656 (T7-ext_RAISE) — Sonnet: RAISE (1.0)
- Hero: AcKc on Jc9c3d, BB, 2-way, faces bet.
- Composition: air 0.282, TP+ 0.38, draws 0.067; raw_equity 0.464; nut_flush_block=1.
- Same logic. air ≥ 0.20 → RAISE.
- Opus verdict: RAISE
- Match: Y

### PILOT_657 (T7-ext_RAISE) — Sonnet: RAISE (1.0)
- Hero: AcQc on Jc9c3d, BB, 2-way, faces bet.
- Composition: air 0.282, TP+ 0.38, draws 0.067; raw_equity 0.432; nut_flush_block=1.
- Q kicker but still nut FD + nut Ace blocker, air 0.282 ≥ 0.20 → RAISE per v3.2 default.
- Opus verdict: RAISE
- Match: Y

### PILOT_605 (T8_sanity) — Sonnet: CHECK (1.0)
- Hero: KsQh on Js9s4s monotone, BTN, 4-way, checked to BTN, no bet.
- Composition: air 0.44, TP+ 0.26, draws 0.04; raw_equity 0.274; non-nut FD (Ks, no Ace); has_straight_draw=1 (KQ on JT9 needs T... actually KQ on J94, only inside straight needs to check — likely BD-straight); better_hand_pct 0.84.
- DO NOT Rule 2: 3+ opponents monotone, no nut blocker, dominated by AsX flushes. CHECK is mandatory.
- Opus verdict: CHECK
- Match: Y

### PILOT_610 (T8_sanity) — Sonnet: CHECK (1.0)
- Hero: KsQc on 9s7s3s monotone, BTN, 4-way.
- Composition: air 0.55, TP+ 0.21, draws 0.0; raw_equity 0.216; non-nut FD; better_hand_pct 0.75.
- DO NOT Rule 2: monotone, 3+ opponents, dominated FD. Despite high air%, leading bet bloats pot with dominated draw and folds out only equity we're already crushing. CHECK.
- Opus verdict: CHECK
- Match: Y

### PILOT_615 (T8_sanity) — Sonnet: CHECK (1.0)
- Hero: AhJc on Th7h4h monotone, BTN, 4-way.
- Composition: air 0.0, TP+ 0.60, draws 0.13; raw_equity 0.364; nut_flush_block=1; better_hand_pct 0.60.
- Air 0.0 means range is entirely value+draws. Nut FD blocker + nut Ace, but on monotone board into 3 opponents, betting is dominated by DO NOT Rule 2 and by composition (60% TP+ range, no air to fold out). CHECK to realise equity / pot-control.
- Opus verdict: CHECK
- Match: Y

### PILOT_676 (T-CONTROL_sanity) — Sonnet: BET (1.0)
- Hero: KsTs on KhTc5d, BB, 2-way, BB-call preflop, no aggression.
- Composition: air 0.37, TP+ 0.17, draws 0.03; raw_equity 0.709; is_strong_made=1 (top two pair); better_hand_pct 0.034.
- Top two on dry-ish board, 96.6% of villain range is below us. Tons of value to extract from Kx/Tx + protection vs gutters/BDFD. BET.
- Opus verdict: BET
- Match: Y

### PILOT_680 (T-CONTROL_sanity) — Sonnet: FOLD (1.0)
- Hero: 7d4s on AcKh9c, BB, HU, faces bet.
- Composition: raw_equity 0.065; better_hand_pct 0.996; no draw, no SDV.
- Trivial fold — 6.5% equity vs 27.8% pot odds, no equity to call.
- Opus verdict: FOLD
- Match: Y

### PILOT_686 (T-CONTROL_sanity) — Sonnet: CALL (1.0)
- Hero: AsTd on Tc8d3s, BB, HU, faces bet.
- Composition: air 0.28, TP+ 0.40, draws 0.04; raw_equity 0.659; is_made_hand=1 (TP-top kicker); better_hand_pct 0.20.
- TPTK on dry board. CALL is standard — keeps villain's bluffs/worse Tx in, avoids bloating against the few overpairs/sets that crush us. Raising folds out air and only gets called by better.
- Opus verdict: CALL
- Match: Y

## Agreement summary

| pid | cohort | sonnet | opus | match |
| --- | --- | --- | --- | --- |
| PILOT_689 | manuals | CHECK | CHECK | Y |
| PILOT_690 | manuals | CHECK | CHECK | Y |
| PILOT_691 | manuals | BET | BET | Y |
| PILOT_692 | manuals | RAISE | RAISE | Y |
| PILOT_693 | manuals | RAISE | RAISE | Y |
| PILOT_694 | manuals | RAISE | RAISE | Y |
| PILOT_647 | T7-ext_CALL | CALL | CALL | Y |
| PILOT_648 | T7-ext_CALL | CALL | CALL | Y |
| PILOT_649 | T7-ext_CALL | CALL | CALL | Y |
| PILOT_650 | T7-ext_CALL | CALL | CALL | Y |
| PILOT_651 | T7-ext_RAISE | RAISE | RAISE | Y |
| PILOT_654 | T7-ext_RAISE | RAISE | RAISE | Y |
| PILOT_656 | T7-ext_RAISE | RAISE | RAISE | Y |
| PILOT_657 | T7-ext_RAISE | RAISE | RAISE | Y |
| PILOT_605 | T8_sanity | CHECK | CHECK | Y |
| PILOT_610 | T8_sanity | CHECK | CHECK | Y |
| PILOT_615 | T8_sanity | CHECK | CHECK | Y |
| PILOT_676 | T-CONTROL_sanity | BET | BET | Y |
| PILOT_680 | T-CONTROL_sanity | FOLD | FOLD | Y |
| PILOT_686 | T-CONTROL_sanity | CALL | CALL | Y |

## Per-cohort
- manuals: 6/6
- T7-ext_CALL: 4/4
- T7-ext_RAISE: 4/4
- T8_sanity: 3/3
- T-CONTROL_sanity: 3/3

Total: 20/20 agreement.

## Verdict per dispatch agreement criteria
- ≥18/20 agreement → LABELS FINAL
- 3-5 disagreement → PARTIAL (per-hand decision)
- ≥6 disagreement → MATERIAL (full Opus relabel)

Final: **LABELS FINAL** (20/20)

## Notes
- T7-ext_CALL cohort cleanly demonstrates v3.4 Fix 2.1.1 floor in action: PILOT_647/648/650 all have villain_air 0.046–0.047 (below 0.05 floor) and Sonnet correctly defaulted to CALL via v3.2. PILOT_649 sits at 0.0614 (above floor) but the carve-out additionally requires bet+call multi-way (num_callers_to_bet ≥ 1) which is not met (single bettor, no caller), so v3.2 default still applies → CALL. Sonnet labelled all four CALL — consistent with v3.4.
- T7-ext_RAISE cohort (PILOT_651/654/656/657) all sit at villain_air 0.282 — comfortably ≥ 0.20 v3.2 threshold — and Sonnet correctly applied default RAISE. These are not v3.4 carve-out cases (no caller); they are vanilla v3.2 NFD+nut-blocker RAISEs.
- T8_sanity (PILOT_605/610/615) all CHECK on monotone 4-way boards, correctly applying DO NOT Rule 2 even when nut blocker present (PILOT_615) — composition reasoning over preflop label dominates.
- Manuals cover the spectrum (passive CHECK, thin BET, vulnerable set RAISE, NFD+blocker RAISE in 3-way bet-only, NFD+blocker RAISE in 4-way bet+call carve-out) — Sonnet's threshold discrimination across 0.05 / 0.20 is clean.
- Confidence calibration: PILOT_690 (0.6) and PILOT_691/694 (0.8) are the closer manuals; agreement on these still holds. The single 0.6 hand is the marginal monotone-4-way nut-blocker check, where the OOP/IP and bet/no-bet status legitimately complicate things — but DO NOT Rule 2 governs.
