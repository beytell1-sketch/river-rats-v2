---
date: 2026-04-26
from: River Rats QC stream
to: Main terminal (orchestrator) · Logic builder (Pilot Orchestrator persona, currently STANDING DOWN) · Owner (briefed)
re: Phase A HALT @ PRE-DISPATCH gate (4 RED rows, v2 1fb5f04, 16:42 SAST) — QC empirical verification + Phase 5 Layer 1 coverage-gap self-audit + curative TC-23 added; QC concurs HALT correct per spec; recommends Option 1 or 2 (Option 3 = spec violation)
status: FLAG (advisory; orchestrator + owner decide path forward)
severity: HIGH (pilot dispatch BLOCKED until 4 RED rows close); QC FOLLOW-UP within 1 tick of HALT surface (16:42 → 16:46 SAST)
---

# QC FOLLOW-UP — Pilot Phase A HALT @ PRE-DISPATCH gate

## Headline

**QC concurs with HALT.** Pilot Orchestrator's empirical claims independently reproduced by QC. 4 rows RED at PRE-DISPATCH PREREQUISITES gate; spec language unambiguous ("If ANY row is RED: pilot does NOT dispatch. Halt.").

This HALT is **NOT a regression of QC's Phase 5 fixes**. HIGH-1 (`_villain_pos_raw` live-selection) and HIGH-2 (calibration_exam.py v2.3 constants) remain clean — they are Phase A.4/A.5 _content_ checks that depend on the missing infrastructure. The HALT fires _before_ Phase A.1, on rows #2/#3/#5/#6 (corpus + labeller-facing prompts existence).

This is a **NEW finding class for QC.** Phase 5 coverage gap acknowledged + closed via curative addition (TC-23).

## QC empirical verification

```
$ ls prompts/protocol_b_composition_first_v1_0_pilot.md
ls: cannot access ... No such file or directory

$ ls prompts/protocol_c_adversarial_elimination_v1_0_pilot.md
ls: cannot access ... No such file or directory

$ ls prompts/
gto_labeller_v1.md  gto_labeller_v2.md  gto_labeller_v3.1.md  gto_labeller_v3.md
protocol_b_composition_first_v1_0.md  protocol_c_adversarial_elimination_v1_0.md
stage4_drafts/

$ find . -maxdepth 4 \( -name "*pilot*100*" -o -name "*pilot_corpus*" -o -name "*stage4*corpus*" \)
(empty)
```

Source design artifacts exist (`protocol_b_composition_first_v1_0.md`, `protocol_c_adversarial_elimination_v1_0.md`); labeller-facing `_pilot.md` artifacts and pilot 100-hand corpus do NOT exist in v2 master at `1fb5f04`.

## Phase 5 Layer 1 coverage gap

**This class of issue slipped past QC's Phase 5 sweep.** The sweep examined:

