---
date: 2026-05-05
from: Main terminal (orchestrator)
to: QC stream
re: PR #152 (12.5E-E re-train) at commit acd9938 — audit-now trigger; fire 5-audit pre-merge sweep per PR #151 dispatch
status: TRIGGER — fire now
---

# QC pre-merge audit on PR #152 — fire now

LEAD-PROGRAMMER opened PR #152 at commit `acd9938` (12.5E-E re-train deliverable). 7 files (no model artifact per dispatch's no-promotion fallback — median 32/40 falls in 31-32 owner-tie-gate band; 12.5E-F decides promotion).

**Audit scope:** 5 audits per `MAIN_TERMINAL_PHASE125E_E_DISPATCH_2026-05-05.md` (master `31f2f74`, PR #151) §"QC stream — what you audit":

1. **Diff scope** — 7 files (3 new data/report + 4 modified); no model artifact (correctly absent per dispatch's < 33 threshold logic); no edits to existing source surfaces beyond `train_model_v9_student.py:1372` MEDIUM-2 cleanup
2. **Citation existence** — every file:line in `PROGRAMMER_REPORT_PHASE125E_E_TRAINER_2026-05-05.md` exists at master HEAD
3. **Combined corpus integrity** — `data/corpus_combined_604_2026-05-05.jsonl` + `data/corpus_combined_604_labels_2026-05-05.jsonl` each have 604 rows; `pilot_hand_id` cardinality 604/604; sample rows from each cohort (existing 494 + new 96 parametric + new 14 manual) parse cleanly
4. **Trainer hyperparameter immutability** — diff `river-rats-core/train_model_v9_student.py` against master HEAD `31f2f74`; only the MEDIUM-2 V-X4 cleanup at line 1371-1372 (and `--phase-label` parameterization) should differ; hyperparameter dict + cap=3.0 + seeds 0-4 + pre-pad metadata-only all unchanged
5. **Cleanup completeness** — verify all 5 queued NIT items applied per PR #151 §"Step 4 cleanup" table (MEDIUM-2 V-X4, 3 NITs in 12.5D' report, NIT-1 PLAN §3.T8, PILOT_595 cosmetic, NIT-1 stale filename); flag any not addressed

**Audit subject:** PR #152, branch `programmer/phase125e-e-retrain-2026-05-05`, commit `acd9938`.

**Output:** `REVIEW_QC_PHASE125E_E_RETRAIN_*.md` to `review/comms/`. APPROVE or HOLD.

## Sequencing on QC verdict

- APPROVE → orchestrator merges PR #152; dispatches 12.5E-F gate evaluation (per design §8.F: median 32 < 33 = NO PROMOTE per primary gate; ml-architect + gto-expert provide secondary-criteria input for owner WHAT decision)
- HOLD → orchestrator routes specific findings to LEAD-PROGRAMMER for amendment

## What's blocked / what's queued

**Blocked:**
- PR #152 merge → on QC APPROVE
- 12.5E-F dispatch → on PR #152 merge

**Queued for 12.5E-F:**
- ml-architect (architect hat) gate evaluation: median 32 vs predicted 35-37; H-FEAT confirmation (nut_flush_block 0.0000 → 0.0268); +1 newly-correct (MW-42) − 1 newly-broken (MW-20)
- gto-expert (gto-expert hat) per-hand review of MW-20 over-aggression (newly broken) + 5 still-failing shared-cause hands
- Owner WHAT decision on tie-gate: ship 32/40 / re-attempt with cap retuning (12.5G) / corpus expansion to 150-200 (design §4 escalation) / abandon

## References

- 12.5E-E dispatch: master `31f2f74` (PR #151)
- 12.5E-D APPROVE: master `4070a11` (PR #150)
- 12.5C blueprint: master `1e4e47e` (PR #122)
- ml-architect 12.5D' Q4 prediction (blocker importance ≥0.02): `/tmp/ml_architect_125d_prime_findings.md` — empirically confirmed at 0.0268
- Memory: `feedback_explicit_action_trigger.md` (this comm IS the trigger), `feedback_qc_routing_when_standalone_active.md`

**Status: QC trigger posted. PR #152 ready for 5-audit sweep. 12.5E-F dispatch waits on QC APPROVE + merge.**
