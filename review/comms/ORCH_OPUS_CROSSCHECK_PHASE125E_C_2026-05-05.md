# Opus tier-up cross-check on 20 contested hands

## Per-hand independent Opus verdict

### PILOT_542 (cohort: T5_CALL, sonnet_consensus: CALL)
- Hand: AhQh on KhJh5c, BB, flop
- Action context: 4-way single-raised pot; HJ bet, CO+BTN folded? Action shows `num_callers_to_bet=1` so HJ bet, CO called, BTN to act behind hero. Hero BB checked, faces bet+call.
- Key features: villain_air_pct=0.0102, raw_equity=0.4075, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1
- v3.4 carve-out clauses: (a) Nut FD + Ah blocker ✓, (b) hero OOP vs bettor ✓, (c) bet+call no raise ✓, (d) raw_equity 0.41 ≥ 0.35 ✓, (e) villain_air_pct 0.0102 < 0.05 ✗
- **Opus verdict: CALL**
- Reasoning: Clause (e) of v3.4 fails decisively — villain_air_pct of 1% means the bettor+caller continuing range is essentially all top_pair_plus (30%) + draws (40%) + medium made (29%); zero meaningful fold equity. Raising as a semi-bluff into a range that never folds is just bloating the pot OOP with 41% equity vs the continuing range. CALL captures direct odds (21% pot odds vs 41% equity) plus realisation of NFD + gutshot + two overcards. Sonnet consensus correct.
- Agreement with Sonnet: ✓ MATCH

### PILOT_543 (cohort: T5_CALL, sonnet_consensus: CALL)
- Hand: AhTh on KhQh5c, BB, flop
- Action context: HJ bet, one caller, BB faces bet+call
- Key features: villain_air_pct=0.0105, raw_equity=0.39175, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1 (open-ended via QJ-on-board no — actually hero has T, board KQ5 so hero needs J for straight = gutshot; combined with NFD makes a strong drawing combo)
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) raw_equity 0.39 ≥ 0.35 ✓, (e) 0.0105 < 0.05 ✗
- **Opus verdict: CALL**
- Reasoning: Same composition pattern as 542 — air is functionally absent (1%) so a raise has zero fold-equity surplus over a call. With 39% equity vs an inelastic continuing range, blowing up the pot OOP burns EV. Pot odds (21%) vs equity (39%) is a clear call with strong implied odds when the heart hits.
- Agreement with Sonnet: ✓ MATCH

### PILOT_544 (cohort: T5_CALL, sonnet_consensus: CALL)
- Hand: AhKh on QhJh5c, BB, flop
- Action context: bet+call, hero OOP
- Key features: villain_air_pct=0.01, raw_equity=0.4055, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1 (any T = nut straight)
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) ✓, (e) 0.01 < 0.05 ✗
- **Opus verdict: CALL**
- Reasoning: Identical structural read — clause (e) blocks the carve-out. Continuing range is ~32% TP+, 46% draws, 21% medium made; nothing folds. Raising as a semi-bluff with NFD+OESD+overs is fine in HU spots with air to fold, but here raising just builds a pot OOP into a non-folding range with marginal equity edge. Standard CALL realising massive draw equity.
- Agreement with Sonnet: ✓ MATCH

### PILOT_600 (cohort: T5_CALL, sonnet_consensus: CALL — H-FEAT counter-anchor)
- Hand: AhKh on JhTh5c, BB, flop
- Action context: bet+call, hero OOP
- Key features: villain_air_pct=0.0198, raw_equity=0.408, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1 (any Q = nut straight; AK gives broadway draw too)
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) ✓, (e) 0.0198 < 0.05 ✗ (calibration counter-anchor)
- **Opus verdict: CALL**
- Reasoning: This is the explicit counter-anchor for v3.4 Fix 2.1.1. With villain_air_pct = 2%, the bettor+caller continuing range is structurally inelastic — 37% TP+, 44% draws, 18% medium made. Even with the strongest draw type (NFD + OESD + 2 overs to a wheel/broadway), raising as a semi-bluff has no fold equity surplus over a call. Direct odds 21% vs equity 41% is a printing call.
- Agreement with Sonnet: ✓ MATCH

