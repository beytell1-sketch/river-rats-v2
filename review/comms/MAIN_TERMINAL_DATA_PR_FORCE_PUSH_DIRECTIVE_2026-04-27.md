---
date: 2026-04-27
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · gto-expert · ml-architect · QC stream · Owner
re: Force-push PR #70 with 494-hand corpus + lock + final report; round 3 reviews dispatch when PR refreshed
status: DIRECTIVE — data-only PR force-push; round 3 review chain follows
---

# Data PR #70 force-push directive

## Context

PR #87 Phase 8 implementation merged at master `e0d6b39`. 494-hand corpus is FINAL per round 9 synthesis (no Phase 9). Builder ran C2 successfully during Phase 8 verification; data files exist on builder's local. Now they need to be on PR #70.

Per memory `feedback_listen_to_orchestrator_always.md`: orchestrator-named-author = sufficient. AUTHORING mode.

## What to do

### Step 1 — pull master + regenerate (or use existing local data)

```
cd ~/river-rats-v2
git pull --ff-only origin master
git checkout programmer/corpus-revision-execution-2026-04-27
git rebase origin/master  # or merge master if rebase has conflicts
```

If your local `data/corpus_revision_500_hand_2026-04-27.jsonl` is from the Phase 8 verification run (494 records, all gates passed), you can use it as-is. Otherwise, re-run the C2 pipeline:

```
# E1 (re-extract pilot 100)
python3 scripts/reextract_pilot_100_features.py \
  --input data/pilot_corpus_100_hand_2026-04-26.jsonl \
  --output data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --bb-chip-size 10

# E2-B (Mode B factory pool — uses Phase 6+8 expanded modules)
python3 river-rats-core/generate_corpus_revision_pool.py --mode b \
  --output data/corpus_revision_pool_mode_b_2026-04-27.jsonl

# E2-A (Mode A self-play — use existing or regenerate via workaround driver)
python3 scripts/run_mode_a_pool_with_positions.py \
  --positions CO,BTN,BB --deals 1000 --seed 20260427 \
  --output data/corpus_revision_pool_mode_a_2026-04-27.jsonl

# Combine for C2
cat data/corpus_revision_pool_mode_a_2026-04-27.jsonl \
    data/corpus_revision_pool_mode_b_2026-04-27.jsonl \
    > data/corpus_revision_pool_combined_2026-04-27.jsonl

# C2 (assembly)
python3 scripts/build_corpus_revision_500_hand.py \
  --pool data/corpus_revision_pool_combined_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 --seed 20260427 \
  --output data/corpus_revision_500_hand_2026-04-27.jsonl \
  --lock-output data/corpus_revision_500_hand_2026-04-27.lock
```

### Step 2 — write final report

`review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_FINAL_2026-04-27.md`. Cover:
- Corpus total: 494 hands
- Per-category fill (all 12 cats with status FULL/UNDER and counts)
- File SHA256s (pilot v2, Mode A pool, Mode B pool, combined pool, 500-hand corpus, lock)
- Wall-time + cost
- Reference round 9 synthesis decision (494 FINAL, no Phase 9)

### Step 3 — force-push PR #70 branch

```
# Stage data files + report
git add data/pilot_corpus_100_hand_2026-04-26_v2.jsonl
git add data/pilot_corpus_100_hand_2026-04-26.lock.json
git add data/corpus_revision_pool_mode_a_2026-04-27.jsonl
git add data/corpus_revision_pool_mode_b_2026-04-27.jsonl
git add data/corpus_revision_pool_combined_2026-04-27.jsonl
git add data/corpus_revision_500_hand_2026-04-27.jsonl
git add data/corpus_revision_500_hand_2026-04-27.lock
git add review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_FINAL_2026-04-27.md
git add scripts/run_mode_a_pool_with_positions.py  # if this isn't already on master

git commit -m "Builder final: 494-hand corpus + lock + Phase 8 final report"
git push --force-with-lease origin programmer/corpus-revision-execution-2026-04-27
```

### Step 4 — update PR #70

```
gh pr ready 70  # take out of DRAFT
gh pr edit 70 --title "Builder: 494-hand corpus revision (FINAL — 99% of 500 target; structural overlap accepted per round 9)"
gh pr edit 70 --body-file review/comms/PROGRAMMER_REPORT_BUILD_EXECUTE_FINAL_2026-04-27.md
```

(Or update via gh comment with summary; orchestrator reviews body/comment.)

## Verification gates (re-confirm before push)

Same gates as Phase 8 directive Gate 4:
- Total: 494 (acceptable per round 9 synthesis)
- All Phase A categories per the Phase 8 final report distribution
- Lock file present with SHA256

If C2 re-run produces different counts than Phase 8's reported 494 (e.g., due to seed determinism), report the actual count in step 2's final report.

## Round 3 review chain (when PR #70 refreshed)

- **gto-expert**: spot-check 10-15 records across families for poker realism (action histories valid, board/hero combinations sensible, opener positions correct)
- **ml-architect**: feature-distribution checks (SPR histogram, IS_PFA distribution, all 59 keys per record, no NaNs except where expected)
- **QC**: paired V-Implementation-Spec-Match (lock file fields populated correctly per `_verify_corpus`'s 8 attestation gates) + V-Integration-Trace (re-run sample of 5 records through `extract_all_features` and confirm output matches stored `feat_dict` bit-for-bit per TC-26 pattern)

Per memory `feedback_qc_required_before_approval.md`: QC must weigh in before merge.

## After PR #70 merges

Mass labelling kickoff directive (separate cycle). The labelling pipeline:
- 5 sonnet labellers per hand × 494 hands = 2470 labels (or revised plan per current Phase B Held status)
- v3.2 protocol (Rule 11 paired-board CHECK + KB §1.7 OVERRIDE villain_air_pct ≥ 0.20)
- Output to `data/corpus_revision_500_hand_labels_2026-04-27.jsonl`
- Reviewer gates per established pilot pattern

## What is NOT in scope for this directive

- Code changes (Phase 8 is in production)
- New Phase X cycle (494 is final)
- v3.2 protocol changes
- Tier 1 calibration manifest (parallel separate PR)

## References

- Master HEAD: `e0d6b39`
- Round 9 synthesis (master `114961f`): `MAIN_TERMINAL_PR87_PHASE8_SYNTHESIS_2026-04-27.md`
- PR #87 (merged): `e0d6b39`
- Phase 8 directive (master `6fc410e`): for verification gate reference
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_quality_default_no_ask.md`, `feedback_qc_required_before_approval.md`, `feedback_shared_tree_commit_hygiene.md`

**Status: DATA PR FORCE-PUSH DIRECTIVE OPEN. Builder produces 494-hand corpus + final report; force-pushes PR #70; round 3 review chain dispatches. After merge: mass labelling kickoff.**
