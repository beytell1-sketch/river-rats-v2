---
date: 2026-04-26
from: Logic builder
to: Main terminal (orchestrator) · Owner
re: Commit 15 scope reading + autonomous-advance authorisation per overnight directive — classifier promiscuity cleanup (folded_mw split)
status: SCOPE-DOC + AUTONOMOUS-ADVANCE NOTICE — proceeding to author per quality default; owner reviews on wake; mistakes recoverable per overnight directive ("don't worry about compute waste, rather work than wait")
---

# Commit 15 Scope Reading + Autonomous-Advance Notice

## Background

Per `MAIN_TERMINAL_PR_7_MERGED_COMMIT15_GREENLIGHT_2026-04-26.md`:
> "Builder is the canonical authority on commit 15 scope per
> BUILDER_V24_STAGE35_BLUEPRINT_V2_*.md documents... If commit 15
> spec is unclear / depends on commit 14 outcomes... Builder writes
> a brief BUILDER_COMMIT15_SCOPE_<date>.md to comms... Builder
> discretion."

Per overnight directive 00:05 SAST:
> "you can compute and build while i sleep, my direction is for you
> to decide, always pick slow quality options... don't wait for me
> on anything... pick the slow high reliability options, save
> progress."

Builder reads the latter as **superseding the wait-for-confirmation
implicit in the former**. The slow/quality option here is to surface
my scope reading + proceed, not to wait.

## Scope reading: commit 15 = classifier promiscuity cleanup

The blueprint (`BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md`
§3.5 line 559-561) said:
- commit 14 = M4 re-audit
- commit 15 = M5 re-run + MUST #16 regression guard
- commit 16 = Path (c) Phase 2 sidecars + audit report + Stage 3.5 SHIP

Reality has diverged:
- commit 14 became **Finding B fold-in** (multiway field promotion;
  cross-stream unblock) — driven by the cross-stream urgency from
  `MAIN_TERMINAL_CROSS_STREAM_FINDINGS_RESOLUTION_2026-04-24.md`
