# PRACTICAL PRO REVIEW PASS #2 — Stage 3.5 v2 + v2.1 supplement

Reviewer: practical pro, second pass
Reviewed artifacts: `BUILDER_V24_STAGE35_BLUEPRINT_V2_2026-04-22.md` (8bb0f9f) + `BUILDER_V24_STAGE35_BLUEPRINT_V2_1_SUPPLEMENT_2026-04-22.md` (3166759)
Date: 2026-04-22

---

VERDICT: APPROVE_WITH_FIXES

---

PLAYER-IMPACT ASSESSMENT

- **T_J01 (owner H_d9edab5d) post-fix vs today:** Today, with 0.70/0.04/0.26 post-fix vs 0.72/0.06/0.22 pre-fix, the player sees "same answer, slightly different noise." The reauthored 0.55/0.04/0.00/0.41 in §3.6 finally gives the hand what a live player reasons: villain's turn-check denies most strong-value hands (they bet twice for value on that Q-high turn), river donk after the check-through is *polarised* — weak showdown hands usually give up, so the bet is thick-value + bluffs. 41% air is the key shift and is exactly what the owner's intuition says. **Direction correct.**

- **T_B01 / T_B04 check-raise (78% / 92% TP+):** Matches how a pro reads a live amateur x/r line. At NL25-100 where owner plays, recreational x/r is almost never with mediums — either a set/two-pair or a semibluff draw. 78% TP+ with 8% draw is a live-realistic composition. T_B04 at 92% is aggressive; in live amateur pools a turn x/r is even tighter than solver (bluff-frequency near zero), so the number holds.

- **T_K05/K06/K07 (delayed probe / multi-street check-then-stab):** This is the core lesson that makes or breaks the oracle as a teaching tool. **These are the hands amateurs lose stacks on because villain's river bet after two checks looks "weak."** Post-fix 55/04/00/41 (K05) and 62/05/00/33 (K06) teach the right thing: these lines are bluff-heavy, hero gets to call wider. Without this fix, the oracle would keep telling hero "fold, villain has it" on delayed probes — exactly the leak the owner is trying to train out of himself.

- **T_E03/E04 multiway primary-villain:** Primary = donker (not preflop opener) is correct. Note: post-fix == pre-fix (baseline-selection test, no chain activity). Reasonable as a baseline-correctness probe; **does not exercise the v2.4 fix at all**, so these cases don't tell us anything about whether Stage 3.5 is working in multiway. That's a corpus gap, not a blueprint bug.

---

T_J01 SHIP CRITERION

The owner will accept the fix if the oracle panel for H_d9edab5d shows:
- Villain range composition line: ~50-60% TP+, ≤5% medium, ~35-45% air
- Oracle recommendation on decision (river facing bet): shifts from FOLD → CALL (or MIXED with CALL the primary action) because pot odds + ~40% bluff frequency beats hero's bluff-catcher equity
- Teaching narrative explicitly names "delayed probe" or "turn check-through polarises river range"

If post-fix number is 0.55/0.04/0.00/0.41 as §3.6 proposes but **the oracle still recommends FOLD**, the fix failed the ship test regardless of feature-level correctness. Practical check: the panel must change its verdict on this hand, not just its numbers.

---

DRY-RUN BATCH COVERAGE (Q21)

