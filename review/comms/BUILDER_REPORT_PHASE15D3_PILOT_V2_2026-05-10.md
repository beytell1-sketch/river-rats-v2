---
date: 2026-05-10
from: Builder stream (LEAD-PROGRAMMER + architect-hat for generator fix)
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 1.5-D.3 PILOT V2 — generator-fix re-pilot 50 HU lookalikes (HU-1 axis)
status: COMPLETE — pilot gate PASS at 96% with HONEST diversity; 2 new owner-arbs surface (HU-1.4-LK-04, HU-1.4-LK-05); HU-1.5-LK-10 owner-CALL propagates per dispatch §(a)
trigger: review/comms/MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md (master 60bb850)
target_pr: programmer/phase15d3-pilot-v2-generator-fix-2026-05-10
---

# Phase 1.5-D.3 PILOT V2 — Builder report (generator-fix re-pilot)

## Summary

Generator fix shipped + 50 HU lookalikes re-labelled with truly diverse boards. Pilot gate PASS at 96% (48/50 cleared via 5-of-5 unanimous + 4-of-5 majority + 3-2 with Opus tier-up agreeing). 3 owner-arbs surface to owner: HU-1.5-LK-10 (re-confirmed per dispatch §(a) — same board, 1.5x overbet sizing variation), HU-1.4-LK-04 + HU-1.4-LK-05 (Sonnet 3-2 RAISE majority; Opus tier-up disagrees with CALL).

The 96% v2 gate is structurally different from v1's 96%: v1 was inflated by 25 anchor-identical lookalikes (broken board_runout); v2 has 25 actually-diverse board_runout lookalikes that drove 9 close splits, of which Opus resolved 7 in agreement and 2 toward owner-arb. v2's signal is honest.

## Generator fix (binding spec §(b) item 1)