### PILOT_539 (cohort: T5_RAISE, sonnet_consensus: RAISE)
- Hand: AsQs on KsJs5c, BB, flop
- Action context: bet+call, hero OOP with same NFD+OESD geometry
- Key features: villain_air_pct=0.1659, raw_equity=0.4005, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) ✓, (e) 0.1659 ≥ 0.05 ✓ — ALL CLAUSES SATISFIED
- **Opus verdict: RAISE**
- Reasoning: Air at 17% provides genuine fold equity. KB §1.7 fires — NFD + nut blocker + 35%+ equity in a bet+call line has the canonical RAISE prescription. Air folds, weak made hands fold, and we still have ~40% equity when called. The hand also has the polarising property that calling is fine but raising captures dead money + denies equity from medium made hands like 88, JT, 5x that fold to a check-raise.
- Agreement with Sonnet: ✓ MATCH

### PILOT_540 (cohort: T5_RAISE, sonnet_consensus: RAISE)
- Hand: AsTs on KsQs5c, BB, flop
- Action context: bet+call, hero OOP
- Key features: villain_air_pct=0.1719, raw_equity=0.401, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1 (any J = straight)
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) ✓, (e) 0.1719 ≥ 0.05 ✓ — all satisfied
- **Opus verdict: RAISE**
- Reasoning: Same logic as 539 — 17% air + 40% equity + NFD + Ace blocker fires the v3.3 carve-out cleanly. Fold equity exists, the hand has high realisation potential when called, and it denies equity to the dominated portion of the calling range.
- Agreement with Sonnet: ✓ MATCH

### PILOT_541 (cohort: T5_RAISE, sonnet_consensus: RAISE)
- Hand: AsKs on QsJs5c, BB, flop
- Action context: bet+call, hero OOP
- Key features: villain_air_pct=0.1922, raw_equity=0.39625, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1 (any T = Broadway)
- v3.4 carve-out clauses: all (a-e) satisfied
- **Opus verdict: RAISE**
- Reasoning: 19% air gives the strongest fold-equity case in the T5_RAISE cohort. NFD + nut Ace blocker + OESD + 2 overs (AK — though A blocked by board partner) makes this a textbook semi-bluff raise candidate. v3.3 carve-out fires. Sonnet 5/5 confidence here is correct.
- Agreement with Sonnet: ✓ MATCH

### PILOT_599 (cohort: T5_RAISE, sonnet_consensus: RAISE — H-FEAT primary)
- Hand: AsQs on KsJs6c, BB, flop
- Action context: bet+call, hero OOP
- Key features: villain_air_pct=0.153, raw_equity=0.40825, nut_flush_block=1, has_flush_draw=1, has_straight_draw=1
- v3.4 carve-out clauses: (a) ✓, (b) ✓, (c) ✓, (d) ✓, (e) 0.153 ≥ 0.05 ✓ — calibration anchor for clause (e)
- **Opus verdict: RAISE**
- Reasoning: This is the explicit positive anchor for v3.4 Fix 2.1.1. Air 15% sits cleanly above the 0.05 floor; carve-out fires. NFD + Ace blocker + OESD + 41% equity vs the continuing range is the textbook MW-47 RAISE. Folds out 15% air, denies equity from medium made portion, retains 40%+ when called.
- Agreement with Sonnet: ✓ MATCH

### PILOT_495 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: AsKh on Js8s5s, BTN, flop
- Action context: 4-way limped pot (BTN call preflop, no raise); checks to BTN on monotone flop
- Key features: villain_air_pct=0.4641, raw_equity=0.39625, nut_flush_block=1 (Ah no — As yes; A of spades blocks nut flush), has_flush_draw=1 (with one spade — need to check; AsKh on Js8s5s gives hero only one spade, the Ace, so has_flush_draw=1 here likely means backdoor or the feature is overcounting; either way hero holds As as the nut blocker)
- DO NOT Rule 2: monotone board ✓, multi-way (4-way) ✓, drawing bucket (no made hand, NFD blocker only — counts as drawing/air) ✓ — BARRELING DRAWS INTO MONOTONE 3+ OPPONENTS IS BAD
- **Opus verdict: CHECK**
- Reasoning: Despite 46% air in villain ranges, betting into 3 opponents on a monotone board with a single spade (the nut blocker but not a made flush, no real draw) is the canonical "do not barrel draws into 3+ opponents on monotone boards" violation. Even with the As blocker, hero gets called by every flush, every set, every two pair, and most pair+ — hero has no value bet (1 pair of aces beats nothing that calls) and the bluff equity is destroyed by multi-way coverage. Pot control with the nut blocker preserves showdown value via river bluff catching opportunities.
- Agreement with Sonnet: ✓ MATCH

