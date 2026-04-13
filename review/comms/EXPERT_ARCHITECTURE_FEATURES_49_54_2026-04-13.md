---
date: 2026-04-13
from: Architecture Expert
to: Owner + Builder team
re: Architecture assessment — features 49-54 promotion
---

# Architecture Assessment: Features 49-54

## 1. Is promoting features 49-52 just adding strings to FEATURE_COLUMNS?

No. There are four independent FEATURE_COLUMNS lists that must all be updated in sync:

- `river-rats-core/train_model.py` line 28 — training pipeline (currently stops at feature 48, the 3 deferred features are absent)
- `river-rats-core/gto_model.py` line 33 — inference oracle (already includes 49-53; this is the source of truth for the trained model)
- `river-rats-core/sizing_oracle.py` line 92 — sizing oracle (currently at 48, comment says "same 45 features", stale)
- `river-rats-core/coaching/gto_model.py` line 33 — coaching copy (currently at 48, comment says N_FEATURES = 48)

The `coaching/sizing_oracle.py` and `coaching/gto_model.py` are older copies; they mirror the production files with a lag. Any feature promotion must touch all four.

The `feature_extractor.py` FEATURE_COLUMNS (CSV export surface, line 1012) is a separate list — it currently includes 49-52 but not 53. Feature 53 (`is_preflop_aggressor`) is computed in feature_extractor.py (line 1647) but is not in the extractor's export list. That is a silent gap: the feature is computed but never written to CSV, so `train_model.py` would silently receive 0.0 for it even if the string were added. This must be verified before training.

Summary of touchpoints for features 49-52:
- `train_model.py` FEATURE_COLUMNS: add 4 strings (primary change)
- `sizing_oracle.py` FEATURE_COLUMNS: sync to 53 (or 54 after feature 54 is added)
- `coaching/gto_model.py` FEATURE_COLUMNS: sync to match production
- `coaching/sizing_oracle.py` FEATURE_COLUMNS: sync to match production
- `feature_extractor.py` FEATURE_COLUMNS: confirm feature 53 is present (currently missing from that list)
- Test `test_new_features.py` lines 302-314: hardcoded count assertions (52 and 53) must be updated to match new counts

## 2. What does feature 54 require in feature_extractor.py?

Line 1173 of feature_extractor.py currently has a comment: "medium_made and weak_made fall into none of the buckets." Feature 54 requires:

1. Add a `medium_made_weight` accumulator in the range composition loop (lines 1167-1173)
2. Add an `elif category in _MEDIUM_MADE_CATEGORIES` branch to capture those hands
3. Compute `medium_made_pct` from the weight, parallel to `tp_pct` / `draw_pct` / `air_pct`
4. Add `F.VILLAIN_MEDIUM_MADE_PCT` constant to `feature_keys.py`
5. Write the feature into the features dict in `extract_all_features`
6. Add the string to all four FEATURE_COLUMNS lists

The `_MEDIUM_MADE_CATEGORIES` set must be defined. Based on the briefing description (second pair, bottom pair, weak top pair), this requires confirming what category labels `classify_hand` actually returns for these hand types — the programmer should not assume labels without checking the classify_hand output.

No other structural change is needed. The composition percentages will shift (villain_air_pct drops), but that is the intended correction, not a side-effect.

## 3. Is N_FEATURES hardcoded or auto-detected?

In `gto_model.py` (production): `N_FEATURES = len(FEATURE_COLUMNS)` — auto-derived. Safe.

In `sizing_oracle.py` (production): same pattern, `N_FEATURES = len(FEATURE_COLUMNS)` — auto-derived. Safe.

In `coaching/gto_model.py`: same pattern. Safe.

In `coaching/sizing_oracle.py`: same pattern. Safe.

The comment `# 53` on `gto_model.py` line 60 will become stale but is not functional. The actual runtime value is always `len(FEATURE_COLUMNS)`, so no manual constant needs updating. The inference code at `predict()` also uses `self._n_features = getattr(model, 'n_features_in_', len(FEATURE_COLUMNS))`, which reads feature width from the saved model after training — correct behavior.

## 4. Downstream impacts

**Test infrastructure:** `test_new_features.py` lines 302-314 have hardcoded count assertions (52 for extractor, 53 for gto_model). These will fail and must be updated as part of the promotion work. Treat this as required, not optional.

**Coaching pipeline:** The coaching copies (`coaching/gto_model.py`, `coaching/sizing_oracle.py`, `coaching/feature_extractor.py`) are separate files that lag production. They will not automatically reflect the new features. If the coaching pipeline is exercised during v2.2 testing, these copies need updating too. At minimum, flag them as out-of-sync so reviewers don't treat a coaching-path test failure as a production bug.

**labelling_agent.py and label_3way_situations.py:** These read feature dicts directly, not FEATURE_COLUMNS arrays. No change needed — the new keys will simply be present in the dict.

**reference_evaluator.py:** Does not import FEATURE_COLUMNS. No change needed.

**Recommendation:** Promote all six features. The touchpoints are mechanical and well-contained. The only non-trivial task is feature 54 (requires verifying `classify_hand` category labels for medium/weak made hands before writing the elif branch). All other changes are list additions and count assertion updates.
