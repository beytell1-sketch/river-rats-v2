---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-ratified design memo §5 + §6.6)
to: LEAD-PROGRAMMER (architect-hat + gto-expert-hat)
re: Phase 2-D — 4-way reference set design (35 hands street-weighted per AMENDMENT 1; 3-bet/4-bet + closing-action variants per AMENDMENT 2; pilot-first 5+30 split per pilot-first standing rule)
status: DISPATCH — fire now (Phase 2-C cleanup merged at master dafa8f9; PR #401 + #403 PASS; owner-ratified 2-D scope per design memo §6.6 ≥28/35 weighted-total ship gate)
---

# Phase 2-D dispatch — 4-way reference set design

## Context

Per design memo (PR #388, owner-ratified all 9 owner-scope items including §6.6 4-way ship gate ≥28/35 street-weighted):
- Phase 2-D builds the **35-hand 4-way reference set** that gates the 4-way model retrain in 2-G
- Street-weighted distribution per AMENDMENT 1 (§3.X.2): **51% flop, 31% preflop, 11% turn, 6% river**
- Includes 4-way 3-bet pots + 4-bet pots + closing-action variants per AMENDMENT 2 (§3.Y.5)
- 4-way greenfield finding (§1.6 + §3.5): no existing v9-4way baseline; reference set is created fresh + must support the new gate calibration

Phase 2-C narrowed Phase 2 to surface 61 (2 winners). The reference set is independent of surface size — it's the per-spot decision evaluation that gates retrain accuracy. Reference set scope unchanged from design memo despite surface narrowing.

## Pilot-first split per standing rule

Per `feedback_pilot_first_for_long_jobs.md` STANDING RULE: long batches MUST split pilot+full with explicit gate.

- **Pilot scope**: 5 hands across the street distribution (e.g., 3 flop, 1 preflop, 1 turn; or architect chooses representative coverage)
- **Pilot gate**: pilot delivers 5 working spots WITH expert-attested actions + per-spot rationale + per-hand axes documented
- **Owner-arb adjudication** for any pilot ambiguous spots (analog to HU labelling pattern)
- **Full scope** (after pilot gate clear): 30 additional hands distributed per AMENDMENT 1 ratios = total 35 hands

## What Phase 2-D builds

### Task 1 — 4-way reference set spec design

Architect-hat + GTO-expert-hat produce a design document covering:
- 35-hand canonical 4-way reference set, distributed per AMENDMENT 1 51/31/11/6
- Each hand specified with: pre-flop action history, board, hero hole cards, opponent count (must be true-4-way at decision moment per §3.X.3), expected GTO action label, axis taxonomy (which decision class is being tested)
- Axes covered: 4-way 3-bet pots, 4-way 4-bet pots, closing-action variants (last-to-act), early-action variants (first-to-act), squeeze-risk spots, multiway-cooler spots, range-asymmetry spots
- Mapping to design memo MW-40/45/47 stay-wrong taxonomy where applicable (some 4-way decisions are HU-translated; some genuinely new)
- Per-hand rationale (gto-expert-hat reasoning chain; NOT rule-based per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`)

### Task 2 — 5-hand PILOT execution

- Architect picks 5 representative hands from the proposed 35
- For each pilot hand: full spec + expected GTO action + per-spot rationale (~200-400 words per hand)
- Pilot output: `data/4way_reference_pilot_5hand_2026-05-11.json` (or `.jsonl`) + per-hand rationale in `review/comms/4WAY_REFERENCE_PILOT_RATIONALE_2026-05-11.md`
- Pilot validates: street distribution achievable; spot types diverse; expert-attested actions consistent; no rule-based shortcuts

### Task 3 — Pilot gate evidence + STOP-condition gate

Builder writes `review/comms/BUILDER_REPORT_PHASE2D_PILOT_4WAY_REFERENCE_2026-05-11.md` covering:
- 5 hands delivered + per-hand axis coverage
- Per-hand rationale quality (gto-expert-hat reasoning evident; no template/rule-based shortcuts)
- Street distribution check (5 hands shouldn't deviate wildly from 51/31/11/6 ratios)
- Calibration evidence: 5 hands span the architect-proposed axes

**Pilot gate outcomes:**

| Outcome | Action |
|---------|--------|
| 5/5 hands clear (gto-expert reasoning + axis coverage + street distribution OK) | PROCEED to full 30-hand design |
| 3-4/5 hands clear (mixed signal) | REPORT to orchestrator; orchestrator triages owner-arb vs revise-pilot |
| <3/5 hands clear (broad fail) | HALT 2-D full; REPORT; likely owner-direction needed on axis taxonomy OR street distribution |

### Task 4 — Full 30-hand design (after pilot gate clear; SEPARATE PR)

Phase 2-D-FULL scope (next dispatch after pilot QC PASS + gate clear):
- 30 additional hands per AMENDMENT 1 distribution
- Full per-hand spec + rationale
- Owner-arb adjudication for any ambiguous spots
- Reference set artifact: `data/4way_reference_35hand_2026-05-11.json` (or `.jsonl`)

## What Phase 2-D (pilot) does NOT do

Per design memo §5 + §7 + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT touch `feature_extractor.py` (surface 61 frozen from 2-C)
- ❌ Does NOT touch `oracle_router.py` (2-H scope)
- ❌ Does NOT generate or label lookalike corpus (2-E scope; 2-E.0 labeller readiness gate first)
- ❌ Does NOT retrain production models (2-F / 2-G)
- ❌ Does NOT touch model artifacts
- ❌ Does NOT drain solver-verification queue (HOLD per owner-ratified §6.4)
- ❌ Does NOT design 4-way labeller brief (that's 2-E.0 scope; AMENDMENT 3 owner-ratified §6.8)

## STOP conditions (per CLAUDE.md §5)

- Architect cannot scope a 4-way reference set without spike work (e.g., needs to research existing PokerBench-multiway data first to find representative spots) → STOP / REPORT
- Street distribution targets can't be hit (e.g., 4-way 3-bet pots too rare in any available source) → REPORT
- Per-hand rationale slides into rule-based shortcuts (mirrors FL4 incident per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`) → STOP; require explicit anti-rule-based prompt
- TC-23 EXISTENCE: reference set artifacts must be git-tracked
- Wall-clock blows past ~10h (memo estimate 6-10h for 2-D + 40% buffer) → REPORT

## QC stream — what you audit (pre-merge milestone for 2-D pilot PR)

Per `feedback_qc_required_before_approval.md` + standing milestone-PR pattern:

1. **Diff scope** (TC-23): pilot artifact + rationale + report; NO river-rats-core/ edits; NO oracle_router; NO model files
2. **5-hand pilot verification**: each hand fully specified (pre-flop action history; board; hole cards; opponent count; expected action; rationale)
3. **Per-hand rationale quality**: gto-expert-hat reasoning chain evident; NOT rule-based / threshold-based / template
4. **Axis coverage**: 5 hands span the proposed axes (3-bet, 4-bet, closing-action, etc.); no axis monoculture
5. **Street distribution**: 5 hands per architect's chosen split (not necessarily 51/31/11/6 at 5-hand scale; but architect-defended split)
6. **True 4-way attestation**: each hand is actually 4-way at decision moment (not 4-way preflop pot that's 3-way by flop)
7. **No spec drift**: 5 hands match dispatch spec (not 4, not 6; not different scope)
8. **TC-X-DISPATCH-COMPLIANCE**: pilot-first standing rule applied; full 30-hand work NOT started

QC routing: standalone per `feedback_qc_routing_when_standalone_active.md`. Output:
- `~/river-rats-qc/findings/2026-05-11-pr<N>-phase2d-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2D_PILOT_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- Builder Phase 2-D pilot PR → QC trigger when pushed
- On QC PASS + pilot gate cleared (5/5 hands) → orchestrator merges + dispatches 2-D-FULL (30-hand design)
- On QC PASS + pilot gate partial (3-4/5) → orchestrator triages; may surface to owner
- On QC PASS + pilot gate fail (<3/5) → HALT 2-D-FULL; REPORT
- On QC SHOULD_FIX-substantive → amend + re-fire builder
- On QC BLOCKER → hold + redo
- STOP condition → REPORT; orchestrator triages

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `dafa8f9` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-C cleanup (preceding): master `ff64928` (PR #401) + QC PASS `dafa8f9` (PR #403)
- Phase 2-A design memo: master `0e5f91f` (PR #388) + QC PASS `a221a9b` (PR #391)
- Design memo §5 row 2-D: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` line 552
- Design memo §3.X.2 street distribution (AMENDMENT 1): lines 260-273
- Design memo §3.Y.5 4-way reference set (AMENDMENT 2): lines 363-372
- Design memo §6.6 owner-ratified ship gate: lines 622-631
- HU reference set analog (HU2/HU6.5 30-hand set): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` + builder reports from Phase 1.5-D.1
- Phase 2 progression:
  - 2-A design memo + 9 owner-scope items: master `0e5f91f`
  - 2-B PILOT v1 (1/6): master `fa0ea24`
  - 2-B RE-PILOT (2/4): master `59978c5` — tpmk_kicker_rank breakthrough 9.18%
  - 2-C cleanup (surface 61): master `ff64928`
- Memory: `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_bucket_first_labelling.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_solver_aligned_sizing.md`

**Status: Phase 2-D PILOT dispatch — 5-hand 4-way reference pilot per pilot-first standing rule. Architect designs 35-hand spec (street-weighted 51/31/11/6 per AMENDMENT 1; 3-bet/4-bet + closing-action variants per AMENDMENT 2); executes 5-hand pilot subset with expert-attested rationales. Gate evidence: 5/5 PROCEED, 3-4/5 triage, <3/5 HALT. NO 2-D-FULL / 2-E / 2-F / 2-G / 2-H scope. Architect estimate ~3-5h for 5-hand pilot (subset of memo's 6-10h full estimate).**
