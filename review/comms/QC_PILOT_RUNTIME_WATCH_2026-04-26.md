---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder (Pilot Orchestrator persona) · Owner (briefed)
re: QC pilot-runtime monitoring mode ACTIVE — owner authorized pilot dispatch at ~15:35 SAST per `MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md`; QC switches from pre-pilot sweep mode to pilot-runtime watch mode per Phase 5 framework Layer 3
status: FLAG (informational; QC publishing watch list so orchestrator + Pilot Orchestrator know what QC monitors during pilot phases)
---

# QC Pilot-Runtime Watch — Phase 5 Layer 3 ACTIVE

## Mode transition

Per `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-framework.md` Layer 3 (end-to-end pilot dry-run watch list) + decision tree in standing /loop prompt:
- Owner authorization received → QC transitions from pre-pilot sweep (Layer 1 + Layer 2 COMPLETE) to pilot-runtime monitoring (Layer 3).

QC operates in parallel to Pilot Orchestrator's per-phase progress reporting. **QC FLAG-only — does not gate pilot phase transitions.** Surfaces any anomaly within 1 tick; orchestrator + Pilot Orchestrator decide remediation.

## Phase A preflight — QC watch items

QC monitors for HALT comms + Phase 5 fix regressions. Six A-substeps map to Phase 5 fix surfaces:

| Substep | What QC watches | HALT signal |
|---------|-----------------|-------------|
| A1 API tier | rate-limit headers visible to operator; insufficient tier should HALT cleanly | `PILOT_PHASE_A_HALT_API_TIER_*` |
| A2 model lock | Opus vs Sonnet selection documented; per-role assignment recorded | (no HALT; operator-selectable) |
| A3 5-call latency probe | p50/p95 within ~30-90s assumption | `PILOT_PHASE_A_HALT_LATENCY_*` |
| A4 28-hand calibration | **HIGH-2 fix — uses `calibration_exam.py` v2.3 with constants by name (`STANDARD_EXAM_SIZE`/`STANDARD_PASS_THRESHOLD`/`GTO_REVERSAL_HANDS`/`GROUP_D_REVERSAL_HANDS`)**; pass criterion 23/28 + 100% on 10 reversal hands | `PILOT_PHASE_A_HALT_CALIBRATION_*` |
| A5 villain-selection | **HIGH-1 fix — 5-hand partial-fold MW fixture verification; `_villain_pos_raw` ∈ live-opponent set** | `PILOT_PHASE_A_HALT_VILLAIN_SELECTION_*` |
| A6 cost telemetry | baseline recorded; Phase B projection within $140-$700 envelope | (no HALT; informational) |

## Phase B/C/D/E/F/G — QC watch items

| Phase | What QC watches | HIGH-class regression signal |
|-------|-----------------|------------------------------|
| B labelling (15 × 100) | per-record schema valid; per-protocol output paths respected (S-X10 firewall) | cross-protocol path violation |
| (post-B) firewall audit | **MEDIUM-S-X10 fix — orchestrator scans all label paths against dispatch records** | any path-traversal flagged |
| (pre-C) anonymisation | **MEDIUM-S-X4 fix — protocol-vocabulary token strip applied** | un-stripped Step N / tier name / RAISE_<sizing> reaches highlighter |
| C highlighting | H1 + H2 both receive same anonymised input | input asymmetry between H1/H2 |
| D convergence | κ math runs cleanly; stop-condition table fires correctly | NaN κ on degenerate marginals (S-X6) |
| E reviewer | reasoning traces present; reviewer dispatches independent of labellers | role-overlap violation |
| F adjudicator | role 1 + role 3 are different subagent dispatches (S-X5 enforcement) | same-session role-1+role-3 |
| G corpus seal | SHA256 hash recorded; corpus disjoint from holdout 50 + calibration 24 | hash mismatch or overlap |

## Standing watch loop

QC's /loop continues at dynamic cadence. During pilot Phase A: 270s wake (cache-warm) — preflight steps complete in minutes; HALT signal must surface within 1 tick. During Phase B (heavy labelling, ~5-6h): 600-1500s wake (Phase B is steady-state; HALT signal less likely than during preflight or transition). During Phase C/D/E/F/G transitions: tighten to 270-600s.

## When QC reports

- HIGH (1-tick): any HALT comm; any per-phase regression matching Phase 5 fixes; any spec violation surfaced in pilot output
- MEDIUM (next routine sweep): cost-overrun trajectory; latency drift; minor schema-violation patterns
- LOW (weekly digest): cosmetic drift, prose-only issues
- NIT: defer

## QC's prior contribution to pilot readiness

Per orchestrator's `MAIN_TERMINAL_PR31_MERGED_PILOT_GATE_CLEAR_2026-04-26.md`:
- 9 HIGH findings surfaced + addressed across QC Phases 1/2/3/5 → all sealed in master
- 7 successive pre-merge audits running cleanly
- 6 multi-expert TC-15 demonstrations
- Orchestrator queued process-level memory addition `feedback_spec_vs_infrastructure_code_drift.md` based on Phase 5 HIGH-2 finding

## Reference

- Phase 5 framework: `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-framework.md`
- Phase 5 results: `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-results.md`
- Pilot dispatch authorization: `MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md`
- Pilot orch spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 (sealed via PR #31 at `c4f29a5`)
- All prior QC findings: `~/river-rats-qc/findings/2026-04-26-*.md` (10 finding files; 9 HIGH addressed; 0 rollbacks)

**Status: QC pilot-runtime monitoring ACTIVE. Standing /loop continues at dynamic cadence. Surfaces HIGH within 1 tick.**
