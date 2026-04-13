---
date: 2026-04-13
from: GTO Expert
to: Owner + Builder team
re: Phase 3A enriched output — revised assessment after clarifications
status: REVISED EXPERT FINDING — supersedes EXPERT_GTO_ENRICHED_OUTPUT_2026-04-13.md
---

# GTO Expert Revised Assessment: Enriched Labelling Output

## Q1 — Does "tags not free text" resolve the street plan defer?

Yes, substantially. My objection was that free text would expand to fill
reasoning space. A constrained tag vocabulary eliminates that failure mode.
An agent cannot write an essay if the only valid output is one of five tags.

Residual concern: the tag must capture the CONDITIONAL plan, not just the
current action. `barrel_value` on its own is not a plan — it is a restatement
of the bet. The plan field needs a two-part structure: current-action tag +
turn-trigger tag. Example: `barrel_value | check_evaluate_on_completing_draw`.
A single tag collapses to the same problem as `strategic_role` — it describes
what you did, not what you intend.

**Revised recommendation: adopt in Phase 3A with two-tag structure.**
Flop plan = `[flop_action_tag, turn_response_tag]`. Turn plan = `[turn_action_tag]`.
River has no plan field. If the two-tag structure is too complex for Phase 3A,
defer — but the single-tag version is not a plan, it is a label.

---

## Q2 — Does "emergent vocabulary" address the 15-tag concern?

Yes. The desk-imagined list was my main concern about completeness. The
emergent approach will surface the tags that actually appear in real hands.
Two observations:

First, the seed list still matters. A poor seed list will anchor early
proposals even under "reason first." If the first five agents all see
`value_bet` in the seed list, their proposed additions will cluster around
bet intentions. The seed list should be action-balanced from the start.

Second, the merge/reject step after first batch is critical. Without it,
synonym drift produces five tags that mean the same thing. Assign one person
(owner or GTO Expert) to do that review — it is a poker judgment call, not
a mechanical dedup.

---

## Q3 — Does "reason first, tag second" address the padding concern?

Partially. Anchoring bias is the smaller problem. The larger problem is
pressure: an agent that is told "intentions is a list" will add a second
intention even when only one is real, because a list with one item feels
like an incomplete answer. "Reason first" does not fix this — the agent
still feels pressure to justify why the list has only one item.

Fix: make the prompt explicit that 1 intention is the correct answer for
clear spots. "If only one tag matches your reasoning, use one. A second
tag that does not appear in your reasoning is noise." This is a prompt
engineering instruction, not a vocabulary question.

---

## Q4 — Seed lists

### Intention seeds (~6 tags, action-balanced)

These cover the dominant WHY for each action class. Every other intention
should be a refinement or subdivision of one of these.

| Tag | Action class | Core meaning |
|---|---|---|
| `value_extract` | BET/RAISE | Worse hands call, you profit on this street |
| `deny_equity` | BET/RAISE | Villain has draws; charge them or fold them out |
| `bluff_fold_better` | BET/RAISE | You are behind; you win only if villain folds |
| `continue_draw` | CALL | You have outs; future street equity justifies price |
| `pot_control` | CHECK/CALL | Hand has showdown value but cannot handle large pot |
| `range_fold_priced_out` | FOLD | Villain's action + range puts you too far behind to continue |

Notes on what these intentionally exclude from the seed list:
- `semi_bluff` is a combination of `deny_equity` + `bluff_fold_better` +
  `continue_draw` — let agents propose the subdivision if they find it real
- `trap` is a subdivision of `pot_control` for strong hands — emergent
- `thin_value` is a subdivision of `value_extract` — emergent
- `mandatory_defend` (range balancing) is a CHECK/CALL intention that
  belongs in the emergent layer — it requires range awareness that may
  not surface in early hands

### Street plan seeds (~5 tags, two-part format)

**Flop action tags** (what you are doing now):
- `barrel_value` — betting for value, plan to continue on most turns
- `bet_protect_evaluate` — betting to deny equity, turn action depends on runout
- `check_trap` — checking strong hand to induce villain aggression
- `check_pot_control` — checking medium hand to manage pot size
- `draw_continue` — calling/checking with a draw, planning to realize equity

**Turn response tags** (conditional on being called / seeing a turn):
- `continue_on_blank` — bet again if turn does not complete obvious draws
- `give_up_on_complete` — check/fold if draw completes
- `check_evaluate` — no strong prior plan; reassess on turn card
- `pot_control_check_call` — check turn, call one bet, fold river to pressure
- `bet_regardless` — committed to two streets of aggression regardless of runout

A flop plan entry looks like: `["bet_protect_evaluate", "continue_on_blank"]`

---

## Q5 — Agent load at 10 hands, and "reason then tag" overhead

"Reason then tag" adds minimal time per hand — it is a lookup step after
reasoning the agent already does. The overhead is not per-hand reasoning;
it is the vocabulary management overhead (checking whether a new tag is
needed, writing a definition, submitting a proposal). That overhead is
real but it falls on the batch review step, not the per-hand labelling.

At 10 hands per agent the risk is still late-batch drift, as noted in my
first assessment. The emergent vocabulary adds one more late-batch risk:
agents 8-10 will see a growing proposed-tag list and start using proposed
tags that have not yet been reviewed or accepted. The prompt must be clear:
use only the approved seed list plus your own new proposals. Do not use
another agent's unreviewed proposal.

**Workable at 10 hands if:** the prompt specifies (a) approved tags only
plus own new proposals, (b) 1 intention is valid for clear spots, and
(c) the two-tag street plan structure is enforced.

---

## Revised overall recommendation

| Field | Phase 3A | Notes |
|---|---|---|
| Multi-label intentions | Adopt | Seed list above; 1 tag minimum enforced |
| Street plans (tagged) | Adopt | Two-tag structure only; single tag is not a plan |
| Feature attention (PRIMARY only) | Adopt | Curated 20-feature list in prompt; no SUPPORTING tier |
| Emergent vocabulary review | After first batch | Owner or GTO Expert merges/rejects proposals |
