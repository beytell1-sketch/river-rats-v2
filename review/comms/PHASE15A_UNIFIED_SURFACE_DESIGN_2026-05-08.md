---
date: 2026-05-08
from: LEAD-PROGRAMMER (architect-hat)
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 1.5-A — unified-59-surface workstream design memo (architect-hat; design only, no execution)
status: DESIGN — single committed path; awaits QC + owner-merge gate
master_head_at_ground: e66e2e6
master_head_at_author: 5863f13
---

# Phase 1.5-A — unified-59-surface design

## 0. Charter and scope

Per dispatch `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306), this memo specifies the unified-59-surface workstream as a single committed path covering five design areas: (1) the 59-feature canonical surface, (2) the 988-corpus drop-2-J-B-features migration, (3) 3-way verification at the new surface, (4) the HU re-train cascade, and (5) cost/time forecast for sub-phases 1.5-B/C/D/E.

This is DESIGN ONLY. No source / data / model / prompt edits. Two PR files: this memo + the matching builder report.

Sequencing pre-commitment from PR #302 binds: HU first → 3-way verification → router/coaching alignment. Where the dispatch left a choice (e.g., warm-start vs from-scratch), this memo commits to ONE option with reasoning per `feedback_quality_default_no_ask.md`. Genuine owner-scope trade-offs are flagged explicitly.

Methodology compliance: pilot-first binding gates per `feedback_pilot_first_for_long_jobs.md`; no deadlines per `feedback_no_deadlines.md`; failure-direction classification per `feedback_failure_direction_classification.md`; solver-aligned bet sizes per `feedback_solver_aligned_sizing.md`; terminology per `feedback_terminology_raise_vs_bet.md`; bucket-first labelling per `feedback_bucket_first_labelling.md`; solver-vs-labels separation per `feedback_solver_vs_expert_labels.md`; postflop composition per `feedback_preflop_geometry_vs_postflop_composition.md`; close-hand selection per `feedback_close_hand_selection.md`; attention/prompt/capture/trainer lock-step per `feedback_attention_flags_when_features_change.md`.

---

## 1. 59-surface canonical

### 1.1 Definition

The 59-surface = `river-rats-core/feature_extractor.py:1569-1620` `FEATURE_COLUMNS` MINUS the 2 Step-18 (12.5J-B) entries at lines 1618-1619. The 59 features below are listed in canonical column order (this is also the order downstream column-drop and re-extract verification will compare against).

| idx | name | extractor step (file:line) | axis-of-targeting | chosen-seed importance (988-corpus, PR #293) |
|---|---|---|---|---|
| 1 | `street` | feature_extractor.py:1571 (Step 1) | shared | 0.0043 |
| 2 | `facing_bet` | feature_extractor.py:1571 | shared | 0.0541 |
| 3 | `pot_size` | feature_extractor.py:1571 | shared | (top 30; not enumerated in PR #293 §C) |
| 4 | `to_call` | feature_extractor.py:1571 | shared | 0.0314 |
| 5 | `pot_odds` | feature_extractor.py:1571 | shared | (top 30; not enumerated) |
| 6 | `bet_to_pot` | feature_extractor.py:1571 | shared | (top 30; not enumerated) |
| 7 | `hero_position` | feature_extractor.py:1572 | shared | (top 30; not enumerated) |
| 8 | `villain_position` | feature_extractor.py:1572 | shared | 0.0462 |
| 9 | `is_ip` | feature_extractor.py:1572 | shared | (top 30; not enumerated) |
| 10 | `hand_category` | feature_extractor.py:1574 (Step 2) | shared | (top 30; not enumerated) |
| 11 | `hand_rank` | feature_extractor.py:1574 | shared | (top 30; not enumerated) |
| 12 | `is_made_hand` | feature_extractor.py:1574 | shared | (top 30; not enumerated) |
| 13 | `is_strong_made` | feature_extractor.py:1574 | shared | (top 30; not enumerated) |
| 14 | `is_monster` | feature_extractor.py:1575 | shared | 0.0561 |
| 15 | `has_flush_draw` | feature_extractor.py:1575 | shared | 0.0038 |
| 16 | `has_straight_draw` | feature_extractor.py:1575 | shared | (top 30; not enumerated) |
| 17 | `draw_outs` | feature_extractor.py:1575 | shared | 0.0220 |
| 18 | `is_monotone` | feature_extractor.py:1577 (Step 3) | shared | 0.0000 |
| 19 | `is_two_tone` | feature_extractor.py:1577 | shared | 0.0000 |
| 20 | `is_rainbow` | feature_extractor.py:1577 | shared | 0.0078 |
| 21 | `is_paired` | feature_extractor.py:1577 | shared | (top 30; not enumerated) |
| 22 | `is_double_paired` | feature_extractor.py:1578 | shared | 0.0000 |
| 23 | `connectivity_score` | feature_extractor.py:1578 | shared | 0.0053 |
| 24 | `high_card_rank` | feature_extractor.py:1578 | shared | 0.0049 |
| 25 | `danger_score` | feature_extractor.py:1579 | shared | (top 30; not enumerated) |
| 26 | `flush_danger` | feature_extractor.py:1579 | shared | 0.0061 |
| 27 | `straight_danger` | feature_extractor.py:1579 | shared | 0.0035 |
| 28 | `raw_equity` | feature_extractor.py:1581 (Step 4) | shared | 0.0382 |
| 29 | `equity_vs_range` | feature_extractor.py:1581 | shared | 0.0352 |
| 30 | `better_hand_pct` | feature_extractor.py:1583 (Step 5) | shared | 0.0248 |
| 31 | `worse_hand_pct` | feature_extractor.py:1583 | shared | (top 30; not enumerated) |
| 32 | `equity_margin` | feature_extractor.py:1585 (Step 6) | shared | 0.0414 |
| 33 | `spr` | feature_extractor.py:1585 | shared | (top 30; not enumerated) |
| 34 | `is_3bet_pot` | feature_extractor.py:1587 (Step 7) | shared | 0.0000 |
| 35 | `villain_aggression_count` | feature_extractor.py:1587 | shared | (top 30; not enumerated) |
| 36 | `villain_checked_back` | feature_extractor.py:1588 | shared | (top 30; not enumerated) |
| 37 | `villain_call_count` | feature_extractor.py:1588 | shared | 0.0026 |
| 38 | `num_opponents` | feature_extractor.py:1590 (Step 8) | 3-way / 4-way / 5-way (HU=1 const) | 0.0205 |
| 39 | `villain_top_pair_plus_pct` | feature_extractor.py:1592 (Step 10) | shared | (top 30; not enumerated) |
| 40 | `villain_draw_pct` | feature_extractor.py:1592 | shared | 0.0206 |
| 41 | `villain_air_pct` | feature_extractor.py:1592 | shared | (top 30; not enumerated) |
| 42 | `villain_range_capped` | feature_extractor.py:1593 | shared | 0.0070 |
| 43 | `board_favour` | feature_extractor.py:1593 | shared | (top 30; not enumerated) |
| 44 | `num_callers_to_bet` | feature_extractor.py:1595 (Step 11) | 3-way / 4-way / 5-way (HU=0 const) | 0.0031 |
| 45 | `facing_raise` | feature_extractor.py:1595 | shared | 0.0000 |
| 46 | `flush_block_pct` | feature_extractor.py:1597 (Step 12) | shared | 0.0504 |
| 47 | `overcard_outs` | feature_extractor.py:1597 | shared | 0.0085 |
| 48 | `improvement_probability` | feature_extractor.py:1597 | shared | 0.0297 |
| 49 | `hero_range_percentile` | feature_extractor.py:1599 (Step 13) | shared | (top 30; not enumerated) |
| 50 | `has_showdown_value` | feature_extractor.py:1599 | shared | 0.0000 |
| 51 | `villain_fold_equity_estimate` | feature_extractor.py:1600 | shared | 0.0065 |
| 52 | `flush_draw_rank` | feature_extractor.py:1600 | shared | 0.0028 |
| 53 | `is_preflop_aggressor` | feature_extractor.py:1602 (Step 14) | shared | (top 30; not enumerated) |
| 54 | `villain_medium_made_pct` | feature_extractor.py:1604 (Step 15) | shared | (top 30; not enumerated) |
| 55 | `board_adjusted_hrp` | feature_extractor.py:1606 (Step 16) | shared | 0.0100 |
| 56 | `nut_flush_block` | feature_extractor.py:1609 (Step 17 v2.4 P1) | shared | 0.0527 |
| 57 | `flush_draw_block_pct` | feature_extractor.py:1610 | shared | 0.0499 |
| 58 | `straight_draw_block_pct` | feature_extractor.py:1611 | shared | 0.0062 |
| 59 | `nut_made_block_pct` | feature_extractor.py:1612 | shared | 0.0140 |

**Dropped (Step 18 / 12.5J-B):**

- `nut_blocker_overcard_count` — `feature_extractor.py:1618` defined; `feature_extractor.py:2136-2171` computed; `feature_keys.py:100`. Chosen-seed importance 0.0091 (PR #293 §C drop list). Targets MW-17 axis (nut-blocker × overcard composite).
- `bet_call_multiway_oop_raise_pressure_index` — `feature_extractor.py:1619` defined; `feature_extractor.py:2174-…` computed; `feature_keys.py:101`. Chosen-seed importance 0.0076 (PR #293 §C drop list). Targets MW-47 axis (multiway OOP raise-pressure composite).

Both are below the 1% Gate 2.3 drop threshold (`docs/PROCESS_GUIDE.md:112-116`); both targeted stay-wrong axes that remained on the stay-wrong list at 12.5K close. The structural-args case for keeping them lapsed when 12.5K-C-E cleared the corpus expansion (3-lever ceiling) without reactivating their importance.

### 1.2 TC-23 EXISTENCE attestation (architect verifies before PR)

Architect verified at master HEAD `e66e2e6` (immediately prior to PR #306 dispatch landing at `5863f13`):

- `river-rats-core/feature_extractor.py` — exists; `FEATURE_COLUMNS` at line 1569 has 61 entries; both J-B features at indices 60-61 (lines 1618-1619).
- `river-rats-core/feature_keys.py` — exists; `F.NUT_BLOCKER_OVERCARD_COUNT` line 100; `F.BET_CALL_MULTIWAY_OOP_RAISE_PRESSURE_INDEX` line 101.
- `river-rats-core/train_model_v9_student.py` — exists; line 97 hard-asserts `len(STUDENT_FEATURE_COLUMNS_V9) == 61`; line 119 hard-asserts `_S18_NEW_FEATURES` at tail; line 127 sets `_N_FEATURES_STUDENT = 61`.
- `river-rats-core/gto_model.py` — exists; production routing FEATURE_COLUMNS (line 33) is 55 features (`N_FEATURES = 55` at line 64); auto-detects width 38/45 at line 104.
- `river-rats-core/coaching/gto_model.py` — exists; line 33 mirrors production at 55 features.
- `river-rats-core/oracle_router.py` — exists; HU slot at line 34 references `gto_model_v8_hu.json`; legacy fallback at line 41 references `gto_model_v8_38feat.json`.
- `river-rats-core/models/gto_model_v8_hu.json` — exists.
- `river-rats-core/models/gto_model_v8_38feat.json` — exists (legacy).
- `river-rats-core/models/gto_model_v9_3way_v2.2.json` — exists (Phase 1 INTERIM lock).
- `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` — exists (12.5K-C-E chosen-seed promotion).
- `data/corpus_combined_988_2026-05-07.jsonl` — exists; 988 rows; `feat_dict` length 61 (verified by inspection of row 1).
- `data/corpus_combined_988_labels_2026-05-07.jsonl` — exists; 988 labels.
- `scripts/assemble_125k_c_e_988.py` — exists; canonical 988-corpus assembly script.
- `docs/PROCESS_GUIDE.md` — exists; §1.1 line 36-44 (agent batch sizes); §1.2 line 45-52 (minimum agent counts); §1.4 line 59-77 (experts recommend, owner decides scope); §2.1 line 94-102 (BLIND calibration).
- `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` — exists (the 40-hand multiway reference set design pattern).
- `prompts/gto_labeller_v3.4.md` — exists.
- `training-data/tag_vocabulary.json` — exists.
- `river-rats-core/calibration_exam.py` — exists.
- `river-rats-core/coaching/spot_classifier.py` — exists.

**Path corrections vs dispatch wording (per `feedback_verify_source_not_plan.md`):**

The dispatch §1 mentions `assemble_v23.py` and `extract_features_parallel.py`; the dispatch §2 mentions `train_v2_3_clean.py` and `check_leakage.py`. Verified locations at master `5863f13`:

- `extract_features_parallel.py` is canonical at `river-rats-core/extract_features_parallel.py` (✓ in core).
- `assemble_v23.py`, `train_v2_3_clean.py`, `check_leakage.py` exist at REPO ROOT (not in `river-rats-core/`). They are legacy v2.3 pipeline files that pre-date the river-rats-core/ discipline addendum (CLAUDE.md §6 training provenance). The 988-corpus is NOT assembled by them — current canonical is `scripts/assemble_125k_c_e_988.py` (which itself ingests prior 788-corpus assembly artifacts, lineage `scripts/assemble_125i_d_788.py`).

Going forward, this memo cites the actual canonical paths (`scripts/assemble_*` for corpus assembly; `river-rats-core/extract_features_parallel.py` for feature extraction; `river-rats-core/train_model_v9_student.py` for the v9 student trainer).

### 1.3 Lock-step touch-points for the 59 → execution sub-phases

Per `feedback_attention_flags_when_features_change.md`, every feature-surface change must move the matching attention vocabulary, prompt rules, capture, and trainer in lock-step or new features ship with raw values + zero attention signal.

**1.3.1 Touch-point inventory (J-B references at master HEAD; all must update in 1.5-B):**

`grep -rln 'nut_blocker_overcard_count\|bet_call_multiway_oop_raise_pressure_index' training-data/ prompts/ river-rats-core/ scripts/` returns (verified at `e66e2e6`):

- `river-rats-core/train_model_v9_student.py` (lines 94-122 module-load asserts; line 127 _N_FEATURES_STUDENT)
- `river-rats-core/feature_extractor.py` (lines 100-101 keys; 1618-1619 columns; 2136-2171 + 2174-… compute fns; 2648 + 2653-2663 call sites)
- `river-rats-core/feature_keys.py` (lines 94-101)
- `river-rats-core/tests/test_features_125j.py` (J-B feature unit tests)
- `river-rats-core/tests/test_train_model_v9_student.py` (trainer surface assert)
- `scripts/generate_lever_c_situations.py` (12.5K Lever C situation generator)
- `scripts/build_corpus_revision_125i_mw40_verif_situations.py` (12.5I MW-40 verification)
- `scripts/assemble_125i_d_788.py` (788 corpus assembly lineage)

**1.3.2 Attention layer status: J-B was NEVER integrated into attention.**

Verification: `grep -rln 'nut_blocker_overcard_count\|bet_call_multiway_oop_raise_pressure_index' training-data/tag_vocabulary.json prompts/gto_labeller_v3.*.md` returns ZERO matches. The attention vocabulary at `training-data/tag_vocabulary.json` and the v3.x labelling prompts (`prompts/gto_labeller_v3.1.md` … `prompts/gto_labeller_v3.4.md`) never gained PRIMARY/CONFIRMED tag rules for the 2 J-B features.

**Implication:** Dropping the 2 J-B features requires NO attention-vocab / prompt-rule deletion (nothing to delete). Per `feedback_attention_flags_when_features_change.md` retroactively, the 12.5J-B implementation already shipped with raw values + zero attention signal — which is part of why their importance never crossed 1%. This is consistent with the dispatch's diagnosis (sub-1% importance, MW-17/47 stay-wrong unresolved) and supports the "structural-args case lapsed" framing of §1.1.

**1.3.3 Touch-points the 59 → 59-attention-aligned execution sub-phases MUST update:**

Going forward (Phase 1.5-B feature-prune mechanical sub-phase + downstream surface-aware sub-phases), the in-scope updates are:

- **Trainer hard-asserts.** `river-rats-core/train_model_v9_student.py:97` (61 → 59); `:115` (`_V24_P1_BLOCKERS` at indices `-5:-1` post-drop, was `-6:-2` pre-drop) — note this is one of the few places where an off-by-N exists in the assertion structure; architect commits to: "assert v2.4 P1 blockers occupy positions 56-59 of the 59-feature list (indices `-4:` of the 59-list)" with rationale that the J-B drop frees the tail. `:127` (`_N_FEATURES_STUDENT = 59`); module docstring at line 1.
- **Feature definitions.** `river-rats-core/feature_extractor.py:1613-1619` (delete Step 18 block); `:2136-2171` and `:2174-…` (delete compute functions); `:2645-2663` (delete the two call-site assignments); `feature_keys.py:94-101` (delete `F.NUT_BLOCKER_OVERCARD_COUNT` + `F.BET_CALL_MULTIWAY_OOP_RAISE_PRESSURE_INDEX`).
- **Tests.** `river-rats-core/tests/test_features_125j.py` (delete entire file; J-B tests are the sole purpose); `river-rats-core/tests/test_train_model_v9_student.py` (update surface-size assertions 61 → 59; revise tail-position assertions per the off-by-N note above).
- **Scripts.** `scripts/generate_lever_c_situations.py`, `scripts/build_corpus_revision_125i_mw40_verif_situations.py`, `scripts/assemble_125i_d_788.py` — delete J-B references; these are historical pipeline scripts; for the latter two (frozen artifacts) the appropriate pattern is to add a docstring note that the script targets a frozen 61-surface and is no longer re-runnable on the 59-surface, rather than mutate it. Architect commits to: scripts/lever_c (active in lever-c lineage) gets the J-B deletion; the two historical scripts get a docstring freeze-note. (This is a quality choice over a menu, per `feedback_quality_default_no_ask.md`: deleting from frozen scripts that produced shipped artifacts violates training provenance per CLAUDE.md §6.)
- **Production routing.** `river-rats-core/gto_model.py:33-64` and `river-rats-core/coaching/gto_model.py:33-64` (production FEATURE_COLUMNS at 55) — DESIGN POSITION: these stay at 55 throughout 1.5-B feature-prune; the 55→59 unification is part of the HU re-train cascade (1.5-D) and the coaching-alignment sub-phase (1.5-E), NOT 1.5-B. Reason: production routing changes require trained 59-feature HU and 3-way models in hand to load; sequencing it earlier creates a router with no model to dispatch to. This is consistent with PR #302's HU-first ordering.
- **988-corpus.** `data/corpus_combined_988_2026-05-07.jsonl` + `data/corpus_combined_988_labels_2026-05-07.jsonl` are a frozen artifact. Migration creates a new artifact `data/corpus_combined_988_on_59_2026-05-XX.jsonl` (re-extract; see §2.4); the 61-surface corpus is retained for provenance.
- **Attention vocab + prompts.** No deletions needed (J-B never landed). Going-forward principle: any future feature ADDITION to the 59-surface MUST land attention-vocab + prompt-rule updates in lock-step in the same PR per `feedback_attention_flags_when_features_change.md`.

---

## 2. Drop-2-J-B-features migration (988-corpus → 59-surface)

### 2.1 Migration philosophy: re-extract, not column-drop (single committed path)

Per dispatch §2 quality discipline ("Single committed path: re-extract from raw situations (NOT column-drop), per `feedback_solver_findings.md` quality discipline"), the 988-corpus 59-surface artifact is produced by re-running `extract_all_features` on the raw 988-situation set after deleting the Step 18 compute block from `feature_extractor.py`.

**Reasoning for choosing re-extract over column-drop:**

The 988-corpus J-B features (`feature_extractor.py:2645-2663`) are computed AT THE END of `extract_all_features` and read only existing feature values (no downstream feature depends on them). Therefore (re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor) — modulo identical RNG seeds in equity computation, which `extract_features_parallel.py` controls. So column-drop would produce a numerically identical corpus.

Despite this, the architect commits to re-extract because:

1. **Future-proofing.** If a future feature change is NOT append-only-end-of-pipeline (e.g., reorders Steps 15-17 for cache locality, or modifies a shared computation read by Step 18), column-drop equivalence breaks silently. Establishing re-extract as the migration pattern now means we never have to audit "is this drop append-only-pure" again.
2. **Quality discipline.** Per `feedback_solver_findings.md`, we have a track record of subtle bugs from "obvious" shortcuts (the 12.5K labelling hash drift was one such). A re-extract is a fresh end-to-end run; any drift between the J-B-removed extractor and prior runs surfaces immediately.
3. **Provenance clarity.** The 988-on-59 artifact's checksum derives from the 59-surface extractor, not from a derived-by-drop pipeline. Future users querying "what produced this corpus?" get a single trainer-extractor pair, not a two-step (extract+drop) lineage.

The bit-equality verification of §2.4 is an additional safeguard, not a substitute.

### 2.2 Re-extraction protocol (architect's committed sequence for Phase 1.5-B)

Phase 1.5-B (feature-prune mechanical) executes in this order:

**Step 1 — Source mutation (single PR, single commit):**

- Delete `feature_extractor.py:1613-1619` (Step 18 column block).
- Delete `feature_extractor.py:2136-2171` (`compute_nut_blocker_overcard_count`).
- Delete `feature_extractor.py:2174-…` through end of `compute_bet_call_multiway_oop_raise_pressure_index` body (architect-hat in 1.5-B identifies the exact closing line; precommitment: function body ends at the return statement following the body in the file as it exists at master `e66e2e6`).
- Delete `feature_extractor.py:2645-2663` (the two call-site assignments inside `extract_all_features`).
- Delete `feature_keys.py:94-101` block (the comment + 2 keys; trim the surrounding blank lines).
- Update `train_model_v9_student.py:97-122` (assert 59 + tail-position assertions per §1.3.3).
- Update `train_model_v9_student.py:127` (_N_FEATURES_STUDENT = 59).
- Update `train_model_v9_student.py:1-30` docstring "61" → "59".
- Delete `tests/test_features_125j.py`.
- Update `tests/test_train_model_v9_student.py` surface-size assertions 61 → 59 (architect identifies exact lines in 1.5-B).
- Update active scripts (`scripts/generate_lever_c_situations.py`); freeze-note historical scripts (`scripts/build_corpus_revision_125i_mw40_verif_situations.py`, `scripts/assemble_125i_d_788.py`).

**Step 2 — Extractor self-test:**

- Run `python -m pytest river-rats-core/tests/` — must pass with 59-surface assertions; existing tests not touched by §1.3.3 must remain green.
- Run an extractor-only smoke test: a single hand from `data/corpus_combined_988_2026-05-07.jsonl`, run through the modified `extract_all_features`, verify output dict has exactly 59 keys matching `FEATURE_COLUMNS` (post-drop) and that the 59 values bit-equal the 988-corpus's `feat_dict[k]` for all `k ∈ 59-keys` (`!=` check on any differs).

**Step 3 — Re-extract 988 → 59 surface:**

- Inputs: the 988 raw situations from the 988-corpus's `prior_actions` / `board` / `hero_cards` / etc. fields (the same input format `extract_all_features` expects).
- Output: `data/corpus_combined_988_on_59_2026-05-XX.jsonl` (date matches 1.5-B PR open date), preserving all non-feature row keys (`deal_id`, `pilot_hand_id`, `board`, `hero_cards`, `hero_position`, `num_opponents`, `pot`, `prior_actions`, `facing_bet`) and replacing `feat_dict` with the new 59-key dict.

**Step 4 — Labels:** `data/corpus_combined_988_labels_2026-05-07.jsonl` is FEATURE-FREE (it stores `action` + confidence + meta only). Per inspection of corpus structure, the labels file has no feat_dict refs that need updating. Architect commits: labels file is COPIED verbatim to a new dated path (`data/corpus_combined_988_on_59_labels_2026-05-XX.jsonl`) for provenance pairing — content identical. (If 1.5-B discovers an embedded feat_dict in labels per row, that's a STOP condition per CLAUDE.md §5; report and re-decompose.)

### 2.3 Determinism guarantee + verification command

Architect commits to the following bit-equality verification, to be run BEFORE 1.5-B PR merge as part of the migration's CI gate:

```bash
# Reference: 61-surface corpus, column-dropped
python3 -c "
import json
keep = [
  'street','facing_bet','pot_size','to_call','pot_odds','bet_to_pot',
  'hero_position','villain_position','is_ip',
  'hand_category','hand_rank','is_made_hand','is_strong_made','is_monster',
  'has_flush_draw','has_straight_draw','draw_outs',
  'is_monotone','is_two_tone','is_rainbow','is_paired','is_double_paired',
  'connectivity_score','high_card_rank','danger_score','flush_danger',
  'straight_danger',
  'raw_equity','equity_vs_range','better_hand_pct','worse_hand_pct',
  'equity_margin','spr',
  'is_3bet_pot','villain_aggression_count','villain_checked_back',
  'villain_call_count','num_opponents',
  'villain_top_pair_plus_pct','villain_draw_pct','villain_air_pct',
  'villain_range_capped','board_favour',
  'num_callers_to_bet','facing_raise',
  'flush_block_pct','overcard_outs','improvement_probability',
  'hero_range_percentile','has_showdown_value',
  'villain_fold_equity_estimate','flush_draw_rank',
  'is_preflop_aggressor','villain_medium_made_pct','board_adjusted_hrp',
  'nut_flush_block','flush_draw_block_pct','straight_draw_block_pct',
  'nut_made_block_pct',
]
import sys
src = 'data/corpus_combined_988_2026-05-07.jsonl'
with open(src) as f:
  for line in f:
    row = json.loads(line)
    fd = row['feat_dict']
    pruned = {k: fd[k] for k in keep}
    print(json.dumps({**row, 'feat_dict': pruned}, sort_keys=True))
