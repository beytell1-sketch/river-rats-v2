# Independent Review: RESEARCH_CBET_R1_FREQUENCY.md and RESEARCH_CBET_R2_TEXTURE.md

**Reviewer:** Independent Reviewer
**Date:** 2026-04-09
**Files reviewed:**
- `review/RESEARCH_CBET_R1_FREQUENCY.md` (c-bet frequency, R1)
- `review/RESEARCH_CBET_R2_TEXTURE.md` (board texture effects, R2)
**KB reference:** `knowledge/three_way_gto.md` (v1.2)

---

## Verdict: PASS WITH MINOR ISSUES

Both documents are acceptable for integration. No blocking defects. Three specific issues
flagged below require either a KB amendment or a noted caveat before the findings are used
in the BET decision tree.

---

## 1. Source Count and Specificity

**R1:** 9 named sources. All meet the bar for specificity: author, outlet, article title or
chapter, year. GTO Wizard is cited multiple times but for distinct articles (aggregated
solver data vs blog posts vs lecture series) — this counts as a single primary source used
across multiple findings, not inflated padding. Total distinct primary source outlets: 6
(GTO Wizard, Acevedo/MPT, Upswing/Fee, Run It Once/Galfond, Solve For Why, Brokos/POP,
Little/PokerCoaching, Red Chip/Sweeney, PioSolver community/2+2). Meets the 8-source
threshold by named citation; all 9 are identified with enough specificity to verify.

**R2:** 18 sources listed with URLs. All are named with outlet, article title, and link.
Source quality is somewhat uneven (888poker and MyPokerCoaching are less authoritative
than GTO Wizard and Galfond) but both are used only to corroborate findings already
established by higher-authority sources. No finding rests solely on a low-authority source.
Comfortably exceeds the 8-source threshold.

**Issue 1 (minor): R1's GTO Wizard citations lack article-level URLs.** R2 provides full
URLs for all GTO Wizard articles; R1 cites "GTO Wizard blog, multiple articles 2022-2025"
without URLs. This is a traceability weakness. Not a blocking issue since the findings are
directionally confirmed by R2's more specifically cited GTO Wizard articles, but R1 should
add URLs on next revision.

---

## 2. Internal Consistency: R1 vs R2

The two documents are broadly consistent. Where they overlap on the same figures, they agree
directionally and are within range numerically:

| Data point | R1 figure | R2 figure | Consistent? |
|------------|-----------|-----------|-------------|
| A-high dry, IP PFA c-bet | 58-65% | 60-70% | Yes (ranges overlap) |
| Low connected, IP PFA c-bet | 22-30% | 20-30% | Yes |
| Monotone boards reduction vs rainbow | ~15-25pp implied | 15-25pp stated | Yes |
| Two-tone reduction vs rainbow | ~5-10pp implied | 5-10pp stated | Yes |
| Connected middling (T86, 976) | 22-30% | 30-40% (Tier 3) | Borderline — see Issue 2 |
| Overall 3-way average | 33-43% | ~43% aggregate | Yes |

**Issue 2 (substantive): Frequency disagreement on middle connected boards.**

R1's board texture table (Finding 6) cites IP PFA c-bet frequency of 22-30% on "connected
middling (T86, 976, 875)." R2's Tier 3 classification for the equivalent texture
("Mid-high connected rainbow") shows 25-40%. That overlap is thin: R1's upper bound (30%)
meets R2's lower bound (25%) but R2's upper bound (40%) is meaningfully above R1's range.

R2 also has a dedicated section (2.5) stating "~30-40%" for middle connected boards.
R1's 22-30% appears tighter. Neither document explains the discrepancy. The difference
likely reflects R1 treating T86/976 as relatively high-connectivity boards (connectivity
~0.75) while R2's Tier 3 spans a wider connectivity range (0.5-0.75) and so includes
some less connected mid boards that pull the range upward.

