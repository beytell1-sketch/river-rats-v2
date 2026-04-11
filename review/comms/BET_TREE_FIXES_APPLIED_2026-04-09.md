---
date: 2026-04-09
from: Builder
re: BET tree v1 — 4 review fixes applied
---

## Fixes applied

1. **is_pfa → is_preflop_aggressor** — all 9 Quick Reference occurrences
2. **S2 override list** — Step 3B added as OOP exception alongside Steps 2 and 6
3. **Tier priority rule** — "evaluate in order — first match applies" added
4. **Danger_score gap** — monster trap threshold corrected from < 0.30 to < 0.45

## Not changed (noted for future)

5. RAISE tree preamble still says 52 features — update in next revision
6. Step 4D rainbow gate — reviewer suggests flush_danger <= 0.25 instead.
   Keeping is_rainbow for now (conservative). Can loosen in v2 if data shows
   legitimate edge cases being missed.

## Ready for owner approval
