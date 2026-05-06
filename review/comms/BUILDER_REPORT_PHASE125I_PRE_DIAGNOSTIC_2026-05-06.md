---
date: 2026-05-06
from: LEAD-PROGRAMMER (analyst hat — diagnostic)
to: Main terminal (orchestrator) · QC stream
re: Phase 12.5I-pre — per-hand diagnostic on 5 stay-wrong hands (MW-17/25/40/45/47); E-FEATURE / E-DIST / isomorph-mismatch classification; 12.5I + 12.5J spec hints
status: REPORT — PR open, ready for QC trigger
branch: programmer/phase125i-pre-diagnostic-2026-05-06
base: master `d366aee`
---

# 12.5I-pre diagnostic — per-hand classification on 5 stay-wrong hands

## TL;DR

Per-hand verdicts on the 5 stay-wrong hands across 12.5E/G/H iterations:

| Hand | Primary | Secondary | Margin (model→corrected expert) | 12.5I vs 12.5J |
|---|---|---|---:|---|
| **MW-17** | E-FEATURE | (none) | +0.843 (FOLD vs CALL; model 0.046 on CALL) | **12.5J** (engineer features for implied-odds + nut-blocker-with-overcards reasoning) |
| **MW-25** | E-DIST underpowered | E-FEATURE secondary | +0.880 (CHECK vs BET; ablating better_hand_pct shifts +0.147 toward BET) | **12.5I** (T8' redesign: BET-after-checked-through-multiway hands with hero-doesnt-have-As-public) |
| **MW-40** | E-DIST underpowered | (none) | +0.267 (CHECK vs BET; **closest to flipping**, BET prob 0.305) | **12.5I** (T9' expansion: 30-40 hands; this is the most tractable) |
| **MW-45** | isomorph-mismatch | E-DIST secondary | +0.746 (CALL vs RAISE; T10' template's parametric texture didn't match MW-45's broadway-completed-turn) | **12.5I'** (T10' redesign: AKQx-broadway-completed-turn variants specifically) |
| **MW-47** | E-FEATURE primary | mixed (with raw-vs-corrected expert disagreement) | +0.910 (CALL vs RAISE-corrected; **model agrees with RAW expert CALL**) | **12.5J** (engineer features for SUITED-NFD-with-blocker-bet+call-multiway clause-e equivalent) |

**Recommended split:** 12.5I addresses MW-25/40/45 (3 of 5; isomorph-mismatch + underpowered family). 12.5J addresses MW-17/47 (2 of 5; E-FEATURE primary). **Both are non-overlapping** — owner can dispatch in parallel without coordination overhead.

**Substantive surprise (worth surfacing to orchestrator):** for MW-45 and MW-47, the v3.4 protocol applied to the corresponding 12.5H manual canonical produced labels that DISAGREE with the BATCH2 reference set's expert action:
- PILOT_692 (T10' MW-45 canonical, 6d6c on AcKd6hQs): full-phase consensus 5/5 RAISE; reference says RAISE — but original 1-labeller pilot was CALL (matches model). The protocol-vs-reference tension manifests as labeller variance.
- PILOT_694 (T-RAISE MW-47 canonical, AsQs on KsJd5s): full-phase consensus 5/5 RAISE; reference says CALL (raw); solver-corrected says RAISE. v3.4 Fix 2.1.1 specifically engineers labellers to RAISE this hand.

The corpus-vs-reference alignment on MW-45/47 is correct (corpus teaches solver-corrected RAISE). The problem is the model doesn't transfer corpus learnings to the reference hand at gate time.

## Per-hand diagnosis (Steps 1-5 protocol)

### MW-17: AdKs on Jd8d4c (BB facing CO bet 3-way → effectively HU after BTN folds; expert CALL)

**Step 1 — Reference spec:** `AdKs nut flush draw + overcards`. Expert: **CALL HIGH** with reasoning: "nut flush draw (9 outs) plus two overcards (6 outs to TPTK/TPGK) — approximately 15 outs giving roughly 54% equity. Pot odds require only 27% to call. Nut draw especially valuable MW because no opponent can beat it with a flush. Calling comfortably; raising as a semi-bluff also viable."

NOTE: the reference's "9 outs nut flush draw" reasoning is actually INCORRECT for the literal AdKs hand — Ad with only Jd+8d on board = 3 diamonds = 0 flush-draw outs (need 4 of suit visible). The reference treats it as nut-FD anyway because the GTO axis was named "Nut Potential". This is a known reference-set disconnect; v3.4 protocol bucket-first reasoning correctly identifies AdKs as drawing-bucket-with-air (no actual FD outs).

**Step 2 — 12.5H corpus alignment:** Originally targeted by T7-ext (UNSUITED, MW-17 literal). Path-(c) amendment redesigned T7-ext to SUITED-NFD-with-blocker (intentionally NOT the literal MW-17 hand). The 12 SUITED T7-ext hands consensus split: 4 CALL (low-villain-air) + 8 RAISE (high-villain-air). MW-17 is UNSUITED so cannot match the SUITED template's discriminative axis — corpus does NOT teach the literal MW-17 pattern.

**Step 3 — Model inference walk-through (v9-3way-v2.2):**
- Model predicts: **FOLD** (probability 0.889; CALL only 0.046)
- Margin to expert (CALL): **+0.843** (very far)
- Top-10 contributions:
  - `to_call=33` × imp 0.091 = +2.99
  - `pot_size=90` × imp 0.022 = +1.95
  - `facing_bet=1` × imp 0.118 = +0.118
  - `raw_equity=0.234` (model sees this as low equity)
  - `better_hand_pct=0.597` (model sees hero behind 60%)
- v9-3way-v2.2 has NO `nut_flush_block` in top-15 — the nut-blocker feature is NOT load-bearing in this model. (`nut_flush_block` is load-bearing in v9-student per cross-seed median 0.0496, but v9-student is NOT promoted.)

**Step 4 — Counterfactual:**
- Ablate `to_call` (33→0): no flip
- Ablate `pot_size` (90→0): no flip
- Ablate `facing_bet` (1→0): flips to CHECK (only because facing_bet drives the FOLD vs CHECK gate)
- Perturb `to_call` ±20% (26.4 to 39.6): no flip

NO perturbation flips toward CALL.

**Step 5 — Verdict: E-FEATURE PRIMARY**

The model has 0.889 confidence in FOLD against an expert CALL. Pure equity-vs-pot-odds reasoning (raw_equity 0.234 < pot_odds 0.367 implied by to_call/pot_size) → FOLD. To shift to CALL the model needs encoded features for:
- Implied-odds-from-improvement (overcards + backdoor diamonds → ≥15 future-card outs)
- Nut-blocker (Ad blocks villain's strongest continuing range)
- 3-way-now-HU position (BTN's preflop-call narrows CO's CB range)

These are NOT in the 59-feature surface (and only weakly in the 45-feature v9-3way-v2.2 surface).

**12.5J spec hint:**
- `implied_outs_via_overcard` (count of overcard outs that improve to TPTK/TPGK)
- `backdoor_flush_outs` (count of one-card runner-runner FD outs)
- `nut_blocker_value` (value of removing villain's nuttiest continuing range; Ad on diamond board = 1.0)
- Estimated rough scope: 3 new features + cascade through `feedback_attention_flags_when_features_change.md` (raw + attention vocab + prompt + capture + trainer) ≈ 1-2 weeks of feature-engineering work for these hands

### MW-25: Ks7s on As9s5d (BTN IP 4-way checked through; expert BET)

**Step 1 — Reference spec:** `Ks7s flush draw IP BTN, 4-way checked to hero`. Expert: **BET HIGH** with reasoning: "strong flush draw with three opponents who all checked. IP with a flush draw, hero can bet after seeing three checks — all opponents showed weakness. Betting serves double duty: deny free cards and potentially take the pot now. IP position allows hero to see all checks before committing chips — position amplified in 4-way pot."

**Step 2 — 12.5H corpus alignment:** Targeted by T8' template (monotone-flop FD checked-through 4-way; 18 hands = 16 parametric + 2 manual). Consensus: 18/18 CHECK (100% unanimous; avg_conf 0.85).

**Important:** the v3.4 protocol applied to T8' hands (including PILOT_689 = Ks7h on As9s5s monotone analog) produces CHECK uniformly. The labellers correctly invoke DO NOT Rule 2 ("don't barrel draws into 2+ opponents 3-way") + KB §1.7 facing-bet requirement. **The corpus does NOT teach the BET reasoning the BATCH2 reference set's MW-25 expert calls for.** This is a corpus-vs-reference protocol disconnect for this template family.

**Step 3 — Model inference walk-through (v9-3way-v2.2):**
- Model predicts: **CHECK** (probability 0.920; BET 0.040)
- Margin to expert (BET): **+0.880**
- Top contributions:
  - `pot_size=110` × imp 0.022 = +2.39
  - `better_hand_pct=0.803` (model sees hero behind 80% of villain range)
  - `equity_margin=0.351` (positive but moderate)
  - `raw_equity=0.351` (drawing range)

**Step 4 — Counterfactual:**
- Ablate `better_hand_pct` (0.803→0): no flip BUT expert (BET) prob increases by **+0.147** (CHECK 0.920→0.745, BET 0.040→0.187)
- Ablate `pot_size`: no flip; trivial Δ
- Ablate `equity_margin`: no flip; -0.011 expert Δ
- Perturb `pot_size` ±20%: no flip

The `better_hand_pct` ablation is informative — the feature CORRECTLY captures "hero is dominated" but suppresses the BET-after-checked-through reasoning. With LESS weight on better_hand_pct (or with a counter-balancing feature), model could flip toward BET.

**Step 5 — Verdict: E-DIST UNDERPOWERED (primary) + E-FEATURE (secondary)**

The model has the right features but their relative weighting needs to learn that "after 4-way check-through with high villain_air, BET is correct DESPITE being behind range" — that's a corpus-driven learning problem, not a feature-surface gap. T8' at 18 hands didn't move the needle (corpus produced CHECK labels matching model, not BET). Need:
- More T8' BET-targeted hands AND/OR
- Re-design T8' to specifically target the "BET after check-through" pattern (not the "CHECK-because-monotone-board-is-flush-heavy" pattern that current T8' produces)
- Or new feature `villain_checked_back_from_aggressor` (which v9-3way-v2.2 has at importance 0.020 in top-15 but not load-bearing) weighted explicitly via training-data design

**12.5I spec hint:**
- T8' redesign: hero on TWO-TONE (not monotone) board; hero has FD without As-public (e.g., 9s8s on Kh4s2s is a non-nut FD on 2-tone board); 4-way checked-through; LABEL must produce BET
- ~30 hands in this redesigned template; would need orchestrator to re-design v3.4 protocol section so labellers route to BET (current v3.4 routes such hands to CHECK via DO NOT Rule 2)
- **Note:** the v3.4 protocol itself is the corpus-vs-reference disagreement source. If MW-25 BET is GTO-correct, v3.4 needs amendment too.

### MW-40: AhTs on AdJc5h (BTN IP 4-way checked through; expert BET MEDIUM)

**Step 1 — Reference spec:** `AhTs top pair T kicker, high SPR 4-way IP, checked to hero`. Expert: **BET MEDIUM** with reasoning: "top pair T kicker in position after 4-way check-through at high SPR. Despite the deep stacks, top pair is strong enough to bet after three checks — the checks cap opponents' ranges. However, at high SPR 4-way, hero should bet small (25-30% pot) rather than a standard 50% sizing. Medium confidence because the bet is thin but correct after complete check-through."

**Step 2 — 12.5H corpus alignment:** Targeted by T9' template (TP-medium-kicker IP 4-way after PFR check; 14 hands = 13 parametric + 1 manual). Consensus: 14/14 BET (100% unanimous; avg_conf 1.00). PILOT_691 (T9' canonical = MW-40 exact replica AhTs on AcJc5d) consensus BET 4/5.

**Step 3 — Model inference walk-through (v9-3way-v2.2):**
- Model predicts: **CHECK** (probability 0.572; BET 0.305)
- Margin to expert (BET): **+0.267** ← **closest to flipping among the 5 stay-wrong**
- Top contributions:
  - `pot_size=110` × imp 0.022 = +2.39
  - `hand_category=6` (TP) × imp 0.034 = +0.207
  - `worse_hand_pct=0.833` (hero ahead of 83%)
  - `equity_margin=0.199`

**Step 4 — Counterfactual:**
- Ablate `pot_size` (110→0): no flip; -0.006 expert Δ
- Ablate `hand_category` (6→0): no flip; +0.000 expert Δ
- Ablate `hand_rank` (1.350→0): no flip; -0.025 expert Δ
- Perturb `pot_size` ±20%: no flip

No single feature ablation flips. The 0.267 margin is small enough that **a richer training distribution should move the prediction**.

**Step 5 — Verdict: E-DIST UNDERPOWERED (primary)**

Model is already 30.5% on BET — the closest to flipping among the 5. Features (`hand_category`=TP, `worse_hand_pct`=0.83) correctly identify hero is ahead. Just needs more training-data signal pushing TP+ → BET on multiway-checked-through-high-SPR.

T9' at 14 hands is underpowered. Tripling to ~40 hands with similar structure (TP-medium-kicker on rainbow A-high or K-high; 4-way checked through at deep SPR) should flip this.

**12.5I spec hint:**
- T9' expansion: 30-40 hands on TP-medium-kicker pattern across A-high / K-high / Q-high boards with rainbow + dry textures
- Vary kicker (T/J/Q for second pair); vary board top (A/K/Q); vary hero position (BTN/CO IP)
- Keep PFR-check-through as canonical preflop+flop sequence
- Prediction confidence: **moderate to high** (+0.267 margin is the smallest; corpus expansion should close it)

### MW-45: 6d6c on AcKd6hQs turn (BB OOP facing CO turn lead 4-way; expert RAISE HIGH)

**Step 1 — Reference spec:** `6d6c set (flopped), facing CO turn bet after checked flop, AK6-Q 4-way`. Expert: **RAISE HIGH** with reasoning: "6d6c flopped a set on AK6r and slowplayed through the flop. Now facing CO's turn bet on AKQ. Despite the scary turn card (Q fills AQ two-pair for CO), hero has a full house draw (6 makes a boat) and trips with bottom set. CO's range after passive flop is wide. Hero's set of sixes is still very strong and should raise the turn to protect and extract value."

**Step 2 — 12.5H corpus alignment:** Targeted by T10' template (slowplayed set turn lead 4-way; 14 hands = 13 parametric + 1 manual). Consensus: 14/14 RAISE (100% unanimous). PILOT_692 (T10' canonical = MW-45 EXACT replica) consensus RAISE 5/5 (after re-pilot resolution; original 1-labeller pilot was CALL).

**Step 3 — Model inference walk-through (v9-3way-v2.2):**
- Model predicts: **CALL** (probability 0.820; RAISE only 0.075)
- Margin to expert (RAISE): **+0.746**
- Top contributions:
  - `to_call=75` × imp 0.091 = +6.79 (huge raw value dominates)
  - `pot_size=120` × imp 0.022 = +2.60
  - `hand_category=12` (set/monster) × imp 0.034 = +0.414
  - `facing_bet=1`, `is_monster=1` (model SEES the monster bucket)
  - `raw_equity=0.513`

**Step 4 — Counterfactual:**
- Ablate `to_call` (75→0): no flip; +0.017 expert (RAISE) Δ
- Ablate `pot_size`: no flip; trivial Δ
- Ablate `hand_category`: no flip; -0.013 Δ
- Perturb `to_call` ±20%: no flip

The model correctly identifies hero as monster (`is_monster=1`, `hand_category=12`, `raw_equity=0.513`) but routes to CALL (passive) not RAISE (aggressive). The features that distinguish "set + slowplay-then-face-turn-lead-on-broadway-completed = RAISE" are not strongly weighted.

**Step 5 — Verdict: ISOMORPH-MISMATCH (primary) + E-DIST (secondary)**

T10' parametric hands (PILOT_634-646) all use NON-broadway-completed turn cards (Td/Tc/Js/Jd/Qc) — they don't match MW-45's specific AKQx broadway-completed pattern. T10' canonical PILOT_692 IS the MW-45 exact replica and DID label as RAISE in full phase, but the booster's gain on the 13 different-texture parametric hands didn't transfer to the AKQx texture in the model's reference-hand inference.

**12.5I' (template redesign sub-direction) spec hint:**
- T10' redesign: include broadway-completed turn cards (AKQ-x, AKJ-x, KQJ-x patterns) in parametric configs
- ~20-30 set+turn-lead hands specifically on broadway-saturated turn textures
- Possibly add T10'' variant: set facing turn lead on STRAIGHT-completing turn (different aggression-vs-protection trade-off)
- Re-train with redesigned T10'/T10'' included
- Prediction confidence: **moderate** — model already has the monster bucket + correct equity reading; corpus on the specific texture should close it

### MW-47: AsQs on KsJd5s (SB OOP facing bet+call 4-way; expert CALL raw / RAISE corrected)

**Step 1 — Reference spec:** `AsQs nut FD+gutshot OOP SB, facing bet+call 4-way, KJ5ss`. Expert (raw): **CALL MEDIUM** with reasoning: "AsQs on KJ5ss gives the nut flush draw plus a gutshot to the broadway straight — approximately 15 outs and very high equity (50-55%). Facing a CO bet of 40 + BTN call into a 4-way pot OOP: nut draw power partially offsets OOP disadvantage. Call is correct — equity is strong enough despite position. **Raising as a semi-bluff OOP into bet+call is too aggressive; just call and realize equity.**"

**Solver correction:** RAISE (per `memory/reference_corrections.md`).

**v3.4 Fix 2.1.1 alignment:** v3.4 specifically engineered to fire RAISE for this pattern via clause-e (villain_air ≥ 0.05 floor + bet+call multiway carve-out). v3.4 prompt cites this hand as the calibration anchor: PILOT_599 (RAISE — `villain_air_pct = 0.153`, clause (e) satisfied). The v3.4 protocol DISAGREES with the BATCH2 RAW expert (CALL) and AGREES with the solver-corrected expert (RAISE).

**Step 2 — 12.5H corpus alignment:** Targeted by T-RAISE-stabilize template (12 hands = 11 parametric + 1 manual canonical PILOT_694 = AsQs on KsJd5s — MW-47 exact replica). Consensus: 12/12 RAISE (100% unanimous; avg_conf 0.78). v3.4 Fix 2.1.1 fires correctly.

**Step 3 — Model inference walk-through (v9-3way-v2.2):**
- Model predicts: **CALL** (probability 0.920; RAISE 0.010)
- Margin to expert (RAISE corrected): **+0.910**
- Margin to expert (CALL raw): **0.000** ← **MODEL AGREES WITH RAW EXPERT**
- Top contributions:
  - `pot_size=200` × imp 0.022 = +4.34
  - `to_call=40` × imp 0.091 = +3.62
  - `facing_bet=1` × imp 0.118 = +0.118
  - `raw_equity=0.458` (drawing range)

**Step 4 — Counterfactual:**
- Ablate `pot_size`: no flip
- Ablate `to_call`: no flip
- Ablate `facing_bet`: flips to CHECK (drives FOLD/CHECK toggle)
- Perturb `pot_size` ±20%: no flip

No realistic perturbation flips toward RAISE. The CALL prediction is robust.

**Step 5 — Verdict: E-FEATURE PRIMARY (mixed with raw-vs-corrected expert disagreement)**

Two interpretations:
1. **If MW-47 raw expert (CALL) is GTO-correct:** model is correct; the "stay-wrong" classification is artificially created by the solver-correction overlay. No fix needed; orchestrator should reconsider whether MW-47's solver-correction to RAISE is justified.
2. **If MW-47 solver-corrected (RAISE) is GTO-correct:** the v3.4 protocol agrees and the corpus correctly trains this. Model fails to transfer because the 59-feature surface (and even more so the 45-feature canonical surface) lacks features that distinguish "RAISE-bet+call-multiway-with-NFD+blocker-OOP" from "CALL-bet+call-multiway-without-it". v3.4 Fix 2.1.1 captures this verbally with 5 clauses (a-e); the model has no feature for clauses-(a)+(d)+(e) compound.

**12.5J spec hint (assuming solver-corrected interpretation):**
- New feature `bet_call_multiway_clause_e` (boolean: villain_air ≥ 0.05 in bet+call multiway lines)
- New feature `nfd_blocker_aggression_score` (combined nut-FD + nut-blocker + multiway-pressure signal)
- Or refactor existing `villain_air_pct` to be street-context-aware (current is street-agnostic)
- Cascade per `feedback_attention_flags_when_features_change.md`
- **OR:** orchestrator should re-evaluate whether the solver-correction to RAISE is justified; if not, MW-47 graduates from the stay-wrong list

## Cross-hand patterns (orchestrator-relevant)

### Pattern 1: corpus-vs-reference protocol disconnect (MW-25 + MW-45)

For both MW-25 and MW-45, the v3.4 protocol applied to the CANONICAL replica produces labels that align with the model's prediction (not the BATCH2 reference's expert action):

