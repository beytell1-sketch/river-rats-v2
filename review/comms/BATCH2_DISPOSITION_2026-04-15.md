---
date: 2026-04-15
from: Architecture Expert (mixed-role)
to: Owner
re: Track 5 — disposition of generate_factory_batch2.py blueprint divergence
---

# batch2 disposition: OUT OF SCOPE (no fix spec)

**Verdict: out of scope.** `review/generate_factory_batch2.py` (1308 lines)
does diverge structurally from the Phase-B generator blueprint — it builds
situations through nested `for base, hands, board_id in all_boards: for
cards in hands: SituationSpec(**spec_kwargs)` loops rather than a flat
iteration over a `SituationSpec` list at the blueprint's cited location,
and its output dicts carry `_situation_id` (underscore-prefixed metadata,
written at line 1271) together with the singular `_villain_pos_raw` from
the feature_extractor path rather than a top-level `situation_id` +
plural `villain_positions` list. Specs inside batch2 *do* pass
`villain_positions=[...]` into `SituationSpec`, but that field is
consumed by `build_situation()` / `extract_all_features()` and not
re-emitted in the JSONL (verified: `head -1
training-data/factory_batch2_situations.jsonl` has no
`villain_positions` key). That matches — and in fact pre-dates — the
BP5 generator defect described in `BP_GENERATOR_DEFECT_DIAGNOSIS_2026-04-15.md`.
However: (1) Phase-B blueprint §7 itself marks batch2 **LOW priority**
("labelling complete, regeneration unlikely"); (2) git log shows both
`generate_factory_batch2.py` and `factory_batch2_situations.jsonl`
have a **single commit** each and have not been regenerated since
initial ingest; (3) the only current consumers are
`check_leakage.py` (leakage audit, read-only) and
`review/deterministic_labeller.py` (historical labelling path, not on
the v2.2/v2.3 training hot path — `v2_2_training.csv` does not depend
on batch2 regeneration); (4) `REVIEW_TIER1_COMPLETE_2026-04-15.md`
already recommends dropping the batch2 portion of the blueprint
"unless a v2.3 supplement hand is sourced from batch2". No such
supplement is planned. **Therefore no separate fix spec is warranted:
close batch2 as out of scope for v2.3. Revisit only if (a) a v2.3
supplement sources situations from batch2, or (b) the labelling-
packet generator is re-run against batch2 output, at which point the
same `villain_positions` plural-vs-singular fix used for BP5 would
apply verbatim.**
