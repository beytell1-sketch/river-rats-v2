---
date: 2026-04-22
from: Main terminal (orchestrator)
to: Builder · Owner
re: Commit 4 atomic merge (fdaa8f6) — parallel architect + red-team review; REJECT with fix-forward
status: REJECT — 3 CRITICAL ship-blockers from red-team; fix-forward commit required before commit 5
---

# Commit 4 Review — REJECT with fix-forward

Parallel architect + red-team review on commit 4 (fdaa8f6) per
ALL-CLEAR directive. Reviewers split:

- **Architect:** APPROVE_WITH_FIXES (issues are follow-up tickets)
- **Red-team:** REJECT (3 CRITICAL, 5 HIGH, 2 MEDIUM — ship-blockers)

Red-team findings take precedence. C1 breaks inference on folded-
villain hands; C2 re-introduces the silent-fallback anti-pattern
the project has been fighting since v2.3.2; C3 renders MUST #46's
cache architecturally dead weight.

## CRITICAL — must fix before commit 5

### C1 — `board_favour` NaN leaks outside allowlist

**Location:** `feature_extractor.py:1639`
**Bug:** When `_villain_folded` or `_villain_chain_overflowed` is True,
`tp_pct` becomes NaN at line 1613. Line 1639 computes:
```python
board_favour = round(0.30 - tp_pct, 4)  # NaN on folded/overflowed
```
`board_favour` is NOT in `gto_model._NAN_ALLOWLIST` (gto_model.py:229-233).
`GtoOracle.features_from_dict` raises ValueError on every folded-villain
hand at inference.

Commit message claims "board_favour stays 0 — hero-range-derived."
**Code contradicts.**

**Fix (builder picks one):**
- (a) Force `board_favour = 0.0` explicitly when `_villain_folded` or
  `_villain_chain_overflowed` is True (matches commit-msg claim)
- (b) Add `board_favour` to `gto_model._NAN_ALLOWLIST` alongside the
  4 composition + 4 blocker features

Orchestrator recommends (a) — cleaner semantics (board_favour is
hero-range-dependent only; NaN is inappropriate). Update test
`test_high4_folded_villain_sentinel` to assert `board_favour == 0.0`.

### C2 — Step 17 `except Exception: pass` silent zeroing

**Location:** `feature_extractor.py:2147-2154`
**Bug:** Step 17 blocker features wrap `compute_block_percentages` in
bare `except Exception:` that defaults the 3 continuous block_pcts
to 0.0 on raise. 0.0 is a real-signal value (hero blocks nothing)
— indistinguishable from "computation failed."

Same silent-fallback class as CRIT #2 / MUST #15. Introduced INSIDE
the CRIT #1 fix itself.

**Fix:** Replace bare except with typed handling:
```python
try:
    flush_draw_block_pct, straight_draw_block_pct, nut_made_block_pct = \
        compute_block_percentages(hero_cards, board_cards, villain_range)
except (ValueError, KeyError, TypeError) as e:
    # Unexpected — log and NaN-flag (MUST #10 pattern)
    import logging
    logging.getLogger(__name__).error(
        'MUST #10: compute_block_percentages failed for hand=%s: %s',
        features.get('_hand_id', '<unknown>'), e,
    )
    flush_draw_block_pct = float('nan')
    straight_draw_block_pct = float('nan')
    nut_made_block_pct = float('nan')
```

Or — simpler — remove the try/except entirely (let exceptions propagate;
this is a helper we control, not external input).

### C3 — MUST #46 cache architecturally orphaned

**Location:** `feature_extractor.py:1270-1294` (step1_through_5) +
`feature_extractor.py:1973-2026` (extract_all_features) +
`extract_range_composition` signature

**Bug:** `extract_range_composition` (runs 3rd in step1_through_5 at
line 2012) does NOT accept `cached_range`/`cached_meta` params. But
`extract_equity_features` + `extract_partition_features` (run 1st/2nd)
each independently invoke `_get_chain_narrowed_villain_range` without
cache.

Result in production: `narrow_by_action_history` runs 3-4x per multiway
hand. MUST #46's "cache contract fast-path" is dead weight.

`test_must63_cache_fast_path` only exercises the helper in isolation,
so tests pass — but the production path never exercises the cache.

**Fix (builder picks):**
- (a) Extend `extract_range_composition` signature to accept
  `cached_range`/`cached_meta`; run it FIRST in step1_through_5;
  equity + partition consume the cache. ORDER SHIFT: composition →
  equity → partition (not equity → partition → composition).
- (b) Cache via the feature-dict: `features['_villain_range_narrowed']`
  populated by composition; equity + partition read from features
  dict on subsequent calls. No explicit cache-params; implicit
  shared state via features dict.

Orchestrator recommends (b) — less invasive, single source of truth,
cache is the features dict itself (already the plan per MUST #26
pattern). Update `_get_chain_narrowed_villain_range` to check
`features.get('_villain_range_narrowed')` as the cache-fast-path;
populate on first compute.

