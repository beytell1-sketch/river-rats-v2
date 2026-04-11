# Factory Design Brief: BET Context Situations — Batch 4

**Date:** 9 April 2026
**Status:** AWAITING REVIEW + OWNER APPROVAL
**Purpose:** Fill the BET/CHECK training gap — 0 IP PFA situations in current data
**Tree version:** BET_DECISION_TREE_V1.md (recalibrated, 9 April 2026)
**Informed by:** BET_FACTORY_PLAN_2026-04-09.md, BET_TREE_RECALIBRATION_RESULTS_2026-04-09.md

---

## Context: What Went Wrong and Why This Brief Exists

The recalibration run (9 April 2026) confirmed that every BET tree step
except Step 2 fires zero times on the current 563-situation dataset.
The root cause is not threshold miscalibration — it is factory coverage:

- 95% of BET-context situations are OOP heroes (138/146). Steps 3A, 4B-D,
  and 5 require is_ip == 1 and cannot fire without IP situations.
- villain_air_pct clusters at 0.162 and 0.297 across all PFA spots.
  Steps 3B and 6 require >= 0.40 and >= 0.45 respectively. Neither fires.
- villain_aggression_count is >= 1 for every near-miss candidate for Step 6,
  which requires == 0.

This batch exists to supply the specific situational configurations that the
tree needs to fire BET labels. It is not a general expansion — every sub-pattern
is targeted at a specific blocked step.

---

## Summary

100 new situations across 6 sub-patterns.
~60 BET labels, ~30 contextual BET labels, ~10 CHECK counterexamples.

| Sub-pattern | Code | Count | Target step | Label |
|-------------|------|-------|-------------|-------|
| IP PFA value c-bet | BP1 | 30 | 3A | BET |
| OOP PFA value c-bet | BP2 | 15 | 3B | BET |
| PFA semi-bluff c-bet | BP3 | 20 | 4A-D | BET |
| IP thin value non-PFA | BP4 | 15 | 5 | BET |
| OOP value exception | BP5 | 10 | 6 | BET |
| CHECK counterexamples | BP6 | 10 | Default / suppressors | CHECK |

Total: 100 situations. BET: ~90 designed-intent. CHECK: 10 explicit.

Note: expert labelling will relabel some designed-BET situations CHECK after
full context evaluation. Target is 90 BET-intent situations so that 70-80
confirmed BET labels survive after labelling yield.

---

## Universal Design Constraints

These apply to EVERY situation in this batch without exception.

### The to_call = 0 Requirement

**ALL situations must have to_call = 0.** Hero is never facing a bet.
Violation of this constraint sends the situation to the RAISE tree, not the
BET tree, and produces a useless data point.

Action sequence patterns that produce to_call = 0:

**IP hero (hero acts last on this street):**
- Preflop: villain A opens, villain B calls (or checks), hero calls.
  Postflop: BB checks, villain B checks → hero (IP) may bet or check.
- Preflop: hero opens from CO/BTN/SB, all callers.
  If PFA: CO opens, BTN calls, BB calls → BB checks, BTN checks → CO acts
  with to_call = 0.

**OOP hero (hero acts first on this street):**
- Hero is first to act. to_call = 0 always when OOP hero acts first.
- Example: BB defended → flop, BB acts first → to_call = 0.

**villain_aggression_count counts prior-street bets, not this street.**
A situation where villain bet the flop and hero called still has
villain_aggression_count = 1 on the turn. That is valid. What changes is
that to_call = 0 on the turn means villain has NOT bet this street yet.

### PFA vs Non-PFA Structural Requirement

**For BP1, BP2, BP3 (PFA situations):**
- hero_pos must equal opener_position (is_preflop_aggressor = 1)
- Prototypical structure: CO opens, BTN calls, BB calls.
  Flop: BB checks, BTN checks → CO (PFA, IP relative to both) has to_call = 0.
- Alternative: HJ opens, CO calls, BTN calls.
  Flop: HJ is IP relative to blinds but OOP relative to BTN/CO.
  Do NOT use this without being explicit about the IP/OOP determination.
- Simplest PFA + IP structure: BTN opens, BB calls, SB calls.
  Flop: SB checks, BB checks → BTN (PFA, IP) acts with to_call = 0.
- Simplest PFA + OOP structure: CO opens, BTN calls, BB calls.
  Flop: CO (PFA, OOP relative to BTN) acts first → to_call = 0.

**For BP4, BP5 (non-PFA situations):**
- hero_pos != opener_position (is_preflop_aggressor = 0)
- Hero defended a raise or cold-called.
- Example (IP non-PFA): BTN opens, BB calls.
  Hero = BB (OOP). For BP4 (IP non-PFA), this is wrong.
  Correct: CO opens, BTN calls (BTN is IP non-PFA).
  Postflop: CO (PFA) checks → BTN acts with to_call = 0.
- Example (OOP non-PFA): BB defends vs CO open (BTN folds).
  Flop: BB acts first → to_call = 0. is_preflop_aggressor = 0 for BB.

### villain_air_pct Construction Guidance

The recalibration confirmed that the factory's villain_air_pct is degenerate
for PFA spots: it clusters at 0.162 and 0.297 when it should reach 0.40-0.55
for boards where villain's preflop calling range misses hard.

villain_air_pct = fraction of villain's range that has no pair and no draw.

On an A-high board (A72r), a BTN cold-caller who called CO's open holds:
- Broadway connects: AK, AQ, AJ... (hit top pair — not air)
- Pairs: KK, QQ, JJ, TT... (overpairs — not air)
- Suited connectors: 87s, 76s, 65s... (gutshots or pair — partial air)
- Offsuit middle cards: K9o, Q8o... (no pair, no draw — air)
- Pocket fours-sixes: 44, 55, 66... (underpairs — low showdown value, marginal)

On a truly dry low board (A72r or A83r), the BTN calling range misses roughly
40-50% in air. This is the board type needed for BP2 and BP5.

On a K52r board for a BB defender (vs CO open), BB's calling range includes:
- K-x combos: hit top pair (not air)
- Pocket pairs below K: underpairs (not air, but low value)
- Connected cards: 65s, 54s... (gutshots on 5-2 gap boards — partial air)
- Offsuit trash: J7o, T8o... (complete air)

BB's air fraction on K52r is lower (~0.30-0.38) because BB defends wider
preflop and hits the board more. Use BTN/CO cold-callers for BP2/BP5
situations — their ranges are tighter preflop and miss harder.

**Target villain_air_pct values by sub-pattern:**
- BP1: 0.20-0.40 (IP situations, villain_air_pct is less critical)
- BP2: 0.40-0.55 (required — dry boards with BTN/CO cold-callers)
- BP3: 0.35-0.55 (semi-bluff situations need some fold equity)
- BP4: 0.20-0.45 (capped villain, but not necessarily air-heavy)
- BP5: 0.45-0.55 (strict requirement — same as 3B but tighter)
- BP6: 0.15-0.35 (CHECK situations — villain not air-heavy enough to justify bet)

### villain_aggression_count = 0 Requirement (BP2, BP5)

Steps 3B and 6 explicitly require villain_aggression_count == 0.

This means: villain has not bet on ANY prior street. The simplest way to
achieve this is flop situations where villain called preflop and checked
the flop. But this also works on turn situations where villain called
preflop, then check-called the flop (villain_aggression_count = 0 because
no bet, only calls).

