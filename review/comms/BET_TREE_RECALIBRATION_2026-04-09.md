# BET Tree Recalibration — Threshold Fixes
**Author:** GTO Expert
**Date:** 9 April 2026
**Status:** AWAITING BUILDER APPLICATION + INDEPENDENT VERIFICATION
**Applies to:** BET_DECISION_TREE_V1.md — Steps 3, 4, 5, 6

---

## Why This Document Exists

The deterministic labelling script found that Steps 3-6 of the BET tree
never fire. Root cause: two features were used with thresholds calibrated
against assumed encoding ranges that do not match actual feature values in
the data. This document specifies exact replacement thresholds with evidence
from the actual BET-situation distribution (n=146).

This is NOT a rewrite of the tree. It is a precision recalibration. The
poker logic, step structure, and GTO reasoning in the tree are all
unchanged. Only the numeric thresholds on the two broken features are
updated.

---

## Fix 1: connectivity_score — Rescale from 0.0-1.0 to 0-10 Integer

### The problem

The tree was written assuming `connectivity_score` is a 0.0-1.0 float.
The actual feature is an 0-10 integer. Every threshold in the tree that
references `connectivity_score` uses values like 0.30, 0.55, 0.65, 0.70,
0.25 — all below the feature's minimum observed value of 2. No condition
gated on `connectivity_score` can ever fire.

### Actual distribution (BET situations, n=146)

```
min=2   p25=2   median=2   p75=5   p90=7   max=8
```

The distribution is heavily skewed toward dry boards (p50 = 2). This
makes sense for BET situations where the PFA c-bets or IP hero bets
more often on dry boards — this is selection bias working in the expected
direction.

### Tier mapping — conceptual intent preserved, scale corrected

The four tiers in Step 3A's texture determination logic correspond to
four poker board types. The original 0.0-1.0 thresholds encoded those
types. The integer equivalents below preserve the same conceptual
boundaries.

**Tier 1 — Very dry / disconnected:**
- Old threshold: `connectivity_score <= 0.30`
- New threshold: `connectivity_score <= 3`
- Evidence: p25 = 2, median = 2. The bottom quartile of BET situations
  sits at connectivity 2-3. This captures the A-high rainbow boards,
  K-high rainbow boards with no flush draw, and low disconnected boards
  (e.g., A72r) that constitute the core "dry board" poker concept. The
  threshold at 3 captures approximately the bottom 30-40% of situations
  by connectivity — comparable to the original <= 0.30 intent.
- Expected impact: Step 3A Tier 1 now fires on the boards it was designed
  for. Boards like A72r, K83r, A94r will pass the Tier 1 gate. Previously
  zero Tier 1 situations were reachable. BET labels will be produced for
  PFA hands holding top pair on these boards.

**Tier 2 — Moderately connected:**
- Old threshold: `connectivity_score <= 0.55`
- New threshold: `connectivity_score <= 5`
- Evidence: p75 = 5. A threshold of 5 captures approximately the bottom
  75% of situations by connectivity. The intent of Tier 2 was "Q/J-high
  boards with mild draw potential but not a full connected runout." An
  integer score of 4-5 corresponds to boards with one connecting gap
  (e.g., QT7, J84) — correctly moderate.
- Expected impact: Step 3A Tier 2 captures a meaningful middle range of
  boards. PFA with TPGK (hand_category >= 7) on moderately connected boards
  will now generate BET labels. This is the largest new label volume since
  Tier 2 spans p30-p75 of situations.

**Tier 3 — Connected:**
- Old threshold: `connectivity_score <= 0.70`
- New threshold: `connectivity_score <= 7`
- Evidence: p90 = 7. A threshold of 7 captures approximately the bottom
  90% of situations. This corresponds to boards with multiple connectors
  and draw potential (e.g., T87, 986, J98). The intent was "moderate danger
  but not fully wet." An integer of 6-7 correctly represents this.
