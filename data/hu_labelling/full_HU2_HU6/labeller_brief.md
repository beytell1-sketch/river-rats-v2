# Phase 1.5-D.2 FULL — HU Reference Set Labeller Brief (HU-2..HU-6)

You are a fresh GTO labelling agent for Phase 1.5-D.2 FULL of the River Rats v2 project. You have NO shared state with other labellers. This is the FULL batch (25 hands across axes HU-2..HU-6) following the pilot (HU-1) which cleared the gate at 5/5 unanimous + QC PASS.

## Your task in 3 phases

### Phase 1: Read protocol + KB (do this first; do not skip)

1. `Read prompts/gto_labeller_v3.4.md` — labelling protocol you MUST follow verbatim. Apply ALL DO NOT Rules including Rule 11 (paired-board / 2-tone OOP exception) and the v3.2 KB §1.7 OVERRIDE.
2. `Read knowledge/three_way_gto.md` — knowledge base referenced by the protocol.

### Phase 2: BLIND calibration exam (28 hands; re-validated per dispatch)

You take the 28-hand calibration exam BLIND. **You MUST NOT** read `river-rats-core/calibration_exam.py` or any answer key before completing your labels. Reading the answer key disqualifies you.

Calibration hand sources:
- `Read design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — 24 multiway reference hands (MW-11 through MW-50, num_opponents=2 only). Action histories, hero hands, boards, positions all there.
- 4 additional hard-anchor calibration hands. Look up these `ref_id` strings in `training-data/test_set_50_labelled.jsonl` and `training-data/3way_combined_350.jsonl` (extract only the spot fields and feat_dict; do NOT read expert_action / expert_reasoning / oracle_action / adjusted_action / difficulty / alternatives_considered / key_factors fields):
  - `d8886_BB_flop`
  - `d2410_CO_turn`
  - `d8963_HJ_turn`
  - `d3178_CO_river`

Output format per calibration hand (one JSON object per line; write to your assigned `calibration_results_labeller_<N>.jsonl`):

```json
{"ref_id": "MW-11", "predicted_action": "CHECK", "confidence": "HIGH", "reasoning": "<2-4 sentences citing protocol rules + features>"}
```

`predicted_action` ∈ {`FOLD`, `CHECK`, `CALL`, `BET`, `RAISE`}. `confidence` ∈ {`HIGH`, `MEDIUM`, `LOW`}.

### Phase 3: HU-2..HU-6 FULL labelling (25 hands)

After calibration, label the 25 HU FULL hands (5 per axis × 5 axes):

- **Axis HU-2 (drawing)**: HU-2.1 through HU-2.5 — read `design/hu_reference_set/HU_AXIS_2_DRAWING.md`
- **Axis HU-3 (air with backdoors)**: HU-3.1 through HU-3.5 — read `design/hu_reference_set/HU_AXIS_3_AIR_BACKDOORS.md`
- **Axis HU-4 (PFA postflop)**: HU-4.1 through HU-4.5 — read `design/hu_reference_set/HU_AXIS_4_PFA_POSTFLOP.md`
- **Axis HU-5 (OOP decisions)**: HU-5.1 through HU-5.5 — read `design/hu_reference_set/HU_AXIS_5_OOP_DECISIONS.md`
- **Axis HU-6 (river decision precision)**: HU-6.1 through HU-6.5 — read `design/hu_reference_set/HU_AXIS_6_RIVER_PRECISION.md`

Each axis file has 5 hand specs with hero cards, board, street, positions, num_opponents, action history, composition class. Apply the v3.4 protocol with explicit attention to its HU carve-outs (e.g., line 729: "Heads-up spots (`num_opponents = 1`) — bet for value/protection per existing v3.1 rules").

All 25 HU full-batch hands have `num_opponents: 1` (explicit HU). Apply HU-appropriate reasoning per protocol.

Output format per pilot hand (one JSON object per line; write to your assigned `raw_labels_labeller_<N>.jsonl`):

```json
{"ref_id": "HU-2.1", "predicted_action": "BET", "confidence": "HIGH", "reasoning": "<2-4 sentences citing protocol rules + composition + position + sizing>", "predicted_sizing_pct": 66}
```

Include `predicted_sizing_pct` ONLY if your action is BET or RAISE. Use solver-aligned sizes per `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150).

## Output files (write to disk; you'll be told your N)

- `data/hu_labelling/full_HU2_HU6/calibration_results_labeller_<N>.jsonl` (28 lines)
- `data/hu_labelling/full_HU2_HU6/raw_labels_labeller_<N>.jsonl` (25 lines)

## Methodology rules (binding)

- **Fresh agent, no shared state**: do not look at other labellers' outputs; do not read the pilot results from `data/hu_labelling/pilot_HU1/` even though they're on disk.
- **Bucket-first per `feedback_bucket_first_labelling.md`**: NO equity thresholds in your reasoning; use composition class (TP+/draws/air) + protocol rules.
- **Solver-vs-labels per `feedback_solver_vs_expert_labels.md`**: do NOT cite solver output as your label rationale; you are an expert labeller, not a solver.
- **Terminology per `feedback_terminology_raise_vs_bet.md`**: "raise" = raise of an existing bet; "bet" = first postflop bet; "open" = preflop opener.
- **No deviation from v3.4 protocol**. If a hand seems to defy the protocol's rules, default to the protocol's explicit guidance rather than inventing a new path.

## Methodology constraints unique to this batch

- The labelling protocol (v3.4) is 3-way-framed. The HU-2..HU-6 full-batch hands are heads-up. v3.4 has explicit HU carve-outs (line 729 etc.) — apply them. The 3-way-multiway rules become vacuous for HU spots; do not over-extend them.
- The 28-hand calibration is 3-way (the 24 BATCH2 multiway anchors + 4 hard anchors). 3-way calibration is a competence superset of HU; passing 3-way calibration validates your reasoning ability for the HU full-batch task.
- **Pilot precedent (informational; don't anchor on it):** the HU-1 pilot reached 5/5 unanimous on all 5 hands across 5 fresh labellers. Reach your own conclusions on HU-2..HU-6 independently.

## When you're done

Write your two output files. Confirm in your final response:
1. Both output files written (path + line count)
2. Calibration self-check: how many of 28 you labelled with HIGH confidence
3. Per-axis pilot summary: for each axis HU-2 through HU-6, list the 5 hands with action + confidence
