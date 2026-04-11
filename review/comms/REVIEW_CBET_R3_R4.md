# Independent Review: RESEARCH_CBET_R3_SIZING_SPR and RESEARCH_CBET_R4_CHECKBACK

**Reviewer:** Independent Reviewer
**Date:** 2026-04-09
**Files reviewed:**
- `review/RESEARCH_CBET_R3_SIZING_SPR.md`
- `review/RESEARCH_CBET_R4_CHECKBACK.md`
- `knowledge/three_way_gto.md` (existing KB, for cross-reference)

---

## Verdict: ISSUES FOUND

Both documents are substantively strong and represent genuine research value. Neither should be blocked. However, several issues require resolution or flagging before KB integration. Details below.

---

## 1. Source Count

**R3 (Sizing/SPR):** 12 sources listed in Section 6, all named specifically with URLs. Source count PASSES.

**R4 (Check-back):** 18 sources listed in Section 5, all named with author/publication/year. Source count PASSES.

---

## 2. Internal Consistency Between R3 and R4

### 2.1 SPR thresholds — alignment confirmed

R3 establishes that standard single-raised 3-way flop SPR at 100bb is approximately 8-12 (high zone), and that medium SPR (2-5) applies to turns in single-raised pots or flops in 3-bet pots. R4 does not explicitly cite SPR zones but its findings are consistent with this: the check-back framework describes flop behaviour (high SPR environment) as favouring pot control, trapping, and infrequent c-betting. No contradiction.

### 2.2 C-bet frequency figures — consistent

Both documents cite ~43% 3-way c-bet frequency and ~57% check frequency (GTO Wizard). These anchor numbers are consistent with the existing KB Section 1.3. No contradiction.

### 2.3 Trapping logic — partial tension, resolved by board texture

R3 states that at low SPR (< 2), trapping is almost never correct and strong hands should bet. R4 Finding 4 states that strong hands trap more 3-way than HU, with sets checking 30-50% frequency even IP. These are not contradictory — R3's low-SPR no-trap rule and R4's general trap-more-3-way rule operate in different SPR environments — but the documents do not cross-reference each other on this point. A reader moving between the two documents without careful reading could see these as conflicting.

**Issue (minor):** Neither document contains a forward reference to the other. R4's trap findings should note the low-SPR exception from R3, and R3's low-SPR no-trap rule should reference R4 for the general (high-SPR) case where trapping is more common.

### 2.4 MDF / fold equity math — consistent but inconsistent numbers

R3 Section Finding 6 calculates that at a 33% pot bet, each opponent must fold 86.7% for a bluff to break even (derived from the independence assumption: sqrt(1 - 0.248) ≈ 0.867). R4 Section 3 Step 1 states "at 33% pot bet: each opponent needs to fold ~25% of their range. Combined: 0.75 × 0.75 = ~56%. Marginal semi-bluffs can work."

**Issue (significant):** These two calculations are computing different things and will confuse a labelling agent reading both documents. R3 is asking "what individual fold rate do I need for a pure bluff to break even?" and arriving at 86.7%. R4 is computing the combined fold rate (0.75 × 0.75 = 56%) and comparing it to the alpha (breakeven fold %) of 24.8% — the question is whether the combined fold achieved (56%) exceeds what is needed (24.8%). R4's conclusion ("marginal semi-bluffs can work") is correct. R3's framing ("each opponent must fold 86.7%") is also technically correct but computed for a different question (required individual fold rate, not expected combined fold rate).

The practical conclusions are not in conflict — both documents agree that small-bet semi-bluffs are marginal-to-barely-viable and large-bet pure bluffs are losing. But the numerical framing will confuse anyone who reads both. This must be reconciled in the KB integration note or with a clarifying comment.

---

## 3. Contradictions with Existing KB

### 3.1 R4 Finding 1 vs KB Section 1.3 — minor framing difference

R4 Finding 1 states the c-bet frequency drops from ~54% HU to ~43% 3-way. KB Section 1.3 states "Overall c-bet frequency: ~54% HU, ~43% 3-way." Identical. No contradiction.

