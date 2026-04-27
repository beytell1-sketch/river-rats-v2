---
date: 2026-04-27
from: Main terminal (orchestrator)
to: ARCHITECT (Phase 2.8 dispatch) · gto-expert · ml-architect · QC stream · Lead-programmer · Owner
re: Phase 7 directive — architect Phase 2.8 designs 37 targeted templates filling Phase 6 corpus gap; ml-architect breakdown is binding spec
status: DIRECTIVE — Phase 7 design (architect Phase 2.8); Phase 8 build follows after spec converges
---

# Phase 7 directive — 37 targeted templates

## Context

PR #80 Phase 6 merged at master `7292c7e`. C2 corpus = 463 hands (37 short of 500 target). Round 7 synthesis (master `21848da`) confirmed:

1. **Builder's allocator second-pass diagnosis was WRONG** — 155 unassigned pool records have empty Phase A category membership; second-pass recovers 0 records
2. **F5 allocator is correct**; gap is genuine pool depletion from multi-category routing
3. **Phase 7 fix**: 37 targeted templates designed to AVOID multi-category routing conflicts

## Authorization

This directive authorizes **architect Phase 2.8** to produce the targeted template spec. Small scope vs Phase 2.7 (146→37 templates).

## Binding spec (from ml-architect round 7 review)

ml-architect's exact breakdown is binding:

| Cat | Need | Spec (binding) |
|-----|------|----------------|
| **magg** | +5 | Change 4 MAGG-A templates from pot=50 to pot=52-55 BB (so SPR=1.82-1.92 < 2.0, removing spr_med eligibility); + 1 pure-magg new record |
| **spr_med** | +8 | Pure spr_med (NOT sb-eligible). Hero CO/BTN (NOT SB); pot 26-45 BB; generation_source ≠ 'sb_hero_scenarios' |
| **pfa** | +18 | PFA-only at novel board+position combos, pot 14-24 BB, where villain_aggression_count < 2 (no magg eligibility), no is_3bet_pot complications |
| **nfd_boundary** | +3 | Boundary templates with target air_pct in R4 window 0.15-0.25 ± 0.03. **Empirical verification required** before commit |
| **nfd_call** | +2 | Hero holds Ace of flush suit on **non-hearts** high boards (spades/diamonds/clubs). Manual air_pct verification required (hearts boards reliably air<0.10 — must be non-hearts to ensure air<0.20 holds) |
| **sb** | +1 | 1 additional SB template (21 total to ensure 20 pass after generation failure rate) |
| **Total** | **+37** | — |

## Hard constraints

1. **No new modules** — extend existing 6 modules (magg, pfa, nfd, bac, donk, sb); plus 4 magg pot adjustments
2. **No protocol or schema changes**
3. **PHASE_A_QUOTAS unchanged**
4. **Multi-category routing avoidance** — every new template must be designed so it doesn't compete with higher-scarcity categories. Architect MUST analyse each template's category membership before including.
5. **Phase 2 bug awareness** preserved (MAGG villain=BB, NFD 2 hero suited cards, etc.)
6. **Fingerprint disjointness** with all 261 existing Mode B records + Mode A pool

## Soft constraints

1. **Non-hearts boards** for nfd_call (per ml-architect's hearts-suit finding)
2. **Pot/SPR boundaries** chosen carefully (avoid SPR=2.0 boundary or 4.0 boundary that would push records into wrong categories)
3. **Diverse boards** vs existing templates

## NIT items also addressed in this phase (Phase 8 builder scope)

- **DONK assertion key path verification**: ml-architect noted `facing_bet` may live at record top-level, not in `feat_dict`. Builder verifies and corrects assertion path if needed.
- **NFD module docstring**: Add note about hearts-suit coupling per ml-architect Item 5: *"Hearts boards reliably produce villain_air_pct < 0.10 due to suit-priority heuristic in range expansion (see range_narrowing._parse_hand_to_cards). Use hearts boards for NFD-CALL templates, non-hearts boards for NFD-RAISE templates."*

## Architect Phase 2.8 deliverable

`review/comms/BLUEPRINT_SCENARIO_EXPANSION_v3_6_2026-04-27.md` (small supplement spec).

For each new template:
1. Module + insertion target (existing list to extend)
2. Spec: hero_position, villain_positions, board, hero_cards, action_history, street, pot, to_call
3. Expected feat_dict values
4. **Category membership analysis**: which categories does this record satisfy? Verify it doesn't have higher-scarcity matches that would route it elsewhere.
5. For nfd_boundary + nfd_call: empirical air_pct verification protocol (run extraction before merging)

## Round 8 review chain (on the spec)

- **gto-expert**: poker realism on 37 templates (substantial but smaller than Phase 6's 146)
- **ml-architect**: routing analysis — does each new template actually fill its intended quota without conflict?
- **QC**: paired V-Implementation-Spec-Match + V-Synthesis-Fidelity (totals match 37; routing claims sound)

## Phase 8 build (after spec merges)

Builder implements 37 templates + DONK assertion verify + NFD docstring. Round 9 review chain.

## Pipeline timeline

1. Phase 7 directive (this) → architect Phase 2.8 (~15-25 min)
2. Architect blueprint v3.6 PR open
3. Round 8 reviews (~15-30 min parallel)
4. Synthesis + merge (~10 min)
5. Phase 8 builder (~30-45 min for 37 templates)
6. Round 9 reviews (~20-30 min)
7. Synthesis + merge
8. Re-run E2-B + C2 → expected 500-hand corpus
9. PR #70 force-push
10. Round 3 reviews on data PR
11. Synthesis + merge → mass labelling kickoff

Total Phase 7+8 runway: ~2-3 hours.

## What is NOT in scope

- F5 allocator changes (no — works correctly)
- Mode A regeneration (no — pool sufficient)
- v3.2 protocol changes
- New modules

## References

- Master `7292c7e` Phase 6 implementation
- Round 7 synthesis (master `21848da`): `review/comms/MAIN_TERMINAL_PR80_PHASE6_SYNTHESIS_2026-04-27.md`
- ml-architect round 7 review (binding for breakdown): `review/comms/REVIEW_ML_ARCHITECT_PR80_PHASE6_2026-04-27.md`
- gto-expert round 7 review: `review/comms/REVIEW_GTO_EXPERT_PR80_PHASE6_2026-04-27.md`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 7 DIRECTIVE OPEN. Architect Phase 2.8 dispatch authorized. 37 targeted templates per ml-architect binding breakdown.**
