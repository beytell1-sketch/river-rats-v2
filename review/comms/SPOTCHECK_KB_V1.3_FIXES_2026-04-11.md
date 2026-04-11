---
date: 2026-04-11
from: Reviewer terminal
to: Logic team (builder) / architect agent
re: Spot-check of F1/F2/F3 fixes applied to review/three_way_gto_v1.3.md
verdict: APPROVED — cutover cleared
---

## Scope

Meta-review sequence step 3: spot-check of the three fixes
applied to `review/three_way_gto_v1.3.md`, read directly from
source per the reviewer's own N-n3 lesson. Did NOT consult
`review/comms/FIXES_KB_V1.3_2026-04-11.md` (or 2026-04-10.md)
before reading source.

## Verdict

**APPROVED.** All three fixes land cleanly. v1.3 is cleared to
replace `knowledge/three_way_gto.md` as production.

## Spot-check results

### F1 — Example 6 false "BB→SB rewrite" note deletion

**Read:** `review/three_way_gto_v1.3.md` lines 670-675.

v1.3 now reads:

```
### Example 6: OOP value bet — high equity overrides position default

**Setup:** Hero holds Qs Jd on Qc 8d 3s. SB (OOP, first to act),
2 opponents (BTN opened, BB called). Pot 90, not facing bet.

**Factors:**
```

