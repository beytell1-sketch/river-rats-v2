---
date: 2026-04-17
from: Main terminal (reviewer/orchestrator)
to: Builder
re: HRP=0.00 display bug on d2410 HTML — MW hands must render from re-extracted features
status: BUG REPORT — fix in the HTML renderer, not gating Phase 4 but should not recur
---

# HRP=0.00 Display on d2410_CO_turn

Owner spotted `hero_range_percentile=0.00` on d2410_CO_turn in
the rendered HTML. This is the known HRP test-harness artifact
from `HRP_INVESTIGATION_2026-04-15.md` — the MW test_set_50
feat_dict is missing 6 features, and the old harness silently
defaulted missing keys to 0.

Real HRP after re-extraction: **~0.45** (per
`MW_MISS_BIAS_ANALYSIS_2026-04-15.md` — d2410 is MW miss #4,
HRP 0.45).

## The rendering bug

Whatever generated the d2410 HTML pulled from the **stored
feat_dict** in `test_set_50_labelled.jsonl` rather than
running `extract_all_features()` at render time. Track 1
(commit `b5d84b5`) fixed this at the evaluation boundary but
the HTML renderer is a separate code path and was not
patched.

## Fix

Any HTML renderer that displays MW-test-set features must:

1. Call `extract_all_features()` at render time — same as the
   hardened evaluator in `reference_evaluator.py`
2. OR read from the re-extracted features in
   `MW_MISSES_FEATURES_PREP_2026-04-15.jsonl` (commit `6501cbb`)
   which has all 54 features correctly populated

Do NOT read from the raw `test_set_50_labelled.jsonl`
feat_dict for display purposes — it has the 6-feature gap on
all 50 MW hands.

## Scope

- Affects: d-series MW test hands only (test_set_50)
- Does NOT affect: Phase 3.5 pilot hands (factory-generated,
  features are clean from generation time), FB-40 test hands,
  v2.2 training data
- Does NOT affect: model evaluation numbers (Track 1 harness
  hardening already guards the eval boundary)
- Affects: any future human-readable rendering of MW hands

## Priority

Not gating Phase 4. But the owner is reviewing MW hands for
solver verification prep, and misleading feature displays
will cause confusion. Fix in the HTML generation script
before the next MW-related rendering.

## The poker observation

Owner noted "checking here seems bad" — correct. With real
HRP ~0.45 (mid-range), equity 0.433, villain_checked_back=1,
SPR 1.25, the override clause fires and BET is the
GTO-correct action. This is a canonical example of the
v2.2 defensive-multiway-checked-through CHECK bias that
v2.3 targets.
