---
date: 2026-04-26
author: general-purpose subagent acting as ml-architect (dedicated subagent unavailable)
derived_from: STAGE4_PILOT_ORCHESTRATION_DRAFT_2026-04-26.md
version: v1.0
review_chain:
  - orchestrator structural skeleton (DRAFT v0.1, 2026-04-26)
  - v1.0 fill (general-purpose subagent acting as ml-architect, this file)
  - independent reviewer pass — REQUIRED before pilot dispatch
  - owner final approval — REQUIRED before pilot dispatch
status: v1.0 (fill complete; pending independent reviewer pass + owner approval)
from: Stage 4 prep Wave 2 — Task 5
to: Owner · Independent reviewer · Pilot Orchestrator agent (when commissioned)
re: Stage 4 pilot orchestration script — concrete agent-dispatch sequence,
    parallelism limits, brief templates, time estimates, pre-dispatch
    prerequisites for the 33-agent pilot per locked Stage 4 plan
---

# Stage 4 Pilot Orchestration Script — v1.0

## Purpose

Per locked Stage 4 plan (`MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md`,
`ee3d9f5`), the pilot dispatches 33 agents across 5 roles:

- 15 labellers (3 protocols × 5 agents per protocol)
- 6 highlighters (H1 + H2, 3 each)
- 8 reviewers
- 3 adjudicators
- 1 pilot orchestrator (independent of all above)

This document is the v1.0 lock of the execution sequencing — who
dispatches whom, in what order, with what handoffs, with what
concurrency budget, with what time profile.

---

## PRE-DISPATCH PREREQUISITES

Pilot does NOT dispatch unless EVERY item below is GREEN. Equivalent
to the PRE-PILOT BUILD REQUIREMENT pattern in Protocol B/C v1.0.1
and the PRE-EVALUATION PREREQUISITES in Stage 6 Held-Out v1.0.3 —
this section is the gate.

