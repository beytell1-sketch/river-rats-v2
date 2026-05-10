# Phase 1.5-D.3 Pilot — HU Corpus Labeller Brief (50 lookalike spots)

You are a fresh GTO labelling agent for Phase 1.5-D.3 PILOT — labelling 50 HU lookalike situations generated from the HU-1 reference axis.

## Your task in 3 phases

### Phase 1: Read protocol + KB

1. `Read prompts/gto_labeller_v3.4.md` — labelling protocol; apply verbatim including DO NOT Rule 11 + KB §1.7 OVERRIDE.
2. `Read knowledge/three_way_gto.md` — KB.

### Phase 2: BLIND calibration exam (28 hands; same as 1.5-D.2)

You take the 28-hand calibration exam BLIND. **You MUST NOT** read `river-rats-core/calibration_exam.py` or any answer key file.

Calibration sources:
- `Read design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — 24 multiway hands (filter to num_opponents=2)
- 4 hard anchors from `training-data/test_set_50_labelled.jsonl` + `training-data/3way_combined_350.jsonl`:
  - `d8886_BB_flop`, `d2410_CO_turn`, `d8963_HJ_turn`, `d3178_CO_river`
  - Extract only spot fields + feat_dict; do NOT read expert_action / expert_reasoning / oracle_action / etc.

Output format per calibration hand to `calibration_results_labeller_<N>.jsonl` (28 lines):

```json
{"ref_id": "MW-11", "predicted_action": "CHECK", "confidence": "HIGH", "reasoning": "<2-4 sentences>"}
```

### Phase 3: HU pilot labelling (50 lookalikes)

Read `data/hu_corpus/pilot_50/situations.jsonl` — each line is a JSON object with `spot_id`, `anchor_id`, `hero_cards`, `board_flop`, `street`, `hero_pos`, `villain_pos`, `pot_bb`, `facing_bet`, `to_call_bb`, `effective_stack_bb`, `opener`, `bettor`, `composition`, `axis`, `action_summary`, `variation_axis`, `variation_param`.

For each of the 50 spots:
1. Reconstruct the situation from the fields (the `action_summary` describes the action history; `variation_axis` + `variation_param` describe how this spot differs from its anchor).
2. All 50 spots have `num_opponents: 1` (HU). Apply v3.4 line 729 HU carve-out (bet for value/protection per v3.1 rules).
3. Apply the v3.4 protocol verbatim.

Output per spot to `raw_labels_labeller_<N>.jsonl` (50 lines):

```json
{"spot_id": "HU-1.1-LK-01", "predicted_action": "BET", "confidence": "HIGH", "reasoning": "<2-4 sentences>", "predicted_sizing_pct": 25}
```

Use `spot_id` (not `ref_id`) as the identifier for the pilot 50 (the anchor `ref_id` would collide across multiple variations of the same anchor). Include `predicted_sizing_pct` only if action is BET or RAISE; sizes per `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150).

## Methodology rules (binding)

- **Fresh agent, no shared state**: do not look at other labellers' outputs; do not read pilot_HU1 or full_HU2_HU6 results.
- **Bucket-first**: NO equity thresholds in reasoning; use composition + protocol rules.
- **Solver-vs-labels**: don't cite solver as label rationale.
- **Terminology**: raise = raise of existing bet; bet = first postflop bet; open = preflop opener.
- **HU-only**: every spot has num_opponents=1; v3.4 line 729 HU carve-out applies; Rule 11 multiway predicates do NOT trigger.
- **Lookalike interpretation**: each spot is a variation of an HU-1 anchor. Use `variation_axis` to understand what changed, but reach your own protocol-driven conclusion — the anchor's GTO action does NOT auto-apply to the variation.

## When you're done

Confirm:
1. Both files written + line counts (28 calibration + 50 pilot = 78 hands)
2. Calibration self-check: HIGH-confidence count out of 28
3. Pilot summary: count of each action across 50 spots (e.g., "BET: 28, CHECK: 12, CALL: 8, FOLD: 1, RAISE: 1")
