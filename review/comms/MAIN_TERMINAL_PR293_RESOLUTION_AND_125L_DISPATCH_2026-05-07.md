---
date: 2026-05-07
from: Main terminal (orchestrator)
to: LEAD-PROGRAMMER · QC stream · Owner (notice + DECISION-PENDING)
re: PR #293 + PR #295 merged (QC PASS; 38th solo cycle; 3-lever ceiling confirmed); ratify NULL outcome on Lever C; dispatch 12.5L gate evaluation (architect-hat synthesis + owner-decision proposal)
status: DIRECTIVE — merges PR #293 + PR #295; fires LEAD-PROGRAMMER on 12.5L synthesis — fire now
---

# PR #293 + PR #295 merge + 12.5L gate evaluation dispatch

QC verdict on PR #293: **PASS**. 38th solo cycle. NULL result confirmed: 988-corpus 5-seed mean **33.00/40 ± 0.00** vs v9-3way-v2.2 baseline **34/40**. **3-lever ceiling empirically established.**

## 12.5K experiment summary (closing)

| Lever | Hypothesis tested | Result | Outcome |
|---|---|---|---|
| A — More seeds (variance) | 5-seed sample too small | 20-seed mean 33.10 ± 0.30 | Variance hypothesis ruled out |
| B — Hyperparameters | 59-surface hypers wrong for 61 | 3-config pilot spread 0.20 hands | Hyperparameter hypothesis ruled out |
| C — Augmented data | 788-row corpus undersized | 988-corpus 5-seed 33.00 ± 0.00 | Augmented-data hypothesis ruled out (minor regression within noise) |

**Conclusion**: v9-3way-v2.2 (34/40 solver-corrected) IS the ceiling for the existing trainer/feature/architecture stack on the available corpus. Further lift requires fundamentally different approach OR acceptance of ceiling.

## LEAD-PROGRAMMER — Step: 12.5L gate evaluation (architect-hat) — fire on this comm merge

Per plan `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` §"Sequencing — what fires after 12.5K-A merges" item 1 ("12.5L gate eval"). Per memory `feedback_orchestrator_decides_not_recommends.md`: orchestrator decides sequencing; owner decides ship-vs-defer.

Branch: `programmer/phase125l-gate-eval-2026-05-07`. Base: master post-this-comm-merge.

### Scope — synthesis comm + owner-decision proposal

This is a SYNTHESIS phase, NOT execution. Builder authors `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md` producing:

1. **Full 12.5K experiment record** — all 3 levers tested with their findings, costs, time, outcomes (mirror table above + add per-lever detail)
2. **Empirical ceiling claim** — v9-3way-v2.2 at 34/40 solver-corrected IS the ceiling for the current stack; cite per-lever evidence
3. **Owner-decision proposal — 3 options minimum**:
   - **Option A: SHIP — accept v9-3way-v2.2 as ceiling.** Lock the 988-corpus + production model; document the 3-lever exhaustion as the empirical case for ceiling acceptance; move to next project phase (multiway 4-way or HU model expansion).
   - **Option B: PURSUE Lever D — different architecture/approach.** Architect-hat exploration of fundamentally different paths (e.g., teacher-student distillation from oracle, transformer-based architecture, meta-learning, broader corpus expansion via untested labelling sources). Cost: undefined; time: weeks.
   - **Option C: ACCEPT CEILING — production model frozen + project moves to other deliverables.** Documents v9-3way-v2.2 as final for HU+3way scope; moves to v9-4way development per the original progressive chain (CLAUDE.md "Progressive model chain").
4. **Cost/time estimates per option**
5. **Risks per option**
6. **Architect-hat recommendation** — single recommendation with reasoning per `feedback_orchestrator_decides_not_recommends.md` (architect recommends; owner decides)
7. **Stay-wrong list final state** — 4 hands (MW-17, MW-40, MW-45, MW-47); 2 are labelling-pipeline-canonical mismatches (MW-17, MW-40); 2 are pipeline-aligned but model-layer-stuck (MW-45, MW-47); document for project memory

### Constraints

