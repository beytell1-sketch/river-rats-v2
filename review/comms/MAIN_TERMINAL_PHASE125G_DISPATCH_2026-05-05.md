---
date: 2026-05-05
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5G — cap=4.0 retune on combined 604-hand corpus (B-then-C step 1); pilot 1-seed before 5-seed full
status: TRIGGER — fire now
---

# Phase 12.5G — cap=4.0 retune (B-then-C step 1)

12.5E-F synthesis (master `16351e1`) presented owner gate options. Per `feedback_quality_default_no_ask.md` standing rule (owner's default = slow quality), default pick = **B-then-C compound**. Orchestrator adopts without re-asking owner.

12.5G is the first half: cap=4.0 retune on the merged 604-hand corpus. Single-cap point (NOT 2.0/2.5/4.0 sweep — Opus evaluation determined 2.0/2.5 likely regress; only 4.0 is informative). Cheapest empirical bet: ~1 builder day + ~$10. Outcome decides next step:

- **Median ≥ 33 → PROMOTE** at 12.5G; ship v9-student (B succeeded; C unnecessary)
- **Median < 33 → 12.5H corpus expansion** with cap=4.0 evidence folded into design (B null result is load-bearing for C)

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125g-cap-retune-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (default — implementation)

#### Step 1: parameterize cap via CLI flag (small trainer edit)

Trainer module `river-rats-core/train_model_v9_student.py:422` currently hard-codes `min(3.0, mean_class_count / max(class_counts[c], 1))`. Parameterize:

- Add `--class-weight-cap` CLI argument with default `3.0` (preserves 12.5D'/12.5E behavior when not specified)
- Replace `min(3.0, ...)` at line 422 with `min(args.class_weight_cap, ...)`
- Update report writer (around line 1202) to log the cap value used in trainer report Section A
- Update `_build_argparse()` (line ~1380) docstring + help text

This is parameterization, NOT a hyperparameter change at the existing code path's behavior. Default remains 3.0.

#### Step 2: PILOT — 1-seed dry-run with cap=4.0

```
python3 river-rats-core/train_model_v9_student.py \
  --corpus data/corpus_combined_604_2026-05-05.jsonl \
  --labels data/corpus_combined_604_labels_2026-05-05.jsonl \
  --class-weight-cap 4.0 \
  --no-write-model \
  --seeds 0
```

**Pilot gate criteria (all must hold to proceed to Step 3):**
- Trainer accepts `--class-weight-cap 4.0` without errors
- Sample weights show new cap distribution: RAISE class boost ~4.0× (was ~3.0×); BET ~1.4×; CALL ~1.6×; CHECK/FOLD ~1.0× (unchanged)
- Held-out classification report produced; sane support per class
- Reference-evaluator gate runs and produces solver-corrected score on 1-seed
- `_StudentInferenceLike45` invariant test passes

#### Stop conditions on pilot

- Trainer crashes on `--class-weight-cap` flag → STOP, fix CLI parse
- Pre-pad mechanism fails → STOP, document
- 1-seed solver-corrected score < 28 (regression vs 12.5E baseline 32-1=31 at lower bound) → STOP, route to orchestrator (cap=4.0 actively hurts)
- 1-seed solver-corrected score > 38 (suspiciously high vs predicted 32-34) → STOP, investigate (likely overfit)
- Invariant test fails → STOP

#### Step 3: FULL — 5-seed run with cap=4.0

Pilot APPROVE → full 5-seed run with `--class-weight-cap 4.0` and write-model. Produces model artifact at `river-rats-core/models/gto_model_v9_student.json` (overwrites 12.5E-E artifact only if median ≥ 33; else artifact NOT promoted).

**Hyperparameters identical to 12.5E-E except cap:**
- cap=**4.0** (was 3.0)
- Pre-pad metadata-only (warm-start anchor `gto_model_v9_3way_v2.2.json`)
- 5 seeds (0-4); 80/20 stratified split
- Multi:softprob 5-class
- Combined 604-hand corpus + labels (same as 12.5E-E)

#### Step 4: trainer report

Produce `review/comms/PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` per blueprint §2.4 + Section F "12.5E vs 12.5G cap delta":

- Section A: training metadata (cap=4.0; everything else identical)
- Section B: reference-evaluator results (5-seed litmus + chosen seed cross-model)
- Section C: Gate 2.3 feature importance (track `nut_flush_block` movement; predicted to slightly increase from 0.0268)
- Section D: provenance hashes
- Section F (NEW): 12.5E (cap=3.0) vs 12.5G (cap=4.0) delta — per-seed scores, per-class metrics, **specific focus on MW-47** (Opus prediction: cap=4.0 may flip MW-47 to RAISE) and **MW-20** (newly broken in 12.5E; cap=4.0 may resolve or worsen)

Per-hand failure direction classification per `feedback_failure_direction_classification.md`.

### LEAD-PROGRAMMER (gto-expert hat — pre-PR sanity check)

After Step 3:
- Verify median solver-corrected against gate: ≥33 = PROMOTE; <33 = STOP for 12.5H dispatch
- Verify MW-47 outcome (Opus prediction: MAY flip under cap=4.0 due to H-FEAT activation interacting with higher RAISE weight)
- Verify MW-20 outcome (newly broken in 12.5E; cap=4.0 likely doesn't fix structural over-rotation but report behavior)
- If gate clears: confirm held-out class metrics didn't catastrophically degrade (CHECK recall floor ~0.85; CALL recall floor ~0.75)

### LEAD-PROGRAMMER (architect hat — only if needed)

If pilot or full STOPs, swap to architect hat → `BUILDER_BLOCKED_PHASE125G_*.md` documenting failure mode + cap=4.0 evidence available for 12.5H corpus design.

### Deliverable scope (PR diff)

Exactly **5 files** (or 4 if no model promotion):

1. `river-rats-core/train_model_v9_student.py` — UPDATE (parameterize cap; ~5-line edit on lines 422 + argparse + report writer)
2. `data/corpus_combined_604_2026-05-05.jsonl` — UNCHANGED (do NOT regenerate; use existing)
3. `data/corpus_combined_604_labels_2026-05-05.jsonl` — UNCHANGED
4. `review/comms/PROGRAMMER_REPORT_PHASE125G_CAP_RETUNE_2026-05-05.md` — NEW
5. `river-rats-core/models/gto_model_v9_student.json` — NEW or UPDATE if median ≥ 33 (overwrites 12.5E-E artifact only on promotion)

If gate < 33 → 4 files (no model artifact); trainer report documents the BLOCKED state + cap=4.0 evidence for 12.5H.

### Stop conditions

- Trainer parameterization edit > 10 lines diff → STOP (overscoped); should be minimal
- Pilot 1-seed gate fails → STOP per Step 2
- 5-seed median < 28 → STOP; cap=4.0 actively hurts; cap-as-lever empirically refuted
- 5-seed median 28-32 → 12.5G fails to clear; route to 12.5H (B null result feeds C design)
- 5-seed median ≥ 33 → 12.5G clears; 12.5H not needed; PROMOTE path
- >5 files in diff → STOP, revert extras

### What you do NOT do

- Do NOT touch existing 494-row corpus or 110-row 12.5E corpus or labels (locked)
- Do NOT change anything except cap parameterization (no other hyperparameter touches)
- Do NOT modify v3.x prompts (locked)
- Do NOT proceed to 12.5H without orchestrator dispatch (STOP on <33 and route)

## QC stream — what you audit (when 12.5G PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` comm pointing at the 12.5G PR commit hash when builder force-pushes.

When triggered (5 audits):

1. **Diff scope** — exactly 5 files (or 4 if no model promotion); no edits to existing source surfaces beyond `train_model_v9_student.py` parameterization
2. **Citation existence** — every file:line in trainer report exists at master HEAD
3. **Cap parameterization minimal** — diff `train_model_v9_student.py` against master `16351e1`; only parameterization changes (line 422 + argparse + report writer); zero other hyperparameter diffs
4. **NEW: cap value verification** — verify trainer ran with `--class-weight-cap 4.0` (not 3.0; not other); cap value documented in Section A
5. **NEW: corpus invariance** — verify combined 604-hand corpus + labels are byte-identical to 12.5E-E (master `b51e525`); no corpus tampering between phases

Post `REVIEW_QC_PHASE125G_CAP_RETUNE_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER pre-flight (verify trainer at master HEAD; parameterize cap; small edit)
2. Pilot 1-seed dry-run with `--class-weight-cap 4.0`
3. Pilot APPROVE → full 5-seed run
4. gto-expert-hat sanity (median + MW-47 + MW-20)
5. PR opens
6. Orchestrator posts QC audit-now trigger
7. Standalone QC audit
8. On QC APPROVE: orchestrator merges; **branches:**
   - Median ≥ 33 → orchestrator authors PROMOTE directive; v9-student ships at cap=4.0
   - Median < 33 → orchestrator authors 12.5H corpus expansion dispatch with cap=4.0 evidence folded in (B-then-C step 2)

## What's blocked / what's queued

**Blocked:**
- 12.5G PR opens → on builder pilot APPROVE + 5-seed run + report
- 12.5G QC trigger → on PR open
- 12.5G merge → on QC APPROVE
- 12.5H dispatch → on 12.5G merge AND median < 33 (if median ≥ 33, 12.5H is unneeded)

**Queued (independent of 12.5G outcome):**
- T1 outcome assessment per PR #144 deferral (MW-25 still wrong → T1 expansion likely needed if 12.5H fires)
- T8 schema gap (PR #150 NEW NIT): encode `design_action` per T8 hand in future situation factory runs
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations) → builder formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5E-F synthesis: master `16351e1` (PR #155)
- Opus second-tier evaluation (B-then-C compound recommendation): `ORCH_OPUS_125E_F_EVALUATION_2026-05-05.md` (master `16351e1`)
- 12.5E-E re-train: master `b51e525` (PR #152)
- 12.5C blueprint: master `1e4e47e` (PR #122)
- ml-architect 12.5D' Q3 cap=3.0 spec: `/tmp/ml_architect_125d_prime_findings.md`
- Memory: `feedback_quality_default_no_ask.md` (B-then-C is the slow-quality compound), `feedback_pilot_first_for_long_jobs.md` (1-seed dry-run before 5-seed), `feedback_explicit_action_trigger.md` (this comm IS the trigger), `feedback_orchestrator_decides_not_recommends.md` (default pick within scope per standing instruction)

**Status: 12.5G TRIGGER posted. LEAD-PROGRAMMER fires cap=4.0 retune (parameterized; pilot → full). Median ≥ 33 = PROMOTE; < 33 = 12.5H dispatch with cap=4.0 evidence.**
