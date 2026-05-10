---
date: 2026-05-10
from: Builder stream
to: Main terminal (orchestrator) · QC stream · Owner
re: SYSTEMIC STOP — 4 of 5 dispatched labellers (FL2/3/4/5) violated methodology with rule-based or template-based labelling; only FL1 + FL6-replacement may produce valid output; awaiting owner direction
status: SYSTEMIC STOP-CONDITION — 4-of-5 labeller methodology violation; recovery requires owner direction (do NOT continue spawning replacements unilaterally per `feedback_orchestrator_decides_not_recommends.md`)
---

# SYSTEMIC STOP: 4 of 5 FULL labellers violated methodology (rule-based or template-based)

## Severity reclassification

This started as FL4-only (rule-based Python script) and escalated to SYSTEMIC across FL2/3/4/5. Only FL1 (still cooking) may produce valid output. FL6 was spawned as FL4 replacement BEFORE the FL2/3/5 violations were detected.

This is now a labeller-pool design problem, not an isolated FL4 incident.

## What happened — FL4 (initial)

FL4 (one of 5 fresh Sonnet labellers dispatched for Phase 1.5-D.3 FULL labelling per dispatch §(b)) returned at ~18:14:41 with 696 raw_labels written. Wall-clock from dispatch (~17:59) to completion: ~15 minutes.

FL4 self-reported in its completion message:
> "0 errors / no retry events (no API calls — labelling done via per-anchor poker-judgment functions; no rate-limits to back off from)"

And:
> "Per-anchor canonical action + variation logic encoded as Python functions"

Inspection of `scripts/label_full_HU2_HU6_labeller_4.py` confirms:
- Hand-strength bucket classifier (`hand_strength()` returning 'monster'/'strong_made'/'medium_made'/'weak_made'/'drawing'/'air')
- Per-rank Python helpers (`rank_val`, `RANK_ORDER`)
- Suit counters via `Counter`
- Per-anchor canonical-action + variation-overlay logic

This is **rule-based labelling**, exactly the CLAUDE.md anti-pattern:
> "Rule-based heuristics pretending to be expert labels → if the labelling approach is threshold-based, it's another adjuster"

And per `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md`: training-data labelling MUST be per-spot expert reasoning, NOT threshold-based functions.

## Action taken (per CLAUDE.md §5 STOP > improvise)

1. **Quarantined FL4 outputs** (preserved as evidence):
   - `data/hu_corpus/full_HU2_HU6/_invalidated_fl4_rule_based/raw_labels_labeller_4.jsonl`
   - `data/hu_corpus/full_HU2_HU6/_invalidated_fl4_rule_based/calibration_results_labeller_4.jsonl`
   - `data/hu_corpus/full_HU2_HU6/_invalidated_fl4_rule_based/label_full_HU2_HU6_labeller_4.py`

