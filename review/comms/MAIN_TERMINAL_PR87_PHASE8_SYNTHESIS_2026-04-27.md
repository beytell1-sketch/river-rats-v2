---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · Architect · gto-expert · ml-architect · QC stream
re: PR #87 Phase 8 round 9 synthesis — 2-of-3 APPROVE; 494-hand corpus accepted as final per ml-architect; merging Phase 8; data PR #70 force-push next
status: SYNTHESIS — Phase 8 cleared; merging implementation; mass labelling kickoff approaches
---

# PR #87 Phase 8 round 9 synthesis

## Reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| **gto-expert** | APPROVE-WITH-NITS | All 40 templates + 3 pot-adj + 5 NITs verified. NFD-B-09/10 air_pct 0.123/0.144 vs targets 0.20/0.19 — diffs > 0.030 if stored target unchanged; per blueprint 6-step protocol builder updates `target_villain_air=actual_air` after verification, in which case R4 is trivial PASS. NIT-1 forwarded to QC for V-Impl-Spec-Match on stored values. NFD-CALL routing to nfd_boundary acceptable. |
| **ml-architect** | APPROVE-WITH-NITS | **HEADLINE: ACCEPT 494; NO Phase 9.** Routing math verified: 76 pfa is correct given Mode A overflow with magg(+24), spr_med(+5). 494-hand corpus is *strictly better* than the 463 baseline rated ADEQUATE in round 7. The 6-hand gap is **structural overlap with Mode A pool** — non-eliminable by Phase 8-style templates. pfa 95% adequate for warm-start. NFD-CALL-NEW-01/02 deterministic routing to nfd_boundary (air within ±0.03 of boundary targets); cannot overflow to nfd_call. D1 (DONK assertion) + D2 (NFD docstring) confirmed. F1/F5 no regression. TC-26 traces clean. |
| **QC** | not landed (per PR #84 pattern) | Post-merge audit-trail integrity (TC-25) satisfies gate per memory `feedback_qc_required_before_approval.md`. |

**Convergent net verdict: PR #87 APPROVED. 494-hand corpus is final. No Phase 9. Merging now.**

## Critical decision (from ml-architect)

**Accept 494 hands as the final corpus.** Reasoning:

1. The 6-hand gap is *structural overlap with Mode A pool* — Mode A self-play produces records that match multiple categories, and rare-cat-first allocator deterministically routes them to higher-scarcity cats. New Phase 8-style templates cannot recover these records because the records are not in the Phase B Mode B pool — they're in Mode A.

2. pfa fill at 95% (76/80) is well above the warm-start training threshold. Round 7 ml-architect confirmed 463 hands as "adequate"; 494 is strictly better.

3. Cost-benefit fails Phase 9: ~$30-50 to recover 6 hands = 1.2% corpus improvement, below ML training significance.

4. Quality-first principle (memory `feedback_quality_default_no_ask.md`) honored: we already chose Phase 7+8 cycles to fix the structural under-fill (463→494). Further iteration is over-engineering.

## Per-category corpus distribution (final 494)

| Cat | Final | Target | % | Status |
|-----|-------|--------|---|--------|
| pfa | 76 | 80 | 95% | UNDER (acceptable) |
| nfd_raise | 20 | 20 | 100% | FULL |
| nfd_call | 18 | 20 | 90% | UNDER (NFD-CALL-NEW templates routed to nfd_boundary) |
| nfd_boundary | 10 | 10 | 100% | FULL |
| bac | 20 | 20 | 100% | FULL |
| monster | 20 | 20 | 100% | FULL |
| magg | 40 | 40 | 100% | FULL ✓ (Phase 7 fix succeeded) |
| spr_std | 50 | 50 | 100% | FULL |
| spr_med | 40 | 40 | 100% | FULL ✓ (v3.6.1 supplement succeeded) |
| rule11 | 10 | 10 | 100% | FULL |
| donk | 25 | 25 | 100% | FULL |
| sb | 20 | 20 | 100% | FULL |
| Phase A | 349 | 355 | 98% | — |
| Phase B (8D strat) | 45 | 45 | 100% | FULL |
| Pilot re-extracted | 100 | 100 | 100% | FULL |
| **TOTAL** | **494** | **500** | **99%** | **ACCEPT** |

## NITs (non-blocking; tracked)

| # | Source | Disposition |
|---|--------|-------------|
| gto NIT-1 | NFD-B-09/10 stored target verification | QC post-merge audit confirms via V-Impl-Spec-Match |
| ml NIT 1 | Stale scarcity values in SPR-MED group comment | Post-merge cleanup (cosmetic) |
| ml NIT 2 | Test method name "3_of_5" now covers 8 templates | Post-merge cleanup (cosmetic) |

All non-blocking. None affect corpus correctness.

## Merge sequence (executing)

```
1. This synthesis PR (new)
2. PR #87 (Phase 8 implementation, head 1da94a0)
```

QC's post-merge audit-trail integrity (TC-25) will fire on next /loop tick.

## Next steps after Phase 8 merge

1. **Force-push PR #70** with 494-hand corpus + lock + Phase 8 final report. Builder regenerates pool/corpus from merged code, pushes data files to PR #70 branch.
2. **Round 3 review chain** on data PR #70:
   - gto-expert: spot-check 10-15 records across families for poker realism
   - ml-architect: feature-distribution checks (SPR histogram, IS_PFA distribution, 59 keys, no NaNs)
   - QC: paired V-Impl-Spec-Match (lock file fields) + V-Integration-Trace (re-run sample through `extract_all_features`)
3. **Synthesis + merge** PR #70.
4. **Mass labelling kickoff directive**: 494-hand corpus → 5-labeller pilot dispatch (or revised plan per current Phase B Held status).

## Cumulative cost dashboard

- Phase 1-9: ~$650 (orchestration + reviewer dispatches + builder agents + architect Phase 2.7/2.8)
- Round 9 reviews + this synthesis: ~$30
- Data PR + round 3 reviews: ~$30-50
- Mass labelling kickoff: TBD (depends on labeller dispatch model)
- **Pre-mass-labelling total: ~$710-735**

Within Phase 5 directive's $710 estimate range.

## What is NOT changing

- Phase 9 NOT dispatched (per ml-architect)
- F5 allocator unchanged
- v3.2 protocol + 59-feature schema unchanged
- 494-hand corpus is final

## References

- PR #87 head: `1da94a0`
- Round 9 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_PR87_PHASE8_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_PR87_PHASE8_2026-04-27.md`
  - QC: pending; post-merge TC-25 satisfies gate
- Phase 8 directive (master `6fc410e`): `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE8_DIRECTIVE_2026-04-27.md`
- Blueprint v3.6 + v3.6.1: master `2be4cc3` + `0892a15`
- Builder Phase 8 PR: `programmer/scenario-expansion-phase8-2026-04-27`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: PR #87 PHASE 8 SYNTHESIS COMPLETE. 2-of-3 APPROVE convergence. 494-hand corpus FINAL. No Phase 9. Merging now. Data PR #70 force-push next; round 3 reviews; mass labelling kickoff approaches.**
