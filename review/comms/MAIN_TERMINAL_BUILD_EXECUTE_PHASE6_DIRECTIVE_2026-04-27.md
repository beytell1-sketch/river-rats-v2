---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · Reviewer streams · QC stream · Owner
re: Phase 6 directive — implement blueprint v3.5 + v3.5.1 corrections; 146 new scenario templates + assertions + tests; re-run E2-B + C2 → unblock data PR #70
status: DIRECTIVE — Phase 6 build (programmer); Phase 7 review chain on builder PR; data PR #70 unblock follows
---

# Phase 6 directive — implement blueprint v3.5 + v3.5.1 corrections

## Context

Blueprint v3.5 merged at master `4ca5268`. Round 5 synthesis (master `76e9f4c`) supplements with v3.5.1 corrections. You (lead-programmer) are named author.

Per memory `feedback_listen_to_orchestrator_always.md`: this directive is sufficient authorization. Per `feedback_named_author_builds_not_polls.md`: your next /loop tick is AUTHORING, not polling.

## Implementation scope

Implement **146 new scenario templates** across 6 modules per blueprint v3.5 + 6 corrections per synthesis.

### Module file changes

Add new template list entries to existing `_*_TEMPLATES` lists in:

| File | New templates | Per blueprint v3.5 + corrections |
|------|---------------|----------------------------------|
| `river-rats-core/corpus_revision_scenarios/magg_scenarios.py` | +52 | 30 MAGG-A (pot 50-75 BB) + 22 MAGG-B (pot 26-45 BB, spr_med overflow) |
| `river-rats-core/corpus_revision_scenarios/pfa_scenarios.py` | +34 | PFA-5 HJ (8) + PFA-6 CO (10) + PFA-7 BTN vs CO+SB (8, BB folds) + PFA-8 turn (8) |
| `river-rats-core/corpus_revision_scenarios/nfd_scenarios.py` | +32 | 16 NFD-RAISE + 16 NFD-CALL (with corrections 1-3 below superseding originals C-03, C-09, C-14) |
| `river-rats-core/corpus_revision_scenarios/bac_scenarios.py` | +11 | BAC-4 (CO bets, BTN calls, BB hero) + BAC-5 (HJ bets, CO calls, BTN hero) + BAC-6 turn |
| `river-rats-core/corpus_revision_scenarios/donk_bet_defence_scenarios.py` | +10 | 6 sub-8c/8d (donk+pfa) + 4 pure donk; DK-N-06/07 with correction 4 |
| `river-rats-core/corpus_revision_scenarios/sb_hero_scenarios.py` | +7 | 4 flop + 3 turn (spr_med range) |

### Synthesis corrections (v3.5.1) — apply during implementation

**Correction 1 — NFD-C-03 swap:**
```python
# REPLACE blueprint v3.5's:
# {'hero_cards': ['Ks', '9s'], 'board': ['As', '7s', '3d'], ...}
# WITH:
{'hero_cards': ['As', '9s'], 'board': ['Ks', '7s', '3d'], ...}  # Ace in hand → nut_flush_block=1
```

**Correction 2 — NFD-C-09 swap:**
```python
# REPLACE: hero ['Kh', 'Jh'], board ['Ah', 'Th', '3d']
# WITH:    hero ['Ah', 'Jh'], board ['Kh', 'Th', '3d']
```

**Correction 3 — NFD-C-14 swap:**
```python
# REPLACE: hero ['Kd', 'Qd'], board ['Ad', '9d', '4s']
# WITH:    hero ['Ad', 'Qd'], board ['Kd', '9d', '4s']
```

**Correction 4 — DK-N-06 + DK-N-07 action history:**
For sub-scenario 8a templates with `villain_positions=['BB', 'BTN']`, prepend BTN's preflop call:
```python
# action_history (per blueprint v3.5):
# (preflop) HJ raise, CO call, BB call → flop BB donk, hero acts
# CORRECTED:
# (preflop) HJ raise, CO call, BTN call, BB call → flop BB donk, hero acts
```
Add `('preflop', 'BTN', 'call')` between `CO call` and `BB call`.

