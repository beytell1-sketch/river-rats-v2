---
date: 2026-04-18
from: Main terminal (reviewer/orchestrator)
to: Owner (decisions) + Teaching terminal (execution)
re: Teaching recentering — context-first architecture + flag window
status: PLANNING — owner walks through classification; teaching implements
---

# Teaching Recentering — Context, Range, Flags

## Why we're here

Teaching drifted twice from the original spec ("provide most
relevant context, range-based, no why"):

1. Phase 2 drift → intention_templates.py explained WHY →
   stripped in Path B (commits a-h, ~3,100 lines removed)
2. Pre-hint panel leaks (blocker directionality, implication
   clauses) → commit i still pending

Before we finalize commit i, recentring the whole output surface
is the right move. Otherwise we keep patching a layer that
wasn't architected around the original intent.

## Original intent — three principles to re-anchor on

1. **Provide most relevant CONTEXT** — not explanations
2. **Range-based thinking is central** — learner reasons about
   ranges vs ranges, not about individual hands vs individual
   hands
3. **Flag what's noteworthy, exclude what's obvious** — the
   new idea: separate flag window for triggered observations
   that demand attention, keeping primary context clean

## Inventory — current EnrichedTeachingOutput fields

Grouped and pre-classified as a DRAFT for owner to redirect.

### A. THE HAND (what hero has)

| Field | Draft class | Notes |
|---|---|---|
| `action` | CORE | GTO recommended action, mandatory |
| `hand_bucket` | **REMOVE?** | "air/medium_made/strong_made" — student sees cards+board; at L3 this is trivially derivable |
| `hero_position` | CONTEXT | Already visible at table; the prose is redundant unless it carries IP/OOP read |
| `draw_outs` | **FLAG?** | Number alone is fine in dashboard; prose "4 outs" may be trivial |
| `draw_type_desc` | **FLAG or REMOVE?** | "flush draw (9 outs)" — at L3, student counts suited cards. At L1-L2, non-trivial |
| `showdown_value_desc` | **REMOVE?** | "Hand has showdown value" — L3 student derives from (hand, board, street) |

**Owner question:** at L3, should the system REPEAT what the student can already see (cards+board), or ONLY surface what requires range reasoning? Gut: remove the hand-description prose at L3; keep it for L1-L2 when built later.

### B. RANGE (primary teaching — your emphasis)

| Field | Draft class | Notes |
|---|---|---|
| `range_position_desc` | **PRIMARY** | "BTN range (~44%) — hold hand at 50th percentile of range" — CORE of range-based thinking |
| `where_we_sit_pct` | **PRIMARY numeric** | Preflop percentile; already suppressed postflop (game builder must not show as standalone postflop — gated) |
| `villain_tp_pct` / `medium_made_pct` / `draw_pct` / `air_pct` | **PRIMARY** | Villain range composition — cannot be derived without range reasoning. Exactly the "range vs range" frame |
| `board_favour` | **PRIMARY numeric** | "Who does this board favour" — range-vs-range signal |
| `villain_actions_desc` | **CONTEXT** | What villain has done so far |

**Recommendation:** this block is the teaching surface. Keep all of it. Consider reordering to put range-composition front-and-center.

### C. BOARD + POSITION

| Field | Draft class | Notes |
|---|---|---|
| `board_texture_desc` | **FLAG when notable** | "wet/dry, suit texture" — often implicit from seeing the cards. FLAG when texture is non-obvious or extreme (monotone, paired, connected) |
| `position_desc` | **REMOVE?** | "IP means last to act" — student sees position at table. Implication may overlap with WHY territory |

### D. COMMITMENT + NOTABLE THRESHOLDS

| Field | Draft class | Notes |
|---|---|---|
| `commitment_desc` | **FLAG when SPR < 2** | Genuine attention-demanding signal; not obvious from raw pot math |
| `danger_score` | **FLAG when >0.5** (numeric) | Show number always; surface as flag when materially high |
| `blocker_desc` | **FLAG, observation-only phrasing** | Instead of "Hero's cards block X%" → "X% of villain's flush combos contain a card in hero's hand." NEUTRAL phrasing. Moves to flag window; only fires at meaningful threshold |

**This changes commit i:** instead of "delete blocker_desc entirely" → "move to flag window with neutral phrasing + threshold gate." Your call — I recommend this revision because blocker IS the kind of range-reasoning flag the new architecture wants.

### E. NUMERIC DASHBOARD

| Field | Class | Notes |
|---|---|---|
| `equity_pct` | NUMERIC | Always show |
| `pot_odds_pct` | NUMERIC | Show when facing bet |
| `spr` | NUMERIC | Always show |
| `board_favour` | NUMERIC | Always show (matches PRIMARY section visibility) |
| `danger_score` | NUMERIC | Always show |

Feature-attention PRIMARY visibility logic stays for highlighting which technicals are most relevant this hand.

### F. HOW-CLOSE

| Field | Class | Notes |
|---|---|---|
| `tightness` | CORE | TOSS_UP / CLOSE / SILENCE. Keep. |
| `draw_claim_suppressed` | AUDIT | False-draw guard audit flag. Debug/owner only, not student-visible |

### G. FORWARD PLAN

| Field | Draft class | Notes |
|---|---|---|
| `forward_plan_desc` | **AUDIT or FLAG** | "Street plan" — may re-introduce implicit WHY. Worth reviewing phrasing. Could be rephrased as observation ("Likely next-street decision point: river card completes the flush") but risks re-drift |
| `street_plan_tags` | internal | Tags → downstream; keep |

## Proposed architecture

### Primary window (what the student sees first)

1. **Range block** (top of surface):
   - Hero range composition + hero's position in that range
   - Villain range composition (TP / medium / draw / air %)
   - Board-vs-range signal

2. **Situation block**:
   - Villain action history
   - Numeric dashboard (equity / pot odds / SPR / board favour /
     danger)

3. **Decision block**:
   - Action + tightness

### Flag window (only fires when triggered)

Collapsed by default; expands when one or more flags trigger:

- **Commitment flag** (SPR < 2)
- **Danger flag** (danger_score > 0.5 or board_favour < −0.3)
- **Texture flag** (monotone, paired, connected-and-wet)
- **Blocker flag** (block% material + neutral phrasing)
- **Tightness flag** (redundant with tightness field —
  consolidate?)

Principle: flag window only shows what's notable. Quiet when
nothing notable triggers. Keeps primary window clean and
range-focused.

### Removed at L3 (deferred to L1/L2 when built)

- hand_bucket prose
- draw_type_desc prose (keep the draw_outs number in
  dashboard)
- showdown_value_desc prose
- position_desc prose

These come back for L1/L2 where perception/label teaching
matters.

## Process — your walk-through

Three decisions per field category:
1. **Primary / Flag / Remove / Defer-to-L1/L2?**
2. **Phrasing strict** (observation only) **or rewrite** the
   remaining ones?
3. **Flag thresholds** (when to trigger each)

I can walk through every row with you one by one, or you can
mark your verdicts on this doc directly and push back. Your
call.

## Blocker (commit i) — stands down pending this

The pending commit i (delete _blocker_desc) should NOT land
until this recentering is decided. If blocker moves to flag
window with neutral phrasing, deletion is wrong; we'd be
re-introducing it in another file. Teaching terminal: hold commit
i.

## Timeline

Recentering decision ~1 hour of your review time. Implementation
~1 day teaching work (refactor renderer to primary/flag split +
threshold tune + L3 hardening re-pass on new structure).

## Cross-stream awareness

- Game builder needs the new CONTENT API when it lands —
  primary window vs flag window is a UI-layer change, not just
  a schema change
- Logic side (v2.3.2 α+β triage) continues independent
- Owner's hand-log system already captures full state, so
  playtest findings against new architecture will be
  structurally capturable

Recommend we walk the table together. When you're ready, I can
do it row-by-row or take your marked-up version as the
directive.
