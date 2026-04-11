# Plan: v3.1 Clean Rebuild

**Date:** 8 April 2026
**Version:** Final
**Status:** AWAITING OWNER APPROVAL

---

## Governing Principles

1. Every training label must be reachable by reasoning the model can
   learn from its features. Solver data verifies and researches. It
   never labels.
2. RAISE = is_monster only in training labels. Bluff-raises are handled
   by a post-hoc inference rule, not by training labels.
3. One variable at a time where possible.

---

## Summary of root causes

1. Solver-derived KB rules led to RAISE labels the model can't learn
2. 52% of factory boards have broken action sequences
3. Model lacks bluff signal (no hero_range_percentile feature)

---

## Phase 0 — COMPLETED

All 7 non-monster RAISE labels: NOT DEFENSIBLE from features.
RAISE = is_monster only for training.

## Phase 1 — COMPLETED (audit)

24 CRITICAL, 10 MODERATE, 12 CLEAN across 46 boards.
Self-play (200 rows) clean. Reference evaluator has separate concerns.

---

## Phase 2 — Feature Pipeline Upgrade

**Goal:** 4 new features + 1 bug fix + action sequence validator.

### New features

| # | Feature | Type | Effort |
|---|---------|------|--------|
| 49 | `hero_range_percentile` | float 0-1 | Medium (wire existing function) |
| 50 | `has_showdown_value` | binary | Trivial (1 line) |
| 51 | `villain_fold_equity_estimate` | float 0-1 | Trivial (3 lines) |
| 52 | `flush_draw_rank` | int 0-14 | Low (8-10 lines) |

### Bug fix

`flush_block_pct`: fix to return useful value when hero has 2+
flush-suit cards (currently returns 0.0 — exactly wrong).

### Action sequence validator

Add to situation_factory.py: verify positional ordering before
building any situation. Prevents the Phase 1 bug class.

### Team

| Agent | Task |
|-------|------|
| Architect | Blueprint for all changes |
| Programmer A | Features 49-52 |
| Programmer B | flush_block_pct fix |
| Programmer C | Action sequence validator |
| Reviewer | Verify all |

### Gate

Owner reviews. 10 test situations verify features produce correct
values and validator catches known-bad sequences.

---

## Phase 3 — Factory Rebuild

**Goal:** Correct action sequences for all 46 boards. Regenerate.

### Work

- Fix all action_history lists (add missing OOP checks, intermediate
  callers, correct positional ordering)
- Run through action sequence validator — all 46 must pass
- Regenerate JSONL files with 52-feature vectors

### Team

| Agent | Task | Scope |
|-------|------|-------|
| Programmer A | Fix batch 1 (16 boards) | generate_factory_situations.py |
| Programmer B | Fix batch 2 (30 boards) | generate_factory_batch2.py |
| Auditors (4) | Re-audit all boards | ~12 boards each |
| Reviewer | Review all fixes | All |

### Validation

Run 10 deals through corrected factory. Verify num_callers_to_bet
and villain_aggression_count match actual sequences.

### Gate

Owner reviews. All 46 boards CLEAN. Zero CRITICAL or MODERATE.

---

## Phase 4 — Relabel

**Goal:** Fresh labels on clean data with simple rules.

### Labelling rules

**RAISE:** is_monster == 1. Nothing else. No blocker logic, no
semi-bluff carve-outs, no solver-derived rules.

**BET/CHECK:** 5-factor framework from KB, using feature-visible
reasoning only.

**CALL/FOLD:** Equity vs pot odds + action history + position.

### Process

1. Update labelling prompt with simplified RAISE rule
2. Calibration exam (20/24 gate)
3. Label all ~400 factory situations (≤10 per agent)
4. Independent review (≤15 per reviewer)

### Team

Same structure as the original labelling round. ~40 labelling
agents + ~27 reviewers.

### Gate

Owner reviews: label distribution healthy, RAISE count matches
is_monster count in the data, no solver contamination.

---

## Phase 5 — Combine + Train + Gate

### 5A: Combine

200 self-play rows (with new features appended) + relabelled factory
rows. Export CSV with 52 features + label.

### 5B: Leakage check (Gate 2.2)

### 5C: Train v3.1

From-scratch, 52 features, cap 3.0. Also train:
- Model B: 48 features (do new features help?)

### 5D: Gates

- Gate 2.3: feature importance. hero_range_percentile should show
  >1%. flush_block_pct should improve after bug fix.
- Gate 2.4: reference evaluation. v8, v2.2, v3.1. Ship-it: ≥32/40
  raw, no regression vs v2.2.

### Team

ML-architect → owner → architect → programmer → reviewer → owner.

---

## Phase 5.5 — Post-Hoc Bluff Rule (after training, before shipping)

### The rule

At inference time only (not in training labels):
```
If model predicts CALL
AND hero_range_percentile < 0.10
AND has_showdown_value == 0
AND villain_fold_equity_estimate > 0.45
→ Override to RAISE (logged as bluff-raise)
```

### Implementation

- Add to oracle_router.py or gto_model.py as a named function
- Log every override with full feature context
- Configurable on/off flag

### Testing

- Run Gate 2.4 WITH the rule active
- Compare: v3.1 without rule vs v3.1 with rule
- If the rule regresses the reference score, disable it
- If it improves or is neutral, ship it

### Gate

Owner reviews both scores (with/without rule) and decides.

---

## Phase 6 — Reference Evaluator Audit (parallel with Phase 3-5)

Verify hand-authored tuples in reference_evaluator.py. Architect B
flagged MW-31, MW-42, MW-46. If miscounts found, correct and re-run
Gate 2.4 for all models.

---

## Decision Points

| # | When | Decision |
|---|------|----------|
| 1 | Now | Approve this plan |
| 2 | After Phase 2 | Approve feature implementations |
| 3 | After Phase 3 | Approve corrected factory |
| 4 | After Phase 4 | Approve labelled dataset |
| 5 | After Phase 5D | Approve or reject v3.1 |
| 6 | After Phase 5.5 | Approve or reject bluff rule |

---

## Estimated effort

| Phase | Hours |
|-------|-------|
| 2: Features + fix + validator | 4-6 |
| 3: Factory rebuild | 4-6 |
| 4: Relabel | 6-8 |
| 5: Train + gate | 3-4 |
| 5.5: Bluff rule | 1-2 |
| 6: Ref eval audit | 2-3 |
| **Total** | **~20-29** |

---

## What this does NOT cover

- KB v1.3 (after v3.1 ships)
- 6-class VALUE_RAISE / BLUFF_RAISE split (v4.0)
- nut_draw_bluff_eligible feature (v3.2, after #51 proves useful)
- Reference set expansion (only if v3.1 fails gate)
- Teaching system (gated on 80%+)
