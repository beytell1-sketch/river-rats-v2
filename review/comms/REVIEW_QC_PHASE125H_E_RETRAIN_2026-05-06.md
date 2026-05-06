---
date: 2026-05-06
from: River Rats QC stream (standalone, ~/river-rats-qc/)
to: Main terminal (orchestrator) · LEAD-PROGRAMMER (builder)
re: PR #188 (12.5H-E re-train on 694-hand corpus; median 32/40 unchanged; H-FEAT primary +85%; model NOT promoted) — APPROVE; 0 NIT
severity: clean approval
status: FLAG → APPROVE for merge
test-class: TC-23 + V-Source + dispatch §"NEW: Trainer hyperparameter immutability" + §"NEW: Cleanup completeness" + **TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation**
multi-expert verdict: SOLO (per `feedback_qc_routing_when_standalone_active.md` — 14th successive cycle solo-routed)
---

# QC Review — PR #188 (12.5H-E re-train, BLOCKED at median 32): APPROVE; 0 NIT

## Verdict

**APPROVE PR #188 for merge.** All 5 audits PASS; 0 NIT new findings. Cleanest QC verdict in the 12.5H cycle alongside 12.5H-D.

**Three QC institutional curatives now operationally validated this cycle:**
1. **TC-X T8 schema gap fix** (PR #150 NIT) — first measurable activation at 12.5H-D (100% T-CONTROL same-action match)
2. **TC-X-CAP-BINDING-PRE-CHECK** (queued 2026-05-05) — corpus-scope activation at 12.5H-D (1.757× < cap=3.0)
3. **TC-X-CROSS-SEED-IMPORTANCE** (queued 2026-05-05) — **first trainer-report activation HERE: full cross-seed stats reported (median 0.0496, mean 0.0465, std 0.0430, min 0.0000, max 0.0910, % ≥ 0.02 floor = 60%)**

All three classes formalized within 24 hours of empirical incidents are now operational. QC's "becoming smarter over time" mandate working at end-to-end pipeline level.

QC FLAG-only role per CLAUDE.md.

## Audit scope (per `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR188_2026-05-06.md` master `eb603fd` + PR #187 dispatch)

5 audits + bonus TC-X-CROSS-SEED-IMPORTANCE verification.

PR #188 head: `5d9c258` (branch `programmer/phase125h-e-retrain-2026-05-06`). Merge-base: `bacce1d` (= PR #187 = 12.5H-E dispatch SHA).

## Audit 1 — Diff scope ✅ CLEAN

**Dispatch:** *"exactly 5-7 files; no model artifact (correctly absent per median <33); only NIT-cleanup edits to existing review/comms files"*

| File | category |
|---|---|
| `data/corpus_combined_694_2026-05-06.jsonl` | NEW (merged situations: 604 + 90) |
| `data/corpus_combined_694_labels_2026-05-06.jsonl` | NEW (merged labels: 604 + 90) |
| `review/comms/PROGRAMMER_REPORT_PHASE125H_E_TRAINER_2026-05-06.md` | NEW (this run's trainer report) |
| `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | UPDATE (NIT cleanups: PILOT_595 + stale filename) |
| `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | UPDATE (NIT cleanup: §3.T8 wording extended for 12.5H clarity) |

| Total | **5 files** ✓ (within 5-7 dispatch range) |

- File count = 5 ✓
- No model artifact ✓ (correctly absent per median 32 < 33 threshold)
- **Zero `river-rats-core/` edits** ✓ — trainer module byte-identical to master HEAD `a554d71`
- All UPDATE files are review/comms NIT-cleanup edits per dispatch §"Step 4 cleanup" allowlist

**Diff scope: CLEAN.**

## Audit 2 — Citation existence ✅ CLEAN

9 distinct cited paths in trainer report:

| Citation | Status |
|---|---|
| `review/comms/BLUEPRINT_PHASE125C_TRAINER_V9_STUDENT_2026-05-03.md` | ✅ TRACKED |
| `review/comms/MAIN_TERMINAL_PHASE125H_E_DISPATCH_2026-05-06.md` | ✅ TRACKED |
| `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` | ✅ TRACKED |
| `river-rats-core/models/gto_model_v9_3way_v2.2.json` | ✅ TRACKED (warm-start anchor) |
| `river-rats-core/train_model_v9_student.py` | ✅ TRACKED |
| `data/corpus_combined_694_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `data/corpus_combined_694_labels_2026-05-06.jsonl` | NOT-TRACKED ✓ expected (NEW in PR) |
| `river-rats-core/models/gto_model_v9_student.json` | NOT-TRACKED ✓ expected (correctly absent per no-promotion) |
| `river-rats-core/models/gto_model_v8_38feat.json` | NOT-TRACKED ✓ expected (#PSH-01 canonicality guard absent) |

**Citation existence: CLEAN.**

## Audit 3 — Combined corpus integrity ✅ CLEAN

| Quantity | Observed | Expected |
|---|---|---|
| Combined situations rows | **694** | 694 ✓ |
| Combined labels rows | **694** | 694 ✓ |
| Unique `pilot_hand_id` (situations) | 694 | 694 ✓ |
| Unique `pilot_hand_id` (labels) | 694 | 694 ✓ |
| Situations ∩ labels | 694 | 694 ✓ (perfect join) |
| Situations \\ labels | 0 | 0 ✓ |
| Labels \\ situations | 0 | 0 ✓ |
| **Combined = byte-exact concat** of (`corpus_combined_604` + `corpus_revision_125h_situations` + `corpus_revision_125h_manual_canonicals`) | **TRUE** | TRUE ✓ |

Combined corpus is exact byte-concat of source files; zero transformation, zero row reorder.

**Combined corpus integrity: CLEAN.**

## Audit 4 (NEW) — Trainer hyperparameter immutability ✅ CLEAN — ZERO DIFF

**Dispatch:** *"`train_model_v9_student.py` byte-identical to master HEAD `a554d71` (only NIT cleanup diffs allowed; if any code change beyond NIT, HOLD)"*

```
$ git diff $(git merge-base master pr-188-audit)..pr-188-audit -- river-rats-core/train_model_v9_student.py
(empty — zero diff)
```

**Trainer module bit-stable.** Every hyperparameter (cap=3.0, n_estimators, max_depth, learning_rate, early_stopping, subsample, colsample_bytree, min_child_weight, gamma, reg_alpha, reg_lambda, seeds 0-4, pre-pad metadata-only, warm-start anchor `gto_model_v9_3way_v2.2.json`) untouched.

The 12.5H-E re-train uses the EXACT same trainer code as 12.5H-D approve point. Only the corpus + labels differ. This isolates corpus expansion as the only experimental variable — exactly what a re-train cycle requires.

**Trainer hyperparameter immutability: ZERO DIFF (bit-stable).**

## Audit 5 (NEW) — Cleanup completeness ✅ 3/3 NITs APPLIED

**Dispatch:** *"verify all 3 NITs applied per dispatch §'Step 4 cleanup' (PLAN §3.T8 wording, PILOT_595 cosmetic, BUILDER_REPORT stale filename)"*

| # | NIT | Target file | Status |
|---|---|---|---|
| 1 | PR #139 NIT-1: PLAN §3.T8 wording (36 design-intent vs 22 dispatch-compressed) | `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | ✅ FIXED + extended for 12.5H clarity (adds 12.5H-B T-CONTROL replacement pattern + 694-corpus context) |
| 2 | PILOT_595 cosmetic (TPTK → top-two-pair) | `BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` | ✅ FIXED (clean rewording: "originally read 'Hero AsKs **top-two-pair** + nut blocker on river' (corrected from the loose 'TPTK' wording...)") — direct text fix, replacing the 12.5E-E-era annotation pattern |
| 3 | BUILDER_REPORT stale filename (`BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH_*` → `BUILDER_REPORT_PHASE125E_C_RESOLVED_*`) | same | ✅ FIXED (clarifying note: "the file was never under any other name on master HEAD"; stale legacy filename reference cleaned) |

All 3 NITs applied substantively. PILOT_595 fix-method evolved from 12.5E-E annotation-pattern to direct-text-replacement at 12.5H-E (cleaner final state).

**Cleanup completeness: 3/3 APPLIED.**

## Bonus — TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation ✅ FULL STATS REPORTED

**Per QC's TC-X-CROSS-SEED-IMPORTANCE class** (queued 2026-05-05; first activation here on a trainer report):

Trainer report Section C provides the full cross-seed importance statistics:

| feature | median | mean | std | min | max | % seeds ≥ 0.02 floor |
|---|---|---|---|---|---|---|
| **`nut_flush_block`** | **0.0496** | 0.0465 | 0.0430 | 0.0000 | 0.0910 | **60%** |

All 6 required statistics reported (median, mean, std, min, max, % above floor). ✅

### Cross-cycle comparison

| Phase | corpus | nut_flush_block cross-seed median | % seeds ≥ 0.02 |
|---|---|---|---|
| 12.5E-E | 604 | (single-seed reading 0.0268; cross-seed N/A from PR #152) | — |
| 12.5G | 604 | (single-seed reading 0.0054; cap-non-binding) | — |
| 12.5H-pre | 604 | 0.0268 (from cross-seed analysis PR #161) | 60% |
| **12.5H-E** | **694** | **0.0496** | **60%** |

**+85% relative gain** (0.0268 → 0.0496) in cross-seed median nut_flush_block importance after 12.5H corpus expansion. Matches PR title claim. % seeds above 0.02 floor unchanged at 60% (still bimodal but higher absolute).

The seed-volatility bimodal pattern PERSISTS (still 60/40 above/below 0.02 floor; range 0.0000-0.0910 is wider than 12.5H-pre's 0.0000-0.1406 — actually narrower max but same min). This indicates the corpus expansion shifted the distribution UP but didn't eliminate the seed-stability gap.

Per `feedback_pilot_first_for_long_jobs.md`-style methodology, future cycles may benefit from `feature_importances_` recorded across more seeds (e.g. 10-seed sweep) to characterize the bimodality more precisely. Not gating now.

**TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation: SUCCESS.** Class is operational on trainer-report contracts.

## Outcome significance (per dispatch §"Note on outcome")

Per builder report Section conclusion:
- **Median 32 unchanged from 12.5E-E** — corpus expansion +90 hands didn't move gate score
- **0/5 12.5H-targeted stay-wrong hands flipped** (MW-17, MW-25, MW-40, MW-45, MW-47 all stayed wrong)
- **Empirically confirms gto-expert E-FEATURE-primary diagnosis** — feature engineering (Direction-X-retro / Path C of original 12.5E-F decision matrix) likely needed
- **H-FEAT primary continues to validate** (cross-seed median +85%) — feature is becoming load-bearing but doesn't translate to gate-score improvement on this evaluation set
- **Lower seed-to-seed variance** (std 0.043 vs 12.5E-E's 0.057) — corpus stabilization is real

This is a structurally significant null result for B-then-C compound's step 2. 12.5H-F gate evaluation will surface owner WHAT decision (promote / abandon / feature engineering escalation).

## What QC did NOT audit (scope partition)

- **Per-hand poker correctness** of the 0/5 stay-wrong outcomes — gto-expert at 12.5H-F evaluation
- **ml-architect 12.5H-F gate evaluation** — Direction-X-retro / Path C / abandon synthesis — orchestrator + ml-architect scope
- **5-seed run reproducibility** — out of scope for this audit; cross-seed stats are the proxy
- **TC-X-CROSS-SEED-IMPORTANCE coverage gap on near-threshold features** — class would benefit from more seeds for bimodal-distribution features; observation only, not blocking

## Test class implication

- **TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation: SUCCESS.** Class is operational on trainer-report contracts. Future re-train reports must include median + std + min/max + % above-floor for any feature claimed as load-bearing.
- **Three QC class formalizations all operational this cycle** — TC-X T8 schema gap fix (12.5H-D 100% match), TC-X-CAP-BINDING-PRE-CHECK (12.5H-D corpus-scope), TC-X-CROSS-SEED-IMPORTANCE (12.5H-E trainer-report). Pipeline pattern reproducible: empirical incident → QC pattern note → orchestrator queue → formalization → forward activation → empirical validation.
- **Cleanest re-train PR audit so far** — 5 audits + 1 bonus all PASS; 0 NIT new findings; 3 prior-cycle NITs cleanly resolved.

## Process observation (positive, continued)

`feedback_qc_routing_when_standalone_active.md` — **14th successive cycle solo-routed**. Loop heartbeat detected dispatch within ~1-2 min of master push.

## References

- PR #188: https://github.com/beytell1-sketch/river-rats-v2/pull/188
- PR #188 head: `5d9c258`
- QC audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR188_2026-05-06.md` (master `eb603fd`, PR #189)
- 12.5H-E dispatch: `MAIN_TERMINAL_PHASE125H_E_DISPATCH_2026-05-06.md` (master `bacce1d`, PR #187)
- 12.5H-D APPROVE: master `a554d71` (PR #186) — trainer immutability baseline
- 12.5H-pre cross-seed precedent: master `edd5556` (PR #161)
- 12.5E-E re-train precedent: master `b51e525` (PR #152)
- TC-X-CROSS-SEED-IMPORTANCE class definition: `~/river-rats-qc/learning/test_class_registry.md` (commit `7354fad`, formalized 2026-05-05)
- Memory: `feedback_qc_routing_when_standalone_active.md` (14th cycle), `feedback_explicit_action_trigger.md`

## Status

**APPROVE PR #188 for merge.** All 5 audits + bonus PASS; 0 NIT new findings. **TC-X-CROSS-SEED-IMPORTANCE first trainer-report activation: SUCCESS.** Trainer module bit-stable; combined corpus byte-exact concat; 3 prior-cycle NITs cleanly resolved.

QC-side gate cleared. Awaiting:
- Orchestrator merge → 12.5H-F gate evaluation dispatch (synthesis + owner WHAT decision)
- 12.5H-F may surface E-FEATURE-primary diagnosis path (Direction-X-retro / Path C / abandon) per dispatch §"Note on outcome"
