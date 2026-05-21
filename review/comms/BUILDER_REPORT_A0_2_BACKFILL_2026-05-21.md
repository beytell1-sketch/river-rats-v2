# BUILDER REPORT — A0.2 BACKFILL (batches 001-007)

**Date:** 2026-05-21
**Author:** Builder (lead-programmer hat)
**Scope:** PR A0.2 per blueprint `DRAFT_BLUEPRINT_A0_SCHEMA_FIX_v2_2026-05-21.md` §6.
**Branch:** `builder/a0.2-backfill-2026-05-21` (rooted at master b0829c3, the A0.1 merge).
**Status:** READY FOR QC PRE-MERGE.

---

## Summary

Ran `river-rats-core/sizing_schema_normalizer.py` (master b0829c3, A0.1 ship) over all 7 full-700 corpus batches (001-007). Produced 63 new files per the §6 manifest (7 batches × 9 files each).

### Acceptance gates

| Gate | Threshold | Result |
|---|---|---|
| Per-batch malformed_rejected rate | ≤ 15% (hard) | 0.00%-4.71% (PASS all 7) |
| Per-label `predicted_action` byte-equal v1 vs v2 (F-10) | 100% | 100% (1577/1577 labels checked) |
| All BET v1 `predicted_sizing_pct ∈ {25,33,50,66,75,100,150}` → matching `predicted_bet_pct` in v2 | 100% | 100% |
| RAISE labels `status=clean / clean_all_in` → numeric `predicted_raise_to_bb` in v2 | 100% | 100% |
| Malformed-rejected RAISE labels with ≥3-of-5 malformed → spot in `owner_arb_queue_normalizer.jsonl` | required | 3/3 spots routed (all in batch_001) |
| v2 consensus ACTION distribution matches v1 consensus | exact | EXACT for batches 002-007; one delta in batch_001 (see "Anomalies" below — NOT sizing-driven) |

### Pilot result

Batch_001 ran first per orchestrator pilot-first instruction. Pilot PASSED all hard gates. Proceeded to batches 002-007. No retraction needed.

---

## Per-batch breakdown

Counts are per-label across 5 labellers + opus tier-up (where present). Action-distribution-delta column: number of `consensus_action` values that differ between v1 consensus and v2 consensus for spots present in BOTH files.

| Batch | Labels | clean | clean_all_in | ambiguous_resolved | malformed_rejected | malformed-rate | normalizer-owner-arb | action-dist-delta |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 001 | 255 | 240 | 0 | 3 | 12 | 4.71% | 3 | 1 (non-sizing; see Anomalies §1) |
| 002 | 253 | 252 | 0 | 1 | 0 | 0.00% | 0 | 0 |
| 003 | 254 | 254 | 0 | 0 | 0 | 0.00% | 0 | 0 |
| 004 | 254 | 224 | 3 | 27 | 0 | 0.00% | 0 | 0 |
| 005 | 255 | 237 | 0 | 18 | 0 | 0.00% | 0 | 0 |
| 006 | 251 | 218 | 3 | 30 | 0 | 0.00% | 0 | 0 |
| 007 | 255 | 240 | 0 | 15 | 0 | 0.00% | 0 | 0 |
| **TOTAL** | **1777** | **1665** | **6** | **94** | **12** | **0.68%** | **3** | **1** |

(Total labels = 5 labellers × 50 spots × 7 batches + opus rows. Opus presence varies per batch since opus tier-up only fires on 3-2 splits.)

---

## Files produced

For each batch N ∈ {001..007}:

- `data/4way_corpus/full_700/batch_NNN_raw_labels_labeller_M_v2.jsonl` for M ∈ {1..5}
- `data/4way_corpus/full_700/batch_NNN_raw_labels_opus_tierup_v2.jsonl`
- `data/4way_corpus/full_700/batch_NNN_consensus_v2.jsonl`
- `data/4way_corpus/full_700/batch_NNN_normalizer_audit.jsonl`
- `data/4way_corpus/full_700/batch_NNN_owner_arb_queue_normalizer.jsonl`

Total: **63 new files**. Plus this report.

### v1 files preserved unchanged (RH-4)

Per blueprint RH-4 ("legacy `predicted_sizing_pct` in v2 files: removed; preserved in audit logs only"), the v1 raw label files and v1 consensus files are NOT modified. They remain on disk as historical record.

---

## Consensus_v2 strategy (per blueprint §3.6)

- ACTION consensus: reuses `scripts/dispatch_4way_labelling_pilot.py:consensus_rule` (per blueprint instruction).
- SIZING consensus: uses `compute_consensus_v2` from `river-rats-core/sizing_schema_normalizer.py` (already shipped in A0.1).
- For sizing: only labellers who voted the consensus action are pooled. Malformed labels excluded. clean/clean_all_in weight=1.0; ambiguous_resolved weight=0.7. Tie-break = smaller wins (conservative).
- BET tie-break: prefer solver-aligned (flop=25/66; turn=33/75; river=33/75/150) per `feedback_solver_aligned_sizing.md`, then smaller.
- ≥3 of 5 RAISE-voting labellers malformed → `sizing_status="malformed-via-arb"`, route to `owner_arb_queue_normalizer.jsonl`.

**No new core code added.** All logic already lives in `river-rats-core/sizing_schema_normalizer.py` (A0.1). The A0.2 driver is a /tmp/ throwaway orchestration script, NOT promoted to repo per blueprint scope ("PR A0.2 adds data only").