| # | Prerequisite | Source of truth | Owner-gate |
|---|---|---|---|
| 1 | **Stage 6 held-out hash matches v1.0.3 lock** | `STAGE6_HOLDOUT_TESTSET_v1_0.md` §"Hash + lock" — recompute SHA256 over the hashed block; must match recorded `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5` (47652 bytes, v1.0.2 hash preserved through v1.0.3 since v1.0.3 edits are outside the hashed block) | YES |
| 2 | **Pilot 100-hand corpus disjoint from Stage 6 holdout** | Run the non-overlap check defined in Stage 6 §"Non-overlap verification" against the pilot 100; zero `(sorted(hero), sorted(board))` fingerprint matches | YES |
| 3 | **Pilot 100-hand corpus disjoint from 24-hand calibration manifest** | Same fingerprint scan against `review/calibration_situations.json` + 4 mirror/batch files (per Stage 6 v1.0.1 closure: 21 unique fingerprints) — zero matches | YES |
| 4 | **Protocol A v3.1 frozen + checksum recorded** | `prompts/gto_labeller_v3.1.md` SHA256 captured in pilot run report; no edits during pilot | YES |
| 5 | **Protocol B v1.0.1 sealed + labeller-facing artifact built** | `prompts/protocol_b_composition_first_v1_0.md` v1.0.1 reviewer-passed; `prompts/protocol_b_composition_first_v1_0_pilot.md` (verbatim-inlined Bucket taxonomy + Features + DO NOT Rules per Protocol B v1.0.1 PRE-PILOT BUILD REQUIREMENT) exists and reviewer-verified | YES |
| 6 | **Protocol C v1.0.1 sealed + labeller-facing artifact built** | `prompts/protocol_c_adversarial_elimination_v1_0.md` v1.0.1 reviewer-passed; `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md` built (same inlining requirement) and reviewer-verified | YES |
| 7 | **Stage 5 retrain protocol v1.0.1 sealed** | `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 reviewer-passed; provides downstream contract (118-column v2.4 = 59 raw + 59 attn_*) so labellers know what schema their output feeds | YES |
| 8 | **Task 4.5 logic hardening sealed** | PR #21 merged at `add2617` — STREET_NAME_MAP whitelist, `classify_hand` raises, cache-key + AH (PILOT GATE), audit-runner immutability — confirmed via `MAIN_TERMINAL_PR21_MERGED_TASK5_GREENLIGHT_2026-04-26.md` | YES |
| 9 | **QC pre-pilot sweep clean (Phase 5)** | QC standing roadmap Phase 5 sweep returns zero NEW HIGH/CRITICAL findings on the labelling pipeline; Phase 2 HIGH-1 (teaching renderer) status confirmed (parallel stream, not blocking pilot logic) | YES |
| 10 | **All 33 pilot agents pass blind calibration** | Phase A of this script — 20/24 + all 3 GTO-reversal hands correct on the 24-hand reference set | YES |
| 11 | **Solver options match `feedback_solver_aligned_sizing.md`** | Adjudication panel preconfigured with flop 25%/66%, turn 33%/75%, river 33%/75%/150% sizing options BEFORE adjudication phase opens | YES |
| 12 | **Pilot orchestrator session-launch cwd verified** | `~/river-rats-v2/` (project-local subagents accessible: gto-expert, ml-architect, reviewer); no `cd` outside the project tree per Tasks 4 / 4.2 lessons | YES |
| 13 | **Owner explicit greenlight** | Per locked plan §11 "execution authorisation, not design"; owner posts ack to comms doc | YES |

If ANY row is RED: pilot does NOT dispatch. Halt. Surface the failed
prerequisite to owner. Do NOT improvise.

---

## Pilot orchestrator agent role

The **Pilot Orchestrator** (1 agent) coordinates the dispatch of
the other 32. They do NOT label, highlight, review, or adjudicate.
Their role is sequencing + tracking + reporting.

Pilot Orchestrator session-launch cwd: `~/river-rats-v2/` so they
have access to all project-local subagents (gto-expert, ml-architect,
reviewer if applicable).

**Resolution of DRAFT v0.1 ML-architect flag (line 58-61):** Pilot
Orchestrator may be a **general-purpose subagent under an explicit
orchestrator persona** (consistent with the Stage 4 prep precedent
where ml-architect / gto-expert dedicated subagents have been
unavailable and general-purpose-with-persona has carried the work
under owner authorisation). Provenance must record this honestly in
every dispatch record (persona embedded, dedicated-subagent-status
flagged).

**Tool restrictions for the Pilot Orchestrator** (resolution of
DRAFT v0.1 line 257-259 flag):

- **Allowed:** Read (any project file), Write (only to `review/comms/`
  and `review/pilot_run_<date>/` artifacts the orchestrator owns),
  Edit (only files the orchestrator authored in the run directory),
  Bash (read-only verification — `git status`, `git log`, `ls`,
  `grep`, `wc`, `sha256sum`), agent dispatch (sub-agent calls per
  the dispatch sequence below)
- **Prohibited:** any write to `prompts/`, `river-rats-core/`,
  `training-data/`, `review/comms/MAIN_TERMINAL_*` (the orchestrator
  posts its OWN comms docs but does not edit upstream directives);
  any `git add` / `git commit` / `git push` / `gh pr create` (those
  belong to the builder, not the orchestrator); any `cd` outside
  `~/river-rats-v2/`

---

## Dispatch sequence

### Phase A — Calibration (parallel, 33 agents)

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

### Phase B — Action labelling (15 agents, batched parallel; 100 hands × 15 = 1500 label-records)

Pilot Orchestrator dispatches 15 labellers (5 Protocol-A + 5
Protocol-B + 5 Protocol-C). Each labeller receives the SAME 100-hand
stratified pilot corpus.

Each labeller returns 100 labels (one per hand) with reasoning
traces specific to their protocol.

Total labels collected: 15 × 100 = 1500 label-records.

**Parallelism resolution (resolution of DRAFT v0.1 line 97-100 flag):**

Recommended concurrency: **5 labellers in parallel**, dispatched in
**3 sequential batches by protocol** (Batch 1: 5× Protocol-A; Batch
2: 5× Protocol-B; Batch 3: 5× Protocol-C).

Reasoning:

1. **Anthropic API concurrency budget — UNCERTAIN at the exact
   rate-limit numerical level for this account.** [UNCERTAIN: this
   document was authored without live access to the account-tier
   rate-limit dashboard. Tier 1 default is on the order of 50 RPM /
   40k input TPM / 8k output TPM for Opus/Sonnet — well below what
   15 concurrent labelling agents (each making bursty multi-call
   sessions over the 100-hand corpus) would consume on a sustained
   basis. Tier 2-4 raises these substantially. Owner / builder must
   confirm the live tier before pilot dispatch.]
2. **Claude Code Network (CCN) concurrency budget.** Subagent
   dispatch from a single orchestrator is bottlenecked at the
   harness level — sustained 15-way parallel dispatch can starve
   the orchestrator's own tool budget and induce rate-limit
   backoffs that invisibly serialise. 5-way parallel within a
   batch keeps each agent's tool calls responsive and keeps the
   orchestrator's queue traceable.
3. **Provenance + debugging.** With 5-way batches per protocol,
   any rate-limit / schema-violation incident is contained inside
   one protocol's evidence pool — easier to diagnose, easier to
   re-dispatch, easier to surface to reviewer without confounding
   protocols.
4. **Total wall-time impact.** 3 sequential batches of 5-way
   parallel adds ~2× the wall-time of pure 15-way (assuming a
   labeller takes the same wall-time regardless of batch placement).
   At ~30 min per labeller on 100 hands (see §"Time estimates"),
   the difference is ~30 min vs ~90 min — small relative to total
   pilot wall-time, large gain in robustness.

**If Anthropic + CCN concurrency budgets confirmed at pilot
preflight to support 15-way parallel:** orchestrator may upgrade
to single-batch 15-way. Decision: orchestrator-level, surfaced to
owner in pre-dispatch readiness comms.

### Phase C — Highlighting (parallel; 6 agents; depends on Phase B + D)

Once Phase B labels collected AND Phase D consensus computed: Pilot
Orchestrator dispatches 6 highlighters in parallel (3 H1 + 3 H2).

Each highlighter receives:

- The 100-hand pilot corpus
- The cross-protocol consensus action label per hand (from Phase D
  3-of-3 majority; for hands routed to adjudication, the highlighter
  receives BOTH the disagreement-marker AND the per-protocol
  candidate set so they can highlight reasoning for the candidate
  set without picking winners)

H1 highlighters tag PRIMARY + CONFIRMED attention flags per Exp 3
auxiliary protocol. H2 highlighters tag intention multi-label per
Exp 4 protocol.

**Highlighter context-scope resolution (resolution of DRAFT v0.1
line 116-119 flag):**

Highlighters receive:
- Hand state (cards, board, action history, pot/SPR)
- Cross-protocol consensus action (Phase D output) — REQUIRED
- Per-protocol vote tally (e.g. "Protocol A: 5/5 BET; Protocol B:
  4/5 BET + 1 CHECK; Protocol C: 5/5 BET") — REQUIRED for
  calibrated attention to known-disputed factors
- Aggregate (concatenated, anonymised) reasoning text from ALL 15
  labellers — REQUIRED for H2 intent-tagging which depends on
  why-the-action-was-chosen, not what

Highlighters do NOT receive:
- Per-labeller attribution (which agent said what) — keeps
  highlighter independent from labeller-identity bias
- Calibration-exam scores per labeller — same independence reason
- Solver output — not yet generated at Phase C; solver is Phase F
  adjudication-only

**Trade-off explicit:** highlighter sees more context than a "pure
independence" design would allow (which would only show consensus
action), but less than full attribution (which would risk pulling
high-calibration labellers' reasoning preferentially). The middle
path matches the locked plan §3 "Highlighting is a separate pass
from action labelling (P6). Highlighter sees the consensus action
label as input and tags reasoning, not action choice."

### Phase D — Convergence analysis (Pilot Orchestrator solo)

Pilot Orchestrator computes:

- **Within-protocol κ** per protocol (3 separate κ values, one each
  for A/B/C)
- **Cross-protocol κ** per pair (3 pairs: A↔B, B↔C, A↔C)
- **3-of-3 cross-protocol agreement** count: hands where all 3
  protocols' majority action agree
- **Hands routed to adjudication:** where cross-protocol agreement
  is < 3-of-3 OR within-protocol κ for any protocol on that hand
  is anomalously low (<0.6 within-protocol on an isolated hand =
  intra-protocol disagreement — flag for adjudication even if
  cross-protocol majority is unanimous)

Compare against pre-registered stop conditions (locked plan §4.3):

| Metric | Threshold | Pilot decision |
|---|---|---|
| Within-protocol κ (each) | ≥ 0.75 | If miss: HALT pilot, prompt revision |
| Cross-protocol κ (any pair) | ≥ 0.60 | If miss: HALT, investigate via solver |
| 3-of-3 agreement | ≥ 70% of hands | If miss: KB has gaps |
| Hands to adjudication | ≤ 25% of pilot | If exceed: HALT, KB / prompt revision |
| H1 ↔ H2 highlight Jaccard | ≥ 0.50 | If miss: investigate |

If ALL thresholds met: PROCEED to Phase E + F.
If ANY threshold missed: HALT pilot, surface to owner, re-pilot.

**Phase D / Phase C ordering note:** Phase D MUST complete BEFORE
Phase C dispatches (highlighters need consensus action labels as
input). Phase D / Phase E / Phase F can overlap with each other —
see §"Phase B/C/D/E/F overlap" below.

### Phase E — Reviewer pass (parallel; 8 agents; depends on Phase B + D)

Pilot Orchestrator dispatches 8 reviewers in parallel:

- 3 reviewers spot-check Protocol-A reasoning traces (sample hands)
- 2 reviewers spot-check Protocol-B
- 2 reviewers spot-check Protocol-C
- 1 reviewer spot-checks H1 + H2 highlighting + audits Pilot
  Orchestrator's convergence analysis

Each reviewer returns concerns + recommendations. Pilot Orchestrator
incorporates recommendations into pilot report.

### Phase F — Adjudication (parallel; 3 agents; depends on Phase D)

For hands routed to adjudication (≤ 25% of pilot per stop condition):

Pilot Orchestrator dispatches 3 adjudicators per the locked Stage 4
panel:

- **GTO expert adjudicator** — reads all 15 labellers' reasoning
  traces; produces tiebreaker reasoning. NEVER sees solver output
  before producing reasoning (per `feedback_solver_vs_expert_labels.md`).
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

### Phase B/C/D/E/F overlap rules

Strict ordering edges (must serialise):
- A → B (calibration must clear before labelling)
- B → D (labels must exist for convergence)
- D → C (consensus must exist for highlighters)
- D → F (adjudication routing requires Phase D output)

Permitted overlaps:
- D + E may overlap: reviewers spot-check Phase B labels while
  orchestrator computes κ — reviewer findings can fold into the
  Phase G report regardless of κ outcome.
- C + F may overlap: highlighters work the consensus-set hands
  while adjudicators work the disputed-set hands; the two sets are
  disjoint by construction.
- E + F may overlap: reviewers and adjudicators look at different
  artifacts (reasoning traces vs disputed-hand resolution).

NOT permitted to overlap:
- B + D (labels still landing while κ being computed = κ on
  incomplete data; orchestrator must wait for all 1500 records
  before invoking κ math).
- D + (C or F) (consensus must exist before highlighters or
  adjudicators dispatch — both depend on Phase D's routing
  decisions).

---

## Concurrency / queue logic

### Labelling-phase batching

100 hands × 3 protocols = 300 unique (hand, protocol) pairs to
label. With 5 labellers per protocol, each labeller does all 100
hands → 100 calls per labeller × 15 labellers = 1500 label calls
total.

**Batch dispatch pattern:**

```
Batch 1 (Protocol A):  5 labellers in parallel × 100 hands each = 500 calls
Batch 2 (Protocol B):  5 labellers in parallel × 100 hands each = 500 calls
Batch 3 (Protocol C):  5 labellers in parallel × 100 hands each = 500 calls
```

Within each batch, the orchestrator dispatches 5 labeller subagents.
Each labeller iterates internally over 100 hands sequentially (one
hand per call within the labeller's session).

### Failure handling policy

| Failure mode | Detection | Retry | Escalate-after |
|---|---|---|---|
| Anthropic 429 (rate limit) | API error code | Exponential backoff: 30s, 60s, 120s, 240s | 4 retries — then degrade to next batch (don't queue indefinitely) |
| Anthropic 5xx (transient) | API error code | Linear retry: 30s, 30s, 30s | 3 retries — then mark labeller-output as INCOMPLETE, re-dispatch a replacement labeller for the slot |
| Agent-internal-error (subagent crash, persona drift, refusal) | Subagent returns error or empty payload | Re-dispatch the same labeller with same input ONCE | 1 retry — then mark slot INCOMPLETE, escalate to owner via comms doc |
| Schema-violation (output missing required JSON fields, malformed reasoning trace, banned-action tag) | Orchestrator's per-record validator | Re-dispatch the same labeller asking for schema-compliant output, attaching the schema spec | 2 retries — then mark record DROP, log to per-protocol failure tally |
| Calibration-failed labeller (Phase A pass criterion miss) | Phase A grading | Replace with fresh labeller dispatch | After 2 replacements per slot fail: HALT pilot per Phase A "4+ fail" outcome |

**Per-labeller record discipline:** each labeller's 100 outputs
land in `review/pilot_run_<date>/labels/protocol_<a|b|c>/agent_<n>/`
as one file per hand. Schema-violations flagged at write-time, not
at end-of-batch — reduces rework.

### Cost tracking

Per-call cost target ranges (UNCERTAIN — depends on model selection
+ input length + reasoning trace length):

| Cost component | Per-label estimate | Per-phase total | Notes |
|---|---|---|---|
| Phase A (calibration) | 33 agents × 24 hands × ~$0.02-$0.10/hand | ~$15-$80 | [UNCERTAIN: per-call cost depends on Opus vs Sonnet selection + reasoning-trace verbosity. Sonnet 4.5 ~5× cheaper than Opus 4.7 per equivalent token.] |
| Phase B (labelling) | 1500 calls × ~$0.05-$0.25/call | ~$75-$375 | Largest cost component. Reasoning-trace heavy. |
| Phase C (highlighting) | 6 agents × 100 hands × ~$0.04-$0.20/hand | ~$24-$120 | H2 multi-label intent tags shorter than H1 attention flags. |
| Phase D (convergence) | Orchestrator-internal (Python kappa math, no model calls) | ~$0 | |
| Phase E (reviewer pass) | 8 agents × spot-check ~10 hands × ~$0.10-$0.40/hand | ~$8-$32 | Reviewer reads reasoning traces, narrower output. |
| Phase F (adjudication) | 3 agents × ~25 adjudicated hands × ~$0.20-$1.00/hand | ~$15-$75 | Solver-verify operator's wall-time cost is solver compute, not API. |
| Phase G (pilot report) | 1 agent × ~$5-$20 | ~$5-$20 | Long-context synthesis. |
| **Total pilot run** | | **~$140-$700** | [UNCERTAIN: full range depends on tier selection + model mix. Owner / builder confirms budget envelope before dispatch.] |

Cost telemetry: orchestrator records per-call $ + token usage at
write-time alongside each label record. Per-phase aggregate posted
to comms doc at phase boundaries.

---

## Time estimates

[UNCERTAIN: per-call latency baseline. The codebase contains
labelling artifacts (e.g. `GTO_EXPERT_AGENT1_FB01_FB10_2026-04-12.md`,
Pass 1 385-hand label runs) but no recorded per-call wall-time
measurements — these were authored during single-shot agent
sessions where wall-time was not instrumented. Estimates below
assume per-call latency consistent with Opus/Sonnet 4.7 reasoning-
heavy responses observed in prior comms-doc fill-ins (Tasks 1-4
of Stage 4 prep): ~30-90s per label call including reasoning trace
generation. Owner / builder MUST instrument the first 5 labelling
calls of Phase B and re-validate this estimate before allowing the
remaining 1495 calls to dispatch — if observed latency >2× the
estimate, halt + re-plan.]

| Phase | Agents in parallel | Per-agent work | Estimated wall-time |
|---|---|---|---|
| A — Calibration | 33 (single batch) | 24 hands × ~60s = ~24 min | **~30 min** (incl. orchestrator grading) |
| B — Labelling | 5 per batch × 3 sequential batches | 100 hands × ~60s = ~100 min per labeller | **~5-6 h** (3 batches × ~100 min + dispatch overhead) |
| C — Highlighting | 6 (single batch) | 100 hands × ~30s (shorter than full label) = ~50 min | **~1 h** |
| D — Convergence | 1 (orchestrator, Python math) | κ + agreement matrix computation | **~30 min** |
| E — Reviewer pass | 8 (single batch) | spot-check ~10 hands × ~120s reasoning = ~20 min per reviewer | **~30-45 min** |
| F — Adjudication | 3 (sequential per hand for the adjudicated set; the 3 roles serialise within a hand but parallelise across the ~25 adjudicated hands) | ~25 hands × ~5 min/hand (3 roles serial: GTO reasoning ~2 min + solver ~2 min + writer ~1 min) | **~2 h** (assuming 25 adjudicated hands; scales linearly with adjudication count) |
| G — Pilot report | 1 | Full synthesis | **~1-2 h** |
| **TOTAL wall-time** | | | **~10-13 h** |

**Comparison to DRAFT v0.1 estimate:** DRAFT estimated 10-18 h.
v1.0 narrows to 10-13 h based on:
- Phase B refined to 3-batch sequential×5-parallel pattern (matches
  CCN concurrency reality more closely than 15-way single-batch
  aspiration)
- Phase A reduced to ~30 min (33-way parallel calibration is short
  per-agent because the 24-hand exam is bounded; the bottleneck is
  orchestrator grading, not subagent compute)
- Phase E reduced to ~30-45 min (reviewer spot-checks are bounded
  to ~10 hands each)

**Real-time vs compute-time:** the table above is wall-time of the
full pilot run assuming continuous orchestrator availability. If
orchestrator session is paused (owner review of intermediate
findings, debugging a failed batch, etc.), real-time extends.
Plan a 1-2 day calendar window for pilot dispatch + report; the
~10-13 h compute fits in one long working day under continuous
attention.

---

## Brief templates

### Brief template — Labeller (Protocol A)

```
You are a Stage 4 pilot LABELLER under PROTOCOL A (KB-first, current
v3.1 lineage).

