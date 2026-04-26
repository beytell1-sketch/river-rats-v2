---
date: 2026-04-26
from: General-purpose subagent acting as INDEPENDENT ml-architect + gto-expert reviewer (different dispatch from Build A/B reviewers and Build C author)
to: Main terminal (orchestrator) · Owner
re: Independent review on PR #39 — Build C: pilot 100-hand stratified corpus (`a3b7828`)
status: APPROVE — all required acceptance criteria met; 1 MED finding flagged for labelling-protocol attention (deal-level correlation), 2 NITs
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/39
branch: stage4-pre-dispatch/pilot-corpus-100-hand
artifact: data/pilot_corpus_100_hand_2026-04-26.jsonl (commit a3b7828; 131,835 bytes; SHA256 492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b)
predecessor: 3241413 (master / PR #37 Build B merged)
predecessor_directive: 3f9564e (Builds A/B/C) + PR37_MERGE_ACK_BUILD_C_KICKOFF
qc_audit: TC-23 (PRE-DISPATCH rows #2 + #3)
---

# Review Verdict — PR #39 (Build C: pilot 100-hand stratified corpus)

## Provenance note
Independent dispatch — did not author Build C and was not the reviewer on Builds A or B. Used Read on the script + lock + holdout spec + calibration_exam.py + calibration JSON; ran the one allowed reproduction of the build script; wrote three throwaway verification scripts under /tmp (independent fingerprint parsing, stratification re-derivation, deal-diversity analysis).

## Reproducibility / determinism
**PASS — HIGH confidence.** Re-ran `python3 scripts/build_pilot_corpus_100_hand.py` on the checked-out `a3b7828` artifact. Output SHA256 = `492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b`, byte_size = 131,835 — byte-identical to the committed file. SEED=20260426 is fixed at module import; `random.shuffle` calls in `_stratified_sample` are seeded deterministically. Reproducible.

## Independent disjointness verification
**PASS — HIGH confidence on all three sources.** Built an independent fingerprint extractor (different regex parser, no shared code with the script):

- **Stage 6 50-hand holdout:** parsed 49 hero/board fingerprints from `STAGE6_HOLDOUT_TESTSET_v1_0.md` (HOLDOUT_032 is a preflop-only hand with `Board: PREFLOP (no flop yet …)` so it has no card fingerprint — both my parser and the script's parser correctly skip it; this is not a defect because all 100 pilot hands are postflop). **Pilot ∩ holdout = 0.**
- **v2.3 calibration legacy:** parsed 21 unique fingerprints across `calibration_situations.json` + 4 mirror/batch files (72 entries → 21 unique after intra-corpus dedup). **Pilot ∩ calib = 0.**
- **v2.3 anchor extension (9 IDs):** all 9 IDs (`d8886/d2410/d8963/d3178` predicate/mixed-zone + `d3688/d4312/d9556/d2074/d5466` Group-D) found in `training-data/3way_situations_10k.jsonl`; 9 unique fingerprints extracted. **Pilot ∩ anchor = 0.**

Forbidden union: 79 fingerprints (matches lock.json `total_forbidden_fingerprints_deduplicated=79`). Zero overlap on any axis. Cross-checked against `_NEW_HARD_ANCHOR_IDS` and `GROUP_D_REVERSAL_HANDS` in `river-rats-core/calibration_exam.py` — script's anchor list is correct.

## Within-pilot uniqueness
**PASS — HIGH confidence.** All 100 pilot records have distinct `(sorted(hero), sorted(board))` fingerprints under independent re-extraction. No hero/board card overlap within any record. No duplicate cards within any record. No NaN values in any `feat_dict` field.

## Stratification report verification
**PASS — HIGH confidence.** Re-derived all 5 dimension counters from the committed JSONL using my own implementation of texture/placement/opponent-bucket logic; results MATCH lock.json `stratification_report` byte-for-byte:
- street: flop=36, turn=30, river=34
- hero_position: BTN=24, BB=25, HJ=22, CO=16, UTG=10, SB=3
- opponent_count_bucket: 3way=100
- board_texture: rainbow_dry=29, two_tone=32, paired=23, monotone=16
- hero_range_placement: premium=17, value=37, draw=23, bluff=23

5 random spot-checks (PILOT_004/015/036/082/095) confirmed correct bucket assignment for street, position, opponent count, texture (flop-only), and placement.

Additional finding: every selected hand sits in its own 5-D stratum bucket — 100 hands fill 100 distinct strata out of the 173 source-pool strata. This is the strongest possible stratification given the round-robin selection logic, and confirms the greedy least-filled-first algorithm is working as designed.

## Stratification adequacy assessment
**Acceptable for Stage 4 pilot scope** with caveats. ml-architect / gto-expert read:

- **5-D coverage:** sound choice of dimensions (street × position × opp-count × texture × placement). The 100-hand → 100-bucket fill rate means each labelled hand contributes maximum information to bucket-level disagreement diagnosis.
- **Single opponent_count_bucket (3way=100):** acceptable — pool is 3-way-only by Stage 4 plan and Builder flagged this as a known limitation. Generalisation to HU/4-way+ requires post-pilot expansion.
- **Position skew:** SB=3 and UTG=10 are under-represented but unavoidable (3-way pool naturally has fewer SB/UTG situations after open-fold filtering). Adequate for pilot.
- **Range-placement balance (17/37/23/23):** value-heavy is expected since `is_made_hand` is permissive (any pair / TP+); premium=17 is a reasonable share of strong holdings; draw=23 and bluff=23 give labelling disagreement surface across both equity-realisation and bluff-frequency calls.
- **Board texture (29/32/23/16):** good diversity across all four textures with monotone 16 being smallest but still ≥15% — adequate to surface texture-conditioned disagreement.
- **Texture caveat (NIT):** the texture function uses only the flop (`cards[:3]`), so a turned/rivered pair or flush on a `rainbow_dry` flop is still labelled `rainbow_dry`. This is internally consistent with the source pool's flop-texture convention but means turn/river `paired` actually means flop-paired, not board-paired-at-decision-time. Worth noting for label-disagreement analysis but not a defect.

No blind spots blocking pilot purpose (surfacing labelling disagreement on a representative postflop 3-way slice).

## Poker-quality plausibility
**PASS — HIGH confidence.** Spot-checked 10 random hands (PILOT_014/016/029/041/065/066/072/077/080/083); all are real plausible poker situations with consistent prior_actions, sane pot sizes, valid card combinations, no impossible hands. Notable verifications:
- PILOT_041 `5cAc` on monotone flop `8c6cKc` correctly flagged `is_monster=1` (nut flush) — sanity check on placement logic.
- PILOT_080 `TdKd` on `JsTsKhAh2h` flagged value+draw with `has_straight_draw=1` on a river — slightly odd source-pool feat (no draw on river), but this is a `feat_dict` quirk inherited from the source 962-pool, NOT introduced by Build C.
- All `pot/to_call/facing_bet` triples are internally consistent (e.g. PILOT_029 `pot=133, to_call=53, facing_bet=True` is a faced 53-into-80 bet on river — coherent).

## Hash-lock + sidecar correctness
**PASS — HIGH confidence.** Recomputed SHA256 over the JSONL bytes = `492154…ef4b` matches lock.json `sha256` field; recomputed `byte_size` = 131,835 matches lock.json `byte_size`. All reported counts (forbidden=79, holdout=49, calib=21, anchor=9, within-pilot uniqueness=100, candidate pool post-disjointness=953) cross-check correctly against my independent re-extraction.

## Source design artifacts UNTOUCHED
**PASS — HIGH confidence.** `git diff master..origin/stage4-pre-dispatch/pilot-corpus-100-hand --name-status` shows exactly:
- `A scripts/build_pilot_corpus_100_hand.py`
- `A data/pilot_corpus_100_hand_2026-04-26.jsonl`
- `A data/pilot_corpus_100_hand_2026-04-26.lock.json`
- `D review/comms/PR39_BUILD_C_PILOT_CORPUS_100_OPENED_2026-04-26.md` (this file was added on master at 912fc9e AFTER the branch diverged; "deletion" is just the diff direction, not an actual removal)

Zero changes to `river-rats-core/`, `training-data/`, `review/calibration_situations.json`, or any other existing artifact.

## Branch verification
**PASS.** Single feature commit `a3b78284ba1163ad28edf70eaee37aa34559d6a7` on `stage4-pre-dispatch/pilot-corpus-100-hand`; branch is one commit ahead of master at the divergence point (3241413). Not on master. PR additions=625 lines (100 JSONL + 61 lock + 464 script), deletions=0.

## TC-23 closure
**PASS.** With the artifact verified deterministic, disjoint, stratified, hash-locked, and source-untouched, PRE-DISPATCH PREREQUISITES rows #2 (pilot 100-hand corpus) and #3 (corpus disjointness from holdout/calibration) close RED → GREEN on merge. After merge, all 4 PRE-DISPATCH rows are GREEN and Phase A.1-A7 dispatch can resume per directive.

## Findings summary

**MEDIUM (1):**
- **Deal-level correlation** — The 100 pilot hands come from only **63 unique deal_ids**. 24 deals contribute ≥2 hands; deal `3409` contributes 6 hands (HJ/BB/BTN across flop/turn/river); deals `6522` and `4775` contribute 5 each. The fingerprint dedup is at `(sorted(hero), sorted(board))` granularity, but multiple records can share the same flop board across positions/streets. This is fine for labelling each decision independently, but the labelling-protocol owner should be aware that "labellers seeing the same board twice from different perspectives" may produce correlated disagreement signals — adjust analysis weighting accordingly. Not a build defect; a labelling-pilot consideration.

**NITs (2):**
- **Script line-count discrepancy** — Reviewer brief says "333-line generator"; actual script is 464 lines. Brief metadata, not artifact issue.
- **`GTO_REVERSAL_NEW_ANCHORS` naming** — The script's variable contains 4 IDs (`d8886/d2410/d8963/d3178`), but only 2 of those (`d2410`, `d3178`) are predicate-reversals in `calibration_exam.py`'s `_PREDICATE_REVERSAL_ANCHORS`; the other 2 (`d8886`, `d8963`) are mixed-zone hard anchors, not reversals. The name suggests they're all reversals. Functionally correct (all 4 are v2.3 hard anchors that must be kept disjoint), but renaming to `V23_NEW_HARD_ANCHOR_IDS` would match `calibration_exam.py`'s `_NEW_HARD_ANCHOR_IDS` exactly. Cosmetic only.

**HIGH:** none.

## VERDICT
**APPROVE — overall confidence HIGH.**

All 9 acceptance criteria are met:
1. ✓ 100 hands selected, deterministic via SEED=20260426 (re-run produces byte-identical artifact)
2. ✓ Disjointness verified independently — 0 overlaps with each forbidden set (49 holdout + 21 calib + 9 anchor = 79 dedup)
3. ✓ Within-pilot uniqueness — 100 unique (hero, board) fingerprints, no duplicates
4. ✓ Stratification re-derived correctly across all 5 dimensions (lock.json values match my independent re-derivation byte-for-byte)
5. ✓ SHA256 hash-lock verified (`492154…ef4b`) and sidecar byte_size accurate
6. ✓ Stratification adequate for Stage 4 pilot scope (every hand in its own bucket; opponent_count single-bucket noted as known limitation)
7. ✓ Poker-quality plausibility passed on 10-hand spot check + all-100 card-validity scan
8. ✓ Source design artifacts UNTOUCHED (only 3 new files added)
9. ✓ Closes PRE-DISPATCH PREREQUISITES rows #2 + #3 RED → GREEN

The artifact is production-ready as the Stage 4 pilot 100-hand corpus. The MED finding (deal-level correlation, 63 unique deals → 100 hands) is a labelling-protocol attention item, not a build defect — should be communicated to the labelling-pilot lead but does not block merge.

**Required fixes:** None.
**Blockers:** None.

## Action

**Builder:**
1. Write this verdict to `review/comms/REVIEW_VERDICT_PR_39_BUILD_C_2026-04-26.md` ✓
2. Commit + push verdict to master with branch verification
3. Post PR comment on PR #39 referencing verdict + flagging MED to labelling-protocol owner
4. After PR #39 merges → surface `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md` (all 4 PRE-DISPATCH RED rows GREEN; pilot dispatch resumes)

**Orchestrator:**
1. Read this verdict
2. Merge PR #39 — APPROVE clean, MED is labelling-protocol consideration not build defect
3. After merge: PRE-DISPATCH gate FULLY CLEAR → re-issue Pilot Orchestrator dispatch directive (Phase A.1-A7 preflight per `082336d`)

**Owner:** wake to find Build C complete; PRE-DISPATCH gate fully clear; pilot dispatch resumes.

## Reference

- PR #39: https://github.com/beytell1-sketch/river-rats-v2/pull/39
- Feature commit: `a3b7828`
- Predecessor PRs: PR #35 (Build A SEALED), PR #37 (Build B SEALED)
- Build C kickoff: `MAIN_TERMINAL_PR37_MERGE_ACK_BUILD_C_KICKOFF_2026-04-26.md`
- Builds A/B/C directive: `3f9564e`
- Source pool: `training-data/3way_situations_10k.jsonl` (962 candidates)
- Stage 6 holdout: `STAGE6_HOLDOUT_TESTSET_v1_0.md` (hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`)
- v2.3 calibration: `river-rats-core/calibration_exam.py` v2.3 (constants by name)
- Pilot orchestration spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` at master `c4f29a5`

**FINAL VERDICT: APPROVE — HIGH confidence overall. PRE-DISPATCH gate fully clear on merge. Pilot dispatch resumes.**
