---
date: 2026-05-21
from: BUILDER (river-rats-v2 / `builder-phase2-e-full-batch8-2026-05-12`)
to: Orchestrator
re: ACK MAIN_TERMINAL — fire now A0.3a (batch-008 labelling resume)
start_timestamp_utc: 2026-05-21T21:34:36Z
---

# Builder ACK — A0.3a batch-008 labelling fire-now

Acknowledging `review/comms/MAIN_TERMINAL_BATCH008_RESUME_FIRE_NOW_2026-05-21.md` (on `origin/orch/fire-now-batch008-a0-3a-2026-05-21`). Spawning 13 parallel labelling subagents now.

## Pre-flight verification (4 steps complete)

1. **Rebase to current master**: HEAD advanced `c4021cd` → `9e749b3` (A0.1 + A0.2 + A0.1.1 now in base). Working tree clean post-rebase; 11 untracked artifacts preserved.
2. **Untracked artifact counts match expected state** (after stripping 1 trailing malformed/blank line each on L2 and L3 — clean state pre-dispatch):
   - L1: 50 valid records (4WF-RANGE-AS-356 → 405)
   - L2: 36 valid records (356 → 391)
   - L3: 11 valid records (356 → 366)
   - L4: 10 valid records (356 → 365)
   - L5: 25 valid records (356 → 380)
3. **Brief is v1**: `git diff origin/master -- data/4way_labeller_brief.md` returned 0 lines. Brief stays v1 through batch-008 per blueprint v2 §4. A0.3c brief patch lands as final commit on A0.3 branch.
4. **Prior labeller context sampled**: tail label per L2/L3/L4/L5 read; persona reference paths passed to each subagent.

## Chunk dispatch plan (13 subagents, ≤10 hands each per PROCESS_GUIDE §1.1)

| Chunk | Labeller | Spots (in batch_008_50hand.jsonl) | Count |
|---|---|---|---|
| 2a | L2 | 4WF-RANGE-AS-392 → 401 | 10 |
| 2b | L2 | 402 → 405 | 4 |
| 3a | L3 | 367 → 376 | 10 |
| 3b | L3 | 377 → 386 | 10 |
| 3c | L3 | 387 → 396 | 10 |
| 3d | L3 | 397 → 405 | 9 |
| 4a | L4 | 366 → 375 | 10 |
| 4b | L4 | 376 → 385 | 10 |
| 4c | L4 | 386 → 395 | 10 |
| 4d | L4 | 396 → 405 | 10 |
| 5a | L5 | 381 → 390 | 10 |
| 5b | L5 | 391 → 400 | 10 |
| 5c | L5 | 401 → 405 | 5 |
| **TOTAL** | **L2-L5** | | **118** |

Per-chunk inputs staged at `/tmp/batch_008_chunks/input_L{N}_{label}.jsonl`. Each subagent writes to `/tmp/batch_008_chunks/output_L{N}_{label}.jsonl`. Builder concatenates per-labeller results into the existing `batch_008_raw_labels_labeller_{N}.jsonl` files post-dispatch.

## Schema discipline carried to subagents

- v1 brief (no split-schema yet); `predicted_sizing_pct` single int (BET=% of pot; RAISE=bb amount; else null)
- `labeller_id` as integer (2/3/4/5) per existing convention
- Solver-aligned sizing per `feedback_solver_aligned_sizing.md` (flop 25%/66%, turn 33%/75%, river 33%/75%/150%)
- Terminology lock per `feedback_terminology_raise_vs_bet.md`
- Bucket-first labelling per `feedback_bucket_first_labelling.md`
- 0 illegal-action votes (FL5); 0 templated rationales (FL4)

## Post-labelling sequence (queued, not yet started)

1. Concatenate chunk outputs → verify L2-L5 each reach 50 records
2. FL5 sentinel re-grep (action vs facing_bet legality across all 118 new labels)
3. Opus tier-up subagent on non-unanimous + owner-arb candidates → `batch_008_raw_labels_opus_tierup.jsonl`
4. A0.3b — normalize via `river-rats-core/sizing_schema_normalizer.py` (per-file CLI) → `*_v2.jsonl` + audit
5. `compute_consensus_v2()` → `batch_008_consensus_v2.jsonl`; malformed-rate gate ≤15%
6. A0.3c — brief patch as FINAL commit on branch (blueprint v2 §2.1-§2.4)
7. PR submission: `builder: A0.3 batch-008 completion + normalize + brief patch (final batch in Phase 2-E)`

Standing by post-completion for QC dispatch.
