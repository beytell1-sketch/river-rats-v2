# Phase 2-F Readiness Scorecard

**DATE:** 2026-05-13
**AUTHOR:** Orchestrator (5 independent audits + 1 process-guide review + 1 master-plan review)
**STATUS:** Decision document for owner — what scope to dispatch when orchestrator terminals restart

This synthesises all audits performed pre-restart. The owner uses this to make 3 scope decisions before authorising the architect to fire.

---

## TL;DR

| | |
|---|---|
| **Original concern** | Diversity in positional action sequences (owner-flagged) |
| **What audits found** | Concern valid AND broader — 3 systemic gaps spanning corpus, prompt, knowledge base |
| **Phase 2-F scope** | Expanded from positional-diversity-only to corpus + prompt + KB + calibration |
| **Critical path** | A1 (chain dim) → A2a/b/c (prompt + brief + KB) → calibration → A3 (audit spec) → B1 (scenarios) → B0 (recalibrate) → B2 (pilot re-label) → B3 (full sample) |
| **Owner decisions outstanding** | 3 (drift thresholds, scope split vs bundled, 5-way reference set timing) |

---

## The 3 systemic gaps (aligned blind spots)

The corpus, the prompt, and the knowledge base have **the same missing strata**:

| Stratum | Corpus (350 hands) | Prompt v3.4 examples | KB v1.3 examples |
|---|---|---|---|
| **Facing-raise** | 0/350 | 0 | 0 |
| **River** | 0/350 | 0 | 0 |
| **Sandwich position** | unmeasured | 0 | 0 |

**Implication:** Labellers were never taught how to label facing-raise / river / sandwich hands, so the corpus generators never asked them to. The gap is **architectural**, not just statistical.

---

## ⚠ CRITICAL FINDING from corpus statistical audit

**`predicted_sizing_pct` field has DUAL SEMANTICS — schema-design defect.**

The 4-way labeller brief (`data/4way_labeller_brief.md:32-33`) instructs labellers to write predicted_sizing_pct as:
- BET → integer % of pot
- RAISE → integer bb amount

But the field name `_pct` suggests one unit. Training-data export does NOT normalize between units. Per the corpus audit:
- 44% of RAISE labels store value=9 (interpretable as 9bb raise-to)
- Outliers: 18/22/27/300/360/720 (mix of bb and possibly pct values)
- BET sizings (n=574) are clean (~66% pot dominates — pct semantics consistent)

**Implication:** If Phase 2-G v9-4way retrain consumes this corpus as-is, the model will learn corrupted RAISE-sizing targets. Sizing accuracy will be effectively random for RAISE labels.

**Severity:** BLOCKER — upstream of all Phase 2-F prompt/KB/corpus work. Must fix before retrain.

**Fix options:**
1. **Schema split** — rename to `predicted_bet_pct` (% of pot, only for BET) and add `predicted_raise_to_bb` (bb amount, only for RAISE). Re-export training data with separate columns.
2. **Normalizer** — deterministic post-processor that converts mixed RAISE values to canonical units. Risk: ambiguous when value=300 could be 300bb OR 300% of pot.

**Recommendation:** Option 1 (schema split). Cleaner, no inference required. Add to Phase 2-F as new architect task: **A0 (schema fix)**, gated before A1.

---

## Audits performed (4 independent)

### Audit 1: Positional action-chain diversity (orchestrator + Explore)

- **Finding:** Corpus generator's 8-D stratification uses binary action_context, not n-ary villain-chain fingerprint
- **Cardinality:** ~100 4-way chains exist; ~10 enumerated; ~240+ at 5-way (0 enumerated)
- **Severity:** Validates owner's concern; concern is **real** and **worse at 5-way**
- **Output:** PR #457 STANDBY directive + PR #458 architect drafts

### Audit 2: v3.4 prompt latent issues (Explore)

11 issues; **3 BLOCKERS**:
- KB §1.7 has 3-layer override patches (v3.2 + v3.3 + v3.4 Fix 2.1.1) — unmaintainable
- Solver-as-reasoning references (violates `feedback_solver_vs_expert_labels.md`)
- DO NOT Rule 11 threshold logic (violates `feedback_bucket_first_labelling.md`)

### Audit 3: KB v1.3 runtime worked examples (Explore)

