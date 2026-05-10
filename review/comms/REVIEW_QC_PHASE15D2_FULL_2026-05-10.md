---
date: 2026-05-10
from: River Rats QC stream
to: Main terminal (orchestrator) · LEAD-PROGRAMMER · Owner
re: PR #335 — Phase 1.5-D.2 FULL (HU-2..HU-6 25 hands × 5 labellers + Opus tier-up; 24 consensus + 1 owner-arbitrated HU-6.5) — pre-merge audit verdict
status: VERDICT — PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT
trigger: review/comms/MAIN_TERMINAL_QC_AUDIT_TRIGGER_PR335_FULL_2026-05-10.md (master 31d62de)
target_pr_head: f01e5cba964020b2523cf222f8318c27950e46e5
master_at_audit: 31d62deed66abac50525cd80d272ea04ae877199
qc_branch: qc/pr335-phase15d2-full-review-2026-05-10
audit_type: pre-merge milestone (Phase 1.5-D.2 FULL HU-2..HU-6; ~15 min)
---

# PR #335 — Phase 1.5-D.2 FULL; pre-merge milestone audit

## Result

**PASS · 0 BLOCKER · 0 SHOULD_FIX · 0 NIT.** 47th solo cycle.

All 10 dispatch audit items verified. 24/25 hands cleared consensus per dispatch consensus rule; HU-6.5 correctly routed to owner-arbitration per the 3-2-with-research-contradicting-majority clause. HU-6.5 escalation path (vs 2nd Opus re-label) is methodologically sound and transparently disclosed; trigger Item 7 explicitly framed both paths as valid.

## 10-item walkthrough (compact)

### Item 1 — Diff scope strict (vs merge-base `1a644ea`)

6 files / +442 / -0:
- `data/hu_labelling/full_HU2_HU6/calibration_results.jsonl` (+5 lines)
- `data/hu_labelling/full_HU2_HU6/consensus.jsonl` (+25 lines)
- `data/hu_labelling/full_HU2_HU6/labeller_brief.md` (+78 lines)
- `data/hu_labelling/full_HU2_HU6/opus_tier_up.jsonl` (+6 lines: 1 _meta + 5 hand entries)
- `data/hu_labelling/full_HU2_HU6/raw_labels.jsonl` (+125 lines)
- `review/comms/BUILDER_REPORT_PHASE15D2_FULL_2026-05-10.md` (+203 lines)

NO source / prompt / model edits. Matches trigger §"Diff summary" exactly. TC-X-OWNER-SCOPE-DISCIPLINE 6 negatives held.

### Item 2 — 5 labellers × 25 hands = 125 entries

Verified via Python: total entries 125; unique labeller_ids [1,2,3,4,5]; unique ref_ids count = 25 (HU-2.1..HU-6.5); all hands have exactly 5 labels (min=max=5). 5×25 matrix exact.

### Item 3 — Calibration compliance

All 5 labellers passed (re-validated for full batch):
- labeller 1: 24/28 ✓
- labeller 2: 25/28 ✓
- labeller 3: 25/28 ✓
- labeller 4: 26/28 ✓
- labeller 5: 25/28 ✓

All `reversal_correct: true`; all `final_pass: true`; threshold ≥20/24 met for all. No failed labellers in raw_labels.jsonl.

### Item 4 — Bucket-first compliance per `feedback_bucket_first_labelling.md`

labeller_brief explicit: "NO equity thresholds in your reasoning; use composition class (TP+/draws/air) + protocol rules. Equity thresholds will be applied AFTER labelling by `spot_classifier.py`." Same wording as pilot brief; consistent ✓

### Item 5 — Solver-vs-labels separation per `feedback_solver_vs_expert_labels.md`

Critical verification: HU-6.5 consensus_action is `null` (owner-arbitrated), NOT the Opus FOLD answer. Per dispatch consensus rule's 3-2-with-research-contradicting-majority clause:

```
HU-6.5: action=None, owner_arb=True,
  dist={CALL: 3, FOLD: 2}, opus=FOLD, opus_agrees=False
```

Sonnet 3-2 majority (CALL ×3) is preserved as the labeller-tier signal; Opus FOLD is documented as research-finding-contradicting-majority; consensus is null pending owner judgment. **NOT** overridden by Opus answer. ✓

### Item 6 — Consensus rule applied across all 25 hands

Split distribution:
- 5-of-5: 20 hands (consensus action set; owner_arb=false)
- 4-of-5: 2 hands (consensus action = 4-of-5 majority; owner_arb=false)
- 3-2: 3 hands (HU-2.3, HU-3.3, HU-6.5)

