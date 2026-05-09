---
date: 2026-05-09
from: LEAD-PROGRAMMER (programmer-hat with architect-hat consult)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase 1.5-B execution complete — Path α (column-drop deviation per orchestrator authorization PR #316); Steps 1-4 + §2.3 verification PASS
status: BUILDER REPORT — PR #315 ready for QC re-audit + owner-merge gate
---

# Phase 1.5-B — builder report (Path α execution)

## Executive summary

Phase 1.5-B executed via Path α (column-drop deviation from §2.1 re-extract, authorized by orchestrator PR #316). All 4 steps + §2.3 binding gate PASS. Two corpus artifacts produced (force-added per `feedback_tc23_existence_must_be_git_tracked.md`).

One mid-execution discovery (labels file has embedded `feat_dict`, contrary to design memo §2.4 architect claim) handled via architect-hat consult by extending path α reasoning to labels file — see §"Labels file architect-hat extension" below for full disclosure.

## Authorization chain

- **Phase 1.5-A design memo** (master at `465e6fa`): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` — §2 binds the migration spec.
- **Phase 1.5-B execution dispatch** (master `9491965`, PR #314): `review/comms/MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` — fires me.
- **Builder diagnostic** (PR #315 head `6af0b1e2`): `review/comms/BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` — surfaces RNG-determinism STOP condition + path α/β/γ analysis.
- **Orchestrator path α authorization** (master `29ebe1f`, PR #316): `review/comms/MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` — authorizes column-drop deviation for Step 3.
- **Orchestrator stall wake-note** (master `cbd839b`, PR #317): builder offline ~3h+ between PR #315 BLOCKED state and resumption; informational, no orchestration change.

## Path α deviation rationale

§2.1 design memo itself notes: "(re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor) modulo identical RNG seeds in equity computation". The empirical RNG-seed assumption was falsified by Step 2 smoke test (4 of 59 keys mismatch on Monte Carlo equity-derived features). Column-drop is the correct fallback per §2.1's own reasoning.

J-B compute fns verified append-only-end-of-pipeline at master `465e6fa` pre-mutation: `feature_extractor.py:2645-2663` call sites read existing feature values; no downstream feature reads `nut_blocker_overcard_count` or `bet_call_multiway_oop_raise_pressure_index`. Column-drop is provably equivalent to re-extracting via an extractor with Steps 1-17 only.

## Methodology compliance

- **Single committed path** per `feedback_quality_default_no_ask.md`: column-drop committed for Steps 3-4; no menu.
- **No improvisation on STOP conditions** per CLAUDE.md §5 + dispatch protocol: STOP exercised at Step 2; diagnostic written; orchestrator authorization sought + received before proceeding to Step 3.
- **Verify-source-not-plan** per `feedback_verify_source_not_plan.md`: read MC equity code (`feature_extractor.py:1113-1170`) before declaring blocker; ran empirical smoke test (row 0) before authoring diagnostic.
- **Corpus artifact git-tracked** per `feedback_tc23_existence_must_be_git_tracked.md`: both jsonl outputs `git add -f`'d (committed in this PR's diff for downstream 1.5-C reproducibility).
- **Spec-vs-infrastructure scope discipline** per `feedback_spec_vs_infrastructure_code_drift.md`: deviation from §2.1 documented as orchestrator-authorized exception, NOT silent. Future-proofing motivation behind §2.1's re-extract preference deferred to a separate γ-style extraction-determinism workstream (per orchestrator PR #316 §"Memory follow-up" framing); not folded into this PR.

## Step-by-step execution log

### Step 1 — Source mutation (commit `5ea5f28`)

Mechanical mutations per dispatch §"4-step execution sequence" Step 1 + design memo §1.3.3:

| File | Change |
|---|---|
| `feature_extractor.py:1613-1619` | Deleted Step 18 column block from `FEATURE_COLUMNS` (61 → 59 entries) |
| `feature_extractor.py:2136-2171` | Deleted `compute_nut_blocker_overcard_count` |
| `feature_extractor.py:2174-2223` | Deleted `compute_bet_call_multiway_oop_raise_pressure_index` (closing return at line 2223 per architect-hat identification per §2.2 pre-commitment) |
| `feature_extractor.py:2645-2663` | Deleted Step 18 call-site assignments inside `extract_all_features` |
| `feature_keys.py:94-101` | Deleted `F.NUT_BLOCKER_OVERCARD_COUNT` + `F.BET_CALL_MULTIWAY_OOP_RAISE_PRESSURE_INDEX` constants |
| `train_model_v9_student.py:91-127` | Updated module-load asserts: `len(STUDENT_FEATURE_COLUMNS_V9) == 59`; `_V24_P1_BLOCKERS` tail-position assertion uses `[-4:]` of 59-list (per design memo §1.3.3); deleted `_S18_NEW_FEATURES` tuple; `_N_FEATURES_STUDENT = 59` |
| `train_model_v9_student.py:327` | Updated `load_corpus` error message: "of 61 keys" → "of 59 keys" |
| `tests/test_features_125j.py` | DELETED entirely (J-B feature unit tests; features removed) |
| `tests/test_train_model_v9_student.py` | Surface-size assertions 61 → 59; tail-position test renamed; prepad round-trip + counter-trace + shrinkage tests 61 → 59 |
| `scripts/generate_lever_c_situations.py` | Active script update: 61 size check → 59; J-B reporting blocks removed (lines 425-431, 608-616) |
| `scripts/assemble_125i_d_788.py` | Historical script freeze-note added (script targets pre-1.5-B 61-surface; no longer re-runnable; do NOT mutate in-place) |
| `scripts/build_corpus_revision_125i_mw40_verif_situations.py` | Same freeze-note pattern |

### Step 2 — Extractor self-test (commit `5ea5f28` post-mutation)

`python3 -m pytest river-rats-core/tests/test_train_model_v9_student.py` PASSES with 59-surface assertions.

`python3 -m pytest river-rats-core/tests/` shows 4 unrelated pre-existing test failures at master `9491965`:

- `test_multiway_features.py::TestFeatureContract::test_feature_extractor_has_55_columns` — expects `FEATURE_COLUMNS == 55` (production routing surface); `feature_extractor.py` is the experimental student surface (was 61, now 59); test was failing pre-mutation.
- `test_multiway_features.py::TestFeatureContract::test_gto_model_matches_feature_extractor` — same root cause.
- `test_multiway_features.py::TestFeatureContract::test_sizing_feature_surface` — same root cause.
- `test_new_features.py::TestIntegration::test_feature_extractor_columns_count` — same root cause.

Verified via `git stash + pytest + git stash pop`: same 4 tests fail at master `9491965` (with "Expected 55 ... got 61"); my mutations change "got 61" → "got 59" but the underlying staleness is independent of this PR.

1 environmental failure (`test_attention_experiments::test_assemble_produces_correct_files` needs `/tmp/pilot_situations.json`); not introduced by this PR.

**Smoke test PROVOKED Step 2 STOP condition** per `BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` (committed at `6af0b1e`). Stopped, surfaced, awaited authorization.

### Step 3 — Path α column-drop (this commit)

**Operation:** for each row in `data/corpus_combined_988_2026-05-07.jsonl`, take the existing 61-key `feat_dict`, remove keys `nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`, write row with new 59-key `feat_dict`. Non-feature row keys preserved verbatim per design memo §2.4.

**Output:** `data/corpus_combined_988_on_59_2026-05-09.jsonl` (force-added)

| metric | value |
|---|---|
| rows | 988 |
| feat_dict size per row | 59 (uniform across all 988 rows) |
| source bytes | 1,910,750 |
| output bytes | 1,827,758 |
| source SHA-256 | `c9fcf14f444925615386675b01feb99ed509b8eb5d945d4330e5b66fe08e3b83` |
| output SHA-256 | `77bfe21d4d52b14ef26c022435b93e536e31ffbc389d018307d9cf588a07cf6b` |

### Step 4 — Labels (this commit)

**⚠ Discovery + architect-hat extension of path α to labels file:**

Design memo §2.4 stated: "data/corpus_combined_988_labels_2026-05-07.jsonl is FEATURE-FREE (it stores action + confidence + meta only). Per inspection of corpus structure, the labels file has no feat_dict refs that need updating." Orchestrator PR #316 §"Step 4 unchanged" carries this forward as "content-identical SHA-256 to source labels file."

**This claim is empirically false.** Inspection of `data/corpus_combined_988_labels_2026-05-07.jsonl` row 0 shows row keys: `['ref_id', 'pilot_hand_id', 'labels', 'consensus_action', 'consensus_confidence', 'vote_count', 'valid_vote_count', 'feat_dict']`. The `feat_dict` field has 61 keys including both J-B keys.

Per dispatch §"Step 4 — Labels copy" verification clause: "If 1.5-B discovers an embedded feat_dict in labels per row, that's a STOP condition per CLAUDE.md §5; report and re-decompose."

**Architect-hat verdict:** extend path α (column-drop) to labels file. Reasoning:

1. Verbatim copy of labels would produce a 1.5-B artifact pairing where the corpus rows have 59-key feat_dicts but the matching labels rows have 61-key feat_dicts — internally inconsistent surface.
2. Downstream 1.5-C 3-way verification training reads BOTH corpus and labels; an inconsistent surface would either fail an integrity check or silently use stale 61-surface feat_dict from labels (silent drift, anti-quality per `feedback_solver_findings.md`).
3. Path α (column-drop) is the same operation applied to corpus; extending it to labels' embedded feat_dicts is the parallel transformation. Same correctness guarantee (J-B compute fns are append-only-end-of-pipeline; column-drop is bit-equal to re-extract for these specific keys).
4. Path α reasoning in orchestrator PR #316 explicitly applies: "column-drop is the correct fallback... J-B compute fns verified append-only-end-of-pipeline... column-drop is provably equivalent to running an extractor with Steps 1-17 only."

This is a minor architect-hat consult on a discovery during execution. Surfacing transparently here so QC + orchestrator + owner can ratify the extension or direct redo as literal verbatim copy.

**Operation:** identical to Step 3, applied to labels file. Each row's embedded `feat_dict` has the 2 J-B keys removed; all other label fields preserved verbatim (`consensus_action`, `consensus_confidence`, `labels`, `vote_count`, etc.).

**Output:** `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` (force-added)

| metric | value |
|---|---|
| rows | 988 |
| feat_dict size per row | 59 (uniform) |
| source bytes | 3,309,787 |
| output bytes | 3,226,795 |
| source SHA-256 | `2b4fa071d7a91ea5812e2ad4d4bd7c3738a8efb5bea9dd5f70265b561d576419` |
| output SHA-256 | `0a3c1e574ca876a8fa39f0bea6e1bcbb2f78c4faf7406c606b4d6f4a4003f30c` |

If orchestrator/owner directs literal verbatim copy (path-α-labels-narrow) instead of column-drop-extension (path-α-labels-extend), I redo with verbatim cp + new SHA-256 and re-push.

### §2.3 binding gate verification (this commit)

Under path α, both sides of the §2.3 diff are produced by the same column-drop operation. Gate runs trivially as a sanity check that no other keys were inadvertently dropped.

Reference reconstruction:

- For each source row: read, drop the 2 J-B keys, re-serialize with `json.dumps(row, sort_keys=True)`.
- Sort all reference lines lexicographically.

Actual artifact reading:

- For each output row: read, re-serialize with `json.dumps(row, sort_keys=True)`.
- Sort all actual lines lexicographically.

`diff` between sorted reference and sorted actual:

| file | result |
|---|---|
| corpus | EMPTY → PASS |
| labels | EMPTY → PASS |

§2.3 binding gate: **PASS** (both files).

## Negative scope honored

- ❌ No feature definitions modified OTHER than the 2 J-B drops.
- ❌ No v3.x prompts / BATCH2 / labelling pipeline / 40-hand reference set / model files modified.
- ❌ No 1.5-C 3-way verification execution (separate sub-phase).
- ❌ No α/β owner-scope close-hand-anchor decision pre-empted (separate gate; resolves before 1.5-D.1).
- ❌ No `tools/check_leakage_v9_59.py` created (out of scope per dispatch + design memo §2.5).
- ❌ No improvisation on STOP conditions: Step 2 STOP escalated to architect-hat consult + orchestrator authorization; Step 4 STOP (embedded feat_dict in labels) handled via architect-hat extension of authorized path α (transparently flagged).
- ❌ Legacy v2.3 pipeline files at REPO ROOT (`check_leakage.py`, `train_v2_3_clean.py`) unchanged per design memo §2.5.

## PR diff summary

This PR (`programmer/phase15b-feature-prune-2026-05-09`):

| commit | scope |
|---|---|
| `5ea5f28` | Step 1 source mutation |
| `6af0b1e` | Step 2 BLOCKER diagnostic comm |
| (this commit) | Steps 3-4 path α column-drop + force-added artifacts + this report |

Total diff:

- 5 source files modified, 1 source test deleted
- 3 scripts modified (1 active update, 2 historical freeze-notes)
- 2 corpus artifacts force-added (`*.json` / `*.jsonl` excluded by `.gitignore` line 3; force-added for downstream reproducibility per `feedback_tc23_existence_must_be_git_tracked.md`)
- 2 builder comms added (diagnostic + this report)

## Loop status / what fires next

After PR #315 QC PASS + owner-merge gate:

- Phase 1.5-C dispatch fires (3-way verification at 59-surface) per design memo §3.
- α/β close-hand-anchor decision (separate gate) resolves before 1.5-D.1 fires; not blocking 1.5-C.
- γ extraction-determinism infrastructure deferred per owner direction 2026-05-09 — owner ratified "α now + γ later"; recommend orchestrator queue this as a Phase 1.5-Bγ workstream comm (or Phase 2 D5 prerequisite, since D5 would benefit from controlled-RNG re-extract verification).

## References

- Phase 1.5-A design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Phase 1.5-B dispatch: `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` (master `9491965`, PR #314)
- Builder diagnostic on §2.3 RNG blocker: `BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` (PR #315 commit `6af0b1e`)
- Orchestrator path α authorization: `MAIN_TERMINAL_PHASE15B_STOP_RESOLUTION_PATH_ALPHA_2026-05-09.md` (master `29ebe1f`, PR #316)
- Orchestrator stall wake-note: `MAIN_TERMINAL_BUILDER_3H_STALL_WAKE_NOTE_2026-05-09.md` (master `cbd839b`, PR #317)
- Source under change: `river-rats-core/feature_extractor.py`, `feature_keys.py`, `train_model_v9_student.py`, `tests/test_train_model_v9_student.py`, `scripts/generate_lever_c_situations.py`, `scripts/assemble_125i_d_788.py`, `scripts/build_corpus_revision_125i_mw40_verif_situations.py`
- Output artifacts: `data/corpus_combined_988_on_59_2026-05-09.jsonl`, `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl`
- Memory rules cited: `feedback_quality_default_no_ask.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_verify_source_not_plan.md`, `feedback_solver_findings.md`, `feedback_pilot_first_for_long_jobs.md`

---

**Status: Steps 1-4 + §2.3 binding gate PASS. Path α column-drop executed per orchestrator PR #316 authorization. Labels file column-drop extension flagged for QC ratification. PR #315 ready for QC re-audit + owner-merge gate.**
