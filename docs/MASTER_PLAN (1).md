# River Rats — Master Plan

**Purpose:** Single source of truth for project state, sequence, and
design decisions. Lives in the repo AND in Claude Web project files.
Both copies must match.

**Last updated:** 6 April 2026  
**Source:** Independent review trail + project lead design sessions

---

## 1. WHERE THE PROJECT IS

### 1.1 What's Built and Stable

- **v8 XGBoost oracle** — 88.1% HU accuracy (PokerBench ground truth).
  MW accuracy is 52.5% on 40-hand expert reference set (19/40 failures).
- **45-feature pipeline** — expanded from 38 on 6 April 2026. Adds 5
  range composition features, 2 current-street action features, and
  activates 4 previously dead features. v8 backward-compatible via
  auto-detect. 916 tests pass.
- **Multiway adjuster** — 7 rules, 20 constants, ceiling reached.
  Will be evaluated per-model after progressive chain trains.
- **Self-play infrastructure** — 7 modules, all reviewed and passing.
  Used for 5 rounds of variant testing and will generate training
  situations for the progressive model chain.
- **Reference evaluator** — evaluates oracle variants against 40
  expert-labelled hands. Infrastructure for gating model progression.
- **feature_keys.py** — single source of truth for feature dict keys.
- **SpotCatalog** — 77 entries, 19 spot types. Migrates to teaching later.
- **Range state classifier** — Key 1 PASSED (56/56 hands).
- **Coaching benchmark** — L2 CLEAR 64.5%, L5 contradiction 1.3%.
- **Human testing instrumentation** — per-hand JSONL logging.
- **Preflop system design** — approved with 3 blocking fixes.

### 1.2 The Accuracy Problem

52.5% accuracy on 40 expert-reviewed multiway hands. The failure
breaks down as:

```
53% of failures (10/19): Oracle won't bet
  Model outputs CHECK where BET is correct — even at 81% equity.
  The adjuster is a one-way tightening valve. It cannot promote
  CHECK→BET or CALL→RAISE. No parameter setting fixes this.

21% of failures (4/19): Range-narrowing blindness
  Model calls where it should fold (MW-30, 31, 46, 50).
  Multi-street aggression implies a crushing villain range.
  Three action-history features were dead in production — bridge
  fix activated them. Model learned nothing from them in training.

Remaining: over-raising and under-raising mix
```

Root cause: The HU model (PokerBench-trained) learned conservative
multiway play. The adjuster compensates but has a structural ceiling.
Self-play proved threshold tuning is the wrong lever. The model itself
must learn multiway play through progressive specialist training.

### 1.3 Self-Play Loop: Concluded

Five rounds (100–1000 deals, 3,600–12,000 games per round) tested
6 initial hypotheses and their hybrids against heuristic opponents.

**Key findings:**
- As sample size increased, modified variants' advantages shrank and
  reversed. R1-R3 results at 100 deals were noise, not signal.
- Heuristic opponents don't punish the errors the adjuster corrects.
- All 3 tested variants scored identically (21/40) on the reference
  set — the adjuster threshold parameters are not the lever.

**Validated independently of self-play:**
- Draw bypass 8→5 is correct (GTO reasoning, not opponent-dependent)
- OOP discount + cold-call tightening interact destructively

**Self-play infrastructure preserved for:** generating labelling
situations and Phase D human testing.

---

## 2. THE 40-HAND MULTIWAY REFERENCE SET

40 expert-designed hands (MW-11 through MW-50), 8 axes, 6-per-batch
numbering (canon). Serves as: validation gate for each model in the
progressive chain, and future teaching curriculum seed.

**Partition by opponent count:**

| Opponents | Hands | Sufficient? |
|-----------|-------|-------------|
| 1 (HU)   | 4     | v8 validated on PokerBench |
| 2 (3-way) | 24   | Yes |
| 3 (4-way) | 12   | Tight but usable |
| 4+ (5-way) | 0   | **Must add 5-10 before Step 3** |

Status: All action-history fields annotated per hand. GTO-reversal
hands (MW-30, 31, 46, 50) have override flags. MW-18 confound fixed.

---

## 3. THE MASTER SEQUENCE

```
OLD (wrong):   Calibration → Teaching → Testing → Self-play (maybe)
SUPERSEDED:    Calibration (done) → Self-play → Teaching → Testing
CURRENT:       Calibration (done) → Self-play (done) → Progressive
               Model Chain → Teaching → Testing
```

Self-play proved the adjuster isn't the answer. Progressive specialist
models are. You cannot teach what you cannot play correctly.

---

## 4. PHASE A: PROGRESSIVE MODEL CHAIN (NOW)

### 4.1 Goal

Replace the single HU model + adjuster with a chain of specialist
models, one per opponent count. Each model starts from the previous
and learns the next level of multiway complexity via XGBoost warm-start.

### 4.2 Architecture

