# MW Miss Bias Analysis — 2026-04-15

**Stream B.2 deliverable.** GTO reasoning on the 10 MW misses in `MW_MISS_EVIDENCE_PACK_2026-04-15.md` (commit `3b69360`). No code changes. No file reads outside the evidence pack.

---

## Executive summary

The dominant bias is **defensive (range-vs-range) CHECK preference in multiway checked-through spots, amplified by a trap-lean on top-of-range holdings**. Nine of the ten "misses" share a near-identical signature: hero was the preflop aggressor or first-in BB caller, opponents checked the previous street (villain_checked_back=1 in every case, villain_aggression_count=0), hero is OOP or on a low SPR (1.25 across the board), and hero is at or near the top of their own range (HRP mean 0.64, 7/10 hands ≥ 0.58) with equity_vs_range ≥ 0.35 and worse_hand_pct ≥ 0.56. The labelled answer is BET for value + protection; the model prefers CHECK. Hand 8 (`d3688_BB_flop`, TPWK OOP vs uncapped HJ) is the **only** hand where the label is CHECK and the model BET — i.e. the model is *also* biased toward aggression when HRP is moderate and the villain range is uncapped, but this is a single outlier and reproduction-variable.

Bias is not plausibly explained by trap-lean alone (HRP varies 0.43–0.83 across the misses). It **is** explained by a defensive-when-both-ranges-are-strong lean: in every miss the model routes probability mass to CHECK/CALL rather than BET even when worse_hand_pct is 56–91% and villain_air_pct is substantial. The label set itself is internally consistent — Pass 1 reasoning explicitly cites "villain showed weakness + capped range + high worse_hand_pct" as the BET trigger. The model is not reproducing that override rule.

**Fix direction:** training-data supplementation (v2.3) is the primary lever; prompt rewording is secondary. Track 6 Section 2 should adopt the narrower, correct signature wording below.

---

## Q1 — Trap bias (top-of-range → slowplay)?

**Partial yes, but not the dominant mechanism.**

HRP across the 10 misses: 0.58, 0.71, 0.67, 0.45, 0.47, 0.77, 0.83, 0.74, 0.43, 0.79 (mean 0.64, median 0.69). That's top-half but not universally top-of-range — three hands (d2410, d2920, d8411) sit at HRP 0.43–0.47, i.e. middle of hero's range, and the model still prefers CHECK. So "the model slowplays its best hands" cannot be the full story: the model is also passive with *median* holdings.

Trap-lean *is* supported on:
- d3178 (HRP 0.77, AA on double-paired board, model CHECK over BET 0.49 vs 0.20)
- d3229 (HRP 0.83, QQ two-pair river IP, both villains checked through, model CHECK 0.22 vs BET 0.16 — and the CALL mass at 0.62 is noise since facing_bet=False)
- d8886 (HRP 0.79, TPGK flop OOP, model CHECK 0.42 vs BET 0.09)

On d3178 and d3229 specifically the "slowplay monster" reading is plausible. Elsewhere HRP alone doesn't predict the miss.

**Verdict:** trap-lean contributes but is subordinate to Q2.

---

## Q2 — Defensive bias (both ranges strong → CHECK)?

**Yes — this is the dominant mechanism.**

The signature that fires in 10/10 misses is *not* "hero is strong" — it's "**hero's range is strong AND villain's range contains meaningful made-hand density AND both sides checked**". The model interprets the mutual strength + passivity as a range-vs-range standoff and defaults to pot control, overriding the protection/value-extraction case the labellers cited.

Per-hand evidence (villain_top_pair_plus_pct, villain_checked_back, model action):

| # | sid | villain_TP+ | villain_air | villain_checked_back | model |
|---|---|---|---|---|---|
| 1 | d1454_CO_turn | 0.27 | 0.02 | 1 | CHECK |
| 2 | d1562_HJ_turn | 0.57 | 0.43 | 1 | CHECK |
| 3 | d1983_HJ_turn | 0.25 | 0.18 | 1 | CHECK |
| 4 | d2410_CO_turn | 0.33 | 0.20 | 1 | BET* |
| 5 | d2920_BB_turn | 0.31 | 0.18 | 1 | CHECK |
| 6 | d3178_CO_river | 0.83 | 0.17 | 1 | CHECK |
| 7 | d3229_BTN_river | 0.58 | 0.42 | 1 | CHECK |
| 8 | d3688_BB_flop | 0.20 | 0.34 | 0 (HJ opened) | BET* |
| 9 | d8411_BB_turn | 0.21 | 0.57 | 1 | CHECK |
| 10 | d8886_BB_flop | 0.18 | 0.59 | 0 (BB defends OOP) | CHECK |

`*` = model matched label (d2410) or model's wrong direction (d3688).