Be explicit in the action history: "Villain calls preflop, checks flop,
checks turn to hero." At that point villain_aggression_count = 0 on the turn.
If villain CHECKED BACK the flop (villain_checked_back = 1), that also
produces villain_aggression_count = 0 on the turn.

---

## Sub-Pattern Definitions

---

### BP1: IP PFA Value C-Bet (30 situations — BET intent)

**Target step:** 3A (IP PFA Value Bet)

**Why this sub-pattern exists:** 0 of 8 IP situations in the current dataset
are PFA. Step 3A fires zero times. This is the highest-volume sub-pattern in
the batch because 3A is the primary BET generator — IP PFA c-bet is the most
frequent BET situation in real 3-way poker.

**Required feature conditions (ALL must be true):**

| Feature | Required value | Notes |
|---------|---------------|-------|
| is_preflop_aggressor | 1 | Hero raised preflop |
| is_ip | 1 | Hero is in position |
| is_made_hand | 1 | Made hand required for Step 3 |
| high_card_rank | >= 12 | Q or higher top card (Step 3 primary gate) |
| hand_category | Varies by tier | See tier-specific gates below |
| to_call | 0 | Universal constraint |
| villain_aggression_count | 0 or 1 | Both values must appear |

**Board tier distribution (for Step 3A Gate 3A-3):**

| Tier | Board definition | hand_category required | BP1 count |
|------|-----------------|----------------------|-----------|
| Tier 1 | high_card_rank >= 13 (K/A) AND flush_danger <= 0.20 AND connectivity_score <= 3 | >= 6 (top_pair+) | 14 |
| Tier 2 | high_card_rank >= 11 (J+) AND flush_danger <= 0.35 AND connectivity_score <= 5 | >= 7 (TPGK+) | 10 |
| Tier 3 | flush_danger <= 0.50 AND connectivity_score <= 7 | >= 10 (two_pair+) | 6 |

**Action sequence prototype (IP PFA):**

BTN opens 3bb, SB calls, BB calls.
Pot = 9bb. Effective stack ~97bb. SPR ~10.8 (high-SPR flop).
Flop: SB checks, BB checks. BTN (PFA, IP) acts first → to_call = 0.

Alternative: CO opens, BTN calls, BB calls.
Flop: BB checks, BTN checks. CO (PFA, IP relative to BB but OOP to BTN) → DO NOT USE
without explicit is_ip verification.

Preferred: BTN opens. This is the cleanest IP PFA structure.

**Hero hand types to cover (across 30 situations):**

- Top pair top kicker (hand_category = 8): min 8 situations
  Example: BTN holds KQ on Kh-7d-3c (Tier 1). TPTK.
- Top pair good kicker (hand_category = 7): min 6 situations
  Example: BTN holds AJ on Qd-8s-4h (Tier 2). Top pair, J kicker.
- Top pair weak kicker (hand_category = 6): min 6 situations, Tier 1 only
  Example: BTN holds A5 on Ad-9c-2h. Top pair, weak kicker.
- Two pair (hand_category = 10): min 6 situations, Tier 3
  Example: BTN holds J8 on Jc-8d-6s. Top two pair.
- Overpair (hand_category = 9): min 4 situations
  Example: BTN holds QQ on Jh-7d-3c. Overpair on Tier 2 board.

**Board examples (not exhaustive — designer must generate at least 10 unique boards):**

Tier 1 boards (A/K-high, dry, rainbow):
- Ad 9c 2h (A-high, rainbow, disconnected)
- Kd 7s 3c (K-high, rainbow, dry)
- As 8d 4h (A-high, rainbow, moderate gap)
- Kh 6c 2d (K-high, rainbow, very dry)

Tier 2 boards (Q/J-high, moderate):
- Qs 8d 4c (Q-high, rainbow, moderate gap)
- Jh 7c 3s (J-high, rainbow, 4-gap)
- Qd 9s 5h (Q-high, moderate connectivity)
- Jd 8s 4c (J-high, two-tone)

Tier 3 boards (connected, hero needs two-pair+):
- Js 9d 7c (connected, J-high, moderate straight danger)
- Th 8s 6d (connected, T-high, two-pair playable)

**SPR requirements for BP1:**

Standard SRP flop SPR is 8-12. BP1 is primarily a flop batch.
- Flop situations: SPR 8.0-12.0 (realistic SRP flop depth)
- Turn situations: SPR 3.0-7.0 (after one street of betting, SPR contracts)
- At least 5 situations at SPR >= 8.0, at least 5 at SPR 3.0-6.0

**Per-situation variation requirements:**

- Boards: min 10 unique boards, max 4 situations per board
- Street: min 20 flop, min 8 turn, max 2 river (c-bets are primarily flop/turn)
- Position: all IP (is_ip = 1 for all 30)
- villain_aggression_count: min 10 at count = 0, min 10 at count = 1
- villain_air_pct: span 0.20-0.40 across the 30 situations

---

### BP2: OOP PFA Value C-Bet (15 situations — BET intent)

**Target step:** 3B (OOP PFA Value Bet Exception)

**Why this sub-pattern exists:** Step 3B requires villain_air_pct >= 0.40 and
villain_aggression_count == 0. All 19 OOP PFA candidates in the current data
have villain_air_pct <= 0.297. None fires.

**Required feature conditions (ALL must be true — Step 3B conditions):**

| Feature | Required value | Notes |
|---------|---------------|-------|
| is_preflop_aggressor | 1 | Hero raised preflop |
| is_ip | 0 | OOP hero |
| is_made_hand | 1 | Step 3 requires made hand |
| hand_category | >= 7 | TPGK minimum — no thin value OOP |
| high_card_rank | >= 13 | K or A board required OOP (stricter gate) |
| villain_air_pct | >= 0.40 | CRITICAL — this blocked Step 3B entirely |
| is_rainbow | 1 OR flush_danger <= 0.20 | Dry board reduces caller draws |
| villain_aggression_count | 0 | REQUIRED — not 1, not 2 |
| hero_range_percentile | >= 0.72 | Top 28% of range OOP |

**How to achieve villain_air_pct >= 0.40 on A/K-high boards:**

The villain (cold-caller) is BTN or CO. Their preflop calling range vs a
CO or BTN open is approximately 15-20% of hands. On a K-high or A-high
rainbow board, a significant fraction of this range has no pair and no draw:

- Example: CO opens, BTN calls (BTN is the villain).
  BTN's calling range: ATo+, KJo+, QJo+, suited connectors, pocket pairs 22+.
  On a K42r board:
  - BTN's K-x hits top pair: KQ, KJ, KT → not air (~15 combos)
  - BTN's A-x: AK has two pair, AQ/AJ have no pair on K42r → air (~8 combos)
  - BTN's QQ, JJ, TT, 99: overpairs → not air
  - BTN's 88-22: underpairs → weak showdown, partially air (~30 combos)
  - BTN's suited connectors on K42r: 87s, 76s → gutshot or nothing
  - BTN's offsuit middling: QJo, QTo, JTo → no pair → air (~18 combos)
  Air fraction: roughly 40-48% of BTN's range on K42r. Use this board type.