| Hand | Reference expert | Canonical PILOT_X label | Model prediction |
|---|---|---|---|
| MW-25 | BET | PILOT_689 (Ks7h on As9s5s analog): CHECK 5/5 | CHECK |
| MW-25 | BET | PILOT_690 (AsKh on Js9s3s): CHECK 3/5 | CHECK |
| MW-45 | RAISE | PILOT_692 (6d6c on AcKd6hQs exact): RAISE 5/5 (after re-pilot) | CALL |

For MW-25, the corpus, the model, AND the v3.4 protocol all align on CHECK — the BATCH2 reference's BET is the OUTLIER. Either:
- BATCH2 spec is wrong for MW-25 (worth re-evaluating)
- v3.4 protocol's bucket-first reasoning under-weights the IP-after-check-through-multiway BET-for-fold-equity heuristic
- A labelling-protocol amendment is needed

For MW-45, the canonical PILOT_692 final label is RAISE (matching reference) but model still says CALL. So the corpus IS correct; the failure is transfer.

**Recommendation to orchestrator:** before committing to 12.5J for MW-25 specifically, gto-expert-hat sanity check on whether BET is GTO-correct for Ks7s on As9s5d 4-way checked through. If GTO is genuinely CHECK, MW-25 should be amended in the BATCH2 reference and removed from the stay-wrong list.

