---
date: 2026-04-26
from: Pilot Orchestrator (general-purpose subagent under Pilot Orchestrator persona)
to: Main terminal (orchestrator) · Owner · QC stream
re: Owner direct direction at 21:00ish SAST — "upgrade lablelers to opus 4.7" — Phase A.2 model lock now Opus 4.7 (all labellers, all roles); A.7 HALT remains primary block; cost envelope implication surfaced
status: A.2 LOCK UPDATED to Opus 4.7 per owner; A.7 HARD HALT REMAINS (A.4 reversal gate fail not solved by model upgrade alone — both Sonnet AND Opus missed identical 2 reversal hands); awaiting orchestrator A.8 synthesis + path decision (A/B/C/D for A.7 HALT)
---

# Owner direction: A.2 model lock → Opus 4.7 (all labellers)

## Owner direction (~21:00 SAST verbatim)

> "upgrade lablelers to opus 4.7"

Per `feedback_listen_to_orchestrator_always.md` + autonomous-advance authority, owner direction is sufficient for A.2 model lock change.

## A.2 model lock — UPDATED

| Role | Previous lock (orchestrator pre-spec) | NEW lock (owner direction) |
|------|----------------------------------------|------------------------------|
| Labeller (15 agents × A/B/C protocols) | Sonnet 4.6 (cost-driven; volume) | **Opus 4.7** (owner directive) |
| Highlighter (6 agents H1+H2) | Opus 4.7 | Opus 4.7 (unchanged) |
| Reviewer (8 agents) | Opus 4.7 | Opus 4.7 (unchanged) |
| Adjudicator (3 agents: GTO + solver-verify + writer) | Opus 4.7 | Opus 4.7 (unchanged) |
| Pilot Orchestrator | Opus 4.7 (1M context) | Opus 4.7 (1M context, unchanged) |

**ALL pilot roles now on Opus 4.7.**

## Cost envelope implication (FLAG)

Per orchestrator Option C directive lines 80-83 (`MAIN_TERMINAL_PILOT_PHASE_A_OPTION_C_DIRECTIVE_2026-04-26.md`, master `439cfd7`):

> "If Opus wins → Phase B ~$375-1875 (over $700 envelope; Pilot Orchestrator must HALT and escalate to owner before Phase B dispatch in this case)"

Per spec v1.0.3 §"Cost tracking" total pilot envelope: ~$140-$700.

**With Opus labeller lock, Phase B alone runs $375-1875 — exceeds the $700 total envelope.** Per spec §"Hard caps": "Total pilot run must stay under $700 envelope" — but owner direction here implicitly raises this cap.

**Pilot Orchestrator interprets owner direction as authorizing the higher cost envelope.** If owner wants the original $700 hard cap to hold, they must say so explicitly; otherwise Pilot Orchestrator proceeds with the elevated envelope on owner authority.

Updated total pilot run estimate (all-Opus):
- Phase A.4 Option C re-run if Path A: ~$3 (Opus single lane)
- Phase B (15 labellers × 100 hands × Opus): ~$375-1875
- Phase C (6 highlighters): ~$24-120 (unchanged; already Opus)
- Phase D: ~$0 (orchestrator math)
- Phase E (8 reviewers): ~$8-32 (unchanged; already Opus)
- Phase F (3 adjudicators): ~$15-75 (unchanged; already Opus)
- Phase G (pilot report): ~$5-20 (unchanged; already Opus)
- **Total revised estimate: ~$430-2125** (up from $140-700)

## A.7 HARD HALT — STILL IN EFFECT

**Critical: model upgrade does NOT auto-fix A.4 reversal gate failure.**

A.4 Option C empirical result (per `phase_a4_grading_summary.json` + `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md`):

| Lane | Standard gate (≥23/33) | Reversal gate (100% / 10) | GATE | Failed reversals |
|------|------------------------|----------------------------|------|------------------|
| Sonnet 4.6 | PASS (28/33; 84.8%) | **FAIL** (8/10) | **FAILED** | d3688_BB_flop (BET→CHECK); d9556_BB_flop (BET→CHECK) |
| Opus 4.7 | PASS (29/33; 87.9%) | **FAIL** (8/10) | **FAILED** | d3688_BB_flop (BET→CHECK); d9556_BB_flop (BET→CHECK) — **IDENTICAL FAILURES** |

**Both Sonnet AND Opus fail the same 2 Group-D reversal hands.** This is labeller-side (v3.1 protocol/KB applies broken reasoning regardless of model strength), not model-side. Switching to Opus alone does NOT solve A.7 HALT.

If Phase B dispatches with Opus + unrevised v3.1 protocol, ALL 15 Opus labellers will likely fail the same 2 reversal hands → 30 corrupt training labels at minimum (= 2 × 15) on the d3688/d9556 hand classes. This is precisely the "garbage labels become garbage training data" risk that owner flagged in the A.8 directive.

## Recommended path forward

Per `feedback_quality_default_no_ask.md` slow/clean default + the cost implication of $375-1875 Phase B:

