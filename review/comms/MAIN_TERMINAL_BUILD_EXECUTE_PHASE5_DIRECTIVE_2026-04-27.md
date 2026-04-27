---
date: 2026-04-27
from: Main terminal (orchestrator)
to: ARCHITECT (named designer; Phase 2.7 dispatch) · Reviewer streams · QC stream · Lead-programmer (waits for spec) · Owner
re: Phase 5 directive — scenario module expansion to fill genuine pool yield insufficiencies surfaced by F5; ~150 additional records across 8 modules; architect Phase 2.7 produces design spec
status: DIRECTIVE — Phase 5 design (architect Phase 2.7); blocks Phase 6 build (programmer) until spec converges through review chain
---

# Phase 5 directive — scenario module expansion

## Context

PR #72 F5 (rare-category-first allocator) merged at master `ee92303`. F5 surfaces genuine pool yield insufficiencies for 8 of 12 Phase A categories. The corpus produced by current modules + Mode A self-play caps at ~318 hands; we need 500.

Per Phase 4 directive's deferred decision: with the allocator now correctly tracking per-category yields, we have the data to make module-expansion targets concrete and minimal.

## Yield gap (from F5 empirical run)

| Category | Yield | Target | Gap | Module(s) responsible |
|----------|-------|--------|-----|------------------------|
| pfa | 46 | 80 | +34 | `pfa_scenarios.py` (currently 22 records) + Mode A PFA-tagged self-play yield |
| magg | 10 | 40 | +30 | `magg_scenarios.py` (currently 10 records) — Mode A produces 0 MAGG naturally |
| spr_med | 18 | 40 | +22 | spans modules — SPR 2-4 distribution depends on pot/stack scenarios |
| nfd_raise | 4 | 20 | +16 | `nfd_scenarios.py` (currently 11 records: 7 non-boundary + 4/5 boundary; only 4 fit "RAISE: air >= 0.20") |
| nfd_call | 4 | 20 | +16 | `nfd_scenarios.py` (currently 11; only 4 fit "CALL: air < 0.20" non-boundary) |
| bac | 9 | 20 | +11 | `bac_scenarios.py` (currently 9 records) |
| donk | 15 | 25 | +10 | `donk_bet_defence_scenarios.py` (currently 15 records) |
| sb | 13 | 20 | +7 | `sb_hero_scenarios.py` (currently 12 records) + Mode A SB-positioned records |
| **TOTAL** | — | — | **~150 records across 8 modules** | — |

Categories already meeting target: nfd_boundary (6/10 acceptable per gto-expert), monster, rule11, spr_std. No expansion needed for these.

## Authorization

