---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice — owner directive 2026-05-07 ~07:39 SAST)
re: PR #297 merged (QC PASS; 12.5L synthesis); owner directive: "best long term quality focused approach" + "proceed"; orchestrator decides Hybrid A→D5-deferred path; dispatch 12.5L-SHIP-A (lock v9-3way-v2.2 + D5 deferred blueprint memo)
status: DIRECTIVE — fires LEAD-PROGRAMMER on 12.5L-SHIP-A — fire now
---

# 12.5L-SHIP-A dispatch — Hybrid A→D5-deferred

PR #297 (12.5L gate-eval synthesis) merged at master `ad84d78`. Owner directive 2026-05-07 ~07:39 SAST: "please recommend best long term quality focused approach band proceed."

## Orchestrator decision: Hybrid A→D5-deferred

Owner explicitly granted WHAT-decision authority on this gate ("recommend best long-term... and proceed"). Per `feedback_orchestrator_decides_not_recommends.md` + `feedback_quality_default_no_ask.md`: orchestrator commits to a single path and executes.

### Why not pure Option A (synthesis recommendation)

Synthesis §5.2 reasoning #2 ("production-readiness ROI is unfavorable for Option B") is **timeline-conditional framing** — explicit anti-pattern per `feedback_quality_default_no_ask.md`. Pure A locks in a 15%-wrong model as "final ceiling" prematurely. The 4 stay-wrong axes are KNOWN structural defects that long-term-quality should NOT permanently accept.

### Why not pure Option B

Synthesis §4.2 enumerates 5 candidate D-directions (D1-D5) with no committed sequence — that's an **open-questions-in-proposal anti-pattern**. Long-term-quality is committed paths.

### Why D5 specifically

| Direction | Eligibility |
|---|---|
| D1 (oracle-direct labelling) | FORBIDDEN per `feedback_solver_vs_expert_labels.md` ("Solver verifies/researches only; NEVER use solver as training labels") |
| D2 (transformer architecture) | High architecture cost; speculative; no pre-experiment evidence |
| D3 (meta-learning task heads) | Speculative; no pre-experiment evidence |
| D4 (5000+ corpus expansion via untested labelling sources) | Requires new labelling-source qualification before scaling; cost prohibitive within current pipeline |
| **D5 (75+ feature surface)** | **Minimal architecture change; builds on 988-corpus; 3/4 stay-wrong are pipeline-aligned (MW-40/45/47) → model-layer signal extraction failure → adding features is the structurally-correct lever** |

D5 is the only candidate where pre-experiment evidence (the model-layer-stuck pipeline-aligned characterization of MW-40/45/47) directly supports the hypothesis that feature-surface expansion CAN lift.

### Hybrid plan

| Phase | What ships | When |
|---|---|---|
| **Phase 1 (NOW)** | v9-3way-v2.2 locked as production for HU+3way; 988-corpus + 61-feat student work parked; coaching/mobile unblocked to ship; explicit "interim ceiling" not "final ceiling" framing | This dispatch |
| **Phase 2 (deferred; explicit blueprint)** | D5 design memo authored in this PR; specifies the 75+ feature surface targeting MW-40/45/47 model-stuck axes; includes pre-experiment hypothesis + cost/time/risks; PARKED for future re-open | This dispatch (memo only; no execution) |
| **Phase 3 (future, after coaching/mobile MVP)** | D5 execution dispatched as fresh workstream when production-readiness deliverables progress past user-value threshold | Future session; not now |

This commits the SHIP decision (Phase 1) and the next-lever (D5) WITH BLUEPRINT, avoiding both pure-A "final ceiling lock" and pure-B "open-question menu" anti-patterns.

## LEAD-PROGRAMMER — Step: 12.5L-SHIP-A (fire on this comm merge)

Branch: `programmer/phase125l-ship-a-2026-05-07`. Base: master post-this-comm-merge.

### Scope — 3 deliverables

#### Deliverable 1: Phase 1 SHIP record

