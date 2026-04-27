---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · gto-expert · ml-architect · QC stream
re: PR #60 Phase 2 round 2 synthesis — 3-way APPROVE convergence; merging PR #60; build-execute directive next
status: SYNTHESIS — Phase 2 cleared; merge sequence executing
---

# PR #60 Phase 2 round 2 synthesis

## Three-way reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| ml-architect | **PASS** (F1/F2/F3) | F1 V-Integration-Trace fully documented (BB-unit SPR flows through `extract_zero_compute_features` → `add_derived_features`). F2 active. F3 production gate verified at spec bounds. Q2 OOP test skip = non-blocker (test infra gap, not logic gap). No attention-vocab impact. |
| gto-expert | **APPROVE-WITH-NITS** (F4) | 5 redesigned templates follow turn-decision spec with 3 improvements (uniform CO villain, 3-suited boards, calibrated boards). Q1 disposition: **accept 4/5 as designed** — T1/T2 (0.158/0.157) bracket below threshold producing CALL labels; T3/T4 (0.202/0.211) bracket above producing RAISE labels. T5 at empirical ceiling ~0.21 redundant to T4. Other modules verified untouched circumstantially. T1-T4 GTO-realistic; T2 (K-turn converting villain broadway air to top pair) noted instructive. |
| QC | **APPROVE clean** | All 4 fixes V-Implementation-Spec-Match PASS + V-Integration-Trace PASS (TC-26 first application; curative validated). Builder's `test_long_form_keys_cause_keyerror` mirrors V-Integration-Trace recommended pattern (test bug is real before testing fix works). False-positive vigilance: long-form keys at output record schema (lines 164-184) correctly distinguished from input to `extract_all_features`. 2 NITs (non-blocking). |

**Convergent verdict: PR #60 Phase 2 APPROVED. No CHANGES_REQUESTED. NITs only.**

## NITs disposition (non-blocking; tracked as follow-up)

| # | Source | Disposition |
|---|--------|-------------|
| QC NIT 1 | Bare `except Exception:` at `generate_corpus_revision_pool.py:154` could mask future exceptions if new error type introduced | Backlog: tighten to `except (KeyError, ValueError, TypeError):` in next cleanup pass. Not blocking merge. |
| QC NIT 2 | T5 NFD ceiling at ~0.21 — flag for gto-expert mini-review whether 4-template boundary acceptable | **Resolved by gto-expert Q1 disposition: accept 4/5 as designed.** Redundant of T4; loosening creates near-identical templates. Empirical ceiling finding documented as valuable provenance for future revisions. |
| gto-expert Q3 | Non-boundary NFD templates untouched only verified circumstantially (file not in working tree at review time) | **Resolved by QC's V-Implementation-Spec-Match audit** — QC explicitly confirms only 5 boundary templates changed (`nfd_scenarios.py:172-200+`), 4 NFD CALL + 4 NFD RAISE templates untouched. Convergence between gto-expert and QC. |
| Builder Q2 | `TestVerifyCorpusOopBoundsStrict` skip due to scripts/ import path | Backlog: add `scripts/` to `conftest.py` sys.path. Non-blocking (production gate is correct per ml-architect direct read). |
| Builder Q3 | Mode A UTG self-play folds preflop → 0 records | Pre-existing; needs broader position pool. Will surface in build-execute directive (E2 Mode A pool generation must use CO/BTN/BB positions, not UTG). |

## TC-26 V-Integration-Trace milestone

This PR is the **first application** of QC's TC-26 V-Integration-Trace vector class (added in QC PR #62 addendum after ml-architect's BUG 1 catch). The curative loop closed cleanly:
1. ml-architect catches BUG 1 in round 1 (V-Implementation-Spec-Match alone missed integration drift)
2. QC adds TC-26 V-Integration-Trace + commits to standard pre-merge checklist
3. Builder's Phase 2 includes paired tests (`test_short_form_keys_accepted_by_extract_all_features` + regression `test_long_form_keys_cause_keyerror`) that mirror TC-26's recommended pattern (test bug is real BEFORE testing fix works)
4. QC's round 2 audit applies TC-26 in full: paired V-Impl-Spec-Match + V-Integration-Trace, including false-positive vigilance (output record schema vs hand_dict input)

This is the multi-pipeline review architecture working as designed: ml-architect catches what QC missed in round 1; QC self-curates with new vector; builder organically aligns with the new vector; QC validates the curative on first real application.

## Merge sequence (executing now)

```
1. PR #65 (QC round 2 FLAG audit, comms-only)
2. PR #64 (orchestrator directive + builder Phase 2 report)
3. This synthesis PR (new)
4. PR #60 (Phase 2 implementation — F1-F4 + 1 NIT cleanup; head 0b97181)
```

After all 4 merge, master will have:
- F1-F4 fixes in production code
- Round 2 audit trail complete (3 reviews + synthesis)
- TC-26 first-application milestone documented
- Open backlog items tracked

## Build-execute directive (next)

Following PR #60 merge, orchestrator writes build-execute directive for:

| Step | Script | Purpose |
|------|--------|---------|
| E1 | `scripts/reextract_pilot_100_features.py` | R1 re-extract 100 hands from pilot corpus with corrected SPR (BB units) + IS_PFA reconstruction |
| E2 | `scripts/generate_corpus_revision_pool.py --mode b` | Mode B factory pool (111 records) |
| E2 | `scripts/generate_corpus_revision_pool.py --mode a --deals 1000 --positions CO,BTN,BB` | Mode A self-play pool (NOT UTG per builder Q3 — UTG self-play folds preflop) |
| E3 | `scripts/verify_feature_schema_compatibility.py` | R2 v9 baseline 45-feat ↔ 59-feat corpus contract delta |
| C2 | `scripts/build_corpus_revision_500_hand.py` | Assemble 500-hand corpus (100 re-extracted + 400 from pool) |
| Tier 1 | calibration manifest expansion 33→45 | (separate PR; runs in parallel) |

Builder picks up via comm directive (not Agent dispatch). When pool generation completes, structural verification gates fire (OOP 0.55-0.65, ip_pct 0.35-0.45, NFD R4 ±0.03 4/5, etc.). Round 2.5 review on corpus contents before mass labelling kickoff.

## What is NOT changing post-merge

- v3.2 protocol unchanged
- Blueprint v3 unchanged
- 500 Phase A v3.2 labels (preserved from earlier corpus) untouched

## References

- PR #60 head: `0b97181`
- PR #65 (QC round 2 audit): https://github.com/beytell1-sketch/river-rats-v2/pull/65
- PR #64 (directive + builder report): https://github.com/beytell1-sketch/river-rats-v2/pull/64
- Round 2 reviews:
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_PR60_PHASE2_2026-04-27.md`
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_PR60_PHASE2_2026-04-27.md`
  - QC: `~/river-rats-qc/findings/2026-04-27-pr60-phase2-pre-merge-fix-forward.md` + (PR #65 mirror)
- Round 1 synthesis: `review/comms/MAIN_TERMINAL_PR60_REVIEW_SYNTHESIS_2026-04-27.md` (master `6c1e2ab`)
- Builder Phase 2 report: `review/comms/PROGRAMMER_REPORT_BLUEPRINT_V3_PHASE2_2026-04-27.md`
- Blueprint v3: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v3_2026-04-27.md` (master `1086de2`)

**Status: PR #60 PHASE 2 SYNTHESIS COMPLETE. 3-way APPROVE convergence. Merge sequence executing. Build-execute directive next.**
