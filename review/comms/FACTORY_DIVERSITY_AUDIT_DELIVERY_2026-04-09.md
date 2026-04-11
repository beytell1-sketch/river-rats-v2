# Delivery: Factory Diversity Audit
**Date:** 9 April 2026
**From:** GTO Expert
**To:** Owner / Factory Designer
**Status:** COMPLETE — awaiting owner review

---

## What was delivered

`river-rats-v2/review/FACTORY_DIVERSITY_AUDIT.md`

Full diversity audit of both existing factory batches (412 situations across 46 boards) plus concrete diversity requirements for the new 151-situation RAISE batch.

---

## Key findings (summary for owner)

**The most serious structural problem found is SPR uniformity in Batch 1.** 80 of 151 situations have SPR=1.11 — a value that almost never occurs in real 3-way flops at 100bb. This is caused by using pot=90 and effective_stack=100, which collapses all flop-board SPRs to 1.11. The model has seen SPR as a near-constant in over half its factory training data. The new batch must actively counter this.

**The OOP bias is real but less severe.** 65% of existing boards have OOP heroes. For a RAISE model where IP thin value and bluff raises are different decisions than OOP check-raises, this biases the training context. The new batch must run at least 55% IP.

**Monotone oversampling is at 11%, roughly 2x real-world frequency.** This is defensible for training purposes but should not increase further. Maximum 2 monotone flop boards in the new batch.

**Within-sub-pattern clustering is the core risk for the new batch.** If SP5 (28 situations) uses only 3–4 boards, all 28 situations will share 3–4 distinct values for villain_fold_equity_estimate, board_favour, and flush_danger. The model learns a point, not a decision boundary. The minimum-boards-per-sub-pattern requirement (7 for SP5, 7 for SP7, 5 for SP8) directly prevents this.

---

## Concrete requirements (what the factory designer must meet)

1. Minimum 25 unique boards, no reuse of any of the 46 existing boards.
2. Maximum 8 situations per board (prefer 6).
3. SPR must span 4 tiers: 1.0–2.0 (max 25%), 2.0–4.0 (min 30%), 4.0–8.0 (min 25%), 8.0+ (min 15%).
4. OOP heroes: at most 70 of 151 situations.
5. River situations: minimum 35.
6. SP5: minimum 7 boards; villain_fold_equity_estimate range >= 0.20 across sub-pattern.
7. SP7: minimum 7 boards; hero_range_percentile spanning 0.75–0.92; villain_fold_equity_estimate spanning 0.40–0.65.
8. SP8: minimum 5 river boards; all 16 situations must have street == 2.
9. Monotone flop boards: maximum 2.
10. All 14 reviewer checklist items in Section 5 of the audit must be documented at review time.

---

## Open questions for owner

None — the audit is based entirely on what is in the factory files. No assumptions were made that required owner input. The requirements in Section 3 are derived from the data, not from preferences.

One note: the SPR=1.11 problem in Batch 1 cannot be corrected retroactively without regenerating those situations. If the owner wants to address it, the options are: (a) accept it and counter with the new batch's SPR variance, (b) regenerate PA flop boards with realistic stack depths. Option (a) is recommended — the new batch can supply the SPR range that Batch 1 lacks, and regenerating Batch 1 would discard expert labels already applied.
