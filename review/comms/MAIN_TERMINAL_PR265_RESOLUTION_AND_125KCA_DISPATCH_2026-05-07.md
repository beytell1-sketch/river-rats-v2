---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #265 + PR #267 merged (QC PASS; 31st solo cycle); ratify hyperparameter-bound finding at Lever B; dispatch 12.5K-C-A Lever C design (architect-hat; 3-axis augmented data labelling round)
status: DIRECTIVE — merges PR #265 + PR #267; fires LEAD-PROGRAMMER on 12.5K-C-A — fire now
---

# PR #265 + PR #267 merge + 12.5K-C-A Lever C design dispatch

QC verdict on PR #265 (`REVIEW_QC_PHASE125K_B_HYPERPARAMETER_SWEEP_2026-05-06.md` on `qc/pr265-125kb-review-2026-05-06`, PR #267): **PASS**. 31st solo cycle expected. Lever B halt-at-pilot ratified per quality-default — spread of 0.20 hands across 3 representative configs is well below meaningful-improvement threshold; full sweep would be 9.5+ hours of disproportionate cost.

**Empirical convergence:**
- Lever A (variance): RULED OUT (20-seed mean 33.10 ± 0.30 stays below baseline 34/40)
- Lever B (hyperparameters): RULED OUT (3-config pilot spread 0.20 hands; no meaningful lift)
- **Lever C (augmented data) is the remaining lever**

The model's accuracy at 788-corpus 61-surface is genuinely ~33.10/40 across configs and seeds. The path to lift past v9-3way-v2.2 baseline is **more training data targeting under-represented stay-wrong axes**.

## LEAD-PROGRAMMER — Step: 12.5K-C-A Lever C design (architect-hat) — fire on this comm merge

Per plan §5 "Lever C — augmented training data" + §6 sequenced recommendation. Lever C is a multi-phase mini-pipeline (mirror MW-40-VERIFICATION 5-phase pattern: A design → B situation gen → C labelling → D Opus tier-up → E corpus integration + re-train). This dispatch is **-A only (design phase)**.

Branch: `programmer/phase125k-c-a-augmented-data-design-2026-05-07`. Base: master post-this-comm-merge.

### Scope — design plan comm only (architect-hat; no execution)

Builder authors `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` analyzing the 3-axis augmented data round. This is a DESIGN phase, NOT execution.

### What 12.5K-C-A design must specify

#### 3 stay-wrong axes (NOT 4 — MW-40 excluded)