- Example: BTN opens, BB calls (BB is the villain).
  BB defends wider → hits boards more → villain_air_pct lower.
  DO NOT use BB as villain for BP2 — air fraction typically 25-35%.

**Preferred structures for BP2:**

- CO opens (PFA, OOP to BTN/CO callers? — clarify)
  Wait: CO opens, BTN calls, BB calls. CO is OOP to BTN.
  Correct PFA + OOP structure: CO opens → BB calls (only). CO is OOP to...
  No: CO is between BTN and BB. CO is OOP to BTN only.
  Simplest: HJ opens (PFA), CO calls (villain), BTN folds, SB folds, BB folds.
  HJ is OOP to CO. CO cold-called. On an A72r board, CO's range misses hard.
  villain (CO) aggression count = 0 if CO only called preflop and checks flop.

- Alternative: CO opens (PFA), BTN calls, BB folds.
  CO is OOP to BTN. BTN is the cold-caller. Postflop: CO checks? No — CO can
  lead. CO acts first because OOP. CO may bet or check. to_call = 0.
  villain = BTN (cold-caller, range misses low/dry boards hard).

Use CO-open vs BTN-call or HJ-open vs CO-call structures. The cold-calling
position (BTN or CO) has a tight preflop range that misses A/K-high dry boards
at 40-50% air rate.

**Hero hand types to cover (across 15 situations):**

- TPGK (hand_category = 7): min 5 situations
  Example: CO holds AQ on A-7-2r. TPGK. villain (BTN) range is air-heavy.
- TPTK (hand_category = 8): min 5 situations
  Example: CO holds AK on A-8-3r. TPTK.
- Two pair (hand_category = 10): min 3 situations
  Example: CO holds K7 on K-7-2r. Top two pair. OOP — bet into air-heavy villain.
- Overpair (hand_category = 9): min 2 situations
  Example: CO holds KK on A-9-3r (aces on board — overpair is top pair effectively).
  Use carefully: KK on A-high board has tricky range implications.

**Board examples (A/K-high, rainbow, dry — all 15 boards must be Tier 1):**

- Ah 7c 2d (A-high, rainbow, very dry, connectivity_score = 2)
- Kd 8s 3c (K-high, rainbow, moderate gap)
- As 9h 4c (A-high, rainbow, 5-gap)
- Kh 6d 2s (K-high, rainbow, disconnected)
- Ad 8c 3h (A-high, rainbow, dry)

All boards: is_rainbow = 1, flush_danger <= 0.10, connectivity_score <= 3.

**SPR requirements for BP2:**

OOP PFA flop c-bets occur at standard SRP depth.
- Flop: SPR 8.0-12.0 (all BP2 situations should be flop — OOP PFA c-bet is
  primarily a flop decision; turn OOP c-bets are rarer and more complex)
- At least 8 situations at SPR >= 8.0

**Per-situation variation requirements:**

- Boards: min 5 unique boards, max 3 situations per board
- Street: min 12 flop, max 3 turn
- hero_range_percentile: span 0.72-0.88 (OOP minimum is 0.72; vary it)
- villain_air_pct: span 0.40-0.55 (all must clear 0.40; include situations at both ends)
- villain_aggression_count: 0 for all 15 — structural constraint, not a variation

---

### BP3: PFA Semi-Bluff C-Bet (20 situations — BET intent)

**Target step:** Step 4 (PFA Bluff C-Bet, sub-conditions 4A through 4D)

**Why this sub-pattern exists:** All 6 current PFA + no-made-hand candidates
are OOP with hero_range_percentile < 0.72 (S2 fires). Only 4A (combo draw,
OOP override) can bypass S2 for OOP hands, but no current candidates have
draw_outs >= 12.

**Required feature conditions (ALL must be true for Step 4):**

| Feature | Required value | Notes |
|---------|---------------|-------|
| is_preflop_aggressor | 1 | Hero raised preflop |
| is_made_hand | 0 | Step 4: hero missed the board |
| high_card_rank | >= 12 | Q or higher (range credibility gate) |
| to_call | 0 | Universal constraint |

**Then one of four sub-conditions must fire (see allocation below).**

**Sub-condition allocation across 20 situations:**

| Sub-condition | Description | Count | Position |
|--------------|-------------|-------|----------|
| 4A: Combo draw | draw_outs >= 12 | 8 | IP (5) + OOP (3) |
| 4B: NFD + blocker | draw_outs >= 9, flush_draw_rank >= 12, flush_block_pct > 0 | 6 | IP only |
| 4C: Nut draw + board favour | draw_outs >= 9, flush_draw_rank >= 13, board_favour >= 0.30, is_ip = 1 | 3 | IP only | NOTE: board_favour is [DEMOTED] as a primary gate in Steps 3/4 (replaced by high_card_rank). Sub-condition 4C is the ONE remaining use of board_favour — it is still active here as a secondary qualifier, not a primary gate. Do not remove it. |
| 4D: Blocker + weak draw | flush_block_pct > 0, draw_outs >= 4, villain_air_pct >= 0.40, is_ip = 1, high_card_rank >= 13, is_rainbow = 1 | 3 | IP only |

**Sub-condition 4A (8 situations):**

draw_outs >= 12 means combo draw (flush draw + straight draw simultaneously).
Example holdings: Jh-Th on Qh-8h-9d (FD + OESD = 15 outs), 9s-8s on Ks-7s-6d
(FD + OESD = 15 outs), 6h-5h on Ah-7h-4d (FD + gutshot = 12 outs).

OOP 4A (3 situations): hero is OOP PFA, S2 fires (raw_equity < 0.60,
hero_range_percentile < 0.72), but 4A combo draw overrides S2.
Note: hero_range_percentile < 0.72 must be true in OOP 4A situations — the
override only matters if S2 actually fired. If hero_range_percentile >= 0.72,
Step 3B would fire instead (if board allows).

IP 4A (5 situations): hero is IP PFA, S2 does not apply (is_ip = 1).

Boards for 4A: two-tone or monotone-approaching boards where flush + straight
draws coexist. Example: Ks-7s-6d (spade flush draw + 8-9 needed for OESD),
Qh-8h-9c (heart FD + JT/T7 OESD), Jd-Td-6c (diamond FD + 8-9 OESD).

**Sub-condition 4B (6 situations — IP only):**

Requirements: draw_outs >= 9, flush_draw_rank >= 12 (Q/K/A of flush suit),
flush_block_pct > 0 (hero holds at least one flush suit card).

Example: BTN holds Ks-9h on Qs-8s-3d. BTN has a king-high flush draw
(flush_draw_rank = 13) and blocks one combo of villain's possible K-flush
draws (flush_block_pct > 0). draw_outs = 9 (flush draw).

Boards: two-tone flop/turn where hero has nut-adjacent flush draw.
Flush danger should be low-to-moderate (0.20-0.40) — on a monotone board,
villain's range has too many flushes for the blocker to matter much.

**Sub-condition 4C (3 situations — IP only):**

