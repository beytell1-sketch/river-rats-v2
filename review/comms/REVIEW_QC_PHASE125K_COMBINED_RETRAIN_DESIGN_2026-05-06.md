---
date: 2026-05-06
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #257 — Phase 12.5K combined re-train DESIGN (architect-hat; 3-lever analysis A→B→C; ~$85/~9.5h capped) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 1 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR257_2026-05-06.md (master `2021444`, PR #258)
pr_branch: programmer/phase125k-combined-retrain-design-2026-05-06 (head `0d6...`)
qc_branch: qc/pr257-125k-design-review-2026-05-06
---

# PR #257 — pre-merge QC verdict: PASS (0/0/1)

29th solo cycle. **Strategic design phase audit — gates orchestrator confidence in 12.5K-A execution.** All 7 trigger items PASS. 1 NIT on cost-budget arithmetic (minor; doesn't affect auto-approval threshold). Plan structure sound: 3 levers analyzed, sequenced A→B→C with explicit gates between each, pilot-first per lever with off-ramps, total budget well under auto-approval caps ($85 LLM / ~9-13h wall clock vs $300/30h caps).

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. All 3 levers analyzed (A, B, C) | ✅ PASS |
| 3. Sequenced recommendation present with gates | ✅ PASS |
| 4. Pilot-first gates per lever | ✅ PASS |
| 5. Cost + time budget realistic | ✅ PASS (NIT-1: minor arithmetic) |
| 6. TC-X-OWNER-SCOPE-DISCIPLINE + solver-as-labels prohibition | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (8th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge.** NIT-1 is a minor arithmetic inconsistency; not blocking, doesn't affect auto-approval threshold.

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125k-combined-retrain-design-2026-05-06`:

```
 review/comms/PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md | 298 +++++++++++++++++++++
 1 file changed, 298 insertions(+)
```

Exactly 1 file (the plan). 0 deletions, 0 modifications. No supporting analysis files. Tighter than the trigger's allowance ("1 file + optional supporting analysis"). **PASS.**

Verified NOT touched (perimeter sweep):
- `prompts/gto_labeller_v3.4.md` — 0 changes
- `design/multiway_reference_set/BATCH2_*` — 0 changes
- `river-rats-core/` — 0 changes
- `data/corpus_*.jsonl` — 0 changes
- `training-data/`, model files — 0 changes
- Memory files — 0 changes

Owner-scope perimeter held.

## §2 — All 3 levers analyzed

| Lever | Plan section | Hypothesis | Action | Pilot-first gate | Expected-outcome cases |
|---|---|---|---|---|---|
| A — more seeds (variance characterization) | §3 | True mean is in [33, 34] but small-N (5 seeds) doesn't reveal it; +10 seeds will tighten the estimate | 15 seeds total (5 existing + 10 new) | 7-seed early gate | 3 cases (mean ≥ 34 / matches existing / worse) |
| B — hyperparameter exploration (CV-driven sweep) | §4 | Default hyperparams may be off-optimum; 12-config CV pilot can identify a better config | 12-config grid → best-config × 5 seeds | 12-config CV pilot | 3 cases (significant improvement / minor / no improvement) |
| C — augmented training data (further labelling rounds) | §5 | Under-represented stay-wrong axes (MW-17, MW-45, MW-47) need more parametric labelling rounds analogous to MW-40-VERIFICATION (but successful) | 250-300 hands across 3 axes; 5 Sonnet × 5 pilot per axis; Opus tier-up on canonicals | 5-hand pilot per axis | 3 cases (all 3 align / mixed / all diverge) |

All 3 levers have dedicated analysis section with hypothesis + action + pilot-first gate + expected-outcome enumeration + slow-quality assessment. **PASS.**

## §3 — Sequenced recommendation with gates

Plan §6 explicitly proposes **A → B → C with gates between each**:

> **Recommended sequence: A → B → C, with explicit gates between each lever.**

Reasoning per lever ordering (§6 lines 196-225):
- **A first**: cheap (~90 min CPU; $0), fast, informative — most ROI per unit cost
- **B second**: moderately expensive (~6h pilot; $0); methodologically sound but should fire AFTER A confirms variance bound
- **C last**: most expensive (~$80; ~3.5-5.5h); addresses root cause but most risky (could replicate MW-40 verification's negative finding)

Gates between levers documented as off-ramp criteria per lever pilot. **PASS.**

## §4 — Pilot-first gates per lever

Per `feedback_pilot_first_for_long_jobs.md` and dispatch §"Pilot-first gates":

| Lever | Pilot scope | Gate criterion | Off-ramp |
|---|---|---|---|
| A | 5+2 seeds (early gate at 7) | Mean ≥ 33.0/40 with consistent std | Mean < 32.5 OR std > 1.0 → STOP, route to orchestrator |
| B | 12-config grid × 5 seeds | Best pilot config CV ≥ existing CV by ≥1 hand | Best pilot CV ≤ existing → STOP, conclude defaults near-optimal |
| C | 5-hand pilot × 5 Sonnet per axis | ≥4/5 hands consensus aligned with structural prediction | Consensus diverges → REPORT (mirror of MW-40-VERIFICATION-C HALT) |

All 3 levers have explicit pilot-first scope with quantitative gate criteria + off-ramp routing to orchestrator. **PASS.**

This is the third major use of the Hybrid pilot-first pattern (per PR #228 SHOULD_FIX-1 Path 3 resolution + PR #232 12.5J-D-pre + PR #253 12.5J-E). The pattern is now standard discipline across 12.5K's design.

## §5 — Cost + time budget realistic

Per-lever cost table (plan §7 lines 234-239):

| Lever | Pilot cost | Pilot wall | Full cost | Full wall | Subtotal |
|---|---|---|---|---|---|
| A | ~$0 | (early-gate at 7 seeds) | ~$0 | ~90 min (15 seeds × 6 min) | ~$0 / ~1.5h |
| B | ~$0 | ~6h (12 configs × 5 seeds) | ~$0 | ~30h (full grid OR best-config × 5 seeds) | ~$0 / 6-36h |
| C | ~$5 (15-hand pilot) | ~30 min | ~$80 (250-300 × 5 + 15 Opus) | ~3-5h | ~$80 / ~3.5-5.5h |
| **Total at recommended cap (B-pilot-only)** | — | — | — | — | **~$85 / ~9.5-13h** |

Auto-approval caps: $300 LLM / 30h wall clock. **Plan total $85 ≪ $300; capped wall clock 9.5-13h ≪ 30h. Both well within auto-approval.** **PASS.**

### NIT-1 (audit item 5: arithmetic precision)

The plan claims "9.5 hours" cap (§7 line 247: "This caps total wall clock at ~9.5 hours (A + B-pilot-only + C)") but the per-lever sub-totals at the recommended cap-strategy don't quite sum to 9.5h:

- A full: ~1.5h (90 min CPU per §3; per-seed 6 min × 15 seeds)
- B pilot-only: ~6h (per §4; 12 configs × 5 seeds × 6 min)
- C full: ~3.5-5.5h (per §5; design + situation gen + labelling + Opus tier-up + report)
- **Sum: ~11-13h** (not 9.5h)

The 9.5h figure also appears in §7 line 239 as the lower bound of "fail-path" total ($85 / 9.5-41.5h) — that interpretation requires each lever to run only its pilot before failing out, which would sum to 0.5h (A pilot via early gate) + 6h (B pilot) + 0.5h (C pilot) = ~7h, still not 9.5h.

The 9.5h figure is approximate / rounded / using a specific scenario interpretation that isn't clearly mapped to the per-lever table. **Doesn't affect auto-approval (any interpretation is well under 30h cap)**, but worth surfacing for clean accounting.

**Suggested resolution (orchestrator-scope per `feedback_orchestrator_decides_not_recommends.md`):**
- (a) Builder amends §7 to clarify the 9.5h derivation (e.g., specific scenario breakdown), OR
- (b) Builder updates the figure to the actually-summed range (e.g., "~7-13h depending on lever exit points"), OR
- (c) Orchestrator accepts the approximation as adequate (within order-of-magnitude correctness; auto-approval threshold not affected)

QC has no preference. Surfaced for orchestrator decision.

## §6 — Owner-scope discipline + solver-as-labels prohibition

Plan §9 "What this PR does NOT do" enumerates prohibitions:

- Plan does NOT recommend training against reference set ✓
- Plan does NOT propose solver-as-labels for any new labelling round ✓ (Lever C uses Sonnet/Opus on parametric variants; same pipeline as MW-40-VERIFICATION-C)
- Plan does NOT propose BATCH2/v3.x edits ✓
- Reference-set labels treated as IMMUTABLE ground truth (not training target) ✓

§5 sub-axis MW-40 explicitly notes "Already verified (graduation-fail; do NOT re-label)" — preserves the verification-round outcome. **PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (8th formal exercise)

| Compliance check | Spec | Observation | Match |
|---|---|---|---|
| Design-only (no execution) | dispatch §"Scope" | 1 plan file; 0 code; 0 model artifacts | ✅ |
| 1 file in PR (+ optional analysis) | dispatch §"Deliverable scope" | exactly 1 file | ✅ |
| Methodology rules cited | dispatch + plan precedents | cross-seed importance (§3 + §4 reporting), cap-binding pre-flight (referenced via §5 corpus assemble), tier-up verification (§5 Opus tier-up plan), pilot-first plan (all 3 levers), pre-flight join-cardinality (§5 Lever C corpus assemble) | ✅ |
| Stop conditions per dispatch | dispatch §"Stop conditions" | §8 Stop conditions enumerates dispatch's STOP triggers + verification | ✅ |
| "What this PR does NOT do" section | dispatch + memory | §9 enumeration | ✅ |
| Risks + open questions for orchestrator | `feedback_orchestrator_decides_not_recommends.md` | §10 Risks + open questions table | ✅ |

Per `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`: builder discipline matches dispatch authoritative wording. **PASS.**

TC-X-DISPATCH-COMPLIANCE class continues to validate as durable on 8th formal exercise.

## §"Stop conditions" — design-phase

Per dispatch §"Stop conditions" + plan §8:
- ❌ Plan addresses fewer than 3 levers → §3-§5 each address one lever
- ❌ Plan does not propose sequenced recommendation → §6 explicit A→B→C with gates
- ❌ Any lever lacks pilot-first plan → §3-§5 all have pilot-first scope + gates
- ❌ Plan total budget exceeds caps → ~$85 / ~9.5-13h (well under $300/30h)

## TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

Quick cross-check for plan-internal contradictions:

| Rule pair | Joint domain | Satisfiable? |
|---|---|---|
| §3 Lever A (15 seeds) ∧ §6 sequence (A first) | A runs fully before B; gate after A | ✅ Consistent |
| §4 Lever B (full grid 30h) ∧ §7 cap (B-pilot-only) | B is capped at 12-config pilot unless explicit orch approval | ✅ Resolved via §7 cap |
| §5 Lever C (250-300 hands) ∧ pre-flight join-cardinality | New parametric corpus joins existing 788; namespace disjoint | ✅ Plan §5 specifies disjoint `MW-XX-VERIFICATION_*` namespaces |
| §5 Lever C (3 axes) ∧ stay-wrong list (4 hands) | MW-40 already verified (graduation-fail; excluded) | ✅ §5 explicitly excludes MW-40 |
| §10 R1 Lever B unbounded grid ∧ §7 cap recommendation | Cap is the recommendation; full grid requires explicit orch approval | ✅ Documented in §10 R1 |

No new contradictions surfaced. Plan §4 contradiction pattern from PR #228 not repeated here. **PASS.**

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (10th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (8th formal exercise; clean PASS)** — class continues to validate as durable
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; explicit cross-check on lever pair joint domains; no contradictions)
- TC-X-METHODOLOGY-RULE-CROSSCHECK (sub-class; all 6 standing methodology rules verified present in plan)

## Smarter-over-time observations

**12.5K design absorbed lessons from MW-40 verification cycle:**

- Pilot-first per lever (per `feedback_pilot_first_for_long_jobs.md` + Hybrid Path 3 from PR #228 SHOULD_FIX-1) — applied uniformly across all 3 levers
- Off-ramp at any failed lever — addresses the curative-class observation that strategic design plans need quantitative gate criteria for early-exit (entry #13 motivating evidence)
- Lever C explicit acknowledgement of MW-40 graduation-fail risk — references the labelling-pipeline-routing-dominates-over-structural-arguments finding from PR #249's -E memo
- Cost-budget transparency with auto-approval thresholds — addresses the curative system's "explicit budget" preference

The QC class system established during the MW-40 verification round is now informing builder design discipline at strategic-planning scale. **The class system is influencing both audit verdicts AND upstream design.**

## Audit cost / time

- Wall clock: ~13 min (plan read + structure verification + cost arithmetic check + dispatch cross-check + verdict authoring). Within 10-15 min estimate.
- LLM cost: $0.

## Gates

PR #257 cleared from QC side. Per dispatch §"What gates on this audit":

- **PR #257 merge:** clear from QC (NIT-1 is non-blocking; orchestrator decides resolution at convenience)
- **12.5K-A execution dispatch** (Lever A more-seeds first) → on PR #257 merge
- Subsequent **12.5K-B / -C execution** → each fires on prior lever's gate per builder's plan
- **12.5L gate evaluation** → on full 12.5K sweep complete

No QC-side blocker.

## References

- 12.5K design dispatch: `MAIN_TERMINAL_PR253_RESOLUTION_AND_125K_DESIGN_DISPATCH_2026-05-06.md` (master `4e55ff4`, PR #256)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR257_2026-05-06.md` (master `2021444`, PR #258)
- Plan: `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md` (in PR #257; 298 lines)
- 12.5J-E source: `BUILDER_REPORT_PHASE125J_E_SMALL_SAMPLE_RETRAIN_2026-05-06.md` (master via PR #253)
- MW-40 verification cycle: PR #228 (plan) / PR #236 (situation gen) / PR #241 (pilot HALT) / PR #245 (Opus tier-up) / PR #249 (-E memo)
- 12.5I-A design precedent: `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md` (master `e0e0304`, PR #228)
- v9-3way-v2.2 baseline (34/40 solver-corrected): CLAUDE.md project state
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entries #11/#12/#13/#14 (cited by builder design discipline)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_vs_expert_labels.md`, `feedback_explicit_action_trigger.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_listen_to_orchestrator_always.md`

**Status: VERDICT = PASS. PR #257 cleared for merge from QC side. Strategic design well-structured (3 levers, sequenced A→B→C, pilot-first per lever, off-ramps). NIT-1 minor arithmetic inconsistency on cost-budget summary; non-blocking. 29th solo QC cycle. TC-X-DISPATCH-COMPLIANCE 8th formal exercise; class durable.**
