---
date: 2026-04-26
from: Logic builder
to: Main terminal (orchestrator) · Owner
re: Commit 16 scope reading + autonomous-advance per overnight directive — delayed_probe HU-only predicate tightening + 2 PR #8 cosmetic NITs
status: SCOPE-DOC + AUTONOMOUS-ADVANCE NOTICE — proceeding to author per quality default; rollback tag stage3.5-pre-commit-16 saved at master `03b89e6`
---

# Commit 16 Scope Reading + Autonomous-Advance Notice

## Background

Per `MAIN_TERMINAL_PR_8_MERGED_COMMIT16_GREENLIGHT_2026-04-26.md`:
> "Builder discretion. Autonomous-advance per owner directive."
> "This is the FINAL substantive Stage 3.5 commit before the M4/M5 audits."

Per overnight directive 00:05 SAST 2026-04-26:
> "always pick slow quality options... pick the slow high reliability options, save progress."

## Investigation summary

I ran `python3 river-rats-core/tests/solver_verify_sidecars.py` against
the post-PR-8 master corpus (86 entries, 7 buckets). Three observations
informed scope choice:

1. **`delayed_probe` bucket is mis-routed.** All 4 entries (MW-41,
   FB-18, FB-19, SYN-F6_MW_all_live) are MULTIWAY (3 positions), but
   the bucket label is "HU delayed-probe large turn bet". The current
   predicate is too loose — it captures any flop-CHECK + turn-BET
   shape regardless of `is_mw`. The synthetic `SYN-F6_MW_all_live`
   was authored as "MW all-live" (per its name) and is clearly NOT
   a delayed-probe — its presence in this bucket is the strongest
   evidence of the bucket-name-vs-content mismatch.

2. **`folded_mw_primary` bucket is empty.** Commit 15 split
   `folded_mw` into `_primary` + `_offvillain`, but the corpus has
   ZERO primary-villain-folded entries — all 38 went to
   `_offvillain`. The split was structurally correct but the
   diagnostic value depends on future entries populating
   `_primary`. NOT a regression; cleanly handled by the new test
   `test_commit15_folded_mw_split_primary_routes_correctly`
   (synthetic AH).

3. **Two PR #8 cosmetic NITs unchanged on master:**
   - NIT #1: stale doc comment in `_reference_action_history_sidecar.py:192`
     references `folded_mw → folded HU` (post-15 it should reference
     `folded_mw_offvillain → folded HU` or be reworded entirely).
   - NIT #2: synthetic primary-fold AH in
     `test_commit15_folded_mw_split_primary_routes_correctly` orders
     `('flop','BB','FOLD')` BEFORE `('flop','CO','BET')` (unrealistic
     postflop sequencing — BB acts after CO when CO opens).

## Scope decision: commit 16 = delayed_probe HU-only predicate tightening + 2 cosmetic NITs

**IN scope:**

1. **`solver_verify_sidecars.py` — tighten `delayed_probe` predicate:**
   add `and not is_mw` gate. The 4 mis-routed MW entries
   (MW-41, FB-18, FB-19, SYN-F6_MW_all_live) will fall through to
   `mw_per_villain` (more truthful — they ARE multiway per-villain
   chains). `delayed_probe` bucket may have 0 entries until a real
   HU delayed-probe lands in Stage 6 corpus.

2. **`_reference_action_history_sidecar.py:192` — NIT #1 fix:**
   reword the stale doc comment.

3. **`test_commit13_sidecar_dryrun.py:326-333` — NIT #2 fix:**
   reorder synthetic AH to realistic CO-bet → BTN-call → BB-fold
   sequence.

4. **3 new tests:**
   - `test_commit16_delayed_probe_hu_only_predicate` — synthetic HU
     delayed-probe AH routes to `delayed_probe`.
   - `test_commit16_delayed_probe_mw_routes_to_mw_per_villain` —
     verify MW-41, FB-18, FB-19, SYN-F6_MW_all_live now route to
     `mw_per_villain` (not delayed_probe).
   - `test_commit16_delayed_probe_bucket_truthfulness` — for every
     entry currently in delayed_probe bucket on the live corpus,
     assert it satisfies `is_mw=False`.

**OUT of scope:**

- `mw_per_villain` distribution growth (37→41 entries post-fix)
  — telemetry-only stratification; no internal sub-split spec
  exists yet, would require GTO-judgment to design. Defer to v2.5
  if needed.
- `hu_donk_x_bet` "check-through variant" rename — INFO only.
- Any new corpus authoring — ship gate per orchestrator
  (commit 16 = LAST substantive code commit before M4/M5).
- Any `feature_extractor.py` change — NOT touching production
  code paths; this is telemetry-only cleanup.

## Risk assessment

- **Backward compat:** the bucket label changes are additive at the
  stratification level. `_SHAPE_PATTERNS` retains `delayed_probe`
  (just with tightened predicate). No production consumer of the
  bucket labels exists outside `solver_verify_sidecars.main` +
  test files (verified by grep on prior commits).
- **MUST #66 risk:** test asserts ≥3 shapes; post-fix bucket count
  is 6 (one less than 7 if `delayed_probe` empties out, but well
  above 3). Trivially holds.
- **Chain-narrowing semantics:** UNAFFECTED. Only telemetry
  (stratification) changes.
- **Risk level:** LOW. Predicate-tightening + 2 doc/test cosmetic
  fixes. Same family as commit 15.
- **Rollback:** tag `stage3.5-pre-commit-16` saved at master
  `03b89e6`. `git revert` if needed.

## Implementation plan

```python
# solver_verify_sidecars.py:_classify_shape
# Replace:
if (flop_check_count >= 1 and turn_present
        and any(e[0] == 'turn' and e[2] == 'BET' for e in action_history)):
    return 'delayed_probe'

# With:
# Commit 16: tighten predicate to HU-only per bucket label
# "HU delayed-probe large turn bet". Prior loose predicate
# mis-routed 4 multiway entries (MW-41, FB-18, FB-19,
# SYN-F6_MW_all_live) into delayed_probe; they now fall through
# to mw_per_villain (correct).
if (flop_check_count >= 1 and turn_present
        and not is_mw
        and any(e[0] == 'turn' and e[2] == 'BET' for e in action_history)):
    return 'delayed_probe'
```

## Carry-forward / explicit deferrals

- `mw_per_villain` 37→41 distribution (post-commit-16 it grows;
  per-entry sub-classification deferred to v2.5)
- `hu_donk_x_bet` rename (INFO-only)
- Any further `_classify_shape` refinements (Stage 6 / live solver)

## Owner action on wake

- If scope reading is correct → no action; commit 16 PR has merged
  by then (or is in flight)
- If scope reading is wrong → redirect via comms doc; builder
  fix-forwards or reverts per overnight directive

## References

- Greenlight: `review/comms/MAIN_TERMINAL_PR_8_MERGED_COMMIT16_GREENLIGHT_2026-04-26.md`
- PR #8 verdict NITs: `review/comms/GTO_REVIEW_VERDICT_PR_8_2026-04-26.md` §"NIT-level observations"
- Predecessor scope doc: `review/comms/BUILDER_COMMIT15_SCOPE_2026-04-26.md`
- Overnight directive: `review/comms/MAIN_TERMINAL_PR_5_MERGED_2026-04-26.md` §"Owner directive update"
- Rollback tag: `stage3.5-pre-commit-16` at `03b89e6`
- `feedback_quality_default_no_ask.md`
