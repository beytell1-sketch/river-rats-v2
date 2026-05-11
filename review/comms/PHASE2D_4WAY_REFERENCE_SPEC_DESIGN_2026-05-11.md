---
date: 2026-05-11
from: BUILDER (architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-D — 35-hand 4-way reference set spec design (framework + axis allocation)
status: PILOT-stage design framework — 5 hands fully specified in pilot artifact; 30 additional reserved for Phase 2-D-FULL after pilot gate clears
---

# Phase 2-D — 35-hand 4-way reference set spec design

## Purpose

Per design memo §6.6 + AMENDMENT 1 (street distribution) + AMENDMENT 2 (re-raise + closing-action variants): build the 4-way reference set that gates the 4-way model retrain in 2-G. Ship gate: **≥28/35 weighted-total**. Analog to HU 30-hand reference set used at v8-HU 88.1% ceiling + vNext-HU-59 28/30 ship gate.

## Street allocation (AMENDMENT 1, §3.X.2)

| Street | Ratio | 35-hand count | 5-hand pilot count |
|--------|-------|---------------|---------------------|
| Flop | 51% | 18 hands | 3 hands |
| Preflop | 31% | 11 hands | 1 hand |
| Turn | 11% | 4 hands | 1 hand |
| River | 6% | 2 hands | 0 hands (deferred to full set) |

**Rationale**: 51% flop reflects multiway-play reality — most 4-way decisions are flop bet-or-check spots; preflop is heavily ranges-driven (open + cold-call decisions); turn/river decisions become rare in 4-way because pots typically narrow by then.

## Axis allocation (35-hand canonical set)

Per design memo §3.3 + §3.Y.5 + stay-wrong taxonomy:

| Axis | Hand allocation | Notes |
|------|-----------------|-------|
| 4-way single-raised pots (SRPs) | 20-22 hands | Most common scenario; baseline 4-way play |
| 4-way 3-bet cold-called pots | 5-7 hands | Squeeze-decision + range-asymmetry signal |
| 4-way 4-bet pots | 1-2 hands | Rare in equilibrium; mostly preflop AA/KK spots |
| Closing-action variants (BTN IP) | 6-8 hands (subset) | AMENDMENT 2 §3.Y.3 axis |
| Early-action variants (SB/BB/EP OOP) | 8-10 hands (subset) | Pressure-asymmetry axis |
| MW-40 axis (TPMK on multiway) | 3-4 hands | Phase 2-B pilot evidence; tpmk_kicker_rank validated |
| MW-45 axis (broadway-completion turns) | 2-3 hands | Phase 2-B pilot evidence; broadway absorbed by baseline |
| MW-47 axis (nut FD with blocker MW) | 2-3 hands | Phase 2-B pilot evidence; signal real but narrow |
| Range-asymmetry MP/CO | 3-4 hands | MP range-capped relative to BTN |
| Multiway-cooler spots (sets/two-pair vs straights/flushes) | 2-3 hands | Stress-test action discipline |

Note: axes overlap (a closing-action hand can also be MW-40); the allocation is approximate, with each hand mapped to its PRIMARY + SECONDARY axes.

## Per-hand spec format

Each hand specifies:
```json
{
  "hand_id": "4W-PILOT-N",
  "stack_size_bb": 100,
  "preflop_action": "<comma-separated action log>",
  "board": "<2-char per card; e.g. 'Kh7d2c'>",
  "hero_position": "<UTG|HJ|MP|CO|BTN|SB|BB>",
  "hero_cards": "<4-char; e.g. 'KhJs'>",
  "num_opponents_at_decision": 3,
  "street": "<preflop|flop|turn|river>",
  "facing_bet": <0|1>,
  "to_call_bb": <float>,
  "pot_bb": <float>,
  "expected_action": "<FOLD|CHECK|CALL|BET|RAISE>",
  "expected_size_bb": <float|null>,
  "primary_axis": "<axis label>",
  "secondary_axis": "<axis label|null>",
  "rationale_summary": "<1-2 sentence summary; full reasoning in rationale doc>"
}
```

## Bet sizing alignment (per `feedback_solver_aligned_sizing.md`)

Standard oracle sizing assumed:
- **Flop**: 25% pot small-cbet, 66% pot polarized
- **Turn**: 33% pot small, 75% pot polarized
- **River**: 33% / 75% / 150% pot (over-bet for polar value)

Reference set hands use solver-aligned sizes; deviations are owner-arb candidates.

## Terminology (per `feedback_terminology_raise_vs_bet.md`)

- **Open** = preflop opener
- **Bet** = first postflop bet (action into uncontested street)
- **Raise** = raise of an existing bet

## Pilot subset (5 hands; subset of full 35)

The 5-hand pilot delivers the FOLLOWING coverage across the 4 streets + 5 axes:

| # | Street | Hero pos | Axis primary | Axis secondary | Spot type |
|---|--------|----------|--------------|----------------|-----------|
| 1 | preflop | BTN | closing-action | range-asymmetry | 4-way SRP cold-call decision |
| 2 | flop | BTN | MW-40 (TPGK) | closing-action | 4-way SRP IP facing small bet |
| 3 | flop | SB | MW-47 (nut FD blocker) | early-action | 4-way SRP OOP first decision |
| 4 | flop | MP | range-asymmetry MP | combo-draw | 4-way SRP middle facing bet |
| 5 | turn | SB | MW-45 (broadway turn) | range-cap turn | 4-way SRP OOP after flop checkdown |

This gives:
- **3 flop / 1 preflop / 1 turn / 0 river** — matches AMENDMENT 1 ratios at 5-hand scale (51% × 5 ≈ 2.55 → 3 flop; 31% × 5 ≈ 1.55 → 1 preflop; 11% × 5 ≈ 0.55 → 1 turn; 6% × 5 ≈ 0.30 → 0 river)
- **5 distinct axes** covered (closing-action, MW-40, MW-47, range-asymmetry, MW-45)
- **5 distinct hero positions** (BTN ×2, SB ×2, MP ×1) — diversity across position spectrum
- **4-way at decision moment** verified for each hand

## Anti-rule-based discipline (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + FL4 lessons)

Per-hand rationale chains gto-expert-hat reasoning:
- Hero range composition at decision moment
- Villain range composition (decomposed by position)
- Equity realization adjustment for multiway count (≈0.75 for 4-way per pilot v1)
- Pot geometry (SPR + facing-bet pressure + closing-action effect)
- Specific blocker/unblocker effects
- Decision class (value bet / protection bet / bluff / check-decoy / call vs raise frequency)

**Each rationale is per-spot reasoning**, NOT thresholds applied to feature values. Outputs are derived from poker logic, not "if hand_rank > X then RAISE".

## What this design does NOT do (per dispatch)

- ❌ Does NOT execute the remaining 30 hands (Phase 2-D-FULL SEPARATE PR)
- ❌ Does NOT touch river-rats-core/ code (surface 61 frozen from Phase 2-C)
- ❌ Does NOT design 4-way labeller brief (2-E.0 scope per AMENDMENT 3)
- ❌ Does NOT generate corpus (2-E scope)
- ❌ Does NOT retrain (2-F / 2-G scope)
- ❌ Does NOT touch oracle_router (2-H scope)

## Pilot gate criteria

Per dispatch §Task 3:
- **5/5 PROCEED**: gto-expert reasoning evident in all 5 rationales + axis coverage achieved + street distribution within 51/31/11/6 ±10% + no rule-based shortcuts
- **3-4/5 mixed**: orchestrator triages — owner-arb on ambiguous spots OR revise-pilot
- **<3/5 fail**: HALT 2-D-FULL; report; likely owner-direction on axis taxonomy or distribution

## References

- Dispatch: `MAIN_TERMINAL_PHASE2D_DISPATCH_4WAY_REFERENCE_2026-05-11.md` (master e2efc93, PR #404)
- Design memo: `PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` §3.X.2 + §3.Y.5 + §6.6
- AMENDMENT 1 (street distribution): PR #386 (master cee0705)
- AMENDMENT 2 (re-raise + closing-action variants): PR #387 (master 596bb89)
- HU 30-hand reference set analog: Phase 1.5-D HU reference at `design/hu_reference_set/hu_30_hand_reference.jsonl`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`
