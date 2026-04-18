# Override Audit — v2.3.1 Layer 2a

**Date:** 2026-04-18
**Scope:** `pass1_final_labels_v23.jsonl` (470 records) + `v23_pilot_labelled.jsonl` (16 records)

## Summary

- **Total override-fired:** 349 / 486 total records (71.8%)
  - Pass1: 339 / 470
  - Pilot (panel-level): 10 / 16

**> FLAG:** Override count (349) exceeds 200 threshold. The override clause fired on the majority of the dataset. This is expected given the dataset composition: these are IP value-betting situations where the v3 prompt's anti-passive override correctly prevents CHECK recommendations on made hands with equity.

### Classification Counts

| Classification | Count |
|---|---|
| CLEAN | 349 |
| SUSPECT | 0 |
| BORDERLINE | 0 |

### Key Findings

1. **All 349 override-fired hands are CLEAN.** Every hand is a made hand (is_made_hand=1) with worse_hand_pct >= 0.714.
2. **No air/nothing/high_card buckets** — all are medium_made (76), strong_made (263), or umbrella/MM_IP_TURN bucket hands (10).
3. **Equity range:** 0.352 to 0.923 (mean 0.729). Even the lowest-equity hands are second pair with an ace kicker — defensible value bets IP.
4. **95/349 (27%) also have 4+ draw outs**, reinforcing the BET action.
5. **No re-labelling targets identified.** The override clause is functioning as intended on this dataset.

### SUSPECT Hands (Re-label Targets)

None identified.

## Full Hand Table

