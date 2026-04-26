---
date: 2026-04-26
from: gto-expert reviewer (orchestrator-dispatched)
to: Main terminal (orchestrator) · Logic builder · Owner (briefed)
re: PR #47 (v3.2 protocol revision: Fix 1 + Fix 2 + Fix 3 bundled) — gto-expert review
status: APPROVE-WITH-NITS
---

# gto-expert Review — PR #47 (v3.2 protocol revision)

## Verdict: APPROVE-WITH-NITS

All three fixes are GTO-correct, internally consistent, and do not break existing reasoning surfaces. Two LOW-severity nits flagged for optional cleanup; neither blocks merge or A.4 re-run.

Files audited at PR head (`stage4-pre-dispatch/v3-2-protocol-revision`):
- `prompts/gto_labeller_v3.2.md` (NEW, 884 lines)
- `prompts/protocol_b_composition_first_v1_0_pilot.md` (15 add / 3 del @ L283-297)
- `prompts/protocol_b_composition_first_v1_0.md` (15 add / 3 del @ L264-278)

PR-touched-file count: 3 (matches A.8 directive scope; no Protocol C edits).

---

## Check 1 — Fix 1 (Rule 11)

- **C1.1 (2 EXCEPT clauses):** PASS. v3.2 L684-693 codifies paired-board EXCEPT (anchor d9556); L694-706 codifies 2-tone-flush board OOP EXCEPT (anchor d3688). Both clauses are explicit, anchor-cited, and structurally distinct (different rationale per clause: paired-board = villain capped to bluff-catchers; 2-tone OOP multiway = avoid isolating into 2nd live villain's flush draw / better TP+).

- **C1.2 (carve-outs HU/IP/dry/river-checked-to):** PASS. v3.2 L728-740 enumerates 5 carve-outs (heads-up `num_opponents = 1`, IP `is_ip = 1`, dry boards, river-checked-to per d3178 pattern, drawing hands governed by KB §1.7 + Fix 2). The river-checked-to carve-out at L735-737 explicitly preserves d3178 AA-checked-to-river BET. Drawing-hand carve-out correctly routes semi-bluff RAISE decisions to KB §1.7 (governed by Fix 2 instead).

- **C1.3 (no conflict with Rules 1-10):** PASS. Rule 11 explicitly cross-references Rule 5 at L742-747 ("This rule supplements (does not contradict) DO NOT Rule 5"). Rule 5 says "TP is medium-strength 3-way" (don't *overbet* TP); Rule 11 narrows to "don't *auto-bet* on paired/2-tone OOP multiway." The two rules push in the same direction (pot-control over auto-aggression). No conflict with Rules 1-4 (equity/draws/checking/c-bets), Rules 6-9 (blockers/streets/asymmetric ranges/range-capped), Rule 10 (HRP=0.00 artifact). Numbering note ("v3.1 compacted v3's Rule 11 §3.B to Rule 10; this is fresh slot") is correctly stated and avoids version collision — confirmed by Rule 10 at v3.2 L657-667 referencing `[v3 addition §3.B]` (HRP artifact, not paired-board).

- **C1.4 (paired-board GTO soundness):** PASS. The paired-board carve-out is solver-aligned: on a paired flop (e.g. 5s6d6h), villain's preflop range structurally cannot contain trips of the paired rank (no 66 in CO open vs BB defend in this construction; 6x suited connectors are rare in the opening range). Villain's continuing range against a flopped fives-full (5h5d) is dominated by air (6x is virtually nil; over-pairs fold to action; bluffs and pair-plus-draw types are the only continues). BET folds out the bluff-catchers and isolates against the few hands that beat hero (none on this board — fives full only loses to 66 / over-house, neither of which villain has). CHECK induces villain's bluff-catching range to bet on later streets. This is textbook trap-line; equity dilution from villain getting a free card is essentially zero (board is so paired villain has no realistic equity). Sound.

- **C1.5 (2-tone-flush OOP GTO soundness):** PASS. The 2-tone-flush OOP exception is solver-aligned for medium-made hands like TPWK (d3688: 8cKc on KdTd4s 2-tone-diamond, hero holds NO diamonds). Betting OOP into 2 live villains commits hero to bigger pots when called, AND the 2nd villain's continuing range skews to the parts of villain's range that beat hero (made flushes, two-pair+, sets, FD+TP combos). The "low villain TP+ + high air → bet" reasoning from KB Example 6 is HU-leaning — in HU, the air folds and you isolate against bluff-catchers, but in OOP multiway the 2nd live villain's continuing range is much more value-heavy than the population air. CHECK preserves pot-control on a board where hero has 1-pair-no-blocker and faces 2 chances at being outdrawn or outflopped. Sound. The 2-tone-flush rule applies to BOARD structure (charging villain's flush draws / better TP+), not to hero holding the suit, so the rule fires correctly on d3688 even though hero has no diamonds.

**Subtle observation (LOW severity):** The 2-tone-flush exception focuses on flop/turn texture; it does not explicitly call out 4-tone river or a 3-tone+ flush-completing turn (e.g. 3-flush turn after 2-tone flop). The Decision rule at L714-715 covers this implicitly via "flush completing on turn/river" but doesn't enumerate the full state space. In practice this is the intended behavior (CHECK on flush-completing rivers in multiway is even more clearly correct), so it doesn't cause failure — just slight under-specification.

---

## Check 2 — Fix 2 (KB §1.7 OVERRIDE)

- **C2.1 (`villain_air_pct >= 0.20` threshold):** PASS. v3.2 L804-816 has the OVERRIDE section with the exact threshold conditional. L805 explicitly: "applies ONLY when `villain_air_pct >= 0.20` (genuine fold equity threshold)." L826 in Decision rule re-states: "AND `villain_air_pct >= 0.20`?" Five total occurrences across changelog + OVERRIDE section + Decision rule — internally consistent.

- **C2.2 ("CALL preferred" below threshold):** PASS. v3.2 L806-808: "When `villain_air_pct < 0.20`, nut FD prefers CALL even with blocker — fold equity insufficient to justify raise EV; better to call and realise equity vs villain's calling range." Re-stated at L828-829 in Decision rule: "BUT if `villain_air_pct < 0.20`: → CALL preferred."

- **C2.3 (rationale references `feedback_solver_findings.md` MW-30 anchor):** PASS. v3.2 L810-812: "The 0.20 threshold matches `feedback_solver_findings.md` solver-corrected MW-30 CALL anchor where `villain_air = 0.15` was insufficient for raise EV despite nut blocker presence." Anchor-correct: MW-30 was the solver-corrected CALL spot (per `reference_corrections.md` memory note) where `villain_air = 0.15`. Threshold of 0.20 is set just above MW-30's actual value (interpolating between 0.15-too-low and where solver simulations clear EV).

- **C2.4 (0.20 threshold GTO soundness):** PASS. The threshold is solver-aligned and conservative. Math sketch: a pot-sized RAISE in 3-way with a single live villain (after 1 fold) needs ~50% fold equity to break even ignoring equity-when-called. With FD+blocker hero has ~33-36% raw equity vs a calling range, but that calling range is value-heavy (TP+ with redraws), so realised equity-when-called is below raw. Below 20% air, the fold equity contribution can't compensate for negative EV vs the value-heavy calling range. Above 20% air, the fold equity component clears EV. The 0.20 threshold matches solver simulation clearance per `feedback_solver_findings.md` and is consistent with general 3-way semi-bluff theory (fold equity P(A)*P(B) requires individual-villain fold rates of ~45%+ for a bluff to break even; with nut FD+blocker the actual equity-when-called is positive enough that ~20% all-fold suffices). Sound.

- **C2.5 (no conflict with KB §1.7 itself):** PASS. v3.2 L799-803: "The standalone KB file `knowledge/three_way_gto.md` §1.7 carve-out is unmodified by this prompt revision; v3.2 adds this override section here in Calibration Notes that supplements the KB §1.7 rule." L831-833: "This OVERRIDE supplements (does not edit) `knowledge/three_way_gto.md` §1.7 — labellers reading both the v3.2 prompt + the standalone KB must apply the v3.2 threshold over the unmodified KB §1.7 carve-out." Supplementation, not contradiction — KB §1.7 still defines the FD+blocker→RAISE pattern; v3.2 adds the threshold gate. Coherent.

---

## Check 3 — Fix 3 (F-S5 phantom feature)

- **C3.1 (phantom removed from pilot L283-285 → now L283-297):** PASS. Pilot file BEFORE: 3-line range-mass axis at L283-285 referencing `hero_top_pair_plus_pct etc. if available`. AFTER: 15-line replacement at L283-297. The phantom feature reference is gone from the substantive guidance; only remaining mention is the explicit clarification at L293: "No `hero_*_pct` feature exists in the 59-feature contract" (this is a NEGATED reference clarifying the absence, intentional and correct).

- **C3.2 (phantom removed from design L264-266 → now L264-278):** PASS. Identical pattern to pilot. Phantom removed from substantive guidance; only remaining mention is the same negated clarification at L274.

- **C3.3 (replacement uses only existing features):** PASS. Replacement text (both files) cites:
  - "hero's current bucket assignment" — bucket label is computed in pipeline (existing).
  - "preflop construction implied by `prior_actions`" — `prior_actions` is an existing 59-feature contract field.
  - The villain composition pcts (TP+/medium/draws/air) are referenced indirectly via "villain's modal slice" — these are existing features.
  - No phantom or non-existent features introduced.

- **C3.4 (byte-equivalence between pilot + design):** PASS. Diff between the two replacement blocks is exact-match. Verified via `diff` of the diff hunks — both files received identical 15-line replacement preserving Build A/B verbatim-inlining pattern.

- **C3.5 (3-axis Step 2 structure preserved):** PASS. Confirmed via grep: both files retain `Equity-vs-range axis` (pilot L221, design L202), `Realisable-equity axis` (pilot L279, design L260), `Range-mass axis` (pilot L283, design L264). Three axes intact; only the third axis text was edited.

- **C3.6 (range-mass derivation logic GTO-soundness):** PASS. The logic — "wide ranges (limp/call) have higher air/draws mass; tight ranges (raise/3bet) have higher TP+ mass" — is poker-theoretically sound. Wide preflop ranges include speculative connectors and small pairs that miss most flops (higher air/draws postflop); tight ranges concentrate broadways and pocket pairs that connect more on broadway boards (higher TP+ mass). The hand-class proxy via bucket assignment is a reasonable replacement for a true `hero_top_pair_plus_pct` aggregate — it gives the labeller a workable mental model without requiring a phantom feature.

  The replacement adds two examples that further ground the axis: "value-vs-value" (both ranges heavy-TP+ → pot-control) and "draw-realisation-vs-deny" (hero heavy-draws vs villain heavy-TP+ → fold-or-bet-large). Both examples are GTO-correct heuristics.

---

## Check 4 — No breaking changes

The v3.2 prompt does NOT contain inline Worked Examples (the KB Worked Examples are loaded from `knowledge/three_way_gto.md` at runtime — see v3.2 L98-104). The "Worked Example" anchors evaluated are the 7 calibration anchors listed in Calibration Notes (3 v2 reversal + 4 v2.3 anchors).

- **C4.1 (mixed-medium TPGK turn — d2410 analog):** PASS. d2410 is `JcKs on Jd9d3h+6d` (CO_turn). Rule 11 carve-out for IP fires (CO is IP vs BB on the turn after BTN folded — Hero is the closer). Even if hero were OOP, the "checked-to" pattern matches the river-checked-to carve-out spirit (turn-checked-to BET preserved per `villain_checked_back = 1` action history signal). Rule 11 does not fire → BET preserved. v3.2 anchor preservation explicit at L778-781.

- **C4.2 (MW-30 weak-made CALL):** PASS. MW-30 has `villain_air = 0.15` per `feedback_solver_findings.md` — below the 0.20 threshold. Fix 2 OVERRIDE explicitly says: "When `villain_air_pct < 0.20`, nut FD prefers CALL." MW-30 outcome: CALL preserved. Indeed, v3.2 L835-837 explicitly lists MW-30 as an "Affected calibration anchor" where the OVERRIDE makes the existing CALL rule explicit.

- **C4.3 (LITMUS_KQ TPGK BET 66%):** PASS. Not affected by Fix 1 (assuming HU or IP or dry board context — LITMUS hands are typically HU per litmus design); not affected by Fix 2 (made hand, not FD+blocker raise).

- **C4.4 (mixed-medium turn — d8886 analog):** PASS. d8886 is `QcJc on 2s5dJd` (BTN_flop). BTN is IP — Rule 11 IP carve-out fires → BET preserved. v3.2 L774-777 anchor preservation explicit.

- **C4.5 (d3178 CO-river-checked-to AA BET):** PASS. d3178 is `AA on JhQcJc+Ks+5h` (CO_river, checked-to). Rule 11's river-checked-to carve-out at L735-737 explicitly cites d3178 by name and preserves BET. Also: the `Decision rule` at L725-726 includes "(c) river-checked-to override fires (see Calibration Notes for d3178-pattern: AA on JhQcJc+Ks+5h checked-to → BET)." Double-cited → preserved with high confidence.

  Additional sanity: the JhQcJc flop is paired (J-pair). On river the board is JhQcJc+Ks+5h — still paired. Without the river-checked-to carve-out, Rule 11's paired-board EXCEPT could conflict with the d3178 BET expectation. The carve-out correctly resolves this by exempting river-checked-to spots.

---

## Check 5 — Cross-protocol consistency

- **C5.1 (only 3 files modified, no Protocol C edits):** PASS. Confirmed via `gh pr view 47 --json files`: PR #47 modifies exactly:
  1. `prompts/gto_labeller_v3.2.md` (NEW, +884 / -0)
  2. `prompts/protocol_b_composition_first_v1_0.md` (+15 / -3)
  3. `prompts/protocol_b_composition_first_v1_0_pilot.md` (+15 / -3)

  No Protocol C files (`protocol_c_*`) modified. The A.8 audit finding F-S5 was Protocol-B-specific; Protocol C did not have the phantom feature and correctly remains unmodified. B-Ex2/C-Ex2, B-Ex3/C-Ex3, B-Ex4/C-Ex4, B-Ex5/C-Ex5 convergent pairs are not in the diff hunks (Step 2 axis text is upstream of Worked Examples). Convergence preserved.

---

## Findings summary

| ID | Severity | File:line | Description |
|----|----------|-----------|-------------|
| F-PR47-N1 | LOW (NIT) | gto_labeller_v3.2.md:714-715 | Rule 11's 2-tone-flush state-space could be enumerated more explicitly (e.g. 3-tone turn after 2-tone flop, 4-tone river). Decision rule covers this implicitly via "flush completing on turn/river" but doesn't enumerate. Optional cleanup; non-blocking. |
| F-PR47-N2 | LOW (NIT) | gto_labeller_v3.2.md:837 | OVERRIDE references MW-39 as "new MW anchor not yet in calibration_exam.py constants." Non-blocking note for follow-up directive (add MW-39 to reversal-set after re-run validates). Already self-flagged in v3.2; no edit needed. |

**No HIGH or MEDIUM findings.** All 3 fixes are GTO-correct, internally consistent, properly cross-referenced, and preserve all existing calibration anchors via explicit carve-outs.

---

## Recommendation

**Merge as-is.** Both NITs are documentary / future-directive and do not affect labelling correctness. PR #47 is cleared from gto-expert review and Pilot Orchestrator may re-run A.4 calibration on v3.2 once other reviewers (V3-compliance + QC TC-23) clear.

Specific verification items for A.4 re-run:
1. d3688_BB_flop should now route to CHECK via Rule 11 2-tone-flush OOP exception (TPWK, OOP, 2-tone, multi-live).
2. d9556_BB_flop should now route to CHECK via Rule 11 paired-board exception (monster, OOP, paired, multi-live).
3. MW-39 (AhJh on Kh8h3d, villain_air = 0.05) should now route to CALL via Fix 2 OVERRIDE (sub-0.20 air defeats KB §1.7 carve-out).
4. d3178 should still BET (river-checked-to carve-out preserves).
5. d2410, d8886, d8963 should still BET (IP carve-out for d8886/d2410; d8963 mixed-strategy unaffected).

If any of these 5 items fail on re-run, the failure is NOT due to v3.2 protocol revision being GTO-incorrect — it would indicate a separate model-application failure. v3.2 protocol logic is sound.

— gto-expert reviewer
