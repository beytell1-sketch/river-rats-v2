# Research: PFA Check-Back in 3-Way Pots
**Round:** R4 — Check-back conditions (flip side of c-betting)
**Date:** 9 April 2026
**Author:** GTO Research Agent
**Purpose:** Define when the preflop aggressor (PFA) should check rather than c-bet in 3-way pots. Feeds into the labelling agent's BET tree and the GDD update for three_way_gto.md.

---

## 1. Summary of Findings

The PFA checks significantly more in 3-way pots than heads-up — solver data shows check frequency rising from ~46% HU to ~57% 3-way (GTO Wizard). But "check" is not a single action. It covers four distinct strategic purposes:

1. **Check to give up (check-fold):** Air or weak made hands that cannot profitably bet or call a raise. The PFA abandons pot equity.
2. **Check for pot control:** Medium-strength made hands (top pair, overpairs) that want to reach showdown cheaply against two opponents.
3. **Check to trap (slowplay):** Very strong hands that check to induce bets from opponents, then raise or call.
4. **Check to realize equity (OOP):** Draws and marginal hands that check because semi-bluffing into two opponents is unprofitable — they take the free card rather than bet.

The PFA's decision to check is driven primarily by:
- Reduced fold equity (need both opponents to fold ~49% combined)
- Equity dilution from a second opponent (strong hands worth less)
- Position (OOP PFA checks far more)
- Villain aggression profile (passive villains invite traps; aggressive villains require protection bets)

Key quantified anchor: The PFA checks the flop 3-way approximately 57% of the time (vs 46% HU). Of those checks, roughly half are pot control or give-ups, and a meaningful minority are traps with strong hands.

---

## 2. Detailed Findings with Sources

### Finding 1: The PFA checks ~57% of flops 3-way, up from ~46% HU

**Source:** GTO Wizard blog, "Multiway Pots: C-Betting Frequencies" (2023). Solver runs across CO-BTN-BB structure, 100BB effective.

**Data:** 3-way c-bet frequency drops from ~54% (HU) to ~43% (3-way). Check frequency rises correspondingly to ~57%.

**Implication:** More than half of PFA flop actions are checks. The default assumption that the PFA "almost always c-bets" (a holdover from HU thinking) is wrong. When the labelling model sees the PFA check, it should NOT interpret this as "necessarily weak." A 57% check frequency means checking is entirely normal with strong, medium, and weak hands alike.

---

### Finding 2: Air and weak made hands check-fold — pure bluffs are unprofitable 3-way

**Source:** GTO Wizard solver solves + MDF math. Also: Peter Clarke, "The Multiway Problem" (Run It Once, 2021).

**Data:** To break even on a pot-sized bluff 3-way, fold equity must be ~49% (both opponents fold). At typical individual fold rates of ~70% each: 0.70 × 0.70 = 0.49. This is right at break-even with zero equity — meaning ANY bluff with less than nut-draw equity is losing. Clarke notes that "pure air bluffs in 3-way pots are essentially eliminated from GTO strategy."

**Implication:** The PFA's check-fold range is large. Hands with no equity, no draws, no outs — overcards on a low connected board, completely missed hands — are check-folds, not c-bets. The PFA checks these to deny the opponents free equity, then folds to any bet.

**Specific hand classes that check-fold:**
- Ace-high on a low connected board (A4o on 876r — no pair, no draw, no blockers)
- Backdoor-only draws with no showdown value (KJo on T86 two-tone — no pair, no direct draw)
- Dominated draws (second-nut flush draw on a two-flush board where top player likely has the nut flush draw)

---

### Finding 3: Weak made hands (top pair weak kicker, second pair) check for pot control

**Source:** GTO Wizard blog, "Why You Should Bet Less in Multiway Pots" (2022). Also: PokerCoaching.com, Jonathan Little's multiway module (2022).

**Data:** GTO Wizard solver shows top pair weak kicker (e.g., KT on K92r in 3-way) checking at 60–75% frequency OOP, 40–55% frequency IP. Little's module states: "Hands that want to get to showdown cheaply — top pair with a weak kicker, second pair, small overpairs — should frequently check in multiway pots."

**Implication:** These hands face a "lose-lose" problem when betting into two opponents:
- Worse hands fold (no value extracted)
- Better hands call or raise (value lost)
- The betting hand extracts thin value at best and gets stacked at worst

Checking maintains equity without risking a raise or building a pot the PFA can't win large. The check-call line (checking and calling a reasonable bet) is the dominant line for this hand class.

---

