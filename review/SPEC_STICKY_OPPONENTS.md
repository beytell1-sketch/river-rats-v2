# Spec: Sticky Opponent Callbacks for 3-Way Situation Generation

**Date:** 6 April 2026
**Status:** SPEC — awaiting review before building
**Blocking:** 3-way training data generation (yield at 1.2%, gate is 3%)

---

## 1. Problem

The v8/v9 oracle is trained on heads-up data. When used as all 6
players in self-play, it over-folds multiway postflop — collapsing
3-way pots to heads-up before hero decisions are recorded.

This is circular: we need 3-way training data to fix the oracle's
multiway play, but the oracle's multiway play prevents us from
generating that data.

**Current numbers:**
- 6.3% of deals go multiway preflop (working)
- Only 1.2% of games produce a 3-way postflop decision (collapsed)
- Of 36 surviving situations, 34/36 are CHECK (no contested pots)

## 2. Key Insight

The self-play runner generates **situations**, not **labels**. The
GTO Expert agent labels them independently based on board, ranges,
position, and pot — not on what opponents actually did. So opponents
don't need to play correctly during generation. They just need to
stay in the pot long enough for hero to face a 3-way decision.

This is already how the pipeline works:
- `generate_3way_situations.py` produces situations
- `labelling_agent.py` sends them to the GTO Expert for labelling
- The Expert evaluates the poker situation, not the opponent's play

## 3. Proposed Change

### What

Add a `_make_sticky_callback()` function in `self_play.py` that
wraps the oracle callback for **non-hero opponent seats only**
during 3-way situation generation. This callback:

- **Preflop:** Uses the normal oracle/range-table path (unchanged).
  Preflop ranges must stay realistic to produce genuine multiway
  entries.
- **Postflop, 3+ way, not facing a bet:** Uses the oracle normally.
  No intervention needed — the oracle already checks here.
- **Postflop, 3+ way, facing a bet:** Overrides FOLD with CALL
  when the player's raw equity is above a threshold (default 15%).
  Below threshold, allows the fold.

### Why equity-gated, not "never fold"

Pure "never fold" creates unrealistic action sequences. If villain
calls a pot-sized river bet with 5% equity, the GTO Expert would
infer a strong villain range from that call, which changes its
advice for hero. An equity threshold of ~15% keeps villain behavior
plausible — villains stay in with draws, middle pair, overcards,
but fold obvious air facing big bets.

The Expert infers villain ranges from actions. If villain calls a
flop bet, the Expert assumes villain has at least a draw or pair.
With 15% equity floor, that assumption is roughly correct.

### Why not use heuristic AI opponents

The heuristic AI (`ai_decision()` with PersonalityProfile) exists
but uses `hand_strength_0_1()` for postflop decisions. The preflop
path would switch from range-table to the old Monte Carlo system,
producing unrealistic preflop ranges and fewer multiway entries.

We need oracle preflop (realistic ranges) + sticky postflop
(multiway survival). A callback wrapper is cleaner than mixing
two AI systems.

## 4. Exact Changes

### File: `self_play.py`

**Add new function** `_make_sticky_callback()` after
`_make_oracle_callback()` (after line 204):

```python
def _make_sticky_callback(oracle, params: dict,
                          equity_floor: float = 0.15) -> Callable:
    """Build a postflop-sticky callback for non-hero opponents.

    Preflop: identical to oracle callback (realistic ranges).
    Postflop in 3+ way pots facing a bet: overrides FOLD with CALL
    when raw equity >= equity_floor. This prevents the HU-trained
    oracle from collapsing multiway pots prematurely.

    Used ONLY for situation generation, not for hero decisions or
    production play.
    """
    use_router = isinstance(oracle, OracleRouter)

    def callback(game, player, context):
        # Preflop: use range-table engine unchanged
        if context.get('street') == 'preflop':
            preflop_state = {
                'num_raises_this_street': context.get('num_raises_this_street', 0),
                'num_callers': context.get('num_callers', 0),
                'hero_has_raised': False,
                'hero_position': player.position,
                'to_call': context['to_call'],
                'opener_position': context.get('opener_position'),
            }
            action, amount = ai_preflop_decision(
                player, context['current_bet'], context['pot'], preflop_state
            )
            return (action, amount)

        # Postflop: extract features, get oracle prediction
        feat_dict = build_features_from_game_state(player, game, context)
        num_opponents = len([p for p in context.get('active_opponents', [])
                            if not p.is_folded])

        if use_router:
            pred = oracle.predict(feat_dict, max(1, num_opponents))
        else:
            features = GtoOracle.features_from_dict(feat_dict)
            pred = oracle.predict(features)

        adjusted = adjust(pred, feat_dict, max(1, num_opponents), params=params)
        action = adjusted.adjusted_action.lower()

        # Sticky override: in 3+ way pots facing a bet, convert
        # FOLD to CALL if equity is above floor.
        # Use to_call > 0 as the facing-bet signal (reliable — always
        # in context), not context['facing_bet'] which may not exist.
        facing_bet = context.get('to_call', 0) > 0
        if (action == 'fold'
                and num_opponents >= 2
                and facing_bet
                and float(feat_dict.get('raw_equity', 0)) >= equity_floor):
            action = 'call'

        # Map action to amount
        if action in ('fold', 'check'):
            return (action, 0)
        elif action == 'call':
            return ('call', game.current_bet)
        else:
            amount = player.bet_this_street + max(int(context['pot'] * 0.67), 10)
            amount = min(amount, player.stack + player.bet_this_street)
            return (action, amount)

    return callback
```

