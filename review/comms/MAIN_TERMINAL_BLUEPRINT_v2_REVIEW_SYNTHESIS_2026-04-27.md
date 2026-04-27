---
date: 2026-04-27
from: Main terminal (orchestrator)
to: Owner · Architect (Phase 2.6 next dispatch) · ml-architect / gto-expert (round 2 reviews acknowledged) · QC stream
re: Blueprint v2 round 2 review synthesis — three reviews converge APPROVE; 7 mechanical corrections required (all small, none structural); architect Phase 2.6 dispatch next to produce v3
status: SYNTHESIS — round 2 complete; PR #56 corrections list locked; architect Phase 2.6 produces v3 → orchestrator merge → lead-programmer
---

# Blueprint v2 round 2 review synthesis

## Three round-2 reviews summary

| Reviewer | Verdict | Findings |
|----------|---------|----------|
| ml-architect | APPROVE-WITH-NITS | 4 pre-programmer corrections; OQ-4 confirmed resolvable (97/100 hands, 3 SB-3bet edge cases need 3-line fix) |
| gto-expert | APPROVE-WITH-NITS | 3 blocking nits (R5 board texture errors + Module 8 position clarification); module 8/9 confirmed realistic; R3-R5 mostly correct |
| QC | APPROVE clean | All vectors PASS (V-Source + V-X1 + V-X4 + V-Synthesis-1 + V-OQ-Resolution); blueprint correctly raises 2 new OQs with graceful-degradation discipline |

## Critical resolution: OQ-4 (`_opener_position` reconstruction)

**OQ-4 is technically resolvable with edge-case handler.**

- ml-architect verified across all 100 corpus records (not just 1): `prior_actions` includes preflop actions in every record; reconstruction algorithm works for 97/100 hands
- 3 edge cases (SB in 3-bet pots) require a 3-line fix using the `is_3bet_pot` field already present in feat_dict
- Path A is technically viable; the edge-case handler is the architect Phase 2.6 deliverable
- QC's broader sampling recommendation in their audit is satisfied by ml-architect's work — they did the broader sample

This dissolves the OQ-4 risk that could have blocked Path A.

## 7 corrections required before lead-programmer (Architect Phase 2.6 scope)

### From gto-expert (3 blocking)

| # | Issue | Fix |
|---|-------|-----|
| C1 | R5 Pair 5 `JsTd4d` labelled "draw-heavy paired" but board is unpaired (J/T/4 distinct) | Substitute with actually-paired draw-heavy texture (e.g. `JsJd9c` or similar paired + draw-heavy) |
| C2 | R5 Pair 4 `9h6h3h` monotone — outside Rule 11's "paired / 2-tone-flush" scope | Substitute with 2-tone-flush or paired texture in Rule 11's actual scope |
| C3 | Module 8 hero position (CO vs BTN) ambiguous per scenario; action order + `num_callers_to_bet` differ | Specify hero position per Module 8 scenario; document action-order implications |

### From ml-architect (4 corrections)

| # | Issue | Fix |
|---|-------|-----|
| C4 | R1 re-extraction script handles 97/100 hands; 3 SB-3bet edge cases incorrectly flag IS_PFA=1 | Add 3-line edge case handler using `is_3bet_pot` field |
| C5 | R2 references "v8 oracle" as warm-start base; should be `gto_model_v9_baseline_45feat.json` | Update file reference |
| C6 | R2 failure path says "STOP and report BLOCKED"; but the 45-vs-59 feature mismatch is expected and known | Replace with explicit resolution path (apply feature delta; document expected mismatch handling) |
| C7 | R2 nit: `pot_chips` field doesn't exist in converted record; should be `pot_bb > 6.0` | Field name correction |

### Non-blocking (fold into programmer phase)

- gto-expert N4: Module 8 donk range description omits semi-bluffs (draws); add nut-FD + combo-draw mention
- gto-expert N5: Module 9 soft assertion — FOLD rate should exceed 30% (SB folds more than any position in facing-bet)
- gto-expert: Pattern D (blocker-driven) escalates LOW → LOW-MEDIUM; recommend 5 blocker-explicit hands in Module 8 (non-blocking, programmer phase)
- gto-expert: Tier 1 architect handoff note — strengthen MAGG FOLD calibration timing requirement (must be ready before/with first Tier 2 MAGG batch)

