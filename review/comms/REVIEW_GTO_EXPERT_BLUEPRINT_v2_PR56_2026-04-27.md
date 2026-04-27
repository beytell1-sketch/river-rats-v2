---
date: 2026-04-27
from: gto-expert (round 2 reviewer)
to: orchestrator → owner
re: Round 2 review of blueprint v2 at PR #56
verdict: APPROVE-WITH-NITS
---

# Round 2 gto-expert review — blueprint v2

## Preamble

Sources read before writing this review:
- Blueprint v2: `review/comms/BLUEPRINT_CORPUS_GENERATION_PIPELINE_v2_2026-04-27.md`
- Synthesis: `review/comms/MAIN_TERMINAL_BLUEPRINT_REVIEW_SYNTHESIS_2026-04-27.md`
- My round 1 review: `review/comms/REVIEW_GTO_EXPERT_BLUEPRINT_PR53_2026-04-27.md`
- KB: `knowledge/three_way_gto.md` (§§1.1–1.10)
- Protocol: `prompts/gto_labeller_v3.2.md`

Scope: poker-domain verification only. Engineering correctness of
scripts, disjointness protocol, and lock-file schema are not my
domain and are not assessed here.

---

## Q1 — Are my R3–R5 fixes correctly incorporated?

### R3: Module 4 truncated histories

**My round 1 finding:** MAGG-1/2/3 action histories were truncated at
the second bet (putting hero on the turn with `villain_aggression_count=1`),
not extended to the river decision point where `villain_aggression_count=2`.

**What the blueprint v2 says:**

The blueprint now explicitly states in Q2 Gap 3:

> To produce `villain_aggression_count=2`, the decision point must be on
> the **river**, after villain has bet both the flop and the turn.

And replaces the truncated action histories with corrected ones. MAGG-1
and MAGG-2 now show:
```
[('flop', 'CO', 'bet'), ('flop', 'BB', 'call'),
 ('turn', 'CO', 'bet'), ('turn', 'BB', 'call')]
```
Decision point: **river** (hero is BB, decides on river).

MAGG-3 shows a check-raise-flop + bet-turn sequence:
```
[('flop', 'BB', 'check'), ('flop', 'CO', 'bet'), ('flop', 'BB', 'raise'),
 ('flop', 'CO', 'call'), ('turn', 'BB', 'bet'), ('turn', 'CO', 'call')]
```
Decision point: **river** (CO/hero acts on river).

**Feature verification — do these histories produce `villain_aggression_count=2`?**

The feature `villain_aggression_count` counts prior-street bets. The
counting mechanism (per `game_state_bridge.py` lines 112-134 per blueprint
Q1 root-cause analysis) reads `game.street_actions` for prior streets
and counts villain bet events.

- MAGG-1/2: flop CO bet (street 1 aggression = 1) + turn CO bet (street 2
  aggression = 1) = `villain_aggression_count=2` at river decision. CORRECT.

- MAGG-3: flop BB check → CO bet → BB raise (this is BB check-raising,
  which is BB aggression) + turn BB bet. Here hero is CO. From CO's
  perspective: BB bet on flop (check-raise counts as 1 aggression event)
  + BB bet on turn = `villain_aggression_count=2` at river. CORRECT for CO.

**Are the sequences realistic 3-way play?**

MAGG-1/2 (CO bets flop, BB calls, CO bets turn, BB calls): YES. CO
c-bets a 3-way pot, BB overcalls the flop (this requires a connected BB
hand — medium pair or draw — to overcall without a BTN in the picture
if BTN folded). Then CO barrels turn with BB calling again. This is
standard multi-street continuation. The only mild concern: if BTN is
still in the pot when BB calls flop, BTN folding between streets must be
specified in the scenario template. The blueprint implies 3-way heads-up
(CO vs BB) by the action history structure, which is realistic if BTN
folds preflop or the flop. No issue.

MAGG-3 (BB check-raises flop, CO calls, BB bets turn, CO calls): YES.
The BB check-raising a CO c-bet in a 3-way pot is a legitimate line —
BB's check-raise range on most boards is strong (it has to be 3-way,
per KB §1.7 which notes check-raises are near-nuts 3-way per DO NOT Rule
3 in v3.2). BB then betting the turn after a check-raise shows extreme
strength — this is a realistic but rare sequence (check-raise for value,
then barrel). CO calling the check-raise implies CO has a strong hand
(TPTK+ to continue in this spot). The sequence is real. A minor note:
from the teaching perspective, MAGG-3 produces a river spot where CO
faces a likely river bet from BB after two streets of BB aggression — the
correct CO response is almost certainly FOLD for non-monsters. This is
exactly the lesson the MAGG module is designed to teach. REALISTIC.

**R3 verdict: CORRECTLY INCORPORATED.** The corrected action histories
produce `villain_aggression_count=2` at river decision points as
required. The sequences are genuine 3-way lines. The assert in the
blueprint's Step 3 validation (`all(r['feat_dict']['villain_aggression_count'] == 2 for r in magg_records)`)
is the right programmers' gate.

