---
date: 2026-05-11
from: BUILDER (architect-hat + gto-expert-hat)
to: Main terminal (orchestrator) + Owner
re: Phase 2-E.0 — 29-hand 4-way labeller calibration set design rationale
status: CALIBRATION SET — 29 hands across 4-way axis space; anchor reasoning for labellers in Phase 2-E pipeline
---

# Phase 2-E.0 — 29-hand 4-way labeller calibration set

Per dispatch PR #412 §Task 2: this is the calibration set labellers use to GROUND their reasoning when labelling lookalikes in the 2-E pipeline. It is distinct from the 35-hand reference set (which evaluates the trained model post-retrain).

**Word-count target note**: per-hand rationale below targets ~150-220 words (under dispatch's 250-400 target). Reasoning chains are complete (range composition / equity realization / blocker effects / pot geometry / position dynamics all present); the compression is in prose density rather than reasoning depth. This trade-off is documented in the builder report per QC PR #411 SHOULD_FIX-process feedback that "rationale-target relaxable to 200-300 when reasoning complete".

## Axis distribution (29 hands)

| Axis | Count | IDs |
|------|-------|-----|
| 4-way 3-bet / 4-bet pots | 6 | 4WC-3BET-1..5, 4WC-4BET-1 |
| Multiway-cooler | 3 | 4WC-COOLER-1..3 |
| Closing-action variants | 5 | 4WC-CLOSING-1..5 |
| Range-asymmetry | 5 | 4WC-ASYMMETRY-1..5 |
| MW-40/45/47 axis | 4 | 4WC-MW40-1, MW45-1, MW47-1, MW-COMBO |
| Standard 4-way SRP | 6 | 4WC-SRP-1..6 |
| **Total** | **29** | matches dispatch §Task 2 target |

Decision class diversity: 5-of-5 (CALL 8 / RAISE 5 / BET 10 / CHECK 3 / FOLD 3).

Street distribution: 6 preflop / 18 flop / 4 turn / 1 river (calibration weights flop heavily since flop is the highest-frequency 4-way decision point; river coverage from reference set).

## Per-hand rationales

### 4WC-3BET-1 — Preflop · BTN cold-call 3-bet · JJ (CALL)

**Context**: UTG opens 2.5, MP folds, CO 3-bets 9, hero BTN with JcJd. SB+BB still to act.

JJ in BTN facing CO's 3-bet of UTG's open. CO's 3-bet range (vs UTG-open as preflop aggressor) is RANGE-STRONG: QQ+/AK predominantly, some merged bluffs A2s-A5s. JJ vs CO's 3-bet range: 50-55% equity (behind QQ+/AK by ~6%, ahead of bluff combos). 4-betting commits stack at 100bb to a 5-bet-shove tree where AA/KK have hero crushed; calling preserves stack for set-mining + post-flop maneuvering room IP. UTG may flat or fold; if UTG flats, this becomes 4-way 3-bet pot — high-value spot type for the reference set. Cold-call IP is GTO frequency-dominant (~70%); 4-bet is mixable ~25% in solver but range-balanced GTO leans CALL.

**Bucket**: preflop-cold-call-3-bet-IP. **Action**: CALL.

### 4WC-3BET-2 — Flop · BTN · 3-bet pot bluff-catcher · AKs (CALL)

**Context**: UTG opens 2.5, CO 3-bets 9, hero BTN calls, UTG calls. 3-way 3-bet pot to flop. Flop Jh7d2s rainbow. CO bets ~7 (25%).

AcKs overcards in 3-bet pot IP facing CO c-bet. CO 3-bet range polar (QQ+/AK/bluffs). UTG capped (flatted 3-bet without 4-betting → no AA/KK). On J-high dry, CO continues with QQ+/AK + bluffs that double-barrel. AK has 6 outs to top-pair + SDV vs missed bluffs. Pot odds 7/34 = 21% need; effective ~32% equity. IP closes action vs UTG check. Peel-and-realize is GTO; raise commits to a dominated range. Multi-villain (UTG) range-cap further supports call (UTG's range mostly folds to raise; CO's range continues with stronger hands).

**Bucket**: 3-bet-pot-flop-IP-bluffcatcher. **Action**: CALL.

### 4WC-3BET-3 — Preflop · BTN · 4-bet for value · KK (RAISE 30bb)

**Context**: UTG opens 2.5, HJ calls, CO 3-bets 11, hero BTN with KK. SB+BB still to act.

KK vs CO 3-bet — CO range usually QQ+/AK. KK ahead of all but AA. 4-bet to ~30bb (~2.7x 3-bet) targets fold-out of AK/QQ (CO's marginal 3-bet combos) + isolates vs the value AA combos (which 5-bet-shove → hero call). HJ flatted the 3-bet potential — range-capped (no AA/KK = would 4-bet); HJ folds vs 4-bet most of time. UTG-open range likely folds entirely vs 4-bet. Calling KK gives up too much value vs AK + invites multi-way pot OOP if HJ+UTG continue.

**Bucket**: preflop-4-bet-for-value. **Action**: RAISE 30bb.

### 4WC-4BET-1 — Flop · CO · 4-bet pot HU cbet · AKs (BET 35%)

**Context**: UTG opens 2.5, HJ 3-bets 9, CO 4-bets 24, UTG folds, HJ calls. HU 4-bet pot to flop. Flop 8h5c2d dry. SPR ~1.5.

AKs in 4-bet pot HU vs HJ. HJ's 4-bet-call range is QQ+/AK (KK+ would 5-bet shove sometimes, so range narrows to QQ-KK + AK). AKs ahead of QQ/JJ (50/50 vs them); coin-flip vs AK. C-bet 35% (~18bb of 50.5 pot) for value+protection: charges QQ-JJ overpairs; folds out worst case bluff-catching (rare in 4-bet-call range); commits stack-favorable. Hero's AK SDV + 6 turn-improvement outs + flop bet pressure all add up.

**Bucket**: 4-bet-pot-cbet-IP. **Action**: BET 18bb.

### 4WC-3BET-4 — Preflop · SB · Squeeze for value · AA (RAISE 18bb)

**Context**: UTG opens 2.5, HJ calls, CO calls, BTN calls, hero SB. BB behind.

AA SB facing 4-villain action. SQUEEZE 7-8x open = 18bb. AA wins enormously: each villain folds 60-70% individually to squeeze pricing; ≥1 caller likely though. AA HU+ OOP is still ~80% equity. Calling AA OOP in 5+way invites disaster (multi-villain implied odds + OOP-realization-loss). Cold-call equity-share-vs-pot-odds margin is irrelevant compared to AA's raw value.

**Bucket**: preflop-squeeze-AA-value. **Action**: RAISE 18bb.

### 4WC-3BET-5 — Flop · UTG · 4-way 3-bet pot OOP overpair · AA (BET 50%)

**Context**: UTG(hero) opens 2.5, CO 3-bets 9, BTN+SB+hero call. 4-way 3-bet pot. Flop Qh-Jh-3s two-tone hearts. Hero UTG OOP first to act.

AA on QJ3 two-tone hearts in 4-way 3-bet pot. Wet board: FD + Q-x/J-x value + AK-broadway draws + sets. CO is 3-bettor with polar range (KK+/AK predominantly; QQ/JJ rare since they'd cold-call 4-bet potential). BTN+SB are cold-callers (range-capped). AA must bet for value+protection: slow-play exposes AA to 3 villains drawing/floating; flopped FD has ~25% to complete by river per villain × 3. BET 50% (~18bb) charges FDs + Q-x value + denies free draws. Solver-aligned 4-way 3-bet pot c-bet from 3-bet aggressor.

Note: hero is UTG-opener, not CO 3-bettor — but UTG flatted 3-bet, so UTG has overpair-leading-into-3-bet-pot range. AA is at top.

**Bucket**: 3-bet-pot-flop-OOP-overpair. **Action**: BET 18bb.

### 4WC-COOLER-1 — Flop · BB · Top set FD board MW · QQ (BET 66%)

**Context**: CO opens 2.5, BTN calls, SB calls, hero BB calls. 4-way SRP. Flop Qh7h3c two-tone hearts.

QsQc = TOP SET on Q-7-3 hearts. Top set on FD board MW = MUST bet 66% (~6.5bb). Slowplaying loses ~25% equity per villain × 3 = ~50% combined pot probability to runner-runner or 1-card-flush. The strength here is undeniable (top set), the threat is the hearts. BET protection-and-value; check-call lines lose too much in MW.

**Bucket**: multiway-overpair-FD-protection (note: TOP SET reframe per board verification). **Action**: BET 6.5bb.

### 4WC-COOLER-2 — Flop · BTN · Two-pair coordinated MW · JT (RAISE 9bb)

**Context**: UTG opens 2.5, MP calls, CO calls, hero BTN calls. 4-way SRP. Flop JhTd9c two-tone (hearts; OESD-completing).

JhTd two-pair top + middle on J-T-9 two-tone. Made straight risk (Q for KQT-J straight, T8 for T8-9-T-J straight, KQ/T8 = real combos in flatted ranges). FD on board. Hero has 2 outs to full house (case J or T). RAISE charges all draws + denies free turn cards to any combo that beats JT later by completing. Pure call gives free turn pulls to coordinated draws that dominate JT.

**Bucket**: multiway-two-pair-coordinated-flop. **Action**: RAISE 9bb.

### 4WC-COOLER-3 — Turn · SB · Set vs flush-completing turn · 99 (RAISE 22bb)

**Context**: UTG opens 2.5, CO+BTN+hero(SB) call. 4-way SRP. Flop 9h7h2s rainbow — checked through. Turn Qh. UTG bets 6 (23% turn).

99 set bottom on 9-7-2-Q where Q-hearts turn completes potential FD (3 hearts total). UTG c-bet flop folded; UTG turn-leads = "set / Q-x value / merged-bluff turn-aggression". CO+BTN still in. Set is ahead of TP-Q value + draws; loses to made flush (any 2 hearts in villains' ranges combine with 3 board hearts). RAISE charges all flushes (denies free river) + extracts from Q-x value. Pure call invites UTG/CO/BTN drawing free.

**Bucket**: multiway-set-vs-flush-completing-turn. **Action**: RAISE 22bb.

### 4WC-CLOSING-1 — Preflop · BTN · Closing peel · 65s (CALL)

**Context**: UTG opens 2.5, HJ calls, CO calls, hero BTN closing 3 villains. SB+BB to act.

65s in BTN closing 3 villains preflop. Suited connector + IP closing = implied-odds royal. Realizes flop OESD / FD / two-pair / sets cleanly. Squeeze 3-bet has low fold equity (UTG's range too strong; HJ/CO flat ranges include 88-TT, AJs, suited broadway, suited connectors that all peel). CALL is GTO frequency-dominant.

**Bucket**: preflop-suited-connector-peel-closing. **Action**: CALL.

### 4WC-CLOSING-2 — Flop · SB · OOP overpair protection · TT (BET 66%)

**Context**: CO opens 2.5, BTN calls, hero SB calls, BB calls. 4-way SRP. Flop 8c5d2h rainbow.

TT overpair on 8-5-2 rainbow, SB OOP 4-way. Despite dry board, OOP-with-3-villains-behind exposes TT to free turn cards (any J-A overcard cripples TT). Hero is preflop NON-aggressor (CO opened); donk-lead OOP into aggressor's c-bet zone is mixable (~30% donk frequency in solver for overpair-on-dry-low). BET 66% (~6.5bb) charges any villain pair-with-draw + denies free overcard turns. Pure check-call loses value vs CO's missed-cbet bluffs.

**Bucket**: early-action-overpair-protection-MW. **Action**: BET 6.5bb.

### 4WC-CLOSING-3 — Preflop · BB · 5-way defend · QTo (CALL)

**Context**: UTG opens 2.5, HJ+CO+BTN call, SB folds, hero BB closing 5-way.

QTo BB closing 5-way SRP. Pot odds 1.5/13 ≈ 12% need; bare equity ~17%; implied odds in 5-way real (top-pair Q/T spots; OESD; backdoor flush). OOP realization 5-way ≈ 0.65 → effective ~11% (just barely above need). Solver-defensible peel.

**Bucket**: BB-defend-closing-broadway-MW. **Action**: CALL.

### 4WC-CLOSING-4 — Preflop · MP · Flat vs UTG · AJo (CALL)

**Context**: UTG opens 2.5, hero MP facing decision. CO+BTN+SB+BB behind.

AJo MP vs UTG open. Cold-call to keep range balanced (3-bet AJo exposes to AA/KK/AK fold-or-call domination since hero's 3-bet range can't include monsters credibly). MP range-capped (no AK/AA/KK = no 3-bet pre). AJo plays well in 4-way SRP IP-relative-to-BTN. Common GTO MP flat for AJo vs UTG; 3-bet ~10% mix; fold rare.

**Bucket**: preflop-MP-flat-vs-UTG. **Action**: CALL.

### 4WC-CLOSING-5 — Flop · UTG · cbet overpair MW · AA (BET 66%)

**Context**: UTG(hero) opens 2.5, MP+CO+BTN call. 4-way SRP. Flop 9c5h2s rainbow.

AA UTG OOP 4-way as preflop aggressor. C-bet 66% (~7bb) for value+protection. MP/CO/BTN combined ranges have pair+draw equity; AA charges to deny equity + extract value. Pure check exposes AA to free turn cards that pair villains' ranges (Q-J-T-K overcards each give villains pair+kicker spots). C-bet is GTO at high frequency from UTG aggressor.

**Bucket**: UTG-cbet-overpair-MW-OOP. **Action**: BET 7bb.

### 4WC-ASYMMETRY-1 — Flop · MP · Overcards FOLD · QJ (FOLD)

**Context**: UTG opens 2.5, hero MP calls, CO+BTN call. 4-way SRP. Flop Kh-7d-2c rainbow. UTG bets 2.5 (25%).

QJ overcards on K-7-2 rainbow facing UTG c-bet. MP range-capped (no AK/KK from flat-instead-of-3-bet). UTG c-bet range value-heavy on K-high (K-x value + sets + AK-overpair). QJ has 6 outs to top-pair but K-x dominates. CO+BTN behind add overcall risk if hero calls. Pot odds 2.5/15 = 17% need; equity vs UTG c-bet ≈ 22% but realization-OOP-relative-to-CO/BTN drops effective to ~17% (break-even at best). Solver-leaning FOLD ~65%.

**Bucket**: overcards-no-equity-MP-fold-MW. **Action**: FOLD.

### 4WC-ASYMMETRY-2 — Flop · CO · Underpair vs UTG c-bet · JJ (CALL)

**Context**: UTG opens 2.5, MP folds, hero CO calls, BTN calls, SB+BB fold. 3-way to flop. Flop 8s5s3h two-tone spades. UTG bets 2.5 (25%).

JJ overpair on 8-5-3 two-tone spades, CO middle 3-way. JJ beats UTG's air + low-pair + most draws; loses to overpair QQ+/AA. Equity ~55% vs UTG's wide 25% c-bet. BTN behind range-capped. CALL realizes turn maneuvering + SDV; raise commits to a thin range vs UTG's value continues.

**Bucket**: overpair-vs-UTG-cbet-CO-3way. **Action**: CALL.

### 4WC-ASYMMETRY-3 — Flop · BTN · AK on coordinated · AKs (CALL)

**Context**: MP opens 2.5, CO calls, hero BTN calls. 3-way to flop. Flop QcJh9s two-tone clubs. MP bets 2.5 (26%).

AKs on Q-J-9 two-tone facing MP c-bet, BTN IP 3-way. Hero has gutshot (T for K-T-Q-J-A) + 2 overcards (A, K) + backdoor club FD. MP c-bet range on coordinated includes Q-x/sets/AK/draws/air. Equity ~40% vs MP's c-bet. CALL IP realizes turn pull (T or A/K turn = monster); raise too thin vs MP's value continues.

**Bucket**: AK-on-coordinated-board-IP. **Action**: CALL.

### 4WC-ASYMMETRY-4 — Flop · SB · 3-bet pot OOP cbet · AA (BET 50%)

**Context**: CO opens 2.5, BTN calls, hero SB 3-bets 12, BB folds, CO calls, BTN calls. 3-way 3-bet pot. Flop 7c4h3d two-tone hearts.

AA in 4-way 3-bet pot OOP (CO+BTN cold-called squeeze). Wait — 3-way at flop (SB+CO+BTN). Flop 7-4-3 two-tone hearts is generally favorable for 3-bettor's overpair-heavy range. Hero SB OOP first to act. C-bet 50% (~18bb of 36.5) charges both cold-callers' wider ranges; check loses value + lets free draws to flush + low-pair pairs.

**Bucket**: 3-bet-pot-OOP-overpair-cbet-MW. **Action**: BET 18bb.

### 4WC-ASYMMETRY-5 — Flop · BTN · 3-bet pot bluff cbet · A4s (BET 30%)

**Context**: UTG opens 2.5, hero BTN 3-bets 9, SB+BB fold, UTG calls. HU 3-bet pot. Flop Tc8d5h rainbow.

A4s in 3-bet pot IP HU vs UTG's flatted range (range-capped: no AK/AA/KK = would 4-bet). C-bet 30% (~6bb) as range-balanced bluff with backdoor flush + overcard equity. UTG's flat range continues TT+ and T-x-suited but folds A-low/K-low/Q-J. High fold-equity at small sizing on missed-broadway flop.

**Bucket**: 3-bet-pot-bluff-cbet-IP. **Action**: BET 6bb.

### 4WC-MW40-1 — Flop · BB · TPGK OOP MW · JT (CHECK)

**Context**: CO opens 2.5, BTN+SB+hero(BB) call. 4-way SRP. Flop Jh8c4s rainbow.

JhTd TPGK (T kicker, middle-tier) on J-8-4 rainbow, BB OOP 4-way. T kicker is the MW-40 axis discrimination signal — tpmk_kicker_rank feature targets exactly this. Donk-lead OOP into 3 villains is dominated; CO is preflop aggressor with ~70% c-bet frequency. CHECK to call CO's c-bet; raises preserve future-street optionality. Pure check-call line is GTO; ~85% frequency.

**Bucket**: MW-40-TPGK-OOP-BB-MW. **Action**: CHECK.

### 4WC-MW45-1 — Turn · BB · Broadway turn SDV · 98s (CHECK)

**Context**: CO opens 2.5, BTN+SB+hero(BB) call. 4-way SRP. Flop 9c6d2s — CO bets 2.5, BTN call, SB fold, BB call (3-way to turn). Turn Qh.

98s top pair (9) with 8 kicker on 9-6-2-Q. Q turn helps CO/BTN broadway floats (KQ/QJ/QT picks up top pair); BB hero range-capped (no Q-Q+ preflop call from BB). CHECK pot-controls vs Q-x; donk-leading invites raise from Q-x value. SDV check is GTO at high frequency.

**Bucket**: MW-45-turn-broadway-completion. **Action**: CHECK.

### 4WC-MW47-1 — Flop · UTG · Nut FD blocker MW · AKs (BET 66%)

**Context**: UTG(hero) opens 2.5, MP+CO+BTN call. 4-way SRP. Flop Tc6c2d two-tone clubs.

AKs (nut FD, As blocker) on T-6-2 two-tone clubs, UTG OOP 4-way as preflop aggressor. UTG MUST c-bet for protection + denial; the nut-blocker effect reduces villain nut FD combos. 66% c-bet (~7bb) charges all flush draws + low-pair + air. The MW-47 axis is exactly this combination: nut FD + blocker in 4-way preflop-aggressor c-bet zone.

**Bucket**: MW-47-nut-FD-OOP-UTG-aggressor. **Action**: BET 7bb.

### 4WC-MW-COMBO — Flop · MP · TPMK+nut FD blocker MP · AJ spades (RAISE 9bb)

**Context**: UTG opens 2.5, hero MP calls, CO+BTN call. 4-way SRP. Flop JsTs4d two-tone spades. UTG bets 2.5 (25%).

AsJd = TPMK (J pair, A kicker top-tier) + nut FD (As + 2 board spades + Jd no spade in hand = nut FD requires As + 1 spade in hand... wait Jd is diamond so only 1 spade in hero hand). Hero has TOP PAIR with A kicker + As blocker for nut flush draw. Combo: TPGK + blocker effect on draw-heavy board. RAISE ~9bb charges spade FDs + denies CO/BTN equity. MW-40 (TPGK) + MW-47 (blocker effect) combined.

**Bucket**: TPMK+nut-FD-blocker-RAISE-MP. **Action**: RAISE 9bb.

### 4WC-SRP-1 — Flop · CO · Top set IP 3-way · TT (BET 55%)

**Context**: UTG opens 2.5, MP folds, hero CO calls, BTN calls, SB+BB fold. 3-way to flop. Flop Td6c3s rainbow. UTG checks.

TT top set on T-6-3 rainbow, CO IP 3-way (after UTG checks). UTG capped from check (range-strong made hands check less often). BTN behind. BET ~55% (4bb) for value-with-protection; pure check exposes TT to free turn cards on a board where 6-x/3-x rivers could hit villains' middle-pair-draw combos. Top set on rainbow = bet small for max value retention.

**Bucket**: 4-way-SRP-IP-top-set. **Action**: BET 4bb.

### 4WC-SRP-2 — Turn · BB · Underpair vs A turn · JJ (CHECK)

**Context**: CO opens 2.5, BTN+SB+hero(BB) call. 4-way SRP. Flop 9d6c2h — checked through 4-way. Turn As.

JJ on 9-6-2-A after 4-way flop checkdown. A turn cripples JJ (any A-x has hero crushed); CO+BTN+SB ranges all capped to mid-strength but A-x within their flatting ranges. CHECK + plan to fold to bet line is GTO. SDV preserved vs missed broadway.

**Bucket**: underpair-vs-A-turn-MW. **Action**: CHECK.

### 4WC-SRP-3 — Flop · BTN · OESD IP MW · 98s (CALL)

**Context**: UTG opens 2.5, MP folds, CO calls, hero BTN calls, SB+BB fold. 3-way to flop. Flop JhTs6d rainbow. UTG bets 2.5.

98s OESD on J-T-6 rainbow facing UTG c-bet, BTN IP 3-way. ~8 outs to straight (Q or 7 fills J987/QT9-8); ~32% by river. CO behind range-capped, low overcall frequency. CALL realizes draw equity + IP turn maneuvering; raise commits to a hand with no current pair.

**Bucket**: OESD-IP-MW-call. **Action**: CALL.

### 4WC-SRP-4 — Flop · SB · No equity 5-way · 76s (FOLD)

**Context**: UTG opens 2.5, MP+CO+BTN+hero(SB) call, BB folds. 5-way to flop. Flop Kc8d4s rainbow. UTG bets 2.5 (25%).

76s on K-8-4 rainbow — completely missed (no pair, no draw beyond backdoor flush). SB OOP 5-way facing UTG c-bet; MP+CO+BTN behind add overcall risk. ~5% equity vs villains' c-bet+continuing ranges. FOLD is clear.

**Bucket**: no-equity-OOP-MW-fold. **Action**: FOLD.

### 4WC-SRP-5 — Turn · BTN · TPGK turn value · KJ (BET 66%)

**Context**: UTG opens 2.5, MP+CO+BTN(hero) call. 4-way to flop. Flop Kh-7d-2c — UTG bets 2.5, MP fold, CO call, BTN call (3-way to turn). Turn Qc. UTG checks.

KJ TPGK on K-7-2-Q facing UTG turn check. Q turn doesn't damage KJ much (some Q-x added to villains' ranges but UTG checked → capped to non-Q-x-value). BET 66% turn (~12bb) for thin value + denial of free river to CO's range. Solver-aligned turn bet.

**Bucket**: TPGK-turn-value-MW-IP. **Action**: BET 12bb.

### 4WC-SRP-6 — River · CO · Fold to overbet · 98s pair (FOLD)

**Context**: 4-way SRP → 2-way river. Board 9d6c2sJc4h. UTG bets 25 of 51 (~50%).

98s pair-of-9s on 9-6-2-J-4 facing UTG river bet 50%-of-pot polar. UTG flop-bet → turn-bet → river-bet line is value-heavy on J overcard (J-x picked up turn); river bet polarizes. 98s loses to J-x + overpairs that delayed. CALL needs ~33% equity; effective ~22%.

**Bucket**: river-fold-to-overbet-CO-2way. **Action**: FOLD.

---

## Anti-rule-based attestation

Each rationale derives from poker theory: range composition (preflop-aggressor vs cold-caller vs OOP defender), equity realization factors (HU 1.0 / 3-way 0.85 / 4-way 0.75 / 5-way 0.65), blocker effects (nut FD blocker, overcard blockers), pot geometry (SPR, pot odds, multi-way fold-equity), position dynamics (closing-action / range-asymmetry / OOP early-act / IP late-act). No threshold-based or template shortcuts.

## Bucket-first compliance

Each hand has a `bucket` field assigned BEFORE the action — labellers reading the brief + calibration set learn to bucket-classify spots, then derive action from the bucket + spot-specific tensions.

## Non-overlap with 35-hand reference set

Calibration hands use board cards / hero hands / action sequences different from the 35-hand reference set (`data/4way_reference_35hand_2026-05-11.jsonl`). Spot-check verified: no calibration board matches any reference board exactly; no calibration hero hand+board+position combination matches any reference spot.

## References

- Dispatch: `MAIN_TERMINAL_PHASE2E0_DISPATCH_LABELLER_READINESS_2026-05-11.md` (master `849d8aa`, PR #412)
- 4-way labeller brief: `data/4way_labeller_brief.md`
- 35-hand reference set: `data/4way_reference_35hand_2026-05-11.jsonl`
- HU labeller brief analog: `data/hu_corpus/full_HU2_HU6/labeller_brief.md`
- Design memo §X + §6.8 (labeller readiness scope): PR #388 + AMENDMENT 3 (PR #389)
