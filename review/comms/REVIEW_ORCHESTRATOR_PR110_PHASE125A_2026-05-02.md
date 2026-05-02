---
date: 2026-05-02
from: Main terminal (orchestrator)
to: Owner · ML-ARCHITECT · LEAD-PROGRAMMER · QC stream
re: Orchestrator review of PR #110 (Phase 12.5A v9 student trainer design) + 12.5B gate prep
status: REVIEW + ORCHESTRATOR FINDINGS — owner decision needed on one scope question
---

# Orchestrator review — PR #110 (Phase 12.5A trainer design)

## Headline

ML-architect's design (`PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md`,
PR #110, 964 lines) is **well-grounded and committed** — all six
items contain decisions with reasoning, not menus. All locked
premises independently verified. The four drifts ml-architect
surfaced are correct and properly handled.

**However, orchestrator independent verification surfaced a fifth,
deeper drift the design is downstream of: project-wide model-file
tracking inconsistency via `.gitignore`.** This is not ml-architect's
fault to fix — it pre-dates Phase 12 by months — but it changes the
shape of the 12.5B gate decision. Owner needs to choose between
proceeding with ml-architect's substitution path or pausing for
project-state cleanup first.

## §1. Independent verification of locked premises

I re-verified each locked premise from the kickoff against master
HEAD `765434b`, NOT trusting ml-architect's claims:

| Locked premise | My verification | Result |
|----------------|-----------------|--------|
| `55 + 4 = 59` arithmetic | `gto_model.py:64` `N_FEATURES = len(FEATURE_COLUMNS)  # 55`; `feature_keys.py:87–92` lists 4 v2.4 P1 blockers | **PASS** |
| Join key: `corpus.source_situation_id == labels.ref_id` | Read corpus row 1 `source_situation_id = 'd6066_BB_flop'`; labels row 1 `ref_id = 'd6066_BB_flop'` | **PASS** |
| 5-class `multi:softprob` | `gto_model.py:29` `ACTION_CLASSES = ("FOLD", "CHECK", "CALL", "BET", "RAISE")` (5 elements); v2.2 model JSON `num_class = 5`, `num_feature = 45`, 645 trees, `multi:softprob` | **PASS** |
| Seed count 5, split 80/20 | Locked by orchestrator; ml-architect adopted | **Adopted** |
| Litmus comparison vs v8 + v9-3way-v2.2 | ml-architect's design routes through `reference_evaluator.evaluate_variants` with `--baseline-models` flag — same-session multi-model evaluation reachable | **Adopted** |

All locked premises hold. No BLOCKED state.

## §2. Six items — orchestrator verification (decision vs menu)

| Item | ml-architect decision | Menu? | Reasoning grounded? |
|------|----------------------|-------|---------------------|
| 1 | New module `river-rats-core/train_model_v9_student.py` | NO menu — single decision with 5 reasons cited (CLAUDE.md §6 addendum, `train_model.py` v9-3way-v3 single-purpose, schema divergence, sacred-core extension pattern, revert-asymmetry) | **YES** (cites file:line evidence throughout) |
| 2 | Pre-pad baseline + `xgb_model=` continued training | NO — pre-pad chosen, curriculum/distillation/from-scratch explicitly rejected with reasons | **YES** |
| 3 | Pure `sample_weight = consensus_confidence` | NO — pure chosen, hybrid/class-normalised explicitly rejected with reasons | **YES** |
| 4 | Path X (extend `gto_model.py:FEATURE_COLUMNS` to 59) as **12.5-prep PR** before 12.5C | NO — Path X chosen, Path Y rejected; 12.5-prep timing chosen, 12.5D-bundle rejected | **YES** |
| 5 | Existing 40-hand MW-11..MW-50 set parsed by `reference_evaluator.py` from `design/multiway_reference_set/` markdown source — no new JSONL | NO — single decision after full audit table of 5 candidate JSONLs (all rejected with reasons) | **YES** |
| 6 | 80/20 stratified by class label `y` (alone), 5 seeds 0–4, per-seed table + mean ± std | NO — `y` chosen, `y × confidence` and `y × street` rejected with reasons (especially the "any stratum < 5 fails sklearn split" risk on confidence cross-product) | **YES** |

Plus committed beyond the six items:
- **Hyperparameters** (committed values mirror v9-3way-v2.2 lineage with reasoning)
- **Trainer CLI surface** (full argparse with 11 flags, defaults, help strings)
- **Gate 2.3 + 2.4 hooks** (function signatures specified)
- **Risk register** (5 entries with mitigations)

**Verdict on six items:** all decisions, no menus. Compliant with
`PROCESS_GUIDE.md` §1.4 and `feedback_quality_default_no_ask.md`.

## §3. Drifts — independent verification