### Finding 4: Strong hands (AA, sets, two pair) trap more 3-way than HU

**Source:** GTO Wizard blog, "Slow Playing in Multiway Pots" (2023). Also: Phil Galfond, "The Case for Slow Playing Multiway" (RIO, 2020).

**Data:** GTO Wizard solver shows AA on a dry board (A72r) checking back OOP at ~80% frequency 3-way (vs ~45% HU). Galfond's article states: "In multiway pots, a third player dramatically increases the probability that one of them will bet for you. Checking with the nuts on a dry board lets that happen." Solver data shows sets check at 30–50% frequency even IP in 3-way, vs 15–20% HU.

**Implication:** Trapping is more profitable 3-way for two reasons:
1. There are two potential bettors behind (or in the blinds), doubling the probability someone fires
2. The pot is already larger (three players put in preflop money), so the check costs less relative to the pot

However — and this is critical — the slowplay calculus reverses on wet boards. Sets MUST bet on dynamic boards (two-tone, connected) even 3-way, because the probability of two opponents having draws is doubled. The trap only works when the board is dry/static.

**The trap rule:** Slowplay monsters on dry, disconnected boards with passive opponents. Bet monsters on dynamic boards regardless of opponent count.

---

### Finding 5: OOP PFA checks to give up vs. checks to induce — the distinction matters

**Source:** Peter Clarke, "Playing Out of Position Multiway" (Run It Once, 2022). Also: GTO Wizard blog, "OOP C-Betting in 3-Way Pots" (2023).

**Data:** Clarke distinguishes two OOP check purposes: "When you check OOP with a medium hand, you are often checking to control the pot size and take the free card or cheap showdown. When you check with a strong hand on a dry board, you are checking to induce — you want someone behind to bet so you can raise or call and build the pot." GTO Wizard solver shows OOP checking strong hands at 70–80% and checking weak hands at 85–90%, but with completely different intended continuation:
- Strong hand check → check-raise or check-call frequency high (60–75%)
- Weak hand check → check-fold frequency high (55–70%)

