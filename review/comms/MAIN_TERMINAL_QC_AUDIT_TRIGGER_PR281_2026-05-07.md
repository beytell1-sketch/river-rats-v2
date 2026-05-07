---
date: 2026-05-07
from: Main terminal (orchestrator)
to: QC stream
re: PR #281 — 12.5K-C-C-FIX Path 2 (MW-47 PASS; MW-17 axis-target shift to RAISE; HALT-escalate) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #281

PR #281: `programmer/phase125k-c-c-fix-redesign-2026-05-07`. Builder report at `review/comms/BUILDER_REPORT_PHASE125K_C_C_FIX_2026-05-07.md`. Per dispatch `MAIN_TERMINAL_PR277_RESOLUTION_AND_125KCC_REDESIGN_DISPATCH_2026-05-07.md` (master `748f3a3`, PR #280).

**Empirical result**: Factory FD-suit fix WORKED (has_flush_draw activation MW-17 70% / MW-47 98%, up from 0%/0%). BUT 50 pilot labels: 10/10 RAISE HIGH unanimous across both axes — MW-47 PASS (target RAISE confirmed); **MW-17 FAIL on axis-target shift** (predicted CALL, observed RAISE).

**Builder discovery**: MW-17 redesign moved hero from canonical "off-suit + 3-same-suit board → backdoor only" CALLING spot to "suited hero + 2-FD-suit board → 4-same-suit nut FD" RAISING spot. Canonical MW-17 reference (AdKs on Jd8d4c) has structurally different hand-class than the redesigned hands. **MW-17 is a labelling-pipeline-canonical mismatch parallel to MW-40 graduation-fail.**

## Audit scope (9 items HALT-fix format)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected 4 files (factory script + v2 situations + pilot labels + report).
2. **Factory FD-suit fix verification** — confirm has_flush_draw activation MW-17 70% / MW-47 98% (up from 0%/0%).
3. **Path 2 re-design integrity** — MW-40 + MW-45 situations PRESERVED unchanged (per dispatch "do NOT modify MW-40 + MW-45"); MW-17 + MW-47 redesigned with corrected configs.
4. **Re-pilot label integrity** — 50 pilot labels well-formed; 5 hands × 5 labellers × 2 axes = 50 calls accounted.
5. **Reasoning convergence per axis** — convergent reasoning citing v3.4 KB §1.7 (nut-FD carve-out triggers correctly post-fix); not mode-collapse.
6. **MW-17 axis-target shift diagnosis** — verify the structural divergence claim: redesigned hands have "suited nut FD" structure that routes to RAISE per KB §1.7; canonical MW-17 reference has different structure (off-suit + backdoor only).
7. **No solver-as-labels** — labels cite v3.4 protocol rules.
8. **TC-X-OWNER-SCOPE-DISCIPLINE** — no v3.x / BATCH2 / source / memory edits beyond scope.
9. **TC-X-DISPATCH-COMPLIANCE 14th formal exercise** — Path 2 phases 1+2+3 executed; HALT-and-escalate per dispatch on EITHER pilot FAIL; orchestrator-scope decision route preserved (Path A/B/C surfaced).

## Critical audit emphasis

Item 6 (MW-17 axis-target shift diagnosis) is critical. If diagnosis correct → MW-17 = labelling-pipeline-canonical mismatch → Path A (re-tag as RAISE) is the empirically faithful choice.

## QC routing + Output

Standalone stream. ~10-15 min. QC writes `review/comms/REVIEW_QC_PHASE125K_C_C_FIX_2026-05-07.md` on `qc/pr281-125kcc-fix-review-2026-05-07`.

**Status: QC stream — fire now on PR #281. ~10-15 min.**
