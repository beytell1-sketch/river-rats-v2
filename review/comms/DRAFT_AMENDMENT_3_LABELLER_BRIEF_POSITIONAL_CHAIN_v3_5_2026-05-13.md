---
date: 2026-05-13
from: Architect (Phase 2-F prep — DRAFT pending ratification)
to: Builder · gto-expert · QC stream · Owner
re: AMENDMENT 3 to data/4way_labeller_brief.md — positional action-chain mandatory phrasing + FL6 failure class
status: DRAFT — DRAFTED IN ADVANCE; builder reviews + ratifies + appends to 4way_labeller_brief.md on next tick
companion: review/comms/DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1_2026-05-13.md
references:
  - data/4way_labeller_brief.md (AMENDMENT 1 — players-left-to-act; AMENDMENT 2 — closing/early action variants)
  - memory: feedback_bucket_first_labelling.md, feedback_solver_vs_expert_labels.md
---

# AMENDMENT 3 — Positional Action-Chain Mandatory Phrasing

> **Insertion location:** append to `data/4way_labeller_brief.md` immediately
> after AMENDMENT 2 ("Closing-action vs. early-action variants"), before the
> "Pot-cascade dynamics" subsection. This amendment is binding on all Phase 2-F
> batch labellers.

## AMENDMENT 3 — Positional action-chain explicit naming (binding)

### 3.1 Why this amendment

