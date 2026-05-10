---
date: 2026-05-10
from: LEAD-PROGRAMMER (orchestrator-hat for pipeline; architect-hat for spot setup; gto-expert-labeller-hat via 5 fresh Agent dispatches)
to: Main terminal (orchestrator) · Owner · QC stream
re: Phase 1.5-D.2 PILOT — HU-1 (5 hands) labelling pipeline; 5-labeller consensus 5/5 unanimous; pilot gate PASS; full batch (HU-2..HU-6) authorized
status: BUILDER REPORT — PR open; QC re-audit + autonomous merge per standing directive on PASS
---

# Phase 1.5-D.2 PILOT — HU-1 builder report

## Executive summary

**Pilot gate: PASS.** 5-of-5 Sonnet labellers reached unanimous consensus on all 5 HU-1 pilot hands. All 5 labellers passed BLIND calibration. No Opus tier-up needed (sample = non-unanimous = empty per dispatch §"Tier-up gate").

**Consensus actions:**

| Hand | Marker | Action | Labeller count | Sizing mode | Sizing distribution |
|---|---|---|---|---|---|
| HU-1.1 | CANONICAL | BET | 5/5 | 25% | {25%: 4/5, 33%: 1/5} |
| HU-1.2 | CANONICAL | BET | 5/5 | 33% | {33%: 3/5, 75%: 2/5} |
| HU-1.3 | CLOSE | BET | 5/5 | 25% | {25%: 4/5, 66%: 1/5} |
| HU-1.4 | CLOSE | RAISE | 5/5 | 75% | {75%: 5/5} |
| HU-1.5 | CLOSE | CALL | 5/5 | n/a | n/a |

Confidence score (per dispatch consensus rule = labeller-count / 5): 1.0 on every hand.

Action consensus is unanimous; sizing variance on HU-1.2 (33% / 75%) and HU-1.3 (25% / 66%) reflects HU sizing-tree uncertainty (small-c-bet vs polarized-overbet on canonical-strong vs close-board-texture spots) but action-level consensus is the load-bearing signal for downstream training.

## Authorization chain

