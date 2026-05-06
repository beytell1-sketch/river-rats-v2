---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #213 — 12.5I-C labelling round (5 Sonnet × 94 hands, v3.4) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #213

PR #213: `programmer/phase125i-c-labelling-2026-05-06`. Builder report at `review/comms/BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md` (commit on the branch). 470 labels, 0 refusals, ~$3.30 spent (well under $120 cap).

## Audit scope (training-data PR — same pattern as 12.5H-C + new MW-25 graduation evidence audit)

1. **Diff scope** — exactly 3 files: `data/corpus_revision_125i_labels_raw_2026-05-06.jsonl` (470 rows), `data/corpus_revision_125i_labels_2026-05-06.jsonl` (94 consensus rows), `review/comms/BUILDER_REPORT_PHASE125I_C_LABELLING_2026-05-06.md`. Anything else in diff → SHOULD_FIX/BLOCKER per TC-23 strict-scope.

2. **Citation existence** — every labeller reasoning trace cites v3.4 clauses (KB §1.7, DO NOT Rule 2, etc.). Spot-check 5 random hands across 3 templates.

3. **Label distribution sanity (G2)** — verify report's distribution table matches the consensus jsonl: T8'-r 30/0/0 CHECK, T9'-e 32 BET / 1 CHECK, T10'-r 27 RAISE / 2 CALL / 2 FOLD. 0 refusals across all 470.

4. **Cost reconciliation** — ≤ $120 cap; report says ~$3.30. Verify against pilot $0.30 + Step 1 $0.85 + Step 2 $2.15.

5. **Manual canonical correctness against predictions** — predictions: T8'-r CHECK (was BET pre-resolution; flipped post-PR #209); T9'-e BET; T10'-r RAISE. Verify 4 manual canonicals: PILOT_785 (MW-25 EXACT) = CHECK ✓, PILOT_786 (T8' adjacent) = CHECK ✓, PILOT_787 (MW-40 EXACT) = CHECK ✗ vs prediction (1 divergence; ≤1 STOP threshold respected), PILOT_788 (MW-45 ADJACENT) = RAISE ✓.

6. **MW-25 graduation evidence (NEW audit)** — verify report §"T8'-redesigned outcome" documents 4-source convergence (5/5 pilot + Opus HIGH + 30/30 step 1 + protocol traces) and that consensus_action + consensus_confidence on T8'-r rows in the jsonl uniformly = CHECK / 1.0.

7. **MW-40 graduation candidate evidence (NEW audit)** — verify report §"MW-40 graduation candidate (NEW)" surfaces PILOT_787 CHECK 0.6 finding and recommends Opus tier-up. Confirm builder did NOT silently update reference set or stay-wrong list (those are owner-scope).

## QC routing per `feedback_qc_routing_when_standalone_active.md`

Route through standalone QC stream (`~/river-rats-qc/`). Do NOT spawn parallel subagent for the same audit. Pre-merge audit (this is a milestone PR per `feedback_qc_required_before_approval.md`).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_C_LABELLING_2026-05-06.md` on `qc/pr213-labelling-review-2026-05-06` branch. PR opens. Verdict: PASS / ISSUES FOUND / FAIL with finding levels (BLOCKER / SHOULD_FIX / NIT).

## What gates on this audit

- PR #213 merge → on QC PASS + orchestrator-side Opus tier-up cross-check (post this audit)
- 12.5I-D corpus QC dispatch → on PR #213 merge
- MW-40 Opus tier-up cross-check → orchestrator runs after this QC verdict (independent of merge)
- 12.5K combined re-train → on 12.5I-E + 12.5J-E ship

## What you do NOT do

- Do NOT make GTO judgments on Sonnet labels (defer to v3.4 protocol + future Opus tier-up)
- Do NOT run Opus tier-up (orchestrator does that)
- Do NOT modify v3.x prompts or BATCH2 reference (owner-scope)
- Do NOT recommend reference updates (orchestrator surfaces to owner)

## References

- 12.5I-C fire dispatch: master `cef0c61` (PR #211)
- 12.5I-C MW-25 resolution: master `077c168` (PR #209)
- 12.5I-C original dispatch: master `a635bcb` (PR #206)
- 12.5H-C precedent (audit pattern): master `90e17dc` (PR #181)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_spec_vs_infrastructure_code_drift.md`, `feedback_explicit_action_trigger.md`

**Status: QC stream — fire now on PR #213. Standalone audit, pre-merge, training-data scope. ~5-10 min.**