MW-40 graduation-fail confirmed via 4-source pattern (PR #241 + PR #245); structural argument empirically too narrow; BATCH2 stays BET MEDIUM. **DO NOT re-label MW-40-axis hands** — that work is complete; structural argument is closed. Including MW-40 in Lever C augmented data would add MW-40-class hands but the labelling pipeline produces BET (matching BATCH2), so the model would learn BET on MW-40-like hands. THIS IS THE INTENDED OUTCOME — the model currently incorrectly predicts CHECK on MW-40 (stay-wrong); adding BET-labelled MW-40-like hands teaches the model the right answer.

**Wait — re-evaluate.** MW-40's labelling pipeline output is BET (matching BATCH2). If Lever C labelled more MW-40-class hands, they would also be BET. The model currently predicts CHECK on MW-40. So MW-40-axis augmented data WOULD help the model learn BET. **Decision (orchestrator-scope):** include MW-40 axis in Lever C if useful, even though MW-40 verification round is graduation-fail. The "do NOT re-label" guidance was for re-running the verification (which is closed); augmented data IS new corpus rows for training, not verification.

**Updated**: 4 stay-wrong axes for Lever C (MW-17, MW-40, MW-45, MW-47). Each axis ~50 hands. Total ~200 new corpus rows.

| Axis | Canonical action | Stay-wrong pattern | Lever C target prediction |
|---|---|---|---|
| MW-17 | CALL | Model predicts FOLD (stay-wrong) | Pilot expects CALL consensus from labelling pipeline |
| MW-40 | BET MEDIUM | Model predicts CHECK (stay-wrong) | Pilot expects BET consensus (per MW-40-VERIFICATION 25/25 + 5/5 finding) |
| MW-45 | RAISE | Model predicts CALL (stay-wrong) | Pilot expects RAISE consensus |
| MW-47 | RAISE (solver-corrected) | Model predicts CALL (stay-wrong) | Pilot expects RAISE consensus |

Per axis: 50 parametric variants targeting the structural pattern. ~50 × 4 = 200 new corpus rows.

#### Per-axis pilot-first 5-hand gate (binding per `feedback_pilot_first_for_long_jobs.md`)

Per plan §5 pilot-first scope. Per axis:

| Pilot gate criterion | Continue if... | Off-ramp (per axis) if... |
|---|---|---|
| Pilot consensus aligns with structural prediction | ≥4/5 hands consensus on the predicted action | <4/5 consensus → REPORT to orchestrator; mirror MW-40-VERIFICATION-C HALT pattern; orchestrator decides per axis |
| Sonnet API errors | <5% on 5-hand × 5-labeller pilot (= 25 calls) | >5% → STOP infrastructure |
| Reasoning convergence | Convergent reasoning citing v3.4 KB sections | Mode-collapse → STOP |

Per-axis off-ramp: if axis fails pilot, that axis is dropped from Lever C; remaining axes proceed. Mirrors the partial-scale pattern in plan §5 outcome matrix row 2.

#### Methodology rules (standing per 12.5I-A precedent)

- design_action per T-CONTROL: per-hand pilot expected action documented per axis
- Cross-seed importance reporting: NOT applicable (Lever C is corpus expansion, not retrain)
- Cap-binding pre-flight: ref_id namespace `PILOT_LEVER_C_<AXIS>_001..050` per axis
- Tier-up verification: Sonnet → Opus on 5 canonical hands per axis × 4 axes = 20 Opus calls (per `feedback_pilot_first_for_long_jobs.md` sub-rule)
- Pilot-first: 5-hand pilot per axis BEFORE scaling
- Hero-only convention: yes
- Pre-flight join-cardinality: ref_id namespace disjoint vs 788-corpus + prior 12.5I namespaces

#### Cost / time

- Design phase (this PR): ~$0; ~30-45 min builder
- Downstream (informational; separate dispatches):
  - -B situation gen: ~$0; ~15-20 min
  - -C labelling: ~$50-80 LLM (5 sonnet × 200 hands × ~$0.05); ~2-3 hours
  - -D Opus tier-up: ~$15-20 (20 Opus × $0.75-1); ~30 min
  - -E corpus integration + re-train (with augmented 988-corpus): ~$0; ~1-2 hours
- **Total Lever C**: ~$65-100 LLM; ~4-6 hours wall clock

Within ~$300/30h auto-approval cap.

#### Deliverable scope (this PR)

1 file: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`

Mirror `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` structure (§3 constraint table, §4 sub-axis tables, §5 factory spec, §6 methodology rules, §7 sequencing, §8 stop conditions, §9 NOT-do, §10 risks/open questions, §11 cost/time, §12 deliverable scope).

### Stop conditions (12.5K-C-A design)

- Plan does NOT include all 4 stay-wrong axes (MW-17 + MW-40 + MW-45 + MW-47) → STOP
- Plan does NOT specify pilot-first 5-hand gate per axis → STOP
- Plan recommends solver-as-labels for any axis → STOP per `feedback_solver_vs_expert_labels.md`
- Plan total cost > ~$300 LLM OR > ~30h wall clock without explicit orchestrator approval → REPORT
- Plan does NOT specify per-axis ref_id namespace → STOP
- Plan recommends labels NOT independently verified by Sonnet+Opus tier-up → STOP

### What you do NOT do

- Do NOT execute any labelling in this PR (this is design only)
- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference
- Do NOT touch existing 788-corpus or labels
- Do NOT auto-fix Lever B's report (orchestrator-scope)
- Do NOT recommend skipping pilot-first per axis (binding)

### Cost / time (this PR)

~$0 (design only); ~30-45 min builder wall clock.

## QC stream — what you audit (when 12.5K-C-A design PR opens)

Standalone audit, ~10-15 min, 7-item design-phase scope:

1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) — exactly 1 file (+ optional analysis)
2. All 4 stay-wrong axes covered (MW-17 + MW-40 + MW-45 + MW-47)
3. Per-axis pilot-first 5-hand gate specified
4. Per-axis structural prediction documented (matches stay-wrong canonical/solver-corrected actions)
5. Methodology rules (7 standing per 12.5I-A) cited
6. TC-X-OWNER-SCOPE-DISCIPLINE (no v3.x / BATCH2 / corpus / source / memory edits)
7. TC-X-DISPATCH-COMPLIANCE 11th formal exercise (design-only; per-axis off-ramp specified)

## Sequencing — what fires after 12.5K-C-A merges

1. **12.5K-C-B situation generation** — 200 hands × 4 axes; factory pass
2. **12.5K-C-C labelling round** — 5 Sonnet × 200 hands; per-axis pilot-first 5-hand gate
3. **12.5K-C-D Opus tier-up** — 20 Opus calls (5 canonical × 4 axes)
4. **12.5K-C-E corpus integration + re-train** — augment 788 → 988 corpus; 5-seed re-train; reference set spot-check
5. **12.5L gate evaluation** — gates on -E outcome (PROMOTE / NOT-PROMOTE)

## What's blocked / what's queued

**Cleared by this comm:**
- PR #265 merge (Builder Lever B halt-at-pilot)
- PR #267 merge (QC verdict record)
- 12.5K-C-A Lever C design dispatch fires
- Hyperparameter hypothesis ruled out

**Newly queued (after 12.5K-C-A merges):**
- 12.5K-C-B situation generation

**Still queued (later):**
- 12.5K-C-C / -D / -E
- 12.5L gate evaluation

## References

- PR #265 (Builder Lever B halt-at-pilot): branch `programmer/phase125k-b-hyperparameter-sweep-2026-05-06`
- PR #267 (QC PASS verdict): branch `qc/pr265-125kb-review-2026-05-06`
- PR #266 (QC trigger): master `5b0b983`
- PR #264 (Lever B dispatch): master `bc7d08b`
- 12.5K master plan §5 (Lever C spec): `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- 12.5I-MW40-VERIFICATION precedent (5-phase mini-pipeline pattern): `review/comms/PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- v9-3way-v2.2 baseline: 34/40 solver-corrected
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md` (per-axis pilot + Opus tier-up), `feedback_solver_findings.md`, `feedback_solver_vs_expert_labels.md`

**Status: PR #265 + PR #267 cleared for merge. Hyperparameter hypothesis ruled out. LEAD-PROGRAMMER fires 12.5K-C-A Lever C design (architect-hat) on this comm merge. ~$0 LLM; ~30-45 min wall clock to PR open.**
