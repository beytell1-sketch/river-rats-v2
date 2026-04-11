# Plan: v3.1 Complete Rebuild

**Date:** 8 April 2026
**Version:** Complete (all data sources audited, no hidden errors)
**Status:** AWAITING OWNER APPROVAL

---

## Governing Principles

1. Every training label must be reachable from the feature vector.
2. RAISE = is_monster only in training. Bluff-raises via post-hoc rule.
3. Every data source must be audited for action sequence correctness
   BEFORE any training or gating uses it.
4. No solver corrections applied until the underlying hand is verified.

---

## The full data integrity picture

| Data Source | Count | Audited? | Finding |
|-------------|-------|----------|---------|
| Self-play (base) | 200 | YES | CLEAN |
| Factory batch 1 | ~144 | YES | 52% CRITICAL |
| Factory batch 2 | 260 | YES | 52% CRITICAL |
| 40 reference hands | 40 | **NO** | MW-30, MW-47 confirmed broken |
| 24 calibration exam hands | 24 | **NO** | Subset of reference — same risk |
| BATCH2_8_HAND_DESIGNS.md | 40 | **NO** | Source file for reference + exam |

**The reference set is the measuring stick. If the measuring stick is
broken, every score we've ever reported is suspect.**

---

## Phase 1 — COMPLETED (factory audit)

24 CRITICAL, 10 MODERATE, 12 CLEAN across 46 factory boards.
Self-play clean. Reference evaluator flagged but not audited.

## Phase 0 — COMPLETED

RAISE = is_monster only. All 7 non-monster RAISEs NOT DEFENSIBLE.

---

## Phase 2 — Reference Set Audit (NEW — MUST BE FIRST)

**Goal:** Verify all 40 reference hands have correct action sequences,
correct hand-authored tuples, and correct expert labels.

**Why first:** We cannot set a gate threshold until we trust the
reference set. Every historical model score (v8, v2.2, v3) may change.

### 2A: Audit BATCH2_8_HAND_DESIGNS.md

For each of the 40 hands (MW-11 through MW-50):
1. Reconstruct the full action sequence chronologically
   (who acts first on each street, in what order)
2. Verify the hand-authored tuple in reference_evaluator.py
   matches the actual action sequence:
   - villain_aggression_count: correct?
   - villain_checked_back: correct?
   - villain_call_count: correct?
   - num_callers_to_bet: correct?
   - facing_raise: correct?
3. Verify the expert label is defensible given the CORRECT
   action sequence (not the potentially broken one)
4. Flag any hand where the tuple is wrong or the sequence is
   ambiguous

### 2B: Audit calibration exam hands

The 24 calibration hands are a subset of the 40. Verify the
calibration_exam.py construction matches the corrected reference.

### Team

| Agent | Task | Scope |
|-------|------|-------|
| Auditor A | MW-11 through MW-25 (15 hands) | Full sequence reconstruction |
| Auditor B | MW-26 through MW-40 (15 hands) | Full sequence reconstruction |
| Auditor C | MW-41 through MW-50 (10 hands) | Full sequence reconstruction |
| Architect | Cross-check all tuples in reference_evaluator.py _ACTION_HISTORY against auditor findings | Code review |
| Reviewer | Independent review of all findings | All |

### Deliverable

For each of the 40 hands:
```
MW-XX:
  Hero: [position] holds [cards]
  Board: [cards]
  Full sequence: [chronological actions, every player, every street]
  Tuple in code: (agg, checked_back, call_count, callers, facing_raise)
  Correct tuple: (agg, checked_back, call_count, callers, facing_raise)
  Match: YES / NO — if NO, what's wrong
  Expert label: [action] — still correct with corrected sequence? YES / NO
```

### Gate

Owner reviews all 40 hands. Any incorrect tuple is fixed before
any gate scoring uses these hands.

---

## Phase 3 — Feature Pipeline Upgrade

Same as previous plan Phase 2. Add 4 features + fix flush_block_pct
+ add action sequence validator.