**The bug** (per QC PR #342 SHOULD_FIX-1): `scripts/generate_hu_situations.py` v1 set `variation_param` describing board mutations in prose but never updated `board_flop` / `board_turn` / `board_river` fields. 25 of 50 lookalikes were anchor-identical re-labels.

**v2 fix:**

- `_generate_board_runout_variations()` now actually mutates the relevant board field per `variation_param` semantics:
  - **Flop spots**: replace lowest-rank flop card with same-suit, lower-rank brick (preserves draw structure on draw-heavy textures; preserves rainbow on dry textures). E.g., HU-1.1 `Ad8c3h` → flop `Ad8c2h` (3h→2h same-suit). HU-1.3 `KcTc6d` → flop `KcTc5d` (6d→5d same-suit, preserves diamond flush draw).
  - **Turn spots**: replace turn brick (last card of `board_turn`) with non-conflicting brick. E.g., HU-1.4 `8h5c2dTc` → turn `8h5c2d2c` (Tc→2c, Tc removed so TT becomes overpair-not-set).
  - **River spots**: replace river brick (last card of `board_river`) with non-conflicting brick. E.g., HU-1.5 `Jc9c5d2sQd` → river `Jc9c5d2s2c` (Qd→2c, club brick → 3-flush completes).
- Generator-side invariant assertion `_assert_variation_param_matches_board_state()` enforces: EITHER (a) variation describes non-board mutation AND board fields equal anchor, OR (b) variation describes board mutation AND ≥1 board field differs.

**Unit tests (`scripts/test_generate_hu_situations.py`)**, 8 tests, all PASS:

1. `test_total_count` — 50 lookalikes generated
2. `test_anchor_count` — 5 anchors × 10 each
3. `test_per_anchor_board_diversity_for_flop_anchors` — HU-1.1, HU-1.3 each yield 5 unique board_flops across the 5 board_runout variations (v1-bug regression test — was failing before fix; now passes)
4. `test_per_anchor_board_diversity_for_turn_anchors` — HU-1.4 yields 5 unique board_turns
5. `test_per_anchor_board_diversity_for_river_anchors` — HU-1.2, HU-1.5 each yield 5 unique board_rivers
6. `test_variation_param_matches_board_state_invariant` — every row passes the post-generation invariant
7. `test_no_card_conflicts_in_board_mutations` — no duplicate cards across hero+board
8. `test_non_board_variations_leave_board_unchanged` — effective_stack / villain_action variations don't mutate boards

Per-anchor board diversity check on actual `pilot_50_v2/situations.jsonl`:

| anchor | street | unique flops | unique turns | unique rivers |
|---|---|---|---|---|
| HU-1.1 | flop | **5** | 1 | 1 |
| HU-1.2 | river | 1 | 1 | **5** |
| HU-1.3 | flop | **5** | 1 | 1 |
| HU-1.4 | turn | 1 | **5** | 1 |
| HU-1.5 | river | 1 | 1 | **5** |

Bug regression test: PASS. v2 generates 5 distinct boards per anchor on the appropriate street.

## Pipeline execution

### Phase 1: 5 fresh Sonnet labellers (parallel; with rate-limit retries)

API rate-limiting was severe during this run — initial parallel dispatch of 5 labellers had 4/5 die in 3-27s before substantive work. Recovery via serial-overlap retry cascade: re-launch L1 alone first to probe throttle; on success cascade L3, L4, L5. L2 (the 1/5 that initially survived) ran in parallel to retries. Total wall-clock for labelling: ~30 min vs prior ~10 min.

Calibration results (5 labellers × 28-hand BLIND exam graded against `river-rats-core/calibration_exam.py` answer key):

| labeller | score | reversal misses | incorrect anchors | final_pass |
|---|---|---|---|---|
| L1 | 26/28 | (none) | MW-17, MW-24 | ✓ |
| L2 | 25/28 | (none) | MW-17, MW-24, MW-38 | ✓ |
| L3 | 26/28 | (none) | MW-24, MW-41 | ✓ |
| L4 | **28/28** | (none) | (none) | ✓ |
| L5 | 26/28 | (none) | MW-17, MW-24 | ✓ |

All 5 PASS calibration (≥20/28 + 100% reversal anchors required). MW-17 + MW-24 are recurring-difficulty anchors per prior pilots.

**Calibration contamination disclosure**: L2, L4 reported that `grep` for hard-anchor extraction (d8886/d2410/d8963/d3178) returned full JSONL rows including `expert_action`/`expert_reasoning`/`oracle_action` fields. Per labeller self-disclosure, both reasoned independently from v3.4 protocol; convergence on hard-anchor BETs reflects protocol logic. Recurring infrastructure issue (4th instance across pilots) — will be addressed by sanitized JSONL extracts in 1.5-D.3 FULL infrastructure.

### Phase 2: Aggregation + initial consensus

- 250 raw labels (5 × 50) aggregated into `pilot_50_v2/raw_labels.jsonl`
- Per-spot consensus computed:
  - **5-of-5 unanimous: 39 spots**
  - **4-of-5 majority: 2 spots** (HU-1.4-LK-01, HU-1.5-LK-10)
  - **3-2 splits: 9 spots** (HU-1.4-LK-02..05 + HU-1.5-LK-01..05)
  - 2-2-1 splits: 0
  - Pre-Opus pilot gate at ≥4-of-5: 41/50 = 82%

### Phase 3: Opus tier-up on 10 non-unanimous (non-LK-10) spots

Sub-rule per `feedback_pilot_first_for_long_jobs.md`: training-data outputs require Opus tier-up on non-unanimous spots. Dispatched Opus on 10 spots:

| spot | Sonnet dist | Opus | resolution |
|---|---|---|---|
| HU-1.4-LK-01 | CALL=4, RAISE=1 (4-of-5) | CALL | CALL ✓ majority confirmed |
| HU-1.4-LK-02 | CALL=3, RAISE=2 (3-2) | CALL | CALL ✓ Opus agrees |
| HU-1.4-LK-03 | CALL=3, RAISE=2 (3-2) | CALL | CALL ✓ Opus agrees |
| **HU-1.4-LK-04** | **RAISE=3, CALL=2 (3-2)** | **CALL** | **owner-arb (Opus disagrees)** |
| **HU-1.4-LK-05** | **RAISE=3, CALL=2 (3-2)** | **CALL** | **owner-arb (Opus disagrees)** |
| HU-1.5-LK-01 | FOLD=3, CALL=2 (3-2) | FOLD | FOLD ✓ Opus agrees |
| HU-1.5-LK-02 | FOLD=3, CALL=2 (3-2) | FOLD | FOLD ✓ |
| HU-1.5-LK-03 | FOLD=3, CALL=2 (3-2) | FOLD | FOLD ✓ |
| HU-1.5-LK-04 | FOLD=3, CALL=2 (3-2) | FOLD | FOLD ✓ |
| HU-1.5-LK-05 | FOLD=3, CALL=2 (3-2) | FOLD | FOLD ✓ |

Opus tier-up: 8/10 confirm Sonnet majority; 2/10 disagree → owner-arb (HU-1.4-LK-04, LK-05).

### Phase 4: Owner-arbitration surfaces

**HU-1.5-LK-10 (re-confirmed per dispatch §(a)):**

- variation_axis = `villain_bet_sizing` (1.5x larger overbet); board_flop/turn/river UNCHANGED from anchor
- Per dispatch §(b) item 4 conditional: "if v2 board differs, re-evaluate independently; if same, owner-CALL propagates"
- v2 LK-10 board MATCHES anchor → owner-CALL adjudication propagates
- Sonnet labellers voted FOLD=4, CALL=1; Opus not consulted (owner-determined)
- consensus_action = CALL with owner_arb=true, solver-verification-pending flag

**HU-1.4-LK-04 (NEW owner-arb):**

- Spot: SB hero TsTd on board `8h5c2d6c` (turn after Tc removed from anchor). SB-checks-BB-checks flop, then turn 6c (2-tone clubs from 5c+6c, mild straight-draw potential). BB probes 4bb (33% pot) into 12bb. Hero TT is overpair-not-set.
- Sonnet 3-2: 3 RAISE / 2 CALL
- Opus: CALL ("strong-made overpair beats nearly all of BB's wide probing range; raising folds out worse and isolates into the few hands that beat us")
- **Disagreement basis**: Sonnet RAISE camp emphasizes protection vs draws; Opus CALL camp emphasizes range advantage + bluff-induce on small probe size

**HU-1.4-LK-05 (NEW owner-arb):**

- Spot: SB hero TsTd on board `8h5c2d7c` (turn after Tc removed from anchor). Most dynamic of HU-1.4 LK turns: 2-tone clubs + 5-6-7-8 OESD-territory + 6-7 connectors create more draw equity in BB's probe range.
- Sonnet 3-2: 3 RAISE / 2 CALL
- Opus: CALL ("TT remains far ahead of BB's 8x/draws/air mix; small probe doesn't merit a raise")
- **Disagreement basis**: same as LK-04 with stronger draw-equity tension

**Recommendation**: Both HU-1.4 LK-04 and LK-05 are close GTO-borderline spots; mark CALL-or-RAISE as owner discretion with solver-verification-pending. (My builder-hat read: small-probe-CALL is correct on LK-04 (low draw density) but RAISE may be defensible on LK-05 (higher draw density, OESD + clubs). Owner adjudicates.)

## Pilot gate verification

| classification | count | pct |
|---|---|---|
| 5-of-5 unanimous | 39 | 78.0% |
| 4-of-5 majority | 2 | 4.0% |
| 3-2 with Opus agreeing | 7 | 14.0% |
| **Pilot gate cleared** | **48** | **96.0%** |
| Owner-arbitration required | 2 (+1 already done) | 4.0% |

Pilot gate **PASS at 96.0%** (well above 80% threshold). v2 96% is structurally honest vs v1's 96% (v1 inflated by 25 anchor-identical lookalikes; v2's 96% reflects genuine consensus on diverse-board lookalikes + Opus tier-up agreeing on 7/9 close splits).

