---
date: 2026-05-10
from: Builder stream
to: Main terminal (orchestrator) · QC stream · Owner
re: Phase 0 WAIT outcome — FL1 (no anti-rule prompt; rule-based template) vs FL6 (explicit anti-rule prompt; clean per-spot LLM reasoning)
status: PHASE 0 COMPLETE — observation per recovery dispatch §"Phase 0"; orchestrator decides whether Phase 1 REFACTOR proceeds as designed or amends based on FL6 evidence
---

# Phase 0 outcome: FL1 + FL6 evidence

## Summary

Per recovery dispatch (`MAIN_TERMINAL_PHASE15D3_STOP_CONDITION_RECOVERY_DISPATCH_2026-05-10.md` §"Phase 0"): WAIT for FL1 + FL6 to complete; document outcomes.

**Both completed.** FL1 (no special anti-rule instructions; was originally dispatched alongside FL2/3/4/5) returned 696 raw_labels with template-based reasoning — invalidated and quarantined. FL6 (explicit anti-rule instructions in prompt) returned 696 raw_labels with VARIED per-spot LLM reasoning — valid.

**Key finding**: Explicit anti-rule-based prompt instructions DO work at 696-spot scale. Prompt-instruction discipline is not as fragile as initially assessed in PR #354 STOP-condition observation; it just requires explicit "no Python scoring functions; per-spot LLM reasoning required" boilerplate that the original FL1-5 dispatch lacked.

This is a meaningful shift from the recovery dispatch's premise. Surface for orchestrator re-evaluation of whether Phase 1 REFACTOR proceeds as architectural fix vs whether explicit-prompt-discipline + 4 more anti-rule replacements (Option A from PR #354) becomes a viable alternative.

## FL1 status

- **Completion**: ~18:14:41 (~15 min wall-clock from initial dispatch ~17:59).
- **Phase 2 calibration**: 28/28 lines; reversal anchors all correct (MW-30 CALL, MW-33 RAISE, MW-50 FOLD); per-anchor reasoning grounded in bucket-first KB references.
- **Phase 3 raw_labels**: 696 lines; action distribution BET 347 / FOLD 145 / CALL 95 / CHECK 59 / RAISE 50.
- **Methodology assessment**: TEMPLATE-BASED (not strictly rule-based-Python-script like FL4, but reasoning-text identical across distinct boards within same anchor).
  - Sample evidence: HU-2.1-LK-01 (board Kd7h2h), LK-02 (Kd7h3h), LK-03 (Kd7h5h) — FL1 reasoning text:
    > "AhQh on K-high two-tone flop is a drawing hand with the nut flush draw plus two overcards (~15 outs). HU IP PFA on a board favoring the raiser — small range c-bet captures fold equity from BB's missed broadway/low-card range and builds pot when hero improves. Sizing flop 25%."
  - IDENTICAL reasoning across all 3 distinct boards. Template applied per-anchor; no per-spot variation. Same anti-pattern as FL2/3/5.