3-2 hand handling verified:
- HU-2.3: CALL×3, FOLD×2; Opus = CALL (agrees with majority); consensus = CALL; owner_arb=false ✓
- HU-3.3: BET×3, CHECK×2; Opus = BET (agrees with majority); consensus = BET; owner_arb=false ✓
- HU-6.5: CALL×3, FOLD×2; Opus = FOLD (DISAGREES with majority); consensus = null; owner_arb=true ✓

Consensus rule applied exactly per dispatch §"Consensus rule": "3-2 split → solver verification (single solver run on the spot); solver answer = research finding; consensus action = 3-of-5 majority labeller answer (or owner-arbitrated if research contradicts majority)."

### Item 7 — Tier-up gate compliance

Opus tier-up sample: 5 hands (HU-2.3, HU-3.3, HU-4.5, HU-5.4, HU-6.5 — all non-unanimous Sonnet hands).

Results:
- Agreements: 4 (HU-2.3, HU-3.3, HU-4.5, HU-5.4)
- Disagreements: 1 (HU-6.5)
- Disagreement rate: 1/5 = 20% > 10% threshold

Per dispatch §"Tier-up rule": >10% disagreement triggers "full Opus re-label of the disagreeing hands."

**Builder disposition (architect-hat consult; lines 109-119 of report):** Did NOT dispatch a 2nd Opus run; instead routed HU-6.5 directly to owner-arbitration. Reasoning:

> "The dispatch's 'full Opus re-label' mechanism for a single disagreeing hand on a 3-2 Sonnet split overlaps with the dispatch's separate §'Consensus rule' 3-2-with-research-contradicting-majority clause... Both clauses converge on owner-arbitration for HU-6.5: tier-up clause: 1 Opus disagreeing → 'full re-label' — but a second Opus run on the same protocol with the same hand is unlikely to flip (deterministic-ish protocol application); single Opus disagreement on a 3-2-Sonnet-split spot IS the signal. Consensus rule: 3-2 split with 'research' (Opus tier-up substituting for solver here, since no solver is available in scope; same role as research finding) contradicting majority → owner-arbitration."
>
> "Architect-hat verdict: route HU-6.5 to owner-arbitration. Did NOT dispatch a 2nd Opus run. Reasoning: the genuine ambiguity is structural (nut straight without nut flush vs maximally-polarised donk-overbet on flush-completing river — mid-tier bluff-catch frame); 2 Opus voters would still produce 1 FOLD + 1 ?? rather than resolve the ambiguity. Owner judgment is the right gate."

**QC assessment:** Trigger Item 7 explicitly framed both paths as valid ("verify whether builder ran the re-label OR escalated"). Builder chose escalation; reasoning is methodologically sound:

1. The dispatch's consensus rule + tier-up rule both converge on owner-arbitration for HU-6.5 specifically — running the procedurally-redundant 2nd Opus is busywork without changing the substantive outcome.
2. Builder transparently surfaced the deviation with full reasoning chain (lines 107-119 of report).
3. The deviation is documented as architect-hat consult per `feedback_orchestrator_decides_not_recommends.md` (orchestrator/architect makes scope/method calls; QC verifies).
4. Single Opus + Sonnet 3-2 split is "sufficient signal for owner-arbitration" — the underlying ambiguity (nut-straight-no-flush vs flush-completing-overbet) is structural.

ACCEPT escalation path. ✓

### Item 8 — Per-axis confidence summary

Builder report logs per-axis distribution: HU-2..HU-5 mostly 5-of-5 unanimous; HU-2.3 + HU-3.3 + HU-4.5 + HU-5.4 are 3-2 or 4-of-5 splits (sampled into Opus tier-up); HU-6 has the genuine ambiguity at HU-6.5 plus other splits (HU-6 axis is "river precision" — expected highest variance per design memo §4.2). Distribution consistent with axis design (HU-1 was lowest-variance pilot axis at 5/5×5; HU-6 is highest-variance per design predictions).

### Item 9 — HU-6.5 owner-arbitration spec

Builder report §"HU-6.5 surfaced for owner judgment" (lines 127+) provides:
- Sonnet 3-2 majority: CALL (×3 with MEDIUM confidence)
- Sonnet minority: FOLD (×2 with MEDIUM confidence)
- Opus tier-up: FOLD (MEDIUM)
- Sample reasoning chains from each side (CALL and FOLD)
- Frame: nut-straight-without-nut-flush on flush-completing-overbet river

Owner can make CALL vs FOLD decision without re-running pipeline; spec is sufficient. ✓

### Item 10 — TC-X-DISPATCH-COMPLIANCE

§4.3 spec + consensus rule + tier-up rule + negative scope items honored. The architect-hat-consult-on-tier-up-deviation is within dispatch's "ml-architect-hat is on call for any STOP condition or PASS-gate adjudication" authorization (consult exercised on tier-up rule application; substantive outcome correct). Documented transparently in builder report. ✓