Requirements: draw_outs >= 9, flush_draw_rank >= 13 (K or A), board_favour >= 0.30.
Note: board_favour is demoted from primary gate but still available as a feature.
Use it as a design parameter here — board_favour >= 0.30 means PFA's range is
substantially advantaged (high-card boards where PFA's opening range hits hard).

Example: BTN holds As-9h on Ks-8s-4d. BTN has nut flush draw (A of flush suit),
flush_draw_rank = 14, draw_outs = 9. K-high board strongly favours BTN opener.

**Sub-condition 4D (3 situations — IP only, restricted):**

Requirements: flush_block_pct > 0, draw_outs >= 4 (gutshot minimum), villain_air_pct
>= 0.40, is_ip = 1, high_card_rank >= 13 (K or A), is_rainbow = 1.

This is the narrowest sub-condition. Edge case — hero holds a blocker card and
a gutshot on a dry A/K-high rainbow board. Fold equity must be real (villain
holds lots of air that folds to any bet).

Example: BTN holds Ah-7d on Kd-9s-6c. BTN has the Ah (blocker — removes
A-flush combos from villain, which is relevant even on rainbow boards because
it blocks villain's perception of BTN's range containing the Ace). draw_outs = 4
(gutshot: 5 makes the straight K-9-6-5-[7]? No — need to construct a proper
gutshot: BTN holds Jh-8h on Ah-9c-7d. J8 has a gutshot: T completes J-8-T-9
or T-8-9-7? Correct: J-T-9-8-7 → J8 needs a T or 6 — wait, J-T-9-8-7 is
the straight. J8 on 97 board: 8 at the bottom, J at the top, T fills it.
That is a gutshot to the T. draw_outs = 4. flush_block_pct > 0 if Jh is the
heart suit and board has no hearts (rainbow). hero holds Jh → blocks villain's
heart nutdraw combos (Ah-Jh is removed). This is the 4D archetype.).

**Hero hand types for BP3 (across 20 situations):**

All heroes are "missed" (is_made_hand = 0). Hand types:
- Combo draw (FD + OESD): 8 situations (4A)
- Near-nut flush draw: 9 situations (4B + 4C, draw_outs = 9)
- Gutshot + blocker: 3 situations (4D, draw_outs = 4-6)

**Per-situation variation requirements:**

- Boards: min 8 unique boards, max 3 situations per board
- Street: min 12 flop, min 6 turn, max 2 river
- flush_danger: span 0.10-0.50 (semi-bluffs work on various flush textures)
- draw_outs: span 4-15 across the 20 situations
- villain_air_pct: span 0.35-0.55 (fold equity required for semi-bluffs)
- villain_aggression_count: min 8 at count = 0, min 8 at count = 1
  (S3 fires at >= 2, so all situations must have count = 0 or 1)

---

### BP4: IP Thin Value Non-PFA (15 situations — BET intent)

**Target step:** Step 5 (Thin Value Bet, IP, Capped Opponent)

**Why this sub-pattern exists:** 0 of 8 IP situations in the current data are
non-PFA made hands with hand_category >= 7. Step 5 cannot fire.

**Required feature conditions (ALL must be true — Step 5 conditions):**

| Feature | Required value | Notes |
|---------|---------------|-------|
| is_ip | 1 | IP only — Step 5 is IP specific |
| is_made_hand | 1 | Made hand required |
| hand_category | >= 7 | TPGK minimum for thin value |
| villain_range_capped | 1 | At least one opponent range is capped |
| villain_top_pair_plus_pct | <= 0.35 | Villain unlikely to hold strong made hands |
| danger_score | <= 0.35 | Dry board — thin value loses on wet boards |
| villain_aggression_count | <= 1 | Not a multi-street aggressor |
| is_preflop_aggressor | 0 | Non-PFA — Step 3 handles PFA |
| to_call | 0 | Universal constraint |

**What makes a villain range "capped" (villain_range_capped = 1):**

villain_range_capped = 1 when the villain's preflop action logically excludes
premium holdings. The most reliable source: villain COLD-CALLED (did not 3-bet)
from a position where they would 3-bet strong hands. A BTN or CO cold-caller
would typically 3-bet AA, KK, QQ, AK — so their flat-call range has these
removed. This caps their range at roughly JJ/TT at best.

Additionally: any position that limped preflop, or a BB that checked their
option, has a capped range.

**Action sequence prototype (IP non-PFA):**

Preferred structure: HJ opens → CO cold-calls (capped villain) → BTN cold-calls (hero, IP).
BB folds. Flop: CO checks, HJ checks → BTN (hero) acts with to_call = 0.

Why this works:
- Hero (BTN) is IP and non-PFA (is_preflop_aggressor = 0)
- CO is the relevant capped villain — cold-called the open, would have
  3-bet AA/KK/QQ/AK → villain_range_capped = 1
- HJ is the PFA but checked — their range is uncapped but passive on this board
- Both opponents checked → villain_aggression_count = 0 on the flop

Alternative: CO opens → BTN calls (hero) → BB calls. Flop: BB checks, CO checks → BTN acts.
This also works — CO is PFA but checked. BB is the capped villain (defended, would
have 3-bet premiums). villain_range_capped = 1 from BB's perspective.

NOTE: The opener's range is NOT capped. villain_range_capped = 1 must come from the
cold-caller or defender, not the opener. All BP4 situations must use a structure
where at least one villain is a cold-caller or defender.

**Hero hand types (across 15 situations):**

- TPGK (hand_category = 7): min 6 situations
  Example: BTN holds KJ on Kd-7s-3c. CO opened, BTN called. CO checks.
- TPTK (hand_category = 8): min 4 situations
  Example: BTN holds AQ on Qh-8d-4c.
- Overpair (hand_category = 9): min 3 situations
  Example: BTN holds QQ on Jh-7d-3s. Overpair, capped villain.
- Two pair (hand_category = 10): min 2 situations
  Example: BTN holds K7 on Kd-7s-3c. Two pair, thin value vs capped range.

**Board requirements for BP4:**

danger_score <= 0.35 requires dry, disconnected boards.
- is_rainbow preferred (flush_danger <= 0.10 helps keep danger_score low)
- connectivity_score <= 4 (low straight danger)
- Example boards: Kd-7s-3c, Qh-8d-4c, Jh-6d-2s, Td-7c-3h

villain_top_pair_plus_pct <= 0.35 is achievable when:
- Board pairs poorly with villain's preflop capped range
- Low boards (J-high or lower) where villain's cold-call range lacks top-pair
  combos (their high cards are Q+/A+ but board is J-low)

**SPR requirements for BP4:**

Step 5 does not have an SPR gate, but thin value bets are most sensible
at moderate-to-high SPR (enough implied odds to make the call worthwhile
for the villain, enough stack to bet small for value).
- Flop SPR: 6.0-12.0
- Turn SPR: 3.0-7.0
- Include at least 4 situations at SPR >= 8.0

**Per-situation variation requirements:**

- Boards: min 6 unique boards, max 3 situations per board
- Street: min 8 flop, min 5 turn, max 2 river
- villain_top_pair_plus_pct: span 0.10-0.35 (all must be <= 0.35)
- danger_score: span 0.10-0.35 (must stay below 0.35)
- villain_aggression_count: min 5 at count = 0, min 5 at count = 1
- villain_range_capped: 1 for all 15 — structural constraint

---

### BP5: OOP Value Exception (10 situations — BET intent)

**Target step:** Step 6 (OOP Value Bet Exception)

**Why this sub-pattern exists:** 8 near-miss candidates exist for Step 6 in
current data, but all are blocked by villain_aggression_count >= 1. Step 6
requires villain_aggression_count == 0. This is the smallest sub-pattern
but represents a documented GTO pattern (KB Example 6) that the model must learn.

**Required feature conditions (ALL must be true — Step 6 conditions):**

| Feature | Required value | Notes |
|---------|---------------|-------|
| is_ip | 0 | OOP hero — Step 6 is OOP only |
| raw_equity | >= 0.65 | Strong equity required OOP |
| villain_air_pct | >= 0.45 | CRITICAL — majority of villain range is air |
| is_rainbow | 1 | Dry board — no flush draws for villains |
| connectivity_score | <= 3 | Disconnected — no straight draws |
| hand_category | >= 8 | TPTK minimum — strong made hand OOP |
| villain_aggression_count | 0 | CRITICAL — both blocked Step 6 in current data |
| villain_fold_equity_estimate | >= 0.35 | Some fold equity required OOP |
| is_preflop_aggressor | 0 | Non-PFA (PFA OOP is handled by Step 3B) |
| to_call | 0 | Universal constraint |

**What makes this pattern different from BP2:**

BP2 (Step 3B) = OOP PFA. Hero raised preflop and has range advantage.
BP5 (Step 6) = OOP non-PFA. Hero is defending (BB, SB) or cold-called.
This is sometimes called the "donk bet" or OOP probe pattern.

The distinction: a BB who defended a CO open, hit TPTK on an A-high rainbow board,
and now leads into the CO — this is the KB Example 6 pattern. The villain (CO)
has a strong preflop range but misses this particular board configuration frequently
enough that villain_air_pct >= 0.45 is achievable.

**How to achieve villain_air_pct >= 0.45 for OOP non-PFA:**

Villain is the OPENER (CO, BTN), not the cold-caller. Opener's range is wide
but positionally polarized. On a low rainbow board (5-4-2r or 7-6-2r), even
the opener's range misses hard because:
- Opener's AK, AQ, AJ, AT, KQ, KJ, QJ... all miss (no pair, no draw on 7-6-2r)
- Opener's suited connectors (87s, 65s) may have caught a piece of 7-6-2r but
  65s hit a pair, 87s hit nothing
- Opener's high pocket pairs (AA, KK, QQ) are overpairs — not air but not top pair
- Opener's middle pocket pairs (77-TT) hit a set or overpair on low boards
- Opener's truly air hands: AK on 7-6-2r (overcards only, no pair) = air

For a BTN opener on a 7-6-2r board, rough air fraction:
- AK, AQ, AJ, KQ, KJ, QJ = multiple combos of complete miss = ~25-30% of BTN range
- Add underpairs below 22 (none) and middling offsuit hands
- villain_air_pct can reach 0.40-0.50 on low boards for openers with wide ranges

Hero (BB or SB) hit this board (7-6-2r) with a holding like 7-7 (set) or
7-6 (two pair) or 7-5s (two pair). hero hand_category >= 8 (TPTK would need
top pair + best kicker, but on a 7-high board, TPTK means hero holds A-7 or
7-7 or similar). Use two pair or better for cleaner situation design.

**Preferred board structures for BP5:**

Low rainbow boards where hero (BB/SB) hit and opener missed:
- 7s 6c 2h (low, rainbow, connected but not flush-dangerous)
  Wait: connectivity_score must be <= 3 for Step 6. 7-6-2 has connectivity 4-5
  (7-6 are adjacent). Check: 7h-4d-2c (5-gap structure, connectivity_score = 2).
  Use genuinely disconnected low boards.
- 8d 4s 2c (disconnected, rainbow, low) — hero might hold 8-4, 8-8, 4-4
- 9c 5h 2s (rainbow, disconnected)
- Ah 7d 2c — if hero is BB and called CO, hero might hold A-3, A-7, or 7-2
  But wait: if A-high board, villain (CO) might have Ax combos. villain_air_pct
  may be lower on A-high because opener holds A-x combos.
  For BP5, low boards (7-high, 8-high, 9-high) work better than A/K boards.

**Hero hand types (across 10 situations):**

- Two pair (hand_category = 10): min 4 situations
  Example: BB holds 8-7 on 8d-7c-2h. Top two pair.
- Trips (hand_category = 11): min 2 situations
  Example: BB holds 7-5 on 7d-7c-2h. Trips on low paired board.
- Set (hand_category >= 12 equivalent in flop context): min 2 situations
  Example: BB holds 4-4 on 8d-4s-2c. Bottom set.
- TPTK on low board (hand_category = 8): min 2 situations
  Example: BB holds A-8 on 8d-4s-2c. TPTK (A kicker is top kicker on this board).

**Per-situation variation requirements:**

- Boards: min 4 unique boards, max 3 situations per board
- Street: min 6 flop, max 4 turn (Step 6 is primarily a flop lead pattern)
- raw_equity: span 0.65-0.80
- villain_air_pct: span 0.45-0.55
- villain_fold_equity_estimate: span 0.35-0.55
- villain_aggression_count: 0 for all 10 — structural constraint

---

### BP6: CHECK Counterexamples (10 situations — CHECK label)

**Purpose:** Situations that LOOK like BET candidates on the surface but
correctly CHECK. These teach the model the boundaries of the BET conditions.
Each counterexample must correspond to a specific suppressor or unmet gate.

**Why 10 situations:** The batch is primarily BET-intent. 10 CHECK counterexamples
prevents the model from seeing 90 BETs and learning to always bet in c-bet contexts.
These must be carefully chosen to illustrate failed conditions, not arbitrary CHECKs.

**Required structure:** For each situation, exactly one key condition must fail
relative to the BET steps. Document which step was "close" and why it failed.

**Failure mode allocation (all 10 situations):**

| Mode | Description | Count | Failed condition |
|------|-------------|-------|-----------------|
| BP6-A | Wet board suppressor (S1) | 2 | flush_danger >= 0.60 OR straight_danger >= 0.50, is_made_hand = 0, draw_outs < 12 |
| BP6-B | OOP suppressor (S2) fires, no override | 2 | is_ip = 0, hero_range_percentile < 0.72, raw_equity < 0.60 |
| BP6-C | Multi-street aggressor (S3) | 1 | villain_aggression_count >= 2, hero_range_percentile < 0.85 |
| BP6-D | Step 3A: Tier 4 board (no c-bet) | 2 | Very connected or monotone — Step 3A exits at Tier 4 |
| BP6-E | Step 3B fails one gate | 1 | OOP PFA, TPGK, dry board, BUT villain_air_pct = 0.32 (below 0.40) |
| BP6-F | Step 5 fails one gate | 1 | IP non-PFA, TPGK, BUT villain_range_capped = 0 OR danger_score = 0.42 |
| BP6-G | Monster on dry board (trap) | 1 | is_monster = 1, danger_score < 0.45 → Step 2 does not fire → CHECK to trap |

**BP6 situation design notes:**

BP6-A (2 situations): Hero holds a draw on a wet board.
- Example: Hero holds Jh-Th on Kh-Qh-8d. flush_danger = 0.62 (high flush danger),
  is_made_hand = 0 (missed), draw_outs = 8 (flush draw only, < 12). S1 fires. CHECK.
- Example: Hero holds 8h-7d on 9c-8s-6h. straight_danger = 0.55. is_made_hand = 0.
  draw_outs = 8 (OESD, but straight_danger >= 0.50). S1 fires. CHECK.
  Note: hero holds a pair (8-8?) — if is_made_hand = 1, S1 does not apply. Make
  sure hero has NO pair on the board. Hero holds J-T on 9-8-6: no pair, OESD = 8 outs.

BP6-B (2 situations): OOP PFA or OOP non-PFA below the range threshold.
- Example: OOP PFA holds top pair weak kicker (hand_category = 6, not 7).
  hero_range_percentile = 0.62 (below 0.72). raw_equity = 0.55 (below 0.60).
  S2 fires. No step 3B (hand_category < 7). CHECK.
- Example: OOP non-PFA holds middle pair (hand_category = 5).
  hero_range_percentile = 0.48. raw_equity = 0.48. S2 fires. CHECK.

BP6-C (1 situation): Villain has shown multi-street aggression. Hero has a
decent hand but villain_aggression_count = 2. hero_range_percentile = 0.78
(< 0.85). S3 fires. CHECK.
- Example: Hero holds two pair on turn. Villain bet flop and turn (aggression_count = 2).
  hero checks back even with a strong made hand.

BP6-D (2 situations): Very connected or monotone board.
- Example: Flop is 8h-7h-6h (monotone). Hero holds no made hand, no nut flush.
  Tier 4 board → Step 3A exits without firing. S1 also fires (flush_danger >= 0.60
  if is_made_hand = 0). CHECK.
- Example: Flop is Tc-9d-8c (connected, two-tone, connectivity_score >= 8).
  Hero is IP PFA, holds top pair (Td-Qs, hand_category = 6). S1 does NOT fire
  (is_made_hand = 1). Step 3A reaches Tier 4 (connectivity > 7) → exits without
  BET. hand_category = 6 is below Tier 3's >= 10 requirement. The made hand is
  not strong enough for this board texture. CHECK. This is the true Tier 4
  teaching signal: even a made hand checks on very connected boards when it's
  not two-pair+.

BP6-E (1 situation): Step 3B almost fires but villain_air_pct = 0.32.
- Design explicitly: OOP PFA, TPGK (hand_category = 7), A-high rainbow board,
  villain_aggression_count = 0, hero_range_percentile = 0.75. But villain_air_pct
  = 0.32 (fails the 0.40 gate). CHECK. This situation is almost identical to a
  valid BP2 situation — only the villain_air_pct distinguishes them. That contrast
  is the training value.

BP6-F (1 situation): Step 5 almost fires but one gate fails.
- Design: IP non-PFA, hand_category = 7, is_ip = 1, villain_aggression_count = 0.
  But danger_score = 0.42 (fails the <= 0.35 gate). Or: villain_range_capped = 0
  (villain is the PFA, not a cold-caller — range is not capped). CHECK.

BP6-G (1 situation): Monster on dry board traps.
- Design: Hero holds a set (is_monster = 1) on a dry board.
  danger_score = 0.28 (low danger — no draws for villain). Step 2 condition:
  danger_score >= 0.45 NOT met. Step 2 does not fire. Steps 3/4/5/6 may fire
  for other reasons — make sure none do (e.g., is_preflop_aggressor = 0, is_ip = 0
  for OOP trap). CHECK. Hero is trapping (slowplaying on a dry board where villain
  has no draws to charge).

**Per-situation variation requirements:**

- All 7 failure modes must appear (see allocation above)
- Boards: min 6 unique boards, no board shared with BET sub-patterns
  (separate boards prevent the model from seeing the same board produce
  both BET and CHECK, which could create position-correlated confusion)
- hero_cards: no duplicates within BP6

---

## Diversity Requirements (adapted from R1-R7)

### R1: Board Uniqueness

- Minimum 15 unique boards across all 100 situations
- Maximum 8 situations per board (prefer 6)
- No board from Batch 1, 2, or 3 may be reused (46 existing boards excluded)
- BP6 boards must not overlap with BP1-BP5 boards (see BP6 note above)

### R2: Board Texture Distribution (of 15+ boards)

| Texture | Min boards | Max boards |
|---------|-----------|-----------|
| Rainbow | 5 | 8 |
| Two-tone | 5 | 7 |
| Monotone (flop) | 0 | 1 |
| Paired | 1 | 2 |
| Connected (connectivity_score >= 6) | 1 | 2 |

Notes:
- Tier 1 boards (A/K-high, dry) must constitute at least 6 boards (BP1 Tier 1 + BP2 all)
- Tier 4 boards (very connected/monotone) max 1-2 (BP6-D only)
- Do not exceed 1 monotone flop board across the entire batch

### R3: SPR Distribution (of 100 situations)

| SPR tier | Min % | Notes |
|----------|-------|-------|
| 8.0-12.0 | 30% | Standard SRP flop depth — most BP1 and BP2 situations |
| 3.0-8.0 | 35% | Turn depth SRP, or flop after short-stack action |
| 1.5-3.0 | 15% | Low SPR turns/rivers |
| 12.0+ | 5% | Deep stacks |

No more than 15% of situations may share the same SPR value within +/- 0.15.
This directly addresses the SPR=1.11 uniformity problem from Batch 1.

Implementation: For a realistic SRP flop with pot = 9bb and effective stacks
= 97bb, set effective_stack = 970 and pot = 90 (units are chips, not bb).
SPR = 970/90 = 10.8. Do NOT use pot=90 with effective_stack=100 (gives SPR=1.1,
which is a 3-bet-pot stack depth, not SRP).

### R4: Street Distribution (of 100 situations)

| Street | Min | Max |
|--------|-----|-----|
| Flop | 50 | 65 |
| Turn | 25 | 40 |
| River | 5 | 10 |

C-bet decisions (the focus of this batch) are primarily flop and turn decisions.
River c-bets are rare and complex — limit to 5-10. This is different from the
RAISE batch which had a larger river allocation.

### R5: Position Distribution (of 100 situations)

| Position | Min | Max |
|----------|-----|-----|
| IP (BTN, CO, HJ) | 55 | 65 |
| OOP (BB, SB) | 35 | 45 |

This directly corrects the 95% OOP concentration in the current BET dataset.
IP minimum of 55 ensures Steps 3A, 4B-D, and 5 have sufficient coverage.

Sub-pattern position breakdown:
- BP1: all 30 are IP (is_ip = 1)
- BP2: all 15 are OOP (is_ip = 0)
- BP3: 17 IP, 3 OOP (from 4A OOP)
- BP4: all 15 are IP
- BP5: all 10 are OOP
- BP6: mixed (some IP, some OOP depending on failure mode)
Total IP from BP1+BP3+BP4: 30 + 17 + 15 = 62 IP. Total OOP from BP2+BP3+BP5: 15 + 3 + 10 = 28 OOP.
Plus BP6 (mixed, ~5 IP, ~5 OOP). Total: ~67 IP, ~33 OOP. Within target range.

### R6: Boards Per Sub-Pattern

| Sub-pattern | Size | Min unique boards | Max situations/board |
|-------------|------|-------------------|---------------------|
| BP1 | 30 | 10 | 4 |
| BP2 | 15 | 5 | 3 |
| BP3 | 20 | 8 | 3 |
| BP4 | 15 | 6 | 3 |
| BP5 | 10 | 4 | 3 |
| BP6 | 10 | 6 | 2 |

### R7: Villain-Feature Variance Within Sub-Patterns (size >= 8)

For BP1, BP3, BP4 (size >= 8), the following ranges must be achieved:

| Feature | Min range (max - min) |
|---------|----------------------|
| villain_fold_equity_estimate | >= 0.20 |
| villain_top_pair_plus_pct | >= 0.10 |
| villain_air_pct | >= 0.15 |
| flush_danger | >= 0.10 (where flush-relevant) |

---

## Per-Sub-Pattern Variation Specifications

### BP1 (30 situations): IP PFA Value C-Bet

**Feature ranges that must be covered:**

| Feature | Required span |
|---------|--------------|
| hand_category | 6-10 (top_pair through two_pair) |
| high_card_rank | 11-14 (J through A — covers Tier 2 and Tier 1) |
| flush_danger | 0.05-0.45 (across Tier 1, 2, 3 boards) |
| connectivity_score | 2-7 (across all tiers) |
| villain_air_pct | 0.20-0.40 |
| villain_aggression_count | 0 and 1 |
| SPR | 3.0-12.0 |

**Board textures that must appear:**

- Min 5 Tier 1 boards (A/K-high, rainbow, dry) — the core IP PFA c-bet texture
- Min 3 Tier 2 boards (Q/J-high, two-tone acceptable)
- Min 2 Tier 3 boards (connected, hero needs two-pair+)

**Hero hand types:**

- TPTK (cat 8): 8 situations, spread across Tier 1 and Tier 2 boards
- TPGK (cat 7): 6 situations, Tier 2 boards primarily
- TP weak kicker (cat 6): 6 situations, Tier 1 boards only (the gate allows this)
- Overpair (cat 9): 4 situations, any tier
- Two pair (cat 10): 6 situations, Tier 3 boards

**Streets:**
- Flop: 20 situations (high SPR, standard SRP depth)
- Turn: 8 situations (SPR contracted after flop)
- River: 2 situations max (turn c-bet follow-through)

---

### BP2 (15 situations): OOP PFA Value C-Bet

**Feature ranges that must be covered:**

| Feature | Required span |
|---------|--------------|
| hand_category | 7-10 (TPGK through two_pair) |
| high_card_rank | 13-14 (K and A only) |
| flush_danger | 0.05-0.15 (all rainbow/near-rainbow) |
| villain_air_pct | 0.40-0.55 |
| hero_range_percentile | 0.72-0.88 |
| villain_aggression_count | 0 for all 15 |

**Board textures:**

- All 5+ boards must be Tier 1 (high_card_rank >= 13, flush_danger <= 0.20,
  connectivity_score <= 3)
- Strongly prefer is_rainbow = 1 for all 15 (Step 3B requires is_rainbow = 1
  OR flush_danger <= 0.20; using all-rainbow is cleaner)

**Hero hand types:**

- TPGK (cat 7): 5 situations — minimum for OOP value bet
- TPTK (cat 8): 5 situations
- Two pair (cat 10): 3 situations
- Overpair (cat 9): 2 situations (careful with A-high boards + KK)

**Street:**
- Flop: 12 situations (OOP c-bet is primarily flop)
- Turn: 3 situations (delayed c-bet after villain checks flop)

---

### BP3 (20 situations): PFA Semi-Bluff C-Bet

**Feature ranges that must be covered:**

| Feature | Required span |
|---------|--------------|
| draw_outs | 4-15 |
| flush_draw_rank | 0-14 (varies by sub-condition) |
| flush_block_pct | 0-0.30 |
| villain_air_pct | 0.35-0.55 |
| high_card_rank | 12-14 |
| flush_danger | 0.10-0.50 |

**Board textures:**

- 4A (combo draw): boards where both FD + SD coexist (two-tone, connected)
  Example: Ks-7s-6d (spade FD + 8-5 OESD), Qh-9h-8c (heart FD + JT OESD)
- 4B (NFD + blocker): two-tone boards, hero holds nut-suit card
  Example: Qs-8s-4d (hero holds Ks, NFD)
- 4C (nut draw + board favour): K-high two-tone boards
- 4D (blocker + weak draw): A/K-high rainbow boards

**Hero hand types (all is_made_hand = 0):**

- Combo draw (FD + OESD): 8 situations (sub-condition 4A)
  - draw_outs: 12-15
  - Example: Jh-Th on Qh-8h-9d (15 outs: 9 FD + 6 OESD unique)
- Near-nut FD (sub-conditions 4B + 4C): 9 situations
  - draw_outs: 9
  - flush_draw_rank: 12-14
- Gutshot + blocker (sub-condition 4D): 3 situations
  - draw_outs: 4-6
  - flush_block_pct: > 0
  - is_rainbow: 1 (required for 4D)

**Streets:**
- Flop: 12 situations (semi-bluffs have more outs and equity pre-runout)
- Turn: 8 situations (fewer outs remain on turn; include situations where draw
  did not improve on turn but hero still has sufficient equity)

---

### BP4 (15 situations): IP Thin Value Non-PFA

**Feature ranges that must be covered:**

| Feature | Required span |
|---------|--------------|
| hand_category | 7-10 |
| danger_score | 0.10-0.35 |
| villain_top_pair_plus_pct | 0.10-0.35 |
| villain_aggression_count | 0-1 |
| SPR | 3.0-12.0 |

**Board textures:**

- All boards must have danger_score <= 0.35
- Prefer rainbow (flush_danger <= 0.10) for cleanest thin value spots
- May include two-tone with low flush_danger (0.15-0.25) as long as danger_score stays low

**Hero hand types:**

- TPGK (cat 7): 6 situations (mid-board top pairs)
- TPTK (cat 8): 4 situations
- Overpair (cat 9): 3 situations
- Two pair (cat 10): 2 situations

**villain_range_capped rationale per situation:**

Document why villain_range_capped = 1 in each situation. Common reasons:
1. Villain cold-called (would have 3-bet premiums) — preferred structure
2. Villain is in BB (checked option, wider range but no premiums above open-raise threshold)
3. Villain limped preflop (if applicable to the action sequence)

---

### BP5 (10 situations): OOP Value Exception

**Feature ranges that must be covered:**

| Feature | Required span |
|---------|--------------|
| raw_equity | 0.65-0.80 |
| villain_air_pct | 0.45-0.55 |
| villain_fold_equity_estimate | 0.35-0.55 |
| hand_category | 8-11 |
| connectivity_score | 1-3 |

**Board textures:**

- All 4+ boards must be rainbow (is_rainbow = 1) AND connectivity_score <= 3
- Low boards preferred (7-high, 8-high, 9-high) for high villain_air_pct
- Paired low boards acceptable: villain's range has few pairs on low paired boards

**Hero hand types:**

- Two pair (cat 10): 4 situations
- Trips (cat 11): 2 situations
- Set (appropriate category): 2 situations
- TPTK (cat 8): 2 situations (on very low boards where hero's top pair has A kicker)

---

### BP6 (10 situations): CHECK Counterexamples

**Feature ranges:**

Must illustrate the specific feature that caused the failure. For BP6-E
(villain_air_pct gate failure), the situation must have villain_air_pct in
the range 0.25-0.39 — close to 0.40 but below the gate. For BP6-G
(dry-board monster trap), danger_score must be clearly below 0.45 (use 0.20-0.30).

**Board textures:**

BP6-A: wet boards (flush_danger >= 0.60 or straight_danger >= 0.50)
BP6-D: Tier 4 boards (connected or monotone)
BP6-G: dry board (rainbow, danger_score < 0.30)
Others: standard textures matching their BP counterpart (to show that
the board texture alone does not determine the CHECK outcome)

---

## Totals Table

| Sub-pattern | Code | Situations | Intended label | Target step |
|-------------|------|-----------|----------------|-------------|
| IP PFA value c-bet | BP1 | 30 | BET | 3A |
| OOP PFA value c-bet | BP2 | 15 | BET | 3B |
| PFA semi-bluff c-bet | BP3 | 20 | BET | 4A-D |
| IP thin value non-PFA | BP4 | 15 | BET | 5 |
| OOP value exception | BP5 | 10 | BET | 6 |
| CHECK counterexamples | BP6 | 10 | CHECK | Default/suppressors |
| **Total** | | **100** | | |

BET-intent: 90 situations
CHECK-intent: 10 situations

**Projected label yield after expert review:**

Some designed-BET situations will be relabelled CHECK by the expert after
full context evaluation. Based on RAISE batch yield (~85%), expect:
- BP1: ~25-26 confirmed BET
- BP2: ~12-13 confirmed BET
- BP3: ~16-17 confirmed BET
- BP4: ~12-13 confirmed BET
- BP5: ~8-9 confirmed BET
- BP6: 10 confirmed CHECK
- Projected net: ~73-78 BET labels from this batch

Combined with the 9 BET labels from the current 563-situation dataset,
total BET labels will reach approximately 82-87. This is sufficient to
begin training a BET classifier that can generalize across IP PFA, semi-bluff,
thin-value, and OOP exception patterns.

---

## Design Constraints — Correctness

- All boards must pass the action sequence validator
- Hero cards must not conflict with board cards
- No boards reused from existing 46-board pool
- No expected labels in situation designs — expert labels fresh
- BP1: every situation must have is_preflop_aggressor = 1 AND is_ip = 1
- BP2: every situation must have villain_air_pct >= 0.40 AND villain_aggression_count = 0
- BP3: every situation must satisfy at least one of sub-conditions 4A-4D
- BP4: every situation must have villain_range_capped = 1 AND danger_score <= 0.35
- BP5: every situation must have villain_aggression_count = 0 AND raw_equity >= 0.65
- BP6: each situation must document which specific condition causes the CHECK
- hand_category references must use numeric encoding (cat >= 7 = TPGK, cat >= 8 = TPTK, etc.)
- All SPR values must be realistic for the action sequence: flop SRP SPR = 8-12,
  NOT the SPR = 1.11 artifact from Batch 1

---

## Reviewer Checklist (BET Context Batch)

The reviewer must document all 18 checks before the batch is approved:

1. Count unique boards. Must be >= 15. None may appear in the existing 46-board list.
2. Count situations per board. No board may have > 8 situations.
3. Count monotone flop boards. Must be <= 1.
4. Compute SPR distribution. At least 3 distinct SPR tiers populated; no tier > 25% of total situations.
5. Count IP vs OOP heroes. IP must be >= 55 situations.
6. Count flop vs turn vs river. Flop: 50-65. Turn: 25-40. River: <= 10.
7. BP1: confirm all 30 have is_preflop_aggressor = 1 AND is_ip = 1.
8. BP1: confirm board tier distribution (>= 5 Tier 1, >= 3 Tier 2, >= 2 Tier 3).
9. BP2: confirm all 15 have villain_air_pct >= 0.40 AND villain_aggression_count = 0.
10. BP2: confirm all 15 have high_card_rank >= 13 AND (is_rainbow = 1 OR flush_danger <= 0.20).
11. BP3: confirm sub-condition allocation (4A: 8, 4B: 6, 4C: 3, 4D: 3). Verify each situation satisfies its sub-condition.
12. BP4: confirm all 15 have villain_range_capped = 1 AND danger_score <= 0.35 AND is_preflop_aggressor = 0.
13. BP5: confirm all 10 have villain_aggression_count = 0 AND raw_equity >= 0.65 AND connectivity_score <= 3.
14. BP6: confirm all 7 failure modes are present. Each situation must have a documented failure condition.
15. R7 check: for BP1, BP3, BP4 — compute villain_fold_equity_estimate range. Must be >= 0.20.
16. R7 check: for BP1, BP3, BP4 — compute villain_air_pct range. Must be >= 0.15.
17. SPR check: no situation on a flop may use effective_stack < 5x pot (would produce SPR < 5, unrealistic for SRP flop).
18. Confirm no hero_cards duplicate within a sub-pattern on the same board.

---

## Tree Version Alignment Check

| Tree step | Key condition | Sub-patterns affected |
|-----------|--------------|----------------------|
| Step 3 primary gate | high_card_rank >= 12 (not board_favour) | BP1, BP3 |
| Step 3A Tier 1 | high_card_rank >= 13, flush_danger <= 0.20, connectivity_score <= 3 | BP1 |
| Step 3A Tier 2 | high_card_rank >= 11, flush_danger <= 0.35, connectivity_score <= 5 | BP1 |
| Step 3A Tier 3 | flush_danger <= 0.50, connectivity_score <= 7 | BP1 |
| Step 3B | villain_air_pct >= 0.40, villain_aggression_count = 0, high_card_rank >= 13 | BP2 |
| Step 4 sub-condition 4A | draw_outs >= 12 (combo draw) | BP3 |
| Step 4 sub-condition 4B | draw_outs >= 9, flush_draw_rank >= 12, flush_block_pct > 0 | BP3 |
| Step 4 sub-condition 4C | draw_outs >= 9, flush_draw_rank >= 13, board_favour >= 0.30, is_ip = 1 | BP3 |
| Step 4 sub-condition 4D | flush_block_pct > 0, draw_outs >= 4, villain_air_pct >= 0.40, is_ip = 1, high_card_rank >= 13, is_rainbow = 1 | BP3 |
| Step 5 | villain_range_capped = 1, villain_top_pair_plus_pct <= 0.35, danger_score <= 0.35, is_preflop_aggressor = 0 | BP4 |
| Step 6 | raw_equity >= 0.65, villain_air_pct >= 0.45, is_rainbow = 1, connectivity_score <= 3, villain_aggression_count = 0 | BP5 |
| S1 wet bluff suppressor | flush_danger >= 0.60 OR straight_danger >= 0.50, is_made_hand = 0, draw_outs < 12 | BP6-A |
| S2 OOP suppressor | is_ip = 0, hero_range_percentile < 0.72, raw_equity < 0.60 | BP6-B |
| S3 aggressor suppressor | villain_aggression_count >= 2, hero_range_percentile < 0.85 | BP6-C |

All thresholds in this brief use the recalibrated values from BET_DECISION_TREE_V1.md
(9 April 2026). connectivity_score is an integer 0-10. board_favour is retained
as a secondary feature (used in sub-condition 4C) but NOT as a primary gate.

---

*File: `/home/rupertbeytell/river-rats-v2/review/FACTORY_DESIGN_BET_CONTEXTS.md`*
*Status: Ready for reviewer then owner approval. Not yet approved or integrated.*
