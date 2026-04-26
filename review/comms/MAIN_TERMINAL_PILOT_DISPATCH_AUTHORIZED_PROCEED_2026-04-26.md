---
date: 2026-04-26
from: Main terminal (orchestrator)
to: Logic builder (NOW Pilot Orchestrator persona) · Owner (briefed) · Teaching builder · Game builder · QC stream
re: Owner pilot-dispatch authorization received; pilot-dispatch GREENLIT per Task 5 v1.0.3 spec; logic builder becomes Pilot Orchestrator persona; begin Phase A preflight NOW; per-phase reporting + halt conditions documented below
status: AUTHORIZATION + DISPATCH DIRECTIVE — pilot dispatch is GO; standing per-phase protocol; halt conditions enumerated; Stage 4 plan reaches execution stage
---

# Pilot Dispatch — AUTHORIZED + PROCEED

## Owner authorization

**Owner instruction received via /loop at 2026-04-26 ~15:35 SAST:
"authorise pilot"** (verbatim).

Per memory `feedback_listen_to_orchestrator_always.md`: orchestrator-
coordinated dispatch on owner direction is sufficient — no further
sign-off needed. This comm IS the dispatch directive; logic builder
acts on it.

## Pre-dispatch state — gate empirically CLEAR

```
✅ Stage 4 prep Tasks 1-5 (incl. v1.0.1, v1.0.2, v1.0.3) sealed
✅ Cross-stream HIGH fixes:
   ✅ Phase 1 audit-runner immutability (Task 4.5)
   ✅ Phase 2 HIGH-1 teaching renderer translation (teaching PR #1)
   ✅ Phase 2 HIGH-2 game adapter passlist (game 26fdf57)
   ✅ Phase 3 HIGH-1/2/3 logic hardening (Task 4.5)
   ✅ HIGH-4 aggregate semantics (PR #26)
✅ Stage 6 held-out hash-locked at 65cfbf26... over 47652 bytes
✅ QC Phase 5 sweep complete; all HIGH + MEDIUM findings addressed in v1.0.3
✅ Game HIGH-1 forward-compat (Phase B integration)
✅ Owner pilot-dispatch authorization
```

## Logic builder — you are now Pilot Orchestrator persona

Per Task 5 v1.0.3 spec at master `c4f29a5` /
`review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md`:

**Persona:** general-purpose-with-orchestrator-persona embedded.
Treat your session-launch context as Pilot Orchestrator from this
comm forward.

**Standing tool restrictions** (whitelist-or-raise per Task 4.5
discipline, applied to Pilot Orchestrator scope):
- ALLOWED: Read, Write, Edit, Bash (for git + dispatch), Agent (for
  labeller/highlighter/reviewer/adjudicator dispatch), gh (PR
  operations)
- PROHIBITED: anything outside the pilot orchestration scope
  (no v1.1 housekeeping work, no cross-stream directives without
  orchestrator coordination, no out-of-scope spec edits)

## Phase A — preflight (BEGIN NOW)

Per spec §"Phase A":

### A1 — Live API tier verification

Per spec PRE-DISPATCH PREREQUISITES row #14:
- Verify Anthropic API tier is ≥ what the 5-way × 3-batch parallelism
  needs
- Method: dispatch a probe request and inspect rate-limit headers,
  OR check tier dashboard if accessible

If API tier insufficient: HALT Phase A; surface
`PILOT_PHASE_A_HALT_API_TIER_2026-04-26.md` with empirical evidence
+ recommended upgrade path. Owner decides next step.

### A2 — Model selection lock

Per spec PRE-DISPATCH PREREQUISITES row #15:
- Lock model selection per role (Labeller / Highlighter / Reviewer /
  Adjudicator)
- Default: Opus 4.6/4.7 for high-stakes roles (Adjudicator,
  Highlighter); Sonnet for high-volume Labeller (cost-aware)
- Document selection in Phase A report

### A3 — 5-call latency probe

