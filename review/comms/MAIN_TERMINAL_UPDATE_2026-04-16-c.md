---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Add Phase 3.5 — Pilot labelling review (qualitative prompt-behaviour gate)
status: DIRECTIVE — modifies V23_HAND_GENERATION_PLAN_2026-04-16.md §3-§4 sequencing
---

# Main Terminal Update — 2026-04-16 (c)

Inserting a new phase between calibration (Phase 3) and
production labelling (Phase 4). Owner-raised gap: the
calibration exam is an accuracy gate, not a prompt-behaviour
gate. Passing 23/28 does not prove the panels are reasoning
the way the v3 prompt intends — only that they got the right
answers on known hands.

A prompt can produce correct action predictions on calibration
spots while still (a) not firing the override clause, (b)
ignoring Scope §3 additions, (c) regressing on reasoning
clarity, or (d) reducing inter-panel variance in one place and
inflating it in another. Catching this after 400 hands of
production labelling is expensive. Catching it on 15-20 hands
is cheap.

## New Phase 3.5 — Pilot labelling review

### Sequencing

```
Phase 3 (calibration gate) — must pass 23/28 + 100% reversals
    ↓
Phase 3.5 (pilot review) — NEW — must pass qualitative gate
    ↓
Phase 4 (production labelling — ~400 hands)
```

Phase 4 does not begin until Phase 3.5 passes.

### 3.5.1 — Pilot hand selection

Sample 15-20 hands from the generated buckets (Phase 1 output)
that are **not in the calibration exam**. Stratify to ensure
the pilot exercises the new prompt features:

- 6-8 hands matching the Section 2 predicate (should trigger
  the Stream B.2 override clause)
- 3-4 hands NOT matching the predicate (override clause
  should NOT fire — negative control)
- 2-3 hands exercising Scope §3 additions A-D (whichever the
  architect lands — these should cite the new guidance)
- 2-3 reversal-shaped hands (boundary spots, MEDIUM confidence)

Total: 15-20 hands. Same factory/curated buckets as Phase 1
output; no separate generation.

Deliverable: `review/comms/PHASE_3_5_PILOT_SAMPLE_2026-04-16.md`
listing the chosen hand IDs and why each was picked.

### 3.5.2 — Run full pipeline

- Pass 1: 4 independent panels label all pilot hands
- Pass 2: 2 review panels handle disagreements
- Assembly: aggregate labels + reasoning traces
- **Preserve ALL reasoning text verbatim** — `expert_reasoning`,
  `factor_conflicts`, `alternatives_considered`, Pass 2
  override-KB-justification fields

Deliverable: `training-data/v23_pilot_labelled.jsonl` (not
merged into main supplement CSV yet).

### 3.5.3 — Qualitative review (the gate)

Builder reads the reasoning output against a five-point
checklist. This is NOT an accuracy check — accuracy was Phase 3.

**Gate criteria:**

1. **Override clause behaviour.**
   - On the 6-8 predicate-matching hands: does Pass 1 cite
     the override (by text or by reasoning that invokes its
     preconditions)? Target: ≥ 80% of predicate-matching
     hands show explicit override engagement.
   - On the 3-4 non-predicate hands: does Pass 1 NOT fire the
     override? Target: 100% — the clause should not leak to
     spots where its preconditions don't hold.

2. **Scope §3 additions engagement.**
   - Do Pass 1 panels cite the new guidance on the 2-3 hands
     selected for this? Target: ≥ 80% cite at least one §3
     addition.

3. **Inter-panel variance.**
   - On the predicate-matching hands, do the 4 panels agree
     more than they did in v2.2? Compare: if v2.2's equivalent
     MEDIUM-confidence spots had 3/4 or 2/2 splits, v2.3
     should trend toward 4/4 on the override spots.
   - Target: ≥ 70% of predicate-matching pilot hands show 4/4
     panel agreement.
   - Flag (do not auto-fail): any hand where v3 has MORE
     variance than v2 would have on the same shape. Investigate.

4. **Pass 2 engagement with new guidance.**
   - On any pilot hand that reaches Pass 2, does the reviewer
     cite v3 prompt sections (override clause, §3 additions)
     rather than reverting to v2-era reasoning?
   - Target: 100% of Pass 2 decisions cite v3 guidance where
     applicable. Failures here suggest Pass 2 reviewers didn't
     read / absorbed the new prompt.