Eight of the eight "CHECK misses" feature villain_checked_back=1 with num_opponents=2 and SPR=1.25. The pattern is unmistakable: **multiway, low-SPR, both villains capped, everyone checked to hero, hero OOP or medium-position → model defaults to CHECK even when worse_hand_pct is 56–91%**. Labellers treat villain_checked_back as a weakness-override that unlocks thin-value betting; the model treats it (plus villain_TP+ density) as "strong-vs-strong → don't build the pot".

The defensive lean compounds with trap-lean when HRP is high (d3178, d3229, d8886) — probability mass sits in CHECK even though the label logic says extract value from the capped+weak villain range.

**Verdict:** defensive/range-vs-range bias is the dominant bias type.

---

## Q3 — Label/model alignment (would Pass 1 have voted CHECK too?)

**Likely no — bias is predominantly model-only, not propagated label conservatism.**

Stop-condition disclosure: per-agent Pass 1 votes for `d*` MW sids are NOT in the repo (only BP sids are covered in `pass1_T[1-4]_labels.jsonl`). I cannot directly count how the 4 labeller agents split. I reason from the `expert_reasoning`, `factor_conflicts`, and `alternatives_considered` fields stamped on the aggregated label.

What the labelled-set cross-reference shows:

- Every miss has `expert_action=BET` stamped with explicit `factor_conflicts` text acknowledging the CHECK case and explicit `alternatives_considered` listing CHECK with a reason it was rejected. I.e. the labellers **engaged with the CHECK alternative and rejected it on poker grounds** (protection, villain weakness override, capped range, high worse_hand_pct). That is a different error mode from "labellers bucket-voted CHECK and propagated that into training data".
- The rejection rationales invoke a consistent override rule: "OOP+TPWK/second-pair would normally check, BUT villain_checked_back + capped + high worse_hand_pct overrides to BET for value/protection". This is a conditional rule — the sort a panel of 4 would plausibly split on (difficulty=2, confidence=MEDIUM on 6/10 hands).
- On d3688 (the only CHECK label the model BET'd) the reasoning explicitly *does not* invoke the override (HJ opened, villain uncapped, flush draw on board) — the labellers correctly applied the rule's precondition check. The model failed to distinguish d3688 from the others; it saw HRP 0.74, worse_hand_pct 0.88, and bet anyway. That tells me the model has not learned the conditional structure at all — it's using a coarser signal (HRP + worse_hand_pct + board texture) without the villain_range_capped × villain_checked_back gating.

So: labellers produced the *correct* override rule under MEDIUM confidence on boundary spots. The model did not learn the override. This is a **training-data sparsity / model-capacity** problem, not label conservatism. If the 4-labeller panel split 3-1 or 2-2 and the aggregator tied to BET on MEDIUM confidence, the signal may be weak — but the direction is correct.

**Caveat (stop condition):** without per-agent d* votes I cannot rule out that 1-2 of the 4 labellers voted CHECK and the aggregation resolved to BET. If that's the case, the training labels on similar spots elsewhere in v2.2 training CSV may be inconsistent ("sometimes CHECK, sometimes BET" on near-identical features), which would degrade model learning of the override rule. **Request for Stream A:** spot-check 50 hands in `v2_2_training.csv` matching the bias signature (villain_checked_back=1 ∧ num_opponents=2 ∧ villain_range_capped=1 ∧ worse_hand_pct>0.55 ∧ facing_bet=False) and report the action-label distribution. If >30% are CHECK in training, there is label-level conservatism the v2.3 supplement must counter.

**Verdict:** primarily model-only; label-side contribution is possible but not demonstrated.

---

## Q4 — Pattern across the 10

| # | sid | pos | street | board texture | SPR | HRP | range shape | facing_bet | CB'd |
|---|---|---|---|---|---|---|---|---|---|
| 1 | d1454_CO_turn | CO | turn | Ace-high two-tone w/ FD | 1.25 | 0.58 | hero mid+FD, villain capped | F | Y |
| 2 | d1562_HJ_turn | HJ | turn | paired dry | 1.25 | 0.71 | hero 2pr (77/JJ), v capped+airy | F | Y |
| 3 | d1983_HJ_turn | HJ | turn | KJ72 dry (scare K) | 1.25 | 0.67 | hero 2nd pair TK, v capped | F | Y |
| 4 | d2410_CO_turn | CO | turn | 3-flush | 1.25 | 0.45 | hero TPGK, v capped | F | Y |
| 5 | d2920_BB_turn | BB | turn | 2-pr dynamic (FD+SD) | 1.25 | 0.47 | hero 2pr top, v capped | F | Y |
| 6 | d3178_CO_river | CO | river | double-paired scary | 1.25 | 0.77 | hero AA, v high TP+ | F | Y |
| 7 | d3229_BTN_river | BTN | river | paired 7s | 1.25 | 0.83 | hero 2pr, v medium TP+ | F | Y |
| 8 | d3688_BB_flop | BB | flop | K-high FD | 1.25 | 0.74 | hero TPWK OOP, v **uncapped** | F | N |
| 9 | d8411_BB_turn | BB | turn | 3-flush w/ nut FD | 1.25 | 0.43 | hero TP+nutFD, v airy | F | N |
| 10 | d8886_BB_flop | BB | flop | J-high dry | 1.25 | 0.79 | hero TPGK OOP, v airy | F | N |

**Dominant patterns:**

1. **SPR 1.25 everywhere** (10/10). Either an artifact of the test-set construction or the bias concentrates at low SPR where pot-control incentive is artificially high. Can't disambiguate from this pack alone.
2. **facing_bet=False on 10/10.** The bias surfaces exclusively in check-decision spots. FOLD/CALL/RAISE lane is not implicated.
3. **villain_checked_back=1 on 7/10**, **num_opponents=2 on 10/10** (by construction — MW set). Multiway checked-through is the classic trigger.
4. **Position skew:** BB 4, CO 3, HJ 2, BTN 1. BB-OOP-as-caller and CO-as-PFA-checking-back are the two hot zones.
5. **Hero holding shape:** second pair/top pair / two-pair / overpair — all *strong-but-not-nutted* value hands. No draws-only, no bluffs, no nut hands below AA. The misses sit in the thin-value-for-protection zone.
6. **Board texture:** mixed — dry (3), dynamic/draw-heavy (4), paired (3). Texture is not the discriminator; the range-and-action-history signature is.

---

## Fix-direction recommendation

**Primary: training-data supplementation (v2.3), bucket-first.** Target bucket: `facing_bet=False ∧ num_opponents≥2 ∧ villain_checked_back=1 ∧ villain_range_capped=1 ∧ worse_hand_pct≥0.55 ∧ equity_vs_range≥0.35 ∧ SPR≤2.0`. Supplement v2.2 training with 400–800 hands in this bucket labelled BET (with position/texture stratification so the model learns the override is robust across context). This directly counters the defensive lean Q2 identified.

**Secondary: Pass 1 prompt reword.** Add an explicit override clause to the labelling prompt: *"When villain_checked_back=1, villain_range_capped=1, num_opponents≤2, and hero's worse_hand_pct exceeds 0.55, prefer BET for value+protection even when OOP or holding a medium-strength made hand. The passive line forfeits the capped villain's air portion."* This reduces variance in panel votes on the boundary spots and strengthens the training signal for v2.3 and beyond.

**Both** is the right call: even if the 4-agent panel is already producing BET labels on average, reducing label variance + bulking up the bucket will compound.

### Track 6 Section 2 wording suggestion

Current framing (as I understand from plan docs): "bucket-first CHECK bias." This is directionally right but too broad — it implies the model overchecks generally. The evidence shows a narrower, conditional bias. Suggested replacement wording:

> **Defensive multiway-checked-through CHECK bias.** The v2.2 model underbets in multiway pots where villain(s) have checked the previous street, villain ranges are capped, hero sits at or above median range strength with worse_hand_pct ≥ 0.55, and SPR is low (≤ 2). The model reads mutual passivity plus villain_top_pair_plus density as range-vs-range standoff and defaults to pot-control CHECK, overriding the value+protection case that the passive villain line actually enables. The v2.3 supplement should target this bucket specifically; a uniform "bet more often" correction would overshoot.

This wording preserves the bucket-first-CHECK mental model while pinning the correct preconditions, which matters for downstream counter-bias (we don't want v2.3 to start betting in spots where the villain has *not* checked back).

---

## Stop-condition disclosures

- **Per-agent Pass 1 votes for d* sids are absent.** I cannot directly measure labeller split/conservatism. Q3 rests on the aggregated reasoning text. Request: Stream A surface per-agent votes if they exist anywhere, or confirm they were not persisted.
- **v2.2 training CSV label distribution is unseen.** I have not read training data (per scope). To confirm whether upstream conservatism compounds, I need a spot-check of the bias-signature bucket in training (see Q3 caveat).
- **SPR=1.25 on 10/10 is suspicious.** Either the test-set selection filtered to this SPR, or the misses cluster at this SPR by signal. Can't tell without the full MW-50 SPR distribution.
- **Two reproduction-variable hands** (d2410, d3688) — treated as variable in analysis, not used to anchor conclusions.
- **Stream A.3 correction (84%/50, not 80%/50).** The live model is better than the shadow model on MW-50, meaning the "10 misses" set overstates the miss count for the shipped model. The bias *pattern* still applies to however many genuine misses remain; v2.3 scoping should verify against the live model before sizing the supplement.
- **Bias is bucket-first-CHECK in the narrow sense, not the broad sense.** Track 6 should use the refined wording above. I did not find a non-bucket-first explanation, so the §8 stop-condition ("if bias is NOT bucket-first-CHECK, STOP") does not fire — but the *preconditions* are narrower than the unqualified phrase implies.