One residual nit: MAGG-1 and MAGG-2 have IDENTICAL action histories in
the blueprint (they differ only by "variant in board texture and hero
hand class"). The blueprint should make this explicit — these are the
same structural template, intentionally varied by hero hand class and
board. This is fine for the corpus (variation is across board texture
and hero holdings, not action structure), but the programmer should be
told explicitly that MAGG-1 and MAGG-2 share the same action template.

---

### R4: NFD boundary validation (±0.03 tolerance)

**My round 1 finding:** After generating NFD boundary hands, verify
actual computed `villain_air_pct` against target. My recommendation was
to discard/replace hands that miss by more than 0.03.

**What the blueprint v2 says:**

The blueprint adds a mandatory post-generation validation step in Q4:
> `|actual_villain_air_pct - target_villain_air_pct| <= 0.03`
> Failure action: filtered out and replaced before corpus assembly.

**Is ±0.03 the right tolerance?**

The 5 target values are: 0.15, 0.17, 0.20, 0.22, 0.25. The critical
boundary is at 0.20 (the KB §1.7 OVERRIDE threshold).

- A hand targeted at 0.17 (CALL) that computes as 0.21 (outside ±0.03
  would be 0.14-0.20) lands in the RAISE bucket — wrong label. At ±0.03,
  0.17 ± 0.03 = [0.14, 0.20]. A computed value of 0.20 exactly is on
  the boundary — ambiguous. This is the tightest tolerance that prevents
  mislabelling: a value of 0.20 at the CALL target is borderline, but
  the protocol default for mixed/boundary is CALL, so it errs correctly.

- A hand targeted at 0.22 (RAISE) that computes as 0.18 (outside
  ±0.03 from 0.22 = [0.19, 0.25]) would be accepted at 0.19 but should
  arguably be CALL not RAISE. At ±0.03 this is caught.

- The adjacent boundary pair (0.17 CALL vs 0.20 RAISE) has only a 0.03
  gap between them. ±0.03 tolerance means these two hands' valid ranges
  touch (0.17 + 0.03 = 0.20 = 0.20 - 0.00). This is the tightest
  possible pairing with no overlap.

**Should it be ±0.02 or ±0.05?**

±0.05 is too loose. A hand targeted at 0.15 (CALL) could compute as
0.20 (RAISE) and pass the ±0.05 gate — wrong label on a boundary case.

±0.02 would be tighter but may cause too many regeneration cycles. The
`villain_air_pct` feature depends on range model calculations; a ±0.02
tolerance on a continuous computed feature from probabilistic range
models may be unreachable without extremely controlled board/position
parameters. Regeneration loops add compute complexity.

**My assessment: ±0.03 is the correct tolerance.** It is the maximum
tolerance that prevents cross-boundary mislabelling given the 0.20
threshold and 0.03 gaps between adjacent targets. ±0.02 would be
overly strict given the computational precision of the range model.

The blueprint's validation placement (pre-labelling gate in corpus
assembly, after NFD pool generation) is correct. Hands that fail
validation are replaced before entering the Phase A quota.

**R4 verdict: CORRECTLY INCORPORATED. Tolerance of ±0.03 is appropriate.**

---

### R5: Rule 11 boundary textures — 5 specified textures

**My round 1 finding:** The blueprint specified only one board type for
all 5 Rule 11 boundary pairs, risking a spurious board-texture confound.
Required: ≥3 different board textures.

**What the blueprint v2 says:**

The blueprint now specifies all 5 textures explicitly:

| Pair | Texture | Example board |
|------|---------|---------------|
| 1 | Dry paired | KcKd4s (rainbow) |
| 2 | 2-tone paired | KdTd4c |
| 3 | Dynamic paired (connected) | 8h8d7c |
| 4 | Monotone | 9h6h3h |
| 5 | Draw-heavy paired | JsTd4d |

**Are these genuinely distinct textures (not minor variations)?**

YES. These are substantively different board types:
- KcKd4s is a statically dominated board (paired Broadway). Villain's
  range on this board is heavily bifurcated: either connected to the K
  or has none.
- 8h8d7c is dynamic — connected pairs create two-pair and straight
  possibilities that generate different range evolution than K-high pairs.
- 9h6h3h is monotone — the entire flush texture changes villain's draw
  vs. value composition dramatically.
- JsTd4d is two-tone with medium connectivity — different from the
  K-high boards and the monotone board.
- KdTd4c sits between dry-paired and draw-heavy — a 2-flush broadway
  paired board.

All 5 are genuinely distinct. There are 3 explicitly different board
families: K-high paired (Pairs 1 and 2), connected/dynamic paired (Pair 3),
and non-K-high textured boards (Pairs 4 and 5). This satisfies the ≥3
texture requirement from R5. I would count it as 5 distinct textures for
the purpose of preventing single-texture confounds.

**Is each texture GTO-meaningful for the Rule 11 threshold (villain_tp+_pct at 0.40)?**

The Rule 11 threshold governs OOP hero's bet-vs-check decision with a
medium-strong made hand when villain's range composition is at the
boundary between "enough value to extract from" and "too air-heavy."

Let me check each:

**Pair 1: KcKd4s (dry paired, rainbow)**

On a board where the community pair is a Broadway card (KcKd), villain's
`villain_top_pair_plus_pct` includes: sets of 4s, trips (Kx for villain),
and two-pair. Villain connecting to K-high pairs is position-dependent:
a BB defender has Kx in range; a BTN opener has many Kx combos. The
0.40 threshold is meaningful here: at <0.40 villain's range has mostly
air (missed overcards, small pairs that didn't pair the board in the high
K-K-4 texture). At >=0.40 villain has enough Kx combos to extract value
from. GTO-MEANINGFUL.

**Pair 2: KdTd4c (2-tone paired)**