**Correction 5 — silent-failure assertions** in `generate_scenarios()` of each module:

```python
# nfd_scenarios.py generate_scenarios() — add at end:
assert all(r['feat_dict']['has_flush_draw'] == 1 for r in records), \
    "NFD module produced records without has_flush_draw=1"
assert all(r['feat_dict']['nut_flush_block'] == 1 for r in records), \
    "NFD module produced records without nut_flush_block=1"

# bac_scenarios.py:
assert all(r['feat_dict']['num_callers_to_bet'] >= 1 for r in records), \
    "BAC module produced records without num_callers_to_bet >= 1"

# pfa_scenarios.py:
assert all(r['feat_dict']['is_preflop_aggressor'] == 1 for r in records), \
    "PFA module produced records without is_preflop_aggressor=1"

# donk_bet_defence_scenarios.py:
assert all(r['feat_dict']['facing_bet'] == 1 for r in records), \
    "DONK module produced records without facing_bet=1"
```

(MAGG already has `assert villain_aggression_count == 2` — no change needed.)

**Correction 6 — spr_med scarcity tie test** in `river-rats-core/tests/test_corpus_revision_v3.py`:

```python
class TestE2BModeBPoolPostExpansion:
    def test_e2b_pool_spr_med_yield_post_expansion(self):
        """Post-blueprint-v3.5 expansion: spr_med yield must support quota fill
        despite scarcity tie with pfa (both 0.9302).
        """
        path = 'data/corpus_revision_pool_mode_b_2026-04-27.jsonl'
        if not os.path.exists(path):
            pytest.skip(f'{path} not yet generated')
        pool = [json.loads(l) for l in open(path)]
        spr_med = sum(1 for r in pool 
                     if 2.0 <= r.get('feat_dict', {}).get('spr', 0) < 4.0)
        assert spr_med >= 22, f'spr_med pool yield {spr_med} below 22 minimum'
    
    def test_e2b_pool_total_post_expansion(self):
        path = 'data/corpus_revision_pool_mode_b_2026-04-27.jsonl'
        if not os.path.exists(path):
            pytest.skip()
        pool_size = sum(1 for _ in open(path))
        assert pool_size >= 250, f'Mode B pool {pool_size} below 250 (115 + 146 = 261 expected)'
```

## Per-template constraints (recap from blueprint v3.5)

For each new template the builder authors:

1. Hero cards: 2 distinct cards; no conflict with board cards
2. Action history: valid 3-way preflop+postflop sequence; each player acts in turn; folded players excluded postflop
3. Phase 2 bug awareness:
   - MAGG: villain = preflop CALLER (BB) — NOT preflop opener; villain_aggression_count=2 at river
   - NFD: hero holds 2 cards in flush suit; nut_flush_block requires Ace of flush suit IN HAND (corrections 1-3 enforce)
   - SB-hero: BB folded → BB NOT in villain_positions
   - BAC: bridge uses LAST entry in villain_positions as bettor
   - DONK 8b: if CO folded preflop, omit CO from postflop action_history
4. Cross-module fingerprint disjointness: no `(hero_cards_str, board_str)` collision with existing OR new templates

## Verification gates

### Gate 1 — unit tests pass

```
python -m pytest river-rats-core/tests/test_corpus_revision_v3.py
```
Expected: 52 + 5 (correction 5 assertion-trigger tests) + 2 (correction 6 spr_med tests) = ≥ 59 passed; existing 7 skipped pattern preserved.

### Gate 2 — E2-B Mode B pool regeneration

```
python river-rats-core/generate_corpus_revision_pool.py --mode b --output data/corpus_revision_pool_mode_b_2026-04-27.jsonl
```
Expected: pool size ≥ 250 (target 261); per-family breakdown shows expanded counts.

### Gate 3 — NFD air-pct verification (FLAG-2 from gto-expert)

