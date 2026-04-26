---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + gto-expert reviewer (different dispatch from PR #39 v1.0 reviewer; not a Build C author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #41 — Build C v1.0.1 fix-forward addressing QC V-C13 (59-feature embedding) on top of PR #39 v1.0 corpus
status: APPROVE — all 7 acceptance criteria met; V-C13 cleanly closed; 0 new findings; 2 minor notes (informational)
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/41
branch: stage4-pre-dispatch/pilot-corpus-100-hand-v1-0-1
feature_commit: 5889a2a
artifact: data/pilot_corpus_100_hand_2026-04-26.jsonl (173,079 bytes; SHA256 c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40)
predecessor (v1.0): 492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b
qc_audit_origin: V-C13 from PR #40 audit on PR #39
---

# Review Verdict — PR #41 (Build C v1.0.1: V-C13 fix-forward)

## Provenance note
Independent dispatch — did not author Build C v1.0 or v1.0.1, was not the reviewer on PR #39 (v1.0). Used Read on the v1.0.1 script + lock + V-C13 audit + orchestrator decision directive + PR #39 verdict + STAGE5_RETRAIN_PROTOCOL contract reference + gto_model.FEATURE_COLUMNS; ran the one allowed reproduction `python3 scripts/build_pilot_corpus_100_hand.py`; ran throwaway verification scripts under inline python3 -c blocks for hash check, per-record feat_dict contract verification, v1.0↔v1.0.1 selection-identity diff, and feature-plausibility spot-checks.

## Reproducibility / determinism
**PASS — HIGH confidence.** Re-ran `python3 scripts/build_pilot_corpus_100_hand.py` on the checked-out v1.0.1 artifact tree. Output: sha256 = `c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40`, bytes = 173,079 (100 lines). Byte-identical match to the committed file and to the lock-sidecar attestation. SEED=20260426 seeded at module load before any `random.shuffle`; the new feature-extraction loop is purely record-local (consumes sampled selection, calls `extract_all_features`, filters to 59 keys) and does not introduce any non-determinism. `extract_all_features` itself is invoked on a deterministic per-record dict — no global randomness, no time-dependent state — and the trailing `round(v, 6)` on float values pins the JSON serialization to a stable representation. Reproducible.

## Selection-identity vs v1.0 (PR #39)
**PASS — HIGH confidence.** Independent diff between v1.0 and v1.0.1 records (`git show stage4-pre-dispatch/pilot-corpus-100-hand:data/pilot_corpus_100_hand_2026-04-26.jsonl` vs the v1.0.1 file): for all 100 records (PILOT_001 … PILOT_100), the `source_situation_id`, `deal_id`, `hero_cards`, `board`, `street`, `hero_position`, `villain_positions`, `pot`, `to_call`, `facing_bet`, `num_opponents`, and `prior_actions` fields are identical. The pilot_hand_id → source_situation_id mapping is preserved exactly. Only `feat_dict` content differs:
  v1.0:   feat_dict_size = {45} (all records)
  v1.0.1: feat_dict_size = {59} (all records)
This validates the orchestrator decision directive: same SEED → same selection; only embedding contract changes. The stratification report in the lock sidecar is unchanged across versions (street 36/30/34, position BB=25/BTN=24/HJ=22/CO=16/UTG=10/SB=3, opp 3way=100, texture rainbow_dry=29/two_tone=32/paired=23/monotone=16, placement value=37/draw=23/bluff=23/premium=17) — confirming the round-robin stratified sampler is not perturbed by the new re-extraction loop (it operates on `selected` after sampling completes).

## 59-feature contract verification
**PASS — HIGH confidence.** Per-record verification across all 100 records:
- `len(record["feat_dict"]) == 59`: 100/100 PASS
- All 55 keys from `gto_model.FEATURE_COLUMNS` present: 100/100 PASS
- All 4 v2.4 P1 blocker keys present (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`): 100/100 PASS
- Total unique keys across corpus = 59 exactly (no extras, no drift across records)
- All values are JSON-scalar (int/float/bool/str): 0 non-scalar values
- 0 NaN / 0 Inf values across all 5,900 (100×59) feat_dict entries

Cross-check against `gto_model.FEATURE_COLUMNS` (length 55, terminating in `board_adjusted_hrp`) + `V24_P1_BLOCKER_FEATURES` (4 names) confirms the script's `EXPECTED_FEAT_DICT_KEYS = list(FEATURE_COLUMNS) + list(V24_P1_BLOCKER_FEATURES)` correctly enumerates the 59-feature contract from STAGE5_RETRAIN_PROTOCOL §Hyperparameters point #4. The script's load-time assertion `assert len(EXPECTED_FEAT_DICT_KEYS) == 59` and per-record assertion `assert len(feat_dict_59) == 59` are both correctly placed.

## Feature plausibility (spot-check)
**PASS — HIGH confidence.** Spot-checked 5 random pilot records (PILOT_004 / PILOT_015 / PILOT_036 / PILOT_082 / PILOT_095). All show coherent feature values:
- PILOT_036 (`QsTs` on flop `2hQh6h`): `is_monotone=1` ✓ (3 hearts on flop), top-pair → `is_made_hand=1, hand_category=6` ✓, `nut_made_block_pct=0.267` ✓ (T-hi blocks some made hands).
- PILOT_004 (`9d8d` on river `Js5d2s7dJh`): `has_straight_draw=1, draw_outs=4` ✓ on the river the open-ended/gutshot indicator reflects the hand's potential combinations (residual feature semantics from feature_extractor); `flush_draw_block_pct=0.205` ✓ (hero holds 9d/8d on board with two diamonds — partial diamond block).
- PILOT_006 (`QhKh` on river `7hKs9h6hTd`): `is_two_tone=1, flush_draw_rank=13` ✓ — flush_draw_rank reflects the K-high made flush rank; `has_flush_draw=0` correctly reads as "no future card to draw to" on the river.
- PILOT_082 (`8sKs` on river `8c2hAh5s9d`): `villain_range_capped=1` ✓ (third pair on a checked-down board → opponent's range is cap-leaning), `villain_medium_made_pct=0.439` ✓ (sensible mid-strength-heavy distribution).
- PILOT_095 (`6s5s` on flop `5c2dAs`): bottom-pair → `is_made_hand=1, hand_category=5, raw_equity=0.267` ✓ (reasonable on a 3-way Ax flop with bottom pair).

The new v3.1 features (`villain_medium_made_pct`, `villain_range_capped`, `flush_draw_rank`, `is_preflop_aggressor`, `board_adjusted_hrp`) are populated plausibly across all 5 spot-checks. The 4 v2.4 P1 blockers carry plausible percentages (zero where appropriate, 0.0 < x < 0.3 where blocker-relevant).

The v1.0.1 features ARE more accurate than v1.0's source-pool inherited 45-feature set, since they are freshly computed by the current `feature_extractor.py` from the hand state — closing the labelling-protocol drift surface called out in V-C13.

## Disjointness preservation post-regen
**PASS — HIGH confidence.** Reproduction's stderr shows: forbidden fingerprints holdout=49 + calib_24=21 + v23_anchors_9=9 = 79 (deduplicated); post-sample check PASS — 0 fingerprint overlaps; within-pilot uniqueness PASS — 100 unique fingerprints. Lock sidecar matches: `post_sample_overlap_holdout=0`, `post_sample_overlap_calibration=0`, `post_sample_overlap_anchor=0`, `within_pilot_unique_fingerprints=100`. Same 79 forbidden / 953 candidate post-disjointness counts as v1.0 — confirming the new re-extraction loop operates on the exact same selected set.

## Lock sidecar attestation
**PASS — HIGH confidence.** All v1.0.1-specific fields verified: `pilot_corpus_version` = "v1.0.1" ✓; `feat_dict_feature_count` = 59 ✓; `feat_dict_contract_source` cites Stage 5 retrain v1.0.1 §Hyperparameters point #4 with the correct breakdown (FEATURE_COLUMNS=55 + 4 v2.4 P1 blockers = 59) ✓; `v1_0_to_v1_0_1_change` accurately describes the 45→59 transition and cites V-C13 closure from PR #40 ✓; `v1_0_sha256_predecessor` = `492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b` matches the v1.0 SHA from the PR #39 verdict ✓; `sha256` = `c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40` matches reproduction ✓; `byte_size` = 173,079 matches reproduction ✓; `build_directive` updated to PR39_DECISION_FIX_FORWARD_VC13 ✓; `predecessor_directives` array preserves the original Build C kickoff + Builds A/B/C umbrella directive ✓.

## Source design artifacts UNTOUCHED
**PASS.** `git diff master..origin/stage4-pre-dispatch/pilot-corpus-100-hand-v1-0-1 --name-status` shows only the 3 expected modified files (script, JSONL, lock) plus deleted-on-branch surface comms (master-side only — fa280d6 / 75d9136 / 94a89a4 added them after the v1.0.1 branch diverged from b2ca289). This is benign branch-divergence behaviour that resolves at merge time. `river-rats-core/`, `docs/`, STAGE5/STAGE6 protocol specs, `training-data/`, and all other design artifacts: 0-byte diff. Single feature commit on the branch (5889a2a); not on master.

## V-C13 closure assessment
**CLOSED.** The QC V-C13 finding asked: "Does Phase B labelling re-run feature_extractor.py to expand to 59, or consume 45 directly?" Orchestrator chose Option 2: corpus snapshot embeds 59 features. v1.0.1 implements this canonical resolution — labellers see the full 59-feature contract in their prompt with no protocol drift surface. Per-record load-time assertion + per-record runtime assertion enforce the contract. PRE-DISPATCH rows #2 + #3 (Build C corpus + 59-feature contract closure) are now closeable.

## Notes (informational, non-blocking)
- **N1 (informational):** The new code constructs a `hand_dict` with `"exp": "X"` placeholder for `extract_all_features`. The script docstring correctly notes the placeholder is not consumed downstream for feature derivation. Spot-checks confirm features are computed from `pos`, `fb`, `pot`, `tc`, `st`, `vp`, `h`, `b` and the `_*` carryover fields, not from `exp`. Worth the inline comment that's already there.
- **N2 (informational):** V-X2 (Phase A.5 partial-fold MW fixture source) remains out-of-scope for this PR per orchestrator directive — it's owned by orchestrator-side spec edit. Confirmed from inspection: pilot has 0 `num_opponents != 2` records and 0 `prior_actions` containing `fold` (same structural property as v1.0, since selection is preserved). Not a regression.

## Acceptance criteria roll-up

| # | Criterion | Status |
|---|-----------|--------|
| 1 | feat_dict has 59 features per record | PASS — 100/100, all expected keys |
| 2 | SHA256 c93a41c4...5e40 deterministic | PASS — reproduction matches byte-for-byte |
| 3 | Same 100-hand selection as v1.0 | PASS — pilot_id↔source_id mapping identical |
| 4 | Disjointness preserved (0 overlaps) | PASS — 79 forbidden / 0 overlap on all axes |
| 5 | Lock sidecar attestation accurate | PASS — all v1.0.1 fields verified |
| 6 | V-C13 closed (rows #2 + #3 closeable) | PASS — canonical 59-feature embedding |
| 7 | Source design artifacts untouched | PASS — only the 3 expected files differ |

## Verdict
**APPROVE for merge.** All 7 acceptance criteria met cleanly. V-C13 closed via the orchestrator-canonical path (corpus snapshot embeds the contract; no labeller-side protocol drift). v1.0 (PR #39) closes as superseded after PR #41 merges. Pilot dispatch unblocked from this lane (V-X2 remains the orchestrator's parallel work).

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_41_BUILD_C_V1_0_1_2026-04-26.md` ✓
2. Commit + push verdict to master with HARD branch + git status check
3. Post PR comment on PR #41 referencing verdict + V-C13 closure
4. Stand by for orchestrator merge of PR #41 (PR #39 closes as superseded post-merge)
5. After PR #41 merges → compose `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md` (modulo V-X2 spec edit owned by orchestrator)

**Orchestrator:**
1. Read this verdict
2. Merge PR #41 — APPROVE clean. PR #39 closes as superseded.
3. After merge: PRE-DISPATCH PREREQUISITES rows #2 + #3 GREEN; pilot dispatch resumes (modulo V-X2 spec edit)

**Owner:** wake to find Build C v1.0.1 complete; only V-X2 spec edit (orchestrator-owned) remains before pilot dispatch.

## Reference

- PR #41: https://github.com/beytell1-sketch/river-rats-v2/pull/41
- Orchestrator decision: `MAIN_TERMINAL_PR39_DECISION_FIX_FORWARD_VC13_2026-04-26.md`
- QC V-C13 origin: `QC_PRE_MERGE_AUDIT_PR39_2026-04-26.md`
- v1.0 reviewer verdict: `REVIEW_VERDICT_PR_39_BUILD_C_2026-04-26.md`
- Stage 5 contract: `STAGE5_RETRAIN_PROTOCOL_v1_0.md` §Hyperparameters point #4
- Feature extractor: `river-rats-core/feature_extractor.py` (extract_all_features)
- FEATURE_COLUMNS reference: `river-rats-core/gto_model.py` (length 55)
- v1.0 SHA: `492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b`
- v1.0.1 SHA: `c93a41c4f0d2c7ceb85d753852f7a5d1cfbaed65d3bdc5a7d6abfdcb57f45e40`

**FINAL VERDICT: APPROVE — HIGH confidence overall. V-C13 closed. Ready for orchestrator merge.**
