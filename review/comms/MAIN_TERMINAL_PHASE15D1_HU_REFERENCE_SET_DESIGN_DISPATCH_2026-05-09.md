---
date: 2026-05-09
from: Main terminal (orchestrator; standing-directive autonomous)
to: LEAD-PROGRAMMER (architect-hat lead; 6 design agents + 1 reviewer per `docs/PROCESS_GUIDE.md`) · QC stream (FYI; standalone audit on PR open) · Owner (notice; α/β resolved to β per standing directive while owner asleep)
re: Phase 1.5-D.1 — HU reference set design (30 spots × 6 axes; close-hand-anchor = v9-3way-on-59 canonical per α/β resolution); design-only, no labelling/corpus/retrain
status: DIRECTIVE — fires LEAD-PROGRAMMER architect-hat — fire now
---

# Phase 1.5-D.1 — HU reference set design dispatch

## Context (state at this dispatch)

Phase 1.5-C merged at master `b4caf38`:
- Builder PR #322 `d3c3da0`: Phase 1.5-C 5-seed re-train at 59-surface; PASS gate cleared at mean 33.00/40 ± 0.00 (matches PR #293 12.5K-C-E precedent exactly); J-B drop verified non-regressive
- QC verdict PR #324 `b4caf38`: PASS · 0/0/0
- Canonical model `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (1.86 MB) force-added to git; verified `git ls-files`-tracked at master

This dispatch fires Phase 1.5-D.1 as the FIRST sub-sub-phase of Phase 1.5-D (HU re-train cascade): design 30 HU postflop reference spots per architect's design memo §4.2 (in master).

## α/β resolution (per standing directive while owner asleep)

Per architect-hat recommendation in design memo §4.2 + standing directive: **α/β decision = β (re-anchor close-hand selection on v9-3way-on-59 model uncertainty)**.

Reasoning per architect (verbatim, paraphrased): 23 MB repo cost for Path α is a recurring infrastructure tax on every clone/fetch/CI; v9-3way handles HU spots structurally via the `num_opponents` feature in the 59-surface (HU = `num_opponents=1` is just a value of an existing input feature, not a workaround); coupling to 1.5-C output is acceptable because 1.5-C verification was already on the critical path before 1.5-D.1, and a 1.5-C HALT would have blocked 1.5-D.1 anyway, so the additional dependency is not load-bearing.

**Concrete close-hand-anchor model**: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (in master; SHA-256 verifiable from PR #322 builder report). Architect-hat uses model uncertainty (predictive entropy or class probability spread) on this model evaluated on the candidate HU spot pool to identify CLOSE hands.

This resolves the §4.2 ⚠️ owner-scope item per standing directive. If owner directs Path α on wake, orchestrator pivots: §4.2 close-hand-anchor + §4.5/§4.6 framing reverts; 1.5-D.1 design re-runs against v8-HU-38 model uncertainty after a separate infrastructure PR commits the v8 artifacts. Default: continue with β.

## LEAD-PROGRAMMER (architect-hat) — fire now

You are authorized to fire Phase 1.5-D.1 per design memo §4.2 + α/β = β resolution above. Architect-hat orchestrates 6 design agents (one per axis, parallel) + 1 reviewer agent (independent). ~$0 LLM spend; ~60-90 min wall-clock estimate (design + review).

### Single committed scope: design memo §4.2 in master

The architect's §4.2 IS the binding spec, with the α/β resolution above. Do not re-design; execute.

- **Target size** (§4.2): 30 HU postflop spots
- **Axis decomposition** (§4.2; architect committed): 6 axes × 5 hands each
  - **Axis HU-1 (made hand vs villain range)**: 5 hands; targets value-betting + protection vs slowplay
  - **Axis HU-2 (drawing hand profitability)**: 5 hands; targets semi-bluff vs check-call discipline
  - **Axis HU-3 (air with backdoors)**: 5 hands; targets float vs check-fold vs c-bet bluff
  - **Axis HU-4 (preflop aggressor postflop discipline)**: 5 hands; testing c-bet sizing + frequency on dry vs wet boards
  - **Axis HU-5 (out-of-position decisions)**: 5 hands; testing check-raise frequency, donk-bet usage, lead-out lines
  - **Axis HU-6 (river decision precision)**: 5 hands; pure river spots — value-bet sizing, bluff-catch threshold, river overbet response
- **Hand selection per axis** (§4.2; architect committed):
  - 3 of 5 CLOSE per `feedback_close_hand_selection.md`: model uncertainty on v9-3way-v22-on-59 canonical (β anchor) + poker difficulty, NOT feature-stat extremes
  - 2 of 5 CANONICAL: uncontroversial value or fold spots; serve as ground-truth anchors for inter-labeller agreement
  - Hand strength composition: TP+/draws/air per `feedback_preflop_geometry_vs_postflop_composition.md` — NOT preflop range buckets
  - **Solver-aligned bet sizes** per `feedback_solver_aligned_sizing.md`: flop 25%/66%, turn 33%/75%, river 33%/75%/150%. Adopt verbatim in spot specs; any deviation requires rationale.
  - **Terminology compliance** per `feedback_terminology_raise_vs_bet.md`: "raise = raise of existing bet; bet = first postflop bet; open = preflop opener". Architect spot-checks every spot specification.

### Design-agent dispatch (per `docs/PROCESS_GUIDE.md` §1.1, §1.2)

- **6 design agents** in parallel, one per axis. Each agent designs 5 hands for its axis. ≤ 10 hands per agent per `docs/PROCESS_GUIDE.md` §1.1 — well within bounds.
- **1 reviewer agent** (independent; reads all 30 spec files; checks card conflicts, board overlaps, hand classification, axis-coverage).
- All 7 agents dispatched in single message for parallelism per `docs/PROCESS_GUIDE.md` §1.3.

### Output (in PR diff)

1. `design/hu_reference_set/HU_30_HAND_DESIGNS.md` — top-level design doc (mirrors `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` pattern; references the 6 per-axis files)
2. `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md` — 5 hands × axis HU-1
3. `design/hu_reference_set/HU_AXIS_2_DRAWING.md` — 5 hands × axis HU-2
4. `design/hu_reference_set/HU_AXIS_3_AIR_BACKDOORS.md` — 5 hands × axis HU-3
5. `design/hu_reference_set/HU_AXIS_4_PFA_POSTFLOP.md` — 5 hands × axis HU-4
6. `design/hu_reference_set/HU_AXIS_5_OOP_DECISIONS.md` — 5 hands × axis HU-5
7. `design/hu_reference_set/HU_AXIS_6_RIVER_PRECISION.md` — 5 hands × axis HU-6
8. `review/comms/BUILDER_REPORT_PHASE15D1_HU_REFERENCE_SET_DESIGN_2026-05-09.md` — execution log: 6-agent dispatch evidence; reviewer findings; methodology compliance; per-axis CLOSE/CANONICAL split; close-hand-anchor model uncertainty methodology; deviation log

### Methodology constraints (binding)

- **Single committed path** per `feedback_quality_default_no_ask.md`: no menus; commit to one design per spot; no "Option A vs B" specs.
- **Pilot-first analog** per `feedback_pilot_first_for_long_jobs.md`: this is a DESIGN sub-sub-phase, not a long-batch-labelling. Pilot-first applies at 1.5-D.2 (labelling pipeline; pilot 5 hands → tier-up gate → full 25 hands). 1.5-D.1 is a single design batch with 6 parallel agents + reviewer.
- **No deadlines** per `feedback_no_deadlines.md`: forecast ~60-90 min; quality path beats schedule.
- **STOP conditions** per CLAUDE.md §5: design agent fails to produce coherent spec / reviewer flags structural issue (e.g., card conflict across axes; board overlap >3) / close-hand selection cannot find sufficient model uncertainty signal → STOP and report. Do NOT improvise.
- **Verify own output** per CLAUDE.md §7: builder report includes per-axis CLOSE/CANONICAL counts, model-uncertainty score for each CLOSE hand, solver-sizing compliance check (every bet specifies a solver-aligned size), terminology spot-check pass/fail per axis.

### What this PR does NOT do (mandatory negative scope)

- ❌ Does NOT execute 1.5-D.2 labelling (separate sub-sub-phase)
- ❌ Does NOT execute 1.5-D.3 corpus assembly (separate)
- ❌ Does NOT execute 1.5-D.4 retrain (separate)
- ❌ Does NOT modify any source / data / prompt / model files (DESIGN ONLY)
- ❌ Does NOT touch v8-HU-38 artifacts (Path β chosen; no commit-to-git of v8 needed)
- ❌ Does NOT pre-empt 1.5-D.2 labelling protocol (architect commits in §4.3 spec; this dispatch covers §4.2 only)
- ❌ Does NOT improvise on STOP conditions

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

Routing per `feedback_qc_routing_when_standalone_active.md`. Pre-merge QC required per `feedback_qc_required_before_approval.md` (HU reference set sets the spec for all downstream HU work — milestone-class).

10-item audit:

1. **Diff scope strict** (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE): 8 PR files (1 top-level + 6 axis breakouts + 1 builder report). NO source/data/prompt/model edits.
2. **30 hands total**: 6 axes × 5 hands each; verifiable by counting hand entries across the 6 axis breakout files.
3. **Per-axis CLOSE/CANONICAL split**: 3 close + 2 canonical per axis; 18 close + 12 canonical total.
4. **α/β resolution applied**: close-hand-anchor cited as `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (β); model uncertainty methodology documented in builder report.
5. **Solver-aligned sizing compliance**: every bet/raise size in spot specs matches flop 25/66, turn 33/75, river 33/75/150 (per `feedback_solver_aligned_sizing.md`).
6. **Terminology compliance**: spot specs use "raise"/"bet"/"open" per memory rule; spot-check sample of 10 spots.
7. **Hand strength composition**: TP+/draws/air composition triple present per `feedback_preflop_geometry_vs_postflop_composition.md`; NOT preflop range buckets.
8. **6-agent + 1-reviewer dispatch evidence**: builder report logs the 7-agent invocation with parallel-dispatch evidence per `docs/PROCESS_GUIDE.md` §1.3.
9. **Card conflict / board overlap check**: reviewer findings include cross-axis collision check; report any unresolved overlaps.
10. **TC-X-DISPATCH-COMPLIANCE**: §4.2 spec + α=β resolution + negative scope items honored.

