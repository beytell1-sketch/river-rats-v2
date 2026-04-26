# Labelling Pipeline — Step-by-Step

## Overview

Situations → Batches → GTO Expert agents → Collect → Training CSV

All commands run from `river-rats-core/`.

> **Scope note (2026-04-26, v1.0.3 refresh per QC S-X3):** Step 0
> calibration gate, Key Files table, and Checksums sections are kept
> current with v2.3 infrastructure. Steps 1–7 below describe the v1-era
> operational pipeline (single-agent labelling, 5-factor framework
> dispatch, batched JSONL flow). For the Stage 4 pilot (15-labeller ×
> 3-protocol orchestration), the canonical dispatch spec is
> `review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3+ — that
> spec supersedes the dispatch flow in Steps 2–4 here for any pilot
> or production labelling round, while the calibration gate (Step 0)
> and post-labelling checks (Step 5) remain authoritative for both
> pipelines.

---

## Step 0: Pre-flight Checks

### Update knowledge base (if solver rules changed)
Edit `knowledge/three_way_gto.md` with any new solver findings
before labelling. The labelling agent's quality depends on this file.

### Calibration exam (MANDATORY before each labelling round)

Generate blind exam (no answers visible to agent):
```python
python3 -c "
from calibration_exam import load_3way_reference_hands, reference_hand_to_situation, format_situation_for_agent
hands = load_3way_reference_hands()
with open('/tmp/blind_calibration_exam.txt', 'w') as f:
    for hand in hands:
        sit = reference_hand_to_situation(hand)
        f.write(f'--- HAND: {hand.ref_id} ---\n')
        f.write(format_situation_for_agent(sit) + '\n\n')
"
```

Save answer key separately (agent must NOT see this):
```python
python3 -c "
import json
from calibration_exam import load_3way_reference_hands
hands = load_3way_reference_hands()
key = {h.ref_id: h.expert_action.upper() for h in hands}
with open('/tmp/calibration_answer_key.json', 'w') as f:
    json.dump(key, f, indent=2)
"
```

Dispatch agent with ONLY:
- `review/label_batches/agent_context.txt` (knowledge base)
- `/tmp/blind_calibration_exam.txt` (situations, no labels)

Agent must NOT access calibration_exam.py, BATCH2_8_HAND_DESIGNS.md,
or any file containing answer keys.

Grade independently against `/tmp/calibration_answer_key.json`.

Gate (v2.3, sourced from `river-rats-core/calibration_exam.py` —
refer to constants by name so future drift surfaces inconsistency):
- `STANDARD_PASS_THRESHOLD/STANDARD_EXAM_SIZE` (= 23/28 at v2.3) on
  the standard exam (24 existing MW reference hands + 4 new hard
  anchors)
- 100% on the reversal set
  `GTO_REVERSAL_HANDS ∪ GROUP_D_REVERSAL_HANDS` (= 10 hands at v2.3:
  MW-30, MW-33, MW-50 + d2410_CO_turn, d3178_CO_river
  predicate-matching anchors + d3688_BB_flop, d4312_CO_turn,
  d9556_BB_flop, d2074_BTN_turn, d5466_CO_flop Group-D anchors).
  ANY single reversal failure = FAIL.

Per `calibration_exam.py` v2.3 docstring: "If gate fails, the agent
must not label training data."

---

## Step 1: Generate Situations

### From SituationFactory (targeted):
Design board sweeps in review/ docs, then:
```bash
python3 generate_factory_situations.py
# Or use situation_factory.py directly with SituationSpec
```

### From self-play (natural distribution):
```bash
python3 generate_3way_situations.py --deals 10000 --seed 42 \
  --output ../training-data/3way_situations.jsonl
```

---

## Step 2: Prepare Batches

```bash
python3 labelling_agent.py prepare \
  --input ../training-data/[situations_file].jsonl \
  --batch-size 10
```

Creates:
- `review/label_batches/batch_01.txt` through `batch_XX.txt`
- `review/label_batches/agent_context.txt` (prompt + knowledge base)
- `review/label_batches/batch_index.json`

---

## Step 3: Dispatch Labelling Agents

Launch one agent per batch, all in parallel. Each agent gets:

**Prompt template:**
```
You are a GTO poker labelling agent. Read the context file and batch file, then label each hand.

CONTEXT: /home/rupertbeytell/river-rats-v2/review/label_batches/agent_context.txt
BATCH: /home/rupertbeytell/river-rats-v2/review/label_batches/batch_XX.txt

