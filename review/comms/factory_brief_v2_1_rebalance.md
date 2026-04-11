---
date: 2026-04-09
from: Builder
re: Factory brief v2.1 — distribution rebalance
---

## What changed

Owner flagged that v2 brief fell short of the 150-160 RAISE target
and the distribution was imbalanced. Analysis confirmed:

- Self-play and existing labels are ~95% value RAISE
- Factory v2 provided only 79 RAISE, projecting ~127 total (short of 150)
- Semi-bluff at 20% vs 30% target, thin value and bluff also under

## Additions (v2.1)

| Sub-pattern | v2 count | v2.1 count | Change | Reason |
|-------------|----------|------------|--------|--------|
| SP5 semi-bluff | 16 | 28 | +12 | Largest gap vs 30% target |
| SP7 thin value | 15 | 25 | +10 | Self-play contributes ~0 |
| SP8 bluff | 8 | 16 | +8 | Self-play contributes 0 |
| SP1-SP3 value | 40 | 40 | 0 | Already over-supplied |

Total factory RAISE: 79 → 109
Total new situations: 121 → 151
Projected total RAISE: ~176-181 (exceeds target, provides buffer)

## What did NOT change

- CALL counterexamples: still 42
- Sub-pattern structure: still 10 patterns
- All v2 tree alignment: unchanged
- Design constraints: unchanged

## Ready for review