" > /tmp/corpus_988_on_59_via_drop.jsonl

# Re-extract path: produced by 1.5-B's modified extractor
# (after Step 1+2+3 of §2.2 above)
sort /tmp/corpus_988_on_59_via_drop.jsonl > /tmp/drop_sorted.jsonl
sort data/corpus_combined_988_on_59_2026-05-XX.jsonl > /tmp/reext_sorted.jsonl

# Bit-equality check
diff /tmp/drop_sorted.jsonl /tmp/reext_sorted.jsonl
# Must produce EMPTY diff. Any non-empty diff = STOP CONDITION per CLAUDE.md §5.
```

**Why this is the right verification:** The drop-side (left) is produced by reading the existing 988-corpus's feat_dicts and projecting to the 59-key set; the re-extract-side (right) is produced by running the modified extractor on raw situations. If they bit-match, we have proof that:

(a) the modified extractor produces the same Steps 1-17 outputs that the unmodified extractor produced (no inadvertent regression);
(b) the 59-surface corpus is faithful to the 988 lineage; and
(c) Step 18 truly was append-only-end-of-pipeline (validating §2.1's claim).

If the diff is non-empty, the migration BLOCKS at this gate. The architect-hat in 1.5-B writes a diagnostic comm explaining the drift and requests scope-expansion authorization from the orchestrator before proceeding.

### 2.4 Output artifact spec (committed)

- **Path:** `data/corpus_combined_988_on_59_2026-05-XX.jsonl` (XX = 1.5-B PR open day).
- **Size:** 988 rows. Each row's `feat_dict` has exactly 59 keys.
- **Keys:** the 59 listed in §1.1 (verifiable via `for k in keep: assert k in row['feat_dict']` and `assert len(row['feat_dict']) == 59`).
- **Other fields:** verbatim from 988-corpus (`deal_id`, `pilot_hand_id`, `board`, `hero_cards`, `hero_position`, `num_opponents`, `pot`, `prior_actions`, `facing_bet`).
- **Checksum:** SHA-256 logged in 1.5-B builder report; will be referenced in 1.5-C 3-way verification training metadata.
- **Labels:** `data/corpus_combined_988_on_59_labels_2026-05-XX.jsonl` (verbatim copy; content-identical SHA-256 to original labels file; date suffix only differs).

### 2.5 Invariant tests re-baseline

Per dispatch §2, "which tests in `check_leakage.py` + `train_v2_3_clean.py` need surface-size update". Architect inventory at master `e66e2e6`:

- `check_leakage.py` (REPO ROOT, legacy v2.3): `grep -n "FEATURE_COLUMNS\|45\|55\|61" check_leakage.py` — leakage check is feature-space nearest-neighbor on the 38-feat surface (legacy v2.3 era). It does NOT need a 59-surface bump for the 1.5-A/B workstream — its current consumers are the 38/45 baselines and it's not in the v9-student trainer's import graph. Architect commits: leave `check_leakage.py` untouched in 1.5-B; if a future leakage check on 59-surface is needed (1.5-C/D), commission a new `tools/check_leakage_v9_59.py` rather than mutating the legacy file (training-provenance discipline).
- `train_v2_3_clean.py` (REPO ROOT, legacy v2.3 trainer): same status — frozen v2.3 trainer; not in v9-student's import graph. Leave untouched.
- `tests/test_train_model_v9_student.py` IS in scope (§1.3.3 covers it).
- `tests/test_features_125j.py` IS in scope (deleted in 1.5-B).

This is a TC-23 EXISTENCE + scope-discipline move: dispatch's mention of `check_leakage.py` and `train_v2_3_clean.py` is acknowledged; architect's reading of master HEAD says they are out-of-band for 1.5-B. If QC reads this differently, the architect will adjust before merge.

---

## 3. 3-way verification at 59-surface

### 3.1 Scope (Phase 1.5-C in the cost/time forecast)

Re-train the v9-3way student on the 988-on-59-surface corpus from §2 and verify that aggregate ceiling holds. Pre-commitment per dispatch: PASS gate is mean ≥ 33.00/40 across N seeds.

This is verification, not improvement. The hypothesis being tested is "removing the 2 sub-1% J-B features does not regress 3-way aggregate." If it does regress, that's load-bearing evidence the J-B importance was not a useful signal of feature value — and we adapt (§3.4 decision matrix).

### 3.2 N-seed commitment

**Architect commits: N = 5 seeds (seeds 0,1,2,3,4).**

Reasoning:

- Mirrors PR #293 12.5K-C-E precedent (5-seed re-train on the 988 corpus, NULL result 33.00 ± 0.00, established the 3-lever ceiling).
- The 12.5K-C-E ± 0.00 standard deviation indicates the 988-corpus produces extremely tight cross-seed agreement at this ceiling — 5 seeds give us low standard error on the mean while keeping cost manageable.
- Going higher (e.g., 10 seeds) doubles cost without informative gain at the current ± 0.00; going lower (3 seeds) loses parity with PR #293's reference for delta interpretation.

### 3.3 Warm-start strategy (single committed path)

**Architect commits: pre-pad warm-start from `models/gto_model_v9_3way_v2.2.json` (45-feat) bumped to 59 via the existing `prepad_baseline_booster` mechanism in `train_model_v9_student.py:409-437`.**

Reasoning vs the dispatch's posed alternatives ("from-scratch OR a specified projection scheme"):

- The pre-pad mechanism IS already a specified, implemented, tested projection scheme. It modifies the warm-start booster's `learner.learner_model_param.num_feature` JSON metadata only; the existing trees are append-only-valid because they only split on feature indices `[0, 45)` which remain valid in the expanded `[0, 59)` index space.
- Pre-pad has been used twice already in this lineage: 45 → 59 at 12.5G/H, and 45 → 61 at 12.5J-B (see `train_model_v9_student.py:95` "Pre-pad mechanism extended to bump 45 → 61"). Both runs trained successfully and the 12.5K-C-E ceiling was achieved on the 61-surface pre-padded warm-start.
- 1.5-C's 45 → 59 pre-pad is a STRICT SUBSET of the 12.5J-B 45 → 61 pre-pad (just one fewer index of expansion). The mechanism is identical; only the target_n_features arg differs.
- "From-scratch" loses the v9-3way-v2.2 lineage that established the Phase 1 INTERIM ceiling. Pre-pad preserves it.

**Hyperparameters (architect commits):** Inherit verbatim from `train_model_v9_student.py:139-154` `_HYPERPARAMETERS` (n_estimators=800, max_depth=5, learning_rate=0.05, early_stopping_rounds=50, subsample=0.8, colsample_bytree=0.75, min_child_weight=5, gamma=0.2, reg_alpha=0.1, reg_lambda=1.0, multi:softprob, num_class=5, eval_metric=mlogloss). No env-var overrides (`RR_HP_*` unset).

**Confidence weighting:** `pure` (matches 12.5K-C-E chosen-seed config).

**Class-weight cap:** 3.0 (matches 12.5K-C-E chosen-seed config).

**Warm-start canonicality:** `is_git_tracked('river-rats-core/models/gto_model_v9_3way_v2.2.json')` must return True at run time (per `train_model_v9_student.py:196-220`). At master `e66e2e6`, that file IS git-tracked.

### 3.4 PASS gate + failure-direction decision matrix

**PASS gate (committed per dispatch):**

- **PASS:** mean across 5 seeds ≥ 33.00/40 on the 40-hand reference set (`mw_11_50`). Median seed promoted to canonical at `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (filename committed).
- **STOP/REPORT (no auto-action):** mean ∈ [32.00, 33.00) — partial regression; surface to orchestrator + owner; do NOT auto-promote.
- **HALT/INVESTIGATE:** mean < 32.00 — material regression; halt 1.5 workstream; trigger root-cause investigation comm before any 1.5-D HU work fires.

