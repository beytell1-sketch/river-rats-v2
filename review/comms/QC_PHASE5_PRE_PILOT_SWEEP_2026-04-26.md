---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder · Owner (briefed; HIGH-severity 1-tick rule)
re: Phase 5 pre-pilot adversarial sweep COMPLETE — 2 HIGH-severity findings affecting pilot-dispatch decision; recommend pre-dispatch resolution; orchestrator's "pilot gate effectively CLEAR" brief was based on logic-side review and missed spec-vs-infrastructure-code drift
status: FLAG (HIGH-severity per 1-tick rule); QC FLAG-only — owner + orchestrator decide gate timing
severity: 2 HIGH (pilot-relevant) / 4 MEDIUM / 5 LOW
multi-expert verdict: CONVERGED on Layer 1 (canonical state intact) | DIVERGED on Layer 2 HIGH findings (each agent surfaced unique high-leverage gap — textbook protocol-diversity)
master HEAD at audit time: 755b0f1
full finding: ~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-results.md
---

# QC Phase 5 Pre-Pilot Sweep — Results (Cross-Stream)

## Headline

QC Phase 5 sweep fired per orchestrator's `755b0f1` Option C trigger. Layer 1 (per-artifact confirmation) clean. Layer 2 (adversarial test case generation, multi-expert) surfaces **2 HIGH-severity findings** the prior review chain missed.

**No rollback warranted.** All 5 Stage 4 prep tasks remain canonical at sealed versions; no merged PR has empirically false content. The 2 HIGH findings are pilot-fitness gaps, not gate failures — but both are pilot-blocking unless reconciled.

## HIGH-1 — Primary-villain selection drives blocker NaN-flagging on partial-fold MW pots (S-A12)

**Surface:** 3-way pot, BB folds mid-flop, SB live through river. Pilot dispatches with different `_villain_pos_raw` selections produce systematically different blocker features:
- `_villain_pos_raw='BB'` (folded): blockers all NaN-flagged
- `_villain_pos_raw='SB'` (live): blockers populated correctly (e.g. `flush_draw_block_pct=0.0`, `straight_draw_block_pct=0.088`, `nut_made_block_pct=0.667`)

**Root cause:** HIGH-4 OR-derivation (monotone-True semantics) at `feature_extractor.py:2412-2429`. Not a regression — documented design choice. But pilot risk: spec doesn't guarantee labellers pick a live opponent as `_villain_pos_raw`. Stage 5 retrain feature regeneration on partial-fold MW training rows with folded-primary loses blocker training signal.

**Suggested fix (advisory):** Option A (preferred) — pilot orchestration spec v1.0.3 adds explicit rule: *"On any multi-opponent hand where any opponent is live, designate a live (non-folded, non-overflowed) opponent as `_villain_pos_raw`."* Plus Phase A preflight assertion. ~30-45 min spec edit. No code change. No cross-stream impact.

Option B (alternative): amend HIGH-4 derivation to per-villain-truth-dominates-HU-sentinel for MW. Requires logic + teaching coordination.

## HIGH-2 — Calibration manifest drift: spec vs `calibration_exam.py` v2.3 infrastructure (S-X1)

