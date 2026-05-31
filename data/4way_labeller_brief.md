# Phase 2-F2 4-way Corpus Labeller Brief (v3.5)

You are a fresh GTO labelling agent for Phase 2-F2 — labelling 4-way lookalike situations for the v9-4way model retrain. This brief extends the HU labeller brief (Phase 1.5-D.3) with the multiway dimensions that 4-way decisions require.

**This is the FULL 4-way labelling phase, gated by Phase 2-E.0 labeller-readiness validation** (29-hand calibration + 5-hand pilot validation; QC PASS required before this brief fires production-scale).

**v3.5 additions (mandatory):** board-read attestation as structured JSON (§Board-Read Attestation), mandatory suit-count checklist (§Suit-Count Checklist), straight-draw verification procedure (§Straight-Draw Verification), and BET_RAISE chain bluff-collapse note in 4-way dimensions. These additions were driven by the batch_009 board-reading audit (2026-05-30) which found 329 CONFLATED_BDFD_AS_FD errors and 224 PHANTOM_GUTSHOT flags across 1,926 labeller-spot pairs.

## Critical: anti-rule-based labelling (read FIRST)

Phase 1.5-D.3 pilot exposed FL4-style failure: one labeller wrote a Python rule-based scoring script; others used template-based reasoning. **All such labels were invalidated.** This brief enforces explicit prohibitions.

