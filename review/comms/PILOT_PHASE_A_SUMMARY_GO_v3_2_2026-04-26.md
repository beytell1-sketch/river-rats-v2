---
date: 2026-04-26
from: Pilot Orchestrator (general-purpose subagent under Pilot Orchestrator persona)
to: Main terminal (orchestrator) · Owner · QC stream
re: A.7 v3.2 retry summary — BOTH LANES PASS GATE; Phase B labeller default = Sonnet 4.6 per Path A revision decision tree row 1; cost $140-700 envelope preserved; A.7 GO; Phase B GO contingent on orchestrator confirmation
status: A.7 GO — A.4 v3.2 retry empirically validates v3.2 fix; both Sonnet 4.6 + Opus 4.7 pass standard + reversal gates; v3.1 → v3.2 fix-forward succeeded; Phase B labeller = Sonnet (per Path A revision default); awaiting orchestrator Phase B dispatch confirmation
phase_a_total_cost: ~$6 ($3.03 v3.1 + ~$3 v3.2 + ~$0 builder cycle); within $200 hard cap (3% utilization)
phase_a_wall_time: ~12 min v3.1 + ~30-60 min v3.2 builder cycle + ~5 min v3.2 retry = ~50-80 min total Phase A
supersedes: PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md (master b2de857) — A.7 HALT now resolved by v3.2 fix-forward
---

# Pilot Phase A.7 v3.2 Retry Summary — GO

## Headline

**A.4 v3.2 RETRY: BOTH LANES PASS GATE.** v3.2 protocol revision (Fix 1 + 2 + 3) empirically resolves all 3 v3.1 failure hands. Phase B labeller = Sonnet 4.6 per Path A revision decision tree row 1.

| Lane | Standard gate (≥23/33) | Reversal gate (100% / 10) | GATE | Cost | Wall-time |
|------|------------------------|----------------------------|------|------|-----------|
| Sonnet 4.6 (v3.2) | PASS (29/33; 87.9%) | **PASS** (10/10) | **PASSED ✓** | ~$0.40 | ~5 min |
| Opus 4.7 (v3.2) | PASS (32/33; 97.0%) | **PASS** (10/10) | **PASSED ✓** | ~$2.45 | ~5 min |

Per Path A revised decision tree row 1 (`MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` master `5cc7ba1`):

> "Sonnet PASS | Opus PASS → Ship **Sonnet** (cheaper; spec adequacy met; matches owner revert; cost in $140-$700 envelope)"

## Per-hand v3.1 → v3.2 comparison

| Hand | Expert | v3.1 Sonnet | v3.2 Sonnet | v3.1 Opus | v3.2 Opus | v3.2 fix triggered |
|------|--------|-------------|-------------|-----------|-----------|---------------------|
| d3688_BB_flop | CHECK | BET ✗ | **CHECK ✓** | BET ✗ | **CHECK ✓** | Rule 11 (paired-board / 2-tone OOP) — TPWK on 2-tone-diamond |
| d9556_BB_flop | CHECK | BET ✗ | **CHECK ✓** | BET ✗ | **CHECK ✓** | Rule 11 (paired-board) — fives full on paired board |
| MW-39 | CALL | RAISE ✗ | **CALL ✓** | RAISE ✗ | **CALL ✓** | KB §1.7 OVERRIDE — villain_air=0.05 < 0.20 threshold |
| MW-30 | CALL | CALL ✓ | CALL ✓ | CALL ✓ | CALL ✓ | (preserved) |
| MW-33 | RAISE | RAISE ✓ | RAISE ✓ | RAISE ✓ | RAISE ✓ | (preserved) |
| MW-50 | FOLD | FOLD ✓ | FOLD ✓ | FOLD ✓ | FOLD ✓ | (preserved) |
| d2410_CO_turn | BET | BET ✓ | BET ✓ | BET ✓ | BET ✓ | (preserved per Calibration Notes) |
| d8886_BB_flop | BET | BET ✓ | BET ✓ | BET ✓ | BET ✓ | (preserved) |
| d8963_HJ_turn | BET | BET ✓ | BET ✓ | BET ✓ | BET ✓ | (preserved) |
| d3178_CO_river | BET | BET ✓ | BET ✓ | BET ✓ | BET ✓ | Rule 11 BET exception (a) + river-checked-to override fire correctly |

**All 3 v3.1 failures fixed; no regressions on the 7 baseline-passing anchor hands.** Empirical validation that v3.2 Fix 1 + Fix 2 deliver as designed.

## Remaining failures (within standard-gate envelope; non-reversal)

**Sonnet (4 failures, all standard non-reversal — within 23/33 threshold):**
- MW-17 (CALL → FOLD; over-fold; AdKs hidden equity not credited)
- MW-41 (CALL → FOLD; over-fold; new failure not in v3.1 trace)
- MW-44 (CALL → FOLD; over-fold; same pattern as v3.1)
- MW-49 (BET → CHECK; new failure; will need investigation post-pilot)

**Opus (1 failure, standard non-reversal):**
- MW-17 (CALL → FOLD; same hidden-equity pattern as Sonnet)

Sonnet fold-bias pattern persists post-v3.2 (3 of 4 Sonnet failures are FOLD-instead-of-CALL on hidden-equity / draw-equity spots). Opus is much cleaner (1 failure only, also a FOLD-bias pattern). **Both lanes within the 23/33 standard-pass threshold; reversal-gate PASS.**

These are deferred for post-pilot v3.x diagnosis (not blocking Phase B). The 23/33 threshold accepts up to 10 standard-exam failures; Sonnet has 4 (within budget); Opus has 1 (well within).

## Cost telemetry

