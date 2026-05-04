---
date: 2026-05-04
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream · ML-ARCHITECT · GTO-EXPERT
re: Phase 12.5D' synthesis ADDENDUM — standalone QC findings on PR #131 (MEDIUM-1 + MEDIUM-2); 12.5E direction reinforced
status: ADDENDUM to PR #132 synthesis
---

# Phase 12.5D' synthesis — ADDENDUM (post standalone QC verdict)

Standalone QC stream delivered PR #131 verdict at master `01d0003` (PR #134, now merged): **APPROVE with 2 MEDIUM + 3 NIT**. Standalone QC pre-merge audit was solo-routed per `feedback_qc_routing_when_standalone_active.md` — no parallel general-purpose subagent this round. **Process improvement from PR #126 confirmed.** Memory rule working as intended.

PR #131 also merged at master `659c572` per QC APPROVE — 12.5D' trainer + tests + report + BLOCKED comm now on master as a re-runnable baseline alongside the 12.5D BLOCKED baseline.

## MEDIUM-1 — MW-49 newly broken (load-bearing for synthesis)

**Standalone QC caught what neither builder nor orchestrator surfaced:**

> Section B per-hand list shows MW-49 student=CHECK vs expert=BET (wrong); MW-49 was correct in 12.5D. Section E framing reports "1 of 7 [shared] flipped" but doesn't mention MW-49 newly broke.

**Net 31/40 = +1 fix (MW-24) − 1 new break (MW-49).** Score is unchanged; direction is informative.

