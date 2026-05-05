---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5E-E — re-train v9 student on 604-hand corpus + queued cleanup; pilot dry-run before 5-seed full
status: TRIGGER — fire now
---

# Phase 12.5E-E — re-train v9 student on 604-hand corpus

12.5E-D APPROVED (master `4070a11`). Combined 604-hand corpus is QC-cleared (G1-G4 all PASS; RAISE class jumped 5.9% → 11.26% — design-intended H-DIST shift confirmed).

12.5E-E re-runs the existing `river-rats-core/train_model_v9_student.py` on the new combined corpus + labels. **No trainer code changes** beyond paths + the queued cleanup items. Hyperparameters identical to 12.5D' (cap=3.0 hybrid weighting, pre-pad metadata-only, 5 seeds 0-4).

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125e-e-retrain-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (default — implementation)

#### Step 1: merge corpus + labels at file level (no trainer code change)

Trainer CLI accepts single `--corpus` and `--labels` paths (verified at master HEAD: `train_model_v9_student.py:1388-1390`). Merge:

```
data/corpus_combined_604_2026-05-05.jsonl    = corpus_revision_500_hand_2026-04-27.jsonl
                                              + corpus_revision_125e_situations_2026-05-04.jsonl
                                              + corpus_revision_125e_manual_canonicals_2026-05-04.jsonl

data/corpus_combined_604_labels_2026-05-05.jsonl = corpus_revision_500_hand_labels_2026-04-27.jsonl
                                                  + corpus_revision_125e_labels_2026-05-05.jsonl
```

Verify post-merge: 604 rows in each; `pilot_hand_id` cardinality 604/604; join works (every situation has matching label).

#### Step 2: PILOT — 1-seed dry-run BEFORE 5-seed full (per `feedback_pilot_first_for_long_jobs.md`)

```
python3 river-rats-core/train_model_v9_student.py \
  --corpus data/corpus_combined_604_2026-05-05.jsonl \
  --labels data/corpus_combined_604_labels_2026-05-05.jsonl \
  --no-write-model \
  --seeds 0
```

Pilot gate criteria (all must hold to proceed to Step 3):
- Trainer loads combined 604 corpus + labels without errors
- Pre-pad metadata-only mechanism succeeds on warm-start anchor (no R-1 fallback needed)
- Held-out classification report produced (5 classes, sane support per class)
- Reference-evaluator gate runs and produces solver-corrected score on the new chosen seed
- `_StudentInferenceLike45` invariant test passes

**STOP conditions on pilot:**
- Trainer crashes on combined corpus → STOP, debug (likely schema mismatch; new files have to match feat_dict shape of old)
- Pre-pad mechanism fails (R-1 fallback fires) → STOP, document, route to architect hat
- Reference-evaluator score in 1-seed pilot is wildly off baseline (< 25/40 or > 40/40) → STOP, investigate before 5-seed
- Invariant test fails → STOP (mirror drift between `_evaluate_one_hand` and `_evaluate_student_one_hand`)

#### Step 3: FULL — 5-seed run

Pilot APPROVE → 5-seed run with `--seeds 0,1,2,3,4` and `--write-model` (or remove `--no-write-model`). Produces model artifact at `river-rats-core/models/gto_model_v9_student.json`.

**Hyperparameters identical to 12.5D'**:
- cap=3.0 hybrid weighting (per ml-architect Q3 verbatim spec)
- Pre-pad metadata-only (warm-start anchor `gto_model_v9_3way_v2.2.json`)
- 5 seeds (0-4); 80/20 stratified split
- Multi:softprob 5-class

#### Step 4: cleanup (queued NITs from prior phases)

Apply these 5 cleanup items in the same PR diff (small footprint; each ~1 line):

