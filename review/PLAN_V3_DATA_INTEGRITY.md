# Plan: v3 Data Integrity — RAISE Validation, Action Audit, Label Correction

**Date:** 8 April 2026
**Status:** AWAITING OWNER APPROVAL — nothing starts until approved
**Trigger:** v3 failed Gate 2.4 (31/40 raw, MW-20 regression). Root cause:
batch 2 labels contaminated by solver-derived KB rules. Action sequence
error also found (Hand C: missing BTN action before hero decision).

---

## Governing Principle

Every training label must be reachable by reasoning the model can learn
from its 48 features. If the explanation requires information not in the
feature vector (suit-specific blockers, fold equity calculations, range
composition nuances), the label is wrong FOR OUR MODEL — even if it's
correct poker. Solver data verifies and researches. It never labels.

See: review/FEEDBACK_SOLVER_LABELS_DANGER.md

---

## Phase 0 — RAISE Label Validation

**Goal:** Determine which of the 9 "KEEP" RAISE labels from the batch 2
analyst review are defensible from feature-visible logic alone.

**Why this is Phase 0:** If we can't justify a RAISE from the features,
no amount of action sequence fixing or retraining will make the model
learn it correctly. This must be settled first.

### Team

| Agent | Task | Scope |
|-------|------|-------|
| GTO Analyst A | Review KEEP hands 1-5. For each hand, write the case for RAISE using ONLY the 48 features. No blocker logic unless flush_block_pct captures it. No fold equity the features can't represent. Verdict: DEFENSIBLE or NOT DEFENSIBLE. | 5 hands |
| GTO Analyst B | Review KEEP hands 6-9. Same brief. | 4 hands |
| Independent Reviewer | Check both analysts' reasoning. Flag any hand where the justification smuggles in solver logic or non-feature information. | All 9 hands |

### Deliverable

A table per hand:

| Hand | Current label | Feature-visible reasoning for RAISE | Verdict | If NOT DEFENSIBLE: recommended label |
|------|--------------|--------------------------------------|---------|--------------------------------------|

### Gate

Owner reviews the table and approves each verdict before Phase 1 starts.
Any DEFENSIBLE verdict the owner disagrees with → relabel per owner
judgment. Any NOT DEFENSIBLE verdict → label changes to the analyst's
recommended alternative (CALL or FOLD).

---

## Phase 1 — Action Sequence Audit

**Goal:** Verify that every training situation has correct positional
action ordering. The Hand C bug (hero decision placed before BTN acts)
may be systemic.

**Why this follows Phase 0:** Phase 0 determines which labels are valid
in principle. Phase 1 determines which situations have valid data. Both
must pass before we can retrain.

### Team

| Agent | Task | Scope |
|-------|------|-------|
| Architect A | Audit SituationFactory code: how does action_history map to features? Does it correctly handle OOP check → villain bet → other villain acts → hero decision? | Code review |
| Architect B | Audit reference_evaluator.py: how are reference hands constructed? Same action sequence concerns. | Code review |
| Auditor A | Audit batch 2 factory boards 1-15: verify action_history matches correct positional order. | 15 boards |
| Auditor B | Audit batch 2 factory boards 16-30. | 15 boards |
| Auditor C | Audit batch 1 factory boards (PA_Board and CALL_Board specs). Split further if count exceeds 15. | All batch 1 boards |
| Auditor D | Audit self-play generated data (sample from 3way_combined_350.jsonl). Confirm self-play path handles action ordering correctly. | Sample of 50 |
| Independent Reviewer | Review all findings from all auditors and architects. | All |

### Checklist per board

1. **Positional order:** On each street, do players act in correct
   positional order? (SB first postflop, then remaining players in
   position order)
2. **Missing actions:** If hero is OOP and checks, is that check in
   action_history? If a villain calls between bettor and hero's
   decision, is that call recorded?
3. **num_callers_to_bet:** If a villain calls before hero acts, does
   the feature reflect that caller?
4. **facing_bet vs facing_raise:** Is the action correctly classified?
5. **"Still to act behind" problem:** Any situation where the design
   says a player is "still to act" at hero's decision — verify whether
   that player actually acts BEFORE hero in the real positional order.
6. **Hero position vs action timing:** For every OOP hero situation,
   verify hero's decision point is AFTER all players between the bettor
   and hero have acted.

### Deliverable

Report listing every board with action sequence issues:

- **CRITICAL:** Missing action that changes feature values
- **MODERATE:** Wrong ordering but features happen to be correct
- **CLEAN:** No issues

### Gate

Owner reviews the audit report. Any CRITICAL finding blocks retraining
until the affected situations are corrected or removed.

---

## Phase 2 — Label Corrections

**Goal:** Apply corrections from Phase 0 (RAISE verdicts) and Phase 1
(action sequence findings). Produce clean training data.

**Scope determined by Phase 0 + Phase 1 findings.** Cannot be planned
in detail until both phases deliver.

### Expected actions

1. Flip NOT DEFENSIBLE RAISE labels to analyst-recommended alternatives
2. Remove or regenerate situations with CRITICAL action sequence errors
3. Recalculate features for any situations where action_history is
   corrected (features derived from action must be recomputed)
4. Re-run leakage check (Gate 2.2) on corrected data
5. Document all changes: what was changed, why, evidence

### Team

| Agent | Task |
|-------|------|
| Programmer A | Apply label corrections to CSV |
| Programmer B | Regenerate or remove action-sequence-broken situations |
| Programmer C | Re-extract features for corrected situations |
| Programmer D | Run leakage check (Gate 2.2) |
| Independent Reviewer | Verify corrections match Phase 0/1 findings |

### Gate

Owner reviews corrected dataset before retraining.

---

## Phase 3 — Retrain v3.1

**Goal:** Train on corrected data. Same model config as v3 (from-scratch,
48 features, cap 3.0). Only the data changes — one variable at a time.

### Team (Process Guide Section 6)

| Step | Agent | Task |
|------|-------|------|
| 1 | ML-architect | Review corrected data, confirm training config is unchanged, present plan |
| 2 | Owner | Approve training plan |
| 3 | Architect | Blueprint any code changes needed (if features were recomputed) |
| 4 | Programmer | Implement and run training |
| 5 | Reviewer | Gate 2.3 (feature importance) + Gate 2.4 (reference evaluation) |
| 6 | Owner | Approve or reject model |

### Gate

- Gate 2.3: feature importance (same thresholds, owner override on
  dormant features still applies)
- Gate 2.4: reference evaluation — v8, v2.2, v3.1 in same session,
  solver corrections applied. Ship-it: ≥33/40 solver-corrected, no
  regression vs v2.2
- If v3.1 still doesn't improve: proceed to reference set expansion
  (separate plan)

---

## Decision Points (owner approval required)

| # | When | Decision |
|---|------|----------|
| 1 | Before Phase 0 starts | Approve this plan |
| 2 | After Phase 0 delivers | Approve RAISE verdicts |
| 3 | After Phase 1 delivers | Approve action audit findings, decide which situations to remove/fix |
| 4 | After Phase 2 delivers | Approve corrected dataset |
| 5 | After Phase 3 Step 1 | Approve training plan |
| 6 | After Phase 3 Step 5 | Approve or reject model |

---

## What this plan does NOT cover

- Reference set expansion (only if v3.1 fails Gate 2.4)
- KB v1.3 update (depends on Phase 0 findings — which rules need rewriting)
- Labelling prompt update (depends on Phase 0 — what instructions to add)
- Process Guide Section 5.4 update (solver-as-verification-only rule)

These are downstream of the data integrity work. Plan them after v3.1
gate results are known.