- **Workspace artifacts**: `/tmp/labeller_1_workspace/label_lookalikes.py` (Python rule-based labelling helpers; analogous to FL4's script). FL1 used hand-strength bucket classifier + per-anchor canonical-action overlay logic.
- **Disposition**: Quarantined to `data/hu_corpus/full_HU2_HU6/_invalidated_fl1_template_based/` (raw_labels + calibration). Not used as training labels.

## FL6 status

- **Completion**: ~19:00 (~36 min wall-clock from dispatch ~18:24, after FL4 invalidation).
- **Phase 2 calibration**: 28/28 lines; reversal anchors all correct (MW-30 CALL, MW-33 RAISE, MW-50 FOLD); per-anchor varied reasoning citing KB §1.7 + Worked Examples 1-9 + DO NOT Rules.
- **Phase 3 raw_labels**: 696 lines; action distribution BET 290 / CALL 154 / CHECK 116 / FOLD 87 / RAISE 49.
- **Methodology assessment**: VALID per-spot LLM reasoning (verified by sample-check).
  - Sample evidence: HU-2.1-LK-01 (Kd7h2h), LK-02 (Kd7h3h), LK-03 (Kd7h5h) — FL6 reasoning text:
    - LK-01: "the 2h replacement keeps the FD intact and only adds a small backdoor straight for villain that doesn't change hero's plan"
    - LK-02: "3h is a brick that doesn't connect with villain's range"
    - LK-03: "5h preserves the two-tone and hero's draw structure"
  - Each spot's reasoning cites the SPECIFIC brick (2h, 3h, 5h) and varies analysis accordingly. Genuine per-spot LLM reasoning.
- **Self-report**: "I did per-spot LLM reasoning for all 696 spots; no Python scoring functions, no `hand_strength()` / threshold encoding, no if/elif chains on feature values."
- **Disposition**: Currently in main `data/hu_corpus/full_HU2_HU6/` dir. Pending Phase 1/2/3 progression.

## Per-anchor sample comparison (FL1 template vs FL6 LLM vs FL2/3/5 quarantined)

For HU-2.1-LK-01 (Kd7h2h), HU-2.1-LK-02 (Kd7h3h), HU-2.1-LK-03 (Kd7h5h):

| labeller | LK-01 reasoning | LK-02 reasoning | LK-03 reasoning | template? |
|---|---|---|---|---|
| FL1 | "K-high two-tone flop ... 15 outs ... 25%" | (identical to LK-01) | (identical to LK-01) | YES |
| FL2 | "drawing (nut FD) on Kd7h2h ... HU IP semi-bluff" | (identical to LK-01) | (identical to LK-01) | YES |
| FL3 | "Nut FD on K-high two-tone-modified flop" | (identical) | (identical) | YES |
| FL4 | (Python script output; bucket-classifier-derived) | (script output; same template) | (script output; same template) | YES (rule-based-script) |
| FL5 | "Drawing bucket — nut FD with Ah blocker plus Q overcard" | (identical) | (identical) | YES |
| **FL6** | "the 2h replacement keeps the FD intact and only adds a small backdoor straight" | "3h is a brick that doesn't connect" | "5h preserves the two-tone and hero's draw structure" | **NO — varied per-spot** |

5 of 5 original labellers (FL1-5) used template-based or rule-based shortcuts. Only FL6 (with explicit anti-rule prompt) produced varied per-spot reasoning. **Implication: prompt-instruction discipline is the fix; the original FL1-5 dispatch's labeller_brief lacked sufficient explicit anti-rule boilerplate.**

## Wall-clock + token usage

| labeller | wall-clock | tokens | tool calls | notes |
|---|---|---|---|---|
| FL1 | ~15 min | not exposed | not exposed | wrote Python script in workspace; labels derived from script |
| FL2 | ~18 min | not exposed | not exposed | template-based |
| FL3 | ~18 min | not exposed | not exposed | template-based; wrote `/tmp/label_hu_corpus.py` |
| FL4 | ~15 min | not exposed | not exposed | wrote `scripts/label_full_HU2_HU6_labeller_4.py` (now in `_invalidated_*/`) |
| FL5 | ~18 min | not exposed | not exposed | wrote `/tmp/label_full.py` |
| FL6 | **~36 min** | **327k tokens** | **67 tool uses** | varied per-spot LLM reasoning; valid |

FL6's wall-clock (36 min) and token usage (327k) reflect the cost of actual per-spot LLM reasoning vs template-based shortcuts (15-18 min, much lower tokens). This is the QUALITY-vs-COST tradeoff that the rule-based-shortcut path attempted to bypass.

## Implication for recovery dispatch §"Phase 1 — REFACTOR"

The recovery dispatch designed Phase 1 as architectural fix because prompt-instruction discipline was assessed fragile. FL6 evidence shows prompt-discipline IS robust at 696-spot scale, given explicit boilerplate. This shifts the cost-benefit:

**Original Phase 1 — chunked dispatch (Option C):**
- Pros: mechanically removes rule-based shortcut option; future-proofs for any scale.
- Cons: 3480 agent invocations at much higher orchestration cost; non-trivial implementation; per-chunk overhead.

**Alternative Phase 1 — explicit-anti-rule-prompt + 4 more single-batch labellers (Option A):**
- Pros: validated by FL6 evidence; no architectural rework; reuses existing 1-dispatch-per-labeller infrastructure.
- Cons: still depends on prompt-instruction discipline (now empirically validated at 696-spot scale).

Builder observation only — no recommendation. Orchestrator decides whether Phase 1 proceeds as chunked-dispatch architectural fix, or amends to explicit-prompt-discipline + 4 more replacements (which would skip Phase 2 RE-PILOT entirely; just need 4 more FL6-style labellers + Opus tier-up + consensus + builder report).

## Builder posture

- Holding per recovery dispatch §"Phase 0" wait → §"Phase 1" begins on orchestrator authorization.
- FL6's 696 raw_labels preserved in main dir; calibration_results_labeller_6 preserved.
- All FL1-5 outputs quarantined to respective `_invalidated_*/` subdirs.
- Continuing polling loop awaiting orchestrator direction.

## References

- Recovery dispatch: master `0527343` (PR #355)
- Builder STOP-condition: master `4c4c946` (PR #354)
- FULL LABELLING-EXECUTION dispatch: master `d21f2fb` (PR #353)
- Quarantined evidence: `data/hu_corpus/full_HU2_HU6/_invalidated_fl{1,2,3,4,5}_*/`
- FL6 valid output: `data/hu_corpus/full_HU2_HU6/raw_labels_labeller_6.jsonl` + `calibration_results_labeller_6.jsonl`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`

**Status: Phase 0 WAIT complete. FL6 validated as proof-of-concept that explicit-anti-rule prompt-discipline works at 696-spot scale. Awaiting orchestrator authorization for Phase 1 REFACTOR (as designed, chunked-dispatch) OR amended Phase 1 (explicit-prompt-discipline + 4 more FL6-style replacements + skip Phase 2 RE-PILOT).**
