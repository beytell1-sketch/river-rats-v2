# SPEC: 3-Way Labelling Protocol

**Date:** 6 April 2026
**Status:** Draft — awaiting approval
**Depends on:** Feature expansion (done), model router (done), v9-baseline (done)
**Blocks:** v9-3way training

---

## Objective

Generate ~200 expert-labelled 3-way postflop decisions from 6-seated
games. Each labelled row has a complete 45-feature vector + correct
GTO action. This is the training data for warm-starting v9-baseline
into v9-3way.

---

## Source: 6-Seated, Filter to 3-Way Postflop

**Why not 3-seated:** GTO Expert analysis found 15-25% action
divergence between 3-seated and 6-seated 3-way pots. 3-seated
produces MEDIUM confidence labels (wide ranges = mixed strategies).
6-seated produces HIGH confidence labels (tight ranges = polarized
decisions). Training on 3-seated data would teach the wrong action
on ~30-50 of 200 hands and require building 3-player infrastructure.

**Generation plan:** Run the self-play runner in 6-seated mode with
baseline params, ~150 deals. Each deal produces 6 hero-position
games. With typical preflop folding, ~25-30% of postflop decisions
will have exactly 2 opponents (3-way). Expected yield: ~200-300
three-way postflop decisions from 150 deals.

**Filtering:** `HeroDecision.num_opponents == 2` and
`HeroDecision.is_preflop == False`. Infrastructure already exists,
no code changes needed for filtering.

---

## Infrastructure Change: Capture Feature Dicts

### The gap

The self-play callback (`_make_oracle_callback` in self_play.py)
computes the full 45-feature dict at line 150 but only saves
`raw_equity` to `HeroDecision`. The rest is discarded. For training,
we need the complete feature vector.

### The fix

Add an optional `feat_dict` field to `HeroDecision`:

```python
@dataclass
class HeroDecision:
    # ... existing fields ...
    feat_dict: Optional[Dict] = None  # full 45-feature dict, for training data export
```

In the callback, save it:

```python
decision_log.append(HeroDecision(
    ...,
    feat_dict=dict(feat_dict),  # copy to avoid mutation
))
```

This is opt-in — only populated when the callback captures it.
Existing code that doesn't use feat_dict is unaffected (defaults
to None). Memory cost: ~45 floats per decision, negligible.

### Export format

New function `export_training_csv(decisions, output_path)` that:
1. Filters to postflop decisions with feat_dict != None
2. Writes 45 FEATURE_COLUMNS + 'action' column
3. Action comes from the expert label (not the oracle's prediction)

---

## Labelling Pipeline

### Step 1: Generate situations

```
python3 generate_3way_situations.py --deals 150 --seed 100
```

New script that:
1. Runs SelfPlayRunner with baseline variant, 150 deals
2. Collects all GameResult objects
3. Filters to postflop HeroDecision where num_opponents == 2
4. Extracts feat_dict + hand context for each
5. Writes to `training-data/3way_situations.jsonl`

Each JSONL row contains:
```json
{
  "situation_id": "d042_BTN_flop",
  "hero_cards": "KsJh",
  "board": "Kd8c3s",
  "street": "flop",
  "hero_position": "BTN",
  "villain_positions": ["CO", "BB"],
  "pot": 100,
  "to_call": 33,
  "facing_bet": true,
  "num_opponents": 2,
  "action_history": "CO opens, BTN calls, BB calls. Flop: CO bets 33.",
  "feat_dict": { ... all 45 features ... },
  "oracle_action": "CALL",
  "adjusted_action": "CALL"
}
```

The `oracle_action` and `adjusted_action` are recorded for analysis
but NOT used as labels. The GTO Expert provides the correct label.

### Step 2: GTO Expert labels each situation

The GTO Expert agent receives each situation with full context and
assigns:

- **action**: FOLD / CHECK / CALL / BET / RAISE
- **confidence**: HIGH / MEDIUM / LOW
- **reasoning**: 1-2 sentences explaining the poker logic

Labelling rules:
- Use the range composition features to reason about villain ranges
  (they reflect 6-seated preflop filtering)
- When the decision is genuinely mixed (EV within 5% between two
  actions), label the higher-frequency GTO action and tag confidence
  as LOW
- When the oracle's action matches the expert's label, still record
  it — correct predictions are valid training data
- Do NOT look at outcome (chips won/lost) — label based on decision
  quality at the point of action

### Step 3: Quality control

**Automatic checks:**
- Every situation has an action label
- No action label is empty or outside {FOLD, CHECK, CALL, BET, RAISE}
- feat_dict has exactly 45 feature columns with numeric values
- Action distribution is not degenerate (no single action > 60%)

**Confidence distribution target:**
- HIGH: >= 60% of labels
- MEDIUM: 20-35%
- LOW: <= 15%

If LOW exceeds 15%, the situations are too ambiguous — regenerate
with a different seed or increase deal count.

**LOW confidence exclusion:** LOW-confidence labels are excluded from
the training CSV. They remain in the labelled JSONL for analysis but
do not enter the model. If excluding LOW drops volume below 180
usable decisions, relabel the ambiguous spots or generate additional
situations rather than training on guesses.

**Spot-check protocol:**
- Randomly sample 20 labelled hands (10%)
- Independent review: does the label match poker reasoning?
- If > 2 of 20 are wrong, review the full batch

### Step 4: Export training CSV

```
python3 export_3way_training.py
```

Reads the labelled JSONL, writes `training-data/train_3way_45.csv`
with 45 feature columns + action column. Only HIGH and MEDIUM
confidence labels are included. This CSV is the input to the
v9-3way warm-start training.

**Warm-start mechanics:** The base model's existing trees (trained
on 62k PokerBench) are frozen in place. Warm-start only appends new
trees that learn corrections from the 3-way rows. HU knowledge is
preserved, not retrained. Use `early_stopping_rounds=10` evaluated
on the 24 three-way reference hands to prevent overfitting the
small training set.