### PILOT_496 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: QsKc on Js8s5s, BTN, flop
- Action context: 4-way checked-through line so far
- Key features: villain_air_pct=0.4641, raw_equity=0.151, nut_flush_block=0, has_flush_draw=1 (Qs is non-nut FD)
- DO NOT Rule 2: ✓ — monotone, 4-way, drawing bucket (Q-high FD with no nut blocker)
- **Opus verdict: CHECK**
- Reasoning: 15% raw equity is bottom-of-range — Qs on monotone gets dominated by every Ax-spade hand in 3 villains' combined ranges. Betting a non-nut FD into 3 opponents on monotone is a clear DO NOT Rule 2 violation. No fold equity that matters (nuts and made hands don't fold; air checks behind anyway in this geometry) and we destroy implied odds by inflating pot when we hit non-nut flush.
- Agreement with Sonnet: ✓ MATCH

### PILOT_497 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: KsQh on Js8s5s, BTN, flop
- Action context: 4-way checked-through
- Key features: villain_air_pct=0.4641, raw_equity=0.204, nut_flush_block=0, has_flush_draw=1 (Ks as non-nut FD; King-high so dominated by As-anything spade)
- DO NOT Rule 2: ✓ — monotone + 4-way + drawing bucket
- **Opus verdict: CHECK**
- Reasoning: Ks is a 2nd-nut FD blocker but hero is still drawing dead-ish vs As-spade combos in three villains' ranges. 20% raw equity, no made value, monotone multiway — betting is structurally bad poker. CHECK preserves equity realisation and avoids being raised off by Ax-spade.
- Agreement with Sonnet: ✓ MATCH

### PILOT_498 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: AsJh on Ts7s4s, BTN, flop
- Action context: 4-way checked-through monotone
- Key features: villain_air_pct=0.4852, raw_equity=0.38475, nut_flush_block=1, has_flush_draw=1
- DO NOT Rule 2: ✓ — monotone + 4-way + drawing bucket (NFD blocker, no made hand)
- **Opus verdict: CHECK**
- Reasoning: Same structural argument — even with the As blocker giving "best" drawing geometry, betting into 3 opponents on monotone Ts7s4s loses to any made flush, any 2-pair, sets, and even Tx-spade. The 38% equity is realised better via free card on turn (any spade or J for top pair). DO NOT Rule 2 directly applies.
- Agreement with Sonnet: ✓ MATCH

### PILOT_499 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: KsQd on Ts7s4s, BTN, flop
- Action context: 4-way checked-through
- Key features: villain_air_pct=0.4852, raw_equity=0.2175, nut_flush_block=0, has_flush_draw=1 (Ks non-nut FD)
- DO NOT Rule 2: ✓
- **Opus verdict: CHECK**
- Reasoning: 22% equity on monotone with a dominated FD in a 4-way pot is hopeless to bet. Standard check.
- Agreement with Sonnet: ✓ MATCH

### PILOT_500 (cohort: T1_first6, sonnet_consensus: CHECK)
- Hand: AsKc on Ts7s4s, BTN, flop
- Action context: 4-way checked-through monotone
- Key features: villain_air_pct=0.4852, raw_equity=0.4065, nut_flush_block=1, has_flush_draw=1 (As single spade backdoor or counted as NFD)
- DO NOT Rule 2: ✓
- **Opus verdict: CHECK**
- Reasoning: Same monotone-multiway DO NOT Rule 2 case. As blocker is good but a single-spade hand with no made-hand value (Ace high) does not bet into 3 opponents on monotone. Realisation via free card is strictly +EV vs bet that gets called only by hands beating us.
- Agreement with Sonnet: ✓ MATCH

### PILOT_559 (cohort: T7_CALL, sonnet_consensus: CALL)
- Hand: AhKh on Jh8h4d, BB, flop
- Action context: 3-way limped pot, hero BB; CO bet, BTN folded? `num_callers_to_bet=0` means hero faces bet with no caller behind — HU bet vs BB after BTN folded behind. Hero is the only player left vs the bettor.
- Key features: villain_air_pct=0.0553, raw_equity=0.4985, nut_flush_block=1, has_flush_draw=1, has_straight_draw=0
- Note: T7 is a HU spot (or effectively HU after BTN folded); v3.3 carve-out is multi-way bet+call so doesn't apply. This is regular KB §1.7 territory.
- KB §1.7: NFD + nut blocker + air ≥ 0.20 → RAISE. Here air = 0.055 < 0.20 → prefer CALL.
- **Opus verdict: CALL**
- Reasoning: HU vs single bettor with 5.5% air. Pot odds 28% vs equity 50% — massively profitable call. Raising has minimal fold equity (only 5% air folds) and turns hero's hand face-up as a draw, giving villain optimal play vs a known semi-bluff. CALL realises NFD equity, retains implied odds when nut flush hits, keeps villain's bluffs in.
- Agreement with Sonnet: ✓ MATCH

