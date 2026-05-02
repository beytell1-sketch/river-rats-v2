---
date: 2026-05-02
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (named author) · QC stream · Owner · ML-ARCHITECT (advisory)
re: Phase 12.5-prep — extend gto_model.py FEATURE_COLUMNS to 59 (operational)
status: DIRECTIVE — operational; owner approved S-1+S-2 on PR #111; round-12-prep review chain
---

# Phase 12.5-prep — FEATURE_COLUMNS extension to 59

## Authorization chain

- Owner approved S-1 (ml-architect design as-is, PR #110) + S-2
  (v9-3way-v2.2 substitute warm-start anchor) via "okay please
  continue" on `REVIEW_ORCHESTRATOR_PR110_PHASE125A_2026-05-02.md`
  (PR #111).
- S-3 defaulted to no canonical-state restoration (proceed with
  v2.2 substitution).
- S-4 defaulted to defer Project-State Housekeeping #PSH-01.
- Orchestrator-named-author authority per
  `feedback_listen_to_orchestrator_always.md`. This is **operational**
  — execute on git fetch.

## Why 12.5-prep exists separately from 12.5C

Per ml-architect's Phase 12.5A design (PR #110, §5 Item 4): the 4
v2.4 P1 blocker features are integrated into `gto_model.py`
`FEATURE_COLUMNS` as a **single source of truth (Path X)**, landing
**before** the 12.5C architect blueprint — so the architect cites
stable line numbers and the new student trainer imports a canonical
59-feature schema instead of duplicating it locally.

This 12.5-prep is a ~6-line surgical patch. ml-architect's design
serves as the architect blueprint for this trivial scope (collapsed
per `feedback_orchestration_efficiency_rules.md` — full §6
architect-as-separate-step is over-application for a 6-line patch).
The full §6 architect step lands at 12.5C for the new trainer
module (which is non-trivial).

## Scope (LEAD-PROGRAMMER, named author)

### Mandatory reads first

- `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md` — §5
  Item 4 (the change spec) + §12 references (cited line numbers).
  This is your blueprint.
- `review/comms/REVIEW_ORCHESTRATOR_PR110_PHASE125A_2026-05-02.md`
  §5 O-1 / O-2 (orchestrator decisions on this prep step).
- `river-rats-core/gto_model.py:33–64` — current `FEATURE_COLUMNS`
  tuple (55 entries) + `N_FEATURES = len(FEATURE_COLUMNS)  # 55`
  comment.
- `river-rats-core/feature_keys.py:87–92` — the 4 v2.4 P1 blocker
  feature constants (their canonical names).
- `scripts/verify_feature_schema_compatibility.py:33–42` — the
  authoritative ordering of `V24_P1_BLOCKER_FEATURES`.

### Patch — exact change

1. **Extend `gto_model.py:FEATURE_COLUMNS`** by appending 4 strings
   at the end of the tuple, in the order specified by
   `verify_feature_schema_compatibility.py:33–42`:

   ```
   "nut_flush_block",
   "flush_draw_block_pct",
   "straight_draw_block_pct",
   "nut_made_block_pct",
   ```

   Total tuple length post-patch: 59 entries (55 + 4).

2. **Update the comment at `gto_model.py:64`** from `# 55` to `# 59`.
   Line: `N_FEATURES = len(FEATURE_COLUMNS)  # 59`.

3. **No other changes** to `gto_model.py`. In particular, leave
   `_NAN_ALLOWLIST` (which already includes the 4 blockers per
   ml-architect §5 finding) untouched.

4. **No changes to** `train_model.py`, `feature_keys.py`,
   `feature_extractor.py`, or any model JSON.

### Regression test

Add a test under `river-rats-core/tests/test_feature_columns_v24_p1.py`
(new file). Two assertions:

```python
def test_feature_columns_count_is_59():
    from river_rats_core.gto_model import FEATURE_COLUMNS, N_FEATURES
    assert len(FEATURE_COLUMNS) == 59
    assert N_FEATURES == 59

def test_feature_columns_includes_v24_p1_blockers():
    from river_rats_core.gto_model import FEATURE_COLUMNS
    expected_blockers = {
        "nut_flush_block",
        "flush_draw_block_pct",
        "straight_draw_block_pct",
        "nut_made_block_pct",
    }
    assert expected_blockers.issubset(set(FEATURE_COLUMNS))
```

Match the exact import path used elsewhere in the test suite — if
the existing tests use `from gto_model import ...` instead of
`from river_rats_core.gto_model`, mirror that. Read existing tests
before writing.

### Verification before opening PR

- `python3 -c "from <appropriate_path> import gto_model; print(len(gto_model.FEATURE_COLUMNS), gto_model.N_FEATURES)"` must print `59 59`
- `pytest river-rats-core/tests/test_feature_columns_v24_p1.py -v` must show 2 PASS
- `pytest river-rats-core/tests/` (full suite) must show no new failures vs master baseline. Existing tests that import `FEATURE_COLUMNS` or `N_FEATURES` must continue to pass — older models loaded via `gto_model.py:104–107` `n_features_in_` auto-detect should be unaffected (they slice to their own width). If any existing test breaks, **STOP and report BLOCKED** — do not patch around it.
- `python3 scripts/verify_feature_schema_compatibility.py` if runnable — must pass.

### Output

- Branch: `programmer/phase125-prep-feature-columns-59-2026-05-02`
- PR title: `Builder Phase 12.5-prep: extend gto_model.py FEATURE_COLUMNS to 59 (4 v2.4 P1 blockers)`
- PR body must include:
  - Link to PR #110 (ml-architect blueprint source)
  - Link to PR #111 (orchestrator review + owner approval citation)
  - Diff stat (expected: ~2 files changed, ~6 insertions in gto_model.py + new test file)
  - Test results (counts of PASS/FAIL on full pytest suite)
  - Confirmation that `_NAN_ALLOWLIST` was NOT modified
  - Confirmation that `train_model.py`, `feature_keys.py`,
    `feature_extractor.py` were NOT modified

## Round-12-prep review chain

This is a milestone-class touch on sacred core. Per
`feedback_qc_required_before_approval.md` + the new TC-23-CANONICAL-STATE
sub-vector (orchestrator decision O-5 from PR #111):

- **QC pre-merge audit on the 12.5-prep PR** — TC-23-CONTENT
  (line-by-line diff matches ml-architect spec at PR #110 §5 +
  ordering matches `verify_feature_schema_compatibility.py:33–42`)
  + TC-23-CANONICAL-STATE (the patch doesn't introduce references
  to untracked artifacts; it only edits tracked source).
- **No ml-architect review on this PR** — the prep PR is the
  mechanical implementation of ml-architect's already-approved
  spec; re-reviewing would be re-litigation. ml-architect re-engages
  at 12.5E review chain on the 12.5D trainer PR.
- **No gto-expert review** — no poker decisions in this patch.

QC absorbs autonomously on PR open (per established pattern).

## Stop conditions

Per `CLAUDE.md` §5: stop, do not improvise.

- Existing test fails after patch: STOP, report BLOCKED
- `_NAN_ALLOWLIST` doesn't contain all 4 blockers (ml-architect's
  claim was based on `gto_model.py:228–231`): STOP, report
- Import path differs from ml-architect's blueprint: STOP, report
  the actual path
- Any tracked file outside `gto_model.py` and the new test file
  needs editing to make tests pass: STOP, report — that's a sign
  the FEATURE_COLUMNS change has wider downstream impact than
  ml-architect modeled

## Cost / risk

- ~$0 in API; ~6-line patch + 2-test file
- Risk: low — the change is append-only at the high end of the
  feature tuple; existing models slice to their own `n_features_in_`
  per `gto_model.py:104–107, 127–130`
- Failure mode: a downstream test reads `len(FEATURE_COLUMNS)` and
  hard-codes 55 somewhere — STOP protocol catches it, orchestrator
  amends scope

## What this directive does NOT cover

- 12.5C architect blueprint for the new student trainer module
  (orchestrator dispatches separately after 12.5-prep merges)
- 12.5D programmer implementation of the new trainer
- Phase 11B calibration discipline retro audit (separate workstream
  per D-5)
- L4 cluster defect formalisation (separate workstream per D-6)
- Project-State Housekeeping #PSH-01 (deferred per S-4)
- Restoring `gto_model_v9_baseline_45feat.json` to canonical state
  (deferred per S-3 default)

## Sequencing after 12.5-prep merges

On 12.5-prep PR merge, orchestrator dispatches **architect (12.5C)**
— full §6 architect step for the new student trainer module. That
directive will name ARCHITECT (subagent dispatch by orchestrator,
since blueprint authoring is orchestrator-scope per `CLAUDE.md`
"Task Decomposition Mandatory") and cite the ml-architect design +
this prep PR's final line numbers as the source. Do not pre-empt.

After 12.5C blueprint merges, lead-programmer dispatches for 12.5D
(implement + run + report).

## References

- Master HEAD: `765434b`
- ml-architect Phase 12.5A: PR #110 — `review/comms/PLAN_PHASE125A_TRAINER_DESIGN_2026-05-02.md`
- Orchestrator review + owner approval: PR #111 — `review/comms/REVIEW_ORCHESTRATOR_PR110_PHASE125A_2026-05-02.md`
- Phase 12.5 kickoff: master `765434b` — `review/comms/MAIN_TERMINAL_PHASE125_KICKOFF_2026-05-02.md`
- Shared baseline: master `b015873` — `review/comms/SHARED_STATE_BASELINE_2026-05-02.md`
- Process: `docs/PROCESS_GUIDE.md` §6, §1.4; `CLAUDE.md` §1, §6
- Memory: `feedback_listen_to_orchestrator_always.md`,
  `feedback_named_author_builds_not_polls.md`,
  `feedback_orchestration_efficiency_rules.md`,
  `feedback_qc_required_before_approval.md`,
  `feedback_spec_vs_infrastructure_code_drift.md`,
  `feedback_verify_source_not_plan.md`,
  `feedback_shared_tree_commit_hygiene.md` (use isolated worktree
  on the prep PR per the recurring multi-terminal HEAD races
  documented today)

**Status: PHASE 12.5-PREP DIRECTIVE OPERATIONAL. LEAD-PROGRAMMER named author; execute on git fetch. QC pre-merge audit on PR open per TC-23-CONTENT + TC-23-CANONICAL-STATE. No ml-architect or gto-expert review on this PR (mechanical prep). Orchestrator dispatches 12.5C architect after this PR merges.**
