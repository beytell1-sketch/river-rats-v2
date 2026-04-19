---
date: 2026-04-19
from: Builder
to: Main terminal / Owner
re: v2.4 P1 — consolidated GTO-reviewer verdicts on all 3 blocker-feature plans
status: VERDICTS AGGREGATED — ONE scope change needs owner ack before revise pass
---

# v2.4 P1 — Consolidated GTO-Review Verdicts

Three GTO-reviewer subagents ran in parallel against the three plan
docs. All three returned **APPROVED_WITH_MODIFICATIONS**. Details +
modifications below, plus ONE scope change flagged for owner decision
before plan revision proceeds.

## Quick verdict table

| Plan | Feature | Verdict | Modifications | Rereview needed? |
|---|---|---|---|---|
| 1 | `nut_flush_block` (bool) | APPROVED_WITH_MODS | 4 small (M1–M4) | No |
| 2 | `draw_block_pct` (continuous) | APPROVED_WITH_MODS | **SPLIT into 2 features + bug fix + 5 Q answers** | **Owner ack needed on split** |
| 3 | `nut_made_block_pct` (continuous) | APPROVED_WITH_MODS | 4 refinements (M1–M4) + answers | No |

## Scope expansion flagged

**Plan 2's GTO reviewer recommends splitting `draw_block_pct` into
two features: `flush_draw_block_pct` and `straight_draw_block_pct`.**

Reviewer reasoning (verbatim):
> "SPLIT into `flush_draw_block_pct` and `straight_draw_block_pct`.
> Owner's scenario is flush-specific; combined metric creates
> cross-texture floor-ceiling artifacts."

If accepted, the new-feature count goes from **3 → 4**:

1. `nut_flush_block` (bool) — unchanged
2. ~~`draw_block_pct`~~ → `flush_draw_block_pct` + `straight_draw_block_pct` (both continuous, 0-1)
3. `nut_made_block_pct` (continuous) — unchanged

Feature vector total: 55 → 59 raw (+ 59 attn = 118 total).

**Builder recommendation:** accept the split. Reviewer's reasoning
is poker-sound — the owner-flagged scenario is specifically
flush-texture blocking; combining with straight-draw blocking
creates dilution on boards where only one class matters. But this
is a scope decision — awaiting owner ack before revising plan 2.

If owner prefers to KEEP combined, plan 2 proceeds with the other
mods (bug fix + Q answers) only; the split becomes a v2.5 item.

## Per-plan modification summary

### Plan 1 — `nut_flush_block` (REVISIONS READY)

**M1 (threshold split by street):**
- Flop: 2+ of suit on board (keep current)
- Turn: **tighten to 3+ of suit** (was 2+)
- River: **tighten to 3+ of suit** (was 2+)

Rationale: 2-tone turn/river is not a nut-blocker-drives-action
situation; over-triggers add noise.

**M2 (paired boards):**
- Do NOT code-gate on `is_paired`
- Downgrade paired-board activations via v3.2 prompt guidance
  (PRIMARY → SECONDARY) rather than at the feature layer

**M3 (hero made-flush exclusion):**
- Plan text says feature = 0 when hero has made flush; pseudocode
  missed it. Add explicit: `if len(hero_of_suit) >= 2 AND total_of_suit >= 5: return 0`.

**M4 (no K-of-suit companion):**
- Reject the proposed `near_nut_flush_block` for K-of-suit
- K/Q/J-of-suit blocking is covered by the continuous
  `draw_block_pct` (or the split variant if scope expands)

**I1 (backfill audit):**
- Before any retrain, report joint distribution of
  `nut_flush_block` vs `flush_draw_rank`. Specifically the
  defensive bucket `(flush_draw_rank == 0 AND nut_flush_block == 1)`
  must be ≥2% of training rows. If below, augment before training.

**I3 (flag — important for v2.4 sequencing):**
- P1 alone does NOT close the defensive-blocker ticket
  (`TICKET_BLOCKER_DIRECTION_DEFENSIVE_2026-04-18.md`).
- The ticket's densification case (hero non-nut blocker + defending)
  is P2 territory (`draw_block_pct`).
- **Implication:** the ticket cannot be marked complete until P1 +
  P2 + P3 all land + v3.2 prompt updates + retrain validates.

### Plan 2 — `draw_block_pct` (PENDING OWNER ACK ON SPLIT)

**BLOCKING (must fix before code):**

**Bug in pseudocode:** `bucket.combos` does not exist on
`HandBucket` in `range_decomposition.py`. Actual fields are
`category`, `subcategory`, `total_combos`, `beats_hero`,
`loses_to_hero`, `pct_of_range`. Combo iteration happens
internally in `decompose_range` and is aggregated away.