5. **Reasoning quality + coherence.**
   - No grammatical/structural regressions vs v2
   - No template-like repetition (panels writing the same
     boilerplate across hands)
   - `factor_conflicts` and `alternatives_considered` remain
     specific to the hand, not generic

**Pass criteria for the gate:**

- Criteria 1, 2, 4 meet their targets → PASS
- Criterion 3 target met OR documented increase-in-variance
  investigated and explained → PASS
- Criterion 5 meets a qualitative "no regression vs v2" bar
  → PASS

Any criterion failing → Phase 3.5 FAIL → return to prompt
redesign.

### 3.5.4 — Failure handling

If Phase 3.5 fails, do NOT proceed to Phase 4. Instead:

- Identify which criterion failed and why
- Revise the v3 prompt (override clause wording, §3 addition
  phrasing, Pass 2 instructions)
- Re-run Phase 3 calibration on revised prompt
- Re-run Phase 3.5 pilot on revised prompt (new hands, not
  the same pilot set — don't train-on-the-test)
- Loop until pass

Document each iteration in
`review/comms/PHASE_3_5_PILOT_ITERATION_<N>_2026-04-16.md`.

### 3.5.5 — Owner touchpoint

The pilot review is qualitative and benefits from owner eye.
After builder's review lands, owner spot-reads the reasoning
traces for 3-5 of the pilot hands. Quick sanity check — not
a full review. If owner sees anything the builder missed,
back to prompt redesign.

This is a small touchpoint (~30 minutes). Worth it.

Deliverable:
`review/comms/PHASE_3_5_PILOT_REVIEW_2026-04-16.md` — builder's
review + gate verdict. Owner adds a comment section confirming
or flagging.

## Why this phase exists

The v3 prompt encodes two kinds of changes:

- **Correctness fixes** (override clause, §3 additions) — these
  have to actually fire. If the panels read the new prompt and
  still reason in v2 patterns, the label signal we designed
  doesn't reach the training data.
- **Quality maintenance** (no coherence regression) — prompt
  edits can introduce subtle problems (grammar, redundancy,
  confused sequencing) that don't affect accuracy on 28
  calibration hands but accumulate across 400 production
  hands.

Phase 3 catches neither. Phase 3.5 catches both before they
get amplified 20×.

## Effort cost

- Pilot generation + labelling: 15-20 hands × 4 panels = 60-80
  agent calls (Pass 1) + 0-10 Pass 2 calls. ~1-2 hours with
  parallel panels. Same unit cost as any small label batch.
- Builder qualitative review: 1 builder call reading through
  the traces. 1-2 hours.
- Owner spot-check: 30 minutes.
- Total added latency: half a day. Value: avoid discovering a
  prompt defect after 400 hands of labelling.

## Updated phase sequencing

| Phase | Content | Gate |
|---|---|---|
| 0 | Pre-flight | Tests + schema + disk + git + v3 prompt exists |
| 1 | Generation (~420 hands) | Per-bucket volume targets met |
| 2 | Assembly QA | JSONL schemas clean |
| 3 | Calibration (28 hands) | 23/28 + 100% reversals |
| **3.5** | **Pilot labelling review (15-20 hands)** | **Qualitative 5-point gate + owner spot-check** |
| 4 | Production labelling (~400 hands) | Pass 1 + Pass 2 complete |
| 5 | Assembly (v2.3 training CSV) | Schema preflight passes |
| 6 | Training | CV, holdout, early-stop numbers logged |
| 7 | Validation | All 5 ship-gate criteria pass |

## Documentation update

Builder: update `V23_HAND_GENERATION_PLAN_2026-04-16.md` in
place with Phase 3.5 inserted (same structure as the other
phases: scope, deliverables, gates, stop conditions). Commit
as "Add Phase 3.5 pilot review per owner directive."

## What does NOT change

- All other approvals from MAIN_TERMINAL_UPDATE_2026-04-16-b
  stand.
- Phase 0 still runs now.
- Phases 1 and 2 are unaffected.
- Phase 3 calibration gate is unchanged.
- Phase 4 through 7 are unchanged, they just wait on Phase 3.5.

---

**Builder: insert Phase 3.5 into the plan, continue Phase 0,
then execute phases in order. Phase 4 gates on Phase 3.5
passing.**
