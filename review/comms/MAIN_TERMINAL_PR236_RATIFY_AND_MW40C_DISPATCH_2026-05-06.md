---
date: 2026-05-06
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice)
re: PR #236 PASS+1SHOULD_FIX+0NIT acknowledged → resolve SHOULD_FIX-1 via Path 1 (Ratify "J-medium" = "J-on-board with low secondaries"); merge PR #236 + PR #239; dispatch 12.5I-MW40-VERIFICATION-C labelling round (5 Sonnet × 30; pilot-first 5-hand gate)
status: DIRECTIVE — merges PR #236 + PR #239; ratifies SHOULD_FIX-1; fires LEAD-PROGRAMMER on -C labelling — fire now
---

# PR #236 + PR #239 merge + SHOULD_FIX-1 ratification + 12.5I-MW40-VERIFICATION-C dispatch

QC verdict on PR #236 (`REVIEW_QC_PHASE125I_MW40_VERIFICATION_B_SITUATION_GEN_2026-05-06.md` on `qc/pr236-mw40-verification-b-review-2026-05-06`, PR #239): **PASS — 0 BLOCKER, 1 SHOULD_FIX, 0 NIT (24th solo cycle).** SHOULD_FIX-1 is a dispatch-internal terminology contradiction surfaced by QC's TC-X-INTRA-PLAN-CONSISTENCY (1st informal activation; class added curative entry #13). Builder behavior was clean PASS (TC-X-DISPATCH-COMPLIANCE 3rd exercise PASS); the contradiction was in MY (orchestrator's) PR #237 amendment text, not in builder's implementation. Path γ' compliance + 4-check pre-flight + Step-18 prediction (0/30 each as predicted) + ref_id namespace + schema integrity all PASS.

## SHOULD_FIX-1 ratification — Path 1

QC offered three resolution paths:
1. **Ratify** "J-medium" = "J-on-board with low secondaries" (terminology drift; consistent with Plan §10 R3 ratification pattern)
2. **Amend** plan: builder authors -B2 PR replacing 15 sub-axis C boards with J-as-middle-card (`AhJc5d`-class)
3. **Hybrid**: keep 10 inherited + replace 5 additional with J-as-middle

Per `feedback_quality_default_no_ask.md` + `feedback_orchestrator_decides_not_recommends.md`. Slow-quality + orchestrator-decides analysis:

### Decision 3β (PR #217 source) literal text

> "design ~30 J-on-board parametric variants targeting MW-40 axis... Predicted v3.4 output: CHECK"

Decision 3β scoped the verification target as **"J-on-board parametric variants"** generically — not "J-as-middle-card-by-rank specifically." The PR #237 amendment's "J as middle card on flop" terminology was over-specification, drift from the original Decision 3β scope.

### Plan inheritance binding

Plan §4 listed 10 specific sub-axis C boards (`Jh5c2d, Jc8h3s, Jd9c4h, Jh6s3c, Jc7d2s, Jd8c5h, Jh4c2s, Jc9h6d, Jd7h3c, JcJh4s`) as the canonical reference for sub-axis C. All 10 are J-as-highest with low secondaries. The plan was merged at PR #228 with QC PASS. Re-litigating the plan-inherited boards now would violate the plan's authority and require a deeper amendment than this verification round warrants.

### Ratification rationale

**Decision: Path 1.**

"J-medium" in plan §4 + PR #237 amendment is ratified as informal terminology meaning **"J-on-board with low secondaries (J + 2 cards both lower than J in rank)."** The 15 sub-axis C boards (10 inherited + 5 additional, all J-as-highest with low secondaries) ARE J-on-board parametric variants targeting MW-40 axis per Decision 3β scope.

The verification's primary structural claim — "J-on-board flips composition triple toward CHECK on TPMK T-kicker 4-way checked-through" — is exercised by all 30 boards (15 sub-axis A J-high-flop + 15 sub-axis C J-medium-as-defined). If at -C labelling 27/30 of these J-on-board boards consensus to CHECK, the structural prediction holds at the J-on-board generic level → MW-40 graduates per Decision 3β.

If a future verification round needs the strict J-as-middle-card-by-rank canonical mirror (overcard + J-middle + low; the precise BATCH2 MW-40 reference structure on `AhTs` / `AJ5r`), that's a follow-up phase candidate AFTER this round's outcome. NOT in scope for this round.

### Why this is not Path 2 or Path 3