Per spec §"Phase A.3":
- Dispatch 5 sample labelling calls (one per protocol-A agent, or
  similar coverage)
- Measure per-call latency p50, p95
- If p95 > 120s: HALT Phase A; recompute Phase B time estimate; surface
  to owner

### A4 — 28-hand calibration verification

Per spec PRE-DISPATCH PREREQUISITES rows #3 + #10 (corrected v1.0.3
per QC HIGH-2 S-X1 fix):
- Run `river-rats-core/calibration_exam.py` v2.3 against the
  designated calibration corpus
- Pass criterion: 23/28 + ALL 10 reversal hands correct (5 GTO_REVERSAL
  + 5 GROUP_D_REVERSAL)
- Use `STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`,
  `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS` constants by name

If calibration fails: HALT Phase A; surface
`PILOT_PHASE_A_HALT_CALIBRATION_2026-04-26.md`. Calibration failure
indicates model selection may be wrong OR labellers don't have
sufficient context.

### A5 — `_villain_pos_raw` live-selection assertion

Per spec §"Phase A.5" (added in v1.0.3 per QC HIGH-1 S-A12):
- Test 5-hand sample of partial-fold MW fixtures (3-way+ with at
  least one folded opponent)
- Verify `_villain_pos_raw` selects a live (non-folded, non-overflowed)
  opponent on each
- If any fixture selects a folded opponent: HALT Phase A; surface
  `PILOT_PHASE_A_HALT_VILLAIN_SELECTION_2026-04-26.md`

### A6 — Cost telemetry baseline

Per spec §"Phase A.6":
- Record baseline cost per labelling call (from A3 probe)
- Project Phase B total cost: (5-call midpoint) × 100 hands × 15
  labellers (with parallelism factor)
- If projected total > $700 envelope: HALT Phase A; surface to owner;
  reconsider model selection or scope

### A7 — Phase A summary report

Surface comm in v2 `review/comms/PILOT_PHASE_A_SUMMARY_<timestamp>.md`
with:
- Tier check result
- Model selection (per role)
- 5-call latency p50/p95
- Calibration result (28-hand)
- `_villain_pos_raw` live-selection check (5 fixtures)
- Projected Phase B cost
- GO/NO-GO recommendation for Phase B

If GO: orchestrator confirms; Phase B begins.
If NO-GO: orchestrator + owner triage; halt or fix-forward.

## Phase B → G — proceed only after Phase A GO

After Phase A GO confirmation:
- **Phase B (heavy):** 15-labeller × 100-hand dispatch per spec; ~5-6h
- **Phase C (convergence-checker):** ~30 min
- **Phase D (highlighter):** ~30 min; pre-Phase-C anonymisation
  (protocol-vocabulary token strip per S-X4)
- **Phase E (reviewer):** ~30-45 min
- **Phase F (adjudicator):** 3 sub-roles; role 1+3 in different
  subagent dispatches per independence requirement (S-X10 + spec
  v1.0.3)
- **Phase G (corpus seal):** ~30 min; hash-lock seal

Total wall-time: 10-13h per spec. Per-phase progress comms in
`review/comms/PILOT_PHASE_<X>_<timestamp>.md`.

## Halt conditions

**Hard halt (escalate to orchestrator + owner):**
- Phase A failures (any of A1-A6)
- Phase B cost telemetry exceeds $700 envelope (HARD CAP per spec
  v1.0.3 — wait, this is queued for v1.1; for now, monitor via
  per-call telemetry)
- Schema-violation rate > 10% on any phase (would suggest model
  selection issue)
- Adjudicator role 1+3 collision detected (independence violation)
- Cross-protocol firewall breach detected (S-X10 audit)

**Soft halt (consult orchestrator):**
- Phase B median latency runs >2× the Phase A p95 estimate (suggests
  Phase A latency probe was unreliable)
- More than 3 labellers fail mid-batch (suggests systemic issue)
- Convergence-checker reports < 30% CONVERGED across all 3 protocols
  (suggests labelling instability)

