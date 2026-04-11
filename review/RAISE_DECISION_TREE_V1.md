# RAISE Decision Tree v1 — For Labelling Agent

**Date:** 9 April 2026
**Source:** GTO Expert synthesis of Research A (28 sources) + Research B (52-feature analysis)
**Status:** AWAITING REVIEW + OWNER APPROVAL

---

## Preamble

Every branch must be explainable using ONLY the 52-feature vector.
If the reason requires suit-specific blocker logic not captured by
flush_block_pct or flush_draw_rank, label CALL.

---

## Step 1 — Flat Spot Check (no hand should raise)

If ANY of these is true → CALL (do not proceed):

A. num_callers_to_bet >= 1 AND is_monster == 0
   → Bet-and-call, non-monster = always CALL

B. board_favour <= -0.30 AND villain_range_capped == 0
   → Board heavily favours villain's uncapped range = CALL

C. villain_aggression_count >= 2 AND is_monster == 0
   → Multi-street aggressor, non-monster = CALL

D. Sandwich position (player behind hasn't acted) AND NOT
   (is_monster == 1 AND spr <= 2.0)
   → Third player behind = CALL unless committed monster

---

## Step 2 — Monster Value Raise

Condition: is_monster == 1

Suppressors (any fires → CALL instead of RAISE):

S1. flush_danger >= 0.60 AND hand is not two-pair+
S2. flush_danger >= 0.60 AND is_paired == 1 (flush on paired board)
S3. villain_aggression_count >= 2
S4. spr >= 4.0 AND is_ip == 1 (high SPR IP = pot control)
S5. num_callers_to_bet >= 1 AND hero_range_percentile < 0.92

No suppressor fires → **RAISE** (Value). Confidence: HIGH.

---

## Step 3 — Low SPR Commit

Condition: spr <= 1.5 AND hero_range_percentile >= 0.80

→ **RAISE** (Stack-off). Confidence: HIGH.

---

## Step 4 — Thin Value OOP Check-Raise

ALL required:
- hero_range_percentile >= 0.75
- is_monster == 0
- is_ip == 0 (OOP only)
- villain_fold_equity_estimate >= 0.30
- villain_aggression_count <= 1
- flush_danger <= 0.35
- straight_danger <= 0.35
- num_callers_to_bet == 0

→ **RAISE** (Thin Value Check-Raise). Confidence: MEDIUM.

Note: IP thin value at percentile >= 0.75 with is_monster == 0 = CALL.

---

## Step 5 — Semi-Bluff Raise

ALL required:
- draw_outs >= 9 (nut-quality draw)
- villain_fold_equity_estimate >= 0.45
- villain_aggression_count <= 1
- is_paired == 0 (no draws on paired boards)

→ **RAISE** (Semi-Bluff). Confidence: MEDIUM.

---

## Step 6 — Bluff Raise (river / zero equity)

ALL required:
- hero_range_percentile <= 0.20
- villain_fold_equity_estimate >= 0.50
- villain_top_pair_plus_pct <= 0.35
- num_callers_to_bet == 0
- villain_aggression_count == 0

→ **RAISE** (Bluff). Confidence: LOW.

---

## Default

No step returned RAISE → **CALL** (or BET/CHECK if not facing bet).

---

## Quick Reference: Monsters That Should CALL

- Sets on dry boards IP at SPR >= 4 (S4)
- Nut flush on paired board (S2)
- Any monster facing multi-street aggression (S3)
- Monster in sandwich without low SPR (Step 1D)
- Monster facing bet-and-call below top 8% of range (S5)
