---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable; persona spec embedded per builder dispatch)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #9 — Stage 3.5 commit 16 (`30dedc2`); delayed_probe HU-only predicate + PR #8 NIT cleanup
status: APPROVE — all 9 review items OK with HIGH confidence; no required fixes; 1 cosmetic NIT (positional-language imprecision in test comment); diff scope provably clean (3 files, telemetry-only)
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/9
---

# GTO Review Verdict — PR #9 (Commit 16, delayed_probe HU-only + PR #8 NITs)

## Provenance note

Same provenance pattern as PR #1-#8 verdicts. Read-only brief honored — verdict returned via message body; builder writes to `review/comms/`. Reviewer ran `python3 river-rats-core/tests/solver_verify_sidecars.py` and `python3 -m pytest river-rats-core/tests/test_commit13_sidecar_dryrun.py river-rats-core/tests/test_commit14_finding_b.py -v` directly against the PR branch (read-only execution per persona allowance).

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item A: "MW-41/FB-18/FB-19/SYN-F6_MW_all_live now route to `mw_per_villain`." **Verified by direct classifier execution.** All 4 entries return `mw_per_villain`; SYN-F3_HU_folded returns `folded_hu`. ✓
- Reviewer claim Item D: "HU synthetic delayed-probe routes to `delayed_probe` post-tightening." **Verified directly** (positions={CO,BTN}, num_positions=2, is_mw=False → predicate fires → `delayed_probe`). ✓
- Reviewer claim Item E: "24/24 PASS." **Verified by direct pytest run** — 24 passed in 2.36s on the PR branch. ✓
- Reviewer claim Item F: "delayed_probe=0, mw_per_villain=41, 6 buckets." **Verified by direct script run** — exact match to PR distribution table. ✓
- Reviewer claim Item I: "Diff scope = 3 files exactly." **Verified** by `git show 30dedc2 --stat` and `git diff master..30dedc2 --stat`: only `_reference_action_history_sidecar.py` (-1/+1), `solver_verify_sidecars.py` (+7/-0), `test_commit13_sidecar_dryrun.py` (+84/-1). ✓

All five spot-checks hold.

---

## Item A — `delayed_probe` predicate tightening correctness

**OK / HIGH confidence.** The change adds `and not is_mw` to the `delayed_probe` branch (`solver_verify_sidecars.py:169-172`):
```python
if (flop_check_count >= 1 and turn_present
        and not is_mw
        and any(e[0] == 'turn' and e[2] == 'BET' for e in action_history)):
    return 'delayed_probe'
```

`is_mw` is computed at line 114 as `num_positions >= 3` where `num_positions = len({e[1] for e in action_history})`. For the 4 named MW entries, all have postflop positions {CO, BTN, BB} (3 distinct) → `is_mw=True` → predicate gate now fails → falls through to PRIORITY 3 multiway branch → `mw_per_villain`.

Walked two MW entries through the new classifier mentally + confirmed by direct execution:

1. **MW-41** (3-way CO-open, double-barrel; `villain_pos=CO`):
   - positions={CO,BTN,BB}, num_positions=3, is_mw=True
   - has_fold=False → PRIORITY 1 skipped
   - flop has 1 BET (CO bet), no RAISE → `hu_bet_raise_call` skipped
   - flop_bet_count=1, turn_check_count=1 (BB), no turn CALL → `hu_bet_x_call_bet` skipped
   - flop_has_villain_bet=True (CO bet flop), but turn_check_count≥1 is True yet `not turn_has_call` is True; however river_present=False → `hu_donk_x_bet` (line 155) skipped
   - flop_check_count=1 (BB), but no river → check-through variant (line 160) skipped
   - flop_check_count≥1 + turn_present + turn-BET present, BUT `not is_mw` is False (is_mw=True) → `delayed_probe` skipped ✓
   - PRIORITY 3: is_mw=True → `mw_per_villain` ✓

