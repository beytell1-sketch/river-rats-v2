---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + gto-expert reviewer (different dispatch from PR #43 v1.0 reviewer; not Build D author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #45 — Build D v1.0.1 fix-forward addressing V-D9 hash-lock determinism (`1d2c23e`)
status: APPROVE — all 7 acceptance criteria PASS; V-D9 cleanly closed; 0 findings (no MED, no HIGH, no NIT escalation)
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/45
branch: stage4-pre-dispatch/phase-a5-partial-fold-fixtures-v1-0-1
artifact: data/phase_a5_partial_fold_fixtures_2026-04-26.jsonl (10,760 bytes; SHA256 98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319)
predecessor (v1.0): c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513
qc_audit_origin: V-D9 from PR #43 reviewer (commit 488373c)
---

# Review Verdict — PR #45 (Build D v1.0.1: V-D9 fix-forward)

## Provenance note
Independent ml-architect + gto-expert reviewer dispatch. Did not author Build D and was not the reviewer on PR #43 (v1.0). Used Read on the v1.0.1 script + lock + V-D9 origin verdict + orchestrator decision directive + Build C v1.0.1 SEED pattern reference; ran two consecutive `python3 scripts/build_phase_a5_partial_fold_fixtures.py` reproductions for determinism verification; ran inline python3 -c verification scripts for hash check, per-record fixture-spec diff vs v1.0, disjointness re-derivation against all 4 forbidden sets, 59-feature contract verification.

## Verdict
**APPROVE for merge — overall confidence HIGH. V-D9 closed cleanly. Ready to unblock Phase A.5 dispatch.**

## Cross-check results

### 1. Two-run determinism — **PASS (PRIMARY criterion)**
Ran `python3 scripts/build_phase_a5_partial_fold_fixtures.py` twice consecutively. Both runs produced byte-identical output:
- Run 1 SHA256: `98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319` (10760 bytes)
- Run 2 SHA256: `98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319` (10760 bytes)
- Committed bytes (HEAD) SHA256: identical match

This closes V-D9. The 1-line `random.seed(20260426)` at module load (lines 68-69) reproducibly seeds Python's `random` module before `feature_extractor.extract_all_features` triggers `_true_multiway_equity_mc()`'s 2000-trial sampling. SEED constant matches Build C v1.0.1 (`5889a2a` line 69) — same project-wide date-stamped pattern.

### 2. Same 5 fixture specs as v1.0 — **PASS**
Independent record-by-record diff between v1.0 (`70bb66f` jsonl, SHA `c196fb82...513`) and v1.0.1 confirmed all 9 spec fields (`fixture_id`, `partial_fold_scenario`, `hero_position`, `hero_cards`, `board`, `street`, `villain_positions`, `num_opponents`, `prior_actions`) byte-identical across all 5 records. Only equity-derived `feat_dict` keys differ — and only the 4 attested ones: `equity_vs_range`, `raw_equity`, `equity_margin`, `board_adjusted_hrp`. Zero non-equity feat_dict diffs. Fixture `phase_a5_pf_003` (AsAd vs Kh8c3sQd) shows zero diffs even in equity fields, consistent with deterministic equity for nut overpair vs minimal MC variance — not a defect.

### 3. Disjointness preserved — **PASS**
Independent re-derivation of all 4 forbidden sets with identical fingerprint method (sorted hero, sorted board): holdout=49, calib=21, anchor=9, pilot=100, dedup=179. All 5 fixture fingerprints distinct from forbidden universe; zero overlaps in any of the 4 sets. Matches both lock sidecar attestations and v1.0 reviewer's independently-counted figures (i.e., disjointness invariant under MC re-seeding, as expected since fingerprint depends only on cards).

### 4. 59-feature contract preserved — **PASS**
Independent load of `FEATURE_COLUMNS` from `river-rats-core/gto_model.py` (length 55) + 4 v2.4 P1 blockers (`nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`) = 59 expected keys. All 5 records have exactly 59 keys, set-equal to expected; zero missing, zero extra. Inherits Build C v1.0.1 contract per `feat_dict_contract_source` attestation.

### 5. Lock sidecar v1.0.1 attestations — **PASS**
- `build_version=v1.0.1` ✓
- `build_seed=20260426` ✓ (matches Build C v1.0.1 SEED)
- `v1_0_to_v1_0_1_change` explanatory note present and accurate ✓
- `v1_0_sha256_predecessor=c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513` ✓ (independently verified by hashing v1.0 file content from commit `70bb66f`)
- `sha256=98e4309a...4319`, `byte_size=10760` match committed bytes and re-derivation ✓
- All disjointness counters match independent recount ✓

### 6. V-D9 closed
Root cause (unseeded MC equity) addressed at the right layer (module load, before `feature_extractor` import side-effects) with the project-canonical SEED. The PR author chose Option A from orchestrator directive correctly. No regressions.

### 7. Source design artifacts UNTOUCHED — **PASS**
`git diff master..head --name-status` shows only 3 expected files (script, jsonl, lock). No changes to `river-rats-core/` (feature_extractor, gto_model, oracle_router, calibration_exam), no changes to `docs/`, no changes to existing review specs (Stage 4/5/6, calibration manifests, anchor sources). Cherry-pick base of v1.0 fixture work + 1 surgical modification commit — branch hygiene clean.

## Findings: NONE

The script change is minimal, targeted, and surgical. Diff is 23 added lines (10 docstring expansion, 1 import, 5 SEED block, 13 lock-sidecar attestation expansion) and 2 modified lines (docstring §Determinism, build_version literal). No code paths altered beyond the deterministic seeding. The same scenario data and disjointness logic execute identically — only the MC sampling sequence is now reproducible.

The "v1.0 bytes valid + only re-derivation broke" framing in the directive and lock note is accurate: v1.0 bytes were a single non-reproducible MC realization; v1.0.1 bytes are now the canonical seeded realization.

## Carryforward observations (informational, non-blocking)

- Pattern coherence: SEED=20260426 now consistent across Build C v1.0.1 and Build D v1.0.1; recommended that any future Build E/F MC-touching scripts adopt the same date-stamped seed for cross-build reproducibility audit.
- The PR author correctly resisted any temptation to alter scenario data, disjointness logic, or feature contract — this is a true minimal fix-forward.

## Acceptance criteria roll-up

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Two-run determinism PASS | PASS — byte-identical reproductions |
| 2 | Same 5 fixture specs as v1.0 | PASS — 9/9 spec fields byte-identical per record |
| 3 | Disjointness preserved | PASS — 0/0/0/0 overlaps |
| 4 | 59-feature contract preserved | PASS — 100/100 feature checks |
| 5 | Lock sidecar v1.0.1 attestation accurate | PASS — all fields verified |
| 6 | V-D9 closed | PASS — canonical seeded realization |
| 7 | Source design artifacts untouched | PASS — only 3 expected files differ |

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_45_BUILD_D_V1_0_1_2026-04-26.md` ✓
2. Commit + push verdict to master with HARD branch + git status check
3. Post PR comment on PR #45 referencing verdict + V-D9 closure
4. Stand by for orchestrator merge (PR #43 closes superseded post-merge)
5. After PR #45 merges → compose `BUILDER_BUILDS_ABCD_COMPLETE_2026-04-26.md` (final builder signal before pilot dispatch resumes)

**Orchestrator:**
1. Read this verdict
2. Merge PR #45 — APPROVE clean. PR #43 closes as superseded.
3. After merge: V-X2 + V-D9 both closed; PRE-DISPATCH PREREQUISITES rows #2/#3/#5/#6 all GREEN; only Phase A.5 spec edit (orchestrator-owned) remains before pilot dispatch resumes.

**Owner:** wake to find Build D v1.0.1 complete; only Phase A.5 spec edit remains before pilot dispatch.

## Reference

- PR #45: https://github.com/beytell1-sketch/river-rats-v2/pull/45
- Feature commit: `1d2c23e`
- Decision directive: `MAIN_TERMINAL_PR43_DECISION_FIX_FORWARD_VD9_2026-04-26.md`
- v1.0 reviewer verdict (V-D9 origin): `REVIEW_VERDICT_PR_43_BUILD_D_2026-04-26.md`
- v1.0 SHA: `c196fb82cf78b6c02660dca72051df36938ebfeca87ebd23e935ec96b510f513`
- v1.0.1 SHA: `98e4309a21b464f8087d525eee0c12681d5f815a3b1b5bd7444d3f108eef4319`
- Build C v1.0.1 (SEED pattern reference): commit `5889a2a` / `scripts/build_pilot_corpus_100_hand.py` lines 68-70

**FINAL VERDICT: APPROVE — HIGH confidence. V-D9 closed. Ready for orchestrator merge.**
