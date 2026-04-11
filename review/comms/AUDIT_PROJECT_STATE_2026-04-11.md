---
date: 2026-04-11
from: Main terminal (orchestrator)
to: Owner (Rupert)
re: Consolidated project state audit — plans, blueprints, comms, file status
status: FOR REVIEW
team: 4 parallel Explore agents (plan-audit, blueprint-audit, comms-audit, file-status-audit)
---

## Executive Summary

**Good news:**
- KB v1.3 cutover (2026-04-11) is clean. All 4 meta-review steps verified complete.
- Only **1 open action item** in comms: B4_03 flop action history fix (1-line correction).
- All scheduled TODOs (ablation, calibration, feature scoping) are properly logged.

**Needs attention:**
- **5 DRIFTED files** in `review/` where `river-rats-core/` has moved ahead. These are stale staging copies, not production risks — but they are misleading and should be cleaned up per Process Guide ("review/ files move to core/ after approval").
- **BLUEPRINT_FEATURES_V3.1** is only PARTIAL — feature constants (hero_range_percentile, has_showdown_value, villain_fold_equity_estimate) exist in `feature_keys.py`, but the `compute_*` functions are missing from `feature_extractor.py`. Either the blueprint was abandoned or implementation stalled mid-flight.
- **~15 files awaiting promotion** from review/ to core/ (factory batch 2/3/4 generators, deterministic_labeller, range source files, board allocation specs).
- **Stale staging cleanup:** PLAN_V3_*.md variants (4 of them), SPEC_KNOWLEDGE_BASE_V1.2.md, KB_V1.3_REQUIREMENTS.md all obsolete post-cutover.

**Decision needed:**
Before moving to "iterate v9-3way to ceiling," we should decide whether to (a) close the B4_03 fix and clean up review/ drift first, (b) resolve the BLUEPRINT_FEATURES_V3.1 incomplete state, or (c) proceed with the next training iteration and defer cleanup. These three tracks interact — see Section 6.

---

## 1. Plans

### Driving plan
**`docs/MASTER_PLAN (1).md`** (2026-04-06) — Progressive model chain: v8 (HU frozen) → v9-3way (shipped 82.5% solver-corrected) → v9-4way → v9-5way. Phase A = iterate v9-3way to ceiling BEFORE starting v9-4way.

### Supporting plans

| Plan | Date | Status | Summary |
|------|------|--------|---------|
| `review/PLAN_3WAY_TRAINING_PIPELINE.md` | 04-06 | **EXECUTED** | 4-step pipeline shipped v9-3way-v2.1 |
| `review/PLAN_PREFLOP_RANGE_FIX.md` | 04-06 | **IN-PROGRESS** | Phase B parallel — replace RFI/3BET/CALL dicts with solver-backed hand lists to unblock yield (0.51% → target 3-5%). Not yet executed. |
| `review/PLAN_V3_DATA_INTEGRITY_FINAL.md` | 04-08 | **IN-PROGRESS** | Phase 0 (RAISE as is_monster) approved; Phase 1 (audit 46 factory boards) and Phase 2 (4 new features + action validator) awaiting decomposition |
| `review/PLAN_FEATURES_45_TO_48.md` | 04-07 | **STALE** | Superseded by Feature 53 plan (04-09) |
| `review/comms/KB_V1.3_EDIT_PLAN.md` | 04-10 | **EXECUTED** | Cutover complete 04-11, spot-check approved |
| `review/comms/CBET_RESEARCH_AND_FEATURE53_PLAN_2026-04-09.md` | 04-09 | **ACTIVE** | Feature 53 (is_preflop_aggressor) + c-bet research (Phase A-D) before labelling 563 situations. Phase A ready; B-D queued. |
| `review/comms/BET_FACTORY_PLAN_2026-04-09.md` | 04-09 | **PLANNED** | Depends on c-bet research (Phase C BET tree). Blocked. |

### Plan risks
- **Preflop Range Fix (Phase B)** has been "in-progress" since 04-06 with no visible execution. Flagged as stale if not picked up this week.
- **V3 Data Integrity (Phase 1-2)** not yet decomposed into agent teams — violates Process Guide Section 0 phase-transition rule.

---

## 2. Blueprints

Two true architect blueprints (exact insertion points + line numbers) exist. Additional design docs are plans or specs, not blueprints.

