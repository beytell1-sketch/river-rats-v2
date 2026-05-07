---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #285 — 12.5K-C-C-SCALE (700 Lever C labels; Path A applied; MW-40 + MW-45 100% target-match; MW-17 + MW-47 sub-axis-variable) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #285

PR #285: `programmer/phase125k-c-c-scale-2026-05-07`. Builder report at `review/comms/BUILDER_REPORT_PHASE125K_C_C_SCALE_2026-05-07.md`. Per dispatch `MAIN_TERMINAL_PR281_RESOLUTION_AND_125KCC_SCALE_DISPATCH_2026-05-07.md` (master `7652b75`, PR #284).

700 labels for 4-axis 200-hand corpus expansion. PR title indicates partial sub-axis-variable on MW-17 + MW-47.

## Audit scope (8 items full-scale labelling format)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — labels jsonl + script + report. NO touch to v3.x prompts / BATCH2 / unrelated source.
2. **Path A re-tag verification** — MW-17 hands have `design_action=RAISE` (not CALL) per Path A ratification.
3. **Row count integrity** — 700 labels for 200 hands × ~3.5 labellers (or per-axis variation; verify math).
4. **Per-axis target-match verification** — MW-40 + MW-45 should be 100% target-match (per builder claim); MW-17 + MW-47 sub-axis-variable should have documented breakdown.
5. **No solver-as-labels** — labels cite v3.4 protocol rules.
6. **Reasoning convergence** — sample reasoning blocks per axis; verify convergent (not mode-collapse).
7. **TC-X-OWNER-SCOPE-DISCIPLINE** — no v3.x / BATCH2 / source / memory edits beyond scope.
8. **TC-X-DISPATCH-COMPLIANCE 15th formal exercise** — Path A applied; pilot-first verified executed; orchestrator-scope decisions preserved (sub-axis-variable not auto-resolved).

## QC routing + Output

Standalone stream. ~15-20 min. QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_SCALE_2026-05-07.md`.

## What gates

- PR #285 merge → on QC PASS
- 12.5K-C-D Opus tier-up dispatch → on PR #285 merge

**Status: QC stream — fire now on PR #285. ~15-20 min.**