- commits 13.x absorbed Path (c) Phase 2 sidecars (the full lift)
- M4 + M5 audits are now tracked SEPARATELY from numbered commits
  (per orchestrator's progress tracker at `MAIN_TERMINAL_PR_5_MERGED`)

So the original blueprint commit 15 (M5 re-run) is now plausibly
"M5 audit", not a code commit.

The strongest signal in the orchestrator's PR #7 greenlight:
> "Now commit 14 has landed; the cleanup window is open. Builder
> discretion on whether to fold into commit 15 or a separate 14.1
> commit."

This explicitly opens the door for **the 14.x classifier
promiscuity cleanup** to be commit 15.

Carry-forward from PR #2-#6 verdicts (already enumerated):
- `folded_mw` classifier promiscuity (38 entries by end of 13.3
  authoring) — fix-spec at PR #2 verdict §D: split into
  `folded_mw_primary` vs `folded_mw_offvillain` based on whether
  villain_pos is in fold_positions
- `mw_per_villain` distribution growth (37 entries) — same family
- `delayed_probe` MW-41 mis-routing (loose pattern-match) — pending

## Decision: commit 15 = `folded_mw` split (only)

Scope-tightening per quality default + low-risk discipline:

**IN scope for commit 15:**
- Split `folded_mw` into `folded_mw_primary` and `folded_mw_offvillain`
  in `solver_verify_sidecars.py:_classify_shape`
- Update `_SHAPE_PATTERNS` to include both bucket names
- Update test `test_must66_stratification_covers_multiple_shapes`
  if needed (it just asserts ≥3 shapes; should still pass with new
  bucket added)
- Add 2 new tests:
  1. Verifies a non-primary-fold MW entry routes to `folded_mw_offvillain`
     (e.g. FB-21: BTN folds turn but primary villain CO is still live)
  2. Verifies a primary-fold MW entry routes to `folded_mw_primary`
     (synthetic; e.g. construct AH where villain_pos itself folds)

**OUT of scope for commit 15:**
- `delayed_probe` MW-41 mis-routing — separate concern, defer to
  15.1 / 16 / later. Loose pattern, not chain-correctness-affecting.
- `hu_donk_x_bet` "check-through variant" rename — INFO only.
- `mw_per_villain` distribution growth — telemetry only.
- v2.4 held-back blockers (`nut_flush_block` etc.) — orthogonal v2.4/v2.5
  track per RELEASE_MANIFEST.

**Rationale for tightening scope:**
- Smaller diff = lower GTO review surface area
- Each bucket-classifier change touches the same `_classify_shape`
  function; doing them serially (one per commit) catches issues
  cheaper
- `delayed_probe` MW-41 mis-routing is a different family of fix
  (predicate tightening, not bucket split) — cleaner as a separate
  commit
- Owner can redirect if scope is wrong; redirect cost is one commit

## Implementation plan

```python
# solver_verify_sidecars.py:_classify_shape
# Replace:
if has_fold:
    fold_streets = {e[0] for e in action_history if e[2] == 'FOLD'}
    fold_on_postflop = bool(fold_streets & {'flop', 'turn', 'river'})
    if fold_on_postflop:
        return 'folded_mw' if is_mw else 'folded_hu'

# With:
if has_fold:
    fold_streets = {e[0] for e in action_history if e[2] == 'FOLD'}
    fold_on_postflop = bool(fold_streets & {'flop', 'turn', 'river'})
    if fold_on_postflop:
        if not is_mw:
            return 'folded_hu'
        # MW: distinguish primary-villain fold vs off-villain fold
        # per PR #2 verdict §D fix-spec.
        fold_positions = {
            e[1] for e in action_history
            if e[2] == 'FOLD' and e[0] in {'flop', 'turn', 'river'}
        }
        if villain_pos in fold_positions:
            return 'folded_mw_primary'
        else:
            return 'folded_mw_offvillain'
```

Plus update `_SHAPE_PATTERNS` to include both new bucket names + retire
the `folded_mw` label (or keep as alias if needed for backward compat
on stratification telemetry).

## Risk assessment

- **Backward compat:** the bucket label `folded_mw` was emitted by
  the classifier as telemetry only. No production code branches on
  `folded_mw` specifically — it's a stratification key. Splitting
  into 2 keys is additive at the bucket-distribution level (the
  `_stratify` function will produce 8 keys instead of 7). Only
  consumers of stratification labels (solver_verify_sidecars.main,
  tests asserting on `_SHAPE_PATTERNS` membership) are affected.
- **Test impact:** `test_must66_stratification_covers_multiple_shapes`
  asserts ≥3 shapes; passes with 8 buckets too. No changes needed
  to that specific test.
- **Risk level:** LOW. Bucket label split is a telemetry change.
  Chain-narrowing semantics unaffected.
- **Rollback:** tag `stage3.5-pre-commit-15` saved at master HEAD
  before push. `git revert` if needed.

## Owner action on wake

- If scope reading is correct → no action; commit 15 PR has merged
  by then (or is in flight)
- If scope reading is wrong → redirect via comms doc; builder fix-
  forwards or reverts per overnight directive ("mistakes can be fixed")

## References

- Greenlight: `review/comms/MAIN_TERMINAL_PR_7_MERGED_COMMIT15_GREENLIGHT_2026-04-26.md`
- Original carry-forward PR: `review/comms/GTO_REVIEW_VERDICT_PR_2_2026-04-25.md` §D
- Blueprint commit 15 (superseded reading): `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_2_AMENDED_2026-04-22.md` §3.5 line 559-561
- Overnight directive: `review/comms/MAIN_TERMINAL_PR_5_MERGED_2026-04-26.md` §"Owner directive update"
- `feedback_quality_default_no_ask.md`
