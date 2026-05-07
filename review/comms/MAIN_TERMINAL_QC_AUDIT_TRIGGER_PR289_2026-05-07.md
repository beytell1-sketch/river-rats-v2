---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #289 — 12.5K-C-D Opus tier-up (20/20 Sonnet-Opus match; 100% across 4 axes; Path A validated) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #289

PR #289: `programmer/phase125k-c-d-opus-tierup-2026-05-07`. Builder report at `review/comms/BUILDER_REPORT_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md`. Per dispatch `MAIN_TERMINAL_PR285_RESOLUTION_AND_125KCD_DISPATCH_2026-05-07.md` (master `4a2a035`, PR #288).

**Result**: 20/20 Sonnet-Opus consensus match across 4 axes (100%). Strongest possible empirical signal — Path A (re-tag MW-17 as RAISE) validated at Opus tier.

## Audit scope (7 items per dispatch)

1. Diff scope strict (exactly 3 files: 20 Opus labels jsonl + script + report)
2. Opus 4.7 model id correctness (`claude-opus-4-7`)
3. Same v3.4 prompt
4. 5 canonical hands per axis × 4 axes = 20 hands matched from Sonnet-labelled corpus
5. No solver-as-labels in Opus reasoning
6. Sonnet-Opus comparison correctness per axis (verify 5/5 match per axis)
7. TC-X-DISPATCH-COMPLIANCE 16th formal exercise

## QC routing + Output

Standalone stream. ~10-15 min. QC writes `review/comms/REVIEW_QC_PHASE125K_C_D_OPUS_TIERUP_2026-05-07.md`.

**Status: QC stream — fire now on PR #289. ~10-15 min.**
