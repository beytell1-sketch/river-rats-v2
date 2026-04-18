---
date: 2026-04-18
from: Builder
to: Main terminal / Owner
re: TICKET — hand_evaluator.py draw_outs semantics: board-only straight draws
  falsely attributed to hero
status: FILED — scope v2.3.2 or v2.4 (not a v2.3.1 blocker)
related_directive: Decision 1 from 492da51 (teaching's false-draw finding)
---

# TICKET — `hand_evaluator._check_straight_draw` Board-Only Bug

## Summary

`river-rats-core/hand_evaluator.py::_check_straight_draw` (lines
494-509) unions `hole_ranks + board_ranks` and returns
`has_straight_draw=True` / `draw_outs=8` (OESD) or `draw_outs=4`
(gutshot) whenever a 4-card window of span ≤ 4 exists in the
union — **without verifying hero's hole cards contribute to the
window**. Board-only straight draws are falsely attributed to
hero.

`_check_flush_draw` (same file) is NOT affected — it correctly
requires `our_suited >= 1` at line 489.

## Why this is being filed now

Teaching terminal flagged "oracle cites draw as reason to BET/CALL
when draw is board-only and hero has no part." Per Decision 1 (in
commit 492da51):

> Teaching ships coherence guard immediately: suppress
> gutshot/OESD claims when air + is_made=0 + has_sdv=0 +
> |raw_eq − improvement_prob| < 0.02. Suppression, not fabrication
> — allowed.
>
> **Builder files v2 core ticket for hand_evaluator.py draw_outs
> semantics. v2.3.2/v2.4 scope, not a v2.3.1 blocker.**

Teaching's coherence guard is a downstream suppression; this
ticket tracks the upstream root-cause fix.

## Repro

```python
from hand_evaluator import evaluate_hand

# Hero K-Q has NO connection to 4-5-6-7 on board; it's a board OESD
ev = evaluate_hand(['Kh', 'Qd'], ['4c', '5c', '6c', '7h'])
print(ev.has_straight_draw)  # True  (WRONG — hero plays no role)
print(ev.draw_outs)          # 8     (WRONG — hero draws dead)
print(ev.category)            # 'overcards'

# Control: hero KQ on J-T-3 does have OESD
ev = evaluate_hand(['Kh', 'Qd'], ['Jc', 'Tc', '3h'])
print(ev.has_straight_draw)  # True (correct — hero contributes)
```

Observed (run during sweep): `evaluate_hand(['Kh','Qd'],
['4c','5c','6c','7h'])` → `has_straight_draw=True, draw_outs=8`.

## Root cause (source)

`river-rats-core/hand_evaluator.py` line 494-509:

```python
def _check_straight_draw(hole_ranks, board_ranks):
    all_ranks = sorted(set(hole_ranks + board_ranks))
    # ...
    for i in range(len(all_ranks)):
        for j in range(i + 1, min(i + 5, len(all_ranks))):
            window = all_ranks[i:j+1]
            if len(window) >= 4:
                span = window[-1] - window[0]
                if span == 3 and len(window) == 4:
                    return True, 8  # OESD — no hole-contribution check
                elif span == 4 and len(window) == 4:
                    return True, 4  # Gutshot — no hole-contribution check
    return False, 0
```

Same bug exists in `river-rats-complete/hand_evaluator.py` at the
same function — cross-repo.

## Proposed fix

Require the 4-card window to contain ≥ 1 rank from `hole_ranks`:

```python
if len(window) >= 4:
    span = window[-1] - window[0]
    hole_in_window = any(r in hole_ranks for r in window)
    if not hole_in_window:
        continue   # board-only draw — hero does not hold this draw
    if span == 3 and len(window) == 4:
        return True, 8
    elif span == 4 and len(window) == 4:
        return True, 4
```

Stricter alternative (to consider on fix PR): require ≥ 1 hole
card to appear in the completed 5-card straight (window + 1
completing rank). The minimal +1 rule above catches the purely-
dead cases without over-filtering legitimate gutshots; the stricter
rule would also tighten corner cases where the hole card appears
outside the eventual 5-straight. GTO review recommended before
fix PR.

## Features affected

Primary: `has_straight_draw`, `draw_outs`.