- Expected impact: Step 3A Tier 3 fires for the 75th-90th connectivity
  percentile. These situations require hand_category >= 10 (two pair+) for
  a BET label — this is the correct conservative gate for connected boards.
  Previously, no Tier 3 situations fired. Now approximately 15% of BET
  situations will reach this tier.

**Tier 4 — Very connected / monotone (Step 3A does not fire):**
- Old threshold: `connectivity_score > 0.70` (implied)
- New threshold: `connectivity_score > 7` (i.e., connectivity_score == 8)
- Evidence: max = 8, p90 = 7. Only the top ~10% of situations have
  connectivity 8. These are the most connected boards — think 9T8 with
  flush draw, or 765 two-tone. Step 3A correctly does not fire here.
  The tree routes to Default CHECK (Step 7) or Step 2 (monster protection).

### Step 6 — OOP Value Exception connectivity gate

**Old threshold:** `connectivity_score <= 0.25`
**New threshold:** `connectivity_score <= 3`

The Step 6 OOP value bet requires a fully disconnected board (tighter than
even Tier 1 in Step 3A, since OOP standards are stricter). A threshold of
3 matches the Tier 1 dry-board concept and aligns with the OOP exception's
intent: OOP value only on the driest boards. The old threshold of 0.25 was
similar in intent to the old Tier 1 boundary of 0.30 — so the rescaling
here mirrors Tier 1.

---

## Fix 2: board_favour — Replace >= 0.20 Gate

### The problem

Steps 3 and 4 require `board_favour >= 0.20`. The actual maximum value
of `board_favour` in the full dataset is 0.171. For PFA situations
specifically (the only situations Steps 3 and 4 are relevant to),
`board_favour` clusters at only two distinct values: 0.003 and 0.111.
The 0.20 gate is structurally unreachable. Steps 3 and 4 can never fire
regardless of all other conditions.

### Actual distribution

```
Full BET sample (n=146):
board_favour: min=-0.232  p10=-0.184  p25=0.003  median=0.090
              p75=0.139   p90=0.144   max=0.171

PFA only (n=25):
board_favour: min=0.003  p25=0.003  median=0.003
              p75=0.111  max=0.111
```

The PFA distribution reveals a data coverage issue: only 2 distinct values
exist across 25 PFA situations. This is flagged separately below and does
NOT alter the threshold decision — the threshold must work with the data
that exists.

### Decision: Replace board_favour gate with high_card_rank

Option A (lower threshold to 0.08-0.10) was evaluated and rejected for
PFA situations. The PFA `board_favour` distribution clusters at 0.003 and
0.111 — a threshold anywhere between 0.004 and 0.110 would produce a
binary split that captures either 0% or ~32% of PFA situations (those at
0.111), with nothing in between. This is a degenerate threshold — minor
changes to the cutoff produce dramatic swings in coverage. The feature
does not have sufficient granularity to serve as a reliable gate for PFA
situations in this dataset.

Option B (replace with `high_card_rank`) is the correct choice. Here is
the poker reasoning:

The original intent of `board_favour >= 0.20` was to test "does this
board hit PFA's preflop raising range harder than villain's calling range?"
The research finding this encodes is that PFA has an equity advantage on
high-card boards (A-high, K-high, Q-high) because their raising range is
AA-TT, AK-AJ, and suited broadways — these hands contain more A, K, Q
combinations than villain's calling range. A high-card board improves
PFA's range more than villain's.

`high_card_rank` measures exactly this: the rank of the highest card on
board. An Ace-high board (high_card_rank = 14) strongly favors PFA's
range. A Queen-high board (high_card_rank = 12) is the GTO research
boundary — research consistently identifies Q+ as the threshold for
"range advantage board" from the preflop aggressor's seat.

`high_card_rank >= 12` is already used in Step 3A Gate 3A-1 as a
softener ("Queen or higher top card forgives moderate connectivity").
Promoting it to the primary gate in Steps 3 and 4 is consistent with
the tree's existing logic.

### Actual high_card_rank distribution (BET situations)

```
min=9   p25=10   median=12   p75=13   p90=14   max=14
```