**Action required before BET tree coding:** The decision tree author must pick one range
or reconcile by sub-categorising (e.g., T86 at 22-30%; T84r at 30-40%). Using R2's
broader tier range in the tree while R1 implies a tighter figure will produce inconsistent
labelling if the two documents are used simultaneously as references. Recommend adopting
R2's tiered classification as the primary framework (it is more structured and sourced
at URL level) and annotating that R1's tighter figure applies to the higher-connectivity
end of Tier 3.

---

## 3. Contradictions with the Existing KB (three_way_gto.md v1.2)

### 3a. KB Section 1.3 — "IP c-bet frequency is still only 30-45%"

R1's Finding 3 (supported by R2) establishes that A-high dry boards produce IP PFA c-bet
frequencies of 58-65% (R1) or 60-70% (R2). The KB's Factor 2 caps the upper bound at
"30-45% even IP." This is a genuine contradiction on specific textures.

**Which is more authoritative?** R1 and R2 are more current (April 2026) and draw from
specific texture-stratified solver data. The KB's 30-45% is an overall average across
all textures, not a cap. The KB language is misleading — "IP c-bet frequency is still
only 30-45%" reads as a ceiling, not a cross-texture mean. The KB should be amended.

**Recommended KB amendment:** In Factor 2 (Position), change "IP c-bet frequency is still
only 30-45%" to "IP c-bet frequency averages 30-45% across all textures; on A/K-high dry
boards it reaches 55-70%, on low connected boards it falls to 20-30%."

This is the most important KB inconsistency found. It would cause a labelling agent
reading the KB to artificially cap IP PFA c-bet decisions at 45% on high-card dry boards,
which conflicts with solver-verified behaviour.

### 3b. KB Section 1.7 / Example 9 — Nut draw raise with blocker, no texture gate

R2 Section 4.1 (Contradiction 3) flags a gap: the KB states the nut draw + blocker raise
(MW-47 pattern) applies OOP without restricting to favorable textures. R2 argues that on
low connected two-tone boards, even a nut flush draw + blocker may have insufficient fold
equity to raise OOP. This is a refinement, not a flat contradiction, but it is a real gap.

The KB's Example 9 uses Ks-Jd-5s (two spades, high-card board) — a Tier 1 or Tier 2
texture in R2's framework. The raise is correctly solver-verified for that specific texture.
The problem is the KB presents it without an explicit texture gate, implying the pattern
generalizes to any board. On a 7s-6s-4c-type board OOP, the same hand (AsQs) may not
have sufficient fold equity to raise.

**Recommended KB amendment (minor):** Add a single-sentence qualifier to Section 1.7:
"This carve-out applies when the board texture is also favorable for the PFA (Tier 1 or
Tier 2 in R2's classification). On low connected boards, even nut draws with blockers
should check-call OOP."

### 3c. KB Section 1.3 — "Default sizing: Small (25-33% pot)"

R2 Section 4.1 (Contradiction 1) flags that A-high dry and A-K-x boards support 50-66%
sizing per poker.pro's solver data. The KB's default sizing guidance reads as universal.
Both R1 and R2 confirm the 25-33% default is correct for most boards but not for Tier 1
boards with clear nut advantage.

This was already self-flagged by R2; it is a framing issue rather than a factual error.
The KB should add a one-line exception clause to Section 1.3 sizing row: "Exception:
Tier 1 textures (A/K-high dry, clear nut advantage) support 40-50% pot."

---

## 4. Unsourced Claims Presented as Fact

**R1, Finding 8:** "The solver never produces 100% (or near-100%) c-bet strategies in
3-way configurations." This is stated as a universal fact but attributed to a bundle
("GTO Wizard, PioSolver community, Modern Poker Theory") rather than a specific data
point. The claim is directionally sound and consistent with everything else in the
research, but it is not precisely sourced. Flag as "accepted with caveat — not precisely
sourced" rather than treating it as a verified solver output.

**R2, Section 2.3:** The GTO Wizard source for paired boards notes "~96% noted for HU;
multiway 'still high'" without providing a specific multiway frequency. The 55-65% range
in R2's findings for paired boards 3-way is interpolated from directional language, not
from a stated solver figure. The range is plausible and internally consistent with the
framework but should be flagged as an estimate in the decision tree, not a solver output.