Persona: gto-expert (general-purpose subagent acting as gto-expert
under owner authorisation if dedicated subagent unavailable).

Read first (ALL):
- prompts/gto_labeller_v3.1.md (your full labelling prompt — the
  canonical Protocol A artifact; bucket taxonomy, features, DO NOT
  Rules, all worked examples)
- LABELLING_PIPELINE.md (output schema reference)

Input you will receive:
- 100 hands from the Stage 4 pilot corpus, in JSONL with hand_id,
  hero cards, board, action history, pot, SPR, position, stack
  depth, opponent count

For each hand, produce:
- One action label (FOLD / CHECK / CALL / BET_<size> / RAISE_<size>)
  per the v3.1 sizing taxonomy (MUST match `feedback_solver_aligned_sizing.md`:
  flop 25%/66%, turn 33%/75%, river 33%/75%/150%; opening bets use
  BET_<size>, raises of an existing bet use RAISE_<size>)
- Bucket assignment (per v3.1 §Bucket taxonomy)
- Reasoning trace following Protocol A's KB-first structure: identify
  the KB anchor (or "no anchor — first-principles reasoning"), apply
  the anchor's logic, document any deviations
- Confidence band (HIGH / MEDIUM / LOW)

Output one JSON record per hand to:
review/pilot_run_<date>/labels/protocol_a/agent_<your_slot>/<hand_id>.json