| Blueprint | Target(s) | Status | Evidence |
|-----------|-----------|--------|----------|
| `review/comms/KB_V1.3_EDIT_PLAN.md` (04-10) | `knowledge/three_way_gto.md` | **BUILT** ✓ | 19 purge edits applied; F1/F2/F3 fixes approved; cutover complete 04-11 |
| `review/BLUEPRINT_FEATURES_V3.1.md` (undated) | `feature_keys.py`, `feature_extractor.py`, `gto_model.py`, `situation_factory.py` | **PARTIAL** ⚠ | Feature constants (`HERO_RANGE_PERCENTILE`, `HAS_SHOWDOWN_VALUE`, `VILLAIN_FOLD_EQUITY_ESTIMATE`) added at `feature_keys.py:73-75`. `compute_hero_range_percentile` and related functions NOT found in `feature_extractor.py`. Either abandoned or stalled. |

### Open question
**BLUEPRINT_FEATURES_V3.1** — is this plan still active? If so, who owns completing it? If abandoned, the orphan constants in `feature_keys.py` should be removed to avoid misleading future work.

---

## 3. Comms

**91 memos total** in `review/comms/`.

### Meta-review sequence verification (KB v1.3)
All 4 expected post-cutover steps complete:

| Step | Status | Evidence |
|------|--------|----------|
| 4 — Cutover to `knowledge/three_way_gto.md` | ✓ DONE | File dated 04-11 01:25, header says v1.3, staging file deleted |
| 5 — Reply memo to teaching team | ✓ DONE | `LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md` posted 04-11 01:28 |
| 6 — Memory file `feedback_preflop_geometry_vs_postflop_composition.md` | ✓ DONE | Exists with proper frontmatter, indexed in MEMORY.md |
| 7 — Ablation TODO in `feedback_solver_findings.md` | ✓ DONE | Lines 95-101 bookmark for next feature-importance audit |

### Open action items

| Item | Source memo | Priority |
|------|-------------|----------|
| **B4_03 flop action history fix** | `GATE_CHECK_BATCH4_ALLOCATION.md` (04-10 01:44) | OPEN — 1-line correction: remove `(flop, BTN, check)` from history. BTN cannot act before CO (hero) decides. Single source-line edit + BP2 structural note. |
| `villain_range_capped` ablation | `LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md` | SCHEDULED — next feature-importance audit |
| L3 bucket calibration (≥60/≥40/≥20/<20) | `LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md` | SCHEDULED — same audit |
| Action history feature scoping | `SCOPING_ACTION_HISTORY_FEATURES_2026-04-10.md` | PARKED — route through ml-architect before feature code |

### Orphaned references
Only one expected orphan: `review/three_way_gto_v1.3.md` referenced in multiple memos but file is gone (consumed by cutover — CORRECT per Process Guide folder protocol). No dead references otherwise.

---

## 4. File status — review/ vs river-rats-core/

### DRIFTED files (review/ behind core/) — CLEANUP CANDIDATES

Not production risks (core is authoritative), but misleading. These were approved and promoted but the review/ copy was not deleted.

| File | Drift |
|------|-------|
| `gto_model.py` | Core has v9 (53 features: +flush_block, +overcard_outs, +improvement_prob, +range_pct, +showdown_val, +fold_equity, +flush_rank, +is_preflop_agg); review at 45-feature baseline |
| `export_3way_training.py` | Core uses 5-class labels directly; review maps to 3-class |
| `game_state_bridge.py` | Core documents 45 features; review documents 38 |
| `generate_3way_situations.py` | Core removed `single_position` param; review still has it |
| `self_play.py` | Core has bet/raise routing based on `game.current_bet`; review returns raw action |

### PROMOTED clean (byte-identical)
`convergence_checker.py`, `deal_generator.py`, `decision_comparator.py`, `hand_logger.py`, `observer.py`, `personality_profiles.py`, `preflop_engine.py`, `variant_evolver.py` — 8 files.

### AWAITING PROMOTION (~15 files)