### File: `self_play.py` — `_play_one_game()`

**Add parameter** `sticky_opponents: bool = False` to
`_play_one_game()` and the `SelfPlayRunner` class.

In `_play_one_game()` (around line 293), change opponent wiring:

```python
# Current:
p.decision_callback = _make_oracle_callback(
    self.oracle, baseline_params)

# New (when sticky_opponents=True):
if self.sticky_opponents:
    p.decision_callback = _make_sticky_callback(
        self.oracle, baseline_params)
else:
    p.decision_callback = _make_oracle_callback(
        self.oracle, baseline_params)
```

### File: `generate_3way_situations.py`

**Pass `sticky_opponents=True`** when constructing the
SelfPlayRunner:

```python
# Current (line 36):
runner = SelfPlayRunner([variant], num_deals=num_deals, seed=seed)

# New:
runner = SelfPlayRunner([variant], num_deals=num_deals, seed=seed,
                        sticky_opponents=True)
```

**Add CLI flags:**

```python
parser.add_argument('--no-sticky', action='store_true',
                    help='Disable sticky opponents (for baseline comparison)')
parser.add_argument('--equity-floor', type=float, default=0.15,
                    help='Equity floor for sticky opponents (default 0.15)')
```

## 5. What Does NOT Change

- **Hero callback:** Hero always uses the full oracle + adjuster
  + decision logging. Hero decisions are what get labelled.
- **Preflop for anyone:** All seats use range-table preflop.
  Multiway entry rates stay at ~6.3%.
- **Production play / coaching:** `sticky_opponents` defaults to
  False. No impact on any non-generation code path.
- **Labelling pipeline:** `labelling_agent.py`,
  `export_3way_training.py`, `calibration_exam.py` — untouched.
- **Oracle model / adjuster:** No changes to prediction logic.

## 6. Expected Impact

With 15% equity floor, opponents in 3-way pots will:
- Still fold air facing large bets (correct — pure air folds)
- Call with draws, middle pair, overcards (sticky — stay in pot)
- Continue to bet/raise when the oracle says to (unchanged)

**Conservative estimate:** If 50% of multiway pots survive (up
from ~20%), yield goes from 1.2% to ~3%. Action distribution
should improve because more opponents staying in = more betting
opportunities for hero.

## 7. Validation Plan

1. Build the callback (small — ~40 lines of new code)
2. Run 500-deal yield check with sticky opponents
3. Compare yield and action distribution vs the 1.2% baseline
4. Primary gate: yield >= 3%
5. Secondary gate: action distribution has >20% non-CHECK
   (If primary passes but secondary doesn't, proceed anyway —
   CHECK-heavy first iteration is acceptable. The v9-3way model
   trained on it will bet more, producing richer data next round.)
6. If primary gate passes, proceed to full generation run

## 8. Risks and Open Questions

**Risk: Equity calculation accuracy.** `raw_equity` in `feat_dict`
is computed by the feature extractor. If this value is unreliable
in multiway spots (it's calibrated for HU), the 15% threshold
might not behave as expected. Mitigation: the threshold is
conservative — 15% is low enough that only genuine trash folds.

**Risk: Inflated pot sizes.** Sticky opponents calling more bets
means bigger pots on later streets. The GTO Expert labels based on
pot odds, so bigger pots could shift recommendations. This is
acceptable — realistic multiway pots ARE bigger than HU pots.

**Equity floor CLI flag:** Added. `--equity-floor 0.15` default,
tunable without code changes.

**Open question: Should sticky mode also prevent opponent FOLDS
when not facing a bet?** Currently no — if not facing a bet, the
oracle checks (not folds), so there's no fold to override. The
sticky logic only fires on `fold + facing_bet + 3+ way`.

## 9. Files to Change

| File | Change | Lines |
|------|--------|-------|
| `self_play.py` | Add `_make_sticky_callback()` | ~40 new |
| `self_play.py` | Add `sticky_opponents` param to class + `_play_one_game()` | ~8 changed |
| `generate_3way_situations.py` | Pass `sticky_opponents=True`, add `--no-sticky` flag | ~5 changed |

Total: ~53 lines changed/added across 2 files. No new files.