This directive authorizes **architect Phase 2.7** to produce a scenario module expansion design specification. Architect is design specialist (not builder) — Agent dispatch from orchestrator is sanctioned per established pattern (PR #53, #56, #59 architect dispatches).

Architect produces a single design spec at `review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md` and opens a comm-only PR.

## Design constraints

### Hard constraints (architect must respect)

1. **No new modules.** Expand existing 8 modules. New scenario types belong to v2.3+ backlog.
2. **No protocol changes.** v3.2 prompt + Blueprint v3 module taxonomy unchanged.
3. **PHASE_A_QUOTAS table is the binding contract** (master `ee92303` `scripts/build_corpus_revision_500_hand.py:PHASE_A_QUOTAS`). Architect designs to fill this table, not to revise it.
4. **Each new scenario template must produce a record that satisfies the category's `_is_X_hand` filter** in `build_corpus_revision_500_hand.py`. E.g., new MAGG templates must pass `villain_aggression_count == 2 AND street == 'river'`.
5. **No new feature contract changes.** 59-feature schema is fixed. Templates use existing features.
6. **GTO realism.** Each new template must represent a realistic 3-way poker decision point. Architect collaborates with gto-expert reasoning during design (per gto-expert's prior round 1 + 2 reviews establishing GTO realism standards).
7. **Within-family fingerprint disjointness.** No new template can produce a record fingerprint matching an existing template's record. Architect specifies how (board variation + hero hand variation + action history variation).
8. **Blueprint v3 R5 board texture diversity.** Where applicable (Rule 11 already met; new MAGG/PFA/donk should diversify boards similarly).

### Soft constraints (architect should aim for)

1. **Minimal expansion**: Design ONLY the records needed to fill target. Don't over-expand.
2. **Diverse boards**: New scenarios should use boards not already in existing templates (preferably).
3. **Diverse hero hands**: Within a board, vary hero hands across the strength spectrum (air, weak, medium, strong).
4. **Diverse villain positions**: Where applicable, expand position coverage (e.g., new BAC scenarios with hero as BB, SB, BTN).

## Architect Phase 2.7 deliverable

`review/comms/BLUEPRINT_SCENORIO_MODULE_EXPANSION_v3_5_2026-04-27.md` (note typo correction: `BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md`):

For each of the 8 modules:

1. **Current state**: existing record count + categories satisfied
2. **Target expansion**: number of new records + which categories they fill (some categories cross-fill: PFA records may also be SPR_MED if SPR in 2-4)
3. **Design rationale**: why these new templates fill the gap (GTO realism + uniqueness)
4. **New template list**: 
   - For each new template: hero_position, villain_positions, board, hero_cards, action_history, street, expected feat values that the category's `_is_X_hand` filter checks
5. **Cross-module overlap**: a single record can satisfy MAGG + PFA + SPR_MED. Architect documents which new records serve multiple categories (so total pool growth is minimised).
6. **Verification spec**: per-template assertions (boundary checks, action history validity, fingerprint uniqueness vs existing templates).

Total expected new templates: ~80-120 (some categories share records — e.g. a MAGG template that also satisfies PFA + SPR_MED counts toward 3 quotas, so 30 well-designed MAGG templates can fill 30 MAGG + significant PFA + SPR_MED gap).

## Round 5 review chain (on the spec, not code)

When architect spec PR opens:

1. **gto-expert**: GTO realism of every new template; no card-conflicts; villain ranges plausible; board/position combinations make poker sense (the prior gto-expert round 1+2 reviews established the standard — apply same rigor)
2. **ml-architect**: feature-extraction implications (each new template must produce records that `extract_all_features` handles correctly + features land in expected ranges); cross-module overlap math (does the architect's overlap claim survive empirical extraction?); test design for new templates
3. **QC**: paired V-Implementation-Spec-Match (spec content matches yield gap math) + V-Synthesis-Fidelity (architect's totals add up to fill quotas without over-fill); flag any architectural inconsistencies

Per memory `feedback_qc_required_before_approval.md`: QC must weigh in before merge.

## Round 6 build (programmer phase, after spec converges)

After architect spec PR merges:

1. Builder authors implementation across the 8 module files
2. Tests: at least 1 new test per category proving the new templates produce records that pass `_is_X_hand` filter + 1 cross-module-overlap test if architect's spec uses overlap
3. Smoke test: re-run E2-B against expanded modules → assert pool grows from 115 → ~250-280
4. Re-run C2 against the expanded pool → assert 500-record corpus + per-category report shows FULL on previously-UNDER categories

## Round 7 review on builder PR (data + tests)

gto-expert + ml-architect + QC on the implementation. Same pattern as round 4.

## After C2 produces full 500-hand corpus

PR #70 (DRAFT) gets force-pushed by builder with the full 500-hand corpus + lock file. Round 3 review chain on data PR (already specified in build-execute directive). Then merge → mass labelling kickoff.

## What is NOT in scope for Phase 5

- Mode A `--positions` flag (Phase 6 cleanup deferred)
- Workaround driver script `run_mode_a_pool_with_positions.py` (kept until Phase 6)
- v3.2 protocol changes
- Feature contract changes
- Tier 1 calibration manifest 33→45 (parallel workstream; separate PR)

## Cumulative cost dashboard

- Phase 1-4: ~$300 (orchestration + reviewer dispatches + builder agents)
- Phase 5 architect dispatch: ~$15-25
- Phase 5 round-5 reviews (gto + ml + QC): ~$30-40
- Phase 6 builder: ~$50-100 (8 module expansions + tests)
- Phase 6 round-7 reviews + data PR + round-3 reviews: ~$30-50
- **Phase 5+6 budget: ~$125-215** to reach a usable 500-hand corpus

## References

- F5 PR #72 merge: master `ee92303`
- F5 synthesis: master `0aeb1ec` PR #74
- Phase 4 directive: master `43a80bb` PR #71
- ml-architect F5 review: `review/comms/REVIEW_ML_ARCHITECT_PR72_F5_2026-04-27.md`
- Builder Phase 3 v2 report: `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_2026-04-27.md` (PR #70 branch head `174bbc3`)
- PHASE_A_QUOTAS source-of-truth: `scripts/build_corpus_revision_500_hand.py` (master `ee92303`)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 5 DIRECTIVE OPEN. Architect Phase 2.7 dispatch authorized. Architect produces scenario module expansion spec → round-5 review chain (gto + ml + QC) → spec merge → builder Phase 6 implementation → round-7 review chain → C2 re-run → PR #70 unblocks.**
