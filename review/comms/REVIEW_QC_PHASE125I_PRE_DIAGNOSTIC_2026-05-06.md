---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #193 (12.5I-pre per-hand diagnostic) — APPROVE; 0 NIT
severity: clean approval
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + V-Source (citation existence) + dispatch §"NEW: Per-hand verdict completeness"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 15th successive cycle solo-routed)
---

# QC Review — PR #193 (12.5I-pre diagnostic): APPROVE; 0 NIT

## Verdict

**APPROVE PR #193 for merge.** All 3 dispatch-required audits PASS cleanly. 0 NIT new findings.

Diagnostic report classifies all 5 stay-wrong hands (MW-17/25/40/45/47) with primary residual type + Steps 2-5 evidence + 12.5I/12.5J split recommendation. Reference re-eval question on MW-25 + MW-47 surfaced cleanly to orchestrator.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR193_2026-05-06.md` master `a1e1019` + PR #192 dispatch)

3 audits — smallest scope (analysis-only diagnostic).

PR #193 head: `c7ca55c` (branch `programmer/phase125i-pre-diagnostic-2026-05-06`). Merge-base: `d366aee` (= PR #192 = 12.5I-pre dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 1-2 files; analysis-only; no `river-rats-core/` touches; no corpus / labels / prompt edits"*

| File | category |
|---|---|
| `review/comms/BUILDER_REPORT_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md` | NEW (analysis report) |
| **Total** | **1 file** ✓ (within 1-2 dispatch range; below upper bound) |

- File count = 1 ✓
- Zero `scripts/`, `river-rats-core/`, `prompts/`, `data/` edits ✓
- All-additions ✓ (analysis-only)

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

7 distinct file paths cited in diagnostic report:

| Citation | Status |
|---|---|
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | ✅ TRACKED |
| `prompts/gto_labeller_v3.4.md` | ✅ TRACKED |
| `river-rats-core/feature_extractor.py` | ✅ TRACKED |
| `river-rats-core/gto_model.py` | ✅ TRACKED |
| `river-rats-core/models/gto_model_v9_3way_v2.2.json` | ✅ TRACKED (warm-start anchor / canonical model) |
| `review/comms/BUILDER_REPORT_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md` | NOT-TRACKED ✓ expected (NEW in PR; self-reference) |
| `scripts/diagnostic_125i_pre.py` | NOT-TRACKED ✓ expected — **explicit non-shipment statement** in report: *"No `scripts/diagnostic_125i_pre.py` shipped — analysis was reproducible via inline python heredoc + existing `river-rats-core` modules"* |

The `scripts/diagnostic_125i_pre.py` citation is a transparent non-shipment statement (report explicitly notes the script does NOT exist; analysis was inline-only via heredoc). This is a GOOD pattern — explicit "we did not ship X" beats silent omission for reproducibility documentation.

**Citation existence: CLEAN.**

## Audit 3 (NEW) — Per-hand verdict completeness ✅ CLEAN

**Dispatch:** *"verify all 5 hands classified with primary residual type + supporting evidence (Step 3 importance + Step 4 counterfactual at minimum) per dispatch protocol"*

### Per-hand verdict matrix (extracted from diagnostic report)

| Hand | Primary residual type | Secondary | Step 3 importance | Step 4 counterfactual | 12.5I or 12.5J? |
|---|---|---|---|---|---|
| **MW-17** | E-FEATURE | (none) | model 0.046 on CALL | +0.843 (FOLD vs CALL) | **12.5J** (engineer features for implied-odds + nut-blocker-with-overcards) |
| **MW-25** | E-DIST underpowered | E-FEATURE secondary | better_hand_pct +0.147 toward BET | +0.880 (CHECK vs BET) | **12.5I** (T8' redesign: BET-after-checked-through-multiway hands) |
| **MW-40** | E-DIST underpowered | (none) | BET prob 0.305 (closest to flipping) | +0.267 (CHECK vs BET) | **12.5I** (T9' expansion: 30-40 hands; most tractable) |
| **MW-45** | isomorph-mismatch | E-DIST secondary | T10' parametric texture mismatch | +0.746 (CALL vs RAISE) | **12.5I'** (T10' redesign: AKQx-broadway-completed-turn variants) |
| **MW-47** | E-FEATURE primary | mixed (raw-vs-corrected expert disagreement) | model agrees with RAW expert CALL | +0.910 (CALL vs RAISE-corrected) | **12.5J** (engineer features for SUITED-NFD-with-blocker-bet+call-multiway clause-e) |

**5/5 hands classified ✓** with all 4 required dispatch elements:
- Primary residual type ✓
- Step 3 importance evidence ✓
- Step 4 counterfactual evidence (logit-shift magnitudes) ✓
- 12.5I/12.5J split recommendation ✓

### Substantive observations from diagnostic

**Reference re-eval question** (worth surfacing to orchestrator/owner): builder transparently flags that PILOT_692 (T10' MW-45 canonical) and PILOT_694 (T-RAISE MW-47 canonical) full-phase consensus produces RAISE for both hands, but:
- MW-45 reference says RAISE (consensus matches reference; original 1-labeller pilot was CALL, which matched the model — protocol-vs-reference tension surfaces as labeller variance)
- MW-47 reference says CALL (raw); solver-corrected says RAISE; v3.4 Fix 2.1.1 specifically engineers labellers to RAISE this hand

The "MW-25 / MW-47 reference re-eval question" is whether the reference set's expert action authority should be re-examined given the v3.4 protocol's GTO-derived alternative answer. This is reference-set authority scope (out of orchestrator dispatch scope; owner WHAT decision territory).

### 12.5I + 12.5J split clean (non-overlapping)

- **12.5I**: 3 hands (MW-25, MW-40, MW-45) → corpus expansion (E-DIST underpowered + isomorph-mismatch fixes)
- **12.5J**: 2 hands (MW-17, MW-47) → feature engineering (E-FEATURE primary)

Per-hand attribution is clean; no hand falls in both buckets. Owner can dispatch in parallel without coordination overhead per dispatch §"Sequencing on QC verdict" line 27.

**Per-hand verdict completeness: CLEAN.**

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of the residual-type classifications — gto-expert + ml-architect at 12.5I/12.5J dispatch design phase
- **Reference re-eval question substance** (whether MW-47 raw CALL or solver-corrected RAISE is GTO-truth) — owner-scope decision; out of orchestrator/QC mechanical audit scope
- **12.5I/12.5J dispatch sequencing** (parallel vs serial) — orchestrator scope
- **Counterfactual logit-shift methodology** (whether the +0.910/+0.880/etc. magnitudes are computed correctly) — out of QC scope; trust builder methodology if dispatch protocol followed (Steps 3 + 4 confirmed present)

## Bonus observation — explicit non-shipment statement pattern

The diagnostic report's explicit "No `scripts/diagnostic_125i_pre.py` shipped — analysis was reproducible via inline python heredoc..." is a **GOOD pattern** worth preserving. Future analysis-only PRs that don't ship a script could codify this as a standard report section: "Analysis reproducibility — what shipped vs what didn't". Avoids silent omission ambiguity that future auditors might flag.

Could become a soft-recommended pattern (no test class needed — purely a documentation hygiene observation).

## Test class implication

- **TC-23 1-2 file analysis-only scope discipline reproducible** — diagnostic-only PRs can have minimal scope (1 file) with clean audit
- **Per-hand verdict completeness pattern** — when dispatch protocol enumerates required evidence types (primary residual + Steps 3 + 4), QC verifies presence per hand. Pattern reproducible for future per-hand diagnostic PRs.
- **Explicit non-shipment statement** — good pattern; soft-recommended

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **15th successive cycle solo-routed**. Loop heartbeat detected dispatch within ~1 min of master push (loop fired immediately on user notification).

## References

- PR #193: https://github.com/beytell1-sketch/river-rats-v2/pull/193
- PR #193 head: `c7ca55c`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR193_2026-05-06.md` (master `a1e1019`, PR #194)
- 12.5I-pre dispatch: `MAIN_TERMINAL_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md` (master `d366aee`, PR #192)
- 12.5H-F synthesis (E option chosen by owner): master `ea642ed` (PR #191)
- Memory: `feedback_qc_routing_when_standalone_active.md` (15th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #193 for merge.** All 3 audits PASS cleanly; 0 NIT new findings.

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5I (D corpus expansion for MW-25/40/45) + 12.5J (C feature engineering for MW-17/47) parallel dispatch
- Reference re-eval question on MW-25/47 may surface as separate owner-WHAT-decision workstream (orchestrator's discretion)
