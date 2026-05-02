---
date: 2026-05-02
from: River Rats QC stream
to: Main terminal (orchestrator) · Lead-programmer · Owner
re: Phase 0 restart — three-way state alignment (QC seat)
status: ALIGNMENT — independent state-of-project view; no audit dispatched
---

# QC state-of-project alignment — Phase 0 restart

Independent re-grounding after 5-day gap (last commit `14c2db1` at
2026-04-27 19:51 SAST → today 2026-05-02). Probe sequence per
directive: `git fetch` + `git status` + `git log -20` + comms ls +
`gh pr list` + read v2 CLAUDE.md / PROCESS_GUIDE.md + my own QC
CLAUDE.md + 5 most-recent comms ground.

Working tree clean; local master at `14c2db1` matches `origin/master`;
no untracked drift.

---

## Q1 — Where are we?

**Master HEAD:** `14c2db1` — *"Orchestrator: Phase 12 directive — v9
student warm-start trainer (59-feat XGBoost) (#104)"*, merged
2026-04-27 19:51:32Z.

**Last shipped baseline (data layer):** PR #101 `Builder Phase 11C:
494-hand mass labels (2470 labels, v3.2 protocol, 0% refusal)` merged
at `78bad39`, 2026-04-27 19:31:07Z. Corpus + labels both present at:
- `data/corpus_revision_500_hand_2026-04-27.jsonl` (494 records, 880 KB)
- `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494 rows × 5-vote arrays, 1.45 MB, SHA `329c43b6...`)
- `data/corpus_revision_500_hand_2026-04-27.lock` (corpus lock attestation)

**Last code-touching merge:** PR #98 (Phase 11A mass-labelling scripts,
24 tests) at `26fa7db`, 2026-04-27 17:50:33Z.

**Last QC PR:** PR #102 (`qc/pre-merge-pr101-2026-04-27`) — APPROVE
clean on Phase 11C labels, merged 19:37:33Z 2026-04-27. My findings
file `~/river-rats-qc/findings/` is current through PR #80 (Phase 6
templates, 2026-04-27 15:21); the PR #98/#101 pre-merge audits ship
as v2-side comms only (not duplicated to QC repo findings/).

**Gap:** 5 days, 0 commits. Origin = local; no silent push during the
gap. Last `~/river-rats-qc/.last_seen_master_sha` value `14c2db1`
matches origin — QC tick #163 saw master move `26fa7db → 78bad39` but
PR #104 (Phase 12 directive) merged 4 minutes after that tick, so the
stored sha is one merge stale relative to my own log entry. Cosmetic.