QC writes `~/river-rats-qc/findings/2026-05-09-pr<n>-phase15d1-hu-reference-set-design.md` + cross-posts `review/comms/REVIEW_QC_PHASE15D1_HU_REFERENCE_SET_DESIGN_2026-05-09.md` + heartbeat sync to current master.

## Owner — what you gate (informational while asleep)

- Standing directive while owner asleep: orchestrator merges this dispatch + builder PR + QC verdict autonomously per quality default
- α/β = β resolution applied; on owner wake, can be reversed if owner directs Path α (orchestrator pivots; new infrastructure PR + 1.5-D.1 re-run on v8-HU-38 anchor)
- After 1.5-D.1 merges: orchestrator dispatches **Phase 1.5-D.2** (HU labelling pipeline; pilot 5 hands → Sonnet→Opus tier-up gate → full 25 hands) per design memo §4.3

## Loop status

Loop CONTINUES through 1.5-D.1 authorship + QC + merge → 1.5-D.2 dispatch (HU labelling pilot+full) → 1.5-D.3 (HU corpus assembly) → 1.5-D.4 (HU retrain on 59-surface; from-scratch per §4.5) → 1.5-E (router/coaching alignment) → Phase 2 D5 deferred per blueprint.

## What's blocked / what's queued

**Cleared by this dispatch:**
- LEAD-PROGRAMMER architect-hat fires Phase 1.5-D.1 (HU reference set design).