| Item | File | Fix |
|---|---|---|
| MEDIUM-2 from PR #134 | `river-rats-core/train_model_v9_student.py` (around line 1371) | Make "Median-litmus seed promoted to {student_output_path}" CONDITIONAL on actual model promotion (not unconditional in BLOCKED runs); update "12.5D" prose to "12.5D' / 12.5E" framing |
| 3 NITs from PR #134 | `review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` | (a) "3 deliverable files + 1 BLOCKED comm" → match actual count; (b) REPORT references list cite 12.5D' (PR #130), not 12.5D (PR #125); (c) line 71 "Schema discoveries surfaced during 12.5D" → "during 12.5D'" |
| NIT-1 from PR #139 | `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` | §3.T8 wording: clarify 36 hands was design-intent; dispatch (PR #133) compressed to 22 (+14 manual = 110 total). Add post-dispatch-compression note. |
| PILOT_595 cosmetic (from PR #136 builder self-review) | `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (line ~315) | design_note describes "TPTK + nut blocker" — fix to "top-two-pair + nut blocker"; bucket + labelling unchanged |
| NIT-1 from PR #148 | `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (line 151 §"What the BLOCKED PR ships") | Fix stale `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH` filename → `BUILDER_REPORT_PHASE125E_C_RESOLVED` |

#### Step 5: trainer report

Produce `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` per 12.5C blueprint §2.4 `write_report` contract + Section E "12.5D' vs 12.5E delta":

- Section A: training metadata (corpus stats now 604, label distribution, hyperparams unchanged from 12.5D')
- Section B: reference-evaluator results (5-seed litmus, chosen seed, solver-corrected per-hand comparison)
- Section C: Gate 2.3 feature importance (P1 blockers — track if `nut_flush_block` importance moves from 0.0000 → ≥0.02 per ml-architect Q4 prediction)
- Section D: provenance hashes (warm-start anchor SHA256, xgboost version, etc.)
- Section E (NEW expanded): 12.5D' vs 12.5E delta — per-seed scores, per-class metrics, per-hand outcomes (especially the 7 shared-cause + 2 distinct-cause hands; the 4 T5 CALL hands; T1 14-CHECK hands; T7 split hands)

**Per-hand failure direction classification** (per `feedback_failure_direction_classification.md`): for each reference-set miss in 12.5E vs 12.5D' chosen seed, classify direction (under-aggress / over-aggress / class-collapse) and identify whether it flipped to correct, stayed wrong, or newly broke.

### LEAD-PROGRAMMER (gto-expert hat — pre-PR sanity check)

After Step 3 5-seed run + Step 5 report:
- Verify chosen-seed solver-corrected score against gate threshold expectations (per design §9: median 35-37 predicted; ≥33 to clear baseline)
- Verify P1 blocker importance moved from 0.0000 (in 12.5D') toward ≥0.02 (per ml-architect prediction)
- Verify the 7 shared-cause hands (MW-17/24/25/40/42/45/47) — how many flipped to correct?
- Verify the 4 T5 CALL hands now have explicit CALL training data; does the booster learn the `nut_flush_block × villain_air` interaction?
- Verify MW-31/MW-46 (distinct-cause) — both stayed wrong as predicted (feature-surface gap)?

Document gto-expert-hat findings in §"gto-expert-hat sanity" section of the trainer report.

### LEAD-PROGRAMMER (architect hat — only if pilot or full STOPs)

If any STOP fires, swap to architect hat and produce `BUILDER_BLOCKED_PHASE125E_E_*.md` documenting the failure mode + plausible directions. Do not improvise around stop conditions.

### Deliverable scope (PR diff)

Exactly **8 files** (3 data + 1 model + 1 report + 3 cleanup edits — unless cleanup edits collapse into fewer files):

1. `data/corpus_combined_604_2026-05-05.jsonl` — NEW (merged situations)
2. `data/corpus_combined_604_labels_2026-05-05.jsonl` — NEW (merged labels)
3. `river-rats-core/models/gto_model_v9_student.json` — NEW (model artifact, only if 5-seed succeeds)
4. `review/comms/PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` — NEW (trainer report)
5. `river-rats-core/train_model_v9_student.py` — UPDATE (MEDIUM-2 V-X4 fix at line 1371)
6. `review/comms/PROGRAMMER_REPORT_PHASE125D_PRIME_TRAINER_2026-05-04.md` — UPDATE (3 NITs)
7. `review/comms/PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` — UPDATE (NIT-1 PLAN §3.T8 wording)
8. `review/comms/BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` — UPDATE (PILOT_595 cosmetic + NIT-1 stale filename)

If 5-seed run STOPs (pilot fails OR gate threshold issue), file 3 (model artifact) is correctly absent → 7 files; trainer report documents the BLOCKED state.

### Stop conditions (any phase)

- Combined corpus merge produces row count ≠ 604 → STOP, fix
- `pilot_hand_id` cardinality ≠ 604 (collisions) → STOP, fix
- Pilot 1-seed run fails any gate → STOP per Step 2 stop conditions
- 5-seed run shows median solver-corrected < 31 (regression vs 12.5D') → STOP, do NOT promote, route to orchestrator (Path C escalation likely)
- `_StudentInferenceLike45` invariant test fails → STOP (mirror drift)
- >8 files in diff → STOP, revert extras

### What you do NOT do

- Do NOT touch existing 494-row corpus or its labels (locked)
- Do NOT change trainer hyperparameters (cap=3.0; 5 seeds 0-4; pre-pad metadata-only; warm-start anchor)
- Do NOT modify v3.4 prompt or any v3.x prompt (locked at master `a598f0a`)
- Do NOT promote model unless 5-seed median solver-corrected ≥ 33 (12.5E-F gate decides promotion; 12.5E-E only writes the artifact)
- Do NOT improvise R-2 mitigations (e.g., cap retuning) — that's 12.5G post-12.5E-F

## QC stream — what you audit (when 12.5E-E PR opens)

I will post an explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` comm pointing at the 12.5E-E PR commit hash when builder force-pushes. Per `feedback_explicit_action_trigger.md`: descriptive ("QC will audit") is not a trigger; explicit "fire now" is.

When triggered, audit scope (5 audits):

1. **Diff scope** — exactly 8 files (or 7 if no model artifact); no edits to existing source surfaces beyond `train_model_v9_student.py:1371` cleanup
2. **Citation existence** — every file:line in trainer report exists at master HEAD
3. **Combined corpus integrity** — 604 row count + cardinality checks per Step 1; sample rows from each cohort (existing 494 + new 96 parametric + new 14 manual) parse cleanly
4. **NEW: Trainer hyperparameter immutability** — diff `train_model_v9_student.py` lines containing hyperparameters (cap, seeds, hyperparam dict) against master HEAD `a598f0a`; only line 1371 V-X4 cleanup should differ
5. **NEW: Cleanup completeness** — verify all 5 queued NIT items were applied per directive §"Step 4 cleanup" table

Post `REVIEW_QC_PHASE125E_E_RETRAIN_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER pre-flight (verify trainer module + paths + dependencies on master HEAD)
2. Step 1: merge corpus + labels at file level
3. Step 2: pilot 1-seed dry-run → gate
4. Step 3: 5-seed full run (only if pilot APPROVE)
5. Step 4: apply 5 queued cleanup items
6. Step 5: write trainer report
7. gto-expert-hat sanity check
8. PR opens
9. Orchestrator posts QC audit-now trigger comm
10. Standalone QC audit
11. On QC APPROVE: orchestrator merges; 12.5E-F dispatched (gate evaluation)

## What's blocked / what's queued

**Blocked:**
- 12.5E-E PR opens → on builder pilot APPROVE + 5-seed run + report + cleanup
- 12.5E-E QC trigger → on PR open (orchestrator posts trigger comm)
- 12.5E-F dispatch → on 12.5E-E PR merge
- 12.5G cap retuning sweep → post-12.5E-F regardless of outcome

**Queued (post-12.5E-E):**
- 12.5E-F gate evaluation (median solver-corrected ≥ 33 to PROMOTE; per design §8.F)
- 12.5G cap retuning sweep (cap=2.0/2.5/3.0 on combined corpus)
- T1 outcome assessment (per PR #144 deferral): if 12.5E-F passes on MW-25, T1 rework not needed; if MW-25 still fails, T1 rework
- T8 schema gap (NEW NIT from PR #150): encode `design_action` per T8 hand in future situation factory runs (12.5+1 work, not 12.5E-E)
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete) → builder formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5E-D APPROVE: master `4070a11` (PR #150)
- 12.5E-C merged: master `a598f0a` (PR #142)
- LABELS_FINAL: master `3914fea` (PR #146)
- 12.5E-A design: master `bad1396` (PR #133)
- 12.5C blueprint: master `1e4e47e` (PR #122)
- ml-architect 12.5D' findings (Q4 H-FEAT prediction): `/tmp/ml_architect_125d_prime_findings.md` (raw, on orchestrator host)
- gto-expert 12.5D' findings (per-hand classification): `/tmp/gto_expert_125d_prime_findings.md` (raw)
- Memory: `feedback_pilot_first_for_long_jobs.md` (1-seed dry-run before 5-seed), `feedback_explicit_action_trigger.md` (QC trigger comes after PR opens), `feedback_quality_default_no_ask.md`, `feedback_failure_direction_classification.md`, `feedback_river_rats_team_structure.md`

**Status: 12.5E-E TRIGGER posted. LEAD-PROGRAMMER pilot 1-seed dry-run → 5-seed full → cleanup → report → PR. Median solver-corrected ≥ 33 = success path; < 33 = STOP, route to orchestrator. 12.5E-F gate decides promotion.**