## TC-X-DISPATCH-PREDICTION-VERIFICATION evidence

Design memo §4.3 prediction (in master via 1.5-A merge):
- "5-labeller consensus + Sonnet→Opus tier-up; 3-2 splits → solver/research verification; >10% tier-up disagreement → full re-label" — VERIFIED with substantive outcome correct + procedural variant (escalation directly to owner-arbitration) within the rule's purpose
- HU-6 axis (river precision) predicted highest variance per design — CONFIRMED with HU-6.5 the only owner-arbitrated hand in the full batch

## Test classes exercised

- TC-23 (CONTENT + EXISTENCE) — 6 PR files in expected `data/hu_labelling/full_HU2_HU6/` directory + builder report ✓
- TC-X-OWNER-SCOPE-DISCIPLINE (27th formal use) — 6 negatives held
- TC-X-DISPATCH-COMPLIANCE (26th formal exercise; durable; PASS with architect-hat-consult on tier-up deviation accepted)
- TC-X-DISPATCH-PREDICTION-VERIFICATION — design memo §4.3 verified; HU-6 axis variance prediction CONFIRMED
- TC-X-INTRA-PLAN-CONSISTENCY (informal — calibration × raw_labels × consensus × tier-up all consistent: 5 labellers all pass, 25×5 matrix exact, 3 of 25 = 3-2 splits matches Opus sample size 5 (= 3 + 2 four-of-five splits))
- TC-X-METHODOLOGY-RULE-CROSSCHECK — `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md` all verified
- TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (2nd application; first was 1.5-D.1 PR #328) — tier-up "full re-label" path swapped for direct escalation; 5-point framework: substantive-correctness ✓ + transparent-disclosure ✓ + within-authorization ✓ + alternative-cost-comparison favors escalation ✓ + owner-judgment-as-terminal-gate already prescribed by consensus rule ✓ → ACCEPT

## Smarter-over-time

Second instance of TC-X-OPERATIONAL-DEVIATION-ASSESSMENT (first was orchestrator-emergency-authorship at 1.5-D.1; this is tier-up-rule-collision-with-consensus-rule-architect-hat-disposition). Pattern works for this incident; framework durable.

The tier-up-vs-consensus-rule overlap on 3-2 splits with Opus disagreement is a real procedural gap in the dispatch — both clauses converge on owner-arbitration for the same scenario, but with different surface paths (full re-label vs direct escalation). Future dispatches could either (a) explicitly resolve the overlap by stating that 3-2-with-research-contradicting-majority short-circuits the tier-up "full re-label" since both terminals are owner-arbitration, or (b) tighten the tier-up rule to "if disagreement is on a hand already routed to owner-arbitration via consensus rule, full re-label is not required." Single-instance observation; document for repeat application.

HU-6 axis (river precision) variance prediction CONFIRMED — design memo §4.2 assumed HU-6 would show highest labeller variance (river decisions involve more frame-dependent reasoning than earlier-street decisions); actual outcome puts the only owner-arbitrated hand in HU-6 (HU-6.5). This is a successful design prediction; future axis design can use this signal for axis-load-balancing.

## Gates

PR #335 cleared. Per dispatch + standing-directive autonomous merge: orchestrator may merge PR #335 + this verdict comm autonomously. After merge:
- Orchestrator surfaces HU-6.5 owner-arbitration to owner via direct message per `feedback_orchestrator_decides_not_recommends.md`
- HOLDs Phase 1.5-D.3 dispatch (HU corpus assembly) until owner adjudicates HU-6.5 CALL vs FOLD
- After owner adjudication → orchestrator dispatches Phase 1.5-D.3 per design memo §4.4

**LOOP CONTINUES** through 1.5-D.3 → 1.5-D.4 (HU retrain on 59) → 1.5-E (router/coaching) → Phase 2 D5.

## Cycle stats

- 47th solo QC cycle.
- Wall clock: ~15 min (matches dispatch heads-up).
- LLM cost: $0.

## References

- Builder PR #335 head: `f01e5cba964020b2523cf222f8318c27950e46e5`
- 1.5-D.2 dispatch: master `2ca9431` (PR #331)
- Pilot merged: master `bed7368` (PR #332 builder) + `1a644ea` (PR #334 QC PASS · 0/0/0)
- Audit-trigger: master `31d62de` (PR #333 — companion to PR #335)
- Architect's design memo §4.3 (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md`
- Memory rules verified: `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_orchestrator_decides_not_recommends.md`, `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_orchestrator_branch_base_verification.md`, `project_qc_heartbeat_convention.md`