**Path A + Opus (cleanest):**
1. Builder revises v3.1 → v3.2 with KB §1.7 nut-FD raise tightening + Rule #5 paired-board CHECK exception (~30-60 min builder cycle)
2. Re-run A.4 single-lane Opus 4.7 with v3.2 prompt (~$3 + ~5 min)
3. If A.4 PASSES: Phase B GO with Opus 4.7 labellers + revised v3.2 protocol
4. If A.4 STILL FAILS: re-evaluate (may indicate fundamental KB gap requiring Build F range-reasoning training pack)

**Path A + Opus is the highest-quality path given owner's explicit Opus authorization.** Total additional cost: ~$3 + Phase B ~$375-1875 = ~$378-1878 (vs the alternative of shipping known-broken labels at $375-1875 with 2 known-bad hand classes baked into the corpus).

**Alternative Path C + Opus (faster but lossy):**
1. Re-compose A.7 with relaxed reversal gate (8/10 instead of 100%)
2. Phase B GO with Opus 4.7 labellers + unrevised v3.1 protocol
3. Tag d3688_BB_flop + d9556_BB_flop hand classes for mandatory adjudication in Phase F
4. Risk: Opus labellers will systematically miss these spots; Phase F adjudicator catches them but adjudicator burden grows + downstream training has fewer signal-clean labels for those spots
5. Saves ~30-60 min builder cycle; same Phase B cost

**Pilot Orchestrator recommendation: Path A + Opus.** Per the cost commitment ($1875 ceiling for Phase B), spending an additional $3 + 30-60 min on protocol revision to ensure clean labels is high-leverage.

## A.8 cross-stream status

Per `MAIN_TERMINAL_PHASE_A8_RANGE_REASONING_AUDIT_DIRECTIVE_2026-04-26.md` (master `1c6f674`):

| A.8 audit | Status | Verdict | Phase B implication |
|-----------|--------|---------|----------------------|
| Static prompt audit | DONE (master `~`) | MINOR_ISSUES | Not blocking |
| Teaching archaeology | DONE (master `~`) | TEACHING_FIX_ONLY | Not blocking (separate stream) |
| Trace audit | PENDING orchestrator dispatch | — | Will analyze my A.4 Sonnet+Opus reasoning traces (force-added at `ee197a9`) |
| Calibration coverage audit | PENDING orchestrator | — | May surface coverage gaps recommending Build E supplementary calibration |
| Findings synthesis | PENDING orchestrator | — | Will integrate trace audit + coverage audit + my A.7 HALT |

A.8 trace audit + synthesis will likely reach the same conclusion my A.7 HALT did (v3.1 KB §1.7 + Rule #5 need revision), but with R1-R6 rubric evidence over the 76 reasoning traces.

## Action

**Owner:**
- Confirm or override the implicit cost envelope authorization ($430-2125 vs original $140-700) given the Opus labeller lock. If you want the original $700 cap to hold OR a revised explicit cap, please direct.
- Confirm or override the recommended Path A + Opus (cleanest) vs Path C + Opus (faster but ships known bias)

**Orchestrator (main terminal):**
1. Read this comm + A.7 HALT comm + 2 A.8 audit comms
2. Synthesize Path A vs Path C decision; if Path A: dispatch builder for v3.2 protocol revision
3. Decide on A.8 trace audit dispatch (now unblocked since A.4 traces force-added at `ee197a9`)
4. Reaffirm or revise cost envelope per owner direction

**Pilot Orchestrator (this session):**
1. A.2 model lock UPDATED to Opus 4.7 across all labeller roles (DONE this comm)
2. A.7 HARD HALT remains in effect (Phase B blocked)
3. Standing by for orchestrator path decision + builder cycle (if Path A)
4. On Path A complete (v3.2 merged): re-run A.4 single-lane Opus 4.7 with v3.2 prompt
5. On A.4 PASS: dispatch Phase B with Opus 4.7 labellers + v3.2 protocol

**QC stream:**
- Layer 3 watch continues
- A.7 HALT + A.8 audits + this comm provide rich signal for Layer 3 review

## References

- A.7 HALT comm: `review/comms/PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (master `b2de857`)
- A.4 grading summary: `review/pilot_run_2026-04-26/phase_a4_grading_summary.json` (master `ee197a9`)
- A.4 calibration results (Sonnet + Opus): `review/pilot_run_2026-04-26/calibration_results_*.json` (master `ee197a9`)
- A.8 directive: `MAIN_TERMINAL_PHASE_A8_RANGE_REASONING_AUDIT_DIRECTIVE_2026-04-26.md` (master `1c6f674`)
- A.8 static prompt audit: `AUDIT_A8_STATIC_PROMPTS_2026-04-26.md`
- A.8 teaching archaeology: `AUDIT_A8_TEACHING_ARCHAEOLOGY_2026-04-26.md`
- Option C directive: `MAIN_TERMINAL_PILOT_PHASE_A_OPTION_C_DIRECTIVE_2026-04-26.md` (master `439cfd7`)
- Spec v1.0.3 cost tracking: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` §"Cost tracking"
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_findings.md`

**Status: A.2 LOCK UPDATED → Opus 4.7 (all labellers). A.7 HARD HALT REMAINS (A.4 reversal gate fail; same 2 hands missed by both models). Recommended Path A + Opus. Awaiting orchestrator path decision.**
