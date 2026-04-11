# Delivery: Fixed Stack Training Research

**Date:** 9 April 2026
**From:** GTO Research Expert
**To:** Owner / Process Reviewer
**Status:** COMPLETE — awaiting owner review

---

## What was delivered

`river-rats-v2/review/RESEARCH_FIXED_STACK_TRAINING.md`

Full research report on whether "fixed stack depth first, then vary" is a recognized methodology in GTO solver work, poker AI, and ML curriculum learning.

---

## Headline findings (5-point summary for owner)

**1. Not a recognized methodology in solver work.**
PioSolver, GTO Wizard, and MonkerSolver do not use a "master one depth, then generalize" approach. Each tree is solved at a specific stack depth as a standalone computation. There is no cross-depth warm-start or staged-depth training in any production solver.

**2. Not recommended by any major training platform.**
GTO Wizard, Upswing, Run It Once, and Solve For Why all present postflop spots at mixed stack depths within the same training category. No major platform uses fixed-stack-first as a curriculum for postflop GTO decisions.

**3. The HU → multiway analogy does not hold for SPR.**
The owner's intuition is correct for topology changes (HU vs multiway are structurally different problems). SPR is not a topology change — it is a continuous parameter within the same 3-way postflop structure. Fixed-SPR training is not the postflop equivalent of HU-first training. The analogy breaks on the key structural dimension: HU training transfers to multiway because range-thinking is common to both; SPR=1.11 training does not transfer cleanly to SPR=8.0 because the dominant decision features are different at those depths.

**4. The model cannot learn SPR as a feature from near-constant training data.**
SPR is feature 57 (one of 52). For it to be a learnable discriminator, it must take varied values in training data paired with different optimal decisions. At SPR=1.11 in 53% of Batch 1, the gradient for SPR as an independent feature signal is near-zero.

**5. The counter-argument has one legitimate component.**
The consistency argument is real: introducing varied SPR in the new batch creates a bimodal SPR distribution in the combined training set (SPR ~1.11 from existing batches, SPR 4–12 from the new batch). This is a training design problem, not a data design problem. The ML architect should be briefed on this before designing the v3.1 training config.

---

## Recommendation on the three options

| Option | Assessment |
|--------|-----------|
| (a) Keep 100bb fixed | Not recommended. No methodological support. Perpetuates a known data problem. |
| (b) Vary SPR per R3 requirements | Technically correct. Requires ML architect to handle bimodal distribution at training time. |
| (c) Hybrid | R3 already implements a hybrid: some low-SPR situations (continuity with existing data) plus 75%+ at higher SPRs. Option (c) is Option (b) correctly specified. |

**R3 as written in the diversity audit should stand.** The factory designer should implement it. The ML architect should receive an explicit brief on the bimodal SPR issue before designing the training config.

---

## Process compliance

| Rule | Status |
|------|--------|
| §3.1 Research before design | Yes — research delivered before factory design begins |
| §3.2 Sources | 10 distinct sources cited (solvers, training platforms, academic papers, internal audit) |
| §1.4 Expert recommends | Yes — clear recommendation made, options not presented as equal choices |
| §4.1 Present for review | Yes — in review/ folder, comms delivery confirmed here |

---

## What this research does NOT decide

- How the ML architect should handle bimodal SPR at training time (normalization, sample weights, SHAP audit) — that is a training design question
- Whether Batch 1 PA boards should be regenerated with realistic SPRs — remains an owner decision

Both questions are flagged in Section 7 of the research document.