**Failure-direction classification (per `feedback_failure_direction_classification.md`):**

The 1.5-C builder report MUST classify per-hand misses (where this run differs from solver-corrected expert per `memory/reference_corrections.md`) along three axes:

- **under-aggress:** student predicted CHECK or CALL where expert+solver predicted BET or RAISE. (Most common 12.5K mode at MW-40/45/47.)
- **over-aggress:** student predicted BET or RAISE where expert+solver predicted CHECK or CALL.
- **class-collapse:** student probability mass concentrated on a class with <5% expert support across the close-spot set; signals confidence calibration drift.

Report format (committed for 1.5-C and 1.5-D builder reports):

```
| hand | this-run | solver-corrected expert | direction |
|------|----------|------------------------|-----------|
| MW-17 | FOLD     | CALL                   | under-aggress |
| MW-40 | CHECK    | BET                    | under-aggress |
| ...   | ...      | ...                    | ...           |

Direction summary: U=N over X total miss; O=N; C=N. (X = total misses on 40-hand reference.)
```

A direction-skewed regression (e.g., 5+ new under-aggress misses) is a STOP/REPORT trigger even if the aggregate mean clears 33.00 — the dispatch's quality bar requires stay-wrong taxonomy fidelity, not just headline number.

### 3.5 Pilot+full split per `feedback_pilot_first_for_long_jobs.md`

