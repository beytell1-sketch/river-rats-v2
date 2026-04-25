---
date: 2026-04-26
from: Main terminal (orchestrator) — DRAFT
to: Owner · ML-architect · Pilot orchestration agent (when commissioned)
re: Stage 4 pilot orchestration script — concrete agent-dispatch sequence for the 33-agent pilot per locked plan
status: DRAFT v0.1 — orchestrator structural framework; awaits ML-architect + owner review for execution sequencing + parallelism details
---

# Stage 4 Pilot Orchestration Script — DRAFT v0.1

## Purpose

Per locked Stage 4 plan (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
`ee3d9f5`), the pilot dispatches 33 agents across 5 roles:

- 15 labellers (3 protocols × 5 agents per protocol)
- 6 highlighters (H1 + H2, 3 each)
- 8 reviewers
- 3 adjudicators
- 1 pilot orchestrator (independent of all above)

This draft specifies the execution sequencing — who dispatches whom,
in what order, with what handoffs.

## Pre-conditions (before pilot dispatch)

The following must be GREEN before pilot dispatch:

1. **Stage 3.5 complete** — commit 16 + M4/M5 audits clean on origin/master
2. **Protocol B + C prompts** — finalised (post-DRAFT-v0.1, owner-
   approved + gto-expert-content-filled + reviewer-passed +
   calibration-exam-passed)
3. **All 33 pilot agents pass blind calibration** — 20/24 + all 3
   GTO-reversals correct
4. **Held-out test set authored + locked** (per
   `STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md`) so it's NOT in the
   pilot corpus
5. **Feature pipeline updated for v2.4 P1 + post-commit-14 multiway
   fields** — Exp 3 auxiliary attention (108 columns base + 8
   additional for v2.4 = 116 total); commit 14 promotes
   `_per_villain_*` fields
6. **Owner explicit greenlight** — pilot dispatch authorisation per
   locked plan §11 "execution authorisation, not design"

If any pre-condition is RED, pilot does NOT dispatch. Wait for
clearance.

## Pilot orchestrator agent role

The **Pilot Orchestrator** (1 agent) coordinates the dispatch of
the other 32. They do NOT label, highlight, review, or adjudicate.
Their role is sequencing + tracking + reporting.

Pilot Orchestrator session-launch cwd: `~/river-rats-v2/` so they
have access to all project-local subagents (gto-expert, ml-architect,
reviewer if applicable).

[**ML-ARCHITECT REVIEW NEEDED:** whether Pilot Orchestrator can be
a general-purpose-with-orchestrator-persona dispatch, or needs to
be a dedicated subagent. Owner to decide. For DRAFT, assume
general-purpose-with-persona is acceptable.]

## Dispatch sequence

### Phase A — Calibration (parallel)

ALL 33 pilot agents take the calibration exam in parallel (same 24
hands, blind, independent grading). Pilot Orchestrator dispatches
33 agents with the same blind exam input.

Each agent returns:
- 24 actions (their answers)
- Reasoning trace per hand (per protocol; protocol-specific format)

Pilot Orchestrator grades against answer key (NOT visible to agents).
Records pass/fail per agent.

Pass criterion: 20/24 + all 3 GTO-reversal hands correct.

| Outcome | Action |
|---|---|
| All 33 pass | PROCEED to Phase B |
| 1-3 fail | Pilot Orchestrator dispatches replacement agents for failed slots; re-test |
| 4+ fail | HALT pilot. Calibration regression — investigate Stage 4 prompt quality before continuing. |

### Phase B — Action labelling (parallel; 100 hands × 15 agents)

Pilot Orchestrator dispatches 15 labellers in parallel (5 Protocol-A
+ 5 Protocol-B + 5 Protocol-C). Each labeller receives the SAME 100-
hand stratified pilot corpus.

Each labeller returns 100 labels (one per hand) with reasoning
traces specific to their protocol.

Total labels collected: 15 × 100 = 1500 label-records.

