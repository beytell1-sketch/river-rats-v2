---
date: 2026-04-26
from: Main terminal (orchestrator) per owner direction at 20:30 SAST
to: Pilot Orchestrator (logic builder under Pilot Orchestrator persona) · Owner · QC stream · gto-expert agents (dispatched)
re: NEW Phase A.8 (Range-Reasoning Coherence Audit) inserted between A.7 GO and Phase B dispatch; HALT Phase B until A.8 clean; owner observed inconsistent range understanding in earlier teaching-stream messages — root-cause + verify before committing 4500 mass labels
status: DIRECTIVE — Phase A.8 ACTIVE; runs in parallel with A.4 (already in flight); Phase B HELD at A.7 GO until A.8 surfaces clean findings; owner-observed historical inconsistency requires root-cause analysis before mass labelling; per quality-default + slow-deliberate
---

# Phase A.8 — Range-Reasoning Coherence Audit

## Owner direction (20:30 SAST)

> "yes make sure check if range is used correctly, we need to teach
> it but it starts at logic. this may take a dedicated approach. i
> noticed some inconsistent understanding of range in teaching
> messages in earlier versions. we need to spend time on labeling
> and feature tagging. it starts at labeling at its core. i want us
> to spend time on it here before mass labeling"

> "go with your recommendations"

Per `feedback_listen_to_orchestrator_always.md` + `feedback_quality_default_no_ask.md` + `feedback_slow_deliberate.md` — this is the right call.

## Why this matters

