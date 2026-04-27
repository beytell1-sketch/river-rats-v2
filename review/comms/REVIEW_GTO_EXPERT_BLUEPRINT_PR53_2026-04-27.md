---
date: 2026-04-27
from: gto-expert (independent reviewer)
to: orchestrator → owner
re: Re-review of blueprint at PR #53 (BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md)
verdict: APPROVE-WITH-NITS
---

# gto-expert re-review — corpus-generation pipeline blueprint

## Preamble

This review is poker-domain focused. The blueprint's engineering design
(Mode A / Mode B generation, disjointness protocol, lock file schema) is
evaluated only where the poker content depends on the engineering
decision. Architecture feasibility is the architect's domain; I review
what the generated hands will look like, whether the scenarios are
real, and whether the boundary cases will teach the model what they
claim to teach.

Sources read before writing this review:
- Prior audit: `AUDIT_GTO_EXPERT_ACTION_DISTRIBUTION_2026-04-27.md`
- Synthesis: `MAIN_TERMINAL_CORPUS_REVISION_SYNTHESIS_2026-04-27.md`
- Blueprint under review: `BLUEPRINT_CORPUS_GENERATION_PIPELINE_2026-04-27.md`
- KB: `knowledge/three_way_gto.md` (§§1.1-1.11)
- Protocol: `prompts/gto_labeller_v3.2.md`

---

## Q1 — Do the 7 scenario modules cover the zero-coverage patterns my audit flagged?

My prior audit identified four zero-coverage poker patterns:
1. Bet-and-call sequences (3-way fold-pressure)
2. Free-card protection (sets on draw-heavy boards)
3. Multi-street equity realisation (linked decisions)
4. Nut-blocker RAISE facing bet (KB §1.7 / MW-39 pattern)

**Assessment per pattern:**

**Pattern 1: Bet-and-call sequences** — Covered by `bac_scenarios.py`
(Scenarios BAC-1, BAC-2, BAC-3). The blueprint's BAC template is
structurally correct: one villain bets, a second villain calls, hero
faces a bet-and-call with `num_callers_to_bet=1`. The synthesis targets
≥15 instances; the blueprint allocates 20 mandatory quota slots in
Phase A. COVERED.

**Pattern 2: Free-card protection** — Partially addressed but not
explicitly named as a scenario module. The blueprint's
`facing_initial_bet_scenarios.py` and `magg_scenarios.py` will generate
some boards where villain has draw-heavy ranges, but there is NO dedicated
protection-bet scenario module. Protection betting is the canonical
spot where hero holds a monster (set, straight) on a dynamic board and
must bet to deny free cards to flush/straight draws — this is a CHECK
vs BET decision where hero is NOT facing a bet, is NOT the PFA per se,
and the motivation is equity denial rather than value extraction or
fold equity. This pattern does NOT map cleanly to any of the 7 named
modules. The PFA scenarios cover c-bet decisions where hero opened, but
the protection-bet pattern also arises for the caller/BB who flops a set
and must lead into draw-heavy texture.

VERDICT ON PATTERN 2: **PARTIALLY COVERED, GAP REMAINS**. The blueprint
generates facing-bet hands and PFA c-bet hands, but the specific
combination (non-PFA hero, monster strength, draw-heavy board, protection
motivation) is absent as a dedicated target. Some protection-bet hands
will emerge from the general self-play Mode A pool if the SPR is correct,
but they are not guaranteed. I flag this as a NIT rather than a blocker
because protection-bet reasoning is partially captured via PFA-3 and
PFA-4 (aggressor protecting on dynamic boards), and the Mode A self-play
with correct SPR should produce some non-PFA protection scenarios.
Recommend adding 10-15 explicitly designed "non-PFA monster on draw-heavy
board" scenarios to `facing_initial_bet_scenarios.py` or as an 8th module.

**Pattern 3: Multi-street equity realisation** — Addressed by
`magg_scenarios.py` (MAGG-1, MAGG-2, MAGG-3). The blueprint's MAGG
template correctly tracks `villain_aggression_count >= 2` across two
streets. Multi-street equity realisation (BB trapping then extracting)
is partially addressed. However: the MAGG scenarios primarily model
hero facing villain's multi-street aggression (a defensive
multi-street response), not hero's own multi-street betting plan
(trap → extract across streets). These are different poker decisions.
The trapping side (hero checks monster, villain bets, hero calls, now
what on turn?) is not explicitly modelled. This is also a NIT since
most corpus spots are single-street snapshots; full linked multi-street
is beyond the scope of the 500-hand corpus. COVERED (defensively),
PARTIALLY MISSED (proactive multi-street trap).

**Pattern 4: Nut-blocker RAISE facing bet** — Covered by
`nfd_scenarios.py` (NFD-RAISE, NFD-CALL). The blueprint produces
both sides of the KB §1.7 threshold, with 5 boundary hands at
`villain_air_pct` 0.15, 0.17, 0.20, 0.22, 0.25. This is the most
important pattern from my audit, and it is the most thoroughly
addressed. COVERED.

