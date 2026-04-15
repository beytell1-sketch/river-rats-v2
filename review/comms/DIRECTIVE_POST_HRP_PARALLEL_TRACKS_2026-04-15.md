---
date: 2026-04-15
from: Owner (Rupert) + main terminal
to: Builder team
re: 6 parallel tracks while Gate 7 awaits solver — informed by HRP investigation
status: DIRECTIVE — start immediately, all tracks parallel
prerequisite: HRP_INVESTIGATION_2026-04-15.md (test harness bug confirmed)
blocks on: owner solver time for 10 MW misses (Gate 7 decision)
---

# 6 Parallel Tracks Post-HRP Investigation

## Context

The HRP investigation showed:
- `hero_range_percentile = 0.00` was a test harness bug, not a
  feature extraction defect on real data
- v2.2 training data is intact
- 80% MW accuracy is real model behaviour
- The bias signature is corrected: model under-bets when hero
  is at TOP of range with strong equity (HRP avg 0.64 vs 0.44
  on misses)

Gate 7 still pending solver. These 6 tracks productively use
the wait time and are all Gate 7-independent.

---

## Track 1: Test harness hardening (HIGH VALUE, SMALL)

### Who
**Programmer** alone

### What
Add a guard to the evaluation harness:
- `extract_all_features()` runs at evaluation time on every test
  hand, regardless of whether `feat_dict` is present in the
  source JSONL
- Fail fast if any of the 54 FEATURE_COLUMNS can't be computed
- Never silently default missing keys to 0
- Test-first: write a test that confirms an MW-style incomplete
  `feat_dict` triggers a hard error before evaluation begins

### Deliverables
1. Updated evaluation harness in
   `river-rats-core/evaluate_oracle.py` (or wherever current
   eval lives)
2. Regression test in `tests/`
3. Re-run evaluation on FB-40 and MW-50 with the hardened
   harness to confirm numbers stand or change

### Why now
The HRP investigation only caught the silent-default bug
because we pushed on it. This guard protects every future
evaluation including v2.3 diagnostic test set, FB-40 reruns,
teaching team scoring.

### Constraints
- 1 agent call (programmer)
- No scope decisions
- Test-first per builder protocol

---

## Track 2: Re-evaluate FB-40 with hardened harness

### Who
**Programmer** (uses Track 1 deliverable)

### What
1. Run Track 1's hardened harness on FB-40
2. Verify FB-40 accuracy matches the previously-reported 72.5%
3. If different, document the difference and impact on Gate 7
   thinking
4. Same check on MW-50 (we know 80%, but confirm with hardened
   harness) — should produce same number with same hand swap
   (d2920 in, d4534 out)

### Deliverables
- Eval report committed to
  `review/comms/EVAL_RERUN_HARDENED_2026-04-15.md`
- Per-hand prediction comparison: old vs new harness output
- Flag any hands that change prediction

### Why now
Trust but verify. The MW finding suggests systemic harness
fragility. Confirm FB-40 (the only Gate 7 PASS) is real and
not similarly harness-corrupted.

### Constraints
- 1 agent call
- Depends on Track 1 completing first
- No model changes — pure evaluation

---

## Track 3: Training data completeness audit

### Who
**Programmer** (audit) + **ML Architect** (interprets results)

### What
For each of the 54 features in `v2_2_training.csv`:
- % of 385 rows with non-zero value
- Distribution: mean, median, std, min, max
- Number of zero values
- For zero values: are they structural (boolean false,
  contextually zero like `facing_bet=0`) or anomalies?

For features where >5% of rows have zero values that aren't
explained by structure, investigate root cause. Compare against
HRP's distribution (96% non-zero) as a baseline for "healthy"
coverage.

### Deliverables
- `review/comms/TRAINING_DATA_AUDIT_2026-04-15.md` with per-feature
  audit table
- Flag any features that look incomplete or anomalous
- Recommendation: does v2.3 need a re-extraction phase, or is
  the current data clean enough to add the supplement on top?

### Why now
If MW test set had silent-zeros bug, training pipeline might
too. Confirms the v2.2 model trained on clean inputs. If it
finds another silent-zeros feature, v2.3 scope changes — needs
a feature audit phase, not just a 206-hand supplement.

### Constraints
- 2 agent calls
- No data changes — pure audit
- ML Architect interprets, not Programmer

---

## Track 4: Bias signature deep-dive on corrected MW misses

### Who
**GTO Expert** (poker analysis) + **Programmer** (data extraction)

### What
The corrected bias signature (from HRP investigation):
| Feature | Miss avg | Non-miss avg |
|---|---|---|
| hero_range_percentile | 0.641 | 0.443 |
| equity_vs_range | 0.656 | 0.431 |
| villain_air_pct | 0.320 | 0.280 |
| villain_top_pair_plus_pct | 0.371 | 0.425 |
| spr | 1.250 | 1.250 |
| better_hand_pct | 0.292 | 0.549 |
| worse_hand_pct | 0.697 | 0.428 |

This says: model under-bets when hero is HIGH in their range
with strong equity. That's not generic passivity.

GTO Expert analyses the 10 MW misses with full feature context:
1. Are these all top-of-range hands the model wants to slowplay?
   (trap bias)
2. Are they spots where bucket-first prefers CHECK because
   villain has strong range vs hero's strong hand? (defensive
   bias when both sides are strong)
3. Are they hands where the labelling agents would have voted
   CHECK too? (in which case the issue is upstream — labels are
   too passive on these patterns) (label/model alignment vs
   label/solver disagreement)
