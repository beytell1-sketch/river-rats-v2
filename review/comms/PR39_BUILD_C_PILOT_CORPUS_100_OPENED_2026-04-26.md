---
date: 2026-04-26
from: Logic builder (Build C author)
to: Main terminal (orchestrator) · Owner · Independent reviewer (when dispatched) · QC stream (TC-23 + V-C vectors candidate; TC-15 multi-expert per QC's standing offer)
re: PR #39 OPEN — Build C: pilot 100-hand stratified corpus + generation script; per orchestrator directives 3f9564e + PR37_MERGE_ACK_BUILD_C_KICKOFF; closes PRE-DISPATCH PREREQUISITES rows #2 + #3; FINAL PRE-DISPATCH gate item; reviewer dispatch next builder action
status: BUILD COMPLETE → REVIEWER PENDING
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/39
branch: stage4-pre-dispatch/pilot-corpus-100-hand
feature_commit: a3b7828
directive_source: MAIN_TERMINAL_PR37_MERGE_ACK_BUILD_C_KICKOFF_2026-04-26.md + Builds A/B/C 3f9564e
predecessors: PR #35 Build A (SEALED) + PR #37 Build B (SEALED)
qc_audit_offer: V-C1...V-C3 vectors expected; TC-15 multi-expert recommended
---

# PR #39 Opened — Build C (pilot 100-hand stratified corpus)

## Summary

**Final PRE-DISPATCH gate item.** Three new files:
- `scripts/build_pilot_corpus_100_hand.py` — corpus generator (deterministic SEED=20260426)
- `data/pilot_corpus_100_hand_2026-04-26.jsonl` — 100 hands, 131,835 bytes
- `data/pilot_corpus_100_hand_2026-04-26.lock.json` — sidecar hash + reports (force-added past `.gitignore` `*.json` glob)

**SHA256:** `492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b`

After PR #39 merge: all 4 RED PRE-DISPATCH PREREQUISITES rows GREEN; pilot dispatch resumes (Phase A.1-A7 preflight per `082336d`).

## Source

`training-data/3way_situations_10k.jsonl` (962 candidates).

## Stratification (5 dimensions per directive)

| Dimension | Distribution |
|-----------|--------------|
| street | flop=36, turn=30, river=34 |
| hero_position | BTN=24, CO=16, HJ=22, BB=25, SB=3, UTG=10 |
| opponent_count_bucket | 3way=100 (pool 3-way only — see Known Limitations) |
| board_texture | rainbow_dry=29, two_tone=32, paired=23, monotone=16 |
| hero_range_placement | premium=17, value=37, draw=23, bluff=23 |

173 unique 5-D stratum buckets observed. Greedy round-robin sampling on least-filled buckets.

## Disjointness verification (per Stage 6 v1.0 §"Non-overlap verification")

Forbidden fingerprints: **79 total (deduplicated)**:

| Source | Fingerprints |
|--------|-------------|
| Stage 6 50-hand holdout (`STAGE6_HOLDOUT_TESTSET_v1_0.md` HOLDOUT_001-050) | 49 (1-hand dedup expected) |
| v2.3 calibration 24-hand legacy (`review/calibration_situations.json` + 4 mirror/batch files) | 21 unique |
| v2.3 anchor extension (4 `GTO_REVERSAL_HANDS` new + 5 `GROUP_D_REVERSAL_HANDS`) | 9 |

Verification:
- Post-sample overlap with Stage 6 holdout: **0**
- Post-sample overlap with v2.3 calibration legacy: **0**
- Post-sample overlap with v2.3 anchor extension: **0**
- Within-pilot unique fingerprints: **100**

Fingerprint method: `(sorted(hero_cards), sorted(board_cards))` — matches Stage 6 v1.0 spec.

## Hash-lock + determinism

- SHA256 over JSONL bytes recorded in `.lock.json` sidecar
- SEED=20260426 fixed; rerunning script reproduces corpus byte-for-byte

To verify at pilot dispatch time:
```bash
sha256sum data/pilot_corpus_100_hand_2026-04-26.jsonl
# Expected: 492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b
```

## Known limitations (flagged for reviewer)

1. **Single-pool opponent_count limitation:** source pool is 3-way only (`3way_situations_10k.jsonl`), so `opponent_count_bucket` distribution is uniformly 3way=100. Per Stage 4 plan §3 the labelling experiment is primarily 3-way focused; consistent with intent. But the directive's "HU / 3-way / 4-way" stratification dimension cannot be satisfied from this single pool. **Reviewer call:** accept as 3-way pilot OR expand source (would require v1.1 corpus build).

2. **Holdout fingerprint count 49 not 50:** parsing returned 49 unique fingerprints from 50 holdout hands. Likely 1 chromatically-equivalent dup under sorted-card method (per Stage 6 v1.0 reviewer flag). Empirically zero-match holds for pilot 100. If reviewer wants tighter, suit-equivalence-class fingerprint extension is a v1.1 hardening item.

## Build C v1.0 conventions for `nit_carryforward` precedent

Per QC PR #38 recommendation. Established v1.0 corpus conventions for any future Build C2 / Stage 5/6 expansion sets:
- Source-pool stratification across 5 dimensions
- Greedy round-robin sampling on least-filled buckets, deterministic via SEED
- Disjointness against Stage 6 holdout hash + v2.3 calibration constants by name (`STANDARD_EXAM_SIZE`, `STANDARD_PASS_THRESHOLD`, `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS`)
- Hash-locked output sidecar with full stratification report
- Within-pilot uniqueness verification
- `force-add` past `.gitignore *.json` for `.lock.json` sidecars (alternative: rename to `.lock.txt` or update `.gitignore`)

## Reviewer dispatch context (next builder action)

Required reviewer characteristics:
- Independent dispatch (different from Builds A/B reviewers); ml-architect or gto-expert persona for stratification adequacy + disjointness audit
- Read-only constraint
- TC-15 multi-expert recommended (per QC PR #38 note + this PR's stratification complexity)
- Cross-checks REQUIRED:
  1. Re-run `python3 scripts/build_pilot_corpus_100_hand.py` — verify byte-identical reproduction (SHA256 match)
  2. Verify `data/pilot_corpus_100_hand_2026-04-26.jsonl` SHA256 = `492154529eb70f07bb5e082a55765c0626b948b72fc48d8aa4a86c424928ef4b`
  3. Verify disjointness against Stage 6 holdout (independent fingerprint extraction from `STAGE6_HOLDOUT_TESTSET_v1_0.md` HOLDOUT_001-050)
  4. Verify disjointness against v2.3 calibration manifest (`review/calibration_situations.json` + 4 mirror/batch files + 9 v2.3 anchor IDs in source pool)
  5. Verify within-pilot uniqueness (100 unique `(sorted(hero), sorted(board))` fingerprints)
  6. Spot-check stratification: any obvious blind spots? (street balance, position balance, texture diversity, hero range placement diversity)
  7. Spot-check 5-10 random hands for poker-quality plausibility (real situations not corrupted records)
  8. TC-23 closure: PRE-DISPATCH rows #2 + #3 closeable after merge
  9. Source design artifacts UNTOUCHED

QC has standing offer for pre-merge audit + TC-15 multi-expert per QC PR #38 closing recommendation.

## Next builder actions

1. Dispatch independent reviewer (general-purpose + ml-architect/gto-expert persona); read-only
2. On reviewer return: write verdict to `review/comms/REVIEW_VERDICT_PR_39_BUILD_C_2026-04-26.md`; commit + push to master; PR comment
3. Stand by for orchestrator merge
4. After Build C merged → surface `BUILDER_BUILDS_ABC_COMPLETE_2026-04-26.md`; orchestrator re-issues pilot dispatch directive (Phase A.1-A7 preflight resumes per `082336d`)

## References

- PR #39: https://github.com/beytell1-sketch/river-rats-v2/pull/39
- Feature commit: `a3b7828`
- Predecessor PRs: PR #35 (Build A SEALED), PR #37 (Build B SEALED)
- Build C kickoff: `MAIN_TERMINAL_PR37_MERGE_ACK_BUILD_C_KICKOFF_2026-04-26.md`
- Builds A/B/C directive: `3f9564e`
- Source pool: `training-data/3way_situations_10k.jsonl`
- Stage 6 holdout: `STAGE6_HOLDOUT_TESTSET_v1_0.md` (hash `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5` over 47652 bytes)
- v2.3 calibration: `river-rats-core/calibration_exam.py` v2.3 (constants `STANDARD_EXAM_SIZE=28`, `STANDARD_PASS_THRESHOLD=23`, `GTO_REVERSAL_HANDS`, `GROUP_D_REVERSAL_HANDS`)
- Pilot orchestration spec v1.0.3: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` at master `c4f29a5`

**Status: PR #39 OPEN. Build C complete. FINAL PRE-DISPATCH gate item — reviewer dispatch next builder action. After Build C seals: PRE-DISPATCH all GREEN; pilot dispatch resumes.**
