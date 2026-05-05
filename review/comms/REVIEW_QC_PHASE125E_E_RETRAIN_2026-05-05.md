---
date: 2026-05-05
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #152 (12.5E-E re-train at commit acd9938) — APPROVE; 1 NIT (PILOT_595 fix-method)
severity: NIT (1); no HIGH; no MEDIUM; no BLOCKER
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + V-Source-1/3/4 (citation existence) + dispatch §"NEW: Trainer hyperparameter immutability" + §"NEW: Cleanup completeness" + design §7-equivalent corpus integrity
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 6th successive cycle solo-routed)
---

# QC Review — PR #152 (12.5E-E re-train, BLOCKED at owner-tie-gate): APPROVE

## Verdict

**APPROVE PR #152 for merge.** All 5 dispatch-required audits clear cleanly. Trainer hyperparameters bit-stable (cap=3.0, 5 seeds, pre-pad metadata-only, warm-start anchor — all unchanged from 12.5D'). Combined 604-hand corpus = exact byte-concat of (old 494 + new 96 par + new 14 man). 5 queued NIT items applied (1 via annotation rather than direct replacement; substance captured). H-FEAT primary outcome empirically confirmed: `nut_flush_block` importance moved from 0.0000 → 0.0268 (above ml-architect's ≥0.02 prediction).

12.5E-E is a BLOCKED PR (median 32/40 < 33 promote threshold; falls in 31-32 owner-tie-gate band). Model artifact correctly absent per dispatch's no-promotion fallback. 12.5E-F gate evaluation will produce the synthesis for owner WHAT decision.

QC FLAG-only role per CLAUDE.md; merge gate decided by orchestrator + owner read.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR152_2026-05-05.md` master `1603113` referencing PR #151 §"QC stream — what you audit")

5 audits — 3 standard + 2 NEW for 12.5E-E (trainer hyperparameter immutability, cleanup completeness).

PR #152 head: `acd9938a755b1538904860859abc83b0aaa5d2c0` (branch `programmer/phase125e-e-retrain-2026-05-05`). Merge-base: `31f2f74` (= PR #151 = 12.5E-E dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"7 files (3 new data/report + 4 modified); no model artifact (correctly absent per dispatch's < 33 threshold logic); no edits to existing source surfaces beyond `train_model_v9_student.py:1372` MEDIUM-2 cleanup"*

| File | additions | deletions | category |
|---|---|---|---|
| `data/corpus_combined_604_2026-05-05.jsonl` | (~604 rows) | 0 | NEW (merged situations) |
| `data/corpus_combined_604_labels_2026-05-05.jsonl` | (~604 rows) | 0 | NEW (merged labels) |
| `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` | (full report) | 0 | NEW (trainer report) |
| `river-rats-core/train_model_v9_student.py` | 21 | 5 | UPDATE (V-X4 cleanup + `--phase-label` arg) |
| `review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` | (3 NIT cleanups) | 3 | UPDATE |
| `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | 1 | 1 | UPDATE (T8 wording) |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | 2 | 1 | UPDATE (PILOT_595 + filename) |
| **Total** | **+1669** | **-14** | **7 files** ✓ |

