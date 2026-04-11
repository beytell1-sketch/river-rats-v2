---
date: 2026-04-11
from: Main terminal (orchestrator)
to: Owner (Rupert)
re: Audit investigation findings — original audit had wrong picture, git state is the real blocker
status: BLOCKING — needs owner decision before any further work
priority: READ FIRST before any of: cleanup, B4_03 fix, v2.2 retrain
---

## Headline

**The original AUDIT_PROJECT_STATE_2026-04-11.md was built on a partial read.** The earlier blueprint-audit agent grepped only the first ~50 lines of `feature_extractor.py` and reported the compute functions as "missing". They are not missing — they exist at `feature_extractor.py:1430` (`compute_flush_draw_rank`) and `feature_extractor.py:1482` (`compute_hero_range_percentile`). Similarly the file-status-audit agent reported "drift" between `review/` and `river-rats-core/` without checking git state.

The **actual** state of the repo is much more surprising, and it changes the recommended course of action.

## Real state

### Git state

Branch: `master`
Last commit: `8254932 Add 3 new features (flush_block_pct, overcard_outs, improvement_probability)` — features 46-48

**Working tree:**
- **24 files modified** in river-rats-core/ + design/ + knowledge/
- **1148 insertions / 235 deletions** uncommitted
- **~200 untracked files** across review/, review/comms/, training-data/, research/, docs/, results/

### Specifically, these are all UNCOMMITTED

| Change | Files | Impact |
|--------|-------|--------|
| **KB v1.3 cutover** | `knowledge/three_way_gto.md` (+426 lines) | The cutover we just "shipped" is in working tree, not committed |
| **Features 49-52 implementation** | `feature_keys.py`, `feature_extractor.py`, `gto_model.py`, `situation_factory.py` | BLUEPRINT_FEATURES_V3.1 is actually IMPLEMENTED in working tree. 53-feature model surface live in code, but never committed. |
| **Feature 53 (is_preflop_aggressor)** | Same files | Also implemented in working tree, uncommitted |
| **BP2 validator** | `situation_factory.py` (+108 lines) | `validate_action_sequence()` function added |
| **Multiway/sizing/poker_game changes** | `multiway_adjuster.py` (+100), `poker_game.py` (+73), `sizing_oracle.py` (+37) | Unknown scope — needs inspection |
| **Coaching module** | `coaching/feature_extractor.py`, `coaching/gto_model.py`, `coaching/sizing_oracle.py` | Unknown scope |
| **Tests** | 7 test files modified, ~15 new test files untracked | Some work tested, some not |
| **train_model.py** | +191 lines | Training pipeline changes |
| **Review/comms folder** | Entire `review/comms/` directory untracked | Every memo we've been writing is untracked |
| **Training data** | ~15 CSV/JSONL files in `training-data/` untracked | Including `train_3way_v2.1_clean.csv` (production training data) |
| **Research docs** | 9 files in `research/` untracked | 50+ source deep research |
| **Docs** | `docs/MASTER_PLAN (1).md`, `PROGRESSIVE_MODEL_CHAIN.md`, `PROCESS_GUIDE.md`'s partner docs untracked |

### What this means

**The `river-rats-core/ is sacred` rule in CLAUDE.md is not being enforced.** CLAUDE.md says: *"Only reviewed, approved, passing files enter river-rats-core/. After every approved change, update river-rats-core/ before starting the next task. This folder is always deployable."*

Reality: `river-rats-core/` has 1148 lines of uncommitted changes mixing multiple distinct changesets (features, KB, tests, multiway, coaching, training pipeline). It is not deployable in the sense of "git checkout master and run it" — the committed master is at feature 48, not feature 53.

## Correcting the audit's findings

| Original audit claim | Reality |
|---|---|
| BLUEPRINT_FEATURES_V3.1 = PARTIAL (functions missing) | **COMPLETE in working tree** — all 4 compute functions exist, wired into Step 13, listed in gto_model.py FEATURE_COLUMNS (N_FEATURES=53), but UNCOMMITTED |
| 5 DRIFTED files in review/ vs core/ | **NEITHER is ground truth.** review/ files are untracked working copies; core/ files are uncommitted modifications. Both diverge from committed master. |
| B4_03 = OPEN 1-line fix | **Already fixed in canonical sources** (`BOARD_ALLOCATION_V4_BET.md:127`, `generate_factory_batch4.py:121-124`) — both of which are UNTRACKED. The gate check memo flagged a stale REVIEW memo, not a live failure. |
| KB v1.3 = cutover complete | **Uncommitted** — `knowledge/three_way_gto.md` is modified (+426 lines) in working tree, never committed |
| Meta-review steps 4-7 all ✓ | Steps 4-7 are correct IN WORKING TREE, but none of them are in git history |

