---
date: 2026-04-09
from: Builder
re: All three decision trees complete — ready for deterministic labelling
---

## Three trees, five actions, zero gaps

| Tree | Applies when | Outputs | Status |
|------|-------------|---------|--------|
| BET tree v1 | to_call == 0 | BET or CHECK | Reviewed, PASS |
| RAISE tree v2 | facing bet | RAISE or pass to FOLD tree | Approved |
| FOLD tree v1 | facing bet, RAISE didn't fire | FOLD or CALL | Reviewed, PASS |

## Decision flow

```
Situation arrives
  → to_call == 0?
    YES → BET tree → BET or CHECK
    NO  → RAISE tree → RAISE?
      YES → RAISE
      NO  → FOLD tree → FOLD or CALL
```

## Files

| File | What |
|------|------|
| review/RAISE_DECISION_TREE_V2.md | RAISE tree (approved) |
| review/BET_DECISION_TREE_V1.md | BET tree (reviewed, awaiting approval) |
| review/FOLD_DECISION_TREE_V1.md | FOLD tree (reviewed, awaiting approval) |

## What's next after approval

1. Write deterministic labelling script (applies all 3 trees to 563 situations)
2. LLM reviewer sample (~60 situations) checks script output
3. Output: all_labels_v3_1.json
4. Then Steps 8-13 per handoff sequence

## For owner

BET tree and FOLD tree need your approval. RAISE tree is already approved.