- **BLOCKER:** KB v1.3 (2026-04-10) hasn't been updated for v3.2/v3.3/v3.4 prompt patches
  - Labellers at runtime read PROMPT + KB → see **contradictory guidance**
- **6 of 11 DO NOT Rules** lack worked examples (Rules 3, 4, 7, 9, 10, 11)
- **Bucket coverage skew:** Strong-made 0%, Air 0%, Monster 22%, Medium-made 44%
- **Position skew:** Sandwich 0%, OOP 44%, IP 33%
- **Critical absence:** 0 river examples, 0 facing-raise examples, 0 sandwich examples (mirrors corpus gap)

### Audit 4: 350-hand corpus statistical (general-purpose)

Beyond the empty strata (audit 5), the corpus has:
- **DUAL-SEMANTICS sizing bug** (see Critical Finding above) — BLOCKER
- **Per-batch heterogeneity:** all 7 batches exceed 10pp drift from corpus mean action distribution. Batches 1-3 are BET-heavy (+15 to +26pp BET); batches 5-6 are CALL/RAISE-heavy (-19 to -27pp ΔBET). Random train/eval splits will hide stratum-specific failures
- **RAISE triple-jeopardy:** under-represented (17%, n=58), lowest agreement (0.91, only 57% unanimous), corrupted sizing semantics
- **FOLD at 9%** — under §2.1's "<10% flag" threshold for class imbalance

### Audit 5: 20-hand pilot stratification (general-purpose)

Pre-built deterministic pilot sample (seed=20260513) revealed corpus structural gaps:
- Facing-raise stratum: **0/350**
- River stratum: **0/350**
- Position skew: BTN/UTG/EP each <5%; CO ~30%

---

## Protocol-adherence gaps found in current FIRE_NOW draft

Reviewing `docs/PROCESS_GUIDE.md` against the directive draft:

| Gap | Process Guide section | Severity | Required fix |
|---|---|---|---|
| **No calibration gate before B2 pilot fires** | §2.1 "Calibration before labelling — MANDATORY before every labelling round. If knowledge base checksum changed, re-calibrate. No exceptions." | BLOCKER | Add Task B0 (pre-B2 calibration): all 5 labellers + Opus pass blind exam against v3.5 prompt + v1.4 KB; gate = 20/24 + all 3 GTO-reversal hands correct |
| **Reviewer count < labeller count ÷ 2** | §1.2 "Reviewer count ≥ labeller count ÷ 2" | SHOULD_FIX | 5 labellers needs ≥3 reviewers; current spec has 1 Opus tier-up. Either accept Opus + consensus mechanism as "review" (clarify in spec) or add 2 more independent reviewers |
| **No solver-verify trigger handling in re-label** | §5.2 "Any RAISE label on non-set/non-nut hand → verify; Any HIGH-confidence disagreement → flag for solver" | SHOULD_FIX | A3 spec should route v3.5-relabel RAISE hands and drift hands to solver-verify queue |
| **KB v1.4 will require re-calibration of all labellers** | §2.3 "Re-calibration mandatory after any KB change" | BLOCKER | Calibration gate covers this when added as B0 |

---

## Phase 2-F task graph (expanded — now with A0 schema fix)

