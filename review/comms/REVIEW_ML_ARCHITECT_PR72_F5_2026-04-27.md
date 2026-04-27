---
from: ml-architect (PR #72 F5 reviewer)
date: 2026-04-27
pr: 72
branch: programmer/allocator-rare-cat-first-2026-04-27
head: 31e0a84
verdict: APPROVE-WITH-NITS
---

# PR #72 F5 Review — rare-category-first allocator (fixes MAGG=0/40 bug)

Review scope: algorithm correctness, empirical verification (C2 run), test coverage,
TC-26 V-Integration-Trace. Per directive (master 43a80bb) and memory
feedback_verify_source_not_plan.md: source read and C2 command executed independently.

---

## 1. Algorithm correctness

### Implementation vs spec match

The directive's algorithm spec and the implementation at `scripts/build_corpus_revision_500_hand.py`
lines 372-476 match precisely. The five-step algorithm is correct:

**Step 1 — Multi-membership classification.** `_classify_record()` (lines 335-369) returns
the full set of Phase A categories a record satisfies. A MAGG+PFA+spr_std record correctly
gets `{'magg', 'pfa', 'spr_std'}`. NFD sub-categories (boundary / raise / call) are correctly
mutually exclusive within that group (boundary wins if `_validate_nfd_boundary` passes, then
raise/call on the air threshold split). All other categories are additive.

**Step 2 — Yield counting.** `yield_per_cat` counts all records satisfying each category
(before deduplication). This is the right definition for scarcity: maximum potential yield,
not unique-assignment yield. Correct.

**Step 3 — Scarcity.** `scarcity[cat] = PHASE_A_QUOTAS[cat] / max(1, yield_per_cat[cat])`.
The `max(1, ...)` guard prevents division by zero when a category has zero pool records.
Correct.

**Step 4 — Sort.** Records sorted descending by their max-scarcity matching category
(`-max(scarcity[c] for c in cats), default=0`). Zero-category records get `default=0` which
maps to priority `-0.0`. Because the algorithm then checks `if not cats: continue`, they are
harmlessly skipped. Verified: empty pool, zero-cat records, single-cat records all handled
without errors.

**Step 5 — Assignment.** For each record (sorted rarest-first), find the highest-scarcity
category that still has unfilled target. `max(eligible, key=lambda c: scarcity[c])`. Correct.
On scarcity tie, `max()` over a set is non-deterministic across Python runs but the pre-shuffle
(seeded RNG) ensures reproducible outputs given the same seed. Tie-breaking is a cosmetic
concern only, not a correctness issue.

**Pre-shuffle.** The pool is shuffled by the seeded RNG before classification, giving
deterministic tie-break resolution. Two runs with the same seed produce identical outputs.
Confirmed empirically.

### Root-cause fix verified

The bug: all 10 MAGG records in the pool also satisfy `is_preflop_aggressor=1` (PFA),
because MAGG template construction uses BB-as-villain with hero as preflop opener. In the
old FCFS allocator, the PFA bucket was filled first (up to quota 80), consuming all 10 MAGG
records. MAGG quota then found zero eligible records.

With the rare-category-first allocator: MAGG scarcity = 40/10 = 4.0 >> PFA scarcity = 80/46
= 1.74. MAGG+PFA records sort to the front. They are assigned to MAGG (highest-scarcity
eligible category). PFA records that satisfy only PFA are assigned to PFA. The 10 MAGG
records now correctly land in the MAGG Phase A bucket.

### Edge cases confirmed

- **Empty pool:** Returns `([], set())`. No error.
- **Zero-category record (spr < 2.0, no other qualifier):** `_classify_record` returns empty
  set; `default=0` in sort key; `if not cats: continue` skips it. Not selected. Correct.
- **Single-category records:** Assigned to their one matching category (if quota not filled).
- **Scarcity tie:** `max()` picks one without error. Pre-shuffle ensures determinism.
- **All-duplicate fingerprints:** Only one record selected per unique fingerprint.
- **Forbidden fingerprints passed in:** Records with fps in `forbidden_fps` are skipped at
  assignment time (line 447-449). Verified: single-record pool with its own fp in forbidden
  returns zero selected.

### Minor design note (NIT-1)

In the scarcity tie situation (two categories with identical scarcity), the allocator picks
whichever `max()` returns from the set's iteration order, which is not guaranteed stable
across Python versions or runs without the pre-shuffle. The pre-shuffle handles this for the
sorted records list, but the `max(eligible, ...)` call inside the assignment loop is still
non-deterministic if multiple eligible categories have equal scarcity. This is a theoretical
concern only: with the seeded pre-shuffle, the pool order entering the assignment loop is
deterministic, and in practice category scarcities rarely tie. No code change required, but
worth noting for future robustness.

---

## 2. Empirical verification — C2 command run

The directive specified:

```
python3 scripts/build_corpus_revision_500_hand.py \
  --pool data/corpus_revision_pool_combined_2026-04-27.jsonl \
  --existing-corpus data/pilot_corpus_100_hand_2026-04-26_v2.jsonl \
  --target-new 400 --seed 20260427 \
  --output /tmp/c2_test.jsonl --lock-output /tmp/c2_test.lock
```

Run independently using:
- PR #72 script: `git checkout origin/programmer/allocator-rare-cat-first-2026-04-27 -- scripts/`
- Pool data from PR #70 branch (head 174bbc3): `git checkout origin/programmer/corpus-revision-execution-2026-04-27 -- data/`

Pool confirmed: 327 records, 10 MAGG records, all 10 MAGG records also have
`is_preflop_aggressor=1` (the documented root cause of the bug).

### Phase A output (new allocator)

```
PFA c-bet (Rule 4):           36/80  UNDER (yield 46)
NFD RAISE (air >= 0.20):       4/20  UNDER (yield 4)
NFD CALL (air < 0.20):         4/20  UNDER (yield 4)
NFD boundary cases:            6/10  UNDER (yield 6)
BAC (MW-30 callers >= 1):      5/20  UNDER (yield 9)
Monster facing bet (MW-33):   20/20  FULL
MAGG river (villain_agg >= 2):10/40  UNDER (yield 10)   <-- FIXED from 0
Standard SPR (4-8):           50/50  FULL
Medium SPR (2-4):             16/40  UNDER (yield 18)
Rule 11 boundary:             10/10  FULL                <-- improved from 8
Donk-bet defence (Module 8):   4/25  UNDER (yield 15)
SB-hero sandwich (Module 9):   8/20  UNDER (yield 13)
Total Phase A:               173/355
```

**MAGG confirmed: 10/40 with yield 10. Fixed from 0/40.**

The old greedy allocator was also run with `scripts/build_corpus_revision_500_hand.py` from
master for direct comparison. SHA256 of old output:
`3f0ed144a7a79c53d3c095e905be7aad94e864e04f77c64a16f1d678da0bdec6` — matches the builder's
Phase 3 v2 report exactly. Reproducibility confirmed.

### Explaining the Phase A display changes (PFA/donk "regressions")

The builder describes PFA dropping from 46 to 36, and donk dropping from 3 to 4 in Phase A
(but then notes donk as a regression of -11). These numbers refer to Phase A bucket tracking,
not corpus totals.

The **structural verification** (which counts the actual combined corpus) shows identical
donk=15 and PFA=94 in both old and new outputs. The same records are present; they are just
tracked under different Phase A quota buckets in the new allocator. This is correct and
expected behavior:

- 10 MAGG+PFA records that were counted under PFA in the old allocator are now counted under
  MAGG. PFA Phase A bucket drops by 10 (46 -> 36). PFA corpus count is unchanged.
- 8 donk+PFA records (with PFA scarcity 1.74 > donk scarcity 1.67) are correctly assigned
  to PFA, not donk. So donk Phase A bucket shows only the 4 donk-only / donk+spr_std records.
  Donk corpus count remains 15 (the remaining 11 come through Phase B).
- 3 donk+spr_med records are assigned to spr_med (scarcity 2.22 > donk 1.67).

These are not regressions. The new allocator correctly classifies by actual pool scarcity.
The Phase A bucket counts now accurately reflect which categories are genuinely under-yield
vs. which were being phantom-filled at the expense of rarer categories.

### Important clarification on builder's empirical claim

The builder states "MAGG=0 → MAGG=10". This refers to Phase A bucket tracking. However, the
structural verification (which counts the combined output corpus) showed 10 MAGG records in
BOTH the old and new outputs. The old allocator included the 10 MAGG records via the PFA
bucket; they were present in the corpus but miscounted as PFA fills.

The real value of the fix is not that MAGG records are newly added to the corpus, but that:
1. They are now correctly tracked as MAGG-quota fills (enabling accurate Phase 5 decisions)
2. Phase A quota reporting now shows true pool yield shortfalls (yield 10 vs target 40)
3. Rule 11 improved from 8 to 10 (FULL) because its 2 records were previously consumed
   by earlier categories
4. Total Phase A selected improves from 168 to 173 (+5 hands more efficiently allocated)

The builder's claim is not wrong, but the fuller picture is: the Phase A MAGG tracker now
correctly reports the yield reality, unmasking genuine pool shortfall for Phase 5.

---

## 3. Test coverage

### Test count

- Master branch: 47 passed + 3 skipped (50 total collected)
- PR branch: 52 passed + 3 skipped (55 total collected)
- New tests added: 5 (the directive predicted 4, builder delivered 5)

### TestRareCategoryFirstAllocator — 5 tests

All 5 pass. Coverage:

**`test_targets_dict_matches_phase_a_quotas`** — Structural. Asserts `PHASE_A_QUOTAS` matches
the canonical 12-category dict and sums to 355. Correctly uses `PHASE_A_QUOTAS` as the
single source of truth (the implementation uses the same constant). Pass.

**`test_magg_records_assigned_to_magg_not_pfa`** — Regression test for the cited bug.
Synthetic pool: 10 MAGG+PFA records + 100 PFA-only records. Old greedy: MAGG scarcity
40/110=0.36 < PFA scarcity 80/110=0.73 under naive yield counting, so PFA gets them.
New allocator: MAGG scarcity 40/10=4.0 >> PFA scarcity 80/110=0.73, so MAGG gets them.
Assert `len(magg_in_selected) >= 10`. Pass. This is the primary regression test.

**`test_scarcity_ordering`** — 5 MAGG-only records + 100 PFA-only records. MAGG scarcity
40/5=8.0 >> PFA scarcity 80/100=0.8. Asserts all 5 MAGG records assigned (rare-cat fills
first). Pass.

**`test_no_fingerprint_dupes_after_assignment`** — Mixed pool of 50 records. Asserts
`Counter(fps)` has no duplicates. Pass.

**`test_classify_record_membership_correctness`** — Unit test for `_classify_record`. Tests
multi-membership for MAGG+PFA+spr_std record, and NFD sub-category routing for an NFD+high-air
record. Pass.

### Coverage gaps (NIT-2)

The following cases are not explicitly covered by the new tests, though they are defensively
handled in code:

1. **Zero-category record in a mixed pool.** No test asserts that records with `spr < 2.0`
   and no other qualifying features are silently dropped (not selected, not crashing). The
   behavior is correct (verified above) but untested.

2. **Forbidden fingerprint exclusion.** No test passes a non-empty `forbidden_fps` set and
   asserts that matching records are excluded from Phase A output. The existing
   `test_no_fingerprint_dupes_after_assignment` passes an empty set.

3. **Pool where a category has zero yield.** When `yield_per_cat[cat] = 0` for some category,
   `scarcity[cat] = target / max(1, 0) = target`. The guard works, but no test exercises this
   path. Low risk; defensive coverage only.

4. **PHASE_A_QUOTAS sum is also tested** in `test_targets_dict_matches_phase_a_quotas` but
   there is no test asserting that the `_PHASE_A_LABELS` dict has the same 12 keys (cosmetic,
   not functional).

None of these gaps affect the fix's correctness. NIT severity only.

---

## 4. TC-26 V-Integration-Trace for F5

Demonstrating the fix path from input boundary to consumer:

**Input boundary (pool of 327 records, MAGG fingerprint set):**
- 10 records satisfying `villain_aggression_count >= 2` and `street == 'river'`
- All 10 also satisfy `is_preflop_aggressor == 1` (the multi-membership that caused the bug)
- `forbidden_fps` loaded from pilot corpus and calibration sets (170 fingerprints)
- None of the 10 MAGG records are in the forbidden set (confirmed: all 10 eligible)

**Through the fix — rare-category-first assignment:**
- Step 1: `_classify_record` classifies each MAGG record as `{'magg', 'pfa', 'spr_std'}`
- Step 2: `yield_per_cat['magg'] = 10`, `yield_per_cat['pfa'] = 46`, `yield_per_cat['spr_std'] = 301`
- Step 3: `scarcity['magg'] = 40/10 = 4.0`, `scarcity['pfa'] = 80/46 = 1.74`, `scarcity['spr_std'] = 50/301 = 0.17`
- Step 4: MAGG records sorted first (max scarcity = 4.0); PFA-only records sorted later (max = 1.74); spr_std-only last
- Step 5: MAGG records processed first. `eligible = {'magg', 'pfa', 'spr_std'}`. `best_cat = 'magg'` (scarcity 4.0). Assigned to `selected_per_cat['magg']`.

**Output — MAGG fingerprints land in MAGG quota:**
- Phase A output: `MAGG river (villain_agg >= 2): 10/40 UNDER (yield 10)`
- `selected_per_cat['magg']` contains all 10 MAGG records
- All 10 MAGG fingerprints are in `used_fps` after Phase A
- Phase B cannot pick them again (confirmed: `remaining_magg = 0` after Phase A)
- Combined corpus structural verify: `magg_villain_agg2 >= 20 — got 10` (WARN, as expected: genuine yield shortfall for Phase 5)

**Fix value reaches consumer (Phase 5 decision gate):**
- The Phase A MAGG yield report (`UNDER (yield 10)`) is now an accurate signal
- Phase 5 will correctly identify MAGG as requiring module expansion (10 records vs 40 target)
- Old allocator's MAGG=0 was a false signal (records were in corpus but miscounted as PFA)
- New allocator's MAGG=10 is the true signal: MAGG records correctly categorized, genuine shortage exposed

---

## 5. Nits

**NIT-1 (low).** Scarcity tie-breaking within `max(eligible, ...)` is set-iteration
non-deterministic if two categories have equal scarcity. The seeded pre-shuffle makes outcomes
reproducible in practice but the guarantee is implicit. A comment noting this would clarify
intent.

**NIT-2 (low).** Test coverage gaps: no test for zero-category records in mixed pool, no test
passing a non-empty `forbidden_fps`, no test for zero-yield categories. All handled correctly
in code; missing only test coverage.

**NIT-3 (informational).** Builder's commit message reports "48 passed + 7 skipped (was
43+7)". Actual measured counts are 52 passed + 3 skipped (was 47+3). The discrepancy
reflects a stale prior count in the builder's report. All 5 new tests pass; all 47 prior
tests remain passing. Not a code defect.

