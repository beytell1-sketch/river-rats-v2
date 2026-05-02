---
date: 2026-05-02
from: Main terminal (orchestrator)
to: ML-ARCHITECT (named author, 12.5A) · LEAD-PROGRAMMER · QC stream · Owner
re: Phase 12.5 kickoff — v9 student trainer extension (operational, owner sign-off received)
status: DIRECTIVE — Phase 12.5A ML design dispatch; full Section 6 sequence follows
---

# Phase 12.5 kickoff — operational

## Authorization chain

- Owner sign-off received 2026-05-02 on `SHARED_STATE_BASELINE_2026-05-02.md` (PR #108).
- Sign-off covers S-1 (gap rationale), S-2 (orchestrator role-assignment for this terminal), and S-3 (Phase 12.5 kickoff scope: D-2 sequence + D-3 commitments + D-4/D-5/D-6 process additions).
- Orchestrator-named-author rule applies (per `feedback_listen_to_orchestrator_always.md`).
- This is **operational**, not a proposal. ML-ARCHITECT is the named 12.5A author and is authorised to begin 12.5A immediately on receipt of this comm.

## Why Phase 12.5 exists

Phase 12 trainer directive (PR #104, master `14c2db1`) is superseded.
Three-way Phase 0 alignment (PRs #105, #106, #107, synthesised in
#108) established that `river-rats-core/train_model.py` master HEAD
is incompatible with the Phase 12 invocation along 9 axes: no
argparse / CSV-only / no warm-start / single-seed / per-class
weighting / `FEATURE_COLUMNS=55` not 59 / cited reference set
doesn't exist / `ref_id` join key undefined / 4 v2.4 P1 blockers
not propagated. Phase 12.5 restores `PROCESS_GUIDE.md` §6 Step 1
(ML design before code) which Phase 12 skipped.

## Phase 12.5 sequence (full Section 6 mandatory training team)

| Phase | Author | Output | Gate |
|-------|--------|--------|------|
| **12.5A** | **ML-ARCHITECT** | `PLAN_PHASE125A_TRAINER_DESIGN_2026-05-XX.md` (design doc, no code) | Owner approval (12.5B) |
| 12.5B | Owner | Approval comm or redirect | Architect dispatch |
| 12.5C | ARCHITECT | `BLUEPRINT_PHASE125C_TRAINER_2026-05-XX.md` (exact insertion points + line numbers) | Owner approval |
| 12.5D | LEAD-PROGRAMMER | Trainer code in `river-rats-core/`, training run, `PROGRAMMER_REPORT_PHASE125D_TRAINER_2026-05-XX.md` | Round 12 review chain (12.5E) |
| 12.5E | ML-architect + GTO-expert + QC (review) | `REVIEW_*_PR<N>_*.md` × 3, plus reviewer Gates 2.3 + 2.4 | Owner ship gate |
| 12.5F | Owner | Model promotion to production | — |

This kickoff dispatches **12.5A only**. Subsequent phases dispatch
on their own gates.

## 12.5A — ML-architect scope

### Mandate

Read master HEAD source end-to-end (no skim), audit
`training-data/` for canonical reference-set candidates, design the
trainer extension. Produce a single design comm with a clear
recommendation on each of the six items below — **no menus, no
"open questions for owner"**, per `PROCESS_GUIDE.md` §1.4 and
`feedback_quality_default_no_ask.md`.

### Mandatory source files to read

- `river-rats-core/train_model.py` (511 lines, master HEAD)
- `river-rats-core/gto_model.py` (FEATURE_COLUMNS at lines 33–62; `N_FEATURES = 55` at line 64)
- `river-rats-core/feature_keys.py:87–92` (4 v2.4 P1 blocker features: `nut_flush_block`, `flush_draw_block_pct`, `straight_draw_block_pct`, `nut_made_block_pct`)
- `river-rats-core/feature_extractor.py` (extraction pipeline; produces 59-key `feat_dict`)
- `scripts/verify_feature_schema_compatibility.py:33–42` (correct `55 + 4 = 59` math)
- `data/corpus_revision_500_hand_2026-04-27.jsonl` (sample first 3 rows for schema)
- `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (sample first 3 rows for schema)
- `river-rats-core/models/gto_model_v9_baseline_45feat.json` (warm-start anchor; inspect feature-name list and tree-count)
- `docs/PROCESS_GUIDE.md` §6 (mandatory training team) and §2 (quality gates)
- `CLAUDE.md` §6 + 2026-04-15 training-provenance addendum

### Six items 12.5A must commit to (each with reasoning)

#### Item 1 — Trainer module location

Decide: (a) extend `train_model.py` in place (sacred-core edit;
single source of truth for "the trainer"), OR (b) author new
`river-rats-core/train_model_v9_student.py` (per `CLAUDE.md` §6
training-provenance addendum: "Every model-producing script
(trainer, evaluator) must live in `river-rats-core/` with a
provenance docstring linking its commit to the model artifact it
produced").

State the call and reasoning. The training-provenance addendum is
a strong prior toward (b); but if you have evidence (b) creates
schema-divergence or maintenance risk, make the case for (a).

#### Item 2 — 45→59 warm-start mechanism

Stock XGBoost warm-start (`xgb_model=` parameter to `fit()`, or
`booster.update()` with `process_type='update'`) requires identical
feature schema. The 45→59 boundary is non-trivial. Decide one
mechanism:

- **Pre-pad baseline:** custom surgery on the booster JSON to add
  4 zero-weight columns at the v2.4 P1 blocker positions
- **Curriculum:** train 45-feat student on the new corpus first, then
  expand to 59-feat as a from-scratch run with the 45-feat student
  used as priors (not strict warm-start)
- **Distillation:** 45-feat baseline as teacher, 59-feat student
  trained to match teacher predictions on overlapping features
- **From-scratch with priors:** abandon warm-start, train 59-feat from
  zero on the 494-hand corpus, use the baseline only for hyperparameter
  defaults and as the dominated-by reference

State the call. If the chosen mechanism requires changes to the
v9 baseline JSON, state what changes and why.

#### Item 3 — Per-sample confidence weighting math

Corpus labels carry `consensus_confidence` per row (1.0 = unanimous,
0.8 = 4/5, 0.6 = 3/5, 0.5 = plurality-tied). Decide weighting math:

- **Pure per-sample:** `sample_weight = consensus_confidence`
- **Hybrid with inverse-class-frequency:** `sample_weight = consensus_confidence × class_weight[y]` where class_weight comes from `train_model.py:252–257` style (esp. `RAISE` boost since 5.9% rarest)
- **Class-normalised per-sample:** `sample_weight = consensus_confidence`, then re-normalise per class so each class's total weight is equal

Decide. Account for RAISE rarity (5.9%, 16 consensus records); state
how the chosen scheme handles minority classes.

#### Item 4 — 4-blocker FEATURE_COLUMNS integration

Decide one of:

- **Path X (single source of truth):** extend
  `gto_model.py:33–62` `FEATURE_COLUMNS` to include the 4 v2.4 P1
  blockers (`nut_flush_block`, `flush_draw_block_pct`,
  `straight_draw_block_pct`, `nut_made_block_pct`); update
  `train_model.py:131–160` to read from `gto_model.FEATURE_COLUMNS`
  (or duplicate consistently). `gto_model.py:64` becomes
  `N_FEATURES = 59`.
- **Path Y (independent schema):** new student trainer module owns
  the 59-feature schema; `gto_model.py` stays at 55. Production
  inference uses a separate code path for the v9 student vs the
  existing models.

Path X is cleaner long-term but touches sacred core (CLAUDE.md §6).
Path Y is faster but creates dual-schema risk. Decide and reason.

If Path X, recommend whether the FEATURE_COLUMNS extension is a
**12.5A-prep PR** (small architect-led patch landing before 12.5C
blueprint) or part of 12.5D's main PR.

#### Item 5 — Canonical reference-set selection

`training-data/3way_reference_40hand.jsonl` (cited by Phase 12
directive) does not exist on master. Audit `training-data/`
candidates. Known options from prior reports:

- `3way_combined_350.jsonl`
- `3way_labelled.jsonl`
- `3way_selected_200.jsonl`
- `3way_situations.jsonl`
- `facing_bet_test_set_40.jsonl`
- Any `*40hand*` files I may have missed

For each candidate, state: row count, label coverage, intended use
(per existing comms history if traceable). Recommend one as the
canonical 40-hand litmus reference. If none qualifies, recommend
authoring a new one (with scope: source corpus, label provenance,
gate criteria) but flag this as a Phase 12.5-prep workstream that
adds time and cost — owner would need to approve that detour.

The reference set is the basis for `PROCESS_GUIDE.md` §2.4 (reference
gate). Solver-corrected scoring per `memory/reference_corrections.md`
must apply.

#### Item 6 — Stratified split + multi-seed strategy

Confirm:

- 80/20 stratified split per seed (5 seeds: 0, 1, 2, 3, 4)
- Stratification dimension (class label `y`, or class × confidence
  bucket, or class × board street) — recommend with reasoning
- Variance reporting: mean ± std across seeds, per-seed accuracy
  table
- Held-out vs litmus distinction (must be reported separately per
  QC concern V-Allocator-Multi-Dim)

### Orchestrator commitments — ML-architect designs against these locked premises

The following are committed; ml-architect does not re-decide them.

- **Arithmetic:** `55 + 4 = 59` (not "45 + 14"). Aligns to
  `scripts/verify_feature_schema_compatibility.py:39–41`.
- **Join key:** `corpus.source_situation_id == labels.ref_id`
  (verified row 1: both `d6066_BB_flop`). `pilot_hand_id` is a
  fallback validation key, not the primary join.
- **Class set:** 5-class `multi:softprob` — CHECK / BET / FOLD /
  CALL / RAISE.
- **Seed count:** 5 (seeds 0–4).
- **Split ratio:** 80/20 stratified.
- **Litmus comparison:** must report v8, v9-3way-v2.2, and v9
  student on the same held-out + reference set in the same trainer
  report (per Gate 2.4).

### 12.5A output

Single comm: `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-XX.md`.

Sections required:

- Executive summary (1 paragraph: chosen architecture in plain prose)
- Item 1 — Trainer module location: decision + reasoning
- Item 2 — 45→59 warm-start mechanism: decision + reasoning
- Item 3 — Per-sample weighting math: decision + reasoning
- Item 4 — 4-blocker FEATURE_COLUMNS integration: decision + reasoning + 12.5-prep vs 12.5D-bundle call
- Item 5 — Canonical reference-set selection: candidate audit + decision
- Item 6 — Stratified split + multi-seed strategy: confirmed approach
- Hyperparameters: `n_estimators`, `max_depth`, `learning_rate`,
  early-stopping rounds — committed values with brief reasoning
  (do not punt to "tune at 12.5D")
- Trainer CLI surface: full argparse contract (flag names, types,
  defaults, help strings)
- Gate 2.3 + 2.4 hooks: how feature-importance check + reference
  evaluation are integrated
- Risk register: 3–5 items where the design could fail at 12.5D, with
  mitigations
- References (file:line citations for every source claim)

### What 12.5A must NOT do

- Write any code (no `.py` changes anywhere)
- Modify `train_model.py`, `gto_model.py`, `feature_keys.py`,
  `feature_extractor.py`, or any model JSON
- Run training (or any pipeline)
- Present menus or "open questions for owner" on the six items —
  commit with reasoning
- Pre-empt architect (12.5C) on insertion points or line numbers —
  that's the architect's job, not ml-architect's
- Pre-empt programmer on coding decisions below the design level

### 12.5A PR + branch

Branch: `mla/phase125a-trainer-design-2026-05-XX` (use today's date
when authoring).

PR title: `ML-architect Phase 12.5A: v9 student trainer design`.

Single comm file in PR. No source changes.

## Cost / risk

- 12.5A cost: ~$0 — design only, file reads + reasoning, no API
  calls outside the design agent itself.
- Risk: low — read-only, owner gates approval before architect
  dispatch.
- Failure mode: ml-architect requests clarification or surfaces a
  blocker on a locked premise. Builder/QC: STOP, escalate to
  orchestrator with specific evidence (do not improvise around
  locked premises).

## Stop conditions for 12.5A

- Master HEAD source contradicts a locked premise (e.g.,
  arithmetic): STOP, post BLOCKED, orchestrator amends.
- A required source file is missing: STOP, post BLOCKED.
- A locked premise is internally inconsistent (e.g., join key
  doesn't actually verify on row 1 of corpus + labels — already
  verified, but if you find it doesn't): STOP, post BLOCKED.

Per `feedback_verify_source_not_plan.md`: ml-architect verifies all
locked premises against master HEAD source before proceeding. If
any verification fails, STOP — do not improvise.

## What this directive does NOT cover

- Tier 1 calibration manifest 33→45 (separate dormant workstream)
- Held-out testset v1.0 expansion beyond what 12.5A may recommend
  for the canonical reference set
- Teaching system Phase C (gated on 80%+ shipped — already met by
  v9-3way-v2.2)
- v9-4way / v9-5way specialist training
- Preflop range fix steps 5–7

## QC stream — what runs in parallel

QC stream stays on alignment + audit-pattern formalisation per D-4
and D-5 from `SHARED_STATE_BASELINE_2026-05-02.md`. No 12.5A audit
dispatch (12.5A is design-only, gated by owner approval). QC will
pre-merge audit at 12.5D PR per the new TC-23-CLI sub-vector
(milestone-class CLI-prescribing directive lands at 12.5C blueprint;
QC pre-merge audit fires on the 12.5D implementation PR).

## References

- Master HEAD: `14c2db1`
- Phase 12 directive (superseded): `review/comms/MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
- Phase 0 alignment PRs: #105 (QC), #106 (builder), #107 (orchestrator)
- Synthesis baseline + owner sign-off: PR #108 — `review/comms/SHARED_STATE_BASELINE_2026-05-02.md`
- Process: `docs/PROCESS_GUIDE.md` §1.4, §2, §6, §8; `CLAUDE.md` §1, §6 (training-provenance addendum 2026-04-15)
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_quality_default_no_ask.md`, `feedback_verify_source_not_plan.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_named_author_builds_not_polls.md`, `feedback_spec_vs_infrastructure_code_drift.md`

**Status: PHASE 12.5 KICKOFF OPERATIONAL. ML-ARCHITECT (12.5A) authorised to begin design. Output → `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-XX.md` + PR. 12.5B owner gate before architect (12.5C) dispatches. No builder, no QC audit dispatch in parallel.**