## QC's HIGH-impact recommendation to lead-programmer (post-merge)

Pre-implementation verification step:
1. Sample 5-10 hands from `pilot_corpus_100_hand_2026-04-26.jsonl`; verify `prior_actions` contains preflop opener's action
2. Alternatively check source-pool record (`3way_situations_10k.jsonl`) for separate `opener_position` field
3. If neither available, implement graceful-degradation fallback (Path A still corrects SPR; IS_PFA=0 stays for old 100 hands; new 400 have correct IS_PFA from generation-time capture)

ml-architect's broader sampling already satisfies #1: works for 97/100, edge case handler covers the 3 outliers. Programmer should still verify on a fresh sample but expect the worst-case to NOT trigger.

## Decision: Architect Phase 2.6 dispatch

Apply 7 mechanical corrections to blueprint v2 → produce v3.

- C1, C2: substitute board textures (mechanical)
- C3: specify hero position per Module 8 scenario (mechanical clarification)
- C4: 3-line edge case handler in R1 algorithm spec (mechanical addition)
- C5: file reference update (mechanical)
- C6: replace failure path text with resolution path (mechanical)
- C7: field name correction (mechanical)

Corrections are mechanical — same architect agent applies them coherently. ~$10-15, ~30 min wall-time.

**Round 3 reviews NOT required.** The v2 round-2 verdict was APPROVE-WITH-NITS on mechanical corrections; running round 3 on the corrections is over-engineering. Orchestrator does a quick verification read on v3 (confirms all 7 corrections present + correctly applied) then merges.

## Sequencing

```
Architect Phase 2.6 (apply 7 corrections)
        ↓
Blueprint v3 → orchestrator quick verification
        ↓
PR + merge v3 (replaces PR #56 / v2)
        ↓
Lead-programmer dispatch (with QC's pre-implementation verification step in brief)
        ↓
[Build E1 / E2 / E3 / C2 / Tier 1 manifest sequence per QC]
```

## What is NOT changing

- v3.2 protocol unchanged
- 500 Phase A labels at master `4bce49f` preserved
- XGBoost architecture unchanged
- All 5 R-items + 2 scope additions stand from v2

## What IS changing in v3

- 7 mechanical corrections applied (C1-C7)
- Texture choices for Rule 11 boundary pairs 4 + 5 substituted
- Module 8 hero position specified per scenario
- R1 edge case handler added
- R2 references corrected; failure path replaced with resolution path

## Cumulative cost dashboard

- Today's research + audits + reviews so far: ~$220
- Architect Phase 2.6: ~$10-15
- Orchestrator verification (mechanical, no agent): $0
- Lead-programmer dispatch (forthcoming): ~$50-100 implementation work
- **Subtotal pre-implementation: ~$235**

Over Phase A's $200 cap (flagged earlier); within $700 pilot envelope.

## References

- v2 blueprint under review: `BLUEPRINT_CORPUS_GENERATION_PIPELINE_v2_2026-04-27.md` (PR #56 head `21b99fe`)
- ml-architect round 2: `REVIEW_ML_ARCHITECT_BLUEPRINT_v2_PR56_2026-04-27.md`
- gto-expert round 2: `REVIEW_GTO_EXPERT_BLUEPRINT_v2_PR56_2026-04-27.md`
- QC pre-merge audit: `~/river-rats-qc/findings/2026-04-27-pr56-pre-merge-blueprint-v2.md`
- Synthesis upstream: `MAIN_TERMINAL_BLUEPRINT_REVIEW_SYNTHESIS_2026-04-27.md` (master `f5008b9`, PR #55)

**Status: ROUND 2 SYNTHESIS COMPLETE. ARCHITECT PHASE 2.6 DISPATCH NEXT (7 MECHANICAL CORRECTIONS). NO ROUND 3 REQUIRED.**
