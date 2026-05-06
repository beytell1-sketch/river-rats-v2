---
date: 2026-05-06
from: Main terminal (orchestrator)
to: QC stream
re: Phase 12.5H-D — corpus QC sweep on combined 694-hand corpus; fire 4-gate sweep + design_action verification
status: TRIGGER — fire now
---

# Phase 12.5H-D — corpus QC sweep

12.5H-C LABELS FINAL merged at master `90e17dc`. New corpus state: 694 hands total (604 from 12.5E + 90 from 12.5H) with consensus labels. Per design §8.D: QC runs 4 gates from §7 on the merged-state.

## QC stream — what you audit (4 gates per design §7 + design_action verification)

### Gate G1 — join-cardinality (combined corpus)

- Join key: `pilot_hand_id`
- Verify cardinality: `pilot_hand_id` count in combined situations files = 694 unique IDs (no collisions)
- Verify labels join: combined labels = 694 unique IDs matching situations
- Pass: 694/694, zero collisions across cohorts (existing 604 vs new 90)

### Gate G2 — distribution sanity

- Class distribution post-merge: 694 hands across {FOLD, CHECK, CALL, BET, RAISE}
- Verify no class < 5% (informational)
- 12.5H-C added: T7-ext air-driven mix (4 CALL + 7 RAISE), T8' CHECK uniform, T9' BET uniform, T10' RAISE + 1 CALL canonical, T-RAISE-stabilize RAISE, T-CONTROL per design_action (5 buckets)
- Verify median consensus_confidence preserved or improved vs 12.5E baseline

### Gate G3 — duplicate detection (cross-cohort)

- Verify zero exact-duplicate situations between the new 90 and existing 604 on (board, hero_cards, action_history, hero_position)
- Builder self-checked at PR #181; QC re-verifies at corpus-QC scope

### Gate G4 — labeller-drift detection

Per design §7 G4: compare new 90 (12.5H-C labels) vs existing 604 (12.5E + earlier).
- Median consensus_confidence shift
- Per-class confidence shift
- T-CONTROL buckets specifically: same-action match against `design_action` field (per TC-X T8 schema gap fix from PR #150 — design_action now encoded per hand for exact same-action match)

Both cohorts used Sonnet × 5 protocol; same v3.4 prompt; expected drift drivers are: corpus-design template specificity (12.5H is more E-DIST/MW-XX targeted than 12.5E); seed-volatility-fix (T-RAISE-stabilize); v3.4 Fix 2.1.1 floor.

Pass: drift documented + within design §7 G4 thresholds.

### NEW G5 — cap-binding pre-flight (per QC TC-X-CAP-BINDING-PRE-CHECK)

For the 694-hand corpus, compute `mean(class_count) / min(class_count)` against any cap parameter. Document for forward reference (12.5H-E re-train + 12.5G-equivalent decisions).

This is forward-looking; not a HOLD condition for 12.5H-D. Just a pre-emptive computation per the test class registry entry from 12.5G empirical refutation.

### Plus design_action verification (T-CONTROL audit)

Per dispatch §"Cleanup items" from PR #168 + PR #150 NEW NIT: T-CONTROL hands now encode `design_action` per row. Verify:
- All T-CONTROL hands have explicit `design_action` field
- Same-action match rate ≥ 70% on T-CONTROL controls (G4 implementation)

If <70%, surface as labeller-drift signal.

## Cleanup items to document (NIT carry-forward — surface, do NOT block)

Same 3 NITs from prior phases ride along until 12.5H-E builder cleanup window:
1. NIT-1 from PR #139 (PLAN §3.T8 wording 36→22+14 then revised to 90 across 6 templates) — at 12.5H-E
2. PILOT_595 design_note cosmetic (TPTK→top-two-pair) — at 12.5H-E
3. NIT-1 from PR #148 (BUILDER_REPORT preserved-original stale filename) — at 12.5H-E

## Output

`REVIEW_QC_PHASE125H_D_CORPUS_QC_2026-05-06.md` to `review/comms/`. APPROVE or HOLD.

## Sequencing on QC verdict

- APPROVE → orchestrator dispatches 12.5H-E re-train (LEAD-PROGRAMMER named author)
- HOLD on G1-G3 → route to LEAD-PROGRAMMER for amendment
- HOLD on G4 drift → orchestrator decides per-magnitude

## What's blocked / what's queued

**Blocked:**
- 12.5H-D output → QC fires now per this trigger
- 12.5H-E dispatch → on 12.5H-D APPROVE
- 12.5H-F gate evaluation → on 12.5H-E PR merge

**Queued:**
- TC-X-DISPATCH-PREDICTION-VERIFICATION formalization (already triggered per PR #183; queued for QC institutional-memory commit)
- 3 prior NITs (cleanup at 12.5H-E)
- All other items per prior queues

## References

- 12.5H-C LABELS FINAL: master `690ca8f` (PR #184)
- 12.5H-C labelling round merged: master `90e17dc` (PR #181)
- 12.5H-C QC verdict: master `14ac162` (PR #183)
- 12.5H-A design (12.5H-D scope): master `858b032` (PR #165)
- 12.5E-D precedent (4-gate sweep + drift detection): master `4070a11` (PR #150)
- Memory: `feedback_explicit_action_trigger.md` (this comm IS the trigger), `feedback_qc_routing_when_standalone_active.md`, `feedback_qc_required_before_approval.md`

**Status: 12.5H-D TRIGGER posted. QC fires 4-gate sweep + design_action verification + G5 cap-binding pre-flight on combined 694-hand corpus.**