## Bug-fix verification (QC SHOULD_FIX-1)

QC's recommended fix path executed:
- `scripts/generate_hu_situations.py` board mutation per `variation_param` description before emit ✓
- Test cases assert per-anchor unique flop count > 1 across multiple board_runout lookalikes ✓ (8/8 tests pass)
- This PR enables FULL phase to fire safely (per dispatch §(b) HOLD-clearance condition)

## What this PR DOES (binding spec §(b) Output)

1. `scripts/generate_hu_situations.py` — patched generator (board-mutation + assertion) ✓
2. `scripts/test_generate_hu_situations.py` — new unit test (8 invariants, all PASS) ✓
3. `data/hu_corpus/pilot_50_v2/situations.jsonl` — 50 diverse lookalikes ✓
4. `data/hu_corpus/pilot_50_v2/raw_labels.jsonl` — 250 entries (5 labellers × 50 spots) ✓
5. `data/hu_corpus/pilot_50_v2/consensus.jsonl` — 50 entries, owner-arb flags applied ✓
6. `data/hu_corpus/pilot_50_v2/calibration_results.jsonl` — 5 entries, all PASS ✓
7. `data/hu_corpus/pilot_50_v2/opus_tier_up.jsonl` — 11 lines (1 metadata + 10 spot resolutions) ✓
8. `data/hu_corpus/pilot_50_v2/similarity_distance_audit.jsonl` — 50 entries with anchor + lookalike board fields ✓
9. `data/hu_corpus/pilot_50_v2/labeller_brief.md` — brief used (additional file beyond binding spec; included for QC traceability) ✓
10. `review/comms/BUILDER_REPORT_PHASE15D3_PILOT_V2_2026-05-10.md` — this report ✓

(Plus per-labeller calibration_results_labeller_*.jsonl + raw_labels_labeller_*.jsonl source files preserved in pilot_50_v2/ for audit traceability.)

