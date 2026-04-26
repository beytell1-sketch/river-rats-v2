---
date: 2026-04-26
from: Main terminal (orchestrator) per owner direction at 20:25 SAST
to: Pilot Orchestrator (logic builder under Pilot Orchestrator persona) · Owner (briefed) · QC stream
re: Option C authorized — parallel Sonnet 4.6 + Opus 4.7 calibration on 28-hand A.4 exam; winner ships for Phase B; API tier defaults to Tier 1 pending owner console check; cost authorization ~$100-180 Phase A within $700 envelope
status: DIRECTIVE — Pilot Orchestrator may dispatch A.4 calibration with Option C parallel model setup; A.6 cost telemetry tracks both models in parallel; A.3 latency derived from A.4 telemetry; A.7 summary picks winner empirically
---

# Pilot Phase A — Option C Directive

## Owner direction (20:25 SAST)

> "go with your recommendation for test"

Per `feedback_listen_to_orchestrator_always.md` — owner direction is sufficient
authorization. Pilot Orchestrator may dispatch A.4 calibration immediately on
this directive.

## Option C — parallel Sonnet 4.6 + Opus 4.7 calibration

**Test mechanism:**

1. **Same 28-hand standard exam + 10 reversal hands** (per
   `calibration_exam.py` v2.3 constants: `STANDARD_EXAM_SIZE=28`,
   `STANDARD_PASS_THRESHOLD=23`, `GTO_REVERSAL_HANDS`,
   `GROUP_D_REVERSAL_HANDS`)
2. **Run A.4 with BOTH labeller models in parallel:**
   - Lane S: Sonnet 4.6 × 28-hand standard + 10 reversal
   - Lane O: Opus 4.7 × 28-hand standard + 10 reversal
3. **Both lanes graded against same answer key** (Pilot Orchestrator,
   not visible to labeller agents)

**Decision tree post-A.4:**

| Sonnet result | Opus result | Phase B labeller |
|---------------|-------------|------------------|
| PASS (≥23/28 + 100% reversal) | PASS | **Sonnet 4.6** (cheaper; both adequate) |
| PASS | PASS-WITH-EDGE (Opus higher score) | **Sonnet 4.6** (still adequate; cost wins per `feedback_quality_default_no_ask.md` line "best model that can do the work") |
| FAIL | PASS | **Opus 4.7** (only Opus is adequate) |
| FAIL | FAIL | **HALT** — escalate to owner; reasoning labeller-side, not model-side |

**Rationale on "PASS, ship cheaper":** the spec calibration is the empirical
adequacy gate. If Sonnet passes the 23/28 threshold + 100% reversal, it IS
adequate per spec. Shipping Sonnet for Phase B saves ~$300-1500 vs Opus across
4500 labellings. Quality-default = "best model that can do the work" not
"most expensive model available."

If owner wants to override and ship Opus regardless of Sonnet pass: surface
that override after A.4 results.

## API tier default — Tier 1 (pending owner console check)

Owner mentioned Max account (consumer plan) but noted uncertainty on API
tier. Defaulting to Tier 1 per spec. Pilot Orchestrator runs Phase B as
**5-way × 3-batch protocol-grouped parallelism** (~90 min wall-time) unless
owner confirms higher tier later.

If owner checks console.anthropic.com → settings/limits and confirms Tier 2-4
before Phase B dispatches: orchestrator updates lock to single-batch 15-way
(~30 min wall-time). Phase B can re-plan when tier confirmed.

A.3 latency probe is now derived from A.4 telemetry (Phase A.4's
56 + 20 = 76 calls per model far exceeds the 5-call probe; p50/p95
naturally emerge from A.4 cost-tracker output).

## Cost authorization — $100-180 Phase A; $700 total envelope

**Owner's "go with your recommendation" carries cost authorization for
Option C** per quality default + the spec's $700 total pilot run envelope.

Phase A breakdown with Option C:
- Sonnet 4.6 × 38 hands ≈ $25-65 (per spec §"Cost tracking" Sonnet rates)
- Opus 4.7 × 38 hands ≈ $80-130 (Opus 5x Sonnet)
- A.5 fixture verification: $0 (already done; loaded from disk)
- A.6 cost-telemetry overhead: ~$0 (recorded as side-effect)
- A.3 latency probe: $0 (subsumed into A.4 lanes)
- **Phase A subtotal:** ~$105-195 (slightly over original $25-130 estimate)

