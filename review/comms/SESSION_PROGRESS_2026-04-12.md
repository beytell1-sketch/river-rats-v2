---
date: 2026-04-12
from: Main terminal (orchestrator)
to: Owner (Rupert)
re: Full session progress — Phase 0 through prep completion, current state and next steps
status: FOR REVIEW
---

## Session summary

This session started with the owner asking for a plan/blueprint/comms/
file-status audit of the River Rats v2 project. It evolved into a
major commit sweep (Phase 0), a full training-pipeline unblock
(Phase B), and a 4-step diagnostic prep cycle. The project moved
from a dirty working tree with ~200 untracked files and 8 failing
tests to a clean committed state with 960 passing tests and a
verified 6% 3-way yield.

---

## Timeline

| Phase | Commits | Key outcome |
|---|---|---|
| **Audit** (session start) | — | 4 parallel Explore agents audited plans, blueprints, comms, file status. Original audit had a partial-read error (BLUEPRINT_V3.1 misdiagnosed as "partial" when features were implemented but uncommitted). Corrected by direct verification. |
| **Phase 0** (commit sweep) | 18 commits (55d6e3b → 6cbde41) | Resolved ~200 untracked files + 24 modified tracked files. Test delta: 894→895 pass, 16→8 fail. KB v1.3 cutover committed. Features 49-53 committed. Variant evolution infrastructure committed. |
| **Phase B** (preflop range fix) | 3 commits (1f9f739 → c4f2f39) | Solver-backed mixed frequencies replaced flat 1.0 ranges. Yield: 0.51%→6%. Tests: 895→960 pass, 8→0 fail. Latent get_3bet_range() duplicate-method bug fixed. THREEB dead dict removed. |
| **Prep steps 1-4** | 1 commit (ef084a1) + 1 commit (prep memo) | Diagnostic fix (FOLD-without-bet filter). Multi-seed yield verified (4.9-7.0%, mean 6%). Oracle probe: 63% model passive bias confirmed. Feedback memo saved. |

**Total commits this session: 24**

---

## What shipped

### Knowledge base
- **KB v1.3** (55d6e3b): purged capped/uncapped vocabulary, reframed
  on composition triple. Full audit chain: edit plan → review →
  meta-review → fixes → spot-check → cutover.

### Feature surface
- **Features 49-53** (1673c2c): hero_range_percentile, has_showdown_value,
  villain_fold_equity_estimate, flush_draw_rank, is_preflop_aggressor.
  Plus flush_block_pct bug fix (hero with 2 flush-suit cards still blocks).
  Plus validate_action_sequence() postflop order validator.
- **Feature count state:**
  - feature_extractor.FEATURE_COLUMNS: 52 (CSV export)
  - gto_model.FEATURE_COLUMNS: 53 (+is_preflop_aggressor)
  - sizing_oracle: 48 (unchanged)
  - train_model: 48 (retrain on 53 is a v2.2 decision)

### Training pipeline
- **48-feature contract** (a07bbd9): train_model.py and
  train_sizing_model.py expanded from 38→48 features. XGBoost
  hyperparameters tuned (n_estimators 500→800, depth 6→5,
  lr 0.1→0.05). RAISE class weighting capped at 3.0.
- **MW-42 action history fix** in reference_evaluator.py.

### Game engine
- **Headless mode + per-player oracles** (0e0c91a): poker_game.py
  supports headless self-play with per-player decision callbacks,
  deck override, and street_actions tracking.
- **Parameterized multiway adjuster** (0e0c91a): get_default_params()
  + adjust(params=...) for variant evolution hypotheses.

### Preflop ranges (Phase B)
- **Solver-backed mixed frequencies** (1f9f739): RFI/THREE_BET/CALL
  dicts replaced with GTO Wizard 100bb data. UTG 17.6%, HJ 21.4%,
  CO 27.8%, BTN 43.5%, SB 43%. Mixed frequencies on boundary hands
  (66 UTG=0.5, 55 UTG=0.25, etc.).
- **SB 3-bet-or-fold enforced** across plan, engine, tests, and
  range data.
- **THREEB dead dict removed**, stale get_3bet_range() duplicate
  removed (latent bug fix).
- **Yield: 4.9-7.0%** (mean 6%) verified across 6 seeds × 2000 deals.

### Infrastructure
- **Variant evolution pipeline** (6f1d05b): variant_evolver.py,
  convergence_checker.py, decision_comparator.py, observer.py,
  hand_logger.py, personality_profiles.py, run_eval/run_round scripts.
- **115 new tests** for the above + game_state_bridge, action history,
  oracle router, headless game, self-play.
- **12 research documents** tracked (50+ sources each).
- **94 review/comms memos** tracked (full audit trail).
- **Training data snapshots** tracked for reproducibility.

