# Phase B-2: Multiway-biased sampling in data generation pipeline

**Status:** FILED 2026-04-11. Unblocks v3 (563-situation) rebuild.
Does NOT block v2.2 (100-200 situation iteration).
**Filed by:** Main terminal (orchestrator), during Phase B ship.
**Depends on:** Phase B (Preflop Range Fix) landing first.

## The problem Phase B did NOT solve

Phase B replaced flat (all 1.0) RFI/CALL/THREE_BET frequencies with
solver-backed mixed frequencies. Projected yield improvement:
**0.51% → ~0.9% 3-way** (ml-architect design,
`review/comms/ML_ARCHITECT_PHASE_B_DESIGN_2026-04-11.md` §4).

The 3-5% original target was **not achievable by range data changes
alone**. The bottleneck is structural: a random deal simulator
samples deal positions uniformly, so the joint probability
`P(opener opens) × P(caller calls) × P(BB defends)` caps around 0.9%
regardless of how wide the individual ranges get, without also
widening catastrophically beyond GTO.

**Volume impact:**
- v2.2 (100-200 new self-play situations): ~11-22k deals. **Acceptable.**
- v3 (563 full rebuild): ~45-65k deals. **Borderline — would be
  painful but not blocking.**
- Anything beyond v3 (v4, v5, position-specific deep dives): **Blocking.**

## The fix (scope of B-2)

Change `river-rats-core/generate_3way_situations.py` and/or
`river-rats-core/self_play.py` to **stratify sampling over the
decision-space axes we care about**, rather than relying on random
deal outcomes to surface multiway spots.

### Option A: Decision-point sampling (recommended starting point)

Instead of "deal a random hand and see who continues," directly
sample from the target distribution:

1. For each target situation, independently draw:
   - Street (flop/turn/river)
   - Facing action (check-to / bet-into / check-raise / etc)
   - Hero position
   - Num opponents (2 or 3, per 3-way/4-way mix)
   - Opener position (matters for range composition)
2. Construct the hand state from those axes, filling in opponent
   cards by forward-simulating villain ranges.
3. Accept the situation if it's internally consistent (no card
   conflicts, ranges non-empty).

**Pros:** Yields trivially hit 100% of the target axis distribution.
**Cons:** Loses realism — some decision points sampled this way
would be rare in actual games. Creates label leakage risk if the
sampling distribution correlates with the label in unexpected ways
(e.g., over-sampling bet-into spots changes the facing-bet base rate).

### Option B: Rejection sampling with importance weighting

Keep the current random-deal simulation but:
1. Run 10× the deals we actually need
2. Score each multiway situation that emerges against the target
   axis distribution (e.g. "do we have enough BTN-as-hero spots?")
3. Accept/reject to hit the target distribution
4. Re-weight training labels by inverse sampling probability to
   avoid bias

**Pros:** Preserves game realism. No leakage risk.
**Cons:** Still slow at the bottleneck positions. 10× compute.
Importance weights complicate training.

### Option C: Hybrid (seeded deals)

1. Pre-seed the deal with a specific (hero_pos, opener_pos, num_opp)
   triple
2. Let the rest of the hand play out naturally
3. Accept the situation

**Pros:** Guaranteed axis coverage + mostly-natural dynamics.
**Cons:** Seeding affects which pairs of hole cards are in play.

## Design risks (leakage)

**Critical:** biased sampling can introduce label leakage if the
sampling distribution correlates with the label. Examples:

- Over-sampling "facing bet" situations changes the base rate of
  FOLD vs CALL vs RAISE — a model can learn "if sampled from this
  pipeline, base rate is X" and then pattern-match the sampling
  distribution rather than poker logic.
- Over-sampling specific positions can cause the hero_percentile
  feature to shift meaning.
- If villain ranges are forward-simulated from GTO, sampling could
  bake GTO label-leakage into features that should be range-agnostic.

**Mitigation:** Any B-2 design must include a leakage test
**before** it generates training data:

1. Train a tiny model to predict "was this situation sampled from
   the old pipeline or the new one?" using only features.
2. If accuracy > 60%, the sampling is introducing leakage. Iterate.

## Deliverables (when B-2 runs)

1. ml-architect brief: compare A/B/C, pick one with rationale
2. architect blueprint: exact insertion points in
   `generate_3way_situations.py` / `self_play.py`
3. Leakage test implementation (distinguish-old-from-new classifier)
4. Yield measurement: target 3-5% effective axis coverage after
   rejection/stratification
5. v3 rebuild run on the new pipeline (at least the first 100
   situations) as smoke test
6. Reviewer gate: tests pass, leakage test <60%, yield target met

## Non-goals for B-2

- Do NOT touch range_manager.py (Phase B owns that)
- Do NOT touch labelling logic (that's orthogonal)
- Do NOT try to fix the 5 remaining v2.1 reference failures — those
  are a labelling/model concern, not a data-generation concern
- Do NOT bundle with feature surface changes (features 49-53 in
  training pipeline is a separate task)

## Dependencies and sequencing

B-2 blocks: v3 rebuild (563 situations)
B-2 does NOT block: v2.2 iteration (100-200 situations)
B-2 blocked on: nothing. Can start as soon as Phase B ships and
  there is free terminal capacity.

## Open questions for the owner

1. Is v2.2 definitely going to be an iteration on v2.1 (adding
   ~100-200 situations to the existing 348), or is it a full
   rebuild (563+)? The answer changes whether B-2 blocks v2.2.
   Default assumption: iteration, B-2 not blocking.

2. Which sampling option (A/B/C) does the owner prefer before we
   brief the ml-architect? Or should the ml-architect decide? Per
   Process Guide 1.4, "experts decide HOW" — default is
   ml-architect decides and presents with rationale.
