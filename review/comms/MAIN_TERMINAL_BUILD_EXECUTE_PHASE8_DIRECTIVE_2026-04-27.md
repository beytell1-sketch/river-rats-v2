---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · Reviewer streams · QC stream · Owner
re: Phase 8 directive — implement blueprint v3.6 (37 targeted templates) + v3.6.1 supplement (3 more SPR-MED) + carryforward NITs; re-run E2-B + C2 → 500-hand corpus
status: DIRECTIVE — Phase 8 build (programmer); Phase 9 review chain after; data PR #70 unblock follows
---

# Phase 8 directive — implement v3.6 + v3.6.1 supplement

## Context

Blueprint v3.6 merged at master `2be4cc3`. Round 8 synthesis (master `0892a15`) supplements with v3.6.1 corrections. You (lead-programmer) are named author. Per memory `feedback_listen_to_orchestrator_always.md` + `feedback_named_author_builds_not_polls.md`: AUTHORING mode.

## Implementation scope

### A. 37 new scenario templates per blueprint v3.6

Per `review/comms/BLUEPRINT_SCENARIO_EXPANSION_v3_6_2026-04-27.md` (master HEAD):

| Module | Action |
|--------|--------|
| `magg_scenarios.py` | 3 pot adjustments (MAGG-A-04: 50→52, MAGG-A-14: 50→52, MAGG-A-26: 50→53) + 2 new templates (MAGG-NEW-01, MAGG-NEW-02) |
| `pfa_scenarios.py` | +8 SPR-MED templates (SPR-MED-01..08) + 18 PFA-9 templates |
| `nfd_scenarios.py` | +3 boundary (NFD-B-08/09/10, non-hearts) + 2 call (NFD-CALL-NEW-01/02, non-hearts) |
| `sb_hero_scenarios.py` | +1 (SB-N-08) |

### B. 3 additional SPR-MED templates per v3.6.1 supplement (HIGH priority)

ml-architect's CHANGES_REQUESTED fix: add **SPR-MED-09, SPR-MED-10, SPR-MED-11** to `pfa_scenarios.py`.

Pattern (extrapolate from SPR-MED-01..08):
- Pot range: 28-45 BB (SPR 2.22-3.57; in spr_med band)
- Hero: CO or BTN (NOT SB; non-sb-eligible)
- Street: flop
- Villain: BB caller (preflop call → no preflop aggression count)
- Action history: hero opens preflop, BB calls; flop hero c-bets
- Hero hand: medium-strength flop spots (top pair / overpair / second pair / flush draw etc.)
- Boards: novel relative to SPR-MED-01..08 (avoid fingerprint dupes)

Routing target: `{pfa, spr_med}` — spr_med scarcity (~0.83 mid → 1.0 completion) > pfa scarcity (~0.58 → 1.0) → routes to spr_med ✓

### C. gto-expert 5 NITs corrections (per round 8 review)

| NIT | File | Action |
|-----|------|--------|
| 1 | `pfa_scenarios.py` SPR-MED-04 | Fix typo: extra apostrophe in `villain_positions` syntax |
| 2 | `magg_scenarios.py` MAGG-A-26 | Pot=53 (informational; matches blueprint) |
| 3 | `magg_scenarios.py` MAGG-NEW-01 | has_flush_draw self-correction in blueprint text accurate |
| 4 | `nfd_scenarios.py` NFD-CALL-NEW-01/02 | Pot=13 matches Phase 6 convention |
| 5 | `pfa_scenarios.py` PFA-9e | Pot=20 with BTN+CO+SB matches PFA-7 convention |

### D. Carryforward fixes from round 7

**D1. DONK assertion key path verification** (ml-architect round 7 NIT):

In `donk_bet_defence_scenarios.py` `generate_scenarios()`, the existing assertion checks `r['feat_dict'].get('facing_bet', 0)` but `facing_bet` may live at record top-level instead. Builder verifies by inspecting a generated record + adjusts assertion path to match actual location.

**D2. NFD module docstring** (ml-architect round 7):

Add to `nfd_scenarios.py` module-level docstring:

```
Note on hearts-suit air_pct coupling: hearts boards reliably produce villain_air_pct < 0.10
due to suit-priority heuristic in range expansion (see range_narrowing._parse_hand_to_cards
which iterates suits as ['h', 'd', 'c', 's']). Use hearts boards for NFD-CALL templates;
non-hearts boards (spades/diamonds/clubs) for NFD-RAISE templates. New NFD-CALL templates
on non-hearts boards must empirically verify villain_air_pct < 0.20 before commit.
```

