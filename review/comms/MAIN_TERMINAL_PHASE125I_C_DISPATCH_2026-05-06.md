---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5I-C — labelling round (5 sonnet × 94 hands; v3.4; pilot-first; orchestrator-side Opus tier-up)
status: TRIGGER — fire now
---

# Phase 12.5I-C — labelling round

12.5I-B merged at master `5df39f7`. 94 new situations on master across T8'-r/T9'-e/T10'-r redesigned templates. Same labelling pattern as 12.5H-C (proven to work).

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125i-c-labelling-2026-05-XX`

### Pre-flight + pilot + full + tier-up cross-check

Identical pattern to 12.5H-C dispatch (`MAIN_TERMINAL_PHASE125H_C_DISPATCH_2026-05-06.md`):
- gto-expert-hat manual review of canonical hands BEFORE labelling
- Pilot phase: first labeller × 18-20 hands across 3 templates + manuals; gate on protocol-correctness
- Full phase: 5 Sonnet × 94 = 470 calls; ≤$120 cap (per 12.5E-C precedent budget)
- v3.4 prompt
- Hero-only convention preserved
- Pre-flight join-cardinality ≥0.99 vs existing 694
- Orchestrator-side Opus tier-up cross-check post-QC-APPROVE before labels-final

### Predictions (preliminary; builder updates after pilot)

Per 12.5I-A design + 12.5I-pre diagnostic:
- T8'-redesigned (MW-25 family): predicted **BET** (corpus teaches BET-after-checked-through-multiway for non-As-public-hero spots)
- T9'-expanded (MW-40 family): predicted **BET** (TP-medium-kicker IP 4-way after PFR check)
- T10'-redesigned (MW-45 family): predicted **RAISE** (slowplay-set on AKQx-broadway-completed turn) — verify via pilot since broadway-completed-turn is the isomorph-mismatch axis we're correcting
- T-CONTROL: per design_action

If pilot reveals prediction errors (per 12.5H-C precedent), STOP and route to orchestrator for prediction update before full phase.

### Deliverable scope

3 new files:
1. `data/corpus_revision_125i_labels_raw_2026-05-XX.jsonl`
2. `data/corpus_revision_125i_labels_2026-05-XX.jsonl`
3. `review/comms/BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-XX.md`

### Stop conditions

- $120 cap reached → STOP
- Manual canonical pilot >1 divergence from prediction → STOP, route to orchestrator (per 12.5H-C precedent)
- Schema malformed → STOP
- Labeller protocol mismatch (v3.2 / v3.3) → STOP
- >3 files in diff → STOP

### What you do NOT do

- Do NOT run Opus pipeline cross-check (orchestrator handles)
- Do NOT touch existing 694-row corpus or labels
- Do NOT touch v3.x prompts
- Do NOT exceed $120 cost cap

## QC stream — what you audit (5 audits)

Same as 12.5H-C: diff scope (3 files), citations, label distribution sanity, cost reconciliation ≤$120, manual canonical correctness against predictions.

## Sequencing

1. LEAD-PROGRAMMER (gto-expert hat) reviews manual canonicals
2. Pilot phase
3. Full phase (only on pilot APPROVE)
4. PR opens
5. Orchestrator posts QC audit-now trigger
6. Standalone QC pre-merge audit
7. **Orchestrator-side Opus tier-up cross-check** post-QC-APPROVE before labels-final
8. On Opus 18+/20 agreement: orchestrator merges; dispatches 12.5I-D corpus QC

## What's blocked / what's queued

**Blocked:**
- 12.5I-C PR opens → on builder pilot APPROVE + full + report
- 12.5I-D dispatch → on PR merge + Opus tier-up

**Parallel:**
- 12.5J-B feature implementation still in progress

## References

- 12.5I-B merged: master `5df39f7` (PR #202)
- 12.5I-A design: master `d045b03` (PR #197)
- 12.5H-C precedent (labelling pattern): master `90e17dc` (PR #181)
- 12.5H-C Opus tier-up: master `690ca8f` (PR #184)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `f5472bc`)

**Status: 12.5I-C TRIGGER posted. LEAD-PROGRAMMER fires manual review → pilot → full → PR.**
