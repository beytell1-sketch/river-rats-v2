---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #218 PASS+1NIT acknowledged → merge PR #218 + PR #220; queue NIT fix-forward into MW-40 update touch; dispatch 12.5I-D corpus assemble + validate (788-row combined)
status: DIRECTIVE — merges PR #218 + PR #220; fires LEAD-PROGRAMMER on 12.5I-D corpus assemble
---

# PR #218 merge + 12.5I-D dispatch

QC PASS+1NIT on PR #218 (`REVIEW_QC_BATCH2_MW25_GRADUATION_2026-05-06.md` on `qc/pr218-batch2-mw25-review-2026-05-06`). NIT is non-blocking citation form (`BATCH2_8_RANGE_ANALYSIS.md` MW-25 detail block cites 3/4 sources by PR # + 1 by description "5/5 pilot CHECK"; memory file `reference_corrections.md` has all 4 by PR #). Per loop directive: doc/memory PR with PASS → merge after re-checking findings. NIT fix-forward queued into the next BATCH2 reference touch (MW-40 graduation update PR if Decision 3β verification passes).

## NIT acknowledged + fix-forward queue

QC suggested 1-line fix: add `(PR #208)` after "5/5 pilot CHECK" in `BATCH2_8_RANGE_ANALYSIS.md` MW-25 detail block. Folded into next BATCH2 PR touch (deferred, not blocking). Owner-scope discipline preserved (NIT not silently fixed by orchestrator since BATCH2 is owner-scope; queued for builder dispatch).

## LEAD-PROGRAMMER — 12.5I-D dispatch (fire on this comm merge + PR #218/220 merge)

Branch: `programmer/phase125i-d-corpus-assemble-2026-05-06`. Base: master post-this-comm-merge + post-PR-#218-merge + post-PR-#220-merge.

### Scope — corpus assemble (mirror 12.5H-D precedent: 604 → 694)