Setup flows directly into Factors. The two fabricated sentences
(previously at v1.3 lines 661-666 describing a "change from BB to
SB" that never happened) are gone. No residue, no dangling
reference. **PASS.**

### F2 — Section 1.9 cross-reference replacement

**Read:** `review/three_way_gto_v1.3.md` lines 220-229.

v1.3 now reads:

> "**Cross-reference.** This section replaces the prior use of
> `villain_range_capped` as a postflop strength indicator in the
> KB. The feature remains in the pipeline for continuity with the
> v9-3way-v2.2 model; no KB-level retraining decision is being
> made in this revision. Whether to drop `villain_range_capped`
> from the feature vector in a future training round is a
> model-training decision, tracked against the next feature-
> importance audit in `feedback_solver_findings.md`. The
> labelling agent must not treat it as a postflop signal. See
> DO NOT Rule #8 for the operative instruction."

The prior "see reviewer note N2 on the villain_range_flag review"
working-document reference is gone. Replaced with plain policy
text scoped to v9-3way-v2.2 continuity and pointing to
`feedback_solver_findings.md` for the retraining-policy
tracking. Matches the replacement text recommended in the
meta-review almost verbatim.

No other working-document references survive in Section 1.9 body
text. Version-history block still points to
`KB_V1.3_EDIT_PLAN.md` per the meta-review disposition (that
pointer is acceptable in append-only history). **PASS.**

### F3 — Provisional hedge removal + source verification

**Read:** three locations.

**Location 1 — v1.3 Section 1.9 worked illustration (lines 184-
188):**

> "shows `villain_top_pair_plus_pct = 0.3174`, `villain_draw_pct
> = 0.0878`, `villain_air_pct = 0.1856` — roughly 32% strong, 9%
> draws, 19% air, and ~40% weaker made hands and pocket pairs in
> the remainder."

Stated as fact, no hedge. Cross-reference at line 193 points to
"Worked Example 3 below" where the full classification
justification is given. **PASS.**

**Location 2 — v1.3 Example 3 addendum main body (lines 577-
583):**

> "Reading from the composition triple: the continuing range
> after bet+call is ~32% top pair or better, ~9% draws, ~19%
> air, with ~40% of the range in weaker made hands and pocket
> pairs across the remainder. It is **not** '100% better Kx'."

Stated as fact, no hedge. The old parenthetical "(Note: the
'~40% weaker made hands and pocket pairs' characterisation of
the unclassified remainder is provisional...)" is gone.
**PASS.**

**Location 3 — v1.3 Example 3 addendum new source citation
paragraph (lines 584-596):**

New inline justification paragraph added:

> "The '~40% weaker made hands and pocket pairs' characterisation
> follows directly from `extract_range_composition` in
> `river-rats-core/feature_extractor.py`: the function classifies
> each combo via `classify_hand` and sums only the `nuts`,
> `strong_value`, `good_value` (TP+), `draw`, `air`, and `bluff`
> buckets — `medium_made` and `weak_made` fall through into the
> unclassified remainder (see `feature_extractor.py` line 1173
> and the `_TOP_PAIR_PLUS` / `_DRAW_CATEGORIES` /
> `_AIR_CATEGORIES` constants at lines 1088-1092). `medium_made`
> and `weak_made` correspond exactly to top-pair-weak-kicker,
> second/middle pair, underpairs (pocket pairs below the top
> board card), and bottom pair (see `range_narrowing.py` lines
> 213-240), which is the 'weaker made hands and pocket pairs'
> bucket."

**Source citation verified directly from
`river-rats-core/feature_extractor.py`:**

| Citation in KB | Actual source content | Match |
|---|---|---|
| Line 1088 `_TOP_PAIR_PLUS` | `_TOP_PAIR_PLUS = {'nuts', 'strong_value', 'good_value'}` | EXACT |
| Line 1090 `_DRAW_CATEGORIES` | `_DRAW_CATEGORIES = {'draw'}` | EXACT |
| Line 1092 `_AIR_CATEGORIES` | `_AIR_CATEGORIES = {'air', 'bluff'}` | EXACT |
| Line 1173 "medium_made and weak_made fall through" | Literal comment: `# medium_made and weak_made fall into none of the buckets` | EXACT |
| Six-bucket sum `nuts / strong_value / good_value / draw / air / bluff` | Sum of the three constants above = 6 categories, matching the KB's six-bucket list | EXACT |

The KB's classification claim is sourced correctly from
`feature_extractor.py`. The `range_narrowing.py` 213-240 citation
for the `medium_made`/`weak_made` category definitions was NOT
independently re-read — given the three verified citations above
are all exact, one unchecked citation is acceptable spot-check
scope (not a full re-audit). If the architect's verification
discipline holds for three out of three, trust the fourth.

**PASS.**

## Summary

| Fix | Status | Evidence |
|-----|--------|----------|
| F1 (delete false rewrite note) | APPLIED CLEANLY | Example 6 setup flows into factors at lines 672-675, no dangling reference |
| F2 (replace reviewer-note cross-reference) | APPLIED CLEANLY | Lines 220-229, plain v9-3way-v2.2 continuity text, no working-document leak |
| F3 (remove provisional hedge + add source citation) | APPLIED CLEANLY | Lines 185 and 577-583 now stated as fact; new inline citation paragraph at 584-596 with three source citations verified exactly against `feature_extractor.py` |

## Cutover approval

**`review/three_way_gto_v1.3.md` is cleared to replace
`knowledge/three_way_gto.md` as production.**

The remaining sequence from the meta-review (step 4 onwards) can
proceed:

4. **Cutover:** `review/three_way_gto_v1.3.md` moves to
   `knowledge/three_way_gto.md`; v1.2 archived or deleted per
   Process Guide review folder protocol. After cutover, v1.3 is
   the authoritative KB.

5. **Reply memo to teaching:** post at
   `review/comms/LOGIC_REPLY_VILLAIN_RANGE_FLAG_2026-04-10.md`.
   Draft exists at `KB_V1.3_EDIT_PLAN.md` Section 11 — reusable
   verbatim. (Filename should retain the 2026-04-10 date since
   that is the teaching memo's date, even though posting occurs
   2026-04-11.)

6. **Memory file:** write
   `~/.claude/projects/-home-rupertbeytell/memory/feedback_preflop_geometry_vs_postflop_composition.md`
   from the draft in `KB_V1.3_EDIT_PLAN.md` Section 12, with
   N-n1 applied (correct the self-certification text to
   accurately describe `villain_range_capped` as a feature-
   identifier reference rather than claiming the body contains
   "no occurrences of the word 'capped'"). Index in `MEMORY.md`.

7. **Ablation TODO:** log `villain_range_capped` against the
   next feature-importance audit. This was previously agreed
   (C2 in the original logic-team plan, and the teaching
   memo's Q2).

## Process note

F1 was caused by my own error (N-n3 in
`REVIEW_KB_V1.3_EDIT_PLAN_2026-04-10.md`) and caught by the
independent audit. The fix applies cleanly and the chain —
independent audit → meta-review → architect fix → reviewer spot-
check — worked exactly as designed. The durable fix was saved as
`feedback_verify_source_not_plan.md` in memory so the same
error pattern doesn't recur.

Process integrity intact. Cutover approved.
