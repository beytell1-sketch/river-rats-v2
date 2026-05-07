---
date: 2026-05-07
from: LEAD-PROGRAMMER (builder)
to: Main terminal (orchestrator) · QC stream · Owner (FYI)
re: Phase 12.5L-SHIP-A — Phase 1 SHIP record + project memory entries + D5 deferred blueprint memo (Hybrid A→D5-deferred path)
status: REPORT — 3 deliverables complete; awaiting QC pre-merge audit
---

# Phase 12.5L-SHIP-A builder report

## §1 Dispatch summary

Per `review/comms/MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md` (master `62eae79`, PR #301), Hybrid A→D5-deferred path: SHIP v9-3way-v2.2 NOW as Phase 1 INTERIM ceiling + commit D5 (75+ feature surface) as Phase 3 deferred blueprint. 3 deliverables in this PR; ~$0; ~45-60 min wall clock.

## §2 Deliverable 1 — Phase 1 SHIP record (RESTART_PROMPT_V9_3WAY.md)

Updated `review/RESTART_PROMPT_V9_3WAY.md`:

- **Added §"12.5K experiment closure (2026-05-07)"** — documents the 3-lever ceiling table (A 33.10 ± 0.30 / B spread 0.20 / C 33.00 ± 0.00) with PR refs.
- **Added §"Production model lock"** — v9-3way-v2.2 IS the Phase 1 INTERIM production model for HU+3way. Production lock means the model artifact `river-rats-core/models/gto_model_v9_3way_v2.2.json` is left as-is. The 12.5K experiment artefact `river-rats-core/models/125k_c_e/v9_3way_125k_c_e.json` is the empirical record only.
- **Replaced §"4 True Remaining Failures"** with the corrected stay-wrong taxonomy per dispatch §"CORRECTION":
  - MW-17: PIPELINE-CANONICAL MISMATCH (1 of 4) — pipeline RAISE / canonical CALL.
  - MW-40: MODEL-STUCK PIPELINE-ALIGNED (1 of 3) — pipeline BET / canonical BET MEDIUM / model predicts CHECK.
  - MW-45: MODEL-STUCK PIPELINE-ALIGNED (2 of 3) — pipeline RAISE / canonical RAISE / model predicts CALL.
  - MW-47: MODEL-STUCK PIPELINE-ALIGNED (3 of 3) — pipeline RAISE / canonical RAISE / model predicts CALL.
- **Added "Phase 1 interim ceiling; Phase 3 D5 deferred"** framing pointing at the dispatch comm + this PR's blueprint memo.

The taxonomy correction (MW-40 was labelled "canonical CALL" in synthesis §6.1; correct is "canonical BET MEDIUM, model predicts CHECK") is load-bearing for D5 hypothesis: 3 of 4 stay-wrong are model-stuck pipeline-aligned → D5 IS the structurally-correct lever for them.

## §3 Deliverable 2 — Project memory entries

Created `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md` and added a pointer in `MEMORY.md` under the "Domain (poker)" section.

Memory file structure (per memory convention `feedback_quality_default_no_ask.md` + types §"project"):

1. **§"Phase 1 INTERIM ceiling"** — project memory (rule + Why + How-to-apply): v9-3way-v2.2 is Phase 1 INTERIM, not final ceiling. 3-lever exhaustion verified; D5 deferred per blueprint.
2. **§"Stay-wrong taxonomy (FINAL after 12.5K closure)"** — sub-sections for each hand:
   - **MW-17** — PIPELINE-CANONICAL MISMATCH project memory (Why + How-to-apply).
   - **MW-40 + MW-45 + MW-47** — MODEL-STUCK PIPELINE-ALIGNED project memory (Why + How-to-apply).
3. **§"Process memory — pre-flight 4-check semantic gap"** — the 4-check covers schema/stats/distribution/feature-presence but NOT feature-rule-semantics; pilot labelling pipeline IS the only validator for that semantic class. Lesson from PR #277 FD-suit factory bug.
4. **§"Process memory — structural arguments must cross-check v3.4 DO NOT rules"** — lesson from MW-40-VERIFICATION-C HALT and PR #236 sub-axis B contradiction. Walk DO NOT rules against canonical-target permutations BEFORE design freeze.

5 memory items total (1 ceiling + 1 mismatch + 1 model-stuck + 2 process). Owner-scope to ratify per dispatch §"Deliverable 2".

MEMORY.md index entry: `- [project_v9_3way_ceiling.md] — v9-3way-v2.2 Phase 1 INTERIM ceiling; corrected stay-wrong taxonomy (MW-17 pipeline-canonical mismatch; MW-40/45/47 model-stuck pipeline-aligned); D5 deferred per blueprint memo.`

## §4 Deliverable 3 — D5 deferred blueprint memo

Created `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (~280 lines; architect-hat / ml-architect-hat). Sections:

- **§1 Purpose** — re-open trigger spec.
- **§2 Hypothesis** — explicit pre-experiment evidence (4 supporting points; what would falsify).
- **§3 Candidate features** — 11 candidates total (3 per axis × 3 axes + 2 cross-axis):
  - MW-40: `tpmk_position_with_kicker_strength`, `multiway_checked_through_pot_aggression_score`, `board_J_position_interaction`.
  - MW-45: `broadway_density_completed_on_turn`, `draw_completion_indicator_on_turn`, `multiway_strong_hand_relative_to_completion`.
  - MW-47: `nut_fd_multiway_pressure_with_blocker`, `nut_fd_villain_range_capped_signal`, `multiway_oop_raise_target_pot_odds_inversion`.
  - Cross-axis: `villain_range_capped_pct_continuous`, `hero_strength_relative_to_villain_capped_range`.
- **§4 Pre-experiment hypothesis test** — 3-feature 1-seed pilot gate before full 11-candidate investment. Pilot gate is BINDING per `feedback_pilot_first_for_long_jobs.md`. Decision matrix: PROCEED if ≥1 of 3 candidates ≥2% importance + ≥1 stay-wrong graduates / HALT to D2 if all <1%; mixed escalates to orchestrator.
- **§5 Cost / time forecast** — Pilot ~$0; ~6-8h. Full ~$0; ~25-30h. Total Phase 3 commitment ~$0; ~30-40h.
- **§6 Stop conditions and off-ramp** — pilot stop conditions (NaN/Inf, trainer crashes, eval failures); full-D5 stop conditions (NULL, partial-lift, full-lift). Off-ramp = D2 (transformer architecture) if pilot HALTS.
- **§7 What this memo does NOT do** — no execution; production model untouched.
- **§8 Re-open trigger** — owner directive post-coaching/mobile MVP.
- **§9 References** — full chain through 12.5L synthesis + memory.

## §5 Diff scope (PR diff; matches dispatch §"Deliverable scope")

| File | Operation | Lines |
|---|---|---|
| `review/RESTART_PROMPT_V9_3WAY.md` | UPDATE (add 2 sections; replace stay-wrong table with corrected taxonomy) | +37, -7 |
| `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md` | CREATE | +60 |
| `~/.claude/projects/-home-rupertbeytell/memory/MEMORY.md` | UPDATE (add 1 index line) | +1 |
| `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` | CREATE | +280 |
| `review/comms/BUILDER_REPORT_PHASE125L_SHIP_A_2026-05-07.md` | CREATE (this report) | ~145 |

**No source/prompt/data/model edits** — production lock means leave as-is per dispatch §"What you do NOT do".

**Note on memory files**: the two memory files (`project_v9_3way_ceiling.md` and `MEMORY.md`) live in `~/.claude/projects/-home-rupertbeytell/memory/`, OUTSIDE the river-rats-v2 git repo. They are not part of the PR diff in the GitHub sense; they are local-to-builder edits that the dispatch explicitly listed as Deliverable 2 outputs. Owner-scope ratification per dispatch §"Deliverable 2" closing line: "Owner-scope to ratify these memory edits when convenient; orchestrator surfaces but doesn't unilaterally finalize."

## §6 What I did NOT do (per dispatch §"What you do NOT do")

- ❌ Did NOT execute D5 — memo only.
- ❌ Did NOT modify v3.x prompts.
- ❌ Did NOT modify river-rats-core/ source.
- ❌ Did NOT modify BATCH2 reference labels.
- ❌ Did NOT modify the 988-corpus or any prior-phase corpus.
- ❌ Did NOT change v9-3way-v2.2 model file.
- ❌ Did NOT auto-fix the synthesis's MW-40 taxonomy error in PR #297 (already merged; correction recorded in this PR's deliverables instead per dispatch instruction).

## §7 Sequencing per dispatch (UPDATED per PR #302)

The original SHIP-A dispatch (PR #301) said "ORCHESTRATOR LOOP STOPS at SHIP-A merge". That was superseded by `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (master `a382fa2`, PR #302), which acknowledges PR #300 (builder directive-receipt for HU + unified-59-surface + drop 2 J-B) as legitimate scope-expansion and queues Phase 1.5 unified-59-surface design POST-SHIP-A merge.

After SHIP-A merges:
- **Phase 1.5-A unified-59-surface design** dispatched immediately by orchestrator. Architect-hat builder produces design comm specifying: 59-surface canonical (61 - 2 J-B features); HU re-train cascade; drop-2-J-B-features migration; retrain-ordering (HU first → 3way verification → router/coaching alignment); cost/time forecast.
- LOOP CONTINUES through Phase 1.5-A design + QC + merge.
- Phase 1.5-B/C/D/E execution sub-phases per Phase 1.5-A design (HU re-train per design recommendation; owner ratifies sequencing if/when sub-phase fires).

## §7.1 Phase 1.5 unified-surface acknowledgment (per PR #302 §"Builder report adjustments")

PR #300 (`BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md`) parsed owner's directive as: HU production-readiness + unified feature surface across the chain + drop the 2 J-B features (61 → 59). Builder correctly held per `feedback_optional_is_not_authorized.md` and surfaced for orchestrator sequencing.

Orchestrator-scope verdict (PR #302 §"Builder directive-receipt acknowledged"): the directive-receipt is legitimate scope-expansion. The unified-surface direction IS structurally-aligned with long-term quality — Path Y discipline currently has 38/45/61 fragmentation across HU + 3way + experimental, and coaching pipeline integration benefits from unified surface. PR #300 merged at master `48297e4`.

This SHIP-A PR's deliverables (Phase 1 SHIP record + project memory + D5 blueprint) are ORTHOGONAL to the unified-surface direction. They record the 12.5K experiment closure regardless of next-phase choice. Throwing them away to re-sequence Phase 1.5 first (Option b in PR #302) would lose recorded work for marginal sequencing gain. SHIP-A merges → Phase 1.5-A fires.

## §7.2 Phase ordering corrected (per PR #302 §"Builder report adjustments")

| Phase | What | Status |
|---|---|---|
| **Phase 1 — SHIP-A** | This PR. v9-3way-v2.2 INTERIM lock + 12.5K experiment closure + corrected stay-wrong taxonomy + project memory + D5 blueprint memo. | EXECUTING (this PR) |
| **Phase 1.5 — unified-59-surface workstream** | Drop 2 J-B features (61 → 59); unify HU + 3way + experimental on a single 59-feature surface; HU production-readiness via re-train cascade; coaching pipeline integration. | QUEUED POST-SHIP-A MERGE |
| **Phase 2 — D5 (75+ features on unified-59 base)** | Per the deferred blueprint memo in this PR; fires POST-Phase-1.5-ship; D5 expansion happens on top of unified-59, NOT on top of fragmented surfaces. | DEFERRED (blueprint ready) |

**Important framing change vs original SHIP-A dispatch (PR #301)**: D5 is NO LONGER the immediate next-phase commitment. Phase 1.5 unified-59-surface workstream replaces it as the next-phase commitment. D5 stays blueprinted as POST-Phase-1.5 candidate. The D5 blueprint memo (`PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`) §2 hypothesis + §9 references have been updated to reflect this re-sequencing.

## §8 References

- Owner directive: 2026-05-07 ~07:39 SAST (per dispatch §"References")
- 12.5L synthesis: `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297)
- SHIP-A dispatch: `review/comms/MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md` (master `62eae79`, PR #301)
- D5 deferred blueprint: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (this PR)
- Project memory: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md` (this PR; owner-scope to ratify)
- Lever A: PR #261 / Lever B: PR #265 / Lever C: PR #293
- v9-3way-v2.2 production model: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (production lock; do NOT modify)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`

---

**Status: 12.5L-SHIP-A 3 deliverables COMPLETE. Phase 1 SHIP recorded (v9-3way-v2.2 INTERIM ceiling lock); project memory entries created (5 items; owner-scope to ratify); D5 deferred blueprint memo authored (11 candidates + binding pilot gate; re-sequenced to Phase 2 post Phase 1.5). Awaiting QC pre-merge audit. After merge, ORCHESTRATOR LOOP CONTINUES into Phase 1.5-A unified-59-surface design dispatch per `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md` (PR #302).**