Update `review/RESTART_PROMPT_V9_3WAY.md`:
- Add §"12.5K experiment closure (2026-05-07)" documenting the 3-lever ceiling
- Add §"Production model lock" — v9-3way-v2.2 IS the production model for HU+3way at the 988-corpus 61-feat ceiling
- Update stay-wrong list with FINAL state per synthesis §6.1 (4 hands; correct taxonomy: MW-17 = pipeline-canonical mismatch; MW-40/45/47 = model-stuck pipeline-aligned)
- Add framing: "Phase 1 interim ceiling; Phase 3 D5 deferred per `MAIN_TERMINAL_PR297_RESOLUTION_AND_SHIP_A_DISPATCH_2026-05-07.md`"

**CORRECTION to synthesis §6.1**: synthesis labelled MW-40 canonical as CALL — that's incorrect. BATCH2 MW-40 canonical is BET MEDIUM (per PR #218 stay-wrong list which kept MW-40 in stay-wrong without label change). Pipeline 25/25 BET (PR #241) + Opus 5/5 BET (PR #245) = pipeline-aligned with canonical BET. MW-40 is MODEL-STUCK PIPELINE-ALIGNED (model predicts CHECK), not pipeline-canonical mismatch. Update §6.1 accordingly.

Corrected stay-wrong taxonomy:
- MW-17: pipeline RAISE / canonical CALL → PIPELINE-CANONICAL MISMATCH (1 of 4)
- MW-40: pipeline BET / canonical BET → MODEL-STUCK PIPELINE-ALIGNED (model predicts CHECK; 1 of 3)
- MW-45: pipeline RAISE / canonical RAISE → MODEL-STUCK PIPELINE-ALIGNED (model predicts CALL; 2 of 3)
- MW-47: pipeline RAISE / canonical RAISE → MODEL-STUCK PIPELINE-ALIGNED (model predicts CALL; 3 of 3)

This taxonomy correction is load-bearing for D5 hypothesis: 3 of 4 stay-wrong are model-stuck pipeline-aligned → adding features (D5) IS the structurally-correct lever for them.

#### Deliverable 2: Project memory entries

Update `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (or create new `project_v9_3way_ceiling.md` per memory convention) with:
1. **project memory**: "v9-3way-v2.2 IS the Phase 1 INTERIM ceiling for the current trainer/feature/architecture stack on 988-corpus 61-surface configuration. 3-lever exhaustion verified via Levers A/B/C in 12.5K. Phase 3 D5 deferred per blueprint memo."
2. **project memory**: "MW-17 is a labelling-pipeline-canonical mismatch (1 of 4 stay-wrong). v3.x labelling pipeline routes 'suited nut FD on 2-FD-suit board → RAISE' via KB §1.7; canonical reference is CALL with low pot odds. Augmented training via current pipeline cannot teach canonical CALL."
3. **project memory**: "MW-40 + MW-45 + MW-47 are model-stuck pipeline-aligned (3 of 4 stay-wrong). Pipeline labels match canonical; model layer cannot extract discriminating signal at current 61-feat scale. D5 (75+ feature surface) is the structurally-correct lever per the model-stuck-pipeline-aligned characterization."
4. **process memory**: "Pre-flight 4-check (Hybrid pilot-first per PR #228) does NOT catch domain-specific feature semantics like FD-suit count; pilot labelling-pipeline IS the only validator for that semantic class. Future factory designs should explicitly cross-check feature-semantic preconditions per labelling-pipeline rule."
5. **process memory**: "Structural arguments for verification rounds must cross-check against v3.4 DO NOT rules before submission — the v3.x DO NOT rules dominate over structural composition arguments in pipeline routing (lesson from MW-40-VERIFICATION-C HALT)."

Owner-scope to ratify these memory edits when convenient; orchestrator surfaces but doesn't unilaterally finalize.

#### Deliverable 3: D5 deferred blueprint memo

Author `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (architect-hat; ~1-2 pages):

