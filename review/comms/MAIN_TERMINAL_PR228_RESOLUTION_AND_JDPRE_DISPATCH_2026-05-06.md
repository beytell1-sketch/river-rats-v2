---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #228 PASS+1SHOULD_FIX+2NIT acknowledged → resolve SHOULD_FIX-1 via Path 3 (Hybrid); merge PR #228 + PR #230; dispatch 12.5J-D-pre test-guard deflake (Option b)
status: DIRECTIVE — merges PR #228 + PR #230; resolves QC SHOULD_FIX-1; fires LEAD-PROGRAMMER on 12.5J-D-pre
---

# PR #228 + PR #230 merge + SHOULD_FIX-1 resolution + 12.5J-D-pre dispatch

QC verdict on PR #228 (`REVIEW_QC_PHASE125I_MW40_VERIFICATION_A_DESIGN_2026-05-06.md` on `qc/pr228-mw40-verification-a-review-2026-05-06`, PR #230): **PASS — 0 BLOCKER, 1 SHOULD_FIX, 2 NIT (22nd solo cycle).** SHOULD_FIX-1 is a methodology-rule divergence between dispatch and plan that requires orchestrator ratification per `feedback_explicit_action_trigger.md` + `feedback_orchestrator_decides_not_recommends.md`. NITs are advisory.

## SHOULD_FIX-1 resolution — Path 3 (Hybrid)

QC offered three resolution paths for the pilot-first divergence (dispatch line 50: "5-hand pilot before full 30-hand factory run during 12.5I-MW40-VERIFICATION-B" vs plan §6 row 4: "deterministic factory exempts pilot-first at -B"). Per `feedback_quality_default_no_ask.md`: pick the slow-quality option without asking.

**Decision: Path 3 (Hybrid).**

### Rationale

The dispatch's pilot-first rule was process-preventative against schema-mismatch / Step-18 feature regressions / ref_id collisions surfacing only after all 30 variants are emitted. The plan's "deterministic factory" argument has merit: factory output is deterministic (no LLM uncertainty to mitigate), so a 5-hand LLM pilot adds cost without commensurate signal. BUT — schema/feature/ref_id integrity bugs ARE the class of failure pilot-first protects against, even in a deterministic pipeline. A binary "either it works or it doesn't" assumption discards a free safety net.

Path 1 (ratify) discards the safety net. Path 2 (amend plan now) requires a builder fix-forward PR + churn. Path 3 closes the gap with minimal overhead — a 5-hand pre-flight schema/feature/ref_id validation at -B time. No LLM cost (factory is deterministic; the validation is on the factory output itself), full process-preventative coverage.

### Authoritative specification (binds at 12.5I-MW40-VERIFICATION-B dispatch)

When 12.5I-MW40-VERIFICATION-B is dispatched (after 12.5J-D-pre merges), the dispatch comm MUST include this Hybrid clause:

> **Pre-flight on first 5 emitted situations (Hybrid pilot-first per PR #228 SHOULD_FIX-1 resolution):**
> 
> Before generating the full 30 variants, the factory MUST emit the first 5 situations as a pre-flight batch and run the following validation pass against them:
> 
> 1. **Schema parity** — verify `feat_dict` keys match the canonical 61-surface (post-PR #205); 0 NaN; 0 Inf; 0 missing keys. Any failure → STOP and report; no further situations emit.
> 2. **Step-18 feature plausibility** — verify `nut_blocker_overcard_count` and `bet_call_multiway_oop_raise_pressure_index` compute deterministically; values in plausible ranges per `feature_extractor.py` definitions. Any failure → STOP.
> 3. **ref_id namespace integrity** — verify the 5 ref_ids fall in the new disjoint namespace (`PILOT_MW40_VERIF_001..005`) and do NOT collide with existing 788-corpus ref_ids. Any collision → STOP.
> 4. **Top-level structural fields** — verify `hero_seat`, `hero_position`, `street_of_decision`, `villain_check_through_count`, `hand_category`, `kicker_class` match plan §3 constraint table on all 5 emitted hands. Any drift → STOP.
> 
> Only on all 4 checks passing does the factory continue with the remaining 25 situations to reach 30. Pre-flight cost: ~$0 (no LLM; pure schema/feature/ref_id validation).

This Hybrid resolution preserves the spirit of the plan's deterministic-factory observation (no LLM pilot needed) AND the dispatch's process-preventative pilot-first intent (catch integrity bugs at hand 5, not hand 30).

### NIT-1 (terminology drift) and NIT-2 (5th stop condition in §10 not §8)

Both are advisory, do not block merge. Queue both as **fix-forward** to be folded into the 12.5I-MW40-VERIFICATION-B dispatch comm or any subsequent design-comm amendment touch (whichever comes first). No standalone PR needed for either; orchestration efficiency per `feedback_orchestration_efficiency_rules.md`.

### TC-X-DISPATCH-COMPLIANCE (proposed test class)

QC proposed `TC-X-DISPATCH-COMPLIANCE` ("for every design-phase plan, run a dispatch-vs-plan methodology-rule diff before per-item audit") in §"Smarter-over-time artefact updates." This is reasonable and codifies the pattern that surfaced SHOULD_FIX-1. **Owner-scope to ratify** the curative addition to `learning/test_class_registry.md` and `learning/curative_additions_log.md` per `project_river_rats_qc.md` operating principle. Surfacing here for owner read; QC will hold pending owner directive.

## Sequencing — what fires next

Per `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` § "Sequencing":

| # | Action | Party | Status / Trigger |
|---|---|---|---|
| 1 | Merge PR #230 (QC verdict record) + PR #228 (Builder design) | Orchestrator | **NOW** (this comm merges) |
| 2 | 12.5J-D-pre dispatch (Option b: tier-2 Δ-tolerance) | LEAD-PROGRAMMER | **fire on this comm merge** (Step 1 below) |
| 3 | QC audit on PR step 2 | QC stream | post-PR-open by orchestrator trigger |
| 4 | 12.5I-MW40-VERIFICATION-B situation generation dispatch | LEAD-PROGRAMMER | post step 2 merge (Hybrid pilot-first clause baked in per resolution above) |

Builder serial. 12.5J-D-pre is engineering scope (test-guard deflake; no poker-judgment overlap with MW-40 work) so it interleaves cleanly between MW-40-A and MW-40-B without coordination overhead.

## LEAD-PROGRAMMER — Step 1: 12.5J-D-pre test-guard deflake (fire on this comm merge)

Per `MAIN_TERMINAL_PR205_MW33_RESOLUTION_2026-05-06.md` § "12.5J-D-pre dispatch queued" (Option b ml-architect-hat default).

Branch: `programmer/phase125j-d-pre-test-guard-deflake-2026-05-06`. Base: master post-this-comm-merge.

### Scope — Option (b): widen tier-2 invariant to Δ-tolerance

Test-guard deflake on the MW-33 RAISE↔BET argmax flip (BLAS reduction-order non-determinism on borderline argmax; gap 0.024 < ~0.05 BLAS-noise threshold per PR #212 memo). Implementation is small + CI-only:

1. **Locate the failing test** — the tier-2 invariant test on MW-33 in `river-rats-core/tests/` (or wherever tier-2 invariants live; check `river-rats-core/tests/test_tier2_invariants.py` or similar). Per memo, this test currently asserts strict `argmax(probs) == BET` on MW-33 inputs and flakes ~20% with RAISE under BLAS reduction-order variance.

2. **Widen the invariant** — replace strict argmax-equality with Δ-tolerance:
   ```python
   # Before (strict):
   assert argmax(probs) == EXPECTED_ACTION
   
   # After (Δ-tolerance):
   sorted_probs = sorted(probs, reverse=True)
   top_gap = sorted_probs[0] - sorted_probs[1]
   if top_gap < 0.05:  # borderline-argmax tolerance
       # Accept either of top-2 actions; both pass
       top_two_actions = top_2_action_indices(probs)
       assert EXPECTED_ACTION in top_two_actions, (
           f"Expected {EXPECTED_ACTION} not in top-2 {top_two_actions} "
           f"(top gap {top_gap:.4f} < 0.05; borderline)"
       )
   else:
       # Above tolerance; strict argmax required
       assert argmax(probs) == EXPECTED_ACTION, (
           f"Expected argmax {EXPECTED_ACTION}, got {argmax(probs)} "
           f"(top gap {top_gap:.4f} ≥ 0.05; non-borderline)"
       )
   ```

3. **Δ-tolerance constant** — define `TIER2_BORDERLINE_ARGMAX_TOLERANCE = 0.05` at module level (or `river-rats-core/test_constants.py` if such a file exists) with a docstring citing PR #212 memo (BLAS reduction-order non-determinism; gap 0.024 observed on MW-33).

4. **Test the deflake** — run the tier-2 invariant test 10 times; verify 0/10 flakes (vs prior ~2/10 baseline). Report flake rate before + after.

5. **Verify no regression on non-borderline MW hands** — run full tier-2 invariant suite on all reference set hands; ensure no hand previously passing strict argmax now fails Δ-tolerance (would only happen if both top-2 don't include EXPECTED_ACTION). Expected: 0 regressions; the tolerance widens the pass criteria, never narrows.

### Stop conditions

- Flake rate after fix > 5% on MW-33 → STOP (tolerance not solving the problem; route to orchestrator for Option c — predictor='cpu_predictor' approach)
- Any non-MW-33 hand passing strict argmax now fails Δ-tolerance → STOP (regression in non-borderline test signal; route to orchestrator)
- Δ-tolerance breaks unrelated tier-2 logic → STOP

### What you do NOT do

- Do NOT widen tolerance beyond 0.05 (that's the BLAS-noise empirical threshold per memo; loosening further hides real regressions)
- Do NOT modify v3.x prompts
- Do NOT modify any model file or training-data file
- Do NOT touch BATCH2 reference
- Do NOT modify `feature_extractor.py` or any feature-side code
- Do NOT add Option (a) MW-33 whitelist as a parallel guard (Option b makes it unnecessary)
- Do NOT add Option (c) `predictor='cpu_predictor'` configuration (separate dispatch if needed; not in scope)

### Cost / time

~$0 (no LLM calls; CI test-guard fix only). ~30-45 min builder time including test runs + report.

### Deliverable scope

Expected files in PR diff:
1. `river-rats-core/tests/test_tier2_invariants.py` (or wherever tier-2 invariants live; locate via grep) — the Δ-tolerance edit
2. `river-rats-core/test_constants.py` (or equivalent) — `TIER2_BORDERLINE_ARGMAX_TOLERANCE = 0.05` constant + docstring — IF a constants file exists; otherwise inline at top of the test file
3. `review/comms/BUILDER_REPORT_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md` — the report:
   - §"Files edited" — exact diff scope
   - §"Δ-tolerance implementation" — code snippet + rationale citing PR #212 memo
   - §"Flake rate before/after" — 10-run table for MW-33 + summary for full suite
   - §"Regression check" — confirm 0 non-borderline regressions
   - §"Stop conditions" — full record (which triggered, which didn't)

### Builder report sections (mandatory)

Same format as 12.5I-D corpus assemble report:
- Headline table (steps + results)
- Stop conditions (full record)
- What I did NOT do (per dispatch)
- What's blocked / what's queued
- References

## QC stream — what you audit (when 12.5J-D-pre PR opens)

Standalone audit, ~10-15 min, 6-item scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — exactly the test file edit + optional constants edit + builder report. No drift outside `river-rats-core/tests/` + `river-rats-core/test_constants.py` (if added) + `review/comms/`.
2. **Δ-tolerance correctness** — verify the 0.05 threshold matches PR #212 memo's empirical BLAS-noise observation (gap 0.024 < threshold; 0.05 is the project policy). Verify the conditional logic: top_gap < 0.05 → top-2 acceptance; top_gap ≥ 0.05 → strict argmax required.
3. **Flake-rate evidence** — verify builder ran 10-run test on MW-33 and reports 0/10 flakes after fix; verify pre-fix flake-rate baseline (~2/10) referenced.
4. **Regression check evidence** — verify full tier-2 invariant suite ran on all reference hands; 0 non-borderline regressions reported.
5. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x prompts, no BATCH2 edits, no `feature_extractor.py` touched, no model/training-data files touched.
6. **TC-X-DISPATCH-COMPLIANCE (provisional, until owner ratifies)** — cross-check builder's implementation against this dispatch's authoritative spec; flag any unilateral deviation as SHOULD_FIX (mirror SHOULD_FIX-1 pattern from PR #228 audit). Specifically: did builder implement Option (b) only, or did they ship Option (a) or (c) hybrid? Prohibitions in §"What you do NOT do" must hold.

QC writes `review/comms/REVIEW_QC_PHASE125J_D_PRE_TEST_GUARD_DEFLAKE_2026-05-06.md` on `qc/pr<N>-jdpre-test-guard-review-2026-05-06`.

## Why no Opus tier-up on 12.5J-D-pre

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: tier-up applies to *labelling* outputs (Sonnet judgments on poker hands). 12.5J-D-pre is engineering scope — CI test-guard fix; no new poker judgments produced, no factory-emitted situations either. Standard QC PASS suffices.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #230 merge (QC verdict record)
- PR #228 merge (Builder MW-40-VERIFICATION-A design)
- 12.5J-D-pre dispatch fires
- SHOULD_FIX-1 resolved (Path 3 Hybrid; binds at 12.5I-MW40-VERIFICATION-B dispatch)

**Newly queued (after 12.5J-D-pre merges):**
- 12.5I-MW40-VERIFICATION-B situation generation dispatch (Hybrid pilot-first clause baked in)
- NIT-1 + NIT-2 fix-forward (folded into 12.5I-MW40-VERIFICATION-B dispatch or next design-comm touch)

**Still queued (later):**
- 12.5I-MW40-VERIFICATION-C labelling round (5 Sonnet × 30 hands; pilot-first per `feedback_pilot_first_for_long_jobs.md` for LLM-uncertainty mitigation)
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo-only PR (depending on graduation outcome)
- 12.5J-C trainer integration test on 61-surface (post-12.5J-D-pre)
- 12.5K combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

**Owner-scope items pending (informational):**
- TC-X-DISPATCH-COMPLIANCE curative addition to `learning/test_class_registry.md` (proposed by QC; orchestrator forwards to owner read)

## References

- PR #228 (Builder MW-40-VERIFICATION-A design): branch `programmer/phase125i-mw40-verification-a-design-2026-05-06`, head `988e39e`
- PR #230 (QC PASS+1SHOULD_FIX+2NIT verdict): branch `qc/pr228-mw40-verification-a-review-2026-05-06`
- PR #229 (QC trigger that fired this audit): master `cec36b4`
- PR #226 (orchestrator: PR #222 merge + MW-40-A dispatch): master `f52a93d`
- PR #212 memo (MW-33 BLAS non-determinism root-cause): master `5da3533`
- PR #205 (12.5J-B feature impl 59→61): master `0b77bdd`
- 12.5J-D-pre Option (b) source: `MAIN_TERMINAL_PR205_MW33_RESOLUTION_2026-05-06.md`
- Memory: `feedback_quality_default_no_ask.md` (slow-quality default; Path 3 Hybrid choice), `feedback_orchestrator_decides_not_recommends.md` (orchestrator resolves SHOULD_FIX-1), `feedback_orchestration_efficiency_rules.md` (single comm covers resolution + merge + dispatch), `feedback_pilot_first_for_long_jobs.md` (sub-rule application: design-phase exempt; labelling-phase required), `feedback_explicit_action_trigger.md` (builder may not auto-fix QC findings)

**Status: PR #228 + PR #230 cleared for merge. SHOULD_FIX-1 resolved via Path 3 Hybrid. LEAD-PROGRAMMER fires 12.5J-D-pre test-guard deflake (Option b) on this comm merge. ~30-45 min wall clock to PR open.**