### Pattern 2: feature surface inadequacy (MW-17 + MW-47)

Both MW-17 and MW-47 have v9-3way-v2.2 prediction confidences > 0.9 against their expert action. Neither responds to feature ablation in a meaningful way (only ablating `facing_bet` flips, which is a structural FOLD/CHECK gate not a hand-strength signal).

These are E-FEATURE primary — the discriminative axis the expert uses (implied-odds + nut-blocker + chain-narrowing-via-bet+call-multiway) is NOT in the 45-feature or 59-feature surface, OR is present but with insufficient inductive bias.

**12.5J should target:** new features for implied-odds (overcard outs + backdoor outs), nut-blocker-value (suit-specific blocker signal), and bet+call-multiway-context-aware villain-air.

### Pattern 3: tractability ranking (closest to flipping)

By margin to corrected expert (smaller = more tractable):
1. **MW-40** (margin +0.267, BET prob 0.305) — most tractable; T9' expansion likely sufficient
2. **MW-45** (margin +0.746, RAISE prob 0.075) — moderate; T10' redesign + isomorph fix
3. **MW-17** (margin +0.843) — hard; needs feature engineering
4. **MW-25** (margin +0.880) — protocol-disagreement; resolve reference-set first
5. **MW-47** (margin +0.910) — hardest; needs feature engineering OR reference re-evaluation

