---
date: 2026-04-26
from: General-purpose subagent acting as GTO reviewer (gto-expert subagent unavailable in builder session; owner authorised general-purpose dispatch with gto-expert persona embedded)
to: Main terminal (orchestrator) · Owner
re: Per-batch GTO review on PR #8 — Stage 3.5 commit 15 (`d090743`); classifier promiscuity cleanup (folded_mw split)
status: APPROVE — all 7 review items OK with HIGH confidence; no required fixes; 2 cosmetic NITs; stale-tree recovery confirmed clean; orchestrator can merge with --merge --delete-branch
pr: https://github.com/beytell1-sketch/river-rats-v2/pull/8
---

# GTO Review Verdict — PR #8 (Commit 15, Folded_MW Split)

## Provenance note

Same provenance pattern as 13.2.5 / PR #1-7 verdicts. Read-only brief honored — agent returned via message body, no file writes. Verdict authored on master per `git checkout master BEFORE` recipe.

## Builder verification spot-checks (pre-publish)

- Reviewer claim Item C: "FB-21 routes to `folded_mw_offvillain` (3-way; BTN folds turn, primary CO live)." **Verified by mental walkthrough.** FB-21 has positions {CO, BTN, BB} (is_mw=True), single FOLD `('turn', 'BTN', 'FOLD')`, villain_pos=CO. fold_positions={'BTN'}; CO ∉ {'BTN'} → `folded_mw_offvillain`. ✓
- Reviewer claim Item F: "Recovery clean — only 2 files in diff." **Verified.** `git show --stat d090743` shows exactly `solver_verify_sidecars.py` + `test_commit13_sidecar_dryrun.py`; no `feature_extractor.py` regression.
- Reviewer claim Item D: "test_must66 still passes (≥3 buckets)." **Verified by builder local run.** Pre-commit was 7 buckets; post is 8 (folded_mw split adds capacity for primary). ≥3 trivially holds.

All three spot-checks hold.

---

## Item A — Bucket split logic correctness

**OK / HIGH confidence.** The new code at `_classify_shape:123-140`:
```python
fold_positions = {e[1] for e in action_history if e[2] == 'FOLD' and e[0] in {'flop', 'turn', 'river'}}
if villain_pos in fold_positions:
    return 'folded_mw_primary'
return 'folded_mw_offvillain'
```

