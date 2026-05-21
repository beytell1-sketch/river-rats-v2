# Orchestrator Ratification — A0 Schema Fix Blueprint v2

**Blueprint reviewed:** `review/comms/DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v2_2026-05-21.md` (765 lines)
**Supersedes:** `DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v1_2026-05-17.md` (PR #459) — v1 had 2 BLOCKERs (F-1, F-2) + 1 promoted-to-BLOCKER (F-6) per QC pre-merge audit (`river-rats-qc/findings/2026-05-21-pr459-a0-blueprint-prereview.md`)
**Date:** 2026-05-21
**Verdict:** **RATIFIED.** v2 fixes all 3 BLOCKERs cleanly. No new override required.

---

## QC blockers addressed

| Finding | Fix in v2 | Verification |
|---|---|---|
| **F-1** all-in handling | §3.2 STEP 2.5 (NEW) — explicit `if v == stack_size_bb: status=clean_all_in` BEFORE legality/tie-break | Real spot 4WF-MULTIWAY-171 (L4 vote v=100) now resolves to raise_to_bb=100 instead of 16 |
| **F-2** preflop BB-defend min-raise | §3.2 STEP 1 (REVISED) — `min_raise_to_bb = 2 × previous_full_bet` where `previous_full_bet = to_call_bb + hero_already_committed_bb` | BB defend: 1.5 + 1.0 = 2.5; min=5.0. Postflop unchanged (hero_already_committed_bb=0) |
| **F-6** consensus_v2 modal-sizing | §3.6 NEW — action-consensus first; sizing-consensus over labellers who voted the action; weighted modal (clean=1.0, ambiguous_resolved=0.7); tie-break prefers smaller (conservative) | New tests 13, 14, 15 cover edge cases |

## Bonus fixes (architect inline-addressed)

- F-3 → §7.5 prediction table now includes v=66 row
- F-7 → Example C-2 demonstrates real tie-break path (v=22 at pot=45)

## Architect-committed without prior review (owner reserves override)

Per architect's report, 2 design commitments were made without prior owner/orchestrator review. Orchestrator accepts both; owner reserves override:

### Commitment 1: min-raise formula = `2 × previous_full_bet`

Architect's task prompt contained an arithmetic contradiction (I wrote "raise_increment = open_size - 1.0" implying min=4.0bb, but F-2 evidence asserted 5.0bb). Architect resolved by committing to `2 × previous_full_bet` → 5.0bb for BB-defend, which matches both the test-case value and the F-2 evidence statement.

**Orchestrator analysis:**
- The architect-committed formula represents the "live casino / double-the-bet" NL convention
- The alternative (4.0bb) represents the "online NL / raise-increment-matching" convention
- The poker engine (`river-rats-core/poker_game.py`) doesn't enforce either; it's permissive
- The normalizer's purpose is to DISAMBIGUATE bb-vs-pct interpretations of legacy labels; stricter min-raise (5.0) over-rejects borderline cases, sending them to owner-arb. Lenient (4.0) under-rejects, accepting potentially-confused labels as "clean"
- Per `feedback_quality_default_no_ask.md` slow/quality path: over-rejecting (more owner-arb spots) is the safer error direction

**Accept:** formula stays at `2 × previous_full_bet` per architect.

### Commitment 2: §3.6 sizing-consensus tie-break thresholds

- Weight 1.0 for clean status, 0.7 for ambiguous_resolved
- ≥3 malformed labellers → sizing-consensus failure (owner-arb)
- Spread >50% of max → flagged high-disagreement

**Orchestrator analysis:** numeric thresholds picked without prior review. Architect's choices are defensible:
- 0.7 weight discounts ambiguous_resolved (where labeller intent wasn't unambiguous) by 30% relative to clean
- 50% spread is a reasonable "this is too divergent to consensus" threshold
- ≥3-of-5 malformed threshold matches the 3-2 split threshold used elsewhere

**Accept:** thresholds stay per architect. Future tuning possible if A0.2 backfill shows excessive owner-arb routing.

## Architect-deferred items (acceptable)

| Finding | Severity | Deferral reason | Where addressed |
|---|---|---|---|
| F-4 | SHOULD_FIX | low-impact documentation polish | future revision |
| F-5 | SHOULD_FIX | wording issue, not algorithmic | future revision |
| F-8 | SHOULD_FIX | absorbed into PR-body note (architect) | PR #461 description |
| F-9 (partial) | SHOULD_FIX | 3 of 4 sub-items absorbed into tests 13-15 | covered |
| F-10 | SHOULD_FIX | folded into test 12 acceptance criterion | covered |
| N-1, N-2, N-3 | NIT | defer | future revision |

Orchestrator accepts the deferrals — none affect correctness.

---

## Sequencing override carries over from v1 ratification

Per the v1 ratification (`RATIFICATION_A0_BLUEPRINT_2026-05-17.md`), the brief patch moves from PR A0.1 to PR A0.3 final step. **This override applies unchanged in v2.**

---

## What changes for Builder's next revision of PR #460

The v2 blueprint authorizes Builder to update `river-rats-core/sizing_schema_normalizer.py` with:

1. **STEP 2.5 (NEW)** — all-in detection branch
2. **STEP 1 (REVISED)** — new `previous_full_bet` derivation; new `hero_already_committed_bb` helper (BB=1.0, SB=0.5, else=0)
3. **§3.6 (NEW)** — `compute_consensus_v2(spot_labels) -> ConsensusV2Record` function
4. **3 new tests** (13, 14, 15) — all-in case, BB-defend min-raise (positive + negative sub-cases), consensus-v2 modal-sizing
5. **Wire `validate_v2_label`** (per code-QC SHOULD_FIX) — currently defined but never called/tested in PR #460

Builder pushes amended commits to existing branch `builder/a0.1-normalizer-2026-05-21`. PR #460 stays open; force-push not required (additive commits acceptable since no one else is on that branch).

## What this directive does NOT authorize

- Modifying the existing 12 tests in PR #460 (only ADDING tests 13, 14, 15; existing tests stay green)
- Touching `data/4way_labeller_brief.md` (brief patch still moves to A0.3 final per v1 override)
- Touching corpus data (A0.2 separate PR)
- Changing the v2 blueprint after ratification — if architect wants further changes, they author v3

---

## Ratification checklist (architect's §7 v2) — orchestrator pass

- [x] F-1 BLOCKER fixed (STEP 2.5 verified against spot 4WF-MULTIWAY-171)
- [x] F-2 BLOCKER fixed (formula verified against to_call=1.5 BB-defend evidence + 19 corpus spots)
- [x] F-6 BLOCKER fixed (§3.6 consensus-v2 algorithm with all required clauses)
- [x] Architect committed to single design (no menus); 2 concerns flagged for owner override
- [x] Worked Example E (all-in v=100 case) and Example D (BB-defend min-raise case) included
- [x] Test count grows from 12 → 15; existing 12 stay unchanged
- [x] Sequencing override from v1 preserved (brief patch → A0.3 final)
- [x] §3.5 test names match the algorithm structure
- [x] Memory rules cited (orchestrator_decides_not_recommends, solver_aligned_sizing, terminology_raise_vs_bet, etc.)

## Sign-off

- Architect: blueprint v2 commits to single design (verified); 2 architect-committed-without-review items flagged for owner reserve
- Orchestrator: RATIFIED with no override required; concerns documented for owner visibility
- Owner: notified; can override commitment 1 (min-raise formula) or commitment 2 (tie-break thresholds) if disagrees with architect's calls

---

## Dispatch authorization

Upon merging this PR, orchestrator dispatches Builder to revise PR #460 per the v2 algorithm. QC will then re-audit the revised code.
