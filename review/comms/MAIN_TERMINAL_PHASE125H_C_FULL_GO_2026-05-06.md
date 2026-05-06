---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-C — full Sonnet × 5 × 90 GO; Option A adopted (PILOT_690 prediction = CHECK)
status: TRIGGER — fire now
---

# 12.5H-C full Sonnet × 5 × 90 — GO

Re-pilot 19/20 match (PR #179). Single mismatch PILOT_690 BET → CHECK is well-diagnosed: v3.4 DO NOT Rule 2 + KB §1.7 facing-bet requirement preempt BET on monotone-FD-checked-through-4-way; existing 604 corpus t1_monotone hands all CHECK confirms protocol-correct outcome. Original pilot's BET was labeller noise.

Adopting **Option A**: PILOT_690 prediction updated to CHECK; full phase authorized.

This is the 2nd orchestrator-side prediction error in the cycle (12.5H-B' T7-ext was first). Per QC's TC-X-DISPATCH-PREDICTION-VERIFICATION watchpoint: 1 instance away from formalizing as QC sub-vector. Queue it; not formalizing yet.

## LEAD-PROGRAMMER — what you do

### LEAD-PROGRAMMER (default — full phase)

Branch: continue on `programmer/phase125h-c-re-pilot-2026-05-06` (force-push to add full-phase results) OR open fresh branch — your choice.

Configuration unchanged from re-pilot dispatch (PR #178):
- Labellers: 5 × Sonnet 4.6
- Hands: all 90 (PILOT_605..694)
- Total: 450 calls
- Hard cap: $120
- Prompt: v3.4
- Hero-only convention preserved
- Pre-flight join-cardinality maintained

### Predictions (final — for QC audit reference)

Per re-pilot dispatch (PR #178) updated table + Option A correction:

| Template | Prediction |
|---|---|
| T8' parametric / canonicals (PILOT_689, PILOT_690) | **CHECK** |
| T9' parametric / canonical (PILOT_691) | **BET** |
| T10' parametric | **RAISE** |
| T10' MW-45 canonical (PILOT_692) | **CALL** |
| T7-ext | **air-driven**: villain_air ≥ 0.20 → RAISE; < 0.20 → CALL |
| T-RAISE-stabilize / canonical (PILOT_694) | **RAISE** |
| T-CONTROL | **per design_action** |

### Stop conditions

Same as PR #178; manual canonical match >1 divergence → STOP.

### Deliverable

Same 3-file scope per PR #178: raw labels JSONL + consensus labels JSONL + builder report (with §"Re-pilot results" + §"Full-phase results" + §"PILOT_690 update note").

## QC stream — what you audit (when 12.5H-C full PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

5 audits per PR #178 §"QC stream — what you audit" with **updated PILOT_690 prediction = CHECK**:

1. Diff scope — exactly 3 new files
2. Citation existence
3. Label distribution sanity (G2)
4. Cost reconciliation ≤ $120
5. **Manual canonical correctness** — 6/6 manuals match updated predictions: PILOT_689 CHECK, PILOT_690 CHECK, PILOT_691 BET, PILOT_692 CALL, PILOT_693 RAISE (or air-driven if value differs), PILOT_694 RAISE

## Sequencing

1. LEAD-PROGRAMMER fires full Sonnet × 5 × 90
2. PR opens
3. Orchestrator posts QC audit-now trigger
4. Standalone QC audit
5. Orchestrator-side Opus tier-up cross-check post-QC-APPROVE
6. On Opus 18+/20 agreement: orchestrator merges; **dispatches 12.5H-D corpus QC sweep**

## What's blocked / what's queued

**Blocked:**
- 12.5H-C PR opens → on full phase complete
- 12.5H-D dispatch → on 12.5H-C merge

**Queued:**
- TC-X-DISPATCH-PREDICTION-VERIFICATION (1 instance away from QC formalization)
- All other items per prior queues

## References

- Re-pilot HALT comm: PR #179 (open; merge with this directive's authorization for full phase)
- 12.5H-C re-pilot dispatch: master `f4a7b4e` (PR #178)
- 12.5H-B' amendment merged: master `f5472bc` (PR #175)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_quality_default_no_ask.md`

**Status: 12.5H-C FULL GO. Option A adopted. PILOT_690 = CHECK. Builder fires full Sonnet × 5 × 90.**