| ml-architect drift claim | My verification | Verdict |
|--------------------------|-----------------|---------|
| `gto_model_v9_baseline_45feat.json` does not exist on master HEAD | `git cat-file -e origin/master:river-rats-core/models/gto_model_v9_baseline_45feat.json` returns "exists on disk, but not in 'origin/master'" — **the file is on local working tree (11.7MB, untracked) but NOT in master** | **CORRECT** |
| RAISE count 16 → 29 | Direct labels-file count: `consensus_action == 'RAISE'` = 29 | **CORRECT** |
| Confidence 0.5 → 0.4 | Direct labels-file count: `consensus_confidence ∈ {1.0:309, 0.8:109, 0.6:71, 0.4:5}`, no 0.5 | **CORRECT** |
| `training-data/3way_reference_40hand.jsonl` does not exist | `ls training-data/3way_reference_40hand.jsonl` → no such file | **CORRECT** |

ml-architect handled all four drifts cleanly within the design.

## §4. Orchestrator-surfaced new finding (the deeper drift)

The R-3 drift (warm-start anchor missing on master) is the visible
tip of a project-wide state issue that none of the three Phase 0
state-of-project reports caught — including mine.

**Root cause:** `.gitignore` line 3 excludes `*.json` globally,
with only two whitelist exceptions for Claude settings:

```
*.json
!.claude/settings.json
!river-rats-complete/.claude/settings.json
```

**Consequence — `git ls-files river-rats-core/models/` vs `ls`:**

| Tracked in master | Present locally only (untracked, ignored) |
|-------------------|-------------------------------------------|
| `gto_model_v9_3way_v2.2.json` (414 KB) | `gto_model_v9_baseline_45feat.json` (11.7 MB) |
| `training_report_v9_3way.json` | `gto_model_v8_38feat.json` |
| `v2_2_*.json`, `v2_3_*.json` (older artifacts) | `gto_model_v8_hu.json` |
| | `gto_model_v9_3way.json`, `_45feat.json`, `_v2.json`, `_v2.1.json`, `_v3.json`, `_v3_45feat.json`, `_warmstart.json` |
| | `raise_sizing_model.json` |

The two highest-value cited artifacts (the baseline warm-start anchor
+ the v8 baseline used as a Gate 2.4 reference) are **NOT in
canonical state**. This means:

1. **Phase 12 directive's invocation never could have worked** on a
   clean checkout — the warm-start anchor it cites is not in the
   repo
2. **`river-rats-core/tests/test_corpus_revision_v3.py:29`** references
   `gto_model_v9_baseline_45feat.json`; this test would fail on any
   fresh checkout / CI runner
