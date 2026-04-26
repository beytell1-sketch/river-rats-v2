---
date: 2026-04-26
from: River Rats QC stream
to: Logic builder · Main terminal (orchestrator) · Owner (briefed)
re: PR #39 pre-merge QC audit — Build C (pilot 100-hand stratified corpus + generation script); APPROVE-WITH-FLAGS; 11/13 vectors PASS; 2 MEDIUM findings flagged for reviewer + orchestrator decision before merge
status: FLAG (advisory; pre-merge informational; FLAG-only role — orchestrator + reviewer decide whether MEDIUMs gate)
severity: APPROVE-WITH-FLAGS / 2 MEDIUM (V-X2 partial-fold MW fixture absence; V-C13 feat_dict 45 vs 59-contract gap) + 1 NIT (builder self-flagged)
PR head: a3b78284ba1163ad28edf70eaee37aa34559d6a7
full finding: ~/river-rats-qc/findings/2026-04-26-pr39-pre-merge-build-c.md
---

# QC Pre-Merge Audit — PR #39 (Build C)

## Headline

**APPROVE-WITH-FLAGS.** 11 of 13 vectors PASS. 2 MEDIUM findings flagged for orchestrator + reviewer decision before merge:

- **V-X2 (MEDIUM):** Pilot 100 has zero partial-fold MW fixtures. Source pool itself has 0 such situations (structural). Phase A.5 preflight per QC HIGH-1 (S-A12) requires 5-hand sample. **Where do those 5 fixtures source from?**
- **V-C13 (MEDIUM):** Corpus `feat_dict` has 45 features; Stage 5 retrain v1.0.1 contract = 59 (54 v3.1 + 1 board_adjusted_hrp + 4 v2.4 P1). **Does Phase B labelling re-run feature_extractor.py to expand to 59, or consume 45 directly?**

Both are flag-for-decision rather than spec violations. Builder's PR body already self-flagged 2 known limitations (single-pool opponent_count, holdout dedup); QC adds 2 more.

## Vector results

| Vector | Result | Note |
|--------|--------|------|
| V-C1 corpus size = 100 | ✅ PASS | exact 100 |
| V-C2 street stratification | ✅ PASS | flop=36, turn=30, river=34 |
| V-C3 hero_position | ✅ PASS | 6 positions covered |
| V-C4 opponent_count | ✅ PASS (NIT) | 3way=100; builder self-flagged single-pool limitation |
| V-C5 board_texture | ✅ PASS | 4 textures |
| V-C6 hero_range_placement | ✅ PASS | 4 placements |
| V-C7 disjointness vs Stage 6 holdout | ✅ PASS | 0 overlaps; hash anchor 65cfbf26... matches |
| V-C8 disjointness vs v2.3 calibration manifest | ✅ PASS | 0 overlaps; constants by name |
| V-C9 disjointness vs v2.x training | ✅ PASS | within-pilot 100 unique |
| V-C10 SHA256 hash-lock | ✅ PASS | 492154...4b verifies exact |
| V-C11 TC-23 file existence | ✅ PASS | 3 files at canonical paths |
| V-C12 source provenance | ✅ PASS | source pool + seed + directive ref |
| V-C13 feat_dict schema | ⚠️ MEDIUM | 45 features vs 59-contract |
| V-X2 partial-fold MW fixtures | ⚠️ MEDIUM | zero in pilot; zero in source pool (structural) |
| V-X4 carryforward claim verification | ✅ PASS (N/A) | Build C frames carryforward as forward-looking convention; no closure claims to verify |

## V-X2 detail

```
$ jq '.num_opponents' /tmp/pilot_corpus.jsonl | sort | uniq -c
    100 2

$ jq -r 'select((.prior_actions // [] | tostring) | test("[fF]old")) | .pilot_hand_id' /tmp/pilot_corpus.jsonl | wc -l
0

$ jq -r 'select((.prior_actions // [] | tostring) | test("[fF]old")) | .situation_id' training-data/3way_situations_10k.jsonl | wc -l
0
```

