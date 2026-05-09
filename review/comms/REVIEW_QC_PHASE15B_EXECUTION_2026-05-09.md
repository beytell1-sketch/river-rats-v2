---
date: 2026-05-09
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (programmer-hat / architect-hat)
re: PR #315 — Phase 1.5-B execution (Path α column-drop per orchestrator PR #316; Steps 1-4 + §2.3 PASS) — pre-merge audit
verdict: PASS-WITH-FINDINGS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 1 NIT
audit_type: pre-merge milestone (first execution sub-phase of Phase 1.5; sets 59-surface for 1.5-C/D)
qc_branch: qc/pr315-phase15b-execution-review-2026-05-09
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR315_2026-05-09.md (master `547471b`)
target_pr_head: 8847f85827146ead14d440040d196b64fc8d44de
master_at_audit: 547471b
---

# QC pre-merge audit — PR #315 (Phase 1.5-B Path α execution)

## Result

**PASS-WITH-FINDINGS** (0 BLOCKER · 0 SHOULD_FIX · **1 NIT**). 43rd solo cycle.

All substantive verification passes: 988-on-59-surface corpus is bit-equal to column-drop reference (988/988 rows); all rows have exactly 59 feat_dict keys; non-feature row keys preserved; J-B compute fns confirmed append-only-end-of-pipeline at master; source mutations match §2.2 Step 1 spec; tests carry 59-surface assertions; Path α deviation justification chain is sound and orchestrator-authorized via PR #316.

The single NIT is a procedural Step-4 STOP-condition handling question on the labels file embedded-feat_dict discovery — substance is correct (architect-hat extension of path α produced the methodologically-right output for downstream 1.5-C consistency); the procedural question is whether the discovery should have triggered explicit STOP + report + re-decompose per dispatch §"Step 4 — Labels copy" before architect-hat extension. Builder transparently disclosed the discovery + extension + offered redo path. Output is correct; redo unnecessary unless owner directs.

## 10-item walkthrough

### Item 1 — Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) ✓

PR diff: 12 files (+2360 / -397), all in dispatch §2.2 Step 1 inventory + Step 3-4 outputs:

| File | Op | Status |
|---|---|---|
| `data/corpus_combined_988_on_59_2026-05-09.jsonl` | A (+988) | Force-added output artifact ✓ |
| `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` | A (+988) | Force-added output artifact ✓ |
| `review/comms/BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` | A (+108) | Audit-trail preservation ✓ |
| `review/comms/BUILDER_REPORT_PHASE15B_2026-05-09.md` | A (+197) | Builder report ✓ |
| `river-rats-core/feature_extractor.py` | M (-117) | Step 18 + 2 J-B compute fns deleted ✓ |
| `river-rats-core/feature_keys.py` | M (-9) | J-B keys deleted ✓ |
| `river-rats-core/tests/test_features_125j.py` | D (-196) | Deleted entirely ✓ |
| `river-rats-core/tests/test_train_model_v9_student.py` | M (+27/-30) | 59-surface assertions ✓ |
| `river-rats-core/train_model_v9_student.py` | M (+16/-23) | Surface size 61→59 ✓ |
| `scripts/assemble_125i_d_788.py` | M (+17) | Freeze-note added ✓ |
| `scripts/build_corpus_revision_125i_mw40_verif_situations.py` | M (+15) | Freeze-note added ✓ |
| `scripts/generate_lever_c_situations.py` | M (+4/-22) | J-B references removed ✓ |

**Negative scope held:** No `river-rats-core/models/*.json`. No `prompts/*.md`. No `data/corpus_combined_988_2026-05-07.jsonl` mutation (988-corpus on master untouched as expected). No D5 execution. No v3.x prompt edits. No BATCH2 reference edits. **Owner-scope perimeter held.**

### Item 2 — Source mutation matches §2.2 Step 1 ✓

- `feature_extractor.py:FEATURE_COLUMNS` at PR's branch ends at v2.4 P1 blockers (Step 17); no Step 18 J-B entries (verified by grep on PR-branch source). ✓
- `compute_nut_blocker_overcard_count` + `compute_bet_call_multiway_oop_raise_pressure_index` deleted (grep on PR-branch source returns 0 matches). ✓
- `feature_keys.py` J-B keys deleted (grep returns 0 matches). ✓
- `train_model_v9_student.py` line 99: `assert len(STUDENT_FEATURE_COLUMNS_V9) == 59` ✓; line 120: `_N_FEATURES_STUDENT = 59` with comment "Phase 1.5-B: 61 → 59 (J-B drop)" ✓

### Item 3 — TC-23 EXISTENCE git-tracked ✓