Produce a new combined corpus by joining the existing `data/corpus_combined_694_2026-05-06.jsonl` with the new 94 labels from `data/corpus_revision_125i_labels_2026-05-06.jsonl` (PR #213).

**Output target:** `data/corpus_combined_788_2026-05-06.jsonl` (694 + 94 = 788 hands).

### What 12.5I-D does

1. **Schema validation** — verify 694-corpus rows + 94-revision rows share identical schema (column names, dtypes, feat_dict structure, version stamps). Any mismatch → STOP and route to orchestrator. Per `feedback_attention_flags_when_features_change.md`: feature changes require matching attention vocab + capture + trainer; if 12.5J-B Step-18 features (now 61-surface per PR #205) appear in 94-revision but not 694-corpus, flag explicitly.

2. **Join** — concatenate 694-corpus + 94-revision into 788-corpus. Primary key: `ref_id` (or whatever the existing corpus uses). Verify no duplicate ref_ids between the two sources. Sort order: preserve 694-corpus order; append 94 in their generation order (PILOT_695..PILOT_788).

3. **Feature backfill (if needed)** — if 694-corpus is on 59-surface (pre-12.5J-B) and 94-revision is on 61-surface (post-12.5J-B), backfill the 2 new Step-18 features (`nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`) into the 694-corpus rows. Per `feature_extractor.py`, both should be deterministically computable from `feat_dict` + board state.

4. **Distribution sanity** — produce per-template + per-action distribution tables (CHECK / BET / RAISE / CALL / FOLD breakdown). Compare against expected distributions from prior reports. Flag any large drift.

5. **Reference correctness check** — verify MW-25 reference label in `BATCH2_8_RANGE_ANALYSIS.md` is now CHECK HIGH (post-PR #218); verify reference_evaluator.py reads it correctly. (No code changes — read-and-verify only.)

6. **Builder report** — `review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md`:
   - §"Schema validation"
   - §"Join statistics" — rows in / rows out / duplicate ref_ids found / final count
   - §"Feature backfill" — what backfilled, how, verification
   - §"Distribution sanity" — tables
   - §"Reference correctness" — confirm MW-25 reads CHECK HIGH
   - §"Stay-wrong baseline" — list 4 remaining (MW-17/MW-40/MW-45/MW-47); MW-40 marked as graduation candidate per Decision 3β

### Stop conditions

- Schema mismatch between 694 and 94 → STOP, route to orchestrator
- Duplicate ref_ids → STOP
- Feature backfill produces ≥1% NaN or Inf → STOP
- Reference label not reading CHECK HIGH on MW-25 → STOP (regression on PR #218 effect)
- 788-row count not exact → STOP

### What you do NOT do

- Do NOT touch v3.x prompts
- Do NOT modify river-rats-core/ source (read-only)
- Do NOT modify BATCH2 reference (orchestrator-scope to dispatch BATCH2 changes)
- Do NOT retrain or run inference (12.5I-D is corpus assemble only; training is 12.5K)
- Do NOT extrapolate or drop labels (Decision 1α = ship all 94 at their 0.6/1.0/0.8 confidence)

### Cost / time

~$0.20 (script execution; no LLM calls). ~20-30 min builder time including report.

### Deliverable scope

3 files in PR diff:
1. `data/corpus_combined_788_2026-05-06.jsonl` (788 rows)
2. `data/corpus_combined_788_labels_2026-05-06.jsonl` (788 rows; consensus action + confidence per hand) — mirror 694 pattern (`corpus_combined_694_labels_2026-05-06.jsonl`)
3. `review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md`

Plus optionally a small assemble script in `scripts/` if needed (per `assemble_v23_*.py` precedent).

## QC stream — what you audit (when 12.5I-D PR opens)

Standalone audit pattern, similar to 12.5I-C but adapted for corpus-assemble scope:

1. **Diff scope strict (TC-23)** — exactly 3 files (+ optional script). No drift outside data/ + review/comms/ + scripts/.
2. **Row count integrity** — 694 + 94 = 788 exact; no duplicates by ref_id.
3. **Schema match** — column names + dtypes consistent between source and output corpora.
4. **Feature backfill correctness** — spot-check 5 random pre-existing 694-corpus rows: do the 2 new Step-18 features compute correctly from `feat_dict`? (Compare against `feature_extractor.compute_step18_features()` if such a helper exists.)
5. **Distribution table correctness** — match builder report's distribution table against the actual jsonl distributions.
6. **Reference correctness** — MW-25 in BATCH2_8_RANGE_ANALYSIS.md still CHECK HIGH (no regression).
7. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x prompts, no BATCH2 edits, no river-rats-core/ source touched in this PR.

QC writes `review/comms/REVIEW_QC_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md`. ~10-15 min audit.

## Why no Opus tier-up on 12.5I-D

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs (Sonnet judgments on poker hands). 12.5I-D is mechanical corpus assembly — script-driven join + backfill. No new poker judgments produced. Standard QC PASS suffices.

## Sequencing — what fires after 12.5I-D merges

Per `MAIN_TERMINAL_PR213_DECISIONS_AND_DISPATCH_2026-05-06.md` queue:

1. **12.5I-MW40-VERIFICATION-A design dispatch** (Decision 3β) — design ~30 J-on-board parametric variants. Mirror 12.5I-A pattern.
2. **12.5J-D-pre test-guard deflake dispatch** (Option b: tier-2 Δ-tolerance per `MAIN_TERMINAL_PR205_MW33_RESOLUTION_*.md`).

Both run sequentially through builder. Orchestrator dispatches each as the prior PR merges.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #218 merge (BATCH2 MW-25 graduation + reference_corrections.md memory)
- PR #220 merge (QC verdict record)
- 12.5I-D dispatch fires

**Newly queued (after 12.5I-D merges):**
- 12.5I-MW40-VERIFICATION-A design dispatch
- 12.5J-D-pre test-guard deflake dispatch
- BATCH2 NIT-1 fix-forward (folds into MW-40 update PR if Decision 3β verification passes; otherwise standalone)

**Still queued (later):**
- 12.5I-MW40-VERIFICATION-B/C/D/E (situation gen → labelling → tier-up → graduation decision)
- 12.5J-C / 12.5J-D / 12.5J-E (post-deflake feature work)
- 12.5K combined re-train (gates on 12.5I-E + 12.5J-E)
- 12.5L gate eval (gates on 12.5K)

## References

- PR #218 (BATCH2 MW-25 graduation update): `programmer/batch2-mw25-graduation-update-2026-05-06`
- PR #220 (QC PASS+1NIT verdict): `qc/pr218-batch2-mw25-review-2026-05-06`
- PR #219 (QC trigger that fired this audit): master `cb86c9d`
- PR #217 (orchestrator decisions + Step 1 dispatch): master `d6912ad`
- 12.5H-D corpus assemble precedent: `data/corpus_combined_604_*.jsonl` → `data/corpus_combined_694_*.jsonl`
- Memory: `feedback_quality_default_no_ask.md` (slow-quality default; queue NIT fix-forward), `feedback_attention_flags_when_features_change.md` (Step-18 feature backfill discipline), `feedback_pilot_first_for_long_jobs.md` (no tier-up needed for mechanical corpus assemble)

**Status: PR #218 + #220 cleared for merge. LEAD-PROGRAMMER fires 12.5I-D corpus assemble (788-row combined) on this comm merge. ~25-30 min wall clock to PR open.**