- §"Hypothesis": MW-40/45/47 model-stuck pipeline-aligned can be lifted by expanding feature surface from 61 to 75+ targeting their structural patterns
- §"Candidate features" (3-7 specific candidates targeting the 3 stay-wrong axes; ml-architect-hat suggested):
  - For MW-40 (J-on-board TPMK 4-way checked-through pipeline-CHECK→canonical-BET): composition-quad + board-J-position interaction features
  - For MW-45 (broadway-completed-turn multiway under-RAISE): broadway-density + draw-completion features
  - For MW-47 (nut FD blocker on multiway should RAISE): nut-FD-multiway-pressure features (Step-18's `bet_call_multiway_oop_raise_pressure_index` was a partial step; expand the family)
- §"Pre-experiment hypothesis test" — minimal pilot to validate D5 has signal before full feature-engineering investment
- §"Cost/time forecast"
- §"Stop conditions and off-ramp"
- §"References" — full chain through 12.5L synthesis

This memo is NOT executed in this PR. It's the COMMITTED BLUEPRINT for future re-open. When owner directs Phase 3 D5 execution (post-coaching/mobile MVP), the blueprint provides the ready-to-execute architecture.

### What you do NOT do

- Do NOT execute D5 in this PR (memo only)
- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference labels
- Do NOT modify the 988-corpus or any prior-phase corpus
- Do NOT change v9-3way-v2.2 model file (production lock means leave as-is)
- Do NOT auto-fix the synthesis's MW-40 taxonomy error in PR #297 (it's merged; record correction in this PR's deliverables instead)

### Cost / time

~$0 (documentation only); ~45-60 min builder wall clock for 3 deliverables.

### Deliverable scope (PR diff)

1. `review/RESTART_PROMPT_V9_3WAY.md` (Phase 1 SHIP + corrected stay-wrong taxonomy)
2. `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md` (new memory file; owner-scope ratify)
3. `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md` (D5 architect-hat blueprint memo)
4. `review/comms/BUILDER_REPORT_PHASE125L_SHIP_A_2026-05-07.md` (the report)

## QC stream — what you audit (when SHIP-A PR opens)

Standalone audit, ~10-15 min, 7-item ship-format scope. Verify:
1. Diff scope strict (4 files; no source/prompt/data edits)
2. Stay-wrong taxonomy corrected per dispatch §"CORRECTION"
3. v9-3way-v2.2 production lock recorded; not modified
4. D5 blueprint comprehensive (hypothesis + candidates + pre-experiment + cost/risks + stop conditions + references)
5. Memory edits structured per memory convention (frontmatter + structured rule + Why + How-to-apply where applicable)
6. TC-X-OWNER-SCOPE-DISCIPLINE
7. TC-X-DISPATCH-COMPLIANCE 19th formal exercise

QC writes `review/comms/REVIEW_QC_PHASE125L_SHIP_A_2026-05-07.md`.

## Sequencing

After SHIP-A merges:
- Master is at the project's natural endpoint (12.5K experiment closed; v9-3way-v2.2 locked; D5 blueprinted)
- 0 PRs open
- ORCHESTRATOR LOOP STOPS (state E with queue empty)
- Owner directive needed to re-open (e.g., "execute D5 now" or "advance to v9-4way")

## What's blocked / what's queued

**Cleared by this comm:**
- PR #297 (12.5L synthesis) merged at master `ad84d78`
- 12.5L-SHIP-A dispatch fires
- Hybrid A→D5-deferred path committed

**Queued (post SHIP-A merge):**
- (none in v2 repo; project pivots to coaching/mobile per CLAUDE.md progressive chain)

**Pending owner re-engagement:**
- D5 execution (Phase 3) — blueprint memo provides ready spec
- v9-4way development per progressive chain — separate workstream
- Memory ratification — orchestrator surfaces; owner ratifies when convenient

## References

- Owner directive: 2026-05-07 ~07:39 SAST conversational
- 12.5L synthesis: `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` (master `ad84d78`, PR #297)
- Memory: `feedback_orchestrator_decides_not_recommends.md` (owner-grant of WHAT-decision authority via "proceed" directive), `feedback_quality_default_no_ask.md` (committed single path; no menus or open questions), `feedback_no_deadlines.md` (no timeline-conditional anti-pattern), `feedback_solver_vs_expert_labels.md` (D1 forbidden), `feedback_solver_findings.md` (blocker effect family expansion candidate)

**Status: PR #297 cleared. Hybrid A→D5-deferred committed. LEAD-PROGRAMMER fires 12.5L-SHIP-A (3-deliverable: Phase 1 SHIP record + project memory entries + D5 blueprint memo) on this comm merge. ~$0; ~45-60 min wall clock. ORCHESTRATOR LOOP STOPS at SHIP-A merge (state E, queue empty).**