For all 16 NFD-CALL templates (including the 3 swapped via corrections 1-3), spot-check actual `villain_air_pct`:
```python
from river_rats_core.feature_extractor import extract_all_features
# load each NFD-CALL template, build hand_dict, extract, check air_pct < 0.20
```
Report actual air_pct per template. If any NFD-CALL template lands at air ≥ 0.20, that record routes to nfd_raise instead — acceptable, just document.

### Gate 4 — C2 corpus assembly with 500-record target

```
python scripts/build_corpus_revision_500_hand.py \
  --pool data/corpus_revision_pool_combined_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 --seed 20260427 \
  --output data/corpus_revision_500_hand_2026-04-27.jsonl \
  --lock-output data/corpus_revision_500_hand_2026-04-27.lock
```
(Re-create combined pool by concatenating Mode A + new Mode B if your script needs combined input.)

Expected: total ≥ 497 (allow up to 3 NFD swap re-routings); per-category quota report shows FULL on previously-UNDER categories. If any category still UNDER (despite F5 + expansion), report it explicitly — don't manually patch.

## PR

- Branch: `programmer/scenario-expansion-phase6-2026-04-27`
- Files: 6 module files + 1 test file changes only — NO data files (those go to PR #70 force-push after C2 succeeds)
- Title: `Builder Phase 6: scenario module expansion v3.5 (146 templates + 6 corrections)`
- Body: cover what was implemented, gate results, NFD air-pct table

## Round 7 review chain on Phase 6 PR

- **gto-expert**: poker realism on the 146 implemented templates (mostly already audited at blueprint stage; spot-check the 6 corrections + any deviations from blueprint)
- **ml-architect**: feature distribution check (run extraction on small sample); F1/F5 regression check (Mode A SPR still BB-unit; rare-cat-first allocator unchanged); test coverage
- **QC**: paired V-Implementation-Spec-Match (templates match v3.5 + v3.5.1) + V-Integration-Trace (assertions trigger when intentionally malformed; NFD swaps actually pass `_is_nfd_hand` filter end-to-end)

Per memory `feedback_qc_required_before_approval.md`: QC gate before merge.

## After Phase 6 PR merges

Force-push PR #70 (data DRAFT) with the regenerated 500-hand corpus + lock + Phase 6 final report at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_PHASE6_2026-04-27.md`. Round 3 review chain on data PR (gto-expert spot-check + ml-architect distribution + QC paired). Then merge → mass labelling kickoff directive.

## What is NOT in scope for Phase 6

- New modules (out of scope; v2.3+ backlog)
- v3.2 protocol changes (locked)
- F5 allocator changes (no — work as-is)
- Mode A `--positions` flag cleanup (Phase 8 NIT cleanup)
- Tier 1 calibration manifest (parallel separate PR)

## References

- Blueprint v3.5 (master `4ca5268`): `review/comms/BLUEPRINT_SCENARIO_MODULE_EXPANSION_v3_5_2026-04-27.md`
- Synthesis v3.5.1 (master `76e9f4c`): `review/comms/MAIN_TERMINAL_BLUEPRINT_v3_5_SYNTHESIS_2026-04-27.md`
- Round 5 reviews: `REVIEW_GTO_EXPERT_BLUEPRINT_v3_5_*.md`, `REVIEW_ML_ARCHITECT_BLUEPRINT_v3_5_*.md`, `QC_PRE_MERGE_AUDIT_PR76_*.md`
- Phase 5 directive (master `2b0ceff`): `MAIN_TERMINAL_BUILD_EXECUTE_PHASE5_DIRECTIVE_2026-04-27.md`
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`, `feedback_check_comms_before_wait.md`

**Status: PHASE 6 DIRECTIVE OPEN. Builder authors 146 templates + 6 corrections + tests. Round 7 review chain (gto + ml + QC) when PR opens. After merge: data PR #70 force-push with 500-hand corpus → round 3 review → merge → mass labelling.**