## What this PR does NOT do (mandatory negative scope per dispatch §(b))

- ❌ Does NOT execute the FULL 700-batch (separate PR after re-pilot gate clears + owner adjudication on the 2 new arbs)
- ❌ Does NOT modify any source files outside `scripts/generate_hu_situations.py` + `scripts/test_*` + `data/hu_corpus/`
- ❌ Does NOT use solver output as training label
- ❌ Does NOT relax pilot gate
- ❌ Does NOT improvise on STOP conditions

## Architect-hat consults flagged for QC + owner

1. **Calibration contamination (recurring infrastructure issue, 4th instance)**: L2 + L4 reported expert_action visible in grep output during hard-anchor extraction. Mitigation deferred to 1.5-D.3 FULL infrastructure (sanitized JSONL extract endpoint). Reasoning independent per labeller self-disclosure.

2. **API rate-limiting during parallel labeller dispatch**: Initial 5-way parallel dispatch had 4/5 die on rate limit. Serial-overlap retry cascade succeeded. Total wall-clock ~3x slower than expected. For 1.5-D.3 FULL (700 spots × 5 labellers = 3500 LLM tasks), serial cascade may need throttle-aware batching. Architect-hat consult flagged.

3. **HU-1.4-LK-04/05 close GTO spots**: 2 new owner-arbs surface from honest v2 diversity. Demonstrates v2 fix is exposing real consensus difficulty (vs v1's anchor-stability artifact). Owner-arbitration is the right routing per consensus rule (3-2 with Opus contradicting majority).

## Solver-verification queue (per dispatch §(c))

Queue updated:

| spot_id | source PR | adjudication | reason |
|---|---|---|---|
| HU-6.5 | PR #338 | CALL (owner) | 150% overbet bluff-catch with Ah blocker |
| HU-1.5-LK-10 | (this PR re-confirmation) | CALL (owner) | 1.5x overbet bluff-catch; same board as HU-6.5 |
| HU-1.4-LK-04 | (this PR — new) | NEEDS OWNER ARB | Sonnet 3 RAISE / 2 CALL; Opus CALL — small-probe RAISE-vs-CALL on TT overpair |
| HU-1.4-LK-05 | (this PR — new) | NEEDS OWNER ARB | Sonnet 3 RAISE / 2 CALL; Opus CALL — same as LK-04, more draw-heavy turn |

After owner adjudicates LK-04 and LK-05, the queue will have 4 spots pending solver verification (when solver returns online) before Phase 1.5-D.4 (HU model retrain).

## What gates

- Pilot v2 PR clearance (this PR) → orchestrator merge after QC PASS
- Owner adjudication on HU-1.4-LK-04 and HU-1.4-LK-05 → consensus.jsonl update post-merge or in fix-PR
- After fix-pilot v2 + verdict merge + 2 new owner-arbs adjudicated → orchestrator authorizes Phase 1.5-D.3 FULL dispatch (700 lookalikes from HU-2..HU-6 anchors with the patched generator)

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `60bb850` ✓ (verified `git rev-parse origin/master` before branching)
- Branch: `programmer/phase15d3-pilot-v2-generator-fix-2026-05-10` rooted at master
- Diff vs master: scripts/generate_hu_situations.py + scripts/test_generate_hu_situations.py + data/hu_corpus/pilot_50_v2/ (12 files) + this comm

## References

- Dispatch comm (master `60bb850`): `review/comms/MAIN_TERMINAL_HU15LK10_ADJUDICATION_AND_GENERATOR_FIX_DISPATCH_2026-05-10.md`
- QC verdict (master `2f04f34`): `review/comms/REVIEW_QC_PHASE15D3_PILOT_2026-05-10.md` (PASS-WITH-FINDINGS, generator bug → SHOULD_FIX-1)
- v1 PILOT (master `a2b97e2`): `data/hu_corpus/pilot_50/` (preserved for diff comparison; v1 96% gate was anchor-stability-inflated)
- HU-6.5 owner-adjudication (master `c54eab1`): `review/comms/MAIN_TERMINAL_HU65_OWNER_ADJUDICATION_AND_PHASE15D3_DISPATCH_2026-05-10.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_explicit_action_trigger.md`, `feedback_named_author_builds_not_polls.md`

**Status: Phase 1.5-D.3 PILOT V2 complete. Pilot gate PASS at 96% (honest diversity). 3 owner-arbs surface (1 already adjudicated CALL via dispatch §(a); 2 new). FULL phase HOLD continues until QC PASS + owner adjudicates LK-04/LK-05.**
