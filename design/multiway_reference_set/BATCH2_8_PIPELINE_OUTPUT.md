# Batch 2-8 Pipeline Output

**Date:** 2026-04-05
**Pipeline:** Post-Fix (opener-aware ranges, bettor-aware narrowing)
**Hands:** 40 (MW-11 to MW-50)

Each hand run twice: Fixed pipeline (with _opener_position + _bettor_position) and Old pipeline (without).

---

## Full Feature Table

| Ref ID | Axis | Opp | Street | Facing | Fixed Equity | Old Equity | Delta | Better% | Worse% | Hand Cat | Pot Odds | Danger |
|--------|------|-----|--------|--------|-------------|-----------|-------|---------|--------|----------|----------|--------|
| MW-11 | bluff_compre | 3 | Flop | No | 0.085 | 0.092 | -0.007 | 0.997 | 0.000 | high_card | 0.000 | 0.000 |
| MW-12 | bluff_compre | 2 | Flop | No | 0.126 | 0.126 | -0.000 | 0.926 | 0.057 | overcards | 0.000 | 0.000 |
| MW-13 | bluff_compre | 2 | Flop | No | 0.124 | 0.137 | -0.013 | 0.644 | 0.328 | high_card | 0.000 | 0.000 |
| MW-14 | bluff_compre | 2 | Flop | Yes | 0.524 | 0.538 | -0.014 | 0.959 | 0.023 | high_card | 0.268 | 0.250 |
| MW-15 | bluff_compre | 2 | River | No | 0.000 | 0.001 | -0.001 | 0.955 | 0.027 | high_card | 0.000 | 0.420 |
| MW-16 | bluff_compre | 3 | Flop | No | 0.089 | 0.103 | -0.014 | 0.968 | 0.013 | overcards | 0.000 | 0.000 |
| MW-17 | nut_potentia | 2 | Flop | Yes | 0.251 | 0.297 | -0.047 | 0.513 | 0.427 | overcards | 0.268 | 0.250 |
| MW-18 | nut_potentia | 2 | Flop | Yes | 0.359 | 0.404 | -0.045 | 0.954 | 0.046 | one_overcard | 0.268 | 0.250 |
| MW-19 | nut_potentia | 2 | Flop | No | 0.803 | 0.817 | -0.013 | 0.000 | 0.982 | straight | 0.000 | 0.300 |
| MW-20 | nut_potentia | 3 | Flop | Yes | 0.589 | 0.602 | -0.013 | 0.028 | 0.954 | straight | 0.267 | 0.800 |
| MW-21 | nut_potentia | 3 | Flop | Yes | 0.356 | 0.404 | -0.048 | 0.714 | 0.267 | one_overcard | 0.216 | 0.450 |
| MW-22 | nut_potentia | 3 | Flop | No | 0.121 | 0.153 | -0.032 | 0.577 | 0.376 | one_overcard | 0.000 | 0.250 |
| MW-23 | position_amp | 2 | Flop | No | 0.458 | 0.496 | -0.039 | 0.180 | 0.808 | top_pair | 0.000 | 0.000 |
| MW-24 | position_amp | 2 | Flop | No | 0.604 | 0.576 | +0.029 | 0.100 | 0.882 | top_pair | 0.000 | 0.000 |
| MW-25 | position_amp | 3 | Flop | No | 0.337 | 0.353 | -0.016 | 0.912 | 0.087 | high_card | 0.000 | 0.250 |
| MW-26 | position_amp | 3 | Flop | No | 0.368 | 0.372 | -0.004 | 0.808 | 0.192 | high_card | 0.000 | 0.250 |
| MW-27 | position_amp | 2 | Flop | No | 0.476 | 0.507 | -0.031 | 0.132 | 0.862 | overpair | 0.000 | 0.000 |
| MW-28 | position_amp | 2 | Flop | No | 0.561 | 0.578 | -0.017 | 0.076 | 0.921 | overpair | 0.000 | 0.000 |
| MW-29 | aggression_r | 3 | Flop | Yes | 0.254 | 0.417 | -0.163 | 0.213 | 0.780 | top_pair | 0.226 | 0.000 |
| MW-30 | aggression_r | 2 | Flop | Yes | 0.399 | 0.574 | -0.174 | 0.214 | 0.780 | top_pair | 0.184 | 0.000 |
| MW-31 | aggression_r | 1 | Flop | Yes | 0.653 | 0.651 | +0.002 | 0.230 | 0.730 | top_pair | 0.222 | 0.000 |
| MW-32 | aggression_r | 1 | Turn | Yes | 0.538 | 0.538 | +0.000 | 0.420 | 0.562 | top_pair | 0.333 | 0.380 |
| MW-33 | aggression_r | 2 | Flop | Yes | 0.885 | 0.896 | -0.011 | 0.000 | 1.000 | set | 0.167 | 0.300 |
| MW-34 | aggression_r | 2 | Flop | No | 0.666 | 0.668 | -0.002 | 0.054 | 0.939 | overpair | 0.000 | 0.000 |
| MW-35 | spr_interact | 2 | Flop | Yes | 0.474 | 0.521 | -0.047 | 0.180 | 0.814 | top_pair | 0.250 | 0.000 |
| MW-36 | spr_interact | 2 | Flop | Yes | 0.454 | 0.531 | -0.077 | 0.180 | 0.814 | top_pair | 0.268 | 0.000 |
| MW-37 | spr_interact | 2 | Flop | Yes | 0.472 | 0.514 | -0.042 | 0.180 | 0.814 | top_pair | 0.250 | 0.000 |
| MW-38 | spr_interact | 2 | Flop | Yes | 0.422 | 0.440 | -0.017 | 0.799 | 0.151 | one_overcard | 0.333 | 0.250 |
| MW-39 | spr_interact | 2 | Flop | Yes | 0.439 | 0.440 | -0.001 | 0.623 | 0.321 | one_overcard | 0.268 | 0.250 |
| MW-40 | spr_interact | 3 | Flop | No | 0.206 | 0.318 | -0.111 | 0.312 | 0.676 | top_pair | 0.000 | 0.000 |
| MW-41 | range_narrow | 2 | Turn | Yes | 0.253 | 0.327 | -0.074 | 0.441 | 0.552 | middle_pair | 0.231 | 0.880 |
| MW-42 | range_narrow | 1 | River | No | 0.816 | 0.816 | +0.000 | 0.166 | 0.797 | top_pair | 0.000 | 0.420 |
| MW-43 | range_narrow | 3 | River | Yes | 0.087 | 0.182 | -0.095 | 0.479 | 0.521 | middle_pair | 0.400 | 0.420 |
| MW-44 | range_narrow | 2 | Turn | Yes | 0.394 | 0.477 | -0.084 | 0.397 | 0.603 | top_pair | 0.280 | 0.580 |
| MW-45 | range_narrow | 3 | Turn | Yes | 0.478 | 0.686 | -0.207 | 0.090 | 0.910 | set | 0.385 | 0.880 |
| MW-46 | range_narrow | 1 | River | Yes | 0.908 | 0.908 | +0.000 | 0.092 | 0.908 | trips | 0.286 | 0.270 |
| MW-47 | combined_nut | 3 | Flop | Yes | 0.445 | 0.453 | -0.008 | 0.618 | 0.324 | one_overcard | 0.167 | 0.250 |
| MW-48 | combined_blu | 2 | Flop | No | 0.220 | 0.288 | -0.068 | 0.533 | 0.440 | one_overcard | 0.000 | 0.300 |
| MW-49 | combined_pos | 2 | Turn | No | 0.540 | 0.591 | -0.051 | 0.145 | 0.780 | top_pair_good_kicker | 0.000 | 0.380 |
| MW-50 | combined_agg | 2 | Turn | Yes | 0.329 | 0.508 | -0.179 | 0.337 | 0.649 | top_pair | 0.290 | 0.380 |