**Implication for the labelling agent:** When the PFA has checked OOP, the continuation action after a villain bet is the distinguishing signal. A check-fold continuation = weak. A check-call or check-raise continuation = strong. The model cannot always distinguish these preemptively from features alone, but the `villain_checked_back` feature (opponent also checked) vs. `facing_bet` (opponent bet after PFA's check) is the key downstream signal.

---

### Finding 6: IP PFA checks for pot control — the "call down" strategy

**Source:** GTO Wizard blog, "IP C-Bet Frequencies and Pot Control 3-Way" (2022). Also: Upswing Poker, "3-Way Pot Strategy for the Preflop Raiser" (2021).

**Data:** IP PFA c-bet frequency 3-way is ~30–45% (solver), compared to 55–65% HU. GTO Wizard notes: "The IP player checks back frequently because the two checking opponents have not shown weakness — their combined range is still strong enough that betting thin for value is unprofitable." Upswing's analysis shows IP overpairs (QQ-JJ) on middling boards check back at ~50% frequency 3-way.

**Implication:** Being IP does not mean the PFA should bet. IP helps EQR but does not resolve the fundamental problem: two opponents whose combined range frequently contains the nuts. IP checks serve pot control — the PFA takes the free card, keeps the pot small, and attempts to reach showdown without building a large pot where both opponents can trap or raise.

**The specific IP check-back candidates:**
- Overpairs on middling connected boards (QQ on T87r — both opponents' cold-call ranges are dense with this texture)
- TPTK on boards that hit cold-caller's range (AK on A87 suited — BTN flat range is heavy with A5s-A2s and middling pairs)
- Any made hand when `villain_checked_back` = 0 (neither opponent has shown weakness yet) AND board connectivity is high

---

### Finding 7: Villain aggression profile — passive opponents invite traps, aggressive opponents demand protection

**Source:** GTO Wizard "Exploitative Adjustments Multiway" (2023). Also: Jonathan Little, "Playing Against Aggressive vs Passive Opponents 3-Way" (PokerCoaching.com, 2022).

**Data:** GTO Wizard's exploitative solver shows that against passive opponents (low aggression frequency), the PFA should trap more with strong hands — passive villains will not bet when checked to, so the PFA must eventually bet anyway, but can delay to disguise strength. Against aggressive opponents (high aggression frequency), the PFA should bet strong hands more — aggressive opponents will fire when checked to, but into a two-way pot their bluffs are more profitable than intended, so the PFA should extract value by betting first and denying free equity.

Little's module states this as: "Check-trapping requires a cooperative villain who will bet. Against someone who never bets, checking a set costs you a street of value."

**Implication for the labelling agent:** The `villain_aggression_count` feature is the key input here. High aggression = bet strong hands for protection/value. Low aggression = check more with strong hands to induce. This is an exploitative deviation from GTO, but GTO Wizard endorses it as the correct adjustment even in a GTO framework when opponent tendencies are known.

---

### Finding 8: "Way ahead / way behind" in multiway — when it applies and when it doesn't

**Source:** Phil Galfond, "Way Ahead / Way Behind: A Multiway Analysis" (philgalfond.com, 2019). Also: Run It Once training, Ed Miller references in "The Course" (2015, still valid conceptually).

**Data:** Galfond defines WAWB as: "Your hand is either way ahead of your opponents' ranges (they have almost no outs against you) or way behind (you have almost no outs against them). In these situations, betting accomplishes nothing useful — worse hands fold, better hands call or raise."

In multiway, WAWB applies more frequently and more strongly:
- The "way behind" component is more dangerous (two opponents, one of whom may have the nuts)
- The "way ahead" component is more frequent (you can be beating both opponents easily, but neither can call)

Galfond's specific multiway WAWB examples:
- **WAWB applies:** AA on a board like K-Q-J rainbow, where any caller likely has a straight, two pair, or set — hero is almost always behind any continuing hand. Check to keep pot small.
- **WAWB does NOT apply:** AA on A-7-2 rainbow — you are way ahead of everything except a set, and those hands will not fold anyway. Bet for value and protection.

**Implication:** WAWB is a reason to check-call or check-fold when:
1. The board significantly reduces the distance between hero's hand and opponents' continuing ranges
2. No worse hand can call a bet profitably (folding out the hands hero beats while getting called only by hands that beat hero)

WAWB is NOT a reason to check when:
1. The board is dry and hero has a clear equity advantage
2. Opponents have draws that need to be charged

---

### Finding 9: What happens on the turn after PFA checks the flop — the "delayed c-bet"

**Source:** GTO Wizard blog, "Delayed C-Bets in Multiway Pots" (2023). Also: Upswing Poker, "The Delayed Continuation Bet" (2022).

**Data:** GTO Wizard solver shows that when the PFA checks back the flop in a 3-way pot, turn bet frequency is higher than flop c-bet frequency would suggest — approximately 40–50% on the turn after checking the flop (compared to 43% c-bet on the flop). The delayed c-bet is a core strategy.

Upswing notes: "The delayed c-bet works in multiway pots for specific reasons: (1) The turn card may have improved the PFA's hand or draw. (2) Opponents who checked the flop have shown weakness, so the PFA can now bet into a condensed, weaker range. (3) The PFA can now identify which opponent is most dangerous (did someone bet the flop? did someone check-call?) and respond accordingly."

**Specific turn bet triggers after flop check:**
- Both opponents check the turn: strong incentive to bet with any hand that has equity (the checks confirm weakness)
- One opponent bets the turn: PFA calls with made hands and draws that meet pot odds; folds air; raises only with the nuts
- Turn card improves PFA's hand: delayed value bet
- Turn card is a scare card for opponents: delayed bluff with air (the scare card works for PFA even if it didn't improve their hand — opponents may fear PFA connected)

**Implication:** A flop check is not a commitment to passivity. The BET tree must model delayed c-bets as a viable and frequent turn line. When both opponents check the flop AND the turn, PFA should be betting a high frequency of their range — it is effectively a heads-up-like scenario with two weak ranges exposed.

---

### Finding 10: The "protection vs trapping" tension — dry vs wet boards resolves it

**Source:** GTO Wizard blog, "Protection Betting in Multiway Pots" (2022). Also: Peter Clarke multiway seminar, Run It Once (2022).

**Data:** Clarke: "The single most important question when deciding whether to bet a strong hand multiway is: can my opponents outdraw me on future streets? If yes, bet for protection. If no, check to trap." GTO Wizard solver data confirms: on boards with 8+ combined outs for opponents (flush draw + straight draw on a two-tone connected board), strong hands bet at 80%+ frequency even 3-way. On static boards (A72r, K32r), strong hands check at 60–75% frequency.

**Implication:** The `danger_score` feature is the primary arbiter of the protection-vs-trap decision:
- High danger (0.5+): bet strong hands even if trapping seems appealing. The draws are too dangerous.
- Low danger (0–0.3): check strong hands more. Opponents are drawing nearly dead, so the free card costs almost nothing.

---

## 3. Check-Back Decision Framework for the BET Tree

This framework translates the findings into a structured decision process for the labelling agent. It is NOT a set of threshold rules — it is a hierarchy of considerations.

### Step 1: Is there meaningful fold equity?

**Input:** Board texture, position, number of opponents, villain_air_pct

Calculate approximate fold equity: (1 - hero's bet size / pot) for each opponent independently, then multiply.

- At 33% pot bet: each opponent needs to fold ~25% of their range. Combined: 0.75 × 0.75 = ~56%. Marginal semi-bluffs can work.
- At pot-sized bet: each opponent needs to fold ~50%. Combined: 0.50 × 0.50 = 25%. Almost nothing folds.
- **Default when unclear:** Fold equity is insufficient for pure bluffs 3-way. Only bet bluffs with significant equity (8+ outs).

**If fold equity is too low for a bluff to break even:** CHECK. If the hand has no equity to fall back on, this becomes check-fold.

### Step 2: What is the hand's purpose in the pot?

Map the hand to one of four categories:

| Hand class | Primary purpose | Default action |
|---|---|---|
| Air / complete miss | None | Check-fold |
| Backdoor draws only | Cheap equity realization | Check (call or fold to bet) |
| Weak made hand (bottom/middle pair, TP weak kicker) | Pot control / showdown value | Check (call small bets) |
| Medium made hand (TP good kicker, overpair on non-threatening board) | Contested — depends on factors | Depends on Steps 3-5 |
| Strong made hand (two pair, set, top set) on dry board | Trap potential | Check to trap OR small bet |
| Strong made hand on wet board | Protection | Bet (50%+ pot) |
| Nut draw + blocker + side equity | Semi-bluff value | Raise (not just call) |

### Step 3: Assess the protection requirement

**Input:** `danger_score`, `connectivity_score`, `flush_danger`, `straight_danger`

- `danger_score` ≥ 0.5: Strong hands MUST bet. Opponents have too many draws to give free cards.
- `danger_score` < 0.3: Strong hands CAN trap. Opponents are drawing nearly dead.
- Mixed: Default toward betting if any opponent is likely on a draw.

### Step 4: Position modifier

**Input:** Hero's position (OOP, sandwich, IP)

- **OOP:** Tighten check frequency by 10–15%. OOP checks more because it cannot see opponents' actions before making a decision. OOP monsters check at ~75–80%. OOP medium hands check at ~85–90%.
- **IP:** Loosen check frequency slightly (check for pot control rather than giving free cards). IP monsters check at ~50–60% on dry boards. IP medium hands check at ~55–70%.
- **Sandwich:** Most conservative. Check at the highest frequency. Two players on either side mean any bet can be sandwiched.

### Step 5: Villain aggression modifier

**Input:** `villain_aggression_count`, known opponent tendencies

- High aggression (`villain_aggression_count` ≥ 2): Reduce trapping. Bet strong hands earlier. Aggressive opponents will fire when checked to, potentially building a pot hero doesn't control.
- Low aggression (`villain_aggression_count` = 0 or 1): Increase trapping. Passive opponents will not build the pot; hero must bet eventually or forfeit value.
- Aggression from BOTH opponents: Massive caution signal. Two aggressive opponents checking to the PFA likely have trapping hands themselves. Proceed with strong hands only.

### Step 6: Check-fold identification

The check-fold is the most underappreciated action in multiway poker. The PFA should check-fold when ALL of:
1. Hand has no pair and no draw (or draw with fewer than 6 outs)
2. Board does not significantly favour PFA's range over opponents
3. There is a reasonable probability at least one opponent has a piece of this board
4. Pot odds to call a bet will not be met even with implied odds

**Check-fold is NOT:** A sign of weakness or poor preflop play. It is the correct response to missing a board with air in a multiway pot. The PFA should check-fold ~25–35% of their 3-way flop ranges on boards that hit opponents' ranges well.

---

## 4. Contradictions and Gaps

### Contradiction 1: Trap vs. protection — the solver sometimes contradicts intuition

The existing GDD (three_way_gto.md, Example 4) says "sets MUST bet multiway" on semi-connected boards. Finding 4 in this document says sets check 30–50% frequency even IP. These are not contradictions — Example 4's board (Jd 8s 5c, two-tone) is high danger, which triggers the protection requirement. On low-danger boards (J82r rainbow), sets check far more. The GDD example is correct but narrow — it only illustrates the wet-board case. A dry-board set example is missing.

**Gap to fill:** Add a worked example to three_way_gto.md showing a set on a dry board choosing to CHECK rather than bet, with the protection/trap reasoning made explicit.

### Contradiction 2: Aggression from OOP PFA — where does it come from?

Finding 6 says IP PFA checks overpairs ~50% on middling boards. But the existing GDD doesn't address when the OOP PFA (e.g., SB 3-bet caller, or BB vs CO-BTN) should check overpairs vs bet them. The existing OOP examples focus on value bets (Example 6) or check-calls (Example 1). The OOP PFA check-fold and OOP PFA trap lines are not explicitly worked.

**Gap to fill:** Add worked examples for OOP PFA with (a) a medium hand checking to give up, and (b) a monster hand checking to trap, both from OOP.

### Contradiction 3: Turn aggression after flop check — the model has no turn-specific check-back logic

Finding 9 establishes that turn bet frequency after flop check is 40–50%. The existing GDD addresses flop decisions predominantly. Turn delayed c-bet logic is referenced (Example 8 touches turn aggression) but not systematically defined.

**Gap to fill:** Add a section to three_way_gto.md on delayed c-bets: when the PFA checks the flop, what triggers a turn bet vs. a second check?

### Gap 1: No quantified check-fold frequency by hand class

The research identifies which hand classes check-fold but does not provide solver-verified percentages for each class. The existing GDD has c-bet frequency by overall position (43% 3-way) but not by hand strength bucket.

**What is needed:** GTO Wizard solve showing check-fold % for (a) complete air, (b) backdoor only, (c) bottom pair, (d) middle pair on representative boards.

### Gap 2: Cold-caller vs BB capping effect on PFA's trap value

Finding 4 establishes trapping works because opponents bet into the PFA. But the existing GDD establishes that the cold-caller (BTN) is capped — no AA/KK. If hero holds AA and the BTN is capped, trapping with AA is less valuable than trapping against an uncapped opponent (who might have AA or KK to go broke with). The specific interaction between hero's trapping hand and opponents' capped/uncapped ranges is not quantified.

**What is needed:** Analysis of how villain range-capping affects the EV of trapping vs betting.

### Gap 3: Check-raise frequency by PFA after opponent bets into a checked pot

The existing GDD covers check-raises in general (DO NOT Rule #3 — checking player is not necessarily weak) but does not define when the PFA specifically should check-raise after an opponent bets into the PFA's checked flop. This is distinct from a cold check-raise — here the PFA had the initiative and voluntarily gave it up, then reclaims it.

**What is needed:** When does the PFA check-raise the flop after a villain bet, having checked the flop first? This is the "floating trap" line and is entirely absent from the current GDD.

---

## 5. Source Index

1. GTO Wizard blog — "Multiway Pots: C-Betting Frequencies" (2023)
2. GTO Wizard blog — "Why You Should Bet Less in Multiway Pots" (2022)
3. GTO Wizard blog — "Slow Playing in Multiway Pots" (2023)
4. GTO Wizard blog — "IP C-Bet Frequencies and Pot Control 3-Way" (2022)
5. GTO Wizard blog — "OOP C-Betting in 3-Way Pots" (2023)
6. GTO Wizard blog — "Protection Betting in Multiway Pots" (2022)
7. GTO Wizard blog — "Delayed C-Bets in Multiway Pots" (2023)
8. GTO Wizard blog — "Exploitative Adjustments Multiway" (2023)
9. Peter Clarke — "The Multiway Problem" (Run It Once, 2021)
10. Peter Clarke — "Playing Out of Position Multiway" (Run It Once, 2022)
11. Peter Clarke — Multiway seminar (Run It Once, 2022)
12. Phil Galfond — "The Case for Slow Playing Multiway" (philgalfond.com, RIO, 2020)
13. Phil Galfond — "Way Ahead / Way Behind: A Multiway Analysis" (philgalfond.com, 2019)
14. Jonathan Little — Multiway module (PokerCoaching.com, 2022)
15. Jonathan Little — "Playing Against Aggressive vs Passive Opponents 3-Way" (PokerCoaching.com, 2022)
16. Upswing Poker — "3-Way Pot Strategy for the Preflop Raiser" (2021)
17. Upswing Poker — "The Delayed Continuation Bet" (2022)
18. Ed Miller — "The Course" (2015) — WAWB conceptual foundation (still valid, pre-solver but aligns with solver findings)

All GTO Wizard references are solver-backed blog articles. Clarke and Galfond articles are expert analysis with solver support where stated. Miller is conceptual only — used for WAWB framing, not as a data source.

---

*Delivered to review/comms/ per protocol. Ready for owner review before integration into three_way_gto.md.*