```
v8 HU (38-feat, existing, FROZEN)
  → warm-start on 200 3-way hands → v9-3way (45-feat, saved)
  → warm-start on 200 4-way hands → v9-4way (45-feat, saved)
  → warm-start on 100 5-way hands → v9-5way (45-feat, saved)
```

Each model is saved permanently. Later models never overwrite earlier
ones. In production, `num_opponents` at the decision point selects
which model runs.

### 4.3 Why Progressive, Not All-At-Once

One model trained on 25k HU + 500 MW rows learns neither well.
"Multiway" spans 3-way to 6-way with fundamentally different decision
boundaries. 500 rows (2% of data) buried in 25k HU cannot teach both
3-way and 5-way patterns.

Progressive works because poker complexity scales incrementally.
3-way is a small step from HU. 4-way is a small step from 3-way.
Each model builds on the last.

### 4.4 The 45-Feature Pipeline

SHIPPED 6 April 2026. All models use the same 45-feature vector:

| # | Feature | Status |
|---|---------|--------|
| 1-33 | Original game state, hand, board, equity features | Live (v8) |
| 34 | `is_3bet_pot` | Activated (was dead) |
| 35-37 | `villain_aggression_count`, `checked_back`, `call_count` | Activated (bridge fix) |
| 38 | `num_opponents` | Live (v8) |
| 39-43 | `villain_top_pair_plus_pct`, `draw_pct`, `air_pct`, `range_capped`, `board_favour` | Promoted from metadata |
| 44-45 | `num_callers_to_bet`, `facing_raise` | New |

v8 auto-detects its 38-feature width and ignores columns 39-45.
v9 models use all 45.

### 4.5 Model Router

```python
MODELS = {
    1: GtoOracle("models/gto_model_v8_hu.json"),
    2: GtoOracle("models/gto_model_v9_3way.json"),
    3: GtoOracle("models/gto_model_v9_4way.json"),
}
DEFAULT = GtoOracle("models/gto_model_v9_5way.json")

def predict(feat_dict, num_opponents):
    oracle = MODELS.get(num_opponents, DEFAULT)
    features = GtoOracle.features_from_dict(feat_dict)
    return oracle.predict(features)
```

Before a specialist exists, the router falls back to the nearest
available model (initially v8 for everything).

### 4.6 Training Sequence (Gated)

Each step: train → evaluate on reference set → pass gate → proceed.

**Infrastructure (before any training):**

| Task | Status |
|------|--------|
| Feature expansion 38→45 | **DONE** |
| Model router | TODO |
| v9-baseline (fresh train on PokerBench with 45 features, pipeline validation) | TODO |

**Step 1: v9-3way**

| | |
|---|---|
| Base model | v9-baseline (25k PokerBench, 45 features) |
| New data | ~200 expert-labelled 3-way hands |
| Training | XGBoost warm-start (`xgb_model` parameter) |
| Output | `gto_model_v9_3way.json` (saved permanently) |
| Validation | Accuracy on 24 three-way reference hands |
| Gate | 3-way accuracy improves over v8; HU does not regress |

**Step 2: v9-4way**

| | |
|---|---|
| Base model | v9-3way |
| New data | ~200 expert-labelled 4-way hands |
| Output | `gto_model_v9_4way.json` (saved permanently) |
| Gate | 4-way accuracy improves over v9-3way on 4-way hands |

**Step 3: v9-5way**

| | |
|---|---|
| Base model | v9-4way |
| New data | ~100 expert-labelled 5-way hands |
| Output | `gto_model_v9_5way.json` (saved permanently) |
| Gate | 5-way accuracy meets threshold on new 5-10 reference hands |

### 4.7 Labelling Protocol

~500 total hands across three batches. Self-play runner generates
realistic game situations. GTO Expert agent labels each decision.

Per-decision requirements:
- All 45 features populated with real multiway values
- Opponent count at decision point (not hand start)
- Stratified by street, position, action type
- Biased toward identified failure modes

### 4.8 Adjuster Evaluation

After each model trains, test with and without adjuster:

- Specialist alone beats specialist+adjuster → strip adjuster
- Adjuster still helps → keep as safety net, examine which rules
- Expected: draw bypass and pot odds survive; bluff suppression and
  value tightening become redundant (model learned them)

### 4.9 Expected Outcome: v9-baseline Won't Improve MW Accuracy

The 5 promoted range features have different semantics in HU vs MW
context. When v9-baseline trains on 25k PokerBench rows (all HU),
it cannot learn MW-specific patterns. The accuracy improvement comes
from the specialist training (Steps 1-3), not the baseline retrain.
Do not treat a flat v9-baseline result as "the features don't help."

---

## 5. PHASE B: PREFLOP SYSTEM (parallel with Phase A)

Separate engine (range tables, not ML). Can run in parallel.

```
□ Resolve 3 blocking fixes:
  - Pot odds formula (standard vs non-standard)
  - Replace CO/BTN test case
  - Add UTG/HJ to CALL_VS_3BET
□ Phases 1-6: range data → engine → teaching → AI fix → integration
```

---

