---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 3.5 M4 — distribution-shift audit on existing training rows
status: AUDIT COMPLETE
---

# Stage 3.5 M4 — Distribution-Shift Audit

Re-extracted villain composition features on existing training rows
using the new action-aware chained narrowing. Compared against
stored pre-Stage-3.5 values.

## Coverage

```
Total training rows loaded: 579
Build failures:             0
Flop-only rows:             124
Multi-street rows:          455
```

## Per-feature distribution shift

| feature | street | n | mean_delta | median_delta | max_abs | |delta| > 0.05 |
|---|---|---|---|---|---|---|
| tp_plus | flop | 124 | +0.0000 | +0.0000 | 0.0000 | 0 |
| tp_plus | turn | 306 | -0.1449 | -0.1203 | 0.3333 | 288 |
| tp_plus | river | 149 | -0.2659 | -0.2763 | 0.5797 | 149 |
| medium | flop | 124 | +0.0000 | +0.0000 | 0.0000 | 0 |
| medium | turn | 306 | +0.0403 | +0.0100 | 0.3364 | 66 |
| medium | river | 149 | +0.1124 | +0.0000 | 0.5915 | 63 |
| draw | flop | 124 | +0.0000 | +0.0000 | 0.0000 | 0 |
| draw | turn | 306 | +0.0342 | +0.0080 | 0.1923 | 105 |
| draw | river | 149 | +0.0000 | +0.0000 | 0.0000 | 0 |
| air | flop | 124 | +0.0000 | +0.0000 | 0.0000 | 0 |
| air | turn | 306 | +0.0704 | +0.0830 | 0.3333 | 168 |
| air | river | 149 | +0.1535 | +0.1328 | 0.3907 | 110 |


## Isolation check (flop-only rows should not shift)

Flop-only rows (n=124) — should have ≤ 0.01 absolute
delta on composition features per GTO review Q2 (same-street
actions excluded from chain).

Isolation violations (|delta| > 0.01 on any composition feature):
0 / 124 rows

**CLEAN** — zero violations. Same-street exclusion working as specified.


## Chain activity verification

Multi-street rows with non-empty `chain_steps`:
455 / 455

If this ratio is high (>80%), chain is firing as designed on
multi-street hands. If low, action_history plumbing isn't reaching
these rows — investigate.

## Acceptable shift thresholds

Per spec lock (a4cab83):
- Flop-only rows: near-zero (< 0.01 absolute) — PASS IFF violations == 0
- Multi-street rows: any direction acceptable, any magnitude