- This is the FINAL phase of the 12.5I/J/K workstream
- Synthesis must be comprehensive (touches PR #228 → PR #293 chain)
- Per `feedback_quality_default_no_ask.md`: builder commits to a single recommendation, doesn't surface as menu
- Per `feedback_orchestrator_decides_not_recommends.md`: orchestrator does NOT pre-decide; surfaces synthesis to owner
- Per memory rule (loop directive): orchestrator HOLDS LOOP after -L merges pending owner decision

### What you do NOT do

- Do NOT execute any of the 3 options in this PR (synthesis only)
- Do NOT modify v3.x prompts
- Do NOT modify river-rats-core/ source
- Do NOT modify BATCH2 reference
- Do NOT modify any data file
- Do NOT make the ship-or-defer decision (owner-scope)

### Cost / time

~$0 (synthesis only); ~45-60 min builder wall clock.

### Deliverable scope

1 file: `review/comms/PHASE125L_GATE_EVAL_SYNTHESIS_2026-05-07.md`

## QC stream — what you audit (when 12.5L PR opens)

Standalone audit, ~10-15 min, 7-item synthesis-phase format. Verify:
- All 3 levers documented with empirical findings + costs
- 3 options analyzed with cost/time/risks
- Architect-hat recommendation present (single committed position)
- TC-X-OWNER-SCOPE-DISCIPLINE
- TC-X-DISPATCH-COMPLIANCE 18th formal exercise
- Stay-wrong list final state cited
- Owner-scope decision data complete (no missing material for owner-gate)

QC writes `review/comms/REVIEW_QC_PHASE125L_GATE_EVAL_2026-05-07.md`.

## Sequencing — HARD OWNER-GATE on -L merge

Per loop directive ("Stop the loop only on explicit owner say-so or on a hard owner-gate"):

After 12.5L gate-eval PR #295L merges + QC PASS:
- **ORCHESTRATOR LOOP HOLDS at this point pending owner decision.**
- Owner reads synthesis on session resume; decides Option A/B/C/other.
- Orchestrator resumes loop on owner directive.

This is the natural endpoint of the overnight progression (MW-40 verification → 12.5J neutral → 12.5K 3-lever exhaustion → 12.5L synthesis).

## What's blocked / what's queued

**Cleared by this comm:**
- PR #293 merge (Builder -E corpus integration + retrain; NULL result)
- PR #295 merge (QC verdict record)
- 12.5L synthesis dispatch fires
- 12.5K experiment closed (3-lever ceiling)

**Queued post-12.5L (HARD OWNER-GATE):**
- Option A: ship synthesis + lock production model + project pivot
- Option B: Lever D exploration (architect-hat phase if owner picks)
- Option C: accept ceiling + advance progressive chain to v9-4way

**Owner-scope items pending consolidated for read:**
- TC-X-INTRA-PLAN-CONSISTENCY ratification
- TC-X-DISPATCH-COMPLIANCE ratification (now 17+ exercises)
- TC-X-PLAN-INTERNAL-CONSISTENCY ratification (proposed via PR #237 NIT-3)
- Memory note refresh: "composition quad" vs "composition triple" terminology
- "Structural arguments must cross-check against v3.4 DO NOT rules" standing-rule candidate (from MW-40-VERIFICATION-C HALT)
- "12.5J-E neutral result" memory candidate
- "Pre-flight 4-check does NOT catch domain-specific feature semantics" memory candidate (from PR #277 FD-suit factory bug)
- "MW-17 + MW-40 are labelling-pipeline-canonical mismatches" project memory (closes 2 of 4 stay-wrong)
- "v9-3way-v2.2 is the ceiling for current stack on 988-corpus" project memory (closes 12.5K)

## References

- 12.5K master plan: `review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- Lever C merged plan: `review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md`
- Lever A: PR #261 (master `edf04a6`)
- Lever B: PR #265 (master `d45575b`)
- Lever C 5-phase pipeline: PR #269/#273/#281/#285/#289/#293 sequence
- v9-3way-v2.2 baseline: 34/40 solver-corrected
- 988-corpus result: PR #293 5-seed mean 33.00 ± 0.00
- Memory: `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, loop directive

**Status: PR #293 + PR #295 cleared. 12.5K experiment closed (3-lever ceiling). LEAD-PROGRAMMER fires 12.5L gate-eval synthesis (architect-hat) on this comm merge. ~$0; ~45-60 min wall clock. ORCHESTRATOR LOOP HOLDS at -L QC PASS pending owner decision.**