Downstream (all read these):
- `is_made_hand`/`overcards`/`one_overcard` category unaffected
- Draw equity estimate (`draw_equity`) inflates in affected spots
- Teaching `_draw_description` (coaching/observation_builders.py:40)
  — fixed downstream as soon as feature is fixed
- Model input features → all training + inference rows where a
  board-only OESD exists

## Impact — why this is a retrain, not a hotfix

**Training data:** rows in the current training set where the
buggy feature fired may have expected-action labels that implicitly
relied on "hero has a draw" signal. Examples:
- Pass 4 labels: panels saw feat_dict including
  `has_straight_draw=1, draw_outs=8` for board-only OESDs and may
  have reasoned "semi-bluff → BET" or "hero has equity → CALL"
  for a hand actually drawing dead. Those labels need review.
- Pilot, CALL supplement: same risk.
- v2.3.1 air-CHECK counter-examples: SAFE. The generator
  predicate `draw_outs <= 2` excluded any 8-out board-only OESDs
  that would have slipped in. Actually acts as a self-check: the
  picker would have dropped those candidates and moved to genuinely
  air hands.

**Test sets:** FB-40 and MW-50 hands with board-only OESDs may
have expected-action labels influenced by the bug. Eval numbers
may shift after fix. Cannot estimate magnitude without running.

**Model:** a model trained on buggy features has learned
"has_straight_draw=1 → reason to BET/CALL" in cases where hero
has no draw. Fixing the feature without retraining leaves the
model's internal weights calibrated to the buggy signal. **Ship
of the fix requires retrain + re-eval.**

## Scope + sequencing

Per Decision 1: **v2.3.2 or v2.4 scope — not a v2.3.1 blocker.**

Recommended sequence when picking this up:

1. **Audit** — scan training + test data for affected rows:
   ```python
   # For each hand, re-run hand_evaluator with proposed fix;
   # count deltas on has_straight_draw / draw_outs.
   ```
   Estimate: 10–30 min compute. Count of affected rows informs
   whether this is a small patch or broader relabel.
2. **Spec** — pick fix variant (+1 vs stricter). GTO-expert review
   on the proposed semantics.
3. **Fix** — apply to `hand_evaluator.py`. Write unit tests for
   the board-only patterns (K-Q on 4-5-6-7; AA on 6-7-8 — already
   correctly excluded because made-hand path short-circuits, but
   worth asserting; 22 on 9-T-J — same).
4. **Rebuild features** — re-run extraction on any affected rows.
5. **Label review** — for rows where `has_straight_draw` flipped
   True → False, flag to GTO panel for label reconsideration.
   Rows where it was already False stay untouched.
6. **Retrain** — fresh model on corrected features + reviewed
   labels.
7. **Re-evaluate** — FB-40, MW-50, flop litmus, generalization
   sweep, self-play diagnostic. Expect slight shifts.

## Not blocking v2.3.1

Reasons this doesn't hold up v2.3.1:

- **Teaching coherence guard per Decision 1** suppresses the
  visible symptom (false "you have a draw" text) from the student
  experience immediately.
- v2.3.1 air-CHECK rows are unaffected (predicate `draw_outs<=2`
  excluded affected candidates).
- Litmus gates and generalization sweep both passed with the bug
  still in place — the air-BET fix is orthogonal to the false-
  draw class.
- Self-play diagnostic at v2.3 scale was fine (~2000 deals). Any
  marginal playtest error from this bug is an edge case, not a
  systematic regression.

## Scope prediction

Best-guess: v2.3.2 priority if playtest surfaces false-draw cases
the teaching guard misses; v2.4 priority otherwise (bundle with
HU counter-examples + other feature refinements). Owner calls
scope.

## Cross-ref

- Logic source: `river-rats-core/hand_evaluator.py::_check_straight_draw`
- Teaching consumer: `coaching/observation_builders.py::_draw_description`
- Teaching guard (to be shipped per Decision 1): teaching terminal
- Related bug class: none known for flush_draw (verified clean)

## Action requested

Log this ticket. No immediate action needed on the builder side
until scope is picked up.

I'll flag this ticket in the v2.3.1 ship manifest trailer when
the coordinated game-adapter swap happens, so the open defect is
documented against the model that contains it.
