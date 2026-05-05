---
date: 2026-05-05
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #157 (12.5G cap=4.0 retune — cap-as-lever empirically refuted; BLOCKED median 32 → 12.5H route) — APPROVE; 0 NIT
severity: no findings; clean approval
status: FLAG → APPROVE for merge
test-class: TC-23 (diff scope) + V-Source (citation existence) + dispatch §"NEW: cap value verification" + §"NEW: corpus invariance" + dispatch §"Cap parameterization minimal"
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 7th successive cycle solo-routed)
---

# QC Review — PR #157 (12.5G cap=4.0 retune): APPROVE; 0 NIT

## Verdict

**APPROVE PR #157 for merge.** All 5 dispatch-required audits clear cleanly. Trainer parameterization is minimal (default 3.0 = backward-compatible); cap=4.0 documented in Section A; corpus + labels byte-identical to 12.5E-E across master + PR head; trainer report correctly characterizes cap-non-binding empirical finding.

12.5G is a BLOCKED PR (median 32/40 < 33 promote threshold; no model artifact). The empirical finding — cap-as-lever non-binding given post-12.5E corpus class distribution — is itself load-bearing for the 12.5H corpus expansion direction. Trainer report Section F captures the math + decisive evidence.

QC FLAG-only role per CLAUDE.md; merge gate decided by orchestrator; 12.5H dispatches on merge.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR157_2026-05-05.md` master `89d75da` + PR #156 dispatch)

5 audits — 3 standard (diff scope, citation existence, parameterization minimal) + 2 NEW for 12.5G (cap value verification, corpus invariance).

PR #157 head: `7a7cc2cd86ec42d6c580e3a6d637a8bfe8da0fe1` (branch `programmer/phase125g-cap-retune-2026-05-05`). Merge-base: `1bd464e` (= PR #156 = 12.5G dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Trigger:** *"3 files (BLOCKED comm + trainer report + parameterized trainer; no model artifact per dispatch's no-promotion fallback at median 32 < 33)"*

| File | additions | deletions | category |
|---|---|---|---|
| `river-rats-core/train_model_v9_student.py` | 13 | 5 | UPDATE (cap parameterization) |
| `review/comms/PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` | 418 | 0 | NEW (trainer report) |
| `review/comms/BUILDER_BLOCKED_PHASE125G_CAP_NON_BINDING_2026-05-05.md` | 108 | 0 | NEW (BLOCKED comm) |
| **Total** | **+539** | **-5** | **3 files** ✓ |

- File count = 3 ✓ (matches trigger; under dispatch's stop condition `>5 files → STOP`)
- No `.json` / `.pkl` / `.pt` model artifact present ✓ (correctly absent per median 32 < 33)
- Existing source surfaces touched: only `river-rats-core/train_model_v9_student.py` (Path Y discipline holds — zero edits to `gto_model.py`, `feature_extractor.py`, `reference_evaluator.py`, etc.) ✓
- Combined corpus + label files NOT in diff ✓ (per dispatch §"What you do NOT do" — UNCHANGED files; corpus invariance is Audit 5)

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

8 distinct cited paths in `PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md`:

| Citation | Status | Notes |
|---|---|---|
| `data/corpus_combined_604_2026-05-05.jsonl` | ✅ TRACKED | unchanged from 12.5E-E |
| `data/corpus_combined_604_labels_2026-05-05.jsonl` | ✅ TRACKED | unchanged from 12.5E-E |
| `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` | ✅ TRACKED | blueprint anchor |
| `review/comms/MAIN_TERMINAL_PHASE125D_DISPATCH_2026-05-03.md` | ✅ TRACKED | predecessor dispatch |
| `river-rats-core/models/gto_model_v9_3way_v2.2.json` | ✅ TRACKED | warm-start anchor |
| `river-rats-core/train_model_v9_student.py` | ✅ TRACKED | this PR's edit target |
| `river-rats-core/models/gto_model_v8_38feat.json` | NOT-TRACKED | correctly absent per #PSH-01 canonicality guard ✓ expected |
| `river-rats-core/models/gto_model_v9_student.json` | NOT-TRACKED | correctly absent per no-promotion (cited as argparse default path) ✓ expected |

**Citation existence: CLEAN.**

## Audit 3 — Cap parameterization minimal ✅ CLEAN

**Dispatch line 17:** *"diff `train_model_v9_student.py` against master `16351e1`; only parameterization changes (line 422 + argparse + report writer); zero other hyperparameter diffs"*

### 5-hunk diff scope

| Hunk lines | Function | Change |
|---|---|---|
| 403-404 | `train_one_seed` signature | adds `class_weight_cap: float = 3.0` kwarg (default = 12.5D'/12.5E backward-compatible) |
| 414-422 | `train_one_seed` body | comment update reflecting parameterization; `min(3.0, ...)` → `min(class_weight_cap, ...)` (line 422 per dispatch) |
| 962 | `write_report` Section A | emits `f"- Class-weight cap (hybrid): \`{...}\`"` |
| 1428-1432 | `_build_argparse` | adds `--class-weight-cap` CLI arg (default 3.0) with help text |
| 1526 | `main` | passes `args.class_weight_cap=args.class_weight_cap` to `train_one_seed` |

### Hyperparameter immutability check (programmatic grep)

```
$ git diff $MB..pr-157-audit -- train_model_v9_student.py | grep -E "^[+-].*(n_estimators|max_depth|learning_rate|early_stopping|subsample|colsample|min_child_weight|gamma|reg_alpha|reg_lambda|seeds|metadata_bump|warm.*start)"
[no diff lines matching unmodified hyperparameters]
```

**Confirmed unchanged from 12.5E-E baseline:**
- Hyperparameter dict (n_estimators, max_depth, learning_rate, etc.) — all unchanged
- 5 seeds (0-4) — unchanged
- 80/20 stratified split — unchanged
- Pre-pad metadata-only mechanism — unchanged
- Warm-start anchor `gto_model_v9_3way_v2.2.json` — unchanged
- `_StudentInference` + `_evaluate_student_one_hand` (Path Y mirror) — unchanged

**Parameterization is minimal.** Default 3.0 preserves 12.5D'/12.5E behavior when `--class-weight-cap` is not specified. Backward-compatible.

**Cap parameterization minimal: CLEAN.**

## Audit 4 (NEW) — Cap value verification ✅ CLEAN

**Dispatch line 18:** *"verify trainer ran with `--class-weight-cap 4.0`; cap value documented in Section A"*

PROGRAMMER_REPORT line 26 (Section A — training metadata):

> `- Class-weight cap (hybrid): \`4.0\``