**Summary:** 3 of 4 zero-coverage patterns are adequately covered.
Pattern 2 (protection bet) is the remaining gap. Add ~10 hands to
address it.

---

## Q2 — Do the 7 scenario modules produce REAL poker situations or synthetic feature-condition spots?

I assess each module for poker realism.

### Module 1: PFA c-bet scenarios (pfa_scenarios.py)

**Scenarios PFA-1 through PFA-4 — Action history plausibility:**

CO raises → BTN calls → BB calls is the most common 3-way scenario in
live and online play. Realistic. BTN opens → SB + BB call is somewhat
less common (squeeze situations are more common from SB/BB vs BTN
opens), but fully plausible. HJ opens → CO + BB call is standard.

**Range realism concern:** In PFA-1 (CO opens, BTN and BB call), the
blueprint says "range of hero hand classes (air through monster)." This
is correct — the CO opening range of ~27-28% contains air (K-high
nothing), draws (suited connectors), medium made (TPTK on some boards),
and monsters (sets). The feature distributions should be realistic
because `feature_extractor` computes villain compositions from actual
preflop range models.

**SPR realism:** The blueprint targets SPR 6-8 for PFA flop decisions by
using `pot=12.5` to `pot=25.0` (BB units). A standard CO open to 3bb,
BTN call, BB call creates a 9bb pot. SPR = 100/9 ≈ 11.1. The blueprint's
target pot of 12.5bb produces SPR = 100/12.5 = 8, which is realistic.
At 25bb pot (likely a 3-bet preflop that went slightly above that), SPR
= 4. Both are within realistic ranges for 3-way pots. REALISTIC.

**One concern:** PFA-4 is a TURN c-bet decision (hero checks flop, villain
checks flop, hero faces turn decision as PFA who checked flop). This
is an unusual action pattern: a PFA who checked flop vs two opponents
now leading the turn. The action history "preflop CO raises, BTN calls,
BB calls, flop all check, turn CO leads" is real but uncommon (only ~10%
of flop-checked PFA decisions involve a PFA turn-lead). It should be in
the corpus but should not be over-represented. Flag: keep PFA-4 to
≤10 hands.

**Verdict for Module 1: REALISTIC.**

### Module 2: Facing initial bet scenarios (facing_initial_bet_scenarios.py)

The blueprint defines these as "initial-bet response decisions." This is
the most important module for CALL/RAISE/FOLD coverage.

**Poker realism concern:** The blueprint notes that in the existing pool,
ALL 27 facing_bet hands are also facing_raise hands, because self-play
generates check-raises more than initial bets. The factory module fixes
this by explicitly constructing situations where villain bets first. The
action history must show only a villain bet with no prior check from
villain on that street. This is CORRECT poker mechanics: villain c-bets
into hero (most common facing-bet scenario in real play).

**Range realism concern:** The blueprint says villain composition features
(`villain_top_pair_plus_pct`, `villain_air_pct`, etc.) are computed by
`feature_extractor` using the preflop range model. For a CO c-bet into
BTN + BB on a K-high dry board, the features should correctly show high
`villain_top_pair_plus_pct` (CO opened with many Kx hands) and low
`villain_air_pct`. This is realistic.

**Risk 3 in the blueprint (factory features may be plausible in isolation
but not jointly):** This is a legitimate concern. On a low connected board
(5-6-7), if hero specifies CO as opener and sets `villain_air_pct=0.45`,
the extractor may accept this but it is NOT realistic — CO's range doesn't
have 45% air on 5-6-7 (CO c-bets this board with K-high air having very
low fold equity). The blueprint flags this and recommends gto-expert
review of 20-30 factory hands before mass generation. I SECOND this
recommendation strongly.

**Verdict for Module 2: CONDITIONALLY REALISTIC** — valid if gto-expert
reviews 20-30 samples before mass generation, per blueprint Risk 3.

### Module 3: Bet-and-call sandwich scenarios (bac_scenarios.py)

**Action history:** BTN bets, SB calls, hero (BB) faces. This is
textbook sandwich position. The action history
`[('flop', 'BTN', 'bet'), ('flop', 'SB', 'call')]` is exactly how
this situation arises in real play. PLAUSIBLE.

**Range realism:** After a BTN c-bet and SB cold-call, both villain ranges
narrow significantly. The BTN's betting range is value-weighted; the SB's
calling range is fairly strong (SB is calling in sandwich position between
BTN and BB, requiring a stronger hand to flat than the BB would). The
`villain_top_pair_plus_pct` should be elevated for both villains. The
`feature_extractor` models this correctly if the position-specific range
narrowing is implemented.

**Critical question:** Does `feature_extractor` correctly model that in a
bet-and-call situation, both villain ranges have narrowed? The feature
`villain_top_pair_plus_pct` aggregates across both opponents. In a
real BAC scenario, BTN's betting range is ~60% TP+ but SB's calling
range is ~40% TP+; the aggregate is somewhere between them. If the
extractor treats them uniformly, the features will still be directionally
correct (the combined range is stronger than a single-villain c-bet into
uncalled), even if not precisely calibrated.

