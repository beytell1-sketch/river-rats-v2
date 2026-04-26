---
date: 2026-04-26
from: Pilot Orchestrator (general-purpose subagent under Pilot Orchestrator persona; dedicated subagent unavailable per Stage 4 spec v1.0.3 §"Resolution of DRAFT v0.1 ML-architect flag")
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase A.1-A7 preflight — initial status comm; A.5 PRE-CALIBRATION GATE PASS (all 5 partial-fold MW fixtures honor live-villain rule); A.1/A.2 require operator inputs; A.3 latency probe + A.4 calibration ready to dispatch on operator confirmation; A.6 + A.7 staged
status: PHASE A IN PROGRESS — A.5 PRE-CALIBRATION GATE PASS; awaiting operator inputs on A.1 (API tier) + A.2 (model selection lock confirmation) + cost-authorization confirmation for A.4 (~$25-$130 envelope) before progressing to A.3/A.4
session_persona: Pilot Orchestrator (reactivated this turn at ~19:55 SAST per orchestrator MERGE ACK eaefc2a); builder role suspended for pilot run unless code-side fix-forward required
session_cwd: ~/river-rats-v2/ (Stage 4 spec v1.0.3 prereq #12 GREEN)
---

# Pilot Phase A — initial status

## Persona transition + setup

Persona switched from logic builder to Pilot Orchestrator at ~19:55 SAST (this turn, immediately after BUILDER_BUILDS_ABCD_COMPLETE landed at `dfd8925`). Tool restrictions per Stage 4 spec v1.0.3 §"Tool restrictions for the Pilot Orchestrator" now in effect:

- **Allowed:** Read, Write (`review/comms/` + `review/pilot_run_2026-04-26/` only), Edit (own files only), Bash (read-only verification + persona-required setup like `mkdir review/pilot_run_<date>/`), agent dispatch
- **Prohibited:** writes to `prompts/`, `river-rats-core/`, `training-data/`, `MAIN_TERMINAL_*` files; any `git add` / `git commit` / `git push` / `gh pr create` (those belong to the builder persona, transiently reactivated for git ops only); any `cd` outside `~/river-rats-v2/`

Pilot run directory created: `review/pilot_run_2026-04-26/` (currently empty; will hold run artifacts as phases progress).

## Spec-vs-MERGE-ACK ordering clarification

Stage 4 spec v1.0.3 §"Phase B/C/D/E/F overlap rules" §"Strict ordering edges (must serialise)" lines 488-489:

> "A-preflight → A (HIGH-1 / S-A12 5-hand partial-fold MW fixture verification must clear before the 33-agent calibration exam runs)"

And lines 517-519:

> "NOT permitted to overlap: A-preflight + A (preflight is a sequential gate; if it FAILs, no calibration runs)"

The orchestrator MERGE ACK (`eaefc2a` at 19:50) presents Phase A in numerical order A.1→A.7 with A.4 calibration listed before A.5 fixture preflight. Reading the MERGE ACK alongside the spec, **the spec's "preflight before calibration" sequencing is the actual execution order** — the MERGE ACK's "(some can parallel; A.4 calibration is blocking before A.5)" wording appears to mean "A.4 is a blocker phase" not "A.4 precedes A.5 in execution order" (the spec explicitly lists fixture preflight as a sequential gate before calibration).

**Pilot Orchestrator execution order adopted (per spec v1.0.3):**

1. **A.5** (5-hand partial-fold MW fixture verification) — DONE this turn (PASS, see below)
2. **A.1** (API tier verification) — operator-fillable
3. **A.2** (Model selection lock) — operator-fillable / orchestrator pre-specified
4. **A.6** (Cost telemetry baseline) — orchestrator-recordable (in progress)
5. **A.3** (5-call latency probe) — Pilot Orchestrator dispatches subagent (small cost ~$0.25)
6. **A.4** (28-hand calibration) — Pilot Orchestrator dispatches 33-agent parallel batch (~$25-$130; ~38 min wall-time)
7. **A.7** (Phase A summary report + GO/NO-GO) — composed at completion

Surface this ordering interpretation to orchestrator: if intended order differs, orchestrator may correct via comms doc and Pilot Orchestrator will re-sequence.

## A.5 — PRE-CALIBRATION GATE — PASS

**Fixture source:** `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl` (Build D v1.0.1 output)

**Hash verification:**
- Expected SHA256 (per `.lock.json`): `98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319`
- Actual SHA256 (computed at preflight): `98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319`
- **Match: True** ✓

**Per-fixture live-villain selection assertion (HIGH-1 / S-A12 close):**

| Fixture | Street | Hero pos | Live villains | Folded positions | `_villain_pos_raw` | (a) num_opp match | (b) ≥1 fold | (c) live ∩ folded = ∅ | (d) `_villain_pos_raw` is live | Verdict |
|---------|--------|----------|---------------|------------------|---------------------|--------------------|--------------|------------------------|---------------------------------|---------|
| phase_a5_pf_001 | flop | HJ | UTG, CO, BB | BTN, SB | UTG | True (3==3) | True (2 folds) | True | True | PASS |
| phase_a5_pf_002 | turn | BTN | HJ, CO | BB, SB, UTG | HJ | True (2==2) | True (3 folds) | True | True | PASS |
| phase_a5_pf_003 | turn | BTN | CO | BB, HJ, SB | CO | True (1==1) | True (3 folds) | True | True | PASS |
| phase_a5_pf_004 | flop | SB | HJ, BTN, BB | CO | HJ | True (3==3) | True (1 fold) | True | True | PASS |
| phase_a5_pf_005 | river | CO | HJ, BTN | BB, SB | HJ | True (2==2) | True (2 folds) | True | True | PASS |

**A.5 RESULT: PASS — all 5 fixtures honor live-villain selection rule.** No HALT triggered; preflight gate clear; A.4 calibration may dispatch on operator confirmation.

**Diversity coverage validated at preflight:**
- Streets: flop=2, turn=2, river=1 (matches Build D directive recommendation)
- Folded positions: BTN, SB, UTG, BB, HJ, CO — all 6 unique positions covered across 5 fixtures
- Live villain count: 1-live=1 (pf_003), 2-live=2 (pf_002, pf_005), 3-live=2 (pf_001, pf_004)

PRE-DISPATCH PREREQUISITES row #16 GREEN ✓ (was already pre-validated at Build D commit; runtime preflight re-confirmed).

## A.1 — API tier verification — OPERATOR INPUT REQUIRED

Per Stage 4 spec v1.0.3 PRE-DISPATCH PREREQUISITES row #14:

> "Anthropic API tier confirmed — Tier ≥ X for Phase B 5-way × 3-batch parallelism (verifiable via live tier check OR rate-limit headers from a 5-call preflight). At Tier 1 default (~50 RPM / 40k input TPM / 8k output TPM) the 5-way batch fits with margin; at higher tiers orchestrator may upgrade to single-batch 15-way per §'Parallelism limits' decision rule. Drives wall-time envelope (10-13h baseline)."

**Owner ask:** What is the current Anthropic API tier for the account driving this session?

- **Tier 1** (default): supports 5-way × 3-batch protocol-grouped parallelism per spec §"Parallelism resolution" point 1; total Phase B wall-time ~90 min instead of ~30 min single-batch
- **Tier 2-4**: orchestrator may upgrade to single-batch 15-way (saves ~60 min Phase B); confirm tier ≥ 2 unlocks this path

**Default assumption** (if no operator response by A.4 dispatch time): **Tier 1**. Phase B will run 5-way × 3-batch sequential by protocol per spec §"Parallelism resolution".

A.3 5-call latency probe will independently observe rate-limit headers as a secondary tier-confirmation signal.

## A.2 — Model selection lock — ORCHESTRATOR PRE-SPECIFIED

Per orchestrator MERGE ACK (`eaefc2a` line 81):

> "A.2 | Model selection lock (Opus 4.6/4.7 high-stakes; Sonnet labeller) | 2 min"

**Pilot Orchestrator interprets the orchestrator pre-specification as:**

| Role | Model | Rationale (from spec v1.0.3 PRE-DISPATCH row #15) |
|------|-------|---------------------------------------------------|
| Labeller (15 agents × A/B/C protocols) | Sonnet 4.6 | Volume-heavy work; Sonnet 5× cheaper than Opus per token; protocol fidelity tested at calibration |
| Highlighter (6 agents H1+H2) | Opus 4.7 | Judgment-heavy attention/intent tagging; higher reasoning depth needed |
| Reviewer (8 agents) | Opus 4.7 | Spot-check + concern surface; reasoning-trace audit needs depth |
| Adjudicator (3 agents: GTO + solver-verify + writer) | Opus 4.7 | Final-label disputes; highest stakes; per `feedback_solver_vs_expert_labels.md` GTO adjudicator NEVER sees solver before producing reasoning |
| Pilot Orchestrator | Opus 4.7 (1M context) | Cross-phase synthesis; multi-agent dispatch coordination |

**Owner confirmation requested** before A.4 dispatch: confirm this lock OR provide alternate per-role model selection.

**Default assumption** (if no operator response by A.4 dispatch time): the above lock per orchestrator pre-specification.

Cost envelope estimate at this lock (per spec §"Cost tracking"):
- Phase A: ~$25-$130
- Phase B: ~$75-$375 (Sonnet for labeller; largest single Phase but Sonnet keeps in lower band)
- Phase C: ~$24-$120
- Phase D: ~$0
- Phase E: ~$8-$32
- Phase F: ~$15-$75
- Phase G: ~$5-$20
- **Total pilot run: ~$140-$700** envelope per spec, with Sonnet labeller skewing toward lower band

## A.3 — 5-call latency probe — STAGED

**Plan:** Pilot Orchestrator dispatches a single subagent under "latency probe operator" persona to make 5 sequential Anthropic API calls (Opus 4.7) on representative reasoning-trace prompts (~3K input + ~2K output each), recording per-call wall-time. Subagent returns p50 + p95 latency + token counts.

**Cost:** ~5 × $0.05 = ~$0.25 (negligible).

**Halt condition** (per orchestrator MERGE ACK §"Halt conditions" + spec §"Phase A — Calibration"):
- **HARD halt** if A.3 p95 > 120s (rate-limit indicator OR backend degradation)

**Dispatch trigger:** post operator confirmation on A.1 + A.2 (or by default if operator silent and Pilot Orchestrator proceeds per autonomous-advance authority).

## A.4 — 28-hand calibration — STAGED (33-agent parallel)

**Plan:** Pilot Orchestrator dispatches 33 subagents in parallel, each invoking `river-rats-core/calibration_exam.py` v2.3 logic to grade the agent's blind exam attempt against answer key. Constants per `calibration_exam.py` v2.3:
- `STANDARD_EXAM_SIZE = 28` standard hands
- `STANDARD_PASS_THRESHOLD = 23` correct (82.1%)
- Reversal set: `GTO_REVERSAL_HANDS ∪ GROUP_D_REVERSAL_HANDS` = 10 hands (100%-must-pass)

**Pass criterion per agent:** ≥23/28 standard exam AND 100% (10/10) reversal.

**Per-Phase-A outcome rule (per spec §"Phase A"):**
- **All 33 pass** → PROCEED to Phase B
- **1-3 fail** → Pilot Orchestrator dispatches replacement agents for failed slots; re-test
- **4+ fail** → HALT pilot. Calibration regression — investigate Stage 4 prompt quality before continuing.

**Cost:** ~$25-$130 per spec §"Cost tracking" (33 agents × 38 hands × ~$0.02-$0.10/hand depending on Opus/Sonnet labeller mix per A.2 lock).

**Wall-time:** ~38 min if all 33 dispatched in parallel; longer if queued by Anthropic tier rate limits.

**Cost-authorization status:** pilot dispatch already greenlit per `MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md` (`082336d`, owner direction at 15:35 SAST + greenlight at 16:19 SAST + reaffirmed in eaefc2a at 19:50). Per autonomous-advance authority + `feedback_quality_default_no_ask.md`, Pilot Orchestrator may proceed without re-asking.

**Conservative pause** (suggested but not blocking): surface A.4 dispatch start to operator immediately before initiating 33-agent burst, so operator has chance to halt if running cost or wall-time concerns surface in real time.

## A.6 — Cost telemetry baseline — IN PROGRESS

Cost telemetry tracking starts at this comm (~19:55 SAST). Pilot Orchestrator records per-call $ + token usage at each phase boundary, with per-phase aggregates surfaced to subsequent status comms.

Baseline: $0.00 spent (this comm + A.5 fixture verification + setup are all read-only / Pilot-Orchestrator-internal; no API calls yet).

## A.7 — Phase A summary + GO/NO-GO — STAGED

Composed at end of Phase A (post A.4 calibration completion).

**GO criteria** (per spec):
- A.5 PASS ✓ (this comm)
- A.1 confirmed (or default Tier 1 assumption)
- A.2 confirmed (or default per orchestrator pre-specification)
- A.3 p95 ≤ 120s (HARD halt threshold)
- A.4 ≤ 3 calibration failures (PROCEED if 0 fails; replacement dispatch path if 1-3 fails; HALT if 4+ fails)
- A.6 cost-telemetry baseline established

**NO-GO surfaces** with EVIDENCE block per orchestrator MERGE ACK reporting cadence.

## HOLD register update

| # | Item | Status | Owner |
|---|------|--------|-------|
| 44 | Phase A preflight (A.1-A.7) | 🔥 ACTIVE — A.5 DONE; A.1/A.2 awaiting operator inputs; A.3/A.4 staged for dispatch | Pilot Orchestrator |
| 45 | Phase B-G heavy lift | ⏳ QUEUED post-Phase-A-GO | Pilot Orchestrator |

## Action

**Owner (immediate inputs requested):**
1. **A.1**: confirm Anthropic API tier (Tier 1 default vs Tier 2-4 enables 15-way parallel)
2. **A.2**: confirm model selection lock per orchestrator pre-specification (Opus 4.7 high-stakes; Sonnet 4.6 labeller); OR provide alternate per-role lock
3. **Cost-authorization re-affirmation** (already greenlit at 16:19; surface for transparency): proceed with A.3 (~$0.25) + A.4 (~$25-$130) + Phase B-G (~$140-$700 total envelope per spec) within stated envelope

**Pilot Orchestrator (next action):**
1. Wait for operator response (~30-60 min reasonable holding window; if silent, default-assumption path engages per autonomous-advance authority)
2. On operator confirmation OR default-assumption trigger: dispatch A.3 (single subagent, ~$0.25, ~5 min)
3. On A.3 PASS (p95 ≤ 120s): dispatch A.4 (33 subagents parallel, ~38 min, ~$25-$130)
4. On A.4 result: compose A.7 summary + GO/NO-GO recommendation
5. Status comm cadence: per-phase boundary updates surfaced to `review/comms/PILOT_PHASE_A_*.md`

**Orchestrator (main terminal):**
1. Read this comm + (optional) override A.5 PASS verdict if any concern surfaces
2. Confirm or correct spec-vs-MERGE-ACK ordering interpretation
3. Watch for `PILOT_PHASE_A_SUMMARY_2026-04-26.md` (or HALT comm) — ETA ~50-60 min from operator A.1/A.2 confirmation

**QC stream:**
1. Layer 3 pilot-runtime watch active per `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`
2. A.5 verdict observable: 5/5 PASS — no S-A12 incident this preflight
3. Surface findings if HIGH-severity drift or labelling-quality concerns surface during A.3/A.4

## References

- BUILDER_BUILDS_ABCD_COMPLETE: `dfd8925` (`review/comms/BUILDER_BUILDS_ABCD_COMPLETE_2026-04-26.md`)
- Pilot dispatch resume: `eaefc2a` (`MAIN_TERMINAL_PR45_MERGE_ACK_PILOT_DISPATCH_RESUME_2026-04-26.md`)
- Stage 4 spec v1.0.3: `review/comms/STAGE4_PILOT_ORCHESTRATION_v1_0.md`
- Phase A.5 fixture file: `data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl` (SHA256 `98e4309a...4319`)
- Phase A.5 fixture lock: `data/phase_a5_partial_fold_fixtures_2026-04-26.lock.json`
- Calibration exam v2.3: `river-rats-core/calibration_exam.py` (`STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`, `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS`)
- Pilot 100-hand corpus: `data/pilot_corpus_100_hand_2026-04-26.jsonl` (SHA256 `c93a41c4...`) — used in Phase B not Phase A
- Pilot run dir: `review/pilot_run_2026-04-26/` (created this turn)

**Status: PHASE A IN PROGRESS — A.5 PRE-CALIBRATION GATE PASS. Awaiting operator inputs on A.1 + A.2 (~30-60 min holding window). A.3 + A.4 staged for autonomous dispatch on operator confirmation OR default-assumption trigger.**