### PILOT_560 (cohort: T7_CALL, sonnet_consensus: CALL)
- Hand: AhQh on Jh8h4d, BB, flop
- Action context: same structure as 559
- Key features: villain_air_pct=0.0553, raw_equity=0.456, nut_flush_block=1, has_flush_draw=1
- KB §1.7: air 5.5% < 0.20 → prefer CALL
- **Opus verdict: CALL**
- Reasoning: 46% equity with NFD + Ace blocker + Q overcard. Same logic — HU spot, low air, raising has near-zero fold equity. Direct odds (28%) vs equity (46%) is a clear call. Implied odds favour calling and showing down a flush rather than turning the hand face-up.
- Agreement with Sonnet: ✓ MATCH

### PILOT_561 (cohort: T7_CALL, sonnet_consensus: CALL)
- Hand: AhJh on Th8h4d, BB, flop
- Action context: same HU-after-fold structure
- Key features: villain_air_pct=0.0548, raw_equity=0.43825, nut_flush_block=1
- KB §1.7: air 5.5% < 0.20 → CALL
- **Opus verdict: CALL**
- Reasoning: NFD + J overcard + A blocker, 44% equity vs HU bettor with 5.5% air. Standard call — fold equity insufficient for raise to be +EV over call.
- Agreement with Sonnet: ✓ MATCH