Villain now has flush draws (Xd-Xd combos) in addition to Kx pair
combos. This makes the TP+ threshold less about pure value density and
more about whether villain's range has both value AND draws. At <0.40,
villain's range is draw-heavy (diamonds without a pair) and folds to
hero's OOP bet. At >=0.40, villain has enough Kx and TT-type hands to
call. The threshold remains meaningful but for a different reason (value
to call vs. draw-only range that folds). GTO-MEANINGFUL.

**Pair 3: 8h8d7c (dynamic paired, connected)**

This is the most important test case for Rule 11. On 8h8d7c:
- Villain's range includes 8x (trips), 77 (full house already), sets of 7s,
  straight draws (9x, 6x, 5x-9x connectors), and air (broadway overcards).
- The `villain_top_pair_plus_pct` here captures a fundamentally different
  composition than the K-high boards: villain's "top pair" equivalent is
  trips/FH, but villain's draws and air are also elevated on this dynamic
  board.
- At <0.40 on 8h8d7c, villain's range is draw-heavy (straight draws,
  overcards) and a hero OOP bet to protect is actually LESS warranted
  (villain folds draws, hero loses value). At >=0.40, villain has enough
  made hands (trips, straight completes, 77) to justify an OOP bet.
- This is GTO-MEANINGFUL but the reasoning is subtly different from
  K-high boards: it's about protection vs. fold equity on a dynamic board,
  not pure value extraction. The model learning this texture alongside
  K-high textures is valuable.

**Pair 4: 9h6h3h (monotone)**

Rule 11 on a monotone board is an interesting edge case. The primary
concern on a monotone board is flush completion — villain's range is
sharply bifurcated into flush-draws/made-flushes vs. off-suit non-flush
hands (air on this texture). The `villain_top_pair_plus_pct` on 9h6h3h
would include hero holding a 9 or flush; villain holding a 9x would be
"top pair" on a monotone board.

One concern: Rule 11 as specified in v3.2 targets paired and 2-tone
boards. The v3.2 text says "DO NOT Rule 11 added (paired-board /
2-tone-flush-board OOP CHECK exception)." A monotone board (3-of-a-suit)
is not a "2-tone flush board" in the standard sense — it's a completed
flush board. The applicable rule for a monotone board is different: hero
OOP must be careful about betting with non-flush hands because villain
may have made the flush.

**FLAG:** The monotone board (Pair 4) may not map cleanly to Rule 11's
paired/2-tone-flush scope. The GTO reasoning for CHECK vs BET on 9h6h3h
is not primarily about `villain_top_pair_plus_pct` at 0.40 — it's about
whether villain has the flush. The pair of 9s is not present on this
board. Rule 11 as written applies to PAIRED boards. A monotone board is
not paired and is not a 2-tone board — it is a 3-flush board.

This is a NIT, not a blocker, because:
1. The model learning texture-dependent behaviour is still valuable.
2. The blueprint's GTO rationale for this board (villain's range
   "dramatically split: flush combos vs. offsuit holdings") is correct
   poker reasoning, even if it's not Rule 11 per se.
3. The programmer implementing this texture will produce realistic hands
   that will teach something real about monotone boards.

However: the label for monotone-board hands may not be consistently
captured by Rule 11's threshold. A labeller applying v3.2 to a hand
on 9h6h3h with OOP hero is likely to apply Rule 1 (flush board danger)
or general range reasoning, not Rule 11 specifically. This means the
boundary pair on the monotone board may produce labels that don't align
with the Rule 11 BET/CHECK structure, undermining the boundary-pair
teaching goal.

**Recommendation:** Replace Pair 4 (monotone 9h6h3h) with a genuinely
paired board in a different connectivity regime — e.g., 6s6d2c (low dry
paired) or Th9h8h is also problematic. A better replacement: **7s7d2c**
(low dry paired, rainbow) — this creates a different K-high dry paired
context while being a genuinely paired board where Rule 11 clearly
applies. The 5 boards would then span: K-high paired dry, K-high paired
2-tone, mid paired connected, low paired dry, draw-heavy paired — all
Rule 11-applicable textures.

Alternatively, if the architect wants to retain a 3-flush board as
texture variety (reasonable for general corpus diversity), the monotone
board should not be labelled as a Rule 11 boundary pair but as a general
OOP decision pair. Keep 4 boards as Rule 11 boundary pairs and 1 board
as a general OOP composition pair. The blueprint should be explicit
about this distinction.

**Pair 5: JsTd4d (draw-heavy paired, two-tone)**

Wait — JsTd4d is not a paired board. It has J, T, 4 — three distinct
ranks. This is a connected two-tone board, NOT a paired board. Rule 11
explicitly applies to "paired-board / 2-tone-flush-board" contexts.
JsTd4d is a 2-tone board (diamonds), which falls within the "2-tone-
flush-board" half of Rule 11's scope. However, the blueprint labels it
"draw-heavy paired" — it is NOT paired. The 4 does not pair any other
card on JsTd4d.

**FLAG (more serious than Pair 4):** JsTd4d is mislabelled as "paired"
in the blueprint's texture table. This board is a connected two-tone
board — the closest real-world analog to what generates Rule 11
violations is when the board has pairs AND texture. JsTd4d has texture
but no pair.

The board KcKd4s has a pair (the Kings). JsTd4d has no pair. Both can
generate Rule 11-appropriate decisions, but the "paired" label for Pair
5 is incorrect.

This is not just a labelling error in the blueprint document — it matters
for the programmer who implements `generate_rule11_boundary_scenarios.py`.
If the programmer follows the "draw-heavy paired" label and constructs a
paired board with draw-heavy texture, they will use a different board
than JsTd4d. If they follow the example board JsTd4d, they'll use a
connected two-tone board. The blueprint is inconsistent.