Schema: {hand_id, action, bucket, reasoning, kb_anchor, confidence}

Provenance: include persona-acknowledgement + dedicated-subagent-
status in your first output record.

Rules:
- NEVER ask the orchestrator clarifying questions during labelling
  (you are dispatched as a sealed agent; clarifications go to
  Phase E reviewer)
- NEVER reason about the solver — Protocol A is KB-first; solver
  is Phase F adjudication only
- NEVER use 'raise' for an opening bet (per `feedback_terminology_raise_vs_bet.md`)
```

### Brief template — Labeller (Protocol B — composition-first)

Same skeleton as Protocol A above, with these substitutions:
- Read first: `prompts/protocol_b_composition_first_v1_0_pilot.md`
  (the v1.0.1 labeller-facing artifact with verbatim-inlined Bucket
  taxonomy + Features + DO NOT Rules)
- Reasoning trace structure: composition-first per Protocol B §"Step
  1/2/3" — derive villain composition slices (TP+ / draws / air),
  pick action from the triple, justify
- Output path: `review/pilot_run_<date>/labels/protocol_b/agent_<your_slot>/<hand_id>.json`

### Brief template — Labeller (Protocol C — adversarial elimination)

Same skeleton as Protocol A above, with these substitutions:
- Read first: `prompts/protocol_c_adversarial_elimination_v1_0_pilot.md`
  (the v1.0.1 labeller-facing artifact)
- Reasoning trace structure: adversarial-elimination per Protocol
  C §"Step 1/2/3" — enumerate candidate actions, build case AGAINST
  each (RAISE sizings: 33% or 66% pot-relative per
  `feedback_solver_aligned_sizing.md` — NOT facing-bet multiples),
  rank by elimination weakness, return survivor
- Output path: `review/pilot_run_<date>/labels/protocol_c/agent_<your_slot>/<hand_id>.json`

### Brief template — Convergence checker (= Pilot Orchestrator solo)

The orchestrator runs the convergence math itself (no subagent
dispatch). Pseudocode:

```
INPUT:
  labels = load 1500 records from review/pilot_run_<date>/labels/**/*.json

  # Validate schema, drop SCHEMA_VIOLATION records, log dropped
  # IDs to per-protocol failure tally
  validated_labels = [r for r in labels if validate_schema(r)]

