---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #222 — Phase 12.5I-D corpus assemble (694 + 94 = 788; 61-surface uniform) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR222_2026-05-06.md (master `6f5e32a`, PR #223)
pr_branch: programmer/phase125i-d-corpus-assemble-2026-05-06 (head `dcb3108`)
qc_branch: qc/pr222-corpus-assemble-review-2026-05-06
---

# PR #222 — pre-merge QC verdict: PASS (0/0/0)

21st solo cycle. Mechanical corpus assemble (no Opus tier-up needed per dispatch §"Why no Opus tier-up on 12.5I-D"). All 7 trigger items verified independently against canonical artefacts (`river-rats-core/feature_extractor.py`, source corpora `corpus_combined_694_2026-05-06.jsonl` + `corpus_revision_125i_situations_2026-05-06.jsonl` + `corpus_revision_125i_labels_2026-05-06.jsonl`, BATCH2 reference `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. Row count integrity (788 / no dups / ordering) | ✅ PASS |
| 3. Schema match (61-surface uniform; 694 + 125i preserved) | ✅ PASS |
| 4. Feature backfill correctness (5/5 spot-check + activation rates) | ✅ PASS |
| 5. Distribution table correctness (action + confidence) | ✅ PASS |
| 6. Reference correctness (MW-25 still CHECK HIGH post-PR #218) | ✅ PASS |
| 7. TC-X-OWNER-SCOPE-DISCIPLINE (no v3.x / BATCH2 / core touched) | ✅ PASS |

**Verdict: PASS — clear to merge.** No follow-up actions queued by QC.

## §1 — Diff scope strict (TC-23)

`git diff --stat master...programmer/phase125i-d-corpus-assemble-2026-05-06`:

```
 data/corpus_combined_788_2026-05-06.jsonl          | 788 +++++++++++++++++++++
 data/corpus_combined_788_labels_2026-05-06.jsonl   | 788 +++++++++++++++++++++
 review/comms/BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md | 168 +++++
 scripts/assemble_125i_d_788.py                     | 282 ++++++++
 4 files changed, 2026 insertions(+)
```

Exactly the 3 mandatory files + 1 optional script per dispatch §"Deliverable scope" / "Optionally a small assemble script in `scripts/` if needed (per `assemble_v23_*.py` precedent)". No scope creep. **Note:** the two-dot view (`git diff master..branch`) shows `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR222_*.md` as a 69-line deletion — this is a base-divergence artefact only (the trigger comm landed on master via PR #223 *after* PR #222 branched at `e01b296`). The three-dot diff above is the merge contribution and is clean. GitHub's PR view computes three-dot, so merging PR #222 will not delete the trigger comm.

## §7 — Owner-scope discipline

Verified the PR diff does NOT touch:
- `prompts/` (v3.x prompt files) — 0 changes
- `design/multiway_reference_set/BATCH2_*` (BATCH2 reference) — 0 changes
- `river-rats-core/` (production source, including `feature_extractor.py`) — 0 changes
- `training-data/` outside the new combined corpus — 0 changes
- Memory files / `reference_corrections.md` — 0 changes

Owner-scope perimeter held. No fix-forward required.

## §2 — Row count integrity

| Metric | Builder claim | QC measurement | Match |
|---|---|---|---|
| corpus rows | 788 | 788 | ✅ |
| labels rows | 788 | 788 | ✅ |
| 694 contribution | 694 | 694 | ✅ |
| 125i contribution | 94 | 94 | ✅ |
| corpus distinct row IDs | 788 | 788 (via `pilot_hand_id` fallback) | ✅ |
| labels distinct row IDs | 788 | 788 | ✅ |
| cross-source ID collision | 0 | 0 | ✅ |
| Ordering: rows 0..693 | 694-corpus order | first 694 ≡ 694-corpus by ID | ✅ |
| Ordering: rows 694..787 | PILOT_695..PILOT_788 | confirmed (rows 694..783 = PILOT_695..PILOT_784 from 125i situations; rows 784..787 = PILOT_785..PILOT_788 manuals) | ✅ |

The 4 manual canonicals at rows 784..787 (PILOT_785..PILOT_788) are: `t8primeR_manual_canonical_mw25_exact`, `t8primeR_manual_canonical_non_nut_fd`, `t9primeE_manual_canonical_mw40_exact`, `t10primeR_manual_canonical_mw45_exact`. Consistent with the dispatch ("90 parametric + 4 manuals = 94 labels").

**Note (informational, not a finding):** rows have no top-level `ref_id` field — the unique identifier is in `pilot_hand_id` (or `source_situation_id` for older 100-row variant). The dispatch §"Join statistics" says ref_id is computed at runtime via `compute_ref_id`, which matches the on-disk schema. Uniqueness across all 788 rows is preserved through the fallback identifier set.

## §3 — Schema match

**Top-level schema preservation (excluding feat_dict):**

- 694-source has 5 distinct top-level key sets across 694 rows (heterogeneous from prior phases; pre-existing pattern)
- 125i-source has 1 top-level key set across 90 rows
- 12.5I-D output: rows 0..693 match 694-source row-by-row in top-level keys, with **0 mismatches** and **0 non-feat_dict field-value changes**; rows 694..783 match 125i-source the same way (90 rows checked, 0 mismatches, 0 changes)

The four manual canonicals (rows 784..787) carry the additional `template` + `author_design_note` + `generation_source` fields per their canonical-manual variant (matches the 24-row variant already present in the 694 baseline).

**feat_dict surface uniformity (61-surface):**

| Check | Result |
|---|---|
| All 788 rows have `feat_dict` size 61 | ✅ |
| Rows missing `nut_blocker_overcard_count` | 0 / 788 |
| Rows missing `bet_call_multiway_oop_raise_pressure_index` | 0 / 788 |
| Rows with NaN/Inf anywhere in feat_dict | 0 / 788 |
| Distinct feat_dict key sets | 1 (perfectly uniform) |

Per `feedback_attention_flags_when_features_change.md`, 61-surface uniform across the entire 788 corpus is the gating requirement for downstream attention vocab + capture + trainer alignment. Confirmed.

## §4 — Feature backfill correctness

Spot-checked **5 random pre-existing 694-corpus rows** (seed=42 → rows [654, 114, 25, 281, 250]) by re-importing `feature_extractor.compute_nut_blocker_overcard_count` + `compute_bet_call_multiway_oop_raise_pressure_index` from `river-rats-core/feature_extractor.py:2136` / `:2174` and recomputing both Step-18 features from each row's `feat_dict` inputs (`high_card_rank`, `nut_flush_block`, `num_callers_to_bet`, `num_opponents`, `is_ip`, `has_flush_draw`, `raw_equity`) + top-level (`hero_cards`, `facing_bet`).

| Row | Hero | Inputs sampled | k1 expected | k1 actual | k2 expected | k2 actual | Match |
|---|---|---|---|---|---|---|---|
| 654 | AsQs | nut_flush_block=1, hi_rank=11 | 2 | 2 | 0.0 | 0.0 | ✅ |
| 114 | KdKh | nut_flush_block=0 | 0 | 0 | 0.0 | 0.0 | ✅ |
| 25 | 7h7d | nut_flush_block=0 | 0 | 0 | 0.0 | 0.0 | ✅ |
| 281 | KsQd | nut_flush_block=0 | 0 | 0 | 0.0 | 0.0 | ✅ |
| 250 | 5s6s | nut_flush_block=0 | 0 | 0 | 0.0 | 0.0 | ✅ |

5/5 PASS — backfill outputs exactly match canonical extractor.

**Activation rates (corpus-wide):**

| Feature | QC measured | Builder claim | Match |
|---|---|---|---|
| `nut_blocker_overcard_count > 0` | 124 / 788 = 15.7% | 124 / 788 = 15.7% | ✅ |
| `bet_call_multiway_oop_raise_pressure_index > 0` | 25 / 788 = 3.2% | 25 / 788 = 3.2% | ✅ |

Both rates align with the MW-17 axis (15.7% nut-blocker + overcard signal class) and the MW-47 axis (3.2% composite v3.4 Fix 2.1.1 clause-e gating). No drift.

## §5 — Distribution table correctness

**Per-action distribution (consensus_action across 788 labels):**

| Action | Builder | QC | Match |
|---|---|---|---|
| CHECK | 326 (295 + 31) | 326 (295 + 31) | ✅ |
| BET | 169 (137 + 32) | 169 (137 + 32) | ✅ |
| RAISE | 131 (104 + 27) | 131 (104 + 27) | ✅ |
| CALL | 81 (79 + 2) | 81 (79 + 2) | ✅ |
| FOLD | 81 (79 + 2) | 81 (79 + 2) | ✅ |
| Total | 788 (694 + 94) | 788 (694 + 94) | ✅ |

**Per-confidence distribution:**

| Confidence | Builder | QC | Match |
|---|---|---|---|
| 1.0 | 493 | 493 | ✅ |
| 0.8 | 165 | 165 | ✅ |
| 0.6 | 125 | 125 | ✅ |
| 0.4 | 5 | 5 | ✅ |
| Total | 788 | 788 | ✅ |

Both tables exactly match. No spot-check fail.

## §6 — Reference correctness (MW-25 post-PR #218)

`design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md:27` reads:

```
| MW-25 | position_ampli | 0.337 | 0.000 | CHECK | HIGH |
```

CHECK HIGH is the active reference label after PR #218's `BET HIGH → CHECK HIGH` graduation. The narrative axis-block at line 1029 confirms (`*(MW-25 corrected 2026-05-06; was BET)*`) and the axis-4 insight at line 1032 carries the corrected reasoning ("the corrected axis-4 insight: position amplification differentiates MADE-hand value... but for non-nut DRAWS it does not flip the action — both IP (MW-25) and OOP (MW-26) check"). No regression on PR #218 effect.

PR #222 does not modify the reference file (verified §1 above), so the post-PR #218 state is preserved by construction. Stop condition "Reference label not reading CHECK HIGH on MW-25" is **not** triggered.

## §"Stop conditions" — all clear

Per dispatch §"Stop conditions":
- ❌ Schema mismatch between 694 and 94 → not triggered (§3)
- ❌ Duplicate ref_ids → not triggered (§2: 0 collisions)
- ❌ Feature backfill produces ≥1% NaN or Inf → not triggered (§3: 0 NaN/Inf in 788 rows × 61 keys)
- ❌ Reference label not reading CHECK HIGH on MW-25 → not triggered (§6)
- ❌ 788-row count not exact → not triggered (§2)

## Test classes exercised

- TC-23 spec-vs-infrastructure code drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (perimeter audit, 2nd formal use after PR #218 introduction)
- TC-25 audit-trail integrity (pre-merge variant on data corpus)
- TC-X-DISPATCH-PREDICTION-VERIFICATION (builder activation-rate predictions verified, both axes match exactly)

## Smarter-over-time artefact updates

No new test classes added (clean PASS, no missed pattern). `learning/coverage_map.md` cell for "data assemble × Step-18 feature backfill" is now exercised twice (12.5H-D 604→694 in PR #181 era, 12.5I-D 694→788 here) — logging this in the curative log as "no curative needed; clean replication of corpus-assemble pattern."

## Audit cost / time

- Wall clock: ~12 min (data inspection + canonical extractor recomputation + reference grep). On the lower end of the dispatch's 10-15 min estimate.
- LLM cost: $0 (mechanical Python / git operations).

## Gates

PR #222 cleared on QC side. Per dispatch sequencing (`MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` §"Sequencing — what fires after 12.5I-D merges"):
- 12.5I-MW40-VERIFICATION-A design dispatch — gates on PR #222 merge
- 12.5J-D-pre test-guard deflake dispatch — gates on PR #222 merge (sequential after MW-40-A)

No QC-side blocker on either downstream dispatch.

## References

- 12.5I-D dispatch: `MAIN_TERMINAL_PR218_MERGE_AND_125ID_DISPATCH_2026-05-06.md` (master `680f51d`, PR #221)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR222_2026-05-06.md` (master `6f5e32a`, PR #223)
- Builder report: `BUILDER_REPORT_PHASE125I_D_CORPUS_ASSEMBLE_2026-05-06.md` (in PR #222)
- Source 694-corpus: `data/corpus_combined_694_2026-05-06.jsonl`
- Source 125i situations: `data/corpus_revision_125i_situations_2026-05-06.jsonl`
- Source 125i labels: `data/corpus_revision_125i_labels_2026-05-06.jsonl`
- Canonical feature extractor: `river-rats-core/feature_extractor.py:2136` / `:2174`
- BATCH2 reference: `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md:27` (table) / `:1029` (narrative)
- Memory: `feedback_attention_flags_when_features_change.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`

**Status: VERDICT = PASS. PR #222 cleared for merge from QC side. No fix-forward queued. 21st solo QC cycle.**
