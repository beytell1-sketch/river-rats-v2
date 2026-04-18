---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: TICKET v2.4 P0 — calibration-anchor pre-flight gate
status: FILED — P0 for v2.4, ready to pick up when owner gives go
scope_bundle: v2.4 (alongside Path C rescope, existing tickets)
---

# TICKET v2.4 P0 — Calibration-Anchor Pre-Flight Gate

## Why this is P0

v2.3.2 passed all litmus gates (air 95%+, value 99%+, holdout 90%+)
but failed a calibration anchor (`d2410_CO_turn`: solver-verified BET,
v2.3.2 predicted CHECK). The β panel re-label identified this as the
linchpin of the Path C regression — "the exact class the calibration
anchor was designed to protect."

This gate would have:
- Caught v2.3.2 at training-report-review, before 45 min of wasted
  self-play compute
- Flagged the regression without requiring either (a) per-hand diff
  across 90 holdout rows or (b) full self-play diagnostic
- Surfaced the root cause directly (compressed-SPR TPGK class missed)

**Cost to implement: ~1-2 hours.** Highest EV gate we can add.

## What exists today

The v3.1 prompt's `Calibration Notes` section (line ~651-685) lists
7 named anchors with expected actions:

**v2 reversal anchors:**
- MW-30: CALL (40% equity, 18% pot odds, action-history narrowing)
- MW-33: RAISE (0.885 equity, set vs bet+call)
- MW-50: FOLD (0.329 equity, BTN raised flop)

**v2.3 MW anchors:**
- d8886_BTN_flop or d8886_BB_flop: BET (QcJc on 2s5dJd, solver 50/50)
- d2410_CO_turn: BET (JcKs on Jd9d3h+6d)
- d8963_HJ_turn: BET (solver 50/50)
- d3178_CO_river: BET (AA on JhQcJc+Ks+5h)

These are tracked in the prompt but NOT mechanically gated against
trained models.

## Proposed implementation

### A. Calibration-anchor fixture

Create `river-rats-core/calibration_anchors.py` with an explicit list:

```python
CALIBRATION_ANCHORS = [
    {
        'anchor_id': 'd2410_CO_turn',
        'source': 'v3.1 Calibration Notes (prompts/gto_labeller_v3.1.md:~678)',
        'situation': {
            'hero_cards': ['Jc', 'Ks'],
            'board_cards': ['Jd', '9d', '3h', '6d'],
            'hero_pos': 'CO',
            'villain_positions': [...],  # from test_set_50_labelled
            'street': 'turn',
            'facing_bet': False,
            # ... full SituationSpec fields
        },
        'expected_action': 'BET',
        'tolerance': 'strict',  # or 'mixed' for d8886, d8963
        'rationale': 'TPGK on J-high turn, checked-to at compressed SPR ~1',
    },
    # ... other 6 anchors
]
```

### B. Pre-flight evaluator

Create `river-rats-core/evaluate_calibration_anchors.py`:

```python
def run_anchor_gate(model_path, csv_path):
    """Run every calibration anchor through the model; return pass/fail.
    STRICT anchors must hit exact action. MIXED anchors must have the
    expected action as top-2 prob with >=0.20 weight."""
    results = []
    for anchor in CALIBRATION_ANCHORS:
        # Build spec via SituationFactory OR load directly from test set
        # Run oracle prediction
        # Compare vs expected_action + tolerance
        results.append({'anchor_id': ..., 'pass': ..., ...})
    return results
```

### C. Integration into training pipeline

At the end of each `train_v2_N_M.py`:

```python
logger.info("--- Calibration anchor pre-flight ---")
results = run_anchor_gate(out_model, csv_path)
failures = [r for r in results if not r['pass']]
if failures:
    logger.error(f"CALIBRATION ANCHOR FAIL: {len(failures)} anchors missed")
    for f in failures:
        logger.error(f"  {f['anchor_id']}: expected {f['expected']}, got {f['predicted']}")
    logger.error("STOP: do not accept this model until anchors resolve.")
    # Option: exit non-zero here
```

### D. Option: integrate into evaluate_v2_2.py

Add `--anchors` flag that runs the anchor gate standalone for any
model. Useful for regression bisecting and historical model auditing.

## Acceptance criteria

- All 7 anchors encoded (or subset if hand-build is blocked by test-set schema)
- Pre-flight runs in <5s per model
- Integrated into `train_v2_3_1.py` + `train_v2_3_2.py` trailers (additive — won't break existing scripts; can be gated on a flag)
- Applied retroactively: confirm v2.2, v2.3-clean, v2.3.1, v2.3.2 match their known behavior against the anchor list
  - Expected: v2.2 + v2.3.1 PASS all anchors; v2.3.2 FAIL d2410 (validation that the gate works)

## Dependencies / sequencing

Does NOT depend on Path C rescope — this is orthogonal infrastructure.

**Order recommendation for v2.4:**
1. **P0: this ticket** (calibration-anchor pre-flight gate) — 1-2 hours
2. **P1a: hand_evaluator straight-draw fix** (existing ticket) — audit + KB spec + fix + retrain
3. **P1b: Path C rescope** — define target subspace by boundary-pattern (e.g., `worse_hand_pct >= 0.80 AND 0.55 <= eq < 0.75 AND vcb=1 AND spr <= 2` covers the d2410 class) + larger counter-example sets
4. **P2: blocker 2-flag design** (existing ticket; gated on teaching recentering)
5. **P2: HU counter-examples** (data already exists in v23_*_hu.jsonl; needs v3.2 prompt)

After P0 lands, every subsequent retrain (P1b onward) benefits from the gate automatically.

## Risk / edge cases

- **Anchor spec drift.** If KB Calibration Notes updates (new solver
  runs, revised reasoning), the anchor fixture must update too.
  Propose: anchor fixture file has its own versioning note linking
  to KB revision.
- **Anchor hand unavailable from test set.** Some anchors (e.g.,
  d8886_BB_flop in v2.3 MW anchors) reference specific hands in
  test_set_50_labelled.jsonl. If the test set doesn't include them,
  we build them via SituationFactory and note that spec as
  "synthesized" — documented in the anchor fixture.
- **Mixed anchors** (d8886, d8963 per v3.1 prompt) are 50/50 solver.
  Tolerance must accept either BET or CHECK as long as both appear
  in top-2 with reasonable weight. Don't treat them as strict.

## Future work (not in scope for this ticket)

- Expand anchor set from 7 to ~20-30 as more solver hands land
- Regression-per-hand bisect tool (given two models, diff which
  anchors pass/fail — complements the v2.3.2 β panel workflow)

## Not blocking anything

File this ticket and wait for owner's go on v2.4 scope. Ready to
pick up on direction.
