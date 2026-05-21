# MAIN_TERMINAL — Batch-008 Resume FIRE NOW (A0.3a)

**DATE:** 2026-05-21
**AUTHOR:** Orchestrator
**STATUS:** FIRE NOW
**TARGET:** Builder terminal (river-rats-v2/ on `builder-phase2-e-full-batch8-2026-05-12`, post-rebase)
**TYPE:** A0.3a — batch-008 labelling continuation; pilot-first sub-rule does NOT apply (already past pilot, mid-batch resume)

---

## MAIN_TERMINAL — Builder: fire now A0.3a

Builder resumes Phase 2-E batch-008 by finishing labellers 2-5. Spawn 13 parallel labelling subagents in ≤10-hand chunks per PROCESS_GUIDE §1.1.

---

## Pre-flight (required before spawning labelling subagents)

1. **Rebase to current master** (orchestrator authorized):
   ```bash
   cd ~/river-rats-v2
   git fetch origin
   git rebase origin/master  # advances HEAD from c4021cd → 9e749b3 (A0.1, A0.2, A0.1.1 land in your base)
   ```
   Confirm working tree still has the 11 untracked batch-008 + mass_labelling artifacts.

2. **Verify untracked artifact counts match expected state:**
   - `wc -l data/4way_corpus/full_700/batch_008_raw_labels_labeller_*.jsonl`
   - Expected: L1=50, L2=36, L3=11, L4=10, L5=25.

3. **Verify brief is v1** (unchanged):
   - `git diff origin/master -- data/4way_labeller_brief.md` returns empty.
   - Brief stays v1 through batch-008 per blueprint v2 §4 + ratification override. Brief patch is A0.3c (final commit in A0.3 PR).

4. **Read prior labeller context** for continuity:
   - `head -1 data/4way_corpus/full_700/batch_008_raw_labels_labeller_2.jsonl` — see L2's most recent label format/style
   - Same for L3, L4, L5 (their last completed label in each file)
   - Each labelling subagent should produce labels stylistically consistent with the existing L_n entries to maintain labeller-persona continuity within the batch

---

## Subagent dispatch plan (13 total, parallel)

Per PROCESS_GUIDE §1.1 ≤10 hands per agent:

| Labeller | Remaining | Chunks | Spot range (in batch_008_50hand.jsonl) |
|---|---|---|---|
| L2 | 14 | 2 (10 + 4) | spots 37-50 (after L2's existing 36) |
| L3 | 39 | 4 (10 + 10 + 10 + 9) | spots 12-50 (after L3's existing 11) |
| L4 | 40 | 4 (10 + 10 + 10 + 10) | spots 11-50 (after L4's existing 10) |
| L5 | 25 | 3 (10 + 10 + 5) | spots 26-50 (after L5's existing 25) |
| **TOTAL** | **118** | **13** | |

Each subagent receives:
- The v1 brief (`data/4way_labeller_brief.md`)
- Its labeller_id (2, 3, 4, or 5 — int per existing convention; A0.1.1 supports str too but use int for Sonnet labellers)
- The 10-hand (or fewer) input subset from `batch_008_50hand.jsonl`
- Any prior label_examples from the same labeller for persona continuity

Subagents run in parallel. Each writes labels in JSONL to a per-subagent temp file; builder concatenates results into the existing labeller jsonl files.

---

## Acceptance criteria (per existing batch-007 patterns + blueprint discipline)

Builder confirms before submitting PR:

1. **Coverage**: each labeller has 50 labels in their jsonl file (L1=50 unchanged; L2-L5 reach 50)
2. **Action-space discipline (FL5)**: 0 illegal-action votes across all 250 Sonnet labels (per batches 001-007 sentinel: 7 consecutive batches at 0/250). Re-grep all new labels for action-vs-facing_bet legality.
3. **Anti-rule-based reasoning (FL4)**: no template repetition, no if/elif chains, no equity-threshold reasoning, no solver citations in rationale text. Per the brief lines 11-17.
4. **Required rationale structure**: each label has all 5 required sections per brief lines 41-46 (preflop context, per-villain range chains, equity/range tensions, spot-specific factors, action+rationale).
5. **Sizing**: per brief lines 31-34 — `predicted_sizing_pct: int|null` (BET → integer % of pot; RAISE → integer bb amount; CHECK/CALL/FOLD → null). Note: brief stays v1 in this batch; A0.3c will switch to split schema for batch-009.
6. **Confidence + bucket fields populated** on every label.

**Post-labelling Opus tier-up** (existing protocol):
- Identify all spots with non-unanimous Sonnet votes (3-2 / 4-1 splits) AND owner-arb candidates
- Dispatch Opus tier-up subagent on those spots → produces `batch_008_raw_labels_opus_tierup.jsonl`

---

## After labels are complete (in same PR commit chain)

A0.3b — Run normalizer (now shipped on master at `river-rats-core/sizing_schema_normalizer.py`):

```bash
# Pattern matches A0.2 driver. Builder may write a small /tmp/ driver
# similar to A0.2's, OR invoke per-file via CLI:
python river-rats-core/sizing_schema_normalizer.py \
  --apply data/4way_corpus/full_700/batch_008_raw_labels_labeller_2.jsonl \
  --context data/4way_corpus/full_700/batch_008_50hand.jsonl \
  --output data/4way_corpus/full_700/batch_008_raw_labels_labeller_2_v2.jsonl \
  --audit data/4way_corpus/full_700/batch_008_normalizer_audit.jsonl
# (repeat for L1..L5 + opus tierup)
```

Then compute `batch_008_consensus_v2.jsonl` via `compute_consensus_v2()` (shipped in A0.1).

Per-batch malformed-rate gate: ≤ 15% (A0.2 batches 001-007 averaged 0.68%; expect similar). If batch-008 exceeds 15%, STOP and report.

---

## A0.3c — Brief patch (FINAL commit in this PR)

After batch-008 v2 files are produced, AS THE LAST COMMIT on the A0.3 branch, apply the brief patch per blueprint v2 §2 (which replaces lines 31-34, 105-112, 173-187 of `data/4way_labeller_brief.md`).

Reference the exact patch in blueprint v2 §2.1-§2.4. Brief becomes v2 (split schema). Takes effect for batch-009 onward.

Acceptance check: the patch must be the LAST commit on the branch (so batch-008 labellers operated entirely under v1).

---

## Submission

Builder submits one PR `builder: A0.3 batch-008 completion + normalize + brief patch (final batch in Phase 2-E)`.

PR body includes:
- Batch-008 raw label counts (50/50 for all 5 labellers + opus tier-up)
- Normalizer summary (clean / clean_all_in / ambiguous_resolved / malformed counts)
- Action distribution per consensus
- Owner-arb queue snapshot for batch-008
- Brief patch diff summary
- Reference to PR #461 (blueprint v2) + PR #462 (A0.2 backfill) + this directive

Orchestrator dispatches QC pre-merge audit on the PR per `feedback_qc_required_before_approval.md`.

---

## What this directive does NOT authorize

- Touching v2 files in batches 001-007 (already shipped via A0.2)
- Modifying `river-rats-core/sizing_schema_normalizer.py` (frozen after A0.1.1)
- Phase 2-F work (separate scope, owner gating)
- Solver-verify queue drain (parallel workstream)
- Starting batch-009 (post-A0.3 ship)

---

## Builder party — explicit fire-now signal

**Builder — fire now A0.3a labelling subagents per the dispatch plan above.** Acknowledge in `review/comms/BUILDER_ACK_A0_3A_2026-05-21.md` (single short file) before spawning subagents so orchestrator has the start timestamp on record.