**Dominant workstream this cycle (Phases 0-12):** corpus revision +
mass labelling. Commit topology since 2026-04-27 09:35:
- Phases 0-7: blueprint + code corrections + scenario expansion (PRs #53–#82)
- Phase 8: scenario module v3.6 + v3.6.1 carryforward (PR #87)
- Phase 9: 494-hand corpus FINAL (PR #70 force-push)
- Phase 10: PILOT_009 prior_actions duplicate fix (PR #70 follow-up)
- Phase 11A: mass-labelling dispatch + collect scripts (PR #98)
- Phase 11B/C: 5×494 mass labelling + consensus (PR #101)
- Phase 12: trainer directive open (PR #104) — **builder not yet engaged**

QC dispatched 4 audits in this window (PRs #92, #93, #99, #102) plus a
backlog response — all CONVERGED with the dispatched reviewer chain at
gate level.

---

## Q2 — Last open directive + status (independent read)

**Directive:** `MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
(merged via PR #104, master `14c2db1`).

**Named author:** LEAD-PROGRAMMER. Round 12 review chain (milestone):
ml-architect (training methodology) + gto-expert (poker realism on 10
held-out predictions) + QC (V-Implementation-Spec-Match +
V-Integration-Trace).

**Authorization:** orchestrator-named-author = sufficient per
`feedback_listen_to_orchestrator_always.md`; cost ~$0 (XGBoost CPU).

**Work done since directive landed:** **NONE that I can see.** No
branch `programmer/v9-3way-59feat-trainer-2026-04-27` exists locally
or on `gh pr list`. No `PROGRAMMER_REPORT_PHASE12_*.md` in
`review/comms/`. No new model artefacts in `river-rats-core/models/`
since 2026-04-21. The 5-day gap is exactly the gap between directive
issuance and any builder execution.

**Drift on the directive itself (independent QC read):** the directive
contains a high-likelihood pre-emptable BLOCK — see Q4 concern #1
below. Specifically, the proposed CLI invocation does not match the
shipped `train_model.py` argparse surface, and the directive
acknowledges this risk in its own §"Failure handling". Builder will
hit STOP-protocol on the first execution attempt unless Phase 12.5
lands first.

**Blockers I see:** (1) train_model.py CLI mismatch, (2) 45→59
warm-start mechanism unproven for stock XGBoost — both pre-emptable
via Phase 12.5.

---

## Q3 — Next step from QC seat (recommendation only)

After the orchestrator's `SHARED_STATE_BASELINE` synthesis + owner
sign-off — and assuming the Phase 12 / 12.5 path resolves the BLOCKERs
in Q4 — my next QC actions are:

1. **Pre-merge audit on the eventual Phase 12 trainer PR** (milestone
   gate per `feedback_qc_required_before_approval.md`). Vector plan:
   - **V-Implementation-Spec-Match:** training script CLI matches final
     directive (post-12.5); 59-feature schema match; warm-start path
     parameters as specified; multi-seed (5) actually executed; output
     paths land at directive-specified locations.
   - **V-Integration-Trace:** trained model loads cleanly via existing
     `gto_model.py` `predict_*` infrastructure; one held-out hand
     produces a 5-class softprob vector (no NaN); inference shape
     matches `oracle_router.py` consumer expectations.
   - **V-Source:** held-out accuracy + per-seed std-dev numbers in the
     trainer report match what re-running the script produces (sample
     1 seed empirically); litmus-test pass/fail claims match
     `training-data/3way_reference_40hand.jsonl` if that's the
     canonical reference.
   - **V-Allocator-Multi-Dim subclass for ML reporting:** distinguish
     train accuracy vs held-out accuracy vs litmus-set accuracy in the
     report — different denominators, different meanings (per
     incident #21 generalization).

2. **Post-merge TC-25 audit-trail integrity sweep** on PRs #98 and
   #101 (Phase 11A scripts, Phase 11C labels). Both merged with QC
   PRE-merge clean; TC-25 is the autonomous post-merge variant. Low
   priority; deferred until trainer PR cycle clears.

3. **Retro audit candidate (Q4 concern #3):** calibration discipline
   on Phase 11B 5-labeller dispatch — was `calibration_exam.py` re-run
   against v3.2-protocol checksum before mass dispatch? PROCESS_GUIDE
   §2.1 mandates "If knowledge base checksum changed since last
   calibration, re-calibrate. No exceptions." Builder report
   (`PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md`) doesn't document
   a re-calibration event. QC PR #99 / #102 didn't extend
   V-Implementation-Spec-Match to pre-flight calibration discipline.
   This is a **TC-23-class gap** — pre-dispatch infrastructure
   discipline. Not blocking trainer; flag for orchestrator scope
   decision.

**Until baseline + sign-off lands:** QC stays on alignment; no audit
dispatched, no /loop tick, no cross-stream comm to teaching/game.

---

## Q4 — Concerns / drift

### #1 — HIGH (likely BLOCKER): Phase 12 directive train_model.py CLI mismatch

The Phase 12 directive prescribes (`MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md` §"Step 3 — train"):

```
python3 river-rats-core/train_model.py \
  --corpus data/corpus_revision_500_hand_2026-04-27.jsonl \
  --labels data/corpus_revision_500_hand_labels_2026-04-27.jsonl \
  --warm-start river-rats-core/models/gto_model_v9_baseline_45feat.json \
  --output river-rats-core/models/gto_model_v9_3way_59feat_2026-04-27.json \
  --seeds 0,1,2,3,4 \
  --confidence-weighting 1
```

`train_model.py` at master HEAD `14c2db1` accepts only:
- `--full` (line 10 docstring; resolves to running on `features_25000.csv`)
- `--45feat` (line 505; diagnostic 45-feature run)

It loads from CSV via `load_csv(csv_path)`, not JSONL. It hard-codes
the 80/20 split with `random_state=42` (line 226-227). It does its own
5-fold CV (line 292-293) but does not expose multi-seed via flag. It
writes to a hard-coded path `gto_model_{model_version}.json` (line
355) where `model_version = 'v9_3way_v3'` (line 351). It does not
support warm-start as a CLI option, nor confidence-weighting.

**None of the 6 directive flags exist.** Corpus + labels are JSONL,
trainer expects CSV. Output filename is hard-coded.

The directive's own §"Failure handling" anticipates this:
> train_model.py CLI mismatch / missing warm-start support: STOP,
> report BLOCKED — orchestrator dispatches small Phase 12.5 fix

**Recommendation:** orchestrator pre-empts by issuing Phase 12.5
*before* builder attempts Phase 12 — saves a wasted build cycle and
lets ml-architect pre-design the warm-start mechanism (Q4 concern #2)
in the same Phase 12.5 scope.

**Test class implication:** TC-23 (pre-dispatch infrastructure
existence) extended to *infrastructure-CLI-surface* — when a directive
prescribes a script invocation, verify the flags exist in the
script's argparse surface at master HEAD before merging the
directive. Pattern adjacent to incident #17 PRE-DISPATCH-table
prose-existence drift; same QC class, narrower target. **Curative
addition candidate** (would have caught this directive at PR #104
pre-merge if QC had been on the round-12 directive review chain;
directive PRs are typically not gated by QC because they're
proposals — but milestone-class directives that prescribe specific
CLI invocations are higher-risk and warrant a TC-23-CLI sub-vector).

### #2 — MEDIUM: 45→59 warm-start mechanism unproven

The directive proposes warm-starting a 59-feature student model from
the 45-feature baseline at `river-rats-core/models/gto_model_v9_baseline_45feat.json`.

Stock XGBoost warm-start (`xgb_model=` parameter to `fit()`, or
`booster.update()` with `process_type='update'`) requires identical
feature schema across the warm-start chain. The 45→59 boundary means
either:
- Pre-pad the baseline's leaves to a 59-feature input space (custom
  surgery on the booster JSON), or
- Curriculum: train a 45-feat student on the new corpus first, then
  expand to 59-feat as a from-scratch run with the baseline used only
  as priors (not warm-start in the strict sense), or
- Distillation: use the 45-feat baseline as a teacher, train the
  59-feat student to match its predictions on overlapping features
  (different protocol entirely)

The directive defers this ("If train_model.py doesn't support
warm-start at this 45→59 boundary, builder reports BLOCKED — Phase
12.5 directive will resolve"). **Recommendation:** ml-architect
pre-designs the mechanism *before* Phase 12.5 lands the trainer code
changes. The decision point is design-class (which approach is
correct), not implementation-class (how to wire flags) — the right
forum is an ml-architect dispatch, not a builder STOP-protocol report.

### #3 — MEDIUM: Calibration discipline on Phase 11B mass labelling — undocumented

PROCESS_GUIDE §2.1 (master at `14c2db1`):
> Calibration before labelling
> - MANDATORY before every labelling round.
> - Must use the BLIND exam: agent sees situations without answers.
> - Gate: 20/24 minimum + all 3 GTO-reversal hands correct.
> - **If knowledge base checksum changed since last calibration,
>   re-calibrate. No exceptions.**

The v3.2 protocol added DO NOT Rule 11 (paired-board / 2-tone-flush
OOP CHECK exception), KB §1.7 OVERRIDE (nut-FD raise gated on
`villain_air_pct >= 0.20`), and the river checked-to override (d3178
pattern) — all KB-checksum-changing additions vs the v3.1.2 protocol
used in earlier rounds.

Builder report `PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md` does
not document a calibration event before the 5 labellers were
dispatched. The §"v3.2 protocol application notes" section reports
*post hoc* that all 5 labellers fired the new rules, but that's not
calibration — that's self-attestation in the labels themselves.

QC PR #99 (Phase 11A scripts) covered the dispatch/collect *plumbing*
— not the calibration pre-flight discipline. QC PR #102 (Phase 11C
labels) covered output schema + 0% refusal — not whether labellers
were calibrated against the new KB checksum first.

**Severity:** MEDIUM — does not invalidate the 2470 labels (PR #103
synthesis already accepted them with both ml-architect and gto-expert
APPROVE-WITH-NITS), but the discipline gap is itself a process drift
worth flagging for retro audit. **Recommendation:** orchestrator
confirms whether calibration-vs-v3.2-checksum was run (perhaps in
a comm I missed) or whether this is a genuine §2.1 discipline gap to
log under TC-23 / PROCESS_GUIDE §2 audit class.

### #4 — MEDIUM: L4 labeller cluster defect — incident library candidate

Synthesis PR #103 documented gto-expert + ml-architect findings that
labeller-instance L4 fires §1.7 RAISE on non-NFD records (template
substitution defect; +48 RAISE vs L1's +17). Synthesis decision
**accept-as-is** on the basis that consensus_action filters L4 noise
(4-vs-1 majorities override; L4 coincident-not-causal on the 16
RAISE-consensus records).

Pattern for `incident_pattern_library.md` (would be #22):
> **Labeller-instance defect detected post-mass-labelling; consensus
> filter mitigates trainer signal but individual-label data is
> permanently noisy at the labeller_id level.**
>
> Test class implication: when a multi-labeller round ships, QC's
> V-Allocator-Multi-Dim should be applied to *labeller distributions*
> (not just allocator buckets) — flag any labeller whose action
> distribution diverges from the median by >2× on any class.
>
> Future cycles using individual labels (not consensus) must re-run
> or null L4 — already flagged in synthesis NIT backlog.

**Recommendation:** add as incident #22 to `incident_pattern_library.md`
with a curative TC sub-vector (V-Labeller-Distribution-Outlier)
queued for activation if individual-label cycles become live. Not
blocking Phase 12 (which trains on consensus_action only).

### #5 — LOW: `river-rats-core/models/` clutter

20 model files in `river-rats-core/models/`, dating Apr 5 → Apr 21,
including `v2_3_*` family (Apr 21) and `v9_3way_v2*` family (Apr 7)
that aren't referenced by the current oracle router or Phase 12
directive. Not blocking; cleanup candidate post-Phase-12 ship.
PROCESS_GUIDE §6 ("river-rats-core/ Is Sacred — only reviewed,
approved, passing files") arguably violated by the `v2_3_iter2_*`
intermediate artefacts. Flag for owner scope decision.

### #6 — LOW: Gap-since-last-activity hygiene observation

5 days with zero commits across orchestrator + builder + QC + teaching
+ game. State is consistent (origin/master = local master across all
3 repos I can probe; no silent push during the gap). Per
`feedback_github_is_state_not_local.md`, GitHub-as-authority discipline
held — the Phase 0 restart probe is the right entry pattern after a
gap of this size.

---

## Q5 — Asks of the other two terminals

### To orchestrator

1. **Pre-empt Phase 12 BLOCKED state** — issue Phase 12.5 directive
   *before* builder unblocks Phase 12. The directive's own
   §"Failure handling" predicts BLOCK; saving the build cycle is pure
   upside. Phase 12.5 scope I'd recommend (orchestrator decides):
   - ml-architect designs the 45→59 warm-start mechanism (concern #2)
   - lead-programmer extends `train_model.py` argparse to match the
     directive flags (concern #1) OR replaces with a fresh trainer
     script (e.g., `train_phase12.py`) that loads JSONL, supports
     warm-start, multi-seed, and confidence weighting
   - QC pre-merge audit on the Phase 12.5 PR before Phase 12 unlocks

2. **Confirm calibration-vs-v3.2-checksum status** for Phase 11B
   labellers (concern #3). If a calibration event happened that I
   didn't see in `review/comms/`, point me to the artefact. If not,
   confirm whether this is in scope for retro audit or accepted as a
   one-time gap.

3. **Triage L4 cluster defect** (concern #4) — confirm whether the
   incident-library entry #22 + V-Labeller-Distribution-Outlier
   sub-vector is the right curative class, or note an alternative
   classification.

### To lead-programmer

1. **Don't improvise on Phase 12 CLI mismatch.** STOP-protocol is the
   spec-correct response per the directive's own §"Failure handling"
   — wait for Phase 12.5 rather than monkey-patching `train_model.py`
   in-place. Improvising is the failure mode the project's CLAUDE.md
   §5 specifically calls out ("Improvising is worse than stopping").

2. **Pre-flight `git fetch` + `git status` after the gap** per
   `feedback_github_is_state_not_local.md` — confirm `master` matches
   `origin/master` before any branch-from-master, even though my probe
   showed clean state from the QC-side.

3. **If Phase 12.5 expands to "re-run or null L4"** (concern #4),
   re-calibrate the relevant labellers against the v3.2 KB checksum
   first per PROCESS_GUIDE §2.1 (concern #3 closure) before any
   re-labelling dispatch.

---

## References (master `14c2db1`)

- Phase 12 directive: `review/comms/MAIN_TERMINAL_PHASE12_TRAINER_DIRECTIVE_2026-04-27.md`
- Phase 11C builder report: `review/comms/PROGRAMMER_REPORT_MASS_LABELLING_2026-04-27.md`
- Phase 11C QC pre-merge audit: `review/comms/QC_PRE_MERGE_AUDIT_PR101_2026-04-27.md`
- Round 11 synthesis: `review/comms/MAIN_TERMINAL_PR101_LABELS_SYNTHESIS_2026-04-27.md`
- PROCESS_GUIDE §2.1 calibration: `docs/PROCESS_GUIDE.md`
- train_model.py current state: `river-rats-core/train_model.py` (no `--corpus / --labels / --warm-start / --output / --seeds / --confidence-weighting` flags at line 505)
- Models dir: `river-rats-core/models/` (`gto_model_v9_baseline_45feat.json` present, ~11.7 MB)
- QC operating manual: `~/river-rats-qc/CLAUDE.md`
- QC learning artefacts: `~/river-rats-qc/learning/` (incident_pattern_library through #21, test_class_registry through TC-26 + V-Allocator-Multi-Dim, coverage_map, curative_additions_log)
- Memory: `feedback_github_is_state_not_local.md`, `feedback_builder_grounds_before_executing.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestration_efficiency_rules.md`, `project_river_rats_qc.md`

---

**Status:** QC alignment-only deliverable. No audit dispatched; no
forward work; no consultation with builder's parallel report.
Standing by for orchestrator's `SHARED_STATE_BASELINE` synthesis +
owner sign-off before any Q3 action.
