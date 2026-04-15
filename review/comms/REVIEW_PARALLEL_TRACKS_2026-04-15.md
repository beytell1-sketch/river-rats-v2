---
date: 2026-04-15
from: Owner (Rupert) + main terminal
to: Builder team
re: Reviews on parallel tracks A, B, D, E (Track C committed as-is)
status: APPROVALS WITH AMENDMENTS — Track A blocker requires investigation
---

# Reviews on Parallel Tracks

## Track A: v2.3 Scope — APPROVE WITH 3 AMENDMENTS

The structure is solid. Three items to address before
implementation:

### Amendment 1 — Reconcile the BET delta inconsistency

The allocation table says +166 BET; the narrative says +155 BET
+ 31 protection BET. Pick one number and make the document
consistent. Likely the narrative double-counts protection BETs
(which are still BET actions). Fix before approval.

### Amendment 2 — `hero_range_percentile = 0.00` is a feature extraction bug, not a labelling problem (CRITICAL)

This is critical. If 10 of 10 MW misses share an extraction
artifact, that's the actual root cause, not bucket-first bias.

Builder must:
1. Investigate the feature extractor for the conditions that
   produce 0.00 on these hands
2. Determine whether v2.2's training data has the same defect
   (likely yes)
3. Decide if v2.3 needs a re-extraction pass on the 385 existing
   hands BEFORE adding the supplement
4. Document this as a Track B-equivalent blocker

If `hero_range_percentile` is broken on a class of hands, the
bucket-first bias diagnosis is wrong — we'd be fixing a
labelling issue that's actually a data issue. **Investigate
this immediately, before any v2.3 hand generation begins.**

### Amendment 3 — Add an explicit calibration gate to v2.3

The plan currently expands the exam from 24 to 28 hands but
doesn't say "must pass before labelling begins." Same gate as
v2.2: 20/24 minimum (or scaled equivalent: 23/28) + all
reversal hands correct. State this explicitly.

### Track B blocker noted
Plan correctly identifies dependency on Track B for the
~166 factory-sourced hands.

---

## Track B: BP Generator Fix — APPROVE BLUEPRINT

Clean diagnosis. The bug was in the batch text formatter, not
the underlying data — JSONL was always correct, the formatter
read `_villain_pos_raw` (single string) instead of
`villain_positions` (list). That makes the fix surgical.

The 4-fix plan is sound:
- Fix 1 (validator on SituationSpec) is the v2.3 blocker
  requirement from memory item 5 — required
- Fix 4 (canonical formatter path) is the structural fix that
  prevents recurrence — required
- Fixes 2, 3 are cleanups that prevent the bug from migrating
  to other batches — required

**Approved. Programmer can implement.** Test-first protocol per
builder's standard. Constraint already documented: do NOT
re-run BP labelling.

---

## Track D: Teaching Handoff — APPROVE

Schema spot-check confirms the export matches the handoff
document. Both file locations populated. 10 fields per row, 385
rows, no schema anomalies. Multi-intention handling correct
(`primary_intention` scalar + `intentions` list). River hands
correctly have empty `street_plan_tags`.

**One small note for teaching team:** the document mentions
"CHECK-over-BET bias may persist in borderline training hands
beyond the 22 corrected cases" — make sure teaching's L3
quality scoring accounts for this. They shouldn't flag every
CHECK-on-marginal-spot as a renderer bug when it might be a
label inheritance.

**Approved as delivered.** Teaching can start Phase 2 work
using this export.

---

## Track E: v2.3 Diagnostic Test Set — APPROVE WITH AMENDMENTS

The four-group structure (mixed zones, BP-pattern, MW-miss
patterns, calibration reversals) is the right diagnostic shape.
Sample size 30-50 is reasonable for a diagnostic instrument.

### Amendment 1 — Add absolute accuracy floor

The 5pp success threshold on a 25-35 hand Groups A+B subset
means 1-2 correct predictions decides pass/fail. That's
noise-sensitive.

Add: v2.3 must hit a minimum absolute accuracy on Groups A+B
(e.g., 70%+) regardless of v2.2 baseline. This prevents a
"5pp improvement from terrible to slightly less terrible" from
passing the diagnostic.

### Amendment 2 — Define Group D regression fallback

The doc flags this as undefined. Add: "if v2.3 regresses on
Group D reversal accuracy by >1 hand, investigate before v2.3
ships — reversal hands are the calibration anchor."

### Group B sourcing
Waits for Track B fix — already noted. The "single session"
inconsistency for Group B ground-truthing is minor; 2 sessions
if needed is fine.

---

## Track C: Vocab dedup
Committed as-is per directive. No review needed.

---

## Summary

| Track | Status |
|---|---|
| A: v2.3 scope | APPROVE WITH 3 AMENDMENTS (BET delta fix, hero_range_percentile investigation, calibration gate) |
| B: Generator fix | APPROVED — programmer implements |
| C: Vocab dedup | Committed, no review |
| D: Teaching handoff | APPROVED |
| E: v2.3 test set design | APPROVE WITH AMENDMENTS (absolute accuracy floor, Group D fallback) |

**Critical priority:** Track A Amendment 2 — the
`hero_range_percentile = 0.00` finding could change everything.
If it's a feature extraction bug, v2.3 might need a
re-extraction phase on existing data, not just a 206-hand
supplement. Builder should investigate this immediately.

**Gate 7:** still pending solver on 10 MW misses. The
`hero_range_percentile` finding might also reframe what those
misses mean — if the feature is broken on those hands, the
model wasn't even given the right input signal.

---

**Builder: address Track A amendments and investigate the
`hero_range_percentile` issue. Other tracks can proceed.**
