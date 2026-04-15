---
date: 2026-04-15
from: Owner (Rupert) + main terminal
to: Builder team
re: Parallel work tracks — Gate 7 decision pending solver, 5 productive tracks in parallel
status: DIRECTIVE — start immediately, all tracks can run in parallel
blocks on: owner solver time for 10 MW misses (Gate 7 decision)
---

# Parallel Work Tracks While Gate 7 Awaits Solver

Owner's solver time is constrained today. The Gate 7 decision
(ship v2.2 / solver-verify 10 MW misses / iterate) waits. Five
productive tracks can run in parallel without blocking on that
decision. All are Gate 7-independent — they support either
shipping or iterating.

---

## Track A: v2.3 scope document (highest value)

### Who
- **Architecture Expert** (design) — drafts structure
- **ML Architect** — validates technical feasibility
- **GTO Expert** — reviews poker content
- **Owner** — reviews and approves scope before implementation

### What to deliver
A single document: `review/comms/PLAN_V23_SCOPE_2026-04-15.md`
that specifies:

**Section 1: The 206-hand aggression supplement**
- Allocation table: which hand buckets, which action targets,
  which streets
- Source: factory generation, curated from existing hands, or
  solver-sourced
- Distribution: how many BET-in-mixed-zones, how many value
  RAISE, how many protection BETs, etc.
- Integration: total v2.3 training size (385 + 206 = 591) and
  class rebalancing implications

**Section 2: Bucket-first CHECK bias diagnosis**
- Extract common features from the 10 MW misses + the 4 d-series
  solver mixed spots (d4312, d8886, d8963, BP5_01)
- What's the pattern? Board texture? Position? Villain
  composition shape? SPR? Hand bucket distribution?
- Document the empirical signature of the bias

**Section 3: Prompt guards for gto_labeller_v3.md**
- Specific language to add addressing the passive lean
- Draft the additions inline (not a separate artifact)
- Reference KB sections and calibration patterns
- Explicit instruction: do NOT add SPR<2 semi-bluff guard
  (v2.3 backlog item 6 was invalidated)

**Section 4: Solver ratio for v2.3**
- Target 15-20% of hands (~90-120 at 591 total)
- Structure: queue-based triggers or batch?
- Owner time budget per session
- Triggers for auto-enqueue (confidence thresholds, mixed
  strategy flags, etc.)

**Section 5: v2.3 calibration exam additions**
- Add 3-4 solver-mixed hands to the calibration exam
- Specific hands from the current 10 MW misses + d-series mixed
- Test: does agent consistently pick passive leg of mixed
  strategies?

**Section 6: v2.2 lessons applied**
- Pass 2 override discipline rule (v2.3 backlog item 8 reframed)
- No new architecture phases — v2.3 uses same 4+2 team structure
  as v2.2
- Solver used for pattern detection + clear-wrong cases, not
  per-hand arbitration

### Constraints
- No code changes in this track — specification only
- ~2-3 agent calls total (architect + ML + GTO review)
- Deliverable blocks nothing else in this directive
- Owner reviews as a Gate before implementation begins

### Not in scope
- Don't draft v3.0 action distribution work here (it's in v2.3
  backlog item 1 — separate document)
- Don't specify implementation details for the generator fix
  (Track B handles that)

---

## Track B: BP generator fix (blocking v2.3 data generation)

### Who
- **Architecture Expert** — locates the defect, writes blueprint
- **Programmer** — implements from blueprint
- **Tester** (optional) — writes the regression test first per
  test-first protocol

### What to deliver
1. Root cause diagnosis committed to
   `review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md`
2. Fix committed to `river-rats-core/situation_factory.py` (or
   wherever the bug lives)
3. Regression test in `tests/` that fails on the old behaviour
4. Validator in `situation_factory.py` per v2.3 backlog item 5:
   fail at generation if `len(villain_positions) < num_opponents`
5. Verification run: re-run the existing 185 BP situation
   generator with the fix, confirm villain lists are complete
   (do NOT re-run labelling — just regenerate the situations)
6. Commit message references v2.3 backlog item 5

### Process
Follow the standard test-first → blueprint → implement pattern:
1. Architect reads `situation_factory.py`, finds the code path
   that dropped the 2nd villain seat
2. Architect writes diagnosis document + blueprint
3. Owner reviews blueprint (5-10 min read)
4. Programmer writes regression test first (must fail)
5. Programmer implements fix (test now passes)
6. Programmer adds the num_opponents validator
7. Full test suite runs (must pass)
8. Commit

### Constraints
- Do NOT re-run labelling on regenerated situations — v2.2 labels
  are locked pending Gate 7
- Fix is standalone — doesn't depend on v2.3 scope decisions
- ~2-3 agent calls (architect + programmer + optional tester)
- Can commit before v2.3 scope is finalised

### Why not wait for v2.3
The bug is in production code. Any v2.3 supplement generation
will inherit the defect. Fix upstream before it re-contaminates.

---

## Track C: Vocab audit dedup (cleanup)

### Who
- **Programmer** only

### What to deliver
1. Fix the aggregation logic in whatever script produces
   `v2_2_vocab_audit.json` — currently treats dict objects as
   keys instead of extracting the `name` field
2. Clean up the 3 `proposed_tags` entries (all variants of
   `give_up_no_equity` / `give_up`)
3. Merge them into `pot_control` in the training data per Gate
   6 decision (builder already has this approved)
4. Regenerate `v2_2_vocab_audit.json` with correct aggregation
5. Verify: 6 intentions, 10 street_plan_tags, 0 proposed_tags
6. Commit

