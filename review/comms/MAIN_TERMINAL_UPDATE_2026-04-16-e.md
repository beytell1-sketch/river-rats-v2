---
date: 2026-04-16
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Track D scope + Group D reversal sourcing; Phase 2 assembly QA OK to proceed
status: DIRECTIVE
---

# Main Terminal Update — 2026-04-16 (e)

Phase 1 main generation accepted (Track A 483/483 clean).
Track B (v3 prompt) and Track C (calibration exam) accepted.
Two items resolved below.

## 1. Track D — accept 4 nut-blocker candidates, umbrella absorbs rest

Decision: Option (a) in builder's framing. Scope rows 6-7
down from 25 combined target to the 4 confirmed nut-blocker
candidates. Do NOT widen the filter. Do NOT factory-generate
to backfill.

### Rationale

- Widening (option b) redefines the row from "nut-blocker
  semi-bluff" to "drawing hand with some blocker-like feature"
  — different teaching pattern, scope drift.
- Factory-generating (option c) contradicts the curated intent.
  Curated rows specifically want organic real-distribution
  hands, not synthesized shapes.
- The 268-hand UMBRELLA bucket already covers the Section 2
  predicate shape. Drawing hands with `equity_vs_range ≥ 0.35
  ∧ worse_hand_pct ≥ 0.55` sit inside the umbrella and produce
  BET labels for semi-bluff value. That coverage is not lost.
- Supplement total: 420 → 399 (≈5% reduction). Negligible
  class-balance impact.
- The 4 curated hands retain their concentrated nut-blocker
  signal as a real-distribution anchor.

### Execution

- Commit the 4 confirmed nut-blocker candidates as
  `v23_curated_draw_flop.jsonl` and
  `v23_curated_draw_turn.jsonl` (split as the source hands fall
  across streets). If all 4 are flop, commit one JSONL and
  leave the turn file empty/not-generated.
- Update `V23_HAND_GENERATION_PLAN_2026-04-16.md §1.2` table
  entry for rows 6-7: "confirmed count 4, scaled from target
  25, umbrella absorbs remaining coverage per
  MAIN_TERMINAL_UPDATE-e §1."
- Drop the remaining 12 unconfirmed candidates — do not merge
  them as best-effort.

### Phase 7 backup clause

If Phase 7 validation shows an identifiable drawing-signal
gap (e.g., v2.3 regresses on semi-bluff BET spots while
improving on made-hand BET), add a factory sub-pattern to
`generate_factory_batch6.py` targeting nut-blocker semi-bluff
shape and iterate. Do NOT add this now; it's a post-validation
fix, not a pre-training fix.

## 2. Group D reversal finalisation — builder surfaces candidates, owner picks

The 4 remaining Group D hands are owner content (poker-domain
judgment required). Instead of asking owner to hunt blind,
produce a shortlist.

### Task (single programmer call)

Build a candidate list of 10-15 reversal-shaped hands. Each
must be a spot where **CHECK is the correct answer despite
looking similar to the bias signature**, making it a genuine
test that v2.3 hasn't over-learned "bet more often" in
multiway-checked-through contexts.

### Sourcing criteria (stratify across sources)

1. **v2.2 training CHECK labels on near-bias-signature hands.**
   Filter: `facing_bet=0 ∧ num_opponents≥2 ∧ villain_checked_back=1
    ∧ spr≤2.0 ∧ action_label=CHECK` — minus any ONE of the BET-
   triggering conditions (`worse_hand_pct < 0.55` OR
   `villain_range_capped = 0` OR `equity_vs_range < 0.35`). These
   are spots that look like the bias signature but have a real
   reason to CHECK. Target 4-6 candidates.

2. **d-series Pass 2 solver-confirmed CHECK overrides.** Hands
   where Pass 1 majority was BET, Pass 2 reversed to CHECK, and
   solver confirmed CHECK. Canonical reversal shapes. Target 2-4
   candidates.

3. **Solver-mixed spots where CHECK ≥ 40%.** If any solver-sourced
   hands in the supplement (or the 10-20 Section 1 row 11 cohort,
   once generated) show mixed strategy with substantial CHECK
   frequency, those are reversal-ready. Target 2-3 candidates if
   available; skip if not.

### Deliverable

`review/comms/GROUP_D_REVERSAL_CANDIDATES_2026-04-16.md` with:

- 10-15 candidate rows, each: sid, source (training / d-series /
  solver), action history summary, hero cards, board, key features
  (SPR, HRP, worse_hand_pct, villain_range_capped,
  villain_checked_back), label action, one-line "why this is a
  reversal" (which bias-trigger condition fails, or why solver
  leaned CHECK)
- Grouping by source so owner can see the stratification
- Owner picks 4 from the list

### Sequencing

This is a Phase 3 prerequisite (calibration can't run without
the full Group D registry). Run in parallel with whatever else
is active. Target: candidate list lands within 30 min of the
programmer call starting.

Owner picks 4 from the list — ~5-10 min async. Registry gets
extended (no code change per Track C).

## 3. Phase 2 assembly QA — proceed

Builder flagged Phase 2 assembly QA as "can do without further
direction." Correct. Proceed with the dry-run on the 10 generated
JSONLs (combined schema, dedupe, predicate splits).

Deliverable: `review/comms/PHASE_2_ASSEMBLY_QA_2026-04-16.md`.

Hard stop: will NOT progress to production labelling. This is
QA only.

## 4. Sequencing check

Current state after this directive:

| Track | State |
|---|---|
| Phase 1 generation | ✅ 483/483 clean + 4 curated |
| v3 prompt | ✅ committed |
| Calibration exam (23/28) | ✅ committed, 10/10 tests |
| Group D registry | ⏳ builder shortlist → owner picks 4 |
| Phase 2 assembly QA | 🟢 builder proceeds |
| Phase 3 calibration gate | ⏸️ waits on Group D finalised |
| Phase 3.5 pilot | ⏸️ waits on Phase 3 pass |
| Phase 4 production labelling | ⏸️ waits on 3.5 pass |

## 5. Owner touchpoints (narrowed)

- Group D pick (4 from shortlist) — 5-10 min async
- Curated-draw spot-check — already fed forward; the 4 confirmed
  candidates are the deliverable. Owner can skim the candidate
  doc if interested; not gating.
- Solver sessions for row 11 + auto-enqueue reserve — at owner
  pace, non-blocking
- Phase 3.5 pilot spot-check (3-5 hands) — when pilot report lands
- Phase 7.3 solver validation (8 MW misses) — at v2.3 ship gate
- v2.3 ship sign-off — when all gates pass

Everything else runs.