This **changes the cap-retuning analysis** in the original synthesis (PR #132, master `5ca1e74`):

| Quantity | Original synthesis estimate | Post-MEDIUM-1 revised |
|---|---|---|
| Cap retuning probability of closing gap | ~5% (ml-architect: orthogonal to root cause) | **15-25%** (cap=3.0 demonstrably over-rotated; cap=2.0 or 2.5 might preserve MW-24 fix without breaking MW-49) |
| Direction-Ship structural read | rejected (regression) | unchanged — still rejected |
| Direction-Abandon structural read | clean close-out | unchanged |
| Direction-Data-fix structural read | only direction with non-trivial close-the-gap probability (50-70%) | **REINFORCED** — MW-49 break shows trainer-side weighting can both fix and break reference-set hands; corpus distribution is the load-bearing variable, not just weighting |

**Implication for the 12.5E direction owner already picked:**

12.5E (corpus expansion) is **reinforced** by MEDIUM-1. The finding shows:
- The reference-set is sensitive to cap-3.0 weighting in BOTH directions (one fix, one break)
- Corpus distribution is doing the structural work; weighting is a tunable on top
- With an expanded corpus (12.5E-E re-train output), weighting becomes a follow-up tunable, not the primary lever

The owner's Data-fix decision is **not revisited** by MEDIUM-1. It's strengthened.

## What MEDIUM-1 does NOT change

- 12.5E-B (situation generation, currently dispatched) proceeds as designed
- 12.5E-A design is not amended
- ml-architect 12.5D' Q4 verdict (H-FEAT primary + H-DIST secondary) stands
- gto-expert 12.5D' E-DIST/E-FEATURE classification stands

## What MEDIUM-1 DOES surface for forward planning

A cap-retuning sweep becomes valuable as a **post-12.5E-E follow-up workstream** (call it 12.5G when scheduled) — once the expanded corpus is on master and 12.5E-E re-train produces a new baseline number, run cap=2.0, 2.5, 3.0 sweeps on the new corpus to find the cap that maximizes reference-set score without introducing new breaks. This is information-only at this point; does NOT block 12.5E shipping.

Per `feedback_quality_default_no_ask.md` (slow-quality rule): cap retuning post-12.5E-E is a 1-day sweep that produces a clean data point. Quality default = include it. Queuing as 12.5G now in this addendum so the question doesn't get re-asked later. **Decision recorded:** 12.5G (cap retuning sweep) will fire automatically after 12.5E-F gate evaluation, regardless of 12.5E-F outcome (PASS or FAIL — both states benefit from knowing the optimal cap for the new corpus).

## MEDIUM-2 — V-X4 prose recurrence (queued for 12.5E-E cleanup)

> Builder claims "fixed 12.5D wording-cleanup item from QC review." Conditional topline (lines 929-934) WAS fixed. But unconditional closing footer at trainer line 1371 still emits "Median-litmus seed promoted to {student_output_path}" → "promoted to /tmp/..." in BLOCKED runs. Plus literally says "12.5D" not "12.5D'". Recurrence after a QC flag — same incident family as #18.

This is **not blocking**; standalone QC noted it as MEDIUM, not HIGH. PR #131 already merged with the cleanup outstanding.

**Queued for 12.5E-E re-train cleanup.** When LEAD-PROGRAMMER picks up 12.5E-E (re-train using existing trainer module on master with expanded corpus), the same trainer module will be touched anyway (no code changes expected per design §8.E, but minor framing/version updates are the right time to fix V-X4). Specifically:

- `train_model_v9_student.py:1371` (or wherever the closing footer lives at audit time): make the "promoted to" line conditional on actual model promotion, not unconditional
- All prose strings referencing "12.5D" → "12.5D' v9-student-12.5E" or framing-appropriate at 12.5E-E

This is a NIT-class change masked as MEDIUM only because it's a recurrence. Cleanup at 12.5E-E satisfies the recurrence flag without process churn now.

## Three NITs (acknowledged, not actioned now)

- NIT-1: "3 deliverable files + 1 BLOCKED comm" framing (improvement over PR #126; no action)
- NIT-2: REPORT references list cites 12.5D dispatch (PR #125) instead of 12.5D' (PR #130) — cosmetic, ride along on 12.5E-E cleanup
- NIT-3: REPORT line 71 says "Schema discoveries surfaced during 12.5D" in 12.5D' report — cosmetic, ride along on 12.5E-E cleanup

## Process-positive observation (worth preserving)

Standalone QC working solo this cycle, per `feedback_qc_routing_when_standalone_active.md`:
- Caught MEDIUM-1 (MW-49) that subagent-style audit on 12.5D missed
- Solo-routed; zero parallel general-purpose subagent
- Surfaced 2 MEDIUM + 3 NIT vs subagent-style audit's 1 NIT + 1 NIT

The QC stream's stated process improvement from PR #126 is empirically confirmed at PR #131. Memory rule continues to apply.

## Updated authority chain on master

- 12.5D BLOCKED baseline: PR #126 (master `d7d2cdd`)
- 12.5D synthesis: PR #128 (master `d6dd36d`)
- 12.5D' dispatch: PR #130 (master `1b95648`)
- 12.5D' synthesis: PR #132 (master `5ca1e74`)
- **12.5E design + 12.5E-B dispatch**: PR #133 (master `bad1396`)
- **PR #131 BLOCKED 12.5D' baseline (merged on QC APPROVE)**: PR #131 (master `659c572`)
- **PR #134 QC finding**: PR #134 (master `01d0003`)
- **THIS ADDENDUM**: lands at next merge

## What does NOT happen at this addendum

- No 12.5E direction revisit (owner picked Data-fix; MEDIUM-1 reinforces)
- No new owner gate (this is informational; 12.5E-B builder action is unchanged)
- No PR amendment to 12.5E-A design (reinforced, not amended)
- No PR amendment to LEAD-PROGRAMMER's 12.5E-B dispatch (unchanged scope)

## Forward agenda (unchanged + 12.5G added)

1. **In flight:** LEAD-PROGRAMMER 12.5E-B (situation generation)
2. **On 12.5E-B PR open:** standalone QC + GTO-EXPERT review of 14 manual canonicals + ml-architect advisory
3. **12.5E-C** labelling round (5 sonnet labellers × 110 hands; $120 cap) — dispatched on 12.5E-B merge
4. **12.5E-D** QC the new corpus (4 gates per design §7)
5. **12.5E-E** re-train (existing trainer module reused; **MEDIUM-2 V-X4 cleanup happens here**)
6. **12.5E-F** gate evaluation (reference-set primary, ≥33 to clear baseline)
7. **NEW: 12.5G** cap retuning sweep (cap=2.0, 2.5, 3.0 on the expanded corpus) — fires automatically after 12.5E-F regardless of outcome

## References

- 12.5D' synthesis (the comm this addends): `MAIN_TERMINAL_PHASE125D_PRIME_SYNTHESIS_OWNER_GATE_2026-05-04.md` (master `5ca1e74`, PR #132)
- QC finding (this addendum's source): `QC_FINDING_2026-05-04_PR131_PHASE_12_5D_PRIME.md` (master `01d0003`, PR #134)
- 12.5D' BLOCKED baseline (now merged): trainer + tests + report + BLOCKED comm at master `659c572`, PR #131
- 12.5E design + dispatch: `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` + `MAIN_TERMINAL_PHASE125E_DISPATCH_2026-05-04.md` (master `bad1396`, PR #133)
- Memory: `feedback_qc_routing_when_standalone_active.md` (rule confirmed at PR #131), `feedback_quality_default_no_ask.md` (12.5G queued in-addendum, no separate ask), `feedback_orchestrator_decides_not_recommends.md`

**Status: ADDENDUM. MEDIUM-1 surfaced (MW-49 newly broken; cap retuning probability revised 5% → 15-25%; 12.5E direction REINFORCED). MEDIUM-2 queued for 12.5E-E cleanup. 12.5G cap-retuning sweep queued for post-12.5E-F. Owner WHAT decision on 12.5E unchanged. LEAD-PROGRAMMER 12.5E-B in flight.**
