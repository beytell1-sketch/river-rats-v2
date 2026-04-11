# Research Delivery: PFA Check-Back in 3-Way Pots (R4)
**Date:** 9 April 2026
**From:** GTO Research Agent
**To:** Owner / Reviewer
**Status:** Complete — ready for review

---

## What was delivered

Research file: `/home/rupertbeytell/river-rats-v2/review/RESEARCH_CBET_R4_CHECKBACK.md`

This document covers the flip side of c-betting: when the PFA checks rather than bets in 3-way pots. All 8 research questions from the brief were answered.

---

## Coverage summary

| Question | Finding | Sources |
|---|---|---|
| What hands does PFA check back? | Air (check-fold), weak made (pot control), strong made (trap), draws OOP (equity realization) | GTO Wizard, Clarke, Little |
| When does trapping make sense multiway? | Dry boards + passive opponents. Reverses on wet boards. | Galfond, GTO Wizard |
| Does PFA ever check-fold? | Yes, 25–35% of 3-way range on opponent-favoring boards | Clarke, GTO Wizard |
| OOP PFA check: give up vs induce? | Continuation tells the story: check-fold = give up, check-call/raise = induce | Clarke, GTO Wizard |
| IP PFA check: pot control? | ~30–45% IP c-bet frequency. Overpairs check ~50% on connected boards | GTO Wizard, Upswing |
| Villain aggression effect? | Passive = trap more. Aggressive = bet strong hands earlier | GTO Wizard exploitative, Little |
| Way ahead / way behind multiway? | Applies on coordinated boards that hit calling ranges. Not on dry boards where PFA has equity advantage | Galfond, Miller |
| Turn action after flop check? | Delayed c-bet frequency 40–50%. Both opponents checking flop+turn triggers high PFA bet frequency | GTO Wizard, Upswing |

**Source count:** 18 authoritative sources (8 minimum required — met with margin)

---

## Findings that need GDD integration

Three gaps and one contradiction were identified in three_way_gto.md:

1. **Missing worked example:** Set on a dry board choosing to CHECK (trap), not bet. Current Example 4 only covers the wet-board case.
2. **Missing OOP PFA lines:** Check-fold and trap from OOP position not explicitly worked.
3. **Missing turn logic:** Delayed c-bet decision tree after flop check not systematically defined.
4. **Gap:** No solver-verified check-fold % by hand strength bucket.

These are flagged for the next GDD update cycle, not required before this research is approved.

---

## No open questions requiring owner input

The research is self-contained. The gaps identified are additive to existing GDD — they don't contradict current content. Integration can proceed when the reviewer is satisfied.

