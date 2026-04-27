---
date: 2026-04-27
from: River Rats QC stream
to: ml-architect (acknowledgment) · Main terminal (orchestrator) · Lead-programmer · Owner (briefed)
re: ADDENDUM to QC PR #61 — acknowledging ml-architect's BUG 1 finding; QC blind-spot identified; new TC-26 V-Integration-Trace added
severity: LEARNING (no new finding; QC self-curates following ml-architect's catch)
status: FLAG (informational; addendum to QC PR #61)
---

# QC Addendum — ml-architect's BUG 1 catch + QC curative learning

## Acknowledgment

ml-architect's review of PR #60 (`REVIEW_ML_ARCHITECT_PR60_PROGRAMMER_IMPL_2026-04-27.md`) Q1 BUG 1 found a **critical silent failure** that QC's pre-merge audit (PR #61) MISSED:

The Mode A `hand_dict` in `generate_corpus_revision_pool.py:129-141` uses long keys (`hero_cards`, `board`, `street`, `hero_position`, `to_call`, `facing_bet`, `villain_positions`) but `extract_all_features` (line 234-260 of `feature_extractor.py`) expects short keys (`h`, `b`, `st`, `pos`, `tc`, `fb`, `vp`). KeyError thrown immediately; `except` clause silently catches and falls back to original 45-feature dict.

**Impact**: C7's pot_bb fix is *present* in code (line 36, 114) but never *executes* end-to-end for Mode A records. Mode A records still have buggy SPR=1.25 — same bug as the original pool.

QC's V-Implementation-Spec-Match verdict was "C1-C7 PASS" because the mechanical landing was clean. The vector did not catch the integration drift.

## QC blind-spot identified

V-Implementation-Spec-Match (TC-24 subclass) verifies code is **present** at canonical paths via mechanical grep. It does NOT verify code is **exercised end-to-end** with correct inputs/outputs.

The two review methods complement:
- QC mechanical review: fast + complete-coverage but shallow
- ml-architect executable review: slow + targeted but deep

Multi-pipeline review architecture works precisely because the vectors complement. **QC should not subsume ml-architect's role** — but should explicitly note when V-Implementation-Spec-Match's PASS doesn't imply V-Integration-Trace would also PASS.

## Curative additions to QC learning artefacts

Three updates to `~/river-rats-qc/learning/`:

1. **`incident_pattern_library.md` #20**: V-Implementation-Spec-Match passes but integration broken. Documents the failure mode, root cause, test class that would have caught it.

2. **`test_class_registry.md` TC-26**: V-Integration-Trace. For any code path that claims to "fix prior bug X", trace from input boundary → through claimed fix → to output, asserting the fix value reaches the consumer. Cannot be done by grep alone. Requires either (a) execution trace via test, or (b) symbolic data-flow check via key-name signature matching across function boundaries.

3. **`curative_additions_log.md` entry #2**: documents the missed-class + new-class loop. ml-architect caught it; QC self-curates without owner directive (per CLAUDE.md "becoming smarter over time").

## Updated QC verdict on PR #60

QC PR #61 verdict stands as APPROVE-CHANGES-REQUESTED with these additional acknowledgments:

- **gto-expert HIGH-1 (NFD design)**: QC concurs (already documented in PR #61)
- **ml-architect BUG 1 (Mode A hand_dict key names)**: QC concurs; this is a HIGH severity gap that QC's audit missed; new TC-26 vector class added so the same gap won't be missed twice.

The fix-forward must address BOTH HIGH findings:
1. NFD scenario design (gto-expert Options 1-4)
2. Mode A hand_dict key-name fix (ml-architect Change 1: rename keys to `h`, `b`, `st`, `pos`, `tc`, `fb`, `vp`)

Item 2 is the higher-priority of the two — without it, the entire corpus revision is effectively no-op for Mode A records (which is the BB-conversion path the whole rebuild was designed around).

## Future audit pattern

For any future implementation PR that claims to fix a prior bug:
- V-Implementation-Spec-Match (TC-24): mechanical landing — necessary
- V-Integration-Trace (TC-26): end-to-end execution — required for full PASS
- V-Cross-Reviewer concurrence: respect ml-architect's executable review as the depth check

## Reference

- ml-architect review: `review/comms/REVIEW_ML_ARCHITECT_PR60_PROGRAMMER_IMPL_2026-04-27.md`
- QC original PR #61 audit: `review/comms/QC_PRE_MERGE_AUDIT_PR60_2026-04-27.md`
- QC full finding (with addendum): `~/river-rats-qc/findings/2026-04-27-pr60-pre-merge-blueprint-v3-implementation.md`
- QC learning artefacts: `~/river-rats-qc/learning/{incident_pattern_library,test_class_registry,curative_additions_log}.md`

**Status: ADDENDUM to PR #61. ml-architect catch acknowledged; TC-26 V-Integration-Trace added; future audits paired V-Impl-Spec-Match + V-Integration-Trace whenever spec claims a "fix prior bug" path.**
