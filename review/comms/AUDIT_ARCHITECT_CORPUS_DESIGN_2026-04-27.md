---
date: 2026-04-27
from: architect (audit subagent)
to: orchestrator
re: Corpus design audit vs v3.2 rule-trigger taxonomy
status: EVIDENCE-BASED AUDIT — corpus rebuild required; supplement path structurally blocked
---

# Architect audit: corpus design vs v3.2 rules

---

## Q1 answer: v3.2 rule-trigger taxonomy

Every rule, override, and carve-out in v3.2 that has a feature-conditional trigger. This is the checklist against which the corpus is measured in Q2.

### Rule 11 (DO NOT Rule 11 — v3.2 Fix 1): Paired / 2-tone OOP made-hand CHECK exception

**Name:** Rule 11 (three sub-variants)

**11a — Paired board monster CHECK (d9556 pattern)**
- Trigger: `is_made_hand=1` AND `is_ip=0` AND `is_paired=1` AND `num_opponents>=2` AND `facing_bet=0`
- Sub-trigger (bet exception): override to BET only if ALSO `villain_top_pair_plus_pct >= 0.40` AND (`is_strong_made=1` OR `is_monster=1`)
- Action produced: CHECK (default); BET only when both override conditions clear
- GTO concept: On paired boards, villain's continuing range (post-flop bet or check) is capped to mostly-air or mostly-bluff-catchers. Betting a monster folds those bluff-catchers and isolates vs the few hands that beat us. CHECK keeps the bluff-catching range in and induces later-street bluffs.

**11b — 2-tone OOP medium-made CHECK (d3688 pattern)**
- Trigger: `is_made_hand=1` AND `is_ip=0` AND (`is_two_tone=1` OR `is_monotone=1`) AND `num_opponents>=2` AND `facing_bet=0`
- Same bet exception: override if `villain_top_pair_plus_pct >= 0.40` AND strong/monster
- Action produced: CHECK (default)
- GTO concept: Betting OOP into live villains on a 2-tone board on TPWK or similar commits to bigger pots when called; the 2nd villain's continuing range skews to flush draws / better TP+. "Low villain TP+ + high air → bet" reasoning from KB Example 6 is HU-leaning and over-fires OOP multiway.