**BAC-3 (villain_aggression_count >= 1 PLUS bet-and-call):** This is a
very tight continuing standard spot — hero is last to act facing a bet
AND a call from a multi-street aggressor AND a caller. In real GTO play,
hero needs close to the nuts to continue. This pattern is important for
teaching the compounding range-narrowing effect. REALISTIC.

**Verdict for Module 3: REALISTIC.**

### Module 4: Multi-street aggression scenarios (magg_scenarios.py)

**MAGG-1 (villain bets flop AND turn, hero faces river):**

Action history for MAGG-1 as specified: `[('flop', 'CO', 'bet'),
('flop', 'BB', 'call'), ('turn', 'CO', 'bet')]`. This means hero (BB)
called the flop bet, then faces a turn bet. Hero faces turn, not river.
There's a notation inconsistency in the blueprint — MAGG-1 says "hero
faces river decision" but the action history has the turn bet as the last
action. This may mean hero is making a CALL/FOLD decision on the turn
with `villain_aggression_count=1` (flop bet), not on the river with
`villain_aggression_count=2`. The blueprint is ambiguous here.

**Clarification needed:** The `villain_aggression_count` feature counts
prior-street bets, not current-street bets. After villain bets flop and
hero calls, on the turn: `villain_aggression_count=1` (one prior-street
bet). After hero calls the turn bet and we're on the river: 
`villain_aggression_count=2` (two prior-street bets). MAGG-1's target of
`villain_aggression_count=2` is a RIVER decision. The action history
should include the river as the decision point, not just the turn bet.
This is a TECHNICAL ERROR IN THE BLUEPRINT that the programmer must
not implement literally. The scenario must extend to the river.

**MAGG-2 and MAGG-3** have the same issue. The `villain_aggression_count`
target of 2 implies a river decision after two prior-street bets, but
the action histories shown only go up to the second bet (which would
put hero on the turn, `villain_aggression_count=1`).