A.4 v3.1 (initial Option C): ~$3.03
A.4 v3.2 retry (this dispatch): ~$2.85 (Sonnet ~$0.40 + Opus ~$2.45; tokens slightly under v3.1 due to similar context)
v3.2 builder cycle: ~$0 (text edits, no model calls beyond reviewer)
v3.2 builder reviewer dispatch: ~$0.50 (Sonnet subagent, ~75K tokens × $3/$15 split)

**Total Phase A spend: ~$6.40 of $200 hard cap (3.2% utilization).** Massive remaining headroom for Phase B and beyond.

## Phase B projected cost (Sonnet labeller, decision tree row 1)

Per spec §"Cost tracking" with Sonnet labeller default:
- Phase B labelling (15 labellers × 100 hands × Sonnet): ~$75-$375
- Total pilot run revised: ~$140-$700 (within original spec envelope)

Phase B is cost-safe under Sonnet default.

## A.7 GO/NO-GO recommendation

**A.7 GO** per Path A revision decision tree row 1.

Phase B prerequisites (per spec v1.0.3 PRE-DISPATCH PREREQUISITES):
| # | Item | State |
|---|------|-------|
| 1 | Stage 6 holdout hash | GREEN (unchanged) |
| 2 | Pilot 100 disjoint from Stage 6 | GREEN (Build C v1.0.1) |
| 3 | Pilot 100 disjoint from v2.3 calibration | GREEN (Build C v1.0.1) |
| 4 | Protocol A v3.1 frozen | **SUPERSEDED by v3.2** at master `42cace2`; checksum capture needed for v3.2 |
| 5 | Protocol B v1.0.1 sealed + pilot artifact built | GREEN (Build A; F-S5 patched at `42cace2`) |
| 6 | Protocol C v1.0.1 sealed + pilot artifact built | GREEN (Build B) |
| 7 | Stage 5 retrain protocol v1.0.1 sealed | GREEN |
| 8 | Task 4.5 logic hardening sealed | GREEN |
| 9 | QC pre-pilot sweep clean | GREEN |
| 10 | All 33 pilot agents pass blind calibration | **READY** — A.4 v3.2 retry validates protocol; Phase B 15 labellers will dispatch on this validated protocol |
| 11 | Solver options match `feedback_solver_aligned_sizing.md` | GREEN |
| 12 | Pilot orchestrator session-launch cwd | GREEN (this session) |
| 13 | Owner explicit greenlight | GREEN (082336d + reaffirmations) |
| 14 | Anthropic API tier confirmed | DEFAULT Tier 1 (5-way × 3-batch parallelism per spec) |
| 15 | Model selection locked | GREEN — Sonnet 4.6 labeller per owner Opus revert + A.4 v3.2 winner-pick |
| 16 | `_villain_pos_raw` live-selection rule honored | GREEN (A.5 PASS at `b2de857`) |

Pre-dispatch row #4 needs a v3.2 checksum capture before Phase B (mechanical task, ~5 min).

## Action

**Owner:**
- Phase A v3.2 retry result: **PASS on both lanes**; v3.2 protocol fix-forward delivered as designed; Phase B labeller defaults to Sonnet per your earlier revert; total Phase A spend ~$6 of $200 cap; Phase B cost projection $75-$375 in original $700 envelope
- No action required unless you wish to override Sonnet→Opus or revisit cost envelope

**Orchestrator:**
1. Read A.7 v3.2 summary
2. Capture v3.2 prompt SHA256 for PRE-DISPATCH row #4 (~5 min)
3. Confirm Phase B dispatch (Sonnet labeller, 5-way × 3-batch protocol-grouped parallelism per spec §"Parallelism resolution")
4. Dispatch Phase B (Pilot Orchestrator executes; 1500 calls; ~90 min wall-time at 5-way × 3-batch)
5. Or HALT if any cross-stream concern surfaces

**Pilot Orchestrator (this session):**
1. A.7 v3.2 summary composed (this comm)
2. Standby for orchestrator Phase B dispatch confirmation
3. Pre-Phase-B housekeeping: optionally capture v3.2 SHA256, generate Phase B 100-hand corpus payload, set up labeller dispatch infrastructure

**QC stream:**
1. Layer 3 watch continues
2. A.4 v3.2 retry validation = high-value evidence for V-A4-1 vector (closes the v3.1 protocol-side gap)
3. May audit A.7 GO comm for synthesis adequacy

## References

- v3.2 protocol: `prompts/gto_labeller_v3.2.md` (master HEAD post `42cace2` merge)
- A.4 v3.1 HALT (superseded): `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (master `b2de857`)
- A.4 v3.2 calibration results: `review/pilot_run_2026-04-26/calibration_results_{sonnet,opus}_v3_2.json`
- A.4 v3.2 grading summary: `review/pilot_run_2026-04-26/phase_a4_v3_2_grading_summary.json`
- A.4 v3.2 blind agent payload: `review/pilot_run_2026-04-26/calibration_exam_for_agents_v3_2.json`
- Path A directive: `MAIN_TERMINAL_PATH_A_V32_PROTOCOL_REVISION_DIRECTIVE_2026-04-26.md` (master `24494eb`)
- Path A revision (Opus revert + decision tree): `MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` (master `5cc7ba1`)
- PR #47 merge ack + A.4 retry directive: `MAIN_TERMINAL_PR47_MERGE_ACK_A4_V32_RETRY_DIRECTIVE_2026-04-26.md` (master `58ceb3c`)
- v3.2 reviewer convergence: builder verdict `5972035` + QC PR #48 + gto-expert `REVIEWER_GTO_EXPERT_PR47_2026-04-26.md`

**Status: A.7 GO. v3.2 PROTOCOL EMPIRICALLY VALIDATED. PHASE B = SONNET LABELLER (Path A revision default). Awaiting orchestrator Phase B dispatch confirmation.**
