---
date: 2026-04-13
from: Reviewer (main terminal) + Owner direction
to: Builder team
re: Forward-thinking gap in labelling prompt — add to Phase 3A
status: INCORPORATE — goes into the bucket-first prompt rewrite
---

# Forward-Thinking Gap in Labelling Prompt

## 1. The problem

The current labelling prompt (`gto_labeller_v1.md`) evaluates each
street as an isolated decision. The 5-factor framework asks "what
is the correct action NOW?" but never asks "what happens NEXT?"

**Evidence from the prompt:**

- The 5 factors (equity, position, range composition, board
  texture, action history) are all backward- or present-looking.
  None asks about future streets.
- DO NOT Rule #7 says "DO NOT analyze streets in isolation.
  Consider the full street tree." But this is a negative rule
  with no positive framework — it says what NOT to do without
  explaining what TO do.
- The reasoning protocol (lines 166-186) has 6 steps. None
  mention forward planning.
- The KB mentions "equity realization" and "implied odds" in
  passing (worked examples) but never instructs the agent to
  reason about them systematically.

**One forward-looking reference in the entire prompt:**

> Line 255-256: "A pot-sized flop bet 3-way leaves SPR ~1.5
> on the turn. Consider the full street tree."

That's SPR compression — a single mechanical consequence. Not a
reasoning framework for forward planning.

## 2. Why it matters for labelling

Forward-thinking changes the correct action in common spots:

### Drawing hands — implied odds

A flush draw with 35% equity and 3:1 pot odds looks like a
marginal call on equity alone. But if hero's flush completes on
the turn and villain has a strong but second-best hand, the
implied odds (future money won when hero hits) justify the call.
Without forward-thinking, the agent sees "35% equity, 25% pot
odds, equity > pot odds → CALL" and gets the right answer for
the wrong reason. Or it sees "35% equity, close to threshold →
FOLD" and gets it wrong entirely.

### Medium-strength hands — pot control plan

Checking top pair weak kicker on the flop is only correct if
hero has a plan for the turn. "Check, then call one bet, then
fold to river aggression" is pot control. "Check, then face a
bet, then agonize" is not a plan. The label should reflect
whether checking leads to a viable street plan, not just whether
checking is better than betting in isolation.

### Protection bets — equity denial

Betting a vulnerable made hand on the flop to deny free cards
is forward-looking by definition. "Bet now because the turn
might bring a flush card / straight card / overcard that kills
my equity" — this reasoning only works if the agent considers
what future cards do to the hand.

### Thin value bets — card removal

"Bet now because the turn might kill my action" is a
forward-thinking judgment. If hero has top pair on a dry flop,
the turn is likely to be a blank — hero can bet again. If hero
has top pair on a wet flop, the turn might scare villain into
folding — bet now for thin value while villain still calls.

### RAISE — building the pot

Raising a strong hand on the flop to build the pot for turn and
river value is forward-thinking. Raising a drawing hand as a
semi-bluff plans for two outcomes: villain folds now (immediate
profit), or villain calls and hero hits the draw (pot is bigger
for the payoff). Both branches require thinking ahead.

## 3. What to add to the bucket-first prompt

The Phase 3A prompt rewrite (bucket-first reasoning protocol)
already has 4 steps: Classify → Situation → Consider All Actions
→ Verify. Forward-thinking fits naturally into Step 3.

**Current Step 3 (from PLAN_V2.2_FINAL_COMBINED, line 262-273):**

```
3. CONSIDER ALL ACTIONS.
   For this hand type in this situation, evaluate every legal
   action. For each, name the strategic role:
   - BET/RAISE with monster/strong → value
   - BET/RAISE with drawing → semi-bluff (requires nut draw
     + blocker 3-way, per KB Section 1.7)
   - CHECK with strong on safe board → trap or pot control
   - CALL with drawing hand getting right price → drawing call
   - FOLD with medium hand when action narrows ranges above
     you → range fold

   No action is the default. Each must earn its place.
```

**Proposed addition — add after "Each must earn its place":**

```
   For each candidate action, state the STREET PLAN:

   - If you BET or RAISE: What's your plan when called? Are
     you betting again on the next street? What if a scare card
     comes (flush completes, straight fills, overcard lands)?
     What if you face a raise — can you continue?
   - If you CHECK: What's your plan when villain bets? Call,
     fold, or check-raise? If villain checks through, are you
     betting the next street?
   - If you CALL: What's your plan if you miss your draw?
     Fold to another bet? What if you hit — how much more can
     you win (implied odds)? Is the call only profitable with
     implied odds factored in?
   - If you FOLD: Is folding now better than calling and facing
     a worse decision on the next street with no improvement
     outs?

   An action without a viable plan for the next street is
   usually wrong, even if it looks correct in isolation.

   Exception: RIVER decisions have no future streets. On the
   river, evaluate the current street only.
```

