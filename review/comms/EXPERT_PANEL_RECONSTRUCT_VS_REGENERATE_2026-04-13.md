---
date: 2026-04-13
from: Builder team (architecture expert + ML architect + GTO expert)
to: Owner (Rupert)
re: Expert panel assessment — reconstruct existing 351 vs regenerate fresh
status: FOR OWNER REVIEW — consolidated findings and recommendation
---

# Expert Panel: Reconstruct vs Regenerate

Three experts assessed the owner's proposal to keep the same
cards/board/positions and reconstruct action sequences. Their
findings converge on a hybrid recommendation.

---

## 1. Architecture Expert — Sequence Reconstruction

### Feasibility

**Factory 151 (mostly 2-way):**
- 6 of 9 unique feature-counter combinations map to exactly 1
  valid sequence → deterministic reconstruction (119 situations)
- 2 combos (villain_aggression_count=2) have 2-3 plausible
  sequences → ambiguous (27 situations)
- 1 combo (facing_bet=0, agg_count=1) appears to be a cross-street
  counter bleed → suspect (5 situations)

**Self-play 200 (3-way):**
- Hero-side sequence recoverable from `prior_actions`
- Villain actions constrainable from feature counters but not
  deterministic in all cases for 3-way pots

### Bet amounts
Inferrable from pot_size and to_call for facing-bet situations.
Multi-action sequences (agg_count≥2) lose intermediate amounts.
Placeholder amounts work for structural validation.

### Risk if wrong
A wrong reconstructed sequence would corrupt the labeller's
reasoning context (the agent reads the action string) but NOT the
numerical features already computed. Risk is mislabelled decisions.

### Verdict
Reconstruction is **partially feasible** — ~119/151 factory at high
confidence, the rest at lower confidence. Self-play is harder.

---

## 2. ML Architect — Data Integrity

### Feature corruption blast radius
**10-14 of 48 features** (20-30%) depend directly or indirectly on
action sequences. Not just the 6 obvious counters — also pot_odds,
effective SPR at decision point, and positional features relative
to aggressor. These are typically top-5 importance features in
poker XGBoost models. **Systematic directional corruption**, not
random noise.

### NULL features are the deciding factor
`flush_block_pct`, `flush_draw_rank`, `hero_range_percentile` are
NULL across ALL 351 rows. XGBoost learned to route these to
arbitrary default directions — that routing is garbage. **You need
a full re-extraction pass regardless.** Once you're re-extracting
all 351 rows anyway, the incremental cost of regenerating fresh
situations is small.

### Label comparison value
**Moderately useful, but as a spot-audit tool, not a bias
diagnostic.** The comparison identifies where protocols disagree
(estimated ~15% of situations). Those disagreements are where
solver verification time should go. It does NOT confirm model
bias — the current model's biases are artifacts of feature
corruption, not just labelling protocol.

### Diversity vs comparability at 351 rows
**Diversity wins.** With ~70 rows per class average, the model
needs coverage across board texture × position × stack depth ×
action history. Re-using the same 351 preserves nothing useful
when you're re-extracting and relabelling anyway.

### Verdict
**Regenerate fresh.** The path of least structural debt. If the
owner wants old-vs-new comparison, apply both protocols to a
shared 40-situation hold-out set (separate from training).

---

## 3. GTO Expert — Poker Perspective

### Where labels will change (most → least)
1. **Drawing hands facing a bet** — bucket-first surfaces RAISE
   as a candidate from the start. Sequential trees had NULL
   features blocking the semi-bluff gate. Expect CALL→RAISE flips
   on nut draws with blockers.
2. **Medium made hands in marginal spots** — sequential defaulted
   to CALL. Bucket-first forces explicit FOLD consideration when
   action history narrows ranges above the hand.
3. **Strong made hands on dangerous boards** — protection logic
   (bet to deny equity) requires reading hand+board interaction,
   not just exceeding an equity threshold.

### Where labels stay the same
- Monsters (equity >80%, sets/straights/flushes) — both approaches
  converge on value action
- Clear air facing reasonable bets — FOLD regardless of reasoning
- Nut hands with obvious value targets

### Bucket-first risks
- **Weak made hands on river** — "weak_made" is a broad bucket.
  Bottom pair on dry board vs bottom pair on wet board 3-way are
  very different strategic situations.
- **Sharp equity thresholds** — 0.54 equity = "medium_made",
  0.56 = "strong_made". The bucket boundary concentrates all
  threshold sensitivity into one step.

### The 151 factory 2-way situations
**Not useful for 3-way training.** Heads-up poker has no sandwich
pressure. 2-way labels ignore the third player entirely — the
defining feature of 3-way spots. Mixing them into 3-way training
data risks actively misleading the model on exactly the spots
where 3-way differs most from 2-way.

---

## 4. Consolidated Recommendation

The three experts agree on the core conclusion but differ on
approach:

| Expert | Recommendation |
|--------|---------------|
| Architecture | Hybrid — reconstruct high-confidence, flag ambiguous |
| ML Architect | Regenerate fresh — re-extraction needed regardless |
| GTO Expert | Regenerate 3-way fresh, discard 2-way factory entirely |

### Builder team's synthesis

**Option H (Hybrid):** Keep the owner's comparison ability while
addressing all three experts' concerns.

**Phase 1A: Triage the 351 situations**

| Category | Count | Action |
|----------|-------|--------|
| Factory 2-way (num_opponents=1) | 9 | **DISCARD** — not useful for 3-way oracle |
| Factory 2-way (num_opponents=2, BUT only 2 positions) | 142 | **DISCARD** — heads-up spots per GTO expert finding |
| Self-play 3-way | 200 | **RECONSTRUCT** — hero cards + board + positions preserved. Sequence reconstructed from prior_actions + counters. Validated by tool. |

This gives us ~200 reconstructable 3-way situations.

**Phase 1B: Reconstruct 200 self-play sequences**

Build a reconstruction tool that:
1. Takes hero_position, villain_positions, street,
   prior_actions, and all feature counters
2. Enumerates all valid action sequences consistent with
   the counter values
3. Validates each candidate through hand_sequence_validator
4. Tags each situation: CERTAIN (1 valid sequence),
   AMBIGUOUS (2+ valid), CORRUPT (0 valid)

Expected distribution (architect's estimate):
- CERTAIN: ~140-160
- AMBIGUOUS: ~30-40
- CORRUPT: ~10-20

**Phase 1C: Generate ~200-270 NEW 3-way situations**

To replace the discarded 151 factory 2-way + any CORRUPT
situations + add diversity (BP7 RAISE situations, BET/CHECK
factory from the original v2.2 plan). All through hardened
pipeline with mandatory action_string and full 48-feature
extraction.

**Phase 1D: Re-extract features for reconstructed situations**

Run the feature extractor on the ~200 reconstructed situations
using the validated action string. This populates the NULL
features and verifies the existing feature values match.

If re-extracted features differ significantly from stored
features (beyond rounding) → the original sequence was likely
wrong. Flag and move to CORRUPT.

**Phase 2: Relabel everything bucket-first**

~400-470 total situations (200 reconstructed + 200-270 new).
All labelled with bucket-first protocol. For the 200
reconstructed situations: compare old label vs new label.

**Phase 2 comparison matrix (for owner review):**

| Old label | New label | Same? | Count | Interpretation |
|-----------|-----------|-------|-------|---------------|
| CALL | CALL | Yes | ~X | Agreement — high confidence |
| CALL | RAISE | No | ~Y | Sequential missed a raise (expected for draws+blockers) |
| CALL | FOLD | No | ~Z | Sequential passive bias masked a fold |
| CHECK | BET | No | ~W | Sequential under-betting |
| Any | Any | — | — | Bucket-first may over-correct — flag for solver check |

**Phase 3: Train + evaluate** (unchanged from full rebuild plan)

### Why this hybrid works

1. **Owner gets the comparison** — 200 reconstructed situations
   with old vs new labels. Safety net against bucket-first
   over-correction.
2. **ML architect's concerns addressed** — full re-extraction
   populates NULL features. Feature verification catches corrupt
   sequences. Fresh situations add diversity.
3. **GTO expert's 2-way concern addressed** — all 151 factory
   2-way situations discarded. Training is pure 3-way.
4. **Architecture risk managed** — reconstruction confidence
   tagged per situation. Only CERTAIN and AMBIGUOUS enter
   training. CORRUPT situations replaced with new ones.

### What this changes from the full rebuild plan

| Full rebuild plan | Hybrid plan |
|-------------------|-------------|
| Discard all 351, regenerate from scratch | Keep 200 self-play 3-way, reconstruct sequences |
| No old-vs-new comparison | Comparison on 200 situations |
| ~370-470 all-new situations | ~200 reconstructed + ~200-270 new |
| ~80 agents | ~85 agents (adds reconstruction + re-extraction) |
| ~6 sessions | ~6-7 sessions |

### Resource estimate

| Phase | Agents | Notes |
|-------|--------|-------|
| Phase 0: Pipeline hardening | 2 | Unchanged |
| Phase 1A: Triage | 1 programmer | Automated — just counting |
| Phase 1B: Reconstruction tool + run | 1 architect + 1 programmer | New tool + batch run |
| Phase 1C: New situation generation | 1 GTO expert + 1 ML architect + 1 programmer | Design + generate |
| Phase 1D: Re-extraction + feature verify | 1 programmer | Batch job |
| Phase 2: Labelling | ~45 GTO experts + ~23 reviewers | Parallel |
| Phase 3: Train + evaluate | 3 | Unchanged |
| **Total** | **~85 agents + 5 owner gates** | |

---

**For owner: Does Option H (hybrid) make sense? The key
trade-off is 5 extra agents and 1 extra session for the
comparison safety net and preservation of 200 proven 3-way
poker scenarios.**
