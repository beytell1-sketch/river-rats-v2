---
date: 2026-05-06
from: LEAD-PROGRAMMER (Builder)
to: Main terminal (orchestrator)
re: 12.5I-MW40-VERIFICATION-B factory pre-flight HALT — sub-axis B blocker-variation spec contradicts hero-hand spec; require orchestrator resolution before emit
status: QUERY — factory NOT fired; awaiting MAIN_TERMINAL_* resolution
branch: programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06 (no commits yet)
---

# 12.5I-MW40-VERIFICATION-B — pre-emit HALT on plan §4 contradiction

## Headline

Factory specification in `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228 merged) §4 sub-axis B has an internal contradiction between the **hero-hand class** and the **blocker-variation rule**:

- Plan §4 sub-axis B hero hand: **TT or T9** (no J in hand)
- Plan §4 blocker variation rule: **5 of 10 within each sub-axis include hero J-blocker; 5 of 10 do not** — example given "hero holds the off-suit J as kicker"
- ⇒ within sub-axis B, hero TT or T9 ⇒ hero NEVER holds a J ⇒ blocker variation **cannot** be 5/5 within sub-axis B (it is forced to 0/10)
- Dispatch §"Stop conditions": **"Blocker split not exactly 15/15 → STOP"**

A 0/10 distribution within sub-axis B would force sub-axis A or C to swap to 10/0 to preserve the 15/15 total. That redistribution is a plan deviation per `feedback_explicit_action_trigger.md` and is not a builder-scope fix.

**No situations have been emitted.** Factory script is unstarted. PR not opened. Builder STOPPED before any side-effect.

## Verification of the contradiction (factual citation)

### From plan §4 (sub-axis B):
> **Sub-axis B — J-low flop with J-on-turn (10 variants)** … **Hero hand:** hero TT or T9 (TPMK on flop with T as top pair); turn-J reveals AhTs-equivalent runout

Boards listed: `9c5d3h, 7c4d2s, 8h6c2d, 9h6c3s, 8c5d2h, 7d4s2c, 9s6h4d, 8d5c3s, 7s5h2d, 9d6s4c` (turn=Js for each). All flops are J-low (no J on flop).

### From plan §4 (Blocker variation):
> **Blocker variation per `feedback_solver_findings.md` finding 2:** within each sub-axis, **5 of 10 variants** include hero J-blocker (e.g., hero holds the off-suit J as kicker on a board with another J), **5 of 10 do not**. Total: 15 with-J-blocker / 15 without across the 30 variants.

### Why this is internally contradictory

- Hero TT contains zero Js → hero blocks zero of the four Js. **No-J-blocker by construction.**
- Hero T9 contains zero Js → same conclusion. **No-J-blocker by construction.**
- The example "hero holds the off-suit J as kicker on a board with another J" requires hero to hold a J, which contradicts "hero TT or T9".
- Within sub-axis B's design, all 10 variants are no-J-blocker → blocker split forced to 0/10 (or 10/0 trivially-not-achievable).
- Plan §10 R1 already flagged sub-axis B as a "stress-test, not a direct test of board-J-at-decision-time" — but did NOT identify the blocker-variation contradiction; it was only spotted at factory-script-design time during MW40-VERIFICATION-B.

The dispatch's stop condition "Blocker split not exactly 15/15 → STOP" applies to the **total** (15/15 across all 30). The plan also imposed a stricter per-sub-axis 5/5 distribution. The plan-internal stricter rule is what cannot be satisfied for sub-axis B given its hero-hand spec.

## Why I cannot fix-forward (memory anchors)

- `feedback_explicit_action_trigger.md`: each action requires explicit `MAIN_TERMINAL_*` directive; the plan is the authoritative source merged at PR #228; redesigning the blocker distribution unilaterally violates owner-scope perimeter.
- `feedback_optional_is_not_authorized.md`: the dispatch did not include "if the plan §4 contradicts itself, builder may swap blocker distribution" — silence is NOT greenlight.
- `feedback_orchestrator_decides_not_recommends.md`: builder recommends HOW; orchestrator decides WHAT.
- `feedback_quality_default_no_ask.md`: the slow-quality path is to surface the contradiction, route to orchestrator, and wait. The fast path (silently re-distribute) is exactly the anti-pattern this rule prohibits.
- `feedback_pilot_first_for_long_jobs.md`: Hybrid pilot-first 4-check pre-flight on first 5 was designed to catch issues like this BEFORE full emit. Builder is honoring that intent at the design-phase translation, before any code-level pilot fires.

## Recommended HOW (orchestrator decides which)

Three paths satisfy the 15/15 stop condition. Builder ranks them by deviation magnitude (smallest first):

### Path α — keep TT/T9 in sub-axis B; relax per-sub-axis to total-only (15/15 redistributed)

| Sub-axis | with-J-blocker | no-J-blocker | Hero-hand-class deviation |
|---|---|---|---|
| A (J-high flop, TJ) | 5 | 5 | None — matches plan |
| B (J-low flop with J-on-turn, TT/T9) | 0 | 10 | None — matches plan |
| C (J-medium flop / paired-J, TJ) | 10 | 0 | None for hero hand; deviates from plan §4 "5/5 within each sub-axis" |
| **Total** | **15** | **15** | Total 15/15 satisfied; per-sub-axis 5/5 violated for B and C |

**Strength:** preserves plan's hero-hand class for all 30 (TT/T9 in B, TJ in A and C). **Weakness:** sub-axis C concentrates all 10 J-blocker variants, which may interact with the J-paired flop (sub-axis C's last variant is `JcJh4s` — J-paired-flop with hero J-blocker creates double-J-removal effect on villain set-of-Js combos).

### Path β — switch sub-axis B hero hand to mixed TJ + TT/T9 (allows 5/5 within B)

| Sub-axis | with-J-blocker | no-J-blocker | Hero-hand-class deviation |
|---|---|---|---|
| A (J-high flop, TJ) | 5 | 5 | None — matches plan |
| B (J-low flop with J-on-turn) | 5 (hero TJ) | 5 (hero TT or T9) | Plan said "TT or T9"; this admits TJ for the 5 with-J-blocker variants |
| C (J-medium flop / paired-J, TJ) | 5 | 5 | None — matches plan |
| **Total** | **15** | **15** | Total 15/15 + per-sub-axis 5/5 both satisfied; hero-hand class deviates from plan in B |

**Strength:** preserves per-sub-axis 5/5 across all three. **Weakness:** sub-axis B becomes hand-class-mixed (5 hands with hero TJ → no-pair-with-2-overcards class on flop; 5 hands with hero TT/T9 → overpair / TP-T-kicker class on flop). Two different hero hand-class signals within sub-axis B blur the per-axis CHECK-consensus measurement at -C.

### Path γ — drop sub-axis B (15/0/15 split per plan §10 R1 fallback)

| Sub-axis | with-J-blocker | no-J-blocker | Total |
|---|---|---|---|
| A (J-high flop, TJ) | 7 or 8 | 7 or 8 | 15 |
| B | — | — | 0 (dropped) |
| C (J-medium flop / paired-J, TJ) | 7 or 8 | 7 or 8 | 15 |
| **Total** | **15** | **15** | 30 with no sub-axis B |

**Strength:** entirely sidesteps the contradiction; plan §10 R1 already pre-authored this fallback ("If orchestrator wants pure 'J-at-decision-time' test → drop sub-axis B → 15/0/15"). All hero hands are TJ; all flops are J-on-board at decision time → maximally pure verification signal. **Weakness:** drops the "future-J expectation" stress-test from the verification round; if orchestrator intends to keep that signal, this path forfeits it.

### Builder's default-if-no-override

**Path γ.** Reasoning:
1. `feedback_quality_default_no_ask.md` recommends the slow-quality interpretation. Path γ is the cleanest signal (zero hand-class mixing; zero blocker-distribution-redistribution).
2. Plan §10 R1 already pre-sanctioned this as a valid override path — orchestrator did not exercise it at PR #228 merge time, but the contradiction was unknown at that time.
3. Sub-axis B's "stress-test" framing was already conceded as noisy (plan §10 R1: "may add noise"); dropping it sharpens the verification signal.
4. -C labelling cost: 30 hands → 30 hands (no change in budget).
5. Verification-round graduation bar (≥27/30 CHECK) becomes 15+15 across two cleanly-aligned sub-axes instead of 10+10+10 with one mixed.

If orchestrator prefers to keep sub-axis B for breadth, **Path β** is second-best (preserves per-sub-axis 5/5 AND keeps sub-axis B's hand-class mostly TT/T9 with 5 TJ deviations).

**Path α** is third — it is the smallest hero-hand deviation from the plan but concentrates J-blocker variation in sub-axis C, which has its own confound (J-paired flop variant).

## What I am NOT doing right now

- NOT emitting any situations (factory script not started)
- NOT redesigning blocker distribution unilaterally
- NOT auto-fixing the plan
- NOT modifying any data/, scripts/, prompts/, BATCH2, river-rats-core/, or training-data file
- NOT creating a PR (no commits on this branch)

The branch `programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06` is empty; the working tree only contains this query comm.

## What unblocks me

Orchestrator authors `MAIN_TERMINAL_PR<N>_MW40B_RESOLUTION_*.md` (or amends the dispatch) selecting Path α / β / γ / a fourth option. Builder fires factory generation per the selected path on that comm's merge.

## References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR232_MERGE_AND_MW40B_DISPATCH_2026-05-06.md` (master `d584023`, PR #235)
- Plan (with §4 sub-axis B contradiction): `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228)
- Plan §10 R1 (sub-axis B fallback pre-sanctioned): `15/0/15` drop-sub-axis-B path
- Plan §10 R1 default-committed: `10/10/10` (this PR's HALT discovers that default cannot satisfy 5/5 per-sub-axis blocker variation)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_optional_is_not_authorized.md`, `feedback_queries_to_orchestrator.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`

**Status: Builder HALTED at design-translation phase before any factory emit. Awaiting orchestrator resolution. Recommended default: Path γ (drop sub-axis B → 15/0/15 split). Path β second; Path α third. Orchestrator decides.**