**Also update Step 4 (Verify):**

```
4. CHOOSE AND VERIFY.
   Select the action with the strongest case. Then verify:
   "You have a [bucket] hand. The correct play is [action]
   because [strategic role] given [key situation factor].
   On the next street, the plan is [street plan]."
   If this sentence doesn't sound like a poker coach
   explaining the play, reconsider.
```

## 4. What changes in the output format

Add `street_plan` as an optional output field (required for
flop and turn, omitted for river):

```json
{
  "situation_id": "...",
  "hand_bucket": "drawing",
  "action": "CALL",
  "strategic_role": "drawing_call",
  "street_plan": "Call flop, evaluate turn card. If flush
    completes: bet for value. If brick: check-fold to a
    second barrel. Implied odds justify the call — villain's
    strong range will pay off a completed flush.",
  "confidence": "MEDIUM",
  "reasoning": "...",
  "alternatives_considered": ["RAISE: rejected because..."]
}
```

This field serves two purposes:
1. Forces the agent to actually think ahead (can't fill it in
   without reasoning about future streets)
2. Gives the comparison report richer data — when old label and
   new label disagree, the street plan shows WHY the bucket-first
   agent chose differently

## 5. What this does NOT change

- **The 5-factor framework** — forward-thinking uses the same
  factors (board texture → dynamic boards change on future
  streets, range composition → villain range narrows as streets
  progress, SPR → bet sizing commits future-street decisions).
  It's not a new factor — it's applying existing factors across
  time.
- **The KB** — already contains the relevant concepts (equity
  realization, implied odds, SPR compression, barrel decisions).
  The agents just aren't told to use them proactively.
- **The calibration exam** — the 24 hands already have correct
  labels. Forward-thinking doesn't change answers, it changes
  the quality of reasoning that produces them.
- **Feature extraction** — no new features needed. `danger_score`,
  `draw_outs`, `spr`, `improvement_probability` already capture
  the inputs forward-thinking needs.

## 6. Risk

**Risk: agents write long street plans that slow down labelling
without improving label quality.**

Mitigation: The `street_plan` field is 1-2 sentences, not a full
analysis. "Call, fold to second barrel if miss, bet if hit" is
sufficient. The instruction says "state the street plan" not
"analyze all possible runouts."

**Risk: agents over-weight future streets and under-weight the
current decision.**

Mitigation: The street plan is part of Step 3 (evaluating each
action), not a separate step. It modifies the action evaluation,
it doesn't replace it. The bucket classification (Step 1) and
situation reading (Step 2) are unchanged.

## 7. Action for builder

Incorporate this into the Phase 3A prompt rewrite. Specifically:

1. Add the street plan block to Step 3 of the bucket-first
   reasoning protocol
2. Update Step 4's verify sentence to include street plan
3. Add `street_plan` as an optional field in the output JSON
   (required for flop/turn, omitted for river)
4. No changes to calibration exam, KB, or feature extraction

This is an addition to Phase 3A, not a new phase. No schedule
impact.

---

**For builder: fold this into the Phase 3A prompt rewrite
alongside the bucket-first protocol, MW-30 fix, and
villain_range_capped demotion.**

---

## Amendment: Multi-Label Intentions (Owner Direction)

### 8. The insight

A single action often has multiple simultaneous reasons. A top
pair bet on a wet flop is:
- **Value** — worse hands call (second pair, weak top pair)
- **Protection** — draws fold (flush draws, straight draws)
- **Equity denial** — preventing free cards that shift equity

The current `strategic_role` field is a single string. This forces
the labelling agent to pick one reason when there are two or three.
Teaching then leads with one reason and the student misses the
others.

### 9. What to change in the output format

Replace the single `strategic_role` with multi-label `intentions`:

```json
{
  "situation_id": "...",
  "hand_bucket": "strong_made",
  "action": "BET",
  "intentions": [
    "value_get_worse_to_call",
    "protection_fold_draws"
  ],
  "primary_intention": "protection_fold_draws",
  "street_plan": "Bet flop for protection. If called, evaluate
    turn card — bet again on safe runouts, check-call on
    completing draws.",
  "confidence": "HIGH",
  "reasoning": "...",
  "alternatives_considered": ["CHECK: rejected because..."]
}
```

**Field definitions:**

- `intentions`: list of ALL reasons this action is correct.
  Order: most important first. Minimum 1, no maximum.
- `primary_intention`: the single strongest reason — what
  teaching leads with. Must be the first item in `intentions`.

### 10. Intention vocabulary

Agents select from this list. Each intention names what you
WANT to happen — the goal, not the category.

**BET / RAISE intentions:**