**Newly queued (post 1.5-D.1 merge):**
- Phase 1.5-D.2 dispatch (HU labelling pipeline) per design memo §4.3.

**Held independently:**
- α/β decision can be reversed by owner on wake; orchestrator pivots if directed.

**Re-queued (post Phase 1.5 ship):**
- Phase 2 D5 per blueprint.

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `b4caf38` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- 1.5-C merged: master `b4caf38` (PR #322 builder `d3c3da0`; PR #324 QC verdict `b4caf38`)
- Canonical model in master: `river-rats-core/models/v9_3way_v22_on_59/v9_3way_v22_on_59.json` (1.86 MB; git-tracked)
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.2
- BATCH2 design pattern reference: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md`
- 988-on-59 corpus: `data/corpus_combined_988_on_59_2026-05-09.jsonl` + labels
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_close_hand_selection.md`, `feedback_solver_aligned_sizing.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_preflop_geometry_vs_postflop_composition.md`, `feedback_orchestrator_decides_not_recommends.md`, `project_qc_heartbeat_convention.md`

**Status: LEAD-PROGRAMMER (architect-hat) fires Phase 1.5-D.1 on this comm merge. Single committed path per design memo §4.2 + α=β resolution; ~$0; ~60-90 min wall-clock to PR open. 6 design agents parallel + 1 reviewer per `docs/PROCESS_GUIDE.md`. STOP conditions per CLAUDE.md §5 escalate — no improvisation. QC standalone audit on PR open. Orchestrator merges PR + QC verdict autonomously per standing directive on PASS. Loop CONTINUES.**