BATCH-001..007 (Phase 2-E) consensus reached 96% average; Opus dissents on
BATCH-007 spots 312/323/352 share a pattern: rationales described villain
aggression in **aggregate** ("villain bets and someone calls", "facing bet+call
from earlier position") without naming *which villain* hero is responding to.
The aggregate framing loses the seat-order information that drives 4-way
decision quality — particularly in `BET_CALL` and `BET_CALL_CALL` chains
(see DRAFT_BLUEPRINT_POSITIONAL_CHAIN_DIMENSION_v1, §3).

Phase 2-F adds positional-chain stratification to the corpus (top-12 chains
get 40% of each batch's quota). Labellers must articulate the chain explicitly
or the corpus's positional structure is invisible in the training signal.

### 3.2 Mandatory phrasing template

For every labelled spot in Phase 2-F batches, the `reasoning` field MUST
include a sentence (or contiguous sentence-pair) that satisfies all four of
these requirements:

**(A) Name each surviving villain by position** at the decision moment.
The reasoning lists the active villains explicitly — "CO and BTN" not
"two villains".

**(B) Identify the aggressor by position** — the player who initiated
betting on the current street, OR state explicitly that the street has
been checked to hero.

**(C) Identify each prior caller** between the aggressor and hero, in
seat-order. If there are no prior callers, state so explicitly ("no
prior callers — hero is first to act after CO's bet").

**(D) Identify which villain's action hero is responding to.** This is
either the aggressor (single bet, hero faces it directly), the raiser
(bet+raise sequence), or the call-closer (hero is OOP-early and the
chain has bet+call(s) ending with a known caller behind whom hero must
act).

The phrasing template (use as a structural guide, not a verbatim copy):

> "Hero is [position], facing [aggressor]'s [bet-or-raise], with [prior
> caller(s) listed in seat-order, or 'no prior caller'] between [aggressor]
> and hero. The decision is against [responsible-villain-name + position]'s
> [bet / raise / call-closing range]."

This is one sentence. Combine with the standard per-villain range-chain
sentences (the existing per-hand structure §3.4 in 4way_labeller_brief.md
"Required reasoning structure (every hand)") which already require per-villain
range narrowing.

### 3.3 Bucket-first compliance — chain is part of bucket-assignment

Per `feedback_bucket_first_labelling.md`: the labelling prompt must NOT
introduce equity thresholds. The chain fingerprint is a **structural
property** of the spot (positions and actions, no equity), so it is
admissible in the bucket-assignment phase.

The order of reasoning remains:

1. **Bucket FIRST** (now augmented): classify the spot using BOTH:
   - hand bucket (monster / strong_made / medium_made / weak_made /
     drawing / air), AND
   - chain bucket (chain_shape from {OPEN, BET, BET_CALL, BET_CALL_CALL,
     BET_RAISE, CHECK_RAISE, MULTI_AGGR}) plus hero_pos.
   - Combined classification example: "4-way SRP flop, OOP-early hand
     class drawing on `BET_CALL` chain — hero is BB facing CO's bet
     with BTN as prior caller."
2. **Action SECOND**: derive from the combined bucket + spot-specific
   tensions.

NO equity thresholds appear in the bucket-assignment phase. Chain
fingerprint is **structural only** — positions and actions, no equity.

### 3.4 FL6 failure class — rationale missing chain identification

**Definition (binding):** A rationale that does not explicitly name each
villain by position AND identify which villain's action hero is responding
to is **rejected at consensus**, regardless of action-correctness.

This sits alongside FL4 (rule-based / threshold drift) and FL5 (illegal
action vote) in the labelling defect taxonomy. A FL6-rejected label does
NOT enter consensus; the consensus is computed over the remaining ≤4
labellers' labels. If ≥3 of 5 labellers are FL6-rejected on the same
spot, the spot escalates to owner-arb with explicit "FL6 escalation" tag.

### 3.5 Operational test for FL6 — regex / parse

The QC stream applies an automated FL6 detector before manual review.
The detector parses each labeller's `reasoning` text for the following
required tokens:

**Required position tokens (at least one occurrence of each, case-insensitive):**

- A token matching `\b(UTG|HJ|CO|BTN|SB|BB)\b` for each surviving villain
  named in the spot's `chain_fingerprint.callers_chain ∪
  {aggressor_pos, raiser_pos} \ {NONE}`.
- A token matching `\bhero\b` followed by or preceded by hero's position
  (within 8 words).

**Required relationship tokens (the response-target identification):**

The reasoning must contain at least one phrase matching this pattern
(any of the four variants is sufficient):

1. `facing\s+(\w+)['']?s?\s+(bet|raise|c-bet|donk)` — names aggressor/raiser
   and identifies the bet hero is facing.
2. `responding\s+to\s+(\w+)['']?s?\s+(bet|raise|action)` — explicit response
   framing.
3. `against\s+(\w+)['']?s?\s+(bet|raise|c-bet|range|continuing\s+range)` —
   targets villain's range.
4. `(\w+)\s+is\s+the\s+(aggressor|raiser|bettor|bettor-and-call-closer)` —
   explicit role assignment.

The captured group (`\w+`) MUST equal one of the position tokens
{UTG, HJ, CO, BTN, SB, BB}.

**Detector pseudocode (for builder reference):**

```
def detect_fl6(rationale_text: str, chain_fp: ChainFingerprint) -> bool:
    """Return True if rationale FAILS the FL6 test (i.e. label is rejected)."""
    POSITIONS = {'UTG', 'HJ', 'CO', 'BTN', 'SB', 'BB'}
    required_positions = (
        set(chain_fp.callers_chain)
        | {chain_fp.aggressor_pos, chain_fp.raiser_pos}
    ) - {'NONE'}

    # (A) all required positions named
    rationale_upper = rationale_text.upper()
    for pos in required_positions:
        if not re.search(rf'\b{pos}\b', rationale_upper):
            return True  # FL6 fail: missing villain

    # (D) response-target identified
    patterns = [
        r"facing\s+(\w+)['']?s?\s+(bet|raise|c-bet|donk)",
        r"responding\s+to\s+(\w+)['']?s?\s+(bet|raise|action)",
        r"against\s+(\w+)['']?s?\s+(bet|raise|c-bet|range|continuing\s+range)",
        r"(\w+)\s+is\s+the\s+(aggressor|raiser|bettor)",
    ]
    rationale_lc = rationale_text.lower()
    for pat in patterns:
        m = re.search(pat, rationale_lc, re.IGNORECASE)
        if m and m.group(1).upper() in POSITIONS:
            return False  # passes (D)

    return True  # FL6 fail: no response-target identified
```

This is testable, deterministic, and runs in O(len(rationale)) per spot.
The detector is run as part of the existing consensus pipeline at
`scripts/compute_4way_consensus.py` (added to the same per-spot pre-flight
gate that detects FL4 and FL5).

### 3.6 What FL6 does NOT require

Explicitly out of scope (to keep the test cheap and avoid false-positives):

- FL6 does NOT require the labeller to use the exact word "chain" or
  "fingerprint". The structural information is what counts.
- FL6 does NOT require enumerating villains who folded preflop (they
  are not in `chain_fp.callers_chain` and need not be named).
- FL6 does NOT require naming hero's position (that is FL5 territory —
  the action-space discipline test already covers position legality).
- FL6 does NOT replace the existing rationale word-count or template-
  uniqueness gates. It is additive.

### 3.7 Three worked examples — mandatory phrasing in context

The following examples show the AMENDMENT 3 phrasing integrated into the
existing per-hand reasoning structure. The mandatory-chain sentence is
**emphasized** for illustration; in production labels it appears as
unstyled prose.

---

**Example (a): Hero IP-closing facing single bet**

*Spot:* hand_id 4WL-CHAIN-101. Flop. Hero=BTN, hole cards AhJh.
Preflop: HJ opens 2.5bb, CO calls, BTN(=hero) calls, BB calls.
Flop board: Ks 7d 2c.
Action so far: SB folded preflop. BB checks, HJ bets 4bb into 11bb (36%).
CO has not yet acted (sequence is BB-checks → HJ-bets, hero faces; CO
to act AFTER hero per closing-action structure — error, fix: CO acts
between HJ and hero in closing-action sense; revise to: SB folds preflop,
flop seat order is BB-then-HJ-then-CO-then-BTN, BB checks, HJ bets, CO
calls 4bb, hero to act).

*Reasoning (250-400 words target):*

This is a 4-way SRP at flop decision with hero in IP-closing position.
**Hero (BTN) is facing HJ's c-bet of 4bb into 11bb, with CO as the prior
caller between HJ and hero (the chain is HJ-bets / CO-calls / hero). The
decision is against the bet-and-call composite range — primarily HJ's
c-betting range filtered through CO's continuing range as a secondary
narrower.**

Per-villain range chains:

- **HJ (opener + c-bettor)**: opens ~17% UTG-adjusted (HJ range), c-bets
  K-high ~70% at 36% sizing. K-high c-bet at this sizing is range-balanced
  → ~30% value (Kx, sets), ~25% strong gutters/back-door equity,
  ~45% air with overcards.
- **CO (cold-caller of HJ open + flat-caller of c-bet)**: range is
  capped pre (no 3-bet → no AK/AA/KK). On K-high flop, CO continues
  with K-x (rare), pair-plus-FD, and occasional gutter floats.
  Continuing range is ~40% value (Kx, sets, AA-overpair-rare),
  ~30% draws/equity, ~30% floats.
- **BB (closing-defender preflop)**: range very wide preflop; on K-high
  flop, BB x-folds most → effectively out of decision tree by this point.

Equity/range tensions: AhJh has top-pair-Jack-kicker on K-high (medium-made,
weak kicker against HJ + CO continuing ranges). Equity vs HJ continuing
range alone: ~42%. Vs CO continuing range alone: ~38%. Vs combined
(bet+call) range: ~37%. Pot odds 4 / 19 = 21%. Equity surplus ~16pp.

Bucket: medium_made in 4-way `BET_CALL` chain (chain_shape per blueprint
§3). Decision: CALL. Hero closes action this street; raising into a
value-skewed bet+call range as a kicker-vulnerable TPWK is dominated.
Folding gives up clear equity surplus + position. Adjacent alternatives:
RAISE (rejected — TPWK 4-way against a range with K-better kicker mass);
FOLD (rejected — 16pp equity surplus before realization is too cheap to
fold).

---

**Example (b): Hero OOP-early facing bet-call-raise sequence**

*Spot:* hand_id 4WL-CHAIN-247. Flop. Hero=SB, hole cards 8d8c.
Preflop: CO opens 2.5bb, BTN calls, SB(=hero) calls, BB calls.
Flop board: Jh 7c 4s.
Action: SB(=hero) checks, BB checks, CO bets 6bb into 11bb (55%),
BTN raises to 18bb. Hero to act.

*Reasoning:*

This is a 4-way SRP at flop with hero OOP-early; chain shape is
`BET_RAISE`. **Hero (SB) is facing BTN's raise to 18bb after CO's
initial bet of 6bb. The chain is CO-bets / BTN-raises (no caller
between CO and BTN in the raise sequence). The decision is against
BTN's raise range, with CO's continuing decision still pending behind
hero. Hero is responding primarily to BTN's raise, secondarily to
the structural pressure of CO acting after hero with a known bet
on the table.**

Per-villain range chains:

- **CO (opener + initial c-bettor)**: opens ~24% from CO. C-bets
  J-high two-tone ~60% at 55% sizing — range is value-skewed
  (overpairs, sets, J-x with good kicker, FD with overs).
- **BTN (cold-caller of CO open + raiser of c-bet)**: cold-call range
  pre is capped (no AK/AA/KK). On J-high two-tone, BTN's raise range
  is very narrow: sets (77, 44, JJ-rare since would 3-bet pre), strong
  two-pair (J7 — unlikely cold-call pre, but J4s combos exist), and
  semi-bluff combos with strong draws + blockers (e.g. T9-suited
  for OESD + over). Approximate composition: ~70% value (sets +
  strong made), ~30% semi-bluff equity. The raise narrows BTN to a
  tightly value-heavy range.
- **BB**: checked behind on flop without action; effectively folding
  / x-folding most of range. Will likely fold to the raise.

Equity/range tensions: pocket 8s is medium-made (middle pair) on
J-high. Equity vs BTN's raise range: ~22%. Pot odds to call BTN's
raise: 12 / (11+6+18+12) = 12/47 = 25.5%. Equity short ~3pp; plus
implied negative-EV from playing OOP on later streets with reverse
implied odds vs sets and overpairs.

Bucket: medium_made → weak in this chain → effectively pure folding
range. Decision: FOLD. The `BET_RAISE` chain with BTN as raiser
(range-capped, but raise narrows tightly to value) is one of the
strongest range-narrowing signals available 4-way. Adjacent
alternatives: CALL (rejected — equity short; OOP realisation factor
~0.75 makes it worse); RAISE (rejected — pocket 8s blocks nothing
relevant; semi-bluff raise into a 70%-value range loses big).

---

**Example (c): Hero OOP-middle in 3-bet pot multiway**

*Spot:* hand_id 4WL-CHAIN-318. Turn. Hero=CO, hole cards AsKs.
Preflop: UTG opens 2.5bb, CO(=hero) 3-bets to 8.5bb, BTN cold-calls,
SB cold-calls, BB folds, UTG calls. 4-way to flop with 35bb pot.
Flop board: Ks 8h 3d. Action: SB checks, UTG checks, CO bets 12bb
into 35bb (34%), BTN calls, SB folds, UTG calls.
Turn card: 5c. Action: UTG checks, CO(=hero) to act.

*Reasoning:*

This is a 4-way → 3-way 3-bet pot at turn with hero OOP-middle; chain
shape on the turn is `OPEN` (action checked to hero). **Hero (CO,
who 3-bet pre and c-bet flop) is the would-be aggressor on the turn
after UTG's check. The chain is UTG-checks / hero (no callers, no
raisers). The decision is whether to second-barrel into UTG and BTN's
continuing ranges; hero is responding to the implicit information
of UTG's flop call + turn check (induced or weak), and to BTN's flop
call (capped + position).**

Per-villain range chains:

- **UTG (opener + flop caller + turn checker)**: opens ~14% from UTG.
  Called CO's 3-bet pre (range capped — no AA/KK / no junk; ~JJ-TT,
  AQ, AK-rare, suited broadway sometimes). On K-high flop, called
  c-bet → continues with overpairs (QQ-JJ rare-because-cap, TT-99),
  K-x is rare in UTG 3-bet-call range, mostly underpairs + some
  back-door. Turn check after flop call: either pot-control with
  middle pair / under-pair OR x-c trap with set-rare.
- **BTN (cold-caller of CO 3-bet + flop caller)**: range very narrow
  pre (cold-call vs 3-bet ~3-5%): JJ-TT, AQs, suited connectors that
  flop well multiway. On K-high, BTN continues with TT-99-mid-pair,
  AQ-FD-pickups, and very rare K-x (KQs sometimes). BTN's range on
  the turn after flop call is capped and draw-heavy.
- **SB**: folded on flop; out of decision tree.

Equity/range tensions: AsKs is monster (top pair top kicker, A-high
flush draw on s on a non-spade board — wait, board is Ks 8h 3d 5c,
no flush draw for spades active yet; AsKs is TPTK with
back-door-flush-and-straight). Equity vs UTG turn-check range:
~75-80%. Equity vs BTN flop-call range on turn: ~70-75%.

Bucket: strong_made (TPTK) in `OPEN` chain (3-bet pot turn). Decision:
BET (33% sizing per solver-aligned turn sizing). Hero benefits from
betting for value (UTG's pot-control range continues; BTN's draws
continue) and from denying free river equity to BTN's draws.
Adjacent alternatives: CHECK (rejected — overcedes too much equity
vs BTN's draw-heavy range; UTG's checked range is mostly bluff-
catcher that calls one bet anyway); larger BET sizing (rejected
per solver-aligned 33% on turn unless polarized).

---

### 3.8 Pre-submission self-check addendum

Append the following items to the existing "Anti-rule-based self-check"
checklist in `data/4way_labeller_brief.md`:

- [ ] Every surviving villain at the decision moment is named by position
      in the reasoning (FL6 (A)).
- [ ] The aggressor on the current street is named, OR the street is
      explicitly identified as checked to hero (FL6 (B)).
- [ ] Prior callers between aggressor and hero are named in seat-order,
      OR explicitly stated as absent (FL6 (C)).
- [ ] The reasoning identifies which villain's action hero is responding
      to via one of the four canonical phrasings (FL6 (D)).
- [ ] No equity thresholds appear in the bucket-assignment phase
      (existing bucket-first compliance — unchanged).

If any of FL6 (A)/(B)/(C)/(D) cannot be checked, your label is rejected
at consensus regardless of action-correctness. The regex test in §3.5
runs automatically; a failed regex match flags the label as FL6 before
manual QC review.

### 3.9 Terminology cross-reference

Per `feedback_terminology_raise_vs_bet.md` (already binding in the brief):

- **bet** = first postflop action initiating aggression
- **raise** = action that raises an existing bet (postflop) OR raises a
  preflop open
- **open** = preflop opener

In chain-fingerprint terms:
- `aggressor_pos` is the **bettor** (first postflop bet) — call this
  villain "the bettor" or "the c-bettor" if they were also PFA.
- `raiser_pos` is the **raiser** — never call this the "bettor".
- `raise_target_pos` is the player whose **bet was raised** — refer to
  this villain's bet that the raiser raised.

A rationale that says "BTN raised the flop" when BTN is the
`aggressor_pos` (first postflop action) is a terminology defect distinct
from FL6 — it falls under the existing terminology rejection in the brief.

End of AMENDMENT 3.

---

## Builder ratification checklist for AMENDMENT 3

- [ ] §3.1 motivation cites BATCH-007 Opus dissents 312/323/352 correctly.
- [ ] §3.2 four mandatory requirements (A/B/C/D) cover the architect's
      intent for "name each villain + identify response-target".
- [ ] §3.4 FL6 placed alongside FL4 (rule-based) and FL5 (illegal action)
      in the defect taxonomy; consensus pipeline updated to compute FL6
      pre-aggregation.
- [ ] §3.5 regex / parse test is implementable in
      `scripts/compute_4way_consensus.py` without additional dependencies.
- [ ] §3.7 three worked examples cover the three target situations
      (IP-closing single bet, OOP-early bet-call-raise, OOP-middle
      3-bet pot multiway).
- [ ] §3.8 self-check items appended to existing brief checklist verbatim.
- [ ] No equity thresholds introduced in any new prose
      (bucket-first compliance preserved).
- [ ] Terminology §3.9 cross-references existing
      `feedback_terminology_raise_vs_bet.md` rule.

End DRAFT.