**Fix:** inline the combo iteration in `feature_extractor.py`
(mirror `decompose_range`'s inner loop). DO NOT modify
`range_decomposition.py`. Isolates the new feature.

**Q1 answer — SPLIT (pending owner ack):**
- `flush_draw_block_pct` — hero blocks villain's flush-draw combos
  (subcategories `nut_flush_draw`, `flush_draw`, + flush half of
  `combo_draw`)
- `straight_draw_block_pct` — hero blocks villain's straight-draw
  combos (subcategories `oesd`, `gutshot`, + straight half of
  `combo_draw`)
- Combo draws counted in both halves (each class that applies)

**Q2 answer — defer weight-by-outs to v2.5:**
Plan 2 ships unweighted (all draw combos count equally). If the
feature proves to carry signal, re-evaluate weighted version in
v2.5.

**Q3 answer — no suit/rank awareness needed for P1:**
Per-combo overlap check is already rank-aware enough
(e.g., `9s7s` combo is a different combo from `9h7h`).

**Q4 answer — do NOT expose `effective_draw_block` product:**
XGBoost learns the interaction via tree splits with
`villain_draw_pct`. Exposing the product inflates SHAP attribution
budget, which matters for v3 SHAP-based teaching ordering.

**Q5 answer — 0.0 (NOT NaN) when villain has no draw combos:**
NaN triggers XGBoost missing-value routing to a branch learned
from non-empty rows. Wrong distribution. 0.0 = "inapplicable"
is the correct null semantics.

**Gutshot note (for v2.5):**
KB §1.7 + DO NOT Rule 2 say gutshots don't semi-bluff 3-way.
Including them in the current `_DRAWS` set dilutes the signal.
Acceptable for P1 (matches `villain_draw_pct` scope) but
document for v2.5 refinement.

**Scope note — zero training signal until prompt updates:**
Feature will be ignored by panels until:
1. KB §1.9 (or new section) documents defensive blocker
   direction
2. v3.2 prompt mandates tagging the new feature in
   defensive-decision feature_attention
3. Training data is re-labelled with v3.2 prompt

Feature can SHIP earlier (additive; existing training won't break).
But no new training signal until the prompt loop closes. This is
the exact v2.3.2 failure mode (undocumented features = no panel
tagging = no training signal).

**Sequence recommendation:** ship feature → update KB → update
prompt → re-label subset → retrain. Don't retrain between feature
land and prompt update — no new signal available.

### Plan 3 — `nut_made_block_pct` (REVISIONS READY)

**M1 — CRITICAL carve-out:** Include `strong_flush` in the nut-made
class **only when A-of-suit is ON THE BOARD** (second-nut flush
case). Without this carve-out:
- `flush_block_pct` retirement is unachievable on textures like
  Ac·Ks·Ts where K-flush is effective nut
- The feature misses exactly the class `flush_block_pct` currently
  handles

**Implementation:** add `_has_ace_of_suit_on_board(board, suit)`
helper; if true, `strong_flush` combos (K-high flush) count as
nut-made.

**M2 — paired-board top-set handled by classifier routing:**
Existing `range_decomposition.py` routes paired-board "top set"
into `quads` / `full_house` subcategories automatically. No
special case needed; just confirm via unit test.

**M3 — nut_straight strictly highest-possible:**
Current plan is correct. `_is_nut_straight` in
`range_decomposition.py` already implements this.

**M4 — taxonomy-drift guard test:**
Add a test that asserts every string in `_NUT_MADE_SUBCATS`
(`straight_flush`, `quads`, `full_house`, `nut_flush`,
`nut_straight`, `top_set`, and post-M1 conditional `strong_flush`)
exists in `range_decomposition.SUBCATEGORY_ORDER`. Prevents silent
drift if taxonomy renames.

**Answers to 5 open questions:**
1. **Strict nut class + A-on-board second-nut carve-out.** Exclude
   top-two-pair (not stack-off 3-way per KB §1.2).
2. **Paired-board top-set:** handled by classifier routing to
   `quads`/`full_house` — no special case.
3. **Nut-straight strictly highest** (current plan correct).
4. **No explicit HU vs 3-way reweighting** — use raw fraction, let
   XGBoost discover interactions via `num_opponents` splits.
5. **Retirement test: A/B + monotone-texture sanity sweep (50-100
   hands on 3+ flush boards with non-Ace blocker).** Feature
   importance alone is INSUFFICIENT because correlated features
   split gain. If monotone sweep regresses even with low feature-
   importance on `flush_block_pct`, KEEP it.

## Three features form a covering triple (or four after split)

| Feature | Hero direction | Applies when |
|---|---|---|
| `nut_flush_block` | Aggressor positive (KB §1.7 canonical) | 2+ suit on flop / 3+ on turn-river |
| `flush_draw_block_pct` (split) | Defender negative (densification) | Flush-draw class in villain range |
| `straight_draw_block_pct` (split) | Defender negative (densification) | Straight-draw class in villain range |
| `nut_made_block_pct` | Defender positive (villain value blocked) | Villain range has nut-made combos |

## What needs to happen next

### 1. Owner decision on P2 split — BLOCKING

- Accept split → 4 new features, revise plan 2 doc, ship with split
- Reject split → 3 new features, plan 2 keeps combined metric, split
  becomes v2.5 item

### 2. Once split decision is made — revise plan docs

- Plan 1: apply M1–M4, add I1 backfill audit (no re-review per
  plan 1's reviewer)
- Plan 2: apply bug fix + Q answers + (if accepted) produce split
  version
- Plan 3: apply M1–M4 including the strong_flush carve-out (no
  re-review per plan 3's reviewer)

### 3. NO code / training still

Per directive-x: "Do NOT yet: start model training." Plans revise →
wait for owner approval on split + revised plans → then code
implementation per revised plans → then training.

## Artifacts this cycle

- `review/comms/GTO_REVIEW_V24_P1_NUT_FLUSH_BLOCK_2026-04-19.md`
- `review/comms/GTO_REVIEW_V24_P1_DRAW_BLOCK_PCT_2026-04-19.md`
- `review/comms/GTO_REVIEW_V24_P1_NUT_MADE_BLOCK_PCT_2026-04-19.md`
- This doc (consolidated verdict)

Standing by for owner on the P2 split decision.