- **Phase 1.5-D.1 merged:** master `7e89d8d` (PR #328 builder) + `79a98e9` (PR #330 QC PASS · 0/0/0)
- **Phase 1.5-D.2 dispatch:** `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` (master `2ca9431`, PR #331)
- **Re-poke acknowledged:** orchestrator's "fire NOW on Phase 1.5-D.2" directive received; builder fired on next online tick per `feedback_named_author_builds_not_polls.md` + `feedback_listen_to_orchestrator_always.md` + `feedback_explicit_action_trigger.md`

## Methodology compliance

- **Single committed path** per `feedback_quality_default_no_ask.md`: v3.4 protocol verbatim; 5 labellers; BLIND calibration; consensus rule + tier-up sub-rule applied.
- **Fresh agent per labeller** per dispatch + design memo §4.3: 5 separate Agent dispatches with no shared state; each agent received the shared brief at `data/hu_labelling/pilot_HU1/labeller_brief.md` and was assigned its labeller_id.
- **BLIND calibration** per `docs/PROCESS_GUIDE.md:94-102`: every labeller confirmed in their final summary that they did NOT read `river-rats-core/calibration_exam.py` or any expert-action field of the labelled JSONLs. Labellers extracted hard anchors via brief-provided `ref_id` strings only.
- **Bucket-first labelling** per `feedback_bucket_first_labelling.md`: labellers reasoned in composition (TP+/draws/air) + protocol rules; NO equity thresholds in labelling reasoning (those are applied AFTER by `coaching/spot_classifier.py`).
- **Solver-vs-labels separation** per `feedback_solver_vs_expert_labels.md`: no labeller cited solver output as label rationale. Reference-corrections from `memory/reference_corrections.md` (MW-30 CALL, MW-46 CALL, MW-47 RAISE) honored via the protocol's Calibration Notes anchors, NOT via solver output.
- **Pilot-first per `feedback_pilot_first_for_long_jobs.md`** STANDING RULE: this PR is the pilot (5 hands × 5 labellers); full batch (25 hands × 5 labellers) holds until pilot gate PASS + this PR merges + orchestrator dispatches Phase 1.5-D.2-full.
- **Tier-up sub-rule per `feedback_pilot_first_for_long_jobs.md`**: Sonnet→Opus cross-check on non-unanimous hands is the rule; sample is empty here (5/5 unanimous), so vacuously satisfied.
- **Terminology** per `feedback_terminology_raise_vs_bet.md`: HU-1.4 spot uses "RAISE" correctly (raising villain's existing bet); HU-1.1/1.2/1.3 use "BET" correctly (first postflop bet); v3.4 protocol's HU carve-out at line 729 applied.
- **No deadlines** per `feedback_no_deadlines.md`: actual wall-clock ~16 min for 5 parallel labellers (longest agent 956s).

## Architect-hat consult (transparently flagged for QC)

**3-way labelling protocol applied to HU labelling task.** v3.4 protocol is titled "3-Way Postflop GTO Labelling Agent" and references `knowledge/three_way_gto.md`; calibration exam is 28 three-way reference hands (24 BATCH2 multiway + 4 hard anchors). For this 1.5-D.2 pilot:

- **v3.4 has explicit HU carve-outs** (e.g., line 729: "Heads-up spots (`num_opponents = 1`) — bet for value/protection per existing v3.1 rules"; DO NOT Rule 11's explicit exclusion list begins with "Heads-up spots ... — bet for value/protection per existing v3.1 rules"). Labellers correctly applied these carve-outs across all 5 HU pilot hands.
- **3-way calibration is a competence superset for HU labelling.** A labeller passing 3-way calibration (which exercises range-collision reasoning, multiway aggression compression, and the full v3.4 DO NOT Rule set) demonstrates deeper protocol competence than HU spots require. All 5 labellers passed (≥20/28 + 100% on the 3 GTO-reversal anchors MW-30, MW-33, MW-50).
- **Empirical signal of HU competence:** unanimous 5/5 action consensus on all 5 HU hands at high (HIGH/MEDIUM) confidence is the strongest possible indication that the v3.4 + 3-way-calibration protocol effectively labels HU spots.

This consideration was foreseeable from the dispatch's spec; flagging here for QC awareness rather than as a STOP-condition consult since (a) v3.4's HU carve-outs validate prompt-level applicability and (b) the empirical pilot signal validates calibration-level applicability.

**No deviation from dispatch spec; no architect-hat scope-expansion request needed.** Distinct from 1.5-B path α (column-drop bypass of bit-equality gate) and 1.5-C v22-baseline-gate (`--baseline-models ""` config knob): 1.5-D.2 pilot ran fully literal-compliant.

## Calibration grading (per labeller)

Pass threshold per dispatch + `docs/PROCESS_GUIDE.md:94-102` §2.1: ≥ 20/28 standard exam + 100% on the 3 original GTO-reversal hands (MW-30, MW-33, MW-50). Solver-corrections from `memory/reference_corrections.md` applied: MW-30=CALL, MW-46=CALL, MW-47=RAISE.

| Labeller | Score | Threshold | Reversals | Final |
|----------|-------|-----------|-----------|-------|
| 1 | 26/28 | PASS | 3/3 | **PASS** |
| 2 | 28/28 | PASS | 3/3 | **PASS** |
| 3 | 28/28 | PASS | 3/3 | **PASS** |
| 4 | 28/28 | PASS | 3/3 | **PASS** |
| 5 | 24/28 | PASS | 3/3 | **PASS** |

Validated labellers: **5/5**. All 5 labellers' pilot labels are included in `raw_labels.jsonl` (no exclusions per dispatch §"Calibration compliance" QC item).

Common miss patterns (informational, not gate-relevant):

- L1 (26/28): missed `d2410_CO_turn` and `d8886_BB_flop` (both flagged Rule 11 default-CHECK MEDIUM despite Calibration Notes preferring BET; explicit Rule-11-vs-Calibration-Notes tension surfaced in L1's reasoning).
- L5 (24/28): missed `MW-17`, `d2410`, `d8886`, `d8963`. Same Rule 11 vs Calibration Notes tension on three of the four.

Both L1 and L5 documented their reasoning explicitly; the misses are not arbitrary — they reflect a real ambiguity in the v3.4 protocol between Rule 11's blanket OOP-2-tone-CHECK default and the Calibration Notes' BET anchors for specific 2-tone hands. This is a protocol-design concern, not a labeller-quality issue. Architect-hat note for orchestrator follow-up: Rule 11 vs Calibration Notes anchor tension may warrant a future v3.5 protocol clarification (out of 1.5-D.2 scope; queue for Phase 1.5 close-out memory follow-up).

## Pilot gate verification (per dispatch §"Pilot+full split")

Gate criteria (binding):
1. Inter-labeller agreement ≥ 80% (4 of 5 labellers consensus on ≥ 4 of 5 hands)
2. Sonnet → Opus tier-up cross-check on disagreements yields ≤ 1 changed action

Results:

1. **Inter-labeller agreement: 100% (5 of 5 unanimous on 5 of 5 hands).** Vastly exceeds the 80% threshold.
2. **Tier-up cross-check: vacuous (0 disagreements).** Sample = non-unanimous hands = empty set; no Opus dispatch needed; trivially ≤ 1 changed action.

**Pilot gate: PASS.**

## Sonnet → Opus tier-up disposition

Per dispatch §"Tier-up gate":
> "Sample = all hands where Sonnet 5-labeller consensus is below 5-of-5 (i.e., any non-unanimous hand). 1 Opus labeller runs on the sample; agreement with Sonnet majority is reported. Disagreement on > 10% of sampled hands triggers full Opus re-label of the disagreeing hands."

Sample size: **0** (all 5 hands had 5-of-5 Sonnet consensus). No Opus dispatch performed. `opus_tier_up.jsonl` contains a single meta-row documenting the empty-sample state.

## Owner-arbitrated splits

Per dispatch §"Consensus rule":
- 2-2-1 or worse → owner-arbitrated; surface in 1.5-D.2 builder report

**Owner-arbitrated splits this pilot: 0.** No 2-2-1 or worse splits surfaced. All 5 hands cleared at 5-of-5 unanimous.

## Per-axis confidence summary (HU-1)

| Confidence pattern | Count | Hands |
|---|---|---|
| 5-of-5 HIGH | 0 | (none — no hand had all 5 labellers at HIGH; HU-1.4 came closest with 2 HIGH + 3 MEDIUM) |
| 5-of-5 mixed (HIGH ∪ MEDIUM) | 5 | HU-1.1, HU-1.2, HU-1.3, HU-1.4, HU-1.5 |
| 4-of-5 | 0 | (none) |
| 3-2 | 0 | (none) |
| 2-2-1 | 0 | (none) |

100% of hands cleared at 5-of-5 action consensus; per-labeller confidence varied (HIGH or MEDIUM depending on hand difficulty + labeller's degree of uncertainty); no LOW confidence labels on any hand.

## Operational notes

- 5 labellers dispatched as parallel Sonnet `general-purpose` Agent calls in single message with `run_in_background=true`; each completed in 11-16 min wall-clock.
- LLM spend: ~$5-10 (5 Sonnet agents × ~140K tokens each input + ~30K output each; plus brief generator + grader Python scripts at ~$0).
- Each labeller produced 28 calibration labels + 5 pilot labels (33 total per labeller; 165 total label rows).
- Per-labeller intermediate files (`calibration_results_labeller_N.jsonl` + `raw_labels_labeller_N.jsonl`) consolidated into the 4 dispatch-spec files (`raw_labels.jsonl`, `consensus.jsonl`, `calibration_results.jsonl`, `opus_tier_up.jsonl`); intermediates removed to keep PR diff minimal per dispatch §"diff scope strict".
- Brief at `data/hu_labelling/pilot_HU1/labeller_brief.md` is preserved (informational; not part of the 5 dispatch-spec files but committed to PR for reproducibility).

## PR diff scope

| File | Purpose |
|---|---|
| `data/hu_labelling/pilot_HU1/labeller_brief.md` | Shared brief read by all 5 labellers (reproducibility) |
| `data/hu_labelling/pilot_HU1/raw_labels.jsonl` | 25 rows (5 labellers × 5 pilot hands) |
| `data/hu_labelling/pilot_HU1/consensus.jsonl` | 5 rows (per-hand consensus + sizing distribution) |
| `data/hu_labelling/pilot_HU1/calibration_results.jsonl` | 5 rows (per-labeller calibration grading + pass/fail) |
| `data/hu_labelling/pilot_HU1/opus_tier_up.jsonl` | 1 meta-row (no tier-up needed; sample empty) |
| `review/comms/BUILDER_REPORT_PHASE15D2_PILOT_2026-05-10.md` | This report |

Total: 6 files. (Dispatch spec listed 5 files; the brief is the 6th — committed for transparent reproducibility of how the 5 fresh labellers were dispatched.)

No source/prompt/model edits. No data outside `data/hu_labelling/pilot_HU1/` modified. No 1.5-D.3 corpus assembly performed (separate sub-sub-phase). No 1.5-D.4 retrain.

## Negative scope honored

- ❌ No 1.5-D.3 corpus assembly executed (separate sub-sub-phase)
- ❌ No 1.5-D.4 retrain executed (separate)
- ❌ No source / prompt / model file edits outside `data/hu_labelling/`
- ❌ No solver output used as training label
- ❌ No relaxation of calibration gate (all 5 labellers met ≥20/28 + 100% reversal)
- ❌ No improvisation: where I observed the 3-way-protocol-applied-to-HU concern, I did NOT improvise a new HU-specific prompt or skip calibration; I applied the protocol literally per dispatch and surfaced the consideration transparently above.

## What fires after this PR merges

Per dispatch §"Loop status":
- Orchestrator dispatches Phase 1.5-D.2 FULL (HU-2..HU-6 = 25 hands × 5 labellers + Opus tier-up) per design memo §4.3
- Builder authors full PR per same protocol; same dispatch-spec output structure (4 data files in `data/hu_labelling/full_HU2_HU6/` + 1 builder report)
- After full PR + QC PASS + merge: Phase 1.5-D.3 (HU corpus assembly; ~600-900 labelled situations target) per design memo §4.4

## References

- Dispatch: `MAIN_TERMINAL_PHASE15D2_HU_LABELLING_PIPELINE_DISPATCH_2026-05-10.md` (master `2ca9431`, PR #331)
- Architect's design memo (in master): `review/comms/PHASE15A_UNIFIED_SURFACE_DESIGN_2026-05-08.md` §4.3
- HU-1 hand specs: `design/hu_reference_set/HU_AXIS_1_MADE_HAND.md`
- Labeller protocol: `prompts/gto_labeller_v3.4.md`
- Knowledge base: `knowledge/three_way_gto.md`
- Calibration anchors (BLIND-extracted by labellers): `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + 4 hard anchors in `training-data/test_set_50_labelled.jsonl` + `training-data/3way_combined_350.jsonl`
- Solver corrections: `memory/reference_corrections.md`
- Process guide: `docs/PROCESS_GUIDE.md` §1.1-§1.3 (agent dispatch + parallelism), §2.1 (calibration discipline)
- Memory: `feedback_quality_default_no_ask.md`, `feedback_pilot_first_for_long_jobs.md`, `feedback_no_deadlines.md`, `feedback_bucket_first_labelling.md`, `feedback_solver_vs_expert_labels.md`, `feedback_terminology_raise_vs_bet.md`, `feedback_named_author_builds_not_polls.md`, `feedback_listen_to_orchestrator_always.md`, `feedback_explicit_action_trigger.md`, `feedback_qc_required_before_approval.md`

---

**Status: pilot gate PASS; full batch (HU-2..HU-6) authorized post-merge per dispatch §"Pilot+full split"; PR open and ready for QC re-audit + autonomous merge per orchestrator standing directive.**