**Stage 4 pilot orchestration spec v1.0.2** (PRE-DISPATCH PREREQUISITES rows #3 + #10) says:
- 24-hand calibration manifest
- "20/24 + all 3 GTO-reversal hands correct"

**`river-rats-core/calibration_exam.py` v2.3** (lines 4-97) actually defines:
- `STANDARD_EXAM_SIZE = 28`
- `STANDARD_PASS_THRESHOLD = 23` → 23/28
- `GTO_REVERSAL_HANDS = {MW-30, MW-33, MW-50, d2410_CO_turn, d3178_CO_river}` (5 hands)
- `GROUP_D_REVERSAL_HANDS = {d3688_BB_flop, d4312_CO_turn, d9556_BB_flop, d2074_BTN_turn, d5466_CO_flop}` (5 more hands)
- **= 10 reversal hands total with 100%-must-pass**

Comms history (`PHASE_0_PREFLIGHT_2026-04-16.md`, `BUILDER_STATUS_5_2026-04-16.md`) records the v2.2→v2.3 threshold change. **Stage 4 pilot spec v1.0.2 was authored without folding that change in.**

**Pilot relevance:** Phase A pass criterion as written is structurally inconsistent with infrastructure. Pilot Orchestrator hand-grades 24-hand subset with 20/24 + 3 reversals (less strict) OR programmatically invokes `calibration_exam.py` v2.3 gate (23/28 + 10 reversals; stricter). Either way the spec misrepresents the gate.

**Why prior reviewers missed it:** all reviewers (orchestrator's gto-expert + ml-architect dispatches; QC's pre-merge audits on PRs #24/#28/#29) checked prose consistency + cross-references to other Stage 4 prep docs. None cross-checked against `calibration_exam.py` infrastructure code. **This is the spec-vs-infrastructure-code drift pattern (incident #18 candidate).**

**Suggested fix (advisory):** v1.0.3 spec reconciles to v2.3 manifest (Option a — preferred per `feedback_quality_default_no_ask.md` quality-default + tighter-gate-is-correct-gate). Refer to constants by name (`STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`, etc.) so future drift surfaces inconsistency. Plus update `docs/LABELLING_PIPELINE.md` (currently stale with v1 prompt + v1.1 KB + 24-hand exam mental model — S-X3 MEDIUM finding compounds this).

## Other findings (compact)

### MEDIUM (4)
- **S-A3:** `_action_history_cache_key` produces different keys for dict-form vs tuple-form encodings of identical logical histories
- **S-X3:** `docs/LABELLING_PIPELINE.md` content stale (compounds HIGH-2)
- **S-X4:** Highlighter prose-style protocol fingerprinting — anonymisation doesn't strip protocol-vocabulary tokens
- **S-X10:** Cross-protocol firewall has no orchestrator-side audit (relies on labeller self-report)

### LOW (5)
- S-A2/S-A9 hand-notation duplicate-card check; audit-runner timestamp 1s collision; S-X5 adjudicator role-separation text-only; S-X6 Fleiss-κ NaN handling unspecified; S-X8 replacement-chain failure pattern not surfaced as separate diagnostic; S-X9 Phase A grades answer-only

## Multi-expert convergence (TC-15 sixth demonstration)

| Aspect | Agent #1 logic-stress | Agent #2 protocol-stress |
|--------|----------------------|--------------------------|
| Layer 1 confirmation | PASS | (skipped; not in scope) |
| HIGH findings | 1 (S-A12) | 1 (S-X1) |
| Overlap on HIGH findings | NONE | NONE |
| MEDIUM findings | 1 (S-A3) | 3 (S-X3, S-X4, S-X10) |
| LOW findings | 4 | 5 |

**CONVERGED on Layer 1 + invariants** (108/108 tests PASS, hash-lock preserved). **DIVERGED on Layer 2 HIGH findings — each agent surfaced unique high-leverage gap.** Sixth TC-15 demonstration; multi-expert principle continues to deliver value.

## STOP-condition assessment

Two HIGH findings IS suggesting the orchestrator's "pilot-dispatch gate effectively CLEAR" claim was based on incomplete review:
- HIGH-1 (S-A12) = previously-undocumented design-choice vs pilot-fitness gap
- HIGH-2 (S-X1) = previously-undocumented spec-vs-infrastructure-code drift

But neither is a STOP-condition in the sense of "merged PR is empirically false":
- All sealed PRs remain canonical (no rollback)
- No production code is broken
- Pilot dispatch is owner-gated; QC's role is to inform that decision

Per QC's STOP-protocol: HIGH findings surfaced 1-tick to comms (this doc); orchestrator + owner decide gate timing.

## Recommended pre-pilot fix-list (bind to owner authorization, not pre-existing merges)

| Priority | Finding | Fix | Effort | Cross-stream impact |
|----------|---------|-----|--------|---------------------|
| HIGH-1 | S-A12 | Pilot spec v1.0.3 adds `_villain_pos_raw` selection rule + Phase A preflight assertion | ~30-45 min | None |
| HIGH-2 | S-X1 | Pilot spec v1.0.3 reconciles Phase A pass criterion to v2.3 calibration_exam.py | ~30-60 min | None (logic-internal infrastructure) |
| MEDIUM | S-X3 | `docs/LABELLING_PIPELINE.md` refresh to v3.1 + 28-hand exam | ~15-30 min | None |
| MEDIUM | S-X4 | Pre-Phase-C anonymisation step: strip protocol-vocabulary tokens | ~30 min in pilot orch spec | None |
| MEDIUM | S-X10 | Post-Phase-B audit: scan label paths against dispatch records | ~30 min in pilot orch spec | None |

**Total estimated effort:** ~2-3h for v1.0.3 spec pass + supporting `LABELLING_PIPELINE.md` refresh.

## Recommended sequence

1. **Now:** orchestrator triages this finding; decide whether to issue v1.0.3 directive
2. **Pre-pilot:** if v1.0.3 directive issued, builder authors fixes; QC re-audits v1.0.3 (light, similar to v1.0.1 pre-merge audit)
3. **Pilot dispatch:** owner authorization gates on v1.0.3 + Stage 6 hash-lock + all PRE-DISPATCH PREREQUISITES rows verified GREEN
4. **Phase A preflight:** standing watch list applies (S-X4 anonymisation, S-X10 audit, S-X9 reasoning-trace shape check)

## Defer to v2.x post-pilot housekeeping

- S-A3 cache-key cross-encoding canonicalisation
- S-A2/S-A9 hand-notation duplicate-card check
- Audit-runner microsecond timestamp resolution
- S-X5 adjudicator dispatch-ID tracking
- S-X6 Fleiss-κ NaN handling
- S-X8 replacement-chain failure-pattern diagnostic
- HOLD #21/#22/#23/#24/#27 logic v1.1 housekeeping

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-results.md`
- Phase 5 framework: `~/river-rats-qc/findings/2026-04-26-phase5-pre-pilot-sweep-framework.md`
- Orchestrator pre-pilot brief: `MAIN_TERMINAL_PRE_PILOT_OWNER_READINESS_BRIEF_2026-04-26.md` (`755b0f1`)
- Pilot orchestration spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.2 (sealed via PR #29 at `b2fbf02`)
- Calibration infrastructure: `river-rats-core/calibration_exam.py` v2.3
- HIGH-4 patch source: `feature_extractor.py:2412-2429` (sealed via PR #26)

**Status: Phase 5 sweep COMPLETE. 2 HIGH findings surfaced. QC FLAG-only — owner + orchestrator decide gate timing. Recommend v1.0.3 directive before owner pilot authorization.**