```
PHASE 2-E batch-008 ships (current builder work)
  │
  ▼
A0 (architect, NEW): sizing-schema fix blueprint
  - Split predicted_sizing_pct → predicted_bet_pct + predicted_raise_to_bb
  - Re-export training data with separated columns
  - Backfill normalizer for batches 001-008 RAISE labels
  - Gate before all subsequent architect tasks; this fixes training-data
    integrity for Phase 2-G v9-4way retrain
  │
  ▼  [QC G0]
  │
  ▼
A1 (architect): positional_action_chain dimension blueprint
  - 9th stratification dim
  - Mandatory facing-raise + river + position-balance quotas (new)
  - File: corpus_revision_scenarios/positional_action_chain_scenarios.py
  │
  ▼
A2 (architect, expanded): v3.5 amendment bundle (3 sub-tasks)
  ├── A2a: AMENDMENT 3 to data/4way_labeller_brief.md (FL6 + chain phrasing)
  ├── A2b: prompts/gto_labeller_v3.5.md (full rewrite — 3 BLOCKERS fixed)
  └── A2c: knowledge/three_way_gto.md v1.4 (NEW — sync KB §1.7, add 6 missing examples)
  │
  ▼
A3 (architect): re-label consistency audit spec
  - 4-D stratification, 80-hand sample (20 pilot subset)
  - Drift metrics + Opus tier-up + solver-verify routing (new)
  - Calibration evidence requirement (new)
  │
  ▼  [QC G1–G4 gate all 4 architect deliverables]
  │
  ▼  [Owner Gate 1: approve scope]
  │
  ▼
B1 (builder): implement positional_action_chain_scenarios.py
  - 20-hand micro-batch yield test
  - Confirms facing-raise + river + position-balance quotas materialise
  │
  ▼  [QC G5]
  │
  ▼
B0 (builder, NEW): calibration before B2 — MANDATORY
  - All 5 Sonnet labellers + Opus tier-up agent take blind exam
  - Exam input: 24 hands + 3 GTO-reversal hands
  - Exam answer key: held separately, graded by independent process
  - Gate: each labeller ≥20/24 + all 3 GTO-reversals correct
  - Re-runs allowed; failure persists → labeller agent prompt is the issue
  │
  ▼  [QC G6 — verify calibration evidence, not labellers' claims]
  │
  ▼
B2 (builder): 20-hand pilot re-label
  - Uses v3.5 prompt + AMENDMENT 3 + KB v1.4 + calibrated labellers
  - 5 Sonnet + Opus tier-up on drift hands
  - Solver-verify routing for drift RAISE + drift HIGH-confidence-disagreement
  - Drift analyzer produces DRIFT_REPORT_PILOT.md
  │
  ▼  [QC G7]
  │
  ▼  [Owner Gate 2: drift acceptable?]
  │
  ▼
B3 (builder, conditional): 80-hand full re-label sample
  - Conditional on Owner Gate 2 passing
  - Same protocol scaled
  - DRIFT_REPORT_FULL.md
  │
  ▼  [QC G8]
  │
  ▼  [Owner Gate 3: ship Phase 2-F? re-label all 350? roll back?]
  │
  ▼
Phase 2-F ships → v9-4way warm-start training (Phase 2-G)
```

**Total architect deliverables:** 6 (A0 + A1 + A2a + A2b + A2c + A3)
**Total QC gates:** 9 (G0–G8)
**Total builder tasks:** 4 (B1 + B0 + B2 + B3)

---

## 3 owner decisions outstanding

### Decision 1: Drift thresholds

| Option | Pilot accept | Pilot reject | Full accept | Full reject | Rationale |
|---|---|---|---|---|---|
| **A — STRICT** (orchestrator) | ≤5% (≤1 hand) | ≥20% (≥4 hands) | ≤5% | ≥15% | "No drift = amendment is safe" |
| **B — PERMISSIVE** (architect draft) | ≤15% | >30% | ≤12% | >25% | "Some drift = expected noise on hard hands" |
| **C — MIDDLE** | ≤10% | ≥25% | ≤8% | ≥20% | Compromise |

**Recommendation:** B (permissive). Rationale: existing Phase 2-E batches show 6% owner-arb rate as routine, meaning labeller noise floor is already ~6%. Demanding ≤5% drift means demanding "less variance than the base process." Owner can tighten in future runs.

### Decision 2: Scope split — bundled or staged?

| Option | Phase 2-F includes | Phase 2-G (later) | Trade-off |
|---|---|---|---|
| **A — BUNDLED** | All: chain dim + prompt v3.5 + KB v1.4 + calibration + relabel audit | v9-4way retrain | One bigger Phase 2-F; one drift measurement against multiple changes simultaneously (harder attribution) |
| **B — STAGED** | Phase 2-F1: chain dim + corpus regen only (no prompt change) | Phase 2-F2: prompt+KB v3.5; Phase 2-G: retrain | Each phase has clean drift attribution; longer total path |
| **C — PROMPT-FIRST** | Phase 2-F1: prompt+KB v3.5 + relabel audit (no new corpus) | Phase 2-F2: chain dim + corpus regen; Phase 2-G: retrain | Fastest to validate prompt fixes; defers corpus structural gap |

**Recommendation:** B (staged). Rationale: per `feedback_pilot_first_for_long_jobs.md`, isolate one change at a time so drift attribution is unambiguous. If A is chosen, the drift report can't distinguish "v3.5 prompt changes labels" vs "KB v1.4 changes labels" vs "facing-raise hands change labels."

### Decision 3: 5-way reference set — generate now or after Phase 2-F?