### Constraints
- Small track, 1 agent call
- No scope decisions — Gate 6 already decided the merge
- Training data modification: the 3 proposed_tag labels need to
  flip to `pot_control` in `training-data/v2_2_training.csv` if
  they appear in the intentions column

### Not in scope
- Don't change the labelling prompt vocabulary — that's v2.3
- Don't retroactively relabel any hands — just merge the tag
  strings in the existing data

---

## Track D: Teaching handoff prep

### Who
- **Programmer** — exports data
- **Architecture Expert** — writes handoff note
- **Teaching team** (recipient) — receives and consumes

### What to deliver
1. `training-data/v2_2_enriched_for_teaching.jsonl` — one row
   per hand with:
   - situation_id
   - consensus action (final, post-Phase 3.5H)
   - hand_bucket (consensus)
   - intentions (list)
   - primary_intention
   - street_plan_tags (if flop/turn)
   - feature_attention (union T1-T6, PRIMARY/CONFIRMED/DISCOVERED
     level preserved)
   - difficulty (consensus)
   - reasoning (consensus text — may aggregate from 4 teams)
   - the full 54-feature vector
   
2. `review/comms/TEACHING_HANDOFF_V2_2_LABELS_2026-04-15.md` —
   brief handoff note explaining:
   - Schema and where data came from
   - The 22 label changes from Phase 3.5H (so teaching can
     invalidate any renderer testing that used old labels)
   - How to interpret multi-intention hands (primary vs
     supplementary)
   - Feature_attention level semantics (PRIMARY drove decision,
     CONFIRMED verified, DISCOVERED caught by bottom-up scan)
   - Any known caveats (the 10 MW misses if relevant to teaching
     reviews)

3. Copy the enriched JSONL to both locations:
   - `river-rats-v2/training-data/v2_2_enriched_for_teaching.jsonl`
   - `river-rats-teaching/data/v2_2_enriched.jsonl` (create the
     `data/` directory if needed)

### Constraints
- Do NOT change v2.2 labels — export only
- Handoff note should NOT recommend teaching team actions —
  they'll design their own response
- 1-2 agent calls total

### Why now
Teaching team has been building L3 renderer v2 aligned with
Phase 3 output. They've been using placeholder data. Real data
unblocks their Phase 2 (quality validation) work.

---

## Track E: v2.3 diagnostic test set design

### Who
- **GTO Expert** — identifies hand patterns to include
- **Architecture Expert** — test set structure and file format
- **Owner** — reviews design; ground-truths hands with solver
  later (not today)

### What to deliver
A design document (not implementation):
`review/comms/PLAN_V23_DIAGNOSTIC_TEST_SET_2026-04-15.md`

**Section 1: Purpose**
- Compare v2.2 vs v2.3 on a test set designed to surface the
  specific biases we're correcting
- Anchors: FB-40 and MW-50 stay as stable comparators
- New: 30-50 hand diagnostic set focused on mixed strategies

**Section 2: Hand patterns to include**
- 10-15 BET-CHECK mixed zones (where solver output contains
  both actions)
- 5-10 BP-pattern hands with full villain info (factory-generated
  post-fix)
- 10-15 passive-lean patterns extracted from the 10 MW misses +
  d-series mixed spots
- 5 calibration reversals (similar to MW-30/33/50)

**Section 3: Sourcing strategy**
- Factory generation? Existing pool? Solver-sourced?
- Criteria for inclusion
- Expected difficulty distribution

**Section 4: Ground-truth process**
- Owner runs each hand in GTO Wizard
- Records: primary action + frequency + any mixed actions
- Pre-flight: sequences validated, bet sizes match solver options
- Estimated owner time: ~2-3 hours over a dedicated session

**Section 5: Success criteria**
- v2.3 vs v2.2 on the diagnostic set — show improvement on
  mixed-zone accuracy
- Not used as a ship gate — pure diagnostic

### Constraints
- This track is DESIGN ONLY. No solver time needed today.
- Owner reviews design before any hand generation begins
- Implementation + ground-truthing happens when solver time is
  available
- 2-3 agent calls (GTO + architect + review)

### Not in scope
- Don't include Action Distribution (v3.0) hands here — that's
  separate
- Don't design the v2.3 training supplement here — that's
  Track A Section 1

---

## Agent allocation summary

| Track | Agents | Type | Can start now? |
|---|---|---|---|
| A: v2.3 scope | 2-3 | Architecture + ML + GTO | YES |
| B: Generator fix | 2-3 | Architecture + Programmer + Tester | YES |
| C: Vocab dedup | 1 | Programmer | YES |
| D: Teaching handoff | 1-2 | Programmer + Architect | YES |
| E: Test set design | 2-3 | GTO + Architect | YES |
| **Total** | **~10-13** | | All parallel |

All 5 tracks can launch immediately. None block any other. Each
produces a reviewable artifact.

## Owner review sequence (when solver time becomes available)

1. **Track A v2.3 scope** — review structure and approve before
   v2.3 implementation
2. **Track B generator fix** — review blueprint before
   implementation
3. **Track D teaching handoff** — spot-check the enriched JSONL
   export for sanity
4. **Track E test set design** — approve before hand sourcing
5. **Track C vocab dedup** — commit as-is, no review needed

## What this directive does NOT cover

- Gate 7 decision (ship/iterate) — pending solver on 10 MW misses
- v3.0 Action Distributions — separate v3.0 backlog (item 1)
- Pass 2 architectural redesign — v2.3 scope document addresses
- Intention prediction model (Model 2) — v2.3 experiment, not
  covered here
- Teaching L3 Phase 2 work — teaching team drives that, Track D
  just unblocks them

---

**Builder: launch all 5 tracks in parallel. Report when each
produces its artifact. Owner reviews incrementally — no need
to wait for all 5 to finish before reviewing the first one.**
