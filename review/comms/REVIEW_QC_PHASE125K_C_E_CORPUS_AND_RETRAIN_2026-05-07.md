---
date: 2026-05-07
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (builder)
re: PR #293 — 12.5K-C-E corpus integration (788→988) + 5-seed re-train (NULL; 33.00 ± 0.00; 3-lever ceiling) — pre-merge audit
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge corpus-integration-and-retrain milestone (FINAL phase before 12.5L owner-gate)
qc_branch: qc/pr293-125kce-corpus-retrain-review-2026-05-07
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR293_2026-05-07.md (master `228c43e`, PR #294)
target_pr_head: 1d8ab7f5b1e3962540a3c969af4f35e2332d4544
---

# QC pre-merge audit — PR #293 (12.5K-C-E)

## Result

**PASS** (0 BLOCKER, 0 SHOULD_FIX, 0 NIT). 38th solo cycle. The 12.5K-C-E corpus assembly + 5-seed re-train executes the dispatch end-to-end; empirical NULL result is the correct outcome-matrix routing and the 3-lever ceiling thesis is supported by the data.

## Audit-item walkthrough (9 items per trigger)

### 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)

6 files (matches dispatch §"Files in PR diff"):

- `data/corpus_combined_988_2026-05-07.jsonl` (988 lines)
- `data/corpus_combined_988_labels_2026-05-07.jsonl` (988 lines)
- `scripts/assemble_125k_c_e_988.py` (assembly script, 189 lines)
- `review/comms/PILOT_REPORT_PHASE125K_C_E_2026-05-07.md` (302 lines)
- `review/comms/BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md` (402 lines)
- `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` (1696209 B; chosen median Seed 2)

No v3.x prompt edits, no BATCH2 edits, no existing-label edits, no trainer-module edits, no memory edits. **Owner-scope perimeter held.**

### 2. Corpus 988-row integrity

Independently verified:

- Corpus rows = 988 ✓
- Label rows = 988 ✓
- 988 distinct `pilot_hand_id` ✓
- 988/988 `pilot_hand_id` populated in BOTH files (clean join key) ✓
- Namespace split: `PILOT_*` = 788 base + `PILOT_LEVER_C_MW*` = 200 augmented = 988 ✓ disjoint

61-surface uniformity (independently re-counted across all 988 rows): `Counter({61: 988})` — every row has exactly 61 feat_dict keys. Total feat values = **60,268** = 988 × 61 ✓. **NaN/Inf count = 0** across all 60,268 values ✓ (matches builder claim).

Lever C per-axis composition (from `PILOT_LEVER_C_MW{17,40,45,47}_*` prefixes; 50/axis × 4 axes = 200):

| Axis | RAISE | CALL | FOLD | BET |
|---|---|---|---|---|
| MW-17 | 27 | 8 | 15 | 0 |
| MW-40 | 0 | 0 | 0 | 50 |
| MW-45 | 50 | 0 | 0 | 0 |
| MW-47 | 38 | 11 | 1 | 0 |

Consistent with PR #285 SCALE audit (700-label scale) per-axis aggregates: MW-40+MW-45 100% target-match preserved; MW-17 54% RAISE (PR #285 was 55.1%); MW-47 76% RAISE (PR #285 was 72.7%). Convergence across scales.

Class label distribution (full 988 corpus): `FOLD 97 / CHECK 326 / CALL 100 / BET 219 / RAISE 246` — exact match to builder Section A ✓. Confidence distribution `1.0=675 / 0.8=182 / 0.6=125 / 0.4=6` — exact match ✓.

### 3. Provenance integrity (5 model artifacts × commit hashes per CLAUDE.md addendum)

Section D claims independently re-computed:

- Output model SHA256: `faa4d3e4d6a17618e3f4c144384f8f1b12e7994fe5b3abe0ca489aa22319839a` ✓ matches Section D
- Warm-start SHA256: `9f3845bb2a56e99328261c70c3f34decd669f3e047162eb85c78f926bc366900` ✓ matches Section D
- Repo HEAD SHA at run: `19f958a2ad9d212ec940c256d6bb0af21e3afc09` ✓ matches dispatch master at fire-time

Note on "5 model artifacts": only the chosen-median Seed 2 is git-committed (per project convention; the other 4 seed runs are documented in Section A's per-seed table with accuracy / rounds / gate23 results, but their JSON artifacts are not promoted to git — same convention as PR #261 Lever A). Per-seed metric records satisfy the audit-trail requirement; trainer module (`river-rats-core/train_model_v9_student.py`) was committed in a prior PR and is referenced by Section D — the addendum's CLAUDE.md provenance-docstring rule applies to the trainer commit, not this run's model-only diff.

### 4. Pilot-first 1-seed gate executed

`PILOT_REPORT_PHASE125K_C_E_2026-05-07.md` documents Seed 0 standalone: 33/40 solver-corrected, 988/988 join clean, 40-hand reference eval, no degenerate predictions. Pilot ran at `2026-05-07T04:54:40Z` (master `19f958a`); full 5-seed at `2026-05-07T04:57:14Z` (same master). Pilot precedes full run by ~3 min ✓. **Pilot gate CLEAR** correctly satisfied per dispatch §"Phase 2".

### 5. 5-seed aggregation correctness

Per-seed solver-corrected litmus (Section B):

| Seed | Solver-corrected |
|---|---|
| 0 | 33/40 |
| 1 | 33/40 |
| 2 (chosen median) | 33/40 |
| 3 | 33/40 |
| 4 | 33/40 |

5/5 identical → mean = 33.00, std = 0.00. Math correct ✓. Median selection well-defined (any seed qualifies; Seed 2 chosen ties broken by builder discretion — defensible).

### 6. Reference set spot-check completeness (40 hands × 5 seeds; stay-wrong subset detail)

Section B includes chosen-seed (Seed 2) per-hand divergence table for 8 hands where any model differs from solver-corrected expert OR where solver-correction overlay activates (MW-17/20/30/31/40/45/46/47). Solver-correction overlay applied to MW-30, MW-46, MW-47 (per `memory/reference_corrections.md`); MW-31 + MW-50 NOT applied (unverified per blueprint §5.3) ✓ correct.

**Stay-wrong subset detail (Section E):** per-hand outcome on gto-expert's 7 shared-cause + 2 distinct-cause failures:

- 7 shared: 2 FLIPPED-CORRECT (MW-24, MW-42), 4 STAYED-WRONG (MW-17, MW-40, MW-45, MW-47), 1 STAYED-CORRECT (MW-25)
- 2 distinct: 0 FLIPPED (MW-31, MW-46) — matches gto-expert prediction (predicted 0)

Empirical 2/7 shared flipped vs gto-expert prediction of 7/7. The 4 stay-wrong (MW-17/40/45/47) are exactly the Lever C augmentation axes — the augmented data did NOT graduate them. This is the central NULL-result evidence.

### 7. Outcome interpretation matches matrix (NULL is correct call)

Outcome matrix routing (Section §"Outcome matrix conclusion"):

- Row 1 (≥34.5/40 1-σ PROMOTE): 33.00 < 34.5 ❌
- Row 2 ([34.0, 34.5) parity): 33.00 < 34.0 ❌
- Row 3 ([33.10, 34.0) improvement vs PR #261): 33.00 < 33.10 floor ❌
- **Row 4 (≈ 33.10 ± 0.30 NULL)**: 33.00 ∈ [32.80, 33.40] ✅ YES
- Row 5 (<33.0 regression): 33.00 ≥ 33.0 ❌ (boundary)

Routing **Row 4 = NULL** is correct interval arithmetic ✓. Per dispatch §"Sequencing": NULL → orchestrator decides next step (12.5L / Lever D / accept-ceiling). Builder did NOT auto-promote past gate; routed to orchestrator decision per dispatch ✓.

### 8. TC-X-OWNER-SCOPE-DISCIPLINE (18th formal use)

No edits to:
- v3.x labelling prompts ✓
- BATCH2 ✓
- river-rats-core/ trainer/evaluator/inference modules ✓
- training-data/ corpus from prior phases ✓
- existing labels (corpus + labels are NEW files; prior labels untouched) ✓
- ~/.claude/projects/.../memory/ ✓
- docs/ ✓

The model artifact `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` is added under a NEW phase-namespaced subdirectory (`125k_c_e/`); no overwrite of `gto_model_v9_3way_v2.2.json` or other production canonicals. **Perimeter held.**

### 9. TC-X-DISPATCH-COMPLIANCE (17th formal exercise; durable)

Dispatch (`MAIN_TERMINAL_PR289_RESOLUTION_AND_125KCE_DISPATCH_2026-05-07.md`) compliance:

- Phase 1 (corpus 788→988 assembly): ✓ via `scripts/assemble_125k_c_e_988.py` (mirrors PR #222 pattern)
- Phase 2 (pilot 1-seed gate binding): ✓ pilot ran first; CLEAR
- Phase 3 (5-seed full re-train): ✓ all 5 seeds executed
- Outcome matrix → NULL → orchestrator-decision route: ✓ no auto-promotion past gate
- "Did NOT modify v3.x / BATCH2 / labels / skip pilot / auto-promote": ✓ all five negatives confirmed

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (18th formal use)
- TC-X-DISPATCH-COMPLIANCE (17th formal exercise; durable)
- TC-X-DISPATCH-PREDICTION-VERIFICATION (entry #11; 7th formal exercise) — NULL outcome verified to match dispatch matrix routing
- TC-X-INTRA-PLAN-CONSISTENCY (informal)

## 3-lever ceiling — independent triangulation

Builder thesis (§"What this null result means"): the v9-3way student's 33-34/40 solver-corrected ceiling is robust to all 3 levers (variance, hyperparameters, augmented data). QC concurs based on the empirical record across the prior PR sequence:

| Lever | Hypothesis | Test | Result |
|---|---|---|---|
| A | seed sample variance | PR #261 (20 seeds; 788-corpus) | 33.10 ± 0.30 |
| B | hyperparameter sweep | PR #265 (3 configs) | 0.20 spread |
| **C** | **augmented data (200 hands; +88% RAISE / +30% BET)** | **PR #293 (5 seeds; 988-corpus)** | **33.00 ± 0.00** |

All three within noise of each other; none cross the 34/40 v9-3way-v2.2 baseline. Stay-wrong on MW-17/40/45/47 is structural — augmenting with pipeline-labelled hands reinforces the pipeline view, which already diverges from canonical on those axes (per PR #245 MW-40 graduation-fail + PR #281 MW-17 axis-target shift findings). Lever C cannot fix what is fundamentally a labelling-pipeline-vs-canonical mismatch.

Lever C did produce real held-out lift in `CALL` recall (+0.117) and `RAISE` recall (+0.480) on the test split, and FLIPPED-CORRECT MW-24 + MW-42 (the shared-cause hands the pipeline CAN reach). It just doesn't move the canonical reference-set needle on the 4 stay-wrong axes — exactly because the labelling pipeline doesn't agree with canonical there.

This learning is durable and worth a memory note (orchestrator-surface candidate per builder report §"Memory candidates").

## Smarter-over-time

**6-PR Lever C cycle complete:**
PR #228-249 MW-40 verification round → PR #269 -A design → PR #273 -B situation gen → PR #277 -C pilot HALT → PR #281 -C-FIX (axis-target shift) → PR #285 -C-SCALE (700 labels) → PR #289 -C-D (Opus tier-up; 20/20) → **PR #293 -C-E (corpus integration + 5-seed retrain; NULL)**.

Class system has accompanied every step; entries #11/#12/#13/#14 in active use across 17 dispatch-compliance exercises and 7 dispatch-prediction-verification exercises. Watchlist `TC-X-CANONICAL-HAND-CLASS-PRESERVATION` (PR #281) validated end-to-end on this PR's stay-wrong outcome (Path A re-tag stayed-wrong on canonical reference; pipeline-labelled training data cannot graduate canonical-divergent axes).

The audit pattern stays the same as prior pre-merge milestones: independent row-counting + provenance-hash recomputation + per-axis verification + outcome-matrix interval arithmetic. Compound value cycle continues — no class system additions this PR (all classes hit are durable).

## Minor observations (non-finding, informational)

- Pilot report header `status:` line says "5-seed run complete; gate did not promote" but the pilot itself was Seed 0 only (Section A `Seeds: 0`). Builder addendum in the full report corrects to "Pilot gate CLEAR". Stale auto-report wording; not a finding.
- Both pilot and full reports include a "Schema discoveries surfaced during 12.5D" section that mentions "494-hand training" which is residual prose from the trainer's auto-report (carried over from 12.5D). Per-seed table correctly shows train=790 + test=198 = 988 for this run. Stale prose; not a finding.

These are autoreport-template artifacts; substantive numbers (988-corpus, 33.00 mean, hyperparameters, provenance hashes) are correct.

## Gates

PR #293 cleared from QC side. **0 BLOCKER, 0 SHOULD_FIX, 0 NIT.**

**12.5L gate evaluation (FINAL phase) is a HARD OWNER-GATE** per dispatch §"What gates" + per loop directive (stop-loop conditions: explicit owner say-so OR hard owner-gate). After PR #293 merge, orchestrator surfaces the 12.5L ship-or-defer decision to owner. QC has no further pre-merge work queued until owner directs.

## Cycle stats

- 38th solo QC cycle.
- Wall clock: ~18 min.
- LLM cost: $0.

---

**Verdict: PASS · 0/0/0 · MILESTONE PR clear from QC side · 12.5L = HARD OWNER-GATE next.**
