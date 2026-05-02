---
date: 2026-05-02
from: Main terminal (orchestrator)
to: Owner · LEAD-PROGRAMMER · QC stream
re: Phase 0 restart — orchestrator state-of-project (1 of 3)
status: ALIGNMENT — no work, no directives downstream of this doc
---

# Orchestrator state-of-project — 2026-05-02

## Why this doc exists

5-day gap since 2026-04-27. Owner has called for a slow-and-steady
restart with all three terminals (orchestrator [me], lead-programmer,
QC) independently grounding in master HEAD + comms history and
posting their state-of-project view. Orchestrator authors first
(this doc) so as not to steer the other two answers. After all
three reports land, orchestrator synthesises into
`SHARED_STATE_BASELINE_2026-05-02.md`. No forward work
(no Phase 12 build, no Phase 12.5 kickoff, no audit dispatch)
until owner approves the shared baseline.

This is alignment-only. No directives are issued downstream of
this doc.

## Q1. Where are we?

**Last shipped production model:** v9-3way-v2.2 (45-feature, 3-class,
from-scratch). Reference set 32/40 raw, **33/40 (82.5%)
solver-corrected**. v8 multiway baseline was 23/40 (57.5%);
v9-3way-v2.2 is +10 hands. Production artefact:
`river-rats-core/models/gto_model_v9_3way_v2.2.json`.