## Files in PR diff (1 file)

1. `review/comms/BUILDER_REPORT_PHASE125I_PRE_DIAGNOSTIC_2026-05-06.md` (NEW, this file)

No `scripts/diagnostic_125i_pre.py` shipped — analysis was reproducible via inline python heredoc + existing `river-rats-core` modules (`reference_evaluator.parse_reference_hands`, `feature_extractor.extract_all_features`, `gto_model.FEATURE_COLUMNS`, xgboost). Re-running requires only loading the canonical model + parsing the reference set.

## Stop conditions checked (per dispatch)

- ✅ Diagnostic ambiguous on >1 hand: 0 hands ambiguous (all 5 classified with primary residual)
- ✅ Counterfactual analysis required no re-training (used existing v9-3way-v2.2 artifact)
- ✅ Diff scope: 1 file (under the 2-file limit)
- ✅ No solver call (used solver corrections from `memory/reference_corrections.md` only as expert-action overlay)

## Recommended 12.5I + 12.5J parallel split

| Direction | Hands | Approach | Estimated probability of fixing the hand |
|---|---|---|---:|
| **12.5I corpus expansion** | MW-40 | T9' to 30-40 hands; same template structure | **70-80%** (small margin + good corpus alignment) |
| **12.5I corpus expansion** | MW-25 | T8' redesign for "BET after check-through"; protocol amendment likely needed | **30-40%** (protocol disagreement is the bottleneck) |
| **12.5I' template redesign** | MW-45 | T10' include AKQx-broadway-completed turns; ~25 hands | **50-60%** (model has features; corpus needs the specific texture) |
| **12.5J feature engineering** | MW-17 | implied-odds + nut-blocker-value + backdoor-outs features (3 new features + cascade) | **40-60%** (requires feature engineering quality) |
| **12.5J feature engineering** | MW-47 | bet+call-multiway-context-aware features OR reference re-evaluation | **30-50%** (depends on raw-vs-corrected expert resolution) |