**1.5-C is a single 5-seed run on a fixed 988-row corpus; it is not a "long batch" in the labelling/generation sense.** However, the STANDING RULE applies to training-data-producing batches; 1.5-C is a verification re-train, not a new training-data generation. The pilot-first analog here is the §2.3 bit-equality verification gate, which IS pilot-first for the data side of the migration.

For the training side: architect commits to a 1-seed smoke run BEFORE the 5-seed run, gating on "does the run complete without a crash + produce a model on disk + score within 5 points of the median 12.5K-C-E result on the 40-hand reference." If any of those fail, halt and report. ~10-min spend.

---

## 4. HU re-train cascade (v8-HU-38 → vNext-HU-59)

### 4.1 Scope and sequencing (Phase 1.5-D in the cost/time forecast)

Per PR #302 retrain-ordering pre-commitment, HU re-train follows 3-way verification (§3) but begins design/pilot work in parallel to keep the critical path short. HU re-train is the heaviest sub-phase: it requires a HU reference set design, HU labelling pipeline, HU corpus assembly, HU training, and ship-gate verification. We decompose into sub-sub-phases 1.5-D.1 through 1.5-D.5 in §4.7.

### 4.2 HU reference set design (1.5-D.1)

**Target size:** 30 HU postflop spots.

Reasoning vs dispatch's "~30-40":

