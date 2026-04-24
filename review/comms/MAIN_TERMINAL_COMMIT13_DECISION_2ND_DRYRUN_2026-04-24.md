---
date: 2026-04-24
from: Main terminal (orchestrator)
to: Builder · Owner
re: Commit 13.1 mid-lift gate — decision: 2nd dry-run batch (option C), NOT (A) direct-to-full-lift
status: DIRECTIVE — builder authors 2nd 5-entry dry-run batch before ~130-entry remaining lift; quality default
---

# Commit 13 Mid-Lift Gate — 2nd Dry-Run Batch First

Owner standing instruction (2026-04-24): **slow and steady, best
quality, never rushing.** When the quality option is clear, execute
it without asking.

I had the decision framing backwards in my prior relay to owner. I
recommended "(A) GO to full ~135-entry authoring now" because signal
from the first 5-entry dry-run looked strong. That was the rushing
option. Owner's quality default means: **more verification before
scaling, not less.**

Revised decision: **(C) 2nd dry-run batch covering the deferred shape
categories.** Commit 13.2 authors 5 more entries, GTO-reviewed, spans
the categories the first dry-run deferred. Catches systematic authoring
errors cheaper in a small batch than mid-way through a 135-entry lift.

## Why (C), not (A)

First dry-run (commit 13, 79c618e) covered:
- HU delayed-probe (FB-17)
- HU donk-x-through + river-bet (FB-23)
- MW per-villain chain (MW-15, MW-30)
- MW baseline no-chain (MW-11)

Total: 4 of 8 MUST #49 shape categories.

Deferred to full lift (if (A) had been chosen):
- T_J02 / T_B05 shape variants (synthetic, not in reference/calibration)
- Folded-villain sentinel fixture (HU + MW)
- Synthetic over-narrow (MUST #15 overflow path)
- Mass-floor truncation (MUST #28)
- Multiway all-live (both villains in hand; per-villain rendering)

Risk of skipping a 2nd dry-run:
- Folded-villain + over-narrow + mass-floor are SENTINEL cases. First
  dry-run's 5 entries don't exercise the sentinel-state authoring
  pattern. Systematic errors in sentinel encoding would surface
  mid-lift, costing rework on ~20-30 entries instead of ~3-5.
- Multiway all-live is structurally distinct from the per-villain-with-
  one-folded case (MW-15/MW-30). Same-pattern authoring risk.
- T_J02/T_B05 shapes aren't in the reference set — synthetic-only
  entries test a different authoring workflow (no ref-ID, no MW-*
  or FB-* prefix). Surface any process drift in a small batch.

A 2nd dry-run batch catches all of this for ~1-2 days of authoring
cost. Saves 3-5 days of rework if systematic error surfaces mid-lift.
Quality default: cheap catch now > expensive catch later.

## Commit 13.2 scope

**5 new entries covering the deferred shape categories:**

1. **F3_HU_folded** (synthetic, HU folded villain sentinel) —
   `_villain_folded=True` on a prior-street hand; no real ref-ID

2. **F5_HU_overflow** (synthetic, HU over-narrow sentinel) —
   `_villain_chain_overflowed=True` via MUST #15 pathway (different
   from C5.1's F2 which used MUST #28 floor-truncation path)

3. **F6_MW_all_live** — multiway 3-way hand, both villains still
   in hand, per-villain rendering exercised (parallel to MW-15 but
   where neither villain folds)

4. **T_J02_synthetic** — matches T_J02's BET-CHECK-CALL-BET 4-class
   chain shape; synthetic (not real ref-ID); exercises non-reference
   authoring workflow

5. **T_B05_synthetic** — matches T_B05's BET-RAISE-CALL donk-pot-
   control shape; synthetic; same workflow test

Each entry authored + structural validator (MUST #35) + solver-verify
stub (MUST #54/#66) + GTO reviewer per-batch pass.

## Expected outputs

After commit 13.2 push:
- Sidecar sizes: _REFERENCE_ACTION_HISTORY 5+5=10 entries (unchanged
  for synthetic entries; they go into a SYNTHETIC_ACTION_HISTORY dict
  OR same sidecars with SYN-* keys — builder chooses per authoring
  pattern); _CALIBRATION_ACTION_HISTORY still 3 (MW-* only; synthetics
  don't mirror)
- Validator: clean exit on all 10 total entries + synthetics
- Solver-verify: stratified sample now 10 → ≥1 per all 8 MUST #49
  buckets guaranteed
- Test coverage: test_commit13_sidecar_dryrun.py extended with 5
  new-entry-specific asserts
- GTO reviewer pass on the 5 new entries before orchestrator
  greenlights the remaining ~130 entries

## Then (C.2) full lift to ~130 remaining entries

After commit 13.2 GTO-approved: builder authors the remaining ~130
(FB-01..16, FB-18..22, FB-24..40 minus FB-17/23; MW-12..14,
MW-16..29, MW-31..50 minus MW-11/15/30). Per-batch GTO review
continues. Orchestrator final gate at completion.

Total Phase 2 authoring cost: 3-4 days + 1-2 days for 2nd dry-run +
GTO reviews = ~5-6 days with quality discipline. Worth it.

## Why "don't ask" applies here

This is NOT one of the owner-only gate types (resource commissioning,
project identity, scope shift). Owner explicitly delegated this class
of decision to orchestrator under the "quality default" instruction:

> "YOU REVIEW EVERYTHING AND ARE BEST EQUIPPED TO DECIDE BEST APPROACH.
> DON'T ASK ME AGAIN IN FUTURE IF THE QUALITY OPTION IS CLEAR."

Memory rule at `feedback_quality_default_no_ask.md` strengthened
accordingly.

The quality option is clear: 2nd dry-run before full lift. Orchestrator
executes. Owner briefed, not asked.

## Action

Builder:
1. Author the 5 new entries above for commit 13.2
2. Run MUST #35 validator + MUST #54/#66 solver-verify + 8-test suite
3. Dispatch GTO reviewer on the 5 new entries (per-batch pattern from
   v2.2 amendment §5)
4. Push commit 13.2
5. Ping orchestrator with GTO verdict

If GTO approves 13.2: orchestrator greenlights commit 13.3 (full
~130-entry lift) with per-batch GTO reviews continuing.

If GTO surfaces issues: fix-forward per standard discipline.

## Reference

- `feedback_quality_default_no_ask.md` (strengthened 2026-04-24)
- Commit 13 dry-run at 79c618e
- v2.2 amendment §5 (Path (c) Phase 2 mid-lift owner gate)
- ALL-CLEAR directive at d290af0