- Layer 1: spec-vs-spec internal consistency + cross-reference correctness within `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.2 + earlier
- Layer 2: spec-vs-infrastructure CODE drift (caught HIGH-2 calibration_exam.py manifest version mismatch via constants-by-name discipline)
- Layer 3: pilot-runtime watch framework (would have caught HIGH-1/HIGH-2 fix-surface regressions during Phase A)

**Not checked:** whether infrastructure files referenced by spec rows #2/#3/#5/#6 actually existed in the working tree. Phase 5 row-text consistency check ≠ row-target existence check.

**Per `feedback_spec_vs_infrastructure_code_drift.md` (queued from Phase 5 HIGH-2):** principle was "verify spec citations against actual file contents." Extended here to: when a spec cites infrastructure file _paths_ that should exist by dispatch time, verify those files actually exist.

## Curative addition — TC-23

QC artefacts updated this tick:

- `~/river-rats-qc/learning/test_class_registry.md` — TC-23 added
- `~/river-rats-qc/learning/incident_pattern_library.md` — incident #17 added
- `~/river-rats-qc/learning/curative_additions_log.md` — curative entry #1

**TC-23 scope:** When a spec defines a PRE-DISPATCH-class gate referencing files that should exist (labeller-facing `_pilot.md` prompts, pilot corpus files, retrain manifests, calibration artifacts), verify each referenced path exists in the working tree at master HEAD as part of any pre-merge audit of that spec.

**Trigger:** All future pre-merge audits of pilot-orchestration-class / dispatch-class specs; pre-milestone sweeps before owner-gated transitions.

## QC opinion on path forward

QC defers scope/sequencing to orchestrator + owner per FLAG-only role. Brief read on the three options offered in HALT comm:

| Option | Read | Recommend |
|--------|------|-----------|
| Option 1 — build artifacts as continuous pre-dispatch work (~2-4h) | Clean. Build A (Protocol B `_pilot.md`) + Build B (Protocol C `_pilot.md`) parallelizable; Build C (pilot 100-hand corpus) sequential since stratification is a scope decision | ✓ |
| Option 2 — reframe as Stage 4 Tasks 6/7/8 | Equivalent artifact outputs; standing-per-batch protocol overhead vs continuous | ✓ |
| Option 3 — remove rows from PRE-DISPATCH gate | NOT recommended. Rows are load-bearing per HALT comm §"Why this halt is correct" — design artifacts inherit-by-reference would break labelling contract; corpus overlap would invalidate Stage 6 evaluation + introduce information leakage | ✗ |

**Option 1 or 2 ≡ clean path forward. Option 3 = spec violation.**

## QC pre-merge audit standing offer

For each new pilot-prep artifact under whichever path orchestrator chooses, QC will pre-merge audit using TC-23 + standard pattern (consistent with prior 7 pre-merge audits this date — PR #21/#22/#24/#26/#28/#29/#31):

- **Build A/B (`_pilot.md` files):** verify verbatim-inlining against source design artifact (taxonomy + features + DO NOT rules sections); verify no inheritance-by-reference paragraphs remain; verify reviewer-required content present.
- **Build C (pilot 100-hand corpus):** verify stratification dimensions; verify disjointness against Stage 6 holdout (hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`) and v2.3 calibration manifest (28 + 10 = 38 hands); verify file lives in expected location per spec rows #2/#3.

Multi-expert TC-15 protocol-diversity available for any of these (corpus stratification in particular benefits from multi-framing audit).

## Cross-stream impact

- Logic builder (Pilot Orchestrator persona): STANDING DOWN per HALT comm; awaiting orchestrator direction.
- Teaching builder: not directly affected.
- Game builder: not directly affected.
- QC stream: pilot-runtime monitoring mode preserved; transitions back to pre-pilot sweep mode for Builds A/B/C pre-merge audits as orchestrator dispatches them; resumes pilot-runtime monitoring on re-issued Phase A directive.

## Post-resolution validation

After all 4 RED rows close to GREEN:
- Pilot Orchestrator re-issues PRE-DISPATCH check; 14 GREEN + 2 UNCERTAIN-pending-A1/A2 expected
- Phase A.1-A.6 begins per spec
- QC pilot-runtime watch resumes per `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`

## References

- HALT comm: `PILOT_PHASE_A_HALT_PREREQ_GAPS_2026-04-26.md` (v2 master `1fb5f04`)
- Pilot dispatch authorization: `MAIN_TERMINAL_PILOT_DISPATCH_AUTHORIZED_PROCEED_2026-04-26.md` (v2 `082336d`)
- Spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 (master `c4f29a5`)
- QC pilot-runtime watch: `~/river-rats-v2/review/comms/QC_PILOT_RUNTIME_WATCH_2026-04-26.md`
- QC FOLLOW-UP full finding: `~/river-rats-qc/findings/2026-04-26-pilot-halt-prereq-gaps-followup.md`

**Status: QC concurs HALT correct. Phase 5 Layer 1 coverage gap acknowledged + closed via TC-23. Awaiting orchestrator + owner path-forward directive. QC standing by for pre-merge audits on Builds A/B/C as dispatched.**
