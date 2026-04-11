---
date: 2026-04-10
from: Logic team (investigation)
to: Future logic team (pickup after v1.3 ships)
re: Action history feature expansion — scoping investigation, PARKED
status: PARKED pending v1.3 KB ship + review findings
---

## Status

**Parked.** This is a scoping investigation only. No code changes.
No memory save. No training action. Do not pick this up in parallel
with the v1.3 KB review.

Pickup trigger: v1.3 KB ships AND a next training round is being
planned. At that point, route through ml-architect to address S1-S4
from the review before any feature code is written.

See `review/comms/REVIEW_ACTION_HISTORY_FEATURE_INVESTIGATION_2026-04-10.md`
for the review findings that gate pickup.

## Question that triggered this

Owner asked (2026-04-10): on the river facing a villain bet in a
3-way pot, can we back-track how many bets villain has made across
prior streets? Same for hero? Is it being done? Can it be done?

## Findings — what's currently tracked

### Villain side — partially tracked

Feature: `villain_aggression_count`
- Source: `river-rats-core/game_state_bridge.py:99-121`
- Definition: integer 0-3, counts the number of prior streets on
  which the primary villain took a bet or raise action.
- Computed by filtering `game.street_actions` to the primary
  villain's position, then counting streets where any action was
  `'bet'` or `'raise'`.

Related features:
- `villain_checked_back` — binary, 1 if villain checked on any
  prior street (loses temporal sequence).
- `villain_call_count` — integer, count of prior streets villain
  flat-called.
- `num_callers_to_bet` — current street only.
- `facing_raise` — derived from `num_raises_this_street > 0`,
  catches check-raises and re-raises.
- `is_3bet_pot` — binary, ≥2 bet/raise actions preflop.

### Hero side — effectively not tracked

Only `is_preflop_aggressor` exists (Feature 53, computed in
`feature_extractor.py:1647-1653`). Binary, 1 if hero opened preflop.

A grep of `*.py` across the repo for `hero_aggression`,
`hero_bet_count`, `_hero_aggression`, `hero_action_count` returned
zero matches. There is no postflop hero-line tracking in the
48-feature pipeline.

## Findings — three genuine limitations of the current feature

These are pre-existing limitations, not regressions. Fixing any of
them is a legitimate improvement; none are blockers for current
training.

1. **Street count, not action count.** Bet-then-raise on one street
   collapses to 1, not 2. Multi-raise streets lose information.
2. **Primary villain only.** In a 3-way pot, the bridge picks ONE
   villain (bettor, or deepest-stacked non-folded opponent). The
   *other* villain's prior-street action history is not in any
   feature. The model cannot distinguish "opponent A triple-barrel,
   opponent B called along" from "opponent A checked, opponent B is
   the aggressor now" when one of them is bettor on the current
   street.
3. **`villain_checked_back` is a single bit.** Cannot distinguish
   "checked flop, bet turn" from "checked flop, checked turn". No
   temporal sequence.

## Proposal (provisional, un-validated)

### Cheap + high-signal (tentative recommendation)

1. `hero_aggression_count` — symmetric to villain version, ~12
   lines in `game_state_bridge.py`. `game.street_actions` already
   contains hero's actions.
2. `hero_checked_count` — same code path, counts prior streets
   hero checked.
3. `any_villain_aggression_count` — aggregate (max over all
   non-folded opponents) to catch the 3-way second-villain blind
   spot without doubling feature surface area.

### Expensive + speculative (parked indefinitely)

4. Per-villain temporal sequence.
5. Action-level (not street-level) counts.
6. Bet-sizing history (requires extending `street_actions` entry
   format).

## Causal hypothesis (SPECULATIVE — must be verified before any build)

Three of the five true remaining failures from
`RESTART_PROMPT_V9_3WAY.md` look like passive-residue bugs:

- MW-17: under-calling (low equity draw)
- MW-25: residual passive (thin value bet)
- MW-40: residual passive (very thin value bet)
- MW-45: under-raising

**Hypothesis:** these could be partially explained by the model not
knowing hero's own prior line. A hero who has been passive for two
streets is in a different situation on street 3 than a hero who has
been aggressive, and the current feature set cannot tell them apart.

**Status:** unverified. The hypothesis must be checked against the
actual feature rows for MW-17/25/40/45 before any feature code is
written. If the hypothesis does not survive contact with the real
data, the feature expansion is unjustified.

This is the S1 gate from the review.

## Blockers and should-fixes from review

Source: `review/comms/REVIEW_ACTION_HISTORY_FEATURE_INVESTIGATION_2026-04-10.md` (to be filed)

- **[BLOCKER] B1** — Do not build in parallel with v1.3 KB review.
  Retraining on v1.2-labelled data while v1.3 is transitioning
  risks baking in the exact over-fold bias v1.3 removes. Build
  only after v1.3 ships.
- **[SHOULD_FIX] S1** — Verify MW-17/25/40/45 causal hypothesis
  against real feature rows before committing to the feature set.
- **[SHOULD_FIX] S2** — Leakage risk requires ml-architect
  assessment. Features derived from hero's prior actions are a
  natural place for label-via-action-sequence leakage.
- **[SHOULD_FIX] S3** — Retrofit feasibility on existing 608
  training situations is unknown. Confirm that stored situations
  preserve `street_actions` in a replayable form, or the "trivial
  code change" becomes "regenerate all 608 situations".
- **[SHOULD_FIX] S4** — `any_villain_aggression_count` attribution
  loss is not quantified. ml-architect opinion required on whether
  the aggregate is actually useful or just a
  correlated-but-lower-resolution shortcut.

## Pickup checklist (when v1.3 ships)

1. Read the filed review memo.
2. Spawn investigator to pull feature rows for MW-17/25/40/45 from
   the reference/test set and assess whether the passive-residue
   hypothesis survives. Produce one-page finding. **If hypothesis
   fails, close this document and do nothing.**
3. If hypothesis survives: spawn ml-architect to address S2
   (leakage risk), S3 (retrofit feasibility), S4 (aggregate
   justification).
4. If ml-architect approves: architect produces feature-addition
   blueprint per Protocol #4, programmer implements, tester writes
   failing tests first.
5. New training gate on feature-expanded model. Leakage check
   mandatory before gate.
6. Independent reviewer audit before any claim of improvement.
7. Only after model improvement is confirmed: save
   `memory/project_action_history_gap.md` encoding the lesson. Not
   before.

## Source citations (verified in this session)

- Villain aggression computation: `river-rats-core/game_state_bridge.py:99-121`
- `is_preflop_aggressor` definition: `river-rats-core/feature_extractor.py:1647-1653`
- Feature key definitions: `river-rats-core/feature_keys.py:53` (`VILLAIN_AGGRESSION_COUNT`)
- Hand context definitions: `river-rats-core/hand_context.py:120-126`
- Grep for hero aggression features: zero matches across `*.py` in repo

## Do NOT

- Do not touch `game_state_bridge.py` or `feature_extractor.py`.
- Do not start any training run.
- Do not save `project_action_history_gap.md` to memory until S1
  confirms the hypothesis.
- Do not treat this as parallel to the v1.3 KB work.
- Do not pick this up without reading the review memo first.