- File count = 7 ✓ (matches dispatch's "7 files when model artifact absent per BLOCKED" path per PR #151 line 121)
- No `.json`/`.pkl`/`.pt` model artifact present ✓ (correctly absent per median 32 < 33)
- Existing source surfaces touched: only `river-rats-core/train_model_v9_student.py` (Path Y discipline holds — zero edits to `gto_model.py`, `feature_extractor.py`, `reference_evaluator.py`, `oracle_router.py`, `coaching/`, etc.) ✓

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

10 distinct cited paths in `PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md`:

| Citation | Status |
|---|---|
| `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125D_PRIME_DISPATCH_2026-05-04.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125E_E_DISPATCH_2026-05-05.md` | ✅ TRACKED |
| `river-rats-core/models/gto_model_v9_3way_v2.2.json` | ✅ TRACKED (warm-start anchor) |
| `river-rats-core/train_model_v9_student.py` | ✅ TRACKED |
| `data/corpus_combined_604_2026-05-05.jsonl` | NOT-TRACKED (NEW in PR; will track post-merge) ✓ expected |
| `data/corpus_combined_604_labels_2026-05-05.jsonl` | NOT-TRACKED (NEW in PR) ✓ expected |
| `river-rats-core/models/gto_model_v9_student.json` | NOT-TRACKED (correctly absent per no-promotion; cited as argparse default path) ✓ expected |
| `river-rats-core/models/gto_model_v8_38feat.json` | NOT-TRACKED (correctly absent per #PSH-01 canonicality guard) ✓ expected per Section A "DROPPED" status |

**Sanity-check on headline numerical claims:**

| Claim | Source | Verified |
|---|---|---|
| Master HEAD at run time: `31f2f74` | report line 13 | ✅ matches PR #151 = 12.5E-E dispatch SHA |
| Run timestamp: 2026-05-05T18:43:36Z | report line 13 | ✅ same-day, plausible |
| Chosen seed solver-corrected: 32/40 | report line 130 | ✅ matches orchestrator's status report |
| `nut_flush_block` importance: 0.0268 | report lines 168, 186 | ✅ above ml-architect's ≥0.02 prediction (Q4 H-FEAT confirmed) |

**Citation existence: CLEAN.**

## Audit 3 — Combined corpus integrity ✅ CLEAN

**Dispatch:** *"604 row count + cardinality checks; sample rows from each cohort parse cleanly"*

| Quantity | Observed | Expected |
|---|---|---|
| Combined situations rows | **604** | 604 ✓ |
| Combined labels rows | **604** | 604 ✓ |
| Unique `pilot_hand_id` (situations) | 604 | 604 ✓ |
| Unique `pilot_hand_id` (labels) | 604 | 604 ✓ |
| Situations ∩ labels | 604 | 604 ✓ (perfect join) |
| Situations \\ labels | 0 | 0 ✓ |
| Labels \\ situations | 0 | 0 ✓ |

### Cohort breakdown in combined situations

| Cohort | Source | Count in combined |
|---|---|---|
| Existing 494 (12.5D) | `corpus_revision_500_hand_2026-04-27.jsonl` | 494/494 ✓ |
| New parametric (12.5E-B) | `corpus_revision_125e_situations_2026-05-04.jsonl` | 96/96 ✓ |
| New manual canonicals (12.5E-B) | `corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` | 14/14 ✓ |

### Sample-row parse check (random sample per cohort)

| Cohort | Sample `pilot_hand_id` | Required fields present | Notes |
|---|---|---|---|
| old 494 | PILOT_348 | ✅ all (board, hero_cards, street, hero_position, feat_dict) | board=2sJcJh hero=6c5c street=flop |
| new par | PILOT_560 | ✅ all | board=Jh8h4d hero=AhQh street=flop |
| new man | PILOT_597 | ✅ all | board=9h6s2cJh hero=9c9d street=turn |

### Bonus check — combined corpus is exact byte-concat

Verified that `data/corpus_combined_604_2026-05-05.jsonl` = byte-exact concat of (`corpus_revision_500_hand_2026-04-27.jsonl` + `corpus_revision_125e_situations_2026-05-04.jsonl` + `corpus_revision_125e_manual_canonicals_2026-05-04.jsonl`). No transformation, no row reorder, no whitespace drift. ✅

**Combined corpus integrity: CLEAN.**

## Audit 4 (NEW) — Trainer hyperparameter immutability ✅ BIT-STABLE

**Dispatch:** *"diff `train_model_v9_student.py` against master HEAD `31f2f74`; only the MEDIUM-2 V-X4 cleanup at line 1371-1372 (and `--phase-label` parameterization) should differ; hyperparameter dict + cap=3.0 + seeds 0-4 + pre-pad metadata-only all unchanged"*

### Diff hunks (5 hunks total)

| Hunk lines | Function | Change |
|---|---|---|
| 926-940 | `write_report` (top) | `phase = getattr(cli_args, "phase_label", None) or "12.5D'"`; `status_line` + `topline` use `{phase}` |
| 940-951 | `write_report` (frontmatter) | re: line + heading use `{phase}` |
| 1369-1391 | `write_report` (footer) | **MEDIUM-2 V-X4 fix:** unconditional `f"**Status: 12.5D RUN COMPLETE. Median-litmus seed promoted to {student_output_path}"` → CONDITIONAL on `promoted` flag (true: "promoted to canonical"; false: "model NOT promoted... 12.5E-F gate decides next direction") |
| 1414 | `_build_argparse` | `--report` default updated `PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` → `PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` |
| 1426-1429 | `_build_argparse` | NEW: `--phase-label` argument (default "12.5E"; help text describes phase parameterization) |

### Hyperparameter immutability verification

Programmatic grep on the trainer diff for any line containing hyperparameter / sample_weight / pre-pad / warm-start tokens:

```
$ git diff $MB..pr-152-audit -- train_model_v9_student.py | grep -E "^[+-].*(cap|n_estimators|max_depth|learning_rate|early_stopping|subsample|colsample|min_child_weight|gamma|reg_alpha|reg_lambda|N_FEATURES_STUDENT|N_CLASSES|metadata_bump|seeds|sample_weight|class_weights|min\(3\.0|warm.*start)"
[no diff lines matching hyperparameters]

$ git diff $MB..pr-152-audit -- train_model_v9_student.py | grep -E "^[+-].*(warm.*start|metadata_bump|prepad|gto_model_v9_3way_v2.2)"
[only context lines mentioning warm-start anchor; no actual diff]
```

**Confirmed unchanged from 12.5D' baseline:**
- cap=3.0 hybrid weighting (per ml-architect Q3 spec)
- 5 seeds (0-4)
- 80/20 stratified split
- Multi:softprob 5-class objective
- Pre-pad metadata-only mechanism (warm-start anchor `gto_model_v9_3way_v2.2.json`)
- All hyperparameters in `_default_hyperparameters` dict (n_estimators, max_depth, learning_rate, early_stopping, subsample, colsample_bytree, min_child_weight, gamma, reg_alpha, reg_lambda)
- Sample-weight + class_weights computation (line 405-432 from PR #131)
- `_StudentInference` + `_evaluate_student_one_hand` (Path Y mirror)

**Trainer hyperparameter immutability: BIT-STABLE.** Authorized edits only (V-X4 cleanup + phase parameterization).

## Audit 5 (NEW) — Cleanup completeness ✅ 5/5 APPLIED (1 via annotation)

**Dispatch §"Step 4 cleanup":** 5 queued NIT items.

| # | Item | Target file | Verification | Status |
|---|---|---|---|---|
| 1 | MEDIUM-2 from PR #134 (V-X4 unconditional "promoted to /tmp/" footer) | `train_model_v9_student.py` line 1371 | Audit 4 confirmed: now CONDITIONAL on `promoted` flag with branch for not-promoted "model NOT promoted; 12.5E-F decides next direction" | ✅ FIXED |
| 2a | PR #134 NIT-1: "3 deliverable files + 1 BLOCKED comm" framing | `PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` | Updated stop-condition row: "4-file deliverable diff (3 deliverables + 1 BLOCKED comm; cleanup matched actual 4-file PR diff at PR #131 open time)" | ✅ FIXED |
| 2b | PR #134 NIT-2: References list cites old 12.5D dispatch (PR #125), not 12.5D' (PR #130) | same | Both now cited: 12.5D' dispatch (PR #130, master `1b95648` — "this run's actual dispatch") + 12.5D dispatch (PR #125, master `e3c0dfc` — "predecessor; original v9-student dispatch") | ✅ FIXED |
| 2c | PR #134 NIT-3: "Schema discoveries during 12.5D" → "during 12.5D'" | same | Heading updated: `### Schema discoveries surfaced during 12.5D'` | ✅ FIXED |
| 3 | PR #139 NIT-1: PLAN §3.T8 wording (36 design vs 22 dispatch) | `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | Original "36 sampled" wording PRESERVED + post-dispatch compression note added: "**Post-dispatch compression note (added at 12.5E-E cleanup per dispatch §'Step 4' NIT-1):** Phase 12.5E dispatch (PR #133) and 12.5E-B amendment (Path B / PR #137) compressed T8 to 22 hands..." | ✅ FIXED |
| 4 | PILOT_595 cosmetic: design_note "TPTK + nut blocker" → "top-two-pair + nut blocker" | `BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | **Annotation added** clarifying "TPTK wording is loose — hero AsKs on Ad8c2sQhKh river actually flops top-pair-Aces (As+Ad) AND pairs Kings on the river K (Ks+Kh) ⇒ top-two-pair, not TPTK" — substance captured. Original "TPTK" text in the design_note prose remains; clarification appears as separate paragraph. | ✅ APPLIED via annotation (see NIT-1) |
| 5 | PR #148 NIT-1: stale `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH` filename in §"What the BLOCKED PR ships" line 151 | same | Line 151 now reads `BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (with rename history annotation: "renamed at 12.5E-C amendment from `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_2026-05-05.md`...") | ✅ FIXED |

**Cleanup completeness: 5/5 items addressed substantively.** PILOT_595 fix-method differs from strict dispatch wording — see NIT-1.

## NIT-1 — PILOT_595 cleanup via annotation rather than replacement

**Evidence:** Dispatch §"Step 4 cleanup" line 78 specified the PILOT_595 fix as: *"design_note describes 'TPTK + nut blocker' — fix to 'top-two-pair + nut blocker'; bucket + labelling unchanged"*.

The diff applied is an ANNOTATION: a new paragraph added to the report that documents (a) the TPTK wording exists at `scripts/build_corpus_revision_125e_situations.py:1386`, (b) the wording is loose because the river K actually pairs both A and K, (c) the correct designation is top-two-pair. The original TPTK wording in the report's preserved §"Original §'What the BLOCKED PR ships' framing" + Section "Per-template consensus alignment" + design_note inlined elsewhere — wherever it appears — was NOT directly replaced with "top-two-pair + nut blocker."

**Substance vs strict-replacement:**
- Substance (recognition that TPTK is loose; top-two-pair is correct): captured ✓
- Strict dispatch wording ("fix to 'top-two-pair + nut blocker'"): could be read as direct replacement of the original TPTK string

**Why this is NIT not MEDIUM:** the annotation pattern is consistent with how the builder handled NIT-1 from PR #148 in the same report (preserve original + annotate). Reader understanding is preserved + improved (now sees both the original wording and why it's loose). The dispatch wording is satisfiable both ways.

**Suggested fix-forward (advisory, doesn't block):** if strict-replacement is preferred for future cleanup cycles, dispatch wording could be tightened to "edit design_note text from X to Y" vs "annotate design_note clarifying X is loose; correct designation is Y." Both are acceptable cleanup patterns; the dispatch wording as-written is ambiguous between them.

**Severity:** NIT.

## Bonus check — H-FEAT primary outcome empirically confirmed

ml-architect's 12.5D' Q4 prediction was that with corpus expansion (12.5E corpus revision), `nut_flush_block` importance should move from 0.0000 (in 12.5D' BLOCKED state) toward ≥0.02 if the H-FEAT diagnosis was correct. 12.5E-E result:

| feature | 12.5D' importance | 12.5E importance | direction |
|---|---|---|---|
| `nut_flush_block` | 0.0000 | **0.0268** | ✅ above ≥0.02 prediction; H-FEAT confirmed |

Other P1 blockers (per Section C of the new report):
- `flush_draw_block_pct`: 0.0040 → ?
- `straight_draw_block_pct`: 0.0086 → ?
- `nut_made_block_pct`: 0.0095 → ?

The full Section C delta is in the trainer report. Importance migration is the load-bearing diagnostic for the migration's premise; nut_flush_block specifically (the most poker-theoretically significant blocker per gto-expert 12.5D analysis) crossed the 1% threshold. **Path B / 12.5E migration premise empirically validated at the feature-importance layer.**

For the gate: median 32/40 < 33 promote threshold → BLOCKED at owner-tie-gate (31-32 band per inherited 12.5D' threshold table). 12.5E-F gate evaluation will produce the synthesis for owner WHAT decision (ship 32 / cap-retune at 12.5G / corpus expansion to 150-200 / abandon).

## What QC did NOT audit (scope partition)

QC's audit deliberately did NOT cover:

- **Per-hand poker correctness** of the 32 reference-set passes vs misses — gto-expert review scope at 12.5E-F. QC verifies aggregate gates + integrity; gto-expert verifies poker-theoretic correctness.
- **ml-architect 12.5E-F gate evaluation** (median 32 vs predicted 35-37; H-FEAT vs H-DIST confirmation; per-hand failure direction classification) — explicitly ml-architect's scope per dispatch line 36-39 of QC audit trigger comm.
- **TC-26 V-Integration-Trace on training run** — trainer code is bit-stable; no new fix-claim code path. Out of scope.
- **Owner WHAT decision pre-framing** — orchestrator scope at 12.5E-F synthesis.

## Test class implication

- **TC-23 (7-file-scope BLOCKED variant) demonstrated cleanly** — first activation on a re-train BLOCKED PR with cleanup-bundle scope. Pattern: data files + report + trainer (with strict immutability check) + cleanup edits collapse to 7 files; model artifact correctly absent on no-promotion.
- **TC-X-HYPERPARAMETER-IMMUTABILITY** sub-vector demonstrated — programmatic grep on diff for hyperparameter tokens; zero-diff threshold for "trainer reused unchanged from prior cycle" pattern. Useful for future re-train cycles where the trainer is stable.
- **TC-X-CLEANUP-COMPLETENESS** sub-vector demonstrated — verifies queued NIT items from prior cycle reviews were applied. Pattern: dispatch enumerates queued items; QC verifies one-by-one via diff inspection.
- **TC-X-CORPUS-CONCAT-EXACT** sub-vector demonstrated — when dispatch declares "merge X + Y + Z at file level (no transformation)", QC verifies the merged file is byte-exact concat of source files. Stronger than line-count check; catches subtle row-reorder or whitespace transformation.
- **PILOT_595 NIT-1 pattern (annotation vs replacement)** — interesting cleanup-style question. Dispatch wording can be ambiguous between "edit text" and "annotate explaining text is loose"; both achieve substance but dispatch tightening could disambiguate.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **6th successive cycle solo-routed**. Orchestrator dispatched via explicit fire-now trigger (PR #153, master `1603113`) per `feedback_explicit_action_trigger.md`; QC fired immediately on receipt. Clean two-phase orchestrator-→-QC handoff: dispatch (PR #151) → builder PR (#152) → audit-now trigger (PR #153) → QC verdict (this comm) → merge.

## References

- PR #152: https://github.com/beytell1-sketch/river-rats-v2/pull/152
- PR #152 head: `acd9938a755b1538904860859abc83b0aaa5d2c0`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR152_2026-05-05.md` (master `1603113`, PR #153)
- 12.5E-E dispatch: `MAIN_TERMINAL_PHASE125E_E_DISPATCH_2026-05-05.md` (master `31f2f74`, PR #151)
- 12.5E-D APPROVE: master `4070a11` (PR #150)
- Trainer report: `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` (in PR)
- Combined corpus: `data/corpus_combined_604_2026-05-05.jsonl` + `data/corpus_combined_604_labels_2026-05-05.jsonl` (in PR)
- Warm-start anchor: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (master, unchanged)
- Memory: `feedback_qc_routing_when_standalone_active.md` (6th cycle), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`

## Status

**APPROVE PR #152 for merge.** All 5 audits per current operative dispatch (PR #151 / trigger PR #153) PASS. 1 NIT-class advisory (PILOT_595 cleanup via annotation rather than replacement; substance captured).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5E-F dispatch (gate evaluation + ml-architect + gto-expert per-hand review)
- Owner WHAT decision at 12.5E-F: ship 32 / cap-retune at 12.5G / corpus expansion / abandon