PER-HAND COMPUTATION (for each of 100 hands):
  hand_labels = group_by_hand(validated_labels)
  for hand_id in hands:
    a_votes = [r.action for r in hand_labels[hand_id] if r.protocol == 'A']
    b_votes = [r.action for r in hand_labels[hand_id] if r.protocol == 'B']
    c_votes = [r.action for r in hand_labels[hand_id] if r.protocol == 'C']
    a_majority = mode(a_votes); b_majority = mode(b_votes); c_majority = mode(c_votes)
    within_proto_kappa[hand_id] = {
      'A': fleiss_kappa(a_votes),
      'B': fleiss_kappa(b_votes),
      'C': fleiss_kappa(c_votes),
    }
    cross_proto_3of3[hand_id] = (a_majority == b_majority == c_majority)

AGGREGATE COMPUTATION:
  within_kappa_per_proto = {
    'A': cohen_kappa_aggregate(all_a_records),
    'B': cohen_kappa_aggregate(all_b_records),
    'C': cohen_kappa_aggregate(all_c_records),
  }
  cross_kappa_pairs = {
    'A_B': cohen_kappa(majority_a_per_hand, majority_b_per_hand),
    'B_C': cohen_kappa(majority_b_per_hand, majority_c_per_hand),
    'A_C': cohen_kappa(majority_a_per_hand, majority_c_per_hand),
  }
  three_of_three_pct = sum(cross_proto_3of3.values()) / 100