Per `docs/MASTER_PLAN (1).md:88-99`: 5-way reference is **0 hands**; "Must add 5-10 before Step 3" (v9-5way training).

| Option | Action | Trade-off |
|---|---|---|
| **A — NOW** | Generate 10-hand 5-way reference set in parallel with Phase 2-F | Earlier; ensures reference exists when v9-5way training fires |
| **B — AFTER Phase 2-F** | Defer; generate after v9-4way ships | Simpler critical path; risks blocking v9-5way training when ready |
| **C — IN Phase 2-F** | Include 5-way reference generation as a 6th architect task (A4) | Bundles with Phase 2-F scope; expands directive further |

**Recommendation:** A. Rationale: 5-way reference generation is independent of Phase 2-F (different deliverable, different agents). Running in parallel costs nothing and resolves a master-plan blocker.

---

## Solver-verify queue status (from Builder Report PR #453)

Pre-Phase-2-F solver-verify queue: **28 spots** (23 prior + 5 from batch-007). Per `feedback_solver_verification_queue.md`: "Queue MUST drain before retrain ships."

**Implication:** Before v9-4way retrain (Phase 2-G), this queue must drain. Phase 2-F doesn't change that — Phase 2-F will likely ADD spots to the queue (drift hands + RAISE hands per §5.2 triggers).

**Recommendation:** Plan solver-verify drain as a parallel workstream during Phase 2-F. Owner runs ~30 spots through solver between now and v9-4way retrain.

---

## Files prepared pre-restart (8-file bundle in PR #458)

| File | Purpose | Status |
|---|---|---|
| AUDIT_GTO_LABELLER_V3_4_LATENT_ISSUES_2026-05-13.md | v3.4 prompt audit (11 issues, 3 BLOCKERS) | DONE |
| DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1 | Architect A1 input | DONE |
| DRAFT_AMENDMENT_3_LABELLER_BRIEF_POSITIONAL_CHAIN_v3_5 | Architect A2a input | DONE |
| DRAFT_SPEC_RELABEL_CONSISTENCY_AUDIT_v1 | Architect A3 input | DONE |
| DRAFT_PILOT_SAMPLE_20HAND (3 files) | Builder B2 input | DONE |
| DRAFT_MAIN_TERMINAL_PHASE2F_FIRE_NOW | Re-issuance template | DONE |
| **DRAFT_AUDIT_KB_v1_3_LATENT_ISSUES** | KB v1.3 audit (this scorecard's source) | DONE (this synth) |
| **DRAFT_FULL_SAMPLE_80HAND** | Builder B3 input | PENDING agent |
| **DRAFT_SPEC_DRIFT_ANALYZER_v1** | Builder drift-tooling spec | PENDING agent |
| **DRAFT_AUDIT_CORPUS_LABEL_DISTRIBUTION** | Statistical bias audit | PENDING agent |

---

## What the orchestrator does at restart

1. Phase 2-E batch-008 must finish first (labellers 2-5 incomplete: 36, 11, 10, 25 of 50)
2. Once batch-008 ships + QC PASS, owner reads this scorecard
3. Owner makes 3 decisions
4. Orchestrator updates DRAFT_MAIN_TERMINAL_PHASE2F_FIRE_NOW with date + chosen scope, dispatches
5. Architect ratifies the 5 pre-drafted deliverables (1-line commits if no changes; reauthor if scope differs)
6. Builder fires B1 → B0 (calibration) → B2 → B3 in sequence
7. QC G1-G8 in sequence
8. Owner gates at 3 checkpoints
9. Phase 2-F ships when DRIFT_REPORT_FULL.md is approved

---

## If owner approves all defaults

- Decision 1: PERMISSIVE thresholds
- Decision 2: STAGED (Phase 2-F1 = chain dim + corpus regen only; Phase 2-F2 = prompt+KB)
- Decision 3: 5-way reference set in parallel

Then orchestrator dispatches **Phase 2-F1 only** with reduced scope:
- A1 (chain dim) + A3 (audit spec)
- B1 (scenarios) + B2 (pilot re-label of EXISTING labels against EXISTING prompt to measure corpus-only drift baseline) + B3 (full sample)
- 5-way reference set work in parallel by a separate architect

Phase 2-F2 follows after Phase 2-F1 ships, with full prompt+KB rewrite scope.

This is the cleanest critical path and the recommendation if you want fastest time-to-v9-4way-retrain.