**Aggregate gap-close estimate (vs current 32/40):**
- 12.5I alone (3 hands): 70% × 1 + 30% × 1 + 50% × 1 ≈ 1.5 expected hand flips → median 33-34 / 40
- 12.5J alone (2 hands): 50% × 1 + 40% × 1 ≈ 0.9 expected hand flips → median 32-33 / 40
- Combined 12.5I + 12.5J (5 hands): ~2.4 expected hand flips → median 34-35 / 40

Median ≥33 (gate) appears tractable from 12.5I alone. 12.5J is the harder direction but addresses the structurally-hardest hands (MW-17 / MW-47 are E-FEATURE primary, not solvable by corpus alone).

## What's blocked / what's queued

**Blocked:**
- 12.5I-pre QC trigger → on this PR open
- 12.5I-pre merge → on QC APPROVE
- **12.5I (D) + 12.5J (C) parallel dispatch → on 12.5I-pre merge** per dispatch §"Sequencing"

**Queued (post-12.5I-pre):**
- 12.5I corpus expansion: 30-40 hands per template (T9' for MW-40; T10' redesign for MW-45; T8' redesign + protocol question for MW-25)
- 12.5J feature engineering: implied-odds + nut-blocker + bet+call-multiway-context features per `feedback_attention_flags_when_features_change.md` cascade (raw + attention vocab + prompt + capture + trainer)
- Both 12.5I + 12.5J ship into combined 12.5K final re-train when both deliver
- 12.5K gate evaluation: median ≥33 = PROMOTE
- **NEW (orchestrator-decision queue):** MW-25 and MW-47 reference-set spec re-evaluation; verify expert actions are GTO-correct before investing in corpus/feature work that may not move the gate if reference is wrong

## References

- 12.5I-pre dispatch: master `d366aee` (PR #192)
- 12.5H-F synthesis: master `ea642ed` (PR #191)
- 12.5H-E re-train: master `283af91` (PR #188)
- 12.5H-C labels final: master `690ca8f` (PR #184)
- Reference set: `design/multiway_reference_set/BATCH2_8_HAND_DESIGNS.md` + `BATCH2_8_RANGE_ANALYSIS.md`
- Solver corrections: `~/.claude/projects/-home-rupertbeytell/memory/reference_corrections.md`
- Canonical model: `river-rats-core/models/gto_model_v9_3way_v2.2.json` (45-feature)
- Feature surface: `river-rats-core/feature_extractor.py` (59 features); `river-rats-core/gto_model.py` (45/55 surfaces)
- v3.4 protocol: `prompts/gto_labeller_v3.4.md` (Fix 2.1.1 at line 880)
- ml-architect 12.5D' Q4 H-FEAT prediction: `/tmp/ml_architect_125d_prime_findings.md`
- gto-expert 12.5D' per-hand classification (E-FEATURE primary on MW-17/47): `/tmp/gto_expert_125d_prime_findings.md`
- Memory: `feedback_pilot_first_for_long_jobs.md` (12.5I-pre IS the pilot for D+C parallel commit), `feedback_quality_default_no_ask.md`, `feedback_attention_flags_when_features_change.md` (12.5J cascade requirements), `feedback_solver_vs_expert_labels.md`

**Status: 12.5I-pre DIAGNOSTIC COMPLETE. 5 hands classified: 3 → 12.5I (corpus); 2 → 12.5J (feature engineering). Recommended parallel dispatch with non-overlapping hand assignments. Median-≥33 gate appears tractable from 12.5I alone; 12.5J targets the structurally-hardest hands. Surface NEW orchestrator queue: MW-25 + MW-47 reference-set spec re-evaluation before committing.**
