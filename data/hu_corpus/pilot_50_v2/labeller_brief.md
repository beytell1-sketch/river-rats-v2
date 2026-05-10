# Phase 1.5-D.3 Pilot v2 — HU Corpus Labeller Brief (50 lookalike spots; board-mutating fix)

You are a fresh GTO labelling agent for Phase 1.5-D.3 PILOT V2 — labelling 50 HU lookalike situations regenerated from the HU-1 reference axis after the v1 generator board-mutation bug fix.

**Why v2**: The prior pilot's generator described board-runout mutations in `variation_param` prose but did not actually mutate `board_flop` / `board_turn` / `board_river` fields, producing 25 anchor-identical "lookalikes". v2 fixes this — board_runout variations now have actually-different boards. Calibration protocol is unchanged.

## Your task in 3 phases

### Phase 1: Read protocol + KB

1. `Read prompts/gto_labeller_v3.4.md` — labelling protocol; apply verbatim including DO NOT Rule 11 + KB §1.7 OVERRIDE.
2. `Read knowledge/three_way_gto.md` — KB.

### Phase 2: BLIND calibration exam (28 hands; same set as v1 / 1.5-D.2)

You take the 28-hand calibration exam BLIND. **You MUST NOT** read `river-rats-core/calibration_exam.py` or any answer key file.

Calibration sources:
- `Read design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — 24 multiway hands (filter to num_opponents=2)
- 4 hard anchors from `training-data/test_set_50_labelled.jsonl` + `training-data/3way_combined_350.jsonl`:
  - `d8886_BB_flop`, `d2410_CO_turn`, `d8963_HJ_turn`, `d3178_CO_river`
  - Extract only spot fields + feat_dict; do NOT read expert_action / expert_reasoning / oracle_action / etc.

Output format per calibration hand to `data/hu_corpus/pilot_50_v2/calibration_results_labeller_<N>.jsonl` (28 lines):

```json
{"ref_id": "MW-11", "predicted_action": "CHECK", "confidence": "HIGH", "reasoning": "<2-4 sentences>"}
```

Pass thresholds: ≥20/28 correct AND 100% on GTO_REVERSAL_HANDS (MW-30, MW-33, MW-50).

### Phase 3: HU pilot v2 labelling (50 lookalikes)

Read `data/hu_corpus/pilot_50_v2/situations.jsonl` — each line is a JSON object with `spot_id`, `anchor_id`, `hero_cards`, `board_flop`, `street`, `hero_pos`, `villain_pos`, `pot_bb`, `facing_bet`, `to_call_bb`, `effective_stack_bb`, `opener`, `bettor`, `composition`, `axis`, `action_summary`, `variation_axis`, `variation_param`, `lookalike_brick`.

**Important v2 change**: For `variation_axis = "board_runout"` rows, the `board_flop` / `board_turn` / `board_river` fields differ from the anchor (a brick has been replaced). The `action_summary` still describes the anchor's action history — interpret as: "same betting line as anchor, but the board card noted in `variation_param` was replaced". Reach your own protocol-driven conclusion based on the actual board fields, not the anchor's GTO action.

For each of the 50 spots:
1. Reconstruct the situation from the fields.
2. All 50 spots have `num_opponents: 1` (HU). Apply v3.4 line 729 HU carve-out (bet for value/protection per v3.1 rules).
3. Apply the v3.4 protocol verbatim.

Output per spot to `data/hu_corpus/pilot_50_v2/raw_labels_labeller_<N>.jsonl` (50 lines):

```json
{"spot_id": "HU-1.1-LK-01", "predicted_action": "BET", "confidence": "HIGH", "reasoning": "<2-4 sentences>", "predicted_sizing_pct": 25}
```

Use `spot_id` as the identifier. Include `predicted_sizing_pct` only if action is BET or RAISE; sizes per `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150).

## Methodology rules (binding)

- **Fresh agent, no shared state**: do not look at other labellers' outputs; do not read pilot_HU1, full_HU2_HU6, or pilot_50 (v1) results.
- **Bucket-first**: NO equity thresholds in reasoning; use composition + protocol rules.
- **Solver-vs-labels**: don't cite solver as label rationale.
- **Terminology**: raise = raise of existing bet; bet = first postflop bet; open = preflop opener.
- **HU-only**: every spot has num_opponents=1; v3.4 line 729 HU carve-out applies; Rule 11 multiway predicates do NOT trigger.
- **Lookalike interpretation**: each spot is a variation of an HU-1 anchor. Use `variation_axis`/`variation_param`/board fields to understand what changed. Anchor's GTO action does NOT auto-apply.

## When you're done

Confirm:
1. Both files written + line counts (28 calibration + 50 pilot = 78 hands)
2. Calibration self-check: HIGH-confidence count out of 28
3. Pilot summary: count of each action across 50 spots (e.g., "BET: 28, CHECK: 12, CALL: 8, FOLD: 1, RAISE: 1")
