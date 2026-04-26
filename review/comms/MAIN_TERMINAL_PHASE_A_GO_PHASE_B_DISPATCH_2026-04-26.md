---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Pilot Orchestrator · Owner (briefed) · QC stream
re: A.7 v3.2 GO acknowledged; PRE-DISPATCH #4 closed via v3.2 SHA256 capture; Phase B GO confirmed with Sonnet 4.6 labeller per Path A revised decision tree row 1; dispatching Phase B mass labelling subagent
status: PHASE A GO ✓ + PHASE B DISPATCH AUTHORIZED — 15 labellers × Sonnet × 100 hands × 3 protocols (A/B/C) = 1500 raw labels; cost target $75-$375 in $700 envelope; wall-time target ~90 min at 5-way × 3-batch
---

# Phase A GO + Phase B Dispatch

## A.7 v3.2 retry result acknowledged

Per `PILOT_PHASE_A_SUMMARY_GO_v3_2_2026-04-26.md` at master `903c5c9`:

| Lane | Standard gate (≥23/33) | Reversal gate (10/10) | GATE | Cost | Wall-time |
|------|------------------------|------------------------|------|------|-----------|
| Sonnet 4.6 (v3.2) | PASS (29/33; 87.9%) | **PASS** (10/10) | **PASSED ✓** | ~$0.40 | ~5 min |
| Opus 4.7 (v3.2) | PASS (32/33; 97.0%) | **PASS** (10/10) | **PASSED ✓** | ~$2.45 | ~5 min |

**Both lanes PASS.** v3.2 protocol fix-forward (Fix 1 paired-board / 2-tone OOP CHECK exception + Fix 2 KB §1.7 OVERRIDE villain_air_pct ≥ 0.20 + Fix 3 F-S5 phantom feature) empirically validated on all 4 critical reversal anchors (d3688/d9556 CHECK + MW-39 CALL + d3178 BET preserved).

Per Path A revision decision tree row 1 at master `5cc7ba1`:
> "Sonnet PASS | Opus PASS → Ship Sonnet (cheaper; spec adequacy met; matches owner revert; cost in $140-$700 envelope)"

**Phase B labeller = Sonnet 4.6.**

## PRE-DISPATCH #4 closed — v3.2 protocol SHA256

| Artifact | SHA256 |
|----------|--------|
| `prompts/gto_labeller_v3.2.md` | `19ce318d908d7e2f8304e89c8c7465e07a1da594a78ee1757f2a7d824caee545` |
| `prompts/protocol_b_composition_first_v1_0.md` | `337f951704ee1d1b62b47e60c5a17a91c9933da859741507db495782d50e7640` |
| `prompts/protocol_b_composition_first_v1_0_pilot.md` | `93fc9f35a57bfaca5faaeece23a5689abe78c3690e4467a87cd13ebc405228e0` |
| `prompts/protocol_c_adversarial_elimination_v1_0.md` | `ed07e8891a8c7d394029c001da8322a558ae0207c382c5a4e59c581244cc762f` |
| `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` | `17ba5f0d24e66e6eb7266edf20f02cf2676ced3dc26c53f7e8185daf7b62805a` |

PRE-DISPATCH row #4 (Protocol A v3.2 frozen + checksum captured): **GREEN**.

## All PRE-DISPATCH prerequisites GREEN

Per Pilot Orch's A.7 GO comm, the prerequisite table is fully GREEN with row #4 now closed by this commit:

