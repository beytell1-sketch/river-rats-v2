---
date: 2026-04-20
from: Builder
to: Main terminal / Owner
re: v2.4 Stage 2 COMPLETE — KB §1.10-§1.12 added + GTO review applied
status: STAGE 2 COMPLETE — Stage 3 (v3.2 prompt) can proceed
---

# v2.4 P1 Stage 2 — COMPLETE

Per directive-aa. KB §1.10-§1.12 drafted, GTO-reviewed, all 6
required modifications applied, committed. Stage 3 gate satisfied
(KB language final + feature naming stable).

## Sections added

Inserted between existing §1.9 (Preflop geometry vs postflop
composition) and §2 (Decision Framework). Avoided renumbering
existing §1.9 because v3.1 prompt has hardcoded cross-references
to it — Stage 3 prompt derivation will re-anchor as needed.

| Section | Lines | Content |
|---|---|---|
| §1.10 | 231-425 | Defensive Blocker Direction intro + 4 feature sub-sections (§1.10.1-4) |
| §1.11 | 427-481 | Covering-triple framework + multi-signal resolution rule + combo-draw caveat |
| §1.12 | 483-506 | DO NOT Rule 6 expansion (operative labelling instructions) |

Plus: forward-pointer added to Rule 6 body (line 1069-1082) in §5
DO NOT Rules so readers arriving at Rule 6 directly find the
§1.10-§1.12 reference.

## GTO review verdict

`review/comms/GTO_REVIEW_V24_STAGE2_KB_1_10_2026-04-20.md`
(reviewer agent ID in git history) — **APPROVED_WITH_MODIFICATIONS**.
Six fixes required; all applied:

1. **§1.10.1 — texture-dependent defender direction (CRITICAL).**
   Original draft claimed `nut_flush_block=1` was uniformly
   defender-positive. Reviewer caught that on a 2-flush flop,
   the A-of-suit blocks villain's semi-bluff combos (same
   densification mechanism as §1.10.2 applied to the ace
   specifically) → defender-NEGATIVE on 2-flush, defender-POSITIVE
   on 3+-flush. Rewrote with explicit texture split + two
   defender examples (2-flush FOLD case, 3-flush CALL case).

2. **§1.10.2 — example equity math revised.** Original 0.38→0.28
   adjustment didn't clear pot-odds on stated pot-sized bet.
   Changed bet size to 1.5× pot (break-even 37.5%), so adjusted
   equity crosses under the threshold. Added a control case
   (same hand without the spade blocker stays call-correct).

3. **§1.10.3 — typo fix.** Clarified "7s" → "pair of 7s (bottom
   pair)" in the straight-draw example.

4. **§1.10.4 — aggressor scope tightened + example replaced.**
   Added "Does NOT apply to pure bluffs" caveat. Replaced the
   AcKs-on-Ks-Qs-7s-2h example (where the text mis-stated Ks as
   blocking nut flush) with a defender example aligned with the
   d2410 calibration anchor: JcKs on Jd-9d-3h-6d, where Jc
   blocks JJ trips (top_set = nut-made on paired board).

5. **§1.11 — multi-signal resolution rule added.** When both
   defender-negative (`draw_block_pct`) and defender-positive
   (`nut_made_block_pct`) fire, use the delta:
   - `nut_made − mean(flush_dr, straight_dr) > 0.15` → CALL lean
   - opposite direction > 0.15 → FOLD lean
   - |delta| ≤ 0.15 → do not tag blocker features PRIMARY
   Flagged as labelling heuristic (not solver-verified).

   Combo-draw double-counting caveat added: a `combo_draw`
   classified combo counts in BOTH flush and straight block
   fractions; sums can exceed 1.0. Use independently; do not add.

6. **§1.12 Rule 6 forward-pointer.** Added one-line reference
   in DO NOT Rule 6 body (line 1069-1082) pointing to §1.10-§1.12.

**Reviewer's side note** (outside scope, logged): lines 160 and
447 still reference "45-feature pipeline." This is v9-era text
and needs update to "59-feature pipeline" to match v2.4. NOT
fixed in this PR — that's a broader KB freshness pass (v2.4
Stage 5+ or separate cleanup).

Reviewer explicitly stated: "No second-round review needed after
the six fixes land; spot-check only."

## Alignment audit — does KB language match Stage 1 code?

| KB text | Code behavior | Match? |
|---|---|---|
| `nut_flush_block = 1` iff 2+ suit on flop / 3+ turn-river + A-of-suit + no made flush | `compute_nut_flush_block` implements exactly this with `threshold = 2 if n_board == 3 else 3` and hero+board ≥5 exclusion | ✅ |
| `flush_draw_block_pct` = fraction of villain flush-draw combos blocked | `compute_block_percentages` filters on `{nut_flush_draw, flush_draw, combo_draw}` | ✅ |
| `straight_draw_block_pct` on `{oesd, gutshot, combo_draw}` | Implemented | ✅ |
| `nut_made_block_pct` on base subcats + `strong_flush` when A-of-suit + 3+ on board | `_strong_flush_is_effective_nut` carve-out | ✅ |
| `combo_draw` counted in BOTH flush and straight block fractions | Code does exactly this | ✅ |
| Returns 0.0 (not NaN) when class empty | Code returns 0.0 | ✅ |

## Cross-stream impact

- Teaching: unchanged this stage (stays on placeholder for blocker
  text in plan v2.1)
- Game: v2.2 production, unchanged

## Stage 2 → Stage 3 handoff

Stage 3 gate is satisfied:
- [x] KB §1.10-§1.12 language final, GTO-approved
- [x] Feature naming stable as-they'll-appear to labeller panels
- [x] Code/KB alignment audited

Stage 3 prompt derivation can proceed when owner gives go. Will
derive v3.2 prompt from v3.1 by:
- Adding `nut_flush_block`, `flush_draw_block_pct`,
  `straight_draw_block_pct`, `nut_made_block_pct` to the feature
  table (55→59 rows)
- Adding feature_attention guidance per decision context
  (defender-side contexts tag blocker features PRIMARY; aggressor-
  side uses §1.7 + §1.10.1 semi-bluff pattern)
- Updating DO NOT Rule 6 to reflect the expanded §1.12 language
- Bumping prompt version to v3.2 (new file `gto_labeller_v3.2.md`)

## Artifacts this commit

- `knowledge/three_way_gto.md` — §1.10-§1.12 added (~290 new lines),
  Rule 6 extended (~8 lines)
- `review/comms/GTO_REVIEW_V24_STAGE2_KB_1_10_2026-04-20.md` — GTO verdict
- `review/comms/BUILDER_V24_STAGE2_COMPLETE_2026-04-20.md` — this doc

No code changes, no training, no prompt changes — discipline held
per directive-aa.
