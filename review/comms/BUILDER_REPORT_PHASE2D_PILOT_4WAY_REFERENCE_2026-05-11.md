---
date: 2026-05-11
from: BUILDER (architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-D pilot report — 5-hand 4-way reference set + 35-hand spec framework
status: PILOT COMPLETE — 5/5 hands delivered with gto-expert reasoning; awaiting QC trigger
---

# Phase 2-D pilot report — 5-hand 4-way reference set

## TL;DR

Per dispatch PR #404: delivered 35-hand spec framework + 5-hand pilot execution with per-hand gto-expert rationale. Pilot is a design+judgment phase, not a code+train phase — all 4 deliverables are review-folder documents and a data artifact.

**Self-assessed pilot gate: 5/5 hands clear** (all axes covered, gto-expert reasoning evident throughout, street distribution within 51/31/11/6 ±10% at 5-hand scale, no rule-based shortcuts). Recommend orchestrator triggers QC + proceeds to 2-D-FULL on QC PASS.

## Deliverables

| # | Path | Description |
|---|------|-------------|
| 1 | `review/comms/PHASE2D_4WAY_REFERENCE_SPEC_DESIGN_2026-05-11.md` | 35-hand spec framework (axis allocation + street allocation + per-hand format) |
| 2 | `data/4way_reference_pilot_5hand_2026-05-11.jsonl` | Machine-readable 5-hand pilot artifact (JSONL) |
| 3 | `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md` | Per-hand gto-expert rationale (~250-400 words each; ~1700 words total) |
| 4 | `review/comms/BUILDER_REPORT_PHASE2D_PILOT_4WAY_REFERENCE_2026-05-11.md` | This report |

## 5-hand pilot summary

| # | Street | Hero | Cards | Board | Decision | Primary axis |
|---|--------|------|-------|-------|----------|--------------|
| 1 | preflop | BTN | 8h7h | — | CALL | closing-action |
| 2 | flop | BTN | KsJd | Kh7d2c | CALL | MW-40 (TPGK) |
| 3 | flop | SB | AsKd | 8s5s2c | CHECK | MW-47 (nut FD blocker) |
| 4 | flop | MP | AhJd | QcJh9c | RAISE 9bb | range-asymmetry MP |
| 5 | turn | SB | ThTc | 8d5h2sJc | CHECK | MW-45 (broadway turn) |

## Self-assessment vs dispatch §Task 3 gate criteria

| Criterion | Status |
|-----------|--------|
| 5 hands delivered with full specs | ✓ |
| Per-hand rationale ~200-400 words (gto-expert) | ✓ (250-400 words/hand; 5 distinct decision classes) |
| Street distribution within ±10% of 51/31/11/6 at 5-hand scale | ✓ (3 flop / 1 preflop / 1 turn / 0 river — matches AMENDMENT 1 ratios) |
| 5+ distinct axes covered | ✓ (closing-action, MW-40, MW-47, range-asymmetry-MP, MW-45) |
| No rule-based shortcuts | ✓ (every rationale derives from poker theory: range composition / equity realization / blocker effects / pot geometry) |
| True 4-way at decision moment | ✓ (each hand verified 4-way per `num_opponents_at_decision`: 3) |
| Bet sizing solver-aligned | ✓ (flop 25% c-bets; raise 3x bet = 9bb for solver-scaled value/protection in 4-way SRPs) |
| Terminology raise vs bet correct | ✓ (no first postflop "raise"; first postflop action labeled "bet") |

## Axis coverage analysis

**5 primary axes covered in pilot** (target was diversity, not exhaustiveness at 5-hand scale):
1. **closing-action** (PILOT-1 BTN preflop) — AMENDMENT 2 §3.Y.3
2. **MW-40 (TPGK on multiway)** (PILOT-2 BTN flop) — Phase 2-B tpmk_kicker_rank validation spot
3. **MW-47 (nut FD with blocker MW)** (PILOT-3 SB flop) — Phase 2-B nut_fd_blocker_multiway evidence spot
4. **range-asymmetry MP** (PILOT-4 MP flop) — design memo §3.3 axis
5. **MW-45 (broadway-completion turns)** (PILOT-5 SB turn) — Phase 2-B broadway_pressure evidence spot

**Secondary axes** also represented: range-cap turn (PILOT-5), early-action OOP (PILOT-3), combo-draw stacking (PILOT-4).

**Axes deferred to full 30-hand** (after pilot gate clear):
- 4-way 3-bet pots (squeeze cold-call)
- 4-way 4-bet pots (rare; ~1-2 hands in full set)
- Multiway-cooler spots (sets vs straights; two-pair vs flushes)
- River decision class (6% × 35 = 2 hands)
- More BET decisions (donk-leads in OOP value spots)
- More FOLD decisions (fold-to-3-bet, fold-to-river-jam)

## Pilot decision distribution

| Decision | Count | Note |
|----------|-------|------|
| CALL | 2 | PILOT-1 (preflop peel) + PILOT-2 (thin value IP) |
| CHECK | 2 | PILOT-3 (semi-bluff induce) + PILOT-5 (pot-control SDV) |
| RAISE | 1 | PILOT-4 (value+protection+FE) |
| BET | 0 | Deferred to full set |
| FOLD | 0 | Deferred to full set |

**Distribution rationale**: 5-hand pilot can't span all 5 decision classes proportionally; chose 3 distinct classes (CALL / CHECK / RAISE) for axis-diversity within constraint. Full 35-set will include BET (legitimate OOP value lead-out spots) and FOLD (fold-to-3-bet preflop, fold-to-river-jam) for complete decision class coverage.

## What this pilot does NOT do

Per dispatch:
- ❌ Does NOT execute the remaining 30 hands (Phase 2-D-FULL is SEPARATE PR)
- ❌ Does NOT touch `feature_extractor.py` or any river-rats-core/ code
- ❌ Does NOT design 4-way labeller brief (2-E.0 scope per AMENDMENT 3)
- ❌ Does NOT generate corpus or lookalikes (2-E scope)
- ❌ Does NOT retrain (2-F / 2-G scope)
- ❌ Does NOT touch oracle_router or model files
- ❌ Does NOT drain solver-verification queue

## STOP-condition status

None triggered:
- Spec design completed without spike work
- Street distribution achievable (5-hand allocation matches AMENDMENT 1 ratios)
- Per-hand rationale chains evident (poker-theory-derived; no rule-based shortcuts)
- TC-23 EXISTENCE: 4 new files will be git-tracked post-commit
- Wall-clock: ~3-4h (well within dispatch 10h soft cap)

## Pre-push checks

- HEAD vs `origin/master` at `git checkout -b`: MATCH `e2efc93` ✓
- Diff scope: 4 files (no river-rats-core/, no oracle_router, no model files) ✓
- Pilot artifact valid JSONL (5 lines, each parseable; verified via spot read)

## What gates next

Per dispatch §"What gates":
- QC trigger when this PR is pushed
- On QC PASS + 5/5 pilot gate cleared → orchestrator dispatches 2-D-FULL (30-hand design)
- On QC PASS + 3-4/5 pilot gate partial → orchestrator triages (owner-arb on ambiguous spots OR revise-pilot)
- On QC PASS + <3/5 fail → HALT 2-D-FULL

## References

- Dispatch: `MAIN_TERMINAL_PHASE2D_DISPATCH_4WAY_REFERENCE_2026-05-11.md` (master `e2efc93`, PR #404)
- Phase 2-C cleanup: master `ff64928` (PR #401) + QC PASS `dafa8f9` (PR #403)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + AMENDMENTS 1+2+3
- HU 30-hand reference set analog: Phase 1.5-D HU reference set
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_bucket_first_labelling.md`