## HIGH — fix before ship

### H1 — `MULTIWAY_CHAIN_MODE` unknown-value silent fallback

`feature_extractor.py:689`: Unknown env values (`"true"`, `"1"`,
`"yes"`, `"primary"`) silently fall through to `primary_only` branch.
No warning.

**Fix:** Whitelist-match `per_villain` | `primary_only`; on unknown,
log WARNING + default to `per_villain`. Or raise. Either, not silent
fall-through.

### H2 — `per_villain_ranges` silent-default on missing position

`feature_extractor.py:515, 1041`: `pv.get(primary, {})` and
`[pv_ranges.get(p, {}) for p in opponent_positions]` silently hand
empty dicts into `partition_range` / `_true_multiway_equity_mc`. A
helper bug that drops a position produces invisible "villain has no
hand" inflation.

**Fix:** Raise on missing-position. Missing `per_villain_ranges[pos]`
is a helper bug, not a legitimate runtime state.

### H3 — Benchmark script false-positive risk

`tests/benchmark_multiway_chain.py:43-51`: CSV rows are strings;
`_action_history` column appends raw string; `extract_all_features`
falls through `if not action_history:` → NON-CHAINED path. Gate
measures the wrong code.

Synthetic fallback hands miss `_hero_cards` / `_board_cards`; all
error out; NaN median; `NaN < 500` always False → FALLBACK branch
with misleading "NaN ms" output.

**Fix:** Parse `_action_history` from CSV (ast.literal_eval or JSON);
synthetic hands include `_hero_cards` + `_board_cards`; gate on error-
rate + explicit NaN-guard.

### H4 — Duplicate `opponent_positions` silently overwrites

`feature_extractor.py:760`: `per_villain_ranges[opp_pos] = opp_range`
without defensive uniqueness check.

**Fix:** `assert opp_pos not in per_villain_ranges, f'duplicate opp_pos {opp_pos!r}'`
at top of loop iteration.

### H5 — `primary_only` telemetry blind

Per MUST #52, fallback to `primary_only` mode should be detectable
in audit logs. Currently no distinguishing return field.

**Fix:** Add `meta['_equity_method'] = 'per_villain' | 'primary_only'`
to helper return. Playtest log + training CSV can filter by vintage.

## MEDIUM — non-blocking but track

### M1 — Test-MUST mapping gaps

11 tests named but #15/#28/#60/#46 lack dedicated named tests in
commit message. Bisection can't attribute #15/#28/#60 failures.

**Fix:** Add named test IDs for the 4 missing MUSTs. Can be new
tests or rename existing ones. Update commit message when fixes
land.

### M2 — MW-cache-consumed-by-HU-caller

`extract_equity_features:1055-1063` calls helper with `num_opponents=1`
while potentially passing cached_range from MW-populated cache. Paired-
assertion guards None+None; won't catch this specific cross-type case.

**Fix (if C3 (b) chosen):** N/A — cache lives in features dict, keyed
by num_opponents. If C3 (a) chosen: strengthen assertion to validate
cache-vs-request num_opponents consistency.

## Review path forward

Single **red-team re-check** after fix-forward commit — not full
5-panel re-dispatch. These are concrete code fixes, not architecture
work.

**Builder action (auto mode):**

1. Fix C1 (recommended option a)
2. Fix C2 (remove bare except or typed NaN-flag)
3. Fix C3 (recommended option b — cache via features dict)
4. Fix H1, H3, H4, H5 (H2 deferrable if scope grows too much)
5. Address M1 test mapping
6. Commit as 4.1 fix-forward ON TOP of fdaa8f6 (not amend — preserves
   review trail per project convention)
7. Push
8. Ping orchestrator for red-team re-check

If red-team re-check returns clean → architect read-only sign-off →
commit 5. If red-team surfaces new CRITICAL → another fix-forward;
expected: this is the final rework on commit 4.

## Also commit 5 waiting

Commit 5 = MUST #20 calibration_exam `_action_history` plumbing +
Path (c) sidecar authoring phase 1 (schema extension). Does not
start until commit 4 is clean.

## Pattern

Pattern recap: commit 1 clean-approve, commit 2 clean-approve, commit
3 clean-approve-with-minor-nits, commit 4 atomic-merge with 3 CRITICAL
fixes before proceeding. 11-MUST scope surfaced more attack surface
than 1-3 MUST commits. Expected. Fix-forward is proportional.

Other commits in the remaining 12 (5, 6, 7, 8, 9, 10, 11, 11A, 11B,
12, 13, 14, 15, 16) are smaller per-MUST scope; expected to clean-
approve faster than commit 4.

## Reports archived

Full architect + red-team reviews in orchestrator transcripts. Key
findings extracted above.

Go.