---

## Stratification

The 200 labelled decisions should cover the failure modes identified
in the reference evaluation. Target distribution:

**By street:**
- Flop: ~50% (100 decisions) — most common decision point
- Turn: ~35% (70 decisions) — multi-street action history
- River: ~15% (30 decisions) — range narrowing from full action line

**By position:**
- IP (hero acts last): ~50%
- OOP (hero acts first): ~50%

**By action type (expert label):**
- CHECK: ~25%
- CALL: ~25%
- BET: ~20% — oversample if natural rate is low (this is the
  model's biggest failure mode: 10/19 failures were BET→CHECK)
- FOLD: ~15%
- RAISE: ~15%

**By facing bet:**
- Facing bet (yes): ~50%
- Not facing bet (checked to hero): ~50%

These are targets, not hard constraints. Natural game play will
produce its own distribution. If BET situations are underrepresented
(< 15%), generate additional deals with a seed that produces more
betting contexts, or manually construct situations that require
betting decisions.

---

## What This Does NOT Do

- No 3-seated data. All situations are 6-seated with natural
  preflop filtering to 3-way.
- No solver validation on this batch. 6-seated 3-way hands have
  HIGH labelling confidence per GTO Expert. Solver validation is
  reserved for the 5-way batch where confidence is lower.
- No changes to the reference set. The 24 existing 3-way reference
  hands remain the validation gate — they are NOT included in the
  training data.
- No adjuster changes. The adjuster runs during generation (to
  record what it would do) but expert labels override it entirely.

---

## Validation Gate

After v9-3way trains on this data:

1. Evaluate on the 24 three-way reference hands
2. Gate: accuracy >= 54.2% (14/24 minimum, must beat v8's 13/24)
3. Secondary: no HU regression — v9-3way on HU reference hands
   should score >= 1/4 (v8 baseline)
4. Report per-axis accuracy breakdown for analysis

If gate fails: examine which hands flipped wrong, check for
labelling errors on those specific failure modes, consider
regenerating with more situations targeting the failure spots.

---

## Files to Create

| File | Purpose |
|------|---------|
| `generate_3way_situations.py` | Runs self-play, filters, exports JSONL |
| `label_3way_situations.py` | GTO Expert agent labels each situation |
| `export_3way_training.py` | Converts labelled JSONL → training CSV |
| `training-data/3way_situations.jsonl` | Raw situations with context |
| `training-data/3way_labelled.jsonl` | Expert-labelled situations |
| `training-data/train_3way_45.csv` | Final training CSV for v9-3way |

---

## Infrastructure Changes Summary

| File | Change |
|------|--------|
| `self_play.py` | Add `feat_dict: Optional[Dict]` to HeroDecision, capture in callback |
| `self_play.py` | Add hero cards + board to HeroDecision (or extract from hand_record) |

These are small additions to existing dataclasses. No structural
changes to the self-play runner.

---

## Estimated Effort

| Step | Effort |
|------|--------|
| Infrastructure (feat_dict capture, JSONL export) | ~1 hour |
| Generation (150 deals, ~200 3-way decisions) | ~5 min runtime |
| GTO Expert labelling (200 decisions) | ~2-3 hours agent time |
| Quality control + spot-check | ~30 min |
| Export + v9-3way training | ~15 min |
| Reference set evaluation + gate check | ~5 min |

**Total: ~4-5 hours, mostly labelling time.**
