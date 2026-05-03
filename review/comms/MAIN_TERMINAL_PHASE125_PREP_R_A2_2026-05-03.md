---
date: 2026-05-03
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5-prep R-A2 — 5 sources + 15 test assertions
status: DIRECTIVE — supersedes PR #115 (R-A)
---

# Phase 12.5-prep — R-A2

PR #116 inventory adopted. 5 source surfaces extend to 59. `feature_extractor.py` already at 59 (no change). `coaching/sizing_oracle.py` stays at 45 (different feature surface, not coupled by tests to the 59 contract). 1 pre-existing test failure carved out.

---

## LEAD-PROGRAMMER

Branch: `programmer/phase125-prep-r-a2-2026-05-03`

### Source files — extend to 59 (5)

Append in this exact order to each `FEATURE_COLUMNS`:

```
"nut_flush_block",
"flush_draw_block_pct",
"straight_draw_block_pct",
"nut_made_block_pct",
```

Files:

1. `river-rats-core/gto_model.py:33-62` (+ comment line 64: `# 55` → `# 59`)
2. `river-rats-core/coaching/gto_model.py:33-62` (+ comment line 64: `# 55` → `# 59`)
3. `river-rats-core/sizing_oracle.py:~120-123` (+ comment `# 55` → `# 59` if present)
4. `river-rats-core/train_model.py:131-160`
5. `river-rats-core/train_sizing_model.py:53+` (+ comment `# 55` → `# 59` if present)

### Source files — DO NOT touch

- `river-rats-core/feature_extractor.py` — already at 59 per `feature_extractor.py:1611`
- `river-rats-core/coaching/sizing_oracle.py` — at 45 features; different surface; not coupled to the 59 contract

### Test files — update assertions (5 files, 15 total)

12 from PR #115 R-A:

- `test_attention_experiments.py:65` — `== 55` → `== 59`
- `test_board_adjusted_hrp.py:84, 91` — `== 55` → `== 59`
- `test_new_features.py:305, 313` — `== 55` → `== 59`
- `test_multiway_features.py:36, 46, 52, 55, 62, 63` — `== 55` → `== 59`
- `test_sizing_oracle.py:171` — `== 55` → `== 59`

3 newly identified by PR #116:

- `test_attention_experiments.py:97` — `n_tagged == 53` → `== 57` (read `assemble_pilot_data.py` attention-tagger before changing to confirm the +4 increment)
- `test_attention_experiments.py:222` — `(20, 55)` → `(20, 59)`
- `test_sizing_oracle.py::test_output_shape` (line TBD — read before edit) — `== 55` → `== 59`

For `test_multiway_features.py:46-50` index-position checks at 52/53/54 (existing v9 features): leave unchanged.

### New test file

`river-rats-core/tests/test_feature_columns_v24_p1.py` per PR #113 spec (count + N_FEATURES + 4 blocker membership assertions).

### Pre-existing failure carve-out

`test_attention_experiments.py::test_assemble_produces_correct_files` fails on bare master (`FileNotFoundError: /tmp/pilot_situations.json`). **Not a regression from this migration.** Do not patch around it. Note in PR body that it remains failing post-patch for the documented reason.

### Verify before PR

- All 5 patched source `FEATURE_COLUMNS` tuples have `len == 59`, last 4 entries are the blockers
- `pytest river-rats-core/tests/` — 0 NEW failures vs master baseline (`test_assemble_produces_correct_files` carve-out aside)

### Stop conditions

- Any source tuple in the 5 wasn't 55 / last entry wasn't `board_adjusted_hrp` → STOP
- Any test still fails post-patch other than the carved-out `test_assemble_produces_correct_files` → STOP
- Anything outside the 11 listed files (5 source + 5 test + 1 new test) needs editing → STOP

PR title: `Builder Phase 12.5-prep R-A2: FEATURE_COLUMNS 55→59 (5 surfaces)`

PR body: diff stat, pytest counts (pre-patch master baseline + post-patch), source surfaces + tuple lengths, carve-out acknowledged.

---

## QC

Pre-merge audit. Three checks:

1. **Diff scope** — only the 11 listed files. Nothing else.
2. **Cross-tuple equality** — all 5 patched source tuples have identical last 4 entries (the 4 blocker names in the directed order). Plus `feature_extractor.py` already-at-59 last 4 entries match.
3. **Test assertions** — 15 listed assertion updates verified line-by-line. `test_assemble_produces_correct_files` carve-out is documented in PR body.

Post `REVIEW_QC_PHASE125_PREP_R_A2_*.md`. APPROVE or HOLD.

---

## After merge

Orchestrator dispatches 12.5C architect blueprint.

## References

- PR #116 (R-A BLOCKED inventory) — master `ddfc6a2`
- PR #115 (R-A directive, superseded) — master `17d0efb`
- PR #114 (PR #113 BLOCKED) — master `9f5c22a`
- PR #110 (ml-architect spec) — master `291af80`
