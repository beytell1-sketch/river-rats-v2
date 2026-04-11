# 3-Way Pot Research: Preflop Range Construction and Board Texture Interactions

**Date:** 2026-04-06
**Scope:** Quantified findings on preflop ranges (CO open / BTN flat / BB defend) and how board texture interacts with range advantage in 3-way postflop pots. Cash game, 100bb, 6-max context unless noted.

---

## 1. Preflop Range Construction: CO Open / BTN Flat / BB Defend

### 1.1 CO Opening Range

| Metric | Value | Source Type |
|--------|-------|-------------|
| Range width | ~27-28% of hands | Solver-based |
| Composition | 33+, A2s+, K3s+, Q6s+, J8s+, T7s+, 97s+, 87s, 76s, A8o+, KTo+, QTo+, JTo | Solver-based |

- CO opens a relatively wide, **uncapped** range containing all premium pairs (AA-QQ), strong broadways (AKs/AKo, AQs), suited connectors, suited aces, and medium pairs.
- This is a **linear** range: strongest hands at the top, trailing off in a continuous fashion.

**Source:** [MyPokerCoaching - Cash Game Opening Ranges 100BB](https://www.mypokercoaching.com/optimal-cash-game-opening-ranges-100bb/) (solver-based); [GTO Wizard - Preflop Range Morphology](https://blog.gtowizard.com/preflop-range-morphology/) (solver-based)

### 1.2 BTN Flatting Range vs CO Open

| Metric | Value | Source Type |
|--------|-------|-------------|
| BTN 3-bet frequency vs CO | ~12% of hands | Solver-based |
| BTN flat (call) frequency vs CO | ~5% of hands | Solver-based |
| Total BTN continue vs CO | ~17% | Derived |

**Composition of the BTN flat range:**
- Small to medium pocket pairs (22-TT, some JJ mixed)
- Suited connectors (76s, 87s, 98s, T9s, JTs)
- Suited aces (A2s-A5s, some A9s-type hands)
- Some suited kings and suited broadway (KTs, QJs)
- Offsuit broadways (KQo, QJo at low frequency)

**Critical property -- CONDENSED and partially CAPPED:**
- BTN's flatting range is **condensed**: mostly medium-strength hands, few trash hands at the bottom, few nutted hands at the top.
- BTN's flatting range is **capped**: AA, KK, QQ, AKs are almost always 3-bet, not flatted. There is essentially no trapping with AA and very little with AKs or KK in the call range.
- This means postflop, BTN's calling range is missing the strongest overpairs and top-pair-top-kicker combos on many boards.
- The range "hits most boards well" due to its connectedness and suitedness, but cannot make the absolute nuts as frequently as CO's uncapped opening range.

**BTN 3-bet range (for contrast):** Contains AA, KK, QQ, AKs, AKo, plus bluff 3-bets with suited Ax blockers and some suited connectors. This is a **polarized** range (premiums + bluffs).

**Source:** [GTO Wizard - Playing Calls From the Button in Cash Games](https://blog.gtowizard.com/playing-calls-from-the-button-in-cash-games/) (solver-based); [GTO Wizard - Range Morphology](https://blog.gtowizard.com/range-morphology/) (solver-based); [poker.pro - CO vs BTN Flat](https://www.poker.pro/strategy/how-to-play-one-of-the-most-annoying-spots-in-6-max-cash-games-co-vs-btn-flat/) (solver-based)

### 1.3 BB Defend (Overcall) Range in 3-Way Pot

| Metric | Value | Source Type |
|--------|-------|-------------|
| Pot odds for BB overcall | ~19% equity needed (1.5bb to win ~8bb) | Theoretical |
| BB squeeze frequency | Variable; threat of squeeze constrains BTN's flat range | Solver-based |
| BB overcall composition | Speculative, suited, connected hands | Solver-based |

**BB overcall range characteristics:**
- BB gets excellent pot odds (~19% equity needed vs ~27% heads-up), which widens the calling range.
- However, being OOP against two opponents offsets some of the price advantage.
- BB's overcalling range skews toward: suited connectors, suited one-gappers, small pairs, suited aces -- hands with **implied odds and nut potential**.
- BB avoids overcalling with hands that make marginal top pairs (e.g., K7o, Q8o) because these have poor playability multiway OOP.
- BB's overcalling range is **capped** (premiums would squeeze) and somewhat **condensed**, but broader than BTN's flat.
- BB also has a squeeze range (3-bet over CO open + BTN call) that is tighter than a standard 3-bet and weighted toward strong value + suited blockers.

**Source:** [GTO Wizard - Overcalling From the BB](https://blog.gtowizard.com/overcalling-from-the-bb/) (solver-based); [Upswing Poker - Multiway Pot Preflop Squeezing](https://upswingpoker.com/multiway-pot-preflop-squeezing-leaks/) (theoretical)

---

## 2. Range Morphology Definitions

These terms recur throughout multiway analysis:

| Term | Definition | Example |
|------|-----------|---------|
| **Linear** | Top-down value, strongest hands included | CO opening range |
| **Polarized** | Nuts + bluffs, very little middle | BTN 3-bet range; BB squeeze range |
| **Condensed** | Medium hands, few nuts or trash | BTN flatting range vs EP/CO open |
| **Capped** | Missing the very strongest hands | BB calling range (no AA); BTN flat (no AA/KK) |
| **Uncapped** | Contains the strongest possible hands | CO opening range; any 3-betting range |

**Source:** [GTO Wizard - Preflop Range Morphology](https://blog.gtowizard.com/preflop-range-morphology/) (solver-based); [GTO Wizard - Range Morphology](https://blog.gtowizard.com/range-morphology/) (solver-based)

---

## 3. C-Bet Frequency: 3-Way vs Heads-Up

### 3.1 Aggregate Frequency Drop

| Scenario | C-bet Frequency | Source Type |
|----------|----------------|-------------|
| Heads-up IP vs BB | ~65-70% (varies by texture) | Solver-based |
| 3-way (IP vs two callers) | ~50-60% | Solver-based |
| Checking frequency increase in MW | +11% vs heads-up (LJ example) | Solver-based |

- The preflop raiser c-bets **significantly less often** when facing two callers vs one.
- Large pot-sized c-bets that were used ~18% of the time heads-up drop to ~1.3% multiway.
- The IP player "concentrates nearly all of its strength in the betting range" -- meaning when they do bet, the range is much stronger than in HU pots.

**Source:** [GTO Wizard - Playing In Position Against Two Callers](https://blog.gtowizard.com/playing-in-position-against-two-callers/) (solver-based); [GTO Wizard - 10 Tips for Multiway Pots](https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/) (solver-based)

### 3.2 Sizing Adjustments Multiway

| Context | Recommended Sizing | Source Type |
|---------|-------------------|-------------|
| Default multiway c-bet | 25-33% pot | Solver-based |
| High/paired static boards (MW) | 50-70% pot available | Solver-based |
| Nut advantage + low SPR spots | Overbet possible | Solver-based |

- "Range advantage = more small c-bets. Nut advantage = larger sizes and polarization."
- Default multiway: stop range-betting; use small sizing with a tighter, stronger range.
- Exception: when you hold nut advantage on a favorable texture, larger sizing (50-70% or even overbet) extracts more EV.

**Source:** [GTO Wizard - 10 Tips for Multiway Pots](https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/) (solver-based); [poker.pro - Multiway Muscle: Big-Bet Windows](https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/) (solver-based)

---

## 4. Board Texture: Which Boards Favor Which Player?

### 4.1 Boards Favoring the Preflop Raiser (CO)

**High-card and paired boards (STATIC textures):**

| Board Type | Example | Why It Favors Raiser | C-bet Approach |
|-----------|---------|---------------------|----------------|
| Ace-high dry/rainbow | A-7-2r, A-K-5r | Raiser's range is heavy with Ax, AK, AQ; callers less so | High frequency, small size (33% pot), 70%+ frequency HU |
| Double broadway | A-Q-4r, K-J-3r | Raiser has both top set and second set; callers would have 3-bet those pairs | High frequency, small-to-medium size |
| King-high paired | K-K-5r, Q-Q-5r | Raiser has all premium pairs + broadway; callers' pair-heavy ranges are dominated | Very high frequency (~96% on KK5r in HU; lower but still high MW) |
| Ace-high + broadway | A-K-x | Raiser dominates with AK, AQ, KK, AA combos | 50-66% sizing can outperform small automatic c-bet MW |

- These are **static boards**: the best hand now is very likely to remain the best hand. Equity doesn't shift much across turns/rivers.
- Raiser's edge: uncapped range means they hold more top-set and overpair combos than either caller.

**Source:** [GTO Wizard - Playing In Position Against Two Callers](https://blog.gtowizard.com/playing-in-position-against-two-callers/) (solver-based); [888poker - Flop C-betting Textural Theory](https://www.888poker.com/magazine/flop-cbetting-textual-beginner-theory) (theoretical)

### 4.2 Boards Favoring the BTN Cold Caller

**Connected, middling boards (DYNAMIC textures):**

| Board Type | Example | Why It Favors Cold Caller | Effect on Strategy |
|-----------|---------|--------------------------|-------------------|
| Low connected | 7-6-4r, 9-8-5r | BTN flat range is dense with suited connectors that smash these boards | Raiser must check more often |
| Middle connected | T-8-6, J-9-7 | BTN's suited connectors (T9s, 98s, 87s) interact heavily | Raiser c-bets less, smaller when they do |
| Two-tone middling | 9h-7h-4c | BTN has flush draws + pair+draw combos from suited connectors | BTN never folds flush draws or OESDs |

- BTN's condensed range "hits most boards well" and is "dense with suited connectors, offsuit broadway combinations, and pocket pairs -- hands that interact heavily with" connected textures.
- On these boards, BTN flops fewer weak draws than BB and, combined with positional advantage, is less inclined to fold them.
- BTN "never folds a flush draw or an open-ended straight draw" in these spots.

**Source:** [poker.pro - CO vs BTN Flat](https://www.poker.pro/strategy/how-to-play-one-of-the-most-annoying-spots-in-6-max-cash-games-co-vs-btn-flat/) (solver-based); [GTO Wizard - Monkey in the Middle](https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/) (solver-based)

### 4.3 Boards Favoring the BB Defender

**Low, unconnected boards and specific texture-changing turns:**

| Board Type | Example | Why It Favors BB | Notes |
|-----------|---------|-----------------|-------|
| Low rainbow | 5-3-2r, 7-4-2r | BB overcalls with suited connectors, small pairs; these boards give BB two-pair, sets, and pair+draw combos | BB can develop a leading/donk range |
| Texture-changing turns | e.g., T-7-5-6 | BB holds more wrap-around straight combos from suited connectors | BB "depends on a texture-changing turn to develop a betting range" |

- BB rarely leads the flop in 3-way pots unless they have a nut advantage on the specific texture.
- On T-7-5-6r, BB has a pronounced nut advantage toward the bottom of ranges (strong one-pair + pair-draw combos like 54, 64, 86).
- BB's probe (lead on turn after flop checks through) is "generally to leverage a nuts advantage, which is best done with a large, polarized betting strategy."
- BB rarely probes a blank turn; only does so for a small size. On a connecting turn card, probes much more frequently.

**Source:** [GTO Wizard - Probing Out Of Position in 3-Way Pots](https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/) (solver-based)

---

## 5. Range Advantage vs Nut Advantage in 3-Way Pots

### 5.1 Key Distinction

| Concept | Definition | Betting Implication |
|---------|-----------|-------------------|
| **Range advantage** | Your range has higher average equity across all combos | Bet frequently, small sizing |
| **Nut advantage** | Your range contains more of the strongest possible hands | Bet less frequently but larger, polarized |

- In heads-up pots, range advantage alone can justify frequent c-betting.
- **In 3-way pots, both range and nut advantage are significantly reduced** compared to heads-up.
- "Betting frequencies in multiway pots strongly correlate with **nut advantage**."
- "A player with a range advantage that lacks the strongest hands should typically play more passively (unless the SPR is very low)."
- This means: in 3-way, having a slight range advantage is NOT enough to c-bet frequently. You need the nuts.

### 5.2 How This Maps to Each Player

| Player | Range Advantage | Nut Advantage | Typical Strategy |
|--------|----------------|---------------|-----------------|
| CO (OOP raiser) | Moderate (widest, uncapped, but OOP) | Strong on high boards (AA, KK, AK) | C-bet selectively; check more than HU |
| BTN (IP cold caller) | Condensed (good equity density) | Weak (capped -- no AA/KK/AK) | Mostly reactive; bet when checked to on favorable textures; cannot rep the nuts easily |
| BB (OOP overcaller) | Weakest overall | Occasional (sets from small pairs, bottom of deck straights) | Mostly check-call/check-fold; lead on specific nut-favoring turns |

### 5.3 The IP BTN Paradox

When action checks to BTN in 3-way:
- BTN "holds many strong-yet-vulnerable value hands (like AQ, KK, and AA)" -- but wait, BTN flatted preflop, so KK and AA are rarely in range.
- The solver data on BTN betting when checked to likely refers to **BTN as the IP preflop raiser** (e.g., BTN opens, SB and BB call). In that formation, BTN bets ~50-60% when checked to and concentrates nearly all strength in the betting range.
- When BTN is the **cold caller** (CO opens, BTN flats), BTN's betting opportunities come from their condensed range advantage on favorable textures, but they must be cautious because CO retains an uncapped checking range.

**Source:** [GTO Wizard - 10 Tips for Multiway Pots](https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/) (solver-based); [GTO Wizard - Playing In Position Against Two Callers](https://blog.gtowizard.com/playing-in-position-against-two-callers/) (solver-based); [GTO Wizard - Barreling as IP Cold-Caller](https://blog.gtowizard.com/barreling-as-ip-cold-caller/) (solver-based)

---

## 6. Dynamic vs Static Boards: How 3-Way Changes Strategy

### 6.1 Static Boards (Dry, Rainbow, High-Card)

| Property | Heads-Up | 3-Way |
|----------|----------|-------|
| C-bet frequency | Very high (range-bet viable) | Reduced but still high on best textures |
| Sizing | Small (25-33% pot) | Small (25-33% pot), same logic |
| Raiser advantage | Strong | Still strong but diluted by second caller |
| Key textures | A-7-2r, K-8-3r, Q-Q-5r | Same boards; raiser still has structural edge |
| Caller(s) response | Fold a lot | Fold a lot, but two ranges folding simultaneously is multiplicative (harder) |

- On static boards, the best hand now stays the best hand -- turn/river cards rarely flip equity.
- "When hand values are static, sizing up turns your structural edge into chips."
- On paired boards like K-K-7r, Q-Q-5r: the raiser's premium pairs dominate, and neither caller has sets frequently.

### 6.2 Dynamic Boards (Connected, Suited, Middling)

| Property | Heads-Up | 3-Way |
|----------|----------|-------|
| C-bet frequency | Lower than static, but still moderate | Significantly lower; check more often |
| Sizing | Larger (55-80% pot) when betting | Typically smaller (25-33%), with occasional larger sizing with nut hands |
| Raiser advantage | Moderate | Weakest -- callers' suited connectors connect well |
| Key textures | J-T-8, 9-7-6, T-8-5 | Same; BTN and BB ranges both interact heavily |
| Caller(s) response | More calls and raises | Even more resistance; rarely fold draws |

- On dynamic boards, equity shifts dramatically across streets. This favors hands with draw potential.
- "On a board like Kd-Jd-8h, you should c-bet less frequently but can size bigger when you do."
- In 3-way: the raiser's checking frequency increases even further because two ranges interact with connected textures.
- BTN's cold-call range is built specifically for these textures (suited connectors, pairs).
- On wet/dynamic boards in 3-way: "stop range-betting" -- only bet with genuine value and strong draws.

### 6.3 Big-Bet Windows in 3-Way (Exceptions to "Always Small")

Certain specific textures justify larger bets even multiway:

| Trigger | Example | Sizing | Why |
|---------|---------|--------|-----|
| Front door flush completes (turn) | A-9-4 two-tone, turn completes flush | 70-90% pot | Nut flush holder locks equity; two opponents are drawing dead/thin |
| Board pairs on turn | K-8-3r, turn 3 | Large | Opponents' two-pair density collapses; overpairs/top pairs hold |
| High/paired + nut advantage + low SPR | A-A-x, K-K-x with SPR < 3 | Overbet/jam | Structural advantage + stack commitment = maximum pressure |

- "While 'always small' is a helpful starting point in multiway pots, it leaves money on the felt when nut edge, last action, and low SPR converge."

**Source:** [poker.pro - Multiway Muscle: Big-Bet Windows](https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/) (solver-based); [SplitSuit - Continuation Betting In Multi-Way Pots](https://www.splitsuit.com/cb-in-multi-way-pots) (theoretical/solver-informed)

---

## 7. CO as OOP Raiser: Specific 3-Way Data Points

When CO opens, BTN flats, BB calls (CO is OOP in a 3-way pot):

| Board | CO Response to 1/4 Pot C-bet | BTN Behavior | BB Behavior | Source |
|-------|------------------------------|-------------|-------------|--------|
| K-7-2r (static) | Raises 16%, calls 54% | Positional; rarely folds strong | Folds ~68% | Solver |
| T-7-4tt (dynamic) | Raises 30%, calls 39% | Holds draws, does not fold FDs/OESDs | Folds ~45% | Solver |

- On the static board, CO is less aggressive (fewer raises, more calls) because equity is stable.
- On the dynamic board, CO raises more to deny equity before draws complete.
- BB folds far less on the dynamic board (~45% vs ~68%) because they hold more draws and connected hands.

**Source:** [GTO Wizard - Monkey in the Middle: 3-Way Pot Heuristics](https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/) (solver-based)

---

## 8. Summary of Key Quantified Findings

1. **CO opens ~27-28%**, BTN 3-bets ~12% and flats ~5%, BB overcalls with speculative hands needing ~19% equity.
2. **BTN's flat range is condensed and capped** -- no AA/KK/QQ/AKs. Composed of suited connectors, small-medium pairs, suited broadways.
3. **C-bet frequency drops ~10-15% going from HU to 3-way.** Large c-bets (~pot size) nearly disappear (18% HU to 1.3% MW).
4. **Default multiway sizing: 25-33% pot.** Exception: nut advantage on static/paired/completing textures allows 50-90%.
5. **Nut advantage drives betting frequency MW**, not range advantage alone.
6. **High/paired boards strongly favor the raiser** (AA, AK, KK combos). Connected/middling boards favor the callers (suited connectors, pairs).
7. **BB rarely leads** except on texture-changing turns where their nut advantage develops (pair+draw combos, made straights).
8. **BTN as cold caller** is mostly reactive -- bets when checked to on favorable textures but must respect CO's uncapped checking range.

---

## 9. Source Index

All sources used, with classification:

| # | Source | URL | Type |
|---|--------|-----|------|
| 1 | GTO Wizard - Playing In Position Against Two Callers | https://blog.gtowizard.com/playing-in-position-against-two-callers/ | Solver-based |
| 2 | GTO Wizard - Monkey in the Middle: 3-Way Pot Heuristics | https://blog.gtowizard.com/monkey-in-the-middle-3-way-pot-heuristics/ | Solver-based |
| 3 | GTO Wizard - 10 Tips for Multiway Pots | https://blog.gtowizard.com/10-tips-multiway-pots-in-poker/ | Solver-based |
| 4 | GTO Wizard - Playing Calls From the Button in Cash Games | https://blog.gtowizard.com/playing-calls-from-the-button-in-cash-games/ | Solver-based |
| 5 | GTO Wizard - Preflop Range Morphology | https://blog.gtowizard.com/preflop-range-morphology/ | Solver-based |
| 6 | GTO Wizard - Range Morphology | https://blog.gtowizard.com/range-morphology/ | Solver-based |
| 7 | GTO Wizard - Overcalling From the BB | https://blog.gtowizard.com/overcalling-from-the-bb/ | Solver-based |
| 8 | GTO Wizard - Probing Out Of Position in 3-Way Pots | https://blog.gtowizard.com/probing-out-of-position-in-3-way-pots/ | Solver-based |
| 9 | GTO Wizard - Barreling as IP Cold-Caller | https://blog.gtowizard.com/barreling-as-ip-cold-caller/ | Solver-based |
| 10 | GTO Wizard - GTO Wizard AI 3-Way Benchmarks | https://blog.gtowizard.com/gto_wizard_ai_3_way_benchmarks/ | Solver-based |
| 11 | poker.pro - Multiway Muscle: Big-Bet Windows | https://www.poker.pro/strategy/multiway-muscle-big-bet-windows-revealed-by-gto-wizard/ | Solver-based |
| 12 | poker.pro - CO vs BTN Flat in 6-Max Cash | https://www.poker.pro/strategy/how-to-play-one-of-the-most-annoying-spots-in-6-max-cash-games-co-vs-btn-flat/ | Solver-based |
| 13 | MyPokerCoaching - Cash Game Opening Ranges 100BB | https://www.mypokercoaching.com/optimal-cash-game-opening-ranges-100bb/ | Solver-based |
| 14 | MyPokerCoaching - Multiway Pots Strategy | https://www.mypokercoaching.com/multiway-pots-strategy-tips/ | Theoretical/solver-informed |
| 15 | Upswing Poker - Multiway Pot Preflop Squeezing | https://upswingpoker.com/multiway-pot-preflop-squeezing-leaks/ | Theoretical |
| 16 | SplitSuit - Continuation Betting In Multi-Way Pots | https://www.splitsuit.com/cb-in-multi-way-pots | Theoretical/solver-informed |
| 17 | 888poker - Flop C-betting Textural Theory | https://www.888poker.com/magazine/flop-cbetting-textual-beginner-theory | Theoretical |
| 18 | GTO Wizard - Custom Multiway Solving | https://blog.gtowizard.com/gto-wizard-ai-custom-multiway-solving/ | Solver-based |