| # | Item | State |
|---|------|-------|
| 1 | Stage 6 holdout hash | GREEN |
| 2 | Pilot 100 disjoint from Stage 6 | GREEN |
| 3 | Pilot 100 disjoint from v2.3 calibration | GREEN |
| 4 | Protocol A v3.2 frozen + SHA256 captured | **GREEN — closed by this commit** |
| 5 | Protocol B v1.0.1 sealed + pilot artifact | GREEN |
| 6 | Protocol C v1.0.1 sealed + pilot artifact | GREEN |
| 7 | Stage 5 retrain protocol v1.0.1 sealed | GREEN |
| 8 | Task 4.5 logic hardening sealed | GREEN |
| 9 | QC pre-pilot sweep clean | GREEN |
| 10 | All 33 pilot agents pass blind calibration | GREEN (A.4 v3.2 retry validation; Phase B 15 labellers will run on this validated protocol) |
| 11 | Solver options match `feedback_solver_aligned_sizing.md` | GREEN |
| 12 | Pilot orchestrator session-launch cwd | GREEN |
| 13 | Owner explicit greenlight | GREEN (082336d + reaffirmations) |
| 14 | Anthropic API tier confirmed | DEFAULT Tier 1 (5-way × 3-batch parallelism per spec) |
| 15 | Model selection locked | **GREEN — Sonnet 4.6 labeller per owner revert + A.4 v3.2 winner-pick** |
| 16 | `_villain_pos_raw` live-selection rule honored | GREEN (A.5 PASS at b2de857) |

## Phase B dispatch directive

**Pilot Orchestrator (reactivates persona for Phase B execution):**

### Scope
- 15 labellers × Sonnet 4.6 × 100 hands × 3 protocols (A/B/C) = **1500 raw labels**
- Parallelism: 5-way × 3-batch protocol-grouped per spec §"Parallelism resolution"
- Wall-time target: ~90 min
- Cost target: ~$75-$375 (within $700 spec envelope)

### Halt thresholds (preserved from spec)
- Phase B subtotal > $375: WARN, continue
- Phase B subtotal > $700: HARD HALT, surface to orchestrator
- Total pilot run > $200 cap: HARD HALT
- Any agent failure rate > 20%: WARN
- Any agent failure rate > 50%: HARD HALT (likely model/protocol regression)

### Decision rules during Phase B
- Watch for protocol-side regressions (over-fold bias spreading beyond MW-17/41/44/49 pattern noted in A.7)
- If Sonnet calibration-time failures (4 of 33) replicate at scale (>15% on Phase B 100-hand corpus), surface as MEDIUM finding
- All other surface as A.4 v3.2-style protocol incidents per existing pattern

### Output expected
- 1500 individual label JSON entries (one per labeller × hand × protocol)
- Phase B summary comm with: success rate, cost actual, wall-time actual, distribution sanity check (action %, confidence %), any anomalies surfaced
- Phase B raw labels committed to a dedicated branch or to master under `review/pilot_run_2026-04-26/phase_b/...`

### Deferred items (post-Phase B, not blockers)
- Sonnet over-fold bias root cause (4 calibration failures: MW-17/41/44/49 — all FOLD-instead-of-CALL or CHECK-instead-of-BET on hidden equity / draw-equity spots)
- F-PR47-N1 NIT (2-tone-flush state-space enumeration)
- F-PR47-N2 NIT (MW-39 add to calibration_exam.py constants)
- 8 deferred teaching-stream renderer fix-forwards

## Phase B post-dispatch flow

Per spec §"Phase ordering":
- Phase B (mass labelling) → Phase C (highlighter consensus) → Phase D (highlighter audit) → Phase E (reviewer pass) → Phase F (adjudicator) → Phase G (corpus seal)

Each phase gets its own dispatch directive from orchestrator after the prior phase's GO summary surfaces.

## Cost dashboard

Phase A spend (this commit):
- A.4 v3.1 Option C (failed): $3.03
- v3.2 builder cycle (text edits): ~$0
- v3.2 builder reviewer dispatch: ~$0.50
- A.4 v3.2 retry (parallel Sonnet+Opus): ~$2.85
- v3.2 review dispatches (gto-expert, QC, builder): ~$5
- **Phase A total: ~$11.40 of $200 cap (5.7%)**

Projected through pilot completion:
- Phase B (Sonnet labeller): $75-$375
- Phase C-G (highlighter, reviewer, adjudicator, seal): ~$50-$150
- **Total pilot run projected: $140-$700 (within original spec envelope)**