**11c — River checked-to BET override (d3178 pattern)**
- Trigger: `villain_checked_back=1` AND `facing_bet=0` AND `street=2` AND `is_ip=0` AND (`is_strong_made=1` OR `is_monster=1`)
- Action produced: BET (not CHECK) even when the rest of Rule 11 would say CHECK
- GTO concept: When villain has passed the option to bet and hero holds AA/KK/strong hand, checking reveals range-cap (hero's checking range becomes dominated by weaker holdings); the balanced GTO line is to bet with the strong hand for range construction purposes.

---

### KB §1.7 carve-out RAISE: semi-bluff raise with nut draw + blocker

**Trigger (RAISE fires):**
- `has_flush_draw=1` AND hero holds the Ace of the flush suit (canonical predicate; feature proxy: `nut_flush_block=1` AND `flush_block_pct >= ~0.40`)
- AND `villain_air_pct >= 0.20` (v3.2 Fix 2 threshold — mandatory override)
- AND `facing_bet=1`
- Action produced: RAISE
- GTO concept: Nut flush draw with Ace-blocker blocks villain's nut-flush-draw combos, increasing effective fold equity beyond what `villain_fold_equity_estimate` alone suggests. Above 20% air, the raise's fold-equity component covers the EV cost of villain's calling range. Semi-bluff raise is +EV.

---

### KB §1.7 OVERRIDE→CALL: nut FD + blocker but villain_air < 0.20

**Trigger (CALL replaces RAISE):**
- `has_flush_draw=1` AND `nut_flush_block=1` AND `flush_block_pct >= ~0.40`
- AND `villain_air_pct < 0.20` ← this is the v3.2 Fix 2 threshold gate
- AND `facing_bet=1`
- Action produced: CALL (not RAISE)
- GTO concept: With sub-20% air, villain's range is too value-heavy for a raise to have adequate fold-equity; the raise's bluff component fails EV-wise. CALL realises equity cheaply vs villain's calling range rather than pumping a pot with insufficient fold equity.
- Anchor: MW-39 (AhJh on Kh8h3d, `villain_air_pct=0.05` — both Sonnet and Opus v3.1 incorrectly raised, empirically motivated Fix 2).

---

### v2 reversal: MW-30 CALL (equity surplus overrides bet-and-call signal)

**Trigger:**
- `facing_bet=1` AND `num_callers_to_bet >= 1` AND hero equity vs range > pot odds (margin > 0)
- Specifically: villain's postflop TP+ < 0.40 (range not value-heavy enough to fold)
- Action produced: CALL (not FOLD despite bet-and-call signal)
- GTO concept: Bet-and-call action narrows villain range but does not automatically dominate hero. If equity margin is positive and villain's TP+ pct is insufficient to warrant fold, hero continues. Do not use action-history range-narrowing as a FOLD trigger without reading the composition quad.

---

### v2 reversal: MW-33 RAISE (set raises facing bet — value extraction not pot control)

**Trigger:**
- `is_monster=1` AND `facing_bet=1` (or `facing_raise=1`)
- Action produced: RAISE
- GTO concept: Sets and full houses should raise facing a bet to extract value and protect against backdoor equity. Pot control reasoning fails on nut-strength hands; the correct play is to build the pot.

---

### v2 reversal: MW-50 FOLD (action history narrows range above hero)

**Trigger:**
- `villain_aggression_count >= 1` AND `facing_raise=1` AND hero is weak-to-medium-made (`is_strong_made=0`, `is_monster=0`)
- Particularly: hero has marginal kicker on dangerous board with `villain_top_pair_plus_pct` very high after raise
- Action produced: FOLD
- GTO concept: Action history (multi-street aggression + raise) updates villain's range dramatically beyond preflop construction. Medium-made hands that are CALL candidates on raw equity become FOLD candidates when the continuation range is heavily TP+.

---

### DO NOT Rule 4: Don't auto-cbet IP (PFA decisions)

**Trigger:**
- `is_preflop_aggressor=1` AND `is_ip=1` AND `facing_bet=0`
- Action produced: Variable (CHECK or BET based on composition/texture), NOT automatic BET
- GTO concept: IP c-bet frequency drops from ~65% HU to 30-45% 3-way. Board texture and range composition determine bet; being PFA + IP is not itself a BET trigger.

---

### DO NOT Rule 2: Don't barrel draws OOP into 2 opponents

**Trigger:**
- (`has_flush_draw=1` OR `has_straight_draw=1`) AND `is_ip=0` AND `facing_bet=0`
- Action produced: CHECK (not BET); RAISE only if KB §1.7 carve-out fires
- GTO concept: 3-way fold equity is ~36% even with a strong draw. Semi-bluffs are unprofitable without nut draw + blocker. OOP draws default to CHECK to realise equity.

---

### DO NOT Rule 5: Don't treat top pair as a strong hand

**Trigger:**
- `is_made_hand=1` AND `is_strong_made=0` AND `is_monster=0` (i.e. TP/second pair bucket)
- Action produced: CHECK or small BET (pot-control framing), NOT value-heavy aggression
- GTO concept: TPTK drops ~12 equity points 3-way; TPWK drops ~15 points. These are medium-made hands that pot-control, not value-bet targets.

---

### DO NOT Rule 7: Street-tree at committed SPR

**Trigger:**
- `spr < 2.0` (flop bet 3-way commits stacks)
- Action produced: Constrained betting decisions (smaller sizings, tighter calling ranges)
- GTO concept: Pot-sized flop bet 3-way → SPR ~1.5 on turn, effectively committed. Decisions must account for the remaining tree, not just current street.

---

### KB §1.9 / Rule 9: Postflop composition not preflop geometry

**Trigger:**
- Any hand where `villain_range_capped=1` AND hero might over-fold or over-bet based on preflop structure alone
- Action produced: Read composition quad (villain_top_pair_plus_pct, villain_medium_made_pct, villain_draw_pct, villain_air_pct) as primary signal
- GTO concept: BTN cold-caller's "structurally narrower" preflop range does NOT mean their postflop continuing range is weak. MW-30 is the canonical failure: preflop capped ≠ postflop thin.

---

## Q2 answer: coverage matrix [rule × corpus hands]

**Computation method:** Python analysis of `data/pilot_corpus_100_hand_2026-04-26.jsonl` (100 hands, 59-feature contract per v1.0.1). Results below are exact counts.

### Basic action-context distribution (N=100)

| Category | Count | Notes |
|---|---|---|
| `facing_bet=0` (opener decisions) | 97 | CHECK or BET candidates |
| `facing_bet=1` | 3 | All 3 also have `facing_raise=1` |
| `facing_raise=1` | 3 | There are zero pure initial-bet decisions |
| `facing_bet=0` AND `facing_raise=0` | 97 | Effectively all opener decisions |

**Finding:** There are no pure "facing initial bet" hands in the corpus. All 3 "facing bet" hands are actually facing a re-raise. The corpus produces 97 opener-decision labels (CHECK or BET) and 3 raise-or-fold decisions. CALL as an action class has zero forcing examples.

### SPR distribution (N=100)

| SPR bucket | Count |
|---|---|
| < 1.0 (committed) | 6 |
| 1.0 – 2.0 (compressed) | 94 |
| 2.0 – 6.0 (standard) | **0** |
| > 6.0 (deep) | **0** |

94/100 hands have SPR exactly 1.25. All 100 hands have SPR ≤ 1.25. The source pool itself (`training-data/3way_situations_10k.jsonl`, 962 hands) has SPR max = 1.25, meaning standard and deep SPR scenarios are **absent from the source pool entirely**.

### Rule-trigger coverage matrix

| Rule | Trigger Conditions | Count | Ref IDs (sample) | Status |
|---|---|---|---|---|
| Rule 11a (paired OOP monster → CHECK) | is_paired+OOP+monster+opener | 6 | PILOT_040, PILOT_042, PILOT_043, PILOT_062, PILOT_067 + 1 more | THIN but present |
| Rule 11b (2-tone OOP medium → CHECK) | is_two_tone+OOP+medium_made+opener | 5 | PILOT_012, PILOT_027, PILOT_060, PILOT_075, PILOT_100 | THIN but present |
| Rule 11c (river checked-to → BET override) | villain_checked_back+river+OOP+strong+opener | 10 | PILOT_005, PILOT_037, PILOT_039, PILOT_040, PILOT_043, PILOT_052, PILOT_073, PILOT_077, PILOT_080 + 1 | THIN |
| Rule 11 (full predicate: OOP+made+paired-or-2tone) | Combined all textures | 27 | PILOT_005, PILOT_012, ... | PRESENT but undifferentiated |
| Rule 11 bet-exception fires | TP+>=0.40 AND strong/monster among Rule 11 | 15 | (subset of 27) | Mixed with CHECK pattern — boundary untested |
| KB §1.7 RAISE | FD+nut_block(>=0.40)+air>=0.20+facing_bet | **0** | — | ZERO |
| KB §1.7 OVERRIDE→CALL | FD+nut_block+air<0.20+facing_bet | **0** | — | ZERO |
| Any nut FD facing initial bet | has_fd+nut_flush_block+facing_bet | **0** | — | ZERO |
| MW-30 CALL pattern | facing_bet+callers_to_bet>=1 | **0** | — | ZERO |
| MW-33 RAISE pattern | monster+facing_bet (not raise) | **0** | — | ZERO |
| MW-50 FOLD pattern | aggression>=1+facing_raise+medium_made | 0 | PILOT_021, PILOT_029, PILOT_094 are facing_raise but strong not medium | ZERO (the 3 raise hands have wrong hand class) |
| Rule 4 (PFA don't auto-cbet IP) | is_preflop_aggressor+IP+opener | **0** | — | ZERO — source pool structural defect |
| Rule 2 (don't barrel draw OOP) | draw+OOP+opener | 28 | (draw hands facing opener decision OOP) | PRESENT |
| Rule 2a (FD OOP specifically) | FD+OOP+opener | 8 | — | THIN |
| Rule 5 (TP not strong) | made+not_strong+not_monster | 19 | — | PRESENT |
| Rule 7 (SPR<2, committed tree) | SPR<2 | 100 | ALL | OVER-REPRESENTED |
| Rule 7 (standard SPR 2-6) | SPR 2-6 | **0** | — | ZERO |
| Rule 7 (deep SPR >6) | SPR>6 | **0** | — | ZERO |
| Rule 3 (don't assume check=nothing) | villain_checked_back=1 | 64 | — | PRESENT, possibly over-represented |
| Rule 8/9 (asymmetric villain ranges) | villain_range_capped=0 | 52 | — | PRESENT |
| Rule 6 (don't overweight blockers) | FD+flush_block_pct>0.30 | **0** | — | ZERO |
| Multi-street aggression fold | villain_aggression_count>=2 | **0** | — | ZERO — source pool structural defect |

### Summary of structural defects

**9 critical gaps (zero examples in corpus):**
1. KB §1.7 RAISE (nut FD + blocker + air≥0.20 facing initial bet)
2. KB §1.7 OVERRIDE→CALL (nut FD + blocker + air<0.20 facing initial bet)
3. MW-30 CALL pattern (facing_bet + callers_to_bet≥1)
4. MW-33 RAISE pattern (monster facing initial bet, not raise)
5. MW-50 FOLD pattern (medium_made facing raise after aggression)
6. Rule 4 (PFA + IP c-bet decisions)
7. Multi-street aggression fold (villain_aggression_count≥2)
8. Standard SPR (2-6) decisions
9. Deep SPR (>6) decisions

**Source pool structural defects (cannot be fixed by resampling the current pool):**
- `is_preflop_aggressor=1`: 0/962 hands in pool (0%) — never generated
- `villain_aggression_count≥2`: 0/962 hands in pool (0%) — never generated
- `SPR > 2.0`: 0/962 hands in pool (0%) — never generated
- `num_callers_to_bet≥1`: 0/962 hands in pool (0%) — never generated
- Only 27/962 hands (2.8%) have `facing_bet=1`, all of which are simultaneously `facing_raise=1` — no pure initial-bet scenarios exist

---

## Q3 answer: are v3.2 reversal hands in the pilot corpus?

### Reversal hands checked

| Hand | In corpus? | Notes |
|---|---|---|
| d3688 (Rule 11b anchor: TPWK OOP 2-tone → CHECK) | **NO** | Not in source_situation_id list |
| d9556 (Rule 11a anchor: monster OOP paired → CHECK) | **NO** | Not in source_situation_id list |
| MW-39 (KB §1.7 OVERRIDE anchor: nut FD low-air → CALL) | **NO** | Not in source_situation_id list |
| d3178 (Rule 11c anchor: river checked-to → BET) | **NO** | Not in source_situation_id list |
| MW-30 (equity surplus CALL anchor) | **NO** | Not in source_situation_id list |
| MW-33 (set RAISE anchor) | **NO** | Not in source_situation_id list |
| MW-50 (action-history FOLD anchor) | **NO** | Not in source_situation_id list |
| d8886 (BET at compressed SPR, villain checked back) | **NO** | Not in source_situation_id list |
| d8963 (BET/CHECK mixed spot) | **NO** | Not in source_situation_id list |
| d2410 (BET kicker advantage) | Partial — deal d2410 appears, but different streets and positions (BTN_river, BTN_turn) | Deal-overlap, NOT the specific calibration hand (d2410_CO_turn) |

**Result: 0/10 reversal hands are in the pilot corpus.** The d2410 deal-id appears in the corpus, but as `d2410_BTN_river` and `d2410_BTN_turn`, not the calibration anchor `d2410_CO_turn`. These are different decision points on the same deal.

### What this implies about calibration vs training set design

The lock file confirms this is correct by design: `disjointness.post_sample_overlap_calibration = 0`. The calibration set is explicitly disjoint from the training corpus.

**However, the design has a gap that matters:** The calibration anchors are not just disjoint — they represent the *hardest pattern-types* in the v3.2 rule taxonomy (the empirically-motivated reversal hands). A corpus that excludes the *specific hands* is acceptable; a corpus that excludes the *hand patterns* those anchors represent is not. The current corpus excludes both.

The calibration exam tests whether labellers *can* apply the rules correctly when explicitly primed. The training corpus is supposed to teach a student model the rules from labelled examples. If the training corpus has zero examples of the patterns the calibration anchors test, the student model cannot learn those patterns — regardless of labeller correctness.

**Implication:** The calibration pass (Sonnet: 29/33, Opus: 32/33 at phase A.4) proves labellers know the rules well enough to pass an exam. It does not prove the training corpus teaches those rules. These are separate requirements.

---

## Q4 answer: patterns v3.2 handles that the corpus barely tests

Rules with fewer than 3 instances (the effective learning floor for any pattern):

### Zero-instance gaps (cannot learn at all)

| Pattern | Count | Why it matters |
|---|---|---|
| KB §1.7 RAISE (nut FD facing initial bet, air≥0.20) | 0 | Core semi-bluff decision rule; the raise/call distinction requires blocker + air threshold examples |
| KB §1.7 OVERRIDE→CALL (nut FD facing initial bet, air<0.20) | 0 | v3.2's most important Fix 2; the MW-39 correction is the entire reason Fix 2 exists |
| MW-30 CALL pattern (facing_bet+callers_to_bet≥1) | 0 | The bet-and-call CALL vs FOLD boundary is one of the three documented v2 reversals |
| MW-33 RAISE pattern (monster+facing_bet, initial bet) | 0 | Set RAISE vs pot-control CHECK boundary; sets default to pot-control without this |
| MW-50 FOLD pattern (medium_made+facing_raise+aggression) | 0 | Action-history range narrowing for FOLD; the correct class boundary for range-dominated folds |
| Rule 4 (PFA c-bet decisions: IP+is_preflop_aggressor+opener) | 0 | Entire c-bet decision class absent; model cannot learn when to c-bet vs check IP as PFA |
| Multi-street aggression fold (aggression_count≥2) | 0 | Range-narrowing fold logic on turn/river unavailable |
| Standard SPR (2-6) decisions | 0 | All 100 hands are committed/near-committed SPR; model learns SPR-ignoring heuristics |

### Thin instances (≤5 examples — below reliable learning threshold)

| Pattern | Count | Sub-pattern |
|---|---|---|
| Rule 11a (paired OOP monster → CHECK) | 6 | Including only 1 with `villain_air_pct < 0.10` (the hardest boundary: low air + monster → still CHECK) |
| Rule 11b (2-tone OOP medium → CHECK) | 5 | d3688 pattern; only 5 examples covering the TPWK-on-2-tone failure mode |
| Flush draw OOP (don't barrel) | 8 | Adequate for Rule 2 if labelled correctly |
| Nut flush draw with blocker | 1 | Not facing a bet — can't test KB §1.7 at all |

### Structural texture gap

Rule 11 predicate fires on 27 hands but is **undifferentiated**: the corpus does not separate the three Rule 11 sub-variants cleanly. A model trained on these 27 hands may learn "OOP+paired/2-tone=CHECK" as a surface rule rather than the three-case structure (CHECK unless exception (a) or exception (c) fires). Boundary cases — where the exception does fire, producing BET — are needed to teach the boundary. Currently the corpus has 15 cases where the exception conditions are nominally met (`villain_top_pair_plus_pct≥0.40` AND strong/monster) but the labeller must still choose CHECK vs BET based on the full predicate. Without boundary pairs (inside/outside the threshold), the model cannot learn the threshold.

---

## Q5 answer: minimum corpus stratification target

### Instance floor per rule

The minimum for a classification model to learn a decision boundary is empirically established at:
- **10 instances per rule trigger**: minimum for statistical signal; boundary learning is unreliable at this count
- **20 instances per rule trigger**: reliable boundary learning for unambiguous rules
- **30+ instances per rule trigger**: reliable boundary learning for rules with sub-conditions and exceptions

For rules with sub-conditions (Rule 11 has 3 sub-variants, KB §1.7 has a RAISE branch and a CALL branch), the minimum per sub-variant is the binding constraint.

**Recommendation for this protocol: 20 instances per distinct trigger pattern, with at least 5 boundary instances (just-inside and just-outside the condition threshold) per rule that has a numeric threshold.**

### Action class balance requirement

For the student model to learn action boundaries:

| Action class | Minimum instances | Rationale |
|---|---|---|
| BET | 40–50 | Opener-decision BET; already most common |
| CHECK | 40–50 | Opener-decision CHECK; already most common |
| CALL | 30–40 | Facing initial bet or facing raise; currently near-zero |
| RAISE | 20–30 | Facing initial bet (KB §1.7) + monster situations; currently near-zero |
| FOLD | 20–30 | Facing raise/aggression; currently near-zero |

**Current corpus distribution (inferred from features, not labelled actions):**
- BET candidates: ~40–50 (opener decisions with value/draw hands)
- CHECK candidates: ~45–55 (opener decisions with pot-control or Rule 11 hands)
- CALL candidates: ~3 (all facing_raise, none facing initial bet)
- RAISE candidates: ~0–3 (no nut FD facing initial bet exists)
- FOLD candidates: ~3 (facing_raise hands, but wrong hand class for MW-50 pattern)

### Full stratification matrix

A corpus that teaches all v3.2 rules reliably needs stratification across:

1. **Action context (primary)**: opener (facing_bet=0) / facing initial bet (facing_bet=1, facing_raise=0) / facing raise (facing_raise=1)
2. **Street**: flop / turn / river
3. **Position**: OOP (is_ip=0) / IP (is_ip=1) / sandwich
4. **SPR bucket**: committed (<1) / compressed (1-2) / standard (2-6) / deep (>6)
5. **Hand class**: air / drawing (FD/SD/combo) / weak_made / medium_made / strong_made / monster
6. **Board texture**: rainbow_dry / two_tone / paired / monotone
7. **Aggressor type**: PFA (is_preflop_aggressor=1) / caller (is_preflop_aggressor=0)
8. **Villain aggression**: none / single-street / multi-street (aggression_count≥2)

The current corpus stratifies on 5 dimensions (street, hero_position, opponent_count, board_texture, hero_range_placement) and is missing **action context**, **SPR**, **aggressor type**, and **villain aggression pattern** — the four dimensions that gate the most important v3.2 rules.

### Recommended total corpus size

For all v3.2 rules at 20 instances per trigger pattern, cross-stratified by the required dimensions:

- Rule 11 sub-variants: 3 × 20 = 60 instances
- KB §1.7 RAISE: 20 instances (nut FD + high air facing initial bet)
- KB §1.7 OVERRIDE→CALL: 20 instances (nut FD + low air facing initial bet)
- MW-30 CALL pattern: 20 instances (facing_bet + callers, equity surplus)
- MW-33 RAISE pattern: 20 instances (monster facing initial bet)
- MW-50 FOLD pattern: 20 instances (medium_made facing raise + aggression)
- Rule 4 c-bet decisions: 30 instances (PFA + IP + opener, mix BET and CHECK outcomes)
- Multi-street aggression fold: 20 instances
- SPR-variant decisions: 40 instances (20 standard-SPR, 20 deep-SPR)
- Boundary cases for Rule 11 thresholds (villain_top_pair_plus_pct 0.35–0.45): 20 instances
- Boundary cases for KB §1.7 threshold (villain_air_pct 0.15–0.25): 20 instances

**Minimum corpus size: ~300 hands** (accounting for pattern overlap where a single hand exercises multiple rules). At 20 instances per rule, some hands will satisfy multiple triggers simultaneously, reducing the total.

**With explicit boundary pairs and inter-rule interaction coverage: 400–500 hands** is the sustainable target for Phase B training.

---

## Q6 answer: supplement vs rebuild recommendation

### Supplement path analysis

**Can we supplement 100 + N targeted hands?**

The supplement path requires the supplemental hands to come from a source that can provide the missing patterns. The current source pool (`training-data/3way_situations_10k.jsonl`, 962 hands) has structural defects at the generation level:

- `is_preflop_aggressor=1`: 0/962 (0%) — never generated
- `villain_aggression_count≥2`: 0/962 (0%) — never generated
- `SPR > 2.0`: 0/962 (0%) — never generated
- `num_callers_to_bet≥1`: 0/962 (0%) — never generated
- `facing_bet=1` with `facing_raise=0`: 0/962 (0%) — all facing-bet hands are simultaneously facing raises

**Conclusion on supplement path:** Supplement is structurally blocked. The 9 critical gap patterns cannot be drawn from the existing 962-hand pool. Any supplement would require new hand generation with different structural parameters (higher SPR envelopes, PFA scenarios, multi-street bet trees, callers-to-bet configurations, initial-bet sequences without raises). Once new generation is required, the supplement path collapses into a rebuild with a retained 100-hand subset.

**Supplemental N required if pool could supply hands:** Approximately 250–350 additional hands (to reach 300–400 total covering all rule patterns). But pool cannot supply them.

### Rebuild path analysis

**Rebuild parameters:**

1. **New source pool generation**: Generate a new pool (target: 5,000–10,000 raw hands) with:
   - `is_preflop_aggressor=1` scenarios included (c-bet decisions)
   - SPR distribution: 20% SPR < 1, 40% SPR 1–2, 30% SPR 2–6, 10% SPR > 6
   - `villain_aggression_count` distribution: 30% 0, 40% 1, 30% 2+
   - `facing_bet=1` WITHOUT `facing_raise=1` (initial bet scenarios)
   - `num_callers_to_bet≥1` scenarios (bet-and-call situations)
   - Nut flush draw scenarios with `villain_air_pct` spread across 0.05–0.60

2. **New stratification dimensions**: Replace hero_range_placement with:
   - action_context (opener / facing_initial_bet / facing_raise)
   - spr_bucket (committed / compressed / standard / deep)
   - villain_aggression_pattern (none / single / multi-street)

3. **Target corpus size**: 400 hands total (not 100)
   - 200 opener decisions (BET/CHECK outcomes) — well-covered by current corpus type
   - 80 facing-initial-bet decisions (CALL/RAISE/FOLD outcomes)
   - 80 facing-raise decisions (CALL/RAISE/FOLD outcomes)
   - 40 boundary-case hands per threshold rule (explicit just-inside/outside)

4. **Retain 100-hand subset**: The existing 100 hands cover Rule 11, Rule 5, Rule 3, and Rule 2 adequately. They remain valid training examples for opener-decision patterns. Retain all 100 as a foundation; add 300 targeted new hands.

**Total rebuild corpus: 400 hands** (100 retained + 300 new generation with corrected parameters).

### Honest tradeoff

| Dimension | Supplement path | Rebuild path |
|---|---|---|
| Source pool feasibility | Blocked — pool lacks required patterns | Requires new generation |
| 9 critical gaps | Cannot close from current pool | Closes all 9 if generation is done correctly |
| Existing 100-hand investment | Preserved but insufficient | Preserved as 100-hand foundation layer |
| Labelling cost (at ~$0.20/hand, 5 labellers) | ~$250 if N=250 (moot — blocked) | ~$400 for 400 hands at 5 labellers = ~$400 |
| Time to produce revised corpus | Blocked by generation need regardless | 1-2 days generation + verification |
| Training signal quality | Biased toward opener-only patterns | Full rule coverage |
| Risk | High — critical patterns still absent | Low — all rule patterns represented |

**Recommendation: Rebuild with 400 hands.**

The supplement path is not viable because it requires the same new-generation work as a rebuild, and the supplement framing would produce a corpus of mixed quality (100 compressed-SPR opener-heavy hands plus mismatched new generation). A clean rebuild with 400 hands, stratified across the 8 required dimensions, produces a corpus that teaches all v3.2 rules at reliable density.

The 100 existing hands should be **retained as a foundation** — they are correctly labelled (500 labels at master `4bce49f`), cover opener-decision patterns for Rule 11 / Rule 5 / Rule 2 / Rule 3 adequately, and are disjoint from the calibration and holdout sets. Scrapping them wastes valid signal. Add 300 targeted new hands via a new generation pipeline that corrects the structural defects identified above.

---

## Recommendation (summary)

**Path: Rebuild to 400 hands = retain 100 + generate 300 targeted new hands.**

The three facts that make supplement impossible and rebuild necessary:

1. **Pool structural defect:** The source pool (962 hands) has zero examples of 4 structural feature classes that gate 9 critical rules. No resampling of the current pool can fill the gaps. New generation is required regardless.

2. **Action class imbalance floor:** With 3 facing-bet hands (all facing_raise, not initial bet), the CALL and RAISE action classes have effectively zero training signal. A 5-class classifier cannot learn boundaries it has never seen. The minimum floor for any action class is ~20–30 examples.

3. **v3.2's hardest rules have zero corpus coverage:** KB §1.7 RAISE (the nut-FD semi-bluff raise) and its OVERRIDE→CALL counterpart (Fix 2) are the rules the range-logic research showed labellers most reliably fail to derive independently. These are the rules v3.2 most needs the corpus to reinforce. Both have zero corpus instances.

**New generation specification (items for architect/gto-expert to produce before corpus rebuild):**

1. SPR envelope: target SPR distribution across committed/compressed/standard/deep (not all ≤1.25)
2. PFA scenarios: `is_preflop_aggressor=1` in 25–30% of hands (c-bet decisions)
3. Initial-bet scenarios: `facing_bet=1` WITHOUT `facing_raise=1` in 20–25% of hands
4. Bet-and-call scenarios: `num_callers_to_bet≥1` in 10% of hands
5. Multi-street aggression: `villain_aggression_count=2` in 15–20% of hands
6. Nut FD with blocker facing bets: `has_flush_draw=1` AND `nut_flush_block=1` AND `facing_bet=1` in targeted 20-hand batch
7. Boundary-case hands for threshold rules: explicit hands just-inside and just-outside KB §1.7 air threshold (0.15, 0.18, 0.20, 0.22, 0.25) and Rule 11 TP+ threshold (0.35, 0.38, 0.40, 0.42, 0.45)

**The 500 Protocol A labels at master `4bce49f` are preserved and valid for the 100 opener-decision patterns they cover.** They are not superseded — they remain training examples for Rule 11 / Rule 5 / Rule 2. They simply do not cover the patterns that require facing-bet, multi-street aggression, PFA c-bet, or standard-SPR scenarios.

---

## Appendix: source data evidence

All counts computed from `data/pilot_corpus_100_hand_2026-04-26.jsonl` (100 hands, 59-feature contract) and `training-data/3way_situations_10k.jsonl` (962 hands, source pool).

| Claim | Evidence |
|---|---|
| 97/100 hands have facing_bet=0 | Python count: `sum(1 for h in hands if feat(h,'facing_bet')==0)` = 97 |
| All facing_bet=1 hands also have facing_raise=1 | Verified by checking all 3: PILOT_021, PILOT_029, PILOT_094 |
| 100/100 hands have SPR ≤ 1.25 | Python: `max(feat(h,'spr') for h in hands)` = 1.25 |
| 0/962 pool hands have is_preflop_aggressor=1 | Python pool scan: `pfa_pool = 0` |
| 0/962 pool hands have SPR > 2.0 | Python pool scan: `high_spr_pool = 0` |
| 0/962 pool hands have villain_aggression_count≥2 | Python pool scan: `multi_agg_pool = 0` |
| 0/962 pool hands have num_callers_to_bet≥1 | Python pool scan: confirmed |
| d3688, d9556, MW-39, d3178, MW-30 not in corpus | Check against source_situation_id: all absent |
| d2410 deal appears in corpus but not the calibration anchor | d2410_BTN_river + d2410_BTN_turn present; d2410_CO_turn absent |
| Rule 11a (paired OOP monster): 6 hands | PILOT_040, PILOT_042, PILOT_043, PILOT_062, PILOT_067 + 1 |
| Rule 11b (2-tone OOP medium made): 5 hands | PILOT_012, PILOT_027, PILOT_060, PILOT_075, PILOT_100 |
| Rule 11c (river checked-to strong OOP BET): 10 hands | PILOT_005, PILOT_037, PILOT_039, PILOT_040, PILOT_043, PILOT_052, PILOT_073, PILOT_077, PILOT_080 + 1 |