2. **SYN-F6_MW_all_live** (3-way no-fold check-through; `villain_pos=CO`):
   - positions={CO,BTN,BB}, num_positions=3, is_mw=True
   - has_fold=False
   - flop_check_count=3, no flop BET → `hu_bet_raise_call`, `hu_bet_x_call_bet`, `hu_donk_x_bet` (both variants) all skipped
   - flop_check_count=3 + turn_present + turn-BET (BB bet), BUT `not is_mw` is False → `delayed_probe` skipped ✓
   - PRIORITY 3: is_mw=True → `mw_per_villain` ✓

For the new HU synthetic test fixture (`hu_delayed_probe_ah` in `test_commit16_delayed_probe_hu_only_predicate_routes_hu_correctly`):
- positions={CO,BTN}, num_positions=2, is_mw=False
- has_fold=False
- flop_check_count=2, no river → upstream branches skipped
- flop_check_count≥1 + turn_present + turn-BET (BTN bet) + `not is_mw` is True → returns `delayed_probe` ✓

Predicate tightening is correct. Bucket label "HU delayed-probe large turn bet" is now truthful by construction.

## Item B — NIT #1 fix correctness (`_reference_action_history_sidecar.py:192`)

**OK / HIGH confidence.** Old comment: `Category 4 (folded_mw → folded HU) : SYN-F3_HU_folded`. New comment: `Category 4 (folded_hu sentinel)    : SYN-F3_HU_folded`.

Verified SYN-F3_HU_folded routing under the post-commit-15+16 classifier:
- AH = `[('preflop','BTN','RAISE'), ('preflop','BB','CALL'), ('flop','BB','FOLD')]`
- positions={BB,BTN}, num_positions=2, is_mw=False
- has_fold=True, fold_streets={'flop'}, fold_on_postflop=True
- `not is_mw` → returns `folded_hu` (line 130) ✓

Direct classifier execution confirms shape=`folded_hu`. The new comment is faithful: SYN-F3_HU_folded routes to the `folded_hu` sentinel bucket (NOT `folded_mw_*`, since num_positions=2). The old wording conflated the pre-split label with the eventual route; the new wording is accurate.

## Item C — NIT #2 fix correctness (synthetic primary-fold AH reorder)

**OK / HIGH confidence on routing; MINOR terminology nit on inline comment.**

New AH:
```python
[('preflop','CO','RAISE'), ('preflop','BTN','CALL'), ('preflop','BB','CALL'),
 ('flop','CO','BET'), ('flop','BTN','CALL'), ('flop','BB','FOLD')]
```

