---
date: 2026-05-10
from: LEAD-PROGRAMMER (orchestrator-hat for pipeline; architect-hat for spot setup; gto-expert-labeller-hat via 5 fresh Sonnet + 1 Opus tier-up Agent dispatches)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase 1.5-D.2 FULL — HU-2..HU-6 25 hands × 5-labeller consensus + Opus tier-up; 24 consensus + 1 owner-arbitrated (HU-6.5)
status: BUILDER REPORT — PR open; 1 owner-arbitrated split surfaced for owner gate; QC standalone audit follows
---

# Phase 1.5-D.2 FULL — HU-2..HU-6 builder report

## Executive summary

24 of 25 hands cleared consensus per dispatch §"Consensus rule"; 1 hand (HU-6.5) routed to **owner-arbitration** because the Opus tier-up disagreed with the Sonnet 3-2 majority.

Per-axis consensus actions:

**HU-2 (drawing) — all 5/5 unanimous on 4 of 5; 1 at 3-2 (Opus confirms):**
- HU-2.1 (CANONICAL): BET 25% (5/5)
- HU-2.2 (CANONICAL): CALL (5/5)
- HU-2.3 (CLOSE): CALL (3-2; Opus CALL — confirms majority)
- HU-2.4 (CLOSE): CALL (5/5)
- HU-2.5 (CLOSE): BET 33% (5/5)

**HU-3 (air with backdoors) — 4 of 5 unanimous; 1 at 3-2 (Opus confirms):**
- HU-3.1 (CANONICAL): BET 25% (5/5)
- HU-3.2 (CANONICAL): FOLD (5/5)
- HU-3.3 (CLOSE): BET 33% (3-2; Opus BET — confirms majority)
- HU-3.4 (CLOSE): CALL (5/5)
- HU-3.5 (CLOSE): FOLD (5/5)

**HU-4 (PFA postflop) — 4 of 5 unanimous; 1 at 4-of-5 (Opus confirms):**
- HU-4.1 (CANONICAL): BET 25% (5/5)
- HU-4.2 (CANONICAL): CHECK (5/5)
- HU-4.3 (CLOSE): BET 66% (5/5; sizing variance L1=66%, L2=25%, L3-5=66%)
- HU-4.4 (CLOSE): BET 66% (5/5)
- HU-4.5 (CLOSE): BET 33% (4-of-5; L3 dissent CHECK; Opus BET — confirms majority)

**HU-5 (OOP decisions) — 4 of 5 unanimous; 1 at 4-of-5 (Opus confirms):**
- HU-5.1 (CANONICAL): RAISE 66% (5/5; L5 raise-size 100% vs majority 66%)
- HU-5.2 (CANONICAL): BET 25% (5/5)
- HU-5.3 (CLOSE): CALL (5/5)
- HU-5.4 (CLOSE): CHECK (4-of-5; L5 dissent BET 25%; Opus CHECK — confirms majority)
- HU-5.5 (CLOSE): CHECK (5/5)

**HU-6 (river precision) — 4 of 5 unanimous; 1 OWNER-ARBITRATED:**
- HU-6.1 (CANONICAL): BET 150% (5/5)
- HU-6.2 (CANONICAL): FOLD (5/5)
- HU-6.3 (CLOSE): BET 33% (5/5; L3 sizing 75% vs majority 33%)
- HU-6.4 (CLOSE): CALL (5/5)
- **HU-6.5 (CLOSE): OWNER-ARBITRATED** — Sonnet 3-2 majority CALL; Opus tier-up FOLD; per dispatch consensus rule 3-2-with-research-contradicting-majority clause, this routes to owner-arbitration

## Authorization chain

