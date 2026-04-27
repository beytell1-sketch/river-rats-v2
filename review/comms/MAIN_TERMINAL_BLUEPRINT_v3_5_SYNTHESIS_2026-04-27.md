---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Architect (ack) · Lead-programmer (Phase 6 author next) · gto-expert · ml-architect · QC stream
re: PR #76 round 5 synthesis — 3-way review chain converged with required corrections; merging blueprint v3.5 + this synthesis as a v3.5.1 supplement; Phase 6 builder directive next
status: SYNTHESIS — CHANGES_REQUESTED resolved via inline corrections; merging now; Phase 6 directive next
---

# Blueprint v3.5 round 5 synthesis

## Three-way reviewer convergence

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| **gto-expert** | APPROVE-WITH-NITS | 1 CR (DK-N-06/07 missing BTN preflop call in 8a action history); 4 FLAGs to ml-architect (NFD Ace-on-board, NFD-CALL air verification, PFA-8 turn check-around order, BAC-6a villain_positions ordering); 1 FLAG to orchestrator (donk-pfa allocator overlap risk). All 30 MAGG templates Bug-1-compliant; spr_med SPR math verified; no card conflicts. |
| **ml-architect** | **CHANGES_REQUESTED** | **HIGH**: 3 NFD-CALL templates (C-03, C-09, C-14) have Ace of flush suit on board, not hero — fail `nut_flush_block=1` filter and don't classify as NFD at all (silent failure). nfd_call fills to 17/20. **MEDIUM**: spr_med vs pfa scarcity tie (both 0.9302) post-expansion; spr_med fill not guaranteed. **MEDIUM**: missing generate_scenarios() assertions for NFD/BAC/PFA/DONK (silent-failure prevention; F1-pattern). **LOW**: donk-pfa overlap concern (gto-expert FLAG-5) is moot post-expansion — scarcity inverts (donk 1.00 > pfa 0.93) so donk+pfa records correctly route to donk. Verified correct: MAGG aggression count, NFD-RAISE templates, SPR math, PFA logic, 146-record minimum, attention-vocab safety. |
| **QC** | APPROVE clean | All vectors PASS including new V-Synthesis-Correction (first application). Validates architect's overlap-math correction of Phase 5 directive. 146 record minimum verified; per-module yield gap fix verified; `used_fps` single-cat-assignment verified at `build_corpus_revision_500_hand.py:393`. |

**Convergent net verdict: CHANGES_REQUESTED on 3 NFD-CALL templates + 1 DK action history fix + 4 silent-failure assertions. Other 142 templates approved. Inline corrections (this synthesis) supplement the blueprint as v3.5.1.**

## Inline corrections (v3.5.1 supplement)

The corrections below modify 3 NFD-CALL templates + 2 DK templates + add Phase 6 implementation requirements. Builder applies these during Phase 6 alongside the rest of the blueprint v3.5 specifications.

### Correction 1: NFD-C-03 (HIGH; ml-architect)

**Original**: hero `[Ks, 9s]`, board `[As, 7s, 3d]` → fails `nut_flush_block=1` (Ace on board).

**Replacement**: hero `[As, 9s]`, board `[Ks, 7s, 3d]`.
- Hero holds Ace-spades (nut blocker) + 9s (second suited card) → 2 spades in hand.
- Board has K-spades + 7-spades → 2 spades on board.
- Total: 4 spades, hero has nut flush draw. `has_flush_draw=1`, `nut_flush_block=1`.
- Air target: villain_air_pct < 0.20 (K-high board, value-heavy villain range).
- Builder verification: re-extract feature for this template; confirm air < 0.20 OR re-route to nfd_raise if air ≥ 0.20.

### Correction 2: NFD-C-09 (HIGH; ml-architect)

**Original**: hero `[Kh, Jh]`, board `[Ah, Th, 3d]` → fails `nut_flush_block=1`.

**Replacement**: hero `[Ah, Jh]`, board `[Kh, Th, 3d]`.
- Hero holds Ace-hearts (nut blocker) + Jh → 2 hearts in hand.
- Board has K-h + T-h → 2 hearts on board. 4 hearts total.
- Air target: villain_air_pct < 0.20 (K-T-3 high-card board).
- Builder verifies air pct after extraction.

### Correction 3: NFD-C-14 (HIGH; ml-architect)

**Original**: hero `[Kd, Qd]`, board `[Ad, 9d, 4s]` → fails `nut_flush_block=1`.

**Replacement**: hero `[Ad, Qd]`, board `[Kd, 9d, 4s]`.
- Hero holds Ad (nut blocker) + Qd → 2 diamonds in hand.
- Board has K-d + 9-d (only 2 diamonds for nut FD).
- Air target: villain_air_pct < 0.20 (K-9-4 connected board, value-leaning).
- Builder verifies.

### Correction 4: DK-N-06 + DK-N-07 (CR; gto-expert)

**Original**: `villain_positions=['BB', 'BTN']` but 8a action_history only includes HJ + CO + BB preflop. BTN's preflop call is missing.

**Fix**: prepend `('preflop', 'BTN', 'call')` to the 8a action_history for both DK-N-06 and DK-N-07. The preflop sequence becomes: HJ raise (PFA), CO call, BTN call, BB call. Then postflop: BB donks, hero (CO or BTN) acts.

### Correction 5: silent-failure assertions in generate_scenarios() (MEDIUM; ml-architect)