ROUTING:
  hands_to_adjudication = [
    h for h in hands
    if not cross_proto_3of3[h]
    or any(within_proto_kappa[h][p] < 0.6 for p in 'ABC')
  ]

OUTPUT:
  review/pilot_run_<date>/convergence_report.json
  Schema: {within_kappa_per_proto, cross_kappa_pairs, three_of_three_pct,
           hands_to_adjudication: [hand_ids], stop_condition_status: {...}}
```

### Brief template — Highlighter H1 (auxiliary attention flags)

```
You are a Stage 4 pilot HIGHLIGHTER (H1 — Exp 3 auxiliary attention
flags).

Persona: ml-architect (general-purpose subagent acting as ml-architect
under owner authorisation if dedicated subagent unavailable).

Read first (ALL):
- review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md (this script —
  §"Phase C — Highlighting" for context-scope rules)
- prompts/gto_labeller_v3.1.md §Features (the 55-feature vector
  + post-commit-14 multiway promotions = 59 raw features per Stage 5
  retrain v1.0.1)
- The Exp 3 attention vocabulary spec (orchestrator provides at
  dispatch — separate file referenced by Stage 5 retrain v1.0.1)

Input you will receive:
- 100 hands from the pilot corpus
- Cross-protocol consensus action per hand (Phase D output)
- Per-protocol vote tally per hand
- Aggregate (anonymised, concatenated) reasoning text from all 15
  labellers per hand

For each hand, produce:
- PRIMARY attention flags: features whose value DROVE the action
  choice (per the aggregate reasoning)
- CONFIRMED attention flags: features whose value RULED OUT
  alternative actions (per the aggregate reasoning)

Output one JSON record per hand to:
review/pilot_run_<date>/highlighting/h1/agent_<your_slot>/<hand_id>.json

Schema: {hand_id, primary_flags: [feature_keys], confirmed_flags: [feature_keys]}

Rules:
- NEVER tag a feature that is not in the 59-feature vocabulary
  (the v2.4 contract is locked at 59 raw + 59 attn_*)
- NEVER tag based on per-labeller attribution (you don't see
  attribution; if you think you do, halt and surface to orchestrator)
- NEVER tag based on solver output (solver is Phase F)
- DO use the cross-protocol vote tally to calibrate attention to
  disputed factors (3-of-3 unanimous → high-confidence flag set;
  mixed votes → narrower / lower-confidence flag set)