**This is a NIT that must be fixed before implementation.** The
programmer should clarify: MAGG scenarios with `villain_aggression_count=2`
require the decision point to be on the river, with the action history
showing flop bet + call + turn bet + call + river (hero's decision).

**Verdict for Module 4: REALISTIC poker pattern, but TECHNICAL ERROR
in action-history construction. Requires correction before programming.**

### Module 5: Nut-FD facing bet (nfd_scenarios.py)

**NFD-RAISE and NFD-CALL:** Hero holds [Ah, Xh] on a board with 2+ hearts.
This is precisely the KB §1.7 pattern. The hero cards and board are
explicitly specified, guaranteeing `nut_flush_block=1` and
`has_flush_draw=1`. The villain_air_pct values are set to either >=0.20
(RAISE) or <0.20 (CALL).

**Range realism concern:** Is it realistic for `villain_air_pct >= 0.20`
on a board where villain has c-bet? On a K-high 2-heart board (Kh-8h-3d),
the CO opener who c-bets has a range including Kx (value), flush draws
(semi-bluff), and some air (unimproved AJ/QJ type hands that c-bet as
bluffs). The feature_extractor's air estimate depends on position and
board texture. On a K-high 2-flush board, CO's c-betting air is
relatively low because CO connects well to this board (many Kx hands).
The `villain_air_pct >= 0.20` requirement may require either using a
position where villain connects less well to the board, or using a more
connected board where CO has more whiffs.

**Recommendation:** For NFD-RAISE scenarios, prefer boards where villain's
position is BB (wider, more air) or use lower boards (7h-4h-2d) where
opener's air fraction is naturally higher. This ensures the villain_air
feature value is realistic rather than forced.

**The boundary cases (villain_air_pct at 0.15, 0.17, 0.20, 0.22, 0.25):**
GTO-meaningful? YES. The KB §1.7 OVERRIDE threshold at villain_air=0.20
is solver-verified (per v3.2 Calibration Notes). The action does genuinely
flip at this boundary: below 0.20, fold equity is insufficient for the
raise to be +EV; above 0.20, fold equity pushes the raise above EV.
These are NOT arbitrary arithmetic boundaries — they reflect real game-
tree EV calculations. BOUNDARY CASES ARE GTO-MEANINGFUL.

**Verdict for Module 5: REALISTIC, with the recommendation to choose
boards/positions that naturally produce villain_air >= 0.20.**

### Module 6: Monster facing initial bet (monster_facing_bet_scenarios.py)

**Blueprint says:** Hero holds a set or better (`is_monster=1`). Villain
bets (first bet on the street, so `facing_raise=0`).

**Poker realism:** Monster facing an initial bet (not a check-raise) is
completely standard. A BTN who bets into a BB who has flopped a set is
one of the most important 3-way RAISE spots. The MW-33 calibration
anchor is exactly this pattern. REALISTIC.

**Action frequency concern:** In real 3-way play, the monster-facing-
initial-bet RAISE occurs ~3-5% of decisions (roughly: monsters are ~5%
of range, facing-bet is ~25% of spots, monster × facing-bet × RAISE ≈
1-1.5%). The blueprint allocates 20 Phase A mandatory slots to this
pattern. 20 monster-facing-bet hands from 400 new = 5% of new hands.
This is a SLIGHT OVERREPRESENTATION of the raw frequency, but it is
appropriate oversampling for a minority class. The model needs these 20
to learn the pattern, even though real frequency is lower. The calibration
note: if 20 RAISE hands from monsters are added and the model predicts
RAISE on real-distribution monster hands at 50%, that oversampling
effect is already accommodated by the synthesis's calibration plan.

**Verdict for Module 6: REALISTIC.**

### Module 7: Rule 11 boundary scenarios (rule11_boundary_scenarios.py)

**Target:** Paired/2-tone boards, OOP made hand, villain_top_pair_plus_pct
crossing the 0.40 threshold (CHECK default vs BET override).

**GTO-meaningful?** Rule 11's 0.40 threshold is the boundary between
"villain has enough value in range for hero's strong-made hand to extract
from" (BET override fires) and "villain has too little value for hero's
strong-made to BET into without tipping range and folding out villain's
bluff-catchers" (CHECK default). This is a genuine GTO boundary rooted
in polarisation theory: on paired/2-tone boards, betting medium-strong
hands OOP folds out villain's bluff-catchers while isolating against
villain's few value hands. At villain_top_pair_plus >= 0.40, the value
extraction compensates for the bluff-catcher fold-out. At villain_top_pair_plus
< 0.40, it doesn't.

**Is the 0.40 threshold solver-verified?** The KB adopts the threshold
from teaching context, tagged as "provisional pending calibration." The
v3.2 rule encodes the empirical failure on d3688 and d9556 (both
incorrectly BET by labellers). The threshold was not explicitly solver-
calibrated at 0.40 — it was set as the boundary that explains those
specific failures. This means the boundary cases near 0.35-0.45 may
be GTO-meaningful at a range around 0.40, but the exact number is not
definitively solver-proven.

**The training implication:** If the corpus teaches 5 pairs of hands
where only `villain_top_pair_plus_pct` differs across 0.40, the model
will learn a crisp decision boundary at exactly 0.40. In reality, GTO
play likely mixes across a band (0.35-0.45) rather than a sharp flip.
This is acceptable for a classification model — we must pick a boundary,
and 0.40 is the best estimate we have. The risk is that the model
over-generalises the 0.40 cutoff to situations where it doesn't apply
(HU, IP, non-paired boards). Mitigation: include board texture and
position as context in the boundary pairs (vary across the 5 pairs to
prevent spurious boundary generalisation).

**Verdict for Module 7: GTO-MEANINGFUL, with the caveat that the boundary
is provisional, not solver-exact. Acceptable for v3.0.**

---

## Q3 — Boundary cases for v3.2 rule triggers — are they GTO-meaningful?

### KB §1.7 OVERRIDE: villain_air_pct >= 0.20 threshold (NFD scenarios)

**5 boundary hands at villain_air_pct = 0.15, 0.17, 0.20, 0.22, 0.25:**

- Just-inside trigger (0.20, 0.22, 0.25): RAISE. GTO-meaningful — the
  action genuinely flips to RAISE above the threshold per solver-verified
  finding in MW-39 correction.
- Just-outside trigger (0.15, 0.17): CALL. GTO-meaningful — fold equity
  insufficient per v3.2 Calibration Notes.

**ARE THESE ARBITRARY FEATURE-ARITHMETIC BOUNDARIES?** No. The 0.20
threshold is solver-grounded (matches the MW-30 CALL anchor where
villain_air = 0.15 was insufficient). The action does genuinely flip at
this boundary. The model learns a real boundary, not an invented one.

**One technical concern:** `villain_air_pct` is computed by
`feature_extractor` from a range model, not directly specified by the
SituationFactory. The scenario specification must produce the target
`villain_air_pct` value from realistic game parameters (position, board,
prior action) rather than directly injecting it. If the extractor produces
villain_air_pct=0.09 for a scenario intended to have 0.15, the hand
lands in the wrong bucket. This requires gto-expert validation of each
boundary hand's computed feature values after generation.

**Recommendation:** After generating the 10 boundary NFD hands, verify
the actual computed villain_air_pct and discard/replace any that land
more than 0.03 away from the target.

### Rule 11: villain_top_pair_plus_pct >= 0.40 threshold

**5 pairs of hands (10 total):**

- Just-inside (>= 0.40): BET override. GTO-meaningful — villain has
  enough value to extract from.
- Just-outside (0.35-0.39): CHECK default. GTO-meaningful — villain
  has too little value.

Same concern as above: `villain_top_pair_plus_pct` is computed, not
specified. Verify actual values after generation.

**Additional concern:** The blueprint does not specify how many of the
5 boundary pairs are at the SAME board texture. If all 5 pairs are on
KdTd4s-type boards (2-tone, K-high), the model may learn "2-tone K-high
paired board → threshold at 0.40" rather than "any paired/2-tone board →
threshold at 0.40." Recommend varying board textures across the 5 pairs
(at least 3 different board types).

### v3.2 as a whole — rules without explicit boundary coverage

The blueprint's Phase A mandatory quota (310 of 400 new hands) includes
boundary cases for KB §1.7 and Rule 11, but does NOT explicitly list
boundary cases for:

- **MW-30 CALL threshold:** The synthesis specifically calls out the
  equity-surplus CALL despite bet-and-call. The BAC scenarios cover the
  MW-30 pattern but do not include just-below-threshold hands (hero has
  equity just below the MW-30 call threshold → FOLD). Recommend: 3-5
  FOLD contrast cases in the BAC scenarios where hero's equity is below
  pot odds despite the bet-and-call.

- **MW-50 FOLD threshold:** The blueprint allocates 20 MW-50 FOLD hands
  (medium_made facing raise + aggression). But the boundary with CALL
  (stronger made hand in similar situation) is not explicitly covered.
  Recommend: 5 contrast CALL cases where hero has trips+ facing the same
  raise + aggression situation.

- **MW-33 RAISE threshold:** Monster facing initial bet (20 hands). The
  boundary with CALL (strong made but not monster, facing initial bet)
  is important — TPTK facing a bet should be CALL not RAISE per v3.2.
  Recommend: 5 contrast CALL cases (TPTK facing initial bet) alongside
  the 20 RAISE cases.

These are NITS. They do not block the blueprint but should be added to
the Phase B stratified fill guidance.

---

## Q4 — Action distribution — does it reflect real 3-way play?

**The synthesis-adopted target: CHECK 30% / BET 27% / CALL 17% / RAISE 14% / FOLD 12%.**

For 500 total hands: 150 CHECK / 135 BET / 85 CALL / 70 RAISE / 60 FOLD.

**My prior audit recommended:**
CHECK 35% / BET 30% / CALL 12% / FOLD 10% / RAISE 13%.

**Difference vs synthesis:**
- CALL: synthesis 17% vs my 12% — synthesis is slightly higher
- FOLD: synthesis 12% vs my 10% — synthesis is slightly higher
- CHECK: synthesis 30% vs my 35% — synthesis is 5pp lower
- BET: synthesis 27% vs my 30% — synthesis is 3pp lower
- RAISE: synthesis 14% vs my 13% — essentially the same

**Is 14% RAISE realistic?** In real 3-way play, RAISE is ~3-6% of
decisions. At 14%, the corpus is oversampling RAISE by ~2.5-4.5x.

Is this a calibration problem? YES, but it is the CORRECT type of problem.
The synthesis explicitly addresses this: oversampling rare classes is
necessary for XGBoost to form reliable leaves, and the model will use
class_weight adjustments during training. The calibration risk (model
over-predicts RAISE on real-distribution data) is mitigated by:
1. The reference gate using real 3-way data (not the training distribution)
2. Class_weight adjustments during training
3. The 70 RAISE labels providing enough signal for tree formation, which
   cannot happen at natural frequency (15-30 RAISE labels in 500 hands)

**GTO verdict on distribution:** The 14% RAISE target is an engineering
necessity, not a claim about real-play frequency. This is the correct
approach. The synthesis's action distribution is APPROPRIATE for a
warm-start training corpus.

**One calibration concern:** FOLD at 12% (60 hands) is likely achievable
within facing-bet contexts, but the synthesis notes "some FOLD on opener
decisions (river-checked-to spots or strong-range check-folds)." In real
3-way play, FOLD without facing a bet is rare (hero would CHECK, not
FOLD). FOLD on opener decisions should be zero or near-zero (only
possible if there was a prior-street bet hero is now deciding to
continue calling — which is technically facing a bet). Verify that FOLD
labels only appear on hands with `facing_bet=1` or `facing_raise=1`.
If FOLD appears on `facing_bet=0` hands, it suggests a labelling error
in the existing 100 hands that carries into the combined corpus.

---

## Q5 — Patterns the blueprint MISSES that should be in the corpus

Beyond the 7 modules explicitly designed, these spot types are absent
from the blueprint's deliberate coverage:

### Missing Pattern A: Donk-bet defence (IP player facing a donk lead)

In 3-way play, the non-PFA who is IP frequently faces a donk bet from
the OOP player. Hero (CO/BTN, IP, not the PFA) faces a lead from the
BB/SB. This is a CALL/RAISE/FOLD decision where hero's range is typically
uncapped (IP caller). This situation is entirely absent from the blueprint's
7 modules — the facing-initial-bet module covers facing c-bets, but
donk bets have a very different range composition (donker is usually
OOP, showing a polarised range of either monsters or air).

**How to address:** 5-10 hands in the `facing_initial_bet_scenarios.py`
module where the bettor is OOP (BB leads into IP hero). These are not
c-bet situations; the action history would show no preflop PFA for the
BB, and the BB is betting into position.

### Missing Pattern B: Turn check-raise by villain (hero is PFA, check-raised on turn)

The blueprint covers check-raises for HERO (facing_raise=1 situations),
but doesn't specifically address the turn check-raise dynamic. On the
turn, after hero c-bet the flop and barrelled the turn, a check-raise
from villain is almost exclusively the nuts (per KB §1.3 and DO NOT Rule
3). Hero must FOLD nearly everything. This is an important teaching
pattern for the multi-street fold decision. The MAGG scenarios partially
cover it via check-raise history, but the sequence (hero PFA, flop bet,
turn bet, villain check-raise on turn) is not explicitly modelled.

**How to address:** 3-5 MAGG scenarios where hero is PFA, bet two streets,
then faces a villain check-raise on the turn or river. Expected label:
FOLD (air/weak made) or CALL (monster). Near-universal FOLD for non-
monsters is the teaching point.

### Missing Pattern C: River overbet response

The blueprint does not cover the river overbet decision. Villain bets
more than pot on the river (~1.5-2x pot). This is a polarised sizing
suggesting villain has either the absolute nuts or pure air. Hero's
decision becomes a pure bluff-catch (equity vs pot odds is at extremes,
and the composition quad becomes the primary reasoning tool). This is a
real and frequent spot in 3-way play that produces distinctive CALL/FOLD
patterns different from standard-sized bets.

**How to address:** 5-8 `facing_initial_bet_scenarios.py` hands where
`bet_to_pot >= 1.2` (river overbet). Hero must decide whether to CALL
or FOLD based on the composition quad. Some with CALL (villain's range
is bluff-heavy given overbet) and some with FOLD (villain's range is
value-heavy given overbet + position).

### Missing Pattern D: Blocker-driven bluff (KB §1.10 defender-side)

KB §1.10 documents the `flush_draw_block_pct` and `straight_draw_block_pct`
defender-side effect (densification toward value when hero blocks villain's
draws). This is specifically modelled in the 59-feature contract with
features 56-59. The corpus should have hands that exercise this logic,
but no module targets it. A hand where hero blocks villain's draws AND is
deciding CALL/FOLD is the teaching case for the densification effect.

**How to address:** 5-8 `facing_initial_bet_scenarios.py` hands on
two-tone boards where hero holds a card in the flush suit (not the nut
blocker — a mid-suit card that creates `flush_draw_block_pct >= 0.3`)
AND hero is deciding between CALL and FOLD with a marginal made hand.

### Missing Pattern E: SB-squeeze decision as preflop decision carrier

The blueprint notes SB is severely underrepresented (3 hands, 3% of
existing corpus). The blueprint's OOP/IP target (55-65% OOP / 35-45% IP)
doesn't specifically address SB representation. SB decisions have unique
dynamics: SB is OOP to the table, faces action from BTN bets behind them
if BTN is still live, and has a sandwich-like defending standard (~20% MDF).
The blueprint's PFA scenarios include "BTN opens, SB + BB call" (PFA-2)
but hero in PFA-2 is the BTN (PFA), not the SB. The SB is a villain.

There are no scenarios where hero IS the SB facing a bet from the BTN
or CO. Recommend: 10-15 scenarios with hero in SB position, facing an
initial bet from BTN (or CO) with a caller behind (BB). This captures
the sandwich dynamic where SB has worst position and tightest continuing
standard.

**Severity:** MEDIUM. SB dynamics are materially different from BB and
BTN. Without SB examples, the model cannot learn the SB's tighter
continuing standard and MDF.

### Summary of missing patterns

| Pattern | Severity | Estimated hands needed |
|---------|----------|----------------------|
| A: Donk-bet defence (IP facing OOP lead) | MEDIUM | 5-10 |
| B: Turn/river check-raise response as PFA | LOW-MEDIUM | 3-5 |
| C: River overbet response | LOW | 5-8 |
| D: Blocker-driven bluff/fold (KB §1.10) | LOW | 5-8 |
| E: SB sandwich decisions as hero | MEDIUM | 10-15 |

Total estimated hands to add: 28-46. These can mostly come from the
Phase B stratified fill (90 hands), but Pattern A and E should be
elevated to Phase A mandatory quota consideration.

---

## Q6 — Are the calibration set additions (Tier 1 33→45) GTO-targeted correctly?

**Synthesis plan:** Add 5-8 facing-bet reversals + 2-4 FOLD reversals
+ 1-3 c-bet pattern hands to bring Tier 1 from 33 to 45 hands.

**My assessment:**

**Facing-bet reversals (5-8 hands):** These must cover the KB §1.7 RAISE
pattern (nut FD + villain_air >= 0.20), the MW-30 CALL pattern (equity
surplus overrides bet-and-call), and the MW-33 RAISE pattern (set facing
initial bet). These are exactly the right additions — they are the
solver-verified patterns that are completely absent from the current Tier
1 calibration set. CORRECT.

**FOLD reversals (2-4 hands):** The synthesis says "over-fold-bias
diagnostic spots." These should be hands where the labeller's instinct
is to FOLD but the correct action is CALL (equity surplus over pot odds)
or hands where FOLD is correct but requires confirming the range-narrowing
logic. MW-50 (medium made facing raise + aggression) is the canonical
FOLD calibration anchor. Adding 2-4 new FOLD anchors where facing_raise=1
AND villain_aggression_count >= 1 is appropriate. CORRECT.

**C-bet pattern hands (1-3 hands):** Rule 4 PFA c-bet decisions.
The synthesis recommends adding these to the calibration set before
labellers encounter them in the 400-hand main corpus. This is essential
— labellers who have never seen a PFA c-bet calibration anchor will
misapply Rule 4 on the first 100 PFA c-bet hands in the corpus.

**Gap I would add:** No calibration hands are proposed for the
multi-street aggression fold (MW-50 extension: after villain bets two
streets, medium made FOLD on river). The existing MW-50 anchor is a
specific spot; the new MAGG scenarios will produce many variants.
Recommend: 1-2 calibration hands explicitly testing multi-street
aggression fold on the river (villain_aggression_count=2, hero medium
made, FOLD). This ensures labellers apply the MAGG fold logic correctly
before encountering it in 20+ hands in the main corpus.

**Revised Tier 1 expansion:**
- 5-8 facing-bet reversals (KB §1.7, MW-30, MW-33): AS SPECIFIED
- 2-4 FOLD reversals (over-fold-bias diagnostic): AS SPECIFIED
- 1-3 c-bet pattern hands (Rule 4 PFA): AS SPECIFIED
- 1-2 multi-street aggression fold (MAGG pattern): ADD THIS

Revised Tier 1 target: 46-48 hands (up from the synthesis's 45 target).
The extra 1-3 hands are worth the minor cost increase.

---

## Q7 — Does the existing-100 vs new-400 mix create teaching-distribution issues?

**Beyond the ml-architect's confound concern, is there a poker-pedagogical issue?**

YES. There is a genuine poker-pedagogical asymmetry that the blueprint's
Risk 7 only partially addresses.

The existing 100 hands are:
- 100% `is_preflop_aggressor=0` (no PFA decisions)
- 100% `facing_bet=0` or very rare facing_bet=1 (97% non-facing-bet)
- 100% SPR=1.25 (compressed, river-heavy)
- Predominantly BB and BTN positions
- Heavily CHECK/BET labels

The new 400 hands will be:
- ~30% `is_preflop_aggressor=1`
- ~25-30% `facing_bet=1`
- ~25% SPR >= 4 (standard early-street)
- Mixed positions including SB
- More evenly distributed across all 5 action classes

**The pedagogical problem:** The model trained on this combined corpus
will encounter a natural correlation: low SPR + is_preflop_aggressor=0
+ facing_bet=0 → CHECK/BET (from the 100 existing hands). High SPR +
is_preflop_aggressor=1 → different action distribution (from the 400
new hands). This is not a spurious ML confound — it is a REAL poker
pattern. The decisions ARE different at different SPRs and with different
aggressor status. The correlation is correct, not spurious.

**The actual risk** is that the existing 100 hands teach CHECK/BET logic
with very different feature distributions (compressed SPR, river, checked-
to) than the new 400 hands. If the model sees 100 training examples of
"SPR=1.25, river, checked-to → BET if strong" and 400 training examples
of "SPR=4-8, flop, PFA → BET sometimes, CHECK sometimes," the model
correctly learns that SPR and street matter. This is GTO-correct
pedagogy.

**The only genuine pedagogical concern is the OOP-CHECK false generalisation:**
The 100 existing hands have 76% OOP rate and predominantly CHECK labels.
Combined with the new 400 hands that maintain 55-65% OOP, the model sees
OOP → CHECK at much higher frequency than OOP → BET. In real GTO play,
OOP betting frequency is ~30-40% (c-bets, leads, protection bets). The
combined corpus target of 27% BET is at the lower end of this range. This
is acceptable but borderline — push BET slightly above 27% in the new
400 hands if the existing 100's BET rate is ~40% (which it appears to be:
40 BET out of 100 = 40%).

**Combined corpus BET arithmetic:** 40 (existing) + 108 (synthesis target
for new 400) = 148 BET labels out of 500 = 29.6%. Acceptable. The BET
rate in the new 400 must be ~27% (108 of 400) to hit the target. This is
within a realistic range for the new hands' mix of PFA c-bets and
protection bets.

**Verdict:** The pedagogical concern is REAL but MANAGEABLE within the
blueprint's current stratification design. No structural change required,
but the programmer should shuffle the combined corpus before training
(blueprint Risk 7 mitigation already notes this). The OOP-BET rate in
the new 400 should be verified to be ≥25% before accepting the corpus.

---

## Q8 — Final verdict

### APPROVE-WITH-NITS

The blueprint is poker-domain sound. The 7 scenario modules address the
correct patterns; the action history templates are realistic for 5 of 7
modules; the boundary cases are GTO-meaningful (not arbitrary arithmetic);
the action distribution is appropriate for a warm-start training corpus.

**The blueprint should proceed to programming with the following required
fixes and recommended additions:**

### Required fixes (MUST fix before programming)

**R1: MAGG action history extends to the decision point.**
MAGG-1, MAGG-2, MAGG-3 action histories show the second bet but not
the hero's decision point. For `villain_aggression_count=2`, the decision
point must be on the river (after two prior-street bets). Action histories
must be extended to show flop bet + call + turn bet + call + river (hero
decides). The programmer must not implement MAGG scenarios as written in
the blueprint — the action history tables are truncated.

**R2: Boundary NFD hand validation after generation.**
After generating the 10 NFD boundary hands (villain_air_pct at 0.15,
0.17, 0.20, 0.22, 0.25), verify the actual computed villain_air_pct from
feature_extractor. Discard/replace any hand where actual value differs
from target by more than 0.03. This must be a pre-labelling step, not
post-labelling.

**R3: Rule 11 boundary pairs — vary board textures.**
The 5 boundary pairs for villain_top_pair_plus_pct should span at least
3 different board textures (not all on the same K-high 2-tone board).
This prevents the model from learning a spurious board-texture confound.

### Recommended additions (SHOULD add)

**N1: Free-card protection as explicit scenario target.**
Add 10-15 hands to the corpus targeting: non-PFA hero, monster hand
(set or straight), draw-heavy board (danger_score >= 0.6,
villain_draw_pct >= 0.25), not facing a bet. Expected label: BET
(protection motivation). These can be added to the `facing_initial_bet_scenarios.py`
or as a sub-category of the general Mode A self-play.

**N2: MW-30 FOLD contrast cases in BAC scenarios.**
Add 3-5 BAC hands where hero's equity is below pot odds → FOLD. The
MW-30 pattern teaches the CALL exception; the corpus also needs the
standard case (FOLD to bet-and-call when equity does not clear pot odds).
Without the FOLD baseline, the model has only the exception, not the rule.

**N3: MW-33 and MW-50 contrast cases.**
Add 5 CALL contrast cases alongside the 20 MW-33 RAISE hands (TPTK facing
initial bet → CALL, not RAISE). Add 3-5 CALL contrast cases alongside
the 20 MW-50 FOLD hands (trips+ facing raise + aggression → CALL, not FOLD).

**N4: SB-as-hero sandwich scenarios.**
Add 10-15 scenarios where hero is the SB facing a BTN bet with a BB
caller behind (or a BTN bet after SB's live straddle). These are
mechanically the same as BAC scenarios but from the sandwich position
perspective. The SB's tighter continuing standard (~20% MDF) produces
systematically higher FOLD rates.

**N5: Donk-bet defence scenarios.**
Add 5-10 facing-initial-bet scenarios where the bettor is the OOP player
(BB leads into IP CO/BTN hero). This captures the donk-bet dynamic where
the bettor's range is more polarised and the IP caller's response
differs from facing a c-bet.

**N6: Multi-street aggression FOLD calibration in Tier 1.**
Add 1-2 calibration hands for MAGG fold pattern before mass labelling.

**N7: PFA-4 turn c-bet volume cap.**
Keep PFA-4 (PFA checked flop, now leading turn) to ≤10 hands. This is
an uncommon action pattern that should not dominate the PFA stratum.

### Pre-labelling gto-expert review (MANDATORY before mass generation)

Per blueprint Risk 3 and my own Q2 analysis: gto-expert must review 20-30
factory-generated hands across all 7 modules BEFORE mass generation begins.
Specifically verify:
- BAC scenarios: villain composition features (villain_top_pair_plus_pct,
  villain_air_pct) are plausible given position + board + prior action
- NFD scenarios: villain_air_pct lands near intended target values
- MAGG scenarios: villain_aggression_count reads correctly at decision point
- PFA scenarios: is_preflop_aggressor = 1 is correctly populated

The pre-generation review is not optional — it prevents systematic feature
mis-specification from propagating through 400 hands.

### On Open Questions (OQ-1, OQ-2, OQ-3)

**OQ-1 (SPR formula fix scope):** Architect recommends accepting mixed SPR
distribution (100 existing at 1.25 compressed, 400 new at real SPR). This
is CORRECT from a poker standpoint. The compressed-SPR decisions are real
poker decisions (just at a specific point in the street tree). No
re-extraction needed.

**OQ-2 (v3.3 decision point):** Architect recommends Option (a) — GTO-expert
review on 30 factory hands before mass labelling. This is CORRECT. PFA
c-bets on monotone boards and multi-street aggression folds on the river
are exactly the spots where v3.2 may produce inconsistent labeller guidance.
The review cost (~$5-10) is trivially small versus re-labelling 400 hands.

**OQ-3 (Tier 1 expansion timing):** Architect recommends Tier 1 expansion
is a blocker, not optional. This is CORRECT from a calibration standpoint.
Labellers hitting PFA c-bet scenarios without calibration exposure to
that pattern will produce systematically incorrect labels on precisely
the patterns the corpus is designed to teach.

---

## Summary of verdict

**APPROVE-WITH-NITS.** The blueprint's poker-domain design is sound.
The 7 modules address the correct patterns with appropriate action
histories. The boundary cases are GTO-meaningful. The action distribution
is appropriate oversampling for a warm-start corpus.

Required fixes R1, R2, R3 must be completed before programmer handoff.
Recommended additions N1-N7 should be incorporated into Phase B or as
minor Phase A additions. The pre-labelling gto-expert review (20-30
factory sample) is mandatory.

The blueprint does NOT require a full revision or blocking rewrite. It
requires targeted corrections and additions that a competent programmer
can implement within the blueprint's existing architecture.