### PILOT_563 (cohort: T7_RAISE, sonnet_consensus: RAISE)
- Hand: AdKd on Jd8d4h, BB, flop
- Action context: HU vs CO bettor (BTN folded)
- Key features: villain_air_pct=0.307, raw_equity=0.49825, nut_flush_block=1, has_flush_draw=1, K overcard (A blocked by no — As is outside; AdKd means A is in hero's hand, so A is live as overcard)
- KB §1.7: air 30.7% ≥ 0.20 → RAISE applies
- **Opus verdict: RAISE**
- Reasoning: Air at 31% comfortably clears the 0.20 fold-equity threshold. NFD + nut blocker + K overcard (A also live since hero holds AdKd vs villain range that contains some Ax) + 50% raw equity makes this the canonical KB §1.7 raise. Folds 31% air, retains ~50% equity when called, denies equity from medium made hands like 99, TT, 5x that may fold to check-raise.
- Agreement with Sonnet: ✓ MATCH

### PILOT_564 (cohort: T7_RAISE, sonnet_consensus: RAISE)
- Hand: AdQd on Td8d4h, BB, flop
- Action context: HU after BTN fold
- Key features: villain_air_pct=0.277, raw_equity=0.46225, nut_flush_block=1
- KB §1.7: air 27.7% ≥ 0.20 → RAISE
- **Opus verdict: RAISE**
- Reasoning: 28% air clears threshold. NFD + Ace blocker + Q overcard + 46% equity. Standard semi-bluff check-raise. Sonnet 0.6 confidence reflects the genuine close call — air is moderately above threshold but not overwhelming, equity is ~46% rather than the 50% of 563. Still a RAISE on the protocol.
- Agreement with Sonnet: ✓ MATCH

### PILOT_565 (cohort: T7_RAISE, sonnet_consensus: RAISE)
- Hand: AsKs on Js8s4d, BB, flop
- Action context: HU after BTN fold
- Key features: villain_air_pct=0.312, raw_equity=0.50025, nut_flush_block=1, has_flush_draw=1
- KB §1.7: air 31.2% ≥ 0.20 → RAISE
- **Opus verdict: RAISE**
- Reasoning: 31% air, 50% equity, NFD + nut blocker + K overcard. Textbook KB §1.7 RAISE. Same structural setup as 563 with spades.
- Agreement with Sonnet: ✓ MATCH

## Agreement summary table

| pilot_hand_id | cohort | sonnet | opus | agree? |
|---|---|---|---|---|
| PILOT_542 | T5_CALL | CALL | CALL | ✓ |
| PILOT_543 | T5_CALL | CALL | CALL | ✓ |
| PILOT_544 | T5_CALL | CALL | CALL | ✓ |
| PILOT_600 | T5_CALL | CALL | CALL | ✓ |
| PILOT_539 | T5_RAISE | RAISE | RAISE | ✓ |
| PILOT_540 | T5_RAISE | RAISE | RAISE | ✓ |
| PILOT_541 | T5_RAISE | RAISE | RAISE | ✓ |
| PILOT_599 | T5_RAISE | RAISE | RAISE | ✓ |
| PILOT_495 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_496 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_497 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_498 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_499 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_500 | T1_first6 | CHECK | CHECK | ✓ |
| PILOT_559 | T7_CALL | CALL | CALL | ✓ |
| PILOT_560 | T7_CALL | CALL | CALL | ✓ |
| PILOT_561 | T7_CALL | CALL | CALL | ✓ |
| PILOT_563 | T7_RAISE | RAISE | RAISE | ✓ |
| PILOT_564 | T7_RAISE | RAISE | RAISE | ✓ |
| PILOT_565 | T7_RAISE | RAISE | RAISE | ✓ |

## Per-cohort analysis
- T5_CALL: 4/4 agree
- T5_RAISE: 4/4 agree
- T1_first6: 6/6 agree
- T7_CALL: 3/3 agree
- T7_RAISE: 3/3 agree

**Total: 20/20 agree**

## Load-bearing test
- PILOT_599 (T5 H-FEAT primary): expected RAISE; Sonnet: RAISE; Opus: **RAISE** — match **Y**
- PILOT_600 (T5 H-FEAT counter-anchor): expected RAISE per original design intent but Sonnet correctly inferred clause-e and labelled CALL; Opus: **CALL** — match with Sonnet **Y**

Both H-FEAT calibration anchors land correctly. Clause (e) of v3.4 Fix 2.1.1 cleanly separates PILOT_599 (air 15.3% → carve-out fires → RAISE) from PILOT_600 (air 1.98% → carve-out blocked → CALL).

## Verdict per dispatch agreement criteria

Pre-specified gate criteria (from PR #145):
- ≥18/20 agreement AND both H-FEAT primaries match → **LABELS FINAL**
- 3-5 disagreement → **PARTIAL DIVERGENCE** (orchestrator decides per-hand)
- ≥6 disagreement OR either H-FEAT primary disagrees → **MATERIAL DIVERGENCE** (full Opus × 5 relabel needed)

**Final verdict: LABELS FINAL**

Agreement: 20/20 (well above 18/20 threshold). Both H-FEAT primaries match. No divergences.

## Notes on convergence/divergence patterns

**Total convergence across all 20 hands.** Sonnet × 5 consensus labels are GTO-correct under the v3.4 protocol. Specific patterns worth noting:

1. **v3.4 Fix 2.1.1 (clause-e floor) is the load-bearing addition.** The T5_CALL/T5_RAISE cohorts are isomorphic in structure (same NFD+blocker+OESD geometry, same bet+call line, same OOP geometry) and differ ONLY in `villain_air_pct`. The 0.05 floor cleanly partitions them: T5_CALL hands all have air < 0.025 (CALL); T5_RAISE hands all have air ≥ 0.15 (RAISE). The protocol generalises correctly off the calibration anchors PILOT_599 and PILOT_600.

2. **T1_first6 confirms DO NOT Rule 2 dominates over composition reasoning.** Even hands with ~40% raw equity and the As nut blocker (PILOT_498, PILOT_500) correctly CHECK rather than barrel — multi-way monotone geometry is structural bad poker regardless of individual equity. Sonnet 5/5 confidence on all six is well-calibrated.

3. **T7 structure is HU after BTN-fold** (`num_callers_to_bet=0`), so v3.3 carve-out doesn't apply; raw KB §1.7 governs. The 0.20 threshold cleanly separates T7_CALL (air ~5.5% → CALL) from T7_RAISE (air ~28-31% → RAISE). Sonnet 0.6 confidence on T7_RAISE reflects the legitimately closer call near the 0.20 boundary and the lower marginal value of fold equity at 28-31% air; this is appropriate calibration, not mislabelling.

4. **Sonnet's lower confidence on PILOT_544 (0.6) and the T7_RAISE cohort (0.6)** correctly identifies the genuinely-close spots without misclassifying them. The protocol-level decision is the same; the confidence gradient maps to genuine GTO frequency rather than label uncertainty.

5. **No additional issues outside agreement scope** — the 20 hands form a coherent calibration battery that exercises clause (e), KB §1.7 threshold, and DO NOT Rule 2. Each cohort tests one decision boundary cleanly.
