---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5I-B — situation generation per 12.5I-A design (~100 hands; T8'-redesigned, T9'-expanded, T10'-redesigned); parallel with 12.5J-B
status: TRIGGER — fire now
---

# Phase 12.5I-B — situation generation

12.5I-A merged at master `d045b03`. Builder fires factory generation per design §3 templates. 12.5I-B parallel with 12.5J-B (feature implementation; separate dispatch).

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125i-b-situation-generation-2026-05-XX`

Per 12.5I-A design §3:
- T8'-redesigned (MW-25 family): ~30-40 hands; hero NOT holding on-board top card; non-nut FD on monotone boards
- T9'-expanded (MW-40 family): ~30-40 hands; TP-medium-kicker IP 4-way after PFR check
- T10'-redesigned (MW-45 family): ~30-40 hands; AKQx-broadway-completed turn texture
- T-CONTROL: drift detection (~20 hands per design §4 if specified)

Total ~100-120 new hands; combined corpus post-12.5I: 694 + 100-120 = ~800.

### Methodology rules (standing per 12.5H-A §10)

- Hero-only convention in `prior_actions` (matches existing corpus)
- Pre-flight join-cardinality ≥0.99 vs existing 694
- design_action field per T-CONTROL hand (TC-X T8 schema gap fix)
- Solver-as-labels prohibited (situations only at this phase)

### Deliverable scope (4 files)

1. `scripts/build_corpus_revision_125i_situations.py` — NEW: factory + 3 redesigned templates + manual canonicals + G1-G3 self-checks. Reuse 12.5H-B factory script as structural template.
2. `data/corpus_revision_125i_situations_2026-05-XX.jsonl` — NEW: parametric situations
3. `data/corpus_revision_125i_manual_canonicals_2026-05-XX.jsonl` — NEW: manual canonicals (subject to GTO-EXPERT review at 12.5I-C trigger)
4. `review/comms/BUILDER_REPORT_PHASE125I_B_SITUATION_GENERATION_2026-05-XX.md` — NEW: report with G1-G3 results

`pilot_hand_id` range: PILOT_695..PILOT_794 (or per-design exact). No collision with existing 694.

### Stop conditions

- Pre-flight finds drift in cited file:lines vs design → STOP
- Per-template count <30 → STOP (12.5H demonstrated underpowering)
- G1/G2/G3 fails → STOP
- Convention not uniform → STOP
- Solver call → STOP
- >4 files in diff → STOP

## QC stream — what you audit

5 audits when 12.5I-B PR opens (same pattern as 12.5H-B). Explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` fires after builder force-push.

## Sequencing

12.5I-B → 12.5I-C labelling → 12.5I-D corpus QC → 12.5I-E re-train → 12.5I-F gate eval (parallel with 12.5J phases). Combined re-train at 12.5K when both 12.5I-E and 12.5J-E ship.

## What's blocked / what's queued

**Blocked:**
- 12.5I-B PR opens → on builder factory + report
- Subsequent 12.5I-X → on prior phase merge
- 12.5K combined re-train → on both 12.5I-E AND 12.5J-E ship

## References

- 12.5I-A merged: master `d045b03` (PR #197)
- 12.5I-A QC APPROVE: master `73963b4` (PR #200)
- 12.5I dispatch: master `c536c30` (PR #196)
- 12.5H-B (structural template): master `094cfc2` (PR #169)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`

**Status: 12.5I-B TRIGGER posted. LEAD-PROGRAMMER fires factory.**