- 30 keeps the labelling cost proportional to the ~3.5x easier-than-multiway difficulty profile of HU (no num_opponents axis; no multiway range collisions).
- 30 maps cleanly to 6 batches × 5 hands or 5 batches × 6 hands per `docs/PROCESS_GUIDE.md:36-44` agent-batch-size cap (≤ 10 hands per labelling agent).
- The 40-hand multiway reference set (MW-11..50) was sized for 8 axes × 5 hands (with batch 8 truncated). HU has fewer canonical axes — value vs draw vs air with position/SPR modulation — so 30 covers the natural axis count without padding.

**Axis design (architect commits to 6 axes):**

- **Axis HU-1 (made hand vs villain range):** 5 hands. Hero has top-pair-or-better; villain range capped vs uncapped. (Targets value-betting + protection vs slowplay decisions.)
- **Axis HU-2 (drawing hand profitability):** 5 hands. Hero has flush draw / straight draw / combo draw with various pot odds / SPR / position contexts. (Targets semi-bluff vs check-call discipline.)
- **Axis HU-3 (air with backdoors):** 5 hands. Hero has high-card-only or weak backdoor draws against capped villain ranges. (Targets float vs check-fold vs c-bet bluff decisions.)
- **Axis HU-4 (preflop aggressor postflop discipline):** 5 hands. Hero is preflop opener; testing c-bet sizing + frequency on dry vs wet boards.
- **Axis HU-5 (out-of-position decisions):** 5 hands. Hero is OOP vs IP villain; testing check-raise frequency, donk-bet usage, and lead-out lines.
- **Axis HU-6 (river decision precision):** 5 hands. Pure river spots — value-bet sizing, bluff-catch threshold, river overbet response.