[**ML-ARCHITECT REVIEW NEEDED:** parallelism vs sequential. 15
agents in parallel is high concurrency. Owner / ml-architect to
confirm tractable. Alternative: 3 batches of 5 agents (one per
protocol) sequentially.]

### Phase C — Highlighting (parallel; depends on Phase B labels)

Once Phase B labels are collected: Pilot Orchestrator dispatches 6
highlighters in parallel (3 H1 + 3 H2). Each highlighter receives:

- The 100-hand pilot corpus
- The cross-protocol consensus action label per hand (from Phase B
  convergence — see Phase D)

H1 highlighters tag PRIMARY + CONFIRMED attention flags per Exp 3
auxiliary protocol. H2 highlighters tag intention multi-label per
Exp 4 protocol.

[**ML-ARCHITECT REVIEW NEEDED:** Phase C ordering — should
highlighting see ONLY the consensus action, or ALSO the protocol-A
reasoning trace? Trade-off: more context = better highlighting; but
contaminates highlighter independence from labeller reasoning.
Owner / ml-architect to decide.]

### Phase D — Convergence analysis (Pilot Orchestrator solo)

Pilot Orchestrator computes:

- **Within-protocol κ** per protocol (3 separate κ values, one each
  for A/B/C)
- **Cross-protocol κ** per pair (3 pairs: A↔B, B↔C, A↔C)
- **3-of-3 cross-protocol agreement** count: hands where all 3
  protocols agree on the action
- **Hands routed to adjudication:** where cross-protocol agreement
  is < 3-of-3 OR within-protocol κ is anomalously low

Compare against pre-registered stop conditions (locked plan §4.3):

| Metric | Threshold | Pilot decision |
|---|---|---|
| Within-protocol κ (each) | ≥ 0.75 | If miss: HALT pilot, prompt revision |
| Cross-protocol κ (any pair) | ≥ 0.60 | If miss: HALT, investigate via solver |
| 3-of-3 agreement | ≥ 70% of hands | If miss: KB has gaps |
| Hands to adjudication | ≤ 25% of pilot | If exceed: HALT, KB / prompt revision |
| H1 ↔ H2 highlight Jaccard | ≥ 0.50 | If miss: investigate |

If ALL thresholds met: PROCEED to Phase E.
If ANY threshold missed: HALT pilot, surface to owner, re-pilot.

### Phase E — Reviewer pass (parallel; depends on Phase B + D)

Pilot Orchestrator dispatches 8 reviewers in parallel:

- 3 reviewers spot-check Protocol-A reasoning traces (sample hands)
- 2 reviewers spot-check Protocol-B
- 2 reviewers spot-check Protocol-C
- 1 reviewer spot-checks H1 + H2 highlighting + audits Pilot
  Orchestrator's convergence analysis

Each reviewer returns concerns + recommendations. Pilot Orchestrator
incorporates recommendations into pilot report.

### Phase F — Adjudication (parallel; depends on Phase D)

For hands routed to adjudication (≤ 25% of pilot per stop condition):

Pilot Orchestrator dispatches 3 adjudicators per the locked Stage 4
panel:

- **GTO expert adjudicator** — reads all 15 labellers' reasoning
  traces; produces tiebreaker reasoning. NEVER sees solver output
  before producing reasoning.
