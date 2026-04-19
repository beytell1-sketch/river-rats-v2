---
date: 2026-04-19
from: Main terminal (reviewer/orchestrator)
to: Teaching terminal
re: Recentering LOCKED — execute plan v2
status: DIRECTIVE — write plan v2, expert-review, implement in small commits
---

# Teaching Recentering — Final Directive

Owner approved the full recommendation. All classifications
locked below. Blocker slot stays as deferred placeholder gated
on v2.4 feature expansion (see directive-u).

## Architecture

**Primary window** (range-first, observation-only):

1. Range block
   - `range_position_desc` — hero's position in range on this board
   - `villain_tp_pct / medium_made_pct / draw_pct / air_pct` — villain range composition
   - `board_favour` — range-vs-range texture signal
   - `villain_actions_desc` — history

2. Numeric dashboard
   - `equity_pct / pot_odds_pct / spr / board_favour / danger_score`
   - Visibility gated by `feature_attention` PRIMARY flags
     (existing logic stays)

3. Decision block
   - `action`
   - `tightness` (TOSS_UP / CLOSE / SILENCE)

**Flag window** (collapsible; quiet unless triggered):

| Flag | Trigger | Observation text (neutral) |
|---|---|---|
| commitment | SPR < 2 | "At SPR X.Y, remaining stack ~Z into pot of P" |
| deep-stack | SPR > 10 | "At SPR X, multi-street room remains" |
| danger | danger_score ≥ 0.5 | "Board danger score: X — {N}% of draws complete on the next card" |
| monotone | is_monotone = 1 | "Monotone board — three suits of one kind" |
| paired | is_paired = 1 | "Paired board" |
| connected | connectivity_score ≥ 4 | "Connected board — four or more ranks within a straight window" |
| board-favour-hostile | board_favour < −0.3 | "Board favour: −0.X — texture favours villain's range" |
| blocker | (deferred) | PLACEHOLDER — L4/L5 two-flag design gated on v2.4 `nut_flush_block` / `draw_block_pct` / `nut_made_block_pct` features |

**Commitment + deep-stack stay separate** (different triggers,
different student insight). Tightness-close and
villain-aggression DROPPED (redundant with `tightness` field
and `villain_actions_desc` respectively).

**Audit-only fields** (not student-visible):

- `draw_claim_suppressed` (false-draw guard audit trail)
- `source_trace` (field-source map)

## Removals — L3 prose cuts

Delete at L3. Restore for L1/L2 perception level when those get
built:

- `hand_bucket` prose — student reads cards+board
- `hero_position` prose — visible at table
- `draw_type_desc` prose — student counts their suited/connected cards
- `showdown_value_desc` prose — student derives from hand+board+street
- `position_desc` prose — visible at table; implications drift toward WHY
- `forward_plan_desc` prose — risks smuggling WHY; delete per Option A

Numeric counterparts stay where they're useful:
- `draw_outs` number stays (dashboard)
- `hero_position` stays as a field (used by range_position_desc)

## Schema implication — `flags: List[FlagEntry]`

New dataclass member on `EnrichedTeachingOutput`:

```python
@dataclass
class FlagEntry:
    kind: str                    # one of the flag kinds above
    trigger_value: float         # the feature value that tripped
    observation_text: str        # the neutral observation
```

```python
flags: List[FlagEntry] = field(default_factory=list)
```

Empty list = flag window collapsed / hidden. Non-empty = render
in collapsible panel with each entry as a line.

Game adapter needs the new field; publish as CONTENT_API v4.0.

## Execution discipline — plan v2

Same as directive-i (Path B):

1. **Plan v2 doc** in `review/comms/TEACHING_PLAN_V2_2026-04-19.md`:
   - Exact files/functions to change
   - Field-by-field diff (what removes, what renames, what adds)
   - FlagEntry dataclass spec
   - Flag rendering order + threshold values
   - L3 removal list with call-site scan
   - CONTENT_API v4.0 schema diff
   - Migration path for game adapter
   - Rollback plan
2. **Expert-review the plan.** GTO reviewer + V3 compliance
   reviewer subagents BEFORE any code change. Both must PASS.
3. **Small reviewable commits.** Not one monolithic rewrite.
4. **Register new guard-leak category:** directional-framing
   words (block/protect/charge/extract/deny) per directive-s §3.
5. **L3 hardening re-pass** on new structure: guard-leak scan,
   10-hand sample across difficulty bands, adversarial suite
   for any new flag-rendering code.
6. **Sample check for residual causal prose** — 10 hands
   render, verify NO flag observation_text contains directional
   framing words or causal verbs.

## What does NOT change

- `range_position_desc` content and phrasing (primary teaching
  — keep as-is per Path B hardening)
- Numeric dashboard fields
- `tightness` signal mechanics (top-two-probability gap proxy)
- `draw_claim_suppressed` audit flag
- Situation describer order (range composition, equity, pot
  odds, SPR, board texture, position, commitment, blocker —
  for the SOURCE fields; render order in primary window is
  range-first per above)
- Path B false-draw guard (stays)

## What does NOT ship in this pass

- Blocker flag implementation (gated on v2.4 features per
  directive-u)
- L1/L2 prose restoration (those are separate phase-3 work)
- Forward-plan re-introduction (deleted; may revisit much later
  if a clean observation-only phrasing emerges)

## Cross-stream

- Game adapter: needs CONTENT_API v4.0 when teaching ships.
  Coordinate adapter update with teaching's schema release.
- Logic (v2.3.x): baseline is v2.3.1; game stays on v2.2 in
  production. Teaching schema ships independently.
- Owner's playtest logging: logs captured under the old schema
  will replay fine; new schema kicks in when game adapter
  swaps.

## Standing by for plan v2

Ping when plan v2 is written and expert-reviewed. I'll verify
plan before you start deletions / additions. Same "check the
blueprint before implementing" discipline as Path B.

Go.
