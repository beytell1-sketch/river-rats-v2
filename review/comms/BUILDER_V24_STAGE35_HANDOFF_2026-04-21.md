---
date: 2026-04-21
from: Builder
to: Reviewer / Owner / next-session builder
re: Stage 3.5 handoff — where I actually stopped. Stage 3.5 is NOT shipped.
status: HANDOFF — 5 MUSTs outstanding from reconciliation
---

# Stage 3.5 Handoff — Honest State

Owner asked for a commit-all + status for the reviewer. Doing both.
Most important line first: **Stage 3.5 is NOT complete.** My earlier
"STAGE 3.5 COMPLETE" report at `e329ea3` was premature. Reviewer's
multi-agent reconciliation at `0276653` surfaced 5 MUSTs I have not
addressed. This doc is the honest pickup for the next cycle.

## What IS committed

All landed in `e329ea3` (my last builder commit) — code is real,
tests pass, M4/M5 gates PASS, but Stage 3.5 is not *ship-gated*:

- `river-rats-core/range_narrowing.py` — M1 tables + M2 chain
  walker + 3 safety rails + 2 new narrow functions
- `river-rats-core/game_state_bridge.py` — flatten
  `game.street_actions` → `_action_history` on hand payload
- `river-rats-core/feature_extractor.py::classify_villain_range` —
  accept `action_history`; chain-narrow prior streets; return
  `_villain_range_chain_steps` + `_villain_range_chain_truncated`
  metadata
- `river-rats-core/tests/test_range_narrowing_stage35.py` — 16
  unit tests (all pass)
- `review/run_stage35_backfill_audit.py` — M4 distribution-shift
  audit runner (579 rows; 0 isolation violations; 455/455
  multi-street chain fires)
- `review/run_v231_anchor_recheck_stage35.py` — M5 pre-retrain
  diagnostic (3/3 β-panel anchors BET restored on v2.3.1 model)
- Stage 3.5 reports at `BUILDER_V24_STAGE35_*_2026-04-20.md`

## What I DID NOT do (the 5 MUSTs)

The reviewer's multi-agent reconciliation (commit `0276653`) ran 6
parallel agents after my Stage 3.5 report and found real gaps. I
stopped before addressing them.

### CRITICAL #1 — Blocker features bypass the chain

`river-rats-core/feature_extractor.py` Step 12 (`flush_block_pct`)
and Step 17 (the 4 new v2.4 P1 blocker features) recompute
`_s12_v_range` by calling `get_villain_range(...)` directly, then
applying only `narrow_to_betting_range` when `facing_bet`. They
**never** call `narrow_by_action_history`.

My Stage 3.5 report claimed "all 10 features inherit" — this was
false. Composition features (`villain_top_pair_plus_pct` etc.) go
through `classify_villain_range` and DO inherit the chain. The
**5 blocker features** (`flush_block_pct` + 4 new) run an
independent un-narrowed range-build path.

**Where to fix:** `feature_extractor.py:1648-1662, 1720+`. Step 12
+ Step 17 must consume the range that `classify_villain_range`
just narrowed, not recompute from scratch.

**Impact if not fixed:** teaching displays chain-narrowed
composition alongside un-narrowed block percentages. Oracle reads
two contradictory views of villain's range. SHAP-vs-action
contradiction class.

### CRITICAL #2 — Silent distribution split when _action_history missing

`_action_history` is populated by `game_state_bridge.py` (live/
factory runs). But gauntlet scripts, synthetic fixtures,
`extract_features_parallel.py`, `extract_incremental.py` may not
populate it — in which case feature extraction silently falls
back to pre-Stage-3.5 behavior.

**This is the exact failure mode that broke v2.3.2.** If Stage 4
re-label runs with mixed presence, training data gets a chained
distribution for some rows + non-chained for others. Model learns
the mixture.

**Where to fix:**
- `feature_extractor.py::extract_range_composition` — emit loud
  warning (or raise) when `action_history` is None + training
  pipeline is active
- Audit `extract_features_parallel.py`, `extract_incremental.py`,
  all gauntlet scripts — confirm action_history propagation
- Add `_action_history_present: bool` flag to training CSV
  schema for post-hoc audit

### HIGH #3 — Check-raise sign flip

`narrow_by_action_history` applies CHECK × BET sequentially on the
same street for check-raise lines. This produces inverted
composition — mediums UP, nuts DOWN — because the CHECK table
says "medium checks 55% of time" and the BET table says "medium
bets 30% of time" and multiplying them further doesn't capture
that a check-raise is a concentrated-value action.