```

### Brief template — Highlighter H2 (intent multi-label)

Same skeleton as H1 above, with these substitutions:
- Output: multi-label binary intent tags per Exp 4 protocol
  (`intent_value_extract`, `intent_pot_control`,
  `intent_bluff_catch`, `intent_protect_equity`, etc. — full
  vocabulary in the orchestrator-provided Exp 4 spec)
- Output path: `review/pilot_run_<date>/highlighting/h2/agent_<your_slot>/<hand_id>.json`
- Schema: `{hand_id, intents: {intent_value_extract: bool, ...}}`

### Brief template — Reviewer

```
You are a Stage 4 pilot REVIEWER.

Persona: reviewer (general-purpose subagent acting as reviewer
per `feedback_review_autosave.md` — write to review/pilot_run_<date>/
reviews/ without asking; the orchestrator will integrate findings
into the Phase G report).

Read first (ALL):
- review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md (this script —
  §"Phase E" for your scope)
- The protocol prompt for your assigned protocol (Protocol A v3.1,
  Protocol B v1.0.1, or Protocol C v1.0.1)

Input you will receive:
- Your assigned scope (which protocol's traces to spot-check, OR
  the H1+H2 highlighting + Phase D audit slot)
- 10 randomly-sampled hands' worth of reasoning traces from the
  assigned scope

Produce: `review/pilot_run_<date>/reviews/reviewer_<your_slot>.md`
with:
- Concerns (HIGH / MEDIUM / LOW / NIT, per `feedback_comms_folder.md`
  + `feedback_review_autosave.md` discipline)
- Recommendations (specific, actionable; cite hand IDs)
- Overall verdict (APPROVE / APPROVE-WITH-NITS / REQUEST-CHANGES /
  HALT-PILOT)