- **5-entry adequate: NO — needs 8-10 and must be shape-targeted, not random.**
- Five random fixtures will hit easy shapes (flop cbet-call patterns dominate FB-40). The dry-run must prove the chain fires on the *hard* cases, otherwise the go/no-go is meaningless.
- **Required shape coverage for dry run (8 entries):**
  1. One HU cbet-call flop (easy baseline, proves plumbing)
  2. One HU x/r-call line (MUST #11 collapse)
  3. One delayed probe (check-through + later bet, T_K05-shape — THIS IS THE OWNER'S HAND CLASS)
  4. One multiway 3-way flop with non-primary actors (T_E05-shape)
  5. One 3bet-pot flop (baseline shift, MUST #11 + B03 pattern)
  6. One turn x/r (T_B04-shape, the "strongest" class)
  7. One villain-folded mid-chain (T_I03-shape, MUST #10 NaN path)
  8. One triple-bet line (T_K03-shape, mass-floor stress)
- **Gate criterion:** chain_steps > 0 on all 8, composition matches hand-authored expectation within direction (not magnitude) on 8/8. If 7/8 or lower, the authoring logic needs review before scaling to 140.

---

SIDECAR AUTHORING REALISM

Required action-sequence patterns the FB-40 sidecar MUST represent (not just for T_J01):

- **Donk leads (flop and turn):** BB-donks-into-PFR — frequent amateur spot, currently invisible in most shape coverage. At least 4 FB entries should be donks.
- **Check-raise + turn barrel vs x/r + turn check:** two different continuation stories that lead to very different ranges. Both must be authored distinctly.
- **Delayed probe / double-barrel give-up:** flop-bet + turn-check + river-bet (T_K06 pattern). At least 3 FB entries.
- **Multi-street barrel with call-call-fold chain ending:** villain fires 3 streets — authored sequence must end with hero FOLD position (tests T_I03 path).
- **Squeeze preflop:** currently missing from FB-40 shape set per prior review; sidecar should include at least one SB-squeeze-BB-4bet-BTN-call construct.

Required patterns for reference-set sidecar (MW-11+):
- Cold-calls + squeeze dynamics with correct baseline range (NOT open-range)
- Multiway with SB-folds-BB-donks so primary-villain selection is exercised on real fixtures

**High-risk authoring categories:**
1. **Multiway hands where primary villain shifts between preflop and flop** — if authoring just lists BTN-open / BB-call / SB-call then flop donk from BB, GTO review must verify the range baseline used. Easy to author with wrong opener.
2. **Limped-pot lines** (if any exist in MW set) — "opener" semantics fuzzy; authoring must establish convention.
3. **All-in chip-action** — T_K08 notes chain must not misread all-in RAISE; sidecar entries must disambiguate.

---

CORPUS REALISM GAPS (from prior review)

- HU donk-lead coverage: **partial** — T_K01 has one turn donk; flop donk and river donk-lead (T_K03) exist. Still no BB-donks-flop-vs-SRP-cbet-opportunity-passed pattern.
- Squeeze preflop: **still gap**. Not addressed in v2 or supplement.
- Check-call-check-raise turn (float + x/r): **still gap**. T_B04 is bet-call / x/r turn, not a check-call / x/r-turn float.
- River overbet sizing distinction: **still gap**. T_K07 notes sizing not consumed by chain — so overbet vs pot-size vs half-pot are all collapsed. That's a v2.4 limitation; blueprint acknowledges it but doesn't fix.

All four are acceptable deferrals to v2.5 since v2.4 ships chain-inheritance correctness, not sizing sensitivity. **Flag for v2.5 backlog explicitly.**

---

MUST #6 PLAYER-VISIBLE CHANGES

- Oracle recommendation shifts on multistreet hands: **YES, visible**. On T_J01 the equity feature today uses open-range villain (~35% equity for hero bluff-catcher) → fold verdict. Post-fix equity reads against chained, polarised-on-river range (hero equity rises 8-12 points against a 41% air range) → call verdict. Same direction on T_K06.
- Player will notice: **YES obvious** on delayed-probe hands. The oracle changing its verdict on the owner's canonical hand is literally the reason for this project. On unchained hands (T_K02-style flop decisions) the player will not notice and should not.

---

NaN RENDER UX (MUST #10 teaching layer)

- **"blockers N/A" wording: better wording needed.** "N/A" is coder-speak; owner will read it and wonder why. Suggested: **"Villain folded earlier — no range to read."** This is how a pro narrates a folded-villain hand to a student.
- Cases wanting partial info even when folded: **NO** — once villain folded, there is no live range to reason about. Showing pre-fold blocker counts would actually mislead: hero cannot "remove" combos from a range that no longer matters. The correct teaching move is to redirect attention to the remaining live opponents (if multiway) or to pot-odds reasoning (if HU and villain folded = hero won, no decision). Blueprint's "skip the villain_* composition line entirely" is correct.
- One add: **when BOTH preflop actors fold and hero is HU with a remaining caller, the teaching panel should name the remaining live villain** so the player isn't confused which villain "folded." Small UX detail but matters in 4-way pots.

---

MUST #11 CHECK-CALL COLLAPSE — pro perspective

**Matches pro range thinking, with one nuance worth flagging.**

A pro reading "villain checked then called" thinks: villain has a call-down range — mediums, weak TP, some draws. The CHECK is passive noise; the CALL defines the range. Collapsing to call-only is correct.

**Nuance:** There IS informational content in "villain was FIRST TO ACT and chose CHECK rather than leading" — it rules out very strong hands who'd donk for value in some pools, and rules out some bluffs. For most GTO-reasonable ranges this is negligible, but in live-amateur pools where donk-leads are more common than solver suggests, the "villain didn't donk" signal has ~5-10% informational content. Blueprint's collapse approximates villain's range correctly on average and loses this ~5-10% nuance — acceptable trade for removing the medium-doubly-weighted bias. **Matches pro thinking at the precision this model operates at.**

---

OTHER PRACTICAL FINDINGS

1. **T_J01 is a shape, not just a test case.** The owner's H_d9edab5d is one instance of a class of hands (turn-check-through + river-bet). The SHIP-criterion should extend to at least 3 delayed-probe variants producing similar shifts. If only T_J01 is reauthored but T_K05/K06 still show old numbers, the fix will look inconsistent in the panel (owner will hit 3 similar hands and see different recommendations).

2. **Dry-run must include owner's personal hands if possible.** Is there a test-set entry traceable to H_d9edab5d or similar owner-history hand? If so, include in the 8-entry dry-run. If not, flag that owner verification at the end of the dry-run should replay his hand database through the updated oracle.

3. **Recommendation shift monitoring:** MUST #6's test plan checks "feature shift distribution" but not "verdict shift distribution." Add a check: post-fix, count how many hands in the MW-50 eval set change oracle verdict (fold→call, bet→check, etc). Expected: 8-15% verdict shifts on multistreet hands. If <3%, the fix didn't land. If >25%, something else is wrong.

4. **Terminology in teaching narrative:** If the panel uses the word "raise" for any first-postflop BET (which prior code has done), owner feedback_terminology_raise_vs_bet.md is violated. The CONTENT_API v4 change for NaN rendering is a good moment to audit all panel strings for raise/bet/open correctness.

5. **Solver-aligned sizing reminder:** When eventually fixing the river overbet gap (v2.5), sizing bins must match solver options (flop 25%/66%, turn 33%/75%, river 33%/75%/150%) per feedback_solver_aligned_sizing.md. Flag this early so the v2.5 blueprint doesn't invent its own sizing buckets.

Close the pass by endorsing: v2 + v2.1 solve the right problems at the right layer; T_J01 reauthor direction is correct; dry-run batch size should be lifted from 5 to ~8 shape-targeted cases; NaN wording should be player-facing English; delayed-probe shape class (K05/K06/J01) is the owner's ship criterion. Ship after these adjustments.
