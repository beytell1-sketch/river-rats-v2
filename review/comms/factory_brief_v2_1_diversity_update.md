---
date: 2026-04-09
from: Builder
re: Factory brief v2.1 — diversity requirements incorporated
---

## What changed

Owner asked how we ensure factory produces varied, realistic situations.
Diversity audit (review/FACTORY_DIVERSITY_AUDIT.md) found:

1. **SPR=1.11 uniformity** — 53% of Batch 1 at same SPR (serious)
2. **65% OOP bias** — new batch needs 55%+ IP
3. **Villain-feature clustering** — same board = same villain features
4. **Paired boards at 6.5%** vs 17% real frequency

Seven mandatory diversity requirements (R1-R7) plus per-sub-pattern
variation requirements incorporated into FACTORY_DESIGN_RAISE_CONTEXTS_V2.md.

14-point reviewer checklist added — all checks must be documented
before batch approval.

## What was NOT changed

- Situation counts (still 109 RAISE + 42 CALL = 151)
- Sub-pattern structure (still 10 patterns)
- Tree alignment (still v2)
- Correctness constraints (still present)

## Files updated

- review/FACTORY_DESIGN_RAISE_CONTEXTS_V2.md — diversity requirements
  and reviewer checklist added after design constraints section
- review/FACTORY_DIVERSITY_AUDIT.md — full audit (reference document)

## Ready for review
