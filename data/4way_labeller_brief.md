# Phase 2-E 4-way Corpus Labeller Brief

You are a fresh GTO labelling agent for Phase 2-E — labelling 4-way lookalike situations for the v9-4way model retrain. This brief extends the HU labeller brief (Phase 1.5-D.3) with the multiway dimensions that 4-way decisions require.

**This is the FULL 4-way labelling phase, gated by Phase 2-E.0 labeller-readiness validation** (29-hand calibration + 5-hand pilot validation; QC PASS required before this brief fires production-scale).

## Critical: anti-rule-based labelling (read FIRST)

Phase 1.5-D.3 pilot exposed FL4-style failure: one labeller wrote a Python rule-based scoring script; others used template-based reasoning. **All such labels were invalidated.** This brief enforces explicit prohibitions.

**Absolute prohibitions** (any of these invalidates ALL your labels):
- ❌ NO if/elif rule chains in your reasoning (e.g., "if hand_rank > 5 then RAISE")
- ❌ NO threshold-based logic ("equity above 0.55 → BET; below → CHECK")
- ❌ NO template repetition across hands (each rationale must derive from THAT spot's poker theory)
- ❌ NO Python-script-style reasoning anywhere in the per-hand rationale
- ❌ NO citation of solver tools or equity calculators as label rationale; this is your reasoning, not solver-replay
- ❌ NO equity thresholds in your reasoning prompt (per `feedback_bucket_first_labelling.md`: bucket assignment FIRST, then action; thresholds live in `spot_classifier.py`, not in labelling prose)

## Action-space discipline: when each action is LEGAL (READ BEFORE LABELLING)

The legal action space at the decision moment is determined by `facing_bet`. Predicting an action outside the legal space is a labelling defect — your label is REJECTED at consensus regardless of reasoning quality.

**When `facing_bet == 0`** (no bet to call this street):
- Legal actions: **BET** (you initiate aggression) or **CHECK** (you pass action)
- ILLEGAL: FOLD (nothing to fold to), CALL (no bet to match), RAISE (no bet to raise)

**When `facing_bet > 0`** (you are facing a bet/raise this street):
- Legal actions: **FOLD** (give up), **CALL** (match), or **RAISE** (raise the existing bet)
- ILLEGAL: BET (cannot bet when facing a bet — that's a raise), CHECK (cannot check when facing aggression)

**Sizing fields**:
- `predicted_action: BET` or `RAISE` → MUST specify `predicted_sizing_pct` (an integer % of pot for BET; integer bb amount for RAISE)
- `predicted_action: CHECK` or `CALL` or `FOLD` → `predicted_sizing_pct: null`

**Hard constraint**: Action-space is NOT a soft preference. Before writing any label, look at `facing_bet` in the input row. If `facing_bet == 0` and you find yourself reaching for FOLD or CALL, your reasoning has departed from the actual decision moment — that label is wrong before you even evaluate the poker. The same applies for BET/CHECK when `facing_bet > 0`.

**FL5 failure class — illegal action vote**: voting an illegal action (e.g., FOLD when facing_bet=0) is a labelling defect distinct from FL4 rule-based drift. If your reasoning cites threshold-style logic to reach an illegal action, your label is wrong twice over (FL4 + FL5) and both your batch and your reasoning are rejected. Don't conflate "I would fold this hand preflop" reasoning with "FOLD on the flop spot in front of me" — re-read `facing_bet` before every label.

Per `feedback_terminology_raise_vs_bet.md`: **bet** = first postflop action initiating aggression; **raise** = action that raises an existing bet (postflop) OR raises the preflop open. CHECK applies only when no bet faces you; CALL applies only when a bet faces you.

**Required reasoning structure (every hand)**:
1. **Pre-flop context**: opener position, intermediate flat/3-bet actions, hero's range at decision moment
2. **Per-villain range chains**: for each of the 3 villains, narrow their range across action history (preflop open/flat/3-bet → flop response → turn → river)
3. **Equity/range tensions at decision**: what hero's range looks like vs. each villain's narrowed range; equity realization adjusted by player count (HU≈1.0, 3-way≈0.85, 4-way≈0.75, 5+way≈0.70)
4. **Spot-specific factors**: blocker effects, position dynamics (closing-action vs. early-action), squeeze-pressure (AMENDMENT 2), players-left-to-act (AMENDMENT 1), pot geometry (SPR + facing-bet pressure)
5. **Action selection + rationale**: chosen action + the specific tensions that drove it; explicit comparison to adjacent alternatives

Target ~250-400 words per hand. If you find yourself writing the same prose for 2 different hands, STOP and re-reason — the rationale is wrong.

## 4-way-specific dimensions (vs. HU)

### Multiway range-chain reasoning

In HU, hero tracks ONE villain's range. In 4-way, hero tracks THREE villains' ranges, each narrowing INDEPENDENTLY across action history. Treat each villain separately:

Example chain for 4-way SRP at flop:
- **Villain A (preflop opener UTG)**: opens 2.5bb with range ~14% (TT+, AQs+, AKo, suited broadway, 87s+). Flop-c-bets ~70% on dry boards, ~75% on coordinated. Continuing range narrows on size: 25% c-bet keeps wider range; 66% c-bet narrows to value+strong-draws.
- **Villain B (flatted MP)**: range ~5-8% (88-TT, AJs-AQs, suited broadway, suited connectors). Did NOT 3-bet preflop → no AK/AA/KK in range. Flat behavior on flop varies.
- **Villain C (flatted BTN)**: range ~6-8% similar to MP but adjusted for position (more suited connectors, fewer dominated broadway).

Each villain's range chain ALSO matters for hero's equity-vs-RANGE calculation at the decision moment. DO NOT collapse all 3 villains into "combined opponents" — that loses critical multi-villain structural information.

### Players-left-to-act (AMENDMENT 1)

Squeeze-pressure asymmetry. When hero is OOP-early in a 4-way pot, all 3 villains can still apply pressure behind hero. When hero is IP-closing, no villains are behind. This shifts:
- **Donk-lead viability**: dominated when hero is OOP with 3 villains behind (announces polar range; loses fold equity)
- **Check-raise lines**: induce-then-CR is generally optimal for OOP+early action with semi-bluff equity
- **Raise sizing**: 4-way raises need to be larger (3-4x bet) to charge multi-villain ranges + deny equity

Explicitly note in your rationale: "Hero is [IP-closing / OOP-early / OOP-middle], so [pressure direction] applies."

### Closing-action vs. early-action variants (AMENDMENT 2)

- **Closing-action (IP, BTN-like)**: hero acts last; villains cannot apply pressure behind; CALL is more often correct (realize SDV cleanly); raises must justify charging villains who already declared
- **Early-action (OOP, SB/BB/EP)**: hero acts first; CHECK preserves optionality; donk-leading is dominated unless very strong range; check-raise opportunities are natural defenses

### Pot-cascade dynamics

A 4-way pot rarely STAYS 4-way through river. By turn it often collapses to 3-way; by river often 2-way. Hero's decision must account for:
- **Flop**: 4-way at decision; consider future-street decisions in 2/3-way
- **Turn**: 3-way is common; hero's decision now is for a 3-way pot evolving toward HU
- **River**: 2-way is most common; hero's decision is HU-equivalent

In your rationale, explicitly note `num_opponents_at_decision`. If hand collapsed (e.g., started 4-way, by river is 2-way), document the collapse explicitly.

### Range-chain narrowing across villains

When MP cold-calls UTG's open, MP's range is RANGE-CAPPED (no AK/AA/KK that would 3-bet; no weak air that folds). When CO behind also flats, CO's range is similarly capped but biased toward suited (position-adjusted). When BTN closes 3 callers with a flat, BTN's range includes suited connectors + middle pairs that play well multi-way IP.

Each villain's range at each decision point depends on:
- Their position
- Their action history (open/flat/3-bet/cold-call/fold)
- The ranges of villains who acted BEFORE them (range-chain dependence)

Capture this explicitly in your rationale.

## Bucket-first compliance (per `feedback_bucket_first_labelling.md`)

For each hand:
1. **Bucket FIRST**: classify the spot type (4-way 3-bet pot / 4-way SRP closing action / 4-way SRP OOP early / multiway cooler / range-asymmetry MP / etc.)
2. **Action SECOND**: derive the action from the bucket + spot-specific tensions

Do NOT use equity-percentage thresholds in your prompt or reasoning. Equity-vs-RANGE estimates are fine as part of reasoning, but DO NOT format them as "if equity > X then ACTION". The threshold logic lives in `spot_classifier.py` (the model architecture), not in labelling rationale.

## Solver-aligned bet sizing (per `feedback_solver_aligned_sizing.md`)

When you label a BET or RAISE action, use solver-aligned sizes:
- **Flop**: 25% (small c-bet) or 66% (polarized; usually for value+protection on wet boards)
- **Turn**: 33% (small) or 75% (polarized)
- **River**: 33% / 75% / 150% (over-bet for polar value/bluff)

Raises (raise-of-bet): 3-4x the bet size on flop; 2.5-3x on turn; 2.5-3.5x on river.

## Terminology (per `feedback_terminology_raise_vs_bet.md`)

- **open**: preflop opener (e.g., "UTG opens 2.5bb")
- **bet**: first postflop bet (e.g., "CO bets 25% pot")
- **raise**: raise of an existing bet (e.g., "BTN raises CO's c-bet to 8bb"; OR preflop "3-bet to 9bb")

Do NOT use "raise" for first postflop action — that's "bet".

## Per-villain range chains — practical examples

### Example A: 4-way SRP, hero BTN closing, K-high flop

Preflop: UTG opens 2.5, MP folds, CO calls, hero BTN calls, SB folds, BB calls.

At hero's flop decision (after CO checks, BB checks, UTG c-bets):

- **UTG**: opens-and-c-bets-25%-on-K-high range = ~70% of preflop opens. Includes: K-x value (KQ, AK, KJ, KK), set-K, overpair AA/KK, air bluffs (AJ-AQ broadway misses, suited connectors). Net composition: ~30% value, ~70% air at 25% sizing.
- **CO**: flatted UTG; range ~88-JJ / suited broadway / suited connectors. On K-high, CO continues with set-K (rare), KJ-suited at most. CO is range-capped (NO AA/KK/AK; would 3-bet). Most of CO's range x-folds.
- **BB**: closing-defended; range very wide (any 2 ≥ 65s, suited broadway, paired). On K-high, BB has occasional K-x (KQ-suited, K9-suited) + low-pair-with-FD-equity + air. Most x-folds.

Hero's decision is shaped by UTG (active aggressor; range-balanced 30/70) + CO+BB (capped; mostly x-folding). RAISE charges CO+BB out, isolates vs UTG's air; CALL keeps everyone in. Decision derives from UTG's range composition × position/equity factors.

### Example B: 4-way 3-bet cold-called pot

Preflop: UTG opens 2.5, CO 3-bets to 9, hero BTN cold-calls, SB folds, BB cold-calls.

At hero's flop decision after BB checks, CO bets:
- **CO (3-bettor)**: range very strong: QQ+/AK + sometimes A5s-A2s bluffs. On low/dry flop, CO c-bets ~85% (range-balanced bet). At wet boards, CO checks more (cap range).
- **BB (cold-caller of 3-bet)**: range range-strong: JJ-99/AQs/suited connectors that play well multi-way. NOT AA/KK (would 4-bet). Continuing range narrows on flop bet.

Hero's decision in 3-bet pot is range-cap-driven: CO is the aggressor with polar range; BB is capped. Hero (BTN cold-caller) is also capped → similar range to BB. Decision: navigate cap-vs-cap dynamic.

### Example C: Multiway cooler on FD board

Hero UTG has AA on Ah-8c-3h (top set on FD board). 4-way.

- **MP/CO/BTN**: each independently has FD potential (heart hands). Combined: ~25% of villains have at least 1 FD combo.
- **Realization vs. each villain's range**: AA dominates all hands not on flush draw; loses to runner-runner heart flush (~9% per villain × 3 villains; but only 1 can have it = ~25% combined).
- **Equity realization MW**: top set is ~78% to win at showdown vs. 3-villain range; drops to ~70% if board completes hearts.

Decision: BET 66% for value + protection. Slowplay loses ~25% of MW pots when a heart completes; bet pays off when villains call with FD/2nd-pair/draws.

## Per-hand structure required (in your rationale)

For each labelled spot, your reasoning prose must include (~250-400 words):

1. **Spot identification** (1-2 sentences): hand_id, street, hero position, num_opponents_at_decision, preflop sequence summary, current board, hero hole cards.
2. **Per-villain range chains** (3-5 sentences per active villain; 3 villains for 4-way): each villain's narrowed range with composition breakdown.
3. **Equity/range tensions** (2-3 sentences): hero's range vs. each villain; equity realization factor (HU/3-way/4-way/5+); blockers/unblockers; pot geometry (SPR, pot odds).
4. **Spot-specific factors** (2-3 sentences): position (closing-action / early-action / middle); players-left-to-act; squeeze-pressure if applicable; pot-cascade trajectory.
5. **Decision selection** (1-2 sentences): bucket + action + size if BET/RAISE; explicit GTO-frequency claim if mixed strategy (e.g., "RAISE 60% / CALL 40%").
6. **Adjacent alternatives** (1-2 sentences): why FOLD / CALL / RAISE / BET / CHECK alternatives are dominated or mixable.

Target word count: **250-400 words per hand**. Below 200 risks under-reasoning; above 500 risks rambling.

## Output schema

Per spot to `data/4way_corpus/raw_labels_labeller_<N>.jsonl`:

```json
{
  "spot_id": "4WL-<axis>-<N>",
  "labeller_id": <N>,
  "predicted_action": "FOLD|CHECK|CALL|BET|RAISE",
  "predicted_sizing_pct": <int or null>,
  "confidence": "HIGH|MEDIUM|LOW",
  "bucket": "<spot-type classification>",
  "reasoning": "<250-400 word per-hand reasoning chain>",
  "num_opponents_at_decision": 3,
  "primary_axis": "<axis label>"
}
```

Include `predicted_sizing_pct` ONLY for BET or RAISE actions.

Include `bucket` as your bucket-first classification (e.g., "4-way-SRP-closing-IP", "4-way-3-bet-pot-cold-call-flop", "multiway-cooler-top-set", "range-asymmetry-MP").

## Anti-rule-based self-check (apply before submitting)

Before submitting each label, verify your rationale:
- [ ] Does NOT contain `if`-style threshold rules ("if hand_rank > X")
- [ ] Does NOT contain numeric equity cutoffs ("equity = 0.55 → BET")
- [ ] Each rationale is UNIQUELY derived (no two hands share template wording)
- [ ] Per-villain range chains are PRESENT (not collapsed to "combined opponents")
- [ ] Equity realization factor (HU/3w/4w/5+) is EXPLICITLY mentioned where relevant
- [ ] Bucket classification is FIRST, action is derived AFTER

If you can't check ALL boxes for ALL hands, your batch will be REJECTED at QC. Reload the brief and re-reason.

## Calibration set + STOP-condition gate

Before you label production lookalikes, you take the **29-hand calibration exam BLIND** (see `data/4way_calibration_29hand_2026-05-11.jsonl` for source spots; corresponding answer key is sanitized so you don't see it). Pass thresholds:
- ≥21/29 correct (matches HU-pilot ≥20/28 ratio)
- 100% on the 7 GTO_REVERSAL_HANDS subset (TBD; orchestrator post-flop publishes)

Fail the calibration → your labels do not enter the consensus. Re-read the brief; re-reason; re-submit calibration.

## When you're done

Confirm to orchestrator:
1. Calibration completed (29/29 with self-confidence rating); HIGH-confidence count
2. Pilot lookalikes labelled (count + axis distribution)
3. Sanitization compliance: did NOT read unsanitized originals
4. Anti-rule-based attestation: no rule-based / template / threshold patterns in your batch

## References (mandatory reads before labelling)

- `data/4way_calibration_29hand_2026-05-11.jsonl` (calibration spots; sanitized)
- `review/comms/PHASE2E0_4WAY_CALIBRATION_SET_2026-05-11.md` (calibration design rationale)
- `prompts/gto_labeller_v3.4.md` (labelling protocol; verbatim)
- `knowledge/three_way_gto.md` (KB)
- `data/4way_reference_35hand_2026-05-11.jsonl` (reference set; for context only, NOT a labelling target)
- `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md` (reference rationale patterns; for style reference)

## Methodology rules (binding)

- Fresh agent, no shared state: do not look at other labellers' outputs
- Bucket-first: NO equity thresholds in reasoning; use composition + protocol rules
- Solver-vs-labels: don't cite solver as label rationale
- Terminology: raise = raise of existing bet; bet = first postflop bet; open = preflop opener
- Per-hand uniqueness: rationale templates across hands = REJECT
- Multiway dimensions explicit: range chains + players-left + cascade + closing-action all addressed

## What to do if you encounter ambiguous spots

If you cannot reach a confident GTO call for a spot:
- Mark `confidence: LOW`
- Write your rationale anyway, explaining the ambiguity (e.g., "50/50 between RAISE and CALL due to range-cap × multi-villain risk")
- Do NOT default to "I don't know" or skip; the orchestrator + owner will handle owner-arb adjudication post-batch

The dispatch protocol queues solver-verification for ambiguous spots later. Your job is to express the GTO-reasoning tension explicitly, not to pretend certainty.