### Diagnostic + data quality
- **FOLD-without-bet filter** (ef084a1): model error filtered out
  of training data pipeline.
- **Oracle passive bias quantified**: 63% of check-to-hero 3-way
  spots have BET prob < 0.05 (model-driven, not adjuster).
- **Adjuster impact**: kills 4/17 model-BET predictions (24% kill
  rate), mostly via value_tightening rule at equity < 0.40.

---

## Test suite state

| Metric | Session start | After Phase 0 | After Phase B | After prep |
|---|---|---|---|---|
| Pass | 894 | 895 | 960 | 960 |
| Fail | 16 | 8 | 0 | 0 |
| Skip | 47 | 47 | 47 | 47 |

**Excluded from counts** (pre-existing, unrelated to any session work):
- `test_explain_hand.py` — XGBoost/SHAP native crash
- `test_oracle_shap.py` — XGBoost/SHAP native crash

**Tests that flipped during session:**
- 8 stale feature-count assertions (48→52/53) — fixed in Phase 0
- 3 SB squeeze CALL tests deleted (wrong per SB policy) — Phase B
- 3 new SB-folds + BTN-implied-odds tests added — Phase B
- 48 test_range_manager_preflop tests unblocked (CALL_VS_OPEN fix) — Phase B
- test_broadway_board_has_high_tp_plus threshold recalibrated — Phase B
- test_hu_with_opener_pos_unchanged tolerance widened — Phase B
- test_game_state_bridge shape 48→53 — Phase B

---

## Bugs found and fixed

| Bug | Severity | How found | Fix |
|---|---|---|---|
| Stale `get_3bet_range()` reading from dead THREEB dict | HIGH — `get_defend_range()` silently returned wrong range data for all defender-range calls | Blueprint execution (edit 3b) | Remove stale duplicate method definition |
| FOLD-without-bet in training data | MEDIUM — produces corrupted training rows | Reviewer caught diagnostic contradiction (O3) | Filter in generate_3way_situations.py |
| `CALL_VS_OPEN` import error | LOW — test collection crash | Phase B investigation | Module-level alias `CALL_VS_OPEN = CALL` |
| Feature-count assertions stale | LOW — test failures | Phase 0 audit | Updated 48→52/53 across 3 test files |
| SB squeeze tests incorrect | LOW — tests asserted wrong SB policy | Phase B research confirmed SB 3-bet-or-fold | Tests replaced with correct assertions |

---

## Findings that affect v2.2 direction

### 1. Oracle passive bias is real and quantified

63% of check-to-hero 3-way spots: model assigns BET probability
< 0.05. This is not adjuster over-correction — it's the model's
own learned passivity. The known reference-set failures (MW-25,
MW-40: BET→CHECK) are instances of this broader pattern.

