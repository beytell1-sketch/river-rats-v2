# Phase 1.5-D.2 Pilot — HU Reference Set Labeller Brief

You are a fresh GTO labelling agent for Phase 1.5-D.2 pilot of the River Rats v2 project. You have NO shared state with other labellers.

## Your task in 3 phases

### Phase 1: Read protocol + KB (do this first; do not skip)

1. `Read prompts/gto_labeller_v3.4.md` — labelling protocol you MUST follow verbatim. Apply ALL DO NOT Rules including Rule 11 (paired-board / 2-tone OOP exception) and the v3.2 KB §1.7 OVERRIDE.
2. `Read knowledge/three_way_gto.md` — knowledge base referenced by the protocol.

### Phase 2: BLIND calibration exam (28 hands)

You take the 28-hand calibration exam BLIND. **You MUST NOT** read `river-rats-core/calibration_exam.py` or any answer key before completing your labels. Reading the answer key disqualifies you.

Calibration hand sources:
- `Read design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — 24 multiway reference hands (MW-11 through MW-50, num_opponents=2 only). Action histories, hero hands, boards, positions all there.
- 4 additional hard-anchor calibration hands (load via the labelled JSONL referenced by `_load_labelled_record` in `calibration_exam.py:138-180` — but DO NOT read calibration_exam.py for the answers; only use it as an index of which `ref_id` strings to look up in `training-data/3way_combined_350.jsonl` or `training-data/test_set_50_labelled.jsonl`):
  - `d8886_BB_flop`
  - `d2410_CO_turn`
  - `d8963_HJ_turn`
  - `d3178_CO_river`

For each calibration hand, compute the FULL feat_dict (call `extract_all_features` from `river-rats-core/feature_extractor.py` if you need feature values you can't see directly; or read the labelled JSONL where feat_dicts are pre-computed for the 4 hard anchors). Apply the v3.4 protocol. Output your action label per hand.

Output format per calibration hand (one JSON object per line; write to your assigned `calibration_results_labeller_<N>.jsonl`):

```json
{"ref_id": "MW-11", "predicted_action": "CHECK", "confidence": "HIGH", "reasoning": "<2-4 sentences citing protocol rules + features>"}
```

`predicted_action` ∈ {`FOLD`, `CHECK`, `CALL`, `BET`, `RAISE`}. `confidence` ∈ {`HIGH`, `MEDIUM`, `LOW`}.

### Phase 3: HU-1 pilot labelling (5 hands)

After calibration, label the 5 HU-1 pilot hands from `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`:
- HU-1.1 (CANONICAL): AhKs TPTK BTN c-bet on dry A83r vs BB
- HU-1.2 (CANONICAL): 9d9c flopped set, river thin value on safe runout BTN vs BB
- HU-1.3 (CLOSE): KhQd TPGK on wet KcTc6d flop, BTN vs BB
- HU-1.4 (CLOSE): TsTd flopped set, turn vs IP probe, SB vs BB
- HU-1.5 (CLOSE): AhJh TPGK with blocker, river bluff-catch vs scary completed runout, BB vs BTN

For each HU-1 hand: read the full hand spec from `HU_AXIS_1_MADE_HAND.md` (which includes hero cards, board, street, positions, num_opponents, action history). Apply the v3.4 protocol with explicit attention to its HU carve-outs (e.g., line 729: "Heads-up spots (`num_opponents = 1`) — bet for value/protection per existing v3.1 rules").

All 5 HU-1 hands have `num_opponents: 1` (explicit HU). Apply HU-appropriate reasoning per protocol.

Output format per pilot hand (one JSON object per line; write to your assigned `raw_labels_labeller_<N>.jsonl`):

```json
{"ref_id": "HU-1.1", "predicted_action": "BET", "confidence": "HIGH", "reasoning": "<2-4 sentences citing protocol rules + composition + position + sizing>", "predicted_sizing_pct": 66}
```

Include `predicted_sizing_pct` ONLY if your action is BET or RAISE. Use solver-aligned sizes per `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150).

## Output files (write to disk; you'll be told your N)

- `data/hu_labelling/pilot_HU1/calibration_results_labeller_<N>.jsonl` (28 lines)
- `data/hu_labelling/pilot_HU1/raw_labels_labeller_<N>.jsonl` (5 lines)

## Methodology rules (binding)

- **Fresh agent, no shared state**: do not look at other labellers' outputs; do not assume what they will say.
- **Bucket-first per `feedback_bucket_first_labelling.md`**: NO equity thresholds in your reasoning; use composition class (TP+/draws/air) + protocol rules. Equity thresholds will be applied AFTER labelling by `spot_classifier.py`.
- **Solver-vs-labels per `feedback_solver_vs_expert_labels.md`**: do NOT cite solver output as your label rationale; you are an expert labeller, not a solver.
- **Terminology per `feedback_terminology_raise_vs_bet.md`**: "raise" = raise of an existing bet; "bet" = first postflop bet; "open" = preflop opener.
- **No deviation from v3.4 protocol**. If a hand seems to defy the protocol's rules, default to the protocol's explicit guidance (e.g., DO NOT Rule 11 default-CHECK with confidence MEDIUM) rather than inventing a new path.
- **No solver-pulling**: if you cannot decide between two actions, pick the one the protocol's decision rule would default to; do NOT consult solver output to break ties.

## Methodology constraints unique to this pilot

- The labelling protocol (v3.4) is 3-way-framed. The HU-1 pilot hands are heads-up. v3.4 has explicit HU carve-outs (line 729 etc.) — apply them. The 3-way-multiway rules (range collisions, multiway aggression compression) become vacuous for HU spots; do not over-extend them.

- The 28-hand calibration is 3-way (the 24 BATCH2 multiway anchors + 4 hard anchors). 3-way calibration is a competence superset of HU; passing 3-way calibration validates your reasoning ability for the HU pilot task.

## When you're done

Write your two output files. Confirm in your final response:
1. Both output files written (path + line count)
2. Calibration self-check: how many of 28 you labelled with HIGH confidence
3. Pilot summary: per-hand action + confidence (one line each)