## Why this is a blocker

1. **Cannot "iterate v9-3way to ceiling"** when the feature surface isn't committed. v2.2 retrain decisions depend on knowing the authoritative feature set.

2. **Cannot clean up review/ files** when those files are untracked — deletion loses work with no git history to recover from.

3. **Cannot promote anything from review/ to core/** when core/ itself isn't at a clean committed state.

4. **The process guide's Section 6 training team protocol** assumes approved code lives in core/. That assumption is currently false.

5. **The earlier audit recommended cleanup and retrain** based on a picture that didn't check git state. Acting on those recommendations (especially the deletions) would have been destructive.

## Recommended course of action

This changes the sequence. New priority order:

### Phase 0 — Commit discipline (NEW, BLOCKING)

Before any other work, resolve the git state. Recommended split into logical commits:

1. **Commit 1: KB v1.3 cutover** — just `knowledge/three_way_gto.md`. This is self-contained, reviewed, spot-checked, approved.
2. **Commit 2: Features 49-53 surface** — `feature_keys.py`, `feature_extractor.py`, `gto_model.py`, `situation_factory.py` (validator), associated test files. All or nothing.
3. **Commit 3: Training pipeline updates** — `train_model.py`, `train_sizing_model.py`, `reference_evaluator.py`.
4. **Commit 4: Multiway/sizing/poker_game** — needs inspection first. Possibly split further.
5. **Commit 5: Coaching module** — needs inspection first.
6. **Commit 6: Add review/comms folder** — track the memo workflow as a first-class artifact, OR add to .gitignore if they're meant to be ephemeral.
7. **Commit 7: Training data snapshot** — add training-data/*.csv for reproducibility.
8. **Commit 8: Research + docs** — research/, docs/, MASTER_PLAN, PROGRESSIVE_MODEL_CHAIN, PROCESS_GUIDE companion docs.

Each commit requires a pass of: (a) read the diff, (b) run the relevant tests if any, (c) write a commit message, (d) commit.

Per memory `feedback_commit_autonomy.md`, I have autonomy to commit in local repos. I will NOT commit blindly — I will inspect each logical unit first, run tests where relevant, and only commit what validates. I will report back with a commit log.

### Phase 1 — Re-audit post-commit

Once working tree is clean, re-run the plan/blueprint/comms/file-status audit against the committed state. This will produce the correct picture.

### Phase 2 — Then proceed with original sequence

1. B4_03 verification (probably already resolved)
2. v9-3way-v2.2 training decomposition
3. etc.

## What I need from you

**One decision only:** approve Phase 0 (commit the working tree in logical units, I inspect each before committing) — OR direct differently.

Specifically:
- If you want me to commit autonomously per `feedback_commit_autonomy.md`: say "go".
- If you want to review each commit individually before I execute: say "one at a time".
- If there's work in the tree that should NOT be committed (e.g. experiments to discard): tell me which paths.
- If you want `review/` and `review/comms/` in `.gitignore` instead of tracked: say so.

## Task list updated

| # | Task | Status |
|---|------|--------|
| 1 | Investigate BLUEPRINT_FEATURES_V3.1 | COMPLETED — not orphan, implemented in working tree |
| 2 | Fix B4_03 action history | IN_PROGRESS — canonical fix already in working tree (untracked); gate check memo stale |
| 3 | Clean up DRIFTED review/ files | BLOCKED — original drift analysis was wrong; deletion would lose untracked work |
| 4 | Build facing-bet test set | PENDING — blocked on #1 (now: blocked on #7) |
| 5 | Phase B Preflop Range Fix | PENDING |
| 6 | Train v9-3way-v2.2 | PENDING — blocked on #1, #4, #5 (now: blocked on #7) |
| **7** | **Resolve uncommitted git state** | **NEW, BLOCKS everything** |

---

**End. Awaiting decision on Phase 0 commit approach.**