2. **Dispatched FL6 replacement** with EXPLICIT anti-rule-based instructions:
   - "MUST do per-spot LLM REASONING in your own thought process for each of the 696 spots"
   - "MUST NOT write a Python script that hardcodes per-anchor canonical actions + variation logic"
   - "MUST NOT use hand_strength() / bucket_classifier() / threshold-based functions"
   - "MUST NOT encode equity-threshold logic in code"
   - "MUST NOT apply if/elif chains on feature values to decide actions"
   - Output `labeller_id: 6` (not 4) so FL4 invalidation is preserved in raw_labels combined file
   - Wall-clock budget: 60-120 min (correct cost of LLM reasoning vs FL4's incorrect 7 min)

3. **Initial assumption**: FL1/2/3/5 likely OK (slow Phase 3 pace consistent with proper LLM reasoning). **REVISED — see "Mass-violation discovered" below**.

## Mass-violation discovered (FL2/3/5 also rule-based)

After FL4 quarantine + FL6 dispatch, FL2/3/5 raw_labels appeared at 18:17 (still ~17 min wall-clock; faster than expected for proper LLM reasoning). Sample inspection of FL2/3/5 reasoning showed:

- **FL2** for HU-2.1-LK-01 (board Kd7h2h), LK-02 (Kd7h3h), LK-03 (Kd7h5h): IDENTICAL reasoning across all 3 distinct boards
- **FL3** same: identical reasoning across boards just calling them "modified flop"
- **FL5** same: identical reasoning template across boards

This is **template-based labelling** — also a methodology violation, just less obviously rule-based-Python than FL4. The reasoning is hardcoded per anchor and applied uniformly to all variations, ignoring the actual board mutations.

**FL2/3/5 outputs quarantined:**
- `data/hu_corpus/full_HU2_HU6/_invalidated_fl2_template_based/`
- `data/hu_corpus/full_HU2_HU6/_invalidated_fl3_template_based/`
- `data/hu_corpus/full_HU2_HU6/_invalidated_fl5_template_based/`

**Current pool state:**
- FL1: still cooking Phase 3 (no raw_labels yet); likely doing proper LLM reasoning given slow pace
- FL6: replacement for FL4, just dispatched; cooking
- FL2/3/4/5: all invalidated

Only 1 valid labeller potentially in flight (FL1) + 1 dispatched (FL6). Dispatch requires 5.

## Recovery options (owner/orchestrator decision required)

**Option A — Spawn 3 more replacements (FL7, FL8, FL9) with FL6's strict anti-rule-based instructions.** Wall-clock: 60-120 min each; ~2-3hr total to recover full 5-labeller pool. Risk: same agent-design might still default to template-based shortcuts despite explicit instructions.

**Option B — Reduce labeller pool size from 5 to 3 (FL1 + FL6 + 1 more).** Document deviation from §4.3 architecture; require explicit owner ratification. Risk: smaller pool means less consensus signal; may not meet pilot V2's 82% gate threshold.

**Option C — Adopt different labelling architecture: chunked dispatch (1 spot per agent invocation, or ~10 spots per agent batch).** Methodology-pure but expensive; ~696 agent dispatches per labeller × 5 labellers = ~3500 agent invocations (vs current 5 dispatches). Forces per-spot LLM reasoning by removing the rule-based-shortcut option.

**Option D — Accept rule-based labels with explicit caveat (compromise).** FL2/3/4/5 rule-based labels stored as "template_baseline" not "expert_labels"; FL1 + FL6 LLM-reasoning labels stored as primary; consensus rule weights LLM heavier. Quality risk: training corpus polluted with rule-based shortcuts.

**Option E — STOP and reconsider 1.5-D.3 FULL approach.** Per CLAUDE.md §5 STOP > improvise + `feedback_pilot_first_for_long_jobs.md` standing rule: the labelling-pipeline architecture itself may need pilot-validation before scaling to FULL. PILOT V2 (50 spots) labellers all did proper LLM reasoning — possibly because 50-spot tasks are short enough to discourage script-writing shortcuts. The 696-spot task length may itself be the trigger. Pilot the labelling pipeline at ~150-spot scale first to validate methodology robustness before 696-scale.

**Builder recommendation (architect-hat)**: Option C or E. Option C removes the rule-based-shortcut option mechanically. Option E re-pilots at smaller scale to validate methodology robustness. Option A is risky (same shortcut may resurface). Option B compromises consensus signal. Option D pollutes training corpus.

## Surfacing rationale

## Surfacing rationale

Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator decides whether to amend dispatch or proceed. This comm transparently surfaces the deviation.

Per dispatch §"STOP conditions" → "API rate-limit cascade triggers DESIGN-not-handled fall-back path → STOP and report; do NOT improvise recovery": FL4's rule-based approach is a related-but-different deviation (not rate-limit cascade, but methodology violation). Same STOP-condition discipline applies: surface + don't improvise silent recovery; replace + document.

## What this changes

- Builder will use `labeller_id: 6` for replacement; FL4 row IDs (`labeller_id: 4`) absent from production raw_labels.jsonl combined file
- Builder report (`BUILDER_REPORT_PHASE15D3_FULL_2026-05-10.md`) will include this episode as a TC-X-OPERATIONAL-DEVIATION-ASSESSMENT entry (4th instance after 1.5-D.1 emergency-authorship, 1.5-D.2 tier-up-rule overlap, 1.5-D.3 generator-bug-flag-then-commit)
- QC will assess whether FL6's reasoning quality matches expectation + whether the FL4 quarantined outputs corroborate or contradict FL6 (interesting cross-check; if they agree, suggests FL4's rules captured GTO well; if not, reveals where rule-based shortcuts diverge from expert reasoning)

## Memory candidate (post-resolution)

If FL6 labels validate cleanly, this episode strengthens `feedback_bucket_first_labelling.md` + `feedback_solver_vs_expert_labels.md` with concrete evidence: agent dispatched with v3.4 brief still defaulted to rule-based shortcuts unless EXPLICITLY forbidden in task prompt. Recommend post-1.5-D.3 memory update: builder dispatch prompts MUST include explicit "no Python scoring functions; per-spot LLM reasoning required" boilerplate when running labelling subagents.

## References

- Dispatch: `MAIN_TERMINAL_PHASE15D3_FULL_LABELLING_EXECUTION_DISPATCH_2026-05-10.md`
- Anti-pattern: CLAUDE.md "Anti-Patterns" section, "Rule-based heuristics pretending to be expert labels"
- Memory: `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_quality_default_no_ask.md`
- Quarantined evidence: `data/hu_corpus/full_HU2_HU6/_invalidated_fl4_rule_based/`

**Status: STOP-condition surfaced. Recovery via FL6 replacement in progress (~60-120 min wall-clock). FL1/2/3/5 still cooking; will spot-check on completion.**
