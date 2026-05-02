---
date: 2026-05-02
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: Phase 0 restart — shared state baseline (synthesis of PRs #105, #106, #107)
status: ORCHESTRATOR DECISIONS — owner sign-off needed on §6 items only
---

# Shared state baseline — Phase 0 restart synthesis

## Executive summary

Three terminals (orchestrator PR #107, lead-programmer PR #106, QC
PR #105) independently re-grounded after a 5-day gap and posted
state-of-project reports. **All three converge** on the headline
finding: the Phase 12 trainer directive (PR #104, master `14c2db1`)
is incompatible with `river-rats-core/train_model.py` master HEAD
along multiple axes and cannot be executed as written. **No
disagreements between the three reports** on substantive findings;
they differ only in granularity. Builder seat produced the deepest
source grounding (9 blockers + 7 drift items, line-cited); QC seat
caught two process-discipline items neither orchestrator nor builder
surfaced (calibration-vs-v3.2-checksum status, L4 labeller-cluster
defect classification). Orchestrator (me) framed the §6 process
drift on the directive itself.

This baseline is the single point of agreement going forward. After
this, `MAIN_TERMINAL_*_DIRECTIVE_*` resumes as the action-issuing
channel.

## §1. Three-way convergence — Where are we

| Item | Three-terminal consensus | Evidence |
|------|--------------------------|----------|
| Master HEAD | `14c2db1` (PR #104, 2026-04-27 19:51 UTC) | All 3 reports |
| Last code-bearing merge | PR #101 (`78bad39`) — Phase 11C 494-hand mass labels | All 3 |
| Production model | v9-3way-v2.2 (45-feat, 82.5% solver-corrected, 33/40 reference) | Orchestrator + Builder |
| Open PRs prior to alignment | None | All 3 |
| Activity gap | 5 days (2026-04-27 → 2026-05-02), 0 commits, 0 comms | All 3 |
| Dominant arc | Phase 8 → 10 → 11A → 11B/C → **Phase 12 directive (issued, not executed)** | All 3 |
| Corpus + labels | `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records) + `..._labels_…jsonl` (2470 labels, 5×494, 0% refusal, consensus_action keyed) | All 3 |
| Action distribution | CHECK 49.6% / BET 17.4% / FOLD 14.6% / CALL 12.6% / RAISE 5.9% (rarest) | Orchestrator + Builder |
| v9 baseline anchor | `river-rats-core/models/gto_model_v9_baseline_45feat.json` (45-feature) | All 3 |

## §2. Three-way convergence — Phase 12 directive status

**Status: EFFECTIVELY BLOCKED. Build cannot proceed as written.**

| # | Drift item | Source seat | Severity | Notes |
|---|-----------|-------------|----------|-------|
| B1 | 6 CLI flags don't exist (`--corpus --labels --warm-start --output --seeds --confidence-weighting`); only `--45feat` argv check at `train_model.py:505` | All 3 | BLOCKER | No argparse anywhere |
| B2 | JSONL vs CSV format mismatch; trainer hardcodes `csv_file = 'training-data/train_3way_v3_combined.csv'` at `train_model.py:498` | All 3 | BLOCKER | Wrong loader entirely |
| B3 | No warm-start hook; `xgb_model=` parameter never passed in `model.fit()` at `train_model.py:259` | All 3 | BLOCKER | Methodology not implemented |
| B4 | Single hardcoded `random_state=42` (`train_model.py:226, 246, 309`); no seed loop | Builder + QC | BLOCKER | Multi-seed not implemented |
| B5 | Per-class inverse-frequency weighting (`train_model.py:252-257`); directive expects per-sample `consensus_confidence` | Builder | BLOCKER | Different scheme entirely |
| B6 / D1 | **Directive arithmetic wrong:** "45 + 14 = 59" — actual `gto_model.py:64` `N_FEATURES = 55`; 4 v2.4 P1 blockers in `feature_keys.py:89-92`. Real: **55 + 4 = 59** | Builder | DRIFT HIGH-2 | `scripts/verify_feature_schema_compatibility.py:39-41` already encodes correct math |
| B7 / D3 | **Cited reference set `training-data/3way_reference_40hand.jsonl` does not exist** on master | Builder + QC | BLOCKER HIGH-1 | Litmus-test gate is undefined; candidate files: `3way_combined_350.jsonl`, `3way_labelled.jsonl`, `3way_selected_200.jsonl`, `facing_bet_test_set_40.jsonl` |
| B8 / D2 | **Join key `ref_id` undefined on corpus.** Corpus has `pilot_hand_id` + `source_situation_id`. Labels carry both `ref_id` (= corpus's `source_situation_id`) and `pilot_hand_id`. Verified on row 1: both join keys resolve | Builder | DRIFT HIGH-2 | Either join works in practice; literal directive instruction wrong |
| B9 / D7 | **4 v2.4 P1 blocker features not integrated into FEATURE_COLUMNS** in `gto_model.py:33-62` or `train_model.py:131-160`. Defined in `feature_keys.py:87-92` but never propagated. Corpus produces 59-feature `feat_dict`, training side stops at 55 | Builder | BLOCKER HIGH-1 | Deepest cause of arithmetic confusion |
| P1 | §6 Step 1 (ml-architect design) skipped on Phase 12 directive — went straight to programmer-named-author | All 3 | Process HIGH-2 | Explains why the drift wasn't caught pre-merge |
| P2 | Round 12 review chain on PR #104 (directive itself) didn't catch any drift; QC was not in the directive-PR pre-merge chain | Orchestrator + QC | Process HIGH-2 | TC-23-CLI sub-vector candidate (QC concern #1) |
| P3 | 45→59 warm-start across feature-count boundary mechanism is design-class unproven (stock XGBoost `xgb_model=` requires identical schema) | QC | DESIGN | ml-architect must commit to: pre-pad / curriculum / distillation / from-scratch with priors |
| Q3 | Calibration-vs-v3.2-checksum status for Phase 11B mass labelling not documented in `PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md`; v3.2 added KB-checksum-changing rules (DO NOT #11, §1.7 OVERRIDE, river-checked) but no calibration event recorded between v3.1.2 and v3.2 dispatch | QC | Process MEDIUM | PR #103 already accepted labels; closure is forward-looking |
| Q4 | Labeller-instance L4 §1.7 RAISE template-substitution defect (post-mass-labelling); consensus filter mitigates trainer signal | QC | LOW (deferred) | Incident #22 candidate per QC concern #4 |
| Q5 | `river-rats-core/models/` clutter (~20 historic v9 artefacts) | QC | LOW (housekeeping) | Post-Phase-12 ship cleanup |
| Q6 | Activity gap 5 days, no commits, no comms | All 3 | NOTE | Restart probe pattern caught it cleanly; not a process failure of the system |

## §3. Orchestrator decisions

These are **decisions within orchestration scope** (sequencing, team
allocation, directive issuance, process patterns). They do not need
owner sign-off; they are how I orchestrate the work given the
state above. Owner sign-off items are in §6.

### D-1 — Phase 12 builder dispatch is HELD indefinitely

Phase 12 directive is superseded by Phase 12.5. No builder action on
`programmer/v9-3way-59feat-trainer-2026-04-27` branch will be
authorized until Phase 12.5 ships a working trainer. Builder D6
self-flag on `feedback_named_author_builds_not_polls.md` is logged
but not actionable — the directive itself anticipated this BLOCKED
state in §"Failure handling".

### D-2 — Phase 12.5 sequence: full §6 mandatory training team

Per `docs/PROCESS_GUIDE.md` §6, the sequence is non-negotiable:

1. **12.5A — ml-architect (design):** read corpus + labels + master
   HEAD `train_model.py` / `gto_model.py` / `feature_keys.py` /
   `feature_extractor.py`; design new training module. Owner approval
   gate. Recommendations the ml-architect must commit to (no menus,
   per §1.4 — pick one with reasoning):
   - Trainer module location: extend `train_model.py` (sacred-core
     edit) vs new `river-rats-core/train_model_v9_student.py` (new
     module per `CLAUDE.md` §6 training-provenance addendum)
   - 45→59 warm-start mechanism (P3): pre-pad baseline / curriculum
     45→59 / knowledge distillation / from-scratch with priors
   - Per-sample `consensus_confidence` weighting math (B5): pure
     `sample_weight = consensus_confidence`, or hybrid with class
     weights, or normalised by class
   - 4-blocker FEATURE_COLUMNS integration (B9): extend `gto_model.py`
     + `train_model.py` FEATURE_COLUMNS to 59 (single source of truth,
     touches core), or new trainer owns 59-feature schema
     independently (schema-divergence risk)
   - Canonical reference-set selection (B7): audit
     `training-data/*reference*` and `*40hand*` candidates; recommend
     one as the canonical 40-hand litmus set, or recommend authoring
     a new one
   - Stratified split: confirm seed-loop strategy that preserves
     stratification per seed
2. **12.5B — owner approves ml-architect design** (gate)
3. **12.5C — architect (blueprint):** read ml-architect design +
   master HEAD source; produce exact insertion-point blueprint with
   line numbers
4. **12.5D — lead-programmer (implement + run):** implement from
   blueprint only; run training; report to comms
5. **12.5E — reviewer (Gates 2.3 + 2.4):** feature importance check;
   reference-set evaluation with v8 + v9-3way-v2.2 baselines in same
   session; solver-corrected scoring per
   `memory/reference_corrections.md`
6. **12.5F — owner approves model** (ship gate)

Round 12 review chain (ml-architect + gto-expert + QC) runs
post-build at 12.5E as the directive originally specified.

### D-3 — Directive amendments commit

When the Phase 12.5 kickoff lands, it carries the following
**orchestrator commitments** (so ml-architect designs against
correct premises):

- **Arithmetic:** "**55 base + 4 v2.4 P1 blockers = 59**" replaces
  the original "45 + 14 = 59" framing. Aligns to
  `scripts/verify_feature_schema_compatibility.py:39-41`.
- **Join key:** `corpus.source_situation_id == labels.ref_id`
  (verified on row 1: both `d6066_BB_flop`). `pilot_hand_id` is
  fallback validation, not primary. Coded explicitly in trainer.

The two larger questions (canonical reference set, FEATURE_COLUMNS
integration path) are **deferred to ml-architect 12.5A** because
they are HOW-class decisions per PROCESS_GUIDE §1.4. Orchestrator
does not pre-empt expert decisions.

### D-4 — TC-23-CLI sub-vector formalised

QC concern #1 stands. Going forward, milestone-class directives that
prescribe a specific CLI invocation receive a QC pre-merge audit on
the directive PR (not just the builder PR that follows). The audit
verifies each cited flag exists in the script's argparse surface at
master HEAD before merging. Adds to `curative_additions_log` on the
QC side. Memory carry: this is the structural fix to P2 — round 12
review chain on directive PR #104 didn't include QC, which is why
the 6-flag drift shipped.

### D-5 — Calibration discipline (Q3)

Phase 11B 2470 labels are accepted as-shipped (PR #103 synthesis
closure stands; ml-architect + gto-expert APPROVE-WITH-NITS holds).
Going forward, the **TC-23-CALIBRATION sub-vector** becomes mandatory
pre-flight on any labelling round: verify `calibration_exam.py` was
re-run against the current KB checksum, with graded score and answer
key isolation, before mass dispatch. Closes Q3 forward; does not
re-litigate the shipped labels.

### D-6 — L4 cluster defect (Q4)

Logged as **incident #22** in `incident_pattern_library.md`:
*Labeller-instance defect detected post-mass-labelling; consensus
filter mitigates trainer signal but individual-label data is
permanently noisy at the labeller_id level.* Curative
**V-Labeller-Distribution-Outlier** sub-vector queued for
activation when individual-label cycles become live (per QC
concern #4 framing). Not blocking Phase 12.5 (which trains on
consensus_action only).

### D-7 — Five-day gap

No process change. The restart probe pattern
(`reference_river_rats_v2_restart_protocol.md`) caught the gap
cleanly across all three terminals. Builder's D6 self-flag is
acknowledged but the system-level mechanism worked: Phase 0
alignment was the correct response.

### D-8 — `models/` clutter (Q5)

Deferred. Post-Phase-12.5 ship cleanup. Not blocking.

## §4. What stays / what changes operationally

| Operational pattern | Status |
|--------------------|--------|
| Plan-before-build (CLAUDE.md §1) | Reinforced (D-2) |
| Section 6 mandatory training team | Reinforced (D-2) |
| `feedback_listen_to_orchestrator_always.md` (orchestrator-named-author = sufficient) | Unchanged |
| `feedback_qc_required_before_approval.md` (QC pre-merge on milestone PRs) | **Extended:** milestone-class directives that prescribe CLI invocations also get QC pre-merge (D-4) |
| `feedback_verify_source_not_plan.md` (verify against actual source, not directive prose) | Unchanged; reinforced by every drift in §2 |
| `feedback_spec_vs_infrastructure_code_drift.md` (CONTENT vs EXISTENCE drift dimensions) | **Extended:** directive PRs are now in scope for this audit class, not just code PRs |
| `feedback_shared_tree_commit_hygiene.md` | Reinforced (cross-branch contamination during this Phase 0 alignment run was the proof) |
| §2.1 calibration before labelling | Reinforced via TC-23-CALIBRATION (D-5) |

## §5. Cross-stream Q5 closure

| Ask | Source | Resolution |
|-----|--------|-----------|
| A1: canonical reference set path | Builder | Deferred to ml-architect 12.5A audit + recommendation (D-3) |
| A2: 4-blocker integration policy | Builder | Deferred to ml-architect 12.5A (D-3) |
| A3: directive arithmetic amendment | Builder | Committed: 55 + 4 = 59 (D-3) |
| A4: join-key commitment | Builder | Committed: `corpus.source_situation_id == labels.ref_id` (D-3) |
| A5: §6 team re-issue | Builder | Committed: full §6 sequence (D-2) |
| QC #1: pre-empt Phase 12.5 | QC | Committed: Phase 12.5 kickoff is the next directive (§6 below) |
| QC #2: calibration-vs-v3.2-checksum status | QC | Forward-only resolution via TC-23-CALIBRATION (D-5) |
| QC #3: L4 cluster defect triage | QC | Incident #22 + V-Labeller-Distribution-Outlier (D-6) |
| Q2 to QC (V-Implementation-Spec-Match on amended directive) | Builder | Committed: QC pre-merge on Phase 12.5 directive itself (D-4) |
| Q3 to QC (Phase 12 trainer pre-flight when authored) | Builder | Committed: round-12 review chain runs at 12.5E |
| Owner: 5-day gap rationale | Orchestrator | §6 below |
| Owner: orchestrator role-assignment confirmation | Orchestrator | §6 below |

## §6. Items requiring owner sign-off

These are **owner-scope decisions** (WHAT/WHETHER, not HOW). I will
not proceed without explicit approval on each.

### S-1 — 5-day gap rationale (informational, not blocking)

The 5-day gap (2026-04-27 → 2026-05-02) is unexplained from comms
history. Owner clarification helps the orchestration record but
doesn't block forward work. Possibilities: planned pause / awaiting
external input / stall I should understand. State your call when
convenient; alignment proceeds either way.

### S-2 — Orchestrator role-assignment confirmation (NOT blocking forward work, but blocking dispatch comms)

The CWD `/home/rupertbeytell/river-rats-review/` `CLAUDE.md` defines
this terminal as reviewer-only. Owner overrode to orchestrator in
this session. Other terminals (builder, QC) interact with whoever
issues `MAIN_TERMINAL_*_DIRECTIVE_*` comms. Suggest owner posts a
one-line confirmation (e.g., "orchestrator role on this terminal
2026-05-02") I can quote in subsequent dispatch comms. Without it,
downstream terminals may rightly question authority.

### S-3 — Phase 12.5 kickoff (BLOCKING: this is the next directive)

I will issue `MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md` as a
proposal-class kickoff (matching #94 mass-labelling kickoff pattern).
Scope as defined in D-2 + D-3 above. Named author: ml-architect.
12.5A is design-only (no code). Owner sign-off on the kickoff is
required before 12.5A dispatches.

**Owner decision points in the kickoff:**
- Approve §6 sequence (D-2) — single decision
- Approve directive amendments (D-3 committed items) — single decision
- Approve TC-23-CLI sub-vector formalization (D-4) — single decision
- Approve forward-only calibration discipline closure (D-5) — single decision
- Approve incident #22 + V-Labeller-Distribution-Outlier (D-6) — single decision

## §7. References

- This baseline synthesises:
  - Orchestrator: PR #107 master `e77800e` `STATE_OF_PROJECT_ORCHESTRATOR_2026-05-02.md`
  - Builder: PR #106 master `4f3da16` `STATE_OF_PROJECT_BUILDER_2026-05-02.md`
  - QC: PR #105 master `387ce24` `STATE_OF_PROJECT_QC_2026-05-02.md`
- Master HEAD: `14c2db1`
- Phase 12 directive: `review/comms/MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
- Critical source files for Phase 12.5 design phase:
  - `river-rats-core/train_model.py` (511 lines, master HEAD)
  - `river-rats-core/gto_model.py` (FEATURE_COLUMNS at lines 33-62, N_FEATURES at line 64)
  - `river-rats-core/feature_keys.py:87-92` (4 v2.4 P1 blockers)
  - `river-rats-core/feature_extractor.py`
  - `scripts/verify_feature_schema_compatibility.py:33-42` (correct 55+4=59 math)
- Process: `docs/PROCESS_GUIDE.md` §0–8; `CLAUDE.md` §1–9 + §"Task Decomposition Mandatory"
- Memory: `feedback_quality_default_no_ask.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_verify_source_not_plan.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_shared_tree_commit_hygiene.md`, `reference_river_rats_v2_restart_protocol.md`

**Status: SHARED STATE BASELINE POSTED. Owner sign-off needed on §6 (S-2 + S-3 are blocking; S-1 informational). Upon S-2 + S-3 approval, orchestrator issues `MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md` (§6 ml-architect 12.5A design directive). No builder dispatch, no QC audit dispatch, no `river-rats-core/` touches in the interim.**