Rules:
- NEVER edit labels yourself (you are reviewer, not labeller)
- NEVER consult solver output (solver is Phase F adjudicator's tool)
- ALWAYS verify the actual source artifact — don't trust an upstream
  summary (per `feedback_verify_source_not_plan.md`)
```

### Brief template — Adjudicator (3 roles, sequential per hand)

```
You are one of three Stage 4 pilot ADJUDICATORS for the disputed-
hand set.

Roles (the orchestrator dispatches you as ONE of these three; do
NOT try to do all three roles):

1. GTO expert adjudicator (gto-expert persona)
   - Read all 15 labellers' reasoning traces for the assigned hand
   - Produce tiebreaker reasoning + tentative action
   - NEVER consult solver output before producing reasoning (per
     `feedback_solver_vs_expert_labels.md`)

2. Solver-verify operator (programmer persona)
   - Run solver on the assigned spot per
     `feedback_solver_aligned_sizing.md` sizing options (flop 25%/
     66%, turn 33%/75%, river 33%/75%/150%)
   - Produce solver action distribution
   - Do NOT interpret — the writer integrates

3. Adjudication writer (gto-expert persona, fresh dispatch)
   - Combine GTO reasoning + solver output → final label
   - Output one of: action label (with confidence band) OR
     "AMBIGUOUS, DROP from training"

Output path:
review/pilot_run_<date>/adjudication/<hand_id>/{role}.json

Schema (final-writer record):
{hand_id, final_action, confidence_band, reasoning_trail}

Provenance: roles 1 and 3 must be DIFFERENT subagent dispatches
(reviewer ≠ author; same-agent-doing-both = independence violation).
```

### Brief template — Pilot Orchestrator (top-level)

```
You are the Pilot Orchestrator for Stage 4 Pilot. Your role is
sequencing + tracking + reporting; you do NOT label, highlight,
review, or adjudicate.

Persona: orchestrator (general-purpose subagent under explicit
orchestrator persona; dedicated subagent unavailable per Stage 4
prep precedent).

Session-launch cwd: ~/river-rats-v2/ (do NOT cd outside this tree
per Tasks 4 / 4.2 incident lessons; use absolute paths for all
file operations)

Read first (ALL):
- review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md (this script,
  including PRE-DISPATCH PREREQUISITES — verify ALL 13 prereqs are
  GREEN before starting Phase A)
- review/comms/MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md
  (locked plan)
- prompts/gto_labeller_v3.1.md (Protocol A artifact)
- prompts/protocol_b_composition_first_v1_0_pilot.md (labeller-facing
  Protocol B artifact, post-build-step)
- prompts/protocol_c_adversarial_elimination_v1_0_pilot.md (labeller-
  facing Protocol C artifact, post-build-step)
- review/comms/STAGE5_RETRAIN_PROTOCOL_v1_0.md (downstream contract:
  118-column v2.4 = 59 raw + 59 attn_*)
- review/comms/STAGE6_HOLDOUT_TESTSET_v1_0.md (held-out hash-lock
  for prereq #1)
- LABELLING_PIPELINE.md (calibration exam infrastructure)
- All Stage 4 stop-conditions (locked plan §4.3)

Tool restrictions: read any project file; write only to
review/comms/ (your own posts) and review/pilot_run_<date>/
(your run artifacts); bash read-only verification only; agent
dispatch per the brief templates in §"Brief templates"; NO git
commit / push / PR (builder territory); NO cd outside the project.

Execute Phases A through G in order, respecting the overlap rules
in §"Phase B/C/D/E/F overlap rules".

For each phase:
- Dispatch agents per the brief templates
- Collect outputs to review/pilot_run_<date>/<phase>/...
- Apply stop conditions (Phase D thresholds, Phase A pass criterion)
- Surface findings + decisions IN REAL TIME to a comms doc named
  review/comms/STAGE4_PILOT_RUN_<date>_STATUS.md so owner can
  review while pilot runs

If any stop condition triggers HALT: STOP execution, surface to
owner via the status comms doc, do NOT proceed to next phase.

Provenance: every dispatched agent's output records its persona +
session-launch cwd + dispatch lineage + dedicated-subagent-status.

Final output: review/comms/STAGE4_PILOT_REPORT_<date>.md per
§"Phase G — Pilot report" with all metrics + recommendation.
```

---

## Author note

v1.0 fill complete. Structural framework + phase ordering preserved
from DRAFT v0.1; the 6 ML-architect-flagged content items
(parallelism, ordering, brief templates, time estimates, orchestrator
tool restrictions, persona requirement) resolved in this revision.

PRE-DISPATCH PREREQUISITES section added (analog to Protocol B/C
PRE-PILOT BUILD REQUIREMENT and Stage 6 PRE-EVALUATION
PREREQUISITES) — this is the gate that converts the design
artifact into an executable plan.

Per Task 5 lessons-applied analog:
- Task 1 (worked self-consistency): brief templates cross-reference
  internal §s and external standing specs consistently
- Task 2 (memory references aligned): solver sizings cited as
  `feedback_solver_aligned_sizing.md` flop 25%/66% / turn 33%/75% /
  river 33%/75%/150% throughout; terminology raise-vs-bet cited
- Task 3 (infrastructure matches current state): Stage 5 retrain
  v1.0.1 118-column contract (59 raw + 59 attn_*) cited as the
  downstream schema labellers feed; Task 4.5 PR #21 merge `add2617`
  cited as PILOT GATE clearance source
- Task 4 (numerical/statistical rigour): time estimates derive from
  cited per-call latency assumption (~30-90s) and acknowledge
  UNCERTAIN-ness; cost estimates show ranges with the dependency
  variables called out; pre-flight 5-call latency validation step
  added so the estimate gets re-validated before the bulk dispatch
- Task 4.5 (whitelist-or-raise discipline): tool restrictions for
  Pilot Orchestrator are whitelist (allowed list explicit, prohibited
  list explicit); failure-handling policy enumerates 5 modes with
  retry+escalate behaviour rather than open-ended "retry on error"

Production: this v1.0 file goes to independent reviewer pass next
(REQUIRED before pilot dispatch), then owner final approval. Pilot
does NOT execute until ALL 13 PRE-DISPATCH PREREQUISITES are GREEN
+ owner explicit greenlight.

---

## Reference

- `MAIN_TERMINAL_STAGE4_STRATEGY_PROPOSAL_2026-04-25.md` (`ee3d9f5`) — locked
  plan; pilot dispatch is locked-plan execution authorisation
- `prompts/protocol_b_composition_first_v1_0.md` (v1.0.1 sealed)
- `prompts/protocol_c_adversarial_elimination_v1_0.md` (v1.0.1 sealed)
- `prompts/gto_labeller_v3.1.md` (Protocol A canonical)
- `STAGE5_RETRAIN_PROTOCOL_v1_0.md` (v1.0.1 sealed) — Stage 5 takes
  pilot output as input; defines 118-column v2.4 contract
- `STAGE6_HOLDOUT_TESTSET_v1_0.md` (v1.0.3 sealed) — held-out set
  hash must be GREEN before pilot dispatch (so it's not in pilot
  corpus) AND pilot 100 must be disjoint from holdout 50
- `LABELLING_PIPELINE.md` — calibration exam infrastructure
- `MAIN_TERMINAL_PR21_MERGED_TASK5_GREENLIGHT_2026-04-26.md` — Task
  4.5 logic hardening sealed at `add2617`; PILOT GATE clearance
- `MAIN_TERMINAL_BUILDER_STAGE4_PREP_TASKS_2026-04-26.md` — original
  Stage 4 prep directive; this file is the Task 5 v1.0 deliverable
- `feedback_solver_findings.md` + `feedback_solver_aligned_sizing.md`
  — adjudication solver protocol
- `feedback_solver_vs_expert_labels.md` — solver verifies/researches
  only; never used as training labels (adjudicator role 1 must
  produce reasoning BEFORE seeing solver per role 2)
- `feedback_terminology_raise_vs_bet.md` — opening bet = BET; raise
  of existing bet = RAISE
- `feedback_attention_flags_when_features_change.md` — Exp 3
  auxiliary attention vocabulary discipline (H1 brief)
- `feedback_review_autosave.md` + `feedback_comms_folder.md` —
  reviewer write-discipline (Phase E briefs)
- `feedback_verify_source_not_plan.md` — reviewer must verify
  source, not plan
- `feedback_no_deadlines.md` — quality over speed; HALT on stop-
  condition miss, do not improvise around the threshold
