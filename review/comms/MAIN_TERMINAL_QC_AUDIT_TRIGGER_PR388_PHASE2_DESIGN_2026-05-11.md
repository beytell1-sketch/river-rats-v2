---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous)
to: QC stream
re: PR #388 — Phase 2-A unified surface design memo (D5 refresh + 4-way feature gap + AMENDMENTS 1+2+3 folded; design-only; 21 candidates → 74-80 surface; 9 owner-scope items; pre-Phase-2-B pilot gate) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire audit now on PR #388 (Phase 2-A unified surface design memo)

PR #388: `builder-phase2-a-design-memo-2026-05-11`. Head `ee1da68cf...`. Title: "Builder Phase 2-A design memo: D5 refresh + 4-way feature gap + AMENDMENTS 1+2 (21 candidates → 74-80 surface)".

Builder Path-A-amended PR #388 to fold AMENDMENT 3 (PR #389):
- Commit 1 (cd5cc4f): base design memo with AMENDMENTS 1 + 2 folded (street distribution + re-raise × players-left)
- Commit 2 (ee1da68c): AMENDMENT 3 fold (labeller readiness §X + 5-way scope §Y; §6.8 + §6.9 new owner-scope items; refs §11/12)

**Combined state: design memo covers Phase 2 dispatch + all 3 AMENDMENTS.** Design-only scope; no code/data/corpus/training touched. Owner-scope items count: 9 (was 7 in base memo; +2 from AMENDMENT 3).

## Diff summary (per `gh pr view 388` + git diff)

2 commits / 1 file:
- `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` — NEW (cd5cc4f: 600 lines; ee1da68c: +126/-2 lines AMENDMENT 3 fold)

No source/data/test/model files touched.

## Audit scope (~30-45 min — larger than typical owing to multi-amendment fold)

### Part A — Base memo (commit cd5cc4f) substantive coverage