**Hand selection per axis (committed methodology):**

- 3 of 5 hands per axis are CLOSE (per `feedback_close_hand_selection.md`: model uncertainty on v8-HU-38 + poker difficulty, NOT feature-stat extremes).
- 2 of 5 are CANONICAL (uncontroversial value or fold spots; serve as ground-truth anchors for inter-labeller agreement).
- Hand strength composition follows TP+/draws/air per `feedback_preflop_geometry_vs_postflop_composition.md` — NOT preflop range buckets.
- Solver-aligned bet sizes per `feedback_solver_aligned_sizing.md`: flop 25%/66%, turn 33%/75%, river 33%/75%/150%. Architect adopts these in spot specs; any deviation requires a rationale comm.
- Terminology compliance per `feedback_terminology_raise_vs_bet.md`: spot specs use "raise = raise of existing bet; bet = first postflop bet; open = preflop opener" verbatim. Architect spot-checks every spot specification before labelling fires.

**Design-agent dispatch (per `docs/PROCESS_GUIDE.md:45-52`):**

- 6 design agents (one per axis) — all parallel.
- 1 reviewer agent (independent; reads all 30 spec files; checks card conflicts, board overlaps, hand classification, axis-coverage).
- Output: `design/hu_reference_set/HU_30_HAND_DESIGNS.md` + per-axis breakouts mirroring the BATCH2 pattern at `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`.

**Pilot-first per `feedback_pilot_first_for_long_jobs.md`:**

- Pilot: design 1 axis (5 hands) end-to-end, run through the labelling pipeline, evaluate cost + quality.
- Gate: pilot must clear inter-labeller agreement ≥ 80% (4 of 5 labellers consensus on ≥ 4 of 5 hands) and a Sonnet→Opus tier-up cross-check on disagreements yields ≤ 1 changed action.
- If pilot fails, halt and report; do not dispatch the remaining 5 axes.

### 4.3 HU labelling pipeline (1.5-D.2)

**Labeller version:** `prompts/gto_labeller_v3.4.md` (or whichever is current at 1.5-D.2 fire time; architect commits to v3.4 for current dispatch).

**5-labeller consensus (per locked Stage 4 plan referenced in dispatch §"HU labelling protocol"):**

- 5 labellers per hand. Each labeller is a fresh agent with no shared state.
- BLIND calibration mandatory before each labeller participates (per `docs/PROCESS_GUIDE.md:94-102`): 20/24 minimum on the calibration exam + all 3 GTO-reversal hands correct. Agent must NOT have access to `river-rats-core/calibration_exam.py` or any answer key during the exam.
- Bucket-first per `feedback_bucket_first_labelling.md`: NO equity thresholds in the labelling prompt; thresholds live in `river-rats-core/coaching/spot_classifier.py` and are applied AFTER labelling.
- Solver-vs-labels separation per `feedback_solver_vs_expert_labels.md`: solver verifies disagreements and informs research; solver output is NEVER used as a training label.

**Consensus rule:**

- ≥ 4 of 5 labellers agree on action → consensus action; confidence = labeller-count / 5.
- 3-2 split → solver verification (single solver run on the spot); the solver answer becomes the research finding; consensus action remains the 3-of-5 majority labeller answer (or owner-arbitrated if research contradicts majority).
- 2-2-1 split or worse → owner-arbitrated; surface in 1.5-D.2 builder report.

**Tier-up rule per `feedback_pilot_first_for_long_jobs.md` sub-rule:**

- All training-data outputs require Sonnet → Opus cross-check on a SAMPLE.
- Sample = all hands where Sonnet 5-labeller consensus is below 5-of-5 (i.e., any non-unanimous hand).
- 1 Opus labeller runs on the sample; agreement with Sonnet majority is reported.
- Disagreement on > 10% of sampled hands triggers full Opus re-label of the disagreeing hands (~5-8 hands typically).

**Pilot+full split:**

- Pilot batch: 5 hands (the HU-1 pilot from 4.2).
- Full batch: 25 hands (axes HU-2..HU-6).
- Full batch fires only after pilot clears the gate in §4.2.

### 4.4 HU corpus assembly (1.5-D.3)

**Target corpus size:** ~600-900 HU labelled situations.

Reasoning:

