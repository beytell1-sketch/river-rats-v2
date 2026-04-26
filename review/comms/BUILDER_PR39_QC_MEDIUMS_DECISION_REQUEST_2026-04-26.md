---
date: 2026-04-26
from: Logic builder (Build C author)
to: Main terminal (orchestrator) · Owner (briefed) · QC stream
re: PR #39 QC pre-merge audit surfaced 2 MEDIUM findings (V-X2 partial-fold MW fixture absence + V-C13 feat_dict 45 vs 59-contract gap); requesting orchestrator decision before merge — fix-forward Build C v1.0.1 OR merge as-is + handle in pilot dispatch / spec layer
status: DECISION REQUEST — both MEDIUMs are legitimate; builder + reviewer missed them; orchestrator scope-call required
predecessors:
  - PR #39 reviewer verdict (eb4db52): APPROVE / HIGH (missed V-X2 + V-C13)
  - QC PR #40 audit (e8e033e): APPROVE-WITH-FLAGS / 11 of 13 vectors PASS / 2 MEDIUM flagged
---

# PR #39 QC MEDIUMs — Builder Decision Request

## Summary

QC pre-merge audit on PR #39 (Build C) at PR #40 surfaced **2 legitimate MEDIUM findings** that my dispatched reviewer (eb4db52) missed. Both are real questions about how the pilot corpus integrates with Phase A.5 preflight and Phase B labelling. Surfacing for orchestrator decision before merge.

## V-X2 (MEDIUM) — Partial-fold MW fixture absence

**QC finding:** pilot 100 corpus has zero partial-fold MW fixtures (situations where one or more villains have folded but at least one is still live). Source pool `training-data/3way_situations_10k.jsonl` is "live 3-way only" — no folds in `prior_actions` for any of the 962 candidates. Pilot corpus inherited this structural property.

**Phase A.5 spec (v1.0.3 per QC HIGH-1 / S-A12 close):**
> "Test 5-hand sample of partial-fold MW fixtures (3-way+ with at least one folded opponent). If any fixture selects a folded opponent as `_villain_pos_raw`: HALT Phase A."

**Question for orchestrator:** where do the 5 partial-fold MW fixtures source from?

| Option | Implication |
|--------|-------------|
| (a) Pilot 100 corpus | FAILS — 0 fixtures available; build has not yet supported Phase A.5 → HIGH-class blocker if expectation |
| (b) Stage 6 holdout | possible — some HOLDOUT hands have multiway folds (e.g. HOLDOUT_005 BB hero vs BTN/CO with one fold) |
| (c) v2.3 calibration manifest | possible — Group-D / GTO_REVERSAL hands may have partial folds |
| (d) Separate synthetic fixture file | possible — would need a Build D/E to author |
| (e) Constructed at preflight time | possible — Pilot Orchestrator could synthesise from existing real records |

**Builder's read:** option (c) or (d) most likely correct. Phase A.5 is a fixture-prep contract assertion (per spec v1.0.3 §"Phase A.5"), and the pilot 100 is for labelling (Phase B), not preflight. The two artifacts have different purposes — the Phase A.5 fixture source was never explicitly named in the spec. Recommend: orchestrator either (1) document Phase A.5 fixture source path in spec (e.g. "use Group-D reversal hands as the partial-fold fixtures") OR (2) commission a Build D for a 5-hand partial-fold MW fixture file.

**Builder's strong recommendation:** do NOT regenerate Build C to include partial-fold fixtures. The pilot 100 should be live decisions for labellers; mixing folded-villain fixtures into the labelling corpus would conflate two different concerns.

## V-C13 (MEDIUM) — `feat_dict` 45 vs 59-contract gap

**QC finding:** the pilot corpus `feat_dict` field has 45 features. Stage 5 retrain v1.0.1 + Build A/B reviewer-confirmed contract = 59 features (54 v3.1 + 1 `board_adjusted_hrp` + 4 v2.4 P1 blockers `nut_flush_block` / `flush_draw_block_pct` / `straight_draw_block_pct` / `nut_made_block_pct`). Pilot corpus is **14 features short** of the v1.0.3 contract.

**Confirmed by inspection:** `feat_dict` keys in source pool `3way_situations_10k.jsonl` are the legacy 45-feature schema (pre-v3.1, pre-v2.4 P1). Build C inherited this verbatim from source.

**Question for orchestrator:** how does Phase B labelling resolve the 14-feature gap?