**Implication:** v2.2 training data must include substantially more
BET-labeled examples in the 0.40-0.70 equity range for 3-way
check-to-hero spots. The facing-bet test set (task #4) is the
measurement axis; the BET factory batch (batch 4, ~80-100 situations
designed in `review/BOARD_ALLOCATION_V4_BET.md`) is the training
data source.

### 2. Facing-bet gap is structural

Zero facing-bet 3-way situations generated naturally across 12,000
deals (6 seeds × 2000). This is game behavior (all-oracle lineup
mostly checks → nobody faces a bet). The facing-bet test set cannot
come from self-play — it must be factory-generated or hand-designed.

**Implication:** task #4 must use SituationFactory + GTO Expert
agents, not self-play. B-2 (multiway-biased sampling) would not fix
this either — even biased sampling can't produce facing-bet
situations if the oracle never bets.

### 3. Feature surface is aspirational, not loaded

gto_model.FEATURE_COLUMNS has 53 features but train_model.py has 48.
The v9-3way-v2.1 production model was trained on 45 features.
gto_model's `n_features_in_` auto-detection slices to the model's
actual width, so inference works — but features 49-53 are computed
and discarded at inference time.

**Implication:** v2.2 retrain needs a decision: train on 48 (current
training pipeline) or expand train_model.py to 53 first? If 53,
extract_incremental.py also needs updating, and all training CSVs
need regeneration.

### 4. Preflop range fix has downstream effects

Wider ranges change:
- Range composition features (TP+, draw%, air%) for all positions
- hero_range_percentile (wider range = different percentile for same hand)
- Board favour scores (wider ranges interact differently with boards)

These shifts were already observed in test recalibration (broadway
TP+ dropped from 0.15+ to 0.14+, HU opener_pos delta widened). The
v2.1 model was trained on old-range features; v2.2 training data
regenerated with new ranges will produce a different feature
distribution. This is expected and correct — but means v2.2 is NOT
a small delta retrain on top of v2.1. It's a fresh training cycle
with a different feature surface.

---

## Task list

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | Investigate BLUEPRINT_FEATURES_V3.1 | COMPLETED | Features were implemented in working tree, committed in Phase 0 |
| 2 | Fix B4_03 action history | COMPLETED | Canonical fix was already in place; committed in Phase 0 |
| 3 | Clean up DRIFTED review/ files | COMPLETED | Moot — original drift analysis was wrong |
| 4 | **Build facing-bet test set (30-50 hands)** | **PENDING — NEXT** | Unblocked by prep steps. Confirmed necessary by yield diagnostic. |
| 5 | Phase B Preflop Range Fix | COMPLETED | 3 commits, yield 4.9-7.0%, 960/0 tests |
| 6 | Train v9-3way-v2.2 | PENDING | Gated on task #4 (need second eval axis before retrain) |
| 7 | Resolve uncommitted git state | COMPLETED | 18 commits in Phase 0 |
| 8 | Phase B-2 multiway-biased sampling | DOWNGRADED | Not blocking v2.2 or v3; future iteration only |

---

## Open items NOT yet tracked as tasks

These surfaced during session work and may need their own tasks:

1. **Feature surface decision for v2.2:** train on 48 or expand to 53?
   Blocks train_model.py update + CSV regeneration. Owner decision
   needed before task #6 decomposition.

2. **BET factory batch 4 labelling:** ~80-100 BET/CHECK situations
   designed in `review/BOARD_ALLOCATION_V4_BET.md`. Ready for GTO
   Expert labelling but no task filed. Will feed into v2.2 training
   as additional BET-labeled data to counter passive bias.

3. **C-bet research + Feature 53 plan:**
   `review/comms/CBET_RESEARCH_AND_FEATURE53_PLAN_2026-04-09.md`
   is still ACTIVE. Phase A (feature 53) is committed but Phase B-D
   (c-bet research → BET tree → calibration) are queued. Related to
   #2 above.

4. **Paranoia test for duplicate RangeManager methods:** Per reviewer
   Q4 decision — bundle with task #4's first commit.

5. **draw_check Rule 4 on river:** oracle probe found the adjuster
   applying draw_check on a river hand with 4 "draw outs" — draw
   outs are meaningless on the river. Feature extraction artifact.
   Low priority but a real data quality smell.

---

## Recommended next action

**Task #4 — Build facing-bet test set (30-50 hands).**

Decomposition per reviewer's approved plan:
1. ml-architect: facing-bet axis specs (board textures × hero
   positions × facing-bet sizings to cover)
2. SituationFactory: generate board candidates against those specs
3. 3-5 GTO Expert agents (parallel, ≤10 hands each): design hero
   hands and label actions
4. Independent reviewer: audit full 30-50 before they become test set
5. Solver verification: mandatory on RAISE/CALL and high-equity FOLD

**Awaiting "go" for task #4.**

---

## Git log (session, 24 commits)

```
ef084a1 generate_3way_situations: filter illegal FOLD-without-bet predictions
c4f2f39 Phase B paperwork: design, blueprint, B-2 task spec, yield sample
aed81a6 Phase B tests: recalibrate thresholds for wider post-Phase-B ranges
1f9f739 Phase B: solver-backed preflop ranges with mixed frequencies
6cbde41 training-data: v2.1 training CSVs, 3way situations, factory batches
0f8cf91 solver screens/: GTO Wizard screenshot archive
ba932c4 review/comms/: 94 inter-terminal memos from v9-3way cycle
6589a12 review/: calibration + batch labelling artifacts
6175aa7 review/: staging copies of core Python modules and diff snapshots
3cbcaf1 review/: 83 spec, plan, blueprint, design, research, review documents
6f1d05b Add variant evolution, self-play, 3-way labelling infrastructure
a2d7b26 Add check_leakage.py top-level runner and results/SELF_PLAY_FINDINGS
150acea research: 12 deep-research documents for 3-way and preflop strategy
1127506 docs: master plan, progressive chain, 3-way labelling protocol
79d749e Reference set: apply MW-30 solver correction and axis reframing
80b57a5 tests: fix hardcoded sys.path and update sizing_oracle to 48-feature
b8c3c1e coaching: expand coaching pipeline oracle to 48-feature surface
0e0c91a Game engine: headless mode, per-player oracles, parameterized adjuster
7d1a2e0 sizing_oracle: expand FEATURE_COLUMNS to 48-feature contract
a07bbd9 Training pipeline: 48-feature contract, tuned hyperparams, MW-42 fix
1673c2c Add features 49-53: range percentile, showdown, fold equity, flush rank
55d6e3b Knowledge base v1.3: purge capped/uncapped, reframe on composition triple
+ 2 comms commits (prep memo + reviewer report)
```