Check-raise range IRL is 60-80% nuts. Our chain produces
medium-heavy. Wrong.

**Reviewer's call:** option (b) — treat CHECK followed by
BET/RAISE on same street as the aggressive action alone. Skip
the CHECK narrowing when paired with a raise on same street.

**Where to fix:** inside `narrow_by_action_history` action loop —
detect double-action-per-street with CHECK → BET/RAISE and apply
only the bet/raise narrow.

### HIGH #4 — FOLD re-fetch silent bug

`feature_extractor.py:1186` — when chain returns empty range
(villain folded), my caller silently re-fetches `get_villain_range()`
un-narrowed:

```python
if not v_range:
    v_range = get_villain_range(hero_pos, villain_pos, opener_pos=...)
```

Features then compute villain composition against the preflop
range for a folded villain. Wrong.

**Fix:** replace re-fetch with `meta['villain_folded'] = True`
sentinel; feature extractor skips composition features (or NaN-
flags them) for folded villains.

### HIGH #5 — `surviving_weight` is hand-count not probability-mass

In `narrow_by_action_history`:
```python
'surviving_weight': float(len(current_range)) / max(1, len(full_range))
```

This is hand COUNT, not probability MASS. A range of 3 hands at
freq 0.33 passes the 5% floor but is semantically collapsed.

**Fix:** track un-normalized weight sum through each narrow step;
compute true surviving proportion of original probability mass.

## Architecture MUSTs (also from reconciliation)

- **Unit test file with 81 canonical cases** — corpus delivered by
  the reconciliation at
  `review/tests/range_narrowing_test_corpus_2026-04-20.yaml`
  (committed in `0276653`). My current 16-test file needs to be
  extended or replaced to consume the 81-case YAML corpus.
- **Observability hooks** — chain_steps, surviving_weight,
  truncated already in the `_meta_` fields; confirm they flow
  through to training CSV / audit paths.

## One conflict resolved (same-street pre-hero)

Reconciliation confirmed **EXCLUDE same-street pre-hero actions**
for v2.4 (my spec was correct). GTO theorist wanted INCLUDE;
red-team verified that EXCLUDE preserves the 4 flop anchor
stability needed to validate Stage 3.5 in isolation. v2.5 may
revisit once bet-sizing conditioning lands.

## Revised ship sequence (post-reconciliation)

Per `0276653`:

1. Fix 5 MUSTs (CRITICAL #1, #2, HIGH #3, #4, #5)
2. Unit test file lands (81-case corpus, not my 16-case file)
3. Observability hooks audit
4. Anchor regression run
5. Retroactive audit on v2.3.1 training CSV (redo — current audit
   didn't exercise the blocker-feature bypass)
6. If anchors pass and audit is clean → Stage 3.5 ships
7. **Then** Stage 4 re-label opens

## What I fixed in working state this cycle

- Deleted `review/v231_selfplay_raw.json` (replaced by v232 at
  `db222d3`; left as unstaged delete in working tree)
- Untracked `review/research/BLOCKER_FEATURE_EXPANSION.md` (owner
  research from 2026-04-18, 197 lines, never committed)

Both committed in this cycle.

## Green/amber lights

What IS solid (from my e329ea3 work):
- `narrow_by_action_history` core logic with bet/check/call/fold
- M4 isolation check on composition features (flop-only 0/124)
- M5 three β-panel anchors predict BET on v2.3.1 without retrain
- 16 unit tests for the chain mechanics

What is NOT solid:
- The 5 MUSTs above
- My claim that "all 10 features inherit" (only 6 do)
- M4/M5 gates did not exercise the 5 blocker features — those
  ran on the un-narrowed bypass path and the audit didn't catch
  it

## Entry points for next builder

1. Read `review/comms/MAIN_TERMINAL_MULTIAGENT_RECONCILIATION_2026-04-20.md`
2. Read this handoff
3. Patch CRITICAL #1 first (single file, localized fix, unblocks
   meaningful re-audit)
4. Patch CRITICAL #2 (add warning + audit training pipeline
   plumbing)
5. Patch HIGH #3, #4, #5
6. Load 81-case test corpus; run against patched code
7. Re-run M4 audit (will now exercise blocker features correctly)
8. Re-run M5 diagnostic (confirm still 3/3 after fixes)
9. If all pass → THEN claim Stage 3.5 complete

## For reviewer

My Stage 3.5 report at `e329ea3` was premature. The reconciliation
you ran was correct to escalate, correct on the findings, and
correct to refuse ship-as-is. I did not loop back to apply the
MUSTs before stopping — that's a builder-discipline miss worth
logging.

Standing by.