For each hand, apply the 5-factor framework. Output ONE json block per hand:
{"situation_id":"...","action":"CHECK/BET/CALL/FOLD/RAISE",
 "confidence":"HIGH/MEDIUM/LOW","reasoning":"2-3 sentences",
 "difficulty":1-3,"key_factors":["..."],
 "factor_conflicts":"None or describe",
 "alternatives_considered":["..."]}

IMPORTANT: River raises are POLARIZED — only nuts or bluffs.
Do NOT raise river with thin value (top two, overpairs). Those
hands CALL. When facing a bet, think about what calls your raise
— if only better hands call, it's a call not a raise.

Write results to: review/label_batches/batch_XX_result.txt
Write ONLY the JSON blocks.
```

---

## Step 4: Collect Results

```bash
python3 labelling_agent.py collect \
  --situations ../training-data/[situations_file].jsonl \
  --output ../training-data/[labelled_output].jsonl
```

Reports: action distribution, confidence distribution, missing batches.

---

## Step 5: Post-Labelling Checks

### Solver verify borderline spots
Any RAISE with equity < 80% (non-set) → verify with solver.
Any FOLD with equity > pot_odds + 5pp → verify with solver.
The labelling agent over-folds and over-raises in these spots.

### Leakage check before training
Compare training situations to reference set:
- Same (hero_cards, board, position, street) = direct leak
- Feature distance < 0.1 = suspicious
Remove any leaks.

---

## Step 6: Combine and Export

```python
# Combine old + new labels
combined = old_labels + new_labels
# Export 
python3 export_3way_training.py \
  --input ../training-data/combined.jsonl \
  --output ../training-data/train_3way.csv
```

Export preserves 5-class labels (CHECK, BET, CALL, FOLD, RAISE).
No vocabulary mapping — the model is 5-class.

---

## Step 7: Train

From-scratch (NOT warm-start for 3-way):
```python
model = xgb.XGBClassifier(
    n_estimators=300, max_depth=4, learning_rate=0.05,
    subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
    gamma=0.2, reg_alpha=0.5, reg_lambda=2.0,
    objective='multi:softprob', num_class=5,
    eval_metric='mlogloss', random_state=42,
    early_stopping_rounds=30)
```

---

## Step 8: Gate Check

```python
from reference_evaluator import evaluate_variants, format_eval_report
from multiway_adjuster import get_default_params
from self_play import Variant

baseline = Variant('baseline', get_default_params())
r = evaluate_variants([baseline], oracle_path='models/[model].json')
print(format_eval_report(r))
```

Gates:
- Reference: >= 32/40
- No regression on any axis below v2.2 levels
- Feature importance: drop any new feature below 1%
- Leakage check passed

---

## Key Files

| File | Role |
|------|------|
| `prompts/gto_labeller_v3.1.md` | Labelling agent prompt (current; v3.1) |
| `prompts/gto_labeller_v3.md` / `v2.md` / `v1.md` | Historical lineage (do not use for new labelling) |
| `knowledge/three_way_gto.md` | GTO knowledge base (current: v1.3) |
| `review/label_batches/agent_context.txt` | Combined prompt + knowledge |
| `labelling_agent.py` | Prepare batches + collect results |
| `calibration_exam.py` | Exam infrastructure (v2.3 — `STANDARD_EXAM_SIZE = 28`, `STANDARD_PASS_THRESHOLD = 23`, `GTO_REVERSAL_HANDS ∪ GROUP_D_REVERSAL_HANDS = 10` reversal hands) |
| `export_3way_training.py` | JSONL → CSV conversion |
| `situation_factory.py` | Construct situations from specs |
| `reference_evaluator.py` | Gate check evaluator |

## Checksums (verify files haven't changed)

```bash
sha256sum knowledge/three_way_gto.md prompts/gto_labeller_v3.1.md \
          river-rats-core/calibration_exam.py
# Recompute and record the SHA256 of the current canonical artifacts
# at pilot dispatch time (per Stage 4 pilot orchestration spec
# PRE-DISPATCH PREREQUISITES row #4 — Protocol A v3.1 frozen +
# checksum recorded; capture in pilot run report).
```

If checksums differ between dispatch and end-of-pilot, an
infrastructure file was edited mid-pilot. Re-run calibration before
trusting any labels produced after the edit. Per QC HIGH-2 (S-X1)
2026-04-26 finding: do NOT hardcode expected hashes here — the
canonical sources of truth are the file contents at master HEAD;
hardcoded hashes invariably go stale and produce false-positive
"changed" alarms.