Median is exactly 12 (Queen). The p25 = 10 (Ten). A threshold of >= 12
captures the top 50% of BET situations by top-card rank — approximately
the boards where PFA range advantage is real. This is well-calibrated:
a 50% pass rate on the board-favour gate is reasonable because we need
other conditions (is_preflop_aggressor, is_made_hand, hand_category) to
do the additional filtering.

### Specific threshold changes

**Step 3 — PFA Value C-Bet (primary condition):**
- Old: `board_favour >= 0.20`
- New: `high_card_rank >= 12`
- Evidence: high_card_rank median = 12. This gate passes when the board's
  top card is Q or higher, encoding "PFA range advantage" as a proxy.
- Expected impact: Steps 3A and 3B now become reachable. Approximately
  50% of BET situations pass this gate. The remaining conditions (PFA
  status, made hand, hand_category, position) then filter down to the
  correct BET frequency.

**Step 3B — OOP PFA Value Bet (stricter condition):**
- Old: two thresholds — `board_favour >= 0.20` (primary) and
  `board_favour >= 0.35` (the stricter OOP carve-out requirement)
- New: Replace BOTH with `high_card_rank >= 13` for the OOP carve-out
- Evidence: high_card_rank p75 = 13. A threshold of >= 13 (K or A high)
  captures only the top 25% of boards by top-card rank. This preserves
  the intended tighter OOP standard: OOP value bets only on the boards
  most strongly favoring PFA's range. The old `board_favour >= 0.35`
  was meant to be approximately 75% stricter than the IP threshold;
  `high_card_rank >= 13` (top 25%) versus `high_card_rank >= 12`
  (top 50%) achieves a comparable relative tightening.
- Expected impact: OOP PFA value bets are restricted to K-high and A-high
  boards only. This matches the OOP c-bet research: OOP PFA fires most
  often on A/K-high boards where their range advantage is largest.

**Step 4 — PFA Bluff C-Bet (primary condition):**
- Old: `board_favour >= 0.20` (range credibility condition)
- New: `high_card_rank >= 12`
- Evidence: Same reasoning as Step 3. The bluff semi-bet uses board_favour
  for range credibility — "even though this hand missed, the overall PFA
  range has high-card advantage on this board, making a bet credible."
  `high_card_rank >= 12` directly measures this.
- Expected impact: Step 4 semi-bluff conditions (4A-4D) become reachable
  for PFA hands on Q+ high boards. The equity sub-conditions (draw_outs,
  flush_draw_rank) remain unchanged and provide the actual selectivity.

---

## Summary Table

| Location | Feature | Old Threshold | New Threshold | Evidence |
|----------|---------|--------------|--------------|---------|
| Step 3A Tier 1 | connectivity_score | <= 0.30 | <= 3 | p25=2, median=2; bottom ~35% of situations |
| Step 3A Tier 2 | connectivity_score | <= 0.55 | <= 5 | p75=5; bottom ~75% of situations |
| Step 3A Tier 3 | connectivity_score | <= 0.70 | <= 7 | p90=7; bottom ~90% of situations |
| Step 3A Tier 4 | connectivity_score | > 0.70 | > 7 | max=8; top ~10% of situations |
| Step 3A Gate 3A-1 | connectivity_score | <= 0.65 | <= 6 | falls between p75=5 and p90=7; moderate-connected boards |
| Step 6 | connectivity_score | <= 0.25 | <= 3 | dry-board OOP exception; matches Tier 1 intent |
| Step 3 primary | board_favour | >= 0.20 | high_card_rank >= 12 | hcr median=12; Q+ boards favor PFA range |
| Step 3B OOP strict | board_favour | >= 0.35 | high_card_rank >= 13 | hcr p75=13; K/A-high only for OOP exception |
| Step 4 primary | board_favour | >= 0.20 | high_card_rank >= 12 | same as Step 3 — range credibility proxy |

---

## Note on Step 3A Gate 3A-1