**R2, Section 2.7 (Straight danger gradient table):** R2 explicitly notes "These are
estimates derived from the direction and magnitude of findings across sources. No single
source provides a clean table." This is appropriately disclosed and does not constitute a
problem — but the decision tree author must treat this table as a directional guide only,
not precision solver output.

No major unsourced claims presented as fact without disclosure were found.

---

## 5. Actionability for the BET Decision Tree

Both documents are actionable. Specific assessments:

**R1** provides: position-split frequency estimates (IP vs OOP PFA), a board texture
table with numeric ranges, donk-bet trigger conditions with frequency estimates, cold-
caller probe frequency ranges, and a three-gate decision structure (texture → position →
hand class). All of these can be translated directly to decision tree logic.

**R2** provides: a four-tier texture classification system with explicit feature mappings
(top_card, flush_danger, straight_danger, board_paired) and a priority-ordered decision
logic summary (Section 3, Decision Logic Summary). This is the more directly actionable
of the two documents for the BET tree because it maps explicitly to named pipeline
features.

The combined framework is: R2's tier system gates the primary c-bet probability; R1's
position split applies the secondary modifier; R1's hand class section determines sizing.
This is coherent and implementable.

**One gap for the coder:** Neither document specifies how to handle the donk-bet and
cold-caller probe nodes in the decision tree's action history context. R1 describes the
frequency and trigger conditions for these actions but does not specify what features in
the existing 45-feature pipeline encode them (e.g., is "cold-caller probe" detectable
from the current feature set, or does it require a new feature?). The decision tree author
should verify that `facing_bet` + `villain_range_capped = 1` is sufficient to distinguish
a cold-caller probe from a BB donk-bet, or flag this as a feature gap.

---

## 6. Gaps Not Covered That Should Have Been

Both documents self-flag their gaps honestly. The review confirms these are the real gaps:

1. **OOP PFA texture-specific frequencies:** R2 explicitly flags this (Gap 5). R1 provides
   directional estimates (25-30% OOP average) but no OOP-by-texture table. The BET tree
   needs this to avoid applying IP figures to OOP situations.

2. **3-bet pot texture effects:** Both documents scope to SRP only. If the model encounters
   3-way 3-bet pots, neither document applies. The existing KB references AA checking 80%
   OOP in 3-bet pots (Example 6) but does not provide a texture-stratified treatment.

3. **Stack depth sensitivity:** R1 flags this (Gap 4). Not covered in R2 either.

One gap neither document addresses and neither self-flags: **the interaction between
board texture and the cold-caller's specific position (BTN vs SB vs CO).** R1 and R2
treat the cold-caller as a generic "BTN flat." In configurations where the cold-caller is
the SB or CO, their range shape differs and the texture interaction changes. This is a
second-order concern but relevant for non-standard 3-way configurations.

---

## Summary of Required Actions Before Integration

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | KB Section 1.3 Factor 2 caps IP c-bet at 45% — contradicts R1/R2 | Moderate | Amend KB Section 1.3 and Factor 2 language before labelling runs |
| 2 | KB Section 1.7 MW-47 pattern has no texture gate | Minor | Add one-line qualifier to Section 1.7 |
| 3 | KB Section 1.3 sizing default has no exception clause | Minor | Add exception for Tier 1 boards |
| 4 | R1/R2 frequency disagreement on middle connected boards | Minor | Decision tree author must pick one range; recommend R2 Tier 3 with R1 figure at upper end |
| 5 | R1 GTO Wizard citations lack URLs | Minor | R1 next revision should add URLs |
| 6 | Donk-bet / probe-bet node feature mapping not specified | Minor | Coder must verify feature coverage or flag as feature gap before implementing |

Items 1-3 require KB amendments before these research findings are used in labelling.
Items 4-6 are pre-implementation decisions for the coder, not blockers to KB integration.

---

*Review complete. Reviewer confirms this document has been written to review/comms/ as required.*