Postflop position order in a 3-way CO-open pot is BB (OOP first to act) → CO → BTN. Realistic full sequence: BB CHECK → CO BET → BTN CALL → BB FOLD (action wraps back to BB facing the bet). The reordered AH omits the BB CHECK preamble (consistent with the sidecar convention of recording only voluntary non-CHECK-then-fold actions on the closer's path) and preserves the realistic CO-bet → BTN-call → BB-fold ordering.

Test intent preserved: villain_pos=BB, FOLD is on flop, fold_positions={BB}, BB ∈ fold_positions → `folded_mw_primary`. Direct classifier execution confirms shape=`folded_mw_primary` ✓.

**NIT (cosmetic, non-blocking):** The inline comment reads "BB acts last in position when CO opens preflop." BB is technically OUT OF POSITION (the OOP small/big blind), not "in position." The intended meaning is "BB acts last on this betting round because action wraps back to them after the bet+call." Slight terminology drift vs HARD RULE in `feedback_terminology_raise_vs_bet.md` neighborhood (positional-language precision). Doesn't affect behavior; clean up incidentally if commit-16.1 is needed for any reason.

## Item D — Test coverage of the 3 new commit-16 tests

**OK / HIGH confidence.**

1. **`test_commit16_delayed_probe_hu_only_predicate_routes_hu_correctly`** — synthetic HU AH with positions={CO,BTN}, flop check-through, turn lead. Asserts shape=='delayed_probe'. Walked above; routes correctly. Test correctly exercises that `not is_mw` does NOT exclude legitimate HU shapes.

2. **`test_commit16_delayed_probe_mw_falls_through_to_mw_per_villain`** — iterates the 4 named corpus entries (MW-41, FB-18, FB-19, SYN-F6_MW_all_live), asserts each shape=='mw_per_villain'. Direct execution confirms all 4 pass. Strong test: locks in the fix-spec exactly.

3. **`test_commit16_delayed_probe_bucket_truthfulness_on_corpus`** — universal-quantifier sweep: every live `delayed_probe` entry must have num_positions<3. Vacuously holds on the current corpus (0 entries) but fires when Stage 6 lands real HU delayed-probes; will catch any future regression that re-loosens the predicate.

**Minor coverage gap (informational, non-blocking):** Test #1 uses a synthetic HU AH that is NOT in the corpus. The predicate tightening's "vacuously true" behavior on the current corpus is intentional, but a future authoring of a real HU delayed-probe will be the first end-to-end exercise of the bucket. Test #1 plus test #3 jointly cover this: #1 verifies the predicate STILL fires on a real HU shape (not just the gate that excludes MW); #3 will catch any future MW leakage. Coverage is adequate.

Assertions are correct; nothing missing for the stated commit-16 scope.

## Item E — Existing tests not broken

**OK / HIGH confidence.** Direct pytest run on PR branch returned `24 passed in 2.36s`. Spot-checked the test inventory for `delayed_probe`-dependent assertions:
- `grep -rn "delayed_probe" river-rats-core/` returns matches only inside the 3 NEW commit-16 tests + the new comment in `solver_verify_sidecars.py` + the static `_SHAPE_PATTERNS` label.
- No pre-existing test asserts on `delayed_probe` containing MW entries.
- `test_commit13_2_5_hu_donk_x_bet_bucket_covered` (SYN-F7) — different branch.
- `test_commit13_2_6_classifier_position_aware_donk` — different branch.
- `test_must66_stratification_covers_multiple_shapes` — distribution-dependent; covered in Item F.
- `test_commit14_finding_b.py` (4 tests) — feature_extractor.py path; unrelated.

PR description's 24/24 PASS claim is accurate.

## Item F — Distribution stability — MUST #66

**OK / HIGH confidence.** Direct script run produced bucket count = 6 (matches PR distribution table). MUST #66 asserts `len(by_shape) >= 3`. 6 ≥ 3 trivially holds. Live distribution:
- `folded_hu`: 1
- `folded_mw_offvillain`: 38
- `hu_bet_raise_call`: 1
- `hu_bet_x_call_bet`: 2
- `hu_donk_x_bet`: 3
- `mw_per_villain`: 41

`folded_mw_primary` and `delayed_probe` are both empty on the live corpus. No other distribution-dependent test exists (verified via grep). `_stratified_sample` uses `max(1, int(round(len(ids) * pct)))` per shape — it iterates `by_shape` so empty shapes simply don't appear; no division-by-zero risk.

## Item G — No production paths touched / no creep

**OK / HIGH confidence.** `git diff master..30dedc2 --stat` shows exactly 3 files:
- `river-rats-core/_reference_action_history_sidecar.py` (+1/-1) — single-line doc comment fix
- `river-rats-core/tests/solver_verify_sidecars.py` (+7/-0) — predicate gate + comment
- `river-rats-core/tests/test_commit13_sidecar_dryrun.py` (+84/-1) — NIT #2 reorder + 3 new tests

No `feature_extractor.py`, no `range_narrowing.py`, no `oracle_router.py`, no `gto_model.py`, no `range_manager.py`, no `coaching/` touches. The 1-line change to `_reference_action_history_sidecar.py` is inside a docstring/comment block (line 192, inside `_REFERENCE_ACTION_HISTORY` dict's authoring annotation — does not alter any data structure value). Telemetry-only claim is accurate.

## Item H — Bucket label truthfulness (keeping empty bucket)

**OK / HIGH confidence.** Keeping `delayed_probe` in `_SHAPE_PATTERNS` with 0 live entries is the right call. Rationale:
- Bucket label exists for future Stage 6 corpus authoring; removing it now would force a re-add later when real HU delayed-probes land.
- `_stratify` is dict-of-list keyed by classifier output; empty-bucket means the key simply doesn't appear in `by_shape` (verified by run output — only 6 keys printed). No "empty bucket noise" in stratification output.
- `_SHAPE_PATTERNS` is a label registry, NOT a manifest of "must be populated" buckets. The `dict(_SHAPE_PATTERNS).get(shape, '(unknown)')` lookup pattern in `main` is forward-compatible with the empty bucket.
- Test #3 (`test_commit16_delayed_probe_bucket_truthfulness_on_corpus`) is explicitly designed to fire on Stage 6 corpus growth — keeping the label preserves the test's purpose.

This is consistent with the project pattern from commit 15 (`folded_mw_primary` retained as empty post-split).

## Item I — Stale-tree recovery

**OK / HIGH confidence.** `git log --oneline master..30dedc2` shows exactly 1 commit. `git diff master..30dedc2 --stat` shows exactly 3 files (matches PR description's "no production paths touched" claim). No spurious changes to commit-14 (`test_commit14_finding_b.py` unchanged in this PR — confirmed by stat) or commit-15 work (the `test_commit15_*` tests survive intact with only the NIT #2 reorder applied to `test_commit15_folded_mw_split_primary_routes_correctly`).

The PR description's "Stale-tree state caught + recovered before authoring" claim is consistent with the diff scope. Recovery is provably clean.

---

## VERDICT

**APPROVE**

**Rationale:** Commit 16 is a faithful, minimal, telemetry-only execution of the BUILDER_COMMIT16_SCOPE plan. The `delayed_probe` predicate tightening correctly excludes the 4 mis-routed MW entries (verified by walking MW-41 + SYN-F6_MW_all_live through the classifier and by direct execution on the corpus), legitimate HU delayed-probe shapes still route correctly (verified on the test fixture), the 3 new tests are well-targeted (positive HU + negative MW + universal truthfulness sweep), no production paths are touched (3 files, all in `tests/` or doc-comment), no existing tests are broken (24/24 PASS confirmed by direct pytest), distribution stability holds (6 buckets ≥ 3), and the 2 PR #8 NITs are correctly addressed.

The bucket label `delayed_probe` is now truthful by construction: empty on the current corpus (HU corpus has no real delayed-probes), and any future MW leakage will fail the bucket-truthfulness test.

**Required fixes:** None.

**Blockers:** None.

**Stale-tree recovery assessment:** **CLEAN.** Diff scope is exactly 3 files; commit-14 + commit-15 work intact on master.

**NIT-level observations (informational, optional follow-up):**

1. **Positional-language imprecision in NIT #2 inline comment.** `test_commit13_sidecar_dryrun.py` test comment says "BB acts last in position when CO opens preflop." BB is OOP, not "in position"; the intended meaning is "BB acts last on this betting round because action wraps back to them after the bet+call." Cosmetic; clean up incidentally if any commit-16.1 is needed for unrelated reasons. Doesn't affect routing or test correctness.

That is the only NIT observed.

**Greenlight commit 17:** N/A — commit 16 is the FINAL substantive Stage 3.5 commit per orchestrator's PR #8 greenlight. Next step is M4/M5 audits.

---

## Action

**Builder:**
1. Write this verdict to `review/comms/GTO_REVIEW_VERDICT_PR_9_2026-04-26.md`.
2. Post comment on PR #9 referencing the verdict.
3. Stand by for orchestrator merge.
4. Ready M4/M5 audit pre-flight per Stage 3.5 ship gate.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check.
3. Merge PR #9 with `gh pr merge 9 --merge --delete-branch`.
4. After merge: declare Stage 3.5 substantive code-commit phase SEALED. Trigger M4/M5 audit cadence per shipping plan.

**Owner:** wake to find merged commit 16 + Stage 3.5 substantive-commit phase complete + M4/M5 audit gate live.

## Reference

- PR #9: https://github.com/beytell1-sketch/river-rats-v2/pull/9
- Feature commit: `30dedc2`
- Scope doc: `review/comms/BUILDER_COMMIT16_SCOPE_2026-04-26.md` (`66a06c0`)
- Predecessor verdict: `review/comms/GTO_REVIEW_VERDICT_PR_8_2026-04-26.md` (`488310f`)
- Rollback tag: `stage3.5-pre-commit-16` at master `03b89e6`
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
- Restart protocol: `review/comms/BUILDER_RESTART_PROTOCOL_2026-04-25.md`

**FINAL VERDICT: APPROVE — HIGH confidence overall.**