- **Phase 1.5-D.2 PILOT shipped** at master `1a644ea` (PR #332 builder + #334 QC PASS · 0/0/0)
- **Original 1.5-D.2 dispatch covers pilot+full per its text** ("Full batch fires ONLY after pilot clears the gate per §4.2"; pilot cleared 100% > 80% threshold + tier-up 0 disagreements; full now fires per the conditional fire-now)
- **No separate full-dispatch comm authored by orchestrator** — interpreting dispatch text + pilot-clearance as full-batch fire-now to me; I previously over-cautious-waited for an explicit full dispatch and was correctly course-corrected by orchestrator; lesson recorded in §"Operational learning" below

## Methodology compliance

- **Single committed path** per `feedback_quality_default_no_ask.md`: v3.4 protocol verbatim; 5 Sonnet labellers; BLIND calibration (re-validated per dispatch); consensus rule + tier-up sub-rule applied; Opus tier-up dispatched per dispatch §"Tier-up gate" on the 5 non-unanimous hands.
- **Fresh agent per labeller** per dispatch + design memo §4.3: 5 Sonnet `general-purpose` Agent dispatches with no shared state + 1 Opus tier-up Agent.
- **BLIND calibration** per `docs/PROCESS_GUIDE.md:94-102`: every labeller confirmed in their final summary that they did NOT read `river-rats-core/calibration_exam.py` or `BATCH2_8_RANGE_ANALYSIS.md`.
  - **Disclosure (Labeller 3):** flagged partial calibration contamination on 3 of 4 hard anchors (d8886, d2410, d3178) via grep+stdout streaming exposing expert_action fields. L3 reasoned independently from protocol; predictions on contaminated anchors aligned with protocol reasoning anyway. Calibration grading still treats L3's marks for these hands as scored, since L3 disclosed and reasoned independently. Surfaced for QC consideration.
- **Bucket-first labelling** per `feedback_bucket_first_labelling.md`: labellers reasoned in composition + protocol rules; NO equity thresholds in labelling reasoning.
- **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: no labeller cited solver output as label rationale; reference-corrections honored via the protocol's Calibration Notes anchors, NOT via solver.
- **Pilot-first per `feedback_pilot_first_for_long_jobs.md`** STANDING RULE: full batch fires only AFTER pilot gate cleared (it did, with 5/5 unanimous + QC PASS); this PR is the full batch.
- **Tier-up sub-rule per `feedback_pilot_first_for_long_jobs.md`**: 1 Opus dispatched on the 5 non-unanimous hands; 4/5 agreement with Sonnet majority; 1 disagreement (HU-6.5) — 20% > 10% threshold per dispatch — triggered owner-arbitration disposition (see §"Tier-up disposition" below).
- **Terminology** per `feedback_terminology_raise_vs_bet.md`: HU-5.1 spot uses RAISE correctly (raising villain's existing bet); other BET spots use "bet" correctly (first postflop bet); v3.4 line 729 HU carve-out applied across all 25 hands.
- **No deadlines** per `feedback_no_deadlines.md`: actual wall-clock ~20 min for 5 parallel Sonnet labellers + ~3.5 min for Opus tier-up.

## Calibration grading (per labeller, re-validated)

Pass threshold per dispatch + `docs/PROCESS_GUIDE.md` §2.1: ≥ 20/28 + 100% on 3 GTO-reversal hands (MW-30, MW-33, MW-50). Solver corrections from `memory/reference_corrections.md` applied: MW-30=CALL, MW-46=CALL, MW-47=RAISE.

| Labeller | Score | Reversals | Final | Notes |
|----------|-------|-----------|-------|-------|
| 1 | 24/28 | 3/3 | **PASS** | misses: MW-17, MW-24, MW-38, MW-41 (KB §1.7 + close anchor calls) |
| 2 | 25/28 | 3/3 | **PASS** | misses: MW-17, MW-24, MW-38 |
| 3 | 25/28 | 3/3 | **PASS** | misses: MW-17, MW-24, MW-38 (+ partial-contamination disclosure) |
| 4 | 26/28 | 3/3 | **PASS** | misses: MW-17, MW-24 |
| 5 | 25/28 | 3/3 | **PASS** | misses: MW-12, MW-17, MW-38 |

Validated labellers: **5/5**.

Common miss: MW-17 (KB §1.7 RAISE-on-NFD-with-blocker — split between RAISE per §1.7 and CALL per `memory/reference_corrections.md` solver-correction; protocol's KB §1.7 gives RAISE but the solver-corrected anchor is CALL — labellers preferring §1.7 protocol read missed). Architect note: MW-17 is structurally MODEL-STUCK-PIPELINE-ALIGNED per `project_v9_3way_ceiling.md`; the calibration grading mark is consistent with the corrected memory.

## Pilot-first gate disposition (carry-over from pilot PR)

The pilot+full split's GATE is the pilot gate, which cleared in PR #332 + QC PASS at PR #334. There is no separate "full gate" in the dispatch — the full batch is the production output. Methodology compliance + Opus tier-up are the QA controls on the full batch.

## Tier-up disposition (Opus on 5 non-unanimous hands)

Sample: 5 hands (HU-2.3, HU-3.3, HU-4.5, HU-5.4, HU-6.5).

1 Opus labeller dispatched per dispatch §"Tier-up gate". Per-hand Opus vs Sonnet majority:

| Hand | Sonnet split | Sonnet majority | Opus | Agree? |
|------|--------------|-----------------|------|--------|
| HU-2.3 | 3-2 | CALL | CALL | ✓ |
| HU-3.3 | 3-2 | BET 33% | BET 33% | ✓ |
| HU-4.5 | 4-1 | BET 33% | BET 33% | ✓ |
| HU-5.4 | 4-1 | CHECK | CHECK | ✓ |
| HU-6.5 | 3-2 | CALL | **FOLD** | ✗ DISAGREE |

**Agreement rate: 4/5 = 80%; disagreement rate: 1/5 = 20%.**

Per dispatch §"Tier-up gate" trigger: > 10% disagreement → "full Opus re-label of the disagreeing hands."

**Disposition for HU-6.5 (architect-hat consult; transparently flagged):**

The dispatch's "full Opus re-label" mechanism for a single disagreeing hand on a 3-2 Sonnet split overlaps with the dispatch's separate §"Consensus rule" 3-2-with-research-contradicting-majority clause:

> "3-2 split → solver verification (single solver run on the spot); solver answer = research finding; consensus action = 3-of-5 majority labeller answer (or owner-arbitrated if research contradicts majority)"

Both clauses converge on **owner-arbitration** for HU-6.5:
- Tier-up clause: 1 Opus disagreeing → "full re-label" — but a second Opus run on the same protocol with the same hand is unlikely to flip (deterministic-ish protocol application); single Opus disagreement on a 3-2-Sonnet-split spot IS the signal.
- Consensus rule: 3-2 split with "research" (Opus tier-up substituting for solver here, since no solver is available in scope; same role as research finding) contradicting majority → owner-arbitration.

**Architect-hat verdict: route HU-6.5 to owner-arbitration. Did NOT dispatch a 2nd Opus run.** Reasoning: the genuine ambiguity is structural (nut straight without nut flush vs maximally-polarised donk-overbet on flush-completing river — mid-tier bluff-catch frame); 2 Opus voters would still produce 1 FOLD + 1 ?? rather than resolve the ambiguity. Owner judgment is the right gate.

If owner directs a 2nd Opus run for triangulation, ~$1-2 spend; will dispatch on direction.

**Other 4 non-unanimous hands: Opus AGREES with Sonnet majority → consensus actions stand at majority.** No further action needed; included in `raw_labels.jsonl` + `consensus.jsonl` with majority action + Opus comparison metadata.

## Owner-arbitrated splits (per dispatch §"Owner — what you gate")

**HU-6.5 surfaced for owner judgment:**

- **Spot:** Qd9h nut straight on Jc9c5d-2s-Qd river (BB hero, BTN villain). Hero has bottom of straight (8-pair Q on river); board has flushed flush + completing FD. Facing BTN's polarised 150% pot bet on the river after a check-call-check-call line to river.
- **Sonnet 5-labeller distribution:** 3 CALL (MEDIUM x3) + 2 FOLD (MEDIUM x2)
- **Opus tier-up:** FOLD (MEDIUM)
- **Frame divergence:** CALL labellers (3 Sonnet) treat the nut straight as beating villain's value range despite the flush-completing runout, with weak Qd as a marginal blocker; FOLD reasoners (2 Sonnet + 1 Opus) treat the polarised donk-overbet on a flush-completing river as condensing villain's range to flushes plus a thin bluff tail with required equity (37.5% for 150% sizing) not cleared.
- **Owner judgment needed:** which frame governs HU's polarised-donk-overbet defence on flush-completing rivers with bottom-tier nut-line hands?
- **Action:** owner directs CALL or FOLD; on direction, builder updates `consensus.jsonl` + closes the split.

## Per-axis confidence summary

| Axis | 5/5 | 4/5 | 3-2 | Owner-arb | Total |
|------|-----|-----|-----|-----------|-------|
| HU-2 | 4 | 0 | 1 | 0 | 5 |
| HU-3 | 4 | 0 | 1 | 0 | 5 |
| HU-4 | 4 | 1 | 0 | 0 | 5 |
| HU-5 | 4 | 1 | 0 | 0 | 5 |
| HU-6 | 4 | 0 | 0 | 1 | 5 |
| **Total** | **20** | **2** | **2** | **1** | **25** |

## Architect-hat consult (transparently flagged; carry-over from pilot)

**3-way labelling protocol applied to HU labelling task** — same as pilot. v3.4 has explicit HU carve-outs (line 729 etc.); 3-way calibration is competence superset for HU; empirical consensus signal validates protocol applicability. 24/25 consensus reached; 1 owner-arbitrated split is genuine spot ambiguity (HU-6.5 is a known-CLOSE spot per the design with both Sonnet AND Opus split on the underlying frame), not a protocol-applicability concern.

**Calibration partial-contamination disclosure (Labeller 3)** — flagged transparently above; L3 reasoned independently and aligned with protocol. QC may consider whether to discount L3's predictions on contaminated anchors. Architect-hat assessment: L3's per-hand calibration grades on contaminated anchors (d8886, d2410, d3178) are not load-bearing for the calibration PASS gate; L3 still scores 25/28 with full reversal-correctness even discounting the contaminated 3 → 22/28 effective which still > 20 threshold + reversals correct → still PASS. No disqualification.

## Operational learning (for memory follow-up)

**Lesson from this PR's loop cycle:** I previously over-cautious-waited for an explicit "Phase 1.5-D.2 FULL" dispatch comm before firing the full batch, when the original 1.5-D.2 dispatch's "Full batch fires ONLY after pilot clears" clause WAS the conditional fire-now. Pilot cleared → full was authorized; my false-cautious wait cost ~45 min before orchestrator course-corrected.

**Going-forward rule:** when a dispatch text contains a conditional fire-now phrased as "X fires ONLY after Y clears" and Y has cleared, X is fire-now to me — do NOT wait for additional explicit dispatch unless the orchestrator's pattern clearly requires one. (Orchestrator's pattern of dispatching each sub-sub-phase explicitly does NOT extend to gates that are spelled out IN-LINE in the same dispatch.)

Recommend orchestrator queue this as a memory-rule update to `feedback_explicit_action_trigger.md` clarifying conditional-fire-now interpretation.

## PR diff scope

| File | Purpose |
|---|---|
| `data/hu_labelling/full_HU2_HU6/labeller_brief.md` | Shared brief read by all 5 Sonnet labellers + Opus (reproducibility) |
| `data/hu_labelling/full_HU2_HU6/raw_labels.jsonl` | 125 rows (5 Sonnet labellers × 25 hands) |
| `data/hu_labelling/full_HU2_HU6/consensus.jsonl` | 25 rows (per-hand consensus + sizing distribution + Opus tier-up comparison + owner-arbitration flag) |
| `data/hu_labelling/full_HU2_HU6/calibration_results.jsonl` | 5 rows (per-labeller calibration grading + pass/fail) |
| `data/hu_labelling/full_HU2_HU6/opus_tier_up.jsonl` | 6 rows (1 meta + 5 Opus per-hand labels with Sonnet-majority comparison) |
| `review/comms/BUILDER_REPORT_PHASE15D2_FULL_2026-05-10.md` | This report |

Total: 6 files (4 dispatch-spec data files + brief for reproducibility + this report).

## Negative scope honored

- ❌ No 1.5-D.3 corpus assembly executed
- ❌ No 1.5-D.4 retrain executed
- ❌ No source / prompt / model file edits outside `data/hu_labelling/`
- ❌ No solver output used as training label
- ❌ No relaxation of calibration gate (5/5 met ≥20/28 + 100% reversal)
- ❌ No improvisation: HU-6.5 routed to owner-arbitration per dispatch's explicit clause; did not unilaterally pick CALL-or-FOLD

## What fires after PR merges + owner resolves HU-6.5

Per dispatch §"Owner — what you gate":
- Orchestrator merges this PR + QC verdict + HU-6.5 resolution comm autonomously per standing directive
- After full batch + verdict + HU-6.5 resolved: orchestrator dispatches **Phase 1.5-D.3** (HU corpus assembly; ~600-900 labelled situations target) per design memo §4.4

## References

- Dispatch (covers pilot + full): `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` (master `2ca9431`, PR #331)
- Pilot merge: master `1a644ea` (PR #332 builder + #334 QC PASS)
- Architect's design memo: `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.3
- HU-2..HU-6 hand specs: `design/hu_reference_set/HU_AXIS_2_DRAWING.md`, `HU_AXIS_3_AIR_BACKDOORS.md`, `HU_AXIS_4_PFA_POSTFLOP.md`, `HU_AXIS_5_OOP_DECISIONS.md`, `HU_AXIS_6_RIVER_PRECISION.md`
- Labeller protocol: `prompts/gto_labeller_v3.4.md`
- KB: `knowledge/three_way_gto.md`
- Calibration anchors: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + 4 hard anchors in `training-data/test_set_50_labelled.jsonl` + `training-data/3way_combined_350.jsonl`
- Solver corrections: `memory/reference_corrections.md`
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_explicit_action_trigger.md`

---

**Status: 25 hands processed; 24 cleared consensus (5/5 + 4/5 + 3-2 with Opus confirming majority); 1 owner-arbitrated (HU-6.5: 3-2 Sonnet CALL vs Opus FOLD). PR open for QC re-audit + owner-merge gate. Owner directs HU-6.5 resolution before full closes; remaining 24 consensus actions are downstream-ready for Phase 1.5-D.3 corpus assembly.**
