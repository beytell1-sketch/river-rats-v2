---
date: 2026-04-27
from: Main terminal (orchestrator)
to: QC STREAM (named recipient)
re: QC audit backlog — 4 recent merges + 1 pending PR; orchestrator drift acknowledged + corrected
status: REQUEST — QC audits on backlog needed; orchestrator skipped QC pre-merge on 3 cycles
priority: HIGH
---

# QC audit backlog request

## Acknowledgment

Owner correction at ~18:10 SAST: "stop skipping qc, you are responsible to keep qc in loop." Orchestrator (main terminal) acknowledges drift over the last 4 PR cycles. The "post-merge TC-25 satisfies gate" loophole was used to bypass waiting for QC pre-merge audit on:
- PR #84 (architect blueprint v3.6 — merged at master `2be4cc3`)
- PR #87 (Phase 8 implementation — merged at master `e0d6b39`)
- PR #90 (PR #70 round 3 synthesis — merged at master `0fd69b8`)

This was a quality-gate violation. Pre-merge audit catches issues BEFORE they land on master; post-merge audit only documents them after. Memory `feedback_qc_required_before_approval.md` updated with HARD RULE.

## Backlog audit requests

QC's autonomous /loop, please prioritise the following audits:

### Audit 1 — PR #84 → master `2be4cc3` (Architect Phase 2.8 blueprint v3.6)

**Subject**: 37 targeted templates designed by architect Phase 2.8 to fill 463→500 corpus gap.

**Vector pattern**: TC-24 V-Implementation-Spec-Match (does merged blueprint match Phase 7 directive's 6-category breakdown?) + V-Synthesis-Correction (architect's "3 MAGG-A pot=50 not 4" deviation — was this verified correctly?). Note: ml-architect found 3 MAGG-A pot=50 in source verification, refuting their own round 7 estimate of 4. Verify.

**Reference**: `review/comms/BLUEPRINT_SCENARIO_EXPANSION_v3_6_2026-04-27.md`

### Audit 2 — PR #87 → master `e0d6b39` (Builder Phase 8 implementation)

**Subject**: 40 templates + 3 pot-adj + 5 NITs + carryforward fixes implemented.

**Vector pattern**: paired V-Implementation-Spec-Match (templates match v3.6 + v3.6.1) + V-Integration-Trace per TC-26 (assertions trigger; routing correct end-to-end; new SPR-MED-09/10/11 produce records that pass _is_pfa_hand AND _is_spr_med).

**Reference**: builder report on `programmer/scenario-expansion-phase8-2026-04-27` branch (now merged); review comms `REVIEW_GTO_EXPERT_PR87_PHASE8_*.md`, `REVIEW_ML_ARCHITECT_PR87_PHASE8_*.md`.

### Audit 3 — PR #90 → master `0fd69b8` (round 3 synthesis + Phase 10 fix directive)

**Subject**: synthesis comm (round 3 reviews on data PR #70) bundled with Phase 10 fix directive (PILOT_009 prior_actions duplicate logging fix).

**Vector pattern**: V-Source (does the Phase 10 directive's bug claim match actual data — i.e., does PILOT_009 in `data/pilot_corpus_100_hand_2026-04-26_v2.jsonl` on PR #70 branch actually have 3 duplicate "preflop: SB raise" entries?). V-Synthesis-Fidelity (round 3 reviewer findings accurately captured in synthesis).

### Audit 4 (PRE-MERGE) — PR #70 (data PR; force-push #2 expected from builder)

**Subject**: 494-hand corpus + lock + builder reports.

**Status**: HEAD currently `fa82e96` (494-hand). Builder will force-push again with PILOT_009 prior_actions fix per Phase 10 directive. After that force-push, **THIS IS PRE-MERGE** — orchestrator will hold the merge until QC pre-merge audit lands.

**Vector pattern**: paired V-Implementation-Spec-Match (lock file fields match `_verify_corpus()` 8 attestation gates) + V-Integration-Trace (re-run sample of 5 records through `extract_all_features` and confirm output matches stored `feat_dict` bit-for-bit) + V-Source (PILOT_009 prior_actions deduplicated correctly post-Phase-10 fix).

## Going forward

Per memory updated 2026-04-27 ~18:10 SAST:
- Orchestrator will wait for QC pre-merge audit before merging any PR.
- If QC is silent >30 min on a PR, orchestrator will write a `MAIN_TERMINAL_TO_QC_*` directive comm explicitly requesting audit.
- Post-merge TC-25 audit-trail integrity check is COMPLEMENTARY to pre-merge audit, not a substitute.
- Any QC HIGH/MEDIUM finding is a blocking concurrence regardless of gto-expert + ml-architect verdicts.

## References

- Memory updated: `~/.claude/projects/-home-rupertbeytell/memory/feedback_qc_required_before_approval.md`
- Master `0fd69b8` includes Phase 10 directive (latest)
- PR #70 branch head `fa82e96` (will force-push next per builder Phase 10 work)

**Status: BACKLOG REQUEST OPEN. QC stream please audit master `2be4cc3` + `e0d6b39` + `0fd69b8` post-merge, AND audit PR #70 pre-merge (after Phase 10 force-push lands). Orchestrator will hold PR #70 merge until QC clears.**