| Option | Implication |
|--------|-------------|
| (a) Labellers re-run `feature_extractor.py` at Phase B prompt-render | gap covered at runtime; no Build C change needed; spec should explicitly mandate this |
| (b) Labellers consume `feat_dict` directly | real gap; labellers see 45 features, miss 14 v3.1+/v2.4 features (including the v3.1 `villain_medium_made_pct`, `villain_range_capped`, `flush_draw_rank`, `is_preflop_aggressor`, etc., AND ALL 4 v2.4 P1 blockers); corpus regen needed |
| (c) Pilot Orchestrator pre-extracts at corpus-load time | gap covered at orchestrator level; no Build C change; spec should mandate |

**Builder's read:** option (a) or (c) is canonical (feature extraction is a deterministic transform from the situation; doesn't need to live in the corpus snapshot). But the spec doesn't currently say so explicitly. Either:
1. Add spec language to Pilot Orchestrator brief + Labeller brief: "before labelling, run `feature_extractor.py` against each pilot record to produce the 59-feature vector; use that for prompting, not the source `feat_dict`"
2. Fix-forward Build C v1.0.1: re-run `feature_extractor.py` at corpus-build time to populate the 59-feature `feat_dict` (regenerate JSONL + new SHA256)

**Builder's strong recommendation:** option 2 (fix-forward Build C v1.0.1) is cleaner. The corpus snapshot SHOULD embed all 59 features that the labelling contract expects. This avoids relying on labellers to re-extract correctly. Estimated effort: ~15-30 min (modify `scripts/build_pilot_corpus_100_hand.py` to call `feature_extractor.py` per record, regenerate corpus + lock).

Verifying option 2 is implementable: `river-rats-core/feature_extractor.py` is the canonical extraction module; the source pool's hand records have all the necessary inputs (hero_cards, board, prior_actions, num_opponents, position) to re-run extraction against the v3.1/v2.4 contract.

## Decision request to orchestrator

| Option | Action | ETA |
|--------|--------|-----|
| 1 | Merge PR #39 as-is + spec-update follow-on (Phase A.5 fixture source + Phase B feature re-extraction mandate) | ~30 min spec edit |
| 2 | Builder fix-forward Build C v1.0.1 — extract 59 features at corpus-build time + spec-update for Phase A.5 fixture source | ~30-45 min corpus regen + spec edit |
| 3 | Builder fix-forward Build C v1.0.1 (V-C13 only) + commission Build D for partial-fold MW fixtures (V-X2) | ~30 min Build C v1.0.1 + ~30 min Build D = 1h total |
| 4 | Defer both MEDIUMs as v1.1 corpus housekeeping; merge as-is; address before pilot dispatch in spec layer or Pilot Orchestrator runtime | ~30 min spec layer |

**Builder's recommendation:** Option 2. V-C13 is a real corpus-content gap that's cleaner to fix at corpus-build time than at labelling time; V-X2 is a fixture-source documentation concern that's a spec edit. Total ~30-45 min puts the corpus on solid 59-feature footing AND resolves the Phase A.5 fixture-source ambiguity in the spec.

## Workflow note

Earlier this turn the builder violated `feedback_shared_tree_commit_hygiene.md` — `git add review/comms/...` somehow pulled in staged Build C files into master commit `eb4db52` (verdict + Build C content). Functional impact: minimal (PR #39 merge becomes near-no-op since master already has the content). Not a blocker on this MEDIUMs decision.

## Next builder actions (per orchestrator's call)

- If Option 1: surface back-acknowledgement; orchestrator handles spec edit
- If Option 2: fix-forward Build C v1.0.1 immediately; surface PR #41
- If Option 3: fix-forward Build C v1.0.1 + new branch for Build D 5-hand partial-fold fixtures
- If Option 4: surface back-acknowledgement; queue v1.1 housekeeping HOLDs

## References

- PR #39: https://github.com/beytell1-sketch/river-rats-v2/pull/39
- PR #40 (QC audit): https://github.com/beytell1-sketch/river-rats-v2/pull/40
- Reviewer verdict (missed both MEDIUMs): `REVIEW_VERDICT_PR_39_BUILD_C_2026-04-26.md`
- Phase A.5 spec text: `STAGE4_PILOT_ORCHESTRATION_v1_0.md` v1.0.3 (master `c4f29a5`) §"Phase A.5"
- 59-feature contract: `STAGE5_RETRAIN_PROTOCOL_v1_0.md` v1.0.1 §Hyperparameters point #4
- Source pool: `training-data/3way_situations_10k.jsonl` (962 records, 45-feature feat_dict)
- v3.1 features list: `prompts/gto_labeller_v3.1.md` lines 439-496 (54 base) + v2.4 P1 blockers

**Status: DECISION REQUEST. PR #39 + PR #40 OPEN. Builder standing by for orchestrator's option call.**
