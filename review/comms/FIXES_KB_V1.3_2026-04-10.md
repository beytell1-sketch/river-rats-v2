---
date: 2026-04-10
from: Architect agent
to: Reviewer terminal
re: F1 / F2 / F3 fixes applied to review/three_way_gto_v1.3.md
status: ready for spot-check
---

## Fix 1 — F1 (false BB→SB editorial note deleted)

- Location: `review/three_way_gto_v1.3.md` lines 661-666 (pre-edit).
- Deleted text (literal, two sentences):
  > This rewrite also changes the hero from BB to SB vs a BTN open.
  > Both are valid 3-handed SRP configurations; the SB-vs-BTN setup
  > was chosen so the feature extractor's gauntlet schema runs cleanly
  > on the existing tooling, and the teaching point about OOP value
  > betting a dry high-card board generalises across OOP positions.
- Rationale: the claim is false. v1.2 already had hero=SB at its line
  441; the "rewrite changes hero from BB to SB" note described a
  change that never happened.
- Post-deletion state: Example 6 setup now reads "SB (OOP, first to
  act), 2 opponents (BTN opened, BB called). Pot 90, not facing bet."
  and flows directly into the **Factors:** block. No dangling blank
  line, no broken paragraph, no markdown damage. Example 6 reads
  naturally end-to-end.

## Fix 2 — F2 (Section 1.9 reviewer-note cross-reference replaced)

- Location: `review/three_way_gto_v1.3.md` lines 220-225 (pre-edit),
  inside the **Cross-reference.** paragraph at the end of Section 1.9.
- Removed text (literal):
  > **Cross-reference.** This section replaces the prior use of
  > `villain_range_capped` as a postflop strength indicator in the KB.
  > The feature remains in the pipeline (no retraining forced this
  > session — see reviewer note N2 on the villain_range_flag review),
  > but the labelling agent must not treat it as a postflop signal.
  > See DO NOT Rule #8 for the operative instruction.
- Replacement text (literal, as now in the file at lines 220-229):
  > **Cross-reference.** This section replaces the prior use of
  > `villain_range_capped` as a postflop strength indicator in the KB.
  > The feature remains in the pipeline for continuity with the
  > v9-3way-v2.2 model; no KB-level retraining decision is being made
  > in this revision. Whether to drop `villain_range_capped` from the
  > feature vector in a future training round is a model-training
  > decision, tracked against the next feature-importance audit in
  > `feedback_solver_findings.md`. The labelling agent must not treat
  > it as a postflop signal. See DO NOT Rule #8 for the operative
  > instruction.
- Rationale: the prior text cited an internal working-document note
  ("reviewer note N2 on the villain_range_flag review"), which the KB
  body must not do. The replacement preserves the operative substance
  (feature stays in pipeline, labelling agent must not use it as a
  postflop signal, feature-importance audit is the future forum for
  the decision) without pointing into a review-file note-numbering
  scheme.
- Version history at lines 993-994 (post-edit) retains the
  `KB_V1.3_EDIT_PLAN.md` and `REVIEW_VILLAIN_RANGE_FLAG_2026-04-10.md`
  provenance pointers. Not touched.

## Fix 3 — F3 (remainder characterization verified)

### Verification sources

- `river-rats-core/feature_extractor.py` lines 1085-1213
  (`extract_range_composition`).
- `river-rats-core/range_narrowing.py` lines 163-260
  (`classify_hand`).

### Quoted classification rules (literal, with line numbers)

From `feature_extractor.py`:

```
1087  # Categories that count as "top pair or better" for villain_top_pair_plus_pct
1088  _TOP_PAIR_PLUS = {'nuts', 'strong_value', 'good_value'}
1089  # Categories that count as "drawing"
1090  _DRAW_CATEGORIES = {'draw'}
1091  # Categories that count as "air" (no showdown value, no meaningful draw)
1092  _AIR_CATEGORIES = {'air', 'bluff'}
```

```
1167      if category in _TOP_PAIR_PLUS:
1168          top_pair_plus_weight += freq
1169      elif category in _DRAW_CATEGORIES:
1170          draw_weight += freq
1171      elif category in _AIR_CATEGORIES:
1172          air_weight += freq
1173      # medium_made and weak_made fall into none of the buckets
```

From `range_narrowing.py` `classify_hand`:

```
213  elif 'top_pair' in category_name:
214      # Top pair - check kicker
215      if 'top_kicker' in category_name or 'good_kicker' in category_name:
216          category = 'good_value'  # TPTK or TPGK
217      else:
218          category = 'medium_made'  # Top pair weak kicker
```

