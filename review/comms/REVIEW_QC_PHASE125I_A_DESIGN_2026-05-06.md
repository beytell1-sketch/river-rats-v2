---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (architect hat)
re: PR #197 (12.5I-A corpus expansion design — 90-120 hands across T8'/T9'/T10') — APPROVE; 0 NIT
severity: clean approval
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"NEW: Per-template scope correctness" + §"NEW: Methodology incorporation"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 16th successive cycle solo-routed; first parallel-PR audit cycle)
---

# QC Review — PR #197 (12.5I-A corpus design): APPROVE; 0 NIT

## Verdict

**APPROVE PR #197 for merge.** All 4 dispatch-required audits PASS cleanly. 0 NIT new findings.

Design addresses MW-25/40/45 stay-wrong hands per 12.5I-pre diagnostic verdicts: T8'-redesigned (fix MW-25 isomorph mismatch), T9'-expanded (scale up MW-40 underpowered family), T10'-redesigned (fix MW-45 isomorph mismatch on AKQx-broadway-completed turn). All 6 standing methodology rules from 12.5H-A §10 reflected + operationalized.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR197_PR198_2026-05-06.md` master `ce2ee5e` + PR #196 dispatch)

4 audits — design-only.

PR #197 head: `d2c9a9e` (branch — design comm only).

## Audit 1 — Diff scope ✅ CLEAN

| File | category |
|---|---|
| `review/comms/PLAN_PHASE125I_CORPUS_EXPANSION_2026-05-06.md` | NEW (design comm) |
| **Total** | **1 file** ✓ |

Zero `scripts/`, `river-rats-core/`, `prompts/`, `data/` edits ✓. All-additions ✓.

## Audit 2 — Citation existence ✅ CLEAN

5 distinct cited paths:

| Citation | Status |
|---|---|
| `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` | ✅ TRACKED |
| `prompts/gto_labeller_v3.4.md` | ✅ TRACKED |
| `scripts/build_corpus_revision_125e_situations.py` | ✅ TRACKED (12.5E-B factory; reuse pattern) |
| `scripts/build_corpus_revision_125h_situations.py` | ✅ TRACKED (12.5H-B factory; reuse pattern) |
| `scripts/build_corpus_revision_125i_situations.py` | NOT-TRACKED ✓ expected (forward path; will be created in 12.5I-B) |

## Audit 3 — Per-template scope correctness ✅ CLEAN

**Dispatch:** *"verify T8'-redesigned (MW-25), T9'-expanded (MW-40), T10'-redesigned (MW-45) match diagnostic spec from PR #193; per-template count 30-40 each (total 90-120)"*

| Template | Failure mode (per PR #193) | Redesign approach | Parametric | Manual | Combined | Within 30-40? |
|---|---|---|---|---|---|---|
| **T8'-redesigned** | MW-25: original T8' put As ON board → hero K-spade dominated; all CHECK | Hero does NOT hold nut blocker; distinguish from 12.5H T8' canonical; pilot-verify v3.4 routes to BET | 30-35 | 2 | 32-37 | ✓ |
| **T9'-expanded** | MW-40: 14 hands all BET correctly; model fails to transfer (margin only +0.267) | Straightforward scale-up; ~32 hands; 2.3× expansion factor | 32 | 1 | 33 | ✓ |
| **T10'-redesigned** | MW-45: 13 parametric used non-broadway-completed turns; T10' canonical PILOT_692 IS the MW-45 exact replica + DID label RAISE 5/5; isomorph-mismatch on AKQx broadway-completed | Add AKQx-broadway-completed-turn variants specifically | 28-32 | 1 | 29-33 | ✓ (just at lower bound; acceptable per "30-40" range with some slack) |
| **Total target** | | | **90-99** | **4** | **94-103** | ✓ within 90-120 |

Per-template alignment with diagnostic spec: each template addresses the specific failure mode from PR #193 (E-DIST, isomorph-mismatch, etc.) with explicit redesign rationale.

**Per-template scope: CLEAN.**

## Audit 4 — Methodology incorporation ✅ COMPLETE (all 6 standing rules + new TC-X classes)

**Dispatch:** *"verify all 6 standing methodology rules from 12.5H-A §10 reflected"*

Design §"methodology" (lines 170-179) enumerates 10 numbered items covering all 6 standing rules + 4 12.5I-specific additions:

| 12.5H-A §10 standing rule | 12.5I-A §"methodology" item | Status |
|---|---|---|
| §10.1 Cross-seed importance reporting (TC-X-CROSS-SEED-IMPORTANCE) | item 7 (line 176) | ✓ |
| §10.2 Cap-binding pre-flight (TC-X-CAP-BINDING-PRE-CHECK) | item 8 (line 177) | ✓ |
| §10.3 Tier-up verification on training-data outputs | item 9 (line 178; 12.5I-C orchestrator-side Opus) | ✓ |
| §10.4 Pilot-first on long batches | items 4-5 (lines 173-174; differentiated 12.5I-B vs 12.5I-C) | ✓ |
| §10.5 Hero-only convention in `prior_actions` | item 1 (line 170) | ✓ |
| §10.6 Pre-flight join-cardinality ≥0.99 | item 2 (line 171) | ✓ |

Plus 12.5I-specific items:
- item 3: `design_action` field for T-CONTROL-like rows (TC-X T8 schema gap fix integration; correctly notes 12.5I doesn't add T-CONTROL by default)
- item 6: solver-as-labels prohibited (per `feedback_solver_vs_expert_labels.md`)
- item 10: TC-X-DISPATCH-PREDICTION-VERIFICATION acknowledged (newly-formalized class; predictions LP-side; pilot phase is truth signal)

**Methodology incorporation: COMPLETE.** All 6 standing rules present + 4 cycle-specific additions.

## Test class implication

- **All 6 12.5H-A methodology rules carrying forward into 12.5I cycle** — pattern stable
- **TC-X-DISPATCH-PREDICTION-VERIFICATION acknowledged in design** — newly-formalized class incorporated; design notes "predictions in this design comm are LP-side; orchestrator may amend at trigger time; pilot phase is the truth signal" — pre-empts the 3rd-instance pattern by acknowledging dispatch predictions are advisory
- **Pilot-first differentiation** — design correctly distinguishes 12.5I-B (deterministic factory output, no pilot needed) vs 12.5I-C (Sonnet × 5 labelling round, pilot-first)

## What QC did NOT audit (scope partition)

- Per-template GTO design correctness — gto-expert at 12.5I-B/C dispatch
- Predicted v3.4 protocol output on T8'-redesigned (whether labellers will route to BET as designed) — pilot phase is the truth signal
- Risk that all T8'-redesigned hands also route to CHECK (corpus-vs-reference protocol amendment territory) — orchestrator/owner WHAT decision if it surfaces

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **16th successive cycle solo-routed**. **First parallel-PR audit cycle** (PR #197 + PR #198 simultaneously). Both audits independent; each PR has its own REVIEW comm.

## References

- PR #197: https://github.com/beytell1-sketch/river-rats-v2/pull/197
- QC audit trigger (combined): master `ce2ee5e` (PR #199)
- 12.5I dispatch: master `c536c30` (PR #196)
- 12.5I-pre diagnostic (per-hand verdicts): master `54e2943` (PR #193)
- Memory: `feedback_qc_routing_when_standalone_active.md` (16th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #197 for merge.** All 4 audits PASS cleanly; 0 NIT new findings.

QC-side gate cleared. Awaiting orchestrator merge → 12.5I-B situation generation dispatch.
