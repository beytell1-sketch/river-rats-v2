---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: PR #241 — 12.5I-MW40-VERIFICATION-C pilot HALT (25/25 BET unanimous; CHECK prediction refuted; Decision 3β graduation-fail signal at pilot stage) — fire audit now
status: TRIGGER — fire now
---

# QC stream — fire now on PR #241

PR #241: `programmer/phase125i-mw40-verification-c-labelling-2026-05-06`. Builder report: `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` (in branch). Per dispatch `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md` (master `3927024`, PR #240) §"Stop conditions" first item: "Pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK) → STOP and report to orchestrator."

**Pilot result**: 5 hands × 5 sonnet = **25/25 BET at 1.00 confidence per hand** (far stronger than the BET-mixed threshold). Builder correctly halted; route-to-orchestrator engaged. This is the verification round's empirical answer at pilot scale.

## Audit scope (8 items; HALT-format adapted from -C labelling audit scope)

This is a HALT audit, not a normal labelling-round audit. Scope is adapted to verify the pilot evidence integrity for graduation-decision use.

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — expected files (squash-merge contribution against `master = 3927024`):
   - `data/corpus_revision_125i_mw40_verif_labels_pilot_raw_2026-05-06.jsonl` (25 raw labels: 5 hands × 5 labellers)
   - `scripts/run_125i_mw40_verif_labelling.py` (orchestration script; pilot-only path executed)
   - `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` (the report)
   - Optionally `review/mass_labelling_mw40v_2026-05-06/pilot/*` working-directory artifacts if useful for QC (within reasonable size budget)
   
   Verify NOT touched: v3.x prompts (`prompts/`), BATCH2 reference, `river-rats-core/` source, training-data, existing 788-corpus or any prior-phase corpus files, plan/comm files, memory files.

2. **Pilot label integrity** — verify the 25 labels are well-formed:
   - Each row has hand-id + labeller-id + action + confidence + reasoning
   - All 25 actions = BET (or whatever builder reports; cross-check against builder claim)
   - All 25 confidences = 1.00 (builder claim) or as reported
   - Reasoning text present per label (not empty, not boilerplate)

3. **Reasoning convergence (NOT mode collapse) verification** — this is the critical audit item for HALT integrity. If 25/25 labels reach BET via the SAME reasoning path (e.g., all cite "DO NOT Rule 11 OOP-only exemption + villain_checked_back weakness + composition quad villain_air_pct + danger_score=0 → value/protection BET"), that's convergent reasoning — empirically robust signal. If 25/25 labels reach BET via DIFFERENT reasoning paths or via copy-paste-identical-token patterns, that suggests mode collapse — empirically weaker signal.
   
   QC verifies by sampling 5-10 of the 25 reasoning blocks and checking:
   - Cited rules / protocol references (Should be in v3.4 protocol surface; e.g., DO NOT Rule N, composition quad, danger_score)
   - Reasoning structure (bucket-first → composition → action; not just "BET because BET")
   - Inter-labeller variation in phrasing while same conclusion (= convergent; OK) vs identical-token-sequences (= mode collapse; FLAG)

4. **No solver-as-labels** (`feedback_solver_vs_expert_labels.md`) — verify reasoning blocks do not cite solver outputs as authority for BET. Solver may be cited descriptively but not as label-source. Any solver-as-label citation → BLOCKER.

5. **Per-hand consensus computation** — 5 labellers × 5 hands = 25 labels. Each hand's per-labeller breakdown should show 5/5 BET (per builder claim). Verify the math: 5 hands × 5 labellers each = 25 BETs total; no hand has fewer than 5 labellers; no labeller missed any hand.

6. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x / BATCH2 / core / corpus / plan / memory edits.

7. **TC-X-DISPATCH-COMPLIANCE (4th formal exercise)** — verify HALT was triggered correctly per dispatch §"Stop conditions" first item (BET-mixed or worse triggers STOP-and-report). 25/25 BET unanimous is strictly stronger than BET-mixed; dispatch's threshold satisfied with margin.