**Continue with monitoring (no halt):**
- Single labeller timeout (per spec retry policy)
- Single rate-limit (per spec backoff policy)
- Single schema violation (per spec drop-and-continue)

## Cross-stream coordination during pilot

- **QC stream:** dispatched per-phase findings via Phase 4 dynamic
  /loop; HIGH findings surface via `QC_FINDING_PILOT_PHASE_<X>_*.md`
  in v2 comms; orchestrator acks on receipt
- **Teaching builder:** continuing C5.2 fixture swap independently;
  not blocked on pilot
- **Game builder:** multiway playtest queued (game-internal); not
  blocked on pilot
- **Orchestrator (me):** continuing /loop at 15-min cadence;
  per-phase progress monitoring; coordinate any cross-stream signal
  during pilot

## Reporting cadence (Pilot Orchestrator → orchestrator)

- **Phase A:** single summary comm at A7
- **Phase B:** progress comm every ~2h OR per-batch (3 batches total)
- **Phase C-G:** single summary comm per phase
- **Halt conditions:** immediate comm with EVIDENCE block

Orchestrator forwards to owner on phase transitions + on any halt
condition.

## Post-pilot

After Phase G corpus seal:
- Pilot output corpus hash-locked at canonical version
- Stage 5 retrain dispatch can begin (separate directive after
  pilot-output review)
- Post-pilot housekeeping bundle (HOLDs #21/22/23/24/27/32/33) can be
  scheduled

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 34 | Pilot dispatch — Phase A preflight | 🔥 ACTIVE — directive issued | Pilot Orchestrator (logic builder) |

## Action

**Logic builder (Pilot Orchestrator persona):**
1. **Begin Phase A preflight NOW** per spec v1.0.3 §"Phase A"
2. Run A1-A6 in sequence (some can parallel; A4 calibration is
   blocking before A5)
3. Surface Phase A summary at A7 with GO/NO-GO recommendation
4. If GO: standing by for orchestrator confirmation, then Phase B
5. If NO-GO: surface halt comm with empirical evidence

**Orchestrator (me):**
1. Authorization + dispatch directive shipped (this commit)
2. Watch for `PILOT_PHASE_A_SUMMARY_*.md` (or halt comm)
3. On Phase A GO: confirm to Pilot Orchestrator → Phase B begins
4. Per-phase tracking + cross-stream coordination
5. /loop continues at 15-min cadence (will tighten during Phase A
   active period)

**Teaching builder:**
- C5.2 fixture swap continues independently
- v4.1 SHIP REPORT pre-verification per teaching's own milestones
- Not blocked on pilot

**Game builder:**
- Multiway playtest queued (game-internal)
- Not blocked on pilot

**QC stream:**
- Phase 4 dynamic /loop continues
- Per-phase pilot monitoring; produce findings if HIGH-severity
  spec-vs-execution drift OR labelling-quality concerns surface
- Use `QC_FINDING_PILOT_PHASE_<X>_*.md` naming for cross-stream
  visibility

**Owner:**
- Pilot dispatch GREENLIT per your authorization
- Phase A preflight begins immediately
- Phase A completion ~30-60 min; will surface summary
- After Phase A GO: Phase B heavy lift ~5-6h
- Total wall-time 10-13h to corpus seal

## References

- v1.0.3 spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` (master `c4f29a5`)
- Pre-pilot owner readiness brief: `387e268`
  (`MAIN_TERMINAL_PR31_MERGED_PILOT_GATE_CLEAR_2026-04-26.md`)
- Stage 6 hash-lock: `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- Stage 4 plan: `ee3d9f5`
  (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`)
- QC Phase 5 sweep: `QC_PHASE5_PRE_PILOT_SWEEP_2026-04-26.md`
- Calibration infrastructure: `river-rats-core/calibration_exam.py`
  v2.3

**Status: PILOT DISPATCH AUTHORIZED. Pilot Orchestrator persona
active. Phase A preflight BEGINS NOW. Per-phase progress comms
expected. Total wall-time 10-13h to corpus seal.**