Range placement (top/middle/bottom of hero's own range) is the
foundational concept driving every postflop decision. If labellers
reason about range INCONSISTENTLY:
- Phase B will produce 4500 labels with internal inconsistency
- Stage 5 retrain ingests labels as ground-truth → garbage-in-garbage-out
- Owner already observed this manifest as inconsistent teaching
  messages in earlier production versions

**Mass labelling is precisely where this matters most.** The ~$700
total envelope buys 4500 labels; if even 10% have inconsistent
range reasoning, that's 450 corrupt training points downstream.

## Phase A.8 scope

Inserted as a new sequential gate between A.7 (Phase A summary)
and Phase B dispatch. Runs in parallel with A.4 (already in flight)
where possible — static audits + teaching archaeology don't need
A.4 results.

**Audit dimensions:**

### 1. Trace audit (post-A.4 completion)

Read every labeller's range-reasoning paragraph from A.4 traces
(Sonnet × 38 + Opus × 38 = 76 traces). Apply this rubric:

- **R1.** Is HRP (`hero_range_percentile`) referenced when relevant?
- **R2.** Is HRP overridden when hand is visibly strong (DO NOT Rule
  10 application)? Specifically: when hand is top-pair+ / overpair /
  two-pair / set / strong-draw and HRP=0.00, does the labeller flag
  it as data-quality vs treating it as bottom-of-range?
- **R3.** Is hero's hand classified into top / middle / bottom of
  range explicitly? Or does the labeller skip this classification?
- **R4.** Does the labeller cite hero range-composition features
  alongside the bucket? (`hero_top_pair_plus_pct`, `hero_overpair_pct`, etc.)
- **R5.** For mixed-strategy spots, is range-placement frequency
  reasoned? Example: "AK is top-25% of my range vs villain's
  composition, so value-bet 75% / check-to-induce 25%."
- **R6.** Cross-trace consistency: do labellers agree on range
  placement for the SAME hand? (Inter-trace agreement check.)

### 2. Static prompt audit

Dispatch gto-expert agent to read:
- `prompts/protocol_b_composition_first_v1_0_pilot.md` (Build A output)
- `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` (Build B output)
- `prompts/gto_labeller_v3.1.md` (canonical source)
- `prompts/protocol_b_composition_first_v1_0.md` (design artifact)
- `prompts/protocol_c_adversarial_elimination_v1_0.md` (design artifact)

Check for:

- **S1.** HRP usage consistency: are all references to `hero_range_percentile` semantically aligned? Any internal contradictions?
- **S2.** DO NOT Rule 10 application: is the test-harness artifact warning correctly cross-referenced everywhere HRP is mentioned?
- **S3.** Worked examples (Examples 1-3 in Protocol B/C) — do they demonstrate range-placement reasoning correctly + consistently?
- **S4.** Cross-protocol consistency: for the SAME hand class on the SAME composition, do Protocol B and Protocol C arrive at the same range-placement classification? (They should — convergence is part of the spec's quality gate.)
- **S5.** Feature semantics:
  - `hero_range_percentile` (1.0 = top, 0.0 = bottom)
  - `board_adjusted_hrp` (board-adjusted version)
  - `hero_top_pair_plus_pct` (% of hero's range that's TP+)
  - Are these interpreted consistently across all reasoning steps?
- **S6.** Mixed-strategy treatment: do the prompts handle "frequency from range-placement" correctly? E.g. "value-bet 75% / check 25% on top-half of range"?

### 3. Teaching-stream archaeology (parallel agent)

Dispatch separate agent to `~/river-rats-teaching/` to:

- **T1.** Find historical teaching messages discussing range / range-placement / hero range / villain range
- **T2.** Identify inconsistencies the owner observed
- **T3.** Root-cause analysis: was the inconsistency from
  - (a) bad training labels (labelling-protocol artifact),
  - (b) bad teaching prompts (teaching-stream artifact),
  - (c) bad model behavior (model-side artifact)?
- **T4.** Surface the most representative ~3-5 inconsistent teaching messages for owner reference

This is critical because if root-cause is (a) bad training labels,
then the labelling protocol fix MUST happen before Phase B. If it's
(b) or (c), Phase B can proceed but the teaching-stream needs its
own fix.

### 4. Calibration coverage audit

Audit the 28-hand exam + 10 reversal hands in `calibration_exam.py`
v2.3 + `BATCH2_8_HAND_DESIGNS.md`:

- **C1.** Coverage: do the 38 hands include sufficient examples of:
  - Top-of-range value-bet scenarios (target: ≥3 hands)
  - Middle-of-range pot-control / mixed scenarios (target: ≥3 hands)
  - Bottom-of-range bluff-catch / fold scenarios (target: ≥3 hands)
  - Range-vs-range matchups across positions (target: ≥3 hands)
- **C2.** Skew: is the calibration set skewed toward one range-placement scenario?
- **C3.** If coverage is insufficient: recommend supplementary calibration hands (Build E candidate)

### 5. Findings synthesis

Orchestrator-owned. Aggregate trace audit + static audit + teaching archaeology + coverage audit. Three possible outcomes:

| Outcome | Action |
|---------|--------|
| **CLEAN** — all 4 audits show consistent range reasoning | Dispatch Phase B with confidence; A.8 sealed |
| **MINOR ISSUES** — single-prompt clarification or coverage gap | Fix-forward via Protocol B/C v1.1.x or Build E supplementary calibration; re-audit; then dispatch Phase B |
| **MAJOR ISSUES** — systemic range-reasoning inconsistency in protocols OR teaching-stream archaeology shows labelling-protocol root cause | Halt Phase B indefinitely; build a "range-reasoning training pack" (Build F candidate) — extra 5-10 worked examples specifically for range placement; integrate into Protocol B + C v1.1.0; re-run subset of A.4 calibration; re-audit |

## Sequencing

```
[NOW: A.4 in flight]
  └→ A.4 dispatched 20:23; ETA ~38 min; produces 76 reasoning traces
[PARALLEL: dispatch now]
  ├→ Static prompt audit (gto-expert agent on prompts/) — ~30-45 min
  └→ Teaching-stream archaeology (general-purpose agent on ~/river-rats-teaching/) — ~30-45 min
[POST-A.4 COMPLETION]
  └→ Trace audit (gto-expert agent on A.4 traces) — ~15-30 min
[POST-A.7]
  └→ Calibration coverage audit + Findings synthesis — orchestrator-owned ~30 min
[GATE]
  └→ A.8 outcome determines Phase B disposition (CLEAN / MINOR / MAJOR)
```

**Phase B HELD at A.7 GO until A.8 surfaces synthesis.**

**Wall-time impact:** A.8 adds ~30-90 min to pilot timeline (~30 min if all parallel work overlaps with A.4; up to 90 min if MAJOR issues require fix-forward). Per `feedback_no_deadlines.md` — quality > speed.

## Cost impact

A.8 adds ~$5-15 in agent dispatch cost (small). Static audit + teaching archaeology + trace audit are all relatively cheap (Read/Grep heavy, light LLM reasoning). Total Phase A budget remains within ~$200 hard cap.

## Action items

**Pilot Orchestrator:**
1. Continue A.4 dispatch (no change — just wait for completion)
2. Compose A.7 summary normally; report findings
3. **HALT Phase B dispatch** — wait for orchestrator A.8 synthesis before Phase B
4. After A.4 completes: surface raw 76 reasoning traces in
   `review/pilot_run_2026-04-26/` for orchestrator agent to audit

**Orchestrator (me):**
1. This directive shipped (atomic flow next)
2. Dispatch static prompt audit agent (gto-expert flavor) — parallel with A.4
3. Dispatch teaching-stream archaeology agent — parallel with A.4
4. Dispatch trace audit agent post-A.4 completion
5. Synthesize findings; gate Phase B on A.8 outcome
6. /loop continues at 25-min cadence; will tighten when A.4 + agents converge

**QC stream:**
- Continue Layer 3 watch
- A.8 audit IS analogous to QC's TC-15 multi-expert framework but
  scoped to range-reasoning specifically; no additional QC dispatch
  required unless QC sees signal worth flagging

**Owner:**
- A.8 inserted; Phase B held until A.8 clean
- ~30-90 min wall-time addition (~$5-15 agent cost)
- Trace audit will use real Sonnet/Opus reasoning paragraphs from A.4
  as ground-truth empirical data
- Outcome surfaced when synthesis complete; may require Build F
  (range-reasoning training pack) if MAJOR issues

## Owner-side input still useful

When you have time, the audit benefits from:
- Specific examples of historical teaching-message range inconsistency
  (which earlier version? what kind of inconsistency? deployed where?)
- Owner-side rubric additions to my proposed R1-R6 / S1-S6 / T1-T4 / C1-C3

But agents will proceed with current rubric while you're away.

## References

- Pilot Phase A status: `review/comms/PILOT_PHASE_A_STATUS_2026-04-26.md`
  (master `70efde6`)
- Option C directive: `review/comms/MAIN_TERMINAL_PILOT_PHASE_A_OPTION_C_DIRECTIVE_2026-04-26.md`
  (master `439cfd7`)
- Spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` (master HEAD)
- Calibration source: `river-rats-core/calibration_exam.py` v2.3
- Build A pilot artifact: `prompts/protocol_b_composition_first_v1_0_pilot.md`
- Build B pilot artifact: `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
- v3.1 canonical source: `prompts/gto_labeller_v3.1.md`
- HRP investigation memo: `HRP_INVESTIGATION_2026-04-15.md` (referenced in DO NOT Rule 10)
- Memory: `feedback_quality_default_no_ask.md`,
  `feedback_slow_deliberate.md`,
  `feedback_listen_to_orchestrator_always.md`,
  `feedback_solver_vs_expert_labels.md`,
  `feedback_preflop_geometry_vs_postflop_composition.md`

**Status: PHASE A.8 RANGE-REASONING COHERENCE AUDIT ACTIVE.
Phase B HELD at A.7 GO. Audit agents dispatching now in parallel
with A.4. Synthesis expected ~21:30-22:00 SAST.**
