---
date: 2026-04-09
from: Builder
re: Feature 53 (is_preflop_aggressor) — added and regenerated
---

## Done

1. feature_keys.py: IS_PREFLOP_AGGRESSOR added (Step 14)
2. feature_extractor.py: computation added (hero_pos == opener_position)
3. gto_model.py: FEATURE_COLUMNS updated (53 features)
4. All 3 factory batches regenerated:
   - Batch 1: 151 rows (PFA=0: 151, PFA=1: 0)
   - Batch 2: 261 rows (PFA=0: 201, PFA=1: 60)
   - Batch 3: 151 rows (PFA=0: 93, PFA=1: 58)
5. Batch 3 now 0 errors (SP8_06 SUSPICIOUS resolved by regeneration)

## Distribution note

Batch 1 has zero PFA=1 situations because all batch 1 boards use
BB or SB as hero (defenders). This is a known OOP bias from the
original factory design. Batch 2 and 3 have ~25-38% PFA situations
(hero is CO or BTN opener).

## Verification

- Feature value verified across 4 test cases (match, no-match,
  missing opener, case-insensitive)
- No existing features changed (confirmed by spot-checking 5
  situations' feature values before/after)
- FEATURE_COLUMNS count: 53

## Next

Phase B: C-bet research before labelling BET situations.
This is next session's primary task per the approved plan.