### 3.2 R4 Finding 4 on trapping vs KB Example 4 ("sets MUST bet multiway")

R4 explicitly identifies this tension and resolves it correctly: KB Example 4's board (Jd 8s 5c, semi-connected two-tone) is high-danger, triggering the protection requirement. R4's trap-with-sets finding applies to dry/static boards. R4 flags this as a gap (needs a dry-board set example) and calls the existing GDD example "correct but narrow."

**This is not a contradiction — it is correct analysis.** The KB example is not wrong; it is incomplete. R4's resolution is accurate and the gap it identifies (dry-board set checking example) is a valid KB improvement request.

### 3.3 R3 commitment threshold table vs KB Section 1.6

KB Section 1.6 notes that "same numeric SPR requires tighter stack-off thresholds multiway" but gives no thresholds. R3 Finding 5 provides a synthesised threshold table. R3 is clear this is a synthesis, not a direct solver output. No contradiction with the KB — R3 extends it.

**Issue (minor):** R3 should explicitly label the commitment threshold table as a working approximation pending solver verification, which it does in the gaps section (Gap 2). This is handled, but the table itself (Section 2, Finding 5) does not carry the "approximate" warning inline. Anyone who reads the table without reading the gaps section will take the numbers as harder than they are.

---

## 4. Unsourced Claims

### 4.1 R3 — synthesised commitment thresholds

The commitment threshold table (R3 Finding 5) contains exact numbers (e.g., "overpair commits at SPR < 2 in 3-way") that are explicitly flagged as derived from a principle ("tighter by one hand class") rather than direct solver output. The synthesis is acknowledged. Acceptable for now, but must not enter the KB without the approximation caveat.

### 4.2 R4 — check-fold frequency estimate "25-35%"

R4 Section 3, check-fold identification: "The PFA should check-fold 25-35% of their 3-way flop ranges on boards that hit opponents' ranges well." No source is cited for this number. R4's own Gap 1 acknowledges there is no solver-verified check-fold frequency by hand class. The 25-35% figure appears to be a plausible inference but is not sourced.

**Issue (significant):** The 25-35% check-fold rate is used in a normative statement ("the PFA SHOULD check-fold 25-35%") without a source. This must either be sourced, removed, or explicitly marked as estimated. A labelling agent treating this as a calibrated number could produce systematically over-aggressive check-folds.

### 4.3 R4 — specific OOP check frequencies (70-80%, 85-90%)

R4 Section 3 Step 4 states: "OOP monsters check at ~75-80%. OOP medium hands check at ~85-90%." R4 cites GTO Wizard solver data for AA checking back OOP at ~80% (Finding 4). The 85-90% figure for OOP medium hands does not have a direct citation in the findings. Finding 5 cites Clarke and GTO Wizard for strong/weak OOP check frequencies but the "85-90% for medium hands" number does not appear in any finding with a source.

**Issue (minor):** The specific 85-90% for OOP medium hands needs either a source citation or a label of "estimated."

### 4.4 R4 — IP PFA c-bet frequency "30-45%"

R4 Finding 6 cites GTO Wizard for "IP PFA c-bet frequency 3-way is ~30-45%." The KB and R3 cite ~43% aggregate. The 30% lower bound is not explained or sourced specifically. The aggregate 43% is plausible as the centre of a 30-45% range, but the range boundaries need justification or the figure should state "~43% (solver aggregate)."

**Issue (minor):** The 30-45% range overstates precision relative to available sources. The lower bound (30%) appears unsupported.

---

## 5. Actionable Implications for the BET Tree

Both documents produce clear, implementable guidance:

**From R3:**
- SPR must be a continuous feature, not a hard threshold gate.
- The standard 3-way single-raised flop exists at SPR 8-12 (high SPR zone) — "high SPR behaviour" is the DEFAULT, not an exception.
- Large bets (> 50% pot) should be near-zero probability outputs at SPR > 5.
- Sizing labels should scale with SPR: 50-75% (low SPR), 33-40% (medium), 25-33% (high), 20-25% (very high).
- SPR interacts with `danger_score`, `connectivity_score`, `is_monotone` — the model needs both features, not SPR alone.

