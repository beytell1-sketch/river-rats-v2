# Labelling Pipeline — Step-by-Step

## Overview

Situations → Batches → GTO Expert agents → Collect → Training CSV

All commands run from `river-rats-core/`.

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
Gate: 20/24 minimum, all 3 GTO-reversal hands correct.

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
| `prompts/gto_labeller_v1.md` | Labelling agent prompt |
| `knowledge/three_way_gto.md` | GTO knowledge base (v1.1) |
| `review/label_batches/agent_context.txt` | Combined prompt + knowledge |
| `labelling_agent.py` | Prepare batches + collect results |
| `calibration_exam.py` | Exam infrastructure |
| `export_3way_training.py` | JSONL → CSV conversion |
| `situation_factory.py` | Construct situations from specs |
| `reference_evaluator.py` | Gate check evaluator |

## Checksums (verify files haven't changed)

```bash
md5sum knowledge/three_way_gto.md prompts/gto_labeller_v1.md
# Expected (as of 7 Apr 2026, v1.2):
# 78dd5008d39d1388bcb428faaa4d3869  knowledge/three_way_gto.md
# ddccb338b59123086f3f5a57857a886a  prompts/gto_labeller_v1.md
```

If checksums differ, the knowledge base was edited. Re-run
calibration before labelling.
