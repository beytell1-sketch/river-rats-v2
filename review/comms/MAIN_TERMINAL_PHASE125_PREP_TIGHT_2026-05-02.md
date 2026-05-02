---
date: 2026-05-02
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream
re: Phase 12.5-prep — tight directive (supersedes #112 prose)
status: DIRECTIVE
---

# Phase 12.5-prep

Owner approved S-1 + S-2 on PR #111. Execute on git fetch.

---

## LEAD-PROGRAMMER

Branch: `programmer/phase125-prep-feature-columns-59-2026-05-02`

**Edit `river-rats-core/gto_model.py`:**

1. Append to `FEATURE_COLUMNS` tuple, in this exact order:
   ```
   "nut_flush_block",
   "flush_draw_block_pct",
   "straight_draw_block_pct",
   "nut_made_block_pct",
   ```
2. Line 64 comment: `# 55` → `# 59`.

**Add `river-rats-core/tests/test_feature_columns_v24_p1.py`:**

- assert `len(FEATURE_COLUMNS) == 59`
- assert `N_FEATURES == 59`
- assert all 4 blocker names are in `FEATURE_COLUMNS`
- Mirror import path of existing tests in that directory.

**Verify before opening PR:**

- `pytest river-rats-core/tests/` — no new failures vs master
- New test file passes
- No other files changed

**Stop conditions** (per CLAUDE.md §5 — do not improvise):

- Existing test fails after patch → STOP, report
- Anything other than `gto_model.py` + new test file needs editing → STOP, report

PR title: `Builder Phase 12.5-prep: FEATURE_COLUMNS 55→59`

---

## QC

Pre-merge audit on the PR when it opens. Two checks:

1. **Diff content** — 4 strings appended in exact order; `# 55` → `# 59`; new test file with 3 assertions; nothing else
2. **Diff scope** — only `gto_model.py` + new test file touched

Post `REVIEW_QC_PHASE125_PREP_*.md` with verdict APPROVE or HOLD (cite specific lines on HOLD). No ml-architect or gto-expert review on this PR.

---

## After merge

Orchestrator dispatches 12.5C architect blueprint for the new student trainer module.

## References

- PR #110 (ml-architect spec) — master `291af80`
- PR #111 (orchestrator review + owner approval) — master `88e5b38`
- PR #112 (verbose prose superseded by this) — master `9de0bc3`