8. **TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)** — flag any new dispatch-internal contradictions surfaced by the pilot data. E.g., did any pilot hand's structural pattern violate plan §3 constraints? Did any pilot hand emerge with feat_dict that contradicts the corpus's documented Step-18 expected ≈ 0 pattern?

## Critical audit emphasis: empirical signal robustness

This audit's verdict is what gates the orchestrator's path decision (halt-verification vs scale-anyway vs hybrid-Opus). QC's verdict on **reasoning convergence** (item 3) is the decisive evidence:

- If reasoning is CONVERGENT (5+ labellers cite the same v3.4 protocol-rule chain → BET) → strong empirical signal → orchestrator likely picks halt-verification (Path 2) or hybrid-Opus (Path 3) for 2nd-source confirmation
- If reasoning is MODE-COLLAPSED (25 identical-token reasoning blocks suggesting Sonnet's pre-trained bias overrides per-hand reasoning) → weaker empirical signal → orchestrator may pick scale-anyway (Path 1) or revisit prompt design before any -D/-E

QC has no preference on which path; QC's job is to surface the empirical-robustness-of-pilot signal.

## QC routing

Standalone stream (`~/river-rats-qc/`) per `feedback_qc_routing_when_standalone_active.md`. Pre-merge audit. Expected duration: ~10-15 min (HALT-format with reasoning-block sampling adds ~5 min vs normal -C labelling audit).

## Output

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_C_PILOT_HALT_2026-05-06.md` on `qc/pr241-mw40-verification-c-pilot-review-2026-05-06`. PR opens. Verdict: PASS / ISSUES FOUND / FAIL.

## What gates on this audit

- PR #241 merge → on QC PASS
- 12.5I-MW40-VERIFICATION-D Opus tier-up dispatch → on PR #241 merge AND orchestrator path decision (Path 1 / 2 / 3). Quality-default tentative selection: **Path 3 (Hybrid Opus on 5 pilot hands)** for 2nd-source confirmation per `feedback_pilot_first_for_long_jobs.md` sub-rule (training-data outputs require Sonnet→Opus tier-up; here the verification-decision output requires multi-source confirmation mirroring MW-25 4-source graduation pattern).
- 12.5I-MW40-VERIFICATION-E memo-only PR (graduation-fail) → on -D Opus confirmation of BET (or escalation if Opus splits)

## What you do NOT do

- Do NOT make GTO judgments on whether 25/25 BET is "correct" — that's the empirical answer; QC's job is to verify the answer is well-founded (convergent reasoning, no mode collapse, no solver-as-labels)
- Do NOT modify any file (review-only)
- Do NOT recommend reverting the pilot HALT (builder followed dispatch correctly)
- Do NOT run additional inference

## References

- 12.5I-MW40-VERIFICATION-C dispatch (with halt condition that triggered): `MAIN_TERMINAL_PR236_RATIFY_AND_MW40C_DISPATCH_2026-05-06.md` (master `3927024`, PR #240)
- PR #228 plan (J-on-board structural prediction; PILOT_787 evidence chain): master `e0e0304`
- PR #209 (Opus 4.7 MW-25 re-eval; precedent for -D Opus tier-up pattern): master `077c168`
- PR #213 + PILOT_787 source (Sonnet 3-2 + Opus HIGH; the 3-source evidence Decision 3β tested): master `994ae67`
- v3.4 prompt protocol (DO NOT Rule 11 OOP-only exemption; the rule that overrode the structural composition argument per builder report): `prompts/gto_labeller_v3.4.md`
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_solver_vs_expert_labels.md`

**Status: QC stream — fire now on PR #241 (HALT audit format). Standalone, pre-merge, 8-item scope (item 3 reasoning-convergence is the critical audit). ~10-15 min.**