Source pool `3way_situations_10k.jsonl` is "live 3-way" only — no partial-fold MW situations available to sample from. Pilot 100 corpus inherits this structural property.

Per Phase A.5 spec (sealed in v1.0.3 per QC HIGH-1 / S-A12 close): "Test 5-hand sample of partial-fold MW fixtures (3-way+ with at least one folded opponent). If any fixture selects a folded opponent: HALT Phase A."

Question: where do the 5 partial-fold MW fixtures source from for Phase A.5?
- (a) Pilot 100 — fails (0 such fixtures); HIGH-class blocker if so
- (b) Stage 6 holdout — possible
- (c) v2.3 calibration manifest — possible
- (d) Synthetic test fixtures — possible
- (e) Separate fixture file — possible

If (a): corpus needs re-build with partial-fold MW situations OR source pool expansion. If (b)-(e): informational; document fixture source in spec.

## V-C13 detail

`feat_dict` length = 45 features. Stage 5 retrain v1.0.1 + Build B reviewer (PR #37 reviewer verdict) confirmed 59-feature contract: `gto_model.py FEATURE_COLUMNS length 55 + 4 v2.4 P1 blockers = 59`. Pilot corpus is ~14 features short.

Possible interpretations (need clarification from builder/orchestrator):
1. Labellers re-run `feature_extractor.py` at Phase B extraction → covers gap → no issue
2. Labellers consume `feat_dict` directly → real gap → corpus regen needed
3. Labellers receive raw situation + extract features at prompt-render → no issue

## Multi-expert verdict

SOLO + concrete-finding-driven. Pre-emptive scoping vectors + concrete jq queries surfaced the 2 MEDIUMs without need for multi-expert dispatch. Multi-expert deferred — concrete findings already surface the design questions for orchestrator.

## Recommendations

### To orchestrator's dispatched reviewer
- **APPROVE merge** if 2 MEDIUMs resolve as informational (V-X2 sources from non-pilot fixtures; V-C13 has Phase B re-extraction).
- **REJECT or hold** if either MEDIUM resolves as spec violation requiring corpus regen.

### Post-merge (assuming MEDIUMs informational)
- PRE-DISPATCH rows #2 + #3 RED → GREEN
- All 4 RED rows (#2, #3, #5, #6) now GREEN
- Pilot dispatch resumes; Phase A.1-A.7 preflight runs
- QC resumes Layer 3 pilot-runtime watch per `QC_PILOT_RUNTIME_WATCH_2026-04-26.md`

### Process learning
- For future corpus-class builds: pre-emptive scoping should include explicit verification of each fix-surface dependency (V-X2 surfaced a Phase A.5 fixture-source question not called out in build directive)
- Build B divergence learning (V-X4) reinforced: body-residual sweep is a complementary check; for Build C this is partly covered by source-pool root-cause tracing on V-X2

## Reference

- Full QC finding: `~/river-rats-qc/findings/2026-04-26-pr39-pre-merge-build-c.md`
- PR #39: https://github.com/beytell1-sketch/river-rats-v2/pull/39
- Build A audit: `~/river-rats-qc/findings/2026-04-26-pr35-pre-merge-build-a.md`
- Build B audit + divergence learning: `~/river-rats-qc/findings/2026-04-26-pr37-pre-merge-build-b.md` + V-X4 curative
- Stage 6 holdout hash: `65cfbf26ad3c6b228a3462574b86c33be41397258519ffd35b1cc08037a4cba5`
- Phase A.5 spec: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3
- 59-feature contract: `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4
- HIGH-1 fix-surface (S-A12): closed via PR #31 (Task 5 v1.0.3)

**Status: APPROVE-WITH-FLAGS. 2 MEDIUMs need orchestrator + reviewer + (potentially) owner decision before merge.**
