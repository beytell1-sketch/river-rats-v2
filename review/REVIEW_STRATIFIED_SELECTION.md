# Review: Stratified Selection of 200 Situations for Labelling

**Date:** 6 April 2026
**Status:** REVIEW — selection complete, awaiting approval before labelling

---

## Process

1. GTO expert agent defined stratification criteria
2. Programmer implemented selection with street-balanced allocation
3. First pass had river-skewed output (97/44/59) due to non-CHECK
   situations being 66% river. Fixed by adding street caps.

## Selection Strategy

**Priority 1:** Lock all 27 facing-bet situations (rare, high-value).
**Priority 2:** Lock all non-CHECK actions (CALL > RAISE > FOLD),
respecting street caps of 67 per street. 5 river FOLDs dropped.
**Priority 3:** Fill remaining budget per street from CHECK pool,
stratified by equity quintile (oversample Q1 and Q5 tails) and
position (55% OOP / 45% IP).
**Constraint:** Max 3 situations per deal_id for board diversity.

## Final Distribution

| Dimension | Value |
|-----------|-------|
| **Total** | **200** |
| Unique deals | 104 (of 125 in pool) |

### Street (balanced)
| Street | Count |
|--------|-------|
| Flop | 67 |
| Turn | 67 |
| River | 66 |

### Action (52% non-CHECK — deliberate oversample)
| Action | Count | Pool % | Selected % |
|--------|-------|--------|------------|
| CHECK | 97 | 89% | 48% |
| FOLD | 55 | 6% | 28% |
| RAISE | 37 | 4% | 19% |
| CALL | 11 | 1% | 6% |

### Position
| Type | Count |
|------|-------|
| OOP | 112 (56%) |
| IP | 88 (44%) |

### Equity Quintiles (tails oversampled)
| Bucket | Count |
|--------|-------|
| Q1 (<20%) | 82 |
| Q2 (20-40%) | 35 |
| Q3 (40-60%) | 20 |
| Q4 (60-80%) | 23 |
| Q5 (80%+) | 40 |

### Seat
| Position | Count |
|----------|-------|
| BTN | 75 |
| BB | 56 |
| CO | 38 |
| HJ | 23 |
| UTG | 8 |

### Facing Bet
| | Count |
|-|-------|
| Facing bet | 27 |
| Not facing | 173 |

## Notes

- **5 non-CHECK situations dropped** (river FOLDs) to maintain
  street balance. These are low-equity river folds — the least
  informative of the non-CHECK pool.
- **104 unique deals** across 200 situations. Max 3 per deal.
  31 deals at the cap of 3.
- **Oracle actions are NOT labels.** The GTO Expert will
  independently determine the correct action. The oracle's CHECK
  may become BET, the oracle's FOLD may become CALL. The action
  distribution above is the oracle's guess, not the training target.

## Output

`training-data/3way_selected_200.jsonl` — 200 situations ready
for labelling pipeline.

## Next Steps (pending approval)

1. Run `labelling_agent.py prepare` to create batch files
2. Dispatch GTO Expert agents to label batches
3. Run `labelling_agent.py collect` to merge labels
4. Run `export_3way_training.py` to create training CSV
5. Train v9-3way model
6. Gate check against reference evaluator