- Path 2 (full amend; 15 J-as-middle replacements): would re-litigate the plan-inheritance binding; adds churn (~15-20 min builder + new -B2 audit cycle) for refinement that goes BEYOND Decision 3β's literal scope ("J-on-board" generic). Slow-quality default is to test the literal Decision 3β scope first; refine only if results demand it.
- Path 3 (hybrid; 10 J-highest + 5 J-middle): introduces character-mixing within sub-axis C that confounds per-axis CHECK-consensus measurement at -C. Quality-degrading, not quality-improving.

Path 1 ratification is the cleanest minimum-deviation path that preserves both Decision 3β's literal scope AND the plan-inheritance binding.

### Memory drift acknowledgment

Plan §10 R3 already flagged "composition quad" (v3.4 prompt) vs "composition triple" (memory note `feedback_preflop_geometry_vs_postflop_composition.md`) terminology drift. PR #237's "J as middle card" was a similar drift (informal label vs literal positional terminology). This ratification handles the second drift the same way: ratify the informal label as project terminology; the literal-positional interpretation is NOT in scope for this round.

**NIT-3 carry-forward (from PR #237 amendment):** terminology cross-checks before merge are now elevated from "nice to have" to "active mitigation" via QC's TC-X-INTRA-PLAN-CONSISTENCY class (informal). This ratification IS the live application of that class to a surfaced contradiction.

## Sequencing — what fires next

| # | Action | Party | Status / Trigger |
|---|---|---|---|
| 1 | Merge PR #239 (QC verdict record) + PR #236 (Builder situation gen) | Orchestrator | **NOW** (this comm merges) |
| 2 | 12.5I-MW40-VERIFICATION-C labelling round dispatch | LEAD-PROGRAMMER | **fire on this comm merge** (Step 1 below) |
| 3 | QC audit on PR step 2 | QC stream | post-PR-open by orchestrator trigger |
| 4 | 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision | LEAD-PROGRAMMER + Opus tier-up subprocess | post-step-2 QC PASS |

Builder serial. 12.5J-C trainer integration test on 61-surface (queued earlier; non-blocking) interleaves at orchestrator's discretion.

## LEAD-PROGRAMMER — Step: 12.5I-MW40-VERIFICATION-C labelling round (fire on this comm merge)

Per `MAIN_TERMINAL_PR222_MERGE_AND_MW40A_DISPATCH_2026-05-06.md` § "Sequencing" + 12.5I-C precedent (`MAIN_TERMINAL_PHASE125I_C_DISPATCH_2026-05-06.md`).

Branch: `programmer/phase125i-mw40-verification-c-labelling-2026-05-06`. Base: master post-this-comm-merge.

### Scope — 5 Sonnet labellers × 30 J-on-board variants (post-Path γ' ratified)

Same labelling pattern as 12.5I-C: 5 independent Sonnet labellers × 30 hands × v3.4 prompt. Pilot-first 5-hand gate. Source corpus: `data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` (PR #236-merged; 30 ref_ids `PILOT_MW40_VERIF_001..030`).

### Pilot-first 5-hand gate (binding per `feedback_pilot_first_for_long_jobs.md`)

This is the LLM-uncertainty pilot-first (different from -B's Hybrid factory pre-flight). Standard 12.5I-C pattern:

1. **Pilot batch**: emit 5 hands × 5 Sonnet labellers = 25 individual labels (~$1-2 LLM cost; 5-10 min wall clock)
2. **Pilot gate**: examine pilot consensus before scaling. Per `feedback_pilot_first_for_long_jobs.md`:
   - If pilot consensus is CHECK with ≥4/5 majority on most pilot hands → proceed to full 30-hand × 5-labeller run
   - If pilot consensus is BET-mixed or RAISE-mixed (contradicts the structural prediction) → STOP and report to orchestrator (potential graduation-fail signal at scale; orchestrator decides whether to scale anyway for completeness or halt verification)
   - If pilot has split-strategy patterns specifically on the J-paired sub-axis C boundary case (`JcJh4s`) → REPORT but proceed (may be a sub-axis-specific signal worth quantifying at full scale)
3. **Full run** (after gate clear): emit remaining 25 hands × 5 labellers = 125 additional labels. Total ~$5-10 LLM cost.

### Pick the 5 pilot hands

Builder selects 5 from the 30 emitted situations. Recommended distribution:
- 2 from sub-axis A J-high flops (different parametric variants)
- 2 from sub-axis C J-on-board boards (1 standard + 1 from the 5 builder-added during -B)
- 1 from the boundary `JcJh4s` paired-J variant in sub-axis C (the most exotic structural test case)

Builder picks specific hands at builder discretion within these constraints. Document selection in builder report.

### Labelling prompt

`prompts/gto_labeller_v3.4.md` (current production prompt; locked). Same prompt used in 12.5I-C labelling round. Sonnet-only at this phase; Opus tier-up is at -D.

### Stop conditions

- Pilot consensus is BET-mixed or RAISE-mixed (≥3/5 hands have <3/5 CHECK) → STOP and report to orchestrator
- Pilot has unexplained mode collapse (5/5 labellers identical labels with low confidence stamps) → STOP (suggests a labelling pipeline degenerate state)
- Sonnet API errors >5% on the pilot run → STOP (infrastructure issue; orchestrator decides retry vs investigate)
- Solver-as-labels appears (per `feedback_solver_vs_expert_labels.md`) → STOP
- Any labels modified after emission → STOP (immutability rule)
- Schema-mismatch between corpus input and label output → STOP

### What you do NOT do

- Do NOT modify v3.x prompts (`prompts/gto_labeller_v3.4.md`)
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference (orchestrator-scope; locked until -E)
- Do NOT modify the merged plan or PR #236 corpus
- Do NOT run Opus at this phase (Opus tier-up is at -D)
- Do NOT skip the pilot-first 5-hand gate (binding per `feedback_pilot_first_for_long_jobs.md`)
- Do NOT auto-fix any borderline pilot result (route to orchestrator per `feedback_optional_is_not_authorized.md`)

### Cost / time

- Pilot batch: ~$1-2 LLM; ~5-10 min wall clock
- Full run: ~$5-10 LLM; ~25-35 min wall clock
- Total: ~$6-12; ~30-45 min builder wall clock including pilot gate + report

### Deliverable scope

Expected files in PR diff:
1. `data/corpus_revision_125i_mw40_verif_labels_2026-05-06.jsonl` (30 hands × 5 labels = 150 label records; or per-hand consensus rows depending on builder's preferred format consistent with prior 12.5I-C output structure)
2. `scripts/run_125i_mw40_verif_labelling.py` (orchestration script; mirrors prior labelling-round scripts)
3. `review/comms/BUILDER_REPORT_PHASE125I_MW40_VERIFICATION_C_LABELLING_2026-05-06.md` (the report)
4. Optionally raw per-labeller intermediates if useful for QC (within 5MB total to keep PR size manageable)

### Builder report sections (mandatory)

- §"Pilot batch results" — 5 hands × 5 labellers; per-hand consensus + confidence; gate decision
- §"Full run results" — 30 hands × 5 labellers; per-hand consensus + confidence
- §"Per-sub-axis CHECK consensus" — sub-axis A (15 hands) + sub-axis C (15 hands; including 1 paired-J boundary)
- §"Aggregate CHECK consensus" — total CHECK / 30 + total non-CHECK / 30; comparison vs Decision 3β graduation threshold (≥27/30 → MW-40 graduates)
- §"Confidence distribution" — 1.0 (5/5) vs 0.8 (4/1) vs 0.6 (3/2) vs lower
- §"Borderline + outlier hands" — any hand with <3/5 CHECK; flagged for -D Opus tier-up consideration
- §"Stop conditions" — full record (which triggered, which didn't)

### Per `feedback_pilot_first_for_long_jobs.md` sub-rule (training-data outputs)

The labels produced at -C are training-data outputs (Sonnet poker judgments). Per the sub-rule: tier-up verification (Sonnet → Opus cross-check) is required at -D before any of these labels are used as training data. -D is a separate dispatch on -C QC PASS. -C does NOT feed labels to a trainer; it only produces the consensus measurement for the graduation decision.

## QC stream — what you audit (when 12.5I-MW40-VERIFICATION-C PR opens)

Standalone audit, ~10-15 min, 8-item scope:

1. **Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE)** — labels jsonl + script + report. NO touch to v3.x prompts, BATCH2, river-rats-core/, training-data, existing corpora, plan, memory.
2. **Pilot-first compliance** — verify builder ran pilot batch FIRST, gate-checked, then proceeded to full run. Builder report must show pilot evidence and gate decision.
3. **Row count integrity** — 30 hands × 5 labellers = 150 individual labels (or 30 consensus rows depending on output format); 0 duplicates; 0 hand-skips.
4. **Per-hand consensus computation** — verify majority-vote logic; verify confidence stamps (1.0 / 0.8 / 0.6 / lower) match the per-hand split.
5. **Schema integrity** — labels schema matches prior 12.5I-C output format (per `corpus_revision_125i_labels_2026-05-06.jsonl` precedent).
6. **TC-X-OWNER-SCOPE-DISCIPLINE** — confirm no v3.x / BATCH2 / core / corpus / plan / memory edits.
7. **TC-X-DISPATCH-COMPLIANCE (4th formal exercise)** — pilot-first ran exactly as specified; Sonnet-only (no Opus); 5 pilot hands matched the recommended distribution OR builder documented divergence with reasoning.
8. **TC-X-INTRA-PLAN-CONSISTENCY (informal class continuation)** — if any new dispatch-internal contradictions surfaced during -C, flag.

QC writes `review/comms/REVIEW_QC_PHASE125I_MW40_VERIFICATION_C_LABELLING_2026-05-06.md` on `qc/pr<N>-mw40-verification-c-review-2026-05-06`.

## Why no Opus tier-up on -C

Per `feedback_pilot_first_for_long_jobs.md` sub-rule: -C produces Sonnet judgments. Opus tier-up runs at -D on canonical hands selected from -C output (mirrors PR #209 + PR #213 + 12.5I-C pattern). -C QC PASS gates on the labelling-round-quality (pilot ran; consensus computed; schema clean), not on label correctness vs solver/oracle.

## What's blocked / what's queued

**Cleared by this comm:**
- PR #236 merge (Builder situation generation)
- PR #239 merge (QC verdict record)
- 12.5I-MW40-VERIFICATION-C dispatch fires
- SHOULD_FIX-1 ratified (terminology drift; "J-medium" = "J-on-board with low secondaries")

**Newly queued (after -C merges):**
- 12.5I-MW40-VERIFICATION-D Opus tier-up + graduation decision
- 12.5I-MW40-VERIFICATION-E BATCH2 reference update OR memo-only PR (NIT-1, NIT-2, NIT-3 bind)

**Still queued (later):**
- 12.5J-C trainer integration test on 61-surface (parallel queue; non-blocking)
- 12.5K combined re-train (gates on 12.5I-MW40-VERIFICATION-E + 12.5J-E ship)
- 12.5L gate eval (gates on 12.5K)

**Owner-scope items pending (informational, non-blocking):**
- TC-X-DISPATCH-COMPLIANCE curative addition to `learning/test_class_registry.md` (3 successful exercises now: PR #228 SHOULD_FIX-1, PR #232 clean PASS, PR #236 SHOULD_FIX-1 surfaced via TC-X-INTRA-PLAN-CONSISTENCY first activation)
- TC-X-INTRA-PLAN-CONSISTENCY curative addition to `learning/test_class_registry.md` (1st formal activation surfaced real contradiction in PR #237 amendment text; QC entry #13 in curative log)
- Owner ratifies-or-declines both proposed classes at convenience

## References

- PR #236 (Builder MW-40-VERIFICATION-B; 30 J-on-board variants): branch `programmer/phase125i-mw40-verification-b-situation-gen-2026-05-06`, head `58ac0d6`
- PR #239 (QC PASS+1SHOULD_FIX+0NIT verdict): branch `qc/pr236-mw40-verification-b-review-2026-05-06`
- PR #238 (QC trigger that fired this audit): master `3693ab4`
- PR #237 (orchestrator: PR #236 HALT resolved Path γ'; the source of SHOULD_FIX-1 terminology drift): master `42460ae`
- PR #228 (Plan with §4 J-medium boards; ratified by this comm as "J-on-board low-secondaries"): master `e0e0304`
- PR #217 (Decision 3β source; "J-on-board parametric variants" literal scope): master `d6912ad`
- 12.5I-C labelling precedent: `MAIN_TERMINAL_PHASE125I_C_DISPATCH_2026-05-06.md`
- Memory: `feedback_quality_default_no_ask.md` (slow-quality default; Path 1 ratification choice), `feedback_orchestrator_decides_not_recommends.md` (orchestrator resolves SHOULD_FIX-1), `feedback_pilot_first_for_long_jobs.md` (pilot-first 5-hand gate at -C; tier-up at -D), `feedback_orchestration_efficiency_rules.md` (single comm: ratification + merge + dispatch), `feedback_solver_vs_expert_labels.md` (no solver-as-labels), `feedback_orchestrator_controls_parallel_timing.md`

**Status: PR #236 + PR #239 cleared for merge. SHOULD_FIX-1 ratified via Path 1 (J-medium = J-on-board low-secondaries; terminology drift). LEAD-PROGRAMMER fires 12.5I-MW40-VERIFICATION-C labelling round (5 Sonnet × 30; pilot-first 5-hand gate) on this comm merge. ~30-45 min wall clock + ~$6-12 LLM to PR open.**