Verified:
- Predicate matches PR #2 verdict §D fix-spec exactly
- Postflop-street filter `{'flop', 'turn', 'river'}` matches existing `fold_on_postflop` gate
- Edge cases handled correctly:
  - Multiple non-primary folds + primary live → `folded_mw_offvillain` ✓
  - Primary fold + another fold → `folded_mw_primary` (presence of second fold doesn't change primary attribution) ✓
  - Primary-only fold → `folded_mw_primary` ✓
- Branch only entered when `is_mw=True` (≥3 distinct positions); preserves prior semantics

## Item B — `_SHAPE_PATTERNS` retirement of `folded_mw`

**OK / HIGH confidence.** Old label removed, two new labels added with descriptive descriptions accurately distinguishing true sentinel from HU-after-fold. Reviewer grepped the entire `river-rats-core/` tree: no production code branches on the literal `'folded_mw'` outside the test asserting its retirement. Bucket consumed only by `_stratify` (label-agnostic dict-keying) and `solver_verify_sidecars.main` diagnostic print loop (uses `dict(_SHAPE_PATTERNS).get(shape, ...)`, works equally with new labels).

**NIT (cosmetic, non-blocking):** stale doc comment in `_reference_action_history_sidecar.py:192` still references `folded_mw → folded HU`. Doesn't affect behavior; clean up incidentally in a future commit.

## Item C — Test coverage

**OK / HIGH confidence.** All 3 new tests verified by mental walkthrough:
1. **FB-21 → `folded_mw_offvillain`:** positions={CO,BTN,BB}, fold=`('turn','BTN','FOLD')`, villain_pos=CO → `folded_mw_offvillain` ✓
2. **Synthetic primary-fold AH → `folded_mw_primary`:** positions={CO,BTN,BB}, fold=`('flop','BB','FOLD')`, villain_pos=BB → `folded_mw_primary` ✓
3. **Legacy retirement:** runtime corpus iteration + `_SHAPE_PATTERNS` static-membership check (double gate)

**NIT (cosmetic, non-blocking):** synthetic primary-fold AH in test #2 sequences `('flop','BB','FOLD')` BEFORE `('flop','CO','BET')`, which is unrealistic postflop ordering (BB normally acts after CO when CO opened). Classifier is order-insensitive within a street so the test still validates correctly, but a more realistic AH (CO-bet → BTN-call → BB-fold) would future-proof.

## Item D — Existing tests not broken

**OK / HIGH confidence.** Reviewer enumerated the test suite touching the classifier:
- `test_must66_stratification_covers_multiple_shapes` (asserts ≥3) — still passes (8 buckets > 3)
- `test_commit13_2_5_hu_donk_x_bet_bucket_covered` (SYN-F7 → `hu_donk_x_bet`) — unrelated branch
- `test_commit13_2_6_classifier_position_aware_donk` — unrelated (no postflop FOLD)
- `test_must54_solver_verify_stub_exits_0` — diagnostic script run; no label assertion
- `test_commit14_finding_b.py` (4 tests) — unrelated (Finding B is in `feature_extractor.py`)

PR description's 16/16 PASS claim confirmed by static analysis: no test asserts on literal `'folded_mw'` outside the new test #3 (which expects retirement).

## Item E — Chain-narrowing semantics unchanged

**OK / HIGH confidence.** Diff touches only `tests/solver_verify_sidecars.py` (a stratification telemetry utility, NOT production) + its test file. No touches to `range_narrowing.py`, `feature_extractor.py`, or any production module. Production chain-narrowing (`narrow_by_action_history`) still filters by `villain_pos` at line 947 — verified directly. PR description's "telemetry-only" claim is accurate.

## Item F — Stale-tree recovery integrity

**OK / HIGH confidence.** `git show --stat d090743` shows ONLY 2 files: `solver_verify_sidecars.py` and `test_commit13_sidecar_dryrun.py`. No `feature_extractor.py` deletion or stray changes. **Recovery was clean.** Builder restored `feature_extractor.py` from HEAD before committing; commit-14's Finding B changes remain intact on master per the cross-reference `test_commit14_finding_b.py PASS` evidence in PR description.

## Item G — Scope / no-creep

**OK / HIGH confidence.** Exactly 2 files changed (`+118 / -14`). Scope matches `BUILDER_COMMIT15_SCOPE_2026-04-26.md` declared boundaries (deferred items not present in diff: `delayed_probe`, `hu_donk_x_bet` rename, `mw_per_villain` distribution, v2.4 blockers).

---

## VERDICT

**APPROVE**

**Rationale:** The folded_mw split is a faithful, minimal, telemetry-only implementation of the PR #2 verdict §D fix-spec. Logic is correct (verified by walking the classifier with FB-21 and the synthetic primary-fold case), tests are well-targeted (runtime routing + static label retirement double-gate), no production paths are touched, no existing tests are at risk, and stale-tree recovery is provably clean (only 2 files in diff, both in tests/).

**Required fixes:** None.

**Blockers:** None.

**Stale-tree recovery assessment:** **CLEAN.** `git show --stat d090743` confirms exactly 2 files modified; no stray `feature_extractor.py` deletion or unrelated file present. Commit-14 Finding B intact on master.

**NIT-level observations (informational, optional follow-up):**

1. **Stale doc comment in `_reference_action_history_sidecar.py:192`** still references `folded_mw → folded HU`. Cosmetic; clean up incidentally in commit 16 or later wrap.
2. **Synthetic primary-fold AH in test #2** sequences `('flop','BB','FOLD')` before CO bets, which is unrealistic postflop ordering. Test passes because classifier is order-insensitive within a street; future-proofing would reorder to `CO-bet → BTN-call → BB-fold`.

Both NITs are non-blocking and can fold into commit 16 wrap-cleanup if desired.

**Greenlight commit 16:** Yes, conditional on orchestrator merge.

---

## Action

**Builder:**
1. Post comment on PR #8 referencing this verdict.
2. Run checkpoint #3 (post-verdict-comment) per the orchestrator's STOP-extension directive — UNKNOWN settle to CLEAN per protocol clarification.
3. Stand by for orchestrator merge.

**Orchestrator:**
1. Read this verdict.
2. Run protocol-compliance check.
3. Merge PR #8 with `gh pr merge 8 --merge --delete-branch`.
4. After merge: builder unblocked to start commit 16.

**Owner:** wake to find merged commit 14 + commit 15 + commit-16-ready state.

## Reference

- PR #8: https://github.com/beytell1-sketch/river-rats-v2/pull/8
- Scope doc: `review/comms/BUILDER_COMMIT15_SCOPE_2026-04-26.md` (`23d24d0`)
- Original fix-spec: `review/comms/GTO_REVIEW_VERDICT_PR_2_2026-04-25.md` §D
- Rollback tag: `stage3.5-pre-commit-15` at master HEAD before commit 15 was authored
- gto-expert persona spec: `~/river-rats-v2/.claude/agents/gto-expert.md`
- Restart protocol: `review/comms/BUILDER_RESTART_PROTOCOL_2026-04-25.md`
