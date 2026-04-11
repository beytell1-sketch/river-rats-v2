---
date: 2026-04-09
from: Builder
re: Batch 4 design — consolidated issues and fixes
---

## Issues resolved directly

1. **B4_24 rainbow**: Changed 6s 3d 2s → 6c 3d 2h (rainbow). BP5 sits 11-12 now valid for Step 6.
2. **B4_03 action history**: BTN check removed (BTN acts after CO hero).
3. **Agent B self-corrections**: 6 hero card conflicts caught and fixed during design.
4. **Agent C self-corrections**: Sit 2 straight completion caught and fixed.

## Issues requiring generation-time resolution

### BP3 OI-1: high_card_rank < 12 on B4_07 and B4_08

B4_07 (Jc 9h 7s, hcr=11) and B4_08 (Tc 8h 5s, hcr=10) are below
Step 4's high_card_rank >= 12 gate. 5 BP3 situations use these boards.

**Fix for generation script:** Reassign these 5 situations to two-tone
Q+ boards. B4_05 (Qs 9c 5h, hcr=12), B4_06 (Qd Jd 5c, hcr=12),
and B4_10 (Qh 9s 8h, hcr=12) are all Tier 2 boards with hcr=12.
The hero hands need to be redesigned for the new boards (different
suits, different draws).

### BP3 OI-3: 4A combo draws on rainbow boards

4A requires draw_outs >= 12. On rainbow boards, max is ~8 (OESD).
Need flush draw + straight draw for 12+ outs. All 4A situations
MUST be on two-tone boards.

**Fix:** B4_05 (Qs 9c 5h — spade+club), B4_06 (Qd Jd 5c — diamond),
B4_09 (Kh 7h 4c — hearts), B4_10 (Qh 9s 8h — heart) are all
two-tone and have hcr >= 12. Use these for ALL 4A situations.

### BP3 OI-2: Sit 18 villain_air=0.38

Move to BP6-H as CHECK counterexample. BP3 reduces to 19. Accept.

## Revised totals after all fixes

| Sub-pattern | Original | After fixes |
|-------------|----------|-------------|
| BP1 | 30 | 30 |
| BP2 | 12 | 12 |
| BP3 | 20 | 19 (sit 18 → BP6) |
| BP4 | 15 | 15 |
| BP5 | 12 | 12 |
| BP6 | 15 | 16 (gained sit 18) |
| **Total** | **104** | **104** |

## Recommendation

These fixes are best applied in the generation script rather than
rewriting the design documents. The generation script can:
1. Remap BP3 sits 1-5 (B4_07/B4_08) to B4_05/B4_06/B4_10 with new hero hands
2. Remap BP3 4A sits to two-tone boards only
3. Move BP3 sit 18 to BP6-H
4. Use B4_24 = ['6c', '3d', '2h'] (already fixed in allocation)

Writing the generation script now with all fixes incorporated.