**From R4:**
- The BET tree must model delayed c-bets as a primary turn line — a flop check is not a commitment to passivity.
- `danger_score` ≥ 0.5 overrides trap logic: strong hands bet for protection.
- `villain_aggression_count` is the primary moderator of trap vs bet decisions.
- The check-fold is the most common action for complete air in 3-way pots.
- OOP vs IP is a 10-15% frequency modifier on check decisions, not a binary rule.

These implications are concrete and consistent with the 45-feature pipeline design. They can be directly used in labelling agent reasoning and feature engineering.

---

## 6. Gaps

### Gaps flagged within the documents (well identified)

R3 correctly flags:
- No public solver output for c-bet frequency by SPR zone (only aggregate)
- 3-way commitment thresholds are synthesised approximations
- OOP c-bet frequency by SPR zone is not quantified
- Board texture × SPR interaction is qualitative, not tabular

R4 correctly flags:
- No solver-verified check-fold % by hand class
- Cold-caller cap effect on trap EV not quantified
- PFA check-raise frequency (floating trap line) is entirely absent

### Additional gaps this review identifies

**Gap A: No worked example of a low-SPR spot in either document.** R3's SPR zone framework is the most actionable contribution of the two documents. But there is no concrete hand example showing SPR < 2 bet-to-commit logic. The existing KB examples are all at standard single-raised flop SPR (high zone). A low-SPR worked example (turn or 3-bet-pot flop) would make the R3 framework concrete for the labelling agent.

**Gap B: R4 does not address the three-check scenario.** Finding 9 covers what happens after the PFA checks and both opponents check the flop. But it does not address: what if the PFA checks, one opponent bets, and the other folds? This reduces to a pseudo-HU spot mid-hand and the appropriate response is not covered.

**Gap C: R3 Section 3.1 Zone 3 correction is important but buried.** The document self-corrects mid-section, revealing that Zone 3 "medium SPR" (2-5) does not apply to standard flop spots at 100bb. This correction is critical and correct, but it is embedded in Zone 3's description rather than elevated to a standalone finding or highlighted in the summary table. Anyone who reads only the summary table (Section 1.3) will miscategorise the standard flop situation. Recommend this correction be promoted to the findings section.

---

## 7. KB Integration Readiness

| Item | Status | Action required |
|---|---|---|
| R3 SPR zone framework | Ready with caveats | Mark commitment threshold table as estimated; elevate the Zone 3 SPR correction |
| R3 DO NOT Rule #9 candidate | Ready | Add to KB |
| R3 SPR zones and c-bet sizing table (Section 5.3) | Ready with caveats | Add "estimated" qualifier to c-bet frequency column for non-aggregate SPR zones |
| R4 check-back decision framework (Steps 1-6) | Ready with caveats | Source or remove the 25-35% check-fold rate; source or mark the 85-90% OOP medium hand figure |
| R4 delayed c-bet section for KB | Ready | Add to KB as new section |
| R4 dry-board set check example | Needs to be written | Gap identified; not yet delivered |
| MDF math reconciliation between R3 and R4 | Required before KB integration | Align framing of the 33% pot bluff math |

---

## Summary

R3 is the stronger document. Its SPR zone framework is well-constructed, the self-correction on Zone 3 (standard flop SPR is high, not medium) is an important insight, and the gaps section is honest about where the data runs out. The commitment threshold table needs a clear "synthesised/approximate" warning promoted to be inline, not just in the gaps section.

R4 is substantively sound on the poker. The check-back decision framework and the delayed c-bet finding are directly useful. The unsourced 25-35% check-fold rate and the conflicting MDF math framing (relative to R3) are the two issues that need resolution before KB integration. The gap in covering the floating trap (PFA check-raise after voluntary check) is worth flagging as a future research item.

Neither document contradicts the existing KB. Both extend it. Integration can proceed after the specific issues above are addressed.

---

*Written to review/comms/ per protocol.*