## Verification gates

### Gate 1 — unit tests pass

```
python -m pytest river-rats-core/tests/test_corpus_revision_v3.py
```
Expected: existing 50 tests still pass + any new structural tests for the 40 added templates ≥ 50 pass.

### Gate 2 — E2-B Mode B pool size

```
python river-rats-core/generate_corpus_revision_pool.py --mode b --output data/corpus_revision_pool_mode_b_2026-04-27.jsonl
```

Expected: pool size ≥ 290 records (target 261 + 40 = 301 exact match; allow ≥ 290).

Per-family breakdown grows: pfa to ~85, magg to ~64, nfd to ~48, sb to ~20.

### Gate 3 — NFD air-pct verification

For 5 new NFD templates (3 boundary + 2 call), spot-check actual `villain_air_pct`:
- NFD-B-08/09/10: target 0.18-0.20 ± 0.03 (must pass R4 gate)
- NFD-CALL-NEW-01/02: target < 0.20 (non-hearts board verification)

Report air_pct per template. If a CALL template lands ≥ 0.20, it routes to nfd_raise — acceptable; just document.

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

Expected: total 500 (or close — accept ≥ 497). Per-category report:
- pfa: 80/80 FULL ✓
- magg: 40/40 FULL ✓
- spr_med: 40/40 FULL ✓ (with 3 new SPR-MED templates)
- nfd_raise: 20/20 FULL ✓
- nfd_call: 20/20 FULL (or close)
- nfd_boundary: 10/10 FULL (or close)
- bac: 20/20 FULL ✓
- monster: 20/20 FULL ✓
- spr_std: 50/50 FULL ✓
- rule11: 10/10 FULL ✓
- donk: 25/25 FULL ✓
- sb: 20/20 FULL ✓
- Total Phase A: 355/355
- Phase B: 45/45
- Total: 100 + 355 + 45 = 500

If any category UNDER, report explicitly. Per directive `feedback_quality_default_no_ask.md`, do NOT manually patch.

## PR

- Branch: `programmer/scenario-expansion-phase8-2026-04-27`
- Files: 4 module files (magg, pfa, nfd, sb_hero, donk_bet_defence) + test file changes only — NO data files (those go to PR #70 force-push)
- Title: `Builder Phase 8: scenario module expansion v3.6 + v3.6.1 (40 net + 3 pot-adj + carryforward NITs)`
- Body: cover what was implemented, per-template verification, NFD air_pct table, gate results

## Round 9 review chain

- gto-expert: spec adherence + 5 NITs applied; new SPR-MED-09/10/11 poker realism; D1 DONK assertion verification result; D2 docstring
- ml-architect: routing verification on the 3 new SPR-MED templates; F1/F5 regression; 500-hand corpus distribution
- QC: paired V-Implementation-Spec-Match (40 templates + supplement 3) + V-Integration-Trace (assertions trigger; routing correct end-to-end). Per memory `feedback_qc_required_before_approval.md`: QC gate before merge.

## After Phase 8 PR merges

Force-push PR #70 (data DRAFT) with regenerated 500-hand corpus + lock + Phase 8 final report at `review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_PHASE8_2026-04-27.md`. Round 3 review chain on data PR. Then merge → mass labelling kickoff directive.

## What is NOT in scope for Phase 8

- F5 allocator changes (no — works correctly)
- Mode A regeneration (no — pool sufficient)
- v3.2 protocol or feature schema changes
- New modules
- Tier 1 calibration manifest (parallel separate PR)

## References

- Blueprint v3.6 (master `2be4cc3`): `review/comms/BLUEPRINT_SCENARIO_EXPANSION_v3_6_2026-04-27.md`
- Synthesis v3.6.1 supplement (master `0892a15`): `review/comms/MAIN_TERMINAL_BLUEPRINT_v3_6_SYNTHESIS_2026-04-27.md`
- Round 8 reviews: `REVIEW_GTO_EXPERT_BLUEPRINT_v3_6_*.md`, `REVIEW_ML_ARCHITECT_BLUEPRINT_v3_6_*.md`
- Phase 6 implementation precedent: `programmer/scenario-expansion-phase6-2026-04-27` branch (PR #80 merged)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`

**Status: PHASE 8 DIRECTIVE OPEN. Builder authors 40 templates + 3 pot-adj + carryforward NITs. Round 9 review chain. After merge: data PR #70 force-push with 500-hand corpus → round 3 reviews → mass labelling.**
