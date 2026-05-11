---
date: 2026-05-11
from: Main terminal (orchestrator; standing-directive autonomous on owner-ratification)
to: LEAD-PROGRAMMER (architect-hat + ml-architect-hat + gto-expert-hat)
re: Phase 2-B — 6-candidate feature implementation PILOT (3 D5 + 2 4-way + 1 re-raise) per architect's §3.4 + §3.Y.4 design; pilot+full split per `feedback_pilot_first_for_long_jobs.md`; owner has RATIFIED all 9 owner-scope items per architect defaults
status: DISPATCH — fire now (Phase 2-A merged at master a221a9b; PR #388 0e5f91f; QC PASS PR #391 0/0/0; owner ratification recorded below)
---

# Phase 2-B PILOT dispatch — 6-candidate feature implementation

## Owner ratification record (2026-05-11 ~03:55 SAST)

Owner answered AskUserQuestion "How do you want to handle the 9 owner-scope items for Phase 2 ratification?" with:

**"Ratify all 9 per architect defaults"**

This locks the following 9 §6 architect proposals as approved:

| # | Item | Architect default (RATIFIED) |
|---|------|-------------------------------|
| 6.1 | Feature lock | APPROVE 21 candidates (D5 11 + 4-way 6 + re-raise 4) → ~15-17 net post-implementation |
| 6.2 | Surface size target | ~74-80 features (from 59 baseline) |
| 6.3 | 4-way corpus origin | Fresh expert-labelled ~750 lookalikes (analog HU; per `feedback_solver_vs_expert_labels.md`) |
| 6.4 | Solver-verification queue posture | Continue HOLD-with-accepted-risk (per `feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`) |
| 6.5 | 3-way ship gate (2-F) | ≥36/40 (D5 hypothesis target) |
| 6.6 | 4-way ship gate (2-G) | Option A weighted-total ≥28/35 street-weighted 51/31/11/6 (flop/preflop/turn/river); per-hand stay-wrong taxonomy per §3.Y.6 |
| 6.7 | Pre-Phase-2 incidentals | Fold into Phase 2; HU-6.5 corpus-gap deferred to post-Phase-2 |
| 6.8 | 4-way labeller readiness + 2-E.0 | Insert NEW sub-phase 2-E.0; 5-hand pilot gate + 29-hand calibration set |
| 6.9 | 5-way scope | Option B = defer to Phase 3 (5-way <5% prod usage; 5-way file missing → HU fallback acceptable for now) |

Builder-architect SHALL not deviate from these defaults during Phase 2-B; deviation requires REPORT + new dispatch.

## What Phase 2-B builds (PILOT scope)

Per design memo §5 row 2-B + §3.4 + §3.Y.4: **6-candidate feature implementation PILOT** in `feature_extractor.py` against existing 59-feat baseline (test surface size 65).

### Candidate set (6 total)

**D5 candidates (3 from §2.2 11; architect picks the 3 most-promising):**
- Architect-hat picks per D5 blueprint §4 (e.g., the 3 with strongest pre-evidence for MW-40/45/47 stay-wrong axes); document the picks + rationale in the implementation PR's commit message / report
- Each D5 candidate targets stay-wrong axis defined in `project_v9_3way_ceiling.md`

**4-way candidates (2 per §3.4):**
- `players_to_act_after_hero` (mandatory; owner-surfaced; direct evidence-of-need per AMENDMENT 1)
- `multiway_equity_realization_factor` (architect's "cleanest GTO theory; orthogonal to existing features" pick)

**Re-raise × players-left candidates (1 per §3.Y.4):**
- Architect-hat picks 1 from §3.Y.3 4-net set: `street_raise_count`, `closing_action`, `squeeze_risk_index`, OR `reverse_implied_odds_signal`
- Architect's preferred pick: `closing_action` (binary; cleanest signal; testable in isolation; per §3.Y.4 "include AT LEAST ONE re-raise-interaction feature ... e.g., `closing_action` or `squeeze_risk_index`")

### Implementation deliverables

Per design memo §5.2 estimate ~10-15h:

1. **Feature implementation** in `river-rats-core/feature_extractor.py`:
   - Each of 6 features added to FEATURE_COLUMNS + corresponding extraction logic
   - Surface size = 65 (59 baseline + 6 pilot candidates); update accordingly
   - Each feature must produce non-NaN/Inf values for every spot in existing 988-corpus (3-way) AND a synthetic 4-way smoke set
2. **Per-feature unit tests** in `river-rats-core/tests/`:
   - Each of 6 features has a unit test asserting (a) feature key in FEATURE_COLUMNS, (b) extraction returns numeric scalar, (c) non-NaN/Inf on test fixtures, (d) reasonable value range
3. **Pilot trainer run** (1-seed smoke):
   - Train 3-way model on existing 988-corpus with surface size 65
   - Per-feature importance scores recorded (XGBoost feature_importances_)
   - Reference set evaluation: 4-way 35-hand street-weighted reference set (per §6.6 ratified) — if not yet built per 2-D, use existing 3-way reference for D5 importance gate + skip 4-way close-hand graduation gate for pilot (REPORT)
4. **Pilot gate evidence in report** per design memo §5 row 2-B:
   - **D5 gate**: importance ≥2% AND ≥1 stay-wrong graduation on reference set
   - **4-way gate**: importance ≥2% AND ≥1 4-way close-hand graduation (if 4-way reference available; else REPORT)
   - **Re-raise gate**: importance ≥1% AND closing-action vs early-action differential captured

### Pilot gate outcome dispatching

Per §3.4 pilot gate table + standing `feedback_pilot_first_for_long_jobs.md`:

| Outcome | Action |
|---------|--------|
| All 6 candidates clear their respective gates | PROCEED to 2-C (full 12-15 remaining feature implementation) |
| ≥3 of 6 clear (mixed signal) | REPORT to orchestrator; orchestrator triages partial-go vs HOLD |
| <3 of 6 clear (broad fail) | HALT 2-C; escalate to "is the issue elsewhere" investigation (corpus quality? feature design? game-state representation?) |

## What Phase 2-B does NOT do

Per design memo §5 + §7 + `feedback_pilot_first_for_long_jobs.md`:

- ❌ Does NOT implement remaining 12-15 candidates (that's 2-C scope; pilot must clear first)
- ❌ Does NOT touch `oracle_router.py` (model swap is 2-H scope)
- ❌ Does NOT build the 4-way reference set (that's 2-D scope)
- ❌ Does NOT generate or label corpus (that's 2-E scope; 2-E.0 labeller readiness gate first)
- ❌ Does NOT retrain production models (2-F retrains 3-way; 2-G retrains 4-way; both AFTER 2-C)
- ❌ Does NOT touch inference path 59 module (inference_path_75 lives in 2-C per §4.3)
- ❌ Does NOT drain solver-verification queue (HOLD-with-accepted-risk per 6.4 ratified)
- ❌ Does NOT design labeller brief (that's 2-E.0 scope)
- ❌ Does NOT work on 5-way (Option B defer per 6.9 ratified)

## STOP conditions (per CLAUDE.md §5)

- D5 blueprint candidates can't be implemented per §2.2 spec (e.g., requires game-state representation change) → STOP / REPORT
- 4-way feature requires a feature_extractor.py architectural change (e.g., extending the pipeline contract) → STOP / REPORT
- Pilot trainer run fails (non-NaN/Inf assertion fails on existing corpus) → STOP / REPORT
- Reference set evaluation cannot run because v9-4way-45feat is missing (per §1.6 greenfield finding) → REPORT; fall back to 3-way reference; flag 4-way gate as deferred-to-2-D
- TC-23 EXISTENCE on new feature_extractor changes: every new feature in FEATURE_COLUMNS must be git-tracked (`git ls-files`)
- TC-X-OWNER-SCOPE-DISCIPLINE: NO deviation from the 9 ratified items above; deviation requires REPORT + new dispatch
- Wall-clock blows past ~20h (memo estimate 10-15h + 33% buffer) → REPORT

## QC stream — what you audit (pre-merge milestone for Phase 2-B pilot PR)

Per `feedback_qc_required_before_approval.md` + standing milestone-PR pattern:

1. **Diff scope** (TC-23):
   - `river-rats-core/feature_extractor.py` (+~250-400 lines; 6 new features + FEATURE_COLUMNS update)
   - `river-rats-core/feature_keys.py` (+6 F-class constants)
   - `river-rats-core/tests/test_feature_extractor.py` OR new test files (+6 unit tests)
   - Pilot report file in `review/comms/BUILDER_REPORT_PHASE2B_PILOT_2026-05-11.md`
   - NO oracle_router edits; NO data/ edits; NO trainer changes; NO inference_path edits; NO model files

2. **Per-feature unit test verification**: independently run 6 unit tests; verify PASS

3. **Surface size attestation**: `len(FEATURE_COLUMNS) == 65` (59 baseline + 6 pilot)

4. **Non-NaN/Inf on full 988-corpus**: independently spot-check 5-10 spots; verify all 6 features extract to numeric scalars

5. **Pilot trainer report verification**:
   - Per-feature importance scores numeric + non-NaN
   - D5 gate evidence: which 3 D5 candidates? importance values? stay-wrong graduation evidence?
   - 4-way gate evidence: 2 candidate importance values + 4-way close-hand graduation (or deferred-to-2-D flag with reason)
   - Re-raise gate evidence: 1 candidate importance + closing-action differential captured

6. **No spec drift**: 6 candidates implemented match dispatch spec (not 5, not 7; not different candidates)

7. **TC-X-DISPATCH-COMPLIANCE**: all 9 ratified owner-scope items honored; design-memo §5 row 2-B scope respected; no scope leak

8. **Process discipline**: pilot-first standing rule explicitly applied; full 2-C not started

QC routing: standalone per `feedback_qc_routing_when_standalone_active.md`. Output:
- `~/river-rats-qc/findings/2026-05-11-pr<N>-phase2b-pilot.md`
- Cross-post: `review/comms/REVIEW_QC_PHASE2B_PILOT_2026-05-11.md`
- Heartbeat: update `~/river-rats-qc/.last_seen_master_sha`

## What gates

- Builder Phase 2-B pilot PR → QC trigger when pushed
- On QC PASS + pilot gate cleared (per §3.4 + §3.Y.4 + above table) → orchestrator merges + dispatches 2-C
- On pilot gate FAIL or partial → orchestrator triages per pilot-gate-outcome table; may HALT or proceed
- On any STOP condition → REPORT; orchestrator triages architect-HOW vs novel owner-WHAT

## Pre-push checks (per `feedback_orchestrator_branch_base_verification.md`)

- HEAD vs `origin/master` at `git checkout -b`: MATCH `a221a9b` ✓
- Diff vs master: 1 file (this dispatch)
- Log vs master: 1 commit

## References

- Phase 2-A design memo (this dispatches from): master `0e5f91f` (PR #388)
- Phase 2-A QC verdict PASS: master `a221a9b` (PR #391)
- Phase 2 design dispatch (PR #385): master `16a5aab`
- Phase 2 design AMENDMENTS 1+2+3: masters `cee0705` / `596bb89` / `3763d8a`
- D5 blueprint: `review/comms/PHASE125_D5_DEFERRED_BLUEPRINT_2026-05-07.md`
- Design memo: `review/comms/PHASE2_UNIFIED_SURFACE_DESIGN_2026-05-11.md` (724 lines)
- Stay-wrong taxonomy: `~/.claude/projects/-home-rupertbeytell/memory/project_v9_3way_ceiling.md`
- Pilot-first standing rule: `~/.claude/projects/-home-rupertbeytell/memory/feedback_pilot_first_for_long_jobs.md`
- Quality default standing rule: `~/.claude/projects/-home-rupertbeytell/memory/feedback_quality_default_no_ask.md`
- Solver-queue posture: `~/.claude/projects/-home-rupertbeytell/memory/feedback_owner_too_difficult_orchestrator_picks_solver_flag.md`
- Memory: `feedback_qc_required_before_approval.md`, `feedback_qc_routing_when_standalone_active.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_orchestrator_branch_base_verification.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_attention_flags_when_features_change.md`, `feedback_bucket_first_labelling.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_solver_aligned_sizing.md`

**Status: Phase 2-B PILOT dispatch — 6-candidate feature implementation (3 D5 + 2 4-way + 1 re-raise) per architect's §3.4 + §3.Y.4 design. Owner has RATIFIED all 9 owner-scope items per architect defaults. Pilot+full split standing rule applied. Builder fires implementation + 1-seed smoke trainer + per-feature importance + pilot gate evidence. NO 2-C work until pilot gate clears.**