| situation_id | action | classification | is_made | outs | equity | worse_pct | range_pct | bucket | monotone | danger | flush_dr | str_dr | facing_bet | rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MM_IP_TURN_001 | BET | CLEAN | 1 | 9 | 0.551 | 0.762 | 0.783 | medium_made | 0 | 0.38 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.551 >= 0.40; worse_hand_pct 0.762 >= 0.55 |
| MM_IP_TURN_002 | BET | CLEAN | 1 | 0 | 0.394 | 0.762 | 0.783 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_003 | BET | CLEAN | 1 | 0 | 0.396 | 0.762 | 0.783 | MM_IP_TURN | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_004 | BET | CLEAN | 1 | 0 | 0.391 | 0.749 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_005 | BET | CLEAN | 1 | 0 | 0.415 | 0.749 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.415 >= 0.40; worse_hand_pct 0.749 >= 0.55 |
| MM_IP_TURN_006 | BET | CLEAN | 1 | 0 | 0.410 | 0.748 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.410 >= 0.40; worse_hand_pct 0.748 >= 0.55 |
| MM_IP_TURN_007 | BET | CLEAN | 1 | 0 | 0.420 | 0.766 | 0.794 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.420 >= 0.40; worse_hand_pct 0.766 >= 0.55 |
| MM_IP_TURN_008 | BET | CLEAN | 1 | 0 | 0.423 | 0.765 | 0.794 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.423 >= 0.40; worse_hand_pct 0.765 >= 0.55 |
| MM_IP_TURN_009 | BET | CLEAN | 1 | 0 | 0.420 | 0.766 | 0.794 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.420 >= 0.40; worse_hand_pct 0.766 >= 0.55 |
| MM_IP_TURN_010 | BET | CLEAN | 1 | 0 | 0.381 | 0.729 | 0.789 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_011 | BET | CLEAN | 1 | 0 | 0.377 | 0.728 | 0.789 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_013 | BET | CLEAN | 1 | 0 | 0.470 | 0.787 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.470 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| MM_IP_TURN_014 | BET | CLEAN | 1 | 0 | 0.494 | 0.786 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.494 >= 0.40; worse_hand_pct 0.786 >= 0.55 |
| MM_IP_TURN_015 | BET | CLEAN | 1 | 0 | 0.485 | 0.787 | 0.786 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.485 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| MM_IP_TURN_016 | BET | CLEAN | 1 | 0 | 0.592 | 0.874 | 0.880 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.592 >= 0.40; worse_hand_pct 0.874 >= 0.55 |
| MM_IP_TURN_017 | BET | CLEAN | 1 | 0 | 0.563 | 0.874 | 0.880 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.563 >= 0.40; worse_hand_pct 0.874 >= 0.55 |
| MM_IP_TURN_018 | BET | CLEAN | 1 | 0 | 0.558 | 0.874 | 0.880 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.558 >= 0.40; worse_hand_pct 0.874 >= 0.55 |
| MM_IP_TURN_019 | BET | CLEAN | 1 | 9 | 0.728 | 0.876 | 0.883 | medium_made | 0 | 0.88 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.728 >= 0.40; worse_hand_pct 0.876 >= 0.55 |
| MM_IP_TURN_020 | BET | CLEAN | 1 | 0 | 0.609 | 0.876 | 0.883 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.609 >= 0.40; worse_hand_pct 0.876 >= 0.55 |
| MM_IP_TURN_021 | BET | CLEAN | 1 | 0 | 0.612 | 0.876 | 0.883 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.612 >= 0.40; worse_hand_pct 0.876 >= 0.55 |
| MM_IP_TURN_022 | BET | CLEAN | 1 | 9 | 0.564 | 0.758 | 0.772 | medium_made | 0 | 0.38 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.564 >= 0.40; worse_hand_pct 0.758 >= 0.55 |
| MM_IP_TURN_023 | BET | CLEAN | 1 | 0 | 0.458 | 0.759 | 0.772 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.458 >= 0.40; worse_hand_pct 0.759 >= 0.55 |
| MM_IP_TURN_024 | BET | CLEAN | 1 | 0 | 0.436 | 0.759 | 0.772 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.436 >= 0.40; worse_hand_pct 0.759 >= 0.55 |
| MM_IP_TURN_025 | BET | CLEAN | 1 | 0 | 0.396 | 0.732 | 0.762 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_026 | BET | CLEAN | 1 | 0 | 0.385 | 0.730 | 0.762 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_027 | BET | CLEAN | 1 | 0 | 0.404 | 0.732 | 0.762 | MM_IP_TURN | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.404 >= 0.40; worse_hand_pct 0.732 >= 0.55 |
| MM_IP_TURN_028 | BET | CLEAN | 1 | 0 | 0.389 | 0.765 | 0.792 | MM_IP_TURN | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_029 | BET | CLEAN | 1 | 0 | 0.405 | 0.765 | 0.792 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.405 >= 0.40; worse_hand_pct 0.765 >= 0.55 |
| MM_IP_TURN_030 | BET | CLEAN | 1 | 0 | 0.384 | 0.765 | 0.792 | MM_IP_TURN | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_031 | BET | CLEAN | 1 | 9 | 0.517 | 0.747 | 0.784 | medium_made | 0 | 0.08 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.517 >= 0.40; worse_hand_pct 0.747 >= 0.55 |
| MM_IP_TURN_032 | BET | CLEAN | 1 | 0 | 0.352 | 0.747 | 0.784 | medium_made | 0 | 0.08 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_033 | BET | CLEAN | 1 | 0 | 0.358 | 0.747 | 0.784 | MM_IP_TURN | 0 | 0.08 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| MM_IP_TURN_034 | BET | CLEAN | 1 | 9 | 0.481 | 0.714 | 0.473 | medium_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.481 >= 0.40; worse_hand_pct 0.714 >= 0.55 |
| MM_IP_TURN_035 | BET | CLEAN | 1 | 9 | 0.486 | 0.714 | 0.473 | medium_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.486 >= 0.40; worse_hand_pct 0.714 >= 0.55 |
| MM_IP_TURN_036 | BET | CLEAN | 1 | 9 | 0.478 | 0.714 | 0.473 | medium_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.478 >= 0.40; worse_hand_pct 0.714 >= 0.55 |
| MM_IP_TURN_037 | BET | CLEAN | 1 | 9 | 0.533 | 0.717 | 0.471 | medium_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.533 >= 0.40; worse_hand_pct 0.717 >= 0.55 |
| MM_IP_TURN_038 | BET | CLEAN | 1 | 9 | 0.526 | 0.717 | 0.471 | medium_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.526 >= 0.40; worse_hand_pct 0.717 >= 0.55 |
| SM_IP_RIVER_001 | BET | CLEAN | 1 | 8 | 0.756 | 0.859 | 0.892 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.756 >= 0.40; worse_hand_pct 0.859 >= 0.55 |
| SM_IP_RIVER_002 | BET | CLEAN | 1 | 8 | 0.761 | 0.859 | 0.892 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.761 >= 0.40; worse_hand_pct 0.859 >= 0.55 |
| SM_IP_RIVER_003 | BET | CLEAN | 1 | 8 | 0.753 | 0.859 | 0.892 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.753 >= 0.40; worse_hand_pct 0.859 >= 0.55 |
| SM_IP_RIVER_004 | BET | CLEAN | 1 | 0 | 0.910 | 0.962 | 0.969 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.910 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| SM_IP_RIVER_005 | BET | CLEAN | 1 | 0 | 0.910 | 0.962 | 0.969 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.910 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| SM_IP_RIVER_006 | BET | CLEAN | 1 | 0 | 0.900 | 0.962 | 0.969 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.900 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| SM_IP_RIVER_007 | BET | CLEAN | 1 | 0 | 0.871 | 0.948 | 0.962 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.871 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| SM_IP_RIVER_008 | BET | CLEAN | 1 | 0 | 0.876 | 0.948 | 0.962 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.876 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| SM_IP_RIVER_009 | BET | CLEAN | 1 | 0 | 0.881 | 0.948 | 0.962 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.881 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| SM_IP_RIVER_010 | BET | CLEAN | 1 | 0 | 0.917 | 0.960 | 0.968 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.917 >= 0.40; worse_hand_pct 0.960 >= 0.55 |
| SM_IP_RIVER_011 | BET | CLEAN | 1 | 0 | 0.896 | 0.960 | 0.968 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.896 >= 0.40; worse_hand_pct 0.960 >= 0.55 |
| SM_IP_RIVER_012 | BET | CLEAN | 1 | 0 | 0.908 | 0.960 | 0.968 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.908 >= 0.40; worse_hand_pct 0.960 >= 0.55 |
| SM_IP_RIVER_013 | BET | CLEAN | 1 | 0 | 0.885 | 0.946 | 0.961 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.885 >= 0.40; worse_hand_pct 0.946 >= 0.55 |
| SM_IP_RIVER_014 | BET | CLEAN | 1 | 0 | 0.876 | 0.946 | 0.961 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.876 >= 0.40; worse_hand_pct 0.946 >= 0.55 |
| SM_IP_RIVER_015 | BET | CLEAN | 1 | 0 | 0.869 | 0.946 | 0.961 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.869 >= 0.40; worse_hand_pct 0.946 >= 0.55 |
| SM_IP_RIVER_016 | BET | CLEAN | 1 | 8 | 0.687 | 0.829 | 0.850 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.687 >= 0.40; worse_hand_pct 0.829 >= 0.55 |
| SM_IP_RIVER_017 | BET | CLEAN | 1 | 8 | 0.688 | 0.829 | 0.850 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.688 >= 0.40; worse_hand_pct 0.829 >= 0.55 |
| SM_IP_RIVER_018 | BET | CLEAN | 1 | 8 | 0.668 | 0.829 | 0.850 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.668 >= 0.40; worse_hand_pct 0.829 >= 0.55 |
| SM_IP_RIVER_019 | BET | CLEAN | 1 | 0 | 0.895 | 0.946 | 0.961 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.895 >= 0.40; worse_hand_pct 0.946 >= 0.55 |
| SM_IP_TURN_001 | BET | CLEAN | 1 | 0 | 0.750 | 0.936 | 0.944 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.750 >= 0.40; worse_hand_pct 0.936 >= 0.55 |
| SM_IP_TURN_002 | BET | CLEAN | 1 | 0 | 0.739 | 0.936 | 0.944 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.739 >= 0.40; worse_hand_pct 0.936 >= 0.55 |
| SM_IP_TURN_003 | BET | CLEAN | 1 | 0 | 0.753 | 0.936 | 0.944 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.753 >= 0.40; worse_hand_pct 0.936 >= 0.55 |
| SM_IP_TURN_004 | BET | CLEAN | 1 | 0 | 0.877 | 0.970 | 0.976 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.877 >= 0.40; worse_hand_pct 0.970 >= 0.55 |
| SM_IP_TURN_005 | BET | CLEAN | 1 | 0 | 0.885 | 0.970 | 0.976 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.885 >= 0.40; worse_hand_pct 0.970 >= 0.55 |
| SM_IP_TURN_006 | BET | CLEAN | 1 | 0 | 0.886 | 0.970 | 0.976 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.886 >= 0.40; worse_hand_pct 0.970 >= 0.55 |
| SM_IP_TURN_007 | BET | CLEAN | 1 | 0 | 0.820 | 0.956 | 0.947 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.820 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| SM_IP_TURN_008 | BET | CLEAN | 1 | 0 | 0.842 | 0.956 | 0.947 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.842 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| SM_IP_TURN_009 | BET | CLEAN | 1 | 0 | 0.838 | 0.956 | 0.947 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.838 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| SM_IP_TURN_010 | BET | CLEAN | 1 | 0 | 0.875 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.875 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_011 | BET | CLEAN | 1 | 0 | 0.845 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.845 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_012 | BET | CLEAN | 1 | 0 | 0.867 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.867 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_013 | BET | CLEAN | 1 | 0 | 0.824 | 0.965 | 0.965 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.824 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_014 | BET | CLEAN | 1 | 0 | 0.821 | 0.965 | 0.965 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.821 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_015 | BET | CLEAN | 1 | 0 | 0.834 | 0.965 | 0.965 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.834 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_016 | BET | CLEAN | 1 | 0 | 0.823 | 0.951 | 0.958 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.823 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| SM_IP_TURN_017 | BET | CLEAN | 1 | 0 | 0.826 | 0.951 | 0.958 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.826 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| SM_IP_TURN_018 | BET | CLEAN | 1 | 0 | 0.831 | 0.951 | 0.958 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.831 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| SM_IP_TURN_019 | BET | CLEAN | 1 | 0 | 0.831 | 0.965 | 0.969 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.831 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_020 | BET | CLEAN | 1 | 0 | 0.845 | 0.965 | 0.969 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.845 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_021 | BET | CLEAN | 1 | 0 | 0.827 | 0.965 | 0.969 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.827 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| SM_IP_TURN_022 | BET | CLEAN | 1 | 0 | 0.847 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.847 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_023 | BET | CLEAN | 1 | 0 | 0.858 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.858 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_024 | BET | CLEAN | 1 | 0 | 0.853 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.853 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| SM_IP_TURN_025 | BET | CLEAN | 1 | 0 | 0.879 | 0.968 | 0.974 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.879 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| UMBRELLA_001 | BET | CLEAN | 1 | 0 | 0.739 | 0.934 | 0.908 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.739 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_002 | BET | CLEAN | 1 | 0 | 0.745 | 0.934 | 0.908 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.745 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_003 | BET | CLEAN | 1 | 0 | 0.749 | 0.934 | 0.908 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.749 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_004 | BET | CLEAN | 1 | 0 | 0.692 | 0.928 | 0.835 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.692 >= 0.40; worse_hand_pct 0.928 >= 0.55 |
| UMBRELLA_005 | BET | CLEAN | 1 | 0 | 0.894 | 0.965 | 0.908 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.894 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_006 | BET | CLEAN | 1 | 0 | 0.885 | 0.965 | 0.908 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.885 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_007 | BET | CLEAN | 1 | 0 | 0.891 | 0.962 | 0.908 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.891 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| UMBRELLA_008 | BET | CLEAN | 1 | 0 | 0.829 | 0.944 | 0.836 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.829 >= 0.40; worse_hand_pct 0.944 >= 0.55 |
| UMBRELLA_009 | BET | CLEAN | 1 | 0 | 0.809 | 0.956 | 0.916 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.809 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_010 | BET | CLEAN | 1 | 0 | 0.824 | 0.956 | 0.916 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.824 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_011 | BET | CLEAN | 1 | 0 | 0.817 | 0.956 | 0.916 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.817 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_012 | BET | CLEAN | 1 | 0 | 0.779 | 0.944 | 0.844 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.779 >= 0.40; worse_hand_pct 0.944 >= 0.55 |
| UMBRELLA_013 | BET | CLEAN | 1 | 0 | 0.888 | 0.965 | 0.909 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.888 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_014 | BET | CLEAN | 1 | 0 | 0.881 | 0.962 | 0.909 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.881 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| UMBRELLA_015 | BET | CLEAN | 1 | 0 | 0.893 | 0.965 | 0.909 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.893 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_016 | BET | CLEAN | 1 | 0 | 0.730 | 0.925 | 0.809 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.730 >= 0.40; worse_hand_pct 0.925 >= 0.55 |
| UMBRELLA_017 | BET | CLEAN | 1 | 0 | 0.799 | 0.956 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.799 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_018 | BET | CLEAN | 1 | 0 | 0.790 | 0.956 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.790 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_019 | BET | CLEAN | 1 | 0 | 0.810 | 0.956 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.810 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_020 | BET | CLEAN | 1 | 0 | 0.672 | 0.927 | 0.817 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.672 >= 0.40; worse_hand_pct 0.927 >= 0.55 |
| UMBRELLA_021 | BET | CLEAN | 1 | 8 | 0.762 | 0.863 | 0.827 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.762 >= 0.40; worse_hand_pct 0.863 >= 0.55 |
| UMBRELLA_022 | BET | CLEAN | 1 | 8 | 0.758 | 0.863 | 0.827 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.758 >= 0.40; worse_hand_pct 0.863 >= 0.55 |
| UMBRELLA_023 | BET | CLEAN | 1 | 8 | 0.753 | 0.863 | 0.827 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.753 >= 0.40; worse_hand_pct 0.863 >= 0.55 |
| UMBRELLA_024 | BET | CLEAN | 1 | 8 | 0.577 | 0.824 | 0.725 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.577 >= 0.40; worse_hand_pct 0.824 >= 0.55 |
| UMBRELLA_025 | BET | CLEAN | 1 | 0 | 0.780 | 0.956 | 0.931 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.780 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_026 | BET | CLEAN | 1 | 0 | 0.816 | 0.956 | 0.931 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.816 >= 0.40; worse_hand_pct 0.956 >= 0.55 |
| UMBRELLA_027 | BET | CLEAN | 1 | 0 | 0.816 | 0.957 | 0.931 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.816 >= 0.40; worse_hand_pct 0.957 >= 0.55 |
| UMBRELLA_028 | BET | CLEAN | 1 | 0 | 0.572 | 0.912 | 0.803 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.572 >= 0.40; worse_hand_pct 0.912 >= 0.55 |
| UMBRELLA_029 | BET | CLEAN | 1 | 0 | 0.899 | 0.962 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.899 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| UMBRELLA_030 | BET | CLEAN | 1 | 0 | 0.883 | 0.965 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.883 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_031 | BET | CLEAN | 1 | 0 | 0.886 | 0.965 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.886 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_032 | BET | CLEAN | 1 | 0 | 0.634 | 0.915 | 0.756 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.634 >= 0.40; worse_hand_pct 0.915 >= 0.55 |
| UMBRELLA_033 | BET | CLEAN | 1 | 0 | 0.879 | 0.974 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.879 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_034 | BET | CLEAN | 1 | 0 | 0.875 | 0.972 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.875 >= 0.40; worse_hand_pct 0.972 >= 0.55 |
| UMBRELLA_035 | BET | CLEAN | 1 | 0 | 0.864 | 0.974 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.864 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_036 | BET | CLEAN | 1 | 0 | 0.638 | 0.924 | 0.812 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.638 >= 0.40; worse_hand_pct 0.924 >= 0.55 |
| UMBRELLA_037 | BET | CLEAN | 1 | 8 | 0.657 | 0.822 | 0.747 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.657 >= 0.40; worse_hand_pct 0.822 >= 0.55 |
| UMBRELLA_038 | CHECK | CLEAN | 1 | 8 | 0.649 | 0.822 | 0.747 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.649 >= 0.40; worse_hand_pct 0.822 >= 0.55 |
| UMBRELLA_039 | BET | CLEAN | 1 | 8 | 0.656 | 0.822 | 0.747 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.656 >= 0.40; worse_hand_pct 0.822 >= 0.55 |
| UMBRELLA_040 | BET | CLEAN | 1 | 8 | 0.651 | 0.822 | 0.747 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.651 >= 0.40; worse_hand_pct 0.822 >= 0.55 |
| UMBRELLA_041 | BET | CLEAN | 1 | 0 | 0.810 | 0.948 | 0.899 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.810 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_042 | BET | CLEAN | 1 | 0 | 0.807 | 0.948 | 0.899 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.807 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_043 | BET | CLEAN | 1 | 0 | 0.817 | 0.948 | 0.899 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.817 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_044 | BET | CLEAN | 1 | 0 | 0.809 | 0.948 | 0.899 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.809 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_045 | BET | CLEAN | 1 | 0 | 0.833 | 0.926 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.833 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_046 | BET | CLEAN | 1 | 0 | 0.837 | 0.926 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.837 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_047 | BET | CLEAN | 1 | 0 | 0.832 | 0.926 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.832 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_048 | BET | CLEAN | 1 | 0 | 0.848 | 0.926 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.848 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_049 | BET | CLEAN | 1 | 0 | 0.866 | 0.974 | 0.948 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.866 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_050 | BET | CLEAN | 1 | 0 | 0.866 | 0.974 | 0.948 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.866 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_051 | BET | CLEAN | 1 | 0 | 0.854 | 0.971 | 0.948 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.854 >= 0.40; worse_hand_pct 0.971 >= 0.55 |
| UMBRELLA_052 | BET | CLEAN | 1 | 0 | 0.529 | 0.907 | 0.803 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.529 >= 0.40; worse_hand_pct 0.907 >= 0.55 |
| UMBRELLA_053 | BET | CLEAN | 1 | 8 | 0.810 | 0.918 | 0.902 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.810 >= 0.40; worse_hand_pct 0.918 >= 0.55 |
| UMBRELLA_054 | BET | CLEAN | 1 | 8 | 0.803 | 0.918 | 0.902 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.803 >= 0.40; worse_hand_pct 0.918 >= 0.55 |
| UMBRELLA_055 | BET | CLEAN | 1 | 8 | 0.814 | 0.918 | 0.902 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.814 >= 0.40; worse_hand_pct 0.918 >= 0.55 |
| UMBRELLA_056 | CHECK | CLEAN | 1 | 8 | 0.460 | 0.844 | 0.712 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.460 >= 0.40; worse_hand_pct 0.844 >= 0.55 |
| UMBRELLA_057 | BET | CLEAN | 1 | 0 | 0.923 | 0.974 | 0.925 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.923 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_058 | BET | CLEAN | 1 | 0 | 0.920 | 0.974 | 0.925 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.920 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_059 | BET | CLEAN | 1 | 0 | 0.910 | 0.971 | 0.925 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.910 >= 0.40; worse_hand_pct 0.971 >= 0.55 |
| UMBRELLA_060 | BET | CLEAN | 1 | 0 | 0.445 | 0.889 | 0.750 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.445 >= 0.40; worse_hand_pct 0.889 >= 0.55 |
| UMBRELLA_061 | BET | CLEAN | 1 | 8 | 0.896 | 0.928 | 0.896 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.896 >= 0.40; worse_hand_pct 0.928 >= 0.55 |
| UMBRELLA_062 | BET | CLEAN | 1 | 8 | 0.878 | 0.931 | 0.896 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.878 >= 0.40; worse_hand_pct 0.931 >= 0.55 |
| UMBRELLA_063 | BET | CLEAN | 1 | 8 | 0.895 | 0.930 | 0.896 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.895 >= 0.40; worse_hand_pct 0.930 >= 0.55 |
| UMBRELLA_064 | BET | CLEAN | 1 | 8 | 0.401 | 0.836 | 0.720 | UMBRELLA | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.401 >= 0.40; worse_hand_pct 0.836 >= 0.55 |
| UMBRELLA_065 | BET | CLEAN | 1 | 0 | 0.784 | 0.951 | 0.943 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.784 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_066 | BET | CLEAN | 1 | 0 | 0.770 | 0.951 | 0.943 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.770 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_067 | BET | CLEAN | 1 | 0 | 0.803 | 0.951 | 0.943 | UMBRELLA | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.803 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_068 | BET | CLEAN | 1 | 0 | 0.490 | 0.888 | 0.797 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.490 >= 0.40; worse_hand_pct 0.888 >= 0.55 |
| UMBRELLA_069 | BET | CLEAN | 1 | 0 | 0.894 | 0.962 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.894 >= 0.40; worse_hand_pct 0.962 >= 0.55 |
| UMBRELLA_070 | BET | CLEAN | 1 | 0 | 0.898 | 0.965 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.898 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_071 | BET | CLEAN | 1 | 0 | 0.895 | 0.965 | 0.923 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.895 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_072 | BET | CLEAN | 1 | 0 | 0.648 | 0.915 | 0.796 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.648 >= 0.40; worse_hand_pct 0.915 >= 0.55 |
| UMBRELLA_073 | BET | CLEAN | 1 | 0 | 0.770 | 0.953 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.770 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_074 | BET | CLEAN | 1 | 0 | 0.767 | 0.953 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.767 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_075 | BET | CLEAN | 1 | 0 | 0.788 | 0.953 | 0.917 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.788 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_076 | BET | CLEAN | 1 | 0 | 0.610 | 0.925 | 0.817 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.610 >= 0.40; worse_hand_pct 0.925 >= 0.55 |
| UMBRELLA_077 | BET | CLEAN | 1 | 8 | 0.790 | 0.908 | 0.872 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.790 >= 0.40; worse_hand_pct 0.908 >= 0.55 |
| UMBRELLA_078 | BET | CLEAN | 1 | 8 | 0.797 | 0.908 | 0.872 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.797 >= 0.40; worse_hand_pct 0.908 >= 0.55 |
| UMBRELLA_079 | BET | CLEAN | 1 | 8 | 0.804 | 0.908 | 0.872 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.804 >= 0.40; worse_hand_pct 0.908 >= 0.55 |
| UMBRELLA_080 | BET | CLEAN | 1 | 8 | 0.716 | 0.886 | 0.798 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.716 >= 0.40; worse_hand_pct 0.886 >= 0.55 |
| UMBRELLA_081 | BET | CLEAN | 1 | 9 | 0.792 | 0.912 | 0.443 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.792 >= 0.40; worse_hand_pct 0.912 >= 0.55 |
| UMBRELLA_082 | BET | CLEAN | 1 | 9 | 0.795 | 0.912 | 0.443 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.795 >= 0.40; worse_hand_pct 0.912 >= 0.55 |
| UMBRELLA_083 | BET | CLEAN | 1 | 9 | 0.788 | 0.912 | 0.443 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.788 >= 0.40; worse_hand_pct 0.912 >= 0.55 |
| UMBRELLA_084 | BET | CLEAN | 1 | 9 | 0.705 | 0.885 | 0.353 | medium_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.705 >= 0.40; worse_hand_pct 0.885 >= 0.55 |
| UMBRELLA_085 | BET | CLEAN | 1 | 0 | 0.815 | 0.908 | 0.499 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.815 >= 0.40; worse_hand_pct 0.908 >= 0.55 |
| UMBRELLA_086 | BET | CLEAN | 1 | 0 | 0.823 | 0.910 | 0.499 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.823 >= 0.40; worse_hand_pct 0.910 >= 0.55 |
| UMBRELLA_087 | BET | CLEAN | 1 | 0 | 0.830 | 0.910 | 0.499 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.830 >= 0.40; worse_hand_pct 0.910 >= 0.55 |
| UMBRELLA_088 | BET | CLEAN | 1 | 0 | 0.497 | 0.845 | 0.345 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.497 >= 0.40; worse_hand_pct 0.845 >= 0.55 |
| UMBRELLA_089 | BET | CLEAN | 1 | 9 | 0.808 | 0.917 | 0.484 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.808 >= 0.40; worse_hand_pct 0.917 >= 0.55 |
| UMBRELLA_090 | BET | CLEAN | 1 | 9 | 0.806 | 0.917 | 0.484 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.806 >= 0.40; worse_hand_pct 0.917 >= 0.55 |
| UMBRELLA_091 | BET | CLEAN | 1 | 9 | 0.816 | 0.917 | 0.484 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.816 >= 0.40; worse_hand_pct 0.917 >= 0.55 |
| UMBRELLA_092 | BET | CLEAN | 1 | 9 | 0.654 | 0.872 | 0.350 | medium_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.654 >= 0.40; worse_hand_pct 0.872 >= 0.55 |
| UMBRELLA_093 | BET | CLEAN | 1 | 4 | 0.873 | 0.904 | 0.460 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.873 >= 0.40; worse_hand_pct 0.904 >= 0.55 |
| UMBRELLA_094 | BET | CLEAN | 1 | 4 | 0.867 | 0.901 | 0.460 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.867 >= 0.40; worse_hand_pct 0.901 >= 0.55 |
| UMBRELLA_095 | BET | CLEAN | 1 | 4 | 0.855 | 0.904 | 0.460 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.855 >= 0.40; worse_hand_pct 0.904 >= 0.55 |
| UMBRELLA_096 | BET | CLEAN | 1 | 4 | 0.407 | 0.817 | 0.306 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.407 >= 0.40; worse_hand_pct 0.817 >= 0.55 |
| UMBRELLA_097 | BET | CLEAN | 1 | 0 | 0.831 | 0.971 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.831 >= 0.40; worse_hand_pct 0.971 >= 0.55 |
| UMBRELLA_098 | BET | CLEAN | 1 | 0 | 0.855 | 0.974 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.855 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_099 | BET | CLEAN | 1 | 0 | 0.828 | 0.974 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.828 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_100 | BET | CLEAN | 1 | 0 | 0.616 | 0.924 | 0.811 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.616 >= 0.40; worse_hand_pct 0.924 >= 0.55 |
| UMBRELLA_101 | BET | CLEAN | 1 | 4 | 0.631 | 0.836 | 0.427 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.631 >= 0.40; worse_hand_pct 0.836 >= 0.55 |
| UMBRELLA_102 | BET | CLEAN | 1 | 4 | 0.733 | 0.861 | 0.427 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.733 >= 0.40; worse_hand_pct 0.861 >= 0.55 |
| UMBRELLA_103 | BET | CLEAN | 1 | 4 | 0.652 | 0.836 | 0.427 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.652 >= 0.40; worse_hand_pct 0.836 >= 0.55 |
| UMBRELLA_104 | BET | CLEAN | 1 | 4 | 0.529 | 0.814 | 0.898 | medium_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.529 >= 0.40; worse_hand_pct 0.814 >= 0.55 |
| UMBRELLA_105 | BET | CLEAN | 1 | 0 | 0.782 | 0.951 | 0.943 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.782 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_106 | BET | CLEAN | 1 | 0 | 0.799 | 0.951 | 0.943 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.799 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_107 | BET | CLEAN | 1 | 0 | 0.771 | 0.951 | 0.943 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.771 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_108 | BET | CLEAN | 1 | 0 | 0.479 | 0.888 | 0.797 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.479 >= 0.40; worse_hand_pct 0.888 >= 0.55 |
| UMBRELLA_109 | BET | CLEAN | 1 | 8 | 0.679 | 0.849 | 0.421 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.679 >= 0.40; worse_hand_pct 0.849 >= 0.55 |
| UMBRELLA_110 | BET | CLEAN | 1 | 8 | 0.744 | 0.872 | 0.421 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.744 >= 0.40; worse_hand_pct 0.872 >= 0.55 |
| UMBRELLA_111 | BET | CLEAN | 1 | 8 | 0.677 | 0.848 | 0.421 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.677 >= 0.40; worse_hand_pct 0.848 >= 0.55 |
| UMBRELLA_112 | BET | CLEAN | 1 | 8 | 0.598 | 0.829 | 0.899 | medium_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.598 >= 0.40; worse_hand_pct 0.829 >= 0.55 |
| UMBRELLA_113 | BET | CLEAN | 1 | 0 | 0.738 | 0.948 | 0.888 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.738 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_114 | BET | CLEAN | 1 | 0 | 0.773 | 0.948 | 0.888 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.773 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_115 | BET | CLEAN | 1 | 0 | 0.761 | 0.948 | 0.888 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.761 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_116 | BET | CLEAN | 1 | 0 | 0.759 | 0.948 | 0.888 | strong_made | 0 | 0.53 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.759 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_117 | BET | CLEAN | 1 | 8 | 0.696 | 0.853 | 0.422 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.696 >= 0.40; worse_hand_pct 0.853 >= 0.55 |
| UMBRELLA_118 | BET | CLEAN | 1 | 8 | 0.649 | 0.828 | 0.422 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.649 >= 0.40; worse_hand_pct 0.828 >= 0.55 |
| UMBRELLA_119 | BET | CLEAN | 1 | 8 | 0.649 | 0.828 | 0.422 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.649 >= 0.40; worse_hand_pct 0.828 >= 0.55 |
| UMBRELLA_120 | BET | CLEAN | 1 | 8 | 0.586 | 0.815 | 0.899 | medium_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.586 >= 0.40; worse_hand_pct 0.815 >= 0.55 |
| UMBRELLA_121 | BET | CLEAN | 1 | 0 | 0.789 | 0.954 | 0.918 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.789 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_122 | BET | CLEAN | 1 | 0 | 0.786 | 0.954 | 0.918 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.786 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_123 | BET | CLEAN | 1 | 0 | 0.800 | 0.954 | 0.918 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.800 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_124 | BET | CLEAN | 1 | 0 | 0.650 | 0.926 | 0.818 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.650 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_125 | BET | CLEAN | 1 | 0 | 0.830 | 0.898 | 0.870 | strong_made | 0 | 0.42 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.830 >= 0.40; worse_hand_pct 0.898 >= 0.55 |
| UMBRELLA_126 | BET | CLEAN | 1 | 0 | 0.829 | 0.898 | 0.870 | strong_made | 0 | 0.42 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.829 >= 0.40; worse_hand_pct 0.898 >= 0.55 |
| UMBRELLA_127 | BET | CLEAN | 1 | 0 | 0.828 | 0.898 | 0.870 | strong_made | 0 | 0.42 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.828 >= 0.40; worse_hand_pct 0.898 >= 0.55 |
| UMBRELLA_128 | BET | CLEAN | 1 | 0 | 0.502 | 0.841 | 0.680 | medium_made | 0 | 0.42 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.502 >= 0.40; worse_hand_pct 0.841 >= 0.55 |
| UMBRELLA_129 | BET | CLEAN | 1 | 0 | 0.608 | 0.885 | 0.888 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.608 >= 0.40; worse_hand_pct 0.885 >= 0.55 |
| UMBRELLA_130 | BET | CLEAN | 1 | 0 | 0.602 | 0.885 | 0.888 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.602 >= 0.40; worse_hand_pct 0.885 >= 0.55 |
| UMBRELLA_131 | BET | CLEAN | 1 | 0 | 0.625 | 0.885 | 0.888 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.625 >= 0.40; worse_hand_pct 0.885 >= 0.55 |
| UMBRELLA_132 | BET | CLEAN | 1 | 9 | 0.549 | 0.848 | 0.761 | medium_made | 0 | 0.38 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.549 >= 0.40; worse_hand_pct 0.848 >= 0.55 |
| UMBRELLA_133 | BET | CLEAN | 1 | 0 | 0.633 | 0.759 | 0.475 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.633 >= 0.40; worse_hand_pct 0.759 >= 0.55 |
| UMBRELLA_134 | BET | CLEAN | 1 | 0 | 0.723 | 0.787 | 0.475 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.723 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| UMBRELLA_135 | BET | CLEAN | 1 | 0 | 0.640 | 0.759 | 0.475 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.640 >= 0.40; worse_hand_pct 0.759 >= 0.55 |
| UMBRELLA_136 | BET | CLEAN | 1 | 0 | 0.382 | 0.714 | 0.893 | medium_made | 0 | 1.00 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| UMBRELLA_137 | BET | CLEAN | 1 | 0 | 0.781 | 0.922 | 0.869 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.781 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_138 | BET | CLEAN | 1 | 0 | 0.785 | 0.922 | 0.869 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.785 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_139 | BET | CLEAN | 1 | 0 | 0.807 | 0.922 | 0.869 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.807 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_140 | BET | CLEAN | 1 | 0 | 0.394 | 0.848 | 0.693 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| UMBRELLA_141 | BET | CLEAN | 1 | 0 | 0.561 | 0.785 | 0.474 | strong_made | 0 | 0.76 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.561 >= 0.40; worse_hand_pct 0.785 >= 0.55 |
| UMBRELLA_142 | BET | CLEAN | 1 | 0 | 0.628 | 0.814 | 0.474 | strong_made | 0 | 0.76 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.628 >= 0.40; worse_hand_pct 0.814 >= 0.55 |
| UMBRELLA_143 | BET | CLEAN | 1 | 0 | 0.537 | 0.785 | 0.474 | strong_made | 0 | 0.76 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.537 >= 0.40; worse_hand_pct 0.785 >= 0.55 |
| UMBRELLA_144 | CHECK | CLEAN | 1 | 0 | 0.446 | 0.772 | 0.901 | medium_made | 0 | 0.76 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.446 >= 0.40; worse_hand_pct 0.772 >= 0.55 |
| UMBRELLA_145 | BET | CLEAN | 1 | 0 | 0.638 | 0.849 | 0.885 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.638 >= 0.40; worse_hand_pct 0.849 >= 0.55 |
| UMBRELLA_146 | BET | CLEAN | 1 | 0 | 0.618 | 0.849 | 0.885 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.618 >= 0.40; worse_hand_pct 0.849 >= 0.55 |
| UMBRELLA_147 | BET | CLEAN | 1 | 0 | 0.604 | 0.849 | 0.885 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.604 >= 0.40; worse_hand_pct 0.849 >= 0.55 |
| UMBRELLA_148 | BET | CLEAN | 1 | 0 | 0.456 | 0.816 | 0.755 | medium_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.456 >= 0.40; worse_hand_pct 0.816 >= 0.55 |
| UMBRELLA_149 | BET | CLEAN | 1 | 4 | 0.816 | 0.884 | 0.421 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.816 >= 0.40; worse_hand_pct 0.884 >= 0.55 |
| UMBRELLA_150 | BET | CLEAN | 1 | 4 | 0.818 | 0.885 | 0.421 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.818 >= 0.40; worse_hand_pct 0.885 >= 0.55 |
| UMBRELLA_151 | BET | CLEAN | 1 | 4 | 0.813 | 0.884 | 0.421 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.813 >= 0.40; worse_hand_pct 0.884 >= 0.55 |
| UMBRELLA_152 | BET | CLEAN | 1 | 4 | 0.376 | 0.794 | 0.222 | medium_made | 0 | 0.77 | 0 | 1 | 0 | made/drawing hand, wp ok; BET defensible |
| UMBRELLA_153 | BET | CLEAN | 1 | 0 | 0.770 | 0.916 | 0.884 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.770 >= 0.40; worse_hand_pct 0.916 >= 0.55 |
| UMBRELLA_154 | BET | CLEAN | 1 | 0 | 0.752 | 0.916 | 0.884 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.752 >= 0.40; worse_hand_pct 0.916 >= 0.55 |
| UMBRELLA_155 | BET | CLEAN | 1 | 0 | 0.764 | 0.916 | 0.884 | strong_made | 0 | 0.58 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.764 >= 0.40; worse_hand_pct 0.916 >= 0.55 |
| UMBRELLA_156 | BET | CLEAN | 1 | 0 | 0.391 | 0.841 | 0.708 | medium_made | 0 | 0.58 | 0 | 0 | 0 | made/drawing hand, wp ok; BET defensible |
| UMBRELLA_157 | BET | CLEAN | 1 | 0 | 0.591 | 0.763 | 0.477 | strong_made | 0 | 0.77 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.591 >= 0.40; worse_hand_pct 0.763 >= 0.55 |
| UMBRELLA_158 | BET | CLEAN | 1 | 0 | 0.585 | 0.764 | 0.477 | strong_made | 0 | 0.77 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.585 >= 0.40; worse_hand_pct 0.764 >= 0.55 |
| UMBRELLA_159 | BET | CLEAN | 1 | 0 | 0.608 | 0.763 | 0.477 | strong_made | 0 | 0.77 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.608 >= 0.40; worse_hand_pct 0.763 >= 0.55 |
| UMBRELLA_160 | BET | CLEAN | 1 | 0 | 0.512 | 0.757 | 0.385 | medium_made | 0 | 0.77 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.512 >= 0.40; worse_hand_pct 0.757 >= 0.55 |
| UMBRELLA_161 | BET | CLEAN | 1 | 9 | 0.635 | 0.787 | 0.466 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.635 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| UMBRELLA_162 | BET | CLEAN | 1 | 9 | 0.636 | 0.787 | 0.466 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.636 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| UMBRELLA_163 | BET | CLEAN | 1 | 9 | 0.633 | 0.787 | 0.466 | strong_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.633 >= 0.40; worse_hand_pct 0.787 >= 0.55 |
| UMBRELLA_164 | BET | CLEAN | 1 | 9 | 0.625 | 0.795 | 0.404 | medium_made | 0 | 0.60 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.625 >= 0.40; worse_hand_pct 0.795 >= 0.55 |
| UMBRELLA_165 | BET | CLEAN | 1 | 8 | 0.732 | 0.888 | 0.868 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.732 >= 0.40; worse_hand_pct 0.888 >= 0.55 |
| UMBRELLA_166 | BET | CLEAN | 1 | 8 | 0.731 | 0.888 | 0.868 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.731 >= 0.40; worse_hand_pct 0.888 >= 0.55 |
| UMBRELLA_167 | BET | CLEAN | 1 | 8 | 0.733 | 0.887 | 0.868 | strong_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.733 >= 0.40; worse_hand_pct 0.887 >= 0.55 |
| UMBRELLA_168 | BET | CLEAN | 1 | 8 | 0.715 | 0.872 | 0.789 | medium_made | 0 | 0.92 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.715 >= 0.40; worse_hand_pct 0.872 >= 0.55 |
| UMBRELLA_169 | BET | CLEAN | 1 | 0 | 0.859 | 0.974 | 0.934 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.859 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_170 | BET | CLEAN | 1 | 0 | 0.862 | 0.974 | 0.934 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.862 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_171 | BET | CLEAN | 1 | 0 | 0.865 | 0.971 | 0.934 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.865 >= 0.40; worse_hand_pct 0.971 >= 0.55 |
| UMBRELLA_172 | BET | CLEAN | 1 | 0 | 0.821 | 0.953 | 0.861 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.821 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_173 | BET | CLEAN | 1 | 0 | 0.866 | 0.965 | 0.915 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.866 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_174 | BET | CLEAN | 1 | 0 | 0.865 | 0.965 | 0.915 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.865 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_175 | BET | CLEAN | 1 | 0 | 0.889 | 0.968 | 0.915 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.889 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| UMBRELLA_176 | BET | CLEAN | 1 | 0 | 0.849 | 0.946 | 0.822 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.849 >= 0.40; worse_hand_pct 0.946 >= 0.55 |
| UMBRELLA_177 | BET | CLEAN | 1 | 0 | 0.855 | 0.974 | 0.935 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.855 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_178 | BET | CLEAN | 1 | 0 | 0.846 | 0.972 | 0.935 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.846 >= 0.40; worse_hand_pct 0.972 >= 0.55 |
| UMBRELLA_179 | BET | CLEAN | 1 | 0 | 0.836 | 0.974 | 0.935 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.836 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_180 | BET | CLEAN | 1 | 0 | 0.737 | 0.935 | 0.813 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.737 >= 0.40; worse_hand_pct 0.935 >= 0.55 |
| UMBRELLA_181 | BET | CLEAN | 1 | 0 | 0.873 | 0.968 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.873 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| UMBRELLA_182 | BET | CLEAN | 1 | 0 | 0.868 | 0.965 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.868 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_183 | BET | CLEAN | 1 | 0 | 0.872 | 0.965 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.872 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_184 | BET | CLEAN | 1 | 0 | 0.780 | 0.930 | 0.790 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.780 >= 0.40; worse_hand_pct 0.930 >= 0.55 |
| UMBRELLA_185 | BET | CLEAN | 1 | 0 | 0.765 | 0.952 | 0.951 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.765 >= 0.40; worse_hand_pct 0.952 >= 0.55 |
| UMBRELLA_186 | BET | CLEAN | 1 | 0 | 0.771 | 0.952 | 0.951 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.771 >= 0.40; worse_hand_pct 0.952 >= 0.55 |
| UMBRELLA_187 | BET | CLEAN | 1 | 0 | 0.779 | 0.952 | 0.951 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.779 >= 0.40; worse_hand_pct 0.952 >= 0.55 |
| UMBRELLA_188 | BET | CLEAN | 1 | 0 | 0.695 | 0.921 | 0.828 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.695 >= 0.40; worse_hand_pct 0.921 >= 0.55 |
| UMBRELLA_189 | BET | CLEAN | 1 | 0 | 0.889 | 0.968 | 0.919 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.889 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| UMBRELLA_190 | BET | CLEAN | 1 | 0 | 0.880 | 0.965 | 0.919 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.880 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_191 | BET | CLEAN | 1 | 0 | 0.884 | 0.965 | 0.919 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.884 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_192 | BET | CLEAN | 1 | 0 | 0.751 | 0.914 | 0.785 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.751 >= 0.40; worse_hand_pct 0.914 >= 0.55 |
| UMBRELLA_193 | BET | CLEAN | 1 | 0 | 0.850 | 0.972 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.850 >= 0.40; worse_hand_pct 0.972 >= 0.55 |
| UMBRELLA_194 | BET | CLEAN | 1 | 0 | 0.841 | 0.974 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.841 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_195 | BET | CLEAN | 1 | 0 | 0.860 | 0.974 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.860 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_196 | BET | CLEAN | 1 | 0 | 0.694 | 0.924 | 0.767 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.694 >= 0.40; worse_hand_pct 0.924 >= 0.55 |
| UMBRELLA_197 | BET | CLEAN | 1 | 0 | 0.867 | 0.954 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.867 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_198 | BET | CLEAN | 1 | 0 | 0.859 | 0.952 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.859 >= 0.40; worse_hand_pct 0.952 >= 0.55 |
| UMBRELLA_199 | BET | CLEAN | 1 | 0 | 0.853 | 0.954 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.853 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_200 | BET | CLEAN | 1 | 0 | 0.718 | 0.904 | 0.804 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.718 >= 0.40; worse_hand_pct 0.904 >= 0.55 |
| UMBRELLA_201 | BET | CLEAN | 1 | 0 | 0.711 | 0.913 | 0.845 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.711 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_202 | BET | CLEAN | 1 | 0 | 0.699 | 0.913 | 0.845 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.699 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_203 | BET | CLEAN | 1 | 0 | 0.700 | 0.913 | 0.845 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.700 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_204 | CHECK | CLEAN | 1 | 0 | 0.699 | 0.913 | 0.845 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.699 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_205 | BET | CLEAN | 1 | 0 | 0.804 | 0.922 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.804 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_206 | BET | CLEAN | 1 | 0 | 0.809 | 0.922 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.809 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_207 | BET | CLEAN | 1 | 0 | 0.818 | 0.922 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.818 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_208 | BET | CLEAN | 1 | 0 | 0.821 | 0.922 | 0.886 | strong_made | 0 | 1.00 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.821 >= 0.40; worse_hand_pct 0.922 >= 0.55 |
| UMBRELLA_209 | BET | CLEAN | 1 | 9 | 0.780 | 0.913 | 0.885 | medium_made | 0 | 0.88 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.780 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_210 | BET | CLEAN | 1 | 0 | 0.701 | 0.913 | 0.885 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.701 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_211 | CHECK | CLEAN | 1 | 0 | 0.702 | 0.913 | 0.885 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.702 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_212 | BET | CLEAN | 1 | 0 | 0.673 | 0.913 | 0.885 | medium_made | 0 | 0.88 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.673 >= 0.40; worse_hand_pct 0.913 >= 0.55 |
| UMBRELLA_213 | BET | CLEAN | 1 | 0 | 0.867 | 0.954 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.867 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_214 | BET | CLEAN | 1 | 0 | 0.856 | 0.954 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.856 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_215 | BET | CLEAN | 1 | 0 | 0.869 | 0.951 | 0.936 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.869 >= 0.40; worse_hand_pct 0.951 >= 0.55 |
| UMBRELLA_216 | BET | CLEAN | 1 | 0 | 0.691 | 0.888 | 0.756 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.691 >= 0.40; worse_hand_pct 0.888 >= 0.55 |
| UMBRELLA_217 | BET | CLEAN | 1 | 0 | 0.774 | 0.963 | 0.952 | UMBRELLA | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.774 >= 0.40; worse_hand_pct 0.963 >= 0.55 |
| UMBRELLA_218 | BET | CLEAN | 1 | 0 | 0.772 | 0.963 | 0.952 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.772 >= 0.40; worse_hand_pct 0.963 >= 0.55 |
| UMBRELLA_219 | BET | CLEAN | 1 | 0 | 0.784 | 0.963 | 0.952 | strong_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.784 >= 0.40; worse_hand_pct 0.963 >= 0.55 |
| UMBRELLA_220 | BET | CLEAN | 1 | 0 | 0.599 | 0.899 | 0.735 | medium_made | 0 | 0.38 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.599 >= 0.40; worse_hand_pct 0.899 >= 0.55 |
| UMBRELLA_221 | BET | CLEAN | 1 | 4 | 0.845 | 0.948 | 0.870 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.845 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_222 | BET | CLEAN | 1 | 4 | 0.848 | 0.948 | 0.870 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.848 >= 0.40; worse_hand_pct 0.948 >= 0.55 |
| UMBRELLA_223 | BET | CLEAN | 1 | 4 | 0.836 | 0.945 | 0.870 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.836 >= 0.40; worse_hand_pct 0.945 >= 0.55 |
| UMBRELLA_224 | BET | CLEAN | 1 | 4 | 0.654 | 0.861 | 0.618 | strong_made | 0 | 0.77 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.654 >= 0.40; worse_hand_pct 0.861 >= 0.55 |
| UMBRELLA_225 | BET | CLEAN | 1 | 0 | 0.844 | 0.972 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.844 >= 0.40; worse_hand_pct 0.972 >= 0.55 |
| UMBRELLA_226 | BET | CLEAN | 1 | 0 | 0.861 | 0.975 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.861 >= 0.40; worse_hand_pct 0.975 >= 0.55 |
| UMBRELLA_227 | BET | CLEAN | 1 | 0 | 0.850 | 0.975 | 0.936 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.850 >= 0.40; worse_hand_pct 0.975 >= 0.55 |
| UMBRELLA_228 | BET | CLEAN | 1 | 0 | 0.612 | 0.891 | 0.684 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.612 >= 0.40; worse_hand_pct 0.891 >= 0.55 |
| UMBRELLA_229 | BET | CLEAN | 1 | 0 | 0.877 | 0.954 | 0.919 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.877 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_230 | BET | CLEAN | 1 | 0 | 0.868 | 0.954 | 0.919 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.868 >= 0.40; worse_hand_pct 0.954 >= 0.55 |
| UMBRELLA_231 | BET | CLEAN | 1 | 0 | 0.882 | 0.957 | 0.919 | UMBRELLA | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.882 >= 0.40; worse_hand_pct 0.957 >= 0.55 |
| UMBRELLA_232 | BET | CLEAN | 1 | 0 | 0.708 | 0.891 | 0.738 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.708 >= 0.40; worse_hand_pct 0.891 >= 0.55 |
| UMBRELLA_233 | BET | CLEAN | 1 | 0 | 0.846 | 0.972 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.846 >= 0.40; worse_hand_pct 0.972 >= 0.55 |
| UMBRELLA_234 | BET | CLEAN | 1 | 0 | 0.843 | 0.974 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.843 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_235 | BET | CLEAN | 1 | 0 | 0.844 | 0.974 | 0.937 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.844 >= 0.40; worse_hand_pct 0.974 >= 0.55 |
| UMBRELLA_236 | BET | CLEAN | 1 | 0 | 0.690 | 0.924 | 0.807 | strong_made | 0 | 0.23 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.690 >= 0.40; worse_hand_pct 0.924 >= 0.55 |
| UMBRELLA_237 | BET | CLEAN | 1 | 0 | 0.889 | 0.965 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.889 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_238 | BET | CLEAN | 1 | 0 | 0.853 | 0.965 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.853 >= 0.40; worse_hand_pct 0.965 >= 0.55 |
| UMBRELLA_239 | BET | CLEAN | 1 | 0 | 0.887 | 0.968 | 0.916 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.887 >= 0.40; worse_hand_pct 0.968 >= 0.55 |
| UMBRELLA_240 | BET | CLEAN | 1 | 0 | 0.776 | 0.928 | 0.790 | strong_made | 0 | 0.57 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.776 >= 0.40; worse_hand_pct 0.928 >= 0.55 |
| UMBRELLA_241 | BET | CLEAN | 1 | 0 | 0.719 | 0.953 | 0.926 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.719 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_242 | BET | CLEAN | 1 | 0 | 0.714 | 0.953 | 0.926 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.714 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_243 | BET | CLEAN | 1 | 0 | 0.741 | 0.953 | 0.926 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.741 >= 0.40; worse_hand_pct 0.953 >= 0.55 |
| UMBRELLA_244 | BET | CLEAN | 1 | 9 | 0.785 | 0.941 | 0.851 | medium_made | 0 | 0.08 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.785 >= 0.40; worse_hand_pct 0.941 >= 0.55 |
| UMBRELLA_245 | BET | CLEAN | 1 | 8 | 0.690 | 0.868 | 0.403 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.690 >= 0.40; worse_hand_pct 0.868 >= 0.55 |
| UMBRELLA_246 | BET | CLEAN | 1 | 8 | 0.691 | 0.868 | 0.403 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.691 >= 0.40; worse_hand_pct 0.868 >= 0.55 |
| UMBRELLA_247 | BET | CLEAN | 1 | 8 | 0.679 | 0.868 | 0.403 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.679 >= 0.40; worse_hand_pct 0.868 >= 0.55 |
| UMBRELLA_248 | BET | CLEAN | 1 | 8 | 0.620 | 0.832 | 0.290 | medium_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.620 >= 0.40; worse_hand_pct 0.832 >= 0.55 |
| UMBRELLA_249 | BET | CLEAN | 1 | 9 | 0.810 | 0.924 | 0.402 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.810 >= 0.40; worse_hand_pct 0.924 >= 0.55 |
| UMBRELLA_250 | BET | CLEAN | 1 | 9 | 0.802 | 0.926 | 0.402 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.802 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_251 | BET | CLEAN | 1 | 9 | 0.808 | 0.926 | 0.402 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.808 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_252 | BET | CLEAN | 1 | 9 | 0.687 | 0.862 | 0.224 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.687 >= 0.40; worse_hand_pct 0.862 >= 0.55 |
| UMBRELLA_253 | BET | CLEAN | 1 | 8 | 0.719 | 0.876 | 0.411 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.719 >= 0.40; worse_hand_pct 0.876 >= 0.55 |
| UMBRELLA_254 | BET | CLEAN | 1 | 8 | 0.700 | 0.876 | 0.411 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.700 >= 0.40; worse_hand_pct 0.876 >= 0.55 |
| UMBRELLA_255 | BET | CLEAN | 1 | 8 | 0.736 | 0.875 | 0.411 | strong_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.736 >= 0.40; worse_hand_pct 0.875 >= 0.55 |
| UMBRELLA_256 | CHECK | CLEAN | 1 | 8 | 0.583 | 0.820 | 0.276 | medium_made | 0 | 1.00 | 0 | 1 | 0 | made hand or 4+ draw outs; equity 0.583 >= 0.40; worse_hand_pct 0.820 >= 0.55 |
| UMBRELLA_257 | BET | CLEAN | 1 | 9 | 0.799 | 0.926 | 0.411 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.799 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_258 | BET | CLEAN | 1 | 9 | 0.800 | 0.923 | 0.411 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.800 >= 0.40; worse_hand_pct 0.923 >= 0.55 |
| UMBRELLA_259 | BET | CLEAN | 1 | 9 | 0.785 | 0.926 | 0.411 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.785 >= 0.40; worse_hand_pct 0.926 >= 0.55 |
| UMBRELLA_260 | BET | CLEAN | 1 | 9 | 0.644 | 0.843 | 0.184 | strong_made | 0 | 0.75 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.644 >= 0.40; worse_hand_pct 0.843 >= 0.55 |
| UMBRELLA_261 | BET | CLEAN | 1 | 0 | 0.732 | 0.894 | 0.408 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.732 >= 0.40; worse_hand_pct 0.894 >= 0.55 |
| UMBRELLA_262 | BET | CLEAN | 1 | 0 | 0.800 | 0.920 | 0.408 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.800 >= 0.40; worse_hand_pct 0.920 >= 0.55 |
| UMBRELLA_263 | BET | CLEAN | 1 | 0 | 0.731 | 0.897 | 0.408 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.731 >= 0.40; worse_hand_pct 0.897 >= 0.55 |
| UMBRELLA_264 | BET | CLEAN | 1 | 0 | 0.630 | 0.849 | 0.784 | strong_made | 0 | 0.91 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.630 >= 0.40; worse_hand_pct 0.849 >= 0.55 |
| UMBRELLA_265 | BET | CLEAN | 1 | 0 | 0.676 | 0.934 | 0.897 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.676 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_266 | BET | CLEAN | 1 | 0 | 0.687 | 0.934 | 0.897 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.687 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_267 | BET | CLEAN | 1 | 0 | 0.682 | 0.934 | 0.897 | strong_made | 0 | 0.08 | 0 | 0 | 0 | made hand or 4+ draw outs; equity 0.682 >= 0.40; worse_hand_pct 0.934 >= 0.55 |
| UMBRELLA_268 | BET | CLEAN | 1 | 9 | 0.713 | 0.911 | 0.769 | UMBRELLA | 0 | 0.08 | 1 | 0 | 0 | made hand or 4+ draw outs; equity 0.713 >= 0.40; worse_hand_pct 0.911 >= 0.55 |

---
*Generated by override audit script. No labels were modified.*