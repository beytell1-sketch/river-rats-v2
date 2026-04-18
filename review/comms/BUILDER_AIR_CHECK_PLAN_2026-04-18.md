---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: v2.3.1 Layer 2 — air-CHECK counter-example generator plan (pre-build)
status: PLAN — awaiting approval before building
---

# Builder Plan — Air-CHECK Counter-Examples (v2.3.1 Layer 2)

Per `MAIN_TERMINAL_UPDATE_2026-04-18-g.md` §Layer 2. Presenting
this plan for owner review before writing the generator script.
No code runs until approval.

## Deliverable

Factory-generated JSONL of ~30–40 checked-through situations where
hero has air and the correct GTO action is CHECK. These teach the
model the missing counter-example class: "villain weak + checked
back + hero has nothing → CHECK, not BET."

## Predicate (from update-g)

| Feature | Condition |
|---|---|
| `facing_bet` | 0 |
| `villain_checked_back` | 1 |
| `num_opponents` | 2 (3-way; matches v2 convention) |
| `is_made_hand` | 0 |
| `draw_outs` | ≤ 2 |
| `equity_vs_range` | < 0.35 |

## Generator design

**Location:** `review/generate_air_check_v231.py` (matches batch6 idiom)
**Output:** `training-data/v23_air_check.jsonl`

**Reuse:** `situation_factory.SituationSpec` + `build_situation` +
`normalise_situation`, plus `ARCHETYPES_IP` / `ARCHETYPES_OOP`,
`DRY_BOARDS` / `TWO_TONE_BOARDS` from the batch6 template.

**Hero selection (new helper):** `_is_air_or_weak_draw(hero, board)`
— accepts cards whose `evaluate_hand().category` is in
`AIR_CATS = {'high_card', 'overcards', 'one_overcard', 'nothing'}`.
Predicate filter drops any candidate with `draw_outs > 2` post-build.

**Action histories:**
- **Flop (hero IP):** preflop opens + calls, flop villains check
  before hero acts. Primary villain is non-opener so that
  `villain_checked_back=1` attaches to the PRIMARY villain.
  Feasible: `ARCHETYPES_IP` with non-opener primary.
- **Turn (hero any):** flop all-check, turn villains-before-hero
  check (if IP) or nothing yet (if OOP, hero acts first on turn).
- No river (per directive).

**Street / position spread (target 30–40 BP, OS 50):**

| Street | Count | Position pool |
|---|---|---|
| Flop | 18–22 | IP only (BTN-CO, BTN-HJ, CO-SB/BB etc.) |
| Turn | 18–22 | IP + OOP mix |

**Boards:** full `DRY_BOARDS` + `TWO_TONE_BOARDS` pool. At least
one monotone spec seeded (Qs5s7s) to cover the A4d litmus.

## Litmus seeds (guaranteed in output)

To ensure the generator covers the playtest findings directly,
seed two exact specs:

1. **A4d on Qs5s7s (flop, hero IP, checked-to):** BTN hero,
   villains SB/BB (primary = SB, non-opener). Validates against
   PLAYTEST_FINDING_002 directly.
2. **T5h on JJ2 (flop, hero IP, checked-to):** BTN hero, similar
   archetype. Matches the T5 litmus.

Both appear in the OS candidate set; predicate filter should pass
both (air, 0 outs, equity < 0.35, checked_back context).

## Yield / stop conditions

- **OS target:** 50 candidates
- **BP target:** ≥ 30 pass predicate + validator
- **Hard stop:** build_failure rate > 25% per CLAUDE.md §2
  (validate-yield-first discipline)
- **Preflight:** `street` and `hero_position` must serialise as
  int (ANOMALY-A guard), zero validation errors

## Post-generation checks (before labelling)

1. Count: 30 ≤ written ≤ 50
2. Predicate conformance: 100% of written rows match all 6
   predicate conditions
3. Hero bucket distribution: all `hand_bucket` = air at eval time
4. Litmus seeds present: A4d/Qs5s7s and T5h/JJ2 both in output
5. Schema preflight: 0 errors

## After approval

1. Build `review/generate_air_check_v231.py`
2. Run small test (first 10 specs) to validate yield assumptions
   per CLAUDE.md §2
3. Full run, report stats
4. Commit: `v2.3.1 Layer 2a: factory-generate ~30-40 air-CHECK
   counter-examples (v23_air_check.jsonl)`
5. Push
6. Report back with yield stats; await go-ahead for labelling via
   `labelling_agent.py prepare` + v3.1 prompt panels
7. After labels land, request confirmation before retraining
   (per restart-prompt directive)

## What this plan does NOT include

- No label generation (separate step, requires panel dispatch)
- No retraining (requires re-extract of all training data with the
  110-feature vector — Layer 2 step 5 in update-g)
- No static overrides (hard rule from restart prompt)
- No predicate softening if yield falls short — instead we'd
  report and expand OS count / board pool on a second pass

## Open questions for owner

1. **File naming:** `v23_air_check.jsonl` OK? (matches `v23_*`
   convention; alternative: `v23_air_checked_through.jsonl`)
2. **Litmus seed strictness:** Should the generator *fail* if
   either litmus seed fails the predicate, or just flag? I'll
   default to flag-and-continue unless told otherwise.
3. **Monotone coverage:** Include more monotone boards beyond
   Qs5s7s? (Current DRY/TWO_TONE pool has none.)

Ready to build on your go-ahead.