Gate 3A-1 currently reads:
`connectivity_score <= 0.65` OR `high_card_rank >= 12`

The `connectivity_score` side of this OR must also be rescaled. The new
reading should be:
`connectivity_score <= 6` OR `high_card_rank >= 12`

This is included in the summary table above. The `high_card_rank >= 12`
side of the OR is unchanged — it was already using the correct scale and
correct threshold.

---

## Feature Reference Table Updates

The Feature Reference Table in the tree currently documents:

| connectivity_score | 0.0-1.0 | Tier determination in Step 3A; Step 6 gate |
| board_favour | Negative = villain favoured; positive = PFA favoured | Primary texture gate for Steps 3, 4 |

These entries must be updated when the builder applies these thresholds:

| connectivity_score | 0-10 integer (observed range: 2-8 in BET situations) | Tier determination in Step 3A; Step 6 gate |
| board_favour | [DEMOTED] No longer used as a primary gate. Retained in preamble feature list for context. Steps 3 and 4 use high_card_rank >= 12 as the range-advantage proxy. |
| high_card_rank | 2-14 (card rank of highest board card) | [PROMOTED] Primary range-advantage gate in Steps 3 and 4. Tier determination in Step 3A (existing). OOP threshold >= 13. |

---

## Data Coverage Flag: PFA board_favour Degeneracy

This is flagged for the owner and factory design team. It does NOT block
the recalibration.

In the PFA BET situations (n=25), `board_favour` takes only two distinct
values: 0.003 and 0.111. This means the feature is not being computed
with sufficient resolution to serve as a discriminating threshold for PFA
c-bet situations. The factory was not designed with PFA c-bet scenarios
as a primary use case, and the range composition machinery used to compute
`villain_top_pair_plus_pct` (which feeds `board_favour`) may not be
producing realistic villain ranges for these spots.

The consequence of replacing `board_favour` with `high_card_rank` in
this calibration is sound even if the factory is later updated. `high_card_rank`
is a directly observed board property — it cannot have degeneracy problems.
`board_favour` would need a factory redesign to be reliable for PFA c-bet
situations, and that is a separate workstream.

The owner should decide whether to:
- Accept `high_card_rank >= 12` as the permanent proxy (simple, reliable)
- Invest in factory redesign to produce better villain range estimates in
  PFA situations (higher accuracy potential, significant build cost)

This recalibration is valid under either decision. The threshold changes
here do not depend on fixing the factory.

---

## Expected BET Rate Impact

Before recalibration: ~1.6% BET rate (Steps 3-6 never fire; only Step 2
monster-protection bets produce BET labels).

After recalibration, rough estimate:
- Step 2 (unchanged): continues to fire on monsters with high danger_score
- Step 3A: now fires for PFA + made hand + high_card_rank >= 12 + connectivity
  in tier range. Approximately 25/146 PFA situations * rough pass rate through
  remaining conditions. Conservative estimate: 4-8% of total situations.
- Step 3B: OOP carve-out, very strict. Marginal additional volume.
- Step 4: PFA + no made hand + draw equity sub-conditions. Adds semi-bluff
  labels. Moderate volume.
- Steps 5-6: unchanged logic, connectivity rescaling means Step 6 can now
  fire. Small additional volume.

Expected total BET rate post-recalibration: 9-15%. This aligns with the
research finding that PFA bets approximately 43% of the time in 3-way
pots, applied to the subset of situations in the labelling dataset where
BET is actually correct.

The 43% figure is the aggregate PFA frequency. The labelling dataset
contains many situations where CHECK is correct (OOP hands, non-PFA hands,
dangerous boards) — a 9-15% BET rate on the full dataset is consistent
with a 35-50% BET rate among the situations where BET conditions are met.

---

*Applies to: BET_DECISION_TREE_V1.md*
*Output this calibration to: review/BET_DECISION_TREE_V1.md (builder applies changes)*
*Then: independent reviewer verifies thresholds fire correctly on spot-check hands*
*Then: deterministic script re-runs*