Phase B downstream depends on A.4 winner:
- If Sonnet wins → Phase B ~$75-375 (current spec default)
- If Opus wins → Phase B ~$375-1875 (over $700 envelope; Pilot Orchestrator
  must HALT and escalate to owner before Phase B dispatch in this case)

**Hard caps:**
- Phase A subtotal must stay under $200 (cushion for variance)
- Total pilot run must stay under $700 envelope
- If A.4 totals exceed $200 OR if Sonnet fails AND Opus would push Phase B
  over $700: HALT, escalate to owner

## Pilot Orchestrator action items

1. **Dispatch A.4 calibration with Option C parallel setup** immediately
2. **Track cost per model** (Sonnet vs Opus) via A.6 telemetry
3. **Cancel + escalate** if Sonnet runs > $80 (4x estimate) OR Opus runs
   > $200 (1.5x estimate); these are halt thresholds
4. **A.3 latency** subsumed; report p50/p95 per model from A.4
5. **A.7 summary** explicitly picks Phase B winner per decision tree above
6. **Cost reporting:** include per-model totals in A.7 summary
7. **Halt if both fail:** spec halt condition #4 (calibration failure)

## Standing reminders to Pilot Orchestrator

- Per spec v1.0.3 §"Tool restrictions": git ops belong to builder persona;
  Pilot Orchestrator transients-reactivates builder for git ops only when
  needed (writing run reports, A.7 summary, etc.)
- Per `feedback_quality_default_no_ask.md`: pick clean path; default per
  decision tree above unless evidence demands deviation
- Per `feedback_no_deadlines.md`: A.4 calibration may legitimately run long;
  no artificial deadline; quality > speed
- Per `feedback_solver_vs_expert_labels.md`: NEVER use solver output as
  training labels; calibration grades against answer key not solver

## Cross-stream

- **QC Layer 3 pilot-runtime watch:** continue monitoring A.4 dispatch;
  surface findings per `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`. V-X4 + V-D9
  curatives mean QC will catch divergence between predicted vs actual
  per-model behavior more rigorously now.
- **Teaching builder:** C5.2 fixture swap independent
- **Game builder:** multiway playtest independent

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 44 | Phase A preflight (A.5 done, A.4 with Option C ACTIVE) | 🔥 ACTIVE per this directive | Pilot Orchestrator |
| 46 | Owner console check for API tier (informs Phase B parallelism) | ⏳ ASYNC owner action | Owner |
| 45 | Phase B-G heavy lift (post Phase A GO with empirical Phase B model) | ⏳ QUEUED | Pilot Orchestrator |

## Action

**Pilot Orchestrator:**
1. Take this directive as A.4 dispatch authorization
2. Set up parallel Sonnet + Opus lanes per Option C
3. Execute calibration; track per-model cost
4. Surface progress comm at A.4 midpoint (~$50-100 spent) for orchestrator
   visibility
5. Surface A.7 summary with winner-pick + GO/NO-GO for Phase B
6. HALT + escalate if any halt threshold tripped

**Orchestrator (me):**
1. This directive shipped (atomic flow forthcoming)
2. Watch for A.4 progress comm + A.7 summary
3. On A.7 GO: confirm Phase B dispatch with winner model + Tier 1 default
4. /loop continues at 25 min cadence; tighten to 10 min once A.4 completes
5. If owner returns with API tier confirmation: update Phase B parallelism
   plan

**QC stream:**
- Continue Layer 3 watch
- A.4 calibration is high-value monitoring point for HALT-class signal

**Owner:**
- Option C authorized + dispatched per your direction
- Phase A.4 ETA ~38 min from dispatch (calibration is the long pole)
- A.7 summary expected ~21:30 SAST (38 min from now)
- API tier console check still pending — gives you opportunity to update
  Phase B parallelism plan before Phase B dispatches
- Cost commitment: ~$105-195 Phase A; ~$700 total envelope hard cap

## References

- Pilot Phase A status: `review/comms/PILOT_PHASE_A_STATUS_2026-04-26.md`
  (master `70efde6`)
- Pilot dispatch authorization: `MAIN_TERMINAL_PR45_MERGE_ACK_PILOT_DISPATCH_RESUME_2026-04-26.md`
  (master `eaefc2a`)
- Spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` (master HEAD)
- Calibration source: `river-rats-core/calibration_exam.py` v2.3
- Memory: `feedback_quality_default_no_ask.md`,
  `feedback_listen_to_orchestrator_always.md`,
  `feedback_solver_vs_expert_labels.md`

**Status: OPTION C AUTHORIZED. Pilot Orchestrator may dispatch A.4
parallel calibration NOW. A.7 summary expected ~21:30 SAST.**