| Intention | Meaning | Example |
|---|---|---|
| `value_get_worse_to_call` | Worse hands will call and you profit | Betting top set on dry board |
| `thin_value_target_marginal_calls` | Targeting calls from hands that barely continue | Betting TPTK for 33% pot 3-way |
| `protection_fold_draws` | Fold out drawing hands that have equity against you | Betting overpair on wet board |
| `equity_denial_prevent_free_cards` | Prevent free cards that shift equity on future streets | Betting medium pair on dynamic board |
| `semi_bluff_fold_equity_plus_draw` | Fold equity now + equity when called and draw hits | Raising nut flush draw with blocker |
| `bluff_fold_out_better` | Pure bluff — fold out hands that beat you | River bet with air, blockers to value |
| `build_pot_for_future_streets` | Inflating pot now to extract more later | Raising set on flop to build turn/river pot |

**CALL intentions:**

| Intention | Meaning | Example |
|---|---|---|
| `drawing_call_implied_odds` | Calling to hit a draw — implied odds justify it | Calling with flush draw, deep stacks |
| `drawing_call_direct_odds` | Calling with a draw — pot odds alone justify it | Calling small bet with combo draw |
| `defend_range_mandatory` | Must call to avoid being exploitably folded | Calling with middle pair facing small bet |
| `pot_odds_priced_in` | Price is too good to fold regardless of hand | Calling 15% pot bet with any showdown value |

**CHECK intentions:**

| Intention | Meaning | Example |
|---|---|---|
| `pot_control_medium_hand` | Managing pot size with a hand that can't handle a big pot | Checking top pair weak kicker OOP |
| `trap_induce_villain_bet` | Checking strong hand to let villain bet, then raise or call | Checking set on dry board |
| `no_value_target` | Nothing worse calls, nothing better folds — no reason to bet | Checking second pair on static board |
| `free_card_draw` | Checking with a draw to see the next card cheaply | Checking flush draw IP after villain checks |

**FOLD intentions:**

| Intention | Meaning | Example |
|---|---|---|
| `range_fold_action_narrows_above` | Action history puts you below villain's continuing range | Folding TP to bet-and-call on turn |
| `equity_denial_accepted` | Cannot profitably continue — equity too low for price | Folding air facing pot-sized bet |

### 11. Why multi-label matters for future learning

**Now (v2.2):** Log the intentions. Teaching uses them
immediately. The L3 renderer can say:

> "You're betting here for two reasons: to get value from
> weaker made hands that will call, and to fold out the
> draws that have ~30% equity against you."

vs the current single-reason output:

> "This is a protection bet."

**v2.3 experiment — Intention Prediction Model:**

Train a second XGBoost model (multi-label) alongside the
action model:

```
Model 1: Features → Action (5-class, decides)
Model 2: Features → Intentions (multi-label, explains)
```

Model 2 learns to predict WHY from the same features that
Model 1 uses to predict WHAT. If Model 2 is accurate, the
oracle can explain its own decisions without the teaching
system having to guess the reason from spot_classifier.

**Why this is worth logging now:**
- 385 hands with multi-label intentions = training data for
  Model 2
- Can't train Model 2 without the labels
- Logging costs nothing — it's one extra field in the JSON
- If Model 2 doesn't work, the intentions are still valuable
  for teaching

### 12. What this changes in Phase 3A

The bucket-first prompt rewrite now produces:

```json
{
  "situation_id": "...",
  "hand_bucket": "...",
  "action": "...",
  "intentions": ["...", "..."],
  "primary_intention": "...",
  "street_plan": "...",
  "confidence": "...",
  "reasoning": "...",
  "alternatives_considered": ["..."],
  "difficulty": 1
}
```

New fields vs the previous spec:
- `intentions` (list) — replaces `strategic_role` (string)
- `primary_intention` (string) — what teaching leads with
- `street_plan` (string) — forward-thinking (flop/turn only)

The labelling agent selects from the vocabulary in Section 10.
Multiple intentions per hand are expected and encouraged. The
reviewer checklist (Phase 3D) should verify:
- At least 1 intention per hand
- `primary_intention` matches the first item in `intentions`
- Each listed intention is justified by the reasoning
- Multi-label hands actually have multiple distinct reasons
  (not just synonyms)

### 13. What this does NOT change

- Model 1 (action prediction) trains on 5-class labels only
- Feature extraction — no new features
- Calibration exam — tests action correctness, not intention
- KB v1.3 — no changes
- v2.2 success criteria — measured by action accuracy, not
  intention accuracy

The intentions are logged data for v2.3, not v2.2 training
targets.

---

**For builder: incorporate Sections 8-13 into Phase 3A alongside
the bucket-first protocol, forward-thinking, MW-30 fix, and
villain_range_capped demotion. The output JSON schema expands
but the model training pipeline is unchanged.**
