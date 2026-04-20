---
date: 2026-04-20
from: Main terminal (reviewer/orchestrator)
to: Builder (future v2.5 work) · Owner
re: v2.5 queue — pro-level range-narrowing gaps NOT covered by Stage 3.5
status: QUEUED for v2.5; explicit out-of-scope for v2.4
---

# v2.5 Queued — Pro-Level Range-Narrowing Gaps

Owner audit question (2026-04-20): does the current range-narrowing
plan match how real pros apply it?

Honest answer: Stage 3.5 fixes dimension #1 (action chaining)
which is the biggest visible bug. Pros condition on 7-8
dimensions; we capture ~1.5 after Stage 3.5. Most remaining gaps
are documented as out-of-scope in the Stage 3.5 doc. One is NOT
documented and is newly queued here.

## Dimension coverage after Stage 3.5

| # | Dimension | v2.4 status | v2.5+ ticket |
|---|---|---|---|
| 1 | Action history across streets | ✅ Stage 3.5 | n/a |
| 2 | **Bet sizing per bet** | ❌ **NEW GAP — see §1** | **v2.5 ticket** |
| 3 | Raise-aware call | deferred §4.2 | v2.5 ticket (§2) |
| 4 | Multiway cross-conditioning | deferred §4.3 | v2.6+ (data structure change) |
| 5 | Opponent type priors | out-of-scope §4.4 | v3+ (new data needed) |
| 6 | Stack depth conditioning | out-of-scope §4.4 | v3+ (new data) |
| 7 | Metagame / history | N/A | static model; out-of-scope |
| 8 | Live tells | N/A | not applicable |

## §1 — Bet-size-conditional narrowing (the undocumented gap)

### Problem

`range_narrowing.py` tables use one scalar per (category, street, action_type):

```python
RIVER_BETTING_FREQUENCIES = {
    'nuts': 0.95, 'strong_value': 0.90, 'medium_made': 0.08, ...
}
```

This implicitly assumes one bet sizing (~66% pot). Solver GTO
actually varies frequencies by sizing — e.g., a 33% pot river
bet typically has more medium-made value bets than 75%+ does,
because small sizings target thinner value. A 150% overbet is
far more polarized toward nuts/air.

Our current tables conflate all sizings into one frequency.
Range composition is therefore off whenever villain's actual
sizing differs from the implicit baseline.

### Solver-grounded fix

Expand tables to (category, street, action_type, sizing_bucket):

```python
RIVER_BETTING_FREQUENCIES = {
    ('nuts', 'small'):  0.92,  # 33% pot
    ('nuts', 'medium'): 0.95,  # 50-75% pot
    ('nuts', 'large'):  0.97,  # 75-125% pot
    ('nuts', 'overbet'): 0.99, # >125% pot
    ('medium_made', 'small'): 0.15,
    ('medium_made', 'medium'): 0.08,
    ('medium_made', 'large'): 0.02,
    ('medium_made', 'overbet'): 0.01,
    ...
}
```

Sizing bucket derived from `bet_to_pot` ratio at the time of
narrowing application.

### Scope for v2.5

- **Derive tables.** Solver runs across positions, board
  textures, and sizing buckets. This is the lift — requires
  GTO Wizard or similar. Multi-day data task.
- **Modify narrow_to_betting_range signature** to accept
  `sizing_bucket` parameter.
- **Update `narrow_by_action_history`** to pass villain's
  actual sizing when iterating action_history.
- **Backfill audit** on v2.4 training CSV: re-extract villain
  composition with sizing-aware narrowing; compare to v2.4
  values; document shift.
- **Retrain v2.5** with expanded feature-vector values.

### Why v2.5 not v2.4

- v2.4 Stage 3.5 fixes the biggest bug (action chaining) which
  is observable to owner in playtest logs RIGHT NOW.
- Sizing-conditional requires new solver data that doesn't
  exist.
- Sequencing: ship action-chain fix, verify it holds on
  playtest, then commission sizing data when v2.4 is stable.

## §2 — Raise-aware call narrowing (documented in §4.2)

### Problem

A "call-of-a-raise" has a materially tighter range than a
"call-of-a-bet." Current `narrow_to_continuing_range` (Stage
3.5, Option A or B) doesn't distinguish.

### Scope for v2.5

- Split `narrow_to_continuing_range` into
  `narrow_call_after_bet` and `narrow_call_after_raise`.
- Derive solver-grounded raise-continuing tables (less data
  but still a solver lift).
- Wire through `narrow_by_action_history` by checking the
  preceding action on the same street.

### Why v2.5

Marginal improvement over Stage 3.5 baseline. Observable impact
smaller than #1 (bet sizing). Lower priority in the queue.

## Items NOT ticketed (out-of-scope by architecture)

- **Multiway cross-conditioning (#4):** would require data
  structure change to track ALL villains per decision, not just
  primary. Blocks on architectural work. v2.6+ at earliest.
- **Opponent type priors (#5):** app has no opponent-specific
  priors; static position-level ranges only. v3+ if ever.
- **Stack depth (#6):** same category as #5 — requires
  per-opponent priors + depth-conditional solver runs.
- **Metagame/history:** static inference model; out-of-scope
  permanently.
- **Live tells:** not applicable to non-live training app.

## Pro-quality bar vs GTO teaching bar

Honest framing: this app teaches baseline GTO theory. Pros
deviate from GTO based on reads; students learn GTO to know
what they're deviating from. The *baseline* matters more than
the exploitation adjustments for a teaching tool.

That said, dimension #2 (bet sizing) IS part of GTO itself —
not an exploit. Worth capturing when solver data allows.
Dimensions #5-6 are exploit-territory and lower priority for
the app's educational mission.

## Queue placement

Added to manifest v1.5 `queued` section:
- `v2_5_bet_sizing_conditional_narrowing`
- `v2_5_raise_aware_call_narrowing`

Both blocked on v2.4 ship + solver data commissioning. Neither
blocks anything upstream.

## Action

- v2.4 Stage 3.5: **proceed unchanged.** GTO dispatch with
  current docs still the right next step.
- v2.5 queue: these tickets wait for v2.4 ship + solver
  resources.
- Owner decision point for v2.5 later: commission solver data
  for sizing-conditional tables when v2.4 is stable.