**Required correction:** Fix Pair 5's texture label. Options:
- If the intent is a draw-heavy paired board: use **Js4d4c** (paired
  4s with two-tone texture and medium connectivity) or **TsTs7d** (paired
  tens with connected lower card).
- If the intent is a connected two-tone board (unpaired): change the
  label from "draw-heavy paired" to "connected two-tone" and keep JsTd4d.

Either is GTO-meaningful for Rule 11's 2-tone-flush-board scope, but
the blueprint must be internally consistent.

**R5 verdict: PARTIALLY CORRECTLY INCORPORATED.** The 5-texture
requirement is met in spirit — these are genuinely distinct board types.
However, Pair 4 (monotone 9h6h3h) is outside Rule 11's explicit
paired/2-tone scope, and Pair 5 (JsTd4d) is mislabelled as "paired"
when the board has no pair. Both are nit-level concerns but should be
corrected before the programmer implements `rule11_boundary_scenarios.py`.
The mislabelling of Pair 5 as "paired" is the more operationally
important fix since it creates ambiguity for the programmer.

**Nit required before programmer handoff: clarify Pair 5 texture label
(paired vs. unpaired two-tone). Pair 4 monotone texture should be noted
as outside Rule 11's paired-board scope (it still produces a useful OOP
decision pair, just not a strict Rule 11 boundary pair).**

---

## Q2 — Is Module 8 (donk-bet defence) realistic 3-way play?

**Spec:** Hero IP (BTN or CO), facing OOP BB donk lead on flop after PFA opens preflop. Action history: preflop CO raise, BTN call, BB call (3-way). Flop: BB leads into CO and BTN (donk bet from OOP non-PFA).

**Are donk-leads by BB realistic at meaningful frequency in 3-way single-raised pots?**

YES, but frequency context matters. In modern GTO play, the BB donk-lead
frequency in 3-way single-raised pots is approximately 15-25% of flop
decisions (varying significantly by board texture). This is non-trivial —
it is not a rare or exploitative line but a standard GTO response on
specific board types where the BB's range hits disproportionately.

Boards where BB donks at high frequency:
- Low connected boards (5-4-2, 6-4-3): BB's speculative preflop range
  (small pairs, suited connectors) smashes these boards while CO's
  opening range has very few nutted combinations. BB donks to protect
  equity, not surrender it.
- Monotone boards that favour BB's wide preflop holdings over CO's
  linear opening range.

Boards where BB donks rarely:
- High dry boards (A-K-x rainbow): CO's c-bet range crushes this
  texture. BB donking on A-K-8r into CO's range-dominant position is
  near-zero GTO frequency.

**What hand classes does BB donk with in real GTO play?**

The donk-lead range is moderately polarised:
- Strong: two-pair, sets, flush draws on 2-flush boards (BB leads to
  protect strong draws that can't allow free cards to CO/BTN).
- Semi-bluff: combo draws, nut flush draws (BB's speculative preflop
  range generates nut FDs on low boards).
- A small number of air hands: some balanced bluffs to prevent
  exploitation.

The blueprint's description of "polarised — either strong (sets, two-pair,
top pair on specific boards) or air" is directionally correct. However,
in GTO play the donk range is not a pure polar 2-bucket strategy —
there is a substantial semi-bluff component (draws) alongside value.
"Air" as the second pole understates the semi-bluff density. The
labelling for donk-defence hands should account for BB's draw-heavy
semi-bluff component, not just air.

**Does the Module 8 spec accommodate the realistic donk-lead range?**

The spec says:
> "BB's donk-betting range is polarised — either strong (sets, two-pair,
> top pair on specific boards) or air (low equity hands leading to deny
> equity)."

The "air (low equity hands leading to deny equity)" description is
slightly off. In GTO donk strategy, the "air" component consists of
hands that can't realize equity by checking (they'll face a c-bet they
can't continue, so they lead as a bluff). The "deny equity" framing
belongs to value bets, not bluffs. This is a subtle description error
but doesn't break the module — the structural feature (`facing_bet=1`,
OOP bettor, hero IP) will be correctly coded regardless of the verbal
description.

More importantly: the spec says hero's IP "uncapped range can respond
with CALL / RAISE / FOLD depending on hero hand strength and villain's
donk range composition." This is accurate. All three options are live:

- FOLD: Hero has air or weak made vs. BB's donk range (which is stronger
  than a c-bet range — donker is showing initiative with a non-trivial
  holding). Hero's air hand folds.
- CALL: Hero has a medium-made or draw hand that has equity vs. BB's
  donk range but not enough to raise. The pot is now 3-way (CO is still
  in), complicating the call.
- RAISE: Hero has a monster (set, two-pair) or the nut FD with side
  equity. Raising the donk serves dual purposes — builds the pot and
  folds out CO's remaining range.

One important distinction the blueprint doesn't explicitly address: in
Module 8 as specified, CO is also still in the pot after BB donks. Hero
(BTN or CO) is not the ONLY remaining opponent. If hero is BTN, CO may
still act behind (CO has yet to respond to the donk). This creates a
true sandwich dynamic for the BTN — BTN is calling/raising with CO still
to act. The blueprint's action history shows BB donk, then hero (BTN or
CO) faces the bet. If hero is CO, hero acts before BTN; if hero is BTN,
CO acts first.

**Clarification needed for programmer:** In the action history
`[('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'), ('preflop', 'BB', 'call'), ('flop', 'BB', 'bet')]`:
- If hero is CO: hero acts first facing the BB donk (with BTN behind).
  This is a sandwich dynamic where hero CO must consider BTN's reaction.
