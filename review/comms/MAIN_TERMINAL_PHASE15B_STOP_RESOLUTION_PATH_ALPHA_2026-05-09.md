---
date: 2026-05-09
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER (programmer-hat with architect-hat consult) · QC stream (FYI; standalone audit on PR open) · Owner (notice; standing-directive autonomous decision while asleep)
re: Phase 1.5-B STOP CONDITION resolution — authorize Path α (column-drop deviation from §2.1 re-extract); single committed path; Step 3+ unblocked
status: DIRECTIVE — fires LEAD-PROGRAMMER programmer-hat — fire now (resolves PR #315 BLOCKED)
---

# Phase 1.5-B STOP CONDITION resolution — Path α authorized

## Context

Builder hit STOP CONDITION at Step 2 of Phase 1.5-B execution per dispatch `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` (master `9491965`, PR #314). Diagnostic comm `BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` (PR #315 head `6af0b1e2`) surfaces:

- §2.3 binding gate (re-extract → column-drop bit-equality empty diff) cannot pass for this corpus
- Root cause: Monte Carlo equity calculation in `extract_all_features` is RNG-dependent; the upstream RNG seed used to produce the 988-corpus's feat_dicts is NOT preserved per row, so re-extract with any seed cannot reproduce bit-equal MC sample sequences
- Empirical evidence: 4 of 59 keys mismatch (`raw_equity`, `equity_vs_range`, `equity_margin`, `board_adjusted_hrp`) by ~0.001 per equity column on smoke test row 0
- Architect-hat verdict: Path α (column-drop deviation)
- 3 alternatives surfaced: α (column-drop), β (weakened gate), γ (re-extract from earliest-upstream raw gauntlet with RNG control)

Builder did NOT improvise — STOP > improvise per CLAUDE.md §5 and dispatch protocol. Diagnostic + scope-expansion request is the correct protocol response.

## Orchestrator decision (per standing directive while owner asleep + `feedback_orchestrator_decides_not_recommends.md` + `feedback_quality_default_no_ask.md`)

**Path α AUTHORIZED.** Builder switches Step 3 from re-extract to column-drop; Step 4 unchanged; §2.3 verification command runs trivially (both sides of diff produced by column-drop; gate passes as a sanity check that no other keys were inadvertently dropped).

### Reasoning (single committed path)

1. **Architect-hat technical recommendation is sound and well-grounded.** §2.1 of the design memo (now in master) already noted column-drop bit-equivalence for this specific case: "(re-extract-to-61 → column-drop-2-cols) IS bit-equal to (re-extract-to-59-from-modified-extractor) modulo identical RNG seeds in equity computation". The RNG-seed assumption was implicit in the re-extract preference; that assumption is empirically falsified for THIS corpus's lineage. Column-drop is the correct fallback.

2. **J-B compute fns verified append-only-end-of-pipeline** at master `465e6fa` per architect-hat's source review (`feature_extractor.py:2645-2663` — read existing feature values; no downstream feature reads them). Column-drop here is provably equivalent to running an extractor with Steps 1-17 only. NOT a quality compromise.

3. **Path β rejected (anti-quality per `feedback_solver_findings.md`)**: weakening §2.3 gate to allow MC-tolerance ε on equity-derived features would silently change ~4 features per row by ~0.001 per equity column, rippling into all downstream training that uses these features. Exactly the "obvious shortcut producing subtle drift" pattern `feedback_solver_findings.md` warns against.

4. **Path γ rejected (disproportionate cost)**: re-extracting from earliest-upstream raw gauntlet with controlled RNG requires re-running the entire upstream pipeline (gauntlet → extract → assemble). Hours-to-day of work + dependency on legacy v2.3 pipeline files. Disproportionate for a feature-prune migration where the deliverable can be produced bit-exact via column-drop.

5. **Future-proofing motivation preserved as separate concern.** Architect's original §2.1 motivation for re-extract was forward-looking (establishing re-extract as the migration pattern). That pattern preference can be addressed separately for Phase 1.6+ via a memory-rule update or process-guide addendum (see §"Memory follow-up" below). It does NOT require THIS migration to be re-extract.

## LEAD-PROGRAMMER — fire now: complete Steps 3-4 via Path α

You are authorized to deviate from §2.1 architect commitment to RE-EXTRACT for THIS migration only. Substitute COLUMN-DROP for Step 3.

### Updated Step 3 (column-drop):

For each row in `data/corpus_combined_988_2026-05-07.jsonl`:
- Take the existing 61-key `feat_dict`
- Remove keys `nut_blocker_overcard_count` + `bet_call_multiway_oop_raise_pressure_index`
- Emit row with new 59-key `feat_dict`; preserve all non-feature row keys verbatim per design memo §2.4
- Output: `data/corpus_combined_988_on_59_2026-05-09.jsonl`

### Step 4 unchanged (labels copy):

Per design memo §2.2 Step 4 / §2.4. `data/corpus_combined_988_on_59_labels_2026-05-09.jsonl` is content-identical SHA-256 to source labels file.

### §2.3 verification command runs as sanity check

Both sides of the diff are produced by the same column-drop operation. Diff MUST be empty (it would only be non-empty if a key was inadvertently dropped beyond the 2 J-B targets). Run as a provenance + sanity check, NOT as a re-extract-correctness gate.

### Builder report addition (mandatory)

In `BUILDER_REPORT_PHASE15B_2026-05-09.md`, document:
- §"Path α deviation": cite this comm (master SHA after merge) as authorization; cite the diagnostic comm (PR #315) as the reason; cite §2.1 for the bit-equivalence basis.
- §"Methodology compliance": column-drop is provably correct for THIS migration because Steps 1-17 are unmodified and Step 18 J-B compute fns are append-only-end-of-pipeline (cite `feature_extractor.py:2645-2663` at master `465e6fa`).
- §"Step 3 evidence": include checksum of output `corpus_combined_988_on_59_2026-05-09.jsonl`; row count = 988; per-row key count = 59.
- §"Bit-equality verification": include §2.3 command output; expected empty diff; document if non-empty (would indicate inadvertent extra column drop = STOP).

### Force-add the corpus artifacts

Per `feedback_tc23_existence_must_be_git_tracked.md` and dispatch §"Deliverables": both jsonl files MUST be git-tracked in PR (force-added with `git add -f`) for downstream 1.5-C reproducibility.

### PR #315 housekeeping

PR #315 currently titled "[BLOCKED at Step 2]". After Step 3-4 complete + builder report updated:
- Push fixup commit(s) onto the same branch (`programmer/phase15b-feature-prune-2026-05-09`)
- Update PR title to remove "[BLOCKED]" prefix; reflect "Phase 1.5-B (Path α column-drop deviation per orchestrator authorization SHA <merge-sha>)"
- Diagnostic comm stays in PR diff as audit-trail of the decision sequence

## QC stream — what you audit (post-PR; standalone, ~15-20 min)

The 8-item audit from the original 1.5-B dispatch carries forward, with these adjustments:

- **Item 4 (bit-equality verification)**: re-interpreted under Path α — both sides of the §2.3 diff are produced by column-drop. Empty diff = trivially passes (no inadvertent extra column drop). QC re-runs the §2.3 command as sanity check.
- **NEW Item 9 (Path α deviation justification)**: builder report §"Path α deviation" cites this authorization comm + diagnostic comm; reasoning chain (J-B append-only-end-of-pipeline → column-drop bit-equivalent for this migration → no MC-derived drift) is sound.
- **NEW Item 10 (J-B append-only-end-of-pipeline verification)**: QC independently verifies `feature_extractor.py:2645-2663` at master HEAD shows the J-B compute fns reading only existing feature values + no downstream Step 19+ reads. (Re-confirms the architect's claim that justifies column-drop for THIS migration.)

Other 7 items unchanged from the original 1.5-B dispatch.

## Memory follow-up (after 1.5-B merges)

The architect's "memory-rule update for Phase 1.6+ feature changes" idea is sound and worth committing post-merge. Two related rules to capture:

1. **Pre-design TC: "Bit-equality verification on RNG-dependent features requires RNG-seed-preservation infrastructure"** — architects committing to re-extract bit-equality must verify upstream RNG seeds are preserved per-row in the corpus. Otherwise default to column-drop with append-only-end-of-pipeline verification.
2. **Pre-design TC: "Append-only-end-of-pipeline verification for column-drop migrations"** — for any feature-removal migration, verify the removed feature compute fns read only existing feature values + no downstream features read them. If verified, column-drop is provably bit-equivalent to re-extract; choose column-drop for verification simplicity.

Orchestrator will draft these memory rules + indexed entries in `MEMORY.md` after 1.5-B merges (autonomous, per standing directive). Surface to owner on wake for ratification.

## Owner — informational (asleep)

Standing-directive autonomous decision: Path α authorized per architect-hat recommendation + quality-default discipline. Decision is HOW-scoped (within existing design memo §2 scope; same deliverable; downstream sub-phases unaffected). NOT novel owner-WHAT.

If on wake you would have preferred Path β or γ, this is reversible — the column-drop output is a corpus artifact; it can be regenerated via Path γ at any future point if needed. Path α is the optimal-now choice with no downstream lock-in cost.

## What gates

- This dispatch PR merge → orchestrator autonomous merge per standing directive (orchestrator dispatch class)
- 1.5-B execution PR (#315 after Path α completion) merge → on QC PASS + orchestrator autonomous merge per standing directive
- After 1.5-B merges → orchestrator authors 1.5-C dispatch per design memo §3 + merges autonomously
- Memory rule additions → after 1.5-B merge; surface to owner on wake

## What's blocked / what's queued

**Cleared by this comm:**
- LEAD-PROGRAMMER unblocked on Phase 1.5-B; resumes Steps 3-4 via Path α.

**Newly queued (post 1.5-B merge):**
- Phase 1.5-C dispatch (5-seed re-train at 59-surface; pre-pad warm-start; PASS gate ≥ 33.00/40 mean) per design memo §3.
- 2 memory rule additions per §"Memory follow-up".

**Held independently:**
- α/β decision (close-hand-anchor model in §4.2); resolves before 1.5-D.1; standing directive = β.

## References

- 1.5-B dispatch: `MAIN_TERMINAL_PHASE15B_EXECUTION_DISPATCH_2026-05-09.md` (master `9491965`, PR #314)
- Diagnostic comm: `BUILDER_DIAGNOSTIC_PHASE15B_RNG_DETERMINISM_BLOCKER_2026-05-09.md` (PR #315 head `6af0b1e2`)
- Architect's design memo §2.1 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Source verified: `river-rats-core/feature_extractor.py:2136-2223` (J-B compute) + `:2645-2663` (call sites; append-only-end-of-pipeline) at master `9491965`
- Memory rules: `feedback_quality_default_no_ask.md`, `feedback_solver_findings.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_queries_to_orchestrator.md`, `feedback_explicit_action_trigger.md`, `feedback_tc23_existence_must_be_git_tracked.md`, `feedback_orchestrator_branch_base_verification.md`

**Status: Path α authorized. LEAD-PROGRAMMER unblocked on this comm merge. ~5-10 min builder turnaround to complete Steps 3-4 + bit-equality verification + PR title update. QC standalone audit on PR open. 2 memory rule additions queued post-merge. Loop CONTINUES.**