```
224  elif category_name in ('second_pair', 'middle_pair', 'underpair'):
225      # Pairs below top pair
226      if strength >= 0.45:
227          category = 'medium_made'
228      else:
229          category = 'weak_made'
```

```
235  elif evaluation.is_made_hand:
236      # Has a pair but not top pair/overpair
237      if strength >= 0.45:
238          category = 'medium_made'  # Decent pair
239      else:
240          category = 'weak_made'    # Bottom/weak pair
```

### Reasoning to MW-30 (KcTh hero, KdJc6s board, 3-way SRP, BB facing CO bet + BTN call)

The composition triple is sums over `_TOP_PAIR_PLUS`, `_DRAW_CATEGORIES`,
and `_AIR_CATEGORIES`. `medium_made` and `weak_made` are explicitly
stated in the line-1173 comment to fall through into the unclassified
remainder. The `classify_hand` branches tell us exactly what ends up
in those two buckets on any board:

- Top pair weak kicker (line 218) — e.g. K2-K9 offsuit that villain
  might continue with.
- Second/middle/underpair strength ≥ 0.45 → `medium_made`; < 0.45 →
  `weak_made` (lines 224-229). On KdJc6s, "second_pair" = Jx (JJ is
  an underpair to K and lands here too depending on `second_pair` vs
  `underpair` naming in `evaluate_hand`), "middle_pair" = 6x, and
  "underpair" = pocket pairs below the top board card (TT, 99, 88,
  77, 55, 44, 33, 22 — 66 is a set and routes to `nuts`/`strong_value`
  via `is_monster`).
- Any other `is_made_hand` not already routed as top pair / overpair
  / two pair (lines 235-240) — bottom pair (weak 6x) etc.

So the "unclassified ~40% remainder" for MW-30 is precisely:
top-pair-weak-kicker + second/middle pair + underpairs (pocket pairs
below the top board card) + bottom pair + any other weak one-pair
hand. Colloquially: **weaker made hands and pocket pairs.**

### Verification outcome

**Outcome A — claim confirmed.** `extract_range_composition` does
fall `medium_made` and `weak_made` through into the unclassified
remainder, and `classify_hand` routes exactly the hand categories
named in v1.3's prose ("weaker made hands and pocket pairs") into
those two buckets. The v1.3 characterisation is correct by
construction of the extractor.

### Actions taken

- **Line 185 (Section 1.9 worked illustration, "roughly 32% strong,
  9% draws, 19% air, and ~40% weaker made hands and pocket pairs in
  the remainder"):** Unchanged. Claim is confirmed; already stated
  as fact; no edit required.
- **Line 574 (Example 3 addendum main body, "with ~40% of the range
  in weaker made hands and pocket pairs across the remainder"):**
  Unchanged. Claim is confirmed; already stated as fact; no edit
  required.
- **Lines 580-583 (provisional hedge in parenthetical):** Removed.
  Replaced with a verification paragraph that cites
  `feature_extractor.py` lines 1088-1092 and 1173 and
  `range_narrowing.py` lines 213-240 as the source of the
  characterisation. The parenthetical hedge ("it requires
  verification against `feature_extractor.py` classification logic
  before v1.4") is gone; the remainder claim is now traceable to
  the extractor constants and the classify_hand branches.

### F3 finding summary (≤5 lines)

`extract_range_composition` sums three buckets (TP+, draws, air) and
explicitly leaves `medium_made` and `weak_made` unclassified
(line 1173). `classify_hand` routes top-pair-weak-kicker,
second/middle pair, underpairs, and bottom pair into those two
buckets (lines 213-240). The "weaker made hands and pocket pairs"
characterisation of the ~40% MW-30 remainder is therefore correct
by construction of the extractor, and the provisional hedge is
unnecessary. Removed.

## Artifact state

- File: `review/three_way_gto_v1.3.md`
- Line count before fixes: 1005
- Line count after fixes: 1013
  (F1: −5 lines; F2: +4 lines; F3: +9 lines net)
- Residual-reference grep (body + version history) for
  `reviewer note`, `N-n2`, `N-n3`, `BB to SB`, `BB→SB`,
  `provisional.*requires verification`: **0 hits.**
- Confirmation: `knowledge/three_way_gto.md` NOT modified.
  md5 before and after this session: `78dd5008d39d1388bcb428faaa4d3869`
  (unchanged).
