---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder
re: v2.3.2 label red-flag → Path A: accept all 39
status: DIRECTIVE — proceed to retrain with all 39 labels
---

# Red-Flag Triage — Path A: Accept All 39

## Decision

**Accept all 39 labels. Proceed to retrain.**

## Why — the red-flag was a false positive

The ">3 CHECK/CALL of 40" threshold was designed to catch
**panel drift** (panels wrongly labelling CHECK when BET is
correct). That's NOT what happened.

What actually happened:
- All 4 CHECKs on one concentrated texture: AhAd on Qs5s7s2h
  (monotone spades, hero no spade blocker)
- Panel reasoning consistent across batches: "three spades + no
  blocker + SPR 1.11 + eq 0.56 → bluff-catch, not value"
- Modern solver theory supports this — it's a genuine
  mixed-strategy zone at the value/bluff-catch threshold
- Panel disagreement across batches on the same shape (one BET
  MEDIUM, others CHECK HIGH) CONFIRMS the mixed zone rather
  than undermining label quality
- Litmus seeds both BET HIGH (AA, KQ) — target class protected

Panels reasoned per-hand on poker merits. That is the hard-rule
principle (feedback_no_manual_overrides_in_labelling.md) working
as intended.

## Why A over B / C / D

**B (re-generate excluding monotone-no-blocker):** narrowing the
predicate to exclude spots where panels would CHECK is selection
bias against honest labels. Effectively a predicate-based
override — same class as a static override, different layer.
Rejected.

**C (drop the 4 CHECK rows):** pure label manipulation. Exactly
the "prune uncomfortable labels" pattern the hard rules warn
against. Rejected.

**D (replace 4 CHECKs with 4 new BET-correct specs):** cherry-
picking specs you know will come back BET. Violates
panels-reason-per-hand principle. Rejected.

**A (accept all 39):** honest labels, bidirectional counter-
examples in the subspace. Model learns BOTH "value-in-checked-
through → BET" (35 rows, the primary goal) AND "overpair no-
blocker monotone → CHECK" (4 rows, a nuanced texture-specific
refinement). This is MORE information, not less. Correct per
both hard rules (real counter-examples in the subspace + panels
reason per-hand).

## The factory predicate gap you surfaced is a real insight

`is_made=1 AND eq>=0.55` captures hand strength but not texture-
specific vulnerability. Logging it for v2.4 consideration:

- Future training-data generators should consider texture
  modifiers (monotone + blocker state, paired-board + overpair
  strength, etc.) in addition to equity gates
- Not a v2.3.2 blocker — the 4 honest CHECKs teach the nuance
  without needing a predicate upgrade right now
- Worth a note in the v2.3.2 manifest as "future work" per §5.1

## Proceed checklist

1. Retrain on all 695-ish rows including all 39 v2.3.2 value
   labels (35 BET + 4 CHECK)
2. Full 4-tier gate eval per directive-o:
   - Standard: FB-40 ≥ 72.5%, MW-50 ≥ 84.0%, holdout, CV
   - Air litmus + 20-sweep (protects Layer 2 / v2.3.1 fix)
   - Value litmus + 20-sweep (protects v2.3.2 balance)
   - Self-play systemic (the gate that caught v2.3.1)
3. STOP-and-report on any miss
4. Manifest per §5.1 with predicate-gap note for v2.4

## Meta-note on red-flag thresholds

For future directives: distribution-count thresholds like ">3
CHECK of 40" are orientation signals, not verdicts. A trip
means "audit panel reasoning," not "reject labels." Panel
reasoning is the authoritative test. If panels reasoned per-hand
on poker merits, the labels are honest regardless of count.

I'll apply that lens on future thresholds. Thank you for the
clear reasoning-audit — that's exactly the "STOP and report"
discipline this system needs.

Go.
