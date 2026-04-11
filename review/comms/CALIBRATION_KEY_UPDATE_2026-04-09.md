---
date: 2026-04-09
from: Builder
re: Calibration answer key corrections — MW-30 and MW-50
---

## Gate: Calibration key must be current before Step 7 labelling

Two hands need resolution. The answer key is in
design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md (GTO Action Table).

---

## MW-30: FOLD → CALL (SOLVER-VERIFIED)

**Current key:** FOLD (HIGH confidence)
**Solver result:** Pure CALL for all KT combos (GTO Wizard)
**Hand:** KcTh on KJ6r, facing CO bet + BTN call

The solver correction is documented in memory/reference_corrections.md
(7 Apr 2026). The Phase 2 reference audit verified the action sequence
tuple (1,0,0,1,0) is correct. The agent already answers CALL citing
the KB correction (Example 3).

**Recommendation: Update to CALL.** The evidence is:
- Solver: pure CALL
- Equity: 40% vs 18% pot odds = 22pp surplus
- KB v1.2 Example 3 already teaches CALL for this pattern
- The labelling agent already learned this correction

If the key stays FOLD, every labelling agent will be penalised for
giving the correct answer during calibration.

---

## MW-50: FOLD → ? (UNVERIFIED)

**Current key:** FOLD (HIGH confidence)
**Hand:** JcTc top pair OOP facing BTN turn bet after flop raise, J845
**Equity:** 33% vs 29% pot odds = 4pp surplus

The memory file flags MW-50 as "likely CALL" based on the same
over-fold pattern as MW-30. But MW-50 has NOT been solver-verified.

**Key differences from MW-30:**
- MW-30 has 22pp equity surplus — clear call even with narrowed ranges
- MW-50 has only 4pp surplus — marginal, ranges matter more
- MW-50 faces a flop raise + turn barrel (two streets of aggression)
- MW-50 hero is OOP with a weak kicker (JT on J845)

**Recommendation: Keep FOLD for now.** The 4pp surplus is thin enough
that narrowed villain ranges could flip it. Unlike MW-30 (where the
surplus overwhelms the range signal), MW-50 is genuinely close. Without
solver verification, changing it risks introducing an error into the
key. If we later solver-verify MW-50, we can update.

**Alternative:** If you want to resolve it now, I can run a solver
check on MW-50. But that adds scope to this session.

---

## Summary

| Hand | Current | Proposed | Status |
|------|---------|----------|--------|
| MW-30 | FOLD | **CALL** | Solver-verified, recommend update |
| MW-50 | FOLD | **FOLD** (keep) | Unverified, thin margin, recommend keep |

Awaiting your approval before editing the answer key.