3. **The Phase 0 alignment reports (#105, #106, #107)** all cited the
   baseline as if it were canonical — because we all happened to have
   it locally
4. **ml-architect's substitute (v2.2) is not just a courtesy — it's
   the only methodologically-honest choice** given canonical state

This drift is **out of Phase 12.5 scope** but materially affects
the 12.5B decision: do we accept v9-student trained against v2.2
(tighter loop, possible 3way-overlap leakage), or do we pause and
restore canonical state first?

## §5. Orchestrator decisions (within orchestration scope)

### O-1 — 12.5A design APPROVED for owner gate

ml-architect's design is technically clean — six committed decisions,
verified locked premises, line-cited reasoning, drifts handled. The
design proceeds to 12.5B for owner ratification.

### O-2 — 12.5-prep PR (Path X FEATURE_COLUMNS extension) follows ml-architect's recommendation

The 12.5-prep PR (~6-line patch to `gto_model.py:33–62, 64`) lands
**before** 12.5C blueprint. Architect (12.5C) writes against the
post-prep line numbers. This sequence is committed.

### O-3 — Methodology substitution (v2.2 anchor) provisionally accepted

In the absence of a canonical baseline_45feat artifact on master,
v9-3way-v2.2 is the only available 45-feat 5-class warm-start anchor
that is reproducible from a fresh checkout. ml-architect's
substitution is therefore the methodologically-honest choice given
current state. **However, this is downstream of the project-state
question in §6; if the owner directs canonical-state restoration
first (S-4 below), 12.5A will be re-targeted.**

### O-4 — Project-state housekeeping flagged as parallel workstream

Independent of Phase 12.5, the `.gitignore *.json` exclusion + 10+
untracked baseline/intermediate model files is a project-state
hygiene issue worth a separate workstream. This becomes
**housekeeping #PSH-01** (Project-State Housekeeping). Not blocking
12.5; logged for future scope.

### O-5 — QC stream gets new TC-23 sub-vector for project-state existence drift

This is the second instance (after Phase 12 directive's CLI drift)
where a directive cited an artifact that didn't exist in canonical
state. **Curative addition: TC-23-CANONICAL-STATE sub-vector** —
when a directive cites a file path, QC pre-merge audit verifies
the file is in `git ls-files`, not just on local disk. Adds to
QC's `curative_additions_log` per existing D-4 framework. (QC
absorbs autonomously; no separate dispatch needed.)

## §6. Owner-class decision points

### S-1 — 12.5B gate: approve ml-architect's design as-is?

If yes, orchestrator dispatches:
1. **12.5-prep PR** (architect-led patch to extend `gto_model.py`
   `FEATURE_COLUMNS` to 59), with QC pre-merge audit per TC-23 (D-4)
2. After 12.5-prep merges, **12.5C architect blueprint** for the
   new student trainer module
3. After 12.5C merges, **12.5D programmer** implements + runs trainer
4. **12.5E review chain** (ml-architect + gto-expert + QC)
5. **12.5F owner ship gate**

If no (revisions needed): owner specifies revision scope,
ml-architect re-runs 12.5A.

### S-2 — Methodology substitution: accept v9-3way-v2.2 as warm-start anchor?

This is a real methodology question, not just a paperwork concern.
v2.2 was trained on 348 3way situations that may overlap the 494-hand
corpus → leakage risk. The `PROCESS_GUIDE.md` §2.2 leakage check at
12.5D pre-flight is the existing safeguard, but it would need to
catch any overlap rather than the trainer assuming cleanliness.

- **Accept:** proceed with v2.2 substitution. 12.5D leakage check is
  the gate.
- **Don't accept:** see S-3.

### S-3 — Restore canonical state before 12.5C?

Three sub-options if S-2 is rejected:

- **S-3a** — owner has the original
  `gto_model_v9_baseline_45feat.json` (11.7MB local file is
  authentic): commit it via `git add -f` (override .gitignore)
  before 12.5C dispatches. ml-architect's R-3 substitution becomes
  unnecessary; trainer warm-starts from baseline. **This requires
  authentication of the local file's provenance** — there's no
  visible script in master that produced it.
- **S-3b** — re-train the v9 baseline from PokerBench: separate
  workstream, weeks of cost, blocks Phase 12.5 entirely. Not
  recommended.
- **S-3c** — accept that the directive's anchor was always
  aspirational and rename/re-target everywhere. Comms history
  becomes inconsistent. Not recommended.

### S-4 — Open Project-State Housekeeping (#PSH-01) workstream now or defer?

The broader `.gitignore *.json` issue is real. Parallel options:

- **S-4a (now):** dispatch a separate housekeeping PR to either
  (i) selectively `-f`-add the canonical v9 baseline and v8 baseline
  files, or (ii) refactor to a `models/MANIFEST.md` listing canonical
  artifacts with provenance scripts, and treat untracked files as
  scratch
- **S-4b (defer):** log #PSH-01 in a backlog comm, address
  post-Phase-12.5 ship

Recommended (orchestration scope, advisory): **S-4b defer**. The
Phase 12.5 critical path doesn't require it; resolving #PSH-01
properly will take a separate design + review cycle that would
extend the gap unnecessarily.

## §7. Orchestrator dispatch sequencing if S-1 + S-2 approved

Slow and steady, one stage at a time:

1. **Now (post-12.5B):** orchestrator dispatches **architect (12.5-prep)**
   with a tight scope: extend `gto_model.py:FEATURE_COLUMNS` to 59
   per ml-architect's specified ordering, update `# 55` comment to
   `# 59`, add a regression test asserting `len(FEATURE_COLUMNS) ==
   59` and the 4 blocker names are present. Single-file (or two-file)
   PR. QC pre-merge audit per TC-23.
2. **After 12.5-prep merges:** orchestrator dispatches **architect
   (12.5C)** for the trainer-module blueprint. Architect cites
   stable post-prep line numbers.
3. **After 12.5C merges (owner gate):** orchestrator dispatches
   **lead-programmer (12.5D)** to implement + run.
4. **After 12.5D PR opens:** **round 12 review chain** (ml-architect +
   gto-expert + QC). QC pre-merge audit on 12.5D PR per the new
   TC-23-CLI sub-vector (D-4) and TC-23-CANONICAL-STATE sub-vector
   (O-5).
5. **12.5F owner ship gate** if review chain converges to APPROVE.

Each stage is a separate dispatch with its own owner gate.

## §8. References

- This review is based on master HEAD `765434b` and PR #110 head `8cb3f190`.
- ml-architect design comm: `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` (PR #110, 964 lines)
- Phase 12.5 kickoff: `review/comms/MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md` (master `765434b`, PR #109)
- Shared baseline: `review/comms/SHARED_STATE_BASELINE_2026-05-02.md` (master `b015873`, PR #108)
- Verifications run by orchestrator:
  - `git cat-file -e origin/master:river-rats-core/models/gto_model_v9_baseline_45feat.json` → not present
  - `git ls-files river-rats-core/models/` → 21 files; baseline absent
  - `.gitignore` line 3: `*.json` global exclusion
  - Direct corpus + labels JSONL inspection (494 records, RAISE=29, conf dist {1.0:309, 0.8:109, 0.6:71, 0.4:5})
  - v2.2 model JSON inspection (`num_class=5, num_feature=45, num_trees=645, multi:softprob`, `feature_names=` empty list)
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_verify_source_not_plan.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_quality_default_no_ask.md`, `feedback_github_is_state_not_local.md`

**Status: ORCHESTRATOR REVIEW POSTED. Owner needs to decide S-1 (approve design as-is or revise), S-2 (accept v2.2 substitution or restore baseline), and optionally S-3/S-4 (sub-options). On S-1+S-2 approval, orchestrator dispatches 12.5-prep architect immediately. No work on `river-rats-core/` until S-1+S-2 land.**
