---
date: 2026-05-05
from: Main terminal (orchestrator)
to: QC stream
re: Phase 12.5E-D — corpus QC phase; fire 4-gate sweep on merged corpus + document queued cleanups
status: TRIGGER — fire now
---

# Phase 12.5E-D — corpus QC sweep

12.5E-C merged at master `a598f0a`. New corpus state: 604 hands total (494 existing + 110 new) with consensus labels. Per `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` §8.D, 12.5E-D is the corpus QC phase — QC runs the 4 gates from design §7 on the merged-state and produces findings.

## QC stream — what you audit (4 gates per design §7 + 3 cleanup items)

### Gate G1 — join-cardinality (combined corpus)

- Join key: `pilot_hand_id` (per 12.5D' protocol amendment)
- Verify cardinality: `pilot_hand_id` count in `data/corpus_revision_125e_situations_2026-05-04.jsonl` + `data/corpus_revision_125e_manual_canonicals_2026-05-04.jsonl` + `data/corpus_revision_500_hand_2026-04-27.jsonl` = 604 unique IDs (no collisions)
- Verify labels join: `data/corpus_revision_125e_labels_2026-05-05.jsonl` (110) + `data/corpus_revision_500_hand_labels_2026-04-27.jsonl` (494) = 604 unique IDs matching situations
- Pass criterion: 604/604 cardinality, zero collisions across cohorts (existing 494 vs new 110)

### Gate G2 — distribution sanity (combined corpus)

- Class distribution post-merge: 604 hands across {FOLD, CHECK, CALL, BET, RAISE}
- Verify no class < 5% (informational; expected: RAISE jumps from 5.9% baseline to ~10.1% per design §4)
- Verify confidence histogram matches expectation (median consensus_confidence ≥ 0.8 across both cohorts)
- Pass criterion: distribution shapes within design §4 predictions

### Gate G3 — duplicate detection (cross-cohort)

- Verify zero exact-duplicate situations between the new 110 and existing 494 on (board, hero_cards, action_history, hero_position)
- Builder self-checked at PR #142 self-checks; QC re-verifies at corpus-QC scope

### Gate G4 — labeller-drift detection (NEW gate; fires for first time)

Per design §7 G4: compare labelling pattern between the new 110 (12.5E-C labels) and existing 494 (12.5D corpus labels). Drift indicators:
- Median consensus_confidence shift (new vs old)
- Per-class confidence shift (e.g., RAISE confidence higher/lower in new cohort)
- T8 control hands specifically: same-action ≥70% match against parametric expectation; confidence-Δ <0.15 vs 12.5D-corpus equivalents

Both cohorts used Sonnet × 5 protocol so model-drift is zero; expected drift drivers are: corpus-design template specificity (T1-T8 are more pattern-locked than 12.5D's mixed-source generation), v3.3/v3.4 protocol vs older versions used at 12.5D corpus authoring time.

Pass criterion: drift within design §7 G4 thresholds OR drift documented + non-blocking.

### Cleanup items to document (3 NITs from prior PRs — surface, do NOT block)

1. **NIT-1 from PR #139** (`REVIEW_QC_PHASE125E_B_AMEND_2026-05-05.md`): `PLAN_PHASE125E_CORPUS_EXPANSION_2026-05-04.md` §3.T8 cites 36 hands; dispatch (PR #133) compressed parametric T8 to 22 (+14 manual = 110 total). Document in 12.5E-D findings; suggest fix-forward at 12.5E-E in a single comm amend.

2. **PILOT_595 design_note cosmetic** (from builder gto-expert-hat self-review, PR #136 amendment): design_note describes hero as "TPTK + nut blocker" but the situation actually gives top-two-pair (AsKs on Ad...QhKh river ⇒ both A and K paired). Bucket + labelling logic unchanged. Document in 12.5E-D findings.

3. **NIT-1 from PR #148** (`REVIEW_QC_PHASE125E_C_AMEND_FINAL_2026-05-05.md`): preserved §"What the BLOCKED PR ships" section in `BUILDER_REPORT_PHASE125E_C_RESOLVED_2026-05-05.md` (line 151) cites old `BUILDER_BLOCKED_PHASE125E_C_T5_MISMATCH` filename which no longer exists post-rename. V-X4 family. Document in 12.5E-D findings.

These are documentation-only items; do NOT block 12.5E-D APPROVE on them. They ride along at 12.5E-E builder cleanup window.

## Output

`REVIEW_QC_PHASE125E_D_CORPUS_QC_2026-05-05.md` to `review/comms/` (orchestrator-side trigger; QC-side filename per QC stream's preferred convention is fine).

Verdict: APPROVE (all 4 gates pass) or HOLD (any gate fails or drift exceeds design thresholds).

## Sequencing on QC verdict

- **APPROVE** → orchestrator dispatches 12.5E-E (re-train using existing trainer module on master + new 604-hand corpus + labels)
- **HOLD on G1-G3** → orchestrator routes to LEAD-PROGRAMMER for amendment (rare; builder self-checked already)
- **HOLD on G4 drift** → orchestrator decides per-magnitude: if drift indicates label-quality issue, route back; if drift indicates real distributional shift the design intended, document and proceed

## What's blocked / what's queued

**Blocked:**
- 12.5E-D output → QC fires now per this trigger
- 12.5E-E dispatch → on 12.5E-D APPROVE
- 12.5E-F gate evaluation → on 12.5E-E run completion
- 12.5G cap retuning sweep → post-12.5E-F regardless of outcome

**Queued (for 12.5E-E builder cleanup window):**
- NIT-1 PLAN §3.T8 wording fix
- PILOT_595 design_note cosmetic fix
- PR #148 NIT-1 (BUILDER report stale filename) fix
- MEDIUM-2 from PR #134 (V-X4 prose at trainer line 1371)
- 3 NITs from PR #134
- Protocol amendment #2 (verify labeller protocol's discriminator on sample situations before declaring blueprint design complete) → builder formalizes in `docs/PROCESS_GUIDE.md`

## References

- 12.5E-C merged: master `a598f0a` (PR #142)
- 12.5E-C QC findings: master `d5f3609` (PR #148)
- LABELS_FINAL directive: master `3914fea` (PR #146)
- 12.5E-A design: master `bad1396` (PR #133); §7 (QC gates) + §8.D (12.5E-D scope)
- Memory: `feedback_explicit_action_trigger.md` (NEW 2026-05-05; this comm IS the explicit trigger), `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_quality_default_no_ask.md`

**Status: 12.5E-D TRIGGER posted. QC fires 4-gate sweep on merged 604-hand corpus. APPROVE unblocks 12.5E-E re-train.**