✓ Cap=4.0 documented in Section A as required.

Cross-reference: Section F (12.5G-specific delta) at lines 332+ contains the load-bearing empirical evidence:

> *"12.5G is the cap=4.0 retune (B-then-C step 1 per `MAIN_TERMINAL_PHASE125G_DISPATCH_2026-05-05.md`). Identical to 12.5E-E except `--class-weight-cap` parameterized from default 3.0 → 4.0 via the new CLI arg."*

> *"The cap is non-binding at both 3.0 and 4.0. On the 604-hand combined corpus, the natural per-class inverse-frequency boosts (mean / class_count) are all below 3.0 ... changing the cap from 3.0 → 4.0 is mathematically a no-op on this corpus."*

The report carefully distinguishes historical references (lines 241 + 312 mention "cap 3.0" in the inherited Section E delta-baseline-comparison context against 12.5D — these are correct historical anchors, not stale claims about the current run).

**Cap value verification: CLEAN.**

## Audit 5 (NEW) — Corpus invariance ✅ BYTE-IDENTICAL across phases

**Dispatch line 19:** *"verify combined 604-hand corpus + labels are byte-identical to 12.5E-E (master `b51e525`); no corpus tampering"*

| File | line count | sha256 (12.5E-E `b51e525`) | sha256 (PR #157 head) | sha256 (master HEAD) | match |
|---|---|---|---|---|---|
| `corpus_combined_604_2026-05-05.jsonl` | 604 | `ebfeebb0...169d0ae5` | `ebfeebb0...169d0ae5` | `ebfeebb0...169d0ae5` | ✅ **BYTE-IDENTICAL** across all three |
| `corpus_combined_604_labels_2026-05-05.jsonl` | 604 | `3edb3576...0663d60` | `3edb3576...0663d60` | `3edb3576...0663d60` | ✅ **BYTE-IDENTICAL** across all three |

Zero corpus tampering between 12.5E-E and 12.5G. The 12.5G run used the EXACT same training data as 12.5E-E — only the cap hyperparameter differed (3.0 → 4.0). This isolates cap as the only experimental variable, which is exactly what a cap-retune sweep requires.

**Corpus invariance: BYTE-IDENTICAL across phases.**

## Bonus: empirical finding cross-validates QC's just-queued TC-X-CAP-BINDING-PRE-CHECK

The 12.5G outcome empirically validates the test class QC queued earlier today (commit `7354fad` on QC repo, before this audit fired):

**TC-X-CAP-BINDING-PRE-CHECK** (queued 2026-05-05 in `~/river-rats-qc/learning/test_class_registry.md`): *"When a dispatch prescribes a cap-sweep on hybrid-class-weighting, QC pre-flights `mean(class_counts) / min(class_counts)` against cap-floor of sweep range. If value < cap-floor, FLAG as cap-non-binding."*

PR #157's Section F provides the math:
- 604-hand combined corpus class counts: CHECK 271 / BET 118 / FOLD 75 / CALL 72 / RAISE 68
- Mean class_count = 604/5 = 120.8
- Min class_count (RAISE) = 68
- Max natural per-class boost = 120.8 / 68 = **1.776×**
- 1.776× < cap=3.0 floor → **cap-non-binding**

If TC-X-CAP-BINDING-PRE-CHECK had been active when 12.5G dispatched, the pre-flight would have produced this exact arithmetic and flagged cap-non-binding immediately. The 12.5G run produced empirical confirmation of what the pre-check would have predicted from corpus statistics alone.

**This is an excellent first validation of the test class.** The class is forward-active for any future cap-tuning dispatch (12.5G' or beyond).

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of 12.5G outcomes — out of scope; 12.5G is mathematically equivalent to 12.5E-E per cap-non-binding evidence
- **5-seed cross-seed feature-importance** (which the orchestrator flagged as informative for TC-X-CROSS-SEED-IMPORTANCE) — the trainer report still emits chosen-seed importance per existing `write_report` contract. Cross-seed enrichment is forward-only per QC's queued curative; not a HOLD on PR #157.
- **12.5H corpus expansion design** — orchestrator scope; will fold cap-non-binding evidence + cross-seed importance reporting requirement into 12.5H dispatch per trigger comm line 41

## Test class implication

- **TC-X-CAP-BINDING-PRE-CHECK first validation** — empirically validated via 12.5G outcome arithmetic; class is forward-active.
- **TC-X-HYPERPARAMETER-IMMUTABILITY (from PR #152)** demonstrated again — programmatic grep on diff for hyperparameter tokens; pattern stable.
- **TC-23 minimal-parameterization sub-vector** — cap parameterization is a clean example: signature kwarg + body update + argparse + report-writer + main, 5 hunks, default-preserves-backward-compat. Pattern reproducible for future small-edit / parameterization PRs.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **7th successive cycle solo-routed**. Orchestrator dispatched via explicit fire-now trigger PR #158 (master `89d75da`) per `feedback_explicit_action_trigger.md`; QC fired immediately on receipt. Trigger comm acknowledged QC's just-queued institutional memory entries (TC-X-CAP-BINDING-PRE-CHECK + TC-X-CROSS-SEED-IMPORTANCE) as "good-quality additions" — feedback loop on QC self-curation working.

## References

- PR #157: https://github.com/beytell1-sketch/river-rats-v2/pull/157
- PR #157 head: `7a7cc2cd86ec42d6c580e3a6d637a8bfe8da0fe1`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR157_2026-05-05.md` (master `89d75da`, PR #158)
- 12.5G dispatch: `MAIN_TERMINAL_PHASE125G_DISPATCH_2026-05-05.md` (master `1bd464e`, PR #156)
- 12.5E-F synthesis: master `16351e1` (PR #155)
- 12.5E-E re-train (corpus origin): master `b51e525` (PR #152)
- QC institutional memory commit (TC-X-CAP-BINDING-PRE-CHECK + TC-X-CROSS-SEED-IMPORTANCE): `7354fad` on `~/river-rats-qc/`
- Memory: `feedback_qc_routing_when_standalone_active.md` (7th cycle), `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`

## Status

**APPROVE PR #157 for merge.** All 5 audits PASS; 0 NIT. Cleanest QC verdict in this cycle (PR #157 was a small parameterization edit + clean empirical retune; no V-X4 family issues; no cleanup-completeness questions; no schema gaps).

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H dispatch (corpus expansion — B-then-C step 2)
- 12.5H trainer report spec to fold cross-seed importance reporting requirement (per QC's queued TC-X-CROSS-SEED-IMPORTANCE)
- 12.5H+ dispatch spec to fold cap-binding pre-flight check (per QC's queued TC-X-CAP-BINDING-PRE-CHECK)