**Master HEAD:** `14c2db1` — Orchestrator: Phase 12 directive —
v9 student warm-start trainer (59-feat XGBoost) (#104), merged
2026-04-27.

**Last 5 merged PRs:**

| PR | Commit | Title |
|----|--------|-------|
| #104 | 14c2db1 | Orchestrator: Phase 12 directive — v9 student warm-start trainer |
| #101 | 78bad39 | Builder Phase 11B: 2470 mass labels (5 sonnet labellers × 494 hands, v3.2) |
| #103 | 3c01114 | Orchestrator: PR #101 labels round 11 synthesis — 3-way APPROVE |
| #102 | 72c5c8b | QC pre-merge audit on PR #101 — APPROVE clean |
| #98 | 26fa7db | Builder Phase 11A: mass-labelling scripts |

**Open PRs:** none.

**Activity gap:** 2026-04-27 (last comms file `21:51` Apr 27) →
2026-05-02 (today). 5 days of no activity in comms. Reason
unknown to me; flagged as Q5 ask of owner.

**Dominant workstream since 2026-04-26:** "Phase 11" mass-labelling
arc — corpus revision (PR #70, 494 hands) → labelling scripts
(PR #98, Phase 11A) → 2470 mass labels (PR #101, Phase 11B) →
Phase 12 trainer directive (PR #104). Adjacent streams (preflop
range fix, teaching/Phase C, Tier 1 calibration manifest 33→45,
held-out testset v1.0 expansion) are listed in Phase 12 directive
as "NOT covered" and are dormant.

**Corpus + labels in master, ready for trainer consumption:**
- `data/corpus_revision_500_hand_2026-04-27.jsonl` — 494 records,
  59-feature schema (45 base + 14 v2.4 P1 blocker features)
- `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` — 2470
  individual labels, consensus_action keyed by ref_id
- Consensus mix: 62.6% unanimous, 22.1% 4/5, 14.4% 3/5, 1.0% tied
- Action distribution: CHECK 49.6% / BET 17.4% / FOLD 14.6% /
  CALL 12.6% / RAISE 5.9% (RAISE is rarest, will need class
  weighting or oversampling at training time)
- Known defect carried forward: Labeller 4 had a
  template-substitution defect on non-NFD §1.7 RAISE; consensus
  majority filters it for aggregate use, but per-individual-label
  uses must null L4 (documented in PR #101 review chain)

**Warm-start anchor:**
`river-rats-core/models/gto_model_v9_baseline_45feat.json`.

**Active labelling protocol:** `prompts/gto_labeller_v3.2.md`
(for any future labelling rounds).

## Q2. Last open directive — status

**Directive:** `MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
(content shipped via PR #104, master `14c2db1`).

**Named author:** LEAD-PROGRAMMER (per
`feedback_listen_to_orchestrator_always.md`,
orchestrator-named-author = sufficient authorisation).

**Goal:** train v9 student model (59-feature XGBoost
`multi:softprob` 5-class) warm-started from
`gto_model_v9_baseline_45feat.json` on 494-hand corpus + 2470
consensus labels. 5 seeds, 80/20 stratified split,
confidence-weighted samples, 5 litmus tests, per-class P/R
(esp. RAISE), feature-importance top-20.

**Round 12 review chain (post-build):** ml-architect (training
methodology) + gto-expert (10-prediction spot-check) + QC
(milestone pre-merge V-Implementation-Spec-Match +
V-Integration-Trace).

**Branch target:** `programmer/v9-3way-59feat-trainer-2026-04-27`
(does not exist yet on remote).

**Work done since directive issued:** none. No builder report
authored. No branch opened.

**Status (my read): EFFECTIVELY BLOCKED.** Pre-flight verification
of `river-rats-core/train_model.py` master HEAD against the
directive's invocation block reveals significant existence drift.

Directive's invocation cites 6 CLI flags:
```
--corpus --labels --warm-start --output --seeds --confidence-weighting
```

`train_model.py` master HEAD (511 lines):
- **No argparse / ArgumentParser** anywhere. Single sys.argv
  membership check at line 505: `if '--45feat' in sys.argv:`
- **Hardcoded input path** at line 498:
  `csv_file = 'training-data/train_3way_v3_combined.csv'`
- **CSV-only ingestion** — no JSONL reader present
- **Hardcoded output** in
  `train_and_evaluate()`: `gto_model_v9_3way_v3_45feat.json`
- **No warm-start mechanism**: `grep -n
  "warm.start\|warm_start\|xgb_model\|process_type"
  river-rats-core/train_model.py` returns zero hits

Per memory `feedback_spec_vs_infrastructure_code_drift.md` two
audit dimensions:
- **EXISTENCE drift (Pilot HALT severity):** 6 CLI flags, JSONL
  ingestion, warm-start mechanism, multi-seed runner, sample
  weighting, stratified split — none exist in master HEAD
- **CONTENT drift (HIGH-2 severity):** the cited invocation does
  not match any runnable path through the script

The directive itself anticipates this in §"Failure handling":
"train_model.py CLI mismatch / missing warm-start support: STOP,
report BLOCKED — orchestrator dispatches small Phase 12.5 fix."
This contingency has not been triggered because no builder
session has been authored since the directive shipped.

**Process drift on the directive itself:** Phase 12 directive
jumped to LEAD-PROGRAMMER as named author without a §6 Step 1
ml-architect design pass. PROCESS_GUIDE.md §6 sequences training
work as ml-architect → owner → architect → programmer → reviewer →
owner. The directive's "round 12 review chain" runs ml-architect
*after* the build, not before. This is the structural reason
the existence drift was not caught: there was no ml-architect
trainer-extension design phase to surface the missing CLI
surface before the directive shipped.

## Q3. Next step from my seat

**Phase 0 alignment (this stream).** Self-author orchestrator
state-of-project (this doc, 1 of 3). Dispatch parallel prompts
to LEAD-PROGRAMMER and QC requesting their state-of-project
reports answering the same five questions, independently
(no cross-consultation between them). Synthesise the three
reports into `SHARED_STATE_BASELINE_2026-05-02.md`. Owner
reviews + approves the baseline.

**After alignment, Phase 12.5 kickoff (proposal).** Restore §6
Step 1: ml-architect designs trainer extension scoped to —
argparse CLI surface (the 6 directive-cited flags), JSONL
corpus + label ingestion with `ref_id` join, XGBoost
warm-start mechanism at the 45→59 feature boundary
(or from-scratch with documented reasoning if warm-start
across a feature-count boundary is unsound — ml-architect
recommends, does not present a menu, per
`feedback_quality_default_no_ask.md` and
PROCESS_GUIDE.md §1.4), 5-seed runner, per-row sample
weighting from `consensus_confidence`, stratified 80/20
split. ml-architect design comm to `review/comms/`.

**Post-design, §6 sequence proper.** Owner approves
ml-architect plan → architect blueprint (insertion points
in `train_model.py`) → programmer implementation + run →
reviewer Gates 2.3 (feature importance) + 2.4 (reference
gate with v8/v9-3way-v2.2 baselines in same session,
solver-corrected scoring) → owner approves model → Phase 12
re-dispatch on the working trainer.

I am NOT issuing any of these directives in this doc.
This doc is alignment only. The Phase 12.5 kickoff (and the
Phase 0 builder/QC dispatch directives that precede it) wait
on owner sign-off of the shared baseline.

## Q4. Concerns / drift I see

| # | Concern | Evidence | Severity (my read) |
|---|---------|----------|-------------------|
| 1 | Existence drift: 6 CLI flags in Phase 12 directive vs `train_model.py` master HEAD | `train_model.py:505` (only `--45feat` present); zero argparse | Pilot HALT |
| 2 | Format drift: directive cites JSONL corpus + labels; script accepts CSV only | `train_model.py:498` hardcoded CSV path | Pilot HALT |
| 3 | Missing warm-start mechanism in `train_model.py` | grep zero hits on warm-start patterns | Pilot HALT |
| 4 | §6 Step 1 (ml-architect design) skipped on Phase 12 — directive went straight to programmer-named-author | PROCESS_GUIDE.md §6 vs PR #104 directive structure | Process HIGH-2 |
| 5 | Round 12 pre-merge review chain on PR #104 (the directive itself) appears to have not caught any of items 1–4. Either the chain wasn't run, or it didn't audit the directive against `train_model.py`. | Comms history shows no `REVIEW_*_PR104_*` files; QC retro-audit is warranted | Process HIGH-2 |
| 6 | 5-day activity gap (Apr 27 → May 02) is unexplained from comms | `ls -lt review/comms/` newest = `2026-04-27 21:51` | Note — flagged for owner |
| 7 | Two-terminal role ambiguity: this terminal's CLAUDE.md (`/home/rupertbeytell/river-rats-review/`) defines reviewer-only role; owner has overridden to orchestrator. Other terminals may be unaware of the override. | Owner instruction in conversation; no comms artefact yet establishes the role assignment for downstream terminals to verify | Process HIGH-2 |

Note on item 5: round 12 review chain was specified *post-build*
(ml-architect + gto-expert + QC review the trainer report and
artefacts). The drift here is in the *directive* itself,
which a pre-merge audit on PR #104 would have caught. QC
retro audit on PR #104 is the natural fix, but I am NOT
dispatching it from this doc — that's a directive,
not alignment.

## Q5. What I need from the other two terminals

**From LEAD-PROGRAMMER (state-of-project, 1 doc):**
- Independent five-question report; specifically your read on
  whether Phase 12 directive is executable against
  `train_model.py` master HEAD as it stands. If you concur
  with my drift inventory, cite evidence; if you disagree,
  show where I'm wrong.
- Explicit statement of any local working-tree state I should
  know about (per `feedback_github_is_state_not_local.md`,
  GitHub is state authority, but local drafts may exist).
- DO NOT consult the QC parallel report; DO NOT start any
  Phase 12 / Phase 12.5 work.

**From QC (state-of-project, 1 doc):**
- Independent five-question report; specifically your read on
  whether the round-12 pre-merge review chain that approved
  PR #104 has a structural gap that lets directive-vs-source
  drift through. The QC stream's "smarter over time" mandate
  per `project_river_rats_qc.md` is the right home for any
  audit-pattern fix here.
- Independent verification (or refutation) of my drift
  inventory in Q4 items 1–3.
- DO NOT consult the builder parallel report; DO NOT run any
  TC-23/TC-25 audit yet (Q3 may RECOMMEND one, that's fine).

**From owner:**
- Confirm 5-day gap rationale (planned pause vs stall I should
  understand).
- Confirm orchestrator role assignment for this terminal so
  downstream terminals can rely on directives from this seat.
  Suggest owner posts a one-line confirmation to comms or in
  conversation that I can quote in dispatch comms.
- After all three state-of-project reports land, review the
  `SHARED_STATE_BASELINE_2026-05-02.md` synthesis and either
  approve (unblocks Phase 12.5 kickoff) or redirect.

## Operating posture

- This doc is alignment only. No directives are issued.
- I will not dispatch the LEAD-PROGRAMMER and QC state-of-project
  prompts until the owner gives green light to the framing
  (those prompts will go as their own comms files + small PRs,
  following the existing `MAIN_TERMINAL_*_DIRECTIVE_*` pattern).
- I will not author Phase 12.5 kickoff until the shared
  baseline is approved.
- I will not modify `river-rats-core/` from this doc or the
  alignment stream that follows it.

## References

- Master HEAD: `14c2db1`
- Phase 12 directive: `review/comms/MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
- `train_model.py` master HEAD: `river-rats-core/train_model.py` (511 lines, line 505 = `--45feat` argv check)
- Corpus: `data/corpus_revision_500_hand_2026-04-27.jsonl`
- Labels: `data/corpus_revision_500_hand_labels_2026-04-27.jsonl`
- Warm-start anchor: `river-rats-core/models/gto_model_v9_baseline_45feat.json`
- Process: `docs/PROCESS_GUIDE.md` (esp. §0 phase transitions, §1.4 experts recommend, §6 mandatory training team, §8 reviewer recommendations)
- `CLAUDE.md` (project root) §1 plan-before-build, §5 stop conditions, §7 verify own output, §"Task decomposition mandatory"
- Memory: `feedback_listen_to_orchestrator_always.md`, `feedback_named_author_builds_not_polls.md`, `feedback_verify_source_not_plan.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `feedback_builder_grounds_before_executing.md`, `feedback_github_is_state_not_local.md`, `feedback_shared_tree_commit_hygiene.md`, `feedback_quality_default_no_ask.md`, `feedback_check_comms_before_wait.md`, `reference_river_rats_v2_restart_protocol.md`, `project_river_rats_qc.md`

**Status: ORCHESTRATOR STATE-OF-PROJECT POSTED (1 of 3). Waiting on (a) owner sign-off to dispatch LEAD-PROGRAMMER + QC parallel state-of-project prompts; (b) owner answers to Q5 asks above.**
