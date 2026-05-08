---
date: 2026-05-08
from: River Rats QC (standalone stream)
to: Main terminal (orchestrator) · Owner · LEAD-PROGRAMMER (architect-hat / default)
re: PR #303 — 12.5L-SHIP-A (v9-3way-v2.2 Phase 1 INTERIM lock + corrected stay-wrong taxonomy + D5 deferred blueprint; Phase 1.5 queued) — pre-merge audit
verdict: PASS
severity_summary: 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
audit_type: pre-merge milestone (Phase 1 INTERIM production lock + load-bearing taxonomy correction + D5 blueprint)
qc_branch: qc/pr303-125l-ship-a-review-2026-05-08
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR303_2026-05-07.md (master `434dabe`, PR #304)
target_pr_head: da9d3d5665b23782010a25beefdf0e9bf5bd3d8a
---

# QC pre-merge audit — PR #303 (12.5L-SHIP-A)

## Result

**PASS** (0 BLOCKER, 0 SHOULD_FIX, 0 NIT). 40th solo cycle. Diff is exactly the dispatched 3-deliverable scope; corrected stay-wrong taxonomy is the authoritative record across both the RESTART_PROMPT and the project memory; v9-3way-v2.2 production model file untouched; D5 blueprint is a single committed path (not a menu) with a binding pilot gate; PR #302 mandatory amendments present in both the blueprint memo AND the builder report.

## Audit-item walkthrough (7 items per trigger)

### 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)

PR diff: 3 files in repo (333 additions / 10 deletions).

| File | Operation | Lines |
|---|---|---|
| `review/RESTART_PROMPT_V9_3WAY.md` | UPDATE | +42 / -10 |
| `review/comms/BUILDER_REPORT_PHASE125L_SHIP_A_2026-05-07.md` | CREATE | +129 |
| `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` | CREATE | +162 |

`grep -E '^(river-rats-core/|prompts/|training-data/|data/|.*\.py$|.*\.csv$|.*\.jsonl$|.*\.json$)'` against `git diff master...pr303-tmp --name-only` returns **0 matches**. No source/prompt/data/model edits. `git log master..pr303-tmp -- river-rats-core/models/gto_model_v9_3way_v2.2.json` is empty — production model artifact unchanged on the PR branch.

Memory file (`~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`) and the MEMORY.md index entry exist outside the repo as Deliverable 2 of the dispatch; surfaced for owner ratification per dispatch §"Owner-scope to ratify these memory edits when convenient." **Owner-scope perimeter held.**

### 2. Stay-wrong taxonomy corrected per dispatch §"CORRECTION"

`review/RESTART_PROMPT_V9_3WAY.md` lines 120-123:

| Hand | Pipeline | Canonical | Model | Taxonomy |
|---|---|---|---|---|
| MW-17 | RAISE (Path A re-tag) | CALL | — | **PIPELINE-CANONICAL MISMATCH** (1 of 4) |
| MW-40 | BET (25/25 Sonnet + 5/5 Opus) | BET MEDIUM | CHECK | **MODEL-STUCK PIPELINE-ALIGNED** (1 of 3) |
| MW-45 | RAISE | RAISE | CALL | **MODEL-STUCK PIPELINE-ALIGNED** (2 of 3) |
| MW-47 | RAISE | RAISE | CALL | **MODEL-STUCK PIPELINE-ALIGNED** (3 of 3) |

Matches dispatch §"CORRECTION" exactly. The MW-40 taxonomy fix is load-bearing (3 of 4 stay-wrong are model-stuck pipeline-aligned → D5 feature-surface expansion is the structurally-correct lever for them) and is mirrored in `project_v9_3way_ceiling.md` §"Stay-wrong taxonomy (FINAL after 12.5K closure)" — single authoritative version across both artifacts. ✓

### 3. v9-3way-v2.2 production lock recorded; model not modified

`RESTART_PROMPT_V9_3WAY.md` §"Production model lock":
- "**v9-3way-v2.2 IS the Phase 1 INTERIM production model for HU+3way.**" with "Interim" framing pointing at the dispatch comm.
- "**Model artifact**: `river-rats-core/models/gto_model_v9_3way_v2.2.json` — DO NOT modify. Production lock means leave as-is."

Model file unchanged on PR branch (verified via `git log master..pr303-tmp -- river-rats-core/models/gto_model_v9_3way_v2.2.json` empty).

INTERIM framing consistent with `project_v9_3way_ceiling.md` §"Phase 1 INTERIM ceiling" + dispatch §"Phase 1 (NOW)" + PR #302 §"Phase ordering corrected." No spec drift between the INTERIM ceiling claim and the Phase 1.5 supersession plan. ✓

### 4. D5 blueprint comprehensive; committed-path single sequencing

`review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` 9-section structure:

- **§1 Purpose** — re-open trigger spec ✓
- **§2 Hypothesis** — explicit pre-experiment evidence (4 supporting points + falsification condition) ✓
- **§3 Candidate features** — 11 candidates total ✓
  - §3.1 MW-40: 3 (`tpmk_position_with_kicker_strength`, `multiway_checked_through_pot_aggression_score`, `board_J_position_interaction`)
  - §3.2 MW-45: 3 (`broadway_density_completed_on_turn`, `draw_completion_indicator_on_turn`, `multiway_strong_hand_relative_to_completion`)
  - §3.3 MW-47: 3 (`nut_fd_multiway_pressure_with_blocker`, `nut_fd_villain_range_capped_signal`, `multiway_oop_raise_target_pot_odds_inversion`)
  - §3.4 cross-axis: 2 (`villain_range_capped_pct_continuous`, `hero_strength_relative_to_villain_capped_range`)
- **§4 Pre-experiment hypothesis test** — BINDING pilot gate (§4.2 PROCEED/HALT/REPORT decision matrix); §4.3 explicit reference to `feedback_pilot_first_for_long_jobs.md` ✓
- **§5 Cost / time forecast** — Pilot ~$0/~6-8h; Full ~$0/~25-30h; Total ~$0/~30-40h ✓
- **§6 Stop conditions and off-ramp** — pilot stop conditions (NaN/Inf, trainer crashes, eval failures); full-D5 stop conditions (NULL, partial-lift, full-lift); D2 off-ramp on pilot HALT ✓
- **§7 What this memo does NOT do** — 7 explicit negatives ✓
- **§8 Re-open trigger** — owner directive post-coaching/mobile MVP ✓
- **§9 References** — full chain through 12.5L synthesis + memory ✓

**Single committed sequencing**: Phase 1 SHIP-A → Phase 1.5 unified-59-surface workstream → Phase 2 D5 (this blueprint, post Phase 1.5 ship). Not a menu of D-directions. Compliant with `feedback_quality_default_no_ask.md` "single committed path." ✓

TC-23 EXISTENCE check on cited infrastructure paths (master HEAD): `PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md`, `MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md`, `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md`, `BUILDER_DIRECTIVE_RECEIPT_HU_PRODUCTION_AND_UNIFIED_SURFACE_2026-05-07.md`, `BUILDER_REPORT_PHASE125K_C_E_CORPUS_AND_RETRAIN_2026-05-07.md`, `river-rats-core/feature_extractor.py`, `river-rats-core/models/gto_model_v9_3way_v2.2.json` — all GREEN. The 12.5J-B reference (`BUILDER_REPORT_PHASE125J_B_FEATURE_IMPLEMENTATION_2026-05-06.md`) also exists at master HEAD. ✓

### 5. Memory edits structured per memory convention

`~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`:

- **Frontmatter present** — name / description / type=project / originSessionId. ✓
- **§"Phase 1 INTERIM ceiling"** — rule + **Why:** + **How to apply:** ✓
- **§"Stay-wrong taxonomy (FINAL after 12.5K closure)"** — sub-sections per axis (MW-17 mismatch + MW-40/45/47 model-stuck), each with **Why:** + **How to apply:** ✓
- **§"Process memory — pre-flight 4-check semantic gap"** — **Why:** + **How to apply:** ✓
- **§"Process memory — structural arguments must cross-check v3.4 DO NOT rules"** — **Why:** + **How to apply:** ✓
- **§"References"** — full PR chain ✓

`MEMORY.md` index updated at line 60 in the "Domain (poker)" section: `- [project_v9_3way_ceiling.md](project_v9_3way_ceiling.md) — v9-3way-v2.2 Phase 1 INTERIM ceiling; corrected stay-wrong taxonomy (MW-17 pipeline-canonical mismatch; MW-40/45/47 model-stuck pipeline-aligned); D5 deferred per blueprint memo.` Single line, under 200 char hint, non-truncating. ✓

The dispatch listed 5 memory items (1 ceiling + 1 MW-17 + 1 MW-40/45/47 + 2 process); the file consolidates the MW-40/45/47 trio into a single sub-section under the stay-wrong taxonomy heading. Substance is fully present; structural consolidation does not lose information. ✓

### 6. TC-X-OWNER-SCOPE-DISCIPLINE (20th formal use)

Dispatch §"What you do NOT do" enumerates 7 negatives:
1. Do NOT execute D5 — memo only ✓ (D5 blueprint §7 confirms; no source/data edits in PR diff)
2. Do NOT modify v3.x prompts ✓ (no prompts/ paths in diff)
3. Do NOT modify river-rats-core/ source ✓ (no river-rats-core/ paths in diff)
4. Do NOT modify BATCH2 reference labels ✓ (no training-data/ paths in diff)
5. Do NOT modify the 988-corpus or any prior-phase corpus ✓ (no data/ paths in diff)
6. Do NOT change v9-3way-v2.2 model file ✓ (verified via git log master..pr303-tmp -- on the file)
7. Do NOT auto-fix the synthesis's MW-40 taxonomy error in PR #297 ✓ (correction recorded in this PR's deliverables; PR #297 left untouched)

Builder report §6 mirrors the same 7 negatives explicitly with checkmarks. **Perimeter held on every dimension.**

Memory edits flagged "Owner-scope to ratify per dispatch §'Deliverable 2'" in builder report §3 — orchestrator surfaces, doesn't unilaterally finalize. ✓

### 7. TC-X-DISPATCH-COMPLIANCE (19th formal exercise; durable)

Dispatch (PR #301) required 4 deliverables (and PR #302 added 2 mandatory amendments):

| Deliverable | Status | Location |
|---|---|---|
| 1. Phase 1 SHIP record | ✓ | RESTART_PROMPT §"12.5K experiment closure" + §"Production model lock" + corrected §"4 True Remaining Failures" + Phase-1-interim framing |
| 2. Project memory entries (5 items) | ✓ | `project_v9_3way_ceiling.md` (1 ceiling + 1 mismatch + 1 model-stuck + 2 process) + MEMORY.md index entry |
| 3. D5 deferred blueprint memo | ✓ | `PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (9 sections; 11 candidates; binding pilot gate) |
| 4. Builder report | ✓ | `BUILDER_REPORT_PHASE125L_SHIP_A_2026-05-07.md` |
| PR #302 amendment A — D5 §"Hypothesis" + §"References" reflect Phase 1.5 unified-59 base | ✓ | D5 blueprint §2 ("D5 is re-sequenced as Phase 2, building on top of the unified-59 base — NOT on top of the current fragmented 38/45/61 surfaces. The 11 candidate features below target a 59 → 75+ transition (not 61 → 75+).") + §9 (PR #302 + PR #300 cited) |
| PR #302 amendment B — D5 re-sequenced Phase 3 → Phase 2 | ✓ | D5 blueprint §2 + §9 + closing status; builder report §7.2 phase-ordering table |
| PR #302 amendment C — Builder report §"Phase 1.5 unified-surface acknowledgment" | ✓ | Builder report §7.1 |
| PR #302 amendment D — Builder report §"Phase ordering corrected" | ✓ | Builder report §7.2 (Phase 1 EXECUTING / Phase 1.5 QUEUED POST-MERGE / Phase 2 D5 DEFERRED-BLUEPRINTED) |

LOOP STOPS → LOOP CONTINUES correction also propagated: builder report §7 closing language and final status both updated to "ORCHESTRATOR LOOP CONTINUES into Phase 1.5-A unified-59-surface design dispatch." ✓

## Critical audit emphasis (per trigger)

| Critical check | Verdict |
|---|---|
| Production lock recorded faithfully (no spec drift between INTERIM ceiling claim and Phase 1.5 supersession plan) | ✓ INTERIM framing consistent across RESTART_PROMPT, project memory, builder report §7.2, D5 blueprint §2 |
| D5 blueprint is committed-path NOT a menu | ✓ Single committed sequencing Phase 1 → Phase 1.5 → Phase 2 D5; pilot gate is BINDING per §4.2; D2 is off-ramp not alternative |
| Stay-wrong taxonomy correction is the authoritative record going forward | ✓ Corrected version in BOTH RESTART_PROMPT and project memory; synthesis (PR #297) intentionally left as historical record per dispatch instruction; new readers find correction at all forward-looking surfaces |
| D5 re-sequencing reflected in BOTH blueprint memo AND builder report | ✓ Blueprint §2 + §9 + closing status; builder report §7.2 + closing status |

## Test classes exercised

- **TC-23** (CONTENT + EXISTENCE) — diff scope content + 7 cited paths existence-checked at master HEAD
- **TC-X-OWNER-SCOPE-DISCIPLINE** (20th formal use)
- **TC-X-DISPATCH-COMPLIANCE** (19th formal exercise; durable; +2 PR #302 amendment dimensions)
- **TC-X-INTRA-PLAN-CONSISTENCY** (informal — INTERIM ceiling + stay-wrong taxonomy cross-checked across RESTART_PROMPT / memory file / D5 blueprint / builder report; all four authoritative surfaces consistent)
- **TC-X-METHODOLOGY-RULE-CROSSCHECK** (informal — D5 blueprint single-committed-path rule per `feedback_quality_default_no_ask.md`; pilot-first BINDING gate per `feedback_pilot_first_for_long_jobs.md`; D1 forbidden per `feedback_solver_vs_expert_labels.md` honored in §3 — no oracle-direct labelling proposed)

No new class additions; all hits durable. The 7-item ship-format audit pattern carries through cleanly to the milestone-PR class.

## Smarter-over-time

This is the second milestone-class PR audited under the 7-item ship-format (after PR #297 synthesis). The pattern holds: the audit reduces to (a) diff-scope perimeter + production-lock content checks, (b) cross-artifact consistency on the load-bearing claim (here: corrected stay-wrong taxonomy), (c) committed-path verification on the deferred blueprint, (d) dispatch-compliance against the original directive PLUS any superseding amendments (PR #302 in this case).

Closing-phase milestone PRs that span "experiment record + production lock + deferred-next-lever blueprint + memory ratification surfacing" are now a durable template — third instance after v8 → v9-3way migration ship-gate and PR #297 12.5L synthesis. Worth carrying forward as a reusable audit format for analogous future ship-gates (Phase 1.5 ship, Phase 2 D5 ship, v9-4way ship).

## Gates

PR #303 cleared from QC side. **0 BLOCKER, 0 SHOULD_FIX, 0 NIT.**

Per dispatch §"What gates": PR #303 merge → on QC PASS. Orchestrator may proceed to merge. After PR #303 + this verdict comm merge, orchestrator dispatches Phase 1.5-A unified-59-surface design (architect-hat) per `MAIN_TERMINAL_SHIP_A_FIRE_AND_PHASE15_QUEUE_2026-05-07.md`. **LOOP CONTINUES.**

## Cycle stats

- 40th solo QC cycle.
- Wall clock: ~12 min.
- LLM cost: $0.

---

**Verdict: PASS · 0/0/0 · milestone-class Phase 1 INTERIM lock cleared from QC side · Phase 1.5-A design dispatch fires next per PR #302.**
