# Research Quality Review

**Reviewer:** Independent (Claude)
**Date:** 6 April 2026
**Files reviewed:** semi_bluff_multiway_research.md, blocker_effects_research.md, draw_play_multiway_research.md
**KB version:** three_way_gto.md v1.2

---

## 1. Source Quality

All three files cite GTO Wizard (solver-backed), Upswing Poker (solver-supported coaching), Phil Galfond, PioSolver docs, and arXiv papers. These are the gold standard for GTO poker research. One minor flag: **hhDealer.com** (semi-bluff file, Section 10) is a hand-history tool blog, not a peer-reviewed or solver-backed source. Its "33-37% bluff success rate" claim is vague and unverifiable. Low risk but worth noting. **Poker.pro** (semi-bluff file, Section 5) is similarly thin -- an aggregator site, not a primary source. The claims it makes are plausible but should be verified against GTO Wizard directly.

**Verdict:** 90%+ of citations are strong. Two marginal sources, neither load-bearing.

## 2. Cross-File Contradictions

**No material contradictions found.** The files are consistent on:
- C-bet frequency drops (18% to 1.3% large sizing) -- cited identically across all three
- NFD betting at ~69% HU (not pure bet) -- consistent between semi-bluff and draw files
- Small sizing default multiway -- unanimous
- Blocker importance amplified multiway -- consistent

One **apparent tension**: the draw file says NFD betting frequency is "50-70% depending on board" while the semi-bluff file pins it at 69% on a specific board. These are compatible (69% falls within 50-70%).

## 3. Contradictions With Knowledge Base v1.2

**No contradictions.** The KB's Section 1.7 (semi-bluff conditions), Section 1.8 (blocker action selection), and DO NOT Rule #6 all align with the research. The KB's 40pp blocker swing claim (AT diamond vs non-diamond) is explicitly validated by the blocker research file. The KB's "1:4 bluff-to-value ratio 3-way" is described as "estimated/derived" -- the research files don't contradict this but also don't provide a direct source. **Flag this as an unsourced KB claim.**

## 4. Missing Citations

- **Draw file, Section 7 decision matrix:** Marked "Synthesized from" multiple sources. The out thresholds (4 = fold, 8 = call, 12 = raise) are reasonable heuristics but no single solver output is cited for the combined table. This is the most dangerous unsourced item -- it will directly drive training labels.
- **Semi-bluff file, summary table:** "3-Way Value" column has multiple "Lower (unspecified)" entries. If the HU numbers are sourced but the 3-way adjustments are guesses, say so explicitly.
- **Blocker file, Section Synthesis Q1:** "Estimated range from literature: 20-50pp swings" -- this range is the author's inference, not a cited finding. Acceptable as synthesis but should be flagged.

## 5. The Ace Blocker Paradox

**These are NOT contradictory. They describe different streets and different decisions.**

- **Semi-bluff file (Section 4):** "Ace of flush suit blocks opponent's FOLDING hands (busted flush draws), making it a worse bluffing card." This applies on the **RIVER when the flush MISSED**. Villain's busted flush draws would fold -- but you hold the Ace of that suit, so fewer of those busted draws exist. Fewer folds = worse bluff.

- **Blocker file (Synthesis):** "Ace blocker is maximum impact for raising." This applies on the **FLOP/TURN when the flush draw is LIVE**. The As blocks villain's nut flush draw combos in their CONTINUING range, meaning fewer strong hands will call or re-raise your semi-bluff. More folds from value hands = better semi-bluff.

**Rule:** Ace of flush suit is BEST for semi-bluff raising on early streets (blocks villain's strong continues). It is WORST for river bluffing when the flush bricked (blocks villain's folding range). The KB's Example 9 (AsQs raising flop) and the semi-bluff file's Rule 5 (Ace-high flush draws worse as river bluffs) are both correct for their respective streets.

## 6. Actionable vs Theoretical

**Directly actionable for board design:**
- Out-threshold decision matrix (draw file Section 7) -- concrete, board-ready
- "Never semi-bluff" hand classes (semi-bluff file Section 8) -- clear exclusion rules
- Sizing defaults (25-40% pot multiway) -- implementable
- NFD check-back rate (~31%) -- usable frequency target

**Too vague to act on:**
- "Blockers become more important multiway" -- true but needs per-hand operationalization
- "CFR doesn't converge 3+ players" -- important caveat but doesn't change any specific label
- hhDealer's "33-37% bluff success rate" -- too generic to inform any specific situation

## 7. Overall Assessment

**This research is sufficient to proceed, with two caveats:**

1. The synthesized out-threshold table (draw file Section 7) needs solver spot-checks before it drives 260 labels. It is the single most influential artifact and the least directly sourced.

2. The street-specific nature of the Ace blocker effect must be explicitly encoded in the labelling agent's reasoning. If the agent sees "Ace blocker = good" without the street qualifier, it will mislabel river bluff spots.

The research is thorough, internally consistent, and well-sourced from legitimate authorities. It is strong enough to base training data design on, provided the two items above are addressed.