- If hero is BTN: hero acts last (CO has already responded to the BB
  donk, either calling or folding). Hero BTN faces a bet and possibly a
  call.

Both scenarios are realistic, but they produce different feature values.
The hero-as-CO scenario (BTN still behind) is the more complex teaching
case. The hero-as-BTN scenario (after CO response) has a known
`num_callers_to_bet` value. The blueprint should specify which scenarios
cover which hero position, since the `num_callers_to_bet` feature value
differs.

**Decision tree realism — are CALL/RAISE/FOLD all live options?**

YES:
- FOLD is live: Hero IP folds the donk-defence when holding air vs. a
  polarised donk range (even IP, a hand with no equity folds to a bet).
- CALL is live: Hero IP calls with medium-made or moderate draws,
  especially if SPR is high enough to realize equity.
- RAISE is live: Hero IP raises monsters or nut-draw combos to build the
  pot and fold out CO (if CO is behind hero).

The 3-way RAISE question in donk-defence is more complex than in facing-
a-c-bet: hero is raising into the donker (showing strength) while CO is
still live and potentially strong. A raise here requires near-monster
strength or a very strong semi-bluff (nut FD + side equity). RAISE
frequency in this spot is lower than in facing-a-c-bet, but it is
non-zero. This will naturally produce a distribution that is more
CALL/FOLD-heavy and RAISE-light compared to other facing-bet modules —
appropriate for the corpus.

**Module 8 verdict: REALISTIC.** The donk-lead occurs at meaningful
frequency (15-25%) in GTO play on specific boards. The decision tree is
genuine. Two nits for the programmer: (1) clarify which hero position
(CO or BTN) acts in which order relative to the donk, as this affects
`num_callers_to_bet` and the sandwich dynamic; (2) the "air" description
of BB's donk range should acknowledge the semi-bluff (draw) component,
not just air bluffs.

**Scenario spec coverage:** 25 mandatory Phase A hands from 80 pool
hands is adequate for this module. A 3:1 pool-to-corpus ratio is
appropriate given the board-texture selectivity needed (only 3-way pots
on BB-favourable boards produce realistic donk-lead scenarios).

---

## Q3 — Is Module 9 (SB-as-hero sandwich) realistic?

**Spec:** Hero in SB, sandwiched between earlier-position aggressor and
later-position caller. Action history: CO opens, BTN calls, SB calls,
BB folds, flop: CO bets into SB (hero) and BTN.

**Is the SB MDF estimate (~20%) correct?**

YES. The KB §1.1 confirms:
> "Sandwich player (action behind): defends ~20%, folds ~80%"

SB in this scenario (CO bet, BTN behind SB) is the sandwich position —
SB must consider that BTN may raise if SB calls, increasing SB's
effective cost. The ~20% MDF for the sandwich position is the correct
order of magnitude. For context:
- BB in standard position (closing action) defends ~40%.
- SB facing a bet WITH BTN behind is the canonical "must fold more"
  position, confirmed by §1.5's EQR data (sandwich position = worst
  seat, must fold more).

The 20% is a round figure; real solver output shows SB MDF in this
configuration at 18-24% depending on board texture and specific ranges.
The blueprint using ~20% as the pedagogical anchor is correct.

**What's the realistic action sequence that puts SB as decision-maker?**

The blueprint specifies:
```
[('preflop', 'CO', 'raise'), ('preflop', 'BTN', 'call'),
 ('preflop', 'SB', 'call'), ('preflop', 'BB', 'fold'),
 ('flop', 'CO', 'bet')]
```
SB acts on the flop facing CO's c-bet with BTN behind.

