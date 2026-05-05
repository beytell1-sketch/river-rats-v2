---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5H-C — labelling round (5 sonnet × 90 hands; v3.4; pilot-first; orchestrator-side Opus tier-up after Sonnet labels)
status: TRIGGER — fire now
---

# Phase 12.5H-C — labelling round

12.5H-B merged at master `094cfc2`. 90 new situations on master. Per design §6 (12.5H-A `PLAN_PHASE125H_CORPUS_EXPANSION_2026-05-06.md`): 5 sonnet × 90 = 450 labels, v3.4 prompt, $120 cap, pilot-first, hero-only convention, pre-flight join-cardinality, bucket-first protocol.

GTO-EXPERT review of 6 manual canonicals fires BEFORE labelling round per design §3 §"Track B" + §8.B exit gate. Builder swaps to gto-expert hat for self-review prior to launching.

## LEAD-PROGRAMMER — what you do

Branch: `programmer/phase125h-c-labelling-2026-05-XX` (XX = your start date)

### LEAD-PROGRAMMER (gto-expert hat — manual canonical review BEFORE labelling)

Per design §3 §"Track B" + §8.B exit gate: review the 6-8 manual canonical hands in `data/corpus_revision_125h_manual_canonicals_2026-05-06.jsonl` for poker correctness BEFORE launching the labelling pipeline. APPROVE required to proceed.