**Note:** MW-18 redesigned from 9d7d to Qd3d (v2) to eliminate OESD confound.
Pipeline recompute complete. Equity 0.359 (fixed) vs 0.404 (old), delta -0.045.
GTO action: CALL (equity margin +0.091 above pot odds).

---

## Summary Statistics

**Hands with valid output:** 40/40
**Average equity delta (Fixed - Old):** -0.0417
**Min delta:** -0.2075
**Max delta:** +0.0285

### Delta by Axis

| Axis | Hands | Avg Delta | Min Delta | Max Delta |
|------|-------|-----------|-----------|-----------|
| aggression_respect | 6 | -0.0582 | -0.1745 | +0.0023 |
| bluff_compression | 6 | -0.0080 | -0.0138 | -0.0003 |
| combined_aggression_narrowing_position | 1 | -0.1790 | -0.1790 | -0.1790 |
| combined_bluff_spr | 1 | -0.0683 | -0.0683 | -0.0683 |
| combined_nut_position_aggression | 1 | -0.0080 | -0.0080 | -0.0080 |
| combined_position_range_narrowing | 1 | -0.0508 | -0.0508 | -0.0508 |
| nut_potential | 6 | -0.0220 | -0.0479 | +0.0203 |
| position_amplification | 6 | -0.0130 | -0.0390 | +0.0285 |
| range_narrowing | 6 | -0.0766 | -0.2075 | +0.0000 |
| spr_interaction | 6 | -0.0491 | -0.1113 | -0.0008 |

---

## Notes on Range Construction

- **Fixed pipeline:** Each opponent assigned the correct range based on their preflop role.
  - Opener (e.g., CO) gets RFI range for that position.
  - Callers (e.g., BTN, BB) get DEFEND range vs opener's position.
  - Bettor's range is narrowed to the betting range when `_bettor_position` is set.
  - Non-betting opponents retain full preflop calling ranges.
- **Old pipeline:** `_opener_position` and `_bettor_position` not provided.
  - Falls back to heuristic: earlier-position player gets RFI, others get DEFEND vs hero.
  - This assigns RFI ranges incorrectly in multiway pots, inflating hero equity.
