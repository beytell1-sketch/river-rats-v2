---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #249 — 12.5I-MW40-VERIFICATION-E graduation-fail memo (4-source pattern documented; stay-wrong 4→4 unchanged) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #249

PR #249: `programmer/phase125i-mw40-verification-e-memo-2026-05-06`. Builder report: `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR245_RESOLUTION_AND_MW40E_DISPATCH_2026-05-06.md` (master `92e2d85`, PR #248).

Documentation milestone: graduation-fail memo closes the MW-40 verification round (5 phases A→B→C→D→E). NO new factory output, NO new labels, NO model inference — pure documentation + memory edit. ~$0 cost.

## Audit scope (7 items per dispatch)

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (squash-merge contribution against `master = 92e2d85`):
   - `review/RESTART_PROMPT_V9_3WAY.md` (annotation in MW-40 row only)
   - `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (Verified Negative Result entry; verify via direct read)
   - `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md` (OPTIONAL footnote; may be skipped at builder discretion)
   - `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md`
   
   Verify NOT touched: v3.x prompts (`prompts/`), `river-rats-core/` source, training-data, existing 788-corpus, prior-phase corpora, plan files (the merged plan stays as-is; -E doesn't amend it), other memory files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Stay-wrong list integrity** — verify in `review/RESTART_PROMPT_V9_3WAY.md`:
   - Header still "4 True Remaining Failures" (no count change)
   - MW-40 row still present (NOT removed; this is graduation-fail not graduation)
   - MW-40 row gets new annotation citing PR #241 + PR #245 + PR #247 + this PR
   - MW-17, MW-45, MW-47 entries unchanged

3. **BATCH2 reference label unchanged** — verify in `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` AND `design/multiway_reference_set/BATCH2_8_RANGE_ANALYSIS.md`:
   - MW-40 canonical action stays **BET MEDIUM** (no label change; this is graduation-FAIL, MW-40 stays as the original expert label)
   - If optional BATCH2 footnote was added per dispatch §"Files to edit" item 3, it's COMMENTARY only; the canonical label table row is unchanged
   - If optional footnote was SKIPPED, the BATCH2 file is untouched (also acceptable per dispatch)

4. **Memory file integrity** — verify in `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md` (via direct read):
   - New "Verified Negative Result" entry exists (or appended structure consistent with file's existing form)
   - MW-40 entry includes 4-source convergence citation (PR #241 Sonnet + PR #245 Opus + protocol-rule chain + PR #209 PILOT_787 reclassified)
   - Existing MW-25 entry (graduated CHECK HIGH) UNCHANGED
   - Existing solver-corrected section UNCHANGED
   - File integrity: no duplicate entries, no stale orphan sections

5. **NIT-1 / NIT-2 / NIT-3 carry-forward fold-in** — verify the -E memo addresses all 3 NITs explicitly:
   - **NIT-1**: "composition quad" used as canonical project terminology; "composition triple" memory note acknowledged as legacy with footnote/cross-reference; memory edit is owner-scope (NOT done in this PR; surfaced for owner read only)
   - **NIT-2**: <27/30 graduation threshold cited as Decision 3β criterion; observed 0/30 effective (5 pilot all BET; remaining 25/30 not labelled); this is the threshold's first formal application in a graduation outcome
   - **NIT-3**: -E memo's "lessons learned" section documents plan-internal-consistency cross-check candidate (TC-X-INTRA-PLAN-CONSISTENCY informal class); routes to TC-X-DISPATCH-COMPLIANCE motivating evidence

6. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x / river-rats-core / training-data / corpus edits beyond scope. Memory edit IS in scope per dispatch (mirrors PR #218 graduation pattern but on failing direction).

7. **TC-X-DISPATCH-COMPLIANCE (6th formal exercise)** — verify -E was authored per dispatch:
   - Memo-only; no new labels added (verification round complete)
   - No factory output (no new corpus rows)
   - No model inference (no LLM cost)
   - 4-source convergence table format matches MW-25 graduation pattern symmetrically
   - References all relevant PRs in the chain (PR #209, PR #213, PR #217, PR #228, PR #236, PR #237, PR #240, PR #241, PR #243, PR #244, PR #245, PR #247, PR #248)
   - Stay-wrong COUNT unchanged (4); ANNOTATION-only changes
   - BATCH2 reference label unchanged (BET MEDIUM stands)

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit (milestone documentation; closes MW-40 verification round). ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_E_GRADUATION_FAIL_MEMO_2026-05-06.md` on `qc/pr249-mw40-verification-e-review-2026-05-06`.

## What gates on this audit

- PR #249 merge → on QC PASS
- 12.5J-C trainer integration test on 61-surface dispatch → on PR #249 merge (next builder serial step; engineering scope)
- 12.5K combined re-train design → gates on -E + 12.5J-E ship

## What you do NOT do

- Do NOT make GTO judgments on whether MW-40 should have graduated — verification round complete; empirical answer is documented
- Do NOT modify any file (review-only)
- Do NOT recommend reverting -E memo to attempt re-verification (orchestrator-scope per `feedback_orchestrator_decides_not_recommends.md`)
- Do NOT run inference

## References

- 12.5I-MW40-VERIFICATION-E dispatch: `MAIN_TERMINAL_PR245_RESOLUTION_AND_MW40E_DISPATCH_2026-05-06.md` (master `92e2d85`, PR #248)
- PR #218 (BATCH2 MW-25 graduation update; the precedent for -E pattern but on graduation direction): master `e01b296`
- PR #245 (Builder -D Opus tier-up; 5/5 BET): master `877555a`
- PR #241 (Builder -C pilot HALT 25/25 BET): master `d411cb8`
- PR #228 (Plan; J-on-board structural prediction; merged): master `e0e0304`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_explicit_action_trigger.md`

**Status: QC stream — fire now on PR #249. Standalone audit, pre-merge, 7-item scope. ~10-15 min.**
