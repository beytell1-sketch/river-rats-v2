---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Lead-programmer · Architect · gto-expert · ml-architect · QC stream
re: PR #80 Phase 6 round 7 synthesis — 3-way reviewer convergence APPROVE; merging Phase 6; Phase 7 directive (architect Phase 2.8 + 37 targeted templates) next
status: SYNTHESIS — Phase 6 cleared; merging implementation; Phase 7 directive next
---

# PR #80 Phase 6 round 7 synthesis

## Three-way reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| **gto-expert** | APPROVE-WITH-NITS | All v3.5.1 corrections applied correctly. All 5 silent-failure assertions present. Spec adherence good across 6 modules. 463-hand corpus acceptable. **Major flag for ml-architect**: hearts-suit empirical finding — builder used hearts boards for 13 NFD-CALL templates because hearts produce air<0.10. Spurious suit-to-label correlation risk. |
| **ml-architect** | APPROVE-WITH-NITS | Implementation correct. **Critical correction: builder's second-pass proposal CANNOT recover 37 records** — the 155 unassigned pool records have empty Phase A category membership. F5 allocator worked correctly; gap is genuine pool depletion. **Hearts-suit anomaly is NOT a bug** — known deterministic property of `_parse_hand_to_cards` suit iteration `[h, d, c, s]`. AKs expands to Ah+Kh; on hearts boards = flush draw (not air); on non-hearts = air. Builder exploited deliberately. Acceptable for warm-start; document. **DONK assertion nit**: `facing_bet` may live at record top-level not feat_dict — builder should verify. **463 corpus adequate** for warm-start with stratified train/val split. **Phase 7 fix**: 37 targeted templates per breakdown below. |
| **QC** | APPROVE clean (PR #81) | All vectors PASS. |

**Convergent verdict: PR #80 APPROVED. Merge now. Phase 7 fills the 37-record gap.**

## Critical insight from ml-architect

The builder's diagnosis (allocator second-pass would recover records) was **wrong**. The 155 unassigned pool records are records that don't match any Phase A category — they're not eligible for ANY quota. Adding a second pass over them recovers ZERO records.

The genuine fix is **targeted pool expansion** with templates designed to avoid multi-category routing conflicts.

## Hearts-suit empirical finding — ACCEPTED, document

The hearts-suit air_pct anomaly is a **known structural property** of the range expansion heuristic in `range_narrowing._parse_hand_to_cards` (suit priority `[h, d, c, s]`). It's deterministic and predictable. Builder exploited it deliberately:
- Hearts boards → AKs expands to Ah+Kh → flush draw → air<0.10 → routes to nfd_call
- Non-hearts boards → AKs expands to Ah+Kh → no flush context → air → air≥0.20 → routes to nfd_raise

Implication: v9 student model will learn flush_suit=hearts ↔ call-side NFD coupling. Acceptable for warm-start. **Action**: document in `nfd_scenarios.py` module docstring during Phase 7 (so future template authors know).

## Phase 7 targeted template breakdown (per ml-architect)

| Category | Need | ml-architect spec |
|----------|------|-------------------|
| magg | +5 | Change 4 MAGG-A templates from pot=50 to pot=52-55 BB (removes spr_med eligibility since SPR=1.82-1.92 < 2.0); + 1 pure-magg new record |
| spr_med | +8 | Pure spr_med (NOT sb-eligible). Hero CO/BTN (not SB); pot 26-45 BB; not generation_source='sb_hero_scenarios' |
| pfa | +18 | PFA-only at novel board+position combos, pot 14-24 BB, where villain doesn't have aggression_count >= 2 (no magg eligibility), no is_3bet_pot complications |
| nfd_boundary | +3 | Boundary templates with target air_pct in R4 window (0.15-0.25 ± 0.03). Empirical verification required before commit |
| nfd_call | +2 | Hero holds Ace of flush suit on **non-hearts** high boards (spades/diamonds/clubs); manual air_pct verification required |
| sb | +1 | 1 additional SB template (21 total to ensure 20 pass after generation failure rate) |
| **Total** | **+37** | Architect-level design needed to avoid new routing conflicts |

## NITs (non-blocking; tracked)

| # | Source | Disposition |
|---|--------|-------------|
| ml-architect (DONK assertion) | `facing_bet` key path verification | Phase 7 builder verifies and corrects if needed |
| ml-architect (NFD docstring) | Document hearts-suit coupling | Phase 7 builder adds module docstring note |
| ml-architect (training config) | Stratified train/val split for 463 corpus | Track for v9 training phase |
| gto-expert (hearts FLAG-A) | Suit-routing coupling concern | Subsumed by ml-architect's "known property" — accepted |

## Merge sequence (executing)

```
1. PR #81 (QC FLAG audit, comms-only)
2. This synthesis PR (new)
3. PR #80 (Phase 6 implementation, head 481f176)
```

## Phase 7 directive (forthcoming)

After this synthesis merges, orchestrator dispatches **architect Phase 2.8** to design the 37 targeted templates per ml-architect's exact breakdown above.

Architect produces blueprint v3.6 (small supplement spec). Round 8 review chain: gto-expert (poker realism on 37 templates) + ml-architect (allocator routing verification) + QC paired V-Impl-Spec-Match + V-Integration-Trace.

After review chain converges: builder Phase 8 implements 37 templates + DONK assertion verify + NFD docstring note. Round 9 review on Phase 8 PR. Then re-run E2-B + C2 → 500-hand corpus → PR #70 force-push → round 3 reviews → merge → mass labelling.

## Cumulative cost dashboard

- Phase 1-6 + reviews: ~$420
- Phase 7 architect Phase 2.8: ~$10-15 (small scope vs Phase 2.7's $25)
- Round 8 reviews: ~$30
- Phase 8 builder: ~$30-50 (37 templates is ~25% of Phase 6's 146)
- Round 9 reviews + data PR + round 3 reviews: ~$30-50
- **Phase 7+8 budget: ~$100-145**

Total Phase 1-8: ~$520-565 to reach 500-hand corpus.

## What is NOT in scope for Phase 7

- F5 allocator algorithm changes (no — works correctly per ml-architect)
- New modules
- v3.2 protocol changes
- Feature contract changes

## References

- PR #80 head: `481f176`
- Round 7 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_PR80_PHASE6_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_PR80_PHASE6_2026-04-27.md`
  - QC: `~/river-rats-qc/findings/2026-04-27-pr80-pre-merge-phase6-builder-146-templates.md` + PR #81
- Phase 6 directive (master `53eb292`): `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE6_DIRECTIVE_2026-04-27.md`
- Blueprint v3.5 (master `4ca5268`): `review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: PR #80 PHASE 6 SYNTHESIS COMPLETE. 3-way APPROVE convergence. Merging now. Phase 7 directive (architect Phase 2.8 + 37 targeted templates) next.**