- **Solver-verify operator** — runs solver on each adjudicated spot
  per `feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/
  75%, river 33%/75%/150%); produces solver action distribution.
- **Adjudication writer** — combines GTO reasoning + solver output
  → final label OR "ambiguous, drop from training."

Output per adjudicated hand:
- Final action (or DROP)
- Confidence band (HIGH / MEDIUM / LOW)
- Reasoning trail

### Phase G — Pilot report

Pilot Orchestrator authors `STAGE4_PILOT_REPORT_<date>.md` with:

- All 33 agents' calibration grades
- All 1500 labels (per Phase B)
- All convergence metrics (Phase D)
- All adjudicated hands with reasoning trails (Phase F)
- All reviewer concerns + dispositions (Phase E)
- Highlighting agreement matrix (H1 ↔ H2 Jaccard per category)
- Disagreement-cluster analysis: which shape categories produced
  the most disagreement
- Recommendation: SCALE / REVISE / RE-PILOT

Owner reviews report. Decision authorisation:

- **SCALE:** owner greenlights full Stage 4 (~600 hands) with same
  protocol; pilot becomes baseline
- **REVISE:** owner directs prompt / KB / threshold revisions; pilot
  re-runs after revision
- **RE-PILOT:** owner directs full re-pilot with stratification or
  protocol changes

## Estimated execution time

[**ML-ARCHITECT REVIEW NEEDED:** parallelism limits affect total
time. Provisional estimates assuming high parallelism:]

| Phase | Agents in parallel | Estimated time |
|---|---|---|
| A — Calibration | 33 | 1-2 hours |
| B — Labelling | 15 | 4-6 hours |
| C — Highlighting | 6 | 1-2 hours |
| D — Convergence | 1 (orchestrator) | 30 min |
| E — Reviewer pass | 8 | 1-2 hours |
| F — Adjudication | 3 (sequential per hand for adjudicated set) | 2-4 hours |
| G — Pilot report | 1 | 1-2 hours |
| **TOTAL** | | **10-18 hours of compute time** |

Real-time may be longer if dispatches need to be staged for
concurrency limits. Owner / ml-architect to verify.

## Pilot orchestration agent brief template

When commissioning the Pilot Orchestrator agent:

```
You are the Pilot Orchestrator for Stage 4 Pilot. Your role is
sequencing + tracking + reporting; you do NOT label, highlight,
review, or adjudicate.

Read first:
- MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md (locked plan)
- STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md (this script's
  production version, post-finalisation)
- prompts/protocol_a_v3.1.md (= current v3.1)
- prompts/protocol_b_v1.0.md (post-DRAFT-finalisation)
- prompts/protocol_c_v1.0.md (post-DRAFT-finalisation)
- LABELLING_PIPELINE.md
- All Stage 4 stop-conditions (locked plan §4.3)

Execute Phases A through G in order.

For each phase: dispatch agents, collect outputs, apply stop
conditions, surface findings + decisions in real-time to a comms
doc that owner can review while pilot runs.

If any stop condition triggers HALT: STOP execution, surface to
owner via comms doc, do NOT proceed to next phase.

Provenance: every dispatched agent's output records its persona +
session-launch cwd + dispatch lineage.

Final output: STAGE4_PILOT_REPORT_<date>.md with all metrics +
recommendation.
```

[**ML-ARCHITECT REVIEW NEEDED:** brief template completeness;
specific tool restrictions for Pilot Orchestrator (read-only?
write to comms only? dispatch agents only?).]

## Author note

DRAFT v0.1. Structural framework + phase ordering + dispatch
mechanics locked-in. ML-judgment specifics (parallelism, ordering
trade-offs, brief templates, time estimates) flagged for ML-architect
review.

Production: `STAGE4_PILOT_ORCHESTRATION_v1.0.md` after content fill
+ reviewer pass + owner approval. Pilot does NOT execute until ALL
preconditions are GREEN + owner explicit greenlight.

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` — locked
  plan; pilot dispatch is locked-plan execution authorisation
- `prompts/stage4_drafts/protocol_b_composition_first_v0_1_DRAFT.md`
- `prompts/stage4_drafts/protocol_c_adversarial_elimination_v0_1_DRAFT.md`
- `STAGE5_RETRAIN_PROTOCOL_DRAFT_2026-04-26.md` — Stage 5 takes pilot
  output as input
- `STAGE6_HOLDOUT_TESTSET_DRAFT_2026-04-26.md` — held-out set must
  be locked before pilot dispatch (so it's not in pilot corpus)
- `LABELLING_PIPELINE.md` — calibration exam infrastructure
- `feedback_solver_findings.md` + `feedback_solver_aligned_sizing.md`
  — adjudication solver protocol
