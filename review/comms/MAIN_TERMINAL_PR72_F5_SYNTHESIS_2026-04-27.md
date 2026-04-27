---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · ml-architect · QC stream
re: PR #72 F5 allocator round 4 synthesis — 2-way APPROVE + QC clean; merging F5; Phase 5 module-expansion next
status: SYNTHESIS — F5 cleared; merging implementation; Phase 5 directive next
---

# PR #72 F5 round 4 synthesis

## Reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| ml-architect | **APPROVE-WITH-NITS** | Algorithm correctness verified vs directive spec. Empirical C2 re-run independently confirms MAGG bucket fills 10/40. **Key nuance: old allocator's MAGG=0 was a Phase A bucket-tracking bug — the 10 MAGG records WERE in the output corpus (counted via PFA bucket).** F5 corrects bucket-tracking accuracy, enabling correct Phase 5 module-expansion decisions. PFA/donk/sb "regressions" expected (records correctly redistributed by scarcity). 3 NITs: no test for zero-category records in mixed pool, no test for non-empty forbidden_fps input, no test for zero-yield categories. |
| QC | **APPROVE clean** | F5 V-Implementation-Spec-Match PASS + V-Integration-Trace PASS. Builder's `test_long_form_keys_cause_keyerror`-style regression test mirrors V-Integration-Trace pattern (test bug is real before testing fix). 2 NITs in QC PR #73 (non-blocking). |
| gto-expert | not dispatched | Per Phase 4 directive: allocator algorithm is not poker-domain; gto-expert overkill. |

**Convergent verdict: F5 APPROVED. NITs only.**

## Critical insight from ml-architect

The "MAGG=0/40" headline that motivated Phase 4 was strictly a **Phase A bucket-tracking** error, not a corpus content error. The 10 MAGG records WERE in the 313-hand corpus (allocated to the PFA bucket which fills first). The fix's value:

1. **Phase A reporting accuracy**: Now we see TRUE per-category yield (MAGG yield 10, target 40 → underfilled by yield, not by allocator)
2. **Phase 5 decision quality**: Module-expansion targets must be calibrated against TRUE yields, not bucket-shifted yields. F5 unblocks this decision.
3. **Output corpus delta is +5 records (313→318)**: Marginal, because most Phase A records were already being captured (just into wrong buckets). The corpus content quality is similar; the labelling/tracking quality is much higher.

This sharpens the Phase 5 scope: we are NOT recovering "lost" MAGG records; we are expanding the underlying scenario modules to actually produce 40 MAGG, 80 PFA, 20 NFD-RAISE, etc.

## NITs (non-blocking; tracked as backlog)

| # | Source | Disposition |
|---|--------|-------------|
| ml-architect NIT 1 | No test for zero-category records in mixed pool | Backlog: add to Phase 5 test additions |
| ml-architect NIT 2 | No test for non-empty `forbidden_fps` input | Backlog: add to Phase 5 test additions |
| ml-architect NIT 3 | No test for zero-yield categories | Backlog: add to Phase 5 test additions |
| QC NIT 1 (from PR #73) | 2 minor (specifics in QC finding) | Track in Phase 6 cleanup |

All 4 NITs land in backlog; none block merge.

## Merge sequence (executing now)

```
1. PR #73 (QC FLAG audit, comms-only)
2. This synthesis PR (new)
3. PR #72 (F5 implementation, head 31e0a84)
```

PR #70 (DRAFT data PR) remains DRAFT; will be force-pushed by builder after Phase 5 module expansion produces full 500-hand corpus.

## Phase 5 directive (next)

After F5 merges, orchestrator dispatches **architect Phase 2.7** to design scenario module expansion targeting the genuine pool yield insufficiencies that F5 surfaced:

| Category | Yield | Target | Need |
|----------|-------|--------|------|
| pfa | 46 | 80 | +34 |
| nfd_raise | 4 | 20 | +16 |
| nfd_call | 4 | 20 | +16 |
| bac | 9 | 20 | +11 |
| magg | 10 | 40 | +30 |
| spr_med | 18 | 40 | +22 |
| donk | 15 | 25 | +10 |
| sb | 13 | 20 | +7 |
| **Total need** | — | — | **~150 additional records** |

This is a substantial scope expansion across 8 scenario modules. Architect designs the spec; gto-expert mini-review on poker realism of new templates; ml-architect on extraction/feature contract; QC on V-Implementation-Spec-Match. Then builder implements.

After Phase 5 module expansion lands + re-run E2-B + re-run C2 → expected 500-hand corpus → PR #70 (DRAFT) unblocks → round 3 review chain → merge.

## What is NOT changing

- v3.2 protocol unchanged
- Blueprint v3 unchanged (the PHASE_A_QUOTAS table is the binding contract; Phase 5 makes scenarios match the contract, not vice versa)
- 100 re-extracted pilot hands untouched
- Mode A pool (212 records) untouched (will be regenerated post-Phase 5 with cleaner --positions flag from Phase 6)

## References

- F5 PR #72: head `31e0a84`
- QC round 4 audit: `~/river-rats-qc/findings/2026-04-27-pr72-pre-merge-f5-rare-cat-first-allocator.md` + PR #73
- ml-architect round 4 review: `review/comms/REVIEW_ML_ARCHITECT_PR72_F5_2026-04-27.md`
- Phase 4 directive: `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE4_DIRECTIVE_2026-04-27.md` (master `43a80bb`)
- Builder Phase 3 v2 report: `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md` (PR #70 branch head `174bbc3`)
- Memory: `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: PR #72 F5 SYNTHESIS COMPLETE. 2-way APPROVE + QC clean. Merging now. Phase 5 directive (architect Phase 2.7 scenario module expansion) next.**
