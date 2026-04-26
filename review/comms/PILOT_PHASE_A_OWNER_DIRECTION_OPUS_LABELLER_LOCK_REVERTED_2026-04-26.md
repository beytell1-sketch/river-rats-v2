---
date: 2026-04-26
from: Pilot Orchestrator (general-purpose subagent under Pilot Orchestrator persona)
to: Main terminal (orchestrator) · Owner · QC stream
re: REVERT — owner withdrew "upgrade lablelers to opus 4.7" direction; A.2 model lock restored to orchestrator pre-spec (Sonnet 4.6 labeller; Opus 4.7 high-stakes); cost envelope returns to original $140-$700 spec
status: A.2 LOCK REVERTED to orchestrator pre-spec; cost envelope back to $140-$700; A.7 HARD HALT on A.4 reversal gate fail STILL IN EFFECT
supersedes: PILOT_PHASE_A_OWNER_DIRECTION_OPUS_LABELLER_LOCK_2026-04-26.md (master `4c44026`)
---

# Owner direction REVERSED: A.2 model lock restored

## Owner direction (verbatim, ~21:00ish SAST then ~21:05 SAST)

> 1. "upgrade lablelers to opus 4.7" (initial)
> 2. "undo upgrade to opus 4.7 request." (revert)

Per `feedback_listen_to_orchestrator_always.md` + autonomous-advance authority, owner direction is sufficient for both the lock change and the revert.

## A.2 model lock — RESTORED to orchestrator pre-spec

| Role | Lock (current) |
|------|----------------|
| Labeller (15 agents × A/B/C protocols) | **Sonnet 4.6** (per orchestrator pre-spec) |
| Highlighter (6 agents H1+H2) | Opus 4.7 |
| Reviewer (8 agents) | Opus 4.7 |
| Adjudicator (3 agents: GTO + solver-verify + writer) | Opus 4.7 |
| Pilot Orchestrator | Opus 4.7 (1M context) |

## Cost envelope — restored to spec

Phase B alone: $75-$375 (Sonnet labeller). Total pilot run: $140-$700 (within original spec hard cap). The implicit envelope authorization in the prior comm (`4c44026`) is withdrawn.

## A.7 HARD HALT — still in effect

The A.4 reversal gate failure is a **separate issue from model selection**. Both Sonnet AND Opus failed the same 2 Group-D BB-flop reversal hands (d3688, d9556). Restoring A.2 to Sonnet does NOT change the A.4 result.

**A.7 HALT remains in effect; Phase B remains BLOCKED** pending orchestrator's path decision (A/B/C/D per `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` master `b2de857`).

## F-S5 patch directive — still active (orchestrator commissioned)

Per `MAIN_TERMINAL_PHASE_A8_SYNTHESIS_FS5_PATCH_DIRECTIVE_2026-04-26.md` (master `947f176`):
- Orchestrator commissioned a phantom-feature patch on `prompts/protocol_b_composition_first_v1_0_pilot.md` L283-285 + `prompts/protocol_b_composition_first_v1_0.md` L264-266 (Range-mass axis cites `hero_top_pair_plus_pct` which doesn't exist in 59-feature contract)
- Directive addressed to logic builder (transient builder persona switch)
- ~30-45 min builder cycle + standard PR + reviewer + QC + V3-compliance

**F-S5 patch is independent of model selection** — the phantom feature affects ALL labellers regardless of Opus vs Sonnet. The patch is needed for Phase B regardless of A/B/C/D path on A.7 HALT.

**Pilot Orchestrator HOLDING F-S5 patch start** until owner confirms direction given active back-and-forth (pause → resume → Opus upgrade → undo). Owner: please confirm whether to proceed with F-S5 patch now per orchestrator directive, OR hold pending broader direction.

## Action

**Owner:**
1. Confirm A.2 revert noted (no action needed unless wrong)
2. Direct on F-S5 patch: proceed per orchestrator directive (~30-45 min), or hold

**Orchestrator (main terminal):**
1. A.2 lock is back to your pre-spec
2. F-S5 patch directive remains your authority; awaiting owner go-signal in this active session
3. A.7 HALT path decision (A/B/C/D) pending

**Pilot Orchestrator (this session):**
1. Reverted A.2 lock (this comm)
2. HOLDING F-S5 patch start pending owner confirmation
3. Standing by for orchestrator A.8 trace audit + final synthesis
4. Standing by for orchestrator A.7 HALT path decision

## References

- Reverted comm: `PILOT_PHASE_A_OWNER_DIRECTION_OPUS_LABELLER_LOCK_2026-04-26.md` (master `4c44026`) — supersedes; A.2 lock reverts
- A.7 HALT: `PILOT_PHASE_A_SUMMARY_HALT_2026-04-26.md` (master `b2de857`)
- F-S5 patch directive: `MAIN_TERMINAL_PHASE_A8_SYNTHESIS_FS5_PATCH_DIRECTIVE_2026-04-26.md` (master `947f176`)
- A.4 calibration results: `review/pilot_run_2026-04-26/calibration_results_*.json` (master `ee197a9`)

**Status: A.2 LOCK REVERTED. A.7 HALT REMAINS. F-S5 PATCH HELD PENDING OWNER CONFIRMATION.**
