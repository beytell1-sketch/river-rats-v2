---
date: 2026-04-27
from: River Rats QC stream
to: Architect (logic-domain) · Main terminal (orchestrator) · ml-architect reviewer · gto-expert reviewer · Owner (briefed)
re: PR #53 pre-merge QC audit — Architect Phase 2 corpus-generation blueprint; APPROVE (clean); all V-Source + V-X1 + V-X4 vectors PASS
severity: APPROVE / no findings
status: FLAG (advisory; pre-merge informational)
---

# QC Pre-Merge Audit — PR #53 (Architect Phase 2 corpus-generation blueprint)

## Headline

**APPROVE clean.** Single-file design blueprint (+772/-0 markdown, 0 code changes). All three root-cause bug claims independently verifiable against master source. SPR unit consistency between existing 100 hands (buggy SPR=1.25) and new 400 hands (corrected SPR=12.5) correctly elevated as **Q1 owner decision** rather than silently assumed.

## Vector results

| Vector | Result |
|--------|--------|
| V-X1 file existence (cited source files + 4 audit comms) | ✅ PASS |
| V-X4 carryforward consistency | ✅ PASS |
| V-Source-1 SPR formula bug at `feature_extractor.py:1643` | ✅ PASS |
| V-Source-2 `_opener_position` metadata gap (Feature 53 line 2499-2505) | ✅ PASS |
| V-Source-3 `_extract_3way_decisions` at `generate_3way_situations.py:31` | ✅ PASS |
| V-Source-4 BAC/MAGG SituationFactory pattern | ✅ PASS |
| V-Cn-action-distribution (Q1 SPR unit consistency flag) | ✅ FLAGGED-TO-OWNER |

## Source-claim verification

### Bug 1 (`is_preflop_aggressor=0` for all 100 hands)
`feature_extractor.py:2499-2505` reads `hand.get('_opener_position', None)`; if pool record's `feat_dict` lacks `_opener_position`, feature defaults to 0 for every hand. Blueprint diagnosis **correct**.

### Bug 2 (SPR=1.25 unit mismatch)
`feature_extractor.py:1566` `DEFAULT_EFFECTIVE_STACK = 100.0`; line 1643 `features['spr'] = round(DEFAULT_EFFECTIVE_STACK / pot, 4)`. Same-unit assumption in formula. Internal unit tests at lines 3578-3589 are self-consistent on synthetic small pots but don't catch real-game unit mismatch (chip-vs-BB). Blueprint diagnosis **plausible**; the 1.25 statistic for 94/100 hands and the proposed fix (convert chips→BB in NEW generator, do NOT modify `feature_extractor.py`) preserve backward-compat for the unit-tests + existing call sites. ✅

### Bug 3 (BAC/MAGG patterns missing from oracle self-play)
`river-rats-core/situation_factory.py` exists; `review/generate_factory_situations.py` exists. Pattern matches Build A/B labeller-facing pilot-artifact verbatim-inlining. ✅

## Recommendations

### To orchestrator's dispatched reviewers (ml-architect + gto-expert)
**APPROVE merge.** All vectors PASS. No findings. Blueprint is design-only with no code modifications.

### To orchestrator (synthesis level — owner-facing)

**Q1 SPR unit consistency**: QC concurs Path A (re-extract 100 with corrected formula) or Path C (fully replace 100, build 500 fresh) over Path B (mix as-is). Path B has high downstream risk:

| Path | Existing 100 | New 400 | Action distribution |
|------|--------------|---------|---------------------|
| A: Re-extract 100 with corrected formula | SPR ~12.5 | SPR ~12.5 | UNIFIED |
| B: Mix as-is | SPR=1.25 | SPR ~12.5 | TWO REGIMES (regime-dependent CHECK/BET/FOLD) |
| C: Discard 100, fully replace | — | SPR ~12.5 | UNIFIED |

Phase B's existing 500-label distribution (CHECK 57-63 / BET 34-40 / FOLD 2-3) was generated on the buggy SPR=1.25 corpus — that distribution is itself regime-anchored to the bug. Path B mixing two SPR regimes contaminates downstream label distribution analysis.

**Q2 v3.3 protocol revision timing**: Wait for Build E source pool sample inspection before deciding v3.3 needed/not. Premature revision risks chasing a phantom gap.

**Q3 Tier 1 expansion as labelling gate**: Tier 1 33→45 readiness should inform Tier 2 mass labelling but does not need to strictly gate it — parallel kickoff possible if Tier 1 is confidently scoped.

### Post-merge sequence (anticipated)
1. Build E source pool PR (corpus-generation pipeline; fixes bugs 1+2 + adds factory-driven BAC/MAGG)
2. Build C2 corpus PR (500-hand on revised pool; per Q1 path: includes re-extracted 100, or fresh-500)
3. Tier 1 calibration manifest 33→45 PR (HIGH-2 fix surface check: constants-by-name discipline)

QC pre-merge audits each via worktree → branch → PR pattern; vector pattern: V-C1...V-C13 + V-X2 + V-X4 + V-D9 + V-Source vectors + V-Cn-action-distribution.

## Process learning — V-Source vector class (new TC-24)

This is the first design-blueprint pre-merge audit. V-Source vector class added to QC `test_class_registry.md`:
- V-Source-1: line-number content match
- V-Source-2: bug-semantic plausibility from cited code
- V-Source-3: function/method signature exists
- V-Source-4: cited file path exists

Distinct from V-X1 (general artifact existence) and TC-23 (pre-dispatch infrastructure). Mechanical grep + line-number verification sufficient for pure-design PRs.

## Reference

- PR #53 head: `e635d003cad0f3f1b8e48a3c7d8df7f5ff790507`
- Master HEAD: `1a5f3e5`
- Blueprint: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md` (772 lines)
- QC full finding: `~/river-rats-qc/findings/2026-04-27-pr53-pre-merge-blueprint-corpus-generation.md`
- Audit speed: ~8 min

**Status: APPROVE clean.**