Per-hand checks (same as 12.5E-B amendment pattern):
- composition triple matches template family (T8'/T9'/T10'/T-RAISE-stabilize)
- board texture canonical for the failure pattern (MW-25/40/45/47-exact replicas)
- action history plausible (no "would never happen at the table")
- position + SPR consistent with the GTO reasoning the hand captures

Document in builder report §"gto-expert-hat manual review (pre-labelling)". If any hand fails review, route to architect hat for amendment BEFORE labelling — do NOT label flagged hands.

### LEAD-PROGRAMMER (default — labelling round)

#### Pre-flight (mandatory before launch)

- Verify `prompts/gto_labeller_v3.4.md` at master HEAD; verify Fix 2.1.1 carve-out present
- Verify `scripts/dispatch_mass_labelling.py` model-config defaults to `claude-sonnet-4-6` (per master `0eaac06` post-12.5E-C parameterization) — labelling round uses Sonnet × 5 (matches existing 604 corpus methodology)
- Verify `scripts/collect_mass_labels.py` glob handles version-agnostic naming
- Pre-flight join-cardinality: 90 new `pilot_hand_id` (PILOT_605..694) zero collision with existing 604

#### Pilot phase (per design §6.3 + `feedback_pilot_first_for_long_jobs.md`)

Pilot = first labeller × ~18-20 hands (single Sonnet labeller, 18-20 of the 90 hands selected to span all 6 templates including all 6-8 manual canonicals).

Pilot gate criteria:
- Schema correct (consensus_action, vote_count, valid JSON)
- Reasoning traces cite v3.4 carve-out clauses where applicable (T-RAISE-stabilize hands; sanity check that prompt routing works)
- Per-call cost matches Sonnet 4.6 pricing estimate (validates total budget for full)
- All ~18-20 hands receive valid label
- PILOT_605, PILOT_606, ... (manual canonical pilot hands) consensus_action matches predicted v3.4 protocol output (RAISE for T-RAISE-stabilize hands; CALL for T7-ext family; BET for T8'/T9'/T10' hands)

#### Stop conditions on pilot

- Schema malformed → STOP, fix
- Reasoning traces don't cite v3.4 → STOP, dispatch script may not route v3.4 prompt correctly
- Per-call cost > 1.5× Sonnet 4.6 estimate → STOP, revise budget
- Manual canonical pilot hand consensus disagrees with predicted v3.4 output → STOP, route back to architect hat (situation construction or v3.4 wording may have a gap; earlier the better)

#### Full phase (only on pilot APPROVE)

5 Sonnet labellers × all 90 hands = 450 labels. Hard cap $120 (per 12.5E-C precedent). Same protocol unchanged.

#### Orchestrator-side Opus tier-up cross-check (per `feedback_pilot_first_for_long_jobs.md` sub-rule)

After full Sonnet labelling completes, orchestrator (NOT builder) runs Opus single-pass cross-check on contested hands per 12.5E-C → 12.5H-pre pattern. Builder does not need to dispatch Opus pipeline; orchestrator runs via subagent. Builder produces the Sonnet labels + report; orchestrator gates "labels final" via Opus cross-check.

This means builder's 12.5H-C deliverable is Sonnet-only; "labels final" decision happens at orchestrator-side Opus cross-check phase (post-PR-merge or pre-PR-merge depending on agreement gate).

### Deliverable scope (PR diff)

Exactly 3 new files:
1. `data/corpus_revision_125h_labels_raw_2026-05-XX.jsonl` — raw 5-labeller responses (450 rows = 90 hands × 5 labellers; one row per labeller-hand pair)
2. `data/corpus_revision_125h_labels_2026-05-XX.jsonl` — consensus labels (90 rows; one row per hand with consensus_action, consensus_confidence, per-class vote counts, pilot_hand_id matching the situations file)
3. `review/comms/BUILDER_REPORT_PHASE125H_C_LABELLING_2026-05-XX.md` — report with G1-G3 self-checks (G4 fires at 12.5H-D) + gto-expert-hat manual review section + pilot phase outcome table + full phase results

### Stop conditions (full phase)

- $120 cost cap reached → STOP, partial report
- Any hand <5 labels → STOP, fix
- Consensus calculation NaN/null → STOP
- Labeller protocol mismatch (v3.2 or v3.3 used) → STOP, discard polluted run, restart with v3.4
- Manual canonical hands consensus diverges from predicted v3.4 output >1 hand → STOP, route to orchestrator (signals situation-protocol gap similar to 12.5E-C T5 issue)
- >3 files in diff → STOP, revert extras

### What you do NOT do

- Do NOT run Opus pipeline cross-check (orchestrator handles tier-up; builder is Sonnet-only at this phase)
- Do NOT touch existing 604-row corpus or its labels
- Do NOT modify v3.4 prompt or any v3.x prompt
- Do NOT label hands that gto-expert-hat self-review flagged (resolve flags at architect hat first)
- Do NOT exceed $120 cost cap

## QC stream — what you audit (when 12.5H-C PR opens)

I will post explicit `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR<X>_*.md` when builder force-pushes.

When triggered (5 audits — same as 12.5E-C amendment pattern):

1. **Diff scope** — exactly 3 new files; no edits to existing source surfaces or 604-corpus data files
2. **Citation existence** — every file:line in builder report exists at master HEAD
3. **Label distribution sanity (G2)** — 90 hands, all 5 classes represented; no class with 0 labels (informational)
4. **Cost reconciliation** — total ≤ $120; per-call cost matches Sonnet 4.6 pricing; 450 calls completed (or partial documented per stop condition)
5. **Manual canonical correctness** — verify the 6-8 manual canonical hands consensus_action matches predicted v3.4 output per design §3 (similar to 12.5E-C PILOT_599/600 H-FEAT primary verification but extended to all manual canonicals); HOLD if any manual diverges from prediction without explanation in builder report

Post `REVIEW_QC_PHASE125H_C_LABELLING_*.md`. APPROVE or HOLD.

## Sequencing

1. LEAD-PROGRAMMER (gto-expert hat) reviews 6-8 manual canonicals; APPROVE → proceed
2. LEAD-PROGRAMMER (default) pre-flight + pilot phase
3. Pilot APPROVE → full Sonnet × 5 × 90 run
4. PR opens
5. Orchestrator posts QC audit-now trigger
6. Standalone QC pre-merge audit
7. **Orchestrator-side Opus tier-up cross-check** (post-QC-APPROVE; before "labels final" merge)
8. On Opus 18+/20 (or all-90 verified) agreement: orchestrator merges; **dispatches 12.5H-D corpus QC sweep**
9. On Opus material divergence: route back to LEAD-PROGRAMMER for full Opus × 5 relabel via pipeline (per 12.5E-C escalation pattern)

## What's blocked / what's queued

**Blocked:**
- 12.5H-C PR opens → on builder pilot APPROVE + full Sonnet run + report
- 12.5H-C QC trigger → on PR open
- 12.5H-C labels-final gate → on QC APPROVE + orchestrator Opus cross-check
- 12.5H-C merge → on labels-final gate
- 12.5H-D dispatch → on PR #142 (sic; 12.5H-C) merge

**Queued:** all items per PR #168 §"What's blocked / queued"

## References

- 12.5H-A design (12.5H-C scope): master `858b032` (PR #165)
- 12.5H-B situations + manuals merged: master `094cfc2` (PR #169)
- 12.5H-A dispatch: master `5f9c507` (PR #164)
- 12.5E-C labelling round (structural template): master `a598f0a` (PR #142) + Opus cross-check pattern: master `3914fea` (PR #146)
- v3.4 prompt: `prompts/gto_labeller_v3.4.md` (master `a598f0a`)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md` (pilot-first + tier-up sub-rule), `feedback_river_rats_team_structure.md`, `feedback_solver_vs_expert_labels.md`, `feedback_bucket_first_labelling.md`

**Status: 12.5H-C TRIGGER posted. LEAD-PROGRAMMER manual review → pilot Sonnet → full Sonnet × 5 × 90 → Sonnet PR. Orchestrator-side Opus tier-up post-QC. Labels-final gate after both clear. 12.5H-D unblocks on merge.**