| # | Feature | Type |
|---|---------|------|
| 49 | hero_range_percentile | float 0-1 |
| 50 | has_showdown_value | binary |
| 51 | villain_fold_equity_estimate | float 0-1 |
| 52 | flush_draw_rank | int 0-14 |
| fix | flush_block_pct bug | compute value for hero draws |
| new | action sequence validator | prevent recurrence |

### Team

Architect → Programmer A (features) → Programmer B (fix) →
Programmer C (validator) → Reviewer.

### Gate

Owner reviews. 10 test situations verify correct values.

---

## Phase 4 — Factory Rebuild

Fix action histories for all 46 boards. Regenerate with 52 features.
All boards must pass action sequence validator.

### Team

Programmer A (batch 1, 16 boards) → Programmer B (batch 2, 30 boards)
→ Auditors (4, ~12 boards each) → Reviewer.

### Gate

All 46 boards CLEAN. Zero CRITICAL or MODERATE.

---

## Phase 5 — Relabel

Fresh labels on clean data. RAISE = is_monster only.

### Labelling rules

- RAISE: is_monster == 1. Nothing else.
- BET/CHECK: 5-factor framework, feature-visible reasoning only.
- CALL/FOLD: equity vs pot odds + action history + position.
- No solver logic. No blocker reasoning beyond what features capture.

### Process

1. Update labelling prompt with simplified rules
2. Calibration exam (using corrected exam hands from Phase 2)
3. Label all ~400 factory situations (≤10 per agent)
4. Review all labels (≤15 per reviewer)

### Gate

Owner reviews: distribution healthy, RAISE = is_monster count,
no contamination.

---

## Phase 6 — Combine + Train + Gate

### 6A: Combine

200 self-play rows + relabelled factory rows. 52 features + label.

### 6B: Leakage check (Gate 2.2)

Against the CORRECTED reference set from Phase 2.

### 6C: Train v3.1

From-scratch, 52 features, cap 3.0. Also Model B (48 features).

### 6D: Gates

- Gate 2.3: feature importance
- Gate 2.4: reference evaluation using CORRECTED reference set
  - v8, v2.2, v3.1 in same session
  - All historical scores recalculated against corrected reference
  - Ship-it: no regression vs v2.2 on corrected reference
  - Only apply MW-46 CALL correction (owner confirmed)
  - MW-30 and MW-47 corrections SUSPENDED until owner re-reviews
    with corrected action sequences

### Team

ML-architect → owner → architect → programmer → reviewer → owner.

---

## Phase 7 — Post-Hoc Bluff Rule

After training, before shipping.

```
If model predicts CALL
AND hero_range_percentile < 0.10
AND has_showdown_value == 0
AND villain_fold_equity_estimate > 0.45
→ Override to RAISE (logged)
```

Run Gate 2.4 with AND without rule. Owner decides.

---

## Decision Points

| # | When | Decision |
|---|------|----------|
| 1 | Now | Approve this plan |
| 2 | After Phase 2 | Approve corrected reference set |
| 3 | After Phase 3 | Approve feature implementations |
| 4 | After Phase 4 | Approve corrected factory |
| 5 | After Phase 5 | Approve labelled dataset |
| 6 | After Phase 6D | Approve or reject v3.1 |
| 7 | After Phase 7 | Approve or reject bluff rule |

---

## Estimated effort

| Phase | Hours |
|-------|-------|
| 2: Reference audit | 3-5 |
| 3: Feature pipeline | 4-6 |
| 4: Factory rebuild | 4-6 |
| 5: Relabel | 6-8 |
| 6: Train + gate | 3-4 |
| 7: Bluff rule | 1-2 |
| **Total** | **~21-31** |

---

## What this plan guarantees

1. Every data source audited for action sequence correctness
2. Reference set verified hand-by-hand before gating
3. All factory boards pass automated validator
4. Labels use only feature-visible reasoning
5. Historical model scores recalculated on corrected reference
6. No solver corrections without owner verification on corrected hands

## What this does NOT cover

- KB v1.3 (after v3.1 ships)
- 6-class split VALUE_RAISE/BLUFF_RAISE (v4.0)
- Reference set expansion (if v3.1 fails gate)
- Teaching system (gated on 80%+)
