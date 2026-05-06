---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #197 (12.5I-A corpus design, commit d2c9a9e) + PR #198 (12.5J-A feature design, commit 58cb94e) — combined audit-now trigger
status: TRIGGER — fire now (parallel audit)
---

# QC pre-merge audit on PR #197 + PR #198 — fire now (parallel)

LEAD-PROGRAMMER opened both 12.5I-A and 12.5J-A design comms simultaneously per the parallel dispatch (PR #196). Audit both in parallel; they're non-overlapping (12.5I = corpus; 12.5J = features).

## PR #197 — 12.5I-A corpus design (commit d2c9a9e)

**Audit scope** per `MAIN_TERMINAL_PHASE125I_DISPATCH_2026-05-06.md` (master `c536c30`, PR #196):

1. **Diff scope** — exactly 1 file (`PLAN_PHASE125I_CORPUS_EXPANSION_*.md`); design-only
2. **Citation existence** — every file:line in design exists at master HEAD
3. **Per-template scope correctness** — verify T8'-redesigned (MW-25), T9'-expanded (MW-40), T10'-redesigned (MW-45) match diagnostic spec from PR #193; per-template count 30-40 each (total 90-120)
4. **Methodology incorporation** — verify all 6 standing methodology rules from 12.5H-A §10 reflected (cross-seed reporting, cap-binding pre-flight, tier-up verification, pilot-first, hero-only, pre-flight join-cardinality)

Post `REVIEW_QC_PHASE125I_A_DESIGN_*.md`. APPROVE or HOLD.

## PR #198 — 12.5J-A feature design (commit 58cb94e)

**Audit scope** per `MAIN_TERMINAL_PHASE125J_DISPATCH_2026-05-06.md` (master `c536c30`, PR #196):

1. **Diff scope** — exactly 1 file (`PLAN_PHASE125J_FEATURE_ENGINEERING_*.md`); design-only
2. **Citation existence** — every file:line in design exists at master HEAD
3. **Cascade scope completeness** — verify all 5 cascade points addressed per `feedback_attention_flags_when_features_change.md`: raw feature + attention vocab + prompt rules (if applicable) + capture pipeline + trainer
4. **Feature design specificity** — verify MW-17 axis (implied-odds + nut-blocker-with-overcards) + MW-47 axis (SUITED-NFD-bet+call-multiway raise pressure) have concrete computation specs, not handwave
5. **Direction-X-retro acknowledgment** — verify design explicitly notes Path Y boundary relaxation (owner approved at 12.5H-F gate)

Post `REVIEW_QC_PHASE125J_A_DESIGN_*.md`. APPROVE or HOLD.

## Sequencing on QC verdicts

Each PR independent:
- PR #197 APPROVE → orchestrator merges; dispatches 12.5I-B (situation generation)
- PR #198 APPROVE → orchestrator merges; dispatches 12.5J-B (feature implementation)
- Either HOLD → route findings to LEAD-PROGRAMMER for amendment

12.5K combined re-train fires only after BOTH 12.5I-E and 12.5J-E ship.

## What's blocked / what's queued

**Blocked:**
- PR #197 merge → on QC APPROVE
- PR #198 merge → on QC APPROVE
- 12.5I-B / 12.5J-B dispatches → on respective merges

**Queued:**
- 12.5K combined re-train (post both 12.5I-E + 12.5J-E)
- 12.5L gate evaluation (median ≥33 = PROMOTE)

## References

- 12.5I + 12.5J parallel dispatch: master `c536c30` (PR #196)
- 12.5I-pre diagnostic: master `54e2943` (PR #193)
- Memory: `feedback_explicit_action_trigger.md`, `feedback_attention_flags_when_features_change.md` (cascade scope for 12.5J)

**Status: QC trigger posted for parallel PRs #197 + #198. Each ready for independent audit.**