**Absolute prohibitions** (any of these invalidates ALL your labels):
- ❌ NO if/elif rule chains in your reasoning (e.g., "if hand_rank > 5 then RAISE")
- ❌ NO threshold-based logic ("equity above 0.55 → BET; below → CHECK")
- ❌ NO template repetition across hands (each rationale must derive from THAT spot's poker theory)
- ❌ NO Python-script-style reasoning anywhere in the per-hand rationale
- ❌ NO citation of solver tools or equity calculators as label rationale; this is your reasoning, not solver-replay
- ❌ NO equity thresholds in your reasoning prompt (per `feedback_bucket_first_labelling.md`: bucket assignment FIRST, then action; thresholds live in `spot_classifier.py`, not in labelling prose)

## Suit-Count Checklist — MANDATORY before any draw-based claim

Run this checklist for EVERY hand before writing any rationale that
mentions a flush draw, backdoor flush draw, or nut flush draw.

**Step 1 — Count suits.**
For each of the 4 suits (s/h/d/c), count the total number of cards
of that suit across hero's 2 hole cards AND all board cards combined.

**Step 2 — Apply the threshold.**

| Max suited count (hero + board) | Flush status |
|----------------------------------|--------------|
| ≥ 4 and hero holds A of that suit | **NFD** (nut flush draw) |
| ≥ 4 and hero does NOT hold A of that suit | **FD** (non-nut flush draw) |
| Exactly 3 | **BDFD** (backdoor flush draw only) |
| ≤ 2 | **NONE** (no flush draw of any kind) |

**Step 3 — Write the result into `board_read_attestation.flush_status`**
before writing any prose about flush draws. See §Board-Read Attestation.

**FD and BDFD are NOT interchangeable.** FD contributes ~9 outs
(~18% equity to complete by river from flop). BDFD contributes
runner-runner only (~4-5% equity). Calling BDFD an "FD" inflates
perceived equity by ~13pp — enough to flip FOLD/CALL decisions.

### Worked suit-count table: AsKs on Jc7s5d2h

This is the canonical CHAIN-009-016 error class from batch_009.
All 5 labellers + the Opus tier-up miscounted this board.

| Source | Card | Suit |
|--------|------|------|
| Hero hole card | As | spades |
| Hero hole card | Ks | spades |
| Board card | Jc | clubs |
| Board card | 7s | spades |
| Board card | 5d | diamonds |
| Board card | 2h | hearts |

**Total spades: As + Ks + 7s = 3 spades.**

3 < 4 → **BDFD, not NFD, not FD.**

`board_read_attestation.total_by_suit = {"s": 3, "h": 1, "d": 1, "c": 1}`
`board_read_attestation.flush_status = "BDFD"`

The correct action on this spot (CHAIN-009-016, facing turn bet with
~15-18% raw equity vs 39% pot odds) is FOLD. The phantom-NFD rationale
drove incorrect CALL votes across labellers and the Opus tier-up. The
debate panel corrected this by running the suit-count explicitly.

---

## Straight-Draw Verification Procedure — MANDATORY before any gutshot/OESD claim

Before writing "gutshot," "OESD," "double-gutshot," or any straight-draw
claim, you MUST enumerate the specific 5-card sequence that completes
the draw. If you cannot name the completing rank, you do not have the draw.

**Procedure:**

1. List all ranks available to hero: 2 hole cards + all board cards.
2. For each possible 5-card consecutive-rank window (A-high down to
   5-high/wheel), check: does this window contain 4 of the 5 required
   ranks from hero+board combined, with exactly 1 rank missing?
3. The 1 missing rank is the completing rank (gutshot out). If 2 ranks
   missing: runner-runner only — NOT a straight draw.
4. If TWO different windows each have exactly 1 missing rank:
   double-gutshot (8 outs total).
5. If a single window has exactly 1 missing rank at BOTH ends (e.g.,
   missing the low card AND the window can be completed from either
   direction): OESD (8 outs).

**Do not claim runner-runner straight draws as outs.** Only single
remaining-card completions count as straight outs.

### Worked example: AdJh on Th6d4c — zero outs (phantom gutshot class)

- Hero: Ad, Jh — ranks A, J.
- Board: Th, 6d, 4c — ranks T, 6, 4.
- Combined: A, J, T, 6, 4.

Enumerate 5-card windows:
- A-K-Q-J-T: present = A, J, T (3 of 5); missing = K, Q (2 ranks) → runner-runner.
- K-Q-J-T-9: present = J, T (2 of 5); missing = K, Q, 9 (3 ranks) → impossible.
- Q-J-T-9-8: present = J, T (2 of 5); missing = Q, 9, 8 → impossible.
- J-T-9-8-7: present = J, T (2 of 5); missing = 9, 8, 7 → impossible.
- T-9-8-7-6: present = T, 6 (2 of 5); missing = 9, 8, 7 → impossible.
- 9-8-7-6-5: present = 6 (1 of 5); missing = 9, 8, 7, 5 → impossible.
- 8-7-6-5-4: present = 6, 4 (2 of 5); missing = 8, 7, 5 → impossible.
- 7-6-5-4-3: present = 6, 4 (2 of 5); missing = 7, 5, 3 → impossible.
- 6-5-4-3-2: present = 6, 4 (2 of 5); missing = 5, 3, 2 → impossible.
- 5-4-3-2-A: present = A, 4 (2 of 5); missing = 5, 3, 2 → impossible.

**Result: zero straight outs. `board_read_attestation.straight_outs = []`.**

AdJh on Th6d4c is ace-high with a backdoor-wheel possibility only.
There is no gutshot. Do not write "gutshot" in the rationale.

### Why this matters: MW-54 phantom gutshot (batch_009 5-way reference)

The architect's MW-54 rationale claimed "nut FD + gutshot + 2 overcards"
for Ah9h on Jh7h2c and estimated ~45% combo-draw equity. The debate panel
enumerated every 5-card window and found zero gutshot outs. The correct
draw composition is NFD only (~9 outs → ~38% equity from flop). The panel
overrode the architect's RAISE recommendation to CALL as a direct result
of the gutshot-enumeration correction. Name the completing rank or drop
the straight-draw claim.

---

## Board-Read Attestation — Structured JSON Field (v3.5 schema addition)

**Every label must include a `board_read_attestation` object as the
FIRST substantive field after `spot_id` and `labeller_id` in the JSON.**

This field is mechanically validated by the consensus pipeline. A
missing or null attestation causes the label to be **rejected at
collection time**. Do not skip it.

```json
"board_read_attestation": {
  "total_by_suit": {"s": <int>, "h": <int>, "d": <int>, "c": <int>},
  "flush_status": "NFD" | "FD" | "BDFD" | "NONE",
  "straight_outs": [<completing rank strings, e.g. "8", "Q">]
}
```

- `total_by_suit`: suit counts across hero hole cards + board cards combined.
- `flush_status`: derived per the Suit-Count Checklist thresholds above.
- `straight_outs`: list of ranks (as strings) that complete a straight
  for hero by the enumeration procedure above. Empty list `[]` if zero
  outs. Do NOT include runner-runner completing ranks.

The attestation MUST appear BEFORE `predicted_action` in the JSON output.
See Output Schema below for the updated field ordering.

---

## Action-space discipline: when each action is LEGAL (READ BEFORE LABELLING)

The legal action space at the decision moment is determined by `facing_bet`. Predicting an action outside the legal space is a labelling defect — your label is REJECTED at consensus regardless of reasoning quality.

**When `facing_bet == 0`** (no bet to call this street):
- Legal actions: **BET** (you initiate aggression) or **CHECK** (you pass action)
- ILLEGAL: FOLD (nothing to fold to), CALL (no bet to match), RAISE (no bet to raise)

**When `facing_bet > 0`** (you are facing a bet/raise this street):
- Legal actions: **FOLD** (give up), **CALL** (match), or **RAISE** (raise the existing bet)
- ILLEGAL: BET (cannot bet when facing a bet — that's a raise), CHECK (cannot check when facing aggression)

**Sizing fields** (TWO separate fields — read carefully):
- `predicted_action: BET` → set `predicted_bet_pct: <int>` (% of pot, ∈ {25, 33, 50, 66, 75, 100, 150}); set `predicted_raise_to_bb: null`.
- `predicted_action: RAISE` → set `predicted_raise_to_bb: <int>` (bb amount of the raise-TO size — the TOTAL chips you push, NOT the raise-by increment); set `predicted_bet_pct: null`.
- `predicted_action: CHECK | CALL | FOLD` → BOTH fields null.

**Worked phrasing — copy these EXACTLY**:
- BET 66% of pot: `"predicted_action": "BET", "predicted_bet_pct": 66, "predicted_raise_to_bb": null`
- RAISE to 9bb total: `"predicted_action": "RAISE", "predicted_bet_pct": null, "predicted_raise_to_bb": 9`
- CHECK: `"predicted_action": "CHECK", "predicted_bet_pct": null, "predicted_raise_to_bb": null`

**Why two fields**: BET sizes are naturally expressed as % of pot (solver convention). RAISE sizes are naturally expressed as bb-total raise-TO (because raise-by/raise-to confusion + % of pot ambiguity in multiway is unrecoverable). Do not write a % in `predicted_raise_to_bb` — that is field-mismatch FL7, and your label is REJECTED at consensus.

**Hard constraint**: Action-space is NOT a soft preference. Before writing any label, look at `facing_bet` in the input row. If `facing_bet == 0` and you find yourself reaching for FOLD or CALL, your reasoning has departed from the actual decision moment — that label is wrong before you even evaluate the poker. The same applies for BET/CHECK when `facing_bet > 0`.

**FL5 failure class — illegal action vote**: voting an illegal action (e.g., FOLD when facing_bet=0) is a labelling defect distinct from FL4 rule-based drift. If your reasoning cites threshold-style logic to reach an illegal action, your label is wrong twice over (FL4 + FL5) and both your batch and your reasoning are rejected. Don't conflate "I would fold this hand preflop" reasoning with "FOLD on the flop spot in front of me" — re-read `facing_bet` before every label.

**FL7 failure class — sizing-field mismatch**: writing a % value in `predicted_raise_to_bb` (e.g., 75, 300, 360) or a bb value in `predicted_bet_pct` (e.g., 9, 18) is a labelling defect. If you cannot compute the raise-to in bb, use `confidence: LOW` and write the value you intended in the reasoning prose; owner-arb queue will adjudicate. Do NOT write a malformed value.

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

### BET_RAISE chain bluff-collapse in 4-way pots (AMENDMENT 3)

In 4-way pots, a BET followed by a RAISE (BET_RAISE chain) creates a
dramatically more value-heavy range for the raiser than in HU or 3-way.
The raiser must price through TWO player ranges: the bettor's range AND
the remaining flat-callers' ranges behind. This dual-range pressure
collapses the bluff fraction of a MW BET_RAISE to approximately
**75-80% value** (vs ~50% value for a HU raise of a flop bet).

**Why the collapse is sharper in 4-way:**

- In HU, the raiser only needs to price through the bettor. The bluff
  component can be ~33-50% of the raising range (river math ≈ 33%
  bluffs, closer to 50% on earlier streets with implied odds).
- In 4-way, the raiser faces: (a) the bettor re-raising or continuing,
  AND (b) 2 remaining players who can cold-call or cold-raise behind.
  Raising as a bluff with cold-callers still to act is -EV: the raiser
  gets called by the bettor's value AND by flat-callers who have
  closed their range toward made hands (cold-callers of a bet are
  range-capped but their continuing range is value-dense). Net fold
  equity collapses.
- GTO equilibrium: 4-way BET_RAISE raiser is ~75-80% value, ~20-25%
  bluff (compared to ~50-67% value HU on flop).

**Implication for labelling:** When hero faces a BET_RAISE chain in a
4-way pot, treat the raiser's range as predominantly value. Do NOT model
the raiser as having a standard HU bluff frequency. The remaining 2+
players (if still in) exert the same pressure, further narrowing
the raiser's realistic bluff combos. A hero hand with only 35-40% equity
vs the raiser's range (after BET_RAISE) is closer to a FOLD than in HU
where the same equity vs a solo-raiser often warrants a CALL.

Explicitly note in your rationale when a BET_RAISE chain is present:
"BET_RAISE chain in 4-way pot → raiser's range is ~75-80% value;
hero needs ~35%+ equity for a +EV call given pot odds and range
compression."

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
- **BET sizing (% of pot, into `predicted_bet_pct`)**:
  - Flop: 25 or 66
  - Turn: 33 or 75
  - River: 33 / 75 / 150
- **RAISE sizing (bb raise-TO, into `predicted_raise_to_bb`)**:
  - vs flop bet: 3.0–4.0× the bet size, converted to total raise-to bb.
  - vs turn bet: 2.5–3.0× the bet size.
  - vs river bet: 2.5–3.5× the bet size.
  - **Preflop BB-defend min 3-bet**: facing a 2.5bb open, min-raise is to 5bb (i.e., raise-to ≥ 2 × open_size). A min-raise 3-bet from BB is `predicted_raise_to_bb: 5`, NOT 4.
The `predicted_raise_to_bb` value must be the FINAL chip count put in by hero (raise-to), not the increment.

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

**Schema version: v3.5 (brief v3.5 / KB v1.4 — 2026-05-31)**

Per spot to `data/4way_corpus/raw_labels_labeller_<N>.jsonl`:

```json
{
  "spot_id": "4WL-<axis>-<N>",
  "labeller_id": <N>,
  "board_read_attestation": {
    "total_by_suit": {"s": <int>, "h": <int>, "d": <int>, "c": <int>},
    "flush_status": "NFD" | "FD" | "BDFD" | "NONE",
    "straight_outs": [<completing rank strings>]
  },
  "predicted_action": "FOLD|CHECK|CALL|BET|RAISE",
  "predicted_bet_pct": <int or null>,
  "predicted_raise_to_bb": <int or null>,
  "confidence": "HIGH|MEDIUM|LOW",
  "bucket": "<spot-type classification>",
  "reasoning": "<250-400 word per-hand reasoning chain>",
  "num_opponents_at_decision": 3,
  "primary_axis": "<axis label>"
}
```

**Schema migration note (v3.5):** `board_read_attestation` is a new
required field introduced in this brief version. It must appear BEFORE
`predicted_action`. The consensus pipeline (`dispatch_4way_labelling_pilot.py`)
validates the presence and non-null status of this field at collection
time; labels missing the field are rejected. Existing consensus_v2 files
(batches 001–009) do not contain this field; migration of existing files
is a separate ticket. This validation applies to all new labels produced
under brief v3.5 onwards (starting with batch_010 pilot).

Set `predicted_bet_pct` ONLY for BET actions; set `predicted_raise_to_bb` ONLY for RAISE actions. Both null otherwise.

Include `bucket` as your bucket-first classification (e.g., "4-way-SRP-closing-IP", "4-way-3-bet-pot-cold-call-flop", "multiway-cooler-top-set", "range-asymmetry-MP").

## Anti-rule-based self-check (apply before submitting)

Before submitting each label, verify your rationale:
- [ ] Does NOT contain `if`-style threshold rules ("if hand_rank > X")
- [ ] Does NOT contain numeric equity cutoffs ("equity = 0.55 → BET")
- [ ] Each rationale is UNIQUELY derived (no two hands share template wording)
- [ ] Per-villain range chains are PRESENT (not collapsed to "combined opponents")
- [ ] Equity realization factor (HU/3w/4w/5+) is EXPLICITLY mentioned where relevant
- [ ] Bucket classification is FIRST, action is derived AFTER
- [ ] `board_read_attestation` is present, non-null, and appears BEFORE `predicted_action` in the JSON
- [ ] `flush_status` in attestation was derived by counting suits (not pattern-matching to card names)
- [ ] Any claimed gutshot or OESD has a named completing rank in `straight_outs` (verified by enumeration)
- [ ] If `straight_outs` is empty, the rationale does NOT claim gutshot or OESD for hero

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
- `knowledge/three_way_gto.md` (**KB v1.4** — read §0 board-reading reference FIRST)
- `data/4way_reference_35hand_2026-05-11.jsonl` (reference set; for context only, NOT a labelling target)
- `review/comms/4WAY_REFERENCE_FULL_RATIONALE_2026-05-11.md` (reference rationale patterns; for style reference)
- `data/5way_reference_10hand_2026-05-30.jsonl` (5-way reference set; includes MW-54 canonical NFD-only example)

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