Builder adds the following assertions to each module's `generate_scenarios()` function (matching MAGG's existing `villain_aggression_count == 2` pattern):

- `nfd_scenarios.py`: `assert all(r['feat_dict']['has_flush_draw'] == 1 for r in records)`; `assert all(r['feat_dict']['nut_flush_block'] == 1 for r in records)`
- `bac_scenarios.py`: `assert all(r['feat_dict']['num_callers_to_bet'] >= 1 for r in records)`
- `pfa_scenarios.py`: `assert all(r['feat_dict']['is_preflop_aggressor'] == 1 for r in records)`
- `donk_bet_defence_scenarios.py`: `assert all(r['feat_dict']['facing_bet'] == 1 for r in records)`

These prevent the F1-pattern silent failure mode: a malformed template silently passes `extract_all_features` but fails category classification downstream.

### Correction 6: spr_med scarcity tie test (MEDIUM; ml-architect)

After expansion, both spr_med and pfa scarcity = 0.9302 (small slack). Builder adds explicit E2-B smoke test:

```python
def test_e2b_pool_spr_med_filled():
    # After regenerating Mode B pool with v3.5 expansions
    pool = load_jsonl('data/corpus_revision_pool_mode_b_2026-04-27.jsonl')
    spr_med_count = sum(1 for r in pool 
                       if 2.0 <= r['feat_dict'].get('spr', 0) < 4.0)
    assert spr_med_count >= 22, f'spr_med yield {spr_med_count} below 22'
```

This catches scarcity-tie shuffle non-determinism before C2 runs.

## Other gto-expert FLAGs (mostly addressed by ml-architect or deferred to builder)

| FLAG | Status |
|------|--------|
| FLAG-1: 2 NFD-CALL Ace-on-board | Subsumed by ml-architect HIGH; corrections 1-3 above (ml-architect found 3, gto-expert spotted 2) |
| FLAG-2: NFD-CALL air verification (C-05, C-06 borderline) | Builder Phase 6 — re-extract feature for ALL 16 NFD-CALL templates; flag any borderline near 0.20 |
| FLAG-3: PFA-8 turn check-around order | Builder Phase 6 — verify SituationFactory accepts the action history; if not, raise BLOCKED |
| FLAG-4: BAC-6a villain_positions ordering | Builder Phase 6 — confirm `['CO', 'BTN']` per Bug 4 convention (CO is bettor, last); test will catch via existing num_callers_to_bet assertion |
| FLAG-5: donk-pfa overlap allocator | Resolved by ml-architect's scarcity-inversion finding — donk-pfa records correctly route to donk post-expansion (donk scarcity 1.00 > pfa 0.93) |

## Merge sequence (executing now)

```
1. PR #77 (QC FLAG audit, comms-only)
2. This synthesis PR (new — includes v3.5.1 supplement)
3. PR #76 (architect blueprint v3.5)
```

Note: the 3 NFD swaps in this synthesis SUPERSEDE the 3 originals in blueprint v3.5. Builder reads both; corrections in synthesis take precedence.

## Phase 6 builder directive (forthcoming)

After this synthesis merges, orchestrator opens Phase 6 directive that operationalises:
- Implement all 146 templates per blueprint v3.5 (with synthesis corrections 1-3 superseding NFD-CALL originals)
- Apply correction 4 (DK-N-06/07 action history)
- Add assertions per correction 5 (4 modules)
- Add E2-B test per correction 6 (spr_med tie test)
- Re-run E2-B → verify pool ≥ 250 records (allowing for 3 NFD swap air re-routing)
- Re-run C2 → verify 500-record corpus (or close — accept 497-500 with explicit per-category UNDER report)

Round 7 review chain on data PR #70 (or successor): gto-expert spot-check + ml-architect feature distribution + QC paired V-Impl-Spec-Match + V-Integration-Trace.

## What is NOT changing

- Other 142 templates (out of 146) approved as-designed
- v3.2 protocol unchanged
- 59-feature schema unchanged
- F5 allocator unchanged
- PHASE_A_QUOTAS table unchanged

## Cumulative cost dashboard

- Phase 1-5: ~$315 (orchestration + reviewer dispatches + builder agents + architect Phase 2.7)
- Round 5 reviews (gto + ml-architect + QC): ~$30
- This synthesis: $0
- Phase 6 builder + round 7 reviews: ~$80-150
- **Phase 5+6 budget: ~$110-180** (within Phase 5 directive's $125-215 estimate)

## References

- Blueprint v3.5: `review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md` (PR #76 head `6872e7b`)
- Round 5 reviews:
  - gto-expert: `review/comms/REVIEW_GTO_EXPERT_BLUEPRINT_v3_5_2026-04-27.md`
  - ml-architect: `review/comms/REVIEW_ML_ARCHITECT_BLUEPRINT_v3_5_2026-04-27.md`
  - QC: `~/river-rats-qc/findings/2026-04-27-pr76-pre-merge-blueprint-v3-5-scenario-expansion.md` + PR #77
- Phase 5 directive: `review/comms/MAIN_TERMINAL_BUILD_EXECUTE_PHASE5_DIRECTIVE_2026-04-27.md` (master `2b0ceff`)
- F5 implementation: `scripts/build_corpus_revision_500_hand.py` (master `ee92303`)
- Memory: `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: BLUEPRINT v3.5 SYNTHESIS COMPLETE. 3-way reviewer convergence with inline corrections. Merging now. Phase 6 directive next.**
