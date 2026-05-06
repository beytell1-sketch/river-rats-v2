---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #245 — 12.5I-MW40-VERIFICATION-D Opus 4.7 tier-up (5/5 BET; full Sonnet-Opus consensus; graduation-fail confirmed) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #245

PR #245: `programmer/phase125i-mw40-verification-d-opus-tierup-2026-05-06`. Builder report: `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR241_RESOLUTION_AND_MW40D_DISPATCH_2026-05-06.md` (master `966fcbd`, PR #244).

**Result**: 5/5 Opus 4.7 = BET (default outcome per Path 3 matrix). Full Sonnet-Opus consensus on graduation-fail signal. **MW-40 graduation-fail is confirmed** under both production-prompt (Sonnet) and tier-up (Opus 4.7) models. Mirror of MW-25 4-source graduation pattern, applied symmetrically on the failing direction.

## Audit scope (7 items per dispatch §"QC stream")

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (squash-merge contribution against `master = 966fcbd`):
   - `data/corpus_revision_125i_mw40_verif_labels_opus_tierup_2026-05-06.jsonl` (5 Opus labels)
   - `scripts/run_125i_mw40_verif_opus_tierup.py` (orchestration script)
   - `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md`
   
   Verify NOT touched: v3.x prompts (`prompts/`), BATCH2 reference, `river-rats-core/` source, training-data, existing 788-corpus, prior-phase corpora, plan/comm files, memory files. Anything outside scope → BLOCKER per TC-X-OWNER-SCOPE-DISCIPLINE.

2. **Opus 4.7 model id correctness** — verify `claude-opus-4-7` exact (not Sonnet, not Haiku, not opus-3). Cite PR #209 precedent for the same model id. Builder report should explicitly cite the model id used.

3. **Same v3.4 prompt** — Opus called with the canonical `prompts/gto_labeller_v3.4.md` content; no prompt modifications, no inline overrides. Builder report should state the prompt source explicitly.

4. **5 hands matched** — Opus run on EXACTLY the same 5 hand-ids as Sonnet pilot in PR #241. Cross-reference the 5 ref_ids in `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl` (now merged on master). Any swap → FLAG.

5. **No solver-as-labels in Opus reasoning** — Opus output should cite v3.4 protocol rules (DO NOT Rule N, composition quad, danger_score), not solver outputs. Solver may be cited descriptively but not as label-source. Any solver-as-label citation → BLOCKER per `feedback_solver_vs_expert_labels.md`.

6. **Sonnet-Opus comparison correctness** — verify the side-by-side table:
   - 5 rows, one per pilot hand
   - Sonnet consensus column matches the 5/5 BET reported in PR #241 per hand
   - Opus action column matches the actual Opus output in the labels jsonl
   - Match/diverge flag computed correctly (5/5 should be MATCH per builder claim)
   - Aggregate verdict matches per-hand details

7. **TC-X-DISPATCH-COMPLIANCE (5th formal exercise)** — verify Path 3 implementation:
   - Opus only on 5 hands (NOT 30 like Path 1; NOT skipped like Path 2)
   - Builder did NOT make the -E decision (orchestrator-scope per dispatch)
   - Builder did NOT auto-fix any divergent result (would only matter if there was divergence; report should still confirm the protocol-discipline)
   - Cost reported within ~$2-5 estimate

## Critical audit emphasis: independent verification of consensus

QC's job is to verify the 5/5 Opus = BET claim is well-founded. Sample at least 2-3 of the Opus reasoning blocks and verify:
- Reasoning structure follows v3.4 protocol (bucket-first → composition → action)
- Cited rules are real v3.4 entities (DO NOT Rule N, composition quad keys, danger_score)
- Conclusion (BET) follows from the cited reasoning chain (not "BET because BET")
- Inter-hand variation in reasoning while same conclusion (= convergent like Sonnet was; not mode collapse)

If Opus reasoning matches Sonnet's DO NOT Rule 11 OOP-only exemption + villain_checked_back weakness chain → **strong corroboration**: Opus arrived at the same answer through the same protocol path. If Opus reasoning routes through DIFFERENT v3.4 rules but reaches BET → **strong corroboration via independent path**: even more robust signal. If Opus reasoning is sparse / boilerplate / non-substantive → FLAG (sparse Opus reasoning is a known failure mode; need to retry).

QC's verdict on this item gates the orchestrator's confidence in -E (graduation-fail memo PR).

## QC routing

Standalone stream (`~/river-rats-qc/`). Pre-merge audit. ~10-15 min.

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_D_OPUS_TIERUP_2026-05-06.md` on `qc/pr245-mw40-verification-d-review-2026-05-06`.

## What gates on this audit

- PR #245 merge → on QC PASS
- 12.5I-MW40-VERIFICATION-E memo-only PR (graduation-fail) → on PR #245 merge AND default outcome (5/5 Opus BET) confirmed by QC. NIT-1, NIT-2, NIT-3 carry-forward fold-into -E dispatch.

## What you do NOT do

- Do NOT make GTO judgments on whether 5/5 Opus = BET is "correct" — QC verifies the answer is well-founded (independent reasoning, no solver-as-labels, real protocol citations); the empirical answer is what it is
- Do NOT modify any file (review-only)
- Do NOT run additional inference

## References

- 12.5I-MW40-VERIFICATION-D dispatch (Path 3 ratification + -D fire): `MAIN_TERMINAL_PR241_RESOLUTION_AND_MW40D_DISPATCH_2026-05-06.md` (master `966fcbd`, PR #244)
- PR #209 (Opus 4.7 MW-25 tier-up; precedent): master `077c168`
- PR #241 (Builder pilot HALT 25/25 Sonnet BET; the source of the 5 pilot hands): master `d411cb8`
- v3.4 prompt protocol: `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: QC stream — fire now on PR #245. Standalone audit, pre-merge, 7-item scope. ~10-15 min.**
