# Restart Links — All GitHub URLs

**Last updated:** 2026-04-15 — added latest recoveries (Tracks 1, 3) and orchestrator handoff

## Repos

- **river-rats-v2:** https://github.com/beytell1-sketch/river-rats-v2
- **river-rats-teaching:** no GitHub remote yet (local only)

## READ FIRST — latest state

- [ORCHESTRATOR_UPDATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/ORCHESTRATOR_UPDATE_2026-04-15.md) — handoff to new main terminal
- [MAIN_TERMINAL_UPDATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/MAIN_TERMINAL_UPDATE_2026-04-15.md) — latest instructions for builder
- [SESSION_STATE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SESSION_STATE_2026-04-15.md) — base project state snapshot

## Restart prompts (copy into fresh sessions)

- [RESTART_MAIN.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_MAIN.md) — main terminal restart prompt (GitHub-first)
- [RESTART_BUILDER.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_BUILDER.md) — builder terminal restart prompt (GitHub-first)
- [RESTART_TEACHING.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/RESTART_TEACHING.md) — teaching terminal (blocked — no remote yet)
- [README.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/restart/README.md) — restart folder index

## Project plans

- [PLAN_V2.2_FINAL_COMBINED_2026-04-13.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PLAN_V2.2_FINAL_COMBINED_2026-04-13.md) — overall v2.2 plan
- [PLAN_PHASE3_FINAL_2026-04-13.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PLAN_PHASE3_FINAL_2026-04-13.md) — Phase 3 plan

## Phase reports

- [PHASE_3_5H_FINAL_ASSEMBLY_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PHASE_3_5H_FINAL_ASSEMBLY_2026-04-15.md) — Gate 6 submission
- [PHASE_4_TRAINING_REPORT_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PHASE_4_TRAINING_REPORT_2026-04-15.md) — Gate 7 submission (pending)

## Investigations

- [HRP_INVESTIGATION_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/HRP_INVESTIGATION_2026-04-15.md) — test harness bug finding
- [TRAINING_DATA_AUDIT_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/TRAINING_DATA_AUDIT_2026-04-15.md) — Track 3 result, revealed ANOMALY-A

## Active directives

- [DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/DIRECTIVE_POST_HRP_PARALLEL_TRACKS_2026-04-15.md) — 6 parallel tracks
- [DIRECTIVE_PARALLEL_WORK_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/DIRECTIVE_PARALLEL_WORK_TRACKS_2026-04-15.md) — original 5 tracks

## Owner reviews

- [REVIEW_PARALLEL_TRACKS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/REVIEW_PARALLEL_TRACKS_2026-04-15.md) — pending amendments for Tracks A and E

## Approved blueprints

- [BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md) — Track B blueprint (IMPLEMENTED commit 64e3d08)

## v2.3 scope documents (needs amendments)

- [PLAN_V23_SCOPE_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PLAN_V23_SCOPE_2026-04-15.md)
- [PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md)

## Teaching handoff

- [TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md) — handoff note
- [training-data/v2_2_enriched_for_teaching.jsonl](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/v2_2_enriched_for_teaching.jsonl) — enriched labels for teaching

## Solver work (pending owner)

- [SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html) — 10 MW miss hands for Gate 7 decision
- [SOLVER_VERIFICATION_DSERIES_2026-04-14.html](https://github.com/beytell1-sketch/river-rats-v2/blob/master/review/comms/SOLVER_VERIFICATION_DSERIES_2026-04-14.html) — d-series hands (verified Apr 14)

## Code files — Track 1 (harness hardening) deliverables

- [river-rats-core/gto_model.py](https://github.com/beytell1-sketch/river-rats-v2/blob/master/river-rats-core/gto_model.py) — features_from_dict now raises KeyError on missing features
- [river-rats-core/reference_evaluator.py](https://github.com/beytell1-sketch/river-rats-v2/blob/master/river-rats-core/reference_evaluator.py) — _validate_feat_dict guard
- [river-rats-core/tests/test_harness_feature_completeness.py](https://github.com/beytell1-sketch/river-rats-v2/blob/master/river-rats-core/tests/test_harness_feature_completeness.py) — 12 regression tests

## Folders

- [review/comms/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/comms) — every comms doc
- [review/restart/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/review/restart) — restart pack
- [river-rats-core/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/river-rats-core) — production code
- [river-rats-core/tests/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/river-rats-core/tests) — tests
- [prompts/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/prompts) — labelling prompts
- [training-data/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/training-data) — datasets
- [knowledge/](https://github.com/beytell1-sketch/river-rats-v2/tree/master/knowledge) — KB

## Key individual files

- [prompts/gto_labeller_v2.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/prompts/gto_labeller_v2.md) — THE labelling prompt
- [training-data/v2_2_training.csv](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/v2_2_training.csv) — production training CSV (385 × 111)
- [training-data/tag_vocabulary.json](https://github.com/beytell1-sketch/river-rats-v2/blob/master/training-data/tag_vocabulary.json) — intention and street plan vocabulary
- [knowledge/three_way_gto.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/knowledge/three_way_gto.md) — KB v1.3
- [CLAUDE.md](https://github.com/beytell1-sketch/river-rats-v2/blob/master/CLAUDE.md) — project conventions

## Communication protocol (main terminal ↔ builder)

Main terminal and builder are on separate machines and can only
communicate via commits in this repo:

### Main terminal → Builder
- `review/comms/MAIN_TERMINAL_UPDATE_<date>.md` — instructions, reviews, priorities

### Builder → Main terminal
- `review/comms/BUILDER_STATUS_<date>.md` — status updates or questions
- `review/comms/BUILDER_BLOCKED_<date>.md` — if blocked on auth or infrastructure
- `review/comms/<TRACK_NAME>_<date>.md` — track deliverables (e.g. `ANOMALY_A_VERIFICATION_2026-04-15.md`)

### Both check for updates
```
ls -lt review/comms/ | head -15
```

## Current state quick reference

- **Gate 7 PENDING** — awaiting owner solver verification on 10 MW misses
- **Tracks 1, 3, 5 DONE** — harness hardening, training data audit, BP generator fix
- **Track 3.5 NEW BLOCKING** — ANOMALY-A verification (street encoding may have corrupted v2.2 training)
- **Track 4 ON HOLD** — bias diagnosis depends on Track 3.5
- **Track 2 CAN RUN** — FB-40 re-eval with hardened harness
- **Track 6 WAITING** — depends on Track 4
- **Track A amendments PENDING** — BET delta fix, bias signature update, calibration gate
- **Track E amendments PENDING** — absolute accuracy floor, Group D fallback
- **v2.2 SHIP DECISION PENDING** — owner, after solver
- **v2.3 GENERATION BLOCKED** — on Track 3.5 + Track A corrections
