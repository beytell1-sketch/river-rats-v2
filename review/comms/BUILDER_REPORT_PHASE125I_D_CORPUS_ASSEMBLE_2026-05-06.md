---
date: 2026-05-06
from: LEAD-PROGRAMMER
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-D corpus assemble — 694 + 94 = 788 hands; all 61-surface uniformly; Step-18 backfill of 94 12.5I-C rows + label-file feat_dicts; MW-25 reference verified CHECK HIGH (no regression)
status: complete; PR opens for QC audit
branch: programmer/phase125i-d-corpus-assemble-2026-05-06
base: master `680f51d` (post-PR #218 + #220 + #221 merge)
---

# Phase 12.5I-D — corpus assemble (788-row combined)

## Headline

| Step | Result |
|---|---|
| Inputs | 694-corpus (61-surface) + 694-labels (59-surface fd) + 94-revision (90 sit + 4 manuals + 94 labels, all 59-surface) |
| Schema validation | ✅ Diff between 694 and 125i feat_dicts is exactly the 2 Step-18 keys |
| Ref-id collision | ✅ 0 (694 ∩ 125i = empty) |
| Step-18 backfill | ✅ 94 situations + (694 + 94) labels feat_dicts brought to 61-surface; 0 NaN/Inf |
| Output rows | 788 / 788 (corpus + labels both) |
| feat_dict surface | 61 keys uniformly across all 788 rows in both files |
| MW-25 reference | ✅ `CHECK HIGH` (verified via `reference_evaluator.parse_reference_hands`); no regression on PR #218 |

**Stop conditions: none triggered.** All 5 dispatch stop checks clean.

**Cost:** ~$0 (mechanical script execution; no LLM calls). **Time:** ~25 min builder.

## §"Schema validation"

```
694-corpus feat_dict size: 61   (post-PR #205 re-extraction)
125i situations feat_dict:  59   (12.5I-B / 12.5I-C predates PR #205 merge)
keys only in 694:           {'nut_blocker_overcard_count', 'bet_call_multiway_oop_raise_pressure_index'}
keys only in 125i:          {} (none)
```

The diff between the two corpora's feat_dict columns is **exactly the 2 Step-18 features** at positions 60-61. This matches the dispatch's anticipated mismatch pattern, just with the directional reverse (the dispatch §"Feature backfill" anticipated 694=59 / 125i=61; reality is 694=61 / 125i=59 because 12.5I-B + 12.5I-C generated their data BEFORE the 12.5J-B PR #205 re-extraction landed). No structural mismatch beyond the expected 2-feature delta — proceeding with backfill direction reversed.

## §"Join statistics"

| Metric | Value |
|---|---|
| 694-corpus rows in | 694 |
| 125i situations in (90 parametric + 4 manuals) | 94 |
| 694 distinct ref_ids | 694 |
| 125i distinct ref_ids | 94 |
| Cross-source ref_id overlap | **0** |
| Final 788-corpus rows | 788 ✓ |
| Final 788-labels rows | 788 ✓ |

ref_id discipline (per `compute_ref_id`): 694-corpus uses `source_situation_id` for some rows and `dN_pos_street` for others; 125i uses `pilot_hand_id`. No collision because the namespaces are disjoint by construction.

## §"Feature backfill"

**Direction:** 59-surface rows backfilled to 61-surface using `feature_extractor.compute_nut_blocker_overcard_count` + `compute_bet_call_multiway_oop_raise_pressure_index` (read-only import; no `river-rats-core/` modifications).

**Rows backfilled:**
- 94 12.5I-C situations (90 parametric + 4 manuals) — top-level `hero_cards` available; backfill direct
- 694 12.5H-D labels — embedded `feat_dict`; `hero_cards` looked up via ref_id in 694-corpus
- 94 12.5I-C labels — embedded `feat_dict`; `hero_cards` looked up via ref_id in 125i situations

**Verification:** all 788 corpus rows AND all 788 label rows have `feat_dict` of size 61 with both Step-18 keys present. NaN/Inf count: **0** (well below the 1% stop threshold).

**Step-18 activation rates (788-corpus):**
- `nut_blocker_overcard_count > 0`: **124 / 788 = 15.7%** (hands with hero holding nut FD blocker AND overcards on board — the MW-17 axis target pattern)
- `bet_call_multiway_oop_raise_pressure_index > 0`: **25 / 788 = 3.2%** (hands matching the v3.4 Fix 2.1.1 clause-e MW-47-axis pattern: facing bet + multiway + OOP + nut FD blocker + has FD + raw_equity ≥ 0.35)

These activation rates look reasonable: MW-17 axis (15.7%) reflects the broader nut-blocker-overcard signal class; MW-47 axis (3.2%) is appropriately narrow per the composite gating logic.

## §"Distribution sanity"

### Per-action distribution (788 combined)

| Action | 788 total | 694 contribution | 125i contribution |
|---|---|---|---|
| CHECK | 326 | 295 | 31 |
| BET | 169 | 137 | 32 |
| RAISE | 131 | 104 | 27 |
| FOLD | 81 | 79 | 2 |
| CALL | 81 | 79 | 2 |
| **Total** | **788** | **694** | **94** |

The 125i contribution skews toward CHECK (T8'-r 30/30) + BET (T9'-e 32/33) + RAISE (T10'-r 27/31) per the targeted MW-25/40/45 axes. The combined 788 distribution stays well-balanced (CHECK 41% / BET 21% / RAISE 17% / FOLD 10% / CALL 10%). No anomalous drift vs the 694 baseline.

### Per-confidence distribution (788)

| Confidence | Count | Notes |
|---|---|---|
| 1.0 (5/5 unanimous) | 493 / 788 = 62.6% | High-signal training rows |
| 0.8 (4-1 majority) | 165 / 788 = 20.9% | Solid signal |
| 0.6 (3-2 majority) | 125 / 788 = 15.9% | Includes the 32 12.5I-C T9'-e + the bulk of pre-existing soft-consensus rows |
| 0.4 | 5 / 788 = 0.6% | Pre-existing 12.5H rows |

The trainer applies sample weights = consensus_confidence; mixed-strategy soft signals down-weight automatically. No quality concerns.

## §"Reference correctness"

Verified via `river-rats-core/reference_evaluator.py:parse_reference_hands` reading the BATCH2 files (post-PR #218 master `e01b296`):

```
MW-25 reference parse: action=CHECK, confidence=HIGH
```

✅ **PR #218 graduation effect confirmed: MW-25 reads CHECK HIGH at the canonical evaluator entrypoint.** No regression.

## §"Stay-wrong baseline"

After PR #218 graduation: 4 stay-wrong remaining.

| Hand | Status | 12.5I-C / 12.5J relevance |
|---|---|---|
| MW-17 | Under-calling (low equity draw) | Step-18 `nut_blocker_overcard_count` targets this axis (positive on hands with hero overcards + nut FD blocker) |
| MW-40 | Residual passive (very thin value bet) | **GRADUATION CANDIDATE per Decision 3β** — 12.5I-MW40-VERIFICATION-A queued (~30 J-on-board parametric variants) |
| MW-45 | Under-raising | T10'-r 27/31 RAISE on slowplay-set core may move the model toward the reference RAISE |
| MW-47 | Shared blind spot (nut draw should raise) | Step-18 `bet_call_multiway_oop_raise_pressure_index` targets this axis |

12.5K combined re-train will measure the impact of the 94-row corpus addition + 2 new features against this 4-hand baseline.

## Files in PR diff (4 per dispatch + 1 supporting script = 5)

1. `data/corpus_combined_788_2026-05-06.jsonl` (788 rows, 61-surface)
2. `data/corpus_combined_788_labels_2026-05-06.jsonl` (788 rows, 61-surface embedded feat_dicts)
3. `scripts/assemble_125i_d_788.py` (assemble script — mirrors `assemble_v23_*.py` precedent)
4. `review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md` (this report)

The dispatch §"Deliverable scope" allows "optionally a small assemble script in scripts/ if needed (per assemble_v23_*.py precedent)". I included the script for reproducibility — the join + backfill discipline is mechanical but non-trivial (handles the 694-vs-125i surface direction inversion + label-file hero_cards lookup via cross-source ref_id map).

## Stop conditions (full record)

| Condition | Triggered? | Evidence |
|---|---|---|
| Schema mismatch between 694 and 94 | NO | diff was exactly the 2 step-18 keys (anticipated; recoverable per dispatch bullet 3) |
| Duplicate ref_ids | NO | 694 ∩ 94 = empty; no within-source duplicates either |
| Feature backfill ≥1% NaN/Inf | NO | 0 NaN/Inf across 788 rows × 2 features = 1576 values |
| MW-25 reference not reading CHECK HIGH | NO | reference_evaluator returned CHECK HIGH |
| 788 row count not exact | NO | 788 / 788 (corpus + labels both) |

## What I did NOT do (per dispatch)

- No edits to `prompts/gto_labeller_v3.4.md`
- No modifications to `river-rats-core/` (read-only import of compute functions)
- No edits to `BATCH2` reference (orchestrator-scope to dispatch BATCH2 changes)
- No retraining or model inference (assemble is corpus-only; training is 12.5K)
- No extrapolation or label drops (Decision 1α = ship all 94 at their consensus confidence)

## What's blocked / what's queued

**Cleared by this PR (after merge):**
- 12.5I-D corpus QC trigger (orchestrator dispatches)
- Step 5: 12.5I-MW40-VERIFICATION-A design dispatch (after 12.5I-D merge)
- Step 6: 12.5J-D-pre test-guard deflake dispatch (after 12.5I-D merge; parallel queue with Step 5)

**Awaiting orchestrator dispatch:**
- 12.5J-C trainer integration test on 61-surface (pending 12.5J-D-pre)
- 12.5K combined re-train (pending 12.5I-E + 12.5J-E ship)

## References

- Dispatch (fire trigger): `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` (master `680f51d`, PR #221)
- PR #218 (BATCH2 MW-25 graduation update merged): master `e01b296`
- PR #220 (QC PASS+1NIT verdict merged): master `7f1365d`
- PR #213 (12.5I-C labelling round merged; 94-revision source): master `994ae67`
- PR #205 (12.5J-B feature implementation merged; 694-corpus 61-surface re-extraction): master `0b77bdd`
- 12.5H-D corpus assemble precedent: `data/corpus_combined_604_*.jsonl` → `data/corpus_combined_694_*.jsonl`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_attention_flags_when_features_change.md`, `feedback_pilot_first_for_long_jobs.md` (no tier-up needed for mechanical assemble), `feedback_orchestrator_decides_not_recommends.md`

**Status: 12.5I-D corpus assemble complete. PR opens for QC audit per dispatch §"QC stream". Builder ready for Step 5 (12.5I-MW40-VERIFICATION-A) on PR merge.**
