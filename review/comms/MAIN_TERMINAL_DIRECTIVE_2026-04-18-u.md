---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Builder (v2.4 queue) · Teaching terminal (hold)
re: Blocker-feature research synthesized → v2.4 tickets queued; teaching recentering resumes after features land
status: DIRECTIVE
related: review/research/BLOCKER_FEATURE_EXPANSION.md (full report)
---

# Blocker Feature Expansion — Synthesis

## What the research found

- `flush_block_pct` is the ONLY range-weighted blocker feature
  currently in the oracle. That's it.
- `range_decomposition.py` already classifies every villain
  combo into sub-categories (nut_flush, top_set, nut_straight,
  flush_draw, oesd, etc.). **Infrastructure is there; it just
  isn't wired into blocker features.** This makes the expansion
  moderate complexity, not solver-level.
- Prior research at `review/RESEARCH_CBET_R5_BLOCKERS.md` already
  quantified +8-15pp fold-equity impact of nut-flush blockers in
  3-way c-bet. Evidence supports prioritization.

## Three features queued for v2.4 (in priority order)

### 1. `nut_flush_block` — P0 for v2.4

**What:** Binary (or rank-graded) signal for "hero holds the
Ace of the board's flush suit."

**Why first:** Directly addresses the directional concern owner
raised. Nut-flush blocker is the sign-flip case: holding Ax of
suit blocks ALL of villain's nut-flush combos (high-impact),
not just a fractional reduction. Prior research already
quantifies the EV delta.

**Complexity:** Trivial. ~10 lines. Zero-cost to existing
training pipeline.

**Reference:** `feature_extractor.py:1240-1362` (existing flush
blocker, next to which this belongs).

### 2. `draw_block_pct` — P1 for v2.4

**What:** Range-weighted fraction of villain's DRAW combos
blocked (flush draws + straight draws), distinct from
made-hand blocks.

**Why:** This is the directional counterweight to made-hand
blockers. It's the feature that lets the oracle distinguish
"hero blocks villain's bluffs" (bad for bluff-catcher) from
"hero blocks villain's value calls" (good for bluff-bettor).
Exactly the weak-made-facing-bet case owner flagged.

**Complexity:** Moderate. ~60-100 lines. Reuses
`range_decomposition.py` classifier output — no new range
machinery needed.

### 3. `nut_made_block_pct` — P1 for v2.4

**What:** Generalizes `flush_block_pct` to all nut-category
made hands (set, two-pair, straight, flush, full house).

**Why:** Current `flush_block_pct` is one slice of the full
picture. If hero blocks villain's straight but not flush,
current features don't capture it. This unifies across made-
hand categories.

**Complexity:** Moderate. ~80-150 lines. Also reuses the
existing classifier. Eventually replaces `flush_block_pct` as
the primary blocker feature.

**Reference:** `hand_categories.py:488-530`
`count_combos_with_blockers` is the reusable primitive.

## Implementation discipline (per hard rules)

When v2.4 comes up:

1. **Add features first, retrain, validate** — no teaching
   changes until oracle can use them
2. **Calibration-anchor pre-flight gate** (P0 from directive-t)
   must run before any self-play burn
3. **Distribution inspection** on any new counter-example sets
   per `feedback_concentration_effect.md`
4. **Both classes locally** per
   `feedback_counter_example_balance.md` — if adding training
   examples that exercise new blocker features, pair them
5. **Retire `flush_block_pct`** only after
   `nut_made_block_pct` is validated to cover its signal +
   more

## Teaching implications — revisit AFTER v2.4 features land

Three new observations become possible at L3+:

- "You hold the nut-flush blocker"
- "You block villain's draws"
- "You block villain's value range"

The second is new — no current analog in the situation
describer. Once `draw_block_pct` and `nut_made_block_pct`
exist as oracle features, teaching can surface them as
observation-only flags in the flag window. Template branches
on `decision_reporter.action` provide directional framing
without emitting WHY.

**Teaching recentering walkthrough resumes after v2.4 features
ship.** The rest of the recentering (groups A–G, other flags)
is architecturally independent of blocker expansion — we COULD
advance it now, but owner correctly identified that locking a
teaching schema before we know what blocker features the oracle
will have risks re-committing to an incomplete flag catalogue.

Reasonable options:

- **A**: Resume recentering now, treat blocker slot as "TBD
  after v2.4," lock in all non-blocker decisions
- **B**: Pause entire recentering until v2.4 blocker features
  land, then do a single clean walkthrough with full picture

**My recommendation: A.** Groups A–G (field classification,
primary-vs-flag-window architecture, L3 prose cuts) and 8 of
9 active flags are independent of blocker design. Locking
them in now gives teaching terminal a plan to execute, and
the blocker flag slot is the only placeholder. Owner call.

## v2.4 ticket list — updated

Adding to directive-t's queue:

| Priority | Ticket | Source |
|---|---|---|
| **P0** | Calibration-anchor pre-flight gate | directive-t |
| **P0** | `nut_flush_block` feature | this directive |
| **P1** | Path C target subspace rescope | directive-t |
| **P1** | `draw_block_pct` feature | this directive |
| **P1** | `nut_made_block_pct` feature | this directive |
| **P1** | `hand_evaluator.py` draw_outs semantics | directive-t |
| **P1** | Larger counter-example sets | directive-t |
| **P2** | HU counter-examples | Decision-h deferred |
| **P2** | Retire `flush_block_pct` after nut_made_block_pct validated | this directive |
| **P2** | Honest-CHECK distinct bucket if weights relax | directive-t |

## Nothing for builder to start right now

v2.4 is owner-paced. No work begins until owner says go. This
directive captures the scoping so when owner is ready, the
queue is clear.

## Nothing for teaching to do right now

Teaching stays stood down pending owner's A/B call on recentering
resumption.