- The 988-corpus 3-way produced 33.00/40 mean at the 988 size (PR #293). HU is structurally easier (no multiway range collision); equivalent ceiling is plausible at smaller corpus.
- Lower bound 600: matches 12.5K's 788-corpus precedent for a "first-pass v9 corpus" before scale-up.
- Upper bound 900: gives ~30x labelled hands per HU reference spot, comparable to the 988/40 = 24.7x density of multiway.
- Architect commits to 750 as the target: 30 reference-spot lookalikes × 25 = 750. Lookalike generation pattern follows `scripts/generate_lever_c_situations.py` precedent (axis-anchored situation generation; pool then filter by similarity).

**Generation pipeline:**

- Mirror the 12.5K Lever C → assembly pattern: HU situation generator (new file `scripts/generate_hu_situations.py`) draws from the 30 reference spots, varies (board run-out / position / SPR / villain action sequence) to produce a pool of ~3000 HU situations.
- Filter to ~750 via similarity-band selection: each reference spot anchors ~25 situations within a feature-space distance threshold (architect commits in 1.5-D.3 to the exact distance threshold based on close-hand-selection analysis on the v8-HU-38 model uncertainty surface).
- Label all 750 through the §4.3 pipeline.
- Assemble into `data/corpus_hu_750_2026-XX-XX.jsonl` + matching labels file.

**Pilot+full split (per STANDING RULE):**

- Pilot: 50 HU situations from the HU-1 pilot batch axis. Run through generation → labelling → consensus → solver verification on disagreements.
- Gate: 50-hand pilot produces ≥ 80% labeller-consensus rate AND solver-verified consensus matches majority on ≥ 90% of solver-checked spots.
- Full 700 fires only after pilot clears the gate.

### 4.5 HU model retrain (1.5-D.4)

**Warm-start strategy (architect commits): from-scratch.**

Reasoning vs dispatch's posed alternatives ("from v8-HU-38-feat OR from-scratch OR projection"):

- The v8-HU-38-feat model's 38-feature surface is a STRICT SUBSET of the 59-feature surface, so a pre-pad warm-start (analogous to the v9-3way 45→59 case in §3.3) is theoretically possible: bump `num_feature` from 38 to 59 in the JSON metadata, then warm-start training on 59-surface inputs.
- HOWEVER, two arguments push toward from-scratch for HU specifically:
  1. **Multi-class transition.** v8-HU-38 was trained as 3-class (FOLD/CHECK_CALL/BET_RAISE) per legacy `gto_model.py` constants; the 5-class expansion (FOLD/CHECK/CALL/BET/RAISE) happened at v9 per `gto_model.py:N_CLASSES = 5`. Pre-pad assumes class-count parity at warm-start; the class-count change requires model-output-layer re-init regardless. From-scratch is therefore unavoidable for the output layer.
  2. **Corpus origin difference.** v8-HU-38 trained on PokerBench-derived data (88.1% accuracy reference); the new HU corpus is a fresh expert-labelled 750 situations. The implicit prior in v8-HU-38 trees may be poorly aligned with the 5-class label distribution of the new corpus, and warm-starting from a poor prior delays convergence relative to from-scratch with the right corpus.
- Therefore architect commits to from-scratch HU retrain. v8-HU-38 stays as a lineage anchor (provenance only); vNext-HU-59 is a clean training run on the 750 HU corpus + 59-surface.

**Trainer:** Adapt `river-rats-core/train_model_v9_student.py` to a HU-specific variant `river-rats-core/train_model_vNext_hu.py`. Differences from the 3-way student:

- Surface size assertion 59 (not 61).
- No `num_opponents`-conditioned features need attention (HU has constant `num_opponents=1`); however, the 59-surface includes `num_opponents` as a feature and the model will learn it as a constant on HU corpus — that's fine; it does not need surgery.
- From-scratch (no `xgb_model=` warm-start arg).
- Hyperparameters identical to the 3-way student (justified: same model family; same regularization regime suitable for ~750-corpus 5-class XGBoost).
- 5-seed standard run.

**Per-hand stay-wrong tracking:** 1.5-D.4 builder report MUST include the §3.4 failure-direction format applied to the 30-hand HU reference set. Stay-wrong hands tracked across seeds (analog to `project_v9_3way_ceiling.md` taxonomy).

### 4.6 HU ship-gate (committed per `feedback_quality_default_no_ask.md`)

**Architect commits: ship gate = aggregate accuracy on the 30-hand HU reference set ≥ 28/30 (≥ 93.3%).**

Reasoning vs dispatch's posed alternatives ("PokerBench 88.1% baseline OR per-hand canonical match rate"):

- PokerBench 88.1% is a different evaluation (large held-out PokerBench split; not our 30-hand reference). Using it as the HU ship gate would be cross-evaluation comparison and is not load-bearing for our reference.
- Per-hand canonical match rate IS load-bearing because the 30-hand HU reference set is the analog of the 40-hand multiway reference. The 3-way Phase 1 INTERIM lock is at 33/40 = 82.5% canonical match rate (with corrections applied). HU is structurally easier; 28/30 = 93.3% is approximately one error per axis on average and gives reasonable headroom over a "canonical match parity with v8-HU-38 PokerBench 88.1%" threshold (which, when projected onto the 30-hand reference, would imply 26-27/30 canonical match — too lax).
- 28/30 chosen specifically: 30 - 2 = 28 lets one CLOSE hand miss per typical axis without tripping the gate, while 27/30 (-3) would allow a class-collapse pattern to slip through.
- This threshold is committed; if 1.5-D.4 produces 26 or 27 of 30, that's STOP/REPORT (not auto-promote).

**Fallback verification:** PokerBench 88.1% parity reported as a SECONDARY metric for provenance; not a gate.

**Ship action:** On gate clear, `models/gto_model_v8_hu.json` (38-feat) is REPLACED in production by `models/gto_model_vNext_hu_59feat.json` via `oracle_router.py:34` filename pointer change. Architect commits to this swap happening in the 1.5-E coaching-alignment sub-phase, NOT the 1.5-D.4 retrain sub-phase, so router/coaching pipelines update in lock-step with the model change.

### 4.7 Sub-sub-phase decomposition

| Sub-phase | Subject | Pilot+full | Owner-gate fires |
|---|---|---|---|
| 1.5-D.1 | HU reference set design (30 hands, 6 axes) | Pilot=5 hands (HU-1); full=25 hands (HU-2..HU-6) | Pilot gate; full gate; design comm merge |
| 1.5-D.2 | HU labelling (5-labeller v3.4 + Opus tier-up) | Pilot=5 hands; full=25 hands | Pilot gate; full gate |
| 1.5-D.3 | HU corpus assembly (~750 labelled situations) | Pilot=50 situations; full=700 | Pilot gate; full gate |
| 1.5-D.4 | HU model retrain (from-scratch, 5-seed, 59-surface) | 1-seed smoke; 5-seed full | Smoke gate; full ship gate |
| 1.5-E   | Router + coaching alignment (production swap to vNext-HU-59) | N/A (mechanical) | Router-swap gate; coaching-test gate |

---

## 5. Cost/time forecast

### 5.1 Per-sub-phase forecast (all estimates per `feedback_no_deadlines.md` — quality path beats schedule)

Costs are LLM API spend estimates assuming Sonnet primary + Opus tier-up sample. Wall-clock is rough order-of-magnitude (architect's estimate, not a deadline).

| Sub-phase | $$ estimate | Wall-clock (rough) | Critical path? | BINDING pilot gate | HALT condition |
|---|---|---|---|---|---|
| 1.5-A (this memo) | ~$0 | ~3-4 hr | Yes | N/A (design) | QC FAIL on memo |
| 1.5-B (feature-prune mechanical) | ~$0 | ~2-3 hr | Yes | §2.3 bit-equality verification | Bit-equality diff non-empty |
| 1.5-C (3-way verification at 59) | ~$2-5 (1 smoke + 5-seed) | ~2-4 hr training + 1-2 hr eval | Yes | §3.5 1-seed smoke | mean < 32.00/40 |
| 1.5-D.1 (HU reference set design) | ~$15-25 (6 design + 1 review agents) | ~6-8 hr | No (parallel after 1.5-C) | §4.2 pilot axis | Pilot < 80% inter-design agreement |
| 1.5-D.2 (HU labelling) | ~$80-130 (5 labellers × 30 hands + Opus tier-up sample) | ~10-15 hr labelling time + 4-6 hr review | Yes | §4.3 5-hand pilot | Pilot consensus < 80% |
| 1.5-D.3 (HU corpus assembly) | ~$40-80 (generator + filter + labelling on 750 situations × 5 labellers w/ tier-up) | ~25-40 hr labelling | Yes | §4.4 50-situation pilot | Pilot consensus < 80% OR solver agreement < 90% |
| 1.5-D.4 (HU model retrain) | ~$1-3 (smoke + 5-seed) | ~3-6 hr | Yes | §4.5 1-seed smoke | Smoke score > 5 pts below v8-HU on reference |
| 1.5-E (router + coaching alignment) | ~$0 (mechanical) | ~2-3 hr | Yes | N/A (mechanical with tests) | Coaching pipeline tests fail |

**Aggregate (rough):**

- $$ total: ~$140-245 (HU labelling dominates).
- Wall-clock total: ~55-90 hr if executed serially. Critical path optimistically ~40-50 hr if 1.5-D.1 design and 1.5-D.2 labelling-prep overlap with 1.5-C 3-way verification.
- The dominant cost driver is HU corpus labelling (~$120-200 of the total). The dominant time driver is HU labelling wall-clock + HU corpus assembly labelling.

### 5.2 Critical path

```
1.5-A (memo)
  → 1.5-B (feature-prune mechanical)
  → 1.5-C (3-way verification at 59)            [must clear before HU retrain consumes the surface]
  → 1.5-D.1 (HU reference set design)            [parallel-startable with 1.5-C; design memo waits for owner gate]
  → 1.5-D.2 (HU labelling on reference set)
  → 1.5-D.3 (HU corpus assembly: 750-situation labelling)
  → 1.5-D.4 (HU model retrain)
  → 1.5-E (router + coaching alignment; production swap)
  → Phase 1.5 SHIP
  → Phase 2 D5 (per `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`)
```

### 5.3 Off-ramps

- **1.5-C HALT (mean < 32.00):** the 2 J-B drops materially regress 3-way; halt the workstream; commission a feature-importance re-investigation. Off-ramp: revert to 61-surface and re-classify J-B as load-bearing.
- **1.5-D.2 HALT (HU labelling pilot < 80% consensus):** signals that v3.4 labelling prompt does not generalize to HU spots. Off-ramp: research-and-update labelling prompt to v3.5 with HU-specific bucket rules; rerun pilot.
- **1.5-D.4 HALT (HU smoke score > 5 pts below v8-HU on reference):** 750-corpus + 59-surface insufficient for HU. Off-ramps: (a) expand corpus 750 → 1500; (b) revert HU to v8-HU-38 in production and ship 3-way-only Phase 1.5 (partial ship); (c) re-investigate HU surface choice (subset of 59 specific to HU).

---

## 6. Falsifiable predictions (TC-X-DISPATCH-PREDICTION-VERIFICATION)

Per dispatch §"Methodology constraints (binding) — TC-X-DISPATCH-PREDICTION-VERIFICATION", architect lists falsifiable predictions to be retrospectively verified by QC at each sub-phase close:

**P1 (1.5-B):** The §2.3 bit-equality verification will produce an EMPTY diff between (column-drop-of-988-corpus-on-61) and (re-extract-of-988-on-modified-extractor). Probability of false: ≤ 5% (only fails if Step 18 has an undocumented side-effect on Steps 1-17; verified by reading `feature_extractor.py:2645-2663` and the underlying compute fns).

**P2 (1.5-C):** 5-seed mean of v9-3way-v22-on-59 ≥ 32.50/40 with high probability (≥ 80%); ≥ 33.00/40 with moderate probability (≥ 60%). Specifically, the J-B drop will NOT cause a 1+ point regression in mean, because the 2 dropped features had < 1% importance and the remaining 59 features contain the load-bearing v2.4 P1 blockers + raw equity + range composition signals.

**P3 (1.5-C, stay-wrong taxonomy):** MW-17 will remain in the PIPELINE-CANONICAL-MISMATCH category on the 59-surface (this is structural, not feature-driven; per `project_v9_3way_ceiling.md`). MW-40 / MW-45 / MW-47 will remain in the MODEL-STUCK-PIPELINE-ALIGNED category (the 2 J-B features were specifically targeted at MW-17 and MW-47 axes; their drop will not unstick those hands; in fact, dropping them removes the failed-targeting signal). Net stay-wrong count at 59: ≥ 4 of 4 unchanged (no new stay-wrongs created by drop; MW-30 and MW-46 remain solver-corrected and STAYED-CORRECT).

**P4 (1.5-D.1):** ≥ 5 of the 30 HU reference spots will be CLOSE per `feedback_close_hand_selection.md` definition (model uncertainty on v8-HU-38 + poker difficulty), of which ≥ 3 will be in axes HU-2 (drawing) and HU-6 (river decision). Reasoning: v8-HU-38 was trained on PokerBench, which weights heavily toward common decisions; semi-bluff and river bluff-catch decisions are the canonical v8 weak points.

**P5 (1.5-D.2):** Sonnet 5-labeller consensus rate on the 30-hand HU reference set ≥ 80% (≥ 24 of 30 unanimous-or-4-of-5). Reasoning: the multiway 40-hand reference set produced ≥ 85% consensus rate on v3.4 labelling per the 12.5K corpus history; HU should be at-or-above-multiway because of fewer structural axes.

**P6 (1.5-D.4):** vNext-HU-59 5-seed mean on the 30-hand HU reference ≥ 26/30. With moderate probability (≥ 60%) ≥ 28/30 (the ship gate). With low probability (≤ 30%) clears on the FIRST 5-seed run; first-run clear-rate on 12.5K-style retrain has been ~30-40% historically.

**P7 (1.5-E):** Coaching pipeline tests pass after the production swap with NO test-suite changes (only the model file and the `oracle_router.py:34` filename pointer). Reasoning: the 59-surface contains all 38 v8-HU features as a strict subset; the auto-detect logic in `gto_model.py:104` handles the surface change; coaching consumes via the router and does not address features by index.

---

## 7. Open owner-scope items (genuine trade-offs; NOT technical menus)

Per `docs/PROCESS_GUIDE.md:59-77` exception: genuine trade-offs where both options have real costs are owner decisions. Architect surfaces these explicitly and does NOT decide:

- **HU corpus size 750 vs 1500.** Architect committed to 750 in §4.4 based on PR #293 precedent + cost; 1500 would double labelling cost (~$80-160 additional) but is more conservative on coverage. Owner-gate at 1.5-D.3 dispatch.
- **Phase 1.5 ship boundary.** Currently committed: Phase 1.5 SHIP after 1.5-E (router/coaching alignment + production swap). Alternative: ship after 1.5-D.4 with 1.5-E as a follow-on. The committed sequencing keeps router/coaching consistent with model swap, but the alternative allows faster headline "Phase 1.5 done" milestone if HU retrain ships on first run. Owner may direct different sequencing.
- **Phase 2 D5 entry condition.** D5 blueprint at `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` assumes Phase 1.5 ships. If Phase 1.5 partially ships (e.g., HU only after a 3-way HALT) or fully ships, D5 entry may need re-scoping. Owner-gate at Phase 1.5 SHIP comm.

---

## 8. References

- Phase 1.5-A dispatch: `MAIN_TERMINAL_PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` (master `5863f13`, PR #306).
- Phase 1.5 queue + retrain-ordering: `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302).
- Builder directive-receipt (owner unified-surface directive): `BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md` (master `48297e4`, PR #300).
- 12.5L SHIP-A (Phase 1 INTERIM lock): master `dceb265`, PR #303; QC PASS at master `e66e2e6`, PR #305.
- 12.5L synthesis (3-lever ceiling): `PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297).
- 12.5J-B feature implementation (the 2 dropped features): `BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md`.
- 12.5K-C-E corpus + 5-seed retrain (the 988-corpus baseline): `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (master `62814a3`, PR #293).
- D5 blueprint (Phase 2 deferred): `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`.
- Project memory: `project_v9_3way_ceiling.md` (Phase 1 INTERIM ceiling + corrected stay-wrong taxonomy).
- 40-hand multiway reference set design pattern: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`.
- PROCESS_GUIDE: `docs/PROCESS_GUIDE.md` (calibration §2.1; agent counts §1.1-§1.2; experts-recommend §1.4).
- Memory feedback rules cited: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_attention_flags_when_features_change.md`, `feedback_solver_aligned_sizing.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_failure_direction_classification.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_close_hand_selection.md`, `feedback_solver_findings.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_verify_source_not_plan.md`, `feedback_builder_grounds_before_executing.md`, `project_qc_heartbeat_convention.md`.

---

**Status: design memo complete; single committed path across 5 design areas; ≥3 (in fact 7) falsifiable predictions registered for QC retro-verification; 3 owner-scope items surfaced. Awaits QC audit + owner-merge gate.**