| File | Size | Date | Notes |
|------|------|------|-------|
| `generate_factory_batch2.py` | 51K | 04-09 | Factory generator |
| `generate_factory_batch3.py` | 56K | 04-09 | Factory generator |
| `generate_factory_batch4.py` | 64K | 04-10 | Factory generator |
| `deterministic_labeller.py` | 31K | 04-06 | Labelling utility |
| `new_range_data.py` | 17K | 04-06 | Range data generator |
| `call_source.py`, `rfi_source.py`, `three_bet_source.py` | ~20K | 04-06 | Range source generators |
| `BOARD_ALLOCATION_V4_BET.md` | 80K | 04-10 | Board allocation spec |
| `FACTORY_DESIGN_BET_CONTEXTS.md` | 50K | 04-09 | Bet factory design |

None of these have explicit approval memos — they may be works-in-progress, not ready-to-ship. Owner decision needed.

### STALE STAGING — cleanup candidates
- `PLAN_V3_DATA_INTEGRITY_*.md` (4 variants) — KB v1.3 cutover complete
- `SPEC_KNOWLEDGE_BASE_V1.2.md` — superseded by v1.3
- `KB_V1.3_REQUIREMENTS.md` — completed task
- `all_557_situations.jsonl`, `calibration_exam_v3_results.txt` — one-off artifacts

---

## 5. Team assignments that produced this audit

| Agent | Brief | Status |
|-------|-------|--------|
| Plan-audit (Explore) | Inventory docs/ and review/ for PLAN documents, status each | COMPLETE |
| Blueprint-audit (Explore) | Find architect blueprints, verify implementation against source | COMPLETE |
| Comms-audit (Explore) | Scan review/comms/, identify open threads, verify meta-review sequence | COMPLETE |
| File-status-audit (Explore) | Diff review/ vs river-rats-core/, flag drift | COMPLETE |

All 4 agents ran in parallel, read-only, self-contained briefs per Process Guide Section 1.1.

---

## 6. Open questions for owner decision

Per Process Guide Section 4.1 ("Present for review, don't decide"), these are for you:

**Q1 — What's the next training priority?**
Memory says "iterate v9-3way to ceiling before v9-4way." The 5 true remaining reference failures are: MW-17 (under-calling), MW-25 (passive), MW-40 (passive), MW-45 (under-raising), MW-47 (under-raising, shared blind spot). Options:
- (a) Train v9-3way-v2.2 with the KB v1.3 corrections + solver findings applied to a new labelling round
- (b) Build the facing-bet test set (30-50 hands) first to get a second evaluation axis before retraining
- (c) Spec + build the blocker feature first, then retrain

**Q2 — Clean up DRIFTED review/ files now or defer?**
Five files in review/ are stale copies behind core/. Cleanup is mechanical (delete stale copies). Not urgent but satisfies Process Guide rule 6 ("river-rats-core/ is sacred, review/ files move after approval"). Do it now or batch with next review folder cleanup?

**Q3 — BLUEPRINT_FEATURES_V3.1 status?**
Feature constants exist in `feature_keys.py` but `compute_*` functions missing. Three options:
- (a) Complete the blueprint — spawn ml-architect to reconfirm design, architect to rewrite insertion points against current source, programmer to implement
- (b) Abandon and remove the orphan constants from `feature_keys.py`
- (c) Leave as-is (not recommended — misleading for future work)

**Q4 — B4_03 action history fix — when?**
1-line correction blocking Batch 4 factory completion. Who owns: single programmer agent or architect blueprint first?

**Q5 — Phase B (Preflop Range Fix) — pick up now or defer?**
Has been "in-progress" since 04-06 with no execution. Blocks 3-way yield improvement. If deferred, flag as STALE.

---

## Recommendation (optional, owner-overridable)

If I were to pick one path:

1. Close **B4_03 fix** (programmer, 15 min) — trivial, unblocks Batch 4
2. Clean up **DRIFTED review/ files** (programmer, 10 min) — mechanical, satisfies Process Guide
3. Resolve **BLUEPRINT_FEATURES_V3.1** by spawning ml-architect to determine: is it still wanted? If yes, complete blueprint + implement. If no, remove orphan constants.
4. Then decompose **v9-3way-v2.2 retrain** into the Section 6 training team (ml-architect → architect → programmer → reviewer), applying KB v1.3 corrections + solver findings to a fresh labelling round

That sequence front-loads cleanup (low risk, clears decks), then enters the next training iteration cleanly.

But Q1 is yours — if you want to test before retraining (facing-bet test set, or blocker feature first), that changes step 4.

---

**End of audit. Please review Section 6 open questions and direct.**
