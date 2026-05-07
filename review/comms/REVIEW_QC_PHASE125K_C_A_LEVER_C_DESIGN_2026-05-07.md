---
date: 2026-05-07
from: QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner (notice)
re: PR #269 — Phase 12.5K-C-A Lever C design (4-axis augmented data; per-axis pilot-first + off-ramp; ~$65-100 / ~4-6h capped) — pre-merge audit
status: VERDICT — PASS; 0 BLOCKER, 0 SHOULD_FIX, 0 NIT
trigger: MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR269_2026-05-07.md (master `b359505`, PR #270)
pr_branch: programmer/phase125k-c-a-augmented-data-design-2026-05-07
qc_branch: qc/pr269-125kca-design-review-2026-05-07
---

# PR #269 — pre-merge QC verdict: PASS (0/0/0)

32nd solo cycle. **Lever C design plan; 4-axis augmented data labelling round.** All 7 audit items PASS. Plan structure sound: 5-phase mini-pipeline (A→B→C→D→E) mirroring 12.5I-MW40-VERIFICATION precedent; per-axis pilot-first 5-hand gates with off-ramps; per-axis structural predictions align with stay-wrong canonical/solver-corrected labels; total budget $65-100 LLM / 4-6h wall clock well under $300/30h auto-approval caps.

## Headline

| Audit item | Result |
|---|---|
| 1. Diff scope strict (TC-23 + TC-X-OWNER-SCOPE-DISCIPLINE) | ✅ PASS |
| 2. All 4 stay-wrong axes covered (MW-17, MW-40, MW-45, MW-47) | ✅ PASS |
| 3. Per-axis pilot-first 5-hand gate specified | ✅ PASS |
| 4. Per-axis structural prediction documented | ✅ PASS |
| 5. Methodology rules cited (7 standing) | ✅ PASS |
| 6. TC-X-OWNER-SCOPE-DISCIPLINE | ✅ PASS |
| 7. TC-X-DISPATCH-COMPLIANCE (11th formal exercise) | ✅ PASS |

**Verdict: PASS — clear to merge. Lever C-A design ready; orchestrator dispatches Lever C-B (situation gen) on PR merge.**

## §1 — Diff scope strict

`git diff --stat master...origin/programmer/phase125k-c-a-augmented-data-design-2026-05-07`:

```
 review/comms/PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md | 263 +++++
 1 file changed, 263 insertions(+)
```

Exactly 1 file (the plan). No optional analysis files. 0 deletions, 0 modifications. **PASS.**

Verified NOT touched:
- `prompts/` (v3.x) — 0 changes
- `design/multiway_reference_set/BATCH2_*` — 0 changes
- `river-rats-core/` — 0 changes
- `data/corpus_*.jsonl` — 0 changes
- `training-data/`, model files, memory files — 0 changes

Owner-scope perimeter held.

## §2 — All 4 stay-wrong axes covered

Per dispatch §"Per-axis structural specifications":

| Axis | Stay-wrong canonical | Plan §3 prediction | Match |
|---|---|---|---|
| MW-17 (under-calling on low-equity nut FD facing CO bet 3-way) | CALL (raw + solver-corrected) | CALL consensus | ✅ |
| MW-40 (residual passive BET MEDIUM thin value 4-way checked-through) | BET (BATCH2 canonical post-graduation-fail) | BET consensus | ✅ |
| MW-45 (under-raising slowplay-set on broadway-completed turn) | RAISE | RAISE consensus | ✅ |
| MW-47 (shared blind spot nut FD+OESD facing bet+call) | CALL raw → RAISE solver-corrected | RAISE consensus | ✅ |

All 4 stay-wrong axes covered with structural predictions aligned to canonical/solver-corrected labels. **PASS.**

## §3 — Per-axis pilot-first 5-hand gate specified

Plan §4 explicitly specifies per-axis pilot-first gates per dispatch §"Per-axis pilot-first 5-hand gate":

| Pilot gate criterion | Continue if | Off-ramp if |
|---|---|---|
| Pilot consensus aligns with structural prediction | ≥4/5 hands consensus on predicted action | <4/5 → REPORT to orchestrator (mirror MW-40-VERIFICATION-C HALT pattern) |

**Per-axis off-ramp** documented: if axis fails pilot, that axis is dropped from Lever C; remaining axes proceed with partial scale. Pre-emptive note (R3) acknowledges that the labelling pipeline can diverge from structural arguments (proven at MW-40-VERIFICATION); the off-ramp builds graceful handling into the design.

**PASS.**

## §4 — Per-axis structural prediction documented

Each axis includes hypothesis + reasoning + sub-axis decomposition + variant counts. Predictions align with PR #245 finding (MW-40 BET MEDIUM is the labelling-pipeline-empirical answer, NOT CHECK):

- MW-17 prediction CALL: "labelling pipeline produces CALL consensus because [low-equity nut FD facing CO bet 3-way → call equity vs pot odds]"
- MW-40 prediction BET: "labelling pipeline produces BET consensus because [TPMK T-kicker + 4-way checked-through + IP non-PFA]" — directly cites PR #245's empirical finding (Sonnet 25/25 + Opus 5/5 = 30/30 BET)
- MW-45 prediction RAISE: "labelling pipeline produces RAISE consensus because [slowplay-set + broadway-completed turn + facing-lead]"
- MW-47 prediction RAISE: "labelling pipeline produces RAISE consensus because [nut FD + multiway + facing bet+call]"

All predictions cite specific structural arguments backed by per-axis sub-axis decomposition. **PASS.**

### Notable: MW-40 axis cost-saving observation (architect-hat note)

Plan §3 MW-40 + §5 "MW-40 axis special case" surfaces a smart cost-saving observation:

> Re-use the 30 already-labelled MW-40-VERIFICATION-B hands (`data/corpus_revision_125i_mw40_verif_situations_2026-05-06.jsonl` PILOT_MW40_VERIF_001..030) + 20 fresh parametric variants `PILOT_LEVER_C_MW40_031..050`. Total 50 hands for MW-40 axis. **Saves ~$30 LLM + ~30 min on this axis** (the existing 30 are already labelled BET 25/25 Sonnet + 5/5 Opus; no need to re-label).

This is a sound architect-hat recommendation: the existing 30 MW-40-VERIFICATION hands have full multi-source consensus (PR #241 + PR #245). Re-labelling would be redundant and costly. Pilot 5 hands of MW-40 axis treated as smoke-test (expected 5/5 BET; reproduces existing consensus).

**This is a positive design choice surfaced for orchestrator-level approval.** QC has no preference — orchestrator decides whether to ratify the cost-saving or require fresh re-labelling for cleanroom independence.

## §5 — Methodology rules cited

Plan §6 lists the 7 standing methodology rules per 12.5I-A precedent:

| # | Rule | Application |
|---|---|---|
| 1 | Hero-only convention in `prior_actions` | Per-axis factory spec (§5) |
| 2 | Pre-flight join-cardinality | Per-axis 50-hand exact count; 0 over/under |
| 3 | `design_action` field per hand for T-CONTROL-like rows | Per-axis prediction (CALL/BET/RAISE/RAISE) |
| 4 | Pilot-first does NOT apply at -B (deterministic factory) | Inherited; Hybrid pre-flight on first 5 per axis (mirrors PR #228 SHOULD_FIX-1 Path 3) |
| 5 | Pilot-first DOES apply at -C (labelling round) | Per-axis 5-hand × 5-labeller pilot; per-axis off-ramp |
| 6 | Solver-as-labels prohibited | Solver may verify per-axis predictions OR canonical references at -D Opus tier-up; never as labels |
| 7 | Cross-seed importance reporting at -E | Inherited (when 988-corpus integrates) |

**Cap-binding pre-flight** referenced via §5 factory specifications: per-axis ref_id namespaces (`PILOT_LEVER_C_MW17_001..050`, `PILOT_LEVER_C_MW40_001..050`, etc) explicitly disjoint from existing corpora.

**PASS.**

## §6 — TC-X-OWNER-SCOPE-DISCIPLINE

(Verified in §1 above; restating.)

- 0 v3.x prompt edits ✓
- 0 BATCH2 reference edits ✓
- 0 `river-rats-core/` source edits ✓
- 0 corpus edits (existing 788-corpus + 30 MW-40-VERIFICATION corpus untouched) ✓
- 0 training-data edits ✓
- 0 memory edits ✓

Plan §3 MW-40 special case (re-use 30 existing MW-40-VERIFICATION hands) is a READ-only inclusion at -E corpus integration; no edits to existing data. **PASS.**

## §7 — TC-X-DISPATCH-COMPLIANCE (11th formal exercise)

| Compliance check | Spec | Observation | Match |
|---|---|---|---|
| Design-only (no execution) | dispatch §"Scope" | 1 plan file; 0 code; 0 model artifacts | ✅ |
| 1 file in PR (+ optional analysis) | dispatch §"Deliverable scope" | exactly 1 file | ✅ |
| Per-axis off-ramp specified | dispatch §"Per-axis pilot-first 5-hand gate" | §4 specifies per-axis off-ramp + dropping mechanism | ✅ |
| ref_id namespace `PILOT_LEVER_C_<AXIS>_001..050` per axis | dispatch | §5 specifies exactly this format | ✅ |
| Total cost ≤ $300 LLM AND ≤ 30h wall clock auto-approved | dispatch + plan | $65-100 LLM / 4-6h | ✅ (well under) |
| 5-phase mini-pipeline mirroring 12.5I-A precedent | dispatch | §2 explicitly mirrors A→B→C→D→E | ✅ |
| Pilot-first per axis (Hybrid pre-flight on first 5) | dispatch + memory | §5 + §6 row 4 (Hybrid Path 3) | ✅ |

Per `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`: builder discipline matches dispatch authoritative wording. **PASS.**

TC-X-DISPATCH-COMPLIANCE class continues to validate as durable on 11th formal exercise.

## TC-X-INTRA-PLAN-CONSISTENCY (informal continuation)

Cross-checked plan rule-pair joint domains for satisfiability:

| Rule pair | Joint domain | Satisfiable? |
|---|---|---|
| 4-axis spec (50 hands × 4 = 200) ∧ corpus integration (788+200=988 at -E) | non-trivial integration; ref_id disjoint per §5 | ✅ |
| MW-40 axis 50 hands ∧ §5 special case (30 reuse + 20 fresh) | total per-axis still 50; ref_id namespace `PILOT_LEVER_C_MW40_031..050` for fresh + existing PILOT_MW40_VERIF_001..030 | ✅ |
| Per-axis pilot-first gate ∧ per-axis off-ramp | gate produces decision → off-ramp activated on fail | ✅ |
| 4 axes ∧ stay-wrong list 4 hands | exactly matches; no axis missing from stay-wrong; no extra | ✅ |
| MW-17 prediction CALL ∧ stay-wrong "Under-calling" | matches (under-calling means "should be CALL but model is FOLD") | ✅ |
| MW-40 prediction BET ∧ stay-wrong "Residual passive" | matches (passive = should be BET but model is CHECK; PR #245 confirms BET is canonical) | ✅ |
| MW-45 prediction RAISE ∧ stay-wrong "Under-raising" | matches | ✅ |
| MW-47 prediction RAISE ∧ stay-wrong "Shared blind spot" + solver-corrected | matches solver-corrected RAISE | ✅ |

No contradictions surfaced. Plan §4 (PR #228) contradiction pattern explicitly addressed via per-axis off-ramp. **PASS.**

## §"Stop conditions" — design-phase

- ❌ Design lacks per-axis specification → §3 has 4 axis-specific sections
- ❌ Design lacks pilot-first gate per axis → §4 has explicit gate per axis
- ❌ Design uses solver-as-labels → §6 row 6 explicitly prohibits
- ❌ Total budget exceeds caps → $65-100 LLM ≪ $300; 4-6h ≪ 30h
- ❌ Plan-internal contradictions → 0 surfaced via TC-X-INTRA-PLAN-CONSISTENCY check above

## Test classes exercised

- TC-23 spec/infrastructure drift (CONTENT + EXISTENCE)
- TC-X-OWNER-SCOPE-DISCIPLINE (13th formal use; clean perimeter)
- **TC-X-DISPATCH-COMPLIANCE (11th formal exercise; clean PASS)** — class durable
- TC-X-INTRA-PLAN-CONSISTENCY (informal continuation; 8 rule-pair satisfiability checks; 0 contradictions)
- TC-X-METHODOLOGY-RULE-CROSSCHECK (sub-class; all 7 standing rules verified)

## Smarter-over-time observations

**Lever C-A design absorbed lessons from MW-40 verification cycle:**

- 5-phase mini-pipeline (A→B→C→D→E) explicitly mirrors 12.5I-MW40-VERIFICATION pattern that was operationalized through the curative class system (entries #11/#12/#13/#14)
- Per-axis off-ramp (§4 R3 pre-emptive note) cites the MW-40-VERIFICATION-C HALT pattern as motivation
- MW-40 axis re-uses the empirically-verified 30 hands (saves ~$30 + 30 min) — the MW-40 verification round's data has 2nd-life value here
- Pilot-first per axis (Hybrid Path 3) inherits PR #228 SHOULD_FIX-1 resolution

The QC class system is now informing builder design discipline at a sophisticated level: builder cites PR #245's MW-40 finding to justify MW-40 axis prediction (BET, not CHECK) + recommends data-reuse from the verification round. This is the curative classes producing compound value (PR #228-249 generated knowledge that's now reusable in PR #269+).

**Lever C is the only remaining positive-promote candidate for 12.5K** (Lever A variance-bound + Lever B hyperparameter-bound both early-stopped at pilot). Plan §4 R3 explicitly acknowledges "even worst case (all 4 axes fail pilot), discovery has informational value — labelling pipeline disagrees with canonical labels on these axes (similar to MW-40 finding)". **Robust to null-result outcome.**

## Audit cost / time

- Wall clock: ~12 min (plan structure + 4-axis verification + intra-plan consistency check + verdict authoring). Within 10-15 min estimate.
- LLM cost: $0.

## Gates

PR #269 cleared from QC side. Per dispatch §"What gates on this audit":

- **PR #269 merge:** clear from QC
- **12.5K-C-B situation generation dispatch** (4 axes × 50 hands = 200 situations factory pass): gates on PR #269 merge

No QC-side blocker.

## References

- 12.5K-C-A dispatch: `MAIN_TERMINAL_PR265_RESOLUTION_AND_125KCA_DISPATCH_2026-05-07.md` (master `1292233`, PR #268)
- Audit trigger: `MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR269_2026-05-07.md` (master `b359505`, PR #270)
- Plan: `PLAN_PHASE125K_C_AUGMENTED_DATA_2026-05-07.md` (in PR #269; 263L)
- 12.5K master plan §5 (Lever C high-level): `PLAN_PHASE125K_COMBINED_RETRAIN_2026-05-06.md`
- 12.5I-MW40-VERIFICATION precedent (5-phase mini-pipeline pattern): `PLAN_PHASE125I_MW40_VERIFICATION_2026-05-06.md`
- PR #245 (MW-40 graduation-fail; BET MEDIUM canonical confirmed): master `877555a`
- Curative log: `~/river-rats-qc/learning/curative_additions_log.md` entries #11-#14 (verification round-cycle classes informing this design)
- Memory: `feedback_qc_routing_when_standalone_active.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_solver_findings.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`

**Status: VERDICT = PASS. PR #269 cleared for merge from QC side. 4-axis Lever C design well-structured (per-axis prediction + pilot-first + off-ramp + budget within caps). MW-40 axis cost-saving observation surfaced for orchestrator approval. 32nd solo QC cycle. TC-X-DISPATCH-COMPLIANCE 11th formal exercise; class durable.**
