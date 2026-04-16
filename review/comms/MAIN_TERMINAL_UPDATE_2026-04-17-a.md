---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: Phase 3.5 spot-check — render the 5 suggested review hands as human-readable HTML
status: DIRECTIVE — do now, owner is waiting
---

# Main Terminal Update — 2026-04-17 (a)

Owner needs the 5 Phase 3.5 pilot review hands in
human-readable visual format — same approach as the solver
verification HTML exports (e.g.
`SOLVER_VERIFICATION_MW_MISSES_2026-04-15.html`).

Raw JSONL is not reviewable. Owner needs to see the hand
visually — cards, board, action history, features, panel
reasoning traces — at a glance.

## Task

Generate an HTML file for each of the 5 suggested review
hands from `PHASE_3_5_PILOT_REVIEW_2026-04-16.md §Owner
spot-check section`:

1. `UMBRELLA_067` — clean 4/4 override
2. `RAISE_VALUE_012` — negative control
3. `BP7_06` — §3-probe with principled 3/1 split
4. `MM_IP_TURN_033` — boundary with override-the-override
5. `PFR_CONT_025` — MW-27-style flop vcb=0 negative control

Source: `training-data/v23_pilot_labelled.jsonl`

## Format per hand

Each HTML should show (same visual shape as the solver
verification exports):

- **Header:** situation_id, street, hero position
- **Cards:** hero hole cards + board (use text card
  representations — e.g. `As Kd` / `Ts 6s 3d 8h`)
- **Action history:** preflop → current street, one line
- **Key features table:** the bias-signature features
  (facing_bet, num_opponents, villain_checked_back,
  villain_range_capped, worse_hand_pct, equity_vs_range,
  SPR, hero_range_percentile) + any other features the
  panels cited
- **Override clause fired:** YES / NO (from the
  `override_clause_fired` boolean)
- **Pass 1 panel traces:** all 4 panels, each with:
  - Action chosen
  - Confidence
  - `expert_reasoning` (full text)
  - `factor_conflicts`
  - `alternatives_considered`
  - `override_clause_fired`
- **Pass 2 review** (if triggered): reviewer action +
  reasoning + v3 citations
- **Final label:** aggregated action

## Deliverables

Option A (preferred): single combined HTML with all 5 hands
as sections, internal anchor links at the top.

Option B: 5 separate HTML files.

Either way, commit to
`review/phase3_5_spot_check/` and push.

Drop a link in a builder status file so owner can open it
directly from GitHub.

## Priority

Owner is waiting on this before confirming the Phase 3.5
gate. Do this now — Phase 4 launches on confirmation.