---

## Anomalies

### §1. Single consensus_action delta in batch_001 (4WF-4-WAY-3--026)

- v1 sonnet votes: `["BET", "BET", "CHECK", "CHECK", "CALL"]`; opus: `CHECK`
- v1 consensus state: `"2-2-1-opus-joins-CHECK"`; v1 consensus_action: `CHECK`
- v2 consensus state (per canonical `consensus_rule`): `"2-2-1+"`; v2 consensus_action: `null` → owner-arb routed

**Root cause:** v1 batch_001 was processed with an ad-hoc extension to the consensus rule that promoted a 2-2-1 split to a consensus when opus joined one of the 2-counts. The canonical `consensus_rule` function in `scripts/dispatch_4way_labelling_pilot.py:189` (the function the blueprint instructs us to reuse) does NOT have this opus-joins-2-2-1 extension — it returns `('2-2-1+', None)` for any 2-2-1 split. Confirmed via search: the string `2-2-1-opus-joins` appears only in batch_001's consensus file and in one historical QC review note; it is not in any committed `.py` file.

**Classification:** NOT sizing-driven. This is a pre-existing consensus-rule inconsistency that surfaces when we re-run the canonical rule. The F-10 invariant ("sizing shouldn't change which action wins") is intact — per-label action drift is 0.

**Recommendation:** route 4WF-4-WAY-3--026 to owner-arb (or owner-confirms-CHECK). The spot is already in `batch_001_consensus_v2.jsonl` with `consensus_action: null` and full vote record preserved for owner adjudication.

### §2. Opus labeller_id type mismatch (handled in driver)

The opus tier-up files write `"labeller_id": "opus_tierup"` (string), but `normalize_label` casts to `int(labeller_id)` which raises `ValueError`. Driver patches `labeller_id` to sentinel `-1` for the normalizer call and restores the string in the v2 output. **Suggested follow-up:** patch the normalizer to accept either str or int for `labeller_id` (one-line fix, would belong in a small core-code PR — out of scope here per "A0.2 adds data only").

### §3. Schema inconsistency in v1 consensus files (`consensus_state` vs `state`)

Per the memory note about prior audit findings: batch_001 v1 consensus uses field name `consensus_state`; batches 002-007 v1 consensus use `state`. Verification logic reads both. v2 consensus files all use canonical `consensus_state` per the blueprint v2 §3.6 schema. **No action required.**

### §4. Batch_001 normalizer-owner-arb spots (3 spots, 12 malformed labels)

Three spots (4WF-4-WAY-3--010, --019, --038) have 4 of 5 sonnet labellers writing `predicted_sizing_pct: null` on a RAISE action. Per blueprint §3.6 (≥3 malformed → sizing-consensus failure), these are routed to `owner_arb_queue_normalizer.jsonl`. The one valid sonnet vote per spot is preserved as `sonnet_sizing_votes` but does not drive consensus.

Owner-arb queue entries:
- 4WF-4-WAY-3--010: 4 malformed, 1 clean (14bb) — owner adjudicate sizing
- 4WF-4-WAY-3--019: 4 malformed, 1 ambiguous_resolved (71bb from v=270) — owner adjudicate sizing
- 4WF-4-WAY-3--038: 4 malformed, 1 clean (14bb) — owner adjudicate sizing

These are the F-4 acknowledged residue plus null-sizing labels from labellers 2-5 who omitted the sizing field for raises.

---

## Verification commands (reproducible)

```bash
# 1. Verify branch base
git rev-parse origin/master  # should equal b0829c3...

# 2. Verify all 63 new files present
ls data/4way_corpus/full_700/batch_*_{v2.jsonl,normalizer_audit.jsonl,owner_arb_queue_normalizer.jsonl} | wc -l  # 63

# 3. Run normalizer dry-run sanity per batch
python3 river-rats-core/sizing_schema_normalizer.py --dry-run \
  data/4way_corpus/full_700/batch_001_raw_labels_labeller_1.jsonl \
  --context data/4way_corpus/full_700/batch_001_50hand.jsonl

# 4. Per-batch malformed counts (audit log)
for n in 001 002 003 004 005 006 007; do
  c=$(grep -c '"status": "malformed_rejected"' data/4way_corpus/full_700/batch_${n}_normalizer_audit.jsonl)
  echo "batch $n: $c malformed"
done
```

---

## Acceptance — final attestation

- [x] §6 file manifest produced in full (63 files).
- [x] All BET clean labels have matching `predicted_bet_pct` and null `predicted_raise_to_bb` in v2.
- [x] All RAISE clean/clean_all_in labels have correct numeric `predicted_raise_to_bb` in v2.
- [x] All RAISE malformed-rejected labels in batches with ≥3 malformed per spot are routed to `owner_arb_queue_normalizer.jsonl`.
- [x] Per-batch malformed_rejected rate ≤ 15% on all 7 batches (max observed: 4.71% in batch_001).
- [x] No sizing-driven action distribution drift (F-10 invariant intact).
- [x] v1 files preserved unchanged (RH-4).
- [x] Brief not modified (orchestrator override; brief patch moves to A0.3).

**Sign-off:** Builder ready for QC pre-merge review per `feedback_qc_required_before_approval.md`.