4. Pattern across the 10: dominant board texture? Position?
   Sandwich shape?

### Deliverables
- `review/comms/MW_MISS_BIAS_ANALYSIS_2026-04-15.md`
- Per-hand breakdown of all 10 misses with poker reasoning
- Conclusion on bias type (trap / defensive / label / mixed)
- Recommendation on fix direction: prompt change, training
  change, or both

### Why now
The original Track A scope assumed generic CHECK bias. The
corrected signature suggests something more specific. The GTO
investigation lets us redesign Track A Section 2 correctly
before v2.3 implementation begins.

### Constraints
- 2 agent calls
- Programmer extracts the per-hand data (action history,
  reasoning, all features), GTO Expert reasons over it
- No code changes — analysis only

---

## Track 5: Implement Track B (BP generator fix)

### Who
**Programmer** (test-first per blueprint)

### What
Implement the BP generator fix per the approved blueprint at
`review/comms/BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md`:

- Fix 1: Add `num_opponents` validator to `SituationSpec` and
  length guard in `build_situation()`
- Fix 2: Add 4 missing metadata fields to `feat_dict` in
  `generate_factory_batch{2,3,4}.py`
- Fix 3: No change needed in `generate_factory_batch5.py`
- Fix 4: Replace ad-hoc inline formatter with canonical path
  via `labelling_agent.prepare_batches()`

### Deliverables
1. Test in `tests/test_situation_factory.py` that fails on the
   old behaviour (validator triggers when villain count
   mismatches num_opponents)
2. Fix implementations as specified
3. Full test suite passes
4. Commit references v2.3 backlog item 5 (mandatory blocker)

### Why now
Approved blueprint, no Gate 7 dependency. Prevents the bug from
recurring in v2.3 generation.

### Constraints
- DO NOT re-run BP labelling
- 1-2 agent calls (programmer + optional tester)
- Standalone commit

---

## Track 6: Track A scope corrections

### Who
**Architecture Expert**

### What
Update `PLAN_V23_SCOPE_2026-04-15.md` with the three required
amendments from REVIEW_PARALLEL_TRACKS_2026-04-15.md:

1. **Reconcile BET delta inconsistency**
   - Allocation table says +166 BET
   - Narrative says +155 BET + 31 protection BET
   - Pick one accounting and make consistent
   - If protection BETs are subset of total BET, narrative
     should say "+166 BET (of which ~31 are protection)"

2. **Update Section 2 CHECK-bias signature**
   - Remove `hero_range_percentile = 0.00` claim (it was a
     test harness artifact)
   - Replace with corrected signature from HRP investigation
     (HRP HIGH at top of range, equity HIGH, BET-true predicted
     CHECK)
   - Coordinate with Track 4 output — final signature should
     reflect GTO Expert's analysis

3. **Add explicit calibration gate**
   - Same gate as v2.2: 23/28 minimum (scaled from 20/24) +
     all reversal hands correct
   - State explicitly: must pass before any v2.3 production
     labelling

### Deliverables
- Updated `PLAN_V23_SCOPE_2026-04-15.md` in place (or v2 file
  if architect prefers, with supersession noted)

### Why now
Track A is the foundation for v2.3. Get it correct before any
v2.3 work proceeds. Best done after Track 4 completes (so the
Section 2 signature is accurate).

### Constraints
- 1 agent call (architect)
- Depends on Track 4 for accurate Section 2 update

---

## Track ordering

**Tier 1 (start immediately, no dependencies):**
- Track 1: Harness hardening
- Track 3: Training data audit
- Track 4: Bias signature deep-dive
- Track 5: Track B generator fix implementation

**Tier 2 (depends on Tier 1):**
- Track 2: FB-40 / MW re-eval (depends on Track 1)
- Track 6: Track A scope corrections (depends on Track 4 for
  signature update)

## Agent allocation summary

| Track | Agents | Type | Tier |
|---|---|---|---|
| 1: Harness hardening | 1 | Programmer | 1 |
| 2: Eval re-run | 1 | Programmer | 2 (after 1) |
| 3: Training audit | 2 | Programmer + ML Architect | 1 |
| 4: Bias deep-dive | 2 | GTO + Programmer | 1 |
| 5: Generator fix | 1-2 | Programmer + Tester | 1 |
| 6: Scope corrections | 1 | Architect | 2 (after 4) |
| **Total** | **8-9** | | All parallel within tiers |

## Owner review sequence

1. **Track 1** — harness hardening: spot-check the regression
   test
2. **Track 3** — training audit: review the per-feature audit
   table for any anomalies
3. **Track 4** — bias deep-dive: review GTO Expert's
   conclusions, this informs v2.3 strategy
4. **Track 2** — eval re-run: confirm Gate 7 numbers stand
5. **Track 6** — scope corrections: review updated Section 2
   and other amendments
6. **Track 5** — generator fix: spot-check regression test +
   commit message

## What this directive does NOT cover

- Gate 7 decision (ship/iterate) — pending solver on 10 MW misses
- v2.3 implementation — gated on owner approval of corrected
  Track A scope (Track 6)
- v2.3 hand generation — gated on Track 5 (generator fix) +
  Track 6 (scope correction) + owner approval
- Teaching team work — already unblocked via Track D handoff
- v3.0 action distributions — still in v2.3 backlog item 1, not
  this directive

---

**Builder: launch Tier 1 tracks immediately (1, 3, 4, 5).
Tier 2 tracks (2, 6) start when their dependencies complete.
Owner reviews incrementally.**