This is correct and common in live 3-way play. CO opens, BTN cold-calls
(BTN's calling range is capped — excludes premiums that would 3-bet),
SB cold-calls behind BTN (SB must have a fairly strong speculative hand
to call two players with position behind), BB folds. The 3-way flop is
CO vs BTN vs SB with CO first to act, typically c-betting.

**Key GTO asymmetry:** SB is the worst seat at the table:
- OOP to both CO (the PFA) and BTN (IP player).
- BTN is yet to act behind SB — SB cannot close the action by calling.
- SB's preflop range (calling CO + BTN) is stronger than BB's calling
  range (BB overcalls a CO+BTN build) — SB needed a real hand to cold-
  call 3-way.

This produces a scenario where SB has a relatively strong preflop range
(required to cold-call), tighter continuing standards due to position,
and systematically higher FOLD rates than BB would have in the same
structural situation. These are distinct poker dynamics that warrant
dedicated corpus coverage.

**Does ~20 Phase B hands provide useful signal?**

Phase B (45 total hands) gets ~20-25 SB-hero hands from the mandatory
Phase A quota. These 20-25 hands come from 70 pool hands. This is an
adequate number to teach the SB's tighter MDF and the systematic fold-
leaning at this position, given that:
- The feature `hero_position = SB` provides explicit positional signal.
- The key teaching points (fold more than BB, consider BTN behind, 20%
  MDF) are learnable from 20+ examples if the feature distributions are
  properly varied across hand classes and board textures.
- SB is currently ~3% of the existing corpus. Adding 20-25 SB hands to
  a 500-hand corpus brings it to ~4-5% (20 / 500) — still below real-
  world SB frequency (~17%) but a meaningful improvement over 3%.

The blueprint's variants are appropriate:
- Hands where BTN has already folded (pure SB-vs-CO with no sandwich).
- Hands where BTN is yet to act (true sandwich).
- Hands where SB faces a BTN c-bet (not CO, different PFA).

These cover the range of SB-hero structural configurations.

**One observation:** The blueprint notes SB MDF ~20% vs BB MDF ~33%.
This means Module 9 should produce a materially higher FOLD rate than
any other facing-bet module. If the programmer generates the 70 SB-hero
pool hands and the labelled hands show FOLD at <30%, something is wrong
with the scenario specs — SB should be folding at very high rates
relative to other positions. This could be added as a soft assertion:
"FOLD rate in Module 9 labelled hands should exceed 30%."

**Module 9 verdict: REALISTIC.** The ~20% MDF is correct. The action
sequence is accurate for SB sandwich scenarios. 20-25 Phase A hands
provide adequate signal given explicit positional features.

---

## Q4 — Are the 3 deferred LOW-severity patterns affected by the new modules?

The 3 deferred patterns from my round 1 review:
- Pattern B (turn/river check-raise response as PFA): LOW-MEDIUM
- Pattern C (river overbet response): LOW
- Pattern D (blocker-driven bluff/fold, KB §1.10): LOW

Newly added modules: Module 8 (donk-bet defence) and Module 9 (SB sandwich).

**Does adding Module 8 make Pattern B (turn check-raise as PFA) more important?**

NO. Module 8 adds IP hero facing OOP donk — this is distinct from hero-
as-PFA facing a check-raise. The donk-bet and the check-raise are
structurally different (donk: villain leads before hero acts; check-raise:
villain checks, hero bets, villain raises). Adding donk defence does not
create a gap that makes check-raise defence more urgent. Pattern B
remains LOW-MEDIUM.

**Does adding Module 9 make Pattern C (river overbet) more important?**

NO. Module 9 adds SB-as-hero in a sandwich position facing an initial
bet. River overbets are a sizing-driven pattern (bet_to_pot > 1.2) that
can occur in any position. The SB module does not create a gap that
makes river overbet coverage more urgent. Pattern C remains LOW.

**Does adding either new module make Pattern D (blocker-driven bluff) more important?**

Marginally. Module 8 (donk defence) involves hero IP facing a donk on
draw-heavy boards — exactly the boards where `flush_draw_block_pct`
and `straight_draw_block_pct` features are most relevant (KB §1.10).
Hero IP facing a BB donk on a 2-flush board where hero holds a flush-suit
card is precisely the defender-negative blocker scenario documented in
KB §1.10.2. Module 8 will generate some of these hands naturally.
However, the module spec doesn't explicitly target the KB §1.10 blocker-
direction mechanism. If the programmer generates Module 8 hands on
2-flush boards without specifying hero's suit holdings, some hands may
exercise the blocker mechanism and some may not.

**Recommendation:** Pattern D escalates from LOW to LOW-MEDIUM in the
context of Module 8. The donk-bet defence scenarios on 2-flush boards
naturally interact with the blocker-direction signal. I recommend that
when Module 8 scenarios are generated on 2-flush boards, at least 5
hands explicitly have hero holding a card in the flush suit (to generate
`flush_draw_block_pct > 0`) — this provides some Pattern D coverage as
a byproduct of Module 8 without requiring a dedicated Pattern D module.

**Summary on deferral:**

| Pattern | Prior severity | Updated severity | Deferral still appropriate? |
|---------|---------------|-----------------|---------------------------|
| B (PFA check-raise) | LOW-MEDIUM | LOW-MEDIUM | YES |
| C (river overbet) | LOW | LOW | YES |
| D (blocker-driven) | LOW | LOW-MEDIUM | YES, but add 5 blocker-explicit hands to Module 8 |

All 3 deferral decisions remain appropriate. Pattern D's severity
creep to LOW-MEDIUM is addressable within Module 8's existing 80-hand
pool budget without adding a new module.

---

## Q5 — Are OQ-4 and OQ-5 GTO-relevant or technical-only?

### OQ-4: `_opener_position` reconstruction from `prior_actions`

**GTO impact if reconstruction fails:**

If `prior_actions` in the existing 100-hand JSONL does not include
preflop actions, reconstruction fails and all re-extracted hands retain
`is_preflop_aggressor=0`. The GTO impact:

The existing 100 hands are predominantly non-PFA decisions (per the
blueprint's Q1 root-cause analysis — the existing pool has structural
deficit of PFA coverage). The re-extraction is needed primarily to fix
SPR (which is corrupted for 94/100 hands) and secondarily to fix
`is_preflop_aggressor`. If IS_PFA remains 0 for all 100 re-extracted
hands, this is acceptable because:

1. The 100 hands were drawn from the existing pool which structurally
   has very few PFA decisions — if those hands are genuinely non-PFA,
   IS_PFA=0 is CORRECT for them.
2. If the handful of hands that are genuinely PFA decisions remain
   mis-labelled IS_PFA=0, the model encounters 5-10 PFA training examples
   with incorrect IS_PFA feature. This is a minor accuracy degradation,
   not a structural confound — the 400 new hands provide the primary
   PFA training signal.
3. The SPR correction (the primary fix) is what prevents the regime-split
   confound. IS_PFA correction is the secondary benefit.

**Are those hands still useful as training examples even if IS_PFA can't be reconstructed?**

YES. The 100 existing hands are training examples for CHECK/BET decisions
with OOP position and late-street timing. Even with IS_PFA=0 (wrong for
~30 hands), the hands teach valid decision patterns. The SPR-corrected
values mean the model won't treat those hands as a distinct compressed-
SPR regime. The pedagogical value is intact.

**OQ-4 assessment: GTO impact is LOW if reconstruction fails. SPR fix
is the critical re-extraction; IS_PFA correction is bonus. Proceed with
Path A regardless of OQ-4 outcome; if reconstruction fails, document in
the lock file and accept IS_PFA=0 for the 100 re-extracted hands.**

### OQ-5: Phase B at 45 vs Phase A at 355

**Is 45 Phase B hands sufficient for a competent 3-way teaching corpus?**

The Phase B stratified fill serves distributional broadening — it fills
gaps in the 8-dimension cell space not covered by Phase A's targeted
modules. Phase A's 355 hands cover:
- PFA c-bets (80 hands)
- Facing initial bets, NFD, monsters (70 hands)
- BAC and MAGG (90 hands)
- SPR variation (90 hands)
- Rule 11 boundaries (10 hands)
- Modules 8 and 9 (45 hands)

These are all high-information, targeted scenarios. Phase B's 45 hands
add distributional entropy — spots that Phase A wouldn't naturally
generate (e.g. mid-SPR turn decisions with medium-made hands on draw-
heavy boards, or BB OOP check decisions in low-action pots).

**Does 45 Phase B hands under-represent the rare classes I flagged in audit Q5?**

My audit Q5 identified rare-class under-representation across several
dimensions. Phase A's mandatory quotas address most of these directly.
The remaining gap from Phase B shrinkage (90→45) is the distributional
fill for non-targeted configurations. The cell-space math in the
blueprint (2592 cells from 8 dimensions, 45 hands = ~57 cells covered)
is correct — Phase B cannot exhaustively cover the space. But Phase A's
structured coverage ensures the model sees all the important patterns;
Phase B adds noise reduction and generalization.

**The real concern is whether the FOLD and RAISE rare classes are
adequately covered by Phase A.** Checking:
- RAISE: 20 NFD RAISE + 20 monster-facing-bet + some PFA RAISE = ~50+ RAISE
  from Phase A. Target is 56 for 400 new hands. Phase A alone provides
  enough RAISE-eligible hands.
- FOLD: 20 MW-50 FOLD + 20 MAGG FOLD = 40 FOLD from Phase A. Target is
  48 for 400 new hands. Phase B provides the remaining 8 FOLD hands
  from its 45-hand fill. Achievable.

**OQ-5 assessment: 45 Phase B hands is sufficient given Phase A's
targeted coverage. The rare-class targets (RAISE 56, FOLD 48) are
achievable within Phase A's quotas. Phase B's reduced scope is an
acceptable trade for the 45 hands allocated to Modules 8 and 9.**

---

## Q6 — Calibration set additions update

**Blueprint disposition:** The recommendation to add 1-2 MAGG FOLD
calibration hands is noted in the OQ-3 handoff: "Include 1-2 MAGG FOLD
calibration hands before labellers encounter the multi-street aggression
river fold in the main corpus."

This is a CORRECT and sufficient disposition. The Tier 1 architect is
the right agent to specify the exact calibration hands — this blueprint
is about corpus generation, not calibration set design. The handoff
note ensures the recommendation is transmitted.

**Is deferral to "Tier 1 architect handoff" appropriate?**

YES, with one clarification: "handoff" should mean the Tier 1 architect
receives and acts on this recommendation BEFORE mass Tier 2 labelling
begins. The synthesis's OQ-3 resolution confirms Tier 1 runs in parallel
with Tier 2, not as a strict gate. However, the MAGG FOLD calibration
hands specifically should be available before labellers encounter MAGG
scenarios in Tier 2 — otherwise labellers will produce 20+ MAGG FOLD
hands without calibration exposure to the pattern.

**The timing question:** If Tier 1 expansion runs in parallel and MAGG
FOLD calibration hands are not ready when labellers hit the MAGG section
of Tier 2, the calibration benefit is lost. This argues for sequencing
the MAGG FOLD calibration addition as early as possible within the
parallel Tier 1 expansion.

**My recommendation:** The blueprint should strengthen the handoff note
to: "MAGG FOLD calibration hands (1-2) should be added to Tier 1 BEFORE
or simultaneous with the first labelling batch of MAGG scenarios in Tier 2.
Tier 1 architect to schedule accordingly." This does not change the
concurrent structure but makes the timing dependency explicit.

**The blueprint as written leaves this timing implicit — a minor
clarification nit, not a blocking issue.**

---

## Q7 — Final verdict on v2

### APPROVE-WITH-NITS

The blueprint v2 is a materially improved document. R3 (MAGG truncation)
and R4 (NFD validation) are correctly incorporated and GTO-sound. The 5-
texture requirement from R5 is met in spirit, with two labelling
inconsistencies that the programmer must not blindly implement (Pair 4
is outside Rule 11's paired-board scope; Pair 5 is mislabelled as "paired"
when JsTd4d has no pair). Modules 8 and 9 are realistic 3-way scenarios.

This blueprint is ready for programmer handoff subject to the following
required fixes:

---

## Verdict + specific changes

### APPROVE-WITH-NITS

**Required before programmer handoff (nits that affect implementation
correctness):**

**N1: Pair 5 in Rule 11 boundary scenarios — fix the "paired" mislabel.**
JsTd4d has no pair. The blueprint labels it "draw-heavy paired" but the
board is connected-two-tone, not paired. The programmer implementing
`rule11_boundary_scenarios.py` will be confused. Either:
- (a) Replace JsTd4d with a genuinely paired draw-heavy board (e.g. JsJs4d,
  but that eliminates one rank — better: **TsTs7d** or **8s8d7c** variant
  if 8h8d7c is used as Pair 3). Recommendation: use **JsJd4c** (paired
  Jacks with some texture) — a board not already used in pairs 1-4, and
  genuinely paired.
- (b) Change the label to "connected two-tone (unpaired)" and keep JsTd4d.
  Then explicitly document that 2 of 5 boundary pairs are on unpaired 2-
  tone boards (still within Rule 11's "2-tone-flush-board" scope).

Option (b) is simpler and preserves a diverse set. The blueprint should
make this explicit.

**N2: Pair 4 in Rule 11 boundary scenarios — document scope exception.**
The monotone board 9h6h3h is outside Rule 11's "paired / 2-tone-flush"
scope. The labellers may not apply Rule 11 to this board — they may
apply flush-board danger logic (Rule 1 or general reasoning). The
blueprint should either:
- (a) Replace 9h6h3h with a paired board (e.g. **6s6d2c** — low dry
  paired, different from the K-high Pairs 1-2 and the mid-connected
  Pair 3). This preserves 5 Rule 11 boundary pairs.
- (b) Keep 9h6h3h but explicitly note: "This board is included for
  monotone texture diversity; labellers should apply flush-board OOP
  reasoning, not Rule 11 specifically. The boundary pair tests
  `villain_top_pair_plus_pct` at 0.40 in a monotone context, which
  exercises general OOP BET/CHECK judgment rather than Rule 11 strictly."

Option (a) is cleaner for the Rule 11 teaching objective. Option (b)
preserves texture diversity at the cost of Rule 11 purity.

**N3: Module 8 — clarify hero position (CO vs BTN) and action order
relative to the donk.**
In the action history `[('flop', 'BB', 'bet')]`, if hero is CO, BTN
is still behind hero. If hero is BTN, CO has already acted. The
programmer must know: for hero-as-CO hands, `num_callers_to_bet` is
0 at hero's decision point (no one has called yet when CO faces the
donk); for hero-as-BTN hands, `num_callers_to_bet` is 0 or 1 depending
on whether CO called or folded the donk. Specify this explicitly in the
module description or the scenario spec template.

**N4: Module 8 — donk range description should include semi-bluffs.**
The blueprint says BB's donk range is "polarised — either strong or air."
In real GTO play, the donk range also includes a substantial semi-bluff
component (draw hands that can't check and allow free cards). This
description affects how labellers reason about the hands. Add "or strong
semi-bluffs (nut flush draws, combo draws on 2-flush boards)" to the
donk range description for labeller guidance.

**N5 (timing, not blocking): Module 9 — add soft assertion for FOLD rate.**
FOLD rate in Module 9 labelled hands should exceed 30% (SB's tighter
~20% MDF vs. BB's ~33% implies folding more than any other facing-bet
module). If the labelled Module 9 hands show FOLD < 30%, investigate
whether the scenario specs are generating hands that are too strong for
the SB position (SB cold-calling preflop requires some hand quality,
but the hand quality must not be so high that SB rarely folds postflop).
Add this as a post-labelling verification note.

### Recommended (should add, not required):

**R6: Pattern D blocker-explicit hands in Module 8.**
When generating Module 8 scenarios on 2-flush boards, include at least
5 hands where hero explicitly holds a card in the flush suit (creating
`flush_draw_block_pct > 0`). This provides Pattern D (blocker-driven)
corpus coverage as a byproduct of Module 8 without a new module. Specify
in `donk_bet_defence_scenarios.py`: 5+ hands where hero_cards include
one card of the flush suit on boards with 2 of that suit.

**R7: MAGG-1/2 distinction clarification in the blueprint.**
MAGG-1 and MAGG-2 share the same action template — explicitly note this
in the scenario descriptions to prevent programmer confusion. The
variation is board texture and hero hand class, not structural.

**R8: MAGG FOLD calibration timing — strengthen handoff note.**
The OQ-3 handoff note should state explicitly that MAGG FOLD calibration
hands (1-2) must be added to Tier 1 before or simultaneously with the
first Tier 2 labelling batch that includes MAGG scenarios, not just
"as part of Tier 1 expansion" generically.

---

### Summary

| Item | Category | Blocking? |
|------|----------|-----------|
| R3 incorporated correctly | VERIFIED | — |
| R4 incorporated correctly (±0.03 appropriate) | VERIFIED | — |
| R5 Pair 4 scope exception (monotone outside Rule 11) | N2 | Yes (programmer may mislabel) |
| R5 Pair 5 mislabelled as "paired" | N1 | Yes (programmer ambiguity) |
| Module 8 action order (CO vs BTN) | N3 | Yes (affects feature generation) |
| Module 8 donk range description | N4 | No (labeller guidance only) |
| Module 9 realistic and MDF correct | VERIFIED | — |
| Module 9 FOLD rate soft assertion | N5 | No (post-labelling check) |
| OQ-4 GTO impact if reconstruction fails | LOW | No |
| OQ-5 Phase B at 45 adequate | ADEQUATE | — |
| MAGG FOLD calibration timing | R8 | No (timing risk only) |
| Pattern D escalation | R6 | No (within Module 8 budget) |
| Deferral of B/C/D patterns | CONFIRMED | — |

The blueprint v2 is APPROVED with N1, N2, and N3 requiring correction
before programmer handoff. N4/N5/R6/R7/R8 are recommended but not
blocking.

*Review complete. No code written. No blueprint modified.*
