---
date: 2026-04-27
from: River Rats QC stream
to: Lead-programmer · Main terminal (orchestrator) · ml-architect reviewer · Owner (briefed)
re: PR #72 pre-merge QC audit — F5 rare-category-first allocator; APPROVE (clean); V-Allocator-Multi-Dim first application validates curative
severity: APPROVE clean
status: FLAG (advisory; pre-merge informational)
---

# QC Pre-Merge Audit — PR #72 (F5 rare-category-first allocator)

## Headline

**APPROVE clean.** All vectors PASS. PR #72 cleanly fixes the cited multi-category overlap bug. Builder's `test_magg_records_assigned_to_magg_not_pfa` is the exact regression test; empirical MAGG 0→10 on existing 327-record pool.

## Vector results

| Vector | Result |
|--------|--------|
| V-Implementation-Spec-Match: PHASE_A_QUOTAS module-level dict | ✅ PASS (line 303) |
| V-Implementation-Spec-Match: `_classify_record` + algorithm | ✅ PASS (lines 335, 388-426 match directive Steps 1-4) |
| **V-Integration-Trace** end-to-end | ✅ PASS (MAGG 0→10 empirical) |
| **V-Allocator-Multi-Dim** (TC-26 sub-vector first application) | ✅ PASS |
| Regression test for incident #21 bug | ✅ PASS (test class line 1420; specific test line 1450-1461) |
| Tests: 48 passed + 7 skipped (was 43+7) | ✅ +5 new |

## Empirical end-to-end on production pool

| Category | Target | Greedy | Rare-cat-first | Yield | Status |
|----------|--------|--------|----------------|-------|--------|
| **magg** | 40 | **0** | **10** | 10 | ✅ FIXED |
| rule11 | 10 | 8 | 10 | (≥10) | ✅ FULL (+2) |
| pfa | 80 | 46 | 36 | 46 | regressed -10 (correct redistribution) |

PFA / donk / sb regressions are **correct**: multi-membership records redirected to scarcer categories.

## V-Allocator-Multi-Dim first application

This is the first PR where TC-26's V-Allocator-Multi-Dim sub-vector applies. The sub-vector demands distinguishing:
- **Criterion-match count** (records that COULD go to category X)
- **Bucket-assignment count** (records ASSIGNED to category X)

Builder's `test_magg_records_assigned_to_magg_not_pfa` operationalizes this discrimination: 10 MAGG-AND-PFA + 100 PFA-only pool; assert ≥10 records ASSIGNED to MAGG bucket. Convergence between QC vector design + builder test design = healthy alignment.

## Genuine pool shortfall (Phase 5 input)

Builder cleanly reports yield-limited categories for next directive:
- pfa: 46/80, magg: 10/40, nfd_raise: 4/20, nfd_call: 4/20, bac: 9/20, spr_med: 18/40, donk: 15/25, sb: 13/20, nfd_boundary: 6/10
- Net: ~150 additional records across 9 modules

This is the right output for Phase 5 module-expansion-or-target-relax decision.

## Findings

- **HIGH/MEDIUM/LOW/NIT:** none

## Recommendations

### To orchestrator + ml-architect reviewer
**APPROVE merge.** No findings.

### Post-merge sequence
1. PR #72 merges (allocator F5 sealed)
2. Builder re-runs C2 → updates PR #70 DRAFT data
3. Orchestrator Phase 5 directive: module expansion for 9 yield-limited categories

## Process learning — V-Allocator-Multi-Dim curative validated

Incident #21 (QC's V-Integration-Trace measured wrong dimension on PR #70 MAGG observation) motivated V-Allocator-Multi-Dim. PR #72's regression test independently mirrors the same discrimination. **Curative validated.**

## Reference

- PR #72 head: `31e0a84d4f50c9177362304d4815b494cda2901b`
- Master HEAD: `43a80bb`
- Phase 4 directive: `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE4_DIRECTIVE_2026-04-27.md`
- QC full finding: `~/river-rats-qc/findings/2026-04-27-pr72-pre-merge-f5-rare-cat-first-allocator.md`
- Audit speed: ~7 min

**Status: APPROVE clean. F5 implementation correct; regression test catches incident #21 bug; empirical MAGG 0→10 validates fix.**
