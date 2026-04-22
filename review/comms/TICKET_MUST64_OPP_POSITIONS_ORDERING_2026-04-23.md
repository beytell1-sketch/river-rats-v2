---
date: 2026-04-23
from: Main terminal (orchestrator)
to: Builder · Teaching · Owner
re: MUST #64 `opponent_positions` ordering convention — surface gap flagged by teaching
status: QUEUED — small scope; best addressed before Stage 5 retrain so training + teaching agree on primary-villain convention
triggered_by: Teaching GTO + V3 review of v4.1 plan 2026-04-23
---

# MUST #64 `opponent_positions` Ordering Convention

## Trigger

Teaching's GTO + V3 reviewer pass on the v4.1 NaN-render plan
surfaced a gap in MUST #64's multiway spec: "first in `opponent_positions`"
determines which villain's range is rendered as the scalar composition
(`villain_tp_pct`, etc.) when teaching can't per-villain-render every
opponent.

No poker-meaningful ordering contract exists today. If `opponent_positions`
comes from a dict iteration or set operation, ordering is effectively
arbitrary. That means the SAME multiway hand could produce different
primary-villain composition values on different runs (or different
machines, different Python versions, etc.) depending on dict hash
randomisation.

## Why this matters

- **Teaching display:** multiway hands where composition is read from
  the primary villain must be stable across runs. Current spec leaves
  that implicit.
- **Training data:** if re-label at Stage 4 produces different primary-
  villain assignments on different runs of the same hand, the training
  CSV is non-deterministic across extraction passes. Not a correctness
  bug at model-fit time (XGBoost is deterministic given a fixed CSV),
  but reproducibility is corrupt.
- **Playtest logs:** the oracle outputs a composition value; the
  teaching layer reads the same; game renders. If primary-villain
  swaps between two runs, the same hand renders differently — learner
  confusion.

## Current behavior

`_get_chain_narrowed_villain_range` iterates `opponent_positions`
(per commit 4.1 spec) and stores `per_villain_ranges[opp_pos]` in
order. The "primary villain" is effectively `opponent_positions[0]`
when a scalar composition is rendered.

`opponent_positions` source-of-truth: check `feature_extractor.py`
callers. Likely constructed from:
- `hand['_opponent_positions']` (if present in input)
- Derived from `hand['_action_history']` by filtering to non-hero
  positions
- Fallback to `range_manager` defaults

No single source-of-truth document. No ordering contract.

## Options

### (a) Acting-order ordering

Order by position-to-act (BTN first preflop, BB last preflop;
flop/turn/river reverses for OOP). Stable + poker-meaningful.
Matches how a player mentally reads a spot ("BTN opened, BB
defended" — BTN is 'first' in the spot).

**Cost:** position-to-act varies by street + hand shape. Preflop ≠
postflop. For a single "primary villain" assignment across the
whole hand, need a tiebreaker (decision street? full-hand-average
aggression? first-to-bet?).

### (b) Position-strength ordering

Order by positional seat strength (BTN > CO > HJ > UTG > SB > BB
in 6max; adapt per table size). Stable + poker-meaningful.
Handles the tiebreaker cleanly (static lookup).

**Cost:** "position-strength" is a teaching-friendly abstraction but
doesn't map to "who's the biggest threat on this specific hand."
A passive BTN in a hand where BB donk-leads = BB is the real threat;
BTN is still primary by this rule.

### (c) Primary-bettor ordering (dynamic)

Order by who was the most-recent aggressor in the decision-street
action history. If no aggression on the decision street, fall back
to (b) or (a).

**Cost:** More complex; tiebreaker logic per-hand. But matches the
"who's actually threatening hero" reading.

### (d) Canonical lexicographic (arbitrary but stable)

Just sort `opponent_positions` alphabetically. Stable, deterministic,
cheap. Not poker-meaningful but not poker-harmful either.

**Cost:** Teaching-layer rendering of "primary villain" as
`opponent_positions[0]` would have no poker rationale; learner sees
"BB" as primary even when BTN is clearly the threat. Rejected by
teaching's reviewer.

## Recommendation

**Option (c) primary-bettor ordering, falling back to (b) position-strength.**

- If decision-street action-history has villain aggression: primary =
  most-recent aggressor
- If decision street is checked-to-hero with no villain aggression:
  primary = highest position-strength among live opponents
- If no opponents are live (edge case, folded): no primary; scalar
  composition is absent

This matches how a pro reads a spot ("BB donk-led on this dry flop,
so BB is the threat; BTN is secondary"). Satisfies both determinism
(same hand → same ordering) and poker-meaningfulness (primary actually
maps to the relevant villain).

## Scope for implementation

Small — single helper `_order_opponents_by_primary(...)` in
`feature_extractor.py`. Two call sites:
- `_get_chain_narrowed_villain_range` entry point
- Any direct iteration of `opponent_positions` that needs stable order

Test plan:
- Multiway donk-led: primary = donker
- Multiway cbet + call: primary = cbetter
- Multiway checked-to-hero: primary = highest positional strength
- Multiway all-folded-but-hero: no primary (edge)
- Determinism across runs: same input → same `opponent_positions` tuple

## Sequencing

Not Stage 3.5 scope. Candidate for:
- **v2.5 ticket** if deferred (preferred): bundle with other scalar-
  composition refinements. Not blocking.
- **Pre-Stage-5 small fix-forward** if the non-determinism surfaces
  during Stage 4 re-label or Stage 5 training-CSV audits. Builder's
  call at Stage 4 start — if training is actually non-deterministic
  across runs, fix-forward before re-label.

Teaching confirmed this is non-blocker for v4.1 NaN-render work —
teaching renders per-villain composition via `_per_villain_composition`
dict iteration which is stable by dict-insertion-order. Scalar-
composition-as-primary is only used when `_per_villain_composition`
isn't available; teaching can route around.

## Action

- Filed as v2.5 candidate in manifest
- Builder picks up at v2.5 OR at Stage 4 re-label start if non-
  determinism surfaces
- No blocking impact on Stage 3.5 remaining commits (8-16)

## Reference

- Teaching plan GTO review: `river-rats-teaching:review/comms/TEACHING_V4_1_PLAN_GTO_REVIEW_2026-04-22.md`
  (teaching-repo local commit 34a0fc1; see §11 of this ticket for
  push-path notes)
- MUST #64 canonical spec: `review/comms/BUILDER_V24_STAGE35_BLUEPRINT_V2_3_1_PATCH_2026-04-22.md`
- Commit 4.1 implementation: `feature_extractor.py:_get_chain_narrowed_villain_range`
