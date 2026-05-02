---
date: 2026-05-03
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5-prep AMENDED — R-A scope (4 source surfaces + 5 test files)
status: DIRECTIVE — supersedes PR #113 tight directive
---

# Phase 12.5-prep — AMENDED (R-A)

PR #114 blocked: 55-feature contract enforced at 4 source files + 5 test files. R-A picked: extend all 4 surfaces to 59 in one PR. No ml-architect re-dispatch — sizing_oracle currently shares the action-model feature surface (test_multiway_features.py:55-58 + test_sizing_oracle.py:175-176 enforce equality); no methodology reason to diverge.

---

## LEAD-PROGRAMMER

Branch: `programmer/phase125-prep-r-a-2026-05-03`

### Pre-flight (mandatory)

For each of the 4 source files, confirm current `FEATURE_COLUMNS` length is 55 AND the last entry is `"board_adjusted_hrp"`:

- `river-rats-core/gto_model.py` (lines 33–62)
- `river-rats-core/coaching/gto_model.py` (lines 33–62)
- `river-rats-core/feature_extractor.py` (line 1569+)
- `river-rats-core/sizing_oracle.py` (lines ~120–123)

If any tuple is not 55 or last entry doesn't match → **STOP, report**.

### Patch — source files (4)

Append these 4 strings to each `FEATURE_COLUMNS` tuple in this exact order:

```
"nut_flush_block",
"flush_draw_block_pct",
"straight_draw_block_pct",
"nut_made_block_pct",
```

Update the trailing `# 55` comment to `# 59` where it exists (`gto_model.py:64`, `coaching/gto_model.py:64`, `sizing_oracle.py:~123`).

### Patch — test files (5, 12 assertions total)

Update `55` → `59`:

- `test_attention_experiments.py:65`
- `test_board_adjusted_hrp.py:84, 91`
- `test_new_features.py:305, 313`
- `test_multiway_features.py:36, 46, 52, 55, 62, 63`
- `test_sizing_oracle.py:171`

For `test_multiway_features.py:46-50` (index-position checks at 52/53/54): verify these reference the existing v9 expansion features (not the new blockers). If they do, leave them alone. If they assert the tuple LENGTH at those positions, update to 56/57/58/59 for the new blockers. **Read the assertion before changing.**

### Patch — new test file (1)

`river-rats-core/tests/test_feature_columns_v24_p1.py` per PR #113 spec:

- `assert len(FEATURE_COLUMNS) == 59`
- `assert N_FEATURES == 59`
- `assert all 4 blocker names ⊂ FEATURE_COLUMNS`

### Verify before PR

- `pytest river-rats-core/tests/` — 0 new failures, all previously-passing tests still pass
- All 4 source `FEATURE_COLUMNS` tuples have `len == 59` and same last 4 entries

### Stop conditions

- Any source tuple wasn't 55 / last entry mismatch → STOP
- Any existing test still fails after all 4 sources + 12 assertions updated → STOP (means scope is still wider than R-A models)
- Any file outside the 9 listed (4 source + 5 test) needs editing → STOP

PR title: `Builder Phase 12.5-prep R-A: FEATURE_COLUMNS 55→59 contract-wide`

PR body: diff stat, pytest counts, list of all 4 source surfaces extended.

---

## QC

Pre-merge audit. Three checks:

1. **Diff scope** — only the 9 listed files (4 source + 5 test) + 1 new test file are touched. Nothing else.
2. **Cross-tuple equality** — all 4 source `FEATURE_COLUMNS` tuples have identical content post-patch (the 4 blockers in identical order at the end).
3. **Test assertions** — every `== 55` in the 5 test files updated to `== 59`; index-position assertions (if any) sensibly updated.

Post `REVIEW_QC_PHASE125_PREP_R_A_*.md`. APPROVE or HOLD with cited lines.

---

## After merge

Orchestrator dispatches 12.5C architect blueprint for the new student trainer module.

## References

- PR #114 (BLOCKED inventory) — master `9f5c22a`
- PR #113 (superseded tight directive) — master `f85a9ea`
- PR #110 (ml-architect spec) — master `291af80`
- PR #111 (orchestrator review + owner approval) — master `88e5b38`
