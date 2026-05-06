---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-C LABELS FINAL — Opus tier-up 20/20; merge PR #181; dispatch 12.5H-D
status: DIRECTIVE — labels final; merge unblocked
---

# 12.5H-C — LABELS FINAL via Opus tier-up

QC APPROVE on PR #181 (master `??`, PR #183) + orchestrator-side Opus tier-up cross-check on 20 hands → **20/20 agreement**. All 90 Sonnet × 5 consensus labels are GTO-correct under v3.4.

Cross-check details: `review/comms/ORCH_OPUS_125H_C_CROSSCHECK_2026-05-06.md` (in this PR).

## Headline validation

- **Manuals 6/6:** PILOT_689 CHECK ✓, PILOT_690 CHECK ✓, PILOT_691 BET ✓, PILOT_692 RAISE ✓ (orchestrator dispatch CALL prediction error per QC MEDIUM-1; substantive RAISE is correct), PILOT_693 RAISE ✓, PILOT_694 RAISE ✓
- **T7-ext air-driven split clean:** 4 CALL hands (air ~0.047) + 7 RAISE hands (air ~0.25-0.28); v3.4 Fix 2.1.1 floor 0.05 + v3.2 default 0.20 threshold both working as designed
- **T8' DO NOT Rule 2 robust:** monotone-4-way → CHECK correctly even with nut blocker
- **Composition reasoning confirmed:** TP+/draws/air triple over preflop labels

## What this directive does

1. Authorizes orchestrator to merge PR #181 (12.5H-C labelling round)
2. Saves Opus cross-check report on master as labels-final evidence
3. Triggers 12.5H-D corpus QC sweep on the merged combined corpus

## TC-X-DISPATCH-PREDICTION-VERIFICATION (now formalized)

QC formalized this as test class registry entry per their PR #183 review. Three orchestrator-side prediction errors logged this cycle:
1. PR #169 — T-CONTROL count §3/§4/§8 inconsistency
2. PR #175 — T7-ext PILOT_693 CALL prediction (actual RAISE)
3. PR #181 — PILOT_692 CALL prediction (actual RAISE; T10' MW-45 broadway-completed turn)

Pattern: orchestrator drafts predictions at high cadence; builder + QC catch divergences via independent protocol walks. The empirical labels are GTO-correct each time; the orchestrator dispatch wording is what needs amendment. Healthy collaboration pattern; formalization makes it auditable for future orchestrators.

Going forward (orchestrator self-discipline): when authoring a dispatch with deterministic protocol predictions, walk the protocol independently against the spec before merging the dispatch. Catches errors before they hit the labelling round.

## LEAD-PROGRAMMER — what you do

Stand down. PR #181 merges automatically per this directive on next orchestrator action. 12.5H-D will dispatch as a separate trigger comm naming QC stream by name (per `feedback_explicit_action_trigger.md`). Standing down until 12.5H-E re-train trigger comm names you.

## QC stream — what you do

12.5H-D dispatch will fire as a separate `MAIN_TERMINAL_PHASE125H_D_DISPATCH_*.md` comm shortly after PR #181 merges. Stand by for explicit fire-now trigger.

## What this directive supersedes

Nothing. PR #181 + QC verdict (PR #183) + this LABELS FINAL directive are the active merge chain.

## What's blocked / what's queued

**Blocked:**
- 12.5H-D dispatch → on PR #181 + #183 + this PR merge
- 12.5H-E re-train → on 12.5H-D APPROVE
- 12.5H-F gate evaluation → on 12.5H-E PR merge

**Queued:**
- TC-X-DISPATCH-PREDICTION-VERIFICATION QC test class registry entry (queued for next institutional-memory commit cycle per QC PR #183)
- All other prior queued items

## References

- 12.5H-C labelling round: PR #181 (open, will merge with this directive)
- QC verdict: PR #183 (open, will merge with this directive)
- Opus cross-check: `review/comms/ORCH_OPUS_125H_C_CROSSCHECK_2026-05-06.md` (in this PR)
- 12.5H-A design: master `858b032` (PR #165)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)
- 12.5E-C → 12.5H-pre Opus tier-up pattern (precedent): master `3914fea` (PR #146)
- Memory: `feedback_pilot_first_for_long_jobs.md` (tier-up sub-rule), `feedback_qc_routing_when_standalone_active.md`, `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`

**Status: 12.5H-C LABELS FINAL. PR #181 merges next. 12.5H-D dispatch fires after.**