Per Phase 2 dispatch (PR #385) §1-§7 + AMENDMENT 1 (PR #386) §3.X + AMENDMENT 2 (PR #387) §3.Y:

1. **§1 current state attestation**: architect confirms 59-feat production surface; lists feature gaps; cites file paths
2. **§2 D5 blueprint refresh**: 11 candidates targeting MW-40/45/47 stay-wrong axes verified
3. **§3 4-way feature gap analysis**: includes players-left + re-raise × players-left interaction (AMENDMENTS 1 + 2)
4. **§3.X street distribution analysis (AMENDMENT 1)**: 4-way reference 51/31/11/6 (flop/preflop/turn/river) weighted; lookalike weighting; feature street-conditionality; ship-gate per-street; post-ship behavior — all 6 sub-items present
5. **§3.Y re-raise × players-left (AMENDMENT 2)**: GTO theory + gap verification + candidate features (`street_raise_count`, `is_4bet_or_higher_pot`, `live_raisers_behind`, `closing_action`, `squeeze_risk_index`, `reverse_implied_odds_signal`) + pilot inclusion + reference set + ship-gate — all 6 sub-items present
6. **§4 surface lock proposal**: 21 candidates → 74-80 surface; 35-hand 4-way reference street-weighted; 6-candidate pilot (3 D5 + 2 4-way + 1 re-raise)
7. **§5 sub-phase decomposition 2-A through 2-H**: design-only scope respected
8. **§6 owner-scope items**: 7 in base; surfaces what owner must ratify before 2-B fires
9. **§7 negative scope**: NO build/train/corpus

### Part B — AMENDMENT 3 fold (commit ee1da68c) substantive coverage

Per AMENDMENT 3 (PR #389) Item 1 + Item 2:

10. **§X labeller readiness (Item 1)**:
    - HU brief survey + extends-naturally-vs-needs-new-design analysis present
    - 4-way labeller brief design: multiway range-chain reasoning, players-left+squeeze-pressure prompt, closing-action decision trees, anti-rule-based boilerplate (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md` + FL6 evidence), bucket-first compliance
    - Calibration set: 29 hands (architect call; vs HU 24-28; verify reasoning)
    - 5-hand pilot validation with STOP-condition gate
    - Sub-phase 2-E.0 inserted before 2-E
11. **§Y 5-way scope (Item 2)**:
    - State assessment (when production routes to 5-way; frequency estimates)
    - **Flagged finding: "5-way file MISSING on disk; falls back to vNext-HU"** — architect surfaces this as material state observation; QC verifies independently (`git ls-files river-rats-core/models/gto_model_v9_5way.json` + production fallback behavior); if confirmed, this is a NEW owner-scope item (rollback safety concern OR routing-table mis-config)
    - Surface-size implication (75+ applies)
    - Corpus implication (multiway scaling; existing PB data)
    - Architect proposal: Option B = defer to Phase 3 (per quality default + scope discipline); surfaces as owner-scope #9
    - Quality-default trade-offs (A pros/cons + B pros/cons)
12. **§6.8 + §6.9 new owner-scope items**:
    - §6.8: 4-way labeller readiness + 2-E.0 sub-phase + 29-hand calibration anchor
    - §6.9: 5-way scope (architect default Option B; owner ratifies A or B)
    - Total now 9 owner-scope items (architect's note: cosmetically check whether internal numbering survives = 9)

### Part C — Process discipline

13. **TC-23 EXISTENCE + CONTENT** (per `feedback_spec_vs_infrastructure_code_drift.md` + `feedback_tc23_existence_must_be_git_tracked.md`):
    - `git ls-files review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` returns the path
    - File content matches design dispatch + AMENDMENT 1 + AMENDMENT 2 + AMENDMENT 3 specifications
    - File size reasonable (~600 lines base + 126 amendment 3 = ~720 lines total expected)

14. **Design-only scope strictly preserved**:
    - ❌ NO river-rats-core/ edits ✓
    - ❌ NO data/ edits ✓
    - ❌ NO corpus/labelling work ✓
    - ❌ NO training scripts touched ✓
    - ❌ NO model files ✓
    - ❌ NO build/train ✓
    - ✅ ONLY design memo authored

15. **TC-X-DISPATCH-COMPLIANCE per PR #385 + #386 + #387 + #389**:
    - All 4 dispatches (base + 3 amendments) addressed in the combined memo
    - Architect-hat + ML-architect-hat + GTO-expert-hat roles all evident in content
    - 21-candidate counting consistent (architect's reported number) across base + amendments
    - 9 owner-scope item count consistent in §6 + status footer

16. **Self-flagged cosmetic concern (builder's commit msg)**:
    - "§3.4 + §3.5 (pilot gate strategy + reframing) appear AFTER §X §Y in document order due to amendment-fold sequencing"
    - QC categorize this: cosmetic-only (SHOULD_FIX-cosmetic) vs material-flow-confusion (SHOULD_FIX-substantive)?
    - Recommend: cosmetic-only since substantive coverage is complete; owner reads memo top-to-bottom but section labels disambiguate

### Part D — Architect's flagged "multiway-specialist-gap"

17. Architect noted in §1.6 (per orchestrator's record): "multiway-specialist-gap" — multiway specialist model history vs single-surface approach. QC verifies this is acknowledged as a known design constraint (NOT a bug; just a documented gap).

## What this PR does NOT change (per all 4 dispatches)

- ❌ Production code (river-rats-core/) UNTOUCHED
- ❌ Models, corpus, training data UNTOUCHED
- ❌ Phase 1.5 ship state UNTOUCHED (vNext-HU-59 still in production via `oracle_router.py:34`)
- ❌ Solver-verification queue UNTOUCHED (48 spots HOLD-with-accepted-risk per owner)

## What gates next (post-merge orchestrator action sequence)

1. Orchestrator merges PR #388 on QC PASS (autonomously per standing directive)
2. Orchestrator surfaces ALL 9 owner-scope items to owner for ratification via AskUserQuestion (one decision per question OR grouped; owner-friendly)
3. After owner ratifies feature lock + surface size + 4-way labeller readiness scope + 5-way scope + corpus origin + ship gates:
   - Phase 2-B feature implementation pilot dispatched (3-candidate pilot per architect's design)
4. Phase 2-B is build/train scope (out of 2-A's design-only scope)

## STOP / SHOULD_FIX / BLOCKER classification guidance

- **BLOCKER**: architect proposes Option A 5-way (when default per quality is Option B); or scope leaks from design-only (any river-rats-core/data/ edit); or material gap in any of the 3 amendments' substantive coverage; or 5-way file-missing finding turns out to be a production-routing bug NOT a design observation
- **SHOULD_FIX-substantive**: any candidate feature missing from §4 surface lock proposal; any sub-phase missing from §5 decomposition; any of the 9 owner-scope items not surfaced as owner-decidable in §6
- **SHOULD_FIX-cosmetic**: §3.4/§3.5 numbering ordering (architect self-flagged); any minor wording / typo issues

## QC routing + Output

Standalone stream per `feedback_qc_routing_when_standalone_active.md`. ~30-45 min wall-clock (larger PR scope; 720-line design memo + 3 amendments + 17 audit items). QC writes:
- `~/river-rats-qc/findings/2026-05-11-pr388-phase2-design-memo.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2_DESIGN_MEMO_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha` to current master `3763d8a`

## What gates

- PR #388 merge → on QC PASS, orchestrator merges autonomously per standing directive
- On QC SHOULD_FIX-cosmetic only → orchestrator merges + queues fixes as follow-up
- On QC SHOULD_FIX-substantive → orchestrator amends + re-fires builder
- On QC BLOCKER → orchestrator holds + redoes per `feedback_listen_to_orchestrator_always.md`
- After merge → orchestrator surfaces 9 owner-scope items for ratification
- Owner ratifies → Phase 2-B pilot dispatch fires

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `3763d8a` ✓
- Diff vs master: 1 file (this comm)
- Log vs master: 1 commit

## References

- Phase 2 design dispatch: master `16a5aab` (PR #385)
- AMENDMENT 1 (street distribution): master `cee0705` (PR #386)
- AMENDMENT 2 (re-raise × players-left): master `596bb89` (PR #387)
- AMENDMENT 3 (labeller readiness + 5-way scope): master `3763d8a` (PR #389)
- D5 blueprint analog: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Phase 1.5 design memo analog template: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- HU labelling incident (informs §X labeller readiness): `review/comms/BUILDER_OBSERVATION_FL4_RULE_BASED_INVALIDATION_2026-05-10.md`
- Production routing (informs §Y 5-way scope): `river-rats-core/oracle_router.py:34-38` `_MODEL_FILES`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_quality_default_no_ask.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`, `feedback_pilot_first_for_long_jobs.md`

**Status: QC stream — fire audit now on PR #388 Phase 2-A unified surface design memo (Path-A-amended to fold AMENDMENTS 1+2+3). ~30-45 min wall-clock. 17-item audit covering base memo (§1-§7) + AMENDMENT 1 (§3.X) + AMENDMENT 2 (§3.Y) + AMENDMENT 3 (§X + §Y + §6.8 + §6.9). Verify "5-way file MISSING on disk" finding (architect-flagged). Design-only scope preserved. After QC PASS + merge → orchestrator surfaces 9 owner-scope items for ratification → Phase 2-B pilot dispatch.**
