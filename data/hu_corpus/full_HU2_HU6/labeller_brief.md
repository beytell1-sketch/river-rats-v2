# Phase 1.5-D.3 FULL — HU Corpus Labeller Brief (696 lookalike spots; HU-2..HU-6 axes)

You are a fresh GTO labelling agent for Phase 1.5-D.3 FULL — labelling ~696 HU lookalike situations from HU-2..HU-6 axes (24 anchors, ~29 variations each).

**This is the FULL phase** following Phase 1.5-D.3 PILOT V2 (50 HU-1 spots; PR #344 merged with QC PASS · 0/0/0). FULL labellers are a fresh pool (NOT L1..L5 from PILOT V2 — fresh draw to avoid same-pool overfit).

## Your task in 3 phases

### Phase 1: Read protocol + KB

1. `Read prompts/gto_labeller_v3.4.md` — labelling protocol; apply verbatim including DO NOT Rule 11 + KB §1.7 OVERRIDE.
2. `Read knowledge/three_way_gto.md` — KB.

### Phase 2: BLIND calibration exam (28 hands; SANITIZED sources per dispatch §(c.1))

You take the 28-hand calibration exam BLIND. **You MUST NOT** read `river-rats-core/calibration_exam.py` or any answer key file.

**IMPORTANT — SANITIZED SOURCES (per dispatch §(c.1)):** The training-data JSONL files contain `expert_action` / `expert_reasoning` / `oracle_action` fields that would leak the answer. Use the sanitized extracts that have these fields stripped:

Calibration sources (USE THESE — sanitized):
- `Read data/hu_corpus/full_HU2_HU6/calibration_sources/BATCH2_8_HAND_DESIGNS_SANITIZED.md` — 24 multiway hands (filter to num_opponents=2). Markdown reference set with situation specs but answer-prose lines stripped.
- 4 hard anchors from sanitized JSONL extracts:
  - `data/hu_corpus/full_HU2_HU6/calibration_sources/test_set_50_labelled_SANITIZED.jsonl` (filter to ref_id `d8886_BB_flop`)
  - `data/hu_corpus/full_HU2_HU6/calibration_sources/3way_combined_350_SANITIZED.jsonl` (filter to ref_id `d2410_CO_turn`, `d8963_HJ_turn`, `d3178_CO_river`)

**Do NOT** read the unsanitized source files at `training-data/test_set_50_labelled.jsonl` or `training-data/3way_combined_350.jsonl` — those contain the answer fields and would corrupt your blind calibration.

Output format per calibration hand to `data/hu_corpus/full_HU2_HU6/calibration_results_labeller_<N>.jsonl` (28 lines):

```json
{"ref_id": "MW-11", "predicted_action": "CHECK", "confidence": "HIGH", "reasoning": "<2-4 sentences>"}
```

Pass thresholds: ≥20/28 correct AND 100% on GTO_REVERSAL_HANDS (which now includes MW-30, MW-33, MW-50 plus 7 newer anchors per `river-rats-core/calibration_exam.py` `GTO_REVERSAL_HANDS` definition — but you don't read that file, the grader applies the rule post-hoc).

### Phase 3: HU FULL labelling (696 lookalikes)

Read `data/hu_corpus/full_HU2_HU6/situations.jsonl` — each line is a JSON object with `spot_id`, `anchor_id`, `hero_cards`, `board_flop`, `street`, `hero_pos`, `villain_pos`, `pot_bb`, `facing_bet`, `to_call_bb`, `effective_stack_bb`, `opener`, `bettor`, `composition`, `axis`, `action_summary`, `variation_axis`, `variation_param`, `lookalike_brick` (board_runout only).

**Important — stale composition/action_summary fields (per dispatch §(c.3) Path b):** For `variation_axis = "board_runout"` rows, the `board_flop` / `board_turn` / `board_river` fields differ from the anchor (a brick has been replaced). The `composition` and `action_summary` prose fields STILL describe the ANCHOR (not the lookalike). Per dispatch §(c.3) builder choice: this is INTENTIONAL — labellers are expected to read the structured board fields and reach independent conclusions about hero's hand strength, ignoring stale prose. PILOT V2 evidence (PR #344) confirmed labellers correctly do this.

**Concrete example**: HU-1.4 anchor was hero TT on board "8h5c2dTc" (turn = Tc, hero has set of tens). A board_runout lookalike replaces Tc with 6c, board becomes "8h5c2d6c". The `composition` field still says "TP+ (set of tens; turned set on rainbow)" but with the actual 6c turn, hero's TT is just an overpair — read the board, not the prose.

For each of the ~696 spots:
1. Reconstruct the situation from the structured fields.
2. All spots have `num_opponents: 1` (HU). Apply v3.4 line 729 HU carve-out (bet for value/protection per v3.1 rules).
3. Apply the v3.4 protocol verbatim.

Output per spot to `data/hu_corpus/full_HU2_HU6/raw_labels_labeller_<N>.jsonl` (~696 lines):

```json
{"spot_id": "HU-2.1-LK-01", "predicted_action": "BET", "confidence": "HIGH", "reasoning": "<2-4 sentences>", "predicted_sizing_pct": 25}
```

Use `spot_id` as the identifier. Include `predicted_sizing_pct` only if action is BET or RAISE; sizes per `feedback_solver_aligned_sizing.md` (flop 25/66, turn 33/75, river 33/75/150).

Include `labeller_id: <N>` in EVERY raw_label row.

## Methodology rules (binding)

- **Fresh agent, no shared state**: do not look at other labellers' outputs; do not read pilot_HU1, full_HU2_HU6 (other labellers' files), pilot_50 (v1), or pilot_50_v2 directories' raw_labels files. (You CAN read pilot_50_v2/labeller_brief.md for protocol clarification if needed.)
- **Bucket-first**: NO equity thresholds in reasoning; use composition + protocol rules.
- **Solver-vs-labels**: don't cite solver as label rationale.
- **Terminology**: raise = raise of existing bet; bet = first postflop bet; open = preflop opener.
- **HU-only**: every spot has num_opponents=1; v3.4 line 729 HU carve-out applies; Rule 11 multiway predicates do NOT trigger.
- **Sanitized calibration**: use ONLY the SANITIZED files in `data/hu_corpus/full_HU2_HU6/calibration_sources/`; do NOT grep or read the unsanitized originals at `training-data/`.
- **Lookalike interpretation**: each spot is a variation of an HU-2..HU-6 anchor. Use `variation_axis`/`variation_param`/board fields. Anchor's GTO action does NOT auto-apply.

## When you're done

Confirm:
1. Both files written + line counts (28 calibration + ~696 pilot = ~724 hands)
2. Calibration self-check: HIGH-confidence count out of 28
3. Pilot summary: count of each action across ~696 spots
4. Confirm sanitization compliance: report that you used `calibration_sources/*SANITIZED*` files only (not the unsanitized `training-data/` originals).