## 6. PHASE C: TEACHING SYSTEM (after Phase A passes accuracy gate)

**Gate — do NOT start until progressive model chain achieves:**

```
3-way accuracy:   Improved over v8 on 24 reference hands
4-way accuracy:   Improved over v9-3way on 12 reference hands
Overall MW:       >= 80% on expert-reviewed hands (combined)
```

Then build Single Truth 3-level teaching. The specialist models'
decisions are the ground truth — no circular adjuster labels.

---

## 7. PHASE D: HUMAN TESTING (after Phase C)

200-hand sessions. Disagreements feed back into evaluation.

---

## 8. THINGS NOT TO DO

```
- Do NOT build teaching before progressive chain passes gates
- Do NOT connect observer flags to oracle decisions (EVER)
- Do NOT retrain all-at-once (500 MW rows in 25k HU = signal drowns)
- Do NOT modify v8 model file (it's the HU anchor, permanently frozen)
- Do NOT skip gates between progressive training steps
- Do NOT use MW adjuster labels for anything (circular)
- Do NOT trust reported 96% MW accuracy (model matching own output)
- Do NOT run more heuristic calibration rounds (ceiling reached,
  5 self-play rounds confirmed threshold tuning is wrong lever)
- Do NOT expect v9-baseline to improve MW accuracy (HU-only training
  data, MW signal comes from specialist batches)
```

---

## 9. DESIGN DECISIONS (SETTLED)

```
DECISION                              ANSWER           DATE
Sequence: accuracy before teaching    YES              5 Apr 2026
Self-play: threshold tuning is wrong  YES              6 Apr 2026
  lever (5 rounds proved it)
Feature expansion 38→45               SHIPPED          6 Apr 2026
Progressive model chain, not single   YES              6 Apr 2026
  retrain (specialist per opponent
  count, warm-start chain)
Training approach: XGBoost warm-start YES              6 Apr 2026
  (xgb_model param, add trees to
  previous model)
Model router by num_opponents         YES              6 Apr 2026
Each model saved permanently          YES              6 Apr 2026
~500 hands total (200+200+100)        YES              6 Apr 2026
GTO Expert agent labels (solver       YES              6 Apr 2026
  validation on hardest 20% of 5-way)
Adjuster evaluated per-model after    YES              6 Apr 2026
  specialist training (keep/trim/strip)
Duplicate deals for self-play         YES              5 Apr 2026
Decision-point comparison             YES              5 Apr 2026
Observer flags: observation only      YES              5 Apr 2026
GTO Expert uses predefined menu       YES              5 Apr 2026
Scoring metric: mbb/hand              YES              5 Apr 2026
Staged stack depth: 100bb in Gen 2    YES              6 Apr 2026
```

---

## 10. QUALITY METRICS

### Current Baselines

```
Oracle HU:            88.1% (real — PokerBench)
Oracle MW:            52.5% (real — 40-hand reference set, 6 Apr 2026)
  HU at decision:     25.0% (1/4 — all are GTO-reversal hands that
                              started multiway, became HU mid-hand)
  3-way (num_opp=2):  50.0% (12/24 correct)
  4-way (num_opp=3):  66.7% (8/12 correct)
Calibration Tier 1:   97.6%
Calibration Tier 3:   83.9%
L2 CLEAR:             64.5%
MISLEADING:           0.9%
```

### Progressive Chain Gates (must pass before teaching)

```
v9-3way:    3-way accuracy >= 54.2% (14/24) on reference hands
v9-4way:    4-way accuracy > 66.7% (8/12) on reference hands
v9-5way:    5-way accuracy meets threshold on 5-10 new hands
Overall MW: >= 80% on combined reference set
```

---

## 11. IMMEDIATE NEXT STEPS

```
NOW:
  ■ Feature expansion 38→45 (DONE)
  □ Build model router
  □ Retrain v9-baseline on PokerBench (pipeline validation)

AFTER infrastructure ships:
  □ Spec 3-way labelling protocol
  □ Generate ~200 3-way situations from self-play runner
  □ GTO Expert labels them
  □ Train v9-3way, evaluate, gate

AFTER 3-way gate passes:
  □ Spec 4-way labelling protocol
  □ Generate ~200 4-way situations
  □ Train v9-4way, evaluate, gate

AFTER 4-way gate passes:
  □ Add 5-10 five-way reference hands
  □ Spec 5-way labelling protocol
  □ Generate ~100 5-way situations
  □ Train v9-5way, evaluate, gate

AFTER all gates pass:
  □ Evaluate adjuster: keep, trim, or remove per model
  □ Teaching system build (Phase C)
  □ Human testing (Phase D)
```

---

## 12. FILE REFERENCE

```
docs/PROGRESSIVE_MODEL_CHAIN.md       — detailed design plan
docs/SPEC_FEATURE_EXPANSION_38_TO_45.md — feature expansion spec
results/SELF_PLAY_FINDINGS.md          — 5-round self-play conclusions
design/multiway_reference_set/         — 40-hand expert reference set
```