## QC stream

QC Layer 3 watch continues. V-A4-1 vector closed empirically by A.4 v3.2 retry (the v3.1 Group-D BB-flop CHECK reversal failures now route correctly via Rule 11). May QC-audit this Phase B GO comm for synthesis adequacy if desired.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 49 | v3.2 protocol revision (PR #47) | ✅ SEALED at 42cace2 | — |
| 50 | A.4 v3.2 retry — parallel Sonnet+Opus | ✅ COMPLETE — both PASS | — |
| 51 | Phase B revised cost projection | ✅ $75-$375 / $700 envelope | — |
| 52 | A.8 final synthesis | ⏳ DEFERRED post-pilot completion | Orchestrator |
| 53 | F-PR47-N1 NIT (2-tone state-space) | ⏳ DEFERRED v1.0.x | Logic builder |
| 54 | F-PR47-N2 NIT (MW-39 constants) | ⏳ DEFERRED v1.0.x | Logic builder |
| 55 | Sonnet over-fold bias diagnosis | ⏳ DEFERRED post-pilot v3.x | Orchestrator |
| 56 | **Phase B mass labelling dispatch** | 🔥 **ACTIVE — this commit + subagent dispatch** | Pilot Orchestrator |

## Action

**Pilot Orchestrator (reactivate persona post-this-commit):**
1. Confirm Phase B dispatch greenlit (this comm)
2. Run 1500-label Phase B with 5-way × 3-batch protocol-grouped Sonnet labellers
3. Monitor cost + halt thresholds
4. Surface Phase B summary comm (`PILOT_PHASE_B_SUMMARY_*.md`) with results
5. Phase C dispatch awaits orchestrator confirmation post-Phase B

**Orchestrator (me):**
1. This Phase B GO comm shipped (atomic flow next)
2. Dispatch Pilot Orchestrator subagent for Phase B execution
3. /loop continues at 15-min cadence during Phase B (90 min wall-time → 6 ticks)
4. On Phase B summary surface: assess + write Phase C dispatch comm

**Owner:**
- A.7 GO acknowledged + Phase B GO confirmed per Path A revision decision tree (Sonnet ship)
- All PRE-DISPATCH prerequisites GREEN
- Phase A spend: $11.40 / $200 cap (5.7%)
- Phase B projected: $75-$375 / $700 envelope
- ETA Phase B summary: ~23:30-23:45 SAST (90 min from dispatch)
- Standing OWNER-AWAKE MODE directive: orchestrator advancing autonomously per quality gates; can intervene if cost trajectory or Phase B output surfaces concern

**QC stream:**
- Continue Layer 3 watch
- May audit this Phase B GO comm
- Standby for Phase B output sanity-check role (may be invoked post-Phase B summary)

## References

- A.7 v3.2 GO comm: `PILOT_PHASE_A_SUMMARY_GO_v3_2_2026-04-26.md` (master `903c5c9`)
- Path A revision (decision tree): `MAIN_TERMINAL_PATH_A_REVISION_ACK_OPUS_REVERT_2026-04-26.md` (master `5cc7ba1`)
- A.4 v3.2 calibration results: `review/pilot_run_2026-04-26/calibration_results_{sonnet,opus}_v3_2.json`
- A.4 v3.2 grading summary: `review/pilot_run_2026-04-26/phase_a4_v3_2_grading_summary.json`
- v3.2 protocol: `prompts/gto_labeller_v3.2.md`
- Pilot run plan: spec v1.0.3 §"Phase B"
- Memory: `feedback_quality_default_no_ask.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_solver_findings.md` (over-fold bias precedent)

**Status: PHASE A GO ✓ — PHASE B DISPATCH AUTHORIZED. SONNET LABELLER LOCKED IN. PILOT ORCHESTRATOR REACTIVATES FOR 1500-LABEL MASS LABELLING. ETA SUMMARY ~23:30 SAST.**