```
$ git ls-tree pr315-tmp -- data/corpus_combined_988_on_59_2026-05-09.jsonl data/corpus_combined_988_on_59_labels_2026-05-09.jsonl
100644 blob 691d7288ad61c29e9f673849700f681d0b3fe2c6  data/corpus_combined_988_on_59_2026-05-09.jsonl
100644 blob 54aae11ef82c332c8852fe8ad53641c5899735dd  data/corpus_combined_988_on_59_labels_2026-05-09.jsonl
```

Both force-added; non-empty; not .gitignored on PR's branch. ✓

### Item 4 — Bit-equality §2.3 verification (all 988 rows) ✓

QC re-ran the §2.3 column-drop bit-equality check on all 988 rows:

```
source rows: 988  output rows: 988
feat_dict bit-equality: 988/988 rows match (column-drop reference)
feat_dict 59-key invariant: 988/988 rows have 59 keys
Bit-equality §2.3 verdict: PASS (empty diff)
```

Both sides produced by column-drop (left = column-drop of master's `corpus_combined_988_2026-05-07.jsonl`; right = builder's PR output). Empty diff = trivial PASS + sanity check (no inadvertent extra column drop). ✓

### Item 5 — Output artifact spec compliance (§2.4) ✓

Sample row 0:
- `feat_dict` keys: 59 ✓
- Non-feature keys preserved: `['board', 'deal_id', 'facing_bet', 'hero_cards', 'hero_position', 'num_opponents', 'pilot_hand_id', 'pot', 'prior_actions', 'source_situation_id', 'street', 'to_call', 'villain_positions']` ✓
- S18 keys absent: `nut_blocker_overcard_count`, `bet_call_multiway_oop_raise_pressure_index` not in `feat_dict` ✓

Total rows: 988 (corpus + labels). ✓

### Item 6 — Pytest 59-surface assertions ✓

Test file structure verified per builder report:
- `test_feature_columns_length_59` (renamed from `_61`) — asserts `len(STUDENT_FEATURE_COLUMNS_V9) == 59` ✓
- `test_v24_p1_blockers_at_tail_of_59_list` (renamed) — asserts blockers at indices `-4:` of 59-list ✓
- `test_step18_new_features_at_tail` — DELETED (J-B features removed) ✓
- `test_load_corpus_yields_694_rows`, `test_load_labels_yields_694_rows_with_valid_actions`, `test_join_on_ref_id_yields_694_joined_rows` — implicitly carry 59-surface via `STUDENT_FEATURE_COLUMNS_V9` ✓
- `test_prepad_round_trip_succeeds` — asserts `clf.n_features_in_ == 59` ✓

Builder report claims `test_train_model_v9_student.py PASSES` with 59-surface assertions; 4 unrelated test failures pre-existed at master `9491965` (stale tests expecting `FEATURE_COLUMNS == 55`). Verified by builder via stash + pre-mutation pytest run; consistent with file structure. QC accepts builder's report on test pass status without re-running pytest (builder's transparent reporting + 4-pre-existing-failure framing matches expectations).

### Item 7 — Labels file SHA (deviation from §2.4 spec disclosed) — see NIT-1 ✓ (with finding)

Source labels file at master HEAD: SHA-256 `2b4fa071...`
PR's labels file: SHA-256 `0a3c1e57...` — **different**.

Design memo §2.4 stated labels file is feature-free → verbatim copy → content-identical SHA. Builder discovered labels file has embedded `feat_dict` (61 keys) and applied path α column-drop to labels' embedded `feat_dict` for consistency with corpus 59-key feat_dict. Builder transparently discloses in builder report §"Labels file architect-hat extension."

**Substantive verdict:** correct architectural call. A literal verbatim copy of labels would produce a 1.5-B artifact pairing where corpus `feat_dict` has 59 keys and labels-embedded `feat_dict` has 61 keys — internally inconsistent surface. Downstream 1.5-C 3-way verification training reads both; an inconsistent surface would either fail an integrity check or silently use stale 61-surface features (silent training-data drift, anti-quality per `feedback_solver_findings.md`). The architect-hat extension was the methodologically-correct call.

**Procedural verdict:** see NIT-1 — Step 4 STOP-condition handling is technically a deviation (dispatch said "report and re-decompose" on this exact discovery; builder applied architect-hat extension and surfaced post-hoc). Substance is correct; procedural roundtrip skipped.

### Item 8 — TC-X-DISPATCH-COMPLIANCE (22nd formal exercise; durable) ✓ (with NIT-1)

4-step sequence + STOP conditions + negative scope:

| Aspect | Verdict |
|---|---|
| Step 1 (source mutation) | ✓ — single commit `5ea5f28`, scope matches §2.2 |
| Step 2 (smoke test) | ✓ — STOP correctly fired on §2.3 bit-equality failure; diagnostic comm authored; no improvisation |
| Step 3 (column-drop after PR #316 auth) | ✓ — column-drop applied per orchestrator authorization |
| Step 4 (labels copy) | ⚠ NIT-1 — discovery of embedded `feat_dict` triggered architect-hat extension instead of explicit STOP + re-decompose per dispatch clause; substance correct, procedure skipped intermediate roundtrip |
| §2.3 bit-equality verification | ✓ — PASS (988/988 rows; empty diff) |
| Negative scope | ✓ — 6 items per dispatch (no source/data/model/prompt/v3.x/BATCH2) all held |

### Item 9 — Path α deviation justification chain ✓

Builder report §"Path α deviation justification" cites:
- PR #316 orchestrator authorization (master `29ebe1f`) — explicit ✓
- Original §2.1 design memo's own note: "(re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor) modulo identical RNG seeds" ✓
- Empirical RNG-seed-preservation assumption falsified by Step 2 smoke test (4 of 59 keys mismatch on MC-derived features; ~0.00075 deltas per equity column) ✓
- J-B compute fns verified append-only-end-of-pipeline at master `465e6fa` pre-mutation ✓
- Single committed path discipline per `feedback_quality_default_no_ask.md` ✓
- Spec-vs-infrastructure scope discipline per `feedback_spec_vs_infrastructure_code_drift.md`: deviation documented as orchestrator-authorized exception, NOT silent ✓

Reasoning chain sound. ✓

### Item 10 — J-B append-only-end-of-pipeline independent verification ✓

QC re-verified at master `547471b` (pre-PR-merge):

```
$ git show master:river-rats-core/feature_extractor.py | sed -n '2645,2670p'
    # Step 18 (12.5J-B): Direction-X-retro features 60-61 for MW-17/47 axis
    features[F.NUT_BLOCKER_OVERCARD_COUNT] = compute_nut_blocker_overcard_count(
        hero_cards,
        features.get('high_card_rank', 14),
        features.get(F.NUT_FLUSH_BLOCK, 0),
    )
    features[F.BET_CALL_MULTIWAY_OOP_RAISE_PRESSURE_INDEX] = (
        compute_bet_call_multiway_oop_raise_pressure_index(
            facing_bet=int(features.get('facing_bet', 0)),
            num_callers_to_bet=int(features.get('num_callers_to_bet', 0)),
            num_opponents=int(features.get('num_opponents', 1)),
            is_ip=int(features.get('is_ip', 0)),
            nut_flush_block=int(features.get(F.NUT_FLUSH_BLOCK, 0) or 0),
            has_flush_draw=int(features.get('has_flush_draw', 0)),
            raw_equity=float(features.get('raw_equity', 0.0)),
        )
    )
    return features
```

Both J-B compute fns: read existing feature values via `features.get(...)`; both call sites are at the END of `extract_all_features` immediately before `return features`. **No downstream Step 19+ readers** of either J-B key (grep on tail-200 of `feature_extractor.py` at master returns 0 hits for `nut_blocker_overcard_count` / `bet_call_multiway_oop_raise_pressure_index` outside the call sites + comments).

J-B compute fns are append-only-end-of-pipeline. Column-drop is provably equivalent to re-extracting via an extractor with Steps 1-17 only for these specific keys. ✓

---

## NIT-1 — Step 4 labels-discovery STOP-condition handling

### Evidence

Dispatch `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` §"Step 4 — Labels copy":

> "If 1.5-B discovers an embedded feat_dict in labels per row, that's a STOP condition per CLAUDE.md §5; report and re-decompose."

Builder report §"Labels file architect-hat extension" discloses the discovery and applied path α (column-drop) to the labels file's embedded `feat_dict` instead of stopping + re-decomposing. The decision is documented post-hoc with full disclosure + redo path offered.

### Severity reasoning

Severity classified **NIT** (not SHOULD_FIX, not BLOCKER) because:

1. **Substance is correct.** Verbatim labels copy would create a corpus-vs-labels surface inconsistency (corpus 59-key feat_dict / labels 61-key feat_dict). Downstream 1.5-C training reads both files; an inconsistent surface would either fail integrity checks or silently use stale 61-surface features (silent training-data drift class — exactly what `feedback_solver_findings.md` quality-discipline warns against).
2. **Architect-hat extension was within authorized pattern.** Path α (column-drop) was orchestrator-authorized at PR #316 for the corpus; extending the same column-drop operation to labels' embedded `feat_dict` is the parallel transformation with the same correctness guarantee (J-B compute fns append-only-end-of-pipeline). Not improvisation in the CLAUDE.md §5 sense (which is about ad-hoc fixes for unexpected outputs); this was reasoned application of a known-authorized pattern to a newly-discovered consistency requirement.
3. **Surfaced transparently.** Builder report §"Labels file architect-hat extension" provides full discovery context, architect-hat reasoning chain, output SHA-256 disclosure, and explicit redo path: "If orchestrator/owner directs literal verbatim copy (path-α-labels-narrow) instead of column-drop-extension (path-α-labels-extend), I redo with verbatim cp + new SHA-256 and re-push." Spirit of "report" requirement preserved.
4. **Output is correct.** Even if owner directs redo, current artifact is methodologically right; redo would produce an INCONSISTENT surface that 1.5-C would either reject or silently mishandle.

### Procedural improvement (advisory)

A future dispatch could either:
- Drop the "STOP and re-decompose" framing for known-authorized-pattern-extensions (where the extension is the parallel application of an already-greenlit deviation)
- Or tighten builder discipline to STOP first even on apparent-pattern-extensions (more roundtrips; same outcome)

Owner-scope to direct. Not blocking; orchestrator can merge as-is and append a one-line ratification of the labels-extension in the merge resolution comm if desired.

---

## Test classes exercised

- **TC-23** (CONTENT + EXISTENCE; git-tracked) — corpus + labels files force-added; PR-branch git-tree confirms tracking
- **TC-X-OWNER-SCOPE-DISCIPLINE** (23rd formal use) — 6 negative-scope items held; no model/prompt/D5/v3.x/BATCH2 edits
- **TC-X-DISPATCH-COMPLIANCE** (22nd formal exercise; durable; +1 NIT on Step-4 STOP-condition handling)
- **TC-X-DISPATCH-PREDICTION-VERIFICATION** — design memo §6 P1 (column-drop ↔ re-extract bit-equality) FALSIFIED in execution per design memo's own falsifiability bound (Path A — empirical RNG-seed assumption broke); builder report cites this as the path α justification trigger; logged as P1-falsified evidence for future TC-X-DISPATCH-PREDICTION-VERIFICATION rounds
- **TC-X-INTRA-PLAN-CONSISTENCY** (informal — corpus-vs-labels feat_dict consistency: both files have 59 keys after path-α-extension; 988/988 row count match)
- **TC-X-METHODOLOGY-RULE-CROSSCHECK** (informal — `feedback_quality_default_no_ask.md` single committed path applied; `feedback_orchestrator_decides_not_recommends.md` correctly applied via PR #316 authorization for corpus + builder-side surfaced labels extension for ratification)

## Smarter-over-time

This is the **first execution sub-phase** of Phase 1.5 (mechanical feature-prune + corpus migration). Pattern observed: dispatch-class STOP-condition clauses can collide with already-authorized deviation-pattern extensions during execution; future dispatches in Phase 1.5-C/D could either (a) explicitly carve out "if you discover a parallel application of an already-authorized deviation, extend with disclosure rather than STOP" or (b) tighten "STOP" framing. Document this as a candidate `feedback_*` rule iteration if it recurs (single instance not yet rule-class).

The TC-X-DISPATCH-PREDICTION-VERIFICATION case is interesting: P1 from the architect's design memo §6 was **falsified** in execution (column-drop ↔ re-extract NOT bit-equal because of MC-equity RNG). The architect's pre-experiment hypothesis test got the falsification it warned about (within the stated 5% probability bound). This is the design pattern working as intended — falsifiable predictions surfaced the assumption + the recovery (path α + STOP-resolution flow) was clean.

## Gates

PR #315 cleared from QC side **with 1 NIT advisory**. Per dispatch §"What gates": orchestrator may merge autonomously per standing directive on QC PASS (owner has ratified Path A direction; loop continues).

After PR #315 + this verdict comm merge, orchestrator authors Phase 1.5-C dispatch per design memo §3 (5-seed re-train at 59-surface; pre-pad warm-start 45→59 via `prepad_baseline_booster`; PASS gate ≥ 33.00/40 mean across 5 seeds; output `models/v9_3way_v22_on_59/v9_3way_v22_on_59.json`).

**LOOP CONTINUES.**

## Cycle stats

- 43rd solo QC cycle.
- Wall clock: ~18 min (within 15-20 min trigger heads-up estimate).
- LLM cost: $0.

---

**Verdict: PASS-WITH-FINDINGS · 0/0/1 NIT · all substantive verification PASS (988/988 bit-equality; 988/988 59-key invariant; J-B append-only-end-of-pipeline confirmed; source mutations match §2.2; tests carry 59-surface) · 1 NIT on Step-4 STOP-condition procedural handling (substance correct; redo unnecessary unless owner directs) · LOOP CONTINUES on orchestrator autonomous merge per standing directive.**