**NIT-4 (informational).** The "donk regression" surfaced in Phase A display (4/25 vs old 3/25
in Phase A; but also vs old structural verify showing 15) is expected behavior. Eight of the 15
donk records have PFA co-membership; PFA scarcity (1.74) exceeds donk scarcity (1.67), so they
correctly go to PFA. Three donk records have spr_med co-membership; spr_med scarcity (2.22)
exceeds donk, so they go to spr_med. The four remaining donk records (donk+spr_std) go to donk.
All 15 donk records end up in the combined corpus (4 via Phase A donk bucket, 11 via Phase B or
PFA/spr_med buckets). The builder's description of this as "expected redistribution" is correct.

---

## Verdict

**APPROVE-WITH-NITS.**

The algorithm matches the directive spec exactly. Root cause (MAGG records consumed by PFA
in FCFS order) is fixed. MAGG Phase A tracking correctly reports 10/40 (yield 10) after the
fix. Empirical verification independently confirms the fix. All 47 prior tests pass; all 5 new
tests pass. Edge cases (empty pool, zero-category records, forbidden fps, duplicate fps) handled
correctly. TC-26 V-Integration-Trace is clean: MAGG fingerprints flow from input boundary
through the rare-cat-first assignment into the MAGG quota bucket, with zero leakage to Phase B.

Nits are all low severity. None require code changes before merge.

**Phase 5 signal after this fix:** MAGG genuinely needs module expansion (yield 10, target 40).
PFA also under-yield (yield 46, target 80). These are real pool shortfalls, not allocator
artifacts. Phase 5 directive should target these categories.
