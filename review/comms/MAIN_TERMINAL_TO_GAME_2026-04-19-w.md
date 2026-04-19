---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Game builder
re: Game UI recentering — first cut scope (range bar + action-order), mockup-first
status: DIRECTIVE — mockup doc first, owner review, then build
---

# Game UI Recentering — First Cut

Owner approved the direction. Build game-flow improvements so
the felt carries glance-level information currently living in
coaching panels. Teaching and logic reworks continue
independently — your work is orthogonal and unblocked.

## Scope — first cut

**Build:**
1. **Villain range bar** under each villain seat
2. **Action-order badge** on each seat's current-street tag

**Defer to second cut (after first cut ships and playtests):**
- Pot-odds chip on felt next to to-call amount

**Defer to later / nice-to-have:**
- Per-seat stack visualization
- Street timeline at bottom of felt

## Villain range bar spec

### Data source — DO NOT recompute

Read these four fields directly from the teaching output per
villain:

- `villain_tp_pct` — top-pair-or-better
- `villain_medium_made_pct` — medium made
- `villain_draw_pct` — draw
- `villain_air_pct` — air

These are the **board-narrowed** range percentages (conditional
on action history on this board), which is what you want. Same
numbers the coaching panel renders. Single source of truth —
do NOT recompute at UI layer.

Note: the four fields are per-decision, not per-villain. If the
teaching output only carries hero-perspective ranges for ONE
villain (typically primary villain), the bar renders only under
that villain. For multiway spots where you want all villain
bars, confirm with teaching terminal whether CONTENT_API v4.0
plans multi-villain range breakdowns. For first cut: render
under the villain the data refers to; leave other villains
without a bar. Don't invent data.

### Visual spec — mockup 2-3 variants

**Mandatory elements:**
- 4 segments: TP+ (strongest visual weight), medium-made,
  draw, air
- Widths proportional to percentages (min 2-3px per non-zero
  segment for visibility)
- Same color palette as existing coaching panel (visual
  consistency: student learns one color mapping, not two)
- Positioned at the villain seat, close enough to the
  avatar/chip-stack that the visual association is immediate
- Tap/hover reveals exact percentages (30% / 10% / 20% / 40%)

**Mockup variants to draft:**

| Variant | Shape | Notes |
|---|---|---|
| A | Horizontal stacked bar (60-80px × 4-6px) under villain | Most compact; reads L-to-R |
| B | Vertical stacked bar (4-6px × 40-60px) beside villain | Vertical space; less horizontal crowding |
| C | Segmented ring around avatar | Most visually integrated; may be cramped at small sizes |

Draft all three; owner picks.

**Out of scope for first cut:**
- Per-villain range bars in multiway if teaching only emits
  primary-villain range (see data-source note above)
- Animation transitions (ship static first; add
  transitions if playtest shows they help)
- Hover tooltips beyond "exact percentages" (no didactic text
  — stay out of teaching territory)

## Action-order badge spec

### Trigger

For each seat that has acted or is currently to act on the
current street, render a small badge indicating their action
order on THIS street.

Example 3-way flop scenario (hero BTN, SB and BB in):
- SB acts 1st → badge "1"
- BB acts 2nd → badge "2"
- BTN (hero) acts 3rd → badge "3"

Badge appears on the seat's current-street action tag (the
thing that shows CHECK / BET / CALL / FOLD / waiting).

### Data source

`game_state.action_history` filtered to current street. Count
each unique position's first action on this street — that's
their action-order index.

If villain has already acted, badge stays attached to their
action tag. If hero is yet to act, badge on hero's "your turn"
indicator shows "N" where N is hero's action-order index.

### Visual spec — mockup 2-3 variants

| Variant | Placement | Notes |
|---|---|---|
| A | Small circle badge left of action tag | Classic badge pattern; unambiguous |
| B | Number prefix in action tag ("3. CHECK") | Most compact; integrates with existing UI |
| C | Small number above seat avatar | Separates order from current action; may duplicate badge-vs-tag space |

Draft all three; owner picks.

### Out of scope for first cut

- Showing PRIOR-street action orders (only current street)
- Animating the badge increment when new player acts (static;
  add animation later if needed)

## Mockup-first workflow

**Step 1 — Mockup doc** at `~/river-rats-game/review/comms/
GAME_UI_RECENTERING_MOCKUP_2026-04-19.md`:

- 3 range-bar variants with exact pixel dimensions + ASCII or
  screenshot mockup per variant
- 3 action-order badge variants with placement + mockup per
  variant
- Color palette reference (match existing coaching panel —
  include hex values so there's no ambiguity)
- Positioning coordinates relative to seat avatar + chip
  stack + action tag
- Tap/hover interaction sketch for the range bar expand

**Step 2 — Owner reviews** mockup doc, picks one variant of
each, provides any redirect. Don't start coding until owner
confirms.

**Step 3 — Small commits.** Build the chosen variants. One
commit per element (range bar, action-order badge), separated
from any other UI work.

**Step 4 — Pre-ship verification.** Before merging to master:
- Test on a real bundle (not mock) — range bar reads correct
  percentages against teaching output
- Check action-order badge on HU, 3-way, and 4-way scenarios
- Tap/hover interaction doesn't break on mobile if applicable
- Color contrast passes standard accessibility thresholds
  (ratios >= 4.5:1 for text overlays)

**Step 5 — Playtest.** Owner plays a real session with the new
UI. Feedback goes to hand-log system (logic/teaching feedback
boxes catch any misreads).

## Orchestration discipline

**Do NOT touch coaching panel content in this pass.** Panel
becomes reference-level reading material instead of primary
glance surface, but the panel's rendering stays unchanged.
Teaching's recentering directive owns the panel content; game
owns the felt.

**Do NOT add teaching prose at the seat.** The range bar is
observation-only (visual, no text). The badge is observation-
only (just a number). No didactic labels like "villain range
weighted to..." — that's teaching layer, not game layer.

**Do NOT couple this to v2.3.1/v2.4 model swap or CONTENT_API
v4.0 rollout.** All four range-bar data fields are stable
across those changes. First-cut UI ships on v2.2 production
bundles. When v2.3.x and v4.0 ship, the UI is already
range-first.

## What this UI change is NOT

- Not a teaching rewrite (teaching owns panel text)
- Not a coaching panel replacement (panel stays as reference)
- Not a multiview overhaul (this is additive — adds seat
  visuals, removes nothing yet)
- Not a schema change (reads existing fields)

## Timeline

Mockup doc: 1-2 hours.
Owner review + pick: owner-paced.
Build + verify: 3-4 hours per element after variant locked.

First-cut ship: likely 1-2 working days total assuming owner
picks variants in one round.

## What I need from you next

Mockup doc at the path above, containing 3 variants per element
plus the color / placement / interaction notes. Ping when
pushed; I'll verify it's reviewable and hand off to owner.

Go.
